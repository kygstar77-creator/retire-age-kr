# H-3·J-1 실제 질문 모으기 — 경쟁 상위 영상 댓글(YouTube Data API commentThreads, 무료 할당 1단위/회) + 조회수 다시 재기.
# 실행: py -3.12 work/research/longform/ep/H-3/getq.py <편> <영상ID...>  → raw/yt_comments_<날짜>.json
import sys, os, json, datetime, re
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, W)
import f2_coupang
ep, vids = sys.argv[1], sys.argv[2:]
yt = f2_coupang.service()
out = {'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'videos': {}}
st = yt.videos().list(part='statistics,snippet,contentDetails', id=','.join(vids)).execute()
for v in st['items']:
    out['videos'][v['id']] = {'title': v['snippet']['title'], 'channel': v['snippet']['channelTitle'], 'published': v['snippet']['publishedAt'][:10],
                              'views': int(v['statistics'].get('viewCount', 0)), 'comments': int(v['statistics'].get('commentCount', 0)), 'dur': v['contentDetails']['duration'], 'top': []}
for vid in vids:
    if vid not in out['videos']: continue
    try:
        r = yt.commentThreads().list(part='snippet', videoId=vid, order='relevance', maxResults=100, textFormat='plainText').execute()
    except Exception as e:
        out['videos'][vid]['err'] = str(e)[:120]; continue
    for it in r.get('items', []):
        s = it['snippet']['topLevelComment']['snippet']
        out['videos'][vid]['top'].append({'id': it['id'], 'text': s['textDisplay'][:400], 'likes': s.get('likeCount', 0), 'at': s['publishedAt'][:10], 'replies': it['snippet'].get('totalReplyCount', 0)})
p = os.path.join(W, 'research', 'longform', 'ep', ep, 'raw', f'yt_comments_{datetime.date.today():%m%d}.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for vid, v in out['videos'].items():
    q = [c for c in v['top'] if '?' in c['text'] or re.search(r'(나요|까요|가요|ㄴ가|는지|어떻게|얼마)', c['text'])]
    print(f"== {vid} {v['channel']} 조회 {v['views']:,} 댓글 {v['comments']} · 받은 {len(v['top'])} · 질문꼴 {len(q)}")
    for c in sorted(q, key=lambda c: -c['likes'])[:12]: print(f"  [{c['likes']}] {c['at']} {c['id']} {c['text'][:160]!r}")
