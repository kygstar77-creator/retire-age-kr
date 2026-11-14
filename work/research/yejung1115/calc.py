# yejung1115 직접 계산 — raw/tasis_4-2-1_2025.txt · raw/tasis_4-2-4_2025.txt
import re,sys
sys.stdout.reconfigure(encoding='utf-8')
rows={}
for l in open('raw/tasis_4-2-4_2025.txt',encoding='utf-8'):
    p=l.strip().split('|')
    if len(p)==12 and re.search(r'\d',p[1]): rows[p[0]]=[int(x.replace(',','')) for x in p[1:]]
T=rows['합계']; N=T[0]
print('§1 전체', N, '환급',T[7],f'{T[7]/N:.1%}','납부',T[9],f'{T[9]/N:.1%}','둘다아님',N-T[7]-T[9],f'{(N-T[7]-T[9])/N:.1%}')
print('   1인당 환급(만원)',round(T[8]/T[7]*100,1),'1인당 납부(만원)',round(T[10]/T[9]*100,1))
print('   결정세액 0', rows['결정세액이 없는자'][0], f"{rows['결정세액이 없는자'][0]/N:.1%}", '그중 환급', rows['결정세액이 없는자'][7], '환급액(억)', rows['결정세액이 없는자'][8]/100)
# 구간 합치기
bands=['1천만 이하','1.5천만 이하','2천만 이하','3천만 이하','4천만 이하','4.5천만 이하','5천만 이하','6천만 이하','8천만 이하','1억 이하']
hi=['2억 이하','3억 이하','5억 이하','10억 이하','10억 초과']
def get(b):
    a=rows.get('있음 '+b,[0]*11); n=rows.get('없음 '+b,[0]*11)
    return [x+y for x,y in zip(a,n)]
groups={'3천만 이하':bands[:4],'3~5천만':bands[4:7],'5~8천만':bands[7:9],'8천만~1억':bands[9:10],'1억 초과':None}
print('§2 총급여 구간별')
for name,bs in groups.items():
    if bs: s=[sum(v) for v in zip(*[get(b) for b in bs])]
    else:
        s=[sum(v) for v in zip(*([rows['있음 '+b] for b in hi]+[rows['없음 1억 초과']]))]
    n=s[0]; print(f'  {name}: 인원 {n:,} · 환급 {s[7]/n:.1%} 1인당 {s[8]/s[7]*100:.1f}만 · 추가납부 {s[9]/n:.1%} 1인당 {s[10]/max(s[9],1)*100:.1f}만 · 납부액 몫 {s[10]/T[10]:.1%}')
print('§2b 세부 구간 추가납부 비율')
for b in bands+hi:
    s=get(b) if b in bands else rows['있음 '+b]
    if b in hi and b!='2억 이하': pass
    n=s[0]
    if n: print(f'  {b}: {n:,} 추가납부 {s[9]/n:.1%} 1인당 {s[10]/max(s[9],1)*100:.1f}만 환급 {s[7]/n:.1%}')
# 상위 10% (4-2-1)
top=dict(n=2107853,ref=1377281,refamt=4240096,pay=628607,payamt=3000675)
print('§3 급여총계 상위10%', f"환급 {top['ref']/top['n']:.1%} 추가납부 {top['pay']/top['n']:.1%} 1인당 납부 {top['payamt']/top['pay']*100:.1f}만 · 납부액 몫 {top['payamt']/T[10]:.1%}")
rn=N-top['n']; rp=T[9]-top['pay']; ra=T[10]-top['payamt']
print('   나머지 90%', f'추가납부 {rp/rn:.1%} 1인당 {ra/rp*100:.1f}만 환급 {(T[7]-top["ref"])/rn:.1%}')
# 2023 대비 (4-2-1)
print('§4 2023년 귀속', '전체 20,852,234 환급 14,899,752', f'{14899752/20852234:.1%}', '납부 3,544,553', f'{3544553/20852234:.1%}', '1인당 납부', round(4009059/3544553*100,1),'만 1인당 환급', round(12282734/14899752*100,1))
print('   납부 인원 증가', 3772299-3544553, f'{(3772299-3544553)/3544553:.1%}')
# §5 둘 다 아닌 사람(환급·납부 0) 중 결정세액 0·기납부 0
z=rows['결정세액이 없는자']; none=N-T[7]-T[9]
print('§5 둘다아님',none,'결정세액0이고 기납부0', z[0]-z[3], f'{(z[0]-z[3])/none:.1%}')
print('   1억 초과 인원 비율', f'{1545725/N:.1%}', '추가납부세액 합(조)', T[10]/1e6)
