import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('video/detf1.json',encoding='utf-8'))
t=open('research/longform/ep/D-ETF-1/shot_plan.md',encoding='utf-8').read().split('# 장면 계획',1)[1]
rows=[[c.strip() for c in l.strip().strip('|').split('|')] for l in t.splitlines() if l.startswith('|') and not re.match(r'\|\s*-',l)][1:]
norm=lambda s:re.sub(r'[\s,.]+','',s)
import difflib
def best(key):
    sc=[(difflib.SequenceMatcher(None,key,norm(l['text'])[:len(key)]).ratio(),j,k) for j,s_ in enumerate(d['scenes']) for k,l in enumerate(s_['lines'])]
    return max(sc)
for i,r in enumerate(rows,1):
    key=norm(r[1])[:14]; hit=[]
    for j,s in enumerate(d['scenes']):
        for k,l in enumerate(s.get('lines',[])):
            if key in norm(l['text']): hit.append((j,k))
    sc=[ (j,d['scenes'][j]['kind'], d['scenes'][j].get('data',{}).get('src') or d['scenes'][j].get('data',{}).get('bg') ) for j,k in hit]
    print(f'r{i:02d}', r[1][:24], '|', r[5], '=>', sc)

# frames
starts=[];f=0
for s in d['scenes']: starts.append(f); f+=s['frames']
out=[];M={}
used=set()
for i,r in enumerate(rows,1):
    key=norm(r[1])[:20]
    sc,j,k=best(key); assert sc>0.8,(r[1],sc); s=d['scenes'][j]
    if (j,k) in used and k+1<len(s['lines']): k+=1
    used.add((j,k))
    fr=starts[j]+sum(l['frames'] for l in s['lines'][:k])+int(s['lines'][k]['frames']*0.85)
    out.append([f'r{i:02d}',fr]); M[f'r{i:02d}']={'scene':j,'line':k,'kind':s['kind'],'src':s.get('data',{}).get('src'),'data':s.get('data')}
json.dump(out,open(sys.argv[1]+'/frames.json','w'))
json.dump(M,open(sys.argv[1]+'/map.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)

# 판(broll 아닌 장면)은 그 줄이 끝나기 10프레임 전(마지막 줄이면 장면 끝 20프레임 전) — 그 줄까지 열린 상태(10/27 visual 2차: 장면 끝으로 잡으니 HDV 줄에 SPYD 강조가 찍힘)
# 뒤 장면(b): 대본 줄의 뜻을 바로 다음 장면이 받는 줄 — 물음 카드 뒤 답 판(DIVO 0.953달러·커버드콜 짜임 등). 우리 쪽 그림 두 장.
EXTRA = {'r05': 7, 'r08': 12, 'r10': 16, 'r12': 20, 'r13': 24, 'r18': 33, 'r26': 42, 'r28': 48, 'r30': 59, 'r33': 62}
def endf(j, k):
    s = d['scenes'][j]
    return starts[j] + (s['frames'] - 20 if k == len(s['lines']) - 1 else sum(l['frames'] for l in s['lines'][:k + 1]) - 10)
out2 = []
for (name, fr) in out:
    m = M[name]; j = m['scene']
    if m['kind'] != 'broll': fr = endf(j, m['line'])
    out2.append([name, fr])
    if name in EXTRA:
        jb = EXTRA[name]; out2.append([name + 'b', starts[jb] + d['scenes'][jb]['frames'] - 20]); M[name]['extra'] = jb
json.dump(out2, open(sys.argv[1] + '/frames.json', 'w'))
json.dump(M, open(sys.argv[1] + '/map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
