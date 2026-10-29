# D-ETF-1 10/29 PD: 10/29 다시 받은 15줄에 10/28과 같은 B-31 손질 — 줄 안 0.30초 넘는 쉼만 0.30초로(말 소리는 안 자름, 앞뒤 무음 그대로)
#   잣대는 lfvoice.pause_stats와 같은 voicenat.env_db·thresh(줄 최고 −25dB). 원본은 _raw/<키>.pre1029cap.wav로 남김.
import sys, os, json, shutil
import numpy as np
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
sys.path.insert(0, R)
import lfvoice, voicenat
EP = os.path.join(R, 'research/longform/ep/D-ETF-1')
ATS = sys.argv[1].split(',')
CAP = 0.30
d = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
for at in ATS:
    si, li = map(int, at.split(':')); l = d['sections'][si]['lines'][li]
    fn = os.path.join(lfvoice.PUB, l['audio']); a, sr = lfvoice.read(fn)
    db = voicenat.env_db(a.astype(np.float32) / 32768.0, sr=sr); th = voicenat.thresh(db)
    runs = [(r0, r1) for r0, r1 in voicenat.quiet_runs(db, th, minrun=CAP) if r1 - r0 > CAP]
    if not runs: print(at, '긴 쉼 없음'); continue
    bak = os.path.join(os.path.dirname(fn), '_raw', os.path.basename(fn)[:-4] + '.pre1029cap.wav')
    if not os.path.exists(bak): shutil.copy2(fn, bak)
    keep, pos = [], 0
    for r0, r1 in runs:
        c0 = int((r0 + CAP / 2) * sr); c1 = int((r1 - CAP / 2) * sr)   # 쉼 가운데를 잘라 앞뒤 0.15초씩 남김
        keep.append(a[pos:c0]); pos = c1
    keep.append(a[pos:])
    b = np.concatenate(keep)
    lfvoice.write(fn, b, sr)
    print(at, f'쉼 {len(runs)}곳 {[round(r1 - r0, 2) for r0, r1 in runs]} → {CAP}초 · {len(a) / sr:.2f}→{len(b) / sr:.2f}초')
