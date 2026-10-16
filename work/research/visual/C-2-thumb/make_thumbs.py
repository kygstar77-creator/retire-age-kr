# C-2 '같은 3억, 5년 차이' 썸네일 시안 (2026-10-15 visual-designer, 요청 meta.json thumb_status 10/14 14:38 · 기한 10/17 06:00)
# 문구: ep/C-2/copy/titles.md thumb_text '같은 3억, 5년 차이' · small '1998년 시작은 바닥 · 2003년은 2.7억'(레드팀: '바닥'·'2.7억'을 크게)
# 숫자: calc_n1_out.txt 월 200만원 1998년 1월 시작 → 2011년 바닥 · 2003년 1월 시작 → 2025년 말 2.72억원 (assert)
# 피한 것: 경쟁 1·2(생성 그림 인물·책상) · 3~5(사진+노랑 테두리 글) · 우리 N-2(남색 두 칸) — 주제 사물 = 통장 두 권(사람 얼굴 0)
# 금지(titles.md): '0원'·'파산'·'평생'·15.9억·정우 씨 이름 · '1998년에 바닥'으로 읽히는 배치(실제 바닥 2011년)
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, '..', '..', 'longform', 'ep', 'C-2')
calc = open(os.path.join(EP, 'calc_n1_out.txt'), encoding='utf-8').read()
assert '월 200만원 · 1998년 1월 시작 → 바닥 2011년' in calc
LEFT = float(re.search(r'월 200만원 · 2003년 1월 시작 → 2025년 말 ([\d.]+)억원 남음', calc).group(1))
assert round(LEFT, 1) == 2.7, LEFT
R = f'{round(LEFT, 1)}억'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]


def book(x, y, w, h, cover, inner, tag='', tagc='#14171C', ts=0.15, band=0.24):
    """펼친 통장 — 위 표지 띠 + 안쪽 흰 면(줄 3개) + 가운데 큰 글(inner)"""
    rows = ''.join(f"<div style='position:absolute;left:{w*0.08:.0f}px;top:{h*(0.3+i*0.1):.0f}px;width:{w*0.84:.0f}px;height:3px;background:#E3E6EC'></div>" for i in range(3))
    t = f"<div class='t' style='left:0;top:{h*0.04:.0f}px;width:{w}px;text-align:center;font-size:{h*ts:.0f}px;color:#FFFFFF'>{tag}</div>" if tag else ''
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#FFFFFF;border-radius:18px;box-shadow:0 14px 0 rgba(0,0,0,.35);overflow:hidden'>"
            f"<div style='position:absolute;left:0;top:0;width:{w}px;height:{h*band:.0f}px;background:{cover}'></div>{t}{rows}"
            f"<div class='t' style='left:0;top:{h*0.4:.0f}px;width:{w}px;text-align:center;{inner}'></div></div>")


def stamp(word, size):
    return f"font-size:{size}px;color:#D7261E'><span style='display:inline-block;border:10px solid #D7261E;border-radius:16px;padding:0 24px;transform:rotate(-8deg)'>{word}</span"


def big(word, size, col='#0E7A3E'):
    return f"font-size:{size}px;color:{col}'>{word}<span style='display:none'></span"


V = {}
HEADLINE = ("<div class='t' style='left:0;top:26px;width:1280px;text-align:center;font-size:132px;color:#FFD23F'>같은 3억,"
            " <span style='color:#FFFFFF'>5년 차이</span></div>")
BG = "<div style='position:absolute;inset:0;background:#14171C'></div>"
# c2a — 통장 두 권: 왼쪽 '바닥' 빨간 도장 · 오른쪽 '2.7억' 초록 (숫자 3개: 3억·5년·2.7억)
V['c2a'] = BG + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥', 120).replace("'></div></div>", "")) + book(640, 214, 520, 340, '#2B6BE4', big(R, 150))
# c2b — 같은 틀, 오른쪽 '남음'(숫자 2개 기준 지킴: 3억·5년)
V['c2b'] = BG + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥', 120)) + book(640, 214, 520, 340, '#2B6BE4', big('남음', 150))
# c2c — c2a + 표지 띠에 시작 해(titles small 줄 '1998년 시작은 바닥 · 2003년은 2.7억' 그대로 나눔) — 숫자 5개, 1초 시험 비교용
V['c2c'] = BG + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥', 120), tag='1998년 시작') + book(640, 214, 520, 340, '#2B6BE4', big(R, 150), tag='2003년 시작')
# 2차(10/15 17시) — 검수 09:50 이해 시험: '1998년 시작은 바닥'을 '주가 바닥에 들어감'으로 거꾸로 읽음 → 주어 '통장'+'바닥남'(끝난 일)
#   + thumb-gap-1015 ①: 진한 판(어두운 질감·밝기 60~150·채도 중앙 100+·명암 폭 80+)과 크림 판을 같은 차수에
DARK = ("<div style='position:absolute;inset:0;background:radial-gradient(circle at 28% 18%,#168A78 0%,#0B5249 52%,#06312C 100%)'></div>"
        "<div style='position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.045) 0 3px,transparent 3px 12px)'></div>")
CREAM = "<div style='position:absolute;inset:0;background:#F3E8CF'></div>"
HL_CREAM = ("<div class='t' style='left:0;top:26px;width:1280px;text-align:center;font-size:132px;color:#1B2A4A'>같은 3억,"
            " <span style='color:#E2541B'>5년 차이</span></div>")


def right_left(size=132):
    return f"font-size:{size}px;color:#0E7A3E'>{R}<span style='font-size:{size*0.5:.0f}px;color:#14171C'> 남음</span"


L1, L2 = '1998년 시작 통장', '2003년 시작 통장'
V['c2d'] = DARK + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥남', 112), tag=L1) + book(640, 214, 520, 340, '#2B6BE4', right_left(), tag=L2)
V['c2e'] = CREAM + HL_CREAM + book(60, 214, 520, 340, '#6B7280', stamp('바닥남', 112), tag=L1) + book(640, 214, 520, 340, '#2B6BE4', right_left(), tag=L2)
# c2f — 진한 판 + 검수 제안 말 그대로 '돈 다 떨어짐'(두 줄 도장)
V['c2f'] = DARK + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('돈 다<br>떨어짐', 76), tag=L1) + book(640, 214, 520, 340, '#2B6BE4', right_left(), tag=L2)
# 3차 — 2차 심사: 무엇에 넣은 3억인지 없음(Claude) · 청록이 직전 편 P-1 p4e와 겹침(제미나이) · aitell A31 '2.7억' 소수점 → 말로 '2억 7천'(대본 113줄)
WINE = ("<div style='position:absolute;inset:0;background:radial-gradient(circle at 30% 15%,#9A2F4A 0%,#5E1630 55%,#350A1B 100%)'></div>"
        "<div style='position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.04) 0 3px,transparent 3px 12px)'></div>")
KICK = ("<div class='t' style='left:0;top:20px;width:1280px;text-align:center;font-size:46px;color:#14171C'>"
        "<span style='background:#FFFFFF;border-radius:12px;padding:2px 22px'>S&amp;P500 퇴직금</span></div>")
HL3 = ("<div class='t' style='left:0;top:84px;width:1280px;text-align:center;font-size:118px;color:#FFD23F'>같은 3억,"
       " <span style='color:#FFFFFF'>5년 차이</span></div>")


def right_word(word, size=104):
    return f"font-size:{size}px;color:#0E7A3E'>{word}<span style='font-size:{size*0.5:.0f}px;color:#14171C'>  남음</span"


assert '2억 7천만원이 남아' in open(os.path.join(EP, 'script.md'), encoding='utf-8').read() and R == '2.7억'
# 3차 레드팀: 머리글 연도를 1.5배(통장은 빼도 됨, '바닥남' 유지) · c2f '돈 다 떨어짐'은 0원과 같은 단정이라 반려
BK = dict(ts=0.23, band=0.31)
Y1, Y2 = '1998년 시작', '2003년 시작'
V['c2g'] = WINE + KICK + HL3 + book(60, 236, 520, 330, '#6B7280', stamp('바닥남', 100), tag=Y1, **BK) + book(640, 236, 520, 330, '#2B6BE4', right_word('2억 7천', 112), tag=Y2, **BK)
KICK_C = KICK.replace("color:#14171C'><span style='background:#FFFFFF", "color:#FFFFFF'><span style='background:#1B2A4A")
HL3_C = HL3.replace("#FFD23F'", "#1B2A4A'").replace("color:#FFFFFF'>5년", "color:#E2541B'>5년")
V['c2i'] = CREAM + KICK_C + HL3_C + book(60, 236, 520, 330, '#6B7280', stamp('바닥남', 100), tag=Y1, **BK) + book(640, 236, 520, 330, '#2B6BE4', right_word('2억 7천', 112), tag=Y2, **BK)
# 4차 후보 — Claude 3차: '통장' 머리글 다시 크게(오독 길 막기)·띠지 키우기
KICK4 = KICK.replace("top:20px", "top:14px").replace("font-size:46px", "font-size:58px")
HL4 = HL3.replace("top:84px", "top:92px").replace("font-size:118px", "font-size:112px")
V['c2j'] = WINE + KICK4 + HL4 + book(40, 240, 560, 330, '#6B7280', stamp('바닥남', 100), tag=L1, ts=0.19, band=0.29) + book(680, 240, 560, 330, '#2B6BE4', right_word('2억 7천', 112), tag=L2, ts=0.19, band=0.29)
# 4차 — 3차 레드팀: '통장' 빼면 '주가 바닥에 샀다' 오독이 돌아옴(통장 유지) · 알약 꼬리표는 경쟁 꼬리표와 닮음(맨 글씨로) · '남음' 1.5배
def right_word4(word, size=112):
    return f"font-size:{size}px;color:#0E7A3E'>{word}<span style='font-size:{size*0.72:.0f}px;color:#14171C'> 남음</span"


KICK_PLAIN = "<div class='t' style='left:0;top:14px;width:1280px;text-align:center;font-size:58px;color:{c}'>S&amp;P500 퇴직금</div>"
HB = dict(ts=0.19, band=0.29)
V['c2k'] = WINE + KICK_PLAIN.format(c='#FFFFFF') + HL4 + book(40, 240, 560, 330, '#6B7280', stamp('바닥남', 100), tag=L1, **HB) + book(680, 240, 560, 330, '#2B6BE4', right_word4('2억 7천', 100), tag=L2, **HB)
HL4_C = HL4.replace("#FFD23F'", "#1B2A4A'").replace("color:#FFFFFF'>5년", "color:#E2541B'>5년")
V['c2l'] = CREAM + KICK_PLAIN.format(c='#1B2A4A') + HL4_C + book(40, 240, 560, 330, '#6B7280', stamp('바닥남', 100), tag=L1, **HB) + book(680, 240, 560, 330, '#2B6BE4', right_word4('2억 7천', 100), tag=L2, **HB)
# 5차 — 4차 Claude: 글자가 화면을 덜 채움(경쟁은 절반) · 띠 글씨 168px에서 안 읽힘 · '바닥남' 도장이 '2억 7천'보다 약함
def stamp_fill(word, size):
    return f"font-size:{size}px;color:#FFFFFF'><span style='display:inline-block;background:#D7261E;border-radius:16px;padding:0 26px;transform:rotate(-6deg)'>{word}</span"


KICK5 = ("<div class='t' style='left:0;top:8px;width:1280px;text-align:center;font-size:66px;color:#FFFFFF'>S&amp;P500 퇴직금"
         "<div style='margin:-4px auto 0;width:420px;height:8px;background:#FFD23F;border-radius:4px'></div></div>")
HL5 = ("<div class='t' style='left:0;top:96px;width:1280px;text-align:center;font-size:150px;color:#FFD23F'>같은 3억,"
       " <span style='color:#FFFFFF'>5년 차이</span></div>")
H5 = dict(ts=0.2, band=0.3)
V['c2m'] = WINE + KICK5 + HL5 + book(40, 286, 560, 290, '#6B7280', stamp_fill('바닥남', 104).replace('top:116px', 'top:100px'), tag=L1, **H5) + book(680, 286, 560, 290, '#2B6BE4', right_word4('2억 7천', 112), tag=L2, **H5)
KICK5_C = KICK5.replace("color:#FFFFFF'>S&amp;P500", "color:#1B2A4A'>S&amp;P500").replace("background:#FFD23F;border-radius:4px", "background:#E2541B;border-radius:4px")
HL5_C = HL5.replace("#FFD23F'", "#1B2A4A'").replace("color:#FFFFFF'>5년", "color:#E2541B'>5년")
V['c2n'] = CREAM + KICK5_C + HL5_C + book(40, 286, 560, 290, '#6B7280', stamp_fill('바닥남', 104).replace('top:116px', 'top:100px'), tag=L1, **H5) + book(680, 286, 560, 290, '#2B6BE4', right_word4('2억 7천', 112), tag=L2, **H5)
# 6차 — 5차 Claude: '바닥남' 글만으론 뜻이 갈림 → 통장 잔액 막대(빈 통/찬 통)로 글 없이도 보이게. 값은 calc: 바닥 해 1월 0.12억/3억, 2025 말 2.72억/3억
LOW = float(re.search(r'1998년 1월 시작 → 바닥 2011년\(시작 14년차, 1월에 남은 돈 ([\d.]+)억원', calc).group(1))
assert LOW == 0.12, LOW


def gauge(x, y, w, frac, col):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:34px;border-radius:17px;background:#E3E6EC;overflow:hidden'>"
            f"<div style='width:{max(frac, 0.04) * 100:.0f}%;height:34px;background:{col};border-radius:17px'></div></div>")


def g6(bg, kick, hl):
    return (bg + kick + hl + book(40, 286, 560, 290, '#6B7280', stamp_fill('바닥남', 96), tag=L1, **H5) + gauge(90, 510, 460, LOW / 3, '#D7261E')
            + book(680, 286, 560, 290, '#2B6BE4', right_word4('2억 7천', 104), tag=L2, **H5) + gauge(730, 510, 460, LEFT / 3, '#0E7A3E'))


V['c2o'] = g6(WINE, KICK5, HL5)
V['c2p'] = g6(CREAM, KICK5_C, HL5_C)
# 7차 — 5차 레드팀: 168px '통장'→'동갑' 오독 · 도장에 해를 넣어 '바닥'을 사건으로('2011년 바닥남', calc 바닥 해) · 강조색은 '5년 차이'에 · 오른쪽 시점 '2025년 말'
#   + 5차 Claude: 빈 통/찬 통 막대(c2o·c2p, 6차와 같은 차수)
assert '바닥 2011년' in calc and '2025년 말' in calc
HL7 = ("<div class='t' style='left:0;top:96px;width:1280px;text-align:center;font-size:150px;color:#FFFFFF'>같은 3억,"
       " <span style='color:#FFD23F'>5년 차이</span></div>")
H7 = dict(ts=0.25, band=0.3)


def g7(bg, kick, hl, sub='#5B6270'):
    when = f"<div class='t' style='left:680px;top:380px;width:560px;text-align:center;font-size:30px;color:{sub}'>2025년 말</div>"
    return (bg + kick + hl + book(40, 286, 560, 290, '#6B7280', stamp_fill('2011년 바닥남', 66), tag='1998년 시작', **H7) + gauge(90, 510, 460, LOW / 3, '#D7261E')
            + book(680, 286, 560, 290, '#2B6BE4', right_word4('2억 7천', 104), tag='2003년 시작', **H7) + when + gauge(730, 510, 460, LEFT / 3, '#0E7A3E'))


V['c2q'] = g7(WINE, KICK5, HL7)
V['c2r'] = g7(CREAM, KICK5_C, HL5_C)
# 8차 — 6차 Claude: '2011년 바닥남'=2011년이 주가 바닥 오독 → 해는 작은 윗줄로 빼고(좌 '2011년'·우 '2025년 말' 대칭) 도장은 '통장 바닥남' · 막대 두 배 두께
def gauge2(x, y, w, frac, col, h=48):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{h//2}px;background:#E3E6EC;overflow:hidden'>"
            f"<div style='width:{max(frac, 0.05) * 100:.0f}%;height:{h}px;background:{col};border-radius:{h//2}px'></div></div>")


def lab(x, txt, c='#5B6270'):
    return f"<div class='t' style='left:{x}px;top:376px;width:560px;text-align:center;font-size:34px;color:{c}'>{txt}</div>"


def g8(bg, kick, hl):
    L = book(40, 286, 560, 290, '#6B7280', stamp_fill('통장 바닥남', 66), tag='1998년 시작', **H7).replace('top:116px;width:560px', 'top:134px;width:560px')
    Rr = book(680, 286, 560, 290, '#2B6BE4', right_word4('2억 7천', 96), tag='2003년 시작', **H7).replace('top:116px;width:560px', 'top:122px;width:560px')
    return (bg + kick + hl + L + lab(40, '2011년') + gauge2(90, 526, 460, LOW / 3, '#D7261E', 40)
            + Rr + lab(680, '2025년 말') + gauge2(730, 526, 460, LEFT / 3, '#0E7A3E', 40))


V['c2s'] = g8(WINE, KICK5, HL7)
V['c2t'] = g8(CREAM, KICK5_C, HL5_C)
# 8차 b — 6차 레드팀: '매달 꺼내 썼다' 조건이 없으면 '지수가 망해 0' · 91% 막대='9%만 잃음'으로 읽힘 → 띠에 조건(titles swap_small '3억 · 월 200만원'의 말)
assert '월 200만원 · 1998년 1월 시작' in calc
KICK8 = ("<div class='t' style='left:0;top:8px;width:1280px;text-align:center;font-size:58px;color:{c}'>S&amp;P500 퇴직금, <span style='color:{a}'>매달 200만원</span>씩 꺼내 쓰면"
         "</div>")
V['c2u'] = g8(WINE, KICK8.format(c='#FFFFFF', a='#FFD23F'), HL7)
V['c2v'] = g8(CREAM, KICK8.format(c='#1B2A4A', a='#E2541B'), HL5_C)
# 9차 — 7차 레드팀: '~하면' 말투가 경쟁과 겹침(유사 3) · '매달'은 계산(해마다 1년 치 한 번에)과 어긋남 → '월 200만원씩'(titles swap_small 말) · 해 표기 168px에서 안 읽힘 → 키움 · 크림 주황 강조가 P-1과 같음 → 빨강
KICK9 = "<div class='t' style='left:0;top:8px;width:1280px;text-align:center;font-size:60px;color:{c}'><span style='color:{a}'>월 200만원씩</span> 꺼내 쓴 S&amp;P500 퇴직금</div>"


def lab9(x, txt, c='#3A4150'):
    return f"<div class='t' style='left:{x}px;top:374px;width:560px;text-align:center;font-size:46px;color:{c}'>{txt}</div>"


def g9(bg, kick, hl):
    L = book(40, 286, 560, 290, '#6B7280', stamp_fill('통장 바닥남', 64), tag='1998년 시작', **H7).replace('top:116px;width:560px', 'top:144px;width:560px')
    Rr = book(680, 286, 560, 290, '#2B6BE4', right_word4('2억 7천', 92), tag='2003년 시작', **H7).replace('top:116px;width:560px', 'top:132px;width:560px')
    return (bg + kick + hl + L + lab9(40, '2011년') + gauge2(90, 528, 460, LOW / 3, '#D7261E', 38)
            + Rr + lab9(680, '2025년 말') + gauge2(730, 528, 460, LEFT / 3, '#0E7A3E', 38))


HL9_C = HL5_C.replace("color:#E2541B'>5년", "color:#C8231B'>5년")
V['c2w'] = g9(CREAM, KICK9.format(c='#1B2A4A', a='#C8231B'), HL9_C)
V['c2x'] = g9(WINE, KICK9.format(c='#FFFFFF', a='#FFD23F'), HL7)
# 10차(10/16 09시) — copywriter 10/15 18:59 큰 글 '같은 3억, 시작만 5년 차이'('5년 차이'가 '5년 더 버팀'으로 읽힘 막음)
#   + 8차 레드팀: ① '2011년'·'2025년 말' 168px에서 작음 → 46→64px ② 도장이 '1998년 시작' 바로 밑 = 외환위기 연상 → 도장을 빈 막대 오른쪽 빈자리로
#   + 8차 Claude: 글자가 화면을 덜 채움·카드 안 잔글씨 → 카드 안 줄 3개 지움, 큰 글 두 줄
def card10(x, y, w, h, cover, year_tag, when, body, bar):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#FFFFFF;border-radius:18px;box-shadow:0 12px 0 rgba(0,0,0,.30);overflow:hidden'>"
            f"<div style='position:absolute;left:0;top:0;width:{w}px;height:84px;background:{cover}'></div>"
            f"<div class='t' style='left:0;top:10px;width:{w}px;text-align:center;font-size:66px;color:#FFFFFF'>{year_tag}</div>"
            f"<div class='t' style='left:0;top:100px;width:{w}px;text-align:center;font-size:62px;color:#1B2A4A'>{when}</div>"
            f"{body}{bar}</div>")


def bar10(frac, col, y=262, x=40, w=480, h=44):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{h//2}px;background:#E3E6EC;overflow:hidden'>"
            f"<div style='width:{max(frac, 0.06) * 100:.0f}%;height:{h}px;background:{col};border-radius:{h//2}px'></div></div>")


STAMP10 = ("<div class='t' style='left:96px;top:180px;font-size:70px;color:#FFFFFF'><span style='display:inline-block;background:#D7261E;border-radius:14px;"
           "padding:4px 22px;transform:rotate(-5deg)'>통장 바닥남</span></div>")
LEFT10 = "<div class='t' style='left:0;top:176px;width:560px;text-align:center;font-size:84px;color:#0E7A3E'>2억 7천<span style='font-size:60px;color:#14171C'> 남음</span></div>"


def g10(bg, kick, l1, l2, top=296, ch=340):
    # 좌우 같은 짜임: 윗줄 해('2011년'/'2025년 말') → 큰 결과('통장 바닥남' 도장/'2억 7천 남음') → 잔액 막대. 도장과 '1998년 시작' 사이에 해 줄을 끼움(외환위기 연상 막음)
    st = STAMP10.replace('left:96px;top:180px;font-size:70px', 'left:70px;top:174px;font-size:74px')
    Lc = card10(40, top, 560, ch, '#6B7280', '1998년 시작', '2011년', st, bar10(LOW / 3, '#D7261E', y=ch - 76))
    Rc = card10(680, top, 560, ch, '#2B6BE4', '2003년 시작', '2025년 말', LEFT10, bar10(LEFT / 3, '#0E7A3E', y=ch - 76))
    return bg + kick + l1 + l2 + Lc + Rc


KICK10 = "<div class='t' style='left:0;top:10px;width:1280px;text-align:center;font-size:54px;color:{c}'><span style='color:{a}'>월 200만원씩</span> 꺼내 쓴 S&amp;P500 퇴직금</div>"
# c2y 크림 · 두 줄: '같은 3억,'(작게) / '시작만 5년 차이'(크게, '5년' 빨강)
L1Y = "<div class='t' style='left:0;top:78px;width:1280px;text-align:center;font-size:86px;color:#1B2A4A'>같은 3억,</div>"
L2Y = "<div class='t' style='left:0;top:160px;width:1280px;text-align:center;font-size:122px;color:#1B2A4A'>시작만 <span style='color:#C8231B'>5년</span> 차이</div>"
V['c2y'] = g10(CREAM, KICK10.format(c='#1B2A4A', a='#C8231B'), L1Y, L2Y, top=306, ch=330)
# c2z 크림 · 한 줄(102px) + 카드 크게
L1Z = "<div class='t' style='left:0;top:84px;width:1280px;text-align:center;font-size:104px;color:#1B2A4A'>같은 3억, <span style='color:#C8231B'>시작만 5년 차이</span></div>"
V['c2z'] = g10(CREAM, KICK10.format(c='#1B2A4A', a='#C8231B'), L1Z, '', top=226, ch=380)
# c3a 남색(진한 판, 경쟁 노랑 강조 피함: 강조 하늘색) · c2y 짜임
NAVY = ("<div style='position:absolute;inset:0;background:radial-gradient(circle at 30% 12%,#2C4A86 0%,#18284D 55%,#0C1630 100%)'></div>"
        "<div style='position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.035) 0 3px,transparent 3px 12px)'></div>")
V['c3a'] = g10(NAVY, KICK10.format(c='#FFFFFF', a='#7FD3FF'), L1Y.replace('#1B2A4A', '#FFFFFF'),
               L2Y.replace("color:#1B2A4A'>시작만", "color:#FFFFFF'>시작만").replace('#C8231B', '#7FD3FF'), top=306, ch=330)
assert all('시작만' in V[k] and '5년' in V[k] for k in ('c2y', 'c2z', 'c3a'))
# 11차 — 10차 c2y(7.70: 제미나이 8.5·Claude 6.8·레드팀 7.8) 지적: '같은 3억,'이 절반 크기라 168px에서 '3억' 약함(레드팀) · 아래 빈자리 70px(레드팀)
#   · 결과(도장/2억 7천)를 더 크게(Claude·레드팀) · 띠 168px 흐림(Claude) · 크림이 피드에서 묻힘(Claude 8차) → c3c 채도 올린 크림
#   얼굴 넣기(Claude 제안)는 사장님 결정 '캐릭터 없이'·실제 인물 금지로 안 함
L1B = "<div class='t' style='left:0;top:70px;width:1280px;text-align:center;font-size:112px;color:#1B2A4A'>같은 3억,</div>"
L2B = "<div class='t' style='left:0;top:172px;width:1280px;text-align:center;font-size:126px;color:#1B2A4A'>시작만 <span style='color:#C8231B'>5년</span> 차이</div>"
KICKB = "<div class='t' style='left:0;top:6px;width:1280px;text-align:center;font-size:60px;color:{c}'><span style='color:{a}'>월 200만원씩</span> 꺼내 쓴 S&amp;P500 퇴직금</div>"


def g11(bg, top=308, ch=356):
    st = STAMP10.replace('left:96px;top:180px;font-size:70px', 'left:58px;top:164px;font-size:80px')
    Lc = card10(40, top, 560, ch, '#6B7280', '1998년 시작', '2011년', st, bar10(LOW / 3, '#D7261E', y=ch - 66)).replace('top:100px;width:560px;text-align:center;font-size:62px', 'top:94px;width:560px;text-align:center;font-size:58px')
    rv = "<div class='t' style='left:0;top:162px;width:560px;text-align:center;font-size:94px;color:#0E7A3E'>2억 7천<span style='font-size:64px;color:#14171C'> 남음</span></div>"
    Rc = card10(680, top, 560, ch, '#2B6BE4', '2003년 시작', '2025년 말', rv, bar10(LEFT / 3, '#0E7A3E', y=ch - 66)).replace('top:100px;width:560px;text-align:center;font-size:62px', 'top:94px;width:560px;text-align:center;font-size:58px')
    return bg + KICKB.format(c='#1B2A4A', a='#C8231B') + L1B + L2B + Lc + Rc


V['c3b'] = g11(CREAM)
V['c3c'] = g11("<div style='position:absolute;inset:0;background:#F6D58E'></div>")
# 12차 — 11차 Claude 독자 6.4('서류처럼'·글자 줄 6개·168px에서 작은 줄 뭉개짐) → 흰 카드·막대 없앰, 바탕 위에 결과 두 덩어리만 크게
#   레드팀 11차: 도장이 '1998년 시작' 바로 밑 → IMF 연상(중간) → 해를 결과와 같은 줄 앞에 둠('2011년' 위 작은 줄 아님) · '2011년'·'2025년 말' 키움
#   가운데 세로 선으로 좌우 가름, 해 머리표는 알약 대신 밑줄 글씨(경쟁 꼬리표 닮음 피함)
def side12(x, head, headc, when, res):
    return (f"<div class='t' style='left:{x}px;top:302px;width:600px;text-align:center;font-size:72px;color:{headc}'>{head}"
            f"<div style='margin:6px auto 0;width:300px;height:8px;background:{headc};border-radius:4px'></div></div>"
            f"<div class='t' style='left:{x}px;top:406px;width:600px;text-align:center;font-size:60px;color:#1B2A4A'>{when}</div>"
            f"<div class='t' style='left:{x}px;top:478px;width:600px;text-align:center;{res}</div>")


RES_L = "font-size:84px;color:#FFFFFF'><span style='display:inline-block;background:#D7261E;border-radius:14px;padding:2px 24px;transform:rotate(-4deg)'>통장 바닥남</span>"
RES_R = "font-size:92px;color:#0E7A3E'>2억 7천<span style='font-size:60px;color:#1B2A4A'> 남음</span>"
V['c3d'] = (CREAM + KICKB.format(c='#1B2A4A', a='#C8231B') + L1B + L2B
            + "<div style='position:absolute;left:638px;top:316px;width:4px;height:280px;background:#1B2A4A;opacity:.25'></div>"
            + side12(20, '1998년 시작', '#5B6270', '2011년', RES_L) + side12(660, '2003년 시작', '#2B6BE4', '2025년 말', RES_R))
# 13차 — 12차 레드팀: 막대는 차트일 뿐 주제 사물(통장) 0 → 카드를 펼친 통장으로(가운데 접힘선·왼쪽 묶음 구멍·줄 칸·머리 '…시작 통장')
#   P-1 좌우 카드 짜임 깨기: 두 통장을 서로 반대로 살짝 기울임 · 막대는 통장 맨 아래 '잔고' 칸으로
def passbook(x, y, w, h, cover, head, when, body, frac, col, rot):
    holes = ''.join(f"<div style='position:absolute;left:14px;top:{110 + i * 60}px;width:14px;height:14px;border-radius:7px;background:#C9CED8'></div>" for i in range(4))
    rows = ''.join(f"<div style='position:absolute;left:44px;top:{h * (0.47 + i * 0.12):.0f}px;width:{w - 70}px;height:2px;background:#E6E9EF'></div>" for i in range(4))
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);background:#FFFFFF;border-radius:12px;"
            f"box-shadow:0 12px 0 rgba(0,0,0,.28);overflow:hidden;border:3px solid {cover}'>"
            f"<div style='position:absolute;left:0;top:0;width:{w}px;height:84px;background:{cover}'></div>"
            f"<div class='t' style='left:0;top:10px;width:{w}px;text-align:center;font-size:62px;color:#FFFFFF'>{head}</div>{holes}{rows}"
            f"<div style='position:absolute;left:{w // 2}px;top:84px;width:0;height:{h - 84}px;border-left:3px dashed #D5D9E2'></div>"
            f"<div class='t' style='left:0;top:94px;width:{w}px;text-align:center;font-size:58px;color:#1B2A4A'>{when}</div>{body}"
            f"<div class='t' style='left:44px;top:{h - 70}px;font-size:34px;color:#5B6270'>잔고</div>"
            + bar10(frac, col, y=h - 72, x=124, w=w - 170, h=40) + "</div>")


def g13(bg):
    st = STAMP10.replace('left:96px;top:180px;font-size:70px', 'left:64px;top:162px;font-size:78px')
    rv = "<div class='t' style='left:0;top:160px;width:560px;text-align:center;font-size:92px;color:#0E7A3E'>2억 7천<span style='font-size:60px;color:#14171C'> 남음</span></div>"
    return (bg + KICKB.format(c='#1B2A4A', a='#C8231B') + L1B + L2B
            + passbook(40, 312, 560, 344, '#6B7280', '1998년 시작 통장', '2011년', st, LOW / 3, '#D7261E', -1.5)
            + passbook(680, 312, 560, 344, '#2B6BE4', '2003년 시작 통장', '2025년 말', rv, LEFT / 3, '#0E7A3E', 1.5))


V['c3e'] = g13(CREAM)
# 14차 (10/16 17시) — 13차 Claude '작은 글자 많아 지저분'(6.4)·레드팀 '구멍=수첩, 168px에선 통장 글자 덕만' → 글자 줄 6→4
#   구멍·줄 칸·'잔고' 글자 뺌 · 펼친 통장 = 가운데 굵은 제본선(그림자) · 남은 돈 = 통장 아래 쌓인 쪽 두께(왼쪽 얇게 2장, 오른쪽 두껍게 9장) — 막대 대신 사물
#   c3g는 띠(제목과 같은 말) 빼고 큰 글 키움 · c3h는 나무 책상 바탕(진한 판, 강조색은 빨강·초록 그대로라 경쟁 노랑과 다름)
def book14(x, y, w, h, cover, head, body, pages, rot):
    edges = ''.join(f"<div style='position:absolute;left:{x + 6 + i * 2}px;top:{y + h - 6 + i * 7}px;width:{w - 12 - i * 4}px;height:7px;background:#FBFAF6;"
                    f"border:1px solid #CFC8B8;border-radius:3px;transform:rotate({rot}deg)'></div>" for i in range(pages, 0, -1))
    return (edges + f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);background:#FFFFFF;border-radius:10px;"
            f"box-shadow:0 4px 0 rgba(0,0,0,.18);overflow:hidden;border:4px solid {cover}'>"
            f"<div style='position:absolute;left:0;top:0;width:{w}px;height:92px;background:{cover}'></div>"
            f"<div class='t' style='left:0;top:8px;width:{w}px;text-align:center;font-size:70px;color:#FFFFFF'>{head}</div>"
            f"<div style='position:absolute;left:{w // 2 - 18}px;top:92px;width:36px;height:{h - 92}px;background:linear-gradient(90deg,rgba(0,0,0,0),rgba(0,0,0,.16) 45%,rgba(0,0,0,.30) 50%,rgba(0,0,0,.16) 55%,rgba(0,0,0,0))'></div>"
            f"{body}</div>")


ST14 = ("<div class='t' style='left:0;top:110px;width:{w}px;text-align:center;font-size:58px;color:#1B2A4A'>2011년</div>"
        "<div class='t' style='left:0;top:174px;width:{w}px;text-align:center;font-size:88px;color:#FFFFFF'><span style='display:inline-block;background:#D7261E;border-radius:14px;padding:0 26px;transform:rotate(-5deg)'>통장 바닥남</span></div>")
RV14 = ("<div class='t' style='left:0;top:110px;width:{w}px;text-align:center;font-size:58px;color:#1B2A4A'>2025년 말</div>"
        "<div class='t' style='left:0;top:168px;width:{w}px;text-align:center;font-size:100px;color:#0E7A3E'>2억 7천<span style='font-size:62px;color:#14171C'> 남음</span></div>")


def g14(bg, kick=True, top=318, ch=290, l1=L1B, l2=L2B):
    w = 560
    return (bg + (KICKB.format(c='#1B2A4A', a='#C8231B') if kick else '') + l1 + l2
            + book14(40, top, w, ch, '#6B7280', '1998년 시작', ST14.format(w=w), 2, -1.5)
            + book14(680, top - 30, w, ch, '#2B6BE4', '2003년 시작', RV14.format(w=w), 9, 1.5))


V['c3f'] = g14(CREAM)
L1G = "<div class='t' style='left:0;top:14px;width:1280px;text-align:center;font-size:124px;color:#1B2A4A'>같은 3억,</div>"
L2G = "<div class='t' style='left:0;top:134px;width:1280px;text-align:center;font-size:140px;color:#1B2A4A'>시작만 <span style='color:#C8231B'>5년</span> 차이</div>"
V['c3g'] = g14(CREAM, kick=False, top=322, l1=L1G, l2=L2G)
WOOD = ("<div style='position:absolute;inset:0;background:linear-gradient(180deg,#6B4A2E,#4E3420)'></div>"
        "<div style='position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.04) 0 2px,transparent 2px 9px,rgba(0,0,0,.06) 9px 11px,transparent 11px 23px)'></div>")
V['c3h'] = g14(WOOD, kick=False, top=322, l1=L1G.replace('#1B2A4A', '#FFF6E6'),
               l2=L2G.replace("color:#1B2A4A'>시작만", "color:#FFF6E6'>시작만").replace('#C8231B', '#FF5A4A'))
# c3i — 14차 제미나이: 막대 있는 c3e 8.5 > 막대 뺀 c3f 7.5('잔고 게이지가 결과를 먼저 보여 줌') → c3f에 막대만 되살림('잔고' 글자 없이)
def g14i(bg, top=306, ch=336):
    w = 560
    stl = ST14.format(w=w).replace('top:110px', 'top:100px').replace('top:174px', 'top:156px')
    rvr = RV14.format(w=w).replace('top:110px', 'top:100px').replace('top:168px', 'top:150px')
    return (bg + KICKB.format(c='#1B2A4A', a='#C8231B') + L1B + L2B
            + book14(40, top, w, ch, '#6B7280', '1998년 시작', stl + bar10(LOW / 3, '#D7261E', y=ch - 62, x=50, w=w - 100, h=38), 2, -1.5)
            + book14(680, top - 24, w, ch, '#2B6BE4', '2003년 시작', rvr + bar10(LEFT / 3, '#0E7A3E', y=ch - 62, x=50, w=w - 100, h=38), 7, 1.5))


V['c3i'] = g14i(CREAM)
# 15차 — 14차 세 명 모두 c3e 1위(제미나이 8.5·Claude 6.5): 막대가 결과를 먼저 보여 줌, 두께·제본선은 168px에서 안 보임
#   Claude·제미나이 같은 지적: 위 띠('월 200만원씩…')가 168px에서 사라져 '무슨 3억인지' 모름 → 띠를 남색 띠 위 흰 글 72px로 키움
#   c3e 구멍(레드팀 '수첩 신호') 뺌 · c3k는 같은 판 나무 책상(14차 c3h: 제미나이 8.2, Claude '진한 바탕 대비 유지')
KICK15 = ("<div style='position:absolute;left:0;top:0;width:1280px;height:96px;background:{band}'></div>"
          "<div class='t' style='left:0;top:6px;width:1280px;text-align:center;font-size:72px;color:#FFFFFF'><span style='color:{a}'>월 200만원씩</span> 꺼내 쓴 S&amp;P500 퇴직금</div>")
L1J = "<div class='t' style='left:0;top:104px;width:1280px;text-align:center;font-size:110px;color:{c}'>같은 3억, <span style='font-size:122px'>시작만 <span style='color:{r}'>5년</span> 차이</span></div>"


def g15(bg, band, a, c, r):
    st = STAMP10.replace('left:96px;top:180px;font-size:70px', 'left:64px;top:162px;font-size:78px')
    rv = "<div class='t' style='left:0;top:160px;width:560px;text-align:center;font-size:92px;color:#0E7A3E'>2억 7천<span style='font-size:60px;color:#14171C'> 남음</span></div>"
    out = (bg + KICK15.format(band=band, a=a) + L1J.format(c=c, r=r)
           + passbook(40, 300, 560, 360, '#6B7280', '1998년 시작 통장', '2011년', st, LOW / 3, '#D7261E', -1.5)
           + passbook(680, 300, 560, 360, '#2B6BE4', '2003년 시작 통장', '2025년 말', rv, LEFT / 3, '#0E7A3E', 1.5))
    return re.sub(r"<div style='position:absolute;left:14px;top:d+px;width:14px;height:14px;border-radius:7px;background:#C9CED8'></div>", '', out)


V['c3j'] = g15(CREAM, '#1B2A4A', '#FFD0C8', '#1B2A4A', '#C8231B')
V['c3k'] = g15(WOOD, '#1B2A4A', '#FFD0C8', '#FFF6E6', '#FF5A4A')
# 16차 — 15차 c3j(제미나이 8.5·Claude 6·레드팀 7.4): 레드팀 '바닥남=0원 오독 → 남은 돈 1,154만원(calc 161줄) 보탬'·'P-1 좌우 대칭 짜임 겹침 3 → 대칭 깸'
#   '잔고' 글자 2개(168px 안 읽힘) 뺌 · 왼쪽 빈 막대 안에 '남은 돈 1,154만원' · 오른쪽 통장을 더 크고 높게(왼 520·오 610)
assert '마지막 해 남은 돈 1,154만원' in calc


def g16(bg):
    st = STAMP10.replace('left:96px;top:180px;font-size:70px', 'left:44px;top:162px;font-size:78px')
    rv = "<div class='t' style='left:0;top:156px;width:610px;text-align:center;font-size:104px;color:#0E7A3E'>2억 7천<span style='font-size:64px;color:#14171C'> 남음</span></div>"
    Lb = passbook(36, 316, 520, 344, '#6B7280', '1998년 시작 통장', '2011년', st, LOW / 3, '#D7261E', -1.5)
    Lb = Lb.replace("color:#5B6270'>잔고</div>", "color:#5B6270'></div>")
    i = Lb.rindex('</div></div></div>')
    Lb = Lb[:i] + "</div></div><div class='t' style='left:150px;top:274px;font-size:34px;color:#3A4150'>남은 돈 1,154만원</div></div>"
    Rb = passbook(626, 286, 610, 374, '#2B6BE4', '2003년 시작 통장', '2025년 말', rv, LEFT / 3, '#0E7A3E', 1.5).replace("color:#5B6270'>잔고</div>", "color:#5B6270'></div>")
    out = bg + KICK15.format(band='#1B2A4A', a='#FFD0C8') + L1J.format(c='#1B2A4A', r='#C8231B') + Lb + Rb
    return re.sub(r"<div style='position:absolute;left:14px;top:d+px;width:14px;height:14px;border-radius:7px;background:#C9CED8'></div>", '', out)


V['c3l'] = g16(CREAM)
for k in V: V[k] = V[k].replace("<span style='display:none'></span'></div>", "</div>")
assert all('같은 3억' in v and '0원' not in v and '정우' not in v for v in V.values())


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")


if __name__ == '__main__':
    keys = sys.argv[1].split(',') if len(sys.argv) > 1 else list(V)
    import numpy as n
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k in keys:
            html = os.path.join(HERE, f'{k}.html'); open(html, 'w', encoding='utf-8').write(HEAD + V[k] + '\n' + TAIL)
            pg.goto('file:///' + html.replace(chr(92), '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out); im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            a = n.asarray(im.convert('L'), float)
            print(k, os.path.getsize(out) // 1024, 'KB 명암폭', round(a.std()), '가려짐:', check_zones(pg) or '없음')
        b.close()
