# 10/19 13시 사장님 "조회수 안 나오고 있는 영상들도 썸네일 바꿔 봐" — 공개 롱폼 저조 편 새 2안(r19a·r19b).
#   꼴은 C-2-thumb/n1019/make_n1019.py(= N-2 pilot thumb_A) 그대로: 꽉 찬 실사 1장 + 글자 3층(작은 흰 줄 1 · 큰 주황 질문 · 주황 알약 1).
#   머리띠·꼬리표·날짜 칸·둥근 카드·작은 글 여러 줄 없음. 오른쪽 아래(재생 시간 자리) 비움.
#   숫자 출처는 편마다 NUM 주석(facts/calc/screen_text 행). 6월 옛 편은 facts가 없어 영상 설명란에 이미 쓴 말·숫자만.
#   지난 시황 편(W-1 1·2화, G-1, E-1)은 '그 주'·'10월 초'·과거형으로 지나간 값임을 밝힌다.
#   py -3.12 make_r1019.py [편키 ...]  → ep/<편>/thumb_r19a.png, thumb_r19b.png (1280×720)
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
PH = os.path.join(H, 'photo'); FONT = os.path.join(WORK, 'fonts')
EPD = os.path.join(WORK, 'research', 'longform', 'ep')
W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE = (255, 90, 0), (255, 255, 255)


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(name, y_anchor=0.5, x_anchor=0.5, dark=1.0, zoom=1.0):
    im = Image.open(os.path.join(PH, name)).convert('RGB')
    r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor)
    im = im.crop((x, y, x + W, y + HH))
    return ImageEnhance.Brightness(im).enhance(dark) if dark != 1.0 else im


def shade_top(im, h, alpha=225):
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(h):
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, (h - y) / (h * 0.45))))
    return Image.composite(Image.new('RGB', im.size, (10, 11, 14)), im, m)


def fit(d, t, size, w, maxw=MAXW, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 4
    return size


def thumb(out, photo_name, white, orange, pill, y_anchor=0.5, x_anchor=0.5, dark=1.0, zoom=1.0, big=215):
    """white: 작은 흰 줄 1 · orange: 큰 주황 1~2줄(리스트) · pill: 주황 알약 1."""
    im = photo(photo_name, y_anchor, x_anchor, dark, zoom)
    d0 = ImageDraw.Draw(im)
    ws = fit(d0, white, 90, '700')
    bs = min(fit(d0, t, big, 'black') for t in orange)
    ps = fit(d0, pill, 64, '700', MAXW - 52)
    y_white = 40; y_big = y_white + ws + 30
    y_pill = y_big + len(orange) * int(bs * 1.12) + 40
    im = shade_top(im, min(900, y_pill + int(ps * 1.4) + 150))
    d = ImageDraw.Draw(im)
    d.text((X0, y_white), white, font=f(ws, '700'), fill=WHITE)
    for k, t in enumerate(orange):
        d.text((X0, y_big + k * int(bs * 1.12) - int(bs * 0.12)), t, font=f(bs, 'black'), fill=ORANGE, stroke_width=6, stroke_fill=(0, 0, 0))
    ft = f(ps, '700'); tw = d.textlength(pill, font=ft); ph = int(ps * 1.4)
    d.rounded_rectangle((X0, y_pill, X0 + tw + 52, y_pill + ph), 18, fill=ORANGE)
    d.text((X0 + 26, y_pill + ph // 2), pill, font=ft, fill=WHITE, anchor='lm')
    im.resize((1280, 720), Image.LANCZOS).save(out); print(out, f'흰{ws} 주황{bs} 알약{ps} 알약끝y{(y_pill + ph) * 2 // 3}')


# 편키: (ep 폴더, [(시안, 사진, 흰 줄, [주황], 알약, 옵션)])
EPS = {
    # W-1 1화 0yWQeW38UJE — NUM: W-1/facts.txt [C5] 주간 −5.07% · [C8] 100주 −1,400,000원 · [C9] 44.2배 · [A1] 107.4조(잠정). 지나간 주(10/2→10/8).
    'W-1': ('W-1', [
        ('r19a', 'w1a.jpg', '10월 초 사흘, 삼성전자 100주', ['얼마 빠졌을까?'], '평가액 −140만원 = 분기 배당 44번 치', dict(y_anchor=0.6)),
        ('r19b', 'w1b.jpg', '107조 실적 나온 그 주, 삼성전자', ['내 100주는?'], '사흘 새 평가액 140만원 줄었다', dict(y_anchor=0.5)),
    ]),
    # W-1 2화 AxTB7izIBUA — NUM: w1016/meta desc: 10/8 262,000 → 10/14 232,000원(−11.45%) · 100주 −300만원 · 자사주 평균 263,823원보다 12.06% 낮음 · 15조원(DART 20261012000421).
    'W-1-2': (os.path.join('W-1', 'w1016'), [
        ('r19a', 'w2a.jpg', '삼성전자가 15조원 들여 산 자기 주식', ['그 값 아래로?'], '10월 14일 종가, 회사가 산 평균값보다 12% 낮았다', dict()),
        ('r19b', 'w2b.jpg', '10월 중순 사흘, 삼성전자 100주', ['얼마 줄었을까?'], '평가액 −300만원, 회사가 산 값보다 12% 아래', dict(y_anchor=0.4)),
    ]),
    # G-1 xBTZtRp5lMs — NUM: G-1/screen_text 9·10행: 1월 꼭대기(2026-01-29) 1천만원 → 10/6 6,634,298원(663만원, −33.66%) · 495행 +50.7%.
    'G-1': ('G-1', [
        ('r19a', 'g1a.jpg', '금 1천만원어치, 올해 1월 꼭대기에 샀다면', ['얼마 남았을까?'], '10월 6일 값으로 663만원', dict(dark=0.95)),
        ('r19b', 'g1b.jpg', '올해 1월 꼭대기에 산 금 1천만원', ['본전까지 얼마?'], '1월 꼭대기 값까지 +50.7% 올라야 (10월 6일 기준)', dict()),
    ]),
    # P-1 vsL7mojDW7w — NUM: meta thumb_text: 5년 일찍 76.7세부터 · 1년 일찍 80.7세부터 · 1969년생(65세 수령) · 월 100만원 가정.
    'P-1': ('P-1', [
        ('r19a', 'p1a.jpg', '국민연금, 65세 대신 5년 일찍 받으면', ['몇 살부터 손해?'], '76.7세부터 제때 받은 쪽이 더 많아진다', dict(y_anchor=0.6)),
        ('r19b', 'p1b.jpg', '국민연금, 딱 1년만 일찍 받아도', ['몇 살부터 손해?'], '1년 일찍 받으면 80.7세부터 손해', dict(y_anchor=0.6)),
    ]),
    # M-1 eTjVs1vDTwg — NUM: M-1/calc_out 5·12행: 월 100만원(세금·건보료 뗀) 필요 원금 SCHD 4.85억 · JEPQ 1.38억.
    'M-1': ('M-1', [
        ('r19a', 'm1a.jpg', '세금·건보료 떼고 배당 매달 100만원', ['원금 얼마?'], 'SCHD로 받으려면 4억 8,500만원', dict()),
        ('r19b', 'm1b.jpg', '세금 떼고 배당 매달 100만원, 필요한 원금', ['JEPQ? SCHD?'], 'JEPQ 1억 3,800만원 · SCHD 4억 8,500만원', dict()),
    ]),
    # D-1 GMc2Rd1-JYA — NUM: D-1/facts 32~34행: 연 금융소득 1,000만원 월 22,800원 → 1,001만원 67,850원 · 연 540,600원 더(약 54만원) · 2.98배.
    'D-1': ('D-1', [
        ('r19a', 'd1a.jpg', '퇴직 후 배당·이자, 1년 1,000만원 넘으면', ['건보료 3배?'], '1만원 넘었을 뿐인데 1년 54만원 더', dict()),
        ('r19b', 'd1b.jpg', '퇴직 후 배당·이자 1,000만원과 1,001만원', ['건보료 차이는?'], '1만원 차이에 1년 54만원 더', dict()),
    ]),
    # E-1 idc3JZOZukc — NUM: E-1 desc: SK하이닉스 주가 1년 5.13배(+412.9%, 25.9.29→26.9.29) · 영업이익 6.57배(2026Q2 60.54조 vs 2025Q2 9.21조, facts 17·21행) · 1년 최대 낙폭 −54.7%.
    'E-1': ('E-1', [
        ('r19a', 'e1a.jpg', '9월 말까지 1년, SK하이닉스 주가 5배', ['이익도 5배?'], '2분기 영업이익은 1년 전의 6.6배', dict()),
        ('r19b', 'e1b.jpg', '1년 새 주가 5배 오른 SK하이닉스', ['반 토막 난 적도?'], '1년 중 가장 크게 빠진 폭 −54.7%', dict()),
    ]),
    # E-2 7eD6SLt_jKc — NUM: E-2 desc: 2026년 2분기 이자수익 4억 2,200만 달러 > 영업이익 3억 9,800만 달러 · 영업이익률 1.4%(10분기 최저) · 매출 282억 달러(10분기 최대).
    'E-2': ('E-2', [
        ('r19a', 'e2a.jpg', '테슬라 2분기 장부를 열어 보니', ['이자가 더 컸다?'], '이자수익 4.22억 달러 > 영업이익 3.98억 달러', dict()),
        ('r19b', 'e2b.jpg', '테슬라 2분기 매출은 10분기 중 최대', ['남은 이익은?'], '매출 100달러에 영업이익 1.4달러', dict()),
    ]),
    # 6월 옛 편 — facts 없음. 영상 설명란(10/19 Data API로 읽음)에 이미 쓴 말·숫자만.
    'J-gSK': ('june-gSKsQWjTabo', [  # 설명: '14억을 모아 조기은퇴에 성공한 파이어족이, 1년 만에 다시 회사로' · '돈이 부족해서가 아니었습니다'
        ('r19a', 'fa.jpg', '14억 모아 조기 은퇴한 사람이', ['1년 만에 출근?'], '돈이 모자라서가 아니었다', dict()),
        ('r19b', 'fb.jpg', '14억 모아 은퇴하고 1년 만에 회사로', ['왜 돌아왔나?'], '돈 때문이 아니었다', dict()),
    ]),
    'J-cxl': ('june-cxls2Ve18-k', [  # 설명: '배당금만으로 사는 삶' · '작은 돈을 오래 지킨 사람의 이야기' · "'6억의 함정'"
        ('r19a', 'da.jpg', '출근 없이 배당금만으로', ['살 수 있을까?'], "많은 사람이 놓치는 '6억의 함정'", dict()),
        ('r19b', 'db.jpg', '큰돈 아니라 작은 돈을 오래 지키면', ['배당으로 산다?'], '배당금만으로 사는 삶, 무엇부터', dict()),
    ]),
    'J-JVT': ('june-JVTYZ208hgw', [  # 설명: '4년 동안 … 거의 다 잃었습니다' · 'QQQM 하나만' · '5년 뒤엔 일을 그만둘 수 있다고'
        ('r19a', 'qa.jpg', '4년 투자로 거의 다 잃은 사람이', ['5년 뒤 은퇴?'], 'QQQM 하나만 모으는 이유', dict()),
        ('r19b', 'qb.jpg', '투자 재능 없는 사람이 5년 뒤 은퇴하려면', ['QQQM 하나로?'], '종목 고르기를 그만둔 이유', dict()),
    ]),
    'J-wwf': ('june-wwfFszPl06g', [  # 설명: 'QQQM 하나에 매달 꾸준히 넣고, 파이어하면 필요한 만큼만 팝니다'
        ('r19a', 'oa.jpg', '매달 QQQM 하나만 사 모으면', ['은퇴 될까?'], '은퇴 뒤엔 필요한 만큼만 판다', dict()),
        ('r19b', 'ob.jpg', '나스닥100 따라가는 ETF 딱 하나', ['QQQM 하나로?'], '이 방법의 빛과 그림자', dict()),
    ]),
    'J-zhT': ('june-zhTjJwy1mwQ', [  # 설명: 'QQQM으로 갈까요 아니면 배당의 SCHD로' · '실제 25년 데이터로 거치식·적립식 시뮬레이션'
        ('r19a', 'sa.jpg', '은퇴 자금, 어디에 모을까', ['QQQM? SCHD?'], '실제 25년 데이터로 돌려 본 결과', dict()),
        ('r19b', 'sb.jpg', '성장의 QQQM, 배당의 SCHD', ['누가 먼저 은퇴?'], '실제 25년 데이터로 모아 봤다', dict()),
    ]),
}

if __name__ == '__main__':
    keys = sys.argv[1:] or list(EPS)
    for k in keys:
        folder, vs = EPS[k]; os.makedirs(os.path.join(EPD, folder), exist_ok=True)
        for name, ph, wt, org, pill, opt in vs:
            thumb(os.path.join(EPD, folder, f'thumb_{name}.png'), ph, wt, org, pill, **opt)
