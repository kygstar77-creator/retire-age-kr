# CC-1 경쟁 영상 댓글 중 물음 — commentThreads.list(관련순 100개씩, 3편) · 읽기만 (youtube-loop 2026-11-22)
import sys, json, re
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import f2_coupang
yt = f2_coupang.service(); out = []   # 업로드·분석 토큰은 commentThreads 403 → 관리 토큰(ytcomment.py와 같은 것), list만 씀
for v in ['yXQ-EMTEQ-k', 'amc8B8SxwgY', 'sGrkDT8vnDY', 'tU1kVGy52qE']:
    r = yt.commentThreads().list(part='snippet', videoId=v, order='relevance', maxResults=100, textFormat='plainText').execute()
    for it in r['items']:
        c = it['snippet']['topLevelComment']; s = c['snippet']
        t = s['textDisplay'].replace('\n', ' ')
        if '?' in t or re.search(r'(까요|나요|ㄹ까|을까|인가요|건가요|궁금)', t):
            out.append(dict(v=v, id=c['id'], like=s['likeCount'], t=t[:300]))
out.sort(key=lambda x: -x['like'])
json.dump(out, open('raw/comments_q_1122.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open('raw/comments_q_1122.txt', 'w', encoding='utf-8') as f:
    for o in out: f.write(f"{o['like']}\thttps://www.youtube.com/watch?v={o['v']}&lc={o['id']}\t{o['t']}\n")
print(len(out))
