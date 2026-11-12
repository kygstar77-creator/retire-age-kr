# 1억원을 넣었을 때 2026년 네 번 분배금(세전·세후), 2029년 뒤 KODEX 예상치 계산 — 원자료: 운용사 분배율(S1 KODEX divid-info, S2 ACE API, S3 TIGER 분배 표·종가)
import sys; sys.stdout.reconfigure(encoding='utf-8')
kodex = [0.5264, 0.4916, 0.5424, 0.5019]          # 26.01·04·07·10 분배율(%), 삼성 divid-info
ace = [0.2604, 0.2343, 0.2451, 0.2280]            # ACE API
tiger_amt = [65, 62, 66, 60]; tiger_px = 25020    # TIGER 분배금(원)·11/11 종가(원) — 근사
tiger = [a / tiger_px * 100 for a in tiger_amt]
for nm, r in (('KODEX', kodex), ('ACE', ace), ('TIGER(근사)', tiger)):
    y = sum(r); pre = 1e8 * y / 100; post = pre * (1 - 0.154)
    print(f'{nm}: 1년 분배율 {y:.3f}% · 1억 세전 {pre:,.0f}원 · 세후 {post:,.0f}원 · 세후 월 {post/12:,.0f}원')
extra = 0.27  # 삼성 공지: 유보분 분기당 NAV 대비 약 0.27%
base_q = sum(kodex) / 4 - extra
print(f'KODEX 유보분 빼면 분기 약 {base_q:.3f}% · 1년 {base_q*4:.3f}% · 1억 세전 {1e8*base_q*4/100:,.0f}원')
print('KODEX 2026 합', 119+118+132+117, '· ACE', 65+62+66+59, '· TIGER', sum(tiger_amt))
