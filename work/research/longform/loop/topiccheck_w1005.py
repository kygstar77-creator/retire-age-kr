"""시리즈 주제 검증(research-kr 2026-10-02) — 주제별 검색어로 최근 90일 긴 영상을 모으고,
영상마다 '그 채널 최근 업로드 30개 조회 중앙값 대비 몇 배'를 잰다(구독 대비 아님). 3배 이상 = 아웃라이어.
비용: 검색 1회 100단위, 채널 업로드 목록·영상 정보는 1단위. 사용: python topiccheck.py"""
import sys, os, re, json, statistics, datetime
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, W); import ytupload
yt = ytupload.service()
TOPICS = {
 '금 사는 방법·세금': ['금 투자 방법 세금', '금 ETF KRX 금현물'],
 '월배당·커버드콜 ETF': ['월배당 ETF 1억', '커버드콜 ETF 배당'],
}
after = (datetime.date.today() - datetime.timedelta(days=90)).isoformat() + 'T00:00:00Z'
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
def vinfo(ids):
    out = []
    for i in range(0, len(ids), 50):
        out += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
    return out
med_cache = {}
def chan_median(cid):
    if cid in med_cache: return med_cache[cid]
    up = 'UU' + cid[2:]
    try:
        items = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=30).execute()['items']
        vs = vinfo([x['contentDetails']['videoId'] for x in items])
        views = [int(v['statistics'].get('viewCount', 0)) for v in vs if dur(v['contentDetails']['duration']) >= 240]
        med_cache[cid] = (statistics.median(views), len(views)) if len(views) >= 5 else (None, len(views))
    except Exception as e:
        med_cache[cid] = (None, 0)
    return med_cache[cid]
res = {}
for t, qs in TOPICS.items():
    ids = []
    for q in qs:
        r = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko',
                             publishedAfter=after, order='viewCount', maxResults=15).execute()
        ids += [it['id']['videoId'] for it in r['items'] if it['id']['videoId'] not in ids]
    rows = []
    for v in vinfo(ids):
        if dur(v['contentDetails']['duration']) < 240: continue
        views = int(v['statistics'].get('viewCount', 0)); med, n = chan_median(v['snippet']['channelId'])
        rows.append({'id': v['id'], 'title': v['snippet']['title'], 'ch': v['snippet']['channelTitle'], 'views': views,
                     'med': med, 'n': n, 'x': round(views / med, 1) if med else None, 'pub': v['snippet']['publishedAt'][:10],
                     'min': round(dur(v['contentDetails']['duration']) / 60, 1)})
    rows.sort(key=lambda r: -(r['x'] or 0)); res[t] = rows
    out = [r for r in rows if (r['x'] or 0) >= 3]
    print(f'\n## {t} | 검색어 {qs} | 긴 영상 {len(rows)}개 | 3배 이상 {len(out)}개')
    for r in rows[:8]:
        print(f"{r['x']}배 | 조회 {r['views']:,} / 채널중앙 {r['med']} | {r['min']}분 | {r['pub']} | {r['ch'][:12]} | {r['title'][:50]}")
json.dump(res, open(os.path.join(os.path.dirname(__file__), 'topiccheck_2026-10-05.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
