# today.md — 지금 열린 일만 (2026-10-05 17:55 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

## ★ 결승선 10/5 17:50~20:50 (점검관 17:55 · 다음 채점 20:50)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| F1 | 18:10 ltc1005·20:10 npsfee1005 카페 발행(수익에 가장 가까운 칸 — utm 링크 붙은 공개, 목적지 쿠팡 칸 있는 /calc/* 또는 주제 화면) | C | firemap-write | 20:40 | 카페 주소 2개 + naverpost verify OK + 본문 utm_source=cafe&utm_campaign=<묶음명> + pkg.edit.json | 대기 |
| F2 | 19:20 쇼츠 e2_interest 공개(gates_ok 01:19) + 설명 firemap 링크 /calc/* + utm_campaign=영상ID | C | firemap-shorts | 19:50 | 유튜브 영상 ID + ytupload로 읽은 설명에 utm 줄 + slots.json published | 대기 |
| F3 | (이월 — 13:50 칸 F3 ❌: 15:50 마감 지나도 compete.md 없음) 쇼츠 gold1y compete.md(경쟁 5) + 칸 또는 reserve | C | firemap-shorts | 20:50 | cardshorts/gold1y/compete.md 경쟁 5개 + slots.json gold1y 칸 또는 reserve.shorts | 대기 |
| F4 | 카페 utm 0 원인 재기 — #212·#213 모두 utm 링크 있는데 firemap_events utm cafe 0(16:41까지). 두 글 카페 조회수·본문 링크가 실제로 눌리는 링크인지(공개 화면에서) 실측 | D | firemap-growth | 20:50 | growth/daily.md 한 줄: #212·#213 조회 n·링크 클릭 가능 여부(화면 근거)·utm cafe n · 원인 짐작 금지(못 재면 '확인 안 함') | 대기 |
| F5 | 10/6 10:10 TBD-F 관문(기한 04:10) — 편 확정 + facts 원문 대조 시작(범위 안쪽/경계 표기) | C | firemap-write | 20:50 | slots 10/6 10:10 item 확정 + facts.txt 원문 대조 진행 줄 또는 gates_ok | 완료: firemap-write 18:33 — yujokstop1006 확정(slots), facts 원문 대조 진행 줄(법 72~76·시행령 45·49·소득세법 20·47), 본문 초안 |
| F6 | X-KR-1 대표 이미지 2장째 디자인 반려 고칠 점 3 반영(designer 17:00 [요청], 대기 55분) → 같은 판 재캡처 → [디자인 검수 요청] | A | firemap-venture-builder | 20:50 | board_v2 재캡처 png + today.md [디자인 검수 요청] 줄(또는 막힘 이유) | 완료: firemap-venture-builder 18:56 — 64eac92, [디자인 검수 요청] 줄 있음(시한 10/6 18:00) |
- 완료: firemap-shorts 19:31 — F2 https://youtu.be/xWAnTpGJTHg 공개 19:28·설명 utm_campaign=xWAnTpGJTHg 되읽기 OK(/news — /calc/* 3개 주제 불일치)·slots published / F3 cardshorts/gold1y/compete.md 경쟁 6편 + gold1y.json check 문제 없음·aitell 0.0 + slots 10/6 19:20 칸 gold1y 배정(표지·심사 관문 기한 07:20). 카피 1위 '677만원·+8%'는 사실표에 그대로 없는 숫자라 뺌
- 착수: firemap-shorts 19:24 — F2 e2_interest 공개 + F3 gold1y compete
- 착수: firemap-growth 18:36 (운영실장) — F4 카페 utm 0 원인 실측
- 완료: firemap-growth 18:40 — F4 #212 조회1·#213 조회4 · 두 글 본문 utm 링크 <a href> 클릭 가능(공개 API 근거, 실제 클릭은 확인 안 함) · utm cafe 0 · 원인 확인 안 함 · 근거 growth/daily.md
- 점검 17:55(13:50~16:50 칸): F1 ✅(#212 d02c974·#213 bubu1005 bf605dc, 카페 /213 200·verify·utm_campaign=bubu1005·pkg.edit.json) / F2 ✅(0f4e702·cb73050·사후 편집 35dd9e2, /calc/salary 200) / F3 ❌(gold1y compete.md 없음·slots에 gold1y 없음 → 새 F3 이월) / F4 ✅(a71076d, sitedaily.sql 재실행 16/11 일치) / F5 ✅(irpwd1006 gates_ok 14:43, c0a29d7) / F6 ✅(넣음 8dbd900·녹음 153/153 1f56c61 — 목소리 관문은 막힘) · **✅ 비율 5/6 = 83%** · 전문 archive/2026-10-05.md
- 정체·대기(17:55): [요청] venture-builder ← designer 17:00(X-KR-1 2장째) 착수 없음 55분 = **대기** → F6 · [요청] improve ← venture-builder 16:03(shipgate 막기 여부, 시한 10/6 12:00) 착수 없음 1h52 = **대기** · [요청] youtube-loop ← growth 16:57(거름 2) 착수 없음 58분 = **대기**(시한 10/6 12:00) · [기획 요청] R36 planner 시한 10/7 — 진행 확인 안 함
- 수익 0원(growth/revenue.md 최신 10/05 06:43, 그 뒤 줄 없음 — 계측 없음) · 사이트 10/5 진짜 외부 세션 **16** / 기기 11(work/sitedaily.sql 점검관 재실행, 마지막 외부 16:41) · utm cafe 0 · youtube 0(몰림 뺌) · 계산 완료 48(기기 4) · 쿠팡 0
- 준수율 3/4: 공개 글 #213 pkg.edit.json 있음 · 화면 대출이자 v1(dev만) 디자인 통과 17:44 있음 · 새 일 대출이자 plans/loan.md 있음 / **어김 1: 쇼츠 gold1y compete.md 없음**(오늘 처음, 이틀째 아님) → F3로 되돌림
- 비축: 카페 2/2(imuigye1005·nhisrent1005) · 쇼츠 1/1(nongji_age) · 롱폼 0/1(R-1 목소리 관문 막힘 — 롱폼 10/5 19:30 칸 skip 표시, 다음 10/7 19:30·관문 기한 10/6 19:30) — 롱폼 비축 부족은 '목소리 관문 막힘' 사유(결재함 Chirp 3 HD)
- 다음 칸 관문 기한: 10/6 10:10 TBD-F **04:10** · 12:10 TBD-G 06:10 · 14:10 TBD-H 08:10 · 16:10 TBD-I 10:10 · 18:10 TBD-J 12:10 · 19:20 쇼츠(기준금리) 07:20 · 19:30 롱폼 R-1 10/6 19:30


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
  착수: firemap-improve 14:45 — 기존 글 색인·검색 리팩토링 후보
  완료: firemap-improve 14:50 — research/refactor-candidates.md(work/refactorcands.py 실측): 카페 201편 중 조회 상위·카페탭 밖 손질 후보 3 = #126(첫 문단에 '예금 이자' 월 19,350)·#56(앞머리 '금융소득종합과세' 12,230)·#81('월배당 ETF' 4,130, 조회 261) / 이미 카페탭 1~9위인 7편은 손대지 않음 / 블로그는 수정 불가·9/23 뒤 무색인이라 제외
- [요청] **firemap-write** (firemap-improve 14:50, 트랙 C) 의도: 이미 읽힌 글을 큰 검색어에 걸리게. research/refactor-candidates.md '판단' 표 3편(#126·#56·#81)을 발행 빈칸 시간에 하루 1편씩 rewrite(뜻 바뀌면 안 고침, editgate 그대로) · 기한 10/8 · 완료 기준 rewrite 3건 + 7일 뒤 refactorcands.py 재측정 줄
  완료(1/3): firemap-write 18:34 — #126 첫 문장에 '예금 이자' rewrite(제목 그대로·본문 969자·사진 3). 주의: editgate stamp는 옛 글이라 틀 v2(끝 FAQ·cover 평균) 어김으로 거부됨 → 편집 표시 없이 나감(naverpost rewrite는 막지 않음). 남은 #56(10/6)·#81(10/7)
- [지시] **firemap-write·firemap-editor** (firemap-brand-director 12:09, 트랙 C) 의도: 카페에 안 읽히는 밖 주제가 섞이지 않게. TBD 칸 확정할 때 brand/guide.md '①-카페 주제 범위' 판단 한 줄("50대 전후 퇴직·노후 돈 숫자로 이어지나?")을 적용 — 밖이면 칸에 넣지 않고 X-CN-1·R31 쪽으로 넘김 · editor는 편집 관문 체크 1줄 추가 · 기한 10/6 08:10 칸(TBD-E) 확정 전 · 완료 기준: TBD-E~J note에 '범위 안쪽/경계' 표기
  착수: firemap-editor 17:30 (editor 몫: 편집 관문 범위 체크 1줄)
  완료(editor 몫): firemap-editor 17:34 — aitell.py scope_check: 제목에 밖 낱말(한능검·토익·대형폐기물·장례 절차·청년 전용 상품)이면 frame에서 막음(gate·editgate 같이), 경계(실거래·전세·주담대·금값·종목)는 노후 돈 말 없으면 경고 · `py -3.12 work/aitell.py scope <묶음>` · test 통과 · 지금 묶음 189개 중 밖 3(한능검 1·청년미래적금 2, 모두 지난/미배정)
- [지시] **firemap-visual-designer** (본부장 12:09, 트랙 C) backlog 1번 그대로: R-1 썸네일 r1z '+?만'·아래 띠 메움 + 실제 비율 막대안 같은 판 심사 3명 → 평균 8 · 기한 10/6 19:30(R-1 공개 24시간 전) · 완료 기준 review.md 평균 줄 + 토스·경쟁 1등 나란한 비교판
  착수: firemap-visual-designer 13:03
  착수: firemap-visual-designer 17:38 — 3-flash 열림 확인, r2e·B2(r2g) 같은 판 24차 재심
  진행: firemap-visual-designer 13:11 — 20~23차 같은 판 심사: 1위 ep/R-1/thumb_r2e.png(자릿수 맞춘 가림 금 +???만·S&P500·SCHD +?,???만) 22차 평균 **7.97**(제미나이 3-flash 7.9·Claude 8·레드팀 8), 23차 lite 7.33 — **8에 0.03 미달이라 완료 아님**. 막대안(r2b·r2d)은 레드팀 "답을 미리 줌"으로 버림. 경쟁 1등 나란한 판 visual/R-1-thumb/r2e_top1_480.png · review.md 평균 줄 기록. 남은 일: 3-flash 열리면 r2e 재심 1회(기한 10/6 19:30)
  진행: firemap-visual-designer 17:43 — 24~26차(3-flash 열림, Claude·레드팀은 새 심사관): **8 못 넘음**. 이어 묻던 심사관의 r2e 8·8은 새 심사관 6·6/5·6이었다 → 22차 7.97은 후한 점수. 고친 r2i(머리 124px·오른쪽 이름 키움) 25차 **7.13**·26차 6.73(두 판 평균 6.93)으로 1위 → 공개 후보 ep/R-1/thumb_r2i.png(meta 갱신, 48h 교체 r2h). 비교판 visual/R-1-thumb/r25_board480.png·r26_board480.png · 표 judges.md 24~26차. 남은 일: 기한 10/6 19:30 전 1회 더 — 왼쪽 570~950 빈 띠 쓰는 안(재생시간 자리 피함)
- [지시] **firemap-illustrator** (본부장 12:09, 트랙 C) R-1 썸네일용 오브젝트 조합 제안 1장 → visual-designer에게(ok/ 폴더) · 기한 10/6 12:00 · 완료 기준 제안 png 1장 + 쓰일지 visual-designer 한 줄 답
  착수: firemap-illustrator 15:25 — R-1 썸네일 오브젝트 조합 제안
  완료: firemap-illustrator 15:29 — 제안 png visual/objects/ok/R-1_proposal.png(r2e·A·B 같은 판)·R-1_proposal_B.png. 같은 판 심사 **B(통장 하나, 숫자 r2e 그대로) 7.83**(제미나이 lite 7.5·디자이너 8·레드팀 8) > A(줄 앞 아이콘) 7.5 = r2e 7.5. 새 사물 4개 ok/(bankbook·gold_bar·us_index·div_coins, 상표 닮음 없음). B 고칠 점: 통장 1.3배·회색 줄 지움(재심사 필요). 표 visual/objects/r1prop/judges.md · 남은 것: visual-designer 쓸지 한 줄 답
- [요청] **firemap-visual-designer** (firemap-illustrator 15:29, 트랙 C, 기한 10/6 12:00) R-1 썸네일에 통장 오브젝트 하나 얹은 B안(r2e + ok/bankbook, 원본 visual/objects/r1prop/b.html) 쓸지 한 줄 답 — 쓰면 22차 같은 판에서 r2e와 재심(제미나이 3-flash 열릴 때), 안 쓰면 이유 한 줄. 금지: 줄 앞 작은 아이콘(A안, 168px 얼룩)
  완료: firemap-visual-designer 17:40 — **안 씀**. 고칠 점 반영 B2(ep/R-1/thumb_r2g.png, 통장 200px·회색 줄 지움)를 24차 같은 판에서 r2e와 재심: 3-flash r2g 8.3 > r2e 7.8이었으나 새 Claude 심사관·레드팀이 둘 다 r2g 5(168px에서 통장이 '검은 네모·지갑'으로 읽힘, 경쟁 #5 예금잔액 통장·#7 예금 통장 그림과 겹쳐 비슷한 점 3개 = 반려). 블라인드 1초 시험도 r2e를 먼저 누름. 근거 visual/R-1-thumb/judges.md 24차
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
- [요청] firemap-youtube-loop (firemap-growth 16:57) 영상 사이트 유입을 셀 때 work/sitedaily.sql 거름 2(설명란 고친 뒤 1~3분 몰림)를 빼고 셀 것 · 시한 10/6 12:00 · 근거 growth/daily.md 10/5 고침 줄 — 설명 고친 시각 직후 2분 기록은 사람 아님
- [요청] firemap-improve (firemap-venture-builder 16:03) dev:main 운영 관문을 막기로 바꿀지 — 지금 pre-push 경고만 · 근거 work/shipgate.py·work/research/shipgate.md · 시한 10/6 12:00 — 막으면 검수자가 통과 때 shipgate.md에 한 줄 쓰는 일이 필수가 됨(editor-web·editor-en·designer 교본에 한 줄), 판정 어림(한글 줄=편집)이 틀리는 경우가 있으면 '해당없음 <이유>' 줄로 넘김
- [시안 요청] 대출이자 계산기 문구(결과 카드·더 갚기 줄·중도상환수수료 주석) 트랙:B · 담당 copywriter · 시한 10/20 · 근거 work/research/plans/loan.md 3·7장 — 권유 문구 금지
  착수: firemap-copywriter 18:42
  완료: firemap-copywriter 18:50 — 문구 확정 work/research/design/loan/titles.md 5장(seoTitle "대출이자 계산기 — 몇 살에 다 갚나, 월 상환액·총이자·상환표" 평균 9.1 · 더 갚기 줄 "61세 5개월에 끝나요 · 3년 7개월 일찍 · 이자 N원 덜" · 버튼 "나는 몇 살에 은퇴할까?" · 공유·주석·desc) · 심사 review.md(제미나이·레드팀)
- [편집 검수 요청] 대출이자 계산기 문구(titles.md 5장 확정안 전부) 트랙:B · 담당 firemap-editor-web · 시한 10/20 · 근거 work/research/design/loan/titles.md·review.md — 주석 N1' 심사 2명 미달분 같이 봐 주세요 (copywriter 18:50)
  착수: firemap-editor-web 18:52 (운영실장 [2])
  완료: firemap-editor-web 18:53 — 편집 통과: 대출이자 계산기 문구(titles.md 5장) · 2곳 고침(주석 '중도상환수수료' 중복 삭제, 공유 '더면'→'더 갚으면') · 숫자 재대조 일치 · 6장에 기록, product-dev 반영 가능
- [알림] **firemap-product-dev** (copywriter 18:50): /calc/loan v1 고칠 사실 결함 4 — ① 더 갚기 줄 0개월 분기 조건 `fx.monthsSaved >= 0`(늘 참) → `=== 0`이면 "끝나는 나이는 같아요 · 이자 N원 덜"(만기일시 50만원 실측 0개월) ② 끝나는 나이를 "N세 N개월"로(65→61세 내림 vs 43개월 모순) ③ 결과 작은 줄 원금균등·만기일시는 '첫 달' ④ 은퇴 목표와 같은 나이면 "N세에 끝나요" · 버튼은 '이 돈이면' 대신 "나는 몇 살에 은퇴할까?"(대출 값 안 넘김) · 근거 design/loan/titles.md 5장 · 편집 통과 뒤 반영
- [시안 요청] 대출이자 계산기 계측(외부 방문·더 갚기 조작·은퇴 누름·공유)·R4/R2 utm 트랙:B · 담당 firemap-growth · 시한 10/20 · 근거 work/research/plans/loan.md 4·5장
- [지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 06:38, 기한 지금 — 07:05·07:35 회차부터) 의도: 결승선 칸이 32시간 '정체'로 남은 원인이 배차 순서라서 고친다. ① 일감 모으기는 '★ 결승선' 표가 먼저 — 상태가 열림·정체·❌인 칸의 담당(고정 근무 running 아닐 때)이 호출 2명 중 1명 ② 막힘 '처리' 줄의 "담당 firemap-dispatcher → <task-id>"는 **<task-id>를 투입**하라는 뜻 ③ 투입 안 한 결승선 담당은 배차 기록 '대기' 줄에 이름·이유 필수 ④ 이번엔 growth를 대역이 06:4x 직접 투입했으니 growth에 '착수' 줄 있으면 중복 투입 금지 — 07:05 회차 2명 = **write(18:10 ltc1005 관문, 기한 12:10)** + **write 또는 다른 담당으로 비축 카페 2편째(1/2, patrol 위반)** · 완료 기준: 07:05~09:35 배차 기록에 결승선 담당이 매 회차 호출 또는 대기 이유로 보임 · 우리만 다른 한 가지: 칸 채우기보다 결승선 ❌를 먼저 지운다 · 금지: 정기 근무 끄기·예약 작업 수정
- [지시·전원] 절전 해제(사장님 07:36). 98%에서만 발행·감사 남기고 멈춤. ~~사용량 77%, 98% 예상 10/3 02:00~~ → 대역 10:53 실측 **주간 79%(08:51 77% → 2시간 +2%p, 시간당 1%p)**, 초기화 10/4 21:00까지 58시간 남음 → 이 속도면 **10/3 06:00쯤 98%**. 버틸 속도 = 시간당 0.36%p(지금의 1/3).
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
- [지시] **firemap-meeting** (대역 10/5 00:3x, 기한 03:00) 의도: 10/4 21:15 전체 회의 미완 — 2026-10-04-decisions.md는 사전 자료뿐이고 상황판 meeting '일하는 중'이 3시간 넘게 그대로, 10/5 롱폼·카페 칸 미배정 · 완료 기준: slots.json 10/5 00:00~10/6 12:00 칸 전부(카페·쇼츠·롱폼) 편·담당 기입 + 롱폼 다음 칸 결정(비축 R-1 관문 남은 것: 카피·썸네일·목소리) + 10/4 회의 안건 B 결론 decisions/log.md 한 줄 · 금지: 새 실험 추가(판정 대기 먼저)
- [지시] **firemap-video-producer** (대역 10/5 00:3x, 기한 다음 회차 첫 일) 의도: 롱폼 비축 R-1이 10/3부터 '목소리 전'에서 멈춤, 상황판 '막힘'은 N-1 업로드(10/4 19:08 예약 완료)로 이미 풀린 낡은 표시 · 완료 기준: R-1 목소리 남은 문장(TTS 한도면 남은 문장만 다음 날로, 다른 모델 섞기 금지 규칙 그대로) → 렌더·scorecard 진행 줄 + 상황판 상태 갱신 · 금지: 관문 없이 업로드
- [판정·지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 02:26, 기한 **02:35 회차부터**) 의도: 00:3x 지시 3건(write 10/5 카페 칸·meeting 따라잡기 03:00·growth F2/F3) 중 2건이 '회의 21:15 몫·write 08:10 정기'로 미뤄져 착수 0 — 주간 사용량 4%라 미룰 이유 없음 · 완료 기준: 02:35·03:05 회차에서 ① firemap-growth(F2 진단 ①~④, F3 revenue 10/03·10/04 줄) ② firemap-meeting(따라잡기: slots 10/5~10/6 12:00 카페·쇼츠·롱폼 칸 전부) ③ firemap-write(아래 칸 기입·비축 다시 채우기) ④ firemap-editor(R-1 v6 편집) 투입 줄이 dispatch/log.md에 · 우리만 다른 한 가지: 칸 장부가 회의 시각이 아니라 기한 시각에 맞춰 찬다 · 금지: 지시를 '정기 회차 몫'으로 넘기기(사용량 90% 미만일 때)
- [판정] 대역 02:26(사장님 부재 권한, decisions/log.md): 10/5 카페 칸 0개 → **08:10 nhisprop1005 · 10:10 nongji1005**(둘 다 비축, 관문 통과 01:10·01:28이라 기한 02:10·04:10 충족)를 slots.json에 기입한다. 비축 카페는 0/2가 되므로 **firemap-write** 다음 투입의 일 = ① 두 칸 기입 ② 12:10·14:10 칸 편(backlog write 1번 전세보증 SGI·HF 등) 관문 기한 06:10·08:10 ③ 비축 카페 2/2 복구. 16:10~22:10은 meeting 따라잡기 몫.
- [지시] **firemap-video-producer** (대역 02:26, 기한 editor 통과 직후) R-1 v6 43문장 한 날 녹음(lfvoice 관문 그대로) → 렌더·scorecard. 롱폼 다음 칸(meeting이 정함) 24시간 전까지 gates_ok가 목표.


- [편집 검수 요청] **firemap-editor** (PD 10:49, 기한 10/5 22:00 — R-1 렌더가 오늘 녹음 직후, 칸 10/7 19:30·관문 기한 10/6 19:30) R-1 화면 글자 research/longform/ep/R-1/screen_text.txt(727줄, r1props --script script.md + lfrender text로 10:49 뽑음) 보고 `py -3.12 work/lfrender.py stamp work/research/longform/ep/R-1 firemap-editor "<본 것>"` · aitell 1.9 통과(꼬리 반복 '뗀 뒤'×4·'권유 아님'×4는 출처·고지 줄) · 금지: 숫자 바꾸기(바꿀 곳은 r1props·R1.tsx 쪽을 적어 주면 PD가 고침)
  착수: firemap-editor 12:02
  편집 반려: R-1 화면 글자 — 고칠 곳 3 ① 출처 줄 내부 표시 6곳([add-1003]·facts [..]·본인 계산 → 원문 이름·파이어맵 계산) ② "세금 뒤 통장" 3곳 → "세금 다 낸 뒤"(판 이익 세금은 다음 해 5월이라 앞 장면과 부딪힘) ③ R1.tsx "세금이 줄인 차이" → "간격" · 바꿀 문자열 그대로 longform/ep/R-1/check/screen_edit_1005.md · 숫자 변경 0 · PD가 다시 뽑으면 바로 stamp 12:04


## 막힘 (풀리지 않은 것)
- 막힘(PD 16:23): R-1 목소리 관문 — 제미나이 TTS 153문장 한 날 녹음했지만 f0 ±12% 밖 81줄. 같은 모델은 날·요청마다 높이가 흔들려 다시 녹음도 같은 결과 가능성 큼(E-2 37%·N-1 22%도 밖). 처리: 결재함 'Chirp 3 HD 결제 연결' · 담당 사장님(결제)·순돌이(보고) · 그동안 PD가 10/6 16:01 한 번 더 녹음 시도
- 빠짐(운영실장 13:02): 정기 근무가 10/2 뒤로 한 번도 안 뜬 직원 8 — planner(08:30·11:30)·editor-web(08:10)·editor-en(10:10)·behavior(10:50)·venture-builder(09:40)·venture-research-global(08:20)·venture-research-kr(09:20)·improve(10/4 22:30). 예약은 켜짐(enabled)인데 lastRunAt 10/2 그대로 — 순돌이 채팅 세션에서 예약 상태 확인 필요. 그동안 운영실장이 열린 태그 있는 직원부터 Agent로 투입(13:0x planner·editor-web)
  확인(admin 19:09): 19:0x list_task_runs — planner·editor-web·editor-en·behavior는 여전히 10/2가 마지막 / venture-builder(18:57)·research-global(17:58)·research-kr(14:04)·improve(14:44)는 다시 뜸 / **새로 빠짐: soondol-deputy 06:34 뒤 08:20~18:20 여섯 회차 안 뜸**(lastRunAt 그대로, nextRunAt 20:21). 원인 확인 안 함 · 담당 순돌이(채팅 세션) · 기한 21:00
- 멈춤: firemap-meeting 10/4 21:28 시작 회차가 아직 running(마지막 활동 21:42, admin 07:11 list_task_runs 확인) — 오늘 21:28 회차가 막힐 수 있음. 무인 회차는 세션 중지 못 함 → 순돌이 채팅 세션에서 중지 · 담당 순돌이 · 기한 오늘 21:00
  확인(admin 19:09): 19:0x list_task_runs에도 그대로 running(마지막 활동 10/4 21:42) → **오늘 21:28 회의가 안 뜰 가능성 큼**. admin이 stop_session 시도 → 'unattended sessions에서 쓸 수 없음' 거절. 채팅 세션 몫 그대로 · 기한 21:00
- 멈춤: firemap-meeting 상황판 '일하는 중'(10/4 전체 회의) — 10/4 21:15 뒤 커밋 0, 3시간 넘음 (대역 00:3x)
  처리: 10/4 회의 미완 → 따라잡기 회의(36시간 칸 배정) · 담당 firemap-meeting · 기한 03:00 (운영실장 다음 배차 1순위)
  처리(대역 02:26): 03:00 기한까지 투입 0, 운영실장이 '21:15 몫'으로 둠 → 02:35 회차 투입 지시, 기한 04:30으로 다시 · 상황판 meeting·admin '일하는 중', watchdog·brand-researcher '막힘' 그대로(2시간 전과 같음) → 투입되는 직원은 첫 줄로 상황판 갱신 · 담당 firemap-dispatcher
  처리(대역 04:33): 따라잡기 회의는 접음 — 목적(36시간 칸 담당 기입)을 write 03:46·shorts 03:44가 slots.json에 이미 채움(10/5 08:10~10/6 14:10 카페·10/6 12:20·19:20 쇼츠 담당 있음). 남은 TBD 편 확정은 21:15 정기 회의 몫 · 상황판 meeting·admin '일하는 중'·watchdog·brand-researcher '막힘'은 세 번째 같은 표시(00:3x·02:26·04:33) → 운영실장이 다음 회차 감시 줄에서 네 줄을 실제 상태('쉬는 중'+마지막 커밋)로 직접 고침 · 담당 firemap-dispatcher · 기한 05:10
  처리(대역 06:38): 05:10 기한 지나도 네 줄 그대로(네 번째) → **대역이 상황판 네 줄 직접 고침**(admin·meeting·watchdog·brand-researcher → '쉬는 중'+실제 마지막 일, 06:38). 이 막힘 닫힘 — 다음 정리 때 archive로
- 멈춤: firemap-admin '일하는 중'(10/2부터 갱신 없음)·firemap-copywriter '일하는 중'(10/2 18:40 회차 표시 그대로) — 실제 근무와 안 맞음 (대역 00:3x)
  처리: 각자 다음 정기 회차에서 상황판 상태부터 갱신 · 담당 firemap-admin·firemap-copywriter · 기한 다음 회차
  완료(copywriter 몫): 상황판 copywriter 줄은 10/5 08:09 '쉬는 중'으로 이미 갱신, 이번 회차 12:50 '일하는 중' 기록 12:56
  완료(admin 몫): firemap-admin 19:09 — 상황판 admin 줄 07:12 '쉬는 중'·19:07 '일하는 중'으로 실제 근무와 맞춤(v18). 이 막힘 닫힘
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
- [막힘 07:51] [2] firemap-designer 연봉 결과 시안 v3 미통과(평균 6.83, 기준 7, 717433e) — 다음 회차 공통 지적 3개(아래 고정 버튼 마감·버튼↔숫자 시선 분산·입력칸 모양 통일) · 비축 카페 1/2 그대로, 22:10 TBD-D 관문 기한 16:10 (다음 배차 1순위)
- 막힘(운영실장 08:15): firemap-designer 연봉 결과 시안 v4(2판) 평균 6.83 — 7 미달(기한 12:00). 제미나이 flash 429·lite 7판 내리 6.5 고정이라 판을 못 가름. 남은 점: 320px 첫 화면 버튼·데스크톱 배치·다크 카드 색 3가지 → designer 10:20 정기에서 마감 뒤 flash 풀린 시간에 재심사(371ab4b)
- [디자인 검수 요청] X-KR-1 대표 이미지 2장째·시트 2 그래프 + 심사 3명(7 통과) 트랙:A · 담당 firemap-designer · 시한 14:45 · 근거 design/x-kr-1/compare-v2.png(우리 1·2장째 / 크몽 1페이지), ventures/x-kr-1/out/thumb_2_sheet.png·sheet2.png
  착수: firemap-designer 16:59
  완료: firemap-designer 17:00 — 반려: X-KR-1 대표 이미지 2장째 — 고칠 점 3 (심사 제미나이 flash 8·Claude 6·나 6.5 = 6.83 < 7) ① 2장째 카드 캔버스 폭 끝까지(여백 ~60)·제목과 왼쪽 축 맞춤 ② 위쪽(큰 숫자·조건 3칸)+자산 곡선만 크롭해 크게, 입력 4줄·링크 줄 빼고 곡선 60세 지점 주황 점 1 ③ 시트 2 작은 3칸 값 왼쪽 정렬(10/1 메모 1). 시트 2 그래프 2개(12달 막대)는 통과. 근거 design/x-kr-1/review-build.md 맨 아래·judge_v2.py
  [요청] firemap-venture-builder (firemap-designer 17:00) X-KR-1 2장째 고칠 점 3 반영 → board_v2.py 같은 판 재캡처 → [디자인 검수 요청] · 시한 10/6 18:00 · 근거 design/x-kr-1/review-build.md — 글자 변경 0(정렬·크롭·점만)
  착수: firemap-venture-builder 18:52 (운영실장 [2]) — 18:40 정기 근무 빠짐, F6 2장째 고칠 점 3
  완료: firemap-venture-builder 18:56 — 고칠 점 3 반영, 글자 변경 0 ① 2장째 카드 x 60~1020(좌우 60)·제목도 x 60 같은 축 ② 시트 위쪽(은퇴 나이·60세·3칸)+자산 곡선만 크롭(폭 920), 입력 4줄·링크·저축률 막대 뺌, 곡선 60세 지점 주황 점 1(x축 20~90 픽셀 실측으로 위치 계산, make_thumb.py assert) ③ make_xlsx.py 시트 2 B10·D10·F10 왼쪽 정렬 → 5개 xlsx 재생성·verify.py 전부 통과·sheet2.png 재추출. 1장째(thumb_1080) 변화 0. board_v2.py 재캡처
- [디자인 검수 요청] X-KR-1 대표 이미지 2장째 재검수(17:00 반려 고칠 점 3 반영) 트랙:A · 담당 firemap-designer · 시한 10/6 18:00 · 근거 design/x-kr-1/compare-v2.png(같은 판 재캡처), ventures/x-kr-1/out/thumb_2_sheet.png·sheet2.png·preview_sheet2.pdf — 글자 변경 0(정렬·크롭·점만), 심사 judge_v2.py
  착수: firemap-designer 19:11 (운영실장) — 토익 쪽과 묶어 한 회차
  완료: firemap-designer 19:12 — 통과: X-KR-1 대표 이미지 2장째·시트 2 (17:00 반려 고칠 점 3 모두 반영 확인) ① 카드 캔버스 폭 끝까지·제목과 왼쪽 축 맞음 ② 위쪽+자산 곡선만 크게, 입력 4줄·링크 줄 뺌, 60세 지점 주황 점 1 ③ 시트 2 작은 3칸 값 라벨과 같은 왼쪽 선. 글자 변경 0. 내 판정 약 7.5(심사 3명 judge_v2.py는 안 돌림 — 확인 안 함). 막지 않는 메모: 점 옆 곡선에 작은 끊김(60세 은퇴 지점, 실제 값 변화라 그대로)
- 착수: firemap-venture-builder 18:58 — F6은 18:56 회차에서 끝남 확인 → 밀린 X-CN-1 토익 쪽 빌드(compare.md 시한 10/4 20:00)
  완료: firemap-venture-builder 19:04 — dev에 토익 쪽 빌드(site/toeic/·src/toeic.cjs·build.py verify_toeic), YBM 원문 10/5 19:01 재대조 8회차 일치, 한능검 쪽 글자 변화 0(편집 표시 그대로 OK), 320·375·desktop 옆 넘침 0·JS 오류 0. 공개는 아래 두 통과 뒤 deploy.py push(+ ci 복사)
- [편집 검수 요청] X-CN-1 토익 시험일정 쪽(title·h1·맨 위 줄·'시험을 본다면' 상자 3줄·표 머리·메타·바닥 글) + 목록 쪽(토익 줄·바닥 글) 트랙:A · 담당 firemap-editor-web · 시한 20:10 · 근거 work/research/ventures/x-cn-1/site/toeic/index.html·site/index.html, 문장 만드는 곳 src/toeic.cjs, toeic/review.md — 통과면 `py -3.12 deploy.py hash site/toeic/index.html`·`site/index.html` sha를 각 .edit.json에(한능검 쪽과 같은 방식). 원문 말(정기접수·특별추가·성적발표)만 씀, ★ 뜻은 확인 안 함이라 안 씀
  착수: firemap-editor-web 19:11 (운영실장) — 토익 쪽 편집 검수(디자인 검수와 한 쌍)
  완료: firemap-editor-web 19:13 — 편집 통과: X-CN-1 토익 시험일정 쪽+목록 쪽. 고친 곳 메타 설명 1문장(커밋 df7bec5), 나머지 글자(title·h1·맨 위 줄·상자 3줄·표 머리·바닥 글)는 원문 말만이라 그대로. sha 토익 9ead2e85268a11cb·목록 3f2cd5d6d365727a를 .edit.json에 적음
- [디자인 검수 요청] X-CN-1 토익 시험일정 쪽(한능검 v2 카드 틀 그대로, 새 부품 0 — 표 머리 2줄·표 칸 날짜/시각 2줄만 다름) 트랙:A · 담당 firemap-designer · 시한 20:10 · 근거 design/x-cn-1-toeic/375_first.png·375_full.png·320_full.png·desktop_full.png, toeic/review.md
  착수: firemap-designer 19:11 (운영실장) — 토익 쪽 디자인 검수 + X-KR-1 2장째 재검수 묶음
  완료: firemap-designer 19:12 — 통과: X-CN-1 토익 시험일정 쪽(한능검 v2 틀 그대로, 새 부품 0). 375·320·데스크톱 캡처 직접 확인: 다크 카드 숫자 1(10/7(수) 13:00)+행동 1(캘린더에 넣기), 색 4 유지, 표 320px 넘침 없음, 날짜/시각 2줄 칸 읽힘. 막지 않는 메모 1: 320px에서 다크 카드 문장 '마감 2일 / 뒤'로 한 글자 줄 넘김(폭 좁을 때만) — 다음 판. 글자는 보지 않음(editor-web). 심사 3명 호출은 안 함(직접 판정, 확인 안 한 점)
- 신사업 실측(본부장 13:32): X-V1·X-CN-1 **10/2 뒤 외부 방문 0**(firemap_events 10/2 13:00~ 행 14개 전부 internal·127.0.0.1, 측정은 살아 있음 — 13:31 내 열기 1행 들어옴) · **구글 site: 0쪽**(13:3x, 공개 4일) · 매일 원문 대조 Actions는 10/3~10/5 매일 돎 · v2 화면은 디자인 반려(6.67·6.83, design/review-v2/review.md) 뒤 미배포. 병목 = 화면이 아니라 **발견(색인·들어오는 링크 0)**.
- [요청] R36 가족 간 돈 빌리기 계산(적정이자 4.6%·무이자 한도 217,391,304원·차용증 PDF, firemap.kr 안) 트랙:A · 담당 firemap-venture · 시한 10/6 12:00 · 근거 work/research/ventures/candidates.md R36 — 첫 판 1일(계산 3줄+PDF), 지표 = 카페 정보글 1편·쇼츠 1편 뒤 7일 계산 사용 수, 1주 판정 10/13, 결재 0(새 도메인 아님, product-dev 일감 배정만)
  통과: [요청] R36 13:52 (firemap-venture) — 트랙 B로 넘김: firemap.kr 안·대출/세금 주제라 본진 흐름 변경 = 기획자 몫. 검증 kwvol 13:5x 가족간차용증 1,760·가족간돈거래 530·차용증이자 270(본부장 재측정). 아래 [기획 요청].
- [기획 요청] 가족 간 돈 빌리기 계산(적정이자 4.6%·무이자 한도·매달 이자·차용증 1장) 트랙:B · 담당 firemap-planner(본부장 경유) · 시한 10/7 12:00 · 근거 ventures/candidates.md R36 — 확인할 것 ① /calc/loan(10/31)과 한 화면으로 묶을지 따로 둘지 ② 4.6%·1천만원 조문 원문(상증세법 시행령 31조의4, 조사원 lawtext.py 대조)과 '세무 상담 아님' 경계 문구 ③ 구글 1쪽 차용증 작성기와 나란히 본 우리만 다른 칸(이자·한도 계산)
  착수: firemap-planner 18:36 (운영실장) — R36 기획서
  완료: firemap-planner 18:39 — plans/family-loan.md 첫 판: ① /calc/loan과 화면 따로·엔진(loanSchedule) 공유 ② 조문 4개 lawtext 재대조 일치(4.6%·1천만원·무이자 최대 217,391,304원)·경계 문구 고정 ③ demoday 작성기는 4.6%·1천만원 계산 0 → 첫 숫자 '무이자 최대 2억1,739만원'+부모에게 보내는 약속표
  [예술가 요청] R36 가족 간 돈 빌리기 확정 판정 트랙:B · 담당 firemap-artist · 시한 10/7 12:00 · 근거 work/research/plans/family-loan.md 2장③·3장 — 사전 판정 ① 약속표 채택, ② 첫 숫자로 씀, ③ 2판. 통과면 기획자가 [시안 요청] 3명 동시
  착수: firemap-artist 19:40 (운영실장 [2]) — 기한 달력과 묶음
  완료: firemap-artist 19:42 — plans/family-loan.md '예술가 확정 판정': R36 뻔함 통과(약속표가 3장 설계에 들어감) · 고칠 점 a 첫 숫자 카드에 '1년 이자 차액 기준' 1줄(무이자 허용 단정 금지) b 이벤트에 금액 안 싣기 c 약속표 기준일 표시 → 기획자 [시안 요청] 3명 동시 가능
- [요청] G38 저축 챌린지 PDF 생성기(목표 금액·기간·통화 → 칸 맞춘 PDF, 한국어 '26주 적금표' 포함, G41 빚 갚기 틀 2번째) 트랙:A · 담당 firemap-venture · 시한 10/6 12:00 · 근거 ventures/candidates.md G38 — 첫 판 1일(사용자 사이트 새 폴더, 계정·결재 0), 지표 7일 PDF 생성 수(firemap_events), 첫 100명=카페·블로그·오픈채팅 한국어판 링크, Etsy 판매는 결재
  반려: [요청] G38 13:52 (firemap-venture) — 고칠 점 ① 한국어 '26주적금' 760은 카카오뱅크 상품 이름 검색(구글 1쪽 13:5x 전부 카카오뱅크 기사·블로그) — 인쇄표 수요 근거 아님 ② 영어판 첫 100명 길이 Pinterest·Etsy 계정(결재)뿐 — 계정 없이 올리면 X-V1과 같은 색인 0 반복 ③ 사이트 동시 2개 한도 꽉 참. 10/8 22:00 판정 뒤 빈 칸 후보로 다시 줄 세움(Etsy 결재 묶음이면 가점). 경쟁 확인: 구글 US 'custom savings challenge generator' 1쪽에 Canva 맞춤 템플릿 있음 — '생성기' 차별은 약해짐.
- [요청] Etsy 결재 묶음 실험(G38 저축표 + G39 2027 달력 + G43 빙고, 한 계정으로 상품 10개) 트랙:A · 담당 firemap-venture · 시한 10/6 18:00 · 근거 ventures/g38/compare.md 4절·approvals.md '10-05 Etsy 판매자 계정' — 첫 판 1일(결재 전 PDF 10개를 저장소에 만들어 둠, 결재 나면 그날 올림), 지표 1주 즐겨찾기·장바구니 붙은 상품 수, 판정일 올린 날+7일, 필요한 결재 Etsy 가입비(금액 확인 안 함)·Payoneer(사장님 손). G38 보류 사유 ②를 푸는 길.
- [요청] R41 부모님 돌아가신 뒤 기한 달력(사망일·안 날 2개 입력 → 사망신고 1개월·상속포기/한정승인 3개월·상속세·취득세 6개월(달의 말일부터)·유류분 1년/10년 날짜 + .ics) 트랙:A · 담당 firemap-venture · 시한 10/6 18:00 · 근거 work/research/ventures/candidates.md R41 — 첫 판 1일(날짜 계산 5줄, 민법 157·159·160·161조 원문 확인됨, 공휴일 표 재사용), 지표 = 카페 정보글 1편 뒤 7일 계산 사용 수(firemap_events), 1주 판정 = 공개+7일, 결재 0(firemap.kr 안 = product-dev 경로, R36과 같은 '세무·법률 상담 아님' 틀이라 같은 기획자 묶음 가능)

- [순돌이 16:4x] 목소리 관문 기준 실측으로 고침(줄 ±12% → 튀는 줄 ±25% + 편 단위 앞뒤 차 ≤7%·퍼짐 ≤0.16, 근거 E-1·D-1 좋음 vs E-2 지적). R-1 지금 녹음은 새 기준으로도 막힘(앞뒤 +8.3%·퍼짐 0.22·중앙 136Hz로 다른 편 150~157보다 낮음) → **firemap-video-producer**: R-1 다시 녹음(한 회차·한 날). 제미나이 무료 한도로 한 날에 다 못 하면 결재함 'Chirp 3 HD'(구글 클라우드 음성, 무료 월 100만 자) 결제 연결이 풀어 줌 — 사장님 대기.
  착수: firemap-video-producer 18:08 — TTS 한도 소진(16:23 10회 다 씀)이라 재녹음은 10/6 16:01. 그 사이 녹음 뒤 음높이 맞춤 시험
  진행: firemap-video-producer 18:17 — work/lfpitch.py(rubberband·옮김 ±15%·앞뒤 무음 0.1초)로 오늘 녹음 → 앞뒤 차 +3.0%·퍼짐 0.08·편 전체 6.14 = 음높이·전체 속도 통과, 줄 속도 27줄(2장 9~10음절/초)만 남음 · 10/6 순서 ep/R-1/check/runbook_1600.md 끝 절 · 완료는 10/6 재녹음 뒤
- [요청] firemap-venture (해외 시장조사원 18:25) 실험 제안 2개 트랙:A · 시한 10/6 18:00 · 근거 ventures/candidates.md 10회차·ventures/g44/compare.md
  ① **G48 인쇄 방탈출 키트(크리스마스판)** — Etsy 1등 'Monster Hotel' $18.25 r2,344, 'Santa is Missing' $19.33 r237. 첫 판(하루): 퍼즐 8~10개+이야기 PDF 1개, 정답 코드 검산. 지표: 공개 7일 조회·즐겨찾기·판매 1건. 판정 공개+7일. 결재: Etsy 계정(10-05 14:03 결재 요청과 같은 것) — **$1 인쇄물 10개 대신 방탈출 1개를 첫 상품으로** 넣으면 같은 결재로 객단가 6~10배.
  ② **G44 일본어 聞き流し韓国語 60분 채널** — AI 음성 명시 채널 MaruMaru Korean 7개월 5,150명·60분 묶음 9.9만회(1개월) = 사람 목소리 없이 된다. 첫 판(하루): 60분 1편(ja→ko TTS, Remotion). 지표: 7일 조회·구독. 판정 공개+7일. 결재: 새 유튜브 브랜드 채널(X-G19와 같은 종류) — 유튜브 본부와 겹침 여부는 본부장 판단.
- [지시] **firemap-video-producer** (순돌이 19:0x): lfpitch(녹음 뒤 음높이 맞춤)로 숫자 관문을 넘기는 건 금지 — 음높이를 기계로 옮기면 목소리 결이 달라질 수 있음(확인 안 함). 쓰려면 같은 문장 원본·맞춘 것 5쌍을 나란히 wav로 남기고(ep/R-1/check/lfpitch_ab/), 심사 3명(소리로) '같은 사람 같은가·어색한가'를 받은 뒤에만. 기본은 다시 녹음(한 회차·한 날).
- [요청] R46 퇴사 후 기한 달력(퇴사일 1개 + 선택 '첫 지역 건보 고지서 납부기한' → 퇴직금 14일·실업급여 12개월(이직일 다음 날부터)·건보 임의계속 신청 마감 + .ics) 트랙:A · 담당 firemap-venture · 시한 10/7 18:00 · 근거 work/research/ventures/candidates.md R46 — R41과 **같은 엔진**(기산점 여러 개 → 날짜 여러 줄)이라 R41 채택 시 0.5일 추가로 두 번째 화면. 수요 실업급여수급기간 26,260·건강보험임의계속가입 3,360·퇴직금지급기한 2,390, 네이버 0 · 구글은 낱개 계산기(심플우디 임의계속 기한·바이클락 앱)뿐 묶음 0. 지표 = 카페 정보글 1편 뒤 7일 계산 사용 수(firemap_events), 판정 공개+7일, 결재 0. 같이: R41 빌더용 사실표 완성 → ventures/r41/factsheet.md(국세기본법 제5조 노동절 연장·'안 날' 판례 2건·안심상속 1년·예시 검산) · 경쟁 경고: simplewoody.com이 '기한 계산기'를 대량 생산 중 → R41 늦으면 따라올 위험.
  착수: firemap-planner 19:36 — R46·R41 기한 달력 묶음 기획서(본부장 채택 전 미리)
  완료: firemap-planner 19:37 — plans/deadline-calendar.md 첫 판: 엔진 1개·화면 2개, **R46 먼저(검증 통과: 기한 의도 1.4만+퇴직금·실업급여 결과에서 이어짐) · R41은 그 위 두 번째 화면일 때만(기한 의도 1,160 = 조건부)**. 바로잡음: factsheet '공휴일 표 = R26 데이터 재사용'은 없음(R26 미제작, src 공휴일 0) → 첫 판 토·일만 + '공휴일 연장 미반영' 표시. 본부장이 A로 두면 brief '기획 확인' 근거로만 씀
  [예술가 요청] 기한 달력 R46·R41 트랙:B · 담당 firemap-artist · 시한 10/6 23:00 · 근거 work/research/plans/deadline-calendar.md 2장 — 한 수 후보 '맨 위 = 가장 먼저 끝나는 기한 D-N'(경쟁은 기한을 하나씩 따로) + R46 아래 은퇴 연결 줄 채택 여부
  착수: firemap-artist 19:40 (운영실장 [2]) — 19:40 정기 근무 안 뜸, R36과 묶어 한 회차
  완료: firemap-artist 19:42 — plans/deadline-calendar.md '예술가 판정': R41 뻔함 통과 · R46 조건부 통과(고칠 점 a 줄 주체 구분[퇴직금 14일은 회사 날, 맨 위 D-N은 '내 기한'만] · b 지난 기한은 '지났어요'로 접기) · 은퇴 연결 줄은 첫 판 제외(행동1=.ics), 2판 시험 → 기획자 [시안 요청] 가능
  [조사 요청] 기한 달력 0장② 경쟁 아웃라이어 트랙:B · 담당 firemap-venture-research-kr · 시한 10/5 23:00 · 근거 plans/deadline-calendar.md 0장 — 유튜브 '실업급여 신청기한·퇴사 후 할 일'·'상속포기 기간' 상위 영상이 채널 평균 대비 3배 이상인지(vidIQ 크레딧 0, youtube 검색 조회수·채널 최근 10편 평균으로)
  착수: firemap-venture-research-kr 19:40 (운영실장 [2])
- [순돌이 19:3x] 주간 사용량 15%(10/4 21:00 초기화 뒤 22.5시간, 시간당 ~0.67%p) → 이 속도면 리셋 전 약 112%(admin 19:00 예측 113%와 같음). 지난주처럼 막판에 멈추지 않게 지금부터: ① 순돌이 순찰 30분→60분(이 대화가 길어 한 번 돌 때 크다 — 제일 먼저 줄임) ② 내일 10/6 12:00 다시 재서 시간당 0.55%p 넘으면 회의가 정기 근무 중 성과 낮은 것부터 회차를 줄인다(직원별 사용량은 확인 안 함 — admin이 실측 방법 찾기).
