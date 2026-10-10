"""W-1 주간 코너 — 매주 같은 영수증 두 장(코스피 1천만원 · 미국 1만 달러) 숫자를 주차만 넣고 뽑는다 (PD 2026-10-10 22:2x)
사용: py -3.12 weekcore.py 2026-10-16            → w1016/raw/ 에 ECOS 일별·야후 SPY를 받고 w1016/core_out.txt 를 쓴다
      py -3.12 weekcore.py 2026-10-09 --raw w1009/raw --out <파일>   → 받지 않고 그 폴더 원문으로만(1화 재현 검산용)
1화(calc.py)는 거래일(10/6~8)·휴일(10/5·10/9)·기준일(10/2)을 손으로 적었다. 여기서는 전부 원문에서 정한다:
  기준일 = 한 주 전 금요일 이하 마지막 한국 거래일 · 이번 주 거래일 = 기준일 다음 ~ 주 끝(금) 사이 ECOS에 값이 있는 날
  휴일 = 그 사이 평일인데 ECOS에 값이 없는 날 · SPY 마지막 = 주 끝(미국 금요일) 이하 마지막 종가(한국 토 06시 뒤 들어옴)
  미국 1만 달러 원화는 1화와 같게 '이번 주 마지막 한국 거래일 매매기준율'로 바꾼다.
  ※ 야후 금요일 종가는 막 들어온 뒤 바뀐다(1화 10/10 05:02 받은 778.54 → 22시 778.57, F4 523원 차이). 한국 토 10:00 전에 받으면 [K6]에 '잠정'을 찍고, 10시 뒤 다시 받는다.
키 이름·식은 calc.py [D1]~[D4]·[E1]~[E6]·[F1]~[F5]와 같다 → w1props.py·w1meta.py가 그대로 읽는다(날짜 칸만 [K*]로 더함)."""
import json, os, sys, argparse, datetime as dt, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(H, *['..'] * 4)))
ECOS = [('802Y001', '0001000'), ('731Y001', '0000001')]          # 코스피 · 원달러 매매기준율(일)

def fetch(end, raw):
    import apis
    os.makedirs(raw, exist_ok=True)
    s = (end - dt.timedelta(days=21)).strftime('%Y%m%d'); e = end.strftime('%Y%m%d')
    data = {}
    for stat, item in ECOS:
        rows = apis.ecos(stat, 'D', s, e, item, 40)
        assert rows, f'ECOS {stat} 못 받음(키·한도 확인)'
        data[stat] = sorted([t, float(v)] for t, v, _ in rows)
    json.dump({'got': f'{dt.datetime.now():%Y-%m-%d %H:%M} weekcore.py', 'src': '한국은행 ECOS 802Y001/0001000 코스피 · 731Y001/0000001 원달러 매매기준율 (일)', 'data': data},
              open(os.path.join(raw, f'ecos_d_{e}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    u = 'https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=3mo&interval=1d'
    j = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))
    json.dump(j, open(os.path.join(raw, 'yh_SPY.json'), 'w'))

def load(end, raw):
    e = end.strftime('%Y%m%d')
    cands = sorted(f for f in os.listdir(raw) if f.startswith('ecos_d_') and f[7:15] >= e)
    assert cands, f'{raw}에 주 끝({e}) 이후 받은 ECOS 파일 없음'
    EC = json.load(open(os.path.join(raw, cands[0]), encoding='utf-8'))['data']
    j = json.load(open(os.path.join(raw, 'yh_SPY.json')))['chart']['result'][0]; tz = j['meta']['gmtoffset']
    spy = {dt.datetime.fromtimestamp(t + tz, dt.UTC).strftime('%Y%m%d'): v for t, v in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if v}
    return {t: v for t, v in EC['802Y001']}, {t: v for t, v in EC['731Y001']}, spy

def core(end, KO, FX, SPY, got=None, cut=None):
    # cut: 녹음이 주 끝보다 앞이면(2화 10/15 녹음) 그 날 마감까지만 센다 — 기준일은 그대로 '한 주 전 금요일 이하' (youtube-loop 10/11)
    e = (cut or end).strftime('%Y%m%d'); pf = (end - dt.timedelta(days=7)).strftime('%Y%m%d')
    base = max(d for d in KO if d <= pf); assert base in FX, f'기준일 {base} 환율 없음'
    week = sorted(d for d in KO if base < d <= e); assert week, '이번 주 한국 거래일 0'
    assert sorted(d for d in FX if base < d <= e) == week, '코스피·환율 거래일이 다름'
    days = [(dt.date.fromisoformat(f'{base[:4]}-{base[4:6]}-{base[6:]}') + dt.timedelta(days=i)) for i in range(1, ((cut or end) - dt.date.fromisoformat(f'{base[:4]}-{base[4:6]}-{base[6:]}')).days + 1)]
    hol = [d.strftime('%Y%m%d') for d in days if d.weekday() < 5 and d.strftime('%Y%m%d') not in KO]
    last = week[-1]
    ub = max(d for d in SPY if d <= base); ul = max(d for d in SPY if d <= e)
    f0, f1, k0, k1 = FX[base], FX[last], KO[base], KO[last]; kr = (k1 / k0 - 1) * 100
    u0, u1 = SPY[ub], SPY[ul]; v1 = 10000 * u1 / u0 * f1
    iso = lambda d: f'{d[:4]}-{d[4:6]}-{d[6:]}'
    out = []
    p = lambda k, v: out.append(f'{k} = {v}')
    p('[K1] 주 끝(금)', end.isoformat()); p('[K2] 기준일(한 주 전 마지막 한국 거래일)', iso(base))
    p('[K3] 이번 주 한국 거래일', ' '.join(iso(d) for d in week)); p('[K4] 이번 주 휴장 평일(ECOS 값 없음)', ' '.join(iso(d) for d in hol) or '없음')
    p('[K5] SPY 기준일 종가 날짜', iso(ub)); settle = dt.datetime.combine(end + dt.timedelta(days=1), dt.time(10))
    if cut: p('[K6] SPY 자르는 날 종가 들어옴', '예' if ul == e else f'아니오 — 마지막 {iso(ul)}(미국 마감 = 한국 다음 날 05:00)')
    else: p('[K6] SPY 금요일 종가 들어옴', (f'잠정 — {got:%m/%d %H:%M} 받음, 토 10:00 뒤 다시 받기' if got and got < settle else '예') if ul == e else f'아니오 — 마지막 {iso(ul)}(한국 토 10:00 뒤 다시)')
    p(f'[D1] 코스피 {iso(base)}', k0); p(f'[D2] 코스피 {iso(last)}', k1); p('[D3] 주간(%)', round(kr, 2)); p('[D4] 코스피 그대로 1천만원 차이(원)', round(10_000_000 * kr / 100))
    p(f'[E1] 원달러 {iso(base)}', f0); p(f'[E2] 원달러 {iso(last)}', f1); p('[E3] 등락(%)', round((f1 / f0 - 1) * 100, 2))
    p(f'[E4] 1만 달러 원화 {iso(base)}(원)', round(10000 * f0)); p(f'[E5] 1만 달러 원화 {iso(last)}(원)', round(10000 * f1)); p('[E6] 환율만으로 차이(원)', round(10000 * (f1 - f0)))
    p('[F1] SPY 마지막 날', iso(ul)); p(f'[F2] SPY {iso(ub)}→마지막(%)', round((u1 / u0 - 1) * 100, 2))
    p(f'[F3] 1만 달러 SPY 원화 {iso(base)}(원)', round(10000 * f0)); p(f'[F4] 1만 달러 SPY 원화 마지막(원, 환율 {iso(last)} 매매기준율)', round(v1)); p('[F5] 원화 차이(원)', round(v1 - 10000 * f0))
    p('[S4] 코스피 1천만원 차이 만원(반올림)', round(10_000_000 * kr / 100 / 1e4))
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('end'); ap.add_argument('--raw'); ap.add_argument('--out'); ap.add_argument('--cut', help='이 날 마감까지만(YYYY-MM-DD, 주 끝 이하)')
    a = ap.parse_args(); end = dt.date.fromisoformat(a.end); assert end.weekday() == 4, '주 끝은 금요일 날짜로'
    tag = f'w{end:%m%d}'; raw = os.path.join(H, a.raw) if a.raw else os.path.join(H, tag, 'raw')
    if not a.raw: fetch(end, raw)
    got = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(raw, 'yh_SPY.json')))
    cut = dt.date.fromisoformat(a.cut) if a.cut else None
    assert not cut or cut <= end, '--cut은 주 끝 이하'
    out = core(end, *load(end, raw), got=got, cut=cut)
    if cut: out.insert(1, f'[K0] 자르는 날(이 날 마감까지만) = {cut.isoformat()}')
    path = a.out or os.path.join(H, tag, 'core_out.txt')
    open(path, 'w', encoding='utf-8').write(f'# W-1 주간 영수증 core_out — 주 끝 {end} ({dt.datetime.now():%Y-%m-%d %H:%M} weekcore.py, 원문 {os.path.relpath(raw, H)})\n' + '\n'.join(out) + '\n')
    print('\n'.join(out)); print('저장', path)
