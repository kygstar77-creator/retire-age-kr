"""D-1 설명란 카페 링크를 짝 글(/206)로. snippet 통째로 받아 description만 바꿔 보낸다(defaultAudioLanguage 유지). 백업: longform/loop/desc_before_<id>.json"""
import sys, json, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import f2_coupang
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'research', 'longform', 'loop')
vid = 'GMc2Rd1-JYA'; NEW = 'https://cafe.naver.com/firemap/206'
yt = f2_coupang.service()
sn = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
json.dump(sn, open(os.path.join(D, f'desc_before_{vid}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
d = sn['description']
pat = re.compile(r'https?://cafe\.naver\.com/firemap(?![/\w])')
print('매치', len(pat.findall(d)), '| 이미 /206:', NEW in d, '| audio:', sn.get('defaultAudioLanguage'))
for l in d.splitlines():
    if 'cafe.naver.com' in l: print('줄:', l)
if '--go' in sys.argv:
    nd = pat.sub(NEW, d)
    new = {k: sn[k] for k in ('title','categoryId') if k in sn}; new['description'] = nd
    for k in ('tags','defaultLanguage','defaultAudioLanguage'):
        if k in sn: new[k] = sn[k]
    yt.videos().update(part='snippet', body={'id': vid, 'snippet': new}).execute()
    c = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
    ok = all(c.get(k) == sn.get(k) for k in ('title','categoryId','tags','defaultLanguage','defaultAudioLanguage')) and c['description'] == nd
    print('되읽기', 'OK' if ok else '불일치', '| audio', c.get('defaultAudioLanguage'), '| 설명 길이', len(d), '->', len(c['description']))
