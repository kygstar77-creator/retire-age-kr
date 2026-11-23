# 예약 쇼츠 칸 옮기기 (11/24 PD, youtube-loop 00:49 지시: k1s_recover를 11/25 19:20에, 그 자리 영상은 뒤 칸으로)
#   py -3.12 work/research/cardshorts/reschedule.py <편이름> <새 publishAt ISO>   # 아직 비공개 예약인 영상만, status 전체를 그대로 두고 publishAt만 바꾼다
import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..')))
import f2_coupang
from w1g1clips_up import STATUS_KEEP
KST = datetime.timezone(datetime.timedelta(hours=9))
name, new = sys.argv[1], sys.argv[2]
p = os.path.join(HERE, name, 'upload.json'); up = json.load(open(p, encoding='utf-8'))
if datetime.datetime.fromisoformat(new) <= datetime.datetime.now(KST) + datetime.timedelta(hours=1): sys.exit('옮기지 않는다: 새 시각이 1시간 안이거나 지났다')
yt = f2_coupang.service(); vid = up['id']
st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
if st.get('privacyStatus') != 'private' or not st.get('publishAt'): sys.exit(f'옮기지 않는다: 예약 비공개가 아님 {st.get("privacyStatus")} {st.get("publishAt")}')
old = st['publishAt']
body = {k: st[k] for k in STATUS_KEEP if k in st}; body.update(privacyStatus='private', publishAt=new, containsSyntheticMedia=True)
r = yt.videos().update(part='status', body={'id': vid, 'status': body}).execute()['status']
back = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
print(vid, old, '→', back.get('publishAt'), back.get('privacyStatus'), '| 응답 synth', r.get('containsSyntheticMedia'))
up.setdefault('rescheduled', []).append({'from': old, 'to': new, 'at': datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')})
up['publishAt'] = new; up['status'] = {k: back.get(k) for k in ('privacyStatus', 'publishAt', 'embeddable', 'publicStatsViewable', 'selfDeclaredMadeForKids')}
json.dump(up, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
lp = os.path.join(HERE, 'log.jsonl'); rows = open(lp, encoding='utf-8').read().splitlines()
for i, ln in enumerate(rows):
    try: o = json.loads(ln)
    except Exception: continue
    if o.get('id') == vid: o['publishAt'] = new; rows[i] = json.dumps(o, ensure_ascii=False)
open(lp, 'w', encoding='utf-8', newline='\n').write('\n'.join(rows) + '\n')
