"""Enforce the D7 IRI scheme on a slice module (deterministic post-step).

Every PRIMARY class (one carrying ex:pcfID) MUST have IRI ex:P<pcfID>. Agents
occasionally emit readable IRIs (ex:ResolveCustomerComplaint) for primary process
classes instead; this renames them to ex:P<pcfID> and rewrites every reference
(genus fillers, partonomy, bridges, realized-in, etc.) by safe token substitution.
Supporting classes (ICEs/agents/roles/capabilities) carry NO pcfID and are left
with their readable names, which is correct per the scheme.

Usage:  python scripts/normalize_iris.py <slice.ttl>
Exits non-zero (and renames nothing) if two classes share a pcfID (a real error).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rdflib  # noqa: E402

from src.apqc_transform import config  # noqa: E402

EX = config.EX


def normalize(path: Path) -> dict:
    g = rdflib.Graph()
    g.parse(str(path), format="turtle")
    pcf = rdflib.URIRef(EX + "pcfID")

    by_pcf: dict[str, list[str]] = {}
    for s, o in g.subject_objects(pcf):
        by_pcf.setdefault(str(o), []).append(str(s))

    dups = {p: ss for p, ss in by_pcf.items() if len(set(ss)) > 1}
    if dups:
        raise SystemExit(f"DUPLICATE pcfID(s) — fix before normalizing: {dups}")

    # Capabilities (R6 standing-function models) are supporting classes: they may
    # carry pcfID for provenance but keep readable names -- do NOT force them to
    # ex:P<pcfID>. Detect by subclass of a CCO Capability or a "Capability" name.
    CAP_PARENTS = {
        rdflib.URIRef("https://www.commoncoreontologies.org/ont00000568"),  # Org Capability
        rdflib.URIRef("https://www.commoncoreontologies.org/ont00001379"),  # Agent Capability
    }
    rdfs_sub = rdflib.RDFS.subClassOf

    def is_capability(subj: str) -> bool:
        node = rdflib.URIRef(subj)
        if str(subj).endswith("Capability"):
            return True
        for parent in g.transitive_objects(node, rdfs_sub):
            if parent in CAP_PARENTS:
                return True
        return False

    rename: dict[str, str] = {}
    for pid, ss in by_pcf.items():
        s = ss[0]
        if not s.startswith(EX):
            continue
        local = s[len(EX):]
        if local != f"P{pid}" and not is_capability(s):
            rename[local] = f"P{pid}"

    if not rename:
        return {}

    txt = path.read_text(encoding="utf-8")
    for local, target in sorted(rename.items(), key=lambda kv: -len(kv[0])):
        txt = re.sub(rf"\bex:{re.escape(local)}\b", f"ex:{target}", txt)
    path.write_text(txt, encoding="utf-8", newline="\n")
    return rename


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: normalize_iris.py <slice.ttl>")
    p = Path(sys.argv[1])
    renamed = normalize(p)
    print(f"Normalized {len(renamed)} primary IRI(s) to ex:P<pcfID> in {p.name}")
    for local, target in list(renamed.items())[:10]:
        print(f"  ex:{local} -> ex:{target}")
    if len(renamed) > 10:
        print(f"  ... and {len(renamed) - 10} more")
