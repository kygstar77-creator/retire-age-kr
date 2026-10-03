# 표지 심사 — 제미나이 이미지 입력(1초 시험 + 10점). firemap-write 2026-10-03
import base64, json, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
ASK = ("이 그림은 네이버 카페 글 목록에 정사각 썸네일(작게, 약 168px)로 보이는 대표 그림입니다. "
       "① 1초만 봤을 때 무슨 글인지 한 줄로 말해 보세요. ② 1초 가독성·숫자 하나 강조·과장 여부·글 제목 '퇴직 후 건강보험료, 배당·이자 1천만원 넘는 순간 월 4.5만원 더'와의 일치를 따져 10점 만점 점수를 주고, 깎은 이유를 두 줄로. "
       "마지막 줄은 '점수: N' 형식. 한국어로.")
img = base64.b64encode(open('pkg/img/00.png', 'rb').read()).decode()
body = json.dumps({'contents': [{'parts': [{'text': ASK}, {'inline_data': {'mime_type': 'image/png', 'data': img}}]}]}).encode()
for m in ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']:
    try:
        r = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', body, {'Content-Type': 'application/json'})
        d = json.load(urllib.request.urlopen(r, timeout=120))
        print(f'[{m}]'); print(d['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e: print(m, str(e)[:60])
