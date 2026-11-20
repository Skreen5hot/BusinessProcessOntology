---
id: BPO-BCO-2026-11-20-backlog-decision-1
from: BPO
to: BCO
date: 2026-11-20
type: notice
subject: "Q12: the eight classes your blocked concepts depend on are now act types, on main"
in_reply_to: BPO-BCO-2026-11-17-q12-capability-typing-answer
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b8f4eb5fd2f4130f7fd4657585c691d5b493c132
    path: ontology/slices/apqc_9_0.ttl
    sha256: 963ff8306668df3b54147deeef08d7c9b386f71dbd42440fa78698a596bddea3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b8f4eb5fd2f4130f7fd4657585c691d5b493c132
    path: docs/wp6/backlog-assessment-1-treasury.md
    sha256: 1509516c3c384cb2419206c42754127979d8dc5a2f54979eabc02b2ee0394b24
author: Claude (agent), drafted at the direction of Aaron Damiano, the BPO architect, under the architect's standing approval to answer messages
requires_act: false
---

Derived in part from the APQC Process Classification Framework® 7.4 (element names and IDs,
under APQC's notice in BPO's `NOTICE.md`). APQC does not endorse this work.

This is the notice our Q12 answer promised when an assessment retypes a class
(`BPO-BCO-2026-11-17-q12-capability-typing-answer`, "What this means for you").

## What changed

The BPO architect assessed the eight classes first, because your blocked concepts depend on
them. On 2026-11-20 the architect decided that all eight are **act types**. The change is on
`main` at `b8f4eb5`. The decision is BPO's "backlog decision 1", and the assessment and
its reasoning are the second reference. Each class is now under an act genus, not under
`cco:ont00000568`:

| Class | PCF element | Genus now |
|---|---|---|
| `bpo:P10788` | 9.1.4.7 Manage continuous cost improvement | `bpo:ActOfImprovement` |
| `bpo:P10894` | 9.7.2.2 Manage cash equivalents | `bpo:ActOfFinancialTransaction` |
| `bpo:P10897` | 9.7.2.5 Manage cash flows | `bpo:ActOfScheduling` |
| `bpo:P10899` | 9.7.2.7 Manage and oversee banking relationships | `bpo:ActOfRelationshipManagement` |
| `bpo:P10908` | 9.7.4.2 Manage financial intermediary relationships | `bpo:ActOfRelationshipManagement` |
| `bpo:P10909` | 9.7.4.3 Manage liquidity | `bpo:ActOfFinancialTransaction` |
| `bpo:P10910` | 9.7.4.4 Manage issuer exposure | `bpo:ActOfMonitoring` |
| `bpo:P16958` | 9.7.6 Manage financial fraud/dispute cases | `bpo:ActOfResolution` |

**Also changed:**

- Each class has a new definition under its genus. Its earlier comment is kept as history.
- `bpo:P10788` has the APQC name again; its label had been "Continuous Cost Improvement
  Capability". Its realized-in restriction to `bpo:P10741` is gone.
- Slice 9 now inlines four more genera from `apqc-ext.ttl`: Relationship Management,
  Resolution, Improvement and Scheduling. The registry itself did not change.

**What stays the same:**

- The IRIs, `bpo:pcfID`, `bpo:hierarchyID` and the catalog bridges
  (`bpo:designatesProcessType`).
- None of the eight had capability wiring, so `capabilities_wiring.ttl` is unchanged.
- The other 29 classes of the backlog are still Organization Capabilities. So are PCF
  10735, 10736 and 14008.

## For your concepts

Your eight blocked concepts now have act evidence at `b8f4eb5`. Re-pinning and the G1-T
admission review are yours.
