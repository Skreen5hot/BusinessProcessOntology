# Release Notes

## v0.3.0 — Reality-layer corpus complete (2026-06-03)

First complete, expert-reviewed release of the **BFO-2020 / CCO-2.0 ontology of the APQC
Process Classification Framework (Cross-Industry)**. All 13 top-level PCF categories are now
transformed into reality-layer modules, individually reviewed, and consistent corpus-wide.

### Architecture (ADR-001: two-layer model)

- **Catalog layer (deterministic).** Every PCF row is a `skos:Concept` paired with a Descriptive
  Information Content Entity — a faithful, lossless index of the framework
  (`ontology/apqc-catalog.ttl`, 1,921 rows, 19,215 triples).
- **Reality layer (selective).** A BFO **process universal** is minted only where the R5
  bounded-occurrent test passes; standing organizational functions become **Organization
  Capabilities** (R6) rather than processes. Each reality-layer class bridges back to its catalog
  node via the `ex:designatesProcessType` annotation property (preserving OWL DL — no
  ICE-to-class punning).
- **Self-contained slices.** Each of the 13 modules **inlines** the canonical act genera it uses
  from the shared registry (`ontology/apqc-ext.ttl`), so every module validates standalone against
  the pinned CCO/BFO closure with no `owl:imports` and no extension merge.

### What's in this release

| Artifact | Description |
| --- | --- |
| `ontology/slices/apqc_1_0.ttl` … `apqc_13_0.ttl` | 13 reality-layer modules — **43,140 triples**, **~1,823** PCF-derived process universals, **~100** organization capabilities, **1,890** catalog→reality bridges |
| `ontology/apqc-catalog.ttl` | Deterministic catalog layer (1,921 PCF rows) |
| `ontology/apqc-ext.ttl` | Shared registry (D9) of the canonical act genera — single source of truth, mirrored into each slice |
| `ontology/reference/apqc_1_1_1.ttl` | Frozen hand-built template (readable IRIs) |
| `ontology/apqc_shapes.ttl` | SHACL shapes S1–S8 (annotation completeness, anchoring, ICE/aboutness discipline) |
| `src/apqc_transform/validate.py` | Validation harness — Gates A–D |
| `scripts/corpus_check.sh` | Corpus-wide merge + ELK consistency check |
| `scripts/consistency_audit.py` | Cross-slice anchor / drift audit |
| `apqc_to_bfo_cco_methodology.md`, `docs/adr/ADR-001-…md` | Methodology spec + architecture decision record |

### Validation

- **Per slice:** Gate A (rdflib parse) · Gate B (every `cco:`/`obo:` IRI resolves in the vendored
  closure) · Gate C (SHACL, zero violations) · Gate D (ELK reasoner, no unsatisfiable classes) —
  all **PASS** standalone.
- **Corpus-wide:** 13 slices + registry + catalog + CCO merged and reasoned with ELK —
  **consistent, 0 unsatisfiable classes.**
- **CCO pin:** CommonCoreOntologiesMerged **v2.0 (2024-11-06)**.

### Modeling patterns established during review

The 13 per-section reviews converged on a set of corpus-wide conventions (each verified against
the vendored CCO before assertion, per D6):

- **GOLDEN PRINCIPLE** — an act's genus must agree with the kind of ICE it outputs
  (Appraisal/Analysis/Monitoring/Info-Processing → Descriptive/Predictive; Planning/Formulation/
  Selection → Directive).
- **Forecasts** → Predictive ICE (`cco:ont00000626`); forecasting acts → `ex:ActOfForecasting`
  (`cco:ont00000371` + `228`).
- **Finance acts** anchored to CCO's financial-instrument branch — `ex:ActOfFinancialTransaction`
  → Act of Financial Instrument Use (`836`), with precise leaves where unambiguous
  (`449` Remuneration, `884` Loaning); transferred money modeled as `ex:PaymentInstrument`
  (`537`), never the act.
- **Communication boundaries** — solicit-feedback / report-to-audience acts → Representative
  Communication (`379`/`151`), distinguished from report *compilation* (Info Processing `366`).
- **Aboutness** points at reality-layer subjects (e.g. the minted `ex:BusinessProcess` for
  `ex:ProcessAnalysis`), never at an input-data ICE.
- **Standalone-SHACL co-parent / CCO-bridge mechanism** — anchors outside a shape allowlist
  co-assert the nearest allowlisted parent (or rely on each slice's `CCO SUPERCLASS BRIDGES`
  block) so modules validate offline.
- **Shared-class harmonization** — cross-slice classes (e.g. `ex:Budget`, `ex:BusinessStrategy`
  → Directive `965`; `ex:PerformanceMeasure` → Descriptive `853`; `ex:Supplier` → Organization
  `1180`; `ex:Risk` → Realizable Entity `BFO_0000017`) carry one consistent anchor corpus-wide.

### Final consistency pass

A deterministic cross-slice audit (`scripts/consistency_audit.py`) confirmed every genus and
shared-class anchor is consistent across the 13 slices and the registry. It surfaced and fixed one
genuine forecast-pattern drift (`ex:DemandForecast` in section 4) and re-synced the registry to the
section-9 decisions (`ex:ActOfFinancialTransaction` → `836+228`, added `ex:ActOfRemuneration`).
Remaining cross-slice variations are documented as benign (e.g. slice 1's deliberate
`ex:BusinessStrategy ⊑ Plan` refinement; material-class co-parent explicitness).

### Known open decisions (non-blocking)

These are deliberately deferred; none affect validity or corpus consistency:

1. **`ex:ActOfNegotiation` genus** — kept at the neutral Planned Act (`228`); CCO Social Act
   (`1327`) is a defensible alternative that could be adopted corpus-wide.
2. **Product / service split** — `Offering` / `ProductServicePrototype` / `ServiceDeliverySolution`
   are conservatively scoped to the material reading.
3. **Material-output convention** — documented in methodology §10; model left as-is.

### Commit range

`9f3591c` (initial) … `dc255ba` (consistency pass) — 39 commits, all on `main`.
