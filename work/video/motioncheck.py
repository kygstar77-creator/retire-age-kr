"""렌더본 화면 변화 관문(2026-10-02 motion). 경쟁 대비 '멈춘 화면'을 숫자로 잰다.
쓰는 법: py -3.12 work/video/motioncheck.py <mp4> [--max-static 15] [--hook 3] [--thr 1.0]
- 그래픽 영역만 본다: 아래 26%(자막·출처)를 잘라 낸다 — 자막만 바뀌는 건 화면 변화로 치지 않는다.
- 4fps·160x90 회색으로 줄여, 각 순간을 1초 전 프레임과 비교한 평균 밝기 차(0~255)가 thr(기본 1.0 — 작은 꼬리표 하나 나타남이 1.1~1.2)를 넘으면 '움직이는 중'.
  (scene 점수 방식은 선이 천천히 그려지거나 숫자가 서서히 나타나는 걸 못 잡아 E-1 첫 16.8초를 정지로 잘못 셌다 — 10/2 폐기)
- 경쟁 실측(10/2, 90초 구간 같은 방법): 매경 rmajvVmxGxM 움직임 88%·최장 정지 6.0초 / 수페TV jSP16zTrEHY 12%·23.8초 / 신과대 cBFFyqiKFRs 8%·34.8초.
  우리 E-1 14%·26.2초, D-1 리허설 17%·30.8초. 기본 15초 = 수페TV와 매경 사이(우리가 1등보다 낫게 하는 선).
- 실패 조건: 첫 hook초 안에 움직임 0 / 움직임 없는 구간이 max-static초 초과.
"""
import subprocess, sys, imageio_ffmpeg
import numpy as np

W, H, FPS = 160, 90, 4

def motion(path):
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-i', path, '-vf',
                        f'fps={FPS},crop=iw:ih*0.74:0:0,scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W).astype(np.int16)
    d = np.zeros(len(fr))
    d[FPS:] = np.abs(fr[FPS:] - fr[:-FPS]).mean(axis=(1, 2))
    return d

def main():
    a = sys.argv[1:]; path = a[0]
    opt = lambda k, v: float(a[a.index(k) + 1]) if k in a else v
    mx, hook, thr = opt('--max-static', 15.0), opt('--hook', 3.0), opt('--thr', 1.0)
    d = motion(path); dur = len(d) / FPS
    mv = d > thr
    runs, st = [], None
    for i, m in enumerate(list(mv) + [True]):
        if not m and st is None: st = i
        if m and st is not None: runs.append(((i - st) / FPS, st / FPS)); st = None
    runs.sort(reverse=True)
    first = (np.argmax(mv[FPS:]) + FPS) / FPS if mv[FPS:].any() else dur
    bad = [r for r in runs if r[0] > mx]
    share = mv.mean() * 100
    print(f'길이 {dur:.1f}s · 움직이는 시간 {share:.0f}% · 첫 움직임 {first:.1f}s · 최장 정지 {runs[0][0] if runs else 0:.1f}s · {mx:.0f}초 넘는 정지 {len(bad)}곳')
    for g, s in bad[:12]: print(f'  정지 {g:.1f}s  {int(s//60)}:{s%60:04.1f}~')
    ok = first <= hook and not bad
    print('통과' if ok else '실패'); sys.exit(0 if ok else 1)

if __name__ == '__main__': main()
