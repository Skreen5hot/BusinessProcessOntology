---
id: BPO-BCO-2026-11-17-q12-capability-typing-answer
from: BPO
to: BCO
date: 2026-11-17
type: answer
subject: "Q12: the 39 are capabilities at bc64e91, by design; 2 are now acts on an unmerged branch; 37 and the three PCF elements are an open backlog, not intended act types"
in_reply_to: BCO-BPO-2026-11-15-q12-capability-typing-inquiry
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: docs/adr/ADR-001-category-and-upper-level-modeling.md
    sha256: 79edfb0d4a1528d593f9c66ddd619c60b8c97fe17e55d429e78989458f7f2bd2
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2b86c91800336044f7ca4e5c21459245fe54a8ee
    path: docs/wp6/capability-as-process-backlog.md
    sha256: 56fe941bac9e581a4e24f4495302981df93f3140977fbf426eacf805592f3f96
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2b86c91800336044f7ca4e5c21459245fe54a8ee
    path: docs/wp6/capability-as-process-backlog.tsv
    sha256: 52225d97255233835314ec5fbc7a627b8c105ac3a1c393654343b5becb2ea14a
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2b86c91800336044f7ca4e5c21459245fe54a8ee
    path: docs/wp6/decision-a-trial.md
    sha256: c54ad42070aae7300fc61ed709c5b1cc5e5f2e21785bb2d53bf0fa6ba4a4767f
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2b86c91800336044f7ca4e5c21459245fe54a8ee
    path: ontology/slices/apqc_12_0.ttl
    sha256: 871d56a131e4c5ebf2410f312525d5dc5c199a4836a4081c1d933699d8fcc81a
author: Claude (agent), drafted at the direction of Aaron Damiano, the BPO architect, under the architect's standing approval to answer messages
requires_act: false
---

Derived in part from the APQC Process Classification Framework® 7.4 (element names and IDs,
under APQC's notice in BPO's `NOTICE.md`). APQC does not endorse this work.

Your reading is right. Every answer below reports a decision BPO's architect has already
recorded, with the reference that records it. This message makes no new decision.

## 1. Are the 39 intended as capabilities?

**At `bc64e91`, yes, all 39.** They are capabilities by ADR-001's R5 and R6, as their
comments say (first reference).

**That reading is now under review, and two classes have changed.** BPO's WP6 review
found that R5 asks two questions at once:

- does the row name a bounded occurrent?
- is what it names performed (an act), or borne (a capability)?

An ongoing programme of activity is still a process, even with no natural end. On
2026-11-03 the architect decided (second reference):

- **`bpo:P11035` and `bpo:P11036` are acts** (decision A, fourth reference).
- **The other 37 are an explicit backlog** of unresolved classification candidates, "not
  37 incorrect classes". Each needs its own assessment. Until then, R5 and R6 stand as
  written, and the 37 stay capabilities.

Your 39 are exactly our 37 (third reference) plus those two.

**No date is set for the assessments.** BPO lists them as a recommendation for its next
cycle. ADR-001 will be amended from the results, as a separate decision.

## 2. Which act genus, for those intended as acts?

- **`bpo:P11035` and `bpo:P11036`:** `bpo:ActOfRelationshipManagement` (fifth reference).
- **The 37:** none is assigned. Any of them may become an act or stay a capability, so
  we name no genus in advance, just as you assume none.

**Where it stands.** Decision A is BPO commit `da2e573`, on branch `wp6-s2-corrections`
(head `2b86c91`). That branch is not merged to `main` and is held unmerged for now. Please
do not pin to it. We will send a `notice` when the change reaches `main`. Neither class
appears in your list of BCO dependencies.

## 3. Are act types intended for PCF 10735, 10736 and 14008?

**Not at present.** All three were routed by the same R5 reading:

- 10735 (9.8) and 10736 (9.9) designate `bpo:InternalControlCapability` and
  `bpo:TaxManagementCapability`.
- 14008 (9.2.4.7) is modelled only by `bpo:DefaultAccountManagementCapability`. That class
  deliberately carries no `bpo:pcfID`; its comment says so.

None is in the 37-class backlog, because none uses its own `bpo:P<id>` IRI. They raise the
same R5 question, though. Your message, now in BPO's record, puts them before the R5/R6
amendment alongside the 37.

## What this means for you

- **Today:** the 37, and the three elements, are capabilities, as intended. You can keep
  the dependent concepts blocked, as you planned.
- **The eight blocked concepts.** Their only act evidence is P10788, P10894, P10897,
  P10899, P10908, P10909, P10910 and P16958. Your message is now in BPO's record, and it
  will be cited when those rows are assessed.
- **Nothing will change in BPO on the BCO's account.** If an assessment retypes a class,
  you will get a `notice` with the commit, as for any change to a class you depend on.
