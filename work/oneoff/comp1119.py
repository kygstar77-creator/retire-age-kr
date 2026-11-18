# 경쟁 배수: 질의어마다 최근 180일·4분 이상 조회순 상위 10편 ÷ 그 채널 최근 4분 이상 10편 조회 중앙 (topic_stats_1112와 같은 법)
import sys, json, re, statistics, datetime
sys.path.insert(0, '.')
import ytupload
yt = ytupload.service()
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = [int(x or 0) for x in m.groups()]; return h*3600+mi*60+se
after = (datetime.datetime(2026,11,19) - datetime.timedelta(days=180)).strftime('%Y-%m-%dT00:00:00Z')
res = {}
for q in sys.argv[1:]:
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=after, videoDuration='medium', regionCode='KR', relevanceLanguage='ko', maxResults=15).execute()
    vids = [i['id']['videoId'] for i in r['items']]
    vv = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(vids)).execute()['items']
    vv = [v for v in vv if dur(v['contentDetails']['duration']) >= 240][:10]
    rows = []
    for v in vv:
        cid = v['snippet']['channelId']
        up = 'UU' + cid[2:]
        try:
            pl = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=40).execute()['items']
            ids = [p['contentDetails']['videoId'] for p in pl]
            cv = yt.videos().list(part='statistics,contentDetails', id=','.join(ids)).execute()['items']
            cv = [int(x['statistics'].get('viewCount', 0)) for x in cv if dur(x['contentDetails']['duration']) >= 240][:10]
            med = statistics.median(cv) if cv else None
        except Exception as e:
            med = None
        views = int(v['statistics'].get('viewCount', 0))
        rows.append(dict(id=v['id'], ch=v['snippet']['channelTitle'], t=v['snippet']['title'], d=v['snippet']['publishedAt'][:10], views=views, med=med, x=round(views/med, 2) if med else None))
    res[q] = rows
    xs = [r['x'] for r in rows if r['x']]
    print('==', q, '배수 중앙', statistics.median(xs) if xs else None, '표본', len(xs))
    for r in rows: print(' ', r['x'], r['views'], r['ch'][:12], r['d'], r['t'][:50])
json.dump(res, open('research/longform/loop/topic_stats_1119_comp.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
