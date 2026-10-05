# 제미나이 심사 — R-1-thumb/judge.py의 ask() 재사용. py -3.12 judge.py
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', '..', 'R-1-thumb'))
import types
src = open(os.path.join(H, '..', '..', 'R-1-thumb', 'judge.py'), encoding='utf-8').read()
J = types.SimpleNamespace(); g = {'__file__': os.path.join(H, '..', '..', 'R-1-thumb', 'judge.py'), '__name__': 'rj'}
exec(src[:src.index("{'boards'")], g); J.ask = g['ask']  # 끝의 명령 분기만 빼고 불러옴
t = ('유튜브 롱폼 썸네일 시안 3장 비교입니다(첫 이미지 480px 판, 둘째 168px 판 — 휴대폰 목록 실제 크기). 영상 주제: 1억을 예금·금·S&P500·SCHD에 1년 넣었을 때 세금 뗀 뒤 결과 비교(과거 값). '
     '시안: r2e(현재 후보, 사물 없음) / A(줄마다 앞에 금괴·꺾은선·동전 아이콘 + 통장) / B(통장 아이콘 하나만). 규칙: 캐릭터·사람 사진 금지, 사물 아이콘은 허용. '
     '각 시안 1~10점(7 통과, 8 목표)으로 168px에서 클릭하고 싶은 정도를 매기고, 아이콘이 이해를 돕는지·잡음인지 한 줄씩. 형식:\nr2e: 점수 | 한 줄\nA: 점수 | 한 줄\nB: 점수 | 한 줄\n마지막 줄: 셋 중 쓸 것 하나와 이유.')
out = J.ask(t, [os.path.join(H, 'board480.png'), os.path.join(H, 'board168.png')])
open(os.path.join(H, 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)
