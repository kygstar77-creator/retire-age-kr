# coinyu1116 자료조사 (카페 비축 — firemap-write-b 11/16 16:40 회차) — 세금(가상자산) 장르, 원문 정리+직접 계산형

## 검증
- 수요: kwvol 11/16 코인과세 35,830 · 가상자산과세 33,240 · 코인과세유예 20,090 · 가상자산과세유예 17,740
- 우리 제목: '코인·가상자산' 3편(#321 coin1019 '코인 과세 시작 전…'은 2027년 시작 기준 — 11/5 발표로 낡음, 이 글이 뒤를 잇는 글), '유예·이월공제' 0편
- 경쟁: 블로그 상위 8편(toprank.txt) 전부 '확정됐나'·일정 정리, 실제 비트코인 값으로 이월공제 효과를 셈한 글 0편(bench.md)

## 원문
- S1 대한민국 정책브리핑 11/5 '가상자산 소득과세 2년 유예 추진…2029년 시행 기반 마련' https://www.korea.kr/news/policyNewsView.do?newsId=148975124 (raw/3b0df9.txt) — 2년 유예, CARF 미국 정보교환 2029년, 손실 이월공제 3년, 워킹그룹·2027 정기국회, 2026-11-16 확인
- S2 KDI 경제교육·정보센터 재정경제부 자료 https://eiec.kdi.re.kr/policy/materialView.do?num=289147&topic=P (raw/0b3389.txt) — '2029년 시행', '3년간 손실 이월공제', 2026-11-16 확인
- S3 국가법령정보센터 소득세법 제37조⑤·제64조의3②·제84조3호 https://www.law.go.kr/법령/소득세법/제37조 (raw/law_current.txt, 내장 브라우저로 본문 확인) — 2027.1.1 시행, 2026.12.31 시가와 취득가 중 큰 금액, (소득-250만원)×20%, 2026-11-16 확인
- S4 아이뉴스24 11/5(2차) https://inews24.com/view/2023113 — 의제 기준일 2028.12.31, 시행 전 확정 손실 제외, 250만원 먼저 빼고 이월 손실 차감·연도 선택 불가(세제실장 설명)
- S5 SBS Biz 11/5(2차) https://biz.sbs.co.kr/amp/article/20000344472 — 2028.12.31 시가, 올해·내년 확정 손실 제외, 1천만원 손해·이익 예시 165만원→0
- S6 업비트 API 일봉 https://api.upbit.com/v1/candles/days?market=KRW-BTC (raw/up_BTC_*.json, 11/16 받음)
- S7 연합뉴스 11/11(한민족센터 게재, 2차) https://www.koreancenter.or.kr/news/articleView.html?idxno=1438059 — 조세소위 유예 공감대, 의결 안 함(공제 상향 정부 반대·자료 제출 시기 이견), 최종 의결은 조세소위 마지막 날
- S8 한국세정신문 김상훈 의원안(2차) https://www.taxtimes.co.kr/news/article.html?no=276600 — 시행일 2027.1.1→2029.1.1 개정안, 현행 이월공제 불허

## 경쟁
bench.md 6편 — 전부 일정·확정 여부·세율 예시. 1천만원 이익 165만원 예시는 3편, 이월공제 설명은 4편, 실제 과거 시세로 셈한 글 0편, '시행 전 확정 손실 제외'를 올해 하락과 이은 글 0편.

## 질문
1. 코인 다들 물려 있는데 과세? — https://m.kin.naver.com/qna/dirs/40102/docs/493805169 → 답: c04(물린 코인은 실제 산 값 그대로 기준, 시행 전 확정 손해는 이월 안 됨)
2. 지난해 코인 손실을 다음 해 신고 때 빼 주나 — https://m.kin.naver.com/qna/dirs/40102/docs/485601790 → 답: c02·c04(지금 법은 안 됨, 정부 안은 시행 뒤 손해만 3년)
3. 코인은 아직 세금 유예인데 신고해야 하나 — https://m.kin.naver.com/qna/dirs/40102/docs/486223544 → 답: c01(아직 과세 전, 의결 전까지 2027년 시작이 법)
4. 비트코인 손실 이월 불가라던데 — https://m.kin.naver.com/qna/dirs/40102/docs/487228081 → 답: c02·c03(정부 안이면 3년, 얼마 줄어드는지 계산)
5. 코인과세유예 확정됐나(검색 20,090) — https://m.search.naver.com/search.naver?query=%EC%BD%94%EC%9D%B8%EA%B3%BC%EC%84%B8%EC%9C%A0%EC%98%88 → 답: c01

## 왜
- 미루는 이유: 미국과의 CARF 정보교환이 2029년부터라 그전 과세는 국내 시장만 불리, 디지털자산법 제정 변화(S1)
- 이월공제 넣는 이유: 높은 가격 변동성 — 일정 기간 손익을 통산하는 게 합리적이라는 전문가 제안, 미국·영국도 인정(S1)
- 올해·내년 손실이 빠지는 이유: 원문(정책브리핑)에 이유 문장은 없음 — 시행 전 손익은 과세 대상이 아니어서로 보임(추측이라 글에 안 씀)
- 이익 해에 세금이 많은 이유: 250만원 공제·세율이 '해당 과세기간' 소득에만 붙음(S3 64조의3②)

## 그래서
- 법 통과 전까지는 2027년 시작이 법: 의결 결과(조세소위 마지막 날·본회의)를 확인
- 처음 산 날 거래 내역 보관: 물린 코인은 실제 산 값이 기준
- 손해 난 코인을 올해·내년에 팔아 확정해도 2029년 이후 이익에서 못 뺌(제도상 사실 — 팔라·들고 있으라 권유 아님)

## 누구라면
- 올해 초 1천만원어치 산 분: 지금 약 691만원(S6) — 실제 산 값 1천만원이 2028년 말 값보다 크면 그대로 기준
- 오래전에 싸게 산 분: 2028년 말 값까지 오른 몫은 세금 0(정부 안), 현행이면 2026년 말 값까지
- 해마다 사고파는 분: 손해 본 해 다음에 이익이 나면 이월공제 효과가 큼(c03 계산)

## 함정
- '유예 확정'이 아님: 11/11 조세소위 의결 안 함(S7)
- 이월공제는 250만원을 먼저 빼고 남은 데서 손해를 뺌, 연도 고르기 불가(S4)
- 시행 전 확정 손실은 이월 안 됨(S4·S5)

## 우리만
- 업비트 연말 종가로 2018~2025년 해마다 오르내림 계산: 손해 본 해 3번(-78.2%·-62.9%·-8.0%), 2026년 11/16까지 -30.9% (calc_out.txt §1)
- 2022년 손해→2023년 이익이면 세금 320만원→182만원(138만원 줄어), 2018→2019년이면 160만원→0원 (calc_out.txt §2)

## 예외
- 같은 해 안에서 코인끼리 손익은 지금 법도 합쳐서 셈 — 이 경우 이월공제와 무관
- 해외 거래소·개인 간 거래는 정보 확보가 늦어 세부 기준이 따로 정해짐(워킹그룹, 2028년 상반기 세부 기준, S4)
- 1년 이익이 250만원 이하면 세금 없음(S3 84조3호)

## 한계
- 정부 안 세부(기준일 2028.12.31, 공제 순서, 시행 전 손실 제외)는 보도자료 원문 PDF를 못 받아 정책브리핑 요약(S1) + 2차 보도 2곳(S4·S5)으로 확인
- 업비트 하나의 연말 종가로 셈 — 실제 기준 시가는 국세청이 고시하는 사업자들 평균(시행령 88조②)
- '해마다 1천만원 사고팖'은 이해를 돕는 가정, 수수료 뺌
- 조세소위 최종 결과(공제 상향 여부)는 11/16 기준 미정

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 11월 5일 2년 유예 발표, 미국과 정보 교환 2029년 | '2년간 유예', 'CARF … 2029년부터' | S1 https://www.korea.kr/news/policyNewsView.do?newsId=148975124 |
| 시작 2029년 1월 1일 | '2029년 시행' · 개정안 2029.1.1 | S2 https://eiec.kdi.re.kr/policy/materialView.do?num=289147&topic=P |
| 지금 법 2027년 1월 1일 시작·2026년 12월 31일 값 | 37조⑤·[시행일: 2027. 1. 1.] | S3 https://www.law.go.kr/법령/소득세법/제37조 |
| 2028년 12월 31일 값과 실제 산 값 중 큰 쪽(2차) | '2028년 12월 31일 시가' | S4 https://inews24.com/view/2023113 · S5 https://biz.sbs.co.kr/amp/article/20000344472 |
| 손해 본 뒤 3년 이익에서 뺌 | '3년간 손실 이월공제' | S1 https://www.korea.kr/news/policyNewsView.do?newsId=148975124 |
| 250만원 먼저, 남은 데서 손해 · 연도 못 고름(2차) | 세제실장 설명 | S4 https://inews24.com/view/2023113 · S5 https://biz.sbs.co.kr/amp/article/20000344472 |
| 시행 전 팔아 확정한 손해 빠짐(2차) | '이미 팔아서 확정된 손실은 이월공제 대상이 아니다' | S4 https://inews24.com/view/2023113 · S5 https://biz.sbs.co.kr/amp/article/20000344472 |
| 250만원 빼고 22%(지방 포함), 1천만원이면 165만원 | 64조의3② 20% · 계산 | S3 https://www.law.go.kr/법령/소득세법/제37조 |
| 11/11 조세소위 이견 없음·의결 안 함·최종 의결 마지막 날(2차) | 연합 11/11 | S7 https://www.koreancenter.or.kr/news/articleView.html?idxno=1438059 · S8 https://www.taxtimes.co.kr/news/article.html?no=276600 |
| 공제 상향 정부 반대(2차) | '정부가 … 기본공제 상향에 대해 반대' | S7 https://www.koreancenter.or.kr/news/articleView.html?idxno=1438059 · https://blog.naver.com/zukem/224478180831 |
| 8해 중 손해 3번, 2022 -63%·2023 +171% | calc_out §1 | S6 https://api.upbit.com/v1/candles/days?market=KRW-BTC |
| 629만원 손해→1,706만원 이익: 320만원→182만원, 138만원 | calc_out §2 | S6 https://api.upbit.com/v1/candles/days?market=KRW-BTC |
| 782만원 손해→979만원 이익: 160만원→0원 | calc_out §2 | S6 https://api.upbit.com/v1/candles/days?market=KRW-BTC |
| 정부 예시 1천만원 손해·이익 165만원→0원(2차) | SBS 예시 · calc_out §3 | S5 https://biz.sbs.co.kr/amp/article/20000344472 · S4 https://inews24.com/view/2023113 |
| (본문에서 뺌 — 2차 이해 시험 3/3 '버텨라'로 읽힘) 2026년 약 31% 하락 | calc_out §1·§5 | S6 https://api.upbit.com/v1/candles/days?market=KRW-BTC |
| 2029년 이후 손해는 다음 3년 이익에서, 2029년 손해면 2032년까지(2차) | 세제실장 설명 | S4 https://inews24.com/view/2023113 · S5 https://biz.sbs.co.kr/amp/article/20000344472 |
| 이더리움 같은 다른 코인도 같은 방식 | 21조①27호 가상자산 | S3 https://www.law.go.kr/법령/소득세법/제37조 |

# 올리기 전 확인
- 2026-11-16 17:1x firemap-write-b(비축 만든 날 — 발행 회차가 발행 날 다시 확인: 조세소위 의결 여부·공제 상향·기준일)
- 다시 연 주소(이번 회차에 받음, raw/): https://www.korea.kr/news/policyNewsView.do?newsId=148975124 · https://eiec.kdi.re.kr/policy/materialView.do?num=289147&topic=P · https://www.law.go.kr/법령/소득세법/제37조 · https://inews24.com/view/2023113 · https://biz.sbs.co.kr/amp/article/20000344472 · https://www.koreancenter.or.kr/news/articleView.html?idxno=1438059 · https://www.taxtimes.co.kr/news/article.html?no=276600 · https://blog.naver.com/zukem/224478180831 · https://api.upbit.com/v1/candles/days?market=KRW-BTC
- 기준일: 2026-11-16(업비트 종가·법령·보도 조회)
- 바뀐 것: 처음 받음 — #321(10/19) 때와 달리 정부가 2년 유예·이월공제 3년 발표, 기준일 2026.12.31→2028.12.31(안)
- 새로 찾은 것: 2018~2025 연말 종가로 이월공제 효과 직접 계산(320만원→182만원)
