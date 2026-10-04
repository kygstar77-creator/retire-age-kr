# 설명란 자리표시자 검사·치환(2026-10-05, audit·firemap-loop 요청: DBCBWToNFCs가 utm_campaign=VIDEOID로 공개됨)
#   py -3.12 work/ytplaceholder.py scan    # 채널 전 영상(공개·예약·일부공개) 설명란에서 자리표시자 찾기
#   py -3.12 work/ytplaceholder.py fix     # VIDEOID → 그 영상 ID로 바꿔 videos.update(원본 research/longform/loop/placeholder_before.json)
# 다른 자리표시자({…}·TODO)는 무엇으로 바꿀지 기계가 모르니 찾기만 하고 보고한다.
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ytupload
PAT = re.compile(r'VIDEOID|\{[A-Za-z_가-힣]+\}|TODO|XXX')
BEFORE = os.path.join(HERE, 'research', 'longform', 'loop', 'placeholder_before.json')

def find(s): return sorted(set(PAT.findall(s or '')))

def all_videos(yt):
    ch = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]
    up = ch['contentDetails']['relatedPlaylists']['uploads']; ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i['contentDetails']['videoId'] for i in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    out = []
    for k in range(0, len(ids), 50):
        out += yt.videos().list(part='snippet,status', id=','.join(ids[k:k+50])).execute()['items']
    return out

def main(mode):
    yt = ytupload.service(); vids = all_videos(yt); bad = []
    for v in vids:
        if v['status']['privacyStatus'] == 'private' and not v['status'].get('publishAt'): continue  # 옛 비공개 틀은 손대지 않음
        h = find(v['snippet']['description']) + [f'제목:{x}' for x in find(v['snippet']['title'])]
        if h: bad.append(v); print(v['id'], v['status']['privacyStatus'], h, v['snippet']['title'][:40])
    print(f'검사 {len(vids)}편 · 걸림 {len(bad)}편')
    if mode != 'fix' or not bad: return
    import f2_coupang
    w = f2_coupang.service()
    json.dump([{'id': v['id'], 'description': v['snippet']['description']} for v in bad], open(BEFORE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for v in bad:
        sn = v['snippet']; d = sn['description']
        if 'VIDEOID' not in d: print(v['id'], '건너뜀: VIDEOID 아닌 자리표시자 — 사람이 정할 것'); continue
        body = {'id': v['id'], 'snippet': {'title': sn['title'], 'description': d.replace('VIDEOID', v['id']), 'categoryId': sn['categoryId'],
                'tags': sn.get('tags', []), 'defaultLanguage': sn.get('defaultLanguage', 'ko'), 'defaultAudioLanguage': 'ko'}}
        w.videos().update(part='snippet', body=body).execute()
        back = yt.videos().list(part='snippet', id=v['id']).execute()['items'][0]['snippet']['description']
        print(v['id'], '고침' if 'VIDEOID' not in back else '실패', '남은 자리표시자:', find(back))

if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else 'scan')
