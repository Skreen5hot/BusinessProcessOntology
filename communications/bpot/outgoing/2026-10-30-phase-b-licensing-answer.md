---
id: BPO-BPOT-2026-10-30-phase-b-licensing-answer
from: BPO
to: BPOT
date: 2026-10-30
type: answer
subject: B2 is closed (ADR-003, 2e55edd); what the port must carry; the other Phase B decisions are not yet made
in_reply_to: BPOT-BPO-2026-10-30-phase-b-decisions
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: docs/adr/ADR-003-pcf-licensing-posture.md
    sha256: 1202b654f045b36d95970d6a9f30e3c8a8db327f2176ebfc2834ccb6b3209cfb
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: NOTICE.md
    sha256: ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: src/apqc_transform/config.py
    sha256: 19a90985b5ec523b93a80c18e3fe43db4c5ef085cc6078cd421f4b1e36e6f942
  - repo: Skreen5hot/BusinessProcessOntology
    commit: b3b7ff3587c0a677a33a946882259571e9b4fc6e
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# Phase B: the licensing answer (B2), and where the rest stands

## B2: closed

- **Decided:** yes. ADR-003, accepted 2026-10-30, commit `b3b7ff3`.
- **Made in BPO:** yes. Commit `2e55edd` adds `NOTICE.md`, `dct:rights` on all 15
  PCF-bearing modules, the site footer and `scripts/notice_check.py`.

**Who decided.** The BPO architect, as architect. BPO has no Legal function and is not
waiting on one. ADR-003 records the architect's reading of APQC's texts and acceptance of
the residual risk, so on BPO's side B2 is no longer "pending Legal". The Template Team's
own question to its Legal about what the template's licensing report may say
(`EXAMPLE-LEGAL-2026-10-28-t9-third-party-text`) is theirs, and this does not answer it.

**What is under APQC's licence.** PCF element IDs, hierarchy IDs, element names and element
descriptions, wherever they appear: `bpo:pcfID`, `bpo:hierarchyID`, `bpo:apqcSourceText`,
the labels that are APQC's element names, the corpus index, and the PCF IDs inside local
names (`P<id>`, `PCF_<id>`). Everything else in BPO is MIT (`LICENSE`).

## What the port must carry

APQC's condition applies to every copy and every derivative work, so it applies to the port,
private or not.

1. **A NOTICE file** that separates the port's MIT work from the PCF material, lists the
   files carrying it, and reproduces APQC's notice verbatim. Copy the notice from BPO's
   `NOTICE.md` at `b3b7ff3`; don't retype it. Record its digest.
2. **`dcterms:rights` on every PCF-bearing module**, with BPO's text: `PCF_RIGHTS` in
   `src/apqc_transform/config.py`, which is also the `dct:rights` literal on each BPO module.
   The simplest way is for `port_from_bpo.py` to carry that triple through unchanged. The text
   points to "this repository's MIT licence (see NOTICE.md)", which reads correctly in the
   port as long as the port has both files. Its `LICENSE` is already MIT with the same
   copyright holder.
3. **The notice in the footer of every site page** that shows PCF text, if the site is
   published.
4. **No suggestion of endorsement.** Process Classification Framework® and PCF are APQC's
   marks, used only to identify the source.
5. **No access to apqc.org.** Take PCF material from BPO only, as `port_from_bpo.py` already
   does. APQC's website Terms forbid automated access.

**Values for `config/third-party-text.yaml`**, which the template leaves to "whoever advises
you on licensing":

| Field | Value |
|---|---|
| source | APQC Process Classification Framework® (PCF), Cross-Industry |
| release | 7.4 |
| licence | The licence in APQC's notice: perpetual, worldwide, royalty-free, to use, copy, publish, modify and create derivative works, provided every copy and derivative work contains the notice |
| attribution | APQC's notice, verbatim, from BPO's `NOTICE.md` |

`bpo:apqcSourceText` is the property that carries APQC passages. `bpo:pcfID` and
`bpo:hierarchyID` carry APQC identifiers. Whether the port declares `rdfs:label` too is the
port's call: some BPO labels are APQC's element names and some are BPO's own.

**`dcterms:source` is not complete in BPO yet.** The template also wants each module to name
the source and release in `dcterms:source`. At `b3b7ff3`, 13 of the 15 PCF-bearing modules
have one (slices 5 and 6 have none), and only the catalog names release 7.4. The release is
named in `dct:rights` on all 15. Completing `dct:source` is B3, below.

**History.** S0 and S1 were ported from `bc64e91`, before the notice. BPO does not rewrite
its own history before `2e55edd` (ADR-002 N3), and does not ask you to rewrite yours. Carry
the notice from S2 on.

## The other items: not yet decided

The architect has not yet decided B1, B4, B7, B8, B9, B10, B11, B13, B14 or B18, nor
whether to back-port B3, B5, B6 or B12. None of them is made in BPO at `b3b7ff3`.

**B16** needs no change in BPO. BPO's comments cite `bpo:` CURIEs, and `bpo:` has been BPO's
prefix since v0.4.1 (`dda9fa5`), before `bc64e91`. In the port those terms are `bpot:`, so
whether to rewrite the citations is the port's decision.

## The S2 commit

Not named yet. It will be `b3b7ff3` or later, so S2 carries the notice. A later message in
reply to your request will give the remaining decisions and name the commit.
