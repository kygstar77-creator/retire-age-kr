"""긴 영상 경쟁 조사 — 유튜브 Data API(공식)로 주제별 조회순 긴 영상을 모으고 채널 대비 성과를 잰다(2026-09-29)."""
import sys, os, re, json, datetime, statistics
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ytupload
yt = ytupload.service()
Q = sys.argv[1:] or ['배당주 비교','미국 배당 ETF 비교','배당 ETF 분석','아파트 실거래가 분석','부동산 손품','단지 분석 실거래','종목 분석 배당','커버드콜 ETF 비교','연금저축 ETF','국민연금 수령액']
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
vids = {}
for q in Q:
    for d in ('medium', 'long'):
        r = yt.search().list(part='snippet', q=q, type='video', videoDuration=d, regionCode='KR', relevanceLanguage='ko',
                             publishedAfter='2026-05-01T00:00:00Z', order='viewCount', maxResults=15).execute()
        for it in r['items']: vids.setdefault(it['id']['videoId'], q)
ids = list(vids); info = []
for i in range(0, len(ids), 50):
    info += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
chs = {v['snippet']['channelId'] for v in info}; subs = {}
chs = list(chs)
for i in range(0, len(chs), 50):
    for c in yt.channels().list(part='statistics,snippet', id=','.join(chs[i:i+50])).execute()['items']:
        subs[c['id']] = (int(c['statistics'].get('subscriberCount', 0) or 0), c['snippet']['title'])
rows = []
for v in info:
    s = v['statistics']; cid = v['snippet']['channelId']; sb, ct = subs.get(cid, (0, '?'))
    views = int(s.get('viewCount', 0)); d = dur(v['contentDetails']['duration'])
    if d < 240: continue
    rows.append({'id': v['id'], 'q': vids[v['id']], 'title': v['snippet']['title'], 'channel': ct, 'subs': sb, 'views': views,
                 'ratio': round(views / sb, 2) if sb else None, 'min': round(d / 60, 1), 'pub': v['snippet']['publishedAt'][:10],
                 'likes': int(s.get('likeCount', 0) or 0), 'comments': int(s.get('commentCount', 0) or 0)})
rows.sort(key=lambda r: -(r['ratio'] or 0))
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'longform', 'compete.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('영상', len(rows), '| 길이 중앙', statistics.median(r['min'] for r in rows), '분')
for r in rows[:40]:
    print(f"{r['ratio']:>6} 배 | 조회 {r['views']:>8,} | 구독 {r['subs']:>9,} | {r['min']:>5}분 | {r['channel'][:12]:12} | {r['title'][:48]}")
