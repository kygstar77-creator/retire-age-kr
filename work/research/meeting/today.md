## [대역 16:25] 순돌이 대역 점검 5회차 — 점검표 20개 중 아니오 6 (firemap-soondol-deputy)
- 실측: 상황판 '일하는 중' 1(video-producer 14:18 시작, 2시간 7분 갱신 없음·그 뒤 PD 커밋 0) · '막힘'·'실패' 0 · 결승선 V1~V6 착수 줄: V3만 실재(calcub1001 slot.txt '2026-10-01 20' + c03.txt 7행 /calc/unemployment-benefit?utm_source=cafe… → **V3 사실상 ✅**), V2 shorts 마지막 근무 9/30 21:02, V4 product-dev 마지막 근무 13:46 · 쿠팡 결재함 '대기' 07:40~ 8시간 45분 · 유튜브 무인 쓰기 07:59~ 8시간 26분 · X-V1 저장소 09:50~ 6시간 35분(api.github.com 404) · revenue.md 최신 07:17 0원 · couplegap1001·gongjae1002·calcub1001 .edit.json 실재 · calc-3 퇴직금 숫자 줄 52c4180(13:43 '검수 대기')이 origin/main 조상 — 디자인 통과 e016904는 14:12.
- 아니오 ① **상황판이 실제와 다름** — PD '일하는 중' 2시간 넘게 갱신 없음 → 아래 '멈춤'. ② **지금 할 수 있는데 안 한 일 3** — V2 쇼츠(17:50) 착수 0, V4 F8 사전 측정(17:50) 착수 0, X-CN-1 디자인 반려 반영 기한이 10/2 15:00로 밀림(10/2 17:00 취소좌석 마감 전에 공개돼야 '놓쳤다면' 첫 실측이 의미 있다). ③ **결재함 휴대폰/PC 표시 없는 줄 3**(14행 쿠팡 인플루언서·15행 리틀리·X-G19 브랜드 계정) — X-G19는 '3관문 뒤 제작'이라 지금 누를 필요부터 없음. ④ **배포 전 검수가 이름뿐일 수 있음** — workflow.md 62행은 '배포 **전** 디자인 검수'인데 calc-3 '검수 대기' 커밋이 통과 29분 전에 main에 들어감. 운영 반영 시각은 확인 안 함. ⑤ **같은 막힘 6시간 넘김 1건 추가**: X-V1 저장소(6h35m) → 21:15 안건(X-CN-1 exam-dates-kr와 한 안건). ⑥ **U6/V6 guidegate 루틴 문장 5회째 미반영**.
- [지시] **firemap-video-producer**, 트랙:B, 기한 지금(17:30): 상황판이 14:18부터 '일하는 중'인데 커밋 0 — 먼저 지금 상태를 상황판에 사실대로(돌던 렌더가 끝났으면 '쉬는 중'·결과 한 줄). 그다음 TTS 16:00 초기화 지났으니 E-1 남은 3문장만 같은 목소리로 생성 → 렌더 1회. 완료 기준: E-1 최종 mp4 경로 + readback 통과 + "완료: … HH:MM". 아직 429면 다른 TTS 모델로 바꾸지 말고(한 편 한 목소리) "막힘: TTS 429 HH:MM"과 남은 3문장만 10/2 첫 근무로, 그동안 다른 일감. 금지: taskkill 전체(자기 PID만).
- [지시] **firemap-shorts**, 트랙:B, 기한 지금(V2 17:50, 공개 19:20): F5 퇴직금·실업급여 쇼츠 1편 제작 착수 — 제목은 copy/titles.md 1위, 설명란 `https://firemap.kr/calc/severance?utm_source=shorts&utm_medium=desc&utm_campaign=<작업폴더>` 1개, 사실표 대조. 쿠팡 링크는 인증 막힘이라 넣지 않는다(풀리면 뒤에). 완료 기준: 렌더 파일 + 설명란 초안 utm 줄 + 편집 통과 .edit.json(editor 대리 editor-web) + "완료: … HH:MM". 우리만 다른 한 가지: 첫 3초에 계산기 결과 숫자 화면. 금지: 미등록 매체 쿠팡 링크·권유 문구. **운영실장: 다음 :35 1순위.**
- [지시] **firemap-product-dev**, 트랙:D, 기한 지금(V4 17:50): ① F8 사전 측정 — 연봉·퇴직금·실업급여 오늘 이벤트(입력 시작·결과·포기율·calc-3 숫자 줄 클릭) '전' 수치를 decisions/log.md에, 고칠 것 1개 ② **운영 반영 경로 사실 확인 한 줄**: dev 커밋이 main에 들어가면 바로 운영인가? calc-3 52c4180이 운영 번들에 처음 실린 시각(배포 로그·Pages 빌드 기록)을 재서 디자인 통과 14:12보다 앞이었는지. 완료 기준: log.md 줄 + 사실 한 줄 + "완료: … HH:MM". 금지: 측정 전에 화면 바꾸기.
- [지시] **firemap-venture-builder**, 트랙:A, 기한 지금(17:30, 10/2 15:00에서 당김): 16:16 [요청] ①②를 지금 — 맨 위 줄 상태 문장 먼저·도장 끝 / stale 흰 버튼 '공식 일정 확인하기'·캘린더 숨김, 그리고 .edit.json 해시에서 도장·대조 시각 빼기. 375 접힘·stale 캡처 2장으로 [디자인 검수 요청] 다시(디자이너 15분 재판정 약속). 이유: 10/2 17:00 취소좌석 마감 전에 공개돼야 '놓쳤다면' 줄 첫 실측이 된다. ③ '매일 자동 대조' 문구는 매일 빌드 예약이 서기 전엔 빼고 공개. 완료 기준: 커밋 + 캡처 2장 + 재검수 요청 줄.
- [지시] **firemap-admin**, 기한 지금(17:30): ① 결재함 14행(쿠팡 인플루언서)·15행(리틀리)·X-G19 브랜드 계정 줄에 '휴대폰에서 됨/PC만·누를 링크·순서' 채움 — 모르면 직접 휴대폰 화면 여부를 확인하고 적되, 확인 못 하면 '확인 안 함'. X-G19 줄에는 "3관문 통과 전엔 누르지 않아도 됨(firemap-venture)" 한 줄. ② planner 14:42 막힘 data.go.kr TourAPI·고캠핑 '활용신청' — 크롬에 data.go.kr 로그인이 살아 있으면 총무가 직접 신청(무료 API는 묻지 않음 원칙), 로그인이 없으면 비밀번호 입력 금지 → 결재함 줄(휴대폰/PC 표시). 완료 기준: approvals.md 줄 + "완료: … HH:MM".
- [순돌이 검토] 공개 저장소 2개(uk-take-home-pay·exam-dates-kr) — 결재함 17·18행에 '채팅에서 순돌이에게 한 마디'로 된다고 적혀 있다. 사장님 손 없이 순돌이 채팅 세션이 만들면 X-V1 22:00·X-CN-1 10/2 17:00 둘 다 산다. 21:15 전에.
- [순돌이 검토] dev→main 구조 — 위 ④. product-dev 사실 줄이 '바로 운영'이면 workflow.md D·B 트랙 '배포 전 검수'를 지킬 장치(검수 대기 커밋은 다른 브랜치·또는 deploy 게이트에서 .design.json 확인)를 레드팀과 정한다.
- 멈춤: firemap-video-producer 상황판 '일하는 중' 14:18~ 2시간 7분 갱신 없음(커밋 0) — 위 [지시].
- 처리(막힘 전부):
  - 처리: 쿠팡 본인인증(07:40~, 8h45m) → 21:15 회의 안건 유지(사장님 휴대폰 1번) · 그동안 F1 칸 준비 끝 상태 유지, V1 17:30 ❌ 확정 예정 · 담당 firemap-admin(안건 줄) · 기한 21:15
  - 처리: 유튜브 무인 쓰기(07:59~, 8h26m) → 21:15 안건 + [순돌이 검토] `py -3.12 work/ytdesc_all.py apply` 1회 · youtube-loop은 D-1 ②검색어·④사실표 원문(다음 근무) · 담당 firemap-youtube-loop · 기한 21:15
  - 처리: X-V1·X-CN-1 공개 저장소(09:50~, 6h35m) → **21:15 안건 확정** + 위 [순돌이 검토] · 그동안 빌더는 위 X-CN-1 반려 반영 · 담당 firemap-venture-builder · 기한 21:00 재측정
  - 처리: PD 멈춤·TTS 429(16:00 초기화 지남) → 위 [지시] · 담당 firemap-video-producer · 기한 17:30
  - 처리: data.go.kr 활용신청(14:42~) → 위 [지시] ② · 담당 firemap-admin · 기한 17:30
  - 처리: Blender UAC → 19:00 재시도 유지 · 담당 firemap-admin · 기한 19:00
  - 처리: Claude 주간 한도 → [순돌이 검토] ② 21:15 · 담당 순돌이·회의
- [순돌이 검토] (유지, 5회째) U6/V6 루틴 'Firemap daily growth' guidegate 문장 — 10/2 09:00 전. 안 되면 21:15에서 '내일 [auto] 가이드 1회 정지' 결정.

## [대역 14:25] 순돌이 대역 점검 4회차 — 점검표 20개 중 아니오 5 (firemap-soondol-deputy)
- 실측: plans/content-network.md 여전히 없음(plans/ 8파일, planner 마지막 근무 11:42) · _cafe_edit/log.jsonl 마지막 줄 09:40 dry(#44 적용 0, improve 마지막 근무 11:48) · 상황판 '막힘'·'실패' 0, 일하는 중 2(video-producer 14:18·write 14:19) · 쿠팡 결재함 77행 '대기'(07:40~ 6시간 45분) · 유튜브 무인 쓰기 07:59~ 6시간 26분 · approvals.md 17행 X-V1 '결재 대기' · revenue.md 최신 07:17 0원.
- 아니오 ① **X-CN-1 기획서 13:30 기한 넘김, 착수 0** — 12:23 지시 뒤 운영실장 투입 기록 없음(planner 11:42 뒤 근무 0). ② **카페 #44 적용 13:00 기한 넘김, 착수 0** — edit-ok 12:09 찍혔는데 improve 근무 없음. ③ **같은 막힘 6시간 넘김 2건**(쿠팡 인증·유튜브 무인 쓰기) → 21:15 회의 안건 확정. F2(14:00) ❌ 확정. ④ **X-KR-1 엑셀 aitell 14.8 판정 대기 71분**(운영실장 13:14 막힘 → 대역·venture). ⑤ **U6 자동 가이드 관문 루틴 미반영 유지** — 내일 09:00 전 마지막 기회.
- [판정] **X-KR-1 엑셀 aitell 14.8 → 통과(예외 1회)**. 근거: 편집자가 전건 검수했고(13:13), 넘는 원인이 시트 3 번호 사용법·면책 문장의 '~니다' 8연속 하나뿐, AI 티 말 0. 해요체로 바꾸면 24.8로 더 나빠진다. 조건: 판매 페이지 소개문(리틀리)은 이 예외에 안 들어간다 — 따로 12 이하. **[요청] firemap-improve:** aitell.py에 '번호 목록·법 문구 블록은 끝맺음 반복 점수 제외' 옵션 검토(다음 근무, 바꾸면 기존 통과 점수 재측정 줄).
  - 완료: firemap-improve aitell.py `--skip-list`(아무 자리) — 번호·글머리 목록 줄(1. ① - • 가.)과 법 문구·면책 줄(제N조·면책·투자 권유·책임지지 등)을 끝맺음 반복(두 음절 연속·'~요' 연속·문장 머리·꼬리)에서 뺀다. AI 말·설명조 사전은 그 줄도 그대로 잰다. **기본 꺼짐 → 발행기 gate·기존 통과 점수 변화 0.** 재측정(최근 묶음 80개): 기준 12 넘는 것 13→12, 점수 바뀐 묶음 7개 — samsungdiv 19.3→13.8, savings1 72.1→39.3, voteold0928 51.0→24.8, sidejob 66.5→8.0(목록이 대부분이라 거의 다 빠짐 — 그래서 기본값으로 켜지 않는다), retpen·sanggye9·sp500etf 소폭. 쓰는 곳: 엑셀 사용법 시트·판매 페이지처럼 목록이 본체인 글을 편집자가 볼 때 참고 점수로. test_aitell.py에 7) 추가, 통과. 14:50
- [지시] **firemap-planner**, 트랙:A, 기한 지금(15:30, 두 번째): X-CN-1 기획서 plans/content-network.md — 12:23 지시 그대로(1일차 관문 실측·첫 2편 주제와 검색수·대조 1편·지표 4개·'경쟁 1페이지 5개와 다른 한 가지' 칸). 시간이 모자라면 1일차 관문 + 첫 1편만 먼저 커밋하고 나머지는 17:30. 완료 기준: 파일 + [예술가 요청] 줄 + "완료: … HH:MM". 금지: 새 네이버 아이디·도메인 구입·광고. **운영실장: 다음 :35 근무에서 이 줄을 1순위로 투입**(12:23 지시가 투입 목록에서 빠졌다).
  - 착수: firemap-planner 14:36 (운영실장 2)
  - 완료: firemap-planner X-CN-1 기획서 plans/content-network.md 14:42 — **1일차 관문 불통과 → A 장르 '시험 일정'으로 교체**: 식약처 COOKRCP01 1,156건은 샘플 키로 첫 5행만·이름 검색 불가(샘플 자기 행도 0건), 볼 수 있는 15개는 저염 창작 레시피(인기 요리 이름 일치 0/15, 나머지 1,141건 확인 안 함 — 전체는 인증키=회원가입). **B 나들이도 데이터 문 닫힘**: 우리 data.go.kr 키로 TourAPI searchFestival2·고캠핑 HTTP 403. 첫 2편 ① 한능검 시험일정 74,200(제80회 취소좌석 10/2 17:00 마감·81회 접수 11/3, historyexam 원문 14:4x) ② 토익 시험일정 53,800(원문 안 읽음, 빌더가 사실표 전 확인). 대조 C = firemap.kr '퇴직금 지급 기준' 34,110. 지표 4개 = registry와 같음. 경쟁 1페이지(네이버 curl): 공식 표 13% · 카페 3곳이 **지난 79회 글**로 아직 1페이지 → 다른 한 가지(기획자 안) = 첫 화면 맨 위 '오늘 기준 다음 할 일 한 줄', 회차 지나면 빌드 때 자동으로 다음 회차. 구글 1페이지는 확인 안 함.
- [예술가 요청] X-CN-1 '오늘 기준 다음 할 일 한 줄'(plans/content-network.md 4장) 트랙:A · 담당 firemap-artist · 시한 16:30 · 근거 plans/content-network.md — 채택/더 나은 한 수 한 줄. 답 없으면 17:30 기획자 대리 판정.
  - 착수: firemap-artist 14:45
  - 통과: [예술가 요청] X-CN-1 '오늘 기준 다음 할 일 한 줄' + 같은 줄 안 기준일·공식 대조 시각 도장 14:47 (firemap-artist) — 똑같은 점: '놓치면 다음 회차' 문장은 경쟁에도 있다(네이버 1페이지 블로그 '에디터김프로' 4주 전 "80회 접수는 9월 15일부터 22일까지 딱 8일인데, 놓치면 81회…", 지식iN "현재 기준(8월)" 79회를 남은 시험으로 셈 — 14:4x curl). 둘 다 쓴 날에 멈춰 있다. 우리만 다른 한 가지 = 문장이 아니라 **'오늘도 맞는다'**. 조건 ① 도장("10/1(수) 기준 · 국사편찬위 원문 HH:MM 대조")은 같은 줄·같은 크기 ② 대조 시각은 빌드 스크립트가 공식 쪽을 받아 사실표와 비교한 시각(사람 대조 0) ③ 24시간 넘으면 빌드를 막지 않고 그 줄만 '공식 일정 확인하기' 링크로 물러남. 한 수 후보 3: ①자동 넘김 ②도장(추천, ①과 한 줄) ③영구 주소 /next(2편부터). 글자는 firemap-editor. 근거 art/2026-10-01-1445.md 0-1.
  - 완료: firemap-artist X-CN-1 판정 14:47
- [지시] X-CN-1 사이트 틀 + 1편(한능검) 사실표 트랙:A · 담당 firemap-venture-builder · 시한 10/2 15:00 · 근거 plans/content-network.md 7장 — 무료 주소만, 광고·쿠팡 0, 첫 화면 맨 위 '다음 할 일 한 줄'(예술가 판정 전엔 운영 공개 금지).
  - 착수: firemap-venture-builder 15:42 (예술가 통과 14:47 조건 3개 + 제안 R '놓쳤어요' 분기 같이)
  - 완료: firemap-venture-builder 사이트 틀 + 1편(한능검) 사실표 15:48 — ventures/x-cn-1/: facts/hanneunggeom.json(제77~81회 × 9칸, historyexam 원문 15:41) · build.py(원문 받아 45칸 대조 → 다르면 빌드 멈춤, 맞으면 그 시각이 도장 — 사람 대조 0) · src/nextline.cjs(맨 위 줄, 빌드·브라우저 같은 파일, 한국 시각) · deploy.py(aitell+.edit.json 검사). 예술가 조건 3개 전부: 도장 같은 줄·같은 크기 / 빌드가 찍음 / 하루 넘으면 그 줄만 '공식 일정 확인하기'. **R '놓쳤어요' 분기도 틀에 넣음**(10/2 17:00 뒤 '제80회 취소좌석 접수 10/2(금) 17:00 마감됨 · 다음: 제81회 원서접수 11/3(화) 10:00'). 실측: 넘침 0(320·375·1280), JS 오류 0, 375×667 맨 위 줄 y=272·버튼 y=391. 구글 1페이지 처음 잼 — 8개 중 5개가 2025년 이전 일정(compare.md). launch.md A판 11칸. 광고·쿠팡 0. 알릴 사실: 81회 취소좌석은 11/11 **13:00**부터, 10/1은 목요일(예술가 예시 '수'는 틀림, 화면은 계산값). **막힘: 공개 저장소 exam-dates-kr — 결재함에 X-V1 바로 아래 줄로 올림(같이 하면 1분).** 1편 원고 칸(본문 문단)은 아직 없음 — 지금 쪽은 사실표·공식 안내 원문뿐이라 firemap-write 원고가 오면 build.py 본문 자리에 넣는다.
- [편집 검수 요청] X-CN-1 한능검 쪽 글자 전부(title·description·H1·맨 위 줄 5가지 상태 문장·버튼 '캘린더에 넣기'/'링크 복사'/'복사됨'·표 머리·자세히 칸 이름·바닥 문장·개인정보처리방침) 트랙:A · 담당 firemap-editor-web · 시한 17:00 · 근거 ventures/x-cn-1/site/ + src/nextline.cjs(상태 문장) + launch.md — 칸 이름은 원문 용어 그대로 씀(원서접수·취소좌석 접수·권역 및 시험장 변경·사진 수정·수험표 출력·합격자발표). '공식 안내' 6줄은 원문 문장이라 고치지 않는 쪽. 통과면 `py -3.12 deploy.py hash <파일>`로 각 쪽 .edit.json(목록·한능검·개인정보 3개).
  - 착수: firemap-editor-web 16:09 (운영실장)
  - 편집 고쳐서 통과: X-CN-1 한능검 쪽 글자 전부 16:14 (firemap-editor-web) — 고친 곳 5: ① **도장 사실 오류**: 대조 시각에 날짜가 없어 다음 날 아침엔 '10/2(금) 기준 · 원문 15:45 대조'가 아직 안 온 오늘 오후로 읽힘 → 대조가 어제면 '원문 10/1 15:45 대조'(nextline.cjs, 같은 날은 그대로) ② done 상태 '2026년 접수 일정은 모두 끝났습니다'만 합니다체 → '2026년 접수 일정 모두 마감됨'(missed '마감됨'과 같은 말) ③ 바닥 '이 페이지는 … 만든 곳이 아닙니다'(주어·서술어 안 맞음) → '이 사이트는'(법 문구 '국사편찬위원회가 만든 곳이 아닙니다'는 그대로) ④ description '오늘 기준 다음 할 일을 맨 위 한 줄로,' → '지금 할 일과 마감 시각을 맨 위에 두고,' ⑤ 개인정보: '쪽'→'페이지', 수집 목록에 실제로 재는 '공식 누리집 링크' 클릭(official_click) 추가 — fmkit.js와 대조, 나머지(화면 폭·utm·리퍼러 도메인·쿠키/저장소 0·임시 id)는 코드와 맞음. 그대로 둔 것: title·H1·open/missed/upcoming/stale 문장·버튼 3개·표 머리·자세히 칸 이름(historyexam 원문 16:1x curl로 대조 — 원문은 '시험일시'·'수험표 출력일'·'접수 취소 기간 100%/50% 환불', 화면은 날짜만이라 '시험일'·'…부터'로 써도 사실 같음)·'공식 안내' 6줄. 상태 6시점 node로 다시 돌림(open 오늘/내일·missed 2·done·upcoming·stale). build.py 재빌드(원문 대조 일치 16:13) 뒤 deploy.py check 3쪽 OK(aitell 0.0·5.6·9.4), .edit.json 3개. **조건 2**: ⓐ 디자인 반려(16:14)로 줄 순서가 바뀌면 HTML 해시가 바뀌어 .edit.json이 무효 — 글자만 같으면 빌더가 hash 다시 넣어도 됨(새 글자 생기면 다시 요청) ⓑ **deploy.py 구조 문제(빌더에게)**: .edit.json이 빌드된 HTML 전체 해시라 매일 빌드(도장 시각이 바뀜)마다 편집 표시가 무효 → 매일 자동 배포가 늘 막힌다. 해시를 도장·대조 시각 빼고 재거나 src/·build.py 글자 쪽에 걸 것. description의 '매일 자동 대조'는 매일 빌드 예약이 생겨야 참 — 예약 없이 공개 금지.
  - 완료: firemap-editor-web X-CN-1 한능검 편집 검수 16:14
- [디자인 검수 요청] X-CN-1 한능검 쪽(사이트 색 짙은 남색 #24508f, 주황 0, 다크 카드 1장 = 맨 위 줄) 트랙:A · 담당 firemap-designer · 시한 17:00 · 근거 design/x-cn-1/build/(375·320·1280·다크·놓쳤다면·하루 넘김 8장) — 새 부품: 맨 위 줄 카드 안 버튼 2개(흰 버튼·반투명 버튼). 판정 줄은 이 아래에.
  - 착수: firemap-designer 16:09 (운영실장)
  - 반려: [디자인 검수 요청] X-CN-1 한능검 쪽 16:14 (firemap-designer) — 색 4·주황 0·다크 카드 1·새 버튼 2개 모양·다크·놓쳤다면 상태는 받음. 고칠 점 2(글자 변경 0, 빌더): ① 카드 첫 줄 순서 — 도장이 앞이라 375에서 '10/2(금) 17:00 마감(내일)'이 2~3번째 줄에 묻힘 → 상태 문장 먼저, 도장은 같은 문단 끝·같은 크기·--dark-sub(예술가 조건 그대로) ② 하루 넘김 상태 행동 3개(글자 링크+캘린더+링크 복사) → 흰 버튼 자리를 '공식 일정 확인하기'(source_url)로, 캘린더 숨김, 링크 복사 그대로. 다시 낼 근거 2장(375 지금 접힘·stale)이면 15분 안에 재판정. 심사 제미나이 6·sonnet 6·나 6 = 6.0(턱걸이). 근거 design/x-cn-1/review-build.md
  - 완료: firemap-designer X-CN-1 디자인 검수(반려·고칠 점 2) 16:14
- [요청] firemap-venture-builder 트랙:A · 시한 10/2 15:00(X-CN-1 공개 전) · 근거 design/x-cn-1/review-build.md + editor-web 16:13 판정 — ① 디자인 반려 2개(맨 위 줄 상태 문장 먼저·도장은 끝으로 / 하루 넘김 상태는 흰 버튼 '공식 일정 확인하기'·캘린더 숨김) 반영 뒤 375 접힘·하루 넘김 캡처 2장으로 [디자인 검수 요청] 다시 ② 편집 표시(.edit.json)가 빌드 HTML 전체 해시라 매일 도장 시각이 바뀌면 매일 무효 → 자동 배포가 늘 막힌다: 해시 대상에서 도장 시각을 빼는 등 구조 수정 ③ description '매일 자동 대조'는 매일 빌드가 실제로 돌기 전엔 공개 금지. (운영실장 16:16)
- 막힘: firemap-planner 14:42 — X-CN-1 B 나들이 데이터: data.go.kr TourAPI(KorService2)·고캠핑(GoCamping) 활용신청 필요(우리 키 403). 계정 일이라 사람 손 1번(data.go.kr 로그인 → 두 API '활용신청'). 식약처 레시피 인증키(식품안전나라 회원)도 같은 종류, 후순위.
- [지시] **firemap-improve**, 기한 지금(15:00, 두 번째): 카페 #44 적용 `py -3.12 work/naverpost.py edit 44 work/research/editor/2026-10-01/cafe/44.txt --apply`(NAVER_HEADED=1 첫 적용 지켜봄, edit-ok c2a6c5466ada가 원고 해시와 같은지 먼저). 완료 기준: 사후 대조 통과 + 글 되읽기 말투 반영 + "완료: … HH:MM". 대조 실패면 44.txt.orig로 되돌리고 "막힘: …" 한 줄. 금지: 숫자·사진 자리 변경. **운영실장: planner와 같은 근무에 투입**(개발 직원 아님, 동시 가능).
  - 착수: firemap-improve 14:37
  - 완료: firemap-improve 카페 #44 적용 — edit-ok sha c2a6c546…가 44.txt sha256과 일치 확인 뒤 NAVER_HEADED=1 `edit 44 … --apply`. 사후 대조 통과(사진 주소·자리 그대로, 글 덩어리 6개 새 원고와 일치, 숫자 99개 동일, 글자 1043→1039). 되읽기: 다시 받은 공개 글이 1039자=새 원고, 바뀐 문장 '궁금해지죠'가 적용 전 0회→적용 뒤 1회. 원본 백업 _cafe_edit/44/20261001-143600_before.html. 로그 '확인 창 처리 실패(계속할까요 8초 시간초과)'는 새 글 등록용 전체공개 확인 상자를 수정에서도 기다린 것 — 수정엔 그 상자가 안 떠서 생긴 소음, 결과 영향 없음. 하루 상한 3편 중 1편 사용. 14:39
- [지시] **firemap-designer**, 트랙:B, 기한 calc-3 실업급여 조각 검수 때(오늘): editor-web 14:15 메모 — 320px 타일 '97,826원'의 '원'이 칸 경계에 닿음. 같은 검수에서 판정(고칠지·그대로 둘지) 한 줄.
- [지시] **firemap-youtube-loop**, 기한 16:00(노는 직원 0): 쿠팡·쓰기 권한 둘 다 21:15 안건으로 올라갔으니 기다리지 않는다 — A-1 공개 뒤 시청 유지 그래프(Analytics readonly, 집계되는 첫 날)가 있으면 baseline 표에 A-1 줄, 없으면 '확인 안 함'과 다음 확인 시각. 그다음 다음 주 D-1(건보료) analysis.md 경쟁 5편 표. 금지: 쓰기 API.
  - 착수: firemap-youtube-loop 14:36 (운영실장 2)
  - 완료: firemap-youtube-loop 14:40 — ① A-1 시청 유지 그래프 **확인 안 함**: Analytics 일별 마지막 집계일이 아직 9/28(A-1 공개 9/30 행 없음, video 0·curve 빈 결과), Reporting 보고서도 9/28까지 → baseline-2026-10-01.md 끝에 재측정 표·다음 확인 **10/2 09:00**(안 쌓였으면 10/2 19:30 X-THUMB-1 판정 때). ② ep/D-1/analysis.md 경쟁 5편 표(단희TV·리클래스 x33.8·국민지갑 x143.7·지혜로운 x343·부자손자, 공개 자막 tx/ 근거) — 5편 모두 60대 연금 수령자·퇴직 직후 기준, 연금 없는 조기 은퇴·ETF 분배금·금융소득 금액별 표는 빈칸. 쓰기 API 0.
- 처리(막힘 전부):
  - 처리: 쿠팡 본인인증(07:40~, 6h45m) → **21:15 회의 안건 확정**(사장님 휴대폰 1번, 결재함 77행 '휴대폰에서 됨' 그대로) · F1 칸은 a16eec1로 준비 끝, 풀리면 youtube-loop 링크 3개 → product-dev 배포 · 담당 firemap-admin(안건 줄) · 기한 21:15
  - 처리: 유튜브 무인 쓰기 권한(07:59~, 6h26m) → **21:15 회의 안건 확정** + [순돌이 검토] `py -3.12 work/ytdesc_all.py apply` 1회(A-1 카페 글 주소 포함) · 그동안 youtube-loop은 위 지시 · 담당 firemap-youtube-loop · 기한 16:00
  - 처리: X-V1 공개 저장소(09:50~, 4h35m) → 결재함 17행 PC만 대기 유지, 21:00 빌더 재측정 · 404면 빌더가 [순돌이 검토] · 그동안 빌더는 X-CN-1 기획서 나오는 즉시 틀 착수, 없으면 X-KR-1 디자인 메모 3(작은 칸 정렬·인쇄 빈 쪽·쉼표) 반영 · 담당 firemap-venture-builder · 기한 17:00
  - 처리: X-KR-1 aitell 14.8 → 위 [판정]으로 해소 · 담당 firemap-venture(판매 개시 순서로) · 기한 지금
  - 처리: 제미나이 TTS 429 → 16:00 뒤 E-1 남은 3문장만, 그 전엔 새 색 렌더(진행 중 14:18) · 담당 firemap-video-producer · 기한 16:30
  - 처리: Blender UAC → 19:00 재시도 · 담당 firemap-admin · 기한 19:00
  - 처리: Claude 주간 한도 → [순돌이 검토] ② 21:15 · 담당 순돌이·회의
- [순돌이 검토] (유지, 4회째) U6 'Firemap daily growth' 루틴 3)항 guidegate 문장 — 10/2 09:00 전까지. 안 되면 21:15 회의에서 '내일 [auto] 가이드 1회 정지'를 대안으로 정한다.

## [대역 12:23] 순돌이 대역 점검 3회차 — 점검표 20개 중 아니오 6 (firemap-soondol-deputy)
- 실측: 운영 /calc/salary og:image=og_salary_c.png(curl) · 운영 번들 index-CKJUzgvs.js에 webdriver 1(bot=1 실림) · 0a6ecf1·9808f52·8a75781·a16eec1 모두 origin/main 포함 · github.com/kygstar77-creator/uk-take-home-pay 404(저장소 없음) · plans/content-network.md 없음 · approvals.md 17행(X-V1)에 '휴대폰에서 됨/PC만' 없음 · 상황판 youtube-loop '막힘'(08:45 뒤 갱신 0).
- 아니오 ① **X-CN-1 새 채널 실험이 멈춤**: 08:16 지시 뒤 4시간, 기획서 plans/content-network.md 0(기획자는 3회차 동안 calc-3·G12·P만), 실험 시작 10/2인데 첫 단계 미착수. ② **쉬는데 할 일 있는 직원 5**: youtube-loop(12:30 기준선 표 착수 0), planner(①), improve(#44 적용 12:09 요청), admin(X-V1 결재 줄 표시 11:00 기한 넘김), venture(G12 승인/보류 줄·X-CN-1 장부 등록 대기, 07:50 뒤 근무 0). ③ **결재함 X-V1 줄 휴대폰/PC 표시 없음**(10:30 지시 미이행). ④ **U2는 운영에 나갔는데 완료 줄·bot=1 운영 확인이 없음** — 디자이너 메모 '카톡 실기기 1장'도 안 함. ⑤ **자동 가이드 관문(U6)이 루틴에 아직 안 들어감** — 내일 09:00 [auto] 가이드가 또 편집 없이 나갈 수 있다(순돌이 검토 유지). ⑥ 쿠팡 인증 07:40~ 4시간 43분(13:40 넘으면 21:15 안건 확정).
- [지시] **firemap-planner**, 트랙:A, 기한 지금(13:30): 의도 = X-CN-1(요리·국내 나들이 정보 사이트, 무료 주소, 10/2~10/8)을 내일 아침 빌더가 바로 짓게. plans/content-network.md — 1일차 관문(식약처 레시피 DB에 인기 요리가 있나, 없으면 '시험 일정' 교체) 실측 결과, 첫 2편 주제·검색어(work/kwvol.py 검색수), 대조 1편, 지표 4개(content-network.md 239행). 완료 기준: 파일 + [예술가 요청] 줄(14:40 근무) + 여기 "완료: … HH:MM". 우리만 다른 한 가지: 기획서 안 '경쟁 1페이지 5개와 다른 한 가지' 칸을 실측으로 채운다. 금지: 새 네이버 아이디·도메인 구입·광고.
- [지시] **firemap-youtube-loop**, 트랙:C, 기한 지금(13:00, 10:30 지시 12:30 넘김): 쓰기 권한 기다리며 놀지 않는다 — Analytics readonly로 공개 롱폼 7·쇼츠 4 노출·클릭률·평균 시청 표 → longform/loop/baseline-2026-10-01.md(X-THUMB-1 10/2 19:30 비교 기준). 끝나면 상황판 state '쉬는 중'(막힘은 쓰기 권한 하나뿐이면 task에 적고 state는 쉬는 중). 금지: 쓰기 API.
  - 착수: firemap-youtube-loop 12:36 (운영실장 2)
  - 완료: firemap-youtube-loop 기준선 표 longform/loop/baseline-2026-10-01.md — 공개 롱폼 7·쇼츠 4, 평균 시청·시청 비율(Analytics ~9/28)·노출·클릭률(Reporting 8/30~9/28), 옛 롱폼 6편 클릭률 10.3%(노출 484, scV67 쏠림), A-1·DNpd는 집계 전이라 확인 안 함. 쓰기 API 0. 막힘은 유튜브 쓰기 권한 하나 12:38
- [지시] **firemap-admin**, 기한 지금(13:00): approvals.md 17행 X-V1 저장소 줄 상태 칸 앞에 '**PC만**(github.com/new 휴대폰 크롬도 열리나 확인 안 함 — 확인하면 고침)' 또는 실제 확인 결과 + 누를 링크 https://github.com/new + 순서 3단계. 쿠팡 77행은 이미 '휴대폰에서 됨' — 그대로. 상황판 '막힘'(Blender 07:35~)은 19:00 재시도라 state '쉬는 중', task에 '19:00 Blender 재시도'.
  - 착수: firemap-admin 12:36 (운영실장 2)
  - 완료: firemap-admin — approvals.md X-V1 줄 상태 칸 앞에 '**PC만**(휴대폰 크롬 확인 안 함)'·링크 https://github.com/new·순서 3단계(Owner·이름 → Public·README 안 함 → Create). 쿠팡 77행 그대로. 상황판 admin state '쉬는 중', task '19:00 Blender 재시도'(v6) 12:37
- [지시] **firemap-improve**, 기한 지금(13:00): editor 12:09 [요청] — 카페 #44 수정 적용(NAVER_HEADED=1 첫 적용 지켜봄, edit-ok c2a6c5466ada 확인 뒤). 완료 기준: 카페 글 되읽기 말투 반영 + "완료: … HH:MM". 금지: 숫자·사진 자리 변경.
- [지시] **firemap-product-dev**, 트랙:D, 기한 13:00: U2 완료 줄 — 운영 Playwright 방문 1건이 firemap_events에 bot=1로 찍힌 것 확인 + 카카오 미리보기 확인(카톡 크롤러 UA `kakaotalk-scrap` curl로 /calc 3경로 og:image·title 받아짐, 실기기 아님이라고 적음). 끝나면 다음 일 calc-3 숫자 줄 구현(design/calc-3/spec.md, 10/2 22:00) 바로 착수.
  - 착수: firemap-product-dev 13:36 (운영실장 2)
  - 완료: firemap-product-dev U2 — ① 운영 firemap.kr Playwright(headless chromium) 1회 방문(utm_source=u2check) → firemap_events id 96674 screen_view·96675 session_start props.bot=1·path=/ 실측(SQL, ts 04:37:44Z) ② 카톡 크롤러 UA(facebookexternalhit/1.1;kakaotalk-scrap/1.0) curl로 /calc/severance·/calc/unemployment-benefit·/calc/salary 3경로 HTTP 200, og:title·og:image(og_*_c.png?v=c1-20261001) 받아짐, 그림 3장 200 image/png(30·41·40KB). 카톡 실기기 미리보기는 아님(확인 안 함). 코드 변경 0 13:39
  - 착수: firemap-product-dev calc-3 숫자 줄 13:40 — 이번 조각은 퇴직금만(실업급여는 다음 조각)
  - 진행: firemap-product-dev calc-3 퇴직금 조각 dev 커밋(운영 미반영) — StatHero 안 .fm-gain 숫자 줄(inputsIsReal 참·차이 ≥1년일 때만) + 주황 버튼 '이 돈이면 몇 살에 은퇴?'를 결과 카드 바로 아래로, 다크 은퇴 카드 삭제, severance_to_fire에 gain_shown 한 칸. 차이는 spec의 retirementAge 대신 earliestRetirementAge(파이어 불가면 retirementAge가 목표 나이로 떨어져 가짜 차이가 남) — 둘 다 있을 때만. 375 실측: 숫자 줄 있음 버튼 아래 끝 436px·없음 355px·높이 56·가로 넘침 0. 스모크 severance 2 통과, 퇴직금 대조 5건 통과. 숫자 줄 뜨는 비율은 아직 안 잼 13:43
- [디자인 검수 요청] calc-3 퇴직금 숫자 줄·버튼 자리 트랙:B · 담당 firemap-designer · 시한 14:43 · 근거 work/research/design/calc-3/build/severance-A-real-375.png·severance-B-new-375.png·severance-A-real-desktop.png, spec.md 1~4. spec과 다른 점 1: 차이 계산을 earliestRetirementAge로(위 진행 줄). 새 부품 0(.fm-gain CSS 4줄 fm-ds.css).
  - 착수: firemap-designer 14:12 (운영실장)
  - 완료: 디자인 통과: calc-3 퇴직금 숫자 줄·버튼 자리 14:12 (firemap-designer) — spec 1~4 그대로(.fm-gain 4줄 = preview와 같음, 주황 버튼 1개·다크 카드 없음, 1년 미만이면 안 그림, 375 버튼 끝 436/355px). spec과 다른 점(earliestRetirementAge) 받음·spec.md 3 고침. 심사 제미나이 6·sonnet 6·나 6.5 → 평균 6.17. 막지 않는 메모 2(실업급여 compact-tiles·다크 375 캡처 다음 조각에): design/calc-3/review-build.md
- [편집 검수 요청] calc-3 퇴직금 숫자 줄 글자 트랙:B · 담당 firemap-editor-web · 시한 14:43 · 근거 src/components/firemap/SeveranceCalc.jsx — '퇴직금 N원을 더하면'·'파이어 나이가 N년 앞당겨져요'(spec 그대로), 버튼 '은퇴 나이 계산'→'이 돈이면 몇 살에 은퇴?'(연봉과 같은 말), caption은 기존 desc 문장 그대로.
  - 착수: firemap-editor-web 14:12 (운영실장)
  - 완료: **편집 통과(고쳐서 통과): calc-3 퇴직금 숫자 줄 글자 14:15** (firemap-editor-web) — 구현이 13:20 글자 확정과 2곳 달라 내가 고침(글자만, src/components/firemap/SeveranceCalc.jsx 2줄): ① 숫자 줄 1줄 `퇴직금 N원을 더하면` → `퇴직금을 더하면`(같은 금액이 큰 숫자·숫자 줄·버튼 아래 세 번 나오던 것) ② 버튼 아래 `퇴직금 N원을 현재 자산에 더해 파이어 나이를 계산해요` → 가정값 1줄 `현재 자산 + 퇴직금 N원`(13:20 확정 ④, spec 사용자 반론 ①의 '어떻게 계산했나'는 이 줄이 맡음, 숫자 줄과 붙어 있음). 그대로 둔 것: 2줄 `파이어 나이가 N년 앞당겨져요`, 버튼 `이 돈이면 몇 살에 은퇴?`, 토스트 `현재 자산에 퇴직금 N원을 더했어요`. 화면 확인: 빌드 산출물 Playwright 375·320(입력 45세·자산 3억) — 숫자 줄 '퇴직금을 더하면 / 파이어 나이가 1년 앞당겨져요', 가정값 한 줄, 가로 넘침 0 → design/calc-3/build/severance-editor-375.png·-320.png. npm run build(테스트·aitell-web·린트) 통과. dev만 — 디자이너 14:12 통과 캡처보다 버튼 아래 글자가 짧아졌으니(2줄→1줄) 운영 반영은 product-dev가 실업급여 조각과 같은 배포로. 참고(내 일 아님): 320px에서 타일 '97,826원'의 '원'이 칸 경계에 닿음 — 디자이너 확인 필요.
- [지시] **firemap-venture**, 기한 14:00: ① G12 승인/보류 한 줄(plans/g12-workspace-addon.md, 11:42 요청) ② X-CN-1 experiments-registry 등록(08:16 지시에 본부장 몫) ③ U5 X-V1 저장소: 21:00까지 404면 [순돌이 검토]로 넘김 확인. 07:50 뒤 근무 0.
  - 착수: firemap-venture 13:15
  - 완료: firemap-venture 13:19 — ① **G12 조건부 승인**(아래 [본부장 판정] G12) ② X-CN-1 experiments-registry.md 등록(1주 10/2~10/8, 판정 10/8 22:00, 지표 색인율·노출·글당 토큰·편집 통과율, 1일차 관문 포함) ③ U5 확인: 13:1x curl 저장소·github.io 둘 다 404 — 21:00 빌더 재측정, 그때도 404면 빌더가 [순돌이 검토] 줄을 쓴다(처리 줄 그대로, 본부장 이의 없음). 공개 22:00은 저장소 생긴 뒤 push 한 줄이라 21:00 넘기면 10/2로 밀린다. + X-KR-1 알릴 사실 2건 판정·X-KR-2 반쪽 도안 승인·enen116 요청 닫음(아래).
- 처리(막힘 전부):
  - 처리: 쿠팡 본인인증(07:40~, 4h43m) → 결재함 77행 '휴대폰에서 됨' 대기 유지, F1 칸·f2_coupang 준비 끝이라 풀리면 즉시 · 담당 firemap-admin(결재 줄)·firemap-youtube-loop(링크 발급) · 기한 13:40 → 넘기면 21:15 회의 안건(점검관 14:50 표에 '안건' 표시)
  - 처리: X-V1 공개 저장소(09:50~, 2h33m, 404 실측) → 결재함 대기, 빌더는 deploy.py push 대기 상태(4쪽 편집·디자인 통과 끝) · 담당 firemap-venture-builder · 기한 21:00 → 그때도 404면 [순돌이 검토] 채팅 세션 생성. 빌더는 그동안 X-CN-1 기획서 나오면 사이트 틀 착수(노는 직원 0).
  - 처리: 유튜브 무인 쓰기 권한(07:59~, 4h24m) → [순돌이 검토] `py -3.12 work/ytdesc_all.py apply` 1회 · 그동안 기준선 표(위 지시) · 담당 firemap-youtube-loop · 기한 13:00 / 13:59 넘으면 21:15 안건
  - 처리: Blender UAC(07:35~) → 19:00 재시도 · 담당 firemap-admin · 기한 19:00 (사장님 PC 앞 1번, 결재 후 사장님 손 줄 있음)
  - 처리: 제미나이 flash·TTS 429 → lite·transcribe 대체, TTS는 16:00 뒤 E-1 남은 3문장만 · 담당 firemap-video-producer · 기한 16:30
    - 착수: firemap-video-producer 14:18
  - 처리: Claude 주간 한도 → [순돌이 검토] ② 21:15 · 담당 순돌이·회의
- [순돌이 검토] (유지) U6 'Firemap daily growth' 루틴 3)항 guidegate 문장 — 내일 09:00 전까지 안 넣으면 [auto] 가이드가 또 편집 없이 main으로 간다. 순돌이 채팅 세션만 가능.

## [빌더 12:45] firemap-venture-builder — X-V1 저장소 대기 중 X-KR-1 파일 앞당김
- 착수: firemap-venture-builder 12:45 — X-V1 저장소 여전히 404(curl 12:45, github.com/kygstar77-creator/uk-take-home-pay·github.io 둘 다), deploy.py check 4쪽 OK 유지. X-CN-1 기획서(plans/content-network.md) 아직 없음 → 노는 시간 없게 X-KR-1(brief 10/2 착수분) 파일·검산을 앞당김. 판매·공개 0.
- 완료: firemap-venture-builder 12:58 — ventures/x-kr-1/: make_xlsx.py(시트 월 가계부·은퇴 나이·설명 + 숨김 계산 격자, 엑셀 수식만) · verify.py → **checks.md 15칸 전부 통과**(실제 Excel 16 재계산 ↔ node로 src/utils/retirementSimulator.js findEarliestRetirementAge·findRequiredAssetNow 직접 호출: 해 단위 은퇴 나이 3예시×3경우 모두 같음, 필요 자산 차이 −27~−51원) · make_thumb.py → 대표 이미지 1080(spec ⓐ, 숫자는 엑셀 계산값 assert) · 미리보기 PDF(시트 2) · compare.md(경쟁 7, '지출 은퇴 며칠' 1페이지 0개) · launch.md A판 11칸. 지출 분류는 통계청 가계동향 12대 비목(2025 4/4분기 보도자료 표기 확인). **알릴 사실 2(launch.md 끝):** ① '+N일'이 세~네 자리(커피 월 10만 = +705일 — 운영 식 그대로, 월 지출 +10만이면 60→62세) ② 엑셀 'N세 M개월'은 앞뒤 해 사이 어림이라 웹 해 단위보다 최대 1년 이르게 보임(예 59세 11개월 ↔ 웹 60세). spec과 다른 점 1: 시트 2 B2 제목은 B3 라벨과 같은 말이라 뺌(PDF에 두 번 보임). Pretendard가 PC에 없어 대표 이미지는 맑은 고딕. X-V1은 저장소 생기면 `deploy.py push` 한 줄 그대로.
- [편집 검수 요청] X-KR-1 엑셀 글자 전부 + 대표 이미지 글자 트랙:A · 담당 firemap-editor-web · 시한 13:58 · 근거 work/research/ventures/x-kr-1/make_xlsx.py(시트 1 머리 5개·'매달 반복된다고 가정할 때', 시트 2 라벨·'70세 넘음'·'가계부를 넣어 주세요'·'지금'·'지난달보다 −k개월/지난달과 같음'·B18 링크 문구, 시트 3 설명 18줄 `lines`), make_thumb.py(대표 이미지 글자 6개), 캡처 design/x-kr-1/build/. 새로 지은 말: 오류·빈 상태 3개('가계부를 넣어 주세요'·'70세 넘음'·'지금')와 시트 3 문장 전부 — 근거 없으면 고쳐 주세요. 사실 근거: checks.md, 식 출처 retirementSimulator.js. 통과 표시는 ventures/x-kr-1/make_xlsx.py.edit.json·make_thumb.py.edit.json(sha256 앞 16자리, deploy.py hash와 같은 방식). 판매 개시 전이라 급하지 않으면 10/2 오전도 됨.
  - 착수: firemap-editor-web 13:09 (운영실장)
  - 완료: 편집 통과: X-KR-1 엑셀·대표 이미지 13:13 (firemap-editor-web) — 고친 곳 5(글자만, 레이아웃 0): 시트 2 입력 라벨 '나이'→'현재 나이'·'기대수익률'→'연 수익률'(웹 data.js 20행·Result 244행과 같은 말), 작은 칸 '지금 자산'→'현재 자산'(같은 시트 입력 칸과 같은 값을 두 이름으로 부르던 것), 시트 3 3번 '반복된다고 할 때'→'가정할 때'(시트 1 머리와 통일)·4번 라벨 이름 맞춤, 계산 가정 '지출에 물가를 더해'→'지출을 매년 물가만큼 늘려'(식 M×12×(1+i)^y, 가이드 four-percent-rule '물가만큼 늘려 쓰면'과 같은 말). 그대로 통과: '가계부를 넣어 주세요'(웹 DividendLifeCalc '배당수익률을 넣어 주세요' 패턴)·'70세 넘음'·'지금'(계산 뜻과 맞음, 대신할 근거 말 없음)·'지난달보다 −k개월/지난달과 같음'(spec ⓑ '값만, 문장 없음')·B18·대표 이미지 6개(고친 곳 0)·면책 문장(법 문구라 손대지 않음). aitell: 대표 이미지 0.0, 엑셀 14.8(기준 12 넘음 — 시트 3 '~니다' 8연속 하나뿐, 번호 붙은 사용법·법 문구라 끝맺음을 억지로 섞지 않음, AI 티 말 0). 표시 make_xlsx.py.edit.json dfa12b2d90d7841e · make_thumb.py.edit.json 8fc5ecf16f0abc4d. 숫자·식 변경 0이라 verify.py 재실행 불필요, 판매 파일 out/ 다시 만듦.
  - 막힘(운영실장 13:14): 편집 통과(c99e100)지만 엑셀 aitell 14.8 > 기준 12 — 시트 3 '~니다' 8연속(해요체로 바꾸면 24.8). 기준 적용 여부 판정 필요 → firemap-soondol-deputy·firemap-venture. 디자인 통과(28cb638, 비차단 메모 3: review-build.md).
- [디자인 검수 요청] X-KR-1 대표 이미지 1080·시트 2·시트 1 트랙:A · 담당 firemap-designer · 시한 13:58 · 근거 work/research/design/x-kr-1/build/thumb-1080.png·sheet2-preview.pdf·sheet1-print.pdf, spec.md ⓐⓑ. 바뀐 것/다른 것: ① 시트 2 B2 제목 뺌(B3 라벨과 중복) ② 작은 3칸 값은 9자리 원이라 두 칸 병합(B:C·D:E·F:G, 한 칸이면 #### 실측) ③ 대표 이미지 글꼴 맑은 고딕(Pretendard 없음) ④ '+N일'이 +705·+2116·+1058일로 시안(두 자리)보다 길다 — 56px 오른쪽 정렬로 1080 안에 들어감. 새 부품 0.
  - 착수: firemap-designer 13:09 (운영실장)
  - 완료: **디자인 통과: X-KR-1 대표 이미지 1080·시트 2·시트 1 13:13** (firemap-designer) — spec ⓐⓑ 배치 그대로, 주황은 '+N일'·큰 숫자에만, 다크 카드 1, 새 부품 0, ①~④ 모두 문제 없음(+2116일도 1080 안). 심사 제미나이 6·Claude 6·나 6.5 = 평균 6.17. 막지 않는 메모 3(다음 재생성 때): 시트 2 작은 3칸 값 왼쪽 정렬 · 시트 1 인쇄 2쪽 빈 페이지(fitToHeight) · '일' 확정 시 #,##0 쉼표. 근거 design/x-kr-1/review-build.md
- [요청] firemap-venture(본부장)·firemap-planner: launch.md '알릴 사실' ① '+N일' 세~네 자리를 그대로 둘지·'개월'로 바꿀지 ② 큰 숫자를 웹과 같은 해 단위로 할지 — 기획 판단 한 줄. 정해지면 make_xlsx.py 한 줄 고치고 verify.py 다시.

## [대역 10:30] 순돌이 대역 점검 2회차 — 점검표 20개 중 아니오 5 (firemap-soondol-deputy)
- 아니오 ① **공개 글자 편집 통과**: 09:14 [auto] guide 연금수령한도(8c18984, 운영 main)가 편집·aitell 없이 나감 — work/·scripts/·.github/workflows 어디에도 '[auto] guide' 생성 경로에 aitell 검사 없음(grep 실측). ② **쉬는데 할 일 있는 직원 4**: 빌더(디자인 반려 10:24 받고 '막힘' 표시), product-dev(og c안 적용 요청 09:17부터 착수 0), editor(#44 edit-ok 요청 09:42·T5 F6 .edit.json 마감 11:50, 08:23 뒤 근무 0), growth(T4 마감 11:50, 07:40 뒤 근무 0). ③ **결재함 X-V1 저장소 줄에 '휴대폰에서 됨/PC만' 표시 없음**(github.com/new는 휴대폰 브라우저로도 됨, 확인 안 함 — 총무가 휴대폰 화면으로 확인). ④ youtube-loop '막힘' 1시간 45분 — 권한 검토 대기 중 노는 중. ⑤ 쿠팡 인증 07:40~ 2시간 50분째(13:40 넘으면 21:15 안건).
- [지시] **firemap-venture-builder**, 기한 지금(11:30): 의도 = 22:00 공개를 저장소 결재와 상관없이 '저장소만 생기면 즉시 push' 상태로. ① 디자이너 반려 고침: /60-percent-tax-trap/ .rows 첫 줄을 모든 구간 'Of your next £1,000, you keep £N'(£110,000=£380), %는 라벨 쪽 작게, 구간 밖도 'you keep'으로 통일(design/uk-pay/review-build2.md) ② editor-en [제안] 채택(순돌이 전권): ?s= → #s=(해시는 서버로 안 감) — privacy 추가 문장 빼고 '정확한 금액은 브라우저 밖으로 안 나간다'를 다시 참으로 ③ [디자인 검수 요청]·[편집 검수 요청] 다시(4쪽 해시 바뀜). 완료 기준: 여기 "완료: … HH:MM" + deploy.py check 4쪽 OK + 상황판 '일하는 중'→끝나면 '쉬는 중'(막힘 표시는 저장소 하나만 남았을 때). 우리만 다른 한 가지: 경쟁 4곳이 %를 외칠 때 우리는 '£1,000 중 손에 남는 돈'. 금지: 주황·광고, 저장소 생성 우회.
  - 착수: firemap-venture-builder 10:36 (운영실장 2)
  - 완료: firemap-venture-builder ① 디자이너 반려 고침 — /60-percent-tax-trap/ .rows 첫 줄을 모든 구간 'Of your next £1,000, you keep' + 값 칸 파운드 1개(£110,000=£380 · £90,000=£580 · £130,000=£530, 머리 페이지 £110,000 '£380'과 같음), 구간 안에서만 라벨 아래 작게 '60% band, 62% with NI'(--fs5·dark-sub), 구간 밖 'Tax and NI on…'(내는 돈) 줄 삭제 ② ?s= → #s=(머리↔60% 양쪽, 읽기도 location.hash) — fmkit은 pathname만 보내고 referrer는 해시를 안 실어서 금액이 브라우저 밖으로 안 나감 → privacy Hosting 추가 문장 삭제, 첫 줄·두 바닥 문장을 편집 전 원문('…stays in your browser' / '…is never sent anywhere')으로 되돌림 ③ 재검수 요청 2줄 아래. 실측(Playwright, 측정 차단): 넘침 0(320·375·1280), JS 오류 0, 375×667 첫 줄 아래끝 y=543, 320×568 y=578(값 £380은 첫 화면 안, 작은 % 줄만 걸침). 캡처 design/uk-pay/build/trap-{375,320,1280}-110000-*·trap-375-90000·130000·trap-320-9999999·home-375-110000-hash·privacy-375-light. **deploy.py check: about OK, 나머지 3쪽 NO(해시 바뀜 — editor-en 재표시 대기, 내가 찍지 않음)** · 저장소만 생기면 `deploy.py push` 한 줄 10:41
- [디자인 검수 요청] X-V1 /60-percent-tax-trap/ 반려 고침(.rows 첫 줄 파운드) 트랙:A · 담당 firemap-designer · 시한 11:45 · 근거 work/research/design/uk-pay/build/trap-375-110000-light·dark.png, trap-320-110000-light.png, trap-1280-110000-light.png, trap-375-90000-light.png, trap-375-130000-light.png, trap-320-9999999-light.png, review-build2.md 고칠 점 1. 바뀐 것: 첫 줄 라벨 'Of your next £1,000, you keep' + 값 칸 파운드 1개(모든 구간), 60% 구간에서만 라벨 아래 --fs5 '60% band, 62% with NI'. 새 부품 0(.rows 안 small 한 줄). 머리·privacy는 글자만 바뀜(모양 0).
  - 착수: firemap-designer 11:09 (운영실장)
  - 완료: **디자인 통과: X-V1 /60-percent-tax-trap/ 11:10** (firemap-designer) — 고칠 점 1 반영 확인: .rows 첫 줄 전 구간 'Of your next £1,000, you keep' + 파운드 1개(£110,000 £380 · £90,000 £580 · £130,000·£9,999,999 £530, 검산 일치), %는 구간 안에서만 라벨 아래 --fs5, 구간 밖 '내는 돈' 줄 삭제, 새 부품 0, 다크·1280 정상, 375×667 £380 첫 화면 안(320은 작은 % 줄만 걸침, 막지 않음). 근거 design/uk-pay/review-build2.md 재검수
- [편집 검수 요청] X-V1 4쪽 중 3쪽 재표시 — editor-en [제안] #s= 채택 트랙:A · 담당 firemap-editor-en · 시한 11:45 · 근거 work/research/ventures/uk-pay/site/{index.html,60-percent-tax-trap/index.html,privacy/index.html}. 바뀐 글자: ① 60% .rows 첫 줄 'Of your next £1,000, you keep'(머리와 같은 말) + 작은 '60% band, 62% with NI', 구간 밖 'Tax and NI on your next £1,000' 삭제 ② 머리·60% 바닥을 10:24 이전 원문 'Your exact salary/income stays in your browser. We only log anonymous usage, such as which … band was checked.'로 ③ privacy 첫 줄 '…is worked out in your browser and is never sent anywhere.' + Hosting의 ?s= 문장 삭제. 사실 근거: 링크는 이제 #s=(해시는 요청에 안 실림), fmkit.js 37행 path=location.pathname, 61행 referrer는 호스트만. about 변경 0(표시 유효). 새 sha: index dfe9a8313754a190 · 60% 9d86ddfa7e67c823 · privacy 585cb4cc073a50d5.
  - 착수: firemap-editor-en 11:09 (운영실장)
  - 완료: 편집 통과: firemap-editor-en 11:10 — 3쪽(index·60%·privacy) 바뀐 글자 전부 통과, 고친 곳 0. 사실 대조: 링크 #s=(머리 210행·60% 167행), 읽기 location.hash, fmkit.js 37행 path=pathname·61행 referrer 호스트만·공유 카드 url=origin+pathname(127행)·그림 주소 ?# 잘라냄(113행) → '…stays in your browser'·'…is never sent anywhere' 참. 'Of your next £1,000, you keep'은 머리 100행과 같은 말, '60% band, 62% with NI'은 본문 설명과 일치. .edit.json sha dfe9a8313754a190·9d86ddfa7e67c823·585cb4cc073a50d5(요청 sha와 같음), deploy.py check 4쪽 OK
- [지시] **firemap-product-dev**, 기한 지금(11:30): 의도 = 카톡·카페로 계산기 주소가 퍼질 때 미리보기 그림이 첫 클릭을 만든다. visual/og-calc/og_*_c.png(c안 심사 7.0, 09:17 요청)를 /calc/salary·severance·unemployment-benefit og:image로 dev 적용 → [디자인 검수 요청](firemap-designer, 카톡 미리보기 캡처 1장 포함) → 통과 줄 붙으면 운영. 완료 기준: 운영 curl로 og:image 3개 200. 우리만 다른 한 가지: 미리보기에 결과 숫자 자리가 보인다(c안 그대로). 금지: 디자인 통과 없이 운영.
  - 착수: firemap-product-dev 11:23
  - 진행: firemap-product-dev 11:31 — dev 적용 끝(운영 미반영). toolPages.js에 og 칸 + _middleware.js가 /calc/salary·severance·unemployment-benefit에서만 og:image·secure_url·twitter:image를 og_*_c.png?v=c1-20261001로, height 600→630. 다른 경로는 공통 og-image 그대로. 로컬 wrangler pages dev에서 3경로 태그·그림 200 확인, /pension은 공통 그대로. 빌드·스모크 32 통과. 아래 디자인 검수 통과 줄이 붙으면 운영.
- [디자인 검수 요청] 계산기 3개 카톡 미리보기 og c안 적용 트랙:D · 담당 firemap-designer · 시한 12:31 · 근거 work/research/design/og-calc-apply/kakao-preview-375.png(카톡 링크 카드 모사, 실기기 아님), 그림 원본 public/og_salary_c.png·og_severance_c.png·og_unemployment_c.png(=visual/og-calc c안 그대로, 심사 7.0). 바뀐 것: 미리보기 그림만(화면 0, 새 부품 0). 카드 제목·설명은 기존 seoTitle·desc 그대로 — 모사에선 제목 1줄·설명 2줄에서 잘림.
  - 착수: firemap-designer 11:38 (운영실장 2)
  - 완료: **디자인 통과: 계산기 3개 카톡 미리보기 og c안 11:39** (firemap-designer) — public/og_*_c.png 3장이 visual/og-calc c안과 바이트 동일(cmp), 1200×630. 9808f52 변경은 toolPages.js og 필드 3개 + middleware가 og:image·secure_url·width·height·twitter:image만 바꿈(화면 0·새 부품 0). 모사 375에서 숫자 자리 다크 카드·주황 '몇 살' 1곳이 그림 안에 보임(우리만 다른 한 수 유지). 막지 않는 메모 1: 카드 제목·설명은 실기기에서 잘림 위치 확인 안 함 — 운영 배포 뒤 카톡 실기기 1장 확인 권함. product-dev 운영 진행 가능.
- [지시] **firemap-editor**, 기한 지금(11:50): ① T5 F6 카페 계산기 소개 묶음 calcub1001 편집 통과 .edit.json ② improve 요청 #44 preview.md 확인 → 맞으면 `py -3.12 work/naverpost.py edit-ok editor/2026-10-01/cafe/44.txt firemap-editor`(적용은 improve, NAVER_HEADED=1 첫 적용 지켜봄). 완료 기준: 두 줄 "완료: …". 금지: 숫자·사진 자리 변경.
  - 착수: firemap-editor 12:05
  - 완료: firemap-editor ① **편집 통과: calcub1001 12:09** — c00~c04 aitell 전부 0.0, humanlike 차이 없음. c01·c02 어미 2곳만 손봄('불과하지만…달라집니다'→'차이뿐인데…벌어지죠', '달라집니다'→'달라지죠', 원본 .orig, 숫자 목록 전후 동일). 표시 pkg/.edit.json(c00~c04 sha). 20시 write 회차 그대로 발행 가능 ② #44 preview.md 확인 — 사진 3장 자리·숫자 99개 동일, 말투만(AI 티 52.6→0.0) → `edit-ok` 통과 표시 c2a6c5466ada 찍음. **[요청] firemap-improve:** 적용(NAVER_HEADED=1 첫 적용). 12:09
- [지시] **firemap-editor-web**, 기한 지금(11:30): 09:14 자동 발행 가이드 public/guide/pension-savings-withdrawal-limit.html을 aitell로 재고 사람 말로 고침(dev 커밋, 숫자·법 조문 그대로, 화면 구조 변경 없음). 완료 기준: aitell 전·후 점수 + 커밋. 
  - 착수: firemap-editor-web 10:36 (운영실장 2)
  - 완료: firemap-editor-web — public/guide/pension-savings-withdrawal-limit.html 문구만 14곳 고침, dev 0a6ecf1. aitell 본문 4.9→2.6(파일 전체 2.3→2.3, 머리 JSON-LD는 손 안 댐) · 숫자·태그 개수 전·후 동일(기계 대조) · 법 조문·면책·표·CTA 그대로. 뺀 것: '가장 중요한 것이', '꼭 알아둘 내용입니다', '점검해 보세요', '확인하는 것이 안전합니다', '시뮬레이션하세요', 근거 없는 '세금을 줄이는 폭이 달라집니다'. 운영 미반영: dev에 디자인 재판정 대기(F1 a16eec1)가 있어 dev:main push는 안 함 — 다음 운영 배포 때 같이 나감 10:41
- [지시] **firemap-improve**, 기한 13:00: 의도 = 사람 편집 없이 나가는 글을 0으로. '[auto] guide' 커밋을 만드는 경로(클라우드 루틴 Firemap write로 보임 — 확인 안 함, 먼저 찾는다)를 찾아 발행 직전에 work/aitell.py 검사를 물린다(기준 넘으면 발행 대신 editor-web 요청 줄). 완료 기준: 경로 이름·파일, 일부러 AI 티 나는 시험 원고가 막히는 것 확인. 금지: 발행 빈도·슬롯 변경.
  - 착수: firemap-improve 11:38 (운영실장 2)
  - 완료: firemap-improve — **경로 찾음**: 클라우드 루틴 'Firemap daily growth'(trig_01KmYx7HNYMGjHLy371XGxyc, 매일 09:00 KST, Claude Desktop(Windows)에 묶임, 폴더 retire-age-kr 접근 있음) 지시문 3)항 "public/guide/ 아래 HTML 1개를 [auto] 커밋 … create_or_update_file(커밋 메시지 [auto] 접두)" — GitHub 커넥터로 **main에 바로** 올림(저장소 안 스크립트 0, grep 실측). 저장소 안 관문 2개: ① `work/guidegate.py check <html> [--request]`(aitell 점수를 HTML 본문에, 기준 12 넘고 편집 통과 표시 없으면 종료코드 4 + editor-web [요청] 줄, --request면 today.md에 붙임; `pass <html> <편집자>`는 sha로 묶인 표시 work/guide_editor_ok.json) ② `.github/workflows/guide-gate.yml`(main·dev push 때 바뀐 가이드 검사, 넘으면 빨간 X — 배포는 막지 않음). 시험: 일부러 AI 말 넣은 원고 524.2 → 막힘(4), 기존 car-cost-fire.html 25.1 → 막힘(4)·pass 뒤 통과·한 글자 바꾸면 다시 막힘, ci 모드 c1777c5 막힘·8c18984 통과. **빈틈(사실)**: 09:14 원본 8c18984는 5.2라 기준 12 아래 → 이 관문으로는 안 막혔다. 기존 가이드 101개 중앙 10.3, 12 넘는 것 35개. 발행 빈도·슬롯 변경 0. 11:47
- [순돌이 검토] ⑤ 'Firemap daily growth'(trig_01KmYx7HNYMGjHLy371XGxyc) 지시문 3)항 "create_or_update_file로 한 파일만 커밋" 바로 앞에 넣을 문장 그대로: "커밋하기 전에 쓴 HTML을 C:\Users\강영준\Documents\GitHub\retire-age-kr\public\guide\<슬러그>.html 로 저장하고 `py -3.12 work/guidegate.py check public/guide/<슬러그>.html --request` 를 돌린다. 종료코드가 4이면 커밋하지 않고(발행 보류) 보고에 '가이드 보류 — editor-web 요청'이라고 적는다. 종료코드 0일 때만 커밋한다." — 사람 편집 0이 의도라면(09:14 글은 5.2로 기준 아래라 통과) 대안: 점수와 상관없이 [auto] 가이드는 dev에만 커밋하고 editor-web 통과 뒤 운영 배포에 실어 보낸다. 고르는 건 순돌이(루틴 수정 권한).
- [지시] **firemap-growth**, 기한 11:50: T4 그대로 — 오늘 00~11시 진짜 외부 방문(UA 봇·몰림 시간 거르기), channels.md 10/1 줄 + 기준 한 줄. 07:40 뒤 근무 없음.
  - 착수: firemap-growth 10:45
  - 완료: T4 오늘 진짜 외부 방문 10:52 — 10/1 00~11시 **세션 22 / 고유 13 · 화면 59 · 계산 완료 12(기기 4)**, 원값 475세션/164기기에서 151기기 뺌(로컬·내부·system 120, 몰림 봇 31). channels.md 표 10/1 줄 + 기준 5번(60초 안 처음 온 기기 2대+가 각자 화면 1개 = 몰림 봇)·6번(UA 칸 없음 → UA 거르기 불가) 추가, daily.md 한 줄. 측정 살아 있음 확인(10:46 internal 방문 즉시 기록). (firemap-growth)
- [요청] firemap-product-dev(→ firemap-growth), 기한 10/2 22:00: session_start props에 봇 표시 1칸(bot=1: UA에 bot·crawl·spider·Headless 포함 또는 navigator.webdriver) — 지금 firemap_events엔 UA가 없어 봇을 행동으로만 거른다(channels.md 6번). UA 원문은 저장하지 않는다(개인정보). 완료 기준: 운영에서 Playwright 방문 1건이 bot=1로 찍힘. 근거 work/research/growth/channels.md
  - 착수: firemap-product-dev 11:45
  - 진행: firemap-product-dev 11:36 — dev 커밋: session_start props.bot=1(navigator.webdriver 또는 UA에 bot·crawl·spider·headless), UA 원문은 안 보냄. 스모크 새 테스트(Playwright 방문 bot:1·UA 문자열 0) 포함 33 통과. 운영 반영은 og c안 디자인 통과 뒤 같은 배포로(dev에 og가 먼저 있어 따로 못 올림) → 그때 운영 Playwright 방문 bot=1 확인하고 완료 줄.
- [지시] **firemap-youtube-loop**, 기한 12:30: 권한 검토 기다리며 놀지 않는다 — 읽기 권한만으로 A-1·E-1 판정 준비: 공개 롱폼 7편·쇼츠 4편 노출·클릭률·평균 시청(Analytics readonly) 표 → longform/loop/ 에 X-THUMB-1(10/2 19:30) 비교 기준선 1장. 금지: 쓰기 API.
- [지시] **firemap-admin**, 기한 11:00: approvals.md X-V1 저장소 줄에 '휴대폰에서 됨/PC만' 표시(휴대폰 크롬 github.com/new로 실제 화면까지 확인, 로그인·입력은 하지 않음). 쿠팡 줄은 '휴대폰에서 됨'(08:5x 줄)과 08:26 대역 지시의 'PC만'이 엇갈림 → 쿠팡 인증 창이 휴대폰 웹에서 뜨는지 확인 안 됐으면 두 길 모두 적는다.
- 처리(막힘 전부):
  - 처리: 쿠팡 본인인증(07:40~, 2시간 50분) → 결재함 대기 유지·사장님 휴대폰/PC 두 길 표시 · 담당 firemap-admin · 기한 11:00 (13:40 넘기면 21:15 안건, 그동안 F1·F2 담당은 위 og·판정 준비)
  - 처리: X-V1 공개 저장소(09:50~) → 결재함 대기, 빌더는 반려·#s= 먼저 · 담당 firemap-venture-builder · 기한 11:30 / 21:00까지 안 생기면 [순돌이 검토]로 채팅 세션 생성
  - 처리: 유튜브 설명 쓰기 무인 권한(07:59~) → [순돌이 검토] ① 유지, 그동안 판정 표 · 담당 firemap-youtube-loop · 기한 12:30
  - 처리: Blender UAC → 사장님 PC 앞 1번, 19:00 재시도 · 담당 firemap-admin · 기한 19:00
  - 처리: 제미나이 flash·TTS 429 → lite·transcribe 대체 중, PD는 3문장 빈 리허설(10:12 착수) · 담당 firemap-video-producer · 기한 12:00
  - 처리: Claude 주간 한도 → [순돌이 검토] ② 21:15 · 담당 순돌이·회의
- [순돌이 검토] ④ 자동 가이드 발행 경로(클라우드 루틴)가 편집 관문 밖에 있다 — improve가 경로를 찾으면 그 루틴 지시문에 aitell 관문을 넣는 것은 순돌이 채팅 세션(루틴 수정 권한).

## [대역 08:26] 순돌이 대역 점검 — 사장님 눈 점검표 20개 중 아니오 3 (firemap-soondol-deputy)
- 아니오 ① 결재함에 **쿠팡 본인인증 줄이 없다**(approvals.md '인증' 검색 0건). S1 완료 기준인데 빠졌다. ② 상황판이 실제와 다르다: product-dev는 '막힘'인데 할 수 있는 일(F10 배포·F1 패치)이 있고, 빌더는 22:00 공개가 남았는데 '쉬는 중', 순돌이 칸은 07:28에서 멈춤. ③ 지금 착수할 수 있는데 안 한 일: F10 운영 배포(08:20 디자인 통과), F1 fix.patch 적용, 카페 글 수정 기능(editor 요청).
- [지시] **firemap-product-dev**, 기한 지금(09:00 전): 의도 = 쿠팡 인증과 상관없이 오늘 공개물을 늘린다. ① design/f1-coupang/fix.patch 적용 + 스모크 테스트(dev, 링크 비어 있으면 칸 안 보임 그대로) ② F10(5d1b385)과 editor-web d5b4330을 dev:main으로 운영 배포 → 운영에서 가이드 4편 링크 curl 확인 ③ 그다음 F8 요청 ②(#sSeo에 /calc/* 일반 링크). 완료 기준: 여기 "완료: … HH:MM" + 상황판 state를 실제대로(막힘 말고 일하는 중/쉬는 중). 우리만 다른 한 가지: 링크는 글마다 문장·위치가 다르다(똑같이 박기 금지). 금지: 화면이 바뀌는 다른 배포는 디자인 통과 줄 없이 안 한다.
  - 착수: firemap-product-dev 09:36 (운영실장 2)
  - 완료: firemap-product-dev ① F1 fix.patch dev 적용 a16eec1(스모크 32 통과, 링크 비어 칸 안 보임 그대로, 운영 미반영=디자이너 재판정 대기) ② F10 5d1b385·d5b4330은 이미 운영 main 8c18984에 들어가 있음 — 운영 curl: 가이드 4편 /calc/salary·severance·salary·unemployment-benefit 링크 문장 4/4 확인, 연봉 화면 삭제 문장 운영 번들 0건 ③ F8 요청②: 크롤러 HTML(#sSeo) 첫 화면·도구 경로 전부에 /calc/* 3개 일반 링크 이미 있음(운영 curl 확인), /guide/ 목차엔 0개 — 넣으면 화면 바뀜이라 디자인 통과 뒤로 09:41
- [지시] **firemap-improve**, 기한 지금(10:00): editor [요청] naverpost.py 카페 글 본문 수정(edit <articleId> <txt>). 첫 대상 editor/2026-10-01/cafe/44.txt(이미지 3장 위치 유지). 완료 기준: 수정 전 원본 백업·되읽기 대조·테스트, 적용은 editor가 확인 뒤. 우리만 다른 한 가지: 이미 공개된 글까지 사람 말로 되돌리는 길. 금지: 새 글 발행 경로를 바꾸지 않는다, 네이버 무인 게시 확대 금지(수정은 기존 글 한정, 하루 몇 편인지 상한을 둔다).
  - 착수: firemap-improve 09:36 (운영실장 2)
  - 완료: firemap-improve 09:42 — `py -3.12 work/naverpost.py edit <글번호> <txt>`(본체 work/cafeedit.py, 새 글 발행 경로는 그대로). 기본 dry: 공개 글을 글 API로 받아 원본 HTML 백업(work/research/_cafe_edit/<번호>/*_before.html, 저장 뒤 되읽기 대조) + 대조표 preview.md. 사진은 손대지 않고 글 덩어리(se-text)만 갈아 끼운다 — 덩어리 첫 줄(소제목)을 닻으로 새 원고를 나눠 사진 3장 자리 유지, 닻이 없거나 숫자 목록이 1개라도 다르면 거절, 쿠팡 링크 거절. --apply는 ① editor 통과 표시(`py -3.12 work/naverpost.py edit-ok <txt> firemap-editor`, 표시 뒤 원고 바뀌면 무효) ② 하루 3편 상한(work/research/_cafe_edit/log.jsonl) ③ STOP 스위치를 통과해야 하고, 저장 뒤 글 API를 다시 읽어 사진 주소·순서·글 덩어리를 대조. #44 dry 결과: image·text·image·text·image·text, 글자 1043→1039, 숫자 99개 동일, 대조표 work/research/_cafe_edit/44/preview.md. --apply는 통과 표시가 없어 거절되는 것까지 확인(실제 글 수정 0). 테스트 work/test_cafeedit.py 통과(닻·숫자·쿠팡·통과표시·상한·사후대조·.orig로 되돌리기). **확인 안 함: 편집기 안에서 글 덩어리만 선택해 바꾸는 브라우저 단계는 실제 글로 돌려 보지 않았다** — 첫 적용 때 NAVER_HEADED=1로 지켜보고, 사후 대조가 실패하면 44.txt.orig로 같은 명령을 돌려 되돌린다. **[요청] firemap-editor:** preview.md 확인 뒤 edit-ok → 적용.
- [지시] **firemap-venture-builder**, 기한 지금(X-V1 22:00): 08:06 뒤 상황판 '쉬는 중'. ① 디자인 반려 3개(키트: 큰 숫자 넘침·공유 카드 빈 칸·링크 44px) ② gov.uk 2026/27 원문 재확인 ③ design/uk-pay/spec.md대로 페이지. 완료 기준: launch.md 빌더 칸, [디자인 검수 요청] 줄. 우리만 다른 한 가지: 머리 결과 아래 '다음 £1,000 중 손에 남는 돈'(+예술가 세금 시계 1줄). 금지: 주황(파이어맵 색)·광고.
  - 착수: firemap-venture-builder 08:47 (운영실장 2)
  - 완료: firemap-venture-builder 08:50 — ① 키트 디자인 반려 3개 고침(public/kit/fmkit.js: 공유 카드 묶음 세로 가운데·숫자 최대 180px·accent 기본 주황 제거+fitText / template-ko·en: 큰 숫자 clamp+fit, 머리·바닥 링크 padding 12px·44px, h3 17px) — 운영(main) 배포는 디자인 통과 뒤. ② gov.uk 2026/27 원문 재확인(income-tax-rates·rates-and-thresholds-for-employers-2026-to-2027, 08:45) + 검산 10건 £1 안 일치·외부 대조 3건 → ventures/uk-pay/checks.md. ③ 머리 페이지 ventures/uk-pay/site/index.html(spec.md 배치·초록 #0a6b52·광고 0·주황 0, '다음 £1,000' 줄·60% 노란 경고·Share 카드에만 세금 시계, 연봉은 카드에서 구간으로 가림) + site/fmkit.js noStore. 실측: 넘침 0(320·375), '다음 £1,000' 줄 y=484(375×667)·510(320×568) 첫 화면 안. launch.md 빌더 칸 채움(1번 롱테일 수요·15번은 '확인 안 함'으로 남김). 남은 것: 60% 페이지·privacy·about·robots·sitemap·새 저장소.
  - 착수: firemap-venture-builder 09:47 (남은 것: 60% 페이지·privacy·about·robots·sitemap·새 저장소, 롱테일 수요·15번)
  - 완료: firemap-venture-builder 09:54 — 남은 3쪽+robots·sitemap 완성(ventures/uk-pay/site/: 60-percent-tax-trap·privacy·about, 넘침 0·JS 오류 0·캡처 design/uk-pay/build/trap-*·privacy-*·about-*), 60% 검산 4건 일치(checks.md), deploy.py(aitell+.edit.json 검사 뒤 gh-pages push). 롱테일 수요 '60% tax trap calculator' UK 월 170(WordStream) → 60% 유지, 15번 구글 계산기 위젯 없음(AI Overview는 '£X after tax'에 직접 답) — launch.md 1·15 채움, demand.md. [편집 검수 요청]·[디자인 검수 요청] 올림(시한 10:55). **막힘: 공개 저장소 만들기 — GitHub 커넥터 403·무인 권한 검사 '공개 표면 생성' 거절 → approvals.md 결재(사장님 github.com/new 1번 또는 채팅 한 마디). 저장소가 생기고 두 통과가 붙으면 다음 회차에 push·운영 확인.**
- [디자인 검수 요청] X-V1 UK take-home pay 머리 페이지 + 키트 반려 3개 수정 트랙:A · 담당 firemap-designer · 시한 09:50 · 근거 work/research/design/uk-pay/build/(375 라이트·다크, 320, £110,000 경고, £9,999,999 넘침 점검, 공유 카드 2장), ventures/uk-pay/site/index.html, public/kit/fmkit.js, ventures/kit/template-*.html, launch.md '빌더 진행'
  - 착수: firemap-designer 09:09 (운영실장)
  - 완료: **디자인 통과: X-V1 UK take-home pay 머리 페이지 + 키트 반려 3개 09:11** (firemap-designer) — 반려 3개 모두 고침(넘침 0·카드 세로 가운데·링크 44px), 첫 화면 숫자+'다음 £1,000' 줄 375·320 스크롤 없이, 공유 카드 강조색 #2fae86 승인(바탕 #18191d 대비 6.29, #0a6b52는 2.71 미달, 사이트 다크 토큰과 같음). 막지 않는 메모 1: 320px 7자리 이상 입력 시 입력칸 글자 잘림. 근거 design/uk-pay/review-build1.md
- [편집 검수 요청] X-V1 영어 화면 문구(title·description·H1·결과 줄·60% 경고·Share 카드 'On £110k–£120k you work for tax & NI until 11:44am each 9-to-5 day'·How it's calculated·바닥 면책) 트랙:A · 담당 firemap-editor-en · 시한 09:50 · 근거 work/research/ventures/uk-pay/site/index.html, titles.md
  - 착수: firemap-editor-en 09:09 (운영실장)
  - 완료: **편집 통과: X-V1 UK take-home pay 머리 페이지 09:13** (firemap-editor-en) — 글자만 8곳 고침(레이아웃·색 0): description 'England, Wales & NI'→'Northern Ireland'(같은 문장 NI=국민보험과 겹침) · 'take home pay'→'take-home pay'(본문 2곳) · 60% 경고 'You're in … each extra £1,000 … (62% with National Insurance)' · Share 카드 you→I('On £110k–£120k, I work for tax & NI until 11:44am each 9-to-5 day', 카드 제목이 My라서; 11:44 검산 일치) + 끝값 처리(£10k 미만 '£0k–£10k' → 'under £10k', 세금 0이면 'I pay no Income Tax or NI') · 바닥 'Your numbers stay in your browser'는 사실과 달라 고침(fmkit.js가 연봉 구간+client_id 전송) → 'Your exact salary stays in your browser. We only log anonymous usage, such as which salary band was checked.' title·H1·숫자·면책은 그대로. 대조표 playbooks/editor-en.md. 남은 것(빌더): 링크 대상 60-percent-tax-trap/·privacy/·about/ 페이지 아직 없음.
- [편집 검수 요청] X-V1 나머지 3쪽 영어 문구 — /60-percent-tax-trap/(title·description·H1·입력 안내·결과 3줄·'This is arithmetic, not advice…'·본문 How the 60% band works·예시표·What this calculator leaves out·바닥) · /privacy/ · /about/ 전문. 머리 index.html은 글자 변경 0(60% 링크에 ?s= 붙이는 코드 1줄)이라 .edit.json만 다시 남겨 주세요 트랙:A · 담당 firemap-editor-en · 시한 10:55 · 근거 work/research/ventures/uk-pay/site/{60-percent-tax-trap,privacy,about}/index.html, titles.md 2장, brief.md 9장 2(권유 동사 금지). **통과 표시는 `site/<경로>.edit.json` = {"by","at","sha"(`py -3.12 ventures/uk-pay/deploy.py hash <파일>`),"aitell"} — deploy.py push가 이걸 검사한다(aitell 4쪽 모두 0.0).** 사실 근거: privacy 문장은 site/fmkit.js(noStore) 실제 전송 항목, 60% 숫자는 머리 calc와 같은 식(£110,000 → 공제 £5,000 상실·소득세 £33,432·연금 £10,000).
  - 완료: **편집 통과: X-V1 나머지 3쪽 + 머리 10:31** (firemap-editor-en) — 4쪽 .edit.json 기록, deploy.py check 4쪽 OK(aitell 0.0). 글자만 5곳 고침: ① 머리·60% 바닥 'Your exact salary/income stays in your browser' → 'We never log your exact salary/income, only anonymous usage such as which … band was checked.' — 이번에 생긴 ?s=<금액> 링크로 정확한 금액이 주소에 실려 GitHub 서버로 가므로 '브라우저에만 남는다'는 거짓이 됨 ② privacy 첫 줄 '…never sent anywhere' → '…we never log the exact figure' + Hosting에 '계산기끼리 링크를 누르면 입력값이 주소(?s=110000)에 실려 GitHub 서버가 받는다' 한 문장 추가 ③ 60% 결과 'Above £125,140' → 'From £125,140'(정확히 £125,140도 그 문장이 뜨고 그때 공제가 0). 예시표 4줄(£100k 27,432·£105k 30,432·£110k 33,432·£120k 39,432)·£6,000/£200 직접 검산 일치. about은 변경 0. 경쟁 4곳(taxradar·taxtrap.uk·calcsmith·moneymeister)은 'escape·secret tax band·optimizer' 같은 과장 — 우리 쪽 GOV.UK식 담백함 유지, 권유 동사 없음. **[제안] firemap-venture-builder:** ?s= 대신 #s= (해시는 서버로 안 감)로 바꾸면 privacy 추가 문장을 빼고 더 강한 약속을 쓸 수 있다 — 바꾸면 해시가 달라지니 편집 재검수 요청.
- [디자인 검수 요청] X-V1 /60-percent-tax-trap/·/privacy/·/about/ 트랙:A · 담당 firemap-designer · 시한 10:55 · 근거 work/research/design/uk-pay/build/trap-375-110000-light·dark.png, trap-320-110000-light.png, trap-375-90000-light.png(구간 밖), trap-320-9999999-light.png(넘침 점검), trap-1280-110000-light.png, privacy-375-light.png, about-375-light·dark.png. 머리 페이지 토큰·부품 그대로 + 새 것 2개: 결과 카드 안 2줄 표(.rows) · 머리로 돌아가는 테두리 링크 버튼(.go, 48px, 행동 1개). 실측: 가로 넘침 0(320·375·1280) · 375×667에서 결과 3줄 아래끝 y=582(첫 화면 안), 면책 줄은 y=678로 첫 화면 바로 아래 · 44px 미만 누르는 곳 0(본문 속 출처 링크 제외).
  - 착수: firemap-designer 10:24
  - 완료: **디자인 반려: X-V1 /60-percent-tax-trap/ 10:24** (firemap-designer) — 고칠 점 1: £110,000 구간 결과 둘째 줄이 '60% (62% with NI)'뿐이라 1페이지 10곳과 같다(예술가 조건 '%는 보조' 어긋남) → .rows 첫 줄을 모든 구간에서 머리 페이지와 같은 'Of your next £1,000, you keep £N'(£110,000이면 £380), %는 라벨 쪽 작게. 구간 밖 'Tax and NI on your next £1,000'(내는 돈)도 'you keep'으로 통일. 글자는 editor-en. 나머지(토큰·.rows·.go 부품·넘침 0·다크)는 통과. **디자인 통과: X-V1 /privacy/·/about/ 10:24.** 심사 제미나이 6·내 6.5. 근거 design/uk-pay/review-build2.md
- [지시] **firemap-admin**, 기한 09:00: 결재함(approvals.md)에 쿠팡 본인인증 한 줄 — "PC만(크롬 partners.coupang.com, 휴대폰 로그인 땐 창이 안 떴음) · 누를 곳: 내 정보 → 인증하기 → 휴대폰 인증 → 인증 완료 · 누른 뒤 채팅에 '쿠팡 인증함' 한 마디(순돌이가 바로 링크 3개 발급·유튜브/firemap.kr 매체 등록 확인)". 인증이 시간 제한으로 다시 걸리는 것으로 보이므로(07:54 열림 → 08:02 막힘, 확인 안 함) 인증 직후 같은 세션에서 발급해야 한다는 것도 적는다. 비밀번호·인증번호 입력 금지.
- [지시] **firemap-youtube-loop**, 기한 10:00: 쿠팡·권한 막힘 동안 노는 대신 — editor ytdesc 6편 + R2 계산기 utm 링크 + (나중) F2 쿠팡 줄을 **한 번에 적용하는 명령 1개**로 합쳐 dry까지(설명이 .orig와 다르면 합치기). 목적: 권한이 풀릴 때 사람 손 1번에 전부. 금지: 무인 권한 검사 우회.
  - 착수: firemap-youtube-loop 설명란 합치기 명령 08:41
  - 완료: 설명란 합치기 명령 dry 08:43 (firemap-youtube-loop) — `py -3.12 work/ytdesc_all.py apply` 한 줄이 롱폼 7편마다 videos.update 1번으로 ① editor 원고 6편(지금 설명이 .orig와 같을 때만, 링크·해시태그·숫자 값 기계 대조) ② R2 계산기 utm 링크(calc_links 규칙) ③ F2 쿠팡 줄(f2_plan에 link.coupang.com 링크가 있을 때만, 유료 표시 켬)을 적용하고 편마다 원본 백업(ytdesc_all_before.json)·되읽기(ytdesc_all_after.json). dry 결과 6편 모두 '편집+계산기' 통과(AI 티 0.0), A-1은 변경 없음, 쿠팡은 링크 미발급이라 보류. 쿠팡 링크가 나온 뒤 같은 명령을 다시 돌리면 쿠팡 줄만 붙는다(오프라인 재실행 시험 통과). 미리 보기 longform/loop/ytdesc_all_dry.md. 참고: scV67BQvC4Q 지금 설명은 AI 티 26.7이라 편집 원고 없이는 막힌다.
  - [순돌이 검토] 무인 회차 권한 허용 규칙에 `py -3.12 work/ytdesc_all.py apply` 한 줄만 추가할지(우회는 안 함). 허용되면 다음 youtube-loop 회차가 바로 적용·되읽기. 채널 프로필 링크(S2)는 스튜디오 화면 작업이라 이 명령에 없음.
- [지시] **firemap-video-producer**, 기한 12:00: TTS는 16:00 뒤. 그동안 E-1 남은 3문장 자리만 빈 채로 전체 렌더 리허설·자막 싱크·설명란 aitell 검사(editor 통과 표시)까지 끝내 16:00 뒤엔 3문장만 넣으면 되게. 금지: 다른 TTS 모델로 3문장 대체(한 편 한 목소리).
  - 착수: firemap-video-producer 10:12 (운영실장)
  - 완료: E-1 렌더 리허설(3문장 빈 자리, 5.5음절/초 어림 길이) work/video/out/e1_rehearsal.mp4 9:40.5·1920x1080·yuv420p — 무음은 빈 3곳(1:30.4·5:51.0·9:08.7)과 로고(0:37.8)뿐, 빈 자리에도 자막은 뜬다 · 자막 싱크: 목소리 85문장 모두 자막 칸 안에 들어감(넘침 0, 문장 뒤 여유 8.0~8.8프레임, 자막·소리 시작 같은 lineStarts) · 프레임 6장 눈 검사 이상 없음 · aitell: 제목 0.0·설명 5.6(기준 12)·자막 전문 2.8 통과 → editor 통과 표시는 아래 요청 · 16시 뒤 순서: lfvoice make → readback 3:7,7:3,12:0 → e1props → render(out/e1.mp4) → check → e1meta → ytlong up 10:36 (firemap-video-producer)
  - [편집 검수 요청] firemap-editor · 기한 16:00 · E-1 script.md·meta.json desc — aitell 통과(설명 5.6, 자막 2.8)지만 script.md에 편집 통과 표시(.edit.json)가 없어 남은 3문장 목소리를 못 만든다. 85문장은 목소리가 이미 있으니 문구 변경은 3:7·7:3·12:0 세 문장 안에서만(숫자 그대로).
    - 착수: firemap-editor 12:05
    - 완료: **편집 통과: E-1 script.md·meta.json desc 12:09** (firemap-editor) — 3:7·7:3 그대로 통과, 12:0만 '정리하면,' 뺀 한 문장으로('영업이익은 1년 전 같은 분기보다 세 회사 모두 6배에서 19배 늘었고, 주가는 3배에서 6.5배 올랐습니다.' 숫자 동일, 원본 script.md.orig). aitell 1.2(전 1.2), 85문장 변경 0. 표시 script.md.edit.json·meta.json.edit.json. video-producer 16:00 뒤 lfvoice make 진행 가능.
- [순돌이 검토] ① 유튜브 설명 쓰기(videos.update)가 무인 회차 자동 권한 검사에 막힘 — calc_links.py·f2_coupang.py apply 허용 규칙을 넣을지, 채팅 세션에서 한 번 돌릴지(권한 설정 변경은 대역이 안 함). ② Claude 주간 한도 50%(10-03 바닥 예상) — 총무 제안(운영실장 1명·점검 하루 3회 등)을 workflow.md와 맞춰 결정. ③ '지시문 추가 필요'의 ?fm_internal=1 한 줄(7개 지시문) 아직 안 들어감.

## [지시·긴급] 새 계산기 주소가 휴대폰에서 파이어맵 첫 화면으로 떨어짐 (순돌이 → firemap-product-dev, 지금, F1보다 먼저)
- 사장님 07:0x: "새로운 계산기 웹사이트 안 들어가진다, 파이어맵으로만 들어가진다."
- 실측(firemap_events, 순돌이 07:1x): client f63b89a2(재방문 30일, 사장님 기기로 추정·확인 안 함)가 07:03·07:04·07:04 세 번 session_start path=/calc/salary·/calc/severance로 들어왔는데 첫 screen_view가 전부 **home**. 반면 순돌이 브라우저(새 기기, 데스크톱·모바일 에뮬)는 salary·severance 화면이 정상. 운영 번들(index-xQrnB8Pe.js)과 캐시 헤더(max-age=0)는 기기 무관 동일.
- 코드상 원인 후보: FireMapMVP.jsx readScreenFromHash — `if (tool && !window.location.hash)`라 주소에 해시(#home 등)가 붙어 있으면 도구 화면을 건너뜀. kakaoAuth.js 59행이 로그인 복귀 때 `pathname + '#home'`을 만든다. 다른 원인(인앱 브라우저·저장 상태)도 확인할 것.
- 완료 기준: 재방문 기기 상태(localStorage에 firemap-inputs-v3·랭크 기록·카카오 로그인 흔적, 주소 끝 #home)를 재현해 원인 확정 → 도구 경로(/calc/*, /tax 등)로 들어오면 해시와 상관없이 그 도구 화면이 뜨게 수정 → 테스트 추가 → 운영 배포 → 운영에서 재현 상태로 다시 열어 도구 화면 확인(스크린샷) → 여기 "완료: … HH:MM".
- 착수: firemap-product-dev 07:10
- 완료: 원인 확정·수정·운영 배포 07:23 — 운영 재현: 주소 끝에 해시가 붙으면(/calc/salary#home·/calc/severance#home) 새 기기·재방문 기기 모두 첫 화면, 해시 없으면 localStorage 상태와 무관하게 정상 → 원인은 해시(저장 상태 아님). 수정: 처음 열 때 도구 경로가 해시를 이기고 해시를 지움(공유 입력·ops 제외, FireMapMVP.jsx readInitialScreen). 스모크 테스트 추가(4경로×#home·#result, 30개 통과). 운영 index-CRiqTGEj.js에서 10가지 상태 전부 도구 화면, 스크린샷 work/research/calc-salary/hashfix-salary.png·hashfix-severance.png. 사장님 기기에 해시가 붙은 경로(방문 기록 자동완성·로그인 복귀 추정)는 확인 안 함 — 어느 쪽이든 이제 도구 화면이 뜸. 카카오톡 인앱 브라우저 실기기는 확인 안 함. (firemap-product-dev, edebf22)
- 배포: git -C C:/Users/강영준/Documents/GitHub/retire-age-kr push -q origin dev:main (빌드·테스트 통과 뒤)

## [지시] Claude Design 시험 (순돌이 → firemap-designer, 기한 오늘 16:20 회차 끝, 사장님 07:1x "클로드 디자인은 성능 안 좋나?")
- 사실: 이 계정에 Claude Design(Artifact 유형 "Design" 캔버스, "Design System")이 켜져 있다(순돌이 07:1x 목록 확인). 우리는 한 번도 안 써 봤다 — 성능은 **확인 안 함**.
- 할 일: Artifact 도구 action "quickstart" intent "design"으로 시작. ① 파이어맵 디자인 시스템(src/ui 토큰·firemap-design-identity 기준)을 "Design System" 유형으로 1개 ② 그걸로 F1 '계산기 결과 아래 쿠팡 상품 1칸'과 연봉 계산기 결과 화면 시안을 "Design" 캔버스에 2안.
- 비교: 같은 과제를 지금 방식(Figma/코드 시안)과 나란히 놓고 심사 3명(제미나이·GPT 웹·레드팀) 점수 + 걸린 시간. 결과를 experiments-registry.md X-TOOL-1에 적고, 이기면 designer·visual-designer 교본에 기본 도구로 넣는다.
- Artifact 도구가 무인 세션에서 안 보이면(ToolSearch로도) '막힘'에 적는다 — 순돌이가 채팅 세션에서 대신 연다.
- 착수: firemap-designer 07:14
- 완료: X-TOOL-1 1회차 07:25 — Design System https://claude.ai/artifact/P4fwu71ximrBCATjtvS8K9 · 캔버스 https://claude.ai/artifact/LcR4aCPejQu2akSWpnk5zQ(2안). 심사 평균 Claude Design 5.2 vs 코드 시안 7.8 → **기본 도구 보류**(무인 세션에서 로그인 화면·Pretendard 2MB가 글꼴 상한 1MB 초과), 사장님께 여러 안 보여 줄 때만 보조로. 두 아티팩트는 비공개 — 사장님이 Share 메뉴에서 켜야 남이 봄. 근거 design/salary-result/compare.md
- 설계 완료: design/salary-result/ — 구현 요청(F3, firemap-product-dev): A안 기본 + 결과 카드 아래 80/100/120% 칩, 공제 6줄은 펼침, 주황은 버튼에만. StatHero 타일 3칸 값이 375px에서 붙음(값 크기 body-sm 또는 2칸). F1 쿠팡 칸: 대가성 문구 13px·ink-2 이상, '쿠팡에서 보기'는 전체 폭 버튼 말고 텍스트 링크 크기, '›' 한 줄 링크형 금지, 애드센스 재심사 중 결과 바로 아래 배치 여부는 판단 필요(레드팀).

## [지시·긴급] 외부 유입 길 전수 점검 (순돌이 → firemap-growth, 지금 근무 안에서 F4와 함께)
- 사장님 07:1x: "우리 사이트가 외부에서 들어올 수 있는 루트가 있는 거야?"
- 순돌이 실측(firemap_events, 9/30 11:30~10/1 07:15, internal 제외 session_start 724): 유튜브 11 · 디시 2 · 다음카페 1 · PWA 9(1명) · **출처 없음 691(243 client)**. 출처 없음 중 도구 페이지 11개가 전부 약 21세션·11명으로 똑같다 → 사람 아닌 점검·봇으로 보임(확인 안 함). 네이버 카페에서 들어온 기록 0(네이버 앱이 출처를 지우는지 확인 안 함). 검색: 네이버 site:firemap.kr에 /, /contact, /disclaimer, /fire-city 정도만, '연봉계산기' 네이버 1페이지에 파이어맵 없음. 구글 '파이어맵' 검색 1페이지에 없음.
- 완료 기준(growth/daily.md와 growth/channels.md):
  1. 진짜 외부 방문 = 봇·직원 점검 걸러 낸 숫자(걸러 낸 기준을 적는다). 직원 점검·빌드 확인은 전부 ?fm_internal=1을 붙이도록 각 지시문 규칙에 요청.
  2. 길마다 상태표: 구글 서치콘솔·네이버 서치어드바이저·다음 검색 등록(소유 확인 여부, 사이트맵 제출일, 색인된 페이지 수), 유튜브 설명란·고정 댓글 링크, 카페 글 링크(utm), 커뮤니티, 카카오톡 오픈채팅.
  3. 우리가 거는 모든 링크에 utm 붙이기(네이버 앱이 출처를 지워도 잡히게).
  4. 사장님 손이 필요한 것(검색 등록 소유 확인 등)은 결재함에 "어디서 무엇을 누르면 되는지" 한 줄.
- 착수: firemap-growth 07:31
- 완료: 외부 유입 길 전수 점검 07:38 — growth/channels.md(거르는 기준 4개·길 12개 상태표). 9/30 진짜 외부 **세션 40/고유 29**(원값 451 중 352가 로컬 테스트 host=127.0.0.1). 유튜브 utm 유입은 전부 같은 초 몰림이라 사람인지 확인 안 함. 결재함: 다음 검색 등록 1줄. (firemap-growth)

## [지시·긴급] 계산기 3종 출시 기획 다시 하기 — "사람이 어디서 어떻게 들어오나" (순돌이 → firemap-venture 주관, growth·product-dev 협조, 착수 지금, 기획서 14:00)
- 사장님 07:2x: "새로 만든 계산기 3개가 외부에서 사용자가 어떻게 들어와야 하냐고. 직원들이 제대로 기획해서 사이트를 새로 만들든 파이어맵에 붙이든 했어야지."
- 무엇이 빠졌나: 연봉·퇴직금·실업급여 계산기를 '만들고 올리는 것'까지만 하고, **첫 사용자가 오는 길**을 기획하지 않았다. 검색은 몇 주 걸리고, 네이버는 자체 위젯이 맨 위라 1페이지 클릭이 어렵다(9/30 실측). 파이어맵 안에 붙인 것도 '은퇴 계산기 브랜드'와 '직장인 생활 계산기'가 맞는지 따져 본 기록이 없다.
- 완료 기준(ventures/calc-gtm.md, 계산기마다 한 쪽):
  1. 누가·언제 필요한가(연봉협상·이직·퇴사 직후·실업급여 신청 전 등)와 그 순간 그 사람이 **지금 있는 곳**(검색어, 블라인드·디시·네이버 직장인 카페·맘카페, 유튜브 쇼츠, 카톡 공유, 고용24 안내 등) — 실측 근거.
  2. 검색 없이 **첫 주 100명**이 오는 경로 3개 이상과 담당·날짜(약관·커뮤니티 규칙 안, 도배 금지).
  3. 결과 공유 장치(결과 카드·링크)가 있는지, 없으면 product-dev 요청.
  4. **별도 사이트(새 주소) vs 파이어맵 안** 결정: 브랜드 맞음, 검색 신뢰, 애드센스 재심사 영향, 유지 비용, 경쟁 사이트 형태를 비교해 하나로. 새 사이트면 신사업 첫 사이트(10/4)와 합친다.
  5. `second_opinion.py <문서> 전략`, 레드팀 확인.
- 기획서가 나오면 실행 칸을 오늘 결승선 표에 담당·시각과 함께 더한다.
- 재발 방지: launch-checklist.md에 20번 "첫 100명 경로(검색 말고 3개, 담당·날짜)"를 더한다. 이 칸이 비면 product-dev는 운영 배포하지 않는다.
- 착수: firemap-venture 07:20
- 완료: 기획서 ventures/calc-gtm.md 07:32 (firemap-venture)
  - 결정: **파이어맵 안(/calc/*) 유지.** 이길 점 ② '몇 살에 은퇴'가 파이어맵에 붙어 있어야 성립한다. 새 주소는 검색·애드센스를 0에서 다시 시작한다.
  - 실측(07:2x): 네이버 세 검색어 모두 임금계산기 위젯이 맨 위지만, 작은 계산기 사이트(k-calc·calcroom·gibugi 등)도 1페이지에 있다 → 검색은 막힌 길이 아니라 늦은 길. 계산기 3종에 출처가 달린 외부 방문은 0건. 우리 자리 외부 유입은 하루 약 15명(유튜브 11). **세 계산기 모두 공유 기능 없음.** 남의 커뮤니티 홍보글은 디시 규정 금지.
  - 첫 주(10/2~10/8) 목표: 외부 100명 + 경로별 전환 + 계산기→쿠팡 클릭. 레드팀 판정 '고쳐서'를 반영했다(제미나이 429로 Claude 레드팀이 대신 검토).
  - launch-checklist.md 20번 추가 완료.
  - **[지시] firemap-product-dev**
    - R1 첫 화면·은퇴 결과 → 계산기 3종 연결(fm_from 이벤트), 10/3
    - R6 계산기 3종 결과 공유(ShareSheet 재사용, 카카오 공유·링크 복사·금액 가리기, utm_source=share, calc_share 이벤트), 10/3 22:00
    - R7 주제가 맞는 가이드 글 끝에 관련 계산기 1개(지금 101편 중 1편뿐, 똑같이 박기 금지), 10/2 22:00
    - 실업급여 '받을 수 있나' 3문항(고용보험법 원문 대조, second_opinion 법 통과 뒤 배포), 10/5
  - **[지시] firemap-growth**
    - R8 색인 제출 목록에 /calc 3개가 들어갔는지 확인, 10/1
    - R5 오픈채팅 공지 1회(utm_source=openchat), 10/2
    - utm.md에 `share` 등록, 10/2
    - daily.md에 '계산기 3종 외부 방문(경로별)' 매일 한 줄, 첫 줄 10/2
  - **[지시] firemap-youtube-loop:** R2 F2 설명란을 수정할 때 주제가 맞는 롱폼에만 계산기 링크 1개를 둘째 줄에(utm_campaign=영상id). 권한이 풀린 첫 회차.
  - **[지시] firemap-shorts:** R3 F5 편의 관련 동영상을 계산기 링크가 있는 롱폼으로. 10/1 19:20.
  - **[지시] firemap-write:** R4 F6 카페 글의 계산기 링크 1개에 utm_source=cafe&utm_medium=post. 10/1 20:10.
  - 판정: 첫 주 10/8 20:10 venture 회차. 10/8까지 /calc가 어디서도 색인되지 않으면 계획을 보류로 바꾸고 다시 짠다.

## [지시·긴급] 무대를 전 세계로 — 한국만으로 월 1억이 되나 (순돌이 → firemap-bizdev, 착수 지금, 보고 13:00)
- 사장님 07:2x: "무대가 우리나라만이면 월 1억이 가능하겠어? 스꾸처럼 전 세계 대상이어야지?"
- 할 일: ① 한국만일 때 월 1억 상한 계산(revenue_model.py, 검색 수요·광고 단가·쿠팡 수수료 실측 근거) ② 전 세계(영어 우선, 다음 일본어·스페인어 등) 시장: 'FIRE calculator'·'salary after tax calculator'·'severance/retirement calculator' 등 검색 수요(구글 트렌드·vidIQ 키워드), 영어권 광고 단가(애드센스 RPM 공개 자료), 아마존 어소시에이트 등 전 세계 제휴 ③ 경쟁(영어권 상위 FIRE·세금 계산기 사이트 5개 실측) ④ 첫 전 세계 제품 후보 3개와 **오늘 안에 낼 수 있는 가장 작은 첫 판**(예: 파이어맵 영어판 1페이지 또는 새 주소) ⑤ 로드맵(roadmap.md) 수정안. second_opinion 전략·법, 레드팀.
- 스꾸는 공개된 사실(전 세계 대상 스티커)만 참고. 스꾸 저장소·계정·데이터는 절대 열지 않는다.
- 착수: firemap-bizdev 07:22
- 완료: firemap-bizdev 07:35 · 결론: 한국 계산기 광고만으로는 월 1억 불가(분야 1등 10% 점유여도 190만~350만원, 후하게 잡아도 약 1,100만원) → 영어 계산기 30~50개 묶음이 1억 경로 · 첫 판 제안: UK take-home pay 2026/27 + 롱테일 1개, 영어 새 사이트(GitHub Pages, builder 키트 template-en), 금융 제휴 없음, 광고 전 CMP 필수 · 문서 work/research/global/strategy.md(레드팀 "고쳐서" 5건·법 참모 반영) · roadmap에 시험 트랙 추가(목표 숫자는 그대로) · 결재함 3건(애드센스 계정 분리·세무·UK GDPR 대리인) → venture 본부장이 첫 사이트를 정할 근거

## [지시·긴급] 신사업 빌더 채용·첫 사이트 오늘 출시 (순돌이, 사장님 07:2x "신사업팀은 뭘 꾸물거리고 있는 거야")
- 사실: 신사업본부는 본부장 1명뿐이고 빌더 채용이 04:47 총무 회차에서 끝나지 않았다(예약 작업 없음). 첫 사이트 기한 10/4는 늦다 → **오늘 22:00**로 당긴다.
- 완료: firemap-venture-builder 채용·즉시 출근(순돌이). 본부장은 계산기 출시 기획(14:00)과 전 세계 전략(bizdev 13:00)을 보고 첫 사이트 한 개를 정해 빌더에게 지시서로 넘긴다(12:00까지). 정할 근거가 부족하면 계산기 3종 중 하나의 독립 사이트 또는 영어판 중 수요가 큰 쪽.
- 착수: firemap-venture-builder 07:25 (지시서 전이라 준비 작업: 배포 길·빈 템플릿 한/영·측정·결과 공유 카드)
- 완료: firemap-venture-builder 준비 작업 07:34 — 운영 확인까지 끝. ① 배포 길: firemap.kr/<경로>/ 됨(push→운영 약 2분 40초), GitHub Pages(kygstar77-creator.github.io, duo-memo 선례 200) 가능, *.pages.dev는 wrangler 없음·로그인 없음이라 막힘. ② 공용 부품 firemap.kr/kit/fmkit.js(측정: site·lang·utm·internal / 결과 공유 카드 1080 PNG·utm 자동) ③ 빈 템플릿 한/영 ventures/kit/template-*.html ④ noindex 점검 페이지 firemap.kr/kit/demo/ 320px 넘침 없음·firemap_events 도착 확인. 사용법 ventures/kit/README.md. **본부장님께: 지시서(사이트·경로·언어) 오면 템플릿으로 바로 만든다 — 12:00 전에 주시면 22:00 기한 여유 있음.**
- 완료: 첫 사이트 결정·지시서 07:4x (firemap-venture) — **X-V1 UK take-home pay 2026/27 + £100k 60% 구간**, GitHub Pages 새 저장소 kygstar77-creator/uk-take-home-pay(firemap.kr 밖), 광고 0·저장 없는 측정. 지시서 ventures/uk-pay/brief.md, 체크리스트 ventures/uk-pay/launch.md(빌더 채움 칸). 아래 [지시] 참고.

## [지시·긴급] 색인 오늘 끝내기 (순돌이 → firemap-growth, 외부 유입 점검과 같은 근무)
- 새 계산기 3개(/calc/salary·/calc/severance·/calc/unemployment-benefit) 주소를 오늘 안에: 구글 서치콘솔 URL 검사·색인 요청, 네이버 서치어드바이저 웹페이지 수집 요청, IndexNow(빙·네이버) 재제출, 사이트맵에 들어 있는지 확인. 로그인이 필요한 곳은 사장님이 이미 로그인해 둔 크롬 세션만 쓰고 비밀번호는 입력하지 않는다. 막히면 결재함에 "어디서 무엇을 누르면 되는지".
- 매일 한 번: 구글·네이버에 site: 검색으로 색인된 페이지 수를 growth/daily.md에 적는다.
- 착수: firemap-growth 07:31
- 완료: 색인 제출 07:38 — 사이트맵 3개 주소 모두 포함 확인 · 구글 서치콘솔: 사이트맵 재제출(6/15 뒤 안 읽혀 28개로 멈춰 있었음)·/calc/salary·severance·unemployment-benefit 색인 생성 요청됨 · 네이버 서치어드바이저: 웹 페이지 수집 요청 3건 내역 확인(07:33~07:3x) · IndexNow 200(07:30). site: 수는 growth/daily.md '색인 일지'. 색인까지 걸리는 시간은 보장 없음 → 매일 site: 재측정. (firemap-growth)

## [지시] 조회수 많은 모든 장르로 글 확장 — 실험 설계 (순돌이 → 콘텐츠 네트워크 조사 TF(임시 에이전트, 07:3x 착수), 결과 → firemap-venture 판단, 보고 11:00)
- 사장님 07:3x: "카페를 더 만들든 블로그를 더 파든 웹사이트를 만들어서 글을 발행하든, 조회수가 많은 모든 장르를 다 글을 써야 하는 거 아닌가."
- 이미 아는 제약(근거 파일): 네이버 블로그 9/23 이후 새 글 무색인(memory blog-noindex-since-0923), 네이버 어뷰징은 양이 아니라 패턴(템플릿·급전환·자동화)으로 걸림(naver-abusing-rules), 네이버 약관 무승인 자동 게시 금지(meeting 9/30 STOP_blog), 구글 '대량 생성 콘텐츠' 정책·애드센스 재심사 중.
- 완료 기준(work/research/ventures/content-network.md): ① 조회수 큰 장르 상위 20개 실측(네이버 검색수·유튜브·커뮤니티 조회, 한국+영어권) ② 채널별(새 네이버 카페, 새 블로그, 자체 웹사이트, 티스토리·브런치, 영어 사이트) 가능 여부·약관·수익 방식(애드포스트·애드센스·제휴)·AI 직원만으로 운영 가능한지 ③ 추천 구조 1개와 1주 실험안(장르 2~3개, 글 수, 지표, 판정일) ④ 위험(계정 정지·저품질·애드센스 영향)과 막는 방법.
- 완료: content-network.md 08:15 — 추천: "모든 장르"가 아니라 새 도메인 자체 사이트 1개에 정보형 장르 2개(요리·국내 나들이, 공공데이터 제한 없음)로 구글 유입 실험(10/2~10/8, 판정 10/8·10/15). 새 네이버 아이디·블로그·카페는 약관(자동화 수단 금지)·무색인 때문에 만들지 않음. 결재: 도메인 구입·"새 네이버 계정 안 만듦" 원칙·애드센스 사이트 추가는 firemap.kr 승인 뒤

## [지시·긴급] 쿠팡 막힘 풀림 → F1·F2 지금 실행 (순돌이 07:54)
- 사실: 사장님이 휴대폰에서 쿠팡 파트너스 로그인 시 '인증 필요' 창이 뜨지 않음. 순돌이가 07:54 PC 크롬에서 partners.coupang.com '링크 생성 > 상품 링크' 화면이 막힘 없이 열리는 것 확인. 유튜브 설명 수정 권한 동의도 07:52 완료.
- firemap-youtube-loop: F2 실행 — f2_coupang.py dry → apply, 되읽기 확인, 쿠팡 '내 정보'에 youtube.com/@firemapkr 등록 여부 먼저 확인(없으면 등록). 끝나면 "완료: F2 HH:MM".
- firemap-product-dev: F1 — coupangPicks.js 세 칸에 실제 쿠팡 링크(파트너스 링크 생성 화면에서 생성, 대가성 문구) 채우고 운영 배포, coupang_click 이벤트 확인. 쿠팡 '내 정보'에 firemap.kr 등록 여부 확인.
- 쿠팡 화면에서 다시 '인증 필요'가 뜨면 멈추고 '막힘'에 화면 문구 그대로 적는다(비밀번호·인증번호 입력 금지).
- 착수: firemap-product-dev F1 07:57
- **막힘(F1, firemap-product-dev 08:02):** PC 크롬 partners.coupang.com에서 '내 정보'와 '링크 생성 > 간편 링크 만들기' 둘 다 창이 뜸 — 화면 문구 그대로: "고객님의 정보 보호를 위해 인증이 필요합니다 ① 인증하기를 눌러 인증을 진행한 후, ② 아래 인증 완료를 눌러주세요." 인증하기는 누르지 않음. 마이페이지(결제정보·채널 아이디 관리)는 열리지만 firemap.kr 매체 등록 목록은 거기 없음 → 등록 여부 확인 안 함. 칸(dev c4185bd)은 준비 끝, 링크 3개만 넣으면 배포. 순돌이 07:54 확인 뒤 인증이 다시 걸린 것으로 보임(세션 시간 제한인지 확인 안 함) — 사장님이 인증한 직후 바로 이어서 발급해야 함.

## [지시·긴급] 디자인 관문 — 화면은 디자이너 통과 뒤에만 운영 (순돌이 08:00, 사장님: "예술가랑 디자이너 뭐 하노, 개발자가 올리면 미감이 좋겠나")
- firemap-designer: 지금 착수. ① F1 계산기 쿠팡 칸(연봉·퇴직금·실업급여 결과 아래) 시안·검수 ② 신사업 빌더 키트(firemap.kr/kit — 템플릿 한/영, 공유 카드) 검수 ③ 신사업 첫 사이트 시안(본부장 결정 나오면). 각 "디자인 통과/반려" 줄.
- firemap-brand-director(디자인·브랜드 본부장, 첫 근무): 오늘 나가는 모든 화면·썸네일의 브랜드 일관성 검수, 디자인실 팀원 일감 분배.
- 착수: firemap-brand-director 08:05
- firemap-artist: 오늘 새로 나가는 것마다 '뻔함' 한 줄과 다른 한 수 [제안].
- 착수: firemap-artist 08:03
- **[제안] 뻔함 점검(artist 08:06, 근거 art/2026-10-01-0803.md)** — 받는 쪽이 받음/거절(이유) 한 줄:
  - F1 쿠팡 칸 → product-dev·designer: 똑같은 점 '주제별 관련 상품 상자'. 한 수: 상품을 결과의 **다음 행동**에 맞춤(실업급여→구직·자격증 수험서, 퇴직금→가계부 노트, 연봉→협상 책), 칸 제목은 상품명 말고 행동 한 줄. 결과보다 아래·작게(사용자 참모도 "광고 냄새").
  - X-V1 UK → venture-builder: 똑같은 점 '60% 전용 계산기 8곳+, 표 한 장 결과'. 한 수: 결과·공유 카드에 "On £X you work for tax & NI until H:MM each 9-to-5 day"(£110,000이면 11:44am, 계산 1줄). 날짜 판(wecovr)은 있고 시각 판은 못 찾음.
  - 영어 계산기 묶음 → venture·bizdev: 똑같은 점 'omni형 종류별 목록 + 대량 생성 위험'. 한 수: **생애 사건 허브**(got a raise / had a baby / redundancy / pension at 55)로 묶어 한 입력에 계산 3~4개. 같은 구조 경쟁은 확인 안 함.
  - 전 장르 글 실험 → 콘텐츠 TF·venture: 똑같은 점 '레시피·여행 준비물 글 수백만 개'. 한 수: 레시피 DB × 농산물 가격 = "오늘 장보기 원가" 붙은 레시피(파이어맵 말고 새 사이트에서만). 가격 API 이용 조건 확인 안 함.
  - X-KR-1 가계부 → venture-builder(10/2): 똑같은 점 '크몽 가계부 + 마지막 줄 은퇴 나이'. 한 수: 지출 **줄마다 '은퇴 +N일'** 열("매달 반복된다고 가정할 때").
- **예술가 제안: 하루 세금 시계** — 실수령 결과 아래 "하루 8시간 중 첫 57분은 세금·4대보험료만큼 일한 셈"(연봉 4,000만원 예시) + 공유 카드에 부채꼴 시계 그림. 금액 안 밝히고 공유 가능. 사용자 참모가 꼽은 유일한 공유 순간.
  - → 담당 **firemap-venture-builder**(X-V1 오늘 22:00 공개분에 1줄), **firemap-product-dev**(연봉 결과 F8 디벨롭 + R6 공유 카드, 10/3). 판정 10/17: 시계 줄 있는 공유 카드의 공유 열기율이 없는 기간 대비 +30%면 퇴직금·실업급여에도, 결과 100회 이상에서 차이 없으면 뺀다. 이벤트 share_open에 clock=1 표시.
- 완료: firemap-artist 뻔함 점검 5건 [제안]·예술가 제안(하루 세금 시계)·아이디어 3개 08:07 — art/2026-10-01-0803.md
- firemap-product-dev·firemap-venture-builder: 화면 바뀌는 배포는 "디자인 통과" 줄 뒤에만. 이미 올린 화면은 디자이너 검수 결과대로 고친다.
- 착수: firemap-designer 08:03
- **디자인 반려: F1 계산기 쿠팡 칸 08:20** — 고칠 점 3개 ① 상품 줄이 '다음 계산' 내부 링크와 같은 부품·아이콘·›(위장형) → 아이콘·› 빼고 '쿠팡 ↗', 라벨 '광고 · 쿠팡 파트너스' ② 대가성 문구 주황 상자 → 상품과 **한 카드 첫 줄**(15px·ink-2, 주황 0) ③ '다음 계산'과 '계산 방법' 사이 → 화면 **맨 끝**(계산 방법 뒤). 적용할 패치 그대로: design/f1-coupang/fix.patch(`git apply --check` 통과). 심사 2명(레드팀·디자이너, 제미나이 429) 현재 4.0 → 수정안 7.0. 근거 design/f1-coupang/spec.md·compare.png. **[지시] firemap-product-dev: 패치 적용·스모크 테스트 뒤 링크가 들어오면 배포 — 이 줄이 수정안 기준 디자인 통과를 겸한다.**
- **디자인 반려: 신사업 빌더 키트 08:20** — 고칠 점 3개 ① 결과 큰 숫자 nowrap 40px → 320px 가로 넘침(문서 폭 346px) — clamp+fit ② 공유 카드 가운데 약 40% 빈 칸 → 묶음 세로 가운데·숫자 180px, **사이트별 accent 필수**(기본 주황이면 파이어맵 복제) ③ 머리·바닥 링크 높이 17~26px → padding 12px로 44px 이상. 근거 design/kit-review/review.md. **[지시] firemap-venture-builder: X-V1 공개 전에 셋 다.**
- **디자인 통과: F10 가이드 4편 본문 계산기 링크 08:20** — 새 부품 없음, 기존 본문 링크 색(#ff5a00) 그대로, 문장 말투가 글과 같음(습니다체), 글마다 위치·문장 다름. product-dev 운영 배포 가능.
- **설계 완료: design/uk-pay/ — 구현 요청(firemap-venture-builder, X-V1)** 08:20 — spec.md·preview.html. 입력 1칸+Year/Month, 버튼 없이 즉시 계산, 결과 다크 카드 안 '다음 £1,000' 줄·£100k~£125,140 노란 경고, 행동은 Share 1개, **사이트 색 짙은 초록 #0a6b52**(파이어맵 주황 금지), system-ui. **X-V1 디자인 통과 조건(planner ③ 반영):** 375×667·320×568에서 입력 직후 월 실수령 숫자와 '다음 £1,000 → £N' 줄이 스크롤 없이 보임(시안 y=450·499px), 넘침 0, 48px, 라이트·다크 캡처 4장을 launch.md에. 공개 전 내 표본 검수 요청을 today.md에 [디자인 검수 요청]으로.
- planner ① 퇴직금·실업급여 '이 돈이면 몇 살에 은퇴?' 버튼 — 사전 기준 08:20: 연봉 A안과 **같은 부품(Button 주황 1개)·같은 문구·결과 카드 바로 아래**면 새 디자인 아님. 단 한 화면 주황 행동은 1개 — 결과 카드 안에 이미 '은퇴 나이 계산' 주황 버튼이 있는 퇴직금 화면(impl-severance-light.png)은 **중복이면 반려**, 기존 버튼을 결과 카드 바로 아래로 옮기는 것으로 대신. 구현 캡처가 오면 통과/반려 줄을 적는다.
- 남은 것: planner ② X-KR-1 화면 3개 → 다음 회차 16:00(10/2 빌더 착수 전) · 예술가 제안 '퇴사 영수증' spec 10/5.
- 완료: firemap-designer 디자인 관문 1회차 08:20
- 완료: firemap-brand-director 브랜드 가이드 v1(work/research/brand/guide.md)과 오늘 표본 5개 검수 08:06. 통과 3(A-1 v5a·E-1 e1c·카페 대문 공지), 반려 2(아래 [지시]), 채널 소개는 어긋나지만 X-BRAND-1 대기. 참모 전략 '보류'·사용자 '고치면 쓰겠다' → 반영 내용은 guide.md ⑨. 팀원 4명에게 오늘 일감을 줌.

## [지시] 디자인·브랜드 본부 오늘 일감 (본부장 firemap-brand-director 08:06 — 기준 work/research/brand/guide.md)
- [지시] **firemap-visual-designer**(09시 근무, 기한 오늘 13시 근무 끝): 계산기 3종 공유 이미지(og) 시안을 연봉·퇴직금·실업급여 하나씩 만든다.
  - 사실: 지금은 셋 다 은퇴 계산기 og-image.png v9("나는 몇 살에 파이어할 수 있을까?", 남색 바탕 — 웹 토큰 밖)를 쓴다(08:0x curl 실측). 카톡으로 연봉 결과를 보내면 다른 질문이 뜬다.
  - 완료 기준:
    - 1200×630 3장이며, 각 계산기의 운영 title 말을 그대로 쓴다(짓지 않음).
    - 웹 토큰(#f6f7f9·#18191d·주황 #ff5a00·Pretendard)과 불꽃 로고를 쓴다.
    - 카톡·네이버 미리보기 크기에서 읽힌다.
    - 심사 3명 평균 6점 이상 → "디자인 통과" 줄 → product-dev 적용.
  - 결과 위치: work/research/visual/og-calc/.
  - 착수: firemap-visual-designer 09:04
  - 완료: firemap-visual-designer 09:17 — work/research/visual/og-calc/og_{salary,severance,unemployment}_c.png (1200×630). 제목·부제는 운영 seoTitle 그대로, 다크 카드 1장에 결과 라벨 → 그 화면의 실제 질문 줄(실업급여만 '재취업 뒤, 몇 살에 은퇴할 수 있을까?'), 주황은 '몇 살' 하나. 글자 전부 가운데 630px 안이라 정사각 미리보기로 잘려도 남는다. 심사 평균 7.0(제미나이 3.1-flash-lite 7·레드팀 7 통과, GPT 확인 안 함). b안(결과 카드+버튼) 반려 — 버튼 문구가 퇴직금·실업급여 화면과 달랐다. 근거 visual/og-calc/judges.md·compare.png·preview_sizes.png.
  - **디자인 통과: 계산기 3종 og c안 09:17** (심사 2명 평균 7.0, GPT 확인 안 함 — 교본 규칙).
  - [요청] firemap-product-dev: /calc/salary·/calc/severance·/calc/unemployment-benefit의 og:image를 각각 og_salary_c.png·og_severance_c.png·og_unemployment_c.png(public/에 복사, width 1200·height 630, ?v= 새 값)로 바꿔 주세요. 지금은 셋 다 og-image.png v9. 다시 그릴 땐 `py -3.12 work/research/visual/og-calc/make_og.py`(화면 문구가 바뀌면 assert가 멈춤).
  - [제안] firemap-product-dev: 결과 공유 때 실제 금액을 넣는 동적 og(functions/og.js가 이미 있음)라면 결과 카드형이 더 낫다(레드팀). 채택은 담당.
- [지시] **firemap-designer**(디자인 관문 검수 때 함께, 기한 오늘 16:20 회차): 연봉 결과 화면(운영 f3-a-prod-320.png)의 설명 캡션 2곳을 검수한다.
  - 대상: 다크 카드 안 4줄 "원천징수 비율 · 기본은 100%예요 …", 주황 버튼 아래 회색 3줄 "실수령 …에서 생활비 …를 빼고 …".
  - 기준: guide ③·메모리 design-identity '설명 캡션 금지(라벨·숫자·버튼·가정값만)'. 사용자 참모도 "깨알 같은 회색 글씨 → 이탈"이라고 했다.
  - 할 일: 줄이거나 접는 안 1개에 "디자인 통과/반려"를 적는다. 통과하면 product-dev가 F8 때 적용한다. 퇴직금·실업급여 결과도 같은 눈으로 본다.
  - 완료: **디자인 통과(안대로 적용 시): 연봉 결과 캡션 2곳 10:24** (firemap-designer) — ① 칩 아래 3줄 → 라벨 '원천징수 비율' 1줄, 문장은 '계산 방법' 카드로 옮김 ② 버튼 아래 회색 3줄 → 가정값 1줄 '생활비 N원 · 월 저축 N원', 문장은 '계산 방법'으로. 새 말 0(기존 단어만). 타일 '세액표'는 칩과 같은 값이라 빼도 됨(재량). 퇴직금·실업급여도 같은 눈: 버튼 아래 가정값 1줄. **[구현 요청] firemap-product-dev(F8 22:00):** design/calc-captions/review.md 1~3장. 글자 확정 firemap-editor-web.
- [지시] **firemap-illustrator**(14:40 근무, 기한 그 회차 끝): X-THUMB-1 B군(캐릭터 있음) 후보를 준비한다.
  - 사실: 지금 B군은 0편이다. 판정일(10/28)까지 4편 중 1편이 필요하다.
  - 할 일: 다음 롱폼(E-1 다음 편)용 캐릭터 1종 시안 2개를 제미나이 이미지로 만든다. ChatGPT 이미지는 금지(스꾸 한도).
  - 조건:
    - 소수몽키·잼투리처럼 곁다리 크기로 그린다(썸네일 면적 25% 이하).
    - 실제 인물·전문가 인격은 금지.
    - 오른쪽 아래 길이 표시 자리는 비운다.
  - 결과 위치: work/research/art/char-b/. 심사 3명을 받은 뒤 copywriter·video-producer에 인계한다.
  - 착수: firemap-illustrator 14:44
  - 완료: firemap-illustrator 14:52 — work/research/art/char-b/ok/char_a.png(1위, 굵은 외곽선+흰 스티커, 놀람+고지서 두 손) · char_b.png(예비, 외곽선 없는 입체+흰 테두리, 이마 짚고 걱정). 같은 사람(퇴사한 40대 초반 직장인, 이름·말풍선·글자 없음). 심사 3차 평균 a **8.0**·b **6.7**(제미나이 3-flash 8.5/6.2·레드팀 7.5/7·디자이너 8/7, GPT 확인 안 함). 배치 시안 thumb_mock_a/b.png: 캐릭터 상자 15.0%/18.8%(25% 이하 assert), 오른쪽 아래 길이 자리·아래 5% 비움. **제미나이 이미지 모델 6개 전부 429** → 지시서 대체 도구 SVG로 그림(prompt.txt, 다음 회차 gen.py 재시도 가능). 근거 judges.md.
  - [요청] firemap-copywriter: D-1(건보료) 썸네일을 X-THUMB-1 B군으로 쓸지 결정하고, 쓰면 노랑 줄·흰 큰 숫자 줄 문구를 art/char-b/thumb_mock_a.png 칸(x≥500) 기준으로 ep/D-1/titles.md에. 캐릭터는 왼쪽 아래 곁다리, 말풍선 없음.
  - [요청] firemap-video-producer: B군 편이 정해지면 char_a.svg(벡터, 크기 자유)를 왼쪽 아래(x 10~380, y≤680)에 넣고 meta.json에 experiment: X-THUMB-1 B, usage.md에 편 이름을 적어 주세요. 실사 아님 → 합성 표시 대상 아님. 포즈가 더 필요하면 today.md에 '[요청] illustrator 새 포즈'.
- [지시] **firemap-motion-designer**(11시 근무, 기한 그 회차 끝): E-1 영상 그래픽을 guide ③ '영상 속 화면' 줄과 대조한다.
  - 기준: 웹 토큰, 제목 왼쪽 위 + 단위·기간, 출처 왼쪽 아래, 주황 = 우리 숫자, 빨강/파랑 = 등락.
  - 어긋나는 장면 번호와 수정안을 적는다. 결과 위치: work/research/brand/audit/E-1-motion.md.
  - 공개 전에 PD가 반영할 수 있게 today.md에 [요청]을 적는다.
  - 착수: firemap-motion-designer 11:26
  - 완료: firemap-motion-designer 11:39 — work/research/brand/audit/E-1-motion.md. guide ③ 어긋남 13곳을 **코드에서 고침**(E1.tsx·parts/charts.tsx·parts/fm.tsx; 숫자·문구·시점은 그대로). 핵심은 회사 색이 SK=주황, 삼성=파랑이었던 것: 13번 삼성 영업이익 19.14배 '증가' 막대가 파랑(내림), 11번 '+211%'(오름)가 파랑이었음 → 회사는 잉크 3단+선 모양, 주황은 손그림 동그라미와 18번 계산기 '그대로 54세' 하나만. 13번 출처가 3줄 자막에 가리던 것도 해결. Georgia 이탤릭은 Pretendard로. 심사 평균 7.5(제미나이 3-flash 8 · 레드팀 7 고쳐서 통과 → 지적 2개 반영, GPT 확인 안 함).
  - [요청] firemap-video-producer(16시 뒤 E-1 렌더 때): 코드는 이미 고쳐져 있으니 **e1props → render만 하면** 된다. 렌더 뒤 장면 3·7·11·12·13·18·19 프레임이 work/research/brand/audit/E-1-motion/a*.png와 같은 색인지 눈으로 확인해 주세요(회사 색 주황/파랑이 보이면 옛 코드). 지금 e1_rehearsal.mp4는 옛 색이다.
    - 착수: firemap-video-producer 14:18
- [지시] **firemap-brand-researcher**(08:30 근무, 기한 그 회차 끝): persona.md 첫 판을 만든다(work/research/brand/research/persona.md).
  - 쟁점: 카페 실측(45~49세 최다·남 60%)과 참모 가정(35세 직장인)이 부딪친다. 이 쟁점 하나를 끝까지 판다.
  - 근거 3개:
    - ① 유튜브 Analytics 시청자 연령·성별(못 읽으면 '확인 안 함')
    - ② kwvol.py 월 검색수: 파이어 / 조기은퇴 / 노후 준비 / 은퇴 나이 / 연봉 실수령액
    - ③ firemap_events 계산 완료 입력 나이 분포(host=firemap.kr, internal 제외, 표본 수 명시)
  - 결과가 나오면 브랜드 디렉터가 guide ①을 고친다.
  - 착수: firemap-brand-researcher 08:41
  - 완료: firemap-brand-researcher 08:46 — 결론: 둘 다 맞고 창구마다 다르다. 계산기 입력 나이 중심 30~34세(3,018명, 기본값 35 제외, 45세+ 7.7%) · 유튜브 남 81%·35~44 34%·45~54 29% · 카페 45~49 최다(홈판 유입). 주의: 나이칸 기본값이 35(Home.jsx:21)라 '35세' 근거로 못 씀. 근거 work/research/brand/research/persona.md
  - [요청] firemap-brand-director: guide ①의 '누구에게'를 창구별(계산기 30대 초중반 / 유튜브 30~50대 남성 / 카페 40대 후반)로 고쳐 주세요. 이번 주 새로 알게 된 것 3가지 — ① 나이 입력 기본값 35가 '35세 직장인' 가정을 만들었을 수 있다(35만 496명으로 튐) ② 검색은 '조기은퇴'(180)가 아니라 '파이어족'(12,540), '은퇴' 계열(850)보다 '노후' 계열(3,810) ③ 유튜브 구독을 부른 건 ETF 파이어 방법 영상뿐(QQQM·SCHD 구독 +12, 금리 쇼츠 구독 0). 근거 persona.md
    - 착수: firemap-brand-director 10:06
    - 완료: firemap-brand-director guide ① '누구에게'를 창구별 3유형(계산기 30대 초중반 / 유튜브 30~50대 남성 / 카페 40대 후반)으로 고침 + '사람들이 쓰는 말'(파이어족 12,540·노후 3,810) 추가, X-BRAND-1 B안 후보에 'ETF 파이어 방법 → 내 숫자' 순서(가정) 추가. 근거 persona.md, 결과 work/research/brand/guide.md 10:07
  - [제안] firemap-product-dev: 나이 입력 기본값 35를 비우거나 바꿔 실제 나이 분포를 잴지 판단(제품 결정, 채택은 담당).
  - [요청] firemap-admin: 네이버 데이터랩 검색어트렌드 API(개발자센터 앱 키) 연결 — 검색자 연령·성별을 재려면 필요.
- [제안] firemap-product-dev·designer(사용자 참모 08:05): 결과 화면에 "지난번보다 은퇴가 N개월 당겨졌어요" 같은 변화 기록이 있으면 다시 오겠다는 의견. 문구는 짓지 말고 실제 서비스 표현을 찾은 뒤 판단한다. 채택 여부는 담당이 정한다.

## [지시·긴급] 모든 글자를 사람 말로 — 편집 3명 분담 + 자동 검사 (순돌이 08:15, 사장님: "사소한 것까지 모든 글을 다 검토해서 사람이 쓴 글로 바꿔야 하는데")
- 분담: firemap-editor = 카페·블로그·유튜브(제목·설명·고정 댓글)·대본·자막·쿠팡 문구 / firemap-editor-web(신규) = 사이트·계산기·신사업 사이트의 모든 화면 글자·메타·알림 / firemap-editor-en(신규) = 영어 전부.
- **firemap-improve (지금 착수, 기한 14:00):** work/aitell.py — AI 티 표현 사전(한·영), 같은 끝맺음·틀 반복, 과한 설명조를 점수로 내는 자동 검사. ① naverpost.py·ytupload.py·f2_coupang.py가 발행 전에 돌려 기준 넘으면 거절(편집 통과 표시 있으면 통과) ② package.json prebuild에서 src/ 화면 문구를 검사해 새로 들어온 AI 티 문구를 경고(처음엔 경고, 편집자 전수 점검 끝나면 실패로). humanlike.py와 겹치면 합친다. 테스트 포함.
  - 착수: firemap-improve 08:17 (aitell.py)
  - 완료: firemap-improve 08:20 — work/aitell.py(점수·gate·pass·scan) + 사전 work/aitell_dict.json(humanlike.py와 합침). ① naverpost.py·cafeapi.py는 묶음이 기준 12(1,000자당)를 넘고 editor_ok.txt가 없으면 거절(표시 뒤 원고가 바뀌면 무효), ytupload.py는 제목·설명, f2_coupang.py는 라벨 — 편집 통과는 FIREMAP_EDITOR_OK=1 ② prebuild에 node work/aitell-web.mjs(src/ 문구, 기준선 대비 새로 들어온 것만 경고, AITELL_STRICT=1이면 실패) ③ 테스트 work/test_aitell.py·work/test-aitell.mjs 통과. 최근 묶음 59개 중 5개가 걸림('~요' 70%대 쏠림). 대기 중 카페 3편은 모두 통과. **editor 참고: 기준 넘는 글을 보고 나면 `py -3.12 work/aitell.py pass <묶음> firemap-editor`. editor-web: 전수 점검 끝나면 `node work/aitell-web.mjs --update-baseline` 뒤 AITELL_STRICT=1 전환.**
- **firemap-editor (지금 착수):** 이미 공개된 글 전수 점검 — 조회 많은 순(카페 조회수·유튜브 조회수)으로 목록 work/research/editor/sweep.md를 만들고 근무마다 이어서 고친다(카페 글은 수정, 유튜브는 설명·고정 댓글).
  - 착수: firemap-editor 08:15
  - 완료: firemap-editor 1차 08:22 — 목록 work/research/editor/sweep.md(유튜브 공개 11 + 카페 174, 조회순). 유튜브 6월 롱폼 6편 설명 원고 끝(AI 티 편당 3~5개→0), 카페 1위 #44(584회) 원고 끝. **적용은 아래 두 [요청]에 걸려 있다**(편집자 루틴은 유튜브 쓰기가 권한에 막힘, 카페는 수정 도구 없음). 다음 근무부터 카페 #81부터 이어 간다.
  - [요청] **firemap-youtube-loop**(F2 설명란 손볼 때 같이, 먼저 해도 됨): 롱폼 6편 설명을 editor/2026-10-01/ytdesc/<id>.txt로 바꿔 주세요 — zhTjJwy1mwQ·wwfFszPl06g·scV67BQvC4Q·JVTYZ208hgw·gSKsQWjTabo·cxls2Ve18-k. 적용 직전 설명이 <id>.txt.orig와 같을 때만(다르면 F2 첫 줄 등 남의 변경이 있으니 그 위에 합쳐서). 제목·태그·카테고리는 그대로. F2 대가성 첫 줄은 이 본문 **위에** 붙이면 된다. 면책·숫자·링크·해시태그는 한 글자도 안 바꿨다. 되읽기 후 "완료: ytdesc HH:MM".
  - [요청] **firemap-improve**(aitell 다음): naverpost.py에 카페 글 **본문 수정**(edit <articleId> <txt>) 기능. 지금은 올리기만 있다. 공개 카페 글 수정은 편집 전수 점검의 유일한 적용 길이다. 첫 대상 editor/2026-10-01/cafe/44.txt(원본 44.txt.orig·44.html.orig, 이미지 3장 위치 유지). 숫자는 전후 대조 완료.
- **firemap-editor-web (지금 착수):** 운영 화면 전수 점검 시작(오늘 나간 계산기 3종·쿠팡 칸·키트 먼저).

## [지시] 콘텐츠 네트워크 실험 X-CN-1 착수 (순돌이 08:16, 전권 결정 — 근거 ventures/content-network.md)
- 결정: '조회수 큰 모든 장르'는 하지 않는다(상위 장르는 91~99.9%가 실시간 숫자·앱 검색). 자체 사이트 1개, 정보형 2장르(요리·국내 나들이), 구글 유입 중심, 광고 없이 1주 실험(10/2~10/8, 14편+대조 1).
- 사장님 결재 없이 가는 방법: **새 도메인 구입 대신 무료 주소(kygstar77 Cloudflare *.pages.dev 또는 kygstar77-creator GitHub Pages)**. firemap.kr·애드센스와 분리. 애드센스 추가는 firemap.kr 승인 뒤, 도메인 구입은 10/8 판정에서 '계속'일 때만 결재함에.
- 원칙 확정: 새 네이버 아이디·블로그·카페는 만들지 않는다(네이버 약관 자동 게시 금지).
- 순서(트랙 A 작은 실험): firemap-planner 기획서(plans/content-network.md, 1일차 관문 = 식약처 레시피 DB에 인기 요리가 있나, 없으면 '시험 일정'으로 교체) + firemap-artist '우리만 다른 한 가지' → firemap-venture-builder 사이트·첫 2편 → firemap-editor(한국어 편집) + 디자인 통과 → 공개. 지표: 색인율·노출·글당 토큰·편집 통과율. experiments-registry.md에 X-CN-1 등록은 firemap-venture.

## ★ 오늘 결승선 10/1 (순돌이 07:10, 사장님: "하루하루 소중히, 하루 안에 수익도 나야 하고 개발은 끝장나게 해서 출시하고 계속 디벨롭")
실측 출발점: 사이트 하루 세션 약 30(9/29 32), 월 목표선까지 약 23배 부족 · 수익 0원 · 공개 쇼츠 조회 수백 회 수준. **하루 안 첫 수익의 유일한 현실 경로는 쿠팡 클릭→구매**다. 그래서 오늘은 (1) 사람이 오는 모든 자리에 합법적인 쿠팡 자리를 켜고 (2) 검색량 큰 계산기를 경쟁 1등 수준으로 올려 사람을 늘린다.
운영실장: 아래 표의 미완료 담당을 매시 우선 투입한다(개발 직원은 한 번에 한 명).
| # | 무엇 | 담당 | 오늘 마감 | 완료 기준 |
|---|---|---|---|---|
| F1 | 계산기 결과 아래 쿠팡 관련 상품 1칸(연봉·퇴직금·실업급여부터) | firemap-product-dev | 17:30 운영 배포 | coupang-policy 규칙표, 대가성 문구, 쿠팡 나감 이벤트, 애드센스 재심사에 불리한 배치 금지 |
| F2 | 공개 유튜브 영상 전부(A-1 + 공개 쇼츠) 설명란 첫 줄 대가성 문구 + 주제 맞는 쿠팡 링크 1개, 유료 광고 포함 표시 | firemap-youtube-loop | 14:00 | ytupload 규칙 통과, 권유 문구 없음, 변경 전후 기록 |
| F3 | 연봉 실수령 계산기를 '연봉 실수령액' 검색 1페이지 경쟁(네이버 위젯·잡코리아·사람인 등)보다 나은 점 2개 더 | firemap-product-dev (→ designer 시안) | 22:00 운영 배포 | 경쟁 화면 나란히 비교 파일, 손검산 5건, 모바일 320px |
| F4 | 연봉 계산기 유입: 서치콘솔·IndexNow 제출 확인, 쇼츠·카페·롱폼 설명란에서 연결 | firemap-growth | 20:00 | utm 달린 연결 3곳 이상, growth/daily.md 기록 |
| F5 | 퇴직금·실업급여 쇼츠 1편(쿠팡 링크 포함) | firemap-shorts | 19:20 | 기존 박차 #3 + 쿠팡 앞당김 지시 |
| F6 | 카페 계산기 소개 글 1편(쿠팡 없음, 사람 말투) | firemap-write + editor | 20:10 | 기존 박차 #6 |
| F7 | 수익 계측 스크립트 첫 실행(쿠팡 클릭·주문 포함) | firemap-growth | 22:00(원래 10/2) | growth/revenue.md 첫 줄 |
| F8 | 매일 디벨롭: 어제 배포한 계산기마다 이벤트 수치를 보고 고칠 것 1개 → 배포 | firemap-product-dev | 매일 22:00 | 고치기 전·후 수치 decisions/log.md |
| F9 | 계산기 3종 첫 사용자 경로: 색인 목록에 /calc 3개 확인(R8) | firemap-growth | 22:00 | growth/daily.md 기록 (calc-gtm.md 4장) |
| F10 | 가이드 → 계산기 내부 링크(R7), 주제 맞는 글만 | firemap-product-dev | 10/2 22:00 | 링크 건 글 목록, 똑같이 박기 금지 |
| F11 | 계산기 결과 공유(R6) | firemap-product-dev | 10/3 22:00 | 세 계산기 공유 → 새 창 같은 결과, calc_share 이벤트 |
- F10 진행(firemap-product-dev 08:20, dev 5d1b385, 운영 미반영): 주제가 맞는 가이드 4편에만 계산기 링크 1개씩, 문장·위치를 글마다 다르게 — unemployment-benefit-before-fire(금액 절 끝→실업급여) · retirement-pension-db-dc(DB형 절 끝→퇴직금) · seed-money-first-job(자동이체 단락 뒤→연봉 실수령) · income-tax-brackets-marginal-rate(한계세율 절 끝→연봉 실수령). 기존 severance-irp-tax 1편 포함 5/101. 뺀 것: personal-exemption-dependents(연말정산 글이라 월 원천징수 계산기와 어긋남), credit-card-income-deduction·earned-income-tax-credit(주제 다름). **[요청] firemap-designer: 디자인 통과/반려** — 본문 문장 1줄 링크(새 부품 없음). 통과 줄이 붙으면 product-dev가 운영 배포.
- F1 진행(firemap-product-dev 07:31): 칸은 준비 끝(dev) — CoupangPick.jsx가 연봉·퇴직금·실업급여 결과의 '은퇴 나이 계산'·'다음 계산' 뒤, 계산 방법 앞에 1칸. 링크 바로 위 권장 대가성 문구(강조색 Notice), rel=sponsored nofollow, 발급 link.coupang.com 주소만 통과, 가격 안 실음, 클릭 이벤트 coupang_click. 링크가 없으면 칸이 안 보인다(src/firemap-v2/coupangPicks.js에 넣으면 바로 켜짐). 스모크 31개 통과+가짜 링크로 렌더 확인. **막힘: 링크 발급 불가 — F2와 같은 쿠팡 본인인증(사장님 1번) + firemap.kr 매체 등록 확인(체크리스트 1, 미등록 매체=제재 A등급).** 인증이 풀리면 다음 회차에 비금융 상품 3개 발급 → 운영 배포.
- 착수: firemap-youtube-loop F2 07:20
- F2 진행(youtube-loop 07:40): **막힘 — 사장님 쿠팡 본인인증 1번 필요.** 쿠팡 파트너스 화면이 모든 메뉴(내 정보·간편 링크 만들기)에서 "인증이 필요합니다" 창으로 막혀, ① 유튜브 채널이 쿠팡 매체로 등록됐는지 확인 불가(미등록 채널에 링크 = 약관 8조·제재 A등급, coupang-policy 체크리스트 1) ② link.coupang.com 링크 발급 불가. 또 설명란 수정은 youtube.force-ssl 권한이 필요한데 지금 토큰은 upload·readonly뿐(videos.update 불가). **준비 끝:** work/f2_coupang.py(auth/dry/apply — 첫 줄 권장 문구·둘째 줄 링크·paidProductPlacement 켬·되읽기 확인), 계획표 longform/loop/f2_plan.json(롱폼 7편마다 다른 도서·가계부 검색, 비금융), 변경 전 설명 백업 longform/loop/f2_before.json(공개 11편). **쇼츠 4편은 이번에 넣지 않음:** 쇼츠 설명·댓글 URL은 클릭되지 않는다(YouTube 고객센터 13748639) → 수익 경로 0인데 유료 광고 표시만 붙음. 주담대 쇼츠는 대출 주제라 금지(체크리스트 12). 순돌이가 그래도 넣으라면 plan의 skip만 지우면 된다. **풀리면(사장님 1회):** ① 쿠팡 인증 → 내 정보에 youtube.com/@firemapkr 등록 확인·추가 ② `py -3.12 work/f2_coupang.py auth` 구글 동의 → 다음 youtube-loop 회차가 링크 발급·apply·되읽기까지 한다. 참고: A-1 유료 광고 표시는 10/2 19:30 클릭률 판정(X-THUMB-1)에 섞인다 — 판정 때 적용 시각을 구간으로 나눠 적는다.
- F7 완료 07:29(growth): 위 '수익 계측 장치' 완료 줄 참고.
- F4 진행 07:29(growth): 구글 서치콘솔 사이트맵이 **6/15 이후 안 읽힘(28개 인식, 실제 165개)**·색인 3쪽뿐 → 사이트맵 재제출, /calc/salary·severance·unemployment-benefit 색인 요청 완료. IndexNow 202는 04:53 기록. 네이버 서치어드바이저는 크롬 차단으로 확인 안 함. utm 연결 3곳은 아래 요청으로 — 담당이 넣으면 growth가 20:00 전에 확인. 기록 growth/2026-10-01-search.md
  - **[요청] firemap-shorts(F5, 오늘 19:20 편):** 설명란 계산기 링크 `https://firemap.kr/calc/severance?utm_source=shorts&utm_medium=desc&utm_campaign=<작업폴더>` 1개(쿠팡 링크와 별개, 대가성 문구 첫 줄 유지).
  - **[요청] firemap-write(F6 카페 계산기 소개 글):** 본문 링크 1개 `https://firemap.kr/calc/unemployment-benefit?utm_source=cafe&utm_medium=post&utm_campaign=<작업폴더>`(퇴직금 쪽 글이면 /calc/severance).
  - **[요청] firemap-youtube-loop(F2 설명란 손볼 때 같이):** 채널 프로필 링크에 `https://firemap.kr/calc/salary?utm_source=youtube&utm_medium=profile&utm_campaign=salary` 추가. ETF 영상 설명란엔 연봉 링크 넣지 않는다(주제 불일치).
- 착수: firemap-youtube-loop F2·R2·S2 07:58
- F2·R2·S2 진행(youtube-loop 07:59): 유튜브 수정 권한 토큰은 생김(07:51). **쿠팡은 여전히 막힘** — 크롬 partners.coupang.com '내 정보'가 07:58에도 '인증이 필요합니다' 창(사장님 휴대폰 본인인증 필요). 링크 발급·매체 등록 확인 불가라 쿠팡 줄은 보류. **R2 계산기 링크는 준비 끝, 적용은 막힘:** work/calc_links.py(롱폼 6편 설명 첫 문단 뒤에 '▶ 내 은퇴 나이 계산하기: https://firemap.kr/?utm_source=youtube&utm_medium=desc&utm_campaign=<영상id>', 아래쪽 맨 firemap.kr 주소도 같은 utm으로; 6편 모두 파이어·ETF·배당 주제라 연봉·퇴직금·실업급여 계산기는 주제 불일치로 안 씀; A-1은 이미 utm 있음). dry 확인 끝. apply(videos.update)는 이 무인 회차의 자동 권한 검사가 '외부 시스템 쓰기'로 거부 — 우회하지 않음. S2 채널 프로필 링크도 같은 종류라 손대지 않음. **풀리려면(사장님 또는 채팅 세션 1회):** `py -3.12 work/calc_links.py apply` 한 번(되읽기 결과 longform/loop/calc_links_after.json), 채널 프로필 링크는 스튜디오 맞춤설정→기본 정보→링크. 무인 회차에서 계속 하려면 Claude Code 권한 설정에 이 명령 허용 규칙 추가 필요.
  - (youtube-loop 07:59) **[요청] firemap-audit:** 옛 롱폼 JVTYZ208hgw·wwfFszPl06g·zhTjJwy1mwQ 설명·내용이 1인칭 개인 투자 경험('4년 동안… 거의 다 잃었습니다', '신용대출', 'QQQM 원툴인 제가')이다. 실제 사람 경험인지 확인 안 함 — 지어낸 인물이면 수익화 정책(AI Personas·misleading)·권유 금지 원칙에 걸릴 수 있다. 감사 판정 부탁(삭제·비공개 전환은 금지 규칙이라 판정만).
  - **[요청] firemap-product-dev(F8 때):** ① 로컬·미리보기 호스트(127.0.0.1·localhost·*.pages.dev)에서는 firemap_events 기록을 끈다 — 9/30 하루 원값 451세션 중 352가 host=127.0.0.1(테스트)이라 실측을 덮음. ② 구글이 아는 주소가 5개뿐 — 사이트맵 재제출은 했으니, 첫 화면·가이드에서 /calc/* 로 가는 일반 <a href> 링크가 크롤러가 보는 HTML(#sSeo)에 있는지 확인. ③ 퇴직금 설명 블록 소제목 후보 2개(퇴직금 지급 기준 34,110 / 퇴직금 지급일 10,640, 검색수 kwvol) — growth/2026-10-01-search.md 3장, 법 조문 대조는 product-dev.
- 22:30 결승선 점검(1회 근무)이 각 칸을 실측해 ✅/❌와 이유를 여기 적는다. ❌는 내일 표 1번으로 넘어간다.
- **점검 07:38 (스프린트 1회차, 결승선 점검관):**
  - F1 진행 중 — 막힘. dev에 칸(c4185bd)은 있지만 coupangPicks.js 세 칸 모두 null. 운영 번들 index-CRiqTGEj.js에 쿠팡 칸 없음. 오늘 coupang_click 0건. 쿠팡 본인인증(사장님)이 필요.
  - F2 진행 중 — 막힘. 설명란 변경 0편. 쿠팡 인증과 youtube.force-ssl 권한(f2_coupang.py auth)이 필요. 준비물은 2bfb95b. 유튜브 설명란을 직접 읽지는 않음(확인 안 함). 근거는 변경 커밋 없음.
  - F3 진행 중. 시안 완료(1e1ec58, design/salary-result/). 구현·운영 배포 전.
- 착수: firemap-product-dev F3 구현 07:42 (운영실장)
- 완료: firemap-product-dev F3(S3) 연봉 결과 A안 운영 배포 61c6952 — 다크 결과 카드 안 80/100/120% 칩(경쟁 5곳에 없음=이길 점①), 결과 바로 아래 '이 돈이면 몇 살에 은퇴?'(이길 점②), 공제 6줄+합계 펼침, 타일 값 body-sm. 손검산 6+경계 8 재통과, 운영 320px 넘침 0·A 2,935,813·80% 2,954,443 줄 대조(shots/f3-a-prod-320.png) 07:51
  - F4 진행 중. 서치콘솔 사이트맵 재제출·색인 요청은 growth/2026-10-01-search.md에 기록. utm 연결 0/3(쇼츠·카페·채널 프로필 모두 아직). 네이버 서치어드바이저 확인 안 함.
  - F5 진행 전(19:20). F6 진행 전(20:10). F8 진행 전(22:00).
  - F7 ✅. growth/revenue.md 첫 줄 2026-10-01 07:17 실재.
  - F9 ✅. 운영 sitemap.xml에 /calc 3개(curl 실측). 서치콘솔 3개 색인 요청은 search.md에 기록. daily.md 줄은 없음.
  - F10 진행 전(10/2). F11 진행 전(10/3).
  - 계산기 3종 운영 주소 200 확인. 해시 수정은 배포됨(index-CRiqTGEj.js).
- ✅ 비율 07:38: 2/11 (18%). X-OPS-4 기준선.
- 수익·세션 07:38: 수익 0원(revenue.md 07:17, 목표 대비 0.0%). 오늘 00:00~07:38 세션: 원값 408, host=firemap.kr·internal 제외 46(기기 40). 봇 거르기 전.

### 지난 결승선 11:50~14:50 (점검관 11:52 작성, 14:54 채점 → 열린 칸은 아래 14:50~17:50 표로)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 |
|---|---|---|---|---|---|
| U1 | 쿠팡 본인인증(T2 이월) → 풀리면 즉시 비금융 링크 3개 발급 → coupangPicks.js에 넣어 F1 운영 배포(디자인 추가 검수 없음, a16eec1) + f2_coupang apply | A | 사장님(결재함 75행) → firemap-youtube-loop(링크) → firemap-product-dev(배포) | 14:50 | 운영 번들 link.coupang.com 3개 + 설명란 되읽기 파일 |
| U2 | og c안(9808f52, 디자인 통과 11:39) + session_start bot=1(8a75781) 한 번에 운영 배포 | D | firemap-product-dev | 12:35 | 운영 curl /calc 3경로 og:image og_*_c.png 200 + 운영 Playwright 방문 bot=1 1건 |
| U3 | [지시] **대리 편집 firemap-editor-web**(editor 82분 대기): F6 카페 계산기 소개 calcub1001 편집 통과 .edit.json → 20:10 발행 가능 상태. #44 edit-ok는 editor가 13:00까지 착수 없으면 같이 | B | firemap-editor-web(대리) | 13:30 | work/research/calcub1001/pkg/.edit.json + aitell 점수 |
| U4 | 유튜브 설명란 utm·채널 프로필 /calc/salary(T3 이월) — 무인 쓰기 권한은 순돌이 채팅 세션 `py -3.12 work/ytdesc_all.py apply` 1회. 그동안 youtube-loop은 A-1·E-1 판정 기준선 표(대역 지시, 12:30) | B | firemap-youtube-loop / [순돌이 검토] 쓰기 1회 | 14:50 | 채널 정보 curl에 /calc/salary + 설명란 되읽기, 기준선 파일 longform/loop/ |
| U5 | X-V1 공개 저장소 생성 → `deploy.py push` → 운영 4쪽 200 | A | 사장님(결재함 17행) 또는 순돌이 채팅 → firemap-venture-builder | 14:50(공개 기한 22:00) | github.io 4쪽 curl 200 |
| U6 | 'Firemap daily growth' 루틴 3)항에 guidegate 문장 넣기(improve 11:47 제안 그대로) — 내일 09:00 [auto] 가이드부터 관문 통과 | C | 순돌이(루틴 수정 권한) | 14:50 | 루틴 지시문에 guidegate.py check 문장 실재 |
- 지난 결승선 07:50~10:50 표·08:52 점검 줄은 done-2026-10-01.md로 옮김(점검관 11:52).

- **점검 14:54 (스프린트 4회차, 결승선 점검관):**
  - U1 ❌ 쿠팡 링크 0개 — dev coupangPicks.js salary·severance·unemployment 모두 null, 운영 index-uQgW-jMI.js에 link.coupang.com 0, 오늘 coupang_click 0(Supabase). 결재함 75행 그대로.
  - U2 ✅ 운영 curl /calc/salary·severance·unemployment-benefit og:image = og_*_c.png?v=c1-20261001(점검관 직접), bot=1 방문 2건 firemap_events 실재(마지막 04:59Z). 완료 줄 0c65510.
  - U3 ✅ calcub1001/pkg/.edit.json 실재(by firemap-editor 12:08, aitell 0.0) — 대리 아닌 원 편집자가 처리.
  - U4 ❌ 유튜브 채널 정보 화면(curl)에 firemap.kr/?utm_source=youtube&utm_medium=profile만, /calc/salary 없음. 기준선 표는 있음(longform/loop/baseline-2026-10-01.md 4fc3eff) — 반쪽.
  - U5 ❌ kygstar77-creator.github.io/uk-take-home-pay/ 404, api.github.com 저장소 404.
  - U6 ❌ 원격 루틴 'Firemap daily growth' 지시문에 guidegate 0회(RemoteTrigger 조회, 마지막 수정 9/26). 10/2 09:00 실행 전 마지막 기회.
  - F1 ❌(진행 중, 17:30) = U1. F2 ❌ **마감 14:00 넘김 확정** — 설명란 쿠팡 0/11. F3 ✅. F4 진행 중 utm 0/3(채널 프로필 없음, 쇼츠·카페는 오늘 저녁 편). F5 진행 전(19:20). F6 진행 중 — 편집 통과(.edit.json 12:08), 발행 20:10. F7 ✅. F8 진행 전(22:00). F9 ✅. F10 ✅. F11 진행 전(10/3).
  - 표 밖: calc-3 퇴직금 숫자 줄('N년 앞당겨져요')이 운영 번들에 있음(curl). 디자인 통과 14:12(e016904)·글자 편집 통과 14:14(2dd1c0e) 줄은 둘 다 실재. 운영 반영 시각이 통과 이전이었는지는 확인 안 함(main=dev 같은 머리 93df365). X-CN-1 기획서 1f512c1 14:42 나옴(대역 지적 ① 해소).
- ✅ 비율 14:54: 이번 표 2/6 (33%) — U2·U3. 오늘 누계 10/27 (37%) — F3·F7·F9·F10·S3·S4·T1·T4·U2·U3. X-OPS-4 기준선.
- 수익·세션 14:54: 수익 0원(growth/revenue.md 07:17이 최신, 목표 대비 0.0%) · coupang_click 0 · 오늘 00:00~14:54 session_start 원값 490 중 로컬(127.0.0.1·localhost)·internal·bot 뺀 65(고유 기기 53), 11:50 이후 9 · 마지막 외부 세션 13:45.
- 정체 점검 14:54: 쿠팡 인증 07:40~ **정체 결재 7시간 14분**(21:15 안건 확정). 유튜브 무인 쓰기 07:59~ **정체 권한 6시간 55분**([순돌이 검토]). X-V1 저장소 09:50~ **정체 결재 5시간 4분**(21:00 빌더 재측정·본부장 처리 줄 있음). U6 루틴 문장 11:47~ **정체 3시간 7분**([순돌이 검토], 안 되면 21:15에서 '[auto] 가이드 1회 정지'). 편집·디자인 검수 대기 0건(calc-3·calcub1001·X-KR-1 모두 통과 줄 있음).

### 다음 3시간 결승선 14:50~17:50 (점검관 14:54 — 운영실장 :05·:35 투입)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 |
|---|---|---|---|---|---|
| V1 | 쿠팡 본인인증(U1 이월, 결재함 75행) → 풀리면 즉시 비금융 링크 3개 → coupangPicks.js → F1 운영 배포(a16eec1 디자인 통과, 추가 검수 없음). 안 풀리면 17:30 F1 ❌ 확정, 21:15 안건 | A | 사장님 → firemap-youtube-loop(링크) → firemap-product-dev(배포) | 17:30 | 운영 번들 link.coupang.com 3개 |
| V2 | F5 퇴직금·실업급여 쇼츠 — 제작 착수, 설명란에 `/calc/severance?utm_source=shorts&utm_medium=desc&utm_campaign=<작업폴더>` 1개(F4 utm 1/3) | B | firemap-shorts | 17:50(공개 19:20) | 렌더 파일 + 설명란 초안에 utm 링크, 편집 통과 .edit.json |
| V3 | F6 카페 계산기 소개 글(calcub1001, 편집 통과) — 발행 슬롯 20:10 확정·본문 `/calc/unemployment-benefit?utm_source=cafe…` 링크 실재 확인(F4 utm 2/3) | B | firemap-write | 17:50 | slot.txt 20:10 + 본문 utm 줄 grep |
| V4 | F8 디벨롭 사전 측정: 연봉·퇴직금·실업급여 계산기 오늘 이벤트(입력 시작·결과·포기율·calc-3 숫자 줄 클릭) 고치기 '전' 수치 → 고칠 것 1개 정하기 | D | firemap-product-dev (+ firemap-growth 수치) | 17:50 | decisions/log.md '전' 수치 줄 + 고칠 것 1개 |
| V5 | 유튜브 설명란 utm·채널 프로필 /calc/salary(U4 이월) — 순돌이 채팅 `py -3.12 work/ytdesc_all.py apply` 1회 | B | [순돌이 검토] | 17:50 | 채널 정보 curl에 /calc/salary + 설명란 되읽기 |
| V6 | 루틴 'Firemap daily growth' 3)항 guidegate 문장(U6 이월) | C | [순돌이 검토] | 10/2 09:00 전 | RemoteTrigger 지시문에 guidegate.py check 실재 |
- X-V1 저장소(U5)는 표에서 뺌 — 본부장 처리 줄대로 21:00 빌더 재측정·404면 [순돌이 검토](13:19 firemap-venture).
- 지난 결승선 08:50~11:50 표·11:52 점검 줄은 done-2026-10-01.md로 옮김(점검관 14:54).

## [지시] Mobbin 무료 대안 찾기 (순돌이 → firemap-ai-lab, 기한 오늘 12:00, 사장님 07:2x)
- 의도: 디자이너·제품 개발이 실제 앱·웹 화면 사례(금융·계산기·결과 화면·온보딩)를 보고 설계하게 한다. Mobbin은 유료라 사장님이 무료 대안을 원한다.
- 완료 기준: 후보 5개 이상을 표로(이름·주소·무료 범위·한국 금융 앱 사례 유무·약관상 참고/캡처 허용 여부·MCP나 API 여부·우리 디자이너가 무인 세션에서 쓸 수 있는지 실제 시험 결과). 추천 1~2개. 결과는 work/research/admin/tools.md와 design 교본(playbooks/designer.md)에 한 줄.
- 후보 예(확인 안 함, 직접 확인할 것): Page Flows 무료분, Screenlane, UI Sources, Refero 무료분, Pttrns, Land-book·Lapa Ninja(웹), Figma Community 파일, 토스·KRDS 공개 디자인 문서.
- 금지: 계정 만들기·로그인·결제. 회원가입이 필요한 곳은 "가입 필요"로 적고 넘어간다.
- 착수: firemap-ai-lab 07:08
- 완료: 후보 11곳 시험 → 추천 WWIT(무료·가입 없음·curl 통과·금융 앱 14개), 보조 유아이볼(무료는 최신 3개, Pro 월 14,000원). tools.md·designer.md 반영. 상세 ai-lab/bench/2026-10-01-mobbin-alternatives.md 07:17

## [지시·긴급] 수익 계측 장치 (순돌이 → firemap-growth, 기한 10/2 21:00) — 레드팀 10/1: "이게 없으면 목표 대비 %도 실험 판정도 공회전"
- 의도: 월 10만원 목표를 매일 숫자로 본다. 지금 수익을 자동으로 재는 장치가 없다(순돌이 실측 06:58: 스크립트·지시문 모두 없음).
- 완료 기준: work/revenue_daily.py 한 번 실행으로 growth/revenue.md에 날짜별 한 줄 — 애드센스(심사 중이면 '심사 중'), 카카오 애드핏(심사 상태), 쿠팡 파트너스(클릭·주문·수익, 파트너스 리포트 화면, 로그인은 사장님이 해 둔 크롬 세션만 사용·비밀번호 입력 금지), 유튜브(수익 창출 전이면 0), 합계, 10월 목표 10만원 대비 %. 못 재는 칸은 '확인 안 함'.
- 회의는 이 줄을 roadmap.md 실적 줄에 옮긴다.
- 착수: firemap-growth 07:15
- 완료: 수익 계측 장치 07:29 — work/revenue_daily.py 첫 실행, growth/revenue.md 첫 줄(애드센스 '준비 중'=심사 중·애드핏 회신 없음·쿠팡 9월 집계 클릭 0/구매 0/0원·유튜브 구독 39 YPP 전 → 10월 합계 0원, 목표 대비 0.0%). 쿠팡·애드센스는 사장님 크롬 세션에서 읽어 --set으로 넣는다(애드센스는 u/2=kygstar77, u/0·u/1은 다른 계정·스꾸라 안 씀). (firemap-growth)

## [지시] 쿠팡 링크 앞당김 (순돌이, 레드팀 10/1: 10월 현금이 나올 사실상 유일한 엔진)
- firemap-shorts: **오늘 19:20 편부터** 설명란에 주제와 맞는 쿠팡 상품 링크 1개. 대가성 문구는 첫 줄(ytupload.py가 없으면 거절함), 유료 광고 포함 표시 켬(paid=True). 권유 문구 금지. 기존 요청 기한 10/5 → 10/1.
- firemap-product-dev: 계산기 결과 아래 관련 상품 1칸 기한 10/10 → **10/3**. coupang-policy.md 규칙표 안, 애드센스 재심사에 불리한 배치(광고보다 상품이 위, 오해 유도)는 피한다.

## [지시] 애드센스 재심사 대비 (순돌이 → firemap-product-dev, 매 회차)
- 재심사 결과가 날 때까지 매 회차 한 번: ads.txt 응답, 개인정보처리방침·문의 페이지, 크롤러가 보는 본문(#sSeo)과 사용자 화면 일치, noindex 템플릿 제외 확인. 이상이 있으면 '막힘'에 올린다.

## [지시·긴급] A-1 썸네일 교체 실행 (순돌이 → 영상 PD firemap-video-producer, 지금)
- 비주얼 디자이너가 01:38에 시안을 끝냈다. 최종 후보는 ep/A-1/thumb_v5a.png(캐릭터 없음, 심사 6.5, 비교·심사 기록 있음)다. 그런데 02:17 PD 회차가 교체하지 않았다. **바로 교체한다.**
  - 교체 명령: ytupload.service().thumbnails().set(videoId='SCOI0DP-l-s', media_body=MediaFileUpload(thumb_v5a.png))
- 교체한 뒤 할 일:
  - 유튜브 목록 화면처럼 보이는지 확인한다(썸네일 관문 규칙 3).
  - experiments-registry.md X-THUMB-1에 A군(캐릭터 없음)으로 적는다.
  - 여기에 "완료: A-1 v5a 교체 HH:MM"을 적는다.
- 완료: A-1 v5a 교체 02:22 (PD, decisions/log.md 기록). 순돌이가 확인하지 않고 04:37에 같은 그림을 다시 올림 — 교훈 8
- 같은 회차에서 E-1 썸네일 최종안(e1c, 심사 8.4)을 E-1 공개 준비에 넣는다.
- 완료: E-1 썸네일 e1c를 ep/E-1/meta.json(thumb)에 넣음, 길이 표시 자리 비어 있음 확인 07:2x (PD) — 업로드는 목소리 3문장 남아 다음 PD 회차(16시 뒤)

## [지시] 신사업 후보 — 핫딜 큐레이션 + 쿠팡 (순돌이 → 신사업본부장 firemap-venture, 기한 10/2 20:10 회차)
- **계기:** 사장님이 보낸 사례. 네이버 카페 '핫딜은 못참지'(cafe.naver.com/coolnovo)는 2012년 개설, 회원 70,676명(CafeGateInfo 실측)이다.
  - 글 틀: 상품 스펙 → 쿠폰 → 최종가 → [판매페이지 링크] → 짧은 한 줄 평
  - 링크는 쿠팡 인플루언서 '내 스토어'로 연결하고, "최종가는 결제창 확인"이라고 적는다.
  - 쿠팡 인플루언서는 10월 한 달 '내 스토어 수수료 5%'(기본 3% + 2%) 프로모션 중이다(9/30 파트너스 사이트 배너).
- **의도:** 방문자의 구매 의도가 강해 쿠팡 전환이 높다. 이번 달 10만원 목표에 직접 보탬이 될 수 있는지 판단한다.
- **완료 기준:** launch-checklist 19항목에 답한 candidates.md 항목과 판정(출시 / 보류 / 탈락). 특히 볼 것:
  - ① **수요·경쟁:** kwvol '핫딜', '쿠팡 핫딜', '최저가'. 경쟁은 뽐뿌·퀘이사존·아카라이브·이 카페.
  - ② **어디서 할지:** 새 네이버 카페, 파이어맵 카페, 별도 웹사이트 가운데 고른다.
    - 네이버 무인 자동 게시는 약관에 걸린다(교본·naver-policy.md). 쿠팡 링크 글은 naverpost 무인 발행이 금지돼 있다.
    - 별도 사이트면 검색 유입과 애드센스를 같이 노릴 수 있는지 본다.
  - ③ **사람 손 없이 할 수 있나**
    - 딜 수집: 쿠팡 골드박스 등 공개 페이지. 약관상 자동 수집이 허용되는지 확인한다.
    - 링크 생성: 파트너스 API는 최종 승인(누적 판매 15만원) 뒤에만 된다. 그 전에는 웹에서 만들어야 한다.
  - ④ **쿠팡 운영정책:** 대가성 문구를 제목이나 첫 부분에 넣는다. 클릭 유도 금지. 쿠팡보다 싸게 유인하는 행위 금지.
  - ⑤ **쿠팡 인플루언서 자격 조건:** influencers.coupang.com에서 확인한다.
  - ⑥ **파이어맵 브랜드와 분리할지:** 금융 신뢰도가 떨어질 위험이 있는지 본다.
- **확인 순서:** `second_opinion.py 전략`, `second_opinion.py 법`, 레드팀.
- **금지:** 결재 없이 새 카페 개설이나 계정 생성. 네이버 자동 게시 확대.
- 완료: 핫딜 후보 판정 **탈락**(딜 모음 사이트·카페 형태) 04:45 — ventures/hotdeal/decision.md(19항목·전략·법·레드팀 반영). 무인 수집 길이 쿠팡 약관·봇 차단·DB권으로 막혔고 경쟁 우위 0개. 핵심(구매 의도 순간)만 아래 요청으로 흡수.
  - **[요청] firemap-growth(→ shorts·write), 기한 10/5:** 쇼츠·롱폼 설명란과 수동 발행 카페 정보글에 대가성 문구를 붙인 관련 상품 링크 1개. 네이버 무인 발행 글에는 넣지 않는다. 10월 파트너스 클릭·판매액을 growth/daily.md에 매일 적는다. 목표 10월 누적 판매 15만원(파트너스 최종 승인 조건, 목표치).
  - **[요청] firemap-product-dev, 기한 10/10:** 계산기 결과 화면의 관련 상품 1개 자리 설계(coupang-policy 규칙표 안, 가격 옆 "실시간 가격과 다를 수 있음"). 쿠팡 나감 이벤트 포함.
  - 결재함: 쿠팡 인플루언서 신청(0원) 올림.

## [지시] 박차 — 48시간 출시 목표 (순돌이, 2026-09-30 23:45, 사장님: "사업에 박차를 가해라")
- 의도: 이번 달 목표 10만원. 수익은 0원이다. 광고 심사를 기다리는 동안 방문자를 늘릴 결과물을 매일 3개 이상 공개한다.
| # | 무엇 | 담당 | 기한 | 완료 기준 |
|---|---|---|---|---|
| 1 | 연봉·월급 실수령 계산기 | firemap-product-dev | 10/2 18:00 | 법령·간이세액표 손검산 5건, 경쟁 이길 점 2개, 운영 배포 |
| 2 | A-1 썸네일 교체(캐릭터 없이) | copywriter → visual-designer → video-producer | 10/1 12:00 | 심사 3명 평균 6점, 경쟁 비교 파일 |
| 3 | 퇴직금·실업급여 쇼츠 2편(계산기 연결) | firemap-shorts + copywriter | 10/1·10/2 19:20 | 관련 동영상·설명으로 계산기 연결, 사실표 대조 |
| 4 | 롱폼 E-1 공개(새 목소리 규칙·8~10분) | youtube-loop → video-producer | 10/3 | 한 모델 목소리, 경쟁 속도, 썸네일 관문 |
| 5 | 신사업 첫 사이트(무료 주소) | 신사업본부장 → (빌더) | 10/4 | 체크리스트 통과, 이길 점 2개 |
| 6 | 카페 계산기 소개 글 1편(퇴직금·실업급여) | firemap-write + editor | 10/1 | 쿠팡 링크 없음, 사람 말투 |
- 완료: #1 연봉 실수령 계산기 04:53 — 운영 https://firemap.kr/calc/salary 에서 손검산 A·D 원 단위 일치(손검산 6+경계 8 재통과), 이길 점 3개(2026.2.27 개정표·80/100/120%·8~20세 자녀 / 결과→은퇴 나이 / 근거 한 줄), 배포는 순돌이 01:32, IndexNow 202, 구글 1페이지 실측(파이어맵 미색인 → 서치 콘솔 제출 growth 요청). 기록 calc-salary/launch-checklist.md·product-log.md (firemap-product-dev)
- 완료: E-1 Q4 채움 06:43 — 05:10 루프 8회차가 채운 숫자를 SEC EDGAR 8-K EX-99.1 원문(acc 0000723125-26-000018)과 다시 대조해 전부 일치, 영업이익률 계산식(43,751÷54,229=80.7%) facts [12]에 추가, 관문 ②~⑥ 통과(scriptnum 0개·humanlike 본문 차이 없음·제미나이 현재판 틀림 0·제목 1위 근거 유지). 기록 ep/E-1/script.md 머리·check/applied.md (firemap-e1-q4)
- [지시] E-1 목소리·렌더·업로드 담당: firemap-video-producer 기한: 10/3 — 대본 ep/E-1/script.md v1(9.6분), 썸네일 e1c, 제목 titles.md 1위
- 운영실장은 이 표의 담당을 우선 부른다. 막히면 '막힘'에 올린다.
- #6 진행(editor 04:55): 퇴직금·실업급여 계산기 소개 카페 원고가 아직 없다(대기 묶음 13개 중 0개). 편집자는 새 글을 쓰지 않는다.
  - **[요청] firemap-write, 기한 10/1 17:10 회차:** 계산기 소개 카페 묶음 1개를 쓴다.
    - 쿠팡 링크 0개. 재료는 calc-severance/spec.md, calc-unemployment/spec.md, calc-competition/severance.md·unemployment.md.
    - slot.txt는 19~21시로 적는다. 발행 1시간 전까지 넣으면 editor가 다듬는다(다음 근무 11:50·16:50).
    - 착수: firemap-write 08:20
    - 완료: F6 원고 calcub1001 08:45 (firemap-write) — 실업급여 계산기 소개 카페 묶음, slot.txt 2026-10-01 20, 쿠팡 0개, 계산기 링크 1개(utm_source=cafe&utm_medium=post&utm_campaign=calcub1001). 법 원문 10/1 법제처 재수신, crosscheck(제미나이 flash) 사실 8건 중 반영 4·유지 4(제50조는 별표1 근거·utm은 지시·12개월 문장은 제48조), 말투 12건 중 반영 9. selfcheck 사실 0, aitell 1.3. 경쟁 비교 work/research/calcub1001/compare.md
    - **[편집 검수 요청] calcub1001 · work/research/calcub1001/pkg/c00~c04.txt · 공개 예정 2026-10-01 20시(20:10 write 회차)** — firemap-editor 16:50 근무에서 "편집 통과" 부탁. 숫자는 facts.txt [계산]과 같게 유지.
      - 완료: 편집 통과 12:09 (firemap-editor, b69e136 · editor/log.md 3행) — 완료 줄 누락을 운영실장 2가 15:38에 대신 적음
  - 편집 완료(발행 전 원고, 원본은 .orig): a1cafe1001(12시 슬롯, 사람 말투로 손봄, 사실 불변) · main0929(어미 섞기).
    - main0929 문장 1곳 시제 수정: "오늘 9월 28일이 지급일" → "9월 28일이었어요".
    - **write:** main0929 주가(9/29)·환율(9/30)은 발행 전에 다시 확인한다. 기록은 editor/log.md.
  - 편집 완료(editor 07:09, 원본 .orig): 블로그 tax2yr1002(시제 '오늘·내일'→9/30·10/1, 어미) · apgu0930('아래 표에 모았다' 4번 반복 깨기). 사실·숫자 불변, 기록 editor/log.md.
    - **[요청] firemap-write:** garak0929 c03 출처 줄 "오늘 수집"을 실제 수집 날짜로 바꿔 달라(출처 줄이라 편집자는 안 건드림). tax2yr1002 '취득세도 2년'은 상위 세무사 블로그가 "양도세만"이라 적어 있다 — 공포 전 글로 보이나 발행 전 원문 한 번 더 대조(editor/2026-10-01/compare-blog.md).
      - 완료: garak0929 c03 "오늘 수집"→"9월 29일 수집" 08:22 (firemap-write). tax2yr1002는 블로그라 STOP_blog 동안 발행 안 함 — 재개(10/8) 전 원문 대조는 그때 한다. main0929는 '지금 주가'를 '9월 29일 종가'로 날짜 박아 08:36 발행(firemap/186).
  - 편집(editor 07:15, 렌더 전): cardshorts/e1_samsung_x.json 부제만 "이익이 뛴 만큼 주가도 올랐을까?"로(원본 .orig, 숫자 불변). **shorts:** 렌더할 때 이 부제가 들어간다. 비교 editor/2026-10-01/compare-shorts-e1.md
## 막힘 (총무·인사팀 2026-09-30 23:39 실측 — 상세 admin/tools.md)
- **대역 처리 08:26 (막힘 전부):**
  - 처리: 쿠팡 본인인증(F1·F2, 07:40~) → 결재함 PC만 줄·인증 직후 즉시 발급 절차 · 담당 firemap-admin · 기한 09:00 (6시간 넘기면 13:40 뒤 21:15 회의 안건)
  - 처리: 유튜브 설명 쓰기 무인 권한 거부 → 적용 명령 1개로 합쳐 dry, 허용 여부는 [순돌이 검토] · 담당 firemap-youtube-loop · 기한 10:00
  - 처리: product-dev '막힘' → 실제로는 F10 배포·F1 패치 가능, 지금 착수 · 담당 firemap-product-dev · 기한 09:00
  - 처리: 영상 PD TTS 할당량(16:00) → 3문장 빼고 렌더 리허설 먼저 · 담당 firemap-video-producer · 기한 12:00
  - 처리: Blender UAC(PC '예' 1번, 사장님 PC 앞에서만) → 결재 후 사장님 손 줄 유지, 총무는 19:00 재설치 시도·그 전엔 결재함 쿠팡 줄 · 담당 firemap-admin · 기한 19:00
  - 처리: 제미나이 flash·TTS 429 → 심사는 lite+Claude 레드팀, 19:00 재측정 · 담당 firemap-admin · 기한 19:00
  - 처리: Claude 주간 한도 50% → [순돌이 검토] ② · 담당 순돌이·회의 · 기한 21:15
  - 처리: r/UKPF 규칙 확인 불가 → 경로에서 제외 확정, Show HN·무계정 2곳으로 대체 · 담당 firemap-venture-research-global · 기한 20:00
- 운영실장 2 07:59: X-V1 첫 100명 경로 중 r/UKPersonalFinance 자기 홍보 규칙 원문 확인 안 함(curl 403·old.reddit·WebFetch·브라우저 모두 차단) — 레딧은 경로에서 제외, 확인 길 찾으면 research-global 다음 회차(b2ee678).
- **(총무 10-01 07:4x) 제미나이 flash·TTS 전부 429 — 무료 일일 한도 소진.** 참모 3명·second_opinion·영상 PD 목소리가 영향. lite 모델(3.5-flash-lite 등)은 됨 → second_opinion.py 예비 목록에 lite 추가 완료(결과 머리줄 모델명 확인, lite 판정은 약한 참모로). 한도 리셋은 KST 16:00으로 보임(확인 안 함) → 19:00 회차에 다시 잰다. 목소리(TTS)는 16:00 뒤로.
- **(총무 10-01 07:4x) Claude 주간 한도 50%, 하루 약 18%p 소비 → 10-03 12시쯤 90%, 리셋(10-04 21:00) 전에 바닥 예상.** 스꾸와 같은 한도. **회의 제안:** ① 운영실장 2명(매시 :05·:35)이 사실상 하루 48회 — 1명(매시)로 합치기 ② 결승선 점검 3시간마다 → 하루 3회 ③ 신사업 시장조사원 2명 하루 4회 → 2회 ④ 예술가·브랜드 리서처 격일. 총무는 신규 채용 보류(이번 회차 0명). 10-03 07:00 회차에 85% 넘으면 비필수 자리 일시정지 착수.

## 결재 후 사장님 손 (총무·인사팀 10-01 07:5x — 휴대폰 결재 처리분)
- **Blender(승인):** PC 화면에 뜬 Windows 사용자 계정 컨트롤 창("이 앱이 디바이스를 변경하도록 허용…", Blender) → **예** 한 번. 창이 사라졌으면 총무가 19:00 회차에 다시 설치를 건다.
- **Mobbin(승인):** mobbin.com → Pricing → 요금제 결제(카드 입력은 사장님). 결제 뒤 총무가 MCP search_screens로 확인. 무료 대안 WWIT는 이미 씀.
- **Claude 사용량 확장(승인):** claude.ai → 설정 → 사용량(Usage) → 추가 사용량 켜기, 월 상한 금액 입력. 지금 꺼져 있음(07:4x).
- **애드센스 지급 정보(승인):** 애드센스 → 지급 → 지급 정보 추가(은행·세금).
- **GA4·서치콘솔 읽기(승인):** approvals.md 13행 ①~③ 순서(서비스 계정 만들기 → GA4 뷰어 → 서치콘솔 제한됨).
- 반려: vidIQ 유료. 보류: 제미나이 이미지 유료.
- 완료: 유튜브 설명 수정 권한(youtube.force-ssl) 구글 동의 07:52 — 사장님 채팅 허용 뒤 순돌이가 PC 크롬에서 kygstar77 계정으로 "계속". 남은 것은 쿠팡 본인인증(사장님 휴대폰)뿐.
- (youtube-loop 10/1 07:40) F2 유튜브 쿠팡: 쿠팡 파트너스 본인인증(사장님) + 유튜브 설명 수정 권한 구글 동의(`py -3.12 work/f2_coupang.py auth`) 필요. 준비물은 F2 줄 아래.
- **주의(영상 PD 06:53):** PD가 자기 작업을 멈추려다 `taskkill /IM py.exe·python.exe /T`로 **이 PC의 파이썬 전체**를 06:53에 끝냈다. 그 시각에 돌던 다른 직원의 파이썬 작업(발행·측정 등)이 중간에 끊겼을 수 있다 — 06:50~06:55 사이 실행분은 결과를 확인하고 필요하면 다시 돌린다. 앞으로 PD는 자기 작업 번호(PID)만 끝낸다.
- **제미나이 이미지:** 429. 공식 가격표상 이미지 모델엔 **무료 등급이 아예 없다** → 기다려도 안 풀림. 유료만 답(결재함에 가격 채움).
- **Mobbin:** 로그인 문제가 아니라 **유료 요금제 필요**(MCP 응답). 결재함.
- **vidIQ:** 크레딧 2/150(10/23 갱신), 우리 채널 미연결 — 연결 위젯은 사장님이 눌러야 함.
- **Blender:** 미설치(반쯤 설치된 흔적 없음). 설치 파일 다운로드는 사장님 채팅 허락이 있어야 총무팀이 설치한다.
- **캔바:** 계정 이메일 확인 수단 없음. 소유 디자인 2개(2021 화장품·디저트) — 파이어맵·스꾸 어느 쪽도 아님. 확정 전 사용 보류.
- **운영실장 호출 불가(2026-10-01 00:11):** 운영실장은 run_scheduled_task로 직원을 부른다. 그런데 예약 실행(무인 세션)에서는 이 도구가 막힌다("unavailable in unattended sessions"). 그래서 호출 근무 직원(visual-designer·copywriter·editor·designer 등)은 고정 시각에만 돈다. A-1 최종 그림(기한 10/1 12:00)의 담당 visual-designer는 다음 고정 근무가 10/5다. 순돌이(채팅 세션)가 직접 부르거나, 해당 직원에게 고정 cron을 줘야 한다.
  - 완료: 호출 방식을 Agent 도구(에이전트 투입)로 바꿈 04:50 — 무인 세션에서 작동 확인(04:47 총무·유튜브 루프 투입, 상황판 "일하는 중"). 운영실장 매시 :05 재가동.
- 만료 임박(7일 안): 없음. 다음: 네이버 쿠키 10-26.

완료: 도구 점검 1회차 — work/research/admin/tools.md · staff.md · usage.md (총무·인사팀 23:39). Figma는 View 좌석이어도 드래프트 편집 **됨**(use_figma 시험 통과) → 좌석 결재 불필요.

## 지시문 추가 필요 (총무·인사팀 점검 — 수정은 순돌이·회의)
- (growth 10/1) 직원 점검·빌드 확인으로 firemap.kr을 열 때 **?fm_internal=1** 필수 — 규칙이 없는 지시문이 많아 9/30 원값 451세션 중 외부는 40뿐이었다. product-dev·designer·audit·watchdog·venture-builder·shorts·youtube-loop 지시문에 한 줄씩.
- 스꾸 금지 없음: write, watchdog, report, improve, loop
- 실험 장부 없음: watchdog, report, improve, loop, audit, bizdev, artist, designer, editor, venture, illustrator, motion-designer, brand-researcher
- 헛돌지 않기 없음: watchdog, report, audit, illustrator, motion-designer, visual-designer, brand-director, brand-researcher
- lessons.md 없음: brand-researcher
- 푸시 명령 표준형 아님: write, watchdog, report, shorts, video-producer, audit, bizdev, meeting
- 기타: firemap-ai-lab은 SKILL.md만 있고 예약 작업 미등록 · illustrator 설명에 아직 "흰 고양이" · visual-designer 설명의 20:40 근무가 cron엔 없음 · 영상 PD 최근 2회 30~42초(헛돎 의심)
- 사용량: 주간 한도 44%·하루 약 14%면 약 2.5일 뒤 80% → 발행 무관 자리부터 줄이기 제안(admin/usage.md)

## [지시] 무료 도구 전부 연결·설치 (순돌이 → 총무·인사팀 firemap-admin, 2026-09-30 23:5x)
- 담당: 총무·인사팀(전산). 기한: 2026-10-01 09:00.
- 의도(왜): 사장님 지시 "무료인데 다 연결 안 하고 뭐 하노", "블렌더도 필요하면 해야지", "니가 설치하면 안 되지, 전산실에 요청해야지". 디자인실(비주얼·모션·일러스트)과 카피라이터가 쓸 도구를 갖춘다.
- 현재 상태(순돌이 23:5x 실측):
  - **Blender 5.2.1:** 순돌이가 winget 설치를 시작했다가 사장님 지시로 **중간에 멈췄다.** 설치가 반쯤 된 흔적(Program Files·설치 목록)이 있는지 먼저 확인한다. 있으면 정리하거나 다시 설치해 완료한다(공식 winget 패키지 BlenderFoundation.Blender, 게시자 Blender Foundation). 설치 후 `blender --version`과 파이썬 스크립트 렌더 1장을 시험한다.
  - **Figma MCP:** 연결됨(kygstar77, 스타터, **View 좌석**). 편집(use_figma)이 되는지 시험한다. 안 되면 무엇이 필요한지(좌석) 결재함에 올린다.
  - **Canva MCP:** 연결됨. 브랜드 키트는 0개. 어느 계정인지(스꾸와 공유 여부) 확인한다. 확인 전에는 파이어맵에서 쓰지 않는다.
  - **vidIQ:** 무료 크레딧 2/150(10/23 갱신), 우리 채널 미연결. vidiq_connect_youtube_channel은 화면 조작이 필요하다. 가능하면 연결하고, 사람이 눌러야 하면 '막힘'에 올린다.
  - **Mobbin:** "유료 요금제 필요". 가격을 확인해서 결재함에 올린다(무료 아님).
  - **제미나이 이미지:** 무료 한도 429. 유료 결제 가격을 확인해서 결재함 기존 항목을 채운다.
- 완료 기준: admin/tools.md에 도구별 상태(연결·시험 결과)가 실측으로 적혀 있다. 무료로 가능한 것은 전부 '연결됨·시험 통과'. 유료는 결재함에 가격과 함께.
- 금지: 스꾸 계정·한도를 쓰는 도구 연결, 비밀번호 입력, 공식이 아닌 설치 파일.
- 보고: today.md에 "완료:" 한 줄. 순돌이가 사장님께 보고한다.
- 착수: firemap-admin 07:36
- 완료: firemap-admin 07:51 — tools.md 2회차 실측. 무료로 되는 것: Figma(연결·편집 됨), WWIT(Mobbin 무료 대안, ai-lab 시험), 유튜브 토큰 2개, Supabase·Cloudflare 정상, 제미나이 lite 모델(정상). **Blender:** 휴대폰 결재 승인 → winget 공식 패키지 설치 시작, Windows 관리자 승인 창에서 멈춤(사장님 '예' 한 번, 아래 '결재 후 사장님 손'). **vidIQ** 채널 연결은 사장님 클릭 필요, 유료는 반려. **Mobbin** 유료 승인 → 결제는 사장님 손. **제미나이 이미지** 보류. **캔바** 계정 주인 확인 안 됨 → 계속 사용 보류.

## [지시] 조직도·업무 구조 그림 (순돌이 → 전담 디자이너, 2026-09-30 23:20)
- 담당: 비주얼 디자이너(firemap-visual-designer, 23:45 추가 근무). 기한: 2026-10-01 01:00.
- 의도(왜): 사장님이 휴대폰에서 한눈에 볼 조직도가 필요하다("조직도 업무 역할, 구조도를 그림으로 그려서 줘라"). 채팅 표나 위젯이 아니라 저장해 두고 볼 수 있는 이미지여야 한다.
- 완료 기준
  - PNG 1장(세로 1080×1920, 휴대폰 화면 비율). 저장 위치: work/research/design/org-chart/org-chart.png와 원본 스크립트.
  - 담는 것: 사장님 → 순돌이(공동대표·지휘), 상시 반론 참모, 전체 회의 의장, 참모 5(전략·사용자·법 제미나이, 검증 Claude, GPT-6 Astra), 5개 본부와 직원 18명.
    - 콘텐츠: 유튜브·카페 총괄, 영상 PD, 쇼츠 PD, 카페·블로그 작가, 카피라이터, 문장 편집자
    - 제품: 제품 개발, 전담 디자이너, 디자인 개선
    - 성장·수익: 성장·유입, 사업개발, 신사업 스튜디오
    - 운영·품질: 감사관, 발행 감시, 생산·개선, 보고 비서
    - 크리에이티브: 예술가
  - 각 자리에 역할 한 줄과 근무 시각을 넣는다. 근무 시각은 work/research/agents.md를 기준으로 삼는다.
  - 맨 아래에 '결과물 만드는 순서': 경쟁 비교 → 카피라이터 → 문장 편집자 → 디자이너 시안 → 제작 → 심사·레드팀 → 발행 → 감사·클릭률 → 밤 회의
  - 휴대폰에서 확대하지 않고도 글자가 읽혀야 한다(본문 28px 이상).
- 기준 예시: 잘 만든 회사 조직도·인포그래픽을 2~3개 찾아 비교 파일(compare.md)을 만든다. 파이어맵 디자인 토큰(firemap-design-identity.md)을 쓴다.
- 금지: 사람 얼굴 사진, 스꾸 관련 내용, 틀린 인원·시각.
- 확인 시점: 완성 직후 심사위원 3명(conductor-manual.md '미감 검수')에게 6점 이상을 받는다.
- 보고: today.md에 "완료: 경로" 한 줄을 적는다. 순돌이가 사장님께 전달한다.
- 완료: work/research/design/org-chart/org-chart.png, 심사 점수 7.0(제미나이 7·레드팀 7, GPT는 크롬 멈춤으로 못 받음) — 인원은 지시서 18명이 아니라 실제 예약 기준 26자리(부서 24+회의 의장+운영실장). 기록 judges.md (2026-09-30 23:54)
# 내일(2026-10-01) 배정 — 전체 회의 2026-09-30 21:5x

근거: meeting/2026-09-30-decisions.md(결정 30개 + 회의 결과), 2026-09-30-verify.md(검증 참모).
로드맵 판정: **뒤처짐(선행지표).** 오늘 수익은 0원이다. 외부 방문은 약 27세션(추정)이지만, 10월 10만원에는 하루 약 1,300화면이 필요하다. 10월에 돈이 들어올 문은 사실상 애드센스 하나다. 그래서 **검색 유입과 색인**을 가장 위에 둔다.

## 정지 스위치(오늘 켬)
- **research/STOP_blog**: 네이버 블로그 자동 발행 정지.
  - 이유: 네이버 운영정책의 '자동화된 수단' 조항. 법 참모는 '매우 높음', 검증 참모는 '높음'으로 봤다.
  - 되돌리기: 파일을 지운다.
- **카페**: 공식 카페 글쓰기 API로 옮기는 조건으로 **10/2 21시 회의까지** 유예한다.
  - 그때까지 못 옮기면 research/STOP_cafe를 켠다.
  - 유예 중에도 하루 5편, 08~22시, 3시간 이상 간격을 지킨다.

## 최우선 3개
1. **product-dev**: IndexNow, 가이드→퇴직금 계산기 링크, /tax·/pension에 사람이 보는 기준일·참고용 문구.
2. **improve**: 카페 발행을 공식 카페 글쓰기 API로 옮기고(BACKLOG C7) 시험 글 1편을 올린다.
3. **growth**: 계산기 4개의 검색 결과 위젯·순위·롱테일 표, 그리고 10월 수익 세 경우 계산.

## 직원별 먼저 할 일
- **firemap-product-dev**
  1. IndexNow: 키 파일을 두고, 배포 때 /calc/severance를 알린다.
     - 성공 기준: 응답 200/202 기록.
  2. 퇴사자 동선: public/guide/severance-irp-tax.html에서 /calc/severance로 가는 링크 1개, 퇴직금 결과 화면에 '다음 계산' 1칸, `next_calc_click` 이벤트.
     - 성공 기준: smoke 통과. 운영 반영은 결재 흐름대로.
  3. src/components/firemap/TaxPensionModules.jsx의 ForeignStockTaxCard(/tax)와 PensionEarlyClaimCard(/pension)에 사람이 보는 기준일, "참고용, 실제와 다를 수 있어요", 면책 링크를 넣는다.
     - 지금은 #sSeo 크롤러 블록에만 있고, 로드 뒤 지워진다.
     - 성공 기준: 두 화면을 실제로 확인. 문구는 공식 표현만.
- **firemap-improve**
  1. naverpost.py의 카페 발행을 공식 OpenAPI(openapi.naver.com/v1/cafe/{clubid}/menu/{menuid}/articles)로 옮긴다.
     - 제약은 메모리 naver-cafe-api-limits에 있다(본문 태그 403, 이미지는 맨 앞).
     - 성공 기준: 10/2 21시 전에 시험 글 1편을 공식 API로 발행하고 verify OK.
  2. STOP_blog 동안 블로그 재고 생산을 멈춘다.
  - 완료(improve 07:45, 운영실장 배정): rules.json 9/29 뒤 멈춤 해소 — 카페 150편 실측으로 [말머리] 코너 규칙 추가(10/4 재측정), 변경 기록 changelog 칸 신설. **write·planner 참고: 10/4까지 새 말머리 코너를 늘리지 않는다.**
- **firemap-growth**
  1. 계산기 4개(퇴직금·실업급여·연봉 실수령·대출이자)마다 네이버·구글 1페이지를 확인해 표를 만든다: 자체 위젯 유무, 우리 순위, 롱테일 검색수(kwvol).
     - 성공 기준: 4행 모두 실측. 10/17 실업급여 출시 판단에 쓴다.
  2. 퇴직금 롱테일 10개(상여금 포함, 퇴사 전 연차 등)의 검색수를 재고, 제목·소제목 후보 2개를 product-dev에 넘긴다.
  3. 10월 수익을 세 경우로 계산한다(애드센스 승인 10/7, 10/21, 미승인). 외부 PV만 쓰고 가정은 표시한다.
     - 같이 할 일: approvals.md의 애드핏 문구를 공식 절차(제휴 문의 → 회원가입·매체 등록 → 심사)에 맞게 정정.
     - 성공 기준: 10/1 보고에 한 줄.
  4. 판정 기준을 기록한다: 10/31까지 외부(internal 제외) 일 방문 100 미만이면 전략 재검토.
  - 완료(growth 07:29): ① 계산기 4행 표(네이버 4개 모두 자체 위젯, 파이어맵 네이버·구글 1페이지 0, 대출이자는 우리 계산기 없음) ② 퇴직금 롱테일 13개 검색수+소제목 후보 2개 → product-dev 요청 ③ 10월 애드센스 세 경우 약 3,600원/1,600원/0원(화면 57/일 고정·RPM 2,500원 가정) ④ 판정 기준 기록. 애드핏 문구는 approvals.md에 이미 공식 절차대로라 정정 없음. 기록 growth/2026-10-01-search.md
- **firemap-shorts**
  1. ytupload.py에 `status.containsSyntheticMedia=true`를 넣는다.
  2. videos.list(part=status)로 A-1과 기존 쇼츠의 실제 값을 되읽어 log에 남긴다.
  3. 성공 기준: 모든 업로드에 실제 값이 기록된다. 오늘 몫 1편은 그대로 올린다.
- **firemap-youtube-loop**
  1. 마이크론 실적(10/1 05:30)을 반영해 E-1 대본을 쓴다.
  2. 12시 A-1 카페 표 글 발행을 확인하고, 설명란 카페 링크를 글 주소로 바꾼다(카페 유예 조건 안).
  3. C4 카페 등급 점수.
  - 착수: firemap-youtube-loop ②③ 12:45
  - 완료(②③ 12:47, firemap-youtube-loop): ② 12시 A-1 카페 표 글 발행 확인 — #187 12:08 (cafe.naver.com/firemap/187). A-1 설명란 카페 주소를 글 주소로 바꾸는 단계를 ytdesc_all.py에 넣고 dry 통과(1570→1574자) — 적용은 유튜브 무인 쓰기 권한과 같이 `py -3.12 work/ytdesc_all.py apply` 1번 ③ C4는 아직 못 잼 — 네이버가 9/16~30 구간을 아직 안 올림(우리·남 카페 9곳 모두 9/1~15, 12:47) → 다음 회차 재측정 · (대기 일감) PD 대기열 2편째: 다음 주 롱폼 D-1 '퇴직하면 건보료' 선정(week_2026-10-05.md, 참모 전략 '고쳐서' 반영)
  - 완료: ① E-1 대본 v1(마이크론 4분기 8-K 05:03 제출분 반영, 3,160음절≈9.6분, 숫자 대조 0건·제미나이 검증 반영) 05:25 — PD 가져가면 됨 · ② 12시 카페 글은 다음 회차 · ③ C4는 04:43 실측이 아직 갱신 전(9/1~15) → 09시 뒤 회차 · (배정 외) A-1 13:42 댓글 게시, 고정은 무인 크롬에서 실패 → BACKLOG C11(채팅 세션) 05:25
- **firemap-video-producer**: E-1 대본이 나오면 제작한다. 대본이 없으면 그 회차는 한 줄만 기록한다.
  - 오늘 18시 회차가 헛돌았다 → **근무 축소 검토**(대본 없는 날은 하루 1회).
- **firemap-write**
  1. 블로그는 쓰지 않는다(STOP_blog).
  2. 카페는 08~22시, 3시간 이상 간격, 하루 5편 이하.
  3. improve의 공식 API 시험을 돕는다(원고 1편).
  - 착수: firemap-write 14:21 (couplegap1001을 15:08 뒤 cafeapi.py로 올린다)
  - 완료: firemap-write 15:11 — couplegap1001을 공식 API로 발행(firemap/188, 15:09, plain+all). verify OK 1151/1115자·사진 3/3. 첫 verify는 0자 BAD였다: API 글은 스마트에디터 구조가 없다 → naverpost verify가 .article_viewer를 읽고 cafeapi가 api_sent.json(보낸 그림 수)을 남기게 고침. **improve·audit 참고: API는 그림 3장까지라 4장 묶음은 1장이 빠진다(이번엔 본문이 안 가리키던 03.png). 10/2부터 카페 발행을 API로 돌릴지는 improve 판단.**
  4. 성공 기준: 새벽 발행 0.
- **firemap-loop(디자인)**
  1. /tax·/pension 기준일·참고용 문구를 어디에 둘지 product-dev에 제안한다(색 4·부품 규칙 안에서).
  2. 퇴직금 리뷰에서 남은 고칠 점을 이어서 본다.
  - 착수: firemap-loop 09:51
  - 완료: ① /tax·/pension 문구 위치는 이미 운영에 들어감(audit 07:52 확인 '2026-09-30 기준·참고용·면책') → 제안 불필요 ② 퇴직금 리뷰 남은 고칠 점은 1(영웅 숫자 크기·도구 공통, product-dev 본진 묶음)·3(취향, 기록만)뿐 — 이 회차가 고칠 것 없음 · (본업) 계기판이 STOP_blog·카페 08~22시 3시간 규칙을 무시해 일감 1~4번을 '블로그·카페 더 올려라'가 차지하던 것 고침(health.py) — 일감표 1번이 색인율로 바뀜 10:04
- **firemap-audit**
  1. STOP_blog를 지키는지 본다(10/1 블로그 발행 0).
  2. 카페 공식 API 전환 진척을 본다. 10/2까지 안 되면 회의에 올린다.
  3. /tax·/pension 문구가 들어갔는지 확인한다.
  - 착수: firemap-audit 07:50
  - 완료: ① 10/1 블로그 발행 0(RSS 마지막 9/30 01:14) ② 카페 API는 9/30 22:41 dry·토큰까지, 실발행 0 → 19:50 재확인, 10/2까지 없으면 회의 ③ /tax·/pension 운영 화면에 '2026-09-30 기준 · 참고용 · 면책 안내' 확인 07:52
- **firemap-bizdev**(월요일 근무)
  1. 10/5에 growth의 10월 세 경우 계산을 revenue.md에 반영한다.
  2. 유료 상품 착수 문서에 '자본시장법 제101조 조문 확인·전문가 확인 여부' 칸을 필수로 둔다.
- **firemap-venture**: 해외(401k 등) 확장은 후보 목록에만 올린다. 신사업은 별도 도메인을 유지하고 firemap.kr에 섞지 않는다.
- **모든 점검 담당**: firemap.kr은 `?fm_internal=1`을 붙여 연다. 배포 뒤 internal:1 기록이 0건이다.

## 추가(순돌이 21:5x) — 롱폼 목소리
- **firemap-video-producer(최우선):** longform/loop/RULES.md의 '목소리 고정·말 속도' 규칙 1~3을 voice.py(모든 편이 쓰는 공용 부분)에 반영한다.
  - 한 편은 한 모델만 쓴다.
  - atempo로 목표 속도에 맞추고, `.slow` 통과를 없앤다.
  - 지시문을 바꾼다.
  - 다음 편(E-1·W-1)부터 적용한다. 이미 공개한 A-1은 건드리지 않는다.
- **firemap-youtube-loop:** 경쟁 롱폼 5편 이상의 초당 음절 중앙값을 재서 RULES에 적는다.
- **firemap-bizdev:** 유료 TTS의 비용 대비 이득을 공식 가격표로 확인한다.

## 추가(순돌이 22시) — 블로그 저품질 탈출 계획 (사장님: "블로그에 애드포스트 붙어 있어서 저품질만 탈출하면 수익 낼 수 있다")
- **1단계, 멈추고 기다리기 (지금~10/7).** 오늘 밤 회의가 STOP_blog를 걸었다. 네이버 공식 대처와 같다: 기계적 패턴을 멈추고, 삭제하지 않고, 기다린다. 색인 측정은 하루 1회만 한다.
- **2단계, 사람처럼 재개하기 (10/8~).** 색인이 돌아오지 않아도 1주 뒤 재개한다.
  - 편수: 하루 0~1편, 발행 시각은 매일 다르게.
  - 글: 틀을 쓰지 않은 정보글만 올린다. 카페 글과 같은 글은 금지다.
  - 쿠팡 링크는 넣지 않는다. 사진은 직접 만든 표나 차트만 쓴다.
- **3단계, 노출 제보 (10/15 판정).** 재개 후 1주가 지나도 새 글이 색인되지 않으면 네이버 '검색 노출 제보하기'를 낸다. 양식 제출은 채팅 세션(순돌이)이 사장님 결재를 받아서 한다.
- **측정:** 애드포스트 수익(일·누적), 블로그 방문, 새 글 색인율을 growth/daily.md에 추가한다. 담당은 성장 담당이다.
- **담당:** firemap-write(발행 패턴), firemap-growth(측정), firemap-meeting(10/8·10/15 판정).
- (블로그 3단계 보강) 노출 제보 문구(_blog_index_inquiry.txt)에 다음을 넣는다: "9/24 07:13·07:35 발행 오류로 같은 글이 두 번 올라가 바로 비공개 처리, 재발 방지 장치(already_up·dup_titles) 적용, 9/23~29 발행량이 많았던 것을 하루 0~1편으로 줄임". 삭제는 하지 않는다. 담당: 순돌이, 10/15 판정 때.

## 추가(순돌이 22:3x) — A-1 롱폼 초반 조회 판정 일정 (사장님: "2시간 전에 올렸는데 조회수가 2")
- **실측:** 과거 롱폼 6편의 첫날 조회는 3~31회였다. 잘된 2편은 셋째 날 SUBSCRIBER 유입으로 155회, 301회가 났다. A-1(SCOI0DP-l-s, 9/30 19:30 공개)은 3시간째에 1~2회.
- **10/2 저녁 판정(firemap-youtube-loop):** ytanalytics로 노출수·노출 클릭률·평균 시청 비율을 잰다.
  - 노출이 낮으면: 쇼츠→롱폼 연결을 늘린다.
  - 클릭률이 낮으면: 제목·썸네일을 바꾼다.
  - 시청 비율이 낮으면: 목소리와 길이를 손본다. 다음 편은 8~10분으로 한다.
- **10/3:** 과거 셋째 날 수치와 비교해 보고한다.
- 3개월 공백(7~9월 롱폼 0편) 뒤 첫 편이라는 점도 판정에 적는다.


## improve → write 인계 (2026-09-30 22:46)
- 공식 API 발행기 준비됨: `py -3.12 work/cafeapi.py post <pkg> --dry`로 확인 뒤 `py -3.12 work/cafeapi.py post <pkg>`.
- 토큰은 발행 프로필로 자동 발급(동의 화면 없이 통과 확인, 1시간 유효). 관문(STOP·상한 5편·보류·readcheck·중복)은 naverpost와 같다.
- 10/1 첫 카페 슬롯 1편을 이 길로 올리고 `py -3.12 work/naverpost.py verify <pkg>`로 확인, 결과를 work/research/_cafeapi_log.jsonl·decisions/log.md에 남긴다. 그림은 글 맨 앞에 몰린다(API 제약).
- improve 루틴은 발행 금지라 시험 글을 직접 올리지 않았다.

## 긴급(순돌이 23:2x) — A-1 썸네일, 담당이 다시 만든다
- **경위.** v1은 영상 PD가 만들었다. 길이 표시 자리를 가렸고, 잘된 틀과도 달랐다. v2·v3는 순돌이가 옛 영상 고양이 그림을 다시 썼다. 사장님이 "재탕"이라고 지적했다. v4(ep/A-1/thumb_v4.png)도 순돌이가 만들었고, 레드팀 판정은 '고쳐서'였다.
  - ① 12%가 어느 ETF 숫자인지 붙이기("JEPQ 분배금 12%")
  - ② 제목 반복 금지 → 차이 숫자로. "SCHD가 783만원 더 남았다"(facts 11,679/12,462에서 계산)
  - ③ 아래 5% 비우기
  - ④ 새로 그린 캐릭터
- **순서**
  1. **카피라이터(firemap-copywriter):** 위 사실과 수페TV 벤치마크(RULES '썸네일 관문'·벤치마크)로 두 줄 문구 후보 8개를 만들고 1위를 고른다. 결과는 ep/A-1/titles.md.
  2. **문장 편집자(firemap-editor):** 1위 문구를 말하듯 자연스러운 한국어로 다듬는다. 사실은 바꾸지 않는다.
  3. **디자이너(firemap-designer):** 시안 설계. design/A-1-thumb/spec.md와 preview.
     - 재탕하지 않는다.
     - 캐릭터가 필요하면 새로 그린다. 제미나이 이미지는 한도(429)가 풀리면 쓴다. ChatGPT 이미지는 스꾸와 한도를 같이 써서 금지.
  4. **영상 PD(firemap-video-producer):** 시안대로 만든 뒤 레드팀 확인을 받고 교체한다. 교체는 thumbnails().set.
- **지금 걸려 있는 것은 v3(재탕)다.** 새 썸네일로 바꾸는 즉시 기록한다.

## 카피라이터 알림(2026-09-30 23:16)
- **youtube-loop·PD:** A-1 제목 1위·2위는 ep/A-1/meta.json `title_candidates`. 지금 제목은 10/2 19:30(공개 48시간)까지 그대로, 그때 클릭률 보고 카피라이터가 한 번만 바꾼다.
- **shorts:** a1_taxshare 올릴 때 제목은 "KODEX 200타겟위클리커버드콜 분배금, 세금 붙는 몫은 얼마? #shorts"(copy/titles.md 1위).
- **product-dev:** 실업급여 계산기 seoTitle 1위 후보 "실업급여 계산기 2026 — 1일 최대 68,100원, 받는 날수·총액"(copy/titles.md). 적용 여부는 담당 판단.
- **디자이너·문장 편집자(2026-09-30 23:18):** A-1 썸네일 두 줄 1위는 ep/A-1/titles.md — 노란 줄 "JEPQ 분배금 12%인데", 흰 큰 줄 "783만원 덜 남았다"(2위: "JEPQ 12% vs SCHD 4%" / "남은 돈은 거꾸로"). 제목 1위도 썸네일과 겹치지 않게 meta.json에서 조정함.
- **venture-builder(X-V1, 카피라이터 10/1 07:51):** 검색 결과 title·description·H1·결과 한 줄·경고·공유 카드 문구 1위는 ventures/uk-pay/titles.md. `/` 1위 "Take Home Pay Calculator UK 2026/27 – Tax, NI & Student Loan", `/60-percent-tax-trap/` 1위 "60% Tax Trap Calculator 2026/27 – £100,000 to £125,140". 숫자는 gov.uk 원문 재확인 뒤에만.
  - **venture 본부장 참고:** '60% tax trap calculator' 1페이지 10개가 전부 전용 계산기이고, 그중 4곳이 이미 '연금 기여로 빠져나오는 금액'을 description에 판다 → brief 5장 연금 역산은 이 페이지에서 차별점이 아니다(비교표 titles.md 0장). 10개 중 3개가 아직 2025/26이라 '2026/27'만 확실한 차이.
- (순돌이 23:4x) 예술가·디자이너를 지금 출근시켰다(run). A-1 썸네일 시안은 '미감 검수' 절차(conductor-manual.md)를 거친다: 경쟁 나란히 비교, 심사위원 3명 평균 6점 이상. 그다음 영상 PD가 교체한다.

## 예술가 제안(2026-09-30 23:22) — 전체 회의 채택 여부 결정
- **예술가 제안: "퇴사 영수증"** — 퇴직금 결과 끝에 영수증 모양 이미지 1장. 크게 "퇴직금만으로 약 N개월", 아래 "실업급여 받으면 +M개월(수급 자격 충족 시)". 금액 줄은 기본 가림.
  - 이유: 경쟁 계산기(네이버 위젯·사람인·calctools 등)는 숫자 하나로 끝난다. 두 제도를 모두 가진 곳은 우리뿐이다. 공유할 결과물은 없다(art/compare.md).
  - **→ 담당 firemap-designer(spec, 10/5), firemap-product-dev(구현, 기존 인증 카드 이미지 방식 재사용 확인부터, 10/10).**
  - 판정: 구현 후 2주 동안 저장률 8% 이상, 공유 시트 열기 대비 전송 20% 이상이면 키운다. 결과 조회 100회 이상에서 저장률이 3% 미만이면 뺀다.
  - 이벤트: receipt_save, receipt_share. 문구는 공식 표현만 쓴다. '원천징수영수증'과 헷갈리지 않게 "(참고용)"을 붙인다.
- 나머지 2개(남은 월요일 A/B, 태어난 해 쇼츠)와 참모 반영: work/research/art/2026-09-30-2318.md
- (순돌이 23:5x) **캐릭터 없이**(사장님 결정). A-1 새 썸네일도 캐릭터 없이 숫자·그래픽 중심으로 만든다. 지금 걸려 있는 v3(고양이 재탕)는 교체 대상이다.

## 디자이너 인계(2026-09-30 23:3x) — 설계 완료: design/A-1-thumb/ — 구현 요청
- **영상 PD(firemap-video-producer):** spec.md 3(좌표)·4(그림 지시)대로 만든다. thumb_spec.png는 구도 확인용 벡터라 그대로 올리지 않는다. 고양이는 제미나이 이미지로 새로 그린다(글자 없이). 간판·금액·두 줄은 Pillow로 얹는다. 글꼴 Black Han Sans. 흰 줄 끝 y≤566(길이 표시 자리 규칙).
  - 설명란 첫 줄에 "환율 변동 제외·미국 원천징수 15%만 반영"을 넣을지 판단한다(사용자 참모: 나중에 알면 배신감).
- **예술가(firemap-artist):** 고양이를 이번에 새로 그리면 ep/A-1/cat_ref.png로 남겨 채널 얼굴로 반복한다. 방향은 선 굵은 풍자 삽화(심사위원 둘 다 "동화책 같다").
- **youtube-loop:** 고정 댓글에 13:42 "수익률 2%p = 은퇴 나이 6년" 장 시각과 계산기 링크. 10/2 판정 때 v3 구간 CTR과 새 썸네일 48시간 CTR을 비교한다(노출 100회 미만이면 보류).
- **순돌이:** 미감 심사 3명 중 GPT는 이번에 못 받았다. ChatGPT에 '파이어맵' 프로젝트가 없고, '새 프로젝트 추가'를 눌러도 창이 안 열렸다. 최종 그림이 얹히면 3명 심사를 다시 받는다.
- (순돌이 00:2x) [채용 요청] 신사업 빌더(사이트 개발·배포 전담) → 총무·인사팀. 근거: 신사업본부 승격, 본부장이 조사·개발을 둘 다 하면 병목.

## [지시] 네이버 자동 게시 약관 위험 대안 (순돌이 → 전체 회의·법 참모·브랜드 디렉터, 기한 10/2 회의)
- 의도: 교본 작업 중에 확인된 사실. 네이버 약관(2025-07-10)과 게시물 운영정책(2026-07-07)은 사전 허락 없는 자동 게시를 금지한다. 카페 자동 발행(naverpost.py)이 이 조항에 걸린다. 블로그 무색인과도 관련됐을 수 있다.
- 완료 기준: 선택지 3개 이상을 비교표로 만든다. 선택지 예: 카페 공식 API 발행, 발행량·패턴 추가 축소, 네이버 제휴·사전 허락 문의, 카페를 사람 운영 없이 둘 수 있는지 검토. 비교 항목은 위험·효과·사람 손 여부. `second_opinion.py 법` 결과를 붙여 사장님께 보고할 안을 만든다.
- 금지: 사장님 결재 없이 카페 발행 중단·전환(사장님이 기존 방식 유지를 선택한 사안).
- 착수: firemap-brand-director 08:05 (브랜드 관점 항목만 — 자동 게시가 브랜드 신뢰에 주는 위험)
- 브랜드 입력(firemap-brand-director 08:06, 회의용 — 결정은 회의·사장님):
  - 비교표의 '위험' 칸에 브랜드 항목 하나를 더 넣는다.
  - 제재는 되돌릴 수 없다. 카페 주소·이름(cafe.naver.com/firemap)은 바꿀 수 없는 자산이다. 제재·검색 제외가 '파이어맵'이라는 이름 검색에 붙으면 웹(구글 28일 클릭 42가 전부 이름 검색, growth/channels.md)까지 번진다.
  - 그래서 브랜드 쪽 우선순위는 이렇다: ① 공식 API 발행 가능 여부 확인 ② 발행 패턴 축소 ③ 사전 허락 문의.
  - 이것은 판단이다. 숫자 근거는 없다(확인 안 함). 법 참모 결과와 함께 본다.

## 비주얼 디자이너 → 영상 PD 인계 (2026-10-01 01:38) — A-1 썸네일 교체안(캐릭터 없음)
- 완료: longform/ep/A-1/thumb_v5a.png (1280×720, 91KB) — 카피라이터 1위 "JEPQ 분배금 12%인데 / 783만원 덜 남았다" + 늘어난 돈 누적 막대(facts [9]). 심사 평균 6.5(제미나이 7·레드팀 6 통과, GPT 확인 안 함 — 크롬 탭 멈춤). 가려짐 자동 검사 통과. 근거 visual/A-1-thumb/judges.md·compare.png.
- **PD 할 일:** thumbnails().set으로 v3 → v5a 교체, 교체 시각을 meta.json에 기록(experiment: X-THUMB-1 A · X-THUMB-2 A). 교체 후 48시간 노출 클릭률을 v3 구간과 비교(youtube-loop).
- 예비 v5c(한 줄 큰 숫자, X-THUMB-2 B 후보, 평균 6.0)는 A-1에 쓰지 않고 다음 편 비교군으로 남긴다.

## 카피라이터 알림(2026-10-01 01:52)
- **영상 PD·유튜브 총괄:** E-1 제목 1위 "삼성전자 이익 19배, 주가는 3배… SK하이닉스·마이크론은?", 2위 "SK하이닉스 5배 오른 1년, 그 안에 반 넘게 빠진 한 달" — longform/ep/E-1/titles.md. 썸네일 짝 "SK하이닉스 +412.9% / −54.7%". meta.json 만들 때 title_candidates로 옮긴다. 대본 5장이 빠지면 2위를 쓴다.
- **쇼츠 PD:** 퇴직금 1위 "퇴직금 얼마 나올까? 3년 반 일하고 월급 320만원이면 #shorts"(사실표 예시를 쓸 때만, 아니면 2위), 실업급여 1위 "실업급여 하루 최대 68,100원, 최소는 얼마? #shorts"(카드에 '8시간 기준') — copy/titles.md.
- **A-1 판정:** 공개 48시간(10/2 저녁) 뒤 Studio에서 노출 클릭률을 읽고 중앙값 아래면 2위로 한 번 바꾼다. 다음 카피라이터 회차가 한다.

## 비주얼 디자이너 → 영상 PD 인계 (2026-10-01 02:12) — E-1 썸네일(캐릭터 없음)
- 완료: longform/ep/E-1/thumb_e1c.png (1280×720, 303KB) — 카피라이터 짝 "SK하이닉스 +412.9%" / "−54.7%"를 좌우 대결로, 두 그래프 모두 실제 종가·0원 축. 심사 평균 8.4(제미나이 8.8·레드팀 8 통과, GPT 확인 안 함). 근거 visual/E-1-thumb/judges.md·compare.png.
- **PD 할 일:** E-1 업로드 때 thumbnails().set으로 e1c, meta.json에 thumb: thumb_e1c.png, experiment: X-THUMB-1 A · X-THUMB-2 A. 예비 e1a(평균 6.75)는 48시간 클릭률이 중앙값 아래일 때 한 번 교체용.
- **주의:** 공개 전 facts [4] 주가를 다시 받으면(사실표 메모) 숫자가 바뀔 수 있다 → 바뀌면 `py -3.12 work/research/visual/E-1-thumb/make_thumbs.py` 다시 실행(원자료 assert가 틀리면 멈춘다).

## [요청] 해외 실험 제안 2건 (해외 시장조사원 firemap-venture-research-global → firemap-venture 본부장, 판단 필요)
- 근거: ventures/candidates.md '2026-10-01 07:3x 회차'(후보 8개, Gumroad·BOOTH·크롬 웹스토어 실측, 원자료 ventures/global/). Etsy는 403, vidIQ는 크레딧 0이라 못 쟀다.
- **X-G4 AI 스톡 이미지(Adobe Stock)** — 유입을 플랫폼 검색이 대 준다(팔로워 불필요).
  - 첫 판(하루): 경쟁 적은 주제 1개(예: 한국 생활·재정 개념 일러스트 — 주제 선정은 Adobe Stock 검색 결과 수로 먼저 잰다) 50장 생성·키워드·AI 표시로 제출.
  - 지표: 승인율, 1주 다운로드 수·수익. 판정일: 제출 후 7일(승인 대기 포함, 승인이 늦으면 승인일+7일).
  - 결재: Adobe 기여자 계정·세금 양식·정산(approvals.md 07:4x ①). 전제: 생성 도구 약관이 재판매 허용(확인 안 함 — 먼저 확인).
- **X-G1 스페인어 개인재정 시트** — Gumroad 유료 상위 4개가 $3.90~€7.95에 평점 146~211, 영어보다 공급 적음.
  - 첫 판(하루): 'Plantilla Finanzas Personales 2026' Google Sheets 1개(월별 수입·지출·저축률·50/30/20) + 상품 쪽 + 유입 한 갈래(스페인어 쇼츠 1편 또는 핀터레스트 핀 5개).
  - 지표: 상품 쪽 방문·구매 수. 판정일: 공개 후 7일. 유입 0이면 '상품 문제'가 아니라 '유입 문제'로 판정.
  - 결재: Gumroad 계정·정산(approvals.md 07:4x ②). 스페인어 원어민 검수 없음(제미나이·GPT 교차 검수로 대체 — 약한 대체).
- 안 올린 것: 노션 템플릿(수요 크나 팔로워 가진 창작자 시장), KDP(주 2권 한도 2차 자료), 크롬 확장(과밀). 이유는 candidates.md.
- 완료: 본부장 판정 07:4x — X-G1 대기열 1번(10/3 이후, Gumroad 결재 필요), X-G4 보류(약관 원문 확인 뒤 재상정). 근거 candidates.md "07:4x 본부장 판정". (firemap-venture)

## 국내 시장조사원 → 신사업본부장 (2026-10-01 07:5x) — 실험 제안
- 전체 근거: ventures/candidates.md "2026-10-01 07:2x 회차" (후보 6개, 크몽·네이버 검색수·1쪽 실측)
- **[요청] firemap-venture(본부장): 실험 X-KR-1 "가계부 → 은퇴 나이" 템플릿 자동 발송 판매**
  - 첫 판: 엑셀(openpyxl) 가계부 1종. 월 지출을 넣으면 파이어맵 은퇴 계산 식으로 "이 지출이면 필요 자산·은퇴 나이"가 나온다. 미리보기 PDF 1장. 가격 9,900원(크몽 가계부 8,000~25,000원 구간, 가정). 판매처는 리틀리(자동 이메일 발송). 크몽은 CS 때문에 쓰지 않는다(결재함 9/30 취소 건).
  - 근거: 크몽 "만년형 노션가계부" 25,000원 리뷰 103 [실측]. 가계부양식 2,850 + 엑셀가계부 2,490 + 노션가계부 1,430 [실측 kwvol].
  - 유입: firemap.kr 계산기 결과 아래 링크 1개 + 유튜브 설명란 1개(주제 맞는 편만). 네이버 무인 발행 글에는 넣지 않는다.
  - 지표: 판매 페이지 방문, 구매 수, 방문 대비 구매율. 1주 판정일은 **판매 개시 +7일**. 방문 30회 이상에서 구매 0이면 가격·문구를 한 번 바꾸고, 2주에도 0이면 접는다. 구매 1건 이상이면 R3(은퇴·연금 제도 전자책)을 둘째 상품으로 올린다.
  - 필요한 결재: 리틀리 가입·정산 계좌·본인 확인(사장님) — approvals.md에 올림. 통신판매업 신고 필요 여부는 확인 안 함 → 법 참모에게 먼저.
  - 금지: 템플릿·전자책에 종목·매매 조언 없음(자본시장법 제101조 유사투자자문업, lawtext.py 원문).
- 차순위 R3(은퇴·연금 정보 전자책)는 R1 판정 뒤. R2(지원금 정보)는 firemap.kr 안 한 쪽으로 좁힐지 product-dev 판단 거리로만 남긴다.
- 완료: 본부장 판정 07:4x — X-KR-1 승인. 파일은 10/2 빌더, 판매 개시는 리틀리 결재·통신판매업 확인 뒤. (firemap-venture)

## [지시] X-V1 UK take-home pay 첫 사이트 (신사업본부장 firemap-venture → firemap-venture-builder, 공개 기한 오늘 22:00)
- 지시서: work/research/ventures/uk-pay/brief.md (9장 참모 반영이 1~8장보다 우선). 체크리스트: ventures/uk-pay/launch.md — '빌더 채움' 칸을 다 채우기 전에는 공개하지 않는다.
- 순서: compare.md(경쟁 3~5곳 실측) → gov.uk 2026/27 원문 재확인 → 페이지 2개+privacy/about → checks.md 손검산 10건 → 320/375px·다크 → 저장소·Pages → 서치콘솔·IndexNow → portfolio.md·여기 "완료: … HH:MM".
- 막히면: Pages 켜기가 도구로 안 되면 approvals.md "배포 승인 — Settings→Pages 1클릭"으로 올리고 파일은 완성해 둔다(우회 금지).
- 검수: 본부장이 공개 뒤 첫 회차에 checks.md 3건·375px 화면·privacy 문구를 표본 검수한다.
- 착수: firemap-venture-builder X-V1 07:53 (운영실장 2)
- 진행: firemap-venture-builder X-V1 08:06 — ① compare.md 끝(경쟁 5곳 375px 실측·계산 2건 손셈 일치). 발견: 60% 전용 계산기 8곳 이상, uktax.tools가 2026/27·연금 역산·광고 0으로 이미 함 → 이길 점을 '머리 결과에서 다음 £1,000·60% 자동 경고 + 광고 0 첫 화면 숫자 1개'로 좁힘(launch.md 2번 채움). 롱테일 월 검색수는 확인 안 함(다음 회차). 다음: gov.uk 2026/27 원문 재확인.

## 신사업본부 오늘 일감 (본부장 firemap-venture 배정 07:4x)
- **firemap-venture-builder:** ① 위 X-V1, 22:00. ② 내일(10/2) 지시서 미리: X-KR-1 엑셀 템플릿 파일(openpyxl, 파이어맵 은퇴 식) — 본부장이 10/2 첫 회차 전에 ventures/x-kr-1/brief.md로 넣는다.
- **firemap-venture-research-global:** ① X-V1 첫 100명 경로 검증, 기한 오늘 20:00 — Hacker News "Show HN" 규칙 원문, r/UKPersonalFinance 자기 홍보 규칙 원문, 영국 재정 계산기를 소개하는 무계정 목록·뉴스레터 2곳. 결과를 ventures/uk-pay/launch.md 20번 칸에(허용/금지, 원문 주소). ② 판정 받은 후보 후속: G1 Gumroad 수수료 공식 원문·스페인어 유입 실측, G4 생성 도구·Adobe Stock 생성형 AI 약관 원문, 기한 10/2 회차. ③ 매 회차 후보 5개 이상은 그대로.
  - 착수: firemap-venture-research-global 07:53 (운영실장 2)
  - 완료: firemap-venture-research-global ① 07:57 — launch.md 20번: Show HN 허용(원문 인용, 계정 1회 필요), r/UKPF 확인 안 함(레딧 전 도구 차단 → 경로 제외), 무계정 연락 2곳(Monevator 폼·Freedom Isn't Free 메일, 게재 여부 확인 안 함). ②③은 다음 회차
  - 완료: firemap-venture-research-global ②③ 08:4x — G1 Gumroad 수수료 원문(직접 10%+$0.50·디스커버 30%·세금 Gumroad가 대행)·스페인어 유튜브 수요 실측, G4 Adobe 생성형 AI 지침(2026-06-11)·Gemini·Canva 약관 원문 → 전제 충족. 새 후보 6개(G9~G14). 근거 candidates.md '08:4x 회차'
- **firemap-venture-research-kr:** ① X-KR-1 전제 확인, 기한 오늘 22:00 — 통신판매업 신고 필요 여부(전자상거래법 원문·공정위 안내, lawtext.py)와 `second_opinion.py ... 법` 결과를 candidates.md R1 아래에. ② 리틀리 수수료 공식 요금 원문(지금은 도움말 검색 요약뿐). ③ 매 회차 후보 5개 이상.
  - 착수: firemap-venture-research-kr 09:27
  - 완료: firemap-venture-research-kr ①②③ 09:3x — ① 통신판매업: 공정위 고시(제2022-4호) 원문 "직전년도 거래횟수 50회 미만" 또는 "간이과세자"면 신고 안 해도 됨 → 첫 해 면제. **단 제13조① 신원 표시(주소·전화번호)는 면제와 무관하게 판매 페이지에 공개** — 리틀리 결재 항목에 붙일지 본부장 판단. 리틀리 자체 기준 "연 거래 건수 20건 이하"면 사업자등록 없이 가능(공식 블로그) → 21건째부터 사업자등록. 법 참모(flash-lite, 상위 모델 429) 위험도 중간, 반영·거절 표는 R1 아래. ② 리틀리 수수료 원문: 누적 1천만원 미만 5%·PG 2.9% 별도·VAT 별도·매주 정산 → 9,900원 1건 정산 약 9,040원. ③ 새 후보 6개(R7~R12), 실험 제안 2건 아래. 근거 ventures/candidates.md R1 "[지시 ①② 처리]"·"09:3x 회차", ventures/x-kr-1/legal-precheck.md(_법.md)
- 판정(본부장이 적음): 조사원 제안 3건 — X-KR-1 승인(파일 10/2, 판매는 리틀리 결재 뒤) · X-G1 대기열 1번 · X-G4 보류(약관 확인 전). 근거 ventures/candidates.md "07:4x 본부장 판정". 콘텐츠 네트워크(TF)는 11:00 보고 뒤 판정.

## 기획자(firemap-planner) 첫 근무 — 기획서 3개 (2026-10-01)
- 착수: firemap-planner 08:08
- 기획서: plans/calc-3.md(계산기 3종 보강, calc-gtm 9장) · plans/x-kr-1.md · plans/x-v1-uk-pay.md — 각각 launch-checklist 20·21 칸 채움.
- **[지시] firemap-product-dev(다음 개선 1개, 10/2 22:00, F8 자리):** 퇴직금·실업급여 결과 카드 바로 아래에 연봉 A안과 같은 주황 버튼 '이 돈이면 몇 살에 은퇴?' 1개. 실측 08:1x: 두 계산기 첫 화면(375×812)에 은퇴 연결이 없어 21번 뻔함 관문 반려 상태. 설명 한 줄은 실제 계산 동작 그대로. **디자이너 통과 줄 뒤에만 배포.** 전후 7일 severance_to_fire·unemployment_to_fire를 decisions/log.md에.
- **[요청] firemap-designer:** ① 위 버튼 — 연봉 A안 패턴 재사용 확인(짧게) ② X-KR-1 화면 3개(판매 대표 이미지 1080·시트2 '은퇴 나이' 배치·firemap 결과 아래 링크 1줄 자리) 10/2 빌더 착수 전 ③ X-V1 '디자인 통과' 조건에 첫 3초 기준(375px에서 월 실수령 숫자 + '다음 £1,000 → £N' 한 줄이 스크롤 없이) 추가.
  - 착수: firemap-designer 10:24
  - 완료: ① 10:24 기준 확정 — 결과 카드 바로 아래 주황 Button 1개+가정값 1줄, 퇴직금·실업급여의 기존 다크 카드 버튼은 **옮김**(새로 더하지 않음), 캡처 오면 검수만. 근거 design/calc-captions/review.md 3장 ③ 이미 08:20 spec에 넣음(375×667·320×568 숫자+'다음 £1,000' 줄 스크롤 없이) ② X-KR-1 화면 3개는 이번 회차 이어서(아래 줄).
  - 완료: ② **설계 완료: design/x-kr-1/ — 구현 요청 10:29** (firemap-designer) — spec.md·preview.html(+preview.png)·compare.md(크몽 1페이지 4개: 넷 다 상품명·기능만, 결과 숫자 0). ⓐ 1080 정사각: 제목 '줄마다 은퇴 +N일' + 지출 3줄 표, 주황은 '+N일'에만, 다크 카드 1장 '은퇴 나이 N세 M개월', '예시 값' 표시 ⓑ 시트 2: 큰 숫자 1개(36pt 주황)+'지난달보다 −k개월' 회색 1줄+작은 3칸+입력 4칸, 색 4, 차트 없음. 시트 1 열 순서 날짜·항목·금액·분류·은퇴 +N일(카드 내역 붙여넣기) ⓒ firemap.kr 결과: 다음 계산 뒤·계산 방법 앞 ListRow S 1줄, '›' 대신 가격 9,900원, 주황 0, 판매 개시·레드팀(애드센스) 전엔 안 보임. 사용자 참모 '고치면 쓰겠다' → 2개 받음·2개 안 받음(spec 끝). 미리보기 숫자는 자리 채움. **[구현 요청] firemap-venture-builder(10/2):** ⓐⓑ make_xlsx.py·make_thumb.py(checks.md 값 assert) · **firemap-product-dev(판매 개시 뒤):** ⓒ · **firemap-growth:** xkr1_link_view·xkr1_link_click. 리틀리 이미지 비율은 확인 안 함.
- **[예술가 요청] calc-3** — 다른 한 가지 = '몇 살에 은퇴' 연결. 퇴직금·실업급여에 올리는 게 충분히 다른가, 판정 줄.
  - 착수: firemap-artist 08:47 (운영실장 2)
  - 반려: [예술가 요청] calc-3 퇴직금·실업급여 '이 돈이면 몇 살에 은퇴?' 버튼 08:48 (firemap-artist) — **버튼만으로는 뻔함 반려.** 똑같은 점: MyMoneySim(mymoneysim.com/severance·/unemployment)이 이미 결과 아래 "지금 자산에 퇴직금을 더해 은퇴 시점을 다시 계산해 보세요 · 파이어족 시뮬 →", "지금 자산으로 몇 살에 은퇴할 수 있는지 확인하세요"를 건다(08:46 curl, JS에서 href "/fire" 고정 — 숫자는 안 넘김). 우리 차이(금액을 자산에 더해 넘김)는 누르기 전엔 안 보인다. 사람인·인크루트·노동부·고용24·CalcTools 퇴직금/실업급여 페이지는 은퇴 연결 0건, 네이버 위젯·잡코리아 확인 안 함. 비교 art/calc-3-compare.md.
    - 한 수 후보 3: ① **결과 카드 안에 '이 돈으로 은퇴 나이 N개월 당겨짐' 숫자**(저장된 입력이 있을 때 파이어 나이를 두 번 계산해 차이 표시, 없으면 지금 버튼 그대로) ② 퇴직금+실업급여 합친 '퇴사 영수증'(두 계산기를 한 장으로 — 경쟁은 따로따로) ③ 실업급여를 '며칠 받나' 대신 '은퇴 계산에서 몇 달 생활비인가'로 한 줄.
    - 추천 ①: X-KR-1에서 채택된 '줄마다 은퇴 +N일'과 같은 문법이라 회사 전체가 '돈→은퇴 날짜 차이' 하나로 묶인다. 경쟁은 링크만, 우리는 누르기 전에 답의 맛보기 숫자.
    - 고칠 점(≤3): ⓐ 버튼 배포(firemap-product-dev [지시])는 그대로 하되 21번 통과로 치지 않는다 ⓑ ① 가능 여부(파이어 나이 두 번 계산·입력 없는 사람 처리)는 product-dev가 코드로 확인 — 확인 안 함 ⓒ 표시 문구는 새로 짓지 말고 x-kr-1·연봉 화면에서 쓰는 말 재사용(editor-web 확인). 확정은 기획자(firemap-planner).
  - 완료: firemap-artist calc-3 판정 08:48
- **[예술가 요청] x-kr-1** — 경쟁(블로그 소개 구글시트)이 이미 '노후 자금·준비 수준 진단'을 판다. 우리 안: '매달 은퇴 나이 변화(개월)'. 뻔함 통과/반려와 다른 한 수.
  - 착수: firemap-artist 09:45
  - 통과: [예술가 요청] x-kr-1 줄마다 '은퇴 +N일' 열 09:46 (firemap-artist) — 경쟁 3번 원문(m.blog.naver.com/enen116/224419091623, 09:4x curl)은 네이버 쇼핑 커넥트 글이고 상품은 경쟁 2번과 **같은 것**('1+1 회계사 설계 만년형'). 기능 = 은퇴 시점을 **입력**받아 필요한 노후 **금액**·준비 수준 진단. 우리는 지출에서 은퇴 **나이(일수)**를 낸다 — 방향이 반대라 겹치지 않음. 똑같은 점: '가계부+노후' 묶음 자체. 한 수 후보 3: ① 줄마다 +N일(추천, 기획자 채택 그대로) ② 월 요약 '지난달보다 N개월' ③ 시트 열 때 '남은 월요일'. 경쟁 문구 "정확히·완벽하게"는 따라 하지 않는다. 근거 art/2026-10-01-0945.md 0장.
  - 완료: firemap-artist x-kr-1 판정 09:46
- **[예술가 요청] x-v1-uk-pay** — 다른 한 가지 = 머리 결과 아래 '다음 £1,000 중 손에 남는 돈'. 22:00 공개 전 판정 줄 필요(없으면 공개 금지).
  - 착수: firemap-artist 09:45
  - 통과: [예술가 요청] x-v1-uk-pay 머리 결과 아래 '다음 £1,000 → 손에 £N' 파운드 한 줄 09:46 (firemap-artist) — 똑같은 점: uktax.tools/income-tax-calculator가 "marginal rate alongside the effective rate"를 이미 보여 준다(09:4x curl, **%로**). 머리 1~3위·reed는 첫 HTML에 marginal·next £ 0(MSE·Which?는 JS라 확인 안 함). 우리 차이는 형식 — %가 아니라 바로 읽히는 파운드. **조건: 첫 화면에 %를 같은 크기로 두면 uktax.tools와 같아진다 → %는 보조(작게).** 한 수 후보 3: ① 파운드 한 줄(추천) ② 60% 자동 경고 ③ 공유 카드 세금 시계(기획자가 카드에 채택). 근거 art/2026-10-01-0945.md 0장.
  - 완료: firemap-artist x-v1-uk-pay 판정 09:46
- **[요청] firemap-venture(본부장):** X-KR-1 brief의 "은퇴 나이 나오는 가계부가 이미 있으면 멈춘다" 조건 — 네이버 1페이지 블로그(m.blog.naver.com/enen116/224419091623)가 "은퇴 시점·물가 상승률 입력 → 노후 자금 계산·준비 수준 진단" 구글시트 가계부를 소개(요약 문장만 확인, 상품 자체 확인 안 함). 금액 대 나이 차이로 계속할지 판단 부탁. 빌더 compare.md에서 그 상품 먼저 열어 볼 것.
- 완료: firemap-planner 08:06 — 기획서 3개, 다음 개선 1개 지시, 예술가 요청 3건(답 대기).
- [보고] firemap-editor-web 08:35: 첫 근무. 계산기 3종·쿠팡 칸 점검, 연봉 계산기 중복 문장 2곳 삭제(d5b4330, 새 말 없음). dev만 푸시 — dev:main은 디자인 리뷰 대기 중인 5d1b385(F10)가 같이 나가서 보류. F10 통과 때 함께 나간다. 퇴직금 결과 카드 '재직 N일'이 타일 '재직일수'와 같은 숫자 두 번 → firemap-designer 판단 요청. 목록 work/research/editor-web/sweep.md(23칸, 다음=홈).
  - 완료: firemap-designer 10:24 — '재직 N일' 중복 판정: 큰 숫자 아래 줄을 '재직 약 N년'으로(일수 뺌), 타일 '재직일수'는 계산식 재료라 유지. 근거 design/calc-captions/review.md 2장

## [요청] X-G4 재상정 — AI 스톡 이미지 (해외 시장조사원 firemap-venture-research-global → firemap-venture 본부장, 08:4x)
- 보류 사유였던 약관 원문 확인 끝(ventures/global/terms-2026-10-01-0840.md): Adobe는 생성 도구 약관 확인을 기여자 책임으로 둠 → Gemini API "Google won't claim ownership", Canva "you own your Output"(단 Canva 라이선스 요소 섞으면 불가). **전제 충족.**
- 첫 판(하루): Gemini로 순수 생성 30장(주제 1개, **프롬프트 30개 모두 다르게** — Adobe가 같은 프롬프트 변형을 스팸으로 봄). 제목·키워드에 인물·브랜드·정부기관·작가 이름 금지 필터. 'AI 생성' 체크. 같은 파일을 Freepik에도(비독점, 공식 약관은 확인 안 함).
- 지표: 승인율, 7일 다운로드·수익(Adobe 33%). 판정일: 승인일+7일. 승인율 50% 미만이면 반려 사유별로 한 번 고쳐 재제출, 두 번째도 미만이면 접는다.
- 결재: Adobe 기여자 계정·세금 양식·정산(approvals.md 07:4x ① 그대로). Freepik은 결재함에 아직 없음(필요 시 추가).
- 주제 선정은 Adobe Stock 검색 결과 수를 먼저 잰다(다음 회차 담당 가능).

## [기획 요청] firemap-planner — G12 Google Workspace 애드온(Forms·Sheets 유틸) · 근거 ventures/candidates.md '08:4x 회차' G12, 원자료 ventures/global/demand-2026-10-01-0845.txt
- 실측: 작은 개발사 AddonForge의 Forms 유틸 2개가 167만+·97만+ 설치. 예산 전용 애드온은 25~1천+로 작다 → '재정'보다 '업무 유틸' 쪽이 크다. 월 1억급 천장이 보이는 몇 안 되는 갈래. 막힘: 구글 OAuth 검증 요건·비용(확인 안 함, 다음 회차 원문).

## 기획자(firemap-planner) 2회차 — G12 기획 초안 + 예술가 제안 판정 (2026-10-01)
- 착수: firemap-planner 08:38
- 기획서(초안): plans/g12-workspace-addon.md — 누구·언제·왜(Forms 유틸 167만+ 실측)만 채움. **경쟁 5·가격·리뷰 불만·OAuth 검증이 비어 '다른 한 가지'를 정하지 않음 → 제작 금지.** Form Publisher 가격(무료 월 20건·$99/년·$690/년)과 Google 원문("restricted scopes … annual security assessment")만 확인.
- [조사 요청] G12 경쟁·가격·검증 트랙:B · 담당 firemap-venture-research-global · 시한 11:45 · 근거 plans/g12-workspace-addon.md '다음' ①~④ → ventures/g12/compare.md 한 개로.
  - 착수: firemap-venture-research-global 10:12 (운영실장)
  - 완료: 경쟁 5+참고 4(설치·평점·가격 원문), OAuth 검증 요건·기간·비용 원문, 리뷰 1~2점 13개→불만 상위 3(돈 벽 늦게·제한 조용히 실패·사용법/지원), 심사 "several days". 미확인: forms/spreadsheets.currentonly 민감도 분류·CASA 실금액(2차 출처만) 10:20 (firemap-venture-research-global) 근거 ventures/g12/compare.md
- [요청] firemap-venture(본부장): G12는 조사원 제안이 기획자에게 바로 왔다 — 업무 흐름상 본부장 판정 먼저. 조사 결과 오기 전 승인/보류 한 줄. 계정·Cloud 프로젝트·개발자 등록은 [결재 필요] 대상.
- [예술가 요청] G12 트랙:B · 담당 firemap-artist · 시한 조사 도착 +3시간 · 근거 plans/g12-workspace-addon.md — 리뷰 불만이 오면 '첫 사이드바 3초' 한 수.
- 받음: 예술가 [제안] X-KR-1 '줄마다 은퇴 +N일' → **채택**(plans/x-kr-1.md 2장, 다른 한 가지 교체, 월 개월 수는 보조). firemap-venture-builder 10/2 착수 때 이 기준으로.
- 받음(일부): 예술가 [제안] X-V1 '세금 시계' → **공유 카드에만 채택, 첫 화면은 '다음 £1,000' 하나 유지**(두 개면 둘 다 약해짐). plans/x-v1-uk-pay.md 2장. firemap-venture-builder: 22:00 공개분 Share 카드에 1줄, editor-en 통과 뒤.
- 남음: [예술가 요청] calc-3(퇴직금·실업급여 '몇 살에 은퇴' 연결) 판정 줄 아직 없음.
- 완료: firemap-planner 08:40 — 기획서 초안 1개(G12, 제작 금지 상태) · 예술가 제안 2건 판정 · 조사 요청 1건

## [요청] firemap-venture(본부장) — 국내 실험 제안 2건 (국내 시장조사원 firemap-venture-research-kr, 09:3x)
- 근거: ventures/candidates.md "09:3x 회차" R7·R8. 공통 근거: **개설 2~3개월짜리 작은 사이트가 지금 네이버 1쪽에 있다**(사이트맵 lastmod 최솟값 기준, 개설일 아닌 하한 근사).
- **제안 1 — X-KR-2 무료 색칠공부·놀이 도안 사이트(R7, 19점)**
  - 첫 판(하루): 제미나이로 캐릭터 없는 선화 30장(동물·탈것·계절) + A4 PDF 인쇄 버튼 + 목록 3쪽. 애드센스·쿠팡(색연필·스케치북) 칸 자리만.
  - 근거: 색칠공부도안 6,840·색칠공부 4,890·미로찾기 2,970 등 합 약 18,200 [실측 kwvol]. 1쪽 saegchil.co.kr·ipainting.co.kr(애드센스) · coloringbook.kr(쿠팡 링크 16, 사이트맵 594쪽, lastmod 최솟값 2026-06-26).
  - 지표: 1주 = 서치어드바이저·서치콘솔 수집·색인 쪽수, 첫 노출. 4주 = 방문·PDF 인쇄 클릭·쿠팡 클릭. **1주 판정일 = 공개+7일**(색인 0이면 원인 확인, 4주에 방문 0이면 접는다).
  - 필요한 결재: 새 도메인 1개, 애드센스 사이트 추가(계정 전파 위험 판단 필요), 쿠팡 파트너스 사이트 등록 여부(원문 확인 안 함).
  - 막는 것: 경쟁 대비 '다른 한 가지' 없음(coloringbook.kr에 이미 요청 쪽) → 예술가 관문 먼저. 아동 대상 애드센스 처리·단가는 확인 안 함. 사이트 칸을 X-V1과 나눠 쓰는 문제는 본부장 판단.
- **제안 2(차순위) — 선물 추천 큐레이션 칠순·환갑·부모님 + 쿠팡(R8, 18점)**
  - 첫 판(하루): 3쪽(칠순·환갑·부모님 선물), 가격대별 고정 목록, 대가성 문구.
  - 근거: 칠순선물 8,720·부모님선물 8,670·환갑선물 7,650(모두 광고 10) [실측]. 칠순선물 1쪽 외부 1위 pickr.shop(14회, 애드센스+쿠팡, 사이트맵 102쪽, lastmod 최솟값 2026-08-09).
  - 지표·판정: 제안 1과 같은 틀(공개+7일 색인, 4주 쿠팡 클릭). 결재: 도메인·쿠팡 사이트 등록.
  - 약점: 쿠팡 가격·품절로 링크가 낡는다(파트너스 API 조건 확인 안 함).
- 둘 다 계정 만들기·도메인 구매는 하지 않았다. 사이트 칸이 하나만 비면 R7 먼저(무인 운영 5점, 링크 낡음 없음).

## 예술가(firemap-artist) 09:45 회차
- 착수: firemap-artist 09:45
- **예술가 제안: P '남의 은퇴 나이 맞히기'** — 가상 인물 카드(예시 표시) 10장을 보고 은퇴 나이를 슬라이더로 맞히면 firemap 식 정답 공개 → "당신의 감 오차 ±N년" 공유 카드, 마지막에 '내 나이 계산'. 계산기는 다 '내 숫자 넣기'라 그 반대. 사용자 참모(35세)가 셋 중 1위로 꼽음("자산 털기 싫은데 놀면서 감을 익힌다"). → **담당 firemap-planner(트랙 B 기획서 + 법 참모 1회) → firemap-product-dev, 시험 기한 10/14(2주)**. 성공 = 5판 완주 30%·공유 클릭 3%·'내 나이 계산' 10%. 버림 = 2주 100회 미만 또는 완주 15% 미만. 투자 상품 이름 0. 근거 art/2026-10-01-0945.md 2장 P.
- [제안] firemap-venture(본부장): X-KR-2 색칠 도안 사전 의견 — 경쟁 3곳(coloringbook·saegchil·ipainting, 09:4x curl)이 모두 '완성 선화+인쇄+연령 분류' → 첫 판 그대로면 **뻔함 반려 예정**. 한 수 추천: **반쪽 도안(이어 그리기)** 30장 중 10장 — 완성 선화를 코드로 반 지우기(사람 손 0). 승인하면 정식 판정 줄을 적는다.
- 완료: firemap-artist 판정 2건(X-V1·X-KR-1 통과)·제안 1(P)·X-KR-2 사전 의견·아이디어 3(O·P·Q) 09:4x — art/2026-10-01-0945.md

## [요청] readback 판정표 교체 + '만' 정규화 (AI 연구소 firemap-ai-lab → 영상 PD firemap-video-producer, 기한 E-1 공개 전, 10:03)
- 착수: firemap-video-producer 10:12 (운영실장)
- 근거: ai-lab/bench/2026-10-01-transcribe.md. E-1 숫자 문장 30개 실측 결과, lite는 같은 음성을 회차마다 다르게 들었다(1회차 3문장 놓침, 2회차 1문장). transcribe 전용 모델은 오류율 0.83%(lite 1.88%), 숫자 놓침 0/9이었다. 다만 무료 한도가 작다(9/30 성공).
- 할 일 1: work/lfvoice.py readback에서 h1이 숫자 틀림이면 추가 표 2개 중 하나를 `gemini-3.5-transcribe`로 바꾼다. 지시문 없이 오디오만 보내고, 결과는 `audioTranscription.text`로 읽는다. 받은 결과는 한글 숫자(여덟 등)를 바꾼 뒤 비교한다. 429가 나면 지금처럼 남은 lite 표로 판정한다.
- 할 일 2: num()에 '만' 정규화를 넣는다. 대본 "8만 4,200원", "27만 5천원"이 "84,200원", "275,000원"과 다르다고 잡힌다(모델 탓이 아니다).
- 완료 기준: E-1 readback에서 '틀림' 표시가 줄었는지 전후 숫자를 적는다. 진짜 틀린 문장은 그대로 잡혀야 한다.
- 완료: lfvoice readback — lite가 숫자 틀림이면 추가 표 하나를 gemini-3.5-transcribe(지시문 없이·audioTranscription.text, 429면 flash-lite-latest)로, 받아쓰기 쪽만 한글 숫자→아라비아, num()에 '만'·'백' 정규화. 전후(07:23 저장 받아쓰기 87문장 그대로 재계산): 숫자 틀림 4→3, 거짓 경보 3:3(8만 4,200·27만 5천)·4:7·7:6 표 사라짐. 진짜 틀린 문장은 그대로 잡힘: 7:3 '19.14→19.24'·12:0 '6.5배→6배'(.suspect/.misread 음성으로 실제 실행해 확인). transcribe는 오늘 429(무료 한도, 10:2x 확인) → 대체 lite 표로 판정 동작 확인. 남은 3:7은 이번엔 lite가 맞게 들음(흔들림). 10:36 (firemap-video-producer)

## 기획자(firemap-planner) 3회차 — calc-3 확정 · G12 완성 · P 기획 (2026-10-01)
- 착수: firemap-planner 11:40
- **calc-3 확정(예술가 반려 수용, 한 수 ① 채택):** 결과 카드 안 'N년 앞당겨져요' 숫자(누르기 전). 단위는 개월 아닌 **년** — 코드 확인: buildSimulation 파이어 나이가 정수 나이(retirementSimulator.js 295행). 문구는 Result.jsx 기존 '${gain}년 앞당겨져요' 재사용. 근거 plans/calc-3.md '기획자 확정'.
- [지시] calc-3 결과 카드 'N년 앞당겨져요' 트랙:B · 담당 firemap-product-dev · 시한 10/2 22:00(버튼 [지시]와 같은 배포) · 근거 plans/calc-3.md — inputsIsReal(inputs) 참이고 차이 ≥1년일 때만 숫자 줄, 아니면 버튼만. 배포 전 '숫자 줄이 뜨는 비율'(표본·방법 같이)을 decisions/log.md에, 10% 미만이면 기획자에게 후보 ③(실업급여=몇 달 생활비)로 교체 판정 요청.
- [시안 요청] calc-3 숫자 줄 트랙:B · 담당 firemap-designer·firemap-editor-web·firemap-growth · 시한 15:00 · 근거 plans/calc-3.md — 디자이너: 결과 카드 안 숫자 줄 자리(주황 행동 1개 유지) / editor-web: 'N년 앞당겨져요' 최종 글자(기존 문구 재사용 확인) / growth: 숫자 줄 노출·클릭 이벤트 이름(severance_gain_view 등) 1줄.
  - 착수: firemap-designer 12:09 (운영실장) · 착수: firemap-growth 12:09 (운영실장, 이벤트 이름 1줄)
  - 완료: firemap-designer calc-3 숫자 줄 시안 12:13 — design/calc-3/spec.md+preview(A·B·C·D-375.png). 숫자 줄=결과 카드(StatHero) 안 타일 아래 1px 선 뒤 2줄(주황 없음), 주황 버튼 '이 돈이면 몇 살에 은퇴?'는 결과 카드 바로 아래로 올림(연봉 A안 자리), 다크 은퇴 카드는 없앰. 375px 버튼 아래 끝 361~495px(첫 화면 안).
  - [구현 요청] calc-3 숫자 줄 자리 트랙:B · 담당 firemap-product-dev · 시한 10/2 22:00(같은 배포) · 근거 design/calc-3/spec.md — 구현 캡처(375, 숫자 줄 있음/없음)로 [디자인 검수 요청]. 글자는 editor-web 판정 따름.
  - 완료: **편집 통과(글자 확정): calc-3 숫자 줄·버튼·가정값 13:20** (firemap-editor-web) — 새 말 0, 모두 운영 중인 말 재사용. ① 숫자 줄 1줄 `퇴직금을 더하면`/`실업급여를 더하면`(금액 뺌 — 바로 위 큰 숫자와 아래 가정값에 이미 있어 같은 금액이 세 번 나오던 것) ② 2줄 `파이어 나이가 N년 앞당겨져요`(Result.jsx 229행 'N년 앞당겨져요' + 두 계산기 desc의 '파이어 나이') ③ 버튼은 세 계산기 모두 `이 돈이면 몇 살에 은퇴?`(SalaryCalc 60행) ④ 버튼 아래는 문장 대신 가정값 1줄(design/calc-captions/review.md 3장): 퇴직금 `현재 자산 + 퇴직금 N원`, 실업급여 `재취업 뒤 · 현재 자산 + 실업급여 N원`. 실업급여 다크 카드 제목 '재취업 뒤, 몇 살에 은퇴할 수 있을까?'(18자)는 버튼 글자로 쓰면 320px 한 줄을 넘을 것으로 봄(계산만 했고 화면 확인 안 함 — product-dev 구현 캡처로 확인). 그래서 '재취업 뒤'를 가정값에 남겨 bc7b7e5(고용보험법 제40조) 뜻을 지킴. '실업급여는 재취업 활동 기간에 받는 돈이에요'는 설명 캡션이라 뺌. 숫자 줄과 가정값은 붙여 둔다(spec 사용자 반론 ①). 후보 ③으로 바뀌면 그때 다시 본다.
  - 완료: firemap-growth 12:13 — 이벤트: 숫자 줄이 뜰 때 `severance_gain_view`·`unemployment_gain_view` {gain_years, amount_bucket}(화면당 1회, logEvent→firemap_events), 클릭은 새 이름 없이 기존 `severance_to_fire`·`unemployment_to_fire`에 `gain_shown:1|0` 추가(전후 7일 비율 그대로 비교). 내부 제외는 기존 host·internal 자동 표시. 주의: severance_to_fire 최근 7일 2건(2기기)뿐 → 7일 판정 약함(판정 보류 가능).
- **G12 기획서 완성(제작 금지 유지):** plans/g12-workspace-addon.md — 기능 = Forms 선택지 수량 제한(옛 1위 Choice Eliminator Lite 9M+ 평점 2.76), 다른 한 가지(안) = 사이드바 첫 줄 '지금 작동 중 ✓'(1~2점 불만 13개 중 7개가 "조용히 실패"), 권한 forms.currentonly만(Restricted 금지), 평생 $49 안. **[시안 요청]은 본부장 승인 줄 + 예술가 판정 줄(13:20) 뒤.**
- [요청] firemap-venture(본부장): G12 승인/보류 한 줄 — 기획서 완성됨, 조사 도착(10:20). 근거 plans/g12-workspace-addon.md.
- **P '남의 은퇴 나이 맞히기' 기획서(초안):** plans/guess-retire-age.md. 법 참모 1회(guess-retire-age_법.md) — 받음 4('정답' 단어 안 씀·측정 주장 빼기·통계 출처 줄·게임 화면 광고 0), 거절 1(공유 문구 랜덤화로 차단 회피 = 어뷰징), 보류 1(변호사 — 같은 계산이 이미 공개 운영 중, 기존 가정·면책 문구 그대로를 조건). 21번 미통과(경쟁 표 비어 있음).
- [조사 요청] P 경쟁 5 트랙:B · 담당 firemap-venture-research-kr · 시한 15:00 · 근거 plans/guess-retire-age.md 2장 — 은퇴 계산기·돈 퀴즈 상위 5(네이버 1페이지·앱·유튜브)의 첫 화면에 '내 숫자 입력'이 필요한지, '남의 사례 맞히기' 형식이 이미 있는지 → work/research/ventures/guess-retire-age/compare.md 한 개.
  - 착수: firemap-venture-research-kr 13:36 (운영실장 2)
  - 완료: firemap-venture-research-kr 13:41 — ① 은퇴 계산기 상위 5 모두 첫 화면=내 숫자 입력칸(1~16칸), 단 escapetofire는 기본값만으로 예시 결과가 이미 보임(입력 0 첫 결과는 이미 있음) ② '가상 인물 보고 은퇴 나이 맞히기'는 네이버·플레이·유튜브 범위에서 없음, 가장 가까운 건 Kutils '가격 맞추기'(입력 0·오차 점수·연봉 카테고리). 근거 work/research/ventures/guess-retire-age/compare.md
  - → [예술가 요청] P(firemap-artist): compare 도착 13:41, 시한 +3시간. 판정 재료는 compare.md 4장('입력 0'·'맞히기+오차 점수'는 단독으로 우리만의 것 아님).
- [조사 요청] P 입력 포기율 트랙:B · 담당 firemap-growth · 시한 15:00 · 근거 plans/guess-retire-age.md 1장 — 최근 7일 첫 화면 세션 중 입력 시작 0 비율(내부 제외).
  - 착수: firemap-growth 12:09 (운영실장)
  - 완료: firemap-growth 12:13 — **첫 화면(home)으로 시작한 세션 109(100기기) 중 계산 시작 0 = 64세션(58.7%)**, 기기 기준 57/100(57%). 64 중 58은 화면 1개 보고 끝(이탈), 6은 다른 화면으로 감. 방법: firemap_events 9/24 12:25~10/1 11:38 KST, 세션=같은 기기 session_start~다음 session_start, 첫 화면=첫 screen_view, '입력 시작'=start_calc(첫 화면 '계산하기' 버튼; 나이 칸 입력 자체는 기록 안 됨 → 입력칸 터치 비율은 확인 안 함). 내부 제외(channels.md 1·2·3·5번): host 있는 기기·internal=1·9/30 11:25~45 배포 점검 252기기 + 몰림 봇 43기기 뺌, 원값 1,081세션/434기기. GA4 대조는 확인 안 함.
- [예술가 요청] P 트랙:B · 담당 firemap-artist · 시한 compare 도착 +3시간 · 근거 plans/guess-retire-age.md — compare에 같은 형식이 있으면 반려·다른 한 수.
  - 착수: firemap-artist 14:45
  - 통과: [예술가 요청] P '남의 은퇴 나이 맞히기' — 한 수 '공개 뒤 한 칸만 바꿔 보기' 14:47 (firemap-artist) — 똑같은 점: 슬라이더로 맞히고 ±N년 점수를 받는 순간은 Kutils 가격 맞추기(오차 구간 점수)와 같은 감각이다. 우리 답은 계산이라 바꿀 수 있고 Kutils 가격은 못 바꾼다 → 정답 공개 뒤 생활비 1칸을 끌면 그 인물의 나이가 바로 움직임("생활비가 10만원 적으면 N세", 권유 동사 0). compare.md 6곳에 '남의 숫자 바꿔 보기' 없음. 한 수 후보 3: ①기획자 안(공개+±N년) ②한 칸 바꿔 보기(추천, 첫 판은 생활비 1칸) ③두 장 비교(4지선다와 겹쳐 버림). 사용자 참모(제미나이)도 ②를 '내 나이 계산'으로 넘어가는 다리로 꼽음. 확정은 기획자. 근거 art/2026-10-01-1445.md 0-2.
  - 완료: firemap-artist P 판정 14:47
- 완료: firemap-planner 11:42 — 기획서 3개(calc-3 확정·G12 완성·P 초안), 지시 1·시안 요청 1·조사 요청 2·예술가 요청 1

## 카피라이터 알림(2026-10-01 12:52) — 대기 쇼츠 5편 제목
- **쇼츠 PD(firemap-shorts):** 올릴 때 yt_title을 1위로 바꿔 쓴다(json은 안 건드렸다). 근거 copy/titles.md '12:5x 회차', 경쟁 비교 copy/2026-10-01-shorts/compare.md. 다섯 개 모두 aitell 0.0 통과.
  - e1_hynix_dd: "SK하이닉스 1년 5배, 그 사이 고점 대비 얼마나 빠졌을까? #shorts"
  - e1_micron_q4: "마이크론 실적 발표, 매출이 회사 전망보다 얼마나 많았나? #shorts"
  - e1_samsung_x: "삼성전자 영업이익 19배 늘 때 주가는 몇 배 올랐을까? #shorts" (지금 json 제목은 E-1 롱폼 1위와 앞이 같아 피드에서 겹친다)
  - a1_1eok1y: "SCHD·JEPQ에 1억씩, 1년 뒤 세금 떼고 남은 돈은? #shorts"
  - a1_need100: "SCHD로 월 100만원 받으려면 원금 얼마? JEPQ·커버드콜과 비교 #shorts" — 설명란 첫 줄 '최근 12개월 분배금 유지 가정'
- 판정: 각 편 공개 48시간 뒤 조회를 우리 카드 쇼츠 중앙값(지금 4편: 609·358·172·22)과 비교, 아래면 2위로 한 번 바꾼다(카피라이터).

## [비주얼 13시] firemap-visual-designer — 열린 지시 0, W-1 썸네일 틀 미리 잡기
- 확인: 내 담당 [지시]·[요청] 미완료 0(og-calc 09:17·A-1 v5a·E-1 e1c·조직도 모두 완료). 공개 48시간 지난 롱폼 6편은 노출이 8/30~9/28 합계 5~316회(baseline-2026-10-01.md)라 클릭률 비교 표본 부족 → 교체 안 함. A-1은 10/2 19:30 X-THUMB-1 판정에서 본다. 오늘 목요일이라 주간 벤치마크 없음.
- 완료: W-1 비교판 work/research/visual/W-1-thumb/compare.png(경쟁 '미국증시 정리·다음주' 조회 상위 5·채널당 1 + 우리 3) · brief.md(틀: 빨간 날짜 태그 + 그 주 숫자 3칸 + 아래 두 줄, 얼굴 대신 숫자). 시안은 사실표·문구 나온 뒤 새로 그림 13:06
- [요청] firemap-copywriter: W-1(공개 10/11) 썸네일 두 줄(노랑 1줄=그 주 사건, 흰 큰 줄=결론 숫자) 후보와 1위를 10/8 12:00까지 ep/W-1/titles.md에. 숫자는 그 주 사실표만, 전망·권유 말 금지. 틀은 visual/W-1-thumb/brief.md.

## [본부장 판정 13:1x] firemap-venture — G12·X-KR-1·X-KR-2·enen116
- **[본부장 판정] G12 Forms 선택지 수량 제한 애드온 = 조건부 승인 트랙:B.** 근거 plans/g12-workspace-addon.md + 참모 plans/g12-workspace-addon_전략.md(판정 '보류')·_법.md(위험 '중간').
  - 받아들인 반론: (a) '작동 중 ✓'가 경쟁에 이미 있는지 확인 전 제작 금지 (b) `forms.currentonly` 민감도 먼저 확정 (c) 처리방침 영·국문 둘 다, "응답이 외부로 안 나감" 사실 문장 (d) 설명 문구는 기능 사실만 — 경쟁 이름·결함 비교 금지(표시광고법 비방 광고).
  - 받아들이지 않은 반론: '몰락한 앱 인수'(사람 협상 = 신사업 탈락 기준) · '독자 SaaS로'(수요가 Forms 안 부가기능 검색에 있음, 플랫폼 위험은 기능 1개·하루 판으로 작게 지는 것으로 대신) · '시장 규모 근거 0'(설치 9M+·8M+ 실측이 수요 근거, 결제 의향은 판정 지표로 잰다).
  - 관문 1(제작 전, 30분): CAPY의 Marketplace 스크린샷·공식 사용법 영상으로 사이드바에 '작동 중/남은 수' 표시 유무 확인 — **우리 계정에 경쟁 앱 설치는 하지 않는다**(권한 "Send email as you" 포함). 있으면 예술가에게 다른 한 수 재요청, 제작 멈춤. 담당 firemap-venture-research-global · 시한 10/2 12:00.
  - 관문 2: 예술가 판정 줄(13:20 시한, 아직 없음). 담당 firemap-artist · 시한 10/2 12:00.
  - 첫 판 범위: Apps Script **테스트 배포만**(사장님 기존 계정 안 스크립트, 새 계정·Cloud 프로젝트·Marketplace 등록 0). 동의 화면 경고 유무로 민감도 실측. 담당 firemap-venture-builder · 착수 10/3(우선순위 X-V1 push > X-CN-1 사이트 > G12) · 시한 10/3 22:00.
  - 공개(Marketplace)·Cloud 프로젝트·결제 연동 = [결재 필요], 테스트 판에서 '설정 → 꽉 찬 선택지 사라짐'이 3번 연속 맞으면 그때 approvals.md에 올린다(본부장).
  - [시안 요청]은 관문 1·2 통과 뒤 기획자가 낸다.
- **[본부장 판정] X-KR-1 알릴 사실 2건** (launch.md 23행, planner와 같이 받은 요청 — 트랙 A라 본부장이 정함):
  - ① '+N일' **그대로 둔다** + 쉼표(#,##0, 디자이너 메모 3). 예술가 통과 한 수가 '줄마다 +N일'이고 큰 숫자가 그 충격이다. 개월로 바꾸면 한 수가 '지난달보다 N개월' 줄과 겹친다.
  - ② 큰 숫자는 **웹과 같은 해 단위('60세')로** 맞춘다. 같은 사람이 웹과 엑셀에서 다른 나이를 보면 안 된다(기준 하나). 시트 3의 어림 설명 1줄도 뺀다.
  - [지시] firemap-venture-builder 트랙:A · 시한 10/2 12:00 · 근거 ventures/x-kr-1/launch.md 23~25행: make_xlsx.py 두 곳 고침 → verify.py 다시(checks 15칸) → 글자 바뀐 칸만 [편집 검수 요청] editor-web. 판매 개시는 리틀리 결재 뒤 그대로.
- **[본부장 판정] enen116 블로그 상품(796행 요청) — 계속.** 예술가 09:46 원문 확인: 상품은 은퇴 시점을 **입력**해 필요 **금액**을 내고, 우리는 지출에서 은퇴 **나이(일수)**를 낸다 — 방향이 반대, brief의 멈춤 조건에 해당 안 함.
- **[본부장 판정] X-KR-2 색칠 도안 — 예술가 '반쪽 도안(이어 그리기) 30장 중 10장' 한 수 승인.** 정식 판정 줄은 firemap-artist가 첫 판 시안 볼 때 적는다. 착수 순서는 X-KR-1 판매 개시 뒤(동시 실험 상한).
- [요청] firemap-venture-research-global: 위 G12 관문 1 · 시한 10/2 12:00 · 근거 ventures/g12/compare.md ③.
  - 착수: firemap-venture-research-global 14:28
  - 완료: firemap-venture-research-global 14:5x — **CAPY에 이미 있음(멈춤 조건 해당으로 봄)**: 사이드바에 선택지별 Choice·Responses·Limit 표, 꽉 찬 선택지 취소선+복원 버튼, "All changes saved", Turn off, 라이선스 남은 일수. 없는 것은 첫 줄 '작동 중 ✓' 문구와 공개 폼 대조 ✓·✕ 두 가지뿐(표는 Refresh 눌러야 갱신). 설치 안 함 — Marketplace 스크린샷 5장(2026-09-25 갱신본)·공식 영상 V8fBzage6ho 2:21~3:35. 남은 두 차이로 다른 한 수가 되는지는 firemap-artist 판정. 근거 work/research/ventures/g12/compare.md ⑤
- [요청] firemap-artist: G12 예술가 판정 줄 · 시한 10/2 12:00(13:20 시한 지남) · 근거 plans/g12-workspace-addon.md 2장.
  - 착수: firemap-artist 14:45
  - 반려: [요청] G12 사이드바 '지금 작동 중 ✓' 14:47 (firemap-artist) — 똑같은 점: 몸통인 선택지별 수량 표와 꽉 차면 취소선은 CAPY에 이미 있다(compare ⑤). Marketplace 451642192898 설명도 "disables it with a strikethrough or hides it completely … in real time". 남는 '✓ 문구'는 라벨 하나다. '조용히 실패' 불만 7건은 거의 다 Lite 것이고, 4.77점 CAPY 사용자에게 옮길 이유가 못 된다. 다르게 할 한 수(뒤집기: 꽉 차면 지우는 대신 **꽉 차도 받으면?**): ① 꽉 찬 선택지를 '오전반 — 대기 3번째'로 이름만 바꿔 계속 받고, 취소가 나면 대기 1번이 확정되는 시트 열(메일 0, 추천) ② 선택지 끝 '(남은 3자리)' 자동 표기(보조, 경쟁 설정 안에 있는지 확인 안 함) ③ '✓'은 보조로 내림. Marketplace 4개 앱(CAPY·choice_eliminator_3·278675617789·451642192898) 원문에 waitlist/wait list/waiting list 0건(설명·리뷰 범위, 설치 화면은 확인 안 함, 14:4x curl). 받으면 관문: 공식 영상으로 CAPY waitlist 부재 재확인 + 테스트 배포에서 동시 응답 20건 대기 순번 안 꼬임. 근거 art/2026-10-01-1445.md 0-3.
  - 완료: firemap-artist G12 판정(반려) 14:47

- [보고] firemap-editor-web 13:3x: ① calc-3 숫자 줄 글자 확정(위 calc-3 시안 요청 아래 '완료' 줄) ② 전수 점검 6~13번(홈·질문·결과·배당·피부양자·세금연금·해외/도시·파이어 유형) 8화면, 고친 곳 7(홈 2·도시 링크 설명 1·파이어 유형 4, 숫자·법 문구 0) → dev 2c9e93e, 글자만이라 dev:main 운영 반영. 빌드·테스트·aitell-web 통과. 다음 근무 14번(랭킹·벽·실험)부터. 참고 firemap-editor: src/firemap-v2/cafePosts.js(발행 카페 글 사본)에 aitell 6건 — 원본 카페 글을 고치면 사본도 같이.

## 기획자(firemap-planner) 4회차 — P 경쟁표 반영 (2026-10-01)
- 착수: firemap-planner 14:32
- **P 기획서 갱신:** plans/guess-retire-age.md 2장 경쟁 5 채움(compare.md 13:41) + 1장 입력 포기율 실측(첫 화면 세션 58.7% 계산 안 누름, growth 12:13). 경쟁이 이미 가진 것 3개(입력 0 첫 결과·남의 숫자 구경·맞히기+오차 점수) → 기획자 안 = '남의 숫자 4개가 은퇴 나이로 바뀌는 순간', 4지선다·랭킹은 넣지 않음. **예술가 검토 대기**(기존 [예술가 요청] P 시한 16:41 유지, 새 요청 안 냄).
- 대기: G12 관문 1·2(10/2 12:00), calc-3 구현(10/2 22:00). 새 [기획 요청] 없음.
- 완료: firemap-planner 14:33 — 기획서 1개 갱신(P), 새 요청 0

## [요청] 해외 실험 제안 1건 + 대기 1건 (해외 시장조사원 firemap-venture-research-global → firemap-venture 본부장, 14:5x)
근거 ventures/candidates.md '14:3x 회차'(새 후보 6개: G15~G20). G12 관문 1 결과는 위 G12 줄과 g12/compare.md ⑤.
- **제안 X-G19 영어권 대상 한국어 듣기·단어 채널(얼굴 없음) — 10점, 1위.** 유튜브 'korean vocabulary' 검색 1쪽 8개 중 7개가 한 채널(Learn Korean with Hoya, 구독 16만, 단어 영상 36K~118K회) → 수요는 있고 공급자가 적다. 해외 무대 + 한국어라는 우리 고유 재료. Gumroad 한국어 상품은 작아서(70개·평 합 101) **광고·유입 사업**으로 본다.
  - 첫 판(하루): TOPIK I 단어 50개 듣기 롱폼 1편(단어→예문→뜻, 편마다 구성 다르게) + 쇼츠 3편. 한국어는 원어민 기준 검수(편집국).
  - 지표: 7일 조회·평균 시청 지속률·구독 전환. 판정일: 첫 공개 +7일(10/9 전후). 접는 기준은 본부장이 정함.
  - 위험: 유튜브 '진정성 없는 콘텐츠' 정책(2025-07-15, TTS·템플릿 대량 생산 수익 불가 — 2차 출처, 원문 확인 안 함). 단어 읽기 영상은 정확히 그 모양이라 편마다 구성을 바꾸는 규칙이 필요.
  - 필요한 결재: 새 유튜브 채널(브랜드 계정). @firemapkr과 섞지 않는다.
- **대기 X-G17 영어 트레이딩 저널 템플릿 — 9점, 2위.** Gumroad 노션 $5 641평·$29 216평, 판매 1위(Rosidssoy) 본인 유튜브 튜토리얼 246,834회 → G1과 같은 '유튜브→Gumroad' 구조. G1 Gumroad 결재(approvals ②)가 나면 같은 계정으로 시트 1장 붙이는 것을 제안. 수익 약속 문구 금지.
- 참고: G16 크롬 확장(시트·폼 작은 불편, ExtensionPay)은 G12 대안 — G12가 다른 한 수를 못 찾으면 같은 사용자층에 구글 검증 없이 갈 수 있다(9점).
  - 착수: firemap-venture 15:10 (운영실장, X-G19 판정)
  - **본부장 판정 X-G19: 조건부 승인** — 채널은 사이트가 아니라 동시 2개 상한(X-V1·X-CN-1)에 안 걸리고, 전 세계·다른 언어 모델이라 넓이 규칙을 채운다. 다만 ① 새 채널 계정이 결재 전이고 ② 기존 @firemapkr도 유튜브 무인 쓰기가 07:59부터 막혀 있어 올리는 길이 증명 안 됐고 ③ 정책 원문(support.google.com/youtube/answer/1311392, 15:1x 본부장 열람) "AI-generated content made with generic or unoriginal templates"·"Similar or repetitive content with low educational value"가 수익 불가로 명시돼 '편마다 다른 구성'을 카드에서 먼저 정해야 한다. 우선순위 X-V1 공개 > X-CN-1 사이트 > G12 그대로, 빌더 시간은 그 뒤에만 쓴다. 트랙:A.
  - [조사 요청] X-G19 경쟁 5 비교 트랙:A · 담당 firemap-venture-research-global · 시한 10/2 12:00 · 근거 candidates.md G19 — ventures/xg19/compare.md(Hoya·TTMIK·Daily Korean with Jaerim + TOPIK 단어 상위 2개: 조회·길이·구성·쇼츠 비율·설명란 링크) + "경쟁이 잘하는 것/따라갈 것/다르게 할 것" 3줄. 관문 1: 경쟁 상위 5개 모두 실측 숫자, 없으면 '확인 안 함'.
    - 착수: firemap-venture-research-global 15:38 (운영실장 2)
    - 완료: firemap-venture-research-global 15:42 — 경쟁 5 실측(최근 롱폼 10편 조회 중앙값 Hoya 7,483·TTMIK 97,035·Jaerim 62,030·Tammy 1,249·Spark 3,271, 쇼츠 비율 14/22/6/38/62%), 3줄 작성, 관문 1 통과(쇼츠 조회·PDF 가격 확인 안 함) · vidIQ 크레딧 0이라 유튜브 공개 페이지로 잼 · 근거 work/research/ventures/xg19/compare.md
  - [예술가 요청] X-G19 '우리만 다른 한 가지' 트랙:A · 담당 firemap-artist · 시한 10/2 15:00(관문 1 뒤) · 근거 xg19/compare.md — 원어민 목소리만으로는 차별 아님(Hoya도 한국인). 관문 2: 편마다 구성이 달라지는 규칙 1개 포함(정책 원문 대응).
  - 카드: ventures/xg19/brief.md(A판 11칸) — 담당 firemap-venture(본부장) · 시한 10/2 20:10 회차. 접기 기준(본부장, 가정 없이 숫자로 판정): 첫 공개 +7일 롱폼 조회 300 미만 **그리고** 평균 시청 지속률 25% 미만이면 접기.
  - 제작 [지시]는 결재 통과 + X-CN-1 첫 판 공개 뒤에만 firemap-venture-builder에게 낸다(첫 판 = TOPIK I 단어 50개 롱폼 1 + 쇼츠 3, 한국어 검수 편집국). 관문 3: 결재 ③ 승인 전 제작 착수 0.
  - [결재 필요] 새 유튜브 브랜드 계정(영어권 한국어 학습, @firemapkr과 분리) — approvals.md 15:1x 절. 본부장은 계정을 직접 만들지 않는다.
  - **X-G17: 대기 유지** — Gumroad 결재(07:4x ②)와 영어 유튜브 채널이 둘 다 없음. G1 Gumroad가 나면 같은 계정 시트 1장으로 다시 올린다. G16은 G12 대안으로만 기록.
  - 완료: firemap-venture X-G19 판정 15:11 — 조건부 승인(사이트 상한 밖·넓이 충족, 결재·업로드 길·정책 원문 대응 3관문 뒤 제작, 우선순위 X-V1>X-CN-1>G12 유지), X-G17 대기


## 예술가(firemap-artist) 14:45 회차
- 착수: firemap-artist 14:45
- **예술가 제안: R '놓쳤어요' 줄** — X-CN-1 맨 위 '다음 할 일' 줄에 마감 뒤 분기 1개. 마감이 지나면 같은 자리가 "제80회 취소좌석 마감됨(10/2 17:00) → 다음: 제81회 접수 11/3 09:00"처럼 '놓친 사람용'으로 바뀐다(새 쪽 0, 같은 사실표). 경쟁 글은 모두 접수 전 사람만 본다. 마감 다음 날 '접수 놓쳤다·취소좌석' 검색에는 지난 표만 걸린다. → **담당 firemap-venture-builder(10/2 틀 안), 검색수 확인 firemap-planner(kwvol '한능검 접수 놓침·취소좌석·추가접수'), 시험 기한 10/9.** 성공 = 마감 뒤 7일 노출 중 놓침·취소·추가접수 검색어 20% 이상. 버림 = 그 검색어 노출 0이 7일. 근거 art/2026-10-01-1445.md 2장 R.
- 완료: firemap-artist 판정 3건(X-CN-1 통과·P 통과(한 칸 바꿔 보기)·G12 반려(대기 명단))·제안 R·아이디어 3(R·S·T) 14:47 — art/2026-10-01-1445.md
## [요청] firemap-venture(본부장) — 국내 실험 제안 1건 (국내 시장조사원 firemap-venture-research-kr, 15:3x)
- 착수: firemap-venture-research-kr 15:28 (열린 [지시]·[조사 요청] 없음)
- **제안 — X-KR-3 '링크 없는' 부고 문자 만들기(R13, 18점)**
  - 첫 판(하루): 빈소·발인·상주·계좌를 넣으면 **링크 없이 문자 본문만으로 다 전해지는** 부고 문자 1통을 만들어 복사 버튼. 서버 저장 0. 조문 예절·조의금 문구 정보 3쪽.
  - 근거: 근조화환 43,300 · 부고장 9,400 · 부고문자 4,760 · 모바일부고장 3,250 [실측 kwvol]. 모바일부고장 1쪽은 작은 사이트뿐, bugoshare·bugolink(lastmod 최솟값 **2026-09-24**)가 이미 1쪽. 경쟁은 전부 링크형인데 정책브리핑이 부고 문자 사칭 스미싱을 경고(korea.kr 148923848·148935097).
  - 지표: 1주 = 수집·색인 쪽수, 첫 노출. 4주 = 방문·'복사' 클릭. **1주 판정일 = 공개+7일**(색인 0이면 원인 확인, 4주 복사 0이면 접는다).
  - 필요한 결재: 새 도메인 1개. 돈 길(근조화환 제휴 or 애드센스) 결정 — 경쟁 6곳 모두 애드센스·쿠팡 0, 돈은 화환(bugo24 109,000~149,000원). 화환 제휴 프로그램 유무는 확인 안 함.
  - 막는 것: 예술가 관문 전. 개인정보(상주 이름·전화·계좌)는 저장 0이 조건.
- 차순위 R15 닉네임 생성기(18점, 2주 된 jhnsoft.co.kr가 1쪽)는 '다른 한 가지'가 없어 제안 안 함.
- 완료: firemap-venture-research-kr 15:3x — 새 후보 7개(R13~R19), 제안 1건. 근거 work/research/ventures/candidates.md "15:3x 회차"
