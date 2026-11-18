# JT-1 4장 쌓이는 잔액(StackGrow) 미리보기 props(11/17 motion) — jt1.json 37·40번 장면(지금 정지 판 jt1_stack.png) 말 줄 그대로
# 숫자 글자는 '500만원' 하나(calc_out §4 초기보증료 5억×1.0%) — assert로 calc_out·대본 줄에 있는지 확인. 나머지는 모양만.
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H)
V = os.path.abspath(os.path.join(EP, '..', '..', '..', '..', 'video'))
sc = json.load(open(os.path.join(V, 'jt1.json'), encoding='utf-8'))['scenes']
ix = [i for i, s in enumerate(sc) if 'jt1_stack.png' in json.dumps(s)]
assert len(ix) == 2, ix
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
assert '5억 → 500만원' in calc
s1, s2 = sc[ix[0]], sc[ix[1]]
assert '500만원' in s1['lines'][4]['text'] and '보증료' in s1['lines'][0]['text'] and '코픽스' in s2['lines'][2]['text'] and '6개월' in s2['lines'][3]['text'] and '0.85%' in s2['lines'][2]['text'] and '매년' in s1['lines'][3]['text'] and '0.95%' in s1['lines'][3]['text']
src = '주택금융공사 자주하는 질문 · 대출잔액 = 받은 돈 + 보증료 + 이자 · 그림은 모양만(금액 아님)'
names = {'pay': '받은 돈', 'fee': '보증료', 'int': '이자'}
out = {
  'stack': {'key': 'stack', 'title': '대출 잔액에 쌓이는 것', 'sub': None, 'chapter': '4', 'source': src, 'lines': s1['lines'], 'frames': s1['frames'],
    'data': {'seed': 'jt1s', 'bars': 6, 'names': names, 'build': [0.0, 1.6],
             'focus': [{'layer': None, 'at': 0}, {'layer': 'fee', 'at': 2, 'bars': 'first'}, {'layer': 'fee', 'at': 3, 'bars': 'rest'}, {'layer': 'fee', 'at': 4, 'bars': 'first'}],   # 11/18 심사: '가입 때 한 번'(첫 막대) vs '매년 0.95%'(나머지)
             'balance': {'text': '대출 잔액', 'at': 1.2}, 'first': {'text': '500만원', 'at': 4.15}, 'wobble': None, 'foot': None,
             'note': {'text': '매년 잔액의 0.95%', 'at': 3.15}}},   # 11/18 U5 8.5초: '매년' 줄에 새 일 하나(대본 자막 [S4] 연보증료)
  'rate': {'key': 'rate', 'title': '이자도 잔액에 붙어요', 'sub': None, 'chapter': '4', 'source': src, 'lines': s2['lines'], 'frames': s2['frames'],
    'data': {'seed': 'jt1r', 'bars': 6, 'names': names, 'build': None,
             'focus': [{'layer': 'int', 'at': 0}],
             'balance': {'text': '대출 잔액', 'at': -1}, 'first': None, 'wobble': {'at': 3.1},
             'foot': {'text': '현금으로 내지 않고 잔액에 더해요', 'at': 1.2},
             'note': {'text': '코픽스 + 0.85%', 'at': 2.35}, 'wobAmp': 0.22, 'origin': '78% 22%', 'pushTo': 1.08}},   # 11/18 심사 rate 5점: 줄마다 새 일 하나(2줄 식·3줄 크게 출렁), 이자 층 쪽으로 다가감
}
json.dump(out, open(os.path.join(H, 'jt1_stack_motion.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', ix, s1['frames'], s2['frames'])
