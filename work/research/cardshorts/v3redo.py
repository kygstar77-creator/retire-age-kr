# 예약 쇼츠 디자인 기준 v3 재렌더(10/16 영상 디자인 총괄) — 화면만 새 틀, 소리는 지난 판(_sz2_ds.mp4) 트랙 그대로(-c copy)
#   py -3.12 work/research/cardshorts/v3redo.py <편>   → work/video/out/<편>_v3_ds.mp4 + 관문(안전 영역·디자인·0초 빈 곳) + <편>/sheet_v3.png
# 틀: C1S(c1s_index) · M1S(m1s_index) · C2P(c2p_index) — upload.json layout으로 고른다. 배경 props는 bgprops.py가 먼저(C2P는 그림이 이미 실사).
import os, sys, json, subprocess, shutil
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..')); REPO = os.path.dirname(WORK); VID = os.path.join(WORK, 'video')
sys.path.insert(0, WORK)
COMP = {'c1clip': ('src/c1s_index.ts', 'C1S'), None: ('src/c1s_index.ts', 'C1S'), 'm1clip': ('src/m1s_index.ts', 'M1S'), 'c2person': ('src/c2p_index.ts', 'C2P')}


def ffmpeg():
    import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()


def nframes(p):
    import cv2; c = cv2.VideoCapture(p); n = int(c.get(7)); c.release(); return n


def sheet(mp4, out, n=12, w=270):
    import cv2
    from PIL import Image, ImageDraw
    c = cv2.VideoCapture(mp4); N = int(c.get(7)); fps = c.get(5); h = int(w * 1920 / 1080)
    S = Image.new('RGB', (6 * (w + 6), 2 * (h + 22)), (40, 40, 40)); d = ImageDraw.Draw(S)
    for i in range(n):
        f = int((i + 0.5) / n * N); c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, fr = c.read()
        if not ok: continue
        x, y = (i % 6) * (w + 6), (i // 6) * (h + 22)
        S.paste(Image.fromarray(cv2.resize(fr, (w, h))[:, :, ::-1]), (x, y + 20)); d.text((x + 2, y + 3), f'{f / fps:.1f}s', fill=(255, 255, 0))
    S.save(out)


def main(name):
    d = os.path.join(HERE, name); up = json.load(open(os.path.join(d, 'upload.json'), encoding='utf-8'))
    idx, comp = COMP[up.get('layout')] if up.get('layout') in COMP else COMP['c1clip']
    if name in ('w1s_kospi', 'h1s_gap', 'd1s_when'): idx, comp = COMP['c1clip']
    old = os.path.join(REPO, up['mp4'])
    v = os.path.join(VID, 'out', f'{name}_v3.mp4'); vd = os.path.join(VID, 'out', f'{name}_v3_ds.mp4')
    props = json.load(open(os.path.join(VID, name + '.json'), encoding='utf-8'))
    if comp != 'C2P' and not props.get('bg'): print('배경 props 없음 — bgprops.py 먼저'); return 2
    if '--skip-render' not in sys.argv or not os.path.exists(v):
        rc = subprocess.call(['npx', 'remotion', 'render', idx, comp, v, f'--props={name}.json', '--muted', '--pixel-format=yuv420p', '--concurrency=4', '--bundle-cache=false'], cwd=VID, shell=(os.name == 'nt'))
        if rc: print('렌더 실패', rc); return rc
    if nframes(v) != nframes(old): print('길이 다름', nframes(v), nframes(old)); return 3
    subprocess.check_call([ffmpeg(), '-y', '-loglevel', 'error', '-i', v, '-i', old, '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', vd])
    import safezone, bgcheck, emptyscan
    ok1, m1 = safezone.gate(vd, quiet=True); ok2, m2 = bgcheck.gate(vd); e0 = emptyscan.frame0(vd)[0]
    print(m1); print(m2); print(f'0초 빈 곳 {e0:.0%} (기준 {emptyscan.LIMIT0:.0%} 이하)')
    sheet(vd, os.path.join(d, 'sheet_v3.png'))
    res = {'mp4': os.path.relpath(vd, REPO).replace('\\', '/'), 'frames': nframes(vd), 'safezone': ok1, 'design': ok2, 'empty0': round(e0, 3), 'msg': [m1, m2]}
    json.dump(res, open(os.path.join(d, 'v3redo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 0 if (ok1 and ok2 and e0 <= emptyscan.LIMIT0) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
