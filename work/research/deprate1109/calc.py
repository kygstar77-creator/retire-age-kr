import json,sys
sys.stdout.reconfigure(encoding='utf-8')
now=json.load(open('deprate1109/raw/finlife_deposit_1109.json',encoding='utf-8'))
bank=now['020000']; sb=now['030300']
def load(p):
    d=json.load(open(p,encoding='utf-8'))
    if isinstance(d,dict):
        for k in ('020000','bank','은행'):
            if k in d: return d[k]
        return sum([v for v in d.values() if isinstance(v,list)],[])
    return d
old=load('bokdep1020/raw/finlife_deposit_1020.json')
print('공시월(지금):',sorted({r['공시월'] for r in bank}), ' 10/20:',sorted({r.get('공시월') for r in old}))
def key(r): return (r['은행'],r['상품'],str(r['기간']),r.get('금리유형'))
om={key(r):r for r in old}
b12=[r for r in bank if str(r['기간'])=='12']
print('은행 12개월 줄',len(b12))
print('\n== 은행 12개월 기본금리 상위 ==')
for r in sorted(b12,key=lambda r:-(r['금리'] or 0))[:12]: print(r['은행'],r['상품'],r['금리유형'],r['금리'],r['최고금리'],'| 10/20:',(om.get(key(r)) or {}).get('금리'))
big=['KB국민은행','국민은행','신한은행','하나은행','우리은행','농협은행주식회사','NH농협은행']
print('\n== 5대 은행 12개월 ==')
for r in b12:
    if any(b in r['은행'] for b in ['국민','신한','하나','우리','농협']): print(r['은행'],r['상품'],r['금리유형'],r['금리'],r['최고금리'],'| 10/20:',(om.get(key(r)) or {}).get('금리'),(om.get(key(r)) or {}).get('최고금리'))
ch=[(r,om[key(r)]) for r in b12 if key(r) in om and om[key(r)]['금리']!=r['금리']]
print('\n바뀐 줄',len(ch),'/ 대응',sum(1 for r in b12 if key(r) in om))
for r,o in ch: print(' ',r['은행'],r['상품'],o['금리'],'->',r['금리'],'| 최고',o['최고금리'],'->',r['최고금리'])
s12=[r for r in sb if str(r['기간'])=='12']
print('\n== 저축은행 12개월 기본 상위 ==', len(s12))
for r in sorted(s12,key=lambda r:-(r['금리'] or 0))[:8]: print(r['은행'],r['상품'],r['금리유형'],r['금리'],r['최고금리'])
import statistics
print('은행 12개월 기본 중앙',statistics.median([r['금리'] for r in b12]),'저축은행 중앙',statistics.median([r['금리'] for r in s12 if r['금리']]))
print('\n== 1억 1년 세후(15.4%) ==')
for r in [3.98,3.8,3.6,2.55,2.4,2.3,4.11]:
    pre=100_000_000*r/100; post=pre*(1-0.154); print(r, int(pre), int(post))
e=json.load(open('deprate1109/raw/ecos_1109.json',encoding='utf-8'))
print('ECOS 1~2년',e['dep_1to2y']); print('기준',e['base'][-4:]); print('국고3',e['ktb3'][-8:])
up=[(r,o) for r,o in ch if r['금리']>o['금리']]; dn=[(r,o) for r,o in ch if r['금리']<o['금리']]
print('오른 상품',len(up),'은행',sorted({r['은행'] for r,o in up})); print('내린 상품',len(dn),sorted({r['은행'] for r,o in dn}))
print('그대로',sum(1 for r in b12 if key(r) in om)-len(ch))
