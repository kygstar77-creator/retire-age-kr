# 해외(영어권 중심) 금융 계산기 사이트 시장 조사 — 원자료

조사일: 2026-10-01. 조사 도구: WebSearch, WebFetch, curl(ads.txt).
원칙: 숫자마다 출처 URL. 확인 못 한 것은 "확인 안 함".

주의 1. WebSearch 결과는 구글 실제 순위가 아니다. 미국 기준 검색 엔진 결과다. 아래 "상위 5"는 그 결과 순서다. 구글 SERP 순위는 확인 안 함.
주의 2. WebFetch는 JS로 뜨는 광고를 못 본다. 그래서 광고 여부는 각 사이트 ads.txt로 확인했다(curl, 2026-10-01).
주의 3. Similarweb·Semrush 방문수는 추정치다. 실측 아님.

---

## 1. 경쟁 사이트

### 1-1. 검색어별 상위 5 (WebSearch 결과 순서)

- "FIRE calculator": playingwithfire.co / engaging-data.com / theficalculator.com / investingfire.com / myfinancialfreedomtracker.com (6위부터 fire-calculator.xyz, nerdwallet)
- "take home pay calculator UK": tembomoney.com / taxd.co.uk / thesalarycalculator.co.uk / takehomepaycalculator.co.uk / calculatemysalary.co.uk
- "paycheck calculator"(미국): gusto.com / quickbooks.intuit.com / rollbyadp.com / adp.com(주별) / adp.com(주별). calculator.net은 7위
- "retirement calculator": prudential.com / edwardjones.com / boldin.com / money.usnews.com / fisherinvestments.com. nerdwallet, schwab, aarp, calculator.net도 결과에 있음
- "coast FIRE calculator": 앱스토어 앱 / get.pelcro.com / nickwolny.com / coastfirecalculator.co / theworkcave.com. 두 번째 검색에서는 walletburst.com이 1위로 나옴
- "severance pay calculator": x0pa.com / timetrex.com / unitedbenefits.com / simpleseverance.co / fedtools.com

관찰:
- paycheck·retirement는 급여대행사(Gusto, ADP, QuickBooks)와 금융사(Prudential, Schwab, Edward Jones)가 차지한다. 개인이 뚫기 어렵다.
- FIRE·coast FIRE는 개인·소규모 사이트가 많다. 2025~26년에 생긴 듯한 신규 도메인도 많다(coastfirecalculator.co, .app, .net, coastfire.org 등). 경쟁이 빠르게 늘고 있다.
- severance(퇴직금)는 미국에 법정 퇴직금이 없어 "추정" 계산기뿐이다. 한국 퇴직금 같은 법정 공식이 없다. 연방공무원용(fedtools)만 공식 규정 기반이다.

### 1-2. 사이트별 상세

| 사이트 | 하는 일 | 수익 모델(확인된 것) | 트래픽(추정, 2026-08) | 약점 |
|---|---|---|---|---|
| calculator.net | 계산기 수백 개 종합 | ads.txt에 google.com DIRECT 2개 + pubmatic·rubicon 등(광고) | 월 5,976만 방문, 오가닉 3,805만, 미국 50.21% | 금융 전용 아님, 디자인 오래됨(주관) |
| omnicalculator.com | 계산기 3,000개 이상 | ads.txt manager=ascendeum.com. 구글 사례글: Playwire·Google Ad Manager, 광고만 | 월 1,442만 방문, 미국 44.39% | 계산기당 깊이 얕음(주관) |
| smartasset.com 급여 계산기 | 미국 연방·주·지방세 반영 실수령액, 50개 주+DC 별도 페이지 | 재무설계사 매칭(리드젠), 예금 상품 비교 | 사이트 월 526만, "paycheck calculator" 2위 | 입력 칸 많음 |
| thesalarycalculator.co.uk | 영국 실수령액(세금·NI·학자금·연금, 2022/23~2026/27) | ads.txt manager=clickio.com(광고), 598줄 | 월 230만(8월), 오가닉 65.2만, 영국 83.22% | 입력 칸 과다, 화면 복잡 |
| listentotaxman.com | 영국 급여 세금 계산 | ads.txt manager=publift.com(광고), 959줄 | 확인 안 함(Semrush 404) | 확인 안 함 |
| walletburst.com | Coast/Barista/Fat FIRE 계산기 | ads.txt Mediavine(광고) + Personal Capital 제휴 배너 + 구글시트 툴킷 $20 판매 | 3개월 25.7만 방문, 미국 74.87%, 오가닉 70.15% | 몬테카를로 없음, 세금 없음, 저장·공유 없음, 미국 가정 |
| engaging-data.com | FIRE 계산기(고정수익·역사·몬테카를로), 시나리오 URL 공유 | ads.txt에 google.com DIRECT 1줄만(애드센스 계정만 등록). 페이지에 광고 안 보임 | 3개월 38.46만 방문, 미국 42.82%, 영국 13.99% | 연금·사회보장 입력 없음, 은퇴 후 인출 따로 |
| networthify.com | 저축률 기반 은퇴까지 연수 | 광고·제휴 안 보임, ads.txt 없음 | 3개월 15.11만 방문, 미국 59.73% | 변동성·인플레 없음, 2012년식 단순 모델 |
| ficalc.app | 역사 데이터로 인출 전략 백테스트 | 기부 | 3개월 9.63만 방문, 미국 78.15% | 초보자에게 어려움 |

출처:
- calculator.net Semrush: https://www.semrush.com/website/calculator.net/overview/ (월 5,976만, 오가닉 3,805만, 키워드 calculator 2,490만 등)
- calculator.net Similarweb: https://www.similarweb.com/website/calculator.net/ (국가 비중, 오가닉 74.37% 데스크톱)
- calculator.net 광고수익 추정 월 $25,144: siteworthtraffic 추정. 공식 수치 아님. 너무 낮아 보이며 신뢰 낮음. https://www.siteworthtraffic.com/report/calculator.net (검색 요약으로만 봄, 직접 확인 안 함)
- omnicalculator Semrush: https://www.semrush.com/website/omnicalculator.com/overview/
- omnicalculator 구글 사례: https://www.google.com/ads/publisher/stories/omni_calculator/ ("2023년 2억 방문", 직원 70명, 광고만)
- omnicalculator 매출: 공식 공개 없음. growjo 추정 연 $4.2M 등 추정만 있음(확인 안 함). https://growjo.com/company/Omni_Calculator
- smartasset: https://www.semrush.com/website/smartasset.com/overview/ , 페이지 https://smartasset.com/taxes/paycheck-calculator
- thesalarycalculator: https://www.semrush.com/website/thesalarycalculator.co.uk/overview/ , 페이지 https://www.thesalarycalculator.co.uk/salary.php
- walletburst: https://www.similarweb.com/website/walletburst.com/ , https://walletburst.com/tools/coast-fire-calc/
- engaging-data: https://www.similarweb.com/website/engaging-data.com/ , https://engaging-data.com/fire-calculator/
- networthify: https://www.similarweb.com/website/networthify.com/ , https://networthify.com/calculator/earlyretirement
- ficalc: https://www.similarweb.com/website/ficalc.app/ , https://ficalc.app/
- ads.txt: 각 도메인 /ads.txt 직접 받음(2026-10-01)

자기 공개 수익 보고서(income report): 위 사이트 중 찾은 것 없음. 확인 안 함.

### 1-3. 신규 진입자가 이길 수 있는 틈
- FIRE 계열: 소규모 사이트는 대부분 한 가지 계산만 한다. 몬테카를로·세금·저장/공유를 한 화면에 합친 곳이 드물다(walletburst는 없음, engaging-data는 있지만 광고 수익화 안 함).
- 국가별: FIRE 계산기는 거의 미국 가정이다(사회보장, 401k). 영국·캐나다·호주 연금·세금 반영 FIRE 계산기는 이번 조사에서 확인 안 함 — 틈일 가능성, 검증 필요.
- 급여 계산기(미국·영국): 대기업·기존 강자 점유. 영국 thesalarycalculator는 권위점수 53인데 "take home pay calculator"(30.1만) 1위다. 화면이 복잡해 UX로 붙어볼 여지는 있다. 다만 1위 탈환 가능성은 확인 안 함.
- 퇴직금(severance): 미국은 법정 공식이 없어 한국식 계산기 수요 구조와 다르다.

---

## 2. 광고 단가(RPM)

| 구분 | 수치 | 출처·날짜 |
|---|---|---|
| Ezoic EPMV 국가별 | 미국 $16.31, 캐나다 $18.25, 영국 $14.24, 호주 $16.31. 한국·일본 없음 | https://www.repmv.com/en/blog-ezoic-geo-location-epmv (데이터 2020-10-01~2021-09-30, 전 분야) |
| 애드센스 vs Ezoic 언어별 | 영어 애드센스 RPM 약 $2, Ezoic 약 $6. 한국어·일본어 Ezoic 약 $2 | https://www.ybierling.com/en/blog-marketing-adsense-cpm-rates-by-country (개인 블로그 실측, 날짜 범위 불명확) |
| 애드센스 CPM 국가별 | 호주 6.15, 미국 5.33, 캐나다 4.64, 영국 4.59 | 위와 같은 URL |
| 일본 애드센스 금융 RPM | 2,877엔(최저 도서 248엔, 11.6배) | https://www.adminweb.jp/blog/2022021201/ (2022-02, 구글 수익 계산기, 월 5만PV, 아시아태평양, $1=115엔) |
| 금융 블로그 Mediavine | $25~60(2026-04 기준이라 주장) | https://roipad.com/product-analysis/business-and-saas/average-rpm-mediavine-finance-niche-2026-performance-guide (2차 자료, 원자료 확인 안 함) |
| 금융 블로그 전반 | 세션당 RPM $15~40, 상위 $55+ | https://toolsignal.site/articles/blog-display-ad-rpm-by-niche-2026 (2차 자료, 확인 안 함) |
| 유튜브 RPM(참고, 웹 아님) | 미국 $5.58, 일본 $3.01, 한국 $2.58 | https://dynamoi.com/data/youtube-adsense-rpm (2026) |
| 한국 웹 애드센스 금융 RPM | 공신력 있는 수치 못 찾음. 확인 안 함 | — |

- 구글 애드센스 공식 수익 계산기: https://adsense.google.com/start/ 에 있음. 카테고리·지역 선택형. fetch로는 숫자를 못 뽑음. 확인 안 함.
- 광고 대행사 가입 조건: Mediavine 월 5만 세션, Raptive 월 10만 PV(2차 자료 요약). https://bloggingexplorer.com/best-ad-networks-for-bloggers/ — 원문 확인 안 함.
- 실제 계산기 사이트 사례: walletburst는 Mediavine, thesalarycalculator는 Clickio, listentotaxman은 Publift, omni는 Ascendeum 관리(ads.txt 확인). 즉 애드센스 단독보다 대행사를 쓴다.

해석(추정 표시): 영어권 금융 트래픽 RPM은 한국어 대비 수 배로 보인다. 다만 같은 조건 비교 자료는 없다. 정확한 배수는 확인 안 함.

---

## 3. 검색 수요(월간 검색량)

| 검색어 | 월 검색량 | 출처 |
|---|---|---|
| paycheck calculator | 378,000 (KD 72, 트래픽 잠재 991,000) | Ahrefs 블로그 2026-07-16 https://ahrefs.com/blog/the-free-tools-seo-strategy/ |
| paycheck calculator | 450,000 (smartasset 2위) | Semrush 2026-08 https://www.semrush.com/website/smartasset.com/overview/ |
| retirement calculator | 1,500,000 (nerdwallet 1위) | Semrush 2026-08 https://www.semrush.com/website/nerdwallet.com/overview/ |
| take home pay calculator | 301,000 (thesalarycalculator 1위) | Semrush 2026-08 https://www.semrush.com/website/thesalarycalculator.co.uk/overview/ |
| salary calculator uk | 90,500 | 위와 같음 |
| take home pay calculator uk | 40,500 | 위와 같음 |
| salary calculator | 368,000(영국 DB 추정) / 201,000(미국 DB 추정) | 위 두 Semrush 페이지 |
| salary to hourly calculator | 42,000 | Ahrefs 블로그 위 URL |
| retirement planning calculators | 27,100 (CPC $2.30) | https://www.kwrds.ai/top-keywords/Retirement-Planning (2026-09) |
| fire calculator | 확인 안 함 | 무료 페이지에서 수치 못 찾음. CPC만 $1.81(Similarweb) |
| coast fire calculator | 확인 안 함 | walletburst 최상위 유입어인 것만 확인 |

- 참고 트래픽: smartasset 급여 계산기 월 69만 오가닉(Ahrefs, 2024-12-30) https://ahrefs.com/blog/website-calculators/ . Gusto 급여 계산기 월 1.78만(Ahrefs 2026-07).
- Google Trends: trends.google.com fetch 시 HTTP 429. 확인 안 함.
- 규모 감: FIRE 계산기 전문 사이트 방문수(walletburst 3개월 25.7만, networthify 15.1만, ficalc 9.6만)로 보아 FIRE 키워드는 급여·은퇴 계산기보다 한 자릿수 이상 작다고 추정. 정확한 검색량은 확인 안 함.

---

## 4. 해외 제휴(어필리에이트) — 한국 거주 1인 운영자 기준

| 프로그램 | 보수 | 한국 거주자 조건 | 출처 |
|---|---|---|---|
| Amazon Associates(미국) | 종이책 4.5%, 킨들·에코 기기 4%, PC 2.5%, TV 2%, 킨들 구독 0% | 비미국인은 세금 인터뷰(W-8BEN) 필수. 조약 혜택 없으면 최대 30% 원천징수. "미국 밖에서만 활동하면 미국 원천소득 아님" 취지 안내 있음. 현지 은행 송금 지원 | 요율 https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ (적용일 표기 없음) / 세금 https://affiliate-program.amazon.com/help/node/topic/GYJB2LE2AB473W2L / 송금 https://affiliate-program.amazon.com/resource-center/receive-your-international-affiliate-earnings-in-your-local-bank |
| Wise | 개인 £10, 사업자 £50 (첫 환전 거래 시, 쿠키 1년) | Partnerize로 GBP·USD·EUR·AUD·JPY 계좌 지급. KRW 계좌 없음 → 외화계좌 필요. 브랜드 키워드 광고·쿠폰사이트 금지 | https://wise.com/gb/blog/affiliate-onboarding-guide |
| Revolut | 개인 £2~20, 사업자 최대 £500, 국가별 상이, 요율 비공개 | Impact 경유. 한국 거주자 가입 가능 여부 확인 안 함 | https://www.revolut.com/affiliate-onboarding-guide/ (2차 요약 https://uppromote.com/affiliate-directory/revolut/) |
| YNAB | 무료체험 1건 $6(월 100건 이상 $8, 200건 이상 $10), 쿠키 30일 | 확인 안 함 | https://getlasso.co/affiliate/ynab/ (2차, 원문 403으로 확인 안 함) |
| Empower(구 Personal Capital) | 적격 리드당 최대 $250. 조건: 자산 $10만 이상 연결 | Impact 경유. 국가 제한 명시 없음. 이해상충 공시 의무 | https://www.empower.com/affiliates |
| Monarch Money | 유료 구독당 $20이라는 2차 자료 + "비활성" 주장 공존 | 확인 안 함 | https://linkclicky.com/affiliate-program/monarch-money/ (확인 안 함) |

법적 위험:
- 영국: FSMA s21. 비인가자가 규제 대상 금융상품을 인가자 승인 없이 홍보하면 형사 범죄가 될 수 있다(인플루언서 사례). 2024-02-07부터 승인 게이트웨이 시행. https://www.fca.org.uk/publication/finalised-guidance/fg24-1.pdf , https://www.fca.org.uk/firms/financial-promotions-and-adverts/approving-financial-promotions (검색 요약 기준, PDF 원문 정독은 안 함)
- 미국: Empower 페이지가 이해상충 공시를 요구. FTC 공시 규정 원문은 이번에 확인 안 함.
- 투자 자문 등록: 계산기가 "개인 맞춤 추천"을 하면 문제될 수 있다는 점은 확인 안 함. 법률 검토 필요.
- 한국 측 세금(해외 제휴 수익 신고)은 확인 안 함.
- 안전한 순서(추정): 도서·예산앱처럼 금융상품 아닌 것부터. 증권·예금·송금 상품 홍보는 영국 트래픽에 특히 위험.

---

## 5. 일본 시장 간단 확인

- "FIRE シミュレーション" 상위(WebSearch 순서): calculator.jp/media / note.com / ma-la.co.jp / plays-inc.jp / studyfire.jp. 전용 도메인 fire-simulator.net, money-keisan.com 도 있음.
- "手取り 計算" 상위: smbc-card.com / mynavi-agent.jp / musashi-corporation.com / doda.jp / moneypro.jp. 카드사·채용사가 강하다(미국 급여대행사 구도와 비슷).
- 일본 검색량: 확인 안 함(무료 페이지에서 못 찾음. keisan.casio.jp Semrush 404).
- 일본 금융 RPM: 2,877엔(2022-02, 구글 계산기 기준) https://www.adminweb.jp/blog/2022021201/
- 언어 장벽: 일본어 문구를 우리가 검증할 수단이 약하다(주관).

---

## 요약용 핵심 수치
1. 검색량: retirement calculator 150만, paycheck calculator 37.8만~45만, take home pay calculator 30.1만, salary calculator uk 9.05만. fire·coast fire 검색량은 확인 안 함.
2. 강자: 급여·은퇴는 대기업(ADP, Gusto, NerdWallet, SmartAsset, 금융사). FIRE는 소규모 개인 사이트 다수.
3. FIRE 전문 사이트 트래픽은 3개월 10만~40만 방문 수준(Similarweb 추정).
4. 계산기 사이트 수익원은 광고 대행사(Mediavine, Clickio, Publift, Ascendeum)와 리드젠(SmartAsset).
5. 영어권 EPMV $14~18(Ezoic, 2020~21). 한국 금융 웹 RPM 공신력 수치는 확인 안 함.
