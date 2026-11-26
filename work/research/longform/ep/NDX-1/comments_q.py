# NDX-1 경쟁 영상 댓글 중 물음 — commentThreads.list(관련순 100개씩) · 읽기만 (youtube-loop 2026-11-27, CC-1 comments_q.py 꼴)
import sys, json, re
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import f2_coupang
yt = f2_coupang.service(); out = []
for v in ['ek6y8KdBNSk', 'FuMxH_PLR9M', 'TT46dYq2-SI', '8dNLA6XK-9o', 'sA83WNMYiqU', 'fewTitcsbWk']:
    try: r = yt.commentThreads().list(part='snippet', videoId=v, order='relevance', maxResults=100, textFormat='plainText').execute()
    except Exception as e: print(v, 'ERR', str(e)[:90]); continue
    for it in r['items']:
        c = it['snippet']['topLevelComment']; s = c['snippet']; t = s['textDisplay'].replace('\n', ' ')
        if '?' in t or re.search(r'(까요|나요|ㄹ까|을까|인가요|건가요|궁금)', t):
            out.append(dict(v=v, id=c['id'], like=s['likeCount'], t=t[:300]))
out.sort(key=lambda x: -x['like'])
json.dump(out, open('raw/comments_q_1127.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out))
for o in out[:40]: print(o['like'], f"https://www.youtube.com/watch?v={o['v']}&lc={o['id']}", '|', o['t'][:160])
