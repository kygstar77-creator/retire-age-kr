# 부동산 히트맵 — 사장님 2026-09-23 "부동산도 히트맵도 만들어주는 건?"
# 주식 히트맵(heatmap.py)과 같은 화면을 서울 25개 구로 그린다. 그리는 코드는 heatmap.py를 그대로 쓴다.
#   py -3.12 work/heatmap_re.py                 → 전세가율(아파트)
#   py -3.12 work/heatmap_re.py jeonse          → 전세가율 = 전세 중앙값 / 매매 중앙값
#   py -3.12 work/heatmap_re.py yield           → 아파트 월세 수익률 = (월세 + 보증금×전환율/12)*12 / 매매
#   py -3.12 work/heatmap_re.py offi            → 오피스텔 월세 수익률
#   py -3.12 work/heatmap_re.py price           → 3.3㎡(평)당 매매가
#   [--out <경로.png>]
#
# 면적 = 평당 값(평당가 그림은 평당 매매가, 전세가율은 평당 전세가, 월세 수익률은 평당 월세), 색 = 그 지표(높을수록 초록).
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
    return [r for r in rows if keep(r)]

def keep(r):
    """해제된 거래와 공공기관 일괄 매입을 뺀다. 2026-09-27 확인: 7~8월 서울 아파트 매매 9,295건 중
    433건이 공공기관 매수였고, 중랑구 신축 한 곳은 7월 9일 하루에 전용 18㎡ 278건이 한꺼번에 잡혔다.
    매입임대용 소형 신축이라 구 평당가·단지 순위를 흔든다."""
    return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'

def area_key(r): return int(num(r.get('excluUseAr')) // 5 * 5)

# 아파트 실거래에는 구 이름(sggNm)이 없고 코드(sggCd)만 있다. 오피스텔에는 이름이 있다(2026-09-23 확인).
try: SGG = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
except Exception: SGG = {}

def sgg_of(r):
    return r.get('sggNm') or SGG.get(str(r.get('sggCd', '')).strip())

def price_change(min_pairs=5, offi=False):
    """구 전체의 평당가 등락률. 같은 단지·같은 5㎡ 면적대끼리 첫 달과 끝 달을 견주고,
    거래가 많은 단지에 무게를 더 준다(사장님 2026-09-24 "저 등락률은 구 전체의 등락률").

    왜 이렇게까지 맞추나 — 2026-09-23에 실제로 겪은 것:
      아무것도 안 맞추면            광진 -36.8%   (그달 거래된 평수가 달라진 착시)
      면적대만 맞추면               양천 -25.1%   (같은 면적대 안 목동과 신월동이 섞임)
      단지·면적대를 맞추면          양천  +2.6%   (서울 전체가 -1% ~ +5% 안으로 들어옴)
    앞의 두 값은 글에 쓰면 거짓이 된다."""
    cell = collections.defaultdict(lambda: collections.defaultdict(list))
    # 오피스텔도 같은 식으로 잰다. 사장님 2026-09-24 "오피스텔도 평당가로 해야 하는 거 아니야".
    # 오피스텔은 단지 이름이 aptNm이 아니라 offiNm 으로 온다.
    for f in glob.glob(os.path.join(HERE, 'research', 'rt', '*_trade.json')):
        is_offi = '_offi_' in os.path.basename(f)
        if is_offi != offi: continue
        ym = os.path.basename(f).split('_')[1]
        try: rows = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for r in rows:
            g = sgg_of(r); ar = num(r.get('excluUseAr')); a = num(r.get('dealAmount'))
            nm = ((r.get('offiNm') if offi else r.get('aptNm')) or '').strip()
            if not g or not nm or ar <= 0 or a <= 0 or not keep(r): continue
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

def conv_rate(rt, offi=False, min_pairs=30):
    """구별 전월세 전환율(%) = 월세×12 ÷ (같은 단지·같은 면적대 전세 중앙값 − 그 월세 계약의 보증금).
    반전세·월세를 전세나 순수 월세로 바꿀 때 쓴다(사장님 2026-09-27 "반전세는 결국 평당 전세가, 평당 월세가를
    뭔가 환산해야겠지?"). 재는 법은 research/jeonwol0927/conv.py와 같다 — 그때 서울 아파트 8,410쌍 중앙값 4.8%.
    표본이 min_pairs 미만인 구는 전체 중앙값을 쓴다."""
    C = collections.defaultdict(lambda: ([], []))
    for r in rt:
        g = sgg_of(r); nm = ((r.get('offiNm') if offi else r.get('aptNm')) or '').strip(); ar = num(r.get('excluUseAr'))
        if not g or not nm or ar <= 0: continue
        d, m = num(r.get('deposit')), num(r.get('monthlyRent'))
        k = (g, nm, int(ar // 5 * 5))
        if m == 0: C[k][0].append(d)
        else: C[k][1].append((d, m))
    per = collections.defaultdict(list); allv = []
    for k, (js, ws) in C.items():
        if len(js) < 2 or not ws: continue
        J = statistics.median(js)
        for d, m in ws:
            if J - d < J * 0.2: continue                    # 보증금이 전세에 거의 붙으면 값이 튄다
            v = m * 12 / (J - d) * 100
            if 0 < v < 20: per[k[0]].append(v); allv.append(v)
    base = statistics.median(allv) if allv else 4.8
    return {g: (statistics.median(v) if len(v) >= min_pairs else base) for g, v in per.items()}, base, len(allv)

def gather(kind):
    """구별 지표를 낸다. 같은 구·같은 5㎡ 면적대끼리만 짝지어 계산한다(면적이 섞이면 뜻이 없다)."""
    # 최근 석 달만 쓴다. 2026-09-24부터 rt/에 2021년 10~12월(고점 비교용)이 같이 쌓여
    # 2021년 매매와 2026년 전월세가 한 칸에 섞였다(2026-09-27 02시 회차가 발견).
    ms = sorted({os.path.basename(f).split('_')[1] for f in glob.glob(os.path.join(HERE, 'research', 'rt', '*_rent.json'))})[-3:]
    tr, rt = [], []
    for m in ms:
        if kind in ('offi', 'offiprice'): tr += load(f'*_{m}_offi_trade.json'); rt += load(f'*_{m}_offi_rent.json')
        else:              tr += load(f'*_{m}_trade.json', drop_offi=True); rt += load(f'*_{m}_rent.json', drop_offi=True)
    T, R = collections.defaultdict(list), collections.defaultdict(list)
    for r in tr:
        sgg = sgg_of(r)
        if sgg: T[(sgg, area_key(r))].append(num(r.get('dealAmount')))
    for r in rt:
        sgg = sgg_of(r)
        if not sgg: continue
        R[(sgg, area_key(r))].append((num(r.get('deposit')), num(r.get('monthlyRent'))))
    per = collections.defaultdict(list); cnt = collections.Counter()
    # 칸 크기 — 전세 그림은 평당 전세가, 월세 그림은 평당 월세. 반전세·월세는 구별 전환율로 바꿔 넣는다:
    #   전세 환산 = 보증금 + 월세×12 ÷ 전환율      월세 환산(보증금 0) = 월세 + 보증금 × 전환율 ÷ 12
    # 2026-09-27 앞 버전은 순수 전세·반전세 뺀 월세만 세서, 보증금을 크게 거는 강남 월세가 싸게 나왔다.
    size = collections.defaultdict(list)
    rate, rbase, rn = conv_rate(rt, offi=(kind in ('offi', 'offiprice'))) if kind in ('jeonse', 'yield', 'offi') else ({}, 4.8, 0)
    for key, rs in R.items():
        if kind not in ('jeonse', 'yield', 'offi') or len(rs) < 3: continue
        py = (key[1] + 2.5) / 3.3058
        r = rate.get(key[0], rbase) / 100
        if kind == 'jeonse': v = [d + m * 12 / r for d, m in rs]             # 전세·반전세·월세 전부 전세로
        else:
            ws = [(d, m) for d, m in rs if m > 0]                              # 월세·반전세만, 보증금 0으로
            if len(ws) < 3: continue
            v = [m + d * r / 12 for d, m in ws]
        size[key[0]].append(statistics.median(v) / py)
    for key in set(T) & set(R):
        sgg = key[0]; t = T[key]; rs = R[key]
        if len(t) < 3 or len(rs) < 3: continue
        mm = statistics.median(t); cnt[sgg] += len(t)
        py = (key[1] + 2.5) / 3.3058                                # 이 면적대의 평 수(가운데 값)
        if kind == 'jeonse':
            js = [d for d, m in rs if m == 0]                       # 전세만
            if len(js) < 3 or mm <= 0: continue
            per[sgg].append(statistics.median(js) / mm * 100)
        elif kind in ('price', 'offiprice'):
            ar = key[1] + 2.5
            if ar <= 0: continue
            per[sgg].append(mm / (ar / 3.3058))                     # 평당 만원
        else:                                                       # yield / offi
            # 수익률 = 환산 월세(보증금 0) × 12 ÷ 매매가. 사장님 2026-09-27 "바꿔" — 칸 크기와 같은 환산을 쓴다.
            # 옛 식(월세×12 ÷ (매매−보증금))은 보증금이 클수록 분모가 줄어 튀어서 반전세를 통째로 뺐다.
            ws = [(d, m) for d, m in rs if m > 0]
            if len(ws) < 3 or mm <= 0: continue
            r = rate.get(sgg, rbase) / 100
            per[sgg].append(statistics.median(m + d * r / 12 for d, m in ws) * 12 / mm * 100)
    if rn: print(f'  전월세 전환율 — 같은 단지·면적대 {rn:,}쌍, 중앙 {rbase:.2f}% (구별 값으로 환산)')
    return ({k: statistics.median(v) for k, v in per.items() if v}, cnt,
            {k: statistics.median(v) for k, v in size.items() if v})

LABEL = {'jeonse': ('아파트 전세가율', '%', '전세 중앙값 ÷ 매매 중앙값'),
         'yield':  ('아파트 월세 수익률', '%', '환산 월세(보증금 0)×12 ÷ 매매가'),
         'offi':   ('오피스텔 월세 수익률', '%', '환산 월세(보증금 0)×12 ÷ 매매가'),
         'price':  ('아파트 평당 매매가', '만원', '매매 중앙값 ÷ 평'),
         'offiprice': ('오피스텔 평당 매매가', '만원', '매매 중앙값 ÷ 평')}

SEOUL = set(SGG.values())          # seoul_sgg.json의 구 이름 25개
# 인천(2026-07 행정구역 개편 뒤 이름). 옛 이름(중구·동구·서구)은 서울 구와 겹칠 수 있어 새 이름만 둔다.
INCHEON = {'영종구', '제물포구', '검단구', '서해구', '계양구', '남동구', '미추홀구', '부평구', '연수구', '강화군', '옹진군'}

def area_name(vals):
    """실제로 그린 지역에 맞는 이름을 만든다.
    2026-09-24: 라벨이 '서울 25개 구'로 박혀 있었는데 work/research/rt/에 경기도(41xxx)
    실거래가 함께 쌓여 안성시·파주시까지 62곳이 그려졌다. 글에 그대로 쓰면 사실이 틀린다."""
    # 2026-09-28: 인천 구(영종·제물포·검단·서해·계양·남동·미추홀·부평·연수)까지 '경기'로 세어
    # '경기 46곳'이라 찍혔다. 인천은 따로 센다.
    ks = set(vals); inc = ks & INCHEON; out = ks - SEOUL - INCHEON
    if not (out or inc): return f'서울 {len(ks)}개 구'
    parts = [f'서울 {len(ks & SEOUL)}개 구'] if ks & SEOUL else []
    if out: parts.append(f'경기 {len(out)}곳')
    if inc: parts.append(f'인천 {len(inc)}곳')
    if len(parts) == 1: return parts[0]
    return f'수도권 {len(ks)}곳(' + '·'.join(parts) + ')'

def main():
    kind = next((a for a in sys.argv[1:] if not a.startswith('--')), 'jeonse')
    out = None
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    title, unit, how = LABEL.get(kind, LABEL['jeonse'])
    vals, cnt, size = gather(kind)
    if '--seoul' in sys.argv:                       # 서울만 그린다(경기 실거래를 뺀다)
        vals = {k: v for k, v in vals.items() if k in SEOUL}
    if not vals: print('자료가 모자라 그릴 수 없다 — work/research/rt/ 에 실거래 원자료가 있는지 본다'); return
    title = f'{area_name(vals)} {title}'            # 이름은 실제 그린 지역으로

    if kind in ('price', 'offiprice'):
        # 사장님 2026-09-23: "부동산은 주식과 달리 구역별로 가치가 명확히 나뉜다.
        #   시총을 못 구해도 값어치로 보면 등수가 정해진다."
        # 그래서 이 그림만 크기 = 평당가(그 구의 급지), 색 = 평당가 등락률로 그린다.
        chg, months, pairs = price_change(offi=(kind == 'offiprice'))
        # vals는 --seoul 로 걸렀는데 chg는 안 걸러, 화면에 찍는 '등락률 중앙값'이
        # 경기까지 섞인 값으로 나왔다(2026-09-24: 지역 25곳인데 '구한 곳 46곳').
        chg = {k: v for k, v in chg.items() if k in vals}
        # 구 이름을 그대로 쓴다(사장님 2026-09-24 "구도 붙여").
        # 등락률을 못 구한 구는 0%(회색)로 그리면 '변동 없음'과 구분이 안 된다 → 글자로 밝힌다.
        rows = [{'sym': k, 'sector': '서울', 'cap': v,
                 'pct': chg.get(k, 0.0),
                 'label': (f'{v:,.0f}만원 {chg[k]:+.1f}%' if k in chg else f'{v:,.0f}만원 (등락 자료 부족)')}
                for k, v in vals.items()]
        day = time.strftime('%Y-%m-%d'); os.makedirs(OUT, exist_ok=True)
        out = out or os.path.join(OUT, f'heatmap_re_{kind}_{day}.png')
        span = f'{months[0]}→{months[-1]}' if months else ''
        what = '오피스텔' if kind == 'offiprice' else '아파트'
        HM.draw(rows, out, f'{area_name(vals)} {what} 평당 매매가 {day} · 크기=평당가, 색={span} 등락률(같은 단지·같은 면적대)')
        print(f'{area_name(vals)} {what} 평당 매매가 — 크기는 평당가, 색은 같은 면적대끼리 견준 등락률')
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
    # 면적은 거래 건수가 아니라 그 그림이 다루는 시장의 평당 값이다(사장님 2026-09-27 "면적을 평당가로 하라 했지"
    # → "전세가율이랑 월세수익률은 평당 전세가랑 평당 월세가 인가?" → "바꿔").
    # 전세가율 = 평당 전세가, 월세 수익률(아파트·오피스텔) = 평당 월세. 매매가로 크기를 잡으면
    # 전세가율(전세÷매매)과 크기가 같은 매매가에 묶여 비싼 구가 늘 크고 빨갛게만 나온다.
    pp = size
    pmid = statistics.median(pp.values()) if pp else 1
    sunit = '평당 전세가(환산)' if kind == 'jeonse' else '평당 월세(보증금 0 환산)'
    miss = [k for k in vals if k not in pp]
    rows = [{'sym': re.sub(r'구$', '', k), 'sector': '서울', 'cap': pp.get(k, pmid),
             'pct': (v - mid) / (mid or 1) * 100 / 8, 'label': fmt(v)} for k, v in vals.items()]
    day = time.strftime('%Y-%m-%d')
    os.makedirs(OUT, exist_ok=True)
    out = out or os.path.join(OUT, f'heatmap_re_{kind}_{day}.png')
    HM.draw(rows, out, f'{title} · {day} · 크기={sunit}, 색=중앙값 대비 (중앙 {mid:.2f}{unit})')
    if miss: print(f'  {sunit}를 못 구한 곳 {len(miss)}곳은 중앙값 크기로 그렸다: {", ".join(miss)}')
    print(f'{title} — {how}')
    print(f'  구 {len(vals)}곳 · 중앙값 {mid:.2f}{unit} · 그림 {out}')
    for k, v in sorted(vals.items(), key=lambda kv: -kv[1])[:5]:
        print(f'  높은 곳 {k} {v:.2f}{unit} ({sunit} {pp.get(k, 0):,.1f}만원)')
    for k, v in sorted(vals.items(), key=lambda kv: kv[1])[:3]:
        print(f'  낮은 곳 {k} {v:.2f}{unit} ({sunit} {pp.get(k, 0):,.1f}만원)')

if __name__ == '__main__': main()
