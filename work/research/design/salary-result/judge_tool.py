# X-TOOL-1 심사(제미나이): 같은 시안을 두 도구로 만든 결과를 나란히 보고 점수.
import sys, json, base64, mimetypes, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash']
ASK = """당신은 토스·뱅크샐러드 수준의 한국 핀테크 앱을 심사하는 시니어 프로덕트 디자이너입니다. 냉정하게, 한국어로.
같은 기획(연봉 실수령액 결과 화면 + 아래 쿠팡 광고 1칸, A안·B안)을 두 도구로 만든 시안입니다.
- 이미지1·2: 도구 X(Claude Design 캔버스) 결과 — 이미지1은 캔버스 전체(A안·B안·메모), 이미지2는 A안 확대.
- 이미지3: 도구 Y(코드 시안, 실제 서비스 CSS 부품·Pretendard 글꼴) 결과 — 왼쪽 A안, 오른쪽 B안.
1) 도구 X 결과 점수 1~10, 도구 Y 결과 점수 1~10 (기준: 시각 완성도·글꼴·정렬·여백·모바일 375px에서 실제 구현 가능성). 첫 두 줄은 'X: N' 'Y: N'.
2) 두 결과의 눈에 보이는 차이 5가지
3) A안과 B안 중 어느 쪽이 '숫자 하나 + 행동 하나' 원칙과 광고 신뢰(광고가 결과를 가리지 않음)에 더 맞는지, 이유
4) 두 안 공통으로 고칠 점 3가지"""
def part(p):
    return {'inline_data': {'mime_type': mimetypes.guess_type(p)[0] or 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}}
body = {'contents': [{'parts': [{'text': ASK}] + [part(p) for p in sys.argv[1:]]}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
