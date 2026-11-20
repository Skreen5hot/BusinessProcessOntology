# SPDX-License-Identifier: MIT
"""Record an incoming message: the original's header (with fields remapped to
this record's codes), a source block, then the original's bytes as the body,
so scripts/communications.py can check the body against source.sha256.

    python scripts/record_incoming.py REPO COMMIT PATH OUT [field=value ...]

REPO/COMMIT/PATH name the original in the sender's repository (read with
gh, so it needs `gh auth`); OUT is the file under communications/<team>/
incoming/. Example remap: id=EXAMPLE-BPOT-... to=BPOT.
"""
import hashlib
import re
import subprocess
import sys

repo, commit, path, out, *subs = sys.argv[1:]
original = subprocess.run(
    ["gh", "api", "-H", "Accept: application/vnd.github.raw",
     "repos/%s/contents/%s?ref=%s" % (repo, path, commit)],
    check=True, capture_output=True).stdout
text = original.decode("utf-8")
header = text.split("---\n", 2)[1]
for sub in subs:
    field, value = sub.split("=", 1)
    header, n = re.subn(r"(?m)^%s: .*$" % re.escape(field),
                        "%s: %s" % (field, value), header, count=1)
    assert n == 1, field
digest = hashlib.sha256(original).hexdigest()
copy = ("---\n" + header +
        "source:\n  repo: %s\n  commit: %s\n  path: %s\n  sha256: %s\n---\n"
        % (repo, commit, path, digest)).encode("utf-8") + original
open(out, "wb").write(copy)
print(out, digest)
