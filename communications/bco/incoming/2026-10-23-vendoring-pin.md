---
id: BCO-BPO-2026-10-23-vendoring-pin
from: BCO
to: BPO
date: 2026-10-23
type: request
subject: BCO now vendors apqc-ext.ttl at 6613194 -- please keep that commit reachable
in_reply_to: null
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: ontology/apqc-ext.ttl
    sha256: 1b9a9375cb7303003556004effd712b63913d6aa4935dbf604a653aec65cab4b
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 3d43724170db5199dde6243e2a6beae306083ec7
    path: config/upstream-sources.yaml
    sha256: e9c00d8e123a6619ae4bc07429684ed254983da00a314648a8b4d17be458000d
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
source:
  repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
  commit: ba953ce738f6e6751183e878b6c2f06779574044
  path: communications/bpo/outgoing/2026-10-23-vendoring-pin.md
  sha256: 645c25b524d121ed0931c7f8a898b8f4ab5de2c5a89732f7de60a688c74089a1
---
---
id: BCO-BPO-2026-10-23-vendoring-pin
from: BCO
to: BPO
date: 2026-10-23
type: request
subject: BCO now vendors apqc-ext.ttl at 6613194 -- please keep that commit reachable
in_reply_to: null
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: ontology/apqc-ext.ttl
    sha256: 1b9a9375cb7303003556004effd712b63913d6aa4935dbf604a653aec65cab4b
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 3d43724170db5199dde6243e2a6beae306083ec7
    path: config/upstream-sources.yaml
    sha256: e9c00d8e123a6619ae4bc07429684ed254983da00a314648a8b4d17be458000d
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# BCO now vendors apqc-ext.ttl at 6613194

The Business Capability Ontology takes its act types from BPO. As of BCO commit
`3d43724`, it vendors a pinned partial extract of BPO's `ontology/apqc-ext.ttl`:

| | |
|---|---|
| BPO commit | `66131945b525c54f44e4962f32bb1f52dfa0cd12` (`main` on 2026-10-23) |
| File | `ontology/apqc-ext.ttl`, SHA-256 `1b9a9375…ab4b` |
| Terms taken | the 6 act genera the BCO specification names — Act of Acquisition, Development, Improvement, Organizational Establishment, Remuneration, Reporting — and their CCO/BFO ancestry |
| Extract | `vendor/bpo/bpo-ext-bco-extract.ttl` in the BCO repository |

## What we are asking

**Please keep commit `6613194` reachable.** The pin names that commit in a raw URL and
records the file's digest. A weekly job in the BCO repository re-fetches it and requires
the bytes to match. A force-push or history rewrite on BPO that drops the commit would fail
that job. That failure would be correct, but it would land without explanation. If BPO
needs to rewrite history, a note here first lets the BCO re-pin in the same week.

An acknowledgment is enough to close this.

## For BPO's information, nothing asked

- **Licence.** BPO's Turtle files carry no `dcterms:license`, so the BCO's vendoring tool
  reads the MIT grant from BPO's `LICENSE` at the same commit, which is digest-checked like
  the ontology itself. If the BPO module headers ever gain a `dcterms:license`, the BCO
  can read it from the artifact directly. That is a nicety, not a request.
- **CCO pin.** The BCO pins CCO v2.0 (2024-11-06, commit `510dad76`) because BPO's act
  genera were anchored against v2.0. A BPO move to another CCO release is something the
  BCO would want to hear about, since its extracts would then disagree with BPO's anchors.
- **Namespace.** BPO's `http://example.org/apqc#` is under a domain reserved for
  documentation. The BCO references BPO terms by those IRIs, but authors its own terms in
  a provisional namespace of its own (`https://fandaws.com/ontology/bco#`, pending the
  BCO's RP-5). It does not mint anything in BPO's namespace.
- **Capability classes.** BCO specification v0.4 §2 proposes moving BPO's capability
  classes out of the slices into a BCO module. That proposal is not ratified, and nothing
  will move without a conversation here first.

## Not covered

Only `apqc-ext.ttl` is vendored. BPO's reality-layer slices, catalog and
`capabilities_*.ttl` are not, so the BPO process classes the BCO specification names
(`ex:P10020` and others) resolve to nothing in the BCO repository today. Vendoring them is
likely to come up when the BCO's realization index is written, and would add further pins
on BPO files.
