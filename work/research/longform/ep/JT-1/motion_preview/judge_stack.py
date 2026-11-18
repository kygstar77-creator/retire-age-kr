# JT-1 StackGrow — 제미나이 심사(2026-11-17 motion, judge.py 그대로, N-3 judge.py 틀). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'stack': "4장 '대출 잔액에 쌓이는 것' 5줄. 금액 축 없는 모양 그림: 손으로 그린 빗금 막대 6개가 왼쪽부터 아래에서 차오른다. 막대마다 세 층(아래 먹 '받은 돈' → 회색 '보증료' 얇게 → 위 황갈색 '이자', 이자 층은 뒤 막대일수록 두꺼움), 오른쪽에 층 이름표. 2줄 '대출 잔액' 마지막 막대 오른쪽 세로 괄호 → 3줄 '가입 때 1% 한 번' 첫 막대 보증료만 진하게 → 4줄 '매년 잔액의 0.95%' 나머지 막대 보증료 진하게 + 먹 글씨 '매년 잔액의 0.95%'(11/18) → 5줄 첫 막대 보증료 칸 손 동그라미 + 주황 '500만원'(5억 집 초기보증료 1%). 출처 줄에 '그림은 모양만(금액 아님)'.",
 'rate': "같은 장 4줄 '이자도 잔액에 붙어요'. 막대 6개가 다 선 채로 이자 층만 진하게, 2줄 아래 주황 한 줄 '현금으로 내지 않고 잔액에 더해요', 4줄 '기준금리가 6개월마다 바뀌니까'에서 이자 층 높이가 천천히 출렁 + 이름표 위 '↕ 변동'. 3줄에 먹 글씨 '코픽스 + 0.85%'(대본 자막 출처), 카메라는 이자 층 쪽으로 천천히 다가감(11/18).",
}
Q0 = open(os.path.join(H, 'judge_q_stack.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_stack.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write('\n## %s (%s)\n%s\n' % (k, m, out)); print('==', k, m); print(out)
