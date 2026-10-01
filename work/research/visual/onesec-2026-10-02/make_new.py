# 1초 시험 재시안(2026-10-02 visual) — 글자 3~6단어, 큰 숫자 1개, 후킹 장치 1개, 캐릭터·인물·로고 없음
#   py -3.12 make_new.py → ep/D-1/thumb_d1e·d1f.png, ep/E-1/thumb_e1d·e1e.png + s168/*.png
# 숫자: D-1 facts.txt [계산] 월 22,800원(1,000만원) → 67,850원(1,001만원), 연 540,600원 차이, 67,850/22,800 = 2.98배
#       E-1 facts.txt [9]·meta desc 삼성전자 영업이익 19.14배(1년 전 같은 분기), 주가 3.27배(25.9.29→26.9.29)
import os, sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(H)
sys.path.insert(0, os.path.join(V, 'E-1-thumb'))
import make_thumbs as M  # BASE·폰트·가려짐 검사 재사용(그림은 새로)
EP = os.path.join(V, '..', 'longform', 'ep')
assert round(67850 / 22800, 2) == 2.98 and (67850 - 22800) * 12 == 540600
assert round(19.14 / 3.27, 1) == 5.9
RED, BLU, YEL, GRY = '#FF4D4F', '#3D8BFF', '#FFD60A', '#5B6475'
BG = "<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 75% 25%,#222a40 0%,#0E1016 65%)'></div>"
TAG = lambda s, x=52, y=40, bg=YEL: f"<div style='position:absolute;left:{x}px;top:{y}px;background:{bg};color:#111;font:64px BH;padding:12px 26px;border-radius:14px;white-space:nowrap'>{s}</div>"
FINE = lambda s: f"<div class='fine'>{s}</div>"

def bars_v(x0, base, vals, w=150, gap=60, hmax=420, cols=(GRY, RED), labs=()):
    """세로 막대, 0부터 비례"""
    m = max(vals); s = ''
    for i, v in enumerate(vals):
        h = v / m * hmax; x = x0 + i * (w + gap)
        s += f"<div style='position:absolute;left:{x}px;top:{base-h}px;width:{w}px;height:{h}px;background:{cols[i]};border-radius:10px 10px 0 0'></div>"
        if labs: s += f"<div class='lab' style='left:{x-30}px;top:{base+12}px;width:{w+60}px;text-align:center;color:#fff;font-size:40px'>{labs[i]}</div>"
    return s

def bars_h(x0, y0, vals, wmax=1100, hh=110, gap=40, cols=(RED, GRY), names=(), nums=()):
    """가로 막대, 0부터 비례. 이름은 막대 안 왼쪽, 숫자는 막대 끝 바깥(짧으면) 또는 안"""
    m = max(vals); s = ''
    for i, v in enumerate(vals):
        w = v / m * wmax; y = y0 + i * (hh + gap)
        s += f"<div style='position:absolute;left:{x0}px;top:{y}px;width:{w}px;height:{hh}px;background:{cols[i]};border-radius:0 12px 12px 0'></div>"
        s += f"<div class='t' style='left:{x0+18}px;top:{y+36}px;font-size:80px;color:#fff'>{names[i]}</div>"
        nx = x0 + w + 24 if w < 520 else x0 + w - 370
        s += f"<div class='t' style='left:{nx}px;top:{y-16}px;font-size:{170 if i==0 else 120}px;color:{YEL if i==0 else '#fff'}'>{nums[i]}</div>"
    return s

D1E = f"""{BG}{TAG('퇴직 후 건보료')}
<div id='d1' class='t' data-fit='860' style='left:52px;top:176px;font-size:104px;color:#fff'>이자·배당 1만원 더</div>
<div id='d2' class='t' data-fit='900' style='left:40px;top:300px;font-size:250px;color:{RED}'>+54만원</div>
<div class='lab' style='left:58px;top:560px;color:#fff;font-size:34px'>1년 건보료가 이만큼</div>
{FINE('연 금융소득 1,000만→1,001만원 · 지역가입자 1인·2026년 예시')}"""
D1F = f"""{BG}{TAG('퇴직 후 건보료')}
<div id='f1' class='t' data-fit='640' style='left:52px;top:180px;font-size:110px;color:#fff'>이자·배당 1만원 차이</div>
<div id='f2' class='t' data-fit='640' style='left:44px;top:310px;font-size:200px;color:{RED}'>거의 3배</div>
{bars_v(720, 480, [22800, 67850], w=150, gap=80, hmax=330, labs=('월 2.3만', '월 6.8만'))}
{FINE('연 금융소득 1,000만원 vs 1,001만원 · 지역가입자 1인·2026년 예시')}"""
E1D = f"""{BG}{TAG('삼성전자')}
{bars_h(52, 180, [19.14, 3.27], wmax=1000, hh=150, gap=50, names=('분기 영업이익', '주가'), nums=('19배', '?'))}
<div class='lab' style='left:58px;top:536px;color:#fff;font-size:44px'>주가는 몇 배 올랐을까</div>
{FINE('영업이익: 1년 전 같은 분기 대비 · 주가: 25.9.29→26.9.29')}"""
E1E = f"""{BG}{TAG('삼성전자')}
{bars_h(52, 180, [19.14, 3.27], wmax=1000, hh=150, gap=50, names=('분기 영업이익', '주가'), nums=('19배', '3배'))}
<div class='lab' style='left:58px;top:536px;color:#fff;font-size:44px'>이익만큼 오르지 않았다</div>
{FINE('영업이익 19.14배(1년 전 같은 분기 대비) · 주가 3.27배(25.9.29→26.9.29)')}"""
D1G = f"""{BG}{TAG('퇴직 후 건보료')}
<div id='g1' class='t' data-fit='640' style='left:52px;top:176px;font-size:104px;color:#fff'>이자·배당 1만원 더</div>
<div id='g2' class='t' data-fit='640' style='left:44px;top:300px;font-size:230px;color:{RED}'><span style='color:#fff;font-size:130px'>건보료 </span>3배</div>
{bars_v(720, 470, [22800, 67850], w=150, gap=80, hmax=330, labs=('1,000만원', '1,001만원'))}
{FINE('연 금융소득 · 월 22,800원→67,850원(2.98배) · 지역가입자 1인·2026년 예시')}"""
E1F = f"""{BG}{TAG('삼성전자')}
{bars_h(52, 180, [19.14, 3.27], wmax=1000, hh=150, gap=50, names=('분기 영업이익', '주가'), nums=('19배', '3배'))}
{FINE('영업이익 19.14배(1년 전 같은 분기 대비) · 주가 3.27배(25.9.29→26.9.29)')}"""
D1H = D1G.replace(TAG('퇴직 후 건보료'), TAG('퇴직하면')).replace(
    "{FINE(", "{FINE(", 1)
D1H = D1H.replace("<div class='fine'>", "<div class='lab' style='left:700px;top:96px;color:#fff;font-size:40px'>월 2.3만 → 6.8만</div><div class='fine'>", 1)
E1G = f"""{BG}{TAG('삼성전자 · 1년 전 대비')}
{bars_h(52, 180, [19.14, 3.27], wmax=1000, hh=150, gap=50, names=('분기 영업이익', '주가'), nums=('19배', '3.3배'))}
{FINE('영업이익 19.14배(1년 전 같은 분기 대비) · 주가 3.27배(25.9.29→26.9.29)')}"""
V2 = {('D-1', 'd1e'): D1E, ('D-1', 'd1f'): D1F, ('E-1', 'e1d'): E1D, ('E-1', 'e1e'): E1E, ('D-1', 'd1g'): D1G, ('E-1', 'e1f'): E1F, ('D-1', 'd1h'): D1H, ('E-1', 'e1g'): E1G}
rep = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
    for (ep, k), body in V2.items():
        html = os.path.join(H, f'{k}.html'); open(html, 'w', encoding='utf-8').write(M.BASE % {'f': M.FONTS, 'body': body})
        pg.goto(Path(html).as_uri()); pg.wait_for_selector('body[data-ready]')
        out = os.path.join(EP, ep, f'thumb_{k}.png'); pg.screenshot(path=out); rep[k] = M.check_zones(pg)
        im = Image.open(out); im.resize((168, 95), Image.LANCZOS).save(os.path.join(H, 's168', k.upper()[:2] + k[2:] + '.png'))
        print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', rep[k] or '없음')
    b.close()
json.dump(rep, open(os.path.join(H, 'zones.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
