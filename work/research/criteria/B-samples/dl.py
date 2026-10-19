# 표본 받기 — yt-dlp(이미 깔림)로 영상만·소리만 따로 받는다(합치기 없음). 롱폼은 앞 10분만(--download-sections).
#   python dl.py <media 폴더>     · 이미 받은 것은 건너뜀 · 영상 사이 20초 쉼(봇 확인 피하기)
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
FF = os.path.join(HERE, 'media', 'bin')   # imageio ffmpeg를 ffmpeg.exe로 복사해 둔 곳(remotion ffmpeg는 구간 받기에서 자주 실패)
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
YT = ['py', '-3.12', '-m', 'yt_dlp', '--js-runtimes', 'node', '-q', '--no-warnings', '--ffmpeg-location', FF, '--no-playlist']
ONLY = sys.argv[2] if len(sys.argv) > 2 else None
if os.environ.get('REV'): S = {k: v[::-1] for k, v in S.items()}
for kind in ('short', 'long'):
    if ONLY and kind != ONLY: continue
    for ch, vid in S[kind]:
        if not os.environ.get('FORCE') and os.path.exists(os.path.join(HERE, 'res', f'{kind}_{vid}.json')): continue   # 이미 잰 것(FORCE=1이면 다시 받음 — 컷 다시 재기·판용)
        base = os.path.join(OUT, f'{kind}_{vid}')
        if os.path.exists(base + '.v.mp4') and os.path.exists(base + '.a.m4a'): continue
        sec = ['--download-sections', '*0-600'] if kind == 'long' else []   # 롱폼은 앞 10분만
        vf = 'bv*[height<=1920][ext=mp4][vcodec^=avc1]/bv*[ext=mp4]' if kind == 'short' else 'bv*[height<=480][ext=mp4][vcodec^=avc1]/bv*[height<=480]'
        for f, ext in ((vf, '.v.mp4'), ('ba[ext=m4a]/ba', '.a.m4a')):
            if os.path.exists(base + ext): continue
            r = subprocess.run(YT + ['-f', f, *sec, '-o', base + ext, f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True, encoding='utf-8', errors='replace')
            print(kind, ch, vid, ext, 'ok' if os.path.exists(base + ext) else 'FAIL ' + r.stderr[-300:], flush=True)
        time.sleep(8)
print('done')
