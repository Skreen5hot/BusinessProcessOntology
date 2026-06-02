"""Per-section LLM transform (deliverable 0.5).

Each section is handed to a Claude agent that executes the methodology pipeline
(Phases 1-7) over the section's PCF rows and returns a reality-layer Turtle
module. The agent never touches the catalog layer (frozen, deterministic) and
proposes -- but does not auto-merge -- any new shared genus for apqc-ext.ttl.

This module isolates the API call so the daemon's orchestration logic (state,
resume, gating, self-repair) is testable without a live model. `--dry-run`
emits a deterministic placeholder module so the full pipeline can be exercised
offline.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from pathlib import Path

from . import config
from .pcf_export import PcfRow


@dataclass
class TransformInput:
    section: str                 # e.g. "1.0"
    pcf_id: str
    name: str
    rows: list[PcfRow]           # the section subtree (catalog provenance)
    ext_ttl: str                 # current apqc-ext.ttl (shared genera, D9)
    prompt: str                  # prompts/slice_transform_prompt.md
    feedback: str | None = None  # validation report from a prior failed attempt


def _rows_table(rows: list[PcfRow]) -> str:
    lines = ["PCF ID\tHierarchy\tLevel\tName\tDescription"]
    for r in rows:
        desc = (r.description or "").replace("\n", " ").replace("\t", " ")
        lines.append(f"{r.pcf_id}\t{r.hierarchy_id}\t{r.level_name}\t{r.name}\t{desc}")
    return "\n".join(lines)


def build_user_message(ti: TransformInput) -> str:
    parts = [
        f"# Transform APQC section {ti.section} — {ti.name} (PCF {ti.pcf_id})",
        "",
        f"You are producing the reality-layer module `apqc_{ti.section.replace('.', '_')}.ttl`.",
        "Follow the operating procedure below exactly. Output ONLY Turtle.",
        "",
        "## Operating procedure",
        ti.prompt,
        "",
        "## Shared extension already in force (apqc-ext.ttl) — reuse these genera, do not re-mint",
        "```turtle",
        ti.ext_ttl,
        "```",
        "",
        f"## PCF rows for this section ({len(ti.rows)} rows)",
        "```",
        _rows_table(ti.rows),
        "```",
    ]
    if ti.feedback:
        parts += [
            "",
            "## Validation feedback from your previous attempt — fix every violation",
            "```",
            ti.feedback,
            "```",
        ]
    return "\n".join(parts)


_DRY_RUN_TEMPLATE = textwrap.dedent(
    """\
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix owl:  <http://www.w3.org/2002/07/owl#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix dct:  <http://purl.org/dc/terms/> .
    @prefix cco:  <https://www.commoncoreontologies.org/> .
    @prefix ex:   <http://example.org/apqc#> .

    # DRY-RUN PLACEHOLDER for section {section} ({name}).
    # The live daemon replaces this with the agent's reality-layer module.
    <http://example.org/apqc/slice/{slug}> a owl:Ontology ;
        dct:title "APQC reality-layer slice {section}: {name} (DRY RUN)" ;
        owl:versionInfo "0.0.0" ;
        rdfs:comment "Placeholder. CCO pin: {cco}. Not for release." .
    """
)


def transform(ti: TransformInput, *, dry_run: bool = True, model: str | None = None) -> str:
    """Return a reality-layer Turtle module for the section.

    dry_run=True (default) skips the API and returns a parseable placeholder so
    the daemon's gating/state/resume logic can be validated offline.
    """
    if dry_run:
        return _DRY_RUN_TEMPLATE.format(
            section=ti.section,
            slug=ti.section.replace(".", "_"),
            name=ti.name,
            cco=f"{config.CCO_VERSION} ({config.CCO_RELEASE_DATE})",
        )

    # Live path: spawn a Claude agent. Imported lazily so the toolchain runs
    # offline without the SDK installed.
    from claude_agent_sdk import query, ClaudeAgentOptions  # type: ignore

    options = ClaudeAgentOptions(
        model=model or "claude-opus-4-8",
        system_prompt=(
            "You are a BFO 2020 / CCO 2.0 ontology engineer. You convert APQC PCF "
            "rows into a conformant reality-layer Turtle module. Output Turtle only."
        ),
    )
    chunks: list[str] = []
    for message in query(prompt=build_user_message(ti), options=options):
        chunks.append(getattr(message, "text", "") or "")
    return _extract_turtle("".join(chunks))


def _extract_turtle(text: str) -> str:
    """Pull the Turtle out of a fenced ```turtle block if the model wraps it."""
    if "```" not in text:
        return text.strip()
    blocks = text.split("```")
    for i in range(1, len(blocks), 2):
        body = blocks[i]
        first_nl = body.find("\n")
        lang = body[:first_nl].strip().lower()
        if lang in ("turtle", "ttl", ""):
            return body[first_nl + 1 :].strip()
    return text.strip()
