# 블로그 대표 이미지(본문 첫 장) 자가발전 루프 — 사장님 2026-09-24 "제목도 사람들이 누르고 싶게 올리고 대표 사진도 마찬가지고."
#   py -3.12 work/coverstudy.py ["검색어" ...]          # 검색어를 안 주면 최근 발행 제목에서 뽑는다
# 썸네일 루프(thumb·thumbstat·loop)는 전부 유튜브용이었다. 블로그 대표 이미지는 재는 자도 규칙도 없었다.
# 유튜브에 한 것을 그대로 블로그에 한다: 상위 노출 글의 대표 이미지를 재고 → 우리 첫 장과 견주고 → 규칙 파일로 남긴다.
#
# 자료: 네이버 통합검색 블로그탭 결과 HTML의 search.pstatic.net 썸네일 URL
#   - blogpfthumb-phinf 는 글쓴이 프로필 사진이라 뺀다(본문 이미지가 아니다)
#   - 우리 것: work/research/*/pkg/img/00.png (order.txt의 첫 이미지)
# 남의 이미지는 재기만 하고 즉시 지운다. 글에 쓰지 않는다. 측정값만 남긴다.
import sys, os, re, json, time, glob, statistics, tempfile, shutil, collections
sys.stdout.reconfigure(encoding='utf-8')
from urllib.parse import unquote, quote
import urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import thumbstat
RES = os.path.join(HERE, 'research')
OUTMD = os.path.join(RES, 'coverrule.md')
KEYS = ['bright', 'contrast', 'sat', 'yellow', 'red', 'white', 'dark', 'text', 'text_top', 'text_mid', 'text_bot', 'text_thick']

def search_thumbs(kw, want=40):
    """블로그탭 검색 결과에서 본문 대표 이미지 URL을 뽑는다. (URL만 가져오고 페이지는 닫는다)"""
    from playwright.sync_api import sync_playwright
    url = f'https://search.naver.com/search.naver?where=blog&sm=tab_jum&query={quote(kw)}'
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(locale='ko-KR')
        page.goto(url, wait_until='domcontentloaded'); page.wait_for_timeout(3500)
        page.mouse.wheel(0, 4000); page.wait_for_timeout(1500)
        html = page.content()
        b.close()
    out, seen = [], set()
    for m in re.finditer(r'https://search\.pstatic\.net/common/\?src=([^"&]+)', html):
        src = unquote(m.group(1))
        if 'blogpfthumb-phinf' in src: continue          # 글쓴이 프로필 사진
        if not re.search(r'(blogfiles|postfiles|blogthumb)', src): continue
        key = src.split('?')[0]
        if key in seen: continue
        seen.add(key); out.append(src)
        if len(out) >= want: break
    return out

def measure_url(src, tmp):
    p = os.path.join(tmp, 'x%d.jpg' % abs(hash(src)))
    try:
        req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://search.naver.com/'})
        with urllib.request.urlopen(req, timeout=15) as r: data = r.read()
        if len(data) < 2000: return None
        open(p, 'wb').write(data)
        return thumbstat.measure(p)
    except Exception:
        return None
    finally:
        if os.path.exists(p): os.remove(p)      # 남의 이미지는 남기지 않는다

def ours(limit=25):
    """우리 글의 첫 장. order.txt가 가리키는 첫 이미지를 쓴다(없으면 img/00.png)."""
    rows = []
    for od in sorted(glob.glob(os.path.join(RES, '*', 'pkg', 'order.txt')), key=os.path.getmtime, reverse=True):
        pkg = os.path.dirname(od)
        first = None
        for line in open(od, encoding='utf-8'):
            m = re.search(r'(img/[\w.\-]+\.(?:png|jpg|jpeg))', line.strip())
            if m: first = m.group(1); break
        cand = os.path.join(pkg, first) if first else os.path.join(pkg, 'img', '00.png')
        if not os.path.exists(cand): continue
        st = thumbstat.measure(cand)
        if st: rows.append({**st, 'pkg': os.path.basename(os.path.dirname(pkg))})
        if len(rows) >= limit: break
    return rows

def default_keywords(n=4):
    """최근 발행 제목에서 검색어를 뽑는다 — 우리가 실제로 경쟁하는 화면을 재기 위해서."""
    ks = []
    for t in sorted(glob.glob(os.path.join(RES, '*', 'pkg', 'title.txt')), key=os.path.getmtime, reverse=True):
        s = open(t, encoding='utf-8').read().strip().split('\n')[0]
        s = re.sub(r'[\[\]"\'‘’“”]', ' ', s)
        w = [x for x in re.split(r'[\s,·—\-–?!]+', s) if 2 <= len(x) <= 8 and not x.isdigit()]
        if len(w) >= 2: ks.append(' '.join(w[:2]))
        if len(ks) >= n: break
    return ks

def main():
    kws = sys.argv[1:] or default_keywords()
    if not kws: print('검색어가 없다 — 인자로 직접 준다'); return
    tmp = tempfile.mkdtemp(prefix='cover')
    comp, per_kw = [], {}
    try:
        for kw in kws:
            urls = search_thumbs(kw)
            got = 0
            for u in urls:
                st = measure_url(u, tmp)
                if st: comp.append({**st, 'kw': kw}); got += 1
            per_kw[kw] = (len(urls), got)
            print(f'  {kw}: URL {len(urls)}개 → 측정 {got}장')
            time.sleep(2)                                  # 검색은 사람 속도로만
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    mine = ours()
    print(f'경쟁 {len(comp)}장 · 우리 {len(mine)}장')
    if len(comp) < 8 or len(mine) < 5:
        print('표본이 적어 규칙을 쓰지 않는다(경쟁 8장·우리 5장 이상 필요).'); return
    lines = [f'# 블로그 대표 이미지 규칙 (coverstudy.py 실측 {time.strftime("%Y-%m-%d %H:%M")})', '',
             f'네이버 블로그탭 상위 노출 글의 대표 이미지 {len(comp)}장 vs 우리 글 첫 장 {len(mine)}장. 잰 값만 적는다.',
             '검색어: ' + ', '.join(f'{k}(URL {a}→{b}장)' for k, (a, b) in per_kw.items()), '',
             '남의 이미지는 재고 바로 지웠다 — 글에 쓰지 않는다.', '',
             '| 항목 | 경쟁 중앙 | 우리 중앙 | 차이 |', '|---|---|---|---|']
    diffs = []
    FLOOR = 0.005     # 둘 다 이만큼도 안 되면 '차이'가 아니라 측정 바닥이다.
                      # 2026-09-24 첫 실측에서 빨강이 경쟁 0.0000·우리 0.0000인데 비율 계산 때문에
                      # '올린다'로 나왔다 — 없는 차이를 규칙으로 만들지 않는다.
    for k in KEYS:
        a = statistics.median(r[k] for r in comp); b = statistics.median(r[k] for r in mine)
        if max(a, b) < FLOOR:
            lines.append(f'| {k} | {a:.4f} | {b:.4f} | 둘 다 거의 0(판정 안 함) |'); continue
        mark = '우리가 높다' if b > a * 1.15 else ('우리가 낮다' if b * 1.15 < a else '비슷')
        lines.append(f'| {k} | {a:.4f} | {b:.4f} | {mark} |')
        if mark != '비슷': diffs.append((k, a, b, abs(b - a)))
    diffs.sort(key=lambda x: -x[3])     # 비율이 아니라 실제 벌어진 폭으로 줄 세운다
    lines += ['', '## 고칠 것(차이가 큰 순서)', '']
    NAME = {'bright': '밝기', 'contrast': '대비', 'sat': '채도', 'yellow': '노랑 면적', 'red': '빨강 면적',
            'white': '흰색 면적', 'dark': '어두운 면적', 'text': '글자 면적', 'text_top': '글자 위쪽',
            'text_mid': '글자 가운데', 'text_bot': '글자 아래쪽', 'text_thick': '글자 덩어리 두께'}
    if diffs:
        for k, a, b, _ in diffs[:5]:
            lines.append(f'- **{NAME.get(k, k)}**: 경쟁 {a:.4f} · 우리 {b:.4f} → blogimg.py에서 {"낮춘다" if b > a else "올린다"}')
    else:
        lines.append('- 이번 측정에서는 경쟁과 15% 넘게 벌어진 항목이 없다.')
    lines += ['', '이 파일은 firemap-write 회차가 묶음 첫 장을 만들 때 읽는다(textrule.md·titlerule.md와 같은 자리).', '']
    open(OUTMD, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    json.dump({'when': time.strftime('%Y-%m-%d %H:%M'), 'n_comp': len(comp), 'n_ours': len(mine),
               'comp': {k: round(statistics.median(r[k] for r in comp), 4) for k in KEYS},
               'ours': {k: round(statistics.median(r[k] for r in mine), 4) for k in KEYS}},
              open(os.path.join(RES, 'coverrule.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('저장', OUTMD)

if __name__ == '__main__': main()
