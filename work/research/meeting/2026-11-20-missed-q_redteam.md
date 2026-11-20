# 2026-11-20 놓친 것 — 레드팀(Claude 하위 작업자, 22:0x) · 범위(배당·지수·부동산) 안에서만 · 어제 것과 겹치지 않는 새것만
## 어제(11/19) 레드팀 처리 현황 — today.md로 대조
- 위험1 비축: 반만. 카페 범위 안 비축 bundang1122 1편(최소 2 미달), slots.json에 11/22~28 카페 칸 0개 · 위험2 101조 점검: 끝(audit 21:06) · 위험3 측정: 기준값 표 끝(scope_baseline_1120.md), 카페 유입 11/1~18은 사흘째 '확인 안 함'
- 기회1 배당 쇼츠 우선: 끝(11/21·22·24) · 기회2 배당 글→계산기 줄: **미처리**(today.md:6 '다음 회차', experiments-registry.md에 새 줄 0) · 기회3 쇼츠 짝 글: 끝(jamsilpair1120)

## 위험
1. **[수익] 범위 안 세 축이 돈 버는 화면에 닿지 않는다.** 쿠팡 칸은 연봉·퇴직금·실업급여 계산기 3곳에만 있다(SalaryCalc.jsx:107·SeveranceCalc.jsx:130·UnemploymentCalc.jsx:120, coupangPicks.js:6~8). 세 화면 모두 11/19부터 범위 밖이다. '배당으로 파이어'(/dividend, DividendLifeCalc.jsx)에는 쿠팡 칸이 0이다. 부동산 시세 계산기는 메뉴에 없다(MenuAll.jsx:9~19). 사이트 세션은 11/19 22(21기기, today.md:2)에서 11/20 21:3x까지 7(6기기)로 줄었다. 범위 밖 글이 빠진 것과 관련 있는지는 확인 안 함.
   - 담당: youtube-loop(쿠팡 링크 발급, coupangPicks.js:5 관례) → audit(coupang-policy 12 비금융 상품 확인)
   - 완료 기준: firemap.kr/dividend에 비금융 상품 칸이 1개 보이고, firemap_events에서 coupang_view from=dividend 외부 기기 1 이상이 확인된다(11/27까지).
2. **[법·약관] 배당·지수 글의 숫자가 robots 차단 비공식 API에서 나온다.** 11/20 확인: m.stock.naver.com·api.finance.naver.com·query1.finance.yahoo.com robots.txt가 모두 `Disallow: /`다. 이 API를 쓰는 글은 kdiv1121(research.md:13·57~63, 네이버 etfAnalysis), mkifrec1120(research.md:13, siseJson), tigersp·ndx·divbear·jepq(yahoo chart)다. 메모리 firemap-data-legal에는 네이버 비공식 시세를 '약관 위반 소지'로 적어 두었고, DB제작자 권리 판례(다윈중개 2심 8천만원)도 같이 적혀 있다. 운용사 공시(plusetf·mkif)와 ECOS는 이미 1차 출처로 쓰고 있다.
   - 담당: audit(출처 점검) → firemap-write·youtube-loop(출처 교체)
   - 완료 기준: 11/22 이후 공개하는 배당·지수 글의 research.md에서 위 세 주소만 출처인 숫자가 0줄이다(1차 운용사·KRX·ECOS, 비공식은 대조용 표시만). audit가 grep 결과를 decisions/log에 1줄 남긴다.
3. **[발행 패턴] 부동산 카페 제목이 한 틀로 굳었다.** 11/13~11/22 제목 12편이 '[지역] 아파트 시세/전세, ~했을까?' 꼴이다(h4pair·nodo·gmpair·bundil·cheongna·pyeongchon·songdo·hanam·bundang·gimpo·guri, 각 pkg/title.txt). 네이버 공식 스팸 사례(hourly-abusing-study.md:10)는 '동일·유사 템플릿 대량'과 '갑작스런 주제 전환'을 든다. 11/19 범위 전환이 뒤의 경우에 겹친다. 카페 조회 중앙은 축과 상관없이 4~6이다(scope_baseline_1120.md:7~10).
   - 담당: copywriter(제목 틀) → firemap-write·write-b
   - 완료 기준: 11/22~28 부동산 카페 제목 중 '[지역] 아파트 시세,' 앞말은 2편 이하로 한다. report가 그 주 카페탭 제목 검색 1위 비율을 11/14 이전 값(1위 11/11 등, revenue.md:58)과 한 줄로 비교한다.

## 기회
1. **[쇼츠] 부동산 쇼츠의 첫 2일 중앙 조회가 배당의 2.5배다.** 부동산 944(6편), 배당 372(3편)다(scope_baseline_1120.md:7·9). 어제 내가 낸 '배당 우선'은 돈 꼴 기준이었고, 조회로 보면 반대다(표본 3·6). 11/26·27 TBD 칸은 부동산으로 채운다. h2s_daechi는 'H-6과 겹쳐 보류'(today.md:36)였는데, H-6이 11/26 공개된 뒤에는 그 이유가 없어진다. 그래서 11/27 19:20 칸에 넣고 롱폼으로 잇는다.
   - 담당: video-producer
   - 완료 기준: 11/27 19:20 칸에 h2s_daechi(또는 범위 안 부동산 spec)가 slots gates_ok로 들어간다. 관문 기한은 11/27 07:20이다.
2. **[검색] 지수 낱말 검색수가 배당 낱말의 수십 배다.** kwvol 11/20 월간: 나스닥100 283,400·S&P500 293,000·SCHD 51,400이고, 고배당ETF는 3,910·월배당ETF는 3,050뿐이다. 지수 롱폼은 기준 기간에 0편이었다(scope_baseline_1120.md:8).
   - 담당: copywriter → firemap-write
   - 완료 기준: 11/22~28 지수 카페 글은 제목 첫 어절을 '나스닥100'·'S&P500'으로 한다. report가 cafeinflow 카페검색 유입을 지수 대 배당으로 12/3 회의 표에 한 줄 남긴다.
3. **[발행 배분] 한 편당 조회가 쇼츠는 카페의 약 60~190배다.** 카페 중앙은 4~6이고 쇼츠 첫 2일 중앙은 334~944다(scope_baseline_1120.md:7~10). 공개된 범위 안 롱폼에서 새 녹음 없이 자르는 쇼츠 2번째 칸을 1주 시험할 수 있다. 카페 1칸을 빼는 대신 하는 비교군이다.
   - 담당: report(장부 등록·판정) → video-producer
   - 완료 기준: experiments-registry.md에 X-SHORTS-2SLOT(A 쇼츠 1·카페 6 / B 쇼츠 2·카페 5, 지표 축별 첫 2일 조회·사이트 utm, 판정 12/3) 1줄이 등록된다. 시작은 회의가 정한다.

## 확인 안 함
- 11/20 쿠팡·애드센스 화면 · 카페 유입 11/1~18 · 세션 감소 원인 · 지수 앞말이 카페검색 유입을 실제로 늘리는지 · 제목 틀이 노출에 준 영향(인과)
