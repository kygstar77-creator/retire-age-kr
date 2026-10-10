# W-1 10/11 16:01 창 준비 — 2~4장 10/10 녹음 27줄을 audio/w-1/_park_1010/로 옮겨 lfvoice make가 2~7장 44줄을 새로 받게 한다.
# 왜: 빠진 17줄(5~7장)만 받으면 녹음 날 10/10 38줄 + 10/11 17줄 = 둘째 날 31% → lfrender 날짜 규칙(둘째 날 20% 이하)으로 거부.
#     0·1장 11줄만 10/10으로 남기면 11/55 = 20.0% → 통과(retake_ok). 0·1장 줄을 더 다시 받으면 비율은 더 내려간다.
#   py -3.12 work/research/longform/ep/W-1/check/park_1011.py [--dry]
import os, sys, json, shutil
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PUB = os.path.abspath(os.path.join(EP, '..', '..', '..', '..', '..', 'video', 'public'))
v = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
KEEP = ('[0.', '1.')                       # 10/10 녹음 그대로 둘 장
dst = os.path.join(PUB, 'audio', 'w-1', '_park_1010'); dry = '--dry' in sys.argv
n_keep = n_move = 0
for s in v['sections']:
    for l in s['lines']:
        if not l.get('audio'): continue
        if s['title'].startswith(KEEP): n_keep += 1; continue
        src = os.path.join(PUB, l['audio']); n_move += 1
        print(('옮길 ' if dry else '옮김 ') + f"{l.get('f0', 0):.0f}Hz | {s['title'][:12]} | {l['text'][:28]}")
        if not dry:
            os.makedirs(dst, exist_ok=True)
            for f in (src, src + '.json'):
                if os.path.exists(f): shutil.move(f, os.path.join(dst, os.path.basename(f)))
tot = sum(len(s['lines']) for s in v['sections'])
print(f'남김(10/10) {n_keep}줄 · 옮김 {n_move}줄 · 전체 {tot}줄 → 10/10 몫 {n_keep / tot:.1%}(20% 이하여야 lfrender 통과)')
