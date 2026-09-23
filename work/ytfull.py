# 채널 전체 영상 수집 — 사장님 2026-09-23 "전체 동영상 스크립트랑 화면 전부". 자막 전문 + 스토리보드 3장씩, 채널 목록·요약 파일.
#   python work/ytfull.py UCC3yfxS5qC6PCwDzetUuEWg 소수몽키 [최대편수]
# 결과: work/research/yt/full/<채널>/<videoId>.txt (자막), <videoId>_sb{0,1,2}.jpg (장면), index.json (제목·날짜·조회·길이·자막유무)
import sys, os, re, json, time, subprocess, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
from youtube_transcript_api import YouTubeTranscriptApi
cid, name = sys.argv[1], sys.argv[2]; limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'yt', 'full', name); os.makedirs(OUT, exist_ok=True)
H = {'User-Agent': 'Mozilla/5.0'}
idx_p = os.path.join(OUT, 'index.json'); index = json.load(open(idx_p, encoding='utf-8')) if os.path.exists(idx_p) else {}
# 1) 채널 전체 목록(yt-dlp flat)
r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '--flat-playlist', '-j', f'https://www.youtube.com/channel/{cid}/videos'], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=900)
vids = []
for line in r.stdout.splitlines():
    try: j = json.loads(line); vids.append({'id': j['id'], 'title': j.get('title', ''), 'views': j.get('view_count') or 0, 'dur': j.get('duration') or 0})
    except Exception: pass
print(name, '전체 영상', len(vids)); vids = vids[:limit]
api = YouTubeTranscriptApi(); done = 0
for i, v in enumerate(vids):
    vid = v['id']
    if vid in index and index[vid].get('sb', 0) >= 1 and index[vid].get('chars', 0) > 0: continue
    rec = dict(v); rec['chars'] = 0; rec['sb'] = 0
    try:
        tr = api.list(vid).find_transcript(['ko']).fetch(); segs = [(round(x.start), x.text) for x in tr]
        open(os.path.join(OUT, f'{vid}.txt'), 'w', encoding='utf-8').write(f"# {v['title']} | {v['views']}회 | {v['dur']}초\n" + '\n'.join(f'{s//60:02d}:{s%60:02d} {t}' for s, t in segs))
        rec['chars'] = sum(len(t) for _, t in segs)
    except Exception as e: rec['err'] = str(e)[:60]
    try:
        j = json.loads(subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-j', f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=120).stdout)
        rec['date'] = j.get('upload_date', ''); rec['views'] = j.get('view_count') or rec['views']; rec['dur'] = j.get('duration') or rec['dur']
        sb = [f for f in j['formats'] if f.get('format_id') == 'sb0']
        if sb:
            frags = sb[0].get('fragments', [])
            for k, fi in enumerate(sorted({0, len(frags) // 2, len(frags) - 1})):
                if fi < len(frags):
                    b = urllib.request.urlopen(urllib.request.Request(frags[fi]['url'], headers=H), timeout=30).read()
                    open(os.path.join(OUT, f'{vid}_sb{k}.jpg'), 'wb').write(b); rec['sb'] = k + 1
    except Exception as e: rec['err2'] = str(e)[:60]
    index[vid] = rec; done += 1
    if done % 10 == 0:
        json.dump(index, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print(f'{i+1}/{len(vids)} 저장', flush=True)
    time.sleep(0.5)
json.dump(index, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
ok = sum(1 for x in index.values() if x.get('chars', 0) > 0); sbn = sum(1 for x in index.values() if x.get('sb', 0) > 0)
print(f'{name}: 영상 {len(index)}개 중 자막 {ok}개, 장면 {sbn}개 → {OUT}')
