# npsday1007 경쟁 쇼츠 검색
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytupload
yt = ytupload.service()
Q = ['국민연금 수령나이','국민연금 65세 69년생','국민연금 출생연도 수령 개시','노령연금 지급개시연령','국민연금 언제부터 받나']
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
vids = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q, type='video', videoDuration='short', regionCode='KR', relevanceLanguage='ko', publishedAfter='2026-09-06T00:00:00Z', order='viewCount', maxResults=15).execute()
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
