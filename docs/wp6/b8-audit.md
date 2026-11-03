# WP6 B8: the 356 capability–process pairs, classified

2026-11-02. The architect's decisions (2026-10-31 and 2026-11-02): audit all 356
pairs, with no automatic inference; review the 197 axiom-derived and the 159
table pairs separately; classify each pair as a possible realization, an enabling
relation or a necessary requirement. For the 339 Organization Capability pairs,
the default is possible realization. A pair becomes a necessary requirement only
with independent evidence, and that includes the 17 agent-capability pairs.

## The problem

`bpo:requiresCapability` was generated as the inverse of every `bpo:enablesProcess`
pair (PHASE1 decision ii), so each pair said "process P needs capability C". But:

- **339 pairs name an Organization Capability (`568`)**, which in CCO (2024-11-06)
  "inheres in an Organization". Dispatch assigns a process to an agent; that agent
  does not bear the organization's capability. These pairs say where the organization's
  standing function is realized, not what the assigned agent must bear.
- **197 pairs come from slice axioms** `C ⊑ ∃ realized in (BFO_0000054) P`. They
  support "C is realized in some P", not "every P needs C". The inversion added
  that necessity.
- **159 pairs come from `capability_scope.json`**, a judgment table of the processes
  a capability's scope covers. Being in scope is not a requirement either.

## The classification (`capabilities/b8_pairs.tsv`)

One row per pair, with its source, bearer category, target kind, classification
and basis. `scripts/assemble_wiring.py` reads it, and it stops on any pair that has
no row, or any row that has no pair.

| Classification | Pairs | Basis |
|---|---|---|
| possible realization | **342** | 197 by the slice's realized-in axiom (2 of them name an act genus, `bpo:ActOfAdministration`, not a PCF process); 145 from the scope table, each process within its capability's definition, checked per capability. Two are weak (below) |
| enabling | 0 | No pair was found where the capability enables the process without being realized in it |
| necessary requirement | **0** | No pair has independent evidence that every performance of the process needs the capability. This includes the 17 agent-capability pairs: each capability is defined as realized in acts of the kind, but nothing says every such act needs it |
| excluded: the target is a capability | **14** | 13 in section 12 and one in section 2: the target is a `bpo:P<id>` class modelled as an Organization Capability (P11010, P11012, P11013, P11035, P11036, P11038–P11041, P11045, P11047–P11049). They are left out of the wiring until the act-versus-capability question (decision A, P11035/P11036) is settled |

The two weak possible realizations:
- `CustomerServiceCapability` → P16928 (upsell/cross-sell opportunities): kept,
  because P16928 works from a customer inquiry, which the definition covers.
- `EmployeeRelationsCapability` → P21437 (monitor employment law): in the same APQC
  group (7.4), but outside the definition's wording.

## Wiring

| | Before | After |
|---|---|---|
| `enablesProcess` | 356 | 342 |
| `requiresCapability` (wiring) | 357 occurrences (356 pairs; one pair harvested in two sections) | 0 |
| `requiresRole` | 197 | 197 |

## Dispatch (12-agent demo fleet, `scripts/matchability.py`)

| | Before | After |
|---|---|---|
| Processes with any requirement | 453 | 197 |
| Routable | 64 | 30 |
| Coverage gaps | 389 | 167 |

- **256 processes carried only a capability requirement**, and now carry none. 40 of
  them were routable. A process with no requirement is not counted by the report.
- **Of the 197 that still carry requirements, none lost routability.** 24 were
  routable before and after; 6 became routable, because their only unmet
  requirement was a capability.
- **The 3 remaining capability gaps** come from 5 `requiresCapability` triples
  authored directly in `delivery_processes.ttl` (AuthorRoadmap,
  AuthorImplementationPlan, and the three FNSR delivery acts). They are not among the
  356 wiring pairs and were not audited here.

The drop in routable processes is not a regression. The earlier figure counted
assignments justified by requirements nobody had shown to be necessary. As the
architect asked, this report gives both the quantity and the basis of the assignments.

The 256 are listed in `b8-not-assessed.tsv`, each with the capability requirements it
lost and whether it was routable before. They are **not assessed** by requirement-based
dispatch: neither valid nor invalid assignments (BPO architect, 2026-11-03, §4D). So
the before and after figures above are not comparable as rates: the denominator lost
256 processes.

## Step 1 (2026-11-03): the 197 slice axioms removed

The architect's decision of 2026-11-03 (§4A): `C ⊑ ∃ realized in P` says that every
instance of capability C *is* realized in some instance of P. Under BFO a realizable
entity can exist unrealized, and nothing in this audit gives evidence of necessary
realization for any of the 197. They are removed. The possible-realization
information is kept at class level:

- **The pairs** move to `capabilities/capability_scope.json`, from which
  `bpo:enablesProcess` is generated. Their `b8_pairs.tsv` rows keep `source = axiom`,
  and their basis now records the removal.
- **Instance level.** That a particular capability instance is realized in a particular
  process instance is stated with BFO's `realized in` (`obo:BFO_0000054`) between the
  instances. No new property.
- **Provenance in the slices.** The 55 capability comments that described the axioms,
  and 14 process comments that cited them, carry a dated note. The standalone
  `bpo:X rdfs:subClassOf [realized in …]` statements are replaced by a dated comment.
- **ADR-001 R6** prescribed this pattern ("`realized in` the underlying acts"). It now
  has a dated amendment recording the decision, and `scripts/stage_section.py` no
  longer tells a slice author to assert the axiom.

Checked mechanically: each slice's new graph equals its old graph minus exactly the
197 restrictions (rdflib isomorphism). The wiring graph is unchanged (600 triples
before and after). Two duplicate lines appear in the file: the slice 2 and 12
declarations of `IntellectualPropertyManagementCapability` both receive its scope-table
pairs.

**Measured (full suite, 2026-11-03).** Gates A–D pass on all 13 slices; corpus ELK consistent; Gate F at baseline (39); C1–C7 0 violations; dispatch unchanged (30 routable / 167 gaps over 197). The inferred named-class hierarchy is identical: 4,553 subclass pairs before and after, none added or removed. The removal changes what the corpus claims about capability instances, not any classification.

**Not removed: 111 restrictions of the same form on 37 P-classes** (113 before decision
A; P11035 and P11036 had one each). These P-classes are themselves modelled as
capabilities, the Gate F capability-as-process backlog. What their restrictions become
depends on each class's assessment (`capability-as-process-backlog.md`).

**Text not changed: 53 capability definitions say the capability "is realized in"
acts of some kind.** Read literally, that is the same necessity claim in prose. They
are reported, not reworded: a reword (to "can be realized in") is for the architect to
decide.

## Open, for the architect

1. **The 111 restrictions on the backlog P-classes:** decided per class, with the
   backlog.
2. **The 53 definitions** that say "is realized in".
