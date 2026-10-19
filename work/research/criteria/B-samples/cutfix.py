# 쇼츠 컷 다시 재기 — 위·아래 고정 띠(제목·로고)가 ffmpeg scene 점수를 묽혀 컷을 놓친다(Turbo832 sheet: 눈으로 2초마다 바뀌는데 scene 0.3은 0).
# 그래서 영상에서 '움직이는 칸'(4fps 회색 90×160, 시간 표준편차 12 넘는 점이 30% 넘는 줄·칸)만 잘라 같은 scene 0.3으로 잰다.
#   py -3.12 cutfix.py <media 폴더>  → cutfix.json
import os, sys, json, re, subprocess
import numpy as np, cv2, imageio_ffmpeg
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]; FF = imageio_ffmpeg.get_ffmpeg_exe()
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
OURS = {x['id']: x['path'] for x in json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8')) if x['kind'] == 'short'}
jobs = [(v, os.path.join(M, f'short_{v}.v.mp4')) for _, v in S['short']] + list(OURS.items())
out_p = os.path.join(HERE, 'cutfix.json'); out = json.load(open(out_p, encoding='utf-8')) if os.path.exists(out_p) else {}
for vid, p in jobs:
    if vid in out or not os.path.exists(p): continue
    cap = cv2.VideoCapture(p); fps = cap.get(cv2.CAP_PROP_FPS) or 30; n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); W, H = cap.get(3), cap.get(4)
    fr = []
    step = max(1, int(fps / 4)); i = 0
    while True:   # 차례로 읽기(되감기 없이)
        ok = cap.grab()
        if not ok: break
        if i % step == 0:
            ok, f = cap.retrieve()
            if ok: fr.append(cv2.cvtColor(cv2.resize(f, (90, 160), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32))
        i += 1
    cap.release(); dur = n / fps
    a = np.array(fr); act = a.std(0) > 12 if len(a) > 2 else np.zeros((160, 90), bool)
    rows = np.where(act.mean(1) > 0.3)[0]; cols = np.where(act.mean(0) > 0.3)[0]
    if len(rows) < 8 or len(cols) < 8:
        out[vid] = {'dur': round(dur, 1), 'active': None, 'cuts_pm': 0.0, 'scene_med': round(dur, 1), 'note': '움직이는 칸 없음(정지 화면)'}
    else:
        y0, y1, x0, x1 = rows[0] / 160, (rows[-1] + 1) / 160, cols[0] / 90, (cols[-1] + 1) / 90
        vf = f"crop=iw*{x1 - x0:.3f}:ih*{y1 - y0:.3f}:iw*{x0:.3f}:ih*{y0:.3f},scale=320:-2,select='gt(scene,0.3)',metadata=print"
        r = subprocess.run([FF, '-hide_banner', '-i', p, '-vf', vf, '-an', '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        cuts = sorted({round(float(m.group(1)), 2) for m in re.finditer(r'pts_time:([\d.]+)', r.stderr)})
        e = [0.0] + [c for c in cuts if 0 < c < dur] + [dur]; segs = [b - a2 for a2, b in zip(e, e[1:]) if b > a2]
        out[vid] = {'dur': round(dur, 1), 'active': [round(y0, 2), round(y1, 2), round(x0, 2), round(x1, 2)], 'cuts': cuts,
                    'cuts_pm': round(len(cuts) / (dur / 60), 2), 'scene_med': round(float(np.median(segs)), 2), 'scene_max': round(max(segs), 1)}
    json.dump(out, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(vid, out[vid].get('active'), out[vid]['cuts_pm'], out[vid]['scene_med'], flush=True)
