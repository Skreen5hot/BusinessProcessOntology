"""Remove local act-genus (ex:ActOf*) class DEFINITIONS from a slice module.

After the genera are consolidated into apqc-ext.ttl (D9), each slice should
only REFERENCE them (as rdfs:subClassOf fillers), not re-define them. This
removes every `ex:ActOf<Name> a owl:Class ; ... .` definition block (plus any
immediately-preceding PROPOSE-EXT/comment lines), leaving every reference intact.
The validator merges apqc-ext.ttl, so the subclass chains still resolve.

Line-based (robust against periods inside rdfs:comment strings): a Turtle
statement ends at the first line whose content ends with '.' rather than ';'/','.

Usage: python scripts/strip_local_genera.py <slice.ttl>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SUBJECT = re.compile(r"^ex:ActOf\w+ a owl:Class\b")


def _is_terminator(line: str) -> bool:
    s = line.strip()
    if s.startswith("#") or not s:
        return False  # a pure comment / blank line is never a statement terminator
    # ignore a trailing line comment (e.g. "cco:ont00000228 ;  # note.") before testing
    code = re.sub(r"\s+#.*$", "", s).rstrip()
    return code.endswith(".") and not code.endswith(";") and not code.endswith(",")


def strip(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    removed: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if SUBJECT.match(line):
            removed.append(line.split()[0])
            # drop any contiguous comment lines we already emitted for this block
            while out and out[-1].lstrip().startswith("#"):
                out.pop()
            # also drop a single trailing blank between the comment and prior content
            # consume the genus statement through its terminator line
            while i < n and not _is_terminator(lines[i]):
                i += 1
            i += 1  # skip the terminator line too
            # skip one trailing blank line left by the removed block
            if i < n and lines[i].strip() == "":
                i += 1
            continue
        out.append(line)
        i += 1

    new = "\n".join(out)
    new = re.sub(r"\n{3,}", "\n\n", new).rstrip() + "\n"
    if removed:
        path.write_text(new, encoding="utf-8", newline="\n")
    return removed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: strip_local_genera.py <slice.ttl>")
    p = Path(sys.argv[1])
    rem = strip(p)
    print(f"{p.name}: removed {len(rem)} local genus def(s): {sorted(set(rem))}")
