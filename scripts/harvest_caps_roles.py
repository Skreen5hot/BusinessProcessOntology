"""Harvest the scattered per-slice capability/role classes into a manifest.

Deterministic extraction (no judgement): for one section's slice it pulls every
ex:*Capability and ex:*Role class, its anchors, label, definition, and the
existing realizable wiring already encoded in the slices --
  - capability  -> realized-in target  (obo:BFO_0000054 someValuesFrom <proc>)
                   => the process the capability ENABLES (basis for ex:enablesProcess
                      and the derived ex:requiresCapability)
  - role        -> bearers              (agent rdfs:subClassOf [BFO_0000196 some <role>])
                   and, via those bearers, the processes that have them as
                   participants (BFO_0000057) => basis for the derived ex:requiresRole.
Cross-slice recurrence is computed over ALL slices so the harvest knows which
classes are the 10 shared ones needing one canonical definition.

Usage:
  python scripts/harvest_caps_roles.py <section-number>   # e.g. 1   -> stdout JSON
  python scripts/harvest_caps_roles.py --all              # recurrence summary only
"""
from __future__ import annotations
import json, sys, glob, collections
from pathlib import Path
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

ROOT = Path(__file__).resolve().parents[1]
SLICES = sorted(glob.glob(str(ROOT / "ontology" / "slices" / "apqc_*_0.ttl")))
EX = "http://example.org/apqc#"
BFO_REALIZED_IN = URIRef("http://purl.obolibrary.org/obo/BFO_0000054")
BFO_BEARER_OF = URIRef("http://purl.obolibrary.org/obo/BFO_0000196")
BFO_HAS_PART = URIRef("http://purl.obolibrary.org/obo/BFO_0000057")  # has participant
HAS_CAPABILITY = URIRef("https://www.commoncoreontologies.org/ont00001954")

PFX = {
    "http://example.org/apqc#": "ex:",
    "https://www.commoncoreontologies.org/": "cco:",
    "http://purl.obolibrary.org/obo/": "obo:",
}
def q(u: str) -> str:
    for ns, p in PFX.items():
        if u.startswith(ns):
            return p + u[len(ns):]
    return u

def section_of(path: str) -> str:
    return Path(path).stem.replace("apqc_", "").replace("_0", "")

def _restriction_fillers(g, cls, prop):
    """someValuesFrom fillers of `prop` among the (possibly blank-node) superclasses of cls."""
    out = []
    for sup in g.objects(cls, RDFS.subClassOf):
        if (sup, OWL.onProperty, prop) in g:
            for f in g.objects(sup, OWL.someValuesFrom):
                if isinstance(f, URIRef):
                    out.append(q(str(f)))
    return out

def load_all():
    """Parse every slice once; return {section: graph} and a global recurrence index."""
    graphs = {}
    recur = collections.defaultdict(set)  # local-name -> {sections}
    for sp in SLICES:
        g = rdflib.Graph(); g.parse(sp, format="turtle")
        sec = section_of(sp); graphs[sec] = g
        for s in g.subjects(RDF.type, OWL.Class):
            if not isinstance(s, URIRef) or not str(s).startswith(EX):
                continue
            ln = str(s)[len(EX):]
            if ln.endswith("Capability") or ln.endswith("Role"):
                recur[ln].add(sec)
    return graphs, recur

def harvest_section(sec: str, graphs, recur) -> dict:
    g = graphs[sec]
    caps, roles = [], []
    # index: role -> set of bearer agents; agent -> set of processes that have it as participant
    bearer_of = collections.defaultdict(set)   # role_q -> {agent_q}
    for agent in g.subjects(RDF.type, OWL.Class):
        for r in _restriction_fillers(g, agent, BFO_BEARER_OF):
            bearer_of[r].add(q(str(agent)))
    participant_proc = collections.defaultdict(set)  # agent_q -> {proc_q}
    for proc in g.subjects(RDF.type, OWL.Class):
        for ag in _restriction_fillers(g, proc, BFO_HAS_PART):
            participant_proc[ag].add(q(str(proc)))

    for s in g.subjects(RDF.type, OWL.Class):
        if not isinstance(s, URIRef) or not str(s).startswith(EX):
            continue
        ln = str(s)[len(EX):]
        if not (ln.endswith("Capability") or ln.endswith("Role")):
            continue
        label = next((str(o) for o in g.objects(s, RDFS.label)), None)
        defn = next((str(o) for o in g.objects(s, SKOS.definition)), None)
        anchors = [q(str(o)) for o in g.objects(s, RDFS.subClassOf) if isinstance(o, URIRef)]
        entry = {
            "iri": q(str(s)), "label": label, "definition": defn,
            "anchors": anchors, "recurs_in": sorted(recur[ln]),
        }
        if ln.endswith("Capability"):
            entry["realized_in"] = _restriction_fillers(g, s, BFO_REALIZED_IN)
            caps.append(entry)
        else:
            bearers = sorted(bearer_of.get(q(str(s)), []))
            entry["borne_by"] = bearers
            procs = sorted({p for b in bearers for p in participant_proc.get(b, [])})
            entry["participates_processes"] = procs
            roles.append(entry)
    return {
        "section": sec,
        "n_capabilities": len(caps), "n_roles": len(roles),
        "capabilities": sorted(caps, key=lambda e: e["iri"]),
        "roles": sorted(roles, key=lambda e: e["iri"]),
    }

def main(argv):
    graphs, recur = load_all()
    if argv and argv[0] == "--all":
        rec = {k: sorted(v) for k, v in recur.items() if len(v) > 1}
        print(json.dumps({"recurring": rec, "n_recurring": len(rec),
                          "total_distinct": len(recur)}, indent=2))
        return 0
    if not argv or argv[0] not in graphs:
        sys.exit(f"usage: harvest_caps_roles.py <section in {sorted(graphs)}> | --all")
    print(json.dumps(harvest_section(argv[0], graphs, recur), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
