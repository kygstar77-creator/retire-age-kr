# 계산기 3종 공유 이미지(og) 시안 — 비주얼 디자이너 2026-10-01 · py -3.12 make_og.py
# 문구: src/firemap-v2/toolPages.js seoTitle을 ' — '에서 나눠 그대로(짓지 않음). 카드 라벨은 같은 파일 sections의 결과 라벨 그대로.
# 색: 웹 토큰 #f6f7f9 바탕 · #fff 카드 · #18191d 잉크 · 주황 #ff5a00(불꽃·행동 하나만) · 다크 카드 #18191d 1장(B만).
# 로고: 운영 og-image.svg(v9)의 불꽃 path 그대로 + '파이어맵' 글자.
# C = A + 레드팀 r1(알약 삭제·다크 카드 1장·주황 '몇 살' 하나·화면 원문 질문 줄) — 운영 후보.
# A = 가운데 630px 안에 전부(정사각 미리보기로 잘려도 제목·부제가 남음), B = 왼쪽 글 + 오른쪽 결과 다크 카드(화면 그대로의 약속).
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
FONT = os.path.join(ROOT, 'public', 'fonts', 'PretendardVariable.woff2').replace('\\', '/')

src = open(os.path.join(ROOT, 'src', 'firemap-v2', 'toolPages.js'), encoding='utf-8').read()
def seo(path):
    i = src.index(f"path: '{path}'"); j = src.index("seoTitle: '", i) + 11
    t = src[j:src.index("'", j)]; a, b = t.split(' — ')
    return a, b
CALC = {
    'salary': (*seo('/calc/salary'), '월 실수령액', 'firemap.kr/calc/salary'),
    'severance': (*seo('/calc/severance'), '예상 퇴직금', 'firemap.kr/calc/severance'),
    'unemployment': (*seo('/calc/unemployment-benefit'), '예상 실업급여 총액', 'firemap.kr/calc/unemployment-benefit'),
}
# c안 질문 줄: 각 화면 결과 아래 문장 원문(레드팀 r1 — b안 버튼 문구가 퇴직금·실업급여 화면과 달랐다)
CJSX = os.path.join(ROOT, 'src', 'components', 'firemap')
ASKQ = {'salary': ('SalaryCalc.jsx', '이 돈이면 몇 살에 은퇴?'), 'severance': ('SeveranceCalc.jsx', '이 돈이면 몇 살에 은퇴?'),
        'unemployment': ('UnemploymentCalc.jsx', '재취업 뒤, 몇 살에 은퇴할 수 있을까?')}
for k, (f, q) in ASKQ.items():
    assert q in open(os.path.join(CJSX, f), encoding='utf-8').read(), (k, q)
import re
def nb(x):  # '4대보험·소득세'처럼 가운뎃점 묶음은 줄 첫머리에 점이 오지 않게 한 덩이로
    return ' '.join(f"<span style='white-space:nowrap'>{w}</span>" if '·' in w else w for w in x.split(' '))
for k, (_, _, lab, _) in CALC.items():  # 카드 라벨이 운영 sections에 그대로 있는지
    assert lab in src, (k, lab)
assert '이 돈이면 몇 살에 은퇴?' in src

FLAME = """<svg viewBox="188 84 136 276" width="%(w)d" height="%(h)d"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>"""
def logo(size):
    return f"<div class='logo' style='font-size:{size}px'>{FLAME % {'w': size*0.62, 'h': size*1.25}}<span>파이어맵</span></div>"

CSS = f"""@font-face{{font-family:PD;src:url('file:///{FONT}') format('woff2');font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;position:relative;font-family:PD;background:#f6f7f9;color:#18191d;letter-spacing:-0.02em;word-break:keep-all}}
.logo{{display:flex;align-items:center;gap:.3em;font-weight:800}}
.logo svg{{display:block}}
.sub{{color:#4e5562;font-weight:600}}
.url{{display:inline-block;background:#ff5a00;color:#fff;font-weight:700;border-radius:999px}}"""

def page_a(t, s, lab, url):
    # 제목을 띄어쓰기에서 두 줄로 — 가운데 630px 안에 다 들어가 정사각으로 잘려도 남는다
    t2 = '<br>'.join(t.split(' '))
    return f"""<div style='position:absolute;left:300px;width:600px;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center'>
{logo(38)}
<div id='T' style='margin-top:30px;font-weight:800;font-size:128px;line-height:1.04;white-space:nowrap'>{t2}</div>
<div id='S' class='sub' style='margin-top:24px;font-size:36px;line-height:1.3;text-wrap:balance'>{s}</div>
<div class='url' style='margin-top:30px;font-size:30px;padding:12px 32px'>firemap.kr →</div></div>"""

def page_b(t, s, lab, url):
    return f"""<div style='position:absolute;left:72px;top:64px;width:560px;bottom:64px;display:flex;flex-direction:column'>
{logo(38)}
<div id='T' style='margin-top:auto;font-weight:800;font-size:96px;line-height:1.05;white-space:nowrap'>{t}</div>
<div id='S' class='sub' style='margin-top:22px;font-size:38px;line-height:1.32;text-wrap:balance'>{s}</div>
<div style='margin-top:auto;font-size:28px;font-weight:700;color:#4e5562'>firemap.kr</div></div>
<div style='position:absolute;right:64px;top:64px;bottom:64px;width:440px;background:#18191d;border-radius:36px;padding:48px 44px;display:flex;flex-direction:column;color:#fff'>
<div style='font-size:34px;font-weight:600;color:#c7cbd3'>{lab}</div>
<div style='margin-top:18px;font-size:150px;font-weight:800;line-height:1;color:#ff5a00'>?<span style='font-size:72px;color:#fff;margin-left:10px'>원</span></div>
<div style='margin-top:auto;background:#ff5a00;border-radius:20px;padding:24px 0;text-align:center;font-size:32px;font-weight:700'>이 돈이면 몇 살에 은퇴?</div></div>"""

def page_c(t, s, lab, url, q):
    # a안 + 레드팀 r1: 알약(가짜 행동) 삭제, 다크 카드 1장에 결과 라벨 → 그 화면의 질문 줄, 주황은 질문 속 '몇 살' 하나.
    # 글자·카드 전부 가운데 630px 안(정사각 미리보기). 레드팀 r2: 카드 폭 880→620·모서리 16(버튼 아닌 카드로), 부제 32→38·라벨 26→32.
    t2 = '<br>'.join(t.split(' ')); q2 = q.replace('몇 살', "<b style='color:#ff5a00;font-weight:800'>몇 살</b>")
    return f"""<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center'>
{logo(34)}
<div id='T' style='margin-top:18px;font-weight:800;font-size:104px;line-height:1.04;white-space:nowrap'>{t2}</div>
<div id='S' class='sub' style='margin-top:16px;font-size:38px;line-height:1.25;max-width:600px;text-wrap:balance'>{s}</div>
<div style='margin-top:26px;width:620px;background:#18191d;border-radius:16px;padding:20px 0 22px;color:#fff'>
<div style='font-size:32px;font-weight:600;color:#aeb3bc'>{lab} →</div>
<div id='Q' style='margin-top:4px;font-size:40px;font-weight:700;letter-spacing:-0.035em;white-space:nowrap'>{q2}</div></div></div>"""

FIT = """<script>for(const [id,w] of [['T',%d],['Q',580]]){const e=document.getElementById(id);if(!e)continue;let s=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>w&&s>40){s-=2;e.style.fontSize=s+'px'}}</script>"""

out = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
    for k, (t, s, lab, url) in CALC.items():
        for v, fn, maxw in (('a', page_a, 560), ('b', page_b, 560), ('c', lambda *a, k=k: page_c(*a, ASKQ[k][1]), 560)):
            html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{fn(t, nb(s), lab, url)}{FIT % maxw}</body></html>"
            hp = os.path.join(H, f'{k}_{v}.html'); open(hp, 'w', encoding='utf-8').write(html)
            pg.goto('file:///' + hp.replace('\\', '/')); pg.wait_for_timeout(300)
            # 넘침 검사: 모든 글자 상자가 1200×630 안, 여백 48px 이상
            # 글자 실제 범위(텍스트 노드 Range)로 검사 — 상자가 넓어도 글자가 가운데면 통과
            bad = pg.evaluate("""([L,R])=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const o=[];let n;while(n=w.nextNode()){if(!n.textContent.trim()||n.parentElement.tagName=='SCRIPT')continue;const g=document.createRange();g.selectNodeContents(n);for(const r of g.getClientRects()){if(r.left<L||r.right>R||r.top<36||r.bottom>594)o.push([n.textContent.slice(0,12),r.left,r.top,r.right,r.bottom])}}return o}""", [300, 900] if v in 'ac' else [48, 1152])
            assert not bad, (k, v, bad)
            op = os.path.join(H, f'og_{k}_{v}.png'); pg.screenshot(path=op); out.append(op)
    b.close()

# 미리보기판: 카톡 큰 말풍선(약 520×273) · 작은 카드(260×137) · 네이버 정사각 썸네일(가운데 630×630 → 160)
F = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 22)
sheet = Image.new('RGB', (520 + 260 + 160 + 80, (273 + 50) * len(out) + 20), '#bfc7d1')
d = ImageDraw.Draw(sheet)
for i, op in enumerate(out):
    im = Image.open(op).convert('RGB'); y = 20 + i * 323
    d.text((20, y), os.path.basename(op), fill='#18191d', font=F)
    sheet.paste(im.resize((520, 273), Image.LANCZOS), (20, y + 30))
    sheet.paste(im.resize((260, 137), Image.LANCZOS), (560, y + 30))
    sheet.paste(im.crop((285, 0, 915, 630)).resize((160, 160), Image.LANCZOS), (840, y + 30))
sheet.save(os.path.join(H, 'preview_sizes.png'))
print('\n'.join(out))
