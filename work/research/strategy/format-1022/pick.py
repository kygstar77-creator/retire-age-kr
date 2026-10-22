# 두 틀의 표본 고르기(10/22) — money_outliers.csv(작은 채널) + 큰 채널 검색(Data API search.list, 지난 1년, 조회순)
#   py -3.12 work/research/strategy/format-1022/pick.py search   → search_cache.json
#   py -3.12 work/research/strategy/format-1022/pick.py stats    → pool.json(videos.list·channels.list 숫자)
import sys, os, json, re, csv
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import ytupload
yt = ytupload.service()
AFTER = '2025-10-22T00:00:00Z'
QS = {'A': ['퇴직금으로 실제로 남은 돈', '1억 넣고 1년 뒤', '실제로 남은 돈 계산', '퇴직금 창업 현실 계산', '은퇴 후 치킨집 개인택시 수익'],
      'B': ['연봉 상위 몇 %', '순자산 상위 몇 %', '상위 몇 퍼센트', '내 자산 상위', '연금 상위 몇 %']}
def P(n): return os.path.join(HERE, n)
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    a = [int(x or 0) for x in m.groups()]; return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]

if sys.argv[1] == 'search':
    c = json.load(open(P('search_cache.json'), encoding='utf-8')) if os.path.exists(P('search_cache.json')) else {}
    for f, qs in QS.items():
        for q in qs:
            if q in c: continue
            r = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko', publishedAfter=AFTER,
                                 order='viewCount', videoDuration='medium', maxResults=25).execute()
            r2 = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko', publishedAfter=AFTER,
                                  order='viewCount', videoDuration='long', maxResults=25).execute()
            c[q] = dict(fmt=f, items=[dict(id=i['id']['videoId'], cid=i['snippet']['channelId'], ch=i['snippet']['channelTitle'], title=i['snippet']['title'])
                                      for i in r.get('items', []) + r2.get('items', [])])
            print(q, len(c[q]['items']))
            json.dump(c, open(P('search_cache.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
elif sys.argv[1] == 'stats':
    c = json.load(open(P('search_cache.json'), encoding='utf-8'))
    ids = {}
    for q, o in c.items():
        for i in o['items']: ids.setdefault(i['id'], dict(fmt=o['fmt'], q=q))
    for r in csv.DictReader(open(os.path.join(HERE, '..', 'outlier-1021', 'money_outliers.csv'), encoding='utf-8-sig')):
        t = r['title']
        if int(r['sec']) < 180: continue
        if re.search(r'퇴직금.*(남은|남는|계산|1년|3년|버티|다 쓴)|실제로 남|계산해\s?보니|넣고.*뒤', t): ids.setdefault(r['id'], dict(fmt='A', q='money_outliers'))
        if re.search(r'상위\s?\d|상위 몇|몇\s?%|퍼센트', t): ids.setdefault(r['id'], dict(fmt='B', q='money_outliers'))
    L = list(ids); vids = []
    for k in range(0, len(L), 50):
        vids += yt.videos().list(part='snippet,contentDetails,statistics', id=','.join(L[k:k+50])).execute()['items']
    cids = list({v['snippet']['channelId'] for v in vids}); chs = {}
    for k in range(0, len(cids), 50):
        for x in yt.channels().list(part='statistics,snippet', id=','.join(cids[k:k+50])).execute()['items']:
            chs[x['id']] = dict(subs=int(x['statistics'].get('subscriberCount', 0)), opened=x['snippet']['publishedAt'][:10])
    pool = []
    for v in vids:
        s = chs.get(v['snippet']['channelId'], {}); views = int(v['statistics'].get('viewCount', 0))
        pool.append(dict(id=v['id'], fmt=ids[v['id']]['fmt'], q=ids[v['id']]['q'], ch=v['snippet']['channelTitle'], subs=s.get('subs'), opened=s.get('opened'),
                         title=v['snippet']['title'], pub=v['snippet']['publishedAt'][:10], sec=sec(v['contentDetails']['duration']), views=views,
                         likes=int(v['statistics'].get('likeCount', 0)), x=round(views / max(s.get('subs') or 1, 1), 1)))
    pool.sort(key=lambda p: -p['views'])
    json.dump(pool, open(P('pool.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in pool:
        if p['sec'] >= 180: print(p['fmt'], p['views'], p['subs'], p['x'], p['sec'], p['pub'], p['id'], p['ch'], '|', p['title'][:70])
