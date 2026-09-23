# 다른 유튜버의 '시리즈'를 찾는다 — 사장님 2026-09-24
#   "수페TV 따라한 시리즈가 좋네. 다른 유튜버의 시리즈도 찾아봐. 구성이 좋아 보이는 걸로,
#    구독자도 많고 조회수도 많고 댓글 반응도 좋은 걸로."
#
#   py -3.12 work/ytseries.py                 → 기본 검색어로 채널을 찾아 시리즈를 뽑는다
#   py -3.12 work/ytseries.py "배당" "부동산"  → 검색어 직접 지정
#
# 시리즈를 어떻게 알아보나: 제목 앞머리가 반복되면 시리즈다.
#   "[9월 3주차] …", "매일 미국증시 …", "○○ 분석 #12" 처럼 같은 틀이 여러 편 있는 것.
# 무엇으로 고르나: 구독자 수 · 그 시리즈 편들의 조회수 중앙값 · 댓글 수 중앙값.
# 남의 영상을 베끼지 않는다. 어떤 '틀'이 반복되고 반응이 좋은지만 본다.
import sys, os, re, json, time, collections, statistics
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'research', 'yt')

QUERIES = ['미국주식', '배당주 투자', '부동산 투자', '경제 뉴스 정리', '재테크', 'ETF 투자']

def service():
    import ytupload
    return ytupload.service() if hasattr(ytupload, 'service') else None

def api(yt, what, **kw):
    return getattr(yt, what)().list(**kw).execute()

def find_channels(yt, q, n=8):
    r = api(yt, 'search', part='snippet', q=q, type='channel', maxResults=n, regionCode='KR', relevanceLanguage='ko')
    return [(i['snippet']['channelId'], i['snippet']['title']) for i in r.get('items', [])]

def channel_stats(yt, ids):
    out = {}
    for i in range(0, len(ids), 50):
        r = api(yt, 'channels', part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50]))
        for c in r.get('items', []):
            s = c.get('statistics', {})
            out[c['id']] = {'name': c['snippet']['title'], '구독자': int(s.get('subscriberCount') or 0),
                            '영상수': int(s.get('videoCount') or 0), '총조회': int(s.get('viewCount') or 0),
                            'uploads': c['contentDetails']['relatedPlaylists']['uploads']}
    return out

def recent_videos(yt, uploads, n=50):
    ids, tok = [], None
    while len(ids) < n:
        r = api(yt, 'playlistItems', part='contentDetails', playlistId=uploads, maxResults=min(50, n - len(ids)), pageToken=tok)
        ids += [x['contentDetails']['videoId'] for x in r.get('items', [])]
        tok = r.get('nextPageToken')
        if not tok: break
    out = []
    for i in range(0, len(ids), 50):
        r = api(yt, 'videos', part='snippet,statistics', id=','.join(ids[i:i + 50]))
        for v in r.get('items', []):
            s = v.get('statistics', {})
            out.append({'title': v['snippet']['title'], 'date': v['snippet']['publishedAt'][:10],
                        'views': int(s.get('viewCount') or 0), 'comments': int(s.get('commentCount') or 0),
                        'likes': int(s.get('likeCount') or 0)})
    return out

def head_key(t):
    """제목 앞머리로 시리즈를 묶는다. 대괄호 머리말, 또는 앞 두 어절."""
    t = t.strip()
    m = re.match(r'^[\[【]([^\]】]{2,20})[\]】]', t)
    if m: return re.sub(r'\d+', 'N', m.group(1)).strip()
    words = re.sub(r'\d+', 'N', t).split()
    return ' '.join(words[:2])[:20] if len(words) >= 2 else ''

def series_of(vids, min_ep=3):
    g = collections.defaultdict(list)
    for v in vids:
        k = head_key(v['title'])
        if len(k) >= 2: g[k].append(v)
    out = []
    for k, vs in g.items():
        if len(vs) < min_ep: continue
        out.append({'틀': k, '편수': len(vs),
                    '조회중앙': int(statistics.median(v['views'] for v in vs)),
                    '댓글중앙': int(statistics.median(v['comments'] for v in vs)),
                    '예': sorted(vs, key=lambda v: -v['views'])[0]['title'][:60]})
    return sorted(out, key=lambda x: -x['조회중앙'])

def main():
    qs = [a for a in sys.argv[1:] if not a.startswith('--')] or QUERIES
    yt = service()
    if yt is None: print('유튜브 인증 실패 — py -3.12 work/ytupload.py auth'); return
    found = {}
    for q in qs:
        try:
            for cid, nm in find_channels(yt, q): found[cid] = nm
        except Exception as e: print(f'{q} 검색 실패 {str(e)[:70]}')
        time.sleep(0.3)
    print(f'검색어 {len(qs)}개에서 채널 {len(found)}곳')
    stats = channel_stats(yt, list(found))
    # 구독자 5만 이상만 본다(반응 표본이 있어야 판단이 된다)
    big = sorted([c for c in stats.values() if c['구독자'] >= 50000], key=lambda c: -c['구독자'])[:12]
    print(f'구독자 5만 이상 {len(big)}곳\n')
    rows = []
    for c in big:
        try: vids = recent_videos(yt, c['uploads'], 50)
        except Exception as e: print(f"  {c['name']} 영상 실패 {str(e)[:50]}"); continue
        for s in series_of(vids)[:3]:
            s['채널'] = c['name']; s['구독자'] = c['구독자']; rows.append(s)
        time.sleep(0.3)
    rows.sort(key=lambda r: -r['조회중앙'])
    L = [f'# 다른 유튜버의 시리즈 (ytseries, {time.strftime("%Y-%m-%d")})', '',
         '제목 앞머리가 3편 이상 반복되는 것을 시리즈로 봤다. 구독자 5만 이상 채널만.',
         '베끼려는 게 아니라 어떤 틀이 반복되고 반응이 좋은지 보려는 것이다.', '',
         '| 채널 | 구독자 | 반복되는 틀 | 편수 | 조회 중앙 | 댓글 중앙 | 가장 많이 본 편 |',
         '|---|---|---|---|---|---|---|']
    for r in rows[:30]:
        L.append(f"| {r['채널']} | {r['구독자']:,} | {r['틀']} | {r['편수']} | {r['조회중앙']:,} | {r['댓글중앙']:,} | {r['예']} |")
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f'series_{time.strftime("%Y-%m-%d")}.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    for r in rows[:12]:
        print(f"  {r['채널'][:14]:16}{r['구독자']:>9,}명 · {r['틀'][:18]:20} {r['편수']:2}편 · 조회 {r['조회중앙']:>8,} · 댓글 {r['댓글중앙']:>4,}")
    print('\n저장', p)

if __name__ == '__main__': main()
