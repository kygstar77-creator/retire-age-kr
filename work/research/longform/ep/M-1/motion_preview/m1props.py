# M-1 첫 장면 ReverseAsk 미리보기 props — 숫자는 calc_out.txt에서만(assert 대조), 말은 script.v2.md 원문.
# 프레임은 목소리 전 어림(글자 수 × 4.6프레임) — 녹음 뒤 voice.json 길이로 다시 맞춘다.
import json, re, pathlib
E = pathlib.Path(__file__).resolve().parents[1]
calc = (E / 'calc_out.txt').read_text(encoding='utf-8')
script = (E / 'script.v2.md').read_text(encoding='utf-8')
bars = [['JEPQ', 1.38, '1.38억원'], ['SCHD', 4.85, '4.85억원'], ['ACE 미국배당다우존스', 5.10, '5.10억원']]
for name, v, lab in bars:
    assert f'필요 원금 {v:.2f}억원' in calc.split(f'## {name}')[1].split('##')[0], name
low = {'i': 2, 'v': 8.92, 'label': '8.92억원', 'times': '×1.75', 'tag': '가장 적은 달 기준'}
assert '가장 적은 달 기준이면 8.92억원(×1.75)' in calc
also = [{'i': 0, 'v': 1.71, 'label': '1.71억원', 'times': '×1.23'}]
assert '가장 적은 달 기준이면 1.71억원(×1.23)' in calc
note = [[1, '분기 1회 지급 · 달마다 아님']]
assert '분기 1회 — 매달이 아님' in calc
says = [
 ('월배당 영상은 보통 이렇게 시작하죠. 큰돈을 넣으면 매달 얼마가 나온다.', None),
 ('근데 대부분은 그런 큰돈이 없잖아요. 그러면 거꾸로 묻는 게 맞죠.', None),
 ('매달 100만원이 필요하면, 지금 얼마가 있어야 할까요?', '세금 · 건강보험료까지 뗀 뒤 손에 남는 돈 기준'),
 ('지난 1년 동안 실제로 나온 분배금으로, 상품 셋을 거꾸로 계산해 봤어요.', None),
 ('2026년 10월 2일 기준입니다. 사라는 얘기가 아니라, 지난 기록으로 한 계산입니다.', None),
 ('가장 적게 필요한 상품은 1억 4천만원 가까이였어요.', 'JEPQ 1.38억원 · SCHD 4.85억원 · ACE 미국배당다우존스 5.10억원 (세후·건보료 뒤 월 100만원)'),
 ('가장 많이 필요한 상품은 5억이 넘었고요.', None),
 ('그런데 이 숫자, 다시 재면 확 바뀌어요.', None),
 ('매달 분배금이 똑같이 나오지 않거든요. 가장 적게 나온 달로 다시 재 보면, 한 상품은 5억에서 9억 가까이로 늘어납니다.', None),
]
for t, c in says:
    assert '- ' + t in script, t
    if c: assert f'[자막: {c}]' in script, c
lines = [{'text': t, 'cap': c, 'frames': int(len(t) * 4.6) + 12, 'audio': None} for t, c in says]
st = [0]
for l in lines: st.append(st[-1] + l['frames'])
rev = {'seed': 'M-1', 'big': '큰돈', 'ask0': '매달 ?', 'goal': '매달 100만원', 'goalSub': '세금·건보료 뗀 뒤',
       'bars': bars, 'low': low, 'also': also, 'note': note,
       'fwd': st[0] + 40, 'nope': st[1] + 20, 'rev': st[2] + 10, 'land': st[3] + 20, 'grow': st[4] + 20,
       'hi': [[st[5] + 6, 0], [st[6] + 6, 2], [st[7] + 6, -1]], 'low0': st[8] + 30}
scene = {'key': 'open', 'kind': 'open', 'title': '매달 100만원 받으려면 얼마 있어야 하나',
         'sub': '지난 1년 실제 분배금 · 세금·건강보험료 뗀 뒤 · 2026-10-02 기준',
         'source': '운용사·거래소 분배 기록, 거래소 종가, 한국은행 ECOS, 법제처 · 과거 값 · 미래 보장 아님 · 투자 권유 아님',
         'chapter': None, 'data': {}, 'lines': lines, 'frames': st[-1] + 20}
out = pathlib.Path(__file__).with_name('m1_open.json')
out.write_text(json.dumps({'scene': scene, 'rev': rev}, ensure_ascii=False, indent=1), encoding='utf-8')
print('frames', scene['frames'], 'starts', st, 'rev', {k: rev[k] for k in ('fwd', 'rev', 'grow', 'hi', 'low0')})
