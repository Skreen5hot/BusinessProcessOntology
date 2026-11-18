# WP6: the CCO dependency brought back to its pin

2026-11-02. A dependency change, recorded on its own as the architect asked
(decisions of 2026-11-02). The Template Team pins CCO v2.0-2024-11-06 for the
port, and the architect approved the same pin for BPO, with verification.

## What was wrong

BPO declared CommonCoreOntologiesMerged v2.0, **2024-11-06** (`config.py`,
`vendor/cco/README.md`, CLAUDE.md), but the file in `vendor/cco/` (fetched
2026-06-02) was the **2026-04-04** release (version IRI
`https://www.commoncoreontologies.org/2026-04-04/CommonCoreOntologiesMerged`,
sha256 `0daf9173…`). Nothing compared the two, so every Gate B/D run and every
D6 check since June used 2026-04-04.

## The pinned file

| | |
|---|---|
| Release tag | `v2.0-2024-11-06` (resolves to commit `510dad76be0ef710b65a421075af912af25342b7`) |
| File | `src/cco-merged/CommonCoreOntologiesMerged.ttl` at that commit |
| sha256 | `e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b` |
| Version IRI | `https://www.commoncoreontologies.org/2024-11-06/CommonCoreOntologiesMerged` |

It is byte-identical to the port's `.upstream-cache/cco.ttl`, which the port
pins by the same commit and digest (`config/upstream-sources.yaml`).

## Why the version IRI alone is not enough

CCO's `develop` branch relabelled `cco:ont00000965` from "Directive Information
Content Entity" to "Prescriptive Information Content Entity" on 2025-06-02
(commit `d67f032`), but its module files kept declaring the 2024-11-06 version
IRI until 2026-04-07 (`a051575`). So a file from that window says "Prescriptive"
under a 2024-11-06 version IRI. Checked in the module
`src/cco-modules/InformationEntityOntology.ttl`:

| Commit | Date | Version IRI | 965 label |
|---|---|---|---|
| `510dad7` (the release tag) | 2024-11-06 | 2024-11-06 | Directive Information Content Entity |
| `161d5c1` | 2025-03-18 | 2024-11-06 | Directive Information Content Entity |
| `d67f032` | 2025-06-02 | 2024-11-06 | **Prescriptive** Information Content Entity |
| `01efddb` | 2026-03-29 | 2024-11-06 | Prescriptive Information Content Entity |
| `a051575` | 2026-04-07 | 2026-04-04 | Prescriptive Information Content Entity |

The released file is the tagged commit's, and in it 965 is "Directive" (altLabel
"Directive ICE"); the word "Prescriptive" does not occur. Hence the check below
tests the digest as well as the version IRI.

## The check

`apqc_transform.validate.cco_pin_problem()` requires `vendor/cco/` to hold
exactly `CommonCoreOntologiesMerged.ttl`, with the pinned sha256 and version IRI
(`config.CCO_FILE`, `CCO_SHA256`, `CCO_VERSION_IRI`, `CCO_COMMIT`). Gate B fails
otherwise, and `corpus_check.sh` stops before ELK. Tested: it passes the pinned
file and refuses the 2026-04-04 file (digest mismatch).

## Effect on BPO

- **Entailments.** At `103405b`, the merged corpus reasoned with ELK under each
  release: no inferred subclass pair with a `bpo:` class differs. All 474 pairs that
  differ (253 only under 2026-04-04, 221 only under 2024-11-06) are between CCO's
  own classes.
- **Gates under the pin, at `0daf297`:** A–D pass on all 13 slices; corpus ELK
  consistent with no unsatisfiable classes; C1–C7 0 violations; matchability
  64 / 389 (unchanged); consistency audit 11 (unchanged).
- **Text.** BPO's sources had taken CCO labels and definitions from the
  2026-04-04 file: "Act of Material Artifact Processing" for `908` (2024-11-06:
  "Act of Artifact Processing"), one comment quoting `965` as "Prescriptive",
  and "verified" definitions of `908` and `950` (`apqc-ext.ttl`, slices 4, 8 and
  10) and of `970`, `051` and `595` (methodology §6) in their 2026 wording.
  Corrected in the next commit; IRIs and axioms unchanged.
- **One anchor to review.** `bpo:P12721` ("Ship hazardous material") is under
  `595` Act of Cargo Transportation, justified by the 2026 definition ("some
  Payload is moved"). The pinned definition is narrower: "the movement of
  manufactured goods through some Transportation Agent". Left for the architect.

## For the WP6 record

The port's Phase A register correction "965 = Prescriptive ICE" rested on the
2026-04-04 file. Under the pin, 965 is "Directive Information Content Entity".
