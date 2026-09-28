# -*- coding: utf-8 -*-
"""앞으로 N일 안에 시행되는 법령 목록 (B7 슬롯용).

실행: py -3.12 work/lawsoon.py [일수=30] [--grep 세|연금|보험]

만든 이유(2026-09-28 23시 회차): lawSearch.do target=law + efYd=A~B 가 0건을 돌려줬다.
target=law 는 '현행 법령'만 주므로 아직 시행 안 된 법은 안 나온다. 시행일 법령은 target=eflaw 로 받아야 한다
(같은 조건으로 130건). efYd에 '-'를 쓰면 필터가 무시돼 5,620건이 나온다 — 그것도 틀린 값이다.
"""
import sys, datetime, urllib.request, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
days = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 30
pat = sys.argv[sys.argv.index('--grep') + 1].split('|') if '--grep' in sys.argv else None
a = datetime.date.today() + datetime.timedelta(days=1); b = a + datetime.timedelta(days=days - 1)
rows = set()
for p in range(1, 20):
    u = f'http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML&display=100&efYd={a:%Y%m%d}~{b:%Y%m%d}&page={p}'
    r = ET.fromstring(urllib.request.urlopen(u, timeout=30).read())
    ls = r.findall('law')
    for l in ls:
        rows.add((l.findtext('시행일자'), l.findtext('법령일련번호'), l.findtext('법령명한글'), l.findtext('제개정구분명'), l.findtext('공포일자')))
    if len(ls) < 100: break
print(f'시행일 {a}~{b}: {len(rows)}건 (본문은 lawService.do?target=eflaw&MST=<일련번호>&efYd=<시행일자>)')
for x in sorted(rows):
    if pat and not any(k in x[2] for k in pat): continue
    print(*x)
