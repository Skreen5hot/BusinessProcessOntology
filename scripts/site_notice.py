"""Put APQC's PCF notice in the footer of every docs-site page (NOTICE.md).

The site generator (fetched at CI, see .github/workflows/static.yml) writes
mkdocs.yml from a fixed template with no footer field, so the publish workflow
runs this between generation and `mkdocs build`. It appends a `copyright:`
entry, which Material for MkDocs renders in every page footer. The notice text
comes from config.PCF_NOTICE, the same source as the modules' dct:rights.

    python scripts/site_notice.py [mkdocs.yml]
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from apqc_transform import config  # noqa: E402

NOTICE_URL = "https://github.com/Skreen5hot/BusinessProcessOntology/blob/main/NOTICE.md"


def footer() -> str:
    return (
        "BPO's own work is MIT-licensed. It contains material derived from the APQC "
        "Process Classification Framework®, which is not covered by the MIT licence and is "
        f'used under APQC\'s licence (<a href="{NOTICE_URL}">NOTICE</a>). BPO is not '
        "endorsed by APQC.<br>" + html.escape(config.PCF_NOTICE, quote=False)
    )


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else ROOT / "mkdocs.yml"
    text = path.read_text(encoding="utf-8")
    if any(line.startswith("copyright:") for line in text.splitlines()):
        print(f"{path}: already has a copyright entry; not changed")
        return 1
    # A JSON string is a valid YAML double-quoted scalar.
    entry = "copyright: " + json.dumps(footer(), ensure_ascii=False)
    path.write_text(text.rstrip("\n") + "\n" + entry + "\n", encoding="utf-8")
    print(f"{path}: APQC notice added to the site footer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
