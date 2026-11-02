# Vendored CCO dependency closure (Gate B / Gate D)

This directory holds the **pinned** Common Core Ontologies closure that Gates B
(IRI resolution) and D (reasoner) validate against. It is **not committed** (see
`.gitignore`) because the files are large; fetch them with the pin below.

## Pin

- **CommonCoreOntologies Merged v2.0** — release date **2024-11-06**
- Version IRI: `https://www.commoncoreontologies.org/2024-11-06/CommonCoreOntologiesMerged`
- Includes BFO 2020 via CCO's import.
- Tag `v2.0-2024-11-06` = commit `510dad76be0ef710b65a421075af912af25342b7`; the file is
  <https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/510dad76be0ef710b65a421075af912af25342b7/src/cco-merged/CommonCoreOntologiesMerged.ttl>
- sha256 `e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b`. Gate B refuses any
  other file (`config.CCO_SHA256`); a later develop snapshot can carry this version IRI.

## How to populate

Download the Merged release for the pinned date and place the Turtle/OWL file(s)
here, e.g. `CommonCoreOntologiesMerged.ttl`. Source:
<https://github.com/CommonCoreOntology/CommonCoreOntologies> (releases / tags).

Once present:
- `validate.gate_b_iri_resolution` resolves every `cco:`/`obo:` IRI used by a
  module against the declared terms in this closure.
- `validate.gate_d_reasoner` can run ELK/HermiT over module + closure.

Until populated, Gates B and D report **SKIP** (not FAIL), so the Phase 0
harness self-test stays green offline. See `PHASE0.md` §9.
