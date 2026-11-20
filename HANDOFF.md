# Handoff: paused 2026-11-20

For the next session, agent or person. It records where BPO stands, what is open, and what
to do first. `CLAUDE.md` has the standing rules and `PHASE1.md` the capability bridge.
This file supersedes the "current phase" framing of both.

## Where things stand

**BPO `main`** is at `a162fc0`, or later if anything follows this file. All gates passed
on it:

- Gates A–D on every slice;
- the corpus ELK run, EXIT 0;
- Gate F at baseline **29**;
- C1–C7 with no violations.

What changed since v0.4.1:

- **WP6 corrections merged** (`2867cd4`, a merge commit, so the S2 source `2b86c91` is in
  `main`'s history). That brought in B1–B18 as the architect decided them; decision A
  (P11035 and P11036 are acts); B8 (capability requirements are no longer derived from
  every enabled pair, and realization definitions say "can be realized"); and the CCO pin
  checked by digest. The branch `wp6-s2-corrections` is kept. Don't delete it.
- **`SeniorManagementRole`**: its definition and parent are restored beside
  `owl:deprecated` (`313b536`).
- **Backlog decision 1** (BPO architect, 2026-11-20; `b8f4eb5`): eight slice-9 classes
  are now acts. The reasoning is in `docs/wp6/backlog-assessment-1-treasury.md`.

**WP6, the template evaluation, is closed** (template decision 30, 2026-11-05). The evidence
is in `Skreen5hot/BPO-Template-Port`, tag `wp6-final`. Port `main` (`7694408`) now carries
WP6. Its Checks suite has 395 passed and 1 failed, a template-owned test (see "Open" below).
The port repository is **public**.

## Open

| Item | Owner | Next step |
|---|---|---|
| **Capability-as-process backlog: 29 classes** (`docs/wp6/capability-as-process-backlog.tsv`) | BPO architect | Assess the rest the way assessment 1 did. The test is decision A's: a performed activity is an act, even an ongoing one. The genus is the architect's call, offered as grouped proposals with a confidence each |
| **ADR-001 R5/R6 amendment** | BPO architect | Draft it once the assessments are done; R5 conflates "no natural end" with "borne, not performed". The backlog `.md` sets out the issue |
| **PCF 10735, 10736, 14008** have no act class | BPO architect | Take with the R5/R6 amendment. The BCO is waiting on 2 concepts here |
| **BCO promise** | BPO | Send a `notice` to the BCO whenever a backlog class is retyped, as our Q12 answer promised |
| **Template finding** `BPOT-EXAMPLE-2026-11-20-template-test-assumes-gitattributes` (communications Discussion #19) | Template Team | Wait. Don't edit the template's test in the port. Record their answer when it comes |
| **11 co-parent advisories** in `consistency_audit.py` | — | Not blocking, and older than WP6 |
| **WP6 recommendations still open** (port `research/wp6/phase-b/quality-evaluation.md` §7): authorship of BPO-written definitions (K01, 1,291); whether to keep the co-asserted allowlist parents or merge CCO in SHACL | BPO architect | Next cycle |
| **Option B: move BPO itself onto the template** (not started; the architect chose not to before the pause) | BPO architect | If taken up: keep the `bpo:` namespace (the BCO vendors it, ADR-002); re-port from current `main`; upgrade the port from template v0.1.0 to current; carry BPO's gates over; write an ADR; notify the BCO |
| Phase 1 leftovers: `requiresPermission` with the RDM/IEE permission catalogue; 6 capabilities with no scopeable process; a real agent roster | — | Unscheduled |

## Communications

Records follow `Skreen5hot/communications` `PROTOCOL.md`; this record pins v1.1, and v1.2
adds only registration. See `communications/README.md`. Messages are announced on that
repository's Discussions board.

- **At session start**, check for waiting messages in both of these places. The board
  misses messages that were never announced; two were found late that way.
  1. From a clone of `Skreen5hot/communications`, run
     `python tools/inbox.py --code BPO --record <BPO>/communications`, and `--code BPOT`
     for the port's record.
  2. List the senders' outgoing folders with `gh api` and compare them with our
     `incoming/`:
     - BCO: `communications/bpo/outgoing/`;
     - Ontology Template: `communications/bpotest/outgoing/`.
- **Recording** a waiting message: `python scripts/record_incoming.py REPO COMMIT PATH OUT
  [field=value ...]` writes the verbatim copy with its `source` block. In the port's
  record, remap the template's `BPOTEST` to `BPOT` in `id`, `to` and `in_reply_to`.
- **Sending**: commit and push the message, then run `python tools/alert.py <msg> --post`
  from the communications clone. Use `--new-thread` for a reply to a message that was
  never announced.
- **Standing approval** (the architect, 2026-11-17): act on messages with your own
  judgment. Ask only before something irreversible. An answer reports decisions already
  recorded; it does not make new ones.

## Working environment (Windows, OneDrive)

- **Never `git stash`, and never switch branches** in the OneDrive checkouts: OneDrive
  wipes the index. Work in a worktree outside OneDrive, for example
  `git worktree add C:\Users\aaron\wt-x origin/main -b x`. Remove it afterwards; the
  stubs left under `.git/worktrees` can't be deleted and are harmless.
- **Gitignored inputs**: `vendor/cco/CommonCoreOntologiesMerged.ttl` (sha256 `e609db27…`)
  and `tools/robot.jar`. Copy them into a new worktree.
- **`corpus_check.sh` takes 10–15 minutes.** Gate F (node) can time out at 900 s under
  load. A timeout is not a pass: rerun it.
- **The port's measurement environment** is `C:\Users\aaron\venvs\wp6-venv010`, Python
  3.12.10, with the pins of the port's `research/wp6/measure/*/manifest.tsv`. The port's
  own `.venv` is stale. Don't keep environments in the temp folder; cleanup broke one.
- **Commits**: one topic per commit, validated first, ending with a `Co-Authored-By:`
  line naming the model used. Pushing directly to `main` is fine. Never push to
  `Skreen5hot/Ontology-Template` or the FNSR repositories.
