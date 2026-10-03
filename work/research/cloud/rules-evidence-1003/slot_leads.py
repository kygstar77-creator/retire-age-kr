"""관문 기한(롱폼 24h·쇼츠 12h·카페 6h)을 실제 제작 시간과 대조 — rules-evidence-1003 일회성 도구.

1) git 역사 속 slots.json 모든 판을 읽어 칸마다 (발행 시각 at, 관문 통과 gates_ok)의 마지막 값을 모은다.
   실제 여유 = at - gates_ok. 기한(lead) 안에 통과했는지 센다.
2) 칸의 편(item) 이름이 저장소 경로에 처음 나타난 커밋 시각을 '착수'로 보고,
   gates_ok까지를 '제작 시간'으로 잰다(묶음 폴더가 처음 커밋된 시각 — 실제 착수보다 늦을 수 있다).
사용: python slot_leads.py   (저장소 안에서; 깊은 git 역사 필요)
"""
import json, subprocess, datetime, statistics, re, os, collections

ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
LEAD = {'long': 24, 'shorts': 12, 'cafe': 6}


def git(*a):
    return subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8').stdout


def ts(s):
    s = (s or '').strip()[:16]
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M')
    except ValueError:
        return None


def slots_history():
    seen = {}
    for h in git('log', '--reverse', '--format=%H', '--', 'work/research/slots.json').split():
        try:
            d = json.loads(git('show', f'{h}:work/research/slots.json'))
        except Exception:
            continue
        for s in d.get('slots', []):
            k = (s.get('at'), s.get('kind'))
            cur = seen.setdefault(k, {})
            for f in ('item', 'gates_ok', 'published', 'note'):
                if s.get(f):
                    cur[f] = s[f]
    return seen


def first_seen(item):
    """편 이름이 들어간 경로가 처음 커밋된 시각(KST)."""
    out = git('log', '--reverse', '--format=%ad', '--date=format-local:%Y-%m-%d %H:%M', '--all', '--', f'*{item}*')
    out = out.split('\n')[0].strip() if out else ''
    return ts(out)


def main():
    os.environ['TZ'] = 'Asia/Seoul'
    seen = slots_history()
    rows = []
    for (at, kind), v in sorted(seen.items(), key=lambda x: (x[0][0] or '')):
        a, g = ts(at), ts(v.get('gates_ok'))
        item = v.get('item')
        lead = (a - g).total_seconds() / 3600 if a and g else None
        st = first_seen(item) if item and re.match(r'^[\w-]+$', item) else None
        prod = (g - st).total_seconds() / 3600 if g and st else None
        rows.append((at, kind, item, v.get('gates_ok'), lead, st, prod))
    print('발행시각\t종류\t편\tgates_ok\t실제여유(h)\t기한(h)\t기한안\t첫커밋\t제작(h)')
    by = collections.defaultdict(lambda: {'lead': [], 'prod': [], 'ok': 0, 'n': 0, 'none': 0})
    for at, kind, item, g, lead, st, prod in rows:
        b = by[kind]
        if lead is None:
            b['none'] += 1
        else:
            b['n'] += 1; b['lead'].append(lead); b['ok'] += lead >= LEAD.get(kind, 0)
        if prod is not None and prod >= 0:
            b['prod'].append(prod)
        print(f'{at}\t{kind}\t{item}\t{g}\t{"" if lead is None else round(lead, 1)}\t{LEAD.get(kind)}\t'
              f'{"" if lead is None else ("O" if lead >= LEAD.get(kind, 0) else "X")}\t{st or ""}\t{"" if prod is None else round(prod, 1)}')
    print()
    for k, b in by.items():
        md = lambda xs: round(statistics.median(xs), 1) if xs else None
        print(f'[{k}] 기한 {LEAD.get(k)}h · gates_ok 있는 칸 {b["n"]} · 기한 안 통과 {b["ok"]} · gates_ok 없음 {b["none"]} · '
              f'실제 여유 중앙 {md(b["lead"])}h(최소 {round(min(b["lead"]), 1) if b["lead"] else None}·최대 {round(max(b["lead"]), 1) if b["lead"] else None}) · '
              f'제작(첫 커밋→gates_ok) 중앙 {md(b["prod"])}h n={len(b["prod"])}')


if __name__ == '__main__':
    main()
