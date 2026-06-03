"""Validation harness -- Methodology §9 Gates A-D, scriptable and offline.

Gate A  Syntax        rdflib parse
Gate B  IRI resolution every cco:/obo: IRI used resolves in the local closure
Gate C  SHACL         pyshacl -a against apqc_shapes.ttl -> zero violations
Gate D  Reasoner      consistency + no unsatisfiable classes (owlready2/robot)

Gates degrade gracefully: if the vendored CCO closure (Gate B/D) or a reasoner
(Gate D) is not yet present, the gate is reported as SKIPPED rather than failing
the run -- Phase 0 stands the harness up before the closure lands (PHASE0 §9).
Mandatory gates that actually run and fail do block release.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path

from . import config


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"


@dataclass
class GateResult:
    gate: str
    status: Status
    detail: str = ""
    mandatory: bool = True


@dataclass
class Report:
    module: str
    results: list[GateResult] = field(default_factory=list)

    @property
    def failed_mandatory(self) -> bool:
        return any(r.status == Status.FAIL and r.mandatory for r in self.results)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["failed_mandatory"] = self.failed_mandatory
        return d

    def summary(self) -> str:
        rows = [f"  {r.gate:<22} {r.status.value:<5} {r.detail}" for r in self.results]
        verdict = "FAILED" if self.failed_mandatory else "OK"
        return f"[{verdict}] {self.module}\n" + "\n".join(rows)


def _closure_files() -> list[Path]:
    if not config.VENDOR_CCO.exists():
        return []
    return sorted(
        p for p in config.VENDOR_CCO.iterdir() if p.suffix in (".ttl", ".owl", ".rdf")
    )


def _supporting_graphs(module: Path) -> list[Path]:
    """Slices are SELF-CONTAINED: each inlines the canonical act-genus anchors
    (mirrored from apqc-ext.ttl) so it validates standalone against CCO with no
    extension merge. Returns nothing extra -- Gate C/D test the module exactly
    as an external reviewer loads it (module + pinned CCO closure). apqc-ext.ttl
    remains the master registry but is no longer a validation dependency.
    """
    return []


# --- Gate A -----------------------------------------------------------------
def gate_a_syntax(module: Path) -> GateResult:
    try:
        import rdflib
    except ImportError:
        return GateResult("A Syntax", Status.SKIP, "rdflib not installed")
    try:
        g = rdflib.Graph()
        g.parse(str(module), format="turtle")
        return GateResult("A Syntax", Status.PASS, f"{len(g)} triples")
    except Exception as e:  # noqa: BLE001
        return GateResult("A Syntax", Status.FAIL, str(e).splitlines()[0])


# --- Gate B -----------------------------------------------------------------
def gate_b_iri_resolution(module: Path) -> GateResult:
    try:
        import rdflib
    except ImportError:
        return GateResult("B IRI resolution", Status.SKIP, "rdflib not installed")

    closure = _closure_files()
    if not closure:
        return GateResult(
            "B IRI resolution", Status.SKIP,
            f"no vendored CCO closure under {config.VENDOR_CCO} (see vendor/cco/README.md)",
        )

    cco = config.NS["cco"]
    obo = config.NS["obo"]

    used: set[str] = set()
    mg = rdflib.Graph(); mg.parse(str(module), format="turtle")
    for s, p, o in mg:
        for term in (s, p, o):
            t = str(term)
            if t.startswith(cco) or t.startswith(obo):
                used.add(t)

    declared: set[str] = set()
    cg = rdflib.Graph()
    for f in closure:
        cg.parse(str(f))
    for s in cg.subjects():
        declared.add(str(s))

    missing = sorted(t for t in used if t not in declared)
    if missing:
        return GateResult(
            "B IRI resolution", Status.FAIL,
            f"{len(missing)} unresolved IRI(s), e.g. {missing[:3]}",
        )
    return GateResult("B IRI resolution", Status.PASS, f"{len(used)} CCO/OBO IRIs resolve")


# --- Gate C -----------------------------------------------------------------
def gate_c_shacl(module: Path, shapes: Path | None = None) -> GateResult:
    shapes = shapes or config.SHAPES_TTL
    try:
        from pyshacl import validate as pyshacl_validate
    except ImportError:
        return GateResult("C SHACL", Status.SKIP, "pyshacl not installed")
    try:
        import rdflib

        # Validate the module STANDALONE. The shapes are authored to target only
        # ex: module nodes; merging the CCO closure into the data graph would make
        # the shapes fire on CCO's own restriction axioms (false positives).
        # Subclass-chain checks (S2/S5) are satisfied in-module because each local
        # genus carries its `rdfs:subClassOf cco:<Act>` axiom locally.
        data = rdflib.Graph(); data.parse(str(module), format="turtle")
        # Load imported shared-extension genera so S2/S5 subclass chains resolve
        # (the CCO closure is still NOT merged here -- see note above).
        for sup in _supporting_graphs(module):
            data.parse(str(sup), format="turtle")
        conforms, _report_graph, report_text = pyshacl_validate(
            data,
            shacl_graph=str(shapes),
            advanced=True,
            inference="none",
            meta_shacl=False,
        )
        if conforms:
            return GateResult("C SHACL", Status.PASS, "zero violations")
        # count violations vs warnings from the text report
        viol = report_text.count("Severity: sh:Violation")
        warn = report_text.count("Severity: sh:Warning")
        status = Status.FAIL if viol else Status.PASS
        return GateResult("C SHACL", status, f"{viol} violation(s), {warn} warning(s)")
    except Exception as e:  # noqa: BLE001
        return GateResult("C SHACL", Status.FAIL, str(e).splitlines()[0])


# --- Gate D -----------------------------------------------------------------
def _java() -> str | None:
    return shutil.which("java")


def gate_d_reasoner(module: Path) -> GateResult:
    """Merge module + pinned closure, reason with ELK via ROBOT.

    ROBOT `reason` exits non-zero (and prints the offending classes) if the
    ontology is inconsistent or has unsatisfiable classes; exit 0 means
    consistent with all classes satisfiable.
    """
    closure = _closure_files()
    if not closure:
        return GateResult(
            "D Reasoner", Status.SKIP,
            f"no vendored CCO closure under {config.VENDOR_CCO}",
        )
    if not config.ROBOT_JAR.exists():
        return GateResult("D Reasoner", Status.SKIP, f"ROBOT jar not found at {config.ROBOT_JAR}")
    if not _java():
        return GateResult("D Reasoner", Status.SKIP, "java not on PATH")

    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    reasoned = config.REPORTS_DIR / f"_reasoned_{module.stem}.ttl"
    cmd = ["java", "-jar", str(config.ROBOT_JAR), "merge", "--input", str(module)]
    for f in _supporting_graphs(module):       # imported shared-extension genera
        cmd += ["--input", str(f)]
    for f in closure:
        cmd += ["--input", str(f)]
    cmd += ["reason", "--reasoner", config.REASONER, "--output", str(reasoned)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return GateResult("D Reasoner", Status.FAIL, "ROBOT reason timed out (>600s)")

    if proc.returncode == 0:
        return GateResult("D Reasoner", Status.PASS, "consistent; no unsatisfiable classes (ELK)")
    # Surface ROBOT's diagnostic (e.g. "There are N unsatisfiable classes"),
    # stripping the timestamp/level log prefix; ignore the generic help footer.
    lines = (proc.stderr + "\n" + proc.stdout).splitlines()
    hit = next(
        (ln for ln in lines
         if ("unsatisf" in ln.lower() or "inconsist" in ln.lower())
         and "--help" not in ln.lower()),
        None,
    )
    if hit and " - " in hit:
        hit = hit.split(" - ", 1)[1]   # drop "<ts> ERROR <logger> - "
    detail = (hit or f"ROBOT exit {proc.returncode}").strip()
    return GateResult("D Reasoner", Status.FAIL, detail)


# --- Driver -----------------------------------------------------------------
def gates(module: Path, shapes: Path | None = None) -> Report:
    rep = Report(module=str(module))
    a = gate_a_syntax(module)
    rep.results.append(a)
    if a.status == Status.FAIL:
        # no point running downstream gates on unparseable Turtle
        for g in ("B IRI resolution", "C SHACL", "D Reasoner"):
            rep.results.append(GateResult(g, Status.SKIP, "skipped: Gate A failed"))
        return rep
    rep.results.append(gate_b_iri_resolution(module))
    rep.results.append(gate_c_shacl(module, shapes))
    rep.results.append(gate_d_reasoner(module))
    return rep


def main(argv: list[str]) -> int:
    if not argv:
        # self-test: frozen reference + catalog should be clean
        targets = [config.REFERENCE_TTL, config.CATALOG_TTL]
    else:
        targets = [Path(a) for a in argv]
    failed = False
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    for t in targets:
        rep = gates(t)
        print(rep.summary(), "\n")
        out = config.REPORTS_DIR / f"gate-{t.stem}.json"
        out.write_text(json.dumps(rep.to_dict(), indent=2), encoding="utf-8")
        failed = failed or rep.failed_mandatory
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
