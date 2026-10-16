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
    # 화면만 렌더(--muted) — 소리는 지난 판 트랙을 붙인다. 옛 wav가 public에서 빠진 편(d1s_when 10/16)도 렌더되게 말 파일 자리를 무음으로 바꾼 임시 props를 쓴다(숫자·글자·프레임 그대로).
    tmp = f'_v3tmp_{name}.json'; tp = json.loads(json.dumps(props))
    for s in tp['scenes']:
        for l in s.get('lines', []):
            if l.get('audio'): l['audio'] = 'audio/_silence.wav'
    json.dump(tp, open(os.path.join(VID, tmp), 'w', encoding='utf-8'), ensure_ascii=False)
    tdir = os.path.join('C:/Users/Public/rtmp', name); os.makedirs(tdir, exist_ok=True)   # 렌더 임시 폴더를 편마다 따로(10/16 h1s_forest: 같이 돌던 렌더 중 임시 폴더가 사라져 이어 붙이기 실패)
    if '--skip-render' not in sys.argv or not os.path.exists(v):
        bdir = 'C:/Users/Public/rtmp/bundles/' + os.path.basename(idx).split('_')[0]   # 미리 묶은 번들(npx remotion bundle) — 같이 도는 렌더끼리 webpack 캐시 충돌(EPERM rmdir) 피함
        src = bdir if os.path.exists(os.path.join(bdir, 'index.html')) else idx
        rc = subprocess.call(['npx', 'remotion', 'render', src, comp, v, f'--props={tmp}', '--muted', '--pixel-format=yuv420p', '--concurrency=6', '--bundle-cache=false'], cwd=VID, shell=(os.name == 'nt'), env=dict(os.environ, TEMP=tdir, TMP=tdir))
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
