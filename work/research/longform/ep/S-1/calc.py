# -*- coding: utf-8 -*-
"""S-1 삼성전자 잠정실적 발표 날 주가 — 44번(2016-01~2026-10) 계산.

원문: DART 잠정실적 공시 원문 raw/docs/<rcept_no>.xml (fetchdocs.py, 분기 첫 공시만, 정정 제외)
주가: 다음 금융 일별 종가 raw/daum_005930_daily.json = KRX 정규장 종가
  - 2018-05-04 전 값은 50:1 액면분할 전 가격이라 /50
  - 대조: 2025-03-04(넥스트레이드 시작) 전 2,269일 네이버 siseJson과 0곳 다름(네이버 이후 값은 20시 통합 종가라 대조에서 뺌)
         야후는 25곳(분할 뒤 묵은 값)·4곳(호가 단위에 안 맞는 값) 틀림 → 쓰지 않음
  - KRX 정보데이터시스템 원본은 로그인 필요라 직접 대조 확인 안 함
발표 시각: 장 시작 전 공시로 보고 '발표 날 = 전날 종가 → 그날 종가'. 공시 시각 원문 대조 확인 안 함.
"""
import json, os, re, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from fetchdocs import prelims

def text(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8', 'cp949'):
        try: t = b.decode(enc); break
        except UnicodeDecodeError: continue
    t = re.sub(r'<[^>]+>', ' ', t); return re.sub(r'\s+', ' ', t)

def parse(t):
    unit = re.search(r'단위\s*:\s*([^\s,]+)', t).group(1)
    m = re.search(r'영업이익\s+당해실적\s+(.*?)\s+누계실적', t).group(1).split()
    num = lambda s: None if s in ('-', '') else float(s.replace(',', '').rstrip('%'))
    # 2025-10 이후 양식은 '흑자적자전환여부' 칸이 끼어 6칸, 그 전은 5칸. 금액은 전부 조원(2016~17 양식은 단위 칸이 '백만원'이지만 본문 4항에 '조원 단위'라 적음)
    if '흑자적자전환여부' in t: cur, prev, qoq, _, yoy_base, yoy = (m + ['-'] * 6)[:6]
    else: cur, prev, qoq, yoy_base, yoy = (m + ['-'] * 5)[:5]
    v = num(cur); vy = num(yoy_base)
    per = re.search(r'당기실적\s+(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})', t)
    return dict(unit=unit, op=v, op_yoy_base=vy, yoy_pct=num(yoy), period=per.group(2) if per else None)

px = {}
for r in json.load(open(os.path.join(D, 'raw/daum_005930_daily.json'), encoding='utf-8')):
    if r['accTradeVolume'] == 0: continue  # 2018-04-30·05-02·05-03 액면분할 거래정지(값만 있는 행) 뺌 — 레드팀·Claude 심사 10/14
    if r['date'] >= '2026-10-14': continue  # 10/14 행은 받은 시각(20시대)에 아직 확정 전(EVEN·거래량 중간값) — 쓰지 않음
    px[r['date'][:10]] = r['tradePrice'] / (50 if r['date'] < '2018-05-04' else 1)
days = sorted(px)

def main():
  rows = []
  for x in prelims():
      d = f"{x['rcept_dt'][:4]}-{x['rcept_dt'][4:6]}-{x['rcept_dt'][6:]}"
      p = parse(text(os.path.join(D, 'raw/docs', x['rcept_no'] + '.xml')))
      i = days.index(d)
      c0, c1 = px[days[i - 1]], px[d]
      c20 = px[days[i + 20]] if i + 20 < len(days) else None
      rows.append(dict(date=d, rcept_no=x['rcept_no'], **p, prev_close=c0, close=c1,
                       day_pct=round((c1 / c0 - 1) * 100, 2),
                       d20_date=days[i + 20] if c20 else None, d20_pct=round((c20 / c0 - 1) * 100, 2) if c20 else None))

  json.dump(rows, open(os.path.join(D, 'calc_out.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
  n = len(rows); up = [r for r in rows if r['day_pct'] > 0]; dn = [r for r in rows if r['day_pct'] < 0]
  r20 = [r for r in rows if r['d20_pct'] is not None]
  print(f'발표 {n}번 ({rows[0]["date"]} ~ {rows[-1]["date"]})')
  print(f'발표 날 오름 {len(up)} · 내림 {len(dn)} · 그대로 {n-len(up)-len(dn)} · 중앙 {statistics.median(r["day_pct"] for r in rows):+.2f}% · 평균 {statistics.mean(r["day_pct"] for r in rows):+.2f}%')
  print(f'20거래일 뒤(전날 종가 대비, {len(r20)}번) 오름 {sum(r["d20_pct"]>0 for r in r20)} · 중앙 {statistics.median(r["d20_pct"] for r in r20):+.2f}%')
  yu = [r for r in rows if r['op_yoy_base'] and r['op'] > r['op_yoy_base']]
  print(f'영업이익이 1년 전보다 늘어난 발표 {len(yu)}번 중 발표 날 내림 {sum(r["day_pct"]<0 for r in yu)} · 오름 {sum(r["day_pct"]>0 for r in yu)}')
  yd = [r for r in rows if r['op_yoy_base'] and r['op'] < r['op_yoy_base']]
  print(f'1년 전보다 줄어든 발표 {len(yd)}번 중 발표 날 내림 {sum(r["day_pct"]<0 for r in yd)} · 오름 {sum(r["day_pct"]>0 for r in yd)}')
  big = sorted(rows, key=lambda r: abs(r['day_pct']), reverse=True)[:5]
  print('발표 날 크게 움직인 5번:', [(r['date'], r['day_pct'], r['op']) for r in big])
  mx = max(rows, key=lambda r: r['op']); print('영업이익 최대 분기:', mx['date'], mx['op'], '조원 · 그날', mx['day_pct'], '%')
  # '사상 최대' 판정: 2011~2015 잠정실적 공시(분기 첫 공시 20건, raw/dart_samsung_prelim_2010_2015.json)까지 넣어 그때까지 가장 큰 분기를 넘었나
  old = json.load(open(os.path.join(D, 'raw/dart_samsung_prelim_2010_2015.json'), encoding='utf-8'))
  old = [x for x in old if not x['report_nm'].strip().startswith('[') and int(x['rcept_dt'][6:]) <= 20 and int(x['rcept_dt'][4:6]) in (1, 4, 7, 10)]
  base = [(x['rcept_dt'], parse(text(os.path.join(D, 'raw/docs', x['rcept_no'] + '.xml')))['op']) for x in old]
  best_d, best = max(base, key=lambda b: b[1])
  print(f'2011~2015 잠정 공시 {len(base)}건 중 최대 {best}조원({best_d})')
  rec = []
  for r in rows:
      if r['op'] > best: rec.append(r); best = r['op']
  print(f'사상 최대(2011년 이후 잠정 공시 기준) 분기 발표 {len(rec)}번: 발표 날 오름 {sum(r["day_pct"]>0 for r in rec)} · 그대로 {sum(r["day_pct"]==0 for r in rec)} · 내림 {sum(r["day_pct"]<0 for r in rec)}')
  r20 = [r for r in rec if r['d20_pct'] is not None]
  print(f'  그중 20거래일 뒤 {len(r20)}번: 오름 {sum(r["d20_pct"]>0 for r in r20)} · 내림 {sum(r["d20_pct"]<0 for r in r20)}')
  for r in rec: print('  ', r['date'], r['op'], '조원 · 그날', r['day_pct'], '% · 20일', r['d20_pct'])
  dn = [r for r in rows if r['day_pct'] < 0 and r['d20_pct'] is not None]; upd = [r for r in rows if r['day_pct'] > 0 and r['d20_pct'] is not None]
  print(f'발표 날 내린 {len(dn)}번 중 20거래일 뒤 전날보다 위 {sum(r["d20_pct"]>0 for r in dn)} · 발표 날 오른 {len(upd)}번 중 {sum(r["d20_pct"]>0 for r in upd)}')
  # 평소 기준선(심사 10/14: '발표 날 17/44'·'한 달 뒤 25/43'은 평소와 견줘야 뜻이 있다)
  first = days.index(rows[0]['date']) - 1
  d1 = [px[days[i]] / px[days[i - 1]] - 1 for i in range(first + 1, len(days))]
  d20 = [px[days[i + 20]] / px[days[i]] - 1 for i in range(first, len(days) - 20)]
  print(f'평소 하루({days[first+1]}~{days[-1]}, {len(d1)}거래일): 오른 날 {sum(x>0 for x in d1)} = {sum(x>0 for x in d1)/len(d1)*100:.1f}% · 내린 날 {sum(x<0 for x in d1)/len(d1)*100:.1f}% · 평균 {statistics.mean(d1)*100:+.2f}%')
  print(f'평소 아무 날 → 20거래일 뒤({len(d20)}구간): 오른 비율 {sum(x>0 for x in d20)/len(d20)*100:.1f}% · 중앙 {statistics.median(d20)*100:+.2f}%')
  a20 = [r for r in rows if r['d20_pct'] is not None]
  print(f'발표 날 오른 비율 {len(up)/n*100:.1f}% · 발표 뒤 20거래일 오른 비율 {sum(r["d20_pct"]>0 for r in a20)/len(a20)*100:.1f}% ({sum(r["d20_pct"]>0 for r in a20)}/{len(a20)})')
  from math import comb
  pu = sum(x>0 for x in d1)/len(d1)
  pv = sum(comb(n, k) * pu**k * (1-pu)**(n-k) for k in range(0, len(up)+1))
  print(f'평소 오를 확률 {pu:.3f}로 44번 던졌을 때 오름 {len(up)}번 이하가 나올 확률 {pv*100:.1f}% (이항, 한쪽)')
  # 2025-03-04 뒤 다음 값 대조(야후, 정규장)
  y = {f'{a[:4]}-{a[4:6]}-{a[6:]}': b for a, b in json.load(open(os.path.join(D, 'raw/yahoo_005930_daily.json'), encoding='utf-8'))}
  post = [k for k in days if k >= '2025-03-04' and k in y]
  diff = [(k, px[k], y[k]) for k in post if abs(px[k] - y[k]) > .5]
  print(f'2025-03-04 뒤 다음↔야후 {len(post)}일 중 다름 {len(diff)}: {diff}')
  for k in ('2026-04-07', '2026-05-07', '2026-07-06', '2026-07-07', '2026-08-05', '2026-10-07', '2026-10-08', '2026-10-13', '2026-04-06'):
      print('  대조', k, px.get(k), y.get(k))
  last = rows[-1]
  print(f"2026-10-08: 영업이익 {last['op']}조원(1년 전 {last['op_yoy_base']}조원, {last['yoy_pct']}%) · 전날 {last['prev_close']:,.0f} → {last['close']:,.0f}원 {last['day_pct']:+.2f}% · 100주 {(last['close']-last['prev_close'])*100:+,.0f}원")
  print('표:'); [print(r['date'], r['period'], r['op'], r['op_yoy_base'], r['day_pct'], r['d20_pct']) for r in rows]


if __name__ == '__main__':
    main()
