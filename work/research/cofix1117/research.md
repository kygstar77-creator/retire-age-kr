# cofix1117 자료조사 (카페 2026-11-18 07:40 칸 — firemap-write-b 11/16 23:1x) — 경제·금리: 10월 코픽스 3.62%, 1년 새 세 가지 코픽스별 이자 차이

## 검증
- 수요: work/kwvol.py 11/16 23:1x — 주담대금리 30,780 · 코픽스금리 6,760 · 코픽스 5,630 · 신잔액코픽스 430
- 겹침: 우리 제목 중 '코픽스' 3편(cofix10·mortgage·reone0925) 모두 9월 블로그(blog.naver.com/kygstar7777) — 카페 0편 · 같은 날 칸(11/18 10:10 정책·돈 관리)과 축 겹침 없음 · 앞 칸 11/17 18:40 부동산·22:40 배당ETF 짝 → 장르 3칸 연속 아님 · selfcheck [중복] 카페 #407 '주담대 금리 5년 고정 끝나면, 한 달 얼마 더 낼까?'는 고정 기간 끝난 뒤 갈아탈 금리 각도, 이번은 세 코픽스 1년 상승폭 각도라 다름
- 경쟁에서 터진 증거: toprank '코픽스' 블로그 상위 8편 모두 2주 안(11/3~11/16) 작성(raw/toprank.txt) — 공시 날마다 새 글이 붙는 주제 · 8편 모두 전월 대비(0.19·0.25%p)만, 1년 동안 세 가지 코픽스별 이자 차이를 낸 글 0편

## 원문
- S1 은행연합회 소비자포털 COFIX 공시(1차) — 2026-11-16 23:1x 확인(raw/cofix.html·cofix.txt): 10월분 신규 3.62·잔액 3.26·신잔액 2.93, 공시일 2026.11.16, 다음 공시일 2026.12.15, '모든 COFIX는 공시일 오후 3시에 공시' https://portal.kfb.or.kr/fingoods/cofix.php
- S2 같은 사이트 COFIX 월별 통계 엑셀 2025·2026(1차) — 2026-11-16 23:1x 받음(raw/cofix_month_2025.xlsx·cofix_month_2026.xlsx): https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026
- S3 은행연합회 COFIX 개요(1차) — 2026-11-16 23:1x 확인(raw/overview.txt): 정의·정보제공은행 8곳·신규/잔액/신잔액 산출방법 https://portal.kfb.or.kr/compare/cofix_overview.php
- S5 은행연합회 소비자포털 '대출금리에 대한 이해'(1차) — 2026-11-16 23:4x 확인(raw/loan.txt): 대출금리 = 대출 기준금리 + 가산금리, 약정서 표시 예시 '잔액기준 COFIX + 1.3%' https://portal.kfb.or.kr/compare/loan.php
- S4 한국은행 경제통계시스템 기준금리(722Y001, 1차) — 2026-11-16 23:2x work/apis.py ecos(): 2025/10 2.5 → 2026-07-16 2.75 → 2026-08-27 3.00 https://ecos.bok.or.kr (722Y001 apis.ecos)

## 경쟁
(bench.md 8편) 1·2·6위 세 가지 코픽스 정의·이번 달 숫자, 3·5위 언제 내 대출에 반영되나(금리 변경일), 4위 기준금리와 비교, 7위 내렸는데 왜 그대로, 8위 '2년 8개월 만에 최고'·은행별 금리 인상폭·신규 vs 잔액 선택. 빠뜨린 것: 1년 단위로 본 세 코픽스 상승폭 차이(1.05 vs 0.42 vs 0.45%p)와 그에 따른 3억원 이자 차이, 1년 전엔 신규가 잔액보다 낮았다가 순서가 바뀐 것

## 질문
1. 코픽스 올랐으면 내 대출 이자는 얼마나 늘었나? — https://blog.naver.com/easy-moneylog/224474895318 ('3억 남았다면 한 달 이자는 얼마나 달라질까') → 답: c00·c02(1년 약 315만원·한 달 약 26만원)
2. 신규취급액·잔액·신잔액 중 뭐가 다르고 어디가 유리한가? — https://blog.naver.com/miso1c8o9/224479289285 ('주담대 신규 vs 잔액 기준 어디가 유리할까?') → 답: c01·c03·c04(1년 상승폭 차이, 순서 바뀜)
3. 기준금리랑 코픽스는 어떻게 다른가? — https://blog.naver.com/ha_kaug/224471422000 ('코픽스 기준금리와 한국은행 기준금리 비교') → 답: c01(기준금리 0.5%p vs 신규 코픽스 1.05%p)·c03(코픽스 정의)
4. 다음 코픽스는 언제 나오나? — https://blog.naver.com/dutyfrees/224479208220 ('코픽스 금리 2026년 11월 공시') → 답: c04(12월 15일 오후 3시)

## 왜
- 신규취급액 기준이 더 많이 오른 이유: S3 정의 — 신규는 '대상월 한 달 동안 신규로 취급한' 수신 금리, 잔액은 '대상월말 보유하고 있는 수신상품 잔액' 금리 → 잔액에는 그 전에 들어온 돈이 섞임(정의에서 나온 설명, 글에 '천천히 움직인다'로만)
- 신잔액이 가장 낮은 이유: S3 '기타 예수금, 기타 차입금, 결제성자금 등을 추가로 포함' — 숫자로는 13달 내내 셋 중 가장 낮음(S2). 결제성자금이 왜 금리를 낮추는지는 원문에 없음 → 글은 '더해서 가장 낮게 나온다'(관찰)만
- 이번에 오른 이유: S1·S3에 이유 없음 → 글에 '공시에 따로 적혀 있지 않다'고 씀

## 그래서
- 내 대출이 세 코픽스 중 어디에 묶였는지 대출 약정서에서 확인 — 같은 3억원도 1년 이자 증가가 180만원 넘게 갈림(c02)
- 다음 공시 12월 15일 오후 3시(S1)

## 누구라면
- 신규취급액 코픽스 변동금리 대출: 3억원이면 1년 약 315만원·1억원이면 약 105만원 이자 증가
- 잔액·신잔액 코픽스 대출: 3억원이면 1년 약 126만원·135만원
- 고정금리 대출·혼합형 고정 기간 중: 이 계산에 해당 안 됨(c02 끝 줄)

## 함정
- '신규취급액 기준이 더 싸다'는 1년 전 숫자(2.57 < 2.84)로는 맞았지만 지금은 신규가 잔액보다 0.36%p 높음 — 순서가 바뀜(S2)
- 전월 대비(0.19%p)만 보면 작아 보이지만 1년으로 보면 1.05%p — 기준금리 상승폭 0.5%p의 두 배 넘음

## 우리만
- 은행연합회 월별 엑셀 13달 치로 세 코픽스 1년 상승폭(1.05·0.42·0.45%p)과 3억원 기준 1년 이자 증가(315·126·135만원) 직접 계산, 기준금리 상승폭(ECOS)과 비교 — 경쟁 8편 0편(calc_out.txt)

## 예외
- 고정금리·혼합형 고정 기간: 코픽스와 무관
- 가산금리가 바뀐 경우·원금을 갚아 잔액이 줄어든 경우: 실제 증가액이 다름(계산은 원금·가산금리 그대로 가정)
- 금리 변경 주기 때문에 아직 새 코픽스가 반영 안 된 대출: 지금 내는 이자와 다름

## 한계
- 내 대출에 새 코픽스가 언제 반영되는지(금리 변경 주기)는 은행 약정마다 달라 1차 원문을 이번에 확인하지 않음 → 글에 주기 숫자를 쓰지 않음
- 코픽스가 이번에 오른 이유는 은행연합회 공시에 없음
- 산출 대상 수신상품 8개 이름은 개요 쪽에 그림으로만 있어 글에 적지 않음
- 이자 증가액은 원금·가산금리 그대로, 1년 내내 같은 금리라고 본 단순 계산

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 11월 16일 공시, 10월 신규취급액 기준 3.62% | 공시일 2026.11.16 · 대상월 2026/10 · 신규 3.62 | S1 https://portal.kfb.or.kr/fingoods/cofix.php · S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 |
| 1년 전보다 1.05%p, 2025년 10월 2.57% | 대상월 2025/10 신규 2.57 → 3.62−2.57=1.05 | S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2025 (calc_out.txt) |
| 잔액 기준 0.42%p 올라 3.26%, 1년 전 2.84% | 2.84 → 3.26 | S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 |
| 신잔액 기준 0.45%p 올라 2.93% | 2.48 → 2.93 | S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 |
| 월별 공시 13달 치 | 대상월 2025/10~2026/10 13줄 | S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 |
| 기준금리 7월·8월 두 번 올라 3.00%, 1년 0.5%p | 2026-07-16 2.75 · 2026-08-27 3.00 · 2025/10 2.5 | S4 https://ecos.bok.or.kr (722Y001 apis.ecos) |
| 기준금리보다 두 배 넘게 | 1.05/0.5=2.1 | 직접 계산 · S2 · S4 |
| 3억원 1년 약 315만원·한 달 약 26만원 | 3억×1.05%=315만 · ÷12=26.2만 | 직접 계산 · S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 (calc_out.txt) |
| 잔액 1년 약 126만원·한 달 약 10만원 | 3억×0.42%=126만 · ÷12=10.5만 | 직접 계산 · S2 |
| 신잔액 1년 약 135만원·한 달 약 11만원 | 3억×0.45%=135만 · ÷12=11.25만 | 직접 계산 · S2 |
| 180만원 넘게 차이 | 315−135=180 · 315−126=189 | 직접 계산 · S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 |
| 1억원 1년 약 105만원 | 1억×1.05%=105만 | 직접 계산 · S2 https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 |
| 은행 8곳이 예금 등으로 돈을 모을 때 준 금리를 금액에 맞춰 평균 | '정보제공은행들의 자금조달금리를 가중평균' · 정보제공은행 총 8개 · '수신상품의 금액과 금리를 가중평균' | S3 https://portal.kfb.or.kr/compare/cofix_overview.php |
| 신규는 그 달 새로 들어온 돈, 잔액은 달 끝 남은 돈 전체 | '대상월 한 달 동안 신규로 취급한…' · '대상월말 보유하고 있는 수신상품 잔액' | S3 https://portal.kfb.or.kr/compare/cofix_overview.php |
| 신잔액은 은행 사이 예금·한국은행 차입금 같은 돈까지 더함 | '기타 예수금(은행간거래 정기예금 등), 기타 차입금(한국은행차입금 등), 결제성자금 등을 추가로 포함' | S3 https://portal.kfb.or.kr/compare/cofix_overview.php |
| 셋 중 가장 낮게 | 2026/10 2.93 < 3.26 < 3.62 | S1 https://portal.kfb.or.kr/fingoods/cofix.php |
| 지금은 신규가 잔액보다 0.36%p 높음 | 3.62−3.26=0.36 | S1 https://portal.kfb.or.kr/fingoods/cofix.php |
| 가산금리는 은행이 운영 비용이나 떼일 위험 등을 따져 정하는 몫 | '가산금리란 … 업무원가, 법적비용, 위험프리미엄, 목표이익률, 가감조정금리 등' | S5 https://portal.kfb.or.kr/compare/loan.php |
| 변동금리 대출 금리는 코픽스에 가산금리를 얹어 정함 | '대출 기준금리와 가산금리를 합산하여 결정' | S5 https://portal.kfb.or.kr/compare/loan.php |
| 약정서에 보통 '잔액기준 코픽스(COFIX) + 1.3%'처럼 적힘 | '대출약정서 등에는 일반적으로 "잔액기준 COFIX + 1.3%" … 합으로 대출금리가 표시' | S5 https://portal.kfb.or.kr/compare/loan.php |
| 신잔액은 예금 말고 은행이 빌린 돈 등까지 넣어 계산 | '기타 차입금(한국은행차입금, 정부차입금, 후순위채…) … 추가로 포함' | S3 https://portal.kfb.or.kr/compare/cofix_overview.php |
| 다음 공시 12월 15일 오후 3시 | '다음 공시일 : 2026. 12. 15.' · '공시일 오후 3시에 공시' | S1 https://portal.kfb.or.kr/fingoods/cofix.php |

# 올리기 전 확인
- 2026-11-18 14:4x firemap-write-b(발행 날 다시 확인, 칸 11/18 18:40). 바뀐 것: 그대로 — 은행연합회 2026.11.16 공시(10월분) 신규 3.62%·잔액 3.26%·신잔액 2.93%, 다음 공시 12/15 · 한국은행 기준금리 3.00%(ECOS 722Y001 2026.10 값, 다음 금통위 11/26) · 단기 COFIX 11/18 공시는 글에 안 씀
- 다시 연 주소(11/18, 모두 HTTP 200): https://portal.kfb.or.kr/fingoods/cofix.php · https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 · https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2025 · https://portal.kfb.or.kr/compare/cofix_overview.php · https://portal.kfb.or.kr/compare/loan.php · https://ecos.bok.or.kr
- 기준일: 은행연합회 COFIX 2026.11.16 공시(2026년 10월분) · 한국은행 기준금리 2026.11.18 조회 3.00%
- 새로 찾은 것: 없음(11/16 뒤 새 COFIX 공시·금통위 없음, 숫자 그대로 발행)
- 2026-11-16 23:1x firemap-write-b(조사·작성 날, 발행 11/18 07:40). 금리 글이라 발행 회차가 당일 S1·S2를 다시 열고 '바뀐 것:'에 숫자를 적을 것(코픽스 월별 다음 공시 12/15 · 금통위 다음 11/26 — 둘 다 발행 뒤)
- 다시 연 주소: https://portal.kfb.or.kr/fingoods/cofix.php · https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2026 · https://portal.kfb.or.kr/fingoods/cofix_excel_jan.php?BasicYear=2025 · https://portal.kfb.or.kr/compare/cofix_overview.php · https://portal.kfb.or.kr/compare/loan.php · https://ecos.bok.or.kr (722Y001 apis.ecos, 23:2x)
- 기준일: 은행연합회 COFIX 2026.11.16 공시(2026년 10월분) · 한국은행 기준금리 2026.11.16 조회 3.00%
- 바뀐 것: 처음 조사 — 신규 3.43→3.62%(전월), 1년 2.57→3.62%
- 새로 찾은 것: 세 코픽스 1년 상승폭 1.05·0.42·0.45%p, 3억원 1년 이자 증가 315·126·135만원
- 조사 뒤 공표: data/release_calendar.json 확인 — 다음 COFIX 12/15, 다음 금통위 11/26(둘 다 발행 11/18 뒤라 숫자 안 바뀜). 단기 COFIX는 11/18 공시(글에 안 씀)

# 교차검증 (crosscheck 11/16 23:27, gemini-3.5-flash-lite — OpenAI 키 없음)
- 사실 지적 2건: 반영 0 · 유지 2 — ① 2025년 10월 잔액·신잔액 값 안 씀: 그림 01과 c04에 1년 전 값 있음, 대조표 S2 ② '이유 공시에 없음': S1·S3 다시 봐도 원인 문장 없음(한계 칸)
- 말투 4건: 반영 1(c02 가정 문장을 목록 앞에 — 이미 그렇게 됨) · 유지 3 — ① 첫 문장 바꾸기: 카페 첫 3줄 꼴(독자 상황→결론 숫자)과 결론 문장 되풀이라 유지 ② 과정 문장 뒤로: 같은 꼴 셋째 줄(무엇을 셌는지) ③ '움직입니다→움직여요': 바꿔 보니 aitell 9.x→12.9('~요' 연속)라 되돌림
