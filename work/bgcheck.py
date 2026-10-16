# 디자인 기준 v3 관문(10/16 영상 디자인 총괄 — 사장님 "모든 쇼츠 롱폼에 저렇게 영상 넣으면 되겠다", 기준 research/visual/design-spec-1016.md)
# 렌더본을 1초마다 뜯어 두 가지를 본다.
#   ① 배경: 글자·판이 없는 가장자리(쇼츠: 왼쪽 0~40·오른쪽 900~1080 × y 300~1240, 아래 y 1320~1900 / 롱폼: 왼쪽 0~90·오른쪽 1830~1920 × y 240~850, 위 y 0~30)가
#      단색·단순 그라데이션이면 '배경 없음'. 세 곳 중 두 곳 이상이 사진처럼 섞인 색이어야 그 프레임 통과. 프레임 90% 이상 통과 + 3초 넘게 연달아 걸리면 거부.
#   ② 자막(세로 쇼츠만): 자막 띠 y 1100~1240·가로 가운데에 높이 기준(글자 상자 56px = 약 2.9%, 72px 글자 기준 v3) 이상 줄이 프레임 70% 이상.
#   py -3.12 work/bgcheck.py <mp4 …>          # 걸리면 종료코드 1 · 결과 <mp4>.bgcheck.json(크기·수정시각·기준 같으면 다시 안 잼)
# 올리기 관문: ytupload.upload()·research/cardshorts/*clips_up.py가 gate(mp4)를 부른다.
import os, sys, json
import numpy as np

VERSION = 'design-v3-1016 bg+cap v1'
CAP_BAND = (1100, 1240); CAP_MIN_H = 56; CAP_FRAC = 0.70
BG_FRAC = 0.90; BG_RUN = 3


def _regions(img):
    h, w = img.shape[:2]
    if h > w:   # 1080×1920 기준 좌표를 실제 크기로
        sx, sy = w / 1080, h / 1920
        R = [(0, 300, 40, 1240), (900, 300, 1080, 1240), (0, 1320, 1080, 1900)]
    else:
        sx, sy = w / 1920, h / 1080
        R = [(0, 240, 90, 850), (1830, 240, 1920, 850), (1000, 866, 1800, 924)]   # 보드(100~1820 × 236~852) 밖: 왼쪽·오른쪽 띠, 보드 아래·자막 위 오른쪽(출처 줄은 왼쪽)
    return [img[int(y0 * sy):int(y1 * sy), int(x0 * sx):int(x1 * sx)] for x0, y0, x1, y1 in R]


def photo_like(reg):
    """사진처럼 색이 섞였나: 16단계로 줄인 색(4096칸) 중 0.3% 넘게 쓰인 칸이 8개 이상. 단색·두 색 띠·검은 그라데이션은 1~5칸, 실사는 8~47칸(10/16 실측)."""
    a = (reg.reshape(-1, 3) // 16).astype(np.int32)
    if len(a) < 50: return False
    c = np.bincount(a[:, 0] * 256 + a[:, 1] * 16 + a[:, 2], minlength=4096) / len(a)
    return bool((c >= 0.003).sum() >= 8)


def frame_bg(img):
    ok = [photo_like(r) for r in _regions(img)]
    return sum(ok) >= 2, ok


def frame_cap(img):
    import safezone
    h, w = img.shape[:2]
    for x0, y0, x1, y1 in safezone.boxes(img):
        cy = (y0 + y1) / 2; cx = (x0 + x1) / 2
        if CAP_BAND[0] <= cy <= CAP_BAND[1] and 250 <= cx <= 690 and (y1 - y0) >= CAP_MIN_H: return True
    return False


def scan(mp4):
    import safezone
    vertical = safezone.is_vertical(mp4)
    fr = []
    for t, img in safezone.frames(mp4, 1.0):
        b, parts = frame_bg(img)
        c = frame_cap(img) if vertical else None
        fr.append({'t': round(t, 1), 'bg': b, 'parts': parts, 'cap': c})
    return vertical, fr


def judge(vertical, fr):
    n = len(fr) or 1
    bg_ok = sum(f['bg'] for f in fr) / n
    run = best = 0
    for f in fr:
        run = run + 1 if not f['bg'] else 0; best = max(best, run)
    why = []
    if bg_ok < BG_FRAC: why.append(f'배경 실사 프레임 {bg_ok:.0%} < {BG_FRAC:.0%}')
    if best > BG_RUN: why.append(f'배경 없는 화면 {best}초 연속(기준 {BG_RUN}초 이하)')
    cap = None
    if vertical:
        cap = sum(bool(f['cap']) for f in fr) / n
        if cap < CAP_FRAC: why.append(f'자막 기준(띠 y {CAP_BAND[0]}~{CAP_BAND[1]}·상자 높이 {CAP_MIN_H}px 이상) 프레임 {cap:.0%} < {CAP_FRAC:.0%}')
    bad = [f['t'] for f in fr if not f['bg']][:12]
    return not why, why, {'bg_frac': round(bg_ok, 3), 'bg_run': best, 'cap_frac': None if cap is None else round(cap, 3), 'bg_fail_t': bad}


def gate(mp4, quiet=False):
    st = os.stat(mp4); key = {'size': st.st_size, 'mtime': int(st.st_mtime), 'std': VERSION}
    cp = mp4 + '.bgcheck.json'
    o = None
    if os.path.exists(cp):
        try:
            o = json.load(open(cp, encoding='utf-8'))
            if o.get('key') != key: o = None
        except Exception: o = None
    if o is None:
        vertical, fr = scan(mp4)
        ok, why, s = judge(vertical, fr)
        o = {'key': key, 'ok': ok, 'why': why, 'sum': s, 'frames': fr}
        json.dump(o, open(cp, 'w', encoding='utf-8'), ensure_ascii=False)
    s = o['sum']
    msg = (f"디자인 관문 {'통과' if o['ok'] else '걸림'}: 배경 실사 {s['bg_frac']:.0%}(연속 없음 최장 {s['bg_run']}초)" +
           (f" · 자막 기준 {s['cap_frac']:.0%}" if s.get('cap_frac') is not None else '') + ('' if o['ok'] else ' — ' + ' · '.join(o['why']) + (f" · 배경 없는 초 {s['bg_fail_t']}" if s['bg_fail_t'] else '')))
    return o['ok'], msg


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    bad = 0
    for p in sys.argv[1:]:
        ok, msg = gate(p); print(os.path.basename(p), msg); bad += not ok
    sys.exit(1 if bad else 0)
