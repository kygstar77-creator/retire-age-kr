# A-1 썸네일 v5 시안 3개(캐릭터 없음, 2026-10-01 visual) — py -3.12 make_thumbs.py
# 숫자 출처: ep/A-1/facts.txt [9](1억·1년, 환율 변동 제외, 미국 원천징수 15%) · [17](분배 12%·4%)
#   JEPQ 세후 분배금 1,005만 + 평가 차익 674만 = +1,679만 → 1억 1,679만
#   SCHD 세후 분배금   330만 + 평가 차익 2,132만 = +2,462만 → 1억 2,462만   · 차이 783만
# 문구: 카피라이터 ep/A-1/titles.md 1위(v5a·v5c) · 2위(v5b). 캐릭터·인물 없음(사장님 결정).
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576(길이 표시)과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표로 자동 검사.
import os, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'A-1')
FONTS = os.path.join(ROOT, 'work', 'video', 'public', 'fonts').replace('\\', '/')

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
@font-face{font-family:PD;src:url('file:///%(f)s/pd500.ttf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1280px;height:720px;overflow:hidden;position:relative;font-family:PD}
.t{position:absolute;font-family:BH;white-space:nowrap;line-height:1;
   -webkit-text-stroke:0;paint-order:stroke fill;text-shadow:0 0 0 #000,
   5px 5px 0 #000,-5px 5px 0 #000,5px -5px 0 #000,-5px -5px 0 #000,0 7px 0 #000,0 -6px 0 #000,7px 0 0 #000,-7px 0 0 #000}
.y{color:#FFD60A}.w{color:#fff}
.fine{position:absolute;left:52px;top:596px;font:500 25px PD;color:#9AA3B2}
</style></head><body>%(body)s
<script>
function fit(id,maxW){const e=document.getElementById(id);let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e.id,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""

DARK = "<div style='position:absolute;left:0;top:0;width:1280px;height:720px;background:linear-gradient(180deg,rgba(14,16,22,0) 0%%,rgba(14,16,22,0) %d%%,rgba(14,16,22,.94) %d%%,#0E1016 100%%)'></div>"
FINE = "<div class='fine'>1억씩·1년(25.9.26→26.9.28) · 미국 배당세 15%만 · 팔지 않은 평가액 · 환율 제외</div>"

def hbar(y, name, color, tint, dist, gain, total, scale):
    wd, wg = dist * scale, gain * scale
    return f"""
<div style='position:absolute;left:52px;top:{y}px;width:176px;height:84px;border-radius:14px;background:{color};
 color:#fff;font:52px BH;display:flex;align-items:center;justify-content:center'>{name}</div>
<div style='position:absolute;left:244px;top:{y}px;height:84px;width:{wd}px;background:{color};border-radius:12px 0 0 12px;
 color:#fff;font:700 26px PD;display:flex;align-items:center;justify-content:center;white-space:nowrap;overflow:hidden'>분배금</div>
<div style='position:absolute;left:{244+wd}px;top:{y}px;height:84px;width:{wg}px;background:{tint};border-radius:0 12px 12px 0;
 color:#1b1b1b;font:700 26px PD;display:flex;align-items:center;justify-content:center;white-space:nowrap;overflow:hidden'>{'주가 오른 몫' if wg>150 else '주가'}</div>
<div style='position:absolute;left:{244+wd+wg+14}px;top:{y+8}px;font:62px BH;color:#15171c'>{total}</div>"""

# v5a — 1위 문구 + 가로 누적 막대(늘어난 돈, 0부터 시작)
SC = 700 / 2462
v5a = f"""<div style='position:absolute;inset:0;background:#F3EEE5'></div>
<div style='position:absolute;left:52px;top:26px;font:700 34px PD;color:#3b3f47'>1억 넣고 1년, <b style='color:#15171c'>늘어난 돈</b></div>
{hbar(70, 'JEPQ', '#E8620C', '#F6B98C', 1005, 674, '+1,679만', SC)}
{hbar(166, 'SCHD', '#1F5FD1', '#9DB9EE', 330, 2132, '+2,462만', SC)}
{DARK % (37, 41)}
<div id='a1' class='t y' data-fit='1176' style='left:52px;top:284px;font-size:96px'>JEPQ 분배금 12%인데</div>
<div id='a2' class='t w' data-fit='1180' style='left:46px;top:392px;font-size:172px'>783만원 덜 남았다</div>{FINE}"""

# v5b — 2위 문구 + '거꾸로' 세로 막대 두 쌍(분배금 ↔ 늘어난 돈)
def vpair(x, title, a, b, amax, la, lb):
    H = 150; ha, hb = a / amax * H, b / amax * H
    return f"""
<div style='position:absolute;left:{x}px;top:14px;width:380px;text-align:center;font:700 34px PD;color:#15171c'>{title}</div>
<div style='position:absolute;left:{x+40}px;top:{268-ha}px;width:130px;height:{ha}px;background:#E8620C;border-radius:10px 10px 0 0'></div>
<div style='position:absolute;left:{x+210}px;top:{268-hb}px;width:130px;height:{hb}px;background:#1F5FD1;border-radius:10px 10px 0 0'></div>
<div style='position:absolute;left:{x-5}px;top:{268-ha-48}px;width:220px;text-align:center;font:42px BH;white-space:nowrap;color:#15171c'>{la}</div>
<div style='position:absolute;left:{x+165}px;top:{268-hb-48}px;width:220px;text-align:center;font:42px BH;white-space:nowrap;color:#15171c'>{lb}</div>
<div style='position:absolute;left:{x}px;top:268px;width:380px;height:4px;background:#15171c'></div>
<div style='position:absolute;left:{x+40}px;top:276px;width:130px;text-align:center;font:30px BH;color:#E8620C'>JEPQ</div>
<div style='position:absolute;left:{x+210}px;top:276px;width:130px;text-align:center;font:30px BH;color:#1F5FD1'>SCHD</div>"""
v5b = f"""<div style='position:absolute;inset:0;background:#F3EEE5'></div>
{vpair(90, '1년 분배율', 11.82, 3.88, 11.82, '12%', '4%')}
<div style='position:absolute;left:560px;top:120px;width:160px;text-align:center;font:110px BH;color:#15171c'>→</div>
{vpair(810, '1억이 늘어난 돈', 1679, 2462, 2462, '+1,679만', '+2,462만')}
{DARK % (42, 46)}
<div id='b1' class='t y' data-fit='1176' style='left:52px;top:326px;font-size:96px'>JEPQ 12% vs SCHD 4%</div>
<div id='b2' class='t w' data-fit='1176' style='left:48px;top:428px;font-size:140px'>남은 돈은 거꾸로</div>{FINE}"""

# v5c — X-THUMB-2 비교군(한 줄 큰 숫자): 어두운 바탕 + 783만원 한 덩이
v5c = f"""<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 30% 35%,#1f2a44 0%,#0E1016 70%)'></div>
<div style='position:absolute;left:52px;top:40px;display:flex;gap:14px;align-items:center'>
 <span style='background:#E8620C;color:#fff;font:52px BH;padding:10px 22px;border-radius:12px'>JEPQ</span>
 <span style='color:#fff;font:44px BH'>분배금 12%인데</span></div>
<div id='c1' class='t y' data-fit='1176' style='left:40px;top:128px;font-size:280px'>783만원</div>
<div style='position:absolute;left:52px;top:402px;font:44px BH;color:#fff'>1년 뒤 <span style='color:#F6B98C'>JEPQ +1,679만</span> · <span style='color:#9DB9EE'>SCHD +2,462만</span></div>
<div style='position:absolute;left:52px;top:470px;display:flex;gap:12px;align-items:center'>
 <span style='background:#1F5FD1;color:#fff;font:60px BH;padding:8px 22px;border-radius:12px'>SCHD</span>
 <span style='color:#fff;font:80px BH'>보다 덜 남았다</span></div>{FINE}"""

VARIANTS = {'v5a': v5a, 'v5b': v5b, 'v5c': v5c}

def check_zones(page):
    # 글자·도형 요소 중 금지 구역에 걸친 것(배경·그라데이션 제외)
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()))return;
      const r=e.getBoundingClientRect();
      if((r.right>960&&r.bottom>576)||r.bottom>684)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(r.right)+','+Math.round(r.bottom));});return bad}""")

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
            d.rounded_rectangle((1160, 668, 1268, 704), 6, fill=(0, 0, 0, 220))  # 길이 표시 모의
            Image.alpha_composite(g, ov).convert('RGB').save(os.path.join(HERE, f'{k}_guides.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(os.path.join(HERE, 'zones.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
