# v3 심사(제미나이) — quality/judge_gemini.py와 같은 질문(ASK), 같은 모델 순서(lite 먼저). py -3.12 judge.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); Q = os.path.join(H, '..', '..', 'quality')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
ASK = open(os.path.join(Q, 'judge_gemini.py'), encoding='utf-8').read().split('ASK = """')[1].split('"""')[0]
name = '연봉 실수령 계산기 /calc/salary — v3 시안(맨 왼쪽, 레퍼런스 토큰 안에서 다시 만든 것). 둘째는 이전 v2f(참고용, 점수 대상 아님)'
img = base64.b64encode(open(os.path.join(H, 'compare-v3-small.png'), 'rb').read()).decode()
parts = [{'text': ASK.format(name=name)}, {'inline_data': {'mime_type': 'image/png', 'data': img}}]
for m in (sys.argv[1:] or ['gemini-3-flash-preview', 'gemini-3.1-flash-lite']):
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text'])
    except Exception as e:
        print(f'[{m} 실패 {e}]')
