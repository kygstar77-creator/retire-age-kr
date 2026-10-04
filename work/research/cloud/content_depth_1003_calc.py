# content-depth-1003: R-1 facts.txt 재대조 + 보강 계산(새 숫자) — 저장소 원자료 사본만 읽는다(웹 재접속 없음)
# 원자료: work/research/longform/ep/R-1/raw/{collect,collect2,yahoo,nasdaq_*}_20261003*.json, irs_treaty_table1.pdf(별도 pdftotext),
#         work/research/schd1003/schwab_dist.txt(슈왑 운용사 분배금 표 사본)
# 출력: 표준출력(키=값) — work/research/longform/ep/R-1/facts.additions-1003.txt 에 옮겨 적음. 미래 예측 없음, 과거 값만.
import json, math, os, re, statistics, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R1 = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'R-1')
P = 100_000_000
S, E = '2025-10-02', '2026-10-02'


def load(name):
    with open(os.path.join(R1, 'raw', name), encoding='utf-8') as f:
        return json.load(f)


def schwab_rows():
    rows = []
    with open(os.path.join(ROOT, 'work', 'research', 'schd1003', 'schwab_dist.txt'), encoding='utf-8') as f:
        for line in f:
            m = re.match(r'(\d\d)/(\d\d)/(\d{4})\t(\d\d)/(\d\d)/(\d{4})\t(\d\d)/(\d\d)/(\d{4})\t([\d.]+)\t([\d.]+)\t([\d.]+)\t(\S+)\t([\d.]+)', line)
            if m:
                g = m.groups()
                rows.append({'ex': f'{g[2]}-{g[0]}-{g[1]}', 'pay': f'{g[8]}-{g[6]}-{g[7]}', 'income': float(g[9]),
                             'stcg': float(g[10]), 'ltcg': float(g[11]), 'roc': g[12], 'total': float(g[13])})
    return rows


def fx_on(fx, day):
    """그날 또는 그 전 가장 가까운 영업일 매매기준율(ECOS 731Y001 사본)."""
    k = day.replace('-', '')
    keys = sorted(x for x in fx if x <= k)
    return float(fx[keys[-1]]), keys[-1]


def verify():
    out = {}
    c1, c2, y = load('collect_20261003.json'), load('collect2_20261003.json'), load('yahoo_20261003.json')
    base = dict(c1['기준금리_M'])
    out['기준금리'] = {m: base.get(m) for m in ['202005', '202301', '202505', '202607', '202608', '202609']}
    dep = {k: float(v) for k, v in c1['정기예금1년_신규_M']}
    since20 = {k: v for k, v in dep.items() if k >= '202001'}
    out['예금1년'] = {'202508': dep['202508'], '202608': dep['202608'], '202510': dep['202510'],
                     'max': max(since20.items(), key=lambda kv: kv[1]), 'min': min(since20.items(), key=lambda kv: kv[1]),
                     'avg': {yr: round(statistics.mean(v for k, v in dep.items() if k.startswith(yr)), 2) for yr in ['2020', '2021', '2022', '2023', '2024', '2025', '2026']}}
    for key in ['finlife_예금12개월_은행', 'finlife_예금12개월_저축은행']:
        rows = c1[key]
        rates = [r['금리'] for r in rows]
        out[key] = {'회사': len({r['은행'] for r in rows}), '상품행': len(rows), 'min': min(rates), 'median': statistics.median(rates), 'max': max(rates)}
    cpi = dict(c1['CPI_M'])
    out['CPI'] = (cpi['202508'], cpi['202608'], round((float(cpi['202608']) / float(cpi['202508']) - 1) * 100, 2))
    fx = dict(c2['USDKRW_D'])
    out['FX'] = (fx['20251002'], fx['20261002'], round((float(fx['20261002']) / float(fx['20251002']) - 1) * 100, 2))
    nas = {}
    for t in ['SPY', 'SCHD', 'GLD']:
        rows = load(f'nasdaq_{t}_20261003b.json')['data']['tradesTable']['rows']
        nas[t] = {r['date']: float(r['close']) for r in rows}
    out['끝값_나스닥'] = {t: nas[t].get('10/02/2026') for t in nas}
    out['시작값_야후'] = {t: round(y[t]['px'][S], 2) for t in ['SPY', 'SCHD', 'GLD']}
    spy_full = {r['date']: float(r['close']) for r in load('nasdaq_SPY_20261003b.json')['data']['tradesTable']['rows']}
    out['SPY_시작_나스닥'] = spy_full.get('10/02/2025')
    spy_div_fmp = [(r['date'], r['paymentDate'], r['dividend']) for r in c2['SPY_div'] if S < r['date'] <= E]
    out['SPY_분배_FMP'] = spy_div_fmp
    out['SPY_분배_FMP_합'] = round(sum(d for _, _, d in spy_div_fmp), 5)
    out['SPY_분배_야후_합'] = round(sum(v for k, v in y['SPY']['div'].items() if S < k <= E), 4)
    sw = [r for r in schwab_rows() if S < r['ex'] <= E]
    out['SCHD_분배_슈왑'] = [(r['ex'], r['pay'], r['total'], r['income'], r['stcg'], r['ltcg'], r['roc']) for r in sw]
    out['SCHD_분배_슈왑_합'] = round(sum(r['total'] for r in sw), 4)
    out['SCHD_분배_야후_합'] = round(sum(v for k, v in y['SCHD']['div'].items() if S < k <= E), 4)
    out['GLD_분배_야후'] = {k: v for k, v in y['GLD'].get('div', {}).items()} if isinstance(y['GLD'].get('div'), dict) else 'GLD div 키 없음'
    return out


def additions():
    out = {}
    c2, y = load('collect2_20261003.json'), load('yahoo_20261003.json')
    fx = dict(c2['USDKRW_D'])
    f0, f1 = float(fx['20251002']), float(fx['20261002'])
    END = {'SPY': 769.64, 'SCHD': 32.72, 'GLD': 380.14}  # facts [11] 확정 끝값
    sh = {t: P / f0 / y[t]['px'][S] for t in END}
    out['주수'] = {t: round(v, 4) for t, v in sh.items()}

    # (1) SPY 4번째 분배금: 기준일 9/18, 지급일 10/30 — 10/2에 판 뒤에 들어온다
    spy4 = [r for r in c2['SPY_div'] if r['date'] == '2026-09-18'][0]
    out['SPY_4번째'] = {'ex': spy4['date'], 'pay': spy4['paymentDate'], 'usd_per_sh': spy4['dividend'],
                       'usd': round(sh['SPY'] * spy4['dividend'], 2), 'krw_at_1002fx_세전': round(sh['SPY'] * spy4['dividend'] * f1)}
    # 산 날(10/2/2025) 직전 분배(기준일 2025-09-19, 지급 10/31)는 못 받는다
    prev = [r for r in c2['SPY_div'] if r['date'] == '2025-09-19'][0]
    out['SPY_직전분배_못받음'] = {'ex': prev['date'], 'pay': prev['paymentDate'], 'usd_per_sh': prev['dividend']}

    # (2) SCHD 분배금: 분기별 세후 원화(지급일 환율) vs facts 방식(끝날 환율 일괄)
    sw = [r for r in schwab_rows() if S < r['ex'] <= E]
    q = []
    for r in sorted(sw, key=lambda r: r['ex']):
        rate, used = fx_on(fx, r['pay'])
        gross = sh['SCHD'] * r['total'] * rate
        net = gross - math.floor(gross * 0.15)
        q.append((r['pay'], r['total'], used, rate, round(gross), round(net)))
    out['SCHD_분기'] = q
    out['SCHD_지급일환율_세후합'] = sum(x[5] for x in q)
    facts_net = round(sh['SCHD'] * sum(r['total'] for r in sw) * f1) - math.floor(round(sh['SCHD'] * sum(r['total'] for r in sw) * f1) * 0.15)
    out['SCHD_끝날환율_세후합(facts방식)'] = facts_net
    out['SCHD_분기_세후_최소최대'] = (min(x[5] for x in q), max(x[5] for x in q))
    # 직전 1년(같은 4회 묶음) 대비 분배금 변화 — 2024-12 ~ 2025-09 지급분
    allrows = sorted(schwab_rows(), key=lambda r: r['ex'])
    prev4 = [r for r in allrows if '2024-10-02' < r['ex'] <= '2025-10-02']
    out['SCHD_직전4회'] = [(r['ex'], r['total']) for r in prev4]
    out['SCHD_분배_변화%'] = round((sum(r['total'] for r in sw) / sum(r['total'] for r in prev4) - 1) * 100, 2)
    out['SCHD_자본이득분배_합'] = round(sum(r['stcg'] + r['ltcg'] for r in sw), 4)

    # (3) 1년 중 가장 낮았던 날(원화 평가액, 분배금 제외·세전) — 미국 종가 × 그날(또는 직전 영업일) 매매기준율
    for t in END:
        px = y[t]['px']
        days = sorted(d for d in px if S <= d <= E)
        vals = []
        for d in days:
            p = END[t] if d == E else px[d]
            rate, _ = fx_on(fx, d)
            vals.append((d, sh[t] * p * rate))
        low = min(vals, key=lambda v: v[1])
        peak, mdd, mdd_pair = -1, 0, None
        for d, v in vals:
            if v > peak:
                peak, pk_d = v, d
            dd = v / peak - 1
            if dd < mdd:
                mdd, mdd_pair = dd, (pk_d, d)
        out[f'{t}_최저일'] = (low[0], round(low[1]), round((low[1] / P - 1) * 100, 2))
        out[f'{t}_최대낙폭(원화)'] = (round(mdd * 100, 2), mdd_pair)
    fxs = [(k, float(v)) for k, v in fx.items() if '20251002' <= k <= '20261002']
    out['FX_1년_최고최저'] = (max(fxs, key=lambda kv: kv[1]), min(fxs, key=lambda kv: kv[1]))

    # (4) 시작일을 바꾸면 세 ETF 순위가 그대로인가 — 달러 기준 세전 총수익(가격+기준일이 기간 안인 분배금)
    #     세 ETF 모두 같은 달러 → 같은 환율로 바꾸므로 '셋 사이' 순위는 환율과 무관(예금과의 비교는 환율 자료가 1년치뿐이라 못 함)
    starts = sorted(d for d in y['SPY']['px'] if '2024-10-02' <= d <= '2025-10-02')
    allpx = {t: y[t]['px'] for t in END}
    divs = {t: (y[t].get('div') if isinstance(y[t].get('div'), dict) else {}) for t in END}
    from datetime import date, timedelta
    orders = {}
    n = 0
    for s in starts:
        sd = date.fromisoformat(s)
        ed = sd.replace(year=sd.year + 1)
        e = max(d for d in allpx['SPY'] if d <= ed.isoformat())
        if any(s not in allpx[t] or e not in allpx[t] for t in END):
            continue
        tr = {}
        for t in END:
            dv = sum(v for k, v in divs[t].items() if s < k <= e)
            tr[t] = (allpx[t][e] + dv) / allpx[t][s] - 1
        od = '>'.join(sorted(tr, key=lambda k: -tr[k]))
        orders[od] = orders.get(od, 0) + 1
        n += 1
    out['시작일별_순위'] = {'시작일수': n, '범위': (starts[0], starts[-1]), '순위분포': dict(sorted(orders.items(), key=lambda kv: -kv[1]))}

    # (5) 시나리오 계산 — 숫자는 facts [2][계산]·D-1 facts [1][3][6][10] 식에서
    def nhis_monthly(fin_income):  # 지역 1인·재산 0·다른 소득 0 (D-1 facts [계산]과 같은 버림 규칙)
        if fin_income <= 10_000_000:
            hi = 20_160
        else:
            hi = math.floor(fin_income / 12 * 0.0719 / 10) * 10
        lt = math.floor(hi * 0.9448 / 7.19 / 10) * 10
        return hi + lt
    out['건보_검산_1001만'] = nhis_monthly(10_010_000)  # D-1 facts 67,850
    out['건보_검산_1000만'] = nhis_monthly(10_000_000)  # D-1 facts 22,800
    i3 = round(300_000_000 * 0.0339)
    out['3억_3.39%_이자'] = i3
    out['3억_건보_월'] = nhis_monthly(i3)
    out['2억_3.39%_이자'] = round(200_000_000 * 0.0339)
    out['2억_건보_월'] = nhis_monthly(round(200_000_000 * 0.0339))
    out['3억_건보_연차이'] = (nhis_monthly(i3) - nhis_monthly(round(200_000_000 * 0.0339))) * 12
    tax3 = math.floor(i3 * 0.14 / 10) * 10
    tax3 += math.floor(tax3 * 0.1 / 10) * 10
    out['3억_이자세'] = tax3
    out['3억_세후이자'] = i3 - tax3
    return out


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for title, fn in [('VERIFY', verify), ('ADD', additions)]:
        print(f'## {title}')
        for k, v in fn().items():
            print(f'{k} = {v}')
