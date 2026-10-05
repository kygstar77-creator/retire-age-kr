# 대출 v1 시안 심사(제미나이) — 비교판 + 375 + 375(저장값) + 320 + 다크
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-flash-lite-latest']
ASK = """You are a senior product designer judging, coldly, a Korean mobile loan-interest calculator screen design (375px). Answer in Korean.
Files: 1) comparison board: ours (2 states) vs Naver widget, 부동산계산기.com, Finda, FSS(금감원), and Toss as quality reference 2) ours 375 first screen 3) ours 375 when the user has saved retirement inputs 4) ours 320x568 5) ours dark mode.
Product rules: one hero number (age when the loan is fully repaid) + one action (orange button that leads to the retirement calculator); only white/ink/gray/orange; competitors all show empty inputs + 'calculate' button first and answer in monthly payment.
Question: placed next to Toss/Banksalad, does this look the same quality level? Is the differentiator visible in 3 seconds? Is it clear and trustworthy?
First line 'Score: N' (1-10). Then the biggest problem, then up to 2 layout fixes. Do not comment on wording."""
def part(f): return {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(f, 'rb').read()).decode()}}
parts = [{'text': ASK}] + [part(f) for f in ('compare-v1.png', 'v1-375.png', 'v1-375-b.png', 'v1-320.png', 'v1-375-dark.png')]
body = {'contents': [{'parts': parts}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
