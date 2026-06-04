"""Matchability -- the registry routability test family (NOT SHACL).

For every process requirement (ex:requiresCapability / ex:requiresRole /
ex:requiresPermission) authored in the wiring/slices, does some agent in the
fleet (capabilities/agents.json) bear a SATISFYING capability and role?

Satisfaction is species-satisfies-genus: an agent bearing C_a satisfies a
requirement C_p iff C_a rdfs:subClassOf* C_p (a more specific borne competence
satisfies a more general requirement). A process is ROUTABLE iff a SINGLE agent
satisfies ALL of its requirements (one agent performs the process).

Emits a coverage-gap report (a deliverable, not a failure): per-process routable
agents, and the requirements no single agent / no agent at all can meet.

Usage: python scripts/matchability.py            # report to stdout + JSON
"""
from __future__ import annotations
import json, glob
from pathlib import Path
import rdflib
from rdflib import RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
EX = "http://example.org/apqc#"
CCO = ROOT / "vendor" / "cco" / "CommonCoreOntologiesMerged.ttl"
AGENTS = ROOT / "capabilities" / "agents.json"
REQ = {
    "capability": URIRef(EX + "requiresCapability"),
    "role": URIRef(EX + "requiresRole"),
    "permission": URIRef(EX + "requiresPermission"),
}

def q(u: str) -> str:
    return "ex:" + u[len(EX):] if u.startswith(EX) else u
def expand(qn: str) -> URIRef:
    return URIRef(EX + qn[3:]) if qn.startswith("ex:") else URIRef(qn)

def load_graph(with_cco: bool = True) -> rdflib.Graph:
    g = rdflib.Graph()
    for f in ["ontology/capabilities_roles.ttl", "ontology/delivery_processes.ttl",
              "ontology/capabilities_wiring.ttl", *sorted(glob.glob("ontology/slices/apqc_*_0.ttl"))]:
        g.parse(str(ROOT / f), format="turtle")
    if with_cco:
        g.parse(str(CCO), format="turtle")
    return g

def main() -> int:
    g = load_graph()
    agents = json.loads(AGENTS.read_text(encoding="utf-8"))
    # precompute each agent's borne capability/role ancestor sets (subClassOf*)
    fleet = []
    for a in agents:
        caps, roles = set(), set()
        for c in a.get("capabilities", []):
            caps |= {str(x) for x in g.transitive_objects(expand(c), RDFS.subClassOf)}
        for r in a.get("roles", []):
            roles |= {str(x) for x in g.transitive_objects(expand(r), RDFS.subClassOf)}
        fleet.append({"id": a["agent_id"], "cap_closure": caps, "role_closure": roles,
                      "caps": a.get("capabilities", []), "roles": a.get("roles", [])})

    # gather per-process requirements
    procs: dict[str, dict] = {}
    for kind, pred in REQ.items():
        for s, _, o in g.triples((None, pred, None)):
            procs.setdefault(str(s), {"capability": set(), "role": set(), "permission": set()})[kind].add(str(o))

    routable, gaps = [], []
    uncovered_any = {"capability": set(), "role": set(), "permission": set()}
    for p, req in sorted(procs.items()):
        # which single agents satisfy ALL requirements of p?
        sat_agents = []
        for f in fleet:
            ok = (all(c in f["cap_closure"] for c in req["capability"])
                  and all(r in f["role_closure"] for r in req["role"])
                  and not req["permission"])  # permission seam unpopulated -> any perm req is a gap
            if ok and (req["capability"] or req["role"]):
                sat_agents.append(f["id"])
        # per-requirement coverage (by ANY agent) -> distinguishes fleet gap vs no-single-agent
        unmet = {"capability": [], "role": [], "permission": []}
        for kind in ("capability", "role", "permission"):
            clo = "cap_closure" if kind == "capability" else "role_closure"
            for need in sorted(req[kind]):
                covered = kind != "permission" and any(need in f[clo] for f in fleet)
                if not covered:
                    unmet[kind].append(q(need)); uncovered_any[kind].add(q(need))
        entry = {"process": q(p),
                 "requires": {k: sorted(q(x) for x in v) for k, v in req.items() if v}}
        if sat_agents:
            entry["routable_via"] = sat_agents; routable.append(entry)
        else:
            entry["unmet"] = {k: v for k, v in unmet.items() if v}
            gaps.append(entry)

    report = {
        "summary": {"processes_with_requirements": len(procs),
                    "routable": len(routable), "coverage_gaps": len(gaps),
                    "fleet_size": len(fleet)},
        "fleet_gaps_no_agent_bears": {k: sorted(v) for k, v in uncovered_any.items() if v},
        "routable": routable, "gaps": gaps,
    }
    out = ROOT / "ontology" / "reports" / "matchability.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    s = report["summary"]
    print(f"MATCHABILITY  fleet={s['fleet_size']}  reqs-on={s['processes_with_requirements']} "
          f"processes  ROUTABLE={s['routable']}  GAPS={s['coverage_gaps']}")
    print("\nRoutable:")
    for e in routable:
        print(f"  + {e['process']:10} via {', '.join(e['routable_via'])}   {e['requires']}")
    print("\nCoverage gaps (deliverable, not a failure):")
    for e in gaps:
        print(f"  - {e['process']:10} unmet={e['unmet']}")
    print(f"\nFleet gaps (no agent bears): {report['fleet_gaps_no_agent_bears']}")
    print(f"\nreport -> {out.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
