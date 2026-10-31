# WP6 B11: what the five Organization-as-Agent cases entail

2026-10-31. The architect's B11 decision: document the pattern, never assert
Organization ⊑ Agent, and accept the five cases as upstream-constraint exceptions
only after documenting their actual entailments. This is that documentation. It
records evidence; it does not accept the cases.

## Method

The merged corpus (13 slices, `apqc-ext.ttl`, the catalog, the capability layer
and wiring) was reasoned with ELK (ROBOT, `SubClass EquivalentClass`, indirect
pairs included), at commit `103405b`. The run was made twice: once with the CCO
file BPO vendors, and once with the 2024-11-06 release BPO declares as its pin.
They differ (see "CCO release" below). The B11 results are the same under both.

## The cases and their entailments

| Case | Axiom | CCO constraint | Entailed for the class |
|---|---|---|---|
| `bpo:ServiceProvider` (s5) | ⊑ Organization ⊓ ∃ has capability (`1954`).ServiceDeliveryCapability | `1954` domain Agent (`1017`) | **ServiceProvider ⊑ Agent** |
| `bpo:SupplyChainOrganization` (s4) | ⊑ Organization ⊓ ∃ has capability.SupplyChainManagementCapability | `1954` domain Agent | **SupplyChainOrganization ⊑ Agent** |
| P11042, P11043 (s12) | ⊑ ∃ has recipient (`1922`).BoardOfDirectors | `1922` range Agent | nothing for `bpo:BoardOfDirectors` |
| P19596 (s11) | ⊑ ∃ has recipient.RegulatoryAuthority | `1922` range Agent | nothing for `bpo:RegulatoryAuthority` |

Why they differ: a domain applies to the class that has the restriction, so a
class required to *have* a capability is entailed to be an Agent. A range on an
existential filler applies only to the filler individuals: each act's recipient
is a BoardOfDirectors that is also an Agent, which is satisfiable, but
BoardOfDirectors itself is not made a subclass of Agent.

Full ancestors of `bpo:ServiceProvider` (both releases): Organization, Group of
Agents, object aggregate, **Agent**, material entity, independent continuant,
continuant, entity.

`cco:Organization` (`1180`) itself is not entailed to be an Agent, and neither is
any other Organization subclass (checked: ITServiceProvider, Supplier,
BoardOfDirectors, RegulatoryAuthority).

## Consistency

No class is unsatisfiable under either release. The two classes become
Organization ⊓ Agent, which nothing in the closure forbids: Agent (`1017`) is a
subclass of material entity only, not of object, and the closure (both releases)
declares no disjointness among material entity's subclasses. Its only
disjointness axioms are between the top-level BFO partitions (material vs
immaterial entity; independent, specifically and generically dependent
continuant; the region, boundary and process partitions). The tension is between the
modelling intent (an organization is a group of agents, not an agent) and two
inferred subclass axioms. It is not a logical inconsistency.

## The same pattern in text only (found in the B9 review)

Six role classes are defined as "borne by an Organization" (or "by an
authority") and are anchored in the wiring overlay under Authority Role (`187`),
whose CCO definition says it "inheres in an Agent": BoardOfDirectorsRole,
CertificationAuthorityRole, GovernmentBodyRole, QuasiGovernmentBodyRole,
RegulatorRole, RegulatoryAuthorityRole. No axiom states the bearer, so nothing is
entailed. The four under Contractor Role (`506`) have no such tension: CCO's
definition admits "an Agent or Group of Agents".

## For the decision

- The two has-capability cases make a class-level claim that BPO's own pattern
  rejects (organization as agent). The alternative recorded in the change record
  is to restrict on a member agent of the organization, which changes BPO's
  meaning.
- The three has-recipient cases make no class-level claim.
- The six Authority Role definitions conflict with CCO's text, not its axioms.

## CCO release

BPO declares CCO v2.0 **2024-11-06** (`config.py`, `vendor/cco/README.md`, CLAUDE.md).
The file in `vendor/cco/` (fetched 2026-06-02) has version IRI
`https://www.commoncoreontologies.org/2026-04-04/CommonCoreOntologiesMerged`.
Nothing checks the version, so BPO's gates and D6 checks have run against
2026-04-04. Of the 76 CCO terms BPO uses, 21 differ between the two releases:
for example, `908` is labelled "Act of Artifact Processing" in 2024-11-06, and
`965` is "Directive Information Content Entity" there, not "Prescriptive". In
2026-04-04, `has agent` (`1833`) gains domain Process and range Agent, and
`has sender`/`has recipient` gain domain Act of Communication. None of this
changes the B11 entailments above.
