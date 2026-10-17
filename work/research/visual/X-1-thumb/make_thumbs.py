# X-1 '환율이 내린 석 달 — S&P500은 올랐는데 원화 계좌는 빠졌다' 썸네일 시안(2026-10-17 visual-designer)
# 문구: ep/X-1/copy/titles.md '10-15 18:58 이해 시험 반영' 절(작은 줄·swap 작은 줄)과 '쓸 것' 줄(큰 글·swap 큰 글) — 파일에서 읽어 assert.
# 숫자: ep/X-1/calc_out.txt §2 SPY(끝날 2026-10-15) — 1년 전 2025-10-13 원화 +9.69% · 2026-07-02 달러 +3.63%·원화 -10.76%. 파일에서 읽어 assert, 정수 반올림.
#   ※ titles.md 문구('+10% vs −10%'·'주가는 +4% / 내 1억은 −10%')는 옛 계산(끝날 10/12, 7/2 원화 −10.07%) 기준.
#     v3 계산(−10.76%)을 반올림하면 −11%라 숫자만 바꿔 씀(사실 고침, 말은 그대로).
#   facts.txt F1: 2026-07-02 1,554.4 = 2024년 이후 최고 → swap 작은 줄 '2024년 이후 달러가 가장 비싸던 7월 2일' assert.
# 그림: 경쟁 5장 공통 문법(어두운 판·노랑/흰 글자·인물·빨강↑파랑↓ 선) 피함. 좌우 카드 두 칸 금지. 밝은 판 + 잉크 + 주황 1색.
#   x1a 0을 가운데 둔 위아래 막대 · x1b 큰 줄 + 산 날 시간 띠 · x1c(swap) 1억 = 1천만원 칸 10개, 빠진 만큼 빈 칸
# 가려짐: 오른쪽 아래 x>960·y>576, 아래 5%(y>684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, json, sys, re, datetime
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'X-1')

# ── 문구(titles.md)
tt = open(os.path.join(EP, 'copy', 'titles.md'), encoding='utf-8').read()
last = tt.split('## 2026-10-15 18:58 이해 시험 반영')[1]
assert "thumb_text: **'같은 S&P500 / +10% vs −10%'**" in tt
assert "thumb_text_swap: '주가는 +4% / 내 1억은 −10%'" in tt
SMALL = re.search(r"thumb_text_small: '([^']+)'", last).group(1)
SWAP_SMALL = re.search(r"thumb_text_swap_small: \*\*'([^']+)'\*\*", last).group(1)
assert SMALL == '작년 이맘때 산 1억 vs 7월 초 산 1억 · 원화로 따지면', SMALL
assert SWAP_SMALL == '2024년 이후 달러가 가장 비싸던 7월 2일에 산 경우', SWAP_SMALL
S_A, S_B, S_C = [s.strip() for s in re.split(r' vs | · ', SMALL)]   # 작년 이맘때 산 1억 / 7월 초 산 1억 / 원화로 따지면

# ── 숫자(calc_out.txt §2 SPY, facts F1)
cal = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
assert '끝날 2026-10-15' in cal.splitlines()[0]
m1 = re.search(r'1년 전 2025-10-13 SPY: 달러 ([+-][\d.]+)% · 환율 [+-][\d.]+% · 원화 ([+-][\d.]+)%', cal)
m2 = re.search(r'환율 최고점 2026-07-02 SPY: 달러 ([+-][\d.]+)% · 환율 [+-][\d.]+% · 원화 ([+-][\d.]+)%', cal)
YR_KRW, JUL_USD, JUL_KRW = float(m1.group(2)), float(m2.group(1)), float(m2.group(2))
assert (YR_KRW, JUL_USD, JUL_KRW) == (9.69, 3.63, -10.76), (YR_KRW, JUL_USD, JUL_KRW)
fa = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
assert '2026-07-02 1,554.4(2024년 이후 최고)' in fa
MINUS = '−'


def pct(v):
    return ('+' if v > 0 else MINUS) + str(round(abs(v))) + '%'


P_YR, P_JUL, P_STK = pct(YR_KRW), pct(JUL_KRW), pct(JUL_USD)
assert (P_YR, P_JUL, P_STK) == ('+10%', MINUS + '11%', '+4%')
BIG1, BIG2 = '같은 S&P500', f'{P_YR} vs {P_JUL}'
SW1, SW2 = f'주가는 {P_STK}', f'내 1억은 {P_JUL}'
print('큰 글', BIG1, '/', BIG2, '· swap', SW1, '/', SW2)

INK, OR, PAPER, GREY, MUTE = '#18191D', '#FF5A00', '#F6F7F9', '#C9CDD4', '#6B7180'
FINE = 'SPY 가격 · 끝 2026.10.15 · 한국은행 환율'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
VARIANTS = {}


def x1a():
    # 0 줄 x=660. 1%=24px. 위: 작년 이맘때(오른쪽으로 +), 아래: 7월 초(왼쪽으로 −). 'S&P500'은 PD 700(BH의 5가 s로 보임 — H-2 배운 것).
    Z, K = 660, 24
    w1, w2 = round(YR_KRW * K), round(-JUL_KRW * K)
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:42px;top:14px;font-size:104px;color:{INK};letter-spacing:-3px'>{BIG1}</div>
<div class='lab' style='left:700px;top:50px;font-size:52px;color:{MUTE}'>{S_C}</div>
<div style='position:absolute;left:{Z - 3}px;top:150px;width:6px;height:430px;background:{INK}'></div>
<div class='lab' style='left:0;width:{Z - 22}px;text-align:right;top:160px;font-size:74px;color:{INK};letter-spacing:-2px'>{S_A}</div>
<div style='position:absolute;left:{Z}px;top:262px;width:{w1}px;height:100px;background:{INK};border-radius:0 12px 12px 0'></div>
<div class='t' style='left:{Z + w1 + 20}px;top:250px;font-size:128px;color:{INK}'>{P_YR}</div>
<div class='lab' style='left:{Z + 22}px;top:378px;font-size:74px;color:{OR};letter-spacing:-2px'>{S_B}</div>
<div style='position:absolute;left:{Z - w2}px;top:476px;width:{w2}px;height:100px;background:{OR};border-radius:12px 0 0 12px'></div>
<div class='t' style='left:0;width:{Z - w2 - 18}px;text-align:right;top:464px;font-size:128px;color:{OR}'>{P_JUL}</div>
<div class='fine' style='left:46px;top:616px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


def x1b():
    # 큰 두 줄 + 아래 시간 띠: 산 날(2025-10-13·2026-07-02) → 끝날(2026-10-15).
    d0, d1 = datetime.date(2025, 9, 1), datetime.date(2026, 10, 31)
    X0, X1 = 60, 900
    X = lambda d: round(X0 + (X1 - X0) * (d - d0).days / (d1 - d0).days)
    a, b, e = X(datetime.date(2025, 10, 13)), X(datetime.date(2026, 7, 2)), X(datetime.date(2026, 10, 15))
    ticks = ''
    for y, mth, t in [(2025, 10, '25.10'), (2026, 1, ''), (2026, 4, ''), (2026, 7, '26.7'), (2026, 10, '26.10')]:
        x = X(datetime.date(y, mth, 1))
        ticks += f"<div style='position:absolute;left:{x - 2}px;top:552px;width:4px;height:18px;background:{MUTE}'></div>"
        if t: ticks += f"<div class='lab' style='left:{x - 40}px;width:80px;text-align:center;top:574px;font-size:26px;color:{MUTE}'>{t}</div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:42px;top:14px;font-size:100px;color:{INK};letter-spacing:-3px'>{BIG1}</div>
<div class='lab' style='left:680px;top:48px;font-size:52px;color:{MUTE}'>{S_C}</div>
<div id='b2' class='t' data-fit='1190' style='left:40px;top:142px;font-size:180px;color:{INK}'>{P_YR}<span style='font-size:92px;color:{MUTE}'> vs </span><span style='color:{OR}'>{P_JUL}</span></div>
<div style='position:absolute;left:{X0}px;top:558px;width:{X1 - X0}px;height:6px;background:{MUTE}'></div>{ticks}
<div class='lab' style='left:{a - 6}px;top:340px;font-size:64px;color:{INK};letter-spacing:-2px'>{S_A}</div>
<div style='position:absolute;left:{a}px;top:420px;width:{e - a}px;height:40px;border:7px solid {INK};border-bottom:none'></div>
<div class='lab' style='left:0;width:{b - 20}px;text-align:right;top:470px;font-size:64px;color:{OR};letter-spacing:-2px'>{S_B}</div>
<div style='position:absolute;left:{b}px;top:488px;width:{e - b}px;height:40px;border:7px solid {OR};border-bottom:none'></div>
<div style='position:absolute;left:{a - 14}px;top:547px;width:28px;height:28px;border-radius:50%;background:{INK}'></div>
<div style='position:absolute;left:{b - 14}px;top:547px;width:28px;height:28px;border-radius:50%;background:{OR}'></div>
<div class='fine' style='left:46px;top:622px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


def x1c():
    # swap: 1억 = 1천만원 칸 10개. 원화 −10.76% → 남은 8.924칸 채움, 빠진 1.076칸은 주황 점선 빈칸.
    left = 10 * (1 + JUL_KRW / 100)
    cw, gap, x0, y0, h = 84, 10, 44, 392, 104
    cells = ''
    for i in range(10):
        x = x0 + i * (cw + gap); fill = max(0.0, min(1.0, left - i))
        cells += f"<div style='position:absolute;left:{x}px;top:{y0}px;width:{cw}px;height:{h}px;border:4px dashed {OR};border-radius:8px'></div>"
        if fill > 0:
            rad = '8px' if fill == 1 else '8px 0 0 8px'
            cells += f"<div style='position:absolute;left:{x}px;top:{y0}px;width:{round(cw * fill)}px;height:{h}px;background:{INK};border-radius:{rad}'></div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:44px;top:34px;font-size:120px;color:{INK}'>{SW1}</div>
<div id='s2' class='t' data-fit='1190' style='left:40px;top:178px;font-size:170px;color:{INK}'>내 1억은 <span style='color:{OR}'>{P_JUL}</span></div>
{cells}
<div class='lab' style='left:46px;top:506px;font-size:30px;color:{MUTE}'>1칸 = 1천만원</div>
<div class='lab' style='left:44px;top:548px;font-size:44px;color:{INK}'>{SWAP_SMALL}</div>
<div class='fine' style='left:46px;top:622px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


VARIANTS['x1a'] = x1a()
VARIANTS['x1b'] = x1b()
VARIANTS['x1c'] = x1c()


# ── 2차(10/17) — 1차 x1c 7.08(제미나이 6.5·8 · Claude 7 · 레드팀 7 겹침 1), x1b 6.75(7.5·7 · 7 · 6), x1a 5.67(6·6 · 6 · 5).
#   공통: 168px에서 '7월 초 산 1억' 사라짐(x1b 시간 띠 글씨 46px), x1c '주가는 +4%'가 작아 −11%와 맞서지 않음·빈 칸이 점선이라 안 보임·작은 줄 안 읽힘.
# x1d: x1b 짜임 유지, 꼬리표를 숫자 바로 밑(시간 띠 점 위치와 같은 x)으로 66px, '원화로 따지면' 먹색 60px, 괄호선 뺌.
# x1e: x1c 짜임 유지, '주가는 +4%' 150px(둘째 줄과 같은 무게), 칸 높이 104→72 · 빈 칸 옅은 주황 면, 작은 줄 44→50px 칸 위로.
def x1d():
    d0, d1 = datetime.date(2025, 9, 1), datetime.date(2026, 10, 31)
    X0, X1 = 60, 900
    X = lambda d: round(X0 + (X1 - X0) * (d - d0).days / (d1 - d0).days)
    a, b, e = X(datetime.date(2025, 10, 13)), X(datetime.date(2026, 7, 2)), X(datetime.date(2026, 10, 15))
    ticks = ''
    for y, mth, t in [(2025, 10, '25.10'), (2026, 1, ''), (2026, 4, ''), (2026, 7, '26.7'), (2026, 10, '26.10')]:
        x = X(datetime.date(y, mth, 1))
        ticks += f"<div style='position:absolute;left:{x - 2}px;top:522px;width:4px;height:18px;background:{MUTE}'></div>"
        if t: ticks += f"<div class='lab' style='left:{x - 40}px;width:80px;text-align:center;top:546px;font-size:26px;color:{MUTE}'>{t}</div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:42px;top:14px;font-size:100px;color:{INK};letter-spacing:-3px'>{BIG1}</div>
<div class='lab' style='left:676px;top:44px;font-size:62px;color:{INK}'>{S_C}</div>
<div class='t' style='left:{a - 100}px;top:150px;font-size:186px;color:{INK}'>{P_YR}</div>
<div class='t' style='left:{a + 400}px;top:214px;font-size:76px;color:{MUTE}'>vs</div>
<div class='t' style='left:{b - 6}px;top:150px;font-size:186px;color:{OR}'>{P_JUL}</div>
<div class='lab' style='left:{a - 100}px;top:356px;font-size:66px;color:{INK};letter-spacing:-2px'>{S_A}</div>
<div class='lab' style='left:{b - 6}px;top:356px;font-size:66px;color:{OR};letter-spacing:-2px'>{S_B}</div>
<div style='position:absolute;left:{X0}px;top:528px;width:{X1 - X0}px;height:6px;background:{MUTE}'></div>{ticks}
<div style='position:absolute;left:{a - 3}px;top:448px;width:6px;height:80px;background:{INK}'></div>
<div style='position:absolute;left:{b - 3}px;top:448px;width:6px;height:80px;background:{OR}'></div>
<div style='position:absolute;left:{a - 16}px;top:515px;width:32px;height:32px;border-radius:50%;background:{INK}'></div>
<div style='position:absolute;left:{b - 16}px;top:515px;width:32px;height:32px;border-radius:50%;background:{OR}'></div>
<div class='fine' style='left:46px;top:610px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


def x1e():
    left = 10 * (1 + JUL_KRW / 100)
    cw, gap, x0, y0, h = 84, 10, 44, 448, 72
    cells = ''
    for i in range(10):
        x = x0 + i * (cw + gap); fill = max(0.0, min(1.0, left - i))
        cells += f"<div style='position:absolute;left:{x}px;top:{y0}px;width:{cw}px;height:{h}px;background:#FFD9C2;border:4px solid {OR};border-radius:8px'></div>"
        if fill > 0:
            rad = '8px' if fill == 1 else '8px 0 0 8px'
            cells += f"<div style='position:absolute;left:{x}px;top:{y0}px;width:{round(cw * fill)}px;height:{h}px;background:{INK};border-radius:{rad}'></div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:44px;top:30px;font-size:150px;color:{INK}'>{SW1}</div>
<div id='s2' class='t' data-fit='1190' style='left:40px;top:190px;font-size:150px;color:{INK}'>내 1억은 <span style='color:{OR}'>{P_JUL}</span></div>
<div class='lab' style='left:44px;top:368px;font-size:50px;color:{INK};letter-spacing:-1px'>{SWAP_SMALL}</div>
{cells}
<div class='lab' style='left:46px;top:530px;font-size:30px;color:{MUTE}'>1칸 = 1천만원</div>
<div class='fine' style='left:46px;top:610px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


VARIANTS['x1d'] = x1d()
VARIANTS['x1e'] = x1e()


# ── 3차(10/17) — 2차 x1d 7.25(제미나이 8·7.5 · Claude 7 · 레드팀 7 겹침 2), x1c 6.58(7·8.5 · 6 · 6), x1e 6.50(6·7 · 6 · 7).
#   Claude·레드팀 둘 다: 시간 띠는 168px에서 안 읽힘 → 지우고 그 높이를 숫자·꼬리표 키우는 데. '같은 S&P500' 1.4배. x1e: 칸이 작아 빈 칸 안 보임, 작은 줄 키움.
#   Claude의 '어두운 판' 처방은 안 따름(H-2 배운 것: 어두운 판 = 경쟁 문법 겹침 3, 레드팀 반려).
# x1f: x1d에서 시간 띠 뺌. 숫자 196px 두 덩이가 폭 95%, 꼬리표 72px를 각 숫자 밑, 맨 위 '같은 S&P500' 132px + '원화로 따지면' 먹색 64px.
# x1g: x1e에서 칸 높이 72→112·테두리 6px, 작은 줄 50→56px('7월 2일'만 주황).
def x1f():
    col = lambda num, lab, c: (f"<div style='display:flex;flex-direction:column;align-items:flex-start'>"
                               f"<div style='font:196px/1 BH;color:{c}'>{num}</div>"
                               f"<div style='font:700 72px/1 PD;color:{c};letter-spacing:-3px;margin-top:24px;white-space:nowrap'>{lab}</div></div>")
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='lab' style='left:40px;top:12px;font-size:132px;color:{INK};letter-spacing:-4px'>{BIG1}</div>
<div class='lab' style='left:790px;top:64px;font-size:64px;color:{INK}'>{S_C}</div>
<div id='row' style='position:absolute;left:34px;top:224px;display:flex;align-items:flex-start;gap:14px;white-space:nowrap'>
{col(P_YR, S_A, INK)}<div style='font:70px/1 BH;color:{MUTE};margin-top:86px'>vs</div>{col(P_JUL, S_B, OR)}</div>
<div class='fine' style='left:46px;top:616px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


def x1g():
    left = 10 * (1 + JUL_KRW / 100)
    cw, gap, x0, y0, h = 84, 10, 44, 424, 112
    cells = ''
    for i in range(10):
        x = x0 + i * (cw + gap); fill = max(0.0, min(1.0, left - i))
        cells += f"<div style='position:absolute;left:{x}px;top:{y0}px;width:{cw}px;height:{h}px;background:#FFD9C2;border:6px solid {OR};border-radius:8px'></div>"
        if fill > 0:
            rad = '8px' if fill == 1 else '8px 0 0 8px'
            cells += f"<div style='position:absolute;left:{x}px;top:{y0}px;width:{round(cw * fill)}px;height:{h}px;background:{INK};border-radius:{rad}'></div>"
    sm = SWAP_SMALL.replace('7월 2일', f"<span style='color:{OR}'>7월 2일</span>")
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:44px;top:24px;font-size:146px;color:{INK}'>{SW1}</div>
<div id='s2' class='t' data-fit='1190' style='left:40px;top:180px;font-size:150px;color:{INK}'>내 1억은 <span style='color:{OR}'>{P_JUL}</span></div>
<div class='lab' style='left:44px;top:344px;font-size:56px;color:{INK};letter-spacing:-2px'>{sm}</div>
{cells}
<div class='lab' style='left:46px;top:546px;font-size:28px;color:{MUTE}'>1칸 = 1천만원</div>
<div class='fine' style='left:46px;top:616px;font-size:26px;color:{MUTE}'>{FINE}</div>
"""


VARIANTS['x1f'] = x1f()
VARIANTS['x1g'] = x1g()


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'&&c.tagName!=='BR'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});
      return bad}""")


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
            sizes = pg.evaluate("()=>[...document.querySelectorAll('[data-fit]')].map(e=>e.id+':'+getComputedStyle(e).fontSize)")
            im = Image.open(out); assert im.size == (1280, 720)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', sizes, '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if any(report[k] for k in keys): sys.exit(3)


if __name__ == '__main__':
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
