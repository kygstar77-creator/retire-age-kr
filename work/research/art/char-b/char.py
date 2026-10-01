# 캐릭터 SVG 2안 — 같은 사람(퇴사한 40대 초반 직장인, 이름·말풍선 없음), 다른 그림체
# r3: 고지서 머리띠 노랑·윗줄 잉크, b 눈썹 걱정형·7.5·고지서 몸에서 뗌(2차 심사)
# r2(2026-10-01 15시): 심사 반영 — 머리 0.88배(어린이처럼 보임 → 나이 올림), 관자놀이 흰머리·눈 밑 주름,
# 고지서 머리띠 주황 → 회색(주황은 썸네일 강조 숫자 하나), 땀방울 흰색, b는 흰 테두리·정장 밝힘·입·눈썹 2배.
INK, SKIN, HAIR, GREY, NAVY, SHIRT, PANTS = '#18191d', '#f6d2b5', '#23262d', '#b9bec8', '#2b3a67', '#ffffff', '#d8c3a0'
STRIPE = '#ffd400'  # r3: 회색은 320px에서 흰 종이로만 보임 → 썸네일 노랑 줄과 같은 색, 두께 1.4배
HEAD = 'transform="translate(150 206) scale(.88) translate(-150 -206)"'
HAIR_D = 'M64 118 Q60 30 150 28 Q240 30 236 118 Q226 78 196 70 Q178 92 140 80 Q110 92 84 84 Q70 96 64 118 Z'


def paper(x, y, w, h, rot, stroke):
    # r3: 맨 윗줄은 잉크 2배 굵기(금액 줄로 읽히게)
    lines = ''.join(f'<rect x="{x+12}" y="{y+24+i*13}" width="{w-24-(18 if i == 3 else 0)}" height="{10 if i == 0 else 5}" rx="2.5" fill="{INK if i == 0 else "#c9ccd3"}"/>' for i in range(4))
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fff" {stroke}/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="5" fill="{STRIPE}"/>{lines}</g>')


def body_a(st, arm_w=26, arm_c=NAVY, face=True):
    # 놀람: 두 손으로 고지서를 든 채 굳음
    f = f'''
  <path d="M68 112 Q66 92 74 84 L80 112 Z" fill="{GREY}"/><path d="M232 112 Q234 92 226 84 L220 112 Z" fill="{GREY}"/>
  <path d="M104 98 Q118 84 132 96" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
  <path d="M168 96 Q182 84 196 98" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
  <circle cx="120" cy="126" r="17" fill="#fff" {st}/><circle cx="180" cy="126" r="17" fill="#fff" {st}/>
  <circle cx="120" cy="128" r="6" fill="{INK}"/><circle cx="180" cy="128" r="6" fill="{INK}"/>
  <path d="M106 150 Q120 156 134 150 M166 150 Q180 156 194 150" fill="none" stroke="#c99a7c" stroke-width="3" stroke-linecap="round"/>
  <ellipse cx="150" cy="176" rx="13" ry="17" fill="#7a2b2b" {st}/>
  <path d="M244 70 q10 16 0 22 q-10 -6 0 -22Z" fill="#fff" {st}/><path d="M258 104 q8 13 0 18 q-8 -5 0 -18Z" fill="#fff" {st}/><path d="M48 92 q8 13 0 18 q-8 -5 0 -18Z" fill="#fff" {st}/>''' if face else ''
    return f'''
  <ellipse cx="128" cy="402" rx="26" ry="11" fill="{INK}" {st}/><ellipse cx="172" cy="402" rx="26" ry="11" fill="{INK}" {st}/>
  <rect x="110" y="318" width="34" height="84" rx="12" fill="{PANTS}" {st}/><rect x="156" y="318" width="34" height="84" rx="12" fill="{PANTS}" {st}/>
  <rect x="88" y="200" width="124" height="135" rx="44" fill="{NAVY}" {st}/>
  <path d="M130 202 L150 236 L170 202 Z" fill="{SHIRT}" {st}/>
  <path d="M98 230 Q70 270 104 286" fill="none" stroke="{arm_c}" stroke-width="{arm_w}" stroke-linecap="round"/>
  <path d="M202 230 Q230 270 196 286" fill="none" stroke="{arm_c}" stroke-width="{arm_w}" stroke-linecap="round"/>
  {paper(92, 232, 116, 88, -4, st)}
  <circle cx="98" cy="282" r="15" fill="{SKIN}" {st}/><circle cx="202" cy="276" r="15" fill="{SKIN}" {st}/>
  <g {HEAD}><circle cx="150" cy="118" r="88" fill="{SKIN}" {st}/>
  <path d="{HAIR_D}" fill="{HAIR}" {st}/>{f}</g>'''


def svg_a():
    st = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"'
    sticker = body_a('stroke="#fff" stroke-width="30" stroke-linejoin="round"', 56, '#fff', face=False)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -10 340 450" width="600" height="794">'
            f'<g>{sticker}</g><g>{body_a(st, 36, INK, face=False)}</g><g>{body_a(st)}</g></svg>')


def body_b(fill_override=None):
    sh, nv = '#2c3f78', 'url(#n)'
    sk = 'url(#f)'
    if fill_override:
        sh = nv = sk = fill_override
    o = fill_override
    face = '' if o else f'''
  <path d="M68 112 Q66 92 74 84 L80 112 Z" fill="{GREY}"/><path d="M232 112 Q234 92 226 84 L220 112 Z" fill="{GREY}"/>
  <path d="M100 110 Q118 104 134 94" fill="none" stroke="{INK}" stroke-width="7.5" stroke-linecap="round"/>
  <path d="M166 94 Q182 104 200 110" fill="none" stroke="{INK}" stroke-width="7.5" stroke-linecap="round"/>
  <circle cx="122" cy="134" r="8" fill="{INK}"/><circle cx="180" cy="134" r="8" fill="{INK}"/>
  <path d="M108 154 Q122 160 136 154 M166 154 Q180 160 194 154" fill="none" stroke="#c99a7c" stroke-width="3" stroke-linecap="round"/>
  <path d="M126 180 q8 -9 16 0 q8 9 16 0 q8 -9 16 0" fill="none" stroke="#7a2b2b" stroke-width="10" stroke-linecap="round"/>'''
    return f'''
  <ellipse cx="128" cy="404" rx="24" ry="11" fill="{o or '#2a2d34'}"/><ellipse cx="172" cy="404" rx="24" ry="11" fill="{o or '#2a2d34'}"/>
  <rect x="112" y="318" width="32" height="86" rx="12" fill="{o or PANTS}"/><rect x="156" y="318" width="32" height="86" rx="12" fill="{o or '#c8b18c'}"/>
  <rect x="90" y="200" width="120" height="136" rx="44" fill="{nv}"/>
  <path d="M130 202 L150 236 L170 202 Z" fill="{o or '#fff'}"/>
  <path d="M206 236 Q240 296 222 306" fill="none" stroke="{sh}" stroke-width="{56 if o else 26}" stroke-linecap="round"/>
  {'' if o else paper(196, 250, 92, 72, -8, 'stroke="#d0d4da" stroke-width="3"')}
  <circle cx="222" cy="300" r="{28 if o else 14}" fill="{sk}"/>
  <g {HEAD}><circle cx="150" cy="118" r="88" fill="{sk}" {f'stroke="{o}" stroke-width="30"' if o else ''}/>
  <path d="{HAIR_D}" fill="{o or HAIR}" {f'stroke="{o}" stroke-width="30" stroke-linejoin="round"' if o else ''}/>{face}
  <path d="M96 232 Q52 180 78 92" fill="none" stroke="{nv if not o else o}" stroke-width="{56 if o else 26}" stroke-linecap="round"/>
  <ellipse cx="88" cy="86" rx="{34 if o else 20}" ry="{29 if o else 15}" fill="{sk}" transform="rotate(-25 88 86)"/></g>'''


def svg_b():
    # 걱정: 한 손은 이마, 한 손은 고지서를 배 앞에서 내려다봄. 검은 외곽선 없이 면+그늘, 둘레만 흰 테두리
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -10 340 450" width="600" height="794">
  <defs><radialGradient id="f" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#ffe2cc"/><stop offset="1" stop-color="#eebc98"/></radialGradient>
  <linearGradient id="n" x1="0" x2="1"><stop offset="0" stop-color="#4d6bb3"/><stop offset="1" stop-color="#3a5698"/></linearGradient>
  <filter id="g"><feMorphology operator="dilate" radius="7"/></filter></defs>
  <g filter="url(#g)">{body_b('#ffffff')}</g>
  {body_b()}
</svg>'''
