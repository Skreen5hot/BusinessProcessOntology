# Phase 0 — Corpus Setup & Section Daemon

**Status:** Plan (ready to execute)
**Scope:** Stand up the repository, fix the corpus-wide meta-decisions, generate the deterministic catalog layer, and build a daemon that iterates the **13 top-level APQC sections**, producing one validated reality-layer ontology module per section.
**Governing decisions:** Methodology v1.1.0 (`apqc_to_bfo_cco_methodology.md`) as amended by **ADR-001** (`docs/adr/ADR-001-category-and-upper-level-modeling.md`), which supersedes the binary D8.

---

## 1. What Phase 0 delivers

Per Methodology §5 *Phase 0 — Meta-decisions (once per corpus)*, plus ADR-001's **build order**:

| # | Deliverable | Kind | Status gate |
|---|---|---|---|
| 0.1 | Repo skeleton, pinned config, vendored CCO closure | setup | — |
| 0.2 | `ontology/apqc-catalog.ttl` — every PCF row as a catalog node (ADR-001 R1) | **deterministic, generated** | Gate A + catalog SHACL |
| 0.3 | `ontology/apqc-ext.ttl` — shared local act genera (D9) | curated seed | Gate A/B |
| 0.4 | Validation harness — Gates A–D, scriptable | tooling | self-test on `apqc_1_1_1.ttl` |
| 0.5 | **Section daemon** — iterates the 13 sections, spawns one LLM transform agent per section, validates output | tooling | end-to-end dry-run + 1 live section |

Phase 0 is *complete* when: the catalog covers 100% of PCF rows and passes its shapes; the harness reproduces the reference module's clean A–D result; and the daemon transforms at least one section end-to-end through the gates.

---

## 2. The two-layer architecture (ADR-001)

This is the load-bearing decision and it shapes every artifact.

```
┌─────────────────────────────────────────────────────────────┐
│ CATALOG LAYER  (apqc-catalog.ttl)                            │
│   • EVERY PCF row, all 1,921 nodes, 5 levels                 │
│   • each node: cco:Descriptive-ICE + skos:Concept            │
│   • ex:pcfID, ex:hierarchyID, ex:apqcSourceText, prefLabel   │
│   • dotted hierarchy → skos:broader  (CURATORIAL, not parts) │
│   • generated deterministically; zero ontological judgement  │
└───────────────┬─────────────────────────────────────────────┘
                │  ex:designatesProcessType   (annotation bridge, R4)
                ▼
┌─────────────────────────────────────────────────────────────┐
│ REALITY LAYER  (apqc_<section>.ttl, one per section)         │
│   • ONLY nodes passing the bounded-occurrent test (R5)       │
│   • owl:Class ⊑ a CCO Act ; cco:has process part mereology   │
│   • inputs/outputs as ICEs (Phase 3 necessity rule)          │
│   • standing-function categories → Organization Capability   │
│     (cco:ont00000568) via R6                                 │
│   • genus from act-type layer in apqc-ext.ttl (D9)           │
└─────────────────────────────────────────────────────────────┘
```

**Why this and not Policy A/B:** the 13 sections are not a uniform ontological kind — some are operating-process families, some are standing management functions. A uniform "categories are processes" mistypes the latter; "ignore categories" loses them. The catalog gives total coverage cheaply and deterministically; the expensive judgement-bearing work accrues only where R5 warrants it. See ADR-001 §Rationale.

**Layer separation (R7) is enforced, not advisory:** `skos:broader` appears only in the catalog; `cco:has process part` and `rdfs:subClassOf`-to-an-Act appear only in the reality layer. Three new SHACL shapes (S9–S11) enforce this.

---

## 3. Corpus-wide meta-decisions (fixed here, recorded in every module header)

| Decision | Value fixed for the corpus |
|---|---|
| **D7** IRI minting | Primary class IRI = `ex:P<pcfID>` (stable PCF ID). Human-readable label via `rdfs:label`. Hierarchy ID stored only as positional annotation. |
| **D8** Category policy | **Superseded by ADR-001** two-layer policy (catalog + selective reality layer). |
| **D9** Shared extension | `ontology/apqc-ext.ttl`, imported by every slice. Seeds: `ex:ActOfAnalysis`, `ex:ActOfIdentification` (from reference module); grows as recurring genera are discovered. |
| **§6** Upper anchor | CCO Act classes: Information Processing `ont00000366`, Appraisal `ont00000636`, Planning `ont00000511`, Planned Act `ont00000228`. Verify-before-assert per term. |
| **CCO pin** | CommonCoreOntologies **Merged v2.0 (2024-11-06)**, vendored under `vendor/cco/` for Gate B offline determinism. |
| **Namespace** | `ex: <http://example.org/apqc#>` (matches reference; swap to a real base before publication). |

---

## 4. Repository layout

```
BusinessProcessOntology/
├── PHASE0.md                         ← this plan
├── README.md                         ← updated: architecture + quickstart
├── apqc_to_bfo_cco_methodology.md    ← spec (unchanged)
├── docs/
│   └── adr/
│       └── ADR-001-category-and-upper-level-modeling.md
├── ontology/
│   ├── apqc-catalog.ttl              ← 0.2  GENERATED (do not hand-edit)
│   ├── apqc-ext.ttl                  ← 0.3  shared act genera (D9)
│   ├── apqc_shapes.ttl               ← existing + new S9–S11
│   ├── apqc_bad_examples.ttl         ← existing + layer-mixing fixtures
│   ├── slices/
│   │   └── apqc_1_1_1.ttl            ← existing reference module
│   └── reports/                      ← validation output (gitignored)
├── prompts/
│   └── slice_transform_prompt.md     ← methodology distilled for the agent
├── src/apqc_transform/
│   ├── config.py                     ← pins, prefixes, paths, IRI scheme
│   ├── pcf_export.py                 ← xlsx → typed PCF rows (stdlib only)
│   ├── catalog.py                    ← R1 deterministic catalog emitter
│   ├── validate.py                   ← Gates A–D harness
│   ├── agent_runner.py               ← per-section LLM transform (Claude Agent SDK)
│   └── daemon.py                     ← iterate 13 sections, orchestrate, report
├── vendor/cco/                       ← pinned CCO+BFO closure (Gate B)
├── tests/
├── requirements.txt
└── .gitignore
```

> **Note on existing files.** The current root-level `apqc_1_1_1.ttl`, `apqc_shapes.ttl`, `apqc_bad_examples.ttl` move under `ontology/`. This is a one-time `git mv` so history is preserved; the plan keeps them runnable from the new paths.

---

## 5. The section daemon (deliverable 0.5)

**Runtime:** Python. **Per-section transform:** an LLM agent (Claude Agent SDK) that executes the methodology pipeline. The daemon is the deterministic orchestrator; the judgement lives in the agent.

### 5.1 Control loop (`daemon.py`)

```
load PCF export  →  load catalog (provenance source of truth)
for section in SECTIONS (1.0 … 13.0):          # 13 iterations
    if state[section] == DONE and not --force:  continue          # idempotent/resumable
    rows         = pcf_export.subtree(section)                    # all descendants
    seed_ext     = read apqc-ext.ttl                              # shared genera (D9)
    module_ttl   = agent_runner.transform(section, rows, seed_ext, prompt, catalog)
    write ontology/slices/apqc_<section>.ttl
    report       = validate.gates(module_ttl, closure=vendor/cco) # A–D
    if report.failed_mandatory:
        if attempts < N:  feed report back to agent_runner; retry # self-repair loop
        else:             mark NEEDS_REVIEW; continue
    record evidence (hashes, CCO pin, gate results) in reports/
    state[section] = DONE
emit corpus roll-up report
```

Design properties:
- **Idempotent & resumable** — section state persisted in `ontology/reports/state.json`; a crash or kill resumes where it stopped. (This is the "daemon" character: long-running, restartable, one unit of work per section.)
- **Self-repair** — a failed mandatory gate (A–D) is fed back to the agent as structured feedback for up to *N* retries before the section is parked as `NEEDS_REVIEW`. Never releases a non-conformant module.
- **Bounded & observable** — one section at a time by default (`--concurrency` opt-in); every run writes an evidence record (input hash, CCO pin, per-gate result) for hash-chained audit (Methodology §11).
- **Shared-extension growth is serialized** — if an agent proposes a new recurring genus for `apqc-ext.ttl`, it is surfaced for human approval, not auto-merged, to prevent duplicate universals (D9).

### 5.2 Per-section agent (`agent_runner.py`)

Each agent receives: the section's PCF rows (with catalog IRIs), `apqc-ext.ttl`, the verified CCO term table (§6), and `prompts/slice_transform_prompt.md` (the methodology Phases 1–7 distilled into an operating procedure). It returns a Turtle module. It does **not** touch the catalog (that layer is deterministic and frozen). Gate F (human semantic review) remains a human step after the daemon — A–D cannot judge anchor correctness (Methodology §9 *Limit*).

### 5.3 What Phase 0 builds vs. defers

- **Build now:** orchestrator, state/resume, validation wiring, evidence records, the prompt, and a working end-to-end run on **one** section (default 1.0, the reference's territory).
- **Defer to Phase 1+:** running all 13 sections to release quality, Gate E competency questions, Gate F review workflow, and the bridge-population (`ex:designatesProcessType`) reconciliation pass between catalog and reality layers.

---

## 6. Validation harness (deliverable 0.4)

Per Methodology §9 / §11, scripted and offline-deterministic:

| Gate | Tool | Check |
|---|---|---|
| **A** Syntax | `rdflib` parse | module is valid Turtle |
| **B** IRI resolution | local closure under `vendor/cco/` | every `cco:`/`obo:` IRI resolves to a declared term — **no live web** |
| **C** SHACL | `pyshacl -a` | `apqc_shapes.ttl` → zero violations; warnings dispositioned |
| **D** Reasoner | **ELK via ROBOT** (`tools/robot.jar`, Java) | merge module + closure, reason; consistent, no unsatisfiable classes; thin classes inspected |

Plus the regression fixture: `apqc_bad_examples.ttl` **must** keep producing its expected violation count (a drop = a shape silently stopped firing). Phase 0 adds layer-mixing bad examples for S9–S11.

**Self-test:** the harness is "done" when it reproduces the reference module's known-clean A–D result and the fixture's known violation count.

---

## 7. SHACL additions for the two-layer model (S9–S11)

Extending `apqc_shapes.ttl` per ADR-001 §Consequences:

- **S9** — a catalog node (`skos:Concept` / Descriptive-ICE in the catalog) **MUST NOT** bear `cco:has process part`.
- **S10** — a reality-layer process **MUST NOT** use `skos:broader`.
- **S11** — an `ex:designatesProcessType` target **MUST** be a process universal or a capability class.

Existing S1–S8 are unchanged and still apply to reality-layer modules.

---

## 8. Execution order (tasks)

1. **Repo skeleton** — dirs, `requirements.txt`, `.gitignore`, `git mv` existing ttl into `ontology/`, README refresh. Record ADR-001.
2. **PCF export reader** (`pcf_export.py`) — xlsx → typed rows (id, hierarchy, level, name, description, parent), stdlib-only for reproducibility.
3. **Catalog generator** (`catalog.py`) — emit `apqc-catalog.ttl` (R1); assert 100% row coverage; pass Gate A + S9.
4. **Shared extension seed** (`apqc-ext.ttl`) + `config.py` pins.
5. **Validation harness** (`validate.py`) — Gates A–D; self-test against the reference module and fixture.
6. **SHACL S9–S11** + layer-mixing bad examples.
7. **Daemon + agent runner** (`daemon.py`, `agent_runner.py`, prompt) — dry-run all 13, live-run section 1.0 through the gates.

Tasks 1–4 are deterministic and judgement-free (safe to fully automate). Task 7 is where the LLM transform enters; everything it produces is gated.

---

## 9. Open items / risks

- **CCO closure acquisition** — ✅ **done.** `vendor/cco/CommonCoreOntologiesMerged.ttl` (v2.0, 2024-11-06) is vendored locally (1.9 MB, gitignored). Gate B resolves all module IRIs against it.
- **Reasoner** — ✅ **done.** Gate D runs **ELK via ROBOT** (`tools/robot.jar` 1.9.10, Java 23). Verified live: reference module + catalog are consistent with no unsatisfiable classes; the bad-examples fixture reports 3 unsatisfiable classes. All four gates A–D are operational.
- **Bridge population** — `ex:designatesProcessType` linking catalog↔reality is defined in Phase 0 but only populated as reality modules land; full reconciliation is a Phase 1 pass.
- **Namespace** — `ex:` example base is a placeholder; choose a publishable base IRI before any external release.
```
