"""Publish docs/migrations.tsv on the docs site as an "IRI migrations" page.

A retired BPO identifier must stay resolvable to its replacement: the site's term
tables leave deprecated and retired terms out, so without this page an IRI that
was once public on main (e.g. bpo:P10530_SuggestionProgram, WP6 B4) would lead
nowhere. The publish workflow runs this after the site generator, which writes
mkdocs.yml from a fixed template, and before `mkdocs build`. It writes
docs/migrations.md (one row per migration, an anchor per retired IRI) and adds
the page to the nav.

    python scripts/site_migrations.py [mkdocs.yml]
"""
import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "docs" / "migrations.tsv"
PAGE = ROOT / "docs" / "migrations.md"
BPO = "https://fandaws.com/ontology/bpo#"
NAV = "  - IRI migrations: migrations.md"


def iri(term: str) -> str:
    """bpo:X -> its full IRI (other prefixes and prose are left as written)."""
    return re.sub(r"\bbpo:(\w+)", lambda m: f"{m.group(0)} (`{BPO}{m.group(1)}`)", term)


def page() -> str:
    rows = [r for r in csv.reader(
        (line for line in TSV.read_text(encoding="utf-8").splitlines() if not line.startswith("#")),
        delimiter="\t")]
    head, body = rows[0], rows[1:]
    out = ["# IRI migrations", "",
           "Every BPO identifier that was retired, replaced or given a changed meaning, "
           "with its successor. Where the replacement differs from the old IRI, use the "
           "replacement; the change says whether the old IRI is still declared (deprecated) "
           "or retired. Source: `docs/migrations.tsv`.", ""]
    for r in body:
        rec = dict(zip(head, r))
        old = rec["old_iri"]
        anchor = re.sub(r"\W+", "-", old.replace("bpo:", "")).strip("-")
        out += [f'<a id="{html.escape(anchor)}"></a>', f"## {old}", "",
                f"- **Replaced by:** {iri(rec['new_iri'])}",
                f"- **Old IRI:** {iri(old)}",
                f"- **Change:** {rec['kind']}",
                f"- **Date:** {rec['date']}",
                f"- **Decision:** {rec['decision']}",
                f"- **Reason:** {rec['reason']}", ""]
    return "\n".join(out)


def add_nav(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    if NAV in lines:
        return False
    i = lines.index("nav:")
    j = i + 1
    while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("-")):
        j += 1
    lines.insert(j, NAV)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    mk = Path(argv[1]) if len(argv) > 1 else ROOT / "mkdocs.yml"
    PAGE.write_text(page(), encoding="utf-8")
    print(f"{PAGE.relative_to(ROOT)}: written from {TSV.relative_to(ROOT)}")
    print(f"{mk}: " + ("migrations page added to the nav" if add_nav(mk) else "nav already lists the page"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
