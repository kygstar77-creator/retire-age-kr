# H-2 5장 견본 방식 장면 셋 — 제미나이 심사(2026-10-18 motion). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'rule': "'대출 규칙'(5줄). 집값 축(15억·25억·35억) 위에 '집값의 40%' 경사 점선과 그 아래 회색 면 → '둘 중 작은 쪽' 줄에 금액 한도 계단 점선과 파란 면 → 말 따라 실제 한도 선(둘 중 작은 쪽)이 칸마다 굵게: 15억 이하 6억까지 40% 경사로 올라감 → 15~25억 4억 → 25억 넘음 2억. 오른쪽 칸엔 지금 칸 한도 하나만 주황 큰 숫자, 지난 칸은 회색 작은 줄.",
 'cash': "'손품 씨 계산서'(5줄, 가상 인물). 영수증처럼 한 줄씩: 한 채 값 '집값 ?' → − 주택담보대출 2억 → − 돌려받는 전세 보증금 9억 5,000만원 → 밑줄 → '= 더 있어야 하는 돈 ?'. 단지마다 첫 줄 값이 바뀌고(리센츠 34억 1,500만원 → 주공5단지 43억 4,500만원 → 래미안원베일리 59억, 매매 가운데 값) 답이 '?'로 비었다가 말이 닿으면 주황으로 열리며 손 동그라미, 지난 답은 왼쪽 회색 칩. 취득세·중개보수 빼고 계산.",
 'edge': "'25억이라는 선'(3줄). 21~29억 확대, 한도 선 4억 → 25억에서 2억으로 뚝. 점이 선을 넘는 순간 오른쪽 '이 집 한도' 4억 → '?' → 주황 2억 + 손 동그라미, 빨간 화살표 '절반'. 끝 줄은 점이 25억 위에서 흔들리고 회색 띠 + 검은 카드 '은행이 보는 이 집 값은?'.",
}
Q0 = open(os.path.join(H, 'judge_q.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_eq.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write(f'\n## {k} ({m})\n{out}\n'); print('==', k, m); print(out)
