# Notice: APQC Process Classification Framework® content

This repository contains two kinds of material, under different terms.

| Material | Terms |
|---|---|
| BPO's own work: the ontology design and BFO/CCO modelling, the act genera, the capability/role layer, the code, the tests and the documentation | MIT, see [`LICENSE`](LICENSE) |
| Material derived from the **APQC Process Classification Framework® (PCF), Cross-Industry, version 7.4**: element IDs, hierarchy IDs, element names and element descriptions | APQC's licence, whose notice is reproduced below. **The MIT licence does not cover this material.** |

## Where the PCF material is

- `K014749_APQC Process Classification Framework (PCF) - Cross-Industry - Excel Version 7.4.xlsx`:
  APQC's own Excel release, distributed unmodified with its Copyright and attribution sheet.
- `ontology/apqc-catalog.ttl`: every PCF element's ID, hierarchy ID, name and description.
- `ontology/slices/apqc_*_0.ttl` and `ontology/reference/apqc_1_1_1.ttl`: PCF element IDs,
  hierarchy IDs, names (in labels) and descriptions (`bpo:apqcSourceText`).
- `ontology/index/corpus_index.tsv`: generated from the modules above, so it carries PCF
  element IDs, names and text.
- The project website, whose pages show the same terms.
- PCF element IDs also appear inside IRIs throughout the corpus (`bpo:P<id>`, `bpo:PCF_<id>`).

Each ontology module above carries this notice in its `dct:rights` annotation, and the
website shows it in the footer of every page.

## APQC's notice

The notice below is copied verbatim from the Copyright and attribution sheet of the PCF 7.4
workbook named above. APQC's licence requires a copy of it in every copy of the PCF and in
every derivative work.

> ©2024 APQC. ALL RIGHTS RESERVED. This Process Classification Framework® (“PCF”) is the
> copyrighted intellectual property of APQC. APQC encourages the wide distribution,
> discussion, and use of the PCF for classifying and defining organizational processes.
> Accordingly, APQC hereby grants you a perpetual, worldwide, royalty-free license to use,
> copy, publish, modify, and create derivative works of the PCF, provided that all copies of
> the PCF and any derivative works contain a copy of this notice.

## Also

- **No endorsement.** The Business Process Ontology is an independent project. It is not
  produced, reviewed or endorsed by APQC.
- **Trademarks.** Process Classification Framework® and PCF are APQC's marks. They are used
  here only to identify the source.
- **Redistributing.** If you copy or adapt any file listed above, keep this notice with it.
