# 공개 중 영상 썸네일·제목 받기(oembed, 키 없음)
import json, urllib.request, os, sys
sys.stdout.reconfigure(encoding='utf-8')
IDS = ['P8Papm8Yxpw','KiHLbeioWNg','scV67BQvC4Q','XzMCiAwQhAo','zhTjJwy1mwQ','5_3ZC8ma5rw','JVTYZ208hgw','wwfFszPl06g','gSKsQWjTabo','E8UeCBNiVZE','LODYqWHht3s','uE1R8g2vH8Q','xDN8mv2ohps','yduGnS0sIm8']
VIEWS = [359,172,149,22,15,4,4,2,2,1,1,1,1,1]
os.makedirs('pub', exist_ok=True); out = []
for i, v in zip(IDS, VIEWS):
    try:
        t = json.load(urllib.request.urlopen(f'https://www.youtube.com/oembed?url=https://youtu.be/{i}&format=json', timeout=20))['title']
    except Exception as e: t = f'(oembed 실패 {e})'
    for q in ('maxresdefault', 'hqdefault'):
        try:
            b = urllib.request.urlopen(f'https://i.ytimg.com/vi/{i}/{q}.jpg', timeout=20).read()
            if len(b) > 3000: open(f'pub/{i}.jpg', 'wb').write(b); break
        except Exception: pass
    out.append({'id': i, 'views28': v, 'title': t}); print(i, v, t)
json.dump(out, open('pub.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
