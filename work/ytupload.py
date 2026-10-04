# 유튜브 업로드 — 사장님 OAuth(데스크톱 앱) 1회 승인 후 토큰(Documents\youtube_token.json)으로 무인 업로드.
#   python work/ytupload.py auth                                  # 처음 한 번: 브라우저가 열리고 사장님이 허용
#   python work/ytupload.py upload <mp4> "<제목>" "<설명>" [공개=private|unlisted|public] [태그,쉼표]
#   python work/ytupload.py stats                                 # 내 채널 최근 영상 조회수
import sys, os, json, re
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

COUPANG_NOTE = '이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'

def upload(path, title, desc, privacy='private', tags='', paid=False):
    # 유튜브는 제목·설명의 < > 를 받지 않는다(400 invalidDescription, 2026-09-28 나이키 숏폼). 전각으로 바꾼다.
    title, desc = [x.replace('<', '＜').replace('>', '＞') for x in (title, desc)]
    # 쿠팡 파트너스 관문(2026-09-30, work/research/coupang-policy.md 체크리스트 9·10):
    # 설명란에 쿠팡 링크가 있으면 ① 첫 줄이 대가성 문구 ② '유료 프로모션 포함'(paid=True → 영상에 '유료 광고 포함' 표시)이 둘 다 있어야 올린다.
    if 'coupang.com' in desc:
        first = desc.strip().splitlines()[0]
        if COUPANG_NOTE not in first or not paid:
            print('올리지 않는다: 쿠팡 링크가 있으면 설명 첫 줄에 대가성 문구 + paid=True 필요'); sys.exit(5)
    # AI 티 검사(10/1) — 제목·설명. 편집자가 본 것은 FIREMAP_EDITOR_OK=1 로 통과시킨다.
    import aitell
    plain = re.sub(r'https?://\S+', ' ', title + '\n\n' + desc.replace(COUPANG_NOTE, ''))
    ok_ai, msg_ai, hits_ai = aitell.gate_text(plain, os.environ.get('FIREMAP_EDITOR_OK') == '1')
    if not ok_ai: aitell.refuse(msg_ai, hits_ai); sys.exit(6)
    print(msg_ai)
    from googleapiclient.http import MediaFileUpload
    yt = service()
    body = {'snippet': {'title': title[:100], 'description': desc[:5000], 'tags': [t.strip() for t in tags.split(',') if t.strip()][:30], 'categoryId': '22', 'defaultLanguage': 'ko', 'defaultAudioLanguage': 'ko'},
            'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False}}
    part = 'snippet,status'
    if paid:
        body['paidProductPlacementDetails'] = {'hasPaidProductPlacement': True}
        part += ',paidProductPlacementDetails'
    req = yt.videos().insert(part=part, body=body, media_body=MediaFileUpload(path, chunksize=8 * 1024 * 1024, resumable=True))
    res = None
    while res is None:
        status, res = req.next_chunk()
        if status: print(f'업로드 {int(status.progress() * 100)}%', flush=True)
    print('완료 https://youtu.be/' + res['id']); return res['id']

def stats():
    yt = service()
    ch = yt.channels().list(part='snippet,statistics,contentDetails', mine=True).execute()['items'][0]
    pl = ch['contentDetails']['relatedPlaylists']['uploads']
    # 2026-09-29: 채널 statistics.viewCount 는 며칠씩 늦게 갱신된다 — 3556 이 여섯 회차(12시간) 그대로인데
    # 같은 시간에 공개 쇼츠 두 편이 104회·162회로 올랐다(영상 수도 8로 멈춰 있었다). loop.py·health.py 가 이 숫자로
    # '늘어난 조회 0회'라 판정해 루프가 멈춰 있었다. 올린 영상 전부의 조회를 더한 값을 '총조회'로 찍는다(큰 쪽).
    all_ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=pl, maxResults=50, pageToken=tok).execute()
        all_ids += [i['contentDetails']['videoId'] for i in r.get('items', [])]
        tok = r.get('nextPageToken')
        if not tok: break
    vsum = 0
    for k in range(0, len(all_ids), 50):
        for v in yt.videos().list(part='statistics', id=','.join(all_ids[k:k + 50])).execute()['items']:
            vsum += int(v['statistics'].get('viewCount', 0))
    chv = int(ch['statistics'].get('viewCount', 0))
    print('채널:', ch['snippet']['title'], '| 구독', ch['statistics'].get('subscriberCount'), '| 영상', len(all_ids),
          '| 총조회', max(vsum, chv), f'(영상별 합 {vsum} · 채널 통계 {chv})')
    items = yt.playlistItems().list(part='snippet', playlistId=pl, maxResults=10).execute().get('items', [])
    ids = [i['snippet']['resourceId']['videoId'] for i in items]
    if ids:
        # 영상 id와 공개상태도 같이 찍는다 — loop.py가 회차 사이에 같은 영상을 짝지어 재려면 id가 있어야 하고,
        # 비공개(private)면 조회가 영영 0이라 조회로는 디자인 조정을 판정할 수 없다(2026-09-24).
        for v in yt.videos().list(part='snippet,statistics,status', id=','.join(ids)).execute()['items']:
            print(' ', v['snippet']['publishedAt'][:10], v['statistics'].get('viewCount', '0'), '회 |',
                  v['status'].get('privacyStatus', '?'), '|', v['id'], '|', v['snippet']['title'][:50])

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if cmd == 'auth': auth()
    elif cmd == 'upload': upload(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else 'private', sys.argv[6] if len(sys.argv) > 6 else '')
    else: stats()
