// src/ri-resolve.mjs — RI4: resolver + readable_label + scheme_violation (D7)
const LOCAL_NS = [
  'https://fandaws.com/ontology/bpo#',
  'https://fandaws.com/ontology/bpo/perf#',
];

const CCO_NS_LIST = [
  'https://www.commoncoreontologies.org/',
  'http://www.ontologyrepository.com/CommonCoreOntologies/',
];
const EX_NS = 'https://fandaws.com/ontology/bpo#';
const OPAQUE_RE = /^ont\d+$/;
const ORG_CAPABILITY_LOCAL = 'ont00000568';

function isLocal(iri) {
  return LOCAL_NS.some(ns => iri.startsWith(ns));
}

function getCCOLocal(iri) {
  for (const ns of CCO_NS_LIST) {
    if (iri.startsWith(ns)) return iri.slice(ns.length);
  }
  return null;
}

function isOrgCapability(iri) {
  return getCCOLocal(iri) === ORG_CAPABILITY_LOCAL;
}

function normalizeForLookup(s) {
  return s.replace(/[_-]/g, ' ').toLowerCase();
}

function lookupSuggestion(local, register) {
  if (!register) return undefined;
  const norm = normalizeForLookup(local);
  const entry = register.find(
    e => normalizeForLookup(e.alias) === norm || normalizeForLookup(e.label) === norm
  );
  return entry ? entry.iri : undefined;
}

export function resolve(collected, register) {
  const { declared, references } = collected;
  const issues = [];
  const seenDangling = new Set();
  const seenLabel = new Set();

  for (const ref of references) {
    if (isLocal(ref.iri)) {
      if (!declared.has(ref.iri)) {
        const key = `${ref.iri}\0${ref.module}\0${ref.line}`;
        if (!seenDangling.has(key)) {
          seenDangling.add(key);
          issues.push({ type: 'dangling_ref', iri: ref.iri, module: ref.module, line: ref.line });
        }
      }
    } else {
      const ccoLocal = getCCOLocal(ref.iri);
      if (ccoLocal !== null && !OPAQUE_RE.test(ccoLocal)) {
        const key = `${ref.iri}\0${ref.module}\0${ref.line}`;
        if (!seenLabel.has(key)) {
          seenLabel.add(key);
          const suggestion = lookupSuggestion(ccoLocal, register);
          const issue = { type: 'readable_label', iri: ref.iri, module: ref.module, line: ref.line };
          if (suggestion !== undefined) issue.suggestion = suggestion;
          issues.push(issue);
        }
      }
    }
  }

  // FR-12: scheme_violation — uses collected.classInfo if present
  // BPO local modification (WP6 Phase B, 2026-10-31): "is a capability" follows
  // rdfs:subClassOf through the loaded classes, not only a directly asserted
  // Organization Capability parent. Read asserted-only, removing a redundant
  // co-parent made 9 capabilities-with-process-IRIs vanish from the count while
  // they were still capabilities. CCO declares no subclass of 568, so the
  // closure over the project's own classes is enough.
  const capMemo = new Map();
  const reachesOrgCapability = (iri, seen = new Set()) => {
    if (isOrgCapability(iri)) return true;
    if (capMemo.has(iri)) return capMemo.get(iri);
    if (seen.has(iri)) return false;
    seen.add(iri);
    const info = collected.classInfo ? collected.classInfo.get(iri) : undefined;
    const result = !!info && info.subClassOf.some((p) => reachesOrgCapability(p, seen));
    capMemo.set(iri, result);
    return result;
  };
  if (collected.classInfo) {
    for (const [iri, info] of collected.classInfo) {
      // FR-12: skip non-owl:Class subjects (NamedIndividual/Concept catalog nodes are exempt)
      if (!declared.has(iri) || !iri.startsWith(EX_NS) || info.pcfID == null || !info.isClass) continue;
      const localName = iri.slice(EX_NS.length);
      const isCapability = reachesOrgCapability(iri);
      if (/^P\d+$/.test(localName) && isCapability) {
        issues.push({ type: 'scheme_violation', iri, module: info.module, line: info.line, rule: 'capability-as-process' });
      } else if (!isCapability && localName !== `P${info.pcfID}`) {
        issues.push({ type: 'scheme_violation', iri, module: info.module, line: info.line, rule: 'pcf-without-P-iri' });
      }
    }
  }

  return issues;
}
