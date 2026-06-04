"""Derive the process<->agent bridge wiring for one section, deterministically.

Reads the harvest manifest (scripts/harvest_caps_roles.py) and emits:
  - ex:<cap> ex:enablesProcess ex:<proc>      (from the capability's realized-in)
  - ex:<proc> ex:requiresCapability ex:<cap>  (derived inverse -- decision ii)
  - ex:<proc> ex:requiresRole ex:<role>       (from role bearer -> process participant)
  - role-enrichment co-anchors under the CORRECT CCO role subclass, by class:
        Authority Role  cco:ont00000187  (gate/approval/regulatory authority -- the deontic seam)
        Occupation Role cco:ont00000984  (employed positions: analyst, manager, planner, ...)
        Contractor Role cco:ont00000506  (externally engaged providers under contract)
    Relational / party roles (customer, competitor, partner, stakeholder, ...) have
    NO precise CCO parent and are LEFT at bare obo:BFO_0000023 (forcing them under
    Occupation Role would falsely assert employment). Low-confidence picks are flagged.

Also reports: capabilities with no derivable scope (no realized-in) -> need judged
enablesProcess; these are emitted as coverage observations, not invented wiring.

Usage: python scripts/derive_wiring.py <section>   # prints {turtle, report}
"""
from __future__ import annotations
import json, sys, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harvest_caps_roles as H

# --- role classification (heuristic; per-section daemon/human confirms) ---
AUTHORITY = re.compile(r"(Approver|Authority|Regulator|Regulatory|Board|GateKeeper|Approval)", re.I)
OCCUPATION = re.compile(r"(Analyst|Manager|Planner|Officer|Personnel|Engineer|Specialist|"
                        r"Administrator|Auditor|Accountant|Representative|Strategist|Director|"
                        r"Coordinator|Lead|Examiner|Inspector|Adviser|Advisor|Agent\b|Operator|"
                        r"Clerk|Technician|Designer|Developer|Recruiter|Trainer|Buyer|Seller)", re.I)
CONTRACTOR = re.compile(r"(Contractor|Vendor|ServicesProvider|ServiceProvider|Consultant)", re.I)
# explicitly relational / party roles that must NOT be forced under Occupation
RELATIONAL = re.compile(r"(Customer|Competitor|Partner|Stakeholder|Supplier|Owner|Shareholder|"
                        r"Beneficiary|Sponsor|Member|Unit|Subsidiary|Citizen|Public|Community|"
                        r"User|Recipient|Applicant|Claimant|Donor|Investor|Distributor|Employee)", re.I)
ROLE_ANCHOR = {
    "authority": "cco:ont00000187", "occupation": "cco:ont00000984",
    "contractor": "cco:ont00000506", "relational": None,
}

def classify_role(local: str) -> tuple[str, float]:
    if AUTHORITY.search(local):  return "authority", 0.9
    if CONTRACTOR.search(local): return "contractor", 0.7
    if RELATIONAL.search(local): return "relational", 0.8
    if OCCUPATION.search(local): return "occupation", 0.8
    return "relational", 0.4   # default: leave bare, flag low-confidence

def local(iri_q: str) -> str:
    return iri_q.split(":", 1)[1] if ":" in iri_q else iri_q

def derive(section: str) -> dict:
    graphs, recur = H.load_all()
    man = H.harvest_section(section, graphs, recur)
    lines, requires_cap, requires_role, enables, gaps, classifications = [], [], [], [], [], []

    for c in man["capabilities"]:
        if c["realized_in"]:
            for p in c["realized_in"]:
                enables.append((c["iri"], p))
                requires_cap.append((p, c["iri"]))
        else:
            gaps.append({"capability": c["iri"], "reason": "no realized-in restriction; enablesProcess needs a judged scope"})

    role_anchor_lines = []
    for r in man["roles"]:
        kind, conf = classify_role(local(r["iri"]))
        classifications.append({"role": r["iri"], "kind": kind, "confidence": conf,
                                "anchor": ROLE_ANCHOR[kind], "recurs_in": r["recurs_in"]})
        anchor = ROLE_ANCHOR[kind]
        if anchor:
            role_anchor_lines.append(f'{r["iri"]} rdfs:subClassOf {anchor} .   # {kind}'
                                     + ("" if conf >= 0.7 else "   # LOW-CONFIDENCE: confirm"))
        for p in r["participates_processes"]:
            requires_role.append((p, r["iri"]))

    def block(title, triples, pred):
        out = [f"# --- {title} ---"]
        for a, b in sorted(set(triples)):
            out.append(f"{a} {pred} {b} .")
        return "\n".join(out) if len(out) > 1 else ""

    turtle = "\n\n".join(x for x in [
        block("enablesProcess (capability -> process, from realized-in)", enables, "ex:enablesProcess"),
        block("requiresCapability (process -> capability, derived inverse)", requires_cap, "ex:requiresCapability"),
        block("requiresRole (process -> role, from bearer/participant triad)", requires_role, "ex:requiresRole"),
        ("# --- role enrichment co-anchors (correct CCO role subclass) ---\n" + "\n".join(sorted(set(role_anchor_lines)))) if role_anchor_lines else "",
    ] if x)

    return {"section": section, "turtle": turtle,
            "report": {"n_requires_capability": len(set(requires_cap)),
                       "n_requires_role": len(set(requires_role)),
                       "capability_scope_gaps": gaps,
                       "role_classifications": classifications}}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: derive_wiring.py <section>")
    res = derive(sys.argv[1])
    print(res["turtle"])
    print("\n# ===== REPORT =====")
    print("# " + json.dumps(res["report"], ensure_ascii=False).replace("\n", "\n# "))
