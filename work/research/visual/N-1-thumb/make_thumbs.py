# N-1 '나 vs 남들 ① 연봉·순자산 줄' 썸네일 시안(2026-10-02 23시 visual) — py -3.12 make_thumbs.py [n1a,n1b,...]
# 숫자 출처: ep/N-1/facts.txt [S1] 전체 21,078,535명·1인 평균 4,475만원, [표A-위치] 4,475 → 상위 35%와 36% 사이
# 지시(today.md 206행): 큰 글자 빈칸 '연봉 ___ → 상위 ?%' + 숫자 1, 층·건물 그림 금지.
# 경쟁과 다른 점(compare.png): 경쟁 5 = 실사·인물 사진 + 아래 노랑/초록 테두리 글씨 두 줄 + 피라미드·사다리·층.
#   우리 = 사진·인물 0, 테두리 글씨 0, 그림은 '100칸 한 줄'(줄 세우기) 하나, '상위 몇%?' 말투 대신 빈칸.
# 실험: X-THUMB-2 — n1a·n1c = B(한 줄 큰 숫자/문장), n1b = A(두 줄 대비)
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표 자동 검사(zones.json).
import os, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'N-1')
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
assert '1인 평균 4,475만원' in facts and '4,475만원(평균) → 상위 35%(4,537)와 36%(4,443) 사이' in facts
assert '전체 신고 인원 21,078,535명' in facts
RED, INK, GREY, PAPER = '#D11F1A', '#16181D', '#5A6170', '#F5F2EA'

BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]


def strip(x, y, w, h, mark=None, mid=True, cells=100, dark=False):
    """100칸 한 줄(왼쪽 = 상위 1%). mark = 칸 번호(1~100)에 빨간 칸."""
    cw = w / cells; s = ''
    for i in range(cells):
        on = mark is not None and i + 1 == mark
        c = RED if on else ('#3A404C' if dark else '#D5D0C4')
        s += f"<div style='position:absolute;left:{x + i * cw:.1f}px;top:{y}px;width:{cw - 2:.1f}px;height:{h}px;background:{c}'></div>"
    if mid:
        mx = x + 50 * cw
        s += f"<div style='position:absolute;left:{mx - 2:.0f}px;top:{y - 18}px;width:4px;height:{h + 36}px;background:{'#C9CED8' if dark else INK}'></div>"
    return s


FINE = "<div class='fine' style='color:%s'>국세청 근로소득 백분위 · 2024년 귀속 · 직장인 2,108만 명</div>"

# n1a — 빈칸만(내 돈 대입 + 질문): '연봉 [    ] 만원' → '상위 ?%' / 아래 100칸 줄
n1a = f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:14px;background:{INK}'></div>
<div class='lab' style='left:58px;top:52px;font-size:40px;color:{GREY}'>직장인 2,108만 명 한 줄로 세우면</div>
<div class='t' style='left:54px;top:132px;font-size:150px;color:{INK}'>연봉</div>
<div style='position:absolute;left:340px;top:128px;width:540px;height:158px;border:8px dashed {INK};border-radius:14px;background:#fff'></div>
<div class='t' style='left:900px;top:172px;font-size:96px;color:{INK}'>만원</div>
<div class='t' style='left:54px;top:322px;font-size:170px;color:{RED}'>→ 상위 ?%</div>
{strip(58, 540, 1160, 24, mid=False)}
<div class='lab' style='left:58px;top:576px;font-size:26px;color:{GREY}'>상위 1%</div>
"""

# n1b — 두 줄 대비(빈칸에 평균을 넣은 결과): '평균 연봉 4,475만원' / '상위 35~36%' + 줄에서 가운데 아님
n1b = f"""<div style='position:absolute;inset:0;background:#101217'></div>
<div class='t' style='left:54px;top:50px;font-size:96px;color:#fff'>평균 연봉 <span style='color:#FFD43B'>4,475만원</span></div>
<div class='lab' style='left:58px;top:176px;font-size:46px;color:#C9CED8'>직장인 줄에서 내 자리는</div>
<div id='b1' class='t' data-fit='1160' style='left:48px;top:240px;font-size:220px;color:#FF4D47'>상위 35~36%</div>
{strip(58, 520, 1160, 26, mark=36, dark=True)}
<div class='lab' style='left:{58 + 50 * 11.6 - 44:.0f}px;top:458px;font-size:28px;color:#C9CED8'>가운데</div>
"""

# n1c — 질문 반전: '평균 연봉은 가운데일까?' + 줄 위 핀(4,475) vs 가운데 선
cw = 1160 / 100; px = 58 + 35.5 * cw
n1c = f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:14px;background:{INK}'></div>
<div id='c0' class='t' data-fit='1170' style='left:50px;top:60px;font-size:150px;color:{INK}'>평균 연봉은</div>
<div id='c1' class='t' data-fit='1170' style='left:50px;top:220px;font-size:150px;color:{RED}'>가운데일까?</div>
{strip(58, 470, 1160, 40)}
<div style='position:absolute;left:{px - 4:.0f}px;top:410px;width:8px;height:110px;background:{RED}'></div>
<div class='lab' style='left:{px - 110:.0f}px;top:352px;font-size:40px;color:#fff;background:{RED};padding:4px 14px;border-radius:8px'>4,475만원</div>
<div class='lab' style='left:{58 + 50 * cw - 50:.0f}px;top:526px;font-size:30px;color:{INK}'>가운데</div>
<div class='lab' style='left:58px;top:526px;font-size:28px;color:{GREY}'>상위 1%</div>
"""

VARIANTS = {'n1a': n1a + FINE % '#6B7280', 'n1b': n1b + FINE % '#8A93A3', 'n1c': n1c + FINE % '#6B7280'}

# ── 2차(23:3x) — 1차 심사 공통 지적 반영: ① 168px에서 줄·핀이 안 보임 → 줄 높이 3배·핀 글씨 2배
#    ② 베이지 바탕이 흰 피드에 묻힘·여백 40% → 진한 바탕, 화면 채우기 ③ '상위 ?%'·'내 자리는'(틀린 주어) 뺌
def big_strip(y, h, mark_at, base, mid_col, hi, band=None):
    """굵은 100칸 줄. mark_at = 핀 위치(칸 단위, 35.5 = 35·36칸 사이). band = 핀~가운데 사이 색."""
    x0, w = 58, 1164; cw = w / 100; s = ''
    for i in range(100):
        c = band if band and mark_at <= i + 0.5 <= 50 else base
        s += f"<div style='position:absolute;left:{x0 + i * cw:.1f}px;top:{y}px;width:{cw - 3:.1f}px;height:{h}px;background:{c}'></div>"
    mx = x0 + 50 * cw; px_ = x0 + mark_at * cw
    s += f"<div style='position:absolute;left:{mx - 3:.0f}px;top:{y - 14}px;width:6px;height:{h + 28}px;background:{mid_col}'></div>"
    s += f"<div style='position:absolute;left:{px_ - 6:.0f}px;top:{y - 34}px;width:12px;height:{h + 48}px;background:{hi}'></div>"
    return s, mx, px_

# n1d — 반전 서술(파랑 바탕): '평균 연봉 4,475만원' / '가운데가 아니다' + 굵은 줄(핀~가운데 노란 띠)
sd, mxd, pxd = big_strip(472, 84, 35.5, '#3D63D6', '#fff', '#FFD400', band='#8FA8F0')
n1d = f"""<div style='position:absolute;inset:0;background:#1A3FB8'></div>
<div class='t' style='left:52px;top:46px;font-size:104px;color:#fff'>평균 연봉 <span style='color:#FFD400'>4,475만원</span></div>
<div id='d1' class='t' data-fit='1170' style='left:48px;top:196px;font-size:190px;color:#fff'>가운데가 아니다</div>
{sd}
<div class='lab' style='left:{pxd - 70:.0f}px;top:572px;font-size:44px;color:#FFD400'>4,475</div>
<div class='lab' style='left:{mxd - 56:.0f}px;top:572px;font-size:44px;color:#fff'>가운데</div>
<div class='lab' style='left:58px;top:572px;font-size:34px;color:#C9D6FF'>상위 1%</div>
"""

# n1e — n1c 고침(질문 유지): 진한 먹색 바탕, 질문 두 줄 더 크게, 굵은 줄 + 큰 핀 라벨
se, mxe, pxe = big_strip(470, 84, 35.5, '#3A404C', '#fff', '#FF3B30', band='#7A2A27')
n1e = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div id='e0' class='t' data-fit='1170' style='left:50px;top:40px;font-size:168px;color:#fff'>평균 연봉은</div>
<div id='e1' class='t' data-fit='1170' style='left:50px;top:214px;font-size:168px;color:#FF3B30'>가운데일까?</div>
{se}
<div class='lab' style='left:{pxe - 236:.0f}px;top:572px;font-size:46px;color:#FF3B30'>4,475만원</div>
<div class='lab' style='left:{mxe - 56:.0f}px;top:572px;font-size:44px;color:#fff'>가운데</div>
<div class='lab' style='left:58px;top:572px;font-size:34px;color:#8A93A3'>상위 1%</div>
"""

# n1f — 지시 틀(빈칸 채움 + 숫자 1): '연봉 [4,475]만원이면' / '상위 35~36%' + 굵은 줄 (빈칸은 흰 입력칸에 숫자를 채운 모양)
sf, mxf, pxf = big_strip(486, 76, 35.5, '#3A404C', '#fff', '#FF3B30')
n1f = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div class='t' style='left:52px;top:58px;font-size:112px;color:#fff'>연봉</div>
<div style='position:absolute;left:290px;top:36px;width:356px;height:150px;background:#fff;border-radius:16px;border-bottom:10px solid #FF3B30'></div>
<div class='t' style='left:318px;top:52px;font-size:120px;color:{INK}'>4,475</div>
<div class='t' style='left:672px;top:58px;font-size:112px;color:#fff'>만원이면</div>
<div id='f1' class='t' data-fit='1170' style='left:46px;top:226px;font-size:200px;color:#FF3B30'>상위 35~36%</div>
{sf}
<div class='lab' style='left:{mxf - 56:.0f}px;top:582px;font-size:44px;color:#fff'>가운데</div>
<div class='lab' style='left:58px;top:582px;font-size:34px;color:#8A93A3'>상위 1%</div>
"""
FINE2 = "<div class='fine' style='color:%s;top:648px;font-size:22px'>국세청 근로소득 백분위 · 2024년 귀속 · 직장인 2,108만 명</div>"
VARIANTS.update({'n1d': n1d + FINE2 % '#C9D6FF', 'n1e': n1e + FINE2 % '#8A93A3', 'n1f': n1f + FINE2 % '#8A93A3'})


# ── 3차(10/3 17:1x) — 8점 재도전. 2차 남은 고칠 점 ① '평균' 다시 ② 핀 라벨·핀~가운데 띠 ③ '1억' 보조 시험
#    + R-1 r1v 형식(아는 값 크게 밝은 면 + 모르는 값 '?' 상자) — r1v는 초록 상자 3개 가로, N-1은 빨강·세로 줄 목록으로 바꿔 재탕 피함.
#    숫자: 4,475 → 상위 35~36% · 3,000만원 → 57~58% · 1억원 → 7~8% (facts [표A-위치]·80행). 답은 '?'로 숨김(영상이 답).
QBOX = lambda x, y, w, h, lab: (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#2A2D34;border-radius:12px;border-left:12px solid #FF3B30'></div>"
    f"<div class='lab' style='left:{x + 36}px;top:{y + (h - 64) // 2}px;font-size:58px;color:#fff'>{lab}</div>"
    f"<div class='t' style='left:{x + w - 150}px;top:{y + (h - 96) // 2}px;font-size:96px;color:#FF3B30'>?%</div>")
assert '3,000만원(57~58%)' in facts and '1억원 → 상위 7%(10,456)와 8%(9,925) 사이' in facts

# n1g — r1v 형식: 왼쪽 밝은 면 = 평균 연봉의 답(상위 35~36%), 오른쪽 = '?' 줄 셋(3천만·1억·내 연봉) → 내 돈 대입
n1g = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div class='t' style='left:40px;top:28px;font-size:92px;color:#fff'>연봉 줄 세우면</div>
<div style='position:absolute;left:40px;top:170px;width:560px;height:410px;background:#F4F1E8;border-radius:12px'></div>
<div class='lab' style='left:72px;top:196px;font-size:54px;color:{INK}'>평균 4,475만원</div>
<div class='t' style='left:68px;top:300px;font-size:120px;color:{INK}'>상위</div>
<div id='g1' class='t' data-fit='500' style='left:68px;top:430px;font-size:132px;color:#D11F1A'>35~36%</div>
<div class='t' style='left:640px;top:170px;font-size:80px;color:#FF3B30'>내 연봉은?</div>
{QBOX(640, 268, 600, 88, '3천만원')}
{QBOX(640, 366, 600, 88, '1억원')}
{QBOX(640, 464, 600, 88, '내 연봉')}
"""

# n1h — r1v 형식 단순판: '?' 상자 하나로 합침(백로그 'R-1 8점용 1안'을 N-1에서 먼저 시험)
n1h = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div class='t' style='left:40px;top:28px;font-size:92px;color:#fff'>직장인 2,108만 명 중</div>
<div style='position:absolute;left:40px;top:170px;width:600px;height:410px;background:#F4F1E8;border-radius:12px'></div>
<div class='lab' style='left:72px;top:196px;font-size:54px;color:{INK}'>평균 연봉 4,475만원</div>
<div class='t' style='left:68px;top:300px;font-size:120px;color:{INK}'>상위</div>
<div id='h1' class='t' data-fit='540' style='left:68px;top:430px;font-size:140px;color:#D11F1A'>35~36%</div>
<div style='position:absolute;left:680px;top:170px;width:560px;height:404px;background:#FF3B30;border-radius:12px'></div>
<div class='lab' style='left:716px;top:196px;font-size:58px;color:#fff'>내 연봉이면?</div>
<div class='t' style='left:790px;top:290px;font-size:240px;color:#fff'>?%</div>
"""

# n1i — n1f 고침(2차 남은 점 ①②): '평균' 넣기, 핀 라벨 '평균', 핀~가운데 밝은 띠 + '가운데 아님'
si, mxi, pxi = big_strip(486, 76, 35.5, '#3A404C', '#fff', '#FF3B30', band='#FFB3AE')
n1i = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div class='t' style='left:52px;top:58px;font-size:104px;color:#fff'>평균</div>
<div style='position:absolute;left:252px;top:36px;width:356px;height:150px;background:#fff;border-radius:16px;border-bottom:10px solid #FF3B30'></div>
<div class='t' style='left:280px;top:52px;font-size:120px;color:{INK}'>4,475</div>
<div class='t' style='left:634px;top:58px;font-size:104px;color:#fff'>만원 연봉</div>
<div id='i1' class='t' data-fit='1170' style='left:46px;top:226px;font-size:200px;color:#FF3B30'>상위 35~36%</div>
{si}
<div class='lab' style='left:{pxi - 54:.0f}px;top:582px;font-size:44px;color:#FF3B30'>평균</div>
<div class='lab' style='left:{mxi - 56:.0f}px;top:582px;font-size:44px;color:#fff'>가운데</div>
<div class='lab' style='left:58px;top:582px;font-size:34px;color:#8A93A3'>상위 1%</div>
"""
VARIANTS.update({'n1g': n1g + FINE2 % '#8A93A3', 'n1h': n1h + FINE2 % '#8A93A3', 'n1i': n1i + FINE2 % '#8A93A3'})


# ── 4차(10/3 17:3x) — 3차 공통 지적: 답만 보여 주면 누를 이유 약함·'평균≠가운데'가 168px 막대 라벨에만 있음·'상위 1%' 라벨 틀림(끝은 맨 위)
#    → n1j: 반전을 글자로('평균 연봉인데' → '상위 35~36%'), 막대 라벨 3배·띠 진하게, 왼쪽 끝 '맨 위'
#    → n1k: n1h 고침 — 왼쪽 '평균인데 상위 35~36%' 크게, 오른쪽 '?' 상자 짧게(길이 표시 자리에서 떨어지게)
sj, mxj, pxj = big_strip(470, 92, 35.5, '#3A404C', '#fff', '#FF3B30', band='#FF8A80')
n1j = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div class='t' style='left:50px;top:40px;font-size:118px;color:#fff'>평균 연봉인데</div>
<div id='j1' class='t' data-fit='1170' style='left:46px;top:196px;font-size:210px;color:#FF3B30'>상위 35~36%</div>
{sj}
<div class='lab' style='left:{pxj - 64:.0f}px;top:574px;font-size:54px;color:#FF3B30'>평균</div>
<div class='lab' style='left:{mxj - 70:.0f}px;top:574px;font-size:54px;color:#fff'>가운데</div>
<div class='lab' style='left:58px;top:578px;font-size:40px;color:#8A93A3'>맨 위</div>
"""
n1k = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div style='position:absolute;left:40px;top:40px;width:700px;height:520px;background:#F4F1E8;border-radius:12px'></div>
<div class='t' style='left:76px;top:76px;font-size:120px;color:{INK}'>평균 연봉인데</div>
<div class='t' style='left:76px;top:236px;font-size:120px;color:{INK}'>상위</div>
<div id='k1' class='t' data-fit='630' style='left:72px;top:372px;font-size:150px;color:#D11F1A'>35~36%</div>
<div style='position:absolute;left:780px;top:40px;width:460px;height:420px;background:#FF3B30;border-radius:12px'></div>
<div class='lab' style='left:814px;top:66px;font-size:60px;color:#fff'>내 연봉은?</div>
<div class='t' style='left:850px;top:170px;font-size:230px;color:#fff'>?%</div>
"""
FINE3 = "<div class='fine' style='color:%s;top:648px;font-size:22px'>국세청 근로소득 백분위(총급여) · 2024년 귀속 · 2,108만 명</div>"
VARIANTS.update({'n1j': n1j + FINE3 % '#8A93A3', 'n1k': n1k + FINE3 % '#8A93A3'})


# ── 5차(10/3 17:4x) — 4차 n1j 7.00(통과): 공통 지적 '막대 라벨이 168px에서 안 읽힘' → 라벨 1.6배, 막대 얇게 위로
sl, mxl, pxl = big_strip(438, 72, 35.5, '#3A404C', '#fff', '#FF3B30', band='#FF8A80')
n1l = f"""<div style='position:absolute;inset:0;background:#121418'></div>
<div class='t' style='left:50px;top:30px;font-size:118px;color:#fff'>평균 연봉인데</div>
<div id='l1' class='t' data-fit='1170' style='left:46px;top:180px;font-size:210px;color:#FF3B30'>상위 35~36%</div>
{sl}
<div class='t' style='left:{pxl - 120:.0f}px;top:528px;font-size:84px;color:#FF3B30'>평균</div>
<div class='t' style='left:{mxl + 20:.0f}px;top:528px;font-size:84px;color:#fff'>가운데</div>
<div class='lab' style='left:58px;top:534px;font-size:40px;color:#8A93A3'>맨 위</div>
"""
VARIANTS.update({'n1l': n1l + FINE3 % '#8A93A3'})


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
