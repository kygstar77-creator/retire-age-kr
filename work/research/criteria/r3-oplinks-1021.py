# 잘되는 카페 15곳 운영자 글의 바깥 링크(네이버·유튜브 밖) 하루 횟수 실측
import sys, json, time, re, urllib.request, collections, datetime
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36','Referer': 'https://cafe.naver.com/'}
def get(u):
    try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read().decode('utf-8','ignore'))
    except Exception as e: return {'err': str(e)}
raw = json.load(open(sys.argv[1], encoding='utf-8'))
SKIP = re.compile(r'(naver\.(com|me|net)|pstatic|youtu|naver\.co)', re.I)
out = []
for c in raw:
    cid, sysop = c['cafeId'], c['sysop']
    arts = []
    for p in range(1, 7):
        d = get(f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.queryType=lastArticle&search.page={p}&search.perPage=50')
        r = (d.get('message') or {}).get('result') or {}
        arts += r.get('articleList') or []
        if not r.get('hasNext'): break
        time.sleep(0.3)
    ops = [a for a in arts if a.get('writerNickname') == sysop]
    days = collections.Counter(); linkdays = collections.Counter(); doms = collections.Counter(); seen = 0; locked = 0
    for a in ops[:40]:
        day = datetime.datetime.fromtimestamp(a['writeDateTimestamp']/1000).strftime('%m-%d')
        d = get(f"https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{cid}/articles/{a['articleId']}?useCafeId=true")
        time.sleep(0.25)
        if 'result' not in d: locked += 1; continue
        html = (d['result'].get('article') or {}).get('contentHtml') or ''
        hs = [h for h in re.findall(r'href="(https?://[^"]+)"', html) if not SKIP.search(h)]
        seen += 1; days[day] += 1
        if hs:
            linkdays[day] += 1
            for h in set(re.sub(r'^https?://(www\.)?([^/]+).*', r'\2', x) for x in hs): doms[h] += 1
    out.append(dict(cafe=cid, members=c['members'], arts=len(arts), op=len(ops), read=seen, locked=locked,
                    opdays=len(days), op_per_day=dict(days), link_per_day=dict(linkdays), domains=doms.most_common(5)))
    print(json.dumps(out[-1], ensure_ascii=False), flush=True)
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
