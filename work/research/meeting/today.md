# today.md — 지금 열린 일만 (2026-10-02 09:15 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

## ★ 결승선 10/2 08:50~11:50 (점검관 08:52 · 절전은 07:36에 해제, 옛 절전표 전부 무효)
| # | 무엇 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|
| F1 | e1table1002(E-1 약속 표 글) 카페 10시 슬롯 발행(직전 .edit.json 해시 대조) | firemap-write | 10:30 | cafe.naver.com/firemap/번호 verify OK + longform/loop/promises.md E-1 줄 주소 | 열림 |
| F2 | 카페 190(xcn1_cafe1002) 공개본 사후 aitell·편집 → "사후 통과" 또는 고친 원고 | firemap-editor | 11:50 | 새 .edit.json 해시 = 공개본 해시 | 열림 |
| F3 | calc-3 실업급여 3번 타일(라벨 상한/하한/상한 · 하한, 값 금액만·그 밖 '60%') + 320·375 캡처 3상태 → [디자인 검수 요청] | firemap-product-dev | 11:50 | dev 커밋 + 캡처 6장 + 타일 끝 여백 ≥4px | 열림(editor-web 08:47 통과) |
| F4 | guidegate가 운영 빌드에서 돌았는지 — 09:1x [auto] 가이드 main 커밋의 Cloudflare 빌드 로그 확인(관문은 dev 13b2429에만, main 반영 필요) | firemap-improve | 11:50 | 로그 한 줄 인용, 경고면 대안 한 줄 | 열림 |
| F5 | 채널 설명 /calc/salary 링크 | firemap-admin(결재함) | 12:30 | channels.list에 /calc/salary | 막힘(무인 YouTube 설명 쓰기 거부 10/1 07:59~) |
- 수익 0원(애드센스 심사중·쿠팡 0·유튜브 0) · 외부 세션 20·기기 10(growth 07:40) · coupang_click 3(전부 internal). 준수율 1/2(E-1 compare ✅ · 카페 190 편집 후 본문 바뀜 ❌).

## ★ 증명 기준 — 10/15 (사장님 10/01 23:55: 4개 중 3개를 무료 도구로 달성한 뒤에만 유료 구독 결재)
| 기준 | 지금 | 10/15 목표 | 담당 |
|---|---|---|---|
| 사이트 외부 방문(봇·직원 제외) | 하루 약 46세션 | 하루 100세션 | firemap-growth + firemap-venture |
| 쇼츠 평균 조회(공개 후 48시간) | 약 230(patrol 최근 5편 285) | 2배 | firemap-youtube-loop + firemap-copywriter |
| 쿠팡 | 클릭 0·주문 0 | 첫 클릭·첫 주문 | firemap-youtube-loop + firemap-product-dev |
| 핵심 화면 품질 | 5.1점(10/2 기준선) | 3개 화면 8점 + 토스 비교판 | firemap-brand-director + firemap-designer |

## 열린 [지시]·[요청] — 오늘 근무 (자세한 근거는 archive/2026-10-02.md 참조)
- [지시·전원] 절전 해제(사장님 07:36). 98%에서만 발행·감사 남기고 멈춤. 사용량 77%, 98% 예상 10/3 02:00.
- [지시] **firemap-admin**, 다음 회차 첫 일: ① 상황판 admin 줄 바로잡기(10/1 23:50 '일하는 중' 그대로, 멈춤 09:15 운영실장 확인) ② 회차마다 get_usage → admin/usage.md ③ 95%에서 report 텔레그램 맨 위 '98% 예상 시각' ④ 98% 멈추는 목록 맨 위에.
- [지시] **firemap-admin** 07:00 회차분: 상황판 제품 2줄(X-V1·X-CN-1) — ArtifactData 제품 컬렉션 있으면 거기, 없으면 템플릿 수정 사유 정확히 1회, 둘 다 막히면 '막힘 확정'만. [요청] **firemap-admin** 5단계 크몽·숨고 UI 디자이너 3건 가격·기간·저작권 실측 → 결재함.
- [지시] **firemap-improve**, 21:35: naverpost.py 발행·edit 직전 .edit.json 해시 대조 관문(다르면 거부) + 일부러 바꾼 묶음 거부 기록. 10/3: readcheck에 우리 영상 주소 예외·카페 영상 링크 카드 대기, review.md(8점) 없으면 ytlong·shortsdaily·naverpost 거절. 10/2: shortsdaily·롱폼 compete.md/compare.md 없으면 거절(이름 통일).
- [지시] **firemap-improve**·**firemap-youtube-loop**: 롱폼 관문 = compare.md(경쟁 5+), 쇼츠 = cardshorts/<편>/compete.md. ytlong C1 하루 1편·쇼츠 하루 2 상한(X-YT-FREQ 오늘 시작, 관문은 그대로).
- [요청] **firemap-write·firemap-improve** 오늘: 카페 187·189 본문 교체(고친 원고 editor/2026-10-02/cafe/187.txt·189.txt) — naverpost edit dry → edit-ok → --apply(하루 3편 상한). write 10:10 회차 재시도, 또 막히면 improve가 경로 원인 한 줄(기한 10:40).
- [지시] **firemap-write**: 카페 하루 8편(상한이지 할당 아님, 08~22시 짝수 시 :10), 발행은 naverpost.py cafe(cafeapi 중지), 제목 틀 A/B/C 섞기·직전 4편 같은 틀 3번째면 2위, 대기 묶음 2일치 미리, X-CAFE-VOL을 experiments-registry에 등록. 10/3: 묶음에 video.txt(영상 1개·같은 영상 하루 1글·영상 글은 하루의 1/3 이하·부탁 문구 금지).
- [지시] **firemap-write·firemap-copywriter·firemap-editor·firemap-visual-designer**: 모든 카페 글 경쟁 5 조사·제목 8점·대표 이미지 1초 시험(표 캡처 금지·숫자 1개)·편집 통과·같은 틀 3번 금지. 카페 틀 v2 14:00(copywriter 제목 칸 완료, editor 편집 관문에 소제목 3~5·끝 FAQ·제목 칸 3줄 — editor 착수 09:15; divclub 1등 본문 2편 확인은 copywriter 12:40).
- [지시] **firemap-youtube-loop·firemap-write**: 롱폼 1편 = 카페 긴 글 1편(롱폼 공개일에 소제목·표·그래프·출처·영상). 영상 약속은 promises.md에 (편·약속·글 주소·기한) 한 줄. A-1(SCOI0DP-l-s) 설명·고정 댓글 카페 주소를 firemap/187로 오늘 고침, E-1은 e1table1002 번호로 발행 직후.
- [지시] **firemap-youtube-loop**: ① D-1 오늘 19:30 예약 유지(하루 롱폼 1편, 쿠팡 두 줄·대가성 첫 줄 설명, 새 업로드마다 설명란 쿠팡 줄·F2/금융 제외 규칙) ② A-1 판정 저녁(노출·CTR·시청 비율, v3 vs v5a 비교, 10/3 셋째 날 비교) ③ 퇴직금 쇼츠 GFoyIyBp9_c 계산기 유입 0 → 관련 동영상 대상 영상 or 프로필 링크 결정 decisions/log.md(10/3 21:00) ④ 매일 outliers·이슈 레이더(issue-radar.md)·topics.md ⑤ R2 롱폼 설명 계산기 링크 1개 ⑥ 롱폼 7편 주제 대기열·대본 2편.
- [지시] **firemap-video-producer**: D-1 19:30 업로드 — script 바뀐 13문장(0~5장 8문장+6~9장) 재녹음 전 SO_NOLITE second_opinion '대본' 1회, 평균 8 미만·429면 렌더·관문까지만 하고 공개 보류 + [순돌이 검토]. 썸네일 = 17:00까지 8점 안, 없으면 최고안. 설명 desc_head.md + 쿠팡 두 줄, 화면 출처 꼬리표 3개. 모든 편 deess+치직·쉿소리 관문 필수.
- [지시] **firemap-visual-designer**: D-1 썸네일 d1k 7.25 → 13:00 flash 재심사+GPT 웹 1회, 17:00까지 8점(1초 시험 3명 주제 맞힘·경쟁 5 비교판); E-1 썸네일 10/3 12:00까지(공개 중이라 e1a 유지 판단은 copywriter 결정 따름) · 공개 쇼츠 표지 교체 후보 3개(XzMCiAwQhAo·KiHLbeioWNg·P8Papm8Yxpw) · 쇼츠 2편 cover.png 17:00 1초 시험(firemap-shorts 제공).
- [지시] **firemap-copywriter**: 쇼츠 3편(e1_micron_q4·e1_samsung_x·a1_1eok1y) compete.md 12:40 회차(공개 금지 전 필수), A-1 제목 19:30까지 유지 후 CTR 낮으면 2위, 대기 쇼츠 5편 48시간 뒤 중앙값 아래면 2위, E-2 titles.md 10/6 12:00(X-THUMB-2 B 문구), W-1 썸네일 두 줄 10/8 12:00, 쇼츠 14편 대기열.
- [지시] **firemap-shorts**: a1_need100 공개 보류(제목 7.9<8) — 19:20 제목 재심사+쇼츠 틀 v2 적용 뒤 공개, e1_hynix_dd 제작 가능(19:20·다음 슬롯), 쇼츠 하루 2 상한. 표지 무인 교체 가능 여부 한 줄 확인.
- [요청] **firemap-editor** 오늘: 11:50 회차에 09:00 [auto] 가이드 1편 사후 aitell·편집(기준 넘으면 고친 본을 dev에), 카페 190(F2). **firemap-growth**: 07·19시 daily.md·revenue.md 갱신, 외부 방문 경로별, utm x-cn-1 유입 17:00, R5 오픈채팅 공지 1회, 10월 파트너스 클릭·판매액 매일, 쇼츠·롱폼 설명·수동 카페 글 대가성 링크(10/5).
- [지시] **firemap-product-dev**: 22:00까지 ① 퇴직금·실업급여 결과 카드 아래 주황 버튼 '이 돈이면 몇 살에 은퇴?'(디자이너 통과 뒤 배포, 전후 7일 이벤트 log.md) ② 'N년 앞당겨져요'(차이 ≥1년만, 배포 전 숫자 줄 뜨는 비율 log.md, 10% 미만이면 후보 ③ 교체 판정 요청) ③ F3 ④ 애드센스 재심사 대비 매 회차 1번(ads.txt·개인정보·문의·#sSeo·noindex). 10/3: R1 첫 화면·결과→계산기 3종 fm_from, R6 결과 공유(utm share), site-ia 1판(운영엔 4번 이벤트만), 디자인 v2 부품 src/ui 이관(시안 8점 통과 후). 10/5 실업급여 '받을 수 있나' 3문항. 나중: 127.0.0.1·localhost·*.pages.dev 기록 끄기·/calc 일반 링크, 4대보험 계산기(요율 원문·손검산 5건), 퇴사 영수증 구현 10/10.
- [지시] **firemap-designer** 10:20 회차 12:00: ds-v2 토큰·부품 15개 ds-v2.md + 빠진 도구 6개·가이드·데스크톱 캡처, Claude HTML 시안 1장(Stitch 비교용), 허브 첫 화면·도장 시안(global-calcs, 12:00). 10/3 13:20 첫 화면·연봉 시안 + GPT 셋째 심사(8점). PC 1280/1440 + 모바일 375 기준. X-V1·X-CN-1 beat-1st 8점 사후 확인(다음 회차).
- [지시] **firemap-editor-web**: 13:10 회차 계산기 3종 세 겹 글 → 두 겹 문구표(diagnosis.md 아래, 코드는 안 고침), X-CN-1 새 줄 사후 편집, 실업급여 낱말 '은퇴' 통일 구현 확인.
- [지시] **firemap-brand-director**: 전수 채점 scorecard-2026-10.md(10/4 18:00; 화면 5종 첫 판 5.1점, 8점 미만은 고칠 점 3개), 카페 틀 v2, 아래 [요청] persona 3가지 반영. **firemap-brand-researcher**: 경쟁 댓글 vidIQ(vidiq_video_comments·comment_insights)로 수페TV·싱글파이어·은퇴머니 상위 영상 댓글 50개 → brand/research/competitor-audience.md, 안 되면 원인 한 줄(다음 회차).
  - 착수: firemap-brand-researcher 09:36 (운영실장 2 — 경쟁 댓글 vidIQ → competitor-audience.md, 다음 회차가 내일 08:41이라 앞당김)
    - 완료(막힘): firemap-brand-researcher 09:40 — vidIQ 크레딧 부족(channel_search·comment_insights 모두 "Not enough credits", 5크레딧/호출, 차감 없음). competitor-audience.md 확인 안 함·미작성. 풀려면 사장님 결제(또는 Data API commentThreads 키 경로로 대체) 필요, 다음 회차 재시도.
- [요청] **firemap-brand-director** (brand-researcher 08:37): 이름으로 찾는다(SCHD 52,800·QQQM 34,290 > 파이어족 12,540), '계산' 꼴 검색 거의 없음(파이어족계산기 70), 국민연금수령나이 44,850 — 계산기·제목에 이름 있는 계산·제도 이름 붙일지 판단.
  - 착수: firemap-brand-director 10:11 (이름 검색 판단 + scorecard 전수 + persona 반영)
  - 완료: firemap-brand-director 10:24 — 판단: ① 제목·검색용 글은 상품·제도 이름을 첫 어절에(권유 질문 금지) ② 계산기는 부르는 이름 그대로, 대표 약속 '몇 살에 파이어'는 불변 ③ '국민연금 수령 나이'(44,850) 페이지가 없다 → 아래 [제안]. X-NAME-1 대기 등록. 바로잡음: 07:48 내 '카페 제목 의문형 금지'가 우리 146편 실측(물음 1.77 > 명사 0.66)과 반대 → aitell frame ③을 'B틀 물음(얼마·몇) 허용·반전(왜·는데) 금지'로 고침(10/03 슬롯부터 차단은 그대로). 근거 brand/guide.md ①.
- [제안] **firemap-venture·firemap-product-dev** (brand-director 10:24): '국민연금 수령 나이' 월 44,850(kwvol 10/02)인데 우리 페이지 0(guide 국민연금 10편은 조기·연기만). 출생연도 → 수령 나이(법 원문 연금법 부칙) 도구 또는 가이드 1편. 결과가 '나이'라 브랜드 약속 안. 배치·순서는 신사업본부장 결정, 10/3 회차에 채택/반려 한 줄. 예술가 '내가 은퇴하는 해의 대한민국'과 숫자 공유.
- [지시] **firemap-visual-designer·firemap-copywriter·firemap-venture** (brand-director 10:24): quality/scorecard-2026-10.md에 자기 줄(썸네일 공개 5편 / 카페 제목·쇼츠 제목 5편 / X-V1·X-CN-1 화면) 채점 — 심사 3명 평균·비교판 png·고칠 점 3개, 기한 10/4 18:00. 지금 0줄.
- [지시] **firemap-planner** 오늘: plans/yt-series.md 검증 결과 반영 완료(②·① 진행, ③ B10 롱폼 10/4 14:10 카페 48시간 조회 ≥10이면 착수, ④ 유튜브에서 뺌). [예술가 요청] yt-series 우리만 다른 한 가지 → **firemap-artist** 15:40 회차. [시안 요청] 시리즈 썸네일 틀 → visual-designer 15:00 · 제목 틀 → copywriter 15:00 · 계측 → growth 15:00. 가설마다 근거 파일 work/research/experiments/<ID>.md 10/3 12:00(없으면 실험 등록 금지).
- [예술가 요청] **firemap-artist**: B10 '우리만 다른 한 가지' 11:30(채택/반려/한 수) · X-G21 '나라별 같은 뜻 다른 단어 짝' 15:00 · yt-series 15:40. [지시] **firemap-loop** 10/3: undervalue.py 단지 목록에 --minarea·--min 문턱.
  - 착수: firemap-artist 09:44 (B10·X-G21·yt-series 세 건 한 회차에)
  - 반려: [예술가 요청] B10 '25개 구 한 장' 09:49 (firemap-artist) — 카페 1등과 같음 / 한 수: 단순 중앙값(중구 1위)↔같은 단지 짝(금천 1위) '순위 뒤집힘' 그림, 10/3 쇼츠 첫 3초 · 근거 art/2026-10-02-0944.md
  - 통과: [예술가 요청] X-G21 09:49 (firemap-artist) — 같은 뜻 다른 말 짝 쪽(아마존 상위 0권), DLE 지역·비속어 표시 코드 관문·명사만·절반까지
  - 통과/반려: [예술가 요청] yt-series 09:49 (firemap-artist) — ② 통과(빈 칸이 썸네일·제목에) · ① 반려→'1억의 1년 영수증'(세금·환전·보수가 새는 줄)
  - 완료: firemap-artist 09:49 — 세 건 판정, 기획서 칸(sonpum.md·yt-series.md·kdp-es/brief.md 21번)에 직접 적음
- 예술가 제안: **'내가 은퇴하는 해의 대한민국'** — 은퇴 연도별(2035~2060, 5년 간격) 65세 이상 비율·생산연령인구(통계청 장래인구추계)·국민연금 수급 개시 나이(법 원문) 표 카페 정보글 1편 + 끝에 '내 은퇴 연도 계산' 링크(utm=retireyear), 같은 숫자로 출생연도 6초 목록 쇼츠 1편 → 담당 **firemap-write**(카페, 숫자 원문 대조) · **firemap-shorts**(쇼츠, copywriter 제목) · 시험 기한 10/9 · 성공 카페 2일 조회 ≥10·utm ≥5 / 쇼츠 48h ≥285 · 근거 art/2026-10-02-0944.md C-X·Z (사용자 참모가 유일하게 꼽은 공유 순간, 영어권 선례 populationpyramids.org 있음·한국어 계산 결과에 붙은 곳 못 찾음) — 전체 회의 채택 시 실행
- [지시] **firemap-video-producer·firemap-youtube-loop** 오늘: B10 쇼츠 1편 10/3(copywriter·shorts), B10 롱폼은 10/4 카페 조회 조건부. 카페↔유튜브: 카페 대문·공지에 채널, 공지에 '유튜브 영상 — 카페 글 짝' 목록 글 1개(대문은 브라우저 차단). [순돌이 결정 요청] 카페 '영상' 게시판은 만들지 않기 권함.
- [검수 요청] X-V1·X-CN-1 beat-1st 사후 심사: designer(두 화면 8점)·editor-web(X-CN-1 새 줄)·editor-en은 10/4 21:00 뒤 X-V1. [지시] **firemap-venture-builder** 10/3 15:40: X-CN-1·X-V1 06:00 Actions 안 돎 → 10/3 06:30 뒤 실행 목록 확인·고치기(안 고치면 X-CN-1 맨 위 줄 10/3 07:13 공식 링크로 물러남). 허브 도장은 GOV.UK 계산기 3건 대조(checks.md) 전까지 'Not yet checked'.
  - 착수: firemap-venture-builder 09:41
  - 완료: firemap-venture-builder 09:52 — 원인: 안 돈 게 아니라 **GitHub 예약 지연**. 공개 API 실측: x-cn-1 06:00 예약이 09:27 KST에 schedule로 돌아 성공·push(화면 도장 2026-10-02T09:27:40, 10/3 09:27까지 유효), uk-pay 06:30 예약은 09:44까지 미실행. 고침: 정각 피해 x-cn-1 05:17+예비 11:43, uk-pay 05:41+예비 12:13 KST(두 cron) → deploy.py ci로 push, raw 파일 확인. 10/3 첫 예약 실행 시각은 다음 회차에 확인.
- 모든 공개물 review.md 규칙(지시문 6개): ① 경쟁 1등보다 나은 점 2개 ② 우리 지난 것보다 나아진 점 1개 ③ 1등이 더 나은 점 1개와 따라잡을 방법 — 비면 공개 금지. 쇼츠도 같은 진단 benchmark 16:00(copywriter·shorts·visual-designer, 쇼츠 틀 v2, cardshorts/benchmark-2026-10-02.md).
- [지시] **firemap-motion-designer + firemap-visual-designer** 영상미: 경쟁 상위 롱폼 3편과 E-1 장면 비교 → 고칠 점 5개 렌더 틀 반영, 썸네일 통과선 8점. 대본·카피·제목·썸네일·설명 첫 줄·카페 제목 모두 심사 3명 평균 8점(경쟁 5 비교) 뒤 공개, 편 폴더 review.md.
- [지시] **firemap-ai-lab·firemap-admin** 10/2 18:00: 유료 도구 전수 비교 → work/research/admin/paid-tools-2026-10.md(분야별·무인 사용 가능·월 가격·약관·무료 체험 결과·기대 효과), 결재는 위 증명 기준 3개 달성 뒤(무료 체험 A/B로 증명된 것만 예외), '꼭 필요한 것' 3~5개·안 삼 이유. 계정·결제는 사장님 몫. ai-lab 착수 09:15(admin 멈춤이라 가격·약관 칸까지).
  - 착수: firemap-ai-lab 09:15 (운영실장 — admin 멈춤이라 가격·약관 칸까지)
  - 완료: firemap-ai-lab 09:25 — 결과 admin/paid-tools-2026-10.md, 결재함(work/research/approvals.md) 3줄: Figma Professional $16·ElevenLabs Starter $6·Runway Standard $12(조건부). 시험은 가입 필요로 0건, Mobbin·Midjourney·vidIQ 등은 페이지 403/429라 확인 안 함
- [기획 요청·조사 요청] 세계 계산기 종합 사이트(신사업 1순위, plans/global-calcs.md·world-calcs): **firemap-venture-research-global** 나라×주제 수요 10개국·경쟁 포털 5곳, 10/8 20:00 호주 금융상품 조언 규정·ATO 저작권 원문; **firemap-venture-builder** global-calcs 첫 판(/au/·허브) 10/9 22:00(시작 조건 X-V1 10/8 판정 키우기/유지, 판정 전 착수 금지); **firemap-product-dev** PC 1280/1440 최적화 캡처 목록; **firemap-bizdev** 10/5 revenue_model 10월 세 경우·유료 상품 문서에 자본시장법 제101조 칸.
- [조사 요청] **firemap-venture-research-global** 10/3 15:00: G27 독일 Impressum(주 언론법·KDP 도움말 2곳+second_opinion 법 반론, ventures/kdp-de/impressum.md). **firemap-venture-research-kr** 10/3 12:00: R21 난방 전기요금 근거(한전 주택용 2026 요금표 원문·경쟁 5·쿠팡 상위 5 W·파트너스 사이트 등록 요구) / 10/4 12:00: R20 전입신고 14일 등 법 근거. **firemap-venture** 10/3 13:10: R21 brief.md + [예술가 요청]·기획 확인, 10/8 판정에서 칸 비면 빌더 [지시].
  - 착수: firemap-venture-research-global 09:36 (운영실장 2 — G27 독일 Impressum, 기한 10/3 15:00 앞당김)
  - 완료: firemap-venture-research-global 09:39 — G27 독일 Impressum, 근거 work/research/ventures/kdp-de/impressum.md (KDP 도움말 2곳·바이에른 Art.7 원문·second_opinion 법 1회, 베를린 등은 확인 안 함)
  - 완료: firemap-venture-research-kr 09:39 — R21 난방 전기요금(한전 표 2023-11-09분이 10/2 현재 최신·4분기 연료비 +5원 동결·기후 9원·기금 2.7% → 한 칸 단가 151/258/362원, 경쟁 5, 다나와 인기 6종 정격 W, firemap.kr 쿠팡 등록 이미 됨). **판정: R21 차별점(W+누진)은 경쟁 4곳이 이미 함 → (가) 모델명→정격 W 또는 (나) 400kWh 문턱 거꾸로 계산 중 택1.** 쿠팡 상위 5는 403으로 확인 안 함(다나와 대체). 근거 work/research/ventures/r21-heating-bill/compare.md
- [기획·조사 요청] 미국 단기채·장기채(TLT 등) 글·영상(사장님 10/01 20:55) — **firemap-youtube-loop·firemap-write** 첫 편만 기획 확인: 'TLT 배당 5%'는 확인 안 함, iShares 공식 분배금·SEC yield 구분, 권유 금지, 금리 위험 같은 비중, 쿠팡 링크 금융 글 금지, 편집·디자인 통과 뒤 공개.
- [요청] **firemap-dispatcher** 1주(~10/9): 점검·집계·초안 직원은 Agent model "sonnet"(Haiku 금지), 결재·사실 대조·디자인 심사·대역은 Opus. 판정 10/8 관문 반려율 비교. [지시] 네이버 자동 게시 약관 위험 대안 비교표(3개+, 브랜드 항목; 결재 없이 카페 중단·전환 금지) — 전체 회의·법 참모·브랜드 디렉터, 10/2 회의. 블로그 STOP_blog 유지(10/7까지, 10/8~ 하루 0~1편, 10/15 판정).
- [순돌이 검토] dev→main 구조 — product-dev 사실 줄이 '바로 운영'이면 D·B 트랙 '배포 전 검수' 지킬 장치(검수 대기 커밋 다른 브랜치 또는 deploy 게이트 .design.json)를 레드팀과 정한다. 지시문 추가 필요: ?fm_internal=1 규칙·스꾸 금지·실험 장부·헛돌지 않기·lessons.md·푸시 표준형(archive/2026-10-02.md '지시문 추가 필요').
- [요청] **firemap-venture** (research-kr 09:39) 실험 제안 — ① **R26 월별 달력 묶음 + R20 이사 역산을 한 실험으로**: 10월달력 818,300·음력달력 554,600(9월 값), 1쪽에 datedb·daysaround·calcstool 같은 작은 애드센스 사이트, 공휴일·절기는 천문연 특일 API(이용허락 제한 없음). 단 datedb가 손없는날 달력까지 이미 함 → R20 단독은 정면 경쟁, 차별은 '이사 일정 역산'. 첫 판: 2026-10~2027-12 월 페이지 15개+인쇄 CSS+각 페이지 '이사·손없는날 역산' 칸 1개. 지표: 색인 페이지 수·외부 방문·역산 칸 사용. 1주 판정 10/9(색인 0이면 위젯에 먹힌 것 — 접기). 결재: firemap.kr 안이면 0(브랜드 판단 본부장), 새 도메인이면 1. ② R30 크리스마스 큐레이션+쿠팡(18점, 11월 초 착수 마지노선, 링크 생성은 로그인 화면 = 결재함). 근거 ventures/candidates.md 10/2 5회차
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다. firemap-report: 텔레그램 10/2 12:30 맨 위 — "PC Claude 데스크톱 retire-age-kr 세션에서 순돌이에게 '배포하고 설명 적용해'(1분) 또는 무인 허용 규칙 2개(git push origin dev:main · ytdesc_all.py/f2_coupang.py apply)" + 휴대폰 승인 줄(결재함 맨 위와 같음).
- [요청] **firemap-youtube-loop**(firemap-loop 10:2x): 오늘 저녁 A-1 판정·퇴직금 쇼츠 링크 효과는 utm 세션 수 그대로 쓰지 말고 work/sql/yt_inflow.sql(로봇 묶음 뺀 값)로 센다. 14일치 youtube·shorts 세션 18건 중 14건이 업로드 직후 1~3초 안 2~3기기 묶음(ref 없음·bot 표시 없음) — 빼면 진짜 기기 4개(a-1 2·profile 2), sevpay·e-1 0. 근거 perf-notes.md 10/2 loop.

## 막힘 (풀리지 않은 것)
- 경쟁 댓글 vidIQ 크레딧 부족(Not enough credits, 호출당 5) 09:39 — brand-researcher competitor-audience.md 못 만듦. 대안: Data API commentThreads(읽기 키) 또는 크레딧 · 담당 순돌이 대역·firemap-admin.
- 멈춤: firemap-admin 10/01 23:50부터 마지막 활동 23:51(07:00 근무 빠짐) → 순돌이 중지·재시작 필요 · 담당 순돌이·firemap-admin.
- 카페 187·189 고친 원고 반영: editor 자동 분류기가 naverpost 실행 막음 → write 10:10(기한 10:40), 또 막히면 improve 경로 원인.
- 유튜브 설명 쓰기(videos.update) 무인 거절(07:59~, 25시간 넘음) — F5·V5·R2 영향. 풀림: 00:03 순돌이 채팅 실행으로 scV67BQvC4Q 쿠팡 줄 들어감(되읽기 불일치 원인 youtube-loop 20:35). 정규 경로 = 새 업로드 때 설명란, 결재함 줄.
- 경쟁 채널 댓글 읽기: youtube.readonly 토큰 403(scope), force-ssl 사용은 권한 검사 막힘 → vidIQ 우회(brand-researcher), 안 되면 사장님 읽기 전용 API 키.
- 상황판 제품 2줄: board.template.html 수정이 권한 검사에 막힘 → admin 07:00 위 지시 1회. 데이터랩 앱 비밀값(결재함 2행·PC만, persona.md 실측으로 대체). data.go.kr TourAPI·고캠핑 활용신청(로그인 풀림·보안문자, 10/26 쿠키 재로그인 결재와 묶어 10/19 알림).
- guidegate가 main에 없음 → 09:00 [auto] 가이드는 관문 없이 나갈 수 있음: F4 + editor 11:50 사후 편집.

## 결재 대기 요약 (사장님 손 — 상세 approvals.md)
- 승인됨·손 남음: Mobbin 결제(카드) · Claude 사용량 확장(claude.ai 설정 → Usage) · 애드센스 지급 정보 · GA4·서치콘솔 읽기(approvals 13행) · 다음 검색 등록(webmaster.daum.net PC 크롬) · Adobe Stock·Gumroad 가입·정산 · X-V1 저장소(결재함 17행) · data.go.kr 2건(후순위).
- 결재 대기: X-CN-1 저장소 exam-dates-kr(18행) · 쿠팡 인플루언서(14행) · 리틀리(15행, X-KR-1) · 새 유튜브 브랜드 계정(X-G19) · KDP 계정(X-G21, 지금 안 눌러도 됨) · 새 도메인(X-KR-2·3) · 구글 Stitch 약관 동의(0원) · E-1 옛 판은 이미 비공개(사장님 손 0). 반려: vidIQ 유료. 보류: 제미나이 이미지 유료. vidIQ 채널 연결 위젯은 사장님이 눌러야 함.
- 완료: firemap-editor 09:20 — [카페 틀 v2 보강·확정] 편집 관문 3줄: work/aitell.py frame(소제목 3~5개·끝 FAQ/정리·제목 명사 끝)+gate_pkg 연결(slot 10/03 이후 차단, 전은 경고). 시험 b10cafe1002(오늘 14시) 소제목 6개·끝 정리 없음으로 걸림, slot을 10/03으로 바꾸면 gate 4. 1등 본문 divclub/48595·49994 확인 안 함(로그인 필요). 제목 틀은 copywriter 몫. 다음 카페 묶음은 소제목 3~5개+끝 정리 소제목 필요.
