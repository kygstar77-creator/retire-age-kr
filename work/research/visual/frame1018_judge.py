# 10/18 visual — 고정 틀 시안 1초 시험·비교판 점수(제미나이). C-2-thumb/judge.py 줄임판.
#   py -3.12 frame1018_judge.py <C-2|H-4> <시안,시안> <경쟁 jpg 폴더> <비교판 출력 폴더> boards|blind|score
# 경쟁 썸네일은 저장소에 넣지 않는다(출력 폴더 = scratchpad). 결과 글만 <편>-thumb/judges.md에 옮긴다.
import sys, os, json, base64, urllib.request, random, glob
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
EPN, KEYS, SRC, OUT, CMD = sys.argv[1:6]
EP = os.path.join(H, '..', 'longform', 'ep', EPN)
OURS = {k: os.path.join(EP, f'thumb_{k}.png') for k in KEYS.split(',')}
# 우리 최근 고정 틀 견본(같은 틀끼리 구별되는지)
PREV = {'우리 다른 편(틀 견본)': os.path.join(H, '..', 'strategy', 'brand-1017', 'long_sonpum.png' if EPN in ('H-2', 'H-4') else 'long_naedon.png')}
COMP = {os.path.basename(p)[:-4]: p for p in sorted(glob.glob(os.path.join(SRC, '*.jpg')))}
ALL = {**OURS, **PREV, **COMP}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
os.makedirs(OUT, exist_ok=True)
TOPIC = {
    'C-2': '퇴직금 3억을 S&P500에 넣고 매달 200만원씩 꺼내 쓴 가상 두 사람 계산. 1998년 1월 시작한 사람은 2011년에 돈이 바닥(1년 치를 못 꺼냄), 5년 늦은 2003년 1월 시작한 사람은 2025년 말 2억 7천이 남음. 가른 건 시작한 해. 제목: "S&P500에 넣은 퇴직금 3억, 조금씩 팔아 생활비로 쓴 두 사람을 가른 건 시작한 해였다".',
    'H-4': '광명 아파트가 서울보다 비싸다는 말을 84㎡ 매매 실거래(2026년 7~9월)로 확인. 서울 25개 구 중 광명보다 싼 구가 8곳, 나머지 17곳은 광명보다 비쌈(광명은 비싼 순 18번째). 비싸다는 말은 2019년 뒤 지은 새 단지 이야기. 제목: "광명 아파트 서울보다 비싸다? 그 말은 2019년 뒤 지은 단지 이야기였다".',
    'H-2': '서울 잠실동 안에서 국민평형 84㎡대 최근 1년 거래로 보면, 1978년에 지은 잠실주공5단지가 매매는 가장 비싸고(중앙 43억) 전세는 가장 쌌다(5억 남짓). 제목은 30년 늦게 지은 리센츠와 견주는 이야기.',
    'T-1': '장기보유특별공제 정부안(국회 통과 전). 2029년에 같은 20억 집을 팔 때 10년 산 사람과 2년만 산 사람의 양도세가 약 12배 차이. 가진 햇수 말고 살았던 햇수로만 공제.',
    'X-1': '같은 S&P500 ETF를 원화 1억으로 산 날만 달리 계산. 작년 이맘때 산 1억은 원화 기준 +10%, 2024년 이후 달러가 가장 비싸던 7월 초에 산 1억은 −11%. 주가는 올랐지만 원화 계좌는 빠짐.',
}[EPN]


def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)


def boards():
    os.makedirs(os.path.join(OUT, 's168'), exist_ok=True)
    items = [(k, '우리 ' + k) for k in OURS] + [(k, k) for k in PREV] + [(k, '경쟁') for k in COMP]
    for W, name in ((168, 'board168.png'), (480, 'board480.png')):
        HH = round(W * 9 / 16); cols = 3; pad = 12; rows = (len(items) + cols - 1) // cols
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
        for n, (k, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            im = fit(ALL[k], W); bd.paste(im, (x, y))
            if W == 168: im.save(os.path.join(OUT, 's168', f'{n:02d}.png'))
            d.text((x, y + HH + 4), lab, fill='black', font=F)
        bd.save(os.path.join(OUT, name)); print(os.path.join(OUT, name))


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
    names = list(OURS) + list(PREV) + list(COMP)
    idx = list(range(len(names))); random.seed(1018); random.shuffle(idx)
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(idx)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름". 이미지 순서 = #1부터. 마지막 줄: 가장 먼저 누르고 싶은 것 #번호 하나.')
    out = ask(t, [os.path.join(OUT, 's168', f'{i:02d}.png') for i in idx])
    lab = {f'#{n + 1}': names[i] for n, i in enumerate(idx)}
    print(out); print(json.dumps(lab, ensure_ascii=False))


def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장 = 같은 비교판(1장째 휴대폰 목록 크기 168px, 2장째 480px). "우리 ..."가 공개 전 시안, "우리 다른 편(틀 견본)"은 채널 고정 틀의 다른 편, "경쟁"은 같은 주제 상위작.\n'
         f'영상: {TOPIC}\n시청자는 50~60대. 제약: 실존 인물 사진 금지, 과장·낚시·권유 금지, 오른쪽 아래 비움. 모방 금지: 경쟁과 비슷한 점이 2개 넘으면 감점.\n'
         '질문: "경쟁 상위작 옆에 놓았을 때 같은 수준 이상으로 보이고 먼저 누르고 싶은가. 경제 지식 없는 58세가 1초에 뜻을 바로 아는가."\n'
         '시안마다: 10점 만점 점수(소수 1자리) · 168px에서 1초에 읽은 뜻 한 문장 · 오독 위험 · 경쟁과 비슷한 점 개수 · 고칠 점 1개. 칭찬 말고 감점부터. 마지막 줄 "1위: 시안 이름".')
    print(ask(t, [os.path.join(OUT, 'board168.png'), os.path.join(OUT, 'board480.png')]))


{'boards': boards, 'blind': blind, 'score': score}[CMD]()
