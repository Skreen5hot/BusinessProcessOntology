---
id: BPOT-BPO-2026-10-30-phase-b-decisions
from: BPOT
to: BPO
date: 2026-10-30
type: request
subject: WP6 Phase B waits on BPO's decisions; which are made, and at which BPO commit?
in_reply_to: null
refs:
  - repo: Skreen5hot/BPO-Template-Port
    commit: 68f22125f5075f67e6179ae447876b9f8d496fd1
    path: research/template-evaluation.md
    sha256: 9b8264334b8361deedca4e2678ab80ad1abf66a9756e2f1cdc6575f5579ae72f
  - repo: Skreen5hot/BPO-Template-Port
    commit: 513b8da6526782773f98ebbd24a9b9edbfb6f09b
    path: research/wp6/classification.md
    sha256: 4ec98d472b2e0794c0ad3cc72f4ae0d8c4426e52b39a7f99c3e0b2423a4a6b6f
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: NOTICE.md
    sha256: ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: docs/adr/ADR-003-pcf-licensing-posture.md
    sha256: 1202b654f045b36d95970d6a9f30e3c8a8db327f2176ebfc2834ccb6b3209cfb
author: Claude (agent), drafted at the direction of Aaron Damiano, the BPO architect and PO
requires_act: true
source:
  repo: Skreen5hot/BPO-Template-Port
  commit: 5d234e0f54a8a27c957da7e80d9cb74961de0833
  path: communications/bpo/outgoing/2026-10-30-phase-b-decisions.md
  sha256: 592e99e6b91657de6b09b7ef1b3f9723bc2700290eefd216ebc675b093b21c59
---
---
id: BPOT-BPO-2026-10-30-phase-b-decisions
from: BPOT
to: BPO
date: 2026-10-30
type: request
subject: WP6 Phase B waits on BPO's decisions; which are made, and at which BPO commit?
in_reply_to: null
refs:
  - repo: Skreen5hot/BPO-Template-Port
    commit: 68f22125f5075f67e6179ae447876b9f8d496fd1
    path: research/template-evaluation.md
    sha256: 9b8264334b8361deedca4e2678ab80ad1abf66a9756e2f1cdc6575f5579ae72f
  - repo: Skreen5hot/BPO-Template-Port
    commit: 513b8da6526782773f98ebbd24a9b9edbfb6f09b
    path: research/wp6/classification.md
    sha256: 4ec98d472b2e0794c0ad3cc72f4ae0d8c4426e52b39a7f99c3e0b2423a4a6b6f
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: NOTICE.md
    sha256: ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: docs/adr/ADR-003-pcf-licensing-posture.md
    sha256: 1202b654f045b36d95970d6a9f30e3c8a8db327f2176ebfc2834ccb6b3209cfb
author: Claude (agent), drafted at the direction of Aaron Damiano, the BPO architect and PO
requires_act: true
---

## What we are asking

WP6 Phase A, our evaluation of the Ontology Template on BPO, is done. Phase B measures **S2**:
BPO with its own corrections made, ported again, and compared with S0 (BPO as ported
unchanged, from `bc64e91`). The template's verdict on whether it improves BPO itself comes
only from S2.

S2 cannot be built until BPO has decided the items below. Several may already be settled,
so for each one please tell us:

1. **Decided?** Give the decision, with its ADR or commit, or say "not yet".
2. **Made in BPO?** Give the BPO commit, or say "decided not to change".

Then name **the BPO commit S2 is to be ported from.** Partial answers are welcome: we can
prepare S2 item by item, but we measure it only once, from that one commit.

Counts are from Phase A, as measured by template v0.1.0 at S0. The classes (K01–K17) are in
`research/wp6/classification.md` (second reference), approved by the BPO architect on
2026-10-30. "Status" is what we read in BPO at `b3b7ff3`, today's `main`.

## 1. Probably resolved: please confirm

| Item | What it was | Status at `b3b7ff3` | To confirm |
|---|---|---|---|
| **B2** | APQC text redistributed under MIT, with no APQC notice | **Looks resolved.** `2e55edd` puts APQC's notice in NOTICE.md (third reference), puts `dct:rights` on all 15 PCF-bearing modules, adds it to the site footer and adds `notice_check.py`. ADR-003 (fourth reference) settles the posture | That B2 is closed. If it is, the port must carry the notice too. That is our work for S2: the port tool, our NOTICE and site, and declaring the APQC text in `config/third-party-text.yaml`. It closes our gaps G1 and G2 |

## 2. Decisions only the architect can make

| Item | Finding | At S0 | Status | Decision needed |
|---|---|---:|---|---|
| **B1** | One shared class reads differently depending on which slice is loaded | 51 definitions, 6 labels (violations); 53 comments (K09, K10, K08) | Open: no ontology change since `bc64e91` | One definition and one label per class. For comments, choose one canonical text or deliberate per-module notes. **The highest-severity item** |
| **B4** | `P10530_SuggestionProgram`: a non-PCF class with a PCF-style IRI and an underscore | 1 (K16) | Open | Rename it to a readable non-PCF IRI, recording the replacement, or keep it as an accepted exception |
| **B7** | `bearsPermission` says a role *bears* a permission, but CCO's Action Permission is a Directive ICE | no check finds it (G4) | Open | Whether to relabel (we proposed `permissionApplicableToRole`), with a deprecation row if so |
| **B8** | `enablesProcess` means "can enable", but `requiresCapability` is derived from it | no check finds it (G4) | Open | Audit `capabilities/capability_scope.json`: does each of the 361 pairs mean *required*? If not, split "can enable" from "requires" |
| **B9** | A definition's genus is not its asserted parent | 233 (145 of them disappear with B13; see K03, K04, K05) | Open | Align each definition's genus with its parent, or re-parent the class. P20799 "an act of design…" ⊑ Act of Formulation is the clearest case |
| **B10** | Editorial notes in labels: "(shared anchor)", "(discernment sense)", "(capability)", … | 9 (K12) | Open | Move them to `skos:altLabel` or a comment, or keep them. The 9 labels that are APQC's own element names (K17) need nothing |
| **B11** | Organizations placed where CCO requires an Agent (CCO 2.0: Organization ⊄ Agent) | 5 (K13) | Known in BPO and documented in CLAUDE.md; no recorded decision | Record BPO's pattern for organizations acting as agents under CCO 2.0, as a decision |
| **B13** | Co-asserted second parents that are redundant once CCO is in scope | 216 redundant (K06), plus 8 genuine (K07) | Open: by design, for offline SHACL | Does standalone-slice validation still need them? If not, remove the redundant ones. Separately, the 8 we classified **unsure** (K07) need your call: 7 delivery-fleet roles sit under the `FNSR Role` marker *and* under Occupation or Authority Role, and IT Infrastructure Component sits under both IT Asset and Information Processing Artifact |
| **B14** | No class cites the source of its definition | 3,119 (K01) | Open | Map BPO's provenance (`pcfID`, the APQC source text, or a citation) to CCO's definition-source annotation, or decide the rule does not apply to BPO. Turning it off is then a recorded decision |
| **B16** | Comments still cite the old `bpo:` CURIEs | no check finds it (G5) | Unclear: ADR-002 made `bpo:` the label again, so these citations may now be correct | Confirm that no change is needed |
| **B18** | BPO's header titles, version and design notes are not carried into the port | — | Open | Decide whether they belong in the ported headers |

## 3. Already done in the port: back-port to BPO?

The PO approved these four changes on 2026-10-26, and the port applies them. BPO itself
still lacks them at `b3b7ff3`. We need to know whether S2 is ported from a BPO that has them,
or whether the port keeps applying them.

| Item | Change | In BPO at `b3b7ff3` | Note |
|---|---|---|---|
| **B3** | Name the PCF release (7.4) on every slice header | No. Slice 5 names no source; slice 1 names the framework but not the release | — |
| **B5** | `skos:definition` on all 10 BPO properties | No | — |
| **B6** | Re-type `requiresCapability`/`Role`/`Permission` from object properties to annotation properties (563 class-to-class assertions, K02) | No: still `owl:ObjectProperty` | Check the effect on BPO's SHACL C5–C7 first; they assume object properties |
| **B12** | A top concept for the PCF concept scheme | No (0 `skos:hasTopConcept`) | — |

## Not needed for Phase B

- **B15**, the 39 capabilities with process IRIs. That is BPO's tracked backlog (Gate F), and
  v0.1.0 now reproduces it exactly.
- **The CCO pin.** v2.2 has been out since 2026-08-14. BPO stays on v2.0 by its own decision,
  shared with the BCO. S2 is measured on the same pin as S0 and S1.

## Why we ask before porting

The classification of S0's findings is fixed (amendment A6), so S2 is judged by real defects
removed and none introduced. A decision we do not know about would look like either a
regression or an unexplained fix. We would rather ask than guess.
