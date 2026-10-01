# 캐릭터 SVG 2안 — 같은 사람(퇴사한 40대 초반 직장인, 이름·말풍선 없음), 다른 그림체
INK, SKIN, HAIR, NAVY, SHIRT, PANTS, ORANGE = '#18191d', '#f6d2b5', '#23262d', '#2b3a67', '#ffffff', '#d8c3a0', '#ff5a00'


def paper(x, y, w, h, rot, stroke):
    lines = ''.join(f'<rect x="{x+12}" y="{y+22+i*13}" width="{w-24-(18 if i == 3 else 0)}" height="5" rx="2.5" fill="#c9ccd3"/>' for i in range(4))
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fff" {stroke}/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="10" rx="5" fill="{ORANGE}"/>{lines}</g>')


def body_a(st, arm_w=26, arm_c=NAVY):
    # 놀람: 두 손으로 고지서를 든 채 굳음
    return f'''
  <ellipse cx="128" cy="402" rx="26" ry="11" fill="{INK}" {st}/><ellipse cx="172" cy="402" rx="26" ry="11" fill="{INK}" {st}/>
  <rect x="110" y="318" width="34" height="84" rx="12" fill="{PANTS}" {st}/><rect x="156" y="318" width="34" height="84" rx="12" fill="{PANTS}" {st}/>
  <rect x="88" y="200" width="124" height="135" rx="44" fill="{NAVY}" {st}/>
  <path d="M130 202 L150 236 L170 202 Z" fill="{SHIRT}" {st}/>
  <path d="M98 230 Q70 270 104 286" fill="none" stroke="{arm_c}" stroke-width="{arm_w}" stroke-linecap="round"/>
  <path d="M202 230 Q230 270 196 286" fill="none" stroke="{arm_c}" stroke-width="{arm_w}" stroke-linecap="round"/>
  {paper(92, 232, 116, 88, -4, st)}
  <circle cx="98" cy="282" r="15" fill="{SKIN}" {st}/><circle cx="202" cy="276" r="15" fill="{SKIN}" {st}/>
  <circle cx="150" cy="118" r="88" fill="{SKIN}" {st}/>
  <path d="M64 118 Q60 30 150 28 Q240 30 236 118 Q226 78 196 70 Q178 92 140 80 Q110 92 84 84 Q70 96 64 118 Z" fill="{HAIR}" {st}/>
  <path d="M104 98 Q118 84 132 96" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <path d="M168 96 Q182 84 196 98" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <circle cx="120" cy="126" r="17" fill="#fff" {st}/><circle cx="180" cy="126" r="17" fill="#fff" {st}/>
  <circle cx="120" cy="128" r="6" fill="{INK}"/><circle cx="180" cy="128" r="6" fill="{INK}"/>
  <ellipse cx="150" cy="172" rx="13" ry="17" fill="#7a2b2b" {st}/>
  <path d="M244 70 q10 16 0 22 q-10 -6 0 -22Z" fill="#8ecbff" {st}/><path d="M258 104 q8 13 0 18 q-8 -5 0 -18Z" fill="#8ecbff" {st}/><path d="M48 92 q8 13 0 18 q-8 -5 0 -18Z" fill="#8ecbff" {st}/>'''


def svg_a():
    st = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"'
    sticker = body_a('stroke="#fff" stroke-width="30" stroke-linejoin="round"', 56, '#fff')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -10 340 450" width="600" height="794">'
            f'<g>{sticker}</g><g>{body_a(st, 36, INK)}</g><g>{body_a(st)}</g></svg>')


def svg_b():
    # 걱정: 한 손은 이마, 한 손은 고지서를 멀찍이. 외곽선 없이 면+그늘 2단
    sh = '#1f2b4f'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -10 340 450" width="600" height="794">
  <defs><radialGradient id="f" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#ffe2cc"/><stop offset="1" stop-color="#eebc98"/></radialGradient>
  <linearGradient id="n" x1="0" x2="1"><stop offset="0" stop-color="#34467a"/><stop offset="1" stop-color="{sh}"/></linearGradient></defs>
  <ellipse cx="150" cy="414" rx="70" ry="9" fill="#000" opacity=".12"/>
  <ellipse cx="128" cy="404" rx="24" ry="11" fill="#2a2d34"/><ellipse cx="172" cy="404" rx="24" ry="11" fill="#2a2d34"/>
  <rect x="112" y="318" width="32" height="86" rx="12" fill="{PANTS}"/><rect x="156" y="318" width="32" height="86" rx="12" fill="#c8b18c"/>
  <rect x="90" y="200" width="120" height="136" rx="44" fill="url(#n)"/>
  <path d="M130 202 L150 236 L170 202 Z" fill="#fff"/>
  <path d="M206 228 Q250 240 262 214" fill="none" stroke="{sh}" stroke-width="26" stroke-linecap="round"/>
  {paper(222, 140, 70, 92, 10, '')}
  <circle cx="262" cy="212" r="14" fill="url(#f)"/>
  <circle cx="150" cy="118" r="88" fill="url(#f)"/>
  <path d="M64 118 Q60 30 150 28 Q240 30 236 118 Q226 78 196 70 Q178 92 140 80 Q110 92 84 84 Q70 96 64 118 Z" fill="{HAIR}"/>
  <path d="M100 104 Q116 96 134 108" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <path d="M166 108 Q184 96 200 104" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <circle cx="122" cy="132" r="7" fill="{INK}"/><circle cx="180" cy="132" r="7" fill="{INK}"/>
  <path d="M132 176 q6 -6 12 0 q6 6 12 0 q6 -6 12 0" fill="none" stroke="#7a2b2b" stroke-width="5" stroke-linecap="round"/>
  <path d="M96 232 Q52 180 78 92" fill="none" stroke="url(#n)" stroke-width="26" stroke-linecap="round"/>
  <ellipse cx="88" cy="86" rx="20" ry="15" fill="url(#f)" transform="rotate(-25 88 86)"/>
</svg>'''
