import os; os.chdir(os.path.dirname(os.path.abspath(__file__))+'/pkg')
def rep(p,a,b):
    s=open(p,encoding='utf-8').read()
    if a not in s: print('없음',p,a[:30])
    open(p,'w',encoding='utf-8').write(s.replace(a,b))
rep('c02.txt',"전부를 넣습니다(국민건강보험법 시행규칙 제44조).","전부를 넣습니다.")
rep('c03.txt',"금융소득이 없어도 건보료가 월 6만 1,000원입니다.","금융소득이 없어도 건보료가 월 6만 1,000원 나와요.")
rep('c01.txt',"보험료율 7.19%를 곱해요.","보험료율 7.19%를 곱합니다.")
rep('c04.txt',"계산하지 않았어요.","계산하지 않았습니다.")
