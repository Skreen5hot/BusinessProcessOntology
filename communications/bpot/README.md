---
team: BPOT
name: BPO Template Port
repository: https://github.com/Skreen5hot/BPO-Template-Port
---

# BPOT

The port of BPO onto the Ontology Template, run as a test of the template. It ports BPO
with `tools/port_from_bpo.py` from a named BPO commit, and measures the result (WP6:
S0 is BPO at `bc64e91` ported unchanged; S2 is BPO with its own corrections made).

**What this means for work here:**

- **The port carries PCF material**, so it carries APQC's notice too (ADR-003 L1, L5). It
  takes the notice text from this repository's `NOTICE.md`.
- **Phase B asks for BPO's decisions** on findings B1 to B18 of the port's evaluation, and
  for the one BPO commit S2 is ported from. Decisions are recorded in `docs/adr/`.
