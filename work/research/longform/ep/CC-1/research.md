# CC-1 자료조사 — KODEX 미국배당커버드콜액티브 vs TIGER 미국배당다우존스, 1억 넣었다면 (youtube-loop 2026-11-22 첫 판)
공개 칸 11/30 11:30 · 관문 11/29 11:30 · 축: 배당·배당ETF(사장님 11/19 범위 안) · 단독 세금 편 아님(세금은 한 장)
근거 파일: facts_1122.md(사실표 S1~S4·대조 결과) · cc1_calc.py → cc1_calc_out_1122.txt · cmp_div_out_1122.txt · cmp_px_out_1122.txt · raw/naver_tiger_px_1122.txt · analysis.md · toc_compare.md(경쟁 16편) · raw/comments_q_1122.txt

# 원문
확인일 2026-11-22(삼성 S1·S2, 야후 S4, 네이버 S5), 2026-11-21(미래에셋 S3), 2026-11-21(법령 S6·S7 — SQ-1 raw/law1121 캡처 재사용)
- S1 삼성자산운용 KODEX 미국배당커버드콜액티브(441640) 분배 이력 50건(2022-10-31~2026-11-13 기준일·주당 금액) — 최근 12번 합 1,181원, 2026년 달마다 92~103원 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 (raw/kodex_divid_info_1122.json)
- S2 삼성자산운용 같은 상품 종가·NAV 표(상장일~, 최근 12개월 일 단위)·총보수 연 0.190%·매월 15일 분배 기준일·과세 문구 '분배금은 배당소득세 과세 : Min(현금분배금, 과표증분) X 15.4%' https://m.samsungfund.com/etf/product/view.do?id=2ETFH4 · https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 (raw/kodex_view_1122.txt 101~105행)
- S3 미래에셋자산운용 TIGER 미국배당다우존스(458730) 분배금 현황 연간 합 2023 202·2024 443·2025 430·2026 361원(2026.11.19 기준)·현재가 14,505원(11/20 종가) https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008
- S4 (2차) 야후 파이낸스 chart API 441640.KS·458730.KS 일별 종가(close)·수정종가(adjclose)·분배 events https://query1.finance.yahoo.com/v8/finance/chart/458730.KS (raw/*_chart_20261122.json)
- S5 (2차) 네이버 금융 일별 시세 458730·441640 — **분배를 반영한 수정 값**(KODEX 2025-11-20 11,520원 = 삼성 원 종가 12,605원과 다름, 야후 adjclose 11,497원과 0.2% 차) https://api.finance.naver.com/siseJson.naver?symbol=458730&requestType=1&startTime=20230619&endTime=20230621&timeframe=day (raw/naver_tiger_px_1122.txt)
- S6 국내 상장 해외 ETF 이익(분배·매매차익) = 배당소득, 원천징수 14%+지방 1.4% — 소득세법 제17조①5호·시행령 제26조의2④·제129조①2호, 지방세법 제103조의13 https://www.law.go.kr/법령/소득세법시행령/제26조의2 · https://www.law.go.kr/법령/소득세법/제129조
- S7 금융소득(이자+배당) 연 2,000만원 이하 분리과세·넘으면 종합과세 — 소득세법 제14조③6호·제62조 https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/소득세법/제62조

# 경쟁
같은 주제 상위 16편(toc_compare.md '# 경쟁 목차', 2026-11-22 조회·자막)
- 말한 것: 콜옵션 원리 그림(머니인사이드 qmTwtRhnFqo 04:38)·가격 따로/분배 따로/합친 총수익(똑재TV J0hc2v8DzRo 2:30)·1억이면 매달 75만~99만원(수페TV hDHVtwBMUzs)·은퇴 소득 공백과 계좌·배분(투자360 yGuybuoroRI)·상품 순위
- 빠뜨린 것: ① 국내 상장 배당 커버드콜 하나에 1억을 넣은 '남은 돈'을 원으로, 분배금 세금 떼고 센 편 0 ② 같은 날 시작한 일반형(옵션 안 파는 같은 계열 배당 ETF)과 나란히 0 ③ 받아 씀 vs 다시 넣음 0 ④ 기간을 어디서 자르냐에 따라 답이 뒤집히는 것을 세 구간으로 보인 편 0 ⑤ 차트 값(수정 값)과 실제 거래가가 달라 댓글에서 헷갈리는 것 설명 0
- 대표 1등: 투자360 yGuybuoroRI(69.6만회·41.44배, 22:15, 2026-11-22 확인) https://www.youtube.com/watch?v=yGuybuoroRI

# 질문
실제 질문(유튜브 댓글 2026-11-22 받음 raw/comments_q_1122.txt, commentThreads relevance 상위 70줄) → 우리 답
| # | 질문(원문 요지) | 출처 | 우리 답 | 장 |
|---|---|---|---|---|
| Q1 | "tiger 미국배당다우존스와 kodex미국배당커버드콜 차이점"(ISA 처음 만든 사람) | https://www.youtube.com/watch?v=yXQ-EMTEQ-k&lc=Ugwxu8rNphH0QOjuL2F4AaABAg | 커버드콜은 담은 주식의 콜옵션을 팔아 받은 돈을 분배 → 분배는 많고 오를 때 위가 막힘. 1년 1억: 분배 793만 vs 294만, 남은 돈 합 9,654만 vs 1억 1,793만 | 1·2장 |
| Q2 | "커버드콜이 원금 녹으면 본주는 안 녹나?" · "개별주식하면 원금이 안 녹냐?" | https://www.youtube.com/watch?v=tU1kVGy52qE&lc=UgymSI1zhnbCV1jg9E94AaABAg · https://www.youtube.com/watch?v=tU1kVGy52qE&lc=UgyAhkCuxMWJwXSq3RJ4AaABAg | 둘 다 내림. 값만 최대 낙폭 1년: 커버드콜 −19.3% vs 일반형 −12.8%(같은 기간). 이번 1년엔 커버드콜 값이 12,605→11,170원으로 내렸고 일반형은 12,615→14,505원으로 올랐음 | 4장 |
| Q3 | "24년 12월 30일 441640 주가가 왜 12200으로 계산되나요? 차트상으론 11000원대인데" | https://www.youtube.com/watch?v=sGrkDT8vnDY&lc=UgzDdgKC2R_mLebNSYB4AaABAg | 증권사·포털 차트는 분배금만큼 과거 값을 낮춘 '수정 값'인 경우가 있음(네이버 2025-11-20 11,520원 vs 삼성 원 종가 12,605원, S2·S5). 우리 계산은 원 종가 + 받은 분배금 | 7장 함정 |
| Q4 | "Irp계좌에서 441640으로 2천만원이 넘더라도 따로 세금이 나오지 않나요?" | https://www.youtube.com/watch?v=amc8B8SxwgY&lc=UgxE189kNw5pkxpwodl4AaABAg | 이 편은 일반 계좌만 셈. 일반 계좌에선 금융소득 연 2,000만원 넘으면 종합과세(S7) — 1년 분배율(9.4%)대로면 원금 약 2억 1천만원부터 닿음. 연금 계좌 과세는 '한계'에 | 6장 |
| Q5 | "절세계좌에서 분배금 재투자하면 복리효과 좀이라도 생길까요?" | https://www.youtube.com/watch?v=sGrkDT8vnDY&lc=UgwHz39BX6O9RQch_MB4AaABAg | 일반 계좌 세후로 센 값: 이번 1년은 다시 넣음 9,580만 vs 받아 씀 9,654만(값이 내리는 동안 되사서 거의 같음), 2023-06-20부터는 1억 4,790만 vs 1억 4,524만 | 5장 |
| Q6 | "정리해 보면 하락장과 횡보장에서는 독, 상승장에서만 빛을 보는 상품?" | https://www.youtube.com/watch?v=sGrkDT8vnDY&lc=UgxcViYx8MCU5-mZkqR4AaABAg | 원리상 반대: 오를 때 위가 막혀 덜 오르고, 내릴 때 분배만큼 덜 빠짐. 다만 이번 1년 숫자에서는 분배 더한 낙폭도 일반형보다 깊었음(−15.1% vs −11.9%), 값만(−19.3% vs −12.8%) → 원리 한 줄 + 실제 숫자 | 4·7장 |
| Q7 | "22년 9월 10000원 상장해서 현재 12695원. 배당까지 고려해도 3년 넘게 30% 오른 걸…" | https://www.youtube.com/watch?v=sGrkDT8vnDY&lc=UgyafiivtQwxNWaQag14AaABAg | 상장일 2022-09-27 1억 → 11/20 종가 기준 받아 씀 1억 4,498만(분배 3,328만+평가 1억 1,170만) | 3장 |
얼마나 자주: 경쟁 4편 상위 댓글 70줄 중 '원금·녹'이 들어간 줄 4개, 계좌(ISA·IRP·연금·절세·연저펀) 말이 든 줄 17개 — 위 표는 그중 이 편 장에 답이 있는 것만.

# 우리만
원자료(S1·S2·S3, 빈 곳 S4)로 직접 계산한 새 숫자(경쟁 16편 0편) — cc1_calc_out_1122.txt
- 최근 1년(2025-11-20→2026-11-20) 1억, 분배금 15.4% 떼고 받아 씀: 커버드콜 분배 793만+평가 8,862만 = **9,654만** vs 일반형 294만+1억 1,498만 = **1억 1,793만**(차이 2,139만)
- 같은 시작일 2023-06-20: 1억 4,524만 vs 1억 5,783만(차이 1,259만) · 커버드콜 상장일 2022-09-27부터 1억 4,498만
- 1억이면 커버드콜 세후 매달 61.7만~69.1만원(2025-12~2026-11, 7,933주) vs 일반형 20.1만~30.2만원
- 금융소득 2,000만원(세전 분배)에 닿는 원금: 커버드콜 약 2억 1,300만원(1년 분배 1,181원 ÷ 12,605원 = 9.37%) vs 일반형 약 5억 7,500만원(439 ÷ 12,615 = 3.48%)

# 왜
- 분배금이 많은 이유: 삼성 상품 화면(S2, raw/kodex_view_1122.txt 70행) '기업의 배당 외에 콜옵션 매도 전략을 사용하여 추가적인 배당 재원을 마련' · '기계적인 콜옵션 매도가 아닌 시장 상황에 따라 탄력적으로'. 같은 이유로 값이 많이 오를 때 그 위 몫을 옵션 산 쪽에 넘긴다 → '위가 막힘'
- 이번 1년 덜 남은 이유: 주당 값이 −1,435원(12,605→11,170원) 빠졌는데 분배는 1,181원(세전) → 분배로 값 하락을 다 못 메움. 일반형은 값 +1,890원에 분배 439원. **값이 왜 빠졌는지(담은 종목·옵션 손익·환율 몫 나눔)는 운용사 원문에 문장이 없다 → 말하지 않는다**(한계)
- 다시 넣어도 1년은 거의 같은 이유: 값이 내리는 동안 분배금으로 되산 주식도 같이 내림(9,580만 vs 9,654만)
- 실제 세후가 우리 값보다 조금 많을 수 있는 이유: 과세는 '현금분배금과 과표증분 중 작은 것 × 15.4%'(S2) — 우리는 분배 전부에 15.4%를 뗀 가정

# 그래서
- 장마다 할 일(제도·확인, 권유 없음): ① 상품 화면에서 '분배금'과 '총수익(값+분배)'을 따로 본다 — 분배율 하나로 판단하지 않기 ② 차트를 볼 때 수정 값인지 원 종가인지 확인한다(Q3) ③ 일반 계좌라면 한 해 이자·배당 합이 2,000만원을 넘는지 미리 센다 — 커버드콜 1억당 세전 약 937만원(이번 1년) ④ 받아 쓸지 다시 넣을지는 '매달 현금이 필요한가'로 정한다 — 숫자 차이는 기간마다 달랐다
- 권유 없음: 어느 상품을 사라·팔라·갈아타라 말하지 않는다. 숫자와 조건만

# 누구라면
- 매달 생활비로 꺼내 쓸 사람(은퇴 뒤): 1억에서 세후 매달 62만~69만원(커버드콜) vs 20만~30만원(일반형) — 다만 1년 뒤 남은 돈 합은 2,139만원 적었다
- 꺼내 쓰지 않고 쌓을 사람: 다시 넣음 1년 9,580만 vs 1억 1,798만, 2023-06-20부터 1억 4,790만 vs 1억 6,069만 — 두 구간 모두 일반형이 많았다
- 2억 넘게 넣을 사람(일반 계좌): 커버드콜은 원금 약 2억 1천만원부터 한 해 분배가 2,000만원에 닿아 종합과세 대상이 될 수 있다(일반형은 약 5억 7천만원)

# 함정
- 기간을 어디서 자르냐에 따라 답이 뒤집힌다(우리 계산 cc1_windows_out_1122, 야후 수정 값·세전·2차): 1년 끝날을 2025-12-05로 자르면 커버드콜 +15.7% vs 일반형 +2.6%(커버드콜 앞섬), 2026-06-05면 +35.8% vs +44.7%, 2026-11-18이면 +0.5% vs +21.4%(일반형 앞섬). 끝날 6개 중 4개는 커버드콜, 최근 2개는 일반형 — 한 구간으로 결론 내지 않는다
- 포털·앱 차트 값은 분배를 뺀 수정 값일 수 있다(S5): 네이버 KODEX 2025-11-20 11,520원 vs 실제 그날 종가 12,605원 — 수익률을 직접 셀 때 섞으면 틀린다
- 분배율은 %라 값이 내리면 분배 현금도 준다: 달마다 103원(2026-07)→92원(2026-11) (S1)
- 액티브 상품이라 운용 방식·보수가 바뀔 수 있다(지금 총보수 0.190%, S2)

# 한계
- TIGER 2023-06-20·2025-11-20 원 종가(9,960·12,615원)는 야후(S4) 하나 — 미래에셋·KRX 일별 원표 확인 안 함(미래에셋 price.ajax 빈 값, KRX 정보데이터 호출 권한에서 막힘). 대신 네이버 수정 값(S5)과 야후 수정 값이 0.3% 안(8,899 vs 8,921원·12,248 vs 12,237원)이라 야후 계열 값은 서로 맞음 · 11/20 종가는 S3 원문과 같음
- 커버드콜 값이 1년에 왜 빠졌는지(종목·옵션 손익·환율 나눔): 원문에 이유 없음 → 말하지 않음 · 투자설명서(옵션 매도 비율·기초 지수) 원문 안 열어 봄
- 연금저축·IRP·ISA 안의 과세(Q4·Q5): 이 편 계산 밖 — 말로 '일반 계좌 기준'만 밝힘
- 분배 세금은 분배 전부에 15.4%(과표증분 쪽이 작으면 실제 세금은 더 적음) · 판 때 세금·증권사 수수료·건강보험료는 뺌
- 기준일 2026-11-20 종가 하나 — 11/23 이후 종가·12월 분배로 숫자가 바뀜(올리기 전 확인에서 다시 셈)

# 대조
대본 v1(2026-11-22 13시) 말 값 + v1.2 말 늘리기(2026-11-23 youtube-loop, 표 끝 10줄) · 정확한 값은 대본 [자막] 줄에 원값 그대로.
| 원문 | 원값 | 대본 값 | 출처 |
|---|---|---|---|
| KODEX 1년 분배(주당 12번) | 1,181원 | 말 '가격 내린 폭보다 적었고요' · 자막 1,181원 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 |
| KODEX 종가 2025-11-20 → 2026-11-20 | 12,605 → 11,170원 | 말 '1,400원쯤 내렸어요' · 자막 1만 2,605원 → 1만 1,170원(−1,435원) | S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 |
| KODEX 총보수 | 연 0.190% | 말 0.19% · 자막 연 0.190% | S2 https://m.samsungfund.com/etf/product/view.do?id=2ETFH4 |
| KODEX 분배 과세 | Min(현금분배금, 과표증분)×15.4% | 15.4% | S2 https://m.samsungfund.com/etf/product/view.do?id=2ETFH4 |
| TIGER 1년 분배(12번) | 439원(연간 합 2025 430·2026 361) | 말 '적지만 분배금이 더 얹혔고요' · 자막 439원 | S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 |
| TIGER 종가 2026-11-20 | 14,505원 | 말 '가격이 올랐습니다' · 자막 1만 4,505원 | S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 |
| TIGER 종가 2025-11-20·2023-06-20 (2차) | 12,615원·9,960원 | 자막 1만 2,615원(야후, 2차) | S4 https://query1.finance.yahoo.com/v8/finance/chart/458730.KS · S5 https://api.finance.naver.com/siseJson.naver?symbol=458730&requestType=1&startTime=20251119&endTime=20251121&timeframe=day (수정 값끼리 0.3% 안) |
| 1년 1억 받아 씀 합 | 9,654만 vs 1억 1,793만 | 말 '9천6백만원 정도' vs '1억 2천만원 가까이' · 차이 '2천만원이 넘었어요'(2,139만) · 자막 원값 | cc1_calc_out_1122 · S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 |
| 1년 끝날별 앞선 쪽 (2차) | 2025-12-05 +15.7% vs +2.6% · 2026-11-18 +0.5% vs +21.4% | 말 '2025년 12월로 자르면 커버드콜이 훨씬 앞섰습니다'·'여섯 번 중 커버드콜이 앞선 때가 더 많았어요' · 자막 6개 원값 | cc1_windows_out_1122 · S4 https://query1.finance.yahoo.com/v8/finance/chart/441640.KS · S5 https://api.finance.naver.com/siseJson.naver?symbol=441640&requestType=1&startTime=20251119&endTime=20251121&timeframe=day |
| 같은 시작일 합 | 1억 4,524만 vs 1억 5,783만 | 말 '1억 5천만원에 조금 못 미쳤'·'일반형이 1천만원 넘게 더'(1,259만) · 자막 원값 | cc1_calc_out_1122 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 · S4 https://query1.finance.yahoo.com/v8/finance/chart/458730.KS (2차) |
| 1억 세후 매달 | 61.7만~69.1만 vs 20.1만~30.2만 | 말 '매달 60만원대'·'그 3분의 1 정도'(20.1만~30.2만 ÷ 61.7만~69.1만 = 0.29~0.49 — '3분의 1 정도'는 가운데 값 25만/65만=0.38 기준) · 자막 원값 | cc1_calc_out_1122 · S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 |
| 국내 상장 해외 ETF 분배 = 배당소득 | 14%+지방 1.4% | 15.4% | S6 https://www.law.go.kr/법령/소득세법/제129조 |
| 금융소득 종합과세 기준 | 연 2,000만원 | 2천만원 | S7 https://www.law.go.kr/법령/소득세법/제14조 |
| 1년 분배율 | 1,181 ÷ 12,605 = 9.37% | 말 '한 해 9%가 넘었습니다' · 자막 9.37% | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 |
| 상장일부터 받아 씀 | 1억 → 1억 4,498만(+45.0%), 가격만 +11.7% | 말 '조금 오른 게 다'·'절반 가까이 불어났습니다' · 자막 원값 | cc1_calc_out_1122 · S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 |
| 값만 최대 낙폭 1년 | 가격만 −19.3% vs −12.8% · 분배 더한 합계 −15.1% vs −11.9% | 말 '분배금까지 더해서… 15% 넘게, 일반형보다 더 깊었어요' · 자막 원값 | cc1_calc_out_1122 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 · S4 https://query1.finance.yahoo.com/v8/finance/chart/458730.KS (2차) |
| 1억 세전 1년 분배 | 7,933주 × 1,181원 = 약 937만 | 말 '9백만원을 넘었어요' · 자막 약 937만원 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 |
| 2,000만원 닿는 원금 | 약 2억 1,300만 vs 5억 7,500만 | 말 '2억 1천만원쯤부터'·'그 두 배를 훌쩍 넘게' · 자막 원값 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 |
| 네이버 수정 값 vs 원 종가 2025-11-20 | 11,520 vs 12,605원 | 말 '11,000원대'·'12,000원대' · 자막 원값 | S5 https://api.finance.naver.com/siseJson.naver?symbol=441640&requestType=1&startTime=20251119&endTime=20251121&timeframe=day · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 |
| 주당 분배 7월 → 11월 | 103 → 92원 | 말 '여름보다 가을에 줄었습니다' · 자막 원값 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 |
| 2023-06-20부터 세후 분배금 | KODEX 3,056만 vs TIGER 1,220만(2.50배) | 말 '일반형의 2.5배' | cc1_calc_out_1122 · S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 |
| 상장일부터 주당 분배 합 | 50번 3,934원(상장가 10,000원의 39.3%) | 말 '3,900원이 넘어요'·'40% 정도' · 자막 원값 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 |
| 상장일부터 다시 넣음 | 1억 4,921만 | 말 '1억 5천만원에 조금 못 미쳤고요' | cc1_calc_out_1122 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 |
| 연도 주당 분배 합 | 2023 634·2024 934·2025 1,130·2026(11번) 1,083원 | 말 '2년 사이 1.8배'(1,130÷634=1.78) · 자막 원값 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 |
| 2023-06-20부터 최대 낙폭 | 합계 −13.3% vs −12.6% · 가격만 −19.3% vs −14.1% | 말 '둘 다 13% 안팎'·'19% 넘게, 14%쯤' · 자막 원값 | cc1_calc_out_1122 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 · S4 https://query1.finance.yahoo.com/v8/finance/chart/458730.KS (2차) |
| 1억 매달 세후 가장 많은/적은 달 | KODEX 69.1만(2026-07)/61.7만(2026-11), 차 7.4만 · TIGER 30.2만(2026-06)/20.1만(2026-08) | 말 '7만원 정도'·'30만원, 20만원 정도' · 자막 원값 | cc1_calc_out_1122 · S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 |
| 1억 1년 분배 세금 | KODEX 7,933주×1,181원=936.9만×15.4%=144.3만 · TIGER 7,927주×439원=348.0만×15.4%=53.6만(세후 792.6만·294.4만 = cc1_calc 793만·294만) | 말 '140만원 넘게'·'50만원대' · 자막 원값 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S6 https://www.law.go.kr/법령/소득세법/제129조 |
| 댓글 중 계좌 이야기 | 상위 70줄 중 17줄(24%) | 말 '네 개 중 하나꼴' | raw/comments_q_1122.txt · Q1 https://www.youtube.com/watch?v=yXQ-EMTEQ-k&lc=Ugwxu8rNphH0QOjuL2F4AaABAg · Q4 https://www.youtube.com/watch?v=amc8B8SxwgY&lc=UgxE189kNw5pkxpwodl4AaABAg (2차 — 댓글 셈은 우리 셈) |
| 1년 끝날 2026-06-05·2024-12-06 (2차) | 35.8% vs 44.7%(차 8.9%p) · 35.2% vs 32.5% | 말 '일반형이 9%포인트 정도 앞섰고요'·'커버드콜이 조금 앞섰지만, 둘의 차이는 크지 않았습니다' · 자막(7장) 원값 | cc1_windows_out_1122 · S4 https://query1.finance.yahoo.com/v8/finance/chart/441640.KS |
| 1년 다시 넣음 vs 받아 씀 | KODEX 9,580만 < 9,654만 | 말 '다시 넣은 쪽이 오히려 덜 남은 해도 있었으니' | cc1_calc_out_1122 · S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · S2 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 |
| 분배 기준일(11/24 v1.3 더함) | 매월 15일 | 말 '매달 15일을 기준일로' | S2 https://m.samsungfund.com/etf/product/view.do?id=2ETFH4 |
| 2천만원 이하 신고(11/24 v1.3 더함) | 분리과세 — 원천징수로 끝 | 말 '2천만원 이하면 따로 신고할 일은 없어요' | S7 https://www.law.go.kr/법령/소득세법/제14조 |
| TIGER 총보수(11/24 v1.3 더함) | 연 0.01%(2026-11-13) | 말 0.01% · 자막 원값 | SQ-1 S9 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009 |
| KODEX 1년 최저 종가(11/26 v1.3 심사 때 더함) | 2026-11-20 1만 1,170원(2025-11-20~2026-11-20 중 가장 낮음, 시작 1만 2,605원) | 말 '1년 중 가장 낮던 날'(16행)·'최근 1년 중 가장 낮던 날'(185행 — 2023-06-20부터 센 기간 전체로는 2023-11-20 9,595원이 더 낮아 '최근 1년'을 붙임) · 자막 22행 | S4 https://query1.finance.yahoo.com/v8/finance/chart/441640.KS (raw/441640.KS_chart·recent_20261122.json, 2차) · S1 삼성 product-earning 종가와 0원 차이(cmp_px_out_1122.txt) |

# 올리기 전 확인
확인일 2026-11-28(youtube-loop 00:43~) · 공개 11/30 11:30 · 관문 11/29 11:30(gate는 이 날짜로 1일 안) · 받은 원본 raw/pre1128/(git add 안 함)
- KODEX 분배 이력 50건 다시 받음 — 11/22 받은 것과 기준일·금액 50건 모두 같음(마지막 2026-11-13 92원, 다음 기준일 12/15는 공개 뒤) https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFH4 · 종가 표 https://m.samsungfund.com/api/v1/kodex/product-earning/2ETFH4.do?srchTerm=0 · 상품 화면 열림(200) https://m.samsungfund.com/etf/product/view.do?id=2ETFH4
- 종가: 야후 441640 11/20 11,170원·458730 11/20 14,505원 그대로(대본 기준값과 같음) https://query1.finance.yahoo.com/v8/finance/chart/441640.KS · https://query1.finance.yahoo.com/v8/finance/chart/458730.KS · 네이버 수정 값 https://api.finance.naver.com/siseJson.naver?symbol=441640&requestType=1&startTime=20251119&endTime=20251121&timeframe=day · https://api.finance.naver.com/siseJson.naver?symbol=458730&requestType=1&startTime=20251119&endTime=20251121&timeframe=day · https://api.finance.naver.com/siseJson.naver?symbol=458730&requestType=1&startTime=20230619&endTime=20230621&timeframe=day
- TIGER 운용사 화면 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009 — 열림(200)이지만 본문이 스크립트로 그려져 글자를 못 받음(curl·playwright 둘 다 141바이트) → 총보수 0.01%는 SQ-1 11/26 확인값 그대로, 11월 분배 공고는 확인 안 함
- 법령: https://www.law.go.kr/법령/소득세법/제129조 · https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/소득세법/제62조 · https://www.law.go.kr/법령/소득세법시행령/제26조의2 — 열림(200). 본문 비교는 SQ-1 11/26(raw/law1126 ↔ law1121 12조 같음) 그대로, 11/26 뒤 새 공포는 확인 안 함
- 댓글 질문 영상 열림(200): https://www.youtube.com/watch?v=yXQ-EMTEQ-k&lc=Ugwxu8rNphH0QOjuL2F4AaABAg · https://www.youtube.com/watch?v=amc8B8SxwgY&lc=UgxE189kNw5pkxpwodl4AaABAg
- 기준일: 가격·남은 돈 = 2026-11-20 종가(대본 166행 '11월 20일에 자른 한 장면'·자막 날짜 그대로) · KODEX 분배 = 2026-11-13 기준일분까지 50건 · TIGER 분배 = 2026-11-19 기준 연간 합(미래에셋 11/21) · 총보수 = KODEX 11/22·TIGER 11/26 운용사 화면 · 세법 = 11/26 현행
- 바뀐 것: 없음 — 기준일 11/20 값이 운용사·야후에서 그대로, KODEX 분배 50건 같음, 조사(11/22) 뒤 끼인 공표 일정 없음. 말·자막은 11/20로 못 박아 두어 다시 녹음할 줄 0
- 새로 찾은 것: ① 11/27 종가 KODEX 11,495원(11/20보다 +2.9%)·TIGER 14,990원(+3.3%) — 11/20에 1억 넣은 같은 계산을 11/27 값으로 매기면 9,912만 vs 1억 2,177만(차 2,264만, 분배는 11/20까지만) → 말 '2천만원이 넘었어요'·'앞선 쪽' 그대로 맞음, 대본은 안 고침(고정 댓글이나 설명란에 '11/27 종가로 다시 세면'을 넣을지는 copywriter 판단) ② 네이버 TIGER 수정 값이 11/26 이전을 약 30원씩 낮춤(11/20 14,475원 vs 원 종가 14,505원) — 11/27 무렵 11월 분배락이 있었던 것으로 보임(금액·기준일 운용사 원문 확인 안 함). 11/20 뒤 일이라 대본 '1년 12번 439원'은 그대로 · 3장 함정 '포털 차트는 수정 값' 말이 이번 주에도 그대로 일어남(KODEX는 아직 11/20 같은 값)
