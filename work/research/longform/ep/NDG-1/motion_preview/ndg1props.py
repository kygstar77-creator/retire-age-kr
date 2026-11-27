# NDG-1 3장 묶음 점 그림(BundleDots) props — calc_dots_out.json(calc_dots.py = calc.py ③ 그대로)에서 만들고 assert (2026-11-27 motion)
# 말 줄은 script.md 그대로(미리보기, 소리 없음). 숫자 글자는 전부 이 파일이 calc에서 만든다 — 대본 숫자와 다르면 여기서 멈춘다.
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H)
c = json.load(open(os.path.join(E, 'calc_dots_out.json'), encoding='utf-8'))
r = [d['r'] for d in c['dots']]
assert len(r) == c['n'] and sum(x >= 1 for x in r) == c['over'] and sum(x < 0.8 for x in r) == c['under80']
assert round(c['median']) == 90, c['median']                     # 대본 '90%'
assert min(r) > 0.55 and max(r) < 1.55, (min(r), max(r))          # 축 50~150% 안
mid = sorted(r)[(len(r) - 1) // 2] * 100
data = {'seed': 'ndg1', 'r': r, 'min': 52, 'max': 152, 'ticks': [60, 80, 100, 120, 140],
        'axis': '2021 최고 대비 %', 'topLine': '2021년 꼭대기 = 100%',
        'dropAt': 0.02, 'sortAt': 0.45, 'mid': {'v': mid, 'text': f"{c['median']:.0f}%", 'ask': '?', 'at': 0.85},
        'lowLine': {'v': 80, 'text': '80%', 'at': 2.1},
        'over': {'text': f"{c['over']}곳", 'at': 3.25}, 'under': {'text': f"{c['under80']}곳", 'at': 4.3}}
S = open(os.path.join(E, 'script.md'), encoding='utf-8').read()
L = ['441곳을 다 모아 보면, 가운데쯤이 꼭대기의 90% 정도예요.', '꼭대기에서 열에 하나 정도 내려온 자리예요.',
     '그런데 묶음마다 많이 갈립니다.', '꼭대기를 이미 넘은 곳이 78곳이고요,', '반대로 꼭대기의 열에 여덟도 안 되는 곳은 68곳입니다.']
for t in L: assert t in S, t
lines = [{'text': t, 'frames': fr} for t, fr in zip(L, (210, 150, 120, 150, 200))]
dots = {'key': 'dots', 'kind': 'dots', 'title': f"노도강 같은 단지·같은 면적 {c['n']}묶음", 'sub': None, 'chapter': '3. 2021년 꼭대기의 몇 %',
        'source': '국토교통부 실거래 · 2026-07~11 가운데 값 ÷ 2021년 최고가 · 자체 계산', 'data': data, 'lines': lines, 'frames': sum(l['frames'] for l in lines)}
json.dump({'dots': dots}, open(os.path.join(H, 'ndg1_dots.json'), 'w', encoding='utf-8'), ensure_ascii=False)
gap = [(a, b) for a, b in ((441, c['n']), (78, c['over']), (68, c['under80'])) if a != b]
print('묶음', c['n'], '· 가운데', c['median'], '· 넘은', c['over'], '· 80% 밑', c['under80'], '· 프레임', dots['frames'], '· 대본과 다른 숫자(대본→지금 자료)', gap)
