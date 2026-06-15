# Vendored tool — RefIntegrity Linter (Gate F)

The `ex:`/`perf:` referential-integrity + D7 scheme linter, vendored so Gate F runs offline and
reproducibly (same discipline as the pinned CCO closure and `tools/robot.jar`).

- **Source:** `https://github.com/Skreen5hot/IRI_Linter`
- **Commit:** `725cc92524c977666a8bb1f13bfb40e61e483a5f` ("RefIntegrity R1.1 FR-12: scheme rules gate on owl:Class")
- **License:** MIT (see the upstream `LICENSE`).
- **Implements:** `FNSR-RefIntegrity-Linter-Spec-R1.1.md` (in the BPO repo root) — Modules 1–2
  (`collect` + `resolve` + CLI, dangling-reference core) and the Module-3 R1.1 scheme checks
  (`capability-as-process`, `pcf-without-P-iri`, gated on `owl:Class` per FR-12). `readable_label`
  (FR-11) fires only with `--register` and is not used by Gate F.

## Files
- `src/ri-cli.mjs`, `src/ri-collect.mjs`, `src/ri-resolve.mjs` — the linter (copied verbatim from `src/`).
- `vendor/n3.mjs` + `vendor/PROVENANCE.md` — the pinned N3.js parser (SHA-256 in that file; ADR-008 upstream).

## Run
```
node tools/refintegrity/src/ri-cli.mjs --modules <corpus .ttl files…>
```
Used by `scripts/refintegrity_check.py` (Gate F), which asserts the FR-18 baseline over the corpus.
Requires `node` on PATH (Gate F SKIPs gracefully if absent, like Gates B/D without their closure/jar).

## Re-sync
When upstream updates: re-copy `src/ri-*.mjs` + `vendor/n3.mjs` from the named commit, update the
**Commit** line above, and re-run `scripts/refintegrity_check.py` to confirm the baseline still holds
(or update `scripts/refintegrity_check.py`'s `BASELINE` deliberately if the expected counts changed).
