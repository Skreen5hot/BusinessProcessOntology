# Direction — BPO Namespace

**Architectural Decision Record ADR-002**
**Status:** Accepted (2026-10-23) · **Release:** v0.4.0 · **Cites:** `BPO-BCO-2026-10-23-vendoring-pin-ack`
(`communications/bco/outgoing/`), which announced the decision to the BCO.

---

## Decision

Every IRI BPO owns moves off the `http://example.org/apqc` placeholder, a domain reserved for
documentation (RFC 2606), to **`https://fandaws.com/ontology/bpo`**. That puts it alongside the
BCO's `https://fandaws.com/ontology/bco#`.

The move is **one base substitution** applied to every BPO IRI, with nothing else changed:

| Old | New |
|---|---|
| `http://example.org/apqc#X` (the `ex:` terms) | `https://fandaws.com/ontology/bpo#X` |
| `http://example.org/apqc/scheme#X` (`apqc:`, the PCF concept scheme) | `https://fandaws.com/ontology/bpo/scheme#X` |
| `http://example.org/apqc/shapes#X` | `https://fandaws.com/ontology/bpo/shapes#X` |
| `http://example.org/apqc/perf#X` (`perf:`, not yet populated) | `https://fandaws.com/ontology/bpo/perf#X` |
| `http://example.org/apqc/slice/N.0`, `/ext`, `/scheme`, `/capabilities`, `/capabilities/wiring`, `/delivery` (ontology IRIs) | the same paths under `https://fandaws.com/ontology/bpo/` |
| `http://example.org/apqc` (reference module's ontology IRI) | `https://fandaws.com/ontology/bpo` |

Local names are unchanged, so `ex:P10020` keeps its PCF-ID-derived local name (D7).

## Rules

**N1 — The prefix label stays `ex:` for now.** Only the namespace it abbreviates changes, so no
Turtle body, judgment table, index row or document that uses `ex:` CURIEs needs editing.
Renaming the label to `bpo:` is wanted, and will be a separate, purely cosmetic phase.

**N2 — The old base never comes back.** `scripts/corpus_check.sh` fails if
`example.org/apqc` appears in any tracked file under `ontology/`, `src/`, `scripts/`, `tools/` or
`qa/`. Historical text is exempt: sent messages in `communications/` never change, and
`FNSR-RefIntegrity-Linter-Spec-R1.1.md` is another team's versioned spec.

**N3 — Published history is not rewritten.** Commits before v0.4.0 (including `6613194`, which
the BCO pins) stay reachable with their `example.org` IRIs. A consumer moves by re-pinning and
applying the table above.

## Consequences

- Every module's `owl:versionInfo` is `0.4.0`.
- The vendored RefIntegrity linter (`tools/refintegrity/`) hard-codes the local namespaces, so it
  carries a local patch, recorded in its `PROVENANCE.md`. Upstream (`Skreen5hot/IRI_Linter`) is
  not changed from here.
- Dereferencing (serving the ontology at these IRIs from fandaws.com) is separate work. The IRIs
  are names first.

## Verification (at the migration commit)

- For each of the 22 tracked `.ttl` files, the pre-move graph with the base rewritten (in IRIs and
  in SHACL SPARQL literals) is isomorphic to the post-move graph, ignoring `owl:versionInfo`.
- The generators reproduce their outputs byte for byte (`assemble_wiring.py` →
  `capabilities_wiring.ttl`, `catalog` → `apqc-catalog.ttl`), and `corpus_index.tsv` is unchanged.
- Gates A–D on all 13 slices, C1–C7, matchability, corpus ELK and Gate F give the same results as
  before the move.
