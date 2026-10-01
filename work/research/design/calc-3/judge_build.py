# calc-3 퇴직금 숫자 줄·버튼 자리 디자인 검수 심사(제미나이). 구현 캡처 375(숫자 줄 있음/없음) + 데스크톱.
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-flash-lite-latest']
ASK = """You are a senior product designer judging, coldly, a Korean severance-pay calculator result screen (mobile 375px + desktop).
Files: 1) 375px with the new gain line inside the result card ('퇴직금 N원을 더하면 / 파이어 나이가 N년 앞당겨져요') 2) 375px when the gain line is hidden (user has no saved inputs) 3) desktop with gain line.
Context: competitors (official labor ministry, Saramin, Incruit) show only the severance amount; MyMoneySim adds a plain link '파이어족 시뮬 →'. This design's one differentiator: a preview of the answer (years earlier you can retire) inside the result card, with ONE orange button right below ('이 돈이면 몇 살에 은퇴?').
Criteria: ① one hero number + one action, 4 colors only (white/ink/gray/orange) ② readable at 375px, above the fold ③ is the differentiator visible in the first screen ④ hierarchy: does the gain line compete with the hero number.
First line 'Score: N' (1-10). Then the biggest problem, then up to 2 fixes. Do not comment on wording."""
def part(f, mt): return {'inline_data': {'mime_type': mt, 'data': base64.b64encode(open('build/' + f, 'rb').read()).decode()}}
parts = [{'text': ASK}, part('severance-A-real-375.png', 'image/png'), part('severance-B-new-375.png', 'image/png'), part('severance-A-real-desktop.png', 'image/png')]
body = {'contents': [{'parts': parts}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
