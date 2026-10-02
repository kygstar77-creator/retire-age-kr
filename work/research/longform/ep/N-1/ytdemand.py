# N-1 나 vs 남들 유튜브 수요: 최근 120일·4~20분, 조회순 상위 → 조회·구독 대비 배수·길이
import sys, json, re, datetime
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import ytupload
yt = ytupload.service()
since = (datetime.datetime.utcnow() - datetime.timedelta(days=120)).strftime('%Y-%m-%dT%H:%M:%SZ')
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = (int(x or 0) for x in m.groups()); return h*60 + mi + se/60
out = {}
for q in sys.argv[1:]:
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=since, videoDuration='medium', regionCode='KR', relevanceLanguage='ko', maxResults=25).execute()
    ids = [i['id']['videoId'] for i in r['items']]
    v = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']
    chs = list({x['snippet']['channelId'] for x in v})
    c = {x['id']: int(x['statistics'].get('subscriberCount', 0) or 0) for x in yt.channels().list(part='statistics', id=','.join(chs)).execute()['items']}
    rows = []
    for x in v:
        views = int(x['statistics'].get('viewCount', 0)); subs = c.get(x['snippet']['channelId'], 0)
        rows.append(dict(id=x['id'], title=x['snippet']['title'], ch=x['snippet']['channelTitle'], date=x['snippet']['publishedAt'][:10], views=views, subs=subs, ratio=round(views/subs, 2) if subs else None, min=round(dur(x['contentDetails']['duration']), 1)))
    rows.sort(key=lambda r: -r['views']); out[q] = rows
    vs = sorted(r['views'] for r in rows); ls = sorted(r['min'] for r in rows)
    print(f'== {q}: {len(rows)}편 조회 중앙 {vs[len(vs)//2]:,} · 길이 중앙 {ls[len(ls)//2]}분')
    for r in rows[:12]: print(f"  {r['views']:>9,} x{r['ratio']} {r['min']}분 {r['date']} {r['ch'][:14]} | {r['title'][:60]}")
json.dump(out, open(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\longform\ep\N-1\yt_top.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
