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


LIMIT0 = 0.40   # 10/15 회의 지시 ④: 0초 화면(목록·표지에 보이는 첫 장)도 40% 넘으면 막는다 — d1s_pension frame0 45%


def frame0(mp4):
    """mp4 맨 첫 장(n=0)의 (전체, 아래 절반) 빈 곳 비율. 3초 간격 재기는 0초를 540px로 줄여 재므로 첫 장을 따로 원본 크기로 잰다."""
    import imageio_ffmpeg, tempfile, os
    p = os.path.join(tempfile.mkdtemp(), 'f0.png')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-i', mp4, '-vf', r'select=eq(n\,0)', '-frames:v', '1', p], check=True)
    return empty_ratio(Image.open(p))



LIMIT_FADE = 0.10   # A51(10/21 thumb-gap-1021 ③): 0초 글자 반투명 금지 — g1s_asym·h1s_forest 0초 답 글이 회색으로 흐린데 빈 곳 0%로 통과
def fade0(mp4, n=6):
    """0초 장 글자가 덜 나타났는지: n프레임(0.2초) 뒤 흰 글자 픽셀(세 값 모두 235↑) 가운데, 0초에는 그 둘레 7×7 안에
    흰 픽셀(215↑)이 하나도 없는 비율. 글자가 페이드·떠오르기 중이면 높게 나온다(옛 g1s_asym 렌더). 반환 (비율, 흰 글자 픽셀 수)."""
    import imageio_ffmpeg, tempfile, os
    d = tempfile.mkdtemp(); ps = []
    for k in (0, n):
        p = os.path.join(d, f'f{k}.png'); ps.append(p)
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-i', mp4, '-vf', rf'select=eq(n\,{k})', '-frames:v', '1', p], check=True)
    a0, a1 = (np.asarray(Image.open(p).convert('RGB')).min(2) for p in ps)
    txt = a1 >= 235; w0 = a0 >= 215
    from numpy.lib.stride_tricks import sliding_window_view
    pad = np.pad(w0, 3); near = sliding_window_view(pad, (7, 7)).any((2, 3))
    tot = int(txt.sum())
    return (float((txt & ~near).sum()) / tot if tot else 0.0), tot


def gate_fade0(mp4, today=None):
    """ytupload 관문: 세로 영상만. 10/23부터 거부, 그 전엔 경고(이미 만든 렌더본이 칸을 놓치지 않게). 고치기 = 틀(C2P·C1S·M1S)이 10/21부터 0초 장면을 다 나타난 꼴로 그리니 다시 렌더."""
    import datetime as dt
    from PIL import Image as _I
    import imageio_ffmpeg, tempfile, os
    p = os.path.join(tempfile.mkdtemp(), 'sz.png')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-i', mp4, '-frames:v', '1', p], check=True)
    w, h = _I.open(p).size
    if h <= w: return True, '0초 글자 관문: 가로 영상 — 안 잼'
    r, t = fade0(mp4)
    if r <= LIMIT_FADE: return True, f'0초 글자 관문 통과: 덜 나타난 글자 {r:.0%} (기준 {LIMIT_FADE:.0%} 이하, A51)'
    msg = f'0초 글자 관문: 0.2초 뒤 흰 글자 {t}px 중 {r:.0%}가 0초엔 안 보이거나 흐림(A51, 기준 {LIMIT_FADE:.0%}) — 10/21 뒤 틀로 다시 렌더'
    if (today or dt.date.today().isoformat()) >= '2026-10-23': return False, msg
    return True, '[경고·10/23부터 거부] ' + msg

if __name__ == '__main__':
    rows = []
    for p in sys.argv[1:]:
        if p.endswith('.mp4'):
            r, t = fade0(p); print(f'{p}  0초 덜 나타난 글자 {r:.0%} (흰 글자 {t}px, 기준 {LIMIT_FADE:.0%} 이하)')
        fs = frames(p) if p.endswith('.mp4') else [p]
        for i, f in enumerate(fs):
            t, b = empty_ratio(Image.open(f)); rows.append((t, b))
            print(f'{p if len(fs) == 1 else f"{i * 3:>3}초"}  전체 빈 곳 {t:.0%} · 아래 절반 {b:.0%}')
    if rows:
        T = np.array(rows); print(f'평균 전체 {T[:, 0].mean():.0%} · 아래 절반 {T[:, 1].mean():.0%} · 최대 전체 {T[:, 0].max():.0%} · 아래 절반 최대 {T[:, 1].max():.0%}')
