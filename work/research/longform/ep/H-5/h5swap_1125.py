# H-5 제목·썸네일 교체(youtube-loop 11/24 05:02 지시 ③, copywriter 11/24 18:58·15:14 1초 시험 통과) — 채팅 세션이 한 번 돌린다.
# 11/25 14:4x 무인 PD 회차에서는 자동 모드 권한이 거부해 돌리지 못함. 설명·태그는 그대로 두고 제목·썸네일만 바꾼다.
# 실행: 저장소 맨 위에서  py -3.12 work/research/longform/ep/H-5/h5swap_1125.py
import sys
sys.path.insert(0, 'work')
import f2_coupang
from googleapiclient.http import MediaFileUpload

VID = 'tvCsLWDF814'
NEW = '송도 아파트 84㎡, 고점 대비 몇 %까지 돌아왔을까?'
PNG = 'work/research/longform/ep/H-5/thumb_h5_n6.png'

yt = f2_coupang.service()
v = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]
sn = v['snippet']
print('지금:', sn['title'], '|', v['status']['privacyStatus'])
if sn['title'] != NEW:
    body = {'id': VID, 'snippet': {'title': NEW, 'description': sn['description'], 'categoryId': sn['categoryId'],
                                   'tags': sn.get('tags', []), 'defaultLanguage': sn.get('defaultLanguage', 'ko')}}
    if sn.get('defaultAudioLanguage'):
        body['snippet']['defaultAudioLanguage'] = sn['defaultAudioLanguage']
    yt.videos().update(part='snippet', body=body).execute()
yt.thumbnails().set(videoId=VID, media_body=MediaFileUpload(PNG, mimetype='image/png')).execute()
after = yt.videos().list(part='snippet', id=VID).execute()['items'][0]['snippet']
print('뒤:', after['title'], '| 태그', len(after.get('tags', [])), '| 설명 같음', after['description'] == sn['description'])
print('교체 시각을 loop/xc36.md·h5-diagnosis-1124.md에 적을 것')
