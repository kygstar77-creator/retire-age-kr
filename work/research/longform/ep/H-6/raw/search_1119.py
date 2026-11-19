# H-6 경쟁 목차 표본: 유튜브 Data API 검색(최근 12개월, 조회순) — 은마 직접 편 모으기
import sys, json, re, datetime
sys.path.insert(0, 'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import ytupload
yt = ytupload.service()
qs = ['은마아파트', '은마 분담금', '은마 재건축 이주', '대치 은마 시세']
after = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).strftime('%Y-%m-%dT00:00:00Z')
ids = {}
for q in qs:
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=after,
                         videoDuration='medium', regionCode='KR', relevanceLanguage='ko', maxResults=25).execute()
    for it in r['items']: ids.setdefault(it['id']['videoId'], q)
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=after,
                         videoDuration='long', regionCode='KR', relevanceLanguage='ko', maxResults=15).execute()
    for it in r['items']: ids.setdefault(it['id']['videoId'], q)
vids = list(ids); out = []
for i in range(0, len(vids), 50):
    r = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(vids[i:i+50])).execute()
    for v in r['items']:
        out.append(dict(id=v['id'], ch=v['snippet']['channelTitle'], chid=v['snippet']['channelId'],
            title=v['snippet']['title'], date=v['snippet']['publishedAt'][:10],
            dur=v['contentDetails']['duration'], views=int(v['statistics'].get('viewCount', 0)), q=ids[v['id']]))
chs = list({o['chid'] for o in out}); subs = {}
for i in range(0, len(chs), 50):
    r = yt.channels().list(part='statistics', id=','.join(chs[i:i+50])).execute()
    for c in r['items']: subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
for o in out: o['subs'] = subs.get(o['chid'], 0)
out.sort(key=lambda o: -o['views'])
json.dump(out, open('research/longform/ep/H-6/raw/yt_search_1119.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out:
    if '은마' in o['title']:
        print(o['views'], o['subs'], o['date'], o['dur'], o['ch'], '|', o['title'][:60], o['id'])
