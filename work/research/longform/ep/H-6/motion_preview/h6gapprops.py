# H-6 2장 강남구 21곳 1년 변화 가로 막대(GapBars) props — calc3_out.txt에서 직접 읽고 assert (2026-11-21 motion)
# 말 줄은 대본 v1.3(youtube-loop 12:54, editor 재서명 전) 92~100행 그대로. frames는 녹음 전 추정(글자 수) — PD가 voice 길이로 바꾼다. 숫자는 이 파일이 calc에서 만든다.
import re, json, os, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H)
txt = open(os.path.join(E, 'calc3_out.txt'), encoding='utf-8').read()
rows = [{'name': f'{a} {b}'.strip(), 'n0': int(n0), 'n1': int(n1), 'v': float(v)} for a, b, n0, n1, v in re.findall(r'^(\S+동) (.+?) · (\d+)건 [\d.]+억 → (\d+)건 [\d.]+억 · ([+-][\d.]+)%', txt, re.M)]
assert len(rows) == 23, len(rows)   # 11/25 다시 받음(calc3_1125)
assert [r['v'] for r in rows] == sorted(r['v'] for r in rows)
dn = sum(r['v'] < 0 for r in rows); up = sum(r['v'] > 0 for r in rows); assert (dn, up) == (16, 7)
md = statistics.median(r['v'] for r in rows); assert md == -5.9, md
assert '단지 23곳 · 변화 가운데 값 -5.9% · 내린 곳 16 · 오른 곳 7' in txt
hi = [i for i, r in enumerate(rows) if r['name'].endswith(' 은마')][0]; assert hi == 1 and rows[hi]['v'] == -19.4
mid = [i for i, r in enumerate(rows) if r['v'] == md][0]; assert mid == 11
n = [x for r in rows for x in (r['n0'], r['n1'])]; assert (min(n), max(n)) == (1, 10)
data = {'seed': 'h6g', 'rows': rows, 'min': -26, 'max': 32, 'hi': hi, 'mid': mid,
  'countText': f'{len(rows)}곳', 'downText': f'내림 {dn}', 'upText': f'오름 {up}',
  'hiText': f'은마 −{abs(rows[hi]["v"]):.1f}%', 'ticks': [-20, -10, 10, 20, 30], 'hiRank': f'{len(rows)}곳 중 {hi + 1}번째 · 거래 {rows[hi]["n0"]}건 → {rows[hi]["n1"]}건', 'midText': f'가운데 단지 −{abs(md):.1f}%',
  'countAt': 1.1, 'growAt': 2.1, 'midAt': 3.1, 'hiAt': 4.1, 'backAt': 5.05}
lines = ['같은 강남구에서 34평 크기 거래가 1년 전에도, 요즘에도 있는 단지를 다 찾아봤어요.', '스물세 곳이었습니다.', '그중 열여섯 곳이 내렸어요.',
  '딱 중간에 오는 단지는 6% 가까이 내렸고요.', '은마는 20% 가까이 내려서, 두 번째로 많이 빠졌습니다.', '강남이 대체로 조금 내릴 때, 은마는 더 많이 내린 거예요.']
sc = {'key': 'gap', 'kind': 'gap', 'title': '강남구 34평 단지 23곳 · 1년 변화', 'sub': None, 'chapter': '2. 1년 실거래',
  'source': '국토교통부 실거래 2026-11-25 받음 · 전용 80~86㎡ · 2025.10~12 ↔ 2026.10~11 가운데 값 · 해제·직거래 뺌 · 단지마다 거래 1~10건',
  'data': data, 'lines': [{'text': t, 'audio': None, 'frames': max(75, int(len(t.replace(' ', '')) * 6.2) + 24)} for t in lines]}
sc['frames'] = sum(l['frames'] for l in sc['lines'])
json.dump({'gap': sc}, open(os.path.join(H, 'h6_gap.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(rows), dn, up, md, rows[hi]['name'], rows[mid]['name'], sc['frames'], [l['frames'] for l in sc['lines']])
