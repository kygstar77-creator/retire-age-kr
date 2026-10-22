# 우리 공개 롱폼 전부: 노출·클릭률·유입 경로·평균 시청 비율·남은 비율 곡선·첫 7일 대 이후·공개 시각 (10/22 format-check)
#   py -3.12 work/research/strategy/format-1022/own.py   → own_longform.json
# 읽기만 한다. 조회·유입·곡선은 YouTube Analytics API, 노출·클릭률은 Reporting API 날짜별 csv(research/longform/loop/reach, ytreach.py가 받음).
import sys, os, json, glob, re, datetime, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import ytupload, ytanalytics as A, ytreach

yt = ytupload.service()
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    a = [int(x or 0) for x in m.groups()]; return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]

ch = yt.channels().list(part='contentDetails,statistics', mine=True).execute()['items'][0]
up = ch['contentDetails']['relatedPlaylists']['uploads']
ids, tok = [], None
while True:
    r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
    ids += [i['contentDetails']['videoId'] for i in r['items']]
    tok = r.get('nextPageToken')
    if not tok: break
vids = []
for k in range(0, len(ids), 50):
    r = yt.videos().list(part='snippet,contentDetails,statistics,status', id=','.join(ids[k:k+50])).execute()
    vids += r['items']
longs = [v for v in vids if v['status']['privacyStatus'] == 'public' and '#shorts' not in v['snippet']['title'].lower()
         and sec(v['contentDetails']['duration']) > 60]
print('전체', len(vids), '공개 롱폼', len(longs))

# 노출·클릭률: 날짜별 csv
reach = collections.defaultdict(dict)
for f in sorted(glob.glob(os.path.join(WORK, 'research', 'longform', 'loop', 'reach', '*.csv'))):
    d = os.path.basename(f)[:10]
    for v, (i, c) in ytreach.day(f).items(): reach[v][d] = (i, c)

today = datetime.date.today().isoformat()
out = []
for v in sorted(longs, key=lambda v: v['snippet']['publishedAt']):
    vid = v['id']; pub = v['snippet']['publishedAt']
    pk = datetime.datetime.fromisoformat(pub.replace('Z', '+00:00')) + datetime.timedelta(hours=9)
    # 분석 API·reach 날짜는 태평양 시간(10월 PDT, UTC−7) — 한국 11:30 공개는 태평양 전날 19:30이라 KST 날짜로 자르면 첫날이 빠진다
    p0 = (datetime.datetime.fromisoformat(pub.replace('Z', '+00:00')) - datetime.timedelta(hours=7)).date()
    row = dict(id=vid, title=v['snippet']['title'], pub_kst=pk.strftime('%Y-%m-%d %a %H:%M'), sec=sec(v['contentDetails']['duration']),
               views_pub=int(v['statistics'].get('viewCount', 0)), likes=int(v['statistics'].get('likeCount', 0)),
               comments=int(v['statistics'].get('commentCount', 0)))
    f = 'video==' + vid
    try:
        r = A.q('views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained', filters=f, start=p0.isoformat())
        if r.get('rows'): row.update(dict(zip(['a_views', 'min', 'avd', 'avp', 'subs'], r['rows'][0])))
        r = A.q('views', dims='insightTrafficSourceType', filters=f, start=p0.isoformat())
        row['traffic'] = {x[0]: x[1] for x in r.get('rows', [])}
        r = A.q('views', dims='day', filters=f, start=p0.isoformat(), sort='day')
        days = [(x[0], x[1]) for x in r.get('rows', [])]
        row['daily'] = days
        d7 = (p0 + datetime.timedelta(days=6)).isoformat()
        row['v7'] = sum(n for d, n in days if d <= d7); row['v_after7'] = sum(n for d, n in days if d > d7)
        row['v2'] = sum(n for d, n in days if d <= (p0 + datetime.timedelta(days=1)).isoformat())
        r = A.q('audienceWatchRatio,relativeRetentionPerformance', dims='elapsedVideoTimeRatio', filters=f, start=p0.isoformat())
        row['curve'] = [(x[0], round(x[1], 3), round(x[2], 3)) for x in r.get('rows', [])]
        r = A.q('views', dims='insightTrafficSourceDetail', filters=f + ';insightTrafficSourceType==YT_SEARCH', start=p0.isoformat(), sort='-views', maxResults=10)
        row['search_terms'] = [(x[0], x[1]) for x in r.get('rows', [])]
        r = A.q('views', dims='insightTrafficSourceDetail', filters=f + ';insightTrafficSourceType==RELATED_VIDEO', start=p0.isoformat(), sort='-views', maxResults=10)
        row['related_from'] = [(x[0], x[1]) for x in r.get('rows', [])]
    except Exception as e:
        row['err'] = str(e)[:200]
    rr = reach.get(vid, {})
    imp = sum(i for i, c in rr.values()); clicks = sum(i * c / 100 for i, c in rr.values())
    d7 = (p0 + datetime.timedelta(days=6)).isoformat()
    imp7 = sum(i for d, (i, c) in rr.items() if d <= d7); cl7 = sum(i * c / 100 for d, (i, c) in rr.items() if d <= d7)
    row.update(imp=imp, ctr=round(clicks / imp * 100, 2) if imp else None, imp7=imp7, ctr7=round(cl7 / imp7 * 100, 2) if imp7 else None,
               reach_days=sorted(rr.items()))
    out.append(row)
    print(vid, row['pub_kst'], row['views_pub'], row.get('avp'), imp, row['ctr'], row['title'][:40])
json.dump(dict(measured=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), subs_now=ch['statistics'].get('subscriberCount'),
               reach_files=[os.path.basename(f) for f in sorted(glob.glob(os.path.join(WORK, 'research', 'longform', 'loop', 'reach', '*.csv')))][::len(glob.glob(os.path.join(WORK, 'research', 'longform', 'loop', 'reach', '*.csv')))-1 or 1],
               videos=out), open(os.path.join(HERE, 'own_longform.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
