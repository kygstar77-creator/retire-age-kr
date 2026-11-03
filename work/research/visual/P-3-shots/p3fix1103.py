"""P-3 실사 11줄 교체 — visual-designer 2026-11-03 07시(운영실장 배차).
10/29 18시 새 심사관 2명(judge3s_a·b)이 '못함'이라 한 r03·06·07·10·23·24·28·31·34·36·39를 고친다.
- 실사가 맞는 3줄(r03·r31·r34): 같은 실사 위 큰 흰 글자(쇼츠·C2 data.over 꼴, 검은 테두리, 주황은 답 하나) → bg/p3/over/
- 외국 글자·외국인·흐림·뜻 안 보임 7줄(r06·07·10·23·28·36·39): 종이 판(p3boards 꼴) → bg/p3/board/
- r24: 11월 달력은 대본과 어긋남(대본 '연금은 해가 바뀌는 1월마다') → 2027년 1월 달력 판(1일 금요일 실제)
글자는 say_v1.txt 말 그대로. 숫자는 calc_out·대본 값만.
사용: py -3.12 p3fix1103.py
"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import W, H, INK, GREY, OR, KRAFT_L, F_B, F_M, F_X, font, canvas, T, title, source, torn, hand_ellipse, hand_under, hand_arrow
from PIL import Image, ImageDraw, ImageFilter

PUB = os.path.join(K.WORK, 'video', 'public', 'bg', 'p3')
FF = os.path.join(K.WORK, 'video', 'node_modules', '@remotion', 'compositor-win32-x64-msvc', 'ffmpeg.exe')
MEMO = (246, 236, 178); PAPER_N = (238, 230, 212); WHITE_P = (250, 248, 242)
def wd(s, size, f=F_X): return font(f, size).getlength(s)

# ---------- 실사 + 큰 흰 글자 ----------
def frame(src, t=2.0):
    p = os.path.join(PUB, src)
    if p.endswith('.mp4'):
        png = os.path.join(os.environ.get('TEMP', '.'), 'p3fix_' + os.path.basename(p) + '.png')
        subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(t), '-i', p, '-frames:v', '1', png], check=True); p = png
    im = Image.open(p).convert('RGB'); r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def over(src, small, big, out, t=2.0):
    im = frame(src, t)
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    for y in range(int(H * 0.45), H):   # 아래 짙은 그라데이션(상자 아님)
        gd.line([(0, y), (W, y)], fill=int(200 * ((y - H * 0.45) / (H * 0.55)) ** 1.1))
    im.paste((0, 0, 0), (0, 0), g); d = ImageDraw.Draw(im)
    d.text((W // 2, 742), small, font=font(F_B, 66), fill=(255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((W // 2, 880), big, font=font(F_X, 112), fill=OR, anchor='mm', stroke_width=7, stroke_fill=(0, 0, 0))
    os.makedirs(os.path.join(PUB, 'over'), exist_ok=True); im.save(os.path.join(PUB, 'over', out)); print('over', out)

# ---------- 종이 판 ----------
B = {}
def board(fn): B[fn.__name__] = fn; return fn

@board
def p3_auto_over(im):   # r06 '아무것도 안 해도 넘을 수 있습니다'
    d = ImageDraw.Draw(im)
    torn(im, (430, 300, 1490, 470), KRAFT_L, seed=301); d = ImageDraw.Draw(im)
    T(d, (W // 2, 385), '올해 국민연금 월 165만원 · 아직은 기준 아래', 50, INK, F_B)
    T(d, (W // 2, 620), '아무것도 안 해도', 104, INK, F_X)
    s = '넘을 수 있습니다'; T(d, (W // 2, 800), s, 120, OR, F_X)
    hand_under(d, W // 2 - wd(s, 120) / 2, W // 2 + wd(s, 120) / 2, 880, seed=302)

@board
def p3_kin_intro(im):   # r07 '지식iN에 이런 질문이 있었어요' — r08 질문 메모 앞 장
    d = ImageDraw.Draw(im)
    torn(im, (460, 330, 1460, 760), MEMO, seed=311); d = ImageDraw.Draw(im)
    T(d, (W // 2, 470), '지식iN에', 92, INK, F_X)
    T(d, (W // 2, 610), '이런 질문이 있었어요', 92, INK, F_X)
    T(d, (W // 2, 900), '국민연금 받는 분이 직접 물은 것', 46, GREY, F_M)

@board
def p3_public_all(im):  # r10 '국민연금은 받은 돈을 전부 셉니다. 세금을 떼는지와 상관없이요.'
    d = ImageDraw.Draw(im)
    torn(im, (420, 260, 1500, 820), PAPER_N, seed=321); d = ImageDraw.Draw(im)
    T(d, (W // 2, 400), '국민연금은', 96, INK, F_X)
    s = '받은 돈 전부 셉니다'; T(d, (W // 2, 580), s, 104, OR, F_X)
    hand_under(d, W // 2 - wd(s, 104) / 2, W // 2 + wd(s, 104) / 2, 650, seed=322)
    T(d, (W // 2, 740), '세금을 떼는지와 상관없이', 54, INK, F_B)
    source(d, '국민건강보험공단 안내 · 피부양자 소득 기준')

@board
def p3_old_erase(im):   # r23 '예전 기사나 영상 계산은 지우셔야'
    d = ImageDraw.Draw(im)
    torn(im, (460, 200, 1460, 760), (232, 226, 210), seed=331); d = ImageDraw.Draw(im)
    T(d, (W // 2, 290), '예전 기사·영상 속 계산', 54, GREY, F_B)
    for k, s in enumerate(('탈락해도 첫해는 80% 깎아 줌', '다음 해 60% · 40% · 20%')):
        y = 420 + k * 120; T(d, (W // 2, y), s, 64, INK, F_B)
        x0, x1 = W // 2 - wd(s, 64, F_B) / 2 - 20, W // 2 + wd(s, 64, F_B) / 2 + 20
        d.line([(x0, y + 6), (x1, y - 6)], fill=INK, width=8)
    T(d, (W // 2, 660), '2026년 8월분으로 모두 끝남', 46, GREY, F_M)
    s = '그 계산은 지우셔야 합니다'; T(d, (W // 2, 880), s, 96, OR, F_X)
    source(d, '국민건강보험공단 · 피부양자 탈락자 보험료 경감 2026년 8월분 종료')

@board
def p3_calendar_jan(im):   # r24 '연금이 오르면 바로 그달부터 탈락? 아님 — 연금은 해가 바뀌는 1월마다'
    d = ImageDraw.Draw(im)
    torn(im, (300, 80, 1240, 1010), WHITE_P, seed=341); d = ImageDraw.Draw(im)
    cx = 770; T(d, (cx, 170), '2027년 1월', 66, INK, F_X)
    days = '일월화수목금토'; cw, ch = 120, 112; x0 = cx - cw * 3.5; y0 = 260
    for k, c in enumerate(days): T(d, (x0 + cw * k + cw / 2, y0), c, 34, GREY, F_B)
    off = 5   # 2027-01-01 금요일
    for n in range(1, 32):
        i = n - 1 + off; k, r = i % 7, i // 7; x = x0 + cw * k; y = y0 + 44 + ch * r
        d.rectangle((x, y, x + cw, y + ch), outline=(200, 194, 184), width=2)
        T(d, (x + 16, y + 28), str(n), 32, INK, F_M, 'lm')
    k, r = off % 7, 0; x = x0 + cw * k; y = y0 + 44
    hand_ellipse(d, (x - 8, y - 6, x + cw + 8, y + ch + 6), OR, 8, seed=342)
    T(d, (1600, 340), '연금이 오른 그달', 56, INK, F_B); T(d, (1600, 430), '바로 탈락?', 70, INK, F_X)
    T(d, (1600, 560), '아니에요', 80, INK, F_X)
    T(d, (1600, 760), '연금은', 56, INK, F_B); T(d, (1600, 850), '1월마다', 84, OR, F_X)
    T(d, (1600, 940), '한 해씩 넘어가요', 50, INK, F_B)
    source(d, '국민건강보험공단 · 연금은 작년 한 해 받은 돈으로 판정')

@board
def p3_interest_too(im):   # r28 '기준 근처인 분은 예금 이자도 신경이 쓰이죠'
    d = ImageDraw.Draw(im); title(d, '기준 근처인 분이라면', 140)
    for i, (a, c) in enumerate((('국민연금', KRAFT_L), ('예금 이자 · 배당', PAPER_N))):
        x0 = 300 + i * 760; torn(im, (x0, 330, x0 + 560, 640), c, seed=351 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 280, 485), a, 70, INK, F_X)
    T(d, (W // 2, 485), '+', 120, INK, F_X)
    s = '예금 이자도 봐야 해요'; T(d, (W // 2, 840), s, 104, OR, F_X)
    hand_under(d, W // 2 - wd(s, 104) / 2, W // 2 + wd(s, 104) / 2, 915, seed=353)

@board
def p3_early_q(im):   # r36 '피부양자를 지키려면 연금을 일찍 당겨 받아서 줄이면 되지 않을까'
    d = ImageDraw.Draw(im)
    torn(im, (360, 260, 1560, 820), MEMO, seed=361); d = ImageDraw.Draw(im)
    T(d, (W // 2, 370), '피부양자를 지키려면', 60, GREY, F_B)
    T(d, (W // 2, 520), '연금을 일찍 당겨 받아서', 84, INK, F_X)
    s = '줄이면 되지 않을까?'; T(d, (W // 2, 670), s, 96, OR, F_X)
    T(d, (W // 2, 920), '이런 생각이 드실 수 있어요', 46, GREY, F_M)

@board
def p3_take_notice(im):   # r39 '연금 통지서를 꺼내서 ~ 셈해 보세요'
    d = ImageDraw.Draw(im); title(d, '오늘 할 일은 하나', 120)
    x0, y0, x1, y1 = 560, 230, 1360, 640
    torn(im, (x0, y0, x1, y1), WHITE_P, seed=371); d = ImageDraw.Draw(im)
    d.line([(x0 + 10, y0 + 10), ((x0 + x1) // 2, y0 + 220), (x1 - 10, y0 + 10)], fill=(190, 182, 170), width=5)
    T(d, ((x0 + x1) // 2, y0 + 300), '국민연금 통지서', 62, INK, F_X)
    T(d, (W // 2, 760), '꺼내서, 내년에 연금이 물가만큼 오르면', 58, INK, F_B)
    s = '한 해 2천만원 넘는지 셈해 보기'; T(d, (W // 2, 880), s, 84, OR, F_X)

def main():
    out = os.path.join(PUB, 'board')
    for n, fn in B.items():
        im = canvas(); fn(im); im.save(os.path.join(out, n + '.png')); print(n)
    over('ai/notice_magnifier.png', '자녀 직장보험 피부양자라면', '건강보험료 한 푼도 안 내요', 'p3_over_r03.png')
    over('stock/phone_pickup.mp4', '999만원처럼 선 근처라면 먼저', '공단 고객센터 1577-1000', 'p3_over_r31.png', 3.0)
    over('stock/apartment_windows.mp4', '집 재산세 기준 금액(시세 아님)', '과세표준 5억 4천만원 넘으면', 'p3_over_r34.png')

# ---------- 2차(11/3 07:17, 새 심사관 2명 1차 지적 반영) ----------
@board
def p3_next_year(im):   # r24 2차: 달력 1일 동그라미가 '1월부터 탈락'으로 거꾸로 읽힘(심사 2명) → 두 칸 흐름. 대본 43~45줄.
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 150), '연금이 오른 그달 바로 탈락?', 70, INK, F_X)
    T(d, (W // 2, 260), '아니에요', 70, INK, F_X)
    for i, (a, b, c) in enumerate((('내년', '연금이 물가만큼 오름', KRAFT_L), ('그다음 해', '판정에 들어감', PAPER_N))):
        x0 = 230 + i * 780; torn(im, (x0, 380, x0 + 680, 700), c, seed=381 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 340, 480), a, 72, INK, F_X); T(d, (x0 + 340, 610), b, 56, INK, F_B)
    hand_arrow(d, (930, 540), (1000, 540), INK, 8)
    s = '고지서는 그다음 해부터'; T(d, (W // 2, 860), s, 100, OR, F_X)
    hand_under(d, W // 2 - wd(s, 100) / 2, W // 2 + wd(s, 100) / 2, 935, seed=383)
    source(d, '국민건강보험공단 · 연금은 작년 한 해 받은 돈으로 판정, 해가 바뀌는 1월마다 넘어감')

@board
def p3_call_first(im):   # r31 2차: 휴대폰 위 손이 흐리고 어색(심사 A) → 종이 판. 대본 55줄.
    d = ImageDraw.Draw(im)
    torn(im, (420, 250, 1500, 470), KRAFT_L, seed=391); d = ImageDraw.Draw(im)
    T(d, (W // 2, 360), '999만원처럼 선 근처라면', 74, INK, F_X)
    T(d, (W // 2, 560), '공단 고객센터', 80, INK, F_X)
    s = '1577-1000'; T(d, (W // 2, 760), s, 150, OR, F_X)
    hand_ellipse(d, (W // 2 - wd(s, 150) / 2 - 90, 645, W // 2 + wd(s, 150) / 2 + 90, 885), INK, 7, seed=392)
    T(d, (W // 2, 975), '먼저 물어보세요', 60, INK, F_B)

def main2():
    out = os.path.join(PUB, 'board')
    for n in ('p3_next_year', 'p3_call_first'):
        im = canvas(); B[n](im); im.save(os.path.join(out, n + '.png')); print(n)
    over('stock/apartment_windows.mp4', '재산세 고지서의 과세표준(시세 아님)', '과세표준 5억 4천만원 넘으면', 'p3_over_r34.png')

if __name__ == '__main__':
    (main2 if sys.argv[1:] == ['2'] else main)()
