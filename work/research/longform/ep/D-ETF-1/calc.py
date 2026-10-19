# -*- coding: utf-8 -*-
"""D-ETF-1 배당 ETF 계산 — 원자료는 전부 raw/(2026-10-19 받음). 결과 calc_out.txt·calc_out.json(대본·화면은 이 두 파일만 본다).

1) 섹터 비중(ETF × GICS 11개 + 기타)
   - 운용사 보유 종목 표에 섹터가 있는 것: SCHD(슈왑 전체 보유 CSV 10/15)·DGRO·HDV(아이셰어즈 CSV 10/15) → 우리가 종목 비중을 섹터별로 더함
   - 섹터가 없는 것: VYM·VIG(뱅가드 보유 9/30)·SPYD(스테이트스트리트 보유 10/15) → 같은 날 아이셰어즈 ITOT(미국 전체 2,4xx종목) 섹터로 종목마다 붙여 더함
   - JEPI·JEPQ: JP모건 운용사 섹터 표(10/16) 그대로(기타 = 옵션 연계 채권 ELN·현금)
   - DIVO: 앰플리파이 운용사 섹터 표(9/30) 그대로
   - 국내 상장: 네이버 증권 ETF 분석 섹터 표(10/16) — 운용사 원문 대조 안 함(미래에셋 구성종목 응답 비어 있음 10/19)
2) 분배율·분배 성장률·총수익·최대 낙폭 — 야후 일별 가격·분배 이력(분할 반영), 원화는 ECOS 731Y001 매매기준율
3) 1억 넣으면 1년 통장 — 세금(미국 원천 15%, 국내 15.4%)·건보료(지역가입자 금융소득 1,000만원 넘으면 전액 × 8.1348%)
"""
import csv, json, pathlib, datetime, re, collections
import openpyxl

HERE = pathlib.Path(__file__).resolve().parent; RAW = HERE / 'raw'
SEC = ['정보기술', '금융', '헬스케어', '필수소비재', '에너지', '산업재', '경기소비재', '통신', '유틸리티', '부동산', '소재', '기타']
EN = {'Information Technology': '정보기술', 'Financials': '금융', 'Health Care': '헬스케어', 'Consumer Staples': '필수소비재',
      'Energy': '에너지', 'Industrials': '산업재', 'Consumer Discretionary': '경기소비재', 'Communication': '통신',
      'Communication Services': '통신', 'Utilities': '유틸리티', 'Real Estate': '부동산', 'Materials': '소재',
      'Cash and/or Derivatives': '기타', 'Other': '기타', 'Cash': '기타',
      'FINANCIALS': '금융', 'INDUSTRIALS': '산업재', 'COMMUNICATION': '통신', 'CONSUMER_DISCRETIONARY': '경기소비재',
      'CONSUMER_STAPLES': '필수소비재', 'UTILITIES': '유틸리티', 'MATERIALS': '소재', 'UNCLASSIFIED': '기타', 'ENERGY': '에너지',
      'HEALTHCARE': '헬스케어', 'IT': '정보기술', 'REAL_ESTATE': '부동산'}
norm = lambda t: re.sub(r'[^A-Z0-9]', '', (t or '').upper())


def ishares(path):
    rows = list(csv.reader(open(path, encoding='utf-8-sig')))
    h = next(i for i, r in enumerate(rows) if r and r[0] == 'Ticker'); hd = rows[h]
    out = []
    for r in rows[h + 1:]:
        if len(r) < len(hd) or not r[0]: continue
        d = dict(zip(hd, r))
        try: out.append((d['Ticker'], d['Sector'], float(d['Weight (%)'].replace(',', '')), float(d['Market Value'].replace(',', ''))))
        except ValueError: pass
    return out


GICS = {norm(t): s for t, s, w, mv in ishares(RAW / 'ish_ITOT_20261019.csv')}
GICS.update({'BRKB': 'Financials', 'BFB': 'Consumer Staples'})


def by_sector(items):  # items: (섹터 영문, 비중%)
    c = collections.Counter()
    for s, w in items: c[EN.get(s, '기타')] += w
    tot = sum(c.values())
    return {k: round(c[k] / tot * 100, 2) for k in SEC}, tot


sectors, meta = {}, {}
# SCHD — 슈왑 보유 CSV
r = [x for x in csv.DictReader(open(RAW / 'schwab_SCHD_holdings_20261019.CSV', encoding='utf-8-sig')) if x.get('Percent of Assets') and re.match(r'20\d\d-', x['As-Of-Date'] or '')]
sectors['SCHD'], t = by_sector([(x['Sector'], float(x['Percent of Assets'])) for x in r])
meta['SCHD'] = f"슈왑 전체 보유 {len(r)}종목 {r[0]['As-Of-Date']} 섹터 열 합산(합 {t:.2f}%)"
for k in ('DGRO', 'HDV'):
    x = ishares(RAW / f'ish_{k}_20261019.csv')
    sectors[k], t = by_sector([(s, w) for _, s, w, _ in x]); meta[k] = f'아이셰어즈 보유 {len(x)}줄 2026-10-15 섹터 열 합산(합 {t:.2f}%)'
    meta[k + '_aum'] = sum(mv for *_, mv in x)
for k in ('VYM', 'VIG'):
    d = json.load(open(RAW / f'vg_{k}_20261019.json', encoding='utf-8'))['holdingDetails']; miss = 0; it = []
    for e in d['equityHoldings']:
        w = float(e['marketValuePercentage'].rstrip('%')); s = GICS.get(norm(e['ticker']))
        if s is None: miss += w; s = 'Other'
        it.append((s, w))
    sectors[k], t = by_sector(it)
    meta[k] = f"뱅가드 보유 {len(d['equityHoldings'])}종목 {d['asOfDate']} + ITOT 섹터 매칭(못 맞춘 비중 {miss:.2f}%→기타)"
    meta[k + '_aum'] = sum(float(e['marketValueBaseCurrency'].replace('$', '').replace(',', '')) for e in d['equityHoldings'])
ws = openpyxl.load_workbook(RAW / 'ssga_SPYD_20261019.xlsx', read_only=True).active; it = []; miss = 0; n = 0
for row in list(ws.iter_rows(values_only=True))[5:]:
    if not row[1] or not isinstance(row[4], (int, float)): continue
    s = GICS.get(norm(row[1]));
    if s is None: miss += row[4]; s = 'Other'
    it.append((s, row[4])); n += 1
sectors['SPYD'], t = by_sector(it); meta['SPYD'] = f'스테이트스트리트 보유 {n}종목 2026-10-15 + ITOT 섹터 매칭(못 맞춘 비중 {miss:.2f}%→기타)'
for k in ('JEPI', 'JEPQ'):
    d = json.load(open(RAW / f'jpm_{k}_sector_20261019.json', encoding='utf-8'))
    sectors[k], t = by_sector([(x['name'], x['value']) for x in d['data']]); meta[k] = f"JP모건 운용사 섹터 표 {d['effectiveDate']}(기타=옵션 연계 채권·현금, 표 합 {t:.1f}%를 100으로 맞춤)"
txt = (RAW / 'DIVO_page_20261019.txt').read_text(encoding='utf-8')
blk = txt.split('Sector Allocation\tWeight (%)')[1].split('Distributions')[0]
sectors['DIVO'], t = by_sector([(m[0], float(m[1])) for m in re.findall(r'^([A-Za-z ]+)\t([\d.]+)%', blk, re.M)])
meta['DIVO'] = f'앰플리파이 운용사 섹터 표 2026-09-30(표 합 {t:.2f}%)'
KR = {'458730': 'TIGER 미국배당다우존스', '446720': 'SOL 미국배당다우존스', '402970': 'ACE 미국배당다우존스', '489250': 'KODEX 미국배당다우존스',
      '161510': 'PLUS 고배당주', '466940': 'TIGER 은행고배당플러스TOP10', '0105E0': 'SOL 코리아고배당'}
for c, nm in KR.items():
    d = json.load(open(RAW / f'naver_etf_{c}_20261019.json', encoding='utf-8'))
    sectors[nm], t = by_sector([(x['detailTypeCode'], x['weight']) for x in d['sectorPortfolioList']])
    meta[nm] = f"네이버 증권 ETF 분석 섹터 표(10/16 기준, 운용사 원문 대조 안 함) · 순자산 {d['totalNav']} · 시총 {d['marketValue']}"
# 슈왑 운용사 공식 섹터 표(6/30) — 우리 합산(10/15)과 대조용
schwab_official = {}
st = (RAW / 'SCHD_page_20261019.txt').read_text(encoding='utf-8')
for m in re.findall(r'^([A-Za-z ]+)\t\n([\d.]+)%', st.split('Sector\tPercent of Portfolio (%)')[1].split('Allocations are subject')[0], re.M):
    schwab_official[EN[m[0].strip()]] = float(m[1])

# ---------- 가격·분배 ----------
fx = {datetime.date(int(k[:4]), int(k[4:6]), int(k[6:])): v for k, v in json.load(open(RAW / 'ecos_731Y001_usdkrw_20261019.json')).items()}
fxd = sorted(fx)
def fxon(d):
    i = max(j for j in range(len(fxd)) if fxd[j] <= d) if fxd[0] <= d else 0
    return fx[fxd[i]]


def series(t):
    r = json.load(open(RAW / f'yh_{t}_20261019.json'))['chart']['result'][0]
    ts = [datetime.datetime.utcfromtimestamp(x).date() for x in r['timestamp']]
    cl = r['indicators']['quote'][0]['close']; ad = r['indicators']['adjclose'][0]['adjclose']
    px = [(d, c, a) for d, c, a in zip(ts, cl, ad) if c and a]
    dv = sorted((datetime.datetime.utcfromtimestamp(x['date']).date(), x['amount']) for x in r.get('events', {}).get('dividends', {}).values())
    return px, dv


def ttm(dv, end):
    return sum(a for d, a in dv if end - datetime.timedelta(days=365) < d <= end)


def at(px, d):  # d 이전 마지막 거래일
    c = [p for p in px if p[0] <= d]
    return c[-1] if c else None


US = ['SCHD', 'VYM', 'VIG', 'DGRO', 'HDV', 'SPYD', 'JEPI', 'JEPQ', 'DIVO', 'SPY']
KRT = {'458730.KS': 'TIGER 미국배당다우존스', '446720.KS': 'SOL 미국배당다우존스', '402970.KS': 'ACE 미국배당다우존스', '489250.KS': 'KODEX 미국배당다우존스',
       '161510.KS': 'PLUS 고배당주', '466940.KS': 'TIGER 은행고배당플러스TOP10', '0105E0.KS': 'SOL 코리아고배당'}
stats = {}
for t in US + list(KRT):
    px, dv = series(t); last = px[-1][0]; usd = not t.endswith('.KS')
    s = dict(name=KRT.get(t, t), last=str(last), close=round(px[-1][1], 2), first=str(px[0][0]), n_div_12m=sum(1 for d, a in dv if last - datetime.timedelta(days=365) < d <= last))
    s['ttm'] = round(ttm(dv, last), 4); s['yield'] = round(s['ttm'] / px[-1][1] * 100, 2)
    for y in (1, 3, 5, 10):
        d0 = last.replace(year=last.year - y)
        if px[0][0] > d0 - datetime.timedelta(days=370): continue
        old = ttm(dv, d0)
        if old > 0: s[f'divcagr{y}'] = round(((s['ttm'] / old) ** (1 / y) - 1) * 100, 2)
        p0 = at(px, d0)
        if p0:
            tr = px[-1][2] / p0[2]; s[f'tr{y}'] = round((tr ** (1 / y) - 1) * 100, 2)
            s[f'pr{y}'] = round(((px[-1][1] / p0[1]) ** (1 / y) - 1) * 100, 2)
            if usd:
                k = tr * fxon(last) / fxon(p0[0]); s[f'trkrw{y}'] = round((k ** (1 / y) - 1) * 100, 2)
            if y == 1: s['div_1y_ago_ttm'] = round(old, 4)
    # 해마다 분배(최근 12개월 끝을 10/16에 맞춰 1년씩 뒤로)
    s['ttm_by_year'] = {str(last.year - k): round(ttm(dv, last.replace(year=last.year - k)), 4) for k in range(0, 11) if px[0][0] <= last.replace(year=last.year - k) - datetime.timedelta(days=360)}
    # 최대 낙폭(분배 재투자 값 기준) — 2020-01-01 뒤, 그리고 2022년 안
    def mdd(rows, key):
        pk, m, when = 0, 0, None
        for r in rows:
            v = key(r); pk = max(pk, v)
            if v / pk - 1 < m: m, when = v / pk - 1, r[0]
        return round(m * 100, 1), str(when)
    r20 = [p for p in px if p[0] >= datetime.date(2020, 1, 1)]
    s['mdd_since2020'], s['mdd_since2020_at'] = mdd(r20, lambda p: p[2])
    r22 = [p for p in px if datetime.date(2022, 1, 1) <= p[0] <= datetime.date(2022, 12, 31)]
    if r22 and r22[0][0] < datetime.date(2022, 2, 1): s['mdd_2022'], _ = mdd(r22, lambda p: p[2])
    if usd:
        s['mdd_since2020_krw'], _ = mdd(r20, lambda p: p[2] * fxon(p[0]))
    if t == 'DIVO':  # 매달 분배 중 한 번 튀는 것(그 12개월 중앙값의 2.5배 넘음)을 따로 뺀 값 — 2025-12-30 0.953달러 등
        def reg(end):
            xs = [a for d, a in dv if end - datetime.timedelta(days=365) < d <= end]
            med = sorted(xs)[len(xs) // 2]; return sum(a for a in xs if a <= 2.5 * med), [a for a in xs if a > 2.5 * med]
        r0, sp0 = reg(last); s['ttm_ex_special'] = round(r0, 4); s['special_12m'] = sp0; s['yield_ex_special'] = round(r0 / px[-1][1] * 100, 2)
        for y in (3, 5):
            r5, sp5 = reg(last.replace(year=last.year - y)); s[f'divcagr{y}_ex_special'] = round(((r0 / r5) ** (1 / y) - 1) * 100, 2); s[f'special_{y}y_ago'] = sp5
    stats[t] = s

# ---------- 1억 넣으면 1년 통장(앞으로 같은 분배라고 놓은 계산) ----------
HEALTH = 0.0719 * (1 + 0.9448 / 7.19)  # 건보+장기요양 (D-1 facts [1][3], M-1 [H1])
FXNOW = fxon(datetime.date(2026, 10, 16))
won = lambda x: f'{x:,.0f}원'
eok = []
for t in US[:-1] + ['458730.KS', '161510.KS', '466940.KS']:
    s = stats[t]; usd = not t.endswith('.KS')
    gross = 1e8 * s['yield'] / 100; tax = gross * (0.15 if usd else 0.154)
    net = gross - tax; hi = gross > 1e7
    hl = gross * HEALTH if hi else 0
    eok.append(dict(t=t, name=s['name'], yield_=s['yield'], gross=round(gross), tax=round(tax), net=round(net), health=round(hl), after=round(net - hl), monthly=round((net - hl) / 12), over10m=hi, over20m=gross > 2e7))

out = []; w = out.append
w(f'# D-ETF-1 calc_out (calc.py, {datetime.date.today()}) — 원자료 raw/ · 가격 마지막 거래일 미국 2026-10-16·국내 2026-10-19 · 환율 ECOS 731Y001 2026-10-16 {FXNOW}원')
w('\n## 1. 섹터 비중(%) — ETF × 섹터')
w('ETF | ' + ' | '.join(SEC) + ' | 가장 큰 섹터 | 상위 2개 합 | 근거')
for k, v in sectors.items():
    top = sorted(v.items(), key=lambda x: -x[1])
    w(f"{k} | " + ' | '.join(f'{v[s]:.1f}' for s in SEC) + f" | {top[0][0]} {top[0][1]:.1f} | {top[0][1] + top[1][1]:.1f} | {meta[k]}")
w('\n슈왑 공식 섹터 표(2026-06-30) vs 우리 합산(2026-10-15 보유): ' + ' · '.join(f'{k} {schwab_official.get(k, 0):.2f}→{sectors["SCHD"][k]:.2f}' for k in SEC if schwab_official.get(k) or sectors['SCHD'][k]))
w('순자산(보유 시가 합): ' + ' · '.join(f"{k} {meta[k + '_aum'] / 1e9:.1f}억달러" .replace('억달러', 'B$') for k in ('VYM', 'VIG', 'DGRO', 'HDV')) + ' · SCHD 1,150억달러(슈왑 Total Net Assets 10/16 $114,999,792,743.92) · JEPI 457.2억달러·JEPQ 431.9억달러(JP모건 aum 10/16) · DIVO 80.1억달러(앰플리파이 Net Assets)')
w('\n## 2. 분배율·성장률·총수익·낙폭 (분배=1주당 최근 12개월 합, 성장률=12개월 합을 N년 전 같은 기간 12개월 합과 비교한 연평균, 총수익=분배 재투자 연평균)')
w('티커 | 종가 | 12개월 분배(회) | 분배율% | 분배 성장 1y/3y/5y/10y % | 총수익 1y/5y/10y %(달러) | 원화 1y/5y/10y % | 낙폭 2020~ %(언제) | 2022 낙폭 | 원화 낙폭 2020~')
g = lambda s, k: f"{s[k]:.1f}" if k in s else '-'
for t, s in stats.items():
    w(f"{t} {s['name'] if s['name'] != t else ''} | {s['close']} | {s['ttm']}({s['n_div_12m']}) | {s['yield']:.2f} | {g(s,'divcagr1')}/{g(s,'divcagr3')}/{g(s,'divcagr5')}/{g(s,'divcagr10')} | {g(s,'tr1')}/{g(s,'tr5')}/{g(s,'tr10')} | {g(s,'trkrw1')}/{g(s,'trkrw5')}/{g(s,'trkrw10')} | {s['mdd_since2020']}({s['mdd_since2020_at']}) | {g(s,'mdd_2022')} | {g(s,'mdd_since2020_krw')}")
d_ = stats['DIVO']
w(f"DIVO 튀는 분배 뺀 값: 12개월 {d_['ttm_ex_special']}(뺀 것 {d_['special_12m']}) → 분배율 {d_['yield_ex_special']}% · 분배 성장 3년 {d_['divcagr3_ex_special']}%·5년 {d_['divcagr5_ex_special']}%(5년 전 창에서 뺀 것 {d_['special_5y_ago']})")
w('\n해마다 12개월 분배(10/16에 끝나는 12개월, 1주당): ')
for t in ('SCHD', 'VYM', 'VIG', 'DGRO', 'HDV', 'SPYD', 'JEPI', 'DIVO'):
    y = stats[t]['ttm_by_year']; ks = sorted(y)
    w(f"  {t}: " + ' · '.join(f"{k} {y[k]:.3f}" + (f"({(y[k] / y[str(int(k) - 1)] - 1) * 100:+.1f}%)" if str(int(k) - 1) in y and y[str(int(k) - 1)] else '') for k in ks))
w(f'\n## 3. 1억 넣으면 1년 통장(최근 12개월 분배가 앞으로 같다고 놓은 계산 · 가격·환율 변동 뺌 · 건보는 지역가입자, 다른 금융소득 0 가정, 합산율 {HEALTH * 100:.4f}%)')
for e in eok:
    w(f"  {e['name']}: 분배율 {e['yield_']:.2f}% → 세전 {won(e['gross'])} · 세금 {won(e['tax'])} · 세후 {won(e['net'])}" + (f" · 건보 더 냄 {won(e['health'])}" if e['health'] else '') + f" → 1년 통장 {won(e['after'])} (월 {won(e['monthly'])})" + (' [연 1,000만원 넘음]' if e['over10m'] else '') + (' [연 2,000만원 넘음]' if e['over20m'] else ''))
(HERE / 'calc_out.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
json.dump(dict(sectors=sectors, meta={k: v for k, v in meta.items() if not k.endswith('_aum')}, schwab_official_0630=schwab_official, stats=stats, eok=eok, fx=FXNOW),
          open(HERE / 'calc_out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(out))
