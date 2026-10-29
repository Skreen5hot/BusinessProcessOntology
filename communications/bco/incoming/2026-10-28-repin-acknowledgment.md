---
id: BCO-BPO-2026-10-28-repin-acknowledgment
from: BCO
to: BPO
date: 2026-10-28
type: acknowledgment
subject: BCO re-pinned apqc-ext.ttl to v0.4.1 (bc64e91) under the https://fandaws.com/ontology/bpo# namespace
in_reply_to: BPO-BCO-2026-10-23-namespace-v0-4-0
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: ontology/apqc-ext.ttl
    sha256: a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 6731f591bc03622d630c87f5f6be91bce9b88651
    path: config/upstream-sources.yaml
    sha256: b3f52b7b8e0ff485cac0d90d656bc58d6ec517a275a490e674326b05dae97216
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
source:
  repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
  commit: d00c763437370f2dc60aaa7f91b35de37a60b4d2
  path: communications/bpo/outgoing/2026-10-28-repin-acknowledgment.md
  sha256: 67ca4413c6bb5c21235189de3a3a05251ad83bd5e38b434a91c98da320b19d3d
---
---
id: BCO-BPO-2026-10-28-repin-acknowledgment
from: BCO
to: BPO
date: 2026-10-28
type: acknowledgment
subject: BCO re-pinned apqc-ext.ttl to v0.4.1 (bc64e91) under the https://fandaws.com/ontology/bpo# namespace
in_reply_to: BPO-BCO-2026-10-23-namespace-v0-4-0
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: ontology/apqc-ext.ttl
    sha256: a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: LICENSE
    sha256: 2154e0221f7e5119b2d45842fcd4be421c11c5d64a459601f2c35f53710c487a
  - repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
    commit: 6731f591bc03622d630c87f5f6be91bce9b88651
    path: config/upstream-sources.yaml
    sha256: b3f52b7b8e0ff485cac0d90d656bc58d6ec517a275a490e674326b05dae97216
author: Claude Code (agent), drafted at Aaron Damiano's direction
requires_act: false
---

# BCO re-pinned apqc-ext.ttl to v0.4.1

Thank you for the v0.4.0 and v0.4.1 notices. The BCO has re-pinned its vendored extract of
`ontology/apqc-ext.ttl` from `6613194` to `bc64e91` (v0.4.1), merged in BCO commit
`6731f59`.

## What we checked

- At your re-pin target `327ea2c`, the file is graph-isomorphic to `6613194` under your
  base substitution (`http://example.org/apqc` to `https://fandaws.com/ontology/bpo`, which
  covers the ontology IRI as well), ignoring `owl:versionInfo`. This matches your notice.
- At `bc64e91` the file differs further only in `owl:versionInfo` and in 13 `rdfs:comment`
  literals, where your prose now writes `bpo:` for `ex:`. Three of those comments are on
  genera we vendor: Improvement, Organizational Establishment and Remuneration.
- No label, definition or `rdfs:subClassOf` axiom of the six genera we vendor changed.
- Your `LICENSE` is unchanged.

## What changed on our side

- The six genera are now referenced at `https://fandaws.com/ontology/bpo#<LocalName>`, local
  names unchanged. We assert no equivalence between the old and new IRIs.
- Our prefix label stays `ex:` for now. It is bound to your new namespace and used for your
  genera only. Renaming it to `bpo:` is planned for a later, separately reviewed revision
  on our side.
- `6613194` no longer needs to stay reachable for the vendored extract. Our capability
  inventory still records it, by digest, as its historical baseline, so we would still
  appreciate it staying reachable.

This closes the loop your v0.4.0 notice offered. Nothing here needs an answer.
