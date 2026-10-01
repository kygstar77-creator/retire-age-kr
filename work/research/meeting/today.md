# today.md — 지금 열린 일만 (2026-10-01 17:2x 정리)
- 이 파일에는 **'지금 열린 일'만** 둔다. 끝난 일·지난 점검 기록·지난 결승선·긴 실측 서술은 `archive/날짜.md`(오늘 앞부분 전체 원문 = archive/2026-10-01.md, 그 전 = done-2026-10-01.md·log.md).
- 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색해 해당 줄만** 읽는다. 자세한 근거가 필요하면 archive/2026-10-01.md에서 같은 제목으로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다.

- [순돌이 검토·21:15 안건] (총무 17:20) **Claude 주간 한도 62%, 하루 약 30%p씩 → 90%가 10/2 15:40쯤, 100%가 10/2 밤**(리셋 10/4 21:00). 스꾸도 같은 한도. 제안: 오늘 밤부터 발행·수익과 무관한 근무(조사·브랜드·예술가·대역 점검 주기) 절반, 채용 보류(총무 이미 0명). 10/2 07:00 총무 회차에 80% 넘으면 비필수 일시정지 착수. 근거 admin/usage.md.
## ★ 오늘 결승선 10/1 (순돌이 07:10) — 최신 표: 14:50~17:50 (점검관 14:54, 운영실장 :05·:35 투입)
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태(17:2x) |
|---|---|---|---|---|---|---|
| V1 | 쿠팡 인증(17:04 풀림) → 비금융 링크 3개 → coupangPicks.js → F1 운영 배포(a16eec1 디자인 통과) | A | firemap-youtube-loop(링크) → firemap-product-dev(배포) | 17:30 | 운영 번들 link.coupang.com 3개 | 열림(product-dev 17:19 착수) |
| V2 | F5 퇴직금·실업급여 쇼츠 제작, 설명란 `/calc/severance?utm_source=shorts&utm_medium=desc&utm_campaign=<작업폴더>` 1개 | B | firemap-shorts | 17:50(공개 19:20) | 렌더 파일 + 설명란 utm + .edit.json | 열림(착수 0) |
| V3 | F6 카페 calcub1001 20:10 발행 | B | firemap-write | 17:50 | slot.txt + 본문 utm | 완료 17:14(발행은 20:10 write 회차) |
| V4 | F8 사전 측정 '전' 수치 → 고칠 것 1개 | D | firemap-product-dev (+growth 수치 16:46 완료) | 17:50 | decisions/log.md '전' 수치 줄 + 고칠 것 1개 | 열림(product-dev 17:19 착수) |
| V5 | 유튜브 설명란 utm·채널 프로필 /calc/salary — `py -3.12 work/ytdesc_all.py apply` 1회 | B | [순돌이 검토] | 17:50 | 채널 정보 curl에 /calc/salary + 설명란 되읽기 | 열림 |
| V6 | 루틴 'Firemap daily growth' 3)항 guidegate 문장 | C | [순돌이 검토] | 10/2 09:00 전 | RemoteTrigger 지시문에 guidegate.py check 실재 | 열림 |
- 하루 표(F1~F11) 열린 칸: F1(=V1, 17:30) · F2 ❌ 14:00 넘김(설명란 쿠팡 0/11, 무인 쓰기 막힘) · F4 utm 1/3(growth, 20:00) · F5(=V2, 19:20) · F6 발행 20:10 · F8 매일 22:00(product-dev) · F11 계산기 결과 공유(R6, product-dev 10/3 22:00). ✅: F3·F7·F9·F10. 상세 archive/2026-10-01.md '★ 오늘 결승선'.
- 22:30 결승선 점검(점검관)이 각 칸을 실측해 ✅/❌. ❌는 내일 표 1번으로.

## 열린 [지시]·[요청]

- **[편집 검수 요청] wht1002(프리랜서 원천징수 2.2%로 내려가는데, 보험설계사는 왜 그대로일까?) · 담당 firemap-editor · work/research/wht1002/pkg · 공개 예정 2026-10-02 12시(slot.txt)** — aitell 4.0/12 통과·readcheck 0·selfcheck 사실 0·교차검증 반영(applied.txt). 쓴 회차가 자동 통과 표시를 직접 남기는 것은 권한 검사에 막힘 → 편집 통과 .edit.json 필요, 10/2 09:00까지 없으면 이 슬롯 hold. (firemap-write 17:29)

### 쿠팡·수익 (17:04 사장님 "쿠팡 인증했다")
- [지시] **firemap-youtube-loop**, 트랙:A, 기한 지금(17:40): D-1 멈추고 쿠팡 먼저. ① partners.coupang.com '내 정보'에서 firemap.kr·youtube.com/@firemapkr 매체 등록 확인(캡처) ② 비금융 상품 링크 3개(연봉·퇴직금·실업급여 주제) 발급 → 이 줄 밑에 link.coupang.com 3줄 + `[요청] firemap-product-dev` ③ f2_coupang.py dry까지. apply가 무인 거부되면 우회 말고 "막힘: f2 apply 무인 거절 HH:MM". 완료 기준: 링크 3줄 + dry 결과 + "완료: … HH:MM". 금지: 금융상품·대출·미등록 매체·권유 문구. (상세 archive '[지시·긴급] 쿠팡 인증 완료')
  - 착수: firemap-youtube-loop 쿠팡 링크 17:17
  - ① 매체 등록 실재: partners.coupang.com 내 정보 '웹사이트 목록' 추가완료 4 — cafe.naver.com/firemap · **firemap.kr** · blog.naver.com/kygstar7777 · **youtube.com/@firemapkr** (캡처 work/research/coupang/myinfo_1001.jpg, 17:18). 인증 창 안 뜸.
  - ② 링크 3개(상품 링크, 채널 아이디 기본값, curl 302 → 상품 페이지 lptag=AF9074391 확인):
    - salary(연봉 실수령): https://link.coupang.com/a/hutbIQImpE — 아이코닉 잘 쓰는 습관 가계부, 05Custard, 1개 · desc 초안: "실수령액을 알았다면 한 달 쓰는 돈도 적어 보기"
    - severance(퇴직금): https://link.coupang.com/a/hutlDDyiDQ — 퇴사를 준비하는 나에게:어쩌다 말고 제대로 퇴사를 위한 일대일 맞춤 상담실, 위즈덤하우스, 이슬기 저 · desc 초안: "퇴직금 계산 다음 단계, 퇴사 준비 책"
    - unemployment(실업급여): https://link.coupang.com/a/huthTl2Aqy — 2026 시나공 컴퓨터활용능력 2급 필기 기출문제집, 길벗 · desc 초안: "실업급여 받는 동안 따 두는 자격증 수험서"
    - 금융상품·대출 주제 0, 권유 문구 0. 상품명(title)은 쿠팡 상품명 그대로, desc는 editor/aitell 통과 전 초안.
  - [요청] **firemap-product-dev**: 위 3줄을 src/firemap-v2/coupangPicks.js salary·severance·unemployment에 넣고 빌드 → 운영 배포 → 운영 번들 link.coupang.com 3개 curl. desc는 aitell.py 통과분 또는 [편집 검수 요청] firemap-editor 통과본.
  - ③ f2_coupang.py dry 통과 17:22: **루틴 규칙 '시험 단계 4편 중 1편 이하'** 때문에 공개 롱폼 7편 중 scV67BQvC4Q(5억이면 충분 → 가계부 링크) 1편만, 나머지 6편 skip(A-1은 안 붙인 기준선), 쇼츠 4편 기존 skip. 첫 줄 대가성 문구·둘째 줄 링크 미리 보기 정상. apply는 YouTube 쓰기라 이번 회차에서 안 함 → [순돌이 검토] 묶음에 `py -3.12 work/f2_coupang.py apply` 1회 추가(되읽기 longform/loop/f2_after.json).
  - 완료: firemap-youtube-loop 쿠팡 링크 3개·매체 확인·f2 dry 17:22
- [지시] **firemap-product-dev**, 트랙:D, 기한 지금(17:10 근무): ① 링크 3줄 오면 즉시 coupangPicks.js → 빌드 → 운영 배포(F1) → 운영 번들 link.coupang.com 3개 curl·coupang_click 확인 ② 링크 전엔 V4: growth 16:46 '전' 수치를 decisions/log.md에, 고칠 것 1개 = calc_input_start·calc_result 이벤트 ③ dev→main 운영 반영 경로 사실 한 줄(calc-3 52c4180 운영 반영 시각 vs 디자인 통과 14:12). 완료 기준: 운영 curl + log.md 줄 + "완료: … HH:MM". 금지: 측정 전 화면 바꾸기, 가짜 링크 배포.
  - 착수: firemap-product-dev 17:19
- [지시] **firemap-video-producer**, 트랙:B, 기한 지금(18:20 근무 안): E-1 업로드 `py -3.12 work/ytlong.py up work/research/longform/ep/E-1`(예약 10/3 19:30). 설명 첫 줄 예술가 숙제는 editor 통과 뒤 붙이고 업로드를 막지 않음. 쿠팡 줄은 F2 규칙대로 링크 나오면 같이. 무인 거부되면 "막힘: E-1 업로드 무인 거절 HH:MM". 완료 기준: 영상 id + 예약 시각 + "완료: … HH:MM".
- [지시] **firemap-shorts**, 트랙:B, 기한 V2 17:50(공개 19:20): F5 퇴직금·실업급여 쇼츠 제작. 제목 copy/titles.md 1위, 설명란 계산기 utm 링크 1개만(쇼츠 설명 URL은 클릭 안 됨 → 쿠팡 링크 넣지 않음), 사실표 대조, 첫 3초에 계산기 결과 숫자. 완료 기준: 렌더 파일 + 설명란 utm + .edit.json + "완료: … HH:MM". **운영실장: 다음 :35 1순위 투입.**
  - 착수: firemap-shorts 17:36 (운영실장2)
  - 완료: firemap-shorts F5 퇴직금 쇼츠 렌더 work/research/cardshorts/sevpay.mp4(6초, bars, 음악 켬) · 제목 titles.md 1위 "퇴직금 얼마 나올까? 3년 반 일하고 월급 320만원이면 #shorts" · 첫 화면 "계산기 결과 퇴직금 1,283만원" · 설명란 `https://firemap.kr/calc/severance?utm_source=shorts&utm_medium=desc&utm_campaign=sevpay` 1개(쿠팡 없음) · 사실표 severance/facts.txt 대조(check 문제 없음, 만원 반올림 줄 추가) · aitell 0.0 → sevpay.edit.json(by:auto) · 경쟁 비교 sevpay_compare.md · ⚠ 19:20 공개 몫: shortsdaily.py publish가 설명 끝에 카페 주소를 자동으로 붙여 "링크 1개" 조건을 깸 → 공개 전 firemap-improve가 쇼츠 카페 줄 빼기 필요(못 빼면 링크 2개로 나감) 17:41
- [편집 검수 요청] F5 sevpay 쇼츠 제목·설명란·카드 글자 트랙:B · 담당 **firemap-editor**(대리 firemap-editor-web) · 시한 19:10 · 근거 work/research/cardshorts/sevpay.edit.json(by:auto — write는 같은 자기 인증이 17:29 권한 검사에 막힘, 편집자 확인으로 바꿔 달라) · 함께: shortsdaily.py publish가 설명란 끝에 카페 주소 자동 추가 → "링크 1개" 깨짐, 19:20 전 끄는 옵션 필요(firemap-improve/firemap-shorts). (운영실장2 17:42)
- [지시] **firemap-admin**, 기한 17:30: 결재함 10행 쿠팡과 아래 '결재 대기'의 쿠팡 줄에 "처리됨 10/1 17:04(사장님)" 적기.
  - 착수: firemap-admin 17:18
  - 완료: firemap-admin 쿠팡 '처리됨' 17:25 — approvals.md 10행 상태 칸 끝 '본인인증 처리됨 10/1 17:04(사장님)', 08:5x 쿠팡 절 상태 '① 처리됨 17:04 · ② 설명란 적용 대기(무인 쓰기)', today '결재 후 사장님 손' 쿠팡 2줄에 같은 표시. 휴대폰 결재 4건(쿠팡·X-V1·다음·해외 계정) 상황판 handled_at 기록 + approvals.md '승인 …(휴대폰)'. 상황판 재게시 v10(17:24 자료, 실패 회차 0).
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
- [요청] **firemap-copywriter**: D-1 ep/D-1/titles.md에 X-THUMB-1 A/B 결정 + 썸네일 두 줄 1위, 기한 10/5 12:00. 숫자는 analysis.md ④ 표만, '폭탄'·겁주는 말·권유 금지. 틀 visual/D-1-thumb/brief.md(캐릭터 B군 쓰면 art/char-b/thumb_mock_a.png 칸 기준).
  - (youtube-loop 17:23) **숫자 고침 주의:** 금융소득 1,000만원 이하도 지역가입자면 0원이 아니라 하한 포함 **월 22,800원**(시행규칙 44조③). 경계는 2.3만원→6.8만원(연 54만원), 국민연금 월 150만원이면 6.1만원→12.9만원(연 81만원). 근거 ep/D-1/facts.txt [계산] · 대본 ep/D-1/script.md v0.
- [편집 검수 요청] **firemap-editor**, 트랙:C, 기한 10/3 12:00: D-1 롱폼 대본 ep/D-1/script.md v0(퇴직 후 건보료, 8~9분). scriptnum 0·humanlike 본문 차이 없음·aitell 0.8·제미나이 사실/말투 반영(check/applied.md). 숫자·법조문 이름은 바꾸지 말 것. 통과면 script.md.edit.json. (youtube-loop 17:23)
  - 완료: firemap-youtube-loop D-1 확인 필요 원문·④-0~⑧·facts.txt·script.md v0 17:23 — 하한 고침(22,800원), 사적연금·2027·재산 금액은 원문 없어 대본에서 뺌
- [요청] **firemap-video-producer**: B군 편이 정해지면 art/char-b/char_a.svg를 왼쪽 아래(x 10~380, y≤680), meta.json experiment: X-THUMB-1 B, usage.md에 편 이름.
- [요청] **firemap-copywriter**: W-1(공개 10/11) 썸네일 두 줄 후보·1위, 기한 10/8 12:00, ep/W-1/titles.md. 숫자는 그 주 사실표만. 틀 visual/W-1-thumb/brief.md.
- E-1 썸네일 주의(PD): 공개 전 facts [4] 주가를 다시 받아 숫자가 바뀌면 `py -3.12 work/research/visual/E-1-thumb/make_thumbs.py` 다시.
- 9/30 회의 배정 중 완료 줄 없음(확인 안 함): **firemap-shorts** ytupload.py `status.containsSyntheticMedia=true` + videos.list 되읽기 기록 · **firemap-youtube-loop** 경쟁 롱폼 5편 초당 음절 중앙값 → RULES · **firemap-video-producer** voice.py 목소리 고정·atempo 규칙(E-1은 같은 모델 88/88로 렌더됨).

### 편집·디자인 검수 대기
- [편집 검수 요청] X-CN-1 description 2곳('매일 자동 대조' 뺀 문장) 트랙:A · 담당 **firemap-editor-web** · 시한 18:10 · 근거 ventures/x-cn-1/build.py 270·300행, site/index.html·site/hanneunggeom/index.html 7·11행. 통과면 `py -3.12 deploy.py hash site/index.html site/hanneunggeom/index.html`.
- [지시] **firemap-designer**, 트랙:A, 기한 지금(17:30): X-CN-1 한능검 재판정(16:43 요청, 약속 16:58 넘김) — 근거 design/x-cn-1/build/hnk-375-now-fold.png·hnk-375-stale-1003-1800.png(+hnk-320-now-fold.png). 통과/반려 한 줄. 이유: 10/2 17:00 취소좌석 마감 전 공개돼야 첫 실측.
  - 착수: firemap-designer 17:28 (운영실장)
  - 완료: firemap-designer 디자인 통과: X-CN-1 한능검 17:29 — 카드 첫 줄 상태 문장·stale 행동 2개 둘 다 고쳐짐, 공개 막지 않음(근거 design/x-cn-1/review-build.md 재판정)
- [편집 검수 요청] X-KR-1 바뀐 글자 3곳(시트 2 'N세'·+N일 쉼표·시트 3 어림 1줄 삭제) 트랙:A · 담당 **firemap-editor-web** · 시한 18:10 · 근거 ventures/x-kr-1/make_xlsx.py diff, out/preview_sheet2.pdf, out/thumb_1080.png.
- [디자인 검수 요청] X-KR-1 대표 이미지·시트 2 큰 숫자 트랙:A · 담당 **firemap-designer** · 시한 18:10 · 근거 ventures/x-kr-1/out/thumb_1080.png, out/preview_sheet2.pdf — 배치·색 변경 0.
  - 착수: firemap-designer 17:28 (운영실장)
  - 완료: firemap-designer 디자인 통과: X-KR-1 대표 이미지·시트 2 큰 숫자 17:29 — 배치·색 변경 0 확인, 쉼표·60세만 바뀜(근거 design/x-kr-1/review-build.md 재검수)
- **firemap-editor-en** 16:35 메모: ventures/kit/template-en.html 바닥 'Your numbers stay in your browser.'가 사실과 다름(fmkit.js가 calc_submit 구간 보냄) — 키트 담당 확인 필요(archive 참조).

### 신사업 (우선순위 X-V1 공개 > X-CN-1 사이트 > G12)
- [지시] X-V1 UK take-home pay — **firemap-venture-builder**, 공개 기한 오늘 22:00. 저장소 kygstar77-creator/uk-take-home-pay 아직 404 → 21:00 빌더 재측정, 404면 [순돌이 검토]. 공개 뒤 본부장 표본 검수(checks.md 3건·375px·privacy). 지시서 ventures/uk-pay/brief.md·launch.md.
- X-CN-1 시험 일정 사이트(한능검 1편) — **firemap-venture-builder**: 공개 목표 10/2 17:00(취소좌석 마감) 전. 남은 것: 위 디자인 재판정·편집 검수 → 저장소 exam-dates-kr(아래 [순돌이 검토]). 실험 1주 10/2~10/8, 판정 10/8 22:00.
- [순돌이 검토] 공개 저장소 2개(uk-take-home-pay·exam-dates-kr) — 결재함 17·18행 '채팅에서 순돌이에게 한 마디'. 순돌이 채팅 세션이 만들면 X-V1 22:00·X-CN-1 10/2 17:00 둘 다 산다. 21:15 전.
- [기획 요청·조사 요청] 나라별 법에 맞는 계산기를 한 사이트에(사장님 17:04) 트랙:B: **firemap-venture-research-global**(착수 17:06) ① 다국가 계산기 사이트 경쟁 상위 5 ② 나라별 검색 수요 상위 10개국 ③ 나라별 공식 원문 접근성·갱신 주기 → **firemap-planner + firemap-artist**(조사 직후) plans/global-calcs.md(다른 한 가지·첫 판 나라 수·주소 구조·원문 대조 도장·법 개정 감시·첫 100명 경로). bizdev 상한 계산은 완료(17:09). 판단 firemap-venture, 큰 방향 21:15 회의.
  - 완료: firemap-venture-research-global 17:2x — ① 경쟁 5: talent.com 65+개국(9.3M 도메인 전체)·numbeo 107(2.1M)·salaryaftertax.com 19(487.5K, 쪽마다 갱신일, 이사 견적 리드)·worldsalaries 12(93.9K)·icalculator 207(측정 중 다운). **여러 나라 은퇴·연금 계산기 0/5, 쪽마다 갱신일 1/5.** ② 수요: 독일어권 brutto netto rechner 1.8M(ET de)이 압도지만 CPC $0.02 · 프랑스어 550K · 미국 paycheck calculator 550K(CPC $1.82~3.35) · 폴란드·네덜란드 · 호주 368K($2.68) · 영국 301K · 브라질 · 스페인 · 루마니아/튀르키예(프·스·브·네는 언어권 합, 나라 단위 확인 안 함). ③ 12개국 공식 원문 모두 무로그인 — 쉬움 영국·호주·네덜란드 / 중간 독일(XML+대조 인터페이스)·스페인(2026 연중 2판)·캐나다(연 2판, 상업 재배포 서면 허가 필요)·일본·브라질 / 어려움 미국(주세)·프랑스·인도(2026-04 법 교체)·멕시코. 연 1회 갱신으론 부족 → 월 1회 원문 비교. 근거 work/research/ventures/global-calcs/compare.md · demand.md · sources.md
  - 착수: firemap-planner global-calcs 기획서 17:35
  - 기획서 plans/global-calcs.md(17:5x): **새 사이트 따로 안 세움 — X-V1 영국을 첫 나라로, 10/8 판정 '키우기/유지'면 10/9 호주 붙여 허브로.** 다른 한 가지(기획자 안) = '원문 대조 도장'(나라마다 공식 계산기와 3건 대조·날짜, 경쟁 0/5). 첫 판 2개국(영·호), 주소 /<나라>/, 월 1회 원문 해시 감시, 금액별 쪽 대량 생성 금지. 판정 허브 공개 +7일(10/16).
  - [예술가 요청] global-calcs 다른 한 가지('원문 대조 도장' 채택/반려 또는 한 수) 트랙:B · 담당 **firemap-artist** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 2장, ventures/global-calcs/compare.md
  - [시안 요청] global-calcs 허브 첫 화면(나라 줄+도장)·나라 쪽 도장 칩·대조표 쪽 트랙:B · 담당 **firemap-designer** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 7장(X-V1 틀 유지, 375px 첫 3초에 나라 줄마다 도장)
  - [시안 요청] global-calcs 도장 문구 영어 1·2·3위("Checked against … on 3 salaries · date", approved/official 금지) 트랙:B · 담당 **firemap-copywriter**(영어 최종 firemap-editor-en) · 시한 10/2 12:00 · 근거 plans/global-calcs.md 2·8장
  - [시안 요청] global-calcs 측정(check_open·country_switch·share, 도장 클릭률=check_open÷calc_submit)·경로별 utm(share/hn/email) 트랙:B · 담당 **firemap-growth** · 시한 10/2 12:00 · 근거 plans/global-calcs.md 4·6장
  - [조사 요청] 호주 계산기 사이트에 적용되는 금융상품 조언 규정 원문(연금 기여 결과 표시가 걸리는지) + ATO 저작권 고지 원문 재확인 트랙:B · 담당 **firemap-venture-research-global** · 시한 10/8 20:00 · 근거 plans/global-calcs.md 8장
  - [지시] global-calcs 첫 판(하루) 트랙:B · 담당 **firemap-venture-builder** · 시작 조건 X-V1 10/8 판정 키우기/유지(접기면 보류) · 공개 목표 10/9 22:00 · 근거 plans/global-calcs.md 7장 — /au/ 1쪽(손검산 10·ATO 대조 3) + 허브 / + /uk/checks/·/au/checks/. 오늘 X-V1 범위는 바꾸지 않음. 금지: 판정 전 착수·금액별 쪽 대량·HMRC/ATO 이름을 사이트 이름에.
  - [결재 필요](10/8 키우기일 때) 허브 중립 도메인 1개 · Show HN 게시 사장님 계정 1회 — firemap-venture 판정 뒤 firemap-admin이 approvals.md에.
- [기획 요청] site-ia 기획서 확정 — firemap-planner 트랙:B · 담당 **firemap-planner** · 시한 10/2 12:00 · 근거 plans/site-ia.md(초안), meeting/ia-workshop-2026-10-01.md — 사장님 17:3x '파이어맵을 한 코너로, 전 세계를?' 워크숍 추천 D(집은 둘·firemap.kr 안은 코너·1판=calc-gtm R1과 합침). 확정 때 레드팀 1문 '재심사 중 메뉴·내부 링크 변경 운영 반영 가능?' 답 반영. (워크숍 17:49)
- [예술가 요청] site-ia 한 수 트랙:B · 담당 **firemap-artist** · 시한 10/2 12:00 · 근거 plans/site-ia.md 2·9장, meeting/ia-workshop-2026-10-01.md 4장 — 1판 '어느 계산기든 끝은 몇 살에 은퇴?' / 2판 '같은 내 숫자, 사는 곳만 바꾸면' / 두 집 공통 '원문 대조 도장' 중 채택·반려.
- [디자인 검수 요청] site-ia 시안 범위 확인 — firemap-designer·firemap-brand-director 트랙:B · 시한 10/2 12:00 · 근거 plans/site-ia.md 6장(S1~S5) — 첫 화면 행동 아래 목록 행 1개·'전체' 코너 순서가 숫자 1+행동 1·부품 30개 안인지, 이름·로고 불변 확인.
  - 완료: firemap-planner global-calcs 기획서 17:55
- X-KR-1 가계부: 판매 개시는 리틀리 결재 뒤(통신판매업 첫 해 면제, 신원 표시 조건 — archive). 위 검수 2건 18:10.
- X-G19 영어권 한국어 단어 채널(조건부 승인, 3관문):
  - [예술가 요청] X-G19 '우리만 다른 한 가지' 트랙:A · 담당 **firemap-artist** · 시한 10/2 15:00 · 근거 ventures/xg19/compare.md — 편마다 구성이 달라지는 규칙 1개.
  - 카드 ventures/xg19/brief.md(A판 11칸) — 담당 **firemap-venture** · 시한 10/2 20:10 회차. 접기: 첫 공개 +7일 롱폼 조회 300 미만 그리고 평균 시청 지속률 25% 미만.
  - 제작 [지시]는 결재(새 브랜드 계정) + X-CN-1 첫 판 공개 뒤에만 firemap-venture-builder에게.
- [요청] X-G4 AI 스톡 이미지 재상정(research-global 08:4x) → **firemap-venture** 판정 줄 없음. 결재 Adobe 기여자 계정(approvals 07:4x ①). 근거 ventures/global/terms-2026-10-01-0840.md.
- [요청] 해외 실험 제안 1건 (firemap-venture-research-global → **firemap-venture** 본부장, 17:2x) — 근거 ventures/candidates.md '17:1x 회차'(새 후보 G21~G26)
  - **X-G21 아마존 KDP 스페인어 큰 글씨 단어찾기 퍼즐북(10점, 1위).** 'sopa de letras letra grande' amazon.com 7,627개, 1쪽 개인 출판 BSR #3,774(평 485)·#8,820(144)·#19,315(158). 퍼즐·정답·PDF가 **코드 산출물**이라 생성형 AI 공개·강등 규칙에서 자유롭고, 유입은 아마존 검색이 자급. 위험: KDP "2 per book format each week"(2026-09-21~) — 주 2권 품질 경쟁.
  - 첫 판(하루): 100문제 큰 글씨(8.5×11) 페이퍼백 원고 PDF + 표지 1권. 스페인어 단어 목록은 원어민 기준 검수(편집국 스페인어 담당 없으면 '확인 안 함'으로 표시).
  - 지표: 출간 +7일 BSR·판매 수(KDP 보고서). 판정일: 출간 +7일.
  - 필요한 결재: KDP 계정·세금 인터뷰·정산 계좌(비용 0, 인쇄비는 판매가에서 차감).
  - 차순위 기록만: G23 itch.io 코드 합성 효과음(9) · G24 CrazyGames 웹게임(9). G26 note.com은 일본 계좌 필요로 막힘.
- G12 Forms 애드온: 관문 1에서 CAPY에 이미 있음 + 예술가 반려(14:47) → 멈춤. 다른 한 수를 못 찾으면 G16 크롬 확장이 대안(기록만).
- 대기열: X-G1 스페인어 시트 1번(10/3 이후, Gumroad 결재) · X-G17(Gumroad·영어 채널 뒤) · X-KR-2 색칠 도안 '반쪽 도안' 승인(X-KR-1 판매 개시 뒤) · X-KR-3 링크 없는 부고 문자 → **firemap-venture** 판정 대기(research-kr 15:3x, 예술가 관문 전) · 선물 큐레이션 R8 차순위 · P '남의 은퇴 나이 맞히기' 예술가 통과(14:47), 기획서 plans/guess-retire-age.md.

### 운영·약관·성장
- [요청] Sonnet 투입 시험 (AI 연구소 firemap-ai-lab → 운영실장 **firemap-dispatcher**, 다음 배차부터 1주, 17:20) — 근거 ai-lab/bench/2026-10-01-model-tiers.md. Agent 투입 때 점검·집계·초안 직원(watchdog류 점검, growth 집계, write·editor 초안)은 `model: "sonnet"`, **Haiku는 쓰지 않는다**. 결재·사실 대조·디자인 심사·순돌이 대역은 Opus 그대로. 예약 작업엔 모델 칸 없음 — 배차 때 Agent 호출만. 판정 10/8: 같은 직원 관문 반려율(편집·디자인·aitell gate)을 지난주와 비교, 나빠지면 그 직원만 Opus로.
- [지시] 네이버 자동 게시 약관 위험 대안 (순돌이 → 전체 회의·법 참모·브랜드 디렉터, 기한 10/2 회의): 선택지 3개 이상 비교표(카페 공식 API·발행량 축소·네이버 사전 허락 문의 등), 위험 칸에 브랜드 항목. 금지: 사장님 결재 없이 카페 발행 중단·전환. 사실: 카페 공식 API 발행 첫 글 #188(15:09, write) 성공.
- 정지 스위치: STOP_blog 유지(블로그 1단계 ~10/7 멈춤, 10/8~ 하루 0~1편 재개, 10/15 노출 제보 판정 — 담당 firemap-write·firemap-growth·firemap-meeting). 카페는 **10/2 21시 회의**까지 유예(하루 5편·08~22시·3시간 간격).
- [순돌이 검토] (6회째) U6/V6 'Firemap daily growth'(trig_01KmYx7HNYMGjHLy371XGxyc) 지시문 3)항 guidegate 문장 — 10/2 09:00 전. 안 되면 21:15에서 '내일 [auto] 가이드 1회 정지'.
- [순돌이 검토] dev→main 구조 — product-dev 사실 줄이 '바로 운영'이면 workflow.md D·B 트랙 '배포 전 검수' 지킬 장치(검수 대기 커밋 다른 브랜치 또는 deploy 게이트 .design.json)를 레드팀과 정한다.
- [순돌이 검토] Claude 주간 한도(아래 막힘) — 21:15 회의.
- [지시] **firemap-admin**, 기한 17:30: ① 결재함 14행(쿠팡 인플루언서)·15행(리틀리)·X-G19 브랜드 계정 줄에 '휴대폰에서 됨/PC만·누를 링크·순서'(모르면 '확인 안 함'), X-G19 줄엔 "3관문 통과 전엔 누르지 않아도 됨(firemap-venture)" ② data.go.kr TourAPI·고캠핑 '활용신청' — 크롬 로그인 살아 있으면 총무가 직접, 없으면 비밀번호 입력 금지 → 결재함 줄. 완료 기준: approvals.md 줄 + "완료: … HH:MM".
  - 착수: firemap-admin 17:18
  - 완료: firemap-admin 17:25 — ① 결재함 14행 쿠팡 인플루언서·15행 리틀리: '휴대폰에서 되는지 확인 안 함 — PC 크롬은 됨(첫 화면 열림)' + 누를 링크 + 순서 3단계. X-G19 절: '지금 누르지 않아도 됨 — 3관문 통과 전엔 누르지 않아도 됨(firemap-venture)' + 통과 뒤 PC 순서. (휴대폰 폭 화면 시험은 창 크기 변경이 먹지 않아 못 함 → 확인 안 함으로 적음.) ② data.go.kr: 크롬 로그인 **풀림**(마이페이지 → 로그인 화면, 아이디 로그인에 보안문자) → 비밀번호·보안문자 입력 금지라 총무 신청 불가 → 결재함 새 줄 'data.go.kr 활용신청 2건(TourAPI·고캠핑)' PC 크롬 권장·순서 3단계·후순위(X-CN-1이 A 시험 일정으로 바뀌어 급하지 않음).
- [요청] **firemap-admin**: 네이버 데이터랩 검색어트렌드 API(개발자센터 앱 키) 연결 — 검색자 연령·성별용.
- **firemap-bizdev**(10/5): growth 10월 세 경우 계산을 revenue.md에 반영 · 유료 상품 착수 문서에 '자본시장법 제101조 조문 확인·전문가 확인 여부' 칸 필수.
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다.
- 지시문 추가 필요(수정은 순돌이·회의): ?fm_internal=1 규칙(product-dev·designer·audit·watchdog·venture-builder·shorts·youtube-loop), 스꾸 금지·실험 장부·헛돌지 않기·lessons.md·푸시 표준형 빠진 지시문 목록 — archive/2026-10-01.md '지시문 추가 필요'.

## 막힘 (풀리지 않은 것)
- 유튜브 설명 쓰기(videos.update) 무인 회차 권한 거부 — 07:59~ · 영향 F2·V5·R2·E-1 업로드(가능성) · 처리: 위 [순돌이 검토] 3건 묶음, 21:15 안건 · 담당 순돌이.
- X-V1·X-CN-1 공개 저장소 없음(github.io 404) — 09:50~ · 처리: 21:15 안건, 빌더 21:00 재측정 · 담당 firemap-venture-builder / 순돌이 채팅.
- data.go.kr TourAPI·고캠핑 활용신청 필요(우리 키 403, planner 14:42) — X-CN-1 B 나들이 데이터 · 총무 17:2x: 로그인 풀림·보안문자라 사장님 손, 후순위(결재 대기 줄).
- Claude 주간 한도 — 10/1 07:4x 50%·하루 약 18%p → 10/3 12시쯤 90%, 리셋 10/4 21:00 전 바닥 예상(스꾸와 같은 한도). 회의 제안: 운영실장 2명→1명, 결승선 점검 횟수 축소 등(archive). 담당 순돌이·회의 · 기한 21:15.
- 제미나이 flash·TTS 무료 한도 429 반복 — 심사는 lite+Claude 레드팀으로 대체(약한 대체), 제미나이 이미지는 무료 등급 없음(유료만) · 담당 firemap-admin 19:00 재측정.
- (풀림, 기록만) 쿠팡 본인인증 17:04 · Blender 16:49 · E-1 TTS 렌더 16:3x · X-KR-1 aitell 예외 판정.

## 결재 대기 요약 (사장님 손 — 상세 approvals.md)
- 쿠팡 본인인증 → **처리됨 10/1 17:04(사장님)**.
- 승인됨·사장님 손 남음: Mobbin 요금제 결제(카드) · Claude 사용량 확장(claude.ai 설정 → Usage, 월 상한) · 애드센스 지급 정보(은행·세금) · GA4·서치콘솔 읽기(approvals 13행 ①~③).
- (총무 17:2x, 휴대폰 승인 처리분) **다음 검색 등록(승인 07:42):** PC 크롬 webmaster.daum.net → 카카오 로그인 → 사이트 등록 https://firemap.kr → PIN 채팅. **해외 판매 계정 2개(승인 07:42):** Adobe Stock 기여자·Gumroad 가입·정산(approvals.md 해외 판매 절). **X-V1 저장소(승인 17:01):** PC 크롬 github.com/new(결재함 17행 3단계) — 또는 순돌이 채팅 세션. **data.go.kr 활용신청 2건(새 줄):** 로그인 풀림·보안문자라 사장님 손, 후순위.
- 결재 대기: X-CN-1 저장소 exam-dates-kr(18행, 순돌이 채팅으로도 가능) · 쿠팡 인플루언서(14행) · 리틀리 가입·정산(15행, X-KR-1) · 새 유튜브 브랜드 계정(15:1x, X-G19) · 새 도메인(X-KR-2·X-KR-3, 제안 단계).
- 반려: vidIQ 유료. 보류: 제미나이 이미지 유료. vidIQ 채널 연결 위젯은 사장님이 눌러야 함.

## [지시·긴급] 실험 저장소 생김 → X-V1·X-CN-1 공개 (순돌이 17:49, 사장님 "저장소 알아서 만들고 진행해라")
- 사실: github.com/kygstar77-creator/kygstar77-creator.github.io (공개, 빈 저장소) 17:49 생성 완료. 레드팀 결정(decisions/2026-10-01-consolidate.md): 실험은 전부 firemap.kr 밖, 이 저장소 아래 폴더로 — 새 실험마다 사장님 손 0번.
- firemap-venture-builder (지금): 저장소를 C:/Users/강영준/Documents/GitHub/kygstar77-creator.github.io 로 클론 → X-V1 → /uk-take-home-pay/, X-CN-1 → /exam-dates-kr/ 폴더로 배포 구조(루트 index.html은 실험 목록 없이 빈 안내 1줄 또는 404 방지만). GitHub Pages는 사용자 사이트 저장소라 main 푸시로 자동 공개 — 공개 직전 편집 통과·디자인 통과(X-CN-1 반려 2건 고친 뒤)·뻔함 통과 줄이 있어야 푸시. 공개 뒤 실제 주소를 열어 확인(모바일 폭), portfolio.md에 주소·시각, 결재함 17·18행 '완료'로.
- firemap-growth: 공개되면 서치콘솔 속성 추가는 사장님 손이 필요한지 확인(필요하면 결재함에 PC만·링크·순서), 사이트맵·IndexNow.

