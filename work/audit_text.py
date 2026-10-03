# 카페 글 글짓기 관문 — 숫자 밀도·원문 용어·제목 틀·글끼리 반복 문장
#   python3 work/audit_text.py <pkg 폴더> [...]            → 걸리면 종료 코드 1
# 기준(근거):
#   - 숫자 밀도: 숫자/1000어절과 숫자 2개 이상 든 문장 %가 경쟁 카페 글(work/research/cafe_style/benchmark_*.json,
#     '잘 읽히는 카페 글' 실측 표본)의 최대값을 넘으면 거부. 우리 글과 경쟁 글을 이 파일의 같은 함수로 잰다.
#     숫자 세는 법은 speechcompare.py와 같다(\d[\d,.]* 덩어리 하나 = 숫자 하나).
#   - 원문 용어: RULES.md '화면 글자·그래프 규칙' 2번(2026-10-03 사장님)의 바꿔 쓰기 목록(결정세액·총급여·몫·상위 51%~100%)이 나오면 거부.
#   - 제목 틀: 묶음(같이 검사한 글) 중 쉼표 없는 제목이 8편에 2편 꼴(25%) 미만이면 거부 — RULES.md 2026-10-03 audit 줄('하루 8편 중 2편 이상 쉼표 없는 제목').
#   - 반복 문장: 같은 4어절 덩어리가 묶음의 30% 이상 글에 나오면 경고(유튜브·네이버 '템플릿 반복' 신호 — RULES 5장 스팸정책 줄). 출처·AI 고지 줄도 센다(고지는 필요하니 문장만 바꿔 쓴다).
import glob, json, os, re, statistics, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = re.compile(r'\d[\d,.]*')
SPLIT = re.compile(r'(?<=[.?!])\s+|\n+')
JARGON = [('결정세액', '실제 낸 세금'), ('총급여', '연봉'), ('몫', '비중'), (re.compile(r'상위\s*51\s*%\s*(부터|~)\s*100\s*%'), '아래 절반')]


def sentences(text):
    return [s.strip() for s in SPLIT.split(text) if len(s.strip()) > 3 and not s.strip().startswith('|')]


def density(text):
    """(숫자/1000어절, 숫자 2개 이상 문장 %, 어절 수). 표(| 로 시작하는 줄)는 뺀다 — 표는 읽는 글이 아니라 찾아보는 칸."""
    body = '\n'.join(l for l in text.splitlines() if not l.strip().startswith('|') and not l.strip().startswith('http'))
    words = len(body.split())
    n = len(NUM.findall(body))
    ss = sentences(body)
    multi = sum(1 for s in ss if len(NUM.findall(s)) >= 2)
    return 1000 * n / max(words, 1), 100 * multi / max(len(ss), 1), words


def baseline(root=ROOT):
    """경쟁 카페 글 표본(제목으로 중복 제거)의 숫자 밀도 중앙·최대."""
    seen, rows = set(), []
    for f in sorted(glob.glob(os.path.join(root, 'work', 'research', 'cafe_style', 'benchmark_*.json'))):
        for x in json.load(open(f, encoding='utf-8')):
            if x.get('text') and x.get('title') not in seen:
                seen.add(x.get('title')); rows.append(density(x['text']))
    if not rows:
        return None
    d = [r[0] for r in rows]; m = [r[1] for r in rows]
    return {'n': len(rows), 'dens_med': statistics.median(d), 'dens_max': max(d), 'multi_med': statistics.median(m), 'multi_max': max(m)}


def body_of(pkg):
    parts = [open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(pkg, 'c[0-9][0-9].txt')))]
    return '\n'.join(parts)


def title_of(pkg):
    p = os.path.join(pkg, 'title.txt')
    return open(p, encoding='utf-8').read().strip() if os.path.exists(p) else ''


def jargon_hits(text):
    hits = []
    for pat, plain in JARGON:
        n = len(pat.findall(text)) if hasattr(pat, 'findall') else text.count(pat)
        if n:
            hits.append((pat.pattern if hasattr(pat, 'pattern') else pat, plain, n))
    return hits


def shared_phrases(bodies, k=4, share=0.3):
    where = defaultdict(set)
    for name, text in bodies.items():
        w = text.split()
        for i in range(len(w) - k + 1):
            g = ' '.join(w[i:i + k])
            if NUM.search(g):
                continue
            where[g].add(name)
    need = max(3, int(share * len(bodies) + 0.999))
    return sorted(((g, sorted(s)) for g, s in where.items() if len(s) >= need), key=lambda x: -len(x[1]))


def audit(pkgs, base):
    report = {'posts': [], 'batch': []}
    bodies = {}
    for p in pkgs:
        name = os.path.basename(os.path.dirname(p.rstrip('/'))) or p
        body = body_of(p); bodies[name] = body
        d, m, w = density(body)
        fails = []
        if base and d > base['dens_max']:
            fails.append(f"숫자 밀도 {d:.0f}/1000어절 > 경쟁 최대 {base['dens_max']:.0f} (경쟁 중앙 {base['dens_med']:.0f})")
        if base and m > base['multi_max']:
            fails.append(f"숫자 2개+ 문장 {m:.0f}% > 경쟁 최대 {base['multi_max']:.0f}% (경쟁 중앙 {base['multi_med']:.0f}%)")
        for pat, plain, n in jargon_hits(title_of(p) + '\n' + body):
            fails.append(f"원문 용어 '{pat}' {n}번 → '{plain}'(RULES 화면 글자 규칙 2)")
        report['posts'].append({'name': name, 'title': title_of(p), 'dens': d, 'multi': m, 'words': w, 'fails': fails})
    titles = [x['title'] for x in report['posts'] if x['title']]
    if titles:
        nocomma = sum(1 for t in titles if ',' not in t)
        if nocomma < 0.25 * len(titles):
            report['batch'].append(('거부', f'쉼표 없는 제목 {nocomma}/{len(titles)}편 — 8편에 2편(25%) 이상이어야(RULES 10/3 audit)'))
    for g, names in shared_phrases(bodies)[:15]:
        report['batch'].append(('경고', f"'{g}' — {len(names)}/{len(bodies)}편에 같은 4어절"))
    return report


def main(argv):
    if not argv:
        print('사용법: python3 work/audit_text.py <pkg 폴더> [...]'); return 2
    base = baseline()
    if base:
        print(f"경쟁 카페 글 {base['n']}편: 숫자/1000어절 중앙 {base['dens_med']:.0f}·최대 {base['dens_max']:.0f} · 숫자 2개+ 문장 중앙 {base['multi_med']:.0f}%·최대 {base['multi_max']:.0f}%")
    else:
        print('경쟁 표본 없음 — 숫자 밀도 판정 확인 안 함')
    r = audit(argv, base)
    bad = 0
    for x in r['posts']:
        print(f"== {x['name']} | {x['title']} | 숫자 {x['dens']:.0f}/1000어절 · 2개+ 문장 {x['multi']:.0f}% · {'거부 ' + str(len(x['fails'])) if x['fails'] else '통과'}")
        for f in x['fails']:
            print('  ' + f)
        bad += bool(x['fails'])
    if r['posts']:
        ds = [x['dens'] for x in r['posts']]; ms = [x['multi'] for x in r['posts']]
        print(f"우리 {len(ds)}편: 숫자/1000어절 중앙 {statistics.median(ds):.0f} · 2개+ 문장 중앙 {statistics.median(ms):.0f}%")
    for k, s in r['batch']:
        print(f'[묶음·{k}] {s}')
        bad += k == '거부'
    return 1 if bad else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
