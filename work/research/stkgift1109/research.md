# stkgift1109 자료조사 (카페 2026-11-09 19:40 회차 write-b — 11/10 :40 빈 칸 몫) — 세금(증여세)·주식 장르, 제도·계산 글

## 검증
- 수요: work/kwvol.py 11/9 — 주식증여세 1,040 · 주식증여 780 · 자녀주식증여 470 · (참고) 자녀증여한도 17,170 · 증여세계산기 12,890
- 겹침: 우리 카페 최근 120묶음에 주식 증여 글 없음(결혼 증여 marrygift1017·직거래 directdeal1019와 대상 다름) · 11/10 칸은 07:40 퇴직연금·12:40 주담대·16:10 해외주식 양도세 → 같은 날 세금 글 2편이라 22:40 칸으로 둠(회의가 옮겨도 됨)
- 경쟁에서 터진 증거: '주식 증여세' 블로그 탭 상위 8편 중 5편이 11/6 폭락 뒤 이틀 안에 쓴 '폭락장 증여' 글(toprank 11/9) — 지금 쓰이는 주제
- 오늘 이슈: issues.md 11/9 '급락후 韓증시만 반등 못했다'·'코스피 0.8% 또 하락'

## 원문
- S1 상속세 및 증여세법 제63조①1가·③ 2026-11-09 확인(raw/law_sz63.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제63조
- S2 같은 법 제53조 2026-11-09 확인(raw/law_sz53.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제53조
- S3 같은 법 제26조·제56조 2026-11-09 확인(raw/law_sz26.txt·law_sz56.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제26조
- S4 같은 법 제69조② 2026-11-09 확인(raw/law_sz69.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제69조
- S5 같은 법 제68조① 2026-11-09 확인(raw/law_sz68.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제68조
- S6 같은 법 제4조④ 2026-11-09 확인(raw/law_sz4.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제4조
- S7 같은 법 제47조② 2026-11-09 확인(raw/law_sz47.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법/제47조
- S8 같은 법 시행령 제24조② 2026-11-09 확인(raw/law_szr24.txt): https://www.law.go.kr/법령/상속세%20및%20증여세법%20시행령/제24조
- S9 국세기본법 제5조① 2026-11-09 확인(raw/law_gb5.txt): https://www.law.go.kr/법령/국세기본법/제5조
- S10 네이버 금융 일별 종가 삼성전자 2026-11-09 20시 받음(raw/px_005930.KS.json): https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day
- S11 네이버 금융 일별 종가 코스피 2026-11-09 20시 받음(raw/px_^KS11.json): https://api.finance.naver.com/siseJson.naver?symbol=KOSPI&requestType=1&startTime=20250101&endTime=20261109&timeframe=day
- S12 네이버 금융 일별 종가 KODEX 200 2026-11-09 20시 받음(raw/px_069500.KS.json): https://api.finance.naver.com/siseJson.naver?symbol=069500&requestType=1&startTime=20250101&endTime=20261109&timeframe=day

## 경쟁
- bench.md 참조. 6편 모두 '앞뒤 2개월 평균'을 말함. 실제 지난 폭락일로 다시 계산한 글 0편(1·7은 가상 숫자, 2는 11/6 하루만) · 반환 규정은 2(ragepose)만 표로 · '올해 폭락일 중 몇 번이 평균>종가였나'는 0편

## 질문
1. 상장주식 증여세는 증여한 날 종가로 신고하나 — https://kin.naver.com/qna/detail.naver?dirId=40309&docId=495734914 → 답: c00·c01(넉 달 평균, S1)
2. 전 2개월·후 2개월 평가금액은 어떻게 계산하나 — https://kin.naver.com/qna/detail.naver?dirId=40303&docId=491351650 → 답: c01(거래소 종가 평균, 7/28 예시)
3. 증여한 주식을 3개월 안에 돌려받으면 — https://kin.naver.com/qna/detail.naver?dirId=40303&docId=488162599 → 답: c03(신고기한 안 반환은 없던 것, 기한 뒤 3개월은 반환만 비과세, S6)
4. 하락하는 주식을 성인 자녀에게 증여하면 — https://kin.naver.com/qna/detail.naver?dirId=60220&docId=427702138 → 답: c00·c02(19일 중 12일 평균>종가, 뒤 두 달이 정함)
5. 현금 증여 뒤 주식 매수했는데 취소되나 — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=494396624 → 답: c03(현금은 반환 규정에서 빠짐)

## 왜
- 평균으로 매기는 이유: 법 원문에 목적 문장은 없음(S1) — 글엔 '법이 이렇게 정한다'까지만
- 폭락일 증여가 오히려 높게 잡히는 이유: 앞 두 달은 이미 지난 높은 가격(S1 기간 정의 + S10 실제 값)
- 반환하면 없던 일로 보는 이유: 원문에 이유 없음, 조건(금전 제외·신고기한·결정 전)만(S6)

## 그래서
- 증여 뒤 두 달이 지나 평균을 확인하고, 너무 높으면 신고기한 안에 주식 그대로 돌려받기(S1·S5·S6)
- 기한 안에 신고해 3% 공제(S4)
- 10년 안 받은 증여를 합쳐 공제 한도 확인(S2·S7)

## 누구라면
- 성인 자녀: 공제 5천만원 — 7/28 예시 세금 약 134만원(종가로는 0원)
- 미성년 자녀: 공제 2천만원 — 약 425만원(종가로는 약 290만원)
- 현금으로 주는 사람: 반환 규정 못 씀(S6)
- 최대주주(대기업): 20% 더해 평가(S1 ③) — 글 대상 밖

## 함정
- 그날 종가로 공제 한도를 맞추면 평균이 높게 나와 한도를 넘을 수 있음(c01)
- 현금 반환은 없던 일 안 됨(S6)
- 신고기한 지나 돌려주면 처음 증여 세금은 그대로(S6)
- 세무서 결정 뒤 반환은 안 됨(S6)

## 우리만
- 2026년 코스피 -5% 이하 23일 중 평가 기간 끝난 19일을 실제 거래소 종가로 다시 계산: 삼성전자·KODEX 200 모두 12일은 평균>종가(calc.py) — 경쟁 0편
- 7/28 삼성전자 5천만원어치 → 평가액 약 6,377만원·세금 약 134만원 / 6/26 → 약 4,155만원 (calc.py)
- 11/6 증여라면 평가액이 그날 종가까지 오려면 남은 두 달 평균 14만원 아래(calc.py, 거래일 수 근사)

## 예외
- 최대주주 할증(S1 ③), 증자·합병이 평가 기간에 있으면 기간이 달라짐(S1 ①1가 괄호) → 글 대상 밖
- 해외주식은 평가 방법이 다를 수 있음(이번 조사 범위 밖) → 글은 국내 상장주식만
- 혼인·출산 증여공제(제53조의2)는 따로 1억원 — 글에서 다루지 않음

## 한계
- 11/6 '14만원 아래'는 뒤 2개월 거래일 수를 앞 2개월과 같은 40일로 근사한 값 → 글엔 '아래로'로만
- 평가 기간 경계일(포함 여부)은 원문 '각 2개월'만 — 하루 차이로 평균이 아주 조금 달라질 수 있음
- 국세청 홈택스 상장주식 평가 조회 화면은 확인 안 함 → 글에 안 씀
- 2027년 2월 28일 다음 첫 평일 날짜는 공휴일 규정 원문 확인 안 해 '그 뒤 첫 평일'로만

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 앞 2개월·뒤 2개월 종가 평균 | 평가기준일 이전·이후 각 2개월 최종 시세가액 평균액 | S1 https://www.law.go.kr/법령/상속세%20및%20증여세법/제63조 |
| 성인 자녀 5천만원·미성년 2천만원·10년 합산 | 제53조 2호, 10년 이내 공제받은 금액 합산 | S2 https://www.law.go.kr/법령/상속세%20및%20증여세법/제53조 |
| 세율 10%(1억원 이하) | 제26조 1억원 이하 100분의 10 | S3 https://www.law.go.kr/법령/상속세%20및%20증여세법/제26조 |
| 기한 안 신고 3% | 제69조② 100분의 3 | S4 https://www.law.go.kr/법령/상속세%20및%20증여세법/제69조 |
| 신고기한 증여한 달 말일부터 3개월 | 제68조① | S5 https://www.law.go.kr/법령/상속세%20및%20증여세법/제68조 |
| 신고기한 안 반환 = 처음부터 없던 것, 현금 제외, 결정 전 | 제4조④ | S6 https://www.law.go.kr/법령/상속세%20및%20증여세법/제4조 |
| 기한 뒤 3개월 안 반환은 반환에 세금 없음 | 제4조④ 후단 | S6 https://www.law.go.kr/법령/상속세%20및%20증여세법/제4조 |
| 자녀 계좌에 들어온 날 | 시행령 제24조② 인도받은 사실이 객관적으로 확인되는 날 | S8 https://www.law.go.kr/법령/상속세%20및%20증여세법%20시행령/제24조 |
| 2월 28일 일요일이라 그 뒤 첫 평일 | 국세기본법 제5조① 토·일·공휴일이면 다음날 | S9 https://www.law.go.kr/법령/국세기본법/제5조 |
| 7/28 코스피 10% 넘게 빠짐 | 전날 대비 -10.84% (calc.py) | S11 https://api.finance.naver.com/siseJson.naver?symbol=KOSPI&requestType=1&startTime=20250101&endTime=20261109&timeframe=day |
| 7/28 삼성전자 22만원·넉 달 평균 약 28만 1천원 | 220,000 · 280,904 | S10 https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day |
| 227주·약 6,377만원·초과 약 1,377만원·약 134만원 | 63,765,120 · 13,765,120 · 1,335,217 | S10 https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day · S2 https://www.law.go.kr/법령/상속세%20및%20증여세법/제53조 · S4 https://www.law.go.kr/법령/상속세%20및%20증여세법/제69조 |
| 미성년 약 290만원 → 약 425만원 | 2,904,180 · 4,245,217 | S2 https://www.law.go.kr/법령/상속세%20및%20증여세법/제53조 · S10 https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day |
| 23일 중 19일, 12일 평균>종가, 7일 낮음 | calc_out.txt | S11 https://api.finance.naver.com/siseJson.naver?symbol=KOSPI&requestType=1&startTime=20250101&endTime=20261109&timeframe=day · S10 https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day · S12 https://api.finance.naver.com/siseJson.naver?symbol=069500&requestType=1&startTime=20250101&endTime=20261109&timeframe=day |
| 6/26 33만 9,500원·약 4,155만원 | 339,500 · 41,549,012 | S10 https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day |
| 11/6 19만 3,500원·앞 두 달 약 24만 6천원·14만원 아래 | 193,500 · 246,312 · 139,490 | S10 https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day |

# 올리기 전 확인
- 2026-11-10 19:43 발행 당일 다시 엶(write-b 19:40 회차): 조문 9개(상증법 제4·26·47·53·63·68·69조, 같은 법 시행령 제24조, 국세기본법 제5조)를 국가법령정보센터 웹(work/lawweb.py)으로 다시 받아 11/9 본과 글자 대조 — 9개 모두 같음(raw/1110/) · 법령 API(OC=test)는 사용자 검증 실패라 웹으로 받음
- 2026-11-10 19:43 종가 다시 받음: https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261110&timeframe=day · symbol=069500 · symbol=KOSPI 같은 주소(endTime 20261110) → calc.py 기준일만 11/10으로 다시 돌림(calc_out_1110.txt)
- 기준일: 2026년 11월 10일
- 바뀐 것: 조문 바뀐 것 없음 · 11/10 삼성전자 종가 197,700·코스피 5,239.13 · 올해 5% 넘게 빠진 날 23일·평가 끝난 19일·평균>종가 12일 그대로 · 11/6 예시의 남은 거래일 평균 문턱 139,490→137,968원(본문 '14만원 아래' 그대로 맞음, 본문 고칠 것 없음)
- 새로 찾은 것: 11/10 하루 코스피 5% 하락 없음(23일 그대로) · 9/10 전후 폭락일 없어 11/10에 새로 평가가 끝난 날 없음
- (아래는 11/9 기록)
- 2026-11-09 20시 대조 칸 출처 S1~S12 전부 이번 회차에 처음 받음(raw/ 11/9 19:45~20:05) — 발행 날 다시 열어 이 칸을 다시 채운다
- 다시 연 주소: https://www.law.go.kr/법령/상속세%20및%20증여세법/제63조 · https://www.law.go.kr/법령/상속세%20및%20증여세법/제53조 · https://www.law.go.kr/법령/상속세%20및%20증여세법/제26조 · https://www.law.go.kr/법령/상속세%20및%20증여세법/제69조 · https://www.law.go.kr/법령/상속세%20및%20증여세법/제68조 · https://www.law.go.kr/법령/상속세%20및%20증여세법/제4조 · https://www.law.go.kr/법령/상속세%20및%20증여세법/제47조 · https://www.law.go.kr/법령/상속세%20및%20증여세법%20시행령/제24조 · https://www.law.go.kr/법령/국세기본법/제5조 · https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20250101&endTime=20261109&timeframe=day · https://api.finance.naver.com/siseJson.naver?symbol=KOSPI&requestType=1&startTime=20250101&endTime=20261109&timeframe=day · https://api.finance.naver.com/siseJson.naver?symbol=069500&requestType=1&startTime=20250101&endTime=20261109&timeframe=day · 질문 주소 https://kin.naver.com/qna/detail.naver?dirId=40309&docId=495734914 · https://kin.naver.com/qna/detail.naver?dirId=40303&docId=491351650 · https://kin.naver.com/qna/detail.naver?dirId=40303&docId=488162599 · https://kin.naver.com/qna/detail.naver?dirId=60220&docId=427702138 · https://kin.naver.com/qna/detail.naver?dirId=40102&docId=494396624
- 기준일: 2026년 11월 9일
- 바뀐 것: 상속세 및 증여세법 시행 2025.10.1 판 그대로(제63조·제53조·제4조 이번 개정 없음) · 11/9 삼성전자 종가 187,400(11/6 193,500에서 더 내림)
- 새로 찾은 것: 올해 폭락일 19일 중 12일 평균>종가(경쟁 0편) · 야후 종가가 거래소와 달라 네이버로 바꿈
- 조사 뒤 공표: data/release_calendar.json 해당 없음(제도 글)
