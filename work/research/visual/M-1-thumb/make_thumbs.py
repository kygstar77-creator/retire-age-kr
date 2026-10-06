# M-1 '월배당 거꾸로' 썸네일 시안(2026-10-06 06시 PD) — py -3.12 make_thumbs.py [m1a,m1b,...]
# 숫자 출처: ep/M-1/calc_out.txt — 월 100만원(세후·건보 뒤) 필요 원금 JEPQ 1.38억 · SCHD 4.85억 · ACE 5.10억, 가장 적은 달 기준 ACE 8.92억(×1.75)
# 문구 출처: ep/M-1/titles.md 썸네일 A(1위)·B(2위) — copywriter 10/5. 제목 T1과 반복 안 함(제목엔 숫자 없음).
# 경쟁과 다른 점(compare.png): 경쟁 5 = 인물 사진·노랑/흰 테두리 글씨·돈다발. 우리 = 인물·사진 0, 막대 하나, 테두리 글씨 0.
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표 자동 검사(zones.json).
import os, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'M-1')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
for s in ('월 100만원: 연 세전 분배 15,611,746원 → 필요 원금 1.38억원', '월 100만원: 연 세전 분배 15,611,746원 → 필요 원금 4.85억원',
          '월 100만원: 연 세전 분배 15,693,413원 → 필요 원금 5.10억원 · 가장 적은 달 기준이면 8.92억원(×1.75)'):
    assert s in calc, s
INK, RED, YEL, GREY, BG = '#16181D', '#FF3B30', '#FFD400', '#8A93A3', '#121418'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
FINE = f"<div class='fine' style='color:{GREY};top:640px;font-size:22px'>2026.10.2 기준 지난 1년 분배 · 세금·건보료 뗀 뒤 · 투자 권유 아님</div>"


def bars(y0, rows, maxv, x0=58, w=860, h=64, gap=26):
    """가로 막대(이름·값). rows = [(이름, 값, 색)]"""
    s = ''
    for i, (name, v, c) in enumerate(rows):
        y = y0 + i * (h + gap); bw = w * v / maxv
        s += f"<div class='lab' style='left:{x0}px;top:{y + 8}px;font-size:56px;color:#fff'>{name}</div>"
        s += f"<div style='position:absolute;left:{x0 + 200}px;top:{y}px;width:{bw:.0f}px;height:{h}px;background:{c};border-radius:6px'></div>"
        s += f"<div class='t' style='left:{x0 + 200 + bw + 18:.0f}px;top:{y + 4}px;font-size:76px;color:{c}'>{v:.2f}억</div>"
    return s


# m1a — 비교(A vs B) + 내 돈 대입: copywriter A 그대로, 숫자마다 이름표
m1a = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div class='t' style='left:54px;top:46px;font-size:104px;color:#fff'>세후 월 <span style='color:{YEL}'>100만원</span> 받으려면</div>
<div id='a1' class='t' data-fit='1170' style='left:46px;top:220px;font-size:230px;color:{RED}'>1.38억 vs 5.10억</div>
<div class='t' style='left:70px;top:430px;font-size:96px;color:#fff'>JEPQ</div>
<div class='t' style='left:790px;top:430px;font-size:96px;color:#fff'>ACE</div>
<div class='lab' style='left:70px;top:556px;font-size:44px;color:{GREY}'>SCHD는 4.85억</div>
"""

# m1b — 반전: copywriter B — 같은 상품, 가장 적은 달로 재면
m1b = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div class='t' style='left:54px;top:46px;font-size:96px;color:#fff'>월 <span style='color:{YEL}'>100만원</span>, 가장 적은 달로 재면</div>
<div id='b1' class='t' data-fit='1170' style='left:46px;top:214px;font-size:240px;color:#fff'>5.10억 <span style='color:{RED}'>→ 8.92억</span></div>
<div class='t' style='left:62px;top:478px;font-size:80px;color:{GREY}'>ACE 미국배당다우존스</div>
"""

# m1c — 질문 + 막대(같은 규칙, 세 상품): 답이 막대 길이로 한눈에
m1c = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='c0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:118px;color:#fff'>월 <span style='color:{YEL}'>100만원</span> 받으려면 얼마?</div>
{bars(232, [('JEPQ', 1.38, '#3D8BFF'), ('SCHD', 4.85, '#C9CED8'), ('ACE', 5.10, RED)], 5.10, w=700, h=84, gap=36)}
"""
VARIANTS = {'m1a': m1a + FINE, 'm1b': m1b + FINE, 'm1c': m1c + FINE}

# ── 2차(06:2x) — 1초 시험(3.1-flash-lite 블라인드)에서 m1b를 '자산이 불어나는 시뮬레이션'으로 잘못 읽음
#    → 윗줄에 '필요한 돈'을 박고, 반전 조건('가장 적은 달로 재면')은 아랫줄로. 8.92억은 노랑(점수 지적).
m1d = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='d0' class='t' data-fit='1170' style='left:54px;top:44px;font-size:104px;color:#fff'>월 <span style='color:{YEL}'>100만원</span>에 필요한 돈</div>
<div id='d1' class='t' data-fit='1170' style='left:46px;top:200px;font-size:250px;color:#fff'>5.10억 <span style='color:{RED}'>→</span> <span style='color:{YEL}'>8.92억</span></div>
<div class='t' style='left:58px;top:470px;font-size:84px;color:{RED}'>가장 적은 달로 재면</div>
<div class='lab' style='left:62px;top:574px;font-size:40px;color:{GREY}'>ACE 미국배당다우존스</div>
"""
VARIANTS['m1d'] = m1d + FINE



# ── 3차(06:2x) — 심사 m1d 제미나이 7.5·7 / Claude 7.0 / 레드팀 6 = 평균 6.75(통과선 7 미달). 공통 지적:
#    ① ACE 이름이 168px에서 안 보임(제목 T1은 JEPQ로 시작해 JEPQ 얘기로 읽힘) ② 윗줄이 제목 T1과 같은 말(월 100만원·가장 적게 나온 달)
#    ③ 화살표가 '시간이 지나 늘었다'로 읽힘 → 숫자 밑에 재는 기준(평균 달·가장 적은 달) 꼬리표.
#    윗줄 = 대본 0장 '매달 분배금이 똑같이 나오지 않거든요'에서 가져옴(지은 말 아님).
m1e = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='e0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:96px;color:#fff'>분배금이 매달 똑같지 않으면</div>
<div class='t' style='left:52px;top:176px;font-size:150px;color:{YEL}'>ACE</div>
<div id='e1' class='t' data-fit='1170' style='left:46px;top:330px;font-size:200px;color:#fff'>5.10억 <span style='color:{RED}'>→</span> <span style='color:{YEL}'>8.92억</span></div>
<div class='lab' style='left:62px;top:520px;font-size:44px;color:{GREY}'>평균 달 기준</div>
<div class='lab' style='left:756px;top:520px;font-size:44px;color:{GREY}'>가장 적은 달 기준</div>
<div class='lab' style='left:400px;top:236px;font-size:52px;color:#fff'>월 100만원 받는 데 필요한 돈</div>
"""
VARIANTS['m1e'] = m1e + FINE


# ── 4차(06:2x) — m1e 제미나이 7·7 / Claude 7.0 / 레드팀 6 = 6.67. 레드팀: '필요한 돈' 줄이 8.92억을 꼭 필요한 돈처럼 보이게 하고,
#    회색 꼬리표가 168px에서 사라짐 → '필요한 돈' 줄 빼고(제목이 말함), 꼬리표를 숫자 바로 밑에 크게·색으로. 꼬리표 말은 대본 104행 '평균으로 잰'·4장 '가장 적게 나온 달'.
m1f = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='f0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:100px;color:#fff'>분배금이 매달 똑같지 않으면</div>
<div class='t' style='left:52px;top:170px;font-size:150px;color:{YEL}'>ACE</div>
<div id='f1' class='t' data-fit='1170' style='left:46px;top:320px;font-size:200px;color:#fff'>5.10억 <span style='color:{RED}'>→</span> <span style='color:{YEL}'>8.92억</span></div>
<div class='t' style='left:60px;top:500px;font-size:62px;color:#C9CED8'>평균으로 재면</div>
<div class='t' style='left:740px;top:500px;font-size:62px;color:{YEL}'>가장 적은 달로 재면</div>
"""
VARIANTS['m1f'] = m1f + FINE


# ── 5차(06:3x) — m1f 6.42(레드팀 5.5: 화살표가 '수익이 불었다'로 오독·큰 숫자 2개·'가장 적은 달'이 제목과 겹침).
#    → 큰 숫자 하나(8.92억), 화살표 없음, 비교는 '평균 기준의 1.75배'(대본 4장 자막 말) 꼬리표, 윗줄 = 대본 104행 '실제 통장에는 평균이 들어오지 않잖아요'.
#    상품 이름은 168px에서 읽히게 흰색 굵게.
m1g = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='g0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:96px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='t' style='left:56px;top:166px;font-size:78px;color:#C9CED8'>ACE 미국배당다우존스</div>
<div id='g1' class='t' data-fit='760' style='left:44px;top:262px;font-size:270px;color:{YEL}'>8.92억</div>
<div class='t' style='left:62px;top:540px;font-size:64px;color:#fff'>필요한 돈, 평균 기준의 <span style='color:{RED}'>1.75배</span></div>
"""
FINE_G = f"<div class='fine' style='color:{GREY};top:640px;font-size:22px'>2026.10.2 기준 · 세금·건보료 뗀 뒤, 2천만원 넘는 추가 세금·건보료는 넣지 않은 최소값</div>"
VARIANTS['m1g'] = m1g + FINE_G


# ── 6차(06:3x) — 5차 공통 지적: '필요'를 숫자와 한 덩어리로(레드팀), 그림 장치 하나 = 12달 분배 막대 중 가장 적은 달만 빨강(Claude).
#    막대 값 = facts [K1] ACE 1주당 분배 12회(원)
_facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
ACE12 = [37, 21, 53, 39, 24, 46, 44, 27, 40, 50, 25, 35]
assert '25-10 37 · 25-11 21 · 25-12 53 · 26-01 39 · 26-02 24 · 26-03 46 · 26-04 44 · 26-05 27 · 26-06 40 · 26-07 50 · 26-08 25 · 26-09 35' in _facts and sum(ACE12) == 441
def month_bars(x0, ybase, hmax, w=38, gap=10):
    s = ''
    for i, v in enumerate(ACE12):
        h = hmax * v / max(ACE12); c = RED if v == min(ACE12) else '#4A5160'
        s += f"<div style='position:absolute;left:{x0 + i * (w + gap)}px;top:{ybase - h:.0f}px;width:{w}px;height:{h:.0f}px;background:{c}'></div>"
    i = ACE12.index(min(ACE12)); s += f"<div class='t' style='left:{x0 + i * (w + gap) - 14}px;top:{ybase - hmax * 21 / 53 - 62:.0f}px;font-size:52px;color:{RED}'>21원</div>"
    return s
m1h = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='h0' class='t' data-fit='1170' style='left:54px;top:36px;font-size:88px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='lab' style='left:58px;top:150px;font-size:36px;color:#C9CED8'>ACE 미국배당다우존스 · 1주당 분배 12달</div>
{month_bars(60, 410, 200)}
<div class='t' style='left:690px;top:214px;font-size:64px;color:#fff'>평균의</div>
<div class='t' style='left:686px;top:296px;font-size:110px;color:{RED}'>1.75배</div>
<div id='h1' class='t' data-fit='880' style='left:46px;top:430px;font-size:170px;color:{YEL}'>8.92억 필요</div>
"""
FINE_H = f"<div class='fine' style='color:{GREY};top:640px;font-size:22px'>세후 월 100만원 기준 · 2026.10.2 · 연 2천만원 넘는 몫의 추가 세금·건보료 미포함</div>"
VARIANTS['m1h'] = m1h + FINE_H


# ── 7차(06:4x) — m1h 제미나이 7.5·7 / Claude 7.0 / 레드팀 6 = 6.75. 레드팀 조건: 1.75배를 작게(큰 숫자 하나), 막대에 평균(441÷12=36.75원) 점선.
def month_bars_avg(x0, ybase, hmax, w=38, gap=10):
    s = month_bars(x0, ybase, hmax, w, gap)
    ya = ybase - hmax * (sum(ACE12) / 12) / max(ACE12); xe = x0 + 12 * (w + gap) - gap
    s += f"<div style='position:absolute;left:{x0 - 6}px;top:{ya - 2:.0f}px;width:{xe - x0 + 12}px;height:0;border-top:5px dashed #fff'></div>"
    s += f"<div class='t' style='left:{xe + 16}px;top:{ya - 30:.0f}px;font-size:52px;color:#fff'>평균</div>"
    return s
m1i = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='i0' class='t' data-fit='1170' style='left:54px;top:36px;font-size:88px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='lab' style='left:58px;top:150px;font-size:36px;color:#C9CED8'>ACE 미국배당다우존스 · 1주당 분배 12달</div>
{month_bars_avg(60, 410, 200, w=62, gap=14)}
<div id='i1' class='t' data-fit='880' style='left:46px;top:430px;font-size:170px;color:{YEL}'>8.92억 필요</div>
<div class='lab' style='left:62px;top:604px;font-size:30px;color:#fff'>월 100만원 받으려면 · 평균으로 잴 때의 1.75배</div>
"""
FINE_I = f"<div class='fine' style='color:{GREY};top:650px;font-size:20px'>세금·건보료 뗀 뒤 · 2026.10.2 · 연 2천만원 넘는 몫의 추가 세금·건보료 미포함</div>"
VARIANTS['m1i'] = m1i + FINE_I


# ── 8차(06:4x) — m1i 제미나이 7·7.5 / Claude 7.0 / 레드팀 6.5 = 6.92. 레드팀 고칠 것: 아랫줄 '월 100만원 받으려면'(제목 반복) 빼기,
#    큰 숫자에 ACE 붙이기(168px에서 'JEPQ도 8.92억' 오해 막기), 각주를 제목 말(세금·건보료 뗀 뒤)과 맞추기.
m1j = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='j0' class='t' data-fit='1170' style='left:54px;top:36px;font-size:88px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='lab' style='left:58px;top:150px;font-size:36px;color:#C9CED8'>ACE 미국배당다우존스 · 1주당 분배 12달</div>
{month_bars_avg(60, 410, 200, w=62, gap=14)}
<div id='j1' class='t' data-fit='900' style='left:46px;top:430px;font-size:170px;color:{YEL}'><span style='color:#fff'>ACE</span> 8.92억 필요</div>
<div class='lab' style='left:62px;top:556px;font-size:44px;color:#fff'>평균으로 잴 때의 1.75배</div>
"""
FINE_J = f"<div class='fine' style='color:{GREY};top:652px;font-size:20px'>세금·건보료 뗀 뒤 · 2026.10.2 · 연 2천만원 넘는 몫의 추가분은 빼고 잰 최소값</div>"
VARIANTS['m1j'] = m1j + FINE_J



# ── 9차(10/6 09시 visual-designer, PD 요청) — 8차까지 세 명 공통 '어두운 숫자판은 다르지만 먼저 누르고 싶지 않다' → 문구가 아니라 판 자체.
#    밝은 바탕 + 그림 장치를 화면 절반 이상으로. 문구는 지난 차수에서 쓴 대본 말(104행 '통장에는 평균이 들어오지 않잖아요', 106행 '가장 적게 나온 달로 다시 재면')만.
#    숫자: calc_out JEPQ 1.38억→1.71억(×1.23)·ACE 5.10억→8.92억(×1.75) · facts K1 12달 분배.
assert '필요 원금 1.38억원 · 가장 적은 달 기준이면 1.71억원(×1.23)' in calc
NAVY, PAPER = '#1B2A4A', '#FFFFFF'

# m1k — 흰 바탕, 12달 막대를 화면 위 절반 가득(굵게), 21원 막대만 빨강, 평균 점선. 아래 'ACE 8.92억 필요'.
def big_month_bars(x0, ybase, hmax, w, gap, base='#C5CCD8'):
    s = ''
    for i, v in enumerate(ACE12):
        h = hmax * v / max(ACE12); c = RED if v == min(ACE12) else base
        s += f"<div style='position:absolute;left:{x0 + i * (w + gap)}px;top:{ybase - h:.0f}px;width:{w}px;height:{h:.0f}px;background:{c};border-radius:6px 6px 0 0'></div>"
    i = ACE12.index(min(ACE12)); xm = x0 + i * (w + gap)
    s += f"<div class='t' style='left:{xm - 18}px;top:{ybase - hmax * 21 / 53 - 80:.0f}px;font-size:68px;color:{RED}'>21원</div>"
    ya = ybase - hmax * (sum(ACE12) / 12) / max(ACE12); xe = x0 + 12 * (w + gap) - gap
    s += f"<div style='position:absolute;left:{x0 - 8}px;top:{ya - 3:.0f}px;width:{xe - x0 + 16}px;height:0;border-top:7px dashed {NAVY}'></div>"
    s += f"<div class='t' style='left:{xe + 18}px;top:{ya - 34:.0f}px;font-size:60px;color:{NAVY}'>평균</div>"
    return s
m1k = f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div id='k0' class='t' data-fit='1170' style='left:48px;top:30px;font-size:92px;color:{INK};background:{YEL};padding:10px 18px 6px'>통장엔 평균이 안 들어온다</div>
{big_month_bars(60, 440, 290, w=64, gap=12)}
<div id='k1' class='t' data-fit='900' style='left:44px;top:462px;font-size:150px;color:{INK}'>ACE <span style='color:{RED}'>8.92억</span> 필요</div>
"""
FINE_K = f"<div class='fine' style='color:#5B6475;top:640px;font-size:22px'>ACE 미국배당다우존스 1주당 분배 12달 · 세후 월 100만원 · 2026.10.2 · 추가 세금 미포함</div>"
VARIANTS['m1k'] = m1k + FINE_K

# m1l — 노랑 바탕, 세로 탑 두 개(JEPQ·ACE): 점선 테두리 = 평균으로 잰 돈, 꽉 찬 탑 = 가장 적은 달로 잰 돈. ACE 탑이 위까지 솟음.
#    레드팀 8차 조건(체리피킹 막기 = JEPQ도 같이) 반영. 큰 숫자 하나 = 8.92억.
def tower(x, w, ybase, hpx_avg, hpx_low, col, name, low_txt, big):
    s = f"<div style='position:absolute;left:{x}px;top:{ybase - hpx_low:.0f}px;width:{w}px;height:{hpx_low:.0f}px;background:{col};border-radius:8px 8px 0 0'></div>"
    s += f"<div style='position:absolute;left:{x}px;top:{ybase - hpx_avg:.0f}px;width:{w}px;height:0;border-top:7px dashed {'#fff' if hpx_avg < hpx_low else INK}'></div>"
    s += f"<div class='t' style='left:{x + w // 2}px;transform:translateX(-50%);top:{ybase + 14}px;font-size:58px;color:{INK}'>{name}</div>"
    s += f"<div class='t' style='left:{x + w + 22}px;top:{ybase - hpx_low - 6:.0f}px;font-size:{big}px;color:{col if col != INK else INK}'>{low_txt}</div>"
    return s
_H = 450 / 8.92  # 8.92억 = 470px
m1l = f"""<div style='position:absolute;inset:0;background:{YEL}'></div>
<div id='l0' class='t' data-fit='1180' style='left:48px;top:30px;font-size:80px;color:{INK}'>가장 적은 달로 다시 재면</div>
{tower(80, 150, 570, 1.38 * _H, 1.71 * _H, NAVY, 'JEPQ', '1.71억', 70)}
{tower(520, 190, 570, 5.10 * _H, 8.92 * _H, RED, 'ACE', '8.92억', 150)}
<div class='lab' style='left:740px;top:{570 - 5.10 * _H - 26:.0f}px;font-size:40px;color:{INK}'>- - - 평균으로 재면 5.10억</div>
"""
FINE_L = f"<div class='fine' style='color:{INK};top:652px;font-size:18px;left:60px'>세후 월 100만원 필요한 돈 · 2026.10.2 지난 1년 분배 · 추가 세금 미포함 · 투자 권유 아님</div>"
VARIANTS['m1l'] = m1l + FINE_L

# m1m — 흰 바탕 통장 그림: 왼쪽에 통장 한 장(날짜·입금 줄 12개, 21원 줄만 빨간 동그라미), 오른쪽 큰 숫자.
def passbook(x, y, w):
    rows = ['25.10', '25.11', '25.12', '26.01', '26.02', '26.03', '26.04', '26.05', '26.06', '26.07', '26.08', '26.09']
    s = f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{38 + 12 * 38 + 14}px;background:#fff;border:4px solid {NAVY};border-radius:14px;box-shadow:10px 12px 0 #D6DBE4'></div>"
    s += f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:44px;background:{NAVY};border-radius:12px 12px 0 0'></div>"
    s += f"<div class='lab' style='left:{x + 20}px;top:{y + 6}px;font-size:28px;color:#fff'>분배 입금 (1주당)</div>"
    for i, (d, v) in enumerate(zip(rows, ACE12)):
        yy = y + 52 + i * 38; c = RED if v == min(ACE12) else INK
        s += f"<div class='lab' style='left:{x + 22}px;top:{yy}px;font-size:28px;color:#6B7486'>{d}</div>"
        s += f"<div class='lab' style='left:{x + w - 110}px;top:{yy}px;font-size:30px;color:{c}'>{v}원</div>"
        if v == min(ACE12):
            s += f"<div style='position:absolute;left:{x + 8}px;top:{yy - 6}px;width:{w - 16}px;height:44px;border:6px solid {RED};border-radius:24px'></div>"
    return s
m1m = f"""<div style='position:absolute;inset:0;background:#EEF1F6'></div>
{passbook(48, 40, 360)}
<div id='m0' class='t' data-fit='800' style='left:456px;top:54px;font-size:84px;color:{INK}'>통장엔 평균이</div>
<div id='m2' class='t' data-fit='800' style='left:456px;top:150px;font-size:84px;color:{INK}'>안 들어온다</div>
<div id='m3' class='t' data-fit='790' style='left:460px;top:286px;font-size:64px;color:{NAVY}'>ACE 미국배당다우존스</div>
<div id='m1' class='t' data-fit='800' style='left:452px;top:380px;font-size:190px;color:{RED}'>8.92억<span style='font-size:110px;color:{INK}'> 필요</span></div>
"""
FINE_M = f"<div class='fine' style='color:#5B6475;top:654px;font-size:18px;left:52px'>세후 월 100만원 · 가장 적은 달 기준 · 2026.10.2 · 추가 세금 미포함</div>"
VARIANTS['m1m'] = m1m + FINE_M


# ── 10차(10/6 visual-designer) — 9차 Claude m1l 7.6(1위): ① '평균으로 재면 5.10억'이 168px에서 안 읽힘 → 크게·흰 점선 굵게 ② 윗줄 더 크게 ③ 1.71억 키워 무게 맞추기.
def tower2(x, w, ybase, hpx_avg, hpx_low, col, name, low_txt, big, avg_txt=None):
    s = f"<div style='position:absolute;left:{x}px;top:{ybase - hpx_low:.0f}px;width:{w}px;height:{hpx_low:.0f}px;background:{col};border-radius:8px 8px 0 0'></div>"
    s += f"<div style='position:absolute;left:{x - 10}px;top:{ybase - hpx_avg - 5:.0f}px;width:{w + 20}px;height:0;border-top:10px dashed {INK}'></div>"
    s += f"<div class='t' style='left:{x + w // 2}px;transform:translateX(-50%);top:{ybase + 6}px;font-size:72px;color:{INK}'>{name}</div>"
    s += f"<div class='t' style='left:{x + w + 22}px;top:{ybase - hpx_low - 4:.0f}px;font-size:{big}px;color:{col}'>{low_txt}</div>"
    if avg_txt:
        s += f"<div class='t' style='left:{x + w + 26}px;top:{ybase - hpx_avg - 30:.0f}px;font-size:60px;color:{INK}'>{avg_txt}</div>"
    return s
m1n = f"""<div style='position:absolute;inset:0;background:{YEL}'></div>
<div id='n0' class='t' data-fit='1180' style='left:44px;top:26px;font-size:96px;color:{INK}'>가장 적은 달로 다시 재면</div>
{tower2(70, 150, 570, 1.38 * _H, 1.71 * _H, NAVY, 'JEPQ', '1.71억', 96)}
{tower2(560, 190, 570, 5.10 * _H, 8.92 * _H, RED, 'ACE', '8.92억', 150, '평균이면 5.10억')}
"""
VARIANTS['m1n'] = m1n + FINE_L


# ── 11차 — 9차 레드팀 m1l 5.5: '필요'가 없어 'ACE 8.92억 됐다'로 읽힘 + '월 100만원'이 168px에 없음.
#    → 윗줄 = '월 100만원에 필요한 돈'(m1d 윗줄, 1초 시험 통과 말), 반전 조건은 8.92억 바로 밑 꼬리표(대본 106행).
m1o = f"""<div style='position:absolute;inset:0;background:{YEL}'></div>
<div id='o0' class='t' data-fit='1180' style='left:44px;top:26px;font-size:96px;color:{INK}'>월 100만원에 필요한 돈</div>
{tower2(70, 150, 570, 1.38 * _H, 1.71 * _H, NAVY, 'JEPQ', '1.71억', 96)}
{tower2(560, 190, 570, 5.10 * _H, 8.92 * _H, RED, 'ACE', '8.92억', 150, '평균이면 5.10억')}
<div class='t' style='left:70px;top:150px;font-size:58px;color:{INK}'>가장 적은 달로</div>
<div class='t' style='left:70px;top:222px;font-size:58px;color:{INK}'>다시 재면 →</div>
"""
FINE_O = f"<div class='fine' style='color:{INK};top:652px;font-size:18px;left:60px'>세금·건보료 뗀 뒤 · 2026.10.2 지난 1년 분배 · 연 2천만원 넘는 몫 추가 세금 미포함 · 투자 권유 아님</div>"
VARIANTS['m1o'] = m1o + FINE_O


# ── 12차 — 10차 m1o 제미나이 7.5·6.5 / Claude 7 / 레드팀 7 = 7.0. 공통: '가장 적은 달로 다시 재면'이 168px에서 뭉개짐·화살표가 ACE만 가리켜
#    JEPQ 기준이 헷갈림 → 조건을 윗줄 바로 밑 둘째 줄(두 막대 공통 기준)로 크게, 막대 이름 키움.
_H2 = 350 / 8.92
m1p = f"""<div style='position:absolute;inset:0;background:{YEL}'></div>
<div id='p0' class='t' data-fit='1180' style='left:44px;top:24px;font-size:96px;color:{INK}'>월 100만원에 필요한 돈</div>
<div id='p2' class='t' data-fit='1180' style='left:48px;top:136px;font-size:64px;color:{RED}'>가장 적은 달로 다시 재면</div>
{tower2(70, 160, 566, 1.38 * _H2, 1.71 * _H2, NAVY, 'JEPQ', '1.71억', 100)}
{tower2(560, 190, 566, 5.10 * _H2, 8.92 * _H2, RED, 'ACE', '8.92억', 138, '평균이면 5.10억')}
"""
VARIANTS['m1p'] = m1p + FINE_O


# ── 13차 — 11차 m1p 제미나이 7.5·7.5 / Claude 7 / 레드팀 6 = 6.83. 레드팀: JEPQ·ACE 나란히 = 상품 우열('JEPQ가 싸다')로 읽힘, 8.92억은 최소값인데 맨숫자.
#    → JEPQ 탑 빼고 이유(ACE 12달 막대, 21원 빨강)를 왼쪽에, 결과 '최소 8.92억'을 오른쪽에. 노랑 바탕·윗줄은 10차 m1o(세 명 7.0)에서 그대로.
def ybars(x0, ybase, hmax, w, gap):
    s = ''
    for i, v in enumerate(ACE12):
        h = hmax * v / max(ACE12); c = RED if v == min(ACE12) else NAVY
        s += f"<div style='position:absolute;left:{x0 + i * (w + gap)}px;top:{ybase - h:.0f}px;width:{w}px;height:{h:.0f}px;background:{c};border-radius:4px 4px 0 0'></div>"
    i = ACE12.index(min(ACE12)); xm = x0 + i * (w + gap)
    s += f"<div class='t' style='left:{xm - 30}px;top:{ybase - hmax * 21 / 53 - 78:.0f}px;font-size:60px;color:{RED};background:{YEL};padding:4px 8px;border:5px solid {RED};border-radius:10px;z-index:2'>21원</div>"
    ya = ybase - hmax * (sum(ACE12) / 12) / max(ACE12); xe = x0 + 12 * (w + gap) - gap
    s += f"<div style='position:absolute;left:{x0 - 8}px;top:{ya - 4:.0f}px;width:{xe - x0 + 16}px;height:0;border-top:8px dashed {INK}'></div>"
    return s
m1q = f"""<div style='position:absolute;inset:0;background:{YEL}'></div>
<div id='q0' class='t' data-fit='1180' style='left:44px;top:24px;font-size:96px;color:{INK}'>월 100만원에 필요한 돈</div>
<div id='q2' class='t' data-fit='1180' style='left:48px;top:136px;font-size:64px;color:{RED}'>가장 적은 달로 다시 재면</div>
{ybars(56, 560, 300, 36, 10)}
<div class='lab' style='left:58px;top:574px;font-size:34px;color:{INK}'>ACE 미국배당다우존스 · 12달 분배(1주)</div>
<div class='t' style='left:640px;top:250px;font-size:64px;color:{INK}'>최소</div>
<div id='q1' class='t' data-fit='600' style='left:634px;top:320px;font-size:170px;color:{RED}'>8.92억</div>
<div class='t' style='left:640px;top:500px;font-size:56px;color:{INK}'>평균이면 5.10억</div>
"""
FINE_Q = f"<div class='fine' style='color:{INK};top:652px;font-size:18px;left:60px'>세금·건보료 뗀 뒤 · 2026.10.2 지난 1년 분배 · 연 2천만원 넘는 몫의 추가 세금·건보료 미포함 · 투자 권유 아님</div>"
VARIANTS['m1q'] = m1q + FINE_Q


# ── 14차 — 13차 m1q 제미나이 7.5·7.5 / Claude 6 / 레드팀 7 = 6.83. 두 명 공통: 8.92억 옆에 '필요'(옆 경쟁 '22억까지 불어납니다'와 오독 막기), 조건 줄 더 크게.
m1r = m1q.replace("id='q2' class='t' data-fit='1180' style='left:48px;top:136px;font-size:64px", "id='q2' class='t' data-fit='1180' style='left:46px;top:132px;font-size:76px") \
         .replace("<div id='q1' class='t' data-fit='600' style='left:634px;top:320px;font-size:170px;color:{RED}'>8.92억</div>".format(RED=RED),
                  "<div id='q1' class='t' data-fit='630' style='left:634px;top:330px;font-size:156px;color:{RED}'>8.92억<span style='font-size:92px;color:{INK}'> 필요</span></div>".format(RED=RED, INK=INK))
assert m1r.count('필요') == 2 and 'font-size:76px' in m1r
VARIANTS['m1r'] = m1r + FINE_Q

def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
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
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))

