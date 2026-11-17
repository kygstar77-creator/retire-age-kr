# 11/17 PD(회의 지시 ④): N-3 설명란 카페 대문 주소 → 짝 글 n3pair1116 #440(10:06 발행, write verify OK). 다른 줄 그대로.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
sys.path.insert(0, W)
import ytupload, f2_coupang
VID = '6x35E3vg650'
OLD = '전체 표와 계산 근거(카페): https://cafe.naver.com/firemap\n'
NEW = '전체 표와 계산 근거(카페): https://cafe.naver.com/firemap/440\n'
yt = ytupload.service()
sn = yt.videos().list(part='snippet', id=VID).execute()['items'][0]['snippet']
if NEW in sn['description']: print('이미 있음'); sys.exit()
assert sn['description'].count(OLD) == 1, '대문 줄 못 찾음'
json.dump(sn, open(os.path.join(os.path.dirname(__file__), 'desc_before_1117.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
live = sn['description'].replace(OLD, NEW)
snip = {k: sn[k] for k in ('title', 'categoryId', 'tags', 'defaultLanguage', 'defaultAudioLanguage') if k in sn}
snip['description'] = live
if '--dry' in sys.argv: print(live[:400]); sys.exit()
f2_coupang.service().videos().update(part='snippet', body={'id': VID, 'snippet': snip}).execute()
back = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]
print('설명란', '바뀜' if NEW in back['snippet']['description'] else '실패', '·', back['status'].get('privacyStatus'), '· 제목 그대로' if back['snippet']['title'] == sn['title'] else '· 제목 달라짐!')
