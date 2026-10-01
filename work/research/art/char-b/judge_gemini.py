# 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']
ASK = """(3차: 2차 a 7.5·b 5.8 → 고지서 머리띠 노랑·윗줄 잉크, b 눈썹 걱정형·고지서를 몸에서 뗌) 당신은 한국 재테크 유튜브 썸네일 심사위원입니다. 실험 X-THUMB-1 B군(캐릭터 있음) 캐릭터 시안 2개를 봅니다.
같은 캐릭터(퇴사한 40대 초반 직장인, 이름·말풍선 없음, 실제 인물·전문가 아님)를 그림체 두 가지로 그렸습니다: a = 굵은 외곽선+흰 스티커 테두리 평면, 놀란 얼굴로 고지서를 두 손에 듦 / b = 외곽선 없는 입체감 평면, 이마 짚고 고지서를 멀리 듦.
다음 편 주제: 퇴직(퇴사)하면 건강보험료가 매달 얼마 붙나. 썸네일은 어두운 바탕 + 노랑 줄 + 흰 큰 숫자 줄(문구는 아직 자리만 표시). 캐릭터는 곁다리(썸네일 면적 25% 이하), 오른쪽 아래 길이 표시 자리는 비움.
첫 이미지는 비교판(위: 1280×720 배치 시안 a·b, 아래: 320px 축소본과 80px 캐릭터), 그다음 a·b 캐릭터 원본.
시안마다 냉정하게 한국어로:
1) 휴대폰 목록에서 눈길을 끌고 주제(건보료 고지서 충격)를 돕는가 1~10점 (6 = 한국 재테크 유튜브 평균). 첫 줄은 반드시 'a 점수: N' 형식
2) 이유 3가지 3) 320px에서 표정·고지서가 읽히는가 4) 2점 올릴 고칠 점 2가지
마지막 줄: '1위: ?'"""
imgs = [os.path.join(H, 'compare.png'), os.path.join(H, 'char_a.png'), os.path.join(H, 'char_b.png')]
parts = [{'text': ASK}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in imgs]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
