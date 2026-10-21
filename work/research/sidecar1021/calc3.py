# KIND 사이드카 공시 52건(raw/kind_sidecar_2026.txt) 세기 — 매수/매도·시각대·한 날 두 번 여부
import collections, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = [l.split() for l in open('raw/kind_sidecar_2026.txt', encoding='utf-8') if l[:1].isdigit()]
print('합', len(rows), collections.Counter(r[3] for r in rows))
print('하루 두 번 이상인 날', [d for d, n in collections.Counter(r[1] for r in rows).items() if n > 1])
t = [r[2] for r in rows]
print('09:06~09:07', sum(1 for x in t if x in ('09:06', '09:07')), ' 09시대', sum(1 for x in t if x.startswith('09')), ' 가장 늦은', max(t), ' 가장 이른', min(t))
print('14시대', [r for r in rows if r[2].startswith('14')])
print('월별', sorted(collections.Counter(r[1][:7] for r in rows).items()))
