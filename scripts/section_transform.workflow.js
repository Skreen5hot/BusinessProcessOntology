export const meta = {
  name: 'apqc-section-transform',
  description: 'Transform one APQC section into a validated, Gate-F-reviewed BFO/CCO reality-layer module (args-driven)',
  phases: [
    { title: 'Vocabulary', detail: 'shared ICEs/agents/roles/capabilities + proposed genera for the section' },
    { title: 'Model', detail: 'one agent per process group: R5 test + act classification + partonomy' },
    { title: 'Assemble', detail: 'merge fragments into the slice module on disk' },
    { title: 'Validate', detail: 'Gates A-D via the harness, self-repair until clean' },
    { title: 'Review', detail: 'adversarial check that each act anchor is the CORRECT act' },
    { title: 'Repair', detail: 'apply the review suggested-fixes (data-driven), re-validate A-D' },
  ],
}

// ---- args: { section, section_name, out, context, groups:[{h,tsv,name}] } ----
// args may arrive as an object or as a JSON string depending on the caller; handle both.
const A = (typeof args === 'string') ? JSON.parse(args) : (args || {})
const SECTION = A.section
const SECTION_NAME = A.section_name
const OUT = A.out
const CONTEXT = A.context
const GROUPS = A.groups

const COMMON = `You are transforming APQC section ${SECTION} "${SECTION_NAME}" into a BFO 2020 / CCO 2.0 reality-layer module.
FIRST read and treat as binding, in order:
  - ${CONTEXT}                         (operating brief: R5 test, IRI scheme, GOLDEN PRINCIPLE, hard rules, material-I/O note)
  - prompts/slice_transform_prompt.md
  - ontology/slices/apqc_1_1_1.ttl     (GOLD pattern; copy house style + prefixes exactly)
  - ontology/apqc-ext.ttl              (shared genera — REUSE, never re-mint)
Verify every cco:ont… IRI in vendor/cco/CommonCoreOntologiesMerged.ttl before use (read the definition, not just the label).
IRI scheme (STRICT, D7): EVERY primary process class IRI MUST be exactly ex:P<pcfID> (e.g. PCF 10399 -> ex:P10399) -- NEVER a readable name like ex:ResolveComplaint. Each pcfID maps to exactly ONE class (no duplicates). Readable ex: CamelCase names are ONLY for supporting classes (ICEs/agents/roles/capabilities/genera), which carry NO ex:pcfID. Catalog node = ex:PCF_<pcfID>.
GOLDEN PRINCIPLE: act genus must agree with output kind — Appraisal/Analysis/Information-Processing → DESCRIPTIVE ICE; Planning/Formulation/Selection → DIRECTIVE ICE.`

const VOCAB_SCHEMA = {
  type: 'object', required: ['vocab_turtle', 'manifest', 'ext_proposals'],
  properties: {
    vocab_turtle: { type: 'string' },
    manifest: { type: 'array', items: { type: 'object', required: ['iri', 'label', 'kind'], properties: { iri: { type: 'string' }, label: { type: 'string' }, kind: { type: 'string' } } } },
    ext_proposals: { type: 'array', items: { type: 'object', required: ['iri', 'turtle', 'reason'], properties: { iri: { type: 'string' }, turtle: { type: 'string' }, reason: { type: 'string' } } } },
  },
}
const GROUP_SCHEMA = {
  type: 'object', required: ['group', 'r5_decisions', 'process_turtle', 'bridges'],
  properties: {
    group: { type: 'string' },
    r5_decisions: { type: 'array', items: { type: 'object', required: ['pcf_id', 'decision', 'reason'], properties: { pcf_id: { type: 'string' }, hierarchy_id: { type: 'string' }, decision: { type: 'string' }, reason: { type: 'string' } } } },
    process_turtle: { type: 'string' },
    extra_supporting_turtle: { type: 'string' },
    bridges: { type: 'array', items: { type: 'object', required: ['catalog_iri', 'reality_iri'], properties: { catalog_iri: { type: 'string' }, reality_iri: { type: 'string' } } } },
  },
}

phase('Vocabulary')
const vocab = await agent(
  `${COMMON}

TASK: Build the SHARED supporting vocabulary for ALL of section ${SECTION} so the group agents reuse one consistent set (no collisions).
Read every group TSV listed here: ${GROUPS.map(g => g.tsv).join(', ')} (and build/section_${SECTION.split('.')[0]}.0/all.json).
Across the section, mint ONCE each input/output ICE (Descriptive cco:ont00000853 vs Directive cco:ont00000965 — judge describe-vs-prescribe), agent/org (cco:ont00001017/ont00001180), role (BFO_0000023), capability (cco:ont00001379/ont00000568). For operations sections, MATERIAL inputs/outputs (bfo:material entity) are legal. Add 'is about' (cco:ont00001808) on output ICEs that describe a subject. Genus-differentia skos:definition + rdfs:label on each. Reuse reference-module classes where they already fit.
Also propose any NEW recurring act genus the section needs beyond ext (anchored under a CCO Act) as ext_proposals.
Return vocab Turtle, a manifest of every IRI, and the ext proposals. No process classes here.
IMPORTANT: do NOT write or create any .ttl file on disk — return everything via the structured result only. The assembly stage is the sole writer.`,
  { label: `vocab:${SECTION}`, phase: 'Vocabulary', schema: VOCAB_SCHEMA },
)
const manifestText = (vocab?.manifest || []).map(m => `${m.iri}  [${m.kind}]  ${m.label}`).join('\n')
log(`Vocabulary: ${vocab?.manifest?.length || 0} shared classes, ${vocab?.ext_proposals?.length || 0} proposed genera`)

phase('Model')
const groupResults = await parallel(GROUPS.map(g => () =>
  agent(
    `${COMMON}

TASK: Model the reality layer for process group ${g.h} "${g.name}". Your rows: read ${g.tsv}.
Apply the R5 test to EVERY row and record the decision (process | capability | catalog-only) + one-line reason. Standing functions → Organization Capability (R6); pure headings → catalog-only.
For each process: mint ex:P<pcfID>, engineer the act genus from the verb (GOLDEN PRINCIPLE), attach I/O as ICEs (or material entities in operations) ONLY when definitional (Phase-3; else rdfs:comment), build parent→child partonomy with cco:ont00001777 (never rdfs:subClassOf between processes), write genus-differentia skos:definition + ex:pcfID/ex:hierarchyID/ex:apqcSourceText + rdfs:label + skos:example.
REUSE these shared vocab IRIs (do not redefine):
${manifestText}
Available shared genera in apqc-ext.ttl (REUSE these, do not re-mint): ex:ActOfAnalysis, ex:ActOfIdentification, ex:ActOfFormulation, ex:ActOfSelection, ex:ActOfAcquisition${(vocab?.ext_proposals || []).length ? '; new proposals this section: ' + (vocab.ext_proposals || []).map(e => e.iri).join(', ') : ''}.
Emit a bridge ex:PCF_<pcfID> → ex:P<pcfID> for every modeled node. Return process Turtle, R5 log, any unavoidable extra supporting classes, and bridges.
IMPORTANT: do NOT write or create any .ttl file on disk — return everything via the structured result only. The assembly stage is the sole writer.`,
    { label: `model:${g.h}`, phase: 'Model', schema: GROUP_SCHEMA },
  )
)).then(rs => rs.filter(Boolean))

const dec = (k) => groupResults.flatMap(r => (r.r5_decisions || []).filter(d => d.decision === k)).length
log(`Model: ${dec('process')} processes, ${dec('capability')} capabilities, ${dec('catalog-only')} catalog-only`)

phase('Assemble')
const fragments = groupResults.map(r => `# ===== group ${r.group} =====\n${r.process_turtle}\n${r.extra_supporting_turtle || ''}`).join('\n\n')
const allBridges = groupResults.flatMap(r => r.bridges || []).map(b => `${b.catalog_iri} ex:designatesProcessType ${b.reality_iri} .`).join('\n')
const extLocal = (vocab?.ext_proposals || []).map(e => e.turtle).join('\n\n')
const slug = SECTION.split('.')[0] + '_0'

const assembled = await agent(
  `${COMMON}

TASK: Assemble ONE valid Turtle module and WRITE it to ${OUT} with the Write tool, then return a summary.
Compose in order:
1) Prefixes (copy from ontology/slices/apqc_1_1_1.ttl) PLUS @prefix apqc: <http://example.org/apqc/scheme#> .
2) owl:Ontology header for <http://example.org/apqc/slice/${SECTION}>: dct:title "APQC reality-layer slice ${SECTION}: ${SECTION_NAME}", owl:versionInfo "0.1.0", rdfs:comment recording CCO pin v2.0 (2024-11-06) + ADR-001. Put owl:imports <http://example.org/apqc/ext> on a COMMENTED line (the validator merges apqc-ext.ttl separately; a live example.org import breaks ROBOT).
3) Provenance annotation properties: ex:pcfID, ex:hierarchyID, ex:apqcSourceText, ex:designatesProcessType.
4) PROPOSED-EXT genera under a '# PROPOSE-EXT: promote to apqc-ext.ttl after review' comment:
${extLocal || '# (none)'}
5) SHARED VOCABULARY:
${vocab?.vocab_turtle || ''}
6) PROCESS CLASSES + capabilities from all groups:
${fragments}
7) CATALOG→REALITY BRIDGES:
${allBridges}
RECONCILE duplicate IRIs to one coherent definition. Ensure every genus/filler IRI is declared (here, in apqc-ext.ttl, or in CCO). Produce SYNTACTICALLY VALID Turtle.`,
  {
    label: `assemble:${SECTION}`, phase: 'Assemble',
    schema: { type: 'object', required: ['written_path', 'n_processes', 'notes'], properties: { written_path: { type: 'string' }, n_processes: { type: 'integer' }, n_capabilities: { type: 'integer' }, n_supporting: { type: 'integer' }, n_bridges: { type: 'integer' }, ext_proposals: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } } },
  },
)
log(`Assembled ${assembled?.written_path}: ${assembled?.n_processes} processes`)

phase('Validate')
const VAL_SCHEMA = { type: 'object', required: ['final_status', 'gate_a', 'gate_b', 'gate_c', 'gate_d', 'attempts'], properties: { final_status: { type: 'string' }, gate_a: { type: 'string' }, gate_b: { type: 'string' }, gate_c: { type: 'string' }, gate_d: { type: 'string' }, attempts: { type: 'integer' }, remaining_issues: { type: 'string' } } }
const validation = await agent(
  `TASK: Normalize, then validate and self-repair ${OUT} until Gates A-D are clean.
FIRST run \`python scripts/normalize_iris.py ${OUT}\` to enforce the D7 scheme (ex:P<pcfID> on every primary class). If it reports a DUPLICATE pcfID, two classes carry the same ex:pcfID: find the mis-keyed one in ${OUT} (cross-check the group TSVs), correct its ex:pcfID to the right value, and re-run the normalizer until it succeeds with no duplicates.
THEN loop (max 6): run \`python -m src.apqc_transform.validate ${OUT}\`; read the gate table + ontology/reports/gate-${slug.replace('_0','_0')}.json (file: ontology/reports/gate-apqc_${slug}.json); fix any FAIL by editing ${OUT} (A syntax; B verify the cco:/obo: IRI in vendor/cco/CommonCoreOntologiesMerged.ttl; C read the SHACL message — common: a Directive ICE anchored only under CCO Plan/Objective needs an explicit rdfs:subClassOf cco:ont00000965, and an act under a CCO Act outside the shape allowlist needs an explicit rdfs:subClassOf cco:ont00000228 Planned Act; D find contradictory restrictions). Preserve intent; never delete a process to silence a gate. Stop when no FAIL remains. Delete ontology/reports/_reasoned_*.ttl when done. Return final gate statuses + attempts.`,
  { label: `validate:${SECTION}`, phase: 'Validate', schema: VAL_SCHEMA },
)
log(`Validate: ${validation?.final_status} after ${validation?.attempts} attempt(s) — C:${validation?.gate_c} D:${validation?.gate_d}`)

phase('Review')
const REVIEW_SCHEMA = {
  type: 'object', required: ['group', 'findings', 'anchors_ok', 'anchors_flagged'],
  properties: { group: { type: 'string' }, anchors_ok: { type: 'integer' }, anchors_flagged: { type: 'integer' }, findings: { type: 'array', items: { type: 'object', required: ['pcf_id', 'severity', 'issue', 'suggested_fix'], properties: { pcf_id: { type: 'string' }, severity: { type: 'string' }, issue: { type: 'string' }, suggested_fix: { type: 'string' } } } } },
}
const reviews = await parallel(GROUPS.map(g => () =>
  agent(
    `You are an adversarial BFO/CCO reviewer (Gate F — semantic correctness, which Gates A-D cannot judge).
Read ${OUT} and the source rows ${g.tsv}, plus the §6 verified CCO term table in apqc_to_bfo_cco_methodology.md.
For EACH process class from group ${g.h} in ${OUT}, judge ADVERSARIALLY: (1) is the act genus the CORRECT kind of act (analysis vs appraisal vs planning vs information-processing vs communication/measuring), or a false-friend? (2) does the genus AGREE with the output's descriptive-vs-directive kind (GOLDEN PRINCIPLE)? (3) does R5 hold (bounded occurrent vs standing function)? (4) are existential I/O restrictions truly definitional (Phase-3)? (5) are sibling/parallel rows anchored consistently? Default to flagging when uncertain. Give each finding a severity (critical/major/minor) and a CONCRETE suggested_fix. Count anchors OK vs flagged.`,
    { label: `review:${g.h}`, phase: 'Review', schema: REVIEW_SCHEMA },
  )
)).then(rs => rs.filter(Boolean))
const findings = reviews.flatMap(r => (r.findings || []).map(f => ({ group: r.group, ...f })))
const actionable = findings.filter(f => f.severity === 'critical' || f.severity === 'major')
log(`Review: ${findings.length} findings (${actionable.length} major+)`)

phase('Repair')
let repairOut = null, reval = validation
if (actionable.length) {
  const fixList = actionable.map(f => `- P${f.pcf_id} [${f.severity}]: ${f.issue}\n    FIX: ${f.suggested_fix}`).join('\n')
  repairOut = await agent(
    `${COMMON}

TASK: Open ${OUT} and apply these Gate-F review fixes class by class (Edit tool). Keep all provenance, partonomy, and gate-passing axioms (direct rdfs:subClassOf cco:ont00000965 / cco:ont00000228). For each re-anchor or rejected candidate, add an rdfs:comment per §6. Mint any new supporting ICE under the correct CCO parent with a genus-differentia definition. Enforce the GOLDEN PRINCIPLE and sibling consistency.

${fixList}

Then run \`python -m src.apqc_transform.validate ${OUT}\` and self-repair any Gate A-D FAIL (max 6 attempts; same tactics as before). Delete ontology/reports/_reasoned_*.ttl when done. Return the change count and the final gate statuses.`,
    {
      label: `repair:${SECTION}`, phase: 'Repair',
      schema: { type: 'object', required: ['changes_applied', 'final_status', 'gate_c', 'gate_d'], properties: { changes_applied: { type: 'integer' }, new_classes: { type: 'array', items: { type: 'string' } }, final_status: { type: 'string' }, gate_a: { type: 'string' }, gate_b: { type: 'string' }, gate_c: { type: 'string' }, gate_d: { type: 'string' }, remaining_issues: { type: 'string' } } },
    },
  )
  log(`Repair: ${repairOut?.changes_applied || 0} fixes applied — ${repairOut?.final_status} (C:${repairOut?.gate_c} D:${repairOut?.gate_d})`)
} else {
  log('Repair: no major findings; skipped')
}

return {
  section: SECTION,
  written: assembled?.written_path,
  counts: { processes: dec('process'), capabilities: dec('capability'), catalog_only: dec('catalog-only') },
  ext_proposals: (vocab?.ext_proposals || []).map(e => e.iri),
  validation: repairOut ? { gate_a: repairOut.gate_a || reval.gate_a, gate_b: repairOut.gate_b || reval.gate_b, gate_c: repairOut.gate_c, gate_d: repairOut.gate_d, final_status: repairOut.final_status } : reval,
  review: { total: findings.length, major_plus: actionable.length, repaired: !!repairOut, findings },
}
