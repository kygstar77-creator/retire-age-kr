"""주제 검색 상위 영상 vs 그 채널 최근 10편 평균(공식 YouTube Data API). 사용: ytoutlier.py 질의... """
import sys, os, re, json, statistics
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ytupload
yt = ytupload.service()
Q = sys.argv[1:]
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600+int(m[2] or 0)*60+int(m[3] or 0)
out = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko',
                         publishedAfter='2025-10-01T00:00:00Z', order='viewCount', maxResults=15).execute()
    ids = [i['id']['videoId'] for i in r['items']]
    info = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']
    rows = []
    for v in info:
        cid = v['snippet']['channelId']
        up = yt.channels().list(part='contentDetails,statistics', id=cid).execute()['items'][0]
        pl = up['contentDetails']['relatedPlaylists']['uploads']
        items = yt.playlistItems().list(part='contentDetails', playlistId=pl, maxResults=11).execute()['items']
        rid = [i['contentDetails']['videoId'] for i in items if i['contentDetails']['videoId'] != v['id']][:10]
        rv = yt.videos().list(part='statistics', id=','.join(rid)).execute()['items'] if rid else []
        vs = [int(x['statistics'].get('viewCount', 0)) for x in rv]
        avg = statistics.mean(vs) if vs else None; med = statistics.median(vs) if vs else None
        views = int(v['statistics'].get('viewCount', 0))
        rows.append({'id': v['id'], 'title': v['snippet']['title'], 'channel': v['snippet']['channelTitle'], 'subs': int(up['statistics'].get('subscriberCount', 0) or 0),
                     'pub': v['snippet']['publishedAt'][:10], 'min': round(dur(v['contentDetails']['duration'])/60, 1), 'views': views,
                     'n_other': len(vs), 'avg10': round(avg) if avg else None, 'med10': round(med) if med else None,
                     'x_avg': round(views/avg, 2) if avg else None, 'x_med': round(views/med, 2) if med else None})
    out[q] = rows
    print('##', q)
    for x in rows: print(f"{x['views']:>9,} | 평균대비 {x['x_avg']} | 중앙대비 {x['x_med']} | 구독 {x['subs']:>8,} | {x['pub']} | {x['min']}분 | {x['channel'][:12]} | {x['title'][:40]}")
json.dump(out, open('research/ventures/r26-calendar/yt_outlier.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
