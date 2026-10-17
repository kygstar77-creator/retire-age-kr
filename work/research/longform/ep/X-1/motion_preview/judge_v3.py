# X-1 v3 새 장면 셋 — 제미나이 심사(2026-10-17 motion). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'hedge': "질문 2 '국내 상장 S&P500 ETF는 왜 내렸고 (H)는 뭔가' 중 '같은 1억 막대 두 개'(12줄). 같은 회사 두 상품 KODEX 미국S&P500(환노출, 잉크)·KODEX 미국S&P500(H)(환헤지, 파랑) 1억 → 2026.10.16 값(KRX 종가+분배금). 세 쌍은 날짜 순 자리(재작년 첫날 2024.1.2·1년 전·달러 가장 비싸던 날 2026.7.2), 켜지는 순서는 말 순서(7.2 → 1년 전 → 재작년). 1억 점선 아래로 줄어든 몫 빨강, 두 막대 차 = 주황 괄호 '차 …'. '그럼 H형이 늘 나을까요?' 줄에 빈 점선 자리 → 재작년 첫날 쌍에서 환노출이 더 남아 뒤집힘, 1,289원↗1,554원↘1,339원 칩.",
 'even': "질문 1 끝 '그래서 내 계좌는 — 본전 환율'(12줄). 오른쪽 세로 환율 눈금 + 주황 점선 지금 1,339원. 왼쪽 식이 말 따라 조립(본전 환율 = 산 날 환율 ÷ 주가 배수, 앱 달러 수익률 16% → 1.16배로 나누면). 날짜마다 본전 줄이 꽂힘: 지금보다 위(가장 비싸던 날 1,500원·석 달 전 1,463원) = 빨강 틈 '아직 손실', 아래(올해 첫날 1,270원·1년 전 1,220원) = 파랑 틈 '이미 이익'. 조심 줄에서 본전 줄이 흔들림(주가가 움직이면 같이 움직임), 오를·내릴 요인 화살표와 재정경제부 원문 인용, 끝 띠.",
 'below': "질문 5 '여행·직구 갈 사람은 지금 바꿔 둘까요?' 중 '지나간 날과 견주기'(7줄). 2024.1.2~2026.10.15 원/달러 매매기준율 일별 679거래일 원문 선 + 오른쪽 '앞날' 빈 점선 칸 '?'. 지금 높이(1,338.6원) 점선이 과거로 쓸어 감 → 679일 세기 → 그 줄보다 같거나 낮았던 81일이 주황 점 → 선이 원/100엔으로 바뀌며 846.65원 이하 4일 → '달러는 싼 쪽'·'엔화는 거의 가장 싼 값' → '나눠 바꾸면 결과가 가운데로'. 전망·권유 없음.",
}
Q0 = open(os.path.join(H, 'judge_v3_q.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_v3.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write(f'\n## {k} ({m})\n{out}\n'); print('==', k, m); print(out)
