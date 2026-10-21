# K-1 calc4 (2026-10-21 youtube-loop, 심사 반영) — 상관(F9)을 말로 풀기: 163달 중 '같은 쪽으로 움직인 달' 수.
# calc.py의 같은 원자료·같은 달 목록을 그대로 쓴다(출력은 버리고 변수만). 실행: py -3.12 calc4.py > calc4_out.txt
import io, contextlib, os
HERE = os.path.dirname(os.path.abspath(__file__)); g = {'__file__': os.path.join(HERE, 'calc.py'), '__name__': 'calc'}
class _Q(io.StringIO):
    def reconfigure(self, **k): pass
with contextlib.redirect_stdout(_Q()):
    exec(open(os.path.join(HERE, 'calc.py'), encoding='utf-8').read(), g)
import sys; sys.stdout.reconfigure(encoding="utf-8")
months, diffs = g['months'], g['diffs']
print('# K-1 calc4 — 월 변화 방향 맞추기 (%s~%s, %d달)' % (months[1], months[-1], len(months) - 1))
for name, s in (('예금1년', g['dep1']), ('주담대 고정', g['mfix']), ('주담대 변동', g['mvar'])):
    y = diffs(s, months)
    for xn, x in (('미10년', g['us_m']), ('한10년', g['kr10']), ('한3년', g['kr3'])):
        dx = diffs(x, months)
        same = sum(1 for a, b in zip(dx, y) if a * b > 0); opp = sum(1 for a, b in zip(dx, y) if a * b < 0)
        print(f' {name} vs {xn}: 같은 쪽 {same}달 · 반대 {opp}달 · 한쪽이 그대로 {len(y)-same-opp}달 (전체 {len(y)})')
