import sys
sys.stdout.reconfigure(encoding='utf-8')
from calc import prem
f10=lambda x:int(x//10*10)
def imui(bosu):
    h=f10(bosu*0.0719); l=f10(h*0.9448/7.19); return h,l,h+l
def half(bosu):
    h=f10(bosu*0.0719/2)  # 월급명세서 시절 본인 몫(건보 절반)
    return h
if __name__=='__main__':
    for b in (2000000,3000000,4000000,5000000,6000000,8000000):
        h,l,t=imui(b); print(b,'건보',h,'장기',l,'합',t,'| 재직때 건보 본인몫',f10(b*0.0719/2),'장기 본인몫',f10(f10(b*0.0719/2)*0.9448/7.19) ,'합',f10(b*0.0719/2)+f10(f10(b*0.0719/2)*0.9448/7.19))
    for gp in (10000,20000,30000,40000,54000,70000,90000):
        a=prem(0,gp); print(gp,a['pts'],a['total'])
