# 조직도 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_org.py org-chart.png
import sys, json, base64, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash']
ASK = """당신은 인포그래픽 디자이너이자 심사위원입니다. 이 이미지는 AI 직원으로 운영되는 작은 회사의 조직도로, 대표가 휴대폰(1080×1920)에서 확대 없이 한눈에 보려는 용도입니다.
잘 만든 회사 조직도·인포그래픽(Creately·Buffer·Canva 템플릿 수준)과 비교해 냉정하게 한국어로 평가하세요.
1) 1~10점(6점 = 잘 만든 일반 템플릿과 비슷). 첫 줄은 반드시 '점수: N'
2) 이유 3가지
3) 3초 안에 이해되는 것 / 헷갈리는 것
4) 점수를 2점 올릴 가장 효과 큰 고칠 점 3가지(구체적으로)"""
img = base64.b64encode(open(sys.argv[1], 'rb').read()).decode()
body = {'contents': [{'parts': [{'text': ASK}, {'inline_data': {'mime_type': 'image/png', 'data': img}}]}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
