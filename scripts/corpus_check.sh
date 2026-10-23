#!/usr/bin/env bash
# Corpus-wide coherence: merge all 13 slices + ext + catalog + the Phase-1
# capability/role layer (capabilities_roles + delivery_processes) + CCO
# closure, reason with ELK. The capability layer is a merge-only shared
# layer (no slice imports it); it is included here so it cannot perturb the
# v0.3.0 ELK consistency unnoticed (PHASE1 definition-of-done).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# Namespace guard (ADR-002): the retired placeholder base must not come back.
# (Prose may cite it; the [c] keeps this line from matching itself.)
if git grep -n "example\.org/apq[c]" -- ontology src scripts tools qa ':!*.md'; then
  echo "FAIL  the retired example.org placeholder base is back (lines above; ADR-002)"; exit 1
fi
echo "Namespace guard: no retired example.org placeholder IRIs (ADR-002)"
INPUTS=""
for f in ontology/slices/apqc_*_0.ttl ontology/apqc-ext.ttl ontology/apqc-catalog.ttl ontology/capabilities_roles.ttl ontology/delivery_processes.ttl ontology/capabilities_wiring.ttl vendor/cco/CommonCoreOntologiesMerged.ttl; do
  INPUTS="$INPUTS --input $f"
done
echo "Merging 13 slices + ext + catalog + capability layer (roles+delivery+wiring) + CCO; reasoning with ELK..."
java -jar tools/robot.jar merge $INPUTS reason --reasoner ELK --output ontology/reports/_corpus_reasoned.ttl
echo "EXIT $?  (0 = consistent, no unsatisfiable classes)"

echo
echo "Gate F -- referential integrity + D7 scheme (vendored RefIntegrity linter; needs node)..."
python scripts/refintegrity_check.py
