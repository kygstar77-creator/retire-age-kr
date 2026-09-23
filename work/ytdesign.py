# 경쟁 채널 디자인 수집 — 썸네일(공개 URL, 차단 없음) + 제목·조회수(YouTube Data API, 우리 OAuth). 2026-09-23.
#   py -3.12 work/ytdesign.py <채널ID> <이름> [편수=30]        → work/research/yt/design/<이름>/ 썸네일 jpg + meta.json
#   py -3.12 work/ytdesign.py --all                            → channels.txt 전부
# 목적: 썸네일 구도·글자 크기·색 대비를 우리 눈으로 보고 우리 디자인을 새로 만드는 것. 남의 디자인을 베끼지 않는다.
import sys, os, re, json, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'research', 'yt', 'design'); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)

def service():
    import ytupload
    return ytupload.service()

def fetch_channel(cid, name, n=30):
    yt = service()
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    ch = yt.channels().list(part='contentDetails,statistics,snippet', id=cid).execute()['items'][0]
    pl = ch['contentDetails']['relatedPlaylists']['uploads']
    items, token = [], None
    while len(items) < n:
        r = yt.playlistItems().list(part='snippet', playlistId=pl, maxResults=min(50, n - len(items)), pageToken=token).execute()
        items += r.get('items', []); token = r.get('nextPageToken')
        if not token: break
    ids = [i['snippet']['resourceId']['videoId'] for i in items]
    vids = []
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).execute()['items']:
            dur = v['contentDetails']['duration']
            m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', dur)
            secs = int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)
            vids.append({'id': v['id'], 'title': v['snippet']['title'], 'views': int(v['statistics'].get('viewCount', 0)),
                         'date': v['snippet']['publishedAt'][:10], 'sec': secs, 'short': secs <= 70,
                         'thumb': (v['snippet']['thumbnails'].get('maxres') or v['snippet']['thumbnails'].get('high'))['url']})
    vids.sort(key=lambda x: -x['views'])
    got = 0
    for v in vids[:20]:
        p = os.path.join(d, f"{v['views']:010d}_{'S' if v['short'] else 'L'}_{v['id']}.jpg")
        if os.path.exists(p): got += 1; continue
        try:
            b = urllib.request.urlopen(urllib.request.Request(v['thumb'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
            open(p, 'wb').write(b); got += 1; time.sleep(0.3)
        except Exception as e: print('썸네일 실패', v['id'], str(e)[:40])
    json.dump({'channel': ch['snippet']['title'], 'subs': ch['statistics'].get('subscriberCount'), 'videos': vids},
              open(os.path.join(d, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sh = [v for v in vids if v['short']]
    print(f"{name}: 구독 {ch['statistics'].get('subscriberCount')} | 영상 {len(vids)}편(쇼츠 {len(sh)}) | 썸네일 {got}장 | 쇼츠 조회 상위: " +
          ' / '.join(f"{v['views']:,} {v['title'][:28]}" for v in sh[:3]))
    return vids

if __name__ == '__main__':
    if sys.argv[1] == '--all':
        for line in open(os.path.join(HERE, 'research', 'yt', 'channels.txt'), encoding='utf-8'):
            if line.startswith('#') or not line.strip(): continue
            cid, name = line.split()[0], line.split()[1]
            try: fetch_channel(cid, name, int(sys.argv[2]) if len(sys.argv) > 2 else 30)
            except Exception as e: print(name, '실패', str(e)[:80])
            time.sleep(1)
    else:
        fetch_channel(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30)
