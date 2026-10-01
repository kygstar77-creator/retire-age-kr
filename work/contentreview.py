# 콘텐츠 회고 표 — 유튜브 공개 영상·카페 글을 주제·형식(뉴스 정리형 vs 내 돈 얼마형)으로 줄 세운다.
#   py -3.12 work/contentreview.py            # 받아서 research/content-review/<날짜>_tables.md
# 매주 일요일 콘텐츠 회고(today.md [지시·긴급] 4번)가 이 표를 다시 만든다. 분류는 제목 키워드 자동 — 경향만 본다.
import sys, os, re, json, datetime, statistics, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'research', 'content-review')
TODAY = datetime.date.today().isoformat()

TOPIC = [('주식·ETF', r'(ETF|SCHD|JEPQ|QQQM|SPYI|SOXX|주가|배당|삼성전자|하이닉스|마이크론|코스피|나스닥|실적|내부자|분배금|커버드콜|종목)'),
         ('부동산·대출', r'(아파트|전세|월세|오피스텔|주담대|대출|집값|국평|실거래|청약|주택)'),
         ('연봉·퇴직', r'(연봉|월급|실수령|퇴직금|실업급여|퇴사)'),
         ('연금·세금·정책', r'(연금|건보료|건강보험|세금|과세|비과세|기초연금|정책|국민연금|소득세)'),
         ('자산·예금', r'(순자산|자산|예금|이자|적금|파이어|은퇴|억)'),
         ('시황·금리', r'(금리|환율|금값|시황|국채)')]
# '내 돈 얼마형' = 시청자 자기 숫자(내 연봉·내 자산·N억 넣으면·몇 등)에 대입. '뉴스 정리형' = 시장·회사·제도 소식 자체.
MINE = r'(얼마|몇 주|몇 등|어디쯤|넣으면|넣고|받으려면|있어야|우리 집|내 |나와|월급 \d|실수령|순위|충분|가능할까|하는 법)'
NEWS = r'(시황|실적|인수|금리.*(최고|내렸)|주가는|발표|내부자|올랐는데|배당락|고점보다|이익 \d+배)'

def topic(t):
    for k, r in TOPIC:
        if re.search(r, t): return k
    return '기타'

def kind(t):
    m, n = bool(re.search(MINE, t)), bool(re.search(NEWS, t))
    return '내 돈 얼마형' if m and not n else '뉴스 정리형' if n and not m else '섞임'

def yt():
    sys.path.insert(0, HERE); import ytupload
    s = ytupload.service()
    up = s.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    while True:
        r = s.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i['contentDetails']['videoId'] for i in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    out = []
    for i in range(0, len(ids), 50):
        for v in s.videos().list(part='snippet,statistics,contentDetails,status', id=','.join(ids[i:i+50])).execute()['items']:
            if v['status']['privacyStatus'] != 'public': continue
            d = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', v['contentDetails']['duration']).groups()
            sec = int(d[0] or 0)*3600 + int(d[1] or 0)*60 + int(d[2] or 0)
            pub = v['snippet']['publishedAt']
            age_h = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(pub.replace('Z', '+00:00'))).total_seconds()/3600
            out.append(dict(id=v['id'], title=v['snippet']['title'], pub=pub[:10], age_h=round(age_h), sec=sec,
                            form='쇼츠' if sec <= 180 else '롱폼', views=int(v['statistics'].get('viewCount', 0))))
    return out

def cafe():
    arts = []
    for p in range(1, 10):
        u = f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=31789001&search.queryType=lastArticle&search.page={p}&search.perPage=50'
        l = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})))['message']['result']['articleList']
        if not l: break
        arts += [dict(no=a['articleId'], title=a['subject'], views=a.get('readCount', 0), comments=a.get('commentCount', 0)) for a in l]
    return arts

def table(rows, key):
    g = {}
    for r in rows: g.setdefault(key(r), []).append(r['views'])
    lines = ['| 칸 | 편수 | 합 | 중앙값 | 최대 |', '|---|---|---|---|---|']
    for k, v in sorted(g.items(), key=lambda x: -statistics.median(x[1])):
        lines.append(f'| {k} | {len(v)} | {sum(v):,} | {statistics.median(v):g} | {max(v):,} |')
    return '\n'.join(lines)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    v, c = yt(), cafe()
    for r in v + c: r['topic'], r['kind'] = topic(r['title']), kind(r['title'])
    json.dump(dict(yt=v, cafe=c), open(os.path.join(OUT, f'{TODAY}_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    md = [f'# 콘텐츠 표 {TODAY} (contentreview.py, 제목 키워드 자동 분류)', '',
          f'## 유튜브 공개 {len(v)}편 — 주제별', table(v, lambda r: r['topic']), '',
          '## 유튜브 — 형식별(쇼츠/롱폼 × 내 돈형/뉴스형)', table(v, lambda r: r['form'] + ' · ' + r['kind']), '',
          '## 유튜브 전 편', '| 조회 | 형식 | 공개 | 경과(시간) | 주제 | 틀 | 제목 |', '|---|---|---|---|---|---|---|']
    md += [f"| {r['views']:,} | {r['form']} | {r['pub']} | {r['age_h']} | {r['topic']} | {r['kind']} | {r['title'][:50]} |" for r in sorted(v, key=lambda r: -r['views'])]
    md += ['', f'## 카페 {len(c)}편 — 주제별', table(c, lambda r: r['topic']), '', '## 카페 — 형식별', table(c, lambda r: r['kind']), '',
           f"- 카페 댓글 합 {sum(r['comments'] for r in c)} · 질문형(?) 제목 {sum('?' in r['title'] for r in c)}/{len(c)}"]
    p = os.path.join(OUT, f'{TODAY}_tables.md'); open(p, 'w', encoding='utf-8').write('\n'.join(md)); print(p)
