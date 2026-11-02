# 11/2 PD(editor 07:11 요청): 설명란 '배경 영상' 줄만 실제 렌더본 BG(de1jclip.py credits)로 — upload.json·YouTube 둘 다, 다른 줄 그대로
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, W)
import ytupload, f2_coupang
UP = os.path.join(os.path.dirname(__file__), 'upload.json')
u = json.load(open(UP, encoding='utf-8'))
cred = json.load(open(os.path.join(W, 'video', 'de1s_jepi.json'), encoding='utf-8'))['credits']
cred = re.sub(r'[\s⠀]+', ' ', cred.replace(' (Pexels License)', '')).strip()
line = 'Pexels(Pexels License) — ' + cred
new = re.sub(r'(?m)^배경 영상: .*$', '배경 영상: ' + line, u['description'])
assert new != u['description'] and new.count('배경 영상:') == 1
yt = ytupload.service()
sn = yt.videos().list(part='snippet', id=u['id']).execute()['items'][0]['snippet']
live = re.sub(r'(?m)^배경 영상: .*$', '배경 영상: ' + line, sn['description'])
assert live.count('배경 영상:') == 1
body = {'id': u['id'], 'snippet': {'title': sn['title'], 'description': live, 'categoryId': sn['categoryId'], 'tags': sn.get('tags', []),
                                   'defaultLanguage': sn.get('defaultLanguage', 'ko')}}
if '--dry' in sys.argv: print(live); sys.exit()
f2_coupang.service().videos().update(part='snippet', body=body).execute()
back = yt.videos().list(part='snippet,status', id=u['id']).execute()['items'][0]
ok = ('배경 영상: ' + line) in back['snippet']['description']
print('YouTube 설명란', '바뀜' if ok else '실패', '·', back['status'].get('privacyStatus'), back['status'].get('publishAt'))
if ok:
    u['description_prev_bg'] = re.search(r'(?m)^배경 영상: .*$', u['description']).group(0)
    u['description'] = new
    json.dump(u, open(UP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('upload.json 바꿈:', line)
