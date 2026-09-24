# 부동산 히트맵 — 사장님 2026-09-23 "부동산도 히트맵도 만들어주는 건?"
# 주식 히트맵(heatmap.py)과 같은 화면을 서울 25개 구로 그린다. 그리는 코드는 heatmap.py를 그대로 쓴다.
#   py -3.12 work/heatmap_re.py                 → 전세가율(아파트)
#   py -3.12 work/heatmap_re.py jeonse          → 전세가율 = 전세 중앙값 / 매매 중앙값
#   py -3.12 work/heatmap_re.py yield           → 아파트 월세 수익률 = 월세*12 / (매매-보증금)
#   py -3.12 work/heatmap_re.py offi            → 오피스텔 월세 수익률
#   py -3.12 work/heatmap_re.py price           → 3.3㎡(평)당 매매가
#   [--out <경로.png>]
#
# 면적 = 그 구의 거래 건수(많이 거래된 구가 크게), 색 = 그 지표(높을수록 초록).
# 자료: 국토교통부 실거래가 오픈API로 받아 work/research/rt/ 에 쌓아 둔 원자료(rtmolit.py).
# 규칙: 화면에 보이는 건 실거래 숫자뿐이다. '사라·사지 마라'는 그리지 않는다(B10과 같은 규칙).
import sys, os, re, json, glob, time, collections, statistics
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import heatmap as HM
OUT = os.path.join(HERE, 'research', '_shots')

def num(s):
    try: return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
    except Exception: return 0.0

def load(pattern, drop_offi=False):
    """glob '*_trade.json'은 '*_offi_trade.json'까지 잡는다. 아파트 매매에 오피스텔이 섞이면
    매매 중앙값이 내려가 전세가율이 105%처럼 말이 안 되는 값으로 나온다(2026-09-23 확인)."""
    rows = []
    for f in glob.glob(os.path.join(HERE, 'research', 'rt', pattern)):
        if drop_offi and '_offi_' in os.path.basename(f): continue
        try: d = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        rows += d if isinstance(d, list) else (d.get('rows') or [])
    return rows

def area_key(r): return int(num(r.get('excluUseAr')) // 5 * 5)

# 아파트 실거래에는 구 이름(sggNm)이 없고 코드(sggCd)만 있다. 오피스텔에는 이름이 있다(2026-09-23 확인).
try: SGG = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
except Exception: SGG = {}

def sgg_of(r):
    return r.get('sggNm') or SGG.get(str(r.get('sggCd', '')).strip())

def price_change(min_pairs=5):
    """구 전체의 평당가 등락률. 같은 단지·같은 5㎡ 면적대끼리 첫 달과 끝 달을 견주고,
    거래가 많은 단지에 무게를 더 준다(사장님 2026-09-24 "저 등락률은 구 전체의 등락률").

    왜 이렇게까지 맞추나 — 2026-09-23에 실제로 겪은 것:
      아무것도 안 맞추면            광진 -36.8%   (그달 거래된 평수가 달라진 착시)
      면적대만 맞추면               양천 -25.1%   (같은 면적대 안 목동과 신월동이 섞임)
      단지·면적대를 맞추면          양천  +2.6%   (서울 전체가 -1% ~ +5% 안으로 들어옴)
    앞의 두 값은 글에 쓰면 거짓이 된다."""
    cell = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in glob.glob(os.path.join(HERE, 'research', 'rt', '*_trade.json')):
        if '_offi_' in os.path.basename(f): continue
        ym = os.path.basename(f).split('_')[1]
        try: rows = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for r in rows:
            g = sgg_of(r); ar = num(r.get('excluUseAr')); a = num(r.get('dealAmount'))
            nm = (r.get('aptNm') or '').strip()
            if not g or not nm or ar <= 0 or a <= 0: continue
            cell[(g, nm, int(ar // 5 * 5))][ym].append(a / (ar / 3.3058))
    months = sorted({m for v in cell.values() for m in v})
    wsum, wn, pairs = collections.Counter(), collections.Counter(), collections.Counter()
    for (g, _, _), bym in cell.items():
        ms = [m for m in months if bym.get(m)]
        if len(ms) < 2: continue
        f0, l0 = statistics.median(bym[ms[0]]), statistics.median(bym[ms[-1]])
        if f0 <= 0: continue
        n = sum(len(v) for v in bym.values())
        wsum[g] += (l0 - f0) / f0 * 100 * n; wn[g] += n; pairs[g] += 1
    return {g: wsum[g] / wn[g] for g in wn if pairs[g] >= min_pairs}, months, pairs

def gather(kind):
    """구별 지표를 낸다. 같은 구·같은 5㎡ 면적대끼리만 짝지어 계산한다(면적이 섞이면 뜻이 없다)."""
    if kind == 'offi': tr, rt = load('*_offi_trade.json'), load('*_offi_rent.json')
    else:              tr, rt = load('*_trade.json', drop_offi=True), load('*_rent.json', drop_offi=True)
    T, R = collections.defaultdict(list), collections.defaultdict(list)
    for r in tr:
        sgg = sgg_of(r)
        if sgg: T[(sgg, area_key(r))].append(num(r.get('dealAmount')))
    for r in rt:
        sgg = sgg_of(r)
        if not sgg: continue
        R[(sgg, area_key(r))].append((num(r.get('deposit')), num(r.get('monthlyRent'))))
    per = collections.defaultdict(list); cnt = collections.Counter()
    for key in set(T) & set(R):
        sgg = key[0]; t = T[key]; rs = R[key]
        if len(t) < 3 or len(rs) < 3: continue
        mm = statistics.median(t); cnt[sgg] += len(t)
        if kind == 'jeonse':
            js = [d for d, m in rs if m == 0]                       # 전세만
            if len(js) < 3 or mm <= 0: continue
            per[sgg].append(statistics.median(js) / mm * 100)
        elif kind == 'price':
            ar = key[1] + 2.5
            if ar <= 0: continue
            per[sgg].append(mm / (ar / 3.3058))                     # 평당 만원
        else:                                                       # yield / offi
            ws = [(d, m) for d, m in rs if m > 0]
            if len(ws) < 3: continue
            dep = statistics.median(d for d, _ in ws); mo = statistics.median(m for _, m in ws)
            inv = mm - dep
            if inv <= 0 or dep > mm * 0.5 or mo < 30: continue      # 반전세는 수익률이 튀어 뺀다
            per[sgg].append(mo * 12 / inv * 100)
    return {k: statistics.median(v) for k, v in per.items() if v}, cnt

LABEL = {'jeonse': ('아파트 전세가율', '%', '전세 중앙값 ÷ 매매 중앙값'),
         'yield':  ('아파트 월세 수익률', '%', '월세×12 ÷ (매매−보증금)'),
         'offi':   ('오피스텔 월세 수익률', '%', '월세×12 ÷ (매매−보증금)'),
         'price':  ('아파트 평당 매매가', '만원', '매매 중앙값 ÷ 평')}

SEOUL = set(SGG.values())          # seoul_sgg.json의 구 이름 25개

def area_name(vals):
    """실제로 그린 지역에 맞는 이름을 만든다.
    2026-09-24: 라벨이 '서울 25개 구'로 박혀 있었는데 work/research/rt/에 경기도(41xxx)
    실거래가 함께 쌓여 안성시·파주시까지 62곳이 그려졌다. 글에 그대로 쓰면 사실이 틀린다."""
    ks = set(vals); out = ks - SEOUL
    if not out: return f'서울 {len(ks)}개 구'
    if not (ks & SEOUL): return f'경기 {len(ks)}곳'
    return f'수도권 {len(ks)}곳(서울 {len(ks & SEOUL)}개 구·경기 {len(out)}곳)'

def main():
    kind = next((a for a in sys.argv[1:] if not a.startswith('--')), 'jeonse')
    out = None
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    title, unit, how = LABEL.get(kind, LABEL['jeonse'])
    vals, cnt = gather(kind)
    if '--seoul' in sys.argv:                       # 서울만 그린다(경기 실거래를 뺀다)
        vals = {k: v for k, v in vals.items() if k in SEOUL}
    if not vals: print('자료가 모자라 그릴 수 없다 — work/research/rt/ 에 실거래 원자료가 있는지 본다'); return
    title = f'{area_name(vals)} {title}'            # 이름은 실제 그린 지역으로

    if kind == 'price':
        # 사장님 2026-09-23: "부동산은 주식과 달리 구역별로 가치가 명확히 나뉜다.
        #   시총을 못 구해도 값어치로 보면 등수가 정해진다."
        # 그래서 이 그림만 크기 = 평당가(그 구의 급지), 색 = 평당가 등락률로 그린다.
        chg, months, pairs = price_change()
        # 구 이름을 그대로 쓴다(사장님 2026-09-24 "구도 붙여").
        # 등락률을 못 구한 구는 0%(회색)로 그리면 '변동 없음'과 구분이 안 된다 → 글자로 밝힌다.
        rows = [{'sym': k, 'sector': '서울', 'cap': v,
                 'pct': chg.get(k, 0.0),
                 'label': (f'{v:,.0f}만원 {chg[k]:+.1f}%' if k in chg else f'{v:,.0f}만원 (등락 자료 부족)')}
                for k, v in vals.items()]
        day = time.strftime('%Y-%m-%d'); os.makedirs(OUT, exist_ok=True)
        out = out or os.path.join(OUT, f'heatmap_re_price_{day}.png')
        span = f'{months[0]}→{months[-1]}' if months else ''
        HM.draw(rows, out, f'{area_name(vals)} 아파트 평당 매매가 {day} · 크기=평당가, 색={span} 등락률(같은 단지·같은 면적대)')
        print(f'{area_name(vals)} 아파트 평당 매매가 — 크기는 평당가, 색은 같은 면적대끼리 견준 등락률')
        print(f'  지역 {len(vals)}곳 · 평당가 중앙 {statistics.median(vals.values()):,.0f}만원 · '
              f'등락률 중앙 {statistics.median(chg.values()):+.1f}% (구한 곳 {len(chg)}곳) · 그림 {out}')
        for k, v in sorted(vals.items(), key=lambda kv: -kv[1])[:5]:
            print(f'  비싼 곳 {k} 평당 {v:,.0f}만원 ({chg.get(k, 0):+.1f}%)')
        for k, v in sorted(vals.items(), key=lambda kv: kv[1])[:3]:
            print(f'  싼 곳   {k} 평당 {v:,.0f}만원 ({chg.get(k, 0):+.1f}%)')
        return

    mid = statistics.median(vals.values())
    # 이름은 맨 끝 '구'만 뗀다. replace로 지우면 '구로구'가 '로'가 된다(2026-09-23 확인).
    # 색은 중앙값 대비 편차로 내되, 칸에 찍는 숫자는 실제 지표값이다.
    fmt = (lambda x: f'{x:,.0f}{unit}') if kind == 'price' else (lambda x: f'{x:.2f}{unit}')
    rows = [{'sym': re.sub(r'구$', '', k), 'sector': '서울', 'cap': max(cnt[k], 1),
             'pct': (v - mid) / (mid or 1) * 100 / 8, 'label': fmt(v)} for k, v in vals.items()]
    day = time.strftime('%Y-%m-%d')
    os.makedirs(OUT, exist_ok=True)
    out = out or os.path.join(OUT, f'heatmap_re_{kind}_{day}.png')
    HM.draw(rows, out, f'{title} · {day} · 면적=거래건수, 색=중앙값 대비 (중앙 {mid:.2f}{unit})')
    print(f'{title} — {how}')
    print(f'  구 {len(vals)}곳 · 중앙값 {mid:.2f}{unit} · 그림 {out}')
    for k, v in sorted(vals.items(), key=lambda kv: -kv[1])[:5]:
        print(f'  높은 곳 {k} {v:.2f}{unit} (거래 {cnt[k]}건)')
    for k, v in sorted(vals.items(), key=lambda kv: kv[1])[:3]:
        print(f'  낮은 곳 {k} {v:.2f}{unit} (거래 {cnt[k]}건)')

if __name__ == '__main__': main()
