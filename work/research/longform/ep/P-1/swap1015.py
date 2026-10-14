import sys, os, json, difflib
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work'; sys.path.insert(0, W)
import f2_coupang, ytplaceholder
from googleapiclient.http import MediaFileUpload
EP = W + '/research/longform/ep/P-1'; VID = 'vsL7mojDW7w'
m = json.load(open(EP + '/meta.json', encoding='utf-8'))
yt = f2_coupang.service()
cur = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]
sn = cur['snippet']
json.dump(cur, open(EP + '/swap1015_before.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
title, desc = [x.replace('<', '＜').replace('>', '＞') for x in (m['title'], m['desc'])]
desc = desc.replace('VIDEOID', VID)
print('placeholders', ytplaceholder.find(title + '\n' + desc))
print('title', sn['title'], '->', title)
print('\n'.join(l for l in difflib.unified_diff(sn['description'].splitlines(), desc.splitlines(), lineterm='', n=0)))
if sys.argv[1:] == ['apply']:
    body = {'id': VID, 'snippet': {'title': title[:100], 'description': desc[:5000], 'tags': m['tags'], 'categoryId': '27', 'defaultLanguage': 'ko', 'defaultAudioLanguage': 'ko'}}
    yt.videos().update(part='snippet', body=body).execute()
    yt.thumbnails().set(videoId=VID, media_body=MediaFileUpload(EP + '/thumb_p4e.png')).execute()
    after = yt.videos().list(part='snippet,status', id=VID).execute()['items'][0]
    json.dump(after, open(EP + '/swap1015_after.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('AFTER', after['snippet']['title'], after['status'].get('privacyStatus'), after['status'].get('publishAt'), after['snippet']['tags'], after['snippet']['description'] == desc[:5000], list(after['snippet']['thumbnails']))
