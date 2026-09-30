# F1 쿠팡 칸 디자인 관문 심사(제미나이). 이미지 compare.png 한 장: X 현재 구현, Y 수정안, 경쟁.
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash']
ASK = """당신은 토스·뱅크샐러드 수준 한국 핀테크 화면을 심사하는 시니어 프로덕트 디자이너입니다. 냉정하게, 한국어로.
이미지는 휴대폰 375px 계산기 결과 페이지 아래의 쿠팡 파트너스 광고 1칸입니다(상품명은 예시). 왼쪽 X=현재 구현, 가운데 Y=수정안, 오른쪽=경쟁 연봉 계산기 사이트의 쿠팡 배너.
기준: ① 광고가 사이트 내부 링크로 오인되지 않는가(위장 없음) ② 대가성 문구가 쉽게 읽히고 링크 바로 위에 있는가 ③ 광고가 본문·핵심 행동보다 눈에 띄지 않는가(주황은 행동 버튼 전용 브랜드 원칙) ④ 정돈·여백·신뢰감.
첫 두 줄은 'X: N' 'Y: N'(1~10). 이어서 각 안의 가장 큰 문제 1개씩, Y에서 더 고칠 점 2개."""
img = base64.b64encode(open('compare.png', 'rb').read()).decode()
body = {'contents': [{'parts': [{'text': ASK}, {'inline_data': {'mime_type': 'image/png', 'data': img}}]}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
