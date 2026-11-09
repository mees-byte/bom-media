import json,sys
for d in sys.argv[1:]:
    W=json.load(open(f'{d}/words.json'))['words']; out=[]
    for w in W:
        t=w['text']
        if out and (t.startswith('.') and t[1:2].isdigit() or t in ('%','%.','%,')):
            out[-1]['text']+=t; out[-1]['end']=w['end']
        else: out.append(dict(w))
    json.dump({"words":out},open(f'{d}/words.json','w')); print(d,len(out),[x['text'] for x in out if '.' in x['text'] and any(c.isdigit() for c in x['text'])])
