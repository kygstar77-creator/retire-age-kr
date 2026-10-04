# nhisrent1005 계산 — 근거: 시행령 별표4(grades.json, 원문 파싱), 제44조 7.19%·211.5원, 장기요양 0.9448%, 시행규칙 제44조③(소득월액 28만 이하→하한액÷7.19%)
import json,math,sys
sys.stdout.reconfigure(encoding='utf-8')
G=json.load(open('grades.json',encoding='utf-8'))
def parse(r):
    a=r.replace(',','')
    if '초과' in a and '~' not in a: return (int(a.split()[0]),10**12)
    if '~' not in a: return (0,int(a.split()[0]))
    lo,hi=a.split('~'); return (int(lo.split()[0]),int(hi.split()[0]))
B=[(k,)+parse(v[0])+(int(v[1].replace(',','')),) for k,v in ((int(k),v) for k,v in G.items())]
def pts(base_man):
    if base_man<=0: return 0,0
    for k,lo,hi,p in B:
        if lo<base_man<=hi: return k,p
f10=lambda x:int(x//10*10)
def prem(income_month,gwapyo_man):
    k,p=pts(gwapyo_man-10000)
    inc=0.0719*income_month if income_month>280000 else 20160
    prop=p*211.5
    h=f10(inc+prop); l=f10(h*0.9448/7.19)
    return dict(grade=k,pts=p,inc=inc,prop=prop,health=h,ltc=l,total=h+l)
if __name__=='__main__':
    for gp in (10000,15000,20000,30000,40000,54000,70000,90000):
        a=prem(0,gp); b=prem(750000,gp)
        print(gp,a['grade'],a['pts'],round(a['prop']),'| 소득없음',a['total'],'| 연금150',b['total'], '재산몫(연금)',b['total']-prem(750000,10000)['total'])
