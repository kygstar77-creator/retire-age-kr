# 조회수 깔때기 다시 재기 — 성장 분석가 2026-10-17 (근거 research/growth/yt-funnel-1017.md·cafe-funnel-1017.md)
#   py -3.12 work/growthfunnel.py yt   [out.json]   # 유튜브: 롱폼 노출 첫 3일·클릭률·조회·시청 %·유입 경로 / 쇼츠→롱폼 연결 / 주별
#   py -3.12 work/growthfunnel.py cafe [out.json]   # 카페: 관리 통계(cafe.stat.naver.com) 유입 경로·글 조회 날짜별 + 주별 '1위 글 빼고' 조회
# 유튜브는 ytanalytics 읽기 토큰, 노출은 ytreach가 받아 둔 Reporting CSV(이틀 늦음). Analytics도 사흘쯤 늦다 → 최근 3일 편은 '집계 전'.
# 카페 통계는 발행 프로필(naverpost.launch, 매니저 로그인)로 읽기만 한다. 카페 글을 쓰거나 고치지 않는다.
import sys, os, json, glob, csv, collections, datetime, re, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
YDAY = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

def wk(d): d = datetime.date.fromisoformat(d[:10]); return (d - datetime.timedelta(days=d.weekday())).isoformat()

def yt(out):
    import ytanalytics as A
    from googleapiclient.discovery import build
    y = build('youtube', 'v3', credentials=A.creds()); an = build('youtubeAnalytics', 'v2', credentials=A.creds())
    def q(**kw):
        kw.setdefault('ids', 'channel==MINE'); kw.setdefault('startDate', '2026-09-01'); kw.setdefault('endDate', YDAY)
        for t in range(4):
            try: r = an.reports().query(**kw).execute(); break
            except Exception as e:
                if t == 3: print('실패', kw.get('filters'), str(e)[:80]); return []
                time.sleep(2 + 3 * t)   # 영상별 유입 경로는 가끔 500(backendError)
        h = [c['name'] for c in r.get('columnHeaders', [])]
        return [dict(zip(h, row)) for row in r.get('rows', [])]
    up = y.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    while True:
        r = y.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i['contentDetails']['videoId'] for i in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    vids = {}
    for k in range(0, len(ids), 50):
        for v in y.videos().list(part='snippet,contentDetails,status,statistics', id=','.join(ids[k:k + 50])).execute()['items']:
            m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', v['contentDetails']['duration'])
            sec = int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)
            if v['status']['privacyStatus'] != 'public' or v['snippet']['publishedAt'] < '2026-08-31T15': continue
            vids[v['id']] = dict(title=v['snippet']['title'], pub=v['snippet']['publishedAt'], sec=sec, views=int(v['statistics'].get('viewCount', 0)))
    for r in q(metrics='views,averageViewPercentage,subscribersGained', dimensions='video', sort='-views', maxResults=200):
        if r['video'] in vids: vids[r['video']]['an'] = r
    for vid, v in vids.items():
        if v.get('an', {}).get('views'): v['ts'] = {t['insightTrafficSourceType']: t['views'] for t in q(metrics='views', dimensions='insightTrafficSourceType', filters='video==' + vid)}
    imp = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
    for f in sorted(glob.glob(os.path.join(HERE, 'research', 'longform', 'loop', 'reach', '*.csv'))):
        for r in csv.DictReader(open(f, encoding='utf-8')):
            i = int(r.get('video_thumbnail_impressions') or 0); a = imp[r['video_id']][os.path.basename(f)[:10]]
            a[0] += i; a[1] += i * float(r.get('video_thumbnail_impressions_ctr') or 0)
    print('롱폼 | 공개 | 노출 첫3일 | 노출합 | 클릭률 | 조회 | 시청% | 탐색 | 검색 | 관련·쇼츠링크')
    for vid, v in sorted(vids.items(), key=lambda x: x[1]['pub']):
        if v['sec'] <= 180: continue
        d0 = datetime.date.fromisoformat(v['pub'][:10]); im = imp.get(vid, {})
        f3 = sum(im.get((d0 + datetime.timedelta(days=k)).isoformat(), [0, 0])[0] for k in range(3))
        I = sum(x[0] for x in im.values()); C = sum(x[1] for x in im.values()); ts = v.get('ts', {}); a = v.get('an', {})
        print(v['title'][:24], v['pub'][:10], f3, I, f'{C / I * 100 if I else 0:.1f}%', v['views'], f"{a.get('averageViewPercentage', 0):.0f}%",
              ts.get('SUBSCRIBER', 0), ts.get('YT_SEARCH', 0), ts.get('RELATED_VIDEO', 0) + ts.get('SHORTS_CONTENT_LINKS', 0))
    sh = [v for v in vids.values() if v['sec'] <= 180]
    print('쇼츠', len(sh), '편 · 주별 조회 중앙값', {w: sorted(x['views'] for x in sh if wk(x['pub']) == w)[len([x for x in sh if wk(x['pub']) == w]) // 2] for w in sorted({wk(x['pub']) for x in sh})})
    ch = q(metrics='views', dimensions='insightTrafficSourceType')
    print('채널 유입(9/1~):', {r['insightTrafficSourceType']: r['views'] for r in ch})
    W = collections.defaultdict(collections.Counter)
    for r in q(metrics='views,subscribersGained', dimensions='day,creatorContentType'):
        W[wk(r['day'])][r['creatorContentType']] += r['views']; W[wk(r['day'])]['구독+'] += r['subscribersGained']
    for vid, dd in imp.items():
        for d, (i, c) in dd.items():
            if d >= '2026-09-01': W[wk(d)]['노출'] += i
    for w in sorted(W): print('주', w, dict(W[w]))
    if out: json.dump(dict(vids=vids, imp={k: dict(v) for k, v in imp.items()}, ch=ch), open(out, 'w', encoding='utf-8'), ensure_ascii=False)

def cafe(out):
    from playwright.sync_api import sync_playwright
    from naverpost import launch
    B = 'https://cafe.stat.naver.com/api/cafe/31789001/'
    res = {}
    with sync_playwright() as p:
        ctx = launch(p, True)
        pg = ctx.new_page(); pg.goto('https://cafe.naver.com/ManageNaverStat.nhn?type=user&cafeId=31789001', timeout=40000); time.sleep(4)
        def get(path):
            r = ctx.request.get(B + path, headers={'Referer': 'https://cafe.naver.com/'}, timeout=30000)
            try: return {s['dataId']: s['data'] for s in r.json()['result']['statData']}
            except Exception: return {}
        d = datetime.date.today() - datetime.timedelta(days=28)
        while d < datetime.date.today():
            s = d.isoformat()
            res[s] = dict(ref=get(f'user/referer/total?service=CAFE&timeDimension=DATE&startDate={s}').get('referer', {}).get('rows', {}),
                          art=get(f'rank/articleCv?service=CAFE&timeDimension=DATE&startDate={s}').get('normal', {}).get('rows', {}))
            d += datetime.timedelta(days=1); time.sleep(0.4)
        ctx.close()
    W = collections.defaultdict(lambda: dict(art=collections.Counter(), ref=collections.Counter(), days=0))
    for s, x in res.items():
        w = W[wk(s)]; w['days'] += 1
        for u, c in zip(x['art'].get('uri', []), x['art'].get('cv', [])): w['art'][u.split('/')[-1]] += c
        for a, c in zip(x['ref'].get('referrerDomain', []), x['ref'].get('cv', [])): w['ref'][a] += c
    for k in sorted(W):
        w = W[k]; tot = sum(w['art'].values()); top3 = w['art'].most_common(3); rt = sum(w['ref'].values()) or 1
        srch = sum(c for a, c in w['ref'].items() if '검색' in a)
        print(k, f"{w['days']}일", '글 조회', tot, '상위3', top3, '나머지/일', round((tot - sum(c for _, c in top3)) / max(w['days'], 1)),
              '| 홈판', f"{w['ref']['네이버 메인_모바일_홈판'] / rt * 100:.0f}%", '검색 전체', f'{srch / rt * 100:.0f}%', '통합검색', f"{(w['ref']['네이버 통합검색_모바일'] + w['ref']['네이버 통합검색_PC']) / rt * 100:.1f}%")
    if out: json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    out = sys.argv[2] if len(sys.argv) > 2 else None
    yt(out) if cmd == 'yt' else cafe(out) if cmd == 'cafe' else print(open(__file__, encoding='utf-8').read().split('import')[0])
