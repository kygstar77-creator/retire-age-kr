# vig1125 자료조사 (카페 11/25 12:40 배당 칸, firemap-write 11/23 18:1x 회차) — VIG 배당성장 10년, VYM과 직접 계산

## 검증
- 수요: kwvol 11/23 — SCHD배당금 5,280 · 고배당ETF 3,790 · 월배당ETF 2,860 · VIG 1,510 · SCHD배당일 440 · VYM 430 · 배당성장ETF 300. SCHD(11/24 07:40 tigerdj1122)·고배당ETF(11/24 22:40 kofinpair1124)·월배당(11/23 qqqi1123)은 하루 안 같은 대상이라 VIG로
- 경쟁에서 터진 증거: toprank 'VIG 배당' 상위 8편 중 7편이 2주 안 글(11/23) — 'VIG 매수 공시' 보도·'SCHD가 VIG 제쳤다' 보도로 관심이 몰림
- 겹침: 최근 2주 카페에 VIG 단독 글 없음
- 칸: 11/25 12:40 배당(slots.json TBD-배당, 관문 기한 11/25 06:40)

## 원문
- S1 야후 파이낸스 chart API VIG·VYM·SPY 일별 종가·배당 events, 11/23 18:2x 받음(raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/VIG
- S2 뱅가드 상품 정보 API VIG·VYM(설정일·총보수·분기 배당·최근 6번 배당): https://investor.vanguard.com/vmf/api/VIG/profile · https://investor.vanguard.com/vmf/api/VIG/distribution · https://investor.vanguard.com/vmf/api/VYM/profile
- S3 S&P DJI 'S&P Dividend Growers Index Series' 방법론(2024-04판): https://spglobal.com/spdji/zh/documents/methodologies/methodology-sp-dividend-growers-index-series.pdf
- S4 뱅가드 VIG 팩트시트(2026-06-30): https://workplace.vanguard.com/iippdf/pdfs/FS920R.pdf
- S5 S1으로 직접 계산(calc.py → calc_out.txt), 2026년 배당 합은 S2와 대조(VIG 2.762 vs 2.7617, VYM 2.729 vs 2.7281)

## 경쟁
- toprank.txt('VIG 배당' 블로그 상위 8, 11/23) — 1위 campcodemoney는 VIG 기본 정보·고금리 전망, 2위 royal23-은 VIG·DGRO 배당률 표, 3위는 기본 정보 표 9,191자, 5위는 SCHD 운용자산 역전 보도. 10년 실제 배당 기록으로 산 값 대비 배당을 센 글은 상위 8편에 없음
- 모닝스타 VYM vs VIG: https://www.morningstar.com/funds/vym-vs-vig-which-vanguard-dividend-etf-should-you-buy — 전략 차이 설명, 산 값 대비 배당 계산 없음

## 질문
1. VIG 배당률이 낮은데 왜 사나 — https://blog.naver.com/campcodemoney/224479441442 ('고금리에도 배당성장주에 투자할 이유가 있을까?') → 답: 1주당 배당 10년 약 2배(연 7%쯤)
2. VIG와 다른 배당 ETF 중 뭘 고르나 — https://blog.naver.com/royal23-/224475583184 ('장기투자 선택기준은?') → 답: 지금 배당은 VYM, 10년 총수익은 VIG가 앞섬
3. 배당성장 ETF가 오래 들면 고배당을 앞서나 — https://www.morningstar.com/funds/vym-vs-vig-which-vanguard-dividend-etf-should-you-buy ('VYM vs. VIG: Which … Should You Buy?') → 답: 10년 전 산 값 대비 지금 배당 VIG 4.6% vs VYM 5.4%, 아직 못 앞섬
4. 배당률만 높으면 좋은가 — https://blog.naver.com/gogofree2030/224468892712 ('배당률 높다고 무조건 좋은 걸까?') → 답: 지수가 배당률 상위 25%를 일부러 뺌(S3)

## 왜
- 왜 VIG 배당률이 낮나: 지수가 배당률 상위 25%를 빼고 10년 연속 배당을 늘린 회사만 담음(S3) — 수익률 함정 회피가 이유로 적혀 있음
- 왜 VIG 주가가 더 올랐나: 원문(S1~S4)에 이유 없음 — 기술 업종 26%(S4)는 사실로만, 원인으로 안 씀

## 그래서
- 생활비로 지금 배당이 필요하면 산 값 대비 배당도 10년간 VYM이 높았다는 점을 본다
- 10년 뒤 총액이 목표면 VIG 총수익이 더 높았다(같은 기간 SPY는 둘 다보다 높음)

## 누구라면
- 은퇴 뒤 매달 배당으로 생활비 쓰는 사람: 지금 배당률 VYM 2.3% vs VIG 1.5%, 10년 뒤에도 VYM 산 값 대비 배당이 높았음
- 10년 넘게 모을 사람: 배당 재투자 총수익 VIG 278% vs VYM 222%
- 하락이 무서운 사람: 2021년 이후 최대 낙폭 VIG 20.4% vs VYM 15.8%

## 함정
- '배당성장 ETF는 오래 들면 고배당을 앞선다'는 말 — VIG와 VYM 사이에선 10년으로 아직 안 맞음
- 기간 하나로 단정 — 최근 1년은 VYM이 총수익도 앞섬

## 한계
- 달러 기준·세전 — 환율·미국 배당 원천징수·국내 세금은 안 넣음
- 2015-11-20 시작 한 기간 — 다른 시작일이면 숫자가 다름
- 야후 배당 기록 전체를 뱅가드 원문과 맞춘 것은 최근 6번(2025-12~2026-09)뿐
- 트럼프 VIG 거래 보도는 매수·매도가 엇갈리고 정부윤리청 원문 안 열어 안 씀
- 운용자산 순위(SCHD vs VIG)는 9~10월 보도만 있어 안 씀

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 지금 배당률 VIG 1.5%·VYM 2.3% | 1.51% · 2.34%(최근 1년 배당 ÷ 11/24 종가) | S1·S5 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 2015년 11월 20일 매수 · 11/24 종가 | 78.94 · 68.16 / 242.11 · 157.32 | S1 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 1주당 연 배당 1.82→3.56 · 2.15→3.50, 약 2배·1.6배, 해마다 7%·5%쯤 | 1.819→3.558(1.96배, 6.9%) · 2.149→3.501(1.63배, 5.0%) | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 산 값 대비 지금 배당 VIG 4.6%·VYM 5.4% | 4.62 · 5.39 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 2015년 배당률 VIG 2.3%·VYM 3.2%쯤 | 2.30 · 3.15 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 1만 달러 → 배당 약 3,700·4,900, 평가액 약 3만 700·2만 3,100달러 | 3,703 · 4,865 · 30,670 · 23,081 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 11년 총수익 VIG 278%·VYM 222%·SPY 311% | 278.3 · 222.3 · 310.8 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 1년 총수익 VYM 16.4%·VIG 15.5% | 16.4 · 15.5 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 최대 낙폭 VIG 20.4%·VYM 15.8%(2021년 이후) | -20.4 · -15.8 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 2020년 1주당 배당 줄지 않음 | VIG 2.134→2.297 · VYM 2.842→2.906 | S1 https://query1.finance.yahoo.com/v8/finance/chart/VIG |
| 2006년 출시 · 총보수 0.04%(둘 다) | 2006-04-21 · 0.0400 / VYM 0.0400 | S2 https://investor.vanguard.com/vmf/api/VIG/profile |
| 3·6·9·12월 배당, 9월 0.93달러 | Quarterly · 0.9295(9/28) | S2 https://investor.vanguard.com/vmf/api/VIG/distribution |
| 10년 넘게 배당 늘린 회사, 배당률 상위 4분의 1 제외 | 10 consecutive years · top 25% excluded | S3 https://spglobal.com/spdji/zh/documents/methodologies/methodology-sp-dividend-growers-index-series.pdf |
| 기술 업종 26%쯤, 6월 말 | IT 약 26%(2026-06-30) | S4 https://workplace.vanguard.com/iippdf/pdfs/FS920R.pdf |

# 올리기 전 확인
- 2026-11-25 12:3x firemap-write(발행 날 12:10 회차) — 야후 VIG·VYM·DGRO·SCHD·SPY 다시 받아 calc.py·mkimg.py 다시 돌림(calc_out.prev1125 ↔ calc_out.txt)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/VIG (11/25) · https://query1.finance.yahoo.com/v8/finance/chart/VYM (11/25) · https://query1.finance.yahoo.com/v8/finance/chart/SPY (11/25) · https://investor.vanguard.com/vmf/api/VIG/profile (11/23, 총보수·이름 — 바뀔 일 없는 값) · https://investor.vanguard.com/vmf/api/VIG/distribution (11/23, 야후 배당 기록 11/25 변화 없음으로 대조) · https://investor.vanguard.com/vmf/api/VYM/profile (11/23) · https://spglobal.com/spdji/zh/documents/methodologies/methodology-sp-dividend-growers-index-series.pdf (11/23) · https://workplace.vanguard.com/iippdf/pdfs/FS920R.pdf (11/23) · https://blog.naver.com/gogofree2030/224468892712 (11/25 다시 엶, 질문 출처 그대로 살아 있음)
- 기준일: 2026-11-24 미국 종가
- 바뀐 것: 기준일 11/20→11/24 · VIG 235.69→242.11·VYM 153.87→157.32달러 · VYM 배당률 2.4→2.3% · 1만 달러 평가액 VIG 2만 9,900→3만 700·VYM 2만 2,600→2만 3,100 · 배당 다시 산 값 VIG 3.7→3.8배·SPY 3.9→4.1배(VYM 3.2배 그대로) · 1년 총수익 VYM 13.9→16.4%·VIG 12.4→15.5%(VYM 앞섬 그대로) · 결론(산 값 대비 배당 VYM 앞섬, 총수익 VIG 앞섬, SPY 최고) 그대로 · 배당 기록 새로 나온 것 없음
- 새로 찾은 것: 11/24 종가로 다시 셈 — SPY가 11/20~24 +4.2% 올라 SPY와 VIG 차이 3.7배 대 3.9배 → 3.8배 대 4.1배로 벌어짐
- 조사 뒤 공표: data/release_calendar.json — 가격 매일, VIG·VYM 12월 배당(12월 하순) 전 발행
