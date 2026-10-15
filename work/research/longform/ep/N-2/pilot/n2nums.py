# N-2 시범작 숫자 — 원문 표7·표13(raw/wagejob2024.pdf 23·28쪽) 값만 옮겨 계산. py -3.12 n2nums.py > n2nums_out.txt
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# 표7 2024년 구간 비율(%): 85미만,85~150,150~250,250~350,350~450,450~550,550~650,650~800,800~1000,1000이상
T7 = {'25~29세': [7.4,4.9,24.2,34.8,16.2,6.1,3.0,2.4,0.8,0.3],
      '40~44세': [6.5,5.7,15.7,16.6,13.4,12.4,10.0,8.1,5.4,6.3],
      '55~59세': [10.6,9.9,21.9,17.6,8.8,6.4,4.5,6.9,6.1,7.2]}
MEAN = {'55~59세': 424}
MED = {'25~29세': 284, '30~34세': 333, '35~39세': 372, '40~44세': 389, '45~49세': 368, '50~54세': 324, '55~59세': 287, '60~64세': 230}
# 표13 2024년 중위: 대기업·중소기업
MED13 = {'35~39세': (580, 300), '40~44세': (664, 300), '45~49세': (717, 290), '50~54세': (725, 273), '55~59세': (621, 253)}
PAY = 350
print('[A] 월 350만원 이상 비율(= 100명 중 앞에서 몇 등)')
for a, r in T7.items():
    print(f'  {a}: {sum(r[4:]):.1f}%  → 100명 중 {round(sum(r[4:]))}등쯤')
print('[B] 55~59세 월 1,000만원 이상', T7['55~59세'][9], '%')
print('[C] 55~59세 평균', MEAN['55~59세'], '· 가운데', MED['55~59세'], '· 차', MEAN['55~59세'] - MED['55~59세'], '· 상호 씨와 평균 차', MEAN['55~59세'] - PAY)
b, s = MED13['55~59세']
print(f'[D] 55~59세 가운데: 대기업 {b} · 중소 {s} · 배율 {b/s:.2f} · 상호 씨-중소 가운데 {PAY-s}')
print('[E] 중소기업 가운데 나이별:', ' · '.join(f'{a} {v[1]}' for a, v in MED13.items()))
print('[F] 나이별 가운데(표7):', ' · '.join(f'{a} {v}' for a, v in MED.items()))
print('[G] 일자리 수: 전수 2,094만 + 표본 37만 =', 2094 + 37, '만 개 (일러두기 2쪽)')
r = T7['55~59세']
print(f'[H] 55~59세 월 85만원 미만 {r[0]}% · 이들을 빼고 다시 세우면 350만원 이상 {sum(r[4:])/(100-r[0])*100:.1f}% → 100명 중 {round(sum(r[4:])/(100-r[0])*100)}등쯤')

# ---- v7(10/16): 전체 직장인 100명 줄 — 표 '소득구간별 분포' 2024년 행(raw/wagejob2024.pdf 9쪽, 인쇄 3쪽, pilot/src/wagejob_p09.png)
#      + 한 달 실수령: 파이어맵 월급 계산기 src/utils/salaryNet.js(소득세법 시행령 별표2 간이세액표 2026.2.27 개정·4대보험 2026 요율)
#        가정: 월급×12를 연봉으로, 1인(본인만), 식대 비과세 월 20만원(계산기 기본값), 자녀 0, 원천징수 100%
import subprocess, json, os
ALL = [12.2, 8.4, 20.9, 20.1, 11.7, 7.8, 5.3, 5.6, 3.7, 4.3]   # 85미만 … 1,000이상, 합 100.0
EDGE = [0, 85, 150, 250, 350, 450, 550, 650, 800, 1000]
ALL_MEAN, ALL_MED = 375, 288                                     # 같은 쪽 '평균소득, 중위소득 현황' 2024년
print('[I] 전체 100명 줄 — 월 X만원 이상 비율(= 앞에서 몇 등)  (합', round(sum(ALL), 1), ')')
for i, e in enumerate(EDGE[1:], 1):
    s = sum(ALL[i:]); print(f'  {e:>5}만원 이상: {s:5.1f}%  → 100명 중 {int(s + 0.5)}등쯤')
print(f'[J] 전체 평균 {ALL_MEAN} · 가운데(50등) {ALL_MED} · 차 {ALL_MEAN - ALL_MED} · 월 85만원 미만 {ALL[0]}%')
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '..'))
JS = 'file:///' + os.path.join(ROOT, 'src', 'utils', 'salaryNet.js').replace(os.sep, '/')
PAYS = [150, 250, 288, 350, 375, 450, 650, 1000]
code = f"import {{salaryNet}} from '{JS}'; console.log(JSON.stringify({PAYS}.map(m => [m, salaryNet({{annual: m*10000*12}}).net])))"
nets = json.loads(subprocess.run(['node', '--input-type=module', '-e', code], capture_output=True, text=True, encoding='utf-8').stdout)
print('[K] 세전 월급 → 한 달 실수령(1인·식대 비과세 20만원 가정):', ' · '.join(f'{m} → {n:,}원(약 {round(n / 10000)}만원)' for m, n in nets))
# [L] 통장 → 세전 어림(대본 1장 '통장 금액에 1할쯤 더하면 세전'): 실수령/세전 비율과 통장 200만원 예시
PAYS2 = [150, 200, 222, 250, 288, 350, 450]
code = f"import {{salaryNet}} from '{JS}'; console.log(JSON.stringify({PAYS2}.map(m => [m, salaryNet({{annual: m*10000*12}}).net])))"
nets2 = json.loads(subprocess.run(['node', '--input-type=module', '-e', code], capture_output=True, text=True, encoding='utf-8').stdout)
print('[L] 실수령/세전:', ' · '.join(f'{m} → {n / (m * 10000):.3f}' for m, n in nets2), '· 세전 222만원 → 통장', f'{dict(nets2)[222]:,}원(≈200만원)')
