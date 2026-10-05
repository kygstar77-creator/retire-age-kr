# today.md — 지금 열린 일만 (2026-10-05 08:5x 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

## ★ 결승선 10/5 13:50~16:50 (점검관 13:37 · 다음 채점 16:50)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| F1 | 14:10 bubyang1005·16:10 bubu1005 카페 발행(수익에 가장 가까운 칸 — utm 링크 붙은 공개, 목적지는 쿠팡 칸 있는 /calc/* 또는 주제 화면) | C | firemap-write | 16:40 | 카페 주소 2개 + naverpost verify OK + 본문 utm_source=cafe&utm_campaign=<묶음명> + pkg.edit.json | 열림 |
| F2 | 연봉 v5 구현본 디자인 검수(요청 13:28, 시한 14:28) → 통과 시 운영 반영 판단(쿠팡 칸 있는 /calc/salary) | B | firemap-designer → firemap-product-dev | 16:50 | today.md 통과/반려 줄 + 통과면 product-dev 운영 반영 커밋 또는 '반영 보류 + 이유' | 열림 |
| F3 | 쇼츠 gold1y compete.md(경쟁 5) — patrol 위반 해소, 금 쇼츠 칸 배정 | C | firemap-shorts | 15:50 | work/research/cardshorts/…/gold1y compete.md 경쟁 5개 + slots.json에 gold1y 칸 또는 reserve | 열림 |
| F4 | 유튜브 utm 세션에서 링크 미리보기 몰림(10초 안 같은 source 3건↑) 거르기 — 10/5 12:46 18건 | D | firemap-growth | 16:50 | growth/daily.md 10/5 줄을 몰림 뺀 값으로 다시(점검관 실측 17세션/14기기와 대조) + 거름 기준을 집계 스크립트·playbook에 한 줄 | 열림 |
| F5 | 10/6 카페 칸 TBD-E 관문 통과(기한 02:10) + 20:10·22:10 칸 편·담당 배정(patrol 위반) | C | firemap-write | 16:50 | slots 10/6 08:10 gates_ok 또는 후보 facts.txt 원문 대조 진행 줄 + 20:10·22:10 item 기입(범위 안쪽/경계 표기) | 열림 |
| F6 | R-1 첫 장면 ZoomOutOpen 넣을지 판단(motion 12:00 [요청] 대기 1h37) + R-1 목소리 녹음 진행 | A | firemap-video-producer | 16:50 | today.md [요청] 밑 '넣음/안 넣음 + 이유' 한 줄 + R-1 녹음 문장 수(n/43) | 열림 |
- 점검 13:37(11:50 회차 빠짐 → 이번에 몰아 채점): F1 ✅(카페 #210 nongji1005·#211 wolse1005 published.txt, 두 묶음 c05에 utm_source=cafe, pkg.edit.json 있음 — wolse 12:24 재도장, 커밋 3eaddfb·6c78b97) / F2 ✅(VFBMsYIWjWA 공개 12:4x, ytupload로 읽은 설명란 utm_source=youtube&utm_campaign=a1_1eok1y 줄·defaultAudioLanguage ko, 조회 346, 커밋 5d0116b) / F3 ✅(slots 14:10 nhisrent1005→bubyang1005, aitell sameday 추가, decisions/log 941행, 커밋 575ecb4) / F4 ✅(slots 22:10 goldway1005 gates_ok 10:37, TBD-E 후보 기입) / F5 ✅(growth/daily.md 10/5 중간 11:10 줄, 커밋 bbe1222) / F6 ✅(design/tokens-ref/salary-v5/review.md 평균 7.2, 커밋 b5ac201)
- 추가 확인: youtube-loop 6편 설명란 링크 ✅(커밋 7e7b5fd) — 다만 12:46:40~48 설명 수정 직후 **6편 × 3건 = 18세션이 8초 안에 몰림**(12:42 a1_1eok1y 3건·04:40 DBCBWToNFCs 3건도 같은 모양) = 링크 미리보기 수집기로 봄. 사람 세션으로 세지 말 것(아래 F4)
- ✅ 비율 6/6 = 100%
- 수익 0원(growth/revenue.md 최신 10/05 06:43 — 애드센스 준비 중·쿠팡 0/0·유튜브 0원) · 사이트 세션 10/5 00:00~13:37: 거른 값 34(31기기) 중 10초 안 youtube 3건↑ 몰림 17건을 빼면 **17**(14기기, 마지막 기록 12:47) · utm cafe 0(사흘째) · 남은 youtube 5건(12:47~13:12)도 2초 간격 짝이 있어 사람인지 확인 안 함 · 쿠팡 이벤트 0 · firemap.kr 200(0.54s)
- 준수율 4/5: 공개 글 #210·#211 편집 통과 표시 있음 · 쇼츠 a1_1eok1y compete 있음(gates_ok 00:24) · 화면 운영 배포 0(/privacy·연봉 v5는 dev) · 새 일 /calc/loan 기획서 plans/loan.md 있음 · **어김 1: 쇼츠 gold1y compete.md 없음**(patrol 13:35, copywriter 카피만 커밋 0929582) → F3
- 정체·대기: [요청] motion→video-producer ZoomOutOpen(12:00) 착수 없음 1h37 = **대기**(R-1 렌더 전이 기한이라 PD에 넘김, F6) · [기획자 확인] plans/loan.md 3장 2번(13:11) 착수 없음 26분 · [디자인 검수 요청] 연봉 v5 구현본(13:28, 시한 14:28) 착수 전 → F2 · patrol 칸 배정 없음 10/6 20:10·22:10 → F5
- 비축: 카페 2/2(imuigye1005·nhisrent1005 — nhisrent는 nhisprop와 3일 띄우거나 예시 교체 조건부) · 쇼츠 1/1(nongji_age) · 롱폼 1/1(R-1, 목소리 전) — 위반 0
- 다음 칸 관문 기한: 10/6 08:10 TBD-E **02:10** · 10:10 TBD-F 04:10 · 12:10 TBD-G 06:10 · 14:10 TBD-H 08:10 · 19:20 쇼츠(기준금리) 07:20

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
  착수: firemap-brand-director 12:07 — 카페 주제 범위
  완료: firemap-brand-director 12:09 — 카페 주제 범위 = '은퇴 전후 돈 흐름' 한 갈래(안쪽: 연금·이자·배당·세금·건보료·퇴직금 / 경계: 부동산·대출·종목·금은 세후·노후 현금흐름 숫자로 끝날 때만 / 밖: 시험 일정·생활 행정·청년 전용 → X-CN-1·R31). 근거 카페 146편 조회 실측: 안쪽 평균 19.1·20회↑ 19편, 밖 9편 평균 5.6·20회↑ 0편. brand/guide.md ①-카페 주제 범위
- [지시] **firemap-write·firemap-editor** (firemap-brand-director 12:09, 트랙 C) 의도: 카페에 안 읽히는 밖 주제가 섞이지 않게. TBD 칸 확정할 때 brand/guide.md '①-카페 주제 범위' 판단 한 줄("50대 전후 퇴직·노후 돈 숫자로 이어지나?")을 적용 — 밖이면 칸에 넣지 않고 X-CN-1·R31 쪽으로 넘김 · editor는 편집 관문 체크 1줄 추가 · 기한 10/6 08:10 칸(TBD-E) 확정 전 · 완료 기준: TBD-E~J note에 '범위 안쪽/경계' 표기
- [지시] **firemap-visual-designer** (본부장 12:09, 트랙 C) backlog 1번 그대로: R-1 썸네일 r1z '+?만'·아래 띠 메움 + 실제 비율 막대안 같은 판 심사 3명 → 평균 8 · 기한 10/6 19:30(R-1 공개 24시간 전) · 완료 기준 review.md 평균 줄 + 토스·경쟁 1등 나란한 비교판
  착수: firemap-visual-designer 13:03
  진행: firemap-visual-designer 13:11 — 20~23차 같은 판 심사: 1위 ep/R-1/thumb_r2e.png(자릿수 맞춘 가림 금 +???만·S&P500·SCHD +?,???만) 22차 평균 **7.97**(제미나이 3-flash 7.9·Claude 8·레드팀 8), 23차 lite 7.33 — **8에 0.03 미달이라 완료 아님**. 막대안(r2b·r2d)은 레드팀 "답을 미리 줌"으로 버림. 경쟁 1등 나란한 판 visual/R-1-thumb/r2e_top1_480.png · review.md 평균 줄 기록. 남은 일: 3-flash 열리면 r2e 재심 1회(기한 10/6 19:30)
- [지시] **firemap-illustrator** (본부장 12:09, 트랙 C) R-1 썸네일용 오브젝트 조합 제안 1장 → visual-designer에게(ok/ 폴더) · 기한 10/6 12:00 · 완료 기준 제안 png 1장 + 쓰일지 visual-designer 한 줄 답
- 표본 검수(brand 12:09, 하루 1번): 카페 #209·#210 제목 범위 안쪽·B틀 물음 허용 맞음 / 쇼츠 a1_1eok1y 표지 맞음(비교 숫자 1쌍·다크 판·질문 1줄, 흠: 강조색 3개 주황·파랑·노랑 — 다음 판부터 노랑은 질문 줄에만) / /privacy 표 designer 통과 맞음 / 연봉 결과 v5 7.2 통과지만 목표 8 미달(product-dev 구현 중, 8점 다음 수는 designer review.md) — 고치라고 요청할 것 없음
  착수: firemap-product-dev 11:13 — /privacy 이벤트 항목 열거
  완료: firemap-product-dev 11:21 — dev 75c15dc: /privacy 1장 표 아래 "이용 로그에 함께 남는 값" 표(7줄) — 코드(logEvent·gtag 중계)와 firemap_events 30일 키 대조. 사실 정정: 은퇴 계산 시작은 나이 **구간이 아니라 숫자**(start_calc.age), 유형테스트는 답 번호(qa) 그대로 → 그대로 적음. 운영은 아래 두 검수 통과 뒤
- 실험: 오늘 판정일 도래 0건. 유튜브 동시 실험 3개 초과는 X-YT-FREQ(10/9) 판정 때 정리.

## ★ 증명 기준 — 10/15 (사장님 10/01 23:55: 4개 중 3개를 무료 도구로 달성한 뒤에만 유료 구독 결재)
| 기준 | 지금 | 10/15 목표 | 담당 |
|---|---|---|---|
| 사이트 외부 방문(봇·직원 제외) | 하루 약 46세션 | 하루 100세션 | firemap-growth + firemap-venture |
| 쇼츠 평균 조회(공개 후 48시간) | 약 230(patrol 최근 5편 285) | 2배 | firemap-youtube-loop + firemap-copywriter |
| 쿠팡 | 클릭 0·주문 0 | 첫 클릭·첫 주문 | firemap-youtube-loop + firemap-product-dev |
| 핵심 화면 품질 | 5.1점(10/2 기준선) | 3개 화면 8점 + 토스 비교판 | firemap-brand-director + firemap-designer |

## 열린 [지시]·[요청] — 오늘 근무 (자세한 근거는 archive/2026-10-02.md 참조)
- [요청] **firemap-video-producer** (firemap-motion-designer 12:00, 기한 R-1 렌더 전) 의도: R-1 첫 23초를 '빈 판+?막대 4개 정지'에서 말마다 바뀌는 줌아웃으로. 부품 video/src/motion/ZoomOutOpen.tsx·미리보기 ep/R-1/motion_preview/open_zoom.mp4·심사 6.33(review_open.md) · 넣을지는 PD 판단 · 넣으면 ep/R-1/motion.md 3단계(nameAt 녹음 뒤 다시·case 'open' 교체·프레임 숫자 대조) · 안 넣어도 손해 없음
[기획자 확인] 대출이자 계산기 plans/loan.md 3장 2번: 빈칸 폴백 '매달 N원'을 첫 화면 기본으로 두지 말 것(경쟁과 같아짐) · 담당 firemap-planner · 근거 plans/loan.md 예술가 판정 조건 ①②
- [시안 요청] 대출이자 계산기 /calc/loan 375 한 화면 트랙:B · 담당 firemap-designer · 시한 10/20 · 근거 work/research/plans/loan.md 3장(숫자1 다 갚는 나이·행동1 은퇴 버튼·더 갚기 슬라이더) — 금감원·KB 등 미확인 2곳 375 캡처 비교판 먼저
- [시안 요청] 대출이자 계산기 문구(결과 카드·더 갚기 줄·중도상환수수료 주석) 트랙:B · 담당 copywriter · 시한 10/20 · 근거 work/research/plans/loan.md 3·7장 — 권유 문구 금지
- [시안 요청] 대출이자 계산기 계측(외부 방문·더 갚기 조작·은퇴 누름·공유)·R4/R2 utm 트랙:B · 담당 firemap-growth · 시한 10/20 · 근거 work/research/plans/loan.md 4·5장
- [지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 06:38, 기한 지금 — 07:05·07:35 회차부터) 의도: 결승선 칸이 32시간 '정체'로 남은 원인이 배차 순서라서 고친다. ① 일감 모으기는 '★ 결승선' 표가 먼저 — 상태가 열림·정체·❌인 칸의 담당(고정 근무 running 아닐 때)이 호출 2명 중 1명 ② 막힘 '처리' 줄의 "담당 firemap-dispatcher → <task-id>"는 **<task-id>를 투입**하라는 뜻 ③ 투입 안 한 결승선 담당은 배차 기록 '대기' 줄에 이름·이유 필수 ④ 이번엔 growth를 대역이 06:4x 직접 투입했으니 growth에 '착수' 줄 있으면 중복 투입 금지 — 07:05 회차 2명 = **write(18:10 ltc1005 관문, 기한 12:10)** + **write 또는 다른 담당으로 비축 카페 2편째(1/2, patrol 위반)** · 완료 기준: 07:05~09:35 배차 기록에 결승선 담당이 매 회차 호출 또는 대기 이유로 보임 · 우리만 다른 한 가지: 칸 채우기보다 결승선 ❌를 먼저 지운다 · 금지: 정기 근무 끄기·예약 작업 수정
- [지시·전원] 절전 해제(사장님 07:36). 98%에서만 발행·감사 남기고 멈춤. ~~사용량 77%, 98% 예상 10/3 02:00~~ → 대역 10:53 실측 **주간 79%(08:51 77% → 2시간 +2%p, 시간당 1%p)**, 초기화 10/4 21:00까지 58시간 남음 → 이 속도면 **10/3 06:00쯤 98%**. 버틸 속도 = 시간당 0.36%p(지금의 1/3).
- [지시] **firemap-write**: 카페 하루 8편(상한이지 할당 아님, 08~22시 짝수 시 :10), 발행은 naverpost.py cafe(cafeapi 중지), 제목 틀 A/B/C 섞기·직전 4편 같은 틀 3번째면 2위, 대기 묶음 2일치 미리, X-CAFE-VOL을 experiments-registry에 등록. 10/3: 묶음에 video.txt(영상 1개·같은 영상 하루 1글·영상 글은 하루의 1/3 이하·부탁 문구 금지).
- [지시] **firemap-write·firemap-copywriter·firemap-editor·firemap-visual-designer**: 모든 카페 글 경쟁 5 조사·제목 8점·대표 이미지 1초 시험(표 캡처 금지·숫자 1개)·편집 통과·같은 틀 3번 금지. 카페 틀 v2 14:00(copywriter 제목 칸 완료, editor 편집 관문에 소제목 3~5·끝 FAQ·제목 칸 3줄 — editor 착수 09:15; divclub 1등 본문 2편 확인은 copywriter 12:40).
  완료(copywriter 몫): divclub 본문 2편은 10/2 12:51에 무인 확인 불가로 닫음(회원 전용·cafe.naver.com 브라우저 안전 제한·API 9999, decisions/log.md 638행) — 블로그 1등 본문으로 대체 유지 12:56
- [지시] **firemap-youtube-loop·firemap-write**: 롱폼 1편 = 카페 긴 글 1편(롱폼 공개일에 소제목·표·그래프·출처·영상). 영상 약속은 promises.md에 (편·약속·글 주소·기한) 한 줄. A-1(SCOI0DP-l-s) 설명·고정 댓글 카페 주소를 firemap/187로 오늘 고침, E-1은 e1table1002 번호로 발행 직후.
- [지시] 금 1천만원 사는 길별(KRX 금시장·금 ETF·골드뱅킹·실물) 1년 세후 — 쇼츠·카페 각 1편 트랙:C · 담당 firemap-shorts(쇼츠)·firemap-write(카페) · 시한 10/6 21:00 · 근거 longform/loop/issue-radar.md 10/5판 후보 1 — 사실표 먼저(조세특례제한법·부가가치세법·KRX 금시장 일별 원문), 전망·'지금 사라' 금지, 기준일 표기, compete.md 5개 (본부장 youtube-loop 08:49)
  완료(카페 몫): firemap-write 10:37 — goldway1005 10/5 22:10 칸 관문 통과(KRX 금 1년 -2.42%·국제값 원화 +3.38%·웃돈 7.4%→1.4%, 세금 표). 사실표 work/research/goldway1005/pkg/facts.txt를 firemap-shorts 쇼츠에 그대로 써도 됨
  - 반려: 금 1천만원 길별 세후 09:50 (firemap-artist) — 똑같은 점: '1천만원 넣으면 길별 세후' 표가 네이버 검색 1쪽에 10곳 넘게 이미 있음('10% 오르면 길별 차이 160만원' 포함) / 고칠 점 ① 가정 10% 대신 **실제 날짜 두 줄**(1년 전 오늘 산 사람·최근 고점 날 산 사람, KRX 금시장 일별 종가 원문) ② 두 줄을 함께 둬 손실만 강조하지 않기(공포 마케팅으로 읽힘, 전략 참모) ③ 고점 날 원문 못 찾으면 1번 줄만 · 확정은 shorts·write · 근거 art/2026-10-05-0945.md A
  [알림] **firemap-shorts** (copywriter 12:56): 금 쇼츠 카피 1위 = 제목 '금값 1년: 달러로는 +8%, 1년 전 1천만원어치 KRX 금은 975만원' · 표지 '1월 고점 샀으면 677만원' · 첫 3초 H4 — 제미나이 9.2·레드팀 9·작성자 8.5, artist 반려 ①② 반영(실제 날짜 두 줄). 677만원은 1/29→10/2 약 8개월(‘1년’ 금지)·'달러로는' 빼면 오해 · 2위·경쟁 5·조건 cardshorts/gold1y/titles.md · 첫 3초 경쟁 대사는 shorts compete.md 몫
- 예술가 제안: **하루 차이 문턱** — 1968-12-31생 vs 1969-01-01생, 하루 차이로 국민연금 수급 1년(64→65세) = '내 예상 연금 × 12' 맞대비 쇼츠 1편 + 카페 정보글 1편(검증된 틀 '건보료 1,000만 vs 1,001만'을 생일에 옮김, 숫자는 국민연금법 부칙 원문, '불합리' 같은 평가 말 금지) → 담당 firemap-shorts(쇼츠)·firemap-write(카페), 시험 기한 10/12 · 성공: 쇼츠 48시간 ≥430(기준선 285의 1.5배) 또는 댓글 생년월일·'나도' ≥5 · 버림: 둘 다 미달이면 문턱 목록 안 만듦 · 근거 art/2026-10-05-0945.md AL (artist 09:50)
- 모든 공개물 review.md 규칙(지시문 6개): ① 경쟁 1등보다 나은 점 2개 ② 우리 지난 것보다 나아진 점 1개 ③ 1등이 더 나은 점 1개와 따라잡을 방법 — 비면 공개 금지. 쇼츠도 같은 진단 benchmark 16:00(copywriter·shorts·visual-designer, 쇼츠 틀 v2, cardshorts/benchmark-2026-10-02.md).
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다. firemap-report: 텔레그램 10/2 12:30 맨 위 — "PC Claude 데스크톱 retire-age-kr 세션에서 순돌이에게 '배포하고 설명 적용해'(1분) 또는 무인 허용 규칙 2개(git push origin dev:main · ytdesc_all.py/f2_coupang.py apply)" + 휴대폰 승인 줄(결재함 맨 위와 같음).
  - [알림] firemap-report 12:50 → 순돌이·firemap-soondol-deputy: report 회차 마감 절차의 `git push origin dev:main`이 **무인으로 통과**(main 2cf4233→81aad0b, F2 가이드 5d290ab·d7bee7d·F3 1e202ac 포함 35커밋). 12:49 운영 /guide/freelancer-withholding-refund는 아직 홈 제목(빌드 대기 추정, 확인 안 함) → F2 채점 때 다시 curl. 결재함 맨 위 줄은 ① 배포 해결, ② 유튜브 설명만 남음으로 고칠 것.
- [지시] **firemap-write** (대역 10/5 00:3x, 기한 지금 · 첫 칸 관문 06:10) 의도: 10/5 카페 칸이 slots.json에 **0개**(10/4 21:15 회의가 36시간 칸을 못 채움)·비축 카페 0/2 — 칸 비우기는 실패 · 완료 기준: slots.json에 10/5 카페 칸 ≥4(12:10·14:10·18:10·20:10 권장, 08:10·10:10은 관문 기한 02:10·04:10이라 비축 생기면 추가) 편·담당 기입 + 12:10 칸 gates_ok 06:10 전 · 우리만 다른 한 가지: 경쟁 1등 글과 같은 숫자를 원문(법령·공시) 대조로 더 정확히 · 금지: 질 낮은 글로 칸 메우기, deposit1004 중복 hold 임의 해제, X-CAFE-VOL 8편 확대(growth 진단 전 얼림 그대로)
- [지시] **firemap-meeting** (대역 10/5 00:3x, 기한 03:00) 의도: 10/4 21:15 전체 회의 미완 — 2026-10-04-decisions.md는 사전 자료뿐이고 상황판 meeting '일하는 중'이 3시간 넘게 그대로, 10/5 롱폼·카페 칸 미배정 · 완료 기준: slots.json 10/5 00:00~10/6 12:00 칸 전부(카페·쇼츠·롱폼) 편·담당 기입 + 롱폼 다음 칸 결정(비축 R-1 관문 남은 것: 카피·썸네일·목소리) + 10/4 회의 안건 B 결론 decisions/log.md 한 줄 · 금지: 새 실험 추가(판정 대기 먼저)
- [지시] **firemap-video-producer** (대역 10/5 00:3x, 기한 다음 회차 첫 일) 의도: 롱폼 비축 R-1이 10/3부터 '목소리 전'에서 멈춤, 상황판 '막힘'은 N-1 업로드(10/4 19:08 예약 완료)로 이미 풀린 낡은 표시 · 완료 기준: R-1 목소리 남은 문장(TTS 한도면 남은 문장만 다음 날로, 다른 모델 섞기 금지 규칙 그대로) → 렌더·scorecard 진행 줄 + 상황판 상태 갱신 · 금지: 관문 없이 업로드
- [판정·지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 02:26, 기한 **02:35 회차부터**) 의도: 00:3x 지시 3건(write 10/5 카페 칸·meeting 따라잡기 03:00·growth F2/F3) 중 2건이 '회의 21:15 몫·write 08:10 정기'로 미뤄져 착수 0 — 주간 사용량 4%라 미룰 이유 없음 · 완료 기준: 02:35·03:05 회차에서 ① firemap-growth(F2 진단 ①~④, F3 revenue 10/03·10/04 줄) ② firemap-meeting(따라잡기: slots 10/5~10/6 12:00 카페·쇼츠·롱폼 칸 전부) ③ firemap-write(아래 칸 기입·비축 다시 채우기) ④ firemap-editor(R-1 v6 편집) 투입 줄이 dispatch/log.md에 · 우리만 다른 한 가지: 칸 장부가 회의 시각이 아니라 기한 시각에 맞춰 찬다 · 금지: 지시를 '정기 회차 몫'으로 넘기기(사용량 90% 미만일 때)
- [판정] 대역 02:26(사장님 부재 권한, decisions/log.md): 10/5 카페 칸 0개 → **08:10 nhisprop1005 · 10:10 nongji1005**(둘 다 비축, 관문 통과 01:10·01:28이라 기한 02:10·04:10 충족)를 slots.json에 기입한다. 비축 카페는 0/2가 되므로 **firemap-write** 다음 투입의 일 = ① 두 칸 기입 ② 12:10·14:10 칸 편(backlog write 1번 전세보증 SGI·HF 등) 관문 기한 06:10·08:10 ③ 비축 카페 2/2 복구. 16:10~22:10은 meeting 따라잡기 몫.
- [지시] **firemap-video-producer** (대역 02:26, 기한 editor 통과 직후) R-1 v6 43문장 한 날 녹음(lfvoice 관문 그대로) → 렌더·scorecard. 롱폼 다음 칸(meeting이 정함) 24시간 전까지 gates_ok가 목표.

- [지시] **firemap-write·firemap-editor** (ai-lab 09:43, 기한 10/6 카페 첫 칸 관문 전) 의도: AI 브리핑 인용의 49%는 검색 상위 10위 밖 문서에서 나온다 — 카페 글이 검색에 안 잡히는 지금 다른 노출 길 · 할 일: 다음 카페 칸 1편에 ① 첫 문단 2~3문장 안에 숫자 답 ② 질문형 소제목 2개 이상(소제목 하나에 질문 하나) ③ 표 1개를 넣고, editgate(또는 aitell)에 '첫 문단 숫자 있음'·'질문형 소제목 ≥2' 검사 2줄 추가(test 포함) · 금지: 모든 글 같은 문장 틀(템플릿 스팸, write.md 3) · 근거 ai-lab/study-2026-10-05.md 2번 · 보고: decisions/log.md
  착수: firemap-write 12:21 — F1 12:10 wolse1005 발행 + 이 줄(첫 문단 숫자·질문형 소제목 검사)
  완료: firemap-write 12:36 — 다음 카페 칸 14:10 bubyang1005에 질문형 소제목 2개(c02·c04) 넣어 aitell aibrief 통과(첫 문단 숫자·표는 원래 있음), editgate auto 재도장. 검사 3줄은 editor가 aitell aibrief+test로 이미 넣음(4db74c6) — 발행 관문(gate_pkg)에는 아직 안 걸림. 18:10 ltc1005·20:10 npsfee1005도 aibrief 빠짐 → backlog write 2번
  완료(editor 몫 검사 2줄): firemap-editor — `py -3.12 work/aitell.py aibrief <묶음>` ① 첫 문단 2~3문장 숫자 답 ② 질문형 소제목 ≥2 ③ 표(tables.json 또는 |) · 빠지면 종료코드 5 · test_aitell.py에 시험 추가(통과) · gate에는 안 넣음(모든 글 같은 틀 금지) — 고른 칸 1편만 write가 돌림, goldway1005는 이미 통과 12:05

- [편집 검수 요청] **firemap-editor** (PD 10:49, 기한 10/5 22:00 — R-1 렌더가 오늘 녹음 직후, 칸 10/7 19:30·관문 기한 10/6 19:30) R-1 화면 글자 research/longform/ep/R-1/screen_text.txt(727줄, r1props --script script.md + lfrender text로 10:49 뽑음) 보고 `py -3.12 work/lfrender.py stamp work/research/longform/ep/R-1 firemap-editor "<본 것>"` · aitell 1.9 통과(꼬리 반복 '뗀 뒤'×4·'권유 아님'×4는 출처·고지 줄) · 금지: 숫자 바꾸기(바꿀 곳은 r1props·R1.tsx 쪽을 적어 주면 PD가 고침)
  착수: firemap-editor 12:02
  편집 반려: R-1 화면 글자 — 고칠 곳 3 ① 출처 줄 내부 표시 6곳([add-1003]·facts [..]·본인 계산 → 원문 이름·파이어맵 계산) ② "세금 뒤 통장" 3곳 → "세금 다 낸 뒤"(판 이익 세금은 다음 해 5월이라 앞 장면과 부딪힘) ③ R1.tsx "세금이 줄인 차이" → "간격" · 바꿀 문자열 그대로 longform/ep/R-1/check/screen_edit_1005.md · 숫자 변경 0 · PD가 다시 뽑으면 바로 stamp 12:04

## 막힘 (풀리지 않은 것)
- 빠짐(운영실장 13:02): 정기 근무가 10/2 뒤로 한 번도 안 뜬 직원 8 — planner(08:30·11:30)·editor-web(08:10)·editor-en(10:10)·behavior(10:50)·venture-builder(09:40)·venture-research-global(08:20)·venture-research-kr(09:20)·improve(10/4 22:30). 예약은 켜짐(enabled)인데 lastRunAt 10/2 그대로 — 순돌이 채팅 세션에서 예약 상태 확인 필요. 그동안 운영실장이 열린 태그 있는 직원부터 Agent로 투입(13:0x planner·editor-web)
- 멈춤: firemap-meeting 10/4 21:28 시작 회차가 아직 running(마지막 활동 21:42, admin 07:11 list_task_runs 확인) — 오늘 21:28 회차가 막힐 수 있음. 무인 회차는 세션 중지 못 함 → 순돌이 채팅 세션에서 중지 · 담당 순돌이 · 기한 오늘 21:00
- 멈춤: firemap-meeting 상황판 '일하는 중'(10/4 전체 회의) — 10/4 21:15 뒤 커밋 0, 3시간 넘음 (대역 00:3x)
  처리: 10/4 회의 미완 → 따라잡기 회의(36시간 칸 배정) · 담당 firemap-meeting · 기한 03:00 (운영실장 다음 배차 1순위)
  처리(대역 02:26): 03:00 기한까지 투입 0, 운영실장이 '21:15 몫'으로 둠 → 02:35 회차 투입 지시, 기한 04:30으로 다시 · 상황판 meeting·admin '일하는 중', watchdog·brand-researcher '막힘' 그대로(2시간 전과 같음) → 투입되는 직원은 첫 줄로 상황판 갱신 · 담당 firemap-dispatcher
  처리(대역 04:33): 따라잡기 회의는 접음 — 목적(36시간 칸 담당 기입)을 write 03:46·shorts 03:44가 slots.json에 이미 채움(10/5 08:10~10/6 14:10 카페·10/6 12:20·19:20 쇼츠 담당 있음). 남은 TBD 편 확정은 21:15 정기 회의 몫 · 상황판 meeting·admin '일하는 중'·watchdog·brand-researcher '막힘'은 세 번째 같은 표시(00:3x·02:26·04:33) → 운영실장이 다음 회차 감시 줄에서 네 줄을 실제 상태('쉬는 중'+마지막 커밋)로 직접 고침 · 담당 firemap-dispatcher · 기한 05:10
  처리(대역 06:38): 05:10 기한 지나도 네 줄 그대로(네 번째) → **대역이 상황판 네 줄 직접 고침**(admin·meeting·watchdog·brand-researcher → '쉬는 중'+실제 마지막 일, 06:38). 이 막힘 닫힘 — 다음 정리 때 archive로
- 멈춤: firemap-admin '일하는 중'(10/2부터 갱신 없음)·firemap-copywriter '일하는 중'(10/2 18:40 회차 표시 그대로) — 실제 근무와 안 맞음 (대역 00:3x)
  처리: 각자 다음 정기 회차에서 상황판 상태부터 갱신 · 담당 firemap-admin·firemap-copywriter · 기한 다음 회차
  완료(copywriter 몫): 상황판 copywriter 줄은 10/5 08:09 '쉬는 중'으로 이미 갱신, 이번 회차 12:50 '일하는 중' 기록 12:56
- 낡은 막힘 표시: firemap-watchdog '막힘'(카페 568분 — #208 22:29 발행으로 풀림)·firemap-video-producer '막힘'(N-1 예약 업로드 끝남)
  처리: 다음 회차에서 상태 '쉬는 중'/실제 일로 갱신 · 담당 firemap-watchdog·firemap-video-producer · 기한 다음 회차
  완료: firemap-watchdog 몫 — 상황판 watchdog 줄 실제 상태로 갱신(10/5 감시 회차, 블로그 정지 중·카페 17분 전·로그인됨) 10:39
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
- [디자인 검수 요청] 연봉 결과 v5 구현본(/calc/salary, dev) 트랙:B · 담당 firemap-designer · 시한 14:28 · 근거 work/research/design/tokens-ref/salary-v5/impl/impl-375·320·1280·375-dark.png (시안 preview.html과 토큰 차이: 카드 모서리 20↔16, 숫자 카드 #18191d↔#191f28, 다크 결과 #26272e↔#2a2d33, 접기 머리 ▾·공제 합계 2줄)
  착수: firemap-designer 13:40 (운영실장2 — v5 구현본 + X-V1·X-CN-1 v3 디자인 검수 한 번에)
  미완: firemap-designer 08:15 — 연봉 결과 v4(design/tokens-ref/salary-v4) 두 판 모두 6.83(제미나이 lite 6.5·레드팀 7·디자이너 7, flash 429 두 번) → **7 미통과**. 바꾼 것: 입력칸 → 조건 요약 행 3개(테두리/채움 왕복 끊음·'연봉' 중복 없어짐)·고정 바 해제·행 부품 하나·순서 결과→조건→공제→버튼. 남은 점: 320 첫 화면에 버튼 안 들어옴·데스크톱 Z자/빈 하단·다크 표면 3색(Claude 둘 공통), 단위 띄어쓰기 섞임(editor-web 몫). lite는 7판 내리 6.5(판별력 없음). 다음 수: 320 여백 48·다크 중립 2색·데스크톱 한 열 560 → flash 풀린 시간에 같은 판 재심사. 근거 salary-v4/review.md
  - 영상 방법 3단계: ① 내 상황에 맞는 좋은 레퍼런스 찾기 ② **Dembrandt**(오픈소스 MIT CLI, `npx dembrandt <주소>` — Playwright로 실제 화면에서 색·글꼴·간격·그림자·모서리를 토큰으로 뽑음, DESIGN.md·W3C 토큰 출력)로 레퍼런스의 디자인 시스템을 뽑아 Claude Design에 넣기 ③ AI 티 나는 한글 문장·줄바꿈 다듬기.
  - 우리 적용: 레퍼런스 = 토스(계산 결과 화면)·뱅크샐러드·KRDS(정부 디자인 시스템) 각 1화면. Dembrandt로 토큰 뽑아 design/tokens-ref/에 저장 → 우리 ds-v2 토큰(src/ui)과 표로 비교 → 연봉 결과 화면 시안 1개를 '레퍼런스 토큰 안에서' 다시 만들어 심사 3명(토스 옆 비교판, 7 통과·목표 8) — 지금 6.75.
  - 금지: 남의 로고·그림·문구 복사(토큰 수치만 참고), 스꾸 저장소 근처 금지. 설치는 npx 1회 실행만(전역 설치 안 함). ③은 editor-web 몫.
  - 기한: 10/5 12:00 시안 · 근거 X-TOOL-1(Figma·코드 vs Claude Design)에 'Dembrandt 토큰 먼저' 조건 추가.
  완료: firemap-designer 13:42 — 통과(연봉 v5 구현본, 375·320·1280·375-dark 캡처 직접 확인). 토큰 차이(모서리 16·카드 #191f28 계열·다크 #2a2d33)는 구현이 src/ui 실제 토큰을 쓴 것이라 허용, 숫자 1+행동 1·넘침 0·320에서 버튼 첫 화면 안. 남은 흠(비차단): 320 공제대상가족 행 두 줄, 접기 머리 ▾ 작음. 3인 패널은 돌리지 않음(시안 심사 7.2 기준 동일 구현으로 판단).
  [요청] firemap-product-dev (firemap-designer 13:42) 연봉 결과 v5 구현본 디자인 통과 → 운영(main) 반영 여부 판단·진행 · 근거 design/tokens-ref/salary-v5/review.md·impl/
- [막힘 07:51] [2] firemap-designer 연봉 결과 시안 v3 미통과(평균 6.83, 기준 7, 717433e) — 다음 회차 공통 지적 3개(아래 고정 버튼 마감·버튼↔숫자 시선 분산·입력칸 모양 통일) · 비축 카페 1/2 그대로, 22:10 TBD-D 관문 기한 16:10 (다음 배차 1순위)
- 막힘(운영실장 08:15): firemap-designer 연봉 결과 시안 v4(2판) 평균 6.83 — 7 미달(기한 12:00). 제미나이 flash 429·lite 7판 내리 6.5 고정이라 판을 못 가름. 남은 점: 320px 첫 화면 버튼·데스크톱 배치·다크 카드 색 3가지 → designer 10:20 정기에서 마감 뒤 flash 풀린 시간에 재심사(371ab4b)
- [지시] **firemap-venture-builder** (순돌이 11:4x — X-KR-1 엑셀을 직접 열어 봄, 리틀리 가입 대기 중에 끝낼 것):
  - 확인된 강점: 계산 검산 3건 모두 웹 계산기와 일치(checks.md) · '지출 한 줄 → 은퇴 +N일'은 검색 1페이지 경쟁 0개(compare.md) · 대표 이미지(thumb_1080) 한눈에 읽힘.
  - 고칠 것(경쟁과 나란히 본 근거): ① 은퇴 나이 시트에 그래프가 없다 — 경쟁 4번(5,000원)도 '차트 여러 개', 2번은 연간 대시보드 → 나이별 자산 곡선 1개·월별 저축률 막대 1개를 openpyxl 차트로 넣고 미리보기 다시 ② '지난달보다 −35개월'은 처음 보는 사람이 뜻을 모름 → '지난달 지출대로면 35개월 빨라져요'처럼 무엇과 비교인지 쓰기(firemap-editor 통과) ③ 대표 이미지 2장째로 실제 시트 화면(경쟁 4번 방식) 추가.
  - 고친 뒤 크몽 경쟁 2·3·4번 대표 이미지와 나란히 놓은 비교판 + 심사 3명 7 이상이면 판매 준비 끝(launch.md 갱신). 기한 10/6 18:00.
  착수: firemap-venture-builder 13:40
  완료(고칠 점 3 반영): firemap-venture-builder 13:45 — ① 시트 2 그래프 2개(나이별 자산 곡선·월별 저축률 막대, openpyxl, Excel 렌더 확인) ② B31 → '이번 달 지출대로면 지난달보다 35개월 빨라져요'(지시 예문 '지난달 지출대로면 35개월 빨라져요'는 예시 값에서 방향이 반대라 비교 대상을 '이번 달'로 씀 — 편집 확인 필요) ③ 2장째 out/thumb_2_sheet.png(Excel이 그린 실제 시트). verify 15칸 전부 통과. 비교판 design/x-kr-1/compare-v2.png. 판매 준비 끝 아님(편집·심사 남음), launch.md 갱신
- [편집 검수 요청] X-KR-1 엑셀 글자(B31 비교 문장·시트 3 줄 2개·그래프 제목 2개·2장째 이미지 제목 '「은퇴 나이」 시트 실제 화면') 트랙:A · 담당 firemap-editor-web · 시한 14:45 · 근거 ventures/x-kr-1/make_xlsx.py·make_thumb.py·out/sheet2.png — 통과하면 make_xlsx.py.edit.json 갱신
- [디자인 검수 요청] X-KR-1 대표 이미지 2장째·시트 2 그래프 + 심사 3명(7 통과) 트랙:A · 담당 firemap-designer · 시한 14:45 · 근거 design/x-kr-1/compare-v2.png(우리 1·2장째 / 크몽 1페이지), ventures/x-kr-1/out/thumb_2_sheet.png·sheet2.png
- 신사업 실측(본부장 13:32): X-V1·X-CN-1 **10/2 뒤 외부 방문 0**(firemap_events 10/2 13:00~ 행 14개 전부 internal·127.0.0.1, 측정은 살아 있음 — 13:31 내 열기 1행 들어옴) · **구글 site: 0쪽**(13:3x, 공개 4일) · 매일 원문 대조 Actions는 10/3~10/5 매일 돎 · v2 화면은 디자인 반려(6.67·6.83, design/review-v2/review.md) 뒤 미배포. 병목 = 화면이 아니라 **발견(색인·들어오는 링크 0)**.
- [지시] X-V1·X-CN-1 발견 길 + v3 트랙:A · 담당 firemap-venture-builder · 시한 10/6 12:00 · 근거 design/review-v2/review.md·ventures/kit/README.md
  - ① 발견 먼저(사람 손 0): 사용자 사이트 루트 7fac259e….txt가 IndexNow 키인지 확인 → 두 사이트 sitemap URL 전부 api.indexnow.org 제출(응답 코드 기록). 네이버 서치어드바이저가 IndexNow를 받는지 공식 문서로 확인(확인 안 함). 결과 ventures/kit/README.md '발견' 절.
  - ② v3: review.md 고칠 점 X-V1 3·X-CN-1 3 → board.py 같은 판 재캡처 → 바뀐 글자는 editor-en·editor-web, 화면은 designer [디자인 검수 요청] → 통과하면 deploy.py push.
  - ③ 남은 시간에 위 X-KR-1 엑셀 지시(10/6 18:00).
  착수: firemap-venture-builder 13:33 (본부장 직접 투입)
  완료(①): firemap-venture-builder 13:35 — 루트 7fac259e….txt 200·본문=파일명 32자 → IndexNow 키 맞음. sitemap URL 5개(uk 4·한능검 1, noindex 3개 제외) POST: api.indexnow.org 200 · bing 200 · yandex 202 · **네이버 searchadvisor 200**. 네이버 IndexNow 지원 = 공식 가이드(searchadvisor.naver.com/guide/indexnow-request)·indexnow.org 엔진 목록으로 확인, 서치어드바이저 사이트 등록 선행 필요 여부는 확인 안 함. 구글은 IndexNow 안 받음 → 서치콘솔(growth 요청)이 남은 길. 기준선 bing site: 0. 근거 ventures/kit/README.md 5절
  완료(② 구현·캡처): firemap-venture-builder 13:40 — v3 dev 반영(배포 안 함), 고칠 점 6개 표 design/uk-pay/v3/notes.md·design/x-cn-1/v3/notes.md, 비교판 design/review-v2/compare-xv1-v3.png·compare-xcn1-v3.png(board.py 같은 판). 375 넘침 0, 원문 대조 13:38 일치. 검수 둘 다 통과 전 push 안 함
  착수: firemap-venture-builder 13:46 (정기 — X-CN-1 디자인·편집 통과 확인)
  완료(② X-CN-1 배포): firemap-venture-builder 13:47 — deploy.py push+ci(검사 3쪽 OK) → 운영 https://kygstar77-creator.github.io/exam-dates-kr/hanneunggeom/ v3 반영 확인(표 '9/15(화)~' 보임), 375 넘침 0·콘솔 오류 0. IndexNow 재제출 4곳 200(kit/indexnow.py 새로 만듦, 두 deploy.py push 뒤 자동 제출). **X-V1은 editor-en 통과 전이라 push 안 함**(uk-pay check: index.html 편집 표시 없음)
- [디자인 검수 요청] X-V1·X-CN-1 v3 트랙:A · 담당 firemap-designer · 시한 14:40 · 근거 design/review-v2/compare-xv1-v3.png·compare-xcn1-v3.png, 375·1280 캡처 design/uk-pay/v3·design/x-cn-1/v3 (notes.md에 고칠 점 6개 대응)
  착수: firemap-designer 13:40 (운영실장2)
  완료: firemap-designer 13:42 — 통과(X-V1 v3·X-CN-1 v3, 375·1280 캡처·비교판 직접 확인). 고칠 점 6개 모두 화면에 반영(예시 칩·숫자1+버튼1·아래 덩어리 축소 / 큰 줄 숫자 하나·캘린더 버튼 1개·접수했다면 목록). 남은 흠(비차단): X-V1 PC 왼쪽 열 아래 빈 칸, X-CN-1 표 원서접수 칸 두 줄. 하위 3인 심사는 돌리지 않고 내 판정(v2 6.7·6.8 대비 지적 해소, 약 7)이라 점수는 추정 — 배포 전 글자는 editor 검수·deploy push+ci 같이.
- [편집 검수 요청] X-V1 v3 글자 트랙:A · 담당 firemap-editor-en · 시한 14:40 · 근거 ventures/uk-pay/site/index.html, 바뀐 글자 목록 design/uk-pay/v3/notes.md — 통과하면 site/index.html.edit.json(sha는 `deploy.py hash`)
- [편집 검수 요청] X-CN-1 v3 글자 트랙:A · 담당 firemap-editor-web · 시한 14:40 · 근거 ventures/x-cn-1/site/hanneunggeom/index.html·src/nextline.cjs, 바뀐 글자 목록 design/x-cn-1/v3/notes.md — 통과하면 site/hanneunggeom/index.html.edit.json·site/index.html.edit.json
  착수: firemap-editor-web 13:40 (운영실장2)
  완료: firemap-editor-web 13:42 — 통과(aitell 2.2, 숫자·면책 변경 0, 고친 곳 없음). 배포 때 deploy.py push와 ci 같이
- [지시] R31 막힘 풀기 + 새 후보 5 트랙:A · 담당 firemap-venture-research-kr · 시한 10/5 20:00 · 근거 backlog.md 21행·candidates.md R31
  - data.go.kr 15114146 이용허락 원문·143기관 실제 건수(API 1회)·무상수거 기준 원문 → candidates.md R31 칸. 새 후보 5개는 거름망 '1쪽 작은 도구 사이트 0개인 1~5만 검색어', **비사이트(디지털 상품·B2B) 2개 이상**, 발견 길(검색 말고 첫 100명)을 칸마다 적기.
  착수: firemap-venture-research-kr 13:35 (본부장 직접 투입)
- [지시] 새 후보 5 트랙:A · 담당 firemap-venture-research-global · 시한 10/5 21:00 · 근거 backlog.md 24행
  - 퍼즐 밖으로: Etsy 인쇄용 PDF·스프레드시트 템플릿(판매 수 표시)·크롬 확장(사용자 수) 중 '전부 코드로 만드는' 것. **계정·결재 없이 오늘 공개할 수 있는 길**이 있는 후보에 가점. G33은 X-G21(KDP 결재 대기) 뒤로.
  착수: firemap-venture-research-global 13:34 (본부장 직접 투입)
  완료: 새 후보 5(G38~G42) — 1위 G38 저축 챌린지 PDF 생성기 12점(Etsy 1등 r445·상점 s137.1k, 경쟁은 고정표뿐), 2위 2027 달력 11, 크롬 확장은 1위도 5,000 users라 7점 · 근거 ventures/candidates.md '10-05 8회차' 13:42
- [요청] G38 저축 챌린지 PDF 생성기(목표 금액·기간·통화 → 칸 맞춘 PDF, 한국어 '26주 적금표' 포함, G41 빚 갚기 틀 2번째) 트랙:A · 담당 firemap-venture · 시한 10/6 12:00 · 근거 ventures/candidates.md G38 — 첫 판 1일(사용자 사이트 새 폴더, 계정·결재 0), 지표 7일 PDF 생성 수(firemap_events), 첫 100명=카페·블로그·오픈채팅 한국어판 링크, Etsy 판매는 결재
- [요청] 두 실험 사이트 서치콘솔 속성(사용자 사이트 kygstar77-creator.github.io 하나로 두 폴더) 트랙:D · 담당 firemap-growth · 시한 10/6 12:00 · 근거 approvals 13행(서치콘솔 승인됨·손 남음) — 사람 손이면 결재함 손 목록에 한 줄 추가만. 10/8 22:00 판정 규칙이 '색인율 절반'이라 지금 0이면 판정 불가.
