# H-6 쇼츠(h6s_before 12/1·h6s_gangnam 12/3) 올리기 전 확인(11/28 PD): 강남구 매매 2026.09~11 다시 받아 raw/rt1128/에(나머지 달은 rt1125 사본)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','..','..','..'))
import rtmolit
OUT=os.path.join(HERE,'raw','rt1128')
for m in ['202512','202609','202610','202611']:
    rows=rtmolit.fetch('trade','11680',m)
    old=json.load(open(os.path.join(HERE,'raw','rt1125',f'11680_{m}_trade.json'),encoding='utf-8'))
    json.dump(rows,open(os.path.join(OUT,f'11680_{m}_trade.json'),'w',encoding='utf-8'),ensure_ascii=False)
    print(m,'trade',len(old),'->',len(rows))
