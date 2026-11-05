# Communications

The record of what this repository has said to, and heard from, the teams it depends on
or that depend on it.

This record follows the communications protocol, version 1.1:
Skreen5hot/communications, PROTOCOL.md at 05068d800506bae6bbf66f6cb11d4eccc6adb312, sha256
fb3a06309eb5ecd5920a7737789df524000e5447f86c008ec16fee6203d9d74d.

That file is the protocol: what a message is, the rules, team codes, and how messages are
announced on the board (the Discussions of `Skreen5hot/communications`). It is not
repeated here. Until 2026-11-05 this record followed the BCO's copy of the template's
protocol (BCO `communications/README.md` at `ba953ce`). Every message recorded under it
satisfies 1.1.

```text
communications/
  README.md                 this file
  <team>/README.md          who the team is and where its repository lives
  <team>/incoming/          messages received, copied verbatim with their source
  <team>/outgoing/          messages sent
```

## Teams

This repository's code is **BPO**. It corresponds with **BCO** (Business and Agent
Capabilities Ontology), which vendors this repository's act genera, and **BPOT** (BPO
Template Port), which ports this repository onto the Ontology Template. Codes are those
of `correspondents.yaml` in the communications repository.

## This record's own rules

These add to the protocol and do not change it.

1. **The checker.** `python scripts/communications.py` checks every message against the
   protocol and lists the threads still open. It is the BCO's `tools/communications.py`
   with this repository's identity, and it follows renames (protocol Rule 1).
2. **Decisions** (protocol Rule 4) are recorded in `docs/adr/`, citing the message by id.
3. **Line endings.** `.gitattributes` keeps this folder byte for byte
   (`communications/** -text`, protocol Rule 7).
4. **Sending.** A message is committed and pushed, then announced with the communications
   repository's `tools/alert.py` (protocol § Alerts). An agent working here checks for
   waiting messages when its session starts, from a clone of that repository:
   `python tools/inbox.py --code BPO --record <this repository>/communications`.
5. **Adding a team.** Create `communications/<team>/README.md` with a header naming the
   team and its repository (see `bco/README.md`), and add the team's code to `TEAMS` in
   `scripts/communications.py`.
