# 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.abspath(os.path.join(H, '..', '..', 'longform', 'ep', 'E-1'))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']
ASK = """당신은 한국 재테크 유튜브 썸네일 심사위원입니다. 첫 이미지는 비교판입니다(맨 윗줄 왼쪽 3개가 우리 시안 e1a·e1b·e1c, 나머지는 같은 주제 경쟁 상위작 5개와 우리 채널 과거 상위작 3개).
그다음 3장은 시안 e1a, e1b, e1c 원본(1280×720)입니다. 영상: SK하이닉스·삼성전자·마이크론, 이익은 몇 배 늘고 주가는 얼마나 흔들렸나(공시 원문 기준). 제목 후보 "삼성전자 이익 19배, 주가는 3배… SK하이닉스·마이크론은?". 썸네일 숫자: SK하이닉스 1년 +412.9%, 그 안의 최대 낙폭 −54.7%(6/22→7/30). 한국 시세 관례대로 오름 빨강·내림 파랑.
제약: 사람 사진·캐릭터·남의 로고 금지, 오른쪽 아래(영상 길이 표시)와 아래 5%는 비워야 함, 숫자는 사실만, 과장·낚시 금지.
시안마다 냉정하게 한국어로:
1) 휴대폰 목록에서 경쟁 상위작보다 먼저 누르고 싶은가 1~10점 (6 = 경쟁 평균과 비슷). 각 시안 첫 줄은 반드시 'e1a 점수: N' 형식
2) 이유 3가지
3) 320px로 줄였을 때 읽히는가
4) 점수를 2점 올릴 고칠 점 2가지(제약 안에서)
마지막 줄: '1위: e1?'"""
imgs = [os.path.join(H, 'compare.png')] + [os.path.join(EP, f'thumb_{k}.png') for k in ('e1a', 'e1b', 'e1c')]
parts = [{'text': ASK}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in imgs]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
