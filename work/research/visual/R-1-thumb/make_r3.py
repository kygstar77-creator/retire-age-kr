# R-1 29차 시안(2026-10-12 visual) — thumb-gap-1011 1위(그림이 주제를 말한다)·2위(글자 적게)·6위(돈 단위 하나) 반영, r2i 틀(글자판+가린 자릿수) 반복 안 함
# r3a: 지폐 더미 두 개(예금·SCHD, '1년 뒤 늘어난 돈' 비율 그대로) + 1등 더미 위 세금으로 빠진 칸(빗금) · 글 '세금이 줄인 차이' + '307만'
# r3b: 같은 그림, 숫자 먼저('307만' 위, '세금이 줄인 차이' 아래)
# r3c: 달러 더미 하나 + 위 한 덩이가 미끄러져 빠짐 · 글 '달러로는 올랐는데' + '−330만' + '환율로 빠진 돈'
# 숫자 출처 facts.txt [영수증]·calc2_out.txt — assert로 잰다. 오른쪽 아래(x>960·y>576)·아래 5%(y>684) 비움 assert
import os, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
# 늘어난 돈(만원): 예금 세전 2,580,000 → 세후 2,182,680 · SCHD 세전 15,728,578+3,728,285 → 세후 115,987,335−1억
dep_pre, dep_post = 2580000, 2182680
sc_pre, sc_post = 15728578 + 3728285, 115987335 - 100000000
gap_pre, gap_post = sc_pre - dep_pre, sc_post - dep_post
assert gap_pre == 16876863 and gap_post == 13804655 and round((gap_pre - gap_post) / 1e4) == 307
assert round(3300142 / 1e4) == 330
FLOOR, K = 600, 440 / (sc_pre / 1e4)          # px per 만원
h = lambda won: round(won / 1e4 * K)
CSS = """<html><head><meta charset='utf-8'><style>
@font-face{font-family:PB;src:url('file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/public/fonts/BlackHanSans.ttf')}
@font-face{font-family:PX;src:url('file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/public/fonts/pd700.ttf')}
html,body{margin:0;width:1280px;height:720px;overflow:hidden}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse at 70% 35%,#6E7F96 0%,#46546A 45%,#2B3340 100%)}
.desk{position:absolute;left:0;right:0;top:600px;bottom:0;background:linear-gradient(#1E242D,#151A21)}
.t{position:absolute;font-family:PB;line-height:1;white-space:nowrap;letter-spacing:-0.02em;text-shadow:0 4px 0 rgba(0,0,0,.45),0 0 18px rgba(0,0,0,.35)}
.l{position:absolute;font-family:PX;line-height:1;white-space:nowrap;letter-spacing:-0.02em;text-shadow:0 3px 0 rgba(0,0,0,.5)}
.st{position:absolute;box-shadow:14px 10px 24px rgba(0,0,0,.45);border-radius:3px}
.top{position:absolute;height:16px;border-radius:3px 3px 0 0}
.ghost{position:absolute;border:5px dashed #FF5A4E;background:repeating-linear-gradient(135deg,rgba(255,90,78,.38) 0 10px,rgba(255,90,78,.08) 10px 20px);box-sizing:border-box;border-radius:3px}
</style></head><body><div class='bg'></div><div class='desk'></div>"""
TAIL = """<script>
function fit(e,maxW){let s=parseFloat(getComputedStyle(e).fontSize);while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
def stack(x, w, hh, edge, line, topc, band='#F7F4EC'):
    # 지폐 다발을 쌓은 모양: 다발(약 46px)마다 살짝 어긋나고 가운데 띠지 — 168px에서 '막대'가 아니라 '돈 더미'로 읽히게
    out, y, n = '', FLOOR, 0
    while y > FLOOR - hh:
        bh = min(46, y - (FLOOR - hh)); y -= bh; dx = (-4, 3, -1, 5, -3, 2)[n % 6] if bh >= 20 else 0
        out += (f"<div class='st' style='left:{x + dx}px;top:{y}px;width:{w}px;height:{bh}px;"
                f"background:repeating-linear-gradient(to bottom,{edge} 0 3px,{line} 3px 4px)'></div>")
        if bh >= 26: out += f"<div style='position:absolute;left:{x + dx + w // 2 - 22}px;top:{y}px;width:44px;height:{bh}px;background:{band};box-shadow:inset 0 0 0 2px rgba(0,0,0,.18)'></div>"
        n += 1
    return out + f"<div class='top' style='left:{x}px;top:{FLOOR - hh - 6}px;width:{w}px;background:{topc}'></div>"
def two_stacks():
    dpo, dpr, spo, spr = h(dep_post), h(dep_pre), h(sc_post), h(sc_pre)
    s = stack(670, 130, dpo, '#F1D79A', '#B8954A', '#FBE7B5') + stack(820, 130, spo, '#CFE8D0', '#7FAE86', '#E4F4E4')
    s += f"<div class='ghost' style='left:670px;top:{FLOOR - dpr - 6}px;width:130px;height:{dpr - dpo}px'></div>"
    s += f"<div class='ghost' style='left:820px;top:{FLOOR - spr - 6}px;width:130px;height:{spr - spo}px'></div>"
    s += "<div class='l' style='left:635px;width:200px;text-align:center;top:608px;font-size:58px;color:#FBE7B5'>예금</div>"
    s += "<div class='l' style='left:800px;width:160px;text-align:center;top:608px;font-size:58px;color:#CFE8D0'>SCHD</div>"
    return s
A = two_stacks() + ("<div class='t' data-fit='610' style='left:40px;top:80px;font-size:120px;color:#FFD43B'>세금이 줄인 차이</div>"
                    "<div class='t' data-fit='600' style='left:34px;top:230px;font-size:270px;color:#fff'>307만</div>")
B = two_stacks() + ("<div class='t' data-fit='600' style='left:34px;top:60px;font-size:270px;color:#fff'>307만</div>"
                    "<div class='t' data-fit='610' style='left:40px;top:370px;font-size:120px;color:#FFD43B'>세금이 줄인 차이</div>")
C = (stack(740, 200, 380, '#CFE8D0', '#7FAE86', '#E4F4E4')
     + "<div style='position:absolute;left:770px;top:120px;width:200px;height:74px;transform:rotate(9deg);box-shadow:14px 10px 24px rgba(0,0,0,.45);"
       "background:repeating-linear-gradient(to bottom,#F3B2AA 0 3px,#C0564B 3px 4px);border-radius:3px'><div style='position:absolute;left:78px;top:0;width:44px;height:74px;background:#F7F4EC;box-shadow:inset 0 0 0 2px rgba(0,0,0,.18)'></div></div>"
     + "<div class='t' data-fit='660' style='left:40px;top:70px;font-size:120px;color:#FFD43B'>달러로는 올랐는데</div>"
       "<div class='t' data-fit='660' style='left:34px;top:200px;font-size:270px;color:#fff'>-330만</div>"
       "<div class='t' data-fit='660' style='left:40px;top:470px;font-size:110px;color:#fff'>환율로 빠진 돈</div>")

# ── 30차(같은 날): 29차 심사 반영 — ① 차이의 주체(예금·SCHD)를 글 안에 ② 빗금 = SCHD 세금(347만)으로 오독 → 두 꼭대기 사이 '간격' 자로 다시 그림(세후 간격 1,380만 흰 자 + 세금이 줄인 307만 빨간 빗금)
#    ③ 더미를 키움(520px) ④ 바탕 대비 키움(남색) ⑤ 라벨 떼어 놓기. 대본 13행 말 '간격'
K2 = 520 / (sc_pre / 1e4); h2 = lambda won: round(won / 1e4 * K2)
def art30(labels=True):
    dpo, spo, cut = h2(dep_post), h2(sc_post), h2(gap_pre - gap_post)
    s = stack(600, 140, dpo, '#F1D79A', '#B8954A', '#FBE7B5') + stack(812, 140, spo, '#CFE8D0', '#7FAE86', '#E4F4E4')
    top_s, top_d = FLOOR - spo - 6, FLOOR - dpo - 6
    s += f"<div style='position:absolute;left:600px;top:{top_d}px;width:350px;border-top:4px dashed rgba(255,255,255,.7)'></div>"
    s += f"<div style='position:absolute;left:962px;top:{top_s}px;width:8px;height:{top_d - top_s}px;background:#fff'></div>"
    s += f"<div class='ghost' style='left:949px;top:{top_s - cut}px;width:34px;height:{cut}px;border-width:4px'></div>"
    if labels:
        s += "<div class='l' style='left:580px;width:180px;text-align:center;top:608px;font-size:58px;color:#FBE7B5'>예금</div>"
        s += "<div class='l' style='left:800px;width:160px;text-align:center;top:608px;font-size:58px;color:#CFE8D0'>SCHD</div>"
    return s
BG30 = "<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 72% 30%,#4F6FA8 0%,#2A3F66 50%,#141E33 100%)'></div><div class='desk'></div>"
D = BG30 + art30() + ("<div class='t' data-fit='560' style='left:40px;top:80px;font-size:120px;color:#FFD43B'>세금이 줄인 간격</div>"
                      "<div class='t' data-fit='560' style='left:34px;top:230px;font-size:270px;color:#fff'>307만</div>")
E = BG30 + art30(False) + ("<div class='t' data-fit='560' style='left:40px;top:70px;font-size:120px'><span style='color:#FBE7B5'>예금</span><span style='color:#fff'>↔</span><span style='color:#9FE0A8'>SCHD</span></div>"
                           "<div class='t' data-fit='560' style='left:34px;top:210px;font-size:270px;color:#fff'>307만</div>"
                           "<div class='t' data-fit='530' style='left:40px;top:480px;font-size:96px;color:#FFD43B'>세금이 줄인 간격</div>")

# ── 31차: 30차 레드팀 — 노랑 빼기(경쟁 유사 3→2), '간격=307만' 오독 막기(숫자 옆에 '줄었다'/−), 자·빗금 2~3배 굵게, 보조 줄은 덜 꾸민 서체(pd700)
def art31():
    s = art30()
    dpo, spo, cut = h2(dep_post), h2(sc_post), h2(gap_pre - gap_post); top_s, top_d = FLOOR - spo - 6, FLOOR - dpo - 6
    s += f"<div style='position:absolute;left:958px;top:{top_s}px;width:16px;height:{top_d - top_s}px;background:#fff;box-shadow:0 0 0 3px rgba(0,0,0,.35)'></div>"
    s += f"<div class='ghost' style='left:946px;top:{top_s - cut}px;width:40px;height:{cut}px;border-width:5px;background:repeating-linear-gradient(135deg,rgba(255,90,78,.85) 0 10px,rgba(255,90,78,.35) 10px 20px)'></div>"
    return s
F = BG30 + art31() + ("<div class='l' data-fit='560' style='left:44px;top:84px;font-size:96px;color:#8FF0CF'>세금 뒤 간격</div>"
                      "<div class='t' data-fit='570' style='left:30px;top:210px;font-size:250px;color:#fff'>-307만</div>"
                      "<div class='l' data-fit='540' style='left:44px;top:470px;font-size:80px;color:#fff'>예금과 SCHD 사이</div>")
G = BG30 + art31() + ("<div class='l' data-fit='560' style='left:44px;top:84px;font-size:92px;color:#8FF0CF'>예금↔SCHD 간격</div>"
                      "<div class='t' data-fit='570' style='left:30px;top:200px;font-size:230px;color:#fff'>307만</div>"
                      "<div class='t' data-fit='540' style='left:44px;top:440px;font-size:120px;color:#FF7A6E'>줄었다</div>")

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
    for k, body in [(k, v) for k, v in (('r3a', A), ('r3b', B), ('r3c', C), ('r3d', D), ('r3e', E), ('r3f', F), ('r3g', G)) if len(sys.argv) < 2 or k in sys.argv[1].split(',')]:
        f = os.path.join(H, 'r29', k + '.html'); open(f, 'w', encoding='utf-8').write(CSS + body + TAIL)
        pg.goto(pathlib.Path(f).as_uri()); pg.wait_for_selector('body[data-ready]')
        boxes = pg.eval_on_selector_all('.t,.l,.st,.ghost', "es=>es.map(e=>{const r=e.getBoundingClientRect();return [e.textContent,r.left,r.top,r.right,r.bottom]})")
        for t, l, tp, r, bt in boxes:
            assert not (r > 960 and bt > 576), (k, t, 'duration zone'); assert bt <= 684, (k, t, 'bottom 5%'); assert r <= 1270 and tp >= 0, (k, t, 'edge')
        out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
        im = Image.open(out).convert('L'); px = list(im.getdata()); m = sum(px) / len(px)
        sd = (sum((v - m) ** 2 for v in px) / len(px)) ** .5; dark = sum(v < 40 for v in px) / len(px)
        print(k, 'mean', round(m), 'sd', round(sd), 'dark<40', f'{dark:.0%}')
    b.close()
