# X-V1 /60-percent-tax-trap/ 디자인 검수 심사(제미나이). 375px £110,000 라이트·다크, £90,000.
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash']
ASK = """You are a senior product designer judging a UK '60% tax trap calculator' mobile page (375px first screen), coldly. Answer in Korean.
Images: 1) £110,000 light 2) £110,000 dark 3) £90,000 light (outside band).
Context: the 10 page-1 Google results for '60% tax trap calculator' are all dedicated calculators that show the 60% rate and pension contribution needed; this site's one differentiator elsewhere is showing in POUNDS how much of the next £1,000 you keep (not a %).
Criteria: ① one number + one action on first screen ② readability at 375 ③ does the differentiator (pounds on next £1,000) appear in the £110,000 case? ④ trust/no ad feel.
First line 'Score: N' (1-10). Then the biggest problem, then up to 2 fixes."""
parts = [{'text': ASK}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open('build/' + f, 'rb').read()).decode()}} for f in ['trap-375-110000-light.png', 'trap-375-110000-dark.png', 'trap-375-90000-light.png']]
body = {'contents': [{'parts': parts}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
