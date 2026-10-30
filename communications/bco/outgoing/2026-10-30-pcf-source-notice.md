---
id: BPO-BCO-2026-10-30-pcf-source-notice
from: BPO
to: BCO
date: 2026-10-30
type: notice
subject: BPO 2e55edd carries APQC's PCF notice (NOTICE.md); source PCF 7.4 material from BPO at this commit or later
in_reply_to: null
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2e55edd9e86a0bc20fa88a21595cc61402faa5dc
    path: NOTICE.md
    sha256: ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2e55edd9e86a0bc20fa88a21595cc61402faa5dc
    path: ontology/apqc-catalog.ttl
    sha256: 598faf6efa81ef6545cac04000c3d3834a9e8478f7619a3b8eed848a5b8d1547
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# BPO carries APQC's PCF notice; the PCF 7.4 source for the BCO

Aaron's change of direction on APQC PCF sourcing says the BCO takes PCF 7.4 material from
BPO, and that BPO would send this notice. It gives the commit to pin and the files to cite.

## The pinning commit

`2e55edd9e86a0bc20fa88a21595cc61402faa5dc` is the first BPO commit that meets the condition
of APQC's licence. Every BPO artifact that carries PCF content also carries APQC's notice:

- **`NOTICE.md`** separates BPO's MIT work from the PCF material, lists the files that carry
  PCF content, and reproduces APQC's notice verbatim from the PCF 7.4 workbook. Copy the
  notice text from this file, at this commit, and record the digest above.
- **`dct:rights`** on the ontology header of each PCF-bearing module states the notice:
  the catalog, the 13 slices and the reference module.
- **The BPO website** shows the notice in the footer of every page.
- **`scripts/notice_check.py`** fails BPO's corpus check if a module with PCF descriptions
  or hierarchy IDs lacks the notice, or if a module without PCF content claims it. It may
  serve as a model for the check the BCO needs.

## The source file

`ontology/apqc-catalog.ttl` holds all 1,921 PCF 7.4 elements: element ID, hierarchy ID,
name and description, each as a `skos:Concept`. It is the one file to vendor for PCF
material. If the BCO vendors it, BPO will send a notice whenever it changes, as for
`apqc-ext.ttl`, and will not rewrite the history that contains it.

## The existing pin

`apqc-ext.ttl` is unchanged since `dda9fa5` (SHA-256 `a8119728…6fd`, the digest of the
current pin). It carries no PCF content and so no notice. The pin at `bc64e91` needs no
action.

Nothing here requires a reply. Aaron's message asks the BCO to acknowledge once the new
pin is in place.
