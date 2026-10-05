# toejikavg1006 이미지 01·02 — 숫자는 calc.py 그대로. firemap-write 2026-10-06 (00은 표지, 09:00 뒤 따로)
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '..', '..')); sys.path.insert(0, D)
import blogimg as B
from calc import avg_day, sev
IMG = os.path.join(D, 'pkg', 'img')
def man(v):
    m = round(v/1e4); e, r = divmod(m, 10000)
    return (f"{e}억 {r:,}만원" if r else f"{e}억원") if e else f"{r:,}만원"
W3, DAYS, SD = 13_500_000, 92, 7305
rows = []
for name, b, an in [('석 달 월급만', 0, 0), ('+ 정기상여 연 800만원', 8e6, 0), ('+ 작년 생긴 연차 10일 수당', 8e6, 1.5e6)]:
    a = avg_day(W3, DAYS, b, an); rows.append([name, f"{a:,.0f}원", man(sev(a, SD))])
B.table(os.path.join(IMG, '01.png'), '월 450만원·20년 근속, 무엇을 넣느냐에 따라', ['넣은 것', '하루치 평균임금', '퇴직금'], rows,
        hl_col=2, note='상여·연차수당은 1년 치의 3/12만 더함. 퇴직 전 석 달 7~9월 92일, 재직 7,305일 가정.',
        src='근로기준법 제2조, 근로자퇴직급여 보장법 제8조, 고용노동부 퇴직금 계산기 예제, 파이어맵 계산')
B.table(os.path.join(IMG, '02.png'), '평균임금에 들어가는 것과 빠지는 것', ['항목', '넣는 법'],
        [['퇴직 전 석 달 월급·수당', '그대로'], ['정기상여금', '1년 합계 × 3/12'],
         ['작년에 생겨 못 쓴 연차수당', '× 3/12'], ['올해 생긴 연차를 못 쓰고 받는 수당', '빠짐'],
         ['그해 한 번 준 임시 보너스', '빠짐']],
        hl_col=1, note='하루치 평균임금이 통상임금보다 적으면 통상임금으로 계산.',
        src='근로기준법 시행령 제2조, 고용노동부 퇴직금 계산기·빠른인터넷상담 답변')
print(rows)
