# N-3 목차 대조·질문용 경쟁 영상 받기(2026-10-27, youtube-loop). 검색 3회.
import sys, json, re
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import ytupload
yt = ytupload.service()
Q = ['연봉 실수령액', '연봉 상위 몇 프로', '연봉 실수령액 표']
ids = []
for q in Q:
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter='2025-10-27T00:00:00Z',
                         regionCode='KR', relevanceLanguage='ko', maxResults=25, videoDuration='medium').execute()
    r2 = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter='2025-10-27T00:00:00Z',
                         regionCode='KR', relevanceLanguage='ko', maxResults=15, videoDuration='long').execute() if q == Q[0] else {'items': []}
    for it in r['items'] + r2['items']:
        v = it['id']['videoId']
        if v not in ids: ids.append(v)
vids = []
for i in range(0, len(ids), 50):
    vids += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
chs = {c['id']: int(c['statistics'].get('subscriberCount', 0) or 0) for c in yt.channels().list(part='statistics', id=','.join({v['snippet']['channelId'] for v in vids})[:2000]).execute()['items']}
def sec(d):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d); h, mi, s = (int(x or 0) for x in m.groups()); return h*3600+mi*60+s
out = []
for v in vids:
    sn, st = v['snippet'], v['statistics']; subs = chs.get(sn['channelId'], 0); views = int(st.get('viewCount', 0))
    out.append({'id': v['id'], 'title': sn['title'], 'channel': sn['channelTitle'], 'published': sn['publishedAt'][:10],
                'views': views, 'subs': subs, 'ratio': round(views / subs, 2) if subs else None, 'sec': sec(v['contentDetails']['duration']),
                'comments': int(st.get('commentCount', 0) or 0),
                'chapters': [l for l in sn['description'].splitlines() if re.match(r'\s*\(?\d{1,2}:\d\d', l)]})
out = [o for o in out if o['sec'] >= 240]
out.sort(key=lambda o: -o['views'])
json.dump(out, open(r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/longform/ep/N-3/raw/yt_1027.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out[:30]:
    print(o['id'], o['views'], o['ratio'], round(o['sec']/60, 1), o['published'], o['channel'][:12], '|', o['title'][:50], '| ch', len(o['chapters']), 'cm', o['comments'])
