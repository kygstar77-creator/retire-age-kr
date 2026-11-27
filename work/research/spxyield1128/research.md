# spxyield1128 자료조사 (카페 11/28 18:40 배당 칸) — S&P500(SPY) 배당수익률 33년, 지금 1.06%는 395달 중 어디쯤인가 (통계·기록형 form 4)

## 상태 (11/27 16:4x write-b)
- 16:4x write-b 회차: 주제 검증(수요·겹침)·원자료 받기(fetch.py)·직접 계산(calc.py → calc_out.txt)·운용사 원문 2곳·경쟁 5편 본문·표지(bench_raw)·질문 3개 주소·조각·그림·검사·이해 시험·editgate
- 발행 회차(11/28 18:1x write): fetch.py·calc.py·mkimg.py 다시(11/27 종가 — 11/27은 미국 조기 폐장일이지만 종가 있음) → 숫자 바뀌면 c0*·facts·대조 고치고 재서명, '올리기 전 확인' 날짜 갱신

## 검증
- 수요: kwvol 11/27 16:4x — S&P500배당 690 · VOO배당금 680 · SPY배당금 100 · VOO배당 90 · SPY배당 80 (자동완성 's&p500 배당률'·'s&p500 배당금 1억' 있음) · 커버드콜·고배당ETF는 11/27 jepivix·11/28 hidiv와 겹쳐 뺌
- 경쟁에서 터진 증거: toprank 'S&P500 배당률' 블로그 상위 8편 중 6편이 11월 글(주제 뜨거움) · 5위 hwakseye1 'SPYD 분배율 4.29%, S&P500보다 배당 4배인데…' 댓글 76(나머지 0~1) — S&P500 배당률 숫자 글 반응 큼 · 7위 finance_study '역사상 최저치' 글(배런스 칼럼 옮김, 사진 0)
- 우리 실측: textrule 11/26 형식 4 우세 · 배당 축 11/26·27 decdiv·schdhold·divdj·jepivix 모두 상품 글 — 지수 전체 배당률 기록은 0편
- 겹침: 같은 날 10:10 sq1pair1128(나스닥100+SCHD 비율)·12:40 hidiv1128(VYM·HDV·SPYD 10년)·16:10 forenon1128(부동산)·22:40 k1split1128(코스피) — 대상·각도 다름 · 옛 글 c1cafe1011 'S&P500 배당 vs 팔아서 쓰기'(인출 기간)·sp500dist1112 '분배금 KODEX 두 배'(국내 상품 분배)·spx10y1122(손해 본 기간) — 배당수익률 33년 위치는 0편

## 원문
- S1 야후 파이낸스 chart API 일별 종가·배당 events SPY(1993-01-29~)·VOO(2010-09-09~), ~2026-11-25 종가(11/26 미국 휴장), 11/27 16:47 받음(raw/SPY.json·VOO.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/SPY
- S2 스테이트스트리트 SPY 공식 — Distribution Yield 1.06%('sum of the distributions within the past 365 days divided by NAV') · Index Dividend Yield 1.18%('underlyings' indicated annual dividend divided by price') · Gross Expense Ratio 0.0945% · Distribution Frequency Quarterly · Inception Jan 22 1993 · Benchmark S&P 500 Index · Number of Holdings 504 · NAV 716.71달러, 11/27 16:48 받음(raw/spy_1127.html): https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy
- S3 뱅가드 VOO 공식 — expenseRatio 0.0300%(2026-04-28) · inception 2010-09-07 · distributionFrequency Quarterly · 최근 4회 1.771000·1.872400·1.962200·1.822600달러(합 7.4282 = 야후 7.428), 11/27 16:48 받음(raw/voo_profile_1127.json·voo_dist_1127.json): https://investor.vanguard.com/vmf/api/VOO/profile · https://investor.vanguard.com/vmf/api/VOO/distribution
- S4 미국 배당 제한세율 15% — 국세청 조세조약상 제한세율 규정표(2021.2) 미국 행(hidiv1128 11/27 13:4x 받은 raw/nts_treaty_1127.html 같은 쪽): https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238

## 우리만 (calc_out.txt, 11/25 종가)
- SPY 배당수익률 1.06% — 1994-01~2026-11 395달 중 더 낮았던 달 19개(1999-12~2000-10 11개·2026년 8개), 낮은 쪽 5%
- 가장 낮은 달 2000-08 0.94% · 가장 높은 달 2009-02 3.68% · 가운데값 1.76% · 2010년대 평균 1.91% · 2020년 뒤 1.37%
- 10년 배당 1.71배 vs 주가 3.24배 · 20년 3.26 vs 5.11 · 30년 5.54 vs 9.53
- 1년 배당 줄어든 해 2001 −5.4% · 2005 −2.2% · 2009 −20.0% · 올해 9월까지 세 번 5.59달러(작년 같은 세 번 +5.7%)
- VOO 1.13% → 1억원 세전 약 113만 · 세후 약 96만 · 세후 월 100만에 약 12억 5천만

## 질문
- Q1 S&P500(SPY) 배당이 줄어드는 거 아니냐(지식iN 'spy etf 배당성장률 왜 이런가요? … 배당성장률이 마이너스인지'): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=486483216 → 우리 답: 1994~2025 해마다 배당 합이 줄어든 해는 2001·2005·2009 세 번, 크게 준 건 2009년 −20% 한 번 · 올해 9월까지는 작년보다 5.7% 많음
- Q2 S&P500 배당률은 얼마이고 낮은 건가(네이버 자동완성 's&p500 배당률'): https://ac.search.naver.com/nx/ac?q=S%26P500%20%EB%B0%B0%EB%8B%B9&st=100&r_format=json → 우리 답: 지금 SPY 1.06%, 1994년 뒤 395달 중 낮은 쪽 5%, 가장 낮은 때는 2000년 8월 0.94%
- Q3 S&P500에 1억이면 배당 얼마(네이버 자동완성 's&p500 배당금 1억'): https://ac.search.naver.com/nx/ac?q=S%26P500%20%EB%B0%B0%EB%8B%B9&st=100&r_format=json → 우리 답: VOO 1.13%로 세전 약 113만·미국 15% 떼면 약 96만원, 석 달마다 약 24만원
- Q4 SPY·VOO 배당은 언제 들어오나(지식iN '미국 s&p 500 spy, voo 시작했는데 배당금이 안들어왔습니다'): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=494113775 → 우리 답: 둘 다 석 달마다(S2·S3) — 지급일 상세는 글에 안 씀(이번 글 주제 밖)

## 왜
- 왜 배당률이 낮아졌나: 1주 배당은 10년 1.71배 늘었는데 주가가 3.24배 올라 비율이 내려감(S1 calc) — 회사들이 왜 배당을 덜 늘렸는지(자사주 매입·기술주 비중 등)는 이번에 본 1차 원문에 없음 → 글에 안 씀(경쟁 7은 배런스 칼럼으로 기술주 비중을 들었지만 우리는 원문 확인 안 함)
- 왜 2009년 2월 3.68%: 주가가 크게 떨어진 때(2009-02-27 종가 S1) — 배당은 그해 20% 줄었지만 주가가 더 많이 떨어짐
- 왜 2009년 배당이 줄었나: 원문(S2·S3)에 이유 없음 — 숫자만
- 왜 분배수익률과 지수 배당수익률이 다른가: S2 정의 — 지난 365일 실제 분배 ÷ NAV vs 담긴 회사 지금 배당을 1년으로 잡은 값 ÷ 가격
- 왜 15%: 한미 조세조약 배당 제한세율 15%(S4)

## 그래서
- '배당률이 낮다 = 배당이 줄었다'가 아님 → 1주 배당 금액이 늘었는지 따로 봄(숫자만, 권유 없음)
- S&P500 ETF로 배당 생활비를 생각한다면: 지금 배당률로 세후 월 100만원에 약 12억 5천만원 필요 — 계산 결과만 제시
- 운용사 화면에서 배당률 볼 때: 지난 1년 실제 받은 돈은 분배수익률(1.06%), 지수 배당수익률(1.18%)은 앞으로 잡은 값

## 누구라면
- S&P500 ETF를 들고 배당을 다시 사는 사람: 배당률보다 1주 배당 금액 추이(10년 1.71배)를 봄
- 배당으로 생활비를 받으려는 사람: 1억원에 세후 1년 약 96만원, 석 달마다 약 24만원
- 2000년 무렵 기억이 있는 사람: 그때(0.94%)가 지금(1.06%)보다 더 낮았음

## 함정
- 흔한 말 '역대 최저': SPY 기록(1994~) 안에서는 2000년 8월 0.94%가 더 낮음 — 지금은 395달 중 20번째로 낮음
- 배당률이 낮으면 배당이 줄었다고 여기기 — 1주 배당은 33년 중 세 해만 줄었음
- 운용사 화면의 지수 배당수익률(1.18%)을 지난 1년 받은 배당으로 여기기 — 실제 지난 1년은 분배수익률 1.06%

## 한계
- S&P500 지수 자체가 아니라 SPY(1993년 상장) 기록 — 1993년 전(예: 1871년부터의 장기 지수 자료)은 안 봄 → 글에 '1994년 뒤·SPY 기록'으로만 씀
- 달마다 마지막 거래일 값만 셈(하루하루 값으로 세면 최저일·순위가 조금 다를 수 있음)
- 배당락일 기준 1년 합 — 지급일 기준과 몇 주 차이
- 환율 뺌(달러 기준 비율에 1억원 곱함) · 국내 추가 세금·건보료 뺌 · 국내 상장 S&P500 ETF 분배는 다른 글(sp500dist1112)
- SPY(1.06%)와 VOO(1.13%) 차이의 이유는 원문 확인 안 함 → 글에 이유 안 씀
- 2026년은 9월 배당까지(12월 배당은 발행 뒤)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| SPY 배당수익률 지금 1.06% | 7.583 ÷ 716.70 = 1.058% · 운용사 Distribution Yield 1.06% | S1 calc_out.txt · S2 https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy |
| 395달 중 더 낮았던 달 19번(1999-12~2000-10 11번·올해 8번) | 19개 목록 | S1 calc_out.txt '지금(1.06%)보다 낮았던 달' |
| 가장 낮은 달 2000년 8월 0.94% · 가장 높은 달 2009년 2월 3.68% | 0.94 · 3.68 | S1 calc_out.txt |
| 33년 가운데값 1.76% · 2010년대 평균 1.91% · 2020년 뒤 1.37% | 1.76 · 1.91 · 1.37 | S1 calc_out.txt |
| 1주 1년 배당 10년 전 4.42 → 지금 7.58달러 1.7배 · 주가 3.2배 | 4.422 → 7.583 · 221.52 → 716.70 | S1 calc_out.txt '10년 전' |
| 30년 배당 5.5배 · 주가 9.5배 | 5.54 · 9.53 | S1 calc_out.txt '30년 전' |
| 줄어든 해 2001 5%·2005 2%·2009 20%(2.18달러) | −5.4 · −2.2 · −20.0 (2.721 → 2.177) | S1 calc_out.txt '해마다 배당 합' |
| 올해 9월까지 세 번 5.59달러, 작년 같은 세 번보다 6% 많음 | 5.590 · 5.288 | S1 calc_out.txt |
| VOO 지난 1년 배당 7.43달러 · 1.13% | 7.428 ÷ 658.87 · 운용사 4회 합 7.4282 | S1 calc_out.txt · S3 https://investor.vanguard.com/vmf/api/VOO/distribution |
| VOO 1억원 → 세전 약 113만 · 세후 약 96만 · 석 달 약 24만 | 1,127,385 · 958,277 · 239,569 | S1 calc_out.txt · 15% S4 https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 |
| 세후 월 100만원 → 약 12억 5천만원 | 1,252,247,449 | S1 calc_out.txt |
| 분배수익률 1.06% · 지수 배당수익률 1.18%(정의) | Distribution Yield 1.06% · Index Dividend Yield 1.18% | S2 https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy |
| 배당 석 달마다 | Quarterly · Quarterly | S2 · S3 https://investor.vanguard.com/vmf/api/VOO/profile |

# 올리기 전 확인
- 확인일: 2026-11-27 17:2x (write-b, 16:4x 처음·17:00 지식iN 다시) — 발행 11/28 18:40, 1일 안. 발행 회차가 11/28에 다시 확인하면 이 칸을 고침
- 기준일: 2026-11-25 미국 정규장 종가(11/26 추수감사절 휴장)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/SPY (VOO 같은 꼴, 16:47 받은 raw) · https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy · https://investor.vanguard.com/vmf/api/VOO/profile · https://investor.vanguard.com/vmf/api/VOO/distribution · https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 · https://kin.naver.com/qna/detail.naver?dirId=40102&docId=494113775 (17:00 다시 열어 200, 질문 그대로)
- 바뀐 것: 처음 계산(16:47) 뒤 새 종가 없음(11/26 휴장, 11/27 장 아직) — 숫자 그대로. 운용사 SPY 분배수익률 1.06%가 우리 계산과 같음을 확인
- 새로 찾은 것: SPY 지수 배당수익률 1.18%(분배수익률과 셈법 다름) · VOO 최근 4회 분배 원문 합 7.4282달러 = 야후 7.428 · SPY 보유 504종목
- 조사 뒤 공표: data/release_calendar.json 해당 없음(SPY·VOO 12월 분배는 12월 중순, 발행 뒤)

## 경쟁 (bench.md — toprank 'S&P500 배당률' 블로그 상위 8, 본문 5편)
- 1 VOO로 월 300만 원 받으려면(분배금 성장 10년) · 2 가격수익률 vs 총수익률 · 5 SPYD vs SPY 배당 4배(댓글 76) · 7 '역사상 최저치' 배런스 칼럼 · 4 SOL S&P500 분배금 — S&P500 배당률 33년 중 지금 위치·더 낮았던 때(2000년)·배당 줄어든 해를 센 글 0편
