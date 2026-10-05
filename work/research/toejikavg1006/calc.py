# toejikavg1006 계산 — 퇴직금 평균임금에 상여·연차수당을 넣으면 얼마나 달라지나. firemap-write 2026-10-06
# 규칙: 근로기준법 2조①6호(산정사유 발생일 이전 3개월 임금총액 ÷ 그 기간 총일수), 근퇴법 8조①(1년에 30일분),
# 고용노동부 퇴직금 계산기(1350.moel.go.kr) 예제: 연간상여금 × 3/12, 연차수당 × 3/12 가산, 퇴직금 = 1일 평균임금 × 30 × 재직일수/365
# 연차수당은 '퇴직 전년도에 발생해 못 쓴 휴가'분만 (고용노동부 빠른상담 201707140941334611000). 퇴직하는 해에 새로 생긴 연차의 수당은 안 들어감.
import sys, datetime as dt; sys.stdout.reconfigure(encoding='utf-8')
def avg_day(wage3m, days, bonus_y=0, annual_pay=0):
    return (wage3m + bonus_y*3/12 + annual_pay*3/12) / days
def sev(avg, service_days):
    return avg * 30 * service_days / 365
def won(x): return f"{x:,.0f}원"
if __name__ == '__main__':
    # 1) 고용노동부 예제 재현(검산)
    a = avg_day(7_080_000, 92, 4_000_000, 300_000); print('노동부 예제 1일 평균임금', f"{a:,.2f}", '(공식 88,641원 31전)', '퇴직금', won(sev(a, 1080)))
    # 2) 우리 사례(가정): 입사 2006-10-01, 마지막 근무 2026-09-30 → 퇴직일 2026-10-01
    join, out = dt.date(2006,10,1), dt.date(2026,10,1)
    sd = (out - join).days
    p0, p1 = dt.date(2026,7,1), out; days = (p1 - p0).days
    base, extra = 4_000_000, 500_000; wage3m = (base+extra)*3
    bonus, annual = 8_000_000, 1_500_000   # 정기상여 연 800만(기본급 200%), 전년도 발생 미사용 연차 10일 × 15만원
    print('재직일수', sd, '| 3개월 일수', days, '| 3개월 임금', won(wage3m))
    res = {}
    for name, b, an in [('월급만', 0, 0), ('+상여', bonus, 0), ('+상여+연차', bonus, annual)]:
        ad = avg_day(wage3m, days, b, an); s = sev(ad, sd); res[name] = (ad, s)
        print(f"{name}: 1일 평균임금 {ad:,.0f}원 · 퇴직금 {s:,.0f}원")
    print('상여 빠지면 차이', won(res['+상여'][1]-res['월급만'][1]), '| 연차 빠지면 차이', won(res['+상여+연차'][1]-res['+상여'][1]),
          '| 둘 다', won(res['+상여+연차'][1]-res['월급만'][1]))
    # 3) 퇴직하는 해 새 연차(15일×15만=225만)를 잘못 넣으면
    wrong = avg_day(wage3m, days, bonus, annual + 15*150_000); print('퇴직 연도 새 연차까지 넣은 잘못된 값 퇴직금', won(sev(wrong, sd)), '차이', won(sev(wrong, sd)-res['+상여+연차'][1]))
    # 4) 3개월 일수: 2/28 마지막 근무(퇴직일 3/1) → 12/1~2/28 = 90일
    d90 = (dt.date(2027,3,1)-dt.date(2026,12,1)).days
    print('2월 낀 3개월 일수', d90, '1일 평균임금', f"{avg_day(wage3m, d90, bonus, annual):,.0f}", '같은 근속이면 퇴직금 비율', f"{92/d90-1:.2%}")
