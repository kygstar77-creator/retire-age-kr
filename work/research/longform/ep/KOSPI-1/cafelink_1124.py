# KOSPI-1 설명란 카페 줄 대문 → 짝 글 #478 (11/24 PD, PD 지시 '설명란 {CAFE}에 그 글 주소'). 그 한 줄만 바꾼다. status 안 건드림.
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..')))
import f2_coupang
VID, OLD, NEW = 'bBoh8J1Ru_4', '크게 빠진 열다섯 번 전체 표(카페): https://cafe.naver.com/firemap\n', '크게 빠진 열다섯 번 전체 표(카페): https://cafe.naver.com/firemap/478\n'
yt = f2_coupang.service()
it = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]; sn = it['snippet']
d = sn['description'] + '\n'
assert d.count(OLD) == 1, ('카페 줄', d.count(OLD))
json.dump(it, open(os.path.join(HERE, 'desc_before_cafelink1124.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
body = {'id': VID, 'snippet': {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage') if k in sn}}
body['snippet']['description'] = d.replace(OLD, NEW)[:-1]
yt.videos().update(part='snippet', body=body).execute()
it2 = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]
print('바꿈', '/478' in it2['snippet']['description'], it2['status']['privacyStatus'], it2['status'].get('publishAt'), it2['snippet']['title'])
