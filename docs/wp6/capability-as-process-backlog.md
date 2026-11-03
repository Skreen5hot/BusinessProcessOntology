# WP6: the capability-as-process backlog, and the R5/R6 methodology issue

2026-11-03. Registered on the BPO architect's decision of 2026-11-03 (§2): after
decision A repaired P11035 and P11036, the remaining Gate F capability-as-process
findings are **an explicit backlog of unresolved classification candidates, not 37
incorrect classes**. Nothing here changes the ontology.

## The backlog

`capability-as-process-backlog.tsv`, one row per class: the 37 `bpo:P<id>` classes
modelled as Organization Capabilities (`cco:ont00000568`). Gate F's baseline is 37
(39 until 2026-11-03).

Each needs its own assessment: does the APQC row name an **activity** that is
performed, whose standing capacity is a separate capability (the P11035 case), or a
**standing function** correctly modelled as a capability? Some may be standing
functions that APQC names with an activity verb.

The `triage` column reads the label only, to order the work. It is not a verdict:

| Triage | Classes |
|---|---|
| "Manage …": either reading | 29 |
| the label names a performed activity (Create, Monitor, Execute, Build, Ensure, Protect) | 6 |
| the label names a capability, not the APQC activity (P10728, P10788) | 2 |

**Related axioms.** The 37 carry 111 `realized in` (`obo:BFO_0000054`) restrictions of
the form `C ⊑ ∃ realized in P`. They are the same necessity claim that B8 step 1
removed from the 197 `*Capability` classes (2026-11-03), but they were left in place:
each class's assessment decides what they become. If the class is an act, the
restriction goes, as it did for P11035/P11036. If it is a capability, the
restriction is removed as for the 197, unless independent evidence supports it.

## The methodology issue (R5/R6)

ADR-001's R5 sends a node that "denotes a standing function or capacity (no natural
end; realized in recurring episodes)" to the catalog only, adding a capability per R6.
R6 models the capability as a class under Organization Capability (`568`). R6 does not
say which IRI the capability takes. In practice, for these 39 rows it took the row's
own `bpo:P<id>` IRI, so a row that APQC lists as a process element became a
capability. P11035 showed the consequence: two classes, the P-class and its
capability twin, with word-for-word the same definition.

The finding is that R5 conflates two questions:

1. Does the row name a bounded occurrent, or an activity with no natural end?
2. Is what the row names performed (an activity), or borne (a capability)?

An activity with no natural end, such as a programme of relationship management, is
still a process. Its standing capacity is a separate continuant. Decision A applied
that reading to two rows.

**Proposed handling.** No silent reinterpretation of the other rows. An amendment to
ADR-001's R5/R6 is to be proposed separately, based on the per-class assessments
of the 37, and decided by the architect. Until then, R5/R6 stand as written, and the
backlog is tracked by Gate F's baseline.

This is a limitation of BPO's mapping method that the experiment exposed: Gate F
counted the cases, and the WP6 review of B8's excluded pairs showed what they were.
