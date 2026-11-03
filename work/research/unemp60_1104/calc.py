# 정년퇴직 실업급여·실업크레딧 계산 (2026-11-03 firemap-write-b) — 원문 raw/ 참조
import sys; sys.stdout.reconfigure(encoding='utf-8')
MIN_WAGE=10320; H=8
low=int(MIN_WAGE*H*0.8)            # 하한 법45④·46①2
cap_base=113500; high=int(cap_base*0.6)  # 시행령68 × 법46①1
print('하루 하한',low,'상한',high)
days=270                           # 별표1 50세 이상·10년 이상
print('270일 총액 하한',low*days,'상한',high*days)
# 신청 마감: 이직 다음 날부터 12개월(법48①) 안에 대기 7일(법49) + 270일
# 이직 다음 날=1일째. d일째 신고 → 대기 d~d+6, 지급 d+7~365 → 받을 날 359-d
print('270일 다 받으려면 이직 다음 날부터 세어 늦어도',359-days,'일째까지 실업 신고(12개월=365일로 셈)')
for d in (89,120,150):
    left=min(days,max(0,359-d)); lost=days-left
    print(f'{d}일째 신고 → 받을 날 {left}일, 잃는 날 {lost}일 = 하한으로 {lost*low:,}원')
# 실업크레딧(NPS 안내): 인정소득=기초일액 월환산 절반, 상한 70만, 보험료 9.5%, 75% 지원, 횟수=지급일수/30
rec=700000; prem=rec*0.095; sup=prem*0.75; own=prem-sup; n=days//30
print('인정소득 상한 기준 월 보험료',prem,'지원',sup,'본인',own,'횟수',n)
print('270일 받는 사람 지원 합계',sup*n,'본인 합계',own*n)
# 월 기초일액 절반이 70만원 넘는 기초일액: 70만*2/30
print('인정소득 70만원이 되는 기초일액(월30일 환산)',round(rec*2/30))
print('하한 기초일액 82,560원 월환산(×30) 절반',int(MIN_WAGE*H*30/2),'→ 70만원 상한에 걸림')
