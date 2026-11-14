# x1s_even 첫 줄 새로 받기 — X-1 tts.json 그대로(Charon 1.1, markup) · lfvoice.chirp_one
import sys, os, json, hashlib
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'; sys.path.insert(0, W)
import lfvoice, numpy as np
EP = os.path.join(W, 'research', 'longform', 'ep', 'X-1')
cfg = json.load(open(os.path.join(EP, 'tts.json'), encoding='utf-8'))
t = sys.argv[1]
h = hashlib.sha1((cfg['voice'] + str(cfg['speakingRate']) + t + (sys.argv[2] if len(sys.argv) > 2 else '')).encode()).hexdigest()[:16]
fn = os.path.join(W, 'video', 'public', 'audio', 'x1s', h + '.wav'); os.makedirs(os.path.dirname(fn), exist_ok=True)
if not os.path.exists(fn): lfvoice.chirp_one(EP, cfg, t, fn, 'lfvoice:x1s_even')
a, sr = lfvoice.read(fn)
print(json.dumps({'text': t, 'audio': 'audio/x1s/' + h + '.wav', 'frames': int(np.ceil(len(a) / sr * 30)), 'f0': float(lfvoice.f0(a, sr))}, ensure_ascii=False))
