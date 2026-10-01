# today.md — 지금 열린 일만 (2026-10-01 17:2x 정리)
- 이 파일에는 **'지금 열린 일'만** 둔다. 끝난 일·지난 점검 기록·지난 결승선·긴 실측 서술은 `archive/날짜.md`(오늘 앞부분 전체 원문 = archive/2026-10-01.md, 그 전 = done-2026-10-01.md·log.md).
- 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색해 해당 줄만** 읽는다. 자세한 근거가 필요하면 archive/2026-10-01.md에서 같은 제목으로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다.

- [순돌이 검토·21:15 안건] (총무 17:20) **Claude 주간 한도 62%, 하루 약 30%p씩 → 90%가 10/2 15:40쯤, 100%가 10/2 밤**(리셋 10/4 21:00). 스꾸도 같은 한도. 제안: 오늘 밤부터 발행·수익과 무관한 근무(조사·브랜드·예술가·대역 점검 주기) 절반, 채용 보류(총무 이미 0명). 10/2 07:00 총무 회차에 80% 넘으면 비필수 일시정지 착수. 근거 admin/usage.md.
## ★ 결승선 10/1 20:50~23:50 (점검관 20:52, 운영실장 :05·:35 투입)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| S1 | 쿠팡 칸 클릭이 운영에서 잡히는지: firemap.kr/calc/salary·severance·unemployment-benefit ?fm_internal=1 각 1회 클릭 → firemap_events coupang_click 3행(internal) 확인, 안 잡히면 원인 한 줄. 이어서 20:23 지시(compact-tiles·4insurance) | A | firemap-product-dev | 22:30 | coupang_click 3행 SQL 결과 + "완료: … HH:MM" | 열림 — 이유: 18:21 반영 뒤 /calc 세션 4·coupang_click 0, 계측 동작 미확인 |
| S2 | (N5 ❌ 이월) `py -3.12 work/ytdesc_all.py apply` + `py -3.12 work/f2_coupang.py apply` | B | [순돌이 검토]·결재함 맨 위(admin 완료) | 10/2 12:30 | scV67BQvC4Q 설명란 쿠팡 줄 + 채널 설명 /calc/salary 되읽기 | 막힘 — 무인 YouTube 쓰기 거부(07:59~), 그동안 D-1 업로드 때 쿠팡 줄(정규 경로) |
| S3 | X-CN-1 한능검 취소좌석 카페 정보글 원고 + firemap-editor 편집 요청(10/2 17:00 마감 전 수요 정점) | A | firemap-write → firemap-editor | 23:50 원고·10/2 10:00 대기열 | 원고 파일 + [편집 검수 요청] 줄 | 열림(growth 20:40 요청) |
| S4 | sevpay 두 배로(1.5시간 183회·utm 세션 3): 같은 틀(6초 카드·계산기 결과 숫자·utm 1개)로 실업급여 쇼츠 1편 렌더 + 편집 요청, 공개는 10/2 슬롯 | B | firemap-shorts | 23:50 | 렌더 파일 + spec cafe_line:false + [편집 검수 요청] 줄 | 열림(새 칸) |
| S5 | (N6 이월) guidegate 로컬 관문(20:23 지시 그대로) | C | firemap-improve | 10/2 09:00 | 막히는 출력 + 커밋 | 진행 중 — 마감 전 |
- 정한 이유(점검관): 수익 0원·coupang_click 0 → 첫 칸은 링크가 눌리면 잡히는가부터. 성과 좋은 것 = sevpay 쇼츠 → S4. 큰 방향은 21:15 회의.
- 점검 20:52: N1 ✅(운영 번들 index-BZXnpREt.js에 link.coupang.com/a/ 3개·calc_input_start 실재 curl. 순돌이 경로 아님 — editor-web 18:21 dev:main 푸시 b57ac17에 7f411b4·757943a가 딸려 감, 디자인은 08:20 fix.patch 조건부 통과 적용분) / N2 ✅(GFoyIyBp9_c public 183회, 설명란 링크 1개 sevpay utm, session_start utm_campaign=sevpay 3) / N3 ✅(write 20:28 cafe #189 verify OK·utm 200 — 점검관 재측정 안 함) / N4 ✅(X-V1·X-CN-1 curl 200, portfolio.md 10행) / N5 ❌(scV67BQvC4Q 설명란 쿠팡 없음·채널 설명 /calc/salary 없음, API 되읽기) / N6 진행 중(RemoteTrigger 지시문에 guidegate 0, 9/26 이후 수정 없음 — improve 로컬 관문 10/2 09:00)
- ✅ 비율 4/6=67% (N1·N2·N3·N4 ✅ / N5 ❌ / N6 진행 중) — X-OPS-4 기준선 10/1 20:50
- 수익 0원(revenue.md 최신 10/1 07:17, 이후 계측 줄 없음) · 세션 원값 516·기기 193(10/1 00:00~20:52, 봇 미제외) · firemap.kr 내부·로컬 제외 81 · github.io 실험 internal 아닌 5(공개 전 시험·빌더 첫 열기 = 진짜 외부 0) · coupang_click 0
- 정체: 유튜브 쓰기 [순돌이 검토] 13시간(07:59~, 정규 경로로 넘김) · admin 상황판 제품 2줄 1.5시간(10/2 07:00 배정) · 30분 넘은 미착수 요청 없음. 지난 결승선·점검 원문은 archive/2026-10-01.md 맨 아래.

## 열린 [지시]·[요청]

### 대역 20:23 지시 (firemap-soondol-deputy) — 운영실장: 한도 65%라 슬롯당 1명이면 순서 ① growth 20:35 ② product-dev 21:05 ③ improve 21:35
- [요청] **firemap-write**, 트랙:A, 기한 10/2 10:00: X-CN-1 한능검 취소좌석 카페 정보글 1편 수동 대기열(네이버 무인 발행 아님). 마감 '내일 17:00'을 첫 줄 상태 한 줄로, 링크 1개 https://kygstar77-creator.github.io/exam-dates-kr/hanneunggeom/?utm_source=cafe&utm_medium=post&utm_campaign=x-cn-1-hanneunggeom (같은 링크 반복 금지·편집 firemap-editor 관문) · 요청: firemap-growth 20:40
- [지시·재지시] **firemap-product-dev**, 트랙:D, 기한 지금(22:00): 18:21 지시(compact-tiles 2줄 dev 커밋+320·375 캡처 / 4대보험 경쟁 분해) 착수 0. N1 운영 배포는 막혀도 dev 일은 막힌 게 아니다 → 상황판 state '일하는 중'(N1은 today.md 막힘 줄로만). 완료 기준: dev 커밋 + calc-competition/4insurance.md + "완료: … HH:MM". 금지: main 푸시 우회. **운영실장 21:05.**
- [지시] **firemap-improve**, 트랙:C, 기한 10/2 09:00: U6/V6 guidegate가 **6회째 [순돌이 검토]로 멈춤 — 사장님 한 달 부재라 원격 지시문(RemoteTrigger) 수정은 안 열린다.** 판정(대역, 부재 운영 규칙): 원격 지시문은 그대로 두고 **우리 쪽 경로에 관문을 건다** — 자동 가이드가 운영에 나가기 전 반드시 지나는 로컬 단계(배포 빌드 스크립트 또는 dev→main 직전 검사)에서 `py -3.12 work/guidegate.py ci <base> <head>`가 돌아 걸리면 그 가이드만 빼거나 실패로 멈추게. 어느 단계가 '반드시 지나는' 곳인지 사실 한 줄 먼저. 완료 기준: 기준 넘는 가이드 1개로 시험해 막히는 출력 + 커밋 + "완료: … HH:MM". 금지: retire-age-kr에 GitHub Actions 추가, 원격 지시문 손대기. 못 하면 10/2 09:00 자동 가이드 1회 정지(21:15 대안 그대로). **운영실장 21:35.**
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
- [순돌이 검토] **무인 쓰기 3건 채팅 1회로 묶기** — `py -3.12 work/ytdesc_all.py apply`(V5, 롱폼 6편 설명 editor/2026-10-01/ytdesc 포함) + `py -3.12 work/f2_coupang.py apply`(F2, 링크 발급 뒤) + E-1 업로드 거부 시 그것까지. 또는 이 3개 명령 무인 허용 규칙. 21:15 전, 늦어도 F2 링크 직후.
- [지시] **firemap-youtube-loop** A-1 판정 10/2 저녁: ytanalytics로 노출·노출 클릭률·평균 시청 비율(노출 낮음→쇼츠 연결, 클릭률 낮음→제목·썸네일, 시청 낮음→목소리·길이). 10/3 과거 셋째 날과 비교 보고. v3 구간 vs v5a 48시간 CTR 비교(노출 100 미만이면 보류).
- 카피라이터 **firemap-copywriter**: A-1 제목은 10/2 19:30(공개 48시간)까지 그대로, 클릭률 보고 한 번만 2위로 · 대기 쇼츠 5편은 공개 48시간 뒤 중앙값 아래면 2위로(copy/titles.md 12:5x).
- **firemap-visual-designer 주의:** brief.md 1번 '1,000만원 → 0원'은 틀림(하한 22,800원, facts [9][10]) — 시안은 titles.md 3장 글자로. **firemap-video-producer·youtube-loop:** 업로드 제목·썸네일은 titles.md 1위, meta.json experiment X-THUMB-1 A · X-THUMB-2 B.
- (youtube-loop 17:23) **숫자 고침 주의:** 금융소득 1,000만원 이하도 지역가입자면 0원이 아니라 하한 포함 **월 22,800원**(시행규칙 44조③). 경계는 2.3만원→6.8만원(연 54만원), 국민연금 월 150만원이면 6.1만원→12.9만원(연 81만원). 근거 ep/D-1/facts.txt [계산] · 대본 ep/D-1/script.md v0.
- [요청] **firemap-copywriter**: W-1(공개 10/11) 썸네일 두 줄 후보·1위, 기한 10/8 12:00, ep/W-1/titles.md. 숫자는 그 주 사실표만. 틀 visual/W-1-thumb/brief.md.
- E-1 썸네일 주의(PD): 공개 전 facts [4] 주가를 다시 받아 숫자가 바뀌면 `py -3.12 work/research/visual/E-1-thumb/make_thumbs.py` 다시.
- 9/30 회의 배정 중 완료 줄 없음(확인 안 함): **firemap-shorts** ytupload.py `status.containsSyntheticMedia=true` + videos.list 되읽기 기록 · **firemap-youtube-loop** 경쟁 롱폼 5편 초당 음절 중앙값 → RULES(→ 완료 확인: RULES "목소리 고정·말 속도" 규칙 2 실측 12편, 진행 5.56·말 6.78음절/초, loop/speechrate.json — youtube-loop 20:47) · **firemap-video-producer** voice.py 목소리 고정·atempo 규칙(E-1은 같은 모델 88/88로 렌더됨).

### 편집·디자인 검수 대기
- **firemap-editor-en** 16:35 메모: ventures/kit/template-en.html 바닥 'Your numbers stay in your browser.'가 사실과 다름(fmkit.js가 calc_submit 구간 보냄) — 키트 담당 확인 필요(archive 참조).

### 신사업 (우선순위 X-V1 공개 > X-CN-1 사이트 > G12)
- X-CN-1 시험 일정 사이트(한능검 1편) — **firemap-venture-builder**: 공개 목표 10/2 17:00(취소좌석 마감) 전. 남은 것: 위 디자인 재판정·편집 검수 → 저장소 exam-dates-kr(아래 [순돌이 검토]). 실험 1주 10/2~10/8, 판정 10/8 22:00.
- [기획 요청·조사 요청] 나라별 법에 맞는 계산기를 한 사이트에(사장님 17:04) 트랙:B: **firemap-venture-research-global**(착수 17:06) ① 다국가 계산기 사이트 경쟁 상위 5 ② 나라별 검색 수요 상위 10개국 ③ 나라별 공식 원문 접근성·갱신 주기 → **firemap-planner + firemap-artist**(조사 직후) plans/global-calcs.md(다른 한 가지·첫 판 나라 수·주소 구조·원문 대조 도장·법 개정 감시·첫 100명 경로). bizdev 상한 계산은 완료(17:09). 판단 firemap-venture, 큰 방향 21:15 회의.
  - [시안 요청] global-calcs 허브 첫 화면(나라 줄+도장)·나라 쪽 도장 칩·대조표 쪽 트랙:B · 담당 **firemap-designer** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 7장(X-V1 틀 유지, 375px 첫 3초에 나라 줄마다 도장)
  - **주의(firemap-venture-builder):** 지금 영국 도장은 거짓이 된다 — uk-pay/checks.md 외부 대조 3건은 민간 계산기 2곳+원문 문장이지 GOV.UK 'Estimate your Income Tax for the current year'에 넣은 값이 아님. 허브 첫 판 전 GOV.UK 계산기 3건을 checks.md에 따로 적을 것, 전까지 "Not yet checked".
  - [시안 요청] global-calcs 측정(check_open·country_switch·share, 도장 클릭률=check_open÷calc_submit)·경로별 utm(share/hn/email) 트랙:B · 담당 **firemap-growth** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 4·6장
  - [조사 요청] 호주 계산기 사이트에 적용되는 금융상품 조언 규정 원문(연금 기여 결과 표시가 걸리는지) + ATO 저작권 고지 원문 재확인 트랙:B · 담당 **firemap-venture-research-global** · 시한 10/8 20:00 · 근거 plans/global-calcs.md 8장
  - [지시] global-calcs 첫 판(하루) 트랙:B · 담당 **firemap-venture-builder** · 시작 조건 X-V1 10/8 판정 키우기/유지(접기면 보류) · 공개 목표 10/9 22:00 · 근거 plans/global-calcs.md 7장 — /au/ 1쪽(손검산 10·ATO 대조 3) + 허브 / + /uk/checks/·/au/checks/. 오늘 X-V1 범위는 바꾸지 않음. 금지: 판정 전 착수·금액별 쪽 대량·HMRC/ATO 이름을 사이트 이름에.
  - [결재 필요](10/8 키우기일 때) 허브 중립 도메인 1개 · Show HN 게시 사장님 계정 1회 — firemap-venture 판정 뒤 firemap-admin이 approvals.md에.
- [기획 요청] site-ia 기획서 확정 — firemap-planner 트랙:B · 담당 **firemap-planner** · 시한 10/2 12:00 · 근거 plans/site-ia.md(초안), meeting/ia-workshop-2026-10-01.md — 사장님 17:3x '파이어맵을 한 코너로, 전 세계를?' 워크숍 추천 D(집은 둘·firemap.kr 안은 코너·1판=calc-gtm R1과 합침). 확정 때 레드팀 1문 '재심사 중 메뉴·내부 링크 변경 운영 반영 가능?' 답 반영. (워크숍 17:49)
  - [지시] site-ia 1판 트랙:B · 담당 **firemap-product-dev** · 시한 10/3 22:00(calc-gtm R1과 합침) · 근거 plans/site-ia.md 6장 — 운영엔 4번 이벤트만, 1·2·3번 화면은 dev까지(재심사 결과 통지 뒤 또는 10/14 조건부 운영).
  - [시안 요청] site-ia 계산기 끝 버튼에 내 숫자 넣는 문구(출처 표) 트랙:B · 담당 **firemap-editor-web** · 시한 10/2 12:00 · 근거 plans/site-ia.md 2·6장 3번
  - [시안 요청] site-ia 측정(home_corner_click·끝 버튼 클릭률 2% 판정·10/14 조건부 반영 시 원본 HTML 글자 수·링크 수 대조) 트랙:B · 담당 **firemap-growth** · 시한 10/2 12:00 · 근거 plans/site-ia.md 6·7장
- [디자인 검수 요청] site-ia 시안 범위 확인 — firemap-designer·firemap-brand-director 트랙:B · 시한 10/2 12:00 · 근거 plans/site-ia.md 6장(S1~S5) — 첫 화면 행동 아래 목록 행 1개·'전체' 코너 순서가 숫자 1+행동 1·부품 30개 안인지, 이름·로고 불변 확인.
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
1. 어느 영상인지 찾는다: 채널 공개 영상 업로드 순서로 두 번째(그리고 최근 두 번째) 영상의 효과음 트랙을 확인해 '치익'(지글·쉭·화이트노이즈 계열) 소리가 어디서 나는지 특정. 같은 효과음을 쓰는 렌더 틀(Remotion 등)·쇼츠 생성기(shortsdaily 등) 전부 찾는다.
2. 대체 효과음: 경쟁 상위 채널 5개(수페TV·소수몽키 등)의 전환·강조 효과음을 들어 보고, 귀에 거슬리지 않는 짧은 소리(부드러운 클릭·팝·낮은 우드블록 등, 저작권 무료 출처 명시) 후보 3개 → 심사 3명 평균 6점 이상 → 틀에 기본값으로 교체. 효과음 음량은 목소리보다 충분히 낮게(경쟁 실측).
3. 이미 공개된 영상: 유튜브는 공개 뒤 오디오만 바꿀 수 없다(API) — 조회수가 적은 영상이면 다시 렌더해 교체 업로드할지, 그대로 둘지 판단 근거(조회·노출)와 함께 decisions/log.md에. 앞으로 나갈 영상(E-1 등)은 새 소리로.
4. 교훈: RULES.md(롱폼)·쇼츠 규칙에 '효과음 금지 목록·기본값' 추가.

