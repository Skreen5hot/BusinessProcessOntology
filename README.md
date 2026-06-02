# BusinessProcessOntology

An ontology of business processes derived from the **APQC Process Classification
Framework (PCF)**, transformed into **BFO 2020 / CCO 2.0**–conformant OWL.

## Architecture (two layers — ADR-001)

| Layer | Artifact | What it is |
|---|---|---|
| **Catalog** | `ontology/apqc-catalog.ttl` | Every PCF row (all 1,921 nodes) as a `skos:Concept` + Descriptive ICE; dotted hierarchy as `skos:broader`. **Generated deterministically**, total coverage, no ontological judgement. |
| **Reality** | `ontology/slices/apqc_<section>.ttl` | Genuine BFO process universals, minted only where a node passes the *bounded-occurrent test*. Built per section, carries the modeling judgement, validated by gates. |
| **Shared ext.** | `ontology/apqc-ext.ttl` | Recurring local act genera (D9), imported by every slice. |

The layers are linked by the `ex:designatesProcessType` bridge and kept strictly
separate. See [`docs/adr/ADR-001-category-and-upper-level-modeling.md`](docs/adr/ADR-001-category-and-upper-level-modeling.md)
and the full spec in [`apqc_to_bfo_cco_methodology.md`](apqc_to_bfo_cco_methodology.md).

## Phase 0

The current phase. Plan and status: [`PHASE0.md`](PHASE0.md). It sets the
corpus-wide meta-decisions, generates the catalog, stands up the validation
harness, and provides a **section daemon** that iterates the 13 top-level APQC
sections, transforming each into a validated reality-layer module.

## Quickstart

```bash
python -m pip install -r requirements.txt        # rdflib, pyshacl, (sdk for live runs)

python -m src.apqc_transform.catalog             # (re)generate apqc-catalog.ttl
python -m src.apqc_transform.validate            # self-test the gates (A-D)
python -m src.apqc_transform.daemon              # dry-run all 13 sections (offline)
python -m src.apqc_transform.daemon --section 1.0 --live   # transform one section via the model
```

All four gates A–D are operational:

| Gate | Tool | Needs |
|---|---|---|
| A Syntax | rdflib | — |
| B IRI resolution | rdflib + `vendor/cco/` closure | pinned CCO ([vendor/cco/README.md](vendor/cco/README.md)) |
| C SHACL | pyshacl `-a` + `apqc_shapes.ttl` | — |
| D Reasoner | **ELK via ROBOT** (`tools/robot.jar`) | Java + the closure |

Gates B/D degrade to **SKIP** (not FAIL) if the closure or `tools/robot.jar` is
absent, so a fresh checkout's offline self-test stays green. Fetch the jar with:

```bash
curl -sL -o tools/robot.jar https://github.com/ontodev/robot/releases/latest/download/robot.jar
```

## Layout

```
ontology/      catalog, shared extension, SHACL shapes, bad-examples fixture, slices/, reports/
src/apqc_transform/  pcf_export · catalog · validate · agent_runner · daemon · config
prompts/       slice_transform_prompt.md  (methodology distilled for the agent)
docs/adr/      architecture decision records
vendor/cco/    pinned CCO 2.0 (2024-11-06) dependency closure  (fetch; not committed)
tools/         robot.jar — Gate D reasoner (ELK)  (fetch; not committed)
```
