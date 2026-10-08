# 롱폼 목소리 다시 받기 — 같은 날·같은 모델·같은 목소리로 튀는 줄만 한 요청에 모아 다시 녹음하고,
# 줄마다 옛 녹음과 새 녹음 중 편 중앙 음높이에 가깝고 속도 기준(4.8~8.2) 안인 쪽을 고른다(2026-10-08 PD, M-1 IQR 0.18 막힘).
#   py -3.12 work/lfretake.py <ep폴더> [--n 20] [--dry] [--trim]   # --trim = 다시 받기 없이 앞뒤 빈 소리만 다듬기
# 옛 녹음은 audio/<편>/_take1/에 남긴다. 요청 1회 = 무료 한도 1회. 다른 모델로 넘어가지 않는다(lfvoice 규칙 1).
import sys, os, json, shutil
import numpy as np
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
import lfvoice as V

ep = os.path.abspath(ARGS[0]); CAP = 0.3   # 줄 앞뒤 빈 소리 상한(초) — 공개된 E-1·D-1 0.4, N-1 0.1 사이
N = int(ARGS[ARGS.index('--n') + 1]) if '--n' in ARGS else 20; dry = '--dry' in ARGS
cfg = V.lock(ep); d = json.load(open(os.path.join(ep, 'voice.json'), encoding='utf-8'))
rows = [l for s in d['sections'] for l in s['lines'] if l.get('audio')]
def trim(ep, cap=CAP):
    # 자르기 경계에서 줄마다 앞뒤로 붙은 빈 소리를 cap초로 줄인다(말소리·빠르기는 그대로, 원본은 _pretrim/) — 10/8 M-1 편 전체 5.40→5.63
    import wave
    d = json.load(open(os.path.join(ep, 'voice.json'), encoding='utf-8')); bk = os.path.join(V.aud_dir(ep), '_pretrim'); os.makedirs(bk, exist_ok=True); n = 0
    for s in d['sections']:
        for l in s['lines']:
            if not l.get('audio'): continue
            fn = os.path.join(V.PUB, l['audio']); a, sr = V.read(fn); m, win = V.loud_mask(a, sr); idx = np.where(m)[0]
            st, en = max(0, idx[0] * win - int(cap * sr)), min(len(a), (idx[-1] + 1) * win + int(cap * sr))
            if st == 0 and en == len(a): continue
            shutil.copy(fn, os.path.join(bk, os.path.basename(fn)))
            with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(a[st:en], -32768, 32767).astype(np.int16).tobytes())
            n += 1
    print('앞뒤 빈 소리 다듬은 줄', n); V.build(ep)
if '--trim' in ARGS: trim(ep); sys.exit()
fm = float(np.median([l['f0'] for l in rows if l['f0']]))
def score(f, r):   # 낮을수록 좋다: 음높이 거리 + 속도 기준 밖 벌점
    return abs(np.log(max(f, 1) / fm)) + (1 if r < 4.8 or r > 8.2 else 0) + (1 if abs(f / fm - 1) > 0.25 else 0)
# 반드시 다시 받을 줄(readback에서 숫자·빠짐이 걸린 줄): ep/check/retake_must.txt 한 줄에 대본 문장 앞부분 하나 — 옛 녹음은 쓰지 않고 2번씩 받아 나은 쪽
mf = os.path.join(ep, 'check', 'retake_must.txt')
must_keys = [x.strip() for x in open(mf, encoding='utf-8')] if os.path.exists(mf) else []
must = [l for k in must_keys if k for l in rows if l['text'].startswith(k)]
pick = must + [l for l in sorted(rows, key=lambda l: -score(l['f0'], l['rate'])) if l not in must][:N]
TAKES = {id(l): (2 if l in must else 1) for l in pick}
print(f'편 중앙 {fm:.0f}Hz · 다시 받을 줄 {len(pick)}(반드시 {len(must)}·2번씩)')
for l in pick: print(f"  {'반드시 ' if l in must else ''}{l['f0']:.0f}Hz {l['rate']:.2f} | {l['text'][:30]}")
if dry: sys.exit()
order = [l for l in pick for _ in range(TAKES[id(l)])]
todo = [l['say'] for l in order]
keep = os.path.join(V.aud_dir(ep), '_take_' + __import__('time').strftime('%m%d%H%M')); os.makedirs(keep, exist_ok=True)
for l in pick:   # 옛 녹음을 먼저 옮겨 둔다
    h, fn = V.wav_of(ep, cfg, l['say']); shutil.copy(fn, os.path.join(keep, h + '.wav'))
rk = V.hashlib.md5(('|'.join([cfg['model'], cfg['voice']] + todo)).encode()).hexdigest()[:16]; raw = os.path.join(V.aud_dir(ep), '_raw', rk + '.pcm')
if not os.path.exists(raw): V.request(cfg, todo).astype(np.int16).tofile(raw); print('저장', raw)
# TTS가 지시문을 앞머리에 읽기도 해서 cut 대신 받아쓰기 맞춤(fixcut 경계)으로 자른다 — 묶음 하나짜리 가짜 pack, 쓰기는 여기서
V.pack = lambda secs, mr: [[{'title': 'retake', 'lines': [l['text'] for l in order]}]]
V.fixcut(ep, 0, dry=True)
pcm, bounds, seg = V.LAST_FIX; pad = np.zeros(int(V.SR * 0.08), dtype=np.float32)
cands = {}
for n, ((s0, e), l) in enumerate(zip(seg, order)):
    tmp = os.path.join(keep, f'cand{n}.wav'); V.write(tmp, np.concatenate([pad, pcm[bounds[s0][0]:bounds[e - 1][1]], pad])); a, sr = V.read(tmp)
    cands.setdefault(id(l), []).append((score(V.f0(a, sr), V.syl(l['say']) / max(V.speech_sec(a, sr), 0.1)), tmp, V.f0(a, sr), V.syl(l['say']) / max(V.speech_sec(a, sr), 0.1)))
won = 0
for l in pick:
    h, fn = V.wav_of(ep, cfg, l['say']); sc, tmp, f, r = min(cands[id(l)])
    new_better = l in must or sc < score(l['f0'], l['rate'])
    print(f"  {'새' if new_better else '옛'} | 옛 {l['f0']:.0f}Hz {l['rate']:.2f} → 새 {f:.0f}Hz {r:.2f} | {l['text'][:26]}")
    if new_better: won += 1; shutil.copy(tmp, fn)
    if os.path.exists(fn + '.json'): os.remove(fn + '.json')
print('바꾼 줄', won); V.build(ep); trim(ep)
