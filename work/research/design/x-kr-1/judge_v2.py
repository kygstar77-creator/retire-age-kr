# X-KR-1 v2 검수 심사(제미나이). 비교판(우리 1·2장째/크몽) + 2장째 원본 + 시트 2 그림.
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-flash-lite-latest']
O = '../../ventures/x-kr-1/out/'
ASK = """You are a senior product designer judging, coldly, a Korean paid Excel household-budget template (9,900 KRW) sold on Kmong. Answer in Korean.
Files: 1) comparison board: our thumbnail #1 (unchanged), our NEW thumbnail #2 (real 'retirement age' sheet screenshot), and Kmong '가계부' page 1 competitors 2) our thumbnail #2 at 1080x1080 3) sheet 2 full render (big number, inputs, asset-by-age curve, monthly savings-rate bars; example values).
Criteria: ① one number + one action, 4 colors only (white/ink/gray/orange) ② thumbnail #2 readable at ~230px marketplace size ③ does #2 make buyers trust the sheet is real and look as polished as Toss/Banksalad-level products ④ sheet layout clarity.
First line 'Score: N' (1-10). Then the biggest problem, then up to 2 fixes. Do not comment on wording."""
def part(f): return {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(f, 'rb').read()).decode()}}
parts = [{'text': ASK}, part('compare-v2.png'), part(O + 'thumb_2_sheet.png'), part(O + 'sheet2.png')]
body = {'contents': [{'parts': parts}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
