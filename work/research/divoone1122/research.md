# divoone1122 자료조사 (카페 11/22 22:40 배당 칸 — 쇼츠 de1s_divo S-bh4F6JB-k 짝 글, firemap-write-b 11/21 13:40 회차) — 배당 ETF, 직접 계산형

## 검증
- 수요: 쇼츠 짝 글(사장님 10/11 '유튜브에 올린 것은 카페에도 반드시 글') · 쇼츠 이해 시험 '남은 궁금증: 12월 돈이 실제로 무엇이었나'(cardshorts/de1s_divo/understand.md) · toprank 'DIVO 분배율' 상위 8편 중 6편이 한 달 안 글(11/21) · kwvol은 이번 회차 안 잼(확인 안 함)
- 경쟁에서 터진 증거: 쇼츠 경쟁 멘토리 '월급 말고 배당금으로' 4.9만 회(cardshorts/de1s_divo/compete.md) · 블로그 상위 1 awxs2_ 댓글 2
- 겹침: 옛 #79 divocal(9/24 '12개월 배당 더하면 왜 공시 분배율보다 높나')은 12월 0.953의 성격을 '확인 못 함'으로 둠 — 이번은 그 성격(공지 3건)·해마다 반복 여부(7년)·다른 ETF 8개 비교라 각도 다름 · 11/22 tigerdj1122(SCHD vs TIGER 총수익)·11/21 kdiv·divbear와도 다름
- 칸: 11/22 22:40 배당(slots.json, 관문 기한 11/22 16:40)

## 원문
- S1 야후 파이낸스 chart API 분배 기록·종가(range=2y, events=div) DIVO·JEPI·JEPQ·QYLD·XYLD·SCHD·SPYD·VYM·HDV·DGRO, 2026-11-21 받음(raw/*_chart_20261121.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/DIVO
- S2 같은 자료로 직접 계산(calc.py → calc_out.txt) — 원자료 S1
- S3 야후 DIVO 10년 분배 기록(raw/DIVO_10y_20261121.json) → calc2.py → calc2_out.txt: https://query1.finance.yahoo.com/v8/finance/chart/DIVO?range=10y&interval=1mo&events=div
- S4 Amplify 19a-1 통지문 DIVO(2025-12-31 지급) — 표 'Estimated Return of Capital $0.8928 94%'(11/21 PDF 텍스트 뽑음 raw/doc_6vovvs.txt): https://amplifyetfs.com/wp-content/uploads/files/19a-1_Notice_12-31-25_DIVO.pdf
- S5 Amplify 2025 Year-End Distribution Estimates(as of 12/12/2025) DIVO 0.97$(raw/doc_kyjwiz.txt): https://amplifyetfs.com/wp-content/uploads/files/2025_Year_End_Distributions.pdf
- S6 BOX Exchange 공지 207477 DIVO 단기 자본이득 분배 $0.58672(raw/doc_e1xjm4.txt): https://boxexchange.com/assets/BOXOnnMemo207477.pdf
- S7 쇼츠 https://youtu.be/S-bh4F6JB-k (11/22 19:20 공개 예약) · 롱폼 https://youtu.be/mkAxQPGaDqc (10/30 공개) · 쇼츠 11/19 값 cardshorts/de1s_divo/prepub_1120.txt

## 경쟁
- toprank.txt('DIVO 분배율' 블로그 상위 8, 11/21). 1(awxs2_)·4(salarytoasset)는 기본 정보+1,000만원이면 월 얼마, 7(lim_and_jin)은 4.88% vs SEC 1.40% 차이, 5(hyjoyer)는 '2025년 12월 0.95339달러 평소보다 큰 분배' 한 줄만 짚고 성격·반복 여부 없음, 6(royal23-)은 DIVO vs QYLD. 12월 돈의 성격을 원문으로 확인하거나 해마다 나왔는지 센 글 0편, 다른 배당 ETF와 같은 잣대로 비교한 글 0편 → bench.md

## 질문
1. DIVO 분배율은 왜 사이트마다 다른가 — https://blog.naver.com/lim_and_jin/224436629727 (제목 'DIVO ETF 월배당, 4.88%와 1.40% 왜 다를까?') → 답: 12개월 합 6.88%에 12월 한 번이 섞임, 운용사 값은 최근 한 번 연환산
2. 12월 큰 분배금은 무슨 돈이었나 — https://youtu.be/S-bh4F6JB-k (쇼츠 이해 시험 남은 궁금증, cardshorts/de1s_divo/understand.md) → 답: 운용사가 12/12 연말 분배 0.97달러 예고, 19a-1 장부 추정 94% 원금 돌려주기, BOX 0.58672 단기 자본이득
3. 매달 얼마 받나·앞으로도 그만큼 나오나 — https://blog.naver.com/awxs2_/224468785266 (제목 '미국 월배당 ETF DIVO, 매달 얼마 받을까?') → 답: 평달 0.18~0.21달러, 큰 12월은 7년 중 두 번
4. 다른 월배당 ETF와 비교하면 — https://blog.naver.com/salarytoasset/224484361326 (제목 '… JEPQ·JEPI 비교') → 답: 한 번 때문에 크게 부푼 건 9개 중 DIVO뿐

## 왜
- 왜 12월에 컸나: 운용사 연말 분배 예상표(S5)에 미리 올린 연말 분배 — 무슨 거래로 생긴 돈인지는 원문에 이유 없음(19a-1·BOX 분류만)
- 왜 19a-1과 BOX가 다른가: 19a-1은 '장부 기준 추정, 세금 신고용 아님'이라 적음(S4) — BOX는 회사 발표 분류를 옮김. 어느 쪽이 최종인지 1099-DIV 미확인
- 왜 평균으로 바꾸나: 분기 ETF는 한 번 빼면 4분의 1이 빠져 불공정 — 같은 잣대

## 그래서
- DIVO 분배율로 생활비를 계산한다면 평달 0.19달러 기준(5.1%쯤)으로 잡음, 12월 큰 돈은 해마다 온다고 보지 않음
- 다른 월배당 ETF도 12개월 기록을 열어 튄 회차가 있는지 봄
- 올해 12월 분배는 운용사 연말 예상표가 나오면 확인

## 누구라면
- 배당을 생활비로 꺼내 쓰는 사람: 6.88%로 계산하면 1년 받을 돈을 넉넉히 잡게 됨
- 배당 재투자로 모으는 사람: 분배율보다 총수익(롱폼 mkAxQPGaDqc)이 중요 — 이 글은 분배율만
- 분기 배당 ETF(SCHD 등) 가진 사람: 한 번 빼기 말고 평균으로 바꿔 봐야 함

## 함정
- 12개월 합 분배율을 '앞으로 1년 받을 돈'으로 보는 것 — 튄 한 달이 섞일 수 있음
- '원금 돌려주기 94%'를 최종 세금 성격으로 보는 것 — 운용사가 추정이라 밝힘
- 분기 ETF에서 한 번을 그냥 빼는 것

## 한계
- 1099-DIV(2025년 세금 서류) 최종 성격은 확인 안 함
- 운용사 공식 페이지(amplifyetfs.com/etfs/divo)는 자바스크립트로 그려져 이번에 직접 못 읽음 — 분배율 4.85%는 2차 2곳
- 야후 분배 기록 하나로 셈(운용사 분배 표와 회차별 대조는 #79 9/24에 한 것뿐)
- 원화·세금(미국 15%)·환율 뺌
- HDV는 분배 주기가 바뀌어 뺌, 국내 상장 커버드콜 ETF는 안 셈

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 12개월 합 3.026달러·11/20 종가 43.98·6.88% | 3.0260 · 43.98 · 6.88% | S1·S2 calc_out.txt |
| 쇼츠 6.78%(하루 앞 종가) | 6.78%(11/19 44.66) | S7 prepub_1120.txt |
| 2025-12-30 0.953달러·나머지 0.18~0.21·다섯 배쯤 | 0.9530 · 0.179~0.214 · 5.1배 | S1·S2 calc_out.txt |
| 빼면 4.71%·평균(0.19)으로 바꾸면 5.14%·5.1%쯤 | 4.71% · 5.14% | S1·S2 calc_out.txt |
| 운용사 분배율 최근 한 번 1년 치로·4%대 | 4.85%(10/31, 연환산) — 2차 | https://blog.naver.com/royal23-/224483947359 · https://blog.naver.com/dividendwhisky/224467524365 |
| 12/12 연말 분배 예상 0.97달러 | 0.97$(as of 12/12/2025) | S5 https://amplifyetfs.com/wp-content/uploads/files/2025_Year_End_Distributions.pdf |
| 12/30 기준 주주 0.9534달러 | $0.9534 record 12/30 payable 12/31 | S4 https://amplifyetfs.com/wp-content/uploads/files/19a-1_Notice_12-31-25_DIVO.pdf |
| 장부 추정 94% 원금 돌려주기·1099-DIV | Estimated ROC 94% · book basis · 1099-DIV | S4 |
| BOX 0.58672달러 단기 매매 차익 분배 | short-term capital gains $0.58672 | S6 https://boxexchange.com/assets/BOXOnnMemo207477.pdf |
| 2019 1.004·7.4배 / 2025 0.953·5.5배 / 2020~2024 0.14~0.17 | 1.004·7.4 / 0.953·5.5 / 0.144~0.165 | S3 calc2_out.txt |
| DIVO 1.74 · JEPQ 0.27 · XYLD 0.16 · JEPI 0.14 · DGRO 0.13 · SPYD 0.09 · SCHD 0.06 · VYM 0.05 · QYLD 0.04 %포인트 | 같음 | S1·S2 calc_out.txt |
| 분기 ETF 한 번 빼면 4분의 1쯤 줄어 | SCHD 3.11→2.29%(4회 중 1) | S1·S2 calc_out.txt |
| HDV 7월부터 매달 기록 | 2026-07-15·08-19·09-16·10-21·11-18 | S1 calc_out.txt |

# 올리기 전 확인
- 2026-11-21 14시대 firemap-write-b(조사·작성 날, 발행 날 11/22 22:40 write-b 회차가 야후 다시 받아 종가·분배율 줄 갱신 — 11/21 종가)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/DIVO (JEPI·JEPQ·QYLD·XYLD·SCHD·SPYD·VYM·HDV·DGRO 같은 꼴, 11/21 받음) · https://amplifyetfs.com/wp-content/uploads/files/19a-1_Notice_12-31-25_DIVO.pdf · https://amplifyetfs.com/wp-content/uploads/files/2025_Year_End_Distributions.pdf · https://boxexchange.com/assets/BOXOnnMemo207477.pdf · https://blog.naver.com/royal23-/224483947359 · https://blog.naver.com/dividendwhisky/224467524365 · https://query1.finance.yahoo.com/v8/finance/chart/DIVO?range=10y&interval=1mo&events=div (10년 분배, 11/21 받음) · https://youtu.be/mkAxQPGaDqc (공개) · https://youtu.be/S-bh4F6JB-k (11/22 19:20 공개 예약 — 발행 회차가 공개 확인)
- 기준일: 야후 2026-11-20 종가(11/21 조회) · 분배 기록 2026-11-18까지
- 바뀐 것: 쇼츠(11/19 종가 44.66, 6.78%·빼면 4.64%) → 11/20 종가 43.98, 6.88%·빼면 4.71%
- 새로 찾은 것: 12월 분배 성격 공지 3건(연말 예상 0.97·19a-1 ROC 94% 추정·BOX 단기 자본이득 0.58672) · 큰 12월 7년 중 2번 · 배당 ETF 9개 중 DIVO만 크게 부풂
- 조사 뒤 공표: data/release_calendar.json — 가격 매일, DIVO 11월 분배 배당락 11월 말 예정(확인 안 함) — 발행 날 다시 받아 12개월 창이 바뀌면 갱신
