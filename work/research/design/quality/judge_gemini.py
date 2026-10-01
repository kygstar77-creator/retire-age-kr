# 운영 화면 5종 미감 심사(제미나이 이미지 읽기) — 8점 관문 기준선. py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.1-flash-lite', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-3-flash-preview']
ASK = """당신은 한국 핀테크 앱(토스·뱅크샐러드) 수준을 아는 모바일 UI 심사위원입니다.
이미지는 휴대폰 375px 화면 비교판입니다. 맨 왼쪽(또는 'firemap'/'우리' 표시)이 파이어맵(firemap.kr, 은퇴·돈 계산기) 운영 화면, 나머지는 같은 일을 하는 화면(네이버 임금계산기 위젯) 또는 완성도 기준(토스·뱅크샐러드 첫 화면)입니다.
화면: {name}
냉정하게 한국어로:
1) 첫 줄은 반드시 '점수: N' (1~10, 질문: 토스·뱅크샐러드 화면 옆에 놓았을 때 같은 수준의 회사가 만든 것처럼 보이나. 6 = 국내 개인 사이트 평균, 8 = 토스 옆에 놓아도 어색하지 않음)
2) 점수를 깎은 이유 3개(화면에서 보이는 것만, 위치를 들어서)
3) 8점으로 올릴 고칠 점 3개(구체적: 무엇을 빼거나 합치거나 키울지)"""
BOARDS = [('home', '첫 화면 /'), ('salary', '연봉 실수령 계산기 /calc/salary'), ('severance', '퇴직금 계산기 /calc/severance'), ('unemp', '실업급여 계산기 /calc/unemployment-benefit'), ('guide', '가이드 목록 /guide/')]
for key, name in BOARDS:
    img = base64.b64encode(open(os.path.join(H, f'compare-{key}-small.png'), 'rb').read()).decode()
    parts = [{'text': ASK.format(name=name)}, {'inline_data': {'mime_type': 'image/png', 'data': img}}]
    print(f'\n## {key} — {name}')
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
        except Exception as e:
            print(f'[{m} 실패 {e}]', file=sys.stderr)
