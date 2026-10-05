import sys
sys.path.insert(0,'../irpwd1006')
exec(open('../irpwd1006/calc.py',encoding='utf-8').read().split('# irpwd1006')[0])
def show(label,pay,y):
    d1,conv,base,t,tot=tax(pay,y)
    print(f"{label}: 퇴직금 {pay/1e4:,.0f}만 근속 {y}년 근속연수공제 {d1/1e4:,.0f} 환산급여 {conv/1e4:,.0f} 과표 {base/1e4:,.0f} 소득세 {t/1e4:,.1f} 지방포함 {tot/1e4:,.1f}")
    return tot
a=show("A 30년 한 번",15000e4,30)
b1=show("B1 15년 중간정산",7500e4,15)
b2=show("B2 퇴직 15년",7500e4,15)
print(f"B 합 {(b1+b2)/1e4:,.1f} 차이 {(b1+b2-a)/1e4:,.1f}")
c=[show(f"C{i}",5000e4,10) for i in range(3)]
print(f"C 합 {sum(c)/1e4:,.1f} 차이 {(sum(c)-a)/1e4:,.1f}")
print("실효 A",a/15000e4*100,"B",(b1+b2)/15000e4*100)
