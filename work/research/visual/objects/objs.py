# 사물 오브젝트 SVG 정의 — guide.md 규칙(512 격자·잉크 선 14·흰 스티커 테두리·그림자 없음)
# 실행: py -3.12 make.py (이 파일을 import)
import re
INK, WHITE, YEL, G1, G2, ORG = '#18191d', '#ffffff', '#ffd400', '#d0d4da', '#8a9099', '#ff5a00'
SW = 14  # 잉크 선 굵기(512 기준)
ST = SW + 26  # 흰 스티커 테두리(뒤에 깔리는 흰 선)


def sticker(body):
    # 같은 도형을 흰색·선 +26으로 한 번 더 깐다(어두운 바탕에서 잉크 윤곽이 묻히지 않게)
    b = re.sub(r'stroke-width="(\d+)"', lambda m: f'stroke-width="{int(m.group(1)) + 26}"', body)
    b = re.sub(r'stroke="#[0-9a-f]{6}"', f'stroke="{WHITE}"', b)
    b = re.sub(r'fill="#[0-9a-f]{6}"', f'fill="{WHITE}"', b)
    # 선 없는 채움 도형에도 흰 테두리
    b = re.sub(r'<(rect|circle|path)((?:(?!stroke=)[^>])*)/>', lambda m: f'<{m.group(1)}{m.group(2)} stroke="{WHITE}" stroke-width="26"/>', b)
    return b


def wrap(body, name):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<title>{name}</title>
<g stroke-linejoin="round" stroke-linecap="round">{sticker(body)}</g>
<g stroke-linejoin="round" stroke-linecap="round">{body}</g>
</svg>'''


def s(fill=WHITE, w=SW):
    return f'fill="{fill}" stroke="{INK}" stroke-width="{w}"'


WON = 'M{x0} {y0} L{x1} {y2} L{xm} {y1} L{x3} {y2} L{x4} {y0} M{x5} {ya} H{x6} M{x5} {yb} H{x6}'


def won(cx, cy, k):
    # ₩ 기호(선): 중심 cx,cy, 크기 k(1 = 높이 약 50)
    d = WON.format(x0=cx-22*k, y0=cy-25*k, x1=cx-11*k, y2=cy+25*k, xm=cx, y1=cy-2*k, x3=cx+11*k, x4=cx+22*k,
                   x5=cx-26*k, x6=cx+26*k, ya=cy-6*k, yb=cy+8*k)
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{round(9*k)}"/>'


def won_stack():
    # r2: 지폐 2장, 오른쪽 줄 삭제, ₩ 원 1.6배·지폐 가운데 쪽. 실제 지폐 도안·초상·액면·은행명 없음
    b = f'<rect x="96" y="186" width="340" height="190" rx="18" {s("#f2e7a6")}/>'
    b += f'<rect x="76" y="150" width="340" height="190" rx="18" {s(YEL)}/>'
    b += f'<rect x="326" y="146" width="52" height="198" {s(WHITE)}/>'  # 띠지
    b += f'<circle cx="206" cy="245" r="66" {s(WHITE, 12)}/>' + won(206, 247, 1.45)
    return b


def calendar(accent=False):
    # r2: 날짜 칸 3x3, '그날'은 큰 잉크 칸
    b = f'<rect x="96" y="112" width="320" height="300" rx="26" {s(WHITE)}/>'
    b += f'<path d="M96 138 a26 26 0 0 1 26 -26 H390 a26 26 0 0 1 26 26 V196 H96 Z" {s(ORG if accent else YEL)}/>'
    for x in (176, 336):
        b += f'<rect x="{x-12}" y="76" width="24" height="76" rx="12" {s(G1, 10)}/>'
    for r in range(3):
        for c in range(3):
            x, y = 150 + c * 80, 232 + r * 60
            if (r, c) == (1, 1):  # r2b: 동그라미가 칸과 겹쳐 지저분 → '그날'은 1.5배 잉크 칸 하나
                b += f'<rect x="{x-12}" y="{y-10}" width="76" height="58" rx="10" fill="{INK}"/>'
            else:
                b += f'<rect x="{x}" y="{y}" width="52" height="38" rx="8" fill="{G1}"/>'
    return b


def rate_up():
    # r2: 막대 2개 같은 회색, 화살촉 1.3배
    b = ''
    for i, h in enumerate((120, 200)):
        x = 120 + i * 120
        b += f'<rect x="{x}" y="{420-h}" width="84" height="{h}" rx="10" {s(G1)}/>'
    p = 'M86 300 L200 196 L276 250 L364 160'
    b += f'<path d="{p}" fill="none" stroke="{INK}" stroke-width="{SW+26}"/>'
    b += f'<path d="{p}" fill="none" stroke="{YEL}" stroke-width="{SW+4}"/>'
    b += f'<path d="M300 132 L430 92 L398 222 Z" {s(YEL)}/>'
    return b


def apartment():
    # r3: 한국 아파트 — 세로로 높은 판상형 2동(앞동 7층·뒷동), 층마다 발코니 띠, 옥탑, 노란 창 하나
    # (2차 심사: 4층 정사각은 사무실·서랍장으로 읽힘 → 높이:너비 1.5:1, 층 늘림)
    b = f'<rect x="300" y="150" width="140" height="276" rx="8" {s(G1)}/>'  # 뒷동
    for r in range(5):
        b += f'<path d="M300 {196+r*46} H440" stroke="{INK}" stroke-width="10" fill="none"/>'
    b += f'<text x="384" y="184" text-anchor="middle" font-family="Pretendard, Arial, sans-serif" font-weight="800" font-size="34" fill="{INK}">101</text>'  # 동 번호(한국 아파트 표지)
    b += f'<rect x="158" y="42" width="84" height="44" rx="6" {s(G1)}/>'  # 옥탑
    b += f'<rect x="80" y="80" width="240" height="346" rx="8" {s(WHITE)}/>'
    for r in range(7):
        y = 104 + r * 44
        b += f'<path d="M80 {y+30} H320" stroke="{INK}" stroke-width="{SW}" fill="none"/>'  # 발코니 띠
        for c in range(3):
            b += f'<rect x="{104+c*72}" y="{y}" width="48" height="20" rx="4" fill="{YEL if (r, c) == (2, 2) else G2}"/>'
    b += f'<path d="M48 426 H464" stroke="{INK}" stroke-width="{SW}" fill="none"/>'
    return b


def chip():
    # r2: 다리 변마다 4개, 가운데 다이 + 코어 사각. 회사 로고 없음
    b = ''
    for i in range(4):
        p = 186 + i * 47
        b += f'<path d="M{p} 84 V136 M{p} 376 V428 M84 {p} H136 M376 {p} H428" stroke="{INK}" stroke-width="{SW+2}" fill="none"/>'
    b += f'<rect x="126" y="126" width="260" height="260" rx="28" {s(INK)}/>'
    b += f'<rect x="186" y="186" width="140" height="140" rx="14" {s(YEL, 10)}/>'
    b += f'<rect x="226" y="226" width="60" height="60" rx="8" fill="{INK}"/>'  # r2b: 2x2 격자가 OS 로고를 닮았다(제미나이 2차) → 가운데 코어 하나
    b += f'<circle cx="162" cy="162" r="11" fill="{G1}"/>'
    return b


def bill():
    # r2: 종이 줄 2개(맨 위 잉크 굵게) + 노란 금액 띠(₩ + 막대) → '고지서'로 읽히게. 기관 이름·서식 없음
    b = f'<rect x="146" y="44" width="240" height="250" rx="12" {s(WHITE)}/>'
    b += f'<rect x="180" y="80" width="150" height="{SW+4}" rx="9" fill="{INK}"/>'
    b += f'<rect x="180" y="116" width="110" height="14" rx="7" fill="{G1}"/>'
    b += f'<rect x="174" y="146" width="184" height="58" rx="10" fill="{YEL}" stroke="{INK}" stroke-width="10"/>'
    b += won(206, 175, 0.66) + f'<rect x="236" y="168" width="100" height="14" rx="7" fill="{INK}"/>'
    b += f'<path d="M80 230 H432 V420 a14 14 0 0 1 -14 14 H94 a14 14 0 0 1 -14 -14 Z" {s(G1)}/>'
    b += f'<path d="M80 236 L256 344 L432 236" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
    return b


GOLD2 = '#e6bf00'  # 노랑 한 단계 진한 면(금괴 윗면·뒷장) — 1세트 '다음에 고칠 것'의 지폐 뒷장 색


def bankbook():
    # R-1(2026-10-05): 예금 통장 — 펼친 통장 한 권, 왼쪽 등 띠, 금액 줄 3개 중 맨 아래만 노랑+₩. 은행 이름·로고·서식 없음
    b = f'<rect x="70" y="112" width="372" height="288" rx="22" {s(G1)}/>'  # 뒤표지
    b += f'<rect x="92" y="94" width="350" height="288" rx="20" {s(WHITE)}/>'
    b += f'<rect x="92" y="94" width="62" height="288" rx="20" {s(INK)}/>'  # 등 띠
    for i in range(2):
        y = 160 + i * 62
        b += f'<rect x="190" y="{y}" width="{200 - i*50}" height="16" rx="8" fill="{G1}"/>'
    b += f'<rect x="180" y="282" width="228" height="66" rx="12" fill="{YEL}" stroke="{INK}" stroke-width="10"/>'
    b += won(222, 315, 0.78) + f'<rect x="256" y="306" width="128" height="18" rx="9" fill="{INK}"/>'
    return b


def gold_bar():
    # R-1: 금괴 3개 피라미드(사다리꼴 옆면 + 진한 윗면). 각인·제련소 표시·순도 숫자 없음
    def bar(x, y):
        w, h, t = 176, 92, 34  # 아래 폭·높이·윗면 들여쓰기
        side = f'M{x} {y+h} L{x+t} {y} H{x+w-t} L{x+w} {y+h} Z'
        top = f'M{x+t} {y} L{x+t+14} {y-26} H{x+w-t-14} L{x+w-t} {y} Z'
        return f'<path d="{top}" {s(GOLD2, 12)}/><path d="{side}" {s(YEL)}/>' +             f'<path d="M{x+t+18} {y+28} H{x+t+60}" stroke="{WHITE}" stroke-width="12" fill="none"/>'  # 반사 한 줄
    return bar(80, 330) + bar(256, 330) + bar(168, 238)  # 윗괴 바닥 = 아랫괴 윗면(330)


def us_index():
    # R-1: 미국 지수(S&P500 자리) — 오르는 꺾은선 판 + 왼쪽 위 별 3개 띠(미국 국기를 줄인 표지, 실제 국기 도안 아님). 운용사·지수 회사 로고 없음
    b = f'<rect x="72" y="96" width="368" height="320" rx="24" {s(WHITE)}/>'
    b += f'<path d="M72 120 a24 24 0 0 1 24 -24 H416 a24 24 0 0 1 24 24 V170 H72 Z" {s(INK)}/>'
    for i in range(3):
        cx = 120 + i * 52
        pts = ' '.join(f'{cx + r * __import__("math").sin(k * 3.14159 / 5):.0f},{133 - r * __import__("math").cos(k * 3.14159 / 5):.0f}'
                       for k, r in zip(range(10), [18, 7] * 5))
        b += f'<polygon points="{pts}" fill="{WHITE}"/>'
    for y in (240, 310):
        b += f'<path d="M104 {y} H408" stroke="{G1}" stroke-width="8" fill="none"/>'
    p = 'M104 380 L176 330 L236 352 L310 262 L392 214'
    b += f'<path d="{p}" fill="none" stroke="{INK}" stroke-width="{SW+26}"/>'
    b += f'<path d="{p}" fill="none" stroke="{YEL}" stroke-width="{SW+4}"/>'
    b += f'<circle cx="392" cy="214" r="20" {s(YEL, 10)}/>'
    return b


def div_coins():
    # R-1: 배당(SCHD 자리) — 동전 3개 쌓임 + 위에서 떨어지는 동전 하나(분배금). $ 표시는 글자 하나, 운용사 로고 없음
    b = ''
    for i in range(3):
        y = 380 - i * 54
        b += f'<path d="M110 {y} V{y-34} A110 36 0 0 1 330 {y-34} V{y} A110 36 0 0 1 110 {y} Z" {s(GOLD2)}/>'
        b += f'<ellipse cx="220" cy="{y-34}" rx="110" ry="36" {s(YEL)}/>'
    b += f'<circle cx="372" cy="128" r="70" {s(YEL)}/>'
    b += f'<text x="372" y="160" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="92" fill="{INK}">$</text>'
    b += f'<path d="M372 222 V262 M352 244 L372 266 L392 244" stroke="{INK}" stroke-width="{SW}" fill="none"/>'  # 아래로 떨어짐
    return b


OBJS = {'won_stack': (won_stack, '지폐 묶음(원화 기호)'), 'calendar': (calendar, '달력(마감일)'),
        'rate_up': (rate_up, '오름 화살표(금리·수익률)'), 'apartment': (apartment, '아파트'),
        'chip': (chip, '반도체 칩(로고 없음)'), 'bill': (bill, '고지서 봉투'),
        'bankbook': (bankbook, '예금 통장'), 'gold_bar': (gold_bar, '금괴'), 'us_index': (us_index, '미국 지수 꺾은선'), 'div_coins': (div_coins, '배당 동전')}


def svg(k):
    f, n = OBJS[k]
    return wrap(f(), n)
