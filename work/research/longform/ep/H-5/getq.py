# H-5 질문 모으기 — 경쟁 영상 댓글(유튜브 Data API commentThreads, 좋아요 순) + 네이버 자동완성
import sys, os, json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
import ytupload
yt = ytupload.service(); out = {'comments': {}, 'ac': {}}
for v in ['6mwoQqj77J8', 'tOn0Q-wrjlk', 'ZQjOiB4F_b0', 'QmHIrynkyiA', 'XdmVjZLmJgo', 'xTS1QbDH1vs']:
    try:
        r = yt.commentThreads().list(part='snippet', videoId=v, order='relevance', maxResults=60, textFormat='plainText').execute()
        out['comments'][v] = [{'id': i['id'], 'like': i['snippet']['topLevelComment']['snippet']['likeCount'], 't': i['snippet']['topLevelComment']['snippet']['textDisplay'][:300]} for i in r.get('items', [])]
    except Exception as e: out['comments'][v] = str(e)[:200]
for q in ['송도 아파트', '송도 집값', '송도 전세', '송도더샵센트럴시티']:
    u = 'https://ac.search.naver.com/nx/ac?q=' + urllib.parse.quote(q) + '&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&st=100'
    try: out['ac'][q] = [x[0] for x in json.load(urllib.request.urlopen(u, timeout=10))['items'][0]]
    except Exception as e: out['ac'][q] = str(e)[:100]
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'raw', 'q_1022.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for q, a in out['ac'].items(): print('AC', q, a)
for v, cs in out['comments'].items():
    if isinstance(cs, str): print(v, cs); continue
    for c in cs:
        if '?' in c['t'] or '까' in c['t'] or '나요' in c['t']: print(v, c['id'], c['like'], c['t'].replace('\n', ' ')[:180])
