# 쉼 길이 — 말하는 동안(앞 180초) 소리가 바닥으로 떨어진 구간(voicenat.quiet_runs: 줄 최고 −25dB 아래, 50ms 중앙값)의 길이 분포.
# 0.25초 넘는 쉼만 센다(말 빠르기 잣대와 같음). 음악이 깔린 영상은 쉼이 덜 잡힌다(바닥이 안 떨어짐) — 표에 바닥 음과 같이 본다.
#   py -3.12 pauses.py media → pauses.json
import os, sys, json, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
import voicenat, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
OURS = json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8'))
jobs = [(k, v, os.path.join(M, f'{k}_{v}.a.m4a')) for k in ('short', 'long') for _, v in S[k]] + [(x['kind'], x['id'], x['path']) for x in OURS]
out_p = os.path.join(HERE, 'pauses.json'); out = json.load(open(out_p, encoding='utf-8')) if os.path.exists(out_p) else {}
for kind, vid, src in jobs:
    key = f'{kind}_{vid}'
    if key in out or not os.path.exists(src): continue
    p = subprocess.run([FF, '-loglevel', 'error', '-i', src, '-t', '180', '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768
    if len(a) < 16000 * 5: continue
    db = voicenat.env_db(a); th = voicenat.thresh(db)
    runs = [r1 - r0 for r0, r1 in voicenat.quiet_runs(db, th, minrun=0.25)]
    runs = runs[1:-1] if len(runs) > 2 else runs   # 앞뒤 무음 뺌
    dur = len(a) / 16000
    out[key] = {'n': len(runs), 'per_min': round(len(runs) / (dur / 60), 1), 'med': round(float(np.median(runs)), 2) if runs else None,
                'p75': round(float(np.percentile(runs, 75)), 2) if runs else None, 'p90': round(float(np.percentile(runs, 90)), 2) if runs else None,
                'share': round(sum(runs) / dur, 3)}
    json.dump(out, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(key, out[key], flush=True)
