# WP6: semantic impact of the corrections of 2026-11-03

The BPO architect's decisions of 2026-11-03, §8: for each correction, whether it
changes the asserted axioms, the inferred hierarchy, or BPO's validation behaviour.
"Inferred" is the named-class `rdfs:subClassOf` set of the ELK-reasoned corpus merge
(13 slices, registry, catalog, capability layer, wiring, pinned CCO), diffed
commit to commit. Checks per commit: Gates A–D on the changed slices, corpus ELK,
Gate F, C1–C7, matchability. The full suite ran on `8fe1246` and runs again on the
last commit.

| Commit | Correction | Asserted change | Inferred hierarchy | Validation behaviour |
|---|---|---|---|---|
| `8fe1246` | B8 step 1: realized-in axioms removed | −197 restrictions on `*Capability` classes; the pairs move to `capability_scope.json`; wiring graph unchanged | **no change** (4,553 pairs) | unchanged; Gate F 39 |
| `2056356` | B4: IRI migrations page | none (site tooling) | — | — |
| `da2e573` | Decision A: P11035/P11036 are acts | 2 classes leave `568` + their capability parent for `ActOfRelationshipManagement`; 2 realized-in restrictions gone; no has-process-part | **4 pairs change** (the two classes' parents) | Gate F **39 → 37**, two documented repairs; B8 +2 possible realizations |
| `d80496f` | `PerformanceMeasureSpecification` (965) | 1 class added; 4 slice 3 restrictions repointed | **+1 pair** (the new class ⊑ 965) | unchanged; three Formulation acts now output a Directive ICE |
| `027be8a` | P12721 under Act of Location Change | 1 parent changed (595 → 065) | **1 pair changes** | unchanged |
| `1686f4e` | `enablesProcess` label/definition; P21437 uncertain | annotation text; 1 wiring triple removed | no change | unchanged; P21437 had no requirement |
| `cadaa1d` | delivery requirements audited | 2 `requiresCapability` triples removed | no change | 2 processes still routable, by role alone |
| `0e2791b` | P12721 parent revised to `bpo:ActOfTransportation` (architect, second decision) | 1 direct parent changed (065 → `ActOfTransportation`); redundant explicit `228` dropped; the registry genus inlined in slice 10 | **1 pair changes** (`P12721 ⊑ 065` → `P12721 ⊑ ActOfTransportation`; 065 stays an ancestor); 4,554 pairs | unchanged; C1–C7 57,793 triples (−1, the dropped `228`); Gate F 37, run with the 900 s linter limit lifted (two timeouts under machine load, then 774 s) |
| `6d2b1fa` | `ITServiceSolution` narrowed to a material Infrastructure System (`870`) | parent `117` → `870` (+ explicit `BFO_0000040`); new definition; 4 of 20 participant restrictions removed (P20679, P20697, P20815, P20823), 16 kept; slice 8 −15 triples | **1 pair changes** (`ITServiceSolution ⊑ 117` → `⊑ 870`); the class leaves Material Artifact; 4,554 pairs | unchanged; C1–C7 57,778 triples (−15); Gate F 37 (linter 570 s, limit lifted); matchability 30/167 |
| `702641c` | 57 realization definitions reworded to possible realization | 57 `skos:definition` literals in 12 slices; no axiom (checked: each slice graph minus its definitions is isomorphic to before) | **no change** (4,554 pairs) | unchanged; Gate F 37 (linter 450 s); C1–C7 0; matchability 30/167 |
| (this commit) | the 3 kept delivery requirements accepted; `requiresCapability` scope note | 1 `skos:scopeNote` on the property; text added to 3 process comments; no requirement added or removed | **no change** (4,554 pairs) | unchanged; C1–C7 57,779 triples (+1); Gate F 37 (linter 423 s); matchability 30/167 |


**Dispatch** stays at 30 routable / 167 gaps over 197 processes with requirements
throughout this batch. Per the architect's §4D, the 256 processes with no requirement
since B8 are **not assessed** (`b8-not-assessed.tsv`), and the figures are not
comparable as rates with the pre-B8 453/64/389.

**Not changed, registered for decision:** `ITServiceSolution` (suspected defect,
`itservicesolution-review.md`); the 37-class capability-as-process backlog and its
111 restrictions, and the definitions of the 20 backlog P-classes that say they are
realized (decided with each class). The 53 definitions registered here earlier were
57, and are reworded (`b8-realization-definitions.tsv`).

**The A9 comparison is untouched.** No template check was added to or removed from
the instruments that measured S0 and S1.
