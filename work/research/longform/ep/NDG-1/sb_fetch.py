# NDG-1 경쟁 스토리보드(sb0, 공개 미리보기 칸) 받기 — 영상 파일은 받지 않는다. 받은 그림은 raw/sb(커밋 안 함, rawclean 3일)
import json, os, subprocess, sys, urllib.request
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw', 'sb'); os.makedirs(OUT, exist_ok=True)
H = {'User-Agent': 'Mozilla/5.0'}
for vid in sys.argv[1:]:
    r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-j', f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=180)
    try: j = json.loads(r.stdout)
    except Exception: print(vid, '실패', r.stderr[-200:]); continue
    sb = [f for f in j['formats'] if f.get('format_id') == 'sb0']
    if not sb: print(vid, 'sb0 없음'); continue
    f = sb[0]; frags = f.get('fragments', []); t = 0.0; meta = []
    for i, fr in enumerate(frags):
        p = os.path.join(OUT, f'{vid}_{i:02d}.jpg')
        if not os.path.exists(p):
            open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(fr['url'], headers=H), timeout=30).read())
        meta.append({'i': i, 'start': t, 'dur': fr.get('duration')}); t += fr.get('duration') or 0
    json.dump({'vid': vid, 'title': j.get('title'), 'fmt': {k: f.get(k) for k in ('width', 'height', 'rows', 'columns', 'fps')}, 'frags': meta}, open(os.path.join(OUT, vid + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(vid, len(frags), '장', f.get('width'), f.get('rows'), f.get('columns'))
