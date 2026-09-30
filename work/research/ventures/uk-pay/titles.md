# X-V1 UK take-home pay — 검색 결과 문구·화면 문구 (카피라이터 2026-10-01 07:5x)

적용은 firemap-venture-builder 몫이다. 숫자(£100,000·£125,140·60%·62%)는 brief.md 값이며, 빌더가 gov.uk 2026/27 원문으로 다시 확인한 뒤에만 쓴다. 원문과 다르면 원문을 따르고 문구는 숫자만 바꾼다.

## 0. 경쟁 비교 (실제로 받은 것, 10/1 07:50 curl·DuckDuckGo uk-en·구글 자동완성)

### 머리 검색어 — 경쟁 title / description
| 사이트 | title | description 요지 |
|---|---|---|
| thesalarycalculator.co.uk (1등) | The Salary Calculator - 2026 / 2027 Tax Calculator | monthly take-home, Tax·NI·Student Loan, "April 2026 budget", 시급·주급·보너스 |
| listentotaxman.com | UK Tax Calculator & Take Home Pay 2026-27 \| Listen to Taxman | (비어 있음) |
| income-tax.co.uk | UK Salary Tax Calculator - UK Salary Tax Calculator | net salary, tax·NI, 기능 나열(학자금·연금·차량·배당·스코틀랜드) |
| gov.uk/estimate-income-tax | Estimate your Income Tax for the current year - GOV.UK | — |
| uktaxcalculators.co.uk | 봇 차단(Just a moment) — 확인 안 함 | |

### 롱테일 '60% tax trap calculator' — 1페이지 10개 전부 전용 계산기
| title | 세금 해 |
|---|---|
| 60% Tax Trap Calculator 2025/26 \| £100,000 Income Tax Trap (ukcalculator.com) | **25/26** |
| 60% Tax Trap Calculator \| Work Out Your £100k+ Salary Tax (UK) (investinginsiders) | 없음 |
| 60% Tax Trap Calculator \| £100k Personal Allowance Taper (ukfinancecalculator) | 없음 |
| UK Tax Trap & Salary Calculator 2025/26 - Avoid the 60% Tax Trap (taxtrapcalculator.co.uk) | **25/26** |
| UK £100k Tax Trap Calculator 2026/27 \| HMRC 60% Marginal Rate (uktax.tools) | 26/27 |
| 60% Tax Trap Calculator - GNS Associates | 없음 |
| 60% Tax Trap Calculator 2026/27 - PensionCalc | 26/27 |
| 60% Tax Trap Calculator 2025/26 \| £100k Tax Calculator UK \| The Marginal | **25/26** |
| 60% Tax Trap Calculator & Guide \| SalaryTaxCalc.co.uk | 없음 |
| 60% Tax Trap Calculator — The Hidden Tax Between £100k and £125k (pensionbible) | 없음 |

- description 5곳 중 4곳이 이미 "pension contribution you need to escape / pension strategies"를 판다(uktax.tools·pensioncalc·ukcalculator·themarginal). **brief 5장의 연금 역산은 이 페이지에서 차별점이 아니다.**
- 구글 자동완성(en-GB): "60 tax trap" → calculator·explained·uk·scotland·how to avoid·money saving expert·graph·reddit·example / "100k tax trap" → money saving expert·uk·**childcare**·explained·calculator.

### 3줄
- **경쟁이 잘하는 것:** 검색어 "60% Tax Trap Calculator"·"Take Home Pay"를 title 맨 앞에 두고, 세금 해(2026/27)를 title에 적는다. description은 기능 나열.
- **우리가 따라갈 것:** 검색어 맨 앞 + "2026/27" + 구간 숫자(£100,000–£125,140).
- **우리가 다르게 할 것:** ① 10개 중 3개가 아직 2025/26 → 우리는 2026/27을 title에 확실히. ② description에 "다음 £1,000에서 얼마 남나"(한계 실수령)를 넣는다 — 머리 경쟁 3곳 description에 없음. ③ "escape·avoid" 같은 권유형 동사 대신 계산 결과만(brief 9장 FSMA). ④ 스코틀랜드 미지원을 숨기지 않는다.

## 1. `/` 머리 페이지

### title 후보 (글자 수)
1. Take Home Pay Calculator UK 2026/27 – Tax, NI & Student Loan (60)
2. Take Home Pay Calculator UK 2026/27 – Your Monthly Pay After Tax (64)
3. UK Take-Home Pay Calculator 2026/27 – Monthly Net Pay (53)
4. Take Home Pay Calculator UK 2026/27 – What the Next £1,000 Keeps (64)
5. UK Salary After Tax 2026/27 – Take Home Pay Calculator (54)
6. Take Home Pay Calculator UK 2026/27 (England, Wales & NI) (57)
7. UK Net Pay Calculator 2026/27 – Income Tax, NI, Pension (55)
8. Take Home Pay Calculator UK – 2026/27 Monthly, Weekly, Hourly (61)

- **1위: 1번.** 검색어 "take home pay calculator"(30.1만)·"…uk"(4.05만, [2차] Semrush)를 붙은 순서 그대로 맨 앞에. 자동완성 1·2위와 같은 말. 뒤는 실제로 계산하는 세 항목만(연금은 선택이라 뺌). 60자라 잘리지 않는다.
- **2위: 6번.** 스코틀랜드 사용자가 잘못 들어오는 것을 title에서 막는다. 1주 판정에서 이탈이 크면 이쪽.
- 버림: 4번(64자, 뒤가 잘려 차별점이 안 보임), 8번(시급·주급 입력이 실제로 되는지 빌더 화면 확정 전).

### description 1위 (143자)
> Enter your salary to see your 2026/27 monthly take-home pay after Income Tax, NI and student loan – and how much of your next £1,000 you keep. England, Wales & NI.

- 2위: See what's left of your salary each month in 2026/27 after Income Tax, National Insurance and student loan. Estimate only, not tax advice.

### 화면 문구
- H1: `Take home pay calculator UK 2026/27`
- 입력 칸 라벨: `Your salary` · 선택: `per year / month / week / hour` · 버튼: `Calculate`
- 결과 큰 숫자 한 줄: `£X,XXX a month after tax` (아래 작게 `£XX,XXX a year`)
- 한계 실수령 한 줄: `Of your next £1,000, you keep £YYY.`
- 60% 구간일 때 경고: `Your salary is in the £100,000–£125,140 band, where the next £1,000 is taxed at an effective 60% (62% with NI).` → 텍스트 링크 `See the 60% band in detail`
- 공유 버튼: `Share my result` · 공유 카드 제목(금액 가림 기본): `My take-home pay, 2026/27` / 가림 줄 `Salary band: £40k–£50k`

## 2. `/60-percent-tax-trap/`

### title 후보
1. 60% Tax Trap Calculator 2026/27 – £100,000 to £125,140 (54)
2. 60% Tax Trap Calculator 2026/27 | £100k Personal Allowance Loss (63)
3. £100k Tax Trap Calculator 2026/27 – Your 60% Band in Numbers (60)
4. 60% Tax Trap Calculator UK 2026/27 – Personal Allowance Taper (61)
5. Earning £100k–£125,140? 60% Tax Trap Calculator 2026/27 (55)
6. 60% Tax Trap Calculator 2026/27 – Pension Needed to Reach £100k (63)
7. 100k Tax Trap Calculator UK – 2026/27 Effective 60% Rate (56)
8. 60% Tax Trap Calculator (2026/27, England, Wales & NI) (54)

- **1위: 1번.** 1페이지 10개 중 9개가 "60% Tax Trap Calculator"로 시작 → 검색어는 그대로 맨 앞. 차이는 2026/27(10개 중 3개가 아직 25/26)과 정확한 구간 숫자. 54자.
- **2위: 8번.** 스코틀랜드 자동완성("60 tax trap scotland")이 있어 잘못 들어오는 사람을 걸러 낸다.
- 버림: 6번(연금 역산을 title에 걸면 권유로 읽힐 수 있고 경쟁 4곳과 같다), 5번(질문형은 머리 페이지와 틀 겹침).

### description 1위 (150자대)
> Earning £100,000–£125,140? See the Personal Allowance you lose, your marginal rate (60%, or 62% with NI) and the pension contribution that brings income to £100,000.

- 주의: 마지막 구는 "adjusted net income"을 줄인 말이다. 화면 본문에는 반드시 "adjusted net income"이라고 쓴다(brief 9장 문장 그대로).

### 화면 문구
- H1: `60% tax trap calculator 2026/27`
- 결과 줄 3개: `Personal Allowance lost: £X` · `Effective marginal rate in this band: 60% (62% with NI)` · `Pension contributions that would reduce adjusted net income to £100,000: £Y`
- 바로 아래(필수, brief 9장): `This is arithmetic, not advice. Speak to a regulated adviser before changing contributions.`
- 쓰지 않는 말: escape, avoid, beat, should, we recommend, save (권유·과장).

## 3. 참고 — 수요가 아직 없는 것
- 롱테일 월 검색수: 확인 안 함(무료 공개 수치 못 받음). 자동완성에 "calculator"가 2위로 뜨는 것만 확인.
- "100k tax trap childcare"가 자동완성에 있다. 이 계산기는 보육 지원(Tax-Free Childcare 등) 상실을 계산하지 않으므로 title·description에 넣지 않는다. 본문에서 다룰지는 빌더·본부장 판단(원문 확인 필요).
