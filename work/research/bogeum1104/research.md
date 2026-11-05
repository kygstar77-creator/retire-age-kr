# bogeum1104 자료조사 — 보금자리론 11월 9일 인상·1년 사이 여섯 번 (firemap-write 2026-11-04 06:2x, 11/5 10:10 부동산① 칸)

## 검증
- 수요: demand.py 11/4 — 보금자리론 월 72,300(같은 회차 후보 전세보증보험 18,870·아파트취득세 10,710·주택담보대출한도 7,300보다 높음) · 자동완성 '11월 보금자리론 금리'·'보금자리론 금리 인상'·'보금자리론 금리 변동'(ac.txt 11/4)
- 경쟁: 네이버 모바일 '보금자리론 금리 인상' 11/4 상위 블로그 7편 모두 11/2~4 글, 0.1%p 차이(3억 월 약 1만 8천원)·8일 기한·올해 여섯 번째 인상까지 다룸. 1년 전 금리로 다시 계산한 월 상환액을 낸 글 0(bench_raw/posts.json kw '3.85' 없음)
- 우리 실측: 지난달 bogeum1017(#306, 만기 20년 vs 30년)과 각도 안 겹침. textrule 11/4: 부동산 축 쏠림보정 0.77(2위), 형식 2(계산 사례) 1위

## 원문
- S1 한국주택금융공사 보도자료 2026-11-02 '11월 보금자리론 금리 0.10% 포인트 인상' — 2026-11-04 확인(raw/p600738.html): https://www.hf.go.kr/ko/sub05/sub05_04_05.do?mode=view&articleNo=600738
- S2 한국주택금융공사 금리안내 2026년 11월(공시일 11/01·11/09) — 2026-11-04 확인(raw/rate.html): https://www.hf.go.kr/ko/interest-rate-guidance.do
- S3 같은 금리안내 2025년 12월~2026년 10월(srBYear·srBMonth) — 2026-11-04 확인(raw/hist/): https://www.hf.go.kr/ko/interest-rate-guidance.do?srBYear=2026&srBMonth=07
- S5 한국천문연구원 월력 2026년 11월 — 2026-11-05 확인(raw1105/kasi_cal.html): https://astro.kasi.re.kr/life/pageView/5?search_year=2026&search_month=11
- S4 한국주택금융공사 보금자리론(일반) 상품소개 — 2026-11-04 확인(raw/sub01_01_01.html): https://www.hf.go.kr/ko/sub01/sub01_01_01.do

## 경쟁
bench.md — 블로그 7편. 모두 이번 0.1%p·8일 기한·3억 월 차이(약 1만 8천원)·우대금리를 다룸. 올해 여섯 번째 인상이라는 말은 4편(cjstkrkfka·eh691769·wannastone·wolgeup_note)이 기사 인용으로 적음. 빠뜨린 것: 1년 전 금리 기준 월 상환액 차이(7편 0), 이미 받은 대출은 그대로라는 답(cjhya1 1편).

## 질문
1. 이미 보금자리론을 쓰는 사람도 금리가 오르나 — https://kin.naver.com/qna/detail.naver?dirId=4010502&docId=491537935 → 답: c03(고정금리라 그대로)
2. 금리는 신청일 기준인가 실행일 기준인가 — https://kin.naver.com/qna/detail.naver?dirId=4010502&docId=495013161 → 답: c01(8일까지 신청 완료면 인상 전 금리, S1)
3. 시장 금리가 내리면 보금자리론 금리도 재조정되나 — https://kin.naver.com/qna/detail.naver?dirId=4010501&docId=485155952 → 답: c03(저절로 안 내려감, 갈아타기는 3년 안 0.5% 한도 수수료)
4. 보금자리론 금리 변동 — 자동완성 https://ac.search.naver.com/nx/ac?q=%EB%B3%B4%EA%B8%88%EC%9E%90%EB%A6%AC%EB%A1%A0%20%EA%B8%88%EB%A6%AC (ac.txt) → 답: c02(올해 여섯 번 올랐고 내린 달 없음)

## 왜
- 이번 인상 이유: S1 "시장금리 및 주택저당증권(MBS) 자금조달 여건 등을 종합적으로 고려" — 글에는 넣지 않음(뜻 풀이가 길어짐, 경쟁 7편이 다 옮김). 앞선 다섯 번 인상 이유는 이번에 원문을 열지 않음 → 쓰지 않음.
- 이미 받은 대출이 안 오르는 이유: S4 '대출 받은 날부터 만기까지 고정금리'.
- 아낌e가 u보다 싼 이유: S4 전자약정·전자등기.

## 그래서
- 이번 주 신청할 사람: 8일(일)까지 신청 완료, 은행 창구(t)는 은행 여는 날 확인 — c01
- 이미 쓰는 사람: 바꿀 것 없음, 갈아타기는 3년·0.5% 수수료 먼저 — c03

## 누구라면
- 새로 받을 사람(3억·30년): 1년 전보다 월 약 24만원 더 — c02
- 이미 받은 사람: 그대로 — c03
- 신혼가구 우대 0.3%p: 30년 4.90% — c04

## 함정
- 8일이 일요일 — 은행 창구 신청은 그 전에 — c01
- u 방식이면 0.1%p 더, 규제지역 0.2%p 더 — c04

## 우리만
- 공사 금리표 12개월 치(S2·S3)로 다시 계산한 1년 전(3.85%) 대비 월 상환액: 2억 +16만·3억 +24만·3.6억 +29만원, 3억 30년 이자 합 차이 약 8,673만원(calc_out.txt) — 경쟁 7편 0편

## 예외
- 원리금균등·거치 없음 가정. 체증식·원금균등이면 첫 달 금액이 다름
- 우대·가산 없는 아낌e 기본 금리 기준. 실제 금리는 우대·u·규제지역에 따라 다름

## 한계
- '신청 완료'가 정확히 어느 단계인지(업무처리기준 PDF) 원문을 이번에 열지 않음 → 보도자료 문장('신청을 완료하면')까지만 씀
- 은행 지점 주말 영업 여부 확인 안 함 → '은행 여는 날을 먼저 보세요'까지만
- 2025년 12월 이전 금리는 이번에 받지 않음

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 11월 9일부터 0.1%포인트 인상 | 11월 9일부터 0.10% 포인트 인상 | S1 https://www.hf.go.kr/ko/sub05/sub05_04_05.do?mode=view&articleNo=600738 |
| 8일까지 신청 마치면 오르기 전 금리 | 11월 8일까지 보금자리론 신청을 완료하면 인상 전 금리 | S1 |
| 10년 4.90→5.00·20년 5.05→5.15·30년 5.10→5.20·50년 5.20→5.30 | 공시일 11/01·11/09 아낌e | S2 https://www.hf.go.kr/ko/interest-rate-guidance.do |
| 작년 12월 30년 3.85% | 2025-12-01 아낌e 30년 3.85 | S3 https://www.hf.go.kr/ko/interest-rate-guidance.do?srBYear=2025&srBMonth=12 |
| 1월 4.10·2월 4.25·4월 4.55·5월 4.80·7월 7일 5.10 | 달별 공시일 아낌e 30년 | S3 |
| 3·6·8~10월 그대로, 내린 달 없음 | 03·06·08·09·10월 공시 같음 | S3 |
| 올해 여섯 번·1.35%포인트 | 6번 합 1.35 | S3·S2 계산 |
| 3억 30년 월 약 141만→약 165만원(+약 24만원) | 1,406,425 → 1,647,333 (+240,908) | calc_out.txt(S2·S3 금리) |
| 8일 전·뒤 월 약 1만 8천원·30년 약 665만원 | 18,483 · 6,653,996 | calc_out.txt(S2·S3 금리) |
| 2억 94→110만(+16만)·3.6억 169→198만(+29만) | 937,616→1,098,222 · 1,687,710→1,976,799 | calc_out.txt(S2·S3 금리) |
| 30년 이자 차 약 8,673만원 | 86,726,861 | calc_out.txt(S2·S3 금리) |
| 고정금리, 대출 받은 날부터 만기까지 | 대출 받은 날부터 만기까지 안정적인 고정금리 | S4 https://www.hf.go.kr/ko/sub01/sub01_01_01.do |
| 3년 안 상환 최대 0.5%, 3억이면 최대 150만원 | 최초 실행일로부터 3년 이내 … 0.5% 한도 | S4 |
| u는 아낌e보다 0.1%p 높음 | 비대면(u방식)금리는 0.1%p 가산 | S2 · S4 |
| 규제지역 0.2%p | 규제지역인 경우 0.2%p 가산금리 | S4 |
| 우대 최대 1.0%p·신혼 0.3%p → 4.90% | 최대 1.0%p 한도 · 신혼가구 0.3%p | S2 |
| t = 은행에 직접 가서 신청 | 은행에 방문해서 직접신청하는 보금자리론 | S4 |
| 8일은 일요일 | 2026년 11월 08일 일요일 | S5 https://astro.kasi.re.kr/life/pageView/5?search_year=2026&search_month=11 |

# 올리기 전 확인
- 2026-11-05 09:22 firemap-write 발행 당일 확인 — S1~S4 다시 열어 raw1105/에 저장
  - S1 https://www.hf.go.kr/ko/sub05/sub05_04_05.do?mode=view&articleNo=600738 (raw1105/p600738.html) — 본문 같음(조회수·다음 글만 바뀜), '11월 8일까지 신청 완료하면 인상 전 금리' 그대로
  - S2 https://www.hf.go.kr/ko/interest-rate-guidance.do (raw1105/rate.html) — 11/04 받은 것과 글자 하나 다르지 않음(공시일 11/01·11/09, 30년 아낌e 5.20)
  - S3 https://www.hf.go.kr/ko/interest-rate-guidance.do?srBYear=2025&srBMonth=12 (raw1105/hist202512.html) — 같음(30년 3.85)
  - S4 https://www.hf.go.kr/ko/sub01/sub01_01_01.do (raw1105/sub01_01_01.html) — 같음
  - S3 7월분 https://www.hf.go.kr/ko/interest-rate-guidance.do?srBYear=2026&srBMonth=07 (raw1105/hist202607.html) — 같음(7/7 30년 5.10)
  - 질문 https://kin.naver.com/qna/detail.naver?dirId=4010502&docId=495013161 (raw1105/kin.html) — 질문 그대로 있음(신청일·실행일 금리)
  - S5 https://astro.kasi.re.kr/life/pageView/5?search_year=2026&search_month=11 (raw1105/kasi_cal.html) — 11월 8일 일요일
- 기준일: 2026-11-05 (금리는 공사 금리안내 공시일 2026-11-09분)
- 바뀐 것: 없음 — 30년 아낌e 11/9부터 5.20%(11/1~8 5.10%), 작년 12월 3.85% 그대로라 계산(월 +약 24만원·이번 인상분 약 1만 8천원)도 그대로
- 새로 찾은 것: 공사 보도자료 다음 글은 사장 캠페인 소식(금리와 무관) — 글에 넣을 새 사실 없음
- 2026-11-06 06:2x firemap-write 발행 당일 다시 확인 — S1~S5·질문 다시 열어 raw1106/에 저장
  - S1 https://www.hf.go.kr/ko/sub05/sub05_04_05.do?mode=view&articleNo=600738 — 조회수만 바뀜, '11월 8일까지 신청 완료' 그대로
  - S2 https://www.hf.go.kr/ko/interest-rate-guidance.do — 어제와 같음(30년 아낌e 11/9부터 5.20)
  - S3 https://www.hf.go.kr/ko/interest-rate-guidance.do?srBYear=2025&srBMonth=12 · https://www.hf.go.kr/ko/interest-rate-guidance.do?srBYear=2026&srBMonth=07 — 같음
  - S4 https://www.hf.go.kr/ko/sub01/sub01_01_01.do — 같음
  - S5 https://astro.kasi.re.kr/life/pageView/5?search_year=2026&search_month=11 — 같음
  - 질문 https://kin.naver.com/qna/detail.naver?dirId=4010502&docId=495013161 — 그대로 있음
- 기준일: 2026-11-06 (금리는 공사 금리안내 공시일 2026-11-09분)
- 바뀐 것: 없음 — 30년 아낌e 11/9부터 5.20%(11/1~8 5.10%), 작년 12월 3.85% 그대로, 계산 그대로 · 글 끝 기준일만 11월 4일→11월 6일
- 새로 찾은 것: 없음(공사 새 금리 공지 없음)
