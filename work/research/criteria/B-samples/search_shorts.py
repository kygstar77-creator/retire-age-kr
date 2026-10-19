# 돈 분야 쇼츠 조회 상위(최근 30일, KR, 4분 미만) — search.list 6회(600단위). 결과 search_shorts.json
import sys, os, re, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
import ytupload
yt = ytupload.service()
after = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
Q = ['재테크', '주식', '부동산 아파트', '연금 노후', 'ETF 배당', '경제 환율 금리']
ids = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q + ' #shorts', type='video', videoDuration='short', order='viewCount', publishedAfter=after,
                         regionCode='KR', relevanceLanguage='ko', maxResults=50).execute()['items']
    for x in r: ids.setdefault(x['id']['videoId'], q)
vids = list(ids); rows = []
for i in range(0, len(vids), 50):
    for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(vids[i:i+50])).execute()['items']:
        rows.append(dict(id=v['id'], ch=v['snippet']['channelTitle'], cid=v['snippet']['channelId'], title=v['snippet']['title'], q=ids[v['id']],
                         published=v['snippet']['publishedAt'][:10], views=int(v['statistics'].get('viewCount', 0)), dur=v['contentDetails']['duration']))
cids = list({r['cid'] for r in rows}); subs = {}
for i in range(0, len(cids), 50):
    for c in yt.channels().list(part='statistics', id=','.join(cids[i:i+50])).execute()['items']:
        subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
for r in rows: r['subs'] = subs.get(r['cid'], 0); r['ratio'] = round(r['views'] / max(r['subs'], 1), 2)
rows.sort(key=lambda r: -r['views'])
json.dump(rows, open(os.path.join(HERE, 'search_shorts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for r in rows[:80]: print(r['views'], r['subs'], r['ratio'], r['ch'], '|', r['title'][:50], r['id'], r['dur'])
