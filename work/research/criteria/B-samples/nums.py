# 문서에 옮길 숫자: 경쟁 중앙값·사분위·범위·n, 우리 값. py -3.12 nums.py
import json, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'summary.json'), encoding='utf-8'))
CF = json.load(open(os.path.join(HERE, 'cutfix.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'cutfix.json')) else {}
EYE = json.load(open(os.path.join(HERE, 'eye.json'), encoding='utf-8'))
for r in R:
    if r['kind'] == 'short' and r['id'] in CF:
        r['cf_pm'] = CF[r['id']]['cuts_pm']; r['cf_med'] = CF[r['id']]['scene_med']
    e = EYE.get(f"{r['kind']}_{r['id']}")
    if e: r['eye_live'] = e['live']; r['eye_card'] = e['card']; r['eye_ai'] = int(bool(e['ai_person']))
def q(v, p): v = sorted(v); return v[min(len(v) - 1, int(round(p * (len(v) - 1))))]
def show(kind, keys, filt=lambda r: True, label=''):
    C = [r for r in R if r['kind'] == kind and not r['id'].startswith('OURS') and filt(r)]
    O = [r for r in R if r['kind'] == kind and r['id'].startswith('OURS')]
    print(f'== {kind} {label} 경쟁 {len(C)}편')
    for k in keys:
        v = [r[k] for r in C if isinstance(r.get(k), (int, float)) and not isinstance(r.get(k), bool)]
        if not v: continue
        print(f'  {k}: 중앙 {round(st.median(v), 2)} · 25~75% {q(v, .25)}~{q(v, .75)} · 범위 {min(v)}~{max(v)} (n={len(v)}) | 우리 ' + ', '.join(f"{o['id'][5:]} {o.get(k)}" for o in O))
SK = ['dur', 'cap_cx', 'cap_cy', 'cap_h', 'cap_w', 'cap_x0', 'cap_x1', 'title_cx', 'title_y0', 'title_y1', 'title_hmax', 'title_h', 'title_lines', 'wide_cx',
      'x0_p05', 'x1_p95', 'y1_p95', 'f_top288', 'f_bot1248', 'f_right888', 'f_btn940', 'f_btn_mw', 'cf_pm', 'cf_med', 'cuts1_pm', 'scene1_med',
      'lufs', 'rate', 'rate_all', 'floor_gap_db', 'eye_live', 'eye_card', 'eye_ai']
show('short', SK)
show('short', ['cap_cy', 'cap_h', 'rate', 'rate_all'], lambda r: (r.get('dur') or 0) >= 15, '(15초 넘는 말 있는 편)')
LK = ['cuts1_pm', 'scene1_med', 'scene1_p90', 'scene_max', 'maxh_med', 'maxh_p75', 'lines_med', 'cap_cy', 'cap_h', 'cap_cx', 'cap_w', 'cap_frames', 'lufs', 'rate', 'rate_all', 'floor_gap_db', 'eye_live', 'eye_card', 'eye_ai']
show('long', LK)
show('long', LK, lambda r: r.get('eye_live') is not None and r['eye_live'] < 0.6, '(얼굴 없는·판 위주 = 눈 실사 60% 미만)')
for r in R:
    if r['kind'] == 'long': print(' ', r['ch'], {k: r.get(k) for k in LK})
