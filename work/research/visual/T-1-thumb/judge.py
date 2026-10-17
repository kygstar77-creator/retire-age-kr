# T-1 1초 시험 + 비교판 점수 — C-2-thumb/judge.py 복사. 경쟁 5 = ep/T-1/compete.md 영상 id(src/), 우리 최근 공개 W-1 w1p·P-1 p4e를 나란히(바탕 겹침 확인).
#   py -3.12 judge.py boards|blind|score t1a,t1b,t1c [접두어]   (JUDGE_MODEL 환경변수, 기본 gemini-3-flash-preview → 실패 시 3.1-flash-lite, 모델명은 결과 첫 줄)
#   제목은 매 차수 meta.json title에서 다시 읽는다(교본 10/11 H-1).
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'T-1')
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in sys.argv[2].split(',')}
PREV = {'W-1': os.path.join(H, '..', '..', 'longform', 'ep', 'W-1', 'thumb_w1p.png'),
        'P-1': os.path.join(H, '..', '..', 'longform', 'ep', 'P-1', 'thumb_p4e.png')}
COMP_IDS = ['dvC8Ll7Y8CI', 'inCjCQl2sbA', 'RC2iAHQvJII', 'SLh90bWU7Tw', 'mS1qn5dYPxw']
COMP = {c: os.path.join(H, 'src', c + '.jpg') for c in COMP_IDS}
ALL = {**OURS, **PREV, **COMP}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
PRE = '' if len(sys.argv) < 4 else sys.argv[3]
TITLE = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))['title']


def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)


def boards():
    os.makedirs(os.path.join(H, 's168'), exist_ok=True)
    items = [(k, '우리 ' + k) for k in OURS] + [(k, '우리 직전 편 ' + k) for k in PREV] + [(k, '경쟁') for k in COMP]
    for W, name in ((168, 'board168.png'), (480, 'board480.png')):
        HH = round(W * 9 / 16); cols = 3 if W == 480 else 4; pad = 12; rows = (len(items) + cols - 1) // cols
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
        for n, (k, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            im = fit(ALL[k], W); bd.paste(im, (x, y))
            if W == 168: im.save(os.path.join(H, 's168', k + '.png'))
            d.text((x, y + HH + 4), lab, fill='black', font=F)
        bd.save(os.path.join(H, PRE + name)); print(PRE + name, bd.size)


KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = [os.environ.get('JUDGE_MODEL', 'gemini-3-flash-preview'), 'gemini-3.1-flash-lite']


def ask(text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return f'[모델 {m}]\n' + r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(f'[{m} 실패 {str(e)[:80]}]', file=sys.stderr)
    return '(전부 실패)'


def blind():
    keys = list(OURS) + list(PREV) + list(COMP); random.seed(int(os.environ.get('SEED', '10171'))); random.shuffle(keys)
    lab = {k: f'#{n + 1}' for n, k in enumerate(keys)}
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 세금: (이 썸네일대로면 내야 할 세금이 늘어나나/줄어드나/모름/해당 없음) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, PRE + 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)


def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 t1?"가 공개 전 시안, "우리 직전 편"은 다른 편(바탕색·짜임 겹침 확인용), "경쟁"은 같은 주제(1주택 양도세·장기보유특별공제 개편) 상위작.\n'
         '영상: 정부 세법 개정안(9월 1일 국무회의 의결, 국회 통과 전) 기준 계산. 8억에 사서 10년 가진 20억 집을 파는 가상 인물 둘. 그 집에 10년 산 사람은 2029년에 팔면 양도세 1,241만원, 2년만 산 사람은 1억 4,777만원(약 12배, 지방세 포함). '
         '2년만 산 사람은 양도차익에서 깎아 주는 장기보유특별공제율이 2027년 48% → 2028년 32% → 2029년 16%로 줄어 세금이 늘어난다(2027년 8,135만원 → 2029년 1억 4,777만원).\n'
         f'제목(썸네일 옆에 같이 보임): "{TITLE}". 큰 글은 카피라이터 확정 문구.\n'
         '시청자는 50~60대. 제약: 인물 사진 금지, 과장·낚시·권유 금지("폭탄" 등 금지), 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가. 경제 지식 없는 58세가 1초에 뜻을 바로 아는가."\n'
         '시안마다: 첫 줄 "t1? 점수: N"(1~10, 6=경쟁 평균, 8=통과) · 1초에 주제를 알 수 있나(예/아니오) · "양도세가 줄어든다(세금이 준다)"로 거꾸로 읽을 위험(높음/중간/낮음) · 사실과 어긋나 보이는 말 · 경쟁과 비슷한 점 개수 · 9점이 되려면 고칠 것 2가지.\n'
         '마지막 줄: "1위: t1?"')
    out = ask(t, [os.path.join(H, PRE + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)


{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
