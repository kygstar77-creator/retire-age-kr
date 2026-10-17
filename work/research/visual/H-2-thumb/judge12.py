# H-2 12차 1초 시험·점수(judge.py 복사 — 질문만 12차 새 문구·시안 설명으로, 블라인드에 '어디 안에서' 질문 추가) — py -3.12 judge.py boards|blind|score h2a,h2b,... [접두어]
#   boards → s168/*.png, board168.png·board480.png(우리 시안 + 경쟁 5)   blind → gemini_blind.md   score → gemini_score.md
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'H-2')
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in sys.argv[2].split(',')}
COMP = {i: os.path.join(H, 'src', i + '.jpg') for i in 'bSrhZncUGD4 WzQebWiEi14 Us6f2rPmpr8 pqVRJi2YfIA ATut9O9qpoU'.split()}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
PRE = '' if len(sys.argv) < 4 else sys.argv[3]
TITLE = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))['title']


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
MODELS = [os.environ.get('JUDGE_MODEL', 'gemini-3.1-flash-lite'), 'gemini-3.5-flash-lite', 'gemini-3-flash-preview']


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
         '(주제 문장에 "가장 비싸고 가장 싼 건 어디 안에서인지"도 보이는 대로 넣으세요.) 추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, PRE + 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)


def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 h2?"가 공개 전 시안(h2t는 11차 최고안 대조 — 옛 문구, 좌우 두 칸·값 43억/5억 글자; h2v는 12차 최고안 대조 — 새 문구, 각 줄 끝에 막대 4개, 값 글자 없음), "경쟁"은 같은 주제(잠실주공5단지·은마·반포 아파트) 상위작. 새 문구: 앞줄 "잠실주공5단지, 잠실동 안에서" · 큰 두 줄 "살 땐 가장 비싸고 / 전세는 가장 쌌다" · 작은 줄 "국민평형 84㎡대 · 최근 1년 거래". 13차 h2x = h2v + 주황 막대 바로 위에 값 "43억"·"5억"(먹색), h2y = 같은 판, 값 주황·조금 크게, 5단지 막대 굵게. 비교판의 우리 시안 전부(대조 포함)를 빠짐없이 채점할 것.\n'
         f'영상 제목(썸네일 옆에 함께 보임): "{TITLE}". 썸네일은 제목과 같은 말을 반복하지 말고 보완해야 한다. 내용: 국토교통부 실거래 1년, 잠실동 84㎡대(거래 3건 이상 8단지) 중 '
         '1978년 지은 잠실주공5단지가 매매 가운데 값 43.45억으로 가장 비쌌고, 신규 순수전세 가운데 값은 5.20억으로 가장 쌌다(리센츠 매매 34.15억·전세 13.50억). 막대는 5단지(주황)와 2007~2008년 새 단지 3곳 리센츠·잠실엘스·트리지움(회색), 줄마다 0에서 시작. 사라·팔라·전망·재건축 해석 없음.\n'
         '제약: 인물·캐릭터·실사 사진 금지, 과장·낚시 금지, 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위 채널 썸네일 옆에 놓았을 때 같은 수준인가, 먼저 누르고 싶은가."\n'
         '시안마다: 첫 줄 "h2u 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · 후킹 장치(반전/질문/비교/내 돈 대입/없음) · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n'
         '마지막 줄: "1위: h2?"')
    out = ask(t, [os.path.join(H, PRE + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)


{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
