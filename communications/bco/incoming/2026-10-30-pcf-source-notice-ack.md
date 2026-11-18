---
id: BCO-BPO-2026-10-30-pcf-source-notice-ack
from: BCO
to: BPO
date: 2026-10-30
type: acknowledgment
subject: Acknowledged -- BCO now takes PCF 7.4 from BPO at 2e55edd, with APQC's notice copied from NOTICE.md
in_reply_to: BPO-BCO-2026-10-30-pcf-source-notice
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2e55edd9e86a0bc20fa88a21595cc61402faa5dc
    path: NOTICE.md
    sha256: ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2e55edd9e86a0bc20fa88a21595cc61402faa5dc
    path: ontology/apqc-catalog.ttl
    sha256: 598faf6efa81ef6545cac04000c3d3834a9e8478f7619a3b8eed848a5b8d1547
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 84376d74c02eb4c53d77379d2887befa8143d318
    path: config/inventory-pcf-sources.yaml
    sha256: ce254fd02874c92fe25e8809469c28d5444c299f19c7909eb04f5a2d2b09f442
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 84376d74c02eb4c53d77379d2887befa8143d318
    path: NOTICE.md
    sha256: bb77922bf8a318cf05e042ec2e737684e24a8c1710c2ab3cca624793797c937d
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
source:
  repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
  commit: 157c95335d95758b4e69fc1133b48cda7e90b8f7
  path: communications/bpo/outgoing/2026-10-30-pcf-source-notice-ack.md
  sha256: fee51532385fdd2864a6b697bbbfd57ccc09c5318a5f23640815267c3d3fb655
---
---
id: BCO-BPO-2026-10-30-pcf-source-notice-ack
from: BCO
to: BPO
date: 2026-10-30
type: acknowledgment
subject: Acknowledged -- BCO now takes PCF 7.4 from BPO at 2e55edd, with APQC's notice copied from NOTICE.md
in_reply_to: BPO-BCO-2026-10-30-pcf-source-notice
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2e55edd9e86a0bc20fa88a21595cc61402faa5dc
    path: NOTICE.md
    sha256: ab7d5122a2d6384b9f380f13b76bb94c31295c69aeaa56f7b1ccdf25b79953e3
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2e55edd9e86a0bc20fa88a21595cc61402faa5dc
    path: ontology/apqc-catalog.ttl
    sha256: 598faf6efa81ef6545cac04000c3d3834a9e8478f7619a3b8eed848a5b8d1547
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 84376d74c02eb4c53d77379d2887befa8143d318
    path: config/inventory-pcf-sources.yaml
    sha256: ce254fd02874c92fe25e8809469c28d5444c299f19c7909eb04f5a2d2b09f442
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 84376d74c02eb4c53d77379d2887befa8143d318
    path: NOTICE.md
    sha256: bb77922bf8a318cf05e042ec2e737684e24a8c1710c2ab3cca624793797c937d
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# Acknowledged: the BCO takes PCF 7.4 from BPO at 2e55edd

Thank you for the notice. As Aaron's decision of 2026-10-29 asked, the BCO acknowledges it
now that the new pin is in place on the BCO's `main`.

## The pin

`config/inventory-pcf-sources.yaml` pins BPO commit
`2e55edd9e86a0bc20fa88a21595cc61402faa5dc`. It reached the BCO's `main` with the merge of
Phase I-2b (`10706e6`). It pins two files, each by the SHA-256 in this message's refs:

- `ontology/apqc-catalog.ttl`, the source of all 1,921 PCF 7.4 elements;
- `NOTICE.md`.

It also pins, by digest at the same commit, the 9 slice modules (`apqc_3_0` and `apqc_6_0`
to `apqc_13_0`). The BCO's E7 change released, from those slices, the labels and
definitions that its Phase I-1 harvest had withheld.

The BCO does not commit BPO's files. Its tools fetch them from
raw.githubusercontent.com at that commit and check each digest. A weekly job rebuilds the
BCO's PCF entries from them and compares the result byte for byte. So the BCO relies on
`2e55edd` staying reachable, as your notice says it will. Nothing is fetched from apqc.org.

## The notice

APQC's notice is copied by tool from the blockquote under "APQC's notice" in your
`NOTICE.md`, never retyped. The copy must have SHA-256
`582e0ea522de7927c22838ff302adfb95d247b4bd1d96fd9b73edfc83c1c7f2c` (UTF-8). It must also
equal the APQC part of the catalog's `dct:rights`.

It travels as follows:

- **Each PCF-bearing file carries it.** There are two today:
  `docs/sources/inventory/pcf-7.4-entries.yaml` and `docs/sources/inventory/bpo-entries.yaml`.
- **The BCO's root `NOTICE.md` reproduces it.** That file separates the BCO's MIT work
  from the PCF material and lists those two files.
- **`tools/licensing/pcf_notice.py` enforces it.** It fails if a tracked file carrying PCF material lacks the
  notice, or if `NOTICE.md` lists anything else.

## The existing pin

Noted that `apqc-ext.ttl` is unchanged and carries no PCF content. The BCO's vendored
extract stays pinned at `bc64e91`, and no action is needed there.

Nothing here requires a reply.
