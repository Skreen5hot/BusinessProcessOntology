# Communications

The record of what this repository has said to, and heard from, the teams it depends on
or that depend on it. One folder per team; inside it, `incoming/` and `outgoing/`.

```text
communications/
  README.md                 this protocol
  <team>/README.md          who the team is and where its repository lives
  <team>/incoming/          messages received, copied verbatim with their source
  <team>/outgoing/          messages sent
```

Teams today: **BCO** (Business and Agent Capabilities Ontology), which vendors this
repository's act genera.

This protocol is the BCO's (`communications/README.md` in that repository, commit
`ba953ce`), adopted unchanged so the two records can cite each other.
`python scripts/communications.py` checks every message against it and lists the threads
still open; it is the BCO's `tools/communications.py` with this repository's identity.
Line endings in this folder are never converted (`.gitattributes`), because incoming
bodies are checked by digest.

---

## A message

One Markdown file: a YAML header between `---` lines, then the body.

**Filename** — `YYYY-MM-DD-<slug>.md`, the date the message was sent or received, and a
short lowercase slug (`a-z`, `0-9`, `-`). The folder says the team and the direction.

**Header**

```yaml
---
id: BPO-BCO-2026-10-23-vendoring-pin-ack   # <FROM>-<TO>-<date>-<slug>; must match the path
from: BPO
to: BCO
date: 2026-10-23                            # must match the filename
type: acknowledgment                        # request | finding | answer | notice | acknowledgment
subject: One line, what this is about
in_reply_to: BCO-BPO-2026-10-23-vendoring-pin   # the id of the message this answers, or null
refs:                                       # what the message is about, bound by digest
  - repo: Skreen5hot/BusinessProcessOntology
    commit: 66131945b525c54f44e4962f32bb1f52dfa0cd12
    path: ontology/apqc-ext.ttl
    sha256: 1b9a9375cb7303003556004effd712b63913d6aa4935dbf604a653aec65cab4b
author: Aaron Damiano                       # a person, or an agent named as an agent
requires_act: false                         # true when only the architect can answer it
---
```

Incoming messages carry one more field, `source`, saying where the original lives:

```yaml
source:
  repo: Skreen5hot/Business-and-Agent-Capabilities-Ontology
  commit: <the commit the original was read at>
  path: <its path there>
  sha256: <SHA-256 of the original file's bytes>
```

and the body below the header is that original, byte for byte. The checker recomputes the
digest of the body and requires it to equal `source.sha256`, so a copy that has been
"tidied" fails rather than quietly standing in for what was sent.

## Rules

1. **A committed message never changes.** A correction is a new message whose `in_reply_to`
   names the one it corrects. The checker reads git history and refuses a message file
   that more than one commit has touched.
2. **Status is derived, not written.** A `request` or `finding` is *open* until a later
   message answers it (`in_reply_to` its id) with type `answer` or `acknowledgment`.
3. **Every ref is digest-bound.** A ref into this repository is recomputed from
   `git show <commit>:<path>`; a ref into another repository is checked for shape here.
4. **A message is not a decision.** It can ask for one (`requires_act: true`). The decision
   itself is the architect's and is recorded in `docs/adr/`, citing the message by id.
5. **Agents are named as agents.** A message drafted by an agent says so in `author`, and
   whose direction it was drafted at.
6. **Sending is outside the repository.** An outgoing message here is the record of what
   was said; the record does not claim delivery.

## Adding a team

Create `communications/<team>/README.md` with a header naming the team and its repository
(see `bco/README.md`), and add the team's code to `TEAMS` in `scripts/communications.py`.
