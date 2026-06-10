"""Build a compact, greppable index of the corpus -- navigate the graph cheaply.

Emits ontology/index/corpus_index.tsv: one row per ex:/perf: class or individual
across the 13 slices + apqc-ext + apqc-catalog + the capability/role layer, with
its kind, label, anchors, hierarchy, and the Phase-1 wiring. Agents Grep this file
instead of Read-ing whole slices (matching lines only -> far fewer tokens).

Columns (tab-separated):
  iri  kind  section  hierarchy  pcf  label  parents  wiring  definition

  kind     process | capability | role | ice | agent | act-genus | catalog |
           individual | property | marker | other
  section  slice number 1-13, or ext | catalog | cap | delivery | wiring
  parents  named rdfs:subClassOf anchors (prefixed), ';'-joined
  wiring   process -> "req-cap:X;req-role:Y"; capability -> "enables:P1,P2,…"

Usage:  python scripts/build_index.py        (regenerate after any corpus change)
"""
from __future__ import annotations
import glob, collections
from pathlib import Path
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

ROOT = Path(__file__).resolve().parents[1]
EX = "http://example.org/apqc#"
PERF = "http://example.org/apqc/perf#"
OUT = ROOT / "ontology" / "index" / "corpus_index.tsv"

PFX = {EX: "ex:", PERF: "perf:", "https://www.commoncoreontologies.org/": "cco:",
       "http://purl.obolibrary.org/obo/": "obo:"}
def q(u: str) -> str:
    for ns, p in PFX.items():
        if u.startswith(ns):
            return p + u[len(ns):]
    return u

# CCO anchor ids that mark an ICE (for kind=ice classification, no closure needed)
ICE_ANCHORS = {"cco:ont00000958", "cco:ont00000853", "cco:ont00000965", "cco:ont00000626",
               "cco:ont00000686", "cco:ont00001163", "cco:ont00000537", "cco:ont00000974"}
AGENT_ANCHORS = {"cco:ont00001017", "cco:ont00001180", "cco:ont00000300"}
CAP_ANCHORS = {"cco:ont00001379", "cco:ont00000568"}

def section_of(path: str) -> str:
    n = Path(path).stem
    if n.startswith("apqc_") and n.endswith("_0"):
        return n.replace("apqc_", "").replace("_0", "")
    return {"apqc-ext": "ext", "apqc-catalog": "catalog",
            "capabilities_roles": "cap", "delivery_processes": "delivery",
            "capabilities_wiring": "wiring"}.get(n, n)

def main() -> int:
    files = sorted(glob.glob(str(ROOT / "ontology" / "slices" / "apqc_*_0.ttl"))) + [
        str(ROOT / "ontology" / f) for f in
        ("apqc-ext.ttl", "apqc-catalog.ttl", "capabilities_roles.ttl",
         "delivery_processes.ttl", "capabilities_wiring.ttl")]

    # 1) parse every module once; collect requires*/enablesProcess wiring from ALL of
    #    them (capabilities_wiring.ttl AND delivery_processes.ttl AND any slice), so the
    #    wiring column reflects every authored direction, not just the harvest overlay.
    graphs = []
    req_cap = collections.defaultdict(list); req_role = collections.defaultdict(list)
    enables = collections.defaultdict(list)
    for f in files:
        g = rdflib.Graph(); g.parse(f, format="turtle")
        graphs.append((section_of(f), g))
        for s, _, o in g.triples((None, URIRef(EX + "requiresCapability"), None)):
            req_cap[q(str(s))].append(q(str(o)))
        for s, _, o in g.triples((None, URIRef(EX + "requiresRole"), None)):
            req_role[q(str(s))].append(q(str(o)))
        for s, _, o in g.triples((None, URIRef(EX + "enablesProcess"), None)):
            enables[q(str(s))].append(q(str(o)))

    rows = {}            # iri -> row dict (dedup across files; first definition wins)
    for sec, g in graphs:
        for s in set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, OWL.NamedIndividual)) \
                | set(g.subjects(RDF.type, OWL.AnnotationProperty)) | set(g.subjects(RDF.type, OWL.ObjectProperty)):
            if not isinstance(s, URIRef) or not (str(s).startswith(EX) or str(s).startswith(PERF)):
                continue
            iri = q(str(s))
            if iri in rows:
                continue
            label = next((str(o) for o in g.objects(s, RDFS.label)), "")
            defn = next((str(o) for o in g.objects(s, SKOS.definition)), "")
            hier = next((str(o) for o in g.objects(s, URIRef(EX + "hierarchyID"))), "")
            pcf = next((str(o) for o in g.objects(s, URIRef(EX + "pcfID"))), "")
            parents = [q(str(o)) for o in g.objects(s, RDFS.subClassOf) if isinstance(o, URIRef)]
            types = {q(str(o)) for o in g.objects(s, RDF.type)}
            ln = iri.split(":", 1)[1]
            # classify
            if "owl:AnnotationProperty" in types or "owl:ObjectProperty" in types or \
               str(OWL.AnnotationProperty) in types or str(OWL.ObjectProperty) in types:
                kind = "property"
            elif "owl:NamedIndividual" in types or any(t.startswith("cco:") for t in types):
                kind = "catalog" if ln.startswith("PCF_") else "individual"
            elif ln.endswith("Capability") or set(parents) & CAP_ANCHORS or "ex:Capability" in parents:
                kind = "capability"
            elif ln.endswith("Role") or "ex:Role" in parents:
                kind = "role"
            elif ln.startswith("ActOf"):
                kind = "act-genus"
            elif pcf or any(p.startswith("ex:ActOf") for p in parents):
                kind = "process"
            elif set(parents) & ICE_ANCHORS:
                kind = "ice"
            elif set(parents) & AGENT_ANCHORS:
                kind = "agent"
            elif iri in ("ex:Capability", "ex:Role"):
                kind = "marker"
            else:
                kind = "other"
            # wiring summary
            w = []
            if iri in req_cap: w.append("req-cap:" + ",".join(sorted(set(req_cap[iri]))))
            if iri in req_role: w.append("req-role:" + ",".join(sorted(set(req_role[iri]))))
            if iri in enables: w.append("enables:" + ",".join(sorted(set(enables[iri]))))
            rows[iri] = {
                "iri": iri, "kind": kind, "section": sec, "hierarchy": hier, "pcf": pcf,
                "label": label.replace("\t", " "), "parents": ";".join(parents),
                "wiring": ";".join(w), "definition": defn.replace("\t", " ").replace("\n", " ")[:160],
            }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["iri", "kind", "section", "hierarchy", "pcf", "label", "parents", "wiring", "definition"]
    lines = ["\t".join(cols)]
    for iri in sorted(rows, key=lambda k: (rows[k]["kind"], k)):
        lines.append("\t".join(rows[iri][c] for c in cols))
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_kind = collections.Counter(r["kind"] for r in rows.values())
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} terms")
    print("  " + "  ".join(f"{k}={n}" for k, n in sorted(by_kind.items())))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
