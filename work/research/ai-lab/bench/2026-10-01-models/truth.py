import re,sys,json
L=open('today_snap.md',encoding='utf-8').read().split('\n')
secs=[]
for i,l in enumerate(L,1):
    if l.startswith('## '): secs.append([i,l,[]])
    elif secs: secs[-1][2].append(l)
out=[]
for i,h,body in secs:
    if not re.match(r'## \[(지시|지시·긴급|요청)\]',h): continue
    done=any(re.match(r'^\s*-\s*완료(?! 기준)',b) for b in body)
    if not done: out.append(i)
print(json.dumps(out)); print(len(out), 'of', sum(1 for s in secs if re.match(r'## \[(지시|지시·긴급|요청)\]',s[1])))
