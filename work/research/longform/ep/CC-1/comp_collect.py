# CC-1 경쟁 영상 모으기 — Data API search 3회(최근 12개월·조회순·4분 넘는 영상) + videos/channels.list (youtube-loop 2026-11-22)
import sys, json
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytupload
yt = ytupload.service()
Q = ['KODEX 미국배당커버드콜액티브', '배당 커버드콜 ETF 수익률', '미국배당다우존스 커버드콜 비교']
ids = []
for q in Q:
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter='2025-11-22T00:00:00Z',
                         videoDuration='medium', regionCode='KR', relevanceLanguage='ko', maxResults=25).execute()
    ids += [i['id']['videoId'] for i in r['items'] if i['id']['videoId'] not in ids]
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter='2025-11-22T00:00:00Z',
                         videoDuration='long', regionCode='KR', relevanceLanguage='ko', maxResults=10).execute() if q == Q[0] else {'items': []}
    ids += [i['id']['videoId'] for i in r['items'] if i['id']['videoId'] not in ids]
vs = []
for i in range(0, len(ids), 50):
    vs += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
chs = list({v['snippet']['channelId'] for v in vs}); subs = {}
for i in range(0, len(chs), 50):
    for c in yt.channels().list(part='statistics', id=','.join(chs[i:i+50])).execute()['items']:
        subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
out = [dict(id=v['id'], ch=v['snippet']['channelTitle'], t=v['snippet']['title'], d=v['snippet']['publishedAt'][:10],
            dur=v['contentDetails']['duration'], views=int(v['statistics'].get('viewCount', 0)), subs=subs.get(v['snippet']['channelId'], 0),
            desc=v['snippet']['description'][:3000]) for v in vs]
out.sort(key=lambda x: -x['views'])
json.dump(out, open('raw/comp_1122.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out[:40]:
    print(o['views'], round(o['views'] / max(o['subs'], 1), 2), o['dur'], o['d'], o['ch'], '|', o['t'][:70], o['id'])
