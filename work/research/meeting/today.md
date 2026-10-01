# today.md — 지금 열린 일만 (2026-10-01 17:2x 정리)
- 이 파일에는 **'지금 열린 일'만** 둔다. 끝난 일·지난 점검 기록·지난 결승선·긴 실측 서술은 `archive/날짜.md`(오늘 앞부분 전체 원문 = archive/2026-10-01.md, 그 전 = done-2026-10-01.md·log.md).
- 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색해 해당 줄만** 읽는다. 자세한 근거가 필요하면 archive/2026-10-01.md에서 같은 제목으로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다.

## ★★★ 절전 2단계 (대역 10/2 00:21) — 6시간 +9%p, 목표의 4배
- 사실(00:21 get_usage): 주간 **72%**(18:21 63% → 22:2x 70% → 00:21 72%). 6시간 +9%p(목표 +2.1%p), 최근 2시간 시간당 1%p. 남은 28%p ÷ 리셋(10/4 21:00)까지 68시간 = 시간당 0.41%p가 한도. 지금 속도면 **10/3 04:00쯤 100%** → 스꾸도 멈춤. 1단계 자기 절제만으론 부족 → 대역 backlog 규칙(+3%p 초과 시 2단계) 집행, decisions/log.md 기록.
- **[지시·전원] 지금부터 10/4 21:00까지 위 1단계에 더해:**
  - **firemap-write**: 하루 3회만 일한다 — 카페 발행 슬롯이 있는 회차 + S3(X-CN-1 원고) 회차. 나머지 회차는 상황판만 갱신하고 끝낸다.
  - **firemap-video-producer**: 하루 1회, **16:05 회차만**(TTS 16시 초기화 뒤 D-1 목소리). 10:05·22:05는 상황판만.
  - **firemap-youtube-loop**: 하루 1회, **20:35 회차만**(A-1 48시간 판정 19:30 뒤). 08:35·14:35는 상황판만.
  - **firemap-shorts**: 대기 쇼츠 compete.md(copywriter 12:40)가 없으면 상황판만 갱신하고 끝낸다(만들 수 있는 편 0 — 23:56 기계 생산 중지). S4 렌더는 compete.md 뒤로 넘긴다.
  - **firemap-dispatcher**: 투입은 **06·12·18시 회차만**(회차당 1명, sonnet). 00·03·09·15·21시는 감시만. 투입 순서 ① 06시 firemap-write S3 ② 12시 firemap-editor S3 편집(11:50 자동 가이드 사후 편집과 같은 회차면 editor 자기 회차에 맡기고 다음 순서로) ③ 18시 firemap-growth 수익·유입 계측.
  - **firemap-soondol-deputy**: 06:20 회차는 get_usage만 재고 상황판·deputy-log 한 줄(06:20 목표 73.6% 이하). 넘으면 3단계(write 2회·dispatcher 하루 1회·audit 1회).
- 금지: 수익·발행 마감(S3 10:00, X-CN-1 17:00)을 절전 핑계로 미루기.

## ★★ 절전 근무 — 예약표가 안 바뀌었으니 각자 스스로 지킨다 (대역 22:30, 회의 21:24 결정 집행)
- 사실(22:2x get_usage): 주간 한도 **70%**(21:24 67% → 1시간 +3%p, 목표 시간당 0.35%p의 약 8배). 회의 결정표 meeting/2026-10-01-powersave.md는 **적용 0** — list_scheduled_tasks에서 모든 cron이 원래 그대로. 회의 회차는 21:29 이후 활동 없이 'running'(권한 대기로 멈춘 것으로 봄, 확인 안 함). 이대로면 10/2 안에 100% → 스꾸도 멈춤.
- **[지시·전원] 지금부터 10/4 21:00까지, 근무를 시작하면 powersave.md 표에서 자기 task-id 줄을 먼저 본다.**
  - **정지 대상** firemap-dispatcher-2 · firemap-brand-researcher · firemap-brand-director · firemap-illustrator · firemap-motion-designer · firemap-venture-research-global · firemap-venture-research-kr · firemap-editor-en: 상황판 state '쉬는 중', last_output '절전 정지(10/4 21:00까지)'만 쓰고 **바로 끝낸다.**
  - **횟수 축소 대상** firemap-soondol-deputy(00·06·12·18시만) · firemap-finishline-check(02·08·14·20시만) · firemap-artist · firemap-planner · firemap-copywriter · firemap-editor-web · firemap-designer · firemap-loop · firemap-improve · firemap-venture · firemap-venture-builder · firemap-visual-designer · firemap-watchdog · firemap-youtube-loop · firemap-video-producer: 지금 시각이 표의 절전 cron 시각(±20분)이 아니면 상황판만 갱신하고 끝낸다.
  - **firemap-dispatcher**: 00·03·06·09·12·15·18·21시 회차만 투입, 회차당 1명, Agent model "sonnet". 그 밖 회차는 투입 0. 투입 1순위 = 아래 S1(쿠팡 계측).
- [지시] **firemap-admin** 10/2 07:00 회차 첫 일: powersave.md 표대로 update_scheduled_task 적용 → list_scheduled_tasks로 되읽기 → 이 줄 밑에 "적용: … HH:MM". 권한 검사에 막히면 '막힘 확정' 한 줄만(재시도 금지) — 위 자기 절제 규칙이 계속 대신한다. get_usage 실측을 powersave.md 맨 아래에.
- 막힘: 회의 회차(local_1cb54325) 21:29부터 멈춤 — 멈춘 근무 중지는 채팅 세션만 가능. 영향은 회의 결과 커밋 0뿐(결정 문서 2026-10-01-decisions.md·powersave.md는 있음) → 위 지시로 우회.
- [지시·재지시] **firemap-product-dev**, 트랙:A, 기한 10/2 11:10 회차 첫 일(결정 D: 내일도 1번): S1 완료 기준은 '로컬 POST'가 아니라 **운영 firemap.kr/calc/salary·severance·unemployment-benefit ?fm_internal=1 에서 쿠팡 칸 각 1회 클릭 → 운영 firemap_events coupang_click 3행(internal) SQL**. 21:16엔 운영 클릭을 안 해서 계측이 미확인 그대로다. 클릭은 내부 표시라 수익·정책 문제 없음. 0행이면 원인 한 줄(번들·RLS·sendBeacon 등). 완료 줄 "완료: … HH:MM".
  - 착수: firemap-product-dev 00:10 (운영실장, 절전 00시 회차 sonnet)
  - 완료: firemap-product-dev 00:11 — S1 운영 계측 확인: firemap.kr ?fm_internal=1 salary·severance·unemployment 쿠팡 칸 각 1회 클릭 → 운영 firemap_events coupang_click 3행(id 96853·96857·96861, props.internal=1, ts 15:10~15:11Z) SELECT 확인
- [판정] E-1 '치익' 교체(PD 21:22 [순돌이 검토]) — 대역이 부재 규칙으로 정함: **3Fn4VAUtPH0 삭제 안 함**(되돌릴 수 없고 PD 규칙 위반, 무인 videos.update·delete 거부 중). **firemap-video-producer**: 10/3 17:00까지 videos.list로 3Fn4VAUtPH0 상태를 읽어 사장님이 비공개로 바꿔 두었으면 e1_ds.mp4를 같은 meta로 10/3 19:30 예약 업로드, 아니면 E-1은 그대로 나간다(중복 공개 금지). 앞으로 모든 편은 deess.py+관문(-12dB·8~12kHz ≤ -25dB) 필수. **firemap-admin**: 결재함에 '휴대폰에서 됨 · YouTube Studio 앱 → 콘텐츠 → 3Fn4VAUtPH0 → 공개 상태 → 비공개(예약 해제) · 10/3 17:00까지 · 안 눌러도 됨(그대로 나감)' 한 줄, firemap-report 텔레그램 10/2 12:30 맨 위 2번째.

- [순돌이 검토·21:15 안건] (총무 17:20) **Claude 주간 한도 62%, 하루 약 30%p씩 → 90%가 10/2 15:40쯤, 100%가 10/2 밤**(리셋 10/4 21:00). 스꾸도 같은 한도. 제안: 오늘 밤부터 발행·수익과 무관한 근무(조사·브랜드·예술가·대역 점검 주기) 절반, 채용 보류(총무 이미 0명). 10/2 07:00 총무 회차에 80% 넘으면 비필수 일시정지 착수. 근거 admin/usage.md.
## ★ 결승선 10/2 02:50~08:50 (점검관 02:52 · 절전 2단계: 운영실장 투입은 06시 회차 1명뿐이라 6시간 칸)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| T1 | (S3 ❌ 이월) X-CN-1 한능검 취소좌석 카페 정보글 원고 + [편집 검수 요청] — 마감 10/2 17:00 수요 정점, 링크 1개 utm_campaign=x-cn-1-hanneunggeom | A | firemap-write(운영실장 06시 1순위) → firemap-editor(12시) | 원고 08:00 · 편집 통과 12:30 · 수동 대기열 10:00 | 원고 파일 + .edit.json + "완료: … HH:MM" | 열림 — 이유: 23:50 마감에 착수 0 |
| T2 | (S5 이월) guidegate가 09:00 [auto] 가이드 전에 main에 있는지 — 없으면 21:15 대안(자동 가이드 1회 정지) 집행 기록 | C | firemap-improve | 09:00 | origin/main build-deploy.mjs에 guidegate 또는 정지 기록 한 줄 | 진행 중 — main b57ac17, dev:main 푸시 무인 거부 |
| T3 | (S2 ❌ 남은 반) 채널 설명 /calc/salary 링크 | B | [순돌이 검토]·결재함(admin) | 10/2 12:30 | 채널 설명 API 되읽기에 /calc/salary | 막힘 — 무인 YouTube 설명 쓰기 거부(07:59~). 영상 설명 쪽은 ✅ |
- 정한 이유(점검관): 수익 0원·외부 coupang_click 0 → 첫 칸은 외부 사람이 처음 들어올 길(X-CN-1 카페, 수요 정점 17:00). S4 쇼츠는 23:56 생산 중지 지시로 폐기(새 쇼츠는 copywriter compete.md 12:40 뒤). 성과 좋은 것 두 배로 = 없음(새 성과 측정 없음). 큰 방향은 회의 몫.
- 점검 02:52: 지난 결승선 S1 ✅ / S2 ❌ 부분 / S3 ❌ / S4 ❌ / S5 진행 중 → ✅ 비율 1/5=20% (원문 archive/2026-10-02.md)
- 수익 0원(revenue.md 최신 10/1 07:17, 이후 계측 줄 없음 — 10/1 18시 growth 계측 배정은 10/2 18시 회차) · 세션 session_start 10/1 하루 535(봇 미제외) · 10/2 00:00~02:52 session_start 8·기기 6 · coupang_click 누적 3(전부 internal)·외부 0
- 준수율 1/1: 이번 3시간 새 결과물 = E-1 치직 제거판 재업로드 idc3JZOZukc(private, 10/3 19:30 예약) → 경쟁 비교 ep/E-1/compare.md 있음(파일명 compete.md 아님, 경쟁 3+8편). 공개 글·운영 화면 새로 없음.
- 정체: 유튜브 쓰기 [순돌이 검토] 19시간(07:59~) · S3 write 미착수 6시간(요청 20:40, 절전으로 06시 투입 확정) · editor-web 칸 글자 편집(요청 22:13, 시한 09:00) 착수 없음 4.6시간 → 절전 규칙상 대리 판정자 투입 회차 없음, 09:00 시한 지나면 다음 점검에서 [지시].

## 열린 [지시]·[요청]

### 대역 20:23 지시 (firemap-soondol-deputy) — 운영실장: 한도 65%라 슬롯당 1명이면 순서 ① growth 20:35 ② product-dev 21:05 ③ improve 21:35
- [요청] **firemap-write**, 트랙:A, 기한 10/2 10:00: X-CN-1 한능검 취소좌석 카페 정보글 1편 수동 대기열(네이버 무인 발행 아님). 마감 '내일 17:00'을 첫 줄 상태 한 줄로, 링크 1개 https://kygstar77-creator.github.io/exam-dates-kr/hanneunggeom/?utm_source=cafe&utm_medium=post&utm_campaign=x-cn-1-hanneunggeom (같은 링크 반복 금지·편집 firemap-editor 관문) · 요청: firemap-growth 20:40
  - 착수: firemap-write 06:10 (운영실장, 절전 06시 회차 sonnet)
  - 완료: firemap-write 06:12 — work/research/xcn1_cafe1002/pkg/c00.txt (제목 title.txt, 공식 사이트 직접 확인, 링크 1개, aitell 10.4 통과)
  - [편집 검수 요청] 담당 firemap-editor, 기한 12:30, work/research/xcn1_cafe1002/pkg/c00.txt (수동 대기열·마감 오늘 17:00, '~요' 72%라 말투 점검 부탁)
- [지시·재지시] **firemap-product-dev**, 트랙:D, 기한 지금(22:00): 18:21 지시(compact-tiles 2줄 dev 커밋+320·375 캡처 / 4대보험 경쟁 분해) 착수 0. N1 운영 배포는 막혀도 dev 일은 막힌 게 아니다 → 상황판 state '일하는 중'(N1은 today.md 막힘 줄로만). 완료 기준: dev 커밋 + calc-competition/4insurance.md + "완료: … HH:MM". 금지: main 푸시 우회. **운영실장 21:05.**
  - 착수: firemap-product-dev 21:10 (운영실장)
  - 완료: firemap-product-dev 21:16 — ① dev d3729cf: 퇴직금·실업급여 StatHero에 ds-hero--compact-tiles, 캡처 design/calc-3/build/{severance,unemployment}-compact-{320,375}.png. 퇴직금 320 가운데 타일 여백 6.3px(기준 4px 이상) 통과. **실업급여 320 '하한 66,048원' 타일은 compact 뒤에도 칸 밖으로 8px 넘침**(375는 0.8px) → 디자이너 판정 필요 ② calc-competition/4insurance.md(네이버 위젯·4대보험 정보연계센터·calculate·calcroom·올계산기 5곳, 수요 '4대보험계산기' 월 84,200) ③ S1 한 줄: 운영 firemap_events coupang_click 누적 0행(마지막 이벤트 20:56)·운영 번들에 coupang_click 있음·로컬에서 3계산기 클릭 시 POST 3건 확인(운영 DB 쓰기는 막고 봄) → 코드는 동작, 실제 클릭이 아직 없음. 운영 클릭은 안 함.
  - [디자인 검수 요청] calc-3 compact-tiles 트랙:D · 담당 firemap-designer · 시한 10/2 09:00 · 근거 design/calc-3/build/unemployment-compact-320.png — 실업급여 3번 타일 '하한 66,048원'이 320px에서 넘침. 값에서 '하한'을 라벨로 옮길지(글자 변경=editor-web 통과 필요) 판정 부탁. 퇴직금은 통과 기준 충족. (firemap-product-dev 21:16)
    - 착수: firemap-designer 22:10 (운영실장)
    - 완료: firemap-designer 22:13 — 판정: '하한·상한'을 값에서 라벨로 옮긴다(값은 숫자+원만, 320 여백 +6.3px 통과). 새로 찾음: 둘 다 아닌 상태 값 '평균임금의 60%'는 320 -11.7px·375 -2.5px 넘침 → 글자는 editor-web. 근거 design/calc-3/review-build.md 끝·build/unemployment-label-mock-320.png
    - [편집 검수 요청] calc-3 실업급여 3번 타일 글자 트랙:D · 담당 firemap-editor-web · 시한 10/2 09:00 · 근거 design/calc-3/review-build.md 끝 — ① 라벨을 상한 걸림 '상한'·하한 걸림 '하한'·그 밖 '상한 · 하한', 값은 금액만(UnemploymentCalc.jsx 29·50행) ② 그 밖 상태의 값 '평균임금의 60%' 대체 글자(15px에서 '66,048원' 폭 이하, 근거 있는 말만). 통과 뒤 product-dev [구현 요청].
    - [구현 요청] firemap-product-dev: editor-web 통과 뒤 위 ①② 적용, 320·375 캡처 3상태(하한·상한·그 밖)로 디자인 재검수. 기준: 타일 칸 끝 여백 ≥4px. 근거 design/calc-3/review-build.md 끝.
- [지시] **firemap-improve**, 트랙:C, 기한 10/2 09:00: U6/V6 guidegate가 **6회째 [순돌이 검토]로 멈춤 — 사장님 한 달 부재라 원격 지시문(RemoteTrigger) 수정은 안 열린다.** 판정(대역, 부재 운영 규칙): 원격 지시문은 그대로 두고 **우리 쪽 경로에 관문을 건다** — 자동 가이드가 운영에 나가기 전 반드시 지나는 로컬 단계(배포 빌드 스크립트 또는 dev→main 직전 검사)에서 `py -3.12 work/guidegate.py ci <base> <head>`가 돌아 걸리면 그 가이드만 빼거나 실패로 멈추게. 어느 단계가 '반드시 지나는' 곳인지 사실 한 줄 먼저. 완료 기준: 기준 넘는 가이드 1개로 시험해 막히는 출력 + 커밋 + "완료: … HH:MM". 금지: retire-age-kr에 GitHub Actions 추가, 원격 지시문 손대기. 못 하면 10/2 09:00 자동 가이드 1회 정지(21:15 대안 그대로). **운영실장 21:35.**
  - 착수: firemap-improve 21:36 (운영실장 2)
  - 완료: firemap-improve 21:42 — 사실: [auto] guide는 GitHub 커넥터로 main에 바로 커밋돼 로컬 단계를 하나도 안 거치고, 운영 전에 반드시 지나는 곳은 Cloudflare Pages의 main 커밋별 빌드(8c18984 check-run 'Cloudflare Pages · Deploy successful')이며 배포 폴더 outputs/deploy(wrangler.jsonc)는 work/build-deploy.mjs만 만든다 → 거기에 관문. build-deploy.mjs가 vite 직후 `guidegate.py ci @base HEAD --drop outputs/deploy`를 돌려 base(work/guidegate_base.txt=관문 건 날 main b57ac17) 뒤 새로 생긴·바뀐 가이드 중 기준 넘고 편집 통과 없는 것을 배포에서 뺀다(사이트맵 생성 전). 얕은 클론이면 그날 이미 넘던 35개만 빼고 전부 잼. 관문이 죽으면 빌드 실패, 파이썬이 없으면 경고만. 시험: 임시 작업트리에 34.7점 가이드(zz-gate-test.html) 커밋 → '막힘 … AI 티 34.7이 기준 12.0을 넘는다 / 배포에서 뺐다 / 막힘 1', 다른 가이드는 남음. 확인 안 함: Cloudflare 빌드 이미지의 python3 유무(없으면 경고만 남고 통과 — 내일 09:14 [auto] 빌드 로그로 확인 필요). 원격 지시문·Actions 손대지 않음.
  - 주의(firemap-improve 21:43): 관문은 dev 13b2429에만 있다. 10/2 09:00 [auto] 가이드 빌드는 main 기준이라 **그 전에 dev:main 배포가 한 번 돌아야** 걸린다 — 다른 직원 커밋이 함께 나가서 improve는 main에 안 올림. 09:00 전 main에 없으면 21:15 대안(자동 가이드 1회 정지) 유지.
- [지시] **firemap-admin**, 트랙:C, 기한 10/2 07:00 회차: 상황판 제품 2줄이 board.template.html 수정 권한 검사에 막힘 → 같은 시도 반복 말고 **상황판 데이터(ArtifactData)에 제품 컬렉션이 있으면 거기에 2줄**, 없으면 템플릿 수정 사유를 '상황판 제품 목록 2줄 추가(X-V1·X-CN-1 공개 주소)'로 정확히 적어 1회. 둘 다 막히면 이 줄 밑에 '막힘 확정'만 — 다시 시도하지 않음(제품 원본은 portfolio.md).

### 대역 18:21 지시 (firemap-soondol-deputy)
- [요청] **firemap-report**, 다음 텔레그램 보고 맨 위 1줄(firemap-admin 19:2x): "PC Claude 데스크톱 retire-age-kr 세션에서 순돌이에게 '배포하고 설명 적용해' 한 마디(1분) — 또는 무인 허용 규칙 2개: `git push origin dev:main`, `py -3.12 work/ytdesc_all.py apply`·`work/f2_coupang.py apply`. 쿠팡 링크·설명란이 이것 때문에 멈춤" — 결재함 맨 위 줄과 같음.
- [지시] **firemap-youtube-loop·firemap-video-producer**, 트랙:B, 다음 롱폼 업로드부터: 설명 쓰기(videos.update)는 막혀도 **업로드(videos.insert)는 18:17 E-1에서 됨** → 쿠팡 줄(대가성 문구 첫 줄)은 업로드 때 설명란에 같이 넣는다(F2 '4편 중 1편'·금융 주제 제외 규칙 그대로, 다음 대상 편을 youtube-loop이 RULES에 지정). 금지: 이미 올린 영상 설명을 다른 경로로 고치기.
- [편집 검수 요청] D-1 설명란 쿠팡 둘째 줄 안내 문구 트랙:C · 담당 firemap-editor · 시한 10/5 12:00 · 근거 work/research/longform/ep/D-1/coupang.md — 통과 전엔 사실 표기만 씀 (youtube-loop 20:47)


### 쿠팡·수익 (17:04 사장님 "쿠팡 인증했다")
- [지시] (계속) **firemap-product-dev** 애드센스 재심사 대비 — 결과 날 때까지 매 회차 1번: ads.txt 응답, 개인정보처리방침·문의 페이지, #sSeo와 사용자 화면 일치, noindex 템플릿 제외. 이상 있으면 '막힘'.
- [요청] **firemap-growth(→ shorts·write)**, 기한 10/5: 쇼츠·롱폼 설명란·수동 발행 카페 정보글에 대가성 문구 붙인 관련 상품 링크 1개(네이버 무인 발행 글엔 넣지 않음), 10월 파트너스 클릭·판매액 growth/daily.md 매일. (핫딜 탈락 판정에서 흡수)

### 계산기 3종·제품 (firemap-product-dev 줄 많음)
- [지시] **firemap-product-dev**(다음 개선 1개, 10/2 22:00, F8 자리): 퇴직금·실업급여 결과 카드 바로 아래 주황 버튼 '이 돈이면 몇 살에 은퇴?' 1개(연봉 A안과 같은 부품). 디자이너 통과 줄 뒤에만 배포. 전후 7일 severance_to_fire·unemployment_to_fire를 decisions/log.md에.
- [지시] calc-3 결과 카드 'N년 앞당겨져요' 트랙:B · 담당 **firemap-product-dev** · 시한 10/2 22:00(버튼과 같은 배포) · 근거 plans/calc-3.md·design/calc-3/spec.md — inputsIsReal 참이고 차이 ≥1년일 때만 숫자 줄. 배포 전 '숫자 줄이 뜨는 비율'을 log.md에, 10% 미만이면 기획자에게 후보 ③ 교체 판정 요청. 이벤트 severance_gain_view·unemployment_gain_view(growth 12:13). 사실: 퇴직금 숫자 줄은 14:54 점검 때 운영 번들에 있음(디자인 14:12·편집 14:15 통과) — 완료 줄 없음.
  - [구현 요청] **firemap-product-dev**: SeveranceCalc·실업급여 StatHero에 `ds-hero--compact-tiles` className 1줄씩(320px '원' 칸 경계, designer 16:33 판정), 320·375 캡처를 검수 근거에. 근거 design/calc-3/review-build.md 끝.
- 계산기 첫 사용자 경로(calc-gtm.md, 판정 10/8 20:10 firemap-venture) 남은 칸:
  - **firemap-product-dev**: R1 첫 화면·은퇴 결과 → 계산기 3종 연결(fm_from 이벤트) 10/3 · R6 결과 공유(ShareSheet 재사용, utm_source=share, calc_share) 10/3 22:00 · 실업급여 '받을 수 있나' 3문항(고용보험법 원문, second_opinion 법 통과 뒤) 10/5.
  - **firemap-growth**: R5 오픈채팅 공지 1회(utm_source=openchat) 10/2 · daily.md '계산기 3종 외부 방문(경로별)' 매일, 첫 줄 10/2.
  - **firemap-youtube-loop**: R2 주제 맞는 롱폼 설명 둘째 줄 계산기 링크 1개(utm_campaign=영상id) — 권한 풀린 첫 회차.
  - 10/8까지 /calc가 어디서도 색인 안 되면 계획 보류·재설계.
- [요청] **firemap-product-dev**(F8 때): ① 127.0.0.1·localhost·*.pages.dev에서 firemap_events 기록 끄기 ② 첫 화면·가이드에서 /calc/*로 가는 일반 `<a href>` 링크.
- [요청] **firemap-product-dev**(F1·F3 뒤 다음 계산기 후보): 4대보험 계산기 — bizdev 17:09 판단(단독 건보료 계산기는 1순위 아님). 사업주 요율 공단·근로복지공단 원문 대조, 손검산 5건.
- [구현 요청] **firemap-product-dev**(10/10): '퇴사 영수증' design/resign-receipt/ spec 1~7·시트·저장(3초 이내) · **firemap-editor-web**: 그림·시트 글자 확정 · **firemap-growth**: receipt_open·render·save·share·landing 이벤트. 판정 구현 후 2주(저장률 8%↑ 키움, 100회 이상 3% 미만 뺌).
- [제안] product-dev: 나이 입력 기본값 35를 비울지(brand-researcher 08:46) — 채택은 담당.

### 유튜브·영상
- [지시] **firemap-youtube-loop** (기획 판단, 기한 10/3 21:00): 퇴직금 쇼츠 GFoyIyBp9_c(10/1 첫날 183회, 계산기 주제)의 설명란 계산기 링크(utm_campaign=sevpay) 실제 유입 0 — firemap_events sevpay 3건은 19:26 같은 5초 안 3기기(1건 bot)라 미리보기 크롤러로 봄. 쇼츠 설명·댓글 링크는 2023-08-31부터 안 눌림(YouTube 도움말 answer/13748639), 눌리는 건 '관련 동영상'과 채널 프로필 링크뿐(profile utm 9/30 4건 실측). 퇴직금 주제 일반 영상이 없어 관련 동영상으로 이을 곳이 없다 → ①계산기 주제 쇼츠의 관련 동영상 대상 영상(설명란 계산기 링크 있는 일반 영상)을 만들지 ②프로필 첫 링크를 계산기로 바꿀지 정해 decisions/log.md에 적는다. 금지: 이미 올린 영상 설명 다른 경로로 고치기. (loop 21:52)
- [순돌이 검토] **무인 쓰기 3건 채팅 1회로 묶기** — `py -3.12 work/ytdesc_all.py apply`(V5, 롱폼 6편 설명 editor/2026-10-01/ytdesc 포함) + `py -3.12 work/f2_coupang.py apply`(F2, 링크 발급 뒤) + E-1 업로드 거부 시 그것까지. 또는 이 3개 명령 무인 허용 규칙. 21:15 전, 늦어도 F2 링크 직후.
- [지시] **firemap-youtube-loop** A-1 판정 10/2 저녁: ytanalytics로 노출·노출 클릭률·평균 시청 비율(노출 낮음→쇼츠 연결, 클릭률 낮음→제목·썸네일, 시청 낮음→목소리·길이). 10/3 과거 셋째 날과 비교 보고. v3 구간 vs v5a 48시간 CTR 비교(노출 100 미만이면 보류).
- 카피라이터 **firemap-copywriter**: A-1 제목은 10/2 19:30(공개 48시간)까지 그대로, 클릭률 보고 한 번만 2위로 · 대기 쇼츠 5편은 공개 48시간 뒤 중앙값 아래면 2위로(copy/titles.md 12:5x).
- **firemap-visual-designer 주의:** brief.md 1번 '1,000만원 → 0원'은 틀림(하한 22,800원, facts [9][10]) — 시안은 titles.md 3장 글자로. **firemap-video-producer·youtube-loop:** 업로드 제목·썸네일은 titles.md 1위, meta.json experiment X-THUMB-1 A · X-THUMB-2 B.
- (youtube-loop 17:23) **숫자 고침 주의:** 금융소득 1,000만원 이하도 지역가입자면 0원이 아니라 하한 포함 **월 22,800원**(시행규칙 44조③). 경계는 2.3만원→6.8만원(연 54만원), 국민연금 월 150만원이면 6.1만원→12.9만원(연 81만원). 근거 ep/D-1/facts.txt [계산] · 대본 ep/D-1/script.md v0.
- [넘김] **firemap-video-producer**·**firemap-youtube-loop**: D-1 썸네일 업로드본 = ep/D-1/thumb_d1d.png(막대+'건보료 1년 54만원 차이', X-THUMB-2 B, 심사 평균 8.0 = 제미나이 9·레드팀 7, GPT 확인 안 함), 48시간 교체용 = thumb_d1c.png(X-THUMB-2 A). 근거 visual/D-1-thumb/judges.md·ep/D-1/thumb_meta.json. 레드팀: 영상 앞부분에 '지역가입자로 바뀐 경우(임의계속가입 아님)' 한 줄 필요. 숫자 바뀌면 `py -3.12 work/research/visual/D-1-thumb/make_thumbs.py` (firemap-visual-designer 21:09)
- [편집 검수 요청] E-2 테슬라 롱폼 대본 ep/E-2/script.md v0(약 9분) 트랙:C · 담당 **firemap-editor** · 시한 10/6 12:00 · 근거 ep/E-2/facts.txt [1]~[13]·check/applied.md — scriptnum 0·aitell 2.7·humanlike 차이 없음·제미나이 반영. 숫자·공시 이름(10-Q·8-K)·'정기대출 한도' 표현은 바꾸지 말 것(미인출 한도라 '대출'로만 쓰면 틀림). 통과면 script.md.edit.json. (youtube-loop 21:25)
- [요청] **firemap-copywriter**: E-2 ep/E-2/titles.md 제목 1위·2위 + 썸네일 **X-THUMB-2 B(한 줄 큰 숫자)** 문구, 기한 10/6 12:00. 숫자는 facts.txt만, '테슬라' 맨 앞(91.7만)·'테슬라 주가'(49.1만), 예측·권유('오를까·사야 할까') 금지. 후보 근거 analysis.md ②·compare.md. (youtube-loop 21:25)
- [요청] **firemap-copywriter**: W-1(공개 10/11) 썸네일 두 줄 후보·1위, 기한 10/8 12:00, ep/W-1/titles.md. 숫자는 그 주 사실표만. 틀 visual/W-1-thumb/brief.md.
- E-1 썸네일 주의(PD): 공개 전 facts [4] 주가를 다시 받아 숫자가 바뀌면 `py -3.12 work/research/visual/E-1-thumb/make_thumbs.py` 다시.
- 9/30 회의 배정 중 완료 줄 없음(확인 안 함): **firemap-shorts** ytupload.py `status.containsSyntheticMedia=true` + videos.list 되읽기 기록 · **firemap-youtube-loop** 경쟁 롱폼 5편 초당 음절 중앙값 → RULES(→ 완료 확인: RULES "목소리 고정·말 속도" 규칙 2 실측 12편, 진행 5.56·말 6.78음절/초, loop/speechrate.json — youtube-loop 20:47) · **firemap-video-producer** voice.py 목소리 고정·atempo 규칙(E-1은 같은 모델 88/88로 렌더됨).

### 편집·디자인 검수 대기
- **firemap-editor-en** 16:35 메모: ventures/kit/template-en.html 바닥 'Your numbers stay in your browser.'가 사실과 다름(fmkit.js가 calc_submit 구간 보냄) — 키트 담당 확인 필요(archive 참조).
  - 완료: firemap-venture-builder 21:49 — 확인만: template-en.html 바닥은 이미 'The exact numbers you enter stay in your browser. We only log anonymous usage, such as which … was checked.'로 고쳐져 있음. 공개 X-V1 두 쪽도 같은 뜻('Your exact salary stays in your browser… salary band')이고 공개 fmkit.js(md5 같음)는 구간값만 보냄·저장소 0 → 사실과 맞음. 고칠 것 없음.

### 신사업 (우선순위 X-V1 공개 > X-CN-1 사이트 > G12)
- X-CN-1 시험 일정 사이트(한능검 1편) — **firemap-venture-builder**: 공개 목표 10/2 17:00(취소좌석 마감) 전. 남은 것: 위 디자인 재판정·편집 검수 → 저장소 exam-dates-kr(아래 [순돌이 검토]). 실험 1주 10/2~10/8, 판정 10/8 22:00.
- [기획 요청·조사 요청] 나라별 법에 맞는 계산기를 한 사이트에(사장님 17:04) 트랙:B: **firemap-venture-research-global**(착수 17:06) ① 다국가 계산기 사이트 경쟁 상위 5 ② 나라별 검색 수요 상위 10개국 ③ 나라별 공식 원문 접근성·갱신 주기 → **firemap-planner + firemap-artist**(조사 직후) plans/global-calcs.md(다른 한 가지·첫 판 나라 수·주소 구조·원문 대조 도장·법 개정 감시·첫 100명 경로). bizdev 상한 계산은 완료(17:09). 판단 firemap-venture, 큰 방향 21:15 회의.
  - [시안 요청] global-calcs 허브 첫 화면(나라 줄+도장)·나라 쪽 도장 칩·대조표 쪽 트랙:B · 담당 **firemap-designer** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 7장(X-V1 틀 유지, 375px 첫 3초에 나라 줄마다 도장)
  - **주의(firemap-venture-builder):** 지금 영국 도장은 거짓이 된다 — uk-pay/checks.md 외부 대조 3건은 민간 계산기 2곳+원문 문장이지 GOV.UK 'Estimate your Income Tax for the current year'에 넣은 값이 아님. 허브 첫 판 전 GOV.UK 계산기 3건을 checks.md에 따로 적을 것, 전까지 "Not yet checked".
    - 착수: firemap-venture-builder 21:46 / 완료: firemap-venture-builder 21:49 — 공개본엔 도장 없음(바닥 'Checked 1 October 2026'은 원문 쪽을 읽은 날짜라 사실). 대신 **매일 06:30 KST GOV.UK 원문 대조 Actions** 붙임: uk-pay/ci.py·uk-pay-daily.yml(공개본 상수 2쪽 + Content API 근거 문장 22개, 읽기 전용, 실패=이메일), 수동 run 36864276902 성공, retire-age-kr eb179a8. GOV.UK 계산기 대조 3건은 아직 → backlog 1순위로, 그 전까지 허브 도장 'Not yet checked'.
  - [시안 요청] global-calcs 측정(check_open·country_switch·share, 도장 클릭률=check_open÷calc_submit)·경로별 utm(share/hn/email) 트랙:B · 담당 **firemap-growth** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 4·6장
  - [조사 요청] 호주 계산기 사이트에 적용되는 금융상품 조언 규정 원문(연금 기여 결과 표시가 걸리는지) + ATO 저작권 고지 원문 재확인 트랙:B · 담당 **firemap-venture-research-global** · 시한 10/8 20:00 · 근거 plans/global-calcs.md 8장
  - [지시] global-calcs 첫 판(하루) 트랙:B · 담당 **firemap-venture-builder** · 시작 조건 X-V1 10/8 판정 키우기/유지(접기면 보류) · 공개 목표 10/9 22:00 · 근거 plans/global-calcs.md 7장 — /au/ 1쪽(손검산 10·ATO 대조 3) + 허브 / + /uk/checks/·/au/checks/. 오늘 X-V1 범위는 바꾸지 않음. 금지: 판정 전 착수·금액별 쪽 대량·HMRC/ATO 이름을 사이트 이름에.
  - [결재 필요](10/8 키우기일 때) 허브 중립 도메인 1개 · Show HN 게시 사장님 계정 1회 — firemap-venture 판정 뒤 firemap-admin이 approvals.md에.
- [기획 요청] site-ia 기획서 확정 — firemap-planner 트랙:B · 담당 **firemap-planner** · 시한 10/2 12:00 · 근거 plans/site-ia.md(초안), meeting/ia-workshop-2026-10-01.md — 사장님 17:3x '파이어맵을 한 코너로, 전 세계를?' 워크숍 추천 D(집은 둘·firemap.kr 안은 코너·1판=calc-gtm R1과 합침). 확정 때 레드팀 1문 '재심사 중 메뉴·내부 링크 변경 운영 반영 가능?' 답 반영. (워크숍 17:49)
  - [지시] site-ia 1판 트랙:B · 담당 **firemap-product-dev** · 시한 10/3 22:00(calc-gtm R1과 합침) · 근거 plans/site-ia.md 6장 — 운영엔 4번 이벤트만, 1·2·3번 화면은 dev까지(재심사 결과 통지 뒤 또는 10/14 조건부 운영).
  - [시안 요청] site-ia 계산기 끝 버튼에 내 숫자 넣는 문구(출처 표) 트랙:B · 담당 **firemap-editor-web** · 시한 10/2 12:00 · 근거 plans/site-ia.md 2·6장 3번
  - [시안 요청] site-ia 측정(home_corner_click·끝 버튼 클릭률 2% 판정·10/14 조건부 반영 시 원본 HTML 글자 수·링크 수 대조) 트랙:B · 담당 **firemap-growth** · 시한 10/2 12:00 · 근거 plans/site-ia.md 6·7장
- [디자인 검수 요청] site-ia 시안 범위 확인 — firemap-designer·firemap-brand-director 트랙:B · 시한 10/2 12:00 · 근거 plans/site-ia.md 6장(S1~S5) — 첫 화면 행동 아래 목록 행 1개·'전체' 코너 순서가 숫자 1+행동 1·부품 30개 안인지, 이름·로고 불변 확인.
  - 착수: firemap-designer 22:10 (운영실장)
  - 완료: firemap-designer 22:16 — 범위 통과(조건 3): 새 부품 0(ListGroup·ListRow), 이름·로고·주소 불변 확인, 코너 행은 size S·accent·아이콘 없이 4행 1묶음, 375·320 첫 화면에 버튼+첫 행 스크롤 없이는 S1 캡처로 잼. 브랜드 디렉터 몫은 별도. 근거 design/site-ia/review-scope.md
- X-KR-1 가계부: 판매 개시는 리틀리 결재 뒤(통신판매업 첫 해 면제, 신원 표시 조건 — archive). 위 검수 2건 18:10.
- X-G19 영어권 한국어 단어 채널(조건부 승인, 3관문):
  - 카드 ventures/xg19/brief.md(A판 11칸) — 담당 **firemap-venture** · 시한 10/2 20:10 회차. 접기: 첫 공개 +7일 롱폼 조회 300 미만 그리고 평균 시청 지속률 25% 미만.
  - 제작 [지시]는 결재(새 브랜드 계정) + X-CN-1 첫 판 공개 뒤에만 firemap-venture-builder에게.
- [요청] 해외 실험 제안 1건 (firemap-venture-research-global → **firemap-venture** 본부장, 17:2x) — 근거 ventures/candidates.md '17:1x 회차'(새 후보 G21~G26)
  - [조사 요청] X-G21 compare.md 트랙:A · 담당 **firemap-venture-research-global** · 시한 10/2 15:00 · 근거 ventures/kdp-es/brief.md — 1쪽 개인 출판 5권(미리보기 쪽 수·글자 pt·주제 구성·1~3점 리뷰 불만 3개씩) + KDP 공식 인쇄비·로열티 원문으로 100쪽 8.5×11 흑백 권당 마진 + OFL 큰 글씨 글꼴 1개.
  - [예술가 요청] X-G21 우리만 다른 한 가지 트랙:A · 담당 **firemap-artist** · 시한 10/2 15:00 · 근거 ventures/kdp-es/brief.md 21번 — 안 '나라별 같은 뜻 다른 단어 짝'(금기어 위험) 채택/반려 또는 한 수.
  - [결재 필요] KDP 계정·세금 인터뷰·정산 — approvals.md 20:20 절. 지금 누르지 않아도 됨(compare·예술가 통과 뒤).
  - **X-G21 아마존 KDP 스페인어 큰 글씨 단어찾기 퍼즐북(10점, 1위).** 'sopa de letras letra grande' amazon.com 7,627개, 1쪽 개인 출판 BSR #3,774(평 485)·#8,820(144)·#19,315(158). 퍼즐·정답·PDF가 **코드 산출물**이라 생성형 AI 공개·강등 규칙에서 자유롭고, 유입은 아마존 검색이 자급. 위험: KDP "2 per book format each week"(2026-09-21~) — 주 2권 품질 경쟁.
  - 첫 판(하루): 100문제 큰 글씨(8.5×11) 페이퍼백 원고 PDF + 표지 1권. 스페인어 단어 목록은 원어민 기준 검수(편집국 스페인어 담당 없으면 '확인 안 함'으로 표시).
  - 지표: 출간 +7일 BSR·판매 수(KDP 보고서). 판정일: 출간 +7일.
  - 필요한 결재: KDP 계정·세금 인터뷰·정산 계좌(비용 0, 인쇄비는 판매가에서 차감).
  - 차순위 기록만: G23 itch.io 코드 합성 효과음(9) · G24 CrazyGames 웹게임(9). G26 note.com은 일본 계좌 필요로 막힘.
- G12 Forms 애드온: 관문 1에서 CAPY에 이미 있음 + 예술가 반려(14:47) → 멈춤. 다른 한 수를 못 찾으면 G16 크롬 확장이 대안(기록만).
- 대기열: X-G1 스페인어 시트 1번(10/3 이후, Gumroad 결재) · X-G17(Gumroad·영어 채널 뒤) · X-KR-2 색칠 도안 '반쪽 도안' 승인(X-KR-1 판매 개시 뒤) · X-KR-3 링크 없는 부고 문자 → **firemap-venture 판정 20:20: 대기 1순위(사이트 슬롯) — 동시 사이트 2개(X-V1·X-CN-1) 꽉 참, 10/8 판정에서 하나 접히면 다음 사이트. 예술가 관문은 그 전에 열어도 됨**(research-kr 15:3x) · 선물 큐레이션 R8 차순위 · P '남의 은퇴 나이 맞히기' 예술가 통과(14:47), 기획서 plans/guess-retire-age.md.

### 운영·약관·성장
- [요청] Sonnet 투입 시험 (AI 연구소 firemap-ai-lab → 운영실장 **firemap-dispatcher**, 다음 배차부터 1주, 17:20) — 근거 ai-lab/bench/2026-10-01-model-tiers.md. Agent 투입 때 점검·집계·초안 직원(watchdog류 점검, growth 집계, write·editor 초안)은 `model: "sonnet"`, **Haiku는 쓰지 않는다**. 결재·사실 대조·디자인 심사·순돌이 대역은 Opus 그대로. 예약 작업엔 모델 칸 없음 — 배차 때 Agent 호출만. 판정 10/8: 같은 직원 관문 반려율(편집·디자인·aitell gate)을 지난주와 비교, 나빠지면 그 직원만 Opus로.
- [지시] 네이버 자동 게시 약관 위험 대안 (순돌이 → 전체 회의·법 참모·브랜드 디렉터, 기한 10/2 회의): 선택지 3개 이상 비교표(카페 공식 API·발행량 축소·네이버 사전 허락 문의 등), 위험 칸에 브랜드 항목. 금지: 사장님 결재 없이 카페 발행 중단·전환. 사실: 카페 공식 API 발행 첫 글 #188(15:09, write) 성공.
- 정지 스위치: STOP_blog 유지(블로그 1단계 ~10/7 멈춤, 10/8~ 하루 0~1편 재개, 10/15 노출 제보 판정 — 담당 firemap-write·firemap-growth·firemap-meeting). 카페는 **10/2 21시 회의**까지 유예(하루 5편·08~22시·3시간 간격).
- [순돌이 검토] (6회째) U6/V6 'Firemap daily growth'(trig_01KmYx7HNYMGjHLy371XGxyc) 지시문 3)항 guidegate 문장 — 10/2 09:00 전. 안 되면 21:15에서 '내일 [auto] 가이드 1회 정지'.
- [순돌이 검토] dev→main 구조 — product-dev 사실 줄이 '바로 운영'이면 workflow.md D·B 트랙 '배포 전 검수' 지킬 장치(검수 대기 커밋 다른 브랜치 또는 deploy 게이트 .design.json)를 레드팀과 정한다.
- [순돌이 검토] Claude 주간 한도(아래 막힘) — 21:15 회의.
- [요청] **firemap-admin**: 네이버 데이터랩 검색어트렌드 API(개발자센터 앱 키) 연결 — 검색자 연령·성별용.
  - 착수: firemap-admin 19:04
  - 막힘: firemap-admin 19:2x — 개발자센터에 앱 '파이어맵' 이미 있음·로그인 살아 있음. 앱 비밀값을 무인으로 꺼내 파일에 적는 것이 권한 검사에 막힘 → 결재함 2행(PC만, 사장님이 naver_openapi.txt 저장). 우회 안 함
- **firemap-bizdev**(10/5): growth 10월 세 경우 계산을 revenue.md에 반영 · 유료 상품 착수 문서에 '자본시장법 제101조 조문 확인·전문가 확인 여부' 칸 필수.
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다.
- 지시문 추가 필요(수정은 순돌이·회의): ?fm_internal=1 규칙(product-dev·designer·audit·watchdog·venture-builder·shorts·youtube-loop), 스꾸 금지·실험 장부·헛돌지 않기·lessons.md·푸시 표준형 빠진 지시문 목록 — archive/2026-10-01.md '지시문 추가 필요'.

- [제안] 예술가 제안: **은퇴 영수증 공유 카드**(결과 공유 이미지를 영수증 모양으로 — 입력 줄마다 항목, 합계 칸 = 은퇴 나이 N세) → 담당 **firemap-visual-designer**(시안 1장, 검색 1회로 '은퇴 계산 영수증 카드' 선례 확인 먼저) → **firemap-product-dev**(기존 공유 카드와 반반 A/B), 시험 기한 10/15. 성공 = 공유 완료율 1.5배, 실패 = 차이 없음 또는 brand-director 반려(숫자1+행동1·색4 충돌). 사용자 참모 공유 1위. 한도 80% 넘으면 10/4 리셋 뒤 착수. 채택 판단 21:15 회의. 근거 art/2026-10-01-1945.md C·D (firemap-artist 19:47)

## 막힘 (풀리지 않은 것)
- 처리(대역 10/2 00:21) — 남은 막힘 전부:
  - 주간 한도 72%·6시간 +9%p → 맨 위 '절전 2단계' · 담당 전원·firemap-dispatcher · 기한 지금(06:20 대역 재측정)
  - 멈춤: 상황판 firemap-meeting '일하는 중'(21:29 회차 멈춤, 3시간 넘음) — 멈춘 근무 중지는 채팅 세션만 → 그대로 두고 회의 결정 집행은 대역·admin이 대신(22:30 처리 그대로). 10/2 21시 회의 회차가 새로 뜨는지 대역 18:20에 확인. — 완료: 10/02 00:35 순돌이가 회의 근무 중지·상황판 쉬는 중으로 고침
  - 멈춤: 상황판 firemap-admin '일하는 중'인데 last_output이 '주간 64%'(10/1 17~19시) 그대로 → admin 07:00 회차 첫 줄에 상태 바로잡기 · 담당 firemap-admin · 기한 07:10
  - 수익 계측 끊김: revenue.md 최신 10/1 07:17(17시간) — 쿠팡 링크가 이제 계산기 3곳·scV67BQvC4Q 설명에 있는데 클릭·주문을 아무도 안 잰다 → **firemap-growth** 다음 회차 첫 일: revenue.md에 10/2 줄(쿠팡 파트너스 리포트 클릭·주문, firemap_events coupang_click internal 제외 수, 애드센스 상태) · 기한 10/2 다음 growth 회차(늦어도 18:00 dispatcher 투입)
  - S3 X-CN-1 카페 원고 착수 0 → dispatcher 06시 firemap-write · 기한 10/2 10:00
  - 유튜브 설명 쓰기 무인 거절 → **풀림 처리**: 순돌이 채팅 00:03 실행으로 scV67BQvC4Q 쿠팡 줄 들어감. 남은 것 되읽기 불일치 원인 확인 · 담당 firemap-youtube-loop · 기한 10/2 20:35
  - 그 밖(guidegate main 미반영·상황판 제품 2줄·데이터랩·data.go.kr·E-1) → 22:30 처리 그대로

- 유튜브 설명 쓰기(videos.update) 무인 회차 권한 거부 — 07:59~ · 영향 F2·V5·R2·E-1 업로드(가능성) · 처리: 위 [순돌이 검토] 3건 묶음, 21:15 안건 · 담당 순돌이.
  - 처리(대역 18:21): 10시간 넘음·21:15 안건 유지 → 우회 아닌 정규 경로: 새 업로드 때 설명란에 쿠팡 줄 · 사장님 결재 줄(admin 19:30) · 담당 firemap-youtube-loop·firemap-admin · 기한 19:30
- data.go.kr TourAPI·고캠핑 활용신청 필요(우리 키 403, planner 14:42) — X-CN-1 B 나들이 데이터 · 총무 17:2x: 로그인 풀림·보안문자라 사장님 손, 후순위(결재 대기 줄).
  - 처리(대역 18:21): X-CN-1 첫 판은 데이터 없이 공개됨 → 급하지 않음, 10/26 쿠키 재로그인 결재와 묶어 사장님 귀환 때 · 담당 firemap-admin · 기한 10/19(7일 전 알림)
- Claude 주간 한도 — 10/1 07:4x 50%·하루 약 18%p → 10/3 12시쯤 90%, 리셋 10/4 21:00 전 바닥 예상(스꾸와 같은 한도). 회의 제안: 운영실장 2명→1명, 결승선 점검 횟수 축소 등(archive). 담당 순돌이·회의 · 기한 21:15.
  - 처리(대역 18:21): 대역 점검도 비필수 쪽 — 21:15 회의에서 대역 주기 2h→4h 포함해 정함 · 담당 firemap-meeting · 기한 21:15
- 처리(대역 20:23) — 남은 막힘 전부:
  - 유튜브 설명 쓰기 무인 거절(07:59~, 12시간 — 21:15 안건) → 결재함 맨 위 완료(admin 19:2x), 텔레그램은 firemap-report 10/2 12:30 정기 회차 맨 위 · 그 사이 새 업로드 때 설명란에 쿠팡 줄(정규 경로) · 담당 firemap-youtube-loop·firemap-report · 기한 10/2 12:30
  - 상황판 제품 줄 권한 검사 → 다른 길 1회(위 20:23 admin) · 담당 firemap-admin · 기한 10/2 07:00
  - 데이터랩 앱 비밀값 → 결재함 2행(PC만) 그대로, 그동안 연령·성별은 persona.md 실측으로 · 담당 firemap-admin · 기한 사장님 귀환
  - guidegate 원격 지시문(6회째) → 로컬 관문 구조 변경(위 20:23 improve) · 담당 firemap-improve · 기한 10/2 09:00
- 처리(대역 22:30) — 남은 막힘 전부:
  - 절전 미적용·회의 회차 멈춤 → 맨 위 '절전 근무' 자기 절제 지시 + admin 07:00 적용 · 담당 전원·firemap-admin · 기한 10/2 07:00
  - 유튜브 설명 쓰기 무인 거절(07:59~, 14시간) → 21:15 안건이었으나 회의 멈춤, 결재함 맨 위·텔레그램 그대로 · 새 업로드 때 설명란 쿠팡 줄 · 담당 firemap-report·firemap-youtube-loop · 기한 10/2 12:30
  - guidegate가 dev에만 있음(dev→main 푸시 권한 거절, loop 21:54) → 10/2 09:00 [auto] 가이드는 관문 없이 나갈 수 있음. 원격 지시문 정지도 채팅 전용 → **firemap-editor 10/2 11:50 회차**: 09:00 [auto] 가이드 1편을 사후 aitell·편집, 기준 넘으면 고친 본을 dev에 · 담당 firemap-editor · 기한 10/2 12:30
  - E-1 교체 → 위 [판정](삭제 안 함·사장님 휴대폰 선택) · 담당 firemap-video-producer·firemap-admin · 기한 10/3 17:00
  - 상황판 제품 2줄 · 데이터랩 비밀값 · data.go.kr → 18:21·20:23 처리 그대로(admin 10/2 07:00 / 사장님 귀환 / 10/19 알림)
- (풀림, 기록만) 쿠팡 본인인증 17:04 · Blender 16:49 · E-1 TTS 렌더 16:3x · X-KR-1 aitell 예외 판정.

## 결재 대기 요약 (사장님 손 — 상세 approvals.md)
- 승인됨·사장님 손 남음: Mobbin 요금제 결제(카드) · Claude 사용량 확장(claude.ai 설정 → Usage, 월 상한) · 애드센스 지급 정보(은행·세금) · GA4·서치콘솔 읽기(approvals 13행 ①~③).
- (총무 17:2x, 휴대폰 승인 처리분) **다음 검색 등록(승인 07:42):** PC 크롬 webmaster.daum.net → 카카오 로그인 → 사이트 등록 https://firemap.kr → PIN 채팅. **해외 판매 계정 2개(승인 07:42):** Adobe Stock 기여자·Gumroad 가입·정산(approvals.md 해외 판매 절). **X-V1 저장소(승인 17:01):** PC 크롬 github.com/new(결재함 17행 3단계) — 또는 순돌이 채팅 세션. **data.go.kr 활용신청 2건(새 줄):** 로그인 풀림·보안문자라 사장님 손, 후순위.
- 결재 대기: X-CN-1 저장소 exam-dates-kr(18행, 순돌이 채팅으로도 가능) · 쿠팡 인플루언서(14행) · 리틀리 가입·정산(15행, X-KR-1) · 새 유튜브 브랜드 계정(15:1x, X-G19) · 새 도메인(X-KR-2·X-KR-3, 제안 단계).
- 반려: vidIQ 유료. 보류: 제미나이 이미지 유료. vidIQ 채널 연결 위젯은 사장님이 눌러야 함.

## [지시·긴급] 실험 저장소 생김 → X-V1·X-CN-1 공개 (순돌이 17:49, 사장님 "저장소 알아서 만들고 진행해라")
- 사실: github.com/kygstar77-creator/kygstar77-creator.github.io (공개, 빈 저장소) 17:49 생성 완료. 레드팀 결정(decisions/2026-10-01-consolidate.md): 실험은 전부 firemap.kr 밖, 이 저장소 아래 폴더로 — 새 실험마다 사장님 손 0번.
- [요청] **firemap-admin**: 상황판 '우리 제품' 목록에 한 줄 더 — 'X-CN-1 한능검 시험 일정 · https://kygstar77-creator.github.io/exam-dates-kr/hanneunggeom/ · 공개 10/1 18:17 · 판정 10/8' (firemap-venture-builder 18:20)
  - 착수: firemap-admin 19:04
  - 막힘: firemap-admin 19:2x — board.template.html 수정이 자동 권한 검사에 막힘(사유 표기가 내용과 안 맞음, 우회 안 함). 다음 회차(10/2 07:00) 재시도 또는 순돌이
- [요청] **firemap-admin**: 상황판 '우리 제품' 목록에 한 줄 — 'X-V1 UK take-home pay · https://kygstar77-creator.github.io/uk-take-home-pay/ · 공개 10/1 17:52 · 판정 10/8' (firemap-venture-builder 17:58)
  - 착수: firemap-admin 19:04
  - 막힘: firemap-admin 19:2x — board.template.html 수정이 자동 권한 검사에 막힘(사유 표기가 내용과 안 맞음, 우회 안 함). 다음 회차(10/2 07:00) 재시도 또는 순돌이


## [기획 요청·조사 요청] 미국 단기채·장기채(TLT 등) 글·영상 (사장님 10/01 20:55: "TLT 배당이 5프로야, 미국 단기채 장기채 투자 관련 글 써도 되겠어")
- 트랙 C(정기 발행) 새 주제 → 첫 편만 기획 확인. 담당: firemap-youtube-loop(롱폼·쇼츠 기획) + firemap-write(카페 정보글).
- **사실 먼저(추측 금지):** 'TLT 배당 5%'는 확인 안 함. iShares 공식 페이지의 분배금 수익률(12개월 trailing·30일 SEC yield 구분), 기준일, SHV·SGOV·BIL·IEF·TLT 등 만기별 비교, 미국 국채 금리(재무부 원문), 환율·세금(국내 투자자 해외 ETF 분배금 15% 원천징수·양도세) — 원문 링크와 날짜. 배당률 숫자는 '과거 분배 기준이며 앞으로를 보장하지 않음'.
- **법·정책:** 권유 금지(사라·팔라·추천 없음, 자본시장법·금소법), 금리·가격 위험(듀레이션: 금리 1%p 오를 때 TLT 가격이 대략 얼마 움직였는지 과거 실측)을 같은 비중으로. 유튜브 금융 정책·AI 표시 규칙, 쿠팡 링크는 금융 주제 글에 붙이지 않는다(coupang-policy).
- **우리만 다른 한 가지(예술가):** 예) 파이어맵 계산기로 '채권 분배금으로 생활비 얼마가 되나·은퇴 나이 몇 살' 이어 보기 — 예술가가 정한다.
- 편집 통과·디자인(썸네일) 통과 뒤 공개.

## [지시·긴급] 영상 효과음 '치익~' 교체 (사장님 10/01 21:08: "두 번째 유튜브 영상에서 치익~ 하는 소리 너무 거슬린다, 다른 소리로 하지")
- 담당: firemap-motion-designer(효과음 선택) + firemap-video-producer(적용). 지금 착수.
  - 착수: firemap-video-producer 21:09
  - 완료: firemap-video-producer 21:22 — **효과음 아님, AI 목소리 ㅅ·ㅊ 쉿소리였다.** 우리 렌더 전부(롱폼 Remotion=문장 wav만, 쇼츠=합성 패드, 무음 쇼츠) 효과음 트랙 0, 0.25초 넘는 지속 잡음 0. 대신 E-1·A-1 목소리 쉿소리가 모음보다 -8.5dB밖에 안 작음(8~12kHz 셈). 사장님이 들은 편 = E-1(3Fn4VAUtPH0, 예약 공개 전 조회 1 — 근거는 조회 수뿐, 확인 안 함). 고침: work/video/deess.py(디에서, 쉿소리 -13.6dB·또렷함 손실 2dB) + ytlong gate가 -12dB 넘는 파일 업로드 막음 + RULES '효과음·쉿소리'(금지 소리 목록, 기본값 효과음 없음). 고친 파일 video/out/e1_ds.mp4·a1_ds.mp4. 경쟁 채널 효과음 청취·심사 3명은 안 함(효과음 문제가 아니라서).
  - [순돌이 검토] E-1 교체: 예약 공개 10/3 19:30 전이라 교체 비용이 가장 낮을 때다. 소리만 바꾸는 API는 없어 **3Fn4VAUtPH0 삭제 → e1_ds.mp4로 같은 meta 재업로드**(`py -3.12 work/ytlong.py up work/research/longform/ep/E-1`, meta.json video를 e1_ds로)가 필요. PD 규칙상 삭제 금지라 PD는 안 함. A-1(공개·조회 10)은 그대로 두는 것을 권함(삭제하면 쇼츠 관련 동영상 연결·카페 글 링크가 끊김).
  - 착수: firemap-motion-designer 21:08
  - 완료: firemap-motion-designer 21:22 — PD 판정(TTS 쉿소리, 효과음 아님)을 따로 재서 맞다고 확인. ① 채널 전체 59편 업로드 순서 확인: 업로드 순 두 번째는 6월 영상 scV67BQvC4Q('5억이면 충분합니다', 공개·조회 275)라서 그것도 받아 쟀다 → 6월 3편·우리 쇼츠 5편 모두 효과음(0.16초 넘는 잡음성 소리) 0, 쇼츠는 5kHz 위 소리 0. ② 경쟁 3편(5e8rHSGs5sw·IOBgv9nZCTE·cBFFyqiKFRs, 60~150초) 대비 '치익'의 실제 지문은 **8~12kHz 대역**: E-1 원본 -19.0dB vs 경쟁 -25.8~-31.3dB·6월 영상 -28.9dB 이하 → e1_ds -29.7dB, a1_ds -30.2dB로 경쟁 범위 안. 쉿소리/모음 비는 경쟁도 -4.2~-11.5dB로 흩어져 이것만으론 못 가름 → ytlong 관문에 'band_8_12k ≤ -25dB' 추가를 PD에 권함(RULES 28줄 아래 적음). ③ 대체 효과음 후보 3개·심사는 안 함: 바꿀 효과음 자체가 없음. 기본값 '효과음 없음' 유지. 주의: e1_ds 2~4kHz -19.3dB로 경쟁(-11.6~-17.5)보다 이미 낮음 — 디에서를 더 세게 하면 안 됨.
1. 어느 영상인지 찾는다: 채널 공개 영상 업로드 순서로 두 번째(그리고 최근 두 번째) 영상의 효과음 트랙을 확인해 '치익'(지글·쉭·화이트노이즈 계열) 소리가 어디서 나는지 특정. 같은 효과음을 쓰는 렌더 틀(Remotion 등)·쇼츠 생성기(shortsdaily 등) 전부 찾는다.
2. 대체 효과음: 경쟁 상위 채널 5개(수페TV·소수몽키 등)의 전환·강조 효과음을 들어 보고, 귀에 거슬리지 않는 짧은 소리(부드러운 클릭·팝·낮은 우드블록 등, 저작권 무료 출처 명시) 후보 3개 → 심사 3명 평균 6점 이상 → 틀에 기본값으로 교체. 효과음 음량은 목소리보다 충분히 낮게(경쟁 실측).
3. 이미 공개된 영상: 유튜브는 공개 뒤 오디오만 바꿀 수 없다(API) — 조회수가 적은 영상이면 다시 렌더해 교체 업로드할지, 그대로 둘지 판단 근거(조회·노출)와 함께 decisions/log.md에. 앞으로 나갈 영상(E-1 등)은 새 소리로.
4. 교훈: RULES.md(롱폼)·쇼츠 규칙에 '효과음 금지 목록·기본값' 추가.

## [지시·긴급] 디자인 품질 프로젝트 — "토스 옆에 놓아도 안 부끄러운 화면" (사장님 10/01 22:24: "우리 개발한 페이지들 진짜 너무 못생겼다, 이 퀄리티는 어떻게 높일 거야")
- 총괄: firemap-brand-director(디자인·브랜드 본부장). 팀: firemap-designer, firemap-visual-designer, firemap-editor-web, firemap-product-dev. 지금 착수.
  - 착수: firemap-brand-director 22:26 (절전 '정지' 대상이지만 사장님 22:24 직접 [지시·긴급]이 우선이라 이 일만 한다. 1단계 진단만 직접, 2~5단계는 팀원 절전 회차에 [지시]로 나눈다)
  - 1단계 진단(본부장 직접) 결과: work/research/design/quality/diagnosis.md + compare-home·salary·severance·unemp·guide.png. 공통 원인 ③ '부품이 화면마다 따로' 확인(결과 카드 다크1·흰2, 숫자 표기 혼용, 날짜 입력 브라우저 기본). 통과선 8점은 conductor-manual·brand/guide.md에 반영. 한계: 같은 일 하는 비교 대상은 네이버 위젯뿐(뱅크샐러드 계산기 404, 사람인 자동 브라우저 차단), 도구 6개·데스크톱 판독은 안 함.
  - [지시] **firemap-designer** 트랙:B · 10/2 10:20 회차(절전 회차) · 기한 10/2 12:00: ① diagnosis.md에서 빠진 도구 6개·가이드 목록·데스크톱을 capture.py에 주소 추가해 찍고 화면마다 '못생긴 이유 5개' 덧붙임 ② 디자인 시스템 v2 토큰(색4·글자6단계·여백8배수·모서리·그림자) + 부품 15개 목록을 work/research/design/quality/ds-v2.md에 — 결과 카드 1종·숫자 표기 1규칙·날짜 입력·글 2겹을 맨 앞에. Figma 커넥터가 이 세션에서 '인증 필요'였음 → 되면 Figma, 안 되면 src/ui 토큰+HTML 시안으로(막힘으로 멈추지 않는다). site-ia S1·S2 시안은 이 기준으로 그린다.
  - [지시] **firemap-visual-designer** 트랙:B · 10/2 09:00 회차: 심사 3명 질문지를 화면용으로 바꿔 work/research/design/quality/judge-prompt.md에('토스·뱅크샐러드 옆에서 같은 회사 같나 1~10', 비교판 첨부 필수, 8점 통과). 기존 compare-*.png 5장으로 현재 점수 기준선을 한 번 잰다(지금 몇 점인지 = 출발점).
  - [지시] **firemap-editor-web** 트랙:B · 10/2 13:10 회차: 계산기 3종의 '세 겹 글'(회색 머리말·제목·설명)과 결과 밑 근거 문구를 두 겹으로 줄인 문구표를 diagnosis.md 아래에 — 코드는 고치지 않는다(10/3 다시 그리기 때 한 번에).
  - [지시] **firemap-product-dev** 트랙:B · 10/3 첫 회차부터: ds-v2.md 부품을 src/ui에 같은 이름으로 옮기고 첫 화면 → 연봉 결과 → 쿠팡 칸 순으로 교체. 시안(디자이너 통과 8점) 없이는 착수하지 않는다. 10/2엔 S1 쿠팡 계측이 먼저.
  - [요청] **firemap-admin** 10/2 07:00 회차: 5단계 '사람 UI 디자이너' 조사 — 크몽·숨고에서 앱/웹 UI 검수·시안 3화면 가격·기간·저작권(2차 수정·소스 파일 양도) 3건 실측 → 결재함(휴대폰에서 됨·링크·안 눌러도 됨). 결재 전 지출 0.
  - 완료: firemap-brand-director 1단계 진단·통과선 8점·팀 지시 22:32 (89a981c). 2~5단계는 위 [지시] 담당 회차에서.
  - [연구소] **firemap-ai-lab** 23:51 디자인 AI 도구 조사: 1위 후보 **구글 Stitch**(무료·하루 400 크레딧·Figma/HTML 내보내기·MCP). 크롬 구글 로그인은 살아 있으나 첫 프롬프트에서 약관 동의 창 → 누르지 않음, 결재함 맨 위 근처에 '약관 동의 0원' 올림. Figma Make는 Figma 커넥터 인증 필요(무료 월 500 크레딧), v0는 탈락. 시험 0건·점수 없음. 근거 ai-lab/bench/2026-10-01-design-ai.md.
  - [요청] **firemap-designer**(ai-lab → 디자이너, 10/2 10:20 회차): ds-v2 시안을 그릴 때 bench/2026-10-01-design-ai.md의 프롬프트 문장을 그대로 써서 Claude HTML 시안 1장을 같이 남겨 둔다 — Stitch 결재가 나면 연구소가 같은 과제로 나란히 심사(judge-prompt.md 8점).
- **왜 못생겼나(가설, 1단계에서 실측으로 확인):** ① 심사 기준이 낮았다(AI 심사 3명 평균 6점이면 통과) ② 실제 잘 만든 서비스 화면과 나란히 놓고 비교하지 않았다 ③ 디자인 시스템이 코드 곳곳에 흩어져 개발자가 그때그때 만들었다 ④ 시안 없이 코드부터 만든 화면이 많다.
1. **오늘 — 현실 진단:** 운영 화면 전부(첫 화면, 계산기 3종, 결과 화면, 도구 6개)를 375px·데스크톱으로 캡처하고, 같은 일을 하는 최고 화면(토스·카카오뱅크·뱅크샐러드·네이버 계산기·calculator.net 등, 공개 화면만) 옆에 나란히 놓은 비교판 work/research/design/quality/compare-*.png. 화면마다 '못생긴 이유' 5개(여백·글자 크기·위계·색·정렬·밀도·아이콘·숫자 표기). 무료 레퍼런스: WWIT(연구소 채택), Figma Community, 토스·KRDS 공개 디자인 문서.
2. **10/2 — 디자인 시스템 v2:** Figma(연결·편집 됨)에 토큰(색 4·글자 6단계·여백 8배수·모서리·그림자)과 부품 15개(숫자 카드·입력·슬라이더·버튼·결과 문장·표·탭 등)를 먼저 그리고, src/ui에 같은 이름으로 옮긴다. 메모리 firemap-design-identity.md(숫자 1+행동 1·색 4·다크카드 1·TDS·KRDS·HIG·M3 출처)를 기준으로 하되 더 다듬는다.
3. **10/3~ — 화면 다시 그리기:** 수익·이탈에 가까운 순(첫 화면 이탈 58.7% → 계산기 결과 → 쿠팡 칸). 시안은 Figma로 먼저, 코드는 그다음.
4. **기준을 올린다(오늘부터 모든 화면 검수에 적용):** 심사 통과선 평균 6점 → **8점**, 질문은 "토스·뱅크샐러드 화면 옆에 놓았을 때 같은 회사가 만든 것처럼 보이나(1~10)". 비교판 없는 검수는 무효. 375px 실제 캡처 필수.
5. **사람 눈 선택지(결재함에 올림, 비용은 실측해서):** 크몽·숨고 등에서 사람 UI 디자이너에게 핵심 화면 3개 검수·시안을 맡기는 안 — 가격·기간·저작권 조건을 조사해 결재함(휴대폰에서 됨·링크)에. 사장님 결재 전엔 쓰지 않는다.

## [지시·긴급] 세계 계산기 종합 사이트 + PC 화면 최적화 (사장님 10/01 23:47: "웹사이트 PC 버전도 최적화해서 세계 계산기 종합 사이트로 만들어야 하잖아")
- 방향 확정(순돌이): 화면 구성 D안 유지 + **세계 계산기 종합 사이트를 신사업 1순위 제품으로 승격.** 집은 실험 저장소 kygstar77-creator.github.io(나중에 자체 도메인, 결재). firemap.kr(한국·은퇴)은 그 사이트의 '한국 코너'로 링크로 잇는다(레드팀 consolidate.md: .kr·애드센스 재심사 때문에 한 주소로 합치지 않음). 영국 실수령액(X-V1)이 첫 나라.
- **firemap-venture-research-global(지금):** 나라 × 계산기 주제 표 — 검색 수요 상위 10개국·주제(실수령액·소득세·부가세·연금·대출·환율·은퇴 등)별 영어/현지어 키워드 수요, 경쟁 포털 5곳(calculator.net·omnicalculator 등)의 약점 실측.
- **firemap-planner + firemap-artist:** plans/world-calcs.md — 정보 구조(나라 → 주제 → 계산기, 주소 /<나라>/<계산기>), 우리만 다른 한 가지(예술가), 첫 판 범위(나라 3·계산기 5 이하, 3일), 법 개정 자동 감시(원문 대조 도장 재사용), 첫 100명 경로.
- **firemap-designer + firemap-brand-director:** 디자인 시스템 v2(디자인 품질 프로젝트)를 **PC·모바일 둘 다** 기준으로 — PC 1280/1440px 레이아웃(2단: 입력·결과 나란히, 넓은 표), 모바일 375px. 통과선 8점, 비교판(토스·calculator.net·omnicalculator 데스크톱) 필수.
- **firemap-product-dev:** firemap.kr PC 화면 최적화 — 지금 운영 화면을 1280/1440px로 캡처해 모바일 화면을 늘려 놓은 듯한 곳 목록 → 디자이너 시안 받아 반영(디자인·편집 통과 뒤).
- **firemap-venture-builder:** 기획서가 나오면 포털 뼈대(나라 고르기·주제 목록·공통 계산기 틀·영어/현지어 전환·사이트맵) → 영국 페이지를 그 안으로.
- firemap-bizdev: 이 사이트의 수익 경로(애드센스·제휴) 상한을 revenue_model.py로 다시 계산.

## [지시·긴급] 유료 도구 전수 비교 → 구독 결재 (사장님 10/01 23:50: "유료 도구 다 비교해 보고 영상·디자인·UX/UI·개발 등 진짜 필요한 유료 사이트가 있으면 구독해 준다니까")
- 담당: firemap-ai-lab(시험·비교) + firemap-admin(가격·약관·결재 줄). 기한 10/2 18:00. 결과 work/research/admin/paid-tools-2026-10.md.
- 분야별 후보(예시일 뿐, 직접 확인): 영상 생성·편집(Runway·Kling·Veo·CapCut Pro·Descript), 목소리·효과음(ElevenLabs 등 — '치익' 효과음·목소리 품질 문제), 이미지·썸네일(Midjourney·Ideogram·Recraft·제미나이 이미지), UX/UI(Mobbin·Figma 유료 좌석·Figma Make·v0·Lovable·Stitch), 레퍼런스·스톡(Envato 등), 유튜브 분석(vidIQ·TubeBuddy), SEO(Ahrefs·Semrush 등 저가 대안 포함), 개발·배포(필요 없으면 '필요 없음').
- 도구마다: ① 우리 문제를 실제로 푸나(오늘 사장님이 짚은 것: 못생긴 화면·거슬리는 효과음·뻔함·영상 품질·유입) ② **AI 직원이 무인으로 쓸 수 있나**(API·MCP·커넥터·브라우저만 되는지) ③ 월 가격·연간 할인·무료 체험 ④ 상업 이용·AI 표시·저작권 약관 ⑤ 무료 체험·무료 등급으로 같은 과제를 돌린 결과(가입 없이 되는 범위만, 가입이 필요하면 '가입 필요') ⑥ 기대 효과(어떤 지표가 얼마나).
- 결론: '꼭 필요한 것' 상위 3~5개만, 월 합계 금액과 함께 결재함(approvals.md)에 한 줄씩 — **휴대폰에서 됨/PC만 · 가입 링크 · 누를 순서 · 결제 후 직원이 할 일**. 스꾸 계정·결제 수단과 섞이지 않게 파이어맵 계정(kygstar77@gmail.com)으로 가입하도록 적는다. 겹치거나 효과 없는 도구는 '안 삼'과 이유.
- 계정 만들기·결제는 직원이 하지 않는다(사장님 몫).

## [지시·긴급] 유튜브·카페 '틀에 박힌 자동 운영' 점검과 재설계 (사장님 10/01 23:51: "유튜브랑 카페는 잘 발전시키면서 운영하고 있나, 또 틀에 박히게 자동 입력된 대로 아무 생각 없이 하고 있는 거 아니겠지?")
- 순돌이 실측(10/01 23:51): 유튜브 구독 39명 며칠째 그대로, 공개 쇼츠 조회 22~609회(순자산 609·주담대 372·퇴직금 183·예금 179·금값 22), 롱폼 JEPQ·SCHD 34회. 쇼츠 제목이 "~얼마 나올까?/얼마일까?" 틀 반복. 쇼츠 설명 링크는 안 눌림(실사용 0). 카페 회원 2명(9/30)인데 하루 5편 발행이 계속 — **발행은 돌지만 성장은 없다 = 사장님 지적이 맞다.**
- 총괄: firemap-youtube-loop(콘텐츠 본부장) + firemap-brand-director + firemap-artist + firemap-copywriter + firemap-growth. 착수 지금, 보고 10/2 12:00. 결과 work/research/content-review-2026-10.md.
1. **잘된 것/안 된 것 분해:** 영상·카페 글 전부를 조회·시청 지속·클릭·댓글·구독 전환으로 줄 세우고, 잘된 상위 3개와 하위 3개의 차이(주제·첫 3초·제목 틀·썸네일·길이·시간대)를 경쟁 채널 상위작과 함께 표로.
2. **틀 깨기:** 같은 제목 틀·같은 화면 구성·같은 글 구조가 3번 넘게 반복된 것 목록 → 다음 편부터 금지하고 대체 형식 3개를 실험 장부에 등록(X-YT-*, X-CAFE-*).
3. **카페 재설계:** 회원 2명인 카페에 하루 5편을 계속 올릴 이유가 있나 — 카페 글이 검색으로 사람을 데려오는지(검색 유입·조회) 실측. 안 데려오면 편수를 줄이고 그 힘을 회원을 모으는 실험(질문 받기·계산 결과 공유·참여형 글 등, 네이버 약관·도배 금지 안)으로 돌린다. 사장님이 정한 '카페=커뮤니티 본진'은 유지하되 방법은 바꾼다.
4. **매주 일요일 콘텐츠 회고:** 위 표를 매주 갱신하고 실험 판정 → 규칙(RULES.md·rules.json) 교체. 숫자가 안 움직이면 '그대로 유지'는 실패로 센다.

## [지시] 증명 먼저 — 10/15 증명 기준 4개 (순돌이 10/01 23:55, 사장님: "애들이 진짜 너무 일 못하는 것 같아, 이러니 유료 구독 결정을 못 하는 거야, 희망이 안 보이니까")
- 유료 구독 결재는 아래 4개 중 3개를 무료 도구로 달성한 뒤에만 올린다(유료 도구 비교 조사는 계속하되 결재 줄은 보류, 무료 체험 A/B로 효과가 증명된 것만 예외).
| 기준 | 지금 | 10/15 목표 | 담당 |
|---|---|---|---|
| 사이트 외부 방문(봇·직원 제외) | 하루 약 46세션 | **하루 100세션** | firemap-growth + firemap-venture |
| 쇼츠 평균 조회(공개 후 48시간) | 약 230회 | **2배(460회)** | firemap-youtube-loop + firemap-copywriter |
| 쿠팡 | 클릭 0·주문 0 | **첫 클릭·첫 주문** | firemap-youtube-loop + firemap-product-dev |
| 핵심 화면 품질 | 통과선 6점 시절 화면 | **3개 화면 8점 + 토스 비교판** | firemap-brand-director + firemap-designer |
- 스프린트 점검이 매 회차 이 표의 '지금' 칸을 실측으로 갱신하고, 순돌이 대역이 뒤처진 칸에 지시를 낸다.

## [지시·긴급] 쇼츠 기계 생산 중지 → 편마다 경쟁 조사 (순돌이 10/01 23:56, 사장님: "경쟁사 조사도 하나도 안 하고 기계적으로 쇼츠 5개 만들고")
- 대기 쇼츠 5편: compete.md(같은 주제 최근 30일 경쟁 상위 5개·잘된 이유 3·우리만 다른 한 가지·첫 3초 문장) 채우기 전엔 공개 금지. 담당 firemap-copywriter(조사) → firemap-shorts(제작) → 예술가 뻔함 통과·편집 통과.
  - 접수: firemap-copywriter 23:58 — 절전표상 내 회차는 12:40뿐이라 23:56 회차는 건너뜀. **10/2 12:40 회차 1순위로 5편 compete.md 착수**(공개 금지라 그 전엔 나가는 편 없음). 롱폼 A-1·E-2·W-1 제목 일은 그 뒤.
- firemap-improve: shortsdaily.py·롱폼 업로드 경로가 compete.md(경쟁 5개 이상) 없으면 거절하는 코드 관문(10/2).
- 쇼츠는 하루 개수보다 편당 조회(증명 기준: 48시간 평균 2배)가 목표 — 조사가 끝난 편만 낸다. 못 채우면 그날은 0편도 괜찮다.
- 완료: [순돌이 검토] 무인 쓰기 — 10/02 00:03 순돌이(채팅 세션)가 `ytdesc_all.py apply` 실행: scV67BQvC4Q(5억이면 충분합니다) 설명 = 편집 원고 + 계산기 링크 + 첫 줄 쿠팡 대가성 문구 + link.coupang.com/a/hutbIQImpE, 유료 프로모션 표시 True 확인. 스크립트는 '되읽기 불일치'를 냈으나 실제 설명 첫 줄·링크는 들어감 — firemap-youtube-loop가 불일치 원인(공백·해시태그 등) 확인. 나머지 롱폼은 실험 규칙상 쿠팡 없음(f2_plan skip). F1(계산기 쿠팡 칸)은 운영 번들에 link.coupang.com 확인됨.
- 완료: [순돌이 검토] E-1 교체 10/02 00:37 — 삭제 대신: 옛 3Fn4VAUtPH0은 예약 취소·비공개 유지(삭제 안 함, 되돌릴 수 있음), 디에서판 e1_ds.mp4로 새 업로드 **-7SLlI1cea8**(예약 10/3 19:30 KST, 썸네일 e1c, 합성 표시). ytlong.py C9가 같은 편 교체본과 비교하지 않게 고침. uploads.jsonl 옛 줄은 replaced 표시. firemap-youtube-loop: 카페 글·쇼츠 관련 동영상 링크가 옛 ID를 가리키면 새 ID로.
- 완료: 멈춘 전체 회의(21:29~) 근무 10/02 00:37 순돌이가 중지.

## [지시·긴급] '치직'은 쉿소리가 아니라 **말 끝난 직후** 나는 소리 — 진단 다시 (사장님 10/02 01:32: "아니야, 유튜브 말 끝나고 치직 했는데")
- 어제 진단(TTS ㅅ·ㅊ 쉿소리, 디에서)은 사장님 설명과 다르다. 사장님은 **문장이 끝난 직후** '치직' 소리를 들었다 → 의심: 문장 wav를 이어 붙일 때 끝부분 클릭·팝(페이드 없음, 0 교차점 아닌 곳에서 자름, DC 오프셋, TTS가 끝에 내는 숨·잡음 꼬리, 무음 패딩 경계).
- 담당 firemap-video-producer(지금) + firemap-motion-designer(재검증). 대상: 공개 롱폼 전부(A-1 SCOI0DP-l-s 등)와 E-1 새 판(-7SLlI1cea8, 10/3 19:30 예약).
1. 실측: 각 문장 경계(말 끝 → 다음 말 시작) 앞뒤 300ms에서 급격한 샘플 점프·짧은 광대역 튐을 찾아 시각·크기 목록(work/video/clickscan.py로 도구화). 경쟁 영상 3편 같은 방식으로 비교.
2. 고침: 문장 wav마다 끝 10~30ms 페이드아웃·시작 5~10ms 페이드인, 0 교차점에서 자르기, DC 제거, TTS 꼬리 잡음 자르기 → lfvoice.py·렌더 틀에 기본값. ytlong gate에 '경계 클릭 0' 관문.
3. 확인: 고친 E-1을 경계 클릭 0으로 다시 렌더 → 10/3 19:30 전이면 -7SLlI1cea8 교체(삭제 말고 예약 취소·비공개, 새 업로드). A-1은 조회 보고 판단, 결정 decisions/log.md.
4. 교훈: 사장님 말("말 끝나고")과 진단이 맞는지 먼저 대조하지 않았다 → lessons.md.
  - 착수: firemap-video-producer 01:35
  - 완료: firemap-video-producer 02:30 — **원인 확정: 제미나이 TTS 응답 맨 끝에 붙어 오는 0.12~0.15초 광대역 잡음**(rms 약 2만, 4kHz 위 38%). 장 마지막 문장 바로 뒤에서 남(E-1 원본 응답 17개 중 13개, A-1·D-1도). 어제 진단(쉿소리)은 다른 소리였고, 디에서판 e1_ds(-7SLlI1cea8에 올라간 파일)에도 55.98초·96.00초 등에 그대로 남아 있음. ① 도구 work/video/clickscan.py(scan/fix) — 문장 wav 치직: E-1 31·A-1 27·D-1 10곳 → 전부 0(원본 _preclick/ 보관). 경쟁 3편(DIOzwBPlf_Q·IDwH4f-xA1g·J0hc2v8DzRo) 같은 검사로 21~24분에 0~4곳(사람 목소리 오탐 수준), E-1 옛 렌더는 9.7분에 37곳. ② lfvoice write()가 자동으로 지움(DC 제거·앞 8ms/뒤 25ms 페이드 포함), ytlong 관문에 '문장 wav 치직 0·무음 0' 추가, 같은 편 교체 업로드를 C1·C5에서 다른 편으로 세던 것 고침. ③ **E-1 새 판 video/out/e1_v3_ds.mp4** 렌더(길이 579.71초 같음, 치직 0, 쉿소리 -13.6dB, 관문 통과, meta.json video 바꿔 둠). 중간 사고: 첫 fix가 문장 wav를 전부 무음으로 만듦 → 업로드 전에 잡아 복구, 안전장치 넣음(lessons). ④ A-1(공개 중)은 교체 안 함(decisions). ⑤ **-7SLlI1cea8 교체는 [순돌이 검토]로 넘김** — PD 규칙상 무인 '이미 올린 영상 비공개 전환' 금지. 10/3 19:30 전에 해야 함: -7SLlI1cea8 예약 취소·비공개(삭제 말고) → uploads.jsonl 그 줄 replaced 표시 → `py -3.12 work/ytlong.py up work/research/longform/ep/E-1`(10/3 19:30 예약, 관문 지금 통과). 안 하면 치직 있는 판이 나간다.
- 완료: [순돌이 검토] E-1 치직 제거판 교체 10/02 02:32 — 새 업로드 **idc3JZOZukc**(e1_v3_ds, 10/3 19:30 KST 예약, 썸네일 설정). 옛 판 -7SLlI1cea8·3Fn4VAUtPH0 모두 예약 취소·비공개(삭제 안 함) 되읽기 확인. youtube-loop: 카페·쇼츠 링크가 옛 ID면 idc3JZOZukc로. 교훈: 첫 videos.update는 publishAt을 지우지 않는다 — publishAt:None을 한 번 더 보내고 되읽어 확인할 것.
- [추가 질문 → 콘텐츠 회고(10/2 12:00 보고)에 포함] 사장님 10/02 06:08: "우리는 부동산·주식·경제·정책·시사를 뉴스로 정리해 주는 유튜브가 제일 어울리지? 근데 연봉·자산 관련 카페 글이 조회수가 제일 높은 것 같지?" → 담당 firemap-youtube-loop·firemap-growth: ① 카페 글 전부 주제별(연봉·자산·부동산·주식·정책·시사) 조회수 실측 표 ② 유튜브도 같은 분류로 ③ '뉴스 정리형' vs '내 돈 얼마형(내 연봉·내 자산에 대입)' 성과 비교 → 채널 정체성 제안 1개. 추측 금지, 숫자로.

