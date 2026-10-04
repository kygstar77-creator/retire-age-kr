# 계산기 고친 문구 (PC 편집 담당 적용용)

- 근거와 이유는 `calculators.md`의 같은 줄을 본다. src는 고치지 않았다.
- 줄 번호는 브랜치 시작점 dev 575023e0 기준이다. `{…}`는 코드 변수 자리다. 숫자는 원문 그대로다. 새로 계산한 값은 calculators.md 이유 칸에 식을 적었다.
- toolPages.js의 sections·body는 화면 문장을 그대로 옮긴 것이다. 화면을 고치면 같이 고친다(파일 주석 규칙).
- 먼저 고칠 것(오해·사실 순서):
  1. 퇴직금 '4주 평균' 빠짐 — SeveranceCalc.jsx:74·103-104·124, toolPages.js:17·19
  2. 실업급여 '이직일' 뜻 — UnemploymentCalc.jsx:90
  3. 실업급여 '상한 · 하한 60%' 칸 — UnemploymentCalc.jsx:30-31·71
  4. 실업급여 상한·하한 차이 2,052원 문장 추가 — UnemploymentCalc.jsx:113
  5. 연봉 국민연금 상·하한 적용 기간 — SalaryCalc.jsx:101
- `(빼기)` = 그 문구를 지운다. `[조사 필요: …]` = 확인되기 전에는 적용하지 말고 앞 문장만 쓴다.

| 파일:줄 | 원문 | 고친 문구 |
|---|---|---|
| src/components/firemap/Home.jsx:39 | 또래 상위 {pct}% · 나는 몇 살에 가능할까? 1분이면 나와요. | 또래 상위 {pct}% · 나는 몇 살에 가능할까? |
| src/components/firemap/Home.jsx:44 | 자산·저축·생활비만 넣으면 물가·국민연금까지 반영한 파이어 나이가 나와요. | 자산·저축·생활비만 넣으면 회사를 그만둬도 되는 나이(파이어 나이)가 나와요. 물가와 국민연금도 넣어 계산해요. |
| src/components/firemap/Home.jsx:31 | {N}명이 계산했어요 · 평균 파이어 {X}세 | {N}명이 계산했어요 · 이들의 평균 파이어 나이 {X}세 |
| index.html:24 | 파이어맵 (title) | 파이어맵 — 몇 살에 은퇴할 수 있을까, 파이어 나이 계산기 |
| index.html:6 | 내 파이어(조기은퇴) 가능 나이와 목표 자산을 1분 만에 계산. 자산·연금·세금 반영. 또래 중 내 등수도. | 내 파이어(조기은퇴) 가능 나이와 필요한 자산을 1분 만에 계산해요. 자산·연금·세금을 넣고, 또래 중 내 등수도 나와요. |
| functions/_middleware.js:27 | 파이어맵 · 1분이면 나도 계산 (도구 주소 로딩 화면 한 줄) | 파이어맵 · 계산기를 여는 중 |
| functions/_middleware.js:27 | 1분이면 나도 계산 (링크) | 내 파이어 나이 계산하기 |
| src/components/firemap/SalaryCalc.jsx:53 | 세액표 {ratio}% | 소득세 떼는 비율 {ratio}% |
| src/components/firemap/SalaryCalc.jsx:58 | 원천징수 비율 · 기본은 100%예요 · 회사에 신청하면 80% · 120%도 돼요 | 매달 떼는 소득세 비율이에요. 기본은 100%, 회사에 신청하면 80%나 120%로 바꿀 수 있어요. 80%면 매달 덜 떼는 대신 연말정산 때 더 낼 수 있어요. |
| src/components/firemap/SalaryCalc.jsx:69 | 연봉 실수령 계산기 (kicker) | (빼기) |
| src/components/firemap/SalaryCalc.jsx:75 | 공제대상가족 (제목) | 부양가족(공제대상가족) |
| src/components/firemap/SalaryCalc.jsx:77 | 공제대상가족 수에 포함된 자녀예요 | 위 가족 수에 이미 넣은 자녀 중 8세 이상 20세 이하인 아이 수예요 |
| src/components/firemap/SalaryCalc.jsx:101 | 소득세는 근로소득 간이세액표(소득세법 시행령 별표 2, 2026. 2. 27. 개정)의 월급여액(비과세 제외)·공제대상가족 수 해당란 세액이에요. | 소득세는 근로소득 간이세액표(소득세법 시행령 별표 2, 2026. 2. 27. 개정)에서 비과세를 뺀 월급과 가족 수가 만나는 칸의 금액이에요. |
| src/components/firemap/SalaryCalc.jsx:101 | 8세 이상 20세 이하 자녀는 1명 20,830원, 2명 45,830원, 3명부터 1명당 33,330원을 더 빼요. | 8세 이상 20세 이하 자녀가 있으면 소득세에서 1명 20,830원, 2명 45,830원, 3명부터 1명당 33,330원을 더 빼요. 국세청 안내 글에는 개정 전 금액(1명 12,500원 등)이 남아 있어 다를 수 있어요(2026-10-01 확인). |
| src/components/firemap/SalaryCalc.jsx:101 | 국민연금은 기준소득월액(41만원~659만원)의 4.75%, 건강보험은 3.595%, 장기요양보험은 건강보험료의 13.14%, 고용보험은 0.9%예요. | 국민연금은 월급이 41만원보다 적으면 41만원, 659만원보다 많으면 659만원으로 보고 계산해요(2026.7~2027.6 기준). |
| src/components/firemap/SalaryCalc.jsx:103 | {2026-10-01} 기준 · 참고용, 실제와 다를 수 있어요. | 2026-10-01 기준 · 회사 급여명세서와는 비과세 항목과 공제 방식에 따라 다를 수 있어요. |
| src/components/firemap/SeveranceCalc.jsx:74 | 1주 소정근로시간 15시간 미만이면 퇴직금 대상이 아니에요 | 4주 평균으로 1주에 15시간 미만 일했다면 퇴직금이 없어요 |
| src/components/firemap/SeveranceCalc.jsx:74 | 계속근로기간 1년 미만이면 퇴직금 대상이 아니에요 | 일한 기간이 1년이 안 되면 퇴직금이 없어요 |
| src/components/firemap/SeveranceCalc.jsx:75 | 재직 {N}일 · 약 {Y}년 | 약 {Y}년 · 1년마다 평균임금 30일치 |
| src/components/firemap/SeveranceCalc.jsx:79 | 3개월 총일수 | 평균 낸 날수 |
| src/components/firemap/SeveranceCalc.jsx:93 | 현재 자산 + 퇴직금 {X} | 지금 자산에 퇴직금 {X}을 더해 계산해요 |
| src/components/firemap/SeveranceCalc.jsx:98 | 퇴직금 계산기 (kicker) | (빼기) |
| src/components/firemap/SeveranceCalc.jsx:103-104 | 1주 15시간 이상 / 1주 15시간 미만 (탭, 이름 '1주 소정근로시간') | 4주 평균 1주 15시간 이상 / 미만 |
| src/components/firemap/SeveranceCalc.jsx:108 | 기본급 + 기타수당 (desc) | (빼기) |
| src/components/firemap/SeveranceCalc.jsx:110 | 상여금 · 연차수당 / 있으면 3개월치(3/12)를 더해요 | 상여금 · 연차수당 / 있으면 3개월치(3/12)를 더해요. 빼먹으면 퇴직금이 적게 나와요 |
| src/components/firemap/SeveranceCalc.jsx:112 | 연차수당 (라벨) | 연차수당 · 1년 치 합계 |
| src/components/firemap/SeveranceCalc.jsx:118 | 실업급여 계산기 / 나이·피보험기간·월급으로 1일 구직급여액·총액 | 실업급여 계산기 / 그만둔 뒤 받는 실업급여, 하루 얼마·모두 얼마 |
| src/components/firemap/SeveranceCalc.jsx:124 | 계속근로기간 1년에 대하여 30일분 이상의 평균임금(근로자퇴직급여 보장법 제8조). | 1년 일할 때마다 평균임금 30일치 이상을 받아요(근로자퇴직급여 보장법 제8조). |
| src/components/firemap/SeveranceCalc.jsx:124 | 계속근로기간 1년 미만이거나 1주 소정근로시간 15시간 미만이면 대상이 아니에요(같은 법 제4조). | 일한 기간이 1년이 안 되거나, 4주 평균 1주 15시간 미만 일했다면 받을 수 없어요(같은 법 제4조). |
| src/components/firemap/SeveranceCalc.jsx:126 | {2026-09-30} 기준 · 퇴직소득세를 빼기 전 금액이에요. | 2026-09-30 기준 · 퇴직소득세를 빼기 전 금액이에요. 예를 들어 3년 6개월 일하고 퇴직금 12,826,183원이면 퇴직소득세·지방소득세는 약 16만원이에요. |
| src/components/firemap/SeveranceCalc.jsx:126 | 육아휴직 등 미산입기간과 통상임금 비교는 반영하지 않았어요. | 마지막 3개월 안에 육아휴직·출산휴가·업무상 병가 같은 기간이 있었거나, 평균임금이 통상임금보다 적으면 실제 금액이 다를 수 있어요. |
| src/components/firemap/SeveranceCalc.jsx:126 | 정확한 금액은 고용노동부 퇴직금 계산에서 확인하세요. | 정확한 금액은 고용노동부 퇴직금 계산기(moel.go.kr)에서 확인하세요. |
| src/components/firemap/UnemploymentCalc.jsx:65 | 예상 실업급여 총액 · 구직급여 | 예상 실업급여 총액 |
| src/components/firemap/UnemploymentCalc.jsx:67 | 고용보험법 제45조·제46조·제50조 · {2026-09-30} 기준 | 한 달(30일)이면 약 {daily×30}원 · 2026-09-30 기준 |
| src/components/firemap/UnemploymentCalc.jsx:69 | 1일 구직급여액 | 하루 실업급여 |
| src/components/firemap/UnemploymentCalc.jsx:70 | 소정급여일수 | 받는 날수 |
| src/components/firemap/UnemploymentCalc.jsx:30-31,71 | (칸 이름) 상한 / 하한 / 상한 · 하한 — (값) {68,100원} / {66,048원} / 60% | 상한·하한에 안 걸릴 때: 이름 '적용 비율', 값 '평균임금의 60%' (상한·하한에 걸릴 때는 그대로) |
| src/components/firemap/UnemploymentCalc.jsx:85 | 현재 자산 + 실업급여 {X} | 지금 자산에 실업급여 {X}을 더해 계산해요 |
| src/components/firemap/UnemploymentCalc.jsx:90 | 실업급여 계산기 (kicker) | (빼기) |
| src/components/firemap/UnemploymentCalc.jsx:90 | 이직일 현재 나이로 소정급여일수가 정해져요 | 이직일은 마지막으로 일한 날이에요(퇴직금 계산기의 퇴직일자보다 하루 앞). 이날 나이로 받는 날수가 정해져요. |
| src/components/firemap/UnemploymentCalc.jsx:104 | 기본급 + 기타수당 (desc) | (빼기) |
| src/components/firemap/UnemploymentCalc.jsx:106 | 1일 소정근로시간 / 8시간보다 짧으면 하한액이 낮아져요 | 하루 정해진 근로시간 / 8시간보다 짧으면 최소 금액이 낮아져요 |
| src/components/firemap/UnemploymentCalc.jsx:107 | 1일 소정근로시간 (라벨) | 하루 정해진 근로시간 |
| src/components/firemap/UnemploymentCalc.jsx:112 | 계산 방법 / 1일 구직급여액 × 소정급여일수 | 계산 방법 / 하루 실업급여 × 받는 날수 |
| src/components/firemap/UnemploymentCalc.jsx:113 | 기초일액 상한은 113,500원이라 1일 최대 68,100원(시행령 제68조). | 기초일액 상한은 113,500원이라 하루 최대 68,100원이에요(시행령 제68조). 3개월 월평균 임금이 약 337만~348만원(3개월 날수 89~92일에 따라)을 넘으면 누구나 68,100원이에요. |
| src/components/firemap/UnemploymentCalc.jsx:113 | 하한은 이직일 최저임금 10,320원 × 1일 소정근로시간 × 80%, 8시간이면 66,048원. | 하한은 이직일 최저임금 10,320원 × 하루 근로시간 × 80%라서, 8시간이면 66,048원이에요. 그래서 하루 8시간 일했다면 누구나 하루 66,048~68,100원 사이를 받아요. |
| src/components/firemap/UnemploymentCalc.jsx:114 | 받으려면 이직일 이전 18개월 동안 피보험 단위기간이 합산 180일 이상이어야 해요(제40조). | 받으려면 그만두기 전 18개월 안에 고용보험에 든 채 임금을 받은 날이 모두 180일 이상이어야 해요(제40조). |
| src/components/firemap/UnemploymentCalc.jsx:114 | 전직·자영업을 하려고 그만두는 등 자기 사정으로 이직하면 수급자격이 없을 수 있어요(제58조). | 스스로 그만두면(이직·창업 준비 등) 받지 못할 수 있어요(제58조). [조사 필요: 제58조의 정당한 이직 사유 예외 원문·고용24 안내] |
| src/components/firemap/UnemploymentCalc.jsx:116 | {2026-09-30} 기준 · 2026년 이직자 기준이에요. | 2026-09-30 확인 · 2026년에 그만둔 사람만 계산해요. |
| src/components/firemap/UnemploymentCalc.jsx:116 | 통상임금 비교와 일용근로자·자영업자·예술인·노무제공자는 반영하지 않았어요. | 일용직·자영업자·예술인·노무제공자는 계산 방식이 달라 여기서는 계산하지 않아요. 평균임금이 통상임금보다 적은 경우도 반영하지 않았어요. |
| src/firemap-v2/toolPages.js:17 | 퇴직금 계산기. 1일 평균임금 × 30일 × (재직일수 ÷ 365). 상여금·연차수당 3/12 반영, 1년 미만·주 15시간 미만 여부까지. 결과로 은퇴 나이 계산. | 입사일·퇴직일·월급을 넣으면 예상 퇴직금이 나와요. 상여금·연차수당 3/12 반영, 1년 미만·4주 평균 주 15시간 미만이면 대상이 아닌 것까지 알려 줘요. 2026-09-30 기준. |
| src/firemap-v2/toolPages.js:19 | body 5문장(화면 124·98·126줄과 같은 문장) | 화면 124·126줄 고친 문장으로 같이 바꾼다 |
| src/firemap-v2/toolPages.js:21 | 실업급여 계산기 — 나이·피보험기간·월급으로 1일 구직급여액·총액 (seoTitle) | 실업급여 계산기 2026 — 나이·가입 기간·월급으로 하루 얼마·총 얼마 |
| src/firemap-v2/toolPages.js:22 | 실업급여 계산기. 1일 구직급여액 × 소정급여일수. 기초일액 상한은 113,500원이라 1일 최대 68,100원, 하한은 8시간이면 66,048원. 소정급여일수 120~270일. 결과로 은퇴 나이 계산. | 2026년 실업급여는 하루 최대 68,100원, 8시간 기준 최소 66,048원이에요. 나이·가입 기간·월급을 넣으면 하루 금액과 받는 날수(120~270일), 총액이 나와요. 2026-09-30 기준. |
| src/firemap-v2/toolPages.js:24 | body 4문장(화면 112~116줄과 같은 문장) | 화면 113·114·116줄 고친 문장으로 같이 바꾼다 |
| src/firemap-v2/toolPages.js:27 | 연봉계산기·연봉 실수령액 계산기. 2026. 2. 27. 개정 근로소득 간이세액표, 국민연금 4.75%·건강보험 3.595%·장기요양 13.14%·고용보험 0.9%. 부양가족·8세 이상 20세 이하 자녀·원천징수 80·120%까지. 결과로 은퇴 나이 계산. | 연봉을 넣으면 4대보험·소득세를 떼고 매달 받는 돈이 나와요. 2026. 2. 27. 개정 간이세액표, 국민연금 4.75%·건강보험 3.595%·장기요양 13.14%·고용보험 0.9%, 부양가족·8세 이상 20세 이하 자녀·원천징수 80·120%까지. 2026-10-01 기준. |
| src/firemap-v2/toolPages.js:29 | body 5문장(화면 101줄과 같은 문장) | 화면 101줄 고친 문장으로 같이 바꾼다 |
