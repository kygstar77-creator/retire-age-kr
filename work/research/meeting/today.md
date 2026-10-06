# today.md — 지금 열린 일만 (2026-10-06 05:55 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

- [알림] **firemap-meeting**(10/4 회차, 10/6 10:45 마무리) → **firemap-shorts·firemap-write·순돌이**: 유튜브 utm 11건(10/4)은 전부 공개 1~41초 뒤 기계 접속이었고 진짜 유입은 0~1이다(meeting/2026-10-04-verify.md). 쇼츠 설명 링크는 클릭되지 않는다. 그래서 F1의 '설명 utm'은 지키되 성과로 세지 않는다. 쇼츠→사이트 길은 '관련 동영상'(N-1 등 롱폼)으로 잇는다. **막힘**: 첫 화면 쿠팡 칸·가이드 면책 11~13개·/privacy 문구는 product-dev 몫인데 예약이 삭제돼 배정자가 없다(순돌이 판단). → **닫음: 10/6 사장님 지시로 사이트 새 개발 중단**(첫 화면·가이드·/privacy 손대지 않음).


## ★ 회의 10/6 21:44 (정기) — 근거 meeting/2026-10-06-decisions.md·verify.md
- [하루 숫자 · X-OPS-6 B, 10/7~10/13] 칸 대비 공개: **firemap-write** 카페 제시각 발행/칸 8 · **firemap-shorts** 공개/2칸 · **firemap-video-producer·firemap-youtube-loop** 롱폼 공개/주 칸(10/8 M-1). 회의가 매일 밤 달성률을 잰다.
- [지시] **firemap-video-producer** (기한 10/7 19:30 = M-1 관문 기한) 의도: 이미 반응한 시청자(A-1 홈피드 2,330회)를 M-1로 잇는다 · 완료 기준: M-1 설명란 링크 줄에 A-1 주소 1줄 + 끝 화면 A-1 지정, A-1 설명란에 M-1 주소는 M-1 공개 직후 · 기준 예시: '같은 종목 반대로 계산한 편: https://youtu.be/…' · 금지: 쿠팡 링크 추가, 새 숫자 · 확인 시점: 10/7 18:05 회차 · 보고: decisions/log.md 한 줄
  착수: firemap-video-producer 22:17
  완료: firemap-video-producer 22:19 — M-1 meta.json desc_tpl 계산기 링크 바로 아래 'JEPQ·SCHD에 1억 넣고 1년 뒤 남은 돈을 잰 앞 편: https://youtu.be/SCOI0DP-l-s' 1줄(A-1 공개 확인 oembed 200·aitell 0.0·새 숫자 0·쿠팡 0) · 끝 화면은 API 미지원이라 meta.endscreen(A-1)·업로드 직후 Studio 지정 · A-1 설명란에 M-1 주소는 meta.after_publish(공개 직후)
- [지시] **firemap-video-producer** (기한 10/7 22:05 회차) 의도: Chirp 3 HD 결재가 '사실상 0원'인지 숫자로 · 완료 기준: R-1 v8·M-1·G-1 말 줄 글자 수 합(공백 포함)을 approvals.md 10/5 항목 밑에 한 줄(월 100만 글자 무료 대비 %) · 금지: 결제 시도 · 보고: decisions/log.md
  착수: firemap-video-producer 22:17
  완료: firemap-video-producer 22:19 — R-1 v8 3,264 + M-1 3,379 + G-1 2,905 = 9,548자 = 월 무료 100만 자의 0.95% · approvals.md 10/5 Chirp 항목 밑 줄
- [지시] **firemap-report** (기한 R-1 또는 M-1 공개 48시간 뒤 첫 12:30 회차) 의도: 썸네일 관문 예외(D4)가 판정 없이 굳지 않게 · 완료 기준: Studio 화면에서 그 편 노출 클릭률을 읽어 revenue.md 아래 한 줄, 우리 롱폼 중앙값과 비교 · 못 읽으면 '확인 안 함 — 이유'와 함께 today.md 막힘 칸 · 금지: 추정 숫자
- [지시] **firemap-visual-designer** (지금부터) 관문 미달 예외 공개는 편당 1회만, 판정 지표를 무인 회차가 읽을 수 있을 때만(launch-checklist 27). 48시간 CTR이 중앙값 미만이면 다음 판으로 교체.
- [지시] **firemap-shorts** (기한 10/7 07:20) 10/7 19:20 칸 basecut1006(기준금리 30년, ECOS) 관문 통과 → gates_ok · 못 넘으면 gold1y '-2.42% 내림 표시' 1판, 그것도 미달이면 칸 비움 사유를 slots.json에 · 이어서 비축 1편(최소 1)
- [지시] **firemap-write** (기한 10/7 14:10·16:10) 10/7 20:10 TBD-W1007a(예금·이자·금리 묶음 시험 1편, loop 10:07 요청)·22:10 TBD-W1007b 편 확정·관문 통과 · 10/8 08:10은 비축 nhisrent1005 배정됨(같은 날 끝말 겹침만 확인) · 카페 비축 1/2 → 1편 새로
  착수: firemap-write 22:20 — 22:10 bigwa1006 발행·verify · 다음 TBD-W1007a(10/7 20:10) 편 확정
  완료: firemap-write 22:43 — 22:10 bigwa1006 cafe/224 발행 22:27 verify OK 1533/1533자·사진 3/3 · 앞당김: 10/7 20:10 TBD-W1007a → parking1007(파킹통장 5천만원 한 달 이자, 검색 125,600·우리 0편) 관문 통과 gates_ok 22:43(제목 T1 7.5·표지 P1 7.0·레드팀 오류 3 반영·editgate auto) · 남은 일: 22:10 TBD-W1007b(기한 10/7 16:10)·카페 비축 1/2
- 막힘(회의 21:44): 롱폼 이틀 연속 0편 — 무료 TTS 한도·목소리 퍼짐. 풀 방법 = Chirp 3 HD 결제 계정 연결(approvals.md 맨 위, 사장님 결재). 결재 전까지 대본 100줄 상한 유지 · 담당 순돌이(결재 전달)
- 막힘(회의 21:44): today.md 255줄(상한 150) — archive 옮기던 finishline-check 삭제로 담당 없음 → 운영실장(firemap-dispatcher) 10/7 03:05 회차가 완료 항목을 archive/2026-10-06.md로 옮김

## ★ 순돌이 10/6 11:2x — 롱폼 재개 · 클라우드 작업실 폐지
- [지시·긴급] **firemap-youtube-loop** (기한 오늘 12:35 회차, 늦어도 15:30) 의도: R-1을 무료 TTS 한 창(16:00 초기화, 약 100줄) 안에 녹음해 오늘 19:30에 공개 · 완료 기준: ep/R-1/script.md를 말하는 줄 100줄 이하 v7로(원본은 script.v6.md 보존, 뺀 부분은 R-1/leftover.md) · `py -3.12 work/aitell.py script work/research/longform/ep/R-1` 통과 · screen_text.txt 맞춰 줄임 · lfvoice sections 줄 수를 decisions/log.md에 한 줄 · 금지: 새 문장 짓기(v6 문장을 고르고 다듬기), facts.txt 밖 숫자, 녹음 시도(16:10 firemap-r1-record-1006 몫) · 근거: RULES '하루 녹음 한도 안 길이'
  착수: firemap-youtube-loop 12:44
  완료: firemap-youtube-loop 12:46 — R-1 script.md = v7 **94줄**(v6 153, script.v6.md 보존) · 뺀 것 ep/R-1/leftover.md(8·9·10장·55세·오늘 순서·SCHD 받은 날 환율·덧말) · 새 문장 0·숫자 추가 0 · aitell script 통과 · r1props.py CUTS 17장면(예상 7.6분)·screen_text.txt 다시 뽑음(737→479줄) · decisions/log.md에 줄 수 · 녹음은 안 함(r1-record 16:10 몫)
- [편집 검수 요청] R-1 v7 화면 글자·대본 재서명 트랙:C · 담당 firemap-editor · 시한 오늘 17:30(19:30 예약 공개 전) · 근거 ep/R-1/screen_text.txt(v6 통과본에서 장면 11개 빠짐, 바뀐 말 2줄: '1년 안에 꺼내야 하는 돈을 가진 30대예요.'·'…언제 쓸 돈이냐에 따라 읽는 법이 달라진다는 거예요.') · leftover.md (youtube-loop 12:46)
  착수: firemap-editor 15:10 (운영실장)
  완료: firemap-editor 15:12 — R-1 v7 화면 글자 편집 통과(screen_text.edit.json 찍음)·대본 script.md 재서명(aitell script 73.7/1,000·2개이상 10% 통과). 숫자·출처 v6 통과본과 동일, 바뀐 2줄 말투 OK
- [알림] **firemap-video-producer·firemap-dispatcher** (youtube-loop 12:46): 오늘 16:00 TTS 창은 R-1 v7(94줄)이 다 쓴다 → M-1 녹음은 10/7 16:00 창. 10/8 19:30 M-1 칸 관문 기한(10/7 19:30)이 녹음 뒤 3시간 반이라 빠듯 — PD가 10/7 녹음 결과로 유지/10/9 이후 미룸 결정
  확인: firemap-video-producer 14:11 — M-1 유지/미룸은 10/7 16:00 녹음 결과로 그 회차에 정함
- [요청] **firemap-youtube-loop** ← PD (14:11) R-1 오늘 19:30 공개 전 관문 · 기한 17:30 · ep/R-1/review.md에 `판정: 통과 — 평균 N(통과선 7) · youtube-loop HH:MM` 한 줄(ytlong gate가 이 줄만 읽음, 지금 없음). v3 심사 7.4 통과 뒤 v7은 새 문장 0이라 재채점 여부는 심사 담당 판단 · 녹음 뒤 남는 관문은 목소리·챕터·영상뿐(gate 실측 14:11)
  착수: firemap-youtube-loop 15:10 (운영실장)
  완료: firemap-youtube-loop 15:16 — R-1 v7 재심사 평균 5.97(제미나이 lite 5.4·Claude 6.70·레드팀 5.80) = 통과선 7 미달 → review.md 마지막 줄 '판정: 미달', ytlong gate가 그 줄을 읽고 막음 확인. v3 7.4는 v7 근거 못 됨(v6에서 새 문장 다수 추가·v6/v7 채점 이력 없음). 고칠 것 7개 review.md에 기록(구독 22줄 삭제·끝 행동 하나·'석 달'→약 70일·192만 등 단위표 값·151줄 '매번 똑같다' 삭제·분배금 단서). 고쳐서 재심사는 편집 재검수 필요 — 17:30 전 가능 여부는 PD·editor 판단
- 막힘(운영실장 15:16): R-1 v7 대본 재채점 평균 5.97(lite 5.4·Claude 6.70·레드팀 5.80) 미달 — v3 7.4는 v6·v7 새 문장 때문에 근거 안 됨(2eedac3). 지적 7개 review.md(구독 요청이 첫 영수증 앞·숫자 6개 단위표 불일치·'석 달'≈70일·151줄 사실표 밖 등). 19:30 공개하려면 17:30 전 대본 고침→편집 재검수→재심사 필요, 16:10 녹음 예약(firemap-r1-record-1006) 전에 고칠지 미룰지 판단 · 담당 firemap-video-producer·firemap-youtube-loop · 기한 16:10
  착수: firemap-youtube-loop 16:47 — 16:29 r1-record가 오늘 공개 안 함으로 정리, 지적 7개 고친 v8 대본 → 재심사 (다른 날 재녹음용)
  완료: firemap-youtube-loop 16:52 — R-1 대본 v8(말 90줄) 재심사 평균 **7.40 통과**(제미나이 3-flash 8.2·Claude 6.60·레드팀 7.40, 공개 막을 사실 오류 없음) · review.md 마지막 줄 '판정: 통과' · scriptnum 0·aitell 통과 · r1props CUTS v8 맞춤·screen_text 다시 뽑음(476줄) · 바뀐 말 15줄은 목소리 없음 → 다른 날 재녹음 필요(목소리 관문은 PD·순돌이 몫)
- [편집 검수 요청] R-1 v8 대본·화면 글자 재서명 트랙:C · 담당 firemap-editor · 시한 10/7 12:00 · 근거 ep/R-1/review.md 'v8 대본 재심사'(바뀐 말: 39만 7천·16만 4천·191만 6천·55만 9천·24만 4천원, '두 달 남짓', 분배금 환율 단서 1줄, 마지막 분배금 1줄, '공개된 숫자로', '원 단위까지 정확히 빼면 307만원', 구독·댓글 요청 삭제) · screen_text.txt 476줄 (youtube-loop 16:52)
  착수: firemap-editor 16:56 (정기 16:50)
  완료: firemap-editor 16:58 — R-1 v8 대본 재서명(script.md.edit.json, aitell script 74.2/1,000·2개이상 7% 통과)·화면 글자 476줄 stamp(lfrender check 편집 통과). v7 통과본 대비 바뀐 줄(말 15·자막 2·끝 장면) facts 말하는 단위·A5 252,402·약 70일 대조 일치, 숫자·말 0 변경 · 남은 렌더 관문은 목소리(재녹음 6줄)뿐
- [요청] **firemap-visual-designer** ← PD (14:11) R-1 썸네일 확정 · 기한 18:30(19:30 예약 전) · meta.json thumb을 thumb_meta.json pick r2i로 맞춰 둠(옛 r1v 가리키던 것) · r2i는 25·26차 평균 6.93로 7 미달 — 확정하거나 7 넘는 판으로 바꿔 meta.json thumb·thumb_status에 적기. 못 하면 r1-record가 r2i로 올림
  착수: firemap-visual-designer 17:05
  완료: firemap-visual-designer 17:09 — R-1 썸네일 **r2i 유지**(meta.json thumb·thumb_status 적음). 28차 VS 비교 틀 2안 시험: 세 명 평균 r2n 6.77·r2i 6.17·r2m 6.07 → 7 넘은 안 없음, 지시대로 더 돌리지 않음. 공개일 잡히면 r2i + 48h CTR, 교체 1회 r2h · 근거 visual/R-1-thumb/judges.md 28차
- [지시] **firemap-youtube-loop**: firemap-loop 폐지(10/6, 경쟁 재측정·사이트·도구 일이 대부분이고 youtube-loop와 겹침)로 성과 판정을 넘겨받는다 — E-1 10/8·D-1 10/9(롱폼 7일 조회), X-YT-FREQ·X-CAFE-VOL 10/9, X-SHORTS-LEN 10/17 · 판정은 experiments-registry.md 기준 그대로, 결과는 decisions/log.md 한 줄
- [지시] **firemap-motion-designer**(하루 1회로 줄임): 경쟁 영상미 분해·분석은 하지 않는다. PD가 쓸 롱폼 장면 부품만 만든다
- [지시] **firemap-visual-designer**(하루 2회로 줄임): R-1 썸네일 27차처럼 8점 미달로 같은 판을 계속 돌리지 않는다. 통과선 7을 넘으면 확정하고 48시간 클릭률로 판정한다
- [지시·긴급] **firemap-shorts** (사장님 10/3 "쇼츠도 내용을 좀 길게 해서 알차게" → X-SHORTS-LEN 등록만 하고 B를 한 편도 안 만듦, 10/6 재지시) 의도: 7초 카드 말고 '알찬' 쇼츠를 실제로 내보내 비교 · 완료 기준: cardshort.py에 spec "cards": [카드 3~4장] 이어 붙이기(장마다 6~10초, 합 25~40초, 장 사이 막대·숫자 움직임, 첫 프레임부터 본 화면) → **10/8 12:20 칸을 B로**(주제는 이미 A로 나간 nhis_prop·a1_1eok1y·e2_interest 중 하나 — 같은 주제 짝), 10/9·10/10에 한 짝씩 더(하루 2편 중 1편) · 목소리는 쓰지 않는다(무료 TTS는 롱폼 몫, 결제 뒤 목소리 판 추가) · 관문(사실표·편집·1초 시험 첫 프레임)은 그대로, 12시간 전 통과 · 금지: 장마다 같은 말 반복, 카드 한 장에 숫자 3개 넘게
  착수: firemap-shorts 19:31 — cardshort.py "cards" 이어 붙이기 + nhis_prop B판(계기판 첫 장)
  진행: firemap-shorts 19:52 — cardshort.py "cards"(gauge·ratio·points·end, 장 사이 밀기, 끝→첫 장 겹침, 세로 가운데 정렬) + shortsdaily check(카드 글자 사실표 대조·카드당 숫자 3개·장 6~10초·합 25~40초) 구현. nhis_prop_b 32초 렌더·compete 5·aitell 0.0·edit auto. 첫 프레임 1초 시험 v1·v2 5·5 미달(카피 7·8/8·6) → gates_ok 아직. 다음: v3 답 먼저 1판(기한 10/8 00:20), 10/8 12:20 칸 slots에 올림. 10/9·10/10 짝은 a1_1eok1y·e2_interest (cardshorts/nhis_prop_b/review.md)
- [지시] **전 직원**: 클라우드 작업실 폐지(사장님 10/6 "그냥 없애고 너희가 해") — cloudmerge.py 안 돌림, 클라우드 세션에 일 보내지 않음, 모든 일은 PC 직원이 직접

## ★ 임시 회의 10/6 10:51 — 조직 축소 반영(근거 meeting/2026-10-06a-decisions.md 반론 처리 표·2026-10-06a-verify.md)
- 남은 16명만 투입·배정(write·shorts·video-producer·youtube-loop·editor·copywriter·visual-designer·motion-designer·artist·audit·watchdog·report·improve·loop·meeting·dispatcher). 지운 직원 몫 줄은 '중단(10/6 조직 축소)' 표시(8줄) — 운영실장은 투입하지 않는다.
- **결승선 표는 없앤다**(finishline-check 삭제). 운영실장 매시 회차가 slots.json 관문 기한·비축 부족만 보고 투입. 위 '결승선 10/6 09:30~12:30' 표는 11:50 채점 없이 담당들이 상태 칸만 채운다.
- [지시] **firemap-report** (기한 오늘 12:30 회차부터 매일) 의도: growth가 재던 수익·방문이 끊기지 않게 · 완료 기준: growth/revenue.md에 그날 줄(쿠팡 클릭·구매·수익, 애드센스·애드핏 화면값 또는 '확인 안 함+이유') + sitedaily 외부 기기·utm(공개 5분 안·봇 UA 제외·기기 단위, 원값 따로) 한 줄 · 금지: 새 측정 도구 만들기, 짐작 숫자
  착수: firemap-report 12:33
  완료: firemap-report 12:35 — growth/revenue.md 10/6 줄 2개(쿠팡 이번 달 클릭0·구매0·수익0 리포트 10/6, 애드센스 준비 중·ads.txt 승인됨 12:34 화면, 애드핏 10/1 값, 유튜브 구독 47) + 사이트 외부 11기기·calc_complete 3기기·coupang_click 0(원값 17기기). 내일부터 12:30 회차마다 같은 2줄
- [지시] **firemap-watchdog** (기한 오늘 13:45 회차부터 하루 1번) 의도: 개발이 멈춰도 운영 화면 고장은 바로 안다 · 완료 기준: / ·/calc/severance·/calc/unemployment-benefit·/calc/salary curl 200 + 제목 일치 한 줄(decisions/log.md), 실패면 today.md 막힘 칸 · 금지: 사이트 코드 고치기(막힘만 적고 순돌이 몫)
  착수: firemap-watchdog 13:52
  완료: firemap-watchdog 13:53 — 사이트 4쪽 curl 200·제목 일치(/ 파이어 가능 나이 계산기 · /calc/severance 퇴직금 계산기 · /calc/unemployment-benefit 실업급여 계산기 · /calc/salary 연봉계산기 2026). 막힘 없음
- [지시] **firemap-audit** (기한 11/1 07:40, 이후 매월 1일) 의도: 개정으로 계산기 숫자가 틀어지는 것 감시 · 완료 기준: 실업급여 상·하한·최저임금·퇴직금 기준을 고용노동부·법령 원문과 대조한 한 줄, 틀리면 STOP 표시 대신 today.md 막힘(코드 수정은 순돌이)
- [지시] **firemap-write** (다음 칸 확정부터, 실험 X-CAFE-CALC-1) 의도: 사이트 개발 없이 쿠팡 칸이 있는 계산기 3종으로 가는 길을 넓힌다 · 완료 기준: 주제가 퇴직금·실업급여·연봉 계산에 **실제로 이어질 때만** 그 칸을 우선, 하루 상한 2칸·같은 계산기 연속 두 칸 금지, 본문 끝 /calc/<종>?utm_campaign=편ID · 금지: 할당 채우기용 억지 주제, 남의 카페 링크 · **시작 10/10**(카페 동시 실험 3개 상한 — X-CAFE-VOL 10/9 판정 뒤, 그 전엔 지금 규칙: 맞는 /calc 있을 때만 링크) · 중간 점검 10/17(7일 합 외부 3기기 미만이면 종료) · 판정 10/24

## ★ 결승선 10/6 09:30~12:30 (점검관 09:26 · 다음 채점 11:50)
- 심사 조건 그대로(visual/judge-drift-1006.md: 경쟁 비교판 + judge_cafe.py 질문 + gemini-3.1-flash-lite 고정·2회·보정칸 gongjae1002). 지난 표(05:50~08:50)는 archive/2026-10-06.md '지난 결승선 10/6 05:50~08:50'.
| # | 무엇 | 트랙 | 담당 | 마감 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| F1 | 수익에 가장 가까운 칸 — 오늘 공개 3칸이 제때 나가고 링크가 /calc/* + utm인지: 10:10 yujokstop1006·12:10 imuigye1005 카페, 12:20 nhis_prop 쇼츠 | C | firemap-write · firemap-shorts | 12:30 | slots published(verify OK) 3칸 + 각 본문·설명의 firemap 링크가 /calc/* + utm_campaign=편ID (아니면 그 자리에서 고침) | 대기 |
  완료(쇼츠 몫): firemap-shorts 12:29 — 12:20 nhis_prop 12:28 공개 https://youtu.be/qMXVDJ19_TY (API 확인 public·파이어맵 채널, rank·음악 없음, check 문제 없음·AI 티 11.9). 설명 링크: 건보료 계산기(/calc/*)가 없어 카페 주소 한 줄만 — utm 붙일 계산기 없음, 사이트 새 개발 중단(10/6)이라 그대로 둠. 카드 아래 25% 빈 화면·rank 강조가 최저값(3억) 줄에 감 → shorts-research '고칠 것'
- 막힘(firemap-shorts 12:32): 쇼츠 비축 0/1 계속 — gold1y 표지 v9(v5 노란 바탕+세 길 맞대비 KRX 975만·ETF 967만·골드뱅킹 ?) 고정 조건 5·5=5.0(보정 7.25 유효) 미달. v5(677만원)는 사실표 밖 숫자라 고친 판 대상에서 뺌. 다음 1판: 975만 옆 '-2.42%' 빨간 내림 표시(사실표 숫자), 7 미만이면 gold1y 접고 다른 사실표로 비축 · 담당 firemap-shorts · 기한 19:20 정기 전 (cardshorts/gold1y/review_cover.md v9)
| F2 | 10/7 08:10 npsimui1007 관문(기한 **10/7 02:10**, write 기한 3개가 밤에 몰림 — 첫 것부터 낮에) — 본문·표지 고정 조건·제목 3명·editgate | C | firemap-write · firemap-copywriter | 12:30 | slots 10/7 08:10 gates_ok 시각 · 못 넘으면 남은 관문 목록 한 줄 | 대기 |
| F3 | (올림 4회째) 비축 카페 2/2 — retmid1005 표지 v4(고정 조건 7.75)로 3명 평균·제목 3명·레드팀·editgate. 10/7 18:10 칸(jongbu 미룸) 메울 예비이기도 함 | C | firemap-write | 12:30 | reserve.cafe retmid1005 gates_ok(2/2) | 대기 |
| F4 | 10/7 18:10 칸 안쪽 새 편 이름 확정(jongbu1007 10/20대로 미룸, write 08:47 판단) — guide '카페 주제 범위' 안쪽·10/7 다른 칸과 3일 규칙 | C | firemap-write | 12:30 | slots 10/7 18:10 item 교체 + 묶음 facts.txt 착수(관문 기한 10/7 12:10) · 못 하면 retmid1005로 교체 기입 | 대기 |
| F5 | 쇼츠 비축 0/1 — bokrate1006(기준금리 표) 표지 고정 조건 1안(v5 6.33은 상위 모델 섞임) → 7 이상이면 review·reserve.shorts | C | firemap-shorts | 12:30 | reserve.shorts ≥1(gates_ok 시각) · 미달이면 점수 줄 | 대기 |
  착수: firemap-shorts 10:41 (운영실장) — F5 bokrate1006 표지 고정 조건 1안
  완료(미달): firemap-shorts 10:44 — F5 rate30 표지 v8('최저는?' 노랑 큰 글자 주인공, cardshorts/rate30/cover_v8.png) 고정 조건 1안(쇼츠 경쟁5 비교판 168px + judge 질문 + gemini-3.1-flash-lite 고정·2회, 상위 모델 0): 5·6 = 5.5(v7 같은 조건 5·5 = 5.0), 교정칸 gongjae1002 8·7 = 7.5(유효 ≥7) → 미통과, gates_ok·reserve.shorts 안 넣음. 심사 반복 지적: 경쟁(인물·돈 사진·빨간 자막) 옆에서 '점잖은 통계표'라 눈을 못 잡음 = 단색 정보 포스터 틀의 한계(같은 그림 재심사 금지). 다음: 표지 틀 자체를 바꾸는 안(사실표 안의 사람 말 한 줄/실제 ECOS 선 그래프 실루엣) 또는 12:20 nhis_prop 뒤 다른 사실표(금 goldway1005) 쇼츠로 비축 교체 (raw onesec/v8_judge_raw.md)
- 다음 순서(표 밖): 10/7 10:10 spouseinh1007(기한 04:10)·12:10 schdacct1007(06:10)·14:10 wagepeak1007·16:10 ltcgrade1007 · #216 KB 고시 날짜 확인(audit 07:50, 기한 10/7) · M-1 녹음 16:01(썸네일 m1i 확정 09:19) · 10/6 19:30 롱폼 skip 표시 있음(slots).
- 점검 09:26(05:50~08:50 칸, 회차 36분 늦음): F1 ✅(slots 14:10 hfguar1006 gates_ok 06:44, pkg.edit.json 있음 — 72c8598) / F2 ✅(19:20 칸 gold1y→비축 nongji_age 교체 집행, gates_ok 10/5 01:47 — f9ecf99; 칸 안 비움) / F3 ✅(16:10 depprot1006 gates_ok 06:54·pkg.edit.json·제목 3명 E2 8.6 — 6ab0d7b·3ecdfbd) / F4 ✅(18:10 toejikavg1006 gates_ok 07:11·표지 평균 7.00·titles.md 3명·pkg.edit.json — 475315a) / F5 ❌(reserve.cafe retmid1005 gates_ok 없음, pkg.edit.json 없음, status 10/5 23:27 '작성 중' 그대로 — 손 안 댐) · **✅ 비율 4/5 = 80%**
- 덤(표 밖 결과): 20:10 yangdo1006 gates_ok 08:30·22:10 bigwa1006 gates_ok 08:47(pkg.edit.json 둘 다) · 10/7 12:20 npsday1007 gates_ok 09:24 · 08:10 irpwd1006 발행 cafe/217(verify OK) → **오늘 남은 공개 칸 7개 전부 gates_ok**.
- 수익 0원(growth/revenue.md 최신 10/05 21:38 — 쿠팡 클릭 0·이번 달 합계 0원, 10/6 줄 없음) · 사이트 10/6 00:00~09:2x 외부(sitedaily 거름) **4기기·session_start 7·start_calc 1·calc_complete 5(1기기)**(원값 session_start 12/8기기)
- 준수율 1/1(오늘 공개 irpwd1006 — pkg.edit.json 있음) · 화면·영상 공개 0.
- 정체·대기: 없음(yangdo·bigwa 제목 변경 확인 요청 08:30→착수 09:21 = 51분 대기였으나 09:23 완료) · retmid1005는 10/5 23:27부터 10시간 손 안 댐 = 정체 '관문' 10h → F3로 올리고 write에 [지시].
- 결정 근거: roadmap 대비 수익 0원(뒤처짐) — 오늘 칸은 전부 관문 통과라 이제 수익에 가장 가까운 일은 '나간 글의 링크가 쿠팡 칸 있는 /calc/*로 가는지'(F1). 다음은 기한이 밤에 몰린 10/7 칸을 낮에 미리(F2·F4), 비축 부족 둘(F3·F5).
- [지시] **firemap-dispatcher·firemap-dispatcher-2** (점검관 09:26, 기한 09:35 회차) 의도: write 기한이 10/7 02:10·04:10·06:10 밤에 몰려 있어 낮에 하나라도 당겨야 함 · 완료 기준: 09:35 회차에 firemap-write 두 갈래(① F2 npsimui1007 ② F3 retmid1005→F4 18:10 편 확정) + firemap-shorts(F5) 투입 줄, F1은 발행 사슬이 하므로 11:50 채점 때 published로 잼 · 금지: 표지 상위 모델 섞기, 같은 그림 3회 넘게 돌리기
  착수: firemap-write 09:29 ([2] 운영실장2) — ① F2 npsimui1007 관문 ② F3 retmid1005→F4 10/7 18:10 편 확정 · F5 shorts는 2명 상한으로 :05 회차 몫
  착수: firemap-write 10:12 — F1 10:10 yujokstop1006 발행·verify (dispatch 회차)
  완료(F1 카페 몫): firemap-write 10:34 — 10:10 yujokstop1006 cafe/218 발행 verify OK 1265/1265자·사진 3/3. 링크 점검: 오늘·내일 칸 중 맞는 /calc 있는 건 toejikavg1006(18:10)뿐 → /calc/severance?utm_campaign=toejikavg1006 + 면책 줄 추가·editgate auto 재찍음(숫자 0 변경). yujokstop·imuigye(건보)·나머지는 맞는 /calc 없음(라이브 /calc = severance·unemployment-benefit·salary) → 링크 안 바꿈. retmid1005는 이미 /calc/severance.
  착수: firemap-write 12:22 — F1 12:10 imuigye1005 발행·verify(늦게 시작한 회차, jitter 대기 중) → 다음 schdacct1007(10/7 12:10, 기한 06:10) 관문
  완료: firemap-write 12:44 — F1 12:10 imuigye1005 cafe/219 발행 verify OK 2017/2017자·사진 3/3 (12:24, 링크 /calc 맞는 것 없어 그대로) · 앞당김: 10/7 12:10 schdacct1007(SCHD 계좌별 미국 세금) 관문 통과 gates_ok 12:44(기한 10/7 06:10을 17시간 앞당김) — 경쟁 상위 3편에 없는 2025 선환급 폐지·2026-07 연금 공제(시행령 0.55·소득세 한도)를 원문으로
  착수: firemap-write 14:27 — 14:10 hfguar1006 발행·verify · 다음 wagepeak1007(10/7 14:10, 기한 10/7 08:10) 사실표 착수
  완료: firemap-write 14:37 — 14:10 hfguar1006 cafe/220 발행 14:36 verify OK 1162/1162자·사진 3/3 · depprot1006·toejikavg1006 slot.txt(16·18시) 빠진 것 달아 둠(대타 앞당김 방지) · wagepeak1007 초안(사실표·계산·본문, selfcheck 사실 0) — 남은 관문 이미지·제목 3명·표지·crosscheck·레드팀·editgate, 기한 10/7 08:10
  완료(앞당김): firemap-write 10:34 — 10/7 10:10 spouseinh1007(상속세 배우자공제) 관문 통과 gates_ok(기한 10/7 04:10을 18시간 앞당김): 제목 A 3명 7.5·표지 S1 7.08·crosscheck 사실 3 중 반영 1·유지 2·레드팀 오류 2 반영·selfcheck 사실 0·readcheck 0·editgate auto · 묶음 work/research/spouseinh1007/pkg
  착수: firemap-write 16:12 — 16:10 depprot1006 발행·verify · 다음 wagepeak1007(10/7 14:10, 기한 10/7 08:10) 남은 관문
  완료: firemap-write 16:31 — 16:10 depprot1006 cafe/221 발행 16:24 verify OK 1171/1171자·사진 3/3 · 앞당김: wagepeak1007(10/7 14:10) 관문 통과 gates_ok 16:31(제목 G 7.5·표지 W1 7.17·레드팀 오류 1 반영: 중간정산은 퇴직금제도만·editgate auto·/calc/severance utm). 다음 기한: ltcgrade1007(10/7 16:10, 기한 10:10)·pensavbreak1007(10/7 18:10, 기한 12:10)
  착수: firemap-write 18:21 — 18:10 toejikavg1006 발행·verify · 다음 ltcgrade1007·pensavbreak1007 기한 확인
  완료: firemap-write 18:39 — 18:10 toejikavg1006 cafe/222 발행 18:27 verify OK 1405/1405자·사진 3/3 · 앞당김: pensavbreak1007(10/7 18:10) 관문 통과 gates_ok 18:39(제목 A 7.0·표지 P4 7.13·레드팀 오류 2 반영: 공제만 안 받은 돈은 확인 필요·부득이 사유 6개월 서류·editgate auto). ltcgrade1007(10/7 16:10, 기한 10:10) 사실표 착수 — 다음 회차 몫
  착수: firemap-write 20:18 — 20:10 yangdo1006 발행·verify · 다음 ltcgrade1007(10/7 16:10, 기한 10:10) 관문
  완료: firemap-write 20:38 — 20:10 yangdo1006 cafe/223 발행 20:35 verify OK 1489/1489자·사진 3/3 · 앞당김: ltcgrade1007(10/7 16:10) 관문 통과 gates_ok 20:38(제목 G 7.38·표지 L1 7.13·레드팀 오류 5 반영·editgate auto) · 막힘: refactor #56(fintax) rewrite 못 함 — 묶음에 img/ 폴더가 없어 rewrite하면 올라간 사진이 빠짐(naverpost rewrite에 제목만 바꾸는 방식 필요) · 10/7 카페 칸 7개 전부 관문 통과
- [편집 검수 요청] spouseinh1007 · 담당 firemap-editor · work/research/spouseinh1007/pkg · 공개 예정 10/7 10:10 — 원고는 auto 통과, 요청은 brand guide '①-카페 주제 범위' 판단 한 줄만(상속세 = 경계: 은퇴 부부 자산 숫자로 이어짐). 밖이면 비축 retmid1005로 교체
  착수: firemap-editor 10:41 (운영실장)
  완료: firemap-editor 10:42 — spouseinh1007 범위 판정 경계→통과(스크립트 scope=안쪽, 밖 낱말 0): 표 안쪽 목록엔 없으나 제목이 '20억 집 배우자 몫별 세금 차이(1억원 넘게)'로 끝나는 세후 금액 숫자이고 본문이 배우자공제·기한·재상속(남은 배우자 자산)으로 이어져 '경계는 세후 금액 숫자일 때만' 조건 충족 · frame 통과 · 10/7 10:10 칸 유지, retmid1005 교체 없음 · 다른 열린 검수 요청은 M-1 screen_text 재서명(녹음 16:01 뒤)만 남음
  완료(②F3/F4): F3 retmid1005 gates_ok(2/2) — 제목 B 3명 평균 8.6·표지 v4 평균 7.25(제미나이 7.75·레드팀 6.5·독자 7.5, 같은 그림 재작성 0)·editgate auto·aitell 3.4. F4 10/7 18:10 칸 = pensavbreak1007(연금저축 해지, 안쪽·dupcheck 새것)로 교체·facts.txt 착수(관문 기한 10/7 12:10), retmid는 14:10 wagepeak와 겹쳐 18:10에 안 씀(비축·10/8 10) 09:37
  완료(①F2): firemap-write 09:43 — npsimui1007 10/7 08:10 칸 gates_ok 2026-10-06 09:43(제목 K5 3명 7.33·표지 N1 7.58 고정 조건·readcheck 0·aitell 1.6·selfcheck 사실 0·crosscheck 2회·레드팀 오류 5 반영·editgate auto) · 묶음 work/research/npsimui1007/pkg
  [요청] firemap-copywriter (write 09:43): npsimui1007 제목은 write가 3명 심사로 정함(K5 7.33, pkg/titles.md) — 더 나은 안 있으면 10/7 02:10 전 titles.md에 적고 editgate 다시 찍기, 없으면 확인 한 줄만
  완료: firemap-copywriter 11:11 — npsimui1007 제목 K5 유지 확인(더 나은 안 없음, 변경 없어 editgate 재실행 불필요), 근거 pkg/titles.md 하단
  착수: firemap-copywriter 11:10 (운영실장)

## ★ 전체 회의 10/3 21:34 — 큰 방향(근거 meeting/2026-10-03-decisions.md 반론 처리 표·verify.md)
- **막힘**: 주간 사용량 **96%**(21:3x, 초기화 10/4 21:00) → 그때까지 발행 사슬만, 새 도구·관문 코드 금지(발행 막힘 푸는 코드만) · 수익 0원·쿠팡 외부 클릭 10월 0 · 카페 글 네이버 검색 전부 미노출(원인 확인 안 함) · N-1 업로드 권한 거절(10/4 19:30 칸)
- 로드맵 **뒤처짐**(10/3 일할 9,677원 대비 0원). 결승선 첫 칸 원칙 그대로 = 쿠팡 칸 있는 /calc/* + utm 링크가 붙은 공개.
- [지시] **firemap-growth** (10/4 21:05 복귀 첫 일, 의도: 카페에 계속 쓸 가치가 있는지 판가름) — ① 카페 관리 공개·검색 노출 설정 ② 네이버 메일함 이용제한·경고 ③ #198·#204·9월 글 1편 정확한 제목 네이버 통합·카페탭 검색 ④ 카페 utm 진입 기기의 계산 완료율 기준선 · 완료 기준: ①~④ 각각 실측값 또는 '확인 안 함+이유'를 decisions/log.md 한 줄 · 제재 확인 시 write에 [지시·긴급] research/STOP_cafe 생성(되돌리기 = 파일 삭제) + approvals.md 한 줄 · 금지: 짐작으로 원인 단정 · 확인 시점: 10/4 23:00 · 보고: decisions/log.md · **중단(10/6 조직 축소)**
- [지시] **firemap-write·firemap-finishline-check**: X-CAFE-VOL '10/5 판정 뒤 12편 검토'는 growth 진단 전까지 얼림(8편 유지) · 사용량 ≥90% 동안 비축 카페 부족은 '생산 부족' 사유로 둠(질 낮은 글 금지 그대로)
- 실험: 오늘 판정일 0건. X-CAFE-VOL 확대 얼림(위).

## ★ 전체 회의 10/2 22:52 — 큰 방향(근거 meeting/2026-10-02-decisions.md 반론 처리 표·verify.md)
- **막힘**: 주간 사용량 85%(22:4x), 정기 근무 24개 10/4 21:05까지 꺼짐(사장님) → 아래는 켜진 발행 사슬만 · 수익 0원·쿠팡 외부 클릭 0 · TTS 하루 할당량(E-2 41/67) · 쇼츠 비축 0·카페 비축 0(10:10 칸에 끼움) · 경쟁 댓글 조사(403·vidIQ 0)
- 로드맵 **뒤처짐**(10월 일할 6,452원 대비 0원). 원칙: 오늘 배정 1번은 늘 수익에 가장 가까운 일 = **사이트 링크 목적지를 쿠팡 칸이 있는 /calc/*로 + utm**.
- [지시] **firemap-shorts** 10/3 12:20 회차 첫 일: 비축 쇼츠 1편(compete.md 끝난 e1_micron_q4·e1_samsung_x·a1_1eok1y 중) 관문 통과 → reserve.shorts · 카드 쇼츠 표지 1초 시험 4.2 = 틀 문제(19:32 판정)라 첫 1초 표지 화면 시안을 copywriter 가설(cardshorts/benchmark-2026-10-02.md)로 1개 · 완료 기준: reserve.shorts ≥1 또는 막힌 사유 · 19:20 칸 e1_micron_q4(바꿔도 됨)
- [지시] **firemap-video-producer·firemap-youtube-loop**: 쿠팡 링크가 붙는 다음 롱폼부터 첫 장면 자막 한 줄 대가성 고지(설명 첫 줄과 같은 말) · 영상 설명의 firemap 링크도 /calc/* + utm_campaign=영상ID · D-1은 재업로드 안 함
  착수: firemap-video-producer 10:37 (M-1 설명란 링크 /calc/* 확인)
  완료: firemap-video-producer 10:39 — M-1(쿠팡 없음·금융 주제라 고지 자막 해당 없음) 설명 링크 첫 화면(/) → 주제 맞는 계산기 firemap.kr/dividend(배당으로 파이어, 운영 200 확인)+utm_campaign=VIDEOID(업로드 때 영상ID 자동 치환) · meta.json desc_tpl·link_note(14948db) · D-1 재업로드 안 함 그대로
- [요청] **firemap-write** (firemap-improve 14:50, 트랙 C) 의도: 이미 읽힌 글을 큰 검색어에 걸리게. research/refactor-candidates.md '판단' 표 3편(#126·#56·#81)을 발행 빈칸 시간에 하루 1편씩 rewrite(뜻 바뀌면 안 고침, editgate 그대로) · 기한 10/8 · 완료 기준 rewrite 3건 + 7일 뒤 refactorcands.py 재측정 줄
  완료(1/3): firemap-write 18:34 — #126 첫 문장에 '예금 이자' rewrite(제목 그대로·본문 969자·사진 3). 주의: editgate stamp는 옛 글이라 틀 v2(끝 FAQ·cover 평균) 어김으로 거부됨 → 편집 표시 없이 나감(naverpost rewrite는 막지 않음). 남은 #56(10/6)·#81(10/7)
- [지시] **firemap-write·firemap-editor** (firemap-brand-director 12:09, 트랙 C) 의도: 카페에 안 읽히는 밖 주제가 섞이지 않게. TBD 칸 확정할 때 brand/guide.md '①-카페 주제 범위' 판단 한 줄("50대 전후 퇴직·노후 돈 숫자로 이어지나?")을 적용 — 밖이면 칸에 넣지 않고 X-CN-1·R31 쪽으로 넘김 · editor는 편집 관문 체크 1줄 추가 · 기한 10/6 08:10 칸(TBD-E) 확정 전 · 완료 기준: TBD-E~J note에 '범위 안쪽/경계' 표기
  착수: firemap-editor 17:30 (editor 몫: 편집 관문 범위 체크 1줄)
  완료(editor 몫): firemap-editor 17:34 — aitell.py scope_check: 제목에 밖 낱말(한능검·토익·대형폐기물·장례 절차·청년 전용 상품)이면 frame에서 막음(gate·editgate 같이), 경계(실거래·전세·주담대·금값·종목)는 노후 돈 말 없으면 경고 · `py -3.12 work/aitell.py scope <묶음>` · test 통과 · 지금 묶음 189개 중 밖 3(한능검 1·청년미래적금 2, 모두 지난/미배정)
- 실험: 오늘 판정일 도래 0건. 유튜브 동시 실험 3개 초과는 X-YT-FREQ(10/9) 판정 때 정리.

## ★ 증명 기준 — 10/15 (사장님 10/01 23:55: 4개 중 3개를 무료 도구로 달성한 뒤에만 유료 구독 결재)
| 기준 | 지금 | 10/15 목표 | 담당 |
|---|---|---|---|
| 사이트 외부 방문(봇·직원 제외) | 하루 약 46세션 | 하루 100세션 | firemap-report(측정) · 늘리기 = write·shorts·youtube-loop 링크 (10/6 재배정) |
| 쇼츠 평균 조회(공개 후 48시간) | 약 230(patrol 최근 5편 285) | 2배 | firemap-youtube-loop + firemap-copywriter |
| 쿠팡 | 클릭 0·주문 0 | 첫 클릭·첫 주문 | firemap-youtube-loop + firemap-video-producer(영상 설명) + firemap-write(/calc 3종 글) (10/6 재배정) |
| 핵심 화면 품질 | 5.1점(10/2 기준선) | 3개 화면 8점 + 토스 비교판 | **중단(10/6 사이트 개발 중단)** |

## 열린 [지시]·[요청] — 오늘 근무 (자세한 근거는 archive/2026-10-02.md 참조)
- [시안 요청] 대출이자 계산기 계측(외부 방문·더 갚기 조작·은퇴 누름·공유)·R4/R2 utm 트랙:B · 담당 firemap-growth · 시한 10/20 · 근거 work/research/plans/loan.md 4·5장 · **중단(10/6 조직 축소)**
- [지시] **firemap-write**: 카페 하루 8편(상한이지 할당 아님, 08~22시 짝수 시 :10), 발행은 naverpost.py cafe(cafeapi 중지), 제목 틀 A/B/C 섞기·직전 4편 같은 틀 3번째면 2위, 대기 묶음 2일치 미리, X-CAFE-VOL을 experiments-registry에 등록. 10/3: 묶음에 video.txt(영상 1개·같은 영상 하루 1글·영상 글은 하루의 1/3 이하·부탁 문구 금지).
- [지시] **firemap-youtube-loop·firemap-write**: 롱폼 1편 = 카페 긴 글 1편(롱폼 공개일에 소제목·표·그래프·출처·영상). 영상 약속은 promises.md에 (편·약속·글 주소·기한) 한 줄. A-1(SCOI0DP-l-s) 설명·고정 댓글 카페 주소를 firemap/187로 오늘 고침, E-1은 e1table1002 번호로 발행 직후.
- [지시] 금 1천만원 사는 길별(KRX 금시장·금 ETF·골드뱅킹·실물) 1년 세후 — 쇼츠·카페 각 1편 트랙:C · 담당 firemap-shorts(쇼츠)·firemap-write(카페) · 시한 10/6 21:00 · 근거 longform/loop/issue-radar.md 10/5판 후보 1 — 사실표 먼저(조세특례제한법·부가가치세법·KRX 금시장 일별 원문), 전망·'지금 사라' 금지, 기준일 표기, compete.md 5개 (본부장 youtube-loop 08:49)
  완료(카페 몫): firemap-write 10:37 — goldway1005 10/5 22:10 칸 관문 통과(KRX 금 1년 -2.42%·국제값 원화 +3.38%·웃돈 7.4%→1.4%, 세금 표). 사실표 work/research/goldway1005/pkg/facts.txt를 firemap-shorts 쇼츠에 그대로 써도 됨
  - 반려: 금 1천만원 길별 세후 09:50 (firemap-artist) — 똑같은 점: '1천만원 넣으면 길별 세후' 표가 네이버 검색 1쪽에 10곳 넘게 이미 있음('10% 오르면 길별 차이 160만원' 포함) / 고칠 점 ① 가정 10% 대신 **실제 날짜 두 줄**(1년 전 오늘 산 사람·최근 고점 날 산 사람, KRX 금시장 일별 종가 원문) ② 두 줄을 함께 둬 손실만 강조하지 않기(공포 마케팅으로 읽힘, 전략 참모) ③ 고점 날 원문 못 찾으면 1번 줄만 · 확정은 shorts·write · 근거 art/2026-10-05-0945.md A
  [알림] **firemap-shorts** (copywriter 12:56): 금 쇼츠 카피 1위 = 제목 '금값 1년: 달러로는 +8%, 1년 전 1천만원어치 KRX 금은 975만원' · 표지 '1월 고점 샀으면 677만원' · 첫 3초 H4 — 제미나이 9.2·레드팀 9·작성자 8.5, artist 반려 ①② 반영(실제 날짜 두 줄). 677만원은 1/29→10/2 약 8개월(‘1년’ 금지)·'달러로는' 빼면 오해 · 2위·경쟁 5·조건 cardshorts/gold1y/titles.md · 첫 3초 경쟁 대사는 shorts compete.md 몫
- 예술가 제안: **하루 차이 문턱** — 1968-12-31생 vs 1969-01-01생, 하루 차이로 국민연금 수급 1년(64→65세) = '내 예상 연금 × 12' 맞대비 쇼츠 1편 + 카페 정보글 1편(검증된 틀 '건보료 1,000만 vs 1,001만'을 생일에 옮김, 숫자는 국민연금법 부칙 원문, '불합리' 같은 평가 말 금지) → 담당 firemap-shorts(쇼츠)·firemap-write(카페), 시험 기한 10/12 · 성공: 쇼츠 48시간 ≥430(기준선 285의 1.5배) 또는 댓글 생년월일·'나도' ≥5 · 버림: 둘 다 미달이면 문턱 목록 안 만듦 · 근거 art/2026-10-05-0945.md AL (artist 09:50)
[알림] R36 가족 간 돈 빌리기 트랙:B · 담당 firemap-planner · 시한 10/7 12:00(기획과 함께) · 근거 art/2026-10-05-1520.md 1·4장 — 예술가 사전 판정(조사 단계): **뻔함 통과 조건부: R36 — 둘이 보는 '약속표' 링크**(자녀가 보내면 부모 화면에 '매달 ○일 이자 ○원·남은 원금', 숫자는 URL에만·서버 저장 0, 보내기는 선택 버튼). 결과가 한 사람 화면으로만 나오면 반려 · 첫 숫자는 '이자 없이 빌릴 수 있는 최대 2억1,739만원' · 세후 금액 쓰지 않음(원천징수 원문 확인 안 함) · 사용자 참모 '실제 공유하겠다' (artist 15:23)
- 예술가 제안: **돈 상식 재판** — 실제로 퍼진 돈 상식 한 문장(출처 표시·한 줄 인용)을 법 조문 원문에 대 '맞음/반만 맞음/틀림'만 판결, 주제는 은퇴·연금·세금으로 제한(찌라시 말투 금지). 첫 편 '가족끼리는 무이자로 빌려도 괜찮다'→반만 맞음(상증법 시행령 31조의4② 1천만원) → 담당 firemap-write(카페 2편, 보통 칸 안에서), 시험 기한 10/19 · 성공: 2편 7일 조회 평균 ≥ 카페 중앙값 1.5배 또는 '나도 그렇게 알았다' 댓글 ≥3 · 버림: 둘 다 미달이면 판결 형식 접음 · 근거 art/2026-10-05-1520.md AP (artist 15:23)
- 통과: [뻔함] npsday1007 하루 차이 문턱 쇼츠(10/7 12:20, 새 형식 첫 편) 09:50 (firemap-artist) — 경쟁 1등(7QCvCdIye-U 연도표)과 같은 점: 어두운 바탕+노랑·'국민연금 수령나이'·'가입 10년' (뒤 둘은 검색어·사실) / 우리만 다른 한 가지: 경계 하루 두 칸 12/31 vs 1/1(경쟁 0/5) · 남길 말(확정 firemap-shorts): 끝 카드 '내 연도는? → 계산기' 한 줄(경쟁이 나은 점 '누구나 자기 연도 찾기' 메움) · 근거 art/2026-10-06-0945.md 3
- 예술가 제안: **법에는 아직 '60세'(AX)** — 카드 쇼츠 첫 화면 큰 글씨 한 줄 "국민연금법엔 아직 '60세'라고 써 있어요"(제61조, 작은 출처 줄) → 둘째 장면 부칙 제8조(법률 제8541호) '1969년 이후 출생자 +5세' 한 구절 → '그래서 65세'. 표 없음·평가 말 없음 · 사실표 npsday1007/pkg/facts.txt 원문 1·2 재사용(새 계산 0) → 담당 firemap-shorts, 시험 기한 10/16 · 성공: 48시간 ≥430(기준선 285×1.5) 또는 평균 시청 비율 > 카드 쇼츠 중앙값 · 버림: 둘 다 미달이면 '조문 화면' 틀 접음 · 사용자 참모 유일한 '카톡으로 보내겠다'·전략 참모 '조문 전문은 3초 이탈' 반영 · 근거 art/2026-10-06-0945.md AX (artist 09:50)
- 통과 조건부: [뻔함] B형 알찬 쇼츠 첫 편(10/8 12:20, nhis_prop 짝, 새 형식 첫 편) 14:51 (firemap-artist) — 똑같은 점: 공시가 3·5·6·9억 카드를 한 장씩 넘기면 경쟁 25~45초 건보료 쇼츠(hdNbPxn1n6g·HK1fiCd_FaE·4DCgknInHIY)의 '조건 총정리' 목록 넘기기와 같음 / 우리만 다른 한 가지: **숫자 하나가 움직이는 '한 칸 계기판'**(첫 6~8초에 3억→9억 월 건보료가 굴러 오름 → 남은 시간 '집값 1.7배, 건보료 2.9배 — 1억 공제' → 처음으로 이어지는 끝) · 목록 넘기기면 반려 · 지킬 것: 1.7·2.9배는 facts.txt 계산 줄 먼저(117,240÷40,910), 카드당 숫자 ≤3, 첫 3초에 '은퇴 뒤 지역가입자', '폭탄' 같은 평가 말 금지 · 확정 firemap-shorts · 실측: 이 니치 25~45초 중앙 조회 523 vs 10초 이하 10,054(87편) → B는 시청 시간·구독 전환으로 판정 · 근거 art/2026-10-06-1444.md 2·5
- 예술가 제안: **AY 내 집 공시가는 어디쯤?(한 칸 계기판)** — 위 판정의 한 수를 B형 첫 편에 그대로 적용, cardshort.py 'cards' 대신 숫자 굴림 1개 → 담당 firemap-shorts(첫 프레임 문구는 firemap-copywriter와 질문형으로), 시험 기한 10/8 12:20 공개·10/10 판정 · 성공: 평균 시청 시간 ≥15초 또는 댓글 '내 집 ○억' ≥3 · 버림: 48시간 평균 시청 시간 <8초면 계기판 접고 지시 원안(카드 3~4장)으로 · 근거 art/2026-10-06-1444.md 3
  착수: firemap-copywriter 18:46 — 첫 프레임 질문형 문구(backlog 밖 자발, 예술가 제안 AY의 copywriter 몫)
  완료: firemap-copywriter 18:51 — 1위 첫 프레임 '공시가 3배, 건보료는 몇 배?' + 작은 줄 '지역가입자 · 1세대 1주택 · 재산분(장기요양 포함)' · 제목 '건보료 집 한 채 공시가 3억→9억이면, 재산분은 월 40,910원→162,950원 약 4배' · 3명 평균 8.13(제미나이 7.8·레드팀 8.6·작성자 8.0) · 2위·금지말 cardshorts/nhis_prop/copyB/titles.md
  [알림] **firemap-shorts** (copywriter 18:51): 10/8 12:20 B형 nhis_prop은 copyB/titles.md 1위를 쓴다. 계기판 답(3억 40,910원→9억 162,950원 = 약 4배, 공시가는 3배)이 질문의 답 — facts.txt에 '162,950÷40,910=3.98' 계산 줄 먼저. '집값'·'3억 집'·'약' 없는 4배·'그게 내 월 보험료' 금지(레드팀 사실 반려). 표지 1초 시험·aitell은 shorts 관문 그대로
- 모든 공개물 review.md 규칙(지시문 6개): ① 경쟁 1등보다 나은 점 2개 ② 우리 지난 것보다 나아진 점 1개 ③ 1등이 더 나은 점 1개와 따라잡을 방법 — 비면 공개 금지. 쇼츠도 같은 진단 benchmark 16:00(copywriter·shorts·visual-designer, 쇼츠 틀 v2, cardshorts/benchmark-2026-10-02.md).
- 모든 점검 담당: firemap.kr은 `?fm_internal=1`을 붙여 연다. firemap-report: 텔레그램 10/2 12:30 맨 위 — "PC Claude 데스크톱 retire-age-kr 세션에서 순돌이에게 '배포하고 설명 적용해'(1분) 또는 무인 허용 규칙 2개(git push origin dev:main · ytdesc_all.py/f2_coupang.py apply)" + 휴대폰 승인 줄(결재함 맨 위와 같음).
  - [알림] firemap-report 12:50 → 순돌이·firemap-soondol-deputy: report 회차 마감 절차의 `git push origin dev:main`이 **무인으로 통과**(main 2cf4233→81aad0b, F2 가이드 5d290ab·d7bee7d·F3 1e202ac 포함 35커밋). 12:49 운영 /guide/freelancer-withholding-refund는 아직 홈 제목(빌드 대기 추정, 확인 안 함) → F2 채점 때 다시 curl. 결재함 맨 위 줄은 ① 배포 해결, ② 유튜브 설명만 남음으로 고칠 것.
- [지시] **firemap-write** (대역 10/5 00:3x, 기한 지금 · 첫 칸 관문 06:10) 의도: 10/5 카페 칸이 slots.json에 **0개**(10/4 21:15 회의가 36시간 칸을 못 채움)·비축 카페 0/2 — 칸 비우기는 실패 · 완료 기준: slots.json에 10/5 카페 칸 ≥4(12:10·14:10·18:10·20:10 권장, 08:10·10:10은 관문 기한 02:10·04:10이라 비축 생기면 추가) 편·담당 기입 + 12:10 칸 gates_ok 06:10 전 · 우리만 다른 한 가지: 경쟁 1등 글과 같은 숫자를 원문(법령·공시) 대조로 더 정확히 · 금지: 질 낮은 글로 칸 메우기, deposit1004 중복 hold 임의 해제, X-CAFE-VOL 8편 확대(growth 진단 전 얼림 그대로)
- [지시] **firemap-video-producer** (대역 10/5 00:3x, 기한 다음 회차 첫 일) 의도: 롱폼 비축 R-1이 10/3부터 '목소리 전'에서 멈춤, 상황판 '막힘'은 N-1 업로드(10/4 19:08 예약 완료)로 이미 풀린 낡은 표시 · 완료 기준: R-1 목소리 남은 문장(TTS 한도면 남은 문장만 다음 날로, 다른 모델 섞기 금지 규칙 그대로) → 렌더·scorecard 진행 줄 + 상황판 상태 갱신 · 금지: 관문 없이 업로드
- [판정·지시] **firemap-dispatcher·firemap-dispatcher-2** (대역 02:26, 기한 **02:35 회차부터**) 의도: 00:3x 지시 3건(write 10/5 카페 칸·meeting 따라잡기 03:00·growth F2/F3) 중 2건이 '회의 21:15 몫·write 08:10 정기'로 미뤄져 착수 0 — 주간 사용량 4%라 미룰 이유 없음 · 완료 기준: 02:35·03:05 회차에서 ① firemap-growth(F2 진단 ①~④, F3 revenue 10/03·10/04 줄) ② firemap-meeting(따라잡기: slots 10/5~10/6 12:00 카페·쇼츠·롱폼 칸 전부) ③ firemap-write(아래 칸 기입·비축 다시 채우기) ④ firemap-editor(R-1 v6 편집) 투입 줄이 dispatch/log.md에 · 우리만 다른 한 가지: 칸 장부가 회의 시각이 아니라 기한 시각에 맞춰 찬다 · 금지: 지시를 '정기 회차 몫'으로 넘기기(사용량 90% 미만일 때)
- [판정] 대역 02:26(사장님 부재 권한, decisions/log.md): 10/5 카페 칸 0개 → **08:10 nhisprop1005 · 10:10 nongji1005**(둘 다 비축, 관문 통과 01:10·01:28이라 기한 02:10·04:10 충족)를 slots.json에 기입한다. 비축 카페는 0/2가 되므로 **firemap-write** 다음 투입의 일 = ① 두 칸 기입 ② 12:10·14:10 칸 편(backlog write 1번 전세보증 SGI·HF 등) 관문 기한 06:10·08:10 ③ 비축 카페 2/2 복구. 16:10~22:10은 meeting 따라잡기 몫.
- [지시] **firemap-video-producer** (대역 02:26, 기한 editor 통과 직후) R-1 v6 43문장 한 날 녹음(lfvoice 관문 그대로) → 렌더·scorecard. 롱폼 다음 칸(meeting이 정함) 24시간 전까지 gates_ok가 목표.

- [지시] **firemap-designer·firemap-improve·firemap-youtube-loop** (대역 21:13, 기한 10/6 12:00) 의도: 사장님과 정한 약속 3건이 commitments.json 기한을 사흘째 넘김(patrol 21:11 위반 7 중 3) — designer '디자인 시스템 v2'(증거 design/system-v2*, 기한 10/2 23:00) · improve '경쟁 조사·review 코드 관문'(ytlong.py에 review.md 확인 0줄, 기한 10/3 12:00) · youtube-loop '주제 후보 점수표 매일'(topics.md 10/2 07:41 뒤 안 고침, 26h 기준). 완료 기준: 각자 ① 끝내서 증거를 만들거나 ② 다른 파일이 이미 그 일을 대신하면 commitments.json evidence를 그 경로로 바꾸고 decisions/log.md에 사유 한 줄 → patrol '약속 기한 넘김' 0 · 우리만 다른 한 가지: 약속을 지운 게 아니라 증거로 닫는다 · 금지: 빈 파일·날짜만 고친 파일로 채우기, 기한만 미루기 · (지운 직원 몫만 중단 10/6)
  착수: firemap-improve 22:44 (improve 몫 '경쟁 조사·review 코드 관문')
  완료: firemap-improve 22:53 — improve 몫 끝: work/ytlong.py gate에 대본 심사 관문(ep/<편>/review.md의 맨 앞 '판정:' 줄 마지막 것이 통과여야 업로드, 미달·보류·막힘은 막음 · 본문 '통과'는 '편집 통과'와 섞여 안 믿음 — D-1이 그걸로 빠져나가는 것 실측) + publishAt 빈 편(R-1) 죽던 것 고침. 실측: D-1·E-2·N-1 gate → "review.md에 '판정: 통과 — 평균 N(통과선 N)' 줄 없음" 막힘, R-1 '예약 시각 없음'. commitments evidence_grep 충족(patrol 약속 넘김에서 improve 빠짐)
  [알림] **firemap-youtube-loop·firemap-video-producer** (improve 22:53): 롱폼 올리기 전 ep/<편>/review.md에 `판정: 통과 — 평균 N(통과선 N) · 담당 HH:MM` 한 줄 필수(없으면 ytlong.py up 막힘). M-1은 표상 평균 7.47 ≥ 통과선 7이지만 판정 줄은 심사 담당이 적는다 · 이미 올린 편 교체 업로드도 같은 관문
  완료: firemap-youtube-loop 00:50 — youtube-loop 몫 '주제 후보 점수표 매일': topics.md 맨 위 '매일 점수표 2026-10-06'(outliers 00:48·kwvol 00:49 숫자로 6주제 판정 — 금 통과 유지, 증여세·상속세·기초연금·국채금리 조건부, 반도체 보류) · commitments evidence 그대로(topics.md, 26h)
  [요청] **firemap-product-dev** ← youtube-loop (00:50) 증여세 계산기 주제 검증(plans/gift-tax-calc.md 맨 위 '검증' 칸) — 네이버 증여세 34,100·증여세면제한도 19,570·증여세계산기 14,450(10/6 kwvol) · 기존 가이드 public/guide/child-gift-tax.html · 상속세증여세법 원문만, 세무 상담 아님 문구 · 근거 longform/loop/topics.md 10/6
  착수: firemap-product-dev 01:37 ([2] 운영실장2)
  완료: firemap-product-dev 01:39 — plans/gift-tax-calc.md 검증 칸: 수요 통과(증여세 34,100·면제한도 19,570·계산기 14,450 재실측) · 경쟁 포화(네이버 1쪽 = 세무사 상담 광고 + taxmade·dawntax·mylawstory·cleantax·홈택스 모두 공제·혼인출산 1억·3% 반영, cleantax 직접 확인) · 이길 점 ①분할증여 시뮬+파이어 연결 1개뿐·경쟁 부재 1곳만 확인 → **판정 보류(조건부)**, 만들기 아님 · 법 원문 상증법 53·53조의2·47·55·56·26·68·69 확인 · 덤: 가이드 child-gift-tax에 혼인·출산 1억 공제·신고세액공제 3% 빠짐 → 글자 수정은 editor-web 관문 필요(트랙 D 후보)
- [요청] 담당 firemap-write ← audit (07:50) 카페 #216 goldway1005: 'KB 골드뱅킹 고시(2026-10-02)' 환율 1,343.85원이 10/2 환율(1,360.59)이 아니라 10/4~10/5 값과 맞음 — KB 고시 날짜 확인, 10/5면 출처 날짜 고치고 '지금은 그 차이가 1%대'를 '1% 안팎'으로 카페 글 수정(10/2 값이면 웃돈 약 0.4%). 결론은 그대로라 경미 · 기한 10/7 · 근거 longform/loop/audit.md 10/6 07:50
- [요청] 담당 firemap-write ← loop (10:07) 카페 주제 고를 때 '예금·이자·금리' 묶음을 앞에: 2일 넘은 카페 138편 하루당 조회 중앙값 — 그 단어 든 제목 22편 1.31 vs 나머지 116편 0.65(2~10일 글만 1.44 vs 0.79). 상위 1·4위가 '예금 N억 이자 + 물음표'(50.1·11.6/일). 금액+물음표 자체는 0.94→2.05로 덜 갈림. 표본 22편이라 '2배'는 단정 아님 — 비축 칸 1개를 이 묶음으로 채우고 10/9 다시 잼(loop) · 근거 perf-notes.md 10/6

- [카피 요청] G-1 금 롱폼 제목·썸네일 문구·첫 3초 트랙:C · 담당 firemap-copywriter · 시한 10/9 21:00 · 근거 longform/ep/G-1/analysis.md ②·⑤·끝 '제목 후보' 3개, compete.md 경쟁 5개 제목 틀 — '금값' 맨 앞, 전망·'지금 사라' 금지, 숫자는 calc 확정 전이라 가안 (youtube-loop 08:56)
  착수: firemap-copywriter 12:48
  완료: firemap-copywriter 12:51 — G-1 1위 제목 '금값 1천만원 영수증 4장, 산 날 따라 677만원부터 975만원까지'·썸네일 '1월 고점에 샀다면 -32.3%'·첫 3초(1/29 677만원→1년 전 975만원) · 심사 3명 평균 7.93(제미나이 7.6·레드팀 8.2·작성자 8) · 2위·지킬 것 ep/G-1/copy/titles.md · 제미나이 1위 C8(방법 비교·'본전')은 레드팀 사실 반려로 탈락 · 숫자는 공개일 calc로 바뀌면 재심사
  [알림] **firemap-youtube-loop·firemap-video-producer** (copywriter 12:51): G-1 제목·썸네일·첫 3초는 ep/G-1/copy/titles.md 1위를 쓴다. meta.json 만들 때 title_candidates로 옮길 것. '달러 금값 +7.8%'는 기준 섞임이라 제목·썸네일에 쓰지 않음
- [요청] **firemap-product-dev** ← youtube-loop (08:56) '산 날·금액 넣으면 내 금 지금 얼마(KRX·ETF·골드뱅킹·골드바)' 계산기 주제 검증 — plans/gold-calc.md 맨 위 '검증' 칸 · 수요 금시세 4,030,000·금현물 18,150·금ETF 10,390(10/6 kwvol) · G-1 롱폼 끝 행동(계산기)·카페 goldway1005와 연결 · 기존 /calc/* 중 쓸 수 있는 것이 있으면 그 경로 한 줄로 끝 · 시한 10/10 · 근거 longform/ep/G-1/analysis.md ⑤ 6장 · **중단(10/6 조직 축소)**

- [요청] firemap-brand-director (firemap-brand-researcher 09:04) 이번 주 새로 알게 된 것 3가지 — ① A-1(JEPQ·SCHD) 조회 2,365의 98.5%가 홈 피드(Browse), 검색 8회, 구독 시청 0.2% → 거의 처음 보는 사람 ② 그런데 조회당 구독은 A-1 0.21%·zhTj(QQQM) 0.61% vs 검색 61%로 온 '5억이면 충분합니다' 1.59% → '이름 있는 영상이 구독을 부른다'는 지지 안 됨, 구독은 검색 유입과 같이 움직임(5편·구독 23명 표본) ③ A-1은 90초(10%)에 남은 비율 0.33 — 초반 이탈이 가장 큼. 판단 요청: 롱폼 제목·첫 30초를 '검색어로 찾는 사람' 쪽에 맞출지 · 근거 work/research/brand/research/persona.md 4회차 · **중단(10/6 조직 축소)**

## 막힘 (풀리지 않은 것)
- 막힘(운영실장 23:16): 10/7 19:20 쇼츠 basecut1006(rate30) 1초 시험 v9·v10 모두 5점 — gates_ok 없음(2a8eca9). 다음 1안: B형 cards 첫 카드 '기준금리 3%' 한 숫자만 재시험, 안 되면 v10으로 칸 채움 · 비축 쇼츠 0/1 · 담당 firemap-shorts · 기한 10/7 07:20
- 막힘(운영실장 11:16): 쇼츠 비축 0/1 계속 — gold1y(goldway1005) 표지 틀 교체 v7 5.0·v8 5.5(고정 조건, 교정칸 유효) 미달(c445461). 다음 1안: v5(7.25) 레드팀 지적(677만원이 원금처럼 읽힘·시점)만 고쳐 재심사, 안 되면 세 길 맞대비+'?' 칸 · 담당 firemap-shorts · 기한 19:20 정기 전
- 막힘(운영실장 10:44): F5 쇼츠 비축 bokrate1006 표지 v8 '최저는?' 고정 조건 평균 5.5(5·6, 교정칸 gongjae1002 7.5 유효) 미달 — 통계표 틀 자체가 경쟁 옆에서 약함. 다음: 표지 틀 교체 또는 다른 사실표(goldway1005) 쇼츠로 비축 교체 · 담당 firemap-shorts · 기한 19:20 정기 전(91259f1)
  착수: firemap-shorts 11:10 (운영실장) — 비축 교체/표지 틀 교체 1안
  완료(미달): firemap-shorts 11:15 — 비축 교체 1안 = goldway1005 사실표 gold1y(spec check '문제 없음'·aitell 0.0·compete 5) 표지 틀 교체. 고정 조건(쇼츠 경쟁5 비교판+judge 질문+gemini-3.1-flash-lite 2회, 상위 모델 0): v7 반전 두 칸(국제 금값(원화) +3.38% / KRX -2.42%) 5·5=5.0, v8 내 돈 한 숫자(1천만원→975만 8천원)+반전 알약 5·6=5.5, 교정칸 gongjae1002 7.5·7.0 / 7.0·7.5 유효 → 미통과, gates_ok·reserve.shorts 안 넣음(레드팀은 제미나이 단독 7 미만이라 생략). 지적: '표처럼 보임'·'975만이 줄어든 돈인지 모호·다른 길 대비 기대감 없음'. 다음: gold1y는 v5(677만 -32.3%, 제미나이 7.25)가 최고 — v5를 레드팀 지적(677 원금 오독·시점)만 고친 판 또는 세 길 맞대비+'?' 1안, 기한 19:20 정기 전 (cardshorts/gold1y/review_cover.md 끝)
- 막힘([2] 운영실장2 07:45): 쇼츠 비축 bokrate1006(기준금리 1999년 이후, ECOS 722Y001) 표지만 미달 — v5 평균 6.33(제미나이 7·A 5·레드팀 7), v6·v7은 제미나이 상위 한도로 lite 5점(e0e88b8). 다음: '최저 ?' 노랑 큰 글자 주인공 판(cardshorts/rate30/review.md) · npsday1007 관문 손 못 댐(기한 10/7 00:20, 안 되면 nongji_age 교체 규칙) · 담당 firemap-shorts · 기한 12:20 정기 근무
  착수: firemap-shorts 08:10 (운영실장) — npsday1007(10/7 12:20 쇼츠) compete·공단 교차확인·관문(기한 10/7 00:20)
  완료: firemap-shorts $T — npsday1007 compete 5·공단 교차확인(facts.txt)·check(layout 한 줄 제외)·카피 통과·표지 v2 제미나이 7.5·A 5·레드팀 5=6.2 미통과 → gates_ok 안 적음(cardshorts/npsday1007/review.md). 남은 관문: 표지 v4(경계 한정 문구·글자 안 잘리게)·review 세 줄 확정, 기한 10/7 00:20, 안 되면 nongji_age류 비축 교체
- 처리(대역 06:59): 쇼츠 비축 0/1(patrol) → 기준금리 30년 표(ECOS) 관문 통과로 reserve.shorts 1/1 · 담당 firemap-shorts · 기한 12:00 / 약속 넘김 '디자인 시스템 v2'(patrol 유일한 약속 위반) → 대역 21:13 지시 기한 그대로 · 담당 firemap-designer · 기한 12:00, 못 닫으면 21:15 안건
- 진행([2] 운영실장2 05:44): F4 retmid1005 표지 3.1-lite v4 7.75·v5 7.0 통과, 남은 것 레드팀·작성자 점수·제목 심사 3명·editgate → reserve.cafe gates_ok · 담당 firemap-write
- 막힘(PD 16:23): R-1 목소리 관문 — 제미나이 TTS 153문장 한 날 녹음했지만 f0 ±12% 밖 81줄. 같은 모델은 날·요청마다 높이가 흔들려 다시 녹음도 같은 결과 가능성 큼(E-2 37%·N-1 22%도 밖). 처리: 결재함 'Chirp 3 HD 결제 연결' · 담당 사장님(결제)·순돌이(보고) · 그동안 PD가 10/6 16:01 한 번 더 녹음 시도
  처리(대역 20:00): 롱폼 10/6 19:30 칸 관문 기한 10/6 19:30 — 10/6 16:01 재녹음이 마지막 기회. 못 넘으면 칸 skip 표시하고 다음 칸 10/7 19:30·비축 롱폼 후보(M-1 대본 편집 통과)를 youtube-loop이 PD 넘김 앞당김 · 담당 firemap-video-producer·firemap-youtube-loop · 기한 10/6 18:00
  진행(youtube-loop 20:51): 10/6 칸은 slots.json에 이미 skip(05:4x) 그대로. 비축 후보 M-1 대본 심사 3명 v1 평균 7.47 통과(제미나이 7.8·Claude 7.4·레드팀 7.2, 숫자 불일치 0) → 공통 지적 고친 script.v2.md · review.md 세 줄 기록. 남은 것: 편집 재검수(v2 변경 말 줄) → PD 넘김. 목소리는 R-1과 같은 TTS 음높이 막힘(결재 Chirp 3 HD)이라 다음 롱폼 칸은 10/6 16:01 재녹음 결과 보고 PD가 R-1/M-1 중 정함
- 빠짐(운영실장 13:02): 정기 근무가 10/2 뒤로 한 번도 안 뜬 직원 8 — planner(08:30·11:30)·editor-web(08:10)·editor-en(10:10)·behavior(10:50)·venture-builder(09:40)·venture-research-global(08:20)·venture-research-kr(09:20)·improve(10/4 22:30). 예약은 켜짐(enabled)인데 lastRunAt 10/2 그대로 — 순돌이 채팅 세션에서 예약 상태 확인 필요. 그동안 운영실장이 열린 태그 있는 직원부터 Agent로 투입(13:0x planner·editor-web)
  확인(admin 19:09): 19:0x list_task_runs — planner·editor-web·editor-en·behavior는 여전히 10/2가 마지막 / venture-builder(18:57)·research-global(17:58)·research-kr(14:04)·improve(14:44)는 다시 뜸 / **새로 빠짐: soondol-deputy 06:34 뒤 08:20~18:20 여섯 회차 안 뜸**(lastRunAt 그대로, nextRunAt 20:21). 원인 확인 안 함 · 담당 순돌이(채팅 세션) · 기한 21:00
  처리(대역 20:00): soondol-deputy는 20:00 회차 뜸(이 줄). 나머지 4명은 운영실장 Agent 대신 투입 유지 → 21:15 안건 · 담당 firemap-dispatcher · 기한 21:35
- 멈춤: firemap-meeting 10/4 21:28 시작 회차가 아직 running(마지막 활동 21:42, admin 07:11 list_task_runs 확인) — 오늘 21:28 회차가 막힐 수 있음. 무인 회차는 세션 중지 못 함 → 순돌이 채팅 세션에서 중지 · 담당 순돌이 · 기한 오늘 21:00
  확인(admin 19:09): 19:0x list_task_runs에도 그대로 running(마지막 활동 10/4 21:42) → **오늘 21:28 회의가 안 뜰 가능성 큼**. admin이 stop_session 시도 → 'unattended sessions에서 쓸 수 없음' 거절. 채팅 세션 몫 그대로 · 기한 21:00
  처리(대역 20:00): 21:15 회의가 안 뜨면 운영실장이 21:35 회차에 Agent로 회의 투입(위 [지시]) · 담당 firemap-dispatcher · 기한 21:35
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
- [막힘 07:51] [2] firemap-designer 연봉 결과 시안 v3 미통과(평균 6.83, 기준 7, 717433e) — 다음 회차 공통 지적 3개(아래 고정 버튼 마감·버튼↔숫자 시선 분산·입력칸 모양 통일) · 비축 카페 1/2 그대로, 22:10 TBD-D 관문 기한 16:10 (다음 배차 1순위) · **중단(10/6 조직 축소)**
- 막힘(운영실장 08:15): firemap-designer 연봉 결과 시안 v4(2판) 평균 6.83 — 7 미달(기한 12:00). 제미나이 flash 429·lite 7판 내리 6.5 고정이라 판을 못 가름. 남은 점: 320px 첫 화면 버튼·데스크톱 배치·다크 카드 색 3가지 → designer 10:20 정기에서 마감 뒤 flash 풀린 시간에 재심사(371ab4b)
- 신사업 실측(본부장 13:32): X-V1·X-CN-1 **10/2 뒤 외부 방문 0**(firemap_events 10/2 13:00~ 행 14개 전부 internal·127.0.0.1, 측정은 살아 있음 — 13:31 내 열기 1행 들어옴) · **구글 site: 0쪽**(13:3x, 공개 4일) · 매일 원문 대조 Actions는 10/3~10/5 매일 돎 · v2 화면은 디자인 반려(6.67·6.83, design/review-v2/review.md) 뒤 미배포. 병목 = 화면이 아니라 **발견(색인·들어오는 링크 0)**.
- [순돌이 16:4x] 목소리 관문 기준 실측으로 고침(줄 ±12% → 튀는 줄 ±25% + 편 단위 앞뒤 차 ≤7%·퍼짐 ≤0.16, 근거 E-1·D-1 좋음 vs E-2 지적). R-1 지금 녹음은 새 기준으로도 막힘(앞뒤 +8.3%·퍼짐 0.22·중앙 136Hz로 다른 편 150~157보다 낮음) → **firemap-video-producer**: R-1 다시 녹음(한 회차·한 날). 제미나이 무료 한도로 한 날에 다 못 하면 결재함 'Chirp 3 HD'(구글 클라우드 음성, 무료 월 100만 자) 결제 연결이 풀어 줌 — 사장님 대기.
  착수: firemap-video-producer 18:08 — TTS 한도 소진(16:23 10회 다 씀)이라 재녹음은 10/6 16:01. 그 사이 녹음 뒤 음높이 맞춤 시험
  진행: firemap-video-producer 18:17 — work/lfpitch.py(rubberband·옮김 ±15%·앞뒤 무음 0.1초)로 오늘 녹음 → 앞뒤 차 +3.0%·퍼짐 0.08·편 전체 6.14 = 음높이·전체 속도 통과, 줄 속도 27줄(2장 9~10음절/초)만 남음 · 10/6 순서 ep/R-1/check/runbook_1600.md 끝 절 · 완료는 10/6 재녹음 뒤
  진행: firemap-video-producer 18:42 — (10/6) 막힘 원인 실측: 기본 지시문 4편 f0 144~157·IQR ≤0.16 통과 vs R-1 'even pitch' 지시문 2회 130~139·IQR 0.18~0.21 → R-1 재녹음은 tts.json prompt 빼고(전부 다시 녹음), 날은 M-1(10/7) 뒤 · 근거 ep/M-1/check/runbook_1007.md 표
- [요청] firemap-venture (해외 시장조사원 18:25) 실험 제안 2개 트랙:A · 시한 10/6 18:00 · 근거 ventures/candidates.md 10회차·ventures/g44/compare.md · **중단(10/6 조직 축소)**
  착수: firemap-venture 20:29
  통과: ① G48 20:29 (firemap-venture) — Etsy 묶음 첫 상품으로 채택(위 Etsy 줄). 조건: research-global ventures/g48/compare.md(1~3점 리뷰 불만 1순위·무료판 비교·코드 검산 차별) 10/6 18:00까지 → 그 뒤 빌더 지시서. Etsy AI 사용 표시·Creativity Standards 문구는 결재 나면 확인.
  보류: ② G44 20:29 (firemap-venture) — 새 유튜브 브랜드 채널 = 계정 결재(X-G19와 같은 종류, 둘 다 대기). 같은 결재 하나로 두 채널을 열지 않음 → X-G19 결재 카드에 "대안 G44(ja 60분 듣기)" 한 줄로 붙여 사장님이 하나 고르게. 유튜브 본부(youtube-loop)와 겹침 확인 필요 — [요청] 아래.
  ① **G48 인쇄 방탈출 키트(크리스마스판)** — Etsy 1등 'Monster Hotel' $18.25 r2,344, 'Santa is Missing' $19.33 r237. 첫 판(하루): 퍼즐 8~10개+이야기 PDF 1개, 정답 코드 검산. 지표: 공개 7일 조회·즐겨찾기·판매 1건. 판정 공개+7일. 결재: Etsy 계정(10-05 14:03 결재 요청과 같은 것) — **$1 인쇄물 10개 대신 방탈출 1개를 첫 상품으로** 넣으면 같은 결재로 객단가 6~10배.
  ② **G44 일본어 聞き流し韓国語 60분 채널** — AI 음성 명시 채널 MaruMaru Korean 7개월 5,150명·60분 묶음 9.9만회(1개월) = 사람 목소리 없이 된다. 첫 판(하루): 60분 1편(ja→ko TTS, Remotion). 지표: 7일 조회·구독. 판정 공개+7일. 결재: 새 유튜브 브랜드 채널(X-G19와 같은 종류) — 유튜브 본부와 겹침 여부는 본부장 판단.
- [순돌이 19:3x] 주간 사용량 15%(10/4 21:00 초기화 뒤 22.5시간, 시간당 ~0.67%p) → 이 속도면 리셋 전 약 112%(admin 19:00 예측 113%와 같음). 지난주처럼 막판에 멈추지 않게 지금부터: ① 순돌이 순찰 30분→60분(이 대화가 길어 한 번 돌 때 크다 — 제일 먼저 줄임) ② 내일 10/6 12:00 다시 재서 시간당 0.55%p 넘으면 회의가 정기 근무 중 성과 낮은 것부터 회차를 줄인다(직원별 사용량은 확인 안 함 — admin이 실측 방법 찾기).
  확인(admin 07:04): 주간 **23%**(시간당 0.67%p 그대로 → 리셋 전 약 112%, 98% ≈ 10/10 19시). 직원별 토큰은 잴 수단 없음 → 근무분으로 대신 잼(admin/usage.md 표: dispatcher·video-producer·write·dispatcher-2·visual-designer 순). [제안] **firemap-meeting**(또는 순돌이) 축소안 — ① artist 3→1회 ② illustrator·brand-researcher 주 2회 ③ venture-research-kr·global 2→1회(발행 영향 0) ④ 부족하면 dispatcher-2 야간만 · 예약 수정은 무인 권한 밖이라 채팅·회의 몫 · 기한 오늘 21:15 · 신규 채용 보류
  완료: firemap-meeting 10:51 — 순돌이가 10/6 10:41 사장님 지시로 예약 21개 삭제(축소안보다 큼) → 이 제안은 닫음. 사용량 관리는 순돌이 순찰(meeting/2026-10-06a-decisions.md D7)
- 멈춤 그대로(admin 07:04): firemap-meeting 10/4 21:28 회차 아직 running → 10/5 정기 회의 안 뜸(lastRunAt 10/4). 오늘 21:28도 막힐 가능성 큼 · 중지는 순돌이 채팅 세션 몫
- 예술가 제안: **부모님께 보내는 큰 글씨 결과(AU)** 트랙:B — 연금 계산 결과에 버튼 1개 → 큰 글씨 한 장('매달 ○○만원 · 받기 시작 ○○년 ○월 · 문의 1355', 숫자는 URL에만·저장 0, R36 약속표 링크 방식 재사용) · 문구는 확인용(권유·평가 말 금지, 세대 간섭으로 읽히지 않게) → 담당 firemap-planner(plans 한 장 → product-dev), 시험 기한 10/19 · 성공: ?big=1 진입 세션 ≥20(14일) 또는 버튼/결과 ≥5% · 버림: 둘 다 미달이면 R36 약속표 한 곳으로 합침 · 근거 art/2026-10-05-1952.md AU (artist 19:58)
  중단: firemap-artist 14:51 — 10/6 조직 축소로 planner·product-dev 없음·사이트 새 개발 중단 → AU 보류(ideas.md 보관), 사이트 재개 때 R36 약속표와 함께 다시 꺼냄
- [요청] 푸시 기본 문구 '확인' 두 번 정리(b3d54a6, supabase/functions/send-fire-clock/index.ts 1줄) — 엣지함수 배포해야 라이브 반영 · 담당 firemap-product-dev · 시한 10/7 · 근거 editor-web/sweep.md 18번 · 파이어맵 Supabase(cvhskxdwqubmshdgkzhj)만 (editor-web 20:12) · **중단(10/6 조직 축소)**
- 신사업 실측(본부장 20:29): X-V1·X-CN-1 10/5 13:30~20:2x 외부 방문 0·수익 0원(firemap_events 14행 전부 직원·로컬). 판정 10/8 22:00 그대로.
- 확인(firemap-editor-en 21:22): editor-en 정기 근무 10/5 21:15 회차 뜸(10/2 뒤 첫 회) · 영어 [편집 검수 요청] 0건 · kit/template-en.html 오류 문구 자리·함정 주석 5d1a66f
- [요청] **firemap-video-producer** ← motion (23:59) M-1 첫 장면 모션 ReverseAsk 심사 통과(평균 7.0) — M-1 녹음 뒤 m1props.py 프레임을 voice.json으로 다시 맞추고 open 장면에 넣기 · 절차 research/longform/ep/M-1/motion.md · 미리보기 motion_preview/m1_open.mp4
  - 추가(motion 11:44): 첫 30초 힘 고침 — hook(0~2초 '매달 100만원')·큰돈 판 전환·말3 당김·도장 띠·끝 다가감, 재심사 평균 6.7(7·7·6) · 본편 ep/M-1/m1props.py에 hook·stamp·fwd·grow 이미 반영(녹음 뒤 그대로 돌리면 됨) · 화면 글자 4칸 늘어 lfrender text 뒤 편집 stamp 다시 · 렌더 뒤 확인 3개(레드팀 조건): hook·stamp 나옴 / motioncheck 최장 정지 3초 이하 / 58초 막대 이름 안 잘림
  착수: firemap-video-producer 02:26 (M-1 화면 먼저 — TTS 한도 16:00 전)
  진행: firemap-video-producer 02:44 — ReverseAsk를 open 장면에 넣음(프레임은 지금 어림 길이로, 녹음 뒤 m1props.py 다시 돌리면 voice.json 길이로 맞춰짐 — 별도 손질 불필요) · M-1 화면 전체: video/src/M1.tsx 장면 24·종류 15 + parts/reverse.tsx 새 부품 8 + ep/M-1/m1props.py(calc_out·facts 원문 줄 기계 대조, 대본 93문장 빠짐 0) · 스틸 48+2장 눈 검사 → 겹침·잘림 9곳 고침(video/out/m1_stills_0330) · 어림 7.3분 · compete.md(30일 상위 5) · 남은 것: 화면 글자 편집 통과 → 녹음 → 렌더·scorecard·썸네일·gate
  [편집 검수 요청] M-1 화면 글자 ep/M-1/screen_text.txt(525줄, lfrender text 02:44) 트랙:C · 담당 firemap-editor · 시한 10/6 15:30(녹음 전) · aitell 1.6 통과 · 통과면 `py -3.12 work/lfrender.py stamp work/research/longform/ep/M-1 firemap-editor "<본 것>"` · 숫자는 calc_out·facts 원문 그대로라 숫자 바꾸지 말 것(말투·용어만)
  착수: firemap-editor 02:46 (운영실장)
  완료: firemap-editor 02:50 — M-1 화면 글자 편집 통과(525줄 전부, aitell 1.6, 숫자 0 변경) · stamp 찍음 · 고침: 출처줄 'calc_out' 내부 파일명→'파이어맵 계산' 7곳, 9번 장면 '건보·세율은 2장'→'세율 1장 · 건보료 2장'(m1props.py) · 남긴 것 '(하한)'·'끝날 환율'은 script.v2.md 자막(youtube-loop 몫). 녹음 뒤 m1props 다시 돌려 screen_text 재뽑기 필요
  [알림] **firemap-youtube-loop** (PD 02:44): 10/6 16:01 TTS 한도(하루 10요청)는 R-1 재녹음과 M-1 녹음(93문장 ≈ 9요청)을 둘 다 못 채움 — 한 편 한 날 녹음 규칙. 18:00 판정 전에 어느 편에 쓸지 16:00 전까지 정해 주세요. PD 제안: R-1은 같은 도구로 10/5 81줄 밖 → 다시 해도 막힐 가능성 큼, M-1은 화면이 다 돼 있어 녹음만 넘으면 바로 렌더 가능 → **M-1 먼저**(근거 STATE.md 10/5 16:23·22:28)
  완료: firemap-youtube-loop 04:47 — **10/6 16:01 TTS = M-1**(PD 제안 그대로: R-1은 같은 도구로 f0 밖 81·lfpitch 블라인드 탈락 → Chirp 3 HD 결재 뒤). slots: 10/7 19:30 롱폼 skip(관문 기한 10/6 19:30에 녹음 16:01이라 불가) · **10/8 19:30 롱폼 = M-1**(기한 10/7 19:30) · 비축 롱폼 1순위 M-1. 자막 youtube-loop 몫 2곳 고침: '(하한)'→'(최저 보험료)', '끝날 환율 근사'→'2026-10-02 환율(1달러 1,359.6원)로 바꾼 어림값'(facts [X1]) — script.v2.md·m1props.py 같이, 말 줄 0 변경(say_v2 그대로)
  [편집 검수 요청] M-1 script.v2.md 자막 2줄 재서명 + 녹음 뒤 screen_text 재서명 트랙:C · 담당 firemap-editor · 시한 10/7 12:00 · 근거 ep/M-1/script.v2.md 60·155행 · 숫자 바꾸지 말 것
  착수: firemap-editor 06:54 (정기 06:50)
  완료(자막 몫): firemap-editor 06:57 — script.v2.md 60·155행 facts H4·X1 일치, 재서명(script.v2.md.edit.json sha 61ab265f) · 말 줄 0 변경 · 녹음 뒤 screen_text 재서명은 남음(16:01 뒤)
  완료(중간): firemap-editor 16:58 — M-1 screen_text 녹음 전 재뽑기(lfrender check가 m1.json 04:45로 다시 씀) 바뀐 4줄 facts H4·X1 일치 → stamp. 모션 새 글자 4칸(hook·stamp)은 대본 2·4줄과 같은 말로 미리 봄 — 녹음(10/7 16:00) 뒤 m1props 재실행하면 다시 stamp 필요
  [알림] firemap-write: 18:10 toejikavg1006 c01·c03, 22:10 bigwa1006 c01·c02 문장 editor가 고치고 editgate 다시 찍음(12:10, 숫자·링크·면책 0 변경 — toejikavg 끝 안내가 '월급만 넣어서'라 본문과 어긋나 계산기 칸 '상여금 · 연차수당'으로) — 발행 그대로 진행
  [알림] firemap-write: 10:10 yujokstop1006 c01·c02 문장 3곳 editor가 고치고 editgate 다시 찍음(06:57, 숫자 0 변경) — 발행 그대로 진행
  진행: firemap-video-producer 06:42 — M-1 목소리 없이 되는 단계: meta.json(제목 T1·설명란 틀 desc_tpl·출처·AI 음성·카페 1·태그 5·publishAt 10/8 19:30·5문항·쿠팡 안 붙임) · scorecard.md 경쟁 칸(중앙값 25, 자막 3편 실측) · cafe.md · 쇼츠 재료 cardshorts/m1_reverse·m1_lowmonth·m1_jepqtotal.json · 썸네일 10시안·8차 심사(visual/M-1-thumb/judges.md) — 세 명 평균 최고 m1i 6.92, **7 미달로 확정 안 함**(임시 m1i). 남은 것: 16:01 녹음 → script.md=script.v2(editor 재서명 뒤) → m1props → 렌더
  [요청] **firemap-visual-designer** ← PD (06:42) M-1 썸네일 관문(기한 10/7 19:30, 롱폼 10/8 19:30 칸) — 숫자판 손질 10시안이 세 명 평균 6.4~6.92에서 멈춤(제미나이 3.1-lite 7~7.25·Claude 7.0·레드팀 5~6.5). 세 명 공통: 어두운 숫자판은 경쟁(밝은 바탕·얼굴·금화) 옆에서 '다르다'는 되지만 '먼저 누르고 싶다'가 약함 → 문구가 아니라 판 자체(밝은 바탕·그림 장치 크게) 시안 1~2장. 근거·숫자 assert·심사 스크립트 visual/M-1-thumb/(make_thumbs.py·judge.py·judges.md 다음 후보 줄) · 사실은 calc_out·facts K1만 · 통과면 meta.json thumb·thumb_status 갱신
  착수: firemap-visual-designer 09:08
  완료: firemap-visual-designer 09:19 — M-1 썸네일 **m1i 확정**(13·14차 세 명 평균 7.0·7.33, 1초 블라인드 매번 맞힘, 목표 8 미달) · 밝은 판 6장(m1k~m1r) 최고 m1o·m1r 7.0 → 예비 thumb_m1r.png(48h CTR 교체 1회 후보) · m1i 각주 '세금·건보료 뗀 뒤'로 고침 · meta.json thumb·thumb_status·thumb_alt · 근거 visual/M-1-thumb/judges.md 9~14차 · PD: 레드팀 사실 메모(8.92억은 연 분배 2,747만원이라 종합과세 전 하한) 대본 4장 표기 확인 부탁- [순돌이 10:5x · 사장님 '불필요한 자동 예약 지워'] 삭제: 끝난 1회용 4개(usage-restore-1004·e1-q4·designer-orgchart·titletest-followup, SKILL.md는 남김). 줄임(admin 07:04 근무분 실측 축소안 그대로): artist 3→1회(14:40)·illustrator 매일→월·목·brand-researcher 매일→월·목·venture-research-kr·global 2→1회. 스꾸 쪽 예약(seukku-*·9/8~9 꺼진 알림 3개)은 손대지 않음. 다음 단계(admin 안 ⑤): 19:00 재측정 시간당 0.58%p 넘으면 dispatcher-2 야간만.
  완료(PD 몫): firemap-video-producer 10:39 — 대본 v2 122행 자막에 이미 "연 세전 분배 약 2,746만원 → 2,000만원 선 넘음, 추가 세금·건보 계산 안 함 = 최소값"(calc_out 15,693,413원×1.75 = 27,463,473원, 2,747은 반올림한 8.92억으로 곱한 값) · 화면 m1props jump 칸도 "×1.75 · 최소값" → 고칠 것 없음
- [순돌이 11:0x · 사장님 '카페·쇼츠·롱폼 관련 예약 빼고는 다 지워. 사이트 개발하는 건 별로'] 예약 21개 삭제(product-dev·venture 4종·designer·editor-web·editor-en·illustrator·brand 2종·admin·ai-lab·bizdev·behavior·planner·growth·deputy·finishline·dispatcher-2·monthly-report — SKILL.md는 남음). 남은 직원 16(카페·쇼츠·롱폼 제작·편집·감사·발행 감시·회의·운영실장). 사이트 새 개발 중단, 운영 화면은 그대로. 스꾸 예약은 손 안 댐. 사용량 관리는 순돌이 순찰이 맡음(admin 없음).
- 막힘(firemap-report 12:42): 작업 폴더에 public/guide/marriage-childbirth-gift-deduction.html 이 지워진 채(' D') 남음 — 원본은 dev·main 9b44e22에 정상. report가 merge 대신 merge-tree로 합친 뒤 파일 꺼내기가 권한에 막힘. 'git commit -a'·'git add -A' 금지 · 순돌이: git checkout HEAD -- public/guide/marriage-childbirth-gift-deduction.html
- 막힘(firemap-r1-record-1006 16:29): R-1 v7 오늘 19:30 공개 못 함 — 94줄 한 창 녹음은 끝났으나 목소리 관문 IQR 0.18(>0.16)·편 전체 5.12음절/초(<5.5)·튀는 줄 9, 대본 재심사 5.97 미달도 겹침. 묶음(요청)마다 음높이 122~156Hz 차이가 원인(같은 묶음 재녹음해도 156Hz). 결정 필요 · 담당 순돌이: lfpitch 사본 소리 심사 / 줄 앞뒤 무음 다듬기 허용 / 대본 고친 뒤 다른 날 재녹음 중 무엇 · 10/7 16:00 창은 예정대로 M-1
  참고: firemap-video-producer 18:42 — 판단 재료: lfpitch·무음 다듬기 전에 지시문부터 의심. 무음은 통과한 E-1·D-1도 줄당 0.8초라 속도 막힘의 주원인 아님, 'even pitch' 지시문 쓴 두 번만 낮고 느림(runbook_1007.md 표). 표본 1편이라 확정 아님 — 10/7 M-1(기본 지시문) 녹음이 대조군
- [대기열] firemap-youtube-loop G-1 금 롱폼 calc.py → 대본 v1(100줄 이하) → 검증·심사 (backlog 31행)
  착수: firemap-youtube-loop 19:08 (운영실장)
  완료: firemap-youtube-loop 19:12 — G-1 calc.py까지(이번 조각): 네이버 증권 front-api(옛 금 일별 페이지 폐지)·야후 ETF·GC=F·ECOS로 공개일 기준 다시 받기, 영수증 산 날 4×산 길 4·세 조각 곱 분해(검산 일치) · 10/2 기준으로 옛 숫자 그대로 재현(677.4만·975.8만·+47.6%) · **10/6 기준은 663.4만·955.7만·고점 -33.66%·+50.7% → 공개 전날 calc 뒤 카피 재심사 필요** · 남은 것: 대본 v1(100줄)→제미나이 검증·심사 · 근거 ep/G-1/calc_out.txt·facts.txt [C1]
  착수: firemap-youtube-loop 20:48 — G-1 대본 v1(100줄 이하)·숫자 대조·제미나이 검증
  완료: firemap-youtube-loop 20:59 — G-1 대본 v1 script.md(=script.v1.md, 말 80줄·7장, 숫자 기준일 10/6 calc_out) · scriptnum 54개 중 사실표 밖 0 · aitell script 통과(73.1/1,000단어·숫자 2개+ 문장 6%, 첫 초안 157·33% 실패 → 날짜·정확값을 자막으로) · aitell text 0.0 · 제미나이 3.6-flash 검증 막을 문제 0·고칠 것 1(곱 표기 → (1+x) 꼴, 고침) review_v1_gemini.md · facts [S] 말하는 단위 표 추가 · **카피 1위 677·975는 10/2 기준, 10/6 기준 663·956** → 공개 전날 calc 뒤 카피 재심사
- [편집 검수 요청] G-1 대본 v1 트랙:C · 담당 firemap-editor · 시한 10/7 18:00 · 근거 longform/ep/G-1/script.md(말 80줄, say_v1.txt) · facts.txt [S] · 금지: 숫자·날짜 바꾸기, 전망 문장 넣기 (youtube-loop 20:59)
  착수: firemap-editor 23:09 (운영실장)
  완료: firemap-editor 23:11 — G-1 대본 v1 편집 통과(트랙C 전건) · humanlike AI 티 0.0→0.0, 말 6곳만 말투 손질(숫자·날짜·전망 0 변경, 끝맺음 -죠·-거든요 섞기), 원본 *.orig · script.md.edit.json
- [카피 요청] G-1 제목·썸네일 숫자 기준일 맞춤 트랙:C · 담당 firemap-copywriter · 시한 공개 전날 calc 직후(10/9 칸이면 10/8 21:00) · 근거 ep/G-1/calc_out.txt(10/6: 고점 663만원 −33.66%·1년 전 956만원, 10/2 가안 677·975·−32.3%) · copy/titles.md '꼭 지킬 것' (youtube-loop 20:59)
- [대기열] firemap-improve shortsdaily check에 제목 '·' 빈칸 글자 경고 (backlog 32행)
  착수: firemap-improve 19:08 (운영실장)
  완료: firemap-improve 19:13 — shortsdaily check에 제목체(BlackHanSans) 글자 없는 글자(·) 빈칸 경고 추가(제목 줄·표지·큰 글자 대상, 공개 막음). 실측: 10/5 a1_1eok1y 원고에서 "카드 제목 글꼴에 '·'(U+00B7) 글자가 없어 빈칸으로 나옴" 적발. 카드 아래 빈칸은 backlog에 남김

- [배차] firemap-shorts 10/7 19:20 칸 basecut1006 관문(gates_ok 없음, 기한 10/7 07:20)
  착수: firemap-shorts 03:09 (운영실장) — 1안 B형 첫 카드 한 숫자, 안 되면 rate30_v10으로 칸 채움(기한 07:20)
  완료: firemap-shorts 03:27 — basecut1006 관문 통과: rate30 B형 cards(rate30_b.json, 첫 장 '지금 3%' 계기판 25초, rate30_b.mp4 렌더) 첫 프레임 1초 시험 고정 조건 7·7(v9·v10 5)·블라인드 주제 맞힘 글자 읽힘 '예'·카피 8·8·레드팀 1초 7/카피 6/사실 오류 0(지적 3 반영)·aitell 0.0 → slots.json gates_ok 2026-10-07 03:26. 19:20 공개는 rate30_b.json으로(rate30_v10 채움안 안 씀) · 근거 cardshorts/rate30/review.md 끝
  착수: firemap-shorts 23:09 (운영실장)
  완료(미달): firemap-shorts 23:15 — basecut1006(=cardshorts/rate30, 사실표 bokrate1006) 한은 홈페이지 교차확인 일치·'2008년 2월까지 콜금리 목표' 주석 추가·check 통과·compete 5. 첫 프레임 1초 시험 v9 5·v10(답 먼저 '기준금리 3% / 최고 5.25% / 최저 0.5%') 5 미달(블라인드 주제 맞힘, 글자 '일부') → gates_ok 안 적음. 다음 1안(기한 10/7 07:20): B형 cards 첫 카드 '기준금리 3%' 한 숫자, 안 되면 rate30_v10.json으로 칸 채움(비축 0이라 교체 편 없음) · 근거 cardshorts/rate30/review.md 끝
- [알림] **firemap-video-producer·firemap-copywriter** (youtube-loop 00:53): M-1(10/8) 같은 틀 경쟁이 새로 떴다 — 데일리대일 NiEyYRen--A '같은 S&P500인데 5배 넘게 배당 나오는 국내, 해외 월배당 ETF' 6.1배·17.9만(쇼츠 156초). 장마다 '월 200만원 받으려면 원금 얼마'를 표시 분배율로 나눔, 세금·건보료·환율 0(breakdown/NiEyYRen--A_break.md). M-1 compare.md 두 번째 비교 대상으로 쓸 것 · 제목에서 '월 N만원 받으려면 원금' 틀이 겹치면 우리는 '세후'·'건보료'를 앞에 · 새 숫자 0
  착수: firemap-copywriter 01:49
  완료: firemap-copywriter 01:55 — M-1 제목 1위 **T1 → N4 교체** 'JEPQ 1.38억, SCHD 4.85억, ACE 5.10억 — 세금·건보료 뗀 월 100만원에 드는 원금'(3명 8.13) · 2위 N4b '…원금, SCHD는 3달에 한 번 들어온다' · 이유: 데일리대일 제목과는 겹침 0이지만 yt_top30에 김범곤 9/16 '월 100만 원 배당받으려면 얼마가 필요할까?'(9.0만)가 T1과 같은 틀 · N2 'JEPQ·SCHD·ACE 월배당'은 SCHD 분기라 사실 반려 · meta.json title·title_candidates·title_swap 갱신 · 근거 ep/M-1/copy/review.md
  [알림] **firemap-video-producer·firemap-youtube-loop** (copywriter 01:55): M-1 업로드 제목은 meta.json title(N4)을 쓴다. 썸네일 m1i는 그대로(제목 ACE 5.10억 ↔ 썸네일 ACE 8.92억 차이가 궁금증). 설명란 첫 줄 '받으려면 얼마가 있어야 할까요?'는 문장이라 둬도 되지만 제목 말과 맞추려면 desc_tpl 손질은 PD 몫. 제목 aitell 0.0
  완료: firemap-copywriter 01:55 — backlog 1칸 E-2·N-1 48시간 판정: reach 10/4분까지 E-2 노출 28(12.5%→0%)·N-1 173(8.7%, A-1 같은 기간 8.7~9.7%) → 교체 안 함(노출 부족, 클릭률 문제 아님) · learn.md
  완료: firemap-youtube-loop 00:53 — 10/7 매일 연구(longform/loop/study/2026-10-07.md: A-1 홈 노출 10/4 2,633→62·N-1 첫날 173·8.7%) · topics.md 매일 점수표 10/7(새 통과 0, 퇴직 건보료·예금 금리 조건부) · shorts-research 루프 규칙 1줄(제도형 vs 종목형, 표본 부족) · RULES 관찰 1줄 · G-1 대본 심사 3명 진행 중
  완료: firemap-youtube-loop 00:58 — G-1 대본 심사 3명 평균 **7.80 통과**(제미나이 8.2·Claude 7.8·레드팀 7.4, 숫자 불일치 0) · 막는 지적 반영 v2(말 7줄, 새 숫자 0: 골드바 '살 때 수수료' 단서·약속 좁힘·'1톤'·'9월 확인 전'·끝 행동 둘째 삭제) · scriptnum 0·aitell 통과 · ep/G-1/review.md 판정 줄 · 남은 막음: 제목·썸네일 10/2 기준 숫자(공개 전날 calc 뒤 한 번에)
- [편집 검수 요청] G-1 v2 바뀐 말 7줄 재서명 트랙:C · 담당 firemap-editor · 시한 10/7 18:00 · 근거 longform/ep/G-1/review.md 'v1 → v2'(script.v1e.md ↔ script.md diff) · 금지: 숫자·날짜 바꾸기 (youtube-loop 00:58)
  착수: firemap-editor 03:09 (운영실장)
  완료: firemap-editor 03:12 — G-1 v2 바뀐 말 7줄 재서명 통과(diff v1e↔v2 7곳 전부 확인: 숫자·날짜 변경 0, '약 91만원'은 facts 57행 909,091원, 전망 0) · humanlike AI 티 0.0·aitell script 71.5/1,000단어·2개+ 문장 7% 통과 · script.md.edit.json 새 sha 758132ec
- [편집 검수 요청] G-1 화면 글자 screen_text.txt(598줄, lfrender text 02:38) 트랙:C · 담당 firemap-editor · 시한 10/8 12:00 · 근거 ep/G-1/screen_text.txt(props video/g1.json·G1.tsx) · aitell 2.3 통과 · 숫자는 calc_out 10/6 기준 — 공개 전날 calc 재실행하면 g1props 다시 돌려 재서명 필요 · 요청 firemap-video-producer
  착수: firemap-editor 03:09 (운영실장)
  완료: firemap-editor 03:12 — G-1 화면 글자 598줄 편집 통과·stamp 찍음(screen_text.edit.json) · 말 줄 79개 = say_v2와 글자 일치, 숫자 calc_out 10/6 일치·전망·권유 0 · 참고(막지 않음): scenes.11 달러 금값 '-21.62%'만 하이픈(나머지 −) — g1.json 다음에 고치면 재뽑기·재서명
- [요청] **firemap-youtube-loop** ← PD (06:22) M-1 review.md에 `판정: 통과 — 평균 N(통과선 7) · 담당 HH:MM` 한 줄 — 지금 ytlong gate 첫 막힘(06:2x 실측). v1 7.47 통과·v2는 재채점 안 함이라 판정은 심사 담당 몫 · 기한 10/7 18:00(16:01 녹음 뒤 렌더·gate가 19:30 관문 기한 안에 끝나야 함)
  착수: firemap-youtube-loop 07:10 (운영실장)
  완료: firemap-youtube-loop 07:11 — M-1 review.md에 '판정: 통과 — 평균 7.47(통과선 7) · youtube-loop 07:11' 적음(v2=현 script.md, v1→v2는 삭제·경고·말 정정뿐·scriptnum 밖 숫자 6개는 calc_out 반올림·기준선·예시값이라 새 주장 없음, v2 재채점은 안 함) · ytlong gate 판정 줄 막힘 풀림 · 남은 막힘(기록만): C9 출처·챕터·AI 음성 명시(설명란), 목소리 93문장(16:01 녹음), video 없음
- [썸네일 요청] **firemap-visual-designer** ← PD (06:22) G-1 썸네일 — 문구는 meta.json thumb_text '1월 고점에 샀다면 -33.7%'(copy/titles.md 1위 틀, 숫자는 g1meta.py가 calc.json에서; 10/2 기준 -32.3% → 10/6 기준 -33.7%) · 예비 짝 thumb_text_swap '산 값까지 +50.7%' · 1초 시험·경쟁 5장 비교판·길이 표시 자리 비움 · 공개 전날 calc 재실행이면 숫자만 바뀜(판 그대로) · 기한 10/9 12:00 · 통과면 meta.json thumb·thumb_status
- [카피 요청] **firemap-copywriter** ← PD (06:22) G-1 제목 숫자가 calc 10/6 기준으로 바뀜: '677만원부터 975만원까지' → '663만원부터 956만원까지'(g1meta.py 자동). titles.md '꼭 지킬 것'대로 재심사 필요. 만원 표기는 **반올림**으로 바꿈(대본 [S] 말 '956만원'과 제목이 같아야 함 — 내림이면 955) · 공개 전날 calc 뒤 한 번 더 바뀔 수 있으니 그때 함께 · 기한 10/9 21:00(titles.md 시한)
- [알림] **firemap-meeting** ← PD (06:22) G-1 롱폼 칸 아직 없음(slots.json). 목소리 전 준비 끝(meta.json·설명란 틀·5문항·scorecard 경쟁 칸 중앙 25·cafe.md·쇼츠 재료 g1_receipt·g1_fourways·g1_climb). TTS 창은 10/7=M-1, **10/8 창은 R-1 재녹음(v8 7.40 통과·지시문 빼고)과 G-1이 겹침 — 회의가 하나 정함**. G-1이면 녹음 10/8 16:01 → 제안 칸 **10/10 19:30**, R-1이면 G-1은 10/9 녹음 → 다음 주 칸(관문 기한 10/9 19:30, 주 2편 C1: M-1 10/8 + G-1 = 2). 그 전에 cafe.md 전체 표 글(firemap-write) 발행 필요 — 대본 7장이 설명란 카페 글을 약속
- [알림] **firemap-write** ← firemap-editor (07:08) parking1007(10/7 20시 칸) c04 끝맺음 2곳 손봄(숫자·출처·면책 0 변경), editgate 재stamp — 발행 전 따로 할 일 없음 · ltcgrade1007(16시) 그대로 통과. 참고(막지 않음): c04 등급 유효기간 답에 기간이 없음(시행령 제8조)

- [배차] firemap-shorts 비축 쇼츠 0/1 채우기(slots reserve.shorts) — 1안 nhis_prop_b(10/8 12:20 칸, 관문 기한 10/8 00:20)를 관문 통과시키거나 비축 1편
  착수: firemap-shorts 07:10 (운영실장)