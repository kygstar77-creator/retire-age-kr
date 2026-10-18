# bgcheck 10/19 '움직이는 판' 시험 — 합성 영상 두 개로 ③ 같은 판 기준만 본다.
#   A 수페 꼴: 실사 5초 + 판 40초(6초마다 점·선·꼬리표 하나씩 붙음, 1.00→1.03 다가가기) + 실사 5초 → ③ 통과해야 한다
#   B 움직임 없는 판: 실사 5초 + 판 21초(그대로) + 실사 5초 → ③ 걸려야 한다
#   py -3.12 work/bgcheck_selftest.py [출력 폴더]
import os, sys, tempfile
import numpy as np, cv2, imageio_ffmpeg
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bgcheck
FPS = 30; W, H = 1920, 1080
rng = np.random.default_rng(7)

def live(i):   # 사진처럼 섞인 색(움직이는 흐린 잡음)
    base = rng.integers(0, 255, (H // 24, W // 24, 3), dtype=np.uint8)
    return cv2.resize(cv2.GaussianBlur(base, (3, 3), 0), (W, H), interpolation=cv2.INTER_LINEAR)

def board(t, moving):
    img = np.full((H, W, 3), 246, np.uint8)
    cv2.rectangle(img, (100, 236), (1820, 852), (255, 255, 255), -1)
    cv2.putText(img, 'SAME 3 EOK, TWO ACCOUNTS', (330, 170), cv2.FONT_HERSHEY_SIMPLEX, 3.2, (24, 25, 29), 9, cv2.LINE_AA)
    cv2.line(img, (300, 760), (1600, 760), (140, 140, 140), 3)
    k = int(t // 6) + 1 if moving else 3          # 붙은 요소 수
    pts = [(300 + j * 190, 360 + (j * 97) % 330) for j in range(8)]
    for j in range(min(k, 8)):
        if j: cv2.line(img, pts[j - 1], pts[j], (0, 90, 255), 8, cv2.LINE_AA)
        cv2.circle(img, pts[j], 18, (0, 90, 255), -1, cv2.LINE_AA)
        cv2.putText(img, f'{2003 + j * 3}', (pts[j][0] - 50, pts[j][1] - 34), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (24, 25, 29), 3, cv2.LINE_AA)
    if moving:   # 천천히 다가가기 1.00→1.03 (세지 말아야 함)
        z = 1 + 0.03 * t / 40; M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
        img = cv2.warpAffine(img, M, (W, H), borderValue=(246, 246, 246))
    return img

def make(path, segs):
    wr = imageio_ffmpeg.write_frames(path, (W, H), fps=FPS, codec='libx264', pix_fmt_out='yuv420p', macro_block_size=8, ffmpeg_log_level='error')
    wr.send(None); i = 0
    for kind, sec, mv in segs:
        for n in range(int(sec * FPS)):
            img = live(i) if kind == 'live' else board(n / FPS, mv)
            wr.send(np.ascontiguousarray(img)); i += 1
    wr.close()

out = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp()
os.makedirs(out, exist_ok=True)
cases = [('A_supe40', [('live', 5, 0), ('board', 40, True), ('live', 5, 0)], True),
         ('B_static21', [('live', 5, 0), ('board', 21, False), ('live', 5, 0)], False)]
bad = 0
for name, segs, want in cases:
    p = os.path.join(out, name + '.mp4'); make(p, segs)
    vert, d = bgcheck.scan(p); ok, why, s = bgcheck.judge(vert, d)
    board_ok = not s['board_over']
    runs = [r for r in s['board_runs']]
    res = 'OK' if board_ok == want else 'FAIL'; bad += res == 'FAIL'
    print(f"{name}: ③ {'통과' if board_ok else '걸림'} (기대 {'통과' if want else '걸림'}) {res} · 판 구간 {runs} · 컷 {d['cuts']}")
sys.exit(1 if bad else 0)
