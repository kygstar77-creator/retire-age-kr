# M-1 쇼츠 렌더본 관문 재료 — 3초 간격 프레임 판·소리·치직·빈 곳·정지를 한 번에 잰다(판정은 사람이 판을 보고 review.md에).
#   py -3.12 work/research/cardshorts/m1clips_review.py <편이름>
# 만드는 것: cardshorts/<편>/sheet.png(ffmpeg fps=1/3 + tile) · measure.json
import os, sys, json, subprocess, glob, tempfile
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import imageio_ffmpeg
from PIL import Image
import emptyscan
FF = imageio_ffmpeg.get_ffmpeg_exe()


def main(name):
    d = os.path.join(HERE, name); os.makedirs(d, exist_ok=True)
    mp4 = os.path.join(WORK, 'video', 'out', name + '_ds.mp4')   # 디에서 통과본(렌더 → deess.py)
    info = subprocess.run([FF, '-hide_banner', '-i', mp4], capture_output=True, text=True, encoding='utf-8', errors='replace').stderr
    dur = [l.strip() for l in info.splitlines() if 'Duration' in l][0]
    streams = [l.strip() for l in info.splitlines() if 'Stream #' in l]
    # 소리: 평균·최대 음량
    vd = subprocess.run([FF, '-hide_banner', '-i', mp4, '-vn', '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace').stderr
    vol = {k: l.split(':')[-1].strip() for l in vd.splitlines() for k in ('mean_volume', 'max_volume') if k in l}
    # 3초 간격 프레임 판
    sheet = os.path.join(d, 'sheet.png')
    subprocess.run([FF, '-v', 'error', '-y', '-i', mp4, '-vf', 'fps=1/3,scale=270:480,tile=6x3', '-frames:v', '1', sheet], check=True)
    # 같은 프레임으로 빈 곳·정지(이웃 3초 프레임 차이) 재기 — 판정용 1초 간격도 같이
    tmp = tempfile.mkdtemp()
    subprocess.run([FF, '-v', 'error', '-i', mp4, '-vf', 'fps=1,scale=270:480', os.path.join(tmp, '%03d.png')], check=True)
    fs = sorted(glob.glob(os.path.join(tmp, '*.png')))
    arr = [np.asarray(Image.open(f).convert('L')).astype(np.float32) for f in fs]
    diff = [float(np.abs(arr[i] - arr[i - 1]).mean()) for i in range(1, len(arr))]
    # 정지: 연속 1초 차이가 0.3 미만(사실상 같은 그림)인 구간의 최장 길이
    run = best = 0; at = 0
    for i, x in enumerate(diff):
        run = run + 1 if x < 0.3 else 0
        if run > best: best, at = run, i + 1 - run
    em = [emptyscan.empty_ratio(Image.open(f)) for f in fs[::3]]
    m = {'duration': dur, 'streams': streams, 'volume': vol, 'frames_1s': len(fs), 'still_longest_s': best, 'still_from_s': at,
         'empty_mean': round(float(np.mean([e[0] for e in em])), 3), 'empty_max': round(float(np.max([e[0] for e in em])), 3),
         'empty_low_mean': round(float(np.mean([e[1] for e in em])), 3), 'empty_low_max': round(float(np.max([e[1] for e in em])), 3),
         'empty_each_3s': [[i * 3, round(e[0], 2), round(e[1], 2)] for i, e in enumerate(em)]}
    json.dump(m, open(os.path.join(d, 'measure.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in m.items() if k != 'empty_each_3s'}, ensure_ascii=False, indent=1))
    print('판:', sheet)


if __name__ == '__main__':
    main(sys.argv[1])
