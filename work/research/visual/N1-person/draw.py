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
    elif book == 'paper':  # 서류 한 장(환전 서류, 글자 없이 줄만)
        s.append('<rect x="-62" y="112" width="124" height="96" rx="4" fill="#FFFFFF" stroke="#C9BFAF" stroke-width="2"/>'
                 '<g stroke="#D8CFC0" stroke-width="4"><path d="M-48 132 L48 132 M-48 150 L30 150 M-48 168 L48 168 M-48 186 L10 186"/></g>'
                 '<rect x="18" y="176" width="30" height="20" rx="3" fill="none" stroke="#E07A5F" stroke-width="3"/>')
    elif book == 'calc':  # 계산기
        s.append('<rect x="-44" y="114" width="88" height="110" rx="10" fill="#E9E5DB" stroke="#B9B2A4" stroke-width="2"/><rect x="-34" y="124" width="68" height="26" rx="4" fill="#B9C9A4"/>'
                 + ''.join(f'<rect x="{-34 + c * 18}" y="{158 + r * 16}" width="14" height="12" rx="3" fill="{"#F08A24" if c == 3 else "#FBFAF6"}"/>' for r in range(4) for c in range(4)))
    elif book == 'news':  # 신문(글자 없이 칸·줄만)
        s.append('<rect x="-104" y="100" width="208" height="136" fill="#F1EEE6" stroke="#BDB6A8" stroke-width="2"/><path d="M0 100 L0 236" stroke="#CFC8BA" stroke-width="2"/>'
                 '<rect x="-92" y="112" width="80" height="14" fill="#8E8A82"/><rect x="-92" y="134" width="80" height="44" fill="#C9C4B8"/>'
                 '<g stroke="#CFC8BA" stroke-width="4"><path d="M-92 190 L-12 190 M-92 204 L-12 204 M-92 218 L-30 218 M12 116 L92 116 M12 130 L92 130 M12 144 L92 144 M12 158 L70 158 M12 176 L92 176 M12 190 L92 190 M12 204 L60 204"/></g>'
                 '<path d="M14 214 L40 196 L60 206 L90 180" stroke="#2E8B57" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif book == 'envelope':  # 흰 봉투를 내밂
        s.append('<rect x="20" y="118" width="120" height="74" rx="4" fill="#FFFFFF" stroke="#C9BFAF" stroke-width="2"/><path d="M20 118 L80 156 L140 118" stroke="#C9BFAF" stroke-width="2" fill="none"/>')
        s.append(f'<ellipse cx="-46" cy="164" rx="16" ry="13" fill="{C["skin"]}"/><ellipse cx="80" cy="190" rx="16" ry="13" fill="{C["skin"]}"/>')
        return ''.join(s)
    hx = 92 if book != 'closed' else 46
    s.append(f'<ellipse cx="-{hx}" cy="164" rx="16" ry="13" fill="{C["skin"]}"/><ellipse cx="{hx}" cy="164" rx="16" ry="13" fill="{C["skin"]}"/>')
    return ''.join(s)

def man(x, y, sc, age, expr, book='closed', bot=330):
    return f'<g transform="translate({x},{y}) scale({sc})">{torso(book, bot)}{head(age, expr)}</g>'

def standing(x, y, sc, age, expr='calm', book='closed'):
    legs = (f'<path d="M-62 196 L-58 360 L-14 360 L-6 214 L6 214 L14 360 L58 360 L62 196 Z" fill="#5E5A55"/>'
            '<ellipse cx="-36" cy="366" rx="30" ry="10" fill="#2B2B2B"/><ellipse cx="36" cy="366" rx="30" ry="10" fill="#2B2B2B"/>')
    return f'<g transform="translate({x},{y}) scale({sc})">{legs}{torso(book)}{head(age, expr)}</g>'

def back(x, y, sc, hair='#3A3633', coat='#6B4E3D', grey=False, bot=300):
    """뒷모습(얼굴 없음) — 영호 씨·민수 씨·아내. 손에 든 파란 통장 모서리만 양옆으로 보임"""
    t = '#BDB8B0' if grey else hair
    return (f'<g transform="translate({x},{y}) scale({sc})">'
            f'<path d="M-104 {bot} L-98 104 Q-90 76 -40 70 L40 70 Q90 76 98 104 L104 {bot} Z" fill="{coat}"/>'
            f'<rect x="-18" y="48" width="36" height="28" fill="{C["skin2"]}"/>'
            f'<ellipse cx="-56" cy="4" rx="10" ry="15" fill="{C["skin2"]}"/><ellipse cx="56" cy="4" rx="10" ry="15" fill="{C["skin2"]}"/>'
            f'<ellipse cx="0" cy="-4" rx="56" ry="64" fill="{t}"/><path d="M-50 30 Q0 52 50 30 L46 46 Q0 64 -46 46 Z" fill="{C["skin2"]}"/>'
            f'<path d="M-120 150 L-96 140 L-96 176 L-120 184 Z M120 150 L96 140 L96 176 L120 184 Z" fill="{C["book"]}"/></g>')

def woman_back(x, y, sc):
    """아내(뒷모습, 얼굴 없음) — 단발, 갈색 외투, 장바구니"""
    return (f'<g transform="translate({x},{y}) scale({sc})">'
            '<path d="M-58 196 L-54 360 L-12 360 L-4 214 L4 214 L12 360 L54 360 L58 196 Z" fill="#7A6F66"/>'
            '<ellipse cx="-34" cy="366" rx="26" ry="9" fill="#2B2B2B"/><ellipse cx="34" cy="366" rx="26" ry="9" fill="#2B2B2B"/>'
            '<path d="M-90 230 L-84 100 Q-78 76 -36 70 L36 70 Q78 76 84 100 L90 230 Z" fill="#A0634A"/>'
            '<path d="M-58 20 Q-60 -64 0 -66 Q60 -64 58 20 Q56 50 40 56 L-40 56 Q-56 50 -58 20 Z" fill="#3A2C26"/>'
            '<path d="M86 150 L130 150 L124 220 L92 220 Z" fill="#E8D9B8" stroke="#B8A27A" stroke-width="3"/><path d="M96 150 Q108 120 120 150" stroke="#B8A27A" stroke-width="4" fill="none"/>'
            '<rect x="98" y="138" width="8" height="18" fill="#7E9A6E"/><circle cx="114" cy="142" r="9" fill="#E07A5F"/></g>')

def kitchen(night=True):
    """S5와 같은 부엌(전등·TV·식탁) — S16·S17 재사용 배경"""
    bg = '#3B3F4E' if night else '#5A6070'
    return (f'<rect width="1920" height="1080" fill="{bg}"/>'
            f'<radialGradient id="l" cx="560" cy="300" r="620" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#F6D9A6" stop-opacity=".95"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></radialGradient>'
            '<rect width="1920" height="1080" fill="url(#l)"/>'
            '<path d="M560 0 L560 150" stroke="#222" stroke-width="4"/><path d="M490 150 L630 150 L600 200 L520 200 Z" fill="#E07A5F"/><ellipse cx="560" cy="204" rx="40" ry="8" fill="#FFF2C8"/>'
            '<rect x="120" y="300" width="260" height="190" rx="14" fill="#1B1D24"/><rect x="138" y="316" width="224" height="158" fill="#2A2E3A"/><rect x="230" y="490" width="40" height="40" fill="#1B1D24"/>')

def table_k():
    return '<rect x="180" y="800" width="860" height="44" rx="8" fill="#8E6844"/><rect x="220" y="844" width="34" height="240" fill="#6E5034"/><rect x="960" y="844" width="34" height="240" fill="#6E5034"/>'

def wallcal(x, y, mark=True):
    cal = ''.join(f'<rect x="{x + 20 + (i % 7) * 40}" y="{y + 90 + (i // 7) * 36}" width="34" height="30" rx="3" fill="#F2EEE6"/>' for i in range(35))
    return (f'<rect x="{x}" y="{y}" width="320" height="280" rx="8" fill="#FFFFFF"/><rect x="{x}" y="{y}" width="320" height="70" rx="8" fill="#E07A5F"/>{cal}'
            + (f'<ellipse cx="{x + 37}" cy="{y + 105}" rx="30" ry="24" fill="none" stroke="#E5484D" stroke-width="6"/>' if mark else ''))

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

# S6 2002년 겨울 · 벽 달력 1월에 동그라미(숫자·글자 없이 칸만) · 통장 오래 봄 · 왼쪽 35% 비움
_cal = ''.join(f'<rect x="{1180 + (i % 7) * 52}" y="{250 + (i // 7) * 46}" width="44" height="38" rx="4" fill="#F2EEE6"/>' for i in range(35))
s2002 = svg('<rect width="1920" height="1080" fill="#D9D3C7"/>'
    + '<rect x="0" y="860" width="1920" height="220" fill="#B9AD98"/>'
    + '<rect x="1160" y="150" width="404" height="350" rx="10" fill="#FFFFFF"/><rect x="1160" y="150" width="404" height="80" rx="10" fill="#E07A5F"/>'
    + '<circle cx="1260" cy="150" r="10" fill="#555"/><circle cx="1464" cy="150" r="10" fill="#555"/>' + _cal
    + '<ellipse cx="1228" cy="269" rx="38" ry="30" fill="none" stroke="#E5484D" stroke-width="7"/>'
    + '<rect x="1640" y="380" width="200" height="480" rx="10" fill="#A7B6C2"/><path d="M1650 420 L1830 420" stroke="#fff" stroke-width="4" opacity=".6"/>'
    + man(900, 440, 1.6, 59, 'worried', 'open')
    + f'<rect x="600" y="800" width="640" height="40" rx="10" fill="{C["wood"]}"/><rect x="640" y="840" width="30" height="110" fill="#8E6844"/><rect x="1170" y="840" width="30" height="110" fill="#8E6844"/>'
    + '<ellipse cx="700" cy="792" rx="36" ry="9" fill="#E8E2D6"/><path d="M684 760 Q690 740 684 724 M704 760 Q710 740 704 724" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>'
    + grain())

# S10 2009년 · 창가에서 통장을 덮음 · 머리 셈(66세 이상) · 오른쪽 40% 비움
s2009 = svg('<rect width="1920" height="1080" fill="#E4DCCD"/>'
    + '<rect x="90" y="110" width="520" height="620" fill="#F4E3B8"/><rect x="90" y="110" width="520" height="620" fill="none" stroke="#9C8F7E" stroke-width="16"/>'
    + '<path d="M350 110 L350 730 M90 420 L610 420" stroke="#9C8F7E" stroke-width="12"/>'
    + '<circle cx="230" cy="260" r="60" fill="#F7C873" opacity=".85"/>'
    + '<rect x="0" y="940" width="1920" height="140" fill="#BFAE93"/>'
    + man(860, 440, 1.7, 66, 'calm', 'closed')
    + '<path d="M860 0 L860 40" stroke="none"/>'
    + '<rect x="560" y="800" width="640" height="40" rx="10" fill="#A27B54"/><rect x="600" y="840" width="30" height="100" fill="#7E5D3E"/><rect x="1130" y="840" width="30" height="100" fill="#7E5D3E"/>'
    + '<rect x="620" y="760" width="90" height="40" rx="6" fill="#7E9A6E"/><rect x="636" y="730" width="58" height="34" rx="12" fill="#9BB78A"/>'
    + grain())

# S11 2010년 겨울 · 은행 창구 탁자(유리 칸막이) · 통장 마지막 장 넘김 · 왼쪽 35% 비움
s2010 = svg('<rect width="1920" height="1080" fill="#CFD8DC"/>'
    + '<rect x="0" y="0" width="1920" height="140" fill="#B8C4CA"/>' + ''.join(f'<rect x="{120 + i * 330}" y="40" width="220" height="40" rx="6" fill="#EAF0F2"/>' for i in range(6))
    + '<rect x="1120" y="200" width="760" height="520" fill="#E9EFF1" opacity=".55" stroke="#9FB0B8" stroke-width="8"/>'
    + '<rect x="1300" y="520" width="400" height="16" fill="#9FB0B8"/>'
    + '<rect x="0" y="780" width="1920" height="300" fill="#8A9AA2"/>'
    + man(860, 420, 1.65, 67, 'worried', 'empty')
    + '<rect x="440" y="760" width="1440" height="48" rx="6" fill="#6E7F88"/>'
    + '<rect x="1460" y="700" width="70" height="60" rx="6" fill="#F2EEE6"/><rect x="1470" y="690" width="50" height="14" rx="4" fill="#4C5A61"/>'
    + grain())
out_extra = {'s2002': s2002, 's2009': s2009, 's2010': s2010}

# ── 10/14 17:4x 나머지 장면(scenes.md S2~S4·S7~S9·S13~S17) — 같은 부품, 그림 안 글자 0
LIV = (f'<rect width="1920" height="1080" fill="{C["wall"]}"/><rect x="0" y="820" width="1920" height="260" fill="#CDB89A"/>'
       '<rect x="1240" y="150" width="440" height="420" rx="8" fill="#FFF6E0"/><rect x="1240" y="150" width="440" height="420" rx="8" fill="none" stroke="#B98B5E" stroke-width="14"/>'
       '<path d="M1460 150 L1460 570 M1240 360 L1680 360" stroke="#B98B5E" stroke-width="10"/><rect x="1720" y="430" width="90" height="390" fill="#7E9A6E" rx="40"/><rect x="1740" y="760" width="50" height="70" fill="#9A6A4A"/>')
TBL = f'<rect x="760" y="760" width="640" height="40" rx="10" fill="{C["wood"]}"/><rect x="800" y="800" width="30" height="110" fill="#8E6844"/><rect x="1330" y="800" width="30" height="110" fill="#8E6844"/>'
BANK = ('<rect width="1920" height="1080" fill="#E3E8E4"/><rect x="0" y="0" width="1920" height="140" fill="#C9D3CC"/>'
        + ''.join(f'<rect x="{120 + i * 330}" y="40" width="220" height="40" rx="6" fill="#F2F5F2"/>' for i in range(6))
        + '<rect x="0" y="780" width="1920" height="300" fill="#9AA79E"/>')

# S2 인물 소개 — 정면 크게, 왼쪽 45% 비움(가상 인물 도장 자리)
s_intro = svg('<rect width="1920" height="1080" fill="#E9E1D2"/><circle cx="1250" cy="560" r="430" fill="#DCD0BC"/>'
    + standing(1250, 250, 1.75, 55, 'calm') + grain())
# S3 1998 은행 창구 옆 탁자 · 환전 서류
s1998b = svg(BANK + '<rect x="1180" y="220" width="680" height="480" fill="#F4F7F4" opacity=".55" stroke="#A9B6AD" stroke-width="8"/>'
    + man(800, 420, 1.65, 55, 'worried', 'paper') + '<rect x="380" y="760" width="1500" height="48" rx="6" fill="#7E8C83"/>'
    + '<rect x="1300" y="700" width="80" height="60" rx="6" fill="#DCE7DF"/>' + grain())
# S3-2 1997 영호 씨 뒷모습 · 책상 위 통장 펼침 · 다른 방(녹색 벽)
s1997 = svg('<rect width="1920" height="1080" fill="#C9D6C2"/><rect x="0" y="860" width="1920" height="220" fill="#A89478"/>'
    + '<rect x="1300" y="160" width="380" height="460" rx="8" fill="#EEF3E6"/><rect x="1300" y="160" width="380" height="460" rx="8" fill="none" stroke="#8E7A5E" stroke-width="14"/><path d="M1490 160 L1490 620" stroke="#8E7A5E" stroke-width="10"/>'
    + '<rect x="560" y="780" width="900" height="44" rx="8" fill="#8E6844"/><rect x="600" y="824" width="34" height="200" fill="#6E5034"/><rect x="1390" y="824" width="34" height="200" fill="#6E5034"/>'
    + back(980, 470, 1.6, hair='#2A2624', coat='#5C6B4E') + grain())
# S4 1999 봄 공원 산책 · 아내(뒷모습) 장바구니
s1999 = svg('<rect width="1920" height="1080" fill="#CFE6F2"/><rect x="0" y="700" width="1920" height="380" fill="#9CC48A"/><path d="M0 820 Q960 760 1920 830 L1920 1080 L0 1080 Z" fill="#D9CDB0"/>'
    + ''.join(f'<rect x="{x}" y="420" width="34" height="300" fill="#8A6A4A"/><circle cx="{x + 17}" cy="400" r="130" fill="#F2C6D4"/><circle cx="{x - 60}" cy="450" r="80" fill="#F6D6E0"/>' for x in (240, 1650))
    + standing(1060, 300, 1.45, 56, 'relieved') + woman_back(1360, 340, 1.35) + grain())
# S7 2003 신문 보며 처음 웃음 · 낮 거실(왼쪽 35% 비움)
s2003 = svg(LIV + man(1080, 420, 1.55, 60, 'relieved', 'news') + TBL + grain())
# S7-2 2003 1월 다른 동네 민수 씨 뒷모습 · 아파트 창 밖
s2003m = svg('<rect width="1920" height="1080" fill="#D6D0E0"/><rect x="200" y="140" width="700" height="560" fill="#BFD3E6"/>'
    + ''.join(f'<rect x="{240 + i * 130}" y="{300 - (i % 3) * 60}" width="100" height="{400 + (i % 3) * 60}" fill="#9AAAC0"/>' for i in range(5))
    + '<rect x="200" y="140" width="700" height="560" fill="none" stroke="#8C8498" stroke-width="16"/><path d="M550 140 L550 700" stroke="#8C8498" stroke-width="12"/>'
    + '<rect x="0" y="880" width="1920" height="200" fill="#A99C88"/><rect x="900" y="800" width="800" height="44" rx="8" fill="#7A6450"/>'
    + back(1300, 480, 1.6, hair='#1E1C1B', coat='#3E5A7A') + grain())
# S8 2005 손주 돌잔치 · 봉투 건넴 · 돌상(떡 탑·과일)
s2005 = svg('<rect width="1920" height="1080" fill="#F3E3D3"/><rect x="0" y="860" width="1920" height="220" fill="#C9A98A"/>'
    + ''.join(f'<circle cx="{1350 + i * 110}" cy="{200 + (i % 2) * 50}" r="46" fill="{c}"/><path d="M{1350 + i * 110} {246 + (i % 2) * 50} L{1350 + i * 110} 420" stroke="#999" stroke-width="2"/>' for i, c in enumerate(['#F2A7B5', '#A7D3F2', '#F7D774', '#B5E0B0']))
    + man(820, 420, 1.6, 62, 'relieved', 'envelope')
    + '<rect x="1180" y="720" width="620" height="44" rx="8" fill="#B23A3A"/><rect x="1220" y="764" width="30" height="120" fill="#7E2A2A"/><rect x="1730" y="764" width="30" height="120" fill="#7E2A2A"/>'
    + '<rect x="1300" y="610" width="140" height="110" rx="10" fill="#FFFFFF"/><rect x="1300" y="650" width="140" height="22" fill="#F2A7B5"/><rect x="1300" y="690" width="140" height="18" fill="#B5E0B0"/>'
    + '<circle cx="1530" cy="690" r="34" fill="#E07A5F"/><circle cx="1600" cy="694" r="30" fill="#F7C873"/><circle cx="1666" cy="690" r="32" fill="#9BB78A"/>' + grain())
# S9 2008 가을 TV 앞에 서 있음 · 화면엔 떨어지는 선만
s2008 = svg('<rect width="1920" height="1080" fill="#4A4540"/><rect x="0" y="880" width="1920" height="200" fill="#5E5248"/>'
    + '<rect x="1100" y="260" width="620" height="390" rx="16" fill="#15171C"/><rect x="1124" y="282" width="572" height="346" fill="#262A33"/>'
    + '<path d="M1150 330 L1260 350 L1330 420 L1400 400 L1480 500 L1560 540 L1670 600" stroke="#E5484D" stroke-width="9" fill="none" stroke-linecap="round"/>'
    + '<rect x="1300" y="650" width="220" height="230" fill="#2E2A26"/>'
    + '<radialGradient id="tv" cx="1410" cy="450" r="900" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#8FA6C8" stop-opacity=".35"/><stop offset="1" stop-color="#4A4540" stop-opacity="0"/></radialGradient><rect width="1920" height="1080" fill="url(#tv)"/>'
    + standing(620, 330, 1.5, 65, 'surprised') + grain())
# S13 두 통장 나란히 — 왼쪽 정우 씨 빈 통장(줄 2개), 오른쪽 민수 씨 통장(줄 가득), 숫자는 렌더 때
def pbook(x, y, rows):
    return (f'<path d="M{x} {y} L{x + 380} {y + 30} L{x + 760} {y} L{x + 760} {y + 470} L{x + 380} {y + 500} L{x} {y + 470} Z" fill="#FBF8F2" stroke="#C9BFAF" stroke-width="4"/>'
            f'<path d="M{x + 380} {y + 30} L{x + 380} {y + 500}" stroke="#C9BFAF" stroke-width="4"/>'
            f'<path d="M{x - 18} {y - 8} L{x} {y} L{x} {y + 470} L{x - 18} {y + 480} Z M{x + 778} {y - 8} L{x + 760} {y} L{x + 760} {y + 470} L{x + 778} {y + 480} Z" fill="{C["book"]}"/>'
            + ''.join(f'<path d="M{x + 40} {y + 80 + i * 44} L{x + 340} {y + 92 + i * 44} M{x + 420} {y + 92 + i * 44} L{x + 720} {y + 80 + i * 44}" stroke="#D3C8B6" stroke-width="7"/>' for i in range(rows)))
s_two = svg('<rect width="1920" height="1080" fill="#E7E1D6"/>' + pbook(110, 300, 2) + pbook(1050, 300, 8) + grain())
# S14 달력 벽 — 1989~2025년 1월 37장, 1998~2002 연달아 5장 회색 + 2004 한 장 회색
def calwall():
    s = '<rect width="1920" height="1080" fill="#EFE9DE"/>'
    for i in range(37):
        r, c = divmod(i, 8); x, y = 150 + c * 210, 70 + r * 196
        grey = (1998 <= 1989 + i <= 2002) or 1989 + i == 2004
        s += (f'<rect x="{x}" y="{y}" width="170" height="172" rx="8" fill="{"#B8B4AE" if grey else "#FFFFFF"}"/>'
              f'<rect x="{x}" y="{y}" width="170" height="40" rx="8" fill="{"#8E8A84" if grey else "#E07A5F"}"/>'
              + ''.join(f'<rect x="{x + 14 + (k % 5) * 30}" y="{y + 54 + (k // 5) * 28}" width="18" height="18" rx="2" fill="{"#A29E98" if grey else "#EFE9DE"}"/>' for k in range(20)))
    return s
s_cal = svg(calwall() + grain())
# S15 1998 거실로 돌아감 · 계산기 두드리다 멈춤
s1998c = svg(LIV + man(1080, 420, 1.55, 55, 'surprised', 'calc') + TBL + grain())
# S16 2001년 1월 같은 부엌 · 통장 펼쳐 놓고 벽 달력
s2001b = svg(kitchen() + wallcal(1300, 220) + man(700, 470, 1.55, 58, 'calm', 'open') + table_k() + grain())
# S17 2003년 1월 같은 부엌 · 신문 보며 망설임
s2003k = svg(kitchen() + wallcal(1300, 220, mark=False) + man(700, 470, 1.55, 60, 'worried', 'news') + table_k() + grain())
out_extra.update({'s_intro': s_intro, 's1998b': s1998b, 's1997': s1997, 's1999': s1999, 's2003': s2003, 's2003m': s2003m,
                  's2005': s2005, 's2008': s2008, 's_two': s_two, 's_cal': s_cal, 's1998c': s1998c, 's2001b': s2001b, 's2003k': s2003k})

out = {'sheet_svg': sheet, 's1998': s1998, 's2001': s2001, 's2011': s2011, **out_extra}
if len(sys.argv) > 1: out = {k: v for k, v in out.items() if k in sys.argv[1].split(',')}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    for k, v in out.items():
        open(os.path.join(H, 'src_' + k + '.svg'), 'w', encoding='utf-8').write(v)
        pg.set_content(f'<html><body style="margin:0">{v}</body></html>'); pg.screenshot(path=os.path.join(H, k + '.png'))
        print('ok', k)
    b.close()
