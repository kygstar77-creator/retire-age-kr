# sevbasis1010 계산 — 퇴직금 지급기준(1년·주 15시간) 경계와 지급 기한 지연이자. firemap-write helper 2026-10-09
# 규칙: 근퇴법 제4조①단서(1년 미만·4주 평균 주 15시간 미만 제외), 제8조①(1년에 30일분 평균임금),
# 고용노동부 퇴직금 계산(1350.moel.go.kr): 퇴직일자 = 마지막 근무일 1일 후, 퇴직금 = 1일 평균임금 × 30 × 재직일수/365,
#   예제 2014.10.2 입사 → 2017.9.16 퇴사 = 재직일수 1,080일(아래에서 검산)
# 고용노동부 예규 2015-99(제4조①단서 해석기준): 1년 넘으면 1년 미만 단수(몇 월 며칠)도 비례 지급
# 근로기준법 제37조①1호·시행령 제17조: 14일이 되는 날까지 안 주면 그다음 날부터 연 20%
import sys, datetime as dt; sys.stdout.reconfigure(encoding='utf-8')
D = dt.date
def days(a, b): return (b - a).days
def sev(avg, sd): return avg * 30 * sd / 365 if sd >= 365 else 0
print('검산: 노동부 예제 재직일수', days(D(2014,10,2), D(2017,9,16)), '(공식 1,080일)')
hire = D(2025,11,3); AVG = 100_000   # 가정: 1일 평균임금 10만원
print(f'가정: 입사 {hire} · 1일 평균임금 {AVG:,}원 · 주 15시간 이상')
rows = []
for last in (D(2026,11,1), D(2026,11,2), D(2027,5,2)):
    out = last + dt.timedelta(days=1); sd = days(hire, out); s = sev(AVG, sd)
    rows.append((last, out, sd, s))
    print(f'마지막 근무 {last} → 퇴직일 {out} · 재직일수 {sd}일 · 퇴직금 {s:,.0f}원' + ('  (1년 미만 — 법정 의무 없음)' if sd < 365 else ''))
print('하루 차이(364→365일) 차액', f'{rows[1][3]-rows[0][3]:,.0f}원')
print('1년 6개월 비례분(546일)', f'{rows[2][3]:,.0f}원', '= 300만원 ×', f'{546/365:.4f}')
# 4주 평균 소정근로시간
for name, wk in (('A', [16,14,16,14]), ('B', [15,14,15,14])):
    av = sum(wk)/4; print(f'근무표 {name} {wk} → 4주 평균 {av}시간 → ' + ('대상(15시간 이상)' if av >= 15 else '제외(15시간 미만)'))
# 지연이자: 300만원을 기한 다음 날부터 30일 늦게
P = 3_000_000
for late in (30, 90):
    print(f'퇴직금 {P:,}원 {late}일 늦게 → 지연이자 연 20% {P*0.2*late/365:,.0f}원')
