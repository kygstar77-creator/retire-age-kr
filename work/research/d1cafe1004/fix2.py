import os; os.chdir(os.path.dirname(os.path.abspath(__file__))+'/pkg')
def rep(p,a,b):
    s=open(p,encoding='utf-8').read()
    if a not in s: print('없음',p,a[:30])
    open(p,'w',encoding='utf-8').write(s.replace(a,b))
rep('c02.txt',"1년 배당·이자가 2,000만원이면 월 13만 5,570원, 3,000만원이면 20만 3,370원입니다.","1년 배당·이자가 1,200만원이면 월 8만 1,340원이에요. 2,000만원이면 13만 5,570원까지 올라갑니다.")
rep('c04.txt'," 그 뒤 2028년 10월분까지 쓰고요. 국민연금은 전년도 연금을 1월분부터 12월분까지 씁니다."," 국민연금은 이와 달리 전년도에 받은 연금을 그해 1년 내내 씁니다.")
rep('c01.txt',"지역가입자가 돼요.","지역가입자가 됩니다.")
rep('c03.txt',"절반만 소득으로 넣어요.","절반만 소득으로 넣습니다.")
