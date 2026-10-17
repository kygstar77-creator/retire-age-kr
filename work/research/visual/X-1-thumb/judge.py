# X-1 1초 시험·점수(H-2 judge.py 구조, 주제·제목·경쟁만 X-1) — py -3.12 judge.py boards|blind|score x1a,x1b,... [접두어]
#   boards → s168/*.png, <접두어>board168.png·board480.png(우리 시안 + 경쟁 5)   blind → gemini_blind.md   score → gemini_score.md
#   경쟁 5 = compete_thumb.json(Data API 최근 30일 조회순, 주제 낱말 걸러 냄) 중 환율·미국주식/S&P500 주제 상위 5(커버드콜·시황 생중계 뺌)
import sys, os, json, base64, urllib.request, random, re
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'X-1')
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in sys.argv[2].split(',')}
COMP_IDS = '9sprlBRpDn8 jwEwdEUq0_Y L95ue7e0E_0 UcHK1WoTPtY f6MAA2GhsEk'.split()
COMP = {i: os.path.join(H, 'src', i + '.jpg') for i in COMP_IDS}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
PRE = '' if len(sys.argv) < 4 else sys.argv[3]
TITLE = re.search(r'title 1위: \*\*([^*]+)\*\*', open(os.path.join(EP, 'copy', 'titles.md'), encoding='utf-8').read()).group(1)


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
    keys = list(OURS) + list(COMP); random.seed(int(os.environ.get('SEED', '10171'))); random.shuffle(keys)
    lab = {k: f'#{n + 1}' for n, k in enumerate(keys)}
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오 | +10%(또는 주가 +4%)가 언제 산 것인지: (읽히면 그 말, 숫자 없는 장이나 안 읽히면 "모름")\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, PRE + 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out); print(lab)


NOTE = os.environ.get('JUDGE_NOTE', '')


def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 x1?"가 공개 전 시안, "경쟁"은 같은 주제(환율 하락·미국 주식/S&P500 환차손) 최근 30일 조회 상위작. ' + NOTE + '\n'
         f'영상 제목(썸네일 옆에 함께 보임): "{TITLE}". 썸네일은 제목과 같은 말을 반복하지 말고 보완해야 한다. 내용: 한국은행 환율·SPY 가격으로 1억원을 달러로 바꿔 SPY를 산 날 4개를 계산. '
         '2025-10-13(작년 이맘때)에 산 1억은 2026-10-15 원화로 +9.69%(반올림 +10%), 환율이 2024년 이후 가장 높던 2026-07-02(1,554.4원)에 산 1억은 SPY 달러 +3.63%(반올림 +4%)인데 원화로 −10.76%(반올림 −11%). '
         '같은 S&P500이라도 산 날 환율에 따라 원화 결과가 갈림(주가 몫도 있음). 사라·팔라·전망 없음. x1a·x1b·x1d·x1f 문구=\'같은 S&P500 / +10% vs −11%\' + 작은 줄 \'작년 이맘때 산 1억 vs 7월 초 산 1억 · 원화로 따지면\', x1c·x1e·x1g 문구=\'주가는 +4% / 내 1억은 −11%\' + \'2024년 이후 달러가 가장 비싸던 7월 2일에 산 경우\'(1칸=1천만원 10칸).\n'
         '제약: 인물·캐릭터·실사 사진 금지, 빨간 경고·과장·낚시 금지, 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점(배치·색·글씨 꾸밈·말투)이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고, 먼저 누르고 싶은가."\n'
         '시안마다: 첫 줄 "x1a 점수: N"(1~10, 6=경쟁 평균, 7=통과, 8=목표) · 1초에 주제를 알 수 있나(예/아니오) · 168px에서 \'작년 이맘때 산\'·\'7월 초 산\'이 읽히나 · 후킹 장치 · 경쟁과 비슷한 점 개수 · 8점이 되려면 고칠 것 2가지.\n'
         '마지막 줄: "1위: x1?"')
    BP = os.environ.get('BOARD', PRE)
    out = ask(t, [os.path.join(H, BP + n) for n in ('board168.png', 'board480.png')])
    open(os.path.join(H, PRE + 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)


{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
