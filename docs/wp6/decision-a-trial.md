# WP6 decision A: P11035 and P11036 as acts, a trial

2026-11-02. Not applied: a trial on the working tree at `fb42d66`, measured and
reverted, for the architect's decision A.

## The finding

`bpo:P11035` ("Plan, build, and manage lender relations", PCF 12.1.1) is modelled as
an Organization Capability, a subclass of `bpo:LenderRelationsManagementCapability`,
and the two have the same definition word for word. The parent's comment says it
was "Minted for 12.1.1 (P11035)", when the Gate-F R5 review re-judged the row a
standing function. `bpo:P11036` (12.1.2, analyst relations) is the same. The
architect's reading: the APQC row names something *performed*, so the P-class
should be a process, with the capability kept as a separate class. Identical
definitions show the defect, and merging the two classes would hide it.

The same pattern covers the 12 other P-classes that B8 excluded as capability
targets, and Gate F's backlog of 39 "capability-as-process" findings.

## The trial model

For each of the two:

- **The P-class becomes an act.** It is a subclass of `bpo:ActOfRelationshipManagement`
  (an Act of Association, Planned Act), defined as the activity: "An Act of Relationship
  Management in which an organization plans, builds, and manages its relationships with
  bankers and lenders over time, …".
- **The bounded episodes become its parts.** `bpo:CultivateLenderRelations`, the
  supporting act minted for the cultivation episodes, is now a process part of it:
  `⊑ ∃ has process part (cco:ont00001777)`. It had been the realized-in filler of the
  P-class as a capability.
- **The capability class is unchanged.** `LenderRelationsManagementCapability` stays a
  Stakeholder Relationship Management Capability. Its relation to the act is B8's
  possible realization (`enablesProcess`, from the scope table). It is not an OWL axiom,
  so it makes no necessity claim.

## Results

| | At `fb42d66` | Trial |
|---|---|---|
| Gates A–D, slice 12 | pass | pass |
| Corpus ELK | consistent | consistent, no unsatisfiable classes |
| Gate F capability-as-process | 39 (baseline) | **37**: the two resolved; the gate fails until `BASELINE` is lowered deliberately |
| C1–C7 | 0 | 0 |
| B8 pairs | 342 possible, 14 excluded | 344 possible, 12 excluded |
| Matchability | 30 / 167 | 30 / 167 |

Entailed subclass pairs, before and after (direct pairs, ELK): exactly four change.

```
- bpo:P11035 ⊑ bpo:LenderRelationsManagementCapability
- bpo:P11036 ⊑ bpo:AnalystRelationsManagementCapability
+ bpo:P11035 ⊑ bpo:ActOfRelationshipManagement
+ bpo:P11036 ⊑ bpo:ActOfRelationshipManagement
```

## For the decision

1. **Adopt for P11035 and P11036?** If so, `BASELINE` in
   `scripts/refintegrity_check.py` goes from 39 to 37 in the same commit.
2. **Extend to the other 37?** Each needs its own check: some may really be standing
   functions that APQC names as activities, and some may lack a bounded episode class.
   This reverses the R5/R6 "standing function → capability" verdicts for these rows,
   so it is a methodology change (`apqc_to_bfo_cco_methodology.md` R5), not only a
   data fix.
3. **The episode classes.** `CultivateLenderRelations` / `CultivateAnalystRelations`
   become parts of the activity. An alternative is to merge them into it. The trial
   keeps them, because the episodes are bounded and the activity is not.
