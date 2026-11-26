# decdiv1126 자료조사 (카페 11/26 10:10 배당 칸, firemap-write-b 11/24 19:40 회차) — 미국 배당 ETF 12월 배당락일·지급일(일정형 form 3)

## 검증
- 범위: 사장님 11/19 '배당·지수·부동산' 중 ① 배당 ETF 배당 일정(개별주·세금정책 아님, 미국 원천징수 15%는 계산 한 줄)
- 수요: work/kwvol.py 11/24 19:5x — SCHD배당금 5,290 · 배당주 4,980 · 미국배당다우존스 4,200 · JEPI 7,920 · 커버드콜ETF 9,470 · VYM 440 · HDV 290. SCHD·JEPI 단독 글은 최근 여러 번 써서(schdpair1105·tigerdj1122·jepipair1103 등) 7개 날짜를 한 글로 묶음
- 경쟁에서 터진 증거: toprank '미국 배당 ETF 12월 배당락일' 상위 8편 중 7편이 3주 안 글, 'SCHD 12월 배당' 1·2위가 11/24 글 — 지금 찾는 주제
- 포화: 높음(같은 날짜 글 다수) — 그래서 우리만: 운용사 원문 4곳 직접 확인(경쟁 1위는 VOO를 '예정'·제3자 인용), 2025년 12월 배당이 1년의 몇 %였는지·1만 달러 세후 계산(경쟁 0편, 1위는 '총액은 뺐다')
- 겹침: 11/26 07:40 k200etf1126(지수·수익 비교형), 12:40 rent100(부동산) — 꼴·축 다름. 11/25 18:40 dgro1125가 DGRO 12/15 한 줄을 썼고 이 글은 7개 달력
- 제목 쉼표 없음(11/26 칸 쉼표 제목 3개라 절반 넘지 않게)

## 원문
- S1 슈왑 2026 주식 ETF 분배 일정표(7/28자 갱신, 2026-11-24 받음, raw/schwab_equity_sched2026.pdf·schwab_p1.png) — SCHD Q4 12/9 배당락·12/14 지급, 12/30 추가(필요 시)·1/5/27 지급, 각주 '배당락일 전에 매매': https://bynder.schwab.com/m/15dbdbecf7339e7f/ (목록 https://www.schwabassetmanagement.com/resource/schwab-equity-etfs-distribution-schedule-2026)
- S2 뱅가드 2026 배당 일정표(2026-11-24 받음, raw/vg_divdat012026.pdf) — VIG·VOO 12/21·12/23, VYM 12/18·12/22, 12/30 줄(1/4/27): https://investor.vanguard.com/content/dam/retail/us/en/pdfs/taxes/divdat-012026.pdf
- S3 아이셰어즈 2026-2028 분배 일정표(11/18자, 2026-11-24 받음, raw/ish_sched.pdf) — DGRO 묶음 12/14 발표·12/15 배당락·12/18 지급, 12/30 소비세용 추가·1/5/27, 날짜 정의: https://www.ishares.com/us/literature/shareholder-letters/isharesandblackrocketfsdistributionschedule.pdf
- S4 JP모건 ETF 2026 배당 달력(2026-11-24 받음, raw/jpm_notice2026.pdf) — JEPI·JEPQ 12/1 배당락·12/3 지급, 자본이득(있으면) 12/15·12/17: https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/supplemental/income-distribution-rates/jpmorgan-etfs-2026-distribution-notice.pdf
- S5 뉴욕증권거래소 휴장일·거래시간(2026-11-24 받음, raw/nyse_hours.html) — 11/26 휴장·11/27 13:00 조기 마감·12/25 휴장·정규장 9:30~16:00 ET: https://www.nyse.com/markets/hours-calendars
- S6 야후 파이낸스 chart API 7개 ETF 3년 일별 종가·배당(2026-11-24 받음, raw/yahoo_*.json): https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=3y&interval=1d&events=div
- S7 S6으로 직접 계산(calc.py → calc_out.txt)

## 경쟁
- toprank.txt('미국 배당 ETF 12월 배당락일'·'SCHD 12월 배당' 블로그 상위 8씩, 11/24) — 1 few_economy 12월 배당 달력 7개(JEPQ·SCHD·VOO·QQQ·국내 3), 2 green8578 12월 배당락 총정리(SCHD·삼성전자·엔비디아), 5 horang1200 국내·미국 마감일, 6 dividendvending 국내 12/29 배당락, SCHD 1 loyal90 12/9 전 세후, 2 nineman903 12/9·연금계좌 세금
- 말한 것: 배당락일·지급일, 배당락일 전 거래일까지, 한국 시간 새벽 6시, 국내 배당락, 15.4%·15% 세금
- 빠뜨린 것: VOO 날짜를 운용사 원문으로 확인한 글(1위는 '예정'), 12월 배당이 1년의 몇 %인지(0편), JEPI·JEPQ 2025년 12월 배당락 두 번(0편), 1만 달러 기준 12월 세후 금액(0편, 1위 '총액은 뺐다')

## 질문
1. 12월 배당 받으려면 언제까지 사야 하나 — https://blog.naver.com/dividendvending/224482199237 (제목 '배당은 며칠까지 사야 받을까?') → 답: 배당락일 전 거래일 미국 장 마감, 한국 시간 배당락일 새벽 6시
2. SCHD 12월 배당락일은 9일인가 10일인가 — https://kr.benzinga.com/quote/SCHD/dividends (12/10로 적음) · https://blog.naver.com/nineman903/224478717119 (12/9) → 답: 슈왑 원문 12/9, 작년이 12/10
3. 12월 배당은 얼마나 나오나 — https://blog.naver.com/loyal90/224474741222 ('SCHD 12월 배당 세후 계산법', 댓글 4) → 답: 올해 금액 미발표, 작년 12월은 1년의 25% 안팎(DGRO 30.8%), 1만 달러면 세후 약 23~178달러
4. 12월 배당인데 왜 1월에 들어오나 — https://blog.naver.com/few_economy/224477589614 ('12월 배당인데 1월에 들어오는 ETF') → 답: 12/30 추가 분배(필요할 때만)는 지급이 1월 초

## 왜
- 왜 배당락일 전날까지: S1 각주 '배당락일 전에 매매해야 기준일 주주', S2~S4 모두 배당락일=기준일
- 왜 새벽 6시: S5 정규장 16:00 ET, 11/1 서머타임 끝(동부 표준시 +14시간) → 한국 06:00
- 왜 SCHD가 작년보다 하루 빠른지: 원문에 이유 없음 — 글에 이유 안 씀(날짜만)
- 왜 DGRO 12월이 컸나: 원문에 이유 없음 — 크기만 씀
- 왜 12/30 줄: S2 '추정 소득과 실제 차이를 맞추려 필요하면 늦은 12월 추가 분배', S3 'Potential Income Distribution for Excise Purposes'

## 그래서
- 받고 싶은 ETF별로 '한국 시간 배당락일 새벽 6시' 전에 매수 체결 — VIG·VOO는 12/19(토) 새벽 6시
- 올해 금액은 발표 뒤 확인(아이셰어즈는 배당락 전 영업일 장 마감 뒤 발표)
- 계좌 입금은 지급일보다 늦을 수 있음(S3 지급일 정의)

## 누구라면
- 매달 생활비를 받는 사람(JEPI·JEPQ): 12월 1일이 먼저, 2025년엔 12/31에 한 번 더(1월분) — 12월 몫이 1년의 17~18%
- 분기 배당 ETF를 모으는 사람(SCHD·DGRO·VYM·VIG·VOO): 12/9~12/21에 흩어짐, 작년 12월 몫 25% 안팎(DGRO 30.8%)
- 배당만 받고 팔 생각인 사람: 이 글은 날짜만 — 배당락일 주가 변화는 exdiv1114 글이 다룸(여기선 안 씀)

## 함정
- SCHD 작년 날짜(12/10)를 그대로 옮긴 글을 보고 12/9에 사면 못 받음
- 미국 날짜와 한국 날짜 혼동 — 배당락일 '전날'은 한국 시간으로는 배당락일 새벽
- VIG·VOO는 배당락이 월요일이라 금요일 미국 장(한국 토요일 새벽)이 마지막
- 지급일=내 계좌 입금일로 생각

## 한계
- 올해 12월 1주당 금액은 미발표 — 작년 금액으로만 셈
- 1만 달러 계산은 11/25 종가·2025년 12월 금액·미국 원천징수 15%만 — 환율·국내 세금·수수료 안 넣음
- 국내 증권사 주간·프리마켓 체결이 어느 미국 거래일로 잡히는지는 증권사마다 달라 확인 안 함 — 글은 정규장 기준
- 12/30 추가 분배는 '필요할 때만'이라 나올지 모름
- 일정은 운용사가 바꿀 수 있음(S1·S4 각주)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| JEPI·JEPQ 12월 1일 배당락·3일 지급 | 12/1/2026 · 12/3/2026 | S4 |
| JP모건 12월 15일 자본이득(있으면) | 12/15/2026 · 12/17/2026 Capital Gains (If any) | S4 |
| SCHD 12월 9일 배당락·14일 지급 | 12/9/26 · 12/14/26 | S1 |
| SCHD 작년 12월 10일 배당락 | 2025-12-10 0.278 | S6 |
| DGRO 12월 15일 배당락·18일 지급, 발표는 배당락 전 영업일 | 15-Dec-26 · 18-Dec-26 · declared aftermarket on the business day prior | S3 |
| VYM 12월 18일·22일 | 12/18/26 · 12/22/26 | S2 |
| VIG·VOO 12월 21일·23일 | 12/21/26 · 12/23/26 | S2 |
| 12월 30일 추가 배당, 지급 1월 초 | 슈왑 12/30/26·1/5/27 · 뱅가드 12/30/26·01/04/27 · 아이셰어즈 30-Dec-26·5-Jan-27 | S1 S2 S3 |
| 지급일은 운용사가 증권사에 돈을 보내는 날 | the fund pays broker-dealers | S3 |
| 정규장 오후 4시 끝, 11/26·12/25 휴장, 11/27 오후 1시 | 9:30~4:00 ET · Nov 26 · Dec 25 · 1:00 p.m. Nov 27 | S5 |
| 12월 몫 DGRO 30.8%·VYM 27.0%·SCHD 26.6%·VOO 25.1%·VIG 24.8%, JEPI·JEPQ 17~18% | 30.8 · 27.0 · 26.6 · 25.1 · 24.8 · 16.9 · 18.4 | S6 S7 |
| DGRO 2025년 12월 0.447달러, 네 번 중 최대 | 0.447 (1년 1.451) | S6 S7 |
| JEPI·JEPQ 2025년 12월 배당락 1일·31일 | 2025-12-01 · 2025-12-31 | S6 |
| 1만 달러 세후 JEPQ 182·JEPI 121·SCHD 67·VYM 51·DGRO 48·VIG 31·VOO 23달러 | 182.0 · 121.0 · 67.0 · 50.8 · 47.7 · 30.9 · 22.8(11/25 종가) | S6 S7 |

# 올리기 전 확인
- 2026-11-26 11:08 firemap-write-b(발행 날 — 10:10 칸, 늦게 냄). 11/24 첫 기록은 아래 '이전'에 남김
- 다시 연 주소(11/26 전부 다시 받음): https://bynder.schwab.com/m/15dbdbecf7339e7f/ (슈왑 2026 주식 ETF 일정표 PDF — 11/24 받은 파일과 바이트까지 같음) · https://investor.vanguard.com/content/dam/retail/us/en/pdfs/taxes/divdat-012026.pdf (같음) · https://www.ishares.com/us/literature/shareholder-letters/isharesandblackrocketfsdistributionschedule.pdf (같음) · https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/supplemental/income-distribution-rates/jpmorgan-etfs-2026-distribution-notice.pdf (같음) · https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=3y&interval=1d&events=div (7종 다시 받음, 11/25 정규장 종가) · https://api.nasdaq.com/api/quote/JEPQ/dividends (12월 분배 발표 아직 없음 — 마지막 11/02 0.53922)
- 기준일: 운용사 일정표 2026-11-26 확인, 종가 2026-11-25 미국 종가(11/26 추수감사절 휴장), 배당 금액 2025년 기록
- 바뀐 것: 12월 배당락·지급 날짜 그대로(JEPI·JEPQ 12/1·SCHD 12/9·DGRO 12/15·VYM 12/18·VIG·VOO 12/21) · 종가 11/23→11/25(SCHD 34.39→35.29·JEPQ 54.03→52.72달러) · 1만 달러 세후 작년 12월 분배 SCHD 69→67달러·JEPQ 178→182달러, 나머지(JEPI 121·VYM 51·DGRO 48·VIG 31·VOO 23) 그대로 · 12월 몫 %(DGRO 30.8 등) 그대로
- 새로 찾은 것: JEPI·JEPQ 12월 분배금은 11/26 기준 아직 발표 전(나스닥 기록 11월분까지) — 글의 '올해 금액은 아직 안 정해졌어요'가 그대로 맞음 · 11/30(월) 미국 장이 JEPI·JEPQ 마지막 날이라 발행일(11/26) 기준 아직 살 수 있는 날짜
- 조사 뒤 공표: 운용사 12월 금액은 배당락 전 영업일 발표(아이셰어즈 일정표) — 발행 뒤 나옴

## 이전(11/24)
- 2026-11-24 20:1x 작성하며 S1~S6 모두 받음: https://www.schwabassetmanagement.com/resource/schwab-equity-etfs-distribution-schedule-2026 https://bynder.schwab.com/m/15dbdbecf7339e7f/ https://investor.vanguard.com/content/dam/retail/us/en/pdfs/taxes/divdat-012026.pdf https://www.ishares.com/us/literature/shareholder-letters/isharesandblackrocketfsdistributionschedule.pdf https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/supplemental/income-distribution-rates/jpmorgan-etfs-2026-distribution-notice.pdf https://www.nyse.com/markets/hours-calendars https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=3y&interval=1d&events=div
- 발행 회차(11/26)가 다시 열어 날짜·종가 확인하고 적을 것
기준일: 운용사 일정표 2026-11-24 확인, 종가 2026-11-23 미국 종가, 배당 금액 2025년 기록
바뀐 것: 없음(작성일)
새로 찾은 것: 슈왑 일정표 SCHD 12/9(작년 12/10과 다름), 뱅가드 원문에 VOO 12/21 확정 날짜
