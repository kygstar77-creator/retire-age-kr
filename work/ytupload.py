# 유튜브 업로드 — 사장님 OAuth(데스크톱 앱) 1회 승인 후 토큰(Documents\youtube_token.json)으로 무인 업로드.
#   python work/ytupload.py auth                                  # 처음 한 번: 브라우저가 열리고 사장님이 허용
#   python work/ytupload.py upload <mp4> "<제목>" "<설명>" [공개=private|unlisted|public] [태그,쉼표]
#   python work/ytupload.py stats                                 # 내 채널 최근 영상 조회수
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
DOCS = r'C:\Users\강영준\Documents'; CLIENT = os.path.join(DOCS, 'youtube_client.json'); TOKEN = os.path.join(DOCS, 'youtube_token.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

def creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    c = Credentials.from_authorized_user_file(TOKEN, SCOPES) if os.path.exists(TOKEN) else None
    if c and c.expired and c.refresh_token: c.refresh(Request()); open(TOKEN, 'w').write(c.to_json())
    return c

def auth():
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
    c = flow.run_local_server(port=0, prompt='consent', access_type='offline')
    open(TOKEN, 'w').write(c.to_json()); print('승인 완료 → 토큰 저장:', TOKEN)

def service():
    from googleapiclient.discovery import build
    c = creds()
    if not c: print('토큰 없음 — python work/ytupload.py auth'); sys.exit(2)
    return build('youtube', 'v3', credentials=c)

def upload(path, title, desc, privacy='private', tags=''):
    from googleapiclient.http import MediaFileUpload
    yt = service()
    body = {'snippet': {'title': title[:100], 'description': desc[:5000], 'tags': [t.strip() for t in tags.split(',') if t.strip()][:30], 'categoryId': '22', 'defaultLanguage': 'ko'},
            'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False}}
    req = yt.videos().insert(part='snippet,status', body=body, media_body=MediaFileUpload(path, chunksize=8 * 1024 * 1024, resumable=True))
    res = None
    while res is None:
        status, res = req.next_chunk()
        if status: print(f'업로드 {int(status.progress() * 100)}%', flush=True)
    print('완료 https://youtu.be/' + res['id']); return res['id']

def stats():
    yt = service()
    ch = yt.channels().list(part='snippet,statistics,contentDetails', mine=True).execute()['items'][0]
    print('채널:', ch['snippet']['title'], '| 구독', ch['statistics'].get('subscriberCount'), '| 영상', ch['statistics'].get('videoCount'), '| 총조회', ch['statistics'].get('viewCount'))
    pl = ch['contentDetails']['relatedPlaylists']['uploads']
    items = yt.playlistItems().list(part='snippet', playlistId=pl, maxResults=10).execute().get('items', [])
    ids = [i['snippet']['resourceId']['videoId'] for i in items]
    if ids:
        for v in yt.videos().list(part='snippet,statistics', id=','.join(ids)).execute()['items']:
            print(' ', v['snippet']['publishedAt'][:10], v['statistics'].get('viewCount', '0'), '회 |', v['snippet']['title'][:50])

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if cmd == 'auth': auth()
    elif cmd == 'upload': upload(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else 'private', sys.argv[6] if len(sys.argv) > 6 else '')
    else: stats()
