# 유튜브 노출수·클릭률(Reporting API channel_reach_basic_a1) 날짜별 받기 + 영상별 요약 — youtube-loop 2026-10-07
#   py -3.12 work/ytreach.py            # 새 보고서만 받아 research/longform/loop/reach/<날짜>.csv, 최근 3일 영상별 노출·클릭률 출력
#   py -3.12 work/ytreach.py <videoId>  # 그 영상의 날짜별 노출·클릭률(받아 둔 csv 전부)
# 누적 조회만 보면 '노출 창이 닫힌 것'을 못 본다(A-1: 10/3 2,633 → 10/4 62). 토큰은 ytanalytics.py 것(읽기 전용).
import sys, os, io, csv, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ytanalytics as A
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'longform', 'loop', 'reach')

def fetch():
    s = build('youtubereporting', 'v1', credentials=A.creds())
    got = []
    for j in s.jobs().list().execute().get('jobs', []):
        if j['reportTypeId'] != 'channel_reach_basic_a1':
            continue
        for r in s.jobs().reports().list(jobId=j['id']).execute().get('reports', []):
            d = r['startTime'][:10]
            p = os.path.join(OUT, f'{d}.csv')
            if os.path.exists(p):
                continue
            req = s.media().download_media(resourceName='')
            req.uri = r['downloadUrl']
            with io.FileIO(p, 'wb') as fh:
                dl = MediaIoBaseDownload(fh, req)
                done = False
                while not done:
                    _, done = dl.next_chunk()
            got.append(d)
    return sorted(got)

def day(path):
    agg = collections.defaultdict(lambda: [0, 0.0])
    for r in csv.DictReader(open(path, encoding='utf-8')):
        imp = int(r.get('video_thumbnail_impressions') or 0)
        ctr = float(r.get('video_thumbnail_impressions_ctr') or 0)
        a = agg[r['video_id']]
        a[0] += imp
        a[1] += imp * ctr
    return {v: (i, round(c / i * 100, 1) if i else 0.0) for v, (i, c) in agg.items()}

if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(OUT, '*.csv')))
    if len(sys.argv) > 1:
        for f in files:
            i, c = day(f).get(sys.argv[1], (0, 0.0))
            print(os.path.basename(f)[:10], i, f'{c}%')
    else:
        print('새로 받음:', fetch() or '없음')
        for f in sorted(glob.glob(os.path.join(OUT, '*.csv')))[-3:]:
            top = sorted(day(f).items(), key=lambda x: -x[1][0])[:8]
            print(os.path.basename(f)[:10], ' · '.join(f'{v} {i}·{c}%' for v, (i, c) in top))
