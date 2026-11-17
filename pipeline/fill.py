"""Fill NARRATION.template.txt with values.json -> NARRATION.txt.  Usage: python3 fill.py <workdir>"""
import json, re, sys, os
d = sys.argv[1]
v = json.load(open(os.path.join(d, "values.json")))
t = open(os.path.join(d, "NARRATION.template.txt")).read()
out = re.sub(r"\{\{(\w+)\}\}", lambda m: v[m.group(1)]["spoken"], t)
assert "{{" not in out
open(os.path.join(d, "NARRATION.txt"), "w").write(out)
words = len(re.sub(r"\[[a-z ]+\]", "", out).split())
print(f"NARRATION.txt written: {words} words, {len(out)} chars ({v['_status'][:10]})")
