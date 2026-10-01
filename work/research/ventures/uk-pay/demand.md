# UK 실수령 계산기 수요 실측 (2026-10-01 KST 09:45~09:52)

측정 위치: 한국 IP(PC). 로그인·계정 생성 없음. 추정치 없음, 화면에 뜬 값만 적음.

## A. 월 검색량

### A-1. WordStream 무료 키워드 도구 (Google Ads 데이터, 국가=United Kingdom, 이메일 입력 없이 표시됨)
출처: https://tools.wordstream.com/fkt (국가 드롭다운 United Kingdom 선택 확인 후 검색)

| 키워드 | 월 검색량(UK) | 확인 시각(KST) | 비고 |
|---|---|---|---|
| 60% tax trap calculator | 170 | 09:47 | "%"를 빼고 "60 tax trap calculator"로 합쳐서 나옴 |
| 60 tax trap calculator | 170 | 09:46 | 경쟁도 Low, 입찰가 표시 없음 |
| 100k tax trap | 1,600 | 09:48 | 입찰가 $0.41~$2.60, Low. 연관: "tax trap 100k" 110, "tax trap over 100k" 90 |
| 100k tax trap calculator | 30 | 09:49 | |
| personal allowance taper calculator | 20 | 09:49 | |
| hicbc calculator | 390 | 09:50 | |
| child benefit tax charge calculator | 확인 안 함 | 09:50 | "No Results" 표시. 같은 화면에서 "child benefit tax charge", "high income child benefit charge"도 No Results. 원인은 확인 안 함 |
| (참고) 60% tax trap | 1,300 | 09:51 | 연관: "60 percent tax trap" 90, "60 tax trap explained" 90, "avoid 60 tax trap" 40, "avoiding the 60 tax trap" 10 |
| (참고 기준) take home pay calculator | 301,000 | 09:52 | 입찰가 $0.46~$5.58. 동의어 묶음(bring home pay calculator 등)이 모두 같은 301,000으로 나옴 = Google Ads 묶음값 |

주의: Google Ads(키워드 플래너) 계열 값은 반올림된 구간 대표값이고 동의어를 묶는다. 입찰가 통화는 화면에 $로 표시됨.

### A-2. 다른 출처 시도 결과
- Ahrefs Keyword Generator (https://ahrefs.com/keyword-generator/?country=gb): 확인 안 함 — "Find keywords" 누르자 Cloudflare 사람 확인 체크박스가 뜸. 규칙대로 거기서 중단.
- keywordtool.io (https://keywordtool.io/google): 확인 안 함 — 무료판은 검색량 칸이 전부 "88,888" 자리표시로 가려지고 "Unlock All Metrics" 유료 안내. 키워드 목록만 받음.
- Semrush: 시도 안 함(키워드 조회는 로그인 필요, 로그인 금지 조건).

### A-3. Google Trends (UK, 지난 12개월, 주별, 상대값 0~100)
출처: https://trends.google.com/trends/explore?date=today%2012-m&geo=GB&q=... (화면 그래프가 안 그려져서 같은 페이지에서 Trends 내부 API 응답을 직접 읽음)

비교 1: "60% tax trap" / "child benefit tax charge" / "100k tax trap"
- 12개월 평균: 1 / 32 / 9
- "60% tax trap"은 53주 중 대부분 0(표본 미달). 최근 3주(9/13~10/3)에만 4·11·8.
- "child benefit tax charge" 최고 100 = 2025-11-23~29 주.

비교 2(기준어 포함): "take home pay calculator" / "child benefit tax charge" / "60 tax trap" / "hicbc" / "tax trap"
- 평균: 71 / 1 / 0 / 1 / 5 · 0이 아닌 주 수: 53 / 33 / 4 / 15 / 53

비교 3: "60 tax trap" / "100k tax trap" / "personal allowance taper" / "hicbc" / "60 tax trap calculator"
- 평균: 3 / 11 / 3 / 17 / 0 · 0이 아닌 주 수: 7 / 13 / 7 / 15 / 0

읽는 법: 이 키워드들은 "take home pay calculator" 대비 1% 안팎 이하라 Trends에서는 대부분 0으로 잘린다. Trends로는 이 키워드들끼리 순위를 가리기 어렵다.

### A-4. Google 자동완성 (UK, hl=en-GB, gl=gb) 09:45
출처: https://suggestqueries.google.com/complete/search?client=firefox&hl=en-GB&gl=gb&q=...
- "60% tax trap" → 2번째 제안이 "60 tax trap calculator". 그 밖에 explained, uk, scotland, how to avoid, money saving expert, graph, reddit, example
- "100k tax trap" → money saving expert, uk, childcare, explained, reddit, **calculator**, graph, scotland
- "personal allowance taper" → uk, **calculator**, over 100k, threshold, pension contributions, scotland, 2025 26
- "hicbc calculator" → gov uk, hmrc, tax calculator, charge calculator, child benefit hicbc calculator, 2024 25 calculator
- "child benefit tax charge calculator" → gov uk, formula, higher tax charge calculator, hmrc, high income
- "take home pay calculator" → uk, scotland (이하 타국)

## B. 체크리스트 15번: Google이 결과 화면에서 직접 계산해 주는가

방법: curl(모바일 UA)은 3개 검색어 모두 JS 필요 페이지(enablejs)만 받아 실패 → 내장 브라우저로 google.co.uk(hl=en-GB, gl=gb) 직접 열어 확인. 09:46~09:47 KST. 한국 IP라 영국 현지 화면과 다를 수 있음. Bing 대체 확인은 Google에서 화면을 얻어서 하지 않음.

| 검색어 | Google 자체 계산기 위젯 | AI Overview | 1위 일반 결과 |
|---|---|---|---|
| take home pay calculator uk | 없음 | 있음. 숫자 계산 없이 계산기 사이트로 안내: "the official GOV.UK Income Tax Estimator" (GOV.UK·The Salary Calculator 인용) | reed.co.uk "Tax Calculator for £997k" (그 다음 moneyguide.org.uk, takehomepay.uk 등) |
| £60,000 after tax uk | 없음 | 있음. **숫자를 직접 답함**: "your net take-home pay is approximately £45,357 per year" + 월 £3,780·주 £872·세금 내역 (payclear/payprecision·Reed 인용) | salaryhub.co.uk "£60,000 Income Tax Calculator UK" (다음 payclear.co.uk) |
| 60% tax trap calculator | 없음 | 있음. 숫자 계산 없이 개념 설명 + 계산기 추천: "using the UK Tax Trap Calculator" (taxtrapcalculator.co.uk 인용) | apps.apple.com "60% Tax Trap UK: Pension Calc" 앱 (다음 convertsheet.com, infycalculator.com, uktaxdrag.co.uk, fableworkshq.com, 100grandcatch.uk 등) |

판정:
- Google 자체 계산기 위젯(입력칸이 있는 상자)은 세 검색어 모두 없음.
- "금액 + after tax" 같은 단일 금액 질문은 AI Overview가 숫자를 바로 답해 클릭이 줄어들 수 있음.
- "calculator"·"60% tax trap" 질문은 AI Overview가 숫자 대신 외부 계산기로 보냄 → 계산기 사이트에 클릭 여지 있음. 단 이미 계산기 사이트·앱이 1페이지에 6개 이상.
