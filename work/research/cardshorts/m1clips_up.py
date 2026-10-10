# M-1 쇼츠 예약 업로드 — cardshorts/<편>/upload.json + review.md '판정: 통과' 줄이 있어야 올린다.
#   py -3.12 work/research/cardshorts/m1clips_up.py <편이름>            # videos.insert(private + publishAt) → videos.list로 확인 → log.jsonl 한 줄
#   py -3.12 work/research/cardshorts/m1clips_up.py <편이름> --check [--fix]   # 올린 영상 상태만 다시 본다(--fix: AI 합성 표시 비었으면 다시 씀)
import os, sys, json, re, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
REPO = os.path.dirname(WORK)
sys.path.insert(0, WORK)
import ytupload, aitell, ytplaceholder

KST = datetime.timezone(datetime.timedelta(hours=9))


def show(yt, vid):
    v = yt.videos().list(part='snippet,status,contentDetails', id=vid).execute()['items'][0]
    st, sn = v['status'], v['snippet']
    keys = ['uploadStatus', 'privacyStatus', 'publishAt', 'embeddable', 'publicStatsViewable', 'selfDeclaredMadeForKids', 'madeForKids', 'containsSyntheticMedia', 'license']
    print('확인 videos.list:', {k: st.get(k) for k in keys})
    print('  snippet:', {'title': sn['title'], 'categoryId': sn.get('categoryId'), 'defaultLanguage': sn.get('defaultLanguage'), 'defaultAudioLanguage': sn.get('defaultAudioLanguage')},
          '| 길이', v['contentDetails'].get('duration'))
    return v


STATUS_KEEP = ('privacyStatus', 'publishAt', 'embeddable', 'publicStatsViewable', 'selfDeclaredMadeForKids', 'license')


def fix_synth(vid, up):
    """AI 합성 표시(containsSyntheticMedia)를 force-ssl 토큰 videos.update로 한 번 더 쓰고, 응답에 True가 돌아오는지 본다.
    실측 10/10 aYCWFSzynJI: insert 본문에 True를 넣어도 videos.list는 이 필드를 아예 돌려주지 않는다(롱폼 eTjVs1vDTwg도 같음).
    update 응답은 True를 돌려준다 → 확인 근거는 update 응답. 아직 비공개(예약) 영상만 — publishAt·privacyStatus를 그대로 함께 보낸다."""
    import f2_coupang
    yt2 = f2_coupang.service()
    st = yt2.videos().list(part='status', id=vid).execute()['items'][0]['status']
    if st.get('privacyStatus') != 'private': print('고치지 않는다: 이미 공개된 영상', st.get('privacyStatus')); return
    body = {k: st[k] for k in STATUS_KEEP if k in st}
    body.update(privacyStatus='private', publishAt=up['publishAt'], containsSyntheticMedia=True)
    r = yt2.videos().update(part='status', body={'id': vid, 'status': body}).execute()
    echo = r['status'].get('containsSyntheticMedia')
    print('videos.update 응답 containsSyntheticMedia =', echo, '| publishAt', r['status'].get('publishAt'), '| privacy', r['status'].get('privacyStatus'))
    return echo


def main(name, check_only=False):
    d = os.path.join(HERE, name); up = json.load(open(os.path.join(d, 'upload.json'), encoding='utf-8'))
    yt = ytupload.service()
    if check_only:
        if not up.get('id'): print('아직 안 올림'); return 1
        v = show(yt, up['id'])
        if '--fix' in sys.argv: up['synth_update_echo'] = fix_synth(up['id'], up); v = show(yt, up['id'])
        up['status'] = {k: v['status'].get(k) for k in ('privacyStatus', 'publishAt', 'embeddable', 'publicStatsViewable', 'selfDeclaredMadeForKids')}
        json.dump(up, open(os.path.join(d, 'upload.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 0
    if up.get('id'): print('이미 올림:', up['id']); show(yt, up['id']); return 0
    rv = open(os.path.join(d, 'review.md'), encoding='utf-8').read() if os.path.exists(os.path.join(d, 'review.md')) else ''
    if not re.search(r'^판정: 통과', rv, re.M): print('올리지 않는다: review.md에 "판정: 통과" 줄 없음'); return 3
    pub = datetime.datetime.fromisoformat(up['publishAt'])
    if pub <= datetime.datetime.now(KST) + datetime.timedelta(minutes=15): print('올리지 않는다: publishAt이 15분 안이거나 지났다', up['publishAt']); return 4
    title, desc = up['title'], up['description']
    if not desc.splitlines()[0].rstrip().endswith('https://youtu.be/eTjVs1vDTwg'): print('올리지 않는다: 설명 첫 줄에 롱폼 링크 없음'); return 5
    if '#shorts' not in title: print('올리지 않는다: 제목에 #shorts 없음'); return 5
    ok, msg, hits = aitell.gate_text(re.sub(r'https?://\S+', ' ', title + '\n\n' + desc), False)
    if not ok: aitell.refuse(msg, hits); return 6
    print(msg)
    if ytplaceholder.find(title + '\n' + desc): print('올리지 않는다: 자리표시자', ytplaceholder.find(title + '\n' + desc)); return 7
    mp4 = os.path.join(REPO, up['mp4'])
    from googleapiclient.http import MediaFileUpload
    body = {'snippet': {'title': title[:100], 'description': desc[:5000], 'tags': [t.strip() for t in up['tags'].split(',') if t.strip()],
                        'categoryId': '27', 'defaultLanguage': 'ko', 'defaultAudioLanguage': 'ko'},
            'status': {'privacyStatus': 'private', 'publishAt': up['publishAt'], 'embeddable': True, 'publicStatsViewable': True,
                       'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}
    req = yt.videos().insert(part='snippet,status', body=body, media_body=MediaFileUpload(mp4, chunksize=8 * 1024 * 1024, resumable=True))
    res = None
    while res is None:
        status, res = req.next_chunk()
        if status: print(f'업로드 {int(status.progress() * 100)}%', flush=True)
    vid = res['id']; print('완료 https://youtu.be/' + vid)
    print('insert 응답 status:', res.get('status'))
    up['synth_insert_echo'] = res.get('status', {}).get('containsSyntheticMedia')
    up['synth_update_echo'] = fix_synth(vid, up)
    v = show(yt, vid)
    up.update(id=vid, uploaded_at=datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S'), status={k: v['status'].get(k) for k in ('privacyStatus', 'publishAt', 'embeddable', 'publicStatsViewable', 'selfDeclaredMadeForKids')})
    json.dump(up, open(os.path.join(d, 'upload.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    props = json.load(open(os.path.join(WORK, 'video', name + '.json'), encoding='utf-8'))
    seed = hashlib.md5('|'.join(l['audio'] for s in props['scenes'] for l in s['lines']).encode()).hexdigest()
    row = {'at': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 'id': vid, 'title': title, 'audio_seed': seed, 'layout': 'm1clip', 'music': False,
           'facts': os.path.join(WORK, 'research', 'longform', 'ep', 'M-1', 'facts.txt').replace('\\', '/'), 'spec': f'work/video/{name}.json',
           'd7_views': None, 'd7_subs': None, 'publishAt': up['publishAt'], 'from_long': 'eTjVs1vDTwg', 'voice': 'M-1 voice.json wav 재사용(새 녹음 없음)'}
    with open(os.path.join(HERE, 'log.jsonl'), 'a', encoding='utf-8') as f: f.write(json.dumps(row, ensure_ascii=False) + '\n')
    print('log.jsonl 한 줄 추가')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], '--check' in sys.argv[2:]))
