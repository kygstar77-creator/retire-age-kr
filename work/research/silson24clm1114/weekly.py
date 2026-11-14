# 카페 주간 인기글(WeeklyPopularArticleList, cafe-copy-1019 방식) + 카페 검색에서 실손·청구 글 찾기 — silson24clm1114 11/14
import sys, json, re, time, html, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148', 'Referer': 'https://m.cafe.naver.com/'}
def get(u):
    try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read().decode('utf-8', 'ignore'))
    except Exception as e: return {'err': str(e)}
CAF = {'배투모': 31050378, '은오': 23676262, '월재연': 22290117, '짠돌이': 14028420, '정가거부': 30786704, '평생ETF': 31097286, '티끌': 30852806, '미주미': 28497937, '노후연구소': 20898041}
out = {}
for n, c in CAF.items():
    r = ((get(f'https://apis.naver.com/cafe-web/cafe2/WeeklyPopularArticleList.json?cafeId={c}').get('message') or {}).get('result') or {})
    L = [{'aid': a['articleId'], 's': html.unescape(re.sub(r'<[^>]+>', '', a.get('subject') or '')), 'read': a.get('readCount'), 'cmt': a.get('commentCount'), 'img': a.get('imageCount'), 'open': a.get('openArticle')} for a in r.get('popularArticleList') or []]
    out[n] = {'cafeId': c, 'list': L}
    for a in L:
        if re.search(r'실손|실비|보험|청구|병원', a['s']): print('HIT', n, c, a)
    print(n, len(L))
    time.sleep(0.3)
json.dump(out, open('bench_raw/weekly_1114.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 카페 안 검색(제목) — 같은 카페들에서 '실손24'
for n, c in CAF.items():
    q = urllib.parse.quote('실손24')
    r = ((get(f'https://apis.naver.com/cafe-web/cafe-mobile/CafeMobileWebArticleSearchListV4?cafeId={c}&query={q}&searchBy=1&sortBy=sim&page=1&perPage=10').get('message') or {}).get('result') or {})
    for a in (r.get('articleList') or [])[:5]:
        it = a.get('item') or a
        print('SRCH', n, c, it.get('articleId'), html.unescape(re.sub(r'<[^>]+>', '', it.get('subject') or '')), it.get('readCount'), it.get('commentCount'), it.get('writeDateTimestamp'))
    time.sleep(0.3)
