"""Corpus-wide pins and conventions fixed in Phase 0.

These are the Methodology Phase-0 meta-decisions (D7, D9, the CCO pin, the §6
anchors) plus ADR-001's two-layer vocabulary. Changing anything here is a
corpus-wide event; every module header records the values in force.
"""

from __future__ import annotations

from pathlib import Path

# --- Paths (repo-root relative) ---------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY_DIR = ROOT / "ontology"
SLICES_DIR = ONTOLOGY_DIR / "slices"
REPORTS_DIR = ONTOLOGY_DIR / "reports"
VENDOR_CCO = ROOT / "vendor" / "cco"
PROMPTS_DIR = ROOT / "prompts"
ROBOT_JAR = ROOT / "tools" / "robot.jar"   # Gate D reasoner (bundles ELK)
REASONER = "ELK"

CATALOG_TTL = ONTOLOGY_DIR / "apqc-catalog.ttl"
EXT_TTL = ONTOLOGY_DIR / "apqc-ext.ttl"
SHAPES_TTL = ONTOLOGY_DIR / "apqc_shapes.ttl"
BAD_EXAMPLES_TTL = ONTOLOGY_DIR / "apqc_bad_examples.ttl"
STATE_JSON = REPORTS_DIR / "state.json"

# The PCF source export (xlsx). Glob so a version bump does not break the path.
PCF_XLSX_GLOB = "*Process Classification Framework*Cross-Industry*.xlsx"

# --- Pinned dependency (Gate B / Gate D run against this closure) ------------
CCO_VERSION = "2.0"
CCO_RELEASE_DATE = "2024-11-06"
CCO_VERSION_IRI = (
    "https://www.commoncoreontologies.org/2024-11-06/CommonCoreOntologiesMerged"
)

# --- Namespaces (D7 IRI scheme; ex: is a placeholder base, see PHASE0 §9) ----
NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dct": "http://purl.org/dc/terms/",
    "obo": "http://purl.obolibrary.org/obo/",
    "cco": "https://www.commoncoreontologies.org/",
    "ex": "http://example.org/apqc#",
    "apqc": "http://example.org/apqc/scheme#",  # the skos:ConceptScheme
}
EX = NS["ex"]


def class_iri(pcf_id: str) -> str:
    """D7: primary IRI anchored to the stable PCF ID, never the Hierarchy ID."""
    return f"{EX}P{pcf_id}"


# --- Verified CCO terms (§6 table; verify-before-assert already done) --------
CCO = {
    # properties
    "has_input": "cco:ont00001921",
    "has_output": "cco:ont00001986",
    "has_process_part": "cco:ont00001777",
    "is_about": "cco:ont00001808",
    "has_capability": "cco:ont00001954",
    # classes
    "ICE": "cco:ont00000958",
    "Descriptive_ICE": "cco:ont00000853",
    "Directive_ICE": "cco:ont00000965",
    "Agent": "cco:ont00001017",
    "Organization": "cco:ont00001180",
    "Agent_Capability": "cco:ont00001379",
    "Organization_Capability": "cco:ont00000568",
    "Planned_Act": "cco:ont00000228",
    "Act_of_Information_Processing": "cco:ont00000366",
    "Act_of_Appraisal": "cco:ont00000636",
    "Act_of_Planning": "cco:ont00000511",
}

# --- The 13 top-level APQC sections (PCF ID -> name); daemon iterates these --
SECTIONS = {
    "1.0": ("10002", "Develop Vision and Strategy"),
    "2.0": ("10003", "Develop and Manage Products and Services"),
    "3.0": ("10004", "Market and Sell Products and Services"),
    "4.0": ("20022", "Manage Supply Chain for Physical Products"),
    "5.0": ("20025", "Deliver Services"),
    "6.0": ("20085", "Manage Customer Service"),
    "7.0": ("10007", "Develop and Manage Human Capital"),
    "8.0": ("20607", "Manage Information Technology (IT)"),
    "9.0": ("17058", "Manage Financial Resources"),
    "10.0": ("19207", "Acquire, Construct, and Manage Assets"),
    "11.0": ("16437", "Manage Enterprise Risk, Compliance, Remediation, and Resiliency"),
    "12.0": ("10012", "Manage External Relationships"),
    "13.0": ("10013", "Develop and Manage Business Capabilities"),
}
