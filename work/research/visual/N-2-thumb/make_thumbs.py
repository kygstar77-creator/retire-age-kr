# N-2 '세전 월급 450만원, 같은 나이끼리' 썸네일 시안 (2026-10-14 visual-designer)
# 문구: ep/N-2/copy/titles.md 1위 — 큰 글 '스물일곱엔 상위 13% / 마흔둘엔 42%', 작은 줄 '세전 월 450만원 · 같은 나이 일자리'(떼지 말 것)
# 숫자: calc_out.txt [X] 25~29세 12.6%·40~44세 42.2% → 13%·42% (assert)
# 피한 것: 경쟁 5(사진+아래 노랑/초록 테두리 글) · 우리 N-1(검은 바탕+가로 게이지) — 주제 사물 = 급여명세서 한 장(같은 월급)
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, '..', '..', 'longform', 'ep', 'N-2')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
P27 = float(re.search(r'25~29세: 상위 ([\d.]+)%', calc).group(1)); P42 = float(re.search(r'40~44세: 상위 ([\d.]+)%', calc).group(1))
assert (round(P27), round(P42)) == (13, 42), (P27, P42)
A, B = f'{round(P27)}%', f'{round(P42)}%'
SMALL = '세전 월 450만원 · 같은 나이 일자리'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
SH = 'text-shadow:0 5px 0 rgba(0,0,0,.35)'


def slip(x, y, w, h, rot=0, big='450만원', top='세전 월급'):
    """급여명세서 한 장 — 글자는 '세전 월급'·'450만원'뿐, 나머지 줄은 회색 막대"""
    rows = ''.join(f"<div style='position:absolute;left:{w*0.1:.0f}px;top:{h*0.56+i*h*0.09:.0f}px;width:{w*(0.8 if i%2==0 else 0.55):.0f}px;height:{h*0.035:.0f}px;background:#D5D9E0;border-radius:4px'></div>" for i in range(4))
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#FFFFFF;border-radius:14px;"
            f"box-shadow:0 16px 0 rgba(0,0,0,.28);transform:rotate({rot}deg)'>"
            f"<div style='position:absolute;left:0;top:0;width:{w}px;height:{h*0.06:.0f}px;background:#2B6BE4;border-radius:14px 14px 0 0'></div>"
            f"<div class='t' style='left:{w*0.1:.0f}px;top:{h*0.12:.0f}px;font-size:{h*0.1:.0f}px;color:#6B7280'>{top}</div>"
            f"<div class='t' style='left:{w*0.08:.0f}px;top:{h*0.27:.0f}px;font-size:{h*0.2:.0f}px;color:#14171C'>{big}</div>{rows}</div>")


V = {}
# n2a — 코발트 바탕, 왼쪽 큰 두 줄, 오른쪽 기울인 명세서
V['n2a'] = f"""<div style='position:absolute;inset:0;background:#1F3FBF'></div>
<div class='t' style='left:48px;top:70px;font-size:96px;color:#FFFFFF;{SH}'>스물일곱엔</div>
<div class='t' style='left:44px;top:178px;font-size:150px;color:#FFD23F;{SH}'>상위 {A}</div>
<div class='t' style='left:48px;top:360px;font-size:96px;color:#FFFFFF;{SH}'>마흔둘엔</div>
<div class='t' style='left:44px;top:466px;font-size:150px;color:#BFD0FF;{SH}'>{B}</div>
<div class='lab' style='left:52px;top:640px;font-size:34px;color:#DCE4FF'>{SMALL}</div>
{slip(800, 90, 400, 440, rot=5)}
"""
# n2c — 위 노랑 판(스물일곱)·아래 남색 판(마흔둘), 같은 명세서 한 장이 두 판에 걸침 = 같은 월급
V['n2c'] = f"""<div style='position:absolute;left:0;top:0;width:1280px;height:330px;background:#FFD23F'></div>
<div style='position:absolute;left:0;top:330px;width:1280px;height:390px;background:#18233F'></div>
<div class='t' style='left:46px;top:46px;font-size:92px;color:#14171C'>스물일곱엔</div>
<div class='t' style='left:42px;top:150px;font-size:156px;color:#D7261E'>상위 {A}</div>
<div class='t' style='left:46px;top:366px;font-size:92px;color:#FFFFFF'>마흔둘엔</div>
<div class='t' style='left:42px;top:470px;font-size:156px;color:#9FB4E8'>{B}</div>
<div class='lab' style='left:50px;top:640px;font-size:34px;color:#C9D3E6'>{SMALL}</div>
{slip(830, 70, 380, 450, rot=-4)}
"""
# n2b — 밝은 하늘 바탕, 명세서를 가운데 위 가로로 크게, 아래 두 칸(나이 · %) 좌우 — 화살표 없음(시간 흐름 오독 금지)
V['n2b'] = f"""<div style='position:absolute;inset:0;background:#DDEBFF'></div>
<div style='position:absolute;left:40px;top:28px;width:1200px;height:190px;background:#FFFFFF;border-radius:20px;box-shadow:0 12px 0 rgba(20,30,60,.18)'></div>
<div style='position:absolute;left:40px;top:28px;width:22px;height:190px;background:#2B6BE4;border-radius:20px 0 0 20px'></div>
<div class='t' style='left:96px;top:72px;font-size:112px;color:#14171C'>세전 월 450만원</div>
<div class='lab' style='left:880px;top:76px;font-size:40px;color:#6B7280'>같은 나이</div><div class='lab' style='left:880px;top:128px;font-size:40px;color:#6B7280'>일자리</div>
<div style='position:absolute;left:40px;top:250px;width:580px;height:400px;background:#14171C;border-radius:24px'></div>
<div style='position:absolute;left:660px;top:250px;width:580px;height:300px;background:#FFFFFF;border-radius:24px'></div>
<div class='t' style='left:40px;top:282px;width:580px;text-align:center;font-size:84px;color:#FFFFFF'>스물일곱엔</div>
<div class='t' style='left:40px;top:410px;width:580px;text-align:center;font-size:180px;color:#FFD23F'><span style='font-size:90px'>상위 </span>{A}</div>
<div class='t' style='left:660px;top:282px;width:580px;text-align:center;font-size:84px;color:#14171C'>마흔둘엔</div>
<div class='t' style='left:660px;top:380px;width:580px;text-align:center;font-size:150px;color:#6B7280'>{B}</div>
"""
assert all(A in v and B in v for v in V.values())

# ── 2차(10/14 17:3x) — 1차 세 명: n2c 6.82(제미나이 8·7.5·Claude 6.4·레드팀 6.3)·n2a 6.57·n2b 6.43, 통과 0.
#    공통: 위아래 쌓기 = '27→42 나이 들면 떨어짐' 시간 흐름 오독(레드팀 높음) · 42%가 약함(옅은 색) · 42% 앞 '상위' 없어 '하위 42%' 오독(Claude·레드팀)
#    · 작은 줄 '같은 나이 일자리' 168px 안 읽힘 · 명세서 '세전' 안 읽혀 실수령 오독 · 빨간 13% = 나쁜 값 · 검은 카드+노랑 = N-1 닮음.
#    처방: 좌우 두 판 같은 크기·같은 굵기 숫자, 위 띠에 '세전 월 450만원'(크게)+'같은 나이 일자리'(60px), 명세서는 띠 안 작은 아이콘(글자 없음), 빨강·검정 판 없음.
#    '상위 42%'는 titles.md 2위 썸네일 말('마흔둘엔 상위 42%') — 1위 문구에 낱말 하나 더함, copywriter 승인 필요(n2f = 원문 대조판).
def icon(x, y, h):
    w = h * 0.78
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w:.0f}px;height:{h}px;background:#fff;border-radius:8px;box-shadow:0 6px 0 rgba(0,0,0,.25)'>"
            f"<div style='position:absolute;left:0;top:0;width:{w:.0f}px;height:{h*0.12:.0f}px;background:#2B6BE4;border-radius:8px 8px 0 0'></div>"
            + ''.join(f"<div style='position:absolute;left:{w*0.14:.0f}px;top:{h*(0.26+i*0.17):.0f}px;width:{w*(0.72 if i%2==0 else 0.48):.0f}px;height:{h*0.07:.0f}px;background:#C9CFDA;border-radius:3px'></div>" for i in range(4))
            + "</div>")


def two(c1, c2, ink1, ink2, sub1, sub2, top='#FFFFFF', topink='#14171C', bg='#0E2A66', b2=f'상위 {B}', gauge=False):
    g = ''
    if gauge:  # 순위 막대(위=상위 0%, 아래=100%): 실제 비율 자리에 표시
        for x0, pct, col in ((560, P27, ink1), (1170, P42, ink2)):
            y0, hh = 230, 340
            g += (f"<div style='position:absolute;left:{x0}px;top:{y0}px;width:16px;height:{hh}px;background:rgba(255,255,255,.35);border-radius:8px'></div>"
                  f"<div style='position:absolute;left:{x0-10}px;top:{y0+hh*pct/100-8:.0f}px;width:36px;height:16px;background:{col};border-radius:8px'></div>")
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:200px;background:{top}'></div>
{icon(40, 26, 148)}
<div class='t' style='left:184px;top:30px;font-size:100px;color:{topink}'>세전 월 450만원</div>
<div class='t' style='left:188px;top:138px;font-size:50px;color:#4A5568'>같은 나이 일자리</div>
<div style='position:absolute;left:24px;top:216px;width:604px;height:470px;background:{c1};border-radius:22px'></div>
<div style='position:absolute;left:652px;top:216px;width:604px;height:370px;background:{c2};border-radius:22px'></div>
<div class='t' style='left:24px;top:240px;width:604px;text-align:center;font-size:84px;color:{sub1}'>스물일곱엔</div>
<div class='t' style='left:24px;top:350px;width:604px;text-align:center;font-size:172px;color:{ink1}'><span style='font-size:92px'>상위 </span>{A}</div>
<div class='t' style='left:652px;top:240px;width:604px;text-align:center;font-size:84px;color:{sub2}'>마흔둘엔</div>
<div class='t' style='left:652px;top:350px;width:604px;text-align:center;font-size:172px;color:{ink2}'>{b2.replace('상위 ', "<span style='font-size:92px'>상위 </span>")}</div>
{g}"""


V['n2d'] = two('#FFD23F', '#2B6BE4', '#14171C', '#FFFFFF', '#3A3220', '#DCE6FF')
V['n2e'] = two('#9FD3FF', '#2B6BE4', '#0E2A66', '#FFFFFF', '#1E3A66', '#DCE6FF', top='#F4F7FB', bg='#0E2A66')
V['n2f'] = two('#FFD23F', '#2B6BE4', '#14171C', '#FFFFFF', '#3A3220', '#DCE6FF', b2=B)
assert all(A in V[k] and B in V[k] for k in ('n2d', 'n2e', 'n2f')) and '상위 ' + B not in V['n2f']

# ── 3차(10/14 17:5x) — 2차 세 명: n2f 6.75(제미나이 7.5·7·Claude 6.3·레드팀 6.7)·n2d 6.63(6·5·6.8·7.6 레드팀 유일 통과)·n2c 6.43·n2e. 통과 0.
#    공통: 카드 높이가 달라 '13이 42보다 큰 막대'로 읽힘(레드팀·Claude) · '같은 나이 일자리' 168px에서 안 보임(셋 다) · 42% '상위' 없으면 무엇의 42%인지 흐림(Claude·레드팀, 제미나이는 원문판 선호).
#    처방: 두 카드 같은 높이(아래 끝 y 560, 오른쪽 아래 비움) · '같은 나이 일자리'를 왼쪽 아래 흰 큰 글씨(62px)로 · 위 띠는 '세전 월 450만원'만 크게.
def three(b2=f'상위 {B}', cond_top=False, c2='#2B6BE4'):
    cond = ("<div class='t' style='left:188px;top:138px;font-size:56px;color:#1E3A8A'>같은 나이 일자리</div>" if cond_top else
            "<div class='t' style='left:40px;top:594px;font-size:64px;color:#FFFFFF'>같은 나이 일자리</div>")
    big = 100 if cond_top else 118; ty = 30 if cond_top else 40
    return f"""<div style='position:absolute;inset:0;background:#0E2A66'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:200px;background:#FFFFFF'></div>
{icon(40, 26, 148)}
<div class='t' style='left:184px;top:{ty}px;font-size:{big}px;color:#14171C'>세전 월 450만원</div>{cond}
<div style='position:absolute;left:24px;top:216px;width:604px;height:350px;background:#FFD23F;border-radius:22px'></div>
<div style='position:absolute;left:652px;top:216px;width:604px;height:350px;background:{c2};border-radius:22px'></div>
<div class='t' style='left:24px;top:240px;width:604px;text-align:center;font-size:84px;color:#3A3220'>스물일곱엔</div>
<div class='t' style='left:24px;top:358px;width:604px;text-align:center;font-size:172px;color:#14171C'><span style='font-size:92px'>상위 </span>{A}</div>
<div class='t' style='left:652px;top:240px;width:604px;text-align:center;font-size:84px;color:#DCE6FF'>마흔둘엔</div>
<div class='t' style='left:652px;top:358px;width:604px;text-align:center;font-size:172px;color:#FFFFFF'>{b2.replace('상위 ', "<span style='font-size:92px'>상위 </span>")}</div>"""


V['n2g'] = three()
V['n2h'] = three(cond_top=True)
V['n2i'] = three(b2=B)

# ── 4차(10/14 18:1x) — 3차: 제미나이 n2i 8·8·n2h 7·7.5·n2g 7·7 / Claude n2g 6.4·n2h 6.0·n2i 5.9(전부 7 미달: '흰 머리띠가 유튜브 흰 화면에 묻힘·PPT 표 같음')
#    처방(Claude): 흰 띠 없애 전면 어둡게, '세전 월 450만원' 노랑으로 크게(위계) · 그림 하나 — 칸 안 '순위 사다리'(위=상위 0%, 아래=100%, 실제 12.6·42.2 자리에 점).
def four(b2=f'상위 {B}', ladder=True):
    L = ''
    if ladder:
        for x0, pct, col in ((560, P27, '#14171C'), (1188, P42, '#FFFFFF')):
            y0, hh = 268, 272
            L += (f"<div style='position:absolute;left:{x0}px;top:{y0}px;width:14px;height:{hh}px;background:rgba(0,0,0,.18);border-radius:7px'></div>"
                  f"<div style='position:absolute;left:{x0-15}px;top:{y0+hh*pct/100-22:.0f}px;width:44px;height:44px;background:{col};border-radius:22px;box-shadow:0 0 0 6px rgba(0,0,0,.15)'></div>")
    al = "text-align:left;padding-left:40px" if ladder else "text-align:center"
    return f"""<div style='position:absolute;inset:0;background:#0B1D45'></div>
{icon(40, 30, 140)}
<div class='t' style='left:176px;top:30px;font-size:112px;color:#FFD23F'>세전 월 450만원</div>
<div class='t' style='left:180px;top:152px;font-size:58px;color:#FFFFFF'>같은 나이 일자리</div>
<div style='position:absolute;left:24px;top:248px;width:604px;height:316px;background:#FFD23F;border-radius:22px'></div>
<div style='position:absolute;left:652px;top:248px;width:604px;height:316px;background:#2B6BE4;border-radius:22px'></div>
<div class='t' style='left:24px;top:272px;width:604px;{al};font-size:80px;color:#3A3220'>스물일곱엔</div>
<div class='t' style='left:24px;top:378px;width:604px;{al};font-size:160px;color:#14171C'><span style='font-size:86px'>상위 </span>{A}</div>
<div class='t' style='left:652px;top:272px;width:604px;{al};font-size:80px;color:#FFFFFF'>마흔둘엔</div>
<div class='t' style='left:652px;top:378px;width:604px;{al};font-size:160px;color:#FFFFFF'>{b2.replace('상위 ', "<span style='font-size:86px'>상위 </span>")}</div>
{L}"""


V['n2j'] = four()
V['n2k'] = four(ladder=False)
V['n2l'] = four(b2=B, ladder=False)

# n2m — 3차 1위 n2g + 레드팀 처방: 조건 줄 두 칸 아래 왼쪽부터 크게(72px, 두 칸에 다 걸리게 칸 폭 아래), '마흔둘엔' 흰색. 오른쪽 아래(x>960,y>576) 비움.
V['n2m'] = three().replace("<div class='t' style='left:40px;top:594px;font-size:64px;color:#FFFFFF'>같은 나이 일자리</div>",
    "<div class='t' style='left:24px;top:590px;width:1232px;text-align:center;font-size:78px;color:#FFFFFF'>같은 나이 일자리</div>").replace("font-size:84px;color:#DCE6FF'>마흔둘엔", "font-size:84px;color:#FFFFFF'>마흔둘엔")

# ── 5차(10/14 18:2x) — 4차 세 명: n2k 7.22(제미나이 7·7.5·Claude 6.8·레드팀 7.6) 통과 · n2m 6.90(6.5·6.2·레드팀 8.0) · n2l 6.62 · n2g(3차 7.07) 대조 6.43.
#    레드팀: 조건 줄은 두 칸 아래 가운데여야 양쪽 숫자에 걸림(n2m만) · Claude: n2k 아래 빈 여백·나이 말 168px 작음.
#    n2n = n2k 어두운 전면 + 조건 줄을 두 칸 아래 가운데 82px(위 띠는 '세전 월 450만원'만, 더 크게) + 나이 말 88px.
V['n2n'] = four(ladder=False).replace("<div class='t' style='left:180px;top:152px;font-size:58px;color:#FFFFFF'>같은 나이 일자리</div>", "")     .replace("left:176px;top:30px;font-size:112px", "left:186px;top:40px;font-size:124px")     .replace("top:248px;width:604px;height:316px", "top:200px;width:604px;height:366px")     .replace("top:272px;width:604px;text-align:center;font-size:80px", "top:226px;width:604px;text-align:center;font-size:88px")     .replace("top:378px;width:604px;text-align:center;font-size:160px", "top:350px;width:604px;text-align:center;font-size:172px")     + "<div class='t' style='left:24px;top:588px;width:1232px;text-align:center;font-size:82px;color:#FFFFFF'>같은 나이 일자리</div>"
assert V['n2n'].count('같은 나이 일자리') == 1 and '세전 월 450만원' in V['n2n']

# ── 6차(10/15 09:1x) — copywriter 18:53 '마흔둘엔 상위 42%' 승인. 5차 처방: ① 문서 아이콘 빼고 '세전 월 450만원' 왼쪽 끝부터 크게
#    ② '상위'를 숫자의 55%로 ③ 두 칸 사이 띄움(나란히 비교) ④ 같은 450이 두 칸에 걸린다는 연결 표시. 화살표·크기 차 금지(시간 흐름 오독).
def six(link=False, gap=72, c1='#FFD23F', c2='#2B6BE4', head='#FFD23F'):
    w = (1232 - gap) // 2; x2 = 24 + w + gap
    L = ''
    if link:  # 머리 글 아래 가로 띠 하나 → 두 칸 가운데로 내려가는 짧은 기둥 2개(한 월급이 두 칸에 같이 걸림)
        L = (f"<div style='position:absolute;left:{24+w//2-7}px;top:168px;width:{x2+w//2-24-w//2+14}px;height:14px;background:{head};border-radius:7px'></div>"
             f"<div style='position:absolute;left:{24+w//2-7}px;top:168px;width:14px;height:52px;background:{head};border-radius:7px'></div>"
             f"<div style='position:absolute;left:{x2+w//2-7}px;top:168px;width:14px;height:52px;background:{head};border-radius:7px'></div>")
    top = 214 if link else 200
    return f"""<div style='position:absolute;inset:0;background:#0B1D45'></div>
<div class='t' style='left:0;top:22px;width:1280px;text-align:center;font-size:136px;color:{head}'>세전 월 450만원</div>{L}
<div style='position:absolute;left:24px;top:{top}px;width:{w}px;height:{566-top}px;background:{c1};border-radius:22px'></div>
<div style='position:absolute;left:{x2}px;top:{top}px;width:{w}px;height:{566-top}px;background:{c2};border-radius:22px'></div>
<div class='t' style='left:24px;top:{top+22}px;width:{w}px;text-align:center;font-size:88px;color:#3A3220'>스물일곱엔</div>
<div class='t' style='left:24px;top:{top+140}px;width:{w}px;text-align:center;font-size:172px;color:#14171C'><span style='font-size:96px'>상위 </span>{A}</div>
<div class='t' style='left:{x2}px;top:{top+22}px;width:{w}px;text-align:center;font-size:88px;color:#FFFFFF'>마흔둘엔</div>
<div class='t' style='left:{x2}px;top:{top+140}px;width:{w}px;text-align:center;font-size:172px;color:#FFFFFF'><span style='font-size:96px'>상위 </span>{B}</div>
<div class='t' style='left:24px;top:588px;width:1232px;text-align:center;font-size:82px;color:#FFFFFF'>같은 나이 일자리</div>"""


V['n2o'] = six()
V['n2p'] = six(link=True)
V['n2q'] = six(link=True, c2='#FFFFFF').replace("color:#FFFFFF'>마흔둘엔", "color:#1E3A8A'>마흔둘엔").replace(f"font-size:172px;color:#FFFFFF'><span style='font-size:96px'>상위 </span>{B}", f"font-size:172px;color:#1E3A8A'><span style='font-size:96px'>상위 </span>{B}")
assert all(V[k].count('상위 ') == 2 and V[k].count('같은 나이 일자리') == 1 for k in ('n2o', 'n2p', 'n2q'))

# ── 7차(10/15 09:2x) — 6차 세 명: n2o 7.35(제미나이 7.5·7 → 7.25·Claude 6.9·레드팀 7.9) 1위 · n2q 7.30 · n2p 7.25 · n2n 6.63.
#    Claude 블라인드: n2o 맨 아래 '같은 나이 일자리'만 흐림 → 레드팀 조건(못 읽은 심사관이 나오면) 대안 1: 조건 줄을 두 칸 바로 아래(간격 10px 이하)·96px.
#    연결 띠(n2p·n2q)는 대진표·조직도로 읽힘(레드팀) → 버림. 흰 칸(n2q)은 42%가 '좋은 쪽'으로 튐 → 버림.
#    오른쪽 아래(x>960,y>576) 비우려고 조건 줄 가운데를 x=600으로.
V['n2r'] = six().replace("height:366px", "height:336px").replace(
    "<div class='t' style='left:24px;top:588px;width:1232px;text-align:center;font-size:82px;color:#FFFFFF'>같은 나이 일자리</div>",
    "<div class='t' style='left:0;top:544px;width:1200px;text-align:center;font-size:96px;color:#FFFFFF'>같은 나이 일자리</div>")
assert V['n2r'].count('font-size:96px;color:#FFFFFF') == 1

# ── 8차 준비(10/15) — 7차 세 명: n2r 6.87(제미나이 6·6·Claude 6.7·레드팀 7.9) · n2o 대조 6.33(5·5·6.3·7.7, 6차 7.35에서 1점 내려감).
#    레드팀: n2r 아래 줄 x=600 왼쪽 이동은 득 0(n2o도 이미 x<960) → 가운데로. n2s = n2r 가운데.
V['n2s'] = V['n2r'].replace("left:0;top:544px;width:1200px", "left:0;top:544px;width:1280px")


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
