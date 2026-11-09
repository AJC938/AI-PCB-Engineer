"""Replace machine-specific absolute paths in generated text evidence with neutral placeholders.

The repository root becomes "<repo>" and any remaining "C:/Users/<name>" style home path becomes "<home>".
Usage: python -I sanitize_paths.py <repo_root> <file> [<file> ...]
"""
import os
import re
import sys

raw = sys.argv[1]
if re.match(r"^/[a-zA-Z]/", raw):  # Git Bash style /c/Users/... -> C:/Users/...
    raw = raw[1].upper() + ":" + raw[2:]
root = os.path.abspath(raw)
fw = root.replace("\\", "/")
variants = {root, fw, fw.replace("/", "\\\\"), fw[0].lower() + fw[1:], "/" + fw[0].lower() + fw[2:]}
home_re = re.compile(r"(?i)[A-Z]:(?:\\+|/)Users(?:\\+|/)[^\\/\"'<>\s]+")  # any escaping depth
for path in sys.argv[2:]:
    s = open(path, encoding="utf-8", errors="surrogateescape").read()
    n0 = s
    for v in sorted(variants, key=len, reverse=True):
        s = s.replace(v, "<repo>")
    s = home_re.sub("<home>", s)
    if s != n0:
        open(path, "w", encoding="utf-8", errors="surrogateescape").write(s)
        print("sanitized", os.path.basename(path))
