# 채널 전체 영상 수집 — 자막 전문 + **장면이 바뀔 때마다 한 장**(PPT 장표 전부). 사장님 2026-09-23 "장면 3장만? 장표가 엄청 많은데".
#   YTFULL_DAYS=90 YTFULL_GAP=90 python work/ytfull.py UCC3yfxS5qC6PCwDzetUuEWg 소수몽키 [최대편수]   ← 최근 90일치만, 90초 간격
# 방법: yt-dlp(node 런타임)로 480p 영상만 잠깐 받아 OpenCV로 1초에 1프레임 읽고, 화면이 크게 바뀐 순간(히스토그램 차이)마다 JPG 저장 → 영상 파일은 지운다.
# 결과: work/research/yt/full/<채널>/<videoId>.txt (자막), <videoId>/NNN_mmss.jpg (장면들), index.json (제목·날짜·조회·길이·자막글자·장면수)
import sys, os, re, json, time, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
import cv2, numpy as np
from youtube_transcript_api import YouTubeTranscriptApi
cid, name = sys.argv[1], sys.argv[2]; limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
GAP = int(os.environ.get('YTFULL_GAP', '90'))
DAYS = int(os.environ.get('YTFULL_DAYS', '90'))   # 최근 N일치만(사장님 2026-09-23 '최근 3개월씩만'). 전체 이력은 받지 않는다   # 영상 사이 대기(초). 2026-09-23 180편쯤에서 유튜브가 '봇 확인'으로 막았다 → 천천히 받는다
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'yt', 'full', name); os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(os.environ.get('TEMP', 'C:/Temp'), 'ytfull_tmp'); os.makedirs(TMP, exist_ok=True)
idx_p = os.path.join(OUT, 'index.json'); index = json.load(open(idx_p, encoding='utf-8')) if os.path.exists(idx_p) else {}
YT = [sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-q', '--no-warnings']

def listing():
    r = subprocess.run(YT + ['--flat-playlist', '-j', f'https://www.youtube.com/channel/{cid}/videos'], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=900)
    out = []
    for line in r.stdout.splitlines():
        try: j = json.loads(line); out.append({'id': j['id'], 'title': j.get('title', ''), 'views': j.get('view_count') or 0, 'dur': j.get('duration') or 0})
        except Exception: pass
    return out

def ytdlp_subs(vid):
    """자막 API가 IP 차단(IpBlocked)일 때의 두 번째 경로. 2026-09-23 실측: api.list()는 되는데 .fetch()가
    IpBlocked 로 떨어져 소수몽키·수페TV·투미TV 1,448편이 전부 자막 0개였다. yt-dlp는 같은 영상의 ko 자동자막을
    목록에 보여 준다. 다만 영상 수집 직후에는 yt-dlp도 429(Too Many Requests)가 나므로 실패하면 조용히 넘긴다."""
    base = os.path.join(TMP, 'sub_' + vid)
    for f in glob.glob(base + '*'):
        try: os.remove(f)
        except OSError: pass
    try:
        subprocess.run(YT + ['--skip-download', '--write-auto-subs', '--write-subs', '--sub-langs', 'ko',
                             '--sub-format', 'json3', '-o', base, f'https://www.youtube.com/watch?v={vid}'],
                       capture_output=True, text=True, timeout=180)
    except Exception:
        return None
    for f in glob.glob(base + '*.json3'):
        try:
            j = json.load(open(f, encoding='utf-8'))
            segs = []
            for ev in j.get('events', []):
                t = ''.join(x.get('utf8', '') for x in ev.get('segs', [])).strip()
                if t: segs.append((round(ev.get('tStartMs', 0) / 1000), t))
            if segs: return segs
        except Exception:
            pass
    return None


def scenes(vid, mp4, outdir, max_frames=120):
    cap = cv2.VideoCapture(mp4)   # 영상 임시 파일은 ASCII 경로(TMP)라 읽기는 된다
    if not cap.isOpened(): return 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 30; n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); step = int(fps)  # 1초 간격
    os.makedirs(outdir, exist_ok=True); last = None; saved = 0; i = 0
    while i < n and saved < max_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, fr = cap.read()
        if not ok: break
        small = cv2.resize(fr, (160, 90)); h = cv2.calcHist([cv2.cvtColor(small, cv2.COLOR_BGR2HSV)], [0, 1], None, [16, 8], [0, 180, 0, 256]); cv2.normalize(h, h)
        if last is None or cv2.compareHist(last, h, cv2.HISTCMP_BHATTACHARYYA) > 0.25:
            sec = int(i / fps); ok2, buf = cv2.imencode('.jpg', fr, [cv2.IMWRITE_JPEG_QUALITY, 80])   # imwrite는 한글 경로에 못 쓴다
            if ok2: open(os.path.join(outdir, f'{saved:03d}_{sec//60:02d}{sec%60:02d}.jpg'), 'wb').write(buf.tobytes()); saved += 1; last = h
        i += step
    cap.release(); return saved

vids = listing(); print(name, '전체 영상', len(vids), flush=True)
# 최신순(채널 목록 순서)으로 훑으며 업로드일이 DAYS보다 오래되면 멈춘다. 날짜는 영상 메타(-j)에서 본다(가벼운 호출).
import datetime
cutoff = (datetime.date.today() - datetime.timedelta(days=DAYS)).strftime('%Y%m%d')
recent = []; fails = 0
for v in vids[:limit]:
    rec0 = index.get(v['id'], {})
    if rec0.get('date'):
        if rec0['date'] >= cutoff: recent.append(v)
        else: break
        continue
    try:
        j = json.loads(subprocess.run(YT + ['--skip-download', '-j', f"https://www.youtube.com/watch?v={v['id']}"], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=120).stdout)
        v['date'] = j.get('upload_date', ''); v['views'] = j.get('view_count') or v['views']; v['dur'] = j.get('duration') or v['dur']
    except Exception: v['date'] = ''
    if not v['date']:
        fails += 1
        if fails >= 3: print('영상 정보 조회가 계속 실패(차단 중일 수 있음) — 이번 회차 중단', flush=True); break
        continue
    if v['date'] < cutoff: break
    recent.append(v); time.sleep(3)
vids = recent; print(name, f'최근 {DAYS}일 영상', len(vids), flush=True)
api = YouTubeTranscriptApi(); done = 0; t0 = time.time()
for k, v in enumerate(vids):
    vid = v['id']
    if index.get(vid, {}).get('frames', 0) > 0: continue   # 장면 받은 건 건너뜀(자막은 차단 풀리면 따로 채움)
    rec = dict(index.get(vid, {})); rec.update({k: v[k] for k in ('id', 'title', 'views', 'dur', 'date') if v.get(k)}); rec.setdefault('chars', 0); rec.setdefault('frames', 0)
    if rec['chars'] == 0:
        segs = None
        try:
            tr = api.list(vid).find_transcript(['ko']).fetch(); segs = [(round(x.start), x.text) for x in tr]
        except Exception as e:
            # 오류를 60자로 자르는 바람에 IpBlocked 가 "video is no longer available" 안내문으로 보였고,
            # 세 채널 1,448편이 자막 0개인 것을 아무도 못 알아챘다(2026-09-23 확인). 예외 이름을 앞에 적는다.
            rec['err'] = type(e).__name__ + ': ' + ' '.join(str(e).split())[:80]
            segs = ytdlp_subs(vid)          # 자막 API가 막히면 yt-dlp로 한 번 더
            if segs: rec['err'] += ' -> yt-dlp로 받음'
        if segs:
            open(os.path.join(OUT, f'{vid}.txt'), 'w', encoding='utf-8').write(f"# {v['title']} | {v['views']}회 | {v['dur']}초\n" + '\n'.join(f'{s//60:02d}:{s%60:02d} {t}' for s, t in segs))
            rec['chars'] = sum(len(t) for _, t in segs)
    if rec['frames'] == 0:
        mp4 = os.path.join(TMP, vid + '.mp4')
        try:
            r2 = subprocess.run(YT + ['-f', '135/134/160', '-o', mp4, f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True, timeout=600)
            if os.path.exists(mp4): rec['frames'] = scenes(vid, mp4, os.path.join(OUT, vid))
            elif 'bot' in (r2.stderr or ''): rec['err2'] = 'bot-check'   # 유튜브 '봇 확인' 차단
            else: rec['err2'] = (r2.stderr or '')[-80:]
        except Exception as e: rec['err2'] = str(e)[:60]
        finally:
            for f in glob.glob(os.path.join(TMP, vid + '*')):
                try: os.remove(f)
                except Exception: pass
    index[vid] = rec; done += 1
    if rec.get('err2', '').find('bot') >= 0 or (rec['chars'] == 0 and rec['frames'] == 0 and done > 3):
        json.dump(index, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print('유튜브 차단 신호 — 이번 회차 중단(다음 회차에 이어서)', flush=True); break
    time.sleep(GAP)
    if done % 5 == 0:
        json.dump(index, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(f'{k+1}/{len(vids)} 처리 | 자막 {rec["chars"]}자 · 장면 {rec["frames"]}장 | 경과 {int(time.time()-t0)//60}분', flush=True)
json.dump(index, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
ok = sum(1 for x in index.values() if x.get('chars', 0) > 0); fr = sum(x.get('frames', 0) for x in index.values())
print(f'{name}: 영상 {len(index)}개, 자막 {ok}개, 장면 총 {fr}장 → {OUT}', flush=True)
