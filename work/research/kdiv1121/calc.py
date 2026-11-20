# kdiv1121 직접 계산 — 같은 갈래 5개, 1억원을 지금(11/20 받은 야후 최근 종가) 넣으면 최근 달 분배금으로 매달 얼마(세전·15.4% 뗀 것), 1년 새 월 분배 변화
import json, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
END = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 11, 19)
OUT = {'g': {}, 'a0': {}, 'a1': {}, 'm': {}, 'p1y': {}, 'ttm': {}}
N = {'161510': 'PLUS 고배당주', '279530': 'KODEX 고배당주', '104530': 'KIWOOM 코리아고배당', '466940': 'TIGER 은행고배당플러스TOP10', '0105E0': 'SOL 코리아고배당'}
for c, nm in N.items():
    r = json.load(open(f'raw/y_{c}.KS.json'))['chart']['result'][0]
    ev = sorted((dt.datetime.fromtimestamp(int(k), dt.UTC).date(), v['amount']) for k, v in r.get('events', {}).get('dividends', {}).items())
    px = [(dt.datetime.fromtimestamp(t, dt.UTC).date(), p) for t, p in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if p]
    px = [x for x in px if x[0] <= END]  # 끝 날 종가(장 마감 뒤 받은 값만)
    d1, p1 = px[-1]; last = ev[-1]
    yr = [a for d, a in ev][-12:]
    a12 = next((a for d, a in ev if last[0] - dt.timedelta(days=380) <= d <= last[0] - dt.timedelta(days=350)), None) if c != '0105E0' else None  # SOL은 2025-11 첫 분배라 1년 전 같은 달 없음
    p0 = next((p for d, p in px if d >= d1 - dt.timedelta(days=365)), None)
    sh = int(1e8 // p1); g = sh * last[1]
    OUT['g'][c] = (last[1] / a12 - 1) * 100 if a12 else None; OUT['a0'][c] = a12; OUT['a1'][c] = last[1]; OUT['m'][c] = g; OUT['p1y'][c] = (p1 / p0 - 1) * 100 if p0 else None; OUT['ttm'][c] = sum(yr) / p1 * 100; OUT['day'] = str(d1)
    print(f'{nm}({c}) 종가 {d1} {p1:,.0f} · 최근 분배 {last[0]} {last[1]:.0f}원 · 1년 전 {a12} → {"" if not a12 else f"{last[1]/a12-1:+.0%}"} · 최근12번 합 {sum(yr):.0f}원 ({sum(yr)/p1:.2%}) · 1억 {sh:,}주 월 세전 {g:,.0f} 세후 {g*0.846:,.0f} · 주가 1년 {"" if not p0 else f"{p1/p0-1:+.1%}"}')

json.dump(OUT, open('calc.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
