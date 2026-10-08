# M-1 첫 장면 거꾸로 묻기 — 제미나이 심사(2026-10-05 motion). 비교판 board_open.png 한 장.
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
Q = ('한국 재테크 유튜브 롱폼(월배당, 매달 100만원 받으려면 얼마 있어야 하나)의 첫 장면 46.8초(실제 녹음 길이) 8장 묶음이다(위 4장·아래 4장, 0.7초: 판 가득 큰 숫자 "매달 100만원 · 지금 얼마가 있어야 할까요?" → 5초: 카메라가 천천히 다가가며 지폐가 쌓인 큰돈 카드→매달? 보통 방향 화살표 → 7.7초: 말 "큰돈이 없잖아요"에 큰돈 카드가 판 전체를 덮는 어두운 판이 됐다가 줄이 그어지고 지폐가 떨어지며 걷힘 → 11초: 카메라가 1.3배 당겨 판 가득, 화살표가 거꾸로 매달 100만원→??? → 18.7초: ?가 막대 자리로 내려앉아 0 기준선에서 자람 → 20.7초: 어두운 도장 판 「2026년 10월 2일 기준 · 사라는 얘기가 아니라, 지난 기록으로 한 계산」이 내려앉았다 위로 걷힘 → 36.7초: 말이 가리키는 막대만 진하게 → 45.7초(끝까지 천천히 다가감): 세 상품을 같은 규칙으로 — ACE 8.92억·JEPQ 1.71억으로 늘어남(빗금=늘어난 몫), SCHD는 분기 지급 칩). '
     '첫 30초 이탈을 막는 힘·한눈에 읽힘·정보의 정직함(막대 길이는 값 비례)·영상미를 기준으로 "새"에 1~10점(6=전달 통과선)을 주고, '
     '잘된 점 1개·약한 점 1개·고칠 점 1개를 한 줄씩. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'board_v1008.png')])
open(os.path.join(H, 'gemini_v1008.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
