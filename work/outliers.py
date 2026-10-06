# 경쟁 '아웃라이어' 매일 찾기 — 채널 '자기 평소' 대비 몇 배 터졌나 (사장님 10/02 07:29, today.md [지시])
#   py -3.12 work/outliers.py            # 채널 목록 갱신 + 최근 30일 3배 이상 → research/longform/loop/outliers.md 맨 위
#   py -3.12 work/outliers.py --max 40   # 채널 수 상한(기본 50 = 고정 35 + 새로 찾은 15)
#   py -3.12 work/outliers.py --discover # 먼저 돈 영역 8개 검색(최근 7일 조회순)으로 새 채널을 더한다(search 8회 = 800단위, 하루 1번)
# 고정 목록만 보면 새로 뜬 채널을 못 본다(topics.md 10/6·10/7 '한계'). 그래서 상한 중 FRESH칸은 최근 28일 안에 새로 찾은 채널을
# 덜 본 순으로 돌려 본다. 새 채널이 28일 동안 아웃라이어를 한 번도 못 내면 FRESH칸에서 빠진다(RULES: 4주 상위에 안 뜬 채널은 뺀다).
# 구독 대비가 아니라 그 채널 최근 업로드(같은 형식: 쇼츠≤180초 / 롱폼)의 조회 중앙값 대비로 본다 — 채널 크기 착시 제거.
# 검색(search.list, 100단위)은 쓰지 않는다: 채널은 이미 받아 둔 연구 파일(study·topiccheck·channels.json)의 영상에서 모은다.
# 비용: 채널당 약 3단위(channels·playlistItems·videos) → 35채널 ≈ 110단위. 업로드 할당량을 남긴다.
import sys, os, re, json, glob, datetime, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
LOOP = os.path.join(HERE, 'research', 'longform', 'loop')
CH_FILE = os.path.join(LOOP, 'outlier_channels.json'); MD = os.path.join(LOOP, 'outliers.md')
KST = datetime.timezone(datetime.timedelta(hours=9)); NOW = datetime.datetime.now(KST)
MIN_X, MIN_VIEWS, DAYS = 3.0, 1000, 30
FRESH, KEEP_DAYS = 15, 28
AREAS = ['주식 투자', '성장주', '배당주 배당금', 'ETF 추천 비교', '부동산 아파트', '경제 금리 환율', '세금 절세', '국민연금 노후']
OURS = 'UCV3ZcSho5Z1i8k_FAiKPlVg'

def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or ''); a = [int(x or 0) for x in m.groups()]
    return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]

def seed_video_ids():
    ids = collections.Counter()
    for f in glob.glob(os.path.join(LOOP, 'study', '*.json')) + glob.glob(os.path.join(LOOP, 'topiccheck_*.json')):
        try: s = open(f, encoding='utf-8').read()
        except Exception: continue
        for m in re.finditer(r'"id":\s*"([A-Za-z0-9_-]{11})"', s): ids[m.group(1)] += 1
    return ids

def channels(yt, cap):
    known = json.load(open(CH_FILE, encoding='utf-8')) if os.path.exists(CH_FILE) else {}
    try:
        for name, c in json.load(open(os.path.join(LOOP, 'channels.json'), encoding='utf-8')).items():
            known.setdefault(c['id'], dict(title=c.get('title', name), hits=0, found=c.get('found')))
    except Exception: pass
    vids = list(seed_video_ids())
    for i in range(0, len(vids), 50):
        for v in yt.videos().list(part='snippet', id=','.join(vids[i:i+50])).execute().get('items', []):
            cid = v['snippet']['channelId']
            if cid == OURS: continue
            k = known.setdefault(cid, dict(title=v['snippet']['channelTitle'], hits=0, found=NOW.date().isoformat()))
            k['hits'] = k.get('hits', 0) + 1
    json.dump(known, open(CH_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    core = sorted(known.items(), key=lambda x: -x[1].get('hits', 0))[:cap - FRESH]
    have = {cid for cid, _ in core}
    def alive(k):  # 새로 찾은 지 28일 안이거나, 최근 28일 안에 아웃라이어를 낸 채널
        d = k.get('last_out') or k.get('found') or '2000-01-01'
        return (NOW.date() - datetime.date.fromisoformat(d)).days <= KEEP_DAYS
    fresh = [(cid, k) for cid, k in known.items() if cid not in have and k.get('src', '').startswith('search') and alive(k)]
    fresh.sort(key=lambda x: x[1].get('scanned') or '')  # 덜 본 순
    return core + fresh[:FRESH]

def discover(yt):
    known = json.load(open(CH_FILE, encoding='utf-8')) if os.path.exists(CH_FILE) else {}
    after = (NOW - datetime.timedelta(days=7)).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    new = []
    for q in AREAS:
        try:
            items = yt.search().list(part='snippet', q=q, type='video', order='viewCount', publishedAfter=after,
                                     regionCode='KR', relevanceLanguage='ko', maxResults=25).execute().get('items', [])
        except Exception as e:
            print('검색 멈춤', q, str(e)[:80]); break
        for it in items:
            cid = it['snippet']['channelId']
            if cid == OURS: continue
            if cid not in known:
                known[cid] = dict(title=it['snippet']['channelTitle'], hits=0, found=NOW.date().isoformat(), src='search:' + q)
                new.append((q, it['snippet']['channelTitle']))
    json.dump(known, open(CH_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return new

def mark(chs, out):
    known = json.load(open(CH_FILE, encoding='utf-8'))
    hit = {r['cid'] for r in out}
    for cid, _ in chs:
        if cid in known:
            known[cid]['scanned'] = NOW.date().isoformat()
            if cid in hit: known[cid]['last_out'] = NOW.date().isoformat()
    json.dump(known, open(CH_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def scan(yt, chs):
    out, info = [], {}
    for i in range(0, len(chs), 50):
        for c in yt.channels().list(part='contentDetails,statistics', id=','.join(cid for cid, _ in chs[i:i+50])).execute().get('items', []):
            info[c['id']] = (c['contentDetails']['relatedPlaylists']['uploads'], int(c['statistics'].get('subscriberCount', 0) or 0))
    for cid, meta in chs:
        if cid not in info: continue
        up, subs = info[cid]
        try: items = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute().get('items', [])
        except Exception as e: print('건너뜀', meta['title'], str(e)[:80]); continue
        vs = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(x['contentDetails']['videoId'] for x in items)).execute().get('items', [])
        rows = []
        for v in vs:
            pub = datetime.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00')).astimezone(KST)
            s = sec(v['contentDetails'].get('duration'))
            rows.append(dict(id=v['id'], cid=cid, title=v['snippet']['title'], ch=meta['title'], subs=subs, pub=pub, sec=s,
                             form='쇼츠' if s <= 180 else '롱폼', views=int(v['statistics'].get('viewCount', 0)),
                             thumb=f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"))
        for form in ('쇼츠', '롱폼'):
            same = [r for r in rows if r['form'] == form and (NOW - r['pub']).days >= 2]  # 막 올라온 건 중앙값에서 뺀다
            if len(same) < 5: continue
            med = statistics.median(r['views'] for r in same)
            for r in rows:
                age = (NOW - r['pub']).days
                if r['form'] != form or age > DAYS or med <= 0: continue
                x = r['views'] / med
                if x >= MIN_X and r['views'] >= MIN_VIEWS: out.append(dict(r, med=med, x=round(x, 1), age=age))
    return out

def write(out, nch):
    from contentreview import topic
    out.sort(key=lambda r: -r['x'])
    wd = '월화수목금토일'
    lines = [f"## {NOW:%Y-%m-%d %H:%M} — 채널 {nch}곳, 최근 {DAYS}일 '자기 평소(같은 형식 최근 50편 중앙값)' {MIN_X:g}배 이상·{MIN_VIEWS:,}회 이상 {len(out)}편",
             '| 배수 | 조회 | 채널 평소 | 형식·길이 | 올린 요일·시각 | 주제(자동) | 채널 | 제목 |', '|---|---|---|---|---|---|---|---|']
    for r in out[:40]:
        ln = f"{r['sec']//60}분" if r['form'] == '롱폼' else f"{r['sec']}초"
        lines.append(f"| {r['x']} | {r['views']:,} | {r['med']:,.0f} | {r['form']} {ln} | {wd[r['pub'].weekday()]} {r['pub']:%H}시 | {topic(r['title'])} | {r['ch']} | [{r['title'][:45]}](https://youtu.be/{r['id']}) |")
    by = collections.Counter(topic(r['title']) for r in out); fm = collections.Counter(r['form'] for r in out)
    lines += ['', f"- 주제별: {', '.join(f'{k} {v}' for k, v in by.most_common())} · 형식: {', '.join(f'{k} {v}' for k, v in fm.items())}",
              '- 주제는 제목 키워드 자동 분류(contentreview.py). 작은 채널(평소 수백 회)은 배수가 쉽게 커진다 — 평소 칸을 같이 본다. 썸네일은 링크로만 보고 내려받지 않는다.', '']
    old = open(MD, encoding='utf-8').read() if os.path.exists(MD) else '# outliers.md — 경쟁 아웃라이어 매일 (work/outliers.py, 최신이 위)\n\n'
    head, _, rest = old.partition('\n\n')
    open(MD, 'w', encoding='utf-8').write(head + '\n\n' + '\n'.join(lines) + '\n' + rest)
    json.dump([dict(r, pub=r['pub'].isoformat()) for r in out], open(os.path.join(LOOP, 'outliers_latest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

if __name__ == '__main__':
    cap = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 50  # 고정 35 + 새로 찾은 15
    import ytupload; yt = ytupload.service()
    if '--discover' in sys.argv:
        new = discover(yt); print(f'새 채널 {len(new)}곳:', ' · '.join(f'{t}({q})' for q, t in new[:40]))
    chs = channels(yt, cap); out = scan(yt, chs); write(out, len(chs)); mark(chs, out)
    nf = sum(1 for _, k in chs if k.get('src', '').startswith('search'))
    print(f'채널 {len(chs)}(새로 찾은 채널 {nf}) · 아웃라이어 {len(out)}편 → {MD}')
