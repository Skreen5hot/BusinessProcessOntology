# Direction — PCF Licensing Posture

**Architectural Decision Record ADR-003**
**Status:** Accepted (2026-10-30) · **Release:** none (no ontology change) · **Cites:**
`BPO-BCO-2026-10-30-pcf-source-notice` (`communications/bco/outgoing/`), which gave the BCO
the commit to source PCF material from. Implemented by commit `2e55edd` (`NOTICE.md`).

---

## Context

BPO is built on the APQC Process Classification Framework® (PCF), Cross-Industry, version
7.4. It carries the PCF's element IDs, hierarchy IDs, names and descriptions in the catalog,
the 13 slices, the reference module, the corpus index and the website, and its IRIs carry
PCF element IDs.

Two APQC texts bear on that use:

- **The PCF's own notice**, on the Copyright and attribution sheet of the workbook. It grants
  a perpetual, worldwide, royalty-free licence to use, copy, publish, modify and create
  derivative works of the PCF. Its one condition is that every copy and every derivative
  work contains a copy of the notice.
- **APQC's website Terms of Service** (July 2026). Among other things, they restrict using
  site content to create, train or test AI systems, and forbid automated access to the
  site.

The BCO's rights review (I-2a) recorded the relation between the two as ambiguous. It drafted
a request to APQC for clarification, naming BPO, and withheld publishing PCF material
until APQC answered.

## Decision

As architect, Aaron Damiano takes the following position and accepts its residual risk:

1. **The PCF notice governs BPO's use of the PCF.** The licence it grants is the licence BPO
   relies on. The website Terms do not narrow what the notice permits for the PCF itself.
2. **BPO is not an AI system within the Terms' AI clause.** Developing an ontology with an AI
   coding assistant, or modelling what software agents are able to do, is not creating,
   training or testing an AI system. No reasonable computer scientist would read it so.
3. **BPO does not ask APQC for clarification.** The licence already in hand covers what BPO
   does, and asking could narrow it. Work cannot wait on an answer that may not come.

This is the architect's reading of APQC's texts, not legal advice. It is recorded so that
later work builds on it rather than reopening it.

## Rules

**L1 — The notice travels with every copy and derivative work.**
- `NOTICE.md` separates BPO's MIT work from the PCF material, lists where the PCF material
  is, and reproduces the notice verbatim from the workbook.
- Every module that carries PCF content states `config.PCF_RIGHTS` as `dct:rights` on its
  ontology header.
- The website shows the notice in the footer of every page (`scripts/site_notice.py`).
- `scripts/notice_check.py`, run by `corpus_check.sh`, enforces this. It fails when a module
  with PCF descriptions or hierarchy IDs lacks the notice, and when a module without PCF
  content claims it.

**L2 — The MIT licence does not cover PCF material.** `LICENSE` covers BPO's own work, and
`NOTICE.md` says where it stops.

**L3 — No endorsement is implied.** BPO says it is independent of APQC. Process
Classification Framework® and PCF are APQC's marks, used only to identify the source.

**L4 — No automated access to apqc.org.** Nothing in this repository fetches from APQC's
website, by script or in CI. PCF releases are obtained by hand.

**L5 — Downstream consumers source PCF material from BPO.** The BCO takes PCF 7.4 material
from BPO at `2e55edd` or later, and carries the notice in what it publishes. BPO tells the BCO
when a vendored PCF-bearing file changes, and does not rewrite history that contains one
(as ADR-002 N3 does for `apqc-ext.ttl`).

**L6 — PCF 8.0 waits for a planned upgrade.** BPO stays on 7.4 until an upgrade is planned.
Before adopting a new edition, read the notice in its workbook. If that notice differs from
7.4's, this decision is revisited before any of the edition's content enters the
repository.

## Alternatives rejected

- **Ask APQC to clarify (BCO decision APQC-2).** This would risk the licence already held,
  for no gain if the answer agrees with it. It also leaves work waiting on people outside the
  project.
- **Cite the PCF without its content (BCO decision APQC-1).** This would gut the catalog
  layer, which ADR-001 makes a lossless index of the framework.

## Consequences

- No ontology content changed. Each of the 15 PCF-bearing graphs gained one `dct:rights`
  triple. `owl:versionInfo` stays `0.4.1`.
- `apqc-ext.ttl` carries no PCF content and no notice, so the BCO's pin of it is unaffected.
- The residual risk is the architect's. It is mentioned again only when something new bears
  on it, such as a different notice in a new edition (L6).
