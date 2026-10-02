# 카페 대표사진 심사 — onesec-2026-10-02/judge_lite.py·judge_flash.py 방식(제미나이 REST), 비교판 board_<name>.png 한 장.
#   py -3.12 judge_cafe.py <name> [모델 ...]   기본: flash 계열 → lite 순서로 되는 것 하나씩 두 모델까지
import sys, os, json, base64, urllib.request, glob
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
def ask(m, text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
        data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
    return r['candidates'][0]['content']['parts'][0]['text']
name = sys.argv[1]; pkg = os.path.join(R, name, 'pkg')
title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
lead = open(os.path.join(pkg, 'c00.txt'), encoding='utf-8').read().strip()[:300]
P = ('네이버 카페 글 대표사진(목록·검색 썸네일) 심사. 이미지는 휴대폰 목록 크기(정사각형 110px) 비교판이다. 맨 왼쪽 "우리 새 표지"가 발행 전 시안, "경쟁"은 같은 검색어 네이버 카페 탭 상위 글의 실제 썸네일.\n'
     f'글 제목: "{title}"\n글 첫머리: {lead}\n'
     '제약: 숫자는 본문에 있는 것만, 과장·낚시 금지, 인물 사진 없음.\n'
     '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 110px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 110px에서 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 고칠 것 2가지.')
models = sys.argv[2:] or ['gemini-3.7-flash', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.1-flash-lite']
out = []
for m in models:
    try: out.append((m, ask(m, P, [os.path.join(H, f'board_{name}.png')])))
    except Exception as e: print(f'[{m} 실패 {e}]', file=sys.stderr); continue
    if len(out) >= 2: break
txt = '\n\n---\n'.join(f'[모델 {m}]\n{o}' for m, o in out)
open(os.path.join(H, f'gemini_{name}.md'), 'w', encoding='utf-8').write(txt); print(txt)
