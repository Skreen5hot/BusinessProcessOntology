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

## Open, for the architect

1. **The slice axioms (B8 step 1).** `C ⊑ ∃ realized in P` says every instance of C
   *is* realized in some P, which is a necessity claim about a realizable entity that may
   never be realized. B8 removed the derived requirement but left these 197 axioms in
   the slices. The change record set this aside as a separate modelling question.
2. **The 5 directly authored requirements** in `delivery_processes.ttl`: should the
   same evidence rule apply?
3. **The 14 excluded pairs** wait on decision A.
