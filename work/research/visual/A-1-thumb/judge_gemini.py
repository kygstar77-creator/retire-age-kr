# 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.abspath(os.path.join(H, '..', '..', 'longform', 'ep', 'A-1'))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash']
ASK = """당신은 한국 재테크 유튜브 썸네일 심사위원입니다. 첫 이미지는 비교판입니다(맨 윗줄 왼쪽 3개가 우리 시안 v5a·v5b·v5c, 넷째가 지금 걸린 썸네일, 둘째·셋째 줄은 경쟁 상위작과 우리 채널 과거작).
그다음 3장은 시안 v5a, v5b, v5c 원본(1280×720)입니다. 영상: JEPQ와 SCHD에 1억씩 넣고 1년 뒤 남은 돈 비교(JEPQ 분배율 12%지만 SCHD보다 783만원 덜 남음).
제약: 사람 사진·캐릭터 금지, 오른쪽 아래(영상 길이 표시)와 아래 5%는 비워야 함, 숫자는 사실만.
시안마다 냉정하게 한국어로:
1) 휴대폰 목록에서 경쟁 상위작보다 먼저 누르고 싶은가 1~10점 (6 = 경쟁 평균과 비슷). 각 시안 첫 줄은 반드시 'v5a 점수: N' 형식
2) 이유 3가지
3) 320px로 줄였을 때 읽히는가
4) 점수를 2점 올릴 고칠 점 2가지(제약 안에서)
마지막 줄: '1위: v5?'"""
imgs = [os.path.join(H, 'compare.png')] + [os.path.join(EP, f'thumb_{k}.png') for k in ('v5a', 'v5b', 'v5c')]
parts = [{'text': ASK}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in imgs]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
