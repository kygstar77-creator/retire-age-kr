# 우리 쇼츠 관문(bgcheck 쇼츠 ①②⑥)을 잘되는 경쟁 쇼츠에 그대로 대 본다 — 관문이 잘되는 영상을 얼마나 '거부'하나.
#   py -3.12 gatecheck.py media → gatecheck.json
#   ① 배경 실사: bgcheck.frame_bg 그대로(가장자리 세 곳 중 둘이 사진처럼 섞인 색) — 90% 미만 또는 3초 넘게 연달아 없으면 거부
#   ② 자막: res/*.json 글자 상자(같은 OCR)로 bgcheck.frame_cap 조건(가운데 y 1100~1240, 가운데 x 250~690, 높이 56↑)과 x만 540 기준(330~750)으로 바꾼 것 둘 다
#   ⑥ UI 상자: bgcheck.ui_boxes 그대로 — 상자 1개↑ 프레임 30% 넘으면 거부(10/21부터)
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
import numpy as np, bgcheck, safezone
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
OURS = {x['id']: x['path'] for x in json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8')) if x['kind'] == 'short'}
out_p = os.path.join(HERE, 'gatecheck.json'); out = json.load(open(out_p, encoding='utf-8')) if os.path.exists(out_p) else {}
jobs = [(v, os.path.join(M, f'short_{v}.v.mp4')) for _, v in S['short']] + list(OURS.items())
for vid, p in jobs:
    if vid in out or not os.path.exists(p): continue
    rp = os.path.join(HERE, 'res', f'short_{vid}.json')
    if not os.path.exists(rp): continue
    res = json.load(open(rp, encoding='utf-8')); bt = {round(f['t']): f['boxes'] for f in res['frames']}
    fr = []
    for t, img in safezone.frames(p, 1.0):
        bg, _ = bgcheck.frame_bg(img); box = bgcheck.ui_boxes(img, skip_bottom=False)
        bs = bt.get(round(t), [])
        def cap(x0, x1): return any(1100 <= (b[1] + b[3]) / 2 <= 1240 and x0 <= (b[0] + b[2]) / 2 <= x1 and b[3] - b[1] >= 56 for b in bs)
        fr.append((bg, box, cap(250, 690), cap(330, 750)))
    n = len(fr) or 1; run = best = 0
    for f in fr: run = run + 1 if not f[0] else 0; best = max(best, run)
    o = {'n': len(fr), 'bg_frac': round(sum(f[0] for f in fr) / n, 2), 'bg_run': best, 'box_frac': round(sum(f[1] >= 1 for f in fr) / n, 2),
         'cap_old': round(sum(f[2] for f in fr) / n, 2), 'cap_540': round(sum(f[3] for f in fr) / n, 2)}
    o['fail_bg'] = o['bg_frac'] < bgcheck.BG_FRAC or best > bgcheck.BG_RUN; o['fail_box'] = o['box_frac'] > bgcheck.NC_FRAC
    o['fail_cap_old'] = o['cap_old'] < bgcheck.CAP_FRAC; o['fail_cap_540'] = o['cap_540'] < bgcheck.CAP_FRAC
    out[vid] = o; json.dump(out, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(vid, o, flush=True)
