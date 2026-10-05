# 기존 카페 글 중 '고쳐 쓰면 검색 유입이 늘 만한 글' 후보를 줄 세운다.
#   py -3.12 work/refactorcands.py [후보 수=12]
# 2026-10-05 firemap-improve: 전체 회의 10/2 '기존 글 SEO 리팩토링' 보류분 → 10/4 복귀 뒤 improve 후보.
# 블로그는 수정 기능이 없고 9/23 뒤 새 글이 무색인이라(blog-noindex-since-0923) 카페만 본다.
# 카페는 naverpost.py rewrite로 고칠 수 있다.
#
# 재는 것(전부 실측, 추정 없음)
#   1) 카페 전체 글 조회수(로그인 없는 ArticleListV2dot1)
#   2) 제목 앞머리 검색어의 월간 검색수 + 같은 뜻의 더 큰 검색어(kwvol.py, 검색광고 키워드도구)
#   3) 그 검색어로 카페탭(m.search.naver.com ssc=tab.m_cafe.all)에서 우리 글이 몇 번째인가
# 후보 = 발행 3일 지난 글 중 조회 상위(관심은 증명됨) → 검색어가 크고 카페탭에 안 잡히는 순.
import sys, os, re, json, time, datetime, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CLUBID = '31789001'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36',
      'Referer': 'https://cafe.naver.com/'}
MUA = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36'}
OUT = os.path.join(HERE, 'research', 'refactor-candidates.md')

def get(u, h):
    return urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=20).read().decode('utf-8', 'ignore')

def all_articles():
    out, page = [], 1
    while page < 20:
        u = ('https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=%s'
             '&search.queryType=lastArticle&search.page=%d&search.perPage=50' % (CLUBID, page))
        lst = json.loads(get(u, UA))['message']['result']['articleList']
        if not lst: break
        for a in lst:
            out.append({'id': a.get('articleId'), 'title': a.get('subject', ''), 'read': a.get('readCount') or 0,
                        'ts': (a.get('writeDateTimestamp') or 0) / 1000, 'menu': a.get('menuName', '')})
        if len(lst) < 50: break
        page += 1; time.sleep(1)
    return out

def head_kw(title):
    # 제목 앞머리: 쉼표·괄호·숫자 앞까지, 최대 3어절
    t = re.sub(r'^\[[^\]]*\]\s*', '', title)
    t = re.split(r'[,?·!]', t)[0]
    w = t.split()
    # 숫자 어절 앞에서 끊되, 한 어절만 남으면 숫자까지 넣는다('예금 3억 이자' → '예금 3억 이자')
    cut = next((i for i, x in enumerate(w) if i and x[0].isdigit()), len(w))
    if cut < 2: cut = len(w)
    return ' '.join(w[:min(cut, 3)]).strip()

def vol(kws):
    try:
        import kwvol
        kv = kwvol.load()
    except SystemExit as e:
        print('kwvol 불가:', e); return {}
    res = {}
    for k in kws:
        hint = k.replace(' ', '')
        try:
            rows = kwvol.call(kv, [hint])
        except Exception as e:
            res[k] = {'err': str(e)[:60]}; time.sleep(1); continue
        def n(r):
            s = 0
            for f in ('monthlyPcQcCnt', 'monthlyMobileQcCnt'):
                v = r.get(f); s += 5 if isinstance(v, str) else (v or 0)
            return s
        me = next((r for r in rows if r['relKeyword'] == hint), None)
        core = hint[:2]
        bigger = sorted([r for r in rows if core in r['relKeyword'] and r['relKeyword'] != hint], key=n, reverse=True)[:3]
        res[k] = {'vol': n(me) if me else 0, 'bigger': ['%s %d' % (r['relKeyword'], n(r)) for r in bigger]}
        time.sleep(1)
    return res

def cafe_tab_rank(kw, aid):
    u = 'https://m.search.naver.com/search.naver?ssc=tab.m_cafe.all&query=' + urllib.parse.quote(kw)
    try:
        s = get(u, MUA)
    except Exception as e:
        return 'err'
    if len(s) < 2000: return 'blocked'
    links = re.findall(r'cafe\.naver\.com/([a-zA-Z0-9_]+)/(\d+)', s)
    seen = []
    for c, n in links:
        if (c, n) not in seen: seen.append((c, n))
    for i, (c, n) in enumerate(seen, 1):
        if c == 'firemap' and n == str(aid): return i
    return '-'

def main():
    arts = all_articles()
    now = time.time()
    old = [a for a in arts if a['ts'] and now - a['ts'] > 3 * 86400]
    old.sort(key=lambda a: -a['read'])
    reads = sorted(a['read'] for a in arts)
    med = reads[len(reads) // 2] if reads else 0
    top = old[:N]
    for a in top: a['kw'] = head_kw(a['title'])
    vols = vol(list({a['kw'] for a in top}))
    for a in top:
        a.update(vols.get(a['kw'], {}))
        a['rank'] = cafe_tab_rank(a['kw'], a['id']); time.sleep(3)
    # 우선순위: 카페탭에 안 잡힘(-) 먼저, 그다음 검색수 큰 순
    top.sort(key=lambda a: (a['rank'] not in ('-',), -(a.get('vol') or 0)))
    d = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    L = ['# 기존 카페 글 리팩토링 후보 — %s 실측 (work/refactorcands.py)' % d, '',
         '- 카페 전체 %d편 · 조회 중앙값 %d · 3일 지난 글 %d편 중 조회 상위 %d편' % (len(arts), med, len(old), len(top)),
         '- 검색어 = 제목 앞머리(최대 3어절) · 월검색 = PC+모바일(검색광고 키워드도구, <10은 5로 셈) · 카페탭 = 그 검색어로 카페탭 1페이지에서 우리 글 순서(- = 없음)',
         '- 고치는 법: 제목 앞머리를 더 큰 검색어로(뜻이 같을 때만) + 첫 문단에 그 검색어 한 번 → `naverpost.py rewrite <번호> <pkg>`. 같은 뜻이 아니면 바꾸지 않는다.', '',
         '| # | 번호 | 제목 | 조회 | 검색어 | 월검색 | 카페탭 | 같은 줄기 더 큰 검색어 |', '|---|---|---|---|---|---|---|---|']
    for i, a in enumerate(top, 1):
        L.append('| %d | %s | %s | %d | %s | %s | %s | %s |' % (
            i, a['id'], a['title'].replace('|', '/'), a['read'], a['kw'],
            a.get('vol', a.get('err', '?')), a['rank'], ' · '.join(a.get('bigger', []))))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L)); print('->', OUT)

if __name__ == '__main__':
    main()
