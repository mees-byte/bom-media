import json,sys
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
for d in sys.argv[1:]:
    segs,_=m.transcribe(f'{d}/voice.mp3',word_timestamps=True,beam_size=5)
    ws=[dict(text=w.word.strip(),start=round(w.start,3),end=round(w.end,3),type="word") for s in segs for w in s.words]
    json.dump({"words":ws},open(f'{d}/words.json','w'))
    print(d,len(ws),' '.join(w['text'] for w in ws[:40]))
