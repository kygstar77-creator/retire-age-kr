# 쇼츠 화면 밝기·채도 재기(10/26 motion, today.md 10/27 지시 '실사 틀 배경 밝기 다시 재기')
#   py -3.12 bright.py <mp4...>  → 편마다 1초 1장(108×192)으로 줄여
#     Y   = 칸 밝기 중앙(BT.601 luma, 0~255)의 편 중앙
#     Ybg = 흰 글자(235↑)·검은 테두리(20↓) 뺀 화소의 밝기 중앙(배경 밝기 어림)
#     S   = HSV 채도 중앙(0~255)
#     Ymid = 가운데 띠(높이 30~70%) 밝기 중앙 — 위아래 검은 띠(레터박스) 편을 칸 전체 중앙이 어둡게 잡는 것 보정
#   결과 json 한 줄씩 stdout
import sys, os, json, subprocess
import numpy as np
FF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'bin', 'ffmpeg.exe')
W, H = 108, 192
def measure(p):
    r = subprocess.run([FF, '-v', 'error', '-i', p, '-vf', f'fps=1,scale={W}:{H}', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = a.size // (W * H * 3)
    if n == 0: return None
    f = a[:n * W * H * 3].reshape(n, H, W, 3).astype(np.float32)
    y = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
    mx, mn = f.max(-1), f.min(-1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1) * 255, 0)
    Y = [float(np.median(k)) for k in y]
    Ybg = []
    for k in y:
        m = (k < 235) & (k > 20)
        Ybg.append(float(np.median(k[m])) if m.mean() > 0.1 else float(np.median(k)))
    S = [float(np.median(k)) for k in s]
    Ymid = [float(np.median(k[int(H * 0.3):int(H * 0.7)])) for k in y]
    return dict(file=os.path.basename(p), n=n, Y=round(float(np.median(Y)), 1), Ybg=round(float(np.median(Ybg)), 1), Ymid=round(float(np.median(Ymid)), 1),
                S=round(float(np.median(S)), 1), Y25=round(float(np.percentile(Y, 25)), 1), Y75=round(float(np.percentile(Y, 75)), 1),
                dark=round(float(np.mean(np.array(Y) < 60)), 2))
for p in sys.argv[1:]:
    print(json.dumps(measure(p), ensure_ascii=False), flush=True)
