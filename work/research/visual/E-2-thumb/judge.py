# E-2 1초 시험 + 비교판 점수(제미나이) — py -3.12 judge.py boards|blind|score
#   boards → s168/*.png, board168.png(우리 3 + 경쟁 5, 168px), board480.png(같은 8장, 480px)
#   blind  → gemini_blind.md (주제·제목 정보 없이 8장 섞어 한 문장씩)
#   score  → gemini_score.md (비교판 + 주제 공개, 1~10, 7=통과·8=목표)
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'E-2')
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in (sys.argv[2].split(',') if len(sys.argv) > 2 else ('e2a', 'e2b', 'e2c'))}
COMP = {c['id']: os.path.join(H, 'src', c['id'] + '.jpg') for c in json.load(open(os.path.join(H, 'compare.json'), encoding='utf-8')) if c['who'] == '경쟁'}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)

def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)

def boards():
    os.makedirs(os.path.join(H, 's168'), exist_ok=True)
    items = [(k, '우리 ' + k) for k in OURS] + [(k, '경쟁') for k in COMP]
    for W, name in ((168, 'board168.png'), (480, 'board480.png')):
        HH = round(W * 9 / 16); cols = 4; pad = 12; rows = 2
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
        for n, (k, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            im = fit({**OURS, **COMP}[k], W); bd.paste(im, (x, y))
            if W == 168: im.save(os.path.join(H, 's168', k + '.png'))
            d.text((x, y + HH + 4), lab, fill='black', font=F)
        bd.save(os.path.join(H, name if len(sys.argv) < 4 else sys.argv[3] + name)); print(name, bd.size)

KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']
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
    keys = list(OURS) + list(COMP); random.seed(21002); random.shuffle(keys)
    lab = {k: f'#{n + 1}' for n, k in enumerate(keys)}
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 8장 중 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)

def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 e2?"가 공개 전 시안, "경쟁"은 테슬라 주제 조회 상위작.\n'
         '영상: 테슬라 SEC 10-Q 장부 해설 — 2026년 2분기 매출 282억 달러(10분기 중 최대), 영업이익 3.98억 달러 < 이자수익 4.22억 달러, 영업이익률 1.4%(10분기 최저), 설비투자·신용 한도 300억 달러, 끝에 시청자 은퇴 나이 계산. 투자 권유 없음.\n'
         '제약: 인물·캐릭터·차 사진 금지, 과장·낚시 금지, 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈)이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가."\n'
         '시안마다: 첫 줄 "e2a 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · 후킹 장치(반전/질문/비교/내 돈 대입/없음) · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n마지막 줄: "1위: e2?"')
    out = ask(t, [os.path.join(H, ('' if len(sys.argv) < 4 else sys.argv[3]) + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, ('' if len(sys.argv) < 4 else sys.argv[3]) + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)

{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
