# H-6 올리기 전 확인(11/25): 강남구 매매·전월세 2025.10~2026.11 다시 받아 raw/rt1125/ 에 저장(공유 research/rt는 안 건드림)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','..','..','..'))
import rtmolit
OUT=os.path.join(HERE,'raw','rt1125')
MS=['202510','202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610','202611']
for m in MS:
    for k in ('trade','rent'):
        rows=rtmolit.fetch(k,'11680',m)
        json.dump(rows,open(os.path.join(OUT,f'11680_{m}_{k}.json'),'w',encoding='utf-8'),ensure_ascii=False)
        print(m,k,len(rows))
