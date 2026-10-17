# H-3 '30억 안팎에 팔린 집 크기 — 신천 85㎡ vs 목동신시가지 96㎡' 썸네일 시안(2026-10-17 visual-designer)
# 문구: ep/H-3/copy/titles.md 1위 짝 B3′(copywriter 10/17 07:56) — 파일에서 읽어 assert. 168px에서 깨지면 쓰는 대체 문구도 같은 파일에서.
# 숫자: ep/H-3/calc_out.txt §5 '30.00억 안팎' 줄(신천동 175건 85㎡ · 목동(신시가지) 67건 96㎡ · 압구정동 0건)·§6 압구정 가장 싼 거래 35.70억 — 파일에서 읽어 assert.
# 그림: 좌우 카드 두 칸 금지(P-1·C-2·H-2 연속). '85 vs 96'은 한 그림 — 넓이에 비례한 평면 두 장을 왼쪽 아래 모서리에 겹침(변 길이 = √넓이), 또는 0부터 시작하는 줄자 하나.
#       사진·인물·캐릭터·단지 로고·지도·노란 글씨·번개 VS·아래 어두운 띠 0(경쟁 5장 공통 문법 피함). 숫자는 PD 700(BH '5'가 's'로 보임 — H-2 배운 것).
# 가려짐: 오른쪽 아래 x>960·y>576, 아래 5%(y>684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, json, sys, re, math
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'H-3')

# ── 문구(titles.md 1위 짝) ──
tt = open(os.path.join(EP, 'copy', 'titles.md'), encoding='utf-8').read()
m = re.search(r"썸네일 B3′: 앞줄 '([^']+)' · 큰 글씨 '([^']+)' · 작은 줄 '([^']+)'", tt)
TOP, BIG, SMALL = m.groups()
assert (TOP, BIG, SMALL) == ('30억 안팎에 팔린 집 크기', '신천 85㎡ vs 목동신시가지 96㎡', '압구정동은 가장 싼 거래도 35억 넘어'), m.groups()
m2 = re.search(r"큰 글씨는 '([^']+)'로 두고 앞줄을 \*\*'([^']+)'\*\*로", tt)
BIG_B, TOP_B = m2.groups()
assert (BIG_B, TOP_B) == ('신천 85㎡ vs 목동 96㎡', '30억 안팎 · 목동신시가지 1~7단지'), m2.groups()
for bad in ('재건축', '갭투자', '사라', '추천', '전망', '대장주', '34평', '30억대', '0건'):
    assert all(bad not in s for s in (TOP, BIG, SMALL, BIG_B, TOP_B)), bad

# ── 숫자(calc_out §5·§6) ──
cal = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
l30 = [l for l in cal.splitlines() if l.startswith('- 30.00억 안팎')][0]
SIN = re.search(r'신천동 (\d+)건 전용 중앙 (\d+)㎡', l30).groups()
MOK = re.search(r'목동\(신시가지\) (\d+)건 전용 중앙 (\d+)㎡', l30).groups()
assert '압구정동 0건' in l30 and SIN == ('175', '85') and MOK == ('67', '96'), (SIN, MOK)
cheap = [float(x) for x in re.findall(r'압구정동 한양1차\(영동한양\) 전용 [\d.]+㎡ · ([\d.]+)억', cal.split('## 6.')[1].split('## 7.')[0])]
assert min(cheap) == 35.70 and min(cheap) > 35, cheap
A_S, A_M = int(SIN[1]), int(MOK[1])
assert f'{A_S}㎡' in BIG and f'{A_M}㎡' in BIG and f'{A_S}㎡' in BIG_B and f'{A_M}㎡' in BIG_B
# facts.txt 대조(사실표와 calc가 같은 값인지)
fx = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
assert '신천동 175건 · 전용 중앙 85㎡' in fx and '67건 · 전용 중앙 96㎡' in fx and '35.70억' in fx
print('문구·숫자 확인:', TOP, '|', BIG, '|', SMALL, '| 신천', SIN, '목동신시가지', MOK, '압구정 최저', min(cheap))

INK, OR, PAPER, MUTE = '#16181D', '#FF5A00', '#F3EFE7', '#7C818C'
FONT = 'file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/public/fonts/'
HEAD = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:BH;src:url('{FONT}BlackHanSans.ttf')}}
@font-face{{font-family:PD;src:url('{FONT}pd700.ttf');font-weight:700}}
@font-face{{font-family:PD;src:url('{FONT}pd500.ttf');font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:PD}}
.t{{position:absolute;font:700 100px PD;white-space:nowrap;line-height:1;letter-spacing:-2px}}
.lab{{position:absolute;font:700 30px PD;white-space:nowrap;line-height:1.1}}
</style></head><body>"""
TAIL = """<script>
function fit(e,maxW){let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
VARIANTS = {}


def big_line(text, base, ink, c85, c96, name_em=.5, vs_em=.34, vs_c=MUTE, fitw=1190, left=44, top=110, idn='big'):
    """큰 글씨 한 줄 — 이름은 작게(base×name_em), 넓이 값은 크게(base). em이라 data-fit 줄이면 같이 줄어든다."""
    a, b = text.split(' vs ')
    n1, v1 = a.rsplit(' ', 1); n2, v2 = b.rsplit(' ', 1)
    sp = lambda t, em, c: f"<span style='font-size:{em}em;color:{c}'>{t}</span>"
    return (f"<div id='{idn}' class='t' data-fit='{fitw}' style='left:{left}px;top:{top}px;font-size:{base}px;color:{ink};display:flex;align-items:baseline;gap:.12em'>"
            f"{sp(n1, name_em, ink)}{sp(v1, 1, c85)}{sp('vs', vs_em, vs_c)}{sp(n2, name_em, ink)}{sp(v2, 1, c96)}</div>")


def plans(x0, ybot, side96, c85, c96, wall, line='#FFFFFF'):
    """넓이 비례 평면 두 장 — 96㎡(뒤, c96)와 85㎡(앞, c85)를 왼쪽 아래 모서리에 겹침. 변 = side96×√(85/96)."""
    s85 = side96 * math.sqrt(A_S / A_M)
    assert abs((s85 / side96) ** 2 - A_S / A_M) < 1e-9
    s96, s85 = round(side96), round(s85)
    o = f"<div style='position:absolute;left:{x0}px;top:{ybot - s96}px;width:{s96}px;height:{s96}px;background:{c96};border:{wall}px solid {INK}'></div>"
    o += f"<div style='position:absolute;left:{x0}px;top:{ybot - s85}px;width:{s85}px;height:{s85}px;background:{c85};border:{wall}px solid {INK}'></div>"
    # 85㎡ 안 방 칸막이(평면도처럼): 세로 벽 하나·가로 벽 하나, 문 틈 남김
    vx = x0 + round(s85 * .56); hy = ybot - round(s85 * .46)
    o += f"<div style='position:absolute;left:{vx}px;top:{ybot - s85}px;width:{max(3, wall // 2)}px;height:{round(s85 * .30)}px;background:{line}'></div>"
    o += f"<div style='position:absolute;left:{vx}px;top:{ybot - s85 + round(s85 * .42)}px;width:{max(3, wall // 2)}px;height:{round(s85 * .12)}px;background:{line}'></div>"
    o += f"<div style='position:absolute;left:{x0}px;top:{hy}px;width:{round(s85 * .36)}px;height:{max(3, wall // 2)}px;background:{line}'></div>"
    o += f"<div style='position:absolute;left:{x0 + round(s85 * .50)}px;top:{hy}px;width:{round(s85 * .50)}px;height:{max(3, wall // 2)}px;background:{line}'></div>"
    return o, s96, s85


# ── 1차 ──
# h3a: 밝은 판. 앞줄 → 큰 줄(값 크게, 96 주황) → 왼쪽 아래 평면 겹침(85 먹색 판·96 주황 테두리 판) + 오른쪽 작은 줄.
def board_a():
    pl, s96, s85 = plans(56, 668, 384, '#3A3F4A', OR, 7)
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:46px;top:28px;font-size:68px;color:{INK};letter-spacing:-1px'><span style='color:{OR}'>30억 안팎</span>에 팔린 집 크기</div>
{big_line(BIG, 158, INK, INK, OR, top=118)}
{pl}
<div class='lab' style='left:{56 + 26}px;top:{668 - s85 + 26}px;font-size:46px;color:#FFFFFF'>신천</div>
<div class='lab' style='left:{56 + s96 + 36}px;top:{668 - s96 + 4}px;font-size:46px;color:{OR}'>← 목동신시가지</div>
<div class='lab' style='left:{56 + s96 + 36}px;top:500px;font-size:42px;color:{INK}'>{SMALL}</div>
"""


# h3b: 대체 문구(큰 글 '신천 85㎡ vs 목동 96㎡', 앞줄 '30억 안팎 · 목동신시가지 1~7단지'). 그림 = 0~100㎡ 줄자 하나, 85·96 자리에 표시.
def board_b():
    x0, x1, ty = 50, 1130, 452
    W = x1 - x0; px = lambda v: x0 + W * v / 100
    ticks = ''
    for v in range(0, 101, 5):
        h = 34 if v % 10 == 0 else 18
        ticks += f"<div style='position:absolute;left:{px(v) - 1.5:.1f}px;top:{ty}px;width:3px;height:{h}px;background:{INK}'></div>"
        if v % 20 == 0:
            ticks += f"<div class='lab' style='left:{px(v) - 40:.1f}px;width:80px;text-align:center;top:{ty + 44}px;font-size:30px;color:{INK}'>{v}</div>"
    mk = lambda v, c, lab, dx: (f"<div style='position:absolute;left:{px(v) - 4:.1f}px;top:{ty - 70}px;width:8px;height:150px;background:{c}'></div>"
                                f"<div class='lab' style='left:{px(v) + dx:.1f}px;top:{ty - 118}px;font-size:44px;color:{c};{'' if dx < 0 else ''}'>{lab}</div>")
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:46px;top:26px;font-size:64px;color:{INK};letter-spacing:-1px'><span style='color:{OR}'>30억 안팎</span> · 목동신시가지 1~7단지</div>
{big_line(BIG_B, 190, INK, INK, OR, name_em=.52, top=112)}
<div style='position:absolute;left:{x0}px;top:{ty}px;width:{W}px;height:96px;background:#FFB98F;border-top:5px solid {INK};border-bottom:5px solid {INK}'></div>
{ticks}
<div class='lab' style='left:{x1 + 48}px;top:{ty + 30}px;font-size:36px;color:{INK}'>㎡</div>
{mk(A_S, INK, '신천', -104)}{mk(A_M, OR, '목동', 14)}
<div class='lab' style='left:48px;top:604px;font-size:46px;color:{INK}'>{SMALL}</div>
"""


# h3c: 어두운 판(화면당 다크 1 = 판 전체). 평면 겹침을 크게(왼쪽), 오른쪽 위 큰 줄 대신 큰 줄은 위 한 줄 그대로, 작은 줄은 평면 오른쪽.
def board_c():
    pl, s96, s85 = plans(56, 668, 420, '#E9E4DA', OR, 7, line='#9AA0AA')
    return f"""<div style='position:absolute;inset:0;background:#121419'></div>
<div class='t' style='left:46px;top:24px;font-size:64px;color:#FFFFFF;letter-spacing:-1px'><span style='color:{OR}'>30억 안팎</span>에 팔린 집 크기</div>
{big_line(BIG, 150, '#FFFFFF', '#FFFFFF', OR, top=104, vs_c='#8A909C')}
{pl}
<div class='lab' style='left:{56 + 24}px;top:{668 - s85 + 22}px;font-size:46px;color:{INK}'>신천 {A_S}㎡</div>
<div class='lab' style='left:{56 + s85 + 24}px;top:{668 - s96 + 22}px;font-size:46px;color:{OR}'>← 목동신시가지 {A_M}㎡</div>
<div class='lab' style='left:{56 + s96 + 30}px;top:510px;font-size:38px;color:#FFFFFF'>{SMALL}</div>
"""


VARIANTS['h3a'] = board_a()
VARIANTS['h3b'] = board_b()
VARIANTS['h3c'] = board_c()


# ── 2차(10/17) — 1차 h3a 6.17(제미나이 8·7 · Claude 5 · 레드팀 6 겹침 2), h3b 6.17(레드팀 겹침 3 반려·'목동' 단독은 facts [11]과 어긋남), h3c 5.83(겹침 3 반려).
#   Claude·레드팀 공통: 11㎡ 차이가 가는 주황 테두리라 안 보임 · 정보가 위 1/3에 몰림 · 압구정 줄이 168px에서 안 읽힘 · '←목동신시가지' 표시 군더더기.
# h3d: 1위 문구. 평면을 '같은 너비, 높이 ∝ 넓이' 직사각형 둘로 겹침(차이 11㎡가 높이 11.5% 띠 — 정사각형 겹침 6%보다 두 배 굵음), 주황 띠를 꽉 채우고 안에 '+11㎡'.
#      그림 높이 ≥ 360(화면 절반), 왼쪽 아래. 압구정 줄은 오른쪽 두 줄 64px(1차 42px의 1.5배).
# h3e: h3d + 출처 한 줄 '국토교통부 실거래 · 최근 1년'(titles.md 설명 첫 줄 제안의 말) — 레드팀 '정체성 ③ 공식 원문이 화면에 없음'.
def plans2(x0, ybot, w, k):
    h96, h85 = round(A_M * k), round(A_S * k)
    assert abs(h85 / h96 - A_S / A_M) < 0.01 and A_M - A_S == 11
    o = f"<div style='position:absolute;left:{x0}px;top:{ybot - h96}px;width:{w}px;height:{h96}px;background:{OR};border:7px solid {INK}'></div>"
    o += f"<div style='position:absolute;left:{x0}px;top:{ybot - h85}px;width:{w}px;height:{h85}px;background:#3A3F4A;border:7px solid {INK}'></div>"
    vx = x0 + round(w * .58); hy = ybot - round(h85 * .45)
    o += f"<div style='position:absolute;left:{vx}px;top:{ybot - h85}px;width:4px;height:{round(h85 * .32)}px;background:#FFFFFF;opacity:.7'></div>"
    o += f"<div style='position:absolute;left:{vx}px;top:{ybot - h85 + round(h85 * .44)}px;width:4px;height:{round(h85 * .10)}px;background:#FFFFFF;opacity:.7'></div>"
    o += f"<div style='position:absolute;left:{x0}px;top:{hy}px;width:{round(w * .38)}px;height:4px;background:#FFFFFF;opacity:.7'></div>"
    o += f"<div style='position:absolute;left:{x0 + round(w * .52)}px;top:{hy}px;width:{round(w * .48)}px;height:4px;background:#FFFFFF;opacity:.7'></div>"
    o += f"<div class='lab' style='left:{x0}px;width:{w}px;text-align:center;top:{ybot - h96 + 4}px;font-size:{h96 - h85 - 8}px;line-height:{h96 - h85 - 4}px;color:#FFFFFF'>+{A_M - A_S}㎡</div>"
    o += f"<div class='lab' style='left:{x0 + 28}px;top:{ybot - h85 + 26}px;font-size:48px;color:#FFFFFF'>신천</div>"
    return o, h96, h85


def board_d(src=False):
    pl, h96, h85 = plans2(48, 672, 440, 4.4)
    a, b = SMALL.split(' 거래도 ')
    tag = (f"<div class='lab' style='left:540px;top:500px;font-size:36px;color:{MUTE}'>국토교통부 실거래 · 최근 1년</div>" if src else '')
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:46px;top:18px;font-size:64px;color:{INK};letter-spacing:-1px'><span style='color:{OR}'>30억 안팎</span>에 팔린 집 크기</div>
{big_line(BIG, 150, INK, INK, OR, top=98)}
{pl}
<div class='t' style='left:540px;top:{(330 if src else 350)}px;font-size:64px;color:{INK}'>{a}</div>
<div class='t' style='left:540px;top:{(410 if src else 430)}px;font-size:64px;color:{INK}'>거래도 <span style='color:{OR}'>35억</span> 넘어</div>
{tag}
"""


VARIANTS['h3d'] = board_d()
VARIANTS['h3e'] = board_d(src=True)


# ── 3차(10/17) — 2차 h3e 6.5(제미나이 8·7 · Claude 6 · 레드팀 6 겹침 2), h3d 6.25, h3a 5.0.
#   Claude: 숫자 줄이 얇고 작아 목록에서 힘이 약함 · 평면 속 칸막이 지우고 덩어리 대비 단순하게 · +11 띠 굵게.
#   레드팀: 먹색 평면 덩어리가 화면 1/3 — 줄이고 그 자리에 '35억'을 크게(85·96·35가 다툼), 대안 = 압구정 줄을 다크카드 1장에 '35억' 주황 크게.
# h3f: 큰 줄 숫자 굵게(획 4px), 평면 너비 440→300·칸막이 없앰·높이 비례 k 4.4→4.6(띠 48→51px), 압구정 줄을 오른쪽 다크카드 1장(35억 120px 주황 — 큰 줄 숫자 128px보다 작게, 카피 위계), 출처 줄 카드 아래.
# h3g: h3f와 같고 카드 없이 밝은 판에 '35억' 120px 먹색 — 다크카드가 경쟁 '어두운 띠'와 겹쳐 보이는지 대조.
def board_f(card=True):
    k, w, x0, yb = 4.6, 300, 48, 676
    h96, h85 = round(A_M * k), round(A_S * k)
    assert abs(h85 / h96 - A_S / A_M) < 0.01
    pl = (f"<div style='position:absolute;left:{x0}px;top:{yb - h96}px;width:{w}px;height:{h96}px;background:{OR};border:7px solid {INK}'></div>"
          f"<div style='position:absolute;left:{x0}px;top:{yb - h85}px;width:{w}px;height:{h85}px;background:#3A3F4A;border:7px solid {INK}'></div>"
          f"<div class='lab' style='left:{x0}px;width:{w}px;text-align:center;top:{yb - h96 + 5}px;font-size:{h96 - h85 - 10}px;line-height:{h96 - h85 - 4}px;color:#FFFFFF'>+{A_M - A_S}㎡</div>"
          f"<div class='lab' style='left:{x0 + 28}px;top:{yb - h85 + 26}px;font-size:50px;color:#FFFFFF'>신천</div>")
    a, b = SMALL.split(' 거래도 ')
    assert b == '35억 넘어'
    cbg, cink = ('#16181D', '#FFFFFF') if card else (PAPER, INK)
    c35 = OR if card else INK
    cardh = f"<div style='position:absolute;left:390px;top:268px;width:846px;height:290px;background:{cbg};border-radius:20px'></div>" if card else ''
    big = big_line(BIG, 150, INK, INK, OR, top=96)  # 획은 넓이 값(85㎡·96㎡)에만 — 이름까지 굵히면 '신천'이 '신촌'으로 읽힘(58세 시험 1회차)
    big = big.replace("<span style='font-size:1em;color:", "<span style='font-size:1em;-webkit-text-stroke:4px currentColor;color:")
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
<div class='t' style='left:46px;top:16px;font-size:64px;color:{INK};letter-spacing:-1px'><span style='color:{OR}'>30억 안팎</span>에 팔린 집 크기</div>
{big}
{pl}
{cardh}
<div class='t' style='left:424px;top:292px;font-size:60px;color:{cink}'>{a} 거래도</div>
<div class='t' style='left:420px;top:388px;font-size:120px;color:{c35};-webkit-text-stroke:4px currentColor'>35억<span style='font-size:.5em;-webkit-text-stroke:0'> 넘어</span></div>
<div class='lab' style='left:394px;top:590px;font-size:34px;color:{MUTE}'>국토교통부 실거래 · 최근 1년</div>
"""


VARIANTS['h3f'] = board_f()
VARIANTS['h3g'] = board_f(card=False)


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
            sizes = pg.evaluate("()=>[...document.querySelectorAll('[data-fit]')].map(e=>e.id+':'+getComputedStyle(e).fontSize+' h'+Math.round(e.getBoundingClientRect().height))")
            im = Image.open(out); assert im.size == (1280, 720), im.size
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', sizes, '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if any(report[k] for k in keys): sys.exit('가려짐 위반 — 고칠 것')


if __name__ == '__main__':
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
