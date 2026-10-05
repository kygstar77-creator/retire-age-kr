# 가정: 월지급금 고정(HF 월지급금 예시 65세 4억 1,011천원, 2026.3.1 기준), 이자율 = CD 3.21% + 1.1%p, 월 복리, 초기보증료는 첫 지급일에 잔액에 가산
def run(years, init, annual_fee, pay=1_011_000, house=400_000_000, rate=0.0321+0.011):
    bal=house*init; paid=0; fee_tot=house*init; int_tot=0
    for m in range(years*12):
        bal+=pay; paid+=pay
        f=bal*annual_fee/12; i=bal*rate/12
        bal+=f+i; fee_tot+=f; int_tot+=i
    return dict(years=years,pay_total=paid,fee=fee_tot,interest=int_tot,balance=bal)
for y in (10,20):
    for name,a,b in (("개편후",0.01,0.0095),("개편전",0.015,0.0075)):
        r=run(y,a,b); print(y,name,{k:round(v/1e4) if k!='years' else v for k,v in r.items()})
