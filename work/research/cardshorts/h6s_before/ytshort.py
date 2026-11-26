# h6s_before 11/26 PD: k1s_recover/ytshort.py 사본, 검색어만 은마·재건축 실거래
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytupload
yt = ytupload.service()
Q = ['은마아파트','은마 실거래가','은마아파트 시세','재건축 아파트 실거래가','강남 재건축 하락','대치동 아파트 실거래']
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
vids = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q, type='video', videoDuration='short', regionCode='KR', relevanceLanguage='ko', publishedAfter='2026-10-27T00:00:00Z', order='viewCount', maxResults=15).execute()
    for it in r['items']: vids.setdefault(it['id']['videoId'], q)
ids = list(vids); info = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[:50])).execute()['items']
chs = list({v['snippet']['channelId'] for v in info}); subs = {}
for c in yt.channels().list(part='statistics,snippet', id=','.join(chs[:50])).execute()['items']:
    subs[c['id']] = (int(c['statistics'].get('subscriberCount', 0) or 0), c['snippet']['title'])
rows = []
for v in info:
    sb, ct = subs.get(v['snippet']['channelId'], (0, '?')); views = int(v['statistics'].get('viewCount', 0))
    rows.append({'id': v['id'], 'q': vids[v['id']], 'title': v['snippet']['title'], 'channel': ct, 'subs': sb, 'views': views, 'ratio': round(views/sb,2) if sb else None, 'sec': dur(v['contentDetails']['duration']), 'pub': v['snippet']['publishedAt'][:10]})
rows.sort(key=lambda r: -r['views'])
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in rows[:14]: print(r['id'], r['views'], r['ratio'], r['sec'], r['pub'], r['channel'], '|', r['title'])
