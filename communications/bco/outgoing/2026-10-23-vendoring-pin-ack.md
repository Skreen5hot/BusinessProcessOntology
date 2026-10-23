---
id: BPO-BCO-2026-10-23-vendoring-pin-ack
from: BPO
to: BCO
date: 2026-10-23
type: acknowledgment
subject: Acknowledged -- 6613194 stays reachable; BPO will give notice before history, CCO or genus changes, and is moving to fandaws.com
in_reply_to: BCO-BPO-2026-10-23-vendoring-pin
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: ontology/apqc-ext.ttl
    sha256: 1b9a9375cb7303003556004effd712b63913d6aa4935dbf604a653aec65cab4b
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# Acknowledged: 6613194 stays reachable

BPO has read the pin and checked it from this side:

| Check | Result |
|---|---|
| `6613194` is `66131945b525c54f44e4962f32bb1f52dfa0cd12` | yes; it is the tip of `origin/main` today |
| `git show 6613194:ontology/apqc-ext.ttl` | SHA-256 `1b9a9375…ab4b`, matches your pin |
| `git show 6613194:LICENSE` | SHA-256 `2154e022…487a`, matches your pin |
| The 6 act genera are declared in that file | all 6 (`ex:ActOfAcquisition`, `…Development`, `…Improvement`, `…OrganizationalEstablishment`, `…Remuneration`, `…Reporting`) |
| No `dcterms:license` in BPO Turtle | correct; none in `ontology/` or its slices |

## What BPO commits to

- **`6613194` stays reachable.** BPO commits straight to `main` and does not force-push
  it. If a history rewrite ever becomes necessary, BPO will send a `notice` here first.
- **CCO stays at v2.0 (2024-11-06)** for now. A move to another release will be sent as a
  `notice` before it lands.
- **Changes to the 6 vendored genera** will also be sent as a `notice`, so the BCO can
  re-pin, even though they don't break the pin.

## On the information items

- **Licence.** Adding `dcterms:license` to the module headers is reasonable, and BPO may do
  it later. Until then, reading `LICENSE` at the pinned commit is the right source.
- **Namespace: BPO is moving to `fandaws.com`.** BPO has decided to move every IRI it
  owns off `http://example.org/apqc`: the `ex:` terms, the `…/apqc/scheme#` D7 scheme and
  the slice ontology IRIs. The proposed home is `https://fandaws.com/ontology/bpo#`,
  alongside the BCO's `…/bco#`. The move changes every BPO IRI the BCO references, so it
  will come here first as its own message: the exact IRIs, the old-to-new mapping, and the
  commit that lands it, so the BCO can re-pin and rewrite its references in one step.
  Until then the `6613194` pin and its `example.org` IRIs stay valid. That commit stays
  reachable after the move.
- **Capability classes (BCO spec v0.4 §2).** BPO agrees nothing moves without a
  conversation here. For that conversation, the BPO side has two parts: the slices'
  Organization Capabilities (`⊑ cco:ont00000568`, including 39 that still carry `ex:P<id>`
  IRIs, a tracked backlog), and the merge-only capability/role overlay
  (`ontology/capabilities_*.ttl`), which no slice imports.
- **Unvendored slices.** Agreed. Vendoring the reality-layer slices or the catalog for
  the realization index would add pins. Please send it as a `request`, so BPO can say
  which files are stable enough to pin.
