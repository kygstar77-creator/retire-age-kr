import re
s=open('da_thresh/onesec/ff.py',encoding='utf-8').read()
s=s.replace("COMP=['-YuYOLaMYcM','HXqB-GiDwtY','KfQASIS4G0A','UINdvu1cqkc','yF8xbi4CwbU']","COMP=['4v8vukzNU24','gyN5SUF534M','q0v3BKT0LAA','-COF66p7bu0','milGZdmrIh8']")
s=s.replace("'da_thresh.mp4'","'bp_thresh.mp4'").replace('da_thresh 첫 프레임','bp_thresh 첫 프레임').replace('건강보험 피부양자 소득','기초연금 기준·소득인정액')
L=s.split('\n')
i=[k for k,l in enumerate(L) if '영상 제목:' in l][0]
NEW=" '영상 제목: \"기초연금 기준 월 247만원 이하 vs 초과, 단독가구 소득인정액 #shorts\"\\n영상 내용: 큰 상자 두 개(247만원 이하면 받아요 / 247만원 넘으면 못 받아요, 소득인정액 월)와 3줄 설명. 복지부 보도자료 기준.\\n'"
L[i]=NEW
open('bp_thresh/onesec/ff.py','w',encoding='utf-8').write('\n'.join(L))
