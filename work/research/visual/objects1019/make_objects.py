# 10/19 visual — 판 몸통 사물 그림 10종(자체 제작 SVG -> 투명 PNG). 얼굴 없음, 색은 fm.tsx T 토큰만(잉크·회색·연주황, 주황은 한 곳).
#   py -3.12 work/research/visual/objects1019/make_objects.py  -> objects1019/svg/*.svg · png/*.png(512) · sheet.png
#   영상: 같은 스크립트가 work/video/public/art/obj/<이름>.svg로 복사 -> TallyArt {kind:'icon', src:'art/obj/<이름>.svg', license:'자체 제작(파이어맵)'}
import os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
PUB = os.path.join(WORK, 'video', 'public', 'art', 'obj')
INK, INK2, INK3, LINE, SOFT, ACC, W = '#18191d', '#4b515c', '#8a909b', '#e6e9ee', '#ffe3d1', '#ff5a00', '#ffffff'
RED, BLUE = '#e5484d', '#2f6fde'  # 국기 전용(실물 색)
S = f'stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"'
s6 = f'stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'


def gl(x1, y1, x2, y2):  # 회색 글줄
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK3}" stroke-width="7" stroke-linecap="round"/>'


OBJ = {}

# 1 통장 — 잔액·꺼내 쓰기 판
OBJ['bankbook'] = ('통장', '잔액·꺼내 쓰기·남은 돈',
    f'<rect x="70" y="60" width="260" height="290" rx="18" fill="{SOFT}" {S}/>'
    f'<rect x="70" y="60" width="50" height="290" rx="18" fill="{ACC}" {S}/>'
    f'<line x1="150" y1="120" x2="290" y2="120" {s6}/>'
    + gl(150, 175, 300, 175) + gl(150, 215, 270, 215) + gl(150, 255, 290, 255) + gl(150, 295, 240, 295))

# 2 저울 — A vs B 비교 판 (왼쪽이 무거움)
OBJ['scale'] = ('저울', 'A와 B 비교·어느 쪽이 더',
    f'<line x1="200" y1="105" x2="200" y2="335" {S}/><line x1="135" y1="340" x2="265" y2="340" {S}/>'
    f'<line x1="80" y1="130" x2="320" y2="90" {S}/>'
    f'<path d="M80 130 L45 225 M80 130 L115 225" fill="none" {s6}/><path d="M40 225 Q80 275 120 225 Z" fill="{SOFT}" {S}/>'
    f'<path d="M320 90 L285 185 M320 90 L355 185" fill="none" {s6}/><path d="M280 185 Q320 235 360 185 Z" fill="{W}" {S}/>'
    f'<circle cx="200" cy="110" r="15" fill="{ACC}" {S}/>')

# 3 달력 — 날짜·기한·시작 시점 판
cells = ''.join(
    f'<rect x="{88 + c * 58}" y="{165 + r * 52}" width="40" height="32" rx="7" fill="{SOFT if (r, c) == (1, 2) else LINE}"'
    + (f' {s6}' if (r, c) == (1, 2) else '') + '/>' for r in range(3) for c in range(4))
OBJ['calendar'] = ('달력', '날짜·기한·시작 시점',
    f'<rect x="60" y="80" width="280" height="260" rx="18" fill="{W}" {S}/>'
    f'<path d="M60 98 Q60 80 78 80 L322 80 Q340 80 340 98 L340 140 L60 140 Z" fill="{ACC}" {S}/>'
    f'<line x1="120" y1="55" x2="120" y2="105" {S}/><line x1="280" y1="55" x2="280" y2="105" {S}/>' + cells)


# 4 국기(한국·미국) — 환율·해외 투자 판. 태극기 괘: 건(☰) 왼쪽 위·곤(☷) 오른쪽 아래·감(☵) 오른쪽 위·리(☲) 왼쪽 아래
def trigram(cx, cy, ang, pat):
    out = []
    for i, b in enumerate(pat):
        y = cy - 12 + i * 9
        out.append(f'<rect x="{cx - 20}" y="{y}" width="40" height="6" fill="{INK}"/>' if b else
                   f'<rect x="{cx - 20}" y="{y}" width="17" height="6" fill="{INK}"/><rect x="{cx + 3}" y="{y}" width="17" height="6" fill="{INK}"/>')
    return f'<g transform="rotate({ang} {cx} {cy})">' + ''.join(out) + '</g>'


KR = (f'<rect x="20" y="60" width="200" height="134" rx="8" fill="{W}"/>'
      f'<circle cx="120" cy="127" r="33" fill="{BLUE}"/>'
      f'<path d="M87 127 A33 33 0 0 1 153 127 A16.5 16.5 0 0 1 120 127 A16.5 16.5 0 0 0 87 127 Z" fill="{RED}"/>'
      + trigram(62, 87, -56, [1, 1, 1]) + trigram(178, 167, -56, [0, 0, 0]) + trigram(178, 87, 56, [0, 1, 0]) + trigram(62, 167, 56, [1, 0, 1])
      + f'<rect x="20" y="60" width="200" height="134" rx="8" fill="none" {s6}/>')
US = (f'<g transform="translate(180 206)"><rect x="0" y="0" width="200" height="126" rx="8" fill="{W}"/>'
      + ''.join(f'<rect x="0" y="{i * 19.4}" width="200" height="9.7" fill="{RED}"/>' for i in range(7))
      + f'<rect x="0" y="0" width="84" height="68" fill="{BLUE}"/>'
      + ''.join(f'<circle cx="{12 + c * 15}" cy="{12 + r * 15}" r="3.2" fill="{W}"/>' for r in range(4) for c in range(5))
      + f'<rect x="0" y="0" width="200" height="126" rx="8" fill="none" {s6}/></g>')
OBJ['flags_kr_us'] = ('국기(한국·미국)', '환율·원화 기준·해외 주식',
    KR + US + f'<path d="M160 290 Q90 300 90 225" fill="none" {s6} stroke-dasharray="3 15"/><path d="M76 240 L90 220 L104 240" fill="none" {s6}/>')

# 5 흐름 화살표 — 돈이 가는 순서·단계 판
OBJ['flow'] = ('흐름 화살표', '돈이 가는 순서·단계',
    f'<rect x="25" y="160" width="90" height="80" rx="14" fill="{W}" {S}/>'
    f'<rect x="155" y="160" width="90" height="80" rx="14" fill="{W}" {S}/>'
    f'<rect x="285" y="160" width="90" height="80" rx="14" fill="{SOFT}" {S}/>'
    f'<path d="M118 200 L146 200 M134 186 L148 200 L134 214" fill="none" {S}/>'
    f'<path d="M248 200 L276 200 M264 186 L278 200 L264 214" fill="none" {S}/>'
    f'<circle cx="330" cy="200" r="16" fill="{ACC}"/>'
    f'<path d="M200 245 Q200 315 120 315 L70 315" fill="none" stroke="{INK3}" stroke-width="8" stroke-linecap="round" stroke-dasharray="4 18"/>')

# 6 동전 더미 — 금액 크기·차이 판(높이 차이)
coins = ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="62" ry="20" fill="{SOFT if k % 2 else W}" {s6}/>' for k, (cx, cy) in enumerate(
    [(130, 320), (130, 296), (130, 272), (130, 248)] + [(270, 320 - 24 * i) for i in range(7)]))
OBJ['coins'] = ('동전 더미', '금액 크기·모은 돈·차이', coins + f'<ellipse cx="270" cy="152" rx="62" ry="20" fill="{ACC}" {s6}/>')

# 7 집 — 아파트·매매·전세·양도세 판
OBJ['house'] = ('집', '아파트·매매·전세·양도세',
    f'<rect x="265" y="90" width="32" height="70" fill="{W}" {S}/>'
    f'<rect x="95" y="180" width="210" height="160" fill="{W}" {S}/>'
    f'<path d="M60 195 L200 75 L340 195" fill="none" {S}/>'
    f'<rect x="170" y="250" width="60" height="90" fill="{SOFT}" {S}/>'
    f'<rect x="115" y="205" width="40" height="38" fill="{LINE}" {s6}/><rect x="245" y="205" width="40" height="38" fill="{LINE}" {s6}/>'
    f'<circle cx="217" cy="298" r="6" fill="{ACC}"/>')

# 8 영수증 — 세금·건보료·낸 돈 판
OBJ['receipt'] = ('영수증', '세금·건보료·낸 돈',
    f'<path d="M95 50 L305 50 L305 345 L280 330 L255 345 L230 330 L205 345 L180 330 L155 345 L130 330 L105 345 L95 338 Z" fill="{W}" {S}/>'
    f'<line x1="130" y1="100" x2="270" y2="100" {s6}/>' + gl(130, 145, 230, 145) + gl(130, 180, 250, 180) + gl(130, 215, 210, 215)
    + f'<line x1="125" y1="252" x2="275" y2="252" {s6} stroke-dasharray="3 12"/>'
    f'<rect x="190" y="270" width="85" height="30" rx="6" fill="{ACC}"/>')

# 9 계산기 — 내 돈 대입·직접 계산 판
keys = ''.join(f'<rect x="{118 + c * 44}" y="{185 + r * 40}" width="32" height="28" rx="7" fill="{ACC if (r, c) == (3, 3) else LINE}"/>' for r in range(4) for c in range(4))
OBJ['calculator'] = ('계산기', '내 돈 대입·직접 계산',
    f'<rect x="95" y="55" width="210" height="300" rx="24" fill="{W}" {S}/>'
    f'<rect x="120" y="85" width="160" height="70" rx="10" fill="{SOFT}" {s6}/>'
    f'<line x1="200" y1="120" x2="260" y2="120" {s6}/>' + keys)

# 10 모래시계 — 기간·돈이 바닥나는 시점 판
OBJ['hourglass'] = ('모래시계', '기간·돈이 바닥나는 시점',
    f'<path d="M135 60 Q135 160 200 200 Q135 240 135 340 L265 340 Q265 240 200 200 Q265 160 265 60 Z" fill="{W}" {S}/>'
    f'<path d="M168 125 Q200 150 232 125 Z" fill="{SOFT}"/>'
    f'<line x1="200" y1="205" x2="200" y2="285" stroke="{ACC}" stroke-width="5" stroke-dasharray="2 10" stroke-linecap="round"/>'
    f'<path d="M148 335 Q200 278 252 335 Z" fill="{ACC}"/>'
    f'<line x1="105" y1="60" x2="295" y2="60" {S}/><line x1="105" y1="340" x2="295" y2="340" {S}/>')


def svg(body, px=400):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="{px}" height="{px}">{body}</svg>'


os.makedirs(os.path.join(H, 'svg'), exist_ok=True); os.makedirs(os.path.join(H, 'png'), exist_ok=True); os.makedirs(PUB, exist_ok=True)
for k, (_, _, body) in OBJ.items():
    p = os.path.join(H, 'svg', k + '.svg')
    open(p, 'w', encoding='utf-8').write(svg(body))
    shutil.copy(p, os.path.join(PUB, k + '.svg'))

from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 512, 'height': 512})
    for k, (_, _, body) in OBJ.items():
        pg.set_content('<html><body style="margin:0;background:transparent">' + svg(body, 512) + '</body></html>')
        pg.screenshot(path=os.path.join(H, 'png', k + '.png'), omit_background=True, clip={'x': 0, 'y': 0, 'width': 512, 'height': 512})
    # 눈 검사용: 판 바탕(#f6f7f9) 위 실제 판 몸통 크기(220px)
    cards = ''.join(
        '<div style="display:flex;flex-direction:column;align-items:center;gap:6px">' + svg(body, 220)
        + f'<div style="font:700 26px Malgun Gothic;color:{INK}">{name}</div>'
        + f'<div style="font:500 18px Malgun Gothic;color:{INK2}">{use}</div>'
        + f'<div style="font:500 15px Consolas;color:{INK3}">{k}</div></div>' for k, (name, use, body) in OBJ.items())
    pg.set_viewport_size({'width': 1500, 'height': 900})
    pg.set_content('<html><body style="margin:0;background:#f6f7f9"><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:28px;padding:40px">' + cards + '</div></body></html>')
    pg.screenshot(path=os.path.join(H, 'sheet.png'), full_page=True)
    b.close()
print('\n'.join(f'{k}\t{v[0]}\t{v[1]}' for k, v in OBJ.items()))
