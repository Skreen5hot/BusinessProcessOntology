---
id: BPO-BCO-2026-11-18-decision-a-on-main
from: BPO
to: BCO
date: 2026-11-18
type: notice
subject: "Q12 follow-up: decision A is on main; bpo:P11035 and bpo:P11036 are acts of relationship management"
in_reply_to: BPO-BCO-2026-11-17-q12-capability-typing-answer
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2867cd4f727f5993c5893c3319f1e5f321a8cee8
    path: ontology/slices/apqc_12_0.ttl
    sha256: 871d56a131e4c5ebf2410f312525d5dc5c199a4836a4081c1d933699d8fcc81a
author: Claude (agent), drafted at the direction of Aaron Damiano, the BPO architect, under the architect's standing approval to answer messages
requires_act: false
---

This is the notice our Q12 answer promised (`BPO-BCO-2026-11-17-q12-capability-typing-answer`,
§2).

**Decision A has reached `main`**, by merge commit `2867cd4`. There, `bpo:P11035` and
`bpo:P11036` are subclasses of `bpo:ActOfRelationshipManagement`, not Organization
Capabilities. Each no longer has a realized-in restriction. Their standing capacities stay
separate: `bpo:LenderRelationsManagementCapability` and
`bpo:AnalystRelationsManagementCapability`. The
reference is the slice, `ontology/slices/apqc_12_0.ttl`, at that commit.

**Nothing else in the Q12 answer changes:**

- The other 37 classes are still Organization Capabilities, an open backlog with no date.
- The eight classes your blocked concepts depend on (P10788, P10894, P10897, P10899,
  P10908, P10909, P10910, P16958) are unchanged.
- PCF 10735, 10736 and 14008 still have no act type.

Neither class appears among your dependencies, so you need not re-pin for this.
