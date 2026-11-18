---
id: BPO-BCO-2026-11-18-registry-after-wp6
from: BPO
to: BCO
date: 2026-11-18
type: notice
subject: "apqc-ext.ttl after WP6: three of your six genera have new text, no axiom changes; the CCO pin is now checked by digest"
in_reply_to: null
refs:
  - repo: Skreen5hot/BusinessProcessOntology
    commit: bc64e91839378e1926189c01bf184d6a22d5c1b7
    path: ontology/apqc-ext.ttl
    sha256: a8119728796872a1814aace8130a32cc8e42961b0bd5feaa28b736d60a0cc6fd
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2867cd4f727f5993c5893c3319f1e5f321a8cee8
    path: ontology/apqc-ext.ttl
    sha256: 504cee52be299e4c9103470e51c4fe8206d8372672241df69ddbff5a8281dc6a
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 2867cd4f727f5993c5893c3319f1e5f321a8cee8
    path: docs/migrations.tsv
    sha256: d96ebddcd50a625f9a67d6dfaf03ba3371784a167cfaefe0b5bb69e42fc40e5d
author: Claude (agent), drafted at the direction of Aaron Damiano, the BPO architect, under the architect's standing approval to answer messages
requires_act: false
---

BPO's WP6 corrections are now on `main`, by merge commit `2867cd4`. Your pin, `bc64e91`,
is unchanged and still resolves, so nothing breaks. This notice lets you re-pin when you
choose. The `bc64e91` copy of the registry is the first reference; the new one is the
second.

## Your six vendored genera

No axiom changed in any of them: no parent, and no class added or removed.

| Genus | What changed |
|---|---|
| `bpo:ActOfReporting` | **Definition** widened: a detailed account "of some subject matter, such as an organization's condition or results", where it was "of an organization's condition or results". The comment now separates disseminating reports (this genus) from compiling them (`cco:ont00000366`) |
| `bpo:ActOfAcquisition` | Comment only: adds why `cco:ont00001334` (Act of Purchasing) and `cco:ont00000389` (Act of Buying) were rejected |
| `bpo:ActOfRemuneration` | Comment only: says that payroll-tax remittances keep `bpo:ActOfFinancialTransaction` |
| `bpo:ActOfDevelopment`, `bpo:ActOfImprovement`, `bpo:ActOfOrganizationalEstablishment` | Unchanged |

## Elsewhere in the registry

- **`bpo:ActOfCommunication` is deprecated.** It is the same class as `cco:ont00000402`.
  It stays declared, with `owl:deprecated true` and `dct:isReplacedBy cco:ont00000402`,
  because you vendor this file. The change is recorded in `docs/migrations.tsv` (third
  reference).
- **`bpo:ActOfIdentification`** is relabelled "Act of Identification". Its sense moved
  from the label to a scope note.
- **Comments and definitions quote the labels of the pinned CCO release.** For example,
  `cco:ont00000908` is "Act of Artifact Processing", where the comments had "Act of
  Material Artifact Processing". The definitions of `bpo:ActOfProduction`,
  `bpo:ActOfForecasting` and `bpo:ActOfFinancialTransaction` changed with them.

## The CCO pin

BPO still pins CCO v2.0, 2024-11-06. BPO's gates now also check the vendored file's
digest:

- tag `v2.0-2024-11-06`, commit `510dad7`;
- sha256 `e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b`.

Before WP6, BPO had vendored a later development-branch file that carried the same version
IRI on relabelled content (965 was "Prescriptive ICE" there). If your extracts were taken
from that file, their CCO labels may differ from the release. The IRIs are the same.

## Also on `main` with this merge

- **The capability wiring changed** (WP6 B8). `capabilities_wiring.ttl` now asserts:
  - 343 `bpo:enablesProcess` pairs, where `bc64e91` had 356;
  - no `bpo:requiresCapability`, where `bc64e91` had 356;
  - 197 `bpo:requiresRole`, unchanged.

  A capability–process pair is no longer read as a requirement unless it is classified as
  one. The 197 `*Capability` classes no longer assert that they are realized in processes.
  The 37 capability-typed `bpo:P…` classes keep their restrictions until each is assessed.
- **Decision A and your Q12 questions** are covered separately, in the Q12 thread.

Nothing is expected of you.
