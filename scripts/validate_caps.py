"""Capability-layer SHACL validation (PHASE1 test families 1 + 2; Gate E).

Structural (C1-C4): the foundation module alone + CCO closure.
Coherence  (C5-C7): module + delivery + wiring overlay + all slices + CCO
                    (the "process graph loaded" family) -- so requiresCapability/
                    requiresRole/requiresPermission resolve to real classes.

Both run with the CCO closure in the data graph (transitive subClassOf* needs it).
Exit 0 iff zero violations across both passes.
"""
from __future__ import annotations
import sys, glob, time
from pathlib import Path
import rdflib
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
SHAPES = ROOT / "ontology" / "capabilities_roles_shapes.ttl"
CCO = ROOT / "vendor" / "cco" / "CommonCoreOntologiesMerged.ttl"
FOUNDATION = ["ontology/capabilities_roles.ttl", "ontology/delivery_processes.ttl"]
OVERLAY = ["ontology/capabilities_wiring.ttl", *sorted(
    f"ontology/slices/{Path(p).name}" for p in glob.glob(str(ROOT / "ontology/slices/apqc_*_0.ttl")))]

def run(label: str, files: list[str]) -> int:
    g = rdflib.Graph()
    for f in files:
        g.parse(str(ROOT / f), format="turtle")
    g.parse(str(CCO), format="turtle")
    t0 = time.time()
    conforms, _rg, txt = validate(g, shacl_graph=str(SHAPES), advanced=True,
                                  inference="none", meta_shacl=False)
    viol = txt.count("Severity: sh:Violation")
    print(f"[{label}] {len(g)} triples  conforms={conforms}  violations={viol}  ({time.time()-t0:.1f}s)")
    if not conforms:
        print(txt[:4000])
    return 0 if conforms else 1

def main() -> int:
    rc = run("structural C1-C4  (module + CCO)", FOUNDATION)
    rc |= run("coherence  C1-C7  (module + wiring + slices + CCO)", FOUNDATION + OVERLAY)
    print("\nCAPABILITY LAYER: " + ("OK -- zero violations" if rc == 0 else "VIOLATIONS"))
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
