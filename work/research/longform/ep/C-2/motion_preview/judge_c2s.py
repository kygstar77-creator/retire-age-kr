# C-2 쇼츠 c2person 틀 첫 편 c2s_jungwoo — 제미나이 심사(2026-10-14 motion). 묶음 c2s_sheet.png(4초마다 1장, 14장).
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
Q = ('한국 재테크 유튜브 쇼츠(세로 52.5초) 새 틀 "c2person" 첫 편의 4초 간격 화면 15장 묶음이다(왼쪽 위부터 0·4·8…56초, 58.5초짜리). '
     '이야기: 가상 인물 정우 씨가 1998년 퇴직금 3억을 미국 S&P500 총수익 지수에 넣고 매달 200만원씩 팔아 쓰다 2000~2002 하락 → 2007~2008 금융위기 → 2009 반등에도 오를 돈 3천만원 미만 → 2011년 1월(68살, 14년째) 한 해 치를 다 못 꺼냄 · 5년 늦게 시작한 사람은 지난해 말 2억 넘게 남음 · 가른 건 시작한 해. 숫자는 실제 기록 계산. '
     '틀: 위 63%는 SVG 삽화(같은 얼굴 인물, 장면마다 해·장소 바뀜, 천천히 확대·흐름, 장면 7.4초 이하), 위에 고정 질문 2줄, 주황 해 카드, 오른쪽 위 "가상 인물 · 지수·환율은 실제, 통장은 계산", 다른 사람 장면은 흐린 배경, 그림 아래 가장자리에 흰 숫자 카드 하나(장면마다 숫자 하나), 아래 어두운 칸에 상자 없는 큰 3줄 자막(숫자 노랑·나쁜 말 빨강·좋은 말 초록). '
     '바꾸기 전 우리 쇼츠 틀은 흰 판 위 숫자 칸 두 개 + 검은 자막 상자 + 주황 답 띠(그림 0). 비교 대상 경쟁 쇼츠 fOdDiP5-Auc(68만회): 같은 AI 인물이 말에 맞춰 장소를 옮겨 다니고, 가운데 큰 3줄 자막, 화면 숫자는 하나. '
     '첫 1초에 멈출 힘·이야기 흐름이 그림으로 보이는지·한눈에 읽힘·정직함(가상 인물 표시, 숫자가 과장/권유로 읽히지 않는지)·영상미를 기준으로 1~10점(6=통과선)을 주고, 잘된 점 1개·약한 점 1개·고칠 점 1개를 한 줄씩. 가장 약한 장면 하나를 꼽는다. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'c2s_sheet.png')])
open(os.path.join(H, 'gemini_c2s.md'), 'w', encoding='utf-8').write('## 점수(' + str(m) + ')\n' + out + '\n'); print(m); print(out)
