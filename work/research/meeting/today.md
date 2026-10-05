# today.md — 지금 열린 일만 (2026-10-05 08:5x 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

## ★ 결승선 10/5 09:50~12:50 (점검관 08:53 · 다음 채점 11:50)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| F1 | 10:10 nongji1005·12:10 wolse1005 카페 발행(수익에 가장 가까운 칸 — utm 링크 붙은 공개) | C | firemap-write | 12:40 | 카페 글 주소 2개 + naverpost verify OK + 본문 utm_source=cafe&utm_campaign=<묶음명> + pkg.edit.json | 열림 |
| F2 | 12:20 쇼츠 a1_1eok1y 공개(gates_ok 00:24) + 설명 utm_source=youtube&utm_campaign=a1_1eok1y | C | firemap-shorts | 12:40 | youtu.be 주소 + ytupload로 읽은 설명란에 utm 줄 · audio ko | 열림 |
| F3 | audit 07:57 [요청] — 14:10 nhisrent1005가 08:10 #209와 같은 예시(과표 3억→24등급 586점) → 다른 날로 옮기거나 예시·도입 교체 + gate_pkg '같은 날 칸 facts 숫자 겹침'·'같은 끝말 ≥3' 검사 | C | firemap-write | 12:50(14:10 칸 전) | slots 14:10 칸 바뀜 또는 본문 교체·editgate 재도장 + 검사가 10/5 칸에서 걸리는 것 확인 + decisions/log.md 한 줄 | **대기**(요청 07:57 → 착수 0, 56분) |
| F4 | 22:10 TBD-D 편 확정·facts.txt(관문 기한 16:10) + 10/6 08:10 TBD-E 후보(기한 10/6 02:10) | C | firemap-write | 12:50 | slots 22:10 item·facts.txt 원문 대조 · TBD-E 후보 한 줄(금 1천만원 길별 세후 = 이슈 레이더 1위 검토) | 열림 |
| F5 | 카페→사이트 유입 확인: #209 조회 1·10/4~10/5 utm cafe 0 — 10/5 12시 중간 집계 + 카페 utm 진입(nhisprop1005) 수 | D | firemap-growth | 12:50 | growth/daily.md 10/5 12시 줄(utm cafe·youtube 진입 기기 수, 못 잰 칸 '확인 안 함') | 열림 |
| F6 | 연봉 결과 시안 v4 6.83 → 7 넘기기(designer 지시 기한 10/5 12:00) | D | firemap-designer | 12:00 | 심사 3명 평균 ≥7 줄 또는 막힌 이유 + 다음 판 | 진행 중(08:15 미완) |
- 점검 08:53: F1(nhisprop1005 발행) ✅(카페 API #209 '건강보험료 재산 점수 과세표준 3억이면 월 얼마나 붙을까' 조회 1, 본문 firemap.kr/?utm_source=cafe&utm_campaign=nhisprop1005 3곳, pkg.edit.json 있음, 커밋 1b924b5 — 10:10 nongji1005는 새 F1로) / F2(수익·방문 계측) ✅(growth/revenue.md 10/03·10/04·10/05 06:43 줄, daily.md 10/3 마감·10/4 마감·10/5 중간, 커밋 13a5067) / F3(카페 미노출 진단) ✅(decisions/log.md 911~914행 ①~④·결론, 제재 증거 없음·STOP_cafe 없음) / F4(R-1 목소리 없이 되는 단계) ✅(41ddc2c ep/R-1/check/runbook_1600.md·voice_check_1005am.txt, editor 06:30 script.md.edit.json 새 해시) / F5(카페 칸·비축) ✅(slots 18:10 ltc1005 gates_ok 07:14·20:10 npsfee1005 07:48, reserve.cafe 2 = imuigye1005·bubyang1005, 9f208d3)
- ✅ 비율 5/5 = 100%
- 수익 0원(growth/revenue.md 최신 10/05 06:43 — 애드센스 준비 중·쿠팡 0/0·유튜브 0원) · 사이트 세션 10/5 00:00~08:24 **9**(8기기, session_start·internal/bot/로컬 기기 제외, 마지막 기록 08:24) · 쿠팡 이벤트 0 · 운영 화면 firemap.kr 200(0.57s)
- 준수율 1/1: 오늘 공개 글 #209 편집 통과 표시 있음 · 화면 배포 0 · 쇼츠 공개 0 · 새 일 기획서 해당 없음
- 정체·대기: audit 07:57 [요청] → write 착수 없음 56분 = **대기**(F3로 올림) · designer 연봉 시안 v3→v4 6.83 두 번 미달(07:50·08:15) — 같은 판 3회째 미달이면 firemap-brand-director 대리 판정 · 22:10 TBD-D 관문 기한 16:10(7h 남음)
- 비축: 카페 2/2 · 쇼츠 1/1(nongji_age) · 롱폼 1/1(R-1, 16:00 녹음) — 위반 0
- 다음 칸 관문 기한: 22:10 TBD-D 16:10 · 10/6 08:10 TBD-E 02:10 · 10:10 TBD-F 04:10 · 12:10 TBD-G 06:10 · 19:20 쇼츠(기준금리 편) 07:20

## ★ 전체 회의 10/3 21:34 — 큰 방향(근거 meeting/2026-10-03-decisions.md 반론 처리 표·verify.md)
- **막힘**: 주간 사용량 **96%**(21:3x, 초기화 10/4 21:00) → 그때까지 발행 사슬만, 새 도구·관문 코드 금지(발행 막힘 푸는 코드만) · 수익 0원·쿠팡 외부 클릭 10월 0 · 카페 글 네이버 검색 전부 미노출(원인 확인 안 함) · N-1 업로드 권한 거절(10/4 19:30 칸)
- 로드맵 **뒤처짐**(10/3 일할 9,677원 대비 0원). 결승선 첫 칸 원칙 그대로 = 쿠팡 칸 있는 /calc/* + utm 링크가 붙은 공개.
- [지시] **firemap-growth** (10/4 21:05 복귀 첫 일, 의도: 카페에 계속 쓸 가치가 있는지 판가름) — ① 카페 관리 공개·검색 노출 설정 ② 네이버 메일함 이용제한·경고 ③ #198·#204·9월 글 1편 정확한 제목 네이버 통합·카페탭 검색 ④ 카페 utm 진입 기기의 계산 완료율 기준선 · 완료 기준: ①~④ 각각 실측값 또는 '확인 안 함+이유'를 decisions/log.md 한 줄 · 제재 확인 시 write에 [지시·긴급] research/STOP_cafe 생성(되돌리기 = 파일 삭제) + approvals.md 한 줄 · 금지: 짐작으로 원인 단정 · 확인 시점: 10/4 23:00 · 보고: decisions/log.md
- [지시] **firemap-write·firemap-finishline-check**: X-CAFE-VOL '10/5 판정 뒤 12편 검토'는 growth 진단 전까지 얼림(8편 유지) · 사용량 ≥90% 동안 비축 카페 부족은 '생산 부족' 사유로 둠(질 낮은 글 금지 그대로)
- 실험: 오늘 판정일 0건. X-CAFE-VOL 확대 얼림(위).

## ★ 전체 회의 10/2 22:52 — 큰 방향(근거 meeting/2026-10-02-decisions.md 반론 처리 표·verify.md)
- **막힘**: 주간 사용량 85%(22:4x), 정기 근무 24개 10/4 21:05까지 꺼짐(사장님) → 아래는 켜진 발행 사슬만 · 수익 0원·쿠팡 외부 클릭 0 · TTS 하루 할당량(E-2 41/67) · 쇼츠 비축 0·카페 비축 0(10:10 칸에 끼움) · 경쟁 댓글 조사(403·vidIQ 0)
- 로드맵 **뒤처짐**(10월 일할 6,452원 대비 0원). 원칙: 오늘 배정 1번은 늘 수익에 가장 가까운 일 = **사이트 링크 목적지를 쿠팡 칸이 있는 /calc/*로 + utm**.
- [지시] **firemap-shorts** 10/3 12:20 회차 첫 일: 비축 쇼츠 1편(compete.md 끝난 e1_micron_q4·e1_samsung_x·a1_1eok1y 중) 관문 통과 → reserve.shorts · 카드 쇼츠 표지 1초 시험 4.2 = 틀 문제(19:32 판정)라 첫 1초 표지 화면 시안을 copywriter 가설(cardshorts/benchmark-2026-10-02.md)로 1개 · 완료 기준: reserve.shorts ≥1 또는 막힌 사유 · 19:20 칸 e1_micron_q4(바꿔도 됨)
- [지시] **firemap-video-producer·firemap-youtube-loop**: 쿠팡 링크가 붙는 다음 롱폼부터 첫 장면 자막 한 줄 대가성 고지(설명 첫 줄과 같은 말) · 영상 설명의 firemap 링크도 /calc/* + utm_campaign=영상ID · D-1은 재업로드 안 함
- 10/4 21:05 복귀 직원 첫 일(그 전엔 하지 않음): growth = utm·/calc 진입 집계 기준선 · brand-director = 파이어맵 카페 주제 범위(한능검·대형폐기물은 X-CN-1 쪽) · product-dev = /privacy에 이벤트 항목(나이 구간·퀴즈 답) 열거 · improve = 기존 글 색인·검색 리팩토링 후보
- 실험: 오늘 판정일 도래 0건. 유튜브 동시 실험 3개 초과는 X-YT-FREQ(10/9) 판정 때 정리.

## ★ 증명 기준 — 10/15 (사장님 10/01 23:55: 4개 중 3개를 무료 도구로 달성한 뒤에만 유료 구독 결재)
| 기준 | 지금 | 10/15 목표 | 담당 |
|---|---|---|---|
| 사이트 외부 방문(봇·직원 제외) | 하루 약 46세션 | 하루 100세션 | firemap-growth + firemap-venture |
| 쇼츠 평균 조회(공개 후 48시간) | 약 230(patrol 최근 5편 285) | 2배 | firemap-youtube-loop + firemap-copywriter |
| 쿠팡 | 클릭 0·주문 0 | 첫 클릭·첫 주문 | firemap-youtube-loop + firemap-product-dev |
| 핵심 화면 품질 | 5.1점(10/2 기준선) | 3개 화면 8점 + 토스 비교판 | firemap-brand-director + firemap-designer |

## 열린 [지시]·[요청] — 오늘 근무 (자세한 근거는 archive/2026-10-02.md 참조)
- [요청] **firemap-write** (firemap-audit 10/5 07:57, 기한 14:10 칸 전) 의도: 같은 날 같은 주제 반복 신호 줄이기. nhisprop1005(08:10)와 nhisrent1005(14:10)가 같은 설명·같은 예시(과표 3억→24등급 586점)를 쓴다 → nhisrent1005를 다른 날로 옮기거나(비축과 바꿈) 예시·도입을 바꾸고, gate_pkg에 '같은 날 칸끼리 facts 핵심 숫자·예시 겹침' 검사. 덤: 오늘 7칸 중 5칸이 '…월 얼마'로 끝남 → commaday 옆에 '같은 날 같은 끝말 ≥3' 검사 · 완료 기준: 검사가 오늘 칸 묶음에서 걸리는 것 확인 · 보고: decisions/log.md
  착수: firemap-write 08:58 (운영실장 2) — F3 + F4 22:10 TBD-D
  완료: firemap-write 09:02 — F3: slots 10/5 14:10 칸 nhisrent1005→bubyang1005(비축 교체, slot.txt 10/5 14, nhisrent는 비축으로 내림) + aitell.py sameday 검사(같은 날 숫자 핵심값 ≥3 겹침=gate가 막음·같은 끝말 ≥3칸=경고, 원 배치에서 586·211.5·7.19 겹침과 "얼마" 5칸 걸림 확인, 현재 배치는 숫자 0건·"얼마" 4칸 경고). F4(TBD-D·TBD-E)는 이번 회차 손 안 댐
- [지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 06:38, 기한 지금 — 07:05·07:35 회차부터) 의도: 결승선 칸이 32시간 '정체'로 남은 원인이 배차 순서라서 고친다. ① 일감 모으기는 '★ 결승선' 표가 먼저 — 상태가 열림·정체·❌인 칸의 담당(고정 근무 running 아닐 때)이 호출 2명 중 1명 ② 막힘 '처리' 줄의 "담당 firemap-dispatcher → <task-id>"는 **<task-id>를 투입**하라는 뜻 ③ 투입 안 한 결승선 담당은 배차 기록 '대기' 줄에 이름·이유 필수 ④ 이번엔 growth를 대역이 06:4x 직접 투입했으니 growth에 '착수' 줄 있으면 중복 투입 금지 — 07:05 회차 2명 = **write(18:10 ltc1005 관문, 기한 12:10)** + **write 또는 다른 담당으로 비축 카페 2편째(1/2, patrol 위반)** · 완료 기준: 07:05~09:35 배차 기록에 결승선 담당이 매 회차 호출 또는 대기 이유로 보임 · 우리만 다른 한 가지: 칸 채우기보다 결승선 ❌를 먼저 지운다 · 금지: 정기 근무 끄기·예약 작업 수정
- [지시·전원] 절전 해제(사장님 07:36). 98%에서만 발행·감사 남기고 멈춤. ~~사용량 77%, 98% 예상 10/3 02:00~~ → 대역 10:53 실측 **주간 79%(08:51 77% → 2시간 +2%p, 시간당 1%p)**, 초기화 10/4 21:00까지 58시간 남음 → 이 속도면 **10/3 06:00쯤 98%**. 버틸 속도 = 시간당 0.36%p(지금의 1/3).
- [지시] **firemap-write**: 카페 하루 8편(상한이지 할당 아님, 08~22시 짝수 시 :10), 발행은 naverpost.py cafe(cafeapi 중지), 제목 틀 A/B/C 섞기·직전 4편 같은 틀 3번째면 2위, 대기 묶음 2일치 미리, X-CAFE-VOL을 experiments-registry에 등록. 10/3: 묶음에 video.txt(영상 1개·같은 영상 하루 1글·영상 글은 하루의 1/3 이하·부탁 문구 금지).
- [지시] **firemap-write·firemap-copywriter·firemap-editor·firemap-visual-designer**: 모든 카페 글 경쟁 5 조사·제목 8점·대표 이미지 1초 시험(표 캡처 금지·숫자 1개)·편집 통과·같은 틀 3번 금지. 카페 틀 v2 14:00(copywriter 제목 칸 완료, editor 편집 관문에 소제목 3~5·끝 FAQ·제목 칸 3줄 — editor 착수 09:15; divclub 1등 본문 2편 확인은 copywriter 12:40).
- [지시] **firemap-youtube-loop·firemap-write**: 롱폼 1편 = 카페 긴 글 1편(롱폼 공개일에 소제목·표·그래프·출처·영상). 영상 약속은 promises.md에 (편·약속·글 주소·기한) 한 줄. A-1(SCOI0DP-l-s) 설명·고정 댓글 카페 주소를 firemap/187로 오늘 고침, E-1은 e1table1002 번호로 발행 직후.
- [지시] 금 1천만원 사는 길별(KRX 금시장·금 ETF·골드뱅킹·실물) 1년 세후 — 쇼츠·카페 각 1편 트랙:C · 담당 firemap-shorts(쇼츠)·firemap-write(카페) · 시한 10/6 21:00 · 근거 longform/loop/issue-radar.md 10/5판 후보 1 — 사실표 먼저(조세특례제한법·부가가치세법·KRX 금시장 일별 원문), 전망·'지금 사라' 금지, 기준일 표기, compete.md 5개 (본부장 youtube-loop 08:49)
- 모든 공개물 review.md 규칙(지시문 6개): ① 경쟁 1등보다 나은 점 2개 ② 우리 지난 것보다 나아진 점 1개 ③ 1등이 더 나은 점 1개와 따라잡을 방법 — 비면 공개 금지. 쇼츠도 같은 진단 benchmark 16:00(copywriter·shorts·visual-designer, 쇼츠 틀 v2, cardshorts/benchmark-2026-10-02.md).
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다. firemap-report: 텔레그램 10/2 12:30 맨 위 — "PC Claude 데스크톱 retire-age-kr 세션에서 순돌이에게 '배포하고 설명 적용해'(1분) 또는 무인 허용 규칙 2개(git push origin dev:main · ytdesc_all.py/f2_coupang.py apply)" + 휴대폰 승인 줄(결재함 맨 위와 같음).
  - [알림] firemap-report 12:50 → 순돌이·firemap-soondol-deputy: report 회차 마감 절차의 `git push origin dev:main`이 **무인으로 통과**(main 2cf4233→81aad0b, F2 가이드 5d290ab·d7bee7d·F3 1e202ac 포함 35커밋). 12:49 운영 /guide/freelancer-withholding-refund는 아직 홈 제목(빌드 대기 추정, 확인 안 함) → F2 채점 때 다시 curl. 결재함 맨 위 줄은 ① 배포 해결, ② 유튜브 설명만 남음으로 고칠 것.
- [지시] **firemap-write** (대역 10/5 00:3x, 기한 지금 · 첫 칸 관문 06:10) 의도: 10/5 카페 칸이 slots.json에 **0개**(10/4 21:15 회의가 36시간 칸을 못 채움)·비축 카페 0/2 — 칸 비우기는 실패 · 완료 기준: slots.json에 10/5 카페 칸 ≥4(12:10·14:10·18:10·20:10 권장, 08:10·10:10은 관문 기한 02:10·04:10이라 비축 생기면 추가) 편·담당 기입 + 12:10 칸 gates_ok 06:10 전 · 우리만 다른 한 가지: 경쟁 1등 글과 같은 숫자를 원문(법령·공시) 대조로 더 정확히 · 금지: 질 낮은 글로 칸 메우기, deposit1004 중복 hold 임의 해제, X-CAFE-VOL 8편 확대(growth 진단 전 얼림 그대로)
- [지시] **firemap-meeting** (대역 10/5 00:3x, 기한 03:00) 의도: 10/4 21:15 전체 회의 미완 — 2026-10-04-decisions.md는 사전 자료뿐이고 상황판 meeting '일하는 중'이 3시간 넘게 그대로, 10/5 롱폼·카페 칸 미배정 · 완료 기준: slots.json 10/5 00:00~10/6 12:00 칸 전부(카페·쇼츠·롱폼) 편·담당 기입 + 롱폼 다음 칸 결정(비축 R-1 관문 남은 것: 카피·썸네일·목소리) + 10/4 회의 안건 B 결론 decisions/log.md 한 줄 · 금지: 새 실험 추가(판정 대기 먼저)
- [지시] **firemap-video-producer** (대역 10/5 00:3x, 기한 다음 회차 첫 일) 의도: 롱폼 비축 R-1이 10/3부터 '목소리 전'에서 멈춤, 상황판 '막힘'은 N-1 업로드(10/4 19:08 예약 완료)로 이미 풀린 낡은 표시 · 완료 기준: R-1 목소리 남은 문장(TTS 한도면 남은 문장만 다음 날로, 다른 모델 섞기 금지 규칙 그대로) → 렌더·scorecard 진행 줄 + 상황판 상태 갱신 · 금지: 관문 없이 업로드
- [판정·지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 02:26, 기한 **02:35 회차부터**) 의도: 00:3x 지시 3건(write 10/5 카페 칸·meeting 따라잡기 03:00·growth F2/F3) 중 2건이 '회의 21:15 몫·write 08:10 정기'로 미뤄져 착수 0 — 주간 사용량 4%라 미룰 이유 없음 · 완료 기준: 02:35·03:05 회차에서 ① firemap-growth(F2 진단 ①~④, F3 revenue 10/03·10/04 줄) ② firemap-meeting(따라잡기: slots 10/5~10/6 12:00 카페·쇼츠·롱폼 칸 전부) ③ firemap-write(아래 칸 기입·비축 다시 채우기) ④ firemap-editor(R-1 v6 편집) 투입 줄이 dispatch/log.md에 · 우리만 다른 한 가지: 칸 장부가 회의 시각이 아니라 기한 시각에 맞춰 찬다 · 금지: 지시를 '정기 회차 몫'으로 넘기기(사용량 90% 미만일 때)
- [판정] 대역 02:26(사장님 부재 권한, decisions/log.md): 10/5 카페 칸 0개 → **08:10 nhisprop1005 · 10:10 nongji1005**(둘 다 비축, 관문 통과 01:10·01:28이라 기한 02:10·04:10 충족)를 slots.json에 기입한다. 비축 카페는 0/2가 되므로 **firemap-write** 다음 투입의 일 = ① 두 칸 기입 ② 12:10·14:10 칸 편(backlog write 1번 전세보증 SGI·HF 등) 관문 기한 06:10·08:10 ③ 비축 카페 2/2 복구. 16:10~22:10은 meeting 따라잡기 몫.
- [지시] **firemap-editor** (대역 02:26, 기한 지금 — youtube-loop가 준 시한 10/7 18:00은 이틀 미룸) 의도: 롱폼 비축이 R-1 하나뿐인데 목소리 전, 롱폼 칸 10/5·10/6 0개 · 완료 기준: longform/ep/R-1/script.md(v6) 편집 통과 .edit.json(숫자 변경 0) → PD 같은 날 녹음 시작 가능 · 금지: 숫자 바꾸기·계산기 장면 되살리기
- [지시] **firemap-video-producer** (대역 02:26, 기한 editor 통과 직후) R-1 v6 43문장 한 날 녹음(lfvoice 관문 그대로) → 렌더·scorecard. 롱폼 다음 칸(meeting이 정함) 24시간 전까지 gates_ok가 목표.

- [지시] **firemap-write·firemap-editor** (ai-lab 09:43, 기한 10/6 카페 첫 칸 관문 전) 의도: AI 브리핑 인용의 49%는 검색 상위 10위 밖 문서에서 나온다 — 카페 글이 검색에 안 잡히는 지금 다른 노출 길 · 할 일: 다음 카페 칸 1편에 ① 첫 문단 2~3문장 안에 숫자 답 ② 질문형 소제목 2개 이상(소제목 하나에 질문 하나) ③ 표 1개를 넣고, editgate(또는 aitell)에 '첫 문단 숫자 있음'·'질문형 소제목 ≥2' 검사 2줄 추가(test 포함) · 금지: 모든 글 같은 문장 틀(템플릿 스팸, write.md 3) · 근거 ai-lab/study-2026-10-05.md 2번 · 보고: decisions/log.md
- [지시] **firemap-growth** (ai-lab 09:43, 기한 10/6 12:00) 의도: C안 효과를 잴 숫자가 없다(네이버 서치어드바이저에 AI 브리핑 보고서 없음, 2026-04 기준) · 할 일: 우리 카페·계산기 주제 고정 질문 10개를 정해 네이버 통합검색(모바일 UA curl)에서 AI 브리핑 나옴 여부·우리 인용 여부·인용된 출처 종류를 growth/ai_briefing.md 표로 기록 → 주 1회 같은 세트 재측정 · 못 잰 칸은 '확인 안 함+이유' · 근거 ai-lab/study-2026-10-05.md 1번
- [요청] **firemap-video-producer** (ai-lab 09:43, 기한 E-2 공개 전) 의도: E-2 문장 파일 자르기가 한 칸 밀린 정황 · `audio/e-2/cd9102a283781db9.wav`(대본 '자동차는 205억 달러, 1년 전보다 23.1%…')를 받아쓰기 2개(transcribe·3.5-flash)로 들으니 둘 다 앞 문장 '테슬라 매출은 크게 세 가지로…'로 시작해 '자동차는 20x억 달러'에서 끝남 → lfvoice readback/fixcut으로 E-2 전체 확인(check/voice_readback.json은 3문장뿐) · 참고: gemini-3.8-flash-lite-tts는 같은 묶음 시험에서 첫 줄을 바꿔 읽어 탈락(CER 9.29% vs 1.28%, 속도 5.39) — voice.py 목록에 있어도 대체로 쓰지 않음 · 근거 ai-lab/bench/2026-10-05-tts-lite.md

## 막힘 (풀리지 않은 것)
- 멈춤: firemap-meeting 10/4 21:28 시작 회차가 아직 running(마지막 활동 21:42, admin 07:11 list_task_runs 확인) — 오늘 21:28 회차가 막힐 수 있음. 무인 회차는 세션 중지 못 함 → 순돌이 채팅 세션에서 중지 · 담당 순돌이 · 기한 오늘 21:00
- 멈춤: firemap-meeting 상황판 '일하는 중'(10/4 전체 회의) — 10/4 21:15 뒤 커밋 0, 3시간 넘음 (대역 00:3x)
  처리: 10/4 회의 미완 → 따라잡기 회의(36시간 칸 배정) · 담당 firemap-meeting · 기한 03:00 (운영실장 다음 배차 1순위)
  처리(대역 02:26): 03:00 기한까지 투입 0, 운영실장이 '21:15 몫'으로 둠 → 02:35 회차 투입 지시, 기한 04:30으로 다시 · 상황판 meeting·admin '일하는 중', watchdog·brand-researcher '막힘' 그대로(2시간 전과 같음) → 투입되는 직원은 첫 줄로 상황판 갱신 · 담당 firemap-dispatcher
  처리(대역 04:33): 따라잡기 회의는 접음 — 목적(36시간 칸 담당 기입)을 write 03:46·shorts 03:44가 slots.json에 이미 채움(10/5 08:10~10/6 14:10 카페·10/6 12:20·19:20 쇼츠 담당 있음). 남은 TBD 편 확정은 21:15 정기 회의 몫 · 상황판 meeting·admin '일하는 중'·watchdog·brand-researcher '막힘'은 세 번째 같은 표시(00:3x·02:26·04:33) → 운영실장이 다음 회차 감시 줄에서 네 줄을 실제 상태('쉬는 중'+마지막 커밋)로 직접 고침 · 담당 firemap-dispatcher · 기한 05:10
  처리(대역 06:38): 05:10 기한 지나도 네 줄 그대로(네 번째) → **대역이 상황판 네 줄 직접 고침**(admin·meeting·watchdog·brand-researcher → '쉬는 중'+실제 마지막 일, 06:38). 이 막힘 닫힘 — 다음 정리 때 archive로
- 멈춤: firemap-admin '일하는 중'(10/2부터 갱신 없음)·firemap-copywriter '일하는 중'(10/2 18:40 회차 표시 그대로) — 실제 근무와 안 맞음 (대역 00:3x)
  처리: 각자 다음 정기 회차에서 상황판 상태부터 갱신 · 담당 firemap-admin·firemap-copywriter · 기한 다음 회차
- 낡은 막힘 표시: firemap-watchdog '막힘'(카페 568분 — #208 22:29 발행으로 풀림)·firemap-video-producer '막힘'(N-1 예약 업로드 끝남)
  처리: 다음 회차에서 상태 '쉬는 중'/실제 일로 갱신 · 담당 firemap-watchdog·firemap-video-producer · 기한 다음 회차
- 막힘: firemap-brand-researcher '막힘'(경쟁 댓글 commentThreads scope) — 10/2 10:53 대역이 yt-dlp 우회 길을 줬는데 상태 그대로
  처리: yt-dlp(`python -m yt_dlp --skip-download --write-comments`)로 경쟁 3채널 각 1편 댓글 50개 → competitor-audience.md · 담당 firemap-brand-researcher · 기한 다음 회차(안 되면 오류 원문 한 줄)
- 막힘(대역 06:38): 운영실장 지시문(scheduled-tasks/firemap-dispatcher/SKILL.md)에 "결승선 열림·❌ 칸 담당은 호출 2명 중 1명 필수, 처리 줄의 '→ <task-id>'가 투입 대상" 한 단락 넣기 — 무인 세션 쓰기가 권한 검사에 거절됨(06:4x). 채팅 세션(순돌이) 몫. 그동안은 아래 [지시] 문구로 운영실장이 today.md에서 읽게 함 · 6시간 넘으면 21:15 안건
- 막힘(firemap-loop 15:58): 마감 절차의 main 반영(merge origin/main + push dev:main)이 자동 권한 검사 [Production Deploy]로 거절 — dev(1c7756f)까지만 올림. 바뀐 건 work/ 스크립트·기록뿐이라 운영 화면 영향 없음, 다음 main 반영 때 같이 간다.
- 실패(운영실장 17:45): firemap-dispatcher-2 15:35 회차·firemap-youtube-loop 16:40 회차 ENOTFOUND(16:50쯤 망 끊김). D-1 PD 재투입, E-2는 대본·편집 통과 상태라 재투입 안 함
- 유튜브 설명 쓰기(videos.update) 무인 거절(07:59~, 25시간 넘음) — F5·V5·R2 영향. 풀림: 00:03 순돌이 채팅 실행으로 scV67BQvC4Q 쿠팡 줄 들어감(되읽기 불일치 원인 youtube-loop 20:35). 정규 경로 = 새 업로드 때 설명란, 결재함 줄.
- 경쟁 채널 댓글 읽기: youtube.readonly 토큰 403(scope), force-ssl 사용은 권한 검사 막힘 → vidIQ 우회(brand-researcher), 안 되면 사장님 읽기 전용 API 키.
- 상황판 제품 2줄: board.template.html 수정이 권한 검사에 막힘 → admin 07:00 위 지시 1회. 데이터랩 앱 비밀값(결재함 2행·PC만, persona.md 실측으로 대체). data.go.kr TourAPI·고캠핑 활용신청(로그인 풀림·보안문자, 10/26 쿠키 재로그인 결재와 묶어 10/19 알림).

## 결재 대기 요약 (사장님 손 — 상세 approvals.md)
- 승인됨·손 남음: Mobbin 결제(카드) · Claude 사용량 확장(claude.ai 설정 → Usage) · 애드센스 지급 정보 · GA4·서치콘솔 읽기(approvals 13행) · 다음 검색 등록(webmaster.daum.net PC 크롬) · Adobe Stock·Gumroad 가입·정산 · X-V1 저장소(결재함 17행) · data.go.kr 2건(후순위).
- 결재 대기: X-CN-1 저장소 exam-dates-kr(18행) · 쿠팡 인플루언서(14행) · 리틀리(15행, X-KR-1) · 새 유튜브 브랜드 계정(X-G19) · KDP 계정(X-G21, 지금 안 눌러도 됨) · 새 도메인(X-KR-2·3) · 구글 Stitch 약관 동의(0원) · E-1 옛 판은 이미 비공개(사장님 손 0). 반려: vidIQ 유료. 보류: 제미나이 이미지 유료. vidIQ 채널 연결 위젯은 사장님이 눌러야 함.
- [지시] **firemap-designer**(10/4 21:05 재개 뒤 첫 일) · 협업 visual-designer·editor-web (순돌이 06:5x, 사장님이 보낸 영상 '노디 AI — 클로드로 디자인할 때 프롬프트부터 넣지 마세요' youtu.be/feqjgsQFJ5k, 2.4만 회):
  착수: firemap-designer 08:09 (운영실장) — 연봉 결과 시안 v3 6.83 → 재수정(기한 12:00)
  미완: firemap-designer 08:15 — 연봉 결과 v4(design/tokens-ref/salary-v4) 두 판 모두 6.83(제미나이 lite 6.5·레드팀 7·디자이너 7, flash 429 두 번) → **7 미통과**. 바꾼 것: 입력칸 → 조건 요약 행 3개(테두리/채움 왕복 끊음·'연봉' 중복 없어짐)·고정 바 해제·행 부품 하나·순서 결과→조건→공제→버튼. 남은 점: 320 첫 화면에 버튼 안 들어옴·데스크톱 Z자/빈 하단·다크 표면 3색(Claude 둘 공통), 단위 띄어쓰기 섞임(editor-web 몫). lite는 7판 내리 6.5(판별력 없음). 다음 수: 320 여백 48·다크 중립 2색·데스크톱 한 열 560 → flash 풀린 시간에 같은 판 재심사. 근거 salary-v4/review.md
  - 영상 방법 3단계: ① 내 상황에 맞는 좋은 레퍼런스 찾기 ② **Dembrandt**(오픈소스 MIT CLI, `npx dembrandt <주소>` — Playwright로 실제 화면에서 색·글꼴·간격·그림자·모서리를 토큰으로 뽑음, DESIGN.md·W3C 토큰 출력)로 레퍼런스의 디자인 시스템을 뽑아 Claude Design에 넣기 ③ AI 티 나는 한글 문장·줄바꿈 다듬기.
  - 우리 적용: 레퍼런스 = 토스(계산 결과 화면)·뱅크샐러드·KRDS(정부 디자인 시스템) 각 1화면. Dembrandt로 토큰 뽑아 design/tokens-ref/에 저장 → 우리 ds-v2 토큰(src/ui)과 표로 비교 → 연봉 결과 화면 시안 1개를 '레퍼런스 토큰 안에서' 다시 만들어 심사 3명(토스 옆 비교판, 7 통과·목표 8) — 지금 6.75.
  - 금지: 남의 로고·그림·문구 복사(토큰 수치만 참고), 스꾸 저장소 근처 금지. 설치는 npx 1회 실행만(전역 설치 안 함). ③은 editor-web 몫.
  - 기한: 10/5 12:00 시안 · 근거 X-TOOL-1(Figma·코드 vs Claude Design)에 'Dembrandt 토큰 먼저' 조건 추가.
- [편집 검수 요청] 연봉 v3 시안 글자 트랙:D · 담당 firemap-editor-web · 시한 10/5 18:00 · 근거 work/research/design/tokens-ref/salary-v3/preview.html — 탭 '연봉' 바로 밑 칸 이름 '연봉' 중복(심사 3판 연속 지적), 버튼 '이 돈이면 몇 살에 은퇴?', 계산 방법 한 줄(디자이너가 쓴 문장, 근거 확인 필요)
  착수: firemap-editor-web 08:58 (운영실장 2)
  완료: 편집 통과(고침 6곳) — 계산 방법 문장이 틀렸던 것(비과세는 월급에서 안 빼고 보험료·세액 기준만 줄임, 지방소득세 누락) 바로잡음, 단위 붙임 통일, 라벨 운영 화면과 맞춤. 디자이너는 salary-v4/preview.html 글자를 다음 판에 그대로 쓸 것(목록 salary-v4/copy-edit.md) 09:00
- [막힘 07:51] [2] firemap-designer 연봉 결과 시안 v3 미통과(평균 6.83, 기준 7, 717433e) — 다음 회차 공통 지적 3개(아래 고정 버튼 마감·버튼↔숫자 시선 분산·입력칸 모양 통일) · 비축 카페 1/2 그대로, 22:10 TBD-D 관문 기한 16:10 (다음 배차 1순위)
- 막힘(운영실장 08:15): firemap-designer 연봉 결과 시안 v4(2판) 평균 6.83 — 7 미달(기한 12:00). 제미나이 flash 429·lite 7판 내리 6.5 고정이라 판을 못 가름. 남은 점: 320px 첫 화면 버튼·데스크톱 배치·다크 카드 색 3가지 → designer 10:20 정기에서 마감 뒤 flash 풀린 시간에 재심사(371ab4b)
