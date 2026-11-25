# shared: hide captions whose sentence is already on screen. exec after defining KTEXT (kind -> on-screen text)
# ---------- no double captions: hide a caption chunk when its words are already on screen ----------
import re as _re
try:
    from num2words import num2words as _n2w
except Exception:
    _n2w = None
STOP = set("a an the and or of to in on for is it its it's that this was were be at by with from as so but if you your her she he his they them their there here just not no".split())
KTEXT = globals().get("KTEXT", {})
def _num_forms(tok):
    out = set()
    v = tok.replace("$", "").replace(",", "").replace("%", "")
    try:
        x = float(v)
    except ValueError:
        return out
    if _n2w:
        for w in _re.split(r"[\s\-,]+", _n2w(x if x != int(x) else int(x))): out.add(w)
        if int(x) == x and 1100 <= x < 10000 and x % 100 == 0:   # 1,400 -> fourteen hundred
            for w in _re.split(r"[\s\-]+", _n2w(int(x) // 100)): out.add(w)
            out.add("hundred")
    if tok.startswith("$"): out.add("dollars"); out.add("dollar")
    return out
def _toks(s):
    out = set()
    for raw in _re.findall(r"\$?[\d,.]+%?|[a-z']+", s.lower()):
        raw = raw.strip(".,")
        if not raw: continue
        if _re.match(r"\$?\d", raw):
            out |= _num_forms(raw); n = raw.replace(",", ""); out |= {raw, n, n.lstrip("$"), n.rstrip("%")}
        else:
            out.add(raw); out.add(raw.rstrip("s")); out.add(raw.replace("'s", ""))
    return out
def _scene_text(s):
    parts = [KTEXT.get(s["kind"], "")]
    def walk(v):
        if isinstance(v, str): parts.append(v)
        elif isinstance(v, (list, tuple)):
            for x in v: walk(x)
        elif isinstance(v, dict):
            for x in v.values(): walk(x)
    walk(s["a"])
    if "from" in s["a"] or "to" in s["a"]: parts.append(f'${s["a"].get("to", 0):,}')
    return " ".join(p for p in parts if isinstance(p, str))
_cache = {}; _sent = {}
def _sentence_of(ch):
    """captions are judged per SENTENCE, so they never flicker on/off inside one sentence"""
    if not _sent:
        cur = []
        for c in CHUNKS:
            cur.append(c)
            if _re.search(r"[.?!]$", c[-1]["text"]):
                ws = [w for cc in cur for w in cc]
                for cc in cur: _sent[id(cc)] = ws
                cur = []
        ws = [w for cc in cur for w in cc]
        for cc in cur: _sent[id(cc)] = ws
    return _sent.get(id(ch), ch)
def CAP_SKIP(s, ch):
    if "kind0" not in s: s["kind0"] = s["kind"]
    if s["a"].get("nocap") is not None: return bool(s["a"]["nocap"])
    k = id(s)
    if k not in _cache: _cache[k] = _toks(_scene_text(s))
    st = _cache[k]
    words = [w for w in (_re.sub(r"[^a-z0-9'$-]", "", x["text"].lower()) for x in _sentence_of(ch)) if w]
    words = [w2 for w in words for w2 in w.split("-") if w2]
    content = [w for w in words if w not in STOP]
    if not content: return False
    hit = sum(1 for w in content if w in st or w.rstrip("s") in st or w.replace("'s", "") in st)
    return hit / len(content) >= 0.6 and (hit >= 2 or len(content) == 1)
