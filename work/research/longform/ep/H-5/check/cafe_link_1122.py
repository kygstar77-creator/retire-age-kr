# 11/22 PD: H-5 tvCsLWDF814 설명란 카페 줄을 짝 글 #468 주소로(write 12:42 요청). 전 설명은 check/desc_before_1122.json
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/강영준/Documents/GitHub/retire-age-kr/work'; sys.path.insert(0, W)
import ytupload, f2_coupang
VID = 'tvCsLWDF814'; OLD = '단지 33곳 전체 표와 계산 근거(카페): https://cafe.naver.com/firemap\n'; NEW = '단지 33곳 전체 표와 계산 근거(카페): https://cafe.naver.com/firemap/468\n'
yt = ytupload.service(); v = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]; sn = v['snippet']; d = sn['description']
json.dump({'id': VID, 'description': d}, open(os.path.join(os.path.dirname(__file__), 'desc_before_1122.json'), 'w', encoding='utf-8'), ensure_ascii=False)
if OLD not in d: print('바꿀 줄 없음', '/468' in d); sys.exit()
body = {'id': VID, 'snippet': {'title': sn['title'], 'description': d.replace(OLD, NEW), 'categoryId': sn['categoryId'], 'tags': sn.get('tags', []),
        'defaultLanguage': sn.get('defaultLanguage', 'ko'), 'defaultAudioLanguage': 'ko'}}
f2_coupang.service().videos().update(part='snippet', body=body).execute()
b = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]
print('고침' if NEW in b['snippet']['description'] else '실패', b['status']['privacyStatus'], b['snippet']['title'])
