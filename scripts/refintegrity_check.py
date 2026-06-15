"""Gate F -- referential integrity + D7 scheme conformance over the merged corpus.

Runs the vendored RefIntegrity linter (tools/refintegrity/, from Skreen5hot/IRI_Linter,
implementing FNSR-RefIntegrity-Linter-Spec-R1.1) over every ex:/perf: module and asserts
the FR-18 baseline:

    dangling_ref           0   (every ex:/perf: reference resolves to a declared term)
    readable_label         0   (not exercised here -- no --register)
    capability-as-process 39   (the known capabilities-wearing-process-IRIs; a tracked backlog)
    pcf-without-P-iri      0

Gate F PASSES iff the actual counts equal the baseline -- so the 39 known findings do NOT
block the build, but ANY deviation does (a new dangling ref, a new mis-IRI'd class, or a silent
fix that should update the baseline). This mirrors the apqc_bad_examples expected-count discipline.

cco:/obo: existence is Gate B's job; this gate checks only the project-minted namespaces, so the
CCO closure is NOT loaded (the run is fast). Requires `node` on PATH; SKIPs gracefully if absent.

Usage:  python scripts/refintegrity_check.py        # exit 0 = at baseline, 1 = deviation, 0 = SKIP
"""
from __future__ import annotations
import glob, re, shutil, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "refintegrity" / "src" / "ri-cli.mjs"

# FR-18 baseline (R1.1). Update deliberately if the corpus changes (and say why in the commit).
BASELINE = {"dangling_ref": 0, "readable_label": 0,
            "capability-as-process": 39, "pcf-without-P-iri": 0}

def modules() -> list[str]:
    """Every project-minted (ex:/perf:) module; NOT the CCO closure (Gate B owns cco:/obo:)."""
    files = sorted(glob.glob(str(ROOT / "ontology" / "slices" / "apqc_*_0.ttl")))
    files += [str(ROOT / "ontology" / f) for f in
              ("apqc-ext.ttl", "apqc-catalog.ttl", "capabilities_roles.ttl",
               "delivery_processes.ttl", "capabilities_wiring.ttl")]
    return [f for f in files if Path(f).exists()]

def parse(out: str) -> Counter:
    """Count violations by rule (scheme_violation) or by type (dangling_ref / readable_label)."""
    c = Counter()
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.search(r"\((capability-as-process|pcf-without-P-iri)\)", line)
        if m:
            c[m.group(1)] += 1
        elif " dangling_ref " in f" {line} ":
            c["dangling_ref"] += 1
        elif " readable_label " in line:
            c["readable_label"] += 1
    return c

def main() -> int:
    if shutil.which("node") is None:
        print("[F RefIntegrity]  SKIP  node not on PATH")
        return 0
    if not CLI.exists():
        print(f"[F RefIntegrity]  SKIP  vendored linter not found at {CLI.relative_to(ROOT)}")
        return 0

    cmd = ["node", str(CLI), "--modules", *modules()]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), timeout=300)
    if proc.returncode == 2:
        print("[F RefIntegrity]  FAIL  linter systemic error (exit 2):")
        print("  " + (proc.stderr.strip() or "(no stderr)"))
        return 1

    actual = parse(proc.stdout)
    keys = sorted(set(BASELINE) | set(actual))
    rows = [f"    {k:<22} {actual.get(k,0):>4}   (baseline {BASELINE.get(k,0)})" for k in keys]
    deviations = {k: (actual.get(k, 0), BASELINE.get(k, 0))
                  for k in keys if actual.get(k, 0) != BASELINE.get(k, 0)}

    if not deviations:
        print("[F RefIntegrity]  PASS  at baseline (referential integrity holds; "
              f"{BASELINE['capability-as-process']} known capability-as-process findings)")
        print("\n".join(rows))
        return 0

    print("[F RefIntegrity]  FAIL  deviation from baseline:")
    print("\n".join(rows))
    for k, (a, b) in deviations.items():
        if k in ("dangling_ref", "readable_label", "pcf-without-P-iri"):
            print(f"  * {k}: {a} (expected {b}) -- a real integrity/scheme regression; see the flagged lines.")
        else:
            verb = "NEW mis-IRI'd class(es)" if a > b else "a finding was resolved"
            print(f"  * {k}: {a} (expected {b}) -- {verb}; fix it, or update BASELINE in this script deliberately.")
    # surface the offending lines that aren't part of the known capability-as-process set
    hard = [ln for ln in proc.stdout.splitlines()
            if "dangling_ref" in ln or "readable_label" in ln or "pcf-without-P-iri" in ln]
    if hard:
        print("\n  offending lines:")
        for ln in hard[:25]:
            print("    " + ln.strip())
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
