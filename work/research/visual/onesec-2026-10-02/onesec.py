# 1초 시험(사장님 10/02 06:17): 휴대폰 목록 크기(가로 168px)로 줄인 썸네일만 보고, 주제를 모르는 심사위원이
# '무슨 내용·왜 누르나'를 한 문장으로 적는다. + 경쟁 상위 5장 옆 비교판 점수(8점 통과).
#   py -3.12 onesec.py boards   → s168/*.png, board_D-1.png, board_E-1.png
#   py -3.12 onesec.py blind    → gemini_blind.md (주제 정보 없이)
#   py -3.12 onesec.py score    → gemini_score.md (비교판 + 주제 공개, 1~10)
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(H); EP = os.path.join(V, '..', 'longform', 'ep')
W = 168; HH = round(W * 9 / 16)
OURS = {  # 공개 전 후보
    'D1d': os.path.join(EP, 'D-1', 'thumb_d1d.png'), 'D1c': os.path.join(EP, 'D-1', 'thumb_d1c.png'),
    'E1c': os.path.join(EP, 'E-1', 'thumb_e1c.png'), 'E1a': os.path.join(EP, 'E-1', 'thumb_e1a.png'),
    'D1e': os.path.join(EP, 'D-1', 'thumb_d1e.png'), 'D1f': os.path.join(EP, 'D-1', 'thumb_d1f.png'),
    'E1d': os.path.join(EP, 'E-1', 'thumb_e1d.png'), 'E1e': os.path.join(EP, 'E-1', 'thumb_e1e.png')}
PUB = {i['id']: os.path.join(H, 'pub', i['id'] + '.jpg') for i in json.load(open(os.path.join(H, 'pub.json'), encoding='utf-8')) if not i['title'].startswith('(oembed')}
D1C = [c['id'] for c in json.load(open(os.path.join(V, 'D-1-thumb', 'compare.json'), encoding='utf-8')) if c['who'] == '경쟁'][:5]
E1C = ['wu8GBMPD_xk', '-Yh53SjCAiw', 'tVaz2qoAySM', 'gJTto7SP8w0', 'cBFFyqiKFRs']
COMP = {**{k: os.path.join(V, 'D-1-thumb', 'src', k + '.jpg') for k in D1C}, **{k: os.path.join(V, 'E-1-thumb', 'bench', k + '.jpg') for k in E1C}}
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)

def small(p):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)  # 4:3 hqdefault는 가운데 16:9로
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, HH), Image.LANCZOS)

def boards():
    os.makedirs(os.path.join(H, 's168'), exist_ok=True)
    for k, p in {**OURS, **PUB, **COMP}.items(): small(p).save(os.path.join(H, 's168', k + '.png'))
    for ep, ours, comps in (('D-1', ['D1d', 'D1c', 'D1e', 'D1f'], D1C), ('E-1', ['E1c', 'E1a', 'E1d', 'E1e'], E1C)):
        items = [(k, '우리 ' + k) for k in ours] + [(k, '경쟁') for k in comps]
        cols = 4; rows = (len(items) + cols - 1) // cols; pad = 12
        bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
        for n, (k, lab) in enumerate(items):
            x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30)
            bd.paste(Image.open(os.path.join(H, 's168', k + '.png')), (x, y)); d.text((x, y + HH + 4), f'{lab} {k if lab=="경쟁" else ""}', fill='black', font=F)
        bd.save(os.path.join(H, f'board_{ep}.png')); print('board', ep, bd.size)

KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest', 'gemini-2.5-flash-lite']
def ask(text, paths):
    parts = [{'text': text}]
    for p in paths: parts.append({'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}})
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return f'[모델 {m}]\n' + r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: print(f'[{m} 실패 {e}]', file=sys.stderr)
    return '(전부 실패)'

def blind():
    keys = list(OURS) + list(PUB); random.seed(1002); random.shuffle(keys)
    lab = {k: f'#{n+1}' for n, k in enumerate(keys)}
    json.dump(lab, open(os.path.join(H, 'blind_key.json'), 'w'), indent=1)
    t = ('휴대폰 유튜브 목록에서 스쳐 보는 썸네일 ' + str(len(keys)) + '장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. '
         '각 장을 1초만 봤다고 치고, 장마다 정확히 이 형식 한 줄:\n#번호 | 주제: (무슨 내용인지 한 문장) | 궁금증: (왜 눌러야 하는지 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n'
         '추측이 안 되면 주제에 "모름"이라 쓰세요. 이미지 순서 = #1부터.')
    out = ask(t, [os.path.join(H, 's168', k + '.png') for k in keys])
    open(os.path.join(H, 'gemini_blind.md'), 'w', encoding='utf-8').write(out + '\n\n번호표: ' + json.dumps(lab, ensure_ascii=False)); print(out)

def score():
    t = ('한국 재테크 유튜브 썸네일 심사입니다. 이미지 2장은 휴대폰 목록 크기(가로 168px) 비교판입니다. "우리"라고 적힌 것이 공개 전 시안, "경쟁"은 같은 주제 상위작.\n'
         '판1(D-1): 퇴직 후 지역가입자 건강보험료 — 배당·이자 연 1,000만원과 1,001만원 경계에서 건보료 1년 54만원 차이.\n'
         '판2(E-1): 제목 "삼성전자 이익 19배, 주가는 3배… SK하이닉스·마이크론은?" — SK하이닉스 1년 +412.9%·최대 낙폭 −54.7%, 삼성전자 영업이익 19배(1년 전 같은 분기)·주가 3.27배. 썸네일은 제목을 반복하지 말고 보완해야 함.\n'
         '판1 제목: "퇴직 후 건강보험료, 배당·이자 1만원 차이에 1년 54만원?"\n'
         '제약: 인물·캐릭터 금지, 과장·낚시 금지, 오른쪽 아래 비움.\n'
         '시안(D1d, D1c, D1e, D1f, E1c, E1a, E1d, E1e)마다: 첫 줄 "D1d 점수: N"(1~10, 경쟁 상위작 옆에서 먼저 누르고 싶은가, 6=경쟁 평균, 8=통과) · '
         '1초에 주제를 알 수 있나(예/아니오) · 후킹 장치(반전/질문/비교/내 돈 대입/없음) · 8점이 되려면 고칠 것 2가지(글자 3~6단어, 숫자 1개 크게).')
    out = ask(t, [os.path.join(H, 'board_D-1.png'), os.path.join(H, 'board_E-1.png')])
    open(os.path.join(H, 'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)

{'boards': boards, 'blind': blind, 'score': score}[sys.argv[1]]()
