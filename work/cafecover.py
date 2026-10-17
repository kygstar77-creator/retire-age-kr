# 카페 대표 이미지(표지) 1080x1080 생성기 — visual-designer 2026-10-17
#   py -3.12 work/cafecover.py <pkg> --topic "전세대출 이자/은행마다 다르다" --num "한 달 8만원 차이" \
#        [--sub "2억 빌리면 · 8월 평균"] [--icon landmark|auto] [--label "금감원 9월 공시"] [--src "출처 한 줄"] [--bg auto|navy|light|yellow|blue] [--out 경로]
#   py -3.12 work/cafecover.py --icons 전세        # 주제어로 쓸 만한 아이콘 이름 보기
# 왜(벤치마크 10/16 research/growth/cafe-gap-1016.md):
#   ① 표지 20장 모두 남색 바탕 글자뿐 — 주제 사물 그림 0/20, 100px 판에서 서로 구별 안 됨
#   ② 가장 큰 글자가 숫자('54만 → 21.6만원') — 주제어 줄이 가장 커야 목록에서 무슨 글인지 보인다
#   ③ cover_review.md에 '100px 읽힘'·'최근 10장 옆 구별' 확인 0/26
# 그래서 이 생성기는 다음을 코드로 지킨다(어기면 멈춘다):
#   - 주제 사물 그림 1개(Lucide 아이콘, ISC 라이선스 — node_modules/lucide-react, 표지 오른쪽 아래 작은 글씨로 표시하지 않고 cover_meta.json에 적는다)
#   - 글자 크기: 주제어 줄 > 숫자 줄 > 보조 줄 (브라우저에서 실제 잰 px로 검사)
#   - 바탕색: 최근 발행 카페 표지 10장과 가장 덜 겹치는 색(--bg auto)
#   - 결과: <pkg>/img/00.png · <pkg>/cover_100.png(100px 축소본) · <pkg>/cover_board.png(최근 10장 옆 비교판) · <pkg>/cover_meta.json
#   그다음 사람(또는 심사 Agent)이 cover_100.png·cover_board.png를 Read로 보고 cover_review.md에 두 줄을 적는다:
#     100px 읽힘: <100px 판에서 읽힌 주제어 그대로>
#     최근 10장 옆 구별: <무엇으로 구별되는지 — 색·그림>
#   naverpost.py·editgate.py가 10/17 10:00 이후 만든 묶음은 두 줄과 cover_meta.json이 없으면 올리지 않는다.
import os, re, sys, json, glob, argparse, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
RES = os.path.join(HERE, 'research')
FONTS = os.path.join(HERE, 'video', 'public', 'fonts').replace('\\', '/')
ICONS = os.path.join(ROOT, 'node_modules', 'lucide-react', 'dist', 'esm', 'icons')
ICON_LICENSE = 'Lucide (lucide-react, ISC License)'

# 색 4벌 — 디자인 정체성 '색4'. (바탕, 주제어, 숫자, 보조·출처)
PAL = {
    'navy':   ('#0F1B3D', '#FFFFFF', '#FFD43B', '#A5B4D4'),
    'light':  ('#F7F8FA', '#111827', '#1D4ED8', '#4B5563'),
    'yellow': ('#FFD43B', '#0F1B3D', '#C2410C', '#3F3A1E'),
    'blue':   ('#1F4FD8', '#FFFFFF', '#FFD43B', '#DCE6FF'),
}
# 주제어 → 아이콘(사물). 맞는 게 없으면 --icon으로 직접 고른다(lucide.dev/icons 이름).
ICON_HINT = [
    (r'전세|월세|임대|세입|집주인', 'house'), (r'아파트|재건축|재개발|분양|청약|단지|평당', 'building-2'),
    (r'대출|은행|금리|이자', 'landmark'), (r'예금|적금|저축', 'piggy-bank'), (r'연금|국민연금|IRP|퇴직연금', 'piggy-bank'),
    (r'세금|양도세|취득세|종부세|상속세|증여세|공제|연말정산|부가세', 'receipt'),
    (r'보험|실손|건강보험|장기요양', 'shield-plus'), (r'병원|의료|치료|요양', 'hospital'),
    (r'주가|주식|코스피|ETF|배당|SCHD|QQQ|증시', 'trending-up'), (r'급락|폭락|하락', 'trending-down'),
    (r'금값|금 |골드', 'coins'), (r'퇴직|퇴직금|실업|구직|재취업|월급|연봉', 'briefcase'),
    (r'마감|신청|기한|날짜|달력', 'calendar-days'), (r'육아|출산|아이', 'baby'), (r'자동차|차량', 'car'),
    (r'농지|농업|귀농', 'tractor'), (r'상가|가게|자영업', 'store'), (r'선물|증여', 'gift'), (r'카드|소비|지출|생활비', 'wallet'),
]


def icon_svg(name, color, px):
    f = os.path.join(ICONS, name + '.mjs')
    if not os.path.exists(f):
        raise SystemExit(f'아이콘 "{name}" 없음 — py -3.12 work/cafecover.py --icons <주제어> 로 고르거나 lucide.dev/icons 이름을 쓴다')
    t = open(f, encoding='utf-8').read()
    body = t.split('__iconNode = [', 1)[1].split('];', 1)[0]
    els = []
    for tag, attrs in re.findall(r'\[\s*"(\w+)",\s*\{(.*?)\}\s*\]', body, re.S):
        a = ' '.join(f'{k}="{v}"' for k, v in re.findall(r'(\w+):\s*"([^"]*)"', attrs) if k != 'key')
        els.append(f'<{tag} {a}/>')
    assert els, f'아이콘 {name} 해석 실패'
    return (f'<svg id="ico" xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{"".join(els)}</svg>')


def guess_icon(text):
    for pat, name in ICON_HINT:
        if re.search(pat, text): return name
    return None


def recent_covers(n=10, exclude=None):
    """최근 발행한 카페 글의 첫 사진(표지) n장 — published.txt 시각 순."""
    rows = []
    for pub in glob.glob(os.path.join(RES, '*', 'pkg', 'published.txt')):
        pkg = os.path.dirname(pub)
        if exclude and os.path.abspath(pkg) == os.path.abspath(exclude): continue
        if 'cafe.naver.com' not in open(pub, encoding='utf-8', errors='ignore').read(): continue
        op = os.path.join(pkg, 'order.txt')
        if not os.path.exists(op): continue
        first = next((l.strip() for l in open(op, encoding='utf-8') if l.strip().startswith('img/')), None)
        if first and os.path.exists(os.path.join(pkg, first)):
            rows.append((os.path.getmtime(pub), os.path.basename(os.path.dirname(pkg)), os.path.join(pkg, first)))
    rows.sort(reverse=True)
    return rows[:n]


def _hex(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def pick_bg(recent):
    """최근 표지들의 테두리 색(바탕)과 가장 멀리 떨어진 색 한 벌."""
    from PIL import Image
    seen = []
    for _, _, p in recent:
        im = Image.open(p).convert('RGB').resize((50, 50))
        px = [im.getpixel((x, y)) for x in range(50) for y in (0, 49)] + [im.getpixel((x, y)) for y in range(50) for x in (0, 49)]
        seen.append(tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3)))
    if not seen: return 'light'
    def score(k):
        b = _hex(PAL[k][0])
        return sum(1 for s in seen if sum((a - c) ** 2 for a, c in zip(b, s)) ** 0.5 > 90)
    return max(PAL, key=lambda k: (score(k), -list(PAL).index(k)))


HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;background:%(bg)s;font-family:PD;position:relative;overflow:hidden}
#ico{position:absolute;right:64px;bottom:120px}
.label{position:absolute;left:80px;top:76px;font:700 40px PD;color:%(mut)s;white-space:nowrap}
#col{position:absolute;left:80px;top:150px;width:920px;display:flex;flex-direction:column;gap:34px}
.k{font-family:BH;line-height:1.06;white-space:nowrap}
#topic{color:%(ink)s} #num{color:%(acc)s} #sub{color:%(ink)s;font-family:PD;font-weight:700;line-height:1.2}
.src{position:absolute;left:80px;bottom:52px;font:700 26px PD;color:%(mut)s;white-space:nowrap;max-width:920px}
</style></head><body>
<div class='label'>%(label)s</div>
<div id='col'>
<div class='k' id='topic' style='font-size:168px'>%(topic)s</div>
<div class='k' id='num' style='font-size:124px'>%(num)s</div>
<div class='k' id='sub' style='font-size:62px'>%(sub)s</div>
</div>
%(icon)s
<div class='src'>%(src)s</div>
<script>
document.fonts.ready.then(()=>{
  const W=920, fs=e=>parseFloat(e.style.fontSize||getComputedStyle(e).fontSize), set=(e,s)=>e.style.fontSize=s+'px';
  const T=document.getElementById('topic'),N=document.getElementById('num'),S=document.getElementById('sub'),C=document.getElementById('col'),I=document.getElementById('ico');
  const fitW=(e,min)=>{let s=fs(e);while(e.scrollWidth>W&&s>min){s-=2;set(e,s);}};
  fitW(T,96);
  // 위계: 숫자는 주제어의 0.8배를 넘지 않는다, 보조 줄은 숫자의 0.75배를 넘지 않는다
  set(N,Math.min(fs(N),Math.floor(fs(T)*0.8))); fitW(N,60);
  set(S,Math.min(fs(S),Math.floor(fs(N)*0.75))); fitW(S,34);
  // 세로: 글 칸이 그림 위(그림 윗변 - 24)를 넘으면 셋을 같이 줄인다
  const lim=()=>I.getBoundingClientRect().top-24;
  let g=0; while(C.getBoundingClientRect().bottom>lim()&&g<40){g++;for(const e of [T,N,S]) if(e.textContent.trim()) set(e,Math.floor(fs(e)*0.96));}
  const src=document.querySelector('.src'); let s=fs(src); while(src.scrollWidth>920&&s>18){s-=1;set(src,s);}
  document.body.dataset.ready=1});
</script></body></html>"""


def esc(t): return (t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('/', '<br>')


def body_text(pkg):
    fs = [os.path.join(pkg, 'title.txt'), os.path.join(pkg, 'facts.txt')] + sorted(glob.glob(os.path.join(pkg, 'c??.txt')))
    return ''.join(open(f, encoding='utf-8').read() for f in fs if os.path.exists(f))


def board(new_png, recent, out, new_name='새 표지'):
    """최근 표지 10장 + 새 표지를 100px로 한 줄에 — 목록에서 보는 크기."""
    from PIL import Image, ImageDraw, ImageFont
    S, G = 100, 12
    items = [(n, p) for _, n, p in recent] + [(new_name, new_png)]
    W = G + len(items) * (S + G); H = G + S + 34
    im = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 11)
    for i, (n, p) in enumerate(items):
        x = G + i * (S + G)
        t = Image.open(p).convert('RGB'); w, h = t.size; m = min(w, h)
        t = t.crop(((w - m) // 2, (h - m) // 2, (w - m) // 2 + m, (h - m) // 2 + m)).resize((S, S), Image.LANCZOS)
        im.paste(t, (x, G))
        if i == len(items) - 1: d.rectangle((x - 4, G - 4, x + S + 3, G + S + 3), outline=(220, 38, 38), width=3)
        d.text((x, G + S + 8), n[:14], font=f, fill=(60, 60, 60))
    im.save(out)
    return out


def make(pkg, topic, num='', sub='', icon='auto', label='', src='', bg='auto', out=None, page=None):
    pkg = os.path.abspath(pkg) if pkg else None
    side = os.path.dirname(os.path.abspath(out)) if out else pkg   # --out을 주면 묶음에는 아무것도 쓰지 않는다(견본)
    out = os.path.abspath(out or os.path.join(pkg, 'img', '00.png'))
    if icon in (None, '', 'auto'):
        icon = guess_icon(' '.join([topic, num, sub, open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read() if pkg and os.path.exists(os.path.join(pkg, 'title.txt')) else '']))
        if not icon: raise SystemExit('주제 사물 아이콘을 못 골랐다 — --icon <이름> 을 준다(--icons <주제어>로 찾기)')
    if pkg:  # 표지 숫자는 본문·facts에 있는 것만
        txt = re.sub(r'\s', '', body_text(pkg))
        miss = [w for w in re.findall(r'[0-9][0-9,.~%]*[0-9가-힣%]*', ' '.join([topic, num, sub])) if re.sub(r'\s', '', w) not in txt]
        if miss: print('[경고] 표지 숫자 중 본문·facts에서 못 찾은 것:', miss)
    recent = recent_covers(10, exclude=pkg)
    if bg == 'auto': bg = pick_bg(recent)
    b, ink, acc, mut = PAL[bg]
    html = HTML % dict(f=FONTS, bg=b, ink=ink, acc=acc, mut=mut, label=esc(label), topic=esc(topic), num=esc(num), sub=esc(sub),
                       src=esc(src).replace('<br>', '/'), icon=icon_svg(icon, acc, 300))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    hp = os.path.splitext(out)[0] + '_cover.html'
    open(hp, 'w', encoding='utf-8').write(html)
    own = page is None
    if own:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start(); br = pw.chromium.launch(); page = br.new_page(viewport={'width': 1080, 'height': 1080})
    try:
        page.goto(Path(hp).as_uri()); page.wait_for_selector('body[data-ready]')
        m = page.evaluate("""(()=>{const r=id=>{const e=document.getElementById(id);const b=e.getBoundingClientRect();
            return {px:parseFloat(getComputedStyle(e).fontSize),l:b.left,t:b.top,r:b.right,b:b.bottom,w:e.scrollWidth,txt:e.textContent.trim()}};
            const i=document.getElementById('ico').getBoundingClientRect();
            return {topic:r('topic'),num:r('num'),sub:r('sub'),ico:[i.left,i.top,i.right,i.bottom]}})()""")
        page.screenshot(path=out)
    finally:
        if own: br.close(); pw.stop()
    os.remove(hp)
    # 위계·넘침 검사 — 어기면 멈춘다
    T, N, S = m['topic'], m['num'], m['sub']
    bad = []
    if N['txt'] and not T['px'] > N['px']: bad.append(f"숫자 줄({N['px']}px)이 주제어 줄({T['px']}px)보다 크거나 같다")
    if S['txt'] and N['txt'] and not N['px'] > S['px']: bad.append(f"보조 줄({S['px']}px)이 숫자 줄({N['px']}px) 이상")
    for k, e in (('주제어', T), ('숫자', N), ('보조', S)):
        if e['txt'] and (e['w'] > 925 or e['r'] > 1010): bad.append(f'{k} 줄 가로 넘침({e["w"]}px)')
    ico = m['ico']
    if ico[2] - ico[0] < 200: bad.append('주제 사물 그림이 200px보다 작다')
    if max(e['b'] for e in (T, N, S) if e['txt']) > ico[1] - 10 and min(e['r'] for e in (T, N, S) if e['txt']) > ico[0]:
        bad.append('글자가 그림과 겹친다')
    if T['px'] < 96: bad.append(f"주제어 줄 {T['px']}px — 너무 길다(100px 판에서 안 읽힘). 줄을 '/'로 나누거나 짧게")
    if bad: raise SystemExit('표지 거부: ' + '; '.join(bad))
    from PIL import Image
    im = Image.open(out); assert im.size == (1080, 1080), im.size
    stem = '' if side == pkg else os.path.splitext(os.path.basename(out))[0] + '_'
    t100 = os.path.join(side, stem + 'cover_100.png'); im.resize((100, 100), Image.LANCZOS).save(t100)
    bp = board(out, recent, os.path.join(side, stem + 'cover_board.png'), '새: ' + (os.path.basename(os.path.dirname(pkg)) if pkg else os.path.basename(side)))
    meta = dict(made_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), by='work/cafecover.py', out=os.path.relpath(out, side),
                topic=topic, num=num, sub=sub, label=label, src=src, icon=icon, icon_license=ICON_LICENSE, palette=bg,
                topic_px=T['px'], num_px=N['px'] if N['txt'] else 0, sub_px=S['px'] if S['txt'] else 0,
                board=[n for _, n, _ in recent])
    json.dump(meta, open(os.path.join(side, stem + 'cover_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"표지 {out} · 바탕 {bg} · 그림 {icon} · 주제어 {T['px']}px > 숫자 {meta['num_px']}px > 보조 {meta['sub_px']}px")
    print(f'  100px: {t100}\n  비교판(최근 {len(recent)}장 옆): {bp}')
    print('  → 두 파일을 Read로 보고 cover_review.md에 적는다:\n     100px 읽힘: <읽힌 주제어>\n     최근 10장 옆 구별: <색·그림으로 구별되는지>')
    return meta


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--icons':
        q = ' '.join(sys.argv[2:])
        g = guess_icon(q); print('추천:', g or '없음')
        if q: print('이름에', q, '든 아이콘:', [os.path.basename(f)[:-4] for f in glob.glob(os.path.join(ICONS, f'*{q}*.mjs'))][:30])
        sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument('pkg', nargs='?')
    ap.add_argument('--topic', required=True); ap.add_argument('--num', default=''); ap.add_argument('--sub', default='')
    ap.add_argument('--icon', default='auto'); ap.add_argument('--label', default=''); ap.add_argument('--src', default='')
    ap.add_argument('--bg', default='auto', choices=['auto'] + list(PAL)); ap.add_argument('--out')
    a = ap.parse_args()
    if not a.pkg and not a.out: ap.error('pkg 또는 --out')
    make(a.pkg, a.topic, a.num, a.sub, a.icon, a.label, a.src, a.bg, a.out)
