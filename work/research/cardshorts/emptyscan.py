# 세로 쇼츠 '빈 곳' 비율 — 화면을 칸(가로 18칸 = 1080px 기준 60px)으로 나눠, 무늬 없는(표준편차 < 3) 바탕색·흰색 칸을 빈 곳으로 센다.
#   py -3.12 work/research/cardshorts/emptyscan.py <그림.png|mp4> [...]      # mp4면 3초 간격 프레임
# 기준(10/10 사장님 지시): 빈 곳 40% 이하. 전체 화면과 아래 절반을 따로 찍는다. 아래 끝 12%(유튜브 제목 덮개)도 빈 곳으로 센다(빼 주지 않음).
import sys, subprocess, numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
BGS = [np.array([246, 247, 249]), np.array([255, 255, 255]), np.array([236, 239, 243])]   # 바탕 · 흰 판 · 회색 칩 바탕


def empty_ratio(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    H, W, _ = a.shape; c = W // 18; ny, nx = H // c, W // c
    e = np.zeros((ny, nx), bool)
    for y in range(ny):
        for x in range(nx):
            b = a[y * c:(y + 1) * c, x * c:(x + 1) * c].reshape(-1, 3)
            if b.std(0).max() < 3 and min(np.abs(b.mean(0) - g).max() for g in BGS) < 6: e[y, x] = True
    return e.mean(), e[ny // 2:].mean()


def frames(mp4, step=3):
    import imageio_ffmpeg, tempfile, glob, os
    d = tempfile.mkdtemp()
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', mp4, '-vf', f'fps=1/{step},scale=540:960', os.path.join(d, '%03d.png')], check=True)
    return sorted(glob.glob(os.path.join(d, '*.png')))


if __name__ == '__main__':
    rows = []
    for p in sys.argv[1:]:
        fs = frames(p) if p.endswith('.mp4') else [p]
        for i, f in enumerate(fs):
            t, b = empty_ratio(Image.open(f)); rows.append((t, b))
            print(f'{p if len(fs) == 1 else f"{i * 3:>3}초"}  전체 빈 곳 {t:.0%} · 아래 절반 {b:.0%}')
    if rows:
        T = np.array(rows); print(f'평균 전체 {T[:, 0].mean():.0%} · 아래 절반 {T[:, 1].mean():.0%} · 최대 전체 {T[:, 0].max():.0%} · 아래 절반 최대 {T[:, 1].max():.0%}')
