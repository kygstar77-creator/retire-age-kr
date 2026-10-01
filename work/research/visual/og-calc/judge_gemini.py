# 미감 심사(제미나이 이미지 읽기) — py -3.12 judge_gemini.py > judge_gemini.md
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']
ASK = """당신은 한국 웹서비스 공유 이미지(og:image) 심사위원입니다. 카카오톡·네이버 카페/블로그에 링크를 붙였을 때 뜨는 미리보기 이미지입니다.
첫 이미지는 비교판(위 세 줄 = 우리 시안 9장: a안 가운데 정렬형, b안 왼쪽 글+오른쪽 결과 카드형, c안 = a안을 고친 것(가짜 버튼 없음, 다크 카드 1장에 결과 라벨 → 그 화면에 실제로 있는 질문 줄, 주황은 '몇 살' 하나) / 아래 줄 = 지금 쓰는 이미지(남색, 은퇴 질문)와 경쟁 계산기 사람인·잡코리아·데모데이 공유 이미지).
둘째 이미지는 미리보기 크기판(카톡 큰 말풍선 520px · 작은 카드 260px · 네이버 정사각 썸네일 160px로 잘렸을 때).
서비스: 파이어맵(firemap.kr) — 연봉 실수령·퇴직금·실업급여 계산기. 각 계산기 결과 아래 은퇴 나이로 잇는 질문 줄이 실제로 있음(연봉·퇴직금 '이 돈이면 몇 살에 은퇴?', 실업급여 '재취업 뒤, 몇 살에 은퇴할 수 있을까?').
제약: 문구는 각 페이지 제목 그대로(새 말 짓기 금지), 웹 색(밝은 회색 바탕·검정 글자·주황 #ff5a00은 행동/핵심 숫자만)과 불꽃 로고, 사람 사진·캐릭터 금지.
a안·b안·c안 각각 냉정하게 한국어로:
1) 단톡방에서 이 링크를 보고 누르고 싶은가 1~10점 (6 = 경쟁 평균과 비슷). 첫 줄은 반드시 'a 점수: N', 'b 점수: N', 'c 점수: N' 형식
2) 이유 3가지
3) 260px·160px 정사각에서 읽히는가
4) 점수를 2점 올릴 고칠 점 2가지(제약 안에서)
마지막 줄: '1위: a|b|c'"""
imgs = [os.path.join(H, 'compare.png'), os.path.join(H, 'preview_sizes.png')]
parts = [{'text': ASK}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in imgs]
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
            data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
