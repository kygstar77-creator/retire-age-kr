# rate30_b(B형 cards) 첫 프레임 1초 시험(10/7 03:1x) — onesec_first.py 복사, 내용 설명만 B형으로
# rate30 첫 프레임 1초 시험(10/6 23:1x, 표지 폐지 뒤) — onesec_short.py 복사·문구만 바꿈
# rate30 표지 1초 시험 — a1_1eok1y onesec_short.py 복사(경쟁 5·제목·내용만 바꿈), firemap-shorts 10/05 01:5x
# 쇼츠 표지 1초 시험(firemap-shorts 10/02 19:3x): 쇼츠 목록 칸 크기(가로 168px 세로형)로 줄여 경쟁 5장과 비교판 → 제미나이 블라인드·점수.
import sys, os, json, base64, urllib.request, random
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite']
COMP = ['uiOfGZb2u48','29YBkaCAhU0','nWMnf1Mcu-w','1ysWp3l97L0','9B7rYYgB7Ok']  # rate30 compete.md 1~5위
W, HH = 168, 299
def small(im):
    im = im.convert('RGB'); w, h = im.size; t = round(h * 9 / 16)
    if t < w: im = im.crop(((w - t) // 2, 0, (w - t) // 2 + t, h))
    return im.resize((W, HH), Image.LANCZOS)
def fetch():
    for v in COMP:
        p = os.path.join(H, v + '.jpg')
        if not os.path.exists(p):
            for q in ('oardefault', 'hqdefault'):
                try: open(p, 'wb').write(urllib.request.urlopen(f'https://i.ytimg.com/vi/{v}/{q}.jpg', timeout=30).read()); break
                except Exception as e: print(v, q, e)
    tiles = [('우리', small(Image.open(os.path.join(H, '..', os.environ.get('COVER', 'cover.png')))))] + [('경쟁' + str(i + 1), small(Image.open(os.path.join(H, v + '.jpg')))) for i, v in enumerate(COMP)]
    for n, (_, im) in enumerate(tiles): im.save(os.path.join(H, f't{n}.png'))
    F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
    b = Image.new('RGB', (len(tiles) * (W + 8) + 8, HH + 30), 'white'); d = ImageDraw.Draw(b)
    for n, (lab, im) in enumerate(tiles): b.paste(im, (8 + n * (W + 8), 26)); d.text((8 + n * (W + 8), 5), lab, fill='black', font=F)
    b.save(os.path.join(H, os.environ.get('R','')+'board168.png'))
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
    ks = list(range(6)); random.seed(1002); random.shuffle(ks)
    t = ('휴대폰 유튜브 쇼츠 목록에서 스쳐 보는 표지 6장입니다(실제 크기 가로 168px). 제목은 안 보인다고 가정하세요. 장마다 1초만 봤다고 치고 정확히 이 형식 한 줄:\n'
         '#번호 | 주제: (한 문장) | 궁금증: (왜 누르나 한 문장, 없으면 "없음") | 글자 읽힘: 예/일부/아니오\n추측이 안 되면 "모름". 이미지 순서 = #1부터.')
    out = ask(t, [os.path.join(H, f't{k}.png') for k in ks])
    out += '\n\n번호표(#n → t번호, t0=우리): ' + json.dumps({f'#{i+1}': f't{k}' for i, k in enumerate(ks)})
    open(os.path.join(H, os.environ.get('R','')+'gemini_blind.md'), 'w', encoding='utf-8').write(out); print(out)
def score():
    t = ('한국 재테크 유튜브 쇼츠 표지 심사입니다. 비교판은 휴대폰 목록 크기(가로 168px). "우리"가 공개 전 시안, "경쟁1~5"는 같은 주제(기준금리) 최근 30일 상위작.\
'
         '우리 쇼츠 제목: "기준금리 3%는 1999년 이후 어디쯤일까? 최고 5.25%, 최저 0.5% #shorts". 설명 첫 줄: "한국은행 기준금리는 2026년 8월부터 3%예요. ECOS 월별 값(1999년 5월~)에서 가장 높았던 값은 5.25%(2000년 10월·2008년 8월), 가장 낮았던 값은 0.5%(2020년 5월)였어요." 내용: 한국은행 ECOS 기준금리 월별 조회 2026-10-06, 최고 5.25% · 지금 3% · 최저 0.5%. 표지 없이 첫 프레임부터 이 카드(첫 장: 지금 3% 계기판, 막대가 최고 5.25%·최저 0.5%로 바뀜) → 둘째 장 최고·최저·지금 → 셋째 장 언제였나, 합 25초.\
'
         '제약: 인물 금지, 과장·낚시 금지, 숫자는 ECOS 원문 그대로, 전망·매수 권유 금지, 높다/낮다 평가 말 금지.\
'
         '형식: 첫 줄 "우리 점수: N"(1~10, 경쟁 옆에서 먼저 누르고 싶은가, 6=경쟁 평균, 7=통과) · 1초에 주제 알 수 있나(예/아니오) · 후킹 장치(반전/질문/비교/내 돈 대입/없음) · 경쟁과 비슷해 보이는 점 개수 · 고칠 것 2가지.\
'
         '이어서 카피 심사: "카피 점수: N"(1~10, 제목·설명 첫 줄·표지 문구를 ①1초 주제 ②궁금증 장치 ③낚시 아님 ④경쟁 제목 틀 반복 아님 ⑤검색어 앞 다섯 기준으로) + 항목별 한 줄.')
    out = ask(t, [os.path.join(H, os.environ.get('R','')+'board168.png')])
    open(os.path.join(H, os.environ.get('R','')+'gemini_score.md'), 'w', encoding='utf-8').write(out); print(out)
{'fetch': fetch, 'blind': blind, 'score': score}[sys.argv[1]]()
