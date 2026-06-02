"""Deterministic catalog-layer generator (ADR-001 R1).

Emits `ontology/apqc-catalog.ttl`: every PCF row as a catalog node -- an
individual that is both a Descriptive ICE (cco:ont00000853) and a skos:Concept
in the apqc:PCF scheme. The dotted hierarchy becomes skos:broader, declared
explicitly CURATORIAL (not parthood, R7). No ontological judgement is applied
here; the output is a pure function of the PCF export, so it is fully
reproducible and needs no third-party dependencies.

Catalog nodes use a DISTINCT IRI (ex:PCF_<pcfID>) from the reality-layer
process classes (ex:P<pcfID>); the two are linked later by the
ex:designatesProcessType bridge (R4), which this generator does NOT emit.
"""

from __future__ import annotations

from pathlib import Path

from . import config, pcf_export
from .pcf_export import PcfRow

EX = config.EX
APQC = config.NS["apqc"]


def catalog_iri(pcf_id: str) -> str:
    return f"{EX}PCF_{pcf_id}"


def _esc(text: str) -> str:
    """Escape for a Turtle long-string literal (\"\"\"...\"\"\")."""
    return (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )


def _lit(text: str) -> str:
    return f'"""{_esc(text)}"""'


_HEADER = f"""\
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix dct:   <http://purl.org/dc/terms/> .
@prefix cco:   <https://www.commoncoreontologies.org/> .
@prefix ex:    <{EX}> .
@prefix apqc:  <{APQC}> .

####################################################################
# APQC PCF -> CATALOG LAYER  (GENERATED -- do not hand-edit)
#
# ADR-001 R1: every PCF row, all levels, as a catalog node.
#   node a owl:NamedIndividual, cco:ont00000853 (Descriptive ICE), skos:Concept
#   skos:inScheme apqc:PCF ; prefLabel ; ex:pcfID/hierarchyID/apqcSourceText
#   dotted hierarchy -> skos:broader  (CURATORIAL relation, NOT parthood; R7)
#
# Regenerate:  python -m src.apqc_transform.catalog
# CCO pin: {config.CCO_VERSION} ({config.CCO_RELEASE_DATE})
####################################################################

<{APQC.rstrip('#')}> a owl:Ontology ;
    dct:title "APQC PCF Catalog Layer" ;
    dct:source "APQC Process Classification Framework (Cross-Industry) v7.4" ;
    owl:versionInfo "0.1.0" ;
    rdfs:comment "Generated deterministically from the PCF export. Curatorial taxonomy only; process semantics live in the reality-layer slice modules." .

# Provenance annotation properties (mirror the reference module)
ex:pcfID a owl:AnnotationProperty ; rdfs:label "APQC PCF ID" .
ex:hierarchyID a owl:AnnotationProperty ; rdfs:label "APQC Hierarchy ID" ;
    rdfs:comment "Positional dotted-decimal locator. NON-STABLE across PCF versions." .
ex:apqcSourceText a owl:AnnotationProperty ; rdfs:label "APQC source description" .
ex:designatesProcessType a owl:AnnotationProperty ; rdfs:label "designates process type" ;
    rdfs:comment "ADR-001 R4 bridge: catalog node -> reality-layer process universal or capability. Populated during reality-layer modeling, NOT by the catalog generator." .

apqc:PCF a skos:ConceptScheme ;
    rdfs:label "APQC Process Classification Framework (Cross-Industry)" ;
    skos:prefLabel "APQC PCF Cross-Industry v7.4" .

####################################################################
# CATALOG NODES
####################################################################
"""


def render(rows: list[PcfRow]) -> str:
    by_hierarchy = {r.hierarchy_id: r for r in rows}
    parts: list[str] = [_HEADER]

    for r in sorted(rows, key=lambda x: _sortkey(x.hierarchy_id)):
        iri = f"ex:PCF_{r.pcf_id}"
        lines = [
            f"{iri} a owl:NamedIndividual, cco:ont00000853, skos:Concept ;",
            f"    skos:inScheme apqc:PCF ;",
            f"    skos:prefLabel {_lit(r.name)} ;",
            f'    ex:pcfID "{r.pcf_id}" ;',
            f'    ex:hierarchyID "{r.hierarchy_id}" ;',
            f'    rdfs:comment "APQC level: {r.level_name}" ;',
        ]
        if r.description:
            lines.append(f"    ex:apqcSourceText {_lit(r.description)} ;")
        if r.parent_hierarchy and r.parent_hierarchy in by_hierarchy:
            parent = by_hierarchy[r.parent_hierarchy]
            lines.append(f"    skos:broader ex:PCF_{parent.pcf_id} ;")
        # terminate
        lines[-1] = lines[-1].rstrip(" ;") + " ."
        parts.append("\n".join(lines))

    return "\n\n".join(parts) + "\n"


def _sortkey(hierarchy_id: str) -> tuple[int, ...]:
    return tuple(int(p) for p in hierarchy_id.split("."))


def generate(out: Path | None = None) -> tuple[Path, int]:
    out = out or config.CATALOG_TTL
    rows = pcf_export.load_rows()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rows), encoding="utf-8")
    return out, len(rows)


if __name__ == "__main__":
    path, n = generate()
    print(f"Wrote {n} catalog nodes -> {path}")
