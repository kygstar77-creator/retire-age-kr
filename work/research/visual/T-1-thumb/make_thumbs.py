# T-1 양도세 장특공제 정부안 썸네일 시안 (2026-10-17 visual-designer, 요청 today.md PD 10/16 10:36 · 기한 10/19 06:00)
# 틀: C-2-thumb/make_thumbs.py 복사(HTML→Playwright 1280x720, check_zones 가려짐 검사, 320·168 축소) — 그림·문구는 새로.
# 문구: ep/T-1/copy/titles.md 1위 '2년만 살았으면 / 양도세 공제 48%→16%로 줄어' · small '정부안 · 2029년 · 20억 집 팔 때'
#       2위(swap) '거주 10년 vs 2년 / 양도세 약 12배' · small '같은 20억 집 · 정부안 2029년'
# 숫자: calc_out.txt B 2027 공제율 48% · 2029 16% · 2029 지방세 포함 B 14,777만 / C 1,241만 = 11.9배(약 12배) (assert)
# 피한 것: 경쟁 5(세무사 얼굴 사진·아래 두 줄 노랑/흰/빨강 테두리 글·'폭탄'·'지옥') · 우리 직전 P-1·R-1(청록 판+좌우 흰/검 카드)·W-1(밝은 회색 판+남색 띠)
# 주제 사물: 집(영상 0장 그림과 같은 지붕 꺾쇠 집) · 계산기 화면(우리 정체성 '계산기') — 사람 얼굴 0
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, '..', '..', 'longform', 'ep', 'T-1')
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
B = calc.split('== B 20억')[1].split('==')[0]
C = calc.split('== C 20억')[1].split('==')[0]
assert '2027: 공제율 48%' in B and '2028: 공제율 32%' in B and '2029: 공제율 16%' in B
TB = int(re.search(r'2029:.*?지방세 포함 ([\d,]+)만원', B).group(1).replace(',', ''))
TC = int(re.search(r'2029:.*?지방세 포함 ([\d,]+)만원', C).group(1).replace(',', ''))
assert (TB, TC) == (14777, 1241) and round(TB / TC) == 12, (TB, TC)
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]
OR, INK, PAPER = '#FF5A00', '#16171B', '#F4F1EA'


def house(x, y, w, col, door='#FFFFFF', stroke=None):
    """영상 0장 집 그림 — 꺾쇠 지붕 + 네모 몸통 + 문"""
    s = w / 100
    st = stroke or col
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px' width='{w}' height='{w * 0.86:.0f}' viewBox='0 0 100 86'>"
            f"<polyline points='6,40 50,6 94,40' fill='none' stroke='{st}' stroke-width='10' stroke-linecap='round' stroke-linejoin='round'/>"
            f"<rect x='17' y='38' width='66' height='46' rx='3' fill='{col}'/>"
            f"<rect x='44' y='56' width='12' height='28' fill='{door}'/></svg>")


def arrow(x, y, w, h, col):
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px' width='{w}' height='{h}' viewBox='0 0 100 60'>"
            f"<path d='M4 30 H70' stroke='{col}' stroke-width='14' stroke-linecap='round'/><path d='M58 8 L94 30 L58 52' fill='none' stroke='{col}' stroke-width='14' stroke-linecap='round' stroke-linejoin='round'/></svg>")


V = {}
# t1a — 주황 판(경쟁 5·우리 최근 3편에 없는 바탕) · 1위 문구 · 오른쪽 위 흰 집에 '2년' 문패 · 48%를 회색 빗금으로 지우고 16% 크게
#   숫자 하나 크게 = '16%'. '48%'는 지운 값(작게·회색) — 168px에서 '줄어든 것 = 공제'가 보이게 '공제' 낱말을 숫자 바로 앞 줄에.
V['t1a'] = (f"<div style='position:absolute;inset:0;background:{OR}'></div>"
            f"<div class='t' style='left:52px;top:34px;font-size:124px;color:{INK}'>2년만 살았으면</div>"
            f"<div class='t' style='left:56px;top:196px;font-size:92px;color:#FFFFFF'>양도세 공제</div>"
            f"<div class='t' style='left:52px;top:326px;font-size:140px;color:{INK};opacity:.55'><span style='position:relative'>48%"
            f"<span style='position:absolute;left:-6px;right:-6px;top:52%;height:16px;background:{INK};transform:rotate(-8deg)'></span></span></div>"
            + arrow(372, 350, 130, 80, INK)
            + f"<div class='t' style='left:520px;top:286px;font-size:210px;color:#FFFFFF'>16%</div>"
            f"<div class='t' style='left:56px;top:500px;font-size:84px;color:{INK}'>로 줄어</div>"
            + house(930, 40, 300, '#FFFFFF', door='#FFFFFF')
            + f"<div class='t' style='left:980px;top:170px;width:200px;text-align:center;font-size:84px;color:{OR}'>2년</div>"
            f"<div style='position:absolute;left:44px;top:606px;height:66px;width:820px;background:{INK};border-radius:12px'></div>"
            f"<div class='t' style='left:44px;top:614px;width:820px;text-align:center;font-size:50px;color:#FFFFFF'>정부안 · 2029년 · 20억 집 팔 때</div>")

# t1b — 2위 문구 · 종이 판 · 같은 집 두 채(검정 10년·주황 2년) 아래 세금 막대(높이 = 2029 실제 세금 비 1,241:14,777)
#   큰 숫자 하나 '12배'. 좌우 카드 대신 집 두 채가 막대 받침이 되는 한 장면(P-1·R-1 카드 짜임 피함).
H_MAX = 300
hc = max(round(H_MAX * TC / TB), 10)
V['t1b'] = (f"<div style='position:absolute;inset:0;background:{PAPER}'></div>"
            f"<div class='t' style='left:52px;top:34px;font-size:104px;color:{INK}'>거주 10년 <span style='color:#8A8F99;font-size:84px'>vs</span> <span style='color:{OR}'>2년</span></div>"
            f"<div class='t' style='left:52px;top:200px;font-size:110px;color:{INK}'>양도세</div>"
            f"<div class='t' style='left:52px;top:300px;font-size:240px;color:{OR}'><span style='font-size:120px;color:{INK}'>약 </span>12배</div>"
            # 오른쪽: 막대 두 개(아래에서 위로) + 밑에 집
            + f"<div style='position:absolute;left:840px;top:{90 + H_MAX - hc}px;width:150px;height:{hc}px;background:{INK};border-radius:10px 10px 0 0'></div>"
            f"<div style='position:absolute;left:1050px;top:90px;width:150px;height:{H_MAX}px;background:{OR};border-radius:10px 10px 0 0'></div>"
            f"<div style='position:absolute;left:820px;top:{90 + H_MAX}px;width:400px;height:6px;background:{INK}'></div>"
            + house(835, 400, 160, INK) + house(1045, 400, 160, OR)
            +             f"<div style='position:absolute;left:44px;top:606px;height:66px;width:820px;background:{INK};border-radius:12px'></div>"
            f"<div class='t' style='left:44px;top:614px;width:820px;text-align:center;font-size:50px;color:#FFFFFF'>같은 20억 집 · 정부안 2029년</div>")

# t1c — 1위 문구 · 먹색 판 + 계산기 화면(우리 정체성) 안에 '48% → 16%' · 왼쪽 위 주황 집('2년만 살았으면' 옆)
#   경쟁 어두운 판은 사진+아래 두 줄 테두리 글 — 여기는 사진 0·테두리 0·글이 위, 화면 칸 안 숫자.
V['t1c'] = (f"<div style='position:absolute;inset:0;background:#202227'></div>"
            + house(52, 34, 150, OR, door='#202227')
            + f"<div class='t' style='left:226px;top:44px;font-size:118px;color:#FFFFFF'>2년만 살았으면</div>"
            f"<div class='t' style='left:56px;top:206px;font-size:96px;color:{OR}'>양도세 공제</div>"
            # 계산기 화면 칸
            f"<div style='position:absolute;left:36px;top:322px;width:930px;height:240px;background:#C9D3B4;border-radius:22px;border:10px solid #3A3D45'></div>"
            f"<div class='t' style='left:80px;top:362px;font-size:170px;color:#5B6352'>48%</div>"
            + arrow(420, 400, 130, 80, '#1F2318')
            + f"<div class='t' style='left:575px;top:354px;font-size:180px;color:#1F2318'>16%</div>"
            f"<div class='t' style='left:986px;top:404px;font-size:96px;color:#FFFFFF'>로 줄어</div>"
            f"<div class='t' style='left:52px;top:604px;font-size:52px;color:#C9CED8'>정부안 · 2029년 · 20억 집 팔 때</div>")

# 2차(10/17) — 1차 블라인드: 레드팀이 t1a·t1c를 '양도세가 16%로 줄어'로 읽음(Claude '모름') → titles.md 규칙대로 2위 문구를 1위로. t1a·t1c 보류.
#   1차 t1b(제미나이 8·Claude 6·레드팀 8): ① 막대 주인(10년/2년)이 색으로만 이어짐 — 집 안에 '10년'·'2년'을 크게 ② 글이 화면 너비 60%(경쟁 90%) — 큰 줄 키움
#   ③ 'vs'·작은 줄 168px에서 흐림 — 진하게 56px ④ 아이보리는 W-1(연회색)과 가깝다(Claude) → 진한 판(t1e)을 같은 차수에
def house_lab(x, y, w, col, txt, tc='#FFFFFF', fs=None):
    fs = fs or round(w * 0.30)
    return (house(x, y, w, col, door=col)
            + f"<div class='t' style='left:{x}px;top:{y + w * 0.47:.0f}px;width:{w}px;text-align:center;font-size:{fs}px;color:{tc}'>{txt}</div>")


def vbars(bg, ink, sub_bg, sub_c, vs_c):
    base, hmax, bw = 392, 228, 160
    h10 = max(round(hmax * TC / TB), 14)
    return (f"<div style='position:absolute;inset:0;background:{bg}'></div>"
            f"<div class='t' style='left:44px;top:30px;font-size:118px;color:{ink}'>거주 10년 <span style='color:{vs_c}'>vs</span> <span style='color:{OR}'>2년</span></div>"
            f"<div class='t' style='left:44px;top:196px;font-size:126px;color:{ink}'>양도세</div>"
            f"<div class='t' style='left:40px;top:318px;font-size:250px;color:{OR}'><span style='font-size:126px;color:{ink}'>약 </span>12배</div>"
            + f"<div style='position:absolute;left:826px;top:{base - h10}px;width:{bw}px;height:{h10}px;background:{ink};border-radius:8px 8px 0 0'></div>"
            f"<div style='position:absolute;left:1046px;top:{base - hmax}px;width:{bw}px;height:{hmax}px;background:{OR};border-radius:8px 8px 0 0'></div>"
            + f"<div style='position:absolute;left:806px;top:{base}px;width:420px;height:6px;background:{ink}'></div>"
            + house_lab(821, base + 14, 170, ink, '10년', tc=bg) + house_lab(1041, base + 14, 170, OR, '2년')
            + f"<div style='position:absolute;left:36px;top:600px;height:74px;width:900px;background:{sub_bg};border-radius:12px'></div>"
            f"<div class='t' style='left:36px;top:610px;width:900px;text-align:center;font-size:56px;color:{sub_c}'>같은 20억 집 · 정부안 2029년</div>")


V['t1d'] = vbars(PAPER, INK, INK, '#FFFFFF', '#5B6270')
V['t1e'] = vbars('#1E2026', '#FFFFFF', '#FFFFFF', INK, '#9AA1AD')
# t1f — 가로 막대 판: 큰 줄 '양도세 약 12배'를 화면 너비 가득, 아래 두 줄 = [집 10년]짧은 막대 / [집 2년]긴 막대(길이 = 2029 세금 비)
def hbars(bg, ink, sub_bg, sub_c):
    x0, wmax = 230, 1000
    w10 = max(round(wmax * TC / TB), 18)
    return (f"<div style='position:absolute;inset:0;background:{bg}'></div>"
            f"<div class='t' style='left:44px;top:26px;font-size:96px;color:{ink}'>거주 10년 <span style='color:#5B6270'>vs</span> <span style='color:{OR}'>2년</span></div>"
            f"<div class='t' style='left:40px;top:134px;font-size:196px;color:{ink}'>양도세 <span style='color:{OR}'><span style='font-size:120px;color:{ink}'>약 </span>12배</span></div>"
            + house_lab(60, 362, 124, ink, '10년', tc=bg, fs=38) + house_lab(60, 484, 124, OR, '2년', fs=40)
            + f"<div style='position:absolute;left:{x0}px;top:384px;width:{w10}px;height:84px;background:{ink};border-radius:0 10px 10px 0'></div>"
            f"<div style='position:absolute;left:{x0}px;top:506px;width:{wmax}px;height:84px;background:{OR};border-radius:0 10px 10px 0'></div>"
            f"<div style='position:absolute;left:36px;top:620px;height:62px;width:860px;background:{sub_bg};border-radius:12px'></div>"
            f"<div class='t' style='left:36px;top:626px;width:860px;text-align:center;font-size:50px;color:{sub_c}'>같은 20억 집 · 정부안 2029년</div>")


V['t1f'] = hbars(PAPER, INK, INK, '#FFFFFF')

# 3차(10/17) — 2차 t1d 7.33(제미나이 8·Claude 7·레드팀 7) · t1f 6.33(5·7·7) · t1e 레드팀 반려(어두운 바탕+주황+배수 말투 = 경쟁 유사 3)
#   공통: ① 10년 막대가 선·네모 한 칸이라 안 보임 ② 집 이름표 168px에서 작음 ③ '12배'가 한 사람 이야기로 읽힐 위험(레드팀) — '10년 vs 2년' 줄을 키워 비교를 앞세움
#   Claude: 금액을 막대에 붙이면 '누가 더 내는지'가 글로 박힘 → t1g(금액 있음) vs t1i(금액 없음) 같은 차수 비교. 문구 '차이' 보탬은 카피 확정 문구가 아니라 안 함.
assert '1,241' in C and '14,777' in B
def hrow(y, col, txt, tc, frac, amt, amt_in, bar_h=74):
    x0, wmax = 214, 1010
    w = max(round(wmax * frac), 40)
    a = (f"<div class='t' style='left:{x0 + w + 18}px;top:{y + (bar_h - 54) // 2}px;font-size:54px;color:{col}'>{amt}</div>" if not amt_in else
         f"<div class='t' style='left:{x0 + 22}px;top:{y + (bar_h - 54) // 2}px;font-size:54px;color:#FFFFFF'>{amt}</div>")
    return (house_lab(46, y - 30, 136, col, txt, tc=tc, fs=46)
            + f"<div style='position:absolute;left:{x0}px;top:{y}px;width:{w}px;height:{bar_h}px;background:{col};border-radius:0 12px 12px 0'></div>"
            + (a if amt else ''))


def g3(amts):
    return (f"<div style='position:absolute;inset:0;background:{PAPER}'></div>"
            f"<div class='t' style='left:40px;top:22px;font-size:124px;color:{INK}'>거주 10년 <span style='color:#5B6270'>vs</span> <span style='color:{OR}'>2년</span></div>"
            f"<div class='t' style='left:40px;top:160px;font-size:168px;color:{INK}'>양도세 <span style='font-size:118px'>약</span> <span style='color:{OR}'>12배</span></div>"
            + hrow(388, INK, '10년', PAPER, TC / TB, '1,241만원' if amts else '', False)
            + hrow(508, OR, '2년', '#FFFFFF', 1.0, '1억 4,777만원' if amts else '', True)
            + f"<div style='position:absolute;left:36px;top:616px;height:64px;width:880px;background:{INK};border-radius:12px'></div>"
            f"<div class='t' style='left:36px;top:622px;width:880px;text-align:center;font-size:52px;color:#FFFFFF'>같은 20억 집 · 정부안 2029년</div>")


V['t1g'] = g3(True)
V['t1i'] = g3(False)

# 4차(10/17) — 3차 t1i 7.00(제미나이 6·Claude 7·레드팀 8) · t1g 7.00(8·6·7, 금액 168px 뭉개짐·숫자 7개) · t1d 6.67
#   Claude·레드팀: 집 안 '10년/2년'이 168px 6px라 안 읽히고 '집 나이'로 읽힐 위험 → 줄 머리를 글자 '10년 거주'·'2년 거주'(56px)로
#   레드팀: '12배'를 키우고 오른쪽 위 빈자리 채움 → 집 그림 하나를 오른쪽 위로(주제 사물 유지) · Claude: 바탕 대비 → t1k는 먹색 테두리
def g4(frame=False):
    x0, wmax, bh = 318, 912, 80
    w10 = round(wmax * TC / TB)
    fr = f"<div style='position:absolute;inset:0;border:14px solid {INK}'></div>" if frame else ''
    return (f"<div style='position:absolute;inset:0;background:{PAPER}'></div>{fr}"
            f"<div class='t' style='left:40px;top:28px;font-size:112px;color:{INK}'>거주 10년 <span style='color:#5B6270'>vs</span> <span style='color:{OR}'>2년</span></div>"
            + house(1096, 14, 140, OR, door=PAPER)
            + f"<div class='t' style='left:36px;top:150px;font-size:186px;color:{INK}'>양도세 <span style='font-size:124px'>약</span> <span style='color:{OR}'>12배</span></div>"
            f"<div class='t' style='left:40px;top:{378 + (bh - 58) // 2}px;font-size:58px;color:{INK}'>10년 거주</div>"
            f"<div style='position:absolute;left:{x0}px;top:378px;width:{w10}px;height:{bh}px;background:{INK};border-radius:0 12px 12px 0'></div>"
            f"<div class='t' style='left:40px;top:{486 + (bh - 58) // 2}px;font-size:58px;color:{OR}'>2년 거주</div>"
            f"<div style='position:absolute;left:{x0}px;top:486px;width:{wmax}px;height:{bh}px;background:{OR};border-radius:0 12px 12px 0'></div>"
            f"<div style='position:absolute;left:36px;top:604px;height:68px;width:900px;background:{INK};border-radius:12px'></div>"
            f"<div class='t' style='left:36px;top:611px;width:900px;text-align:center;font-size:54px;color:#FFFFFF'>같은 20억 집 · 정부안 2029년</div>")


V['t1j'] = g4()
V['t1k'] = g4(True)
for k in V:
    assert '폭탄' not in V[k] and '0%' not in V[k].replace('16%', '').replace('48%', '')


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")


if __name__ == '__main__':
    keys = sys.argv[1].split(',') if len(sys.argv) > 1 else list(V)
    import numpy as n
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k in keys:
            html = os.path.join(HERE, f'{k}.html'); open(html, 'w', encoding='utf-8').write(HEAD + V[k] + '\n' + TAIL)
            pg.goto('file:///' + html.replace(chr(92), '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out); im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            a = n.asarray(im.convert('L'), float)
            print(k, os.path.getsize(out) // 1024, 'KB 명암폭', round(a.std()), '가려짐:', check_zones(pg) or '없음')
        b.close()
