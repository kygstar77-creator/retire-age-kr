# hidiv1128 자료조사 (카페 11/28 12:40 배당 칸) — 미국 고배당 ETF VYM·HDV·SPYD 10년, 배당률 순서와 끝값 순서가 거꾸로 (통계·계산형 form 4)

## 상태 (11/27 13:4x write-b)
- 07:1x write 회차: 주제 검증(수요·겹침)·원자료 받기(fetch.py)·직접 계산(calc.py → calc_out.txt)
- 13:4x write-b 회차: 운용사 원문 3곳(S2~S4)·HDV 분배 기록 대조(분할 조정값 확인)·미국 원천 15%(S5)·경쟁 5편 본문·표지(bench_raw)·질문 3개 주소·조각·그림·검사·이해 시험·editgate
- 발행 회차(11/28 12:1x write): fetch.py·calc.py 다시(11/27 종가) → 숫자 바뀌면 c0*·mkimg.py·facts·대조 고치고 재서명, '올리기 전 확인' 날짜 갱신

## 검증
- 수요: kwvol 11/27 07:1x — 고배당ETF 3,830 · 미국배당ETF 2,780 · 미국고배당ETF 780 · SPYD 470 · VYM 460 · HDV 300 (커버드콜ETF 8,950은 11/27 jepivix·11/23 qqqi와 겹쳐 뺌, 리얼티인컴 7,870은 개별주라 뺌)
- 우리 실측: textrule 11/26 축 '종목' 1.25 > 배당현금흐름 0.79, 형식 4 우세 · 잘된 글 2위 '나스닥100 ETF 네 곳 수익 비교, 같은 날 샀다면' 14.4/일 — divdj1127(11/27 18:40)이 '같은 날 1억' 제목 꼴이라 제목은 배당률↔결과 물음 꼴로
- 겹침: 같은 날 10:10 sq1pair1128(나스닥100+SCHD)·22:40 k1split1128(코스피) — 상품·축 다름 · 11/26·27 decdiv·schdhold·jepivix·divdj(SCHD 지수 국내 4종) — 상품 다름 · 옛 글 #59 vymdgro·#68 hdvdiv·#73 spydcal(9월, 각 상품 배당금 한 가지, 30일 넘음) — 세 곳 10년 맞대기 아님

## 원문
- S1 야후 파이낸스 chart API 일별 종가·배당 events VYM·HDV·SPYD, ~2026-11-25 종가(11/26 미국 휴장), 11/27 07:1x 받음(raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/SPYD
- S2 뱅가드 VYM 공식 — 총보수(expenseRatio) 0.0400%(2026-02-27 기준)·설정 2006-11-10(vmf/api/VYM/profile), 배당 주기 Quarterly·최근 2026-09-18 기준 0.8869달러(vmf/api/VYM/distribution), 지수 FTSE High Dividend Yield Index(상품 페이지), 11/27 13:4x 받음(raw/vym_profile_1127.json·vym_dist_1127.json·vym_page_1127.html): https://investor.vanguard.com/vmf/api/VYM/profile · https://investor.vanguard.com/vmf/api/VYM/distribution · https://investor.vanguard.com/investment-products/etfs/profile/vym
- S3 블랙록 iShares HDV 공식 — Expense Ratio 0.08% · Distribution Frequency Monthly · Benchmark Morningstar Dividend Yield Focus Index · 보유 73종목(11/25) · 순자산 165.6억달러(11/25) · 설정 2011-03-29 · 분배 기록(배당락일) 2026-03-17 다음부터 06-15·07-15·08-19·09-16·10-21·11-18 매달, 최근 1년 합 1.023042달러(야후 1년 합 1.0232와 같음 — 야후 HDV 값은 iShares 분배표와 같은 기준), 11/27 13:4x 받음(raw/hdv_1127.html): https://www.ishares.com/us/products/239563/ishares-core-high-dividend-etf
- S4 스테이트스트리트 SSGA SPYD 공식 — Gross Expense Ratio 0.07% · Distribution Frequency Quarterly · Benchmark S&P 500 High Dividend Index('S&P 500 안 배당수익률 상위 80곳') · 보유 77종목 · 상장 2015-10-22(NYSE Arca), 11/27 13:4x 받음(raw/spyd_1127.html): https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-portfolio-sp-500-high-dividend-etf-spyd
- S5 미국 배당 제한세율 15% — 국세청 조세조약상 제한세율 규정표(2021.2) 미국 행, 11/27 13:4x 다시 엶(raw/nts_treaty_1127.html): https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 · 소득세법 제129조: https://www.law.go.kr/법령/소득세법/제129조

## 우리만 (calc_out.txt, 11/25 종가, 세전·배당 다시 삼, 달러 기준 비율 × 1억원)
- 10년(2016-11-25~2026-11-25) 1억이면: VYM 2억 8,766만 · HDV 2억 7,158만 · SPYD 2억 2,289만 — 1년 배당률은 거꾸로 SPYD 4.16% · HDV 3.36% · VYM 2.32%
- 배당을 현금으로 받았다면: 주식 VYM 2억 1,248만 · HDV 1억 8,849만 · SPYD 1억 4,060만, 받은 배당 VYM 4,162만 · HDV 4,510만 · SPYD 4,998만 — 합 VYM 2억 5,410만 > HDV 2억 3,359만 > SPYD 1억 9,058만
- 2020년 코로나 낙폭: SPYD −46.4% · HDV −37.0% · VYM −35.2%
- 해마다 1등(2016~2026, 2026은 11/25까지): VYM 6번(2017·2019·2020·2023·2024·2025) · HDV 3번(2018·2022·2026) · SPYD 2번(2016·2021)
- 최근 1년(2025-11-26~): HDV 1억 2,838만 · SPYD 1억 1,866만 · VYM 1억 1,237만 — 올해는 순서가 다름
- 배당금 2016→2025 늘어난 배: VYM 1.59 · HDV 1.45 · SPYD 1.29
- 세후(미국 원천 15%만 떼고 다시 삼) 10년: VYM 2억 7,492만 · HDV 2억 5,716만 · SPYD 2억 809만

## 질문
- Q1 배당수익률 높은 해외 배당 ETF가 결과도 좋은가(지식iN '고배당 etf관련 질문 드립니다!' — 해외 배당펀드 배당수익률이 더 높다는데): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=464932869 → 우리 답: 10년 끝값은 배당률 순서와 거꾸로(VYM 2억 8,766만 > HDV > SPYD 2억 2,289만)
- Q2 ETF 배당을 다시 넣는 것과 받아 쓰는 것 차이(지식iN '미국 주식 etf 복리 투자법??'): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=467380086 → 우리 답: 다시 산 값과 현금으로 받은 합을 둘 다 셈(SPYD는 받은 배당 4,998만으로 가장 많지만 주식은 1억 4,060만)
- Q3 미국 고배당 ETF 순위(네이버 자동완성 '미국 고배당 etf 순위'·'미국 고배당 ETF 순위 추천'): https://ac.search.naver.com/nx/ac?q=%EB%AF%B8%EA%B5%AD%20%EA%B3%A0%EB%B0%B0%EB%8B%B9%20etf&st=100&r_format=json → 우리 답: 해마다 1등이 바뀜(VYM 6·HDV 3·SPYD 2번), 최근 1년은 HDV 1등 — 순위는 기간에 따라 달라짐(추천 안 함)

## 왜
- 왜 배당률 높은 SPYD가 끝값은 가장 적나: 주가만 VYM 2.12배 · HDV 1.88배 · SPYD 1.41배(S1 calc) — 받은 배당은 SPYD가 가장 많았지만(4,998만) 주가가 덜 올라 합이 뒤짐. 주가가 덜 오른 이유는 운용사 원문에 없음 — 글엔 지수 고르는 법(S2~S4)만 적고 이유로 단정하지 않음
- 왜 2020년 SPYD 낙폭이 컸나: 원문에 이유 없음 — 숫자만
- 왜 HDV가 매달 주나: iShares 분배 기록상 2026년 6월부터 매달(S3) — 바꾼 이유는 이번에 본 페이지에 없음
- 왜 15%: 한미 조세조약 배당 제한세율 15%(S5), 국내 배당소득세 14%보다 높아 국내 추가 원천징수 없음(소득세법 제129조)

## 그래서
- 배당률 하나로 고르면 끝값 순서를 거꾸로 볼 수 있음 → 고를 때 볼 것: 같은 기간 배당 다시 산 값(총수익)·낙폭·배당 주기(월/분기)·총보수 — 숫자만 제시, 권유 없음
- 배당을 생활비로 꺼내 쓸 사람은 '받은 배당'과 '남은 주식'을 따로 봄

## 누구라면
- 배당을 다시 사는 사람: 10년 VYM 2억 8,766만 vs SPYD 2억 2,289만(세전), 세후 15% 떼도 순서 같음(2억 7,492만 vs 2억 809만)
- 배당을 생활비로 쓰는 사람: 10년 받은 배당 SPYD 4,998만 > HDV 4,510만 > VYM 4,162만, 남은 주식은 거꾸로 — 1억 1년 배당 SPYD 약 416만(한 달 약 35만)·VYM 약 232만(한 달 약 19만), 세전
- 매달 받고 싶은 사람: 셋 중 매달 주는 건 HDV뿐(2026년 6월부터), VYM·SPYD는 석 달마다

## 함정
- 배당률 높은 상품이 오래 들면 더 많이 남는다고 여기기 — 10년 끝값은 거꾸로
- 최근 1년만 보고 순위 매기기 — 최근 1년은 HDV 1등, 해마다 1등은 VYM이 6번
- 배당이 많이 늘어날 거라 여기기 — 9년 동안 배당금 늘어난 배는 SPYD가 가장 작음(1.29배)

## 한계
- 환율 뺌(달러 기준 비율에 1억원을 곱함) · 매매 수수료·국내 추가 세금·양도세 뺌
- 야후 HDV 종가·배당은 분할 조정값(splits 기록 없음) — iShares 공식 분배표 1년 합(1.023042)과 같아 비율 계산엔 영향 없음, 분할 날짜 원문은 확인 안 함 → 글에 분할 얘기 안 씀
- 시작일 바꾸면 순서 바뀜(최근 1년은 HDV 1등, 2015-10-22 시작도 VYM>HDV>SPYD — calc_out)
- 2026년은 11월 25일까지(한 해 다 안 참)
- 총보수는 운용사 공시 값, 실제 비용(매매·기타)은 확인 안 함

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 10년 1억 → VYM 2억 8,766만 · HDV 2억 7,158만 · SPYD 2억 2,289만 | 2.8766·2.7158·2.2289 | S1 calc_out.txt '세전 2016-11-25' |
| 1년 배당률 SPYD 4.16% · HDV 3.36% · VYM 2.32% | 2.06/49.55 · 1.0232/30.49 · 3.676/158.36 | S1 calc_out.txt · HDV 1년 합 S3 https://www.ishares.com/us/products/239563/ishares-core-high-dividend-etf |
| 현금으로 받기 주식 2억 1,248만·1억 8,849만·1억 4,060만 · 받은 배당 4,162만·4,510만·4,998만 | 2.1248·1.8849·1.4060 · 0.4162·0.4510·0.4998 | S1 calc_out.txt |
| 2020년 낙폭 SPYD −46.4% · HDV −37.0% · VYM −35.2% | -46.4·-37.0·-35.2 | S1 calc_out.txt |
| 해마다 1등 VYM 6번 · HDV 3번 · SPYD 2번 | 2016~2026 표 | S1 calc_out.txt '해마다' |
| 최근 1년 HDV 1억 2,838만 · SPYD 1억 1,866만 · VYM 1억 1,237만 | 1.2838·1.1866·1.1237 | S1 calc_out.txt '세전 2025-11-26' |
| 배당금 늘어난 배 VYM 1.59 · HDV 1.45 · SPYD 1.29 | 2016 합 → 2025 합 | S1 calc_out.txt |
| 세후 10년 VYM 2억 7,492만 · SPYD 2억 809만 | 2.7492·2.0809 | S1 calc_out.txt '세후 15%' · 15% S5 https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 |
| 총보수 VYM 0.04% · HDV 0.08% · SPYD 0.07% | 0.0400 · 0.08% · 0.07% | S2 https://investor.vanguard.com/vmf/api/VYM/profile · S3 · S4 https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-portfolio-sp-500-high-dividend-etf-spyd |
| 배당 주기 VYM·SPYD 석 달마다 · HDV 2026년 6월부터 매달 | Quarterly · Quarterly · Monthly, 배당락 06-15~11-18 | S2 https://investor.vanguard.com/vmf/api/VYM/distribution · S4 · S3 |
| 지수 VYM FTSE High Dividend Yield · HDV Morningstar Dividend Yield Focus(73종목) · SPYD S&P 500 안 배당 상위 80곳 | 원문 문구 | S2 https://investor.vanguard.com/investment-products/etfs/profile/vym · S3 · S4 |
| 1억 1년 배당 SPYD 약 416만·VYM 약 232만, 한 달 약 35만·19만 | 4.16%·2.32% × 1억 ÷ 12 | S1 calc_out.txt(직접 계산) |

# 올리기 전 확인
- 확인일: 2026-11-27 13:4x (write-b) — 발행 11/28 12:40, 1일 안. 발행 회차가 11/28에 다시 확인하면 이 칸을 고침
- 기준일: 2026-11-25 미국 정규장 종가(11/26 추수감사절 휴장)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/SPYD (VYM·HDV 같은 꼴, 07:1x 받은 raw) · https://investor.vanguard.com/vmf/api/VYM/profile · https://investor.vanguard.com/vmf/api/VYM/distribution · https://investor.vanguard.com/investment-products/etfs/profile/vym · https://www.ishares.com/us/products/239563/ishares-core-high-dividend-etf · https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-portfolio-sp-500-high-dividend-etf-spyd · https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2516&nttSn=1293238 · https://www.law.go.kr/법령/소득세법/제129조
- 바뀐 것: 07:1x 계산 뒤 새 종가 없음(11/26 휴장) — 숫자 그대로. HDV 배당이 2026년 6월부터 매달로 바뀐 것을 iShares 분배 기록에서 새로 확인(07:1x엔 몰랐음)
- 새로 찾은 것: VYM 총보수 0.04%(2026-02-27 기준)·HDV 0.08%·SPYD 0.07% · HDV 보유 73종목·SPYD 77종목 · iShares 1년 분배 합 1.023042달러 = 야후 1.0232
- 조사 뒤 공표: data/release_calendar.json 해당 없음(운용사 분배 공지는 12월 중순 — VYM·SPYD 12월 배당은 발행 뒤)

## 경쟁 (bench.md — toprank '미국 고배당 ETF 비교' 블로그 상위 8, 본문 5편)
- 1 VYM vs HDV 배당률·보수·수익률(6,526자) · 2 고배당 ETF 개념·운용사·주기 · 4 TOP10 '주가와 배당 합친 총수익' · 6 배당률 10% 함정 · 7 미국 배당 ETF 4종 · 2는 세 곳 10년 연환산 총수익·배당 증가율 표까지 있음 — 배당률 순서와 끝값 순서 대조·현금으로 받기·세후·해마다 1등·낙폭을 센 글 0편
