# h4s_ladder 경쟁 쇼츠 찾기(11/14 PD) — Data API search(KR·ko·short), 10/15 이후, 관련순 → compete_raw.json
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
import ytupload as u
yt = u.service()
Q = ['철산동 아파트', '광명 아파트 가격 차이', '같은 동네 아파트 가격 차이', '신축 구축 가격 차이', '구축이 신축보다 비싼', '광명 철산 시세', '철산 래미안자이', '철산주공']
seen = {}
for q in Q:
    r = yt.search().list(part='snippet', q=q, type='video', videoDuration='short', regionCode='KR', relevanceLanguage='ko', publishedAfter='2026-10-15T00:00:00Z', maxResults=25, order='relevance').execute()
    for it in r['items']:
        seen.setdefault(it['id']['videoId'], {'q': q, 'title': it['snippet']['title'], 'ch': it['snippet']['channelTitle'], 'at': it['snippet']['publishedAt'][:10]})
ids = list(seen)
for i in range(0, len(ids), 50):
    for it in yt.videos().list(part='statistics,contentDetails', id=','.join(ids[i:i + 50])).execute()['items']:
        d = it['contentDetails']['duration']; m = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', d)
        seen[it['id']].update(views=int(it['statistics'].get('viewCount', 0)), sec=(int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else None)
json.dump(seen, open(os.path.join(os.path.dirname(__file__), 'compete_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in sorted(seen.items(), key=lambda x: -x[1].get('views', 0))[:40]:
    print(k, v.get('views'), v.get('sec'), v['at'], v['ch'][:14], '|', v['title'][:60], '|', v['q'])
