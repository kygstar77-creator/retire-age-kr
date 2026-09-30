"""주간 리포트 숫자 모으기 — 사용: py -3.12 weekly_facts.py [주 마지막 날 YYYY-MM-DD]  (기본: 오늘 기준 지난 금요일)
FRED(미국 지수·금리·유가·변동성)와 한국은행 ECOS(코스피·원달러)에서 '그 주 마지막 값 vs 한 주 전 마지막 값'을 계산해
facts_<날짜>.txt 로 쓴다. 자료가 그 주 끝까지 안 올라온 지표는 '마지막 날'을 같이 적어 대본에서 기간을 말하게 한다.
분석 관문 W-1 참모 반론 5(수작업이 많으면 멈춘다) 대응 — 사람 손은 이슈 3개 원문 고르기뿐."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
import apis

FRED = [('S&P 500', 'SP500', '지수'), ('나스닥 종합', 'NASDAQCOM', '지수'), ('다우', 'DJIA', '지수'),
        ('미국 10년 국채 금리', 'DGS10', '%p'), ('미국 2년 국채 금리', 'DGS2', '%p'),
        ('WTI 유가', 'DCOILWTICO', '달러'), ('VIX 변동성', 'VIXCLS', '지수'), ('원달러(FRED)', 'DEXKOUS', '원')]
ECOS = [('코스피', '802Y001', '0001000'), ('원달러 매매기준율', '731Y001', '0000001')]

def week_end(arg):
    if arg: return dt.date.fromisoformat(arg)
    d = dt.date.today()
    while d.weekday() != 4: d -= dt.timedelta(days=1)
    return d

def pick(rows, end):
    """rows: [(YYYY-MM-DD, float)] 오래된 순. 그 주 마지막 값과 한 주 전 마지막 값."""
    cur = [r for r in rows if r[0] <= end.isoformat()]
    prev = [r for r in rows if r[0] <= (end - dt.timedelta(days=7)).isoformat()]
    return (cur[-1] if cur else None), (prev[-1] if prev else None)

def main():
    end = week_end(sys.argv[1] if len(sys.argv) > 1 else None)
    out = [f'# 주간 사실표 — 주 마지막 날 {end} (weekly_facts.py, {dt.datetime.now():%Y-%m-%d %H:%M} 받음). 대본 숫자는 여기서만.']
    for name, sid, unit in FRED:
        try:
            rows = sorted((d, float(v)) for d, v in apis.fred(sid, 30))
        except Exception as e:
            out.append(f'[FRED {sid}] {name}: 못 받음 {e}'); continue
        c, p = pick(rows, end)
        if not c or not p: out.append(f'[FRED {sid}] {name}: 자료 부족'); continue
        lag = '' if c[0] >= (end - dt.timedelta(days=1)).isoformat() else f'  ※ 마지막 날 {c[0]} — 주 끝까지 안 올라옴'
        chg = f'{c[1]-p[1]:+.2f}%p' if unit == '%p' else f'{(c[1]/p[1]-1)*100:+.2f}%'
        out.append(f'[FRED {sid}] {name}: {p[0]} {p[1]:,.2f} → {c[0]} {c[1]:,.2f} ({chg}){lag}')
    for name, stat, item in ECOS:
        try:
            s = (end - dt.timedelta(days=21)).strftime('%Y%m%d'); e = end.strftime('%Y%m%d')
            rows = sorted((f'{t[:4]}-{t[4:6]}-{t[6:]}', float(v)) for t, v, _ in apis.ecos(stat, 'D', s, e, item, 30))
        except Exception as ex:
            out.append(f'[ECOS {stat}] {name}: 못 받음 {ex}'); continue
        c, p = pick(rows, end)
        if not c or not p: out.append(f'[ECOS {stat}] {name}: 자료 부족'); continue
        lag = '' if c[0] >= (end - dt.timedelta(days=1)).isoformat() else f'  ※ 마지막 날 {c[0]} — 주 끝까지 안 올라옴(휴장이면 무시)'
        out.append(f'[ECOS {stat}/{item}] {name}: {p[0]} {p[1]:,.2f} → {c[0]} {c[1]:,.2f} ({(c[1]/p[1]-1)*100:+.2f}%)' + lag)
    out.append('출처: 세인트루이스 연준 FRED(api.stlouisfed.org), 한국은행 경제통계시스템 ECOS. 섹터·ETF·이슈 원문은 따로 붙인다.')
    p = os.path.join(os.path.dirname(__file__), f'facts_{end}.txt')
    open(p, 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out)); print('저장', p)

if __name__ == '__main__': main()
