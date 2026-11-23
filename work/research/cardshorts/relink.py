# 롱폼 교체 뒤 예약 쇼츠 설명란의 롱폼 주소 바꾸기 (11/24 PD — KOSPI-1 새 판 올림)
#   py -3.12 work/research/cardshorts/relink.py <편이름> <옛 롱폼 videoId> <새 롱폼 videoId>
#   아직 비공개 예약인 쇼츠만. snippet은 제목·설명·태그·분류를 그대로 두고 설명의 옛 ID만 새 ID로 바꾼다. status는 건드리지 않는다.
import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..')))
import f2_coupang
KST = datetime.timezone(datetime.timedelta(hours=9))
name, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
p = os.path.join(HERE, name, 'upload.json'); up = json.load(open(p, encoding='utf-8'))
yt = f2_coupang.service(); vid = up['id']
it = yt.videos().list(part='snippet,status', id=vid).execute()['items'][0]
st, sn = it['status'], it['snippet']
if st.get('privacyStatus') != 'private' or not st.get('publishAt'): sys.exit(f'바꾸지 않는다: 예약 비공개가 아님 {st.get("privacyStatus")} {st.get("publishAt")}')
if old not in sn.get('description', ''): sys.exit('바꾸지 않는다: 설명에 옛 ID 없음')
body = {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage') if k in sn}
body['description'] = sn['description'].replace(old, new)
yt.videos().update(part='snippet', body={'id': vid, 'snippet': body}).execute()
back = yt.videos().list(part='snippet,status', id=vid).execute()['items'][0]
ok = new in back['snippet']['description'] and old not in back['snippet']['description']
print(vid, '설명 롱폼', old, '→', new, '확인' if ok else '실패', '| 상태', back['status'].get('privacyStatus'), back['status'].get('publishAt'))
up['from_long'] = new; up['description'] = up.get('description', '').replace(old, new)
up.setdefault('relinked', []).append({'from': old, 'to': new, 'at': datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')})
json.dump(up, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
