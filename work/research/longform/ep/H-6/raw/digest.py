import re, glob, os, json
out = open('digest.txt', 'w', encoding='utf-8')
for f in sorted(glob.glob('subs/*.vtt')):
    vid = os.path.basename(f).split('.')[0]
    t = open(f, encoding='utf-8').read()
    cues = re.findall(r'(\d\d):(\d\d):(\d\d)\.\d+ --> .*?\n(.*?)(?:\n\n|\Z)', t, re.S)
    seen = []; last = None
    for h, m, s, txt in cues:
        sec = int(h)*3600+int(m)*60+int(s)
        for line in re.sub(r'<[^>]+>', '', txt).splitlines():
            line = line.strip()
            if line and line != last: seen.append((sec, line)); last = line
    open(f'subs/{vid}.txt', 'w', encoding='utf-8').write('\n'.join(f'{s}\t{l}' for s, l in seen))
    out.write(f'\n===== {vid}\n')
    buck = {}
    for s, l in seen: buck.setdefault(s // 90, []).append(l)
    for k in sorted(buck):
        txt = ' '.join(buck[k])
        out.write(f'[{k*90//60}:{k*90%60:02d}] {txt[:330]}\n')
