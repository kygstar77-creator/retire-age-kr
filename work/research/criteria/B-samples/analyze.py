# res/*.json → 표(summary.csv·summary.json). 쇼츠는 1080×1920, 롱폼은 1920×1080 좌표.
#   py -3.12 analyze.py
import os, json, glob, statistics as st, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
NAME = {v: c for k in ('short', 'long') for c, v in S[k]}
med = lambda a: round(st.median(a), 1) if a else None


def lines(boxes):
    """낱말 상자를 줄로 합친다: 세로 겹침이 작은 쪽 높이의 50% 넘고 가로 틈이 글자 높이 1.5배 안이면 한 줄."""
    bs = sorted([list(b) for b in boxes if b[3] - b[1] >= 12], key=lambda b: b[0]); out = []
    for b in bs:
        for L in out:
            ov = min(L[3], b[3]) - max(L[1], b[1]); h = min(L[3] - L[1], b[3] - b[1])
            if ov > 0.5 * h and b[0] - L[2] < 1.5 * max(L[3] - L[1], b[3] - b[1]):
                L[0], L[1], L[2], L[3] = min(L[0], b[0]), min(L[1], b[1]), max(L[2], b[2]), max(L[3], b[3]); break
        else: out.append(b)
    return out

def fixed_mask(frames, W, H):
    """같은 자리(40px 칸)에 프레임 40% 넘게 나오는 상자 = 고정 글자(위 제목·채널명·로고)."""
    cnt = collections.Counter()
    for f in frames:
        seen = set()
        for b in f['boxes']:
            k = (round(b[0] / 24), round(b[2] / 24), round(b[1] / 24)); seen.add(k)   # 같은 왼끝·오른끝·위끝 = 같은 글(자막은 줄마다 폭이 달라 빠진다)
        cnt.update(seen)
    n = len(frames) or 1
    return {k for k, c in cnt.items() if c / n >= 0.4}

def short_row(d):
    fr = d['frames']; W, H = 1080, 1920; fx = fixed_mask(fr, W, H)
    key = lambda b: (round(b[0] / 24), round(b[2] / 24), round(b[1] / 24))
    cap, title, allb = [], [], []
    for f in fr:
        for b in f['boxes']:
            h = b[3] - b[1]; w = b[2] - b[0]
            if h < 12 or w < 20: continue
            allb.append((f['t'], b))
            cy = (b[1] + b[3]) / 2
            if key(b) in fx:
                if cy < 0.45 * H: title.append(b)
            elif 0.35 * H <= cy <= 0.90 * H and w >= 100: cap.append(b)
    # 자막 띠: 바뀌는 상자의 가운데 y를 40px 칸으로 묶어 가장 많은 칸 ±60px
    if cap:
        band = collections.Counter(round((b[1] + b[3]) / 2 / 40) for b in cap).most_common(1)[0][0] * 40   # 자막 = 바뀌는 글 가운데 가장 자주 나오는 높이
        cap = [b for b in cap if abs((b[1] + b[3]) / 2 - band) <= 60]
    capf = len({t for t, b in allb if b in cap})
    r = {
        'cap_cy': med([(b[1] + b[3]) / 2 for b in cap]), 'cap_cx': med([(b[0] + b[2]) / 2 for b in cap]),
        'cap_h': med([b[3] - b[1] for b in cap]), 'cap_x0': med([b[0] for b in cap]), 'cap_x1': med([b[2] for b in cap]),
        'cap_w': med([b[2] - b[0] for b in cap]), 'cap_frames': round(capf / max(len(fr), 1), 2),
        'title_cx': med([(b[0] + b[2]) / 2 for b in title]), 'title_y0': min([b[1] for b in title], default=None),
        'title_y1': max([b[3] for b in title], default=None), 'title_h': med([b[3] - b[1] for b in title]),
        'title_hmax': max([b[3] - b[1] for b in title], default=None), 'title_w': med([b[2] - b[0] for b in title]),
        'title_lines': len({round((b[1] + b[3]) / 2 / 40) for b in title}),
    }
    n = len(fr) or 1
    def frac(pred): return round(sum(any(pred(b) for b in f['boxes'] if b[3] - b[1] >= 12) for f in fr) / n, 2)
    r['f_top288'] = frac(lambda b: b[1] < 288)                 # 위 288 안에 글자
    r['f_bot1248'] = frac(lambda b: b[3] > 1248)               # 아래 672(Ads 기준) 안에 글자
    r['f_right888'] = frac(lambda b: b[2] > 888 and b[3] > 288)
    r['f_btn940'] = frac(lambda b: b[2] > 940 and b[3] > 940)  # 오른쪽 버튼 줄 높이(y 940 아래)에서 x 940 넘음
    r['f_btn_mw'] = frac(lambda b: b[2] > 907 and b[3] > 1414) # 모바일 웹 실측 버튼 칸(x 907~, y 1414~)과 겹침
    r['x1_p95'] = round(sorted(b[2] for _, b in allb)[int(0.95 * (len(allb) - 1))]) if allb else None
    r['x0_p05'] = round(sorted(b[0] for _, b in allb)[int(0.05 * (len(allb) - 1))]) if allb else None
    r['y1_p95'] = round(sorted(b[3] for _, b in allb)[int(0.95 * (len(allb) - 1))]) if allb else None
    # 가장 넓은 상자들의 가운데 x(줄 정렬)
    wide = [b for _, b in allb if b[2] - b[0] >= 300]
    r['wide_cx'] = med([(b[0] + b[2]) / 2 for b in wide])
    return r

def long_row(d):
    fr = d['frames']; H = 1080
    cap = [b for f in fr for b in f['boxes'] if (b[1] + b[3]) / 2 > 0.80 * H and b[3] - b[1] >= 12]
    tx = [f for f in fr if f.get('nlines')]
    return {'cap_cy': med([(b[1] + b[3]) / 2 for b in cap]), 'cap_h': med([b[3] - b[1] for b in cap]), 'cap_cx': med([(b[0] + b[2]) / 2 for b in cap]),
            'cap_w': med([b[2] - b[0] for b in cap]), 'cap_frames': round(len({id(f) for f in fr for b in f['boxes'] if (b[1] + b[3]) / 2 > 0.8 * H}) / max(len(fr), 1), 2),
            'maxh_med': med([f['maxh'] for f in tx]), 'maxh_p75': round(sorted(f['maxh'] for f in tx)[int(0.75 * (len(tx) - 1))], 1) if tx else None,
            'lines_med': med([f['nlines'] for f in tx]), 'text_frames': round(len(tx) / max(len(fr), 1), 2)}

rows = []
for p in sorted(glob.glob(os.path.join(HERE, 'res', '*.json'))):
    d = json.load(open(p, encoding='utf-8'))
    for f in d['frames']: f['boxes'] = lines(f['boxes'])
    base = {'kind': d['kind'], 'id': d['id'], 'ch': NAME.get(d['id'], d['id']), 'dur': d['dur'], 'measured': d['measured'], 'w': d['w'], 'h': d['h'],
            'cuts_pm': d['cuts_pm'], 'cuts_mid_pm': d.get('cuts_mid_pm'), 'scene_med': d['scene_med'], 'scene_mid_med': d.get('scene_mid_med'), 'scene_max': d['scene_max'],
            'lufs': d.get('lufs'), 'lra': d.get('lra'), 'rate': d.get('rate'), 'rate_all': d.get('rate_all'), 'floor_gap_db': d.get('floor_gap_db'),
            'win_p05_db': d.get('win_p05_db'), 'win_med_db': d.get('win_med_db'), 'bed_gap_db': d.get('bed_gap_db'), 'n_words': d.get('n_words')}
    # 컷을 1초 안에 몰린 것은 하나로(겹쳐 넘기기·번쩍임이 여러 번 잡힌다)
    def merge(cs):
        out = []
        for c in cs:
            if c < d['measured'] and (not out or c - out[-1] >= 1.0): out.append(c)
        return out
    for key, cs in (('', d['cuts']), ('mid_', d.get('cuts_mid', []))):
        m = merge(cs); e = [0.0] + m + [d['measured']]; sg = [b - a for a, b in zip(e, e[1:]) if b > a]
        base[f'cuts1_{key}pm'] = round(len(m) / (d['measured'] / 60), 2) if d['measured'] else 0
        base[f'scene1_{key}med'] = round(st.median(sg), 1) if sg else None
        base[f'scene1_{key}p90'] = round(sorted(sg)[int(0.9 * (len(sg) - 1))], 1) if sg else None
    base.update(short_row(d) if d['kind'] == 'short' else long_row(d))
    rows.append(base)
keys = list(dict.fromkeys(k for r in rows for k in r))
with open(os.path.join(HERE, 'summary.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, keys); w.writeheader(); w.writerows(rows)
json.dump(rows, open(os.path.join(HERE, 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for kind in ('short', 'long'):
    R = [r for r in rows if r['kind'] == kind and not r['id'].startswith('OURS')]
    print(f'== {kind} 경쟁 {len(R)}편 중앙값')
    for k in keys:
        v = [r[k] for r in R if isinstance(r.get(k), (int, float)) and not isinstance(r.get(k), bool)]
        if v and k not in ('w', 'h'): print(f'  {k}: 중앙 {round(st.median(v), 2)} · 범위 {min(v)}~{max(v)} (n={len(v)})')
    for r in rows:
        if r['kind'] == kind and r['id'].startswith('OURS'): print('  우리', r)
