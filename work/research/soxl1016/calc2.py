import sys; sys.stdout.reconfigure(encoding='utf-8')
exec(open('calc.py',encoding='utf-8').read().split('days = sorted')[0])
days=sorted(set(L)&set(X))
import datetime as D
a,b=D.date(2026,10,5),D.date(2026,10,15)
print('10/5~10/15', f'SOXX {(X[b]/X[a]-1)*100:+.1f}% SOXL {(L[b]/L[a]-1)*100:+.1f}%')
s=max(d for d in days if d<=D.date(2021,10,5)); print('5년 10/5 기준 시작', s, f'SOXX {(X[a]/X[s]-1)*100:+.1f}% SOXL {(L[a]/L[s]-1)*100:+.1f}% | 100만원 {100*X[a]/X[s]:.0f}만 {100*L[a]/L[s]:.0f}만')
a,b=D.date(2024,6,4),D.date(2025,6,11)
print('제자리 구간 100만원', f'SOXX {100*X[b]/X[a]:.0f}만 SOXL {100*L[b]/L[a]:.0f}만')
# 장난감: 하루 -10% 다음 날 제자리로
up=1/0.9-1; print('제자리 회복 상승률', f'{up*100:.2f}%', '3배', f'{(0.7*(1+3*up)-1)*100:.2f}%', '100만원->', round(100*0.7*(1+3*up),1))
