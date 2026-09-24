# 우리 글끼리 얼마나 닮았나 — 제목이 달라도 틀이 같으면 스팸으로 잡힌다.
#   py -3.12 work/simcheck.py [최근 N=40]
#
# 사장님 2026-09-25: 중복 발행 때문에 블로그 신규 글이 통째로 노출에서 빠졌다.
# 네이버 공식 스팸 사례(2026-07-06)가 든 항목이 이것이다:
#   "동일·유사한 템플릿을 활용하여 콘텐츠를 무의미하게 대량으로 발행하는 경우.
#    문장 일부만 바꾼 페이지를 수십 개 이상 발행하는 방식이 이에 해당합니다."
#
# 제목 겹침은 이미 잡고 있다(naverpost.same_subject_today). 여기서 보는 것은 **본문**이다.
# 우리 글은 전부 같은 파이프라인으로 나가므로 제목이 달라도 틀이 같을 수 있다.
# 두 가지를 잰다:
#   ① 말 겹침 — 5글자 토막을 얼마나 공유하나(자카드). 같은 문장을 돌려 쓰면 높아진다.
#   ② 틀 겹침 — 문단 수·문단 길이 배열·첫 문장 형태·끝 문장 형태가 얼마나 같나.
import sys, os, re, glob, json, time, statistics, itertools, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')

def body_of(pkg):
    fs = sorted(glob.glob(os.path.join(pkg, 'b[0-9]*.txt'))) or sorted(glob.glob(os.path.join(pkg, 'c[0-9]*.txt')))
    out = []
    for f in fs:
        try: out.append(open(f, encoding='utf-8').read().strip())
        except Exception: pass
    return '\n'.join(out)

def shingles(t, k=5):
    """5글자 토막 집합. 같은 문장을 돌려 쓰면 여기가 겹친다."""
    s = re.sub(r'[\s\d,.%~·\-()]+', '', t)
    return {s[i:i + k] for i in range(max(0, len(s) - k + 1))}

def jac(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

def shape(t):
    """글의 틀. 숫자와 고유명사를 지우고 남는 뼈대를 본다."""
    paras = [x.strip() for x in t.splitlines() if x.strip()]
    if not paras: return None
    def skel(s):
        s = re.sub(r'\d[\d,.]*', 'N', s)                 # 숫자는 전부 N
        s = re.sub(r'[가-힣A-Za-z]{2,}(?=[은는이가을를])', 'X', s)   # 조사 앞 말은 X
        return s[:40]
    return {'n': len(paras), 'lens': [len(re.sub(r'\s', '', p)) for p in paras],
            'first': skel(paras[0]), 'last': skel(paras[-1]),
            'heads': tuple(skel(p) for p in paras[:3])}

def shape_sim(a, b):
    """틀이 얼마나 같나 0~1. 문단 수·길이 배열·첫/끝 문장 뼈대를 함께 본다."""
    if not a or not b: return 0.0
    n = 1 - abs(a['n'] - b['n']) / max(a['n'], b['n'], 1)
    m = min(len(a['lens']), len(b['lens']))
    if m == 0: return 0.0
    L = [1 - abs(x - y) / max(x, y, 1) for x, y in zip(a['lens'][:m], b['lens'][:m])]
    l = statistics.mean(L)
    f = 1.0 if a['first'] == b['first'] else jac(shingles(a['first'], 3), shingles(b['first'], 3))
    t = 1.0 if a['last'] == b['last'] else jac(shingles(a['last'], 3), shingles(b['last'], 3))
    return round(n * 0.2 + l * 0.4 + f * 0.2 + t * 0.2, 3)

def main():
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    pks = [p for p in glob.glob(os.path.join(R, '*', 'pkg')) if os.path.exists(os.path.join(p, 'published.txt'))]
    pks.sort(key=lambda p: -os.path.getmtime(os.path.join(p, 'published.txt')))
    docs = []
    for pk in pks[:top]:
        b = body_of(pk)
        if len(re.sub(r'\s', '', b)) < 300: continue
        try: title = open(os.path.join(pk, 'title.txt'), encoding='utf-8').read().strip()
        except Exception: title = os.path.basename(os.path.dirname(pk))
        kind = 'cafe' if glob.glob(os.path.join(pk, 'c[0-9]*.txt')) else 'blog'
        docs.append({'name': os.path.basename(os.path.dirname(pk)), 'title': title, 'kind': kind,
                     'sh': shingles(b), 'shape': shape(b), 'n': len(re.sub(r'\s', '', b))})
    print(f'검사 {len(docs)}편 (최근 발행분)')
    if len(docs) < 2: return

    rows = []
    for a, b in itertools.combinations(docs, 2):
        if a['kind'] != b['kind']: continue          # 블로그·카페는 애초에 다른 글이다
        rows.append((jac(a['sh'], b['sh']), shape_sim(a['shape'], b['shape']), a, b))
    rows.sort(key=lambda x: -(x[0] * 0.6 + x[1] * 0.4))

    print('\n말 겹침이 높은 쌍 (0.30 넘으면 같은 문장을 돌려 쓴 것)')
    hi = [r for r in rows if r[0] >= 0.30][:10]
    for w, s, a, b in hi or []:
        print(f'  말 {w:.2f} 틀 {s:.2f} | {a["title"][:34]}  ↔  {b["title"][:34]}')
    if not hi: print('  없음')

    print('\n틀 겹침이 높은 쌍 (0.75 넘으면 같은 템플릿으로 본다)')
    hs = [r for r in rows if r[1] >= 0.75][:10]
    for w, s, a, b in hs or []:
        print(f'  말 {w:.2f} 틀 {s:.2f} | {a["title"][:34]}  ↔  {b["title"][:34]}')
    if not hs: print('  없음')

    ws = [r[0] for r in rows]; ss = [r[1] for r in rows]
    print(f'\n전체 {len(rows)}쌍 · 말 겹침 중앙 {statistics.median(ws):.3f}(최대 {max(ws):.3f}) '
          f'· 틀 겹침 중앙 {statistics.median(ss):.3f}(최대 {max(ss):.3f})')
    out = {'at': time.strftime('%Y-%m-%d %H:%M'), 'docs': len(docs),
           'word_med': round(statistics.median(ws), 3), 'word_max': round(max(ws), 3),
           'shape_med': round(statistics.median(ss), 3), 'shape_max': round(max(ss), 3),
           'word_hi': len([1 for x in ws if x >= 0.30]), 'shape_hi': len([1 for x in ss if x >= 0.75])}
    json.dump(out, open(os.path.join(HERE, 'simcheck_last.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  기록 work/simcheck_last.json')

if __name__ == '__main__': main()
