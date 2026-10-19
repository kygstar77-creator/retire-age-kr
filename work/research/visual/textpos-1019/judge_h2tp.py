# C-2 10/19 n1019 — 사장님 'N-2 thumb_A 꼴이 좋다·지금 것은 클로드 디자인 티' 뒤 새 2안(n1a·n1b)을 지금 공개판 f1d와 함께. C-2-thumb/judge.py 복사, 모델은 judge_1014.py처럼 3.1-flash-lite 하나 고정. 원래 설명: W-2-thumb/judge.py 복사, 경쟁 5는 C-2-thumb/compare.json(src/), 우리 최근 공개 P-1 p4e를 나란히(바탕 겹침 확인).
#   py -3.12 judge.py boards|blind|score w2a,w2b,w2c [접두어]   (JUDGE_MODEL 환경변수, 기본 gemini-3-flash-preview → 실패 시 3.1-flash-lite, 모델명은 결과 첫 줄)
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'H-2'); SRC = os.path.join(H, '..', 'H-2-thumb', 'src')
OURS = {k: (os.path.join(H, k + '.png') if k.startswith('h2tp') else os.path.join(EP, f'thumb_{k}.png')) for k in sys.argv[2].split(',')}
PREV = {'N-2': os.path.join(H, '..', '..', 'longform', 'ep', 'N-2', 'pilot', 'preview', 'thumb_A.png')}
COMP_IDS = ['bSrhZncUGD4', 'WzQebWiEi14', 'Us6f2rPmpr8', 'pqVRJi2YfIA', 'ATut9O9qpoU']
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
    t = '한국 부동산 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 h2f4"는 지금 예약된 판(큰 글 왼쪽 위), "우리 h2tp_a"는 같은 문구에 글자만 아래로 내린 후보(큰 두 줄 아래 40~45%, 작은 줄과 알약은 왼쪽 위), "우리 h2tp_c"는 h2tp_a와 같은 사진에 글자만 왼쪽 위, "우리 직전 편"(N-2)은 채널 주인이 좋다고 고른 다른 편, "경쟁"은 같은 주제(재건축 단지 값·대치·잠실) 상위작.\n영상: 서울 잠실·대치·반포 같은 넓이(84㎡)의 오래된 단지와 새 단지의 1년 실제 거래값 비교. 잠실주공5단지는 매매 중앙값 43억쯤으로 8곳 중 가장 비싼데 전세는 5억 남짓으로 가장 쌌다(국토교통부 실거래).\n제목(썸네일 옆에 같이 보임): "잠실주공5단지가 30년 늦게 지은 리센츠보다 비쌌다, 은마는 견주는 단지마다 갈렸다".\n시청자는 50~60대. 제약: 과장·낚시·권유 금지, 사실과 어긋난 말 금지. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가. 경제 지식 없는 58세가 1초에 뜻을 바로 아는가."\n시안마다(h2f4·h2tp_a2·h2tp_b): 첫 줄 "h2tp_a 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · AI 디자인 티(높음/중간/낮음) · 사실과 어긋나 보이는 말 · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n마지막 줄: "1위: h2tp_?"'
    out = ask(t, [os.path.join(H, PRE + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)

{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
