# 은행별 '평균' 칸(맨 끝 금리 칸)의 대출·기준·가산·가감조정금리 월별 — 은행연합회 가계대출금리 비교공시(신규취급액 기준) (firemap-write 11/18)
import json, sys, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('raw/hh_202604_202605_202606_202607_202608_202609_202610.json',encoding='utf-8'))
def parse(rows):
    res={}; bank=None
    for r in rows:
        if len(r)>=12 and r[1]=='대출금리':
            bank=r[0]; vals=r[2:12]; res[bank]={'대출금리':vals[-1],'점수':r[12] if len(r)>12 else ''}
        elif bank and r and r[0] in ('기준금리','가산금리','가감조정금리'):
            res[bank][r[0]]=r[10] if len(r)>10 else '-'
    return res
T={}
for k,rows in d.items():
    y,m,p=k.split('-'); T.setdefault(p,{})[y+m]=parse(rows)
names={'p1':'분할상환 주담대','p3':'일반신용대출'}
for p,bym in T.items():
    print('#',names[p]); months=sorted(bym)
    banks=[b for b in bym[months[-1]] if all(bym[mm].get(b,{}).get('가산금리','-') not in ('-','') for mm in ('202606','202610'))]
    print('은행', *months, sep='\t')
    for col in ('가산금리','대출금리','기준금리','가감조정금리'):
        print('['+col+']')
        for b in banks:
            print(b,*[bym[mm].get(b,{}).get(col,'-') for mm in months],sep='\t')
        med=[]
        for mm in months:
            v=[float(bym[mm][b][col]) for b in banks if bym[mm].get(b,{}).get(col,'-') not in ('-','')]
            med.append(round(st.median(v),2) if v else '-')
        print('중앙(%d곳)'%len(banks),*med,sep='\t')
    ch=[(round(float(bym['202610'][b]['가산금리'])-float(bym['202606'][b]['가산금리']),2),b) for b in banks]
    print('6월→10월 가산금리 변화', sorted(ch)); print('내린 곳',sum(1 for c,_ in ch if c<0),'/',len(ch))
