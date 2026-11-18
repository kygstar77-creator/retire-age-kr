# 11/26 롱폼 칸 후보 비교용: 우리 공개 롱폼(4분 이상) 지금 조회·일당 조회 (youtube-loop 11/19)
import sys, json, re, datetime
sys.path.insert(0, '.')
import ytupload
yt = ytupload.service()
ch = yt.channels().list(part='contentDetails', mine=True).execute()
up = ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']
ids, tok = [], None
while True:
    r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
    ids += [i['contentDetails']['videoId'] for i in r['items']]
    tok = r.get('nextPageToken')
    if not tok: break
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = [int(x or 0) for x in m.groups()]; return h*3600+mi*60+se
out = []
for i in range(0, len(ids), 50):
    r = yt.videos().list(part='snippet,statistics,contentDetails,status', id=','.join(ids[i:i+50])).execute()
    for v in r['items']:
        st = v['status']; pub = st.get('publishAt') or v['snippet']['publishedAt']
        out.append(dict(id=v['id'], t=v['snippet']['title'], d=v['snippet']['publishedAt'][:10], sec=dur(v['contentDetails']['duration']),
                        views=int(v['statistics'].get('viewCount', 0)), priv=st['privacyStatus'], publishAt=st.get('publishAt')))
json.dump(out, open('research/longform/loop/topic_stats_1119_ours.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
now = datetime.date(2026, 11, 19)
longs = sorted([o for o in out if o['priv'] == 'public' and o['sec'] >= 240], key=lambda o: o['d'], reverse=True)
for o in longs[:40]:
    age = (now - datetime.date.fromisoformat(o['d'])).days or 1
    print(o['d'], o['id'], o['views'], round(o['views']/age, 1), o['sec']//60, o['t'][:60])
import statistics
print('최근 20편 중앙', statistics.median([o['views'] for o in longs[:20]]), '공개 롱폼 수', len(longs))
