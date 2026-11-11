# JT-1 toc_compare 재료: 상위 영상 설명란 챕터(videos.list, 1단위) → raw/toc_desc_1111.json
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
import ytupload
yt = ytupload.service()
top = json.load(open(os.path.join(HERE, 'raw', 'yt_top_jt1.json'), encoding='utf-8'))
ids = [r['id'] for r in top]
out = {}
for i in range(0, len(ids), 50):
    for it in yt.videos().list(part='snippet', id=','.join(ids[i:i+50])).execute()['items']:
        d = it['snippet']['description']
        ch = [l.strip() for l in d.splitlines() if re.match(r'^\s*\(?\d{1,2}:\d{2}', l)]
        out[it['id']] = {'title': it['snippet']['title'], 'ch': it['snippet']['channelTitle'], 'chapters': ch, 'desc_head': d[:300]}
json.dump(out, open(os.path.join(HERE, 'raw', 'toc_desc_1111.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in top:
    o = out.get(r['id'])
    print(r['id'], r['views'], r['mult'], r['mins'], '챕터', len(o['chapters']) if o else '없음(비공개?)')
