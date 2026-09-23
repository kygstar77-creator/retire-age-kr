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

LABEL = {'jeonse': ('서울 25개 구 아파트 전세가율', '%', '전세 중앙값 ÷ 매매 중앙값'),
         'yield':  ('서울 25개 구 아파트 월세 수익률', '%', '월세×12 ÷ (매매−보증금)'),
         'offi':   ('서울 25개 구 오피스텔 월세 수익률', '%', '월세×12 ÷ (매매−보증금)'),
         'price':  ('서울 25개 구 아파트 평당 매매가', '만원', '매매 중앙값 ÷ 평')}

def main():
    kind = next((a for a in sys.argv[1:] if not a.startswith('--')), 'jeonse')
    out = None
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    title, unit, how = LABEL.get(kind, LABEL['jeonse'])
    vals, cnt = gather(kind)
    if not vals: print('자료가 모자라 그릴 수 없다 — work/research/rt/ 에 실거래 원자료가 있는지 본다'); return
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
