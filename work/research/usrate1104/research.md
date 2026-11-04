# usrate1104 자료조사 (카페 비축 — 11/4 16:10 경제·정책 칸 후보, 2026-11-03 21:37 firemap-write) — 경제 시황, 통계·기록형

## 검증
- 수요: demand.py 11/3 — 미국기준금리 월 31,600 · 원달러환율 422,300 · 한미금리차 280 · FOMC 10 → 검색어 '미국 기준금리' 맨 앞
- 경쟁: 네이버 통합검색 모바일 '한미 금리차'·'미국 기준금리 한국 기준금리 차이' 11/3 상위 블로그 6편 — 모두 금리차 1%p·12월 일정까지만, 역전이 며칠째인지·역대 몇 번째로 긴지 센 글 0편(bench_raw/posts.json kw '역대'·'최장'·'일째' 전부 false)
- 우리 실측: 지난 금리 글 bokrate1022(기준금리 동결, 10/22)·fomc10(9월 점도표)와 각도 안 겹침

## 원문
- S1 미 연준 FOMC 보도자료 2026-10-28 — 목표 범위 3-3/4~4% 유지, 10대 2, Cook·Hammack 0.25%p 인상 주장, "Inflation remains elevated." — 2026-11-03 확인(raw/fed_20261028.html): https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm
- S2 미 연준 FOMC 일정 — 2026년 12월 8~9일 — 2026-11-03 확인(raw/fed_cal.html): https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- S3 FRED DFEDTARU·DFEDTARL(2008-12-16~)·DFEDTAR(~2008-12-15) 일별 — 2026-11-02 상단 4·하단 3.75 — 2026-11-03 확인(raw/rates_1103.json): https://fred.stlouisfed.org/series/DFEDTARU
- S4 한국은행 ECOS 722Y001 기준금리 일별 1999-05-06~2026-11-01 — 3.00, 2026-07-16 2.5→2.75, 2026-08-27 2.75→3 — 2026-11-03 확인(raw/ecos_daily_1103.json): https://ecos.bok.or.kr/
- S5 한국은행 통화정책방향 2026-10-22 '기준금리 3.00% 유지'(KDI 경제교육·정보센터 게재) — 2026-11-03 확인(raw/kdi_bok_1022.html): https://eiec.kdi.re.kr/policy/materialView.do?num=288401
- S6 한국은행 ECOS 731Y001 원/미국달러 매매기준율 일별 2022-09-01~2026-11-03 — 2026-11-03 확인(raw/ecos_fx_1103.json): https://ecos.bok.or.kr/
- S7 (2차) 한국은행 11월 26일 금통위 — 블로그 2곳·정리 글 1곳: https://blog.naver.com/zappu/224463007537 · https://blog.naver.com/lsyivy0722/224458601600 · https://secretlinker.co.kr/?p=6521 (한국은행 원 일정표는 확인 안 함)

## 경쟁
bench.md — 블로그 6편. 모두 지금 금리·1%p·12월 일정·환율 영향 '가능성'을 다룸. 빠뜨린 것: 역전 기간을 센 글 0, 역전 첫날 대비 실제 환율 0.

## 질문
1. 한미 금리 역전이 오래 이어지면 환율 상승 등 어떤 문제가 생기나 — https://kin.naver.com/qna/detail.naver?dirId=409&docId=484042677 → 답: c00(얼마나 오래인지 1,503일)·c04(같은 기간 환율 실제 값)
2. 금리차가 커지면 원화 약세·외자 이탈 가능성이 높아진다던데 — https://kin.naver.com/qna/detail.naver?dirId=409&docId=484042860 → 답: c04(역전 첫날 1,393.6원 → 11/3 1,341원, 환율은 금리차 말고도 움직임)
3. 금리차가 줄면 환율이 내려가나 — https://kin.naver.com/qna/detail.naver?dirId=409&docId=484042747 → 답: c02·c04(2%p→1%p로 좁혀졌고 환율은 그 사이 1,554.4원까지 올랐다 내림)
4. 한미 금리가 주담대에 어떤 경로로 영향을 주나 — https://kin.naver.com/qna/detail.naver?dirId=409&docId=484548886 → 답: c05(대출·예금 금리는 한국은행 결정이 더 가깝다, 다음 11월 26일)

## 왜
- 연준이 동결한 이유: 결정문 "Inflation remains elevated."(S1) — 물가가 여전히 높음. 반대 2명은 인상 주장(S1).
- 한국은행 10월 동결 이유: 원문 본문을 못 받음(KDI 게재 페이지 본문이 스크립트로만 나옴) → 글에 이유를 쓰지 않음.
- 역전이 길어진 이유: 원문에 '역전 기간'에 대한 설명은 없음. 변경 이력(S3·S4)만 보면 2024~25년 미국이 내릴 때 한국도 내려 차이가 남았음 — 글에는 '미국이 내리고 한국이 올리면서 좁혀졌다'까지만 씀.

## 그래서
- 대출·예금 금리가 궁금하면 한국은행 11월 26일, 미국 주식·달러 예금이면 연준 12월 10일 새벽(한국 시간) 결정 — c05
- 금리차 하나로 환율 방향을 단정하지 않기 — c04

## 누구라면
- 변동금리 대출·원화 예금이 있는 사람 → 한국은행 결정(c05)
- 미국 주식·달러 예금을 가진 사람 → 연준 결정·환율(c05·c04)

## 함정
- 상단·하단 어느 쪽으로 비교하느냐에 따라 1%p/0.75%p로 숫자가 달라짐 — c01
- 역전 시작일을 2022-07-28로 세면 더 길어짐, 그 뒤 28일 같았던 기간이 있음 — c03

## 우리만
- 1999-05-06~2026-11-01 10,041일 날짜별 맞대기로 센 역전 구간 5개와 길이 — 지금 1,503일(11/3)이 역대 최장, 이전 최장 769일(calc_out.txt)
- 역전 첫날 대비 실제 환율(1,393.6 → 1,341원)

## 예외
- 미국 금리를 실효금리(EFFR)로 보거나 한국을 시장금리로 보면 숫자가 다름 — 이 글은 두 중앙은행이 정한 정책금리만
- 2008-12-15 이전 미국은 범위가 아닌 한 값(DFEDTAR) — 그 시기는 그 값으로 비교

## 한계
- 한국은행 11월 26일 회의 날짜는 11/3엔 2차(S7)만, 11/4 올리기 전 확인에서 한국은행 원 일정표로 확인함
- 한국은행 10/22 동결 이유 원문은 못 받음
- FRED·ECOS 두 자료 날짜가 겹치는 날만 셈. 결정 시각 차이로 하루 어긋나는 날이 있음(그래프의 가는 튐)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 기준금리 = 중앙은행이 정하는 금리, 예금·대출 금리의 바탕 | 한국은행 기준금리 설명 | S4 https://ecos.bok.or.kr/ |
| 미국 3.75~4% 동결(10/28) | maintain the target range ... at 3-3/4 to 4 percent | S1 https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm |
| 위원 12명 중 2명 인상 주장 | 10 – 2 vote · preferred to raise ... by 1/4 percentage point | S1 |
| "물가가 여전히 높다" | Inflation remains elevated. | S1 |
| 한국 3.00% 동결(10/22) | 기준금리 3.00% 유지 | S5 https://eiec.kdi.re.kr/policy/materialView.do?num=288401 · S4 |
| 올해 여름 두 번 인상 | 2026-07-16 2.5→2.75, 2026-08-27 2.75→3 | S4 https://ecos.bok.or.kr/ |
| 차이 1%p(위쪽) · 0.75%p(아래쪽) | 4−3 · 3.75−3 | S3 https://fred.stlouisfed.org/series/DFEDTARU · S4 |
| 2022-09-22 시작, 11/3까지 1,503일째·4년 1개월 | 날짜 계산 1503 | S3·S4 계산 |
| 앞선 세 번 약 1년 9개월·2년 1개월·1년 11개월 | 628·769·712일 | S3·S4 계산 |
| 가장 클 때 2%p, 2023년 7월 처음 | 최대차 2.0 · 2023-07-27 | S3·S4 계산 |
| 7월 말 처음 뒤집힘 · 8월 말부터 28일 같음 | 2022-07-28 시작 · 2022-08-25~09-21 28일 차이 0 | S3·S4 계산 |
| 환율 1,393.6원(2022-09-22) · 1,341원(11/3) | 1393.6 · 1341 | S6 https://ecos.bok.or.kr/ |
| 최고 1,554.4원(2026-07-02) · 최저 1,219.3원(2023-02-03) | max·min | S6 |
| 다음 FOMC 12월 8~9일 | December 8-9* | S2 https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm |
| 한국은행 11월 26일 (2차) | 11월 26일 | S7 https://blog.naver.com/zappu/224463007537 · https://blog.naver.com/lsyivy0722/224458601600 |

# 올리기 전 확인
- 2026-11-04 13:46 firemap-write-b — 발행 당일(16:10 칸) 대조 칸 출처 전부 다시 엶
  - S1 https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm — 200, '3-3/4 to 4 percent'·'Inflation remains elevated'·'1/4 percentage point' 그대로
  - S2 https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm — 200, 2026 December '8-9*' 그대로
  - S3 https://fred.stlouisfed.org/series/DFEDTARU — FRED API 11/4: DFEDTARU 2026-11-03 4 · DFEDTARL 3.75 그대로
  - S4·S6 https://ecos.bok.or.kr/ — ECOS API 11/4: 722Y001 기준금리 2026-11-01 3 그대로 · 731Y001 환율 11/3 1,341 그대로, 11/4 1,341.2 새로 나옴
  - S5 https://eiec.kdi.re.kr/policy/materialView.do?num=288401 — 오늘은 '정상적인 접근이 아닙니다' 안내만 나옴(봇 차단). 같은 결정은 한국은행 원문 일정표(아래)의 10월 22일(목) 국문보도자료(2610)로 확인
  - S7(2차) https://blog.naver.com/zappu/224463007537 · https://blog.naver.com/lsyivy0722/224458601600 · https://secretlinker.co.kr/?p=6521 — 한국은행 원문으로 대신 확인(아래)
- 기준일: 금리 2026-11-03(FRED)·2026-11-01(ECOS 일별 마지막 값), 환율 2026-11-03 매매기준율, 역전 일수 11/3 기준 1,503일 — 본문 c00·c06은 '11월 3일 기준'으로 날짜를 박아 두어 그대로 맞음. 환율도 11/3 값이라 일수와 기준일이 같아 고치지 않음(묶음 해시 그대로)
- 바뀐 것: 없음 — 미국 3.75~4%(11/3)·한국 3.00%(11/1)·차이 1%p 그대로, 환율 11/4 1,341.2원(본문 11/3 1,341원과 0.2원 차, 본문은 11/3 기준이라 그대로), 연준 다음 회의 12월 8~9일 그대로
- 새로 찾은 것: 한국은행 통화정책방향 결정회의 일정 원문 https://www.bok.or.kr/portal/singl/crncyPolicyDrcMtg/listYear.do?mtgSe=A&menuNo=200755 (raw/bok_mtg_1104.html) — 2026년 10월 22일(목) 국문보도자료(2610) 다음 칸이 11월 26일(목). S7을 1차로 확인함
