# P-1 '국민연금 수령나이' 썸네일 시안(2026-10-10 visual-designer, 운영실장 19:09 배차 — 비축 롱폼, 주간 선정 10/12 전)
# 문구: ep/P-1/copy/titles.md 1위(copywriter 18:57, 결선 8.33) — 큰 글씨 '5년 당김 76.7세 / 1년 당김 80.7세'(80.7세 크게),
#        작은 줄 '제때 받은 쪽이 따라잡는 나이 · 1969년생·월 100만원 가정'(지우지 말 것). 금지: '15만원씩'·'월급 519만원'·'6/17 개정'.
#        더한 말은 주제 꼬리표 '국민연금'(제목 첫 낱말) 하나뿐.
# 숫자: ep/P-1/calc_out.txt 2절에서 읽고 문구와 assert(76.67→76.7, 80.67→80.7).
# 경쟁 5(compete.md 상위 5) 공통: 검정·주황 바탕 + 노랑/흰 테두리 글씨, 인물 사진·만화 노인·금화·돈자루. 우리: 사진·인물·테두리 0,
#        밝은 판 + 실제 나이 눈금(65~85세) 위 막대 두 개 — '오래 당길수록 더 빨리 따라잡힌다' 반전을 그림 길이로.
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576, 아래 5%(y≥684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'P-1')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
A5 = float(re.search(r'5년 당김 월 700,000원 → 제때와 같아지는 나이 ([\d.]+)세', calc).group(1))
A1 = float(re.search(r'1년 당김 월 940,000원 → 제때와 같아지는 나이 ([\d.]+)세', calc).group(1))
assert re.search(r'1969년생 제때 65세', calc)
S5, S1 = f'{A5:.1f}세', f'{A1:.1f}세'
assert (S5, S1) == ('76.7세', '80.7세'), (S5, S1)
SM0, SM1 = '제때 받은 쪽이 따라잡는 나이', '1969년생·월 100만원 가정'
SM0J = '덜 당겼는데 4년 더 늦는 이유'  # p1j 띠 전용(copywriter 10/12): 80.7-76.7=4.0, 정의는 제목('따라잡히는 나이')이 받침

INK, RED, NAVY, GREY, CREAM, BG = '#16181D', '#E5322D', '#1E2A44', '#6B7280', '#F6F1E7', '#121418'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]


def ruler(x0, y0, w, lo=65, hi=85, col=GREY, dy=22):
    """나이 눈금 65~85세(5세 간격). 반환 (html, 나이→x 함수)"""
    X = lambda a: x0 + w * (a - lo) / (hi - lo)
    s = f"<div style='position:absolute;left:{x0}px;top:{y0}px;width:{w}px;border-top:4px solid {col}'></div>"
    for a in range(lo, hi + 1, 5):
        s += f"<div style='position:absolute;left:{X(a) - 2:.0f}px;top:{y0 - 12}px;width:4px;height:28px;background:{col}'></div>"
        s += f"<div class='lab' style='left:{X(a) - 30:.0f}px;top:{y0 + dy}px;width:60px;text-align:center;font-size:30px;color:{col}'>{a}</div>"
    return s, X


# p1a — 크림 판 + 나이 눈금(65~85세) 위 막대 두 개(65세 제때에서 따라잡는 나이까지). 5년 당김 짧은 남색, 1년 당김 긴 빨강 — 길이 = 반전.
_r, X = ruler(60, 514, 1000)
p1a = f"""<div style='position:absolute;inset:0;background:{CREAM}'></div>
<div class='t' style='left:52px;top:34px;font-size:60px;color:{NAVY}'>국민연금</div>
<div class='lab' style='left:300px;top:46px;font-size:38px;color:{INK}'>{SM0}</div>
<div class='t' style='left:52px;top:130px;font-size:84px;color:{NAVY}'>5년 당김</div>
<div style='position:absolute;left:{X(65):.0f}px;top:236px;width:{X(A5) - X(65):.0f}px;height:56px;background:{NAVY};border-radius:0 10px 10px 0'></div>
<div class='t' style='left:{X(A5) + 20:.0f}px;top:214px;font-size:100px;color:{NAVY}'>{S5}</div>
<div class='t' style='left:52px;top:326px;font-size:84px;color:{RED}'>1년 당김</div>
<div style='position:absolute;left:{X(65):.0f}px;top:430px;width:{X(A1) - X(65):.0f}px;height:72px;background:{RED};border-radius:0 10px 10px 0'></div>
<div id='a1' class='t' data-fit='400' style='left:{X(A1) + 16:.0f}px;top:296px;font-size:190px;color:{RED}'>{S1}</div>
{_r}
<div class='fine' style='color:{INK};top:606px;font-size:34px'>{SM1}</div>
"""

# p1b — 어두운 판, 글자 두 줄이 주인공(5년 줄은 회색, 1년 줄은 빨강으로 크게) + 아래 눈금 위 두 점
_r2, X2 = ruler(60, 540, 820, col='#8A93A3')
p1b = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div class='t' style='left:52px;top:38px;font-size:60px;color:#fff'>국민연금</div>
<div class='lab' style='left:300px;top:50px;font-size:38px;color:#C9CED8'>{SM0}</div>
<div class='t' style='left:52px;top:134px;font-size:104px;color:#C9CED8'>5년 당김 {S5}</div>
<div class='t' style='left:52px;top:300px;font-size:104px;color:#fff'>1년 당김</div>
<div id='b1' class='t' data-fit='640' style='left:500px;top:262px;font-size:210px;color:{RED}'>{S1}</div>
{_r2}
<div style='position:absolute;left:{X2(A5) - 18:.0f}px;top:524px;width:36px;height:36px;border-radius:50%;background:#C9CED8'></div>
<div style='position:absolute;left:{X2(A1) - 24:.0f}px;top:518px;width:48px;height:48px;border-radius:50%;background:{RED}'></div>
<div class='fine' style='color:#9AA0AA;top:622px;font-size:28px'>{SM1}</div>
"""

# p1c — 흰 판 좌우 두 칸 비교(5년 당김 | 1년 당김), 오른쪽 칸이 더 큰 숫자. 오른쪽 아래 비움 위해 칸은 y<560.
p1c = f"""<div style='position:absolute;inset:0;background:#FBFAF6'></div>
<div class='t' style='left:52px;top:34px;font-size:62px;color:{NAVY}'>국민연금</div>
<div class='lab' style='left:310px;top:46px;font-size:38px;color:{INK}'>{SM0}</div>
<div style='position:absolute;left:40px;top:130px;width:500px;height:420px;background:#E6E9EF;border-radius:24px'></div>
<div class='t' style='left:80px;top:170px;font-size:84px;color:{NAVY}'>5년 당김</div>
<div id='c0' class='t' data-fit='430' style='left:76px;top:330px;font-size:150px;color:{NAVY}'>{S5}</div>
<div style='position:absolute;left:570px;top:130px;width:670px;height:420px;background:{RED};border-radius:24px'></div>
<div class='t' style='left:610px;top:170px;font-size:84px;color:#fff'>1년 당김</div>
<div id='c1' class='t' data-fit='600' style='left:604px;top:300px;font-size:220px;color:#fff'>{S1}</div>
<div class='fine' style='color:{INK};top:590px;font-size:30px'>{SM1}</div>
"""
VARIANTS = {'p1a': p1a, 'p1b': p1b, 'p1c': p1c}

# ── 2차(19:1x) — 1차 제미나이 3.1-lite p1a 6·6.5 / p1b 7·7.5 / p1c 5·6, 168px 판에서 우리 글자가 경쟁보다 작게 보임.
# p1d — 1차 Claude 지적(부제가 168px에서 안 읽혀 76.7·80.7이 무슨 나이인지 모름, 검정 바탕 경쟁과 겹침) 반영:
#        짙은 남색 판, 부제를 흰 굵은 글씨 56px 한 줄로 키움, 눈금 없앰(168px에서 안 보임), 두 줄 120/250px.
NV2 = '#14203A'
p1d = f"""<div style='position:absolute;inset:0;background:{NV2}'></div>
<div class='t' style='left:48px;top:30px;font-size:78px;color:#fff'>국민연금</div>
<div class='lab' style='left:50px;top:124px;font-size:56px;color:#fff'>{SM0}</div>
<div class='t' style='left:48px;top:222px;font-size:116px;color:#97A3BA'>5년 당김 {S5}</div>
<div class='t' style='left:48px;top:388px;font-size:116px;color:#fff'>1년 당김</div>
<div id='d1' class='t' data-fit='700' style='left:520px;top:338px;font-size:240px;color:#FF4B3E'>{S1}</div>
<div class='fine' style='color:#C9D1E0;top:612px;font-size:32px'>{SM1}</div>
"""
# p1e — 1차 Claude 1위 p1c 처방: 부제를 두 칸 위 띠로(남색 바탕 흰 글자 58px), 칸 비율 회색 35 : 빨강 65, 칸을 아래로 늘리고 오른쪽 아래 끝은 비움.
p1e = f"""<div style='position:absolute;inset:0;background:#FBFAF6'></div>
<div class='t' style='left:44px;top:22px;font-size:70px;color:{NAVY}'>국민연금</div>
<div class='lab' style='left:340px;top:42px;font-size:34px;color:{INK}'>{SM1}</div>
<div style='position:absolute;left:30px;top:116px;width:1220px;height:92px;background:{NAVY};border-radius:16px'></div>
<div class='lab' style='left:62px;top:130px;font-size:58px;color:#fff'>{SM0}</div>
<div style='position:absolute;left:30px;top:226px;width:410px;height:384px;background:#E3E7EE;border-radius:22px'></div>
<div class='t' style='left:62px;top:258px;font-size:78px;color:{NAVY}'>5년 당김</div>
<div id='e0' class='t' data-fit='360' style='left:58px;top:420px;font-size:130px;color:{NAVY}'>{S5}</div>
<div style='position:absolute;left:460px;top:226px;width:790px;height:340px;background:{RED};border-radius:22px'></div>
<div class='t' style='left:496px;top:258px;font-size:78px;color:#fff'>1년 당김</div>
<div id='e1' class='t' data-fit='720' style='left:490px;top:356px;font-size:220px;color:#fff'>{S1}</div>
"""
VARIANTS['p1e'] = p1e
VARIANTS['p1d'] = p1d



# p1f — 1차 레드팀 1위 p1a 처방: 주어('제때 받은 쪽이 따라잡는 나이')를 54px 축 제목으로 눈금 바로 위, 숫자를 막대 끝 같은 줄,
#        막대 굵게(80/100px), 크림 한 단계 진하게, 65세 굵은 기준선(막대 = 받는 기간이 아니라 눈금 위 나이), 작은 줄은 눈금 아래.
_r4, X4 = ruler(60, 516, 880, col='#4B5262')
p1f = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
<div class='t' style='left:48px;top:26px;font-size:80px;color:{NAVY}'>국민연금</div>
<div style='position:absolute;left:{X4(65) - 5:.0f}px;top:136px;width:10px;height:384px;background:{INK}'></div>
<div style='position:absolute;left:{X4(65):.0f}px;top:142px;width:{X4(A5) - X4(65):.0f}px;height:104px;background:{NAVY};border-radius:0 12px 12px 0'></div>
<div class='t' style='left:{X4(65) + 24:.0f}px;top:160px;font-size:70px;color:#fff'>5년 당김</div>
<div class='t' style='left:{X4(A5) + 18:.0f}px;top:142px;font-size:110px;color:{NAVY}'>{S5}</div>
<div style='position:absolute;left:{X4(65):.0f}px;top:272px;width:{X4(A1) - X4(65):.0f}px;height:132px;background:{RED};border-radius:0 12px 12px 0'></div>
<div class='t' style='left:{X4(65) + 24:.0f}px;top:302px;font-size:76px;color:#fff'>1년 당김</div>
<div id='f1' class='t' data-fit='420' style='left:{X4(A1) + 14:.0f}px;top:244px;font-size:186px;color:{RED}'>{S1}</div>
<div class='lab' style='left:{X4(65) + 20:.0f}px;top:428px;font-size:56px;color:{INK}'>{SM0}</div>
{_r4}
<div class='fine' style='color:{INK};top:604px;left:60px;font-size:36px'>{SM1}</div>
"""
VARIANTS['p1f'] = p1f


# ── 3차(10/12 19:2x) — 2차 레드팀 열린 위험: 막대 둘 다 65세에서 시작 → '65세부터 76.7세까지 받는 기간'으로 오독(실제 시작 60·64세).
# p1g — 처방 ①: 막대 없앰. 눈금(65~85세) 위 끝점 두 개 + 숫자에서 눈금까지 내린 점선. 위치 차이가 반전(80.7이 더 오른쪽).
_r5, X5 = ruler(60, 520, 880, col='#4B5262')
p1g = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
<div class='t' style='left:48px;top:26px;font-size:80px;color:{NAVY}'>국민연금</div>
<div class='lab' style='left:400px;top:46px;font-size:46px;color:{INK}'>{SM0}</div>
<div class='t' style='left:52px;top:150px;font-size:76px;color:{NAVY}'>5년 당김</div>
<div class='t' style='left:{X5(A5) - 150:.0f}px;top:136px;font-size:104px;color:{NAVY}'>{S5}</div>
<div style='position:absolute;left:{X5(A5) - 3:.0f}px;top:250px;height:262px;border-left:6px dashed {NAVY}'></div>
<div class='t' style='left:52px;top:330px;font-size:84px;color:{RED}'>1년 당김</div>
<div id='g1' class='t' data-fit='420' style='left:{X5(A5) + 34:.0f}px;top:262px;font-size:180px;color:{RED}'>{S1}</div>
<div style='position:absolute;left:{X5(A1) - 4:.0f}px;top:446px;height:66px;border-left:8px dashed {RED}'></div>
{_r5}
<div style='position:absolute;left:{X5(A5) - 22:.0f}px;top:498px;width:44px;height:44px;border-radius:50%;background:{NAVY}'></div>
<div style='position:absolute;left:{X5(A1) - 30:.0f}px;top:490px;width:60px;height:60px;border-radius:50%;background:{RED}'></div>
<div class='fine' style='color:{INK};top:604px;left:60px;font-size:36px'>{SM1}</div>
"""
VARIANTS['p1g'] = p1g

# p1h — 처방 ②의 변형: p1f 막대 그대로(길이 = 반전, Claude 2차), 막대가 시작하는 굵은 선 위에 '제때 65세'(calc 1절 원문 낱말)를 붙여
#        막대 = '제때 받은 사람 기준 눈금'임을 1초에 보이게. 축 제목 줄은 그대로.
p1h = p1f.replace(f"<div class='t' style='left:48px;top:26px;font-size:80px;color:{NAVY}'>국민연금</div>",
    f"<div class='t' style='left:48px;top:26px;font-size:80px;color:{NAVY}'>국민연금</div>"
    f"<div class='lab' style='left:{X4(65) - 12:.0f}px;top:96px;font-size:30px;color:#fff;background:{INK};padding:2px 10px;border-radius:6px'>제때 65세</div>")
assert p1h != p1f
VARIANTS['p1h'] = p1h


# ── 4차 — 3차 세 명: p1f 6.53·p1g 6.27·p1h 6.70(7 미달). 레드팀 p1g 1위(7.2, 오독 줄었음) 처방: 숫자를 자기 점에 붙이고 '1년 당김'을 빨강 점 쪽으로.
#        Claude: 점 크게·숫자를 자기 점 바로 위에. p1h '제때 65세' 꼬리표는 168px에서 안 보이고 오히려 '65세 시작' 인상 강화(레드팀) → 버림.
# p1i — 끝점판: 5년 줄은 숫자 오른쪽 끝을 남색 점 x에 맞춰 위에서 실선으로 내림, 1년 줄은 빨강 점 x에서 시작해 아래 실선. 점 64/84px.
_r6, X6 = ruler(60, 556, 880, col='#4B5262')
p1i = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
<div class='t' style='left:48px;top:26px;font-size:80px;color:{NAVY}'>국민연금</div>
<div class='lab' style='left:400px;top:44px;font-size:48px;color:{INK}'>{SM0}</div>
<div class='t' style='left:52px;top:176px;font-size:60px;color:{NAVY}'>5년 당김</div>
<div id='i0' class='t' style='right:{1280 - X6(A5) - 8:.0f}px;top:150px;font-size:100px;color:{NAVY}'>{S5}</div>
<div style='position:absolute;left:{X6(A5) - 4:.0f}px;top:262px;width:8px;height:270px;background:{NAVY}'></div>
<div class='t' style='left:{X6(A1) + 6:.0f}px;top:204px;font-size:72px;color:{RED}'>1년 당김</div>
<div id='i1' class='t' data-fit='520' style='left:{X6(A1) - 10:.0f}px;top:284px;font-size:170px;color:{RED}'>{S1}</div>
<div style='position:absolute;left:{X6(A1) - 5:.0f}px;top:458px;width:10px;height:72px;background:{RED}'></div>
{_r6}
<div style='position:absolute;left:{X6(A5) - 32:.0f}px;top:524px;width:64px;height:64px;border-radius:50%;background:{NAVY}'></div>
<div style='position:absolute;left:{X6(A1) - 42:.0f}px;top:514px;width:84px;height:84px;border-radius:50%;background:{RED}'></div>
<div class='fine' style='color:{INK};top:630px;left:60px;font-size:34px'>{SM1}</div>
"""
VARIANTS['p1i'] = p1i


# ── 5차 — 4차 세 명: p1i 6.95(제미나이 8·6.5·Claude 6.4·레드팀 7.2)·p1f 6.17·p1h 6.32. 막대판은 오독 확정(레드팀·Claude 둘 다) → 끝점판으로 간다.
# p1j — p1i 처방 셋: ① 부제 '제때 받은 쪽이 따라잡는 나이'를 64px 흰 글자 남색 띠로(168px에서 읽히게, 두 심사 공통) ② 76.7세를 점 위 가운데로(레드팀)
#        ③ 빨강 점이 눈금 '80'을 가림 → 눈금 숫자를 점 아래로 내림(Claude). 문구 추가 없음(반전 문구 제안은 copywriter 몫).
_r7, X7 = ruler(60, 548, 880, col='#4B5262', dy=48)
p1j = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
<div class='t' style='left:48px;top:22px;font-size:76px;color:{NAVY}'>국민연금</div>
<div style='position:absolute;left:30px;top:116px;width:{X7(A1) + 330:.0f}px;height:88px;background:{NAVY};border-radius:14px'></div>
<div class='lab' style='left:58px;top:126px;font-size:62px;color:#fff'>{SM0}</div>
<div class='t' style='left:52px;top:252px;font-size:60px;color:{NAVY}'>5년 당김</div>
<div id='j0' class='t' style='left:{X7(A5) - 146:.0f}px;top:232px;font-size:100px;color:{NAVY}'>{S5}</div>
<div style='position:absolute;left:{X7(A5) - 4:.0f}px;top:338px;width:8px;height:186px;background:{NAVY}'></div>
<div class='t' style='left:{X7(A1) + 50:.0f}px;top:236px;font-size:60px;color:{RED}'>1년 당김</div>
<div id='j1' class='t' data-fit='440' style='left:{X7(A1) + 50:.0f}px;top:312px;font-size:150px;color:{RED}'>{S1}</div>
{_r7}
<div style='position:absolute;left:{X7(A5) - 30:.0f}px;top:518px;width:60px;height:60px;border-radius:50%;background:{NAVY}'></div>
<div style='position:absolute;left:{X7(A1) - 38:.0f}px;top:510px;width:76px;height:76px;border-radius:50%;background:{RED}'></div>
<svg style='position:absolute;left:0;top:0' width='1280' height='720'><line x1='{X7(A1) + 24:.0f}' y1='518' x2='{X7(A1) + 70:.0f}' y2='446' stroke='{RED}' stroke-width='9' stroke-linecap='round'/></svg>
<div class='fine' style='color:{INK};top:640px;left:60px;font-size:32px'>{SM1}</div>
"""
VARIANTS['p1j'] = p1j


# ── 6차(10/13) — SM0J 띠 '덜 당겼는데 4년 더 늦는 이유' 재심: 제미나이 7.5·7.5, Claude 5, 레드팀 5(오독 높음: '늦는'=수령이 늦다로 읽힘, '따라잡히는'이 화면에 없음)
#    → copywriter 조건대로 p1j는 SM0 원문으로 되돌림(1회). p1l = p1j + 두 심사 공통 처방(띠 글자 62→80px·띠 진하게) — 문구는 그대로.
VARIANTS['p1l'] = p1j.replace("left:30px;top:116px", "left:24px;top:110px").replace(f"width:{X7(A1) + 330:.0f}px;height:88px;background:{NAVY}", "width:990px;height:112px;background:#101A33").replace("left:58px;top:126px;font-size:62px", "left:50px;top:118px;font-size:82px")


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




# ── 8차(10/14 07:1x, PD 18:50 bench_check 미달 처방) — ① 주제 사물(숫자 초 꽂힌 생일 케이크 = '몇 살에') ② 글자 56→30자 안팎(눈금 숫자 뺌)
#    ③ 바탕 주제색(짙은 남색·짙은 초록, 평균 밝기 170 아래) ④ 소수점 둘 → '만 76세'·'만 80세'(calc 76.67·80.67의 만 나이, 8개월은 작은 꼬리).
#    76.67-76=0.67년=8개월, 80.67-80=0.67년=8개월 — assert. SM0·SM1 원문 유지(SM1 '지우지 말 것').
assert int(A5) == 76 and int(A1) == 80 and round((A5 - 76) * 12) == 8 and round((A1 - 80) * 12) == 8
N5, N1 = str(int(A5)), str(int(A1))


def cake(cx, top, w, num, numcol, fs, body='#F4E9D8', icing='#E5322D'):
    """숫자 초 케이크: cx 가운데, top=초 숫자 윗변. 케이크 몸통은 숫자 아래."""
    ch = fs * 0.95
    s = ''
    # 불꽃·심지(숫자마다)
    n = len(num); gap = fs * 0.62
    for i in range(n):
        x = cx - fs * 0.17 + (i - (n - 1) / 2) * gap
        s += f"<div style='position:absolute;left:{x - 3:.0f}px;top:{top - 8:.0f}px;width:6px;height:{fs * 0.24:.0f}px;background:#3A2F25'></div>"
        s += (f"<div style='position:absolute;left:{x - 16:.0f}px;top:{top - 64:.0f}px;width:32px;height:56px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;"
              f"background:radial-gradient(circle at 50% 70%,#FFF6C8 0 25%,#FFC93C 45%,#FF7A1A 80%);box-shadow:0 0 30px 8px rgba(255,170,40,.55)'></div>")
    s += f"<div class='t' style='left:{cx - w / 2:.0f}px;width:{w:.0f}px;text-align:center;top:{top - fs * 0.02:.0f}px;font-size:{fs}px;color:{numcol};-webkit-text-stroke:6px #fff;paint-order:stroke'>{num}<span style='font-size:{fs * 0.38:.0f}px'>세</span></div>"
    by = top + fs * 0.9
    s += f"<div style='position:absolute;left:{cx - w / 2:.0f}px;top:{by:.0f}px;width:{w:.0f}px;height:{fs * 0.62:.0f}px;background:{body};border-radius:14px'></div>"
    s += f"<div style='position:absolute;left:{cx - w / 2:.0f}px;top:{by:.0f}px;width:{w:.0f}px;height:{fs * 0.17:.0f}px;background:{icing};border-radius:14px 14px 22px 22px'></div>"
    s += f"<div style='position:absolute;left:{cx - w / 2 - 24:.0f}px;top:{by + fs * 0.62 - 8:.0f}px;width:{w + 48:.0f}px;height:16px;background:#C9CED8;border-radius:8px'></div>"
    return s


def p1cake(bg, band, k5='#9FB0D0'):
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='t' style='left:44px;top:26px;font-size:74px;color:#FFD23F'>국민연금</div>
<div class='lab' style='left:330px;top:40px;font-size:52px;color:#fff'>{SM0}</div>
<div class='t' style='left:150px;top:170px;font-size:64px;color:{k5}'>5년 당김</div>
{cake(270, 330, 300, N5, '#5B6B8C', 170, body='#DCE3EF', icing='#7F90B3')}
<div class='t' style='left:600px;top:140px;font-size:84px;color:#fff'>1년 당김</div>
{cake(735, 300, 400, N1, RED, 220)}
<div class='lab' style='left:462px;top:{300 + 220 * 0.33:.0f}px;font-size:60px;color:#fff'>→</div>
<div class='fine' style='color:#C9D1E0;top:636px;left:52px;font-size:30px'>{SM1} · 만 나이</div>
"""


VARIANTS['p1m'] = p1cake('#14203A', NAVY)          # 짙은 남색
VARIANTS['p1n'] = p1cake('#0F3A33', '#0B2C27')      # 짙은 초록(경쟁 5장에 없는 색)


# ── 9차 — 8차 Claude 6.4: 화살표가 '수령나이 76→80 연장'(정책 변경)으로 읽힘, 머리 글자 168px에서 사라짐.
# p1o = p1m에서 화살표 → 'vs'(두 경우 나란히), 머리 줄을 두 줄 크게('국민연금' 노랑 + SM0 흰 66px).
p1o = p1cake('#14203A', NAVY).replace("<div class='lab' style='left:462px;top:{:.0f}px;font-size:60px;color:#fff'>→</div>".format(300 + 220 * 0.33),
    "<div class='t' style='left:452px;top:{:.0f}px;font-size:64px;color:#9FB0D0'>vs</div>".format(300 + 220 * 0.30))
p1o = p1o.replace("<div class='lab' style='left:330px;top:40px;font-size:52px;color:#fff'>", "<div class='lab' style='left:330px;top:30px;font-size:66px;color:#fff'>")
p1o = p1o.replace(f">{SM0}</div>", f">{SM0.replace('제때', '제때(65세)')}</div>", 1)  # 레드팀: 기준점 '제때 65세' 없으면 '76세에 받는다' 오독 — calc 1절 '1969년생 제때 65세'
p1o = p1o.replace("left:330px;top:30px;font-size:66px", "left:310px;top:32px;font-size:60px")
assert '→' not in p1o and 'vs' in p1o and '제때(65세)' in p1o
VARIANTS['p1p'] = p1o                                                    # 남색
VARIANTS['p1o'] = p1o.replace("background:#14203A'", "background:#0F3A33'", 1)  # 짙은 초록(레드팀: 남색 경쟁작과 분리)


# ── 10차(10/14 09:1x, copywriter 07:54 큰 말 '당긴 이득 끝나는 나이' + 8~9차 처방 ①③) — p1n(초록) 바탕
#    머리 줄 SM0 → BW(74px 흰), 케이크 몸통에 월 수령액(calc 2절 5년 당김 700,000·1년 당김 940,000 → '월 70만'·'월 94만'), 화살표 → 'vs'(→ '연장' 오독).
#    '손익분기'·'본전'·'역전' 금지(copywriter). SM1 그대로.
BW = '당긴 이득 끝나는 나이'
assert re.search(r'5년 당김 월 700,000원', calc) and re.search(r'1년 당김 월 940,000원', calc)
M5, M1 = '월 70만', '월 94만'
_arrow = "<div class='lab' style='left:462px;top:{:.0f}px;font-size:60px;color:#fff'>→</div>".format(300 + 220 * 0.33)
_vs = "<div class='t' style='left:452px;top:{:.0f}px;font-size:60px;color:#9FB0D0'>vs</div>".format(300 + 220 * 0.30)
_sm0 = "<div class='lab' style='left:330px;top:40px;font-size:52px;color:#fff'>" + SM0 + "</div>"
_g = p1cake('#0F3A33', '#0B2C27'); assert _arrow in _g and _sm0 in _g
p1q = _g.replace(_arrow, _vs).replace(_sm0, f"<div class='t' style='left:330px;top:26px;font-size:74px;color:#fff'>{BW}</div>")
p1q = p1q.replace(f"<div class='fine'", f"<div class='t' style='left:150px;top:{483 + 18}px;width:240px;text-align:center;font-size:62px;color:#2B3A57'>{M5}</div>"
                  f"<div class='t' style='left:535px;top:{498 + 30}px;width:400px;text-align:center;font-size:84px;color:#B3201C'>{M1}</div>\n<div class='fine'", 1)
VARIANTS['p1q'] = p1q
# p1r = p1q에서 머리 두 줄: 1줄 '국민연금' 작게(54px 노랑), 2줄 BW 크게(96px) — 168px에서 큰 말이 주인공. 케이크 아래로 조금 내림.
p1r = p1q.replace("<div class='t' style='left:44px;top:26px;font-size:74px;color:#FFD23F'>국민연금</div>",
                  "<div class='t' style='left:44px;top:18px;font-size:50px;color:#FFD23F'>국민연금</div>")
p1r = p1r.replace(f"<div class='t' style='left:330px;top:26px;font-size:74px;color:#fff'>{BW}</div>",
                  f"<div class='t' style='left:44px;top:72px;font-size:96px;color:#fff'>{BW}</div>")
p1r = p1r.replace("left:150px;top:170px;font-size:64px", "left:150px;top:196px;font-size:56px").replace("left:600px;top:140px;font-size:84px", "left:660px;top:180px;font-size:54px")
assert BW in p1r and '국민연금' in p1r
VARIANTS['p1r'] = p1r


# ── 11차(10/14 09:2x) — 10차 세 명: p1q 6.80(제미나이 8.1·Claude 6.5·레드팀 5.8)·p1r 6.82(7.75·6.8·5.9)·p1j 6.55. 케이크판 반려:
#    레드팀 경쟁 유사 3('vs' 대결·나이+월액 짝(경쟁 '60세 70만')·어두운 바탕 노랑/빨강), 케이크=80세 생일, '76세 → 월 70만' 받는다 오독.
#    처방(두 심사 공통): 케이크·vs·월액 빼고 p1j 눈금 끝점 구조로 + 큰 말 BW 머리 띠 + 짙은 바탕 + 눈금 65에 '제때' 기준 표시.
def p1dot(bg, ink5, ink1, rul, band):
    _r, X = ruler(60, 548, 880, col=rul, dy=48)
    return f"""<div style='position:absolute;inset:0;background:{bg}'></div>
<div class='t' style='left:48px;top:20px;font-size:54px;color:#FFD23F'>국민연금</div>
<div style='position:absolute;left:30px;top:92px;width:860px;height:112px;background:{band};border-radius:14px'></div>
<div class='t' style='left:56px;top:100px;font-size:88px;color:#fff'>{BW}</div>
<div class='t' style='left:52px;top:262px;font-size:58px;color:{ink5}'>5년 당김</div>
<div class='t' style='left:{X(A5) - 146:.0f}px;top:236px;font-size:100px;color:{ink5}'>{S5}</div>
<div style='position:absolute;left:{X(A5) - 4:.0f}px;top:342px;width:8px;height:182px;background:{ink5}'></div>
<div class='t' style='left:{X(A1) + 50:.0f}px;top:236px;font-size:60px;color:{ink1}'>1년 당김</div>
<div id='d1' class='t' data-fit='440' style='left:{X(A1) + 50:.0f}px;top:312px;font-size:150px;color:{ink1}'>{S1}</div>
{_r}
<div class='lab' style='left:{X(65) - 40:.0f}px;top:470px;width:80px;text-align:center;font-size:30px;color:{rul}'>제때</div>
<div style='position:absolute;left:{X(A5) - 30:.0f}px;top:518px;width:60px;height:60px;border-radius:50%;background:{ink5}'></div>
<div style='position:absolute;left:{X(A1) - 38:.0f}px;top:510px;width:76px;height:76px;border-radius:50%;background:{ink1}'></div>
<svg style='position:absolute;left:0;top:0' width='1280' height='720'><line x1='{X(A1) + 24:.0f}' y1='518' x2='{X(A1) + 70:.0f}' y2='446' stroke='{ink1}' stroke-width='9' stroke-linecap='round'/></svg>
<div class='fine' style='color:{rul};top:640px;left:60px;font-size:32px'>제때(65세) 받은 사람 기준 · {SM1}</div>
"""
VARIANTS['p1s'] = p1dot('#0F3A33', '#B9C8E6', '#FF5A4E', '#A9BDB6', '#0A2823')   # 짙은 초록
VARIANTS['p1t'] = p1dot('#14203A', '#B9C8E6', '#FF5A4E', '#A9B4C8', '#0B1428')   # 짙은 남색


# ── 12차 — 11차 세 명: p1s 6.88(제미나이 6.75·Claude 6.8·레드팀 7.1)·p1t 6.82(남색, 경쟁 유사 3 반려)·p1j 6.30.
#    처방: ① 머리 띠가 바탕과 같아 168px에서 사라짐 → 띠 밝게 ② 76.7 옅은 하늘색 → 흰색 ③ '5년 당김'을 76.7 바로 위로 ④ 노랑 '국민연금' → 흰(경쟁 노랑 글자 유사 빼기)
#    ⑤ '제때'를 눈금 65 바로 위에 붙임.
def p1dot2(band, bandink):
    h = p1dot('#0F3A33', '#FFFFFF', '#FF5A4E', '#A9BDB6', band)
    _r, X = ruler(60, 548, 880, col='#A9BDB6', dy=48)
    h = h.replace("<div class='t' style='left:48px;top:20px;font-size:54px;color:#FFD23F'>국민연금</div>", "<div class='t' style='left:48px;top:14px;font-size:50px;color:#DDE7E3'>국민연금</div>")
    h = h.replace("left:30px;top:92px;width:860px;height:112px", "left:30px;top:80px;width:840px;height:108px")
    h = h.replace(f"<div class='t' style='left:56px;top:100px;font-size:88px;color:#fff'>{BW}</div>", f"<div class='t' style='left:54px;top:86px;font-size:86px;color:{bandink}'>{BW}</div>")
    h = h.replace("<div class='t' style='left:52px;top:262px;font-size:58px;color:#FFFFFF'>5년 당김</div>",
                  f"<div class='t' style='left:{X(A5) - 150:.0f}px;top:206px;width:300px;text-align:center;font-size:50px;color:#DDE7E3'>5년 당김</div>")
    h = h.replace(f"left:{X(A5) - 146:.0f}px;top:236px;font-size:100px", f"left:{X(A5) - 160:.0f}px;top:262px;font-size:104px")
    h = h.replace(f"left:{X(A5) - 4:.0f}px;top:342px;width:8px;height:182px", f"left:{X(A5) - 4:.0f}px;top:372px;width:8px;height:152px")
    h = h.replace(f"left:{X(65) - 40:.0f}px;top:470px", f"left:{X(65) - 10:.0f}px;top:496px")
    assert '5년 당김' in h and h.count(BW) == 1
    return h
VARIANTS['p1u'] = p1dot2('#2F8C74', '#FFFFFF')   # 밝은 초록 띠 + 흰 글자
VARIANTS['p1v'] = p1dot2('#F2EEE6', '#0F3A33')   # 크림 띠 + 짙은 초록 글자


if __name__ == '__main__':
    print('숫자', S5, S1)
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
