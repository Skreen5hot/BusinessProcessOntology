"""APQC notice gate (NOTICE.md): every ontology module that carries PCF content
must state APQC's notice, and no other module may claim it.

A module carries PCF content when it asserts bpo:apqcSourceText or
bpo:hierarchyID (PCF descriptions and positions; bare bpo:pcfID test values in
apqc_bad_examples.ttl are not PCF content). Such a module must have exactly
one dct:rights, equal to config.PCF_RIGHTS. Run by corpus_check.sh.
"""
import glob
import sys
from pathlib import Path

import rdflib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from apqc_transform import config  # noqa: E402

BPO = rdflib.Namespace(config.EX)
DCT_RIGHTS = rdflib.URIRef("http://purl.org/dc/terms/rights")
PCF_PREDICATES = (BPO.apqcSourceText, BPO.hierarchyID)


def main() -> int:
    problems, bearing = [], 0
    for path in sorted(glob.glob(str(ROOT / "ontology" / "**" / "*.ttl"), recursive=True)):
        rel = Path(path).relative_to(ROOT).as_posix()
        if rel.startswith("ontology/reports/"):
            continue
        g = rdflib.Graph().parse(path)
        carries = any(next(g.triples((None, p, None)), None) for p in PCF_PREDICATES)
        rights = [str(o) for o in g.objects(None, DCT_RIGHTS)]
        if carries:
            bearing += 1
            if rights != [config.PCF_RIGHTS]:
                problems.append(f"{rel}: carries PCF content but its dct:rights is not the APQC notice")
        elif config.PCF_NOTICE in "".join(rights):
            problems.append(f"{rel}: claims the APQC notice but carries no PCF content")
    if problems:
        print("[notice]  FAIL")
        for p in problems:
            print("  * " + p)
        return 1
    print(f"[notice]  PASS  {bearing} PCF-bearing modules state APQC's notice (NOTICE.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
