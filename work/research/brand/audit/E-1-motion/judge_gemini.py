# E-1 영상 그래픽 감사 — 지금(리허설) vs 고친 안 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']
ASK = """당신은 한국 주식·경제 유튜브 롱폼(수페TV·소수몽키급)의 영상 그래픽 심사위원입니다.
이미지는 한 영상(메모리 3사 — 마이크론·SK하이닉스·삼성전자 이익과 주가)의 장면 7개를 줄마다 '왼쪽 = 지금 안 / 오른쪽 = 고친 안'으로 놓은 것입니다.
채널 규칙: 밝은 회색 바탕·검정 글자, 주황 #ff5a00은 '우리 계산기 숫자'와 손그림 강조 동그라미에만, 빨강=오름·파랑=내림(국내 관행)에만. 제목 왼쪽 위+단위·기간, 출처 왼쪽 아래.
지금 안은 SK하이닉스=주황, 삼성전자=파랑으로 회사를 칠했고(삼성 이익 19.14배 증가 막대가 '내림' 파랑), 고친 안은 회사를 검정·회색 단계와 선 모양(실선·긴 점선·짧은 점선)으로 가르고 강조는 검정으로 바꿨습니다.
냉정하게 한국어로:
1) 각 안을 '휴대폰으로 보는 시청자가 숫자를 바로, 틀리지 않게 읽는가 + 보기 좋은가' 1~10점(6 = 국내 경제 유튜브 평균). 첫 줄은 반드시 '지금 점수: N', 둘째 줄 '고친 점수: N'
2) 고친 안이 잃은 것(심심함 등)과 얻은 것 각 2가지
3) 장면 번호를 들어, 고친 안에서 규칙을 지키면서 2점 올릴 수정 2가지
4) 고친 안에서 회사 셋이 선 그래프(장면 12)에서 구분되는가: 예/아니오와 이유"""
parts = [{'text': ASK}, {'inline_data': {'mime_type': 'image/jpeg', 'data': base64.b64encode(open(os.path.join(H, 'compare.jpg'), 'rb').read()).decode()}}]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
