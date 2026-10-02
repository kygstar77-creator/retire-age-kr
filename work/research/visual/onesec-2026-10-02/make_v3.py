# D-1 썸네일 3차(10/02 15:1x visual, 순돌이 13:2x 결정) — d1k에 GPT 웹·레드팀 고칠 점 반영 새 안 2(d1n·d1o) + d1l 수정 1(d1p)
#   py -3.12 make_v3.py → ep/D-1/thumb_d1n·d1o·d1p.png + s168 + board6_d1knop.png(우리 4 + 경쟁 5, 168px) + board4_<k>.png(제미나이용)
# 고칠 점 출처
#   GPT 웹(gpt_web_d1klm.md): d1k '월 건보료'·막대 숫자 라벨 키우기 / d1l '건보료'↔'약 3배' 크기 차 벌리기·막대 대비 강화
#   레드팀(onesec-2026-10-02.md 68행): ① 경쟁 겹침(어두운 남색 바탕+빨간 큰 숫자, 테두리 글씨) ② '1만원 차이'가 제목 반복 ③ 전제 잔글씨
#   제미나이 lite(gemini_d1k_score.md): '3배' 더 크게
# 숫자: facts.txt [계산] 월 22,800원(1,000만원) → 67,850원(1,001만원), 2.98배('약 3배')
import os, sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(H)
sys.path.insert(0, os.path.join(V, 'E-1-thumb'))
import make_thumbs as M
EP = os.path.join(V, '..', 'longform', 'ep')
assert round(67850 / 22800, 2) == 2.98
RED, YEL, GRY = '#FF4D4F', '#FFD60A', '#6B7385'
FINE = "<div class='fine'>예시: 지역가입자 1인·재산 0·다른 소득 0 · 월 22,800원→67,850원(2.98배) · 2026년</div>"
# 경쟁(남색 방사 그라데이션)과 다른 무채색 숯 바탕
COAL = "<div style='position:absolute;inset:0;background:#15161A'></div>"

def bars_big(x0=690, base=468, w=210, gap=60, hmax=300, lab_col=YEL):
    """GPT 고칠 점: '월 건보료'·막대 숫자·아래 라벨 키움"""
    s = f"<div class='t' style='left:{x0}px;top:44px;font-size:64px;color:{lab_col}'>월 건보료</div>"
    for i, (v, c, top, bot) in enumerate(((22800, GRY, '2.3만', '1,000만'), (67850, RED, '6.8만', '1,001만'))):
        h = v / 67850 * hmax; x = x0 + i * (w + gap)
        s += f"<div style='position:absolute;left:{x}px;top:{base-h}px;width:{w}px;height:{h}px;background:{c};border-radius:12px 12px 0 0'></div>"
        s += f"<div class='t' style='left:{x-30}px;top:{base-h-100}px;width:{w+60}px;text-align:center;font-size:92px;color:{YEL if i else '#fff'}'>{top}</div>"
        s += f"<div class='t' style='left:{x-40}px;top:{base+8}px;width:{w+80}px;text-align:center;color:#fff;font-size:64px'>{bot}</div>"
    return s

# d1n: d1k + '1만원 차이'(제목 반복) → '1,000만 넘으면' · 숯 바탕 · 큰 숫자는 테두리 글씨 대신 빨간 상자 속 흰 글씨
D1N = f"""{COAL}
<div id='n1' class='t' data-fit='600' style='left:52px;top:60px;font-size:96px;color:#fff'>이자·배당</div>
<div id='n2' class='t' data-fit='600' style='left:52px;top:170px;font-size:112px;color:{YEL}'>1,000만 넘으면</div>
<div id='n3' class='t' style='left:52px;top:300px;font-size:100px;color:#fff'>건보료</div>
<div style='position:absolute;left:40px;top:392px;background:{RED};border-radius:18px;padding:4px 28px 10px'>
 <div id='n4' data-fit='560' style='font:178px BH;color:#fff;line-height:1;white-space:nowrap'><span style='font-size:110px'>약 </span>3배</div></div>
{bars_big()}
{FINE}"""

# d1o: d1k + 내 돈 대입 질문('내 이자·배당 1,000만 넘으면?') · 노란 형광펜 띠 · 숯 바탕 · '약 3배' 더 크게
D1O = f"""{COAL}
<div id='o1' class='t' data-fit='600' style='left:52px;top:60px;font-size:92px;color:#fff'>내 이자·배당</div>
<div style='position:absolute;left:40px;top:168px;width:600px;height:118px;background:{YEL};border-radius:10px'></div>
<div id='o2' data-fit='580' style='position:absolute;left:58px;top:176px;font:104px BH;color:#111;line-height:1;white-space:nowrap'>1,000만 넘으면?</div>
<div id='o3' class='t' style='left:52px;top:318px;font-size:96px;color:#fff'>건보료</div>
<div id='o4' class='t' data-fit='620' style='left:40px;top:400px;font-size:230px;color:{RED}'><span style='color:#fff;font-size:110px'>약 </span>3배</div>
{bars_big()}
{FINE}"""

# d1p: d1l 수정 — GPT '건보료↔약 3배 크기 차 벌리기·막대/2.3만·6.8만 대비 강화' + lite '연 이자·배당 작다'
PAPER = "<div style='position:absolute;inset:0;background:#F4F0E6'></div><style>.t{text-shadow:none!important}.fine{color:#5B6070!important}</style>"
def bars_p(x0=740, base=476, w=190, gap=50, hmax=330):
    s = "<div class='t' style='left:740px;top:44px;font-size:56px;color:#14161C'>월 건보료</div>"
    for i, (v, c, top, bot) in enumerate(((22800, '#7D828E', '2.3만', '1,000만'), (67850, '#E5383B', '6.8만', '1,001만'))):
        h = v / 67850 * hmax; x = x0 + i * (w + gap)
        s += f"<div style='position:absolute;left:{x}px;top:{base-h}px;width:{w}px;height:{h}px;background:{c};border-radius:10px 10px 0 0'></div>"
        s += f"<div class='t' style='left:{x-30}px;top:{base-h-84}px;width:{w+60}px;text-align:center;font-size:76px;color:{'#E5383B' if i else '#14161C'}'>{top}</div>"
        s += f"<div class='t' style='left:{x-30}px;top:{base+10}px;width:{w+60}px;text-align:center;font-size:56px;color:#14161C'>{bot}</div>"
    return s
D1P = f"""{PAPER}
<div class='t' style='left:56px;top:50px;font-size:60px;color:#5B6070'>연 이자·배당</div>
<div id='p1' class='t' data-fit='650' style='left:52px;top:122px;font-size:112px;color:#14161C'>1,000만<span style='font:700 96px PD;color:#E5383B;margin:0 10px'>→</span>1,001만</div>
<div id='p2' class='t' style='left:56px;top:270px;font-size:88px;color:#14161C'>건보료</div>
<div id='p3' class='t' data-fit='660' style='left:40px;top:350px;font-size:260px;color:#E5383B'><span style='color:#14161C;font-size:110px'>약 </span>3배</div>
{bars_p()}
{FINE}"""

V3 = {'d1n': D1N, 'd1o': D1O, 'd1p': D1P}
rep = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
    for k, body in V3.items():
        html = os.path.join(H, f'{k}.html'); open(html, 'w', encoding='utf-8').write(M.BASE % {'f': M.FONTS, 'body': body})
        pg.goto(Path(html).as_uri()); pg.wait_for_selector('body[data-ready]')
        out = os.path.join(EP, 'D-1', f'thumb_{k}.png'); pg.screenshot(path=out); rep[k] = M.check_zones(pg)
        Image.open(out).resize((168, 95), Image.LANCZOS).save(os.path.join(H, 's168', 'D1' + k[2:] + '.png'))
        print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', rep[k] or '없음')
    b.close()
z = json.load(open(os.path.join(H, 'zones.json'), encoding='utf-8')); z.update(rep)
json.dump(z, open(os.path.join(H, 'zones.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 비교판: board5와 같은 방식(168px, 경쟁 5 = D-1-thumb/compare.json 앞 5개)
W, HH = 168, 95; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
D1C = [c['id'] for c in json.load(open(os.path.join(V, 'D-1-thumb', 'compare.json'), encoding='utf-8')) if c['who'] == '경쟁'][:5]
def small(pth):
    im = Image.open(pth).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, HH), Image.LANCZOS)
def board(ours, name, cols):
    items = [(f'우리 {t.upper()}', os.path.join(EP, 'D-1', f'thumb_{t}.png')) for t in ours] + \
            [(f'경쟁 {i+1}', os.path.join(V, 'D-1-thumb', 'src', k + '.jpg')) for i, k in enumerate(D1C)]
    pad = 12; rows = -(-len(items) // cols)
    bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 30) + pad), 'white'); d = ImageDraw.Draw(bd)
    for n, (lab, pth) in enumerate(items):
        x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 30); bd.paste(small(pth), (x, y)); d.text((x, y + HH + 4), lab, fill='black', font=F)
    bd.save(os.path.join(H, name)); return bd.size
print('board6', board(('d1k', 'd1n', 'd1o', 'd1p'), 'board6_d1knop.png', 5), D1C)
for k in ('d1k', 'd1n', 'd1o', 'd1p'):  # 제미나이 judge_flash.py용(시안 1 + 경쟁 5)
    board((k,), f'board4_{k}.png', 3)
