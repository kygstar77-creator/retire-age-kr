# 10/19 쿠팡 링크 전수: 채널 업로드 전부의 설명란에서 coupa.ng·link.coupang 검색 (읽기만)
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'
sys.path.insert(0, W)
import f2_coupang
yt = f2_coupang.service()
ch = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]
up = ch['contentDetails']['relatedPlaylists']['uploads']
ids, tok = [], None
while True:
    r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
    ids += [i['contentDetails']['videoId'] for i in r['items']]
    tok = r.get('nextPageToken')
    if not tok: break
rows = []
for k in range(0, len(ids), 50):
    for v in yt.videos().list(part='snippet,status,contentDetails,paidProductPlacementDetails', id=','.join(ids[k:k+50])).execute()['items']:
        d = v['snippet']['description']
        hits = [l for l in d.split('\n') if re.search(r'coupa\.ng|link\.coupang|쿠팡', l)]
        rows.append({'id': v['id'], 'title': v['snippet']['title'], 'privacy': v['status']['privacyStatus'],
                     'publishAt': v['status'].get('publishAt'), 'dur': v['contentDetails']['duration'],
                     'paid': (v.get('paidProductPlacementDetails') or {}).get('hasPaidProductPlacement'), 'coupang_lines': hits})
json.dump(rows, open(os.path.join(os.path.dirname(__file__), 'census.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('전체', len(rows))
for r in rows:
    if r['coupang_lines']: print(r['id'], r['privacy'], r['dur'], r['paid'], r['title'][:40], '|', ' / '.join(r['coupang_lines'])[:200])
