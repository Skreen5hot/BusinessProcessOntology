"""Read the APQC PCF Excel export into typed rows -- stdlib only.

The catalog layer (ADR-001 R1) must be reproducible with zero third-party
dependencies, so this parser reads the .xlsx (a zip of XML) directly rather
than via openpyxl/pandas. Columns expected on the 'Combined' sheet:

    PCF ID | Hierarchy ID | Name | Difference Index | Change details |
    Metrics available? | Element Description
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path

from . import config

_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

LEVEL_NAMES = {1: "Category", 2: "ProcessGroup", 3: "Process", 4: "Activity", 5: "Task"}


@dataclass(frozen=True)
class PcfRow:
    pcf_id: str
    hierarchy_id: str          # dotted-decimal, positional, NON-stable
    name: str
    description: str
    level: int                 # 1..5
    level_name: str            # Category..Task
    parent_hierarchy: str | None   # dotted id of parent, or None for a Category

    @property
    def is_category(self) -> bool:
        return self.level == 1


def find_export(root: Path | None = None) -> Path:
    root = root or config.ROOT
    matches = sorted(root.glob(config.PCF_XLSX_GLOB))
    if not matches:
        raise FileNotFoundError(
            f"No PCF export matching {config.PCF_XLSX_GLOB!r} under {root}"
        )
    return matches[0]


def _shared_strings(z: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("m:si", _NS):
        # concatenate all <t> descendants (handles rich-text runs)
        out.append("".join(t.text or "" for t in si.iter() if t.tag.endswith("}t")))
    return out


def _combined_sheet_path(z: zipfile.ZipFile) -> str:
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    name_to_rid = dict(
        re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wb)
    )
    rid_to_target = dict(
        re.findall(r'Id="(rId\d+)"[^>]*Target="(worksheets/sheet\d+\.xml)"', rels)
    )
    rid = name_to_rid.get("Combined")
    if not rid:
        raise KeyError("No 'Combined' sheet in workbook")
    return "xl/" + rid_to_target[rid]


def _parent_hierarchy(hierarchy_id: str) -> str | None:
    """Parent of '1.1.1' is '1.1'; parent of a Category '1.0' is None.

    APQC writes Categories as 'N.0'; their children are 'N.1', 'N.2', ...
    so the parent of 'N.1' is the Category 'N.0'.
    """
    parts = hierarchy_id.split(".")
    if re.match(r"^\d+\.0$", hierarchy_id):
        return None
    if len(parts) == 2:                # 'N.m' -> Category 'N.0'
        return f"{parts[0]}.0"
    return ".".join(parts[:-1])


def _level(hierarchy_id: str) -> int:
    if re.match(r"^\d+\.0$", hierarchy_id):
        return 1
    return hierarchy_id.count(".") + 1


def load_rows(xlsx: Path | None = None) -> list[PcfRow]:
    xlsx = xlsx or find_export()
    with zipfile.ZipFile(xlsx) as z:
        ss = _shared_strings(z)
        sheet = ET.fromstring(z.read(_combined_sheet_path(z)))

        def cell(c) -> str:
            v = c.find("m:v", _NS)
            if v is None:
                return ""
            return ss[int(v.text)] if c.get("t") == "s" else (v.text or "")

        raw = [
            [cell(c) for c in row.findall("m:c", _NS)]
            for row in sheet.findall(".//m:row", _NS)
        ]

    header, *body = raw
    rows: list[PcfRow] = []
    for r in body:
        # pad short rows (trailing empty cells are omitted in the XML)
        r = (r + [""] * 7)[:7]
        pcf_id, hierarchy_id, name, _diff, _chg, _metrics, desc = r
        if not hierarchy_id:
            continue
        lvl = _level(hierarchy_id)
        rows.append(
            PcfRow(
                pcf_id=pcf_id,
                hierarchy_id=hierarchy_id,
                name=name,
                description=desc,
                level=lvl,
                level_name=LEVEL_NAMES.get(lvl, f"L{lvl}"),
                parent_hierarchy=_parent_hierarchy(hierarchy_id),
            )
        )
    return rows


def subtree(rows: list[PcfRow], section_hierarchy: str) -> list[PcfRow]:
    """All rows under a top-level section, e.g. '1.0' -> 1.0 and every 1.x..."""
    prefix = section_hierarchy.split(".")[0] + "."
    sect_num = section_hierarchy.split(".")[0]
    return [
        r
        for r in rows
        if r.hierarchy_id == section_hierarchy
        or r.hierarchy_id.startswith(prefix)
        and r.hierarchy_id.split(".")[0] == sect_num
    ]


if __name__ == "__main__":  # quick smoke test
    rows = load_rows()
    from collections import Counter

    print(f"rows: {len(rows)}")
    print("by level:", dict(Counter(r.level_name for r in rows)))
    cats = [r for r in rows if r.is_category]
    print(f"categories: {len(cats)}")
    orphans = [
        r
        for r in rows
        if r.parent_hierarchy
        and r.parent_hierarchy not in {x.hierarchy_id for x in rows}
    ]
    print(f"rows with missing parent: {len(orphans)}")
