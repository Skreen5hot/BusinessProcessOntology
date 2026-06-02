"""Stage the per-section data bundles + context pack the transform workflow reads.

Usage:  python scripts/stage_section.py <section>     e.g.  2.0
Writes  build/section_<n>/all.json, group_<g>.tsv (one per process group),
        build/section_<n>/CONTEXT.md
Prints  a JSON line:  {"section","section_name","out","groups":[{h,tsv,name}]}
so the orchestrator can pass `groups` straight into the workflow `args`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.apqc_transform import config, pcf_export  # noqa: E402

CONTEXT_TMPL = """\
# Transform context pack — APQC section {section} ({section_name}) reality layer

You are one stage of a pipeline producing the reality-layer module
`{out}` for APQC section {section} "{section_name}".

## Read these first (binding)
- `prompts/slice_transform_prompt.md` — operating procedure (hard rules + per-node steps).
- `apqc_to_bfo_cco_methodology.md` — full spec (§6 verified CCO term table; Phase-3 necessity rule).
- `docs/adr/ADR-001-category-and-upper-level-modeling.md` — two-layer model; R5 bounded-occurrent test.
- `ontology/slices/apqc_1_1_1.ttl` — GOLD reference; mirror its house style, prefixes, patterns.
- `ontology/apqc-ext.ttl` — shared act genera: ex:ActOfAnalysis, ex:ActOfIdentification, ex:ActOfFormulation, ex:ActOfSelection, ex:ActOfAcquisition (REUSE; never re-mint). New recurring genera are PROPOSE-EXT, not silently duplicated.

## Verify-before-assert (D6)
Before using any `cco:ont…` IRI, confirm its label+definition+parent in the closure:
`grep -A3 'ont00000XXX' vendor/cco/CommonCoreOntologiesMerged.ttl`. A matching label is NOT sufficient.

## IRI scheme (D7)
- reality-layer process class: `ex:P<pcfID>`  ·  catalog node (exists already): `ex:PCF_<pcfID>`.
- supporting classes (ICEs/agents/roles/capabilities/new genera): readable `ex:` CamelCase, NO pcf ids.

## R5 (the one judgement per node) — apply to EVERY row, record the decision + reason
- repeatable occurrent with begin/end, can be a proper part → process `owl:Class ⊑ <CCO Act / ext genus>`.
- standing function/capacity ("Manage…", no natural end) → NOT a process; `owl:Class ⊑ cco:ont00000568` (Organization Capability), `realized in` the acts (R6).
- pure grouping/heading → model NOTHING in the reality layer (catalog already has it).

## GOLDEN PRINCIPLE (genus ↔ output agreement)
Appraisal / Analysis / Information-Processing produce DESCRIPTIVE ICEs (cco:ont00000853 — judgements/representations).
Planning / Formulation / Selection produce DIRECTIVE ICEs (cco:ont00000965 — plans/specs/decisions).
The act genus MUST agree with the descriptive-vs-directive kind of its definitional output.

## Operations categories (4.0,5.0,6.0,8.0,9.0,10.0) — material I/O is legal here
Unlike the planning categories, operations processes may have MATERIAL inputs/outputs
(bfo:material entity fillers); the input-as-role pattern is then available again (D4).
Informational I/O is still modeled as ICEs.

## Hard gate rules (a validator rejects violations)
D1 partonomy via cco:ont00001777 (never rdfs:subClassOf between processes); D3 informational I/O are ICEs;
D4 realizables on Agents/Orgs only; Phase-3 necessity: someValuesFrom ONLY when definitional, else rdfs:comment;
every process carries ex:pcfID/ex:hierarchyID/ex:apqcSourceText + label + genus-differentia skos:definition.
The Category {section} itself is catalog-only (R3) — no has-process-part to its groups.

## Your data
Your subtree's rows are in the TSV named in your task. Columns:
`pcf_id  hierarchy_id  level  parent_pcf  name  description`.
"""


def stage(section: str) -> dict:
    num = section.split(".")[0]
    pid, section_name = config.SECTIONS[section]
    out_dir = config.ROOT / "build" / f"section_{num}.0"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = pcf_export.load_rows()
    byh = {r.hierarchy_id: r for r in rows}
    sub = pcf_export.subtree(rows, section)

    def parent_pcf(r):
        p = byh.get(r.parent_hierarchy)
        return p.pcf_id if p else ""

    # whole-section json
    (out_dir / "all.json").write_text(
        json.dumps(
            [
                {
                    "pcf_id": r.pcf_id, "hierarchy_id": r.hierarchy_id, "level": r.level_name,
                    "name": r.name, "parent_pcf": parent_pcf(r), "description": r.description,
                }
                for r in sub
            ],
            indent=1, ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    groups = []
    for g in [r for r in sub if r.level == 2]:
        members = [r for r in sub if r.hierarchy_id == g.hierarchy_id
                   or r.hierarchy_id.startswith(g.hierarchy_id + ".")]
        tsv = out_dir / f"group_{g.hierarchy_id}.tsv"
        lines = ["pcf_id\thierarchy_id\tlevel\tparent_pcf\tname\tdescription"]
        for r in members:
            desc = (r.description or "").replace("\t", " ").replace("\n", " ").replace("\r", " ")
            lines.append(f"{r.pcf_id}\t{r.hierarchy_id}\t{r.level_name}\t{parent_pcf(r)}\t{r.name}\t{desc}")
        tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
        groups.append({"h": g.hierarchy_id, "tsv": str(tsv.relative_to(config.ROOT)).replace("\\", "/"), "name": g.name})

    out_ttl = f"ontology/slices/apqc_{num}_0.ttl"
    (out_dir / "CONTEXT.md").write_text(
        CONTEXT_TMPL.format(section=section, section_name=section_name, out=out_ttl),
        encoding="utf-8",
    )

    return {"section": section, "section_name": section_name, "out": out_ttl,
            "context": str((out_dir / "CONTEXT.md").relative_to(config.ROOT)).replace("\\", "/"),
            "groups": groups}


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in config.SECTIONS:
        sys.exit(f"usage: stage_section.py <section>; valid: {list(config.SECTIONS)}")
    print(json.dumps(stage(sys.argv[1])))
