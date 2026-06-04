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

## CURRENT PHASE — capability/role module (`capabilities_roles.ttl`)

The process→agent bridge. Today, capabilities and roles are declared **per-slice and scattered**:
**111 `*Capability`** classes (⊑ `cco:ont00000568` Organization Capability; base `ex:Capability`) and
**87 `*Role`** classes (⊑ `obo:BFO_0000023` Role). 10 of them recur across slices (e.g. `CustomerRole`
in 7 slices, `SupplierRole`/`RegulatoryAuthorityRole` in 4) — duplicated, not shared.

Existing wiring: an Organization **has capability** (`cco:ont00001954`) some `*Capability`; a capability
is **realized in** (`obo:BFO_0000054`) the acts that perform it (R6); an Agent **bears** (`obo:BFO_0000196`)
a `*Role`. **S7** (`NoRoleInGDCShape`) forbids an ICE/GDC from bearing a role — roles inhere only in
independent continuants (Agent/Organization).

New in this phase (do **not** exist yet — grep confirms zero occurrences):
`ex:requiresCapability` and `ex:requiresRole` — object properties on **process** classes pointing at
capability/role classes. The registry maps to the new module.

Decisions the phase must settle (none decided yet):
1. **Consolidation** — does `capabilities_roles.ttl` become the single home for the 198 capability/role
   classes (slices reference it), or a shared layer alongside the still-self-contained slices? How does
   this interact with the no-`owl:imports` self-containment rule and Gate-C-without-CCO?
2. **Property semantics** — domain/range of `requiresCapability` (process → Organization Capability)
   and `requiresRole` (process → Role); relation to the existing `has capability` / `realized in` /
   `bearer of` wiring (a `requires*` is a TBox necessity on the universal, distinct from the ABox
   realization). Watch OWL-DL / SHACL implications.
3. **Dedup + harmonization** — the 10 recurring roles/capabilities need one canonical definition
   (same lesson as the shared-class harmonization above).
4. **Validation** — extend the Gate-C shapes (a `requires*` analogue of S2/S3 anchoring) and re-run
   `corpus_check.sh` after each change.

## Open decisions from v0.3.0 (non-blocking, may resurface here)

`ex:ActOfNegotiation` genus (kept `228`; Social Act `1327` is a defensible corpus-wide alternative) ·
product/service split (conservative material reading) · material-output convention (methodology §10).
