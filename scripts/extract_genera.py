"""Dump every local act-genus (ex:ActOf*) definition across all slice modules,
grouped by genus, so the consolidation step can reconcile conflicting anchors
into one canonical definition per genus in apqc-ext.ttl.
"""

from __future__ import annotations

import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    slices = sorted(glob.glob(str(ROOT / "ontology" / "slices" / "apqc_*_0.ttl")))
    inv: dict[str, list[dict]] = {}
    for p in slices:
        name = Path(p).name
        txt = Path(p).read_text(encoding="utf-8")
        for m in re.finditer(r"(ex:ActOf\w+) a owl:Class ;(.*?) \.", txt, re.S):
            genus, block = m.group(1), m.group(0).strip()
            anchors = re.findall(r"rdfs:subClassOf (cco:ont\d+)", block)
            inv.setdefault(genus, []).append(
                {"slice": name, "anchors": anchors, "block": block}
            )

    out = ROOT / "build" / "genera_inventory.md"
    out.parent.mkdir(exist_ok=True)
    lines = ["# Act-genus inventory across all 13 slices", ""]
    for genus, occ in sorted(inv.items(), key=lambda kv: -len(kv[1])):
        anchor_set = {tuple(o["anchors"]) for o in occ}
        conflict = " **<-- ANCHOR CONFLICT**" if len(anchor_set) > 1 else ""
        lines.append(f"## {genus}  ({len(occ)} slices){conflict}")
        lines.append("")
        seen = set()
        for o in occ:
            if o["block"] in seen:
                continue
            seen.add(o["block"])
            lines.append(f"--- from {o['slice']} (anchor {o['anchors']}) ---")
            lines.append(o["block"])
            lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(inv)} distinct genera, {sum(len(v) for v in inv.values())} blocks -> {out}")
    print("conflicts:", [g for g, occ in inv.items()
                          if len({tuple(o['anchors']) for o in occ}) > 1])


if __name__ == "__main__":
    main()
