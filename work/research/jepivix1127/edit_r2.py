# 2차 이해 시험(41·57·66세 새 심사관 3명) 반영 — firemap-write 11/26
import os, re
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.join(here, 'pkg'))
def ed(p, a, b):
    s = open(p, encoding='utf-8').read(); assert a in s, (p, a); open(p, 'w', encoding='utf-8').write(s.replace(a, b))
ed('c03.txt', "VIX 20 이상이던 29번 중 5번은 전체 중간값인 7.9%보다 낮았어요.", "VIX 20 이상이던 29번 중 5번은 77번 전체의 중간값인 7.9%보다도 낮았어요.")
ed('c05.txt', "· 12월엔 배당락이 두 번 있었어요.", "· 12월엔 배당락일(이날부터 사면 그달 분배금을 못 받는 날)이 두 번 있었어요.")
ed('c04.txt', "분배금을 다시 넣으면 결과가 커져요.", "분배금을 현금으로 쓰지 않고 다시 넣으면 결과가 커져요.")
m = os.path.join(here, 'mkimg.py'); s = open(m, encoding='utf-8').read()
s = s.replace("분배 77번의 묶음별 가운데 값", "분배 77번의 묶음별 중간값"); open(m, 'w', encoding='utf-8').write(s)
print('ok')
