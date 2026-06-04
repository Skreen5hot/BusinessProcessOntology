# PHASE 1 — Capability / Role Module & the Process→Agent Dispatch Bridge

Status: **v0.1.0 seed built and validated** (`capabilities/`), full build not started.
Audience: the next session, which will build the **daemon** that generalizes the seed to the
whole corpus. Read alongside `CLAUDE.md` (project grounding), `apqc_to_bfo_cco_methodology.md`
(spec; §8.1 granularity, §8.8 gates, §16.12 permission conflicts), and `RELEASE_NOTES.md` (v0.3.0).

The v0.3.0 reality layer answers *"what work is done."* Phase 1 answers *"who can do it, in what
capacity, and may they."* It is the bridge from a **process** universal to the **agent** that
performs it — the layer a dispatcher reads to route work and to find coverage gaps **before**
runtime instead of during it.

---

## 1. The governing distinction — Capability ≠ Role ≠ Process

This is the whole foundation, and BFO makes it precise. All three are kept ontologically distinct:

| | What it answers | BFO/CCO grounding | Practical force |
|---|---|---|---|
| **Capability** | *Can this agent do this kind of work?* | `cco:ont00001379` Agent Capability — a **realizable entity** grounded in the agent's own constitution (`⊑ obo:BFO_0000017`) | **Hard feasibility filter** for dispatch |
| **Role** | *In what capacity is it acting?* | `obo:BFO_0000023` Role — a **position** the agent occupies, externally/relationally grounded | **Framing + authority** — the authority is where the **deontic** layer attaches |
| **Process** | *What is being done?* | a BFO process universal (the v0.3.0 reality layer) | the action itself — **borne by** the agent, not the same as cap/role |

The seam that matters: **collapsing capability and role into one "can-do" tag loses where
permission lives.** Capability is competence (constitution); role is position (relation), and
permission rides on the role's authority. Keep them separate or the deontic hook has nowhere to
attach.

## 2. Well-formed criteria

**A capability** — names a *competence*, not a task or an output (✗ "produce competitor analysis";
✓ "competitive analysis capability"); reaches `cco:ont00001379` by `subClassOf*`; carries a
`skos:definition`; declares scope via `ex:enablesProcess` (the process types it realizes).

**A role** — names a *position*; reaches `obo:BFO_0000023`; and per **reuse-before-mint** anchors
on the CCO role taxonomy rather than bare `BFO_0000023`:
- occupation roles (analyst, planner, strategist) → `cco:ont00000984` **Occupation Role**;
- approver / gate authority → `cco:ont00000187` **Authority Role** (this is where permissions bind).

(Both CCO role classes verified ⊑ `BFO_0000023`.)

## 3. Granularity is the decomposition stop-condition (not free choice)

A capability is exactly the **coherent bundle one agent can plausibly own** — which methodology
**§8.1** already defines as *where process decomposition stops*. Too fine (one capability per
process) and the registry explodes; too coarse and matching under-qualifies. **The granularity
decision and the decomposition-stop decision are the same decision** — derive capability
boundaries from the §8.1 stop nodes, do not re-litigate them.

## 4. Matching semantics — species satisfies genus

The bridge logic. An agent bearing capability `C_a` satisfies a process requirement `C_p` **iff
`C_a rdfs:subClassOf* C_p`** — a more specific borne competence satisfies a more general
requirement (a competitor-identification capability satisfies a requirement for the broader
analysis capability, because the species *is-a* the genus). Therefore:

- author `ex:requiresCapability` **at the precise level the process needs**;
- agents declare the **specific** capabilities they hold;
- **specialization rolls up** — the registry matcher closes the gap.

Roles match identically. This resolves the apparent inconsistency in the old spec example, and the
matchability test confirmed it end to end.

---

## 5. What exists now — the v0.1.0 seed (`capabilities/`)

Three artifacts, validated (parses; all CCO/BFO anchors independently re-verified against the
2024-11 closure):

**`capabilities_roles.ttl`** — two marker genera + reused CCO anchors:
- `ex:Capability ⊑ cco:ont00001379` (Agent Capability); `ex:Role ⊑ obo:BFO_0000023` (Role).
- two module-local **annotation** properties: `ex:enablesProcess` (capability → process it realizes;
  the operational **inverse** of `requiresCapability`, BFO-grounded in *has realization*) and
  `ex:bearsPermission` (role → `cco:ont00000751` Action Permission — the **deontic hook**).
- worked examples wiring real cases: `CompetitiveAnalysisCapability` → P19945/P10021;
  `StrategicPlanningCapability` → P10037/P10045; `PlanAuthoringCapability` → AuthorRoadmap /
  AuthorImplementationPlan; roles `MarketAnalystRole`/`StrategistRole`/`PlannerRole` (Occupation),
  `ApproverRole` (Authority) bearing an `ApproveImplementationPlanPermission` **stub**.

**`capabilities_roles_shapes.ttl`** — 7 shapes, run with CCO+BFO in the data graph (transitive
`subClassOf` needs the closure):
- structural C1–C4: capability reaches `1379` + has label/definition; role reaches `BFO_0000023`
  + label/definition; **capability ⟂ role** (no class reaches both anchors); `bearsPermission`
  targets an Action Permission.
- coherence C5–C7: `requiresCapability` → reaches `1379`; `requiresRole` → reaches `BFO_0000023`;
  `requiresPermission` → reaches `751`. (These fire only once processes carry the `requires*`
  triples — today none do.)

**`agents.json`** — the fleet registry (2 agents): `market_analysis.v1`
(CompetitiveAnalysisCapability + MarketAnalystRole), `planner.v1` (PlanAuthoringCapability +
PlannerRole).

## 6. Fit with the existing corpus — two findings that shape the build

**(a) The capability hierarchies unify cleanly.** The 111 slice capabilities are
`⊑ cco:ont00000568` Organization Capability, and **`568 ⊑ 1379`** — so they already reach Agent
Capability. The new `ex:Capability (⊑ 1379)` is the umbrella; the dispatch "reaches 1379" test is
satisfied by *both* an individual-agent competence and a slice Organization Capability. No
conflict — but the build must decide whether slice org-capabilities are **re-homed** under
`ex:Capability` (so the marker is universal) or left at `568` and matched purely by the
`subClassOf* 1379` test (so slices stay untouched). Recommended: the latter — leave the
v0.3.0 slices alone; match on "reaches 1379."

**(b) Two process sources, and one of them has no home.** `enablesProcess`/`requiresCapability`
point at process classes from **two** origins: APQC slice processes (P19945/P10021/P10037/P10045 —
all confirmed in `apqc_1_0.ttl`) **and** the daemon's own **delivery-process universals**
(`AuthorRoadmap`, `AuthorImplementationPlan`, the agile-loop processes from spec §8) — which **do
not exist anywhere in the corpus yet** (grep-confirmed). The build must give them a home (a small
`delivery_processes.ttl` under BFO process / the appropriate CCO Planned-Act anchors) or those
references dangle.

**(c) Self-containment interaction.** The v0.3.0 slices are deliberately self-contained (no
`owl:imports`) and Gate C validates each slice **without CCO merged** (relying on each slice's
`CCO SUPERCLASS BRIDGES` block). The capability module is a **new shared layer**. Decide up front:
is it a standalone module merged only at corpus-check + dispatch time (preserves slice
self-containment — recommended), and do its shapes run with CCO loaded (the seed shapes already
assume this)? This is the analogue of the registry-vs-self-containment tension already noted in
`CLAUDE.md`.

## 7. Test criteria — three families, all demonstrated on the seed

1. **Structural SHACL** (module alone, CCO loaded) — C1–C4 above. Clean run conformed; a broken
   fixture produced **exactly three** violations: a role-as-capability mis-wire, an orphan
   capability missing its anchor, and an orphan missing its definition.
2. **Coherence SHACL** (process graph loaded) — C5–C7: each `requires*` points at the right *kind*
   of class. This is the check that catches the most likely real error — pointing
   `requiresCapability` at a **role**.
3. **Matchability** (NOT SHACL — a registry routability check; enforces spec routability point 7).
   For each process requirement, does any agent in `agents.json` bear a **satisfying** capability
   *and* role (species-satisfies-genus, `subClassOf*`)? The seed run showed **P19945** and
   **AuthorImplementationPlan routable**, and **P10037 unmatchable** — correctly flagging that no
   agent yet bears strategic-planning competence. This is the test that surfaces **fleet coverage
   gaps before runtime.**

## 8. Boundaries & open decisions (decide before/early in the build)

- **`permissions.ttl` is RDM/IEE's to author.** The actual Action Permission classes — and
  **conflict resolution between competing permissions at a gate (§16.12)** — belong to that layer,
  not here. The seed stubs one permission only to show the role→permission seam. Do not author the
  permission catalogue in this phase; keep the seam, leave the content.
- **`enablesProcess` vs `requiresCapability` — authoring direction.** `enablesProcess` is currently
  authoring/coherence metadata (capability→process). If the daemon should **derive**
  `requiresCapability` (process→capability) from it rather than hand-author both directions, that
  inversion is a small, deliberate decision — pick **one** authored direction and generate the
  other, so the two never drift.
- **Consolidation** of the 10 recurring slice roles/capabilities (e.g. `CustomerRole` in 7 slices)
  to one canonical definition each — same harmonization discipline that keeps the corpus
  ELK-consistent.
- **Marker re-homing** (§6a) and **delivery-process home** (§6b) and **module/self-containment**
  (§6c) — settle these three before the daemon writes at scale.

---

## 9. DIRECTIONS FOR THE NEW SESSION — build the capability/role daemon

**Objective.** A daemon that generalizes the v0.1.0 seed into the **full** capability/role registry
across all 13 APQC sections plus the delivery-process universals — wiring `requiresCapability` /
`requiresRole` (/ `requiresPermission` seam) onto process classes, declaring the agent fleet, and
proving routability — every artifact validating under the three test families above.

**Pattern to reuse.** Follow the per-section, per-commit cadence of the v0.3.0 build
(`scripts/section_transform.workflow.js`, `scripts/stage_section.py`) and the verify-before-assert
+ validate-then-commit workflow (`CLAUDE.md`). Each section's capability/role output is built,
validated, and committed on its own.

**Daemon steps (per section, then corpus-wide):**
1. **Promote the seed.** Move `capabilities_roles.ttl` + `capabilities_roles_shapes.ttl` into
   `ontology/`; define the three real object properties `ex:requiresCapability` / `ex:requiresRole`
   / `ex:requiresPermission` (currently only referenced by the shapes); add a
   `delivery_processes.ttl` home for `AuthorRoadmap`/`AuthorImplementationPlan`/the §8 loop.
2. **Harvest + dedup.** Pull the 111 `*Capability` and 87 `*Role` classes already declared in the
   slices; reconcile the 10 cross-slice recurrences to one canonical definition each; double-anchor
   roles on Occupation/Authority Role; leave slice anchors at `568`/`984`/`187` (match on
   "reaches 1379 / reaches BFO_0000023").
3. **Set granularity from §8.1.** Derive each capability as the coherent bundle at a process
   decomposition-stop node — do not invent a parallel granularity.
4. **Wire scope.** Author **one** direction (recommend `enablesProcess` on the capability) and
   **derive** the inverse `requiresCapability` onto the process classes; same for roles. Keep the
   `requiresPermission` seam present but unpopulated (RDM/IEE owns the content).
5. **Declare the fleet.** Grow `agents.json` to the agents the dispatcher actually has; each
   declares the **specific** capabilities/roles it bears.
6. **Validate (the daemon's gates, all three families):**
   - structural C1–C4 and coherence C5–C7 — **zero violations**, CCO+BFO loaded;
   - **matchability** — every authored `requires*` is routable to ≥1 agent, OR the unmatched
     requirements are emitted as an explicit **coverage-gap report** (a deliverable, not a failure);
   - **corpus regression** — `bash scripts/corpus_check.sh` still **EXIT 0** (the capability module
     must not perturb the v0.3.0 ELK consistency).
   Wire C1–C7 into the validation harness (extend `src/apqc_transform/validate.py` or add a Gate E),
   and add a `scripts/matchability.py` that reads the registry + `agents.json`.
7. **Commit per section** with the project's message convention; keep one-shot fix scripts as
   `scripts/_fix*.py` (run, delete).

**Definition of done (phase):** the full capability/role registry + delivery processes parse and
resolve; structural + coherence shapes are zero-violation; the matchability report routes every
`requires*` or lists the gaps explicitly; corpus ELK stays EXIT 0; the `requiresPermission` seam is
in place for RDM/IEE to populate later.

**Settle first (gating decisions, §6 + §8):** (i) leave slice org-capabilities at `568` and match
on `subClassOf* 1379` vs re-home under `ex:Capability`; (ii) `enablesProcess`→`requiresCapability`
derivation direction; (iii) where delivery-process universals live; (iv) capability module as a
corpus-merge-only shared layer that preserves slice self-containment. These four shape everything
downstream — decide them before the daemon writes at scale.
