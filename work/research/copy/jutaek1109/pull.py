# 11/26 주택연금 칸 앞말: 경쟁 제목(최근 1년 조회순)·AqIAvPw-pFE 댓글 질문 (copywriter 11/9)
import sys, json, re, datetime, os
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import ytupload
yt = ytupload.service()
here = os.path.dirname(os.path.abspath(__file__))
since = (datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
ids = []
for d in ('medium', 'long'):
    r = yt.search().list(part='id', q='주택연금', type='video', order='viewCount', publishedAfter=since, videoDuration=d, regionCode='KR', relevanceLanguage='ko', maxResults=15).execute()
    ids += [i['id']['videoId'] for i in r.get('items', [])]
v = yt.videos().list(part='snippet,statistics', id=','.join(ids[:50])).execute()['items']
rows = sorted([dict(id=x['id'], title=x['snippet']['title'], ch=x['snippet']['channelTitle'], date=x['snippet']['publishedAt'][:10], views=int(x['statistics'].get('viewCount', 0))) for x in v], key=lambda r: -r['views'])
for r in rows[:15]: print(f"{r['views']:>9,} {r['date']} {r['id']} {r['ch']} | {r['title']}")
cm = []
for vid in ['AqIAvPw-pFE'] + [r['id'] for r in rows[:3]]:
    try:
        c = yt.commentThreads().list(part='snippet', videoId=vid, order='relevance', maxResults=50, textFormat='plainText').execute()
        for t in c.get('items', []):
            s = t['snippet']['topLevelComment']['snippet']
            cm.append(dict(v=vid, likes=s['likeCount'], text=s['textDisplay'][:200].replace('\n', ' ')))
    except Exception as e: print('댓글 못 받음', vid, str(e)[:80])
json.dump(dict(rows=rows, comments=cm), open(os.path.join(here, 'pull_1109.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('\n== 물음표 댓글(좋아요순)')
for c in sorted([c for c in cm if '?' in c['text'] or '까' in c['text']], key=lambda c: -c['likes'])[:25]: print(c['likes'], c['v'], c['text'][:150])
