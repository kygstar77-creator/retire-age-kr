# P-1 실사 장 머리 StockShot — 제미나이 심사(2026-10-12 motion). 묶음 board_stock.png 한 장.
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
Q = ('한국 재테크 유튜브 롱폼(국민연금 받는 나이: 당기기·제때·미루기) 장이 바뀔 때 3.5초씩 끼우는 "실사 장 머리" 4개 묶음이다(위 줄 1장·4장, 아래 줄 5장·6장 / 각 장 0.7초·3.0초 두 컷). '
     '지금까지 우리 영상은 흰 바탕 차트·카드만 있었고, 사장님이 "다른 채널들은 다 실사 장면을 넣는다"고 해서 만든 부품이다. 경쟁(수페TV·소수몽키)은 주제를 보여 주는 실사 B-roll을 차트 사이에 넣는다. '
     '화면: Pexels 무료 영상(상업 이용 허락) 위에 한쪽만 어둡게 깔고 "N장" 주황 표시 + 대본 장 제목 그대로(2차 고친 판: 1장 생일 케이크 촛불·4장 낙엽 길 발걸음·5장 노트북 치는 손·6장 서류·계산기, 얼굴·국적·상표·연도 없음, 글자 쪽 왼·오 번갈아. 제목: 하루 차이로 한 살? / 평균까지 살면 누가 앞서나 / 519만원 위의 계단 / 445억원은 누구 몫?) + 사실표 원문 칩 한 줄(1969년생부터 65세 / 65세 기대여명 남 19.5년 · 여 23.7년 (평균일 뿐) / 국민연금법 제63조의2 · 2026-06-17 시행 / 신청 없이 7월 말부터 환급). '
     '움직임: 영상 재생 + 천천히 밀어 들어감 + 제목 올라옴/옆에서 들어옴 + 끝 10프레임 어두워짐. 최장 정지 1.0초. '
     '주제와 실사가 맞는지·한눈에 읽힘·정직함(실사가 사실처럼 오해되지 않는지)·영상미를 기준으로 1~10점(6=통과선)을 주고, 잘된 점 1개·약한 점 1개·고칠 점 1개를 한 줄씩. 장별로 가장 약한 장 하나를 꼽는다. 첫 줄은 "점수: N".')
m, out = ask(Q, [os.path.join(H, 'board_stock.png')])
open(os.path.join(H, 'gemini_stock.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
