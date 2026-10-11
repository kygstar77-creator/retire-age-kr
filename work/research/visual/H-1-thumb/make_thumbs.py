# H-1 '올림픽파크포레온·헬리오시티 84㎡' 썸네일 시안(2026-10-11 visual-designer 정기 09:04)
# 문구: ep/H-1/copy/titles.md 1위(copywriter 07:54, 결선 8.63) — 큰 글씨 '6년 가까이 늦게 지었는데', 작은 줄 '84㎡대 1년 실거래 · 평당 중앙'.
#        금지: 큰 글씨에 '−0.6%'·'−37%'·'+19억'·'직거래'·'6년 차이'. 사라·추천·전망·충격·하락 0. 단지 이름은 주제 꼬리표로만 더함(제목 첫 낱말).
# 숫자: deals.json(deals.py — calc.py 3절과 같은 원자료·거르기, 중앙 assert). 입주 2018.12·2024.11 = facts.txt F4·F5.
# 경쟁 5(compete.md) 공통: 아파트 실사 사진 전면 + 아래 흰/노랑 큰 글씨 + 'VS'·빨강 띠. 우리: 사진·VS·노랑 0, 밝은 판 + 실제 거래 점(85건·45건).
# 가려짐: 오른쪽 아래 x≥960·y≥576, 아래 5%(y≥684) 글자·점 없음 — 렌더 뒤 자동 검사(zones.json).
import os, json, sys, statistics as st
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'H-1')
meta = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))
BIG, SMALL = meta['thumb_text'], meta['thumb_text_small']
assert (BIG, SMALL) == ('6년 가까이 늦게 지었는데', '84㎡대 1년 실거래 · 평당 중앙'), (BIG, SMALL)
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
assert '헬리오시티: 2018.12 입주' in facts and '올림픽파크포레온: 2024.11 입주' in facts
D = json.load(open(os.path.join(HERE, 'deals.json'), encoding='utf-8'))
HE, OP = D['헬리오시티'], D['올림픽파크포레온']

INK, RED, NAVY, GREY, PAPER, TEAL = '#16181D', '#E5322D', '#1E2A44', '#6B7280', '#F3EFE6', '#0F7B6C'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]


def strip(vals, x0, w, y, h, col, lo=7500, hi=12500, r=11):
    """거래 하나 = 점 하나(평당, 만원). 띠(높이 h) 안에 고정 난수로 흩뿌림(겹침 허용, 반투명). 중앙 굵은 검은 선."""
    import random
    X = lambda v: x0 + w * (v - lo) / (hi - lo)
    rnd = random.Random(1011 + len(vals)); s = ''
    for v in vals:
        cy = y + r + rnd.random() * (h - 2 * r)
        s += f"<div style='position:absolute;left:{X(v) - r:.0f}px;top:{cy - r:.0f}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;background:{col};opacity:.75'></div>"
    m = X(st.median(vals))
    s += f"<div style='position:absolute;left:{m - 5:.0f}px;top:{y - 10}px;width:10px;height:{h + 20}px;background:{INK}'></div>"
    return s, X


def axis(X, y, col=GREY):
    s = ''
    for v, t in ((8000, '8천만'), (10000, '1억'), (12000, '1억 2천')):
        s += f"<div class='lab' style='left:{X(v) - 80:.0f}px;top:{y}px;width:160px;text-align:center;font-size:30px;color:{col}'>{t}</div>"
    return s


# h1a — 밝은 종이 판, 큰 글씨 한 줄('6년 가까이' 빨강) + 두 단지 실제 거래 점 두 줄(같은 눈금) + 중앙 검은 선. 점이 같은 자리에 몰린 것 = 답.
sa, Xa = strip(HE, 420, 800, 210, 120, NAVY)
sb, _ = strip(OP, 420, 800, 380, 120, TEAL)
h1a = f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div id='a0' class='t' data-fit='1180' style='left:48px;top:40px;font-size:118px;color:{INK}'><span style='color:{RED}'>6년 가까이</span> 늦게 지었는데</div>
<div class='t' style='left:48px;top:226px;font-size:62px;color:{NAVY}'>헬리오시티</div>
<div class='lab' style='left:50px;top:298px;font-size:40px;color:{NAVY}'>2018년 입주</div>
<div class='t' style='left:48px;top:376px;font-size:50px;color:{TEAL}'>올림픽파크포레온</div>
<div class='lab' style='left:50px;top:440px;font-size:40px;color:{TEAL}'>2024년 입주</div>
{sa}{sb}{axis(Xa, 520)}
<div class='lab' style='left:50px;top:590px;font-size:46px;color:{INK}'>{SMALL}</div>
"""

# h1b — 입주 연도 눈금(2016~2026) 위 두 단지 점 + '6년 가까이' 괄호, 아래 '평당 중앙' 막대 두 개(실제 비율 = 거의 같은 길이).
X0, W = 80, 1100
YX = lambda y: X0 + W * (y - 2016) / 10
yh, yo = 2018 + 11.5 / 12, 2024 + 10.5 / 12
mh, mo = st.median(HE), st.median(OP)
PX = lambda v: v / 12500 * 860
years = ''.join(f"<div class='lab' style='left:{YX(y) - 50:.0f}px;top:276px;width:100px;text-align:center;font-size:30px;color:{GREY}'>{y}</div>" for y in (2016, 2018, 2020, 2022, 2024, 2026))
h1b = f"""<div style='position:absolute;inset:0;background:#EEF1F5'></div>
<div id='b0' class='t' data-fit='1180' style='left:48px;top:34px;font-size:118px;color:{INK}'><span style='color:{RED}'>6년 가까이</span> 늦게 지었는데</div>
<div style='position:absolute;left:{X0}px;top:262px;width:{W}px;border-top:6px solid {GREY}'></div>
{years}
<div style='position:absolute;left:{YX(yh):.0f}px;top:200px;width:{YX(yo) - YX(yh):.0f}px;height:40px;border:6px solid {RED};border-bottom:none;border-radius:10px 10px 0 0'></div>
<div style='position:absolute;left:{YX(yh) - 14:.0f}px;top:248px;width:28px;height:28px;border-radius:50%;background:{NAVY}'></div>
<div style='position:absolute;left:{YX(yo) - 14:.0f}px;top:248px;width:28px;height:28px;border-radius:50%;background:{TEAL}'></div>
<div class='lab' style='left:56px;top:350px;font-size:44px;color:{INK}'>평당<br>중앙</div>
<div style='position:absolute;left:200px;top:330px;width:{PX(mh):.0f}px;height:96px;background:{NAVY};border-radius:0 12px 12px 0'></div>
<div class='t' style='left:226px;top:350px;font-size:58px;color:#fff'>헬리오시티 · 2018</div>
<div style='position:absolute;left:200px;top:446px;width:{PX(mo):.0f}px;height:96px;background:{TEAL};border-radius:0 12px 12px 0'></div>
<div class='t' style='left:226px;top:466px;font-size:58px;color:#fff'>올림픽파크포레온 · 2024</div>
<div class='lab' style='left:50px;top:592px;font-size:46px;color:{INK}'>{SMALL}</div>
"""

# h1c — 큰 글씨 두 줄(왼쪽, 150px) + 오른쪽 아래쪽에 거래 점 구름 두 줄 — 글자가 주인공, 점은 '같은 자리' 증거.
sc1, Xc = strip(HE, 600, 640, 372, 80, NAVY)
sc2, _ = strip(OP, 600, 640, 470, 80, TEAL)
h1c = f"""<div style='position:absolute;inset:0;background:#FBF8F2'></div>
<div class='t' style='left:48px;top:40px;font-size:150px;color:{RED}'>6년 가까이</div>
<div class='t' style='left:48px;top:196px;font-size:150px;color:{INK}'>늦게 지었는데</div>
<div class='t' style='left:48px;top:372px;font-size:56px;color:{NAVY}'>헬리오시티</div>
<div class='lab' style='left:340px;top:384px;font-size:40px;color:{NAVY}'>2018</div>
<div class='t' style='left:48px;top:470px;font-size:48px;color:{TEAL}'>올림픽파크포레온</div>
<div class='lab' style='left:470px;top:476px;font-size:40px;color:{TEAL}'>2024</div>
{sc1}{sc2}
<div class='lab' style='left:50px;top:592px;font-size:46px;color:{INK}'>{SMALL}</div>
"""
VARIANTS = {'h1a': h1a, 'h1b': h1b, 'h1c': h1c}


# ── 2차(09:1x) — 1차 h1a 6.5(제미나이 7.5·7.5·Claude 5·레드팀 7). 공통 지적: 168px에서 단지 이름 안 읽힘(62/50px), 점 남색이 회색처럼, 결론 숫자 없음.
# h1d: h1a 밝은 판 유지, 이름 둘 다 66px 같은 크기, 점 띠 x 600~1240·지름 26·불투명 .9·남색 #24365F, 중앙선 옆 '평당 중앙 1억 1천만' 44px(답은 제목과 같은 말, 하락·차이% 없음).
# h1e: 같은 배치 어두운 판(#121826, 제목 흰색·'6년 가까이' #FF4B3E, 헬리오 흰 점·포레온 #1FB58F) — Claude 처방, 경쟁 어두운 사진과 겹침은 심사로 잰다.
def rows(bg, ink, red, c1, c2, sub, axc):
    s1, X = strip(HE, 600, 640, 196, 116, c1, r=13)
    s2, _ = strip(OP, 600, 640, 362, 116, c2, r=13)
    s1 = s1.replace('opacity:.75', 'opacity:.9'); s2 = s2.replace('opacity:.75', 'opacity:.9')
    if ink != INK:
        s1 = s1.replace(f'background:{INK}', f'background:{ink}'); s2 = s2.replace(f'background:{INK}', f'background:{ink}')
    m = X(st.median(HE))
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div id='t0' class='t' data-fit='1184' style='left:48px;top:36px;font-size:118px;color:{ink}'><span style='color:{red}'>6년 가까이</span> 늦게 지었는데</div>
<div class='t' style='left:48px;top:204px;font-size:66px;color:{c1}'>헬리오시티</div>
<div class='lab' style='left:52px;top:280px;font-size:40px;color:{sub}'>2018년 입주</div>
<div id='n2' class='t' data-fit='540' style='left:48px;top:370px;font-size:66px;color:{c2}'>올림픽파크포레온</div>
<div class='lab' style='left:52px;top:446px;font-size:40px;color:{sub}'>2024년 입주</div>
{s1}{s2}
<div class='lab' style='left:{X(8000) - 60:.0f}px;top:500px;width:120px;text-align:center;font-size:30px;color:{axc}'>8천만</div>
<div class='lab' style='left:{m - 230:.0f}px;top:496px;width:400px;text-align:center;font-size:44px;color:{ink}'>평당 중앙 1억 1천만</div>
<div class='lab' style='left:50px;top:592px;font-size:46px;color:{ink}'>{SMALL}</div>
"""
VARIANTS['h1d'] = rows(PAPER, INK, RED, '#24365F', TEAL, GREY, GREY)
VARIANTS['h1e'] = rows('#121826', '#FFFFFF', '#FF4B3E', '#DCE3F0', '#1FB58F', '#9AA4B8', '#8A93A3')


# ── 3차(09:1x) — 2차 h1d 6.58(제미나이 6.5·6·Claude 6·레드팀 7.5), h1e 6.5(겹침 3 반려). 처방: 이름 78~84px, 연도 빨강 48px('6년'=입주 차이로 묶음),
#    중앙선 둘을 빨강 22% 띠로 묶고 '둘 다 평당 중앙 1억 1천만', '8천만' 대신 '점 1개 = 거래 1건', 크림 한 단계 진하게(#E9E2D3).
# h1f: 위 처방 그대로(제목 '6년 가까이' 빨강). h1g: 같은 판, 강조색을 빨강 대신 진한 청록(경쟁2 빨강 띠와 겹침 줄이기 시험).
def rows3(acc, bg='#E9E2D3'):
    x0, w = 690, 550
    s1, X = strip(HE, x0, w, 196, 112, '#24365F', r=13)
    s2, _ = strip(OP, x0, w, 344, 112, TEAL, r=13)
    s1 = s1.replace('opacity:.75', 'opacity:.9'); s2 = s2.replace('opacity:.75', 'opacity:.9')
    a, b = X(st.median(OP)), X(st.median(HE))
    band = f"<div style='position:absolute;left:{a - 22:.0f}px;top:180px;width:{b - a + 44:.0f}px;height:292px;background:{acc};opacity:.22;border-radius:8px'></div>"
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div id='t0' class='t' data-fit='1184' style='left:48px;top:36px;font-size:118px;color:{INK}'><span style='color:{acc}'>6년 가까이</span> 늦게 지었는데</div>
{band}
<div id='n1' class='t' data-fit='620' style='left:44px;top:196px;font-size:80px;color:#24365F'>헬리오시티</div>
<div class='lab' style='left:48px;top:282px;font-size:46px;color:{acc}'>2018년 입주</div>
<div id='n2' class='t' data-fit='630' style='left:44px;top:344px;font-size:80px;color:{TEAL}'>올림픽파크포레온</div>
<div class='lab' style='left:48px;top:430px;font-size:46px;color:{acc}'>2024년 입주</div>
{s1}{s2}
<div id='md' class='lab' data-fit='560' style='left:{x0}px;top:482px;width:560px;text-align:center;font-size:48px;color:{INK}'>둘 다 평당 중앙 1억 1천만</div>
<div class='lab' style='left:{x0}px;top:540px;font-size:30px;color:{GREY}'>점 1개 = 거래 1건</div>
<div class='lab' style='left:50px;top:596px;font-size:46px;color:{INK}'>{SMALL}</div>
"""
VARIANTS['h1f'] = rows3(RED)
VARIANTS['h1g'] = rows3('#0B6E60')


# ── 4차(09:1x) — 3차 h1f 6.5(제미나이 7·7·Claude 6·레드팀 6.5) · h1g 6.33 · h1d 6.0. 세 명 공통: 결론 줄 26px(168px)라 사라짐, 연도가 다음 단지에 붙어 읽힘,
#    빨강 세 곳(제목·연도·띠)=경고 느낌. 처방: 결론 '둘 다 1억 1천만'을 80px급으로, 연도는 자기 단지 바로 아래·자기 색, 빨강은 제목 한 곳, 띠 무채색, 포레온 점 명도 올림.
def rows4(bg='#ECE6DA'):
    x0, w, C1, C2 = 668, 572, '#22325A', '#16A085'
    s1, X = strip(HE, x0, w, 186, 104, C1, r=14)
    s2, _ = strip(OP, x0, w, 328, 104, C2, r=14)
    s1 = s1.replace('opacity:.75', 'opacity:.92'); s2 = s2.replace('opacity:.75', 'opacity:.92')
    a, b = X(st.median(OP)), X(st.median(HE))
    band = f"<div style='position:absolute;left:{a - 24:.0f}px;top:170px;width:{b - a + 48:.0f}px;height:278px;background:{INK};opacity:.13;border-radius:8px'></div>"
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div id='t0' class='t' data-fit='1184' style='left:48px;top:30px;font-size:118px;color:{INK}'><span style='color:{RED}'>6년 가까이</span> 늦게 지었는데</div>
{band}
<div id='n1' class='t' data-fit='600' style='left:44px;top:184px;font-size:80px;color:{C1}'>헬리오시티</div>
<div class='lab' style='left:48px;top:268px;font-size:40px;color:{C1}'>2018년 입주</div>
<div id='n2' class='t' data-fit='600' style='left:44px;top:330px;font-size:80px;color:{C2}'>올림픽파크포레온</div>
<div class='lab' style='left:48px;top:412px;font-size:40px;color:{C2}'>2024년 입주</div>
{s1}{s2}
<div id='md' class='t' data-fit='590' style='left:{x0 - 10}px;top:466px;font-size:82px;color:{INK}'>둘 다 평당 1억 1천만</div>
<div class='lab' style='left:50px;top:596px;font-size:46px;color:{INK}'>{SMALL}</div>
"""
VARIANTS['h1h'] = rows4()


# ── 5차(10/11 17:0x, 새 형식) — 4차까지 같은 판(제목 위·이름 왼쪽 세로·점 오른쪽) 최고 6.58. 공통 지적: 168px에서 이름이 경쟁(화면 30~40%) 대비 절반, 점 구름=먼지, 결론 큰 숫자=경쟁 '억 줄' 겹침.
#    처방(judges.md 다음 판): 두 단지를 좌우 두 칸 주인공으로, 칸마다 큰 입주 연도, 점은 칸 아래 얇은 띠(같은 눈금·중앙선 같은 자리), 결론 숫자 없음.
# h1i: 이름이 주인공(헬리오 100px·포레온 fit 560), 연도 110px, 칸 사이 굵은 '=' (점 띠 높이) — '같다'를 숫자 없이 기호로.
# h1j: 연도가 주인공(180px, 2018 남색·2024 청록), 이름 64px 위, 칸 사이 빨강 화살표 '→ 6년'은 쓰지 않고 제목에 맡김, 점 띠 + '='.
def cols(name_px, year_px, name_top, year_top, strip_top, bg='#ECE6DA'):
    C1, C2 = '#22325A', '#12866F'
    L, R, Wc = 44, 664, 572
    s1, X1 = strip(HE, L + 20, Wc - 40, strip_top, 70, C1, r=11)
    s2, X2 = strip(OP, R + 20, Wc - 40, strip_top, 70, C2, r=11)
    s1 = s1.replace('opacity:.75', 'opacity:.9'); s2 = s2.replace('opacity:.75', 'opacity:.9')
    card = lambda x, c: f"<div style='position:absolute;left:{x}px;top:168px;width:{Wc}px;height:{strip_top + 70 + 26 - 168}px;background:#FFFFFF;border-radius:18px;border-top:12px solid {c}'></div>"
    eq = f"<div class='t' style='left:612px;top:{strip_top - 4}px;font-size:84px;color:{INK}'>=</div>"
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div id='t0' class='t' data-fit='1190' style='left:44px;top:34px;font-size:112px;color:{INK}'><span style='color:{RED}'>6년 가까이</span> 늦게 지었는데</div>
{card(L, C1)}{card(R, C2)}
<div id='n1' class='t' data-fit='532' style='left:{L + 20}px;top:{name_top}px;font-size:{name_px}px;color:{C1}'>헬리오시티</div>
<div id='n2' class='t' data-fit='532' style='left:{R + 20}px;top:{name_top}px;font-size:{name_px}px;color:{C2}'>올림픽파크포레온</div>
<div class='t' style='left:{L + 20}px;top:{year_top}px;font-size:{year_px}px;color:{INK}'>2018<span style='font:700 {year_px // 3}px PD'> 입주</span></div>
<div class='t' style='left:{R + 20}px;top:{year_top}px;font-size:{year_px}px;color:{INK}'>2024<span style='font:700 {year_px // 3}px PD'> 입주</span></div>
{s1}{s2}{eq}
<div class='lab' style='left:48px;top:600px;font-size:44px;color:{INK}'>{SMALL}</div>
"""
VARIANTS['h1i'] = cols(100, 110, 196, 314, 450)
VARIANTS['h1j'] = cols(64, 180, 192, 270, 458)


# ── 6차(10/11 17:2x) — 5차 h1j 6.97(제미나이 6.5·7.5·Claude 7·레드팀 6.9, 겹침 1), h1i 6.47, h1d 6.08. 세 명 공통: 점 띠·'='가 168px에서 안 보임,
#    '무엇이 같은지'(평당값)가 아래 작은 글씨에만, 베이지 판 대비 약함. 처방: 점 띠 삭제, 칸 아래 전폭 검은 띠 '둘 다 평당 1억 1천만'(중앙 11,087·10,988 둘 다 반올림 1억 1천만),
#    칸 사이 '=' 키움. h1k 밝은 판·h1l 어두운 판(대비 시험).
def cols6(dark=False):
    C1, C2 = ('#8FB3FF', '#2FD3A6') if dark else ('#22325A', '#12866F')
    bg, card_bg, ink = ('#10141F', '#1B2232', '#FFFFFF') if dark else ('#ECE6DA', '#FFFFFF', INK)
    L, R, Wc = 44, 684, 552
    card = lambda x, c: f"<div style='position:absolute;left:{x}px;top:164px;width:{Wc}px;height:272px;background:{card_bg};border-radius:18px;border-top:14px solid {c}'></div>"
    band_bg, band_fg = ('#FFFFFF', INK) if dark else (INK, '#FFFFFF')
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div id='t0' class='t' data-fit='1190' style='left:44px;top:30px;font-size:112px;color:{ink}'><span style='color:{"#FF4B3E" if dark else RED}'>6년 가까이</span> 늦게 지었는데</div>
{card(L, C1)}{card(R, C2)}
<div id='n1' class='t' data-fit='532' style='left:{L + 20}px;top:190px;font-size:66px;color:{C1}'>헬리오시티</div>
<div id='n2' class='t' data-fit='532' style='left:{R + 20}px;top:190px;font-size:66px;color:{C2}'>올림픽파크포레온</div>
<div class='t' style='left:{L + 20}px;top:270px;font-size:144px;color:{ink}'>2018<span style='font:700 50px PD'> 입주</span></div>
<div class='t' style='left:{R + 20}px;top:270px;font-size:144px;color:{ink}'>2024<span style='font:700 50px PD'> 입주</span></div>
<div style='position:absolute;left:{L}px;top:452px;width:{R + Wc - L}px;height:112px;background:{band_bg};border-radius:18px'></div>
<div class='t' style='left:0;width:1280px;text-align:center;top:466px;font-size:84px;color:{band_fg}'>둘 다 평당 1억 1천만</div>
<div class='t' style='left:613px;top:262px;font-size:110px;color:{ink}'>=</div>
<div class='lab' style='left:48px;top:600px;font-size:44px;color:{ink}'>{SMALL}</div>
"""
VARIANTS['h1k'] = cols6()
VARIANTS['h1l'] = cols6(dark=True)


# ── 7차(10/11 17:3x) — 6차 h1k 6.67(제미나이 7.5·7.5·Claude 6·레드팀 6.5 겹침 2)·h1l 6.6·h1j 5.83. 레드팀: meta title이 16:36 질문형('포레온은 헬리오시티보다 비쌀까?')으로 바뀜 →
#    띠 '둘 다 1억 1천만'은 제목 질문의 답을 미리 말함 + 전폭 억 줄 = 경쟁 '억 하락' 줄 겹침, 연도 사이 '='는 '2018=2024' 오독. 처방: 띠·'=' 삭제.
# h1m: 두 칸만(이름·큰 연도), 칸 아래에 각 단지 평당 칸 '평당 ?' — 답은 제목 질문에 맡기고 '새 단지 값'을 궁금증으로(숫자 없음).
# h1n: 같은 칸, 칸 안에 실제 평당 중앙(F4 11,087 · F5 원자료 10,988) '1억 1,087만'·'1억 988만' — 새 단지가 오히려 조금 낮다는 반전을 숫자 둘로(크기 중간, 전폭 줄 아님).
def cols7(reveal):
    C1, C2, ink = '#22325A', '#12866F', INK
    L, R, Wc = 44, 684, 552
    card = lambda x, c: f"<div style='position:absolute;left:{x}px;top:164px;width:{Wc}px;height:392px;background:#FFFFFF;border-radius:18px;border-top:14px solid {c}'></div>"
    v1, v2 = ('1억 1,087만', '1억 988만') if reveal else ('?', '?')
    vs = 68 if reveal else 96
    price = lambda x, c, v: (f"<div style='position:absolute;left:{x + 20}px;top:438px;width:{Wc - 40}px;height:98px;background:{c};border-radius:12px'></div>"
                             f"<div class='lab' style='left:{x + 40}px;top:462px;font-size:46px;color:#fff'>평당</div>"
                             f"<div class='t' style='left:{x + 140}px;top:{454 if reveal else 444}px;font-size:{vs}px;color:#fff'>{v}</div>")
    return f"""<div style='position:absolute;inset:0;background:#ECE6DA'></div>
<div id='t0' class='t' data-fit='1190' style='left:44px;top:30px;font-size:112px;color:{ink}'><span style='color:{RED}'>6년 가까이</span> 늦게 지었는데</div>
{card(L, C1)}{card(R, C2)}
<div id='n1' class='t' data-fit='512' style='left:{L + 20}px;top:190px;font-size:66px;color:{C1}'>헬리오시티</div>
<div id='n2' class='t' data-fit='512' style='left:{R + 20}px;top:190px;font-size:66px;color:{C2}'>올림픽파크포레온</div>
<div class='t' style='left:{L + 20}px;top:276px;font-size:144px;color:{ink}'>2018<span style='font:700 50px PD'> 입주</span></div>
<div class='t' style='left:{R + 20}px;top:276px;font-size:144px;color:{ink}'>2024<span style='font:700 50px PD'> 입주</span></div>
{price(L, C1, v1)}{price(R, C2, v2)}
<div class='lab' style='left:48px;top:600px;font-size:44px;color:{ink}'>{SMALL}</div>
"""
VARIANTS['h1m'] = cols7(False)
VARIANTS['h1n'] = cols7(True)


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||e.closest('svg')||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'&&c.tagName!=='BR'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});
      document.querySelectorAll('div[style*="border-radius:50%"]').forEach(e=>{const b=e.getBoundingClientRect();if((b.right>960&&b.bottom>576)||b.bottom>684)bad.push('점 '+Math.round(b.left)+','+Math.round(b.bottom))});return bad}""")


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
    print('중앙', st.median(HE), st.median(OP))
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
