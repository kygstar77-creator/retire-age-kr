# 카페 대표사진(첫 사진) 1080x1080 정사각형 표지 — visual 2026-10-02 15:2x
#   py -3.12 work/research/visual/cafe-covers-1002/make_covers.py [offimkt1002 gongjae1002 nps1002]
# 왜: 사장님 10/2 15:3x "네이버 대표사진 이렇게 긴 거 넣으면 잘리는 거 알아 몰라" — 900x402 첫 사진은 목록 정사각형 썸네일에서 숫자가 잘린다.
#     naverpost.py 관문: 첫 사진 가로/세로 0.9~1.1·짧은 변 800px 이상.
# 틀: b10-cafe/make_b10.py(B10 00.png) 그대로 — 도장 라벨 → 굵은 제목 2줄 → 큰 숫자 1개(파랑) → 비교 한 줄 → 출처.
# 숫자: 각 묶음 title.txt·c??.txt·facts.txt에 있는 것만. 아래 CHECK가 본문에 그 글자가 있는지 확인한다(없으면 멈춤).
# 기존 00.png는 00_orig.png로 보존. order.txt는 첫 img 줄이 img/00.png(새 표지). 원래 00이 큰 숫자 카드(새 표지와 같은 숫자)면
# 본문에서 빼도 사진 수는 그대로(교체)라 넣지 않고, 정보가 다른 그림이면(gongjae 대상·한도·기간) 00_orig.png를 두 번째 자리에 넣는다.
import os, sys, shutil, glob
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
sys.path.insert(0, os.path.join(R, 'visual', 'E-1-thumb')); import make_thumbs as M

# 2차(15:3x): 심사 3명 공통 지적 "110px에선 큰 숫자와 검은 제목만 읽힌다, 숫자의 뜻을 붙이는 줄이 안 읽힌다" →
#   층을 줄이고(제목 1줄 + 숫자 + 숫자에 붙는 뜻 줄) 뜻 줄을 90px 안팎으로 키운다. 자잘한 비교는 출처 줄로 내린다.
# rows: (글자, 크기px, 색, 종류) — 종류 'num'은 남는 세로 칸을 다 쓰는 큰 숫자. 위에서 아래로 쌓는다(도장 아래 200~960).
B, K, G = '#1D4ED8', '#111827', '#374151'
COV = {
    'offimkt1002': dict(
        stamp='2026년 9월 실거래',
        rows=[('송파 파크하비오 투룸', 104, K, 't'), ('전세가 매매가의', 112, B, 't'), ('84%', 470, B, 'num'),
              ('HUG 전세보증은 90% 이하만', 76, K, 't')],  # 3차: 84%가 높은지 판단할 기준선(본문 c03)
        src='국토부 실거래 9월 중간값 · 전세 3억 9,690 / 매매 4억 7,450만원 · 47~51㎡', keep_orig=False,
        check=['84%', '3억 9,690만원', '4억 7,450만원', '47~51㎡', '파크하비오', '전세가 매매가의', 'HUG 전세보증', '90% 이하여야 가입할 수']),
    'gongjae1002': dict(
        stamp='10월 1일 국토부 발표',
        rows=[('공공재개발 이주비 이자 지원', 84, K, 't'), ('대출금리', 118, B, 't'), ('3.8%', 470, B, 'num'),
              ('밑이면 덜 받아요', 118, K, 't')],
        src='국토교통부 10-01 발표 · 연 1.8% 넘는 부분 최대 2%p 지원 · 1주택자', keep_orig=True,
        check=['3.8%', '연 1.8%', '2%포인트', '밑이면 덜 받아요', '대출금리']),
    'nps1002': dict(
        stamp='한국경제 10월 1일 보도',
        rows=[('국민연금 미적립부채', 100, K, 't'), ('1,450|조', 330, B, 'num'),
              ('내 연금 계산식엔/기금 잔액이 없다', 90, K, 't')],  # 3차: 파랑은 숫자 하나만, 뜻 줄은 검정 두 줄로 숫자 밑에
        src='한국경제 2026-10-01 보도 · 국민연금법 기본연금액 계산식(법제처)', keep_orig=False,
        check=['1,450조', '내 연금 계산식엔 기금 잔액이 없다', '기본연금액']),
}

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;background:#F7F8FA;font-family:PD;position:relative;overflow:hidden}
.stamp{position:absolute;left:80px;top:72px;border:6px solid #1F2937;color:#1F2937;font:700 44px PD;padding:10px 26px;border-radius:14px;transform:rotate(-3deg);white-space:nowrap}
#col{position:absolute;left:80px;top:196px;bottom:118px;width:920px;display:flex;flex-direction:column;justify-content:space-between}
.k{font-family:BH;line-height:1.08;white-space:nowrap;align-self:flex-start}
.num{letter-spacing:-10px;line-height:0.9}
.unit{font-size:0.6em;letter-spacing:0;margin-left:12px}
.src{position:absolute;left:80px;bottom:52px;font:700 27px PD;color:#6B7280;white-space:nowrap}
</style></head><body>
<div class='stamp'>%(stamp)s</div>
<div id='col'>%(rows)s</div>
<div class='src fit'>%(src)s</div>
<script>
document.fonts.ready.then(()=>{
  for(const e of document.querySelectorAll('.fit')){let s=parseFloat(getComputedStyle(e).fontSize);
    while(e.getBoundingClientRect().right>1000&&s>20){s-=2;e.style.fontSize=s+'px';}}
  // 칸 넘치면(세로) 큰 숫자를 줄인다
  const col=document.getElementById('col'),n=document.querySelector('.num');
  let s=parseFloat(n.style.fontSize);while(col.scrollHeight>col.clientHeight+1&&s>120){s-=6;n.style.fontSize=s+'px';}
  document.body.dataset.ready=1});
</script></body></html>"""


def rows_html(rows):
    out = []
    for i, (t, size, col, kind) in enumerate(rows):
        t = t.replace('/', '<br>')
        if '|' in t: a, u = t.split('|'); t = f"{a}<span class='unit'>{u}</span>"
        out.append(f"<div class='k fit{' num' if kind == 'num' else ''}' id='r{i}' style='font-size:{size}px;color:{col}'>{t}</div>")
    return ''.join(out)


def body_text(pkg):
    return ''.join(open(f, encoding='utf-8').read() for f in [os.path.join(pkg, 'title.txt')] + sorted(glob.glob(os.path.join(pkg, 'c??.txt'))))


def make(name, pg):
    c = COV[name]; pkg = os.path.join(R, name, 'pkg'); img = os.path.join(pkg, 'img')
    txt = body_text(pkg) + open(os.path.join(pkg, 'facts.txt'), encoding='utf-8').read()
    miss = [w for w in c['check'] if w not in txt]
    assert not miss, f'{name} 본문·facts에 없는 글자: {miss}'
    orig = os.path.join(img, '00_orig.png')
    if not os.path.exists(orig): shutil.copy(os.path.join(img, '00.png'), orig)
    html = os.path.join(H, name + '.html')
    open(html, 'w', encoding='utf-8').write(HTML % dict(stamp=c['stamp'], src=c['src'], f=M.FONTS, rows=rows_html(c['rows'])))
    pg.goto(Path(html).as_uri()); pg.wait_for_selector('body[data-ready]')
    box = pg.evaluate("[...document.querySelectorAll('.k,.src,.stamp')].map(e=>{const r=e.getBoundingClientRect();return [e.id||e.className,Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom),getComputedStyle(e).fontSize]})")
    for b in box: assert b[3] <= 1040 and b[4] <= 1040, f'{name} 넘침 {b}'
    out = os.path.join(img, '00.png'); pg.screenshot(path=out)
    im = Image.open(out); assert im.size == (1080, 1080), im.size
    im.resize((168, 168), Image.LANCZOS).save(os.path.join(H, name + '_168.png'))
    # order.txt: 첫 img 줄 = img/00.png, 필요하면 바로 뒤에 img/00_orig.png
    op = os.path.join(pkg, 'order.txt'); lines = open(op, encoding='utf-8').read().split('\n')
    if c['keep_orig'] and 'img/00_orig.png' not in lines:
        i = next(i for i, l in enumerate(lines) if l.strip().startswith('img/'))
        assert lines[i].strip() == 'img/00.png', lines[i]
        lines.insert(i + 1, 'img/00_orig.png')
        open(op, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    first = next(l.strip() for l in open(op, encoding='utf-8') if l.strip().startswith('img/'))
    print(name, im.size, '첫 사진', first, box)


if __name__ == '__main__':
    names = sys.argv[1:] or list(COV)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
        for n in names: make(n, pg)
        b.close()
