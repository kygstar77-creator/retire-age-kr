# H-1 주택연금: 최근 1년·4~20분/20분+ 조회순 상위 (유튜브 Data API, 내부 판단용·30일 안 재측정)
import sys, json, re, datetime
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import ytupload
yt = ytupload.service()
since = (datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = (int(x or 0) for x in m.groups()); return h*60 + mi + se/60
out = {}
for q in sys.argv[1:]:
    ids = []
    for d in ('medium', 'long'):
        r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=since, videoDuration=d, regionCode='KR', relevanceLanguage='ko', maxResults=15).execute()
        ids += [i['id']['videoId'] for i in r.get('items', [])]
    if not ids: print('== '+q+': 0편'); continue
    v = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[:50])).execute()['items']
    chs = list({x['snippet']['channelId'] for x in v})
    c = {x['id']: int(x['statistics'].get('subscriberCount', 0) or 0) for x in yt.channels().list(part='statistics', id=','.join(chs[:50])).execute().get('items', [])}
    rows = []
    for x in v:
        views = int(x['statistics'].get('viewCount', 0)); subs = c.get(x['snippet']['channelId'], 0)
        rows.append(dict(id=x['id'], title=x['snippet']['title'], ch=x['snippet']['channelTitle'], date=x['snippet']['publishedAt'][:10], views=views, subs=subs, ratio=round(views/subs, 2) if subs else None, min=round(dur(x['contentDetails']['duration']), 1)))
    rows.sort(key=lambda r: -r['views']); out[q] = rows
    vs = sorted(r['views'] for r in rows)
    print(f'== {q}: {len(rows)}편 조회 중앙 {vs[len(vs)//2]:,}')
    for r in rows[:15]: print(f"  {r['id']} {r['views']:>9,} x{r['ratio']} {r['min']}분 {r['date']} {r['ch'][:14]} | {r['title'][:70]}")
json.dump(out, open('raw/yt_top.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
