s=open('../costchk1016/cover_try.py',encoding='utf-8').read()
a=s.index('V_ = {');b=s.index('}',s.index("'K3'"))+1
s=s[:a]+'''V_ = {
 'R1': [('퇴직금 똑같이 2억', 120, Wt, 't'), ('25년 다니면 세금 약 508만원', 80, Wt, 't'), ('10년이면 약 1,788만원', 95, Y, 't')],
 'R2': [('퇴직소득세', 150, Wt, 't'), ('같은 2억인데', 120, Wt, 't'), ('세 배 넘게 차이', 125, Y, 't')],
 'R3': [('퇴직금 2억 퇴직소득세', 100, Wt, 't'), ('25년 다닌 사람 약 508만원', 82, Wt, 't'), ('10년 다닌 사람 약 1,788만원', 82, Y, 't')],
}'''+s[b:]
import re
s=re.sub(r"^SRC = .*$", "SRC = '소득세법 제48조·제55조 · 퇴직금 2억원 예시 · 국세 기준'", s, flags=re.M)
s=s.replace('# costchk1016 표지','# retax1016 표지')
open('cover_try.py','w',encoding='utf-8').write(s)
