L=open('rejudge_ff.py',encoding='utf-8').read().split('\n')
# lines index 19.. : fix by joining until PC
j=[k for k,l in enumerate(L) if l.startswith('PC=')][0]
blk='\n'.join(L[19:j]).replace('\n','\n')
# blk now has literal \n; restore quoting
print(repr(blk)[:300])
L[19:j]=[blk]
open('rejudge_ff.py','w',encoding='utf-8').write('\n'.join(L))
