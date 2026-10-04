import sys, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytupload
yt = ytupload.service()
ids = ['_B7zY8B0T2U','sIxR17p2Wyo','_vdpEoN18FQ','HjZKuzk5VHM','H3IeR-EyVx0','9fhn6oJhha4','SlvY4YuVuvA']
for v in yt.videos().list(part='snippet', id=','.join(ids)).execute()['items']:
    d = v['snippet']['description']
    print(v['id'], '| 이자' if '이자' in d or '이자' in v['snippet']['title'] else '| -', '|', d[:160].replace('\n',' / '))
