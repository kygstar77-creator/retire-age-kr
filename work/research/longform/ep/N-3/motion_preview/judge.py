# N-3 움직이는 판 둘(CapStop·MeanPull) — 제미나이 심사(2026-10-29 motion). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'cap': "'국민연금에는 끝이 있다'(5줄). 연봉 3천·4천·5천·6천·7천·8천 막대(국민연금 보험료 내 몫 한 달, 회색)가 왼쪽부터 차례로 자람 → '659만원까지만' 말에 천장 점선 + 왼쪽 '한 달 659만원까지만' → 1억·1억 2천·1억 5천 막대(먹)가 자라다 천장에 부딪혀 멈춤 → '31만원 정도에서' 말에 주황 '31만원에서 멈춤' + 세 막대 꼭대기 손 동그라미. 막대 높이 = 계산값(10.9만~31.3만원), 천장이 없었다면 얼마였을지는 안 그림. 왼쪽 위 '연봉별 · 국민연금 보험료(내 몫) 한 달'.",
 'mean': "'평균은 앞으로 끌려간다'(7줄). 돈 자(0~6,000, 한 해 총급여·만원)가 왼쪽부터 그어짐 → '4,475만원' 말에 먹 깃발 '평균 4,475만원' 꽂힘 → '줄 한가운데' 말에 회색 깃발 '가운데 사람 3,417만원' → '상위 1%' 말에 자 끝 너머(// 끊김)에 검은 추 '상위 1%' 떨어지고 아래 '평균 3억 4,630만원'(말은 '3억 5천만원 가까이'), 처진 줄이 추에서 평균 깃발 장대로 → '끌어올려요' 말에 줄 팽팽, 평균 깃발이 앞으로 기울고 위 화살표, 가운데 깃발 위 '그대로' → '1천만원쯤 높게' 말에 두 깃발 사이 주황 괄호 + '약 1천만원' + 손 밑줄. 평균 깃발 자리는 옮기지 않음(1%를 뺀 평균은 사실표에 없어서).",
}
Q0 = open(os.path.join(H, 'judge_q.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_n3.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write(f'\n## {k} ({m})\n{out}\n'); print('==', k, m); print(out)
