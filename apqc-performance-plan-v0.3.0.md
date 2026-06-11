# APQC Performance Layer — Hardened Specification

```text
Document: APQC Performance Layer Plan
Version:  v0.3.0
Status:   Approved baseline (supersedes v0.2.0)
Purpose:  Ontology and implementation specification
Scope:    Planning and formal commitments; not a TTL file
Editor:   Revised under delegated authority; corrections grounded against the
          vendored CCO v2.0 (2024-11-06) closure and the live v0.3.0 corpus
          (catalog + 13 reality slices + the Phase-1 capability/role layer).
```

> **Why v0.3.0.** v0.2.0 was architecturally sound but several anchors and integration
> points were asserted, not verified. This revision grounds every CCO/IAO/PROV reference
> against the deployed closure and the real corpus IRIs, reuses the existing act-genus
> registry (`apqc-ext.ttl`) and capability/role layer instead of re-minting, and settles
> the five open architecture questions (ABox locus, module/merge strategy, provenance
> vocabulary, process-aggregate typing, the deontic seam). Every change is a decision in §0.

---

## 0. Decision Log

D1–D17 are carried from v0.2.0 unchanged except where a v0.3.0 decision below supersedes them
(noted inline). D18–D27 are new and binding for the first TTL build.

| # | Decision | Resolution | Rejected / superseded |
|---|----------|------------|----------------------|
| D1 | Type/instance bridge | Reality-layer process classes annotated with their APQC catalog element; observations are about named process-aggregate individuals typed by those classes (§4.1, refined by **D21**) | OWL punning of APQC elements |
| D2 | Class reuse | Every minted class subclasses a named BFO/CCO parent via the alignment table (§4.2); **exact IRIs are now verified, not deferred** (see D26) | Free-standing hierarchy |
| D3 | Directive-to-act relation | Specifications/rules connect to acts via `prescribes`/`prescribed by`, never `has input` (§4.3) | Specs as inputs |
| D4 | Playbook realization | `ActionExecutionAct prescribed by ActionPlaybook`; `realizes` reserved for BFO realizable entities | ICE `realizes` (category error) |
| D5 | KPI identity over time | `KpiLineage`; versioned specs are immutable individuals linked to one lineage (§4.4) | "The KPI" = current spec |
| D6 | Versioning pattern | Immutable per-version individuals + succession links; no time-qualified triples on one individual (§4.5) | Mutable dated individuals |
| D7 | Role accountability over time | Reified `RoleAssignment` with effective/retirement dates (§4.5) | Direct agent→role triples |
| D8 | Maturity status over time | Reified `ActionabilityStatusAssertion` (§4.5) | Status as mutable property |
| D9 | Mapping classes | `CandidateKpiMapping` merged into `KpiProcessMapping`; candidacy is a status (§5.1) | Two classes + promotion step |
| D10 | Decision context | First-class `DecisionContext` with identity conditions (§5.1) | Annotation string |
| D11 | Observation→spec link | Minted `perf:conformsToSpecification`, declared derivable from the act chain (§4.3) | Undeclared "conforms to" |
| D12 | Naming convention | All act classes end in `Act`; uniform suffixes | Mixed suffixes |
| D13 | MVP scope rule | A class is in the MVP iff exercised by the §10/§7 validation instance data | "Useful someday" inclusion |
| D14 | Dimensions | Dimension values MUST be IRIs to reference-data individuals (§4.7) | Stringly-typed dimensions |
| D15 | Temporal representation | `MeasurementPeriod` individuals with `xsd:date` bounds, anchored to **`bfo:BFO_0000008` temporal region** (§4.6, see D26) | Bare period literals |
| D16 | Validation tooling | SHACL for all record classes; every competency question paired with SPARQL (§10) | OWL-only |
| D17 | Provenance | Ingestion provenance tracked; source licensing verified before verbatim ingestion (§4.8, vocabulary set by **D20**) | Untracked ingestion |
| **D18** | **ABox locus** | The performance ontology is **TBox-only**. Process-aggregate individuals, observations, periods, records, role assignments, status assertions are a **separate deployment artifact**, validated against this ontology's SHACL + SPARQL at deploy time. `corpus_check.sh` and Gates A–D stay TBox-pure (§3.1). | Instances committed into the corpus graph |
| **D19** | **Module & merge strategy** | One module `ontology/apqc-performance.ttl`: a **merge-only shared overlay** (no slice imports it), **self-contained** (it inlines the act genera it reuses, mirroring the slice convention), merged into `corpus_check.sh` for ELK. A dedicated shape file `ontology/apqc_performance_shapes.ttl` (P-shapes) + a `*_bad_examples` fixture; wired into the gate runner as **Gate E** (§3.1, §8.4). | Standalone unmerged module; or imports |
| **D20** | **Provenance vocabulary** | Use **DCTERMS** (`dcterms:replaces`/`isReplacedBy`/`source`/`isVersionOf`) for succession and source links, plus the minimal minted `perf:` properties in the §4.3 register. **PROV-O is NOT vendored** into the closure; do not depend on it (reproducibility/closure-hygiene — §11 methodology pins every external dependency). PROV is neither `cco:` nor `obo:`, so it is *not* mechanically caught by Gate B; the discipline, not a gate, is the reason. | Importing un-pinned PROV-O |
| **D21** | **Process-aggregate typing** | A measured individual is typed by a **process universal that genuinely has it as an instance** — never a catalog ICE (no punning), never a classless group. **Leaf-grained KPI →** type by the reality-layer **leaf class `ex:P<pcfID>`**. **Group-grained KPI →** the performance layer mints a **thin aggregate process universal** `ex:<Name>Process ⊑ bfo:process (BFO_0000015)`, bridged to the catalog group; its instances' `cco:has_process_part` are the leaf-process instances. The reality slices are untouched (ADR-001 R3: groups stay catalog-only). (§4.1) | One leaf for a group (under-covers); punned ICE; instance-of a classless group |
| **D22** | **Act genera (reuse + GOLDEN PRINCIPLE)** | The six acts anchor to **existing** genera with output-kind agreement: `KpiMeasuringAct ⊑ cco:ont00000345`; `KpiAnalysisAct`/`SignalDetectionAct ⊑ ex:ActOfAnalysis (⊑366)`; `DecisionAct ⊑ cco:ont00000228`; `ActionExecutionAct ⊑ ex:ActOfImplementation (⊑228)`; `LearningReviewAct ⊑ cco:ont00000636`. **CCO has no `ActOfAnalyzing`/`ActOfDeciding`/`ActOfSelection` — verified absent; reuse `apqc-ext.ttl`.** (§4.2, §5.4) | `⊑ cco:Act` (too generic for S2 allowlist + GOLDEN PRINCIPLE); nonexistent CCO act names |
| **D23** | **Real bridge IRIs + reuse the existing bridge** | Catalog elements are **`ex:PCF_<pcfID>`** (`cco:ont00000853` + `skos:Concept`); reality classes are **`ex:P<pcfID>`**. The catalog→reality bridge **already exists**: `ex:designatesProcessType` (ADR-001 R4). `perf:definedByApqcElement` is declared as its **inverse** (annotation), not a parallel mechanism. (§4.1) | Fictional `apqc:10.3-MaintainAssets` IRIs; a second, unrelated bridge |
| **D24** | **Reuse existing classes; plug into the Phase-1 taxonomy** | `ex:ProcessOwnerRole` **already exists** (slice 13) — reuse and harmonize, never re-mint. New perf roles carry Phase-1 enrichment anchors (Occupation `984` / Authority `187`) in `capabilities/role_anchors.json` so they are matchable. (§5.5) | Re-minting `ProcessOwnerRole` (disjoint-collision risk) |
| **D25** | **The deontic seam** | `DecisionOwnerRole ⊑ Authority Role (cco:ont00000187)` is the landing site for Phase 1's unpopulated `requiresPermission` seam: a `DecisionAct`/approval is where an Action Permission (`cco:ont00000751`) binds. The seam is **declared here, populated by RDM/IEE** — the performance layer does not author the permission catalogue. (§5.5, §4.3) | Permissions invented in this layer; or seam ignored |
| **D26** | **Verified anchor corrections** | Verified present in CCO v2.0: Designative ICE `ont00000686`, Measurement ICE `ont00001163` (base; **not** `164`, which is "Minimum Ordinal Measurement ICE"), Algorithm `ont00000653` (⊑ `965`), Act of Measuring `ont00000345` (⊑ `228`), Descriptive `ont00000853`, Directive `ont00000965`, ICE `ont00000958`, `cco:occurs_at` `ont00001918`. **IAO `plan/objective specification` dropped** in favor of Directive ICE `965` (the corpus's universal directive anchor). (§4.2) | Unverified parents; IAO terms not labeled in the closure |
| **D27** | **Source investigation is governed, not ad hoc** | A repeatable onboarding pipeline (§4.9) with a candidate-source register and a six-step per-source checklist (licensing gate → APQC-relevance → metric depth → format → dedup → outcome). Sources are **evidence** (`KpiSourceRecord`), never **identity** (`KpiLineage`). **FinOps Foundation** (FinOps Framework KPIs + FOCUS cost/usage schema; `github.com/finopsfoundation`) added as a candidate for APQC 9.x/8.x. | Adopting sources case-by-case with no licensing gate, relevance test, or dedup |

---

## 1. Purpose

The `apqc-performance` layer extends the APQC process knowledge graph into an actionable process
intelligence layer, above two existing layers:

- **Catalog layer** (`ontology/apqc-catalog.ttl`): the APQC hierarchy as `skos:Concept` + Descriptive
  ICE individuals (`ex:PCF_<pcfID>`), with hierarchy IDs, element IDs, labels, definitions, structure.
- **Reality layer** (`ontology/slices/apqc_1_0.ttl … apqc_13_0.ttl`): BFO/CCO process **universals**
  (`ex:P<pcfID>`), input/output ICEs, participant roles, and Organization Capabilities — plus the
  Phase-1 capability/role dispatch bridge.

The performance layer adds measurement, analysis, signal, decision, action, and learning semantics.
The governed chain (unchanged from v0.2.0):

```text
APQC Process (catalog element / reality universal / measured individual)
→ KpiSourceRecord → KpiProcessMapping (status: candidate → … → learning-enabled)
→ KpiMeasurementSpecification (version of a KpiLineage) → KpiImplementationSpecification
→ KpiMeasuringAct → KpiObservation → KpiAnalysisAct → AnalysisResult
→ SignalDetectionAct → DetectedSignal → DecisionAct → DecisionRecord
→ ActionExecutionAct → ActionRecord → Follow-up KpiObservation
→ LearningReviewAct → LearningRecord
```

The goal is not to attach KPI names to processes; it is to make APQC process knowledge measurable,
interpretable, governable, and actionable. Dashboards are downstream presentation artifacts of this
chain, never the source of truth.

## 2. Design Principles

The layer preserves these distinctions as separate classes (metric-collapse control):

```text
KPI lineage ≠ measurement spec ≠ implementation spec ≠ measuring act ≠ observation
≠ analysis result ≠ detected signal ≠ decision record ≠ action record ≠ learning record
Dashboard tile ≠ any of the above
```

Three reuse disciplines govern the build (the third is the v0.3.0 sharpening that caught the v0.2.0
misses):

1. **Relation reuse.** Prefer `is about`, `has input`, `has output`, `has participant`, `bearer of`,
   `prescribes` before minting object properties. Minted properties live in the closed §4.3 register.
2. **Class reuse.** Every minted class subclasses a **verified** BFO/CCO parent (§4.2). No free-standing
   classes.
3. **Genus reuse (new).** Act classes reuse the corpus's existing act-genus registry
   (`apqc-ext.ttl`: `ex:ActOfAnalysis`, `ex:ActOfImplementation`, …) and obey the **GOLDEN PRINCIPLE**
   (an act's genus agrees with the descriptive/directive/measurement kind of its output ICE). CCO is
   verified for the genus *before* a CCO name is used; where CCO lacks one (analysis, selection,
   monitoring), the corpus already mints it — reuse, never duplicate.

## 3. Layering & Module Architecture

- **Catalog layer** — what work exists, where in the APQC hierarchy, its APQC-defined scope.
- **Reality layer** — what kind of work it is; roles, I/O ICEs, capabilities.
- **Performance layer** — how the work is measured, governed, implemented, observed, analyzed,
  signalled, decided, acted on, and reviewed.

### 3.1 Module, merge, and the TBox/ABox split (D18, D19)

- **One TBox module:** `ontology/apqc-performance.ttl`, namespaces `perf:`
  (`http://example.org/apqc/perf#`) for layer-local terms and `ex:` (`http://example.org/apqc#`) where
  it reuses corpus terms. **Self-contained** (it inlines the `apqc-ext` genera it reuses, exactly as
  the slices do) so it validates standalone against the pinned CCO closure.
- **Merge-only overlay:** no slice `owl:imports` it; it is merged into `scripts/corpus_check.sh`
  (alongside the capability layer) so it cannot perturb the v0.3.0 ELK closure unnoticed. It bridges
  to reality (`ex:P…`) and catalog (`ex:PCF_…`) by **annotation**, so the merge stays OWL-DL clean.
- **The ABox is a separate deployment artifact (D18).** Process-aggregate individuals, observations,
  periods, records, role assignments, and status assertions are **not** committed into the corpus and
  are **not** seen by Gates A–D / `corpus_check.sh`. The ontology ships the **types + SHACL shapes +
  SPARQL competency queries**; a deployment validates its own instance graph against them. This keeps
  the corpus TBox-pure (its invariant since v0.3.0) and makes the performance layer reusable across
  many deployments without entangling their data.
- **Validation (Gate E):** `ontology/apqc_performance_shapes.ttl` (P-shapes for the TBox: anchor
  reachability, genus/output agreement, register closure) + `apqc_performance_bad_examples.ttl`
  (the mandated regression fixture). Instance-level shapes (record completeness, dimension-as-IRI,
  maturity-level conformance) ship with the ontology but **run at the deployment**, over the ABox.

## 4. Formal Commitments

### 4.1 Type/Instance Bridge (real IRIs; D21, D23)

The hard problem: a catalog element is a reference-model ICE, but observations are about actual work at
actual sites in actual periods. The binding pattern, with the corpus's real IRI scheme:

1. **Catalog elements are ICEs.** `ex:PCF_19238` ("10.3 Maintain assets") is a `cco:ont00000853`
   Descriptive ICE + `skos:Concept`. It is never the subject of an observation.
2. **Reality universals carry the bridge — reusing the existing one.** The ADR-001 R4 bridge
   `ex:designatesProcessType` (catalog → reality) already links them. `perf:definedByApqcElement` is
   declared `owl:inverseOf`-style **annotation** (reality → catalog) for query convenience:

   ```text
   ex:PCF_19238  ex:designatesProcessType  ex:P19245 .         # existing (slice 10)
   ex:P19245     perf:definedByApqcElement  ex:PCF_19238 .      # convenience inverse (annotation)
   ```
3. **Observation subjects are measured-process individuals**, typed per **D21**:

   ```text
   # group-grained KPI (10.3 as a whole): a thin aggregate universal, perf-layer only
   ex:AssetMaintenanceProcess a owl:Class ; rdfs:subClassOf obo:BFO_0000015 ;   # bfo:process
       perf:definedByApqcElement ex:PCF_19238 .
   ex:SiteA-AssetMaintenance-2026-05 a ex:AssetMaintenanceProcess ;
       cco:occurs_at ex:SiteA ; perf:coversPeriod ex:Period-2026-05 .           # ABox (deployment)
   ```

   For a **leaf-grained** KPI the individual is typed directly by the reality leaf class
   (e.g. `a ex:P10947` "Perform preventative asset maintenance") — no new class needed.
4. **Observations are about individuals, never types.**
   `KpiObservation is_about ex:SiteA-AssetMaintenance-2026-05`.

Bridge query path (no punning, either granularity):
`observation → is_about → individual → rdf:type → process universal → perf:definedByApqcElement →
catalog element ← perf:hasMappedProcess ← KpiProcessMapping`.

**Why this is BFO-clean (the A4 concern):** the measured individual instantiates a *genuine process
universal* with real instances — that is precisely what universals are for, so BFO/CCO reviewers have
no objection. What they reject — punning the catalog ICE, or `rdf:type` to a group that has no class —
is exactly what D21 forbids. The aggregate universal lives in the **performance layer**, not the
reality slices, so ADR-001's "groups are catalog-only" invariant is preserved; the aggregate's
`cco:has_process_part` ties it to the leaf processes for drill-down.

### 4.2 Class Alignment Table (verified against CCO v2.0, 2024-11-06)

Every MVP class subclasses a verified parent. "✓" = IRI confirmed present in the deployed closure.

| Performance class | Verified parent |
|---|---|
| KpiSourceRecord, KpiProcessMapping, DecisionContext, RoleAssignment | `cco:ont00000853` Descriptive ICE ✓ |
| KpiLineage | `cco:ont00000686` Designative ICE ✓ |
| ActionabilityStatus / ActionabilityStatusAssertion | `cco:ont00000958` ICE ✓ (statuses are named individuals) |
| KpiMeasurementSpecification, KpiImplementationSpecification, TargetSpecification, ThresholdSpecification, AnalysisPatternSpecification, SignalDetectionRule, DecisionRule, ActionPlaybook | `cco:ont00000965` Directive ICE ✓ |
| FormulaSpecification | `cco:ont00000653` Algorithm ✓ (verified `653 ⊑ 965` Directive ICE — no co-anchor needed) |
| KpiObservation | `cco:ont00001163` Measurement ICE ✓ (base class, verified; `164`/`1010` are its narrow ordinal leaves — do not use them) |
| AnalysisResult, DetectedSignal, DecisionRecord, ActionRecord, LearningRecord | `cco:ont00000853` Descriptive ICE ✓ |
| KpiMeasuringAct | `cco:ont00000345` Act of Measuring ✓ |
| KpiAnalysisAct, SignalDetectionAct | `ex:ActOfAnalysis` ✓ (apqc-ext, ⊑ `cco:ont00000366`) — **CCO has no Act of Analyzing** |
| DecisionAct | `cco:ont00000228` Planned Act ✓ (see §5.4 / D25 — CCO has no Act of Deciding/Selection) |
| ActionExecutionAct | `ex:ActOfImplementation` ✓ (apqc-ext, ⊑ `cco:ont00000228`) |
| LearningReviewAct | `cco:ont00000636` Act of Appraisal ✓ |
| KpiOwnerRole, DataStewardRole, ActionOwnerRole | `obo:BFO_0000023` Role, enriched `cco:ont00000984` Occupation |
| DecisionOwnerRole | `obo:BFO_0000023` Role, enriched `cco:ont00000187` Authority (deontic seam, D25) |
| ProcessOwnerRole | **reuse `ex:ProcessOwnerRole`** (slice 13; already Occupation `984`) — do not re-mint |
| MeasurementPeriod | `obo:BFO_0000008` temporal region (verify a CCO temporal-interval subclass at build; else BFO core) |

Rule: if CCO already provides an exact match, reuse it directly (the entry becomes an equivalence note).
**Genus reuse is mandatory for acts** — the corpus's S2 SHACL anchor allowlist is `{366,636,511,228}`
and the GOLDEN PRINCIPLE is enforced; `⊑ cco:Act` will not pass.

### 4.3 Relation Patterns and Minted Relations Register

**Directives prescribe; data flows** (unchanged backbone). Act → genus → output, GOLDEN-PRINCIPLE-aligned:

```text
KpiMeasuringAct (345)        prescribed by KpiImplementationSpecification
                            has input source data; has output KpiObservation (Measurement ICE)
KpiAnalysisAct (ActOfAnalysis) prescribed by AnalysisPatternSpecification
                            has input KpiObservation(s); has output AnalysisResult (Descriptive)
SignalDetectionAct (ActOfAnalysis) prescribed by SignalDetectionRule
                            has input Observation/AnalysisResult; has output DetectedSignal (Descriptive)
DecisionAct (228 Planned Act) prescribed by DecisionRule
                            has input DetectedSignal; has participant DecisionOwnerRole bearer
                            has output DecisionRecord (Descriptive)
ActionExecutionAct (ActOfImplementation) prescribed by ActionPlaybook
                            has input DecisionRecord; has participant ActionOwnerRole bearer
                            has output ActionRecord (Descriptive)
LearningReviewAct (636 Appraisal) has input ActionRecord + follow-up Observations
                            has output LearningRecord (Descriptive)
```

`realizes` is reserved for BFO realizables; it never targets an ICE.

**External vocabularies (DCTERMS only — D20):** `dcterms:replaces` / `dcterms:isReplacedBy` (version
succession), `dcterms:isVersionOf` / `dcterms:hasVersion` (lineage↔version where useful),
`dcterms:source` (a spec or source record derived from an external resource). **No PROV-O.** These are
neither `cco:` nor `obo:`, so they are unconstrained by Gate B, but per the reproducibility discipline
the build records the DCTERMS version it pins.

**Minted Relations Register** — the closed list for v0.3.0. Adding one requires showing no
BFO/CCO/DCTERMS relation suffices, then registering it.

| Property | Domain → Range | Rationale |
|---|---|---|
| perf:definedByApqcElement | reality universal → catalog element (annotation; inverse of `ex:designatesProcessType`) | Query-convenience bridge; OWL-DL safe |
| perf:hasMappedProcess | KpiProcessMapping → catalog element | `is about` cannot distinguish the two ends of a mapping |
| perf:hasMappedIndicator | KpiProcessMapping → KpiLineage | the other end |
| perf:specifiesIndicator | KpiMeasurementSpecification → KpiLineage | binds a versioned spec to its identity node |
| perf:implements | KpiImplementationSpecification → KpiMeasurementSpecification | spec-to-spec; not aboutness, not prescription |
| perf:conformsToSpecification | KpiObservation → KpiMeasurementSpecification | materialized shortcut, derivable from the act chain; declared so queries need not walk it |
| perf:coversPeriod | observation / measured individual → MeasurementPeriod | retire if a CCO temporal relation verifies at build |
| perf:hasStatus | ActionabilityStatusAssertion → ActionabilityStatus individual | controlled-vocabulary link |
| perf:assignsRole / perf:assignedToAgent / perf:assignmentScope | RoleAssignment → Role / Agent / governed object | reified assignment needs three typed ends |
| perf:hadIngestionSource | KpiSourceRecord → external-source individual | provenance of ingestion; DCTERMS `source` is value-typed, this is the typed-individual form (replaces `prov:hadPrimarySource`) |

Ten entries (nine from v0.2.0 minus the dropped `prov:`-shaped one, plus `perf:implements` promoted
from prose and `perf:hadIngestionSource` replacing the PROV link). Closed for the MVP build.

### 4.4 KPI Identity: KpiLineage

Unchanged from v0.2.0. `KpiLineage` (now verified `cco:ont00000686` Designative ICE) designates one
indicator across all spec versions; identity-stable content only (preferred/alt labels, stable id).
Everything mutable lives on the versioned `KpiMeasurementSpecification`. "Current approved spec" is a
query (`?s perf:specifiesIndicator ?lineage` not the object of any `dcterms:replaces`).

### 4.5 Versioning Pattern

Unchanged from v0.2.0 except provenance vocabulary (D20: `dcterms:replaces` for succession,
`dcterms:isVersionOf`/`dcterms:source` for derivation; no `prov:wasRevisionOf`). Immutable per-version
individuals; reified `RoleAssignment` and `ActionabilityStatusAssertion`; records born immutable,
superseded only by a correction that `dcterms:replaces` the original; every `KpiObservation` carries
its period, creation date, and the producing implementation-spec version.

### 4.6 Temporal Representation (D15, D26)

`MeasurementPeriod` individuals anchored to **`bfo:BFO_0000008` temporal region** (the build verifies
whether a CCO temporal-interval subclass is present and prefers it), with `startDate`/`endDate`
(`xsd:date`) and a label. No bare string periods.

### 4.7 Dimension Representation

Unchanged: dimension **values are IRIs** to reference-data individuals, never literals — SHACL-enforced
(at the deployment, D18). The MVP ships a small **reference-data module** stub (sites, asset classes,
teams, criticality, priority) as named individuals; the measurement spec declares the legal
reference-data classes (a structured field, not a class in MVP). This is the structural control against
metric collapse re-entering through stringly-typed dimensions.

### 4.8 Source Provenance (D17, D20)

`KpiSourceRecord` individuals carry `perf:hadIngestionSource` → the external-source individual,
a retrieval date, and a source-type controlled-vocabulary individual (OpenKPIs, APQC-suggested,
FinOps Foundation, internal, vendor, regulatory). Approved specs derived from a source record link
back via `dcterms:source`. **Build step 0 verifies each source's licensing** before verbatim ingestion
of labels, descriptions, or formulas. Source records remain candidates/evidence until placed into
enterprise context via the chain in §1. New sources enter only through the governed investigation
process in **§4.9**.

### 4.9 Source Investigation & Onboarding (D27)

KPI sources are not adopted ad hoc; they pass a **repeatable onboarding pipeline** so that every
candidate is licensing-cleared, APQC-relevant, and deduplicated before it produces a single
`KpiSourceRecord`. The discipline is the same as the rest of the factory: a source is **evidence**
(`KpiSourceRecord`), never **identity** (`KpiLineage`).

**Candidate Source Register** (seeded; extended per deployment):

| Source | Scope / what it provides | License (verify at build step 0) | APQC areas | Status |
|---|---|---|---|---|
| OpenKPIs | Cross-industry KPI library (labels, definitions, often formulas) | TBD — verify before verbatim ingestion | broad / cross-industry | candidate |
| APQC measures | APQC's own suggested measures attached to PCF elements | APQC terms | cross-industry (1–13) | candidate |
| **FinOps Foundation** | **FinOps Framework** (cloud-financial-management capabilities + KPIs: cost allocation coverage, forecast accuracy, commitment/discount coverage, unit economics, anomaly rate, …) and **FOCUS** (a normalized cost-and-usage **data schema** — a strong fit for the implementation-spec data layer and dimension-as-IRI design). `github.com/finopsfoundation`, `finops.org`. | tooling MIT/Apache-2.0 (confirmed); **Framework content license to be confirmed** | **9.x Manage Financial Resources; 8.x Manage IT** | **candidate** |
| Internal / vendor / regulatory | Per-deployment metric catalogues, vendor KPI packs, regulatory reporting metrics | per source | per deployment | placeholder |

**Per-source investigation checklist** (each step gates the next; record the outcome on the source's
register row and, on adoption, as `KpiSourceRecord` provenance):

1. **Licensing & provenance (the build-step-0 gate).** Can we ingest labels/definitions/formulas, and
   under what attribution/share-alike terms? Record license + retrieval date. *A source that cannot be
   cleared is **rejected**, not quietly used.* (FinOps tooling is MIT/Apache-2.0; the Framework content
   repo's license is verified here specifically before its KPI text is ingested.)
2. **APQC relevance mapping.** Which catalog elements (`ex:PCF_<pcfID>`) / reality processes do its
   metrics target? A source with no APQC mapping is **out of scope** (this is an APQC performance layer,
   not a generic KPI warehouse). FinOps → primarily slice 9 (treasury/accounting/cost) and slice 8 (IT).
3. **Metric depth.** Does it supply formula / numerator / denominator / grain, or only labels? This caps
   how far up the §6 maturity model a derived mapping can climb (labels-only → stalls at Level 1 Defined).
4. **Format.** Structured and machine-ingestible (FOCUS-style schemas, CSV/JSON KPI registers) vs prose.
   A normalized schema (FOCUS) additionally informs the `KpiImplementationSpecification` data layer.
5. **Overlap / dedup.** Does the candidate metric duplicate an existing `KpiLineage`? If so, attach a new
   `KpiSourceRecord` as additional evidence to that lineage — **do not mint a second lineage** (D5).
6. **Outcome.** Adopt → candidate `KpiSourceRecord`(s) + candidate `KpiProcessMapping`(s) at Level 0; or
   reject with a recorded reason. Either way the register row is updated, so the investigation backlog is
   auditable, not lost.

This makes "what other sources should we consider?" a standing, governed question with a written trail,
rather than a one-off decision. Adding a source to the register is cheap; promoting it past step 1 is the
gate.

## 5. MVP Class Set

**Inclusion rule (D13):** in the MVP iff exercised by the §7 validation instance data. 34 classes in
six groups (Specifications, Records, Acts, Roles, plus source/identity/governance infra and reference
data). Everything else deferred (§11). Group contents are as v0.2.0 §5.1–§5.3 except the corrections
below.

### 5.4 Act layer — genus assignments (D22)

```text
KpiMeasuringAct     ⊑ cco:ont00000345 Act of Measuring          → KpiObservation (Measurement ICE)
KpiAnalysisAct      ⊑ ex:ActOfAnalysis (⊑ cco:ont00000366)      → AnalysisResult (Descriptive)
SignalDetectionAct  ⊑ ex:ActOfAnalysis (⊑ cco:ont00000366)      → DetectedSignal (Descriptive)
DecisionAct         ⊑ cco:ont00000228 Planned Act               → DecisionRecord (Descriptive)
ActionExecutionAct  ⊑ ex:ActOfImplementation (⊑ cco:ont00000228) → ActionRecord (Descriptive)
LearningReviewAct   ⊑ cco:ont00000636 Act of Appraisal          → LearningRecord (Descriptive)
```

**`DecisionAct` is anchored at the generic Planned Act `228`, not Act of Selection (D25).** The GOLDEN
PRINCIPLE tension is real: a choice from candidates *prescribes* (directive output), but `DecisionRecord`
as specified (selected option, **rejected options, rationale, date**) is a *descriptive* audit ICE.
`228` is neutral on output kind — the corpus's established move for "settle a matter" acts (cf.
`ex:ActOfResolution`, `ex:ActOfAdministration`, both `⊑ 228`). The **directive force flows through the
selected `ActionPlaybook`** (itself a Directive ICE) that `prescribes` the `ActionExecutionAct`; the
decision's descriptive record need not itself be directive. If a deployment wants the selected option as
a first-class directive, mint `DecisionDirective ⊑ 965` as a second output and anchor `DecisionAct ⊑
ex:ActOfSelection` — recorded here as the deliberate alternative, deferred from MVP.

If a dedicated `ex:ActOfDetection` (signal detection) or `ex:ActOfMonitoring` is later wanted, it is a
PROPOSE-EXT to `apqc-ext.ttl` (human-approved), not a silent local mint.

### 5.5 Role layer (D24, D25)

```text
KpiOwnerRole       (Occupation 984)  governs a measurement specification
DataStewardRole    (Occupation 984)  data definitions, quality, lineage, implementation support
DecisionOwnerRole  (Authority 187)   authorized to make/approve decisions on signals  ← deontic seam
ActionOwnerRole    (Occupation 984)  executes/coordinates selected actions
ProcessOwnerRole   REUSE ex:ProcessOwnerRole (slice 13; Occupation 984)  the process itself
```

Roles inhere in agents per BFO; accountability links to governed objects only through `RoleAssignment`
(§4.5). The five roles register in the Phase-1 `capabilities/role_anchors.json` so the dispatch
matchability layer can route them. **`DecisionOwnerRole`** is the explicit landing site for Phase 1's
`requiresPermission` seam: an Action Permission (`cco:ont00000751`) binds at a `DecisionAct`/approval
gate. The permission catalogue and gate conflict-resolution remain **RDM/IEE's to author** — declared
here, populated there.

## 6. Actionability Maturity Model

Unchanged from v0.2.0. Maturity is a property of a **KpiProcessMapping**, asserted through dated
`ActionabilityStatusAssertion`s (never of a KPI globally); seven `ActionabilityStatus` individuals
(Level 0 Candidate … Level 6 Learning-enabled). Each level has a SHACL shape checking the surrounding
graph actually satisfies it; an overstated status fails validation. **These level shapes run over the
ABox at the deployment (D18).**

## 7. MVP Walkthrough: APQC 10.3 Maintain Assets (real IRIs)

Target: APQC `10.3 Maintain assets` = catalog `ex:PCF_19238` (ProcessGroup), reality universals
`ex:P19239 … ex:P19257` in slice 10 (10.3.1 Plan / 10.3.2 Manage / 10.3.3 Perform). Chosen for its
concrete operational entities (assets, work orders, schedules, teams, technicians, downtime, backlog).

```text
Bridge (TBox: the aggregate universal + existing reality leaves)
  ex:AssetMaintenanceProcess  ⊑ bfo:process ; perf:definedByApqcElement ex:PCF_19238
                              (cco:has_process_part ex:P19245, ex:P19253, …)   # group-grained typing
  # leaf-grained alternative for a PM-specific KPI: type individuals directly by ex:P10947

Identity & mapping (TBox classes; individuals are ABox at the deployment)
  ex:PmCompliance-Lineage            KpiLineage "Preventive Maintenance Compliance"
  ex:PmCompliance-SourceRecord       KpiSourceRecord (perf:hadIngestionSource an OpenKPIs entry)
  ex:MaintainAssets-PmCompliance-Mapping  KpiProcessMapping
      perf:hasMappedProcess   ex:PCF_19238
      perf:hasMappedIndicator ex:PmCompliance-Lineage
      decision context        ex:MaintenanceResourceAllocationContext
  ex:MaintenanceResourceAllocationContext  DecisionContext
      question: rebalance labor, adjust PM schedule, escalate, or investigate parts?
      deciding role: DecisionOwnerRole; cadence: monthly; scope: per site

Specifications (each v1, immutable Directive ICEs)  — fields per v0.2.0 §7, unchanged
  ex:PmComplianceSpec-v1 / Target-v1 (95%) / Threshold-v1 / Impl-v1 (CMMS; daily refresh)
  ex:PmDeteriorationPattern-v1 / DeteriorationRule-v1 / EscalationRule-v1
  ex:PmRecoveryPlaybook-v1 (reassign technicians; escalate overdue critical PM; defer low-criticality;
      investigate parts; revise schedule) — expected effects + follow-up lineage references

Governance (ABox)
  RoleAssignments: Maintenance Manager → KpiOwnerRole (lineage); CMMS Data Steward → DataStewardRole
      (impl); Director of Facilities → DecisionOwnerRole (mapping); Maintenance Manager → ActionOwnerRole
      (playbook); Site A Operations Lead → ProcessOwnerRole (process)  — one agent, two assignments
  ActionabilityStatusAssertions: Level 0 (2026-01) … Level 5 (2026-04), each dated

The loop (ABox) — corrected genera in action
  ex:PmMeasuringAct-2026-05 (Act of Measuring) prescribed by Impl-v1 →
  ex:PmObservation-SiteA-2026-05  value 82%, conformsToSpecification Spec-v1,
                                  is_about ex:SiteA-AssetMaintenance-2026-05
  ex:PmAnalysisAct-2026-05 (ActOfAnalysis) prescribed by Pattern-v1 → AnalysisResult (2nd period below)
  ex:PmSignalAct-2026-05 (ActOfAnalysis) prescribed by Rule-v1 → DetectedSignal (severity high)
  ex:LaborRebalancingDecisionAct (Planned Act 228) prescribed by EscalationRule-v1,
      participant Director of Facilities → DecisionRecord (selected: reassign; rejected: defer)
  ex:TechReassignmentAct-SiteA (ActOfImplementation) prescribed by Playbook-v1, input DecisionRecord →
      ActionRecord
  ex:PmObservation-SiteA-2026-06  follow-up (+ corrective-rate, downtime observations)
  ex:PmLearningReviewAct-SiteA (Act of Appraisal) inputs ActionRecord + follow-ups → LearningRecord
```   

The corrected patterns: each act anchors to a verified/existing genus agreeing with its output; the
observation is about the **process individual** (not `ex:PCF_19238`); the individual instantiates a
**real universal** (the aggregate `ex:AssetMaintenanceProcess` or a leaf `ex:P…`); succession is DCTERMS.

## 8. Build Sequence

```text
 0. Verify OpenKPIs (and other source) licensing terms for ingestion.
 1. Author ontology/apqc-performance.ttl: §5 classes, each subclassed per the verified §4.2 table;
    INLINE the reused apqc-ext genera (ActOfAnalysis, ActOfImplementation) for self-containment.
 2. Re-verify each CCO parent IRI against the deployed closure (the §4.2 ✓ set); record the temporal
    and Algorithm parent choices in the ontology header. Replace any minted class that duplicates CCO.
 3. Declare the ten registered properties (§4.3); pin the DCTERMS version (no PROV-O).
 4. Author ontology/apqc_performance_shapes.ttl: TBox P-shapes (anchor reachability, genus↔output
    agreement, register closure) + the *_bad_examples fixture; wire as Gate E in validate.py.
 5. Author the instance-level SHACL (six record classes, KpiProcessMapping, RoleAssignment,
    ActionabilityStatusAssertion, the seven maturity-level shapes) — shipped with the ontology, RUN
    AT THE DEPLOYMENT (D18).
 6. Annotate the 10.3 reality classes with perf:definedByApqcElement (inverse of the existing
    ex:designatesProcessType); mint the ex:AssetMaintenanceProcess aggregate universal if group-grained.
 7. Register the five performance roles in capabilities/role_anchors.json (Occupation/Authority).
 8–15. (Deployment) reference-data stubs; ingest 10–20 KpiSourceRecords; lineages + candidate mappings;
    promote 5–10; measurement + implementation specs; role assignments + status assertions; §7 loop;
    one SPARQL per competency question; validate (all shapes pass; all CQs return §7 individuals; loop
    closes). corpus_check.sh stays EXIT 0 with the TBox merged.
```

## 9. Competency Questions

Unchanged from v0.2.0 §9 (each ships a SPARQL query). The ★ history/bridge questions now run over the
**deployment ABox**; the process-to-KPI and KPI-definition questions resolve against the merged TBox.

## 10. Validation Criteria

The MVP succeeds when (TBox gates in this repo; ABox gates at the deployment):

1. **TBox (Gate E + corpus):** `apqc-performance.ttl` passes the P-shapes; every act reaches a verified
   genus that agrees with its output kind; the minted-relations register is closed; `corpus_check.sh`
   stays **EXIT 0** with the module merged. The bad-examples fixture still produces its expected count.
2. **ABox (deployment):** all instance SHACL shapes pass over the §7 graph; every §9 competency query
   returns the expected individuals; the §4.1 bridge round-trips `ex:PCF_19238 → May observation → back`;
   retiring `PmComplianceSpec-v1` mid-loop leaves all v1-conformant observations queryable as such;
   every MVP class has ≥1 individual (D13 audit); reasoner/SHACL check: no `realizes` targets an ICE,
   no directive ICE is a `has input`, no observation `is_about` a type.

Dashboards are demonstrably downstream: a presentation layer is generable from the records with no class
or property added.

## 11. Deferred (Post-MVP)

As v0.2.0 §11, plus: `DecisionDirective`/`ex:ActOfSelection` decision-as-directive model (D25 alternative);
`ex:ActOfDetection`/`ex:ActOfMonitoring` as PROPOSE-EXT genera; a CCO temporal-interval anchor for
`MeasurementPeriod` if one verifies; PROV-O alignment **only** if a downstream consumer requires it and
PROV is vendored + pinned.

## 12. Risks and Controls

As v0.2.0 §12, with two additions:

| Risk | Control |
|---|---|
| **Unverified anchors** (the v0.2.0 miss) | §4.2 IRIs verified against the deployed closure; Gate E re-verifies at build; genus reuse from apqc-ext |
| **TBox/ABox entanglement** | D18: instances are a separate artifact; corpus gates stay TBox-pure; instance shapes run at the deployment |
| **Re-minting corpus classes** | D24: reuse `ex:ProcessOwnerRole` and the apqc-ext genera; harmonize, never duplicate |
| *(all v0.2.0 controls retained)* | |

## 13. Strategic Value

Unchanged. The catalog says what work exists; the reality layer says what kind of work it is; the
performance layer makes that work measurable, interpretable, governable, actionable, and improvable —
a semantic operating model, not a dashboard catalog — now grounded on verified anchors and cleanly
separated TBox/ABox.

## 14. Changelog: v0.2.0 → v0.3.0

```text
Verified  §4.2 alignment table against CCO v2.0: Designative ICE 686, Measurement ICE 1163 (base;
          164 was a too-narrow ordinal leaf — caught and corrected), Algorithm 653 (⊑965 confirmed),
          Act of Measuring 345 (⊑228); KpiLineage→686, FormulaSpec→653, occurs_at=1918.
Fixed     act genera (D22): KpiAnalysisAct/SignalDetectionAct → ex:ActOfAnalysis (CCO has no
          Act of Analyzing); ActionExecutionAct → ex:ActOfImplementation; DecisionAct → Planned Act 228;
          LearningReviewAct → Appraisal 636. Removed all "⊑ cco:Act" and nonexistent cco act names.
          GOLDEN PRINCIPLE (act genus ↔ output kind) now explicit; DecisionAct/record tension resolved.
Dropped   IAO plan/objective-specification candidates → Directive ICE 965 (the corpus's universal anchor;
          IAO terms not reliably labeled in the closure).
Replaced  PROV-O with DCTERMS + minimal minted perf: provenance (D20); reproducibility/closure hygiene,
          not a Gate-B failure (PROV is neither cco: nor obo:, so Gate B never checked it — v0.2.0 review
          overstated this; corrected here).
Fixed     bridge IRIs (D23): catalog = ex:PCF_<pcfID> (e.g. ex:PCF_19238), reality = ex:P<pcfID>;
          reuse the existing ex:designatesProcessType bridge; perf:definedByApqcElement is its inverse.
Added     D21 process-aggregate typing: leaf reality class where leaf-grained; else a thin perf-layer
          aggregate process universal ⊑ bfo:process bridged to the catalog group; never pun the ICE,
          never instance a classless group. Reality slices untouched (ADR-001 R3 preserved).
Added     D18 ABox = separate deployment artifact; TBox-only ontology; corpus gates stay TBox-pure.
Added     D19 module = merge-only self-contained overlay ontology/apqc-performance.ttl + Gate E shapes
          + bad-examples fixture, merged into corpus_check.sh.
Reused    ex:ProcessOwnerRole (slice 13) instead of re-minting (D24); registered perf roles in the
          Phase-1 role_anchors.json; DecisionOwnerRole ⊑ Authority 187 as the requiresPermission seam (D25).
Corrected MeasurementPeriod → bfo:BFO_0000008 temporal region (verify CCO interval at build).
Closed    minted-relations register at ten entries (dropped the PROV-shaped link; promoted perf:implements
          and perf:hadIngestionSource).
Added     §4.9 governed source-investigation pipeline (D27): candidate-source register + six-step
          per-source checklist (licensing → relevance → depth → format → dedup → outcome). Added FinOps
          Foundation (FinOps Framework KPIs + FOCUS schema; github.com/finopsfoundation) as a candidate
          for APQC 9.x/8.x; tooling MIT/Apache-2.0, Framework content license to confirm at build step 0.
```
