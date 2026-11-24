# k1s_bottom 첫 줄 새로 받기 — KOSPI-1 tts.json 그대로(Charon 1.1, markup, pause_v 2) · lfvoice.chirp_one (jt1s_even/newline.py 사본)
#   py -3.12 newline.py "<자막 글>" "<읽을 말>"
import sys, os, json, hashlib
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'; sys.path.insert(0, W)
import lfvoice, numpy as np
EP = os.path.join(W, 'research', 'longform', 'ep', 'KOSPI-1')
cfg = json.load(open(os.path.join(EP, 'tts.json'), encoding='utf-8'))
t, say = sys.argv[1], sys.argv[2]
h = hashlib.sha1((cfg['voice'] + str(cfg['speakingRate']) + say).encode()).hexdigest()[:16]
fn = os.path.join(W, 'video', 'public', 'audio', 'k1s', h + '.wav'); os.makedirs(os.path.dirname(fn), exist_ok=True)
if not os.path.exists(fn): lfvoice.chirp_one(EP, cfg, say, fn, 'lfvoice:k1s_bottom')
a, sr = lfvoice.read(fn)
print(json.dumps({'text': t, 'say': say, 'audio': 'audio/k1s/' + h + '.wav', 'frames': int(np.ceil(len(a) / sr * 30)), 'f0': float(lfvoice.f0(a, sr))}, ensure_ascii=False))
