# APQC Performance Layer — Hardened Specification

```text
Document: APQC Performance Layer Plan
Version:  v0.2.0
Status:   Approved baseline (supersedes v0.1.1 draft)
Purpose:  Ontology and implementation specification
Scope:    Planning and formal commitments; not a TTL file
Editor:   Revised under delegated authority per v0.1.1 review
```

---

## 0. Decision Log

Every change from v0.1.1 was made to convert a stated requirement into a formal commitment expressible in RDF/OWL. Each decision below is binding for the first TTL build. Alternatives considered are recorded so future revisions can reopen them deliberately rather than accidentally.

| # | Decision | Resolution | Rejected alternative |
|---|----------|------------|----------------------|
| D1 | Type/instance bridge | Reality-layer process classes annotated with their APQC catalog element; observations are about named process-aggregate individuals typed by those classes (§4.1) | OWL punning of APQC elements (complicates DL profile, tooling) |
| D2 | Class reuse | Every minted class declared as subclass of a named BFO/CCO/IAO parent via the alignment table (§4.2); exact IRIs verified at build step 2 | Free-standing class hierarchy |
| D3 | Directive-to-act relation | Specifications and rules connect to acts via `prescribes` / `prescribed by`, never `has input` (§4.3) | Specs as inputs (conflates data with prescription) |
| D4 | Playbook realization | `ActionExecutionAct prescribed by ActionPlaybook`. `realizes` reserved for BFO realizable entities only (§4.3) | `ActionEvent realizes ActionPlaybook` (category error: ICE is not realizable) |
| D5 | KPI identity over time | New class `KpiLineage`; versioned specifications are immutable individuals linked to one lineage (§4.4) | "The KPI" = current spec (breaks history queries); resurrect CanonicalKpi (re-collapses spec and identity) |
| D6 | Versioning pattern | Distinct immutable individuals per version + `dcterms:replaces` / `prov:wasRevisionOf`; no time-qualified triples on a single individual (§4.5) | Mutable individuals with dated properties (unqueryable history in RDF) |
| D7 | Role accountability over time | Reified `RoleAssignment` class with effective/retirement dates (§4.5) | Direct agent→role triples (history lost) |
| D8 | Maturity status over time | Reified `ActionabilityStatusAssertion` linking a mapping to a status individual with effective date (§4.5) | Status as mutable property on mapping (history lost) |
| D9 | Mapping classes | `CandidateKpiMapping` merged into `KpiProcessMapping`; candidacy is Level 0 status, not a class (§5.1) | Two classes with a promotion/copy step (duplicate provenance) |
| D10 | Decision context | First-class `DecisionContext` class with stated identity conditions (§5.1) | Annotation string (load-bearing concept left informal) |
| D11 | Observation→spec link | Single deliberately minted shortcut `perf:conformsToSpecification`, declared derivable from the act chain (§4.3) | Undeclared "conforms to" in examples only |
| D12 | Naming convention | All process classes end in `Act`; `ActionEvent` renamed `ActionExecutionAct`; `CorrectiveAction`/`PreventiveAction` removed (deferred) | Mixed suffixes |
| D13 | MVP scope rule | A class is in the MVP set iff it is exercised by the §10 validation loop instance data | "Useful someday" inclusion |
| D14 | Dimensions | Dimension values MUST be IRIs to reference-data individuals, never string literals (§4.7) | Stringly-typed dimensions |
| D15 | Temporal representation | `MeasurementPeriod` individuals with `startDate`/`endDate` (xsd:date), aligned to BFO temporal region (§4.6) | Bare period literals on observations |
| D16 | Validation tooling | SHACL shapes for all record classes; every competency question paired with a SPARQL query (§10) | OWL-only (cannot enforce closed-world completeness) |
| D17 | Provenance | `KpiSourceRecord` ingestion aligned to PROV-O; OpenKPIs licensing verified before verbatim ingestion (§4.8) | Untracked ingestion |

---

## 1. Purpose

The `apqc-performance` layer extends the existing APQC process knowledge graph into an actionable process intelligence layer. It sits above two existing layers:

- **APQC catalog layer** (`apqc-catalog.ttl`): the APQC hierarchy — categories, process groups, processes, activities, tasks, with hierarchy IDs, element IDs, labels, definitions, and parent-child structure.
- **APQC reality layer**: BFO/CCO interpretations of APQC elements as real-world kinds of work — act types, input/output information content entities, participant roles, capabilities.

The performance layer adds measurement, analysis, signal, decision, action, and learning semantics. The governed chain is:

```text
APQC Process (catalog element / reality type / process instance)
→ KpiSourceRecord
→ KpiProcessMapping            (status: candidate → … → learning-enabled)
→ KpiMeasurementSpecification  (version of a KpiLineage)
→ KpiImplementationSpecification
→ KpiMeasuringAct
→ KpiObservation
→ KpiAnalysisAct
→ AnalysisResult
→ SignalDetectionAct
→ DetectedSignal
→ DecisionAct
→ DecisionRecord
→ ActionExecutionAct
→ ActionRecord
→ Follow-up KpiObservation
→ LearningReviewAct
→ LearningRecord
```

The goal is not to attach KPI names to APQC processes. The goal is to make APQC process knowledge measurable, interpretable, governable, and actionable. Dashboards are downstream presentation artifacts of this chain, never the source of truth.

## 2. Design Principles

The layer preserves these distinctions as separate classes:

```text
KPI lineage ≠ KPI measurement specification
KPI measurement specification ≠ KPI implementation specification
KPI implementation specification ≠ KPI measuring act
KPI measuring act ≠ KPI observation
KPI observation ≠ analysis result
Analysis result ≠ detected signal
Detected signal ≠ decision record
Decision record ≠ action record
Action record ≠ learning record
Dashboard tile ≠ any of the above
```

Two symmetric reuse disciplines govern the build:

1. **Relation reuse (kept from v0.1.1):** prefer `is about`, `has input`, `has output`, `has participant`, `bearer of`, `prescribes`, `realizes` before minting object properties. All minted properties live in the register at §4.3.
2. **Class reuse (new in v0.2.0):** every minted class must subclass a named BFO/CCO/IAO parent, recorded in the alignment table at §4.2. No free-standing classes.

## 3. Layering Strategy

Unchanged from v0.1.1 in substance:

- **Catalog layer** answers: what work exists in the enterprise process model, where it sits in the APQC hierarchy, and its APQC-defined scope.
- **Reality layer** answers: what kind of work this is, what roles participate, what information artifacts are inputs and outputs, what capabilities are realized.
- **Performance layer** answers: how the work is measured, who governs the KPI, how it is implemented, what observations and analyses are produced, what signals matter, who decides, what actions are available, and how outcomes are reviewed.

## 4. Formal Commitments

This section is new in v0.2.0 and is normative. It converts the v0.1.1 "should support X" requirements into patterns expressible in RDF/OWL.

### 4.1 Type/Instance Bridge

The hardest problem in v0.1.1: APQC 10.3 is a reference-model element, but observations are about actual work at actual sites in actual periods. The binding pattern:

1. **Catalog elements are ICEs.** `apqc:10.3-MaintainAssets` is an information content entity describing a kind of work. It is never the subject of an observation.
2. **Reality-layer classes carry the bridge annotation.** Each reality-layer process class is linked to its catalog element by the annotation property `perf:definedByApqcElement` (annotation, OWL-DL safe, no punning):

   ```text
   ex:AssetMaintenanceProcess  rdfs:subClassOf  cco:Act ;
       perf:definedByApqcElement  apqc:10.3-MaintainAssets .
   ```

3. **Observation subjects are process-aggregate individuals.** Each measured slice of real work is a named individual typed by the reality-layer class, located in space and time:

   ```text
   ex:SiteA-AssetMaintenance-2026-05  a  ex:AssetMaintenanceProcess ;
       cco:occurs_at      ex:SiteA ;
       perf:coversPeriod  ex:Period-2026-05 .
   ```

4. **Observations are about instances, never types.** `KpiObservation is_about ex:SiteA-AssetMaintenance-2026-05`.

The full bridge query path, answerable in SPARQL with no punning:

```text
observation → is_about → process individual → rdf:type → reality class
            → perf:definedByApqcElement → catalog element
            ← perf:hasMappedProcess ← KpiProcessMapping
```

This resolves the v0.1.1 ambiguity: `KpiProcessMapping` points at the **catalog element**; `KpiObservation` is about a **process individual**; the reality-layer **class** joins them.

### 4.2 Class Alignment Table

Every MVP class subclasses one of the parents below. Exact IRIs are verified against the deployed CCO/IAO versions at build step 2; where two candidates exist, the build verifies which is present and records the choice in the ontology header.

| Performance class | Nearest parent (verify IRI at build) |
|---|---|
| KpiSourceRecord | cco:DescriptiveInformationContentEntity |
| KpiProcessMapping | cco:DescriptiveInformationContentEntity |
| KpiLineage | cco:DesignativeInformationContentEntity |
| DecisionContext | cco:DescriptiveInformationContentEntity |
| ActionabilityStatus / ActionabilityStatusAssertion | cco:InformationContentEntity (status individuals as named individuals) |
| RoleAssignment | cco:DescriptiveInformationContentEntity |
| KpiMeasurementSpecification | cco:DirectiveInformationContentEntity |
| KpiImplementationSpecification | cco:DirectiveInformationContentEntity |
| FormulaSpecification | cco:Algorithm (candidate: iao:algorithm) |
| TargetSpecification | iao:objective specification (candidate: cco objective subclass) |
| ThresholdSpecification | cco:DirectiveInformationContentEntity |
| AnalysisPatternSpecification | cco:DirectiveInformationContentEntity (candidate: iao:plan specification) |
| SignalDetectionRule, DecisionRule | cco:DirectiveInformationContentEntity |
| ActionPlaybook | iao:plan specification (candidate: cco plan subclass) |
| KpiObservation | cco:MeasurementInformationContentEntity (candidate: iao:measurement datum) |
| AnalysisResult, DetectedSignal, DecisionRecord, ActionRecord, LearningRecord | cco:DescriptiveInformationContentEntity |
| KpiMeasuringAct | cco:ActOfMeasuring |
| KpiAnalysisAct, SignalDetectionAct, LearningReviewAct | cco:Act (use cco:ActOfAnalyzing etc. if present) |
| DecisionAct | cco:Act (use cco act-of-deciding subclass if present) |
| ActionExecutionAct | cco:Act |
| KpiOwnerRole, DataStewardRole, DecisionOwnerRole, ActionOwnerRole, ProcessOwnerRole | cco:Role (bfo:role) |
| MeasurementPeriod | cco temporal interval class aligned to bfo temporal region |

Rule: if CCO/IAO already provides a class that matches a performance-layer concept exactly, **reuse it directly and do not mint** — the table entry becomes an equivalence note, not a subclass.

### 4.3 Relation Patterns and Minted Relations Register

**Directives prescribe; data flows.** The corrected patterns:

```text
KpiMeasuringAct      prescribed by  KpiImplementationSpecification
                     has input      source data records
                     has output     KpiObservation

KpiAnalysisAct       prescribed by  AnalysisPatternSpecification
                     has input      KpiObservation(s)
                     has output     AnalysisResult

SignalDetectionAct   prescribed by  SignalDetectionRule
                     has input      KpiObservation / AnalysisResult
                     has output     DetectedSignal

DecisionAct          prescribed by  DecisionRule
                     has input      DetectedSignal
                     has participant  DecisionOwnerRole bearer
                     has output     DecisionRecord

ActionExecutionAct   prescribed by  ActionPlaybook
                     has input      DecisionRecord
                     has participant  ActionOwnerRole bearer
                     has output     ActionRecord

LearningReviewAct    has input      ActionRecord, follow-up KpiObservation(s)
                     has output     LearningRecord
```

`realizes` is reserved for BFO realizable entities (roles, dispositions, functions). It never targets an ICE. Where a CCO concretization chain (plan specification → plan → realized by act) is wanted later, it may be added without disturbing the `prescribed by` backbone.

**Reused external vocabularies:** `dcterms:replaces` / `dcterms:isReplacedBy` (version succession), `prov:wasRevisionOf`, `prov:wasDerivedFrom` (spec derived from source record), `prov:hadPrimarySource` (ingestion provenance).

**Minted Relations Register** — the complete, closed list for v0.2.0. Adding a relation requires demonstrating that no BFO/CCO/IAO/PROV/DCTERMS relation suffices, then registering it here.

| Property | Domain → Range | Rationale |
|---|---|---|
| perf:definedByApqcElement | reality class → catalog element (annotation) | Type/instance bridge; no punning-free alternative exists |
| perf:hasMappedProcess | KpiProcessMapping → catalog element | `is about` cannot distinguish the two ends of a mapping |
| perf:hasMappedIndicator | KpiProcessMapping → KpiLineage | Same; the other end |
| perf:specifiesIndicator | KpiMeasurementSpecification → KpiLineage | Binds a versioned spec to its identity node |
| perf:conformsToSpecification | KpiObservation → KpiMeasurementSpecification | Deliberate materialized shortcut; derivable from observation ← output ← act ← prescribed-by ← impl spec → implements → measurement spec. Declared so queries need not walk the chain |
| perf:implements | KpiImplementationSpecification → KpiMeasurementSpecification | Spec-to-spec; not aboutness, not prescription of an act |
| perf:coversPeriod | observation / process individual → MeasurementPeriod | Pending verification of a suitable CCO temporal relation at build; retire if one exists |
| perf:hasStatus | ActionabilityStatusAssertion → ActionabilityStatus individual | Controlled-vocabulary link |
| perf:assignsRole / perf:assignedToAgent / perf:assignmentScope | RoleAssignment → Role / Agent / governed object | Reified assignment requires three typed ends |

Nine entries. The register is closed for the MVP build.

### 4.4 KPI Identity: KpiLineage

v0.1.1 deleted `CanonicalKpi` but kept asking "given a KPI…". The referent is now explicit.

**KpiLineage** — a designative information content entity that designates one performance indicator across all successive versions of its measurement specification. The lineage node carries only identity-stable content: preferred label, alternative labels, and a stable identifier. Everything that can change between versions (formula, grain, unit, thresholds, owner) lives on the versioned `KpiMeasurementSpecification`.

```text
ex:PmCompliance-Lineage  a  perf:KpiLineage .
ex:PmComplianceSpec-v1   perf:specifiesIndicator  ex:PmCompliance-Lineage .
ex:PmComplianceSpec-v2   perf:specifiesIndicator  ex:PmCompliance-Lineage ;
                         dcterms:replaces         ex:PmComplianceSpec-v1 .
```

"The current approved specification" is a query (the approved spec not the object of any `dcterms:replaces`), not a stored mutable pointer. `KpiProcessMapping` maps the **lineage** to the process; the maturity status assertion history records which spec versions were in force when.

### 4.5 Versioning Pattern

One pattern, applied uniformly:

1. **Versions are distinct immutable individuals.** Once a specification, rule, playbook, or implementation is approved, it is never edited; a successor is created and linked with `dcterms:replaces` (and `prov:wasRevisionOf` where derivation detail matters).
2. **Versioned classes:** KpiMeasurementSpecification, KpiImplementationSpecification, FormulaSpecification, TargetSpecification, ThresholdSpecification, AnalysisPatternSpecification, SignalDetectionRule, DecisionRule, ActionPlaybook.
3. **Version metadata** on each versioned individual: version identifier, effective date, retirement date, approval status, review date.
4. **Role accountability is reified.** A `RoleAssignment` records: the role, the bearing agent (person, team, organization, or position), the governed object (lineage, mapping, spec, or playbook), effective date, retirement date. History is the set of assignments; "current owner" is a date-filtered query.
5. **Maturity status is reified.** An `ActionabilityStatusAssertion` records: the `KpiProcessMapping`, the `ActionabilityStatus` individual, effective date, asserting agent. The mapping's status history is the ordered set of its assertions.
6. **Records are born immutable.** Observations, analysis results, signals, decision records, action records, and learning records are events-in-information form; they are never versioned, only superseded by corrections that `prov:wasRevisionOf` the original.
7. **Every KpiObservation carries** its measurement period, creation date, and the specific implementation-specification version that produced it — making "which observations were produced under a superseded spec?" answerable.

### 4.6 Temporal Representation

`MeasurementPeriod` individuals (aligned to BFO temporal region via the CCO temporal interval class) with `startDate` and `endDate` as `xsd:date`, plus a label (`"2026-05"`). Observations, process-aggregate individuals, status assertions, and role assignments reference period individuals or carry xsd:date effective/retirement dates directly. No bare string periods.

### 4.7 Dimension Representation

Dimension **values are IRIs**, never literals. Sites, asset classes, teams, criticality levels, and work-order priorities are reference-data individuals (in the reality layer or a small reference-data module). The measurement specification declares which reference-data classes are legal dimensions (structured field, not a separate class in MVP); an observation's dimension links must target individuals of those classes — enforced by SHACL, not OWL. This is the structural control against metric collapse re-entering through stringly-typed dimensions.

### 4.8 Source Provenance

`KpiSourceRecord` individuals carry `prov:hadPrimarySource` (the external catalog record), retrieval date, and source type (OpenKPIs, APQC-suggested, internal, vendor, regulatory) as a controlled-vocabulary individual — source subtypes are **not** classes in the MVP (deferred; see §11). Approved measurement specifications derived from a source record link back via `prov:wasDerivedFrom`. Build step 0 verifies OpenKPIs licensing terms before any verbatim ingestion of labels, descriptions, or formulas.

Source records remain candidates/evidence only. A source KPI becomes useful only after placement into enterprise context: source record → KpiProcessMapping (candidate) → decision context → role accountability → measurement specification → implementation specification → analysis pattern → signal rule → action playbook.

## 5. MVP Class Set

**Inclusion rule (D13):** a class is in the MVP iff it is exercised by the §10 validation loop instance data. 34 classes in six groups. Everything else is deferred (§11).

### 5.1 Source, identity, mapping, and governance infrastructure

```text
KpiSourceRecord
KpiLineage
KpiProcessMapping
DecisionContext
ActionabilityStatus            (class; 7 named individuals, Level 0–6)
ActionabilityStatusAssertion
RoleAssignment
MeasurementPeriod
```

**KpiSourceRecord** — a descriptive ICE recording a KPI or metric as represented by an external or internal source. Source type is a controlled-vocabulary value, not a subclass.

**KpiLineage** — see §4.4. The stable referent of "the KPI."

**KpiProcessMapping** — a first-class descriptive ICE connecting a `KpiLineage` to one APQC catalog element in one `DecisionContext`. Carries: mapped process (catalog element), mapped indicator (lineage), decision context, mapping rationale, mapping confidence, review status (candidate / under-review / approved / rejected / retired), reviewer, effective date, retirement date. Candidacy is the initial review status — there is no separate candidate-mapping class (D9). Owner accountability attaches via `RoleAssignment`; maturity attaches via `ActionabilityStatusAssertion`. A KPI relevant to several processes for different reasons (e.g., customer churn rate serving service retention, sales, and product-market-fit decisions) gets one mapping per process-context pair, each with its own status history.

**DecisionContext** — a descriptive ICE specifying the recurring decision a KPI serves. Carries: decision question, deciding role, decision cadence, scope (the organizational or process scope over which the decision operates). **Identity conditions:** two contexts are the same iff they have the same decision question, same deciding role, and same scope. This is what makes "the same KPI mapped to three processes" three distinct mappings rather than one vague relevance claim.

**ActionabilityStatus** — a class whose seven named individuals are the maturity levels (§6). **ActionabilityStatusAssertion** — see §4.5(5). **RoleAssignment** — see §4.5(4). **MeasurementPeriod** — see §4.6.

### 5.2 Specification layer (directive ICEs; all versioned per §4.5)

```text
KpiMeasurementSpecification
FormulaSpecification
TargetSpecification
ThresholdSpecification
AnalysisPatternSpecification
SignalDetectionRule
DecisionRule
ActionPlaybook
KpiImplementationSpecification
```

**KpiMeasurementSpecification** — a directive ICE prescribing how a performance indicator is to be measured, calculated, and interpreted. Carries: definition; formula specification (component); unit of measure; measurement grain; measurement population; measurement time window; legal dimension classes (per §4.7); target specification; threshold specification; data requirements (as structured fields in MVP); version metadata. Labels live on the lineage; accountability lives on role assignments. Answers: *what should be measured?*

**FormulaSpecification** — a directive ICE (aligned to algorithm) prescribing calculation logic. MVP fields: human-readable formula text, numerator description, denominator description, aggregation rule, population constraint, exclusion rule, time-window rule. Numerator/denominator are structured **fields**, not classes, in the MVP (promoted to classes post-MVP only if machine-actionable formulas require it). A slot for a machine-actionable formula expression is reserved but unpopulated in MVP. A formula is never only a label.

**TargetSpecification** — desired value, range, or direction (e.g., PM compliance target = 95%). **ThresholdSpecification** — boundary conditions that trigger review, signal detection, or escalation; **tolerance is a field of the threshold** (acceptable deviation before triggering), not a separate class (trimmed per D13).

**AnalysisPatternSpecification** — prescribes how observations are to be analyzed (trend, variance-to-target, consecutive-period checks, segmentation). **SignalDetectionRule** — prescribes the condition under which a signal is detected, including severity assignment logic. **DecisionRule** — prescribes who decides what question under which signal conditions, referencing the decision context. **ActionPlaybook** — a plan specification prescribing the available action options and their expected effects, including the follow-up indicators (as lineage references) that the learning review must examine. Expected effects on other KPIs are modeled here — not via a minted "action affects KPI" relation.

**KpiImplementationSpecification** — a directive ICE prescribing how one measurement specification is computed in one environment: source systems, required data elements, inclusion/numerator/denominator rules, transformation logic, refresh cadence, validation and data-quality rules (structured fields in MVP), known exclusions and limitations, implementation owner (via RoleAssignment), version metadata. Linked to its measurement specification by `perf:implements`. Answers: *how is it computed here?*

### 5.3 Record layer (descriptive ICEs; born immutable per §4.5)

```text
KpiObservation
AnalysisResult
DetectedSignal
DecisionRecord
ActionRecord
LearningRecord
```

**KpiObservation** — a measurement ICE reporting the measured value of an indicator for a process individual and period. Carries: measured value, unit, `perf:coversPeriod` → MeasurementPeriod, `is about` → process-aggregate individual (§4.1), dimension links (IRIs per §4.7), `perf:conformsToSpecification` → the measurement-spec version in force, producing implementation-spec version, quality/confidence indicator, creation date.

**AnalysisResult** — reports the output of a KpiAnalysisAct (trend, variance, Pareto, aging, control-chart, forecast-versus-actual results). **DetectedSignal** — reports that a signal detection rule was satisfied; carries severity, triggering rule version, input observations/results, and aboutness to the same process individual. A signal is a reportable condition, not a decision. **DecisionRecord** — records: the decision act, inputs considered, selected option, rejected options, rationale, decision date, expected effect, follow-up date. **ActionRecord** — records that an action was performed (distinct from the act itself). **LearningRecord** — records: the action record, expected effect, follow-up observations, observed effect, conclusion, recommendation (continue / modify / retire the playbook).

### 5.4 Act layer (occurrents)

```text
KpiMeasuringAct
KpiAnalysisAct
SignalDetectionAct
DecisionAct
ActionExecutionAct
LearningReviewAct
```

All follow the §4.3 patterns: prescribed by their directive, consuming records/data as inputs, producing exactly the record class paired with them. Naming convention: every act class ends in `Act` (D12).

### 5.5 Role layer

```text
KpiOwnerRole          accountable for interpreting and governing a measurement specification
DataStewardRole       accountable for data definitions, quality rules, lineage, implementation support
DecisionOwnerRole     authorized to make or approve decisions on signals
ActionOwnerRole       accountable for executing or coordinating selected actions
ProcessOwnerRole      accountable for the process itself
```

Roles inhere in agents (persons, organizations, teams) per BFO. Accountability links to governed objects only through `RoleAssignment` (§4.5), so one person bearing four roles, and ownership changing over time, are both representable without ambiguity.

## 6. Actionability Maturity Model

Maturity is a property of a **KpiProcessMapping**, asserted through time-stamped `ActionabilityStatusAssertion`s — never of a KPI globally. The seven `ActionabilityStatus` individuals:

```text
Level 0  Candidate          mapping exists with review status candidate
Level 1  Defined            approved measurement specification exists for the lineage
Level 2  Computable         implementation specification implements that specification
Level 3  Governed           role assignments and review cadence in force for the mapping
Level 4  Interpretable      targets, thresholds, and analysis patterns defined
Level 5  Actionable         signal rules, decision rules, decision-owner assignment, playbooks defined
Level 6  Learning-enabled   follow-up indicators and learning review pattern defined
```

Each level has a SHACL shape that checks whether the mapping's surrounding graph actually satisfies the level — a status assertion that overstates maturity fails validation. Status history, supersession, and review dates come for free from the assertion pattern (§4.5).

## 7. MVP Walkthrough: APQC 10.3 Maintain Assets

The MVP target is APQC `10.3 Maintain assets` (10.3.1 Plan / 10.3.2 Manage / 10.3.3 Perform asset maintenance), chosen for its concrete operational entities: assets, work orders, maintenance schedules, teams, technicians, facilities, asset classes, preventive and corrective maintenance, downtime, backlog.

The walkthrough below names the individuals the validation loop must contain. Field-level detail (formulas, inclusion rules, dimensions) is carried over from v0.1.1 §12 unchanged except where corrected.

```text
Bridge
  ex:AssetMaintenanceProcess        reality class, perf:definedByApqcElement apqc:10.3
  ex:SiteA-AssetMaintenance-2026-05 process individual at Site A, May 2026
  ex:SiteA-AssetMaintenance-2026-06 follow-up period individual

Identity and mapping
  ex:PmCompliance-Lineage           KpiLineage "Preventive Maintenance Compliance"
  ex:PmCompliance-SourceRecord      KpiSourceRecord (prov:hadPrimarySource an OpenKPIs entry)
  ex:MaintainAssets-PmCompliance-Mapping   KpiProcessMapping
      perf:hasMappedProcess   apqc:10.3
      perf:hasMappedIndicator ex:PmCompliance-Lineage
      decision context        ex:MaintenanceResourceAllocationContext
  ex:MaintenanceResourceAllocationContext  DecisionContext
      question: rebalance labor, adjust PM schedule, escalate, or investigate parts?
      deciding role: DecisionOwnerRole; cadence: monthly; scope: per site

Specifications (each v1, immutable)
  ex:PmComplianceSpec-v1            KpiMeasurementSpecification
      formula: completed scheduled PM work orders / scheduled PM work orders due
      unit: percent; grain: site × asset class × criticality × team × period
      time window: weekly and monthly
      dimensions: Site, Asset, AssetClass, AssetCriticality,
                  MaintenanceTeam, Technician, WorkOrderPriority (reference-data classes)
  ex:PmComplianceTarget-v1          95%
  ex:PmComplianceThreshold-v1       signal if below 90% for two consecutive periods;
                                    tolerance field: 3 percentage points period-over-period
  ex:PmComplianceImpl-v1            KpiImplementationSpecification (CMMS work-order records;
                                    inclusion, numerator, denominator rules; daily refresh;
                                    known limitation: technician closeout timeliness)
  ex:PmDeteriorationPattern-v1      AnalysisPatternSpecification (threshold + trend + segmentation)
  ex:PmDeteriorationRule-v1         SignalDetectionRule (below target two consecutive periods,
                                    or drop beyond tolerance; severity high on critical assets)
  ex:MaintenanceEscalationRule-v1   DecisionRule
  ex:PmRecoveryPlaybook-v1          ActionPlaybook (reassign technicians; escalate overdue
                                    critical PM; defer low-criticality PM; investigate parts;
                                    revise schedule; root-cause review)
      expected effects: PM compliance ↑; corrective-maintenance rate not ↑;
                        downtime not ↑; backlog age ↓
      follow-up indicators: PM compliance, corrective maintenance rate,
                            asset downtime (as lineage references)

Governance
  RoleAssignments: Maintenance Manager → KpiOwnerRole over the lineage;
                   CMMS Data Steward → DataStewardRole over the implementation;
                   Director of Facilities → DecisionOwnerRole over the mapping;
                   Maintenance Manager → ActionOwnerRole over the playbook;
                   Site A Operations Lead → ProcessOwnerRole over the process
                   (one agent bearing two roles — distinct assignments, per §5.5)
  ActionabilityStatusAssertions: Level 0 (2026-01) … Level 5 (2026-04), each dated

The loop
  ex:PmMeasuringAct-2026-05         prescribed by Impl-v1 → outputs
  ex:PmObservation-SiteA-2026-05    value 82%, conformsToSpecification Spec-v1,
                                    about SiteA-AssetMaintenance-2026-05
  ex:PmAnalysisAct-2026-05          prescribed by Pattern-v1 → outputs
  ex:PmAnalysisResult-SiteA-2026-05 below target; second consecutive period; critical assets
  ex:PmSignalAct-2026-05            prescribed by Rule-v1 → outputs
  ex:PmSignal-SiteA-2026-05         severity high
  ex:LaborRebalancingDecisionAct    prescribed by EscalationRule-v1,
                                    participant: Director of Facilities → outputs
  ex:LaborRebalancingDecisionRecord selected: reassign technicians; rejected: defer PM;
                                    expected effect; follow-up date 2026-06-30
  ex:TechReassignmentAct-SiteA      prescribed by Playbook-v1, input DecisionRecord → outputs
  ex:TechReassignmentRecord-SiteA   ActionRecord
  ex:PmObservation-SiteA-2026-06    follow-up observation (plus corrective-rate and
                                    downtime observations for June)
  ex:PmLearningReviewAct-SiteA      inputs: action record + follow-up observations → outputs
  ex:PmLearningRecord-SiteA         observed vs expected effect; recommendation on Playbook-v1
```

Note the corrected patterns in action: the act is **prescribed by** the playbook (not "realizes" it); the observation is about the **process individual** (not APQC 10.3); the observation cites the **spec version** in force.

## 8. Build Sequence

```text
 0. Verify OpenKPIs (and other source) licensing terms for ingestion.
 1. Define the ontology skeleton: classes from §5, each subclassed per the §4.2 table.
 2. Verify exact CCO/IAO parent IRIs against deployed versions; record choices in the
    ontology header; replace any minted class that duplicates an existing one.
 3. Declare the nine registered properties (§4.3); import dcterms and prov-o terms used.
 4. Author SHACL shapes for all six record classes, KpiProcessMapping, RoleAssignment,
    ActionabilityStatusAssertion, and the seven maturity-level conformance shapes (§6).
 5. Create the ActionabilityStatus individuals (Level 0–6) and reference-data stubs
    (sites, asset classes, teams, criticality, priority) for the MVP.
 6. Annotate the 10.3 reality-layer classes with perf:definedByApqcElement.
 7. Ingest 10–20 source KPI records as KpiSourceRecord individuals with PROV provenance.
 8. Create KpiLineage nodes and candidate KpiProcessMappings (status: candidate)
    with DecisionContext individuals.
 9. Promote 5–10 mappings; author the approved KpiMeasurementSpecification versions.
10. Author 2–3 KpiImplementationSpecification versions (perf:implements links).
11. Create RoleAssignments and initial ActionabilityStatusAssertions.
12. Generate the §7 instance data: process individuals, periods, measuring acts,
    observations.
13. Run the loop: analysis acts → results → signal acts → signals → decision act →
    decision record → action execution act → action record → follow-up observations →
    learning review act → learning record.
14. Write one SPARQL query per competency question (§9); store alongside the ontology.
15. Validate: all SHACL shapes pass; all competency-question queries return the
    expected §7 individuals; the §10 loop closes.
```

## 9. Competency Questions

Each question ships with a SPARQL query (build step 14). Additions over v0.1.1 are marked ★.

**Process-to-KPI.** Given an APQC process: what candidate mappings exist? What approved measurement specifications monitor it (via mapping → lineage → current spec)? Which mappings sit at each maturity level? ★Which process **individuals** instantiate work governed by this catalog element (the §4.1 bridge query)?

**KPI definition.** Given a KPI lineage: what is its current approved measurement specification? ★What superseded specifications exist and when were they in force? What are the formula, numerator, denominator, unit, grain, population, time window, and legal dimensions of a given spec version?

**Implementation.** Given a measurement specification: what implementation specifications implement it? What source systems and data elements are required? What known limitations exist? What implementation version produced a given observation?

**Observation and analysis.** Given an observation: what process individual is it about, and what catalog element governs it? What period does it cover? What spec version does it conform to? ★Which observations were produced under a now-superseded specification or implementation? What target and threshold applied at that time? What analysis results were produced from it?

**Signal.** Given an analysis result or observation: did it satisfy a signal detection rule? What detected signals exist for a process individual? What severity and what rule version produced each?

**Decision and action.** Given a detected signal: who held DecisionOwnerRole over the mapping at signal time (★date-filtered RoleAssignment query)? What decision rule applied? What decision record resulted, with selected and rejected options? What playbook prescribed the action? Who owned the action?

**Learning.** Given an action record: what follow-up observations were reviewed? Did the action produce the expected effect? What learning record was created, and what does it recommend for the playbook version?

**Governance history.** ★Given a mapping: what is its full actionability status history? ★Given a lineage: who has held each role over it, when? ★Which status assertions fail their level's SHACL conformance shape (overstated maturity)?

## 10. Validation Criteria

The MVP succeeds when the graph supports this loop with no dashboard-specific logic, every step instantiated by the §7 individuals:

```text
APQC process selected
→ source records identified → mapping reviewed (status history recorded)
→ measurement specification approved (lineage-bound, versioned)
→ implementation specification defined → observation produced (about a process
  individual, citing spec and impl versions, period as individual, dimensions as IRIs)
→ analysis result → detected signal → decision record (by the assigned decision owner)
→ action record → follow-up observations → learning record
```

Acceptance gates:

1. All SHACL shapes pass over the full instance graph.
2. Every §9 competency question's SPARQL query returns the expected individuals.
3. The §4.1 bridge query round-trips: from `apqc:10.3` to the May observation and back.
4. The history queries work: retiring `PmComplianceSpec-v1` in favor of a v2 mid-loop leaves all v1-conformant observations queryable as such.
5. Every MVP class has at least one individual in the validation graph (D13 audit).
6. Reasoner check: no `realizes` triple targets an ICE; no directive ICE appears as `has input` to an act.

Dashboards are demonstrably downstream: a presentation layer can be generated from observations, results, signals, decisions, and learning records without adding any class or property to this ontology.

## 11. Deferred (Post-MVP) Items

Removed from the MVP by D13, to be reconsidered only with a driving use case:

```text
OpenKpiSourceRecord and other KpiSourceRecord subclasses   (source type is a vocabulary value)
KpiReviewRecord            (review fields live on the mapping in MVP)
NumeratorSpecification / DenominatorSpecification as classes  (fields on FormulaSpecification)
ToleranceSpecification     (field on ThresholdSpecification)
BenchmarkSpecification     (descriptive/directive split deferred with it)
DataSourceRequirement, DataElementRequirement, DataQualityRule, DataContract,
CalculationServiceSpecification, RefreshCadenceSpecification, ValidationRule,
KnownLimitationRecord      (structured fields on KpiImplementationSpecification in MVP)
CorrectiveAction / PreventiveAction   (subtypes of ActionExecutionAct when needed)
ReviewCadenceSpecification (field on mapping/spec in MVP)
Machine-actionable formula expressions (slot reserved on FormulaSpecification)
Dashboard / presentation-artifact classes (explicitly out of scope; downstream layer)
CCO concretization chain for plans (plan spec → plan → realization), if process-level
plan tracking is later required alongside the prescribed-by backbone
```

## 12. Risks and Controls

| Risk | Control |
|---|---|
| **Metric collapse** — label, formula, implementation, observation, chart, and rule treated as one object | Separate classes per §5; SHACL forbids observations without spec-version links |
| **Over-minting properties** | Closed nine-entry register (§4.3); reasoner gate 6 in §10 |
| **Over-minting classes** | Alignment table (§4.2) with build-step verification and reuse-over-mint rule |
| **Misplaced maturity** — actionability attached to the KPI globally | Status assertions attach only to KpiProcessMapping; level shapes verify the claim |
| **Lost history** — definitions, owners, thresholds change invisibly | Immutable versions + dcterms/prov succession; reified RoleAssignment and status assertions; acceptance gate 4 |
| **Type/instance confusion** — observations "about APQC 10.3" | §4.1 bridge; SHACL requires observation aboutness to target a process individual |
| **Formula underspecification** | FormulaSpecification structured fields are SHACL-mandatory for approved specs |
| **Stringly-typed dimensions** | D14: dimension values must be IRIs; SHACL-enforced |
| **Dashboard-centric modeling** | No presentation classes in the ontology; §10 downstream demonstration |
| **Identity drift** — "the KPI" means different things in different queries | KpiLineage is the sole referent; specs bind to it; mappings map it |

## 13. Strategic Value

The catalog layer identifies the enterprise's work. The reality layer explains what kind of work it is. The performance layer makes that work measurable, interpretable, governable, actionable, and improvable — a semantic operating model for organizational intelligence, not a dashboard catalog.

```text
APQC tells us what work exists.
The reality layer tells us what kind of work it is.
The performance layer tells us how that work is measured, interpreted,
governed, acted upon, and improved.
```

## 14. Changelog: v0.1.1 → v0.2.0

```text
Added    §0 Decision Log (D1–D17) binding each requirement to a formal pattern.
Added    §4.1 type/instance bridge (annotation-based, punning-free).
Added    §4.2 class alignment table; class-reuse discipline symmetric to relation reuse.
Fixed    realizes misuse: directives now connect to acts via prescribes/prescribed-by;
         specifications and rules are no longer modeled as act inputs.
Added    KpiLineage as the identity-over-time referent of "the KPI".
Fixed    versioning: immutable version individuals + dcterms:replaces/prov:wasRevisionOf;
         reified RoleAssignment and ActionabilityStatusAssertion.
Merged   CandidateKpiMapping into KpiProcessMapping (candidacy = review status).
Added    DecisionContext as a defined class with identity conditions.
Renamed  ActionEvent → ActionExecutionAct; uniform -Act naming.
Removed  CorrectiveAction/PreventiveAction (undefined in v0.1.1; deferred).
Fixed    spine: ActionRecord and LearningReviewAct now present and consistent with §5.
Declared perf:conformsToSpecification deliberately (was an unregistered "conforms to").
Closed   minted-relations register at nine entries; reused dcterms and PROV-O.
Trimmed  MVP per D13; deferred items enumerated in §11.
Added    D14 dimensions-as-IRIs and D15 MeasurementPeriod commitments.
Added    SHACL + per-question SPARQL validation; maturity-level conformance shapes.
Added    PROV-O ingestion provenance and licensing check (build step 0).
Added    competency questions for superseded specs, status history, role history.
```

