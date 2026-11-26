# sq1pair1128 자료조사 (카페 11/28 10:10 칸 — 롱폼 SQ-1 짝 긴 글, firemap-write 11/27 07:1x 회차) — 지수·배당ETF, 통계형 form 4

## 검증
- 수요: toprank '나스닥100 SCHD' 블로그 상위 8편 중 8편이 3일 안(toprank.txt, 2026-11-27) · 배당투자모임 주간 인기 SCHD·나스닥 제목 23편(최고 조회 3,189, bench_raw/weekly_31050378.json) · SQ-1 analysis.md ① 수요
- 경쟁에서 터진 증거: 주간 인기 '국내상장 미국 etf 1배 지수만 하시는분' 댓글 35 · 'SCHD 매도, QLD 매수 조언' 댓글 14 — 섞을지·비율 고민 질문
- 우리 실측: 짝 영상 SQ-1(qXwnz1RbLRk, 11/28 11:30 예약) 끝 말 '비율별 전체 표는 파이어맵 카페에 올려 두었어요' — 이 글이 그 표(영상보다 먼저 10:10)
- 칸: 11/28 10:10(slot.txt 2026-11-28 10) · 같은 날 h6pair1128(부동산)·TBD-배당·k1split1128(코스피 지수)와 대상 겹침 없음 · 범위(지수·배당ETF) 안, 세금은 비교의 한 칸

# 원문
- S1 야후 파이낸스 QQQ·SCHD 월말 수정종가 2011-10~2026-10(분배 재투자) — SQ-1 calc_mix.py → ../longform/ep/SQ-1/calc_mix_out_1112.txt https://finance.yahoo.com/quote/QQQ/history · https://finance.yahoo.com/quote/SCHD/history (SQ-1 S1, 운용사 NAV와 대조 ±0.05%p)
- S2 한국은행 ECOS 원·달러 매매기준율(731Y001) 2011-10-31 1,104.5원 → 2026-10-30 1,335.3원 — ../longform/ep/SQ-1/calc_krw_out_1120.txt https://ecos.bok.or.kr/
- S3 세후 계산 ../longform/ep/SQ-1/calc_tax_out_1121b.txt — 해외 상장 양도 22%·250만원 공제 소득세법 제104조·제103조 https://www.law.go.kr/법령/소득세법/제104조 · 국내 상장 해외 ETF 이익 = 배당소득 시행령 제26조의2 https://www.law.go.kr/법령/소득세법시행령/제26조의2 · 금융소득 2천만원 종합과세 제14조 https://www.law.go.kr/법령/소득세법/제14조
- S4 원천징수에서 외국 세금 빼기 — 소득세법 제129조 https://www.law.go.kr/법령/소득세법/제129조 (SQ-1 review v1.7 ①)
- S5 새로 받음 2026-11-27 07:1x: 야후 chart API 일봉 QQQ·SCHD 2026-10-30 → 2026-11-25 종가(fetch.py → fetch_out.txt, raw/QQQ_1d.json·raw/SCHD_1d.json) https://query1.finance.yahoo.com/v8/finance/chart/QQQ · https://query1.finance.yahoo.com/v8/finance/chart/SCHD
- S6 짝 영상 SQ-1 대본 199행·cafe.md(재료) — ../longform/ep/SQ-1/cafe.md

# 질문
1. 같은 지수면 국내 상장 ETF로 해도 되나 — https://www.youtube.com/watch?v=z45kjKrdQEg&lc=Ugx77hGqdnUca64jmlt4AaABAg → 답: 일반 계좌에서 한 번에 팔면 15년은 직접 산 쪽, 5년은 국내 상장 쪽이 더 남음(c04)
2. 나스닥100만 살까, SCHD를 섞을까 — https://www.youtube.com/watch?v=MPooDiIP2N4 → 답: 비율 다섯 줄 15년 끝값·빠진 폭(c01), 5년은 차이 200만원(c02)
3. 국내상장 1배 지수(S&P500·나스닥100)만 하는 사람 — https://cafe.naver.com/ca-fe/cafes/31050378/articles/68730 (댓글 35) → 답: 국내 상장 세후는 판 해 몰아 팔면 종합과세(c04·c05)
4. SCHD 팔고 나스닥 레버리지로 옮길까 — https://cafe.naver.com/ca-fe/cafes/31050378/articles/68973 → 답: 레버리지는 계산 안 함, 1배 기준 SCHD만 vs 나스닥100만 빠진 폭 −21.5% vs −32.6%(c01) · 권유 안 함

# 왜
- 왜 나스닥100 몫이 클수록 끝값이 컸나: 15년 동안 QQQ 연평균 18.98% vs SCHD 13.60%(S1) — 왜 그렇게 올랐는지는 계산 자료에 없음 → 본문에 이유 안 씀
- 왜 SCHD 70%가 SCHD만보다 빠진 폭이 얕나: 두 상품이 같은 달 똑같이 빠지지 않음(S1 최대낙폭 −20.7% vs −21.5%)
- 왜 원화 빠진 폭이 얕나: 2020년 3월 주가 바닥 때 환율 상승(S2, calc_krw 고점 2020-01 → 바닥 2020-03)
- 왜 국내 상장이 15년에 덜 남나: 판 차익이 배당소득이라 판 해 2천만원 넘어 종합과세(S3)

# 그래서
- 궁금한 비율의 줄을 찾고 계좌가 일반 계좌인지 연금저축·ISA인지 먼저 확인(대본 끝과 같음)
- 국내 상장 세후 숫자는 한 해에 몰아 판 값 — 나눠 팔면 달라짐(S3 '한 해에 몰아 판 값' 줄)

# 누구라면
- 나스닥100만 가진 사람: 15년 끝값 가장 컸지만 빠진 폭 −32.6%(2022년)
- SCHD만 가진 사람: 끝값 6억 7,700만원, 빠진 폭 −21.5%
- 국내 상장 ETF로 일반 계좌에서 오래 둔 사람: 판 해 종합과세 — 15년 반반 기준 직접 산 쪽보다 약 2억 덜 남음(다른 소득 0)

# 함정
- 영상 계산은 10/30까지 — 11/25 종가로 QQQ −8.2%·SCHD −1.4%(S5), 반반 9억 6,200만원쯤(c05)
- 국내 상장 세후는 몰아 판 경우(c05)
- 세후 표는 비율 맞춤 없는 계산이라 세전 끝값이 앞 표와 다름(c04 단순화 둘째 줄)

# 한계
- 국내 상장 ETF 실제 가격 대신 QQQ·SCHD로 움직였다고 가정(TIGER 미국배당다우존스는 2023 상장 — 15·10년은 가상)
- 건강보험료 영향 숫자 없음, 연금저축·ISA 계산 안 함
- 70%·30% 줄은 원화·세후 계산 안 함
- 12/1 상장 예정 4:4:2 섞는 ETF(블로그 2차 출처)는 운용사 1차 공지를 못 찾아 안 씀
- 지난 값은 앞날을 말해 주지 않음

# 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 15년 SCHD만 6억 7,700만원·70% 8억 7,200만원·반반 10억 1천만원·30% 11억 5천만원·나스닥100만 13억 5,600만원 | 100% 6.77억 · 70% 8.72억 · 50% 10.10억 · 30% 11.50억 · 0% 13.56억 | S1 https://finance.yahoo.com/quote/QQQ/history · calc_mix_out_1112.txt |
| 빠진 폭 −21.5%·−20.7%·−24.0%·−27.4%·−32.6% | 최대낙폭 같은 값 | S1 https://finance.yahoo.com/quote/SCHD/history · calc_mix_out_1112.txt |
| 네 줄이 2022년, SCHD만 2018년(−5.6%) | 최악연도 2018 −5.6% · 나머지 2022 | S1 https://finance.yahoo.com/quote/SCHD/history |
| 10년 SCHD만 3억 6,100만원·반반 5억 200만원·나스닥100만 6억 3,200만원 | 3.61억 · 5.02억 · 6.32억 | S1 https://finance.yahoo.com/quote/QQQ/history |
| 5년 1억 6,600만원·1억 8,200만원·1억 8,400만원, 차이 200만원, 빠진 폭 −24.0%·−32.6% | 1.66억 · 1.82억 · 1.84억 · −24.0% · −32.6% | S1 https://finance.yahoo.com/quote/QQQ/history |
| 환율 1,104.5원 → 1,335.3원 | 20111031 1,104.5 → 20261030 1,335.3 | S2 https://ecos.bok.or.kr/ |
| 원화 8억 1,800만원(+1억 4,100만원)·12억 2,100만원(+2억 1,100만원)·16억 3,900만원(+2억 8,300만원) | 8.18억 +1.41 · 12.21억 +2.11 · 16.39억 +2.83 | S2 https://ecos.bok.or.kr/ · calc_krw_out_1120.txt |
| 원화 빠진 폭 −17.5%·−13.6%·−27.9%, 2020년 3월 | 같은 값 · 바닥 2020-03 | S2 https://ecos.bok.or.kr/ |
| 세후 직접 6억 4,700만원/국내 5억 6,100만원 · 9억 6,700만원/7억 6,900만원 · 12억 8,700만원/9억 6,200만원 | 6.47/5.61 · 9.67/7.69 · 12.87/9.62(다른 소득 0) | S3 https://www.law.go.kr/법령/소득세법/제104조 · calc_tax_out_1121b.txt |
| 5년 국내 상장이 329만~405만원 더 | 차이 −366 · −405 · −329만원 | S3 https://www.law.go.kr/법령/소득세법/제14조 |
| 판 차익 250만원 뺀 나머지에 22% · 국내 상장 차익은 배당소득 | 제104조·제103조 · 시행령 제26조의2 | S3 https://www.law.go.kr/법령/소득세법시행령/제26조의2 |
| 국내 상장 분배금은 미국 세금만큼 빼고 원천징수 | 제129조 | S4 https://www.law.go.kr/법령/소득세법/제129조 |
| 11/25 종가 QQQ −8.2%·SCHD −1.4%, 반반 9억 6,200만원쯤·나스닥100만 12억 4,500만원쯤 | 690.49→633.93 수정 −8.19% · 35.78→35.29 −1.37% · 9.62억 · 12.45억 | S5 https://query1.finance.yahoo.com/v8/finance/chart/QQQ · fetch_out.txt |

# 올리기 전 확인
- 2026-11-27 07:2x firemap-write(작성 날 = 발행 전날, 11/28 10:10 발행 회차가 fetch.py 다시 돌려 최근 종가로 c05·c06 기준일 갱신)
- 다시 연 주소: https://finance.yahoo.com/quote/QQQ/history · https://finance.yahoo.com/quote/SCHD/history · https://ecos.bok.or.kr/ · https://www.law.go.kr/법령/소득세법/제104조 · https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/소득세법시행령/제26조의2 · https://www.law.go.kr/법령/소득세법/제129조 · https://query1.finance.yahoo.com/v8/finance/chart/QQQ · https://query1.finance.yahoo.com/v8/finance/chart/SCHD
- 기준일: 15년·10년·5년 표 2026-10-30 미국 종가 · 환율 2026-10-30 매매기준율 · 세법 2026-11 현행 · 한 달 변화 2026-11-25 미국 종가(11/26 휴장)
- 바뀐 것: 영상(10/30 종가) 뒤 11/25 종가 QQQ −8.19%·SCHD −1.37% → 반반 10.10억→9.62억쯤·나스닥100만 13.56억→12.45억쯤(c05에 적음), 그 사이 분배 없음
- 새로 찾은 것: 11/25 종가 한 달 변화(S5) · 배당투자모임 주간 인기 섞기·국내 상장 질문(댓글 35) · 12/1 상장 예정 4:4:2 ETF 소식(블로그만, 1차 못 찾음 → 안 씀)
- 조사 뒤 공표: 없음
