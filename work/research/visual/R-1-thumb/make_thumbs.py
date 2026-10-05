# R-1 '1억의 1년 영수증' 썸네일 시안(2026-10-03 visual) — py -3.12 make_thumbs.py [r1a,r1b,...]
# 숫자 출처: ep/R-1/facts.txt [영수증] 세후 통장 — 예금 102,182,680 · 금 103,241,818 · S&P500 110,394,170 · SCHD 116,525,333
#   예금 vs SCHD 차이 14,342,653 → '1,434만'(facts [말하는 단위] 오차 0.03%). 기간 2025-10-02 → 2026-10-02, 과거 값.
# 문구: copywriter S4 '같은 1억, 1년 뒤 1,434만 차이'(제목 = 예금 금리 2.58%·질문 → 썸네일은 답 쪽 간격, 겹침 없음)
# 막대는 0원부터(늘어난 돈 = 세후 통장 - 1억) — 1억부터 자른 막대로 차이를 부풀리지 않는다.
# 경쟁(compare.png) = 2D 일러스트·진행자 얼굴·상품 표. 우리 = 사진·인물 0, '영수증' 한 장(시리즈 정체성), 큰 숫자 1개.
# 실험: X-THUMB-2 — r1a·r1c = B(한 줄 큰 숫자), r1b = A(영수증 + 숫자)
import os, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'R-1')
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
for s in ('통장 102,182,680', '통장 103,365,122', '통장 110,225,307', '통장 115,987,335', '통장 13,804,655'):
    assert s in facts, s
# 10/3 13:0x 갱신: 분배금 원천징수 15%([15])·끝값 확정치 반영(옛 값 금 3,241,818·S&P 10,394,170·SCHD 16,525,333 = 분배금 세전)
GAIN = {'예금': 2182680, '금': 3365122, 'S&P500': 10225307, 'SCHD': 15987335}
assert GAIN['SCHD'] - GAIN['예금'] == 13804655
FONT = 'file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/public/fonts/'
HEAD = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:BH;src:url('{FONT}BlackHanSans.ttf')}}
@font-face{{font-family:PD;src:url('{FONT}pd700.ttf');font-weight:700}}
@font-face{{font-family:PD;src:url('{FONT}pd500.ttf');font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:PD}}
.t{{position:absolute;font-family:BH;white-space:nowrap;line-height:1}}
.lab{{position:absolute;font:700 30px PD;white-space:nowrap}}
.fine{{position:absolute;font:500 22px PD;white-space:nowrap}}
</style></head><body>"""
TAIL = """<script>
function fit(id,maxW){const e=document.getElementById(id);let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e.id,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
YEL, RED, INK, MUTE = '#FFD43B', '#FF4D47', '#0F1720', '#8A93A3'
FINE = "<div class='fine' style='left:52px;top:640px;color:%s'>세금 뗀 통장 기준 · 2025.10 → 2026.10 실제 값(과거, 미래 보장 아님)</div>"


def hbars(x, y, wmax, h, gap, names, dark=True, hi='SCHD', lo='예금', labw=190, fs=40):
    top = max(GAIN.values()); s = ''
    for i, n in enumerate(names):
        w = max(8, wmax * GAIN[n] / top); yy = y + i * (h + gap)
        c = YEL if n == hi else ('#E6E8EC' if n == lo else ('#3C4656' if dark else '#C9CDD4'))
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 4:.0f}px;font-size:{fs}px;color:{'#fff' if dark else INK}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + labw}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{c};border-radius:0 8px 8px 0'></div>"
    return s


# r1a — 큰 숫자 한 줄 + 0부터 막대 4개(이름만, 숫자 없음)
r1a = f"""<div style='position:absolute;inset:0;background:{INK}'></div>
<div class='t' style='left:52px;top:44px;font-size:92px;color:#fff'>같은 1억, 1년 뒤</div>
<div id='a1' class='t' data-fit='1180' style='left:46px;top:152px;font-size:196px;color:{YEL}'>1,434만 차이</div>
{hbars(56, 388, 640, 46, 14, ['예금', '금', 'S&P500', 'SCHD'])}
""" + FINE % MUTE


# r1b — 영수증 한 장(왼쪽, 깎이는 줄) + 오른쪽 큰 숫자
def receipt():
    rows = [('예금', '+218만'), ('금', '+324만'), ('S&P500', '+1,039만'), ('SCHD', '+1,653만')]
    s = "<div style='position:absolute;left:60px;top:40px;width:480px;height:580px;background:#FBFAF6;transform:rotate(-3deg);box-shadow:0 18px 40px rgba(0,0,0,.45)'>"
    s += f"<div class='t' style='left:34px;top:34px;font-size:52px;color:{INK}'>1억의 1년 영수증</div>"
    s += "<div style='position:absolute;left:34px;right:34px;top:108px;border-top:4px dashed #9AA0A8'></div>"
    for i, (n, v) in enumerate(rows):
        y = 132 + i * 86; hi = n == 'SCHD'; lo = n == '예금'
        col = '#9A6B00' if hi else INK
        if hi: s += f"<div style='position:absolute;left:24px;right:24px;top:{y - 10}px;height:70px;background:rgba(255,212,59,.55);border-radius:10px'></div>"
        if lo: s += f"<div style='position:absolute;left:24px;right:24px;top:{y - 10}px;height:70px;border:4px solid {RED};border-radius:10px'></div>"
        s += f"<div class='lab' style='left:34px;top:{y}px;font-size:44px;color:{col}'>{n}</div>"
        s += f"<div class='lab' style='right:34px;top:{y}px;font-size:44px;color:{col}'>{v}</div>"
    s += "<div style='position:absolute;left:34px;right:34px;top:486px;border-top:4px dashed #9AA0A8'></div>"
    s += "<div class='lab' style='left:34px;top:506px;font-size:28px;color:#5A6170'>세금 뗀 뒤 늘어난 돈</div></div>"
    return s


r1b = f"""<div style='position:absolute;inset:0;background:#123B33'></div>
{receipt()}
<div class='t' style='left:620px;top:120px;font-size:84px;color:#fff'>같은 1억인데</div>
<div class='t' style='left:614px;top:232px;font-size:76px;color:#CFE3DC'>1년 뒤 차이</div>
<div id='b1' class='t' data-fit='640' style='left:608px;top:336px;font-size:200px;color:{YEL}'>1,434만</div>
<div class='fine' style='left:620px;top:540px;color:#9FC2B7'>2025.10 → 2026.10 실제 값 · 과거 기준</div>
"""

# r1c — 두 막대만(예금 vs SCHD), 높이 = 세후 늘어난 돈(0부터)
H0, HMAX = 560, 460
hd = round(HMAX * GAIN['예금'] / GAIN['SCHD'])
r1c = f"""<div style='position:absolute;inset:0;background:#F4F1E8'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:16px;background:{INK}'></div>
<div class='t' style='left:52px;top:70px;font-size:104px;color:{INK}'>같은 1억</div>
<div class='t' style='left:52px;top:196px;font-size:104px;color:{INK}'>1년 뒤</div>
<div id='c1' class='t' data-fit='640' style='left:46px;top:330px;font-size:150px;color:#D11F1A'>1,434만</div>
<div class='t' style='left:52px;top:494px;font-size:84px;color:{INK}'>차이</div>
<div style='position:absolute;left:740px;top:{H0}px;width:340px;height:4px;background:{INK}'></div>
<div style='position:absolute;left:760px;top:{H0 - hd}px;width:120px;height:{hd}px;background:#9AA0A8'></div>
<div class='lab' style='left:778px;top:{H0 + 8}px;font-size:40px;color:{INK}'>예금</div>
<div style='position:absolute;left:920px;top:{H0 - HMAX}px;width:120px;height:{HMAX}px;background:{INK}'></div>
<div class='lab' style='left:922px;top:{H0 - HMAX - 52}px;font-size:40px;color:{INK}'>SCHD</div>
<div style='position:absolute;left:890px;top:{H0 - HMAX}px;width:22px;height:{HMAX - hd}px;border:6px solid #D11F1A;border-left:none'></div>
<div class='fine' style='left:52px;top:640px;color:#6B7280'>세금 뗀 뒤 늘어난 돈 · 2025.10 → 2026.10 실제 값(과거)</div>
"""
VARIANTS = {'r1a': r1a, 'r1b': r1b, 'r1c': r1c}

# ── 2차(10/3) — 1차 평균 r1a 6.33·r1c 6.00·r1b 5.67(제미나이 lite 8/6/7 · Claude 6/7/5 · 레드팀 5/5/5) 공통 지적:
#   ① '1,434만 차이'가 무엇과 무엇인지 안 보임 → '예금 vs SCHD'를 숫자 바로 위에 ② 168px에서 막대 이름 안 읽힘 → 이름 2배
#   ③ 막대 2개만 = 골라 보여 주기(레드팀) → 4개 다 두고 금·S&P500은 회색 ④ 남색+노랑 = 경쟁 겹침 → 흰 바탕+먹색+빨강
#   ⑤ 사실(레드팀): SCHD 통장은 분배금을 세전으로 넣은 값(facts 50·52행 '분배금 세금 줄 확인 안 함') → '세금 뗀' 문구 뺌
FINE2 = "<div class='fine' style='left:52px;top:640px;color:%s'>1년 뒤 통장 기준 · 2025.10.2 → 2026.10.2 실제 값(과거)</div>"
MAN = {'예금': '+218만', 'SCHD': '+1,653만'}


def hbars2(x, y, wmax, h, gap, labw=230, fs=56, dark=False):
    top = GAIN['SCHD']; s = ''
    for i, n in enumerate(['예금', '금', 'S&P500', 'SCHD']):
        w = max(10, wmax * GAIN[n] / top); yy = y + i * (h + gap); key = n in MAN
        c = '#E5322D' if n == 'SCHD' else (INK if n == '예금' and not dark else ('#fff' if n == '예금' else ('#4A5262' if dark else '#C4C8CF')))
        tc = ('#fff' if dark else INK) if key else ('#7C8494' if dark else '#9AA0A8')
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + labw}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{c};border-radius:0 8px 8px 0'></div>"
        if key: s += f"<div class='lab' style='left:{x + labw + w + 16:.0f}px;top:{yy + (h - 48) / 2 - 6:.0f}px;font-size:48px;color:{c if n == 'SCHD' else tc}'>{MAN[n]}</div>"
    return s


# r1d — 흰 바탕: '예금 vs SCHD' 꼬리표 + 큰 '1,434만 차이' + 가로 막대 4개(이름 크게, 두 끝값만)
r1d = f"""<div style='position:absolute;inset:0;background:#FFFFFF'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:18px;background:{INK}'></div>
<div class='t' style='left:52px;top:52px;font-size:72px;color:{INK}'>같은 1억, 1년 뒤</div>
<div class='lab' style='left:640px;top:58px;font-size:58px;color:#fff;background:{INK};padding:4px 22px;border-radius:12px'>예금 vs SCHD</div>
<div id='d1' class='t' data-fit='1180' style='left:46px;top:150px;font-size:178px;color:#E5322D'>1,434만 차이</div>
{hbars2(56, 340, 500, 46, 14)}
""" + FINE2 % '#6B7280'

# r1e — 세로 막대 4개(0부터, 오른쪽) + 왼쪽 글자 세 줄. 괄호 = 예금~SCHD 차이 구간
BX, BW, BG_, HMAX2, BASE = 640, 88, 46, 400, 560
def vbars():
    s = f"<div style='position:absolute;left:{BX - 20}px;top:{BASE}px;width:{4 * (BW + BG_) + 20}px;height:5px;background:{INK}'></div>"
    for i, n in enumerate(['예금', '금', 'S&P500', 'SCHD']):
        hh = max(10, round(HMAX2 * GAIN[n] / GAIN['SCHD'])); x = BX + i * (BW + BG_)
        c = '#E5322D' if n == 'SCHD' else (INK if n == '예금' else '#C4C8CF')
        s += f"<div style='position:absolute;left:{x}px;top:{BASE - hh}px;width:{BW}px;height:{hh}px;background:{c}'></div>"
        if n in MAN: s += f"<div class='lab' style='left:{x - 6}px;top:{BASE - hh - 56}px;font-size:40px;color:{c}'>{MAN[n]}</div>"
        else: s += f"<div class='lab' style='left:{x}px;top:{BASE - hh - 40}px;font-size:28px;color:#8A909C'>{n}</div>"
    return s
r1e = f"""<div style='position:absolute;inset:0;background:#FFFFFF'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:18px;background:{INK}'></div>
<div class='t' style='left:52px;top:70px;font-size:84px;color:{INK}'>같은 1억</div>
<div class='lab' style='left:52px;top:182px;font-size:60px;color:#fff;background:{INK};padding:4px 22px;border-radius:12px'>예금 vs SCHD</div>
<div id='e1' class='t' data-fit='560' style='left:46px;top:300px;font-size:170px;color:#E5322D'>1,434만</div>
<div class='t' style='left:52px;top:486px;font-size:84px;color:{INK}'>1년 뒤 차이</div>
{vbars()}
<div class='lab' style='left:{BX - 10}px;top:{BASE + 10}px;font-size:40px;color:{INK}'>예금</div>
<div class='lab' style='left:{BX + 3 * (BW + BG_) - 8}px;top:{BASE - HMAX2 - 112}px;font-size:46px;color:#E5322D'>SCHD</div>
""" + FINE2 % '#6B7280'
VARIANTS.update({'r1d': r1d, 'r1e': r1e})


# ── 3차(10/3) — 2차 r1d 7(Claude)·7(제미나이 lite) 1위, 고칠 점: 꼬리표 1.5배·숫자 바로 위 왼쪽 / 끝값 2배·SCHD 막대 굵게 / 아래 빈칸
def hbars3(x, y, wmax, h, gap, labw=210, fs=50, vfs=62):
    top = GAIN['SCHD']; s = ''
    for i, n in enumerate(['예금', '금', 'S&P500', 'SCHD']):
        w = max(12, wmax * GAIN[n] / top); yy = y + i * (h + gap); key = n in MAN
        c = '#E5322D' if n == 'SCHD' else (INK if n == '예금' else '#C9CDD4')
        tc = INK if key else '#A0A6B0'
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + labw}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{c};border-radius:0 8px 8px 0'></div>"
        if key: s += f"<div class='t' style='left:{x + labw + w + 18:.0f}px;top:{yy + (h - vfs) / 2:.0f}px;font-size:{vfs}px;color:{c}'>{MAN[n]}</div>"
    return s


r1f = f"""<div style='position:absolute;inset:0;background:#FFFFFF'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:18px;background:{INK}'></div>
<div class='t' style='left:52px;top:46px;font-size:64px;color:{INK}'>같은 1억, 1년 뒤</div>
<div class='lab' style='left:52px;top:128px;font-size:78px;color:#fff;background:{INK};padding:2px 26px 8px;border-radius:14px'>예금 vs SCHD</div>
<div id='f1' class='t' data-fit='1180' style='left:46px;top:246px;font-size:168px;color:#E5322D'>1,434만 차이</div>
{hbars3(56, 428, 420, 44, 12)}
<div class='fine' style='left:52px;top:650px;color:#6B7280'>1년 뒤 통장 기준 · 2025.10.2 → 2026.10.2 실제 값(과거)</div>
"""
VARIANTS['r1f'] = r1f


# ── 4차(10/3) — 2차 r1d 6.67(lite 7·Claude 7·레드팀 6). 레드팀 사실 지적 2개:
#   ① 끝값 +1,653만 − +218만 = 1,435만 ≠ 1,434만(반올림 엇갈림) → 끝값 빼고 숫자 1개만(차이 14,342,653 → 1,434만)
#   ② SCHD 통장은 분배금 세전(facts 50·52행) → '통장 기준'도 세후 약속으로 읽힘 → 꼬리말에 '분배금은 세전' 그대로 밝힘
#   + 금·S&P500 이름 진하게(168px 읽힘), 흰 바탕 테두리(밝은 화면에서 묻힘 방지)
def hbars4(x, y, wmax, h, gap, labw=230, fs=50):
    top = GAIN['SCHD']; s = ''
    for i, n in enumerate(['예금', '금', 'S&P500', 'SCHD']):
        w = max(12, wmax * GAIN[n] / top); yy = y + i * (h + gap)
        c = '#E5322D' if n == 'SCHD' else (INK if n == '예금' else '#B3B8C1')
        tc = '#E5322D' if n == 'SCHD' else (INK if n == '예금' else '#5A6170')
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + labw}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{c};border-radius:0 8px 8px 0'></div>"
    return s


r1g = f"""<div style='position:absolute;inset:0;background:#FFFFFF;border:12px solid {INK}'></div>
<div class='t' style='left:52px;top:46px;font-size:64px;color:{INK}'>같은 1억, 1년 뒤</div>
<div class='lab' style='left:52px;top:128px;font-size:78px;color:#fff;background:{INK};padding:2px 26px 8px;border-radius:14px'>예금 vs SCHD</div>
<div id='g1' class='t' data-fit='1170' style='left:46px;top:246px;font-size:168px;color:#E5322D'>1,434만 차이</div>
{hbars4(56, 412, 640, 42, 12)}
<div class='fine' style='left:52px;top:648px;color:#6B7280'>2025.10.2 → 2026.10.2 실제 값(과거) · 이자·양도세 뗀 통장, 분배금은 세전</div>
"""
VARIANTS['r1g'] = r1g


# ── 5차(10/3) — 3차 r1g 7.07(제미나이 3-flash 8.2·Claude 7·레드팀 6) 통과선 7, 목표 8 미달. 고칠 점:
#   ① 굵은 먹색 테두리 = 나두시니어 굵은 테두리와 겹침 3(레드팀) → 4px 회색 ② 숫자가 가로 60% → 85%+(Claude)
#   ③ 첫 줄 168px 겨우 읽힘 → 꼬리표급 ④ 막대 굵게·아래 빈칸 없앰 ⑤ '양도세 뗀 통장'은 10/2 기준 문자 그대로는 아님(양도세는 다음 해 5월 신고, facts [15]) → '세금 계산 기준' 문구
r1h = f"""<div style='position:absolute;inset:0;background:#FFFFFF;border:4px solid #C9CDD4'></div>
<div class='t' style='left:52px;top:40px;font-size:80px;color:{INK}'>같은 1억, 1년 뒤</div>
<div class='lab' style='left:52px;top:138px;font-size:72px;color:#fff;background:{INK};padding:0 24px 8px;border-radius:14px'>예금 vs SCHD</div>
<div id='h1' class='t' data-fit='1180' style='left:44px;top:244px;font-size:200px;color:#E5322D'>1,434만 차이</div>
{hbars4(56, 452, 680, 40, 6, labw=200, fs=42)}
<div class='fine' style='left:52px;top:652px;color:#6B7280'>2025.10.2 → 2026.10.2 실제 값(과거) · 이자세·양도세 계산, 분배금은 세전</div>
"""
VARIANTS['r1h'] = r1h


# ── 6차(10/3) — 4차 r1h 6.73(lite 7.2·Claude 7·레드팀 6), r1g는 레드팀 겹침 3(굵은 먹색 틀)으로 반려.
#   r1h 남은 지적: 4px 회색 틀이 168px에서 사라져 흰 페이지에 녹음(Claude) → 바탕을 연한 미색으로 갈라놓고 틀은 3px 중간 회색
#   막대 40→48px·이름 42→예금/SCHD 56·금/S&P500 46(레드팀 '뒷걸음' 지적), 숫자는 85% 유지
def hbars6(x, y, wmax, h, gap, labw=210):
    top = GAIN['SCHD']; s = ''
    for i, n in enumerate(['예금', '금', 'S&P500', 'SCHD']):
        w = max(14, wmax * GAIN[n] / top); yy = y + i * (h + gap); key = n in ('예금', 'SCHD')
        c = '#E5322D' if n == 'SCHD' else (INK if n == '예금' else '#B3B8C1')
        tc = '#E5322D' if n == 'SCHD' else (INK if n == '예금' else '#5A6170')
        fs = 56 if key else 46
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + labw}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{c};border-radius:0 8px 8px 0'></div>"
    return s


r1i = f"""<div style='position:absolute;inset:0;background:#F3EFE6;border:3px solid #8A909C'></div>
<div class='t' style='left:52px;top:34px;font-size:78px;color:{INK}'>같은 1억, 1년 뒤</div>
<div class='lab' style='left:52px;top:126px;font-size:68px;color:#fff;background:{INK};padding:0 24px 8px;border-radius:14px'>예금 vs SCHD</div>
<div id='i1' class='t' data-fit='1180' style='left:44px;top:222px;font-size:190px;color:#E5322D'>1,434만 차이</div>
{hbars6(56, 428, 680, 48, 8)}
<div class='fine' style='left:52px;top:654px;color:#6B7280'>2025.10.2 → 2026.10.2 실제 값(과거) · 이자세·양도세 계산, 분배금은 세전</div>
"""
VARIANTS['r1i'] = r1i

# 6차(10/3 12:1x) 형식 바꾸기 — 글자 슬라이드 정체(6점대) 탈출: 통장 두 장 크기 대비(레드팀 제안, 사실에서 온 그림 장치·돈더미 사진 아님)
# 숫자는 facts [영수증] 늘어난 돈 예금 2,182,680 → '+218만' · SCHD 16,525,333 → '+1,653만'(끝값 2개, 차이 숫자는 안 씀 → 반올림 엇갈림 없음)
FOOT6 = "<div class='fine' style='left:52px;top:654px;color:%s'>2025.10.2 → 2026.10.2 실제 값(과거) · 이자세·양도세 계산, 분배금은 세전</div>"


def book(x, y, w, h, name, val, bg, fg, sub, vfs, nfs, rot=0):
    s = f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};border-radius:22px;transform:rotate({rot}deg);box-shadow:0 22px 50px rgba(0,0,0,.45);overflow:hidden'>"
    s += f"<div style='position:absolute;left:0;right:0;top:0;height:{round(h * .26)}px;background:rgba(0,0,0,.18)'></div>"
    s += f"<div class='lab' style='left:{round(w * .07)}px;top:{round(h * .05)}px;font-size:{nfs}px;color:{fg}'>{name}</div>"
    s += f"<div class='lab' style='left:{round(w * .07)}px;top:{round(h * .34)}px;font-size:{round(nfs * .62)}px;color:{sub}'>1년 동안 늘어난 돈</div>"
    s += f"<div class='t' style='left:{round(w * .06)}px;top:{round(h * .52)}px;font-size:{vfs}px;color:{fg}'>{val}</div></div>"
    return s


# r1j — 남색 바탕, 통장 두 장(예금 작게·회색 / SCHD 크게·노랑, 살짝 기울임)
r1j = f"""<div style='position:absolute;inset:0;background:#14213D'></div>
<div class='t' style='left:52px;top:36px;font-size:84px;color:#fff'>1억 넣고 1년 뒤 통장</div>
{book(52, 210, 330, 290, '예금', '+218만', '#5B6578', '#fff', '#D3D8E0', 92, 52)}
{book(430, 160, 520, 410, 'SCHD', '+1,653만', '#FFD43B', '#14213D', '#5B4A00', 112, 68, rot=-2)}
<div class='lab' style='left:56px;top:594px;font-size:34px;color:#AEB6C4'>금 +324만 · S&P500 +1,039만</div>
""" + FOOT6 % '#AEB6C4'
VARIANTS['r1j'] = r1j

# r1k — 흰 바탕, 숫자 크기 대비만(그림 없음): 작은 +218만 vs 아주 큰 +1,653만
r1k = f"""<div style='position:absolute;inset:0;background:#FFFFFF;border:3px solid #C9CDD4'></div>
<div class='t' style='left:52px;top:40px;font-size:80px;color:{INK}'>같은 1억, 1년 뒤 통장</div>
<div class='lab' style='left:56px;top:196px;font-size:54px;color:#5A6170'>예금</div>
<div class='t' style='left:56px;top:270px;font-size:100px;color:#8A909C'>+218만</div>
<div class='lab' style='left:470px;top:196px;font-size:54px;color:#E5322D'>SCHD</div>
<div id='k1' class='t' data-fit='790' style='left:462px;top:262px;font-size:240px;color:#E5322D'>+1,653만</div>
<div class='lab' style='left:56px;top:500px;font-size:44px;color:#8A909C'>금 +324만 · S&P500 +1,039만</div>
""" + FOOT6 % '#6B7280'
VARIANTS['r1k'] = r1k


# r1l — r1j 고침(6차 Claude 심사관: 카드·숫자 키우고 카드 안 작은 글씨 빼기, 제목 더 크게) · 금·S&P500 줄은 유지(골라 보여 주기 방지)
def book2(x, y, w, h, name, val, bg, fg, vfs, nfs, rot=0):
    s = f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};border-radius:24px;transform:rotate({rot}deg);box-shadow:0 22px 50px rgba(0,0,0,.5);overflow:hidden'>"
    s += f"<div style='position:absolute;left:0;right:0;top:0;height:{round(h * .30)}px;background:rgba(0,0,0,.18)'></div>"
    s += f"<div class='lab' style='left:{round(w * .07)}px;top:{round(h * .06)}px;font-size:{nfs}px;color:{fg}'>{name}</div>"
    s += f"<div class='t' style='left:{round(w * .05)}px;top:{round(h * .45)}px;font-size:{vfs}px;color:{fg}'>{val}</div></div>"
    return s


r1l = f"""<div style='position:absolute;inset:0;background:#14213D'></div>
<div class='t' style='left:48px;top:30px;font-size:100px;color:#fff'>1억 넣고 1년 뒤 통장</div>
{book2(48, 214, 340, 330, '예금', '+218만', '#5B6578', '#fff', 90, 64)}
{book2(414, 168, 548, 400, 'SCHD', '+1,653만', '#FFD43B', '#14213D', 128, 80, rot=-2)}
<div class='lab' style='left:52px;top:596px;font-size:34px;color:#AEB6C4'>금 +324만 · S&P500 +1,039만</div>
""" + FOOT6 % '#8E97A8'
VARIANTS['r1l'] = r1l


# r1m — 6차 3명 지적 합침: 어두운 고대비(Claude) + 남색·노랑·기울인 카드 뺌(레드팀 겹침 3) + '통장' 말 뺌(양도세 다음 해 5월·분배금 세전)
#   + 크기 대비 = 실제 값 비율(막대 0부터, SCHD 기준) + 4종 모두(골라 보여 주기 방지)
def mbars(x, y, wmax):
    rows = [('예금', 96, '#FFFFFF', '#FFFFFF', 64, 78), ('금', 50, '#5C6068', '#A9AEB6', 44, 44),
            ('S&P500', 50, '#5C6068', '#A9AEB6', 44, 44), ('SCHD', 96, '#2BD98C', '#2BD98C', 64, 84)]
    val = {'예금': '+218만', '금': '+324만', 'S&P500': '+1,039만', 'SCHD': '+1,653만'}
    s = ''; yy = y
    for n, h, bc, tc, fs, vfs in rows:
        w = wmax * GAIN[n] / GAIN['SCHD']
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 230}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{bc};border-radius:0 10px 10px 0'></div>"
        if n == 'SCHD':
            s += f"<div class='t' style='right:{1280 - (x + 230 + w) + 22:.0f}px;top:{yy + (h - vfs) / 2:.0f}px;font-size:{vfs}px;color:#0E1A14'>{val[n]}</div>"
        else:
            s += f"<div class='t' style='left:{x + 230 + w + 20:.0f}px;top:{yy + (h - vfs) / 2:.0f}px;font-size:{vfs}px;color:{tc}'>{val[n]}</div>"
        yy += h + 16
    return s


r1m = f"""<div style='position:absolute;inset:0;background:#1E1F22'></div>
<div class='t' style='left:52px;top:40px;font-size:104px;color:#fff'>같은 1억, 1년 뒤</div>
{mbars(52, 196, 900)}
<div class='fine' style='left:52px;top:654px;color:#8E939C'>2025.10.2 → 2026.10.2 실제 값(과거) · 늘어난 돈, 이자세·양도세 계산 · 분배금은 세전</div>
"""
VARIANTS['r1m'] = r1m


# r1n — r1m 고침(7차 레드팀: 막대 두께 같게·예금 흰 막대→테두리 / Claude: 숫자 키우기)
def nbars(x, y, wmax, h=84, gap=14):
    rows = [('예금', 'out', '#FFFFFF', 60, 88), ('금', '#4A4E56', '#A9AEB6', 48, 64),
            ('S&P500', '#4A4E56', '#A9AEB6', 48, 64), ('SCHD', '#2BD98C', '#2BD98C', 60, 78)]
    val = {'예금': '+218만', '금': '+324만', 'S&P500': '+1,039만', 'SCHD': '+1,653만'}
    s = ''; yy = y
    for n, bc, tc, fs, vfs in rows:
        w = wmax * GAIN[n] / GAIN['SCHD']
        bg = 'transparent;border:5px solid #FFFFFF;border-left:none' if bc == 'out' else bc
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 220}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{bg};border-radius:0 10px 10px 0'></div>"
        if n == 'SCHD':
            s += f"<div class='t' style='right:{1280 - (x + 220 + w) + 22:.0f}px;top:{yy + (h - vfs) / 2:.0f}px;font-size:{vfs}px;color:#0E1A14'>{val[n]}</div>"
        else:
            s += f"<div class='t' style='left:{x + 220 + w + 20:.0f}px;top:{yy + (h - vfs) / 2:.0f}px;font-size:{vfs}px;color:{tc}'>{val[n]}</div>"
        yy += h + gap
    return s


r1n = f"""<div style='position:absolute;inset:0;background:#1E1F22'></div>
<div class='t' style='left:52px;top:36px;font-size:108px;color:#fff'>같은 1억, 1년 뒤</div>
{nbars(52, 186, 900)}
<div class='fine' style='left:52px;top:654px;color:#8E939C'>2025.10.2 → 2026.10.2 실제 값(과거) · 늘어난 돈, 이자세·양도세 계산 · 분배금은 세전</div>
"""
VARIANTS['r1n'] = r1n


# r1o — 8차 지적 합침: 내 돈 대입 제목(레드팀 궁금증 장치·우리 정체성) + 숫자 1.3배·막대 굵게(Claude) + 예금 흰 채움(두께 같아 면적 왜곡 없음)
def obars(x, y, wmax, h=92, gap=6):
    rows = [('예금', '#FFFFFF', '#FFFFFF', 62, 104), ('금', '#4A4E56', '#A9AEB6', 50, 72),
            ('S&P500', '#4A4E56', '#A9AEB6', 50, 72), ('SCHD', '#2BD98C', '#2BD98C', 62, 84)]
    val = {'예금': '+218만', '금': '+324만', 'S&P500': '+1,039만', 'SCHD': '+1,653만'}
    s = ''; yy = y
    for n, bc, tc, fs, vfs in rows:
        w = wmax * GAIN[n] / GAIN['SCHD']
        s += f"<div class='lab' style='left:{x}px;top:{yy + (h - fs) / 2 - 6:.0f}px;font-size:{fs}px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 220}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{bc};border-radius:0 10px 10px 0'></div>"
        if n == 'SCHD':
            s += f"<div class='t' style='right:{1280 - (x + 220 + w) + 22:.0f}px;top:{yy + (h - vfs) / 2 + 4:.0f}px;font-size:{vfs}px;color:#0E1A14'>{val[n]}</div>"
        else:
            s += f"<div class='t' style='left:{x + 220 + w + 18:.0f}px;top:{yy + (h - vfs) / 2 + 2:.0f}px;font-size:{vfs}px;color:{tc}'>{val[n]}</div>"
        yy += h + gap
    return s


r1o = f"""<div style='position:absolute;inset:0;background:#1E1F22'></div>
<div class='t' style='left:48px;top:30px;font-size:100px;color:#fff'>1년 전 내 1억이었다면</div>
{obars(52, 180, 880)}
<div class='fine' style='left:52px;top:654px;color:#8E939C'>2025.10.2 → 2026.10.2 실제 값(과거) · 늘어난 돈, 이자세·양도세 계산 · 분배금은 세전</div>
"""
VARIANTS['r1o'] = r1o


# r1p — 9차 레드팀 '진짜 궁금증 장치 + 실물 그림' 시험: 예금 통장 한 장(그림, 사진 아님)에 +218만만 크게,
#   나머지 셋은 숫자 없이 실제 비율 막대만('다른 셋은?') → 답 하나 숨김. '내 1억이었다면' 후회 말투 뺌(레드팀 9차 ②)
def pbars(x, y, wmax, h=50, gap=12):
    rows = [('예금', '#FFFFFF', '#FFFFFF'), ('금', '#6A6F78', '#A9AEB6'), ('S&P500', '#6A6F78', '#A9AEB6'), ('SCHD', '#2BD98C', '#2BD98C')]
    s = ''; yy = y
    for n, bc, tc in rows:
        w = wmax * GAIN[n] / GAIN['SCHD']
        s += f"<div class='lab' style='left:{x}px;top:{yy + 2}px;font-size:40px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 180}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{bc};border-radius:0 8px 8px 0'></div>"
        yy += h + gap
    return s


r1p = f"""<div style='position:absolute;inset:0;background:#1E1F22'></div>
<div class='t' style='left:48px;top:30px;font-size:100px;color:#fff'>같은 1억, 1년 뒤</div>
<div style='position:absolute;left:48px;top:178px;width:520px;height:400px;background:#F4F1E8;border-radius:18px;box-shadow:0 18px 40px rgba(0,0,0,.5);overflow:hidden'>
 <div style='position:absolute;left:0;right:0;top:0;height:92px;background:#5C6068'></div>
 <div class='lab' style='left:34px;top:18px;font-size:52px;color:#fff'>예금 통장</div>
 <div style='position:absolute;left:34px;right:34px;top:150px;border-top:3px solid #D5D0C4'></div>
 <div style='position:absolute;left:34px;right:34px;top:330px;border-top:3px solid #D5D0C4'></div>
 <div class='lab' style='left:34px;top:110px;font-size:34px;color:#5A6170'>1년 이자(세후)</div>
 <div class='t' style='left:26px;top:180px;font-size:136px;color:{INK}'>+218만</div>
</div>
<div class='t' style='left:640px;top:190px;font-size:88px;color:#2BD98C'>다른 셋은?</div>
{pbars(640, 318, 400)}
<div class='fine' style='left:52px;top:654px;color:#8E939C'>2025.10.2 → 2026.10.2 실제 값(과거) · 막대 = 세금 뗀 뒤 늘어난 돈</div>
"""
VARIANTS['r1p'] = r1p


# r1q — r1p 고침(10차 세 명 공통: 오른쪽 막대 키우기 / 레드팀·Claude: 통장으로 알아볼 장치·카드 빈 공간 줄이기)
def qbars(x, y, wmax, h=60, gap=8):
    rows = [('예금', '#FFFFFF', '#FFFFFF'), ('금', '#6A6F78', '#A9AEB6'), ('S&P500', '#6A6F78', '#A9AEB6'), ('SCHD', '#2BD98C', '#2BD98C')]
    s = ''; yy = y
    for n, bc, tc in rows:
        w = wmax * GAIN[n] / GAIN['SCHD']
        s += f"<div class='lab' style='left:{x}px;top:{yy + 6}px;font-size:44px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 190}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{bc};border-radius:0 8px 8px 0'></div>"
        yy += h + gap
    return s


lines = ''.join(f"<div style='position:absolute;left:30px;right:30px;top:{t}px;border-top:2px solid #D5D0C4'></div>" for t in (150, 300, 336))
r1q = f"""<div style='position:absolute;inset:0;background:#1E1F22'></div>
<div class='t' style='left:48px;top:30px;font-size:108px;color:#fff'>같은 1억, 1년 뒤</div>
<div style='position:absolute;left:48px;top:186px;width:480px;height:372px;background:#F4F1E8;border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.5);overflow:hidden'>
 <div style='position:absolute;left:0;right:0;top:0;height:86px;background:#5C6068'></div>
 <div style='position:absolute;left:0;top:0;bottom:0;width:14px;background:repeating-linear-gradient(#C9C3B4 0 10px,#F4F1E8 10px 20px)'></div>
 <div class='lab' style='left:34px;top:16px;font-size:50px;color:#fff'>예금 통장</div>
 <div style='position:absolute;right:26px;top:14px;width:58px;height:58px;border:4px solid #E5322D;border-radius:50%'></div>
 <div class='lab' style='left:34px;top:100px;font-size:34px;color:#5A6170'>1년 이자(세후)</div>
 {lines}
 <div class='t' style='left:28px;top:168px;font-size:128px;color:{INK}'>+218만</div>
</div>
<div class='t' style='left:572px;top:186px;font-size:96px;color:#2BD98C'>다른 셋은?</div>
{qbars(572, 300, 460)}
<div class='fine' style='left:52px;top:654px;color:#8E939C'>2025.10.2 → 2026.10.2 실제 값(과거) · 막대 = 세금 뗀 뒤 늘어난 돈</div>
"""
VARIANTS['r1q'] = r1q


# r1r — 11차 지적: 아래 빈 띠 메우기·카드 숫자 키우기(Claude), 막대 라벨 줄이고 막대 길게(레드팀), 좌우 시인성(제미나이)
def rbars(x, y, wmax, h=62, gap=6):
    rows = [('예금', '#FFFFFF', '#FFFFFF'), ('금', '#6A6F78', '#A9AEB6'), ('S&P500', '#6A6F78', '#A9AEB6'), ('SCHD', '#2BD98C', '#2BD98C')]
    s = ''; yy = y
    for n, bc, tc in rows:
        w = wmax * GAIN[n] / GAIN['SCHD']
        s += f"<div class='lab' style='left:{x}px;top:{yy + 12}px;font-size:36px;color:{tc}'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 164}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:{bc};border-radius:0 8px 8px 0'></div>"
        yy += h + gap
    return s


r1r = f"""<div style='position:absolute;inset:0;background:#1E1F22'></div>
<div class='t' style='left:44px;top:26px;font-size:112px;color:#fff'>같은 1억, 1년 뒤</div>
<div style='position:absolute;left:44px;top:168px;width:500px;height:452px;background:#F4F1E8;border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.5);overflow:hidden'>
 <div style='position:absolute;left:0;right:0;top:0;height:104px;background:#4B5563'></div>
 <div class='lab' style='left:30px;top:20px;font-size:62px;color:#fff'>예금 통장</div>
 <div class='lab' style='left:30px;top:124px;font-size:48px;color:{INK}'>1년 이자(세후)</div>
 <div style='position:absolute;left:24px;right:24px;top:196px;border-top:3px solid #CFC9BA'></div>
 <div class='t' style='left:18px;top:236px;font-size:138px;color:{INK}'>+218만</div>
</div>
<div class='t' style='left:584px;top:172px;font-size:104px;color:#2BD98C'>다른 셋은?</div>
{rbars(584, 298, 460)}
<div class='fine' style='left:52px;top:654px;color:#8E939C'>2025.10.2 → 2026.10.2 실제 값(과거) · 막대 = 세금 뗀 뒤 늘어난 돈</div>
"""
VARIANTS['r1r'] = r1r



# r1s·r1t — 13차(10/3 13:2x, 새 숫자) 두 심사 공통: 'SCHD 막대가 답을 미리 보여 궁금증을 죽인다'·작은 글씨 걷기·미래 보장 아님(레드팀)
#   r1s = 막대 대신 '?' 상자 셋(답 완전 숨김) · r1t = 막대 같은 회색·끝에 '?'(순서는 보이되 색으로 정답 강조 안 함)
def sboxes(x, y):
    s = ''
    for i, n in enumerate(('금', 'S&P500', 'SCHD')):
        xx = x + i * 214
        s += f"<div style='position:absolute;left:{xx}px;top:{y}px;width:196px;height:250px;background:#2A2C31;border:4px solid #FFD43B;border-radius:16px'></div>"
        s += f"<div class='t' style='left:{xx}px;width:196px;text-align:center;top:{y + 40}px;font-size:150px;color:#FFD43B'>?</div>"
        s += f"<div class='lab' style='left:{xx}px;width:196px;text-align:center;top:{y + 192}px;font-size:{40 if len(n) < 4 else 34}px;color:#fff'>{n}</div>"
    return s


CARD = lambda top, h, nfs: f"""<div style='position:absolute;left:40px;top:{top}px;width:560px;height:{h}px;background:#F4F1E8;border-radius:16px;overflow:hidden'>
 <div style='position:absolute;left:0;right:0;top:0;height:100px;background:#4B5563'></div>
 <div class='lab' style='left:30px;top:18px;font-size:62px;color:#fff'>예금 통장 1년</div>
 <div class='t' style='left:20px;top:214px;font-size:{nfs}px;color:{INK}'>+218만</div>
</div>"""
FINE2 = "<div class='fine' style='left:44px;top:654px;color:#8E939C'>2025.10→2026.10 과거 값 · 세금 뗀 뒤 · 미래 보장 아님</div>"
r1s = f"""<div style='position:absolute;inset:0;background:#111214'></div>
<div class='t' style='left:40px;top:28px;font-size:92px;color:#fff'>같은 1억, 1년 뒤</div>
{CARD(166, 440, 168)}
<div class='t' style='left:640px;top:180px;font-size:96px;color:#FFD43B'>다른 셋은?</div>
{sboxes(640, 312)}
{FINE2}
"""
VARIANTS['r1s'] = r1s


def tbars(x, y, wmax, h=74, gap=10):
    s = ''; yy = y
    for n in ('금', 'S&P500', 'SCHD'):
        w = wmax * GAIN[n] / GAIN['SCHD']
        s += f"<div class='lab' style='left:{x}px;top:{yy + 14}px;font-size:42px;color:#fff'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + 180}px;top:{yy}px;width:{w:.0f}px;height:{h}px;background:#6A6F78;border-radius:0 8px 8px 0'></div>"
        s += f"<div class='t' style='left:{x + 180 + w + 14:.0f}px;top:{yy + 4}px;font-size:66px;color:#FFD43B'>?</div>"
        yy += h + gap
    return s


r1t = f"""<div style='position:absolute;inset:0;background:#111214'></div>
<div class='t' style='left:40px;top:28px;font-size:92px;color:#fff'>같은 1억, 1년 뒤</div>
{CARD(166, 440, 168)}
<div class='t' style='left:640px;top:180px;font-size:96px;color:#FFD43B'>다른 셋은?</div>
{tbars(640, 320, 340)}
{FINE2}
"""
VARIANTS['r1t'] = r1t


# r1u — 14차: r1s 1위(레드팀 8)지만 겹침 4(노랑·통장 카드·1억·물음표) → 노랑을 우리 초록으로, 통장 카드 모양 뺌,
#   '세후'를 숫자 바로 위 큰 글씨로(레드팀 ①), 상자 글씨 키움(Claude: 168px에서 금·S&P500·SCHD 안 읽힘)
def uboxes(x, y, c='#2BD98C'):
    s = ''
    for i, n in enumerate(('금', 'S&P500', 'SCHD')):
        xx = x + i * 196
        s += f"<div style='position:absolute;left:{xx}px;top:{y}px;width:182px;height:262px;background:#1B2A23;border:5px solid {c};border-radius:16px'></div>"
        s += f"<div class='t' style='left:{xx}px;width:182px;text-align:center;top:{y + 26}px;font-size:150px;color:{c}'>?</div>"
        s += f"<div class='t' style='left:{xx}px;width:182px;text-align:center;top:{y + 194}px;font-size:{52 if len(n) < 4 else 40}px;color:#fff'>{n}</div>"
    return s


r1u = f"""<div style='position:absolute;inset:0;background:#111214'></div>
<div class='t' style='left:40px;top:28px;font-size:92px;color:#fff'>같은 1억, 1년 뒤</div>
<div style='position:absolute;left:40px;top:186px;width:10px;height:400px;background:#fff'></div>
<div class='lab' style='left:72px;top:190px;font-size:58px;color:#C9CDD3'>예금 이자(세후)</div>
<div class='t' style='left:64px;top:312px;font-size:172px;color:#fff'>+218만</div>
<div class='t' style='left:690px;top:186px;font-size:92px;color:#2BD98C'>다른 셋은?</div>
{uboxes(690, 312)}
{FINE2}
"""
VARIANTS['r1u'] = r1u


# r1v — 15차(r1u 7.00·겹침 2): Claude·레드팀 공통 '밝은 면 되돌리기'(통장 머리띠·카드 모양 없이 면만), 라벨 흰색·짧게,
#   상자 라벨 글꼴 통일(PD 굵은 고딕), '?' 상자 안을 초록으로 채워 반전
def vboxes(x, y, c='#2BD98C'):
    s = ''
    for i, n in enumerate(('금', 'S&P500', 'SCHD')):
        xx = x + i * 196
        s += f"<div style='position:absolute;left:{xx}px;top:{y}px;width:182px;height:262px;background:{c};border-radius:16px'></div>"
        s += f"<div class='t' style='left:{xx}px;width:182px;text-align:center;top:{y + 26}px;font-size:150px;color:#0F1720'>?</div>"
        s += f"<div class='lab' style='left:{xx}px;width:182px;text-align:center;top:{y + 192}px;font-size:{50 if len(n) < 4 else 38}px;color:#0F1720'>{n}</div>"
    return s


r1v = f"""<div style='position:absolute;inset:0;background:#111214'></div>
<div class='t' style='left:40px;top:28px;font-size:92px;color:#fff'>같은 1억, 1년 뒤</div>
<div style='position:absolute;left:40px;top:186px;width:610px;height:420px;background:#F4F1E8;border-radius:12px'></div>
<div class='lab' style='left:72px;top:212px;font-size:60px;color:{INK}'>예금 1년 (세후)</div>
<div class='t' style='left:58px;top:330px;font-size:176px;color:{INK}'>+218만</div>
<div class='t' style='left:690px;top:186px;font-size:92px;color:#2BD98C'>다른 셋은?</div>
{vboxes(690, 312)}
{FINE2}
"""
VARIANTS['r1v'] = r1v


# r1w·r1x — 2026-10-05 09:4x 벤치마크 규칙 3개(thumb-bench.md: 그래픽 화면 절반 이상 · 바탕색 지난 편과 다르게 · 보조 글 큰 줄의 60% 이상)
#   + 16차 Claude 8점 조건(① '?' 상자 셋 → 큰 상자 하나 ② 맨 위 줄 줄이고 +218만 키움) · 레드팀('1억'만 초록)
# r1w = 크림 바탕(지난 6편 남색·검정과 다름), 두 카드가 화면 85%: 예금 +218만(먹색 카드) vs 1등은?(초록 카드, 이름·숫자 숨김)
r1w = f"""<div style='position:absolute;inset:0;background:#F4F1E8'></div>
<div class='t' style='left:44px;top:34px;font-size:84px;color:{INK}'>같은 <span style="color:#14A86A">1억</span>, 1년 뒤</div>
<div style='position:absolute;left:40px;top:160px;width:640px;height:450px;background:#14181F;border-radius:20px'></div>
<div class='lab' style='left:76px;top:190px;font-size:72px;color:#fff'>예금 (세후)</div>
<div class='t' style='left:62px;top:340px;font-size:184px;color:#fff'>+218만</div>
<div style='position:absolute;left:704px;top:160px;width:536px;height:400px;background:#2BD98C;border-radius:20px'></div>
<div class='lab' style='left:704px;width:536px;text-align:center;top:190px;font-size:72px;color:{INK}'>1등은?</div>
<div class='t' style='left:704px;width:536px;text-align:center;top:320px;font-size:170px;color:{INK}'>+???만</div>
<div class='fine' style='left:44px;top:640px;color:#6B7280'>2025.10→2026.10 과거 값 · 세금 뗀 뒤 · 미래 보장 아님</div>
"""
VARIANTS['r1w'] = r1w

# r1x = 흰 바탕, 0원부터 실제 비율 막대 2개(예금 2,182,680 vs 1등 15,987,335 = 7.32배 → '7배 넘게').
#   큰 숫자는 하나(7배), 예금 +218만은 보조(큰 줄 60% 이상), 1등 이름은 '?'로 숨김(질문 + 반전)
R = GAIN['SCHD'] / GAIN['예금']; assert 7 < R < 7.5, R
BW = 1000; bw_dep = round(BW / R)
r1x = f"""<div style='position:absolute;inset:0;background:#FFFFFF'></div>
<div class='t' style='left:44px;top:40px;font-size:86px;color:{INK}'>같은 1억, <span style="color:#E8382F">1등은 7배 넘게</span></div>
<div class='lab' style='left:48px;top:196px;font-size:64px;color:{INK}'>예금 (세후)</div>
<div style='position:absolute;left:48px;top:282px;width:{bw_dep}px;height:110px;background:#14181F;border-radius:0 12px 12px 0'></div>
<div class='t' style='left:{48 + bw_dep + 20}px;top:290px;font-size:96px;color:{INK}'>+218만</div>
<div style='position:absolute;left:48px;top:420px;width:{BW}px;height:140px;background:#2BD98C;border-radius:0 14px 14px 0'></div>
<div class='t' style='left:76px;top:432px;font-size:116px;color:{INK}'>1등 = ?</div>
<div class='fine' style='left:48px;top:640px;color:#6B7280'>세후 늘어난 돈, 0원부터 · 2025.10→2026.10 과거 값 · 미래 보장 아님</div>
"""
VARIANTS['r1x'] = r1x

# r1y — 17차(r1v 1위 유지, r1w·r1x 반려: 후보 이름을 숨기면 주제가 안 읽힘 · '1등' = 파킹통장 경쟁 겹침 3)
#   r1v 틀 유지 + 보조 글 60% 규칙(Claude·레드팀 공통 '168px 라벨 안 읽힘'): 큰 숫자 150px, 라벨 92px,
#   오른쪽 '?' 상자 셋 → 이름이 큰 가로 줄 셋(이름 84px + '?' 상자, 길이 같음 = 답 숨김)
def yrows(x, y, w=560, h=118, gap=16, c='#2BD98C'):
    s = ''
    for i, n in enumerate(('금', 'S&P500', 'SCHD')):
        yy = y + i * (h + gap)
        s += f"<div style='position:absolute;left:{x}px;top:{yy}px;width:{w}px;height:{h}px;background:#22262E;border-radius:14px'></div>"
        s += f"<div class='lab' style='left:{x + 26}px;top:{yy + 10}px;font-size:84px;color:#fff'>{n}</div>"
        s += f"<div style='position:absolute;left:{x + w - 150}px;top:{yy + 12}px;width:134px;height:{h - 24}px;background:{c};border-radius:10px'></div>"
        s += f"<div class='t' style='left:{x + w - 150}px;width:134px;text-align:center;top:{yy + 16}px;font-size:88px;color:{INK}'>?</div>"
    return s


r1y = f"""<div style='position:absolute;inset:0;background:#111214'></div>
<div class='t' style='left:40px;top:30px;font-size:84px;color:#fff'>같은 <span style="color:#2BD98C">1억</span>, 1년 뒤</div>
<div style='position:absolute;left:40px;top:160px;width:600px;height:390px;background:#F4F1E8;border-radius:16px'></div>
<div class='lab' style='left:70px;top:180px;font-size:92px;color:{INK}'>예금 세후</div>
<div class='t' style='left:58px;top:340px;font-size:150px;color:{INK}'>+218만</div>
{yrows(670, 160)}
<div class='fine' style='left:44px;top:600px;color:#8E939C'>2025.10→2026.10 과거 값 · 세금 뗀 뒤 · 미래 보장 아님</div>
"""
VARIANTS['r1y'] = r1y

# r1z — 18차(r1v·r1y 둘 다 6.50): Claude '맨 위 줄은 제목과 같은 말 → 빼고 +218만 되돌리기', 레드팀 "'?' → '+???만'(같은 단위)·아래 빈 띠 줄이기"
#   '1억'은 카드 라벨로 옮김(1억 예금 세후 92px = 큰 숫자 160px의 58%→ 96px로 60%)
def zrows(x, y, w=580, h=158, gap=18, c='#2BD98C'):
    s = ''
    for i, n in enumerate(('금', 'S&P500', 'SCHD')):
        yy = y + i * (h + gap)
        s += f"<div style='position:absolute;left:{x}px;top:{yy}px;width:{w}px;height:{h}px;background:#22262E;border-radius:16px'></div>"
        s += f"<div class='lab' style='left:{x + 24}px;top:{yy + 30}px;font-size:{84 if len(n) < 4 else 72}px;color:#fff'>{n}</div>"
        s += f"<div class='t' style='right:{1280 - x - w + 22}px;top:{yy + 32}px;font-size:96px;color:{c}'>???만</div>"
    return s


r1z = f"""<div style='position:absolute;inset:0;background:#111214'></div>
<div style='position:absolute;left:36px;top:40px;width:620px;height:510px;background:#F4F1E8;border-radius:18px'></div>
<div class='lab' style='left:66px;top:70px;font-size:96px;color:{INK}'><span style="color:#14A86A">1억</span> 예금</div>
<div class='lab' style='left:66px;top:186px;font-size:96px;color:{INK}'>세후 1년</div>
<div class='t' style='left:52px;top:346px;font-size:164px;color:{INK}'>+218만</div>
{zrows(676, 40)}
<div class='fine' style='left:40px;top:590px;color:#8E939C'>2025.10→2026.10 과거 값 · 세금 뗀 뒤 · 미래 보장 아님</div>
"""
VARIANTS['r1z'] = r1z

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
            pg.goto('file:///' + html.replace('\\', '/')); pg.wait_for_selector('body[data-ready]')
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
