"""Corpus-wide consistency audit (read-only). Deterministic checks:
  1. header/version/imports/stale-prose drift per file
  2. genus (ex:ActOf*) named-anchor consistency across slices + registry
  3. shared-class (>=2 files) named-anchor consistency
  4. standalone-SHACL co-parent presence for out-of-allowlist anchors
"""
import glob, re, pathlib
import rdflib
from rdflib import RDFS, URIRef
from rdflib.namespace import OWL

EX = "http://example.org/apqc#"
CCO = "https://www.commoncoreontologies.org/"
BFO = "http://purl.obolibrary.org/obo/"

slices = sorted(glob.glob("ontology/slices/apqc_*.ttl"),
                key=lambda p: int(re.search(r"apqc_(\d+)_", p).group(1)))
registry = "ontology/apqc-ext.ttl"
files = slices + [registry]

def short(u):
    s = str(u)
    if s.startswith(EX): return "ex:" + s[len(EX):]
    if s.startswith(CCO): return "cco:" + s[len(CCO):]
    if s.startswith(BFO): return "obo:" + s[len(BFO):]
    return s

# class_name -> {file: frozenset(named parents)}
anchors = {}
for fp in files:
    g = rdflib.Graph().parse(fp, format="turtle")
    fn = pathlib.Path(fp).name
    for s in set(g.subjects(rdflib.RDF.type, OWL.Class)):
        if not isinstance(s, URIRef) or not str(s).startswith(EX):
            continue
        named = frozenset(short(o) for o in g.objects(s, RDFS.subClassOf)
                          if isinstance(o, URIRef))
        if not named:
            continue
        anchors.setdefault(short(s), {})[fn] = named

print("="*70); print("1. HEADER / VERSION / IMPORTS / STALE-PROSE DRIFT"); print("="*70)
stale_pat = re.compile(r"REUSED from apqc-ext|validator merges|merged in for validation|"
                       r"DEFINED IN apqc-ext|local definitions (have been )?removed|"
                       r"PROPOSE-EXT: promote|NEW ACT-GENUS PROPOSALS|owl:imports|"
                       r'versionInfo "0\.[012]\.', re.I)
for fp in files:
    txt = pathlib.Path(fp).read_text(encoding="utf-8")
    fn = pathlib.Path(fp).name
    ver = re.search(r'owl:versionInfo "([^"]+)"', txt)
    hits = []
    for m in stale_pat.finditer(txt):
        ln = txt[:m.start()].count("\n") + 1
        hits.append(f"L{ln}:{m.group(0)[:40]}")
    flag = "" if (ver and ver.group(1) == "0.3.0" and not hits) else "  <<<"
    print(f"{fn:20} ver={ver.group(1) if ver else '?':7}{flag}")
    for h in hits: print(f"      {h}")

print(); print("="*70); print("2. GENUS (ex:ActOf*) ANCHOR CONSISTENCY"); print("="*70)
for name in sorted(anchors):
    if not name.startswith("ex:ActOf"): continue
    perfile = anchors[name]
    sets = set(perfile.values())
    mark = "  <<< DIVERGENT" if len(sets) > 1 else ""
    reg = perfile.get("apqc-ext.ttl")
    print(f"{name:28} in {len(perfile):2} files{mark}")
    if len(sets) > 1 or mark:
        for fn, st in sorted(perfile.items()):
            print(f"      {fn:20} {sorted(st)}")
    elif reg is None:
        print(f"      (not in registry) anchor={sorted(next(iter(sets)))}")

print(); print("="*70); print("3. SHARED-CLASS (>=2 files) ANCHOR CONSISTENCY"); print("="*70)
divergent = 0
for name in sorted(anchors):
    if name.startswith("ex:ActOf"): continue
    perfile = anchors[name]
    if len(perfile) < 2: continue
    sets = set(perfile.values())
    if len(sets) > 1:
        divergent += 1
        print(f"{name:34}  <<< DIVERGENT across {len(perfile)} files")
        for fn, st in sorted(perfile.items()):
            print(f"      {fn:20} {sorted(st)}")
print(f"\n  shared classes in >=2 files: {sum(1 for n,p in anchors.items() if not n.startswith('ex:ActOf') and len(p)>=2)}; divergent: {divergent}")

print(); print("="*70); print("4. CO-PARENT CHECK (out-of-allowlist anchors needing a co-parent)"); print("="*70)
S2 = {"cco:ont00000366","cco:ont00000636","cco:ont00000511","cco:ont00000228"}
ICE = {"cco:ont00000958","cco:ont00000853","cco:ont00000965"}
# process genera outside S2 must co-assert 228; predictive 626 must co-assert 853; material CCO must co-assert BFO_0000040
PROC_OUTSIDE = {"cco:ont00000379","cco:ont00000151","cco:ont00000371","cco:ont00000836",
                "cco:ont00000449","cco:ont00000884","cco:ont00000137","cco:ont00001334",
                "cco:ont00001327","cco:ont00000433","cco:ont00000345","cco:ont00000234",
                "cco:ont00000402","cco:ont00000133","cco:ont00000566","cco:ont00000950",
                "cco:ont00000970","cco:ont00000051","cco:ont00000908"}
issues = 0
for name, perfile in sorted(anchors.items()):
    for fn, st in perfile.items():
        if (st & PROC_OUTSIDE) and "cco:ont00000228" not in st:
            print(f"  {name} in {fn}: {sorted(st)} -- process anchor outside S2, missing 228 co-parent"); issues += 1
        if "cco:ont00000626" in st and "cco:ont00000853" not in st:
            print(f"  {name} in {fn}: {sorted(st)} -- Predictive 626 missing 853 co-parent"); issues += 1
        if "cco:ont00000537" in st and "obo:BFO_0000040" not in st:
            print(f"  {name} in {fn}: {sorted(st)} -- Financial Instrument 537 missing BFO_0000040 co-parent"); issues += 1
print(f"\n  co-parent issues: {issues}")
