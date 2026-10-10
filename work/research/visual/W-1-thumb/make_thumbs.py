# W-1 '이번 주 영수증' 1화 썸네일 시안 (2026-10-10 visual-designer, today.md [지시] 기한 10/10 14:00) — py -3.12 make_thumbs.py [w1a,w1b,...]
# 문구: ep/W-1/meta.json thumb_text '107조(잠정) 공시한 사흘, 내 100주는?'(copy/titles.md 1위, 10/10 01:50 오독 시험 0/3 → 그대로).
#   제목 = 결과 숫자(−5.07%·−140만원·44번치) / 썸네일 = 뉴스 이름 + 내 돈 질문 → 썸네일에 결과 숫자 안 씀(숫자 겹침 0).
# 숫자: ep/W-1/calc_out.txt [A1] 107.4 → '107조' assert. 레드팀(copywriter 01:50) '107조가 무엇인지 없으면 손실로 읽힘' → '삼성전자 영업이익' 꼬리표를 큰 숫자 바로 위에(E-2 교훈: 지표 이름은 숫자 위 같은 크기급).
# 경쟁 5(compete.md): 검은 바탕·캔들 차트·앵커 얼굴·아래 두 줄 흰+빨강 굵은 글씨·시세판. 우리: 밝은 판, 얼굴·캔들·시세판 0, 아래 두 줄 공식 안 씀.
# 가려짐: 오른쪽 아래 x≥960·y≥576, 아래 5%(y≥684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.abspath(os.path.join(HERE, '..', '..', 'longform', 'ep', 'W-1'))
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
meta = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))
OP = float(re.search(r'\[A1\][^=]*= ([\d.]+)', calc).group(1))
assert int(OP) == 107, OP
assert meta['thumb_text'] == '107조(잠정) 공시까지 사흘, 내 100주 −140만', meta['thumb_text']  # copywriter 10/10 2차 오독 시험(copy/titles.md 끝)
assert re.search(r'\[C3\] 10/8 종가\(실적 발표일\)', calc)

INK, RED, BLUE, GREY = '#16181D', '#E03A2F', '#1F5BD8', '#6B7280'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
FINE = '삼성전자 3분기 잠정실적 공시(10/8) · 종가 10/2→10/8 · 투자 권유 아님'

# w1a — 밝은 판, 위 '삼성전자 영업이익 / 107조(잠정)' 빨강 ▲, 아래 '공시한 사흘, 내 100주는?' 파랑 ▼ (반전: 회사 숫자 위로, 내 돈 아래로)
w1a = f"""<div style='position:absolute;inset:0;background:#F5F2EB'></div>
<div class='t' style='left:56px;top:40px;font-size:84px;color:{INK}'>삼성전자 영업이익</div>
<div id='a1' class='t' style='left:44px;top:140px;font-size:250px;color:{RED};letter-spacing:-6px'>107조<span style='font-size:72px;letter-spacing:0'> (잠정)</span></div>
<div class='t' style='left:900px;top:120px;font-size:200px;color:{RED}'>▲</div>
<div class='t' style='left:56px;top:418px;font-size:84px;color:{INK}'>공시한 사흘,</div>
<div id='a2' class='t' data-fit='880' style='left:52px;top:508px;font-size:118px;color:{BLUE}'>내 100주는? ▼</div>
<div class='fine' style='color:{GREY};top:650px;font-size:20px'>{FINE}</div>
"""

# w1b — 밝은 하늘 판 + 흰 '평가액 카드'(브랜드 흉내 없음), 값은 실제 자릿수로 가림(R-1 교훈: +???만 → 8·8)
w1b = f"""<div style='position:absolute;inset:0;background:#E8EEF8'></div>
<div class='t' style='left:52px;top:36px;font-size:70px;color:{GREY}'>삼성전자 영업이익</div>
<div class='t' style='left:46px;top:116px;font-size:150px;color:{RED};letter-spacing:-4px'>107조<span style='font-size:64px'> (잠정)</span></div>
<div class='t' style='left:52px;top:276px;font-size:70px;color:{INK}'>공시한 사흘,</div>
<div style='position:absolute;left:40px;top:368px;width:900px;height:200px;background:#fff;border-radius:28px;box-shadow:0 8px 0 #C9D3E6'></div>
<div class='t' style='left:80px;top:404px;font-size:120px;color:{INK}'>내 100주</div>
<div class='lab' style='left:84px;top:526px;font-size:32px;color:{GREY}'>평가액 10/2→10/8</div>
<div id='b1' class='t' style='left:560px;top:404px;font-size:120px;color:{BLUE}'>−???만</div>
<div class='fine' style='color:{GREY};top:650px;font-size:20px'>{FINE}</div>
"""

# w1c — 좌우 두 판(왼쪽 회사·따뜻한 면 / 오른쪽 내 돈·찬 면), 문구를 쉼표에서 둘로 나눔. 'vs' 글자 없음(C-1 교훈: vs는 경쟁 겹침 +1)
w1c = f"""<div style='position:absolute;left:0;top:0;width:640px;height:720px;background:#FBEDE9'></div>
<div style='position:absolute;left:640px;top:0;width:640px;height:720px;background:#E6EEFB'></div>
<div class='t' style='left:48px;top:48px;font-size:80px;color:{INK}'>삼성전자</div>
<div class='t' style='left:48px;top:140px;font-size:80px;color:{INK}'>영업이익</div>
<div id='c1' class='t' data-fit='560' style='left:36px;top:236px;font-size:200px;color:{RED};letter-spacing:-6px'>107조▲</div>
<div class='t' style='left:48px;top:446px;font-size:64px;color:{RED}'>(잠정) 공시한 사흘</div>
<div class='t' style='left:684px;top:60px;font-size:84px;color:{INK}'>내 100주는</div>
<div class='t' style='left:740px;top:170px;font-size:340px;color:{BLUE}'>?▼</div>
<div class='fine' style='color:{GREY};top:650px;font-size:20px'>{FINE}</div>
"""
VARIANTS = {'w1a': w1a, 'w1b': w1b, 'w1c': w1c}

# ── 2차 — 1차 세 명 평균 w1b 7.82(제미나이 3.1-lite 8·8.5 / Claude 7.6 / 레드팀 7.6) · w1a 7.08(7·7.5/7.0/7.0) · w1c 6.27(6·6.5/6.3/6.3, 레드팀 '(잠정)' 떨어짐 규칙 위반).
#    공통 처방(w1b): 회색 윗줄 '삼성전자 영업이익' 168px에서 사라짐 → 먹색 · '평가액 10/2→10/8'을 키움(레드팀: '공시한 사흘'이 공시 뒤 사흘로 읽히는 오독·확정 손실 오독을 같이 막음)
#    · '−'가 BH 글꼴에서 줄표(—)로 보임 → 굵은 PD 마이너스 · 카드 키움. 문구·숫자 변경 0.
w1d = f"""<div style='position:absolute;inset:0;background:#E8EEF8'></div>
<div class='t' style='left:52px;top:34px;font-size:76px;color:{INK}'>삼성전자 영업이익</div>
<div class='t' style='left:46px;top:120px;font-size:156px;color:{RED};letter-spacing:-4px'>107조<span style='font-size:66px;letter-spacing:0'> (잠정)</span></div>
<div class='t' style='left:52px;top:286px;font-size:72px;color:{INK}'>공시한 사흘,</div>
<div style='position:absolute;left:36px;top:378px;width:910px;height:226px;background:#fff;border-radius:28px;box-shadow:0 8px 0 #C9D3E6'></div>
<div class='t' style='left:76px;top:404px;font-size:124px;color:{INK}'>내 100주</div>
<div class='t' style='left:80px;top:538px;font-size:46px;color:{GREY}'>평가액 10/2→10/8</div>
<div id='d1' class='t' style='left:560px;top:404px;font-size:124px;color:{BLUE}'><span style='font-family:PD;font-weight:700'>-</span>???만</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE}</div>
"""
VARIANTS['w1d'] = w1d

# ── 3차 — 2차(새 심사관) w1d 6.95(제미나이 7.5·6 / Claude 6.9 / 레드팀 7.2) · w1b 6.45 · w1a 6.62(레드팀·Claude 겹침 3 반려: ▼ 시세판 문법).
#    처방: '3분기'를 윗줄에(레드팀 — 연간·손실 오독) · 168px에서 옅은 판이 빛바램 → 카드를 진한 남색·글자 흰색(Claude) · 마이너스는 U+2212를 PD 굵게.
#    w1f = 카피 원문 '내 100주는?' 그대로 + 가린 값은 둘째 줄(레드팀: '−???만'은 확정 문구 변경이라 카피 승인 필요).
NAVY = '#14264A'
def top3():
    return f"""<div style='position:absolute;inset:0;background:#E8EEF8'></div>
<div class='t' style='left:52px;top:34px;font-size:76px;color:{INK}'>삼성전자 3분기 영업이익</div>
<div class='t' style='left:46px;top:120px;font-size:156px;color:{RED};letter-spacing:-4px'>107조<span style='font-size:66px;letter-spacing:0'> (잠정)</span></div>
<div class='t' style='left:52px;top:286px;font-size:72px;color:{INK}'>공시까지 사흘,</div>
<div style='position:absolute;left:36px;top:378px;width:910px;height:236px;background:{NAVY};border-radius:28px'></div>"""
MINUS = "<span style='font-family:PD;font-weight:700'>−</span>"
w1e = top3() + f"""
<div class='t' style='left:76px;top:404px;font-size:124px;color:#fff'>내 100주</div>
<div class='t' style='left:80px;top:540px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div id='e1' class='t' style='left:560px;top:404px;font-size:124px;color:#7FB0FF'>{MINUS}???만</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE}</div>
"""
w1f = top3() + f"""
<div class='t' style='left:76px;top:400px;font-size:132px;color:#fff'>내 100주는?</div>
<div class='t' style='left:80px;top:546px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8 <span style='color:#7FB0FF'>{MINUS}???만원</span></div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE}</div>
"""
VARIANTS.update(w1e=w1e, w1f=w1f)

# ── 4차 — 3차(새 심사관) w1e 6.88(제미나이 7·7.5 / Claude 6.6 / 레드팀 6.8) · w1f 6.07(겹침 3) · w1d 6.33. 형식 바꿈(교본: 2차수 안 오르면 다듬지 말고 형식).
#    공통 지적: 오른쪽 40% 빈칸 → '발표 자료 한 장' · 레드팀 사실: 공시(10/8)는 사흘 중 마지막 날, −5.07% 중 −2.72%는 공시 전 → '공시 뒤 사흘 하락'으로 오독.
#    처방: 오른쪽에 실제 종가 3점 선(calc_out C1·C2·C3, 거래일 간격) + 10/8 점에만 '공시' 꼬리표 → 공시 전부터 내린 게 그림으로 보임. 각주 '거래일 사흘'.
C = [int(re.search(rf'\[{k}\][^=]*= (\d+)', calc).group(1)) for k in ('C1', 'C2', 'C3')]
assert C == [276000, 268500, 262000] and round((C[2] / C[0] - 1) * 100, 2) == -5.07, C
FINE4 = '삼성전자 3분기 잠정실적 공시 10/8 · 종가 10/2·10/7·10/8(거래일 사흘) · 투자 권유 아님'
def strip(x0=1000, x1=1220, y0=120, y1=400, lo=255000, hi=280000):
    """실제 종가 3점 선. 세로축 25.5만~28만(눈금 글자 없이 끝값만 표기)."""
    pts = [(x0 + (x1 - x0) * i / 2, y0 + (y1 - y0) * (hi - v) / (hi - lo)) for i, v in enumerate(C)]
    P = ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    s = (f"<div style='position:absolute;left:968px;top:30px;width:288px;height:520px;background:#fff;border-radius:24px'></div>"
         f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='{P}' fill='none' stroke='{BLUE}' stroke-width='14' stroke-linejoin='round' stroke-linecap='round'/>")
    for i, (x, y) in enumerate(pts):
        s += f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{22 if i == 2 else 14}' fill='{RED if i == 2 else BLUE}' stroke='#fff' stroke-width='6'/>"
    s += '</svg>'
    s += f"<div class='t' style='left:990px;top:{pts[0][1] - 76:.0f}px;font-size:48px;color:{INK}'>10/2</div>"
    s += f"<div class='t' style='left:1080px;top:{pts[2][1] + 34:.0f}px;font-size:48px;color:{RED}'>10/8</div>"
    s += f"<div class='t' style='left:1104px;top:{pts[2][1] + 90:.0f}px;font-size:48px;color:{RED}'>공시</div>"
    return s
w1g = top3() + strip() + f"""
<div class='t' style='left:76px;top:404px;font-size:124px;color:#fff'>내 100주</div>
<div class='t' style='left:80px;top:540px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div id='g1' class='t' style='left:556px;top:404px;font-size:124px;color:#7FB0FF'>{MINUS}???만</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE4}</div>
"""
VARIANTS['w1g'] = w1g

# ── 5차 — 4차(새 심사관) w1g 7.10(제미나이 7.5·7.5 / Claude 6.6 / 레드팀 7.2) · w1e 6.70 · w1b 6.20.
#    레드팀 사실: 10/5 대체공휴일 → 거래일 사흘 = 10/6·10/7·10/8, 종가 4점(10/2 기준)인데 w1g는 10/6을 빼고 같은 간격 → 틀림. 세로축 25.5만~28만은 −5.07%를 높이 56%로 과장.
#    Claude: 빨간 끝점 원 = 경쟁 2·3 '차트 끝 원' 문법(겹침 3 반려).
#    고침: 10/6 종가는 calc.py와 같은 원자료(w1009/raw/yh_005930.KS.json, 야후 종가)에서 읽고 C1~C3과 assert, 숫자 글자로는 안 씀(점만).
#    점 4개 거래일 같은 간격 · 끝점 원 없음 · 10/8 자리에 '공시' 세로 띠 · 세로축 24만~28만(−5.07% = 높이 35%) + 양 끝값 27.6만·26.2만(C1·C3) · 각주 '거래일 10/6·10/7·10/8'.
import datetime as _dt
_j = json.load(open(os.path.join(EP, 'w1009', 'raw', 'yh_005930.KS.json'), encoding='utf-8'))['chart']['result'][0]
_s = {_dt.datetime.fromtimestamp(t + _j['meta']['gmtoffset'], _dt.UTC).strftime('%Y-%m-%d'): v for t, v in zip(_j['timestamp'], _j['indicators']['quote'][0]['close']) if v}
DAYS = ['2026-10-02', '2026-10-06', '2026-10-07', '2026-10-08']
assert [d for d in sorted(_s) if '2026-10-02' <= d <= '2026-10-08'] == DAYS, sorted(_s)[-6:]
C4 = [int(_s[d]) for d in DAYS]
assert [C4[0], C4[2], C4[3]] == C, (C4, C)
FINE5 = '삼성전자 3분기 잠정실적 공시 10/8 · 종가 10/2→10/8(거래일 10/6·10/7·10/8) · 투자 권유 아님'
def strip5(x0=1010, x1=1214, y0=150, y1=470, lo=240000, hi=280000):
    pts = [(x0 + (x1 - x0) * i / 3, y0 + (y1 - y0) * (hi - v) / (hi - lo)) for i, v in enumerate(C4)]
    P = ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    s = (f"<div style='position:absolute;left:968px;top:30px;width:288px;height:520px;background:#fff;border-radius:24px'></div>"
         f"<div style='position:absolute;left:{pts[3][0] - 26:.0f}px;top:44px;width:52px;height:440px;background:#FBE3E0;border-radius:14px'></div>"
         f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='{P}' fill='none' stroke='{BLUE}' stroke-width='14' stroke-linejoin='round' stroke-linecap='round'/></svg>"
         f"<div class='t' style='left:{pts[3][0] - 50:.0f}px;top:488px;font-size:50px;color:{RED}'>공시</div>"
         f"<div class='t' style='left:986px;top:{pts[0][1] - 66:.0f}px;font-size:46px;color:{INK}'>27.6만</div>"
         f"<div class='t' style='left:1060px;top:{pts[3][1] + 22:.0f}px;font-size:46px;color:{BLUE}'>26.2만</div>")
    return s
assert f'{C[0] / 10000:.1f}만' == '27.6만' and f'{C[2] / 10000:.1f}만' == '26.2만'
w1h = top3() + strip5() + f"""
<div class='t' style='left:76px;top:404px;font-size:124px;color:#fff'>내 100주</div>
<div class='t' style='left:80px;top:540px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div id='h1' class='t' style='left:556px;top:404px;font-size:124px;color:#7FB0FF'>{MINUS}???만</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE5}</div>
"""
VARIANTS['w1h'] = w1h

# ── 6차 — 5차(새 심사관) w1h 7.08(제미나이 7.5·7 / Claude 6.8 / 레드팀 7.2, 사실 대조 전부 맞음) · w1g 6.73(사실 틀림 반려) · w1e 6.38.
#    레드팀: '공시' 세로 띠 = 경쟁 3·4 '차트 끝 빨간 세로선' 문법 → 겹침 3 반려. Claude도 띠를 빼라. 둘 다: 선 칸 키워 168px에서 27.6만→26.2만 읽히게.
#    w1i = 띠 없음, 10/8 점 아래 '공시' 글자만, 선 칸 세로로 좁혀 선 기울기 그대로·글자 크게.
#    w1j = w1i 그림 + 카드 문구는 카피 원문 '내 100주는?' 그대로(레드팀·Claude: '−???만'은 확정 문구 변경, 제목 −140만원이 답을 바로 줘 감춤 효과도 약함). 하락 방향은 오른쪽 선이 맡음(3차 w1f 실패 원인 = 방향 단서 없음).
def strip6(x0=1012, x1=1212, y0=130, y1=420, lo=240000, hi=280000):
    pts = [(x0 + (x1 - x0) * i / 3, y0 + (y1 - y0) * (hi - v) / (hi - lo)) for i, v in enumerate(C4)]
    P = ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    return (f"<div style='position:absolute;left:968px;top:30px;width:288px;height:520px;background:#fff;border-radius:24px'></div>"
            f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='{P}' fill='none' stroke='{BLUE}' stroke-width='16' stroke-linejoin='round' stroke-linecap='round'/></svg>"
            f"<div class='t' style='left:984px;top:{pts[0][1] - 76:.0f}px;font-size:56px;color:{INK}'>27.6만</div>"
            f"<div class='t' style='left:1030px;top:{pts[3][1] + 30:.0f}px;font-size:56px;color:{BLUE}'>26.2만</div>"
            f"<div class='t' style='left:1090px;top:{pts[3][1] + 96:.0f}px;font-size:56px;color:{RED}'>10/8</div>"
            f"<div class='t' style='left:1102px;top:{pts[3][1] + 160:.0f}px;font-size:56px;color:{RED}'>공시</div>")
w1i = top3() + strip6() + f"""
<div class='t' style='left:76px;top:404px;font-size:124px;color:#fff'>내 100주</div>
<div class='t' style='left:80px;top:540px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div id='i1' class='t' style='left:556px;top:404px;font-size:124px;color:#7FB0FF'>{MINUS}???만</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE5}</div>
"""
w1j = top3() + strip6() + f"""
<div class='t' style='left:76px;top:404px;font-size:140px;color:#fff'>내 100주는?</div>
<div class='t' style='left:80px;top:548px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE5}</div>
"""
VARIANTS.update(w1i=w1i, w1j=w1j)

# ── 7차 — 6차(새 심사관) w1i 6.97(제미나이 7.5·7.5 / Claude 6.8 / 레드팀 6.6, 레드팀 겹침 3 반려: '−???' = 경쟁 '−5% 폭락..?') · w1j 6.72(6.5·7 / 6.3 / 7.1, 레드팀 겹침 2) · w1h 6.37.
#    레드팀 처방(w1j): 선에 점 4개를 실제로 · 시작에 '10/2' · 세로축 넓혀 과장 줄이기(20만~28만) · 빨강은 상승색이라 '공시'를 빨강으로 쓰면 색 뜻이 섞임 → 먹색.
#    Claude 처방: 168px에서 선이 안 읽힘 → 굵게. 문구는 카피 원문 그대로('−???만'은 레드팀이 승인 말라고 권함).
def strip7(x0=1014, x1=1210, y0=170, y1=420, lo=220000, hi=280000):
    """세로축 22만~28만(−5.07% = 선 칸 높이 23%). 6차 레드팀 '24~28만은 과장' 반영, 20만~28만은 168px에서 평평해져 중간값."""
    pts = [(x0 + (x1 - x0) * i / 3, y0 + (y1 - y0) * (hi - v) / (hi - lo)) for i, v in enumerate(C4)]
    P = ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    s = (f"<div style='position:absolute;left:968px;top:30px;width:288px;height:520px;background:#fff;border-radius:24px'></div>"
         f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'><polyline points='{P}' fill='none' stroke='{BLUE}' stroke-width='20' stroke-linejoin='round' stroke-linecap='round'/>")
    for x, y in pts:
        s += f"<circle cx='{x:.0f}' cy='{y:.0f}' r='15' fill='{BLUE}' stroke='#fff' stroke-width='5'/>"
    s += '</svg>'
    s += (f"<div class='t' style='left:990px;top:56px;font-size:50px;color:{INK}'>10/2</div>"
          f"<div class='t' style='left:990px;top:{pts[0][1] - 66:.0f}px;font-size:50px;color:{INK}'>27.6만</div>"
          f"<div class='t' style='left:1056px;top:{pts[3][1] + 30:.0f}px;font-size:50px;color:{BLUE}'>26.2만</div>"
          f"<div class='t' style='left:1110px;top:{pts[3][1] + 86:.0f}px;font-size:50px;color:{INK}'>10/8</div>"
          f"<div class='t' style='left:1122px;top:{pts[3][1] + 142:.0f}px;font-size:50px;color:{INK}'>공시</div>")
    return s
w1k = top3() + strip7() + f"""
<div class='t' style='left:76px;top:404px;font-size:140px;color:#fff'>내 100주는?</div>
<div class='t' style='left:80px;top:548px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE5}</div>
"""
VARIANTS['w1k'] = w1k


# ── copywriter 10/10 2차 오독 시험(ep/W-1/copy/titles.md 끝) — top3 셋째 줄 '공시한 사흘,'→'공시까지 사흘,'(공시 원인 오독 줄임) · 카드 '−???만'은 낚시로 읽혀 불승인.
#    w1l = w1i 그림 + 카드 '내 100주 −140만'(calc_out C8, 감춤 없음) · w1m = w1k 그림 + 새 셋째 줄(예비). w1a~w1k png는 옛 문구 — 다시 렌더하지 말 것(top3가 바뀌어 덮어씀).
C8 = int(re.search(r'\[C8\][^=]*= (-?\d+)', calc).group(1)); assert C8 == -1400000, C8
w1l = top3() + strip6() + f"""
<div class='t' style='left:72px;top:410px;font-size:112px;color:#fff'>내 100주</div>
<div class='t' style='left:80px;top:540px;font-size:50px;color:#C9D3E6'>평가액 10/2→10/8</div>
<div id='l1' class='t' style='left:500px;top:410px;font-size:112px;color:#7FB0FF'>{MINUS}{-C8 // 10000}만</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>{FINE5}</div>
"""
VARIANTS.update(w1l=w1l, w1m=w1k)


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


def peek(keys, out):
    """시안 640px + 168px 실제 크기를 한 장에(눈 검사용)."""
    bd = Image.new('RGB', (640 * len(keys), 470), 'white')
    for i, k in enumerate(keys):
        bd.paste(Image.open(os.path.join(EP, f'thumb_{k}.png')).resize((640, 360), Image.LANCZOS), (i * 640, 0))
        bd.paste(Image.open(os.path.join(HERE, f'{k}_168.png')), (i * 640 + 10, 370))
    bd.save(out)


if __name__ == '__main__':
    print('영업이익', OP)
    ks = sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS)
    main(ks)
    if len(sys.argv) > 2: peek(ks, sys.argv[2])
