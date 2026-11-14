"""전날(또는 지정 날짜, KST) 작업별 출력 토큰 표. ~/.claude/projects/*/*.jsonl의 assistant output_tokens 합(메시지 id 중복 제거).
작업 이름 = 첫 queue/user 내용의 <scheduled-task name="...">. 결과물 수 = 그날 커밋 중 메시지에 작업 이름이 든 수.
사용: py -3.12 work/tokenday.py [YYYY-MM-DD]"""
import json, glob, os, re, sys, subprocess, datetime as dt
KST = dt.timezone(dt.timedelta(hours=9))
day = sys.argv[1] if len(sys.argv) > 1 else (dt.datetime.now(KST).date() - dt.timedelta(days=1)).isoformat()
rx = re.compile(r"<scheduled-task name=.?.([A-Za-z0-9_.-]+)")
agg = {}
for f in glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')):
    if os.path.getmtime(f) < dt.datetime.fromisoformat(day).timestamp() - 86400: continue
    name = start = None; seen = set(); out = 0
    with open(f, encoding='utf-8', errors='ignore') as fh:
        for line in fh:
            try: o = json.loads(line)
            except Exception: continue
            ts = o.get('timestamp')
            if start is None and ts: start = dt.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(KST)
            if name is None:
                m = rx.search(line[:4000])
                if m: name = m.group(1)
            msg = o.get('message') if isinstance(o.get('message'), dict) else None
            if o.get('type') == 'assistant' and msg and msg.get('usage'):
                k = msg.get('id') or id(o)
                if k in seen: continue
                seen.add(k); out += msg['usage'].get('output_tokens', 0) or 0
    if start is None or start.date().isoformat() != day: continue
    name = name or '(수동·기타)'
    a = agg.setdefault(name, [0, 0]); a[0] += 1; a[1] += out
log = subprocess.run(['git', 'log', '--since', day + 'T00:00:00+09:00', '--until', day + 'T23:59:59+09:00', '--format=%s'],
                     capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout
ALIAS = {'firemap-video-producer': ['pd'], 'firemap-youtube-loop': ['yt-loop', 'yt'], 'firemap-visual-designer': ['visual'],
         'firemap-write': ['write'], 'firemap-write-b': ['write-b', 'cafe: write-b'], 'firemap-dispatch': ['dispatch'],
         'firemap-publish-watchdog': ['watchdog'], 'firemap-meeting': ['meeting'], 'firemap-report': ['report']}
def ncommit(n):
    keys = ALIAS.get(n, [n.replace('firemap-', '')])
    c = 0
    for l in log.splitlines():
        h = re.split(r'[:\s]', l.strip(), 1)[0]
        if any(l.startswith(k) and (h == k or l.startswith(k + ' ') or l.startswith(k + ':')) for k in keys) or (n not in ALIAS and keys[0] in l): c += 1
    return c
tot = sum(v[1] for v in agg.values()) or 1
rows = sorted(agg.items(), key=lambda kv: -kv[1][1])
print(f'### {day} 작업별 출력 토큰 (세션 jsonl 합, 측정 {dt.datetime.now(KST):%m-%d %H:%M})')
print('| 작업 | 회차 | 출력 토큰 | 비중 | 커밋(결과물) |\n|---|---|---|---|---|')
for n, (c, t) in rows[:5]:
    print(f'| {n} | {c} | {t:,} | {t*100//tot}% | {ncommit(n)} |')
rest = rows[5:]
print(f'| 나머지 {len(rest)}종 | {sum(v[0] for _, v in rest)} | {sum(v[1] for _, v in rest):,} | {sum(v[1] for _, v in rest)*100//tot}% | - |')
print(f'| 합계 | {sum(v[0] for v in agg.values())} | {tot:,} | | 커밋 {len(log.splitlines())} |')
