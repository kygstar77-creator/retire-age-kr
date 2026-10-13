# r1s_startday 경쟁 쇼츠(10/13 PD, r1s_spytax/ytshort_r1.py 복사 · 30일 = 9/13 이후)
# w1s_div·g1s_buyday·r1s_fx 경쟁 쇼츠(10/12 PD, c1s_half/ytshort_c1s.py 복사): 유튜브 웹 검색(innertube, Data API search 할당량 소진) + Data API videos.list + 첫 3초 자막
import sys, os, re, json, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'c1s_half'))
import ytupload, itsearch
yt = ytupload.service()
BASE = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\cardshorts'
EP = {
 'r1s_startday': ['예금 vs 미국 ETF','금 vs 주식 수익률','S&P500 1억','투자 시점 수익률','1억 어디에 넣을까'],
}
def dur(s):
    m = re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s); return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
def first3(vid):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        tr = YouTubeTranscriptApi().fetch(vid, languages=['ko'])
        txt = ' '.join(s.text for s in tr if s.start < 3.0)
        return txt.replace('\n', ' ').strip() or None
    except Exception as e:
        return 'ERR:' + type(e).__name__
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
def shorts_code(vid):
    try:
        rq = urllib.request.Request('https://www.youtube.com/shorts/' + vid, headers={'User-Agent': 'Mozilla/5.0'})
        try: return urllib.request.build_opener(NR).open(rq, timeout=20).status
        except urllib.error.HTTPError as e: return e.code
    except Exception as e: return str(e)[:40]
only = sys.argv[1:] or list(EP)
for ep in only:
    vids = {}
    for q in EP[ep]:
        for qq, pp in ((q, 'EgIIBA%3D%3D'), (q + ' #shorts', 'EgIIBA%3D%3D'), (q, 'EgQIBBgB')):
            try:
                for vid in itsearch.search(qq, pp, pages=3): vids.setdefault(vid, q)
            except Exception as e: print('ERR', qq, e)
    ids = list(vids); info = []
    for i in range(0, len(ids), 50):
        info += yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']
    chs = list({v['snippet']['channelId'] for v in info}); subs = {}
    for i in range(0, len(chs), 50):
        for c in yt.channels().list(part='statistics,snippet', id=','.join(chs[i:i+50])).execute()['items']:
            subs[c['id']] = (int(c['statistics'].get('subscriberCount', 0) or 0), c['snippet']['title'])
    rows = []
    for v in info:
        sb, ct = subs.get(v['snippet']['channelId'], (0, '?')); views = int(v['statistics'].get('viewCount', 0))
        rows.append({'id': v['id'], 'q': vids[v['id']], 'title': v['snippet']['title'], 'channel': ct, 'subs': sb, 'views': views,
                     'ratio': round(views/sb,2) if sb else None, 'sec': dur(v['contentDetails']['duration']), 'pub': v['snippet']['publishedAt'][:10],
                     'lang': v['snippet'].get('defaultAudioLanguage') or v['snippet'].get('defaultLanguage'),
                     'desc': v['snippet'].get('description', '')[:300]})
    print('=====', ep, 'ids', len(ids), 'meta', len(rows))
    rows = [r for r in rows if r['pub'] >= '2026-09-13' and 0 < r['sec'] <= 60 and re.search('[가-힣]', r['title'] + r['channel'])]
    for r in rows: r['shorts_url'] = shorts_code(r['id'])
    rows.sort(key=lambda r: -r['views'])
    pass
    os.makedirs(os.path.join(BASE, ep), exist_ok=True)
    json.dump(rows, open(os.path.join(BASE, ep, 'compete_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('kept', len(rows))
    for r in rows[:30]: print(r['id'], r['views'], r['ratio'], r['sec'], r['pub'], r['lang'], r['channel'], '|', r['q'], '|', r['title'], '|', r['shorts_url'], '|', r.get('first3'))
