import sys,os
sys.stdout.reconfigure(encoding='utf-8')
src=open('judge_run.py',encoding='utf-8').read().split("V=os.path.join")[0]
exec(src)
P='당신은 레드팀입니다. 칭찬 말고 감점부터 하세요. '+prompt('pkg')
t=ask(P,'covers_try/board_F.png'); print(t[:1200]); open('covers_try/redteam_F.md','w',encoding='utf-8').write(t)
