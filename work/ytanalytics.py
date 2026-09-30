# 유튜브 분석(시청 지속·클릭률·유입 경로) — 업로드 토큰과 따로 둔다(업로드·쇼츠 루틴이 쓰는 youtube_token.json을 건드리지 않으려고).
#   py -3.12 work/ytanalytics.py auth                 # 처음 한 번: 브라우저가 열리면 사장님이 파이어맵 채널 계정으로 '허용'
#   py -3.12 work/ytanalytics.py video <videoId>      # 한 편: 조회·평균 시청 시간·평균 시청 비율·노출 클릭률·구독 증가
#   py -3.12 work/ytanalytics.py curve <videoId>      # 한 편: 구간별 남은 시청자 비율(어디서 나가는지)
#   py -3.12 work/ytanalytics.py recent [일수=28]     # 최근 영상들 한 줄씩
# 권한: yt-analytics.readonly + youtube.readonly(읽기만). 2026-09-30 사장님 "동의 어떻게 하는데".
import sys, os, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
DOCS = r'C:\Users\강영준\Documents'; CLIENT = os.path.join(DOCS, 'youtube_client.json'); TOKEN = os.path.join(DOCS, 'youtube_analytics_token.json')
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly', 'https://www.googleapis.com/auth/youtube.readonly']

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

def svc():
    from googleapiclient.discovery import build
    c = creds()
    if not c: print('토큰 없음 — py -3.12 work/ytanalytics.py auth'); sys.exit(2)
    return build('youtubeAnalytics', 'v2', credentials=c)

def q(metrics, dims=None, filters=None, start='2026-01-01', end=None, sort=None, maxResults=None):
    end = end or datetime.date.today().isoformat()
    kw = dict(ids='channel==MINE', startDate=start, endDate=end, metrics=metrics)
    if dims: kw['dimensions'] = dims
    if filters: kw['filters'] = filters
    if sort: kw['sort'] = sort
    if maxResults: kw['maxResults'] = maxResults  # dims=video는 maxResults 없으면 400
    return svc().reports().query(**kw).execute()

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'auth': auth()
    elif cmd == 'video':
        r = q('views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes', filters='video==' + sys.argv[2])
        print(r.get('columnHeaders') and [h['name'] for h in r['columnHeaders']], r.get('rows'))
        try:
            r2 = q('impressions,impressionsClickThroughRate', filters='video==' + sys.argv[2]); print('노출·클릭률', r2.get('rows'))
        except Exception as e: print('노출·클릭률은 이 API에서 못 받음:', str(e)[:120])
    elif cmd == 'curve':
        r = q('audienceWatchRatio,relativeRetentionPerformance', dims='elapsedVideoTimeRatio', filters='video==' + sys.argv[2])
        for row in r.get('rows', []): print(f'{row[0]*100:5.0f}% 지점  남은 비율 {row[1]:.2f}  비슷한 길이 대비 {row[2]:.2f}')
    elif cmd == 'recent':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 28
        start = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        r = q('views,averageViewDuration,averageViewPercentage,subscribersGained', dims='video', start=start, sort='-views', maxResults=50)
        for row in r.get('rows', [])[:30]: print(row)
    else: print(__doc__ if __doc__ else open(__file__, encoding='utf-8').read().split('import')[0])
