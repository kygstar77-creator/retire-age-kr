# 돈 밖 장르 아웃라이어 넓게 재기(10/22). 기준은 10/21 scan.py와 같다: 조회÷구독 ≥10, 조회 3,000+, 구독 1만 미만, 90일.
# 다른 점 하나: 시드 검색은 Data API search.list(100단위/회) 대신 유튜브 검색 화면(로그인 없음, 0단위)으로 받는다.
#   이유: 오늘 H-3 업로드(videos.insert)가 같은 할당량을 쓴다. 검색 화면 3가지 정렬(올해·조회순 / 이번 달·조회순 / 올해·관련도) 첫 화면을 합치고 90일 안만 남긴다.
#   나머지(videos/channels/playlistItems.list)는 Data API 1단위짜리라 10/21과 같다.
#   py -3.12 scan1022.py search      # seeds1022.json의 시드 → cache_web.json
#   py -3.12 scan1022.py meta        # 검색에 나온 영상·채널 숫자 → seedvids.json · channels.json
#   py -3.12 scan1022.py videos      # 구독 1만 미만 채널 최근 50편 중 90일 안 → videos.json (10/21에 받은 채널은 그 값을 재사용)
import sys, os, re, json, urllib.parse, subprocess, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..')); sys.path.insert(0, WORK)
O = os.path.join(H, '..', 'outlier-1021')
AFTER = '2026-07-24'   # 90일 전(10/22 기준)
OURS = 'UCV3ZcSho5Z1i8k_FAiKPlVg'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
SP = ['CAMSAggF', 'CAMSAggE', 'EgIIBQ%3D%3D']
def P(n): return os.path.join(H, n)
def load(p, d): return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else d
def save(n, o): json.dump(o, open(P(n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    if not m: return 0
    a = [int(x or 0) for x in m.groups()]; return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]
UNITS = [0]
def ex(req):
    UNITS[0] += 1
    return req.execute()

def search():
    seeds = load(P('seeds1022.json'), {}); c = load(P('cache_web.json'), {})
    for g, qs in seeds.items():
        for q in qs:
            if q in c: continue
            ids = []
            for sp in SP:
                url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(q) + '&sp=' + sp + '&hl=ko&gl=KR'
                h = subprocess.run(['curl', '-s', '-A', UA, '-H', 'Accept-Language: ko-KR', url], capture_output=True).stdout.decode('utf-8', 'ignore')
                for i in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', h):
                    if i not in ids: ids.append(i)
                time.sleep(0.5)
            c[q] = dict(genre=g, ids=ids); print(g, q, len(ids)); save('cache_web.json', c)

def meta():
    import ytupload; yt = ytupload.service()
    c = load(P('cache_web.json'), {}); sv = load(P('seedvids.json'), {})
    ids = list({i for v in c.values() for i in v['ids']} - set(sv))
    for i in range(0, len(ids), 50):
        for v in ex(yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50]))).get('items', []):
            sv[v['id']] = dict(cid=v['snippet']['channelId'], ch=v['snippet']['channelTitle'], title=v['snippet']['title'], pub=v['snippet']['publishedAt'][:10],
                               sec=sec(v['contentDetails'].get('duration')), views=int(v['statistics'].get('viewCount', 0)))
    save('seedvids.json', sv)
    ch = load(P('channels.json'), {}); old = load(os.path.join(O, 'channels.json'), {})
    cids = {v['cid'] for v in sv.values() if v['pub'] >= AFTER} - {OURS}
    todo = [x for x in cids if x not in ch]
    for x in list(todo):
        if x in old: ch[x] = dict(old[x], src='1021'); todo.remove(x)
    for i in range(0, len(todo), 50):
        for it in ex(yt.channels().list(part='snippet,statistics,contentDetails', id=','.join(todo[i:i+50]))).get('items', []):
            s = it['statistics']
            ch[it['id']] = dict(title=it['snippet']['title'], opened=it['snippet']['publishedAt'][:10],
                                subs=None if s.get('hiddenSubscriberCount') else int(s.get('subscriberCount', 0)),
                                nvid=int(s.get('videoCount', 0)), views=int(s.get('viewCount', 0)),
                                uploads=it['contentDetails']['relatedPlaylists']['uploads'], src='1022')
    save('channels.json', ch)
    small = [k for k, v in ch.items() if v['subs'] is not None and v['subs'] < 10000]
    print('영상', len(sv), '채널', len(ch), '구독 1만 미만', len(small), '| API 단위', UNITS[0])

def videos():
    import ytupload; yt = ytupload.service()
    ch = load(P('channels.json'), {}); vd = load(P('videos.json'), {}); oldv = load(os.path.join(O, 'videos.json'), {})
    small = [k for k, v in ch.items() if v['subs'] is not None and v['subs'] < 10000 and k not in vd]
    for n, cid in enumerate(small):
        if cid in oldv:
            vd[cid] = [v for v in oldv[cid] if v['pub'] >= AFTER]; continue
        try:
            items = ex(yt.playlistItems().list(part='contentDetails', playlistId=ch[cid]['uploads'], maxResults=50)).get('items', [])
        except Exception as e:
            s = str(e)
            if 'quota' in s.lower(): print('할당량 멈춤', n, len(small)); save('videos.json', vd); return
            vd[cid] = []; continue
        vids = [i['contentDetails']['videoId'] for i in items if (i['contentDetails'].get('videoPublishedAt') or '9')[:10] >= AFTER]
        rows = []
        if vids:
            try:
                its = ex(yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(vids))).get('items', [])
            except Exception as e:
                if 'quota' in str(e).lower(): print('할당량 멈춤', n, len(small)); save('videos.json', vd); return
                its = []
            for v in its:
                rows.append(dict(id=v['id'], title=v['snippet']['title'], pub=v['snippet']['publishedAt'][:10],
                                 sec=sec(v['contentDetails'].get('duration')), views=int(v['statistics'].get('viewCount', 0)),
                                 likes=int(v['statistics'].get('likeCount', 0) or 0), comments=int(v['statistics'].get('commentCount', 0) or 0),
                                 desc=v['snippet'].get('description', '')[:300]))
        vd[cid] = rows
        if n % 25 == 0: save('videos.json', vd); print(n, len(small), 'API 단위', UNITS[0])
    save('videos.json', vd); print('끝', len(vd), 'API 단위', UNITS[0])

if __name__ == '__main__':
    dict(search=search, meta=meta, videos=videos)[sys.argv[1]]()
