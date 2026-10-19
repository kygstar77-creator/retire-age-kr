# 갈래 C(10/19): 잘되는 채널 롱폼 제목 실측 — 채널마다 최근 롱폼 최대 50편(공개 7일 지남, 180초 초과, 라이브 아님)
#   python titles.py → titles.json(행) + titles_stats.json(묶음)
#   채널 = textpos-1019 collect.py의 18곳(같은 목록) + 우리 채널. 조회는 그 채널 중앙값 대비(rel)로 본다(채널 크기 착시 제거).
import sys, os, re, json, datetime, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK); sys.path.insert(0, os.path.join(WORK, 'research', 'visual', 'textpos-1019'))
import ytupload
from collect import MAIN, SMALL, sec
CH = dict(MAIN); CH.update({k: SMALL[k] for k in ['오십의 경제지도', '연금왕 배형', '투자360', '자람들']})
OURS = {'파이어맵(우리)': 'UCV3ZcSho5Z1i8k_FAiKPlVg'}

def feats(t):
    nums = re.findall(r'\d[\d,.]*', t)
    return dict(len=len(t), len_nospace=len(t.replace(' ', '')), words=len(t.split()), nums=len(nums),
                q='?' in t, pipe='|' in t, quote=bool(re.search(r'["“”\'‘’]', t)), bracket=bool(re.search(r'[\[\(【]', t)),
                hashtag='#' in t, vs=bool(re.search(r'(?i)\bvs\b', t)), ellipsis=('...' in t or '…' in t),
                you=bool(re.search(r'(당신|여러분|내 |나는|우리)', t)), emph=bool(re.search(r'(충격|경고|절대|무조건|당장|폭락|폭등|역대급|결국)', t)),
                ends_da=bool(re.search(r'다[.!]*$', t.strip())))

def pull(yt, name, cid, n=50):
    ch = yt.channels().list(part='statistics,contentDetails', id=cid).execute()['items'][0]
    subs = int(ch['statistics'].get('subscriberCount', 0)); up = ch['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    while len(ids) < 150:
        r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [x['contentDetails']['videoId'] for x in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    out, now = [], datetime.datetime.now(datetime.timezone.utc)
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part='snippet,statistics,contentDetails,liveStreamingDetails', id=','.join(ids[i:i+50])).execute()['items']:
            s = sec(v['contentDetails'].get('duration'))
            if s <= 180 or 'liveStreamingDetails' in v: continue
            pub = datetime.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00'))
            if (now - pub).days < 7: continue
            out.append(dict(channel=name, id=v['id'], title=v['snippet']['title'], published=v['snippet']['publishedAt'][:10],
                            views=int(v['statistics'].get('viewCount', 0)), subs=subs))
    out.sort(key=lambda r: r['published'], reverse=True); out = out[:n]
    if out:
        med = st.median([r['views'] for r in out])
        for r in out: r['rel'] = round(r['views'] / max(med, 1), 3); r.update(feats(r['title']))
    return out

if __name__ == '__main__':
    yt = ytupload.service(); rows = []
    for name, cid in list(CH.items()) + list(OURS.items()):
        rs = pull(yt, name, cid); rows += rs; print(name, len(rs))
    json.dump(rows, open(os.path.join(HERE, 'titles.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    comp = [r for r in rows if r['channel'] not in OURS]
    def q(xs, p): xs = sorted(xs); return xs[int(p * (len(xs) - 1))]
    S = dict(n=len(comp), channels=len({r['channel'] for r in comp}), collected=datetime.datetime.now().isoformat(timespec='minutes'))
    L = [r['len'] for r in comp]; S['len'] = dict(p10=q(L, .1), p25=q(L, .25), med=st.median(L), p75=q(L, .75), p90=q(L, .9), max=max(L))
    S['len_per_channel_med'] = {c: st.median([r['len'] for r in comp if r['channel'] == c]) for c in CH}
    top = [r for r in comp if r['rel'] >= 1.5]; bot = [r for r in comp if r['rel'] <= 0.67]
    S['top_n'], S['bot_n'] = len(top), len(bot)
    keys = ['q', 'pipe', 'quote', 'bracket', 'hashtag', 'vs', 'ellipsis', 'you', 'emph', 'ends_da']
    S['share_all'] = {k: round(sum(r[k] for r in comp) / len(comp), 3) for k in keys}
    S['share_top'] = {k: round(sum(r[k] for r in top) / max(1, len(top)), 3) for k in keys}
    S['share_bot'] = {k: round(sum(r[k] for r in bot) / max(1, len(bot)), 3) for k in keys}
    S['nums_dist_all'] = dict(collections.Counter(min(r['nums'], 3) for r in comp))
    S['has_num_all'] = round(sum(r['nums'] > 0 for r in comp) / len(comp), 3)
    S['has_num_top'] = round(sum(r['nums'] > 0 for r in top) / max(1, len(top)), 3)
    S['has_num_bot'] = round(sum(r['nums'] > 0 for r in bot) / max(1, len(bot)), 3)
    S['len_top_med'] = st.median([r['len'] for r in top]) if top else None
    S['len_bot_med'] = st.median([r['len'] for r in bot]) if bot else None
    # 길이 구간별 rel 중앙값
    bins = [(0, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 101)]
    S['rel_by_len'] = {f'{a}-{b - 1}': dict(n=len(xs), rel_med=round(st.median(xs), 2)) for a, b in bins
                       for xs in [[r['rel'] for r in comp if a <= r['len'] < b]] if xs}
    S['rel_by_nums'] = {str(k): dict(n=len(xs), rel_med=round(st.median(xs), 2)) for k in range(4)
                        for xs in [[r['rel'] for r in comp if min(r['nums'], 3) == k]] if xs}
    S['rel_by_q'] = {str(k): dict(n=len(xs), rel_med=round(st.median(xs), 2)) for k in (True, False)
                     for xs in [[r['rel'] for r in comp if r['q'] == k]] if xs}
    ours = [r for r in rows if r['channel'] in OURS]
    S['ours'] = dict(n=len(ours), len_med=st.median([r['len'] for r in ours]) if ours else None,
                     has_num=round(sum(r['nums'] > 0 for r in ours) / max(1, len(ours)), 3), q=round(sum(r['q'] for r in ours) / max(1, len(ours)), 3),
                     pipe=round(sum(r['pipe'] for r in ours) / max(1, len(ours)), 3))
    json.dump(S, open(os.path.join(HERE, 'titles_stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(S, ensure_ascii=False, indent=1))
