# H-3 1초 시험(H-2 judge.py 틀, 주제·제목·경쟁만 H-3) — py -3.12 judge.py boards|blind|score h3a,h3b,... [접두어] ["점수 질문에 붙일 차수 설명"]
#   boards → s168/*.png, <접두어>board168.png·board480.png(우리 시안 + 경쟁 5)   blind → gemini_blind.md   score → gemini_score.md
import sys, os, json, base64, urllib.request, random, re
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'H-3')
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in sys.argv[2].split(',')}
COMP_IDS = 'QO-6aWpqVm4 4O6trzyjalI TPD-zw4TvG4 BAO0xDdBGVI y76t2BQ4O6s'.split()  # ep/H-3/compete.md 상위 5편
COMP = {i: os.path.join(H, 'src', i + '.jpg') for i in COMP_IDS}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
PRE = '' if len(sys.argv) < 4 else sys.argv[3]
NOTE = '' if len(sys.argv) < 5 else sys.argv[4]
TITLE = re.search(r'\*\*제목: ([^*]+)\*\*', open(os.path.join(EP, 'copy', 'titles.md'), encoding='utf-8').read()).group(1).strip()
assert TITLE.startswith('압구정현대아파트엔 30억 안팎에 팔린 집이 없었다'), TITLE


def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)


def boards():
    os.makedirs(os.path.join(H, 's168'), exist_ok=True)
    items = [(k, '우리 ' + k) for k in OURS] + [(k, '경쟁') for k in COMP]
    for W, name in ((168, 'board168.png'), (480, 'board480.png')):
        HH = round(W * 9 / 16); cols = 4; pad = 12; rows = (len(items) + cols - 1) // cols
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), '#0f0f0f'); d = ImageDraw.Draw(bd)
        for n, (k, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            im = fit({**OURS, **COMP}[k], W); bd.paste(im, (x, y))
            if W == 168: im.save(os.path.join(H, 's168', k + '.png'))
            d.text((x, y + HH + 4), lab, fill='white', font=F)
        bd.save(os.path.join(H, PRE + name)); print(PRE + name, bd.size)


KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = [os.environ.get('JUDGE_MODEL', 'gemini-3.1-flash-lite'), 'gemini-3.5-flash-lite', 'gemini-3-flash-preview', 'gemini-2.5-flash']


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
    keys = list(OURS) + list(COMP); random.seed(10171); random.shuffle(keys)
    lab = {k: f'#{n + 1}' for n, k in enumerate(keys)}
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, PRE + 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)


def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 h3?"가 공개 전 시안, "경쟁"은 같은 주제(목동신시가지·압구정·잠실 장미 아파트) 상위작. ' + NOTE + '\n'
         f'영상 제목(썸네일 옆에 함께 보임): "{TITLE}". 썸네일은 제목과 같은 말을 반복하지 말고 보완해야 한다. 내용: 국토교통부 아파트 매매 실거래 최근 1년(2025.11~2026.10 계약) 중 30억 안팎(27~33억) 거래의 전용면적 가운데 값 — '
         '신천동 175건 85㎡ · 목동신시가지 1~7단지 67건 96㎡ · 압구정동 0건(가장 싼 거래가 한양1차 35.70억). 평면 그림(있는 판)은 넓이에 비례(변 길이 = √넓이)해 두 집을 겹친 것, 줄자(있는 판)는 0부터 100㎡. 사라·팔라·전망·재건축 해석 없음.\n'
         '제약: 인물·캐릭터·실사 사진 금지, 과장·낚시 금지, 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가."\n'
         '시안마다: 첫 줄 "h3a 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · 후킹 장치(반전/질문/비교/내 돈 대입/없음) · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n'
         '마지막 줄: "1위: h3?"')
    out = ask(t, [os.path.join(H, PRE + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)


{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
