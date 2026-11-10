import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
WORK = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'
sys.path.insert(0, WORK); import ytupload
rows = [json.loads(x) for x in open(os.path.join(WORK, 'research','cardshorts','log.jsonl'), encoding='utf-8') if x.strip()]
yt = ytupload.service()
ids = [r['id'] for r in rows if r.get('id')]
info = {}
for k in range(0, len(ids), 50):
    for v in yt.videos().list(part='statistics,snippet,status,contentDetails', id=','.join(ids[k:k+50])).execute()['items']:
        info[v['id']] = {'views': int(v['statistics'].get('viewCount', 0)), 'pub': v['snippet']['publishedAt'], 'priv': v['status']['privacyStatus'], 'dur': v['contentDetails']['duration']}
out = []
for r in rows:
    i = info.get(r.get('id'))
    out.append({'id': r.get('id'), 'layout': r.get('layout'), 'publishAt': r.get('publishAt') or r.get('at'), 'title': r['title'][:40], **(i or {'views': None})})
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'views.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# channel uploads all
ch = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
allv = []; tok = None
while True:
    r = yt.playlistItems().list(part='contentDetails', playlistId=ch, maxResults=50, pageToken=tok).execute()
    allv += [x['contentDetails']['videoId'] for x in r['items']]; tok = r.get('nextPageToken')
    if not tok: break
print('channel uploads', len(allv), 'log ids', len(ids), 'not in log', len(set(allv)-set(ids)))
for o in out: print(o['publishAt'][:16], o['layout'], o.get('priv'), o['views'], o['title'])
