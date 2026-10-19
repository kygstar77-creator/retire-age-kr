# 받은 표본 전부 재기(이미 잰 것은 건너뜀). py -3.12 runall.py <media> <worker번호 0|1> <workers 2>
import sys, os, json, subprocess, glob, time
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]; k, K = int(sys.argv[2]), int(sys.argv[3])
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
jobs = [('short', v) for _, v in S['short']] + [('long', v) for _, v in S['long']]
extra = json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'ours.json')) else []
jobs += [(x['kind'], x['id'], x['path']) for x in extra]
env = dict(os.environ, PYTHONIOENCODING='utf-8', VOICENAT_CACHE=os.path.join(M, 'wcache'))
if len(sys.argv) > 4 and sys.argv[4] == "rev": jobs = jobs[::-1]
if len(sys.argv) > 4 and sys.argv[4] == "long": jobs = [j for j in jobs if j[0] == "long"]
for j, job in enumerate(jobs):
    if j % K != k: continue
    kind, vid = job[0], job[1]
    if os.path.exists(os.path.join(HERE, 'res', f'{kind}_{vid}.json')): continue
    lk = os.path.join(HERE, 'res', f'{kind}_{vid}.lock')   # 다른 작업자가 재는 중
    if os.path.exists(lk) and time.time() - os.path.getmtime(lk) < 3600: continue
    if len(job) == 3: args = [job[2]]
    else:
        v, a = os.path.join(M, f'{kind}_{vid}.v.mp4'), os.path.join(M, f'{kind}_{vid}.a.m4a')
        if not (os.path.exists(v) and os.path.exists(a)): print('not yet', vid, flush=True); continue
        args = [v, a]
    open(lk, 'w').write('x')
    r = subprocess.run(['py', '-3.12', os.path.join(HERE, 'measure.py'), kind, *args, vid, os.path.join(HERE, 'res')], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    os.remove(lk)
    print((r.stdout.strip().splitlines() or ['?'])[-1], r.stderr[-400:] if r.returncode else '', flush=True)
