import sys, os, json, base64, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(H, '..', '..', '..', 'visual', 'cafe-covers-1002')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
M = 'gemini-3.1-flash-lite'
def ask(text, p):
    parts = [{'text': text}, {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}}]
    err = ''
    for t in range(3):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err = str(e); time.sleep(4)
    return f'(실패 {err})'
PS = ('한국 재테크 유튜브 쇼츠 표지 심사. 이미지는 휴대폰 목록 크기(가로 168px) 비교판. 맨 왼쪽 "우리"가 발행 전 시안, "경쟁1~5"는 같은 주제(기준금리) 최근 30일 상위 쇼츠의 실제 썸네일.\n'
      '우리 제목: "기준금리 3%는 1999년 이후 어디쯤일까? 최고 5.25%, 최저는? #shorts". 제약: 숫자는 ECOS 원문, 과장·낚시·인물 없음.\n'
      '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 168px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 168px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
PC = open(os.path.join(V, 'judge_cafe.py'), encoding='utf-8').read()
def sc(t):
    m = re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)', t); return float(m.group(1)) if m else None
out = []; res = {}
jobs = [('v8 우리 비교판(쇼츠 168)', os.path.join(H, 'v8_board168.png'), PS), ('v7 비교판(참고)', os.path.join(H, 'v7_board168.png'), PS.replace('우리 제목', '우리 제목'))]
for name, p, q in jobs:
    for rep in (1, 2):
        t = ask(q, p); s = sc(t); res.setdefault(name, []).append(s); out.append(f'### {name} 회{rep} 점수 {s}\n{t}\n'); print(name, rep, s, flush=True)
# 교정칸: gongjae1002 (10/2 통과작, 카페판 질문)
sys.path.insert(0, V)
import importlib.util
try:
    ns = {}
    src = PC
    m = re.search(r"\nP\s*=\s*(\(.*?\)|'.*?'|\".*?\")\s*\n", src, re.S)
except Exception: m = None
GP = ('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
      '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 약점 · 고칠 것 2가지.')
for rep in (1, 2):
    t = ask(GP, os.path.join(V, 'board_gongjae1002.png')); s = sc(t); res.setdefault('교정 gongjae1002(기준 7.25)', []).append(s); out.append(f'### 교정 gongjae1002 회{rep} 점수 {s}\n{t}\n'); print('교정', rep, s, flush=True)
open(os.path.join(H, 'v8_judge_raw.md'), 'w', encoding='utf-8').write(f'[모델 {M} 고정]\n' + '\n'.join(out))
json.dump(res, open(os.path.join(H, 'v8_judge.json'), 'w'), ensure_ascii=False, indent=1)
