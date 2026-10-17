# H-2 썸네일 12차(2026-10-17 visual-designer) — copywriter 10/16 18:58 새 문구로 처음 그리는 판.
# 문구: meta.json thumb_text_top '잠실주공5단지, 잠실동 안에서' / thumb_text '살 땐 가장 비싸고 / 전세는 가장 쌌다' / thumb_text_small '국민평형 84㎡대 · 최근 1년 거래' (assert).
# 숫자: calc_out.txt §1 잠실동 — 파일에서 읽어 assert(5단지 매매 중앙 43.45억 최고·순수전세 5.20억 최저). 그림에 값 글자 없음(막대만).
# 11차까지 지적: Claude '보고서 슬라이드'(덩어리 4개) · 레드팀 '좌우 카드 틀 쓰지 말 것'(10/17) · 경쟁 '억 vs 억' 겹침.
#   → 값 글자를 빼고 막대를 큰 두 줄에 붙여 덩어리를 3개로(앞줄 · 큰 두 줄+막대 · 작은 줄). 좌우 두 칸 대신 위(살 때)·아래(전세) 한 그림.
# h2u: 큰 두 줄 끝에 그 줄의 막대 4개를 바로 붙임(줄마다 0부터 자기 눈금) — 글과 그림이 한 줄.
# 앞줄은 PD 700(BH '5'가 's'로 보이던 문제). 가려짐: 오른쪽 아래 x>960·y>576, 아래 5%(y>684) 글자 없음 — zones.json 자동 검사.
import os, json, sys, re
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'H-2')
meta = json.load(open(os.path.join(EP, 'meta.json'), encoding='utf-8'))
TOP, BIG, SMALL = meta['thumb_text_top'], meta['thumb_text'], meta['thumb_text_small']
assert (TOP, BIG, SMALL) == ('잠실주공5단지, 잠실동 안에서', '살 땐 가장 비싸고 / 전세는 가장 쌌다', '국민평형 84㎡대 · 최근 1년 거래'), (TOP, BIG, SMALL)
B1, B2 = [s.strip() for s in BIG.split('/')]
T1, T2 = [s.strip() for s in TOP.split(',')]

cal = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
jam = cal.split('### 잠실동')[1].split('###')[0]
rows = {}
for m in re.finditer(r'- (\S+)\(건축 (\d+)\) (\d+)건 중앙 ([\d.]+)억 .*?순수전세 (\d+)건 ([\d.]+)억', jam):
    rows[m.group(1)] = (float(m.group(4)), float(m.group(6)))
assert rows['주공아파트5단지'] == (43.45, 5.20), rows['주공아파트5단지']
assert max(rows, key=lambda k: rows[k][0]) == '주공아파트5단지' and min(rows, key=lambda k: rows[k][1]) == '주공아파트5단지'
PICK = ['주공아파트5단지', '리센츠', '잠실엘스', '트리지움']  # 11차와 같은 견줌(거래 많은 새 단지 셋)
SALE = [rows[k][0] for k in PICK]; JS = [rows[k][1] for k in PICK]
print('매매', SALE, '전세', JS)

INK, OR, PAPER, GREY, BASE, MUTE = '#16181D', '#FF5A00', '#ECE6DA', '#B3B8C1', '#8A8F99', '#6E737D'
BASEHTML = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASEHTML.split('<body>')[0] + '<body>', '<script>' + BASEHTML.split('<script>')[1]
VARIANTS = {}


def bar(x, y, w, h, c, up=True):
    r = '6px 6px 0 0' if up else '0 0 6px 6px'
    return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};border-radius:{r}'></div>"


def top_line(fs, y):
    return f"<div class='lab' style='left:44px;top:{y}px;font-size:{fs}px;color:{INK};letter-spacing:-1px'><span style='color:{OR}'>{T1}</span>, {T2}</div>"


# h2u — 줄 끝 막대(덩어리 3개): 막대 4개 같은 굵기
# h2v — h2u 짜임에서 그림을 키움: 5단지 막대만 굵게(72px), 새 단지 셋은 가늘고 옅게(40px) — '하나만 튐'
# h2w — h2u에 막대 아래 작은 이름 '5단지'(주황)만 — 회색 셋은 이름 없이 옅게
# (첫 렌더의 위·아래 거울 막대 판은 168px에서 막대가 한 줄로 이어져 촛대 그래프로 읽혀 버림 — 심사에 안 넣음)
def board_row(fs=140, x0=1020, bws=(44, 44), gap=12, hm=134, grey=GREY, name=False, fit=950):
    s = ''
    rows_ = ((150, SALE), (352, JS))
    for line_top, vals in rows_:
        yb = line_top + 140; top = max(vals); x = x0
        for i, v in enumerate(vals):
            bw = bws[0] if i == 0 else bws[1]
            h = round(hm * v / top)
            s += bar(x, yb - h, bw, h, OR if i == 0 else grey)
            if name and i == 0:
                s += f"<div class='lab' style='left:{x - 20}px;width:{bw + 40}px;text-align:center;top:{yb + 6}px;font-size:30px;color:{OR}'>5단지</div>"
            x += bw + gap + (10 if i == 0 else 0)
        s += f"<div style='position:absolute;left:{x0 - 8}px;top:{yb}px;width:{x - gap - x0 + 16}px;height:4px;background:{BASE}'></div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
{top_line(92, 28)}
<div id='b1' class='t' data-fit='{fit}' style='left:42px;top:150px;font-size:{fs}px;color:{INK}'>{B1}</div>
<div id='b2' class='t' data-fit='{fit}' style='left:42px;top:352px;font-size:{fs}px;color:{INK}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{s}
<div class='lab' style='left:46px;top:560px;font-size:50px;color:{MUTE}'>{SMALL}</div>
"""


VARIANTS['h2u'] = board_row()
VARIANTS['h2v'] = board_row(fs=130, x0=960, bws=(76, 44), gap=12, hm=150, grey='#C4C8CF', fit=890)
VARIANTS['h2w'] = board_row(grey='#C4C8CF', name=True)


# ── 13차(10/17) — 12차 h2v 6.50(제미나이 7·6 · Claude 6.5 · 레드팀 6.5 겹침 1), h2u 6.25, h2w 6.17. Claude·레드팀 같은 처방: h2v 짜임 그대로 막대 끝에 값 하나씩('43억'·'5억').
#   값은 따로 칸을 만들지 않고 주황 막대 바로 위에 붙임(줄 → 막대 → 값이 한 덩어리). 위·아래 줄이라 왼→오 '폭락' 연결 없음.
# h2x: 값 먹색 BH 66px. h2y: 값 주황 BH 78px, 막대 묶음 넓게(5단지 막대 92px).
def board_val(vfs=66, vcol=INK, obw=80, gbw=44, x0=950, hm=104, fs=130, fit=880):
    s = ''
    for line_top, vals, v in ((176, SALE, f"{round(SALE[0])}억"), (390, JS, f"{round(JS[0])}억")):
        yb = line_top + 140; top = max(vals); x = x0
        for i, val in enumerate(vals):
            bw = obw if i == 0 else gbw
            h = round(hm * val / top)
            s += bar(x, yb - h, bw, h, OR if i == 0 else '#C4C8CF')
            if i == 0:
                s += f"<div class='t' style='left:{x - 60}px;width:{bw + 120}px;text-align:center;top:{yb - h - vfs - 6}px;font-size:{vfs}px;color:{vcol}'>{v}</div>"
            x += bw + 12 + (12 if i == 0 else 0)
        s += f"<div style='position:absolute;left:{x0 - 8}px;top:{yb}px;width:{x - 12 - x0 + 16}px;height:4px;background:{BASE}'></div>"
    return f"""<div style='position:absolute;inset:0;background:{PAPER}'></div>
{top_line(88, 22)}
<div id='b1' class='t' data-fit='{fit}' style='left:42px;top:176px;font-size:{fs}px;color:{INK}'>{B1}</div>
<div id='b2' class='t' data-fit='{fit}' style='left:42px;top:390px;font-size:{fs}px;color:{INK}'>{B2.replace('가장 쌌다', f"<span style='color:{OR}'>가장 쌌다</span>")}</div>
{s}
<div class='lab' style='left:46px;top:590px;font-size:48px;color:{MUTE}'>{SMALL}</div>
"""


VARIANTS['h2x'] = board_val()
VARIANTS['h2y'] = board_val(vfs=78, vcol=OR, obw=92, gbw=40, x0=944, hm=96)


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'&&c.tagName!=='BR'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});
      return bad}""")


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
            sizes = pg.evaluate("()=>[...document.querySelectorAll('[data-fit]')].map(e=>e.id+':'+getComputedStyle(e).fontSize+':'+Math.round(e.getBoundingClientRect().right))")
            im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', sizes, '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(zp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(sys.argv[1].split(',') if len(sys.argv) > 1 else list(VARIANTS))
