import sys, os, json, datetime, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import ytanalytics as A
from googleapiclient.discovery import build
c = A.creds()
yt = build('youtube', 'v3', credentials=c)
ch = yt.channels().list(part='contentDetails,statistics,snippet', mine=True).execute()['items'][0]
print(ch['snippet']['title'], ch['statistics'])
up = ch['contentDetails']['relatedPlaylists']['uploads']
ids=[]; tok=None
while True:
    r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
    ids += [i['contentDetails']['videoId'] for i in r['items']]
    tok = r.get('nextPageToken')
    if not tok: break
vids=[]
for i in range(0,len(ids),50):
    r = yt.videos().list(part='snippet,contentDetails,statistics,status', id=','.join(ids[i:i+50])).execute()
    for v in r['items']:
        d=v['contentDetails']['duration']
        m=re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',d); s=int(m[1] or 0)*3600+int(m[2] or 0)*60+int(m[3] or 0)
        vids.append(dict(id=v['id'],title=v['snippet']['title'],pub=v['snippet']['publishedAt'],sec=s,views=int(v['statistics'].get('viewCount',0)),privacy=v['status']['privacyStatus'],publishAt=v['status'].get('publishAt')))
json.dump(vids,open('own_videos.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(vids))
# per-video daily views
svc=A.svc()
out={}
for v in vids:
    if v['privacy']!='public': continue
    st=v['pub'][:10]
    try:
        r=svc.reports().query(ids='channel==MINE',startDate=st,endDate=datetime.date.today().isoformat(),metrics='views',dimensions='day',filters='video=='+v['id']).execute()
        out[v['id']]=r.get('rows',[])
    except Exception as e:
        out[v['id']]=str(e)[:100]
json.dump(out,open('own_daily.json','w',encoding='utf-8'),indent=0)
print('done',len(out))
