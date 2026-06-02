# Direction — APQC Category & Upper-Level Modeling

**Architectural Decision Record ADR-001**
**Status:** Accepted · **Supersedes:** the provisional binary D8 (Policy A / Policy B) in Methodology v1.1.0 · **Folds into:** Methodology D8 at next bump (v1.2.0).

---

## Decision

Model the APQC PCF in **two layers**, and keep them strictly separate:

1. A **catalog layer** that represents every PCF node, at every level, as a classification entry. Generated mechanically from source; total coverage; no ontological judgement.
2. A **reality layer** of genuine BFO process universals, built only where a node denotes a real bounded process. Grown incrementally; carries the modeling judgement.

The two are connected by a **bridge** annotation. **Categories are catalog nodes; they are not modeled as process universals** unless they independently pass the bounded-occurrent test (rare). Standing-function categories ("Manage X") may additionally be modeled as organizational capabilities.

This replaces "choose Policy A or Policy B." Neither applies uniformly, because the 13 categories are not a uniform ontological kind.

---

## Rules (normative)

**R1 — Catalog layer is mandatory and total.**
Every PCF row (Category → Process Group → Process → Activity → Task) **MUST** be emitted as a catalog node:
- typed `cco:ont00000853` (Descriptive ICE) and `skos:Concept`, `skos:inScheme apqc:PCF`;
- carrying `ex:pcfID`, `ex:hierarchyID`, `ex:apqcSourceText`, `skos:prefLabel`;
- the dotted hierarchy expressed as `skos:broader`, declared explicitly as a **curatorial** relation, **NOT** parthood.
This layer **MUST** be generated deterministically from the PCF export, with 100% row coverage, before any reality-layer modeling.

**R2 — Reality layer is selective.**
A node is promoted to a BFO process universal (`owl:Class rdfs:subClassOf` a CCO Act) **only if** it passes the **bounded-occurrent test** (R5). There is **no fixed cut level**: the test is applied per node, top to bottom. `cco:has process part` (D1) is used **only** within the reality layer, for genuine mereology, and existentially only where the part is definitional (Phase-3 necessity rule).

**R3 — Categories.**
A Category **MUST** be a catalog node. A Category **MUST NOT** be given existential `has process part` restrictions to its children — APQC states that not every listed process exists in every organization, so such restrictions are false. A Category **MAY** also receive a reality-layer universal only if it passes R5 (e.g. a coarse but bounded strategy cycle); otherwise it has no reality-layer class.

**R4 — Bridge.**
A catalog node links to its reality-layer universal (or capability) via the annotation property `ex:designatesProcessType`. It is an `owl:AnnotationProperty` (keeps the module in OWL DL; avoids ICE-to-class punning). A catalog node with no coherent corresponding universal **MUST** have no bridge — this is the correct, honest outcome.

**R5 — The bounded-occurrent test (the one judgement per node).**
Model a node in the reality layer **iff** it denotes a *repeatable occurrent with an identifiable beginning and end that can occur as a proper part of a larger process*.
- Passes → reality-layer process universal (almost always Process / Activity / Task; often Process Group).
- Denotes a *standing function or capacity* (no natural end; realized in recurring episodes) → catalog only; **SHOULD** add a capability per R6.
- Denotes only a *grouping or heading* → catalog only.

**R6 — Function enrichment.**
A standing-function category or group ("Manage IT", "Manage Financial Resources", "Develop and Manage Human Capital") **SHOULD** be modeled as an `owl:Class rdfs:subClassOf cco:ont00000568` (Organization Capability), borne by the organization and `realized in` the underlying acts, and bridged from its catalog node via R4.

**R7 — No layer mixing.**
`skos:broader` appears **only** in the catalog layer; `cco:has process part` and `rdfs:subClassOf`-to-an-Act appear **only** in the reality layer. The curatorial hierarchy and the mereological/taxonomic structure **MUST NOT** be conflated.

---

## Rationale (compressed)

- **Heterogeneity.** APQC's own categories span operating-process families and management/support standing functions; no single BFO category covers both, so a uniform "categories are processes" (A) or "ignore categories" (B) mistypes a large fraction either way.
- **Necessity.** APQC explicitly disclaims that every listed process exists in every organization, which makes category→child existential parthood false to the source.
- **Cost.** The catalog gives full structural coverage immediately and deterministically; the expensive, judgement-bearing ontology work accrues only where warranted. This is the lowest-commitment option, not the heaviest.

---

## Consequences

- **Methodology:** rewrite D8 to this two-layer policy at v1.2.0; the §10 category note is fully retired.
- **Reference module (`apqc_1_1_1.ttl`):** `DevelopVisionAndStrategy` (10002) moves to the catalog layer (it is a category heading). `DefineBusinessConcept` (17040) stays a reality-layer universal (it passes R5) but is reached from its catalog node via the R4 bridge, not as a `has process part` filler of the category. The intra-1.1.1 partonomy is unaffected.
- **New artifacts:** `apqc-catalog.ttl` (generated, all rows) and `apqc-ext.ttl` (shared act genera, per D9). Slice modules import both.
- **SHACL additions:** (a) a catalog ICE **MUST NOT** bear `cco:has process part`; (b) a reality-layer process **MUST NOT** use `skos:broader`; (c) an `ex:designatesProcessType` target **MUST** be a process universal or a capability class. These extend `apqc_shapes.ttl` and the bad-examples fixture.

---

## Build order

1. Generate `apqc-catalog.ttl` from the PCF export (R1) — deterministic, no judgement.
2. Stand up `apqc-ext.ttl` with the shared act genera (D9).
3. For each slice, apply R5 per node to populate the reality layer; bridge via R4; enrich functions via R6.
4. Extend the SHACL suite and fixture; re-run Gates A–F.
