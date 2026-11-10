import os, sys, json, re, datetime
sys.stdout.reconfigure(encoding='utf-8')
WORK = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'
sys.path.insert(0, WORK); import ytupload
yt = ytupload.service()
CH = {'UCE9Q2l8yGDiDph3nTIQvDzQ':'위키타카','UC4i1O9S9_RVztD333qiCp5Q':'1분썰배달','UCS_vefzRwq-vhxcswl2zMWw':'시니어노후',
      'UC02kXDUIhuSqZYb191FneJA':'노후 관리사무소','UCEJIw_FUvkxK7ZoiejSj7HA':'투자360','UC2ByczqyZtt0Lj2DCkQuXJA':'절세미녀',
      'UCiIp3SArhmQjBsr_tt6Jq9A':'김범곤의 연금수업','UCohjHDdtYtoKYtiCSVFoHAw':'KODEX','UCriq8I8GEESkQq0svX19oCw':'부티플','UC1eyYJRpM_g5WBp60mmRwCQ':'경제명탐정'}
def dur(s):
    m = re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
out = {}
for cid, nm in CH.items():
    up = 'UU' + cid[2:]; ids = []; tok = None
    while len(ids) < 300:
        try: r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        except Exception as e: print(nm, 'ERR', e); break
        ids += [x['contentDetails']['videoId'] for x in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    vids = []
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[k:k+50])).execute()['items']:
            vids.append({'id': v['id'], 'pub': v['snippet']['publishedAt'], 'sec': dur(v['contentDetails']['duration']),
                         'views': int(v['statistics'].get('viewCount', 0) or 0), 'title': v['snippet']['title'][:50],
                         'thumb': v['snippet']['thumbnails'].get('medium', {}).get('url')})
    vids.sort(key=lambda x: x['pub'])
    out[cid] = {'name': nm, 'vids': vids}
    print(nm, len(ids), 'shorts', sum(1 for v in vids if v['sec'] <= 180))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comp.json'), 'w', encoding='utf-8'), ensure_ascii=False)
