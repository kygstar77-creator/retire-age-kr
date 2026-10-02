# ds-v2 시안 심사(제미나이) — judge_gemini.py와 같은 질문, 같은 모델 순서. py -3.12 ds-v2/judge_v2.py > ds-v2/judge_gemini.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')
import json, base64, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
src = open(os.path.join(os.path.dirname(H), 'judge_gemini.py'), encoding='utf-8').read()
ASK = src.split('ASK = """')[1].split('"""')[0]
MODELS = sys.argv[1:] or ['gemini-3.1-flash-lite']
for key, name in [('salary-v2', '연봉 실수령 계산기 /calc/salary — ds-v2 시안(맨 왼쪽)'), ('stitch-claude', '연봉 실수령 결과 화면 — Claude 시안(맨 왼쪽)')]:
    img = base64.b64encode(open(os.path.join(H, f'compare-{key}-small.png'), 'rb').read()).decode()
    parts = [{'text': ASK.format(name=name)}, {'inline_data': {'mime_type': 'image/png', 'data': img}}]
    print(f'\n## {key}')
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text'])
        except Exception as e:
            print(f'[{m} 실패 {e}]')
