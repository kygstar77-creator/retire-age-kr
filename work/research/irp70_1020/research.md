# irp70_1020 자료조사 (firemap-write 2026-10-20) — 카페 10/20 15:10 칸(TBD, 운영실장 07:10 지시) · 연금계좌 칸(오늘 0칸) · 형식2(계산 사례형)

## 검증
- 수요: demand.py 10/20 — 디폴트옵션 1,540 · 연금저축펀드 ETF 710 · IRP 퇴직금 260 · 퇴직연금 수익률 240 · DC형 DB형 140 (디폴트옵션은 dopt0928 #146에서 이미 씀 → 한 번도 안 쓴 '위험자산 70% 한도' 각도) · toprank 'IRP 위험자산 70%' 상위 8편이 '70%'를 90번 씀(수요 확인)
- 시기: 코스피 2025-12-30 4,214 → 2026-10-19 5,768(+37%), 오늘 이슈 '코스피 이틀 연속 상승'(연합 10/19, issues.md) — 가격 상승으로 한도 넘는 계좌가 늘 때
- 겹침: 우리 카페 '위험자산' 글 0편(grep 10/20), IRP 글(#221 예금자보호·#237 ISA 이전·#294 세액공제)과 각도 다름

## 원문
- S1 근로자퇴직급여 보장법 시행령 제26조①2가(총투자한도는 고용노동부령), 2026-10-20 lawtext.py: https://www.law.go.kr/법령/근로자퇴직급여보장법시행령/제26조
- S2 근로자퇴직급여 보장법 시행규칙 제10조①2(DC·IRP 가입자별 적립금 100분의 70), 2026-10-20: https://www.law.go.kr/법령/근로자퇴직급여보장법시행규칙/제10조
- S3 퇴직연금감독규정(금융위 고시 2023-56 현행) 제13조②(시장가치 변동으로 한도 초과 → 위반으로 보지 않음, 운용관리기관 즉시 통보) · 제11조①5·9(주식 투자한도 50% 미만 증권형·요건 갖춘 TDF), 2026-10-20: https://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=2100000231486&type=HTML (raw/kamdok.xml)
- S4 네이버 증권 일별 시세(분배금 반영) KODEX 200·TIGER 미국S&P500 2025-12-30·2026-10-19, 2026-10-20 조회: https://fchart.stock.naver.com/sise.nhn?symbol=069500&timeframe=day&count=220&requestType=0 (raw/fc_*.xml)
- S5 Yahoo 일별 종가(수정 전) 같은 두 종목·코스피, 2026-10-20 조회: https://query1.finance.yahoo.com/v8/finance/chart/069500.KS (raw/y_*.json)
- S6 KB자산운용 '연금계좌에서 투자 가능한 상품'(2026-08-05, 2차), 2026-10-20 확인: https://kbam.co.kr/pension/guide/pension-account-investment-products-guide
- S7 헤럴드경제 2026-06-23 '퇴직연금 70% 룰 족쇄 언제쯤 풀리나'(2차), 2026-10-20 확인: https://www.heraldk.com/article/2026062318205779499
- S8 미래에셋투자와연금센터 2024-01-26(2차) — 초과분 무조건 매도 아님·추가 매수 불가, 2026-10-20 확인(레드팀): http://investpension.miraeasset.com/contents/view.do?idx=20427
- S9 비즈니스워치 2026-08-12(2차) — 노동부 70→100% 논의 중단, 2026-10-20 확인: https://news.bizwatch.co.kr/article/market/2026/08/12/0034
- S10 헤럴드 2026-09-30(2차) — 폐지 검토 사실상 보류, 2026-10-20 확인: https://www.koreaherald.com/article/10889250

## 경쟁
- bench.md·bench_raw.md 참조(블로그 상위 4편+카페 1편, 2026-10-20). 1위 huck_e는 조문별로 '넘어도 위반 아님·통보·추가 매수만 거절'까지, 나머지는 70% 넘는 상황을 안 다룸. 실제 가격으로 얼마나 넘었나·얼마를 옮겨야 70%인가를 계산한 글 0편. 채권혼합형 기준이 글마다 40%·50%로 다름

## 질문
(questions_raw.md 20건 중)
1. 넘었다고 메일이 왔는데 매번 팔아야 하나, 그냥 둬도 되나(2025-12-25) — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=490981496 → 답: c01·c03(무조건 팔 필요 없음, 추가 매수만 막힘)
2. 안 팔면 자동 매도되나, 불이익 있나(2018-10-15) — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=312136055 → 답: c03 '강제로 팔리지는 않아요'
3. 71%인데 강제매매인가 추가 매수만 막히나(2026-05-13, 조회 2,391) — https://cafe.naver.com/dlxogns01/385733 → 답: c01(미래에셋·KB 안내)
4. 은행 DC 71%에서 예수금으로 예금도 못 산다(2026-05-12) — https://cafe.naver.com/divclub/51499 → 답: c03 '금융회사마다 처리가 다를 수 있으니 물어보세요'
5. 월 적립금이 들어와도 70% 초과면 주문이 안 들어간다(2026-10-02) — https://cafe.naver.com/divclub/64794 → 답: c03(넘은 동안 새 돈은 안전자산 쪽)
6. 비율은 어디서 보고 어떻게 맞춰지나(2025-11-01, 조회 4,050) — https://cafe.naver.com/dlxogns01/324185 → 답: c03(금융회사 앱·고객센터)·c02(70%까지 금액)

## 왜
- 70% 한도를 두는 이유: 시행령 제26조 제목이 '적립금의 안정적 운용을 위한 운용방법 및 기준' — 원문에 이 이상 설명 없음
- 가격 상승 초과를 위반으로 안 보는 이유: 감독규정 제13조② 원문에 이유 문장 없음(가입자가 고른 뒤 시장가치가 변한 경우라는 조건만)
- 국내 ETF 계좌만 크게 넘은 이유: 같은 기간 KODEX 200 +47.7%, TIGER 미국S&P500 +3.1%(원화 종가, S5) — 오른 폭 차이

## 그래서
- 할 일: 문자를 받아도 팔 의무 없음·기한 없음(S3 ②). 넘은 동안 새 돈은 30% 쪽(예금·채권형·주식 50% 미만 채권혼합형·요건 갖춘 TDF)
- 70%까지 내려가려면: 1억 계좌 KODEX 200 약 1,000만원어치, S&P500 약 64만원어치(calc_out.txt, 분배금 뺀 가격) — 의무 아님
- 더 살 수 있는 돈 = 평가금액 × 70% − 위험자산
- 한도 없는 계좌: 연금저축(S6) — 권유 아님, 계좌별 차이로만 씀

## 누구라면
- 국내 주식형 ETF를 70% 가까이 담은 사람: 올해 가격만으로 77.5% → 안내 문자 대상
- 미국 지수 ETF를 담은 사람: 같은 기간 원화 종가 +3.1%라 70.6%, 거의 그대로
- 연금 받는 중인 은퇴자: 예금 쪽에서만 돈이 빠지면 위험자산 비중이 올라감(산수) — c04
- 예금 위주: 해당 없음(위험자산 비중이 낮음)

## 함정
- 70%는 상품별이 아니라 계좌 전체 합(S2 '가입자별 전체 적립금')
- 은행 계좌는 넘은 상태에서 예금 매수·종목 교체까지 막혔다는 사례(카페 51499·384227) — 금융회사마다 다를 수 있음
- 채권혼합형 분류 기준이 원문(주식 50% 미만)과 운용사 안내(40%)가 다르게 적힘 → 앱 분류 확인

## 우리만
- 2025-12-30에 70:30으로 담은 1억 계좌를 2026-10-19 분배금 반영 가격으로 다시 계산: KODEX 200 77.5%·TIGER 미국S&P500 70.6%, 70%까지 금액 약 1,000만원·64만원(calc_out.txt) — 경쟁 상위 글은 '주가가 오르면 넘을 수 있다'를 말로만(bench_raw.md)

## 예외
- 적격 TDF·사전지정운용(디폴트옵션)은 70% 밖(S3 제11조①9·10) — 이 글의 계산에서는 다루지 않음
- 가격 변동이 아닌 이유(합병·경비 감소 등)로 넘은 경우는 '다음 운용방법 변경 때까지'(S3 ③) — 다른 조건

## 한계
- 감독규정 제13조②의 '위반으로 보지 않음'은 문언상 감독규정 제10~12조 한도 대상(레드팀) — 70% 한도(시행규칙)에 바로 적용된다고 쓰지 않고 '같은 취지 조항이 있다'로만 씀, 강제 매도 없음은 S6·S8 안내로
- 추가 매수가 막힌다는 건 원문 조항이 아니라 한도 자체에서 나오는 결과이고, 실제 처리(주문 거절 방식)는 금융회사 안내(S6·S7 사례)로만 확인
- 예금 이자를 빼고 계산 → 실제 비중은 조금 낮음
- 연금저축 한도 없음: 70% 조문 대상이 DB·DC·IRP뿐이고 소득세법 시행령 제40조의2에 비중 한도 없음(레드팀 확인) — '없다'를 적은 조문은 없음
- 12/30 수정 전 종가는 야후만(네이버는 분배금 반영 60,440), 10/19는 두 곳 같음(89,930·25,505)
- 한도 완화: 6월 검토 중 → 8월 중단·9월 보류(언론, S9·S10) — 고용노동부 공식 자료 확인 안 함

## 대조
| 항목 | 원문 값 | 글 값 | 출처 |
|---|---|---|---|
| DC·IRP 위험자산 총투자한도 | 100분의 70 | 70% | S2 https://www.law.go.kr/법령/근로자퇴직급여보장법시행규칙/제10조 |
| 가격 상승 초과(감독규정 한도) | 위반으로 보지 않음·즉시 통보 | 같은 취지 조항이 있다 | S3 https://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=2100000231486&type=HTML |
| 채권혼합형 | 주식 투자한도 100분의 50 미만 | 주식 50% 미만 | S3 https://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=2100000231486&type=HTML |
| 강제 매도 없음·추가 매수 불가(2차) | 무조건 매도 아님·추가 매수 불가 | 강제로 팔리지 않음·더 살 수 없음 | S8 http://investpension.miraeasset.com/contents/view.do?idx=20427 · S6 https://kbam.co.kr/pension/guide/pension-account-investment-products-guide |
| 운용사 안내 혼합형 기준(2차) | 40% | 40% | S6 https://kbam.co.kr/pension/guide/pension-account-investment-products-guide · bench https://blog.naver.com/spman2/224440631781 |
| 연금저축 한도 | 70% 조문은 DB·DC·IRP만 | 한도 없음 | S2 https://www.law.go.kr/법령/근로자퇴직급여보장법시행규칙/제10조 |
| KODEX 200 12/30 → 10/19(2차) | 60,895 → 89,930 (+47.68%) | 약 48% | S5 https://query1.finance.yahoo.com/v8/finance/chart/069500.KS · S4 https://fchart.stock.naver.com/sise.nhn?symbol=069500&timeframe=day&count=220&requestType=0 |
| TIGER 미국S&P500(2차) | 24,750 → 25,505 (+3.05%) | 약 3% | S5 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS · S4 https://fchart.stock.naver.com/sise.nhn?symbol=360750&timeframe=day&count=220&requestType=0 |
| KODEX 계좌 위험 비중(2차) | 10,338/13,338 = 77.5% | 77.5% | S5 https://query1.finance.yahoo.com/v8/finance/chart/069500.KS · S4 https://fchart.stock.naver.com/sise.nhn?symbol=069500&timeframe=day&count=220&requestType=0 |
| S&P 계좌 위험 비중(2차) | 7,214/10,214 = 70.6% | 70.6% | S5 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS · S4 https://fchart.stock.naver.com/sise.nhn?symbol=360750&timeframe=day&count=220&requestType=0 |
| 70%까지 금액(2차) | 1,001만 · 64만 | 약 1,000만원 · 약 64만원 | S5 https://query1.finance.yahoo.com/v8/finance/chart/069500.KS · S4 https://fchart.stock.naver.com/sise.nhn?symbol=069500&timeframe=day&count=220&requestType=0 |
| 완화 논의(2차) | 6/23 검토 중 → 8/12 중단 → 9/30 보류 | 멈춘 상태 | S9 https://news.bizwatch.co.kr/article/market/2026/08/12/0034 · S10 https://www.koreaherald.com/article/10889250 · S7 https://www.heraldk.com/article/2026062318205779499 |

# 올리기 전 확인
- 날짜: 2026-10-20 (발행 같은 날 12:2x~12:5x 조사·다시 확인)
- 다시 연 원문: https://www.law.go.kr/법령/근로자퇴직급여보장법시행령/제26조 · https://www.law.go.kr/법령/근로자퇴직급여보장법시행규칙/제10조 · https://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=2100000231486&type=HTML · https://kbam.co.kr/pension/guide/pension-account-investment-products-guide · https://www.heraldk.com/article/2026062318205779499 · http://investpension.miraeasset.com/contents/view.do?idx=20427 · https://news.bizwatch.co.kr/article/market/2026/08/12/0034 · https://www.koreaherald.com/article/10889250 · https://query1.finance.yahoo.com/v8/finance/chart/069500.KS · https://query1.finance.yahoo.com/v8/finance/chart/360750.KS · https://fchart.stock.naver.com/sise.nhn?symbol=069500&timeframe=day&count=220&requestType=0 · https://fchart.stock.naver.com/sise.nhn?symbol=360750&timeframe=day&count=220&requestType=0 · https://blog.naver.com/spman2/224440631781
- 기준일: ETF 2025-12-30·2026-10-19 15:30 종가(10/20 조회) · 감독규정 2023-11-16 시행 현행(10/20 조회) · 시행규칙 현행(10/20 조회)
- 바뀐 것: 처음 쓴 '6월 기준 검토 중' → 8/12 중단·9/30 보류 보도로 고침. 분배금 반영 가격(77.6%) → 분배금 뺀 가격(77.5%)으로 바꿈(이해 시험 지적)
- 새로 찾은 것: 카페에서 은행 계좌는 넘은 상태에서 예금 매수·종목 교체까지 막혔다는 사례(divclub 51499, 2026-05-12) · 미래에셋 안내(2024-01-26)
