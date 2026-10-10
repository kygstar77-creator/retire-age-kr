# 롱폼 렌더 관문 — RULES.md '화면 글자·그래프 규칙'(10/3 22시)·'목소리 한결같음'(10/3 22시)을 렌더 전에 코드로 막는다.
# 사고: N-1 '쌍둥이 막대'에 상위 1%와 상위 10%(1% 포함)를 나란히 그려 "상위 10%가 내는 세금이 왜 1%보다 높아?"(사장님),
#       E-2 녹음을 날 나눠 해서 뒤쪽 목소리 155→137Hz, 빠르기 1.25배까지 조절.
#   py -3.12 work/lfrender.py text   <ep폴더>                 # 화면 글자 전부 → ep/<편>/screen_text.txt (props 문자열 + 컴포지션 tsx 한글 글자)
#   py -3.12 work/lfrender.py stamp  <ep폴더> <by> [note]     # 편집 통과 표시 screen_text.edit.json(sha256 = screen_text.txt 바이트) — firemap-editor만
#   py -3.12 work/lfrender.py check  <ep폴더>                 # 관문 3개(화면 글자 편집 통과·누적 구간 막대·목소리 한결같음)만 본다
#   py -3.12 work/lfrender.py voice  <ep폴더|voice.json>      # 목소리 관문만(다시 녹음할 줄 목록)
#   py -3.12 work/lfrender.py render <ep폴더> [remotion 추가 인자…]  # 관문 3개 통과해야 npx remotion render 를 부른다
# 편 폴더 이름 E-2 → 컴포지션 E2, props work/video/e2.json, 출력 work/video/out/e2.mp4 (STATE.md에 적힌 렌더 명령과 같음).
# 우회 표시는 두지 않는다(규칙 3 "통과 전 렌더는 금지"). 화면 미리보기(node stills.mjs)는 이 관문을 거치지 않는다.
import os, re, sys, json, glob, hashlib, datetime, subprocess
from collections import Counter
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(HERE, 'video')
F0_TOL = 0.25          # 목소리 한결같음 ①: 튀는 줄만 — 그 편 중앙값 ±25%
DRIFT_MAX = 0.07       # ② 앞·뒤 절반 평균 차
IQR_MAX = 0.20         # ③ 퍼짐 IQR/중앙 — 10/11 사장님 "롱폼 무조건 하루 한 개": 0.16→0.20. 사장님이 지적한 '뒤쪽 다른 목소리'(E-2)는 앞뒤 차 −11.6%로 ② 관문이 그대로 막는다. 0.16~0.20은 공개하되 meta voice_note에 남긴다(R-1·C-1 0.18, W-1 0.19)
# 10/5 16:3x 순돌이: 줄마다 ±12%는 근거 없던 값 — 사장님이 좋다 한 E-1도 22% 줄이 걸렸다. 실측 기준(voice.json f0): 좋다 한 E-1·D-1 vs 지적된 E-2 → 줄 단위는 ±25%(튀는 줄만), 편 단위로 앞·뒤 절반 평균 차 ≤7%(E-1 −6.8·E-2 −11.6)·퍼짐 IQR/중앙 ≤0.16(E-1 0.16·E-2 0.17). 표본 4편 — 새 편이 쌓이면 다시 잰다.
TEXT_SKIP_KEYS = {'audio', 'kind', 'img', 'src', 'image', 'color', 'colors', 'id', 'font'}
MEDIA = re.compile(r'\.(wav|mp3|mp4|png|jpe?g|webp|svg|json|pcm)$', re.I)


# ───────────────────────── 편 이름 ─────────────────────────
def comp_id(ep):
    return os.path.basename(os.path.normpath(ep)).replace('-', '')          # E-2 → E2

def props_path(ep, vid=VID):
    return os.path.join(vid, comp_id(ep).lower() + '.json')                  # → work/video/e2.json


# ───────────────────────── 1. 화면 글자 뽑기 ─────────────────────────
def _walk(x, path, out):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in TEXT_SKIP_KEYS: continue
            _walk(v, f'{path}.{k}' if path else str(k), out)
    elif isinstance(x, list):
        for i, v in enumerate(x): _walk(v, f'{path}.{i}', out)
    elif isinstance(x, str):
        s = x.strip()
        if not s or MEDIA.search(s): return
        if re.fullmatch(r'[\d.,:/\- ]+', s): return                          # 날짜·숫자 열(20250102 등)은 축 값이지 글자가 아니다('1~10%'는 남긴다)
        out.append((path, ' '.join(s.split())))

def props_text(props):
    out = []; _walk(props, '', out); return out

_LIT = [re.compile(r"'([^'\n]*[가-힣][^'\n]*)'"), re.compile(r'"([^"\n]*[가-힣][^"\n]*)"'),
        re.compile(r'`([^`\n]*[가-힣][^`\n]*)`'), re.compile(r'>([^<>{}\n]*[가-힣][^<>{}\n]*)<')]

def tsx_text(src):
    """컴포지션 코드 안에 박힌 한글 화면 글자(따옴표 문자열·JSX 글자). 주석은 뺀다."""
    src = re.sub(r'\{/\*.*?\*/\}', '', src, flags=re.S); src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    out = []
    for n, line in enumerate(src.splitlines(), 1):
        line = re.sub(r'(^|[^:])//.*$', r'\1', line)
        seen = []
        for rx in _LIT:
            for m in rx.finditer(line):
                t = ' '.join(m.group(1).split())
                if t and t not in seen: seen.append(t)
        out += [(n, t) for t in seen]
    return out

def tsx_files(ep, vid=VID):
    main = os.path.join(vid, 'src', comp_id(ep) + '.tsx')
    if not os.path.exists(main): return []
    fs = [main]
    for m in re.finditer(r"from\s+'\./(parts/[\w-]+|MotionKit)'", open(main, encoding='utf-8').read()):
        p = os.path.join(vid, 'src', m.group(1) + '.tsx')
        if os.path.exists(p) and p not in fs: fs.append(p)
    return fs

def screen_text(ep, vid=VID, props=None):
    """화면 글자 전부를 한 글로. 시각·절대경로·코드 줄 번호를 넣지 않아 같은 화면 글자면 같은 바이트(해시)가 나온다."""
    pp = props_path(ep, vid)
    if props is None:
        if not os.path.exists(pp): raise FileNotFoundError(f'props 없음: {pp} (ep/<편>/<편>props.py 먼저)')
        props = json.load(open(pp, encoding='utf-8'))
    L = [f'# 화면 글자 — {os.path.basename(os.path.normpath(ep))} (lfrender.py text가 만듦. 여기를 고치지 말고 대본·props·tsx를 고친 뒤 다시 뽑는다)',
         '# 그래프 제목·부제·출처·자막(lines.text)·막대 이름·코드에 박힌 글자. 썸네일 문구는 그림이라 안 들어간다.', '',
         f'## props: video/{os.path.basename(pp)}']
    L += [f'[{p}] {t}' for p, t in props_text(props)]
    for f in tsx_files(ep, vid):
        rel = os.path.relpath(f, vid).replace(os.sep, '/')
        L += ['', f'## 화면 코드: video/{rel}'] + [f'[{os.path.basename(f)}] {t}' for n, t in tsx_text(open(f, encoding='utf-8').read())]
    return '\n'.join(L) + '\n'

def write_screen_text(ep, vid=VID, props=None):
    fn = os.path.join(ep, 'screen_text.txt')
    with open(fn, 'w', encoding='utf-8', newline='\n') as f: f.write(screen_text(ep, vid, props))
    return fn


# ───────────────────────── 1-2. 편집 통과 해시(editgate.py 방식) ─────────────────────────
def text_sha(ep):
    return hashlib.sha256(open(os.path.join(ep, 'screen_text.txt'), 'rb').read()).hexdigest()

def mark_path(ep):
    return os.path.join(ep, 'screen_text.edit.json')

def edit_check(ep):
    """(ok, 이유). 표시 없음·못 읽음·sha 없음·해시 다름은 전부 거부."""
    if not os.path.exists(os.path.join(ep, 'screen_text.txt')): return False, 'screen_text.txt 없음 — lfrender.py text 먼저'
    p = mark_path(ep)
    if not os.path.exists(p): return False, '화면 글자 편집 통과 표시(screen_text.edit.json) 없음'
    try: d = json.load(open(p, encoding='utf-8'))
    except Exception as e: return False, f'screen_text.edit.json을 못 읽음: {e}'
    if not d.get('sha'): return False, 'screen_text.edit.json에 sha 없음'
    if d['sha'] != text_sha(ep): return False, f'편집 통과({d.get("by", "?")} {d.get("at", "?")}) 뒤 화면 글자가 바뀌었다'
    return True, f'화면 글자 편집 통과 해시 일치({d.get("by", "?")} {d.get("at", "?")})'

def stamp(ep, by, note=''):
    d = {'by': by, 'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'sha': text_sha(ep), 'sha_of': 'screen_text.txt bytes'}
    if note: d['note'] = note
    with open(mark_path(ep), 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False)
    return d['sha']


# ───────────────────────── 2. 누적 구간 막대(상위 1% vs 상위 10%) ─────────────────────────
CUM = re.compile(r'^\s*\(?\s*(상위|하위)\s*(\d+(?:\.\d+)?)\s*%(?!\s*[~\-–])')   # '상위 1~10%'·'1~10%'는 비누적 구간이라 안 걸린다

def _strings(x):
    if isinstance(x, str): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from _strings(v)
    elif isinstance(x, list):
        for v in x: yield from _strings(v)

def cumulative_check(props):
    """같은 장면(그래프 하나)의 data 안 막대 이름이 '상위 N%' 누적 구간 2개 이상이면 경고.
    더 넓은 쪽 이름에 '포함'이 없으면 거부. → (ok, [경고·거부 줄])"""
    msgs, ok = [], True
    for i, s in enumerate(props.get('scenes', []) if isinstance(props, dict) else []):
        found = {}
        for t in _strings(s.get('data', {})):
            m = CUM.match(t)
            if m: found.setdefault(m.group(1), {}).setdefault(float(m.group(2)), []).append(' '.join(t.split()))
        for side, byn in found.items():
            if len(byn) < 2: continue
            ns = sorted(byn); wide = [lab for n in ns[1:] for lab in byn[n]]
            name = f"장면 {i} {s.get('kind', '')} '{s.get('title', '')}'"
            labs = ', '.join(lab for n in ns for lab in byn[n])
            if all('포함' in lab for lab in wide):
                msgs.append(f'경고 · {name}: 누적 구간 나란히({labs}) — 포함 표시 있음, 통과')
            else:
                ok = False
                msgs.append(f'거부 · {name}: 누적 구간 나란히({labs}) — 넓은 쪽이 좁은 쪽을 품는다. '
                            f"'{side} 1% / 1~10% / …'처럼 겹치지 않게 나누거나(빼기 계산식은 facts.txt에) 막대 이름에 '({side} {ns[0]:g}% 포함)'을 적는다")
    return ok, msgs


# ───────────────────────── 3. 목소리 한결같음 ─────────────────────────
def voice_check(vj):
    """voice.json(dict) → (ok, 결과 dict). 줄마다 f0 중앙값 ±12%·tempo 1.0·녹음 날짜 한 날.
    voice.json에 기록이 없는 항목은 지어내지 않고 '확인 안 함'으로 적는다(f0·tempo 없음은 거부, 날짜 없음은 경고)."""
    rows = []
    for si, s in enumerate(vj.get('sections', [])):
        for li, l in enumerate(s.get('lines', [])):
            if not l.get('audio'): continue
            d = l.get('date') or l.get('rec') or l.get('recorded') or l.get('recorded_at')   # lfvoice build는 'rec'에 적는다
            rows.append({'at': f'{si}:{li}', 'section': s.get('title', ''), 'text': l.get('text', ''),
                         'f0': l.get('f0'), 'tempo': l.get('tempo'), 'date': str(d)[:10] if d else None})
    res = {'lines': len(rows), 'median_f0': None, 'lo': None, 'hi': None, 'dates': {}, 'redo': [], 'notes': []}
    if not rows:
        res['notes'].append('소리 있는 줄 없음'); return False, res
    fs = sorted(r['f0'] for r in rows if isinstance(r['f0'], (int, float)) and r['f0'] > 0)
    if fs:
        n = len(fs); med = fs[n // 2] if n % 2 else (fs[n // 2 - 1] + fs[n // 2]) / 2
        res.update(median_f0=round(med, 1), lo=round(med * (1 - F0_TOL), 1), hi=round(med * (1 + F0_TOL), 1))
    else:
        res['notes'].append('f0 기록 없음 — 음높이 확인 안 함(lfvoice.py build로 voice.json을 다시 만들면 f0가 들어간다)')
    if all(r['tempo'] is None for r in rows):
        res['notes'].append('tempo 기록 없음 — 빠르기 확인 안 함')
    ds = Counter(r['date'] for r in rows if r['date'])
    res['dates'] = dict(sorted(ds.items()))
    nodate = sum(1 for r in rows if not r['date'])
    if nodate: res['notes'].append(f'녹음 날짜 기록 없음 {nodate}/{len(rows)}줄 — 한 날 녹음 여부 확인 안 함')
    main_day = ds.most_common(1)[0][0] if ds else None
    retake_ok = len(ds) == 2 and min(ds.values()) / max(1, sum(ds.values())) <= 0.20   # 10/10 순돌이: lfretake 다시 받기(둘째 날 20% 이하)는 허용, 편 단위 앞뒤 차·IQR 관문은 그대로(lfvoice.check와 같은 기준)
    for r in rows:
        why = []
        f = r['f0']
        if res['median_f0']:
            if not isinstance(f, (int, float)) or f <= 0: why.append('f0 없음')
            elif abs(f / res['median_f0'] - 1) > F0_TOL: why.append(f'음높이 {f:g}Hz(중앙 {res["median_f0"]:g} ±25% = {res["lo"]:g}~{res["hi"]:g} 밖)')
        t = r['tempo']
        if t is not None and abs(float(t) - 1.0) > 1e-9: why.append(f'빠르기 {t:g}배(1.0 고정)')
        if not retake_ok and len(ds) >= 2 and r['date'] and r['date'] != main_day: why.append(f'녹음 날짜 {r["date"]}(주 녹음일 {main_day})')
        if why: res['redo'].append({**r, 'why': why})
    ep_bad = []
    seq = [r['f0'] for r in rows if isinstance(r['f0'], (int, float)) and r['f0'] > 0]
    if len(seq) >= 8:
        h = len(seq) // 2; a, b = sum(seq[:h]) / h, sum(seq[h:]) / (len(seq) - h)
        drift = b / a - 1; q = sorted(seq); iqr = (q[3 * len(q) // 4] - q[len(q) // 4]) / res['median_f0']
        res.update(drift=round(drift, 3), iqr=round(iqr, 3))
        if abs(drift) > DRIFT_MAX: ep_bad.append(f'앞·뒤 절반 음높이 차 {drift:+.1%}(기준 ±{DRIFT_MAX:.0%}) — 뒤쪽이 다른 목소리처럼 들림')
        if iqr > IQR_MAX: ep_bad.append(f'음높이 퍼짐 IQR/중앙 {iqr:.2f}(기준 ≤{IQR_MAX})')
    res['episode'] = ep_bad
    ok = not res['redo'] and not ep_bad and (len(ds) < 2 or retake_ok) and bool(fs) and not all(r['tempo'] is None for r in rows)
    return ok, res

def print_voice(res, ok, where=''):
    print(f"목소리 관문{(' · ' + where) if where else ''}: 줄 {res['lines']} · f0 중앙 " + (f"{res['median_f0']}Hz" if res['median_f0'] else '기록 없음')
          + (f" (허용 {res['lo']}~{res['hi']})" if res['lo'] else '') + f" · 녹음 날짜 {res['dates'] or '기록 없음'}")
    for n in res['notes']: print('  확인 안 함 ·' if '확인 안 함' in n else '  ·', n)
    if len(res['dates']) >= 2: print(f"  녹음이 {len(res['dates'])}날로 나뉨 — 규칙 ③ 한 편은 한 회차(같은 날)에 녹음, 이어 붙이기 금지")
    if res['redo']:
        print(f"  다시 녹음할 줄 {len(res['redo'])}개:")
        for r in res['redo']: print(f"    {r['at']} | {r['text'][:30]} | " + ' · '.join(r['why']))
    print('  통과' if ok else '  거부')


# ───────────────────────── 관문 묶음 · 렌더 ─────────────────────────
def gates(ep, vid=VID, write_text=True):
    """(ok, [줄]) — 화면 글자를 다시 뽑아(write_text) 편집 통과 해시와 대조, 누적 구간, 목소리."""
    ok, out = True, []
    pp = props_path(ep, vid)
    if not os.path.exists(pp): return False, [f'props 없음: {pp}']
    props = json.load(open(pp, encoding='utf-8'))
    if write_text: write_screen_text(ep, vid, props)
    e_ok, why = edit_check(ep); ok &= e_ok
    out.append(('통과 · ' if e_ok else '거부 · ') + why)
    if not e_ok: out.append(f'  firemap-editor가 {os.path.join(ep, "screen_text.txt")}를 보고: py -3.12 work/lfrender.py stamp {ep} firemap-editor "<무엇을 봤는지>"')
    c_ok, msgs = cumulative_check(props); ok &= c_ok
    out += msgs or ['통과 · 누적 구간 막대 없음']
    vp = os.path.join(ep, 'voice.json')
    if os.path.exists(vp):
        v_ok, res = voice_check(json.load(open(vp, encoding='utf-8'))); ok &= v_ok
        out.append(('통과' if v_ok else '거부') + f" · 목소리 한결같음(다시 녹음 {len(res['redo'])}줄 — lfrender.py voice {ep} 로 목록)")
        out += ['  ' + n for n in res['notes']]
    else:
        ok = False; out.append('거부 · voice.json 없음')
    return ok, out

def render(ep, extra=(), vid=VID):
    ok, out = gates(ep, vid)
    print(*out, sep='\n')
    if not ok:
        print('렌더하지 않는다 — 위 거부를 고친 뒤 다시'); return 1
    cid = comp_id(ep); low = cid.lower()
    cmd = ['npx', 'remotion', 'render', 'src/index.ts', cid, f'out/{low}.mp4', '--pixel-format=yuv420p', f'--props={low}.json', *extra]
    print('렌더:', ' '.join(cmd))
    return subprocess.call(cmd, cwd=vid, shell=(os.name == 'nt'))


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 2: print(open(__file__, encoding='utf-8').read().split('import ')[0]); sys.exit(2)
    cmd, ep = a[0], os.path.abspath(a[1])
    if cmd == 'text': print('뽑음', write_screen_text(ep)); sys.exit(0)
    if cmd == 'stamp' and len(a) >= 3:
        if not os.path.exists(os.path.join(ep, 'screen_text.txt')): write_screen_text(ep)
        print('찍음', stamp(ep, a[2], ' '.join(a[3:]))); sys.exit(0)
    if cmd == 'voice':
        vp = ep if ep.endswith('.json') else os.path.join(ep, 'voice.json')
        ok, res = voice_check(json.load(open(vp, encoding='utf-8'))); print_voice(res, ok, os.path.basename(os.path.dirname(vp)))
        sys.exit(0 if ok else 1)
    if cmd == 'check':
        ok, out = gates(ep); print(*out, sep='\n'); print('관문 통과' if ok else '관문 거부'); sys.exit(0 if ok else 1)
    if cmd == 'render': sys.exit(render(ep, a[2:]))
    print('모르는 명령:', cmd); sys.exit(2)
