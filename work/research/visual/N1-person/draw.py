# N1 가상 인물 '정우 씨' — 제미나이 429 대신 SVG로 직접 그림(같은 얼굴이 장면마다 똑같이 나오게 부품 고정).
# py -3.12 draw.py → sheet_svg.png, s1998.png, s2001.png, s2011.png (1920x1080, 그림 안 글자 0)
# 인물은 지어낸 사람. 설정: 둥근 얼굴, 옆가르마, 관자놀이 흰머리, 검은 사각 안경, 왼눈(보는 사람 기준 오른쪽) 밑 점, 남색 카디건, 하늘색 셔츠, 파란 통장.
import os, sys
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
C = dict(bg='#F3EBDD', navy='#23324F', grey='#8A8178', coral='#E07A5F', skin='#EDC7A4', skin2='#D9A983', shirt='#BFD5E8',
         book='#1F4A8A', wall='#E8DCC8', wood='#B98B5E', line='#2B2B2B')

def head(age, expr):
    old = age >= 66
    hair = '#C9C6C0' if old else '#2C2A28'
    temple = '#E4E1DA' if old else '#A9A6A0'
    rx = 52 if old else 56
    s = []
    s.append(f'<ellipse cx="-{rx+2}" cy="6" rx="10" ry="15" fill="{C["skin2"]}"/><ellipse cx="{rx+2}" cy="6" rx="10" ry="15" fill="{C["skin2"]}"/>')
    s.append(f'<ellipse cx="0" cy="0" rx="{rx}" ry="64" fill="{C["skin"]}"/>')
    # 머리: 옆가르마(보는 사람 기준 왼쪽 가르마)
    s.append(f'<path d="M-{rx} -4 C-{rx} -58 -26 -76 4 -74 C40 -72 {rx} -54 {rx} -8 L{rx-6} -14 C{rx-10} -38 30 -48 4 -46 C-14 -46 -22 -40 -28 -30 L-30 -46 C-38 -36 -{rx-8} -24 -{rx-4} -4 Z" fill="{hair}"/>')
    s.append(f'<rect x="-{rx+1}" y="-14" width="8" height="26" rx="4" fill="{temple}"/><rect x="{rx-7}" y="-14" width="8" height="26" rx="4" fill="{temple}"/>')
    # 눈썹·눈
    if expr == 'calm':
        s.append('<path d="M-38 -22 L-14 -22 M14 -22 L38 -22" stroke="#3A3530" stroke-width="5" stroke-linecap="round"/>')
        s.append('<circle cx="-24" cy="-4" r="4.5" fill="#2B2B2B"/><circle cx="24" cy="-4" r="4.5" fill="#2B2B2B"/>')
        mouth = '<path d="M-14 34 Q0 40 14 34" stroke="#7A4A3A" stroke-width="4" fill="none" stroke-linecap="round"/>'
    elif expr == 'worried':
        s.append('<path d="M-38 -18 L-14 -27 M14 -27 L38 -18" stroke="#3A3530" stroke-width="5" stroke-linecap="round"/>')
        s.append('<circle cx="-24" cy="-2" r="4.5" fill="#2B2B2B"/><circle cx="24" cy="-2" r="4.5" fill="#2B2B2B"/>')
        mouth = '<path d="M-14 38 Q0 30 14 38" stroke="#7A4A3A" stroke-width="4" fill="none" stroke-linecap="round"/>'
    elif expr == 'surprised':
        s.append('<path d="M-38 -30 Q-26 -38 -14 -31 M14 -31 Q26 -38 38 -30" stroke="#3A3530" stroke-width="5" fill="none" stroke-linecap="round"/>')
        s.append('<circle cx="-24" cy="-4" r="6.5" fill="#fff" stroke="#2B2B2B" stroke-width="2"/><circle cx="-24" cy="-4" r="3.5" fill="#2B2B2B"/>'
                 '<circle cx="24" cy="-4" r="6.5" fill="#fff" stroke="#2B2B2B" stroke-width="2"/><circle cx="24" cy="-4" r="3.5" fill="#2B2B2B"/>')
        mouth = '<ellipse cx="0" cy="37" rx="8" ry="10" fill="#7A4A3A"/>'
    else:  # relieved
        s.append('<path d="M-38 -24 Q-26 -28 -14 -24 M14 -24 Q26 -28 38 -24" stroke="#3A3530" stroke-width="5" fill="none" stroke-linecap="round"/>')
        s.append('<path d="M-31 -3 Q-24 -10 -17 -3 M17 -3 Q24 -10 31 -3" stroke="#2B2B2B" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
        mouth = '<path d="M-16 32 Q0 46 16 32" stroke="#7A4A3A" stroke-width="4" fill="none" stroke-linecap="round"/>'
    # 안경
    s.append('<g fill="none" stroke="#1E1E1E" stroke-width="3.5"><rect x="-42" y="-16" width="36" height="24" rx="5"/><rect x="6" y="-16" width="36" height="24" rx="5"/>'
             f'<path d="M-6 -6 Q0 -10 6 -6 M-42 -8 L-{rx} -6 M42 -8 L{rx} -6"/></g>')
    s.append('<path d="M0 4 Q-6 18 0 20 Q4 20 6 18" stroke="#B07A58" stroke-width="3" fill="none" stroke-linecap="round"/>')
    s.append(f'<circle cx="27" cy="18" r="2.8" fill="#5A3A2A"/>')  # 왼눈 밑 점
    if old:
        s.append('<path d="M-24 -40 Q0 -44 24 -40 M-18 -34 Q0 -37 18 -34" stroke="#C99C7C" stroke-width="2" fill="none" opacity=".8"/>'
                 '<path d="M-26 20 Q-30 32 -24 42 M26 20 Q30 32 24 42" stroke="#C99C7C" stroke-width="2.5" fill="none"/>')
    s.append(mouth)
    return ''.join(s)

def torso(book='closed', bot=200):
    s = [f'<rect x="-16" y="56" width="32" height="26" fill="{C["skin2"]}"/>',
         f'<path d="M-98 {bot} L-92 104 Q-86 80 -40 74 L40 74 Q86 80 92 104 L98 {bot} Z" fill="{C["navy"]}"/>',
         f'<path d="M-30 74 L0 128 L30 74 Z" fill="{C["shirt"]}"/><path d="M-30 74 L-12 98 L0 82 L12 98 L30 74" fill="{C["shirt"]}" stroke="#9AB4CC" stroke-width="2"/>',
         '<circle cx="0" cy="146" r="3.5" fill="#E8E2D6"/><circle cx="0" cy="172" r="3.5" fill="#E8E2D6"/>']
    if book == 'closed':
        s.append(f'<rect x="-40" y="128" width="80" height="58" rx="5" fill="{C["book"]}"/><rect x="-30" y="140" width="40" height="5" rx="2" fill="#6F8FC4"/>')
    elif book == 'open':
        s.append('<path d="M-84 132 L0 140 L84 132 L84 190 L0 198 L-84 190 Z" fill="#FBF8F2" stroke="#C9BFAF" stroke-width="2"/><path d="M0 140 L0 198" stroke="#C9BFAF" stroke-width="2"/>'
                 '<g stroke="#D8CFC0" stroke-width="3"><path d="M-70 152 L-14 156 M-70 166 L-14 170 M-70 180 L-14 183 M14 156 L70 152 M14 170 L70 166 M14 183 L70 180"/></g>'
                 f'<path d="M-88 130 L-84 132 L-84 190 L-88 192 Z M88 130 L84 132 L84 190 L88 192 Z" fill="{C["book"]}"/>')
    elif book == 'empty':  # 빈 통장: 줄 없음, 마지막 장
        s.append('<path d="M-84 132 L0 140 L84 132 L84 190 L0 198 L-84 190 Z" fill="#FBF8F2" stroke="#C9BFAF" stroke-width="2"/><path d="M0 140 L0 198" stroke="#C9BFAF" stroke-width="2"/>'
                 '<g stroke="#D8CFC0" stroke-width="3"><path d="M-70 152 L-14 156 M-70 166 L-40 168"/></g>'
                 f'<path d="M-88 130 L-84 132 L-84 190 L-88 192 Z M88 130 L84 132 L84 190 L88 192 Z" fill="{C["book"]}"/>')
    hx = 92 if book != 'closed' else 46
    s.append(f'<ellipse cx="-{hx}" cy="164" rx="16" ry="13" fill="{C["skin"]}"/><ellipse cx="{hx}" cy="164" rx="16" ry="13" fill="{C["skin"]}"/>')
    return ''.join(s)

def man(x, y, sc, age, expr, book='closed', bot=330):
    return f'<g transform="translate({x},{y}) scale({sc})">{torso(book, bot)}{head(age, expr)}</g>'

def standing(x, y, sc, age):
    legs = (f'<path d="M-62 196 L-58 360 L-14 360 L-6 214 L6 214 L14 360 L58 360 L62 196 Z" fill="#5E5A55"/>'
            '<ellipse cx="-36" cy="366" rx="30" ry="10" fill="#2B2B2B"/><ellipse cx="36" cy="366" rx="30" ry="10" fill="#2B2B2B"/>')
    return f'<g transform="translate({x},{y}) scale({sc})">{legs}{torso("closed")}{head(age, "calm")}</g>'

def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">{body}</svg>'

def grain():
    return ('<filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0.3 0 0 0 0 0.25 0 0 0 0 0.2 0 0 0 .07 0"/></filter>'
            '<rect width="1920" height="1080" filter="url(#g)"/>')

sheet = svg(f'<rect width="1920" height="1080" fill="{C["bg"]}"/>'
    + '<line x1="80" y1="540" x2="1840" y2="540" stroke="#D9CDB8" stroke-width="3" stroke-dasharray="10 12"/>'
    + standing(200, 150, 0.95, 55)
    + ''.join(man(470 + i * 360, 200, 1.05, 55, e, bot=200) for i, e in enumerate(['calm', 'worried', 'surprised', 'relieved']))
    + standing(200, 640, 0.95, 68)
    + ''.join(man(470 + i * 360, 690, 1.05, 68, e, bot=200) for i, e in enumerate(['calm', 'worried', 'surprised', 'relieved']))
    + grain())

# S1 1998년 1월 거실 · 왼쪽 40% 비움
s1998 = svg(f'<rect width="1920" height="1080" fill="{C["wall"]}"/>'
    + '<rect x="0" y="820" width="1920" height="260" fill="#CDB89A"/>'
    + '<rect x="1240" y="150" width="440" height="420" rx="8" fill="#FFF6E0"/><rect x="1240" y="150" width="440" height="420" rx="8" fill="none" stroke="#B98B5E" stroke-width="14"/>'
    + '<path d="M1460 150 L1460 570 M1240 360 L1680 360" stroke="#B98B5E" stroke-width="10"/>'
    + '<path d="M1240 150 L1680 570" stroke="#FFFFFF" stroke-width="40" opacity=".35"/>'
    + '<rect x="1720" y="430" width="90" height="390" fill="#7E9A6E" rx="40"/><rect x="1740" y="760" width="50" height="70" fill="#9A6A4A"/>'
    + man(1080, 420, 1.55, 55, 'calm', 'open')
    + f'<rect x="760" y="760" width="640" height="40" rx="10" fill="{C["wood"]}"/><rect x="800" y="800" width="30" height="110" fill="#8E6844"/><rect x="1330" y="800" width="30" height="110" fill="#8E6844"/>'
    + '<ellipse cx="1300" cy="752" rx="40" ry="10" fill="#E8E2D6"/><rect x="1270" y="712" width="60" height="42" rx="8" fill="#F7F3EA"/>'
    + grain())

# S5 2001년 저녁 부엌 · 오른쪽 40% 비움 · 뒤 TV 빨간 선
s2001 = svg('<rect width="1920" height="1080" fill="#3B3F4E"/>'
    + '<radialGradient id="l" cx="560" cy="300" r="620" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#F6D9A6" stop-opacity=".95"/><stop offset="1" stop-color="#3B3F4E" stop-opacity="0"/></radialGradient>'
    + '<rect width="1920" height="1080" fill="url(#l)"/>'
    + '<path d="M560 0 L560 150" stroke="#222" stroke-width="4"/><path d="M490 150 L630 150 L600 200 L520 200 Z" fill="#E07A5F"/><ellipse cx="560" cy="204" rx="40" ry="8" fill="#FFF2C8"/>'
    + '<rect x="120" y="300" width="260" height="190" rx="14" fill="#1B1D24"/><rect x="138" y="316" width="224" height="158" fill="#2A2E3A"/>'
    + '<path d="M150 340 L200 350 L240 380 L280 372 L320 430 L350 460" stroke="#E5484D" stroke-width="7" fill="none" stroke-linecap="round"/>'
    + '<rect x="230" y="490" width="40" height="40" fill="#1B1D24"/>'
    + man(600, 470, 1.55, 58, 'worried', 'closed')
    + '<rect x="180" y="800" width="860" height="44" rx="8" fill="#8E6844"/><rect x="220" y="844" width="34" height="240" fill="#6E5034"/><rect x="960" y="844" width="34" height="240" fill="#6E5034"/>'
    + '<path d="M820 770 L860 800 L780 800 Z" fill="none"/><rect x="820" y="742" width="50" height="58" rx="8" fill="#E8E2D6"/>'
    + grain())

# S12 2011년 1월 · 빈 통장 들고 창밖 · 오른쪽 40% 비움
s2011 = svg('<rect width="1920" height="1080" fill="#DCD6CC"/>'
    + '<rect x="70" y="120" width="560" height="640" fill="#C8D6E2"/><path d="M70 600 Q200 560 330 610 T630 590 L630 760 L70 760 Z" fill="#EEF2F5"/>'
    + '<g fill="#fff" opacity=".9"><circle cx="160" cy="220" r="5"/><circle cx="300" cy="300" r="4"/><circle cx="460" cy="200" r="5"/><circle cx="540" cy="380" r="4"/><circle cx="220" cy="450" r="4"/><circle cx="400" cy="500" r="5"/></g>'
    + '<rect x="70" y="120" width="560" height="640" fill="none" stroke="#9C8F7E" stroke-width="16"/><path d="M350 120 L350 760" stroke="#9C8F7E" stroke-width="12"/>'
    + '<rect x="40" y="760" width="620" height="26" fill="#B5A894"/>'
    + '<rect x="0" y="940" width="1920" height="140" fill="#B5A894"/>'
    + man(860, 430, 1.75, 68, 'worried', 'empty')
    + '<rect x="560" y="790" width="620" height="160" rx="6" fill="#8E7A62"/><rect x="580" y="810" width="280" height="120" rx="4" fill="#9C876D"/><rect x="880" y="810" width="280" height="120" rx="4" fill="#9C876D"/><rect x="700" y="862" width="40" height="8" rx="4" fill="#6E5C48"/><rect x="1000" y="862" width="40" height="8" rx="4" fill="#6E5C48"/>'
    + grain())

out = {'sheet_svg': sheet, 's1998': s1998, 's2001': s2001, 's2011': s2011}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    for k, v in out.items():
        open(os.path.join(H, 'src_' + k + '.svg'), 'w', encoding='utf-8').write(v)
        pg.set_content(f'<html><body style="margin:0">{v}</body></html>'); pg.screenshot(path=os.path.join(H, k + '.png'))
        print('ok', k)
    b.close()
