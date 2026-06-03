# APQC PCF → BFO 2020 / CCO Transformation Methodology

**Specification v1.1.0**
**Status:** Stable. Derived from and validated against the `1.1.1` reference implementation (`apqc_1_1_1.ttl` v0.2.0) and its SHACL suite (`apqc_shapes.ttl` v0.1.0).
**Dependencies (pinned):** Common Core Ontologies Merged **v2.0 (2024-11-06)**; BFO 2020 (via CCO import).

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used per RFC 2119.

### Changelog
- **v1.1.0** — Scoped provenance requirements to PCF-derived classes (§4). Loosened the decision→Directive-ICE rule (Phase 3). Made existential restrictions conditional on definitional necessity (Phase 3). Promoted the Category policy to a foundational decision (D8) and added the shared-extension-module decision (D9). Added method-phrase part/definition criteria (Phase 1) and the compound-row caveat (§4). Pinned Gate B to a local dependency closure (§9). Aligned the definition standard to CCO house style (§7) — see note. Added module architecture (§12).
- **v1.0.0** — Initial specification.

> **Definition-style note (v1.1.0).** §7 previously required restating the defined term ("*a B is a C that Ds*"), which the examples did not follow. Rather than restate the label, §7 now matches CCO's own convention ("*A ⟨genus⟩ that ⟨differentia⟩*", label not restated, as in CCO's definition of Information Content Entity). This resolves the inconsistency toward dependency-ontology conformance; restating the label remains permitted but optional, applied uniformly per module.

---

## 1. Scope

This document specifies the normative procedure for converting entries of the APQC Process Classification Framework (PCF) — a hierarchical taxonomy of business process descriptions — into a BFO 2020 / CCO 2.0–conformant OWL ontology module.

It is input-format-agnostic above the data layer: the input is any PCF export carrying, per row, a **PCF ID**, a **Hierarchy ID** (dotted decimal), and an **Element Description** (free text). The output is a Turtle module plus its validation evidence.

An output module **conforms** to this specification if and only if it passes Validation Gates A–D (§9) under the chosen corpus policies (D8, D9).

---

## 2. Inputs and outputs

**Inputs**
- PCF export: `PCF ID`, `Hierarchy ID`, `Element Description`.
- Pinned ontology dependencies, as a local closure (§9 Gate B).

**Output artifacts (per slice)**
- The ontology module (`apqc_<hierarchy>.ttl`).
- Inline provenance annotations as required by §4.
- A SHACL validation report (zero violations).
- A reasoner consistency report (no unsatisfiable classes).

---

## 3. Foundational commitments

These nine decisions are load-bearing. Every later phase depends on them; violating one silently corrupts the module. D8 and D9 are corpus-wide and **MUST** be fixed before any slice is transformed.

- **D1 — Partonomy, not taxonomy.** The PCF dotted hierarchy is meronomic. A child is an **occurrent part** of its parent, never an `rdfs:subClassOf` it. Decomposition links **MUST** use `cco:has process part`; they **MUST NOT** use `rdfs:subClassOf`.

- **D2 — The is-a hierarchy is engineered separately.** A process's genus is the *kind of act* it is, determined from the Element Description, **not** from its PCF position. Siblings routinely scatter across distinct act classes; non-adjacent PCF entries routinely share a genus.

- **D3 — Informational inputs/outputs are Information Content Entities.** They attach via `cco:has input` / `cco:has output` directly to the ICE class. They **MUST NOT** be modeled as roles.

- **D4 — Realizables inhere only in independent continuants.** Roles, dispositions, and capabilities **MUST** be borne by Agents, Organizations, or other independent continuants. A Role **MUST NOT** be placed on an ICE or any other generically dependent continuant — a specifically dependent continuant cannot inhere in a generically dependent one. This is why the input-as-role pattern valid for *material* inputs does not generalize to informational ones.

- **D5 — Reuse before mint.** A term **MUST** reuse an existing CCO/BFO class or property where one genuinely fits. A local (`ex:`) term **MAY** be minted only where no CCO/BFO term fits, and **MUST** then be anchored under the nearest correct CCO/BFO parent.

- **D6 — Verify before assert.** Every opaque CCO IRI (`cco:ont…`) used **MUST** be verified against the pinned CCO release — label, definition, *and* parent — before it is written into a module. Recognizing a label is not sufficient grounds to use the IRI (§6).

- **D7 — Stable identity is the PCF ID.** Primary class IRIs **MUST** be derivable from the PCF ID, which is stable across PCF releases. The Hierarchy ID is positional and **MUST NOT** be used for IRI minting or any subsumption decision.

- **D8 — Category policy is fixed corpus-wide.** Before transforming any slice, choose exactly one and record it in the corpus README and every module header. Modules **MUST NOT** mix policies.
  - **Policy A:** each APQC Category is modeled as a process aggregate class whose instances have the group-level processes as `has process part`.
  - **Policy B:** APQC Categories are not modeled as process classes; transformation begins at the Process-Group level.

- **D9 — Recurring local genera live in one shared extension module.** Local act genera that recur across slices (e.g. `ex:ActOfAnalysis`, `ex:ActOfIdentification`) **MUST** be defined once in a shared APQC extension module (e.g. `apqc-ext.ttl`) imported by every slice, never re-minted per slice. This prevents duplicate local universals.

---

## 4. Identity, minting, and provenance

- Mint one **primary** `owl:Class` per PCF entry, IRI anchored to the PCF ID (a human-readable local name **MAY** be added). Where an Element Description contains multiple independently classifiable processes, additional supporting process classes **MAY** be minted; the primary PCF class **MUST** retain the PCF identifiers and source text.
- A class minted **directly from a PCF entry** **MUST** carry `ex:pcfID`, `ex:hierarchyID` (annotated as positional/non-stable), and `ex:apqcSourceText` (verbatim Element Description).
- A **supporting local class** (act genus, ICE, role, capability, agent, subject matter) **MUST NOT** carry PCF row identifiers. It **MUST** carry `rdfs:label`, `skos:definition`, and provenance (`rdfs:comment`) explaining why it was minted and how it is anchored.
- The module header **MUST** record the pinned CCO version IRI it was built against.

This provenance layer makes the transform deterministic and auditable: the verbatim source text and stable key let any consumer (or audit) re-derive and diff a class without ambiguity. The scoping above matches the SHACL suite, which requires `ex:pcfID` only on process classes.

---

## 5. The transformation pipeline

Each phase lists its procedure and the rules that bind it.

### Phase 0 — Meta-decisions (once per corpus)
Fix the IRI-minting scheme (D7), the Category policy (D8), the shared-extension module (D9), and the upper-anchor strategy (§6). Pin the CCO release and vendor a local dependency closure (§9 Gate B).

### Phase 1 — Parse and de-conflate the Element Description
A PCF description fuses up to five distinct ontological commitments. Separate them before modeling:
1. the **process** itself (the lead gerund);
2. its **output(s)** (the artifact/judgement/decision produced);
3. its **method / sub-steps**;
4. its **participants** (agents, named or implied);
5. **cross-references** (bracketed PCF IDs, "feeds into", "drawing upon").

A BFO-aware parser (e.g. TagTeam.js) **SHOULD** perform first-pass extraction; a human **MUST** curate.

**Method-phrase criterion (layer 3).** A method phrase **MUST** become a `has process part` filler only when it denotes a **repeatable occurrent** that can occur as a proper part of the target process *and* is independently tracked (by APQC or the domain model). When it merely describes *how* the process is typically performed and is not independently tracked, it **MUST** remain in the class definition or an `rdfs:comment` — not the partonomy.

### Phase 2 — Classify the act (engineered is-a)
Determine the kind of act from the de-conflated verb, then anchor it per the **CCO reuse decision procedure (§6)**. The result is either a direct CCO Act class or a subclass of a **shared-extension** act genus (D9), which is itself anchored under the nearest correct CCO Act class.

### Phase 3 — Model inputs and outputs as ICEs
For each input/output, mint or reuse an ICE class and attach it.
- A representation / report / analysis / judgement **MUST** be a **Descriptive ICE** (`cco:ont00000853`).
- A specification or procedure that prescribes required, permitted, or recommended action **MUST** be a **Directive ICE** (`cco:ont00000965`).
- A **decision MUST** be a Directive ICE *only* where its content authorizes, selects, or prescribes future action. A decision **record** that merely registers that an agent selected an option **MUST** be a Descriptive ICE about the act of deciding and its selected outcome.
- An output that is *about* a portion of reality **SHOULD** carry an `is about` (`cco:ont00001808`) restriction to its subject class.
- A genuinely material input/output (rare in planning categories, common in operations categories) **MAY** use a material-entity filler; the input-as-role pattern then becomes available again (D4).

**Existential-necessity rule.** An input or output **MUST** be promoted to an existential (`owl:someValuesFrom`) class restriction *only* when its presence is necessary for **every** instance of the process type (i.e. definitional). Inputs/outputs the description merely cites as typical, exemplary, intermediate, or optional **MUST** instead be recorded as an annotation, a competency-question target, or a design note pending domain review — not as an existential restriction.

### Phase 4 — Model realizables and participants
- A named or implied agent **MUST** be an `cco:Agent` or `cco:Organization`, not bare `bfo:material entity`.
- An agent's competence **SHOULD** be a capability anchored under `cco:Agent Capability` (or `cco:Organization Capability`), linked by `cco:has capability`, and `realized in` the act.
- Roles **MUST** be borne via `bfo:bearer of` by independent continuants only (D4).
- Participation **MUST** use `bfo:has participant`.

### Phase 5 — Build the partonomy
Render every parent→child PCF link as a `cco:has process part` restriction on the parent (D1). Use existential restrictions; do **not** assert exhaustive closure unless the PCF children are genuinely complete (they are usually illustrative).

### Phase 6 — Chain and order
Where the source text licenses it (cross-references, "feeds into"), assert `bfo:precedes` and/or make the **output ICE** of one process a `has input` filler of another. Among parallel facets of a single scan, assert **no** ordering.

### Phase 7 — Definitions and annotations
Write a genus-differentia definition for every class (§7) and complete the required annotations (§4). Record any rejected CCO candidate in an `rdfs:comment` (§6).

### Phase 8 — Validate
Run all gates (§9). A failing mandatory gate halts release.

---

## 6. CCO reuse decision procedure (verify-before-assert)

For each term the module needs:

1. **Search** the pinned CCO release for candidate classes/properties by label and definition.
2. **Verify** each candidate against the actual ontology: read its `rdfs:label`, its definition, **and its parent chain**. A matching label is *not* sufficient.
3. **Decide:**
   - If a candidate's *definition* fits the intended meaning → reuse its IRI.
   - If no candidate fits → mint a local subclass (in the shared extension module if recurring, D9) under the nearest correct CCO/BFO parent, and record the rejected candidate(s) and the reason in `rdfs:comment`.
4. **Pin** the IRI; never reconstruct an `ont…` IRI from memory.

> **Normative caution — false-friend labels.** A CCO label can match the surface word while its definition denotes a different universal. In the reference work, `cco:ont00001261` *Act of Identifying* was rejected: its definition is "an Act of Representative Communication performed by asserting who or what a thing is" — a *communication* act — whereas APQC "Identify …" denotes *discernment*. Discernment was modeled as a shared-extension subclass of `Act of Information Processing` instead. Skipping Step 2 here would have misclassified every "Identify" process under communication.

### Verified core terms (CCO v2.0, 2024-11-06)

**Properties**

| IRI | Label | Notes |
|---|---|---|
| `cco:ont00001921` | has input | process → continuant; input present at start |
| `cco:ont00001986` | has output | process → continuant; output present at end |
| `cco:ont00001777` | has process part | subPropertyOf `bfo:has occurrent part`; process→process |
| `cco:ont00001808` | is about | domain ICE; range entity |
| `cco:ont00001954` | has capability | subPropertyOf `bfo:bearer of`; Agent → Agent Capability |

**Classes**

| IRI | Label | Use |
|---|---|---|
| `cco:ont00000958` | Information Content Entity | ICE root |
| `cco:ont00000853` | Descriptive ICE | reports, analyses, judgements, decision records |
| `cco:ont00000965` | Directive ICE | specifications, procedures, prescriptive decisions |
| `cco:ont00001017` | Agent | individual agents |
| `cco:ont00001180` | Organization | organizational agents |
| `cco:ont00001379` | Agent Capability | agent competence |
| `cco:ont00000568` | Organization Capability | organizational competence |
| `cco:ont00000228` | Planned Act (alt: Intentional Act) | top intentional-act anchor |
| `cco:ont00000366` | Act of Information Processing | analysis, discernment |
| `cco:ont00000636` | Act of Appraisal | assessment, evaluation, judgement |
| `cco:ont00000511` | Act of Planning | producing plans / procedures / strategy |
| `cco:ont00001261` | Act of Identifying | **REJECTED** for discernment (communication sense) |

**BFO relations/classes used:** `bfo:process` (`BFO_0000015`), `generically dependent continuant` (`0000031`), `material entity` (`0000040`), `role` (`0000023`), `disposition` (`0000016`), `realizable entity` (`0000017`), `bearer of` (`0000196`), `realized in` (`0000054`), `has participant` (`0000057`), `precedes` (`0000063`), `has occurrent part` (`0000117`).

### Additional verified Act classes (corpus-wide consolidation, CCO v2.0)

These CCO Act classes were verified (label + definition + parent chain) against the pinned closure during the 13-section transform and are used as genus anchors (directly, or as the parent of a shared-extension genus in apqc-ext.ttl). Where CCO has no fitting class, a local genus was minted in apqc-ext.ttl and records its rejected CCO candidate per verify-before-assert.

| IRI | Label | Verified note |
|---|---|---|
| `cco:ont00000402` | Act of Communication | A Planned Act in which some Information Content Entity is transferred from some Agent to Another. (Parent: cco:ont00000228 Planned Act.) The verified communication anchor (NOT the §6 false-friend reject cco:ont00001261 'Act of Identifying'); anchor for ex:ActOfCommunication. |
| `cco:ont00000151` | Act of Reporting | An Act of Representative Communication performed by giving a detailed account or statement. (Parent: cco:ont00000379 Act of Representative Communication.) CCO's leaf reporting act; reuse directly for pure submission/forwarding of an already-prepared report. The broader ex:ActOfReporting anchors at ont00000379 to also cover scorecards/filings/disclosures. |
| `cco:ont00000345` | Act of Measuring | A Planned Act that involves determining the extent, dimensions, quantity, or quality of an Entity relative to some standard. (Parent: cco:ont00000228 Planned Act.) Parent of cco:ont00000636 Act of Appraisal; the direct anchor for single quantification-against-a-standard nodes. |
| `cco:ont00000950` | Act of Maintenance | An Act of Artifact Modification in which a Material Artifact is modified in order to preserve or restore one or more of its designed Qualities or Functions. (Parent: cco:ont00000970 Act of Artifact Modification.) The recurring reject across ex:ActOfDataManagement, ex:ActOfAcquisition, ex:ActOfImplementation, ex:ActOfImprovement, ex:ActOfAdministration, ex:ActOfDeployment, ex:ActOfAccounting (it modifies Material Artifacts, not processes/records/ICEs). |
| `cco:ont00000234` | Act of Training | A Planned Act in which knowledge, skills or values are imparted from one or more Agents to at least one other Agent. (Parent: cco:ont00000228 Planned Act.) Verified for train/educate processes (no local genus minted; reuse directly). |
| `cco:ont00000970` | Act of Artifact Modification | An Act of Material Artifact Processing in which an existing Material Artifact is acted upon in a manner that changes, adds, or removes one or more of its Qualities, Dispositions, or Functions. (Parent: cco:ont00000908 Act of Material Artifact Processing.) Parent of cco:ont00000950 Act of Maintenance; cited as a reject for ex:ActOfDisposition. |
| `cco:ont00000379` | Act of Representative Communication | An Act of Communication that commits a speaker to the truth of the expressed proposition (scopeNote includes announcing, disclosing, informing, reporting, stating). (Parent: cco:ont00000402 Act of Communication.) Anchor for ex:ActOfReporting; superclass of CCO's leaf cco:ont00000151 Act of Reporting. |
| `cco:ont00000065` | Act of Location Change | An Act of Motion in which the location of some Object is changed by some Agent. (Parent: cco:ont00000357 Act of Motion -> cco:ont00000228 Planned Act.) Anchor for ex:ActOfTransportation; parent of cco:ont00000595 Act of Cargo Transportation. |
| `cco:ont00000371` | Act of Prediction | A Planned Act that involves the generation of a Predictive Information Content entity intended to describe an uncertain possible future event, value, entity, or attribute of an entity. (Parent: cco:ont00000228 Planned Act; output: cco:ont00000626 Predictive ICE.) Anchor for ex:ActOfForecasting. |
| `cco:ont00000051` | Act of Construction | An Act of Material Artifact Processing wherein Material Artifacts are built on site as prescribed by some contract. (Parent: cco:ont00000908 Act of Material Artifact Processing.) Cited as a reject for ex:ActOfDesign and ex:ActOfDevelopment; the direct anchor where an act builds material artifacts on site. |
| `cco:ont00000684` | Act of Contract Formation | An Act of Promising having a lawful object entered into voluntarily by two or more agents with legal capacity, each intending to create one or more legal obligations between them. (Parent: cco:ont00000821 Act of Promising -> cco:ont00001162 Act of Commissive Communication -> cco:ont00000402 Act of Communication.) Evaluated and rejected for ex:ActOfNegotiation (it is the consummating promise, narrower than the bargaining process); listed for the contracting verbs that genuinely form a contract. |
| `cco:ont00000908` | Act of Material Artifact Processing | A Planned Act of performing a series of physical operations on a material artifact in order to change or preserve the artifact. (Parent: cco:ont00000228 Planned Act.) Anchor for ex:ActOfProduction; parent of cco:ont00000970, cco:ont00000051, cco:ont00001359. |
| `cco:ont00000595` | Act of Cargo Transportation | An Act of Location Change wherein some Payload is moved from one location to another. (Parent: cco:ont00000065 Act of Location Change.) Cited as the close-but-too-narrow sibling rejected in favor of ex:ActOfTransportation; reuse directly where a Payload is conveyed. |
| `cco:ont00000836` | Act of Financial Instrument Use | An Act of Artifact Employment in which some Agent uses some Financial Instrument. (Parent: cco:ont00000566 Act of Artifact Employment.) Anchor for ex:ActOfPayment; parent of cco:ont00001334 Act of Purchasing. |
| `cco:ont00000433` | Act of Association | A Social Act wherein an Agent unites with some other Agent in a Planned Act, enterprise or business. (Parent: cco:ont00001327 Social Act.) Anchor for ex:ActOfRelationshipManagement. |
| `cco:ont00001158` | Act of Data Transformation | An Act of Information Processing in which an algorithm is executed to act upon one or more input Information Content Entities into one or more output Information Content Entities. (Parent: cco:ont00000366 Act of Information Processing.) Cited as a reject for ex:ActOfDataManagement (which need not execute an algorithm). |
| `cco:ont00001327` | Social Act | A Planned Act having an objective that affects, is performed by, or is performed on behalf of, a community or group of Persons. (Parent: cco:ont00000228 Planned Act.) Anchor for ex:ActOfAdvocacy. NOTE: this is 'Social Act', NOT 'Act of Social Movement' (that is the distinct IRI cco:ont00000079, a subclass of this one) -- a false-friend caution. |

---

## 7. Definition standard

Every class **MUST** carry a `skos:definition` in **genus-differentia** form, matching the dependency ontologies' convention — "*A ⟨genus⟩ that ⟨differentia⟩*" — where:
- ⟨genus⟩ names the immediate (CCO/BFO or shared-extension) parent;
- ⟨differentia⟩ states the distinguishing conditions so the definition supports clarity, inclusiveness, and exclusiveness checks;
- for ICEs that represent a subject, the differentia **SHOULD** name the aboutness target.

CCO's own definitions do not restate the defined term (e.g. Information Content Entity is "A Generically Dependent Continuant that…"); this specification follows that convention. Restating the label (*"Analyze Competitors is an Act of Analysis that…"*) is **PERMITTED** but not required, and a module **MUST** apply one style uniformly.

Every class **MUST** carry `rdfs:label`. Every **process** class **MUST** additionally carry the PCF provenance of §4 (if PCF-derived) and **SHOULD** carry `skos:example` and an `rdfs:comment` recording any non-obvious modeling choice.

---

## 8. Canonical patterns

The reference module `apqc_1_1_1.ttl` is the authoritative pattern library. The five reusable patterns are:

- **Process** — `ex:Proc rdfs:subClassOf <act genus>, [has input some <ICE>], [has output some <ICE>], [has participant some <Agent>]` (each restriction subject to the Phase 3 existential-necessity rule).
- **Descriptive output with aboutness** — `ex:Report rdfs:subClassOf cco:Descriptive-ICE, [is about some <Subject>]`.
- **Directive output** — prescriptive specifications/decisions `rdfs:subClassOf cco:Directive-ICE`.
- **Agent + role + capability triad** — `ex:Agent rdfs:subClassOf cco:Agent, [has capability some <AgentCapability>], [bearer of some <Role>]`; the capability is `realized in` the act.
- **Partonomy** — parent `rdfs:subClassOf [has process part some <Child>]`, repeated per child.

---

## 9. Validation gates

A module is released only after passing the gates below. **A–D are mandatory; E–F are strongly recommended.**

- **Gate A — Syntax.** The module parses as valid Turtle.
- **Gate B — IRI resolution.** Every `cco:`/`obo:` IRI referenced resolves to a declared term. Gate B **MUST** be run against the locally vendored / CI-pinned dependency closure corresponding to the pinned CCO release and its BFO import. Live web resolution **MAY** be used diagnostically but **MUST NOT** be required for release; this preserves reproducibility and offline determinism.
- **Gate C — SHACL.** Validation with `apqc_shapes.ttl` (advanced mode) yields **zero violations**; warnings are reviewed and dispositioned. The eight shapes enforce: process annotation completeness; process anchored to a CCO Act; output is an ICE; input is a recognized continuant kind (warn); process-part filler is a process; **no process subsumes another process**; no role inheres in a GDC; `is about` only on an ICE.
- **Gate D — Reasoner.** An OWL reasoner (ELK or HermiT) over module + pinned closure reports the ontology consistent with **no unsatisfiable classes**. Thin classes (a single restriction) **MUST** be inspected here for the over-commitment risk of Phase 3.
- **Gate E — Competency questions.** A fixed CQ set returns expected answers (e.g. "which acts produce an ICE consumed by a downstream strategy act?").
- **Gate F — Human semantic review.** A reviewer confirms each process is anchored to the *correct* act (Gates C/D confirm an anchor exists, not that it is the right one) and that definitions pass inclusiveness/exclusiveness.

> **Limit.** Gates A–D are structural and logical; they cannot judge the semantic correctness of an anchor. An analysis act mis-filed under *Act of Planning* passes A–D. Gate F is therefore not optional in spirit.

A regression fixture of deliberately non-conformant classes (`apqc_bad_examples.ttl`) **MUST** be retained and asserted to keep producing its expected violation count; a drop signals a shape has silently stopped firing.

---

## 10. Standing cautions

- **Existential over-commitment.** See the Phase 3 existential-necessity rule; thin classes are re-checked at Gate D.
- **Precedence discipline.** Assert ordering only where the source licenses it. Parallel facets of one scan get none.

*(The Category-as-aggregate question, formerly here, is now foundational — D8.)*

---

## 11. Tooling and determinism

- Parsing/validation: `rdflib` (Gates A–B), `pyshacl -a` (Gate C), ELK/HermiT (Gate D).
- The CCO release **MUST** be pinned in the module header and in CI, and resolved from a local closure (Gate B); transforms are otherwise non-reproducible across CCO versions.
- The pipeline is deterministic and scriptable end to end, suiting it to CI and to hash-chained audit of each released slice.

---

## 12. Module architecture, artifacts, and versioning

**Architecture.**
- One **shared extension module** (`apqc-ext.ttl`, D9): recurring local act genera and any cross-slice patterns; imports the pinned CCO closure.
- One **slice module** per PCF subtree (`apqc_<hierarchy>.ttl`): imports the shared extension; contains the PCF-derived classes and their slice-local supporting classes.
- A single **Category policy** (D8) applied across all slice modules.

**Artifacts & versioning.**
- Slice modules are versioned with semantic versioning; a changelog block in the header records each pass (the reference module moved `v0.1.0` structural → `v0.2.0` CCO-conformant this way).
- The shared extension, the SHACL suite, the bad-examples fixture, and this specification are versioned independently and referenced by pinned version from each module's evidence record.

---

## Appendix A — Worked transform (PCF 19945, end to end)

**Source row.** `19945 | 1.1.1.1 | "Identifying your competitors, their service and/or product. Evaluating competitors strategies to determine their strengths and weaknesses relative to those of your own product or service."`

**Phase 1 (de-conflate).** Process = analyze competitors; output = a competitor analysis; participant = a competitive-intelligence agent; subject = competitor organizations. The method phrase "evaluating competitors' strategies to determine strengths and weaknesses" is *not* independently tracked by APQC, so by the Phase 1 method-phrase criterion it stays in the definition rather than becoming a process part.

**Phase 2 (classify).** Analysis → information processing. CCO has no generic analysis class (verified), so the genus is the shared-extension class `ex:ActOfAnalysis ⊑ cco:ont00000366` (D9 — defined once in `apqc-ext.ttl`, not re-minted here).

**Phase 3 (I/O).** Input `ex:CompetitorData ⊑ Descriptive ICE`; output `ex:CompetitorAnalysis ⊑ Descriptive ICE, [is about some ex:Competitor]`. Producing a competitor analysis is definitional for this process type, so the output is promoted to an existential restriction; the input likewise.

**Phase 4 (realizables).** `ex:CompetitiveIntelligenceAnalyst ⊑ cco:Agent, [has capability some ex:CompetitiveAnalysisCapability], [bearer of some ex:…AnalystRole]`; `ex:Competitor ⊑ cco:Organization, [bearer of some ex:CompetitorRole]`.

**Phase 5 (partonomy).** Parent `1.1.1` gets `[has process part some ex:AnalyzeCompetitors]`.

**Phase 7 (definition, CCO house style).** "An Act of Analysis that has as input competitor data and has as output a competitor analysis about one or more competitors."

**Phase 8 (validate).** Passes Gates A–C against the local closure; A–D with the reasoner.

Resulting axiom set (the genus `ex:ActOfAnalysis` resides in `apqc-ext.ttl`):

```turtle
ex:AnalyzeCompetitors a owl:Class ;
    ex:pcfID "19945" ; ex:hierarchyID "1.1.1.1" ;
    ex:apqcSourceText "Identifying your competitors, ..." ;
    rdfs:label "Analyze competitors" ;
    skos:definition "An Act of Analysis that has as input competitor data and has as output a competitor analysis about one or more competitors." ;
    rdfs:subClassOf ex:ActOfAnalysis ,
        [ a owl:Restriction ; owl:onProperty cco:ont00001921 ; owl:someValuesFrom ex:CompetitorData ] ,
        [ a owl:Restriction ; owl:onProperty cco:ont00001986 ; owl:someValuesFrom ex:CompetitorAnalysis ] ,
        [ a owl:Restriction ; owl:onProperty obo:BFO_0000057 ; owl:someValuesFrom ex:CompetitiveIntelligenceAnalyst ] .
```
