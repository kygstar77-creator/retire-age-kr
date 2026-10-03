"""착수→완료 회차 길이와 '편 첫 기록→관문 통과' 경과 시간 — rules-evidence-1003 일회성 도구.

A) today.md의 git 역사(git log -p)에서 더해진 줄 중 '착수: firemap-<담당> HH:MM'과
   '완료: firemap-<담당> HH:MM'을 모아, 같은 담당의 착수 뒤 6시간 안 첫 완료와 짝지어 회차 길이를 잰다.
   날짜는 그 줄을 더한 커밋 날짜(KST)로 본다(자정 넘김은 +1일로 보정).
B) slots.json 칸의 편 이름이 커밋 메시지나 경로에 처음 나온 시각 → gates_ok 까지 경과 시간.
사용: TZ=Asia/Seoul python work_durations.py
"""
import re, subprocess, datetime, statistics, collections, json

ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
ROLES = ('firemap-write', 'firemap-shorts', 'firemap-video-producer')


def git(*a):
    return subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout


def sessions():
    out = git('log', '-p', '--reverse', '--since=2026-09-28', '--format=@@C %ad', '--date=format-local:%Y-%m-%d',
              '--', 'work/research/meeting/today.md')
    day, ev, seen = None, [], set()
    pat = re.compile(r'(착수|완료)[^:：]{0,12}[:：]\s*(firemap-[a-z-]+)\s+(\d{1,2}):(\d{2})')
    for ln in out.splitlines():
        if ln.startswith('@@C '):
            day = ln[4:].strip(); continue
        if not ln.startswith('+') or ln.startswith('+++'):
            continue
        m = pat.search(ln)
        if not m or m.group(2) not in ROLES:
            continue
        key = (m.group(1), m.group(2), m.group(3), m.group(4), ln[:80])
        if key in seen:
            continue
        seen.add(key)
        t = datetime.datetime.strptime(f'{day} {int(m.group(3)):02d}:{m.group(4)}', '%Y-%m-%d %H:%M')
        ev.append((m.group(2), m.group(1), t))
    res = collections.defaultdict(list)
    for role in ROLES:
        st = sorted(t for r, k, t in ev if r == role and k == '착수')
        fin = sorted(t for r, k, t in ev if r == role and k == '완료')
        for s in st:
            nxt = [f for f in fin if s <= f <= s + datetime.timedelta(hours=6)]
            if nxt:
                res[role].append((nxt[0] - s).total_seconds() / 60)
    return res


def first_mention(item):
    a = git('log', '--reverse', '--all', f'--grep={item}', '--format=%ad', '--date=format-local:%Y-%m-%d %H:%M').split('\n')[0].strip()
    b = git('log', '--reverse', '--all', '--format=%ad', '--date=format-local:%Y-%m-%d %H:%M', '--', f'*{item}*').split('\n')[0].strip()
    c = [x for x in (a, b) if x]
    return datetime.datetime.strptime(min(c), '%Y-%m-%d %H:%M') if c else None


def main():
    s = sessions()
    print('== A) 회차 길이(착수→같은 담당 첫 완료, 분)')
    for r, xs in s.items():
        if xs:
            print(f'{r}: n={len(xs)} 중앙 {statistics.median(xs):.0f}분 · 최소 {min(xs):.0f} · 최대 {max(xs):.0f} · 90% {sorted(xs)[int(len(xs) * 0.9) - 1 if len(xs) > 1 else 0]:.0f}')
    print('\n== B) 편 첫 기록 → gates_ok 경과(시간)')
    d = json.loads(git('show', 'HEAD:work/research/slots.json'))
    per = collections.defaultdict(list)
    hist = {}
    for h in git('log', '--format=%H', '--', 'work/research/slots.json').split():
        try:
            for x in json.loads(git('show', f'{h}:work/research/slots.json')).get('slots', []):
                if x.get('item') and x.get('gates_ok'):
                    hist.setdefault((x['at'], x['kind']), (x['item'], x['gates_ok']))
        except Exception:
            pass
    for (at, kind), (item, g) in sorted(hist.items()):
        f = first_mention(item)
        gt = datetime.datetime.strptime(g[:16], '%Y-%m-%d %H:%M')
        if f:
            h = (gt - f).total_seconds() / 3600
            per[kind].append(h)
            print(f'{at}\t{kind}\t{item}\t첫 기록 {f:%m-%d %H:%M}\tgates_ok {g}\t{h:.1f}h')
    for k, xs in per.items():
        print(f'[{k}] n={len(xs)} 중앙 {statistics.median(xs):.1f}h 최소 {min(xs):.1f} 최대 {max(xs):.1f}')


if __name__ == '__main__':
    main()
