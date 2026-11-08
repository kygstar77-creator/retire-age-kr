# W-3 제목 짝 비교용: 최근 30일 같은 주제 경쟁 롱폼 제목(유튜브 Data API, 조회순)
import sys, json, datetime
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import ytupload
yt = ytupload.service()
since = (datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - datetime.timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
seen = {}
for q in sys.argv[1:]:
    ids = []
    for d in ('medium', 'long'):
        r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=since, videoDuration=d, regionCode='KR', relevanceLanguage='ko', maxResults=10).execute()
        ids += [i['id']['videoId'] for i in r.get('items', [])]
    if not ids: continue
    for x in yt.videos().list(part='snippet,statistics', id=','.join(ids[:50])).execute()['items']:
        seen[x['id']] = (int(x['statistics'].get('viewCount', 0)), x['snippet']['publishedAt'][:10], x['snippet']['channelTitle'], x['snippet']['title'], q)
for vid, (v, d, ch, t, q) in sorted(seen.items(), key=lambda kv: -kv[1][0])[:20]:
    print(f'{v:>9,} | {d} | {ch} | {t} | {vid} | q={q}')
