# 자가개선 루프 — 사장님 2026-09-23 "루프를 돌려라. 내가 물어보지 않아도 전부 발전하게".
#   py -3.12 work/loop.py            → 한 바퀴 돌고 work/loop_log.json에 기록
# 한 바퀴:
#   1) 수집  경쟁 채널 썸네일·제목·조회(ytdesign) + 우리 채널 성과(ytupload stats) + 블로그/카페 성과(perf·visitors)
#   2) 측정  경쟁 썸네일을 픽셀로 재고(thumbstat) 우리 썸네일도 같은 자로 잰다
#   3) 비교  우리 값 − 경쟁 상위 값 = 차이(gap). 차이가 큰 항목을 고른다
#   4) 조정  design.json(생성기가 읽는 값)을 그 방향으로 한 칸 움직인다. 한 번에 최대 3개만.
#   5) 기록  무엇을 왜 바꿨는지, 지난번 조정 뒤 성과가 올랐는지 loop_log.json에 남긴다
# 규칙: 한 번에 다 바꾸지 않는다(무엇이 효과였는지 알 수 없어서). 성과가 내려가면 되돌린다.
import sys, os, re, json, glob, time, subprocess, statistics, hashlib
# 2026-09-26: 출력을 줄 단위로 흘린다. 전에는 기본(블록) 버퍼라, 이 바퀴가 도중에 죽으면
# 그때까지 찍은 것이 전부 버퍼에 남은 채 사라졌다 — 파일로 받아 보면 0바이트다.
# 실제로 이날 14:00 바퀴가 도중에 죽었는데 어디까지 갔는지 아무 흔적이 없었고,
# 11:52 회차가 죽은 것도 같은 이유로 진단할 수 없었다. 한 바퀴가 6~10분 걸리므로
# 줄마다 흘려도 값은 무시할 만하고, 대신 죽어도 어디서 죽었는지가 남는다.
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
DESIGN = os.path.join(HERE, 'design.json'); LOG = os.path.join(HERE, 'loop_log.json')
SPEC = os.path.join(R, 'yt', 'design', 'spec.json')
SPEC_FP = os.path.join(R, 'yt', 'design', 'spec.fingerprint.json')
SAMPLE = os.path.join(R, 'yt', 'design', 'ours'); os.makedirs(SAMPLE, exist_ok=True)
PY = [sys.executable]
LOCK = os.path.join(HERE, '.loop.lock')

def take_lock(stale=3600):
    """한 번에 한 바퀴만 돈다. 2026-09-24 15시 회차에 바퀴 둘이 겹쳐 돌아 격자 측정이 섞였다 —
    앞 바퀴가 그린 샘플을 뒤 바퀴가 재는 바람에 text_spread 격자 7점이 전부 같은 값(0.2653)으로 나왔고,
    그 '전부 같음'을 최선으로 골라 손잡이를 0.45→0.0 으로 옮겨 판형 오차가 0.2653 → 2.213 으로 뛰었다."""
    try:
        if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < stale:
            age = int(time.time() - os.path.getmtime(LOCK))
            # 나이만 보던 것을 2026-09-25 125회차에 고쳤다. 앞 바퀴가 죽으면(타임아웃·재부팅) 락 파일이
            # 그대로 남고, 그 뒤 한 시간(stale) 동안 오는 바퀴가 **전부** 그냥 돌아간다. 두 시간마다 도는
            # 회차이므로 한 번 죽으면 다음 회차까지 통째로 날아간다 — 실제로 이번 회차가 그렇게 막혔다
            # (죽은 PID 753288 이 604초째 '돌고 있다'고 나왔다). 주인이 살아 있는지 물어보면 되는 일이다.
            # 판단 기준은 naverpost 가 쓰는 것을 그대로 빌려 쓴다 — 두 군데서 다르게 세지 않으려고.
            owner = ''
            try: owner = open(LOCK, encoding='utf-8').read().strip()
            except Exception: pass
            alive = True
            try:
                sys.path.insert(0, HERE); import naverpost
                alive = bool(owner) and naverpost._alive(owner)
            except Exception:
                alive = True      # 못 물어보면 막는 쪽으로 둔다(겹쳐 도는 것이 더 나쁘다)
            if alive:
                print(f'다른 바퀴가 {age}초째 돌고 있다 — 이번 바퀴는 돌지 않는다 ({LOCK})')
                return False
            print(f'죽은 락을 치운다 — 주인 {owner or "?"} 는 살아 있지 않다 ({age}초 전에 잡힌 락)')
        open(LOCK, 'w', encoding='utf-8').write(str(os.getpid()))
        global HELD; HELD = True
        return True
    except Exception:
        return True

HELD = False      # 이 프로세스가 락을 잡았나. 안 잡았으면 풀 자격도 없다

def drop_lock():
    """내가 잡은 락만 푼다.

    2026-09-25 121회차에 실측으로 찾았다. 아래 `finally: drop_lock()` 은 main() 이 **락을 못 잡아
    그냥 돌아온 경우에도** 실행된다 — 즉 못 들어간 바퀴가 나가면서 **돌고 있는 바퀴의 락을 지운다**.
    그래서 락은 두 번째 바퀴가 오는 순간 없는 것이 된다: 그 두 번째가 락을 지우고 나가면
    세 번째는 문이 열린 것으로 보고 그대로 들어와 같은 샘플 파일에 겹쳐 그린다.
    막으려고 만든 사고(2026-09-24 격자 측정 섞임)가 그대로 다시 날 수 있는 상태였다.
    실측: 내 바퀴가 20:04:43 에 락을 잡고 돌고 있었는데 20:11:56 에 락 파일이 사라졌다.
    그때 살아 있던 프로세스는 내 loop.py 와 그 자식 thumb.py 뿐이었다 — 즉 못 들어간 바퀴가
    지나가며 지운 것이다(그 바퀴가 그리지는 않았으므로 이번 측정은 섞이지 않았다)."""
    if not HELD: return
    try: os.remove(LOCK)
    except Exception: pass

DEFAULT = {   # 생성기가 읽는 값. 처음 값은 2026-09-23 첫 측정에서 나온 경쟁 상위 중앙값
    'long':  {'yellow': 0.050, 'contrast': 0.372, 'white': 0.101, 'text_top': 0.911, 'bright': 0.447},
    'short': {'yellow': 0.007, 'contrast': 0.187, 'white': 0.012, 'text_mid': 0.430, 'bright': 0.216},
    'title': {'quote': True, 'region': True, 'number': True, 'warn': False, 'len': 33},
    'video': {'scene_sec': 9.0, 'total_sec': 45, 'zoom': 0.0009},
    'step': 0,
}

def sh(*a, timeout=1800):
    """시간이 넘으면 그때까지 받은 출력만 돌려준다.

    예전에는 subprocess.run 의 TimeoutExpired 가 그대로 올라와 바퀴 전체가 죽었다. 수집처럼 오래 걸리는
    일에 상한을 걸면 그 상한이 곧 바퀴를 죽이는 장치가 된다 — 수집은 다음 회차에 이어받으면 되는 일이다."""
    try:
        r = subprocess.run(PY + list(a), capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout, cwd=os.path.dirname(HERE))
        return (r.stdout or '') + (r.stderr or '')
    except subprocess.TimeoutExpired as e:
        got = (e.stdout or '') + (e.stderr or '')
        if isinstance(got, bytes): got = got.decode('utf-8', 'ignore')
        return got + ('\n[시간초과 %d초 — 여기까지만 받았다]' % timeout)

def spec_fingerprint():
    """경쟁 썸네일 측정이 이번에도 같은 답을 낼지 미리 알아보는 지문.

    thumbstat 은 design/*/*.jpg 를 픽셀로 재어 spec.json 을 만든다. 같은 파일을 넣으면 같은 값이 나오는
    순수 계산이라, 파일이 하나도 안 바뀌었으면 다시 재도 답이 같다. 그런데 89~95회차 일곱 바퀴가
    전부 같은 296장을 다시 쟀다 — 수집은 12시간마다라 그 사이 파일이 늘지 않는다.
    2026-09-25 실측: 재측정 한 번이 23.0초, 그날 95회차 한 바퀴 전체가 345초였다(6.7%).
    지문은 파일 목록·크기·수정시각과 thumbstat.py 자신의 수정시각이다 — 재는 자가 바뀌면 다시 잰다."""
    D = os.path.join(R, 'yt', 'design')
    items = []
    for f in sorted(glob.glob(os.path.join(D, '*', '*.jpg'))):
        try: st = os.stat(f)
        except OSError: continue
        items.append((os.path.relpath(f, D).replace(os.sep, '/'), int(st.st_mtime), st.st_size))
    try: ts = int(os.path.getmtime(os.path.join(HERE, 'thumbstat.py')))
    except OSError: ts = 0
    return {'n': len(items), 'thumbstat': ts,
            'hash': hashlib.sha1(repr(items).encode('utf-8')).hexdigest()}


def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def our_shorts_stats():
    """우리가 올린 영상의 조회수 — 조정이 효과 있었는지 보는 유일한 답.
    id·공개상태까지 돌려준다. 2026-09-24에 알아낸 것: 최근 10편을 '합계'로 재면 새 영상을 올릴 때마다
    합계가 무너진다(2089 → 120 → 6). 새로 올린 영상은 조회 0이라 최신 10편 합계가 떨어지는 것이지
    디자인이 나빠진 게 아니다. 그래서 회차 판정은 채널 총조회(누적, 절대 안 줄어든다)로 한다."""
    out = sh(os.path.join(HERE, 'ytupload.py'), 'stats')
    vids = re.findall(r'(\d{4}-\d{2}-\d{2})\s+(\d+)\s*회\s*\|\s*(\w+)\s*\|\s*([\w-]{6,})\s*\|\s*(.+)', out)
    rows = [{'date': d, 'views': int(v), 'privacy': pv, 'id': vid, 'title': t.strip()} for d, v, pv, vid, t in vids]
    if not rows:   # 옛 형식(아이디 없음)도 읽는다
        rows = [{'date': d, 'views': int(v), 'privacy': '?', 'id': '', 'title': t.strip()}
                for d, v, t in re.findall(r'(\d{4}-\d{2}-\d{2})\s+(\d+)\s*회\s*\|\s*(.+)', out)]
    m = re.search(r'총조회\s*(\d+)', out)
    total = int(m.group(1)) if m else None
    return rows, total

def render_samples(keep_chart=False):
    """지금 설정으로 샘플 썸네일을 새로 그린다 — 이게 있어야 조정 효과가 다음 측정에 나타난다.
    쇼츠 샘플을 '배경 없이' 그리던 것이 6회차 막힘의 진짜 원인이었다(step19~26). 실제 쇼츠(shorts.py:116)는
    첫 장면 자료 화면을 배경으로 깔고 썸네일을 만드는데, 여기서만 맨 그라데이션 위에 글자 두 줄을 그렸다.
    자료 화면이 없으면 글자 말고는 가장자리가 없어 text_top이 손잡이를 어떻게 돌려도 0.0329에 얼어붙는다
    (실측: 같은 설정 + 차트 배경 → text_top 0.0329→0.5178, text_mid 0.1167→0.3902, text_bot 0.1299→0.2211).
    경쟁은 전부 사진·자료 위에 글자를 얹은 판형이라, 배경 없는 샘플로 재는 것은 애초에 다른 물건을 재는 것이었다.
    그래서 production이 실제로 쓰는 자료 화면 세 종류(차트·히트맵·부동산 화면) 위에 그려 중앙값을 낸다(2026-09-23).
    """
    for p in glob.glob(os.path.join(SAMPLE, '*.png')):
        if keep_chart and os.path.basename(p) == '_bg_chart.png': continue
        try: os.remove(p)
        except OSError: pass
    shots = os.path.join(R, '_shots')
    chart = os.path.join(SAMPLE, '_bg_chart.png')   # 이름이 short*/long* 이 아니라 측정에서는 빠진다
    if not (keep_chart and os.path.exists(chart)):
        sh(os.path.join(HERE, 'chartimg.py'), 'bar', '서울 구별 전세가율', chart,
           '금천=61', '구로=58', '중랑=56', '강북=55', '노원=53', '강남=36',
           '--unit', '%', '--hi', '3', '--short', '--source', '국토부 실거래가')
    bgs = [chart, os.path.join(shots, 'heatmap_re_jeonse_2026-09-23.png'), os.path.join(shots, 'naverland_test.png')]
    for i, bg in enumerate([b for b in bgs if os.path.exists(b)]):
        sh(os.path.join(HERE, 'thumb.py'), '금천 61% 강남 36%', '서울 전세가율 전수 조사',
           os.path.join(SAMPLE, f'short{i}.png'), bg, '--short')
    bg = os.path.join(shots, 'heatmap_2026-09-23.png')
    sh(os.path.join(HERE, 'thumb.py'), '전세가율 61% vs 36%', '서울 25개 구 전부 계산', os.path.join(SAMPLE, 'long.png'), *( [bg] if os.path.exists(bg) else [] ))

def measure_ours():
    """우리 썸네일을 경쟁과 같은 자로 잰다. 쇼츠는 배경 종류별로 여러 장이라 뒤에서 중앙값을 낸다"""
    sys.path.insert(0, HERE)
    import thumbstat
    rows = []
    for pat, isshort in (('short*.png', True), ('long*.png', False)):
        for p in sorted(glob.glob(os.path.join(SAMPLE, pat))):
            st = thumbstat.measure(p, pad=False)   # 우리 그림에는 유튜브 여백이 없다(2026-09-25)
            if st: rows.append({**st, 'file': os.path.basename(p), 'short': isshort})
    return rows

def thumb_defaults():
    """thumb.py가 design.json 없이 쓰는 기본값 — 새 손잡이의 출발점"""
    sys.path.insert(0, HERE)
    try:
        import thumb
        return {k: thumb.cfg(k) for k in ('long', 'short')}
    except Exception:
        return {}

THUMB_DEFAULT = {}

# ── 세 칸(위·가운데·아래)은 손잡이 하나를 나눠 쓴다 ────────────────────────────────
# 한 칸씩 "우리-경쟁" 만큼 밀면 서로 반대로 밀어 영원히 흔들린다. 2026-09-23 실측(쇼츠, 배경 3종 중앙값):
#   text_spread  0.0    top 0.2264  mid 0.4856  bot 0.2149
#                0.3    top 0.2264  mid 0.4903  bot 0.2149
#                0.45   top 0.3079  mid 0.3792  bot 0.1711
#                0.6304 top 0.3441  mid 0.2375  bot 0.2831   ← 지금 값
#                1.0    top 0.3804  mid 0.2375  bot 0.2318
#   경쟁 상위     top 0.2748  mid 0.4241  bot 0.3093
# 위·가운데는 낮은 쪽을, 아래는 높은 쪽을 원한다 — 한 손잡이로 셋을 동시에 맞출 수 없다.
# 그래서 밀지 않고 "재서 고른다": 격자마다 실제로 그려 재고, 세 칸 상대오차 합이 가장 작은 값을 쓴다.
# (text_mid 가 5회차 넘게 "듣지 않는 손잡이"로 막혀 있던 진짜 이유 — 쇼츠에서 text_y 를 보고 있었다.
#  실측하면 text_y 는 text_mid 를 0.2375~0.3674 안에서만 흔들어 목표 0.4241 에 닿지 못한다.)
BAND_KEYS = ('text_top', 'text_mid', 'text_bot')
BAND_KNOB = {'long': 'text_y', 'short': 'text_spread'}
# 롱폼 격자에 0.38·0.41 을 2026-09-25 123회차에 넣었다. 성긴 격자가 0.35 다음에 0.50 으로 뛰어서
# 그 사이가 한 번도 안 재졌는데, 반쪼개기는 이미 최선이던 0.35~0.3688 주변만 파고들어 거기까지 못 갔다.
# 실제로 그려 재 보니(text_scale 0.775 · bot_scrim 0.5 · sub_scale 0.9 고정, 배경 3종 중앙값):
#   v=0.38 err 0.5132 top 0.1655 mid 0.0796 · 0.39 1.1181/0.1524/0.1349 · 0.40 1.1181/0.1376/0.1497
#   v=0.41 0.6876/0.1248/0.1203 · 0.42 1.7239/0.1083/0.1761
# 0.38 이 지금 자리(0.3688, err 0.5297)보다 낫다 — 건너뛴 구간에 더 나은 점이 있었다.
# 0.41 은 text_top 이 목표 0.1309 를 지나가는 자리라 남겨 둔다(아래 BAND_CAPPED 근거를 다시 재게).
BAND_GRID = {'long':  [0.20, 0.35, 0.38, 0.41, 0.50, 0.62, 0.72, 0.80],
             'short': [0.0, 0.15, 0.30, 0.45, 0.60, 0.80, 1.0]}
# 손잡이 하나로는 세 칸을 못 맞춘다(2026-09-24 실측): 쇼츠 두 줄 판형은 text_spread 를 한계 1.0 까지 올려도
# text_bot 0.203 에서 멈췄다(경쟁 0.3093). 칸이 둘뿐인데 목표는 셋이라 구조적으로 못 닿는 것이었다.
# 그래서 아랫줄을 띄어쓰기에서 둘로 나눠 세 칸을 채우고(thumb.lines=3), 나뉘어 짧아진 두 줄을
# 폭 여유만큼 키우는 split_scale 을 두 번째 손잡이로 뒀다. 실측(lines=3): 1.0 → bot 0.1091,
# 1.3 → 0.1565, 1.6 → 0.2144, 2.0 → 0.3035(세 칸 오차 합 0.8496 → 0.4092; 두 줄 판형 최선은 0.7165).
# 롱폼 두 번째 손잡이는 재 보고 물렀다 — 84회차에 text_spread 격자 7점을 실제로 그려 측정했다.
# 얼어 있던 자리: text_y 를 어디에 둬도 err 0.3856 에서 안 내려갔고, 세 칸 중 top(0.6999/목표 0.9241)만
# 22% 비고 bot(0.7158/목표 0.7345)은 이미 맞아 있었다. 두 줄을 벌리면 top 이 찰 거라 보고 손잡이를 달았다.
# 실측은 그 예상을 부쉈다. 벌리면 top 은 오르지만(0.6999 → 0.7876, v=0.3) mid 가 그보다 빨리 빈다
# (0.8356 → 0.6096). 롱폼 mid 목표는 0.9469 로 세 칸 중 제일 높아, mid 를 깎는 어떤 배치도 손해다.
#   v=0.0 err 0.3856 · 0.15 0.5736 · 0.3 0.5323 · 0.45 0.5403 · 0.6 0.4866 · 0.8 0.7053 · 1.0 0.6059
# 그래서 되돌린다. 다시 달지 않는다 — 글자를 어디에 놓아도 못 닫는 차이다.
#
# 남는 사실: 경쟁 롱폼은 세 칸이 전부 0.73~0.95 로 꽉 차 있다. text_map 은 글자만이 아니라 화면의
# 결(에지)을 재므로, 저 숫자는 '글자 배치'가 아니라 '배경에 사진이 깔려 있다'는 뜻이다. 우리 롱폼은
# 0.70~0.84 다. 롱폼 판형 거리 0.3856 은 글자 손잡이로는 안 닫히고 배경 자료 화면으로만 닫힌다.
# 다음에 이 항목을 잡는 회차는 손잡이를 더 달지 말고 롱폼 배경부터 본다.
# 롱폼 두 번째 손잡이를 2026-09-25에 다시 달았다(text_scale). 위 "재 보고 물렀다"는 옛 글자 지도로
# 잰 목표(top 0.9241 · mid 0.9469)에서 나온 판단이라 근거가 없어졌다 — 새 자로 다시 잰 경쟁 롱폼은
# top 0.1309 · mid 0.0784 · bot 0.0 이고, 우리는 top 0.081 · mid 0.5784 · bot 0.0729 다.
# 차이의 정체는 '어디에 두나'가 아니라 '얼마나 크게 쓰나'였다 — 우리 글자 잉크 0.2441 vs 경쟁 0.0769(3.2배).
# 실측(2026-09-25, 같은 배경·같은 문구, text_scale 1.0/0.85/0.75/0.66/0.55/0.45):
#   text_mid 0.5784/0.4588/0.3586/0.3172/0.2620/0.2027   ← 줄이면 실제로 줄어든다
#   text_top 0.0810/0.0542/0.0658/0.0931/0.1065/0.1146   ← 목표 0.1309 쪽으로 같이 붙는다
#   text_bot 0.0729/0.0821/0.1125/0.1259/0.1392/0.1464 · white 0.0851→0.0275
BAND_KNOB2 = {'short': ('split_scale', [1.0, 1.3, 1.6, 2.0, 2.4, 2.8]),
              'long':  ('text_scale',  [0.55, 0.66, 0.75, 0.85, 1.0])}
# 쇼츠 세 번째 손잡이 text_y. 2026-09-24에 "쇼츠에서 text_y 는 안 듣는다"고 떼어 낸 자리다(위 주석).
# 그 판정은 옛 글자 지도로 잰 목표(mid 0.4241)에서 나왔고, 새 자는 목표가 정반대다(mid 0.0788 · bot 0.0338).
# 2026-09-25 113회차에 다시 재 봤다(lines=3 · spread 0.3 · split 1.6 고정, 배경 3종 중앙값):
#   text_y 0.20 err 1.1971 · 0.35 1.2487 · 0.41 1.2165 · 0.44 1.2165 · 0.46 1.0153 · 0.48 0.3690 · 0.50 0.9878
#   0.48 에서 top 0.1300(목표 0.1186) · mid 0.0884(0.0788) · bot 0.0413(0.0338) — 세 칸이 전부 0.01 안에 든다.
# 듣지 않는 손잡이가 아니었다. 다만 **최저점이 뾰족하다**: 0.46 과 0.50 은 1.0 근처인데 그 사이 0.48 만 0.37 이다.
# 이유는 아랫줄 윗변이 가운데/아래 칸 경계(1280px)를 넘느냐 마느냐로 갈리기 때문이다 — 3px 움직이면 한 줄이
# 통째로 다른 칸으로 센다. 그래서 격자를 0.02 간격으로 촘촘히 두고, 아래 grid_pick 에 반쪼개기(refine)를 넣었다.
# 성긴 격자로는 이 골짜기를 그냥 건너뛴다(24칸 훑기에서 0.50 이 최선으로 보였던 이유).
#
# 같은 이유로 lines=2 로 되돌리는 길은 닫혔다. lines=3 은 옛 자(bot 목표 0.3093)에서 나온 값이라
# 새 자에서는 근거가 없어졌다고 보고 113회차에 24칸(lines 2·3 × text_y 4 × spread 3)을 전부 그려 재 봤다.
# lines=2 는 12칸 최선이 1.4697 로 lines=3 최선(0.9878)보다 나빴다 — 두 줄이면 아래 칸이 늘 0.0000 이고
# (줄이 둘뿐이라 아래 칸에 들어갈 줄이 없다) 가운데 칸도 0 아니면 0.17 로 튄다. 되돌리지 않는다.
BAND_KNOB3 = {'short': ('text_y', [0.20, 0.35, 0.44, 0.46, 0.48, 0.50, 0.62, 0.72]),
              # 롱폼 세 번째 손잡이 bot_scrim(아래 칸을 눌러 평평하게, thumb.py). 2026-09-25 116회차.
              # 롱폼 세 칸 오차가 3.2773 에 얼어 있었고 그 75%(0.1719/0.2286)가 아래 칸 하나였다.
              # 글자 손잡이로는 못 닫는다 — text_y 6점 x text_scale 3점 18장을 전부 그려 쟀고 아래 칸
              # 최저가 0.0845 였다. 글자만 빼고 같은 설정으로 그리면 아래 칸이 0.0000 이라, 아래 칸 잉크는
              # 글자(거기 있을 때) 아니면 배경(글자 뒤 띠가 위로 비켜났을 때)이다. 경쟁은 정확히 0.0 이다.
              # 실측(scrim x text_y x text_scale 24장): 0.38/0.35/0.55 에서 오차 2.0042 · bot 0.0100.
              'long':  ('bot_scrim', [0.0, 0.2, 0.3, 0.38, 0.45])}
# 롱폼 네 번째 손잡이 sub_scale(아랫줄만 작게, thumb.py). 2026-09-25 121회차.
# 닫으려는 것: long.text_mid 하나다. 120회차 최선(text_y 0.3875 · text_scale 0.775 · bot_scrim 0.475)에서
# 세 칸은 top 0.1558(목표 0.1309) · mid 0.1389(0.0784) · bot 0.0(0.0) 이고, 판형 오차 1.2245 의
# **71%가 mid 한 칸**(0.0605/0.0854)이다. 나머지 두 칸은 이미 맞아 있다.
# 왜 지금 손잡이로는 안 닫히나 — 격자표(120회차 bands.long)가 그대로 보여 준다.
#   text_y 0.20 → top 0.3890 · mid 0.0275   (두 줄이 다 위 칸에 들어가 mid 는 비지만 top 이 3배로 넘친다)
#   text_y 0.3875 → top 0.1558 · mid 0.1389 (top 은 맞는데 아랫줄이 통째로 가운데 칸에 있다)
# 두 줄이 같은 크기라서 top 과 mid 를 따로 못 만진다 — 한 손잡이가 두 칸을 나눠 쥐고 있다.
# 글자 크기(text_scale)를 더 줄이는 길은 막혀 있다: 하한 0.55 는 화면 검증에서 나온 값이고
# (0.45 는 두 줄이 히트맵 글자에 묻혀 안 읽힌다) 어차피 두 줄을 같이 줄이면 top 도 같이 무너진다.
# 그래서 **아랫줄만** 줄인다. 윗줄 위치·크기가 그대로라 top 은 건드리지 않고 mid 만 내려간다
# (thumb.py 에서 ys[1] = cy 는 lhs[0] 로만 정해지므로 아랫줄 크기가 줄어도 윗줄은 1px도 안 움직인다).
# 판형으로도 지어낸 것이 아니다 — 큰 제목 + 작은 부제는 경쟁 롱폼이 쓰는 배치다.
# 읽힘은 thumb.py 가 지킨다: 아랫줄도 자연 크기의 0.55(화면 검증으로 정한 바닥) 밑으로는 안 내려간다.
BAND_KNOB4 = {'long': ('sub_scale', [0.7, 0.8, 0.9, 1.0])}
# sub_scale 을 JOINT(두 손잡이 같이 훑기)에 text_y 와 함께 넣으려다 실측으로 물렀다(2026-09-26 127회차).
# 생각: text_y 는 top 을 만지고 sub_scale 은 mid 만 만지니(윗줄이 1px도 안 움직인다) 둘을 같이 훑으면
# 'top 을 맞추는 자리(0.41)로 옮기고 그때 비는 mid 를 아랫줄 크기로 메운다'가 될 것이라 봤다.
# 30점(text_y 0.38·0.395·0.41·0.425·0.44 x sub_scale 0.7·0.75·0.8·0.85·0.9·1.0)을 전부 그려 쟀다:
#   text_y 0.38 → mid 0.1039/0.1160/0.1276/0.1418/0.0796/0.1281   (sub_scale 0.7→1.0 순서)
#   text_y 0.41 → mid 0.1446/0.1567/0.1706/0.1825/0.1203/0.1688
# 틀렸다. **아랫줄을 줄이면 mid 는 오히려 커진다** — 0.7 이 0.85 보다 작긴 하지만 0.9 보다 크다.
# 0.9 만 혼자 0.0796 으로 떨어지는 계단이고, 그 앞뒤는 전부 0.10~0.18 이다. 아랫줄 윗변이 가운데 칸
# 경계를 넘느냐로 갈리는 한 점짜리 골짜기라서, '연속으로 mid 를 줄이는 손잡이'가 아니다.
# 30점 최선은 지금 자리(0.38 · 0.9, 오차 0.6187)였고 2위가 0.41 · 0.9(0.7599)다 — top 을 맞추러 가면
# mid 가 0.0467 비어 전체가 나빠진다. BAND_CAPPED 의 long.text_top 판정이 이 30점으로도 그대로 섰다.
# JOINT 에 넣지 않는다. 다시 넣으려면 이 30점부터 다시 재라.
# 격자 끝점에 최선이 붙으면 "유지(가장 작다)"는 수렴이 아니라 격자가 짧다는 뜻이다.
# split_scale 은 72회차까지 늘 끝점 2.0 이 최선이었고(오차 1.0121→0.728→0.5784→0.2653, 계속 내려감)
# 그릴 때 thumb.py 가 2.0 으로 깎고 있어 판형 오차가 0.2653 에 얼어 있었다(2026-09-24).
# 그래서 (1) thumb.py 한계를 3.2 로 넓히고 (2) 끝점에 붙으면 아래 한계까지 격자를 저절로 늘린다.
# text_spread 도 같은 모양으로 92회차에 끝점 1.0 에 붙어 막혔다(쇼츠 오차 0.1912).
# 그릴 때 실제로 움직이는 구간을 재 보니 1.4 까지였다(thumb.py 주석에 숫자) — 한계를 1.4 로 넓힌다.
# 넓힌 뒤 94회차 실측: 1.0 err 0.1912 · 1.2 0.3412 · 1.4 0.4096 → 오차는 안 줄었고 1.0 이 진짜 최선이다.
# 얻은 것은 오차가 아니라 판정이다 — 이 자리는 '아직 못 푼 막힘'이 아니라 '재서 고른 값'이 됐다.
KNOB_LIMIT = {'text_spread': (0.0, 1.4),      # thumb.py 가 0~1.4 로 깎는다
              'text_y':      (0.15, 0.80),    # thumb.py 가 0.15~0.80 으로 깎는다
              'split_scale': (1.0, 3.2),      # thumb.py 윗한계와 같게 유지한다
              # 하한 0.55 는 화면 검증에서 나왔다(2026-09-25). 같은 배경·같은 문구로 1.0/0.66/0.55/0.45 를
              # 그려 480px(실제 피드 크기)로 견줬다. 0.45 는 두 줄이 히트맵 글자에 묻혀 안 읽힌다.
              # 숫자로는 0.45 가 더 낫지만(오차 4.11 vs 4.98) 거기까지 내려가지 않는다.
              'text_scale':  (0.55, 1.0),
              'bot_scrim':   (0.0, 0.5),    # thumb.py 가 0~0.5 로 깎는다
              # 하한 0.7 은 읽힘 바닥에서 거꾸로 계산한 값이다. thumb.py 는 아랫줄을 자연 크기의 0.55
              # 밑으로 안 내린다(화면 검증). 지금 text_scale 0.775 에서 0.775 x 0.7 = 0.54 이므로
              # 0.7 아래는 그려도 같은 그림이 나온다 — 격자를 그 죽은 구간에 들여보내지 않는다.
              'sub_scale':   (0.7, 1.0)}

def band_err(rows, kind, spec):
    """세 칸 상대오차 합. 작을수록 경쟁 판형에 가깝다"""
    tgt = spec.get(kind) or {}
    mine = [r for r in rows if (r['short'] if kind == 'short' else not r['short'])]
    if not mine or not tgt: return None, {}
    got = {k: statistics.median(r[k] for r in mine) for k in BAND_KEYS if k in tgt}
    if not got: return None, {}
    # 칸마다 그 칸의 목표로 나누던 것을 2026-09-25에 고쳤다. 롱폼 text_bot 목표는 실측 0.0 인데
    # max(0, 1e-3) 이 분모가 되면서 그 한 칸이 오차의 91.5%를 차지했다(우리 0.0729 / 0.001 = 72.9,
    # 전체 79.66). 나머지 두 칸은 합쳐서 6.76 이라, 격자는 사실상 text_bot 하나만 줄이고 있었다.
    # 게다가 text_bot 은 want=0 이라 gaps 목록(아래 `if want and ...`)에서 통째로 빠진다 —
    # 보고서에는 안 보이는데 목적함수는 그것만 보고 있었다. long.text_mid 가 82회차부터 안 닫힌 이유다.
    # 이제 세 칸을 같은 자로 나눈다(그 판형 목표 세 칸의 평균). 목표가 0인 칸도 제 몫만큼만 센다.
    base = max(sum(tgt[k] for k in got) / len(got), 1e-3)
    return sum(abs(got[k] - tgt[k]) for k in got) / base, got

def ctx_tag(design, kind, knob):
    """그 판형에서 '지금 움직이려는 손잡이 말고 나머지'가 어디에 있는지를 짧은 지문으로 만든다.
    같은 지문에서 잰 값끼리만 견줄 수 있다 — 다른 손잡이가 움직인 뒤의 값과 섞으면 손잡이가 듣는지 안 듣는지,
    목표를 지나쳤는지 아닌지를 알 수 없다."""
    import hashlib
    d = design.get(kind, {})
    body = ';'.join(f'{k}={round(float(v), 4) if isinstance(v, (int, float)) else v}'
                    for k, v in sorted(d.items()) if k != knob)
    return hashlib.md5(body.encode('utf-8')).hexdigest()[:6]


def grid_pick(design, spec, kind, knob, base_grid, did, blocked):
    """손잡이 하나를 격자로 실제로 그려 재고 가장 나은 값을 고른다. 미는 게 아니라 재는 것이라 흔들리지 않는다"""
    d = design.setdefault(kind, {})
    cur = d.get(knob)
    if cur is None:
        cur = float(THUMB_DEFAULT.get(kind, {}).get(knob, 0.0))
    grid = sorted(set(base_grid + [round(float(cur), 4)]))
    table, failed = [], []
    # 격자를 훑는 동안 design.json 에는 '지금 재보는 값'이 들어 있다. 회차가 그 사이에 죽으면(타임아웃·재부팅)
    # 고른 값이 아니라 우연히 마지막으로 재던 격자 점이 그대로 남아, 다음 회차까지 production 썸네일이
    # 그 값으로 그려진다. 2026-09-25 125회차에 실제로 겪었다 — 앞 회차를 300초에서 끊었더니 long.text_y 가
    # 고른 값 0.3688 이 아니라 격자 점 0.72 에 남아 있었고(세 칸 오차 0.5297 → 2.5731), 커밋된 값과 달라진
    # 것을 git diff 로 찾기 전까지 아무도 몰랐다. 그래서 '되돌릴 자리'를 파일에 같이 적어 둔다(main 이 치운다).
    design['_probe'] = {'kind': kind, 'knob': knob, 'safe': cur}

    def measure(vals):
        """격자 점들을 실제로 그려 재서 table 에 넣는다. 못 재면 failed 에 표시한다"""
        for v in vals:
            if any(abs(t['v'] - v) < 1e-9 for t in table): continue
            d[knob] = v
            json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            render_samples(keep_chart=True)
            err, got = band_err(measure_ours(), kind, spec)
            if err is None: failed.append(v); return
            table.append({'v': v, 'err': round(err, 4), **{k: round(x, 4) for k, x in got.items()}})
        table.sort(key=lambda t: t['v'])

    measure(grid)
    if failed or not table:
        blocked.append(f'{kind} 세 칸 맞추기 — 샘플이나 경쟁 기준이 없어 못 쟀다')
        d[knob] = cur; design.pop('_probe', None)
        json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return
    def pick():
        # 비긴 값끼리는 지금 값을 이긴 것으로 치지 않는다. 격자 전체가 같은 값으로 나오는 경우(손잡이가
        # 안 듣거나 측정이 섞인 경우)에 min() 은 늘 격자의 맨 아래값을 골라 손잡이를 끝으로 밀어 버린다.
        #
        # 다만 그 '지금 값 지키기'가 한쪽으로만 걸려서, 한때 듣던 손잡이가 안 듣게 된 뒤에도 그 자리에
        # 얼어붙는다. 2026-09-25 119회차 실측 — long.bot_scrim 이 그랬다. 116회차에 scrim x text_y x
        # text_scale 을 같이 훑어 0.38/0.35/0.55 를 골랐는데, 그 뒤 text_y 0.3875 · text_scale 0.775 로
        # 옮겨 가면서 scrim 이 세 칸에 아무 영향을 못 주게 됐다. 지금 값으로 실제로 그려 재 보면:
        #     bot_scrim 0.00 → text_top 0.1028 · text_mid 0.1391 · text_bot 0.0000
        #     bot_scrim 0.38 → text_top 0.1028 · text_mid 0.1391 · text_bot 0.0000   (세 칸 전부 같다)
        #     대신 bright 0.4935 → 0.4286 (-0.0649) · contrast 0.2852 → 0.2573 (-0.0279)
        # 세 칸에는 0을 벌면서 밝기·대비에서는 값을 치르고 있었고, 그게 long.bright·long.dark 가 '미해결
        # 차이'로 다시 잡힌 이유다. 격자가 통째로 평평하면 그 손잡이는 지금 자리에서 안 듣는 것이므로,
        # 지금 값을 지키지 말고 기본값(아무것도 안 하는 자리)으로 되돌린다 — 벌지 못하는 손잡이가 다른
        # 곳에서 값을 치르게 두지 않는다. 다시 듣기 시작하면 격자가 평평하지 않을 테니 저절로 풀린다.
        best = min(table, key=lambda t: t['err'])
        spread = max(t['err'] for t in table) - min(t['err'] for t in table)
        if len(table) > 1 and spread <= 1e-4:
            neutral = float(THUMB_DEFAULT.get(kind, {}).get(knob, table[0]['v']))
            flat = min(table, key=lambda t: abs(t['v'] - neutral))
            if abs(flat['v'] - cur) > 1e-9:
                did.append(f'{kind}.{knob} 격자가 통째로 평평하다(세 칸 오차 폭 {spread:.4f}) — '
                           f'지금 자리에서 안 듣는 손잡이라 {cur} → {flat["v"]}(기본값)으로 되돌린다')
            return flat
        here = next((t for t in table if abs(t['v'] - cur) < 1e-9), None)
        if here is not None and here['err'] <= best['err'] + 1e-4: return here
        return best

    # 끝점에 최선이 붙어 있으면 수렴이 아니다 — 한계까지 격자를 늘려 실제로 넘어가 본다.
    lo_lim, hi_lim = KNOB_LIMIT.get(knob, (None, None))
    for _ in range(3):
        best, vs = pick(), [t['v'] for t in table]
        step = max((round(b - a, 4) for a, b in zip(vs, vs[1:])), default=0) or 0.1
        if abs(best['v'] - vs[-1]) < 1e-9 and hi_lim is not None and vs[-1] < hi_lim - 1e-9:
            nxt = [round(min(vs[-1] + step * i, hi_lim), 4) for i in (1, 2)]
        elif abs(best['v'] - vs[0]) < 1e-9 and lo_lim is not None and vs[0] > lo_lim + 1e-9:
            nxt = [round(max(vs[0] - step * i, lo_lim), 4) for i in (1, 2)]
        else:
            break                                   # 안쪽에서 최선이 나왔다 = 진짜 수렴
        measure(sorted(set(nxt)))
        if failed: break
        did.append(f'{kind}.{knob} 격자 끝점({best["v"]})에 최선이 붙어 한계 {hi_lim if nxt[0] > best["v"] else lo_lim} 쪽으로 {nxt} 를 더 재 봤다')
    # 안쪽에서 최선이 나왔어도 '수렴'이 아니다 — 격자 사이에 더 깊은 골짜기가 있을 수 있다.
    # 2026-09-25 113회차: 쇼츠 text_y 를 0.02 간격으로 재니 0.46 err 1.0153 · 0.48 0.3690 · 0.50 0.9878 이었다.
    # 성긴 격자(0.44/0.50/0.62)로는 0.50 을 최선으로 골라 그 골짜기를 통째로 지나쳤다. 세 칸 오차는 줄의 윗변이
    # 칸 경계(쇼츠 1280px)를 넘느냐로 갈려서, 손잡이가 몇 px만 움직여도 한 줄이 다른 칸으로 통째로 센다.
    # 그래서 최선 양옆을 반으로 갈라 들어간다. 한 바퀴에 두 점(왼쪽·오른쪽 중간)만 재고,
    # 그 바퀴에서 최선이 안 바뀌면 멈춘다 — 손잡이 하나당 최대 4장만 더 그린다(회차 시간을 지키려고).
    for _ in range(2):
        best, vs = pick(), sorted(t['v'] for t in table)
        i = vs.index(best['v'])
        mids = []
        for j in (i - 1, i + 1):
            if 0 <= j < len(vs):
                m = round((best['v'] + vs[j]) / 2, 4)
                if m != best['v'] and not any(abs(t['v'] - m) < 1e-9 for t in table): mids.append(m)
        if not mids: break
        measure(sorted(set(mids)))
        if failed: break
        if pick()['v'] == best['v']: break      # 갈라도 최선이 그대로다 = 이 자리가 진짜 골짜기 바닥
        did.append(f'{kind}.{knob} 격자 사이를 갈라 더 나은 자리를 찾았다: {best["v"]}(오차 {best["err"]}) → {pick()["v"]}({pick()["err"]})')
    best = pick()
    vs = [t['v'] for t in table]
    if abs(best['v'] - vs[-1]) < 1e-9 and hi_lim is not None and abs(vs[-1] - hi_lim) < 1e-9:
        # 한계까지 갔는데도 끝점이 최선이다. 예전에는 여기서 무조건 "손잡이를 더 넓혀야 줄어든다"고 적었다.
        # 그 말이 맞으려면 '남은 오차를 만드는 칸'을 이 손잡이가 한계 근처에서 아직 움직이고 있어야 한다.
        # 2026-09-25 125회차 실측 — long.bot_scrim 이 그 말이 틀린 경우였다. thumb.py 한계를 0.5 → 0.8 로
        # 열고 실제로 그려 쟀다(text_y 0.3688 · text_scale 0.775 · sub_scale 0.9 고정, 배경 3종 중앙값):
        #     0.50 → 세 칸 오차 0.5297 (top 0.1673 · mid 0.0778 · bot 0.0000)
        #     0.55 → 0.5297   0.60 → 0.5297   0.70 → 0.5297   0.80 → 0.5297   (세 칸이 1픽셀도 안 움직인다)
        #     대신 bright 0.3881 → 0.3644 (목표 0.4797 에서 더 멀어진다) · contrast 0.2597 → 0.2521 (역시 멀어진다)
        # 아래 칸은 0.5 에서 이미 목표(0.0)에 정확히 닿아 있어 더 눌러도 벌 것이 없고, 남은 오차는 전부
        # text_top(0.0364, 잔차의 98%) 이다. 그 칸은 BAND_CAPPED 에 "text_y 로만 움직이고 그 대가로 mid 가
        # 빈다"고 실측으로 세워 둔 자리다. 그래서 넓히면 밝기·대비만 내주고 세 칸은 그대로다.
        # 그래서 thumb.py 한계는 0.5 로 되돌렸다. 넓혀 봐야 소용없는 자리를 회차마다 '막힘'으로 띄우면
        # 다음 회차가 그걸 닫으려고 같은 일을 또 한다(이번 회차가 실제로 그렇게 시작했다).
        # 판정 기준: 남은 오차의 10% 이상을 차지하는 칸이 격자 윗구간에서 이미 평평(<0.002)하면,
        # 이 손잡이는 한계에서 '멈춘' 것이 아니라 '다 쓴' 것이다 — 막힘이 아니라 기록으로 남긴다.
        #
        # 그 판정에 **절대 바닥**을 같이 둔다(2026-09-26 127회차에 실측으로 알았다). 위 10% 는 비율만 보므로
        # 판형이 좋아져 잔차 자체가 작아지면 아무것도 아닌 칸이 그 문턱을 넘는다. 127회차 롱폼이 그랬다:
        #   잔차 top 0.0359 · mid 0.0060 · bot 0.0000 (합 0.0419) → mid 가 14.3% 로 10% 를 넘었고,
        #   bot_scrim 격자 윗구간(0.45·0.475·0.5)에서 mid 가 0.0841→0.0796 으로 0.0045 움직이니 '아직 산다'.
        # 그래서 125회차에 '넓혀도 소용없다'고 실측으로 닫아 둔 자리가 다시 '막힘'으로 떴고, 127회차가
        # 실제로 그걸 닫으려고 시작했다 — 이 주석이 막으려던 일이 그대로 일어났다.
        # 2026-09-26 재실측(thumb.py 한계를 0.7 로 임시로 열고 text_y 0.38 · text_scale 0.775 · sub_scale 0.9):
        #   0.50 err 0.6187 (top 0.1655 mid 0.0796 bot 0.0)   0.525 0.6187   0.55 0.6187
        #   0.60 0.6187   0.65 0.6187   0.70 0.6187            ← 세 칸이 소수 넷째 자리까지 똑같다
        #   대신 bright 0.3888 → 0.3717 (목표 0.4851 에서 멀어진다) · contrast 0.2606 → 0.2550 (역시 멀어진다)
        # 한계 아래에서 움직이던 기울기는 한계 위에 남은 것이 있다는 뜻이 아니었다. 아래 칸이 0.5 에서
        # 목표 0.0 에 정확히 닿으면서 띠가 가운데 칸에 더는 안 걸치기 때문이다. thumb.py 한계는 0.5 로 되돌렸다.
        # 바닥 0.01 의 근거: 세 칸 목표 평균(base)이 롱폼 0.0677 · 쇼츠 0.0771 이라 0.01 은 오차 0.15 어치다.
        # 그만큼 벌려고 밝기·대비(미해결 차이가 0.13 인 항목)를 내주는 것은 손해다.
        LIVE_FLOOR = 0.01
        tgt_l = spec.get(kind) or {}
        resid = {k: abs(best[k] - tgt_l[k]) for k in BAND_KEYS if k in best and k in tgt_l}
        tot = sum(resid.values())
        topband = sorted(table, key=lambda t: t['v'])[-3:]    # 격자 맨 위 세 점
        live = [k for k, r in resid.items()
                if tot > 0 and r / tot >= 0.10 and r >= LIVE_FLOOR
                and max(t[k] for t in topband) - min(t[k] for t in topband) >= 0.002]
        if live:
            blocked.append(f'{kind}.{knob} 가 그리기 한계 {hi_lim} 에서 멈췄다 — 오차 {best["err"]} 는 '
                           f'손잡이를 더 넓혀야 줄어든다(아직 움직이는 칸: {", ".join(sorted(live))})')
        else:
            did.append(f'{kind}.{knob} 가 한계 {hi_lim} 에 있지만 넓혀도 소용없다 — 남은 오차 {best["err"]} 는 '
                       + ', '.join(f'{k} {r:.4f}' for k, r in sorted(resid.items(), key=lambda kv: -kv[1]) if r > 0)
                       + ' 에서 오고, 그 칸들은 격자 윗구간에서 이미 평평하다')
    d[knob] = best['v']
    design.pop('_probe', None)        # 고른 값을 적는 순간 되돌릴 이유가 없어진다
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if best['v'] != cur:
        was = next((t for t in table if t['v'] == cur), None)
        did.append(f"{kind}.{knob} {cur} → {best['v']} (세 칸 오차 합 {was['err'] if was else '?'} → {best['err']}, 격자 {len(table)}점 실측)")
    else:
        did.append(f"{kind}.{knob} {cur} 유지 (격자 {len(table)}점 중 오차 합 {best['err']} 이 가장 작다)")
    return table


# 두 손잡이를 같이 움직여야만 보이는 자리. 좌표 하강은 이런 자리를 구조적으로 못 찾는다 —
# 손잡이를 하나씩 고르는데, 각자 혼자서는 이득이 없기 때문이다.
# 2026-09-25 118회차 실측이 그 장면이다. bot_scrim 을 새로 달고 두 바퀴를 돌렸는데 3.2773 → 3.2047 로
# 0.07 밖에 안 줄었다. 이유: 첫 바퀴에 scrim 을 고를 때 글자가 아직 아래(text_y 0.72)에 있어서, 아래 칸 잉크가
# 배경이 아니라 글자다. 글자는 scrim 위에 그리므로 scrim 을 아무리 올려도 그 자리에서는 이득이 0 이다
# (격자 전 구간 3.26~3.31 로 평평했고 0.1 이 뽑혔다). 그래서 다음 바퀴의 text_y 도 0.67 에 머문다.
# 둘을 같이 움직이면 보인다(24장 전수 실측, text_scale 0.55):
#   scrim 0.00 · text_y 0.72 → 3.4919      scrim 0.38 · text_y 0.72 → 3.2631   (글자를 안 옮기면 이득 없음)
#   scrim 0.00 · text_y 0.35 → 4.1839      scrim 0.38 · text_y 0.35 → 2.0042   (같이 옮기면 -2.18)
# 그래서 롱폼은 좌표 하강 앞에 거친 2차원 훑기를 한 번 둔다. 8점만 본다(회차 시간).
JOINT = {'long': ('text_y', [0.25, 0.35, 0.50, 0.72], 'bot_scrim', [0.0, 0.38])}


def joint_seed(design, spec, kind, did, blocked):
    """두 손잡이를 곱으로 훑어 출발점을 잡는다. 여기서 고른 값 위에서 좌표 하강이 다듬는다"""
    if kind not in JOINT: return
    ka, ga, kb, gb = JOINT[kind]
    d = design.setdefault(kind, {})
    cur = (d.get(ka), d.get(kb))
    best = None
    for va in ga:
        for vb in gb:
            d[ka], d[kb] = va, vb
            json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            render_samples(keep_chart=True)
            err, got = band_err(measure_ours(), kind, spec)
            if err is None:
                blocked.append(f'{kind} 두 손잡이 같이 훑기 — 못 쟀다')
                d[ka], d[kb] = cur; json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
                return
            if best is None or err < best[0] - 1e-4: best = (err, va, vb, got)
    here = None
    if cur[0] is not None and cur[1] is not None:
        d[ka], d[kb] = cur
        json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        render_samples(keep_chart=True)
        here, _ = band_err(measure_ours(), kind, spec)
    if best and (here is None or best[0] < here - 1e-4):
        d[ka], d[kb] = best[1], best[2]
        did.append(f"{kind} 두 손잡이 같이 훑기({len(ga) * len(gb)}점): {ka} {cur[0]}→{best[1]} · {kb} {cur[1]}→{best[2]} "
                   f"(세 칸 오차 합 {round(here, 4) if here else '?'} → {round(best[0], 4)}, "
                   f"{ {k: round(v, 4) for k, v in best[3].items()} })")
    else:
        did.append(f'{kind} 두 손잡이 같이 훑기 — 지금 자리({cur[0]}·{cur[1]}, 오차 {round(here, 4) if here else "?"})가 여전히 최선이다')
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def tune_bands(design, spec, kind, did, blocked):
    """세 칸 맞추기. 손잡이를 하나씩 차례로 골라 내려간다(좌표 하강) — 곱으로 다 돌면 너무 오래 걸린다.

    격자표는 손잡이마다 따로 남긴다. 예전에는 두 번째 손잡이 표가 첫 번째 것을 통째로 덮어써서
    loop_log 의 bands 에 split_scale 표만 남고 text_spread 표는 한 번도 안 남았다 —
    92회차가 'text_spread 가 그리기 한계 1.0 에서 멈췄다'고 알렸는데 다음 회차가 로그만 보고는
    그 격자가 실제로 무슨 값을 냈는지 따질 수 없던 이유다(2026-09-25).
    """
    out = {}
    plan = [(BAND_KNOB[kind], BAND_GRID[kind])]
    for tbl in (BAND_KNOB2, BAND_KNOB3, BAND_KNOB4):
        if kind in tbl: plan.append(tbl[kind])
    # 한 바퀴만 돌면 '나중에 단 손잡이'가 굶는다. 좌표 하강은 앞 손잡이를 뒤 손잡이가 없는 세상에서 고르기
    # 때문이다 — 2026-09-25 116회차에 bot_scrim 을 달고 실측으로 확인했다(24장 전수):
    #   한 바퀴: text_y 0.72(scrim 없을 때 최선) → scrim 0.28 → scale 0.55 → 오차 3.2631 에서 멈춘다
    #   두 바퀴: 새 scrim 자리에서 text_y 를 다시 고르면 0.35 로 옮겨 가고 오차가 2.0042 까지 내려간다
    # 그래서 두 바퀴를 돌되, 한 바퀴에서 손잡이가 하나도 안 움직이면 거기가 바닥이므로 멈춘다.
    d = design.setdefault(kind, {})
    joint_seed(design, spec, kind, did, blocked)
    for rnd in range(2):
        before = {k: d.get(k) for k, _ in plan}
        for i, (knob, grid) in enumerate(plan):
            t = grid_pick(design, spec, kind, knob, grid, did, blocked)
            if t: out[knob] = t
            elif i == 0: return out          # 첫 손잡이를 못 쟀으면 샘플·기준이 없는 것이라 더 돌지 않는다
        if all(before.get(k) == d.get(k) for k, _ in plan):
            if rnd: did.append(f'{kind} 세 칸 — 두 바퀴째에 움직인 손잡이가 없다(좌표 하강 바닥)')
            break
    return out


# 사람이 눈으로 보고 정한 한계. 숫자로는 더 갈 수 있지만 가면 썸네일이 제 일을 못 한다.
# 여기 적힌 자리에 손잡이가 붙어 막히면 그건 '아직 못 푼 숙제'가 아니라 '풀지 않기로 한 것'이다.
# 2026-09-24: 이 둘이 계기판의 '미해결 차이 수'에 계속 잡혀, 회차마다 이미 끝난 판단을 다시 뒤지게 만들었다
# (75회차가 text_tint 를 1.0 까지 올렸다가 화면 검증에서 되돌린 것이 그 결과다). 갈라 센다.
CAPPED = {
    ('short', 'white'):    ('text_tint', 0.7,
                            '2026-09-24 화면 검증 — 0.85·1.0 에서는 글자가 흰빛을 잃고 잿빛 파랑으로 죽는다'),
    ('short', 'contrast'): ('tint_v', 0.75,
                            '2026-09-24 화면 검증 — 0.6 은 숫자로는 목표에 맞는데 글자가 회색으로 죽는다'),
    # 2026-09-25 실측. 롱폼 대비는 '글자 뒤 띠'로 못 닫는다 — 차이가 배경에서 오기 때문이다.
    # 경쟁 롱폼 60장 vs 우리 long.png 를 글자 지도로 갈라 쟀다(쇼츠에서 2026-09-24에 썼던 같은 자):
    #     배경만 대비      우리 0.2573 < 경쟁 0.3222   ← 차이가 여기 있다
    #     글자자리 대비    우리 0.4343 > 경쟁 0.3408   ← 글자 쪽은 이미 우리가 더 세다
    #     아주 밝은 픽셀   우리 0.0892 vs 경쟁 0.1650(V>0.80), 아주 어두운 픽셀 0.5531 vs 0.4122
    # 경쟁 롱폼은 얼굴·사진이 프레임을 채워 배경 자체가 울퉁불퉁하다. 우리 배경은 차트·히트맵이라 평평하다.
    # 글자 쪽 손잡이를 네 개 다 실측했고 전부 목표(+0.1133)의 1/5도 못 민다:
    #     panel_alpha  150→0.2736 · 182→0.2804 · 230→0.2778   (아예 안 듣는다)
    #     panel_blur   28→0.2778 · 14→0.2857 · 4→0.2926 · 0→0.2949   (전 구간 +0.0171)
    #     panel_pad    0.3→0.2714 · 1.0→0.2778 · 3.0→0.2938  (+0.0224, 대신 bright 0.4034→0.2954 로 무너진다)
    #     stroke_ratio 6→0.2817 · 16→0.2778 · 40→0.2768   (+0.0049)
    # 넷을 다 끝까지 밀어도 0.31 언저리고 목표는 0.3911 이다. 남은 길은 배경을 사진으로 바꾸는 것뿐인데,
    # 자료 화면을 보여 준다는 지시와 정면으로 부딪힌다(쇼츠에서 같은 결론을 냈다 — '배경은 건드릴 것이 아니다').
    # 그래서 '아직 못 푼 숙제'가 아니라 '풀지 않기로 한 것'이다. panel_pad·panel_blur 손잡이는 thumb.py 에
    # 달아 뒀다(기본값은 옛 하드코딩값 그대로라 그림은 안 바뀐다) — 나중에 배경 방침이 바뀌면 그때 쓴다.
    # 2026-09-26: 여기 있던 ('long','contrast') 칸을 뺐다. 손잡이 자체를 RULE 에서 뗐기 때문에
    # 'RULE 주석에 이유' 쪽(long.white 와 같은 길)으로 나간다. 배경 대비(bg_contrast)를 달아 봤다가
    # 물린 기록은 RULE['contrast'] 주석에 있다 — 다시 달기 전에 그것부터 읽을 것.
}

# 세 칸 항목(BAND_KEYS)은 tune_bands 가 맡아서 위 CAPPED 를 안 거친다 — 격자가 한계까지 다 훑어도 목표에
# 못 닿는 항목은 회차마다 '미해결 차이'로 다시 잡히고, 다음 회차가 또 같은 격자를 처음부터 훑는다.
# long.text_mid 가 그랬다(82~87회차). 2026-09-25 실측으로 닫힐 수 없는 항목임을 확인했다:
#   · 경쟁 롱폼 255장의 기준값은 text 0.9433 · text_thick 1.0 — 글자 지도가 화면을 통째로 덮은 값이다.
#     경쟁 롱폼은 사진·얼굴·그래픽이 프레임을 꽉 채워서 Canny 가 어디서나 터진다. '글자를 어디 두나'가 아니라
#     '화면이 얼마나 빽빽한가'를 재고 있다.
#   · 측정을 의심해 팽창 커널을 줄여 봤다(25x9x2 → 13x5x1 → 9x3x1 → 5x3x1). 경쟁 상·하위는 더 잘 갈렸지만
#     우리와의 거리는 오히려 벌어졌다(우리 롱 mid 0.624→0.193, 상대 차이 -34% → -70%). 측정 탓이 아니다.
#   · 그리기 손잡이도 전부 훑었다. panel_alpha 212/160/110/60/0 → mid 0.450~0.490 · bot 0.363 고정,
#     bg_bright 0.5/0.9/1.29/1.6/1.8 → mid 0.270~0.453 · bot 0.363 고정.
#     쇼츠에서 통했던 3줄 나누기도 넣어 봤다(lines=3, split 1.0/1.6/2.2) → 오차합 1.4469/1.3301/1.1284 로
#     2줄(1.1829)보다 나아지지 않고 bot 이 0.363 → 0.190 으로 되레 비었다. 그래서 되돌렸다.
#   · 남는 원인은 배경이다. 우리 롱폼 배경은 차트라 아래 1/3이 비어 있고, 어떤 손잡이로도 그 칸이 안 채워진다.
#     프레임을 꽉 채우는 자료 화면을 깔아야 닿는 숫자다 — 그리기 손잡이가 아니라 '무엇을 배경에 까나'의 문제라
#     tools-wanted.md 에 사람 판단으로 올렸다. 숫자를 맞추려고 없는 자료를 지어 깔지 않는다.
BAND_CAPPED = {
    # ('long', 'text_mid') 는 2026-09-25 98회차까지 '한계 확정'이었다. 근거는 "경쟁 기준값 0.9433 은
    # 프레임을 꽉 채운 사진에서 나온 값이라 닿지 않는다" 였는데, 그 0.9433 자체가 옛 text_map 이 포화된
    # 결과였다(가장자리가 있으면 켜지는 자였다 — thumbstat.text_map 주석의 실측 참고). 재는 자를 고쳤으니
    # 근거가 없어졌다. 다시 격자로 재게 풀어 둔다. 새 자로도 못 닿으면 그때 실측을 적어 다시 세운다.
    #
    # ('long','text_top') 은 2026-09-25 123회차에 실측으로 세웠다. 그때까지 이 항목 하나가 계기판의
    # '미해결 차이 수 1' 을 잡고 있었고, 회차마다 같은 격자를 처음부터 다시 훑게 만들었다.
    # 네 손잡이 격자 30점 + 안 재진 구간 5점, 모두 35점을 놓고 보면 닫히지 않는 이유가 한 가지다:
    #   · bot_scrim 전 구간에서 top 0.1673~0.1953 — 손잡이가 top 을 거의 안 움직인다
    #   · sub_scale 전 구간에서 top 0.1673~0.1684 — 마찬가지로 안 움직인다
    #   · text_scale 전 구간에서 top >= 0.1602 — 어디를 잡아도 목표 0.1309 아래로 안 내려온다
    #   · text_y 만 top 을 목표까지 끌고 온다. 그런데 닿는 자리에서 mid 가 그보다 더 빈다:
    #       v=0.40 top 0.1376(목표와 0.0067 차) 인데 mid 0.1497(목표 0.0784 에서 0.0713 빔) → err 1.1181
    #       v=0.41 top 0.1248(0.0061 차)        인데 mid 0.1203(0.0419 빔)                  → err 0.6876
    #       v=0.38 top 0.1655(0.0346 차)        인데 mid 0.0796(0.0012 빔)                  → err 0.5132  ← 최선
    #     top 을 0.0346 줄이려면 mid 를 0.04~0.07 내줘야 한다. 한 자로 재면 언제나 손해다.
    # 위·가운데가 한 손잡이를 반대 방향으로 나눠 쓰는 구조라서 그렇다(text_y 를 내리면 글자가 위 칸으로
    # 올라가 top 이 차고 mid 가 빈다). 글자를 어디에 놓아도 셋을 동시에 맞출 수 없다 —
    # 이 판형에서 top 26% 초과는 mid·bot 을 정확히 맞춘 대가다. '아직 못 푼 숙제'가 아니라 그 값이다.
    # 손잡이를 더 달지 않는다(롱폼에서 같은 이유로 두 번 달았다 물렀다 — 위 BAND_KNOB2 주석).
    ('long', 'text_top'): ('2026-09-25 실측 35점 — top 을 목표로 끌 수 있는 손잡이는 text_y 뿐이고, '
                           '닿는 자리(0.40·0.41)에서 mid 가 0.04~0.07 빈다. mid·bot 을 맞춘 대가다'),
}

def main():
    global THUMB_DEFAULT
    THUMB_DEFAULT = thumb_defaults()
    if not take_lock(): return
    t0 = time.time(); log = load(LOG, []); design = load(DESIGN, DEFAULT)
    step = design.get('step', 0) + 1
    did, blocked, capped = [], [], []

    # 앞 회차가 격자를 훑다가 죽었으면 design.json 에 '재보던 값'이 남아 있다 — 고른 값으로 되돌린다.
    # 이걸 안 하면 다음 회차가 그 우연한 값을 '지금 자리(cur)'로 알고 거기서부터 격자를 다시 짜고,
    # 그 사이에 나가는 썸네일도 그 값으로 그려진다(grid_pick 의 _probe 주석 참고).
    pr = design.pop('_probe', None)
    if pr and isinstance(pr, dict) and pr.get('kind') in design:
        was = design[pr['kind']].get(pr['knob'])
        if pr.get('safe') is not None and was != pr['safe']:
            design[pr['kind']][pr['knob']] = pr['safe']
            did.append(f"앞 회차가 {pr['kind']}.{pr['knob']} 격자를 훑다 죽었다 — "
                       f"재보던 값 {was} 를 고른 값 {pr['safe']} 로 되돌렸다")
        json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # 1) 수집 — 경쟁(하루 한 번이면 충분하므로 마지막 '수집'이 12시간 넘었을 때만)
    # 2026-09-25에 찾았다: 이 문이 마지막 **수집** 시각이 아니라 마지막 **회차** 시각(log[-1]['at'])과
    # 견주고 있었다. 이 루프는 두 시간마다 도니까 그 간격은 늘 2시간 안쪽이라 12시간을 영영 못 넘는다.
    # 실측: 97회차를 도는 동안 '경쟁 수집'이 did 에 뜬 것은 **딱 한 번**(2026-09-23 18:02, 첫 바퀴)이고,
    # design/*/meta.json 12개가 그때 이후 41시간째 그대로였다(영상 459편 고정).
    # 그래서 89~97회차 아홉 바퀴가 같은 296장·같은 459개 제목에서 같은 답을 다시 뽑고 있었다 —
    # 루프가 안 발전한 게 아니라 **새 재료가 한 번도 안 들어왔다**. 이제 수집 시각을 따로 적고 그것과 견준다.
    lastcol = design.get('collected_at') or (log[0]['at'] if log else '2000-01-01 00:00')
    if time.time() - time.mktime(time.strptime(lastcol, '%Y-%m-%d %H:%M')) > 12 * 3600:
        # 상한 2400초(40분)는 회차 예산(loop 40분)과 같아서, 수집이 길어지면 바퀴가 통째로 예산을 넘긴다.
        # 수집은 못 끝내도 다음 회차에 이어받으면 되는 일이라 1200초로 줄였다(나머지 단계가 약 310초).
        out = sh(os.path.join(HERE, 'ytdesign.py'), '--all', '40', timeout=1200)
        did.append('경쟁 수집: ' + str(len(re.findall(r'구독', out))) + '채널')
        design['collected_at'] = time.strftime('%Y-%m-%d %H:%M')
    else:
        did.append(f'경쟁 수집 건너뜀 — 마지막 수집 {lastcol} (12시간 안)')
    ours_before, ch_views = our_shorts_stats()

    # 2) 측정 — 경쟁 썸네일이 한 장도 안 바뀌었으면 다시 재지 않는다(같은 파일 → 같은 spec.json)
    fp_now, fp_old = spec_fingerprint(), load(SPEC_FP, {})
    if fp_now == fp_old and os.path.exists(SPEC):
        did.append(f"경쟁 썸네일 {fp_now['n']}장 그대로 — 지난 측정값을 쓴다(재측정 건너뜀)")
    else:
        out = sh(os.path.join(HERE, 'thumbstat.py'), timeout=1200)
        m = re.search(r'썸네일 (\d+) 장 측정', out); did.append(f'경쟁 썸네일 {m.group(1) if m else "?"}장 재측정')
        if os.path.exists(SPEC):
            json.dump(fp_now, open(SPEC_FP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    spec = load(SPEC, {})
    # 2-b) 세 칸(위·가운데·아래)은 손잡이 하나를 나눠 쓰므로 밀지 않고 격자로 재서 고른다
    bands = {}
    for kind in ('short', 'long'):
        if spec.get(kind): bands[kind] = tune_bands(design, spec, kind, did, blocked)
    render_samples(keep_chart=True)   # 고른 값으로 샘플을 새로 그린다
    ours = measure_ours()             # 그 샘플만 잰다
    # 조회로는 판정할 수 없을 때(전부 비공개) 쓸 판정 눈금 — 경쟁 판형과의 세 칸 거리.
    # 이 값은 공개 여부와 무관하게 매 회차 재어지므로, 조정이 실제로 경쟁에 가까워졌는지 숫자로 남는다.
    px_err = {}
    for kind in ('short', 'long'):
        e, _ = band_err(ours, kind, spec)
        if e is not None: px_err[kind] = round(e, 4)

    # 3) 비교 — 우리 평균 vs 경쟁 상위 중앙값
    gaps = []
    for kind in ('short', 'long'):
        tgt = spec.get(kind) or {}
        mine = [r for r in ours if (r['short'] if kind == 'short' else not r['short'])]
        if not mine or not tgt: continue
        for k, want in tgt.items():
            if k not in ('yellow', 'contrast', 'white', 'bright', 'text_top', 'text_mid', 'text_bot', 'sat', 'dark'): continue
            got = statistics.median(r[k] for r in mine)
            # 2026-09-25: 25% 는 '상대' 기준뿐이라 값이 0 근처인 항목은 눈에 안 보이는 차이로도 걸렸다.
            # short.yellow 가 그랬다 — 우리 0.0114 대 경쟁 0.0087, 노란 픽셀 비율로 0.27%포인트 차이다.
            # 이 항목들은 전부 0~1로 정규화된 값이다(yellow·white·dark·text_* 는 픽셀 비율,
            # bright·contrast·sat 은 V.mean/V.std/S.mean 을 255로 나눈 값 — thumbstat.measure 참고).
            # 그래서 같은 자로 잴 수 있다. 1%포인트 안쪽 차이는 손잡이를 돌려도 화면이 달라지지 않으므로
            # 차이로 세지 않는다. 안 그러면 계기판이 회차마다 노이즈를 '미해결'로 띄우고,
            # 다음 회차가 그걸 닫으려고 격자를 처음부터 다시 훑는다.
            if want and abs(got - want) / max(want, 1e-3) > 0.25 and abs(got - want) >= 0.01:
                gaps.append({'kind': kind, 'key': k, 'ours': round(got, 4), 'target': round(want, 4), 'diff': round(got - want, 4)})
    gaps.sort(key=lambda g: -abs(g['diff'] / max(g['target'], 1e-3)))

    # 4) 조정 — 측정 차이를 '그리기 손잡이'로 옮긴다. (손잡이, 방향계수, 최소~최대)
    BINARY = {'yellow_bottom', 'num_yellow'}
    RULE = {
      # ※ text_top/text_mid/text_bot 항목은 2026-09-23부터 tune_bands(격자 실측)가 맡는다. 아래 계수는 그때까지의 기록으로 남겨 둔다.
      # 손잡이·계수·한계는 판형별로 다르게 둘 수 있다({'long':..,'short':..}). 쇼츠는 세로 1920이라 두 줄을 붙여 두면
      # text_y를 어디로 옮겨도 top·bot 두 칸을 같이 못 채운다 — 5회차 연속 "듣지 않는 손잡이"로 막혀 있었다(step19~23).
      # 그래서 쇼츠는 두 줄을 위·아래로 벌리는 text_spread(thumb.py)로 바꿨다. 롱폼(1280x720)은 text_y가 듣는다.
      # 쇼츠 계수는 실측 5점(spread 0/.3/.5/.7/1.0)에서 나온 기울기다: text_bot 0→0.1265(0.5에서 포화),
      # text_top 0.0329→0.1496, text_mid 0.2245→0(반대로 줄어든다). 기울기 0.25/단위 → 계수 -4.0.
      # 0.55 위로는 아랫줄이 화면 아래 한계에 붙어 더 안 움직이므로 한계를 0.55로 둔다.
      # 2026-09-23 step30 재실측(쇼츠 배경 3종 중앙값, spread 0.4/0.55/0.7/0.85/1.0):
      #   text_bot 0.1117/0.1117/0.1260/0.2310/0.2416 — 0.55~0.7 구간이 평평해서 "한계에 붙었다"고 오판했을 뿐,
      #   0.85를 넘기면 다시 오른다. 한계를 1.0으로 열고 기울기 0.2887/단위에서 계수 -3.5를 다시 냈다.
      'text_top': ({'long': 'text_y', 'short': 'text_spread'}, {'long': +0.45, 'short': -3.5},
                   {'long': 0.15, 'short': 0.0}, {'long': 0.80, 'short': 1.0}),
      'text_bot': ({'long': 'text_y', 'short': 'text_spread'}, {'long': -0.45, 'short': -3.5},
                   {'long': 0.15, 'short': 0.0}, {'long': 0.80, 'short': 1.0}),
      # 밝기: 상한 0.9는 '원본 그대로'라 롱폼이 0.2825에서 멈춰 목표 0.4307에 닿지 못했다(step30 막힘).
      # thumb.py 클램프를 1.8까지 열고 실측(0.6/0.9/1.2/1.5/1.8 → bright 0.2255/0.2825/0.3386/0.3926/0.4402),
      # 기울기 0.1752/단위 → 계수 -5.7. 옛 -1.2는 기울기의 1/5라 한 칸에 0.02씩만 올라가 상한에 먼저 붙었다.
      'bright':   ('bg_bright', -5.7, 0.12, 1.80),
      'dark':     ('bg_bright', +3.8, 0.12, 1.80),
      # 배경 채도. 2026-09-23 실측(bg_sat 0.4/0.8/1.5/2.2/3.0 → sat 0.0985/0.1871/0.3197/0.4167/0.4971),
      # 기울기 0.1533/단위 → 계수 -6.5. 여섯 회차 "그리기 손잡이 없음"이던 항목이다.
      'sat':      ('bg_sat', -6.5, 0.0, 3.0),
      # 흰 면적은 흰 글자 픽셀에서 나온다. 외곽선은 검정이라 아무리 얇게 해도 흰 면적이 안 줄어 stroke_ratio가 한계 40에 붙어
      # 버렸다(2026-09-23 step20). 그래서 글자 크기 배율로 바꿨다. 면적은 크기의 제곱이라 계수를 작게 잡아 한 칸씩 간다.
      # 흰 면적과 아랫줄 글자량이 같은 손잡이(text_scale)를 공유한다 — 2026-09-23 실측(spread 1.0 고정,
      # text_scale 0.66/0.8/0.9/1.0 → text_bot 0.2251/0.2603/0.2803/0.3112, white 0.0114/0.0167/0.0205/0.0257).
      # 쇼츠는 목표가 서로 반대라(text_bot 0.3093 ↑ / white 0.0107 ↓) 둘 다 만족하는 값이 없어 하한 0.9에 붙어
      # step38~39 두 회차 연속 "한계에 붙어 더 못 감"으로 막혔다.
      # 2026-09-24: 쇼츠를 text_tint(줄마다 아래쪽 몇 %를 아이보리로 칠하나, thumb.py)로 바꿨다. 글자 크기를
      # 건드리지 않으므로 white 와 text_bot 이 더는 싸우지 않는다 — 실측(tint 0/0.2/0.4/0.6/0.8/1.0):
      #   white     0.0273/0.0273/0.0236/0.0150/0.0066/0.0003   (목표 0.0107 이 구간 안에 있다)
      #   yellow    0.0086 전 구간 그대로 — 강조색을 얼음빛 파랑으로 잡아 노랑 손잡이와 안 싸운다
      #   text      0.2667 전 구간 그대로, text_bot 0.1898 도 그대로 — 글자량은 1픽셀도 안 줄어든다
      # 0.4~1.0 기울기 -0.0388/단위 → 계수 +25.8(흰 면적은 tint가 커질수록 줄어들어 부호가 text_scale과 반대).
      # 0~0.2는 아직 임계(채도 40)를 못 넘어 평평하다. 롱폼은 white 차이가 없어 그대로 text_scale 을 쓴다.
      # 2026-09-24 화면 검증: 75회차가 text_tint 를 0.726 → 1.0(한계)로 올렸다. 숫자로는 white 가 목표에
      # 다가가지만 실제 썸네일을 보니 글자가 흰빛을 잃고 잿빛 파랑으로 죽어 배경 차트 위에서 안 읽힌다.
      # 같은 배경·같은 문구로 0.7 / 0.85 / 1.0 을 그려 눈으로 견줬고 0.7 에서만 글자가 희게 남았다.
      # tint_v 하한 0.75 와 같은 이유로 윗한계를 0.7 로 막는다 — 숫자를 맞추려고 글자를 죽이지 않는다.
      # 그래서 short.white 는 앞으로 '한계에 붙어 막힘'으로 남는다. 그게 맞는 상태다.
      # 2026-09-25: 롱폼 white 에서 손잡이를 뗐다. 흰 면적을 늘리는 길이 '글자를 키운다' 하나뿐인데,
      # 그 손잡이는 text_mid(우리 0.5784 vs 경쟁 0.0784, 상대 638%)를 정면으로 망친다. white 차이는
      # 상대 32%(0.0851 vs 0.1247)다. 한 손잡이를 두 목표가 나눠 쥐면 작은 쪽이 이겨 버린다 —
      # 실제로 text_scale 은 white 때문에 한계 1.0 에 못 박힌 채였고, 그래서 글자가 가운데 띠를 뒤덮었다.
      # 큰 차이 쪽에 손잡이를 준다: text_scale 은 이제 tune_bands 격자가 쥔다(BAND_KNOB2['long']).
      # 2026-09-26 loop 회차: '배경 자료를 무엇으로 깔 것인가'를 처음으로 숫자로 재 봤다.
      # 경쟁 롱폼 528장에서 흰 픽셀이 글자 위에 있나 배경에 있나를 갈랐다(글자 지도로 가름):
      #   조회 상위 176장  white 0.1250 · 그중 글자 위 2.8% · 글자면적 0.077
      #   조회 하위 176장  white 0.0785 · 그중 글자 위 13.2% · 글자면적 0.090
      #   white 상위 176장 white 0.1788 · 그중 글자 위 2.8% · 글자면적 0.062  ← 글자는 오히려 적다
      # 즉 경쟁의 흰 면적은 97%가 배경에서 온다. 글자를 희게·크게 해서 닫을 수 있는 차이가 아니다
      # (그 길은 2026-09-25에 text_mid 를 망가뜨려 이미 뗐다 — 위 주석). 흰 면적이 많은 쪽이 글자면적은
      # 더 적다는 것도 같은 말이다. 남은 길은 하나뿐이다: 롱폼 배경을 밝은 면으로 바꾸는 것.
      # 그런데 그건 '다크 카드' 정체성을 바꾸는 일이라 루프가 혼자 정할 것이 아니다 —
      # tools-wanted.md 에 사람이 볼 항목으로 올린다. 그때까지 long.white 는 한계로 남는 게 맞다.
      'white':    ({'long': None, 'short': 'text_tint'}, {'long': None, 'short': +25.8},
                   {'long': None, 'short': 0.0}, {'long': None, 'short': 0.7}),
      # 아랫줄 노랑 글자 비율(0~1). 2026-09-23 실측 5점(0/.25/.5/.75/1): 롱폼 0.0007→0.0533, 쇼츠 0.0003→0.0199.
      # 기울기가 판형마다 달라(롱폼 0.052 · 쇼츠 0.020) 계수를 판형별로 둔다.
      # 2026-09-24: 쇼츠는 yellow_frac 으로 못 맞춘다. 그 손잡이는 '글자 몇 개'라 계단이기 때문이다 —
      # 실측 0/0.0997 → 0.0003 · 0.1088~0.2 → 0.0099 · 0.3~0.6 → 0.0169 · 1.0 → 0.0345.
      # 경쟁 목표 0.0067 이 '0개'와 '1개' 사이에 있어 53~61회차 내내 "사이를 좁혔는데도 못 맞춘다"로 막혔다.
      # 그래서 쇼츠는 yellow_tint(마지막 줄 글자의 아래쪽 몇 %를 노랑으로 칠하나, thumb.py)로 바꿨다.
      # 새 잉크를 안 더해서 글자량·대비가 안 흔들린다 — 실측(tint 0.34/0.38/0.42/0.46):
      #   yellow   0.0006/0.0022/0.0049/0.0071   (목표 0.0067 이 구간 안에 있다)
      #   text_bot 0.3008/0.3007/0.3009/0.3009 · text 0.3397 전 구간 그대로 · contrast 0.2622~0.2639 그대로
      # 0.30 아래는 글자 아래 빈 공간이라 평평하다(0.0003) — 하한을 0.30 으로 둬 죽은 구간에 안 들어가게 한다.
      # 기울기 0.061/단위 → 계수 -16.4.
      # 밑줄(형광펜) 안도 실측했지만 버렸다: 노랑은 잘 듣는데 text_bot 이 0.3009 → 0.3894 로 뛴다
      # (측정의 글자 지도가 가장자리를 25x9 로 부풀려 가로줄 하나가 아래 칸을 통째로 글자로 만든다).
      'yellow':   ({'long': 'yellow_frac', 'short': 'yellow_tint'}, {'long': -19.0, 'short': -16.4},
                   {'long': 0.0, 'short': 0.30}, 1.0),
      # 대비. 롱폼은 패널 진하기로 민다. 쇼츠는 panel_alpha 가 듣지 않는 손잡이였다(128→0.2623, 150→0.2638).
      # 2026-09-24 갈라 재서 원인을 찾았다(경쟁 상위 10장 vs 우리 3장, 글자 지도로 갈라 잰 값):
      #   배경만 대비   우리 0.0531 < 경쟁 0.0734  ← 우리 배경은 이미 경쟁보다 평평하다
      #   글자자리 대비 우리 0.4063 > 경쟁 0.2732 · 아주 밝은 픽셀(V>0.80) 우리 0.0913 vs 경쟁 0.0235
      # tools-wanted.md 에 "배경을 누르는 손잡이(bg_flat)를 달아야 하나, 자료가 보여야 한다는 지시와 부딪힌다"고
      # 사람 판단을 올려 뒀던 항목인데, 숫자가 아니라고 답했다 — 배경은 건드릴 것이 아니다.
      # 넘치는 대비는 얼음빛 파랑(V=255)으로 글자 아래 88%를 칠한 데서 온다. 그래서 강조색 밝기(tint_v)를 단다.
      # 실측(tint_v 1.0/0.85/0.7/0.55/0.4): contrast 0.2619/0.2285/0.1977/0.1698/0.1463
      #   white 0.0137/0.0126/0.0125/0.0110/0.0106 · yellow 0.0071~0.0077 · text_bot 0.3009 전 구간 그대로.
      # 기울기 0.1827/단위 → 계수 -5.47.
      # 하한 0.75 는 화면 검증에서 나왔다(2026-09-24). tint_v 0.6 은 숫자로는 목표(0.1791)에 딱 맞는데
      # 실제 그림을 보니 글자가 흰빛을 잃고 회색으로 죽는다 — 썸네일이 해야 할 일(눈에 띄기)을 잃는다.
      # 숫자를 맞추려고 글자를 죽이지 않는다. 0.75 아래로는 안 내려간다. 그래서 못 닫으면 '막힘'으로 남는 게 맞다.
      # 2026-09-26: 롱폼 손잡이를 panel_alpha → bg_contrast 로 바꿨다. 9/25 에 '한계 확정'으로 닫을 때
      # 이유를 "차이가 배경에서 온다"고 적어 놓고, 정작 배경을 만지는 손잡이는 밝기·채도 둘뿐이라
      # 대비는 손댈 길이 자체가 없었다. 배경을 '누르는' 쪽(bg_flat)은 자료가 안 보여 안 된다고 이미
      # 판단했지만 '올리는' 쪽은 그 판단에 안 걸린다 — 자료가 더 또렷해진다.
      # 실측(2026-09-26, 같은 배경 _bg_chart.png·같은 문구, bg_contrast 1.0/1.3/1.6/2.0/2.4):
      #   contrast 0.2481/0.2628/0.2804/0.2932/0.3051  ← 글자 뒤 띠 손잡이 4종을 다 민 0.31 을 혼자 낸다
      #   white    0.0395 전 구간 그대로 · text_mid 0.1017~0.1042 · text_bot 0.0384~0.0388 (안 흔들린다)
      #   bright   0.3015→0.3521 은 같이 오른다 — 'bright' 항목이 뜨면 bg_bright 가 되받는다
      # 기울기 0.0407/단위 → 계수 -24.6. 윗한계 2.4 는 화면 검증에서 정했다(1.0·2.0·2.4 를 같은 배경·
      # 같은 문구로 그려 눈으로 견줬다): 2.4 에서도 막대·구 이름·출처 글씨가 다 읽히고 글자는 희게 남는다.
      # 2026-09-26 재실측: 물렸다. bg_contrast 2.4 는 contrast 를 실제로 닫았다(131회차 gap 목록에서
      # long.contrast 가 사라졌다). 그런데 닫는 방식이 틀렸다 — 같은 회차에 이런 것들이 같이 왔다:
      #   long.sat 0.5826 vs 0.3453 새로 벌어짐 → 루프가 bg_sat 을 1.4032 에서 한계 0.0 까지 내렸다
      #   세 칸 오차 합 0.6187 → 2.0283 (3배) · text_top 0.1655 → 0.1955 · text_mid 새 차이 0.1001
      # 화면으로 봤다: 배경이 완전한 흑백이 됐다. 강조한 금천 막대(노랑)가 나머지 막대와 같은 회색이 되어
      # 차트가 하려던 말이 사라졌다. 자료를 보여 주라는 지시와 정면으로 어긋난다.
      # 왜 숫자는 좋아졌나: 대비를 올리면 배경의 결이 세지고, thumbstat 의 글자 지도(에지)가 그 결을
      # 글자로 센다. 그래서 text_top·text_mid 가 같이 흔들렸다. 배경 대비로 contrast 를 맞추는 것은
      # 눈금을 맞추는 것이지 썸네일을 좋게 하는 것이 아니다. 손잡이는 thumb.py 에 남겨 두되(기본 1.0 이라
      # 그림은 안 바뀐다) 루프에는 다시 안 맨다. 남은 길은 여전히 '배경 자료를 무엇으로 깔 것인가'다.
      'contrast': ({'long': None, 'short': 'tint_v'}, {'long': None, 'short': -5.47},
                   {'long': None, 'short': 0.75}, {'long': None, 'short': 1.0}),
      'text_mid': ('text_y', 'center', 0.15, 0.80),   # 가운데 띠에 글자가 없으면 text_y를 0.5 쪽으로 당긴다
    }
    # 손잡이 없는 차이가 위쪽 세 자리를 잡아먹지 않게 먼저 갈라 둔다
    knobbed = [g for g in gaps if g['key'] in RULE and g['key'] not in BAND_KEYS]
    for g in gaps:
        if g['key'] in BAND_KEYS:
            # 2-b 격자 탐색이 이미 최선을 골랐다. 여기서 또 밀면 서로 밀쳐 흔들린다.
            # 다만 격자를 끝까지 훑어도 못 닿는다고 실측으로 확인한 항목은 '못 푼 숙제'가 아니라 '닫히지 않는 항목'이다.
            why = BAND_CAPPED.get((g['kind'], g['key']))
            if why:
                capped.append(f"{g['kind']}.{g['key']} — 격자를 다 훑어도 못 닿는다: {why}"
                              f" (우리 {g['ours']} vs 경쟁 {g['target']})")
            continue
        if g['key'] not in RULE:
            blocked.append(f"{g['kind']}.{g['key']} 우리 {g['ours']} vs 경쟁 {g['target']} — 그리기 손잡이 없음")
    memo = design.setdefault('_memo', {})   # "종류.항목.손잡이=값" → 그 값일 때 실측치. 같은 자리를 또 밟지 않으려고 적어 둔다
    moved_knobs = set()   # 같은 손잡이를 한 바퀴에 두 번 움직이면 뒤 항목이 앞 항목을 덮어써 값이 계속 뒤집힌다(2026-09-23)
    def bykind(v, kind):
        return v.get(kind) if isinstance(v, dict) else v
    for g in knobbed[:3]:
        knob, coef, lo, hi = (bykind(v, g['kind']) for v in RULE[g['key']])
        if knob is None:
            # 손잡이를 일부러 뗀 자리는 조용히 넘기지 않는다 — 넘기면 다음 회차가 또 손잡이를 찾는다.
            capped.append(f"{g['kind']}.{g['key']} — 이 판형에서는 손잡이를 떼기로 정했다"
                          f" (우리 {g['ours']} vs 경쟁 {g['target']}, RULE 주석에 이유)")
            continue
        if (g['kind'], knob) in moved_knobs:
            blocked.append(f"{g['kind']}.{g['key']} — 같은 손잡이 {knob} 를 이번 바퀴에 다른 항목이 이미 움직였다, 다음 바퀴에 잰다")
            continue
        if coef is None: continue
        d = design.setdefault(g['kind'], {})
        cur = d.get(knob)
        if cur is None:
            # 새로 생긴 손잡이는 thumb.py가 쓰는 기본값에서 시작한다. 예전에는 text_spread만 열어 둬서
            # bg_sat 같은 새 손잡이를 RULE에 넣어도 design.json에 없다는 이유로 영영 건너뛰었다(2026-09-23).
            cur = d[knob] = float(THUMB_DEFAULT.get(g['kind'], {}).get(knob, 0.0))
        tag = f"{g['kind']}.{g['key']}.{knob}"
        # 실측치는 '그때 나머지 손잡이가 어디에 있었나'에 딸려 있다. 예전에는 손잡이 값만 적어 둬서, 다른 손잡이가
        # 움직인 뒤에 잰 값과 그 전에 잰 값을 같은 줄에 놓고 비교했다 — short.white 실측이 text_tint 0.7689/0.8059/
        # 0.85/0.9455 에서 0.0076/0.0184/0.0144/0.0028 로 오르락내리락한 것이 그 탓이다(강조색 얼음빛 파랑이
        # 채도 40 아래라 흰 면적으로 세어져, yellow_frac 이 움직이면 white 도 같이 움직인다). 그래서 나머지 설정을
        # 지문으로 같이 적고, 값끼리 견줄 때는 지문이 같은 것만 쓴다.
        ctx = ctx_tag(design, g['kind'], knob)
        memo[f'{tag}={cur}@{ctx}'] = g['ours']
        seen, same = {}, {}   # seen: 지문 상관없이 전부(듣는 손잡이인지 보는 용도) · same: 지문이 지금과 같은 것만
        for mk, mo in memo.items():
            if not mk.startswith(tag + '='): continue
            v, _, c = mk[len(tag) + 1:].partition('@')
            seen[v] = mo
            if c == ctx: same[v] = mo
        # 손잡이를 움직였는데 실측이 그대로면 그 항목에 듣지 않는 손잡이다 — 더 돌리지 않는다
        if len(seen) > 1 and max(seen.values()) - min(seen.values()) < 0.002:
            blocked.append(f"{g['kind']}.{g['key']} — {knob} 를 {'/'.join(sorted(seen))} 로 바꿔도 실측 그대로, 듣지 않는 손잡이")
            continue
        # 이미 잰 값들이 목표를 위·아래로 끼고 있으면(사이에 낀다) 계수로 미는 대신 그 사이를 갈라 들어간다.
        # 계수 밀기는 한 방향으로만 가므로 한 번 목표를 지나쳐 버리면 되돌아올 길이 없다 — 다음 회차에 그 값을
        # 다시 제안해도 "이미 재봤고 더 나빴다"에 걸려 영영 그 자리에 선다. short.white 가 그 꼴이었다:
        # text_tint 0.85 → 0.0144(목표 0.0107 위), 0.9455 → 0.0028(아래). 답은 두 값 사이인데 38~50회차 내내
        # 못 들어갔다. 사이에 낀 두 점을 직선으로 이어 목표를 지나는 자리를 집으면 한 번에 들어간다.
        if coef != 'center' and knob not in BINARY and len(same) > 1:
            pts = []
            for v, o in same.items():
                try: pts.append((float(v), o))
                except ValueError: pass
            hi_pts = [(v, o) for v, o in pts if o > g['target']]
            lo_pts = [(v, o) for v, o in pts if o < g['target']]
            pair = min(((a, b) for a in hi_pts for b in lo_pts), key=lambda ab: abs(ab[0][0] - ab[1][0]), default=None)
            if pair:
                (va, oa), (vb, ob) = pair
                span = abs(hi - lo) if hi is not None and lo is not None else 1.0
                if abs(va - vb) <= max(span * 0.01, 1e-4):
                    blocked.append(f"{g['kind']}.{g['key']} — {knob} {min(va, vb)}~{max(va, vb)} 까지 좁혔는데도 목표 {g['target']} 를 못 맞춘다, 다른 손잡이가 필요")
                    continue
                hit = va + (vb - va) * (g['target'] - oa) / (ob - oa)
                hit = min(max(hit, min(va, vb)), max(va, vb))
                cand = round(hit, 4) if isinstance(cur, float) else int(round(hit))
                if str(cand) in same or cand == cur:
                    blocked.append(f"{g['kind']}.{g['key']} — {knob} 사이 가르기가 이미 재본 {cand} 로 돌아온다, 다른 손잡이가 필요")
                    continue
                moved_knobs.add((g['kind'], knob))
                d[knob] = cand
                did.append(f"{g['kind']}.{knob} {cur} → {cand} ({g['key']} 목표 {g['target']} 를 {va}={oa}/{vb}={ob} 사이에서 갈라 집음)")
                continue
        # 계수는 모두 '우리 - 경쟁' 기준으로 적혀 있다(주석 참고). 부호를 뒤집지 말 것.
        if coef == 'center':
            # 가운데 띠 비율은 text_y에 대해 단조가 아니다 — 0.5 쪽으로 당기기만 한다
            if g['ours'] >= g['target']: continue
            delta = (g['target'] - g['ours']) * 0.45 * (1 if 0.5 > cur else -1)
        else:
            delta = (g['ours'] - g['target']) * coef
        new = min(max(cur + delta, lo), hi)
        if knob in BINARY:                       # 0/1 스위치 — 0.5를 넘어서면 뒤집는다
            new = 1 if cur + delta >= 0.5 else 0
        else:
            new = round(new, 4) if isinstance(cur, float) else int(round(new))
        if new == cur:
            if cur in (lo, hi):
                cap = CAPPED.get((g['kind'], g['key']))
                if cap and cap[0] == knob and abs(cur - cap[1]) < 1e-9:
                    capped.append(f"{g['kind']}.{g['key']} — {knob} 는 {cur} 에서 멈추기로 정했다: {cap[2]}"
                                  f" (우리 {g['ours']} vs 경쟁 {g['target']})")
                else:
                    blocked.append(f"{g['kind']}.{g['key']} — {knob} 가 한계 {cur} 에 붙어 더 못 감, 다른 손잡이가 필요")
            continue
        moved_knobs.add((g['kind'], knob))
        prev = same.get(str(new))
        if prev is not None and abs(prev - g['target']) >= abs(g['ours'] - g['target']):
            blocked.append(f"{g['kind']}.{g['key']} — {knob}={new} 는 이미 재봤고 더 나빴다({prev} vs 지금 {g['ours']}), 그대로 둠")
            continue
        d[knob] = new
        did.append(f"{g['kind']}.{knob} {cur} → {new} ({g['key']} 우리 {g['ours']} vs 경쟁 {g['target']})")
    if not gaps: did.append('썸네일 수치는 경쟁 상위와 25% 안쪽 — 조정 없음')

    # 5) 지난 조정의 효과 판정
    # 2026-09-24에 고친 것: 예전에는 '최신 10편 조회 합계'로 판정했다. 새 영상을 올리면 그 합계가
    # 무너지므로(실측 2089 -> 120 -> 6) 발행할 때마다 "조회 하락"으로 읽혀 직전 회차의 조정을 전부 되돌렸다.
    # 그래서 short.contrast / short.white 는 회차마다 넣었다 뺐다만 반복하고 영영 안 닫혔다(step 64~66).
    # 이제는 (a) 누적이라 절대 줄지 않는 채널 총조회로 '시간당 늘어난 조회'를 재고,
    #        (b) 그 창에서 실제로 늘어난 조회가 MIN_GAIN 미만이면 판정을 보류한다(되돌리지 않는다).
    #        (c) 최근 10편이 전부 비공개면 조회는 영영 0이므로 그 사실을 판정문에 적어 둔다.
    MIN_GAIN = 30
    verdict, now_rate, prev_rate = '', None, None
    if ch_views is not None and log:
        pv, pat = log[-1].get('ch_views'), log[-1].get('at')
        if pv is None:
            verdict = f'채널 총조회 {ch_views} — 지난 회차 기록이 없어 이번 회차부터 비교한다'
        else:
            hours = max(0.25, (time.time() - time.mktime(time.strptime(pat, '%Y-%m-%d %H:%M'))) / 3600)
            gain = ch_views - pv
            now_rate = round(gain / hours, 2)
            prev_rate = log[-1].get('gain_rate')
            pub = sum(1 for v in ours_before if v.get('privacy') == 'public')
            verdict = (f'채널 총조회 {pv} -> {ch_views} ({gain:+}회 / {hours:.1f}시간 = 시간당 {now_rate})'
                       f' · 최근 10편 중 공개 {pub}편')
            if pub == 0:
                # 2026-09-24에 고친 것: 최근 10편이 전부 비공개면 채널 총조회가 늘어도 그건 **옛 공개 영상**이
                # 번 조회다 — 이번 회차 썸네일 손잡이와 아무 상관이 없다. 그런데도 아래 되돌리기 가지는
                # gain >= MIN_GAIN 만 넘으면 '시간당 조회가 떨어졌다'며 직전 조정을 되돌릴 수 있었다.
                # 공개 0편이면 조회는 판정 근거가 못 되므로 되돌리기에 쓰지 않는다.
                verdict += ' -> 조회로는 판정 안 함(공개 0편, 늘어난 조회는 옛 공개 영상 몫)'
            elif gain < MIN_GAIN:
                verdict += f' -> 판정 보류(늘어난 조회 {gain}회 < {MIN_GAIN}회, 되돌리지 않는다)'
            elif prev_rate is not None and now_rate < prev_rate * 0.7 and log[-1].get('changed'):
                for c in log[-1]['changed']:
                    mm = re.match(r'(\w+)\.(\w+) ([\d.]+) ', c)
                    if mm and mm.group(1) in design and mm.group(2) in design[mm.group(1)]:
                        design[mm.group(1)][mm.group(2)] = float(mm.group(3))
                        did.append(f'되돌림 {mm.group(1)}.{mm.group(2)} -> {mm.group(3)} '
                                   f'(시간당 조회 {prev_rate} -> {now_rate})')

    # 조회가 못 재는 회차에도 '나아졌나'를 숫자로 남긴다 — 경쟁 판형과의 세 칸 거리 비교.
    if px_err:
        prev_px = next((r.get('px_err') for r in reversed(log) if r.get('px_err')), None)
        now_sum = round(sum(px_err.values()), 4)
        if prev_px:
            was_sum = round(sum(prev_px.values()), 4)
            arrow = '줄었다' if now_sum < was_sum - 1e-4 else ('늘었다' if now_sum > was_sum + 1e-4 else '그대로')
            verdict += f' · 경쟁 판형 거리 {was_sum} -> {now_sum} ({arrow})'
        else:
            verdict += f' · 경쟁 판형 거리 {now_sum} (이번 회차부터 비교한다)'

    design['step'] = step
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 바꾼 값으로 우리 샘플을 다시 만든다 — 안 그러면 다음 회차가 같은 차이를 또 잡는다
    if any('→' in d for d in did): did.append('다음 회차가 바뀐 값으로 다시 그려 잰다')
    rec = {'step': step, 'at': time.strftime('%Y-%m-%d %H:%M'), 'sec': int(time.time() - t0),
           'changed': [d for d in did if '→' in d], 'did': did, 'gaps': gaps[:6], 'blocked': blocked[:8], 'bands': bands,
           'capped': [c.split(' —')[0] for c in capped], 'capped_why': capped,
           'ours_views': sum(v['views'] for v in ours_before[:10]) if ours_before else None,
           'ch_views': ch_views, 'gain_rate': now_rate, 'px_err': px_err, 'verdict': verdict}
    log.append(rec); json.dump(log[-200:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[루프 {step}회차] {rec['sec']}초")
    for d in did: print(' ·', d)
    for b in blocked[:8]: print(' · 막힘:', b)
    for c in capped: print(' · 한계 확정:', c)
    if verdict: print(' ·', verdict)
    capkeys = {c.split(' —')[0] for c in capped}
    open_gaps = [g for g in gaps if f"{g['kind']}.{g['key']}" not in capkeys]
    if open_gaps: print(' 남은 차이:', ', '.join(f"{g['kind']}.{g['key']} {g['ours']}→{g['target']}" for g in open_gaps[:5]))
    elif gaps: print(' 남은 차이: 없음 — 남은 것은 한계 확정 ' + ', '.join(sorted(capkeys)))

if __name__ == '__main__':
    try: main()
    finally: drop_lock()
