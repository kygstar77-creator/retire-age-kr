# G-1 '금값 영수증 4장' 썸네일 시안(2026-10-07 visual-designer, PD 06:22 요청) — py -3.12 make_thumbs.py [g1a,g1b,...]
# 문구: ep/G-1/meta.json thumb_text '1월 고점에 샀다면 -33.7%'(copywriter 1위, 10/6 기준 재심사 8.50). 제목 = 만원 범위, 썸네일 = %(숫자 겹침 0).
# 숫자: ep/G-1/calc_out.txt에서 읽음(공개 전날 calc 재실행 → 다시 돌리면 숫자만 바뀜). 그래프 = raw/calc_<asof>.json KRX M04020000 일별 종가.
# 경쟁과 다른 점: 경쟁 5 = 금괴 사진·앵커 얼굴·아래 두 줄 테두리 글씨. 우리 = 사진·얼굴·테두리 0, 실제 KRX 종가 선 또는 영수증 한 장.
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576, 아래 5%(y≥684) 글자 없음 — 렌더 뒤 자동 검사(zones.json).
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'G-1')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
meta = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))
ASOF = re.search(r'기준일 (\d{4}-\d\d-\d\d)', calc).group(1)
m = re.search(r'1년 고점 (\d{4})-(\d\d)-(\d\d) [\d,]+원/g · 고점 대비 (-[\d.]+)%', calc)
PEAK_DAY, PEAK_M, PEAK_D, DROP = f'{m.group(1)}-{m.group(2)}-{m.group(3)}', int(m.group(2)), int(m.group(3)), float(m.group(4))
PCT = f'{DROP:.1f}%'.replace('-', '−')
assert meta['thumb_text'] == f'{PEAK_M}월 고점에 샀다면 {DROP:.1f}%', (meta['thumb_text'], DROP)
start = re.search(r'\| 1년 전 (\d{4}-\d\d-\d\d) \(', calc).group(1)
krx = json.load(open(os.path.join(EP, 'raw', f'calc_{ASOF}.json'), encoding='utf-8'))['KRX_M04020000_won_per_g']
SER = [(d, v) for d, v in sorted(krx.items()) if start <= d <= ASOF]
assert SER[-1][0] == ASOF and max(v for _, v in SER) == krx[PEAK_DAY]
Y0 = ASOF.replace('-', '.'); S0 = start.replace('-', '.')

INK, RED, GOLD, CREAM, NAVY, GREY, BG = '#16181D', '#E5322D', '#C8900E', '#F6F1E7', '#1E2A44', '#6B7280', '#121418'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]


def line(x0, y0, w, h, color, peak_col, lw=10):
    """KRX 일별 종가 선(SVG). 고점부터 지금까지 빨강. (svg, 고점 좌표, 지금 좌표)"""
    vs = [v for _, v in SER]; lo, hi = min(vs), max(vs); n = len(vs) - 1
    pts = [(x0 + w * i / n, y0 + h * (1 - (v - lo) / (hi - lo))) for i, v in enumerate(vs)]
    ip = vs.index(hi)
    P = lambda ps: ' '.join(f'{x:.1f},{y:.1f}' for x, y in ps)
    s = (f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
         f"<polyline points='{P(pts[:ip + 1])}' fill='none' stroke='{color}' stroke-width='{lw}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<polyline points='{P(pts[ip:])}' fill='none' stroke='{peak_col}' stroke-width='{lw + 4}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<circle cx='{pts[ip][0]:.1f}' cy='{pts[ip][1]:.1f}' r='{lw * 2.2}' fill='{peak_col}' stroke='#fff' stroke-width='6'/>"
         f"<circle cx='{pts[-1][0]:.1f}' cy='{pts[-1][1]:.1f}' r='{lw * 1.6}' fill='{peak_col}' stroke='#fff' stroke-width='6'/></svg>")
    return s, pts[ip], pts[-1]


# g1a — 밝은 크림 판(우리 조회 1위 A-1 계열) + 실제 KRX 1년 선(오른쪽 위), 1월 고점부터 빨강, 큰 숫자 하나(왼쪽 아래)
_s, pk, now = line(790, 250, 430, 290, NAVY, RED)
g1a = f"""<div style='position:absolute;inset:0;background:{CREAM}'></div>
{_s}
<div class='t' style='left:{pk[0] + 34:.0f}px;top:{pk[1] - 40:.0f}px;font-size:52px;color:{RED}'>1월 고점</div>
<div class='t' style='left:52px;top:44px;font-size:118px;color:{INK}'><span style='color:{GOLD}'>금</span>, 1월 고점에</div>
<div class='t' style='left:52px;top:180px;font-size:118px;color:{INK}'>샀다면</div>
<div id='a1' class='t' data-fit='720' style='left:40px;top:350px;font-size:250px;color:{RED}'>{PCT}</div>
<div class='fine' style='color:{GREY};top:640px;font-size:22px'>KRX 금시장 1g 종가 {S0}~{Y0} · 지나간 값 · 투자 권유 아님</div>
"""

# g1b — 어두운 판 + 영수증 한 장(편의 장치 '영수증 4장' 중 가장 아픈 칸): 낸 돈 1,000만원 → 결과 %만, 663만원은 제목 몫이라 안 씀
RCPT_CLIP = 'polygon(0 0,100% 0,100% 96%,' + ','.join(f'{100 - 5 * i}% {100 if i % 2 else 96}%' for i in range(1, 20)) + ',0 96%)'
g1b = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div class='t' style='left:52px;top:52px;font-size:112px;color:#fff'><span style='color:#F2B92B'>금</span> 1천만원,</div>
<div class='t' style='left:52px;top:184px;font-size:112px;color:#fff'>1월 고점에</div>
<div class='t' style='left:52px;top:316px;font-size:112px;color:#fff'>샀다면</div>
<div style='position:absolute;left:650px;top:34px;width:560px;height:500px;background:#FBFAF6;transform:rotate(4deg);clip-path:{RCPT_CLIP}'>
  <div class='t' style='left:40px;top:34px;font-size:58px;color:{INK}'>영수증 · 금</div>
  <div style='position:absolute;left:40px;right:40px;top:116px;border-top:5px dashed #9AA0AA'></div>
  <div class='lab' style='left:40px;top:142px;font-size:40px;color:{INK}'>산 날 {PEAK_M}월 {PEAK_D}일 (1년 고점)</div>
  <div class='lab' style='left:40px;top:202px;font-size:40px;color:{INK}'>낸 돈 1,000만원</div>
  <div style='position:absolute;left:40px;right:40px;top:270px;border-top:5px dashed #9AA0AA'></div>
  <div id='b1' class='t' data-fit='480' style='left:34px;top:296px;font-size:170px;color:{RED}'>{PCT}</div>
</div>
<div class='fine' style='color:#9AA0AA;top:640px;font-size:22px'>KRX 금시장 종가 기준 {Y0} · 지나간 값 · 투자 권유 아님</div>
"""

# g1c — 크림 판 + 같은 1년 선을 크게(그림이 주인공), 글자는 위 한 줄·큰 숫자 하나(선 아래 왼쪽)
_s2, pk2, now2 = line(60, 236, 1150, 230, NAVY, RED, lw=12)
g1c = f"""<div style='position:absolute;inset:0;background:{CREAM}'></div>
{_s2}
<div id='c0' class='t' data-fit='1180' style='left:48px;top:36px;font-size:112px;color:{INK}'><span style='color:{GOLD}'>금</span>, 1월 고점에 샀다면</div>
<div class='t' style='left:{pk2[0] + 36:.0f}px;top:{pk2[1] - 44:.0f}px;font-size:54px;color:{RED}'>1월 고점</div>
<div id='c1' class='t' data-fit='640' style='left:48px;top:440px;font-size:190px;color:{RED}'>{PCT}</div>
<div class='fine' style='color:{GREY};top:640px;font-size:22px'>KRX 금시장 1g 종가 {S0}~{Y0} · 지나간 값 · 투자 권유 아님</div>
"""
VARIANTS = {'g1a': g1a, 'g1b': g1b, 'g1c': g1c}

# ── 2차(09:4x) — 1차 세 명 평균 g1a 6.98(제미나이 7.5·7 / Claude 7.0 / 레드팀 6.7) · g1b 6.98(6.5·8 / 6.3 / 7.4) · g1c 6.73(7·6 / 7.2 / 6.5).
#    레드팀(g1b 1위): 영수증 안 두 줄이 168px에서 안 읽힘 → 한 줄로 합쳐 키우기, 산 길 'KRX 금시장'·기준일 표기(골드바면 -39.7%라 '금 사면 다'로 오독), 뒤에 영수증 3장 겹쳐 '4장 중 한 장'.
#    Claude(g1c 1위): 제목 한 줄이 길어 작다 → '1월 고점에 샀다면' 짧게·크게, 크림 바탕 한 단계 진하게. 663만원은 제목 숫자라 썸네일에 안 넣음(copy/titles.md 숫자 겹침 0).
def receipt(x, y, w, h, rot, inner=''):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#FBFAF6;transform:rotate({rot}deg);"
            f"clip-path:{RCPT_CLIP};box-shadow:0 0 0 2px #C9CED8'>{inner}</div>")
g1d = f"""<div style='position:absolute;inset:0;background:{NAVY}'></div>
<div class='t' style='left:52px;top:46px;font-size:150px;color:#F2B92B'>금</div>
<div class='t' style='left:52px;top:214px;font-size:116px;color:#fff'>1월 고점에</div>
<div class='t' style='left:52px;top:350px;font-size:116px;color:#fff'>샀다면</div>
{receipt(700, 70, 520, 470, -9)}{receipt(690, 54, 520, 470, -5)}{receipt(680, 40, 520, 470, 9)}
{receipt(640, 30, 560, 520, 3, f'''
  <div class='t' style='left:36px;top:32px;font-size:62px;color:{INK}'>KRX 금 1,000만원</div>
  <div style='position:absolute;left:36px;right:36px;top:118px;border-top:6px dashed #9AA0AA'></div>
  <div class='t' style='left:36px;top:146px;font-size:62px;color:{INK}'>산 날 {PEAK_M}월 {PEAK_D}일</div>
  <div id='d1' class='t' data-fit='500' style='left:28px;top:250px;font-size:210px;color:{RED}'>{PCT}</div>
  <div class='lab' style='left:38px;top:460px;font-size:34px;color:{GREY}'>{ASOF[5:7].lstrip('0')}/{ASOF[8:].lstrip('0')} 종가 기준</div>''')}
<div class='fine' style='color:#AEB6C6;top:640px;font-size:22px'>KRX 금시장 종가 {Y0} 기준 · 지나간 값 · 투자 권유 아님</div>
"""

_s3, pk3, now3 = line(60, 250, 1150, 220, NAVY, RED, lw=13)
g1e = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
{_s3}
<div class='t' style='left:44px;top:30px;font-size:150px;color:{INK}'><span style='color:{GOLD}'>금</span> 1월 고점에 샀다면</div>
<div class='t' style='left:{pk3[0] + 36:.0f}px;top:{pk3[1] - 46:.0f}px;font-size:56px;color:{RED}'>1월 고점</div>
<div class='t' style='left:{now3[0] - 120:.0f}px;top:{now3[1] + 30:.0f}px;font-size:48px;color:{NAVY}'>10/6</div>
<div id='e1' class='t' data-fit='700' style='left:44px;top:452px;font-size:200px;color:{RED}'>{PCT}</div>
<div class='fine' style='color:{GREY};top:650px;font-size:22px'>KRX 금시장 1g 종가 {S0}~{Y0} · 지나간 값 · 투자 권유 아님</div>
"""
assert ASOF == '2026-10-06'  # g1e '10/6' 라벨 — 기준일 바뀌면 고칠 것
VARIANTS.update(g1d=g1d, g1e=g1e)

# ── 3차(10:0x) — 2차 세 명 평균 g1e 7.23(제미나이 7·7 / Claude 7.3 / 레드팀 7.4) 통과 · g1a 6.97 · g1d 6.70.
#    레드팀: 나머지 산 날 3개를 숫자 없는 점으로(영수증 4장 연결·'다른 날은?') · 'KRX 금시장' 꼬리표를 큰 숫자 옆으로 · '10/6' 라벨 빼기 · 마이너스 붙이기.
#    Claude: 선 아래 금색 면(사진 없이 금 신호) · 끝점 위로.
BUY = [re.search(rf'\| {k} (\d{{4}}-\d\d-\d\d) \(', calc).group(1) for k in ('1년 전', '3개월 전', '1개월 전')]
def line_fill(x0, y0, w, h, lw=13):
    vs = [v for _, v in SER]; ds = [d for d, _ in SER]; lo, hi = min(vs), max(vs); n = len(vs) - 1
    pts = [(x0 + w * i / n, y0 + h * (1 - (v - lo) / (hi - lo))) for i, v in enumerate(vs)]
    ip = vs.index(hi); P = lambda ps: ' '.join(f'{x:.1f},{y:.1f}' for x, y in ps)
    s = (f"<svg style='position:absolute;left:0;top:0' width='1280' height='720'>"
         f"<polygon points='{P(pts)} {pts[-1][0]:.1f},{y0 + h + 40} {pts[0][0]:.1f},{y0 + h + 40}' fill='#E9C766' opacity='.55'/>"
         f"<polyline points='{P(pts[:ip + 1])}' fill='none' stroke='{NAVY}' stroke-width='{lw}' stroke-linejoin='round' stroke-linecap='round'/>"
         f"<polyline points='{P(pts[ip:])}' fill='none' stroke='{RED}' stroke-width='{lw + 4}' stroke-linejoin='round' stroke-linecap='round'/>")
    for d in BUY:
        x, y = pts[ds.index(d)]; s += f"<circle cx='{x:.1f}' cy='{y:.1f}' r='15' fill='#fff' stroke='{NAVY}' stroke-width='7'/>"
    s += (f"<circle cx='{pts[ip][0]:.1f}' cy='{pts[ip][1]:.1f}' r='{lw * 2.2}' fill='{RED}' stroke='#fff' stroke-width='6'/>"
          f"<circle cx='{pts[-1][0]:.1f}' cy='{pts[-1][1]:.1f}' r='{lw * 1.4}' fill='{RED}' stroke='#fff' stroke-width='6'/></svg>")
    return s, pts[ip]
_s4, pk4 = line_fill(60, 236, 1100, 200)
g1f = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
{_s4}
<div class='t' style='left:44px;top:30px;font-size:150px;color:{INK}'><span style='color:{GOLD}'>금</span> 1월 고점에 샀다면</div>
<div class='t' style='left:{pk4[0] + 36:.0f}px;top:{pk4[1] - 46:.0f}px;font-size:56px;color:{RED}'>1월 고점</div>
<div id='f1' class='t' data-fit='640' style='left:40px;top:462px;font-size:200px;color:{RED};letter-spacing:-6px'>{PCT}</div>
<div class='t' style='left:690px;top:494px;font-size:58px;color:{INK}'>KRX 금시장</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>KRX 금시장 1g 종가 {S0}~{Y0} · 흰 점 = 다른 산 날 3개 · 지나간 값 · 투자 권유 아님</div>
"""
VARIANTS['g1f'] = g1f


# ── 교체용 예비판(10:1x) — 48h CTR이 채널 중앙값 아래일 때 title_swap과 짝으로 한 번만. 문구 = meta.json thumb_text_swap(copywriter 07:52 '산 값 되찾으려면 +50.7%').
#    g1f 판 그대로(선·금색 면·흰 점) + 지금 점에서 고점 높이까지 점선. 아직 심사 전 — 교체 결정 때 같은 판에서 3명 심사.
UP = re.search(r'산 값\(고점\)으로 돌아가려면 (\+[\d.]+)%', calc).group(1)
assert meta['thumb_text_swap'] == f'산 값 되찾으려면 {UP}%', meta['thumb_text_swap']
_s5, pk5 = line_fill(60, 236, 1100, 200)
g1s = f"""<div style='position:absolute;inset:0;background:#EFE4CC'></div>
{_s5}
<div style='position:absolute;left:{pk5[0]:.0f}px;top:{pk5[1] - 3:.0f}px;width:{1160 - pk5[0]:.0f}px;border-top:7px dashed {NAVY}'></div>
<div class='t' style='left:44px;top:30px;font-size:150px;color:{INK}'><span style='color:{GOLD}'>금</span> 산 값 되찾으려면</div>
<div class='t' style='left:{pk5[0] + 36:.0f}px;top:{pk5[1] - 66:.0f}px;font-size:56px;color:{RED}'>1월 고점에 산 값</div>
<div id='s1' class='t' data-fit='640' style='left:40px;top:462px;font-size:200px;color:{NAVY};letter-spacing:-6px'>{UP}%</div>
<div class='t' style='left:690px;top:494px;font-size:58px;color:{INK}'>KRX 금시장</div>
<div class='fine' style='color:{GREY};top:652px;font-size:20px'>KRX 금시장 1g 종가 {S0}~{Y0} · 전망 아님, 산수 · 투자 권유 아님</div>
"""
VARIANTS['g1s'] = g1s


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||e.closest('svg')||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")


def main(keys):
    zp = os.path.join(HERE, 'zones.json')
    report = json.load(open(zp, encoding='utf-8')) if os.path.exists(zp) else {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k in keys:
            html = os.path.join(HERE, f'{k}.html')
            open(html, 'w', encoding='utf-8').write(HEAD + VARIANTS[k] + '\n' + TAIL)
            pg.goto('file:///' + html.replace(chr(92), '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
            report[k] = check_zones(pg)
            im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    print('기준일', ASOF, '고점', PEAK_DAY, PCT, '선 점', len(SER))
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
