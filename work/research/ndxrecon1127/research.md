# ndxrecon1127 자료조사 (카페 11/27 16:10 지수 칸, firemap-write-b 11/26 13:4x 회차) — 나스닥100 12월 정기 교체·올해 바뀐 규칙, 원문 정리형(form 1)

## 검증
- 수요: kwvol 11/26 — 나스닥100지수 6,630 · 나스닥100종목 880 · 코스피200편입 440(참고) · 나스닥100편입 15 · 나스닥100리밸런싱 10 → 검색어는 '나스닥100 종목'을 제목 앞에
- 경쟁에서 터진 증거: toprank '나스닥100 편입 종목 변경' 상위 8편 중 2편이 오늘(11/26)·5편이 1주 안(앤트로픽 상장·빠른 편입·12월 정기변경) — 지금 쓰이는 주제
- 우리 실측: textrule 주제축 종목(지수) 1위(k200etf1126 메모) · 우리 글 중 12월 교체·규칙 변경을 다룬 글 0편
- 겹침: ndx1121(하락장)·santa1123(12월 수익)·ndxetf1122(국내 ETF 4곳)·lev1125(레버리지) — 지수 명단 교체는 0편 · 11/27 10:10 dow1124는 다우 가격가중 비중(다른 지수·다른 질문)
- 칸: 11/27 16:10 지수(같은 날 07:40 과천 부동산·10:10 dow 지수·12:40 jepivix 배당 → 18:40 divdj 배당·22:40 부동산, 같은 축 3연속 아님) · 관문 기한 11/27 10:10

## 원문
- S1 나스닥 'Annual Changes to the Nasdaq-100 Index' 발표문 2019~2025 7건(raw/pr2019~2025.html, 11/26 받음): https://www.nasdaq.com/press-release/annual-changes-nasdaq-100-indexr-2025-12-13 · https://www.nasdaq.com/press-release/annual-changes-nasdaq-100-indexr-2024-12-13 · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-indexr-2023-12-08 · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2022-12-09 · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-indexr-2021-12-10 · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2020-12-11 · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2019-12-13
- S2 나스닥 Global Indexes '2025 Nasdaq-100 Reconstitution and Performance Highlights'(2026년 1월, raw/hl202601.pdf): https://indexes.nasdaqomx.com/docs/202601%20NDX%20Reconstitution%20and%20Performance%20Highlights.pdf
- S3 나스닥 'Nasdaq-100 Index Methodology Changes FAQ'(2026년 5월, raw/2026_May_NDX_Changes_FAQ.pdf): https://indexes.nasdaqomx.com/docs/2026_May_NDX_Changes_FAQ.pdf
- S4 나스닥 'Methodology Change Log NDX'(raw/Methodology_Change_Log_NDX.pdf): https://indexes.nasdaqomx.com/docs/Methodology_Change_Log_NDX.pdf
- S5 나스닥 'Consultation February 2026 Summary of Responses and Conclusion'(raw/…Conclusion.pdf): https://indexes.nasdaqomx.com/docs/Nasdaq-100_Index_Consultation_February_2026_Summary_of_Responses_and_Conclusion.pdf
- S6 (2차①) 'Nasdaq-100 Index June 2026 Quarterly Changes' GlobeNewswire 사본(raw/jun_finviz.html): https://finviz.com/news/361357/nasdaq-100-index-june-2026-quarterly-changes
- S7 (2차②) 같은 발표 사본(raw/jun_mondo.html): https://mondovisione.com/news/nasdaq-100-index-june-2026-quarterly-changes-2026612/
- S8 (2차③) 알자지라 2026-07-07 스페이스X 편입: https://aljazeera.com/economy/2026/7/7/spacex-shares-slide-as-it-joins-the-tech-heavy-nasdaq-100
- S9 (2차④) RTTNews 스페이스X 상장 한 달 안 편입: https://www.rttnews.com/3663388/spacex-joins-nasdaq-100-less-than-a-month-after-going-public.aspx?type=ipo
- S10 미래에셋자산운용 TIGER 미국나스닥100 상품 정보(벤치마크 NASDAQ 100, raw/tiger_133690_1126.html): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008
- S11 S1로 직접 센 것(count.py → count_out.txt): 해마다 넣은·뺀 수, 들고 난 회사, 발표·적용 요일, 2026년 12월 금요일

## 경쟁
- toprank.txt('나스닥100 편입 종목 변경' 블로그 상위 8, 11/26) · bench_raw 5편. 1(cclchero) 편입 뉴스 보고 사면 오르나·상장과 편입 차이, 2(whitecoffee0528) 5월 규칙 변경 Q&A·스페이스X·S&P500과 차이, 8(sovbks) 12월 정기변경 일정·선물 만기·빅테크 쏠림, 3·7 앤트로픽 편입 조건. 7년 발표문을 모아 해마다 개수·들고 난 회사를 센 글 0편 → bench.md

## 질문
1. 내 ETF에 새 회사가 들어오기까지 얼마나 걸리나 — https://blog.naver.com/whitecoffee0528/224471178677 ('내 ETF 안에 새 회사가 들어오기까지 얼마나 걸릴까요?') → 답: 12월 정기 교체가 기본, 5/1부터 상위 40위 새 상장사는 15거래일, 스페이스X 6/12→7/7
2. 12월 정기변경은 언제 어떻게 하나 — https://blog.naver.com/sovbks/224479233534 ('12월 정기변경은 언제 어떻게 이뤄지는지') → 답: 둘째 금요일 발표·셋째 금요일 다음 월요일 적용(7번 모두), 올해 11일·21일
3. 편입되면 주가가 오르나 — https://blog.naver.com/cclchero/224483668276 ('편입 소식을 듣고 매수하면 주가는 계속 오를까요?') → 답: 예측은 안 함. 들어온 회사는 이미 그해 50% 넘게 오른 뒤였다는 나스닥 자료만
4. 해마다 몇 개나 바뀌나 — https://blog.naver.com/sovbks/224479233534 ('어떤 기업이 남고 어떤 기업이 새로 들어오는지') → 답: 7년 39개, 2024년만 3개

## 왜
- 왜 12월인가: 분기 만기일(쿼드러플 위칭, 셋째 금요일)에 맞춘다고 발표문에 적힘(S1)
- 왜 들고 나나: 101~125위 기존 회사는 자리가 남을 때만 남는 규칙(S2) — 100위 언저리는 그해 시가총액에 따라 갈림
- 왜 규칙을 바꿨나: 비상장으로 오래 머물다 크게 상장하는 회사가 늘어 큰 신규 상장사를 빨리 담으려고(S3 'Private companies are remaining private for longer periods')
- 왜 2024년만 3개인가: 원문에 이유 없음 — 글에서 이유를 쓰지 않음

## 그래서
- ETF를 들고 있으면 따로 할 일 없음(QQQ는 지수 성과를 따르는 것이 목표 S1, 국내 TIGER도 벤치마크 NASDAQ 100 S10) — 날짜만 알아 두면 됨
- 새로 들어온 회사 몫은 작음: 상위 10개가 52%(S2)

## 누구라면
- QQQ·QQQM 같은 미국 상장 ETF를 모으는 사람: 미국 시각 12/11 발표, 12/21 적용
- 국내 나스닥100 ETF(연금저축·ISA 포함)를 모으는 사람: 같은 지수라 같은 명단, 한국 시각 12일 토요일 오전에 발표 확인
- 편입 뉴스를 보고 개별 종목을 사려는 사람: 편입 전 이미 그해 50% 넘게 오른 회사였다는 사실(S2)만 — 권유 없음

## 함정
- '편입 = 주가 상승'으로 읽기 — 나스닥 자료로는 들어온 회사는 편입 전에 이미 많이 오른 회사였음, 반대로 반년 만에 빠진 인스메드
- 12월만 바뀐다고 알기 — 올해부터 3·6·9월 분기 심사·빠른 편입이 생김

## 한계
- 2018년 이전 발표문은 이 글에서 세지 않음(나스닥 '지난 10년 보통 6개' 문장으로 대신)
- 수시 교체(인수·합병·0.10% 비중 미달)는 해마다 개수에서 뺌 — 나스닥 '지난 10년 연 3개쯤' 문장만 있고 해마다 수는 원문으로 못 셈
- 9월 분기 심사 발표문은 못 찾음(나스닥 IR 403·검색 안 나옴) — 글에서 9월 결과를 쓰지 않음
- 스페이스X 편입일은 나스닥 원문 못 열어 2차 보도 2곳으로 씀
- 올해 12월 날짜는 지난 7번 규칙으로 센 예상 — 글에 그렇게 밝힘

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 7년 39개 · 2024년만 3개, 나머지 6개 | six×6·three×1 = 39 | S1 7건 · S11 count_out.txt |
| 둘째 금요일 발표·셋째 금요일 다음 월요일 적용(7번 모두) | Dec 13/23 2019 … Dec 12/22 2025 | S1 · S11 |
| 12월 11일 금요일 발표·21일 월요일 적용(예상) · 한국 12일 토요일 오전 | 2026-12 금요일 4·11·18 · 'Dec 12, 2025 8:00pm EST' | S11 · S1 |
| 네 단계(75·100위·101~125위·새 회사) · 최근 5년 91.6% | 'top 75'·'top 100'·'101–125'·'91.6%' | S2 https://indexes.nasdaqomx.com/docs/202601%20NDX%20Reconstitution%20and%20Performance%20Highlights.pdf |
| 지난 10년 12월 보통 6개쯤 | 'about six additions and deletions' | S2 |
| 2025 편입 6곳 모두 50% 넘게 · 더트레이드데스크 68%·룰루레몬 46% 내림 | 'at least 50%' · -67.7% · -45.7% | S2 |
| CDW 두 번 들어오고 두 번 빠짐 · 루시드 2021→2년 뒤 · 지스케일러 2021→올해 6월 · 인스메드 작년 12월→올해 6월 | 2019 in·2021 out·2023 in·2025 out 등 | S1·S11 · 6월은 2차 S6 https://finviz.com/news/361357/nasdaq-100-index-june-2026-quarterly-changes · S7 https://mondovisione.com/news/nasdaq-100-index-june-2026-quarterly-changes-2026612/ |
| 101~125위 기존 회사는 자리가 남을 때만 | 'Steps 3 and 4 apply only if fewer than 100' | S2 |
| 5월 1일부터 40위 안 15거래일 · 예전 석 달 | 'top 40'·'15 trading days'·'three months' | S3 https://indexes.nasdaqomx.com/docs/2026_May_NDX_Changes_FAQ.pdf · S4 |
| 석 달마다 125위 밖 빠짐 · 3월·6월·9월 | 'outside of the top 125' · 'March, June, and September Rebalance' | S3 · S4 https://indexes.nasdaqomx.com/docs/Methodology_Change_Log_NDX.pdf |
| 6월 5개 들어오고 5개 빠짐 · 6월 22일 (2차) | five/five · June 22, 2026 | 2차 S6 · S7 |
| 스페이스X 6월 12일 상장 · 7월 7일 편입 (2차) | June 12 · July 7 | 2차 S8 https://aljazeera.com/economy/2026/7/7/spacex-shares-slide-as-it-joins-the-tech-heavy-nasdaq-100 · S9 https://www.rttnews.com/3663388/spacex-joins-nasdaq-100-less-than-a-month-after-going-public.aspx?type=ipo |
| 2025년 말 상위 10개 52% | 'top ten securities comprised 52%' | S2 |
| QQQ 비용 빼기 전 지수만큼 · TIGER 미국나스닥100 벤치마크 나스닥100 | 'before expenses, correspond to' · '벤치마크 NASDAQ 100' | S1 · S10 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 |

# 올리기 전 확인
- 2026-11-27 15:23 firemap-write(발행 날) — 위 주소 16곳 다시 엶: 15곳 200, 알자지라 301(같은 기사 주소 이동) · 웹 검색 2건(12월 연례 교체 2026 발표일·9월 분기 변경) — 나스닥 12월 2026 발표 아직 없음, 9월 분기 공식 발표문 못 찾음(9/20 블룸버그 인용 보도로 9월 심사 있었던 것만 확인) · 바뀐 것: 없음(본문 숫자·날짜 그대로) · 새로 찾은 것: indexes.nasdaqomx.com/docs/2026_NDX_Changes_FAQ.pdf(5월 FAQ와 별도 판) 있음 — 본문에 안 넣음
- 2026-11-26 14:18 firemap-write-b(조사·작성 날 — 발행 날 11/27 16:10 회차가 나스닥 발표·규칙 문서 다시 열어 바뀐 것 반영)
- 다시 연 주소: https://www.nasdaq.com/press-release/annual-changes-nasdaq-100-indexr-2025-12-13 (11/26 200) · https://www.nasdaq.com/press-release/annual-changes-nasdaq-100-indexr-2024-12-13 (11/26 200) · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-indexr-2023-12-08 (11/26 200) · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2022-12-09 (11/26 200) · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-indexr-2021-12-10 (11/26 200) · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2020-12-11 (11/26 200) · https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2019-12-13 (11/26 200) · https://indexes.nasdaqomx.com/docs/202601%20NDX%20Reconstitution%20and%20Performance%20Highlights.pdf (11/26 200) · https://indexes.nasdaqomx.com/docs/2026_May_NDX_Changes_FAQ.pdf (11/26 200) · https://indexes.nasdaqomx.com/docs/Methodology_Change_Log_NDX.pdf (11/26 200) · https://indexes.nasdaqomx.com/docs/Nasdaq-100_Index_Consultation_February_2026_Summary_of_Responses_and_Conclusion.pdf (11/26 200) · https://finviz.com/news/361357/nasdaq-100-index-june-2026-quarterly-changes (11/26 200) · https://mondovisione.com/news/nasdaq-100-index-june-2026-quarterly-changes-2026612/ (11/26 200) · https://aljazeera.com/economy/2026/7/7/spacex-shares-slide-as-it-joins-the-tech-heavy-nasdaq-100 (11/26 검색 확인) · https://www.rttnews.com/3663388/spacex-joins-nasdaq-100-less-than-a-month-after-going-public.aspx?type=ipo (11/26 검색 확인) · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 (11/26 200)
- 기준일: 2026-11-26(나스닥 발표문 2019~2025·2026년 5월 규칙·6월 분기 발표)
- 바뀐 것: 처음 조사 — 없음
- 새로 찾은 것: 7년 12월 교체 39개(2024년만 3개) · 발표·적용 요일 7번 모두 같음 → 올해 12/11·12/21 · 5/1 빠른 편입·3·6·9월 분기 심사 · 6월 첫 분기 심사 5개 · 인스메드 반년 만에 빠짐 · 경쟁 글 7년 개수 센 글 0편
- 조사 뒤 공표: 나스닥 2026년 12월 연례 교체 발표 12/11(미국) 예상 — 발행(11/27) 뒤라 글은 '예상'으로 씀 · 9월 분기 심사 결과 발표문 못 찾음
