# 10/19 visual — 고정 틀 썸네일 1초 시험·점수(제미나이). H-2·T-1 공용. py -3.12 judge1019.py <편> <시안,...> <접두어> boards|blind|score
#   boards → <편>-thumb/<접두어>board168.png·board480.png(우리 + 경쟁 5, src/*.jpg)  blind·score → <접두어>gemini_*.md
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EPN, KEYS, PRE, MODE = sys.argv[1], sys.argv[2].split(','), sys.argv[3], sys.argv[4]
H = os.path.join(HERE, f'{EPN}-thumb'); EP = os.path.join(HERE, '..', 'longform', 'ep', EPN)
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in KEYS}
COMP = {f[:-4]: os.path.join(H, 'src', f) for f in sorted(os.listdir(os.path.join(H, 'src')))[:5]}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
META = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))


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
        bd.save(os.path.join(H, PRE + name)); print(os.path.join(H, PRE + name))


KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = [os.environ.get('JUDGE_MODEL', 'gemini-3-flash-preview'), 'gemini-3.1-flash-lite', 'gemini-3.5-flash-lite']


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
    keys = list(OURS) + list(COMP); random.seed(1019); random.shuffle(keys)
    lab = {k: f'#{n + 1}' for n, k in enumerate(keys)}
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, PRE + 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)


def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 …"가 공개 전 시안, "경쟁"은 같은 주제 상위작. '
         f'영상 제목: "{META.get("title", "")}". 우리 시안 전부를 빠짐없이 채점하세요. 시안마다:\n'
         '- 점수 0~10 (질문: 경쟁 상위작 옆에 놓았을 때 같은 수준으로 보이나, 168px에서 1초에 주제와 누를 이유가 읽히나)\n- 168px 1초 한 문장 뜻\n- 오독 위험(있으면 어떻게 잘못 읽히나)\n- 경쟁과 비슷한 점 개수\n- 8점이 되려면 고칠 것 1개\n'
         '맨 끝에 "1위: <시안>" 한 줄.')
    out = ask(t, [os.path.join(H, PRE + 'board168.png'), os.path.join(H, PRE + 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)


{'boards': boards, 'blind': blind, 'score': score}[MODE]()
