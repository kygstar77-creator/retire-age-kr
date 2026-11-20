# de1s_kofin 경쟁 쇼츠 모으기 — 유튜브 Data API search(짧은 영상, KR·ko, 10/1 이후) → compete_raw.json (firemap-video-producer 2026-11-20)
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytupload
yt = ytupload.service()
Q = ['고배당 ETF 금융주', 'PLUS 고배당주', 'TIGER 은행고배당플러스', 'SOL 코리아고배당', '국내 고배당 ETF', '은행 고배당 ETF', '국내 배당 ETF 추천', '고배당주 ETF 비교']
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
vids = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q, type='video', videoDuration='short', regionCode='KR', relevanceLanguage='ko',
                         publishedAfter='2026-10-01T00:00:00Z', order='viewCount', maxResults=15).execute()
    for it in r['items']: vids.setdefault(it['id']['videoId'], q)
ids = list(vids); info = []
for i in range(0, len(ids), 50):
    info += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
rows = []
for v in info:
    sec = dur(v['contentDetails']['duration'])
    if sec > 180: continue
    rows.append(dict(id=v['id'], q=vids[v['id']], title=v['snippet']['title'], channel=v['snippet']['channelTitle'],
                     views=int(v['statistics'].get('viewCount', 0)), sec=sec, pub=v['snippet']['publishedAt'][:10]))
rows.sort(key=lambda r: -r['views'])
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in rows[:30]: print(f"{r['views']:>7} {r['sec']:>3}s {r['pub']} {r['id']} [{r['channel'][:12]}] {r['title'][:60]}  <{r['q']}>")
