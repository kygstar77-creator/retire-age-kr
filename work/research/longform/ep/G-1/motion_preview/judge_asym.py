# G-1 6장 산 값까지 AsymClimb — 제미나이 심사(2026-10-09 motion). 비교판 board_open.png 한 장.
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
Q = ('한국 재테크 유튜브 롱폼(금값 1천만원 영수증) 6장 "산 값까지의 산수" 장면 17.8초(녹음 전 어림 길이) 8장 묶음이다(위 4장·아래 4장, 시간 순). '
     '말: "대신 산수 하나는 할 수 있어요. 고점에 산 금이 산 값으로 돌아가려면, 지금부터 51% 올라야 해요. 34% 떨어진 걸 메우는 데 51%가 필요한 거죠. 떨어진 만큼만 올라서는 모자라요. 이것도 증권사 수수료나, 골드바라면 팔 때 값 차이를 뺀 숫자예요." '
     '화면: 같은 0원 기준선 위 1g 값 막대 두 개(높이 = 값 비례). 왼쪽 1월 고점 269,810원 막대 → 위 몫이 파랑 빗금 "−33.66% 내려온 폭" → 오늘 179,000원 막대가 오른쪽 칸으로 옮겨 가고 빨강 "+50.7% 산 값까지 올라야 할 폭"이 고점 선까지 쌓임 → 두 폭 사이 "같은 폭" 화살표, 칸 아래 "269,810원의 33.66%" / "179,000원의 50.7%"(기준 막대 테두리) → "34%만 오르면 →" 흰 몫이 고점 선 아래에서 멈추고 남은 주황 빗금 "← 모자라요" → 검은 도장 "수수료·팔 때 값 차이는 뺀 숫자" + 천천히 다가감. 숫자는 calc_out 그대로, 차액 원 숫자는 만들지 않음. 최장 정지 2.2초·움직임 80%. '
     '한눈에 읽힘·정보의 정직함·이탈 막는 힘·영상미를 기준으로 1~10점(6=전달 통과선)을 주고, 잘된 점 1개·약한 점 1개·고칠 점 1개를 한 줄씩. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'board_asym.png')])
open(os.path.join(H, 'gemini_asym.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
