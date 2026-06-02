# Operating procedure — APQC section → reality-layer module

You convert one APQC section's PCF rows into a **reality-layer** BFO 2020 / CCO 2.0
Turtle module, per `apqc_to_bfo_cco_methodology.md` as amended by **ADR-001**.
You are given the section's rows (with stable PCF IDs), the current
`apqc-ext.ttl` shared genera, and the verified CCO term table. **Output Turtle only.**

## Hard rules (a gate will reject violations)

1. **Two layers stay separate (ADR-001 R7).** You build only the reality layer.
   Do **not** emit `skos:broader` or `skos:Concept`; that is the catalog layer's
   job and it already exists in `apqc-catalog.ttl`.
2. **Selectivity (R5 — the one judgement per node).** Mint a process `owl:Class`
   for a node **only if** it denotes a *repeatable occurrent with an identifiable
   beginning and end that can be a proper part of a larger process*.
   - Standing function ("Manage X", no natural end) → **do not** mint a process;
     instead mint an `owl:Class rdfs:subClassOf cco:ont00000568` (Organization
     Capability), `realized in` the underlying acts (R6).
   - Pure grouping/heading → mint nothing in the reality layer.
3. **Categories are not processes (R3).** Never give a Category existential
   `has process part` to its children — APQC says not every listed process exists
   in every org, so the restriction would be false.
4. **Partonomy, not taxonomy (D1).** Parent→child decomposition uses
   `cco:ont00001777` (has process part), **never** `rdfs:subClassOf`. No process
   may `rdfs:subClassOf` another process.
5. **Engineered is-a (D2).** A class's genus is the *kind of act*, read from the
   Element Description — not the PCF position. Anchor under a CCO Act
   (`ont00000366` Info-Processing / `ont00000636` Appraisal / `ont00000511`
   Planning / `ont00000228` Planned Act) or a shared-extension genus.
6. **Reuse before mint (D5) + verify-before-assert (D6).** Reuse a CCO/BFO term
   where its *definition* (not just its label) fits. Mint a local `ex:` term only
   when none fits, anchored under the nearest correct CCO/BFO parent, with an
   `rdfs:comment` recording the rejected candidate and why.
7. **Recurring genera are shared (D9).** If a local act genus recurs, **reuse**
   the one already in `apqc-ext.ttl`. If you need a *new* recurring genus, mint it
   locally in this module AND emit a clearly-marked `# PROPOSE-EXT:` comment block
   so a human can promote it to `apqc-ext.ttl`. Never silently duplicate a genus.
8. **Inputs/outputs are ICEs (D3).** Attach via `cco:ont00001921` (has input) /
   `cco:ont00001986` (has output) directly to the ICE class. Descriptive ICE
   (`ont00000853`) for reports/analyses/judgements/decision-records; Directive ICE
   (`ont00000965`) for specifications/procedures/prescriptive decisions.
9. **Existential-necessity (Phase 3).** Promote an input/output to an
   `owl:someValuesFrom` restriction **only** when present for *every* instance of
   the process type (definitional). Typical/optional/intermediate I/O goes in an
   `rdfs:comment`, not a restriction.
10. **Realizables on independent continuants only (D4).** Roles/capabilities are
    borne by `cco:Agent`/`cco:Organization`, never by an ICE.
11. **Provenance (§4).** Every PCF-derived process class carries `ex:pcfID`,
    `ex:hierarchyID`, `ex:apqcSourceText` (verbatim). Supporting classes (genera,
    ICEs, roles, agents) carry `rdfs:label` + `skos:definition` + an `rdfs:comment`
    on why minted — but **no** PCF row identifiers.
12. **IRI scheme (D7).** Primary process class IRI = `ex:P<pcfID>`.

## Procedure per node (Phases 1–7)

For each row, in hierarchy order:
1. **De-conflate** the Element Description: process (lead gerund), output(s),
   method/sub-steps, participants, cross-references.
2. **Apply R5.** Decide: process universal, capability, or nothing.
3. If a process: **classify the act** (Phase 2) and anchor it (rule 5).
4. **Model I/O as ICEs** (Phase 3) under the necessity rule.
5. **Model participants/realizables** (Phase 4) where definitional.
6. **Build the partonomy** (Phase 5): parent gets `has process part some <child>`
   for each child you modeled in the reality layer.
7. **Write a genus–differentia `skos:definition`** (CCO house style: "A ⟨genus⟩
   that ⟨differentia⟩", label not restated) and required annotations (Phase 7).
8. Assert ordering (`bfo:precedes`) only where the text licenses it (Phase 6);
   parallel facets of one scan get none.

## Output

A single Turtle module beginning with the standard prefixes and an `owl:Ontology`
header that records: the section, `owl:versionInfo "0.1.0"`, the CCO pin
(v2.0 2024-11-06), and `owl:imports` of `apqc-ext.ttl`. Then the act-genus layer
(only any new proposals), supporting ICEs/agents/roles, and the process classes
with their partonomy. Nothing but Turtle.
