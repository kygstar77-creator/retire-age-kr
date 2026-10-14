import sys
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
sys.stdout.reconfigure(encoding='utf-8')
import toprank, re
for bid,no in [('jusikdev','224440349237'),('gimmg_ss','224441607966'),('thelastdot','224440759500'),('tempus10280','224441313080'),('heyuwl','224438386306')]:
    r=toprank.post(bid,no)
    if not r: print('fail',bid); continue
    open(f'comp_{bid}_{no}.txt','w',encoding='utf-8').write(r['title']+'\n'+'\n'.join(r['paras']))
    t='\n'.join(r['paras'])
    print(bid,r['chars'],r['imgs'],'| 52주:',t.count('52주'),'배당:',t.count('배당'),'분기:',t.count('분기'),'목표:',t.count('목표'),'코스피:',t.count('코스피'),'수정주가:',t.count('수정'),'유상증자:',t.count('유상'),'5년:',t.count('5년'))
