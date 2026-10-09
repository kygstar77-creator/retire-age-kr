# G-1 첫 장면 산 날 영수증 — 제미나이 심사(2026-10-05 motion). 비교판 board_open.png 한 장.
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.8-pro', 'gemini-3-pro-preview', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite']
def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    for m in MODELS:
        try:
            r = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', json.dumps({'contents': [{'parts': parts}]}).encode(), {'Content-Type': 'application/json'})
            return m, json.load(urllib.request.urlopen(r, timeout=120))['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(m, str(e)[:80])
    return None, ''
Q = ('한국 재테크 유튜브 롱폼(금값, 금 1천만원어치를 산 날에 따라 지금 얼마인가)의 첫 장면 12.2초(녹음 전 어림 길이) 8장 묶음이다(위 4장·아래 4장, 0.8초: 어두운 판 가득 "올해 1월, 금값이 꼭대기였던 날 천만원어치를 샀다면 / 지금 663만원" → 2.4초: 어두운 판이 1월 고점 점으로 빨려 들며 걷히고 KRX 금 1년 선이 그려짐 → 3.5~5초: 고점 점에서 오늘 값 점선까지 내려온 선, 점에서 1천만원 덩이가 오른쪽 막대 자리로 날아가 오늘 값(663만원)만큼 줄어듦, 줄어든 몫은 빗금·낸 돈은 점선 테두리 → 6.3~7.6초: 말 "작년 이맘때 샀다면 956만원"에 1년 전 점에서 두 번째 막대가 같은 규칙으로 → 9.5~11.8초: 말 "같은 금인데 산 날만 달랐던 거죠"에 선이 흐려지고 큰 글씨 "같은 금, 산 날만 달랐다 →" + 두 막대 밑 괄호, 카메라 천천히 다가감). '
     '첫 30초 이탈을 막는 힘·한눈에 읽힘·정보의 정직함(막대 높이는 값/낸 돈 비례, 0 기준선 공유)·영상미를 기준으로 1~10점(6=전달 통과선)을 주고, '
     '잘된 점 1개·약한 점 1개·고칠 점 1개를 한 줄씩. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'board_open.png')])
open(os.path.join(H, 'gemini.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
