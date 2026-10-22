# B-45(0초 글자) 고친 판으로 예약 쇼츠 바꾸기 — 10/22 PD. motion이 만든 video/out/b45/<편>_b45_ds.mp4(소리=올린 _ds 그대로, 0초 프레임만 다름)를
#   같은 제목·설명·태그·publishAt으로 새로 올리고, 새 판 예약이 확인되면 옛 예약 영상은 지우지 않고 publishAt만 빼서 비공개로 둔다(c1clips_up.py --replace와 같은 방식).
#   py -3.12 work/research/cardshorts/b45swap.py <편이름>
import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.normpath(os.path.join(HERE, '..', '..')); REPO = os.path.dirname(WORK)
sys.path.insert(0, WORK); sys.path.insert(0, HERE)
import ytupload, aitell, ytplaceholder, safezone, bgcheck, emptyscan, re
from c1clips_up import show, fix_synth, unschedule, KST

def main(name):
    d = os.path.join(HERE, name); p = os.path.join(d, 'upload.json'); up = json.load(open(p, encoding='utf-8'))
    old = up['id']; mp4 = os.path.join(REPO, 'work', 'video', 'out', 'b45', f'{name}_b45_ds.mp4')
    if not os.path.exists(mp4): print('없음', mp4); return 2
    pub = datetime.datetime.fromisoformat(up['publishAt'])
    if pub <= datetime.datetime.now(KST) + datetime.timedelta(minutes=30): print('올리지 않는다: publishAt 30분 안', up['publishAt']); return 4
    yt = ytupload.service()
    st = yt.videos().list(part='status', id=old).execute()['items'][0]['status']
    if st.get('privacyStatus') != 'private' or not st.get('publishAt'): print('옛 영상 상태가 예약이 아님 — 멈춤', st); return 3
    title, desc = up['title'], up['description']
    ok, msg, hits = aitell.gate_text(re.sub(r'https?://\S+', ' ', title + '\n\n' + desc), False); print(msg)
    if not ok: return 6
    if ytplaceholder.find(title + '\n' + desc): print('자리표시자'); return 7
    for g in (safezone.gate, bgcheck.gate, emptyscan.gate_fade0):
        okg, m = g(mp4); print(m)
        if not okg: print('올리지 않는다:', g.__module__); return 12
    from googleapiclient.http import MediaFileUpload
    body = {'snippet': {'title': title[:100], 'description': desc[:5000], 'tags': [t.strip() for t in up['tags'].split(',') if t.strip()],
                        'categoryId': '27', 'defaultLanguage': 'ko', 'defaultAudioLanguage': 'ko'},
            'status': {'privacyStatus': 'private', 'publishAt': up['publishAt'], 'embeddable': True, 'publicStatsViewable': True,
                       'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}
    req = yt.videos().insert(part='snippet,status', body=body, media_body=MediaFileUpload(mp4, chunksize=8 * 1024 * 1024, resumable=True))
    res = None
    while res is None: _, res = req.next_chunk()
    vid = res['id']; print('완료 https://youtu.be/' + vid)
    up['synth_update_echo'] = fix_synth(vid, up)
    v = show(yt, vid)
    if v['status'].get('publishAt') is None or v['status'].get('privacyStatus') != 'private': print('새 판 예약 확인 실패 — 옛 예약 그대로'); return 8
    back = unschedule(old)
    up.setdefault('replaced', []).append({'id': old, 'unscheduled_at': datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S'), 'why': 'B-45 0초 글자(motion 10/22 12:02)',
                                          'status_after': {k: (back or {}).get(k) for k in ('privacyStatus', 'publishAt')}})
    up.update(id=vid, mp4=f'work/video/out/b45/{name}_b45_ds.mp4', uploaded_at=datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S'),
              status={k: v['status'].get(k) for k in ('privacyStatus', 'publishAt', 'embeddable', 'publicStatsViewable', 'selfDeclaredMadeForKids')})
    json.dump(up, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('RESULT', name, old, '→', vid, up['publishAt'])
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
