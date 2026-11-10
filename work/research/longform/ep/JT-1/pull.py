# JT-1 주택연금 경쟁 표본: 최근 12개월 조회순 + 구독 대비 배수 (youtube-loop 11/11)
import sys, json, datetime, os, statistics
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import ytupload, re
yt = ytupload.service()
here = os.path.dirname(os.path.abspath(__file__))
since = (datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
ids = []
for q in ('주택연금', '주택연금 얼마'):
    for d in ('medium', 'long'):
        r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=since, videoDuration=d, regionCode='KR', relevanceLanguage='ko', maxResults=25).execute()
        ids += [i['id']['videoId'] for i in r.get('items', []) if i['id']['videoId'] not in ids]
vs = []
for i in range(0, len(ids), 50):
    vs += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
chs = list({v['snippet']['channelId'] for v in vs}); subs = {}
for i in range(0, len(chs), 50):
    for c in yt.channels().list(part='statistics', id=','.join(chs[i:i+50])).execute()['items']:
        subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
def mins(p):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', p); h, mi, s = (int(x or 0) for x in m.groups()); return round(h*60+mi+s/60, 1)
rows = []
for v in vs:
    t = v['snippet']['title']
    if '주택연금' not in t and '역모기지' not in t: continue
    sc = subs.get(v['snippet']['channelId'], 0); vw = int(v['statistics'].get('viewCount', 0))
    rows.append(dict(id=v['id'], title=t, ch=v['snippet']['channelTitle'], date=v['snippet']['publishedAt'][:10], views=vw, subs=sc, mult=round(vw/sc, 2) if sc else None, mins=mins(v['contentDetails']['duration'])))
rows.sort(key=lambda r: -r['views'])
json.dump(rows, open(os.path.join(here, 'raw', 'yt_top_jt1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('제목에 주택연금 든 편', len(rows), '· 조회 중앙', statistics.median([r['views'] for r in rows]), '· 길이 중앙', statistics.median([r['mins'] for r in rows]))
for r in rows[:25]: print(f"{r['views']:>9,} {r['mult']!s:>6}배 {r['mins']:>5}분 {r['date']} {r['id']} {r['ch']} | {r['title'][:70]}")
