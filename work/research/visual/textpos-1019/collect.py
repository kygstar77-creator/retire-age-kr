# 10/19 썸네일 글자 위치 조사 — 경쟁 채널 최근 롱폼 5편씩 썸네일·조회·구독 수집 (읽기 전용 API)
#   python work/research/visual/textpos-1019/collect.py [--probe]
#   --probe: 작은 채널 후보의 최근 롱폼 조회÷구독 중앙값만 출력(고르기용)
import sys, os, re, json, datetime, statistics, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))  # work/
import ytupload
SRC = os.path.join(HERE, 'src')
MAIN = {  # 잘되는 큰·중간 채널
 '수페TV': 'UCfnqgWlC5IvJEAPTmyjaixA', '소수몽키': 'UCC3yfxS5qC6PCwDzetUuEWg',
 '월급쟁이부자들TV': 'UCDSj40X9FFUAnx1nv7gQhcA', '김작가TV': 'UCvil4OAt-zShzkKHsg9EQAw',
 '부읽남TV': 'UC2QeHNJFfuQWB4cy3M-745g', '박곰희TV': 'UCr7XsrSrvAn_WcU4kF99bbQ',
 '똑재TV': 'UCmshc9VpICv4oPyjMK3Vk_w', '머니인사이드': 'UCxfko2YOD6DODYRGzeOPhIQ',
 '815머니톡': 'UCCG6BEYjfQMGzypJw2EJCDQ', '슈카월드': 'UCsJ6RuBiTVWRX156FVbeaGg',
 '은퇴머니': 'UCQrlX5mzcTICHZC1BMVKwhQ', '싱글파이어': 'UC5CyCSvCdoEP-VgQmFq3iww',
 '김범곤의 연금수업': 'UCiIp3SArhmQjBsr_tt6Jq9A', 'ETF 아는 형': 'UCIt_hQy30blHrVAS7QLTyTg',
}
SMALL = {  # 작은 채널 후보(조회÷구독 높은 곳을 --probe로 고른다)
 '노후 관리사무소': 'UC02kXDUIhuSqZYb191FneJA', '연금왕 배형': 'UCV5OaRenLVz74JYlTzg3G-Q',
 '실거래로그': 'UCuoNViN-aL6EwUOeEf_w7YQ', '경제명탐정': 'UC1eyYJRpM_g5WBp60mmRwCQ',
 '부티플': 'UCriq8I8GEESkQq0svX19oCw', '시니어노후': 'UCS_vefzRwq-vhxcswl2zMWw',
 '노후 복지번역기': 'UCnV7DC5le_85T5mifmWKJug', '자람들': 'UC5UFGiELUPSTvFfMGEUxeiQ',
 '투자360': 'UCEJIw_FUvkxK7ZoiejSj7HA', '경제해적단': 'UCn49LSg2JSP-9rXV5G2kt4A',
 '너와 나의 경제학교': 'UCF9cuJUvzJyVnoDke5clbHw', '오십의 경제지도': 'UCqcbPnnY1jxklrdTwLH0qqA',
 '노후머니가이드': 'UCsavGn5Fg1bOthryzEATA1w', '은퇴선배': 'UCdjlmN3mK2PCasVfDNhnF1w',
 '펜셔니어': 'UCipn775CE6-x5VoHUtRza7w', '연금박사 이영주': 'UCD9mxN8o9qLei1MbzroeP_A',
}
def sec(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    if not m: return 0
    a = [int(x or 0) for x in m.groups()]; return a[0]*86400+a[1]*3600+a[2]*60+a[3]

def latest_long(yt, cid, n=5):
    ch = yt.channels().list(part='snippet,statistics,contentDetails', id=cid).execute()['items'][0]
    subs = int(ch['statistics'].get('subscriberCount', 0))
    up = ch['contentDetails']['relatedPlaylists']['uploads']
    ids = [x['contentDetails']['videoId'] for x in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute()['items']]
    vs = yt.videos().list(part='snippet,statistics,contentDetails,liveStreamingDetails', id=','.join(ids)).execute()['items']
    vs.sort(key=lambda v: v['snippet']['publishedAt'], reverse=True)
    out = []
    now = datetime.datetime.now(datetime.timezone.utc)
    for v in vs:
        s = sec(v['contentDetails'].get('duration'))
        if s <= 180 or 'liveStreamingDetails' in v: continue  # 쇼츠·라이브 제외
        pub = datetime.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00'))
        age = (now - pub).total_seconds() / 86400
        if age < 3: continue  # 3일 안 된 편은 조회가 덜 쌓여 뺀다
        views = int(v['statistics'].get('viewCount', 0))
        out.append(dict(id=v['id'], title=v['snippet']['title'], published=v['snippet']['publishedAt'][:10],
                        age_days=round(age, 1), sec=s, views=views, subs=subs, ratio=round(views / max(subs, 1), 3),
                        thumbs=list(v['snippet'].get('thumbnails', {}).keys())))
        if len(out) >= n: break
    return ch['snippet']['title'], subs, out

def dl(vid):
    for q in ('maxresdefault', 'hqdefault'):
        p = os.path.join(SRC, f'{vid}.jpg')
        try:
            data = urllib.request.urlopen(f'https://i.ytimg.com/vi/{vid}/{q}.jpg', timeout=20).read()
            if len(data) > 5000:
                open(p, 'wb').write(data); return q
        except Exception: pass
    return None

if __name__ == '__main__':
    yt = ytupload.service()
    if '--probe' in sys.argv:
        for name, cid in SMALL.items():
            try:
                t, subs, vs = latest_long(yt, cid)
                r = [v['ratio'] for v in vs]
                print(f'{name}\t{subs}\t{len(vs)}\t{statistics.median(r) if r else 0:.2f}\t{[v["published"] for v in vs][:2]}')
            except Exception as e: print(name, 'ERR', e)
        sys.exit()
    picks = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    chans = dict(MAIN); chans.update({k: SMALL[k] for k in picks})
    os.makedirs(SRC, exist_ok=True)
    rows = []
    for name, cid in chans.items():
        t, subs, vs = latest_long(yt, cid)
        for v in vs:
            v['channel'] = name; v['channel_title'] = t; v['group'] = 'small' if name in SMALL else 'main'
            v['img'] = dl(v['id'])
            rows.append(v)
        print(name, subs, len(vs))
    json.dump(dict(collected=datetime.datetime.now().isoformat(timespec='minutes'), rows=rows),
              open(os.path.join(HERE, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('total', len(rows))
