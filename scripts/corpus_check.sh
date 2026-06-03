#!/usr/bin/env bash
# Corpus-wide coherence: merge all 13 slices + ext + catalog + CCO closure, reason with ELK.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
INPUTS=""
for f in ontology/slices/apqc_*_0.ttl ontology/apqc-ext.ttl ontology/apqc-catalog.ttl vendor/cco/CommonCoreOntologiesMerged.ttl; do
  INPUTS="$INPUTS --input $f"
done
echo "Merging 13 slices + ext + catalog + CCO; reasoning with ELK..."
java -jar tools/robot.jar merge $INPUTS reason --reasoner ELK --output ontology/reports/_corpus_reasoned.ttl
echo "EXIT $?  (0 = consistent, no unsatisfiable classes)"
