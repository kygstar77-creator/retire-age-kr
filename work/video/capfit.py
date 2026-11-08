# 출처 위 작은 줄(cap)·출처(source)가 TallyFrame 한 줄에 드는지 렌더 전에 잰다 (2026-11-08 motion)
#   py -3.12 work/video/capfit.py <props.json> [...]
# TallyFrame.capLineSize·srcSize와 같은 어림(한글 1em·공백 0.3em·그 밖 0.56em, 폭 1280px, 하한 13px).
# 13px로도 넘치는 cap은 화면에서 두 줄로 접혀 작은 글자가 출처 포함 3줄이 된다(규칙 2줄) → 대본·props에서 줄인다. 넘친 줄이 있으면 종료 코드 1.
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
W, MIN = 1280, 13
def units(t, sp=0.3): return sum(1 if re.match('[ㄱ-힝]', c) else (sp if c.isspace() else 0.56) for c in t)
def walk(x, out, key):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == key and isinstance(v, str): out.append(v)
            walk(v, out, key)
    elif isinstance(x, list):
        for v in x: walk(v, out, key)
bad = 0
for f in sys.argv[1:]:
    d = json.load(open(f, encoding='utf-8')); caps, srcs = [], []
    walk(d, caps, 'cap'); walk(d, srcs, 'source')
    over = sorted({c for c in caps if units(c) * MIN > W}, key=units, reverse=True)
    sover = sorted({s for s in srcs if units('출처 ' + s, 0.56) * MIN > W}, key=len, reverse=True)
    print(f'{f}: cap {len(caps)}줄 · 13px로도 넘침 {len(over)} · 출처 넘침 {len(sover)}')
    for c in over: print(f'  cap {units(c):.0f}칸(한 줄 {W // MIN}칸까지): {c}')
    for s in sover: print(f'  출처: {s}')
    bad += len(over) + len(sover)
sys.exit(1 if bad else 0)
