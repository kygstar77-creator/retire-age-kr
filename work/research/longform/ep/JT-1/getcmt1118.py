# JT-1 review 공개 조건 2 — 단희TV TX4W8Tpftfg 상위 댓글(관련도 순) 12개 중 상속 질문 수 다시 세기 (youtube-loop 11/18)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
import f2_coupang
yt = f2_coupang.service()
r = yt.commentThreads().list(part='snippet', videoId='TX4W8Tpftfg', order='relevance', maxResults=20, textFormat='plainText').execute()
cs = [{'id': i['id'], 'like': i['snippet']['topLevelComment']['snippet']['likeCount'], 't': i['snippet']['topLevelComment']['snippet']['textDisplay'][:400]} for i in r.get('items', [])]
json.dump(cs, open(os.path.join(os.path.dirname(__file__), 'raw', 'cmt_TX4W8_1118.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for n, c in enumerate(cs[:12], 1): print(n, c['like'], c['id'], c['t'].replace('\n', ' ')[:200])
