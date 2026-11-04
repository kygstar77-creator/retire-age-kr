"""N-3 실사 11줄 교체 — visual-designer 2026-11-04 09시.
11/4 07시 새 심사관 2명(judge1_a·b)이 '못함'이라 한 Pexels 실사 11줄(r01·05·09·13·15·20·26·30·35·39·41)을 고친다.
심사관 지적: 대본 뜻 안 전함·외국 서식/간판/영문 UI·검은 띠·구상과 다름 → P-3(p3fix1103.py)처럼 바꾼다.
- 10줄: 종이 판. P-3 때 '9줄이 같은 종이 판(반복 티)' 흠이 남아서 꼴을 나눈다 —
  한글 급여명세서 서식(r01·05·13) · 빈 칸 미리 보기(r09 사다리 머리·r15 폭포 빈 틀) · 댓글/질문 메모(r20·26·35) · 큰 숫자(r30) · 계산식(r39)
- r41: 같은 노을 창 실사의 검은 띠를 잘라 꽉 채우고 위에 끝인사 한 줄(아래는 최종 화면 자리로 비움)
글자는 say_v1.txt 말 그대로. 숫자는 calc_out.txt 값만(A 5천 줄·D·I).
사용: py -3.12 n3fix1104.py [이름 ...] → work/video/public/bg/n3/board/·over/
"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import W, H, INK, GREY, OR, KRAFT_L, FADE, F_B, F_M, F_X, font, canvas, T, title, source, torn, hand_ellipse, hand_under, hand_arrow, hand_check
from PIL import Image, ImageDraw

PUB = os.path.join(K.WORK, 'video', 'public', 'bg', 'n3')
FF = os.path.join(K.WORK, 'video', 'node_modules', '@remotion', 'compositor-win32-x64-msvc', 'ffmpeg.exe')
MEMO = (246, 236, 178); PALE = (250, 248, 242); PAPER_N = (238, 230, 212); LINE = (170, 162, 150)
COND = '1인 · 식대 비과세 월 20만원 · 2026년 보험료율·간이세액표'
def wd(s, size, f=F_X): return font(f, size).getlength(s)

# ---------- 한글 급여명세서(자체 그림, 연봉 5천 · calc_out A 5천 줄) ----------
PAY = (('기본급 등', '3,966,666'), ('식대(비과세)', '200,000'))
DED = (('소득세', '190,620'), ('지방소득세', '19,060'), ('국민연금', '188,380'), ('건강보험', '142,600'),
       ('장기요양', '18,730'), ('고용보험', '35,690'))
def payslip(im, x0, y0, x1, seed, hi_net=False, blur_rows=False):
    torn(im, (x0, y0, x1, y0 + 760), PALE, seed=seed); d = ImageDraw.Draw(im)
    cx = (x0 + x1) // 2
    T(d, (cx, y0 + 62), '급 여 명 세 서', 50, INK, F_X)
    d.line([(x0 + 40, y0 + 108), (x1 - 40, y0 + 108)], fill=INK, width=3)
    mid = cx; T(d, ((x0 + mid) // 2, y0 + 146), '지급', 36, GREY, F_B); T(d, ((mid + x1) // 2, y0 + 146), '공제', 36, GREY, F_B)
    d.line([(mid, y0 + 120), (mid, y0 + 560)], fill=LINE, width=2)
    col = FADE if blur_rows else INK
    for i, (a, v) in enumerate(PAY):
        y = y0 + 210 + i * 62; T(d, (x0 + 40, y), a, 30, col, F_M, 'lm'); T(d, (mid - 24, y), v, 30, col, F_B, 'rm')
    for i, (a, v) in enumerate(DED):
        y = y0 + 210 + i * 62; T(d, (mid + 24, y), a, 30, col, F_M, 'lm'); T(d, (x1 - 40, y), v, 30, col, F_B, 'rm')
    y = y0 + 210 + 3 * 62; d.line([(x0 + 30, y - 34), (mid - 14, y - 34)], fill=LINE, width=2)
    T(d, (x0 + 40, y), '지급 합계', 30, col, F_B, 'lm'); T(d, (mid - 24, y), '4,166,666', 30, col, F_X, 'rm')
    d.line([(x0 + 40, y0 + 580), (x1 - 40, y0 + 580)], fill=INK, width=3)
    T(d, (x0 + 50, y0 + 660), '실지급액', 46, INK, F_X, 'lm')
    T(d, (x1 - 50, y0 + 660), '3,571,586원', 50, OR if hi_net else INK, F_X, 'rm')
    if hi_net: hand_ellipse(d, (x0 + 4, y0 + 592, x1 - 4, y0 + 730), seed=seed + 1)
    return d

B = {}
def board(fn): B[fn.__name__] = fn; return fn

@board
def n3_open(im):   # r01 '안녕하세요, 파이어맵입니다. 오늘은 연봉 실수령액 이야기입니다.'
    d = payslip(im, 980, 170, 1760, seed=401, blur_rows=True)
    T(d, (520, 330), '파이어맵', 58, GREY, F_B)
    T(d, (520, 480), '오늘은', 92, INK, F_X)
    T(d, (520, 620), '연봉', 120, INK, F_X)
    s = '실수령액'; T(d, (520, 780), s, 132, OR, F_X)
    hand_under(d, 520 - wd(s, 132) / 2, 520 + wd(s, 132) / 2, 865, seed=402)

@board
def n3_gross(im):  # r05 '먼저 연봉이 어떤 돈인지' → 14·15행 '계약서 연봉은 떼기 전 돈, 세전 · 통장은 세후'
    d = payslip(im, 1000, 170, 1780, seed=411)
    hand_ellipse(d, (1012, 520, 1392, 612), OR, 7, seed=412)       # 지급 합계 = 세전
    hand_arrow(d, (900, 640), (1004, 590), OR, 7)
    T(d, (960, 700), '연봉 5,000만 ÷ 12', 36, INK, F_B)
    T(d, (500, 300), '연봉은 어떤 돈?', 70, INK, F_B)
    T(d, (520, 480), '계약서 연봉', 84, INK, F_X)
    s = '= 떼기 전 돈(세전)'; T(d, (520, 600), s, 72, OR, F_X)
    hand_under(d, 520 - wd(s, 72) / 2, 520 + wd(s, 72) / 2, 650, seed=413)
    T(d, (520, 800), '통장에 들어오는 돈 = 다 뗀 세후', 50, INK, F_B)
    source(d, '그림: 연봉 5천 한 달 예시 · ' + COND)

@board
def n3_seven(im):  # r09 '이제 일곱 칸입니다. 칸마다 통장 금액과 줄 위치를 같이 볼게요.'
    d = ImageDraw.Draw(im)
    s = '이제 일곱 칸'; T(d, (W // 2, 170), s, 104, INK, F_X)
    hand_under(d, W // 2 - wd(s, 104) / 2, W // 2 + wd(s, 104) / 2, 240, seed=421)
    labs = ('3천', '4천', '5천', '6천', '7천', '8천', '1억')
    bw, gap = 200, 34; x = (W - (7 * bw + 6 * gap)) // 2
    for i, a in enumerate(labs):
        y_top = 700 - 58 * i                      # 계단처럼 한 칸씩 위로
        torn(im, (x, y_top, x + bw, 900), KRAFT_L, seed=430 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, y_top - 40), '연봉 ' + a, 44, INK, F_X)
        T(d, (x + bw // 2, (y_top + 900) // 2 - 30), '통장', 36, INK, F_B)
        T(d, (x + bw // 2, (y_top + 900) // 2 + 28), '?', 64, OR, F_X)
        x += bw + gap
    T(d, (W // 2, 975), '칸마다 통장 금액 · 백 명 줄에서 몇 번째', 46, INK, F_B)

@board
def n3_netcheck(im):  # r13 '급여명세서 실지급액과 비교 · 상여 달은 따로'
    d = payslip(im, 180, 150, 960, seed=441, hi_net=True)
    T(d, (1380, 360), '표의 통장 금액은', 60, INK, F_B)
    s = '실지급액과 비교'; T(d, (1380, 480), s, 84, OR, F_X)
    hand_arrow(d, (1130, 560), (1010, 760), INK, 7)
    torn(im, (1120, 660, 1720, 900), MEMO, seed=442); d = ImageDraw.Draw(im)
    T(d, (1420, 740), '상여 나온 달은 따로', 50, INK, F_X)
    T(d, (1420, 820), '보통 달끼리 비교하세요', 40, INK, F_B)
    source(d, '그림: 연봉 5천 한 달 예시 · ' + COND)

def dashed(d, box, color=LINE, w=3, dash=14):
    x0, y0, x1, y1 = box
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        L = max(abs(bx - ax), abs(by - ay)); n = int(L // (2 * dash)) + 1
        for k in range(n):
            t0, t1 = 2 * k * dash / L, min(1, (2 * k + 1) * dash / L)
            d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=color, width=w)

@board
def n3_leak_q(im):  # r15 '그 세전 월급에서, 무엇이 얼마나 빠질까요?' — 다음 판 n3_waterfall과 같은 눈금의 빈 계단
    d = ImageDraw.Draw(im); title(d, '무엇이 얼마나 빠질까?', 110)
    steps = (('국민연금', 188380), ('건강보험', 142600), ('장기요양', 18730), ('고용보험', 35690), ('소득세', 190620), ('지방소득세', 19060))
    pre, net = 4166666, 3571586
    lo, hi, base, top = 3000000, 4200000, 850, 250
    Y = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    n = 8; bw = 150; gap = (1680 - n * bw) / (n - 1); X = lambda i: 120 + i * (bw + gap)
    torn(im, (X(0), Y(pre), X(0) + bw, base), KRAFT_L, seed=451); d = ImageDraw.Draw(im)
    T(d, (X(0) + bw / 2, Y(pre) - 76), '세전 월', 36, GREY, F_B); T(d, (X(0) + bw / 2, Y(pre) - 32), '417만원', 44, INK, F_X)
    cur = pre
    for i, (a, v) in enumerate(steps, 1):
        nxt = cur - v; d.line([(X(i - 1) + bw, Y(cur)), (X(i), Y(cur))], fill=GREY, width=3)
        dashed(d, (X(i), Y(cur), X(i) + bw, max(Y(nxt), Y(cur) + 12)))
        T(d, (X(i) + bw / 2, Y(cur) - 40), '−?', 54, OR, F_X)
        T(d, (X(i) + bw / 2, base + 46), a, 34 if len(a) < 5 else 30, INK, F_B)
        cur = nxt
    d.line([(X(6) + bw, Y(net)), (X(7), Y(net))], fill=GREY, width=3)
    dashed(d, (X(7), Y(net), X(7) + bw, base), INK)
    T(d, (X(7) + bw / 2, (Y(net) + base) / 2), '?', 96, OR, F_X)
    T(d, (X(0) + bw / 2, base + 46), '세전', 34, INK, F_B); T(d, (X(7) + bw / 2, base + 46), '통장', 38, INK, F_X)
    source(d, '연봉 5천 · ' + COND + ' · 300만원 아래는 잘라 그림')

def comment(im, box, who, lines, seed, size=64):
    """댓글 메모 — 노란 종이 + 작은 이름 줄 + 말(따옴표 없이)."""
    torn(im, box, MEMO, seed=seed); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    T(d, (x0 + 50, y0 + 60), who, 36, GREY, F_B, 'lm')
    for k, s in enumerate(lines): T(d, ((x0 + x1) // 2, y0 + 170 + k * (size + 30)), s, size, INK, F_X)
    return d

@board
def n3_why_q(im):   # r20 '연봉이 올랐는데 월급은 왜 별로 안 늘까요. 정말 많이 묻는 질문이에요.'
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), '정말 많이 묻는 질문', 54, GREY, F_B)
    torn(im, (330, 260, 1590, 780), PALE, seed=461); d = ImageDraw.Draw(im)
    T(d, (W // 2, 420), '연봉이 올랐는데', 104, INK, F_X)
    s = '월급은 왜 별로 안 늘까?'; T(d, (W // 2, 590), s, 104, OR, F_X)
    hand_under(d, W // 2 - wd(s, 104) / 2, W // 2 + wd(s, 104) / 2, 670, seed=462)
    T(d, (W // 2, 900), '연봉 1천만원 오를 때 통장에 남는 돈, 칸마다 셌어요', 46, INK, F_B)

@board
def n3_rev_q(im):   # r26 '세후 300이면 연봉이 얼마냐고요. 통장에 한 달 300만원이 찍히려면요.'
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 160), '검색창에 거꾸로 묻는 분도 많아요', 54, GREY, F_B)
    torn(im, (240, 330, 860, 720), PALE, seed=471); d = ImageDraw.Draw(im)
    T(d, (550, 440), '통장에 한 달', 54, INK, F_B); T(d, (550, 580), '300만원', 110, INK, F_X)
    hand_arrow(d, (900, 525), (1060, 525), INK, 9)
    torn(im, (1100, 330, 1700, 720), KRAFT_L, seed=472); d = ImageDraw.Draw(im)
    T(d, (1400, 440), '연봉은', 60, INK, F_B); T(d, (1400, 590), '얼마?', 130, OR, F_X)
    hand_ellipse(d, (1220, 500, 1580, 680), seed=473)
    T(d, (W // 2, 880), '세후 300 · 400 · 500 · 600만원 차례로', 50, INK, F_B)
    source(d, COND)

@board
def n3_back357(im):  # r30 '처음에 본 357만원으로 돌아가 볼게요.'
    d = ImageDraw.Draw(im)
    torn(im, (560, 250, 1360, 770), KRAFT_L, seed=481); d = ImageDraw.Draw(im)
    T(d, (W // 2, 360), '처음에 본', 60, INK, F_B)
    T(d, (W // 2, 470), '연봉 5천 · 통장 한 달', 52, INK, F_B)
    s = '357만원'; T(d, (W // 2, 630), s, 150, OR, F_X)
    hand_ellipse(d, (W // 2 - wd(s, 150) / 2 - 80, 525, W // 2 + wd(s, 150) / 2 + 80, 738), seed=482)
    T(d, (W // 2, 900), '같은 연봉인데 통장이 다른 이유 두 가지', 52, INK, F_X)
    source(d, COND)

@board
def n3_top25_q(im):  # r35 '이번엔 이런 댓글이에요. 난 왜 상위 25%인데 삶이 힘드냐.'
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 150), '이번엔 이런 댓글이에요', 54, GREY, F_B)
    d = comment(im, (360, 250, 1560, 640), '댓글', ('난 왜 상위 25%인데', '삶이 힘드냐'), seed=491, size=92)
    T(d, (W // 2, 790), '백 명 중 앞에서 스물다섯 번째쯤 사람들은', 52, INK, F_B)
    s = '통장에 얼마?'; T(d, (W // 2, 900), s, 80, OR, F_X)
    hand_under(d, W // 2 - wd(s, 80) / 2, W // 2 + wd(s, 80) / 2, 955, seed=492)

@board
def n3_sameformula(im):  # r39 '오늘 본 숫자는 전부 같은 계산식에서 나왔습니다.'
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), '오늘 본 숫자는 전부', 70, INK, F_B)
    s = '같은 계산식'; T(d, (W // 2, 300), s, 120, OR, F_X)
    hand_under(d, W // 2 - wd(s, 120) / 2, W // 2 + wd(s, 120) / 2, 380, seed=501)
    ins = ('연봉', '식대 비과세', '가족 수'); bw = 380; gap = 60; x = (W - (3 * bw + 2 * gap)) // 2
    for i, a in enumerate(ins):
        torn(im, (x, 480, x + bw, 640), PALE, seed=502 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, 560), a, 64, INK, F_X)
        if i < 2: T(d, (x + bw + gap // 2, 560), '+', 64, GREY, F_X)
        x += bw + gap
    hand_arrow(d, (W // 2, 670), (W // 2, 790), INK, 8)
    T(d, (W // 2, 860), '통장 금액', 84, INK, F_X)
    T(d, (W // 2, 975), '보험료율·간이세액표 올해 기준 · 국세청 줄 2024년 귀속', 40, GREY, F_B)

# ---------- r41 실사(검은 띠 잘라 꽉 채움) + 끝인사 ----------
def trimmed_frame(src, t=2.0):
    png = os.path.join(os.environ.get('TEMP', '.'), 'n3fix_' + os.path.basename(src) + '.png')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(t), '-i', os.path.join(PUB, src), '-frames:v', '1', png], check=True)
    im = Image.open(png).convert('RGB'); g = im.convert('L'); w, h = im.size
    rows = [sum(g.crop((0, y, w, y + 1)).get_flattened_data()) / w for y in range(h)]
    top = next(y for y in range(h) if rows[y] > 18); bot = next(y for y in range(h - 1, -1, -1) if rows[y] > 18)
    im = im.crop((0, top + 4, w, bot - 4))                       # 검은 띠 + 경계 4px 잘라냄
    r = max(W / im.width, H / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)), (top, bot, h)

def n3_end_over():
    im, info = trimmed_frame('stock/window_dusk.mp4')
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    for y in range(0, int(H * 0.4)):    # 위 짙은 그라데이션(상자 아님), 아래는 최종 화면 자리라 비움
        gd.line([(0, y), (W, y)], fill=int(170 * (1 - y / (H * 0.4)) ** 1.2))
    im.paste((0, 0, 0), (0, 0), g); d = ImageDraw.Draw(im)
    d.text((W // 2, 150), '다음 영상에서 다시 뵙겠습니다', font=font(F_X, 96), fill=(255, 255, 255), anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
    os.makedirs(os.path.join(PUB, 'over'), exist_ok=True); im.save(os.path.join(PUB, 'over', 'n3_end_r41.png'))
    print('over n3_end_r41', 'letterbox rows', info)

def main(names):
    os.makedirs(os.path.join(PUB, 'board'), exist_ok=True)
    for n in names or list(B) + ['n3_end_over']:
        if n == 'n3_end_over': n3_end_over(); continue
        im = canvas(); B[n](im); im.save(os.path.join(PUB, 'board', n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
