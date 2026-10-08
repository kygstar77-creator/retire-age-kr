# C-1 'S&P500 3억 배당 vs 매도, 몇 년 버티나' 썸네일 시안(2026-10-08 visual-designer) — py -3.12 make_thumbs.py [c1a,c1b,...]
# ※ 14:0x 문구 바뀜: titles.md 13:58 개정(예술가 뻔함 반려 13:54) — 1위 썸네일 = '1997년 시작: 아직 남음 / 1998년: 11년째 바닥'
#   작은 줄 '원화 계산 · 3억 · 월 200만원 · 배당으로 받기' → 아래 '4차' c1h~c1j. c1a~c1g(옛 문구 2000년 9·11년)는 심사 기록용 보관, 쓰지 않음.
# (옛) 문구: ep/C-1/copy/titles.md 1위 썸네일 '배당 9년 · 매도 11년' / 작은 줄 '2000년 시작 · 3억 · 월 200만원'(copywriter 13:48, 결선 8.50).
#   조건 '2000년 시작·배당 쪽'을 떼지 않는다(titles.md 꼭 지킬 것). 2008년 5.27억(원화)·'평생'·상품명 안 씀.
# 숫자: ep/C-1/calc_out.txt 4)·6)에서 읽고 assert — 잔액 선은 6) '해마다 연말 잔액(3억원·월 200만원)' 2000년 시작 A·B 그대로.
# 경쟁과 다른 점: 경쟁 5 = 그림 인물·실사 얼굴·아래 두 줄 노랑/흰 테두리 글씨. 우리 = 얼굴·그림·테두리 0, 실제 잔액 선 두 개가 0에 닿는 해.
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576, 아래 5%(y≥684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'C-1')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
m = re.search(r'월 200만원 · 2000년 시작: A (\d+)년차 바닥 \| B (\d+)년차 바닥', calc)
YA, YB = int(m.group(1)), int(m.group(2))
assert (YA, YB) == (9, 11), (YA, YB)  # titles.md 문구와 같아야 함


def bal(mode):
    s = re.search(rf'2000년 시작 {mode}: (.+)', calc).group(1)
    return [3.0] + [float(x.split(':')[1]) for x in s.split()]


A, B = bal('A'), bal('B')
assert A[-1] == 0 and B[-1] == 0 and len(A) - 1 == YA and len(B) - 1 == YB, (A, B)

INK, RED, NAVY, GREY, CREAM = '#16181D', '#E5322D', '#1E2A44', '#6B7280', '#F3EEE3'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
SUB = '2000년 시작 · 3억 · 월 200만원'
FINE = 'S&amp;P500 총수익지수·원화 환산, 2000년부터 실제 연도 순서 · 세금·건보료 반영 · 지나간 값 · 투자 권유 아님'


def lines(x0, y0, w, h, yrs=12, lw=12, ca=RED, cb=NAVY):
    """두 사람 잔액 선(3억 → 0). x = 지난 해 수(0~yrs), y = 억원(0~3). (svg, A 바닥 좌표, B 바닥 좌표, 시작 좌표)"""
    X = lambda i: x0 + w * i / yrs
    Y = lambda v: y0 + h * (1 - v / 3.0)
    P = lambda vs: ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(vs))
    s = (f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
         f"<line x1='{x0}' y1='{Y(0):.1f}' x2='{x0 + w}' y2='{Y(0):.1f}' stroke='#9AA0AA' stroke-width='4'/>"
         f"<polyline points='{P(B)}' fill='none' stroke='{cb}' stroke-width='{lw}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<polyline points='{P(A)}' fill='none' stroke='{ca}' stroke-width='{lw + 2}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<circle cx='{X(YA):.1f}' cy='{Y(0):.1f}' r='{lw * 1.8}' fill='{ca}' stroke='#fff' stroke-width='6'/>"
         f"<circle cx='{X(YB):.1f}' cy='{Y(0):.1f}' r='{lw * 1.8}' fill='{cb}' stroke='#fff' stroke-width='6'/></svg>")
    return s, (X(YA), Y(0)), (X(YB), Y(0)), (X(0), Y(3))


# c1a — 밝은 크림 판(우리 조회 1위 A-1 계열) + 오른쪽 실제 잔액 선 두 개, 왼쪽 큰 두 줄(빨강 '배당 9년' / 남색 '매도 11년')
_s, pa, pb, p0 = lines(660, 180, 560, 380, lw=14)
c1a = f"""<div style='position:absolute;inset:0;background:{CREAM}'></div>
{_s}
<div class='lab' style='left:{p0[0] + 26:.0f}px;top:{p0[1] - 30:.0f}px;font-size:40px;color:{INK}'>3억</div>
<div class='lab' style='left:{p0[0]:.0f}px;top:{pa[1] + 14:.0f}px;font-size:36px;color:{GREY}'>0원</div>
<div id='a0' class='t' data-fit='1180' style='left:48px;top:44px;font-size:52px;color:{INK};font-family:PD;font-weight:700'>S&amp;P500 · {SUB}</div>
<div id='a1' class='t' data-fit='590' style='left:44px;top:150px;font-size:200px;color:{RED}'>배당 9년</div>
<div id='a2' class='t' data-fit='640' style='left:44px;top:380px;font-size:150px;color:{NAVY}'>매도 11년</div>
<div class='fine' style='color:{GREY};top:640px;font-size:20px'>{FINE}</div>
"""


# c1b — 남색 판 + 두 사람 '통장 막대'(해마다 한 칸, 바닥난 해에서 ✕) — 시간 경주 그림, 큰 두 줄
def bars(x0, y0, cw, ch, gap, vs, col):
    out = ''
    for i in range(1, len(vs)):
        v = vs[i]
        x = x0 + (i - 1) * (cw + gap)
        if v > 0:
            hh = max(6, ch * v / 3.0)
            out += f"<div style='position:absolute;left:{x}px;top:{y0 + ch - hh:.0f}px;width:{cw}px;height:{hh:.0f}px;background:{col};border-radius:6px'></div>"
        else:
            out += f"<div class='t' style='left:{x - 8}px;top:{y0 + ch - 58}px;font-size:60px;color:{col}'>✕</div>"
    return out


c1b = f"""<div style='position:absolute;inset:0;background:{NAVY}'></div>
<div id='b0' class='t' data-fit='1180' style='left:48px;top:40px;font-size:50px;color:#C9D3E6;font-family:PD;font-weight:700'>S&amp;P500 · {SUB}</div>
<div id='b1' class='t' data-fit='540' style='left:44px;top:140px;font-size:150px;color:#FF5A4E'>배당 9년</div>
<div id='b2' class='t' data-fit='540' style='left:44px;top:350px;font-size:150px;color:#fff'>매도 11년</div>
{bars(630, 140, 42, 170, 8, A, '#FF5A4E')}
{bars(630, 370, 42, 170, 8, B, '#fff')}
<div style='position:absolute;left:630px;top:338px;width:550px;border-top:3px solid #4A5878'></div>
<div class='fine' style='color:#AEB6C6;top:640px;font-size:20px'>{FINE}</div>
"""

# c1c — 흰 판 + 넓은 잔액 선(그림이 주인공), 위 한 줄 문구, 바닥 점마다 큰 라벨
_s2, pa2, pb2, p02 = lines(70, 220, 1080, 320, lw=14)
c1c = f"""<div style='position:absolute;inset:0;background:#FBFAF7'></div>
{_s2}
<div id='c0' class='t' data-fit='1180' style='left:44px;top:30px;font-size:46px;color:{GREY};font-family:PD;font-weight:700'>S&amp;P500 {SUB}</div>
<div class='lab' style='left:{p02[0] - 4:.0f}px;top:{p02[1] - 60:.0f}px;font-size:44px;color:{INK}'>3억</div>
<div id='c1' class='t' style='left:{pa2[0] - 400:.0f}px;top:{pa2[1] - 300:.0f}px;font-size:150px;color:{RED}'>배당 9년</div>
<div id='c2' class='t' style='left:{pb2[0] - 200:.0f}px;top:{pb2[1] - 150:.0f}px;font-size:76px;color:{NAVY}'>매도 11년</div>
<div class='fine' style='color:{GREY};top:640px;font-size:20px'>{FINE}</div>
"""
VARIANTS = {'c1a': c1a, 'c1b': c1b, 'c1c': c1c}

# ── 2차 — 1차 세 명 평균 c1a 6.83(제미나이 7.5·7.5 / Claude 7.0 / 레드팀 6) · c1b 6.18(레드팀 겹침 3 반려) · c1c 6.0. 7 넘은 안 없음.
#    168px에서 우리 판이 경쟁보다 흐림(연한 바탕·가는 선) → 흰 바탕, 선 굵게.
#    레드팀: 168px에서 조건 줄이 안 읽혀 '배당 9년'만 남음(titles.md 꼭 지킬 것 1) → '2000년 시작' 남색 알약 72px을 큰 글씨 바로 위로.
#            '9년→0원'이 안 붙음 → 빨간 점 옆 '0원' 빨강 64px. 각주에 '같은 S&P500·꺼내는 방식만 다름'(배당 ETF 비교로 오독 방지), 종합과세 추가세 제외 명시.
#    Claude: 반전(평균이면 안 떨어짐)이 그림에 없음 → 회색 점선 '평균이면'.
#    평균 선 = calc_out 첫 줄 원화 기하평균 + 2) 월 200만원 A 분배액으로 A를 매년 같은 수익률로 돌린 값(오름 — calc_out 1) '100년+'와 같은 방향).
FINE2A = '같은 S&amp;P500 총수익지수에서 꺼내는 방식만 다름 · 원화 환산 · 2000년부터 실제 연도 순서'
FINE2B = '미국 배당세·양도세·지역 건보료 반영(종합과세 추가세 제외) · 지나간 값 · 투자 권유 아님'
G = float(re.search(r'원화 (\d+\.\d+)%', calc).group(1)) / 100
GROSS = int(re.search(r'월 200만원\(연 24,000,000원\): A 분배 ([\d,]+)원', calc).group(1).replace(',', ''))
AVG = [3.0]
for _ in range(11):
    AVG.append((AVG[-1] * 1e8 - GROSS) * (1 + G) / 1e8)
assert AVG[-1] > 3.0 and re.search(r'3\.00억원 · 월 200만원: 세금 빼기 전 100년\+ \| A 배당 세금\+건보 100년\+', calc)


def lines2(x0, y0, w, h, yrs=12, top=4.4, lw=20):
    X = lambda i: x0 + w * i / yrs
    Y = lambda v: y0 + h * (1 - v / top)
    P = lambda vs: ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(vs))
    s = (f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
         f"<line x1='{x0}' y1='{Y(0):.1f}' x2='{x0 + w}' y2='{Y(0):.1f}' stroke='#9AA0AA' stroke-width='5'/>"
         f"<polyline points='{P(AVG)}' fill='none' stroke='#A9AFBA' stroke-width='{lw - 6}' stroke-dasharray='2 24' stroke-linecap='round'/>"
         f"<polyline points='{P(B)}' fill='none' stroke='{NAVY}' stroke-width='{lw}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<polyline points='{P(A)}' fill='none' stroke='{RED}' stroke-width='{lw + 2}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<circle cx='{X(YA):.1f}' cy='{Y(0):.1f}' r='26' fill='{RED}' stroke='#fff' stroke-width='7'/>"
         f"<circle cx='{X(YB):.1f}' cy='{Y(0):.1f}' r='26' fill='{NAVY}' stroke='#fff' stroke-width='7'/></svg>")
    return s, X, Y


PILL = lambda x, y, fs, txt: (f"<div class='t' style='left:{x}px;top:{y}px;font-size:{fs}px;color:#fff;background:{NAVY};"
                              f"padding:10px 22px 12px;border-radius:999px;font-family:PD;font-weight:700'>{txt}</div>")

# c1d — c1a 고침: 흰 바탕, '2000년 시작' 알약, 선 굵게 + 점선 '평균이면', 빨간 '0원', 남색 끝점 길이 자리에서 왼쪽
_s4, X4, Y4 = lines2(640, 130, 500, 420)
c1d = f"""<div style='position:absolute;inset:0;background:#fff'></div>
{_s4}
<div class='lab' style='left:{X4(0) - 20:.0f}px;top:{Y4(3) - 70:.0f}px;font-size:44px;color:{INK}'>3억</div>
<div class='lab' style='left:{X4(7.0):.0f}px;top:{Y4(AVG[8]) - 84:.0f}px;font-size:40px;color:#8A909C'>평균이면</div>
<div class='t' style='left:{X4(YA) - 190:.0f}px;top:{Y4(0) + 6:.0f}px;font-size:64px;color:{RED}'>0원</div>
{PILL(40, 34, 64, '2000년 시작')}
<div class='t' style='left:448px;top:50px;font-size:46px;color:{INK};font-family:PD;font-weight:700'>3억 · 월 200만원</div>
<div id='d1' class='t' data-fit='570' style='left:36px;top:180px;font-size:200px;color:{RED}'>배당 9년</div>
<div id='d2' class='t' data-fit='570' style='left:36px;top:410px;font-size:160px;color:{NAVY}'>매도 11년</div>
<div class='fine' style='color:{GREY};top:606px;font-size:18px'>{FINE2A}</div>
<div class='fine' style='color:{GREY};top:634px;font-size:18px'>{FINE2B}</div>
"""

# c1e — 큰 글자 한 줄 전폭 + 알약, 그림을 아래 넓게(점선 평균 vs 실제 두 선)
_s5, X5, Y5 = lines2(70, 250, 820, 290, lw=18)
c1e = f"""<div style='position:absolute;inset:0;background:#fff'></div>
{_s5}
{PILL(40, 28, 60, '2000년 시작 · 3억 · 월 200만원')}
<div id='e0' class='t' data-fit='1190' style='left:36px;top:128px;font-size:150px;color:{RED}'>배당 9년 <span style='color:{NAVY}'>· 매도 11년</span></div>
<div class='lab' style='left:{X5(9.4):.0f}px;top:{Y5(AVG[11]) + 18:.0f}px;font-size:40px;color:#8A909C'>평균이면</div>
<div class='t' style='left:{X5(YA) - 150:.0f}px;top:{Y5(0) + 4:.0f}px;font-size:60px;color:{RED}'>0원</div>
<div class='fine' style='color:{GREY};top:620px;font-size:18px'>{FINE2A}</div>
<div class='fine' style='color:{GREY};top:646px;font-size:18px'>{FINE2B}</div>
"""
VARIANTS.update(c1d=c1d, c1e=c1e)

# ── 3차 — 2차: 제미나이 c1a 7.5·7.5 / c1d 6.5·6.5 / c1e 6.0·6.0(점선이 무게 중심을 흐림) · Claude c1a 5.8 / c1d 6.5 / c1e 7.1(점선 '평균'과 0원 선이 갈라지는 반전이 1초에 읽힘).
#    두 심사가 반대 → 둘 다 받는 처방만: 알약에 'S&P500'(검색어·신뢰), 점선은 굵고 진하게(168px에서 '흐린 잡음'이 아니게), 각주 1줄, '0원' 키움.
#    c1f = c1e 고침(한 줄 전폭 + 넓은 그림) · c1g = c1a 배치(왼쪽 큰 두 줄 — 제미나이 1위) + 오른쪽 그림에 굵은 평균 선.
FINE3 = '같은 S&amp;P500 총수익지수·꺼내는 방식만 다름 · 원화·실제 연도 순서 · 세금·건보료 반영 · 투자 권유 아님'


def lines3(x0, y0, w, h, yrs=12, top=4.4, lw=20):
    X = lambda i: x0 + w * i / yrs
    Y = lambda v: y0 + h * (1 - v / top)
    P = lambda vs: ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(vs))
    s = (f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
         f"<line x1='{x0}' y1='{Y(0):.1f}' x2='{x0 + w}' y2='{Y(0):.1f}' stroke='#9AA0AA' stroke-width='5'/>"
         f"<polyline points='{P(AVG)}' fill='none' stroke='#7C8494' stroke-width='{lw}' stroke-dasharray='1 34' stroke-linecap='round'/>"
         f"<polyline points='{P(B)}' fill='none' stroke='{NAVY}' stroke-width='{lw}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<polyline points='{P(A)}' fill='none' stroke='{RED}' stroke-width='{lw + 2}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<circle cx='{X(YA):.1f}' cy='{Y(0):.1f}' r='26' fill='{RED}' stroke='#fff' stroke-width='7'/>"
         f"<circle cx='{X(YB):.1f}' cy='{Y(0):.1f}' r='26' fill='{NAVY}' stroke='#fff' stroke-width='7'/></svg>")
    return s, X, Y


_s6, X6, Y6 = lines3(70, 250, 820, 300, lw=20)
c1f = f"""<div style='position:absolute;inset:0;background:#fff'></div>
{_s6}
{PILL(40, 26, 56, 'S&amp;P500 3억 · 월 200만원 · 2000년 시작')}
<div id='f0' class='t' data-fit='1190' style='left:36px;top:122px;font-size:150px;color:{RED}'>배당 9년 <span style='color:{NAVY}'>· 매도 11년</span></div>
<div class='lab' style='left:{X6(9.3):.0f}px;top:{Y6(AVG[11]) + 18:.0f}px;font-size:46px;color:#5F6675'>평균이면</div>
<div class='t' style='left:{X6(YA) - 170:.0f}px;top:{Y6(0) + 4:.0f}px;font-size:72px;color:{RED}'>0원</div>
<div class='fine' style='color:#9AA0AA;top:648px;font-size:18px'>{FINE3}</div>
"""

_s7, X7, Y7 = lines3(640, 150, 500, 400)
c1g = f"""<div style='position:absolute;inset:0;background:#fff'></div>
{_s7}
{PILL(40, 30, 54, 'S&amp;P500 3억 · 월 200만원 · 2000년 시작')}
<div class='lab' style='left:{X7(6.6):.0f}px;top:{Y7(AVG[8]) - 88:.0f}px;font-size:44px;color:#5F6675'>평균이면</div>
<div class='t' style='left:{X7(YA) - 200:.0f}px;top:{Y7(0) + 6:.0f}px;font-size:72px;color:{RED}'>0원</div>
<div id='g1' class='t' data-fit='570' style='left:36px;top:170px;font-size:200px;color:{RED}'>배당 9년</div>
<div id='g2' class='t' data-fit='570' style='left:36px;top:400px;font-size:160px;color:{NAVY}'>매도 11년</div>
<div class='fine' style='color:#9AA0AA;top:648px;font-size:18px'>{FINE3}</div>
"""
VARIANTS.update(c1f=c1f, c1g=c1g)

# ── 4차(14:0x) — 새 문구(titles.md 13:58). 선 = paths9798.json(calc.py path()를 그대로 돌린 3억·월 200만원 배당(A) 1997·1998년 시작 연말 잔액,
#    calc_out 3) '1997:29+ 1998:11'과 assert). 1997은 첫해 환율(844.2→1,415.2원)로 6억까지 뛴다 — 그래서 작은 줄 '원화 계산'을 떼지 않는다.
#    1998 선은 11번째 해에 0, 1997 선은 2025년(29년째) 자료 끝까지 남음 → 같은 가로 눈금(29년)에 그대로 그린다(잘라서 과장하지 않음).
#    옛 차수에서 배운 것: 168px에서 조건 알약은 읽힘(레드팀 +1), 각주 2줄은 회색 띠(Claude·레드팀) → 1줄. '0원'은 빨강 큰 글씨.
P97 = json.load(open(os.path.join(HERE, 'paths9798.json')))
Y97, Y98 = [3.0] + P97['1997'], [3.0] + P97['1998']
assert Y98[-1] == 0 and len(Y98) - 1 == 11 and Y97[-1] > 0 and len(Y97) - 1 == 29
assert re.search(r'3\.00억원 · 월 200만원 · A: .* 1997:29\+ 1998:11 ', calc)
GREEN = '#0F7B5F'
SUB4 = '원화 계산 · 3억 · 월 200만원 · 배당으로 받기'
FINE4 = 'S&amp;P500 총수익지수 · 원화(ECOS 연말 환율) · 1997·1998년부터 실제 연도 순서 · 세금·건보료 반영 · 2025년까지 · 투자 권유 아님'


def lines4(x0, y0, w, h, top=7.0, lw=16, end_dot=True):
    X = lambda i: x0 + w * i / 29
    Y = lambda v: y0 + h * (1 - v / top)
    P = lambda vs: ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(vs))
    s = (f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
         f"<line x1='{x0}' y1='{Y(0):.1f}' x2='{x0 + w}' y2='{Y(0):.1f}' stroke='#9AA0AA' stroke-width='5'/>"
         f"<polyline points='{P(Y97)}' fill='none' stroke='{GREEN}' stroke-width='{lw}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<polyline points='{P(Y98)}' fill='none' stroke='{RED}' stroke-width='{lw + 4}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<circle cx='{X(11):.1f}' cy='{Y(0):.1f}' r='24' fill='{RED}' stroke='#fff' stroke-width='7'/>")
    if end_dot:
        s += f"<circle cx='{X(29):.1f}' cy='{Y(Y97[-1]):.1f}' r='18' fill='{GREEN}' stroke='#fff' stroke-width='6'/>"
    return s + '</svg>', X, Y


# c1h — 위 큰 두 줄(문구 그대로, '11년'만 가장 크게) + 아래 넓은 그림(같은 29년 눈금)
_s8, X8, Y8 = lines4(60, 372, 1150, 230)
c1h = f"""<div style='position:absolute;inset:0;background:#fff'></div>
{_s8}
<div id='h1' class='t' data-fit='1190' style='left:36px;top:26px;font-size:104px;color:{GREEN}'>1997년 시작: 아직 남음</div>
<div id='h2' class='t' data-fit='1190' style='left:36px;top:148px;font-size:104px;color:{RED}'>1998년: <span style='font-size:150px'>11년</span>째 바닥</div>
<div class='t' style='left:{X8(11) + 34:.0f}px;top:{Y8(0) - 66:.0f}px;font-size:56px;color:{RED}'>0원</div>
<div class='t' style='left:44px;top:322px;font-size:38px;color:{INK};font-family:PD;font-weight:700'>{SUB4}</div>
<div class='fine' style='color:#9AA0AA;top:650px;font-size:17px'>{FINE4}</div>
"""

# c1i — 그림이 주인공: 선 끝에 바로 라벨(1997 녹색 오른쪽 위 '아직 남음', 1998 빨강 0원 점 옆 '11년째 바닥'), 위 알약 한 줄
_s9, X9, Y9 = lines4(60, 130, 1080, 330, lw=16)
c1i = f"""<div style='position:absolute;inset:0;background:#fff'></div>
{_s9}
{PILL(40, 26, 50, SUB4)}
<div id='i1' class='t' data-fit='620' style='left:560px;top:104px;font-size:80px;color:{GREEN}'>1997년 시작: 아직 남음</div>
<div id='i2' class='t' data-fit='760' style='left:{X9(11) + 36:.0f}px;top:{Y9(0) + 16:.0f}px;font-size:84px;color:{RED}'>1998년: 11년째 바닥</div>
<div class='fine' style='color:#9AA0AA;top:650px;font-size:17px'>{FINE4}</div>
"""

# c1j — 크림 판(우리 조회 1위 A-1 계열, G-1 g1f 승리 틀) + 왼쪽 큰 네 줄 + 오른쪽 그림(앞 15년만이 아니라 29년 전체를 좁게)
_s10, X10, Y10 = lines4(700, 120, 520, 400, lw=14)
c1j = f"""<div style='position:absolute;inset:0;background:{CREAM}'></div>
{_s10}
<div class='t' style='left:40px;top:34px;font-size:84px;color:{GREEN}'>1997년 시작</div>
<div class='t' style='left:40px;top:128px;font-size:96px;color:{GREEN}'>아직 남음</div>
<div class='t' style='left:40px;top:278px;font-size:84px;color:{RED}'>1998년</div>
<div id='j4' class='t' data-fit='640' style='left:36px;top:372px;font-size:150px;color:{RED}'>11년째 바닥</div>
<div class='t' style='left:{X10(11) + 30:.0f}px;top:{Y10(0) - 64:.0f}px;font-size:52px;color:{RED}'>0원</div>
<div class='t' style='left:44px;top:566px;font-size:34px;color:{INK};font-family:PD;font-weight:700'>{SUB4}</div>
<div class='fine' style='color:{GREY};top:650px;font-size:17px'>{FINE4}</div>
"""
VARIANTS.update(c1h=c1h, c1i=c1i, c1j=c1j)

# ── 5차 — 4차: 제미나이 c1h 6.25 / c1i 6.5 / c1j 7.0 · Claude 6.2 / 5.3 / 6.7(1위 c1j — 빨간 '11년째 바닥'+0원 점이 1초에 걸림).
#    Claude 처방: 연한 바탕이 경쟁 옆에서 꺼짐 → 대비↑, 그림 폭 55% 이상·선 굵게, 녹색 '아직 남음'을 빨강과 같은 크기, 작은 줄 굵게.
#    레드팀 4차(c1j 7): '0원'은 카피에 없는 말이고 10년 말 0.09억 남음(11년째 필요한 돈 부족) → 뺀다. 크게는 '11년' 하나(titles.md) → '째 바닥' 작게. 작은 줄은 50px 진한 알약.
#    c1k = c1j + 진한 크림(g1f #EFE4CC)·그림 넓게·선 22·두 갈래 같은 크기·작은 줄 남색 알약 · c1l = 같은 배치를 어두운 판(M-1 m1i처럼 어두운 판이 이긴 적 있음).
def c1kl(bg, green, red, ink, sub_bg, sub_fg, fine):
    s, X, Y = lines4(610, 96, 630, 404, lw=22)
    s = s.replace(GREEN, green).replace(RED, red)
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
{s}
<div class='t' style='left:40px;top:30px;font-size:70px;color:{green}'>1997년 시작</div>
<div id='k2' class='t' data-fit='510' style='left:36px;top:104px;font-size:124px;color:{green}'>아직 남음</div>
<div class='t' style='left:40px;top:270px;font-size:70px;color:{red}'>1998년</div>
<div id='k4' class='t' data-fit='510' style='left:36px;top:340px;font-size:150px;color:{red}'>11년<span style='font-size:96px'>째 바닥</span></div>
<div id='k5' class='t' data-fit='900' style='left:36px;top:548px;font-size:46px;color:{sub_fg};background:{sub_bg};padding:8px 18px 10px;border-radius:999px;font-family:PD;font-weight:700'>{SUB4}</div>
<div class='fine' style='color:{fine};top:656px;font-size:16px'>{FINE4}</div>
"""


c1k = c1kl('#EFE4CC', GREEN, RED, INK, NAVY, '#fff', GREY)
c1l = c1kl('#141B26', '#2FD39A', '#FF5A4E', '#fff', '#fff', '#141B26', '#8C95A6')
VARIANTS.update(c1k=c1k, c1l=c1l)

# ── 6차 — 5차: 제미나이 c1j 5·6.5 / c1k 6·7.5 / c1l 7.5·8.0 · Claude 6.9 / 6.2 / 7.1(1위 c1l).
#    실측: data-fit이 '11년째 바닥'을 116px로 줄여 녹색 '아직 남음'(124px)보다 작았다 — 강조가 거꾸로(Claude). → 녹색 96px, 빨강 '11년' 170px·'째 바닥' 80px.
#    빨강 선 +6·끝점 키움, 작은 줄 알약 52px로 키워 왼쪽에. 배경 = c1l 어두운 판(겹침: Claude 2 — 검정 글씨판·'3억', 상한 안).
def c1m_html():
    s, X, Y = lines4(620, 96, 620, 404, lw=22)
    s = s.replace(GREEN, '#2FD39A').replace(RED, '#FF5A4E')
    a, b = "stroke='#FF5A4E' stroke-width='26'", "r='24' fill='#FF5A4E'"
    assert a in s and b in s
    s = s.replace(a, "stroke='#FF5A4E' stroke-width='32'").replace(b, "r='32' fill='#FF5A4E'")
    return f"""<div style='position:absolute;inset:0;background:#141B26'></div>
{s}
<div class='t' style='left:40px;top:34px;font-size:64px;color:#2FD39A'>1997년 시작</div>
<div class='t' style='left:38px;top:106px;font-size:96px;color:#2FD39A'>아직 남음</div>
<div class='t' style='left:40px;top:250px;font-size:64px;color:#FF5A4E'>1998년</div>
<div id='m4' class='t' data-fit='575' style='left:32px;top:320px;font-size:170px;color:#FF5A4E'>11년<span style='font-size:80px'>째 바닥</span></div>
<div id='m5' class='t' data-fit='900' style='left:32px;top:540px;font-size:52px;color:#141B26;background:#fff;padding:8px 20px 10px;border-radius:999px;font-family:PD;font-weight:700'>{SUB4}</div>
<div class='fine' style='color:#8C95A6;top:658px;font-size:15px'>{FINE4}</div>
"""


VARIANTS['c1m'] = c1m_html()

# 5차 평균: c1l 7.12(제미나이 7.75·Claude 7.1·레드팀 6.5)지만 레드팀 겹침 3(검은 판 = 경쟁 '은퇴 후 주식 팔지 말고' 글씨판·글자 위주·빨강) → 모방 규칙 반려.
#   c1k 6.65(6.75·6.2·7, 레드팀 1위) · c1j 6.22('0원' 사실 관문 실패).
#   레드팀 c1k 처방: ① 알약 1.5배 또는 두 선 시작점에 '3억'(같은 3억 출발이 그림으로) ② '11년째' 한 덩어리·'바닥'만 작게, 끝점 크게+밝은 테두리, 바닥선 진하게.
#   Claude: 크게는 '11년'(녹색보다 커야), 대비↑. → c1n(진한 크림) · c1o(흰 판, 같은 배치) — 어두운 판은 겹침 때문에 c1m 참고용만.
def c1no(bg, base_col):
    s, X, Y = lines4(620, 96, 620, 404, lw=22)
    a, b, c = f"stroke='{RED}' stroke-width='26'", f"r='24' fill='{RED}' stroke='#fff' stroke-width='7'", "stroke='#9AA0AA' stroke-width='5'"
    assert a in s and b in s and c in s
    s = s.replace(a, f"stroke='{RED}' stroke-width='32'").replace(b, f"r='34' fill='{RED}' stroke='#fff' stroke-width='10'").replace(c, f"stroke='{base_col}' stroke-width='8'")
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
{s}
<div class='t' style='left:{X(0) - 30:.0f}px;top:{Y(3) - 92:.0f}px;font-size:50px;color:{INK}'>3억</div>
<div class='t' style='left:40px;top:34px;font-size:62px;color:{GREEN}'>1997년 시작</div>
<div class='t' style='left:38px;top:104px;font-size:96px;color:{GREEN}'>아직 남음</div>
<div class='t' style='left:40px;top:244px;font-size:62px;color:{RED}'>1998년</div>
<div id='n4' class='t' data-fit='520' style='left:32px;top:312px;font-size:150px;color:{RED}'>11년째<span style='font-size:84px'> 바닥</span></div>
<div id='n5' class='t' data-fit='900' style='left:32px;top:536px;font-size:54px;color:#fff;background:{NAVY};padding:8px 20px 10px;border-radius:999px;font-family:PD;font-weight:700'>{SUB4}</div>
<div class='fine' style='color:{GREY};top:658px;font-size:15px'>{FINE4}</div>
"""


VARIANTS.update(c1n=c1no('#EFE4CC', '#3A4150'), c1o=c1no('#FFFFFF', '#3A4150'))


# ── 7차(10/8 17시) — 6차: c1n 6.88(제미나이 6.75·Claude 6.9·레드팀 7). 1초 블라인드에서 새 문구는 '1997/1998 투자 수익률 그래프'로만 읽혀
#    '3억으로 노후 생활비 꺼내 쓰기'라는 주제를 3/3 못 맞힘(경쟁 5장은 '3억'이 가장 큼). → 이번 차수의 1순위 = 주제가 168px에서 읽히게.
#    처방: 작은 줄의 말 '3억 · 월 200만원'을 글자 그대로 맨 위 큰 줄로 올리고(낱말 변경 0), 나머지 '원화 계산 · 배당으로 받기'는 알약에.
#    레드팀 6차: 두 선 출발점에 공통 점 + '3억'(초록 선에서 뗀 자리) · 바탕 한 단계 진하게 · '11년째' 키움. Claude 6차: 크기 1순위 하나 — '1997년 시작: 아직 남음'은 한 줄 64px로 낮춤.
#    그림에 축 이름 '남은 돈'(사실 설명, 카피 아님) — 수익률 그래프가 아니라 통장 잔액이라는 것을 1초에 알리려고.
#    c1p = 1위 문구(titles.md 1위) · c1q = 교체안 문구(titles.md thumb_text_swap '1년 차이: 29년 넘게 vs 11년째 바닥', '넘게' 반드시)
CREAM7 = '#E9D9B4'


def lines7(x0, y0, w, h, lw=24):
    s, X, Y = lines4(x0, y0, w, h, lw=lw)
    a, b, c = f"stroke='{RED}' stroke-width='{lw + 4}'", f"r='24' fill='{RED}' stroke='#fff' stroke-width='7'", "stroke='#9AA0AA' stroke-width='5'"
    assert a in s and b in s and c in s
    s = s.replace(a, f"stroke='{RED}' stroke-width='{lw + 10}'").replace(b, f"r='34' fill='{RED}' stroke='#fff' stroke-width='10'").replace(c, "stroke='#3A4150' stroke-width='8'")
    s = s.replace('</svg>', f"<circle cx='{X(0):.1f}' cy='{Y(3):.1f}' r='50' fill='{INK}' stroke='#fff' stroke-width='6'/></svg>")
    return s, X, Y


def c1p_html():
    s, X, Y = lines7(740, 196, 500, 374)
    return f"""<div style='position:absolute;inset:0;background:{CREAM7}'></div>
{s}
<div class='t' style='left:{X(0) - 38:.0f}px;top:{Y(3) - 27:.0f}px;font-size:40px;color:#fff'>3억</div>
<div class='t' style='left:{X(0) - 40:.0f}px;top:{Y(7) - 40:.0f}px;font-size:34px;color:#3A4150;font-family:PD;font-weight:700'>계좌에 남은 돈</div>
<div id='p0' class='t' data-fit='1200' style='left:36px;top:18px;font-size:104px;color:{INK}'>3억 · 월 200만원 <span style='font-size:44px;color:#fff;background:{NAVY};padding:6px 18px 9px;border-radius:999px;font-family:PD;font-weight:700;vertical-align:middle'>원화 계산 · 배당으로 받기</span></div>
<div id='p1' class='t' data-fit='640' style='left:40px;top:170px;font-size:64px;color:{GREEN}'>1997년 시작: 아직 남음</div>
<div class='t' style='left:40px;top:268px;font-size:70px;color:{RED}'>1998년:</div>
<div id='p3' class='t' data-fit='640' style='left:30px;top:344px;font-size:190px;color:{RED}'>11년째<span style='font-size:96px'> 바닥</span></div>
<div class='fine' style='color:#5F6675;top:660px;font-size:15px'>{FINE4}</div>
"""


def c1q_html():
    s, X, Y = lines7(740, 196, 500, 374)
    return f"""<div style='position:absolute;inset:0;background:{CREAM7}'></div>
{s}
<div class='t' style='left:{X(0) - 38:.0f}px;top:{Y(3) - 27:.0f}px;font-size:40px;color:#fff'>3억</div>
<div class='t' style='left:{X(0) - 40:.0f}px;top:{Y(7) - 40:.0f}px;font-size:34px;color:#3A4150;font-family:PD;font-weight:700'>계좌에 남은 돈</div>
<div class='t' style='left:{X(16):.0f}px;top:{Y(6.4):.0f}px;font-size:40px;color:{GREEN}'>1997 시작</div>
<div class='t' style='left:{X(11) + 40:.0f}px;top:{Y(0) - 70:.0f}px;font-size:40px;color:{RED}'>1998 시작</div>
<div id='q0' class='t' data-fit='1200' style='left:36px;top:18px;font-size:104px;color:{INK}'>3억 · 월 200만원 <span style='font-size:40px;color:#fff;background:{NAVY};padding:6px 18px 9px;border-radius:999px;font-family:PD;font-weight:700;vertical-align:middle'>1997 vs 1998 시작 · 원화 · 배당으로 받기</span></div>
<div class='t' style='left:40px;top:170px;font-size:72px;color:{INK}'>1년 차이:</div>
<div id='q2' class='t' data-fit='640' style='left:34px;top:254px;font-size:120px;color:{GREEN}'>29년 넘게</div>
<div class='t' style='left:44px;top:390px;font-size:56px;color:#3A4150'>vs</div>
<div id='q4' class='t' data-fit='640' style='left:30px;top:440px;font-size:150px;color:{RED}'>11년째<span style='font-size:84px'> 바닥</span></div>
<div class='fine' style='color:#5F6675;top:660px;font-size:15px'>{FINE4}</div>
"""


VARIANTS.update(c1p=c1p_html(), c1q=c1q_html())


# 7차 판정(17:1x): c1p 세 명 평균 7.0(제미나이 7.0·7.0 / Claude 7 / 레드팀 7) → 통과선 7, 확정. c1n 6.67 · c1q 6.75지만 레드팀 겹침 3('3억'·'vs'·빨강) 반려.
#   레드팀 사실: 축 이름 '통장'은 증권 계좌라 틀린 말 → '계좌에 남은 돈'(위에서 바꿈, 카피 아님). 
#   c1p_s = '1998년 시작:'(copywriter 답 대기, 10/9 12:00) — 승인되면 이 판으로 바꿈. 낱말 하나 차이라 재심사 없이 레드팀 처방 그대로.
VARIANTS['c1p_s'] = VARIANTS['c1p'].replace(">1998년:</div>", ">1998년 시작:</div>")
assert VARIANTS['c1p_s'] != VARIANTS['c1p']


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||e.closest('svg')||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")


def main(keys):
    zp = os.path.join(HERE, 'zones.json')
    report = json.load(open(zp, encoding='utf-8')) if os.path.exists(zp) else {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k in keys:
            html = os.path.join(HERE, f'{k}.html')
            open(html, 'w', encoding='utf-8').write(HEAD + VARIANTS[k] + '\n' + TAIL)
            pg.goto('file:///' + html.replace(chr(92), '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
            report[k] = check_zones(pg)
            im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    print('A 배당', YA, '년차', A, '| B 매도', YB, '년차', B)
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
