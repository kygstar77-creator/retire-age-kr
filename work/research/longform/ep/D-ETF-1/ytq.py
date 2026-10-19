# D-ETF-1: 30일 상위 영상 댓글에서 질문(물음표·'어떻게'·'얼마') 뽑기 — 공식 Data API commentThreads
import sys, json, re
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import ytupload
yt = ytupload.service()
top = json.load(open('raw/yt_top30_1019.json', encoding='utf-8'))
seen = {}
for q, rows in top.items():
    for r in rows:
        if re.search(r'[가-힣]', r['title']) and r['views'] >= 50000: seen[r['id']] = r
out = []
for vid, r in sorted(seen.items(), key=lambda x: -x[1]['views'])[:14]:
    try:
        res = yt.commentThreads().list(part='snippet', videoId=vid, maxResults=100, order='relevance', textFormat='plainText').execute()
    except Exception as e:
        print('skip', vid, str(e)[:80]); continue
    for it in res['items']:
        s = it['snippet']['topLevelComment']['snippet']
        out.append(dict(vid=vid, ch=r['ch'], title=r['title'][:50], text=s['textDisplay'].replace('\n', ' ')[:300], likes=s['likeCount']))
json.dump(out, open('raw/yt_comments_1019.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
qs = [c for c in out if re.search(r'\?|어떻게|얼마|뭐가|어느|할까|하나요|인가요|나요|까요|세금|환율|섹터', c['text'])]
print(len(out), '댓글 /', len(qs), '질문꼴')
for c in sorted(qs, key=lambda c: -c['likes'])[:70]: print(f"{c['likes']:>4} [{c['ch'][:8]}] {c['text'][:170]}")
