# X-1 썸네일 경쟁 상위 — 유튜브 Data API(ytupload.service, 읽기만)로 '환율·미국ETF·S&P500 환차손' 최근 30일 조회순 + 우리 채널 조회 상위 3
# py -3.12 fetch_compete.py → compete_thumb.json, src/<id>.jpg(maxresdefault, 없으면 hqdefault)
import sys, os, re, json, urllib.request, datetime
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, W); import ytupload
yt = ytupload.service()
AFTER = (datetime.datetime(2026, 10, 17) - datetime.timedelta(days=30)).strftime('%Y-%m-%dT00:00:00Z')
Q = ['환율 하락 미국 ETF', '환율 S&P500', '환차손 미국 주식', '환율 떨어지면 미국 ETF', 'S&P500 ETF 환노출 환헤지', '달러 환율 미국주식 손실']
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
vids = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko', publishedAfter=AFTER, order='viewCount', maxResults=15).execute()
    for it in r['items']: vids.setdefault(it['id']['videoId'], q)
ids = list(vids); info = []
for i in range(0, len(ids), 50):
    info += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
KEYW = re.compile(r'환율|달러|환차|환헤지|환노출')
TOPIC = re.compile(r'S&P|S＆P|에스앤피|미국 ?ETF|미국 ?주식|미국주식|나스닥|미국 ?지수|SPY|VOO|QQQ|해외 ?주식|ETF')
rows = []
for v in info:
    t = v['snippet']['title']; d = dur(v['contentDetails']['duration'])
    if d < 240 or not (KEYW.search(t) and TOPIC.search(t)): continue
    rows.append({'id': v['id'], 'q': vids[v['id']], 'title': t, 'channel': v['snippet']['channelTitle'], 'views': int(v['statistics'].get('viewCount', 0)),
                 'min': round(d / 60, 1), 'pub': v['snippet']['publishedAt'][:10]})
rows.sort(key=lambda r: -r['views'])
OURS = ['SCOI0DP-l-s', 'scV67BQvC4Q', '420buEFKB8k']
ours = [{'id': o['id'], 'title': o['snippet']['title'], 'views': int(o['statistics'].get('viewCount', 0))} for o in yt.videos().list(part='snippet,statistics', id=','.join(OURS)).execute()['items']]
def grab(i):
    p = os.path.join(H, 'src', i + '.jpg')
    if os.path.exists(p): return
    for n in ('maxresdefault', 'hqdefault'):
        try: open(p, 'wb').write(urllib.request.urlopen(f'https://i.ytimg.com/vi/{i}/{n}.jpg', timeout=30).read()); return
        except Exception: pass
for r in rows[:5] + ours: grab(r['id'])
json.dump({'after': AFTER, 'queries': Q, 'top': rows[:15], 'ours': ours}, open(os.path.join(H, 'compete_thumb.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in rows[:15]: print(f"{r['views']:>9,} | {r['pub']} | {r['min']:>5}분 | {r['channel'][:14]:14} | {r['id']} | {r['title'][:60]}")
print('ours', ours)
