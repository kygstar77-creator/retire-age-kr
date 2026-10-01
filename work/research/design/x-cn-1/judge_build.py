# X-CN-1 한능검 쪽 디자인 검수 심사(제미나이). 구현 캡처 375 지금/놓쳤다면/하루 넘김 + 다크 + 1280.
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-flash-lite-latest']
ASK = """You are a senior product designer judging, coldly, a Korean exam-schedule info page (Korean History Proficiency Test, 한능검), mobile 375px + dark + desktop.
Files: 1) 375 now (10/1, cancel-seat window closes tomorrow) above the fold 2) 375 dark 3) 375 after the deadline passed ('missed' state) 4) 375 when the official cross-check is >24h old ('stale': the line falls back to a link '공식 일정 확인하기') 5) desktop 1280.
Context: competitors on Naver/Google page 1 (13 results) are blog/cafe posts frozen on the day they were written; 5 of 8 Google results show 2025-or-older schedules. This page's one differentiator: a dark card at the very top whose line is recomputed for today, with a stamp 'date · official source HH:MM cross-check' on the same line. New parts: two buttons inside the dark card (white '캘린더에 넣기' = add to calendar, translucent '링크 복사' = copy link).
Criteria: ① one key fact + one action, 4 colors only (bg/ink/gray/one dark navy card), no orange ② readable at 375px, key deadline above the fold ③ is the differentiator visible in the first screen ④ hierarchy inside the dark card: does the stamp compete with the deadline ⑤ state coverage (missed/stale/dark) consistent.
First line 'Score: N' (1-10). Then the biggest problem, then up to 2 fixes. Do not comment on wording."""
def part(f): return {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open('x-cn-1/build/' + f, 'rb').read()).decode()}}
parts = [{'text': ASK}] + [part(f) for f in ['hnk-375-now-fold.png', 'hnk-375-now-dark.png', 'hnk-375-missed-1002-1730.png', 'hnk-375-stale-1003-1800.png', 'hnk-1280-now.png']]
body = {'contents': [{'parts': parts}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]')
