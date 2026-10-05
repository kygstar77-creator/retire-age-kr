# M-1 '월배당 거꾸로' 썸네일 시안(2026-10-06 06시 PD) — py -3.12 make_thumbs.py [m1a,m1b,...]
# 숫자 출처: ep/M-1/calc_out.txt — 월 100만원(세후·건보 뒤) 필요 원금 JEPQ 1.38억 · SCHD 4.85억 · ACE 5.10억, 가장 적은 달 기준 ACE 8.92억(×1.75)
# 문구 출처: ep/M-1/titles.md 썸네일 A(1위)·B(2위) — copywriter 10/5. 제목 T1과 반복 안 함(제목엔 숫자 없음).
# 경쟁과 다른 점(compare.png): 경쟁 5 = 인물 사진·노랑/흰 테두리 글씨·돈다발. 우리 = 인물·사진 0, 막대 하나, 테두리 글씨 0.
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표 자동 검사(zones.json).
import os, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'M-1')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
for s in ('월 100만원: 연 세전 분배 15,611,746원 → 필요 원금 1.38억원', '월 100만원: 연 세전 분배 15,611,746원 → 필요 원금 4.85억원',
          '월 100만원: 연 세전 분배 15,693,413원 → 필요 원금 5.10억원 · 가장 적은 달 기준이면 8.92억원(×1.75)'):
    assert s in calc, s
INK, RED, YEL, GREY, BG = '#16181D', '#FF3B30', '#FFD400', '#8A93A3', '#121418'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
FINE = f"<div class='fine' style='color:{GREY};top:640px;font-size:22px'>2026.10.2 기준 지난 1년 분배 · 세금·건보료 뗀 뒤 · 투자 권유 아님</div>"


def bars(y0, rows, maxv, x0=58, w=860, h=64, gap=26):
    """가로 막대(이름·값). rows = [(이름, 값, 색)]"""
    s = ''
    for i, (name, v, c) in enumerate(rows):
        y = y0 + i * (h + gap); bw = w * v / maxv
        s += f"<div class='lab' style='left:{x0}px;top:{y + 8}px;font-size:56px;color:#fff'>{name}</div>"
        s += f"<div style='position:absolute;left:{x0 + 200}px;top:{y}px;width:{bw:.0f}px;height:{h}px;background:{c};border-radius:6px'></div>"
        s += f"<div class='t' style='left:{x0 + 200 + bw + 18:.0f}px;top:{y + 4}px;font-size:76px;color:{c}'>{v:.2f}억</div>"
    return s


# m1a — 비교(A vs B) + 내 돈 대입: copywriter A 그대로, 숫자마다 이름표
m1a = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div class='t' style='left:54px;top:46px;font-size:104px;color:#fff'>세후 월 <span style='color:{YEL}'>100만원</span> 받으려면</div>
<div id='a1' class='t' data-fit='1170' style='left:46px;top:220px;font-size:230px;color:{RED}'>1.38억 vs 5.10억</div>
<div class='t' style='left:70px;top:430px;font-size:96px;color:#fff'>JEPQ</div>
<div class='t' style='left:790px;top:430px;font-size:96px;color:#fff'>ACE</div>
<div class='lab' style='left:70px;top:556px;font-size:44px;color:{GREY}'>SCHD는 4.85억</div>
"""

# m1b — 반전: copywriter B — 같은 상품, 가장 적은 달로 재면
m1b = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div class='t' style='left:54px;top:46px;font-size:96px;color:#fff'>월 <span style='color:{YEL}'>100만원</span>, 가장 적은 달로 재면</div>
<div id='b1' class='t' data-fit='1170' style='left:46px;top:214px;font-size:240px;color:#fff'>5.10억 <span style='color:{RED}'>→ 8.92억</span></div>
<div class='t' style='left:62px;top:478px;font-size:80px;color:{GREY}'>ACE 미국배당다우존스</div>
"""

# m1c — 질문 + 막대(같은 규칙, 세 상품): 답이 막대 길이로 한눈에
m1c = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='c0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:118px;color:#fff'>월 <span style='color:{YEL}'>100만원</span> 받으려면 얼마?</div>
{bars(232, [('JEPQ', 1.38, '#3D8BFF'), ('SCHD', 4.85, '#C9CED8'), ('ACE', 5.10, RED)], 5.10, w=700, h=84, gap=36)}
"""
VARIANTS = {'m1a': m1a + FINE, 'm1b': m1b + FINE, 'm1c': m1c + FINE}

# ── 2차(06:2x) — 1초 시험(3.1-flash-lite 블라인드)에서 m1b를 '자산이 불어나는 시뮬레이션'으로 잘못 읽음
#    → 윗줄에 '필요한 돈'을 박고, 반전 조건('가장 적은 달로 재면')은 아랫줄로. 8.92억은 노랑(점수 지적).
m1d = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='d0' class='t' data-fit='1170' style='left:54px;top:44px;font-size:104px;color:#fff'>월 <span style='color:{YEL}'>100만원</span>에 필요한 돈</div>
<div id='d1' class='t' data-fit='1170' style='left:46px;top:200px;font-size:250px;color:#fff'>5.10억 <span style='color:{RED}'>→</span> <span style='color:{YEL}'>8.92억</span></div>
<div class='t' style='left:58px;top:470px;font-size:84px;color:{RED}'>가장 적은 달로 재면</div>
<div class='lab' style='left:62px;top:574px;font-size:40px;color:{GREY}'>ACE 미국배당다우존스</div>
"""
VARIANTS['m1d'] = m1d + FINE



# ── 3차(06:2x) — 심사 m1d 제미나이 7.5·7 / Claude 7.0 / 레드팀 6 = 평균 6.75(통과선 7 미달). 공통 지적:
#    ① ACE 이름이 168px에서 안 보임(제목 T1은 JEPQ로 시작해 JEPQ 얘기로 읽힘) ② 윗줄이 제목 T1과 같은 말(월 100만원·가장 적게 나온 달)
#    ③ 화살표가 '시간이 지나 늘었다'로 읽힘 → 숫자 밑에 재는 기준(평균 달·가장 적은 달) 꼬리표.
#    윗줄 = 대본 0장 '매달 분배금이 똑같이 나오지 않거든요'에서 가져옴(지은 말 아님).
m1e = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='e0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:96px;color:#fff'>분배금이 매달 똑같지 않으면</div>
<div class='t' style='left:52px;top:176px;font-size:150px;color:{YEL}'>ACE</div>
<div id='e1' class='t' data-fit='1170' style='left:46px;top:330px;font-size:200px;color:#fff'>5.10억 <span style='color:{RED}'>→</span> <span style='color:{YEL}'>8.92억</span></div>
<div class='lab' style='left:62px;top:520px;font-size:44px;color:{GREY}'>평균 달 기준</div>
<div class='lab' style='left:756px;top:520px;font-size:44px;color:{GREY}'>가장 적은 달 기준</div>
<div class='lab' style='left:400px;top:236px;font-size:52px;color:#fff'>월 100만원 받는 데 필요한 돈</div>
"""
VARIANTS['m1e'] = m1e + FINE


# ── 4차(06:2x) — m1e 제미나이 7·7 / Claude 7.0 / 레드팀 6 = 6.67. 레드팀: '필요한 돈' 줄이 8.92억을 꼭 필요한 돈처럼 보이게 하고,
#    회색 꼬리표가 168px에서 사라짐 → '필요한 돈' 줄 빼고(제목이 말함), 꼬리표를 숫자 바로 밑에 크게·색으로. 꼬리표 말은 대본 104행 '평균으로 잰'·4장 '가장 적게 나온 달'.
m1f = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='f0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:100px;color:#fff'>분배금이 매달 똑같지 않으면</div>
<div class='t' style='left:52px;top:170px;font-size:150px;color:{YEL}'>ACE</div>
<div id='f1' class='t' data-fit='1170' style='left:46px;top:320px;font-size:200px;color:#fff'>5.10억 <span style='color:{RED}'>→</span> <span style='color:{YEL}'>8.92억</span></div>
<div class='t' style='left:60px;top:500px;font-size:62px;color:#C9CED8'>평균으로 재면</div>
<div class='t' style='left:740px;top:500px;font-size:62px;color:{YEL}'>가장 적은 달로 재면</div>
"""
VARIANTS['m1f'] = m1f + FINE


# ── 5차(06:3x) — m1f 6.42(레드팀 5.5: 화살표가 '수익이 불었다'로 오독·큰 숫자 2개·'가장 적은 달'이 제목과 겹침).
#    → 큰 숫자 하나(8.92억), 화살표 없음, 비교는 '평균 기준의 1.75배'(대본 4장 자막 말) 꼬리표, 윗줄 = 대본 104행 '실제 통장에는 평균이 들어오지 않잖아요'.
#    상품 이름은 168px에서 읽히게 흰색 굵게.
m1g = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='g0' class='t' data-fit='1170' style='left:54px;top:40px;font-size:96px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='t' style='left:56px;top:166px;font-size:78px;color:#C9CED8'>ACE 미국배당다우존스</div>
<div id='g1' class='t' data-fit='760' style='left:44px;top:262px;font-size:270px;color:{YEL}'>8.92억</div>
<div class='t' style='left:62px;top:540px;font-size:64px;color:#fff'>필요한 돈, 평균 기준의 <span style='color:{RED}'>1.75배</span></div>
"""
FINE_G = f"<div class='fine' style='color:{GREY};top:640px;font-size:22px'>2026.10.2 기준 · 세금·건보료 뗀 뒤, 2천만원 넘는 추가 세금·건보료는 넣지 않은 최소값</div>"
VARIANTS['m1g'] = m1g + FINE_G


# ── 6차(06:3x) — 5차 공통 지적: '필요'를 숫자와 한 덩어리로(레드팀), 그림 장치 하나 = 12달 분배 막대 중 가장 적은 달만 빨강(Claude).
#    막대 값 = facts [K1] ACE 1주당 분배 12회(원)
_facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
ACE12 = [37, 21, 53, 39, 24, 46, 44, 27, 40, 50, 25, 35]
assert '25-10 37 · 25-11 21 · 25-12 53 · 26-01 39 · 26-02 24 · 26-03 46 · 26-04 44 · 26-05 27 · 26-06 40 · 26-07 50 · 26-08 25 · 26-09 35' in _facts and sum(ACE12) == 441
def month_bars(x0, ybase, hmax, w=38, gap=10):
    s = ''
    for i, v in enumerate(ACE12):
        h = hmax * v / max(ACE12); c = RED if v == min(ACE12) else '#4A5160'
        s += f"<div style='position:absolute;left:{x0 + i * (w + gap)}px;top:{ybase - h:.0f}px;width:{w}px;height:{h:.0f}px;background:{c}'></div>"
    i = ACE12.index(min(ACE12)); s += f"<div class='t' style='left:{x0 + i * (w + gap) - 14}px;top:{ybase - hmax * 21 / 53 - 62:.0f}px;font-size:52px;color:{RED}'>21원</div>"
    return s
m1h = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='h0' class='t' data-fit='1170' style='left:54px;top:36px;font-size:88px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='lab' style='left:58px;top:150px;font-size:36px;color:#C9CED8'>ACE 미국배당다우존스 · 1주당 분배 12달</div>
{month_bars(60, 410, 200)}
<div class='t' style='left:690px;top:214px;font-size:64px;color:#fff'>평균의</div>
<div class='t' style='left:686px;top:296px;font-size:110px;color:{RED}'>1.75배</div>
<div id='h1' class='t' data-fit='880' style='left:46px;top:430px;font-size:170px;color:{YEL}'>8.92억 필요</div>
"""
FINE_H = f"<div class='fine' style='color:{GREY};top:640px;font-size:22px'>세후 월 100만원 기준 · 2026.10.2 · 연 2천만원 넘는 몫의 추가 세금·건보료 미포함</div>"
VARIANTS['m1h'] = m1h + FINE_H


# ── 7차(06:4x) — m1h 제미나이 7.5·7 / Claude 7.0 / 레드팀 6 = 6.75. 레드팀 조건: 1.75배를 작게(큰 숫자 하나), 막대에 평균(441÷12=36.75원) 점선.
def month_bars_avg(x0, ybase, hmax, w=38, gap=10):
    s = month_bars(x0, ybase, hmax, w, gap)
    ya = ybase - hmax * (sum(ACE12) / 12) / max(ACE12); xe = x0 + 12 * (w + gap) - gap
    s += f"<div style='position:absolute;left:{x0 - 6}px;top:{ya - 2:.0f}px;width:{xe - x0 + 12}px;height:0;border-top:5px dashed #fff'></div>"
    s += f"<div class='t' style='left:{xe + 16}px;top:{ya - 30:.0f}px;font-size:52px;color:#fff'>평균</div>"
    return s
m1i = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='i0' class='t' data-fit='1170' style='left:54px;top:36px;font-size:88px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='lab' style='left:58px;top:150px;font-size:36px;color:#C9CED8'>ACE 미국배당다우존스 · 1주당 분배 12달</div>
{month_bars_avg(60, 410, 200, w=62, gap=14)}
<div id='i1' class='t' data-fit='880' style='left:46px;top:430px;font-size:170px;color:{YEL}'>8.92억 필요</div>
<div class='lab' style='left:62px;top:604px;font-size:30px;color:#fff'>월 100만원 받으려면 · 평균으로 잴 때의 1.75배</div>
"""
FINE_I = f"<div class='fine' style='color:{GREY};top:650px;font-size:20px'>세후 기준 · 2026.10.2 · 연 2천만원 넘는 몫의 추가 세금·건보료 미포함</div>"
VARIANTS['m1i'] = m1i + FINE_I


# ── 8차(06:4x) — m1i 제미나이 7·7.5 / Claude 7.0 / 레드팀 6.5 = 6.92. 레드팀 고칠 것: 아랫줄 '월 100만원 받으려면'(제목 반복) 빼기,
#    큰 숫자에 ACE 붙이기(168px에서 'JEPQ도 8.92억' 오해 막기), 각주를 제목 말(세금·건보료 뗀 뒤)과 맞추기.
m1j = f"""<div style='position:absolute;inset:0;background:{BG}'></div>
<div id='j0' class='t' data-fit='1170' style='left:54px;top:36px;font-size:88px;color:#fff'>통장엔 평균이 안 들어온다</div>
<div class='lab' style='left:58px;top:150px;font-size:36px;color:#C9CED8'>ACE 미국배당다우존스 · 1주당 분배 12달</div>
{month_bars_avg(60, 410, 200, w=62, gap=14)}
<div id='j1' class='t' data-fit='900' style='left:46px;top:430px;font-size:170px;color:{YEL}'><span style='color:#fff'>ACE</span> 8.92억 필요</div>
<div class='lab' style='left:62px;top:556px;font-size:44px;color:#fff'>평균으로 잴 때의 1.75배</div>
"""
FINE_J = f"<div class='fine' style='color:{GREY};top:652px;font-size:20px'>세금·건보료 뗀 뒤 · 2026.10.2 · 연 2천만원 넘는 몫의 추가분은 빼고 잰 최소값</div>"
VARIANTS['m1j'] = m1j + FINE_J


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
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
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))

