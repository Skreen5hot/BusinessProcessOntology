# Request to the Dev Team — rebuild RefIntegrity Module 3 to spec R1.1

**From:** Ontology Team (BPO)
**Re:** the RefIntegrity Linter (`src/ri-collect.mjs` / `ri-resolve.mjs` / `ri-cli.mjs`) — scheme-check false positives
**Spec:** **`FNSR-RefIntegrity-Linter-Spec-R1.1.md`** (supersedes R1.0; precision edit to FR-12 + FR-18, no new capability)
**Blocking:** no — the dangling-reference core is accepted and in use; this is a Module-3 correctness fix.

---

## 1. What we did

We ran the as-built linter (the loop's 2/3-module build) over the **live merged BPO corpus** — 13
slices + `apqc-ext` + `apqc-catalog` + the capability/role layer + the delivery/participant overlay (18
modules) — the FR-18 integration check that was out of the sandbox's scope.

```
node src/ri-cli.mjs --modules ontology/slices/apqc_*_0.ttl ontology/apqc-ext.ttl \
     ontology/apqc-catalog.ttl ontology/capabilities_roles.ttl \
     ontology/delivery_processes.ttl ontology/capabilities_wiring.ttl
```

## 2. Result — the core is right; one scheme rule mis-fires

| Check | Count | Verdict |
|---|---|---|
| `dangling_ref` | **0** | ✅ **Accepted.** Referential integrity holds across the whole corpus (incl. a recent `Roadmap → RoadmapPlan` class rename and 12 new participant classes — all resolve cross-module). The `collect`+`resolve` composition and the N3.js parser swap (your judge catching the lexical-tokenizer unsoundness, FR-3) are exactly right. **Do not touch Modules 1–2.** |
| `scheme_violation` · `capability-as-process` | **39** | ✅ **Exactly the baseline** — the genuine capabilities-wearing-process-IRIs (slices 8–13). Correct. |
| `scheme_violation` · `pcf-without-P-iri` | **1,921** | ❌ **All false positives** — every catalog `ex:PCF_<id>` node. |

Root cause: catalog nodes are `owl:NamedIndividual`s (`skos:Concept` + Descriptive ICE) that use the
**correct** `ex:PCF_<pcfID>` catalog scheme, but they carry `ex:pcfID` and aren't `⊑ cco:ont00000568`,
so they trip the literal `pcf-without-P-iri` rule. This was partly a spec gap (R1.0 FR-12 said
"a declared ex: *class*" without explicitly exempting the catalog individual scheme); **R1.1 fixes the
spec**, and this request asks for the matching build fix.

## 3. The ask (Module 3 only)

Rebuild `flag_extra` (the scheme checks in `ri-resolve.mjs`, fed by `ri-collect.mjs`) to **R1.1 FR-12**:
**both scheme rules apply only to subjects typed `owl:Class`.** Concretely:

1. **`collect`** — record, per declared subject in `classInfo`, whether it is an `owl:Class` (vs
   `owl:NamedIndividual` / `skos:Concept`). N3.js already gives you the `rdf:type` triples; add an
   `isClass` boolean.
2. **`resolve`** — gate *both* `capability-as-process` and `pcf-without-P-iri` on `info.isClass`. A
   subject that is not an `owl:Class` is **never** a `scheme_violation` (this exempts the 1,921 catalog
   `ex:PCF_<id>` individuals; the `dangling_ref` logic is unchanged).

No change to the dangling-ref core, the CLI, or the output format.

## 4. Acceptance (FR-18, R1.1)

Over the live corpus the rebuilt linter **MUST** report exactly:

```
dangling_ref            0
readable_label          0
capability-as-process  39
pcf-without-P-iri       0
exit code               1   (the 39 are real findings, surfaced until resolved/waived)
```

Plus the existing **FR-17 two-file dirty fixture** continues to pass, and the **50 dangling-ref
assertions** (`node test/ri-run.mjs`) stay green (FR-13 regression: the scheme edit must not break the
core).

## 5. Note on Module 3's other half (FR-11 `readable_label`)

Your README flags `readable_label` (the ported CCO-label diagnostic) as deferred. It's **optional** for
this fix (it only fires with a `--register`, and the corpus is already CCO-clean — 0). Land it when the
edit-module generation is stable; it is **not** on the critical path for the FR-18 baseline.

---

*Once §3 lands and §4 passes, we wire `ri-cli.mjs` into the BPO validation harness as **Gate F** (after
Gate B), and the FR-18 counts above become the standing referential-integrity + scheme regression gate.
Thanks — the dangling-ref leg is genuinely the piece nothing else in our pipeline had.*
