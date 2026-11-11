# p3pair1111 자료조사 (카페 2026-11-12 12:40 칸 — P-3 롱폼 짝 글, yt_pair vgFx2od9_sg · firemap-write 11/11 23시) — 건강보험 피부양자 연 2천만원 기준, 국민연금 월 얼마부터 보험료

## 검증
- 수요: work/kwvol.py 11/11 — 건강보험피부양자 12,600 · 피부양자 4,290 · 피부양자자격 1,790 · 피부양자소득기준 350 (월, PC+모바일)
- 겹침: P-3 영상과 같은 계산(2026년 요율)에 영상에 없던 2027년 요율(건보 7.19% 동결 + 장기요양 13.90%) 다시 계산과 분리과세 소득 부과 논의를 더함. 같은 날 07:40 bunrinhis1111(이자 1천만원 분리과세 건보료)과는 대상이 다름 — 이 글은 이자·배당을 한 줄(함정)만
- 경쟁에서 터진 증거: toprank '피부양자 탈락 기준 국민연금' 상위 8편 중 7편이 2주 안 작성(11/11 2편), incar_ansan 댓글 13 — 지금 쓰이는 주제

## 원문
- S1 국민건강보험법 시행규칙 [별표 1의2] — 소득 연 2천만원 이하, 재산 과표 5.4억~9억 소득 1천만원, 사업소득, 부부(제1호라목) — 2026-10-26 P-3 읽음, 2026-11-11 youtube-loop 다시 엶 200: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566181&bylClsCd=110201
- S2 시행령 제41조①5호·③, 제44조(1만분의 719): https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행령
- S3 시행규칙 제44조① 단서·②2호·③, 부칙<제907호> 제3조: https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행규칙
- S4 복지부 2025.11.4 장기요양 2026년 13.14%: https://www.mohw.go.kr/board.es?act=view&bid=0027&list_no=1487817&mid=a10503000000
- S5 복지부 2026.1.9 국민연금 2.1% 인상: https://mohw.go.kr/board.es?act=view&bid=0027&list_no=1488572&mid=a10503000000
- S6 공단 2025.12.26 보험료율 7.19%: https://www.nhis.or.kr/nhis/together/wbhaea01000m01.do?mode=view&articleNo=11008009
- S7 공단 웹진 2023.9 사적연금 불포함: https://www.nhis.or.kr/static/alim/paper/oldpaper/202309/sub/section3_3.html
- S8 복지부 2026.10.30 장기요양 2027년 13.90%: https://www.mohw.go.kr/board.es?mid=a10503000000&bid=0027&list_no=1492396&act=view
- S9 정책브리핑 2026.9.8 제15차 건정심 결과 브리핑 — 2027년 건강보험료율 7.19% 유지(2026-11-11 WebFetch로 읽음): https://www.korea.kr/policy/civilView.do?newsId=156780681
- S10 (2차) 분리과세 소득 보험료 부과 — 공단 국감 보고·복지부 "구체적으로 검토되거나 결정된 바 없음": https://economist.co.kr/article/view/ecn202611050022 · https://biz.sbs.co.kr/amp/article/20000344153
- S11 계산: calc.py → calc_out.txt (P-3 calc.py와 같은 식, 원 단위 반올림)

## 경쟁
- bench.md 참조. 6편 모두 2026년 기준만, 2027년 요율(건보 동결·장기요양 인상)로 다시 계산한 글 0편. 탈락 뒤 보험료는 '월 10만~20만원'(r_saeng) 어림이나 사례 한 사람 값

## 질문
1. 국민연금 2천만원 초과 시 건보료 부담 어느 정도 — https://kin.naver.com/qna/detail.naver?dirId=6100402&docId=495559838 (지식iN) → 답: c02(월 167만 약 6만 8천원, 200만 8만 1천원)
2. 피부양자 유지하려면 국민연금 수령액 조절 필요한가 — https://kin.naver.com/qna/detail.naver?dirId=6100401&docId=494829917 (지식iN) → 답: c03(올해처럼 2.1% 오르면 월 164만원부터 넘음, 권유 안 함)
3. 피부양자 탈락 시 경감률 — https://kin.naver.com/qna/detail.naver?dirId=6100401&docId=471610208 (지식iN) → 답: c04(2026년 8월분으로 끝)

## 왜
- 공적연금을 전부 세는 이유: 시행령 제41조①5호 문구, 정책 취지 문장은 원문에 없음(S2)
- 탈락 뒤 연금 절반만 보험료에 넣는 이유: 제44조②2호·③ 문구, 취지는 원문에 없음(S3)
- 2027년 건보료율 동결 이유: 브리핑은 국민 부담을 고려했다고 설명(S9) — 글에는 안 씀
- 2027년에 456원 오르는 이유: 장기요양률만 13.14%→13.90%(S8), 건보료율은 그대로(S9)

## 그래서
- 월 160만원대면 2027년 1월 인상률 발표 뒤 연 2천만원 넘는지 다시 셈(c03)
- 이자·배당 1천만원 근처면 공단 고객센터 1577-1000에 판정 기준 확인(c04)
- 탈락 통지 뒤 소득이 줄었으면 조정 신청(시행령 41조의2, P-3 대본 4장) — 글에는 안 넣음(분량)

## 누구라면
- 국민연금만 있고 재산 없는 사람: c02 표 그대로
- 연금저축·IRP 연금만 받는 사람: 소득에 안 셈(S7)
- 재산 과표 5.4억 넘는 사람·사업소득 있는 사람: 기준이 다름(S1)

## 함정
- '탈락해도 깎아 준다' — 2026년 8월분으로 끝(S3 부칙)
- 이자·배당 1천만원 넘으면 전부 들어감(S3 제44조①)
- 2027년 장기요양률 인상으로 같은 연금이어도 고지액이 조금 오름(S8)

## 우리만
- 2027년 요율(건보 7.19% 동결 + 장기요양 13.90%)로 월 167만원 다시 계산: 6만 8,382원, 2026년보다 456원 많음(calc_out) — 경쟁 6편 0편

## 예외
- 재산분 보험료 안 넣음 — 재산 있으면 더 큼
- 직장가입자로 일하면 다른 계산
- 이자·배당 1천만원 단서가 피부양자 판정에도 같은지 공단 문서 못 찾음(P-3 한계 그대로)

## 한계
- 분리과세 소득 부과는 보도(2차)로만 확인, 공단 국감 자료 원문은 확인 안 함 — 글은 '검토·결정한 것 없음'까지만
- 2027년 국민연금 인상률은 2027년 1월 발표라 모름 — '같은 비율로 오른다면'
- 2027년 지역 재산 점수당 금액은 계산에 안 씀(재산 0 가정)
- 고지 금액 원 단위 끝처리는 P-3 calc.py처럼 반올림 — 실제 고지서와 몇 원 다를 수 있음

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 한 해 소득 2천만원 이하, 한 달 166만원 조금 넘음 | 연 2천만원 이하 · 1,666,666원 | S1 https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566181&bylClsCd=110201 |
| 공적연금 전부 셈, 작년 연금으로 봄 | 제41조①5호 · ③ | S2 https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행령 |
| 연금저축·IRP 안 셈 | 사적연금 피부양자 소득 불포함 | S7 https://www.nhis.or.kr/static/alim/paper/oldpaper/202309/sub/section3_3.html |
| 연금 절반 × 7.19% | 100분의 50 · 1만분의 719 | S3 · S6 https://www.nhis.or.kr/nhis/together/wbhaea01000m01.do?mode=view&articleNo=11008009 |
| 167만 약 6만 8천 · 170만 6만 9천 · 180만 7만 3천 · 200만 8만 1천원 | 67,926 · 69,146 · 73,213 · 81,348(계산) | S4 https://www.mohw.go.kr/board.es?act=view&bid=0027&list_no=1487817&mid=a10503000000 · calc_out.txt |
| 10만원 늘어도 4천원쯤 · 10년 800만원 넘음 | 4,067 · 815만원(계산) | S4 https://www.mohw.go.kr/board.es?act=view&bid=0027&list_no=1487817&mid=a10503000000 · S11 calc_out.txt |
| 2027년 건보료율 7.19% 그대로(9월 8일) | "2027년도 건강보험료율은 올해와 동일한 7.19%를 유지" | S9 https://www.korea.kr/policy/civilView.do?newsId=156780681 |
| 장기요양 13.14% → 13.90%(10월 30일) | 2027년 소득 대비 0.9994%, 건강보험료의 13.90% | S8 https://www.mohw.go.kr/board.es?mid=a10503000000&bid=0027&list_no=1492396&act=view |
| 2027년 월 167만 6만 8,382원, 456원 많음 | 68,382 − 67,926 = 456(계산) | S8 · S9 · calc_out.txt |
| 2026년 2.1% 인상, 월 164만원부터 넘음 | 2.1% · 164만×1.021×12 = 2,009만(계산) | S5 https://mohw.go.kr/board.es?act=view&bid=0027&list_no=1488572&mid=a10503000000 |
| 2027년 연금은 2028년 판정에서 빠짐 | 제41조③ 연금은 전년도 소득 | S2 https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행령 |
| 분리과세 소득 부과, 복지부 검토·결정한 것 없음 (2차) | "구체적으로 검토되거나 결정된 바 없다" | S10 https://economist.co.kr/article/view/ecn202611050022 · https://biz.sbs.co.kr/amp/article/20000344153 |
| 2022년 9월 뒤 첫 탈락자 경감, 2026년 8월분으로 끝 | 부칙<제907호, 2022.9.1> 제3조 | S3 https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행규칙 |
| 이자·배당 1천만원 넘으면 전부 | 제44조① 단서 | S3 https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행규칙 |
| 재산 과표 5억 4천만원·9억원, 사업소득, 부부 | 별표 1의2 1.나·1.라·2.가 | S1 https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566181&bylClsCd=110201 |

# 올리기 전 확인
- 2026-11-11 23시(발행 전날, write) 대조 칸 출처 11곳 전부 다시 엶(curl, 모두 200 — raw/prepub_20261111.txt) · S8 본문 '13.90%' 그대로 · S9는 WebFetch로 '7.19%를 유지' 문장 읽음
- 다시 연 주소: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566181&bylClsCd=110201 · https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행령 · https://www.law.go.kr/LSW/lsInfoP.do?lsNm=국민건강보험법+시행규칙 · https://www.nhis.or.kr/static/alim/paper/oldpaper/202309/sub/section3_3.html · https://www.nhis.or.kr/nhis/together/wbhaea01000m01.do?mode=view&articleNo=11008009 · https://www.mohw.go.kr/board.es?act=view&bid=0027&list_no=1487817&mid=a10503000000 · https://www.mohw.go.kr/board.es?mid=a10503000000&bid=0027&list_no=1492396&act=view · https://mohw.go.kr/board.es?act=view&bid=0027&list_no=1488572&mid=a10503000000 · https://www.korea.kr/policy/civilView.do?newsId=156780681 · https://economist.co.kr/article/view/ecn202611050022 · https://biz.sbs.co.kr/amp/article/20000344153
- 기준일: 2026년 11월 11일
- 바뀐 것: 없음 — P-3 youtube-loop 11/11 00:49 확인과 같음(시행령 2026.10.1·시행규칙 2026.9.28 시행판, 보험료율 7.19%, 장기요양 2026년 13.14%·2027년 13.90%, 국민연금 2.1%)
- 새로 찾은 것: 2027년 건강보험료율 7.19% 동결(정책브리핑 2026.9.8) → 2027년 월 167만원 6만 8,382원(+456원)
- 조사 뒤 공표: 2027년 국민연금 인상률 2027년 1월(발행 뒤) · data/release_calendar.json 11/11~11/12 건보·연금 요율 관련 없음— 2027년 1월 인상률만 남음
