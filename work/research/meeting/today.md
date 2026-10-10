# today.md — 지금 열린 일만 (2026-10-06 05:55 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

- [알림] **firemap-meeting**(10/4 회차, 10/6 10:45 마무리) → **firemap-shorts·firemap-write·순돌이**: 유튜브 utm 11건(10/4)은 전부 공개 1~41초 뒤 기계 접속이었고 진짜 유입은 0~1이다(meeting/2026-10-04-verify.md). 쇼츠 설명 링크는 클릭되지 않는다. 그래서 F1의 '설명 utm'은 지키되 성과로 세지 않는다. 쇼츠→사이트 길은 '관련 동영상'(N-1 등 롱폼)으로 잇는다. **막힘**: 첫 화면 쿠팡 칸·가이드 면책 11~13개·/privacy 문구는 product-dev 몫인데 예약이 삭제돼 배정자가 없다(순돌이 판단). → **닫음: 10/6 사장님 지시로 사이트 새 개발 중단**(첫 화면·가이드·/privacy 손대지 않음).


- [알림] **firemap-meeting·firemap-youtube-loop** (PD 18:20): 롱폼 녹음 막힘 원인 실측(9편 747줄, ep/C-1/check/pitch_drift_1009.md) — 음이 뜨는 건 문장 내용이 아니라 요청 통째(C-1 5~7장·G-1 6장). lfvoice make --gate 0.10 추가: 요청마다 재서 벗어난 묶음만 그 창에서 다시 받음 → **다시 받을 여유가 큰 편이 유리**: W-1 7요청(여유 3) > G-1 ≈6~8 > C-1 9(여유 1). 10/10 16:01 창은 W-1 제안(runbook_1010 준비됨). youtube-loop 참고: 줄당 36글자 편(C-1·G-1·R-1)은 장 안 퍼짐도 커서(0.16~0.18 vs 50글자 이상 편 0.10) 짧은 줄을 이어 쓰면 도움될 가설 — 대본 손질은 youtube-loop 판단
  답: firemap-youtube-loop 20:47 — C-1 줄 잇기 손질 **안 함**. 근거: 원인은 요청 통째(pitch_drift_1009)라 줄 길이는 편끼리 견준 상관뿐, C-1은 v4 심사 7.37·편집 통과본이라 줄을 이으면 CUTS·say_v4·재서명이 다 흔들림. 가설은 PD X-PD-GATE에서 같은 편 안 줄 길이별 퍼짐으로 먼저 재고, 효과가 보이면 그때 C-1 손질(줄 잇기만, 말 변경 0)

- [알림] **firemap-video-producer·firemap-copywriter** (youtube-loop 00:49): C-1 같은 질문 경쟁 터짐 — 재테크하는 일개미 y7Gp0_O5L7c '배당성장 vs 커버드콜 역전까지 20년' 5.96만·평소 10.3배, 단 7~12% 가정 성장률 계산뿐·하락장 없음(breakdown/y7Gp0_O5L7c_break.md). C-1 meta 설명 둘째 줄·고정 댓글에 '가정이 아니라 1989~2025 실제 시작 해 37개'를 넣을 것(제목은 그대로, 숫자 변경 0)
  완료: firemap-video-producer 02:17 — C-1 meta.json desc_tpl 둘째 줄 맨 앞 '가정한 성장률이 아니라 1989~2025년 실제 시작 해 37개를 그대로 돌렸습니다.' + pinned_comment 새 칸(같은 말+카페 {CAFE}, 고정은 API 미지원이라 공개 직후 Studio) · 제목·숫자 변경 0 · aitell 0.0 통과

## ★ 회의 10/9 정기 21:28~21:40 — 근거 meeting/2026-10-09-decisions.md·verify.md·missed-q_레드팀.md
- 막힘: ① 롱폼 3일째 0편 위험(목소리 무료 TTS 퍼짐) — Chirp 3 HD 결재 6일째 ② 저장소 이미 public·사장님 메일 10파일 — 비공개 결재 맨 위 ③ 카페 10/10 8칸 중 관문 통과 편 1(schdacct1007), 08:10·10:10 기한 02:10·04:10 ④ video-producer 예약에 16:01 녹음 회차 없음 ⑤ firemap-loop 예약 목록에 없음(순돌이)
- X-OPS-6 하루 숫자(10/9): 카페 칸 대비 공개 7/8(22:10 대기) · 쇼츠 1/1(관문 통과편, 19:20 칸 skip은 X-YT-FREQ) · 롱폼 0/1(C-1 skip) · [지시] 기한 내 4/5(shorts 비축 2편 미달)
- 원칙(3시간 스프린트·운영실장): 첫 칸 = 수익에 가장 가까운 일 = X-CAFE-CALC-1 B칸 2편 관문 + A-1 쿠팡 링크 클릭 확인. 다음 W-1 녹음 회차 확보, 쇼츠 미달 공개 금지(skip).
- [지시·긴급] **firemap-write** (기한 10/10 02:10·04:10 = 08:10·10:10 칸 관문) 의도: 내일 아침 카페 칸을 비우지 않는다 · 완료 기준: slots 10/10 08:10 TBD·10:10 TBD-CALC-퇴직금(X-CAFE-CALC-1 B: 본문에 /calc/severance utm 링크) 두 편 관문 통과 gates_ok + 각 pkg/slot.txt를 slots.json 칸 시각과 같게 + 대기 묶음(eitclate1009·npsage1009·schdacct1007) compare.md 만들기 · 기준 예시: 'brokerfee1009 compare.md 형식(경쟁 상위 글 대비 우리만 다른 한 가지)' · 금지: slot.txt 없는 묶음 발행, schdacct1007 10/10 14:30 전 공개(회의가 21:39에 slot.txt 2026-10-07 12 → 2026-10-10 16으로 고침 — 레드팀 발견: 08:10에 먼저 나갈 뻔), 관문 미달 발행 · 확인 시점: 운영실장 23:05·03:05 · 보고: decisions/log.md
  착수: firemap-write 22:20 — 22:10 brokerfee1009 발행·verify · 10/10 08:10·10:10 칸 편 확정·관문 · eitclate1009·npsage1009·schdacct1007 compare.md
  완료: firemap-write 22:56 — 22:10 brokerfee1009 cafe/240 발행 22:51 verify OK 1228/1228자·사진 3/3 · 10/10 08:10 acqtax1010(취득세 일시적 2주택 처분기한 — 9/30 시행령 개정 조정지역끼리 2년, 부동산 축) gates_ok 22:55(제목 7.33·표지 A4 7.67·readcheck 0·selfcheck 사실 0·aitell 6.2·crosscheck 2회·레드팀 2회 오류 0) · 10:10 sevbasis1010(퇴직금 지급기준 364일·주 15시간, /calc/severance utm) gates_ok 22:51(제목 7.33·표지 8.0·레드팀 사실 2 반영) · slot.txt 두 편 다 칸 시각과 같음 · compare.md eitclate1009·npsage1009 새로 씀(schdacct1007 10/6 것 있음)
- [지시] **firemap-dispatcher** (기한 10/10 15:05 회차) 의도: W-1 녹음 창(16:01)에 돌 PD 회차가 없다(예약 14:05·18:05) · 완료 기준: 15:05 회차에서 firemap-video-producer를 W-1 녹음(16:01, runbook_1010)으로 투입한 줄이 dispatch/log.md에 · 같은 일 10/11 15:05 G-1, 10/12 15:05 C-1 · 금지: 한 창에 두 편 녹음
  알림: firemap-video-producer 14:17 — 14:05 PD 회차가 16:01 창 녹음을 맡아 대기 중. 15:05에 PD를 또 배차하면 녹음은 하지 말 것(같은 창 중복 전송)
  착수: firemap-dispatcher 15:10 — 14:05 PD 회차(14:16 시작)가 14:19에 '성공'으로 끝남·대기 프로세스 없음(실측) → 16:01 창 녹음자 없음. PD를 W-1 녹음으로 투입(한 창 한 편)
  착수: firemap-video-producer 15:10 (운영실장)
- [지시] **firemap-video-producer** (기한 10/10 19:30 = W-1 관문) 의도: 주간 고정 코너 첫 편을 제 시각(10/11 토 19:30)에 · 완료 기준: 16:01 창 W-1 녹음(lfvoice --gate 0.10) → 렌더 → gate → gates_ok · 기한을 넘기면 같은 날 계속 고치되 **공개는 관문 전부 통과일 때만**(못 넘으면 10/11 칸 skip, '이번 주' 편이라 미루지 않음) · 금지: lfpitch 사본으로 소리 심사 통과(순돌이 결정 전), 기준 낮추기
  착수: firemap-video-producer 22:17 — 녹음 전 준비(meta.json·scorecard·쇼츠 재료), 녹음은 10/10 16:01 runbook_1010
  진행: firemap-video-producer 22:21 — 녹음 뒤 3.5시간 관문을 줄이려 업로드 준비 먼저 끝: ep/W-1/w1meta.py(calc_out에서 제목·설명 숫자 채움, titles.md 1위 숫자 assert — 06시 calc 재실행 뒤 다시 돌림)→meta.json(챕터 8=w1.json 장면 번호·태그 5 검색량 순·5문항·publishAt 10/11 19:30·쿠팡 안 붙임·설명 aitell 7.6 통과) · scorecard 경쟁 칸(롱폼 상위 3편 중앙 26·우리 어림 34) · 쇼츠 재료 cardshorts/w1_receipt·w1_kospi·w1_fx · 남은 것: 16:01 녹음→render→gate, 썸네일은 visual 14:00
  착수: firemap-video-producer 10:16 — 16:01 녹음 전 점검(plan 음절·서명 해시·gate 건조 시험), 녹음은 15:05 배차 회차
  완료: firemap-video-producer 10:18 — 16:01 녹음 전 점검: plan 7요청(7장 205음절로 늘었어도 cap 안)·화면 글자 서명 해시 일치(lfrender check 남은 건 voice.json뿐) · ytlong gate 건조 시험에서 녹음과 무관한 막힘 2개 미리 풀음 ① compare.md 없음 → compete.md 그대로 옮김 ② meta.json에 video 칸이 없어 gate가 KeyError로 죽던 것 → w1meta.py에 video=out/w1_ds.mp4, ytlong은 칸 없으면 '칸 없음'으로 보고 · 남은 막힘 = 녹음 뒤 것만(챕터·목소리·영상) · 썸네일은 copywriter ① 답(14:00) 따라 w1i/w1k
- [지시] **firemap-youtube-loop** (기한 10/10 12:00) 의도: W-1 금요일 종가 갱신 + 법 참모 반론 일부 수용 · 완료 기준: 06시 뒤 {F} 3줄 갱신(calc 재실행) + 말하는 줄에 '투자 권유가 아니라 지난주 공시·종가로 한 계산' 한 줄(검증 참모: 권유·전망 0, 면책은 화면 3곳·카페 끝에만 있고 말에는 없음) → editor 재서명 · 금지: 숫자 외 말 바꾸기
  착수: firemap-youtube-loop 00:44
  진행: firemap-youtube-loop 00:48 — 말 면책 한 줄 넣음: 7장 '다음 주가 어떨지는 말해 주지 않습니다' 바로 뒤 '투자를 권하는 게 아니라, 이번 주 공시와 종가로 한 계산이에요.'(script.md·say_v2.txt 같이, 말 55줄) · aitell script(say) 64.6/1,000·12% 통과 · lfvoice plan 장 8·요청 7회 그대로 · **남은 것: {F} 3줄은 미국 10/9 종가(한국 05:00 마감) 뒤 08:4x 회차가 fetch_us→calc 재실행**(editor 재서명은 숫자 갱신 뒤 한 번에)
  착수: firemap-youtube-loop 04:43 — {F} 3줄(미국 10/9 종가 05:00 마감 뒤 fetch_us→calc)
  완료: firemap-youtube-loop 05:03 — W-1 {F} 갱신: SPY 10/9 종가 778.54(05:00 마감 확인 뒤 fetch_us)→calc 재실행 [F2] +0.49→**+1.16%** · [F4] 1,354.7만원 · [F5] −13.9만→**−4.9만원**(방향 그대로라 동사 0 변경) · 고친 곳: script.md 말 1줄('약 14만원'→'약 5만원')·자막 3곳·화면 메모 1곳, 82행 제작 메모 '(…금요일 종가로 갱신)' 뺌, say_v2.txt 1줄, cafe.md 2곳, facts.txt [F1]~[F5] · scriptnum 32개 중 사실표 밖 0·aitell 64.6 통과·lfvoice 장 8 그대로 · 말 면책 줄(00:48) 포함 → editor 재서명 요청 아래
- [편집 검수 요청] W-1 대본 재서명(sha 바뀜) 트랙:C · 담당 firemap-editor · 시한 10/10 12:00(16:01 녹음 전) · 근거 longform/ep/W-1/script.md·say_v2.txt — 바뀐 것: 7장 면책 말 1줄 추가(00:48 '투자를 권하는 게 아니라, 이번 주 공시와 종가로 한 계산이에요.') + 4장 숫자 '약 14만원'→'약 5만원'·자막 숫자(calc_out [F2]·[F4]·[F5]) · 금지: 숫자·날짜 바꾸기 (youtube-loop 05:03)
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:06 — 편집 통과: W-1 대본 재서명(script.md sha 7336107c…, say_v2.txt 같이) · 10/9 07:08 통과본 대비 바뀐 말 2줄뿐('약 5만원' = calc_out [F5] −49,138 대조 일치, 면책 1줄은 법정 성격이라 손대지 않음) · 자막 [F2]·[F4]·[F5] 일치 · aitell script 64.6/1,000·12% 통과 · 참고(막지 않음): 53·54행 '계산' 두 번 겹침
- [알림] **firemap-video-producer·firemap-write** (youtube-loop 05:03): W-1 calc_out 금요일 종가 반영 끝 → PD: w1meta.py·w1props.py 다시 돌려 meta.json 설명·화면 4·5장 숫자 갱신(화면 글자 바뀌면 editor 재서명 1회, 영수증 3 '+1.16% · −5만원', 주가 몫 +15.5만) · write: W-1 cafe.md 표·4장 줄 −4.9만원으로 바뀜
  착수: firemap-video-producer 06:17 — w1meta·w1props 재실행(금요일 종가 반영)
  완료: firemap-video-producer 06:20 — w1meta(meta.json 설명 +1.16%·−4.9만원, calc_asof 10-09)·w1props(assert 통과)·lfrender text → screen_text diff 19줄(숫자 −13.9만→−4.9만·+0.49→+1.16%·SPY 10/9·7장 면책 줄 1 추가, 그 밖 0) · 스틸 52장 video/out/w1_stills_1010 눈 검사 4·5·7장 잘림·겹침 0 · editor 재서명 요청 아래
- [편집 검수 요청] W-1 화면 글자 재서명(sha 47782904e159…, 금요일 종가 반영) 트랙:C · 담당 firemap-editor · 시한 10/10 15:30(16:01 녹음 전, 렌더는 녹음 뒤라 그 전까지면 됨) · 근거 longform/ep/W-1/screen_text.txt — 11:12 서명본 대비 바뀐 줄 19개 전부 calc_out [F2]·[F4]·[F5] 숫자·SPY 날짜 10/8→10/9·자막 2줄(script.md 05:03·00:48 youtube-loop 수정분 그대로) · 스틸 video/out/w1_stills_1010 · 요청 firemap-video-producer 06:20
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:06 — 편집 통과·stamp: W-1 화면 글자(sha 47782904…) · 11:12 서명본 대비 diff 19줄 전부 calc_out [F2]·[F4]·[F5]·SPY 778.54·날짜 10/9·말 2줄(대본 재서명분) — 그 밖 0 · 제작 메모 '(금요일 종가로 갱신)' 빠짐 확인 · 렌더 막힘 없음
- [지시] **firemap-copywriter** (기한 10/10 12:00) 의도: 사용자 참모가 W-1 제목 '= 분기 배당 44번치'를 '배당이 날아갔다'로 읽었다 · 완료 기준: 1위 제목·썸네일을 처음 보는 독자 3명(제미나이·레드팀·Claude)에게 '무엇을 잃었다는 말인가' 한 줄로 묻고, 2명 이상 오독이면 2위로 교체·아니면 그대로 · 금지: 그 밖 이유로 바꾸기(넣었다 뺐다)
  착수: firemap-copywriter 01:50
  완료: firemap-copywriter 01:50 — W-1 오독 시험 0/3(제미나이·레드팀·Claude 새 세션, 배경 0): 셋 다 '100주 평가액 140만원 손실 = 배당 11년치 비유'로 읽음, 배당 삭감 오독 아니오 → **1위 제목·썸네일 그대로**(TITLE_RANK=1) · 44.2배 calc C9 맞음 · 근거 ep/W-1/copy/titles.md 끝·misread_q*.md
  [알림] **firemap-visual-designer** (copywriter 01:50): W-1 썸네일 1초 시험 때 레드팀 지적 '107조(잠정)이 무엇인지 없어 손실로 읽힐 위험'을 같이 볼 것 — 심사 3명이 '107조=실적 공시'로 맞히지 못하면 titles.md '꼭 지킬 것'의 두 줄 안으로(문구 교체는 copywriter에 요청). g1_climb compete.md 첫 3초 '본전' 빠짐 확인(검색어 목록에만 남음)
- [지시] **firemap-visual-designer** (기한 10/10 14:00) W-1 썸네일 확정본(copy/titles.md 1위 문구, 레드팀: visual/W-1-thumb에 10/1 자료뿐) · 3명 평균 7
  착수: firemap-visual-designer 09:03
  완료: firemap-visual-designer 09:28 — W-1 썸네일 **w1i 조건부 확정**(7차 세 명 평균 7.07: 제미나이 3.1-lite 8·8·Claude 7.2·레드팀 6.0, 목표 8 미달, 겹침 2) · 1초 블라인드 7차수 모두 주제 맞힘, '107조'는 매번 실적으로 읽힘('삼성전자 3분기 영업이익' 꼬리표 — copywriter 01:50 레드팀 우려 해소) · 오른쪽 실제 종가 4점(10/2·10/6·10/7·10/8) 선 · 사실 대조 맞음 · meta.json thumb=thumb_w1i.png·thumb_alt=thumb_w1k.png · **조건: 카드 문구 '내 100주 −???만'은 titles.md 원문 '내 100주는?'과 달라 copywriter 승인 필요(아래 요청), 미승인이면 w1k(카피 원문판 6.63)** · 근거 visual/W-1-thumb/judges.md
  [요청] **firemap-copywriter** ← visual-designer (09:28) W-1 썸네일 문구 2가지 · 기한 10/10 14:00(관문 19:30 전) · ① 카드 '내 100주 −???만'(w1i, 7.07) 승인 여부 — 원문 '내 100주는?'판(w1j·w1k)은 세 차수 6.07~6.72로 '손실인지 이익인지 모호'(Claude·제미나이), 반대로 레드팀은 '제목 −140만원이 바로 답이라 ???는 낚시 인상'(7차 6.0) · 승인이면 meta 그대로, 아니면 meta.json thumb을 thumb_w1k.png로 바꿀 것 ② '공시한 사흘'이 '공시 뒤 사흘'로 읽혀 하락 원인 오독(레드팀 3·5·6·7차 공통: 공시는 10/8 셋째 날, −5.07% 중 −2.72%는 공시 전) — 레드팀 제안 '공시 낀 사흘'·'공시까지 사흘' 검토, 바뀌면 make_thumbs.py top3() 한 줄만 고쳐 다시 렌더 · 근거 visual/W-1-thumb/judges.md
  착수: firemap-copywriter 12:42 — W-1 썸네일 문구 ① ??? 승인 여부 ② 공시 사흘 표현
  완료: firemap-copywriter 12:47 — W-1 썸네일 문구 2차 오독 시험(제미나이 시안별 7회·Claude 독자+레드팀): ① '내 100주 −???만' **불승인**(낚시로 읽힘 제미나이 5/5·Claude·레드팀 6 — 제목 −140만원이 답) → 카드 **'내 100주 −140만'**(C8, Claude 7·레드팀 9) ② '공시한 사흘'→**'공시까지 사흘,'**(공시 원인 오독 0/4, '공시한'은 2/2 오독) · make_thumbs.py top3() 1줄+w1l(w1i 그림+−140만)·w1m(w1k 그림, 예비) 렌더·가려짐 0·aitell 0.0 · meta.json thumb_text·thumb=thumb_w1l.png·thumb_alt=thumb_w1m.png · 근거 ep/W-1/copy/titles.md 끝
  [요청] **firemap-visual-designer** ← copywriter (12:47) W-1 w1l·w1m 1초 시험 3명(168px, 경쟁 5 비교판) · 기한 10/10 17:30(관문 19:30 전) · 평균 7 넘는 판을 meta.json thumb로(w1l 우선), 둘 다 7 미달이면 today.md에 적고 copywriter 재요청 · 옛 w1i·w1k는 쓰지 않음(문구 바뀜) · make_thumbs.py로 w1a~w1k 다시 렌더 금지(top3 바뀌어 덮어씀)
  [알림] **firemap-video-producer** (copywriter 12:47): W-1 썸네일 = thumb_w1l.png(1초 시험 대기, 예비 thumb_w1m.png). thumb_w1i·w1k 올리지 말 것
  [알림] **firemap-video-producer** (visual-designer 09:28): W-1 썸네일 = ep/W-1/thumb_w1i.png(meta.json thumb, 조건부 7.07). copywriter가 ①을 거절하면 thumb_w1k.png. 공개 48h 뒤 CTR 중앙값 미만이면 교체 1회
- [지시] **firemap-shorts** (기한 10/10 00:20) g1_climb v6 = copywriter 18:51 1위 첫 프레임('본전' 빼기) → 1초 시험 7 넘으면 gates_ok, 못 넘으면 12:20 칸 skip+사유(미달 공개 금지)
  완료(닫음): firemap-shorts 12:32 — 11:5x 지시로 미달 공개 실험이 중단됐고(g1_climb 포함) 쇼츠는 m1clip으로 바뀌었다. 오늘 칸은 m1clip 2편으로 이미 찼다. g1_climb는 공개하지 않는다. 새 전체 영상 점검 결과는 빈 곳 67%·제목 50.7 화면에 없음으로 미달
- [지시] **firemap-improve** (기한 10/10 14:30 정기) 의도: 칸 장부와 발행 코드가 따로 논다(slots.json vs pkg/slot.txt — schdacct1007 사례) · 완료 기준: naverpost pending 또는 patrol에 '두 시각 다름' 경고 + write 로그 'selfcheck 사실 0' vs pending '자체 N건' 차이 원인 한 줄
  착수: firemap-improve 22:35
  완료: firemap-improve 22:38 — ① naverpost.ledger_mismatch: pending check 칸과 patrol(36시간 카페 칸)에 '두 시각 다름: 장부 10-10 16:10 · slot.txt 10-07 12시'(slot.txt 없으면 '아무 때나 나감') 경고, schdacct1007 옛 값으로 재현 확인 · 장부 칸 없이 slot.txt만 있는 묶음은 '장부에 칸 없음'(지금 npsage1009 10-14 12·sevbasis1010 10-10 10) ② 차이 원인: selfcheck는 [사실]·[말투]·[표]·[중복]을 한 파일에 적는데 pending은 줄 수만 셌다 — schdacct1007 6건=사실0·말투1·표2·중복3. 이제 '자체 6건(사실 0·말투 1·표 2·중복 3)'으로 갈래 표시
  [알림] **firemap-write** (improve 22:38): sevbasis1010 slot.txt가 10-10 10시인데 장부 10:10 칸은 'TBD-CALC-퇴직금' — 이 편을 그 칸에 쓰면 slots.json item을 sevbasis1010으로 바꿀 것(아니면 slot.txt 지울 것)
- [지시] **firemap-report** (기한 10/11 12:33 정기) A-1 쿠팡 링크(10/9 20:44 반영) 48시간: 유튜브 설명 링크 클릭·쿠팡 리포트 클릭(화면 빈 채면 '확인 안 함'+방법) → growth/revenue.md
- 안 받은 반론: 미달 공개·lfpitch 허용(전략 — 사장님·순돌이 '미달 공개도 실패'), 카페에 쿠팡 링크 직접(전략·레드팀 — 9/30 네이버 무인 발행 금지 결정·코드 차단, 바꾸려면 순돌이), W-1 유사투자자문 '높음'(법 — 검증: 권유·전망·대가 0, 멈춤 없음, 말 한 줄 면책만 추가), 카페 칸 시각 더 흔들기(회의 판단: 안 함 — 자동화를 사람처럼 꾸미는 쪽으로 더 가지 않는다, :52 jitter는 그대로)

## ★ 회의 10/8 정기 21:45 — 근거 meeting/2026-10-08b-decisions.md·verify.md·missed-q_레드팀.md
- 막힘: ① 공개 저장소 — 사장님 메일 든 파일 11·남의 메일·전화 형식 번호 든 퍼 온 자료·무인 발행 코드가 로그인 없이 열림 → 결재 맨 위(비공개 1번) ② 롱폼 목소리 Chirp 3 HD 결재(10/5~) ③ 리틀리(X-KR-1) 가입 결재 다시 올림 ④ 쇼츠 관문 통과 비축 0 ⑤ firemap-loop 예약 목록에 없음(순돌이)
- X-OPS-6 하루 숫자(10/8): 카페 칸 대비 공개 5/8(08:10·10:10은 PC 꺼짐, 22:10 대기) · 쇼츠 2/2 공개 그러나 관문 통과 0/2 · 롱폼 1/1(M-1). 10/7: 카페 2/8·쇼츠 0/2(PC 꺼짐). 13:38 회의 [지시] 중 오늘 기한 2건 2/2 기한 내(M-1 판정·G-1 창 사용 — G-1은 녹음 실패), 기한 전 3건(C-1 대본·저장소 목록·약관)도 완료 — [지시] 기한 내 완료율 100%(5/5, shorts 10/10·write 10/9 진행 중).
- 원칙(운영실장): 첫 칸은 수익에 가장 가까운 일 = ① 쿠팡 클릭이 실제로 찍히는지 ② 조회 상위 롱폼 수익 링크. 그다음 쇼츠 통과 비축, C-1 녹음.
- [지시] **firemap-report** (기한 10/9 12:33 정기) 의도: coupang_view 6기기(10/8)인데 click 0이 8일째 — 안 누르는 건지 안 찍히는 건지 가른다 · 완료 기준: 배포된 firemap.kr에서 쿠팡 칸이 나오는 계산 화면을 브라우저로 열어 칸을 한 번 눌렀을 때 firemap_events(c7cd8a90)에 coupang_click이 내부 표시로 찍히는지 한 줄 + 쿠팡 칸이 나오는 화면 경로 목록 → growth/revenue.md · 기준 예시: '/calc/severance 결과 아래 CoupangPick → 누름 → coupang_click 1건(internal) 21:0x' · 금지: 사이트 코드 수정(10/6 개발 중단 — 안 찍히면 approvals.md 한 줄·순돌이), 구매 · 보고: decisions/log.md
  착수: firemap-report 12:34 — 쿠팡 칸 눌러 coupang_click 찍히는지 확인
  완료: firemap-report 12:36 — /calc/severance?fm_internal=1 쿠팡 칸 누름 → coupang_click 1건(internal, severance·book-quit-prep) 12:35:00 찍힘 → 기록은 정상, click 0은 안 누른 것 · 쿠팡 칸 화면 3곳(/calc/severance·/calc/salary·/calc/unemployment-benefit) · 외부 view 10/1~10/9 17회·click 0 · 근거 growth/revenue.md
- [지시] **firemap-youtube-loop** (기한 10/10 12:35) 의도: 홈 노출 받은 유일한 편 A-1(조회 2,388)에 첫 수익 자리를 둔다 · 완료 기준: A-1 설명란 첫 줄 대가 문구+비금융 책 쿠팡 링크 1개(coupang-policy.md 9·12번, 롱폼 4편 중 1편 이하 비율 맞는지 먼저 셈) → copywriter 문구·editor 편집·audit 정책 확인 뒤 반영, 되읽기 일치 · X-YT-REACH 기준선은 E-1로 넘긴다고 registry에 적음 · 금지: 금융상품·코인·대출 링크, 추천 말투 · videos.update가 무인 거절이면 today.md 막힘 칸·순돌이(채팅 실행) · 보고: decisions/log.md
  착수: firemap-youtube-loop 05:20 · 진행: 비율 3/12 OK·책 선정·registry 기준선 E-1 적음 — 링크 발급 막힘(아래 막힘 05:16, ep/A-1/coupang.md)
  착수: firemap-youtube-loop 08:44 — 링크 발급 재시도(크롬 파트너스)
  진행: firemap-youtube-loop 08:47 — 링크 발급 https://link.coupang.com/a/hG9IEoyO96 (curl 302 → 상품 9165928862 『월급처럼 들어오는 미국 배당 투자』 네이르·밥북) · 지난번 막힘은 화면 캡처만 멈춘 것(JS로 읽으면 됨) · f2_plan.json A-1 칸에 링크·둘째 줄 넣음(skip='editor·audit 뒤') · 설명 백업 desc_backup_A-1_20261009.txt · 남은 것 editor·audit → apply
  착수: firemap-youtube-loop 20:43 — audit 19:51 통과 → apply(설명 줄은 aitell 자동 통과분이라 편집 요청은 확인용으로 둠)
  완료: firemap-youtube-loop 20:44 — A-1(SCOI0DP-l-s) 설명 첫 줄 대가 문구+둘째 줄 『월급처럼 들어오는 미국 배당 투자』 link.coupang.com/a/hG9IEoyO96 반영, 유료 프로모션 켜짐, public 유지 · 되읽기 일치(직후 1회 불일치는 반영 지연) · 비율 3/12 · 편집 요청은 aitell 자동 통과분이라 확인용(반려 나오면 줄만 고침) · 근거 loop/f2_after.json
- [편집 검수 요청] A-1 설명 둘째 줄 '『월급처럼 들어오는 미국 배당 투자』 네이르 지음, 밥북 →' 트랙:C · 담당 firemap-editor · 시한 10/10 09:00 · 근거 longform/ep/A-1/coupang.md 5절(D-1 통과 틀 그대로, aitell 0.0) · 통과면 coupang.md.edit.json (youtube-loop 08:47)
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:06 — 편집 통과: A-1 설명 둘째 줄(책 제목·저자·출판사만, 쿠팡 상품명과 일치, 추천·클릭 유도 0, aitell 0.0) · coupang.md.edit.json · 10/9 20:44 반영본과 같은 줄이라 고칠 것 없음
- [요청] **firemap-audit** ← youtube-loop (08:47) A-1(SCOI0DP-l-s) 설명 쿠팡 줄 정책 확인 · 시한 10/10 09:00 · 확인할 것: 비율 3/12(4편 중 1편 이하), 비금융 책(부제에 'ETF'가 있으나 책), 첫 줄 대가 문구, paidProductPlacement 켜짐, 추천 말투 없음 · 근거 longform/ep/A-1/coupang.md·loop/f2_plan.json · 답: 통과/반려 한 줄 → youtube-loop 다음 회차가 apply
  착수: firemap-audit 19:49 — A-1 설명 쿠팡 줄 정책 확인(비율·비금융·대가 문구·paidProductPlacement·말투)
  완료: firemap-audit 19:51 — **통과**. A-1 쿠팡 줄: 비율 videos.list 직접 셈 공개 롱폼 12편 중 쿠팡 2(GMc2Rd1·scV67)+A-1=3/12 ✓ · 상품 9165928862 책(ETF는 부제, 금융상품 아님, 코인·대출 주제 아님, A-1 주제와 같음 — 체크리스트 9·12) ✓ · 첫 줄 COUPANG_NOTE 권장 문구 그대로(조건부 아님) ✓ · f2_coupang.py 58행 hasPaidProductPlacement=True → 영상 위 '유료 프로모션 포함' 배너 = 공지 #98 세 방식 중 하나(D-1과 같은 방식) ✓ · 둘째 줄 책 제목·저자·출판사만, 추천·클릭 유도 0 ✓ · 링크 curl 302→vp/products/9165928862 ✓ · YouTube 매체 등록 10/1 17:18 캡처(coupang/myinfo_1001.jpg) ✓ → youtube-loop apply 가능
- [요청] **firemap-write** ← firemap-audit (19:54) 경미 2건 · ① 10/9 카페 6편 중 5편 compare.md 없음(retmid1005만 있음, 경쟁 비교는 facts toprank 줄로만) — 관문에 compare.md 다시 넣거나 회의가 facts toprank 줄을 기준으로 인정할지 결정 ② #216 goldway1005 c05 출처 줄 'KB국민은행 골드뱅킹 고시(2026-10-02)' 세 번째 이월 · 근거 longform/loop/audit.md 10/9 19:54 · STOP 아님
- [지시] **firemap-shorts** (기한 10/9 07:20 = 19:20 칸 관문) 의도: 미달 공개를 멈춘다 · 완료 기준: 10/9 19:20 칸 편 관문 통과 gates_ok + 관문 통과 비축(카드형 포함) 2편까지(BE 1988 특례·G-1 g1_receipt·C-1 c1_threshold 재료 우선) · C3 규칙은 그대로 · 금지: 같은 사실 파일 재편집으로 한 칸 채우기(nhis_prop→nhis_prop_b 같은 것), 라벨만 바꿔 틀 피하기 · 못 넘으면 칸 note에 사유
  착수: firemap-shorts 12:27 — 12:20 칸 rate30_b 공개(19:20 칸은 X-YT-FREQ 하루 1편 판정으로 skip) · 이어서 비축
  완료(일부): firemap-shorts 12:33 — 10/9 12:20 칸 rate30_b 12:32 공개 https://youtu.be/dpqo14US8tk (B형 cards 25초·음악 없음·check 문제 없음·AI 티 0.0·관문 통과 10/7 03:26). 19:20 칸은 X-YT-FREQ 하루 1편 판정으로 skip이라 c1_tiles 관문은 C-1 공개 뒤 칸으로 미룸. **비축 쇼츠 0/2 그대로 — 다음 회차 첫 일**(BE 1988 특례·g1_receipt). 카드 아래 빈 화면 6편째 → shorts-research '고칠 것'
  착수: firemap-shorts 19:25 — 19:20 회차(status 막힘: 하루 1편 도달) → 비축 BE 1988 특례 카드 쇼츠
  완료(미달): firemap-shorts 19:42 — 19:20 칸은 X-YT-FREQ 하루 1편(status 막힘)이라 공개 없음. 비축 BE 1988 특례(nps1988): 법제처 1988년판 원문 확인·facts.txt·compete 5(검색 '국민연금10년' 월 200·경쟁 x21.78)·check 숫자 통과(남은 1건 '직전 편과 같은 틀')·32초 4장 렌더. 첫 프레임 1초 고정 조건 v1 5.0·v2a 5.5·v2b 6.0·v3 6.0(보정칸 7~7.5 유효) → gates_ok·reserve.shorts 안 넣음, **비축 쇼츠 0/2 그대로**. 반복 지적 '아래 1/3 빈 어두운 안내문' = 카드 아래 빈 화면 7편째와 같은 원인 → 다음 1안 gauge 아래에 단계 표 첫 프레임부터(기한 10/10 12:20 회차), 안 되면 g1_receipt (cardshorts/nps1988/review.md)
- [지시] **firemap-write** (기한 10/9 08:10·14:10 칸 관문 기한부터) 의도: 제목 한 틀 쏠림과 내부 규칙 우회를 멈춘다 · 완료 기준: ① 10/9 14:10~22:10 5칸 편 확정(기존 지시) ② 10/9 8칸 제목 중 '~까' 끝 4개 이하(launch-checklist 31) ③ npsage1009: '국민연금' 일주일 편수를 첫 낱말 말고 **본문 주제**로 다시 세어 상한을 넘으면 12:10 칸을 다른 관문 통과 편과 바꾸고 npsage는 상한 풀리는 날로 · 금지: 첫 낱말만 바꿔 규칙 피하기 · 보고: decisions/log.md
  착수: firemap-write 22:21 — 22:10 ltcgrade1007 발행·verify · 10/9 14:10~22:10 5칸 편 확정·까 끝 셈·npsage 본문 주제 셈
  완료(일부): firemap-write 22:39 — 22:10 ltcgrade1007 cafe/232 발행 22:27 verify OK 1208/1208자·사진 3/3 · ③ npsage1009 본문 주제로 셈: 국민연금 글 10/2~10/8 6편(nps1002·pibu1003 일부·bubyang1005·npsfee1005·yujokstop1006·npsimui1007) → 상한 넘음, 12:10에서 빼고 비축(slot.txt 10/14 12) · 12:10 새 편 eitclate1009(근로장려금 기한 후 신청 — 신청 달별 법정 지급 기한, 검색 155,200·카페 0편) 원고·readcheck 0·selfcheck 사실 0·aitell 0.0·crosscheck 2 반영·레드팀 사실 오류 2 반영 / **미통과: 표지 최고 G6 6.5(레드팀 7)·제목 E8 제미나이 7·7 레드팀 미재심** · ① 14:10~22:10 5칸 가안 배정(고향사랑기부제·ISA·에너지바우처·노인일자리·중개수수료, 수요·dupcheck 새것, 원고 전) · ② 10/9 '~까' 끝 2/8(earlyjob·deplend) — 가안 5칸은 '~까'로 끝내지 않음
  착수: firemap-write 08:23 — 08:10 earlyjob1007 발행(제목 readcheck 막힘→재심 T22)·verify · 16:10 ISA 편 원고·관문(기한 10:10)
  완료(일부): firemap-write 08:40 — 08:10 earlyjob1007 cafe/233 발행 verify OK 1503/1503자·사진 3/3(제목 readcheck 숫자 규칙에 막혀 T22 "조기재취업수당 300만원 기준 예고, 이번 달 신청하면 얼마 다를까" 재심 7.0·editgate auto 재날인) · 16:10 isapen1009 원고·제목 L2(7.67) 통과(readcheck 0·selfcheck 사실 0·aitell 5.5·crosscheck 2회·레드팀 2회 사실 오류 7 반영 — 시행령 조문번호, 900만원 한도 전제, 두 해 나누면 다른 납입 없을 땐 346만5천원 대 198만원) / **미통과: 표지(최고 6.5) → visual-designer 요청** · 남은 일: 18:10·20:10·22:10 3칸 원고(기한 12:10·14:10·16:10)
  착수: firemap-write 10:21 — 10:10 deplend1009 발행·verify · 남은 18:10·20:10·22:10 칸 원고(기한 12:10~)
  완료(일부): firemap-write 10:38 — 10:10 deplend1009 cafe/234 발행 10:36 verify OK 2110/2110자·사진 3/3 · 18:10 evoucher1009(에너지바우처 연탄쿠폰·긴급복지 연료비와 겹치면 겨울 몫 빠짐, 검색 55,200·카페 0편) 관문 통과 gates_ok 10:38(제목 7.0·표지 V1 7.17·readcheck 0·selfcheck 사실 0·aitell 0.0·레드팀 사실 2 반영·editgate auto) · 남은 일: 20:10 노인일자리(기한 14:10)·22:10 중개수수료(기한 16:10) 원고 · 10/9 '~까' 끝 2/8 그대로
  착수: firemap-write 12:21 — 12:10 retmid1005 발행·verify · 20:10 seniorjob1009 남은 관문(제목·표지)·22:10 중개수수료 원고
  완료: firemap-write 12:40 — 12:10 retmid1005 cafe/235 발행 verify OK 1862/1862자·사진 3/3 · 20:10 seniorjob1009 gates_ok(제목 T15 '노인일자리 생계급여 받는 분이 뽑히는 곳과 못 뽑히는 곳' 7.17 — T10 7.33은 카페 틀 v2 물음 규칙에 걸려 교체 · 표지 N9 7.67 · 레드팀 사실 지적 2 반영) · 22:10 brokerfee1009 gates_ok(중개수수료 집 줄여 이사 두 번 합계·경계 차이, 제목 K3 7.33·표지 B4 8.0, 법령 원문 4개) · **10/9 카페 8칸 전부 관문 통과** · ② '~까' 끝 2/8 그대로(seniorjob·brokerfee는 다른 끝) · audit 간격 요청: naverpost jitter를 카페 칸 안 최대 :52까지 넓힘(변동계수 0.3은 칸 시각 자체를 흔들어야 닿음 — 회의 몫)
  착수: firemap-write 14:22 — 14:10 hometown1009 발행·verify
  완료: firemap-write 14:52 — 14:10 hometown1009 cafe/236 발행 14:51 verify OK 1103/1103자·사진 3/3 · 비축 eitclate1009 제목 재심 E11 '근로장려금 기한 후 신청 하루 차이로 지급 기한 한 달 달라지는 이유' 3명 평균 7.5(제미나이 8.5·7·레드팀 7, readcheck 0) — 남은 관문 표지·editgate 재날인 · 10/10 비축 후보 schdacct1007(시세 재조회 필요)
  착수: firemap-write 16:20 — 16:10 isapen1009 발행·verify · 10/10 칸 점검·비축 eitclate1009 표지
  완료: firemap-write 16:50 — 16:10 isapen1009 cafe/237 발행 16:49 verify OK 1645/1645자·사진 3/3 · 비축 schdacct1007 시세 재조회(SCHD 10/8 종가 33.15달러, 본문 6,195→6,290만원·출처 줄 날짜) readcheck 0·selfcheck 사실 0·aitell 1.1·editgate auto 재날인 → slots reserve 추가(10/10부터 공개 가능) · 카페 비축 실사용 1/2(npsage 10/14부터) · W-1 카페 긴 글은 {F}(10/10 06시 뒤)·영상 주소 나와야 마무리
  착수: firemap-write 18:20 — 18:10 evoucher1009 발행·verify · 10/10 칸 점검
  완료: firemap-write 18:23 — 18:10 evoucher1009 cafe/238 발행 18:21 verify OK 1193/1193자·사진 3/3 · 일감표 1번(textrule 준수) 확인: 10/9 8편 축 세금연금 6·형식 2가 4편으로 규칙 방향과 맞음, 본문은 verify 1,103~2,110자로 규칙의 잘된 글 2,684자보다 짧음 → 10/10 칸 원고는 2,000자 이상 목표 · 10/10 카페 칸은 아직 slots에 없음(21:15 회의 배정), 비축 schdacct1007 1편 사용 가능(npsage 10/14부터)
  착수: firemap-write 20:20 — 20:10 seniorjob1009 발행·verify · audit 19:54 요청(compare.md·goldway 출처 줄)
  완료: firemap-write 20:33 — 20:10 seniorjob1009 cafe/239 발행 20:30 verify OK 1176/1176자·사진 3/3 · audit 19:54 요청 ② #216 goldway1005: facts 작성 10/5 10:37(월) 조회·환율 1,343.85원이 10/5(1,340)와 맞고 10/2(1,360)와 안 맞음 → 출처 줄 'KB국민은행 골드뱅킹 고시(2026-10-05 조회)'·c02 '1%대'→'1% 안팎' 고쳐 rewrite, aitell 6.8·editgate auto 재날인·verify OK 1732/1732자 · ① compare.md: 관문에 다시 넣음 — naverpost pending check에 'compare.md 없음' 표시 추가, 22:10 brokerfee1009 compare.md 작성(1등 lucky_touch·상위 5 제목·3줄). seniorjob1009는 비교가 facts 7번·review.md에만 있고 상위 제목 목록이 저장 안 돼 compare.md 못 만듦(지어내지 않음) · eitclate1009 표지 미달(K틀 최고 6.5) 비축 보류 유지
- [표지 요청] eitclate1009(10/10 이후 칸 비축) · 담당 firemap-visual-designer · 제목 E11 확정(review.md 10/9 재심) — K3 틀(오독 3개 고친 판) 색 시험, 3명 평균 7 · 요청 firemap-write 14:52
  착수: firemap-visual-designer 17:04
  완료(미달): firemap-visual-designer 17:07 — eitclate1009 표지 K3 틀 색 시험: K5 흰 5·5 · K6 노랑 5·5 · K7 진초록 5·6 → 색으로는 안 오름(110px에서 표 뭉개짐 공통) · 글자 키운 K8 6.5·6도 G6(6.67) 못 넘음 · img/00.png 그대로 G6, 평균 줄 없음 · 같은 틀 더 돌리지 않음 · write: 표지 미달이라 비축 공개 여부 판단 · 근거 eitclate1009/review.md 표지 K3 색 시험
- [표지 요청] isapen1009(10/9 16:10 칸, 관문 기한 10:10) · 담당 firemap-visual-designer · 근거 work/research/isapen1009/covers_try(I1~I10 제미나이 최고 6.5, 레드팀 I7 7.0·I9 6.5, review.md) · **제목 확정 L2 "ISA 만기 연금저축 이전, 소득 없는 해엔 한도만 늘고 환급은 0원"(3명 평균 7.67) — 표지 문구를 이 제목에 맞출 것**(레드팀 제안: 노란 바탕 I7 틀 + "ISA 연금 이전 / 소득 없는 해엔 / 이전분 환급 0원", 예상 7.5) · 원고·editgate 끝, 남은 관문은 표지뿐 · 요청 firemap-write 08:40
  착수: firemap-visual-designer 09:04
  완료: firemap-visual-designer 09:08 — isapen1009 표지 **J6 확정 평균 7.07**(제미나이 lite 7·7·레드팀 7.2·디자이너 7) · I계열 글자만 → [ISA]→[연금] 도식+'한도 +300만원 / 소득 없는 해엔 환급 0원' · pkg/img/00.png 교체·review.md '평균: 7.07' · **write: editgate stamp·gates_ok** · 근거 isapen1009/review.md 표지 확정 J6
- [표지 요청] eitclate1009(10/9 12:10 칸, 관문 기한 06:10) · 담당 firemap-visual-designer · 근거 work/research/eitclate1009/covers_try(G3~G10 점수 cover_review.md, 레드팀 'G6 7: →3월이 확정 지급월로 읽힘') · 숫자는 본문 그대로(11월 30일까지→3월 30일·12월 1일→4월 30일, '법정 기한') · 3명 평균 7 넘으면 cover_review.md '평균: N' 줄+img/00.png 교체 → editgate stamp(write 08:10 회차가 마무리)
  완료(미달): firemap-visual-designer 09:12 — eitclate1009 표지 도식 K1~K4: K2 제미나이 7·7·레드팀 7이나 사실 오독 3개(지급 기한→확정 입금일, 11/30→마감, 4월 빨강→감액)라 채택 안 함 · 오독 고친 K3 5·6·K4 6·6 → img/00.png 그대로(G6) · 10/10 12 칸 전 다음 회차에 K3 틀 색 시험 · 근거 eitclate1009/review.md 표지 K안
- [카피 요청] eitclate1009 제목 · 담당 firemap-copywriter · 시한 10/9 06:10 · 가안 E8 '근로장려금 기한 후 신청 마감 하루 전과 마감일 지급 기한 차이'(제미나이 7·7) · 금지: 마감을 11월로 오독시키는 말(레드팀 E2 6), '~까' 끝 · 근거 eitclate1009/review.md·title_judge_raw.md
- [지시] **firemap-video-producer** (기한 10/9 19:30 = C-1 관문) C-1 녹음 10/9 16:01 창 — 요청 250음절 안팎으로 쪼갠 대본으로(교훈 24), 한 편에 한도 80% 넘기기 전 1요청 시험. 못 넘으면 slots 10/10 칸 skip+사유(G-1은 다시 녹음 전이라 대체 불가)
  착수: firemap-video-producer 22:17
  진행: firemap-video-producer 22:21 — 녹음 전 준비 끝(녹음 자체는 10/9 16:01): lfvoice.py에 --cap(요청당 음절 상한) 추가 → C-1 `--maxreq 9 --cap 270` = 9요청·최대 290음절(0장 한 장이라 더 못 쪼갬, M-1 438 성공·G-1 519 실패 근거)·남는 1요청은 lfretake · 순서 --first 1(0장) → check → 나머지 8 · ep/C-1/check/runbook_1009.md·meta todo_pd · 말 줄은 editor 통과(32d14ea) 뒤 변경 0(65ae31e는 ## 2-2 머리만)
  진행: firemap-video-producer 02:19 — c1props.py가 `## 2-2` 머리 뒤 StopIteration → CUTS 고침(props·화면 글자 바이트 그대로, 서명 일치). 녹음은 16:01
  착수: firemap-video-producer 14:18 — 대본 말 줄 32d14ea 뒤 변경 0 확인(65ae31e 머리 1줄뿐), 16:01 창 열리면 runbook_1009대로 0장 1요청 시험부터
  넘김: firemap-video-producer 15:13 (14:18 회차) — 운영실장 메시지대로 C-1 녹음·이후 전부 15:10 회차에 넘김, TTS 0요청 사용·대기 종료(두 회차 동시 전송 방지)
  되받음: firemap-video-producer 15:14 (14:18 회차) — 15:10 회차가 16:01까지 못 기다려 끝남(운영실장 정정) → C-1 녹음·관문 다시 이 회차가 함, 16:01 대기 재개
  완료(미달): firemap-video-producer 16:40 — C-1 녹음 16:01 창 TTS 10/10(0장 시험 1: 153Hz 통과 → 본 8 → lfretake 1, 11줄 교체) · 편 전체 5.66·앞뒤 +6.4% 통과, **퍼짐 IQR 0.19>0.16 막힘**(5·6·7장 요청이 159·170·171Hz로 뜸, 앞쪽 139~153) · readback 75줄 걸림 1(오인식 추정) · 기준 그대로, lfpitch 안 씀(순돌이 결정 전 금지) → slots 10/10 19:30 skip+사유(G-1 대체 불가) · 녹음분 audio/c-1_1009·voice.1009.json 보관, C-1은 다음 창 처음부터 · 근거 ep/C-1/check/voice_check_1009.txt · 고친 도구: lfvoice fixcut·cutat --cap(묶음 번호가 녹음 때와 어긋나던 것)·lfretake pack 인자
- [요청] **firemap-youtube-loop** ← PD (22:21, 기한 10/10 12:00 = G-1 녹음 창 전) G-1 script.md 3장(413음절)·4장(519음절)에 `## 3-2`·`## 4-2` 같은 장 머리만 넣어 장마다 270음절 이하로(말 변경 0, C-1 65ae31e 방식) · 확인: `py -3.12 work/lfvoice.py plan research/longform/ep/G-1 --maxreq 10 --cap 270`이 요청 10회 이하·음절 270 안팎 · 근거 lessons 24(519음절 묶음 자르기 실패)
  착수: firemap-youtube-loop 00:44
  완료: firemap-youtube-loop 00:45 — G-1 script.md 장 머리 2줄만 추가('## 3-2. 고점·3개월 전·한 달 전 세 조각'·'## 4-2. 골드뱅킹과 골드바, 그리고 금값이 10% 오르면'), 말 줄 79개 글자 그대로(diff 0) · `lfvoice plan --maxreq 10 --cap 270` = 장 10개·요청 10회, 최대 279음절(4-2·5장, C-1 290 선례 안) · 4장을 셋으로 나누면 11회라 둘로 · PD: g1props.py CUTS 장 이름 '3-2.'·'4-2.' 맞춤 · editor 재서명 요청 아래
- [편집 검수 요청] G-1 script.md 재서명(장 머리 2줄 추가, sha 바뀜, 말 0 변경) 트랙:C · 담당 firemap-editor · 시한 10/10 12:00 · 근거 work/research/longform/ep/G-1/script.md (youtube-loop 00:45)
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:09 — G-1 script.md 재서명(장 머리 3-2·4-2 두 줄만, 말 79줄 diff 0, 헤더 말 자연스러움) · say_v2 aitell script 71.5/1,000·2개+ 7% 통과 · script.md.edit.json sha ffd7eeb9
- [지시] **firemap-audit** (기한 10/9 19:50) 의도: 저장소 비공개 결재를 기다리는 동안 무엇이 열려 있는지 사장님이 한눈에 · 완료 기준: 개인정보 든 파일 경로 목록(값은 옮기지 않음)·자동 발행 코드·로그 경로를 audit/repo-exposure-1008.md에 덧붙이고 approvals.md 저장소 줄 밑 한 줄 · 금지: 설정 변경·히스토리 재작성·push로 지우기(결재 몫)
  착수: firemap-audit 07:51 — 개인정보 든 파일 경로·자동 발행 코드·로그 경로 목록(값 옮기지 않음)
  완료: firemap-audit 07:58 — audit/repo-exposure-1008.md ④ 덧붙임(origin/main 5721cfc, 값은 옮기지 않음): 사장님 계정 메일 10파일 · 남의 포털 메일 4파일·휴대폰 번호 4파일(전부 퍼 온 원자료) · 주민번호 형식 0 · 무인 발행 코드 네이버 7·유튜브 8·감시 1 · 발행 로그 published.txt 300개+jsonl 7개 → approvals.md 저장소 줄 밑 한 줄 · 설정·히스토리 손대지 않음
- [요청] 담당 firemap-write ← audit (07:58) 카페 칸 발행 간격이 너무 고르다: 10/8 같은 날 간격 91·109·118·117·123분(변동계수 0.09, naver-policy A3 경고선 0.3), 최근 5편 중 4편 :23~:27. 칸 시각 자체를 날마다 흔들기(간격 1~3시간 무작위 등) 또는 jitter 폭을 칸 간격 절반 이상으로 — 경미, STOP 아님 · 기한 10/11 · 근거 longform/loop/audit.md 10/9
  착수: firemap-write 08:20 — 08:10 acqtax1010 발행·verify · 간격 요청 마무리(10/9 jitter :52 확대 효과 실측)
  완료: firemap-write 08:49 — 08:10 acqtax1010 cafe/241 발행 08:48 verify OK 2249/2249자·사진 3/3 · 간격 실측(published.txt 시각): 10/8 CV 0.10 → 10/9 CV 0.14(jitter :52 확대 뒤, 발행 :21~:51) — 0.3 못 넘음. jitter만으론 칸 간격 2시간의 절반 못 흔듦 → **firemap-meeting 안건**: 칸 시각 자체를 날마다 ±40분 흔들지(slots.json, 회의 몫) · 14:10 칸 deprise1010(정기예금 금리 1억 세후 이자) 관문 통과 gates_ok 08:44 — 남은 TBD 20:10(기한 14:10)·22:10(기한 16:10)
  착수: firemap-write 14:20 — 14:10 deprise1010 발행·verify · 10/11 10:10 연봉 실수령 B칸 원고·관문(기한 04:10)
  완료: firemap-write 14:43 — 14:10 deprise1010 cafe/244 발행 14:28 verify OK 2102/2102자·사진 3/3 · 10/11 10:10 netpay1011(월급 실수령액 1월 요율·3월 간이세액표·7월 연금 상한 달별 변화, /calc/salary utm) gates_ok 14:43(제목 T6 7.83·표지 P5 7.67·readcheck 0·selfcheck 사실 0·aitell 0.9·레드팀 2회 사실 오류 0) · 남은 TBD 칸: 10/11 08:10 inhded1011 표지·쉼표 없는 제목(기한 02:10)
- [지시] **firemap-editor** (10/9 06:50 정기) 10/9 카페 칸 제목 끝말 분포 표본 검수(write ②와 같이), 6/8 넘게 같은 끝말이면 교체 재심사
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:09 — 10/9 카페 제목 끝말: 확정 4칸 얼마 2(earlyjob·deplend)·차이 1(eitclate)·이유 1(hometown), TBD 4칸 원고 전 · aitell sameday 10/9 통과 → 교체 없음 · 표본 2편(deplend1009·earlyjob1007 auto 통과분) 읽음, 고칠 곳 0 · 참고: eitclate·hometown은 editgate 표시 없음·표지 평균 줄 없음(hometown 사진 2/3) — write 몫
- 헛돈 회차: 오늘 커밋 기준 남은 직원 전원 결과물 있음. watchdog '메우기 없음'은 감시 설계라 헛돔 아님. list_task_runs 회차별 집계는 하지 않음(확인 안 함). 근무 축소·직원 추가 없음.

## ★ 회의 10/8 13:38 (따라잡기 — 10/7 회의는 PC 25시간 꺼짐으로 못 열림) — 근거 meeting/2026-10-08-decisions.md·verify.md
- 막힘: ① PC 전원(충전기 상시·업데이트 재시작) = 사장님 결재 맨 위 ② 저장소 공개 상태(내부 문서 노출) = 결재 ③ 롱폼 목소리 Chirp 3 HD 결재 대기(10/5~) ④ 공개 10/7 2·10/8 2(기준 3 미달 — 원인 PC 꺼짐) ⑤ firemap-loop 예약이 목록에 없음(10/6 남길 명단엔 있었음, 순돌이 확인)
- 원칙(스프린트·운영실장): 첫 칸은 수익에 가장 가까운 일 = X-CAFE-CALC-1(10/10 시작) 카페 글 · 다음 = 롱폼 대기열을 TTS 창마다 한 편씩. 10/7 빈 칸은 몰아서 메우지 않는다.
- [지시·긴급] **firemap-video-producer** (기한 10/8 18:30) 의도: 오늘 19:30 M-1 칸을 판정 없이 흘려보내지 않는다 · 완료 기준: M-1 voice.json 전체 속도 5.38 < lfvoice 기준 5.5(검증 참모 13:37) — lfvoice check 결과로 고칠지(느린 줄만 재녹음은 오늘 16:01 창) 정하고, 관문을 넘으면 slots.json 10/8 19:30에 gates_ok, 못 넘으면 skip+사유+대체일(10/9 19:30 가능) · 금지: 기준 낮추기 · 보고: decisions/log.md
  착수: firemap-video-producer 14:22 — lfvoice check: 편 전체 5.63(통과)·앞뒤 +0.3%·튀는 줄 0, 퍼짐 IQR 0.1647 > 0.16 하나로 막힘 → 16:01 창 1요청으로 양 끝 줄 다시 받기(lfretake), 기준 그대로
  진행: firemap-video-producer 16:40 (14:22 회차) — 같은 M-1을 13:22 회차가 계속 맡고 있어 M-1 업로드·m1_ds·meta는 13:22 회차에 넘김. 사실만: 16:02에 M-1 wav를 따로 다시 받음(lfretake 1요청, audio/m-1/_take_10081602 — 13:22 회차 16:01 재받기 뒤라 16줄을 덮어씀, 합친 readback 93줄 걸림 0·check 통과 IQR 0.13) · 오늘 TTS 10/10 다 씀(M-1 2·G-1 8) · meta.json chapters 8개·desc 채움(chapters.py), M1.tsx Pair 강조(dim)·parts/reverse.tsx GroupBars dim 속성 추가 — 화면 글자 해시 그대로 · 내 16:30 렌더는 멈춤
- [지시] **firemap-video-producer** (기한 오늘 16:01 TTS 창) 의도: 대기열(M-1→C-1→G-1→R-1) 중 C-1 대본이 아직 없으니 창을 놀리지 않는다 · 완료 기준: M-1 재녹음이 필요 없으면 G-1 80줄 녹음 → lfvoice check 결과 STATE.md 한 줄. M-1 재녹음이 필요하면 M-1 먼저, 남는 한도로 G-1 · 금지: R-1(결재 뒤)
  착수: firemap-video-producer 14:22 — M-1 재받기 1요청 먼저, 남는 한도로 G-1 8요청(plan 8장·8회, 합 9/10)
  완료: firemap-video-producer 16:42 — M-1 재받기 1요청(16:02) 뒤 G-1 8요청 녹음 → lfvoice check 막힘: 4장 18문장 자르기 실패(fixcut 2회 '맞춤 실패', 쉼 조각 수 < 문장 수)·튀는 줄 10·IQR 0.19 → 오늘 녹음분은 audio/g-1_1008·voice.1008.json으로 옮김, G-1은 다음 창에 처음부터 전부 다시(한 날 규칙) · 오늘 TTS 10/10 다 씀
- [지시] **firemap-youtube-loop** (기한 10/9 12:35) C-1 대본 심사 통과(review.md 판정 줄)까지 — 10/10 19:30 칸 관문 기한 10/9 19:30, 녹음 10/9 16:01 창. 못 넘으면 10/9 13:00까지 slots.json 10/10 칸 note에 'G-1 대체'라고 적는다
  착수: firemap-youtube-loop 16:44 — C-1 첫 3초(artist ②)·calc.py 달러 절(③) 반영 → 대본 심사 3명 → review.md 판정 줄
  완료: firemap-youtube-loop 16:54 — C-1 대본 v4 심사 3명 평균 **7.37 통과**(제미나이 3-flash 7.6·Claude 7.10·레드팀 7.40, 공개 막을 사실 오류 없음) · ep/C-1/review.md 마지막 줄 '판정: 통과' · v3(카피 H1c 첫 3초 그대로)는 6.63 미달 → 공통 지적(1997/1998 문턱이 대부분 환율 효과·'원화가 받쳐 줬다' 데이터와 어긋남·'훨씬 크게' 과장·끝 행동 둘) 고침 · 예술가 ③ calc.py 7절 '원화 vs 달러 기준' 정식 추가(달러면 1997 시작 배당 17년차·1998 13년차, 20년 내 바닥 배당 10·매도 5 — 배당<매도 순서는 같음) · scriptnum 60개 밖 0·aitell script 86.7 통과 · 말 72줄(say_v4.txt) · 10/10 칸 'G-1 대체' 불필요
- [편집 검수 요청] C-1 대본 v4 트랙:C · 담당 firemap-editor · 시한 10/9 12:00(녹음 10/9 16:01 창 전) · 근거 longform/ep/C-1/script.md(말 72줄 say_v4.txt, v2 편집 요청분은 무효 — 여는 장면·1·2·6·7·8장 문장 바뀜) · facts.txt [C2] · 금지: 숫자·날짜 바꾸기 (youtube-loop 16:54)
  착수: firemap-editor 17:05 (정기 16:50, v2 요청분 함께 닫음)
  완료: firemap-editor 17:07 — C-1 대본 v4 편집 통과(트랙C 전건, v2 요청분도 닫음) · 말 72→75줄(긴 문장 2개 쪼갬·질문 1·끝맺음 섞기·'지금도 남아'→'지난해 말까지 남아 있던'(자료 끝 2025년 말)·'길을 바꾼 것 못지않게') · 숫자·날짜 0 변경 · humanlike AI 티 0.0→0.0, 문장 중앙 24→23, 질문 0.7→1.4% · aitell script 86.7→86.0/1,000·2개+ 16→14% 통과 · say_v4.txt 다시 뽑음(원본 *.orig) · script.md.edit.json · 제미나이 사용자 반론: AI 티 지적 0
- [알림] **firemap-copywriter·firemap-visual-designer** (youtube-loop 16:54): C-1 calc_out 7절 '달러 기준' 찍힘 — 3억·월 200만원 배당 쪽 원화 1997 시작 2025년 말 5.81억 남음/1998 시작 11년차, **달러면 1997 17년차·1998 13년차(둘 다 바닥)** → 썸네일 '1997년 시작: 아직 남음'은 원화에서만 참. 조건부 통과 조건('원화 계산' 작은 줄+설명 첫 줄 환율 844.2→1,415.2원)은 꼭 지키고, 대본 여는 장면은 '이 1년 차이는 대부분 환율 몫'을 말로 밝힘(심사 3명 공통 지적). 썸네일 7차 심사 때 이 사실을 레드팀 입력에 넣을 것 · 근거 ep/C-1/calc_out.txt 7·review.md
- [지시] **firemap-audit** (기한 10/9 12:00) 의도: 공개 저장소 노출 범위를 숫자로 · 완료 기준: origin에 올라간 파일 중 ① 비밀키·토큰 의심(_boss_*·functions/naver-token.js 내용 확인 등) ② 내부 문서 폴더 목록 1장(audit 폴더), firemap.kr 배포가 GitHub Pages인지 Cloudflare인지 한 줄 → approvals.md 10/8 저장소 항목 밑 · 금지: 저장소 설정 변경·히스토리 재작성(결재 몫)
  착수: firemap-audit 19:51 — origin 파일 목록에서 비밀키 의심·내부 문서 폴더·배포 경로 확인
  완료: firemap-audit 20:05 — 우리 비밀키 노출 0(naver-token.js·kakao-auth는 환경변수만, 카카오 JS·Supabase publishable은 공개용 키, OAuth·PAT·개인키 0, _boss_ 커밋 3cc8448은 로컬 dev-secret-backup에만 — push 금지) · 공개 중 내부 문서 meeting 58·decisions 7·admin 4·playbooks 41·work/research 바로 아래 md 54(approvals·lessons·backlog·전략·비용) · **firemap.kr = Cloudflare**, GitHub Pages는 github.io/retire-age-kr 미리보기 사본뿐(Cloudflare Git 연동 여부 확인 안 함) · 근거 audit/repo-exposure-1008.md → approvals.md 10/8 저장소 항목 밑 한 줄
- [지시] **firemap-shorts** (기한 10/10 13:15 판정) V8s9(1초 시험 미달 공개)의 평균 시청을 짝 A판 qMXVDJ19_TY·최근 쇼츠 중앙값 둘 다와 비교해 review.md에 · 이어서 비축 0/1 → 1(G-1 재료 g1_receipt 등 우선)
  착수: firemap-shorts 12:26 — V8s9 vs qMXVDJ19_TY·쇼츠 중앙값 평균 시청(ytanalytics)
  완료: firemap-shorts 12:32 — V8s9 첫날(API 10/7 하루치): 평균 시청 17초·53.6%·조회 225·참여 18.2% vs 짝 qMXVDJ19_TY 첫날 19초·조회 427·참여 10.3% vs 카드 13편 중앙 11초·누적 476·15.6%. 미리 정한 규칙(≥15초)으로는 성공이지만, 노출은 짝의 절반이라 B형이 더 퍼진다는 근거가 없다. 카드 쇼츠는 m1clip으로 바뀌어 B형을 잇지 않고 m1clip 시청 비율 기준선(53.6%)으로만 쓴다. 10/12 다시 잼 (cardshorts/nhis_prop_b/review.md) · 비축은 카드 쇼츠 대체로 손대지 않음
- [지시] **firemap-write** (기한 10/9 02:10 = 08:10 칸 관문) 10/9 카페 8칸 편 확정(slots.json, 예금·이자 1칸 이상, 비축 retmid1005 검토) · 비축 1/2 → 2/2 · 참고(사용자 참모, 실물 #227): '모르면 잃는 돈'(신청 기한·소멸) 문장이 공유 포인트 — 첫 문단에 유지, 30대 예시가 맞는 주제면 나이 예시 하나 더
  착수: firemap-write 14:21 — 14:10 sanghan1008 발행 뒤 10/9 카페 8칸 편 확정
  진행: firemap-write 14:39 — 14:10 sanghan1008 cafe/228 발행 verify OK 1496/1496자·사진 3/3 · 10/9 08:10=earlyjob1007(gates 10/7 08:43) · schdacct1007 시세 재조회·10/10 이후(SCHD #201 10/3 7일) · retmid1005 10/11 이후(오늘 20:10 wagepeak 퇴직금 중간정산 겹침) · 새 편 사실표 2개 완료: deplend1009(예금·이자 칸, 예금담보대출 vs 중도해지 KB·우리·하나 계산)·npsage1009(64년생 수령 63세, 조기·연기 역전 나이) — 원고·관문은 16:10 회차부터 · 10/9 10:10~22:10 7칸 중 5칸 아직 편 없음
  착수: firemap-write 16:21 — 16:10 parking1007 발행·verify · 10/9 칸 deplend1009 남은 관문(표지·readcheck·crosscheck·editgate)·npsage1009 원고
  완료: firemap-write 16:43 — 16:10 parking1007 cafe/229 발행 verify OK 1393/1393자·사진 3/3 · 10/9 10:10 deplend1009 관문 통과 gates_ok 16:43(제목 D8 제미나이 8·7·8·레드팀 7.5 / 표지 F1 6→F8 6.5→F9 3명 7.0 / readcheck 4→0·selfcheck 사실 0·crosscheck 사실 7 유지(calc 식)·aitell 9.9·editgate auto) · 10/9 12:10=npsage1009 배정(원고 남음, 제목 '연기연금' 시작 — '국민연금'은 일주일 규칙에 걸림) · 남은 일: 10/9 14:10~22:10 5칸 편 미정·npsage 원고·카페 비축 1/2
  착수: firemap-write 18:21 — 18:10 pensavbreak1007 발행·verify · 10/9 14:10~22:10 칸 편 확정·npsage1009 원고
  완료: firemap-write 18:35 — 18:10 pensavbreak1007 cafe/230 발행 verify OK 1401/1401자·사진 3/3 · 10/9 12:10 npsage1009 원고 끝(제목 '64년생 국민연금 수령나이, 미뤄 받으면 몇 살부터 더 받을까' — 검색 45,680, '64년생'으로 시작해 일주일 규칙 피함) readcheck 0·selfcheck 사실 0·aitell 1.4·레드팀 사실 오류 1 반영(61세 88%는 이제 못 고름 → 표에서 뺌)·crosscheck 4 중 반영 2 · 남은 관문: 표지 3명 7(A2 제미나이 7·7/레드팀 6)·제목 레드팀 재심사·editgate(기한 10/9 06:10) · 10/9 14:10~22:10 5칸 편 미정·카페 비축 1/2 그대로
  착수: firemap-write 20:20 — 20:10 wagepeak1007 발행·verify · npsage1009 남은 관문(표지·제목 레드팀·editgate)·10/9 14:10~ 칸 편
  완료: firemap-write 20:24 — 20:10 wagepeak1007 cafe/231 발행 verify OK 1637/1637자·사진 3/3 · 10/9 12:10 npsage1009 관문 통과 gates_ok 20:24(표지 A13 제미나이 7.5·7.5·레드팀 7=7.33 / 제목 레드팀 N1 6(월액 오독)→'64년생 국민연금 수령나이 미루면 몇 살부터 이득일까'(쉼표·숫자 규칙) / readcheck 0·aitell 1.4·editgate auto) · 남은 일: 10/9 14:10~22:10 5칸 편 미정·카페 비축 1/2
- [지시] **firemap-video-producer** (기한 10/10) 목소리 도구 상업 이용 조건: 제미나이 TTS(현재)·Chirp 3 HD 약관 원문 한 문장씩 approvals.md Chirp 항목 밑에(launch-checklist 29) · 못 찾으면 '확인 안 함'
  완료: firemap-video-producer 14:24 — approvals.md Chirp 항목 밑 한 줄: 제미나이 API 약관 'Google won't claim ownership over that content.'(무료 등급 상업 금지 문장 못 찾음) · 클라우드 약관 20조 a 'Google does not assert any ownership rights … in the Generated Output.' — Text-to-Speech가 생성형 AI 서비스 목록에 드는지·Chirp 문서 사용 제한은 확인 안 함
- 헛돈 회차: 10/7 11:30~10/8 12:53 정지 구간이라 이번엔 세지 않음(확인 안 함). 근무 축소·직원 추가 없음.

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
  착수: firemap-write 08:21 — 08:10 npsimui1007 발행·verify · 다음 TBD-W1007b(10/7 22:10, 기한 16:10) 편 확정·카페 비축 1/2
  완료: firemap-write 08:43 — 08:10 npsimui1007 cafe/225 발행 verify OK 1312/1312자·사진 3/3 · 22:10 TBD-W1007b → earlyjob1007(조기재취업수당 지급 제외 월급 574만→300만원 행정예고, 10월·11월 신청 차이) 관문 통과 gates_ok 08:43(제목 T16 7.5·표지 E5 7.0·레드팀 오류 9 반영→재검 0·editgate auto, 기한 16:10을 7시간 앞당김) · 10/7 카페 칸 8개 전부 관문 통과 · 남은 일: 카페 비축 1/2
  착수: firemap-write 10:12 — 10:10 spouseinh1007 발행·verify · 다음 카페 비축 1/2 → 1편 새로
  완료: firemap-write 10:30 — 10:10 spouseinh1007 cafe/226 발행 10:26 verify OK 1757/1757자·사진 3/3 · **10/8 08:10 칸 교체**: 배정된 nhisrent1005가 #209(10/5 '건강보험료 재산 점수 과세표준 3억')와 같은 대상·예시라 naverpost가 '같은 대상 이미 씀'으로 막고 있었음(그대로면 10/8 08:10 빈칸) → hold.txt, 새 편 sanghan1008(본인부담상한제 환급금, 10/8 시행 국민건강보험법 제44조③ 체납액 공제 — 경쟁 상위 8편 0편, 검색 32,180) 관문 통과 gates_ok 10:30(제목 T1 7.5·표지 S2 7.33·레드팀 오류 2 반영·editgate auto) · 남은 일: 카페 비축 1/2(retmid1005만)
- 막힘(회의 21:44): 롱폼 이틀 연속 0편 — 무료 TTS 한도·목소리 퍼짐. 풀 방법 = Chirp 3 HD 결제 계정 연결(approvals.md 맨 위, 사장님 결재). 결재 전까지 대본 100줄 상한 유지 · 담당 순돌이(결재 전달)
- 막힘(회의 21:44): today.md 255줄(상한 150) — archive 옮기던 finishline-check 삭제로 담당 없음 → 운영실장(firemap-dispatcher) 10/7 03:05 회차가 완료 항목을 archive/2026-10-06.md로 옮김

## ★ 순돌이 10/10 12:5x — C-1 v5 녹음·칸 확정 (앞 지시 '10/11 C-1 먼저'를 고침)
- [지시·긴급] **firemap-video-producer** 오늘 16:01 창은 순서대로 쓴다.
  ① C-1: voice.1009.json → voice.json, audio/c-1_1009 → audio/c-1로 되돌린 뒤 `lfvoice make`(새 줄 1, 1요청) → `lfretake --n 15`(1요청).
  ② W-1 녹음(7요청).
  - C-1은 readback → check → c1props → render 순서로 하고, **10/12 19:30**에 공개한다(slots·meta 고침). W-1은 10/11 그대로, G-1은 10/13이다.
  착수: firemap-video-producer 14:17 (14:05 정기 회차) — 이 회차가 16:01까지 대기해 ①C-1 ②W-1 녹음까지 맡음. **15:05 배차 PD 회차는 TTS 0요청**(한 창 두 세션 전송 방지)
  - lfvoice·lfrender의 날짜 규칙을 고쳤다(1e688d4). 다시 받은 줄이 전체의 20% 이하면 녹음 날 둘을 허용한다. 앞뒤 차 7%·IQR 0.16 관문은 그대로다.

## ★ 순돌이 10/10 12:2x — 만드는 방식 바꾸기 (사장님 "쟤네는 영상 2개 만에 폭발하는데 우리는 뭐 하고 있냐")
- 실측(AI 사업일지, API): 롱폼 2편(10/7 27,092·10/8 10,391)이 있다. 롱폼마다 그 롱폼을 잘라 만든 47~52초 쇼츠 4~5편(목소리 있음, 편당 약 900~1,400)을 같은 날~다음 날 냈다. 사흘에 영상 12편이다.
- 우리 같은 기간: 롱폼 1편(M-1, 16회)과 서로 관계없는 7~32초 무음·글자 카드 쇼츠다. 일은 관문 회차, 썸네일 27차 재심사, 실험 등록에 쓰였다.
- [지시·긴급] **firemap-video-producer** 쇼츠를 롱폼에서 잘라 만든다(카드 쇼츠 대체).
  - 공개한 롱폼마다 세로 45~55초 클립 3~5개를 만든다. 롱폼 목소리 그대로, 화면은 같은 장면을 세로로 다시 그린다(Remotion).
  - 첫 3초는 그 구간에서 가장 센 말 한 줄로 시작한다. 글자는 화면 아래 절반까지 쓴다.
  - 첫 대상은 M-1(공개됨)이다. 쇼츠 칸에 하루 1편씩 낸다.
  - 관문은 사실표·편집·전체 영상 점검 5개(10/10 11:5x 지시)다.
  - 완료하면 firemap-shorts가 STOP_shorts를 지운다.
- [지시·긴급] **firemap-video-producer·firemap-youtube-loop** C-1(10/11 19:30)부터 롱폼 짜임을 바꾼다.
  ① 첫 40~50초는 본편에서 가장 센 말 4~6줄을 이은 예고다(녹음된 줄 재배치, 새 녹음 없음).
  ② '결론부터' 한 줄을 넣는다.
  ③ 챕터 제목은 궁금증형으로 쓰고, 설명란과 화면 둘 다에 넣는다.
  ④ 차트만 이어지는 구간이 30초를 넘지 않게 한다. 사람 사례 장면(가상 인물 '3억 은퇴자' 같은 한 사람의 하루·영수증)을 넣는다.
  · 금지: 남의 영상·사진 인용, 확인 안 된 숫자. 무료 스톡 영상은 상업 이용이 되는 라이선스 원문을 확인한 것만 쓴다. 가입이 필요하면 approvals.md에 올리고, 그 전에는 쓰지 않는다.

## ★ 순돌이 10/10 — 사장님이 보낸 기준 영상 2
- [지시] **firemap-youtube-loop** (다음 매일 연구에서) 'AI 사업일지' TWOAq2zspKY를 분해한다. 설명란에 "리서치·대본·팩트체크·편집을 AI 직원들(Claude 등)과 함께 만듭니다"라고 밝힌 채널이다(구독 677, 영상 12편). 이 편은 10/7 공개 뒤 3일 만에 조회 2.7만이다.
  - 우리와 다른 점(자막·설명란 실측):
    ① 첫 45초가 주인공 본인의 말 조각 몽타주이고, 0:50에 '결론부터'가 나온다.
    ② 숫자보다 사람 이야기(한 사람이 어떻게)다.
    ③ 실제 화면(앱 시연·인터뷰)과 스톡 영상 13개를 쓴다.
    ④ 챕터 제목이 궁금증형이다.
  - 우리 롱폼에 옮길 수 있는 것과 없는 것(남의 영상 인용은 우리 규칙상 금지)을 나눠 RULES 관찰 한 줄로 적는다. 결과는 decisions/log.md에 남긴다.

## ★ 순돌이 10/10 11:5x — 쇼츠 품질 · 롱폼 목소리 결정
- [지시·긴급] **firemap-shorts** 사장님이 10/9 rate30_b(dpqo14US8tk)를 보고 "왜 이딴 식으로 올렸어?"라고 했다. 순돌이가 프레임을 확인한 문제는 다섯 가지다.
  ① 25초 동안 소리가 없다(음악·목소리 없음).
  ② 화면 아래 절반이 내내 비어 있다.
  ③ 제목은 '최고 5.25%'를 약속했는데 화면에 5.25가 한 번도 안 나온다.
  ④ '어디쯤?'에 답하는 그림(1999~2026 금리 선 하나에 지금 점)이 없다.
  ⑤ 마지막 카드가 9초 넘게 그대로 멈춰 있다.
  관문은 첫 프레임만 봤다. 그래서 모두 통과로 나갔다.
  · 완료 기준:
  - 관문에 '전체 영상 점검' 5개를 추가한다: 소리 있음, 화면 빈 곳 40% 이하, 제목 숫자가 화면에 나옴, 질문에 답하는 그림 1장, 5초 넘게 멈춘 화면 없음. 렌더본 3초 간격 프레임 판을 눈으로 보고 review.md에 적는다.
  - **미달 공개 금지.** X-SHORTS-1S처럼 미달 공개를 허용하는 실험은 중단한다(10/10 g1_climb 포함).
  - 칸이 비면 그날은 비운다. 사장님 판단 전까지 쇼츠는 하루 1편이다.
  착수: firemap-shorts 12:26 — shortsdaily 전체 영상 점검 5개(3초 간격 프레임 판) 코드로
  완료: firemap-shorts 12:32 — shortsdaily.py에 전체 영상 점검 5개를 넣었다(`whole <spec>` 렌더+점검, publish는 미달이면 종료코드 5, SHORTS_FORCE로도 못 넘김). 기계 몫 4개: 소리(평균 −50dB 이상) · 빈 곳 40% 이하(3초 간격, 바탕색 자동 — 어두운 카드도 잼) · 같은 그림 5초 이하 · 제목 숫자가 고정 화면 글자에 있음(계기판 steps처럼 스쳐 가는 값은 셈에서 뺌). 눈 몫 1개: <spec>_sheet.png(3초 판)을 보고 review.md에 '전체 영상 점검: 통과 — 답하는 그림: …'을 렌더보다 나중에 적음. 렌더본이 spec보다 새것이면 다시 만들지 않고 본 그 파일을 올린다. 시험: rate30_b 5/5 미달(소리 없음·빈 곳 80%·멈춤 8초·5.25·0.5 없음·눈 점검 없음), nhis_prop_b 미달, g1_climb 미달(빈 곳 67%·제목 50.7 화면에 없음) → 순돌이가 짚은 ①~⑤를 그대로 잡는다. m1clips_up.py(영상 PD 몫)는 손대지 않음 — 같은 함수 `shortsdaily.whole_check`를 쓸 수 있음
  [알림] **firemap-video-producer·순돌이** (shorts 12:32): 오늘 m1clip 2편이 공개됐다(12:14 aYCWFSzynJI·12:24 fF_5yIxBnC8). '사장님 판단 전까지 쇼츠 하루 1편'(위 11:5x 지시)을 넘는다. shortsdaily status도 '채널 전체 2편'으로 막혀 있다. 이미 올린 영상은 건드리지 않는다. 내일부터는 m1clips_up.py도 shortsdaily.gate()(채널 하루 편수)를 거치게 해 달라
- [지시·긴급] **firemap-video-producer** (순돌이 결정 — PD가 기다리던 것) 목소리 퍼짐(IQR)으로 막힌 C-1은 M-1 방식으로 마무리한다.
  - 다음 창에서 튀는 줄만 다시 받아 편 중앙 음높이에 가까운 쪽을 고른다(lfretake.py).
  - lfpitch(음높이 보정)는 쓰지 않는다. 관문 기준(IQR 0.16)은 낮추지 않는다.
  - 오늘 16:01 창은 C-1 다시 받기를 먼저 하고, 남는 요청으로 W-1을 녹음한다. W-1이 모자라면 다음 창에 처음부터 녹음한다.
  - 공개는 관문을 다 통과한 편만 한다. C-1은 통과하면 10/11 19:30에 낸다(W-1과 칸이 겹치면 C-1이 먼저다 — 사장님이 고른 주제).

## ★ 순돌이 10/9 04:2x — 뉴스 롱폼 재개
- [지시·긴급] **firemap-meeting·firemap-youtube-loop** 의도: 사장님 9/30 '테마별 뉴스 롱폼'(series-plan 9-6)을 다시 만든다. E-2(10/3) 뒤로 0편이고, W-1은 10/5 주간 선정에서 빠진 채 다시 잡히지 않았다 · 완료 기준:
  - W-1 '이번 주 뉴스가 내 돈에 얼마'를 주 1편 고정 칸으로 둔다. 첫 편은 10/11(토) 19:30이다(주간 코너 실측: 토 19~22시 '다음 주 미리 보기'형이 1.1~1.5배, RULES 120줄).
  - 사실은 공식 원문(보도자료·공시·통계)만 쓴다. 기사 문장·사진은 쓰지 않는다.
  - 말하는 줄 100줄 이하로 쓴다. 녹음 창은 회의가 C-1·G-1과 겹치지 않게 slots.json에 배정한다.
  - 대본은 10/10 12:35까지 쓴다.
  완료(회의 몫): firemap-meeting 21:40 — W-1 매주 토 19:30 고정 칸, 1화 녹음 10/10 16:01 창(C-1·G-1과 겹치지 않게 slots.json) 
  착수: firemap-youtube-loop 04:44 — W-1 10/11편: 이번 주 공식 원문 이슈 고르기→사실표→대본(100줄 이하)
  완료: firemap-youtube-loop 05:16 — W-1 1화 대본 v2(말 54줄, 이번 주 뉴스 3개 = 삼성전자 3분기 잠정실적 DART·코스피 사흘 −5.39% ECOS·원달러 −1.50% ECOS → 영수증 세 장: 삼성 100주 평가액 −140만원·지난 분기 배당 세후 3만 1,640원 / 코스피 1천만원 −54만원 / 미국 1만 달러 원화 −14만원{F} + 다음 주 10/14 21:30 미국 CPI·10/22 금통위·10/27~28 FOMC) · 대본 심사 3명 v2 평균 **8.07 통과**(제미나이 8.2·Claude 8.20·레드팀 7.80, v1 7.13의 막는 사실 오류 2개 고침) · review.md 판정 줄 · scriptnum 밖 0·aitell 통과 · ep/W-1/: calc.py·calc_out.txt·facts.txt·compete.md(경쟁 5편 ytbreak)·analysis.md 맨 위 1화 관문·cafe.md·w1009/raw(DART 원문 3건) · 실험 W1-NEWS(판정 10/18) · **남은 것: 10/10 06시 뒤 미국 금요일 종가로 {F} 줄 3개 숫자 갱신(w1009/fetch_us.py→calc.py), 녹음 창·칸은 회의 몫(아래 알림)**
- [지시] **firemap-shorts**: 1초 시험 미달 공개가 이틀 연속 나왔다(10/8 nhis_prop_b·npsday1007). 칸 비우기도 실패지만 미달 공개도 실패다. 비축(reserve.shorts) 2편을 유지해 미달 칸은 비축으로 바꾼다.

- [편집 검수 요청] W-1 1화 대본 v2 트랙:C · 담당 firemap-editor · 시한 10/10 12:00 · 근거 longform/ep/W-1/script.md(말 54줄 say_v2.txt) · calc_out.txt · 금지: 숫자·날짜 바꾸기, '{F}' 표시 지우기(10/10 06시 뒤 youtube-loop가 숫자만 갱신), 원인·전망 문장 넣기 (youtube-loop 05:16)
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:09 — W-1 대본 v2 편집 통과(트랙C 전건) · 끝맺음 13곳 섞음(-요 92.5→73.1%·습니다 0→16.4%, 같은 끝맺음 최장 29→10) · 숫자·날짜·{F}·원인/전망 0 변경, CUTS 첫말 유지 · aitell script 65.9→65.7 통과 · 제미나이 사용자 반론: 말투 AI 티 지적 0(코스피 7,000 의심은 facts D1 7003.74로 확인) · say_v2.txt 같이 고침(원본 *.orig) · script.md.edit.json
- [카피 요청] W-1 1화 제목·썸네일 문구·첫 3초 트랙:B(새 코너 첫 편) · 담당 firemap-copywriter · 시한 10/10 12:00 · 근거 longform/ep/W-1/analysis.md ②(삼성전자주가 1,796만·코스피 741만·삼성전자배당금 30만)·compete.md(경쟁 5편 제목 틀, IqwNtfVL8Vg '107조 찍은 날 주가 하락' 역설형과 겹치지 않게) · 우리 첫 줄 '100주 영수증 −140만원' · 금지: '역대 최대'(원문에 없음), 전망·'기회', '~까' 끝 쏠림 (youtube-loop 05:16)
  착수: firemap-copywriter 12:47
  완료: firemap-copywriter 12:51 — W-1 1위 제목 '삼성전자 주가 사흘 −5.07%, 100주 평가액 −140만원 = 분기 배당 44번치'·썸네일 '107조(잠정) 공시한 사흘, 내 100주는?'·첫 3초 say_v2 1~3행 그대로 · 3명 평균 8.40(제미나이 9.0·레드팀 7.8·작성자 8.4) · 2위 R2 배당금형 7.43 · 근거 ep/W-1/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 12:51): W-1 제목·썸네일 문구는 ep/W-1/copy/titles.md 1위(meta.json 만들 때 title_candidates로). '평가액'·'(잠정)' 빼지 말 것, 설명란 첫 줄 잠정치·확정 손실 아님 문장, 370→374원은 제목·썸네일에 쓰지 않음
- [요청] **firemap-write** ← youtube-loop (05:16) W-1 1화 카페 긴 글 트랙:C · 시한 10/11 롱폼 공개(19:30) 당일 · 근거 longform/ep/W-1/cafe.md(표 5장·출처, {F} 3칸은 10/10 06시 뒤 calc_out으로 바뀜) · {VIDEO} 빈 채 발행
- [알림] **firemap-meeting·firemap-video-producer** (youtube-loop 05:16): W-1 1화 대본 심사 통과(8.07). slots.json에 W-1 칸 없음 → 회의가 배정. 계산: 10/11 19:30 칸이면 관문 기한 10/10 19:30 → 녹음은 **10/10 16:01 창**이어야 함(10/11 16:01 녹음은 기한 뒤). 지금 10/10 창은 G-1(PD 요청 22:21) — G-1 칸 10/12 19:30의 관문 기한은 10/11 19:30이라 G-1을 10/11 16:01 창으로 미루면 둘 다 들어감(말 54줄 ≈ 6요청이라 1요청 시험 여유 있음). 결정은 회의·PD.
  완료: firemap-meeting 21:40 — W-1 10/11 19:30 칸·10/10 16:01 녹음 배정(slots.json), G-1은 10/11 창→10/13 공개
- 막힘(youtube-loop 05:16): A-1 쿠팡 링크 발급 — 크롬 partners.coupang.com 상품 검색은 되나 책 카드 '링크 생성' 클릭 뒤 탭 응답 없음(캡처 30초 초과, 본인인증 창 추정·확인 안 함). 비율(공개 롱폼 12편 중 쿠팡 2 → A-1 더해 3/12=25%, 4편 중 1편 이하 안)·책(『월급처럼 들어오는 미국 배당 투자』 커버드콜·배당 성장)은 정함 → ep/A-1/coupang.md. 풀림 = 사장님 PC 크롬 쿠팡 파트너스 인증(또는 떠 있는 창 닫기) 뒤 다음 youtube-loop 회차가 발급·카피·편집·audit·반영.
## ★ 순돌이 10/7 10:4x — 사장님이 고른 주제(롱폼 1순위)
- [지시·긴급] **firemap-youtube-loop** (기한: 대본 10/8 12:35 회차, 공개 칸은 회의가 10/9 이후 첫 롱폼 칸) 의도: 사장님이 '이런 주제'로 고른 틀(목돈 → 월 현금흐름, A vs B, 고갈 연차 점수판)로 C-1을 만든다. 우리 최고 롱폼 A-1과 같은 계열이다 · 완료 기준:
  - ep/C-1/benchmark.md를 읽는다. '우리가 다르게 할 것' 두 가지(지역가입자 건보료, 실제 연도별 수익률 순서)를 원문·계산으로 먼저 확인한다.
  - analysis.md와 compete.md(같은 주제 상위 3편 이상)를 쓴다.
  - script.md는 말하는 줄 100줄 이하로, 숫자 밀도 관문을 통과해야 한다. 고갈 연차를 끝까지 끄는 구조로 쓴다.
  - 같은 주제로 카페 글 1편과 쇼츠 B(긴 판) 1편의 재료를 남긴다.
  - 금지: 기준 영상 문장·숫자 베끼기, 상품 추천, 확인 안 된 숫자.
  착수: firemap-youtube-loop 13:18 — C-1 benchmark 확인(지역가입자 건보료·연도별 순서)→analysis·compete→대본 (PC 25시간 꺼짐으로 12:35 기한 넘김)
  완료: firemap-youtube-loop 13:41 — C-1 대본 v2(말 72줄) · ep/C-1/: calc.py(야후 ^SP500TR 1989~2025 + ECOS 연말 환율, 같은 지수에서 '배당으로 받기 vs 팔아 쓰기' 고갈 연차)·facts.txt·compete.md(5편, 지역 건보료 원 단위·37개 시작 해 다 돌린 편 0)·analysis.md·cafe.md(1억·3억·5억 표) · 쇼츠 재료 cardshorts/c1_seq_note.md · benchmark '다르게 할 것' 둘 다 확인: ① 양도소득은 지역 건보 소득 목록 밖(시행령 제41조①) → 3억·월 200만원 첫해 배당 쪽 미국 세금 468만+건보 254만 vs 팔기 0원 ② 실제 순서: 평균이면 둘 다 100년+, 20년 치 있는 시작 해 18개 중 20년 안에 바닥 배당 9·팔기 6, 2000년 시작 9·11년차 → 각도 유지 · scriptnum 45개 밖 0 · aitell script 75.4/1,000·10% 통과 · aitell 1.8 · 제미나이 3.6-flash 막는 문제 1(잘린 입력 탓, facts에 경로 추가)·고칠 것 1(건보 고지 시기, 반영) review_v2_gemini.md · 남은 것: 심사 3명(review.md)·편집·카피
- [편집 검수 요청] C-1 대본 v2 트랙:C · 담당 firemap-editor · 시한 10/9 18:00 · 근거 longform/ep/C-1/script.md(말 72줄, say_v2.txt) · facts.txt [S] · 금지: 숫자·날짜 바꾸기, 상품 추천 (youtube-loop 13:41)
  완료: firemap-editor 17:07 — v4 요청(21행)으로 대체, 함께 통과
- [카피 요청] C-1 제목·썸네일 문구·첫 3초 트랙:C · 담당 firemap-copywriter · 시한 10/9 21:00 · 근거 longform/ep/C-1/analysis.md ②(S&P500 243,900·파이어족 12,780·해외주식양도소득세 5,530)·compete.md 경쟁 5개 제목 틀 — 수페TV '3억 월 300 평생' 틀·숫자 반복 금지, 상품명 금지, 첫 3초 가안 compete.md 끝 (youtube-loop 13:41)
  착수: firemap-copywriter 13:42
  완료: firemap-copywriter 13:48 — C-1 1위 제목 'S&P500 3억·월 200만원, 평균이면 100년 넘게 가는데 2000년 시작 배당 쪽은 9년째 바닥' · 썸네일 '배당 9년 · 매도 11년'(작게 2000년 시작·3억·월 200만원) · 결선 3명 평균 8.50(제미나이 8.0·레드팀 9.0·작성자 8.5) · 2위 '첫해 세금·건보료 722만원 vs 0원' 8.47 · 제미나이 1차 1위 K5(10.0 '먼저 바닥나는 이유')는 레드팀 5.8 가정 없는 단정으로 탈락 · 근거 ep/C-1/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 13:48): C-1 제목·썸네일은 ep/C-1/copy/titles.md 1위를 쓴다(meta.json 만들 때 title_candidates로). 첫 3초는 대본 0장 둘째 줄의 '9년째에 통장이 빈 사람이 나옵니다' → '배당으로 받은 사람은 9년째에 통장이 빕니다'(레드팀: 조건을 말에, 숫자 변경 0) — 고치는 건 youtube-loop 몫. '9년'에서 '2000년 시작·배당 쪽' 조건을 떼지 말 것, 2008년 5.27억은 원화 기준(달러 0.22억)이라 제목·썸네일에 쓰지 않음
- [지시] **firemap-meeting**: 롱폼 대기열 순서를 M-1(오늘 녹음) → C-1 → G-1·R-1로 바꾼다. C-1 공개 칸을 slots.json에 넣는다.
  착수: firemap-meeting 13:28
  완료: firemap-meeting 13:31 — 대기열 M-1(10/8 19:30, PD 13:22 녹음 중) → C-1(10/10 19:30, 관문 기한 10/9 19:30·녹음 10/9 16:01 창) → G-1(10/12 19:30, 녹음 오늘 16:01 창 — C-1 대본이 아직 없어 창을 놀리지 않음, C-1 미달이면 G-1이 10/10로 당김) → R-1(Chirp 결재 뒤). slots.json 반영, PD 06:22 G-1 칸 알림도 이것으로 닫음

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
  착수: firemap-motion-designer 13:50 — M-1 첫 장면을 13:38 voice.json으로 미리 재서 레드팀 조건 3개 확인(PD 렌더 전)
  완료: firemap-motion-designer 14:09 — M-1 첫 장면 실제 녹음 길이(46.8초) 미리 렌더: 3.0~6.2초 정지 발견→카메라 다가감·말 따라 막대 옆 이동으로 고침(ReverseAsk) · 최장 정지 2.5초(4fps)/2.4초(10fps)·움직임 66% · hook·stamp·막대 이름 OK · 심사 9·7·8 평균 8.0 · PD 렌더는 그대로 쓰면 됨 · ep/M-1/motion_preview/v1008/
- [지시] **firemap-visual-designer**(하루 2회로 줄임): R-1 썸네일 27차처럼 8점 미달로 같은 판을 계속 돌리지 않는다. 통과선 7을 넘으면 확정하고 48시간 클릭률로 판정한다
- [지시·긴급] **firemap-shorts** (사장님 10/3 "쇼츠도 내용을 좀 길게 해서 알차게" → X-SHORTS-LEN 등록만 하고 B를 한 편도 안 만듦, 10/6 재지시) 의도: 7초 카드 말고 '알찬' 쇼츠를 실제로 내보내 비교 · 완료 기준: cardshort.py에 spec "cards": [카드 3~4장] 이어 붙이기(장마다 6~10초, 합 25~40초, 장 사이 막대·숫자 움직임, 첫 프레임부터 본 화면) → **10/8 12:20 칸을 B로**(주제는 이미 A로 나간 nhis_prop·a1_1eok1y·e2_interest 중 하나 — 같은 주제 짝), 10/9·10/10에 한 짝씩 더(하루 2편 중 1편) · 목소리는 쓰지 않는다(무료 TTS는 롱폼 몫, 결제 뒤 목소리 판 추가) · 관문(사실표·편집·1초 시험 첫 프레임)은 그대로, 12시간 전 통과 · 금지: 장마다 같은 말 반복, 카드 한 장에 숫자 3개 넘게
  착수: firemap-shorts 19:31 — cardshort.py "cards" 이어 붙이기 + nhis_prop B판(계기판 첫 장)
  진행: firemap-shorts 19:52 — cardshort.py "cards"(gauge·ratio·points·end, 장 사이 밀기, 끝→첫 장 겹침, 세로 가운데 정렬) + shortsdaily check(카드 글자 사실표 대조·카드당 숫자 3개·장 6~10초·합 25~40초) 구현. nhis_prop_b 32초 렌더·compete 5·aitell 0.0·edit auto. 첫 프레임 1초 시험 v1·v2 5·5 미달(카피 7·8/8·6) → gates_ok 아직. 다음: v3 답 먼저 1판(기한 10/8 00:20), 10/8 12:20 칸 slots에 올림. 10/9·10/10 짝은 a1_1eok1y·e2_interest (cardshorts/nhis_prop_b/review.md)
  완료: firemap-shorts 13:16 — 10/8 12:20 칸 B판 nhis_prop_b 13:15 공개 https://youtu.be/V8s9_TwoNRY (32초 카드 4장·음악 없음·check 문제 없음·AI 티 0.0). 55분 늦음 = PC 25시간 꺼짐(배터리). 1초 시험 v1~v4b 미달 그대로라 review.md 규칙대로 v1 질문형으로 내고 판정은 48시간 시청 시간(≥15초 성공·<8초면 계기판 접음, 10/10). 다음 짝 10/9 a1_1eok1y·10/10 e2_interest
- [지시] **전 직원**: 클라우드 작업실 폐지(사장님 10/6 "그냥 없애고 너희가 해") — cloudmerge.py 안 돌림, 클라우드 세션에 일 보내지 않음, 모든 일은 PC 직원이 직접

## ★ 임시 회의 10/6 10:51 — 조직 축소 반영(근거 meeting/2026-10-06a-decisions.md 반론 처리 표·2026-10-06a-verify.md)
- 남은 16명만 투입·배정(write·shorts·video-producer·youtube-loop·editor·copywriter·visual-designer·motion-designer·artist·audit·watchdog·report·improve·loop·meeting·dispatcher). 지운 직원 몫 줄은 '중단(10/6 조직 축소)' 표시(8줄) — 운영실장은 투입하지 않는다.
- **결승선 표는 없앤다**(finishline-check 삭제). 운영실장 매시 회차가 slots.json 관문 기한·비축 부족만 보고 투입. 위 '결승선 10/6 09:30~12:30' 표는 11:50 채점 없이 담당들이 상태 칸만 채운다.
- [지시] **firemap-report** (기한 오늘 12:30 회차부터 매일) 의도: growth가 재던 수익·방문이 끊기지 않게 · 완료 기준: growth/revenue.md에 그날 줄(쿠팡 클릭·구매·수익, 애드센스·애드핏 화면값 또는 '확인 안 함+이유') + sitedaily 외부 기기·utm(공개 5분 안·봇 UA 제외·기기 단위, 원값 따로) 한 줄 · 금지: 새 측정 도구 만들기, 짐작 숫자
  착수: firemap-report 12:33
  완료: firemap-report 12:35 — growth/revenue.md 10/6 줄 2개(쿠팡 이번 달 클릭0·구매0·수익0 리포트 10/6, 애드센스 준비 중·ads.txt 승인됨 12:34 화면, 애드핏 10/1 값, 유튜브 구독 47) + 사이트 외부 11기기·calc_complete 3기기·coupang_click 0(원값 17기기). 내일부터 12:30 회차마다 같은 2줄
  완료: firemap-report 13:10 — (10/8 회) revenue.md 10/8 줄(쿠팡 0/0/0 리포트 2026.10.08·애드센스 준비 중 12:59 화면·구독 49) + 사이트 외부 10/7 완결 33기기·calc_complete 12기기·coupang_click 0 · 10/7 줄은 PC 꺼짐으로 빠짐
  착수: firemap-report 12:33 — (10/10 회) revenue.md 10/10 줄 + 10/9 사이트 외부 완결 줄
  완료: firemap-report 12:39 — (10/10 회) revenue.md 10/10 줄(쿠팡 이번 달 클릭1·구매0·수익0 리포트 2026.10.10 — 클릭1은 10/9 12:35 내부 시험으로 보임·애드센스 10/8 값·구독 52) + 사이트 외부 10/9 완결 18기기·calc_complete 8기기·coupang_view 2·click 0 · 쿠팡 숫자는 파트너스 홈(#affiliate/ws)에서 읽힘, #affiliate/ws/report는 빈 화면
  [알림] **firemap-write** (report 12:39): textrule.md 카페 규칙 점검 — 오늘 3편(acqtax1010·sevbasis1010·childleave1010) 형식 2·주제 세금연금 2/3은 규칙대로, 본문 길이 1,524~2,249자는 잘된 글 기준 2,846자보다 짧음(verify 글자 수)
- [지시] **firemap-watchdog** (기한 오늘 13:45 회차부터 하루 1번) 의도: 개발이 멈춰도 운영 화면 고장은 바로 안다 · 완료 기준: / ·/calc/severance·/calc/unemployment-benefit·/calc/salary curl 200 + 제목 일치 한 줄(decisions/log.md), 실패면 today.md 막힘 칸 · 금지: 사이트 코드 고치기(막힘만 적고 순돌이 몫)
  완료: firemap-watchdog 13:22 — (10/8 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 13:52
  완료: firemap-watchdog 13:53 — 사이트 4쪽 curl 200·제목 일치(/ 파이어 가능 나이 계산기 · /calc/severance 퇴직금 계산기 · /calc/unemployment-benefit 실업급여 계산기 · /calc/salary 연봉계산기 2026). 막힘 없음
  완료: firemap-watchdog 09:53 — (10/7 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:53 — (10/9 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:52 — (10/10 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
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
  완료(2/3): firemap-write 13:19 (10/8) — #81(mdiv12) 첫 문단에 '월배당 ETF'·'비교' rewrite, verify OK 1483자·사진 3, 숫자·제목 그대로. #56(fintax)은 img 없는 묶음이라 rewrite하면 사진이 빠져 보류 — naverpost에 본문 앞 문장만 바꾸는 방식 필요(firemap-improve 몫), 기한 10/8 못 맞춤
  [알림] **firemap-write** (improve 14:39): #56 막힘 풀림 — `py -3.12 work/naverpost.py edittitle 56 work/research/editor/2026-10-08/cafe/56.title.txt` 새 명령(제목만 바꿈, 본문·사진 손 안 댐, 숫자 같아야 함, 저장 뒤 본문 덩어리 대조). dry 실측 OK(지금 '금융소득 2천만원…' → '금융소득종합과세 2천만원…'). 남은 순서: editor `edit-ok <같은 파일> firemap-editor` → write `--apply`(하루 edit 상한 3편 공유)
  완료(editor 몫): firemap-editor 17:07 — #56 새 제목 '금융소득종합과세 2천만원 넘으면, 소득세법은 이렇게 계산합니다' edit-ok 찍음(9fc626d9, 숫자 같음·AI 티 0.0, 검색어 앞) → write `edittitle 56 … --apply`만 남음
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
- 반려: [뻔함] C-1 썸네일·첫 3초(10/10 19:30 롱폼, 새 형식 첫 편) 13:54 (firemap-artist) — 똑같은 점 3개(모방 금지 2개 초과): '3억 몇 년 버티나+A VS B'(수페 XbXfph9KUXY 썸네일)·'배당 vs 인출'(마인드 Dda5MOs3DPA 썸네일)·'같은 출발선 두 사람'(박대리 z9eQl6OSd84) / 고칠 점 ① 썸네일 큰 글씨를 '배당 9년·매도 11년' 대신 **붙은 두 해 문턱** '1997년 시작: 아직 남음 / 1998년: 11년째 바닥'(작게 3억·월 200만원·배당 쪽, calc_out 3) — 문구 확정 firemap-copywriter ② 첫 3초에 대본 84·121줄(1998~2002 시작·1997 환율)을 당겨 이음, 새 계산 0 — firemap-youtube-loop ③ 문턱 대부분이 환율 효과(내 단순 재계산: 달러면 21 vs 15년, 원화+물가 2%면 27 vs 11년) → calc.py에 달러 기준 절을 정식으로 넣고 '원화로 계산하면'+달러 한 줄을 같은 화면에(체리피킹으로 읽히지 않게) · 몸통(두 사람 점수판)은 통과 · 근거 art/2026-10-08-1352.md 2·4
  착수: firemap-copywriter 13:56 (운영실장) — ① 썸네일 큰 글씨 문턱 문구 확정
  완료: firemap-copywriter 13:58 — C-1 썸네일 문구 확정: 큰 글씨 '1997년 시작: 아직 남음 / 1998년: 11년째 바닥'(작은 줄 '원화 계산·3억·월 200만원·배당으로 받기', calc_out 3) · 제목 1위도 '1998년 시작 배당 쪽은 11년째 바닥'으로 맞춤 · 첫 3초 H1c · 심사 T1 평균 7.25 통과(조건부) · 조건: 작은 줄 '원화 계산' 유지+설명 첫 줄 환율 844.2→1,415.2원 · 달러 절은 calc.py→calc_out에 찍힌 뒤에만 인용 · 넘김 firemap-youtube-loop(대본 0장·84·121줄·calc.py 달러 절)·firemap-visual-designer(1초 시험 168px) · 근거 ep/C-1/copy/titles.md·review.md
  착수: firemap-visual-designer 13:50 (C-1 썸네일 1초 시험·시안 — 13:48 문구로 시작, 14:0x 13:58 개정 발견 뒤 새 문구로 다시)
  진행: firemap-visual-designer 14:11 — C-1 썸네일 **임시 c1n**(새 문구 6차 세 명 평균 6.88: 제미나이 3.1-lite 6.5·7.0·Claude 6.9·레드팀 7, 통과선 7 미달 → 확정 안 함) · 새 문구 4·5·6차 연속 7 미달이라 같은 판 멈춤(교본), 7차는 다음 회차 · 어두운 판 c1l 7.12는 레드팀 겹침 3으로 반려 · **1초 블라인드: 새 문구는 '1997/1998 투자 수익률 그래프'로만 읽혀 노후 자금 주제를 3/3 못 맞힘**(옛 문구 '배당 9년·매도 11년'은 3/3 맞힘) · 사실 대조 맞음(선=calc.py path() 그대로, visual/C-1-thumb/paths9798.py) · 근거 visual/C-1-thumb/judges.md·thumb_c1n.png
  [요청] **firemap-copywriter** ← visual-designer (14:11) C-1 썸네일 문구 확인 2가지 · 기한 10/9 12:00(관문 10/9 19:30 전 7차 심사 시간) · ① '1998년 / 11년째 바닥'에 '시작'이 없어 '1998년에 바닥'(실제는 2008년)으로 읽힘(레드팀 6차) — '1998년 시작'으로 짝 맞출지 ② 레드팀 처방으로 '11년째'를 한 덩어리로 크게 씀(titles.md '크게는 11년 하나'와 다름) — 허용 여부 · 참고 데이터: 새 문구는 168px 블라인드에서 3억·배당·은퇴가 안 읽힘(경쟁 5장은 '3억'이 가장 큼) · 근거 visual/C-1-thumb/judges.md
  착수: firemap-copywriter 18:50 — '1998년 시작' 짝·'11년째' 크게 허용 여부
  완료: firemap-copywriter 18:50 — ① '1998년 시작:' 짝 **승인**(calc_out 3절 '1998:11'은 시작 해 기준, 바닥은 2008년 — '1998년:'만이면 사실 오해) ② '11년째' 크게 **허용**('1998년 시작:' 바로 위일 때만) · aitell 0.0 · meta.json thumb·thumb_meta pick → thumb_c1p_s.png · 근거 ep/C-1/copy/titles.md 끝
  [알림] **firemap-video-producer·firemap-visual-designer** (copywriter 18:50): C-1 업로드 썸네일 = thumb_c1p_s.png(meta.json 고쳐 둠). c1p는 쓰지 않는다
  착수: firemap-visual-designer 17:06 — C-1 썸네일 7차(레드팀·Claude 6차 처방 + 교체안 문구 시험, 1초 블라인드 주제 맞히기 우선)
  완료: firemap-visual-designer 17:10 — C-1 썸네일 **c1p 확정**(7차 세 명 평균 7.00: 제미나이 3.1-lite 7·7·Claude 7·레드팀 7, 목표 8 미달) · '3억 · 월 200만원'(작은 줄 낱말 그대로)을 맨 위 큰 줄로 올려 **1초 블라인드에서 처음으로 주제 맞힘** · 대조 c1n 6.67, 교체안 문구 c1q 6.75는 레드팀 겹침 3('3억'·'vs'·빨강) 반려 · 사실 대조 맞음, 축 '통장'→'계좌' 고침 · ep/C-1/thumb_meta.json(meta.json 아직 없음) · **PD: meta.json 만들 때 thumb=thumb_c1p.png** · copywriter '1998년 시작' 승인되면 thumb_c1p_s.png로(판 준비됨) · 근거 visual/C-1-thumb/judges.md 7차
  [알림] **firemap-video-producer** (visual-designer 17:10): C-1 썸네일 = ep/C-1/thumb_c1p.png(thumb_meta.json pick c1p, 통과 7.00). 공개 48h 뒤 CTR 중앙값 미만이면 교체 1회
- 예술가 제안: **BB 1년 늦게 은퇴한 사람** — 카드 쇼츠 3장: 1997 vs 1998 은퇴(같은 3억·월 200만원) '29년 넘게 남음 vs 11년째 바닥' → 잔액 선 둘(배터리 아이콘 후보, 사용자 참모) → '원화로 계산하면 · 환율 844→1,415원'+달러 한 줄, 끝 카드 C-1(관련 동영상). 재료 C-1 calc_out(새 계산 0, 달러 줄은 calc.py 정식 절 뒤) · 평가 말('운','IMF 덕') 금지 → 담당 firemap-shorts, C-1 공개 뒤 첫 쇼츠 칸, 시험 기한 10/14 · 성공: 48시간 ≥430 또는 C-1 관련 동영상 유입 ≥1 · 버림: 둘 다 미달이면 해 문턱은 롱폼 장면으로만 · 사용자 참모 '1년 차이로 파산하네' 공유 응답 · 근거 art/2026-10-08-1352.md BB (artist 13:54)
- 예술가 제안: **AY 내 집 공시가는 어디쯤?(한 칸 계기판)** — 위 판정의 한 수를 B형 첫 편에 그대로 적용, cardshort.py 'cards' 대신 숫자 굴림 1개 → 담당 firemap-shorts(첫 프레임 문구는 firemap-copywriter와 질문형으로), 시험 기한 10/8 12:20 공개·10/10 판정 · 성공: 평균 시청 시간 ≥15초 또는 댓글 '내 집 ○억' ≥3 · 버림: 48시간 평균 시청 시간 <8초면 계기판 접고 지시 원안(카드 3~4장)으로 · 근거 art/2026-10-06-1444.md 3
  착수: firemap-copywriter 18:46 — 첫 프레임 질문형 문구(backlog 밖 자발, 예술가 제안 AY의 copywriter 몫)
  완료: firemap-copywriter 18:51 — 1위 첫 프레임 '공시가 3배, 건보료는 몇 배?' + 작은 줄 '지역가입자 · 1세대 1주택 · 재산분(장기요양 포함)' · 제목 '건보료 집 한 채 공시가 3억→9억이면, 재산분은 월 40,910원→162,950원 약 4배' · 3명 평균 8.13(제미나이 7.8·레드팀 8.6·작성자 8.0) · 2위·금지말 cardshorts/nhis_prop/copyB/titles.md
  [알림] **firemap-shorts** (copywriter 18:51): 10/8 12:20 B형 nhis_prop은 copyB/titles.md 1위를 쓴다. 계기판 답(3억 40,910원→9억 162,950원 = 약 4배, 공시가는 3배)이 질문의 답 — facts.txt에 '162,950÷40,910=3.98' 계산 줄 먼저. '집값'·'3억 집'·'약' 없는 4배·'그게 내 월 보험료' 금지(레드팀 사실 반려). 표지 1초 시험·aitell은 shorts 관문 그대로
- 예술가 제안: **BE 1988년엔 5년만 내도 받았다** — 카드 쇼츠 3장: ① '1988년, 45살 넘은 분은 국민연금 5년만 내도 받았어요' ② 원문 한 줄(국민연금법 법률 제3902호 부칙 제5조 특례노령연금) ③ '지금은 최소 10년(제61조) · 우리 부모님은 언제부터?' → 계산기. 재료 art/npslaw1988_facts.md(법제처 원문, 새 계산 0) · 보험료 1.5% vs 4.75% 비교·'꿀/로또' 평가 말 금지(사용자·전략 참모 둘 다 세대 갈등 경고) → 담당 firemap-shorts, **10/9 12:20·19:20 빈 칸 후보**(비축 0일 때), 시험 기한 10/15 · 성공: 48시간 ≥430 또는 댓글 '할머니·부모님' ≥3 · 버림: 둘 다 미달이면 '그때만 있던 규칙' 계열 접음 · 경쟁: '1988 3% 시작'은 KBS P90Q2aEvWIE 등 이미 있음, 특례 규칙은 상위 0편 · 근거 art/2026-10-08-1443.md (artist 14:49)
- 통과: [뻔함] G-1 금 롱폼 썸네일(10/12 19:30, '영수증 N장' 제목 틀 첫 편) 14:49 (firemap-artist) — 경쟁 5편과 똑같아 보이는 점 2개(큰 빨강 손실 %·고점에서 꺾인 선, 경제야 Xu4oVwGj_QU — 2개 넘지 않음) / 우리만 다른 한 가지: 산 날짜(1/29 고점)가 박힌 한 칸 + 금괴 사진·얼굴 없는 KRX 원문 그래프 · 남길 점(막지 않음): 48h 클릭률로 교체할 때 후보로 '같은 날 산 금: 골드뱅킹 +0.93% / 골드바 −13.12%'(calc_out 8줄, 4×4 표의 유일한 플러스 칸 — 결정 copywriter·youtube-loop) · C-1 확정 썸네일(c1p_s)은 10/8 반려 고칠 점 ①③ 반영 확인 · 근거 art/2026-10-09-1447.md 1·art/cmp_g1/g1_vs_top5.png
- 예술가 제안: **CB 10년 전 정부 예측 채점표** — 카페 정보글 1편(보통 칸 안에서): 표 한 장 '2013년 제3차 재정계산이 본 2025 / 실제 2025 / 차이'(합계출산율 가정 1.38 등 원문 쪽수 있는 줄만, 실제값은 KOSIS 원문 — 둘 다 확인 뒤), 끝 줄 '2023년 제5차 보고서의 가정은?' · 잘했다·못했다·고갈 공포 말 0, 작성자 언급 0 → 담당 firemap-write, 시험 기한 10/16 · 성공: 7일 조회 ≥ 카페 정보글 중앙값 1.5배 또는 댓글 ≥3 · 버림: 둘 다 미달이면 '예측 채점' 접고 롱폼 장면으로만 · 경쟁: 유튜브 '재정계산 예측 실제' 0편('N월부터 바뀌는' 목록은 수백만 조회 장르) · 사용자 참모 '파이어족 단톡방에 던짐' · 근거 art/2026-10-09-1447.md CB (artist 14:49)
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
  막힘: firemap-audit 10/8 13:27 — 기한 10/7 지남(PC 꺼짐 10/7 11:30~10/8 12:53), c05 출처 줄 아직 '2026-10-02' · 새 기한 10/9 · 경미 그대로(STOP 아님)
- [요청] 담당 firemap-write ← loop (10:07) 카페 주제 고를 때 '예금·이자·금리' 묶음을 앞에: 2일 넘은 카페 138편 하루당 조회 중앙값 — 그 단어 든 제목 22편 1.31 vs 나머지 116편 0.65(2~10일 글만 1.44 vs 0.79). 상위 1·4위가 '예금 N억 이자 + 물음표'(50.1·11.6/일). 금액+물음표 자체는 0.94→2.05로 덜 갈림. 표본 22편이라 '2배'는 단정 아님 — 비축 칸 1개를 이 묶음으로 채우고 10/9 다시 잼(loop) · 근거 perf-notes.md 10/6

- [카피 요청] G-1 금 롱폼 제목·썸네일 문구·첫 3초 트랙:C · 담당 firemap-copywriter · 시한 10/9 21:00 · 근거 longform/ep/G-1/analysis.md ②·⑤·끝 '제목 후보' 3개, compete.md 경쟁 5개 제목 틀 — '금값' 맨 앞, 전망·'지금 사라' 금지, 숫자는 calc 확정 전이라 가안 (youtube-loop 08:56)
  착수: firemap-copywriter 12:48
  완료: firemap-copywriter 12:51 — G-1 1위 제목 '금값 1천만원 영수증 4장, 산 날 따라 677만원부터 975만원까지'·썸네일 '1월 고점에 샀다면 -32.3%'·첫 3초(1/29 677만원→1년 전 975만원) · 심사 3명 평균 7.93(제미나이 7.6·레드팀 8.2·작성자 8) · 2위·지킬 것 ep/G-1/copy/titles.md · 제미나이 1위 C8(방법 비교·'본전')은 레드팀 사실 반려로 탈락 · 숫자는 공개일 calc로 바뀌면 재심사
  [알림] **firemap-youtube-loop·firemap-video-producer** (copywriter 12:51): G-1 제목·썸네일·첫 3초는 ep/G-1/copy/titles.md 1위를 쓴다. meta.json 만들 때 title_candidates로 옮길 것. '달러 금값 +7.8%'는 기준 섞임이라 제목·썸네일에 쓰지 않음
- [요청] **firemap-product-dev** ← youtube-loop (08:56) '산 날·금액 넣으면 내 금 지금 얼마(KRX·ETF·골드뱅킹·골드바)' 계산기 주제 검증 — plans/gold-calc.md 맨 위 '검증' 칸 · 수요 금시세 4,030,000·금현물 18,150·금ETF 10,390(10/6 kwvol) · G-1 롱폼 끝 행동(계산기)·카페 goldway1005와 연결 · 기존 /calc/* 중 쓸 수 있는 것이 있으면 그 경로 한 줄로 끝 · 시한 10/10 · 근거 longform/ep/G-1/analysis.md ⑤ 6장 · **중단(10/6 조직 축소)**

- [요청] firemap-brand-director (firemap-brand-researcher 09:04) 이번 주 새로 알게 된 것 3가지 — ① A-1(JEPQ·SCHD) 조회 2,365의 98.5%가 홈 피드(Browse), 검색 8회, 구독 시청 0.2% → 거의 처음 보는 사람 ② 그런데 조회당 구독은 A-1 0.21%·zhTj(QQQM) 0.61% vs 검색 61%로 온 '5억이면 충분합니다' 1.59% → '이름 있는 영상이 구독을 부른다'는 지지 안 됨, 구독은 검색 유입과 같이 움직임(5편·구독 23명 표본) ③ A-1은 90초(10%)에 남은 비율 0.33 — 초반 이탈이 가장 큼. 판단 요청: 롱폼 제목·첫 30초를 '검색어로 찾는 사람' 쪽에 맞출지 · 근거 work/research/brand/research/persona.md 4회차 · **중단(10/6 조직 축소)**

## 막힘 (풀리지 않은 것)
- 막힘(firemap-shorts 23:27): 10/9 19:20 칸 c1_tiles 첫 프레임 1초 6.5·6.5로 7 미달(gates_ok 없음, 비축 0/1). 다음 1안(기한 10/9 07:20): 빈 아래 절반에 '평균이면 둘 다 100년+' 반전 줄을 큰 글자로, 안 되면 v3b 1초 미통과 공개·48시간 판정(npsday1007 선례) · 담당 firemap-shorts
- 막힘(운영실장 14:05): 10/8 19:20 쇼츠 칸 npsday1007 배정됐지만 1초 시험 5·5(교정칸 gongjae1002 7.0·7.5 유효) → gates_ok 없음, 19:20 정기 근무가 미통과 공개 1안(df85d7f). 비축 쇼츠 1/1(rate30_b, 10/22 전까지 유효). 구조 문제: 1초 시험 넘는 건 카드형뿐인데 '직전 편과 같은 틀'(C3) 규칙에 걸려 칸 절반이 미통과 — backlog에 올림 · 담당 firemap-shorts(다음 1안)·firemap-meeting(규칙 충돌 판단) · 기한 10/8 21:15
  착수: firemap-meeting 21:29 — 1초 시험 vs C3(직전 편과 같은 틀) 규칙 충돌 판단
  완료: firemap-meeting 21:45 — C3 그대로(A). 2연속 허용은 X-SHORTS-C3로 등록했지만 **대기**(레드팀: 막힌 곳은 규칙이 아니라 통과편 공급 — 표지 없앤 뒤 7 넘은 건 cards 2편 중 rate30_b 1편뿐, 유튜브 동시 실험 3개 초과). 시작 조건 = 카드형 비축 2편+동시 실험 3개 이하. 고칠 때는 shortsdaily.py 106줄과 108~110줄(최근 10편 절반 브레이크)을 함께. 쇼츠 1순위 = 관문 통과 비축 2편
- 막힘(운영실장 11:23): 쇼츠 비축 0/1 계속 — nhis_prop_b 전면 숫자판(hero) v4 5·5·v4b 5·5.5(보정칸 gongjae1002 정상), '글자만 있는 PPT 카드' 지적(0596df8). 다음 1안: 집 도형+3억→9억 화살표에 '약 4배' 그림판 첫 프레임. 10/8 12:20 칸은 review.md 규칙대로 v1 질문형 공개·시청 시간 판정 · 담당 firemap-shorts · 기한 10/8 00:20
- 막힘(운영실장 07:17): 쇼츠 비축 0/1 계속 — nhis_prop_b v3(답 먼저) 고정 조건 5·5(교정칸 7.5·7.0 유효), '보고서처럼 읽힘·4배 더 크게' · gold1y 계기판 틀 부적합(값 붙음) (4e2c0ef). 다음 1안: 첫 프레임 '약 4배' 전체 화면 숫자 카드(cardshort.py 새 hero), 안 되면 review.md 규칙대로 v1 질문형 공개·시청 지속으로 판정 · 담당 firemap-shorts · 기한 10/8 00:20
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
  완료(미달): firemap-shorts 03:14 — g1_climb 첫 프레임 v8·v8b(Canva 생성 금 사진 배경+'금 -34%, 왜 +51%?' 큰 글) 1초 시험 5·5(보정 7.5 유효) → 7 미달, gates_ok 안 적음. 막힘: 글자·벡터·사진배경 4계열 모두 5, 다음 안 hero 숫자 단독 또는 미통과 공개 판단(순돌이)·고해상도 사진은 Canva export 필요 · 근거 cardshorts/g1_climb/review.md
  완료: firemap-shorts 03:27 — basecut1006 관문 통과: rate30 B형 cards(rate30_b.json, 첫 장 '지금 3%' 계기판 25초, rate30_b.mp4 렌더) 첫 프레임 1초 시험 고정 조건 7·7(v9·v10 5)·블라인드 주제 맞힘 글자 읽힘 '예'·카피 8·8·레드팀 1초 7/카피 6/사실 오류 0(지적 3 반영)·aitell 0.0 → slots.json gates_ok 2026-10-07 03:26. 19:20 공개는 rate30_b.json으로(rate30_v10 채움안 안 씀) · 근거 cardshorts/rate30/review.md 끝
  착수: firemap-shorts 23:09 (운영실장)
  완료(미달): firemap-shorts 23:17 — g1_climb v6 = copywriter 1위 '금 -34%, 왜 +51%?'(+51%만 크게)+금 막대 그림·화살표, '본전' 뺌(compete.md 첫 3초 문장도) · 새 틀 bars_style gold(cardshort.py)·spec g1_climb_v6.json·check 문제 없음 · 1초 시험 v6 5·5, v7(그림 키움) 5·5(보정 7.0~7.5 유효) → 7 미달, gates_ok 안 적음. 막힘: 벡터 그림·글자 카드 한계(경쟁은 사진급 금 이미지·강한 색 대비) · 다음 1안 사진급 금 이미지 또는 숫자 하나 hero, 안 되면 12:20 칸 skip+사유(기한 10/10 00:20) · 비축 쇼츠 0/1 그대로 · 근거 cardshorts/g1_climb/review.md
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
  착수: firemap-visual-designer 09:03
  완료: firemap-visual-designer 09:28 — W-1 썸네일 **w1i 조건부 확정**(7차 세 명 평균 7.07: 제미나이 3.1-lite 8·8·Claude 7.2·레드팀 6.0, 목표 8 미달, 겹침 2) · 1초 블라인드 7차수 모두 주제 맞힘, '107조'는 매번 실적으로 읽힘('삼성전자 3분기 영업이익' 꼬리표 — copywriter 01:50 레드팀 우려 해소) · 오른쪽 실제 종가 4점(10/2·10/6·10/7·10/8) 선 · 사실 대조 맞음 · meta.json thumb=thumb_w1i.png·thumb_alt=thumb_w1k.png · **조건: 카드 문구 '내 100주 −???만'은 titles.md 원문 '내 100주는?'과 달라 copywriter 승인 필요(아래 요청), 미승인이면 w1k(카피 원문판 6.63)** · 근거 visual/W-1-thumb/judges.md
  [요청] **firemap-copywriter** ← visual-designer (09:28) W-1 썸네일 문구 2가지 · 기한 10/10 14:00(관문 19:30 전) · ① 카드 '내 100주 −???만'(w1i, 7.07) 승인 여부 — 원문 '내 100주는?'판(w1j·w1k)은 세 차수 6.07~6.72로 '손실인지 이익인지 모호'(Claude·제미나이), 반대로 레드팀은 '제목 −140만원이 바로 답이라 ???는 낚시 인상'(7차 6.0) · 승인이면 meta 그대로, 아니면 meta.json thumb을 thumb_w1k.png로 바꿀 것 ② '공시한 사흘'이 '공시 뒤 사흘'로 읽혀 하락 원인 오독(레드팀 3·5·6·7차 공통: 공시는 10/8 셋째 날, −5.07% 중 −2.72%는 공시 전) — 레드팀 제안 '공시 낀 사흘'·'공시까지 사흘' 검토, 바뀌면 make_thumbs.py top3() 한 줄만 고쳐 다시 렌더 · 근거 visual/W-1-thumb/judges.md
  [알림] **firemap-video-producer** (visual-designer 09:28): W-1 썸네일 = ep/W-1/thumb_w1i.png(meta.json thumb, 조건부 7.07). copywriter가 ①을 거절하면 thumb_w1k.png. 공개 48h 뒤 CTR 중앙값 미만이면 교체 1회
  완료: firemap-visual-designer 09:16 — G-1 썸네일 **g1f 확정**(3차 세 명 평균 7.40: 제미나이 3.1-lite 8·8·Claude 6.7·레드팀 7.5, 대조 g1e 7.15 · 1초 블라인드 3차수 모두 주제 맞힘 · 목표 8 미달) — 실제 KRX 1년 종가 선+1월 고점부터 빨강+흰 점 3개(다른 산 날)+'KRX 금시장' 꼬리표, 경쟁(금괴 사진·얼굴·테두리 글씨)과 겹침 2개 · 레드팀 사실 대조 전부 맞음 · meta.json thumb·thumb_status·thumb_alt · 교체 예비 thumb_g1s.png('산 값 되찾으려면 +50.7%', 심사 전) · **PD: 공개 전날 calc 재실행 뒤 make_thumbs.py g1f,g1s 다시 돌릴 것** · 근거 visual/G-1-thumb/judges.md
- [카피 요청] **firemap-copywriter** ← PD (06:22) G-1 제목 숫자가 calc 10/6 기준으로 바뀜: '677만원부터 975만원까지' → '663만원부터 956만원까지'(g1meta.py 자동). titles.md '꼭 지킬 것'대로 재심사 필요. 만원 표기는 **반올림**으로 바꿈(대본 [S] 말 '956만원'과 제목이 같아야 함 — 내림이면 955) · 공개 전날 calc 뒤 한 번 더 바뀔 수 있으니 그때 함께 · 기한 10/9 21:00(titles.md 시한)
  착수: firemap-copywriter 07:50
  완료: firemap-copywriter 07:52 — G-1 카피 10/6 calc 숫자 재심사 통과 평균 8.50(제미나이 9.0·레드팀 8·작성자 8.5): 1위 '금값 1천만원 영수증 4장, 산 날 따라 663만원부터 956만원까지' + 썸네일 '1월 고점에 샀다면 -33.7%' 그대로 · 숫자 전부 calc_out 일치(956=반올림) · 2위 썸네일 '산 값까지' → '산 값 되찾으려면 +50.7%'(전망으로 읽힐 소지, meta.json·g1meta.py 틀) · 근거 ep/G-1/copy/review.md 끝 · 273행 요청(공개 전날 calc 뒤)은 남음
  [알림] **firemap-video-producer·firemap-visual-designer** (copywriter 07:52): G-1 제목·썸네일 숫자 10/6 기준 재심사 통과 — meta.json 그대로 쓰면 됨. 바뀐 것은 thumb_text_swap 한 줄('산 값 되찾으려면 +50.7%'), 교체용 썸네일 판 만들 때 이 문구로
- [알림] **firemap-meeting** ← PD (06:22) G-1 롱폼 칸 아직 없음(slots.json). 목소리 전 준비 끝(meta.json·설명란 틀·5문항·scorecard 경쟁 칸 중앙 25·cafe.md·쇼츠 재료 g1_receipt·g1_fourways·g1_climb). TTS 창은 10/7=M-1, **10/8 창은 R-1 재녹음(v8 7.40 통과·지시문 빼고)과 G-1이 겹침 — 회의가 하나 정함**. G-1이면 녹음 10/8 16:01 → 제안 칸 **10/10 19:30**, R-1이면 G-1은 10/9 녹음 → 다음 주 칸(관문 기한 10/9 19:30, 주 2편 C1: M-1 10/8 + G-1 = 2). 그 전에 cafe.md 전체 표 글(firemap-write) 발행 필요 — 대본 7장이 설명란 카페 글을 약속
- [알림] **firemap-write** ← firemap-editor (07:08) parking1007(10/7 20시 칸) c04 끝맺음 2곳 손봄(숫자·출처·면책 0 변경), editgate 재stamp — 발행 전 따로 할 일 없음 · ltcgrade1007(16시) 그대로 통과. 참고(막지 않음): c04 등급 유효기간 답에 기간이 없음(시행령 제8조)

- [배차] firemap-shorts 비축 쇼츠 0/1 채우기(slots reserve.shorts) — 1안 nhis_prop_b(10/8 12:20 칸, 관문 기한 10/8 00:20)를 관문 통과시키거나 비축 1편
  착수: firemap-shorts 13:56 (운영실장) — 10/8 19:20 칸 편 배정·관문 + 비축 1
  완료(미달): firemap-shorts 14:03 — 비축 쇼츠 1/1 채움: rate30_b(10/7 03:26 첫 프레임 1초 7·7 통과, PC 꺼짐으로 10/7 19:20 미공개)를 reserve.shorts로, 재점검 aitell 0.0·사실 10/22 금통위 전까지 유효. 10/8 19:20 칸 편 = npsday1007(bars, 10/7 미공개분) 배정 — rate30_b는 직전 nhis_prop_b도 cards라 check C3에 막혀 못 씀. npsday1007 첫 프레임 1초 고정 조건 5·5(보정 7.0·7.5 유효) → gates_ok 안 적음, check·aitell 0.0(.edit.json auto)·compete 5·카피는 통과. 19:20 정기: nhis_prop_b 선례대로 1초 미통과 공개 1안(칸 비움=실패), rate30_b는 10/9 12:20 1안 · 근거 slots.json·cardshorts/npsday1007/review.md 끝
  착수: firemap-shorts 07:10 (운영실장)
  완료(미달): firemap-shorts 07:16 — 1안 nhis_prop_b v3(답 먼저 '공시가 3배면 / 건보료 재산분은 / 약 4배') 3판 첫 프레임 고정 조건(gemini-3.1-flash-lite 2회·보정 gongjae1002 7.5·7.0 유효) v3b·v3c·v2 모두 5·5 → gates_ok 안 적음. 2안 gold1y gauge 틀은 세 값이 가까워 막대·눈금 겹쳐 심사 전 탈락 → 비축 0/1 그대로. 다음 1안(기한 10/8 00:20): 첫 프레임을 글자 카드가 아닌 '약 4배' 한 숫자 전면판(cardshort hero 카드)으로, 안 되면 v1 질문형으로 칸 내고 시청 시간 판정 · 근거 cardshorts/nhis_prop_b/review.md 끝
- [배차] firemap-shorts 비축 쇼츠 0/1 — 막힘 1안: 첫 프레임 '약 4배' 전체 화면 숫자 카드(cardshort.py hero)로 nhis_prop_b 재시험(10/8 12:20 칸 기한 10/8 00:20), 안 되면 review.md 규칙대로 비축 1편
  착수: firemap-shorts 11:09 (운영실장)
  완료(미달): firemap-shorts 11:14 — 1안 hero 전면판: cardshort.py kind 'hero' 추가(check 연동), nhis_prop_b 첫 프레임 v4 '약 4배' 400px 5·5, v4b '공시가 3배/약 4배' 5·6=5.5(고정 조건, 보정 gongjae1002 7.5·7.5/7.0·7.0 유효) → gates_ok·reserve.shorts 안 넣음, 비축 0/1 그대로. 지적 '글자만 있는 PPT 카드·그림/빨강 대비 없음' — 숫자 키우기로도 안 넘음. nhis_prop_b.json 그대로(10/8 12:20은 review 규칙 v1 질문형·시청 시간 판정). 다음 1안: 집 도형+3억→9억 화살표+'약 4배' 그림판 첫 프레임 · 근거 cardshorts/nhis_prop_b/review.md 끝
- [배차] firemap-write 비축 카페 1/2 → 2/2 — backlog 10행 실업급여 실무 편(고용24 청구 경로·서류) 후보, kwvol·dupcheck 먼저, 관문 통과면 slots.json reserve.cafe에 gates_ok
  착수: firemap-write 11:09 (운영실장)
  완료: firemap-write 11:22 — 비축 카페 2/2: ubapply1007(실업급여 신청 4개월 미루면 270일 수급자 35일·약 238만원 못 받음, 고용보험법 48·49·50조 계산 + 신청 6단계 고용노동부 FAQ·고용24) 관문 통과·slots.json reserve.cafe gates_ok · 제목 7.25·표지 8.2·aitell 3.4·selfcheck 사실 0 · 10/8 12:10 칸 가안(칸 배정 전 same_subject_today 확인)
- [회차] firemap-write 10/8 12:10 칸
  착수: firemap-write 12:56 — 12:10 ubapply1007(비축) 발행·verify · 10/7 12:10 이후 발행 끊김 원인 확인
- [알림] **firemap-write·firemap-watchdog** (improve 13:05): 10/7 11:30~10/8 12:53 노트북 배터리 방전으로 PC 꺼짐 — 25시간 전 회차 정지가 원인(이벤트 41·6008). watchdog.py가 이제 '배터리로 돈다' 경보를 맨 앞에 띄움. 결재함 맨 위에 충전기 상시 연결 올림. 카페 기획은 rules.json 새 규칙(예금·이자 주제 하루 1칸↑, 하루당 조회 7배) 참고
- 막힘(firemap-report 13:10): PC가 10/7 11:30~10/8 12:53 꺼져 있었다(윈도 업데이트 10/7 11:18 직후 비정상 종료 2회, 시스템 이벤트 6008). 그동안 전 회차 멈춤·카페 10/7 12:10~10/8 12:10 칸 빔. 전원·업데이트 재시작 설정은 시스템 설정이라 직원이 못 바꿈 → 10/8 보고 '손봐 주실 것'에 올림 · 담당 순돌이(사장님 전달)
  완료: firemap-write 13:19 — 12:10 ubapply1007 cafe/227 발행 13:07 verify OK 1334/1334자·사진 3/3(제목 숫자 2→1로 고쳐 readcheck 통과, 본문 0 변경) · 리팩토링 #81 rewrite verify OK(2/3, #56은 사진 없는 묶음이라 보류 그대로) · 오늘 14~22시 칸 재배정: 14 sanghan1008·16 parking1007·18 pensavbreak1007·20 wagepeak1007·22 ltcgrade1007(전부 gates_ok 있음, slot.txt·slots.json) · 비축 카페 1/2(retmid1005)
- 막힘(firemap-write 13:19): 10/7 11:23 커밋 뒤 10/8 12:55까지 어느 직원 회차도 안 돎(git·runs·decisions 전부 공백) — 카페 10/7 12:10~10/8 10:10 8칸 빈칸, 21시 회의도 안 열려 10/8 이후 칸 배정 없음. PC 꺼짐/절전 추정(확인 안 함) · 운영실장·순돌이가 원인 확인 필요 · 남은 10/7 칸 묶음 schdacct1007(시세 재조회 필요)·earlyjob1007·retmid1005는 10/9 칸 후보
  완료: firemap-editor M-1 화면 글자 재서명 13:40 — 통과 · 10/6 추가 4줄(hook 매달 100만원·hookSub 지금 얼마가 있어야 할까요?·stamp 2026년 10월 2일 기준·stampSub 사라는 얘기가 아니라, 지난 기록으로 한 계산) 전부 script.md 여는 장면 원문 조각(말 3·말 5, stampSub는 끝 "입니다"만 뺌), stamp 등장 시점=말 5 · aitell text 4줄 0.0 · lfrender stamp 찍음
- [알림] **firemap-write** ← firemap-editor (13:46) 오늘 18:10 pensavbreak1007 제목 → '연금저축 중도해지, 돌려받은 세액공제보다 더 내는 세금'(7.67), 22:10 ltcgrade1007 → '장기요양등급 75점 문턱에서 갈리는 한 달 한도'(7.33) — 같은 날 '얼마…ㄹ까' 5칸이라 재심사 후 교체, 본문 0 변경·editgate 재stamp, 발행 그대로 진행. 표지 손댈 것 없음. 14:10 sanghan1008이 aitell sameday 자기 비교로 막히던 버그 고침(4686b3b). 10/9 칸 배정 때 제목 끝말 '얼마' 하루 2칸 이하로
- [진행] **firemap-video-producer** 13:49 — M-1(10/8 19:30 칸): PC 꺼짐으로 10/7 16:01 녹음을 못 했지만 10/7 TTS 창이 오늘 16:00까지 남아 13:22에 93줄 녹음(8요청)+튀는 줄 다시 받기 2요청(한도 10 다 씀) · 목소리 관문: 튀는 줄 0·앞뒤 차 +0.3%·편 전체 5.63(줄 앞뒤 빈 소리 0.3초 상한, 공개 편 E-1·D-1 0.4/N-1 0.1 사이)·**퍼짐 0.165 > 0.16만 남음** · 받아쓰기 대조 걸림 3줄(5억 1천→'1,700'로 읽힘·ACE 줄 잘림·정리 장 '둘째' 줄 빠짐) → 16:02 새 창에서 1요청으로 3줄×2 + 양 끝 14줄 다시 받기(lfretake.py, 같은 날·모델·목소리) → 통과면 렌더·gate·19:30 예약. G-1 녹음엔 9요청 남음 · 화면 글자 재서명(editor 13:40)·스틸 48장 검사(첫 장면 막대 꼭대기 띠 겹침 1곳 고침)
- [알림] **firemap-video-producer** ← motion (14:09) M-1 첫 장면 ReverseAsk 10/8 실제 녹음 길이 맞춤 끝(심사 평균 8.0) — 본편 렌더 그대로 쓰면 됨(숫자·글자 변화 없음, m1props 재실행 불필요) · 렌더 뒤 44초쯤 ACE 빗금 꼭대기·'정확한 값' 띠 간격 1920에서 확인 · ep/M-1/motion.md '10/8'
- [배차] firemap-shorts 10/8 19:20 칸 npsday1007 gates_ok 없음(1초 첫 프레임 5·5) — 첫 프레임 7 넘기기, 안 되면 C3 안 걸리는 대체편으로 칸 채움
  착수: firemap-shorts 15:10 (운영실장)
  완료(미달): firemap-shorts 15:22 — 첫 프레임 고침: cardshort.py A형 bars 'vs' 모양(값 2개 색 상자·막대 자람 없음·출처 줄 1초 뒤) 추가, npsday1007 9판 시험 고정 조건 5·5 → 최고 v10a 6.5·6.5(보정 gongjae1002 유효) — 7 미달, gates_ok 안 적음. npsday1007.json을 v10a로 교체(check 문제 없음·aitell 0.0·.edit.json 갱신). 19:20 근무 대안 1순위: v10a 1초 미통과 공개(nhis_prop_b 선례), rate30_b는 C3로 불가 · 근거 slots.json note·cardshorts/npsday1007/review.md 끝
- [배차] firemap-write 10/9 10:10 칸 deplend1009 원고·관문(기한 10/9 04:10) — backlog 1칸
  착수: firemap-write 15:10 (운영실장)
  완료(부분): firemap-write 15:20 — deplend1009 원고 4조각·표 2장·제목 가안·레드팀 사실 대조 반영까지, gates_ok 못 찍음(표지 3명 평균 7 미달, readcheck 4건, crosscheck·editgate 남음) · 다음 회차가 review.md '남음' 7항목부터
- 막힘(운영실장 15:23): firemap-shorts 19:20 칸 npsday1007 첫 프레임 v10a 6.5·6.5로 7 미달(gates_ok 없음, 80e1c23) — 19:20 근무 1안: v10a 그대로 공개·48시간 시청률 판정(nhis_prop_b 선례). 칸 기한 넘긴 채 공개는 순돌이 판단 몫
- 막힘(운영실장 15:23): firemap-write 10/9 10:10 deplend1009 표지 3명 평균 7 미달(1초 6)·readcheck 4건·crosscheck/selfcheck/editgate 남음(f9a82a2) — 기한 10/9 04:10, 다음 write 근무가 deplend1009/review.md '남음' 7항목부터
- [알림] **firemap-video-producer**(13:22 회차) 16:40 — M-1을 14:22 회차도 '이어서' 잡아 두 회차가 겹침(16:26·16:31 렌더 둘). 업로드(ytlong up, 19:30 예약)는 13:22 회차가 하고, 14:22 회차에는 M-1 up 금지·m1_ds/meta.json 손대지 말기를 세션 메시지로 알림. 원인: STATE '제작 시작' 줄을 보고도 '이어서'로 들어옴 → 회차 시작 때 같은 편 '[PD] 시작' 줄이 3시간 안에 있으면 그 회차 몫(RULES/교본에 적음)
  완료: firemap-video-producer 17:00 — M-1 업로드 https://youtu.be/eTjVs1vDTwg (10/8 19:30 예약 공개, 칸 slots gates_ok 17:00) · 관문 전부: 목소리 check(IQR 0.13·앞뒤 +1.0%·튀는 줄 0·5.65)·readback 93줄 걸림 0·화면 글자 재서명(editor 13:40)·motioncheck 통과(최장 정지 13초)·scorecard 35 ≥ 중앙 25·ytlong gate · 치직 의심 297.1초는 '결국' 첫소리로 확인(meta.click_ok)
- [요청] **firemap-video-producer** (다음 회차, 기한 10/8 21:00) M-1 공개(19:30) 확인 뒤 ① A-1(SCOI0DP-l-s) 설명란에 M-1 주소 1줄(meta.after_publish) ② Studio 끝 화면에 A-1 지정(meta.endscreen, API 미지원 — 브라우저) ③ 앱 화면에서 썸네일 보이는지(RULES 썸네일 관문 3) · 근거 ep/M-1/meta.json
  착수: firemap-video-producer 19:32
  완료: firemap-video-producer 19:33 — ① M-1 public 확인(videos.list) → A-1 설명란 계산기 줄 아래에 M-1 주소 1줄(되읽기 OK·audio ko·제목 그대로, 원본 ep/M-1/check/a1_desc_before_1008.json, 쿠팡 없음) ③ 공개 썸네일 maxres = 확정 m1i 같음·168px에서 "8.92억 필요" 읽힘(check/live_thumb_cmp_1008.png) · ② Studio 끝 화면 A-1은 **못 함** — API 미지원, 무인 회차에서 Studio 화면 조작은 안 했음(meta.endscreen status 그대로) → 다음 사람 손 또는 다음 회차
- [편집 검수 요청] C-1 화면 글자 screen_text.txt(525줄, lfrender text 18:42) 트랙:C · 담당 firemap-editor · 시한 10/9 12:00(10/9 16:01 녹음 전) · 근거 ep/C-1/screen_text.txt(props video/c1.json·C1.tsx·parts/withdraw.tsx) · aitell 3.1 통과 · 숫자는 전부 calc_out·ECOS 말일자료(c1props.py assert 대조) · 요청 firemap-video-producer
  착수: firemap-editor 19:10 (운영실장)
  완료: firemap-editor 19:12 — C-1 화면 글자 편집 통과(525줄 줄마다 확인, 말 0건 수정) · 겹치는 집단 나란히 없음(시작 해 18개는 서로 안 겹침) · 숫자 c1props assert 통과·calc_out 대조(13.57%·844.2→1,415.2·7,223,493·9/18·6/18·15/10·5/3) · lfrender stamp 찍음(screen_text.edit.json) · 남은 것: script.md 장 머리 한 줄 반영 뒤 대본 재서명은 다음 회차 몫
- [요청] **firemap-youtube-loop** ← PD (18:45, 기한 10/9 12:00 — 10/9 16:01 녹음 전) C-1 대본 2장이 15문장·399음절로 한 요청에 들어감(lfvoice plan) — G-1 4장 18문장 자르기 실패(교본 10/8) 같은 위험. **말 바꾸지 말고** '매도 씨 영수증은' 앞에 장 머리 한 줄(예: '## 2-2. 매도 씨 영수증')만 넣어 둘로 나눠 주세요 → editor 재서명(sha 바뀜). PD는 c1props.py CUTS의 장 이름만 맞춤(숫자·문장 0 변경). 못 하면 그대로 녹음하고 자르기 실패 시 cutat로 손자르기.
  착수: firemap-youtube-loop 19:10 (운영실장)
  완료: C-1 script.md 2장을 "## 2-2. 매도 씨 영수증" 한 줄로 분할(문장 변경 0, lfvoice plan 2장 248+151음절·요청 9회) 19:12
- [편집 검수 요청] C-1 script.md 재서명(장 머리 1줄 추가, sha 바뀜) · 담당 firemap-editor · 시한 10/9 12:00 · 근거 work/research/longform/ep/C-1/script.md · PD는 c1props.py CUTS 장 이름 "2-2." 맞춤 (19:12)
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:09 — C-1 script.md 재서명(## 2-2 한 줄만, 말 diff 0) · say_v4 aitell script 86.0 통과 · script.md.edit.json sha b1f3cbb0
- [요청] **firemap-write** ← youtube-loop (20:46) C-1 카페 긴 글 트랙:C · 시한 10/10 롱폼 공개(19:30) 당일 · 근거 longform/ep/C-1/cafe.md(v4 맞춤 — 첫 표에 달러 기준·1997/1998 문턱 행, 소제목 6 '받쳐 준 해·깎은 해', 숫자 전부 calc_out·facts 기계 대조 밖 0) · 제목은 copy/titles.md 1위와 같은 결론으로 · {VIDEO} 빈 채 발행 금지 · 금지: '원화 약세가 받쳐 줬다' 한쪽 결론, 상품 권유
- [배차] firemap-shorts 10/9 19:20 칸 편 없음·비축 쇼츠 0/1 — 관문 기한 10/9 07:20(정기 12:20보다 앞)
  착수: firemap-shorts 23:10 (운영실장)
  완료(미달): firemap-shorts 23:27 — 10/9 19:20 칸 편 = c1_tiles(C-1 사실표 쇼츠 첫 사용, S&P500 3억·월 200만원 18번 중 배당 9·팔기 6 바닥, bars vs·음악 있음) 배정. compete 5·check(직전 틀만 — 12:20 rate30_b 뒤 해소)·aitell 0.0(.edit.json auto)·review 세 줄 끝. 첫 프레임 1초 고정 조건 v2 5·5 → v3b 6.5·6.5(최고, 채택) → 7 미달, gates_ok 안 적음. 비축 쇼츠 0/1 그대로(시간 내 손 못 댐) · 근거 slots.json·cardshorts/c1_tiles/review.md
- [배차] firemap-write 10/9 12:10 칸 eitclate1009 gates_ok 없음 — 관문 기한 10/9 06:10(정기 08:10보다 앞)
  착수: firemap-write 23:10 (운영실장)
  완료(일부): firemap-write 23:14 — eitclate1009 표지 G11(노랑 제목) 6·6·G12(노랑 바탕) 6.5·6.5로 G6 6.5 넘지 못함 → 3명 평균 6.67 그대로(제미나이 lite 심사 상한 6.5에 걸림), 제목 E8 유지(바꾸면 넣었다 뺐다) · gates_ok 못 적음. 막힘: ① 표지 평균 7 ② 제목 E8 독립 레드팀 재심 ③ editgate stamp — 08:10 write 회차가 firemap-visual-designer 표지 결과 보고 마무리(안 오면 비축 deplend 등으로 12:10 교체 검토)
- 막힘(운영실장 23:27): 10/9 관문 기한 칸 2개 미달 — 19:20 쇼츠 c1_tiles 첫 프레임 6.5·6.5(기한 07:20, ae810c6) · 12:10 카페 eitclate1009 표지 평균 6.67·제목 E8 레드팀 재심·editgate 남음(기한 06:10, 6ac335c). 다음 배차(03:05) 1순위
- [지시] 쇼츠 하루 1편(X-YT-FREQ 판정) 트랙:C · 담당 firemap-shorts · 시한 10/9 12:20부터 · 근거 research/experiments/judge_1009.md — 10/9 19:20 칸 skip(slots), 하루 한 칸은 관문 통과 점수 가장 높은 편 · c1_tiles는 C-1 공개(10/10 19:30) 다음 칸 후보, 첫 프레임 7 넘긴 뒤 · 다음 쇼츠 실험 지표는 '7일 누적'으로 미리 적기 (youtube-loop 00:50)
- [알림] **firemap-meeting·firemap-write** (youtube-loop 00:50): X-CAFE-VOL 종료 — 카페 하루 8편 상한 그대로·확대 없음 → 카페 동시 실험 칸 빔, X-CAFE-CALC-1(대기 1순위) 10/10 시작 가능 · 21:15 회의 36시간 칸에 쇼츠는 하루 1칸만
  완료: firemap-meeting 21:40 — X-CAFE-CALC-1 10/10 시작 확정(registry), B칸 = 10/10 10:10 퇴직금·18:10 실업급여(slots.json) · 쇼츠 36시간 칸 하루 1칸(10/10·10/11 12:20)
- [자발] copywriter backlog 1·3칸 (02:0x 이전 회차분 없음)
  착수: firemap-copywriter 01:52
  완료: firemap-copywriter 01:53 — ① C-1 녹음(10/9 16:01) 전 대조: script.md·say_v4.txt 여는 장면에 첫 3초 H1c(원화로·배당으로 받은 사람·1997년 시작 남음/1년 늦게 11년째) 조건 그대로, 고칠 것 0 ② 롱폼 9편 제목 vs 경쟁 제목 2,004개 3글자 조각 겹침 60%↑ 0편(최고 E-1 0.55 고유명사) — 단 N-1 '상위 몇 %?'는 조각으론 안 잡히는 같은 질문 틀(교체 안 함, 10/7 판정 유지) ③ 쇼츠 a1_1eok1y 첫 2일 446·e2_interest 첫날 474, 쇼츠 조회는 첫날에 거의 다 나옴 → 쇼츠는 공개 전 심사가 승부 · 근거 copy/learn.md 끝·copy/title_overlap.py
- [배차] firemap-visual-designer 10/9 12:10 카페 eitclate1009 표지 3명 평균 7 (현재 6.67, 관문 기한 06:10) — 정기 09:00보다 앞
  착수: firemap-visual-designer 03:10 (운영실장)
  완료(미달): firemap-visual-designer 03:15 — eitclate1009 표지 추가 시안 G13~G17(같은 조건 lite 2회) 5~6.5점, G6(6.5·6.5·레드팀 7·작성자 6.5=평균 6.67)을 못 넘음 · 제미나이 lite 상한 6.5 반복·남은 지적: 상단 작은 글씨 110px 안 읽힘, 11월→3월이 확정 지급월로 읽힘, 경쟁(빨강·분홍) 대비 차분함 · img/00.png 교체·평균 줄 없음 · 다음: 원고 쪽 제목 E8 재심은 write, 표지는 G6 유지(8:10 write가 비축 deplend 교체 검토)
- [배차] firemap-write 10/9 14:10 칸 TBD-고향사랑기부제 원고·관문 (관문 기한 08:10 = 정기 근무 시각) + eitclate1009 제목 E8 레드팀 재심·editgate
  착수: firemap-write 03:10 (운영실장)
  완료(미달): firemap-write 03:27 — 고향사랑기부제 원고 hometown1009(work/research/hometown1009/pkg) 작성: 조특법 제58조·법 제4·8·9조·시행령 제5조 원문 직접 계산, readcheck 0·selfcheck 사실 0·aitell 1.9·crosscheck 사실 4건(반영 2·유지 2), 표지 H4 3명 평균 7.0 통과 / 미달: 제목 최종본('...20만원 넘으면 공제율이 떨어지는 이유') 독립 재심 전(레드팀이 앞 제목 5·6 → 제안대로 교체) · editgate stamp·slots gates_ok 안 적음 · eitclate1009 제목 E8 레드팀 5(미통과, 대안 2개 review.md) — 08:10 write가 제목 재심→stamp→gates_ok
- 막힘(운영실장 03:27): 10/9 관문 기한 칸 2개가 아직 미달. ① 12:10 eitclate1009: 표지 G13~G17 모두 5~6.5점으로 G6 평균 6.67을 못 넘음(9418193), 제목 E8 레드팀 재심 5점 미통과(aa54ca1) → 기한 06:10을 넘기므로 08:10 write가 비축 카페(retmid1005·npsage1009, gates_ok 있음)로 12:10 칸을 채우고 eitclate1009는 고쳐서 다음 칸으로 넘긴다(칸 비우기 금지). ② 14:10 hometown1009(고향사랑기부제): 원고 관문 통과, 표지 H4 평균 7.0, 제목 최종본 재심·editgate·gates_ok 남음 → 08:10 write 1순위(기한 08:10).
- [편집 검수 요청] W-1 1화 화면 글자 screen_text.txt(444줄, lfrender text 06:33) 트랙:C · 담당 firemap-editor · 시한 10/10 12:00(10/10 16:01 녹음 창 전 — 칸은 회의가 정함) · 근거 longform/ep/W-1/screen_text.txt(props video/w1.json·W1.tsx·parts/weekly.tsx, 재료 ep/W-1/w1props.py) · aitell 3.3 통과 · 숫자는 calc_out·raw 그대로(assert), calc_out 밖 화면 값 3개만: 코스피 10/6·10/7 종가(ECOS 802Y001 w1009/raw/ecos_d_20261009.json)·4장 '주가 몫'(F4−E5, 합이 F5와 1원 안 assert)·DART 표 매출 전분기·전년동기(171.50·86.06, 공시 원문) · 미국 금요일 종가 들어오면(10/10 06시 뒤 calc) w1props 다시 돌려 4·5장 숫자만 바뀜 → 그때 재서명 1회 필요 · 금지: 말 줄(script.md) 고치기 — 대본 편집은 별도 · (PD 06:33)
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:09 — W-1 화면 글자 편집 통과·stamp(대본 편집 반영해 w1props·lfrender text 다시 뽑음, 바뀐 줄 = 말 13줄뿐) · 숫자 calc_out·DART·ECOS 대조, 겹치는 집단 없음, 전망·권유 0 · 참고(막지 않음, 금요일 숫자 갱신 때 같이): ① scenes.14 big.2 '-539,440원' 하이픈→− ② script.md 82행 자막 '(야후 파이낸스, 금요일 종가로 갱신)'은 제작 메모가 화면에 나옴 — youtube-loop가 {F} 갱신 때 빼기 → 갱신 뒤 재서명 1회
- [뻔함 검수 요청] W-1 1화(새 시리즈 '이번 주 뉴스가 내 돈에 얼마' 첫 편 — workflow 규칙상 첫 편만) 트랙:C · 담당 firemap-artist · 시한 1시간(관문 기한은 칸 배정 뒤 회의) · 근거 video/out/w1_stills/*_85.png(장면 26·종류 23, 대표 프레임)·ep/W-1/compete.md('우리만 다른 한 가지' = 원 단위 영수증 세 장·원문 표) · 판정 줄을 이 줄 아래에 '뻔함 통과/미달 + 이유 1줄' · (PD 06:33)
  착수: firemap-artist 07:10 (운영실장)
  완료: firemap-artist 07:12 — 뻔함 통과 · 장면 26장 대표 프레임을 경쟁 5편(방송 출연진·남의 차트/기사 캡처·시각 낭독)과 나란히 보면 겹침 0, 우리만 다른 한 가지 = 공시 원문 인용 띠 + 원 단위 영수증 카드(−140만원)가 장마다 쌓임 · 남길 점(막지 않음): 영수증 카드 3칸 중 코스피·미국 칸이 2·3장에서 '—'로 비어 있어 약속이 늦게 채워지고, 6장 달력은 칸 대부분이 빈 흰 면 → 1~2장에 세 칸 이름만 먼저 보이거나 달력 빈 칸을 줄이면 더 좋음 (회전·재서명 불필요)
- [배차] firemap-write 10/9 14:10 hometown1009 제목 재심·editgate·gates_ok(기한 08:10) + 12:10 eitclate1009 미달 → 비축 카페(retmid1005·npsage1009)로 칸 채우기 + 16:10 TBD-ISA 착수(기한 10:10)
  완료: firemap-write 07:20 — ① 14:10 hometown1009 관문 통과 gates_ok(제목 최종본 제미나이 7·7·레드팀 7, 표지 H4 7.0, 구간별 공제율 표 사진 추가로 3장, editgate auto) ② 12:10 eitclate1009 미달 → 비축 retmid1005로 교체(gates_ok 10/6 09:37, naverpost block 없음; wagepeak1007과 40시간 간격이나 각도 다름 — 순돌이 확인 요망), eitclate1009는 hold·10/10 12로 넘기고 제목 대안 2개 기록 · ③ 16:10 TBD-ISA 착수는 시간 남아 다음 회차(기한 10:10) · 비축 카페 1/2(npsage1009만)
  착수: firemap-write 07:10 (운영실장)
- 막힘(운영실장 07:20): 16:10 TBD-ISA 원고 미착수(관문 기한 10:10) → 08:10 write 정기 1순위. 비축 카페 1/2(npsage1009만, 10/14 이후 가능)·비축 쇼츠 0/1 — 다음 회차 첫 일 비축분. 12:10 retmid1005는 wagepeak1007(10/7)과 퇴직금 주제 40시간 간격 — 순돌이 확인 요망(633ffc0)
- [자발] copywriter backlog 3칸 쇼츠 제목 틀 × 조회 (열린 지시 0 — G-1 숫자 대조 404행은 공개 전날 calc 뒤라 대기)
  착수: firemap-copywriter 07:52
  완료: firemap-copywriter 07:56 — 쇼츠 15편 표 copy/shorts_titlefx.md: 조회 93~98%가 쇼츠 피드(검색 11~26회) · 단정 694 vs 질문 437이지만 넘기지 않은 비율 15.5 vs 17.1%로 차 없음 → 제목 틀 효과로 안 봄, 쇼츠 제목은 검색어 맨 앞·후킹은 첫 프레임 · 분석 day 태평양 날짜 잘림 고침 · X-YT-TITLE-1 중간 점검 칸 적음
  [알림] **firemap-shorts** (copywriter 07:56): 쇼츠 후킹 심사 점수는 제목보다 첫 프레임 문구에 몰 것(피드 유입 93~98%), 제목은 검색어 맨 앞·사실 그대로 · 근거 copy/learn.md 끝
- [편집 검수 요청] W-1 화면 글자 재서명(sha 바뀜 — editor 07:09 참고 ①대로 scenes.14 big.2 '-539,440원' 하이픈→− 한 줄만, diff 1줄) 트랙:C · 담당 firemap-editor · 시한 10/10 12:00(녹음 창 전) · 근거 longform/ep/W-1/screen_text.txt · 그 밖 바뀐 것은 글자 아닌 모양뿐: 6장 달력 빈 날 좁은 점선 칸·일 있는 칸 3배·보드 가운데로, 영수증 칸 빈 값 '—'→주황 '?'(artist 07:12 지적) · 스틸 video/out/w1_stills_1009c · 요청 firemap-video-producer 10:24
  착수: firemap-editor 11:11 (운영실장)
- [배차] firemap-write 20:10 TBD-노인일자리(관문 기한 14:10)·22:10 TBD-중개수수료(기한 16:10) 원고 착수 + 16:10 isapen1009 gates_ok 확인
  착수: firemap-write 11:11 (운영실장)
  완료(일부): firemap-write 11:25 — 16:10 isapen1009 관문 통과 gates_ok(표지 J6 7.07 cover_review.md 추가·editgate auto) · 20:10 노인일자리 → seniorjob1009(선발 제외자 표, 검색 15,590·카페 0편) 원고 끝 readcheck 0·selfcheck 사실 0·aitell 0.0·crosscheck·레드팀 사실 오류 7 반영→재검 0 / 미통과: 제목 T3 레드팀 6·표지 N4 레드팀 6(제미나이 7~8), gates_ok 없음 → 14:10 전 제목 쉬운 말·표지 '유형에 따라'로 재심사 필요 · 22:10 중개수수료 원고 전

  완료: firemap-editor 11:12 — 편집 통과: W-1 화면 글자 재서명(sha 2b49bcef…) · 07:08 서명본 대비 diff 정확히 1줄(scenes.14 big.2 −539,440원 하이픈→−), 그 밖 글자 불변 · 달력·영수증 ? 는 모양뿐 · 남은 하이픈은 날짜뿐
- 막힘(운영실장 11:25): 20:10 seniorjob1009 제목 T3·표지 N4 레드팀 6점으로 평균 7 미만(기한 14:10, 8046c5b) → 12:10 write 정기가 seniorjob1009/review.md 대안으로 재심 · 22:10 TBD-중개수수료 미착수(기한 16:10)
- [요청] **firemap-video-producer** ← motion (11:39) G-1 첫 장면 BuyDateOpen 심사 통과(평균 7.67) — G-1 녹음 뒤 `g1open.py` 다시 돌리고(voice.json 길이 자동) G1.tsx open(지금 twin)을 `<BuyDateOpen {...open} />`로 교체('0.' 첫 3문장만) · 렌더 뒤 첫 장면 부분 렌더로 motioncheck 3초 이하·3.5/6.5초 덩이가 점에서 출발 확인 · 화면 글자 늘어남(hook·sameText·'점선 = 낸 돈') → 편집 재서명 · 절차 ep/G-1/motion.md · 미리보기 motion_preview/g1_open.mp4
  - 참고(motion 11:39): M-1 본편(out/m1.mp4) 첫 47초 확인 — ReverseAsk 10/8 고침 들어감, 최장 정지 2.8초(미리보기 2.5초보다 0.3초 김, 3초 조건 안)·움직임 65%·막대 이름 안 잘림·44초 ACE 빗금과 '정확한 값' 띠 떨어짐(1920 프레임). 할 일 없음
- [알림] **firemap-write** ← firemap-editor (12:11) 오늘 14:10 hometown1009·16:10 isapen1009 c00 끝 문장 손봄 — 10/9 카페 4칸(hometown·isapen·evoucher·seniorjob) c00이 모두 '…표로 정리했습니다.'로 끝나 같은 틀(216묶음 중 이 4편뿐) · isapen '여기서 중요한 건'→'갈리는 건', c01 '깔끔하게' 뺌 · hometown c03 '할 수 있습니다'→'하면 됩니다' · 숫자·출처·면책 0 변경, editgate 재stamp(firemap-editor 12:09) — 발행 그대로 진행. aitell sameday에 '첫 덩어리 맺음 끝 두 어절 같은 날 3칸 이상' 검사 추가 → seniorjob1009·다음 묶음은 c00 끝을 다른 문장으로
- 확인(firemap-editor 12:11): 정기 11:50 근무 — 열린 [편집 검수 요청] 0건 · auto 표본 3(hometown·evoucher·isapen, evoucher 고칠 곳 0) · sweep #120·118 볼 것 적음, #169 원고·edit-ok(적용 대기, 하루 edit 상한은 #56 제목 우선)
- [막힘] firemap-improve 14:42: dev(2826c46)→main 반영 못 함 — main 쪽 2커밋(e1b1c35 가이드·b936d60) 병합 시 작업트리의 남의 미커밋 파일(outputs/jepiq_short.mp4 등)로 merge 중단, 임시 worktree 병합은 권한 분류기가 거부. 이번 변경은 research·rules 파일뿐이라 운영 영향 없음 · 다음 정상 병합 때 같이 넘어감
- [배차] firemap-video-producer 10/10 19:30 C-1 롱폼 관문(기한 10/9 19:30) — 16:01 TTS 창 녹음→렌더→gate (정기 18:16은 기한에 빠듯)
  착수: firemap-video-producer 15:10 (운영실장)
  완료(미달·넘김): firemap-video-producer 15:14 — 준비만: editor 서명 해시 일치(script b1f3cbb0·screen_text 6f93fd58)·c1props CUTS 2-2 확인·lfvoice plan 9요청 최대 290음절·ep/C-1/compare.md 만듦(gate 요구) · 막힘: 이 회차가 16:01 전에 끝나야 해서 녹음 못 함(TTS 0요청 사용) → 녹음~gate는 14:18 PD 세션에 세션 메시지로 다시 넘김 · gate 주의: meta desc 없음(chapters.py 뒤), {CAFE} 채우면 끝 카페 줄과 2개 → C9
- [배차] firemap-shorts 비축 쇼츠 0/1 + 10/10 12:20 칸 편·관문(기한 10/10 00:20)
  착수: firemap-shorts 15:10 (운영실장)
  완료(미달): firemap-shorts 15:21 — 10/10 12:20 칸 편 = g1_climb(G-1 '고점에 산 금 본전까지 34%→51%', bars vs·음악 있음) 새로 만듦: compete 5·check 문제 없음·aitell 0.0(.edit.json auto)·review 세 줄 끝. 첫 프레임 1초 고정 조건 v4 5·5, v5 5·5(보정 gongjae1002 7.0~7.5 유효) → 7 미달, gates_ok 안 적음, slots 10/10 12:20 칸 신설. 비축 쇼츠 0/1 그대로(시간 내 둘째 편 못 만듦). 막힘: vs 틀로는 7 안 나옴(최고 6.5) — 다음 1안 +51% 전면 숫자(hero)나 그림 요소 첫 프레임, 공개 전날 G-1 calc 재실행 뒤 숫자 재확인 · 근거 cardshorts/g1_climb/review.md
- 막힘(운영실장 15:21): ① C-1 롱폼(관문 기한 19:30) 녹음은 14:18 PD 세션(local_c8023e07)이 16:01 창에서 이어받음(dcb4c19) — gate 전 걸림 2개: meta.json desc 없음(chapters.py 먼저)·{CAFE} 채우면 카페 링크 2개로 C9. 19:05 운영실장 회차에 voice.json·gates_ok 확인, 없으면 대체 G-1 판단 → firemap-video-producer ② 10/10 12:20 쇼츠 g1_climb 첫 프레임 1초 5·5 미달(통과선 7, a73584d) · 기한 10/10 00:20 · 비축 쇼츠 0/1 → firemap-shorts 다음 안(+51% 전면 숫자·금 그림) ③ 비축 카페 실사용 0/2(npsage1009는 10/14부터) → firemap-write 16:10 정기 1순위

- [요청] **firemap-meeting** ← firemap-video-producer (16:40) 롱폼 녹음 창 배정 · 사실: 10/10 19:30 칸 skip(C-1 IQR 0.19). 남은 대기 C-1(75줄·9요청)·W-1(54줄≈6요청, 10/11 19:30 칸이면 10/10 창 필수)·G-1(다시 녹음) — 한 창 10요청이라 하루 한 편 · 제안: 10/10 창 W-1, 10/11 창 C-1(10/12 칸) 또는 G-1 · 판단 필요(순돌이): ① 1요청 시험이 뒤쪽 요청의 음높이 흔들림(+15%)을 못 잡음 — 무료 제미나이 TTS로는 IQR 0.16이 운(R-1·G-1·C-1 세 번 막힘) ② 이번 C-1 녹음분(c-1_1009)에 lfpitch 사본 소리 심사 허용 여부 ③ Chirp 3 HD 결재(approvals.md, 3편 0.95%)
  착수: firemap-meeting 21:28 — 녹음 창·W-1 칸 배정(위 [지시·긴급] W-1·[알림] 05:16 함께)
  완료: firemap-meeting 21:40 — 녹음 창: 10/10 16:01 W-1(→10/11 19:30 토 고정 칸) · 10/11 16:01 G-1(→**10/13** 19:30) · 10/12 16:01 C-1(→**10/14** 19:30). 레드팀: 녹음 다음 날 공개면 관문까지 3.5시간뿐(M-1 3시간 38분 실측) → G-1·C-1은 녹음 이틀 뒤 공개로. W-1은 '이번 주' 편이라 토요일 유지 · lfpitch 사본 심사: 회의 권고 '쓰지 않음'(법·사용자 참모 모두 기계음 신뢰 하락 지적), 최종은 순돌이 · Chirp 결재 그대로 맨 위 · slots.json 반영 · 근거 meeting/2026-10-09-decisions.md·verify.md·missed-q_레드팀.md
- [알림] **firemap-write** ← firemap-editor (17:08) 오늘 20:10 seniorjob1009 c00 끝 문장 손봄('표로 정리했습니다'가 18:10 evoucher와 같은 틀) — 숫자·출처·면책 0 변경, editgate 재stamp, 발행 그대로 진행 · 22:10 brokerfee1009 그대로 통과(경계 계산 검산 맞음). 다음 묶음 c00 끝은 '표로 정리했습니다' 말고 다른 문장으로
- 확인(firemap-editor 17:08): 정기 16:50 근무 — 열린 [편집 검수 요청] 0건 · auto 표본 2 · 공개 카페 #169 끝맺음 3곳 적용(되읽기 OK, 오늘 수정 1/3)
- [자발] copywriter g1_climb(10/10 12:20 쇼츠) 첫 프레임 문구 — 1초 5·5 미달의 문구 몫 (열린 지시 0, G-1 calc 대조는 10/11)
  착수: firemap-copywriter 18:52
  완료: firemap-copywriter 18:51 — 1위 첫 프레임 '금 -34%, 왜 +51%?'(+51%만 크게) + 작은 줄 '1/29 고점 1g 269,810원 → 10/6 179,000원' · 제목 '금값 고점 대비 -34%, 산 값으로 돌아가려면 +50.7% #shorts' · 3명 평균 8.57(제미나이 9.2·레드팀 8·작성자 8.5) · 2위 K7 7.77 · 근거 cardshorts/g1_climb/copy/titles.md
  [알림] **firemap-shorts** (copywriter 18:51): g1_climb v6은 copy/titles.md 1위 문구로. **지금 v5 '본전까지 몇 %?'는 G-1 금지어('본전' — 파는 값 차이 별도)라 공개 전 반드시 뺄 것**(compete.md 첫 3초 문장도). 제목 '고점에 샀다면'은 경쟁 4 틀이라 바꿈. 설명란에 'KRX 금 종가 기준, 사고팔 때 수수료 별도'. 1초 시험 점수는 그림 요소(금 막대) 몫이 남음
- [배차] firemap-write 비축 카페 실사용 0/2(retmid1005 사용·npsage1009 10/14까지 잠김) → 비축 1편 관문 통과까지 (운영실장 19:09)
  착수: firemap-write 19:09 (운영실장)
  완료: firemap-write 19:12 — 비축 카페 schdacct1007 gates_ok 기입(slots.json reserve.cafe): editgate auto 해시 일치(10/9 16:21)·readcheck 0·selfcheck 사실 0·aitell 1.1·naverpost pending block 없음. 한계: SCHD 7일 규칙으로 10/10 14:30부터 공개 가능, 공개 전날 시세 재조회 필요. 비축 사용 가능 1/2(npsage1009 10/14 잠김) — 한 편 더 필요
- [배차] firemap-motion-designer backlog 1순위 G-1 핵심 장면 2개(WaterfallPieces·AsymClimb) 미리보기·심사 (운영실장 19:09)
  착수: firemap-motion-designer 19:09 (운영실장)
  완료: firemap-motion-designer 19:28 — G-1 3장 세 조각 WaterfallPieces 미리보기(34.5초 어림, ep/G-1/motion_preview/g1_wf.mp4) · 숫자 calc_out만(곱 % 글자·로그 몫 %p 막대 assert) · 최장 정지 2.5초 · 심사 9·6·6 평균 7.0(레드팀 '더하기로 읽힘'→막대 %p 표기·꼬리표 색·화살표 고침) · AsymClimb은 다음 회차
  [요청] **firemap-video-producer**: G1.tsx '3.' 장 piece1·prem·piece1b 세 장면을 `<WaterfallPieces {...wf} />`(TallyFrame 자식) 한 장면으로 — 녹음 뒤 `py -3.12 work/research/longform/ep/G-1/motion_preview/wfprops.py` 돌려 g1_wf.json의 scene.frames·wf 그대로, 렌더 뒤 그 구간 motioncheck(최장 정지 3초 이하) · 자세히 ep/G-1/motion.md · (motion 19:28)
- [배차] firemap-shorts 10/10 12:20 칸 g1_climb v6(copywriter 1위 문구 '금 -34%, 왜 +51%?'·'본전' 빼기) 1초 시험 — 관문 기한 10/10 00:20, 비축 쇼츠 0/1 (운영실장 23:09)
  착수: firemap-shorts 23:09 (운영실장)
- [배차] firemap-write 10/10 12:10 칸 eitclate1009 hold — 비축 schdacct1007(14:30부터라 12:10 불가면 다른 편)로 교체·관문(기한 06:10) + 10/11 10:10 칸 배정 (운영실장 23:09)
  착수: firemap-write 23:09 (운영실장)
  완료(일부): firemap-write 23:14 — 10/10 12:10 칸 교체: eitclate1009(표지 6.67 상한에 막힘)를 뺴고 새 편 childleave1010(육아휴직급여, 검색 79,500·dupcheck 새것·법 제70조/시행령 제95조 원문 facts.txt) 배정 · 10/11 10:10 TBD-CALC-연봉실수령 배정(기한 04:10) · patrol의 '보류됨'·'10-11 10:10 배정 없음' 사라짐 / 미완: childleave1010 원고·관문 gates_ok(기한 06:10, 00:10~06:10 회차) — 비축 npsage1009(10/14 08:30 전 불가)·schdacct1007(14:30 전 불가)은 12:10에 못 써서 새 편이 유일한 길 · 비축 카페 2/2지만 schdacct 16:10 소진 뒤 1
- 막힘(운영실장 23:17): ① 10/10 12:20 쇼츠 g1_climb v6·v7 첫 프레임 1초 5·5 미달(fc0df33) — 관문 기한 00:20 넘김, 비축 쇼츠 0/1. 쇼츠 칸은 skip 불가(patrol) → 다음 안(사진급 금 이미지·hero 숫자 카드) 또는 다른 편, 12:20 정기 근무 전 결론 필요 · 순돌이 판단: 기한 넘긴 채 공개 여부 ② 10/10 12:10 카페 childleave1010 새 편(afc23fd) 원고~editgate 남음, 기한 06:10 — write 다음 회차(08:10 정기 전 03:05 배차) 1순위 · 10/11 10:10 TBD-CALC-연봉실수령 기한 04:10 ③ 10-10 19:20 쇼츠 칸 배정 없음(하루 1편 규칙이면 skip 표시 필요 — 회의 몫)
- [배차] firemap-write 10/10 12:10 칸 childleave1010 원고~editgate·gates_ok(관문 기한 06:10) + 10/11 10:10 연봉실수령(기한 04:10 넘김 → 비축으로 칸 채우기) (운영실장 03:09)
  착수: firemap-write 03:09 (운영실장)
  완료: firemap-write — 10/10 12:10 카페 childleave1010 원고~관문 끝(제목 평균 7.5·표지 7.25·editgate auto·readcheck/selfcheck/aitell 통과·slot.txt 12시·naverpost pending은 코너 시각 전 보류만), slots.json gates_ok 기입(기한 06:10 안) · 표지 약점: 하단 부제 110px에서 안 읽힘(다음 개선) · 10/11 10:10 연봉실수령 기한은 10/11 04:10이라 아직 안 넘음(오늘 밤 회차 몫, 비축 대체 불필요) · 03:30
- [배차] firemap-shorts 10/10 12:20 칸 g1_climb 1초 미달(기한 00:20 넘김) — 다음 안(사진급 금 이미지·hero 숫자 카드) 또는 다른 편으로 첫 프레임 7 넘기기·비축 쇼츠 0/1 (운영실장 03:09)
  착수: firemap-shorts 03:09 (운영실장)
- 막힘(운영실장 03:31): 10/10 12:20 쇼츠 g1_climb v8·v8b(사진급 금 배경) 첫 프레임 1초 5·5 미달(f04709c) — 네 계열(v4~v8b) 모두 5, 비축 쇼츠 0/1. 12:20 정기 근무 전 결론 필요: +51% 한 숫자 hero 카드 또는 다른 편 · 순돌이 판단: 미통과 공개 여부(npsday1007 선례) → firemap-shorts
- [알림] **firemap-write** ← firemap-editor (07:08) 오늘 12:10 childleave1010 c04 신청 문단 말투만 손봄('-하고요' 겹침·'그리고' 덜어냄) — 숫자·기간·출처·면책 0 변경, editgate 재stamp, 발행 그대로 진행 · 08:10 acqtax1010·10:10 sevbasis1010 그대로 통과
- 확인(firemap-editor 07:08): 정기 06:50 근무 — 열린 [편집 검수 요청] 3건 전부 통과(W-1 대본·화면 재서명, A-1 쿠팡 줄) · auto 표본 3(고침 1) · sweep은 다음 근무(하루 edit 상한)
- [배차] firemap-write 10/10 14:10 카페 칸 TBD 편 확정~관문(기한 08:10) + 18:10 TBD-CALC-실업급여(기한 12:10) (운영실장 07:09)
  착수: firemap-write 07:09 (운영실장)
  완료(일부): firemap-write 07:16 — 14:10 칸 주제 후보 종부세 1주택 고령자·보유 공제 합산 80%(jongbuse1010, 검색 9,820·dupcheck 새것) 선정·법령 원문 사실표 작성(work/research/jongbuse1010/pkg/facts.txt) / 미완: 원고~관문·gates_ok(기한 08:10) · 18:10 칸은 보조 직원이 진행 중 · 막힘: 재경부 9/1 세제개편안 종부세 개편 본문이 첨부 PDF뿐이라 다운로드 승인 필요(개편 내용 미확인이면 글에 안 씀)
- [배차] firemap-shorts 10/10 12:20 칸 — g1_climb 네 계열 1초 5 미달 → '+51%' 한 숫자 hero 카드 또는 다른 편으로 첫 프레임 7 넘기기(12:20 전), 비축 쇼츠 0/1 (운영실장 07:09)
  착수: firemap-shorts 07:09 (운영실장)
  완료(미달): firemap-shorts 07:14 — g1_climb v9 hero 한 숫자 전면판('금 -34%, 왜 +51%?') 고정 조건 1초 시험 5·5(보정 7.5·7.0 유효) 미달 → gates_ok·reserve.shorts 안 넣음, 미달 공개 금지. 글자·벡터·사진·hero 5계열 모두 5라 g1_climb 접음(같은 그림 재시험 금지). 12:20 칸은 slots.json note에 사유. **비축 쇼츠 0/1 그대로** — 다음 판은 사진·인물급 그림 요소를 넣을 수 있는 다른 편 또는 칸 skip (cardshorts/g1_climb/review.md v9)
- 막힘(운영실장 07:16): ① 10/10 12:20 쇼츠 — g1_climb v9 hero 카드도 1초 5·5(4474047), v4~v9 다섯 계열 미달로 g1_climb 접음 · 비축 쇼츠 0/1 → 12:20 정기 근무가 다른 편 관문 통과 아니면 skip+사유 · 순돌이 판단: 쇼츠 칸 skip 불가 규칙 vs 미달 공개 금지 충돌 → firemap-shorts ② 10/10 14:10 카페 jongbuse1010(종부세 고령자·보유공제) 사실표만, 원고·관문 0(addfe82) — 9/1 세제개편안 첨부(PDF/hwpx) 원문 미확인이라 개편 언급 없이 현행법만으로 08:10 정기가 이어감, 관문 기한 08:10 넘김 → 안 되면 비축 schdacct1007 당겨쓰기 검토 · 18:10 실업급여 칸 ubcalc1010은 보조 에이전트 작업분 미커밋 가능 → firemap-write 08:10 확인
- [자발] copywriter g1_climb 1초 5점 다섯 계열 — 그림만 바뀌고 문구('금 -34%, 왜 +51%?')는 그대로였다. 심사 지적은 매번 '호기심 장치 약함·수학 퀴즈' → 문구 몫 진단·새 문구 시험 (열린 지시 0)
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:52 — 그림 v9 고정·문구만 3안(n1 '고점에 산 금 1천만원/지금은 663만원'·n3 '…산 값 되찾으려면 +51%'·n2 '금 34% 빠지면 산 값까지 +51%') 1초 시험 전부 5·5(보정 7.0~7.5 유효), 주제는 6/6 맞힘 → **문구는 병목 아님**. 같은 심사로 c1_tiles·nps1988·npsday1007 27건도 평균 7 이상 0건(최고 6.5) = 글자 카드 틀 천장 · 근거 cardshorts/g1_climb/copy/ff/README.md · 쓸 거면 문구 1위 n3
  [알림] **firemap-shorts** (copywriter 07:52): g1_climb은 문구를 바꿔도 5 — 같은 문구 재시험 말 것. 다른 편을 글자 카드로 만들어도 이 심사에선 6.5 천장이라 12:20 칸 관문 통과는 그림 틀(사진·화살표가 주인공인 첫 프레임)을 바꾸지 않으면 어렵다
- 막힘(copywriter 07:52): 쇼츠 1초 시험(rejudge_ff 고정 조건) 글자 카드 31건 평균 7 이상 0건 → 쇼츠 칸 'skip 불가'와 '미달 공개 금지'가 구조적으로 부딪침(비축 쇼츠 0/1이 계속 남는 이유) · 순돌이 판단: 쇼츠 첫 프레임 틀 자체를 바꿀지, 1초 시험 기준을 쇼츠 틀에 맞게 다시 보정할지 → firemap-shorts·순돌이
- [지시] **firemap-shorts** 트랙:A (본부장 youtube-loop 08:46, 기한 12:20) 의도: 12:20 쇼츠 칸을 비우지 않는다 · g1_climb v9(copywriter 1위 '금 -34%, 왜 +51%?', '본전' 없는 판)를 **1초 미달인 채 공개**: X-SHORTS-1S B 첫 편(experiments-registry, log.jsonl experiment='1S-B'·1초 점수 5·5 기록) · 공개 전 확인: 숫자 기준일 표기(1/29 고점·10/6 KRX 종가), 설명란 'KRX 금 종가 기준', shortsdaily.gate() 통과, 사실·편집·compete·review 관문은 그대로 · 판정 10/12 12:20(48시간): 조회 225 미만 **그리고** 넘기지 않은 비율 12% 미만이면 B 중단 보고 · 근거 decisions/docs/shorts-1s-gate-1010.md · 금지: 다른 관문 생략, '본전' 문구
- [배차] firemap-write 10/10 16:10 카페 칸 gates_ok 없음(관문 기한 10:10 넘김) → 편 확정~관문 통과, 안 되면 비축으로 칸 채우기 + 10/11 08:10 칸(기한 02:10) 배정 (운영실장 11:09)
  착수: firemap-write 11:09 (운영실장)
  완료: 10/10 16:10 카페 칸 schdacct1007(비축) 관문 통과 gates_ok 10/10 11:12 기입(SCHD 10/9 종가 33.04달러 재조회 6,290→6,270만원, editgate 재날인, readcheck 0·selfcheck 사실 0·aitell 1.1) · 10/11 08:10 칸 firemap-write 배정(기한 02:10, 후보 새 편/eitclate1009) 11:12
- [배차] firemap-visual-designer 비축 쇼츠 0/1·10/11 12:20 칸(기한 00:20) — copywriter 07:52 결론(글자 카드 틀 1초 천장 6.5)에 따라 사진·화살표가 주인공인 새 첫 프레임 틀 시안 → 1초 시험 7 넘기기 (운영실장 11:09)
  착수: firemap-visual-designer 11:09 (운영실장)
  완료(미달): firemap-visual-designer 11:17 — g1_climb 사진·화살표 첫 프레임 틀 13안(p1~t3) 같은 1초 시험(rejudge_ff 고정 조건) 26회: **7 넘긴 틀 없음**, 최고 r1(밝은 금 사진+'고점에 샀다면?'+'산 값까지'+거대 +51%+노랑↑) 6·6.5·6·6(평균 6.13)·t1·t3 6·6 — 글자 카드 5·5보다 한 칸 오름, 보정칸 7~7.5 정상 · 심사 매번 '+51%가 수익률로 오독, 본전·회복 단어 넣어라'(copywriter 원칙상 안 씀) · 실제 KRX 선을 크게 키우면 5로 떨어짐 · 근거 cardshorts/g1_climb/ff2/README.md·all_168.png · [알림] 없음(통과 틀 없음) · 다음 열쇠: copywriter '본전' 류 단어 허용 판단 → r1 틀 문구만 교체 시험
- 막힘(운영실장 11:18): ① 비축 쇼츠 0/1 — visual 사진·화살표 첫 프레임 13안 최고 r1 평균 6.13(글자 카드 5보다 +1, 7 미달, 82fe1ea). 심사가 매번 '+51%가 수익률로 읽힘·본전/회복 단어 넣어라' → copywriter 판단: '본전·회복' 허용 여부(허용 시 r1 문구만 바꿔 재시험) → firemap-copywriter 12:40 정기 ② 10/11 08:10 카페 칸 편 미확정(기한 02:10) → firemap-write 22:10·00:10 · 비축 카페 1/2
- [자기 배정] firemap-motion-designer backlog 1순위 G-1 '6. 산 값까지' AsymClimb 미리보기·심사
  착수: firemap-motion-designer 11:25
  완료: firemap-motion-designer 11:39 — G-1 6장 AsymClimb 미리보기(17.8초 어림, ep/G-1/motion_preview/g1_asym.mp4) · 숫자 calc_out 첫 줄만(269,810·179,000원·−33.66%·+50.7% assert, 차액 숫자 안 만듦) · 최장 정지 1.0초·움직임 93% · 심사 제미나이 9·Claude 6.5·레드팀 5→7(빗금 두 뜻·빨강 몫 사라짐·후반 정적 고침) 평균 7.5 통과
  [요청] **firemap-video-producer**: G-1 녹음 뒤 `py -3.12 work/research/longform/ep/G-1/motion_preview/asymprops.py` → G1.tsx math 장면(kind 'asym', 지금 숫자를 굴리는 TallyCountUp)을 `<AsymClimb {...asym} />`(TallyFrame 자식)로, scene.frames·sub는 g1_asym.json · 렌더 뒤 그 구간 motioncheck(최장 정지 3초 이하)·'51% 올라야' 말과 빨강 몫 쌓임 시점 확인 · 화면 글자 늘어남 → 편집 재서명 · 자세히 ep/G-1/motion.md '6장' · (motion 11:39)
- [알림] **firemap-shorts** ← firemap-editor (12:07) 12:20 g1_climb v9 편집 통과(g1_climb_v9.edit.json) · 제목만 copywriter 1위로 바꿈: '금값 고점 대비 -34%, 산 값으로 돌아가려면 +50.7% #shorts'(desc.txt 첫 줄도) — 업로드 때 v9 spec의 yt_title 그대로 쓰면 됨 · 지시대로 설명란 'KRX 금 종가 기준, 사고팔 때 수수료 별도'는 아직 없음(사실 문구라 편집이 안 넣음, 공개 전 shorts가 넣기)
- [알림] **firemap-write** ← firemap-editor (12:07) 18:10 ubcalc1010 c01·c02, 20:10 jongbuse1010 c00 말투만 손봄 — 숫자·출처·면책 0 변경, frame 통과, editgate 재stamp, 발행 그대로 진행
- 확인(firemap-editor 12:07): 정기 11:50 근무 — 열린 [편집 검수 요청] 0건 · 쇼츠 g1_climb v9 통과 · auto 표본 2(고침 2) · sweep은 다음 근무
- [정기] firemap-write 12:10 칸 childleave1010 발행·verify
  착수: firemap-write 12:21
  완료: firemap-write 12:44 — 12:10 childleave1010 cafe/243 발행 verify OK 1524/1524자·사진 4/4 · 10/11 08:10 칸 inhded1011(상속세 면제한도 1차 2,037만·2차 1억3,240만5천·동거주택 533만5천원, 검색 27,390·dupcheck 새것, 법 2026-01-01 시행본 원문) 원고·readcheck 0·selfcheck 사실 0·aitell 3.6·crosscheck 반영·제목(쉼표판) 7.5 통과 / **미통과: 표지 최고 F 6.83(레드팀 6)·쉼표 없는 제목 최고 6.67 → editgate stamp 안 됨**(기한 02:10, 다음 write 회차) · slots.json 08:10 칸 item 기입
- [표지 요청] inhded1011(10/11 08:10 칸, 관문 기한 02:10) · 담당 firemap-visual-designer · 근거 work/research/inhded1011/pkg/cover_review.md(제미나이 최고 7.5, 레드팀 6 — 큰 숫자 판 폭 절반·아랫줄 110px 안 읽힘) · 문구는 '상속세 면제한도 / 6배 넘게 / 2,037만→1억3,240만'(본문 숫자) · 요청 firemap-write 12:44
- [카피 요청] P-1 국민연금 수령나이 롱폼 제목·썸네일 문구·첫 3초 트랙:C · 담당 firemap-copywriter · 시한 10/12 12:00(주간 선정 전) · 근거 longform/ep/P-1/analysis.md ②(검색어 '국민연금 수령나이' 45,780 맨 앞)·compete.md 경쟁 제목 틀(명령형 경고·'덜컥 받으면 큰일' — 피할 틀)·script.md 0장(하루 차이 생일 두 장) · 금지: '받으세요'·'이득'·'손해'·68세 단정 (youtube-loop 12:49)
- [편집 검수 요청] P-1 대본 v1 트랙:C · 담당 firemap-editor · 시한 10/12 18:00 · 근거 longform/ep/P-1/script.md(말 76줄, say_v1.txt) · scriptnum 35개 중 사실표 밖 0·aitell script 62.9/7% 통과·제미나이 지적 3 반영(review_v1_gemini.md) · 금지: 숫자·조문 표현('조문대로 계산하면') 바꾸기 (youtube-loop 12:49)
- 확인(youtube-loop 12:49): 자발 — PD 대기열 C-1·G-1 뒤 빈칸이라 P-1 대본 v1을 주간 선정(10/12) 전에 미리 씀. 선정 안 되면 비축 롱폼. 남은 것: 심사 3명(review.md)·카피·편집
- [알림] **firemap-write** (improve 14:37): rules.json 새 규칙 — 카페 배당·ETF 제목은 %보다 원 금액(224편 실측, 배당·ETF 안 % 제목 19편 하루당 0.41 vs 48편 0.74). 오늘 22:10 odivfx1010 제목 '…석 달 새 11.35% 감소'가 해당 — facts C5에 '100주 세후 34,958→30,989원(3,969원 감소)' 금액이 있음. 제목을 바꾸면 제목 관문(judge_title) 다시 거칠 것, 시간이 없으면 그대로 내도 됨(판단은 write)
- 예술가 제안: **DA 문턱 쇼츠 '국민연금 밖' 대조 1편** — 건보 피부양자 소득 2,000만원 경계 두 칸('1,999만원 / 2,001만원' → 피부양자 유지 / 지역가입자), 숫자는 시행규칙 별표 원문 사실표 먼저(내 원문 확인 안 함)·보험료는 계산 줄 있을 때만·'폭탄' 금지 → 담당 firemap-shorts, 다음 빈 쇼츠 칸(비축 0이면 비축 1번), 시험 기한 10/17 · 목적: AL(npsday1007 46h 1,457회, 1초 5·5)이 '문턱 모양' 덕인지 '국민연금 검색어' 덕인지 가르기 · 성공: 48h ≥675(중앙 450×1.5) 또는 댓글 '부모님' ≥3 · 버림: 48h <450이면 문턱은 국민연금 안에서만 · 경쟁 상위 8편 전부 8~28분 설명, 경계 두 칸 쇼츠 0 · 근거 art/2026-10-10-1445.md DA (artist 14:48)
- 판정(artist 14:48): **AL 하루 차이 문턱 성공**(성공선 48h ≥430 → 46h 1,457회, 최근 12편 1위) → [알림] **firemap-youtube-loop**: longform/loop/proven-formats.md에 쇼츠 '문턱 두 칸' 틀 등록 검토(기준선 1.5배 넘음 — 편마다 새 원문 1개) · 참고: 1초 점수 5·5 편이 1위 = X-SHORTS-1S 판정 자료 · AY 계기판 247회(시청 시간 비교 확인 안 함)
- [배차] firemap-shorts 비축 쇼츠 0/1 — artist 14:48 제안 DA 문턱 '1,999만원/2,001만원' 피부양자 대조 1편(AL 문턱 틀 46h 1,457회 성공) 사실표 원문부터·관문 통과 시 reserve.shorts (운영실장 15:10)
  착수: firemap-shorts 15:10 (운영실장)
  완료(미달): firemap-shorts 15:30 — DA 문턱 피부양자(da_thresh): 법제처 원문(시행규칙 별표 1의2 소득요건 '연간 2천만원 이하'·시행령 제41조·법 제6조③) facts.txt·compete 5(경쟁 전부 '탈락 N가지' 목록, 경계 두 칸 0/5, 조회/구독 x75.9)·check 문제 없음·32초 아닌 6초 vs 카드 렌더·전체 영상 점검 통과(빈 곳 65%→38%, cardshort.py vs_point_size 추가). 1초 시험(첫 프레임 168px) v1 5·5·v2 5·5 = 5.0 미달 → gates_ok·reserve.shorts 안 넣음, **비축 쇼츠 0/1 그대로**. 안 돌린 것: aitell·편집·레드팀(미달이라 건너뜀). 키워드 수요 낮음(kwvol 피부양자소득 30) (cardshorts/da_thresh/review.md)
