# 검색 상위 블로그들의 실제 발행 빈도 실측 — "하루 몇 편까지 써도 상위에 남는가"를 추측 대신 잰다.
#   python work/blogfreq.py "퇴직금계산기" "연봉계산기" ...   → 키워드별 블로그 탭 상위 결과의 블로그를 모아 RSS(최근 50편)로 편/일 계산
import sys, re, json, time, urllib.request, email.utils, collections
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from urllib.parse import quote
UA = {'User-Agent': 'Mozilla/5.0'}
def rss_stats(bid):
    try:
        s = urllib.request.urlopen(urllib.request.Request(f'https://rss.blog.naver.com/{bid}.xml', headers=UA), timeout=15).read().decode('utf-8', 'ignore')
    except Exception as e: return None
    dates = [email.utils.parsedate_to_datetime(d) for d in re.findall(r'<pubDate>(.*?)</pubDate>', s)]
    if not dates: return None
    days = collections.Counter(d.strftime('%Y-%m-%d') for d in dates)
    span = (max(dates) - min(dates)).days + 1
    return {'n': len(dates), 'span_days': span, 'per_day': round(len(dates) / span, 2), 'max_day': max(days.values()), 'last': max(dates).strftime('%Y-%m-%d')}
kws = sys.argv[1:]
found = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True); page = b.new_page(locale='ko-KR')
    for kw in kws:
        page.goto(f'https://search.naver.com/search.naver?ssc=tab.blog.all&query={quote(kw)}', wait_until='domcontentloaded'); page.wait_for_timeout(4000)
        ids = page.evaluate("() => [...document.querySelectorAll('a[href*=\"blog.naver.com/\"]')].map(a=>(a.href.match(/blog\.naver\.com\/([A-Za-z0-9_\-]+)\/\d+/)||[])[1]).filter(Boolean)")
        uniq = list(dict.fromkeys(ids))[:10]
        print(f'== {kw}: 상위 블로그 {len(uniq)}개')
        for rank, bid in enumerate(uniq, 1):
            found.setdefault(bid, []).append((kw, rank))
    b.close()
rows = []
for bid, hits in found.items():
    st = rss_stats(bid)
    if st: rows.append((bid, hits, st))
rows.sort(key=lambda r: -r[2]['per_day'])
print('\n블로그 | 키워드(순위) | 최근50편 기간(일) | 편/일 | 하루 최다')
for bid, hits, st in rows:
    print(f"{bid} | {','.join(f'{k}#{r}' for k, r in hits)} | {st['span_days']} | {st['per_day']} | {st['max_day']}")
per = [r[2]['per_day'] for r in rows]; mx = [r[2]['max_day'] for r in rows]
per.sort(); mx.sort()
print(f'\n블로그 {len(rows)}개: 편/일 중앙값 {per[len(per)//2]}, 상위 10% {per[int(len(per)*0.9)]}, 하루 최다 중앙값 {mx[len(mx)//2]}, 최대 {mx[-1]}')
print('편/일 2 이상:', sum(1 for x in per if x >= 2), '| 5 이상:', sum(1 for x in per if x >= 5), '| 10 이상:', sum(1 for x in per if x >= 10))
