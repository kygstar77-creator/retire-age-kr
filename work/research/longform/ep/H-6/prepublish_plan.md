# H-6 올리기 전 확인 — 11/25 오전에 할 순서 (youtube-loop 2026-11-23 23:1x 준비)

공개 11/26 11:30 · 관문 기한 11/25 11:30 · research_gate.prepublish_check(days=1, strict) 기준.
이 파일은 계획뿐이다. 실제 기록은 11/25에 research.md 맨 끝 `# 올리기 전 확인` 칸에 쓴다(지금 쓰면 날짜가 11/23이라 11/25 gate에서 '1일 넘음'으로 다시 막힌다).
숫자는 바꾸지 않는다. 원문 값이 달라졌으면 '바뀐 것:'에 적고, 대본은 손대지 않은 채 순돌이·PD에 [알림](말 바꾸면 editor 재서명·PD 다시 받기가 끼어 기한을 넘긴다).

## 순서 (어림 40분, 11/25 08:00 시작 → 09:00 끝 목표)
1. 실거래 다시 받기(S1·S2) — calc.py와 같은 조건(강남구 11680, 매매 2025.10~2026.11 · 전월세 2025.10~2026.11)으로 국토부 API 새로 받아 raw/에 `_1125` 붙여 저장.
   - 볼 것: ① 2026-10 은마 매매가 11/19 받은 뒤 늦게 신고된 건(신고 기한 30일 → 10/31 계약분은 11/30까지 들어옴) ② 2026-11 은마 매매 새 건 ③ 해제(cdealDay) 새로 붙은 건 ④ 전월세 2026-10 건수(아직 기한 안 — 대본은 '10월 말일 쪽 계약은 아직 신고 기한 안'이라 말함, 바뀌어도 대본과 어긋나지 않음).
   - 대본 숫자(75건·9월 12·10월 23·84㎡ 가운데 34.30억·77㎡ 31.45억·43.10억·33.00억·전월세 164→31→20)와 대조해 같으면 '바뀐 것: 없음', 다르면 값과 차이를 적는다.
2. 강남구 원문 2곳 다시 열기 — S5 재초환 예정액 보도자료(1075588), S14 사업시행인가 보도자료(1075184). 정정·후속 게시 있는지.
3. 법령 7개 조문 현행 확인(S4·S17~S23) — law.go.kr 조문 주소 그대로 열어 시행일이 그대로인지(재초환법 시행 2025.10.1 · 도정법 2026.7.1). 11/20 뒤 개정·시행 새로 있으면 '바뀐 것:'.
4. 서울시·국토부 원문(S15/S31 같은 주소, S30, S33, S32) — 정보몽땅 은마 추진경과에 관리처분 신청·분양신청 재접수 같은 새 단계가 올라왔는지.
5. 2차 보도(S9~S13, S24 + S6~S8) — 주소 열림 확인만, 그리고 '새로 찾은 것:'을 위해 11/20~11/25 은마 새 기사 검색(분담금 확정·이주비·분양신청 재접수·재초환 이의신청). 새 사실은 적기만 하고 대본에 넣지 않는다.
6. 댓글 질문 — H-4(MRQqitzEgDw) 등 우리 부동산 롱폼 최근 댓글에 은마·재초환 질문 있는지(새로 찾은 것 후보).
7. research.md에 칸 쓰기 → `py -3.12 -c "import research_gate as g; print(g.prepublish_check('research/longform/ep/H-6/research.md', strict=True))"`(work에서) 빈 목록 확인 → today.md 완료 줄 + PD [알림].

## 칸에 반드시 들어갈 것 (strict 관문)
- 날짜: `2026-11-25` (확인한 날)
- 대조 칸 출처 주소 26개 전부(빠지면 막힘) — 아래 목록을 그대로 붙이고 줄마다 '열림/바뀜 없음' 또는 바뀐 내용.
- `바뀐 것:` 한 줄(없으면 '없음')
- `새로 찾은 것:` 한 줄(11/20 뒤 나온 은마 기사·발표·댓글 질문 1개 이상)
- `기준일:` 한 줄 — 예: '매매 실거래 2025-10~2026-10 계약분(2026-11-19 신고분 기준, 11/25 다시 받아 대조) · 전월세 2025-10~2026-09 계약분(11/19 신고분) · 재초환 예정액 2026-11-10 강남구 공표 · 법령 시행 2025-10-01(재초환법)·2026-07-01(도정법)'
- release_calendar 공표: 11/20~11/25 사이 이 편 낱말에 걸리는 공표 없음(11/23 research_gate.release_hits 실측 [] ) — 11/25에 다시 돌려 생기면 '바뀐 것:'에 적는다.

## 대조 칸 출처 주소 26개 (research_gate.source_urls 11/23 실측)
https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev
https://apis.data.go.kr/1613000/RTMSDataSvcAptRent
https://rt.molit.go.kr
https://www.law.go.kr/법령/부동산거래신고등에관한법률/제3조
https://www.gangnam.go.kr/board/B_000031/1075588/view.do
https://www.sidae.com/article/2026111013032293310
https://v.daum.net/v/20260521114137718
https://v.daum.net/v/20260530070229266
https://news.bizwatch.co.kr/article/real_estate/2026/09/24/0002
https://www.mt.co.kr/article/2026092914481837987
https://www.gangnam.go.kr/board/B_000031/1075184/view.do
https://news.seoul.go.kr/citybuild/archives/541084
https://www.law.go.kr/법령/재건축초과이익환수에관한법률/제8조
https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=277019&efYd=20251001&chrClsCd=010202&ancYnChk=0
https://www.law.go.kr/법령/재건축초과이익환수에관한법률/제12조
https://www.law.go.kr/법령/재건축초과이익환수에관한법률/제14조의2
https://www.law.go.kr/법령/재건축초과이익환수에관한법률/제17조의2
https://www.law.go.kr/법령/재건축초과이익환수에관한법률/제14조
https://www.law.go.kr/법령/재건축초과이익환수에관한법률/제15조
https://www.law.go.kr/법령/도시및주거환경정비법/제73조
https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=284065&efYd=20260701&chrClsCd=010202&ancYnChk=0
https://www.law.go.kr/법령/도시및주거환경정비법/제72조
https://v.daum.net/v/2S7nxy3Ghn
https://cleanup.seoul.go.kr
https://www.molit.go.kr/USR/NEWS/m_71/dtl.jsp?id=95092432
https://www.hub.go.kr
(관문 밖이지만 같이 열 2차: S6 https://supple.kr/news/cmw9vj6mhqp80al9p56d4b07r · S7 https://inews24.com/view/2024585 · S8 https://www.mt.co.kr/article/2026110614422041034)

## 11/23 확인한 loop 몫 나머지 (gate dry 막힘 중)
- toc 우리 목차 3장 이름: toc_compare.md 14:20 고침(4 세 가지 숙제(청구서)·5 세입자 계약 신고·7 함정과 직접 확인) → 11/23 23:1x toc_check [] · 15:12·15:17 gate log에도 안 나옴. 끝남.
- 이해 판정: understand_test.md 끝 줄 '판정: 통과'(copywriter 18:53, 제목·썸네일 3차) · ytlong 이해 검사 항목 전부 있음(11/23 23:1x 실측). 끝남. 15:17 gate log의 막힘은 그 앞 기록.
- bench_check '대조: 보류' 조건 둘(썸네일 3차·이해 판정) 다 풀림 → PD가 '대조: 통과' 줄 달 차례.
