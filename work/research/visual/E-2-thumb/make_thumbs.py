# E-2 테슬라 썸네일 시안 3개(캐릭터·로고·사진 없음, 2026-10-02 17시 visual) — py -3.12 make_thumbs.py
# 숫자 출처: ep/E-2/facts.txt [2](영업이익 398·영업이익률 1.4%) [3](이자수익 422) [10](10분기 매출·영업이익률) — 백만 달러
# 후킹: 반전 하나(대본 오프닝·review.md '영업이익 < 이자수익'). 카피 1위 제목은 18:40 copywriter → 썸네일은 제목을 되풀이하지 않는 짝.
# 경쟁과 다른 점(compare.png): 경쟁 5편 전부 실사 차·로봇 사진 + 아래 노랑·빨강 테두리 두 줄 → 우리는 사진 0, 장부 숫자 그래프, 테두리 글씨 없음.
# 실험: X-THUMB-1 A(캐릭터 없음) · e2a·e2b = X-THUMB-2 B(한 줄 큰 숫자/문장), e2c = A(두 줄 대비, 48시간 교체용)
# 가려짐 규칙: 오른쪽 아래 x≥960·y≥576(길이 표시)과 아래 5%(y≥684)에 글자 없음 — 렌더 뒤 좌표 자동 검사.
import os, re, json, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EP = os.path.join(ROOT, 'work', 'research', 'longform', 'ep', 'E-2')
FONTS = os.path.join(ROOT, 'work', 'video', 'public', 'fonts').replace('\\', '/')

facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
OP = int(re.search(r'\[2\] 2026년 2분기 영업이익 ([\d,]+)', facts).group(1).replace(',', ''))
INT = int(re.search(r'이자수익 ([\d,]+) > 영업이익', facts).group(1).replace(',', ''))
Q = re.findall(r'(\d{4})-(\d\d)-\d\d\*? +([\d,]+) / ([\d,]+) / ([\d.]+)%', facts)
assert (OP, INT, len(Q)) == (398, 422, 10), (OP, INT, len(Q))
REV = [int(q[2].replace(',', '')) for q in Q]; MG = [float(q[4]) for q in Q]
assert REV[-1] == max(REV) == 28236 and MG[-1] == min(MG) == 1.4
QL = [f"'{q[0][2:]} {int(q[1]) // 3}Q" for q in Q]
E = lambda v: f'{v / 100:.2f}억 달러'          # 398 → 3.98억 달러
YOY = re.search(r'2026년 2분기 매출 [\d,]+ \(1년 전 [\d,]+, \+([\d.]+)%', facts).group(1); assert YOY == '25.5'
REVs = f'{round(REV[-1] / 100)}억 달러'          # 282억 달러
RED, BLUE, INK = '#E5322D', '#2D6BE5', '#16181D'

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
@font-face{font-family:PD;src:url('file:///%(f)s/pd500.ttf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1280px;height:720px;overflow:hidden;position:relative;font-family:PD}
.t{position:absolute;font-family:BH;white-space:nowrap;line-height:1}
.lab{position:absolute;font:700 30px PD;white-space:nowrap}
.fine{position:absolute;left:52px;top:636px;font:500 24px PD;white-space:nowrap}
</style></head><body>%(body)s
<script>
function fit(id,maxW){const e=document.getElementById(id);let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e.id,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
FINE = "<div class='fine' style='color:%s'>2026년 2분기 · SEC 10-Q 손익계산서 원문 · 테슬라</div>"

# e2a — B(한 줄 문장) 밝은 장부지: 왼쪽 반전 문장, 오른쪽 0부터 막대 두 개(비율 그대로)
BH_, BY = 400, 560
ho, hi = round(BH_ * OP / INT), BH_
e2a = f"""<div style='position:absolute;inset:0;background:#F5F2EA'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:14px;background:{INK}'></div>
<div class='t' style='left:54px;top:44px;font-size:76px;color:{INK}'>테슬라 <span style='font:700 38px PD;color:#5A6170'>2분기 장부</span></div>
<div style='position:absolute;left:56px;top:130px;width:120px;height:8px;background:{RED}'></div>
<div id='a0' class='t' data-fit='760' style='left:50px;top:172px;font-size:140px;color:{INK}'>본업보다</div>
<div id='a1' class='t' data-fit='760' style='left:50px;top:332px;font-size:140px;color:{RED}'>이자가 더</div>
<div id='a2' class='t' data-fit='760' style='left:54px;top:492px;font-size:90px;color:{INK}'>벌었다</div>
<div style='position:absolute;left:860px;top:{BY}px;width:380px;height:4px;background:{INK}'></div>
<div style='position:absolute;left:880px;top:{BY - ho}px;width:150px;height:{ho}px;background:#9AA0AA'></div>
<div style='position:absolute;left:1070px;top:{BY - hi}px;width:150px;height:{hi}px;background:{RED}'></div>
<div class='lab' style='left:880px;top:{BY - ho - 44}px;font-size:30px;color:{INK}'>{E(OP)}</div>
<div class='lab' style='left:1070px;top:{BY - hi - 44}px;font-size:30px;color:{RED}'>{E(INT)}</div>
<div class='lab' style='left:916px;top:{BY - 64}px;font-size:40px;color:#fff'>본업</div>
<div class='lab' style='left:1106px;top:{BY - 64}px;font-size:40px;color:#fff'>이자</div>
"""

# e2b — B(한 줄 큰 숫자) 어두운 바탕: '매출 최대인데' + 1.4% + 10분기 영업이익률 막대(마지막만 빨강)
bx, bw, gap, top, H = 700, 40, 14, 130, 390
hgt = lambda m: round(H * m / max(MG))
bars = ''.join(f"<div style='position:absolute;left:{bx + i * (bw + gap)}px;top:{top + H - hgt(m)}px;width:{bw}px;height:{hgt(m)}px;background:{RED if i == 9 else '#4A5160'}'></div>" for i, m in enumerate(MG))
e2b = f"""<div style='position:absolute;inset:0;background:#101217'></div>
<div class='t' style='left:54px;top:52px;font-size:76px;color:#fff'>테슬라 <span style='font:700 40px PD;color:#C9CED8'>매출은 10분기 최대인데</span></div>
<div class='lab' style='left:58px;top:180px;font-size:46px;color:#C9CED8'>영업이익률</div>
<div id='b1' class='t' data-fit='620' style='left:44px;top:250px;font-size:300px;color:{RED}'>1.4%</div>
{bars}
<div style='position:absolute;left:{bx - 6}px;top:{top + H}px;width:{10 * (bw + gap)}px;height:3px;background:#8A93A3'></div>
<div class='lab' style='left:{bx}px;top:{top + H + 12}px;font-size:24px;color:#8A93A3'>{QL[0]}</div>
<div class='lab' style='left:{bx + 9 * (bw + gap) - 40}px;top:{top + H + 12}px;font-size:24px;color:{RED}'>{QL[-1]}</div>
<div class='lab' style='left:{bx + 2 * (bw + gap) - 20}px;top:{top + H - hgt(MG[2]) - 40}px;font-size:28px;color:#C9CED8'>{MG[2]:g}%</div>
"""

# e2c — A(두 줄 대비) 흰 영수증: 매출 ↑ 10분기 최대 / 이익률 ↓ 10분기 최저
e2c = f"""<div style='position:absolute;inset:0;background:#E9ECF1'></div>
<div style='position:absolute;left:48px;top:36px;width:1184px;height:570px;background:#fff;border-radius:18px;box-shadow:0 6px 0 #C9CED8'></div>
<div class='t' style='left:94px;top:56px;font-size:70px;color:{INK}'>테슬라 <span style='font:700 36px PD;color:#5A6170'>10분기 장부</span></div>
<div style='position:absolute;left:96px;top:146px;width:1088px;height:3px;background:repeating-linear-gradient(90deg,{INK} 0 14px,transparent 14px 24px)'></div>
<div class='lab' style='left:96px;top:208px;font-size:52px;color:#5A6170'>매출</div>
<div id='c0' class='t' data-fit='640' style='left:300px;top:168px;font-size:140px;color:{INK}'>최대 <span style='font-family:Malgun Gothic;font-size:96px;color:{RED}'>▲</span></div>
<div class='lab' style='left:304px;top:318px;font-size:30px;color:#5A6170'>{REVs} · 10분기 중 1위</div>
<div class='lab' style='left:96px;top:412px;font-size:52px;color:#5A6170'>이익률</div>
<div id='c1' class='t' data-fit='640' style='left:300px;top:372px;font-size:140px;color:{BLUE}'>1.4% <span style='font-family:Malgun Gothic;font-size:96px'>▼</span></div>
<div class='lab' style='left:304px;top:522px;font-size:30px;color:#5A6170'>10분기 중 꼴찌</div>
"""

# e2d — e2a 1차 심사 반영(제미나이 3-flash·Claude 심사관·레드팀): '이자로 더 벌었다'(문법), 막대 이름 영업이익/이자수익(정의),
#        세 줄 같은 크기, 테슬라 더 크게, 빨강 진하게
R2 = '#D11F1A'
e2d = f"""<div style='position:absolute;inset:0;background:#F5F2EA'></div>
<div style='position:absolute;left:0;top:0;width:1280px;height:14px;background:{INK}'></div>
<div class='t' style='left:54px;top:40px;font-size:92px;color:{INK}'>테슬라 <span style='font:700 38px PD;color:#5A6170'>2026년 2분기</span></div>
<div id='d0' class='t' data-fit='780' style='left:50px;top:172px;font-size:136px;color:{INK}'>본업보다</div>
<div id='d1' class='t' data-fit='780' style='left:50px;top:320px;font-size:136px;color:{R2}'>이자로 더</div>
<div id='d2' class='t' data-fit='780' style='left:50px;top:468px;font-size:136px;color:{INK}'>벌었다</div>
<div style='position:absolute;left:860px;top:{BY}px;width:380px;height:4px;background:{INK}'></div>
<div style='position:absolute;left:880px;top:{BY - ho}px;width:150px;height:{ho}px;background:#9AA0AA'></div>
<div style='position:absolute;left:1070px;top:{BY - hi}px;width:150px;height:{hi}px;background:{R2}'></div>
<div class='lab' style='left:876px;top:{BY - ho - 46}px;font-size:32px;color:{INK}'>{E(OP)}</div>
<div class='lab' style='left:1066px;top:{BY - hi - 46}px;font-size:32px;color:{R2}'>{E(INT)}</div>
<div class='lab' style='left:891px;top:{BY - 60}px;font-size:32px;color:#fff'>영업이익</div>
<div class='lab' style='left:1081px;top:{BY - 60}px;font-size:32px;color:#fff'>이자수익</div>
"""

# e2e — e2b 1차 심사 반영: 반전 '매출 최대인데'를 큰 글자로, 축 글씨 뺌, 막대는 흐름만, 1.4% 뒤 '남았다'
e2e = f"""<div style='position:absolute;inset:0;background:#101217'></div>
<div class='t' style='left:54px;top:44px;font-size:80px;color:#fff'>테슬라 매출 <span style='color:#7FB2FF'>늘었는데</span></div>
<div class='lab' style='left:58px;top:150px;font-size:34px;color:#8A93A3'>1년 전보다 +{YOY}% · 남은 영업이익률은</div>
<div id='e1' class='t' data-fit='620' style='left:44px;top:236px;font-size:300px;color:{RED}'>1.4%</div>
{bars}
<div style='position:absolute;left:{bx - 6}px;top:{top + H}px;width:{10 * (bw + gap)}px;height:3px;background:#8A93A3'></div>
"""
VARIANTS2 = {'e2d': e2d + FINE % '#6B7280', 'e2e': e2e + FINE % '#8A93A3'}

# e2f — e2e 2차 심사 반영(세 명 공통: 1.4%가 무엇인지 168px에서 안 읽힘): '영업이익률'을 큰 글자로 1.4% 바로 위에,
#        '늘었는데' 흰색(색 줄이기), 빨강 막대에 '10분기 최저'([10]), 잔글씨 줄 삭제
e2f = f"""<div style='position:absolute;inset:0;background:#101217'></div>
<div class='t' style='left:54px;top:44px;font-size:84px;color:#fff'>테슬라 매출 늘었는데</div>
<div id='f0' class='t' style='left:56px;top:178px;font-size:88px;color:#C9CED8'>영업이익률</div>
<div id='f1' class='t' data-fit='620' style='left:44px;top:282px;font-size:290px;color:{RED}'>1.4%</div>
{bars}
<div style='position:absolute;left:{bx - 6}px;top:{top + H}px;width:{10 * (bw + gap)}px;height:3px;background:#8A93A3'></div>
<div class='lab' style='left:{bx + 9 * (bw + gap) - 112}px;top:{top + H - hgt(MG[-1]) - 48}px;font-size:32px;color:{RED}'>10분기 최저</div>
"""
VARIANTS2['e2f'] = e2f + FINE % '#8A93A3'

VARIANTS = {'e2a': e2a + FINE % '#6B7280', 'e2b': e2b + FINE % '#8A93A3', 'e2c': e2c + FINE % '#6B7280'}
VARIANTS.update(VARIANTS2)

def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")

def main():
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k, body in VARIANTS.items():
            html = os.path.join(HERE, f'{k}.html')
            open(html, 'w', encoding='utf-8').write(BASE % {'f': FONTS, 'body': body})
            pg.goto('file:///' + html.replace('\\', '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
            report[k] = check_zones(pg)
            im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            print(k, os.path.getsize(out) // 1024, 'KB', '가려짐 위반:', report[k] or '없음')
        b.close()
    json.dump(report, open(os.path.join(HERE, 'zones.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
