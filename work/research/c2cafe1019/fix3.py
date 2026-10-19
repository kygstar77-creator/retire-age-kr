import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pkg'))
p='c04.txt';a='이대로 내년 1월을 맞으면, 올해 쓸 돈을 빼고 나니 처음 넣은 3억보다 700만원쯤 적습니다.';t=open(p,encoding='utf-8').read();assert a in t
open(p,'w',encoding='utf-8').write(t.replace(a,'이 값으로 내년 1월을 맞으면, 통장이 처음 넣은 3억보다 700만원쯤 적습니다.'))
