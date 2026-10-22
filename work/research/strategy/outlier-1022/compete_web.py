# 경쟁 확인(노아 모리스 3단계): 구조 문구를 유튜브 검색 화면(로그인 없음, 올해 필터)에서 받고 → 영상·채널 숫자는 Data API(videos/channels.list, 50편에 1단위)
#   py -3.12 compete_web.py "문구1" "문구2" ...   → compete_web.json
import sys, os, re, json, urllib.parse, subprocess, statistics, html
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H,'..','..','..')); sys.path.insert(0, WORK)
import ytupload
yt = ytupload.service()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '');
    if not m: return 0
    a = [int(x or 0) for x in m.groups()]; return a[0]*86400+a[1]*3600+a[2]*60+a[3]
F = os.path.join(H, 'compete_web.json'); out = json.load(open(F, encoding='utf-8')) if os.path.exists(F) else {}
for q in sys.argv[1:]:
    ids = []
    for sp in ['EgIIBQ%3D%3D', 'CAMSAggF']:   # 올해·관련도 / 올해·조회순
        url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(q) + '&sp=' + sp
        h = subprocess.run(['curl', '-s', '-A', UA, '-H', 'Accept-Language: ko-KR', url], capture_output=True).stdout.decode('utf-8', 'ignore')
        for i in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', h):
            if i not in ids: ids.append(i)
    vs = []
    for i in range(0, len(ids), 50):
        vs += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute().get('items', [])
    cids = list({v['snippet']['channelId'] for v in vs}); chs = {}
    for i in range(0, len(cids), 50):
        for c in yt.channels().list(part='snippet,statistics', id=','.join(cids[i:i+50])).execute().get('items', []):
            s = c['statistics']; chs[c['id']] = dict(title=c['snippet']['title'], subs=None if s.get('hiddenSubscriberCount') else int(s.get('subscriberCount', 0)), opened=c['snippet']['publishedAt'][:10])
    rows = []
    for v in vs:
        c = chs.get(v['snippet']['channelId'], {}); rows.append(dict(id=v['id'], title=html.unescape(v['snippet']['title']), pub=v['snippet']['publishedAt'][:10], sec=sec(v['contentDetails'].get('duration')),
            views=int(v['statistics'].get('viewCount', 0)), cid=v['snippet']['channelId'], ch=c.get('title'), subs=c.get('subs'), opened=c.get('opened')))
    out[q] = rows; json.dump(out, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('##', q, '결과', len(rows))
# 요약(10/22 덧붙임): 문구별 채널 수·구독 층·작은 채널 성공(구독 1만 미만, 조회÷구독 ≥10, 조회 3,000+)
summ = {}
for q, rows in out.items():
    chs = {}
    for r in rows: chs[r['cid']] = r['subs']
    s = [v for v in chs.values() if v is not None]
    summ[q] = dict(results=len(rows), channels=len(chs), ch_100k=sum(v >= 1e5 for v in s), ch_10k_100k=sum(1e4 <= v < 1e5 for v in s), ch_small=sum(v < 1e4 for v in s),
                   small_wins=sum(1 for r in rows if r['subs'] is not None and r['subs'] < 1e4 and r['views'] / max(r['subs'], 1) >= 10 and r['views'] >= 3000),
                   top=[(r['views'], r['subs'], r['ch'], r['title'][:50]) for r in sorted(rows, key=lambda r: -r['views'])[:3]])
json.dump(summ, open(os.path.join(H, 'compete_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for q, s in summ.items(): print(f"{q} | 결과{s['results']} 채널{s['channels']} 10만+{s['ch_100k']} 1만~10만{s['ch_10k_100k']} 1만미만{s['ch_small']} 작은성공{s['small_wins']} | {s['top'][0] if s['top'] else ''}")
