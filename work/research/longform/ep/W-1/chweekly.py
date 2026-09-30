# W-1: 주간 정리 코너를 가진 채널의 최근 50편 — 주간 코너 편과 나머지의 조회 중앙값·공개 요일 비교.
# 검색이 아니라 업로드 목록(1단위)만 쓴다.
import sys, os, json, re, statistics, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import ytanalytics as a
from googleapiclient.discovery import build

# 채널 id: 주간 코너 판별 정규식
CH = {
    'UCfnqgWlC5IvJEAPTmyjaixA': '주간|이번 ?주|다음 ?주|한 ?주',   # 수페TV
    'UCC3yfxS5qC6PCwDzetUuEWg': '주간|이번 ?주|다음 ?주|한 ?주',   # 소수몽키
}
yt = build('youtube', 'v3', credentials=a.creds())
top = json.load(open(os.path.join(os.path.dirname(__file__), 'yt_top.json'), encoding='utf-8'))['rows']
for r in top:  # 검색에서 '다음주/이번주' 코너가 보인 채널을 더한다
    if re.search('다음 ?주|이번 ?주|주간', r['title']) and r['min'] >= 5: CH.setdefault(r['chid'], '다음 ?주|이번 ?주|주간')

def dur(s):
    m = re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = [int(x or 0) for x in m.groups()]; return h * 60 + mi + se / 60

res = {}
for cid, pat in CH.items():
    ch = yt.channels().list(part='contentDetails,snippet,statistics', id=cid).execute()['items'][0]
    up = ch['contentDetails']['relatedPlaylists']['uploads']
    ids = [i['contentDetails']['videoId'] for i in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute()['items']]
    vs = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']
    rows = []
    for v in vs:
        m = dur(v['contentDetails']['duration'])
        if m < 3: continue  # 쇼츠 제외
        t = datetime.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00')) + datetime.timedelta(hours=9)
        rows.append(dict(id=v['id'], title=v['snippet']['title'], views=int(v['statistics'].get('viewCount', 0)), min=round(m, 1),
                         kst=t.strftime('%Y-%m-%d %a %H:%M'), weekly=bool(re.search(pat, v['snippet']['title']))))
    w = [r['views'] for r in rows if r['weekly']]; o = [r['views'] for r in rows if not r['weekly']]
    res[cid] = dict(title=ch['snippet']['title'], subs=int(ch['statistics'].get('subscriberCount', 0)), rows=rows,
                    weekly_n=len(w), weekly_med=statistics.median(w) if w else None, other_n=len(o), other_med=statistics.median(o) if o else None)
    print(ch['snippet']['title'][:14], '구독', res[cid]['subs'], '| 주간코너', len(w), '편 중앙', res[cid]['weekly_med'], '| 나머지', len(o), '편 중앙', res[cid]['other_med'])
    for r in rows:
        if r['weekly']: print('   ', r['kst'], r['views'], r['min'], r['title'][:50])
json.dump(res, open(os.path.join(os.path.dirname(__file__), 'ch_weekly.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
