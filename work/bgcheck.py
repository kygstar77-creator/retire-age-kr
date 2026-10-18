# 디자인 관문 — 쇼츠는 v3(10/16) 그대로, 롱폼은 10/17 화면 기준(research/longform/visual-gap-1017.md 7절 · research/visual/design-spec-1016.md 9절)으로 바꿨다.
# 렌더본을 1초마다 뜯어 본다.
# [쇼츠·세로] 10/16 v3 그대로(사장님 "모든 쇼츠 롱폼에 저렇게 영상 넣으면 되겠다")
#   ① 배경: 글자·판이 없는 가장자리(왼쪽 0~40·오른쪽 900~1080 × y 300~1240, 아래 y 1320~1900)가 단색·단순 그라데이션이면 '배경 없음'.
#      세 곳 중 두 곳 이상이 사진처럼 섞인 색이어야 그 프레임 통과. 프레임 90% 이상 통과 + 3초 넘게 연달아 걸리면 거부.
#   ② 자막: 자막 띠 y 1100~1240·가로 가운데에 높이 기준(글자 상자 56px = 약 2.9%, 72px 글자 기준 v3) 이상 줄이 프레임 70% 이상.
# [롱폼·가로] 10/17 — '모든 장면 뒤 실사 배경'(v3) 요구는 뺐다. 경쟁 롱폼 배경 5/5 실사는 대담 영상이라서였다(실사 B-roll 0~2.4%).
#   얼굴 없는 채널 기준은 수페TV 3편 전체 길이 실측이다(visual-gap-1017 5절).
#   ① 실사 장면(화면을 꽉 채운 실사 — 판 뒤에 깐 배경은 아님) 전체의 10% 이상     (수페 7.7~22.4%, R-1·H-1 0%, P-1 5.1%)
#   ② 화면 전체 컷(ffmpeg scene 0.3, 320px) 분당 3회 이상                           (수페 2.9~4.4, R-1 0, H-1 1.3, P-1 4.5)
#   ③ 같은 판(컷과 컷 사이, 실사 아닌 구간) 20초 이하 — 10/19 둘로 나눔(design-spec-1016 §10, quality-gap-1019 ②):
#      판 안에서 8초 안에 새 요소(점·선·꼬리표·칸)가 계속 붙으면 '움직이는 판' → 40초까지(수페 2:17→2:47 핀 1→4개). 아니면 20초 그대로(TQQQI 60초 정지 판).
#      요소 추가 = 1초 간격 두 프레임 사이 새로 생긴 잉크(바탕과 다른 점, 320×180, 보드 안만 — 자막 띠 바뀜은 빼고)가 보드의 0.15% 이상. 앞 프레임 잉크를 2점 넓혀 빼므로 천천히 다가가기(1.00→1.03)는 세지 않는다.
#      컷 분당(②)에는 넣지 않는다 — ②는 화면 통째 바뀜을 재는 값이다.
#   ④ 판 화면의 가장 큰 글자 줄 높이 중앙값 9% 이상                                 (수페 9.1~9.6%, 우리 5.4~6.7%)
#   ⑤ 판 화면의 글자 줄 수 중앙값 8줄 이하                                          (수페 7~9, 우리 10~13)
#   ④⑤는 visual-gap과 같은 법으로 잰다: 426×240으로 줄였다 852×480으로 키운 프레임에 RapidOCR 글자 찾기(읽지 않음), 가운데 높이 80% 위 상자만.
#   실사 판정: 426×240 위 80%에서 밝기 기울기 3 미만인 '평평한 점'이 45% 미만. 10/17 렌더본 실측: 판(R-1·P-1·T-1 배경 깐 판 포함) 0.52~0.85,
#   P-1 실사 장 머리(StockShot, 글자 쪽 어둡게) 0.12~0.39. 남의 영상(유튜브 압축·종이 질감 판)에는 맞지 않는다 — 우리 렌더본 전용.
#   이 기준은 '얼굴 없는 그래픽 채널의 표준'에 맞추는 바닥이다. 같은 채널 안에서 화면은 조회를 가르지 않았다(visual-gap 3절).
#   py -3.12 work/bgcheck.py <mp4 …>          # 걸리면 종료코드 1 · 결과 <mp4>.bgcheck.json(크기·수정시각·기준 같으면 다시 안 잼)
# 올리기 관문: ytupload.upload()·ytlong(롱폼 렌더본)·research/cardshorts/*clips_up.py가 gate(mp4)를 부른다.
import os, sys, json
import numpy as np

VERSION = 'shorts design-v3-1016 bg+cap v1 | long visual-gap-1017 v1 + add-1019'
CAP_BAND = (1100, 1240); CAP_MIN_H = 56; CAP_FRAC = 0.70
BG_FRAC = 0.90; BG_RUN = 3
# 롱폼(10/17)
LIVE_MIN = 0.10; CUT_PM = 3.0; BOARD_MAX = 20.0; BIG_MIN = 9.0; LINES_MAX = 8
FLAT_LIVE = 0.45; SCENE = 0.3
BOARD_MOVE_MAX = 40.0; ADD_GAP = 8.0; ADD_MIN = 0.0015   # 10/19 움직이는 판


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
    if not vertical: return vertical, scan_long(mp4)
    fr = []
    for t, img in safezone.frames(mp4, 1.0):
        b, parts = frame_bg(img)
        c = frame_cap(img) if vertical else None
        fr.append({'t': round(t, 1), 'bg': b, 'parts': parts, 'cap': c})
    return vertical, fr


# ───────── 롱폼(10/17) ─────────
def flatness(img):
    """426×240으로 줄인 화면 위 80%에서 밝기 기울기 3 미만인 점의 비율. 판(흰 보드·단색)은 높고 실사는 낮다."""
    import cv2
    s = cv2.resize(img, (426, 240), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(s, cv2.COLOR_RGB2GRAY)[:192].astype(np.float32)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    m = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    return float((m < 3).mean())


def text_lines(img):
    """(가장 큰 글자 줄 높이 %, 글자 줄 수) — visual-gap-1017 ocrsize와 같은 법(자막 띠 = 상자 가운데가 아래 20%면 뺀다)."""
    import cv2, safezone
    s = cv2.resize(cv2.resize(img, (426, 240), interpolation=cv2.INTER_AREA), (852, 480), interpolation=cv2.INTER_CUBIC)
    r, _ = safezone._engine()(s[:, :, ::-1].copy(), use_det=True, use_cls=False, use_rec=False)
    hs = []
    for b in (r or []):
        b = np.array(b, dtype=float); y0, y1 = b[:, 1].min() / 480, b[:, 1].max() / 480
        if (y0 + y1) / 2 < 0.80: hs.append(y1 - y0)
    return round(max(hs, default=0) * 100, 2), len(hs)


def cuts(mp4):
    """화면 전체 컷 시각(초) — ffmpeg scene 점수 > SCENE, 320px로 줄여서(visual-gap-1017 proc.scene_ff와 같은 법)."""
    import subprocess, re, imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-i', mp4, '-vf', f"scale=320:-2,select='gt(scene,{SCENE})',metadata=print", '-an', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = []
    for line in r.stderr.splitlines():
        m = re.search(r'pts_time:([\d.]+)', line)
        if m: out.append(round(float(m.group(1)), 2))
    return sorted(set(out))


def ink(img):
    """바탕과 다른 점(잉크) — 320×180, 가장 흔한 밝기(바탕)에서 40 넘게 벗어나거나 채도 60 넘는 점."""
    import cv2
    s = cv2.resize(img, (320, 180), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(s, cv2.COLOR_RGB2GRAY); hsv = cv2.cvtColor(s, cv2.COLOR_RGB2HSV)
    bgv = int(np.bincount(g.ravel(), minlength=256).argmax())
    m = (np.abs(g.astype(np.int16) - bgv) > 40) | (hsv[:, :, 1] > 60)
    return m[39:142, 17:303]   # 보드(100~1820 × 236~852)만 — 자막 띠·제목·출처 줄이 바뀌는 건 요소 추가가 아니다


def added(prev, cur):
    """앞 프레임 잉크를 2점 넓힌 밖에 새로 생긴 잉크 비율(요소 추가). 다가가기·작은 흔들림은 넓힌 칸 안이라 0에 가깝다."""
    import cv2
    if prev is None: return 0.0
    grown = cv2.dilate(prev.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    return float((cur & ~grown).mean())


def scan_long(mp4):
    import safezone
    fr = []; prev = None
    for t, img in safezone.frames(mp4, 1.0):
        fl = flatness(img); live = fl < FLAT_LIVE
        mh, n = (None, None) if live else text_lines(img)
        cur = ink(img); ad = added(prev, cur); prev = cur
        fr.append({'t': round(t, 1), 'flat': round(fl, 3), 'live': live, 'maxh': mh, 'n': n, 'add': round(ad, 4)})
    return {'frames': fr, 'cuts': cuts(mp4)}


def judge_long(d):
    fr, cs = d['frames'], d['cuts']
    n = len(fr) or 1; dur = (fr[-1]['t'] + 1) if fr else 0
    for f in fr: f['live'] = f['flat'] < FLAT_LIVE
    live = round(sum(f['live'] for f in fr) / n, 3)
    cpm = round(len(cs) / (dur / 60), 2) if dur else 0
    # 같은 판: 컷과 컷 사이 구간 중 실사 프레임이 절반 미만인 구간의 길이
    # 10/19: 판 안 요소 추가 시각을 컷처럼 세서, 추가 사이(판 시작·끝 포함) 최장 간격이 ADD_GAP 이하면 '움직이는 판' → BOARD_MOVE_MAX까지
    edges = [0.0] + [c for c in cs if 0 < c < dur] + [dur]; runs = []
    for a, b in zip(edges, edges[1:]):
        inside = [f for f in fr if a <= f['t'] < b]
        if inside and sum(f['live'] for f in inside) < len(inside) / 2:
            adds = [f['t'] for f in inside[1:] if f.get('add', 0) >= ADD_MIN]
            marks = [a] + adds + [b]; gap = max(y - x for x, y in zip(marks, marks[1:]))
            lim = BOARD_MOVE_MAX if gap <= ADD_GAP else BOARD_MAX
            runs.append((round(b - a, 1), round(a, 1), lim, len(adds), round(gap, 1)))
    runs.sort(reverse=True)
    over = [r for r in runs if r[0] > r[2]]
    board = [f for f in fr if not f['live'] and f['maxh'] is not None]
    mh = float(np.median([f['maxh'] for f in board])) if board else 0.0
    ln = float(np.median([f['n'] for f in board])) if board else 0.0
    small = [f['t'] for f in board if f['maxh'] < BIG_MIN]; many = [f['t'] for f in board if f['n'] > LINES_MAX]
    why = []
    if live < LIVE_MIN: why.append(f'실사 장면 {live:.0%} < {LIVE_MIN:.0%}(관점·사례·비유·장 머리를 TallyBroll·StockShot 꽉 찬 실사로)')
    if cpm < CUT_PM: why.append(f'화면 전체 컷 분당 {cpm:.1f}회 < {CUT_PM:g}회(판 위 요소만 바꾸지 말고 판↔실사↔표로 화면을 통째 바꾼다)')
    if over: why.append(f'같은 판 기준 넘음(움직임 없는 판 {BOARD_MAX:g}초·8초 안 요소 추가 판 {BOARD_MOVE_MAX:g}초) ' + ', '.join(f'{int(r[1] // 60)}:{r[1] % 60:02.0f}~ {r[0]:.0f}초(한도 {r[2]:g}·추가 {r[3]}번·최장 간격 {r[4]:.0f}초)' for r in over[:5]))
    if board and mh < BIG_MIN: why.append(f'판 가장 큰 글자 중앙 {mh:.1f}% < {BIG_MIN:g}%(제목 100px 위 가운데·핵심 숫자 크게)')
    if board and ln > LINES_MAX: why.append(f'판 글자 줄 중앙 {ln:.0f}줄 > {LINES_MAX}줄(판 하나에 말 하나·숫자 둘까지)')
    s = {'live_frac': round(live, 3), 'cuts_pm': round(cpm, 2), 'board_max_s': runs[0][0] if runs else 0, 'big_med': round(mh, 2), 'lines_med': ln,
         'small_t': small[:12], 'many_t': many[:12], 'board_over': over[:12], 'board_runs': runs[:12], 'dur': dur}
    return not why, why, s


def judge(vertical, fr):
    if not vertical: return judge_long(fr)
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
    if 'live_frac' in s:   # 롱폼(10/17 기준)
        msg = (f"롱폼 화면 관문 {'통과' if o['ok'] else '걸림'}: 실사 {s['live_frac']:.0%}(≥{LIVE_MIN:.0%}) · 컷 분당 {s['cuts_pm']:.1f}(≥{CUT_PM:g}) · "
               f"같은 판 최장 {s['board_max_s']:.0f}초(정지 ≤{BOARD_MAX:g}·추가 판 ≤{BOARD_MOVE_MAX:g}, 넘음 {len(s.get('board_over', []))}) · 판 큰 글자 {s['big_med']:.1f}%(≥{BIG_MIN:g}) · 판 글자 줄 {s['lines_med']:.0f}(≤{LINES_MAX})" +
               ('' if o['ok'] else ' — ' + ' · '.join(o['why'])))
        return o['ok'], msg
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
