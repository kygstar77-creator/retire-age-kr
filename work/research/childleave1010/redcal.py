import sys,os
sys.stdout.reconfigure(encoding='utf-8')
src=open('judge_run.py',encoding='utf-8').read().split("V=os.path.join")[0]
exec(src)
P='당신은 레드팀입니다. 칭찬 말고 감점부터 하세요. '+prompt('../gongjae1002/pkg')
for i in (1,2):
    t=ask(P,'../visual/cafe-covers-1002/board_gongjae1002.png'); print(t[:60].replace('\n',' '))
