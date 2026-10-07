# ubapply1007 계산: 이직일 2026-06-30, 신청일 = 7/1 + n개월(1일). 수급기간 = 이직 다음 날부터 12개월(~2027-06-30, 365일), 대기 7일(신고일부터), 상한 일액 68,100원
from datetime import date, timedelta
import calendar
def addm(d,n):
    y=d.year+(d.month-1+n)//12; m=(d.month-1+n)%12+1
    return date(y,m,min(d.day,calendar.monthrange(y,m)[1]))
leave=date(2026,6,30); end=addm(leave,12)
for S in (270,180):
  for n in (0,2,3,4,6,8):
    sin=addm(leave+timedelta(1),n); st=sin+timedelta(7)
    avail=(end-st).days+1; got=min(S,max(avail,0))
    print(S,f'{n}개월',sin,'지급시작',st,'가능',avail,'받음',got,'못받음',S-got,'금액',(S-got)*68100)
print('안전선 일수', 365-7-270)
