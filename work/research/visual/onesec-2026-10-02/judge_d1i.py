# D-1 d1i 재심사(10/02 09:1x visual) — 168px 비교판(d1i·d1h + 경쟁 5) · 제미나이 블라인드(주제 맞힘) + 점수
#   py -3.12 judge_d1i.py board|blind|score
import sys, os, json, base64, urllib.request
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(H); EP = os.path.join(V, '..', 'longform', 'ep')
W = 168; HH = 95; T = sys.argv[2] if len(sys.argv) > 2 else 'd1i'
D1C = [c['id'] for c in json.load(open(os.path.join(V, 'D-1-thumb', 'compare.json'), encoding='utf-8')) if c['who'] == '경쟁'][:5]
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
def small(p):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, HH), Image.LANCZOS)
def board():
    items = [('우리 ' + T.upper(), os.path.join(EP, 'D-1', 'thumb_' + T + '.png'))] + [(f'경쟁 {k}', os.path.join(V, 'D-1-thumb', 'src', k + '.jpg')) for k in D1C]
    cols, pad = 3, 12; rows = 2
    bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
    for n, (lab, p) in enumerate(items):
        x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
        im = small(p); bd.paste(im, (x, y)); d.text((x, y + HH + 4), lab, fill='black', font=F)
        if n == 0: im.save(os.path.join(H, 's168', T.upper() + '.png'))
    bd.save(os.path.join(H, 'board4_' + T + '.png')); print(bd.size)
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash', 'gemini-3.1-flash-lite']
def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return f'[모델 {m}]\n' + r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(f'[{m} 실패 {e}]', file=sys.stderr)
    return '(전부 실패)'
def blind():
    out = ask('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 1장(실제 크기 가로 168px). 제목은 안 보인다고 가정. 1초만 봤다고 치고 정확히 한 줄:\n'
              '주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오', [os.path.join(H, 's168', T.upper() + '.png')])
    open(os.path.join(H, 'gemini_' + T + '_blind.md'), 'w', encoding='utf-8').write(out); print(out)
def score():
    out = ask('한국 재테크 유튜브 썸네일 심사. 이미지는 휴대폰 목록 크기(가로 168px) 비교판. "우리 ' + T.upper() + '"가 공개 전 시안, "경쟁"은 같은 주제 상위작.\n'
              '영상: 퇴직 후 지역가입자 건강보험료 — 배당·이자 연 1,000만원과 1,001만원 경계에서 월 건보료 22,800원→67,850원(2.98배), 1년 54만원 차이.\n'
              '제목: "퇴직 후 건강보험료, 배당·이자 1만원 차이에 1년 54만원?" (썸네일은 제목 반복 말고 보완)\n'
              '제약: 인물·캐릭터 금지, 과장·낚시 금지, 오른쪽 아래 비움, 경쟁 배치·색을 따라 하지 않음.\n'
              '답 형식: 첫 줄 "' + T.upper() + ' 점수: N"(1~10, 경쟁 상위작 옆에서 먼저 누르고 싶은가, 6=경쟁 평균, 7=통과) · 1초에 주제를 알 수 있나(예/아니오) · 후킹 장치 · 경쟁과 비슷해 보이는 점 수 · 7점 미만이면 고칠 것 2가지.',
              [os.path.join(H, 'board4_' + T + '.png')])
    open(os.path.join(H, 'gemini_' + T + '_score.md'), 'w', encoding='utf-8').write(out); print(out)
{'board': board, 'blind': blind, 'score': score}[sys.argv[1]]()
