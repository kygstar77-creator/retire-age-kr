# 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini_r1.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-flash-latest', 'gemini-3.1-flash-lite']
ASK = open(os.path.join(H, 'judge_ask.txt'), encoding='utf-8').read()
parts = [{'text': ASK}, {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(os.path.join(H, 'board.png'), 'rb').read()).decode()}}]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
