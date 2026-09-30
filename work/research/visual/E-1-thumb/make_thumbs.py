# E-1 썸네일 시안 3개(캐릭터·로고·인물 없음, 2026-10-01 visual) — py -3.12 make_thumbs.py
# 숫자 출처: ep/E-1/facts.txt [4] SK하이닉스 349,000원(2025-09-29) → 1,790,000원(2026-09-29) +412.9%
#   · 최대 낙폭 −54.7%(2026-06-22 → 2026-07-30) · 선은 raw/naver_000660.txt 종가(네이버 금융 일별 시세)
# 문구: 카피라이터 ep/E-1/titles.md 썸네일 1위 짝 "SK하이닉스 +412.9%" / "−54.7%".
# 색: 한국 시세 관례(오름 빨강·내림 파랑). 카피라이터 메모의 '−54.7% 빨강'은 한국 시청자에게 '오름'으로 읽혀 파랑으로 바꿈.
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576(길이 표시)과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표로 자동 검사.
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'E-1')
FONTS = os.path.join(ROOT, 'work', 'video', 'public', 'fonts').replace('\\', '/')

# 종가 1년(2025-09-29 ~ 2026-09-29)
raw = open(os.path.join(EP, 'raw', 'naver_000660.txt'), encoding='utf-8', errors='ignore').read()
rows = [(d, float(c)) for d, o, h, l, c in re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)', raw)]
S = [r for r in rows if '20250929' <= r[0] <= '20260929']
assert S[0] == ('20250929', 349000.0) and S[-1] == ('20260929', 1790000.0), (S[0], S[-1])
PK = max((r for r in S if r[0] <= '20260622'), key=lambda r: r[1]); TR = [r for r in S if r[0] == '20260730'][0]
assert PK[0] == '20260622' and round((TR[1] / PK[1] - 1) * 100, 1) == -54.7, (PK, TR)
UP, DN, YEL = '#FF4D4F', '#3D8BFF', '#FFD60A'

def chart(x0, y0, w, h, rng=None, stroke=7, area=True, marks=True):
    """0원부터 시작하는 선. rng=(시작일, 끝일)이면 그 구간만(확대)."""
    pts = S if not rng else [r for r in S if rng[0] <= r[0] <= rng[1]]
    lo = 0  # 확대 구간도 0원부터(레드팀 r1: 바닥을 올리면 반토막이 88% 하락처럼 보임)
    hi = max(p[1] for p in pts) * 1.04
    X = lambda i: x0 + i / (len(pts) - 1) * w
    Y = lambda v: y0 + h - (v - lo) / (hi - lo) * h
    line = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, (_, v) in enumerate(pts))
    ip = next(i for i, p in enumerate(pts) if p[0] == PK[0]); it = next(i for i, p in enumerate(pts) if p[0] == TR[0])
    seg = ' '.join(f'{X(i):.1f},{Y(pts[i][1]):.1f}' for i in range(ip, it + 1))
    s = f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
    if area:
        s += f"<polygon points='{x0},{y0+h} {line} {x0+w},{y0+h}' fill='url(#g)'/>"
    s += f"<defs><linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{UP}' stop-opacity='.35'/><stop offset='1' stop-color='{UP}' stop-opacity='0'/></linearGradient></defs>"
    s += f"<rect x='{X(ip):.1f}' y='{y0-6}' width='{X(it)-X(ip):.1f}' height='{h+6}' fill='{DN}' opacity='.22'/>"
    s += f"<polyline points='{line}' fill='none' stroke='{UP}' stroke-width='{stroke}' stroke-linejoin='round' stroke-linecap='round'/>"
    s += f"<polyline points='{seg}' fill='none' stroke='{DN}' stroke-width='{stroke+2}' stroke-linejoin='round' stroke-linecap='round'/>"
    if marks:
        for i, c in ((ip, '#fff'), (it, '#fff')):
            s += f"<circle cx='{X(i):.1f}' cy='{Y(pts[i][1]):.1f}' r='{stroke+4}' fill='{c}' stroke='#0E1016' stroke-width='4'/>"
    s += "</svg>"
    return s, (X(ip), Y(pts[ip][1])), (X(it), Y(pts[it][1])), (X(0), Y(pts[0][1])), (X(len(pts) - 1), Y(pts[-1][1]))

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
@font-face{font-family:PD;src:url('file:///%(f)s/pd500.ttf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1280px;height:720px;overflow:hidden;position:relative;font-family:PD;background:#0E1016}
.t{position:absolute;font-family:BH;white-space:nowrap;line-height:1;text-shadow:
   5px 5px 0 #000,-5px 5px 0 #000,5px -5px 0 #000,-5px -5px 0 #000,0 7px 0 #000,0 -6px 0 #000,7px 0 0 #000,-7px 0 0 #000}
.lab{position:absolute;font:700 28px PD;color:#C9D1DE;white-space:nowrap}
.fine{position:absolute;left:52px;top:612px;font:500 24px PD;color:#8A93A3;white-space:nowrap}
</style></head><body>%(body)s
<script>
function fit(id,maxW){const e=document.getElementById(id);let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e.id,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
FINE = "<div class='fine'>종가 기준 · 25.9.29→26.9.29 · 네이버 금융 일별 시세</div>"
BG = "<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 70% 20%,#1d2438 0%,#0E1016 65%)'></div>"

# e1a — X-THUMB-2 A(두 줄 대비): 왼쪽 두 숫자(크기 비슷하게), 오른쪽 위 1년 선(0원부터)
c, pk, tr, st, en = chart(640, 70, 600, 260)
e1a = f"""{BG}{c}
<div class='lab' style='left:{pk[0]-150}px;top:{pk[1]-46}px'>6/22 고점</div>
<div class='lab' style='left:{tr[0]+18}px;top:{tr[1]+2}px'>7/30</div>
<div id='a1' class='t' data-fit='560' style='left:52px;top:44px;font-size:96px;color:{YEL}'>SK하이닉스</div>
<div id='a0' class='t' data-fit='600' style='left:48px;top:156px;font-size:156px;color:{UP}'>+412.9%</div>
<div class='lab' style='left:56px;top:322px;color:#fff;font-size:32px'>1년(25.9.29→26.9.29)</div>
<div id='a2' class='t' data-fit='640' style='left:44px;top:392px;font-size:172px;color:{DN}'>−54.7%</div>
<div class='lab' style='left:700px;top:392px;color:#fff;font-size:44px'>그 안의 최대 낙폭</div>
<div class='t' style='left:700px;top:452px;font-size:66px;color:#fff'>6/22→7/30</div>{FINE}"""

# e1b — X-THUMB-2 B(한 줄 큰 숫자): 큰 −54.7% 한 덩이, 선은 뒤에 흐리게
c, pk, tr, st, en = chart(40, 60, 1200, 470, stroke=6, marks=False)
e1b = f"""{BG}<div style='position:absolute;inset:0;opacity:.5'>{c}</div>
<div style='position:absolute;left:52px;top:40px;display:flex;gap:18px;align-items:center'>
 <span style='background:{YEL};color:#111;font:56px BH;padding:10px 22px;border-radius:12px'>SK하이닉스</span>
 <span class='t' style='position:static;font-size:84px;color:{UP}'>+412.9%</span></div>
<div class='lab' style='left:56px;top:150px;color:#fff;font-size:34px'>1년 동안 오른 주식, 그 안에서</div>
<div id='b1' class='t' data-fit='1176' style='left:36px;top:208px;font-size:330px;color:{DN}'>−54.7%</div>
<div class='lab' style='left:56px;top:548px;color:#fff;font-size:32px'>6/22 고점 → 7/30 저점</div>{FINE}"""

# e1c — 대결 구도: 왼쪽 1년 전체(+412.9%) | 오른쪽 확대(−54.7%), 두 그래프 모두 0원부터
cl, pkl, trl, stl, enl = chart(40, 300, 560, 250, stroke=6)
cr, pkr, trr, _, _ = chart(700, 300, 520, 250, rng=('20260601', '20260814'), stroke=7)
e1c = f"""{BG}
<div style='position:absolute;left:650px;top:30px;width:4px;height:530px;background:#2a3246'></div>
{cl}{cr}
<div id='c0' class='t' data-fit='570' style='left:40px;top:34px;font-size:72px;color:{YEL}'>SK하이닉스 1년</div>
<div id='c1' class='t' data-fit='580' style='left:34px;top:122px;font-size:160px;color:{UP}'>+412.9%</div>
<div id='c2' class='t' data-fit='540' style='left:700px;top:34px;font-size:72px;color:#fff'>그중 6/22→7/30</div>
<div id='c3' class='t' data-fit='540' style='left:694px;top:122px;font-size:160px;color:{DN}'>−54.7%</div>{FINE}"""

VARIANTS = {'e1a': e1a, 'e1b': e1b, 'e1c': e1c}

def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(['SCRIPT','svg','polyline','polygon','rect','circle','defs','linearGradient','stop'].includes(e.tagName)||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()))return;
      const r=e.getBoundingClientRect();
      if((r.right>960&&r.bottom>576)||r.bottom>684||r.right>1280||r.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(r.left)+'-'+Math.round(r.right)+','+Math.round(r.bottom));});return bad}""")

def main():
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k, body in VARIANTS.items():
            html = os.path.join(HERE, f'{k}.html')
            open(html, 'w', encoding='utf-8').write(BASE % {'f': FONTS, 'body': body})
            pg.goto('file:///' + html.replace('\\', '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
            report[k] = check_zones(pg)
            im = Image.open(out); im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            g = im.copy().convert('RGBA'); ov = Image.new('RGBA', g.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            d.rectangle((960, 576, 1280, 720), fill=(255, 0, 0, 90)); d.rectangle((0, 684, 1280, 720), fill=(255, 0, 0, 90))
            d.rounded_rectangle((1160, 668, 1268, 704), 6, fill=(0, 0, 0, 220))
            Image.alpha_composite(g, ov).convert('RGB').save(os.path.join(HERE, f'{k}_guides.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(os.path.join(HERE, 'zones.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
