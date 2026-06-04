"""Audit + apply the judgment-pass output into the curated tables.

Input : capabilities/_judgment.json  (from the judgment workflow):
        { "role_anchors":     [{section, role, anchor, reason}, ...],
          "capability_scope": [{section, capability, enables:[...], reason}, ...] }

Audits (verify-before-assert):
  - every anchor is one of {187, 984, 506} or null
  - every role / capability / scoped process IRI EXISTS as a class in the corpus
  - every scoped capability genuinely has NO realized-in (is a real scope-gap)
  - recurring roles classified by several section-agents are reconciled to one
    anchor (conflicts are reported, not silently resolved)

Writes capabilities/role_anchors.json + capabilities/capability_scope.json
(merging onto the existing seeds) and prints an audit report. Use --check to
audit only (no write).
"""
from __future__ import annotations
import json, sys, glob, collections
from pathlib import Path
import rdflib
from rdflib import RDF, OWL, URIRef

ROOT = Path(__file__).resolve().parents[1]
EX = "http://example.org/apqc#"
JUDGMENT = ROOT / "capabilities" / "_judgment.json"
ROLE_ANCHORS = ROOT / "capabilities" / "role_anchors.json"
CAP_SCOPE = ROOT / "capabilities" / "capability_scope.json"
VALID_ANCHORS = {"cco:ont00000187", "cco:ont00000984", "cco:ont00000506", None}

def corpus_classes() -> set[str]:
    classes = set()
    for sp in glob.glob(str(ROOT / "ontology" / "slices" / "apqc_*_0.ttl")):
        g = rdflib.Graph(); g.parse(sp, format="turtle")
        for s in g.subjects(RDF.type, OWL.Class):
            if isinstance(s, URIRef) and str(s).startswith(EX):
                classes.add("ex:" + str(s)[len(EX):])
    return classes

def scope_gaps() -> set[str]:
    """capabilities with EMPTY realized_in across the corpus (genuine scope-gaps)."""
    sys.path.insert(0, str(ROOT / "scripts")); import harvest_caps_roles as H
    graphs, recur = H.load_all(); gaps = set()
    for sec in graphs:
        for c in H.harvest_section(sec, graphs, recur)["capabilities"]:
            if not c["realized_in"]:
                gaps.add(c["iri"])
    return gaps

def main(argv) -> int:
    j = json.loads(JUDGMENT.read_text(encoding="utf-8"))
    classes = corpus_classes(); gaps = scope_gaps()
    errors, warnings = [], []

    # --- roles: reconcile across sections ---
    by_role = collections.defaultdict(list)
    for a in j.get("role_anchors", []):
        by_role[a["role"]].append((a.get("anchor"), a.get("section"), a.get("reason", "")))
    role_table = {}
    for role, picks in sorted(by_role.items()):
        if role not in classes:
            errors.append(f"role {role} not a class in the corpus"); continue
        anchors = {p[0] for p in picks}
        for an in anchors:
            if an not in VALID_ANCHORS:
                errors.append(f"role {role}: invalid anchor {an!r}")
        valid = [a for a in anchors if a in VALID_ANCHORS]
        if len(anchors) > 1:
            # reconcile: prefer a non-null consensus; report the conflict
            nonnull = [a for a in valid if a]
            chosen = collections.Counter(p[0] for p in picks if p[0]).most_common(1)
            pick = (chosen[0][0] if chosen else None)
            warnings.append(f"role {role} classified {sorted(anchors)} across sections {[p[1] for p in picks]} -> chose {pick}")
            role_table[role] = pick
        else:
            role_table[role] = picks[0][0]

    # --- capability scope ---
    scope_table = {}
    for c in j.get("capability_scope", []):
        cap = c["capability"]; enables = c.get("enables", [])
        if cap not in classes:
            errors.append(f"capability {cap} not a class in the corpus"); continue
        if cap not in gaps:
            warnings.append(f"capability {cap} already has realized-in; scope ignored"); continue
        bad = [p for p in enables if p not in classes]
        if bad:
            errors.append(f"capability {cap}: scoped processes not in corpus: {bad}")
        good = [p for p in enables if p in classes]
        if good:
            scope_table[cap] = good

    # --- report ---
    print(f"roles classified: {len(role_table)}  | capabilities scoped: {len(scope_table)}")
    print(f"anchor distribution: {collections.Counter(role_table.values())}")
    print(f"scope-gaps total {len(gaps)}, scoped {len(scope_table)}, left unscoped {len(gaps)-len(scope_table)}")
    if warnings:
        print("\nWARNINGS:"); [print("  ! " + w) for w in warnings]
    if errors:
        print("\nERRORS:"); [print("  X " + e) for e in errors]
        print("\nABORT: fix _judgment.json and re-run."); return 1
    if "--check" in argv:
        print("\n[check only] not written."); return 0

    # merge onto existing seeds (preserve _doc, keep any pre-set values)
    ra = json.loads(ROLE_ANCHORS.read_text(encoding="utf-8")) if ROLE_ANCHORS.exists() else {}
    cs = json.loads(CAP_SCOPE.read_text(encoding="utf-8")) if CAP_SCOPE.exists() else {}
    ra.update(role_table); cs.update(scope_table)
    ROLE_ANCHORS.write_text(json.dumps(ra, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAP_SCOPE.write_text(json.dumps(cs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nwrote {ROLE_ANCHORS.relative_to(ROOT)} ({len(ra)-1} roles) and "
          f"{CAP_SCOPE.relative_to(ROOT)} ({len(cs)-1} capabilities)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
