import sys, urllib.request
sys.path.insert(0,'work')
import lawtext as L
def get(url, out):
    x=urllib.request.urlopen(url,timeout=90).read().decode('utf-8','replace')
    open(out,'w',encoding='utf-8').write(x); return x
base='http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&type=XML&MST=284449&efYd=20260918'
x=get(base,'work/research/ubcalc1010/law_ub_act.xml')
print(len(x))
for jo,g in [(14,''),(40,''),(41,''),(50,''),(45,''),(46,'')]:
    a=L.pick(x,jo,g)
    print('=====',L.label(a) if a else (jo,'none')); print(a['글'] if a else '')
