import sys
sys.path.insert(0,'work')
import lawtext as L
x=open('work/research/ubcalc1010/law_ub_act.xml',encoding='utf-8').read()
for jo,g in [(10,''),(10,'2'),(15,''),(43,''),(48,''),(58,'')]:
    a=L.pick(x,jo,g)
    print('=====',L.label(a) if a else (jo,'none')); print((a['글'] if a else '')[:2200])
import re
i=x.find('별표 1')
for m in re.finditer(r'<별표단위[^>]*>(.*?)</별표단위>',x,re.S):
    b=m.group(1)
    if '소정급여일수' in b[:400]:
        cd=re.search(r'<별표내용><!\[CDATA\[(.*?)\]\]>',b,re.S)
        print('=== 별표', (cd.group(1) if cd else b)[:2500])
