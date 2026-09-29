"""매일 연구(유튜브 루프 0번) — 경쟁 채널 최근 영상 · 주제별 이번 주 조회 상위 · 우리 채널 성과를 유튜브 Data API(공식)로 모은다.
검색 호출은 하루 20회 이하(업로드 할당량을 남긴다). 채널 ID는 channels.json에 저장해 두고 다음부터는 검색하지 않는다.
실행: py -3.12 work/research/longform/loop/study.py [주제 검색어 …]  → study/YYYY-MM-DD.json
"""
import sys, os, re, json, datetime, statistics, zoneinfo
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import ytupload
yt = ytupload.service()
KST = zoneinfo.ZoneInfo('Asia/Seoul'); NOW = datetime.datetime.now(KST); TODAY = NOW.strftime('%Y-%m-%d')
OURS = 'UCV3ZcSho5Z1i8k_FAiKPlVg'
NAMES = ['수페TV', '소수몽키', '잼투리', '은퇴머니', '똑재TV', '싱글파이어', '절세미녀', '투자360']
TOPICS = sys.argv[1:] or ['커버드콜 ETF', '국민연금 수령 나이', '나스닥 레버리지 적립식']
searches = 0

def dur(s):
    m = re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or ''); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0) if m else 0

def videos(ids):
    out = []
    for i in range(0, len(ids), 50):
        out += yt.videos().list(part='snippet,statistics,contentDetails,status', id=','.join(ids[i:i+50])).execute()['items']
    return out

def row(v, subs=None):
    s = v['statistics']; views = int(s.get('viewCount', 0) or 0); pub = v['snippet']['publishedAt']
    age_h = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(pub.replace('Z', '+00:00'))).total_seconds() / 3600
    return {'id': v['id'], 'title': v['snippet']['title'], 'channel': v['snippet']['channelTitle'], 'pub': pub, 'age_h': round(age_h, 1),
            'sec': dur(v['contentDetails']['duration']), 'views': views, 'likes': int(s.get('likeCount', 0) or 0),
            'comments': int(s.get('commentCount', 0) or 0), 'subs': subs, 'ratio': round(views / subs, 2) if subs else None,
            'privacy': v.get('status', {}).get('privacyStatus')}

# 1) 경쟁 채널 ID(처음 한 번만 검색)
cpath = os.path.join(HERE, 'channels.json')
chans = json.load(open(cpath, encoding='utf-8')) if os.path.exists(cpath) else {}
for n in NAMES:
    if n in chans: continue
    r = yt.search().list(part='snippet', q=n, type='channel', regionCode='KR', maxResults=3).execute(); searches += 1
    it = r['items'][0] if r['items'] else None
    if it: chans[n] = {'id': it['snippet']['channelId'], 'title': it['snippet']['title'], 'found': TODAY,
                       'candidates': [x['snippet']['title'] for x in r['items']]}
json.dump(chans, open(cpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 2) 채널별 최근 업로드 10편(uploads 재생목록 — 검색 아님, 1단위)
res = {'date': TODAY, 'at': NOW.isoformat(timespec='minutes'), 'channels': {}, 'topics': {}, 'ours': []}
ids_all = [c['id'] for c in chans.values()] + [OURS]
cinfo = {}
for c in yt.channels().list(part='statistics,contentDetails,snippet', id=','.join(ids_all)).execute()['items']:
    cinfo[c['id']] = c
for n, c in list(chans.items()) + [('파이어맵', {'id': OURS})]:
    ci = cinfo.get(c['id'])
    if not ci: continue
    subs = int(ci['statistics'].get('subscriberCount', 0) or 0)
    up = ci['contentDetails']['relatedPlaylists']['uploads']
    n_items = 50 if n == '파이어맵' else 10
    pl = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=n_items).execute()['items']
    vs = [row(v, subs) for v in videos([p['contentDetails']['videoId'] for p in pl])]
    if n == '파이어맵':
        res['ours'] = vs; res['our_subs'] = subs; res['our_views'] = int(ci['statistics'].get('viewCount', 0) or 0)
    else:
        res['channels'][n] = {'title': ci['snippet']['title'], 'subs': subs, 'recent': vs}

# 3) 우리 주제 이번 주(7일) 조회 상위
since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
for q in TOPICS:
    if searches >= 20: break
    r = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko', publishedAfter=since,
                         order='viewCount', maxResults=15).execute(); searches += 1
    vs = videos([it['id']['videoId'] for it in r['items']])
    cids = list({v['snippet']['channelId'] for v in vs}); subs = {}
    for i in range(0, len(cids), 50):
        for c in yt.channels().list(part='statistics', id=','.join(cids[i:i+50])).execute()['items']:
            subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
    res['topics'][q] = sorted([row(v, subs.get(v['snippet']['channelId'])) for v in vs], key=lambda x: -x['views'])
res['searches'] = searches
os.makedirs(os.path.join(HERE, 'study'), exist_ok=True)
json.dump(res, open(os.path.join(HERE, 'study', TODAY + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 요약 출력
print('검색 호출', searches, '회 |', TODAY)
for n, c in res['channels'].items():
    rec = c['recent']; longs = [v for v in rec if v['sec'] >= 240]
    print(f"\n## {n} ({c['title']}) 구독 {c['subs']:,} | 최근 {len(rec)}편 중 긴 영상 {len(longs)} | 긴 영상 조회 중앙 {statistics.median([v['views'] for v in longs]) if longs else '-'}")
    for v in rec[:10]:
        print(f"  {v['pub'][:10]} {v['views']:>9,} {v['sec']//60:>3}:{v['sec']%60:02d} x{v['ratio']} | {v['title'][:60]}")
print(f"\n## 파이어맵 구독 {res.get('our_subs')} 총조회 {res.get('our_views')}")
for v in res['ours']:
    if v['privacy'] == 'public':
        print(f"  {v['pub'][:16]} {v['age_h']:>7}h {v['views']:>6,} 좋아요 {v['likes']} 댓글 {v['comments']} {v['sec']}s | {v['title'][:50]}")
for q, vs in res['topics'].items():
    print(f"\n## 이번 주 '{q}' 조회 상위")
    for v in vs[:8]:
        print(f"  {v['pub'][:10]} {v['views']:>9,} 구독 {v['subs'] or 0:>9,} x{v['ratio']} {v['sec']//60}:{v['sec']%60:02d} | {v['channel'][:10]} | {v['title'][:55]}")
