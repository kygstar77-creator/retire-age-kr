# P-1 썸네일 13차~ 새 틀(2026-10-14 사장님 10:3x "기준 넘게 경쟁사 조사 잘하고 발전시켜서") — 눈금 끝점 틀을 버림.
# 경쟁 조사: ep/P-1/thumb-compete-1014.md (조기수령·수령나이·연기 조회순 26장)
#   ① 큰 글 줄 높이 프레임의 13~17%, 가로 85~95%를 채움(우리 p1s 큰 말 10%, 라벨 6%)
#   ② 11/26이 '?'나 가린 답(□□세·'이때'·'이 금액')으로 물음을 남김 — 우리 12차까지 0(답을 다 보여 줌)
#   ③ 명암 폭(밝기 표준편차) 중앙 80 — 우리 p1s 48·p1j 65
# 문구: 큰 말 '당긴 이득 끝나는 나이'(copywriter bigword1014 F, 블라인드 3/3) · '5년 당기면'·'1년만 당기면'(대본 0·3장 말) · '1969년생 기준'
#   (따라잡히는 나이는 월액과 무관 — 비율만으로 정해짐, calc 1절 1964~69년생 모두 월 100만원 같은 비율로 확인 → '월 100만원 가정'은 이 숫자에 안 필요)
# 숫자: calc_out 2절에서 읽음(make_thumbs.A5/A1 assert 76.67·80.67)
import os, sys, json
sys.argv = sys.argv[:1] + sys.argv[1:]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
_argv = sys.argv; sys.argv = sys.argv[:1]
import make_thumbs as M
sys.argv = _argv
from PIL import Image
S5, S1 = M.S5, M.S1                      # '76.7세', '80.7세'
N5, N1 = S5[:-1], S1[:-1]                 # '76.7', '80.7'
BW = '당긴 이득 끝나는 나이'
BY = '1969년생 기준'
L5, L1 = '5년 당기면', '1년만 당기면'
assert (N5, N1) == ('76.7', '80.7')
# 금액과 무관 확인: 5년 당김 0.70, 1년 0.94 비율만으로 같아지는 나이 = 65 + (당긴 햇수×비율)/(1-비율)
assert abs(65 + 5 * 0.70 / 0.30 - M.A5) < 0.01 and abs(65 + 1 * 0.94 / 0.06 - M.A1) < 0.01

YEL, INK, WHT = '#FFD23F', '#14171C', '#FFFFFF'
SH = 'text-shadow:0 6px 0 rgba(0,0,0,.55)'   # 굵은 그림자(경쟁 26장 대부분 글자 테두리/그림자, 168px 분리용)


def calc(x, y, w, lcd, lcdcol='#1B2A1F', lcdbg='#B9C9A4', body='#E9E5DB', fs=None):
    """납작한 계산기(광택 없음). x,y 왼위, 너비 w, 높이 1.45w. lcd = 화면 글자."""
    h = w * 1.45; pad = w * 0.08; lh = w * 0.42
    s = f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;background:{body};border-radius:{w*0.08:.0f}px;box-shadow:0 14px 0 rgba(0,0,0,.35)'></div>"
    s += f"<div style='position:absolute;left:{x+pad:.0f}px;top:{y+pad:.0f}px;width:{w-2*pad:.0f}px;height:{lh:.0f}px;background:{lcdbg};border-radius:{w*0.03:.0f}px;box-shadow:inset 0 4px 0 rgba(0,0,0,.18)'></div>"
    fs = fs or lh * 0.78
    s += f"<div class='t' style='left:{x+pad:.0f}px;top:{y+pad+(lh-fs)/2+fs*0.06:.0f}px;width:{w-2*pad-w*0.05:.0f}px;text-align:right;font-size:{fs:.0f}px;color:{lcdcol}'>{lcd}</div>"
    bw = (w - 2 * pad - 3 * w * 0.04) / 4; by0 = y + pad + lh + w * 0.07; bh = (h - (by0 - y) - pad - 3 * w * 0.04) / 4
    for r in range(4):
        for c in range(4):
            col = '#F08A24' if c == 3 else ('#C9C4B8' if r == 0 else '#FBFAF6')
            s += (f"<div style='position:absolute;left:{x+pad+c*(bw+w*0.04):.0f}px;top:{by0+r*(bh+w*0.04):.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;"
                  f"background:{col};border-radius:{w*0.025:.0f}px;box-shadow:0 4px 0 rgba(0,0,0,.18)'></div>")
    return s


V = {}
# p1w — 계산기 + 가린 답(1년만 당기면 → 화면 '?'). 짙은 초록. 글자 왼쪽 3줄.
V['p1w'] = f"""<div style='position:absolute;inset:0;background:#0F3A33'></div>
<div style='position:absolute;left:0;top:34px;width:820px;height:118px;background:{YEL}'></div>
<div class='t' style='left:46px;top:50px;font-size:86px;color:{INK}'>{BW}</div>
<div class='t' style='left:46px;top:210px;font-size:104px;color:{WHT};{SH}'>{L5} <span style='color:#BFD8CF'>{N5}세</span></div>
<div id='q' class='t' data-fit='790' style='left:46px;top:362px;font-size:150px;color:{YEL};{SH}'>{L1}?</div>
<div class='lab' style='left:50px;top:590px;font-size:38px;color:#A9C4BB'>{BY}</div>
{calc(900, 120, 330, '??.?', fs=110)}
"""
# p1x — 계산기 화면이 답(80.7)을 큼직하게, 왼쪽은 5년 76.7 작게 → '1년만 당기면' 크게. 답을 보여 주는 판(p1w와 대조).
V['p1x'] = f"""<div style='position:absolute;inset:0;background:#0F3A33'></div>
<div style='position:absolute;left:0;top:34px;width:820px;height:118px;background:{YEL}'></div>
<div class='t' style='left:46px;top:50px;font-size:86px;color:{INK}'>{BW}</div>
<div class='t' style='left:46px;top:214px;font-size:80px;color:#BFD8CF;{SH}'>{L5} {N5}세</div>
<div class='t' style='left:46px;top:356px;font-size:120px;color:{WHT};{SH}'>{L1}</div>
<div style='position:absolute;left:640px;top:410px;width:0;height:0;border-left:44px solid {YEL};border-top:30px solid transparent;border-bottom:30px solid transparent'></div>
<div class='lab' style='left:50px;top:590px;font-size:38px;color:#A9C4BB'>{BY}</div>
{calc(800, 180, 420, N1 + '<span style="font-size:60px">세</span>', fs=128)}
"""
# p1y — 글자만, 위아래 두 색(위 짙은 남먹·아래 노랑 판). 가린 답 '??세'. 경쟁 글자판(06·10·12)처럼 글자가 화면을 채움.
V['p1y'] = f"""<div style='position:absolute;inset:0;background:#15191F'></div>
<div style='position:absolute;left:0;top:360px;width:1280px;height:360px;background:{YEL}'></div>
<div class='t' style='left:52px;top:36px;font-size:76px;color:{YEL}'>{BW}</div>
<div class='t' style='left:52px;top:150px;font-size:150px;color:{WHT}'>{L5} <span>{N5}세</span></div>
<div id='q' class='t' data-fit='1180' style='left:52px;top:392px;font-size:158px;color:{INK}'>{L1} <span style='display:inline-block;background:{INK};color:{YEL};padding:0 18px;border-radius:14px'>??세</span></div>
<div class='lab' style='left:56px;top:600px;font-size:40px;color:{INK}'>{BY}</div>
"""
# p1z — p1y 답 보여 주는 판: 아래 노랑 판 '1년만 당기면 80.7세'
V['p1z'] = V['p1y'].replace("<span style='display:inline-block;background:#14171C;color:#FFD23F;padding:0 18px;border-radius:14px'>??세</span>",
                            f"<span style='display:inline-block;background:{INK};color:{YEL};padding:0 18px;border-radius:14px'>{N1}세</span>")
assert N1 in V['p1z']
# p2a — 계산기 가운데 크게(화면 '??.?'), 위 큰 말, 아래 두 줄 좌우 — 주제 사물이 화면 절반(thumb-gap 1위 처방)
V['p2a'] = f"""<div style='position:absolute;inset:0;background:#1F5F78'></div>
<div class='t' style='left:40px;top:28px;font-size:84px;color:{WHT};{SH}'>{BW}</div>
<div class='t' style='left:40px;top:180px;font-size:66px;color:#CFE3EA;{SH}'>{L5}</div>
<div class='t' style='left:40px;top:262px;font-size:150px;color:{WHT};{SH}'>{N5}<span style='font-size:80px'>세</span></div>
<div class='t' style='left:40px;top:470px;font-size:84px;color:{YEL};{SH}'>{L1}</div>
<div class='lab' style='left:44px;top:600px;font-size:38px;color:#CFE3EA'>{BY}</div>
{calc(640, 150, 360, '??.?', fs=120)}
"""
# p2b — 계산기 없이 '물음표 큰 칸' — 왼쪽 76.7세 칸(흰), 오른쪽 ??세 칸(노랑), 위 큰 말. 칸 두 개(쇼츠 조회 1위 wPIHi7cSmQQ 두 칸 대결)
V['p2b'] = f"""<div style='position:absolute;inset:0;background:#15191F'></div>
<div class='t' style='left:44px;top:34px;font-size:88px;color:{WHT}'>{BW}</div>
<div style='position:absolute;left:40px;top:170px;width:560px;height:400px;background:#F2EEE6;border-radius:24px'></div>
<div style='position:absolute;left:640px;top:170px;width:600px;height:400px;background:{YEL};border-radius:24px'></div>
<div class='t' style='left:40px;top:196px;width:560px;text-align:center;font-size:72px;color:#3B4250'>{L5}</div>
<div class='t' style='left:40px;top:316px;width:560px;text-align:center;font-size:170px;color:{INK}'>{N5}<span style='font-size:80px'>세</span></div>
<div class='t' style='left:640px;top:196px;width:600px;text-align:center;font-size:72px;color:{INK}'>{L1}</div>
<div class='t' style='left:640px;top:310px;width:600px;text-align:center;font-size:200px;color:{INK}'>??<span style='font-size:80px'>세</span></div>
<div class='lab' style='left:46px;top:600px;font-size:38px;color:#AEB6C4'>{BY}</div>
"""


def stats(p):
    import numpy as n
    a = n.asarray(Image.open(p).convert('L'), float); return round(a.mean()), round(a.std())


# ── 14차 — 13차 세 명: p1z 6.88(제미나이 7.25·Claude 6.4·레드팀 7)·p1y 6.73·p1x 6.47·p2b 6.47·p1w 6.23·p2a 5.45·p1j 5.77.
#    반려(레드팀): p1w·p1y·p2a·p2b 경쟁 OJUjwfzJsXI와 비슷한 점 4('이득'·물음표·어두운 바탕 노랑·당김별 숫자 비교), p1x·p1z 3.
#    두 심사 공통 처방: 머리말 '당긴 이득 끝나는 나이' → '국민연금 따라잡히는 나이'('이득' 단정·'연금 끝나는 나이' 오독 제거, 제목과 같은 이름)
#    · 검정·노랑 배색 버림 → 밝은 바탕+짙은 칸 · 두 칸 구조 키우고 빈 공간 없앰(Claude p2b) · 답 가림/보임 둘 다 다시.
HEAD2 = '국민연금 <span style="color:#1F4FA8">따라잡히는 나이</span>'
PAGE, CARD, DARK, SKY = '#E7E2D6', '#FFFFFF', '#17233A', '#8FD3FF'


def cards2(right, rcol=SKY):
    return f"""<div style='position:absolute;inset:0;background:{PAGE}'></div>
<div class='t' style='left:40px;top:26px;font-size:84px;color:{INK}'>{HEAD2}</div>
<div style='position:absolute;left:30px;top:142px;width:590px;height:478px;background:{CARD};border-radius:26px;box-shadow:0 8px 0 rgba(0,0,0,.12)'></div>
<div style='position:absolute;left:650px;top:142px;width:600px;height:478px;background:{DARK};border-radius:26px;box-shadow:0 8px 0 rgba(0,0,0,.25)'></div>
<div class='t' style='left:30px;top:176px;width:590px;text-align:center;font-size:84px;color:#4A5568'>{L5}</div>
<div class='t' style='left:30px;top:306px;width:590px;text-align:center;font-size:220px;color:{INK}'>{N5}<span style='font-size:90px'>세</span></div>
<div class='t' style='left:650px;top:176px;width:600px;text-align:center;font-size:84px;color:#fff'>{L1}</div>
<div class='t' style='left:650px;top:306px;width:600px;text-align:center;font-size:220px;color:{rcol}'>{right}<span style='font-size:90px'>세</span></div>
<div class='lab' style='left:40px;top:636px;font-size:36px;color:#5B6472'>{BY}</div>
"""


def bands2(right):
    return f"""<div style='position:absolute;inset:0;background:{PAGE}'></div>
<div style='position:absolute;left:0;top:372px;width:1280px;height:348px;background:{DARK}'></div>
<div class='t' style='left:52px;top:30px;font-size:84px;color:{INK}'>{HEAD2}</div>
<div class='t' style='left:52px;top:160px;font-size:156px;color:{INK}'>{L5} {N5}<span style='font-size:100px'>세</span></div>
<div id='q' class='t' data-fit='1180' style='left:52px;top:410px;font-size:156px;color:#fff'>{L1} <span style='color:{SKY}'>{right}</span><span style='font-size:100px;color:{SKY}'>세</span></div>
<div class='lab' style='left:56px;top:612px;font-size:40px;color:#AEB6C4'>{BY}</div>
"""


V['p2c'] = cards2('??')
V['p2d'] = cards2(N1)
V['p2e'] = bands2('??')
V['p2f'] = bands2(N1)
assert '이득' not in V['p2c'] + V['p2d'] + V['p2e'] + V['p2f']

# ── 15차 — 14차 세 명: p2d 6.67(제미나이 6·Claude 7.0·레드팀 7, 유사 1~2)·p2c 6.53(레드팀 반려 3)·p1z 6.30·p2e 6.27(반려)·p2f 6.23·p1j 5.83.
#    p2d 기준으로 처방: ① 기준선이 화면에 없음(누가 누구를 따라잡나) → 아래 줄 '제때(65세) 받은 사람 기준'(p1s에서 사실 대조 끝난 말) 크게
#    ② '1969년생'이 168px에서 안 읽힘 → 키우거나 머리로 ③ 80.7 연파랑 = 강조·권유 소지 → 흰색 ④ 가린 답 '??'는 레드팀 경쟁 문법(물음표)로 반려 → 답 보임만.
BASE = '제때(65세) 받은 사람 기준'


def cards3(head, l5, l1, foot, num=220, foot_fs=46, head_fs=84, top=142, h=430):
    return f"""<div style='position:absolute;inset:0;background:{PAGE}'></div>
<div class='t' style='left:40px;top:26px;font-size:{head_fs}px;color:{INK}'>{head}</div>
<div style='position:absolute;left:30px;top:{top}px;width:590px;height:{h}px;background:{CARD};border-radius:26px;box-shadow:0 8px 0 rgba(0,0,0,.12)'></div>
<div style='position:absolute;left:650px;top:{top}px;width:600px;height:{h}px;background:{DARK};border-radius:26px;box-shadow:0 8px 0 rgba(0,0,0,.25)'></div>
<div class='t' style='left:30px;top:{top+30}px;width:590px;text-align:center;font-size:84px;color:#4A5568'>{l5}</div>
<div class='t' style='left:30px;top:{top+140}px;width:590px;text-align:center;font-size:{num}px;color:{INK}'>{N5}<span style='font-size:90px'>세</span></div>
<div class='t' style='left:650px;top:{top+30}px;width:600px;text-align:center;font-size:84px;color:#C9D3E6'>{l1}</div>
<div class='t' style='left:650px;top:{top+140}px;width:600px;text-align:center;font-size:{num}px;color:#fff'>{N1}<span style='font-size:90px'>세</span></div>
<div class='t' style='left:40px;top:{top+h+22}px;font-size:{foot_fs}px;color:#3B4250'>{foot}</div>
"""


V['p2g'] = cards3(HEAD2, L5, L1, f'{BY[:-3]} · {BASE}')
V['p2h'] = cards3('1969년생 <span style="color:#1F4FA8">따라잡히는 나이</span>', '5년 당김', '1년 당김', BASE, foot_fs=52)
V['p2i'] = cards3(HEAD2, '5년 당김', '1년 당김', f'{BY[:-3]} · {BASE}', num=240)
for _k in ('p2g', 'p2h', 'p2i'): V[_k] = V[_k].replace(f'background:{PAGE}', 'background:#D3CDBF', 1)   # 밝기 173 → 170 아래(경쟁 26장 최고 131)
assert '76.7' in V['p2g'] and '80.7' in V['p2h'] and '1969년생' in V['p2i']

# ── 16차 — 15차 세 명: p2d 6.87(제미나이 7·Claude 6.6·레드팀 7)·p2i 6.83(7·6.5·7)·p2g 6.60·p2h 6.48·p1j 6.00.
#    공통 처방: ① 80.7 흰색으로 바꾸자 두 숫자 무게가 같아져 반전 신호가 사라짐 → 강조색(연파랑) 되살림 ② 숫자는 p2i처럼 크게
#    ③ 두 숫자 관계 표시(Claude: 부등호·화살표 하나) → 칸 사이 '<' (76.67 < 80.67 사실) ④ 기준 줄이 168px에서 안 읽힘 → 머리 바로 밑 큰 줄로
#    ⑤ 베이지가 목록에서 흐림(Claude) → 진한 청록 바탕 판도 같이.
def cards4(head, sub, l5, l1, bg='#D3CDBF', headc=INK, subc='#1F4FA8', num=210):
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='t' style='left:40px;top:20px;font-size:78px;color:{headc}'>{head}</div>
<div class='t' style='left:42px;top:112px;font-size:52px;color:{subc}'>{sub}</div>
<div style='position:absolute;left:30px;top:196px;width:540px;height:430px;background:{CARD};border-radius:26px;box-shadow:0 8px 0 rgba(0,0,0,.15)'></div>
<div style='position:absolute;left:710px;top:196px;width:540px;height:430px;background:{DARK};border-radius:26px;box-shadow:0 8px 0 rgba(0,0,0,.25)'></div>
<div class='t' style='left:30px;top:236px;width:540px;text-align:center;font-size:80px;color:#4A5568'>{l5}</div>
<div class='t' style='left:30px;top:362px;width:540px;text-align:center;font-size:{num}px;color:{INK}'>{N5}<span style='font-size:84px'>세</span></div>
<div class='t' style='left:710px;top:236px;width:540px;text-align:center;font-size:80px;color:#C9D3E6'>{l1}</div>
<div class='t' style='left:710px;top:362px;width:540px;text-align:center;font-size:{num}px;color:{SKY}'>{N1}<span style='font-size:84px'>세</span></div>
<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='675,392 605,447 675,502' fill='none' stroke='{headc}' stroke-width='22' stroke-linecap='round' stroke-linejoin='round'/></svg>
"""


_sub = f'{BY[:-3]} · {BASE}'
V['p2j'] = cards4(HEAD2, _sub, '5년 당김', '1년 당김')
V['p2k'] = cards4('제때 받은 쪽이 <span style="color:#1F4FA8">따라잡는 나이</span>', f'국민연금 · {BY}', '5년 당김', '1년 당김')
V['p2l'] = cards4('국민연금 <span style="color:#8FD3FF">따라잡히는 나이</span>', _sub, '5년 당김', '1년 당김', bg='#1E5F57', headc='#FFFFFF', subc='#CDE7E1')
V['p2m'] = cards4(HEAD2, _sub, L5, L1)

# ── 17차 — 16차 세 명: p2k 6.92(제미나이 7.25·Claude 6.0·레드팀 7.5)·p2j 6.82·p2l 6.75(Claude 1위 6.5 — 청록 바탕만 목록에서 안 묻힘)·p2m 6.63·p1j 6.58.
#    처방: ① 주어 있는 말 '제때(65세) 받은 쪽이 따라잡는 나이'(p1j 확정판 문구 + 65세 복원, 레드팀) ② '국민연금' 크게 머리로(두 심사)
#    ③ 청록 바탕(Claude: 베이지는 빈 슬라이드) ④ 연파랑 80.7 + '<' = '1년 당김이 낫다' 신호(두 심사) → 강조는 정체성 주황(#FF5A00, 핵심 숫자 하나) 한 곳만, 또는 숫자 같은 색.
ORG = '#FF5A00'
HEAD3 = "국민연금 <span style='font-size:58px;color:#CDE7E1'>· 1969년생</span>"
MEAN = '제때(65세) 받은 쪽이 따라잡는 나이'


def cards5(bg, head, mean, c5, c1, n5c, n1c, l5c, l1c, chev, headc='#FFFFFF', meanc='#FFFFFF', l5='5년 당김', l1='1년 당김'):
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='t' style='left:40px;top:16px;font-size:80px;color:{headc}'>{head}</div>
<div class='t' style='left:42px;top:110px;font-size:62px;color:{meanc}'>{mean}</div>
<div style='position:absolute;left:30px;top:200px;width:540px;height:426px;background:{c5};border-radius:26px'></div>
<div style='position:absolute;left:710px;top:200px;width:540px;height:426px;background:{c1};border-radius:26px'></div>
<div class='t' style='left:30px;top:236px;width:540px;text-align:center;font-size:80px;color:{l5c}'>{l5}</div>
<div class='t' style='left:30px;top:362px;width:540px;text-align:center;font-size:210px;color:{n5c}'>{N5}<span style='font-size:84px'>세</span></div>
<div class='t' style='left:710px;top:236px;width:540px;text-align:center;font-size:80px;color:{l1c}'>{l1}</div>
<div class='t' style='left:710px;top:362px;width:540px;text-align:center;font-size:210px;color:{n1c}'>{N1}<span style='font-size:84px'>세</span></div>
<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='675,392 605,447 675,502' fill='none' stroke='{chev}' stroke-width='22' stroke-linecap='round' stroke-linejoin='round'/></svg>
"""


TEAL = '#1E5F57'
V['p2n'] = cards5(TEAL, HEAD3, MEAN, CARD, DARK, INK, ORG, '#4A5568', '#C9D3E6', '#FFFFFF')        # 1년 칸 남색 + 80.7 주황
V['p2o'] = cards5(TEAL, HEAD3, MEAN, CARD, CARD, INK, INK, '#4A5568', '#4A5568', ORG)              # 두 칸 흰색·숫자 같은 색, 부등호만 주황
V['p2p'] = cards5(TEAL, HEAD3, MEAN, CARD, DARK, INK, '#FFFFFF', '#4A5568', '#C9D3E6', '#FFFFFF')  # 강조 없음(80.7 흰색)
V['p2q'] = cards5('#D3CDBF', "국민연금 <span style='font-size:58px;color:#4A5568'>· 1969년생</span>", MEAN, CARD, DARK, INK, ORG, '#4A5568', '#C9D3E6', INK,
                  headc=INK, meanc='#1F4FA8')                                                         # p2n 베이지 대조
assert all(MEAN in V[k] and '국민연금' in V[k] for k in ('p2n', 'p2o', 'p2p', 'p2q'))

# ── 18차 — 17차 세 명: p2n 6.97(제미나이 9·8 → 8.5·Claude 6.4·레드팀 6)·p2q 6.40·p2o 6.03·p2p 5.57.
#    두 심사 공통 처방: ① 뜻을 지는 말이 168px에서 약 5~7px로 뭉개짐 → '제때 받은 쪽이 따라잡는 나이'(p1j SM0 원문) 88px로, '국민연금·1969년생·65세'는 작은 윗줄로
#    ② '세'가 168px에서 안 보여 76.7이 %·수명으로 읽힘(레드팀) → '세'를 숫자 높이 절반 넘게 ③ 아래 빈 띠 없앰 ④ 강조는 주황 80.7 하나(레드팀: 칸 색 같게)
#    ⑤ Claude: 반전을 글로 — 제목의 '오히려 늦다'(한 판만 시험).
TOP4 = '국민연금 · 1969년생 · 제때 65세'
MEAN2 = '제때 받은 쪽이 따라잡는 나이'


def cards6(c1, l1c, n1c=ORG, chev='#FFFFFF', tag=''):
    return f"""<div style='position:absolute;inset:0;background:{TEAL}'></div>
<div class='t' style='left:40px;top:16px;font-size:50px;color:#CDE7E1'>{TOP4}</div>
<div class='t' style='left:38px;top:80px;font-size:88px;color:#FFFFFF'>{MEAN2}</div>
<div style='position:absolute;left:30px;top:196px;width:540px;height:470px;background:{CARD};border-radius:26px'></div>
<div style='position:absolute;left:710px;top:196px;width:540px;height:470px;background:{c1};border-radius:26px'></div>
<div class='t' style='left:30px;top:226px;width:540px;text-align:center;font-size:80px;color:#4A5568'>5년 당김</div>
<div class='t' style='left:30px;top:350px;width:540px;text-align:center;font-size:200px;color:{INK}'>{N5}<span style='font-size:118px'>세</span></div>
<div class='t' style='left:710px;top:226px;width:540px;text-align:center;font-size:80px;color:{l1c}'>1년 당김</div>
<div class='t' style='left:710px;top:350px;width:540px;text-align:center;font-size:200px;color:{n1c}'>{N1}<span style='font-size:118px'>세</span></div>
<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='678,385 602,445 678,505' fill='none' stroke='{chev}' stroke-width='30' stroke-linecap='round' stroke-linejoin='round'/></svg>
{tag}"""


V['p2r'] = cards6(CARD, '#4A5568')                       # 두 칸 흰색, 주황 80.7 하나
V['p2s'] = cards6(DARK, '#C9D3E6')                       # p2n 구조(1년 칸 남색) + 주황 80.7
V['p2t'] = cards6(CARD, '#4A5568', tag="<div class='t' style='left:710px;top:300px;width:540px;text-align:center;font-size:56px;color:#FF5A00'>오히려 늦다</div>")
V['p2t'] = V['p2t'].replace("left:710px;top:226px", "left:710px;top:212px").replace("left:710px;top:350px", "left:710px;top:366px")
assert '오히려 늦다' in V['p2t'] and MEAN2 in V['p2r']

# ── 19차 — 18차 세 명: p2s 6.62(제미나이 6.5·6 → 6.25·Claude 6.6·레드팀 7, 두 심사 1위)·p2t 6.40(레드팀 반려 3: 주황 두 곳·훅 문구)·p2r 6.35·p1j 6.20·p2n 6.17.
#    p2s 기준 처방(두 심사): ① 칸 아래 약 150px 빔 → 칸 줄이고 숫자 키움 ② 168px에서 '국민연금'·'1969년생' 윗줄 4~5px → '국민연금 · 1969년생' 80px로
#    ③ '<' = 승패 표시(레드팀) → 뺌(한 판만 남겨 비교) ④ 남색 칸과 청록 경계 흐림(레드팀) → 한 판은 더 짙은 칸.
HEAD5 = "국민연금 <span style='color:#CDE7E1'>· 1969년생</span>"
MEAN3 = '제때(65세) 받은 쪽이 따라잡는 나이'


def cards7(c1=DARK, chev=False, border=''):
    ch = ("<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='668,400 612,445 668,490' fill='none' stroke='#FFFFFF' "
          "stroke-width='24' stroke-linecap='round' stroke-linejoin='round'/></svg>") if chev else ''
    w = 560 if chev else 590; x1 = 1250 - w
    return f"""<div style='position:absolute;inset:0;background:{TEAL}'></div>
<div class='t' style='left:38px;top:24px;font-size:84px;color:#FFFFFF'>{HEAD5}</div>
<div class='t' style='left:40px;top:126px;font-size:70px;color:#FFFFFF'>{MEAN3}</div>
<div style='position:absolute;left:30px;top:228px;width:{w}px;height:462px;background:{CARD};border-radius:26px'></div>
<div style='position:absolute;left:{x1}px;top:228px;width:{w}px;height:462px;background:{c1};border-radius:26px;{border}'></div>
<div class='t' style='left:30px;top:250px;width:{w}px;text-align:center;font-size:74px;color:#4A5568'>5년 당김</div>
<div class='t' style='left:30px;top:346px;width:{w}px;text-align:center;font-size:226px;color:{INK}'>{N5}<span style='font-size:112px'>세</span></div>
<div class='t' style='left:{x1}px;top:250px;width:{w}px;text-align:center;font-size:74px;color:#C9D3E6'>1년 당김</div>
<div class='t' style='left:{x1}px;top:346px;width:{w}px;text-align:center;font-size:226px;color:{ORG}'>{N1}<span style='font-size:112px'>세</span></div>
{ch}"""


V['p2u'] = cards7()
V['p2v'] = cards7(chev=True)
V['p2w'] = cards7(c1='#0D1320', border='box-shadow:0 0 0 6px #CDE7E1')
assert '1969년생' in V['p2u'] and '&lt;' not in V['p2u']

# ── 20차 — 19차 세 명: p2w 7.38(제미나이 8·8.5 → 8.25·Claude 6.9·레드팀 7)·p2u 7.07(7.5·6.7·7)·p2s 6.55·p2v 6.48·p1j 6.08.
#    평균은 통과선을 넘었으나 레드팀이 경쟁 유사 3개 '경계선'('국민연금' 첫머리·조기 대 제때 비교 구도·어두운 바탕) + '뜻 줄이 머리보다 작아 위계 뒤집힘'으로 확정 보류.
#    처방: ① 뜻 줄 '제때(65세) 받은 쪽이 따라잡는 나이'를 머리보다 크게(78px), '1969년생 · 국민연금'은 작은 윗줄(첫머리 '국민연금' 아님)
#    ② p2w 밝은 테두리 뺌('추천 칸'으로 읽힘, 168px에서 안 보임) ③ 숫자를 칸 세로 가운데로 내려 아래 빈칸 줄임 ④ 한 판은 청록을 밝혀 '어두운 바탕' 겹침 줄임.
TOP6 = "1969년생 · 국민연금"


def cards8(bg=TEAL, c1='#0D1320', top=TOP6):
    w = 590; x1 = 1250 - w
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='t' style='left:40px;top:20px;font-size:58px;color:#CDE7E1'>{top}</div>
<div class='t' style='left:38px;top:92px;font-size:78px;color:#FFFFFF'>{MEAN3}</div>
<div style='position:absolute;left:30px;top:206px;width:{w}px;height:484px;background:{CARD};border-radius:26px'></div>
<div style='position:absolute;left:{x1}px;top:206px;width:{w}px;height:484px;background:{c1};border-radius:26px'></div>
<div class='t' style='left:30px;top:240px;width:{w}px;text-align:center;font-size:76px;color:#4A5568'>5년 당김</div>
<div class='t' style='left:30px;top:348px;width:{w}px;text-align:center;font-size:226px;color:{INK}'>{N5}<span style='font-size:112px'>세</span></div>
<div class='t' style='left:{x1}px;top:240px;width:{w}px;text-align:center;font-size:76px;color:#C9D3E6'>1년 당김</div>
<div class='t' style='left:{x1}px;top:348px;width:{w}px;text-align:center;font-size:226px;color:{ORG}'>{N1}<span style='font-size:112px'>세</span></div>
"""


V['p2x'] = cards8()
V['p2y'] = cards8(c1='#17233A')
V['p2z'] = cards8(bg='#2A7A70')
assert MEAN3 in V['p2x'] and 'box-shadow:0 0 0 6px' not in V['p2x']

# ── 21차 — 사장님 10/14 "주제를 보여주는 무료 그림 넣으면 되잖아." p2z 숫자·문구 그대로, Pexels 사진(출처 ep/P-1/thumb_photo_src.md) 위치만 바꿈.
#    p3a 왼쪽 사진(노부부 얼굴)·오른쪽 두 칸 / p3b 오른쪽 사진 기둥 / p3c 사진 전면 배경 + 청록 덮개 / p3d p2z 칸 줄이고 아래 빈자리에 사진 띠.
PH = {'couple': 'photo/p_couple_1642883.jpg', 'sea': 'photo/p_sea_13600760.jpg', 'seoul': 'photo/p_seoul_32028728.jpg'}


def img(src, x, y, w, h, pos='50% 50%', extra=''):
    return f"<img src='{src}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;object-position:{pos};{extra}'>"


def twocards(x0, y0, w, h, gap, num=226, sefs=112, lab=76):
    x1 = x0 + w + gap; ny = y0 + (h - num) / 2 + 30; ly = y0 + 30
    return f"""<div style='position:absolute;left:{x0}px;top:{y0}px;width:{w}px;height:{h}px;background:{CARD};border-radius:26px'></div>
<div style='position:absolute;left:{x1}px;top:{y0}px;width:{w}px;height:{h}px;background:#0D1320;border-radius:26px'></div>
<div class='t' style='left:{x0}px;top:{ly}px;width:{w}px;text-align:center;font-size:{lab}px;color:#4A5568'>5년 당김</div>
<div class='t' style='left:{x0}px;top:{ny:.0f}px;width:{w}px;text-align:center;font-size:{num}px;color:{INK}'>{N5}<span style='font-size:{sefs}px'>세</span></div>
<div class='t' style='left:{x1}px;top:{ly}px;width:{w}px;text-align:center;font-size:{lab}px;color:#C9D3E6'>1년 당김</div>
<div class='t' style='left:{x1}px;top:{ny:.0f}px;width:{w}px;text-align:center;font-size:{num}px;color:{ORG}'>{N1}<span style='font-size:{sefs}px'>세</span></div>
"""


TB = '#2A7A70'
# p3a — 왼쪽 40% 사진(부부 얼굴), 오른쪽 청록에 윗줄·뜻 줄(두 줄로)·두 칸
V['p3a'] = f"""<div style='position:absolute;inset:0;background:{TB}'></div>
{img(PH['couple'], 0, 0, 470, 720, '58% 30%')}
<div class='t' style='left:500px;top:18px;font-size:54px;color:#CDE7E1'>{TOP6}</div>
<div class='t' style='left:498px;top:84px;font-size:66px;color:#FFFFFF;line-height:1.12'>제때(65세) 받은 쪽이<br>따라잡는 나이</div>
{twocards(496, 268, 372, 370, 20, num=128, sefs=64, lab=60)}
"""
# p3b — p2z 위 두 줄 그대로(전체 폭), 두 칸 왼쪽으로 좁히고 오른쪽 사진 기둥(아래 재생시간 자리는 사진만)
V['p3b'] = f"""<div style='position:absolute;inset:0;background:{TB}'></div>
{img(PH['couple'], 900, 196, 380, 524, '62% 25%')}
<div class='t' style='left:40px;top:20px;font-size:58px;color:#CDE7E1'>{TOP6}</div>
<div class='t' style='left:38px;top:92px;font-size:78px;color:#FFFFFF'>{MEAN3}</div>
{twocards(30, 216, 418, 470, 22, num=150, sefs=76, lab=68)}
"""
# p3c — 사진 전면 배경(바닷가 부부) + 청록 덮개 82% → 칸은 그대로 위에
V['p3c'] = f"""{img(PH['sea'], 0, 0, 1280, 720, '50% 30%')}
<div style='position:absolute;inset:0;background:linear-gradient(180deg, rgba(42,122,112,.85) 0%, rgba(42,122,112,.35) 40%, rgba(20,60,55,.45) 100%)'></div>
<div class='t' style='left:40px;top:20px;font-size:58px;color:#FFFFFF;text-shadow:0 3px 0 rgba(0,0,0,.4)'>{TOP6}</div>
<div class='t' style='left:38px;top:92px;font-size:78px;color:#FFFFFF;text-shadow:0 4px 0 rgba(0,0,0,.45)'>{MEAN3}</div>
{twocards(60, 236, 520, 400, 120, num=210, sefs=104)}
"""
# p3d — p2z 그대로에서 칸 높이 줄여(484→330) 아래 빈자리를 없애고, 그 아래 띠(왼쪽 2/3)에 부부 사진. 오른쪽 아래는 청록 그대로.
V['p3d'] = f"""<div style='position:absolute;inset:0;background:{TB}'></div>
<div class='t' style='left:40px;top:20px;font-size:58px;color:#CDE7E1'>{TOP6}</div>
<div class='t' style='left:38px;top:92px;font-size:78px;color:#FFFFFF'>{MEAN3}</div>
{twocards(30, 200, 590, 340, 40, num=210, sefs=104, lab=0).replace("font-size:0px", "font-size:0px;display:none")}
<div class='t' style='left:30px;top:206px;width:590px;text-align:center;font-size:54px;color:#4A5568'>5년 당김</div>
<div class='t' style='left:660px;top:206px;width:590px;text-align:center;font-size:54px;color:#C9D3E6'>1년 당김</div>
{img(PH['couple'], 30, 556, 830, 164, '50% 40%', 'border-radius:20px 20px 0 0')}
"""
assert all(N5 in V[k] and N1 in V[k] and '1969년생' in V[k] and '65세' in V[k] for k in ('p3a', 'p3b', 'p3c', 'p3d'))

if __name__ == '__main__':
    M.VARIANTS.update(V)
    keys = sys.argv[1].split(',') if len(sys.argv) > 1 else list(V)
    M.main(keys)
    for k in keys: print(k, '밝기·명암폭', stats(os.path.join(M.EP, f'thumb_{k}.png')))


