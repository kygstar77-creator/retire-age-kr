# 시각 관문(2026-10-02) — 실제 시계 12:52에 "완료 13:05"·상황판 13:06 같은 미래 시각이 3건 적혔다.
# today.md·decisions/log.md에 새로 들어간 줄의 HH:MM이 그 줄을 넣은 커밋 시각보다 5분 넘게 늦으면 잡는다.
#   py -3.12 work/timecheck.py            오늘 커밋 전부 검사(순찰용, 결과만 출력)
#   py -3.12 work/timecheck.py --mark     잡힌 줄 끝에 "[시각 확인: 커밋 HH:MM]"을 붙인다(today.md만)
#   py -3.12 work/timecheck.py staged     지금 스테이지된 변경을 현재 시각으로 검사(pre-commit 경고, 커밋은 막지 않음)
import os, re, sys, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FILES = ['work/research/meeting/today.md', 'work/research/decisions/log.md']
SLACK = 5  # 분
STAMP_HEAD = re.compile(r'^\s*-?\s*(?:착수|완료|진행|막힘|실패)\s*:\s*(?:[\w가-힣.-]+\s+)?(\d{1,2}):(\d{2})\b')
STAMP_TAIL = re.compile(r'\b(\d{1,2}):(\d{2})\s*(?:\([\w가-힣 .-]+\))?\s*$')
LOG_HEAD = re.compile(r'^(\d{4}-\d\d-\d\d) (\d{1,2}):(\d{2}) ·')
MARK = '[시각 확인'


def stamp(path, line):
    """줄이 스스로 적은 기록 시각. 내용 속 예정 시각(16:05 회차 등)은 보지 않는다."""
    if path.endswith('log.md'):
        m = LOG_HEAD.match(line)
        return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None
    if not re.match(r'^\s*-?\s*(?:착수|완료|진행|막힘|실패)\s*:', line): return None
    m = STAMP_HEAD.match(line) or STAMP_TAIL.search(line)
    return (None, int(m.group(1)), int(m.group(2))) if m else None


def late(path, line, at):
    s = stamp(path, line)
    if not s or MARK in line: return None
    d, h, mi = s
    if h > 23 or mi > 59: return None
    if d and d != at.strftime('%Y-%m-%d'): return None
    t = at.replace(hour=h, minute=mi, second=0, microsecond=0)
    gap = (t - at).total_seconds() / 60
    return gap if SLACK < gap < 12 * 60 else None  # 12시간 넘으면 전날 줄로 본다


def added(diff):
    return [l[1:] for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')]


def git(*a):
    return subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout


def check_staged():
    now = datetime.datetime.now(); hits = []
    for f in FILES:
        for l in added(git('diff', '--cached', '-U0', '--', f)):
            g = late(f, l, now)
            if g: hits.append((f, now, g, l))
    return hits


def check_today():
    hits = []
    since = datetime.datetime.now().strftime('%Y-%m-%d 00:00')
    for f in FILES:
        for c in git('log', f'--since={since}', '--format=%H %ci', '--', f).splitlines():
            h, ci = c.split(' ', 1)
            at = datetime.datetime.strptime(ci[:19], '%Y-%m-%d %H:%M:%S')
            for l in added(git('show', '-U0', '--format=', h, '--', f)):
                g = late(f, l, at)
                if g: hits.append((f, at, g, l))
    return hits


def mark(hits):
    p = os.path.join(ROOT, FILES[0]); s = open(p, encoding='utf-8').read(); n = 0
    for f, at, g, l in hits:
        if f != FILES[0] or l not in s or MARK in l: continue
        s = s.replace(l, l.rstrip() + f' {MARK}: 커밋 {at:%H:%M}]', 1); n += 1
    if n: open(p, 'w', encoding='utf-8').write(s)
    return n


if __name__ == '__main__':
    staged = 'staged' in sys.argv
    hits = check_staged() if staged else check_today()
    seen = set()
    for f, at, g, l in hits:
        if l in seen: continue
        seen.add(l)
        print(f'시각 확인 · {os.path.basename(f)} · 커밋 {at:%H:%M}보다 {int(g)}분 늦은 기록: {l.strip()[:110]}')
    if staged and hits:
        print("  → 시각은 그때 `date '+%H:%M'`로 찍은 값만 적는다(예정 시각 금지). 고쳐서 다시 add 하라.", file=sys.stderr)
    if '--mark' in sys.argv and not staged:
        print(f'표시 {mark(hits)}줄')
    if not hits: print('시각 확인 · 미래 시각 기록 없음')
