# 작은 채널 아웃라이어 찾기(10/21, 노아 모리스 방법 적용) — 조회 ÷ 구독 배수
#   py -3.12 work/research/strategy/outlier-1021/scan.py search 시드1 시드2 ...  # 검색(100단위/회), 결과는 cache_search.json에 쌓임(이미 찾은 시드는 건너뜀)
#   py -3.12 work/research/strategy/outlier-1021/scan.py channels               # 검색 결과 + loop/outlier_channels.json 채널 구독·개설일
#   py -3.12 work/research/strategy/outlier-1021/scan.py videos                 # 구독 1만 미만 채널의 최근 업로드 50편 → 90일 안 영상 조회÷구독
#   py -3.12 work/research/strategy/outlier-1021/scan.py compete "구조 문구" ... # 경쟁 확인(구조 문구 검색, 90일·조회순 50편)
import sys, os, re, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import ytupload
yt = ytupload.service()
AFTER = '2026-07-23T00:00:00Z'   # 90일 전(10/21 기준)
OURS = 'UCV3ZcSho5Z1i8k_FAiKPlVg'
def P(n): return os.path.join(HERE, n)
def load(n, d): return json.load(open(P(n), encoding='utf-8')) if os.path.exists(P(n)) else d
def save(n, o): json.dump(o, open(P(n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    if not m: return 0
    a = [int(x or 0) for x in m.groups()]; return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]

def search(seeds, fname='cache_search.json'):
    c = load(fname, {})
    for q in seeds:
        if q in c: continue
        try:
            r = yt.search().list(part='snippet', q=q, type='video', regionCode='KR', relevanceLanguage='ko',
                                 publishedAfter=AFTER, order='viewCount', maxResults=50).execute()
        except Exception as e:
            print('검색 멈춤', q, str(e)[:120]); break
        c[q] = [dict(id=i['id']['videoId'], cid=i['snippet']['channelId'], ch=i['snippet']['channelTitle'],
                     title=i['snippet']['title'], pub=i['snippet']['publishedAt'][:10]) for i in r.get('items', [])]
        print(q, len(c[q])); save(fname, c)
    return c

def channels():
    c = load('cache_search.json', {}); ch = load('channels.json', {})
    ids = {v['cid'] for vs in c.values() for v in vs}
    pool = json.load(open(os.path.join(WORK, 'research', 'longform', 'loop', 'outlier_channels.json'), encoding='utf-8'))
    ids |= set(pool); ids.discard(OURS)
    todo = [i for i in ids if i not in ch]
    for i in range(0, len(todo), 50):
        for it in yt.channels().list(part='snippet,statistics,contentDetails', id=','.join(todo[i:i+50])).execute().get('items', []):
            s = it['statistics']
            ch[it['id']] = dict(title=it['snippet']['title'], opened=it['snippet']['publishedAt'][:10],
                                subs=None if s.get('hiddenSubscriberCount') else int(s.get('subscriberCount', 0)),
                                nvid=int(s.get('videoCount', 0)), views=int(s.get('viewCount', 0)),
                                uploads=it['contentDetails']['relatedPlaylists']['uploads'],
                                src='search' if it['id'] in {v['cid'] for vs in c.values() for v in vs} else 'pool')
    save('channels.json', ch); small = [k for k, v in ch.items() if v['subs'] is not None and v['subs'] < 10000]
    print('채널', len(ch), '구독 1만 미만', len(small))

def videos():
    ch = load('channels.json', {}); vd = load('videos.json', {})
    small = [k for k, v in ch.items() if v['subs'] is not None and v['subs'] < 10000 and k not in vd]
    for n, cid in enumerate(small):
        try:
            items = yt.playlistItems().list(part='contentDetails', playlistId=ch[cid]['uploads'], maxResults=50).execute().get('items', [])
        except Exception as e:
            vd[cid] = []; continue
        vids = [i['contentDetails']['videoId'] for i in items if (i['contentDetails'].get('videoPublishedAt') or '9') >= AFTER]
        rows = []
        if vids:
            for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(vids)).execute().get('items', []):
                rows.append(dict(id=v['id'], title=v['snippet']['title'], pub=v['snippet']['publishedAt'][:10],
                                 sec=sec(v['contentDetails'].get('duration')), views=int(v['statistics'].get('viewCount', 0)),
                                 likes=int(v['statistics'].get('likeCount', 0) or 0), comments=int(v['statistics'].get('commentCount', 0) or 0)))
        vd[cid] = rows
        if n % 20 == 0: save('videos.json', vd); print(n, len(small))
    save('videos.json', vd); print('끝', len(vd))

def compete(phrases):
    search(phrases, 'cache_compete.json')
    c = load('cache_compete.json', {}); cc = load('compete_channels.json', {})
    vids = {v['id'] for p in phrases for v in c.get(p, [])}; vids = list(vids)
    st = load('compete_videos.json', {})
    todo = [v for v in vids if v not in st]
    for i in range(0, len(todo), 50):
        for v in yt.videos().list(part='statistics,contentDetails', id=','.join(todo[i:i+50])).execute().get('items', []):
            st[v['id']] = dict(views=int(v['statistics'].get('viewCount', 0)), sec=sec(v['contentDetails'].get('duration')))
    save('compete_videos.json', st)
    cids = list({v['cid'] for p in phrases for v in c.get(p, [])} - set(cc))
    for i in range(0, len(cids), 50):
        for it in yt.channels().list(part='snippet,statistics', id=','.join(cids[i:i+50])).execute().get('items', []):
            s = it['statistics']; cc[it['id']] = dict(title=it['snippet']['title'], opened=it['snippet']['publishedAt'][:10],
                                                     subs=None if s.get('hiddenSubscriberCount') else int(s.get('subscriberCount', 0)))
    save('compete_channels.json', cc)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'search': search(sys.argv[2:])
    elif cmd == 'channels': channels()
    elif cmd == 'videos': videos()
    elif cmd == 'compete': compete(sys.argv[2:])
