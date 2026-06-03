"""Make slice modules SELF-CONTAINED: inline the canonical act-genus anchors.

The D9 consolidation moved the act genera into apqc-ext.ttl and the slices
imported them. That made slices fragile: validated standalone (without ext),
their process classes float free of any CCO Act (an expert reviewer hit exactly
this). This inlines each slice's referenced genera -- the CANONICAL definitions
from apqc-ext.ttl (so no cross-slice divergence) -- and drops the now-redundant
owl:imports, so every slice validates standalone against CCO alone, like the
frozen reference module. apqc-ext.ttl remains the master registry / generator.

Usage: python scripts/inline_genera.py
"""

from __future__ import annotations

import re
from pathlib import Path

import rdflib
from rdflib import RDFS

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "ontology" / "apqc-ext.ttl"
SLICES = ROOT / "ontology" / "slices"
EX = "http://example.org/apqc#"


def _is_terminator(line: str) -> bool:
    s = re.sub(r"\s+#.*$", "", line.strip())
    return bool(s) and s.endswith(".") and not s.endswith(";") and not s.endswith(",")


def extract_genus_blocks() -> dict[str, str]:
    lines = EXT.read_text(encoding="utf-8").splitlines()
    blocks: dict[str, str] = {}
    i, n = 0, len(lines)
    while i < n:
        m = re.match(r"^(ex:ActOf\w+) a owl:Class\b", lines[i])
        if m:
            start = i
            while i < n and not _is_terminator(lines[i]):
                i += 1
            blocks[m.group(1)] = "\n".join(lines[start: i + 1])
        i += 1
    return blocks


SECTION_HEADER = (
    "####################################################################\n"
    "# ACT GENERA -- SELF-CONTAINED (canonical defs mirrored from\n"
    "# apqc-ext.ttl, the D9 shared registry). Inlined so this module\n"
    "# validates standalone against CCO without merging the extension.\n"
    "####################################################################\n\n"
)


def inline(slice_path: Path, blocks: dict[str, str]) -> list[str]:
    g = rdflib.Graph()
    g.parse(str(slice_path), format="turtle")
    used = sorted(
        f"ex:{str(o)[len(EX):]}"
        for o in set(g.objects(None, RDFS.subClassOf))
        if str(o).startswith(EX + "ActOf") and f"ex:{str(o)[len(EX):]}" in blocks
    )
    if not used:
        return []

    text = slice_path.read_text(encoding="utf-8")
    # drop the (now redundant) live import of the extension
    text = re.sub(r"^[ \t]*owl:imports <http://example\.org/apqc/ext> ;\n", "", text, flags=re.M)

    section = SECTION_HEADER + "\n\n".join(blocks[g] for g in used) + "\n"

    # insert the genus section right after the owl:Ontology statement block
    lines = text.splitlines()
    onto_i = next(i for i, l in enumerate(lines) if "a owl:Ontology" in l)
    end_i = next(i for i in range(onto_i, len(lines)) if _is_terminator(lines[i]))
    out = lines[: end_i + 1] + ["", section.rstrip()] + lines[end_i + 1:]
    slice_path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return used


if __name__ == "__main__":
    blocks = extract_genus_blocks()
    print(f"{len(blocks)} canonical genera available in apqc-ext.ttl")
    for p in sorted(SLICES.glob("apqc_*_0.ttl")):
        used = inline(p, blocks)
        print(f"  {p.name}: inlined {len(used)} genera, import removed" if used
              else f"  {p.name}: no ext genera referenced")
