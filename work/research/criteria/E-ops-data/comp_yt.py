import sys, os, json, datetime, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytanalytics as A
from googleapiclient.discovery import build
yt = build('youtube', 'v3', credentials=A.creds())
oc=json.load(open(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\longform\loop\outlier_channels.json',encoding='utf-8'))
top=sorted(oc.items(), key=lambda x:-x[1].get('hits',0))[:24]
since=datetime.datetime(2026,8,20,tzinfo=datetime.timezone.utc)
res={}
for cid,info in top:
    ch=yt.channels().list(part='contentDetails,statistics,snippet',id=cid).execute().get('items',[])
    if not ch: continue
    ch=ch[0]; up=ch['contentDetails']['relatedPlaylists']['uploads']
    ids=[];tok=None;stop=False
    while not stop:
        r=yt.playlistItems().list(part='contentDetails',playlistId=up,maxResults=50,pageToken=tok).execute()
        for i in r['items']:
            p=i['contentDetails'].get('videoPublishedAt')
            if p and datetime.datetime.fromisoformat(p.replace('Z','+00:00'))<since: stop=True;break
            ids.append(i['contentDetails']['videoId'])
        tok=r.get('nextPageToken')
        if not tok or len(ids)>400: break
    vids=[]
    for i in range(0,len(ids),50):
        for v in yt.videos().list(part='snippet,contentDetails,statistics',id=','.join(ids[i:i+50])).execute()['items']:
            d=v['contentDetails']['duration'];m=re.match(r'P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',d)
            s=int(m[1] or 0)*3600+int(m[2] or 0)*60+int(m[3] or 0) if m else 0
            if v['snippet'].get('liveBroadcastContent')!='none': continue
            vids.append(dict(id=v['id'],pub=v['snippet']['publishedAt'],sec=s,views=int(v['statistics'].get('viewCount',0))))
    res[cid]=dict(title=ch['snippet']['title'],subs=ch['statistics'].get('subscriberCount'),vids=vids)
    print(ch['snippet']['title'],ch['statistics'].get('subscriberCount'),len(vids),flush=True)
json.dump(res,open('comp.json','w',encoding='utf-8'),ensure_ascii=False)
