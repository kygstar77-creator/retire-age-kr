# CC-1 7장 '끝날 6개' 움직이는 판(EndFlip) props — cc1_windows_out_1122.txt에서 직접 읽고 script.md 자막과 assert (2026-11-26 motion)
# 말 줄 = voice.json 88~91(cc1props board('cc1_ends6', [88, 89, 90, 91])와 같은 줄, 길이 frames−GAP_TRIM 3). 숫자는 이 파일이 calc 출력에서 만든다.
# 쓰는 법: py -3.12 endflipprops.py → cc1_ends.json (미리보기 CC1Ends · 본편은 PD가 cc1props mo()로 같은 data를 넣음)
import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H)
txt = open(os.path.join(E, 'cc1_windows_out_1122.txt'), encoding='utf-8').read()
SCRIPT = open(os.path.join(E, 'script.md'), encoding='utf-8').read()
raw = re.findall(r'^(\d{4})-(\d{2})-(\d{2}) ([\d.]+) ([\d.]+) (커버드콜|일반형)$', txt, re.M)
assert len(raw) == 6, raw
rows = []
for y, m, d, a, b, lead in raw:
    a, b = float(a), float(b)
    assert (a >= b) == (lead == '커버드콜'), (y, m, a, b, lead)
    assert f'{y}-{m}-{d} {a}% vs {b}%' in SCRIPT, ('자막에 없음', y, m, d)      # 화면 숫자 = 대본 자막 숫자
    rows.append({'date': f'{y}년 {int(m)}월', 'a': a, 'b': b, 'iso': f'{y}-{m}-{d}'})
na = sum(r['a'] >= r['b'] for r in rows); nb = len(rows) - na
assert (na, nb) == (4, 2) and '끝날 6개 중 4개 커버드콜' in SCRIPT
# 말한 순서(대본 158~161행): 2025년 12월 → 2026년 11월 → 같은 해 6월 → 2024년 말
V = json.load(open(os.path.join(E, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
said = {88: '2025년 12월', 89: '2026년 11월', 90: '6월', 91: '2024년 말'}
iso = {88: '2025-12', 89: '2026-11', 90: '2026-06', 91: '2024-12'}
for i, w in said.items(): assert w in ALL[i]['text'], (i, ALL[i]['text'])
assert '여섯 번' in ALL[92]['text'] and '더 많았' in ALL[92]['text'], ALL[92]['text']
order = [[k for k, r in enumerate(rows) if r['iso'].startswith(iso[i])][0] for i in (88, 89, 90, 91)]
assert order == [2, 5, 4, 0], order
lines = [{'text': ALL[i]['text'], 'audio': ALL[i]['audio'], 'frames': ALL[i]['frames'] - 3} for i in (88, 89, 90, 91, 92)]   # 11/26 심사: 92 '끝날을 여섯 번 바꿔 보니, 커버드콜이 앞선 때가 더 많았어요'에 남은 두 줄·세기가 열려야 함(91 '크지 않았습니다'와 겹치면 4·2 차이로 읽힘)
tot = sum(l['frames'] for l in lines)
data = {'seed': 'cc1e', 'names': ['커버드콜', '일반형'], 'rows': [{k: r[k] for k in ('date', 'a', 'b')} for r in rows], 'order': order,
        'restAt': 4.0, 'tallyAt': 4.35, 'tallyText': [f'커버드콜 {na}', f'일반형 {nb}'], 'unit': '%', 'max': 48, 'end': tot}
sc = {'key': 'ends', 'kind': 'ends', 'title': '기간을 어디서 자르느냐 · 1년 총수익', 'sub': None, 'chapter': '7. 함정',
      'source': '분배 포함·세전 · 야후 파이낸스 수정 종가 · KODEX 미국배당커버드콜액티브 vs TIGER 미국배당다우존스',
      'data': data, 'lines': lines, 'frames': tot}
json.dump({'ends': sc}, open(os.path.join(H, 'cc1_ends.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', [(r['date'], r['a'], r['b']) for r in rows], 'order', order, f'{tot}프레임 {tot / 30:.1f}초', [l['frames'] for l in lines])
