# 자막(vtt) → 90초 토막 요약 + 설명란 시간표 (youtube-loop 2026-11-23)
import json, re, glob, os
d = {o['id']: o for o in json.load(open('raw/yt_search_1123.json', encoding='utf-8'))}
out = []
for f in sorted(glob.glob('raw/subs/*.vtt')):
    vid = os.path.basename(f).split('.')[0]; o = d.get(vid, {})
    txt = open(f, encoding='utf-8').read(); segs = []; last = ''
    for m in re.finditer(r'(\d\d):(\d\d):(\d\d)\.\d+ --> [^\n]*\n(.*?)(?:\n\n|\Z)', txt, re.S):
        t = int(m[1])*3600+int(m[2])*60+int(m[3])
        line = re.sub(r'<[^>]+>', '', m[4]).strip().split('\n')[-1].strip()
        if line and line != last: segs.append((t, line)); last = line
    chap = re.findall(r'^\s*((?:\d+:)?\d{1,2}:\d\d)\s+(.+)$', o.get('desc', ''), re.M)
    out.append(f"\n## {vid} · {o.get('channel')} · {o.get('views')}회 · 배수 {o.get('ratio')} · {o.get('sec',0)//60}:{o.get('sec',0)%60:02d} · {o.get('date')}\n제목: {o.get('title')}")
    if chap: out.append('설명란 시간표: ' + ' / '.join(f'{a} {b[:40]}' for a, b in chap))
    buck = {}
    for t, l in segs: buck.setdefault(t // 90, []).append(l)
    for b in sorted(buck):
        s = ' '.join(buck[b]); out.append(f"{b*90//60}:{b*90%60:02d} {s[:170]}")
    ends = [l for t, l in segs if t >= o.get('sec', 0) - 30]
    out.append('끝 30초: ' + ' '.join(ends)[:300])
open('raw/digest.txt', 'w', encoding='utf-8').write('\n'.join(out))
print(len('\n'.join(out)))
