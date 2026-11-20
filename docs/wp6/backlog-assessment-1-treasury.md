# Capability-as-process backlog: assessment 1, the eight the BCO depends on

2026-11-18. The first per-class assessment of the 37-class backlog
(`capability-as-process-backlog.md`), for the BPO architect to decide. **Nothing here
changes the ontology.** Each row is a proposal.

**Why these eight first.** The BCO's Q12 inquiry (`BCO-BPO-2026-11-15-q12-capability-typing-inquiry`)
names eight BCO concepts that are blocked because their only act evidence is one of these
classes. They are the classes where an assessment has a consumer waiting.

## The test

Decision A (2026-11-03) is the precedent: P11035 and P11036 became acts. The test asks
two questions of each APQC row.

- **Is what the row names performed, or borne?** If it is a performed activity, the class
  is an act. That holds even when the activity is an ongoing programme with no natural
  end. Its standing capacity, if needed, is a separate continuant.
- **Is it a standing function?** A row that names a capacity or condition, not an
  activity, stays a capability.

None of the eight rows has child rows in the PCF. The APQC text for each describes doing
something: maintaining, handling, delaying, utilizing.
**All eight pass as performed activities.** What needs the architect's judgment is the
genus.

**Facts that hold for all eight:**

- **No capability wiring.** None is the subject or target of `bpo:enablesProcess`, none is
  in `capability_scope.json` or `b8_pairs.tsv`, and none has a `*Capability` twin. Retyping
  is self-contained.
- **P10788 is the exception.** It carries one `obo:BFO_0000054` (realized in) restriction,
  to P10741. Under decision A that restriction goes when the class becomes an act.
- **Each definition says "is realized in".** That is the same over-claim B8 corrected for
  the `*Capability` classes. It is moot once the class becomes an act: the definition is
  rewritten under the act genus, as for P11035.

## Proposals

| Class | APQC row | Proposed genus | Confidence | Reasoning and precedent |
|---|---|---|---|---|
| P10899 | 9.7.2.7 Manage and oversee banking relationships | `bpo:ActOfRelationshipManagement` | **high** | The genus's definition, "builds, maintains … an ongoing relationship between an organization and one or more external parties". It is decision A's exact case: P11035 is lender relations |
| P10908 | 9.7.4.2 Manage financial intermediary relationships | `bpo:ActOfRelationshipManagement` | **high** | As P10899. APQC: "maintaining smooth relations with financial investment banks" |
| P16958 | 9.7.6 Manage financial fraud/dispute cases | `bpo:ActOfResolution` | **high** | The genus's definition, "settles a raised case … comprising as needed the receipt, investigation, decision, and closure". APQC: "handling cases … resolve disputes" |
| P10788 | 9.1.4.7 Manage continuous cost improvement | `bpo:ActOfImprovement` | **high** | The genus's definition, "modifies an existing process, system, or capability with the intent of raising its performance". APQC: "conducting activities to improve cost distribution regularly". **Also:** its label, "Continuous Cost Improvement Capability", names the capability, not the APQC row. Restore the APQC name, as the backlog's triage flagged |
| P10894 | 9.7.2.2 Manage cash equivalents | `bpo:ActOfFinancialTransaction` | medium | APQC: "utilize short-term assets … marketable securities, commercial paper … treasury bills". These are Financial Instruments used as an investment, which is the genus's definition (`cco:ont00000836`, Act of Financial Instrument Use, verified). Precedent: 9.7.5.4.3 "Manage customer collateral" is `ActOfFinancialTransaction` |
| P10909 | 9.7.4.3 Manage liquidity | `bpo:ActOfFinancialTransaction` | medium | "Maintaining enough liquidity in form of cash and cash equivalents" is done by moving funds between cash and equivalents, an exchange of Financial Instruments. Alternative: `bpo:ActOfAdministration`, if liquidity is read as carrying out a liquidity policy. APQC names no policy, so the transaction reading is closer to the text |
| P10910 | 9.7.4.4 Manage issuer exposure | `bpo:ActOfMonitoring` | medium | "Managing the exposure incurred … for providing credit" is tracking an exposure against limits. Precedent: 9.7.5.3.5 "Manage foreign exchange balance sheet risk" and 9.7.5.2.1 are `ActOfMonitoring`, and 9.7.5.5.5 "Monitor credit" is too. Under the GOLDEN PRINCIPLE the output is a Descriptive ICE (`853`), the exposure status |
| P10897 | 9.7.2.5 Manage cash flows | **open: the architect's choice** | low | APQC: "delaying the outflow of funds … encourage the inflow". Two readings. (a) `bpo:ActOfScheduling`: fixing *when* payments and collections happen produces a schedule, a Directive ICE (`965`). (b) `bpo:ActOfFinancialTransaction`: the payments and collections themselves. The text is about timing, not the transfers, which favours (a). But "Develop cash flow forecasts" is a sibling row (9.7.2.4, `cco:ont00000371`), so the planning reading must not duplicate it |

## What a decision changes

For each class decided as an act, following decision A:

1. Its parent changes from `cco:ont00000568` to the genus. The genus's allowlisted anchor
   carries SHACL S2.
2. A new definition is written under the genus, with a decision comment. Its earlier
   comment is kept as history.
3. P10788 also loses its `obo:BFO_0000054` restriction and gets back its APQC label.
4. Gate F's `BASELINE` drops by one per class, from 37 down to 29 if all eight are decided.
   `docs/wp6/capability-as-process-backlog.tsv` and the migration record are updated in
   the same commit.
5. The BCO gets a `notice`, as our Q12 answer promised. Its eight blocked concepts then
   have act evidence. Admission is still the BCO's own review.

**Not settled by this:** the ADR-001 R5/R6 amendment. It follows the assessments. These
eight would be its first evidence after decision A: all eight are "Manage …" rows, the
most common pattern in the backlog (29 of 37).

## Decided (BPO architect, 2026-11-20)

All eight are acts, with the proposed genera:

- the four high-confidence rows as proposed;
- the three medium-confidence rows as proposed, with liquidity as Financial Transaction,
  not Administration;
- P10897 as `bpo:ActOfScheduling`.

What was applied, in `apqc_9_0.ttl`:

- **Each class** was given its new parent and a definition under the genus. The decision
  comment comes first, and the earlier comment is kept after it as history.
- **P10788** got back the APQC name, "Manage continuous cost improvement", and lost its
  realized-in restriction.
- **Four genera were inlined** from `apqc-ext.ttl`: Relationship Management, Resolution,
  Improvement and Scheduling.
- **Gate F's baseline** went from 37 to 29, and the eight rows left the backlog TSV.

The BCO receives a `notice`.
