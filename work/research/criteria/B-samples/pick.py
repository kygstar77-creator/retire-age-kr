# B-screen 표본 고르기(10/19) — 유튜브 Data API 읽기만. 채널마다 최근 업로드 50편에서 쇼츠(≤180초)·롱폼(>180초, 라이브 아님) 조회 순.
#   python work/research/criteria/B-samples/pick.py            → channels.json, cands.json
import sys, os, re, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
import ytupload
CH = {
 '수페TV': 'UCfnqgWlC5IvJEAPTmyjaixA', '소수몽키': 'UCC3yfxS5qC6PCwDzetUuEWg', '월급쟁이부자들TV': 'UCDSj40X9FFUAnx1nv7gQhcA',
 '김작가TV': 'UCvil4OAt-zShzkKHsg9EQAw', '부읽남TV': 'UC2QeHNJFfuQWB4cy3M-745g', '슈카월드': 'UCsJ6RuBiTVWRX156FVbeaGg',
 '머니인사이드': 'UCxfko2YOD6DODYRGzeOPhIQ', '박곰희TV': 'UCr7XsrSrvAn_WcU4kF99bbQ', '똑재TV': 'UCmshc9VpICv4oPyjMK3Vk_w',
 '815머니톡': 'UCCG6BEYjfQMGzypJw2EJCDQ', '싱글파이어': 'UC5CyCSvCdoEP-VgQmFq3iww', '은퇴머니': 'UCQrlX5mzcTICHZC1BMVKwhQ',
 '오십의 경제지도': 'UCqcbPnnY1jxklrdTwLH0qqA', '투자360': 'UCEJIw_FUvkxK7ZoiejSj7HA', '자람들': 'UC5UFGiELUPSTvFfMGEUxeiQ',
 '연금왕 배형': 'UCV5OaRenLVz74JYlTzg3G-Q',
}
SEARCH = ['삼프로TV', '리치고TV', '렘군']
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    a = [int(x or 0) for x in m.groups()] if m else [0, 0, 0, 0]; return a[0]*86400+a[1]*3600+a[2]*60+a[3]
yt = ytupload.service()
for q in SEARCH:
    r = yt.search().list(part='snippet', q=q, type='channel', maxResults=3, regionCode='KR').execute()['items']
    print(q, [(x['snippet']['title'], x['snippet']['channelId']) for x in r])
    if r: CH[r[0]['snippet']['title']] = r[0]['snippet']['channelId']
now = datetime.datetime.now(datetime.timezone.utc); chans, cands = {}, []
for name, cid in CH.items():
    ch = yt.channels().list(part='snippet,statistics,contentDetails', id=cid).execute()['items'][0]
    subs = int(ch['statistics'].get('subscriberCount', 0)); up = ch['contentDetails']['relatedPlaylists']['uploads']
    ids = [x['contentDetails']['videoId'] for x in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute()['items']]
    vs = yt.videos().list(part='snippet,statistics,contentDetails,liveStreamingDetails', id=','.join(ids)).execute()['items']
    chans[name] = {'id': cid, 'title': ch['snippet']['title'], 'subs': subs}
    for v in vs:
        s = sec(v['contentDetails'].get('duration')); pub = datetime.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00'))
        age = (now - pub).total_seconds() / 86400
        if age < 3 or 'liveStreamingDetails' in v: continue
        views = int(v['statistics'].get('viewCount', 0))
        cands.append(dict(ch=name, id=v['id'], title=v['snippet']['title'], published=v['snippet']['publishedAt'][:10], age=round(age, 1), sec=s,
                          kind='short' if s <= 180 else 'long', views=views, subs=subs, ratio=round(views / max(subs, 1), 3)))
json.dump({'collected': now.isoformat(timespec='minutes'), 'channels': chans}, open(os.path.join(HERE, 'channels.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(cands, open(os.path.join(HERE, 'cands.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
import collections
for name in chans:
    c = [x for x in cands if x['ch'] == name]
    s = sorted([x for x in c if x['kind'] == 'short'], key=lambda x: -x['views']); l = sorted([x for x in c if x['kind'] == 'long'], key=lambda x: -x['views'])
    print(f"{name}\t구독 {chans[name]['subs']:,}\t쇼츠 {len(s)} 최고 {s[0]['ratio'] if s else '-'}\t롱폼 {len(l)} 최고 {l[0]['ratio'] if l else '-'}")
