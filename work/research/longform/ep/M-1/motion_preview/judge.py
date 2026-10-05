# M-1 첫 장면 거꾸로 묻기 — 제미나이 심사(2026-10-05 motion). 비교판 board_open.png 한 장.
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite']
def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    for m in MODELS:
        try:
            r = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', json.dumps({'contents': [{'parts': parts}]}).encode(), {'Content-Type': 'application/json'})
            return m, json.load(urllib.request.urlopen(r, timeout=120))['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(m, str(e)[:80])
    return None, ''
Q = ('한국 재테크 유튜브 롱폼(월배당, 매달 100만원 받으려면 얼마 있어야 하나)의 첫 장면 56초 비교판이다. 1~2줄 "새" = 우리 첫 장면 8장(2초: 큰돈→매달? 보통 방향 화살표 → 8.7초: 큰돈에 줄 → 15.7초: 화살표가 거꾸로 매달 100만원→??? → 30초: ?가 막대 자리로 내려앉아 0 기준선에서 자람 → 33·39초: 말이 가리키는 막대만 주황 → 50·55초: 세 상품을 같은 규칙으로 — ACE 8.92억·JEPQ 1.71억으로 늘어남(빗금=늘어난 몫), SCHD는 분기 지급 칩). '
     '3줄 = 경쟁 수페TV·소수몽키 첫 장면. 첫 30초 이탈을 막는 힘·한눈에 읽힘·정보의 정직함(막대 길이는 값 비례)·영상미를 기준으로 "새"에 1~10점(6=전달 통과선)을 주고, '
     '경쟁보다 나은 점 1개·경쟁 1등보다 못한 점 1개·고칠 점 1개를 한 줄씩. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'board_open.png')])
open(os.path.join(H, 'gemini.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
