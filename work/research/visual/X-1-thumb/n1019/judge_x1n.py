# X-1 10/19 n1019 — 새 썸네일 꼴(N-2 thumb_A + 큰 글 아래 40~45%) 3안 x1n_a·b·c를 지금 meta 판 x1f와 함께. C-2-thumb/n1019/judge_n1019.py 복사(judge_1014 방식, 3.1-flash-lite 하나 고정). 경쟁 5 = X-1-thumb/compete_thumb.json 상위 중 최근 30일(10/19 기준).
#   py -3.12 judge.py boards|blind|score w2a,w2b,w2c [접두어]   (JUDGE_MODEL 환경변수, 기본 gemini-3-flash-preview → 실패 시 3.1-flash-lite, 모델명은 결과 첫 줄)
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', '..', 'longform', 'ep', 'X-1'); SRC = os.path.join(H, '..', 'src')
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in sys.argv[2].split(',')}
PREV = {'N-2': os.path.join(EP, '..', 'N-2', 'pilot', 'preview', 'thumb_A.png')}
COMP_IDS = ['9sprlBRpDn8', 'jwEwdEUq0_Y', 'L95ue7e0E_0', 'GbM_AXlbJt0', 'UcHK1WoTPtY']
COMP = {c: os.path.join(SRC, c + '.jpg') for c in COMP_IDS}
ALL = {**OURS, **PREV, **COMP}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
PRE = '' if len(sys.argv) < 4 else sys.argv[3]

def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)

def boards():
    os.makedirs(os.path.join(H, 's168'), exist_ok=True)
    items = [(k, '우리 ' + k) for k in OURS] + [(k, '우리 직전 편') for k in PREV] + [(k, '경쟁') for k in COMP]
    for W, name in ((168, 'board168.png'), (480, 'board480.png')):
        HH = round(W * 9 / 16); cols = 3; pad = 12; rows = (len(items) + cols - 1) // cols
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
        for n, (k, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            im = fit(ALL[k], W); bd.paste(im, (x, y))
            if W == 168: im.save(os.path.join(H, 's168', k + '.png'))
            d.text((x, y + HH + 4), lab, fill='black', font=F)
        bd.save(os.path.join(H, PRE + name)); print(PRE + name, bd.size)

KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = [os.environ.get('JUDGE_MODEL', 'gemini-3.1-flash-lite')]  # judge-drift-1006: 모델 하나만

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
    keys = list(OURS) + list(PREV) + list(COMP); random.seed(int(os.environ.get('SEED','10152'))); random.shuffle(keys)
    lab = {k: f'#{n + 1}' for n, k in enumerate(keys)}
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, PRE + 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)

def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 x1f"는 지금 정해 둔 판(옛 꼴), "우리 x1n_a·x1n_b·x1n_c"는 바꿀 후보, "우리 직전 편"(N-2)은 채널 주인이 좋다고 고른 다른 편 썸네일(같은 꼴인지 보는 기준), "경쟁"은 같은 주제(환율·미국 ETF) 최근 30일 상위작.\n'
         '영상: 원화 1억을 달러로 바꿔 S&P500 ETF(SPY)를 산 날 네 개를 비교한 계산(2026년 10월 15일까지, 원화 기준). 2025년 10월 13일에 산 1억은 원화로 +9.69%(약 1억 970만원), 달러가 가장 비싸던 2026년 7월 2일에 산 1억은 주가가 +3.63% 올랐는데도 환율이 13.88% 내려 원화로 −10.76%(약 8,924만원). 같은 상품, 가른 건 산 날.\n'
         '제목(썸네일 옆에 같이 보임): "환율이 내린 석 달, 미국 ETF는 올랐는데 원화 계좌는 빠졌다 — 1억을 달러로 바꾼 날 네 개로 계산".\n'
         '시청자는 50~60대. 제약: 얼굴 정면 사진 금지(손은 됨), 과장·낚시·권유 금지. 채널 주인 평: 옛 꼴(위 머리띠·작은 글 여러 줄·카드)은 "AI가 만든 디자인 티가 난다", N-2는 꽉 찬 사진+큰 주황 글자라 좋다. 잘되는 채널 공통 틀(큰 글 아래 두 줄)은 따라 해도 됨, 한 채널 겉모습 통째 베끼기만 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가. 경제 지식 없는 58세가 1초에 뜻을 바로 아는가."\n'
         '시안마다(x1f·x1n_a·x1n_b·x1n_c): 첫 줄 "x1n_a 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · AI 디자인 티(높음/중간/낮음) · "+10%·−11%"를 그 달 주가 등락(산 날 기준 수익이 아님)으로 잘못 읽을 위험(높음/중간/낮음) · 사실과 어긋나 보이는 말 · 8점이 되려면 고칠 것 2가지.\n'
         '마지막 줄: "1위: x1n_?"')
    out = ask(t, [os.path.join(H, PRE + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)

{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
