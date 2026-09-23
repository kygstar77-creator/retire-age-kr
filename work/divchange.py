# -*- coding: utf-8 -*-
"""이번 주에 '배당을 발표한' 종목을 모아 직전 배당과 대비해 인상·삭감·동결을 가른다.
카페 C8 / 블로그 B12 시리즈 재료. 편성표는 heatmap.py --list를 시켰지만 그건 등락 히트맵이라
배당 증감을 낼 수 없었다(2026-09-24 03시 회차에서 확인, 그래서 C8이 한 편도 못 나갔다).

  py -3.12 work/divchange.py [일수=7] [--min 0.01] [--json 경로]

자료: Nasdaq 배당 캘린더(api.nasdaq.com/api/calendar/dividends, 무키)의 announcement_Date로
이번 주 '발표'를 고르고, 같은 API의 종목별 배당 이력으로 직전 회차 금액과 비교한다.
주기가 바뀐 종목(분기→월 등)은 증감률이 뜻을 잃으므로 '주기변경'으로 따로 뺀다.
"""
import json, sys, os, time, datetime, urllib.request, collections
from concurrent.futures import ThreadPoolExecutor

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': 'application/json'}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research')

def get(u, tries=3):
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25))
        except Exception:
            if k == tries - 1: return None
            time.sleep(1.2)

def d2s(s):
    for f in ('%m/%d/%Y', '%Y-%m-%d'):
        try: return datetime.datetime.strptime(s, f).date()
        except Exception: pass

def calendar(days):
    """최근 days일의 배당 캘린더를 모아 announcement_Date가 그 안인 것만 남긴다."""
    today = datetime.date.today()
    rows, seen = [], set()
    # 발표 뒤 배당락이 며칠 늦으므로 앞뒤로 넉넉히 훑는다
    for k in range(-days, days + 1):
        d = today + datetime.timedelta(days=k)
        j = get(f'https://api.nasdaq.com/api/calendar/dividends?date={d:%Y-%m-%d}')
        for r in ((j or {}).get('data') or {}).get('calendar', {}).get('rows') or []:
            a = d2s(r.get('announcement_Date') or '')
            if not a or (today - a).days > days or a > today: continue
            key = (r['symbol'], r.get('dividend_Ex_Date'))
            if key in seen: continue
            seen.add(key); r['_ann'] = a; rows.append(r)
    return rows

def history(sym):
    for cls in ('stocks', 'etf'):
        j = get(f'https://api.nasdaq.com/api/quote/{sym}/dividends?assetclass={cls}')
        d = (j or {}).get('data') or {}
        rows = (d.get('dividends') or {}).get('rows') or []
        if rows: return rows, d, cls
    return [], {}, None

def prev_amount(rows, ex_date, rate):
    """직전 회차 금액과 주기(일 간격)를 돌려준다. 같은 배당락 건은 건너뛴다."""
    hist = []
    for r in rows:
        ed = d2s(r.get('exOrEffDate') or '')
        try: amt = float(str(r.get('amount') or '').replace('$', '').replace(',', ''))
        except Exception: continue
        if ed and amt > 0: hist.append((ed, amt))
    hist.sort(key=lambda x: -x[0].toordinal())
    cur = None; prev = None
    for ed, amt in hist:
        if ex_date and ed == ex_date and cur is None: cur = (ed, amt); continue
        if cur is not None or (ex_date and ed < ex_date):
            prev = (ed, amt); break
    if prev is None and len(hist) >= 2: prev = hist[1]
    gap = None
    if prev and cur: gap = (cur[0] - prev[0]).days
    elif prev and ex_date: gap = (ex_date - prev[0]).days
    return (prev[1] if prev else None), gap, len(hist)

def main():
    args = [a for a in sys.argv[1:]]
    days = 7; floor = 0.0; jout = None; only_stocks = False
    i = 0
    while i < len(args):
        if args[i] == '--stocks': only_stocks = True; i += 1
        elif args[i] == '--min': floor = float(args[i + 1]); i += 2
        elif args[i] == '--json': jout = args[i + 1]; i += 2
        else: days = int(args[i]); i += 1

    rows = calendar(days)
    print(f'이번 {days}일 발표 배당 {len(rows)}건 (Nasdaq 배당 캘린더, announcement_Date 기준)')
    if not rows: return

    def work(r):
        h, meta, cls = history(r['symbol'])
        if not h: return None
        r['_cls'] = cls
        if only_stocks and cls != 'stocks': return None
        prev, gap, n = prev_amount(h, d2s(r.get('dividend_Ex_Date') or ''), r.get('dividend_Rate'))
        try: cur = float(r.get('dividend_Rate') or 0)
        except Exception: return None
        if not prev or not cur or cur < floor: return None
        r['_prev'] = prev; r['_cur'] = cur; r['_gap'] = gap; r['_n'] = n
        r['_pct'] = (cur - prev) / prev * 100
        r['_yield'] = meta.get('yield'); r['_ann_div'] = meta.get('annualizedDividend')
        r['_payout'] = meta.get('payoutRatio')
        return r

    with ThreadPoolExecutor(max_workers=8) as ex:
        got = [x for x in ex.map(work, rows) if x]

    # 주기가 바뀐 종목은 증감률이 뜻을 잃는다(분기 0.22 → 월 0.07은 삭감이 아니다)
    def 주기바뀜(r):
        g = r.get('_gap')
        return g is not None and not (20 <= g <= 40 or 75 <= g <= 105 or 160 <= g <= 200 or 330 <= g <= 400)

    normal = [r for r in got if not 주기바뀜(r)]
    odd = [r for r in got if 주기바뀜(r)]
    up = sorted([r for r in normal if r['_pct'] > 0.5], key=lambda r: -r['_pct'])
    dn = sorted([r for r in normal if r['_pct'] < -0.5], key=lambda r: r['_pct'])
    flat = [r for r in normal if -0.5 <= r['_pct'] <= 0.5]

    print(f'비교 성공 {len(got)}건 · 인상 {len(up)} · 삭감 {len(dn)} · 동결 {len(flat)} · 주기변경 {len(odd)}')
    def show(t, items, k=12):
        print(f'\n[{t}]')
        for r in items[:k]:
            print(f"  {r['symbol']:6s} {r['_prev']:.4f} → {r['_cur']:.4f} ({r['_pct']:+.1f}%) "
                  f"배당락 {r.get('dividend_Ex_Date')} 발표 {r['_ann']} 지급 {r.get('payment_Date')} "
                  f"연환산 {r.get('indicated_Annual_Dividend')} 수익률 {r.get('_yield')} "
                  f"성향 {r.get('_payout')} [{r.get('_cls')}] | {r['companyName'][:42]}")
    show('인상', up); show('삭감', dn); show('주기변경(증감률 무의미)', odd, 8)

    if jout:
        os.makedirs(os.path.dirname(jout) or '.', exist_ok=True)
        with open(jout, 'w', encoding='utf-8') as f:
            json.dump({'asof': str(datetime.date.today()), 'days': days,
                       'up': up, 'down': dn, 'flat': flat, 'odd': odd},
                      f, ensure_ascii=False, default=str, indent=1)
        print('\n저장', jout)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
