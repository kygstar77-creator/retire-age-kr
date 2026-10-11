# W-1 8차 점수(제미나이) — judge.py ask 재사용 없이 같은 모델·같은 판(r8_board168/480). py -3.12 r8_score.py [회차표시]
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
M = os.environ.get('JUDGE_MODEL', 'gemini-3.1-flash-lite')
PRE = os.environ.get('PRE', 'r8_')
T = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 w1?"가 공개 전 시안, "경쟁"은 같은 주제(삼성전자 실적·코스피 하락) 최근 30일 상위작.\n'
     '영상: 주간 코너 1화. 삼성전자가 3분기 영업이익 107.4조원(잠정)을 공시한 주, 주가는 10/2→10/8 거래일 사흘 −5.07%. 삼성전자 100주 평가액 −140만원 = 세후 분기 배당 44번치, 코스피 1천만원 −54만원, 미국 1만 달러 원화 평가를 DART·한국은행 원문으로 계산. 원인 추측·전망·매수 권유 없음.\n'
     '제목(썸네일 옆에 같이 보임): "삼성전자 주가 사흘 −5.07%, 100주 평가액 −140만원 = 분기 배당 44번치".\n'
     '제약: 인물·캐릭터·사진 금지, 과장·낚시 금지, 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n'
     '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가."\n'
     '시안마다: 첫 줄 "w1? 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · 107조가 무엇의 숫자로 읽히나(실적/손실/모름) · −140만이 공시 때문에 생긴 손실(원인)로 읽히나(예/아니오) · 후킹 장치(반전/질문/비교/내 돈 대입/없음) · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n'
     '마지막 줄: "1위: w1?"')
parts = [{'text': T}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(os.path.join(H, PRE + n), 'rb').read()).decode()}} for n in ('board168.png', 'board480.png')]
r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',
    data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
out = f'[모델 {M}]\n' + r['candidates'][0]['content']['parts'][0]['text']
tag = sys.argv[1] if len(sys.argv) > 1 else 's1'
open(os.path.join(H, f'{PRE[:-1]}{tag}_gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)
