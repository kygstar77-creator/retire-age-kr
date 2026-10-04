# 기초연금 부부감액 계산 — 기초연금법 제8조①②, 시행령 제11조②⑤, 2026 기준연금액 349,700·부부 선정기준액 3,952,000
BASE=349700; SEL2=3952000
def couple(inc):
    each=BASE-BASE*20//100           # 법 제8조① 각각 20% 감액
    tot=each*2
    if inc+tot>SEL2:                  # 시행령 제11조②
        gap=SEL2-inc
        tot=BASE*20//100 if gap<=BASE*20//100 else gap
    return each,tot
if __name__=='__main__':
    print('each',couple(0)[0],'couple',couple(0)[1],'cut/mo',BASE*2-couple(0)[1],'cut/yr',(BASE*2-couple(0)[1])*12,'threshold',SEL2-couple(0)[1])
    for i in (3000000,3392480,3500000,3700000,3850000,3900000,3952000): print(i,couple(i)[1])
