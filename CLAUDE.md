# CLAUDE.md — project grounding

BFO-2020 / CCO-2.0 ontology of the **APQC Process Classification Framework (Cross-Industry, v7.4)**.
Deeper docs: `apqc_to_bfo_cco_methodology.md` (the spec), `docs/adr/ADR-001-…md` (architecture
decision), `RELEASE_NOTES.md` (v0.3.0 state), `PHASE0.md` (repo/daemon setup).

## Architecture (ADR-001: two layers)

- **Catalog layer** — `ontology/apqc-catalog.ttl`. Deterministic: every PCF row → `skos:Concept` +
  Descriptive ICE (1,921 rows). Lossless index of the framework.
- **Reality layer** — `ontology/slices/apqc_1_0.ttl … apqc_13_0.ttl`, one per top-level PCF
  category. A BFO **process universal** is minted only where the **R5** bounded-occurrent test
  passes; standing functions become **Organization Capabilities** (**R6**), not processes. Each
  reality-layer class bridges to its catalog node via the `ex:designatesProcessType` annotation
  property (keeps OWL DL; no ICE-to-class punning).
- **Self-contained slices** — each slice **inlines** the canonical act genera it uses from the
  registry `ontology/apqc-ext.ttl` (the D9 single source of truth, mirrored into slices). No
  `owl:imports`; every slice validates standalone against the pinned CCO/BFO closure.

## Validation — ALWAYS run before committing a slice change

```
PYTHONPATH=src python -m apqc_transform.validate ontology/slices/apqc_N_0.ttl   # Gates A–D
bash scripts/corpus_check.sh        # merge all 13 + ext + catalog + CCO, reason with ELK
python scripts/consistency_audit.py # cross-slice anchor / drift audit
```

- **Gate A** rdflib parse · **B** every `cco:`/`obo:` IRI resolves in vendored closure ·
  **C** SHACL (`ontology/apqc_shapes.ttl`, shapes S1–S8), zero violations ·
  **D** ELK reasoner (`tools/robot.jar`), no unsatisfiable classes.
- **Gate C does NOT merge CCO** — it validates the slice alone. Each slice's
  `# 1b. CCO SUPERCLASS BRIDGES` block locally asserts the chains the shapes need offline
  (e.g. `371⊑228`, `626⊑853`). This is why a class anchored to an out-of-allowlist CCO term still
  passes: the bridge (or an explicit co-parent) carries it to an allowlisted parent.
- **CCO pin:** CommonCoreOntologiesMerged **v2.0 (2024-11-06)**, vendored under `vendor/cco/`
  (gitignored — fetch per `vendor/cco/README.md`). `tools/robot.jar` likewise fetched, not committed.

## Conventions that hold corpus-wide (verify before changing)

- **D6 verify-before-assert** — never assert a `cco:`/`obo:` IRI without grepping
  `vendor/cco/CommonCoreOntologiesMerged.ttl` to confirm its label, definition, and parent chain.
  Reviews (external, fed one slice at a time) often over-reach; turn back claims that don't verify,
  with evidence.
- **GOLDEN PRINCIPLE** — an act's genus agrees with the ICE kind it outputs:
  Appraisal/Analysis/Monitoring/Info-Processing → Descriptive (`853`) / Predictive (`626`);
  Planning/Formulation/Selection → Directive (`965`).
- **SHACL anchor allowlists** — S2 process anchors `{366,636,511,228}`; S3/S4 ICE
  `{958,853,965}` + `BFO_0000040` (material). Anchor outside the allowlist ⇒ co-assert the nearest
  allowlisted parent locally (or rely on the bridge block).
- **Forecasts** → Predictive ICE `626` (+`853` co-parent); forecasting acts → `ex:ActOfForecasting`
  (`371`+`228`). **Money** transferred = `ex:PaymentInstrument` (`537`), not the act.
- **Shared classes are harmonized corpus-wide** (changing one risks a disjoint collision):
  `ex:Budget`/`ex:BusinessStrategy` → `965`; `ex:PerformanceMeasure` → `853`; `ex:Supplier` → `1180`;
  `ex:Risk` → `BFO_0000017`. Fix a definition/anchor *contradiction* by correcting the text, not by
  diverging the anchor.
- **Commits** — one slice/topic per commit; validate first; direct-to-`main` is fine (single-author
  repo); end messages with `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
  One-shot fix scripts are written to `scripts/_fix*.py`, run, then deleted.

## Verified CCO IRIs (the ones reached for constantly)

Full table in methodology §6 and `src/apqc_transform/config.py` (`CCO` dict). Hot set:
`853` Descriptive ICE · `965` Directive ICE · `626` Predictive ICE (⊑853) · `958` ICE ·
`366` Info-Processing · `636` Appraisal · `511` Planning · `371` Act of Prediction · `345` Measuring ·
`379` Representative Communication · `151` Reporting · `402` Communication · `228` Planned Act ·
`836` Financial-Instrument-Use · `537` Financial Instrument · `1017` Agent · `1180` Organization
(⊑ Group-of-Agents `300`, an Object Aggregate — **not** ⊑ Agent) · `1379` Agent Capability ·
`568` Organization Capability · `1954` has capability · `1777` has process part · `1921` has input ·
`1986` has output · `1808` is about. BFO: `0000015` process · `0000040` material entity ·
`0000017` realizable entity · `0000023` role · `0000054` realized in · `0000196` bearer of.

## CURRENT PHASE — capability/role bridge **DELIVERED** (`ontology/capabilities_*.ttl`)

**Authoritative brief: `PHASE1.md`.** The process→agent dispatch bridge is built and validated
across all 13 sections. Governing distinction: **Capability** (`cco:ont00001379` Agent Capability —
competence, feasibility filter) ≠ **Role** (`obo:BFO_0000023`) ≠ **Process**. Matching is
**species-satisfies-genus** (`subClassOf*`); **`568 ⊑ 1379`** so slice Organization Capabilities
already reach Agent Capability (match on "reaches 1379," slices left at 568). The four gating
decisions were settled: (i) leave slice caps at 568; (ii) author `ex:enablesProcess`, **derive**
`ex:requiresCapability`; (iii) delivery universals live in `delivery_processes.ttl`; (iv) the
capability layer is a **merge-only shared overlay** (no slice imports it).

**Artifacts (in `ontology/`):**
- `capabilities_roles.ttl` — foundation: `ex:Capability`/`ex:Role` markers; `ex:enablesProcess`/
  `ex:bearsPermission` (annotation) + `ex:requiresCapability`/`ex:requiresRole`/`ex:requiresPermission`
  (object properties — range enforced by SHACL C5–C7, **not** `rdfs:range`, to avoid forcing
  entailments into the merged corpus). `requiresPermission` seam declared but **unpopulated** (RDM/IEE
  owns the permission catalogue, `cco:ont00000751`).
- `delivery_processes.ttl` — `AuthorRoadmap`/`AuthorImplementationPlan` (⊑ `ex:ActOfFormulation`) +
  `ApproveImplementationPlan` gate act. (The "agile-loop" set PHASE1 §6b cites does not exist in the
  methodology, which ends at §12; left as a scope note, not invented.)
- `capabilities_roles_shapes.ttl` — C1–C7. `capabilities_wiring.ttl` — **generated** merge-only overlay:
  354 `requiresCapability` + 197 `requiresRole` + 197 `enablesProcess` + 62 role enrichment anchors.

**Pipeline (deterministic, reproducible):** `scripts/harvest_caps_roles.py` (manifest) →
`scripts/derive_wiring.py` (heuristic draft) → judgment tables `capabilities/role_anchors.json` +
`capabilities/capability_scope.json` → `scripts/assemble_wiring.py` (regenerates the wiring; **edit
the tables, not the ttl**) → `scripts/validate_caps.py` (C1–C7) + `scripts/matchability.py`
(routability + coverage-gap report) + `corpus_check.sh` (ELK).

**Role enrichment taxonomy** (refines the brief's blunt "Occupation/Authority"): Authority `187`
(deontic seam — 4 roles: Regulatory/Regulator/GovernmentBody/CertificationAuthority) / Occupation
`984` (44) / Contractor `506` (6) / **relational-party left bare** `BFO_0000023` (33 — customer,
competitor, partner, stakeholder, supplier, board, function roles; CCO has no parent, forcing
Occupation would falsely assert employment). All 87 distinct roles classified; all 10 cross-slice
recurrences converged to one canonical definition each.

**Validate the layer:** `python scripts/validate_caps.py` (C1–C7 zero violations) ·
`python scripts/matchability.py` (12-agent fleet: 60 routable / 385 gaps over 445 required processes) ·
`bash scripts/corpus_check.sh` EXIT 0 (now merges the capability layer + wiring).

**Remaining / handoff:** 6 standing capabilities have no scopeable process (honest gaps); the 12-agent
`agents.json` is a representative demo fleet, not a real roster; `requiresPermission` + the RDM/IEE
permission catalogue are future work.

## Open decisions from v0.3.0 (non-blocking, may resurface here)

`ex:ActOfNegotiation` genus (kept `228`; Social Act `1327` is a defensible corpus-wide alternative) ·
product/service split (conservative material reading) · material-output convention (methodology §10).
