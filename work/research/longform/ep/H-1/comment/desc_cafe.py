# H-1 설명 '…전체 표(카페)' 줄의 카페 대문 주소를 짝 글 주소로 바꾼다(PD 10/15, R-1 desc_cafe.py 그대로).
#   py -3.12 work/research/longform/ep/H-1/comment/desc_cafe.py <카페 글 주소>
# videos.update는 snippet 전체 필드를 같이 보낸다(교훈 18) · 쓰기 토큰은 f2_coupang.service(ytupload 토큰은 403) · 되읽기 확인.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
WORK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
sys.path.insert(0, WORK)
import f2_coupang
VID = 'rVg0pQVo_wk'
url = sys.argv[1]; assert url.startswith('https://cafe.naver.com/firemap/'), url
yt = f2_coupang.service()
v = yt.videos().list(part='snippet', id=VID).execute()['items'][0]; sn = v['snippet']
json.dump(sn, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'desc_before.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
old = '걸어서 몇 m인지 전체 표(카페): https://cafe.naver.com/firemap'
assert [l.endswith(old) for l in sn['description'].splitlines()].count(True) == 1, '바꿀 줄 없음(이미 바뀜?)'
desc = '\n'.join(l[:-len(old)] + f'걸어서 몇 m인지 전체 표(카페): {url}' if l.endswith(old) else l for l in sn['description'].split('\n'))
body = {'id': VID, 'snippet': {'title': sn['title'], 'description': desc, 'tags': sn.get('tags', []), 'categoryId': sn['categoryId'],
        'defaultLanguage': sn.get('defaultLanguage', 'ko'), 'defaultAudioLanguage': sn.get('defaultAudioLanguage', 'ko')}}
yt.videos().update(part='snippet', body=body).execute()
import time
for _ in range(4):   # 10/14: 되읽기가 몇 초 늦게 바뀐 값을 돌려줌
    back = yt.videos().list(part='snippet', id=VID).execute()['items'][0]['snippet']['description']
    if url in back: break
    time.sleep(5)
assert url in back, '되읽기 실패'
print('바뀜 —', [l for l in back.splitlines() if url in l][0])
