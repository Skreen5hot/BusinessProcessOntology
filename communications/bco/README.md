---
team: BCO
name: Business and Agent Capabilities Ontology
repository: https://github.com/Skreen5hot/Business-and-Agent-Capabilities-Ontology
---

# BCO

The BCO says what an organization *can* do; this repository says what it *does*. The BCO
takes its act types from this repository (BCO spec v0.4 §1).

**What the BCO takes from this repository:** a pinned partial extract of
`ontology/apqc-ext.ttl` (6 act genera and their CCO/BFO ancestry) at commit `bc64e91`
(v0.4.1; re-pinned from `6613194` on 2026-10-28, BCO merge `6731f59`), digest-checked
weekly against the raw GitHub URL (BCO `config/upstream-sources.yaml`, id `bpo`). It
also reads the MIT grant from `LICENSE` at the same commit. The BCO's own prefix label
for our terms is still `ex:`, bound to our new namespace. That is deliberate; it plans a
separate rename to `bpo:`.

**What this means for work here:**

- **Never rewrite published history on `main`.** Dropping `bc64e91` breaks the BCO's weekly
  check. `6613194` is still cited by digest as the baseline of the BCO's capability
  inventory, so keep it reachable too. If a rewrite is ever needed, send a `notice` here
  first.
- **A move off CCO v2.0 (2024-11-06)** puts the BCO's extracts out of step with our
  anchors; send a `notice` before it lands.
- **Changing any of the 6 vendored genera** (`ex:ActOfAcquisition`, `ActOfDevelopment`,
  `ActOfImprovement`, `ActOfOrganizationalEstablishment`, `ActOfRemuneration`,
  `ActOfReporting`) does not break the pin, but the BCO will be behind until it re-pins;
  a `notice` lets it re-pin promptly.
- **BCO spec v0.4 §2 proposes moving our capability classes into a BCO module.** It is not
  ratified; it is a joint decision, recorded in `docs/adr/` if taken.
