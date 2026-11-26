# NDX-1 목차 대조용 경쟁 영상 모으기 (youtube-loop 2026-11-27) — 검색 6회, 최근 12개월, 조회순, 4분 이상
import sys, json, re, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
import ytupload
yt = ytupload.service()
Q = ['나스닥 하락장 회복', '나스닥100 원금 회복', 'QQQ 고점']
ids = {}
for q in Q:
    for dur in ('medium', 'long'):
        r = yt.search().list(q=q, part='id', type='video', order='viewCount', maxResults=25,
                             publishedAfter='2025-11-27T00:00:00Z', videoDuration=dur, regionCode='KR', relevanceLanguage='ko').execute()
        for it in r['items']: ids.setdefault(it['id']['videoId'], set()).add(q)
print('ids', len(ids))
vl = list(ids); vids = []
for i in range(0, len(vl), 50):
    vids += yt.videos().list(id=','.join(vl[i:i+50]), part='snippet,statistics,contentDetails').execute()['items']
ch = {v['snippet']['channelId'] for v in vids}; subs = {}
cl = list(ch)
for i in range(0, len(cl), 50):
    for c in yt.channels().list(id=','.join(cl[i:i+50]), part='statistics').execute()['items']:
        subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = (int(x or 0) for x in m.groups()); return h*3600+mi*60+se
out = []
for v in vids:
    vc = int(v['statistics'].get('viewCount', 0)); s = subs.get(v['snippet']['channelId'], 0)
    out.append(dict(id=v['id'], title=v['snippet']['title'], channel=v['snippet']['channelTitle'], views=vc, subs=s,
                    ratio=round(vc/s, 2) if s else None, sec=dur(v['contentDetails']['duration']), date=v['snippet']['publishedAt'][:10],
                    desc=v['snippet']['description'][:1500], q=sorted(ids[v['id']])))
out.sort(key=lambda x: -x['views'])
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'raw', 'yt_search_1127.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out[:60]:
    print(o['views'], o['ratio'], o['sec']//60, o['date'], o['id'], o['channel'][:14], '|', o['title'][:60])
