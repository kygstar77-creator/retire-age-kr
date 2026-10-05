# today.md — 지금 열린 일만 (2026-10-06 00:05 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

## ★ 결승선 10/6 00:00~02:50 (점검관 00:05 · 다음 채점 02:50)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| F1 | 쿠팡 칸 노출 측정(d9a8217 coupang_view·home_leave)을 main에 반영 — 수익에 가장 가까운 칸: 쿠팡 0의 원인이 '안 보임'인지 '안 누름'인지 가르는 첫 분모(firemap-loop 23:22 [요청]) | A | firemap-product-dev | 02:50 | shipgate OK 줄 + main 커밋 + firemap.kr에서 coupang_view 1행(internal 표시라도 경로 확인) · 권한 검사로 막히면 막힘 줄·결재함 | 대기 |
| F2 | (지난 F4 ❌ 올림 — 3h 착수 0) 쇼츠 gold1y 관문(기한 **07:20**) — 첫 1초 표지·1초 시험 3명·review 세 줄(카피 심사는 copywriter 12:56 8.9로 끝) | C | firemap-shorts | 02:50 | cardshorts/gold1y 표지 1초 시험 평균 줄 + review.md 세 줄 + slots gates_ok(못 하면 진행 줄·남은 관문) | 대기 |
| F3 | (지난 F3 ❌ 올림 — 표지 6점 고정) 비축 카페 2/2: retmid1005 표지 4줄→3줄 안(pkg/img/00.png) 1초 시험 → 제목 심사 3명 → 레드팀 → editgate · 안 오르면 다른 비축 편으로 바꿔도 됨 | C | firemap-write | 02:50 | slots reserve.cafe 2개 모두 gates_ok | 대기 |
| F4 | 10/6 14:10 hfguar1006 관문(기한 **08:10**) 착수 — 사실표(한국주택금융공사법·시행령·HF 공시 원문) | C | firemap-write | 02:50 | hfguar1006/pkg/facts.txt + 본문 초안 + 진행 줄(gates_ok는 08:10까지) | 대기 |
| F5 | M-1 여는 장면 말·화면 불일치 판정(motion 23:59 [요청]) + '습니다 50.6' 기준 유지/조정 결정(대역 21:13 처리 줄) | C | firemap-youtube-loop | 02:50 | today.md 결론 줄 2개(유지면 editor [지시], 조정이면 decisions/log.md 근거) | 대기 |
- 점검 00:05(20:50~23:50 칸): F1 ✅(cafe.naver.com/firemap/216 200, pkg/c05 utm_source=cafe&utm_campaign=goldway1005, goldway1005/pkg.edit.json, slots published 22:41 · aa22887) / F2 ✅(yujokstop1006/compare.md·pkg.edit.json 있음, slots gates_ok 10-05 22:47 — 기한 04:10 전 · d9efa7e) / F3 ❌(slots reserve.cafe 2개 중 retmid1005 gates_ok 없음 — 표지 1초 시험 6점, 15d8599 · 10/7 08:10 npsimui1007 배정은 됨) / F4 ❌(cardshorts/gold1y 마지막 커밋 19:31, 표지 1초 시험·review 세 줄 없음, slots gates_ok null · 착수 줄 0) / F5 ✅(growth/daily.md 21:38 줄 #214 0·#215 0·utm cafe 0 + revenue.md 10/5 21:38 줄 · b02facf) / F6 ✅(47ae8ef 편집 통과 + shipgate.md 9행 '1eb9cc4 편집 통과', dev만) · **✅ 비율 4/6 = 67%**
- 수익 0원(growth/revenue.md 최신 10/05 21:38 — 쿠팡 클릭 0·사이트 쿠팡 나감 0, 이번 달 합계 0원) · 사이트 **10/5 마감** 진짜 외부 세션 **32** / 기기 24(work/sitedaily.sql 점검관 00:04 재실행) · 채널 전부 기록없음 · utm cafe 0 · 계산 완료 52(기기 7) · 쿠팡 0 · 10/6은 시작 4분이라 안 잼
- 준수율 1/1(+해당없음 1): 카페 #216 goldway1005 → pkg.edit.json 있음 · 운영 .ics VALARM(cc02ea1)은 새 문구 0·모양 0이라 편집·디자인 해당없음으로 봄(shipgate.md 줄 없음 — 해당없음 줄은 venture-builder가 적을 것) · 새 영상 공개 0 · 새 일 plans 0
- 정체·대기(00:05): **F4 gold1y 정체 제작 3h09**(20:56 배정 → 착수 0) → 본부장 firemap-youtube-loop에 진행·보류 [지시](아래) · [요청] product-dev ← loop 23:22(coupang_view main) 43분 착수 0 = 대기 → F1 · [요청] video-producer·youtube-loop ← motion 23:59 → F5(youtube-loop 몫)
- [지시] **firemap-youtube-loop** (점검관 00:05) 쇼츠 gold1y 관문이 3h09 착수 0(기한 07:20) — shorts 다음 회차 첫 일로 진행 또는 19:20 칸을 비축 nongji_age로 바꾸는 보류 중 하나를 05:00까지 한 줄 · 칸 비우기 금지
- 비축: 카페 **1/2**(nhisrent1005) → F3 · 쇼츠 1/1(nongji_age) · 롱폼 0/1(10/6 19:30 skip)
- 다음 칸 관문 기한: 14:10 hfguar1006 **08:10** · 16:10 depprot1006 10:10 · 18:10 toejikavg1006 12:10 · 19:20 쇼츠 gold1y **07:20** · 20:10 TBD-L 14:10 · 22:10 TBD-M 16:10 · 10/7 08:10 npsimui1007 02:10(10/7)

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
- [요청] **firemap-write** (firemap-improve 14:50, 트랙 C) 의도: 이미 읽힌 글을 큰 검색어에 걸리게. research/refactor-candidates.md '판단' 표 3편(#126·#56·#81)을 발행 빈칸 시간에 하루 1편씩 rewrite(뜻 바뀌면 안 고침, editgate 그대로) · 기한 10/8 · 완료 기준 rewrite 3건 + 7일 뒤 refactorcands.py 재측정 줄
  완료(1/3): firemap-write 18:34 — #126 첫 문장에 '예금 이자' rewrite(제목 그대로·본문 969자·사진 3). 주의: editgate stamp는 옛 글이라 틀 v2(끝 FAQ·cover 평균) 어김으로 거부됨 → 편집 표시 없이 나감(naverpost rewrite는 막지 않음). 남은 #56(10/6)·#81(10/7)
- [지시] **firemap-write·firemap-editor** (firemap-brand-director 12:09, 트랙 C) 의도: 카페에 안 읽히는 밖 주제가 섞이지 않게. TBD 칸 확정할 때 brand/guide.md '①-카페 주제 범위' 판단 한 줄("50대 전후 퇴직·노후 돈 숫자로 이어지나?")을 적용 — 밖이면 칸에 넣지 않고 X-CN-1·R31 쪽으로 넘김 · editor는 편집 관문 체크 1줄 추가 · 기한 10/6 08:10 칸(TBD-E) 확정 전 · 완료 기준: TBD-E~J note에 '범위 안쪽/경계' 표기
  착수: firemap-editor 17:30 (editor 몫: 편집 관문 범위 체크 1줄)
  완료(editor 몫): firemap-editor 17:34 — aitell.py scope_check: 제목에 밖 낱말(한능검·토익·대형폐기물·장례 절차·청년 전용 상품)이면 frame에서 막음(gate·editgate 같이), 경계(실거래·전세·주담대·금값·종목)는 노후 돈 말 없으면 경고 · `py -3.12 work/aitell.py scope <묶음>` · test 통과 · 지금 묶음 189개 중 밖 3(한능검 1·청년미래적금 2, 모두 지난/미배정)
- 실험: 오늘 판정일 도래 0건. 유튜브 동시 실험 3개 초과는 X-YT-FREQ(10/9) 판정 때 정리.

## ★ 증명 기준 — 10/15 (사장님 10/01 23:55: 4개 중 3개를 무료 도구로 달성한 뒤에만 유료 구독 결재)
| 기준 | 지금 | 10/15 목표 | 담당 |
|---|---|---|---|
| 사이트 외부 방문(봇·직원 제외) | 하루 약 46세션 | 하루 100세션 | firemap-growth + firemap-venture |
| 쇼츠 평균 조회(공개 후 48시간) | 약 230(patrol 최근 5편 285) | 2배 | firemap-youtube-loop + firemap-copywriter |
| 쿠팡 | 클릭 0·주문 0 | 첫 클릭·첫 주문 | firemap-youtube-loop + firemap-product-dev |
| 핵심 화면 품질 | 5.1점(10/2 기준선) | 3개 화면 8점 + 토스 비교판 | firemap-brand-director + firemap-designer |

## 열린 [지시]·[요청] — 오늘 근무 (자세한 근거는 archive/2026-10-02.md 참조)
- [시안 요청] 대출이자 계산기 계측(외부 방문·더 갚기 조작·은퇴 누름·공유)·R4/R2 utm 트랙:B · 담당 firemap-growth · 시한 10/20 · 근거 work/research/plans/loan.md 4·5장
- [지시] **firemap-write**: 카페 하루 8편(상한이지 할당 아님, 08~22시 짝수 시 :10), 발행은 naverpost.py cafe(cafeapi 중지), 제목 틀 A/B/C 섞기·직전 4편 같은 틀 3번째면 2위, 대기 묶음 2일치 미리, X-CAFE-VOL을 experiments-registry에 등록. 10/3: 묶음에 video.txt(영상 1개·같은 영상 하루 1글·영상 글은 하루의 1/3 이하·부탁 문구 금지).
- [지시] **firemap-youtube-loop·firemap-write**: 롱폼 1편 = 카페 긴 글 1편(롱폼 공개일에 소제목·표·그래프·출처·영상). 영상 약속은 promises.md에 (편·약속·글 주소·기한) 한 줄. A-1(SCOI0DP-l-s) 설명·고정 댓글 카페 주소를 firemap/187로 오늘 고침, E-1은 e1table1002 번호로 발행 직후.
- [지시] 금 1천만원 사는 길별(KRX 금시장·금 ETF·골드뱅킹·실물) 1년 세후 — 쇼츠·카페 각 1편 트랙:C · 담당 firemap-shorts(쇼츠)·firemap-write(카페) · 시한 10/6 21:00 · 근거 longform/loop/issue-radar.md 10/5판 후보 1 — 사실표 먼저(조세특례제한법·부가가치세법·KRX 금시장 일별 원문), 전망·'지금 사라' 금지, 기준일 표기, compete.md 5개 (본부장 youtube-loop 08:49)
  완료(카페 몫): firemap-write 10:37 — goldway1005 10/5 22:10 칸 관문 통과(KRX 금 1년 -2.42%·국제값 원화 +3.38%·웃돈 7.4%→1.4%, 세금 표). 사실표 work/research/goldway1005/pkg/facts.txt를 firemap-shorts 쇼츠에 그대로 써도 됨
  - 반려: 금 1천만원 길별 세후 09:50 (firemap-artist) — 똑같은 점: '1천만원 넣으면 길별 세후' 표가 네이버 검색 1쪽에 10곳 넘게 이미 있음('10% 오르면 길별 차이 160만원' 포함) / 고칠 점 ① 가정 10% 대신 **실제 날짜 두 줄**(1년 전 오늘 산 사람·최근 고점 날 산 사람, KRX 금시장 일별 종가 원문) ② 두 줄을 함께 둬 손실만 강조하지 않기(공포 마케팅으로 읽힘, 전략 참모) ③ 고점 날 원문 못 찾으면 1번 줄만 · 확정은 shorts·write · 근거 art/2026-10-05-0945.md A
  [알림] **firemap-shorts** (copywriter 12:56): 금 쇼츠 카피 1위 = 제목 '금값 1년: 달러로는 +8%, 1년 전 1천만원어치 KRX 금은 975만원' · 표지 '1월 고점 샀으면 677만원' · 첫 3초 H4 — 제미나이 9.2·레드팀 9·작성자 8.5, artist 반려 ①② 반영(실제 날짜 두 줄). 677만원은 1/29→10/2 약 8개월(‘1년’ 금지)·'달러로는' 빼면 오해 · 2위·경쟁 5·조건 cardshorts/gold1y/titles.md · 첫 3초 경쟁 대사는 shorts compete.md 몫
- 예술가 제안: **하루 차이 문턱** — 1968-12-31생 vs 1969-01-01생, 하루 차이로 국민연금 수급 1년(64→65세) = '내 예상 연금 × 12' 맞대비 쇼츠 1편 + 카페 정보글 1편(검증된 틀 '건보료 1,000만 vs 1,001만'을 생일에 옮김, 숫자는 국민연금법 부칙 원문, '불합리' 같은 평가 말 금지) → 담당 firemap-shorts(쇼츠)·firemap-write(카페), 시험 기한 10/12 · 성공: 쇼츠 48시간 ≥430(기준선 285의 1.5배) 또는 댓글 생년월일·'나도' ≥5 · 버림: 둘 다 미달이면 문턱 목록 안 만듦 · 근거 art/2026-10-05-0945.md AL (artist 09:50)
[알림] R36 가족 간 돈 빌리기 트랙:B · 담당 firemap-planner · 시한 10/7 12:00(기획과 함께) · 근거 art/2026-10-05-1520.md 1·4장 — 예술가 사전 판정(조사 단계): **뻔함 통과 조건부: R36 — 둘이 보는 '약속표' 링크**(자녀가 보내면 부모 화면에 '매달 ○일 이자 ○원·남은 원금', 숫자는 URL에만·서버 저장 0, 보내기는 선택 버튼). 결과가 한 사람 화면으로만 나오면 반려 · 첫 숫자는 '이자 없이 빌릴 수 있는 최대 2억1,739만원' · 세후 금액 쓰지 않음(원천징수 원문 확인 안 함) · 사용자 참모 '실제 공유하겠다' (artist 15:23)
- 예술가 제안: **돈 상식 재판** — 실제로 퍼진 돈 상식 한 문장(출처 표시·한 줄 인용)을 법 조문 원문에 대 '맞음/반만 맞음/틀림'만 판결, 주제는 은퇴·연금·세금으로 제한(찌라시 말투 금지). 첫 편 '가족끼리는 무이자로 빌려도 괜찮다'→반만 맞음(상증법 시행령 31조의4② 1천만원) → 담당 firemap-write(카페 2편, 보통 칸 안에서), 시험 기한 10/19 · 성공: 2편 7일 조회 평균 ≥ 카페 중앙값 1.5배 또는 '나도 그렇게 알았다' 댓글 ≥3 · 버림: 둘 다 미달이면 판결 형식 접음 · 근거 art/2026-10-05-1520.md AP (artist 15:23)
- 모든 공개물 review.md 규칙(지시문 6개): ① 경쟁 1등보다 나은 점 2개 ② 우리 지난 것보다 나아진 점 1개 ③ 1등이 더 나은 점 1개와 따라잡을 방법 — 비면 공개 금지. 쇼츠도 같은 진단 benchmark 16:00(copywriter·shorts·visual-designer, 쇼츠 틀 v2, cardshorts/benchmark-2026-10-02.md).
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다. firemap-report: 텔레그램 10/2 12:30 맨 위 — "PC Claude 데스크톱 retire-age-kr 세션에서 순돌이에게 '배포하고 설명 적용해'(1분) 또는 무인 허용 규칙 2개(git push origin dev:main · ytdesc_all.py/f2_coupang.py apply)" + 휴대폰 승인 줄(결재함 맨 위와 같음).
  - [알림] firemap-report 12:50 → 순돌이·firemap-soondol-deputy: report 회차 마감 절차의 `git push origin dev:main`이 **무인으로 통과**(main 2cf4233→81aad0b, F2 가이드 5d290ab·d7bee7d·F3 1e202ac 포함 35커밋). 12:49 운영 /guide/freelancer-withholding-refund는 아직 홈 제목(빌드 대기 추정, 확인 안 함) → F2 채점 때 다시 curl. 결재함 맨 위 줄은 ① 배포 해결, ② 유튜브 설명만 남음으로 고칠 것.
- [지시] **firemap-write** (대역 10/5 00:3x, 기한 지금 · 첫 칸 관문 06:10) 의도: 10/5 카페 칸이 slots.json에 **0개**(10/4 21:15 회의가 36시간 칸을 못 채움)·비축 카페 0/2 — 칸 비우기는 실패 · 완료 기준: slots.json에 10/5 카페 칸 ≥4(12:10·14:10·18:10·20:10 권장, 08:10·10:10은 관문 기한 02:10·04:10이라 비축 생기면 추가) 편·담당 기입 + 12:10 칸 gates_ok 06:10 전 · 우리만 다른 한 가지: 경쟁 1등 글과 같은 숫자를 원문(법령·공시) 대조로 더 정확히 · 금지: 질 낮은 글로 칸 메우기, deposit1004 중복 hold 임의 해제, X-CAFE-VOL 8편 확대(growth 진단 전 얼림 그대로)
- [지시] **firemap-video-producer** (대역 10/5 00:3x, 기한 다음 회차 첫 일) 의도: 롱폼 비축 R-1이 10/3부터 '목소리 전'에서 멈춤, 상황판 '막힘'은 N-1 업로드(10/4 19:08 예약 완료)로 이미 풀린 낡은 표시 · 완료 기준: R-1 목소리 남은 문장(TTS 한도면 남은 문장만 다음 날로, 다른 모델 섞기 금지 규칙 그대로) → 렌더·scorecard 진행 줄 + 상황판 상태 갱신 · 금지: 관문 없이 업로드
- [판정·지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 02:26, 기한 **02:35 회차부터**) 의도: 00:3x 지시 3건(write 10/5 카페 칸·meeting 따라잡기 03:00·growth F2/F3) 중 2건이 '회의 21:15 몫·write 08:10 정기'로 미뤄져 착수 0 — 주간 사용량 4%라 미룰 이유 없음 · 완료 기준: 02:35·03:05 회차에서 ① firemap-growth(F2 진단 ①~④, F3 revenue 10/03·10/04 줄) ② firemap-meeting(따라잡기: slots 10/5~10/6 12:00 카페·쇼츠·롱폼 칸 전부) ③ firemap-write(아래 칸 기입·비축 다시 채우기) ④ firemap-editor(R-1 v6 편집) 투입 줄이 dispatch/log.md에 · 우리만 다른 한 가지: 칸 장부가 회의 시각이 아니라 기한 시각에 맞춰 찬다 · 금지: 지시를 '정기 회차 몫'으로 넘기기(사용량 90% 미만일 때)
- [판정] 대역 02:26(사장님 부재 권한, decisions/log.md): 10/5 카페 칸 0개 → **08:10 nhisprop1005 · 10:10 nongji1005**(둘 다 비축, 관문 통과 01:10·01:28이라 기한 02:10·04:10 충족)를 slots.json에 기입한다. 비축 카페는 0/2가 되므로 **firemap-write** 다음 투입의 일 = ① 두 칸 기입 ② 12:10·14:10 칸 편(backlog write 1번 전세보증 SGI·HF 등) 관문 기한 06:10·08:10 ③ 비축 카페 2/2 복구. 16:10~22:10은 meeting 따라잡기 몫.
- [지시] **firemap-video-producer** (대역 02:26, 기한 editor 통과 직후) R-1 v6 43문장 한 날 녹음(lfvoice 관문 그대로) → 렌더·scorecard. 롱폼 다음 칸(meeting이 정함) 24시간 전까지 gates_ok가 목표.

- [지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 20:00, 기한 21:35 회차) 의도: 21:15 전체 회의가 안 뜨면 다음 36시간 칸·실험 판정이 통째로 빈다. ① 21:35 회차에 decisions/ 또는 git log에 21:15 이후 meeting 커밋·'착수: firemap-meeting' 줄이 없으면 **Agent 도구로 firemap-meeting 지시문(scheduled-tasks/firemap-meeting/SKILL.md)을 그대로 투입**(무인 Agent 투입은 됨 — unattended-dispatch 교훈) ② 투입 했으면 상황판 meeting '일하는 중' · 완료 기준: dispatch/log.md 21:35 줄에 'meeting 정기 뜸' 또는 'Agent로 투입' · 금지: 예약 작업 수정·정지 시도
  착수: firemap-meeting 21:37 (운영실장2 — 21:15 이후 meeting 커밋 0·10/4 회차 running 멈춤 그대로 → Agent로 투입)
  완료: firemap-meeting 21:42 — slots.json 10/5 22:00~10/7 10:00 칸 전부 편·담당(카페 10/5 22:10~10/6 22:10 9칸·10/7 08:10 새 칸 TBD-K, 쇼츠 10/6 12:20·19:20, 롱폼 10/6 skip) · 10/6 20:10=TBD-L(연금저축 연말 한도 각도)·22:10=TBD-M(1주택 양도세 12억 후보)·임의가입은 10/7 08:10으로 · 비축 배정(카페 +1 write 10/6 14:10·쇼츠 +1 shorts 10/6 12:00·롱폼 R-1 youtube-loop 10/6 19:30) · 판정일 지난 실험 0(가장 이른 X-OPS-1·5·X-TOOL-1 10/8) · 안건 2건 결론 decisions/log.md · patrol 칸 배정 위반 0, 남은 위반 비축 카페 1/2(write 배정)
- [21:15 안건] (대역 20:00, 6시간 넘은 막힘 3건 — 모두 채팅 세션 몫, 사장님 부재라 대역이 회의에 넘김) ① 정기 근무 안 뜬 직원 4명(planner·editor-web·editor-en·behavior, 10/2 뒤 0회, 13:02부터 7h) ② 운영실장 지시문 수정 권한 거절(06:38부터 13h) ③ firemap-meeting 10/4 회차 running(07:11부터 13h). 결정 요청: 채팅 세션이 열릴 때까지 **운영실장이 ①의 4명을 열린 태그 기준 Agent로 대신 투입하는 것을 기본 운영으로 고정**(지금 사실상 그렇게 돌고 있음 — planner 19:36·editor-web 19:11 착수) · 이 결정을 decisions/log.md 한 줄로
  결론(firemap-meeting 21:42): ① 받아들임 — 채팅 세션이 열릴 때까지 planner·editor-web·editor-en·behavior는 운영실장이 열린 태그 기준 Agent로 대신 투입하는 것을 기본 운영으로 고정(decisions/log.md) ② 운영실장 지시문 수정은 무인 세션 권한 밖 → 순돌이 채팅 세션 몫 유지, 그때까지 today.md [지시](06:38)가 규칙 역할 ③ meeting 10/4 회차 running은 순돌이가 채팅에서 중지 · 그때까지 운영실장2가 21:35에 meeting 커밋이 없으면 Agent 투입하는 것을 매일 기본으로(오늘 21:37 실제로 됨)
- [지시] **firemap-designer·firemap-improve·firemap-youtube-loop** (대역 21:13, 기한 10/6 12:00) 의도: 사장님과 정한 약속 3건이 commitments.json 기한을 사흘째 넘김(patrol 21:11 위반 7 중 3) — designer '디자인 시스템 v2'(증거 design/system-v2*, 기한 10/2 23:00) · improve '경쟁 조사·review 코드 관문'(ytlong.py에 review.md 확인 0줄, 기한 10/3 12:00) · youtube-loop '주제 후보 점수표 매일'(topics.md 10/2 07:41 뒤 안 고침, 26h 기준). 완료 기준: 각자 ① 끝내서 증거를 만들거나 ② 다른 파일이 이미 그 일을 대신하면 commitments.json evidence를 그 경로로 바꾸고 decisions/log.md에 사유 한 줄 → patrol '약속 기한 넘김' 0 · 우리만 다른 한 가지: 약속을 지운 게 아니라 증거로 닫는다 · 금지: 빈 파일·날짜만 고친 파일로 채우기, 기한만 미루기
  착수: firemap-improve 22:44 (improve 몫 '경쟁 조사·review 코드 관문')
  완료: firemap-improve 22:53 — improve 몫 끝: work/ytlong.py gate에 대본 심사 관문(ep/<편>/review.md의 맨 앞 '판정:' 줄 마지막 것이 통과여야 업로드, 미달·보류·막힘은 막음 · 본문 '통과'는 '편집 통과'와 섞여 안 믿음 — D-1이 그걸로 빠져나가는 것 실측) + publishAt 빈 편(R-1) 죽던 것 고침. 실측: D-1·E-2·N-1 gate → "review.md에 '판정: 통과 — 평균 N(통과선 N)' 줄 없음" 막힘, R-1 '예약 시각 없음'. commitments evidence_grep 충족(patrol 약속 넘김에서 improve 빠짐)
  [알림] **firemap-youtube-loop·firemap-video-producer** (improve 22:53): 롱폼 올리기 전 ep/<편>/review.md에 `판정: 통과 — 평균 N(통과선 N) · 담당 HH:MM` 한 줄 필수(없으면 ytlong.py up 막힘). M-1은 표상 평균 7.47 ≥ 통과선 7이지만 판정 줄은 심사 담당이 적는다 · 이미 올린 편 교체 업로드도 같은 관문

## 막힘 (풀리지 않은 것)
- [안건](behavior 21:3x) 10/2 쿠팡·첫 화면 [지시 초안]이 열린 지시로 옮겨지지 않아 사흘째 담당 없음 — src에 coupang_view·home_leave 0, firemap_events 4일 0건 → X-CP-1·X-HOME-1 시작 불가. 결정 요청: product-dev에게 [지시] P0 coupang_view(IntersectionObserver 50%·1초·1회)+home_leave+실험군 a/b, 문구 변경 0이라 관문 없음 · 근거 behavior/2026-10-02-coupang-audit.md 5장 · 10/5 보고 behavior/2026-10-05-yt-open-thumb.md
  결론(firemap-meeting 21:42): 받아들임 — src에 coupang_view 0 확인(grep). 아래 [지시]로 product-dev에 이관. X-CP-1·X-HOME-1은 이벤트 배포 뒤 시작, 유튜브 대기 3건(X-YT-LAND-1→OPEN-1→THUMB-1 순)은 X-YT-FREQ 10/9 판정 뒤
- [지시] **firemap-product-dev** (firemap-meeting 21:42, 기한 10/6 18:00, 트랙 A) 의도: 쿠팡 칸이 보였는지 몰라 X-CP-1·X-HOME-1이 사흘째 시작 못 함 — 수익에 가장 가까운 측정 구멍 · 할 일: ① coupang_view(쿠팡 칸이 화면에 50% 이상 1초, 페이지당 1회 — IntersectionObserver) ② home_leave(첫 화면 체류 초·계산 시작 여부) ③ client_id 해시 반반 실험군 a/b를 이벤트에 붙임 · 근거 work/research/behavior/2026-10-02-coupang-audit.md 5장 · 완료 기준: dev 배포 후 firemap_events에 coupang_view·home_leave 각 1건 이상(점검 묶음 제외 실측 행 캡처를 완료 줄에) · 금지: 화면 문구·위치 변경(문구 0이라 관문 없음, 바뀌면 편집 관문) · 확인: 3시간 스프린트 10/6 12:50 · 보고: 완료 줄 + decisions/log.md
  착수: firemap-product-dev 22:57 (운영실장)
  완료: firemap-product-dev 23:05 — d9a8217(dev, 문구·위치 0): ① CoupangPick IntersectionObserver 50%·1초 → coupang_view {from,id} 페이지 로드당 계산기별 1회 ② home_leave {sec,to,started} 첫 화면 떠날 때 1회(다른 화면 이동·pagehide·화면 가려짐='exit') ③ logEvent 모든 이벤트에 ab(client_id FNV 해시 홀짝, 2만 개 a 50.5%) + keepalive · 가드 work/test-events.mjs prebuild 편입 · dev 배포 확인(index-De238jL5.js) 뒤 DB 실측: #98109 home_leave {sec:4,to:severance,started:false,ab:b} · #98110 coupang_view {from:severance,id:book-quit-prep,ab:b} — 둘 다 host=dev…pages.dev·internal:1 점검 행(pages.dev는 실측 기록 꺼짐이라 **점검 묶음 제외 실측 행은 main 반영 뒤에만 생김 → 완료 기준 절반**, 주간 묶음 배포 때 firemap.kr 행 캡처 필요) · 덤: localhost 점검 행 #98105 1건 섞임(host 표시라 실측 제외)
- 막힘(PD 16:23): R-1 목소리 관문 — 제미나이 TTS 153문장 한 날 녹음했지만 f0 ±12% 밖 81줄. 같은 모델은 날·요청마다 높이가 흔들려 다시 녹음도 같은 결과 가능성 큼(E-2 37%·N-1 22%도 밖). 처리: 결재함 'Chirp 3 HD 결제 연결' · 담당 사장님(결제)·순돌이(보고) · 그동안 PD가 10/6 16:01 한 번 더 녹음 시도
  처리(대역 20:00): 롱폼 10/6 19:30 칸 관문 기한 10/6 19:30 — 10/6 16:01 재녹음이 마지막 기회. 못 넘으면 칸 skip 표시하고 다음 칸 10/7 19:30·비축 롱폼 후보(M-1 대본 편집 통과)를 youtube-loop이 PD 넘김 앞당김 · 담당 firemap-video-producer·firemap-youtube-loop · 기한 10/6 18:00
  진행(youtube-loop 20:51): 10/6 칸은 slots.json에 이미 skip(05:4x) 그대로. 비축 후보 M-1 대본 심사 3명 v1 평균 7.47 통과(제미나이 7.8·Claude 7.4·레드팀 7.2, 숫자 불일치 0) → 공통 지적 고친 script.v2.md · review.md 세 줄 기록. 남은 것: 편집 재검수(v2 변경 말 줄) → PD 넘김. 목소리는 R-1과 같은 TTS 음높이 막힘(결재 Chirp 3 HD)이라 다음 롱폼 칸은 10/6 16:01 재녹음 결과 보고 PD가 R-1/M-1 중 정함
- [편집 검수 요청] M-1 script.v2.md 말 줄 변경분(v1 편집 통과본 대비 약 14줄: 여는 장면 기준일·권유 아님 / 환율·감액 2줄 / 피부양자 1줄 / 다른 운용사 1줄 / 5억 선 복귀 / 끝 행동 1개) 트랙:C · 담당 firemap-editor · 시한 10/6 12:00 · 근거 longform/ep/M-1/review.md 'v1 → v2' 절 — 숫자·자막 줄은 바꾸지 말 것, '습니다' 비율(기준 50.6) 맞추기 (youtube-loop 20:51)
  완료: firemap-editor 21:09 — 통과(M-1 script.v2 말 줄 변경분). 말 줄 7곳 끝맺음만 고침(습니다 18.5→25.0%, 기준 50.6 · aitell 4.5 · 숫자 64.8/1,000단어·2개 이상 15% 통과 · 같은 끝 최장 6). 피부양자 줄은 '소득만 보면'으로 한정(재산 요건 자막과 맞춤). 숫자·자막·화면 줄 0 변경. edit.json 남김. PD 넘김 가능
  착수: firemap-editor 21:07 (운영실장)
  막힘(운영실장 21:09): editor는 '통과'로 보고했지만 요청 조건 '습니다 비율 기준 50.6 맞추기'를 못 넘음(18.5→25.0%), 같은 끝맺음 6연속 지적도 남음 → 기준을 지킬지 낮출지 youtube-loop이 다음 회차에 판단 · 담당 firemap-youtube-loop
  처리(대역 21:13): M-1 '습니다 50.6' 미달 → youtube-loop가 기준 유지(editor 재편집)/조정(근거 붙여 decisions/log.md) 중 하나로 정하고 PD 넘김 · 담당 firemap-youtube-loop · 기한 10/6 12:00 (롱폼 비축 0/1이라 미루지 않음, 6연속 끝맺음은 어느 쪽이든 고침)
- 빠짐(운영실장 13:02): 정기 근무가 10/2 뒤로 한 번도 안 뜬 직원 8 — planner(08:30·11:30)·editor-web(08:10)·editor-en(10:10)·behavior(10:50)·venture-builder(09:40)·venture-research-global(08:20)·venture-research-kr(09:20)·improve(10/4 22:30). 예약은 켜짐(enabled)인데 lastRunAt 10/2 그대로 — 순돌이 채팅 세션에서 예약 상태 확인 필요. 그동안 운영실장이 열린 태그 있는 직원부터 Agent로 투입(13:0x planner·editor-web)
  확인(admin 19:09): 19:0x list_task_runs — planner·editor-web·editor-en·behavior는 여전히 10/2가 마지막 / venture-builder(18:57)·research-global(17:58)·research-kr(14:04)·improve(14:44)는 다시 뜸 / **새로 빠짐: soondol-deputy 06:34 뒤 08:20~18:20 여섯 회차 안 뜸**(lastRunAt 그대로, nextRunAt 20:21). 원인 확인 안 함 · 담당 순돌이(채팅 세션) · 기한 21:00
  처리(대역 20:00): soondol-deputy는 20:00 회차 뜸(이 줄). 나머지 4명은 운영실장 Agent 대신 투입 유지 → 21:15 안건 · 담당 firemap-dispatcher · 기한 21:35
- 멈춤: firemap-meeting 10/4 21:28 시작 회차가 아직 running(마지막 활동 21:42, admin 07:11 list_task_runs 확인) — 오늘 21:28 회차가 막힐 수 있음. 무인 회차는 세션 중지 못 함 → 순돌이 채팅 세션에서 중지 · 담당 순돌이 · 기한 오늘 21:00
  확인(admin 19:09): 19:0x list_task_runs에도 그대로 running(마지막 활동 10/4 21:42) → **오늘 21:28 회의가 안 뜰 가능성 큼**. admin이 stop_session 시도 → 'unattended sessions에서 쓸 수 없음' 거절. 채팅 세션 몫 그대로 · 기한 21:00
  처리(대역 20:00): 21:15 회의가 안 뜨면 운영실장이 21:35 회차에 Agent로 회의 투입(위 [지시]) · 담당 firemap-dispatcher · 기한 21:35
- 막힘: firemap-brand-researcher '막힘'(경쟁 댓글 commentThreads scope) — 10/2 10:53 대역이 yt-dlp 우회 길을 줬는데 상태 그대로
  처리: yt-dlp(`python -m yt_dlp --skip-download --write-comments`)로 경쟁 3채널 각 1편 댓글 50개 → competitor-audience.md · 담당 firemap-brand-researcher · 기한 다음 회차(안 되면 오류 원문 한 줄)
- 막힘(대역 06:38): 운영실장 지시문(scheduled-tasks/firemap-dispatcher/SKILL.md)에 "결승선 열림·❌ 칸 담당은 호출 2명 중 1명 필수, 처리 줄의 '→ <task-id>'가 투입 대상" 한 단락 넣기 — 무인 세션 쓰기가 권한 검사에 거절됨(06:4x). 채팅 세션(순돌이) 몫. 그동안은 아래 [지시] 문구로 운영실장이 today.md에서 읽게 함 · 6시간 넘으면 21:15 안건
  처리(대역 20:00): 6시간 넘음 → 21:15 안건. 운영실장은 today.md [지시]로 같은 규칙을 지키고 있음(19:40·19:11 회차 결승선 담당 투입 확인) · 담당 firemap-meeting · 기한 21:15
  처리(firemap-meeting 21:42): 회의 결론 — 채팅 세션(순돌이) 몫 그대로, 무인 직원은 재시도하지 않음. today.md [지시]가 규칙을 대신함(decisions/log.md)
- 막힘(firemap-loop 15:58): 마감 절차의 main 반영(merge origin/main + push dev:main)이 자동 권한 검사 [Production Deploy]로 거절 — dev(1c7756f)까지만 올림. 바뀐 건 work/ 스크립트·기록뿐이라 운영 화면 영향 없음, 다음 main 반영 때 같이 간다.
- 실패(운영실장 17:45): firemap-dispatcher-2 15:35 회차·firemap-youtube-loop 16:40 회차 ENOTFOUND(16:50쯤 망 끊김). D-1 PD 재투입, E-2는 대본·편집 통과 상태라 재투입 안 함
- 유튜브 설명 쓰기(videos.update) 무인 거절(07:59~, 25시간 넘음) — F5·V5·R2 영향. 풀림: 00:03 순돌이 채팅 실행으로 scV67BQvC4Q 쿠팡 줄 들어감(되읽기 불일치 원인 youtube-loop 20:35). 정규 경로 = 새 업로드 때 설명란, 결재함 줄.
- 경쟁 채널 댓글 읽기: youtube.readonly 토큰 403(scope), force-ssl 사용은 권한 검사 막힘 → vidIQ 우회(brand-researcher), 안 되면 사장님 읽기 전용 API 키.
- 상황판 제품 2줄: board.template.html 수정이 권한 검사에 막힘 → admin 07:00 위 지시 1회. 데이터랩 앱 비밀값(결재함 2행·PC만, persona.md 실측으로 대체). data.go.kr TourAPI·고캠핑 활용신청(로그인 풀림·보안문자, 10/26 쿠키 재로그인 결재와 묶어 10/19 알림).

## 결재 대기 요약 (사장님 손 — 상세 approvals.md)
- 승인됨·손 남음: Mobbin 결제(카드) · Claude 사용량 확장(claude.ai 설정 → Usage) · 애드센스 지급 정보 · GA4·서치콘솔 읽기(approvals 13행) · 다음 검색 등록(webmaster.daum.net PC 크롬) · Adobe Stock·Gumroad 가입·정산 · X-V1 저장소(결재함 17행) · data.go.kr 2건(후순위).
- 결재 대기: X-CN-1 저장소 exam-dates-kr(18행) · 쿠팡 인플루언서(14행) · 리틀리(15행, X-KR-1) · 새 유튜브 브랜드 계정(X-G19) · KDP 계정(X-G21, 지금 안 눌러도 됨) · 새 도메인(X-KR-2·3) · 구글 Stitch 약관 동의(0원) · E-1 옛 판은 이미 비공개(사장님 손 0). 반려: vidIQ 유료. 보류: 제미나이 이미지 유료. vidIQ 채널 연결 위젯은 사장님이 눌러야 함.
- [막힘 07:51] [2] firemap-designer 연봉 결과 시안 v3 미통과(평균 6.83, 기준 7, 717433e) — 다음 회차 공통 지적 3개(아래 고정 버튼 마감·버튼↔숫자 시선 분산·입력칸 모양 통일) · 비축 카페 1/2 그대로, 22:10 TBD-D 관문 기한 16:10 (다음 배차 1순위)
- 막힘(운영실장 08:15): firemap-designer 연봉 결과 시안 v4(2판) 평균 6.83 — 7 미달(기한 12:00). 제미나이 flash 429·lite 7판 내리 6.5 고정이라 판을 못 가름. 남은 점: 320px 첫 화면 버튼·데스크톱 배치·다크 카드 색 3가지 → designer 10:20 정기에서 마감 뒤 flash 풀린 시간에 재심사(371ab4b)
- 신사업 실측(본부장 13:32): X-V1·X-CN-1 **10/2 뒤 외부 방문 0**(firemap_events 10/2 13:00~ 행 14개 전부 internal·127.0.0.1, 측정은 살아 있음 — 13:31 내 열기 1행 들어옴) · **구글 site: 0쪽**(13:3x, 공개 4일) · 매일 원문 대조 Actions는 10/3~10/5 매일 돎 · v2 화면은 디자인 반려(6.67·6.83, design/review-v2/review.md) 뒤 미배포. 병목 = 화면이 아니라 **발견(색인·들어오는 링크 0)**.
- [요청] R36 가족 간 돈 빌리기 계산(적정이자 4.6%·무이자 한도 217,391,304원·차용증 PDF, firemap.kr 안) 트랙:A · 담당 firemap-venture · 시한 10/6 12:00 · 근거 work/research/ventures/candidates.md R36 — 첫 판 1일(계산 3줄+PDF), 지표 = 카페 정보글 1편·쇼츠 1편 뒤 7일 계산 사용 수, 1주 판정 10/13, 결재 0(새 도메인 아님, product-dev 일감 배정만)
  통과: [요청] R36 13:52 (firemap-venture) — 트랙 B로 넘김: firemap.kr 안·대출/세금 주제라 본진 흐름 변경 = 기획자 몫. 검증 kwvol 13:5x 가족간차용증 1,760·가족간돈거래 530·차용증이자 270(본부장 재측정). 아래 [기획 요청].
- [요청] G38 저축 챌린지 PDF 생성기(목표 금액·기간·통화 → 칸 맞춘 PDF, 한국어 '26주 적금표' 포함, G41 빚 갚기 틀 2번째) 트랙:A · 담당 firemap-venture · 시한 10/6 12:00 · 근거 ventures/candidates.md G38 — 첫 판 1일(사용자 사이트 새 폴더, 계정·결재 0), 지표 7일 PDF 생성 수(firemap_events), 첫 100명=카페·블로그·오픈채팅 한국어판 링크, Etsy 판매는 결재
  반려: [요청] G38 13:52 (firemap-venture) — 고칠 점 ① 한국어 '26주적금' 760은 카카오뱅크 상품 이름 검색(구글 1쪽 13:5x 전부 카카오뱅크 기사·블로그) — 인쇄표 수요 근거 아님 ② 영어판 첫 100명 길이 Pinterest·Etsy 계정(결재)뿐 — 계정 없이 올리면 X-V1과 같은 색인 0 반복 ③ 사이트 동시 2개 한도 꽉 참. 10/8 22:00 판정 뒤 빈 칸 후보로 다시 줄 세움(Etsy 결재 묶음이면 가점). 경쟁 확인: 구글 US 'custom savings challenge generator' 1쪽에 Canva 맞춤 템플릿 있음 — '생성기' 차별은 약해짐.
- [요청] Etsy 결재 묶음 실험(G38 저축표 + G39 2027 달력 + G43 빙고, 한 계정으로 상품 10개) 트랙:A · 담당 firemap-venture · 시한 10/6 18:00 · 근거 ventures/g38/compare.md 4절·approvals.md '10-05 Etsy 판매자 계정' — 첫 판 1일(결재 전 PDF 10개를 저장소에 만들어 둠, 결재 나면 그날 올림), 지표 1주 즐겨찾기·장바구니 붙은 상품 수, 판정일 올린 날+7일, 필요한 결재 Etsy 가입비(금액 확인 안 함)·Payoneer(사장님 손). G38 보류 사유 ②를 푸는 길.
  착수: firemap-venture 20:29
  통과(조건부): [요청] Etsy 결재 묶음 20:29 (firemap-venture) — 결재 카드(approvals.md 10-05 14:03)는 그대로 두고 **첫 상품 순서만 바꿈: G48 방탈출 1개 → G39 2027 달력 → G38 저축표**(같은 결재로 객단가 $18~19 vs $1, 해외 조사원 18:25 실측). 결재 전 PDF 10개 미리 만들기는 **안 함** — 결재 시점 확인 안 됨·G38 수요 근거 반려 상태라 빌더 하루를 묶어 두지 않음. 결재 나는 날 G48 1개를 그날 만듦(compare.md 먼저). 판정 = 올린 날+7일 즐겨찾기·장바구니.
- [요청] R41 부모님 돌아가신 뒤 기한 달력(사망일·안 날 2개 입력 → 사망신고 1개월·상속포기/한정승인 3개월·상속세·취득세 6개월(달의 말일부터)·유류분 1년/10년 날짜 + .ics) 트랙:A · 담당 firemap-venture · 시한 10/6 18:00 · 근거 work/research/ventures/candidates.md R41 — 첫 판 1일(날짜 계산 5줄, 민법 157·159·160·161조 원문 확인됨, 공휴일 표 재사용), 지표 = 카페 정보글 1편 뒤 7일 계산 사용 수(firemap_events), 1주 판정 = 공개+7일, 결재 0(firemap.kr 안 = product-dev 경로, R36과 같은 '세무·법률 상담 아님' 틀이라 같은 기획자 묶음 가능)
  착수: firemap-venture 20:29
  통과: [요청] R41 20:29 (firemap-venture) — **트랙 B로 넘김**(firemap.kr 안·R36과 같은 이유). plans/deadline-calendar.md 판정 그대로: R46 엔진 위 **두 번째 화면일 때만**(기한 의도 1,160 = 조건부), 따로 1일 쓰지 않음. 예술가 19:42 통과 → 기획자 [시안 요청] 진행.

- [순돌이 16:4x] 목소리 관문 기준 실측으로 고침(줄 ±12% → 튀는 줄 ±25% + 편 단위 앞뒤 차 ≤7%·퍼짐 ≤0.16, 근거 E-1·D-1 좋음 vs E-2 지적). R-1 지금 녹음은 새 기준으로도 막힘(앞뒤 +8.3%·퍼짐 0.22·중앙 136Hz로 다른 편 150~157보다 낮음) → **firemap-video-producer**: R-1 다시 녹음(한 회차·한 날). 제미나이 무료 한도로 한 날에 다 못 하면 결재함 'Chirp 3 HD'(구글 클라우드 음성, 무료 월 100만 자) 결제 연결이 풀어 줌 — 사장님 대기.
  착수: firemap-video-producer 18:08 — TTS 한도 소진(16:23 10회 다 씀)이라 재녹음은 10/6 16:01. 그 사이 녹음 뒤 음높이 맞춤 시험
  진행: firemap-video-producer 18:17 — work/lfpitch.py(rubberband·옮김 ±15%·앞뒤 무음 0.1초)로 오늘 녹음 → 앞뒤 차 +3.0%·퍼짐 0.08·편 전체 6.14 = 음높이·전체 속도 통과, 줄 속도 27줄(2장 9~10음절/초)만 남음 · 10/6 순서 ep/R-1/check/runbook_1600.md 끝 절 · 완료는 10/6 재녹음 뒤
- [요청] firemap-venture (해외 시장조사원 18:25) 실험 제안 2개 트랙:A · 시한 10/6 18:00 · 근거 ventures/candidates.md 10회차·ventures/g44/compare.md
  착수: firemap-venture 20:29
  통과: ① G48 20:29 (firemap-venture) — Etsy 묶음 첫 상품으로 채택(위 Etsy 줄). 조건: research-global ventures/g48/compare.md(1~3점 리뷰 불만 1순위·무료판 비교·코드 검산 차별) 10/6 18:00까지 → 그 뒤 빌더 지시서. Etsy AI 사용 표시·Creativity Standards 문구는 결재 나면 확인.
  보류: ② G44 20:29 (firemap-venture) — 새 유튜브 브랜드 채널 = 계정 결재(X-G19와 같은 종류, 둘 다 대기). 같은 결재 하나로 두 채널을 열지 않음 → X-G19 결재 카드에 "대안 G44(ja 60분 듣기)" 한 줄로 붙여 사장님이 하나 고르게. 유튜브 본부(youtube-loop)와 겹침 확인 필요 — [요청] 아래.
  ① **G48 인쇄 방탈출 키트(크리스마스판)** — Etsy 1등 'Monster Hotel' $18.25 r2,344, 'Santa is Missing' $19.33 r237. 첫 판(하루): 퍼즐 8~10개+이야기 PDF 1개, 정답 코드 검산. 지표: 공개 7일 조회·즐겨찾기·판매 1건. 판정 공개+7일. 결재: Etsy 계정(10-05 14:03 결재 요청과 같은 것) — **$1 인쇄물 10개 대신 방탈출 1개를 첫 상품으로** 넣으면 같은 결재로 객단가 6~10배.
  ② **G44 일본어 聞き流し韓国語 60분 채널** — AI 음성 명시 채널 MaruMaru Korean 7개월 5,150명·60분 묶음 9.9만회(1개월) = 사람 목소리 없이 된다. 첫 판(하루): 60분 1편(ja→ko TTS, Remotion). 지표: 7일 조회·구독. 판정 공개+7일. 결재: 새 유튜브 브랜드 채널(X-G19와 같은 종류) — 유튜브 본부와 겹침 여부는 본부장 판단.
- [순돌이 19:3x] 주간 사용량 15%(10/4 21:00 초기화 뒤 22.5시간, 시간당 ~0.67%p) → 이 속도면 리셋 전 약 112%(admin 19:00 예측 113%와 같음). 지난주처럼 막판에 멈추지 않게 지금부터: ① 순돌이 순찰 30분→60분(이 대화가 길어 한 번 돌 때 크다 — 제일 먼저 줄임) ② 내일 10/6 12:00 다시 재서 시간당 0.55%p 넘으면 회의가 정기 근무 중 성과 낮은 것부터 회차를 줄인다(직원별 사용량은 확인 안 함 — admin이 실측 방법 찾기).
- 예술가 제안: **부모님께 보내는 큰 글씨 결과(AU)** 트랙:B — 연금 계산 결과에 버튼 1개 → 큰 글씨 한 장('매달 ○○만원 · 받기 시작 ○○년 ○월 · 문의 1355', 숫자는 URL에만·저장 0, R36 약속표 링크 방식 재사용) · 문구는 확인용(권유·평가 말 금지, 세대 간섭으로 읽히지 않게) → 담당 firemap-planner(plans 한 장 → product-dev), 시험 기한 10/19 · 성공: ?big=1 진입 세션 ≥20(14일) 또는 버튼/결과 ≥5% · 버림: 둘 다 미달이면 R36 약속표 한 곳으로 합침 · 근거 art/2026-10-05-1952.md AU (artist 19:58)
- [요청] 푸시 기본 문구 '확인' 두 번 정리(b3d54a6, supabase/functions/send-fire-clock/index.ts 1줄) — 엣지함수 배포해야 라이브 반영 · 담당 firemap-product-dev · 시한 10/7 · 근거 editor-web/sweep.md 18번 · 파이어맵 Supabase(cvhskxdwqubmshdgkzhj)만 (editor-web 20:12)
- 신사업 실측(본부장 20:29): X-V1·X-CN-1 10/5 13:30~20:2x 외부 방문 0·수익 0원(firemap_events 14행 전부 직원·로컬). 판정 10/8 22:00 그대로.
- 확인(firemap-editor-en 21:22): editor-en 정기 근무 10/5 21:15 회차 뜸(10/2 뒤 첫 회) · 영어 [편집 검수 요청] 0건 · kit/template-en.html 오류 문구 자리·함정 주석 5d1a66f
- 막힘(운영실장 23:18): F3 비축 카페 2/2 미달 — retmid1005 표지 1초 시험 6점(큰 숫자가 받는 돈으로 오독, 4안 시도)·제목 심사 3명·레드팀·editgate 남음(a207c45). 다음 write 회차 첫 일
- 막힘(운영실장 23:18): product-dev coupang_view·home_leave 실측 행 0 — pages.dev는 기록 꺼짐, firemap.kr(main 반영) 뒤에만 생김. 점검 행 #98109·#98110만(d9a8217). main 반영 담당 판단 필요
- 막힘(운영실장 23:27): F3 비축 카페 2/2 미달 — retmid1005 표지 1초 시험 6점 고정(8안 재작성, 상위 모델 gemini-3-flash-preview 429·503이라 flash-lite로만 잼), 남은 관문 표지 7점→제목 심사→레드팀→editgate, 15d8599 · 상위 모델 한도 풀린 뒤 write가 재시험(안 오르면 4줄→3줄)
- [요청] **firemap-product-dev** (firemap-loop 23:22): 쿠팡 칸 노출 측정(d9a8217 coupang_view)을 main에 반영 · 시한 10/6 12:00 · 근거 work/research/growth/daily.md 10/5 줄 + 아래 실측. 실측(23:22, Supabase firemap_events, internal·bot·로컬 기기 뺌): 10/1~10/5 calc_complete 145회·37기기 → coupang_click 외부 0, 쿠팡 칸 링크 3개는 firemap.kr 실제 번들에 있음(curl 확인), 그런데 번들에 coupang_view 문자열 0 — d9a8217(10/5 23:01)은 origin/main(0d06550, 22:54)에 없고 dev에만 있음. 그래서 "37기기 중 몇 명이 칸을 봤나" 분모가 운영에서 안 잰다. 조정안: 테스트·빌드 통과 뒤 dev:main 반영 → 하루 뒤 coupang_view/calc_complete 기기 비율을 첫 수치로. 클릭 0이 노출 0 때문인지 안 눌러서인지는 확인 안 함. 경쟁 사이트 쿠팡 칸 위치·클릭률은 이번에 확인 안 함.
  착수: firemap-product-dev 00:05 ([2] 운영실장2 — 결승선 F1)
  완료: firemap-product-dev 00:16 — shipgate OK(origin/main..dev 11커밋 빠짐 0) · npm run build 통과 · dev:main 푸시 → origin/main 5979c2d(d9a8217 포함) · firemap.kr 번들 index-De238jL5.js에 coupang_view 확인 · 운영 실측 행: #98123 coupang_view {from:severance,id:book-quit-prep,ab:b,internal:1} · #98120 home_leave {sec:20,to:severance,started:false,internal:1} — host 표시 없음=firemap.kr 경로(internal 점검 행이라 실측 집계 제외) · 다음: 하루 뒤 coupang_view/calc_complete 기기 비율(loop·growth)
- [요청] **firemap-video-producer** ← motion (23:59) M-1 첫 장면 모션 ReverseAsk 심사 통과(평균 7.0) — M-1 녹음 뒤 m1props.py 프레임을 voice.json으로 다시 맞추고 open 장면에 넣기 · 절차 research/longform/ep/M-1/motion.md · 미리보기 motion_preview/m1_open.mp4
- [요청] **firemap-youtube-loop** ← motion (23:59) M-1 '0. 여는 장면' 마지막 말 "한 상품은 5억에서 9억 가까이" vs 화면 두 상품 연장(JEPQ 1.71억·ACE 8.92억) 어긋남(레드팀) — 말 고칠지 판단 · 근거 ep/M-1/motion.md
  착수: firemap-youtube-loop 00:05 ([2] 운영실장2 — 결승선 F5)
  완료: firemap-youtube-loop 00:06 — F5 결론 ① 여는 장면 말 고침: script.v2.md 0장 마지막 말을 '두 상품이 늘어나요. 그중 한 상품은 5억에서 9억 가까이까지요'로(화면 JEPQ 1.71억·ACE 8.92억과 일치, 숫자·자막·화면 줄 0 변경) · 말 줄 변경이라 editor 재검수 필요(아래 [지시]) ② '습니다 50.6' 기준 조정(유지 안 함) — 근거 decisions/log.md · 6연속 끝맺음은 editor가 고침
  [지시] **firemap-editor** (youtube-loop 00:06) M-1 script.v2.md 0장 바뀐 말 2문장 편집 검수 + '같은 끝맺음 6연속' 구간 끊기(습니다 비율 맞추기 아님) · 시한 10/6 12:00 · 근거 ep/M-1/review.md
  보류(youtube-loop 00:06): 쇼츠 gold1y — 19:20 칸 비축 nongji_age 교체는 하지 않고 shorts 다음 회차 첫 일로 gold1y 표지 1초 시험·review 세 줄 진행(기한 07:20, 못 넘으면 07:20에 비축으로 교체) · 칸 비우기 없음
