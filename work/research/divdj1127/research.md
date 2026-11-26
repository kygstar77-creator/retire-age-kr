# divdj1127 자료조사 (카페 11/27 18:40 배당 칸, firemap-write 11/26 07:1x 회차) — 미국배당다우존스(SCHD 지수) 국내 ETF 4곳 같은 날 1억, 직접 계산형(잘된 글 1위 ndxetf1122·k200etf1126 틀)

## 상태 (11/26 09:34)
- 09:2x 회차: 운용사 원문 4곳 중 3곳 공식(SOL·TIGER·KODEX)+ACE 2차 2곳 끝(S3~S6)
- 이번 회차에 한 것: 주제 검증(수요·겹침)·원자료 받기(fetch.py)·직접 계산(calc.py → calc_out.txt)
- 09:4x: toprank·bench.md 경쟁 5편·포화 끝(따라 한 것 표지·사진·끝맺음 칸과 사진 비교는 그림·조각 뒤)
- 남은 것(관문까지): bench 나머지 칸 · 질문 3개 주소 · 조각 c00~ · 그림 3장(mkimg.py) · readcheck·selfcheck·aitell spoken·crosscheck · 이해 2차 6명 · cover · editgate · slots.json gates_ok

## 검증
- 수요: kwvol 11/26 — TIGER미국배당다우존스 24,010 · KODEX미국배당다우존스 8,100 · SOL미국배당다우존스 7,800 · ACE미국배당다우존스 5,450 · 미국배당다우존스 4,220 (합 약 4만 9천)
- 우리 실측: 잘된 글 1위 ndxetf1122 '나스닥100 ETF 네 곳 수익 비교, 같은 날 샀다면' 27.7회/일(textrule 11/24) → 같은 틀을 k200etf1126(코스피200)에 이어 배당 ETF에
- 겹침: tigerdj1122(#477, 11/22) 'TIGER 미국배당다우존스 vs SCHD' — 본문에 SOL·ACE·KODEX 0번, 국내 네 곳 맞대기 아님. 다만 naverpost same_product_30d가 제목 속 'TIGER미국배당다우존스'를 #477과 겹침으로 잡으므로 **제목에 운용사 상표+상품명을 넣지 않는다**(예: '미국배당다우존스 ETF 네 곳, 같은 날 1억 넣었다면')
- 칸: 11/27 18:40 배당(회의 11/25 21:4x 배정, 관문 기한 11/27 12:40) · 같은 날 12:40 jepivix1127(JEPI) — 같은 상품 아님

## 원문
- S1 야후 파이낸스 chart API 일별 종가·분배 events 402970(ACE)·446720(SOL)·458730(TIGER)·489250(KODEX).KS, ~2026-11-25 종가, 11/26 07:2x 받음(raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/458730.KS
- S2 (2차) 네이버페이 증권 ETF 분석 4종 — 상장일 20211021·20221115·20230620·20240813, 기초지수 'Dow Jones U.S. Dividend 100 Price Return Index' 넷 다, totalFee 0.01·0.01·0.01·0.0099, 11/26 받음(raw/naver_etfan_*_1126.json): https://m.stock.naver.com/api/stock/458730/etfAnalysis
- S3 신한 SOL 공식 상품 페이지 — 총보수 연 0.01%(집합투자 0.003·AP/LP 0.001·신탁 0.003·일반사무 0.003), 분배 월 1회·지급 기준일 매월 마지막 영업일, 상장 2022.11.15, 11/26 09:27 받음(raw/sol_1126.html): https://www.soletf.com/ko/fund/etf/210942
- S4 미래에셋 TIGER 공식 상품 페이지 — 총보수 연 0.01%(운용 0.003·지정참가 0.001·신탁 0.003·일반사무 0.003), 지급기준일 매월 마지막 영업일·지급 익영업일부터 7영업일 안, 순자산 45,799억원, 상장 2023-06-20, 분배금 배당소득세 Min(현금분배금, 과표증분)×15.4%, 11/26 09:35 Playwright(raw/tiger_pw_1126.txt, fetch_pw.py): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009
- S5 삼성 KODEX 공식 상품 페이지 — 총보수 연 0.0099%('1억 투자 시 총보수 연간 9,900원'), 지급기준일 매월 15일(영업일 아니면 직전 영업일) '월중배당', 11/26 09:30 Playwright(raw/kodex_pw_1126.txt): https://www.samsungfund.com/etf/product/view.do?id=2ETFN9
- S6 (2차) funetf ACE 미국배당다우존스 — 총보수 연 0.0100%·순자산 9,959억원(11/25 기준)·최근 지급기준일 2026.11.13 24원·월중배당·상장 2021.10.21, 11/26 09:35(raw/ace_pw_1126.txt): https://www.funetf.co.kr/product/etf/view/KR7402970008 — 한투 공식 상품 페이지는 주소를 못 찾음(검색 페이지가 자바스크립트, /fund/<코드> 모름) → ACE 보수·기준일은 2차 2곳(S2 네이버·S6 funetf)으로만
- 기준일 갈래(직접 확인): 월말 기준 SOL·TIGER / 월중(15일 무렵) KODEX·ACE — 야후 분배 날짜도 같은 갈래(SOL·TIGER 7/30·8/28·9/29·10/29, ACE·KODEX 8/13·9/14·10/14·11/12)
- 세율 15.4%: k200etf1126 research.md S4·S5(소득세법 제129조·지방세법 제103조의13) — 발행 전 주소 다시 엶

## 우리만 (calc_out.txt, 11/25 종가)
- 네 곳 다 있는 2024-08-13(KODEX 상장일) 1억, 분배금 다시 삼(세전): KODEX 1억 3,748만 · TIGER 1억 3,681만 · ACE 1억 3,653만 · SOL 1억 3,645만 — 차이 103만원(세후 15.4% 101만원)
- 분배금 현금으로 받기: 받은 현금 KODEX 836만 · SOL 824만 · TIGER 814만 · ACE 803만
- 최근 1년(2025-11-25~) 차이 25만원 · 2026년(1/2~) 52만원
- 해마다 폭: 2024 0.45%p · 2025 0.83%p · 2026 0.50%p
- 가장 긴 ACE(2021-10-21 상장) 1억 → 1억 7,418만(분배 43번)
- 최근 1년 분배율 2.96~2.99% · 분배 기록 날짜가 ACE·KODEX는 달 중순(11/12), SOL·TIGER는 달 말(10/29) — 야후 events는 배당락 기준일 수 있어 운용사 원문으로 지급일 확인 필요(확인 안 함)

## 경쟁 · 질문 · 왜 · 그래서 · 누구라면 · 함정 · 한계 · 대조
- 확인 안 함 — 다음 회차(toprank '미국배당다우존스 ETF 비교' 8편, 지식iN·카페 질문 3개 주소)
- 한계(지금까지): 공통 기간이 2년 3개월뿐(KODEX 상장 2024-08) · 매매 수수료·호가 차이·팔 때 세금 뺌 · 총보수는 네이버 값(2차)만
