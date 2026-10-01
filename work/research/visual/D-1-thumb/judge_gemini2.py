# 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.abspath(os.path.join(H, '..', '..', 'longform', 'ep', 'D-1'))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']
ASK = """당신은 한국 재테크 유튜브 썸네일 심사위원입니다. 첫 이미지는 비교판입니다(경쟁 상위작 5개 = 퇴직 후 건강보험료 주제, 우리 채널 과거 상위작 3개).
그다음 3장은 우리 새 시안 d1a, d1c, d1d 원본(1280×720)입니다. 영상: 퇴직 후 지역가입자 건강보험료, 배당·이자(금융소득) 1년 1,000만원과 1,001만원 경계. 제목 "퇴직 후 건강보험료, 배당·이자 1만원 차이에 1년 54만원?".
사실(사실표): 지역가입자 1인·재산 0·다른 소득 0·2026년 예시에서 연 금융소득 1,000만원이면 월 22,800원(하한), 1,001만원이면 월 67,850원 → 연 540,600원 차이.
제약: 사람 사진·캐릭터·남의 로고 금지, 오른쪽 아래(영상 길이 표시)와 아래 5%는 비워야 함, 숫자는 사실만, 과장·낚시·겁주기 금지.
시안마다 냉정하게 한국어로:
1) 휴대폰 목록에서 경쟁 상위작보다 먼저 누르고 싶은가 1~10점 (6 = 경쟁 평균과 비슷). 각 시안 첫 줄은 반드시 'd1a 점수: N' 형식
2) 이유 3가지
3) 320px로 줄였을 때 읽히는가
4) 점수를 2점 올릴 고칠 점 2가지(제약 안에서)
마지막 줄: '1위: d1?' (d1d는 d1c 그림에 제목 1위와 짝인 한 줄을 붙인 것)"""
imgs = [os.path.join(H, 'compare.png')] + [os.path.join(EP, f'thumb_{k}.png') for k in ('d1a', 'd1c', 'd1d')]
parts = [{'text': ASK}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in imgs]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
