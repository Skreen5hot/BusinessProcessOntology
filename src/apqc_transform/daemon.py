"""Section daemon (deliverable 0.5).

Iterates the 13 top-level APQC sections, transforms each into a reality-layer
module via an LLM agent, and gates the output (A-D). Idempotent and resumable:
section state is persisted, so a crash or kill resumes where it stopped. A
failed mandatory gate is fed back to the agent for up to N self-repair retries
before the section is parked as NEEDS_REVIEW; a non-conformant module is never
released.

Usage:
    python -m src.apqc_transform.daemon                # dry-run all 13 (offline)
    python -m src.apqc_transform.daemon --section 1.0  # one section
    python -m src.apqc_transform.daemon --live         # call the model
    python -m src.apqc_transform.daemon --force        # ignore prior DONE state
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

from . import agent_runner, config, pcf_export, validate
from .agent_runner import TransformInput


class SectionState(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    NEEDS_REVIEW = "NEEDS_REVIEW"


@dataclass
class SectionRecord:
    section: str
    pcf_id: str
    name: str
    state: str
    attempts: int
    module: str | None
    gate_summary: str
    updated_epoch: float


MAX_REPAIR_ATTEMPTS = 2


def _load_state() -> dict[str, dict]:
    if config.STATE_JSON.exists():
        return json.loads(config.STATE_JSON.read_text(encoding="utf-8"))
    return {}


def _save_state(state: dict[str, dict]) -> None:
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    config.STATE_JSON.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _module_path(section: str) -> Path:
    return config.SLICES_DIR / f"apqc_{section.replace('.', '_')}.ttl"


def process_section(
    section: str,
    all_rows: list[pcf_export.PcfRow],
    prompt: str,
    ext_ttl: str,
    *,
    dry_run: bool,
    now: float,
) -> SectionRecord:
    pcf_id, name = config.SECTIONS[section]
    rows = pcf_export.subtree(all_rows, section)
    out = _module_path(section)

    feedback: str | None = None
    last_summary = ""
    for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):
        ti = TransformInput(
            section=section, pcf_id=pcf_id, name=name, rows=rows,
            ext_ttl=ext_ttl, prompt=prompt, feedback=feedback,
        )
        module_ttl = agent_runner.transform(ti, dry_run=dry_run)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(module_ttl, encoding="utf-8")

        report = validate.gates(out)
        last_summary = report.summary().splitlines()[0]
        if not report.failed_mandatory:
            return SectionRecord(
                section, pcf_id, name, SectionState.DONE.value,
                attempt, str(out), last_summary, now,
            )
        # self-repair: hand the violations back to the agent
        feedback = report.summary()

    return SectionRecord(
        section, pcf_id, name, SectionState.NEEDS_REVIEW.value,
        MAX_REPAIR_ATTEMPTS, str(out), last_summary, now,
    )


def run(sections: list[str], *, dry_run: bool, force: bool) -> int:
    all_rows = pcf_export.load_rows()
    prompt = (config.PROMPTS_DIR / "slice_transform_prompt.md").read_text(encoding="utf-8")
    ext_ttl = config.EXT_TTL.read_text(encoding="utf-8")
    state = _load_state()
    epoch_base = time.time()

    review = 0
    for i, section in enumerate(sections):
        prior = state.get(section)
        if prior and prior.get("state") == SectionState.DONE.value and not force:
            print(f"[skip] {section} already DONE")
            continue
        print(f"[run ] {section} — {config.SECTIONS[section][1]}")
        rec = process_section(
            section, all_rows, prompt, ext_ttl,
            dry_run=dry_run, now=epoch_base + i,
        )
        state[section] = asdict(rec)
        _save_state(state)
        print(f"       -> {rec.state}  ({rec.gate_summary})")
        if rec.state == SectionState.NEEDS_REVIEW.value:
            review += 1

    done = sum(1 for s in state.values() if s["state"] == SectionState.DONE.value)
    print(f"\nRoll-up: {done} DONE, {review} NEEDS_REVIEW this run "
          f"({'dry-run' if dry_run else 'live'}).")
    return 1 if review else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="APQC section transform daemon")
    ap.add_argument("--section", help="one section id, e.g. 1.0 (default: all 13)")
    ap.add_argument("--live", action="store_true", help="call the model (default: dry-run)")
    ap.add_argument("--force", action="store_true", help="re-run sections already DONE")
    args = ap.parse_args()

    sections = [args.section] if args.section else list(config.SECTIONS)
    bad = [s for s in sections if s not in config.SECTIONS]
    if bad:
        ap.error(f"unknown section(s): {bad}; valid: {list(config.SECTIONS)}")
    return run(sections, dry_run=not args.live, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
