# W-1 주간 리포트 수요 조사: 최근 30일 한국 유튜브에서 '한 주 시장 정리'류 영상 조회 상위를 모은다.
# 업로드 토큰이 만료돼(9/30) 읽기 전용 분석 토큰(ytanalytics)으로 검색한다. 검색 1회 = 100 단위.
import sys, os, json, datetime, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import ytanalytics as a
from googleapiclient.discovery import build

QS = sys.argv[1:] or ['미국증시 정리', '배당주 이번주', '다음주 일정 증시']
yt = build('youtube', 'v3', credentials=a.creds())
after = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
out = {}
for q in QS:
    r = yt.search().list(part='snippet', q=q, type='video', maxResults=25, publishedAfter=after,
                         regionCode='KR', relevanceLanguage='ko', order='viewCount').execute()
    out[q] = [i['id']['videoId'] for i in r['items']]
ids = list(dict.fromkeys(sum(out.values(), [])))
vids = {}
for i in range(0, len(ids), 50):
    for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).execute()['items']:
        vids[v['id']] = v
chs = list({v['snippet']['channelId'] for v in vids.values()})
subs = {}
for i in range(0, len(chs), 50):
    for c in yt.channels().list(part='statistics,snippet', id=','.join(chs[i:i + 50])).execute()['items']:
        subs[c['id']] = (int(c['statistics'].get('subscriberCount', 0)), c['snippet']['title'])

def dur(s):
    m = re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); h, mi, se = [int(x or 0) for x in m.groups()]; return h * 60 + mi + se / 60

rows = []
for vid, v in vids.items():
    s, t = subs.get(v['snippet']['channelId'], (0, ''))
    views = int(v['statistics'].get('viewCount', 0))
    rows.append(dict(id=vid, title=v['snippet']['title'], ch=t, chid=v['snippet']['channelId'], subs=s, views=views,
                     ratio=round(views / max(s, 1), 2), min=round(dur(v['contentDetails']['duration']), 1),
                     date=v['snippet']['publishedAt'][:10], q=[k for k, l in out.items() if vid in l]))
rows.sort(key=lambda r: -r['views'])
p = os.path.join(os.path.dirname(__file__), 'yt_top.json')
json.dump(dict(fetched=datetime.date.today().isoformat(), after=after, queries=out, rows=rows), open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(rows), {k: len(v) for k, v in out.items()})
for x in rows:
    if x['min'] >= 3:
        print(x['views'], x['ratio'], x['min'], x['date'], x['subs'], x['ch'][:12], '|', x['title'][:60], x['id'])
