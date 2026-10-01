# D-1 건보료 썸네일 시안 3개(캐릭터·로고·인물 없음, 2026-10-01 21시 visual) — py -3.12 make_thumbs.py
# 숫자 출처: ep/D-1/facts.txt [계산] 지역가입자 1인·재산 0·다른 소득 0·2026년
#   연 금융소득 1,000만원 → 월 22,800원(약 2.3만원, 하한) · 1,001만원 → 월 67,850원(약 6.8만원) · 연 540,600원(약 54만원) 차이
#   (brief.md 1번 '1,000만원 → 0원'은 틀림 — 하한 때문에 0원이 아니다, today.md 주의 줄)
# 문구: 카피라이터 ep/D-1/titles.md 3장 — 1위(X-THUMB-2 B 한 줄 큰 숫자) '1년에 54만원 차이', 2위(A 두 줄) '배당·이자 +1만원 / 건보료 월 2.3만 → 6.8만'
# 실험: X-THUMB-1 A(캐릭터 없음) · d1a·d1b = X-THUMB-2 B, d1c = X-THUMB-2 A(48시간 교체용)
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576(길이 표시)과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표로 자동 검사.
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'D-1')
FONTS = os.path.join(ROOT, 'work', 'video', 'public', 'fonts').replace('\\', '/')

# 사실표에서 숫자를 읽고 확인(바뀌면 멈춘다)
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
LO = int(re.search(r'연 금융소득 1,000만원:.*?= ([\d,]+)원', facts).group(1).replace(',', ''))
HI = int(re.search(r'연 금융소득 1,001만원:.*?= ([\d,]+)원', facts).group(1).replace(',', ''))
YR = int(re.search(r'1,000만원 → 1,001만원: 월 [\d,]+원 더 \(약 [\d.]+만원\), 연 ([\d,]+)원', facts).group(1).replace(',', ''))
assert (LO, HI, YR) == (22800, 67850, 540600), (LO, HI, YR)
assert (HI - LO) * 12 == YR
M = lambda v: f'{round(v / 10000, 1):g}만원'   # 22,800 → 2.3만원
LOs, HIs, YRs = M(LO), M(HI), f'{round(YR / 10000):d}만원'
assert (LOs, HIs, YRs) == ('2.3만원', '6.8만원', '54만원')
RED, YEL, WH = '#FF4D4F', '#FFD60A', '#FFFFFF'

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
@font-face{font-family:PD;src:url('file:///%(f)s/pd500.ttf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1280px;height:720px;overflow:hidden;position:relative;font-family:PD;background:#0E1016}
.t{position:absolute;font-family:BH;white-space:nowrap;line-height:1;text-shadow:
   5px 5px 0 #000,-5px 5px 0 #000,5px -5px 0 #000,-5px -5px 0 #000,0 7px 0 #000,0 -6px 0 #000,7px 0 0 #000,-7px 0 0 #000}
.lab{position:absolute;font:700 30px PD;color:#C9D1DE;white-space:nowrap}
.tag{position:absolute;background:%(yel)s;color:#111;font:50px BH;padding:10px 22px 12px;border-radius:12px;white-space:nowrap}
.fine{position:absolute;left:52px;top:632px;font:500 24px PD;color:#8A93A3;white-space:nowrap}
.card{position:absolute;border-radius:22px;background:#171B26}
</style></head><body>%(body)s
<script>
function fit(id,maxW){const e=document.getElementById(id);let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e.id,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
FINE = "<div class='fine'>예시: 지역가입자·재산 0·다른 소득 0·2026년 · 건강보험법 시행규칙 44조</div>"
BG = "<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 70% 15%,#1d2438 0%,#0E1016 65%)'></div>"

# d1a — B(한 줄 큰 숫자, titles 1위): 위 경계 두 칸 + 아래 '1년에 54만원 차이'
d1a = f"""{BG}
<div class='tag' style='left:48px;top:34px'>퇴직 후 건보료</div>
<div class='lab' style='left:390px;top:50px;color:#fff;font-size:34px'>배당·이자 1년 합계가</div>
<div class='card' style='left:48px;top:128px;width:470px;height:290px;border:4px solid #3a4258'></div>
<div class='t' style='left:84px;top:156px;font-size:64px;color:{WH}'>1,000만원</div>
<div class='lab' style='left:88px;top:246px;font-size:30px'>건보료(월)</div>
<div id='a1' class='t' data-fit='400' style='left:80px;top:296px;font-size:100px;color:{WH}'>{LOs}</div>
<div class='t' style='left:542px;top:226px;font-size:56px;color:{YEL}'>+1만원</div>
<div class='t' style='left:596px;top:296px;font-size:80px;color:{YEL}'>→</div>
<div class='card' style='left:762px;top:128px;width:470px;height:290px;border:5px solid {RED};background:#2a1418'></div>
<div class='t' style='left:798px;top:156px;font-size:64px;color:{WH}'>1,001만원</div>
<div class='lab' style='left:802px;top:246px;font-size:30px'>건보료(월)</div>
<div id='a2' class='t' data-fit='400' style='left:794px;top:296px;font-size:100px;color:{RED}'>{HIs}</div>
<div id='a3' class='t' data-fit='890' style='left:44px;top:448px;font-size:170px;color:{WH}'>1년에 <span style='color:{YEL}'>{YRs}</span> 차이</div>
{FINE}"""

# d1b — B 극단(x343 틀): 숫자 하나가 주인공, 경계는 작은 한 줄
d1b = f"""<div style='position:absolute;inset:0;background:#0B0C10'></div>
<div class='tag' style='left:48px;top:34px'>퇴직 후 건보료</div>
<div id='b0' class='t' data-fit='1180' style='left:48px;top:128px;font-size:64px;color:{WH}'>배당·이자 <span style='color:{YEL}'>딱 1만원</span> 더 받았을 뿐인데</div>
<div id='b1' class='t' data-fit='1180' style='left:40px;top:226px;font-size:270px;color:{RED}'>건보료 1년 +{YRs}</div>
<div id='b2' class='t' data-fit='880' style='left:52px;top:520px;font-size:56px;color:{WH}'>연 1,000만원 월 {LOs} → 연 1,001만원 월 {HIs}</div>
{FINE}"""

# d1c — A(두 줄 대비, titles 2위 = 교체용): 왼쪽 두 줄, 오른쪽 0원부터 막대 두 개(비율 그대로)
BAR_H = 316; BASE_Y = 410
hl, hh = round(BAR_H * LO / HI), BAR_H
d1c = f"""{BG}
<div class='t' style='left:836px;top:{BASE_Y-hl-64}px;font-size:52px;color:#fff'>{LOs}</div>
<div class='t' style='left:1046px;top:{BASE_Y-hh-64}px;font-size:52px;color:{RED}'>{HIs}</div>
<div class='tag' style='left:48px;top:34px'>퇴직 후 건보료</div>
<div id='c0' class='t' data-fit='640' style='left:48px;top:150px;font-size:96px;color:{YEL}'>배당·이자</div>
<div id='c1' class='t' data-fit='640' style='left:48px;top:262px;font-size:140px;color:{YEL}'>+1만원</div>
<div id='c2' class='t' data-fit='890' style='left:44px;top:476px;font-size:118px;color:{WH}'>건보료 월 2.3만 → <span style='color:{RED}'>6.8만</span></div>
<div style='position:absolute;left:800px;top:{BASE_Y}px;width:430px;height:4px;background:#5a6378'></div>
<div style='position:absolute;left:840px;top:{BASE_Y-hl}px;width:150px;height:{hl}px;background:#C9D1DE;border-radius:10px 10px 0 0'></div>
<div style='position:absolute;left:1050px;top:{BASE_Y-hh}px;width:150px;height:{hh}px;background:{RED};border-radius:10px 10px 0 0'></div>
<div class='lab' style='left:848px;top:{BASE_Y+10}px;font-size:34px'>1,000만원</div>
<div class='lab' style='left:1058px;top:{BASE_Y+10}px;font-size:34px;color:#fff'>1,001만원</div>
{FINE}"""


# d1d — d1c 막대(심사 1위 그림) + titles 1위 한 줄 '1년에 54만원 차이' = X-THUMB-2 B
d1d = d1c.split("<div id='c0'")[0] + f"""
<div id='d0' class='t' data-fit='700' style='left:48px;top:150px;font-size:84px;color:{WH}'>배당·이자 연 합계</div>
<div id='d1' class='t' data-fit='700' style='left:48px;top:254px;font-size:120px;color:{YEL}'>딱 +1만원</div>
<div id='d2' class='t' data-fit='890' style='left:44px;top:476px;font-size:150px;color:{WH}'>건보료 1년 <span style='color:{RED}'>{YRs}</span> 차이</div>
<div style='position:absolute;left:800px;top:{BASE_Y}px;width:430px;height:4px;background:#5a6378'></div>
<div style='position:absolute;left:840px;top:{BASE_Y-hl}px;width:150px;height:{hl}px;background:#C9D1DE;border-radius:10px 10px 0 0'></div>
<div style='position:absolute;left:1050px;top:{BASE_Y-hh}px;width:150px;height:{hh}px;background:{RED};border-radius:10px 10px 0 0'></div>
<div class='lab' style='left:848px;top:{BASE_Y+10}px;font-size:34px'>1,000만원</div>
<div class='lab' style='left:1058px;top:{BASE_Y+10}px;font-size:34px;color:#fff'>1,001만원</div>
{FINE}"""

VARIANTS = {'d1a': d1a, 'd1b': d1b, 'd1c': d1c, 'd1d': d1d}

def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")

def main():
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k, body in VARIANTS.items():
            html = os.path.join(HERE, f'{k}.html')
            open(html, 'w', encoding='utf-8').write(BASE % {'f': FONTS, 'body': body, 'yel': YEL})
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
