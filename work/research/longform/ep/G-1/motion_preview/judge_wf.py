# G-1 3장 세 조각 폭포 막대 — 제미나이 심사(2026-10-09 motion). 비교판 board_open.png 한 장.
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.8-pro', 'gemini-3-pro-preview', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite']
def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    for m in MODELS:
        try:
            r = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', json.dumps({'contents': [{'parts': parts}]}).encode(), {'Content-Type': 'application/json'})
            return m, json.load(urllib.request.urlopen(r, timeout=120))['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(m, str(e)[:80])
    return None, ''
Q = ('한국 재테크 유튜브 롱폼(금값 1천만원 영수증) 3장 "세 조각" 장면 34.5초(녹음 전 어림 길이) 8장 묶음이다(위 4장·아래 4장). '
     '말: 작년(25.10.02)에 산 금이 왜 −4.43%인지 — KRX 금값 = 달러 금값 × 환율 × KRX 웃돈. 화면: 0 기준선(산 날 값)에서 폭포 막대가 차례로 — 달러 금값 +6.65%(빨강, 위로) → 환율 −3.38%(파랑, 앞 막대 끝에서 아래로) → KRX 웃돈 −7.26%(파랑, 0 아래까지) → "= 내 금" −4.43%(주황, 0부터, 셋째 막대 끝과 같은 높이) + "1천만원 → 9,556,861원". '
     '웃돈 꼬리표 "그때 +6.3% → 지금 −1.4%", "이 웃돈이 빠진 것만으로도"에 −7.26% 손 동그라미, 결론 "금값이 아니라 환율·웃돈에서 잃었다 →"(첫 막대 흐려짐). 막대 길이 = 곱을 로그로 나눈 %p(합 = 전체), 글자 = 곱 비율. 말마다 카메라가 해당 칸으로 다가갔다 물러남(최장 정지 2.8초). '
     '한눈에 읽힘·정보의 정직함·이탈 막는 힘·영상미를 기준으로 1~10점(6=전달 통과선)을 주고, 잘된 점 1개·약한 점 1개·고칠 점 1개를 한 줄씩. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'board_wf.png')])
open(os.path.join(H, 'gemini_wf.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
