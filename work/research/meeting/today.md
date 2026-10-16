# today.md — 지금 열린 일만 (2026-10-06 05:55 점검관 정리, 150줄 이하 유지)
- 열린 일만 둔다. 끝난 일·지난 점검·순찰 메모·긴 설명은 `archive/날짜.md`(오늘 앞부분 전체 원문 = **archive/2026-10-02.md 맨 아래 '554줄 원본'**, 어제 = archive/2026-10-01.md).
- 지난 기록은 archive/날짜.md. 직원은 이 파일 전체를 읽지 말고 **자기 task-id(예: firemap-product-dev)로 검색**해 자기 줄만 읽는다. 근거가 필요하면 archive/2026-10-02.md에서 같은 문구로 찾는다.
- 끝나면 그 항목 밑에 "완료: … HH:MM" 한 줄. 다음 정리 때 완료 항목은 archive로 옮긴다(이 파일이 150줄을 넘으면 같은 방식으로 다시 줄인다).

- [요청] **firemap-write** ← PD (04:13) 쇼츠 짝 카페 글 1편 · 칸은 10/22 20:10 또는 22:10(쇼츠 07:20 공개 뒤, 회의 배정) · g1s_asym https://youtu.be/ZK219BbhJSA 질문 '1월 고점에 산 금, 본전까지 몇 % 올라야 하나' — 표: 1천만원어치 산 날 4개(1년 전 956·3개월 전 878·한 달 전 918·1월 고점 663만원, KRX 2026-10-06) + 본전까지 337만원=51%('떨어질 땐 1천만원에서, 오를 땐 663만원에서 셈') · 원본 롱폼 https://youtu.be/xBTZtRp5lMs · 재료 cardshorts/g1s_asym/upload.json·review.md · 전망·권유 없음
- [요청] **firemap-write·firemap-video-producer** ← firemap-audit (21:16) 경미 · work/disclaim.py PAT가 '(라는 뜻|라는 말)…(아니)'만 있어도 통과 → r1cafe_start1016(ETF 비교)이 '…아니라는 뜻입니다. 앞으로도 이럴 거라는 얘기가 아니에요.'로 editgate disclaim_check 통과(권유 말투는 0, 공개분 수정 불필요) · 할 것: PAT에 같은 줄 '권유|사거나|팔라|사라는|넣으라|받으라' 필수 조건 추가(ytlong C9·w1g1clips_up도 같은 함수) → 대기 묶음·예약 설명 재검사 · 기한 10/18 · 근거 longform/loop/audit.md 10/16 · STOP 아님
  착수: firemap-video-producer 22:21 — disclaim.py PAT 엄격화(PD 몫, ytlong·w1g1clips_up·editgate 같은 함수)
  완료: firemap-video-producer 22:33 — disclaim.py: 같은 줄에 '권유|사거나|팔라|사라는|넣으라|받으라' 필수(ACT) 추가 · 시험: '…아니라는 뜻입니다. 앞으로도…' 거부·'투자 권유가 아닙니다'·'사거나 팔라는 뜻이 아닙니다' 통과 · 대기분 재검사(ep/*/meta.json·cardshorts/*/upload.json): 새로 걸린 것 p1s_step 1편('일을 줄이거나 늘리라는 뜻이 아닙니다' → '…권유가 아닙니다'로 고침, 미업로드) · N-1 meta는 옛 규칙에도 없던 것(공개분, 고치지 않음) · editgate.disclaim_check 같은 함수라 카페 대기 묶음도 자동 적용(write 재검사 몫)
- [요청] **firemap-video-producer** ← firemap-audit (21:16) 경미 이월 · 썸네일 규칙 3 P-1(10/16 11:30) 공개 뒤 ep/P-1/app_preview.png 없음(10/15 요청 착수 줄도 없음) · 감사 대신 확인 통과(ep/P-1/app_preview_1016_audit.png) · 할 것: ytlong 공개 확인 단계에 app_preview 저장을 넣어 W-1 2화(10/17 11:30)부터 남김 · STOP 아님
  완료: firemap-video-producer 22:33 — 썸네일 규칙 3 단계: `py -3.12 work/ytlong.py preview <ep폴더> <videoId>` 추가(i.ytimg 실제 걸린 썸네일 → 412px·168px + 길이 칸, ep/<편>/app_preview.png) · P-1 vsL7mojDW7w로 시험 저장·눈 확인(168px에서 76.7·80.7 읽힘, 길이 칸이 글자 안 가림) · W-1 2화(10/17 11:30)부터 공개 뒤 첫 댓글 회차가 함께 돌림
  완료: firemap-audit 21:16 — 10/16 감사 심각 0·경미 2(위 두 요청), 사실 4편 일치, 켠 스위치 없음
## ★ 전체 회의 10/16 21:29~21:58 — 반론 처리·내일 지시 (근거 meeting/2026-10-16-verify.md·missed-q_레드팀.md)
- 막힘: 수익 경로 — 쿠팡 칸은 연봉·퇴직금·실업급여 계산기 3개에만 있고, 10/16 카페 중 그 셋으로 가는 글은 1편(레드팀, editgate.py:88~96) · utm 16세션 전부 '기록없음'이라 카페→사이트 유입 판정 불가(체크리스트 46) · 리틀리 가입(X-KR-1) 결재 16일째
- [지시·긴급] **firemap-video-producer** (기한 10/18 11:30 — C-2 관문 기한) 의도: C-2(10/19 11:30)가 ytlong C1 '7일 7편'에 **확정으로** 걸림(검증: W-1 0yWQ 10/12 19:47 때문, C-1 장부와 무관) · 완료 기준: C-2 예약을 10/19 **19:50**으로(그날 롱폼 1편 유지, 11:30 칸은 비움 표시 'C1 이동') · ytlong gate 통과 출력 남김 · 금지: 장부 고치기·C1 끄기 · 보고: decisions/log
  착수: firemap-video-producer 22:21
  완료: firemap-video-producer 22:33 — C-2 meta publishAt 2026-10-19T19:50+09:00(옛 값 publishAt_prev_1016) · slots 10/19 11:30 줄 item '비움(C1 이동)'·19:50 C-2 새 줄 · ytlong gate 출력 ep/C-2/check/gate_1016_2235.txt: **C1 안 걸림**(남은 막힘 4: understand_test 판정 줄·bench_check 대조 줄·thumb·배경 v3 bgcheck 28%) · 덤: C-2·T-1 meta에 desc 칸 없어 gate KeyError → desc_tpl+챕터로 채움(C-2 챕터 초 단위=c2.json 장면 시작과 맞음, 배경 재렌더 뒤 다시 맞출 것) · 쇼츠 c2s_jungwoo 10/19 19:20 → 10/23 19:20(원본 C-2 19:50보다 먼저 나가지 않게, 빈 칸 채움) · 10/19 19:20은 N-2 새 클립(v3 틀, 제작 중) · 장부·C1 안 건드림
- [지시] **firemap-improve** (기한 10/18) 의도: C1이 하루 1편 지시와 부딪쳐 매주 늦은 편 하나가 7일 뒤 11:30을 막는다(10/25 11:30도 7편 예상, 레드팀) · 완료 기준: ① ytlong.py에 `forecast` — 앞으로 14일 롱폼 칸 전부에 C1을 미리 돌려 막히는 칸을 출력(체크리스트 47) ② uploads.jsonl 줄에 공개 상태 확인(videos.list, 내린·비공개 영상은 'removed'로 표시해 셈에서 뺌 — 공개되지 않은 영상은 '대량 공개'가 아니므로 측정 바로잡기) · 막는 코드: ytlong.py C1 · 금지: 7편 상한 숫자 바꾸기(사장님 빈도 결정 영역)
- [지시] **firemap-write** (기한 10/18) 의도: 글 질문과 다른 계산기로 보내지 않기 + 수요 몰린 주제에 길 내기 · 완료 기준: ① editgate.py CALC/calc_check — '퇴직소득세' 제목이 세전 퇴직금 계산기(severance)로 가는 것을 막음(src에 퇴직소득세 계산기 없음 → 줄 없음 또는 '퇴직금 먼저 계산' 문구로) ② 예금·이자 주제(10/14 정기예금 글 1,322회, 30편 조회 74%)에 맞는 계산기가 firemap.kr에 있는지 확인해 있으면 대응표 추가, 없으면 '없음' 기록 · 막는 코드: editgate.py calc_check
- [요청 확인] **firemap-write·firemap-video-producer** disclaim.py 엄격화(감사 21:16 요청, 기한 10/18) — 회의가 받아들임(법 참모·검증 ①). 막는 코드 disclaim.py PAT → editgate.disclaim_check·ytlong.gate 같이 강해짐
- [지시] **firemap-report** (기한 10/18 12:30 회차) 의도: 카페→사이트 전환을 잴 수 있게 · 완료 기준: sitedaily.sql에 utm_campaign별 줄 + 외부 세션 utm·referrer 기록률 줄, revenue.md 줄에 '기록률 %' · utm cafe 사흘 0이면 report에 경보 한 줄 · 카페 본문 계산기 URL이 실제 링크로 걸리는지 공개 글 1편 열어 확인
- [지시] **firemap-youtube-loop** (기한 10/18) X-XP-1 판정용 유튜브 EXT_URL(cafe.naver.com) 28일 값 ytanalytics로 재기 · 쇼츠→롱폼 '관련 동영상' 연결이 API로 되는지 확인(10/16 쇼츠 786·421회인데 관련 동영상 유입 0, 레드팀 기회 2)
- 칸(회의 원칙): 10/17 카페 TBD 9칸은 3시간 스프린트가 배정 · 짝 글 note 넣음(10/17 21:10 d1s_when·10/18 07:40 g1s_why·10/18 15:10 N-2(12:10에서 옮김)·10/18 21:10 r1s_gap) · **10/17 07:40 h1s_gap 짝은 write-b가 note 확인**(장부 반영 안 됨) · w2cafe1017(10:40) 관문 기록 없음 → write-b 04:40까지 · 카페 비축 0/2 → 각 회차 새 편
  완료: firemap-meeting 21:58 — 반론 처리·지시 6건·짝 글 칸 4(today.md·decisions/log)
## ★ 전체 회의 10/15 21:28~21:45 — 반론 처리·내일 지시 (근거 meeting/2026-10-15-verify.md·missed-q_레드팀.md)
- 막힘: 예약 영상 videos.update가 무인 회차에서 자동 권한 판단기에 거부(10/15 06:22·10:21) → P-1 제목·썸네일, W-1 2화 설명란, w1s_kospi 교체 모두 못 함 · 순돌이 채팅 세션 실행 또는 사장님 허용 필요 · E-2·N-1·M-1 합성 표시 꺼짐(10/13부터)
- [지시·긴급] **firemap-video-producer** (기한 10/16 07:20 — w1s_kospi 공개 12시간 전) 의도: 10/15 코스피 −7.57% 뒤 '지난주 −54만원' 쇼츠가 이번 주 숫자로 오독되지 않게 · 완료 기준: ① w1s_kospi(njvFqMeKQlU, 10/16 19:20) 예약을 풀고 그 칸에 p1s_step(P-1 11:30 공개 뒤 업로드, 다른 질문) 또는 날짜 박은 제목으로 교체 ② videos.update가 또 거부되면 고치지 말고 공개 직후 첫 댓글에 '10/6~10/10 주 기준, 10/15 급락 전 숫자' 한 줄(댓글은 무인으로 됨) + today.md 막힘 · 금지: 권한 판단기 우회 · 보고: decisions/log
  착수: firemap-video-producer 22:17 — njvFqMeKQlU 예약 풀기 1회 시도 → 되면 p1s_step을 10/16 19:20에, 거부면 공개 뒤 첫 댓글 길
  완료(① 막힘 → ② 길 준비): firemap-video-producer 22:27 — njvFqMeKQlU 예약 풀기(videos.update) 1회 시도 → 권한 판단기 거부(External System Writes), 우회 안 함 · ② 첫 댓글 문구 cardshorts/w1s_kospi/first_comment.txt('지난주'=10/6~8 화~목 장, 10/5·9 휴장, 10/12 이후 급락 미포함 + 원본 롱폼 링크, aitell 0.0, 원문에 없는 −7.57%는 넣지 않음) — **10/16 19:20 공개 뒤 PD 회차가 commentThreads.insert** · 채팅 세션이 먼저 열리면 ①(예약 풀고 p1s_step 10/16 19:20) 실행 가능
  막힘: firemap-video-producer 22:27 — 무인 회차 YouTube 쓰기(videos.update) 오늘 세 번째 거부 → w1s_kospi 교체·d1s_pension v3 교체(--replace)·P-1 제목·W-1 2화 설명 모두 채팅 세션 또는 사장님 허용 필요. 첫 댓글(commentThreads.insert)도 같은 판단기에 걸릴 수 있음(확인 안 함)
  완료(②): firemap-video-producer 19:51 — 19:20 공개 뒤 첫 댓글 게시 UgxyBiCoxufD1cfDxB14AaABAg (지금 판 **DRtKbSuCUiQ** — 오늘 쇼츠 안전 영역 틀 교체판, njvFqMeKQlU는 비공개·예약 없음) · 문구 cardshorts/w1s_kospi/first_comment.txt 그대로 · commentThreads.insert는 무인 회차에서 됨 · 고정 대기: DRtKbSuCUiQ
- [지시] **firemap-video-producer** (기한 10/17 11:30) W-1 2화(AxTB7izIBUA): 공개 직후 첫 댓글에 목요일 10/15 숫자(삼성 종가·코스피 −7.57%, 대본 계산식 그대로 −300만원→목요일까지 치면 얼마) + 짝 글 w2cafe1017 주소 · 설명란 '이번 주' 고치기는 videos.update 허용 뒤 · 근거 verify 5·6, 레드팀 1
- [지시] **firemap-write-b** (기한 10/17 04:40 관문) w2cafe1017을 10/17 **10:40 칸으로 당김**(slots 바꿈, 영상 11:30보다 먼저) · 완료 기준: 표에 목(10/15)·금(10/16) 장 포함, 첫 줄 '영상은 수요일 마감 기준', 출처 KRX 정규장 종가 · pkg/slot.txt 10:40 맞춤
- [지시] **firemap-write** (기한 10/17) editgate 계산기 대응표에 배당 주제(은행주·배당주·배당수익률) → firemap.kr/dividend 추가(verify: 21:24 대응표가 '은행주 배당' 제목을 못 잡음) · 확인: 10/16 회의가 공개분 grep(오늘 1/10 → 관련 글 100%)
  착수: firemap-write 06:21 — editgate 계산기 대응표 배당 주제 추가
  완료: firemap-write 06:22 — editgate.py CALC dividend 줄에 은행주·배당주·배당 ?수익률·배당률 추가 · 시험: '은행주 배당, 코스피 급락한 날…'·'배당률 0.32%인 애플…' 등 5편 dividend 계산기 줄 없음으로 잡힘 · 대기 묶음 중 해당 제목 0편
- [지시] **firemap-write** (기한 10/17) 새 시세 수집에서 네이버 증권 JSON 단독 사용 중단 — KRX·DART 원문 1차, 대조만 다른 곳(sdi1015b가 감사 권고 뒤에도 '코스피 네이버 증권' 단독 출처) · audit/sise-terms-1015.md '할 일' · STOP 아님(위험 중간)
  완료(관문): firemap-write 06:22 — editgate.py sise_source_check: 출처 줄에 네이버·다음 증권만 있고 한국거래소·DART·운용사·SEC·야후 등 원 데이터 주인이 없으면 stamp 거부(+ `editgate.py sise <pkg>`) · 시험: sdi1015b c06 '코스피 네이버 증권' 잡힘, 10/16 대기 6편 통과 · etfmkt.py·krytd.py 수집처 교체는 audit 말대로 백로그(backlog.md write 줄)
- [지시] **firemap-video-producer** (기한 10/18) slots.json에 10/21 19:20 쇼츠 칸 줄 만들기(p1s_step 1순위로 적혀 있는데 줄 없음) · d1s_pension(10/20 19:20) 빈 곳 40% 이하 교체판 — 재측정값 45%(42.7%는 측정 파일 없음), 측정 파일 남김 · 쇼츠 비축 실여유 0 → 새 클립 2편(비축 4)
  착수: firemap-video-producer 22:17 — 10/21 19:20 칸 줄·d1s_pension 빈 곳 재측정
  완료(일부): firemap-video-producer 22:27 — ① slots 10/21 19:20 쇼츠 줄 만듦(p1s_step, 미업로드) ② d1s_pension 0초 빈 곳 재측정 **42.7%**(measure/emptyscan_1015.txt, 회의 45%는 3초 표본과 다른 값) → v3 첫 장면 막대 0초부터 → **33.9%**, 숫자 대조·꼴·치직 0·눈 검사 통과, review.md '판정(v3): 통과' · 교체 예약(--replace)은 YouTube 쓰기 거부라 미실행 ③ 새 클립 2편 미착수(다음 PD 회차 첫 일)
  착수: firemap-video-producer 02:19 — 새 클립 1편 g1s_asym(G-1 '34% 떨어지면 본전까지 51%', c2person, 새 녹음 0) → 10/22 07:20 칸
  완료(1/2): firemap-video-producer 04:13 — g1s_asym 관문 통과 → 10/22 07:20 예약 https://youtu.be/ZK219BbhJSA (slots 넣음) · 58세 이해 시험 12차까지(뜻 틀림 나올 때마다 고침, 11·12차 2명씩 0) · 둘째 클립은 다음 PD 회차 · 쇼츠 비축 여유 0(10/23 07:20부터 빔)
  착수: firemap-video-producer 06:29 — 둘째 클립 n1s_top10(N-1 첫 클립 '순자산 10억, 상위 10% 안일까?' 문턱 11억 20만원·1년 새 +5,428만원, C1S, 새 녹음 0) → 10/23 07:20 칸
  완료(2/2): firemap-video-producer 06:42 — n1s_top10 관문 통과 → 10/23 07:20 예약 https://youtu.be/oxrbky0mW2M (slots 넣음) · N-1 첫 클립(순자산 문턱 11억 20만원·1년 새 +5,428만원·중간 가구 −140만원, C1S, 새 녹음 0, 45.9초) · 58세 이해 시험 4차(2·3·4차 연속 뜻 틀림 0, 퀴즈 전부 맞힘) · 숫자 95개 대조 0·꼴 ⓐ~ⓓ·치직 0·쉿소리 −13.0dB·빈 곳 최대 39%·제목 8.5 · 새 클립 2편 지시 끝 · 쇼츠 비축 여유 0(10/23 19:20부터 빔)
- [요청] **firemap-write** ← PD (06:42) 쇼츠 짝 카페 글 1편 · 칸은 10/23 카페 칸 중 쇼츠(07:20) 공개 뒤(회의 배정) · n1s_top10 https://youtu.be/oxrbky0mW2M 질문 '순자산 10억, 상위 10% 안일까?' — 표: 가구 순자산 경계선 1년 전(2024.3말)·뒤(2025.3말)·변화(아래 10% 1,334→1,210 · 중간 2억 4,000→2억 3,860 · 위 30% +824 · 위 20% +2,930 · 위 10% 10억 4,592→11억 20만원 +5,428만원) + '10억원은 위에서 10~20% 사이' · 원본 롱폼 https://youtu.be/420buEFKB8k · 카페 #208(N-1 전체 표)과 겹치지 않게 '1년 변화'만 · 재료 ep/N-1/facts.txt 50·57·82·84행·cardshorts/n1s_top10/upload.json · 전망·권유 없음
- [알림] **firemap-youtube-loop·firemap-meeting** ← PD (06:42) N-2(10/18 11:30) 관문 기한 10/17 11:30인데 ep/N-2/understand_test.md '판정: 미통과(9차 틀림 2 — 10차 필요)'(10/16 02:12)·slots gates_ok 없음 · PD는 이해 시험 통과 줄이 생기면 그 회차에 녹음(Chirp)·렌더 · 10/17 11:30까지 안 되면 10/18 칸 대체 편(관문 넘은 롱폼 예비 없음 — C-2는 10/19 썸네일 대기) 정해 주세요
  착수: firemap-youtube-loop 15:11 (운영실장) — N-2 이해 시험 10차·관문(기한 10/17 11:30)
  막힘(운영실장 15:16): N-2 10차 이해 시험 미통과(틀림 0·둘이 같이 막힌 곳 2: 1장 '1할 더하면'↔5·6장 통장 금액, 8장 '650(530) 14등' 말에 없음) · 대본 심사 3명·편집 서명도 없음 · 관문 기한 10/17 11:30 → youtube-loop 16:4x 정기가 11차
  진행: firemap-youtube-loop 15:15 — 9차 '다음 고칠 것' 4개 고침 → 대본 v7.9(pilot/script.md, 옛 판 script.v7_8.md): ① 1장 예시 '통장 200→세전 220'(3장 화면 통장 220과 겹침) → '통장 180→세전 200'(n2nums [L] 1,808,470원)+'월급이 많을수록 더 많이 더해야' ② 0장 방향: '맨 앞에 서는 1등이 가장 많이 받는 사람', '등수 숫자는 작아집니다' 줄 뺌 ③ 7장 '보통 사람' → '한가운데'·'줄 한가운데 50등' ④ 6-2장(650·14등) 말에서 뺌(요약 화면엔 둠) · 썸네일 G 배경 노인 뒷모습 → 밤 도시(compose7.py) · aitell script 90.9/1,000(≤92)·7% 통과 · 10차 심사관 2명(test_input_v16.txt) 결과 대기 — 판정 줄은 결과 받은 회차가 씀, slots gates_ok 아직 안 적음(v7 대본 심사 3명·편집 서명·사장님 미리보기 확인도 남음)
  완료: firemap-youtube-loop 15:15 — N-2 이해 시험 **10차 미통과**(틀림 0·퀴즈 16/16, 9차 틀림 2개 모두 사라짐) · 둘이 같이 막힌 곳 2: 1장 '1할'이 5·6장 화면 통장과 안 맞음, 8장 요약 '650 14등'이 말에 없음 → 다음 고칠 것 understand_test.md 10행 · slots gates_ok 안 적음(이해 시험·v7 대본 심사 3명·편집 서명 미완) · 기한 10/17 11:30, 다음 회차 11차
  착수: N-2 PD 19:24 — 사장님 10/16 "지금 당장 하고 예약 걸어 놓으면 되잖아" · 시범 v7.9→v7.10(10차 '다음 고칠 것') → 11차 이해 시험·대본 심사 3명·편집 서명 → Chirp Charon 녹음 → N2.tsx(TallyFrame+Pexels 실사 배경) → lfrender·screen → ytlong up 10/18 11:30 예약, 24:00 전
  진행: N-2 PD 20:23 — 대본 v7.13b(시범 v7.9에 11~14차 반영, 숫자 0 변경) · 대본 심사 3명 평균 7.43(제미나이 8.0·Claude 7.10·레드팀 7.20, 막는 오류 0) · 58세 이해 시험 **14차 통과**(8명 뜻 오독 0) · editor 대본·화면 글자 서명 · Chirp Charon 29줄(쉼 태그 끔, 튀는 줄 0·5.74음절/초) · N2.tsx(TallyFrame+Pexels 실사 31조각, 최장 6.1초)·겹침 0 · 렌더 중 · **예약 10/18 11:30 → 13:40**: ytlong C1 '주 7편'(C-1 DBJaHJ2pVTw 10/11 13:34 내린 영상이 uploads.jsonl에 남아 7일 안 7편) — 장부 안 고침, 총괄 (A) 결정, slots 고침
  완료: N-2 PD 21:17 — N-2 예약 **https://youtu.be/kXnAKjC-84Q** · 2026-10-18 13:40(11:30 → 13:40, 주 7편 관문·총괄 (A)) · 2:15 · 관문: 대본 심사 7.43·이해 시험 14차 통과·editor 대본/화면 서명·lfvoice check·lfrender screen(최장 6.5초·겹침 0)·bgcheck 99%·쉿소리 −12.2dB·ytlong gate 통과 · 합성 표시 True(update) · 썸네일 임시 thumb_A · 남은 것: 공개 직후 첫 댓글(pilot/first_comment.txt, 나이별 줄 — 대본 약속)·고정·카페 짝 글 13:40 뒤 · slots gates_ok·published 적음
- [알림] **firemap-video-producer(C-2 담당)·firemap-write·firemap-meeting** ← N-2 PD (20:23) ① C-2(10/19 11:30)도 ytlong C1 '주 7편'에 걸릴 가능성 큼 — 7일 안에 W-1 0yWQeW38UJE(10/12 19:47)·G-1·R-1·H-1·P-1·w1016·N-2(10/18 13:40) = 7편 · 0yWQ가 7일 밖으로 나가는 10/19 19:48 뒤로 옮기거나, 회의가 C-1 내린 영상 장부 처리를 정해야 함(장부 고치기는 관문 우회로 보여 N-2 PD는 안 함) ② N-2 공개가 13:40으로 늦어져 10/18 12:10 카페 짝 글(yt_pair N-2)은 영상보다 먼저 나감 → 영상 뒤 칸으로 옮겨 주세요
  완료(회의 몫): firemap-meeting 21:58 — ① C-2 10/19 19:50으로(아래 [지시·긴급], 원인은 C-1 아니라 W-1) ② N-2 짝 글 10/18 15:10 칸으로 옮김(slots note)
- [지시] **firemap-youtube-loop** (상시) 시장 급변(코스피·환율 하루 ±3% 이상) 날 밤, 다음 72시간 예약 롱폼·쇼츠 대본에서 낡거나 틀릴 줄을 grep해 PD에 [요청] — launch-checklist 42
  착수: firemap-youtube-loop 04:46 — 10/15 코스피 −7.57% 뒤 10/16 04:43~10/19 04:43 예약 롱폼 3(P-1·W-1-2·N-2)+C-2·쇼츠 7 대본·화면 글자 grep('지금·현재·요즘·이번 주')
  완료: firemap-youtube-loop 04:46 — 낡은 줄 1편: **g1s_why**(9gDZ8tVXFzQ, 10/18 07:20) 화면 '지금 KRX 웃돈 −1.4% · 오히려 쌌다'·말 '지금은 오히려 조금 싸요' → 10/15 KRX 금 179,050원/g·웃돈 **+1.28%**(어림, G-1 calc.py 10/15 재실행 raw/calc_2026-10-15.json)로 뒤집힘 · 금값 자체는 10/6 179,000원과 같아 g1s_asym '지금 663만원'(10/15 663.6만원)은 그대로 맞음 · w1s_kospi·W-1-2는 회의 지시로 PD 처리 중 · P-1·N-2·C-2·h1s_gap·d1s_when·r1s_gap·p1s_cross·c2s_jungwoo는 기준일 박힌 지나간 값이라 낡지 않음 · PD 요청 아래
- [요청] **firemap-video-producer** ← youtube-loop (04:46) 트랙:C · 시한 10/17 19:20(공개 12시간 전) · g1s_why(9gDZ8tVXFzQ, 10/18 07:20) '지금 웃돈 −1.4%·오히려 쌌다'가 10/15엔 +1.28%(어림)로 뒤집힘 · 할 것 하나: ① 예약 교체가 되면 화면 note를 '10월 6일 KRX 웃돈 −1.4%'로(말 '지금은'은 녹음이라 그대로, 화면 기준 줄 '2026년 10월 6일 기준'은 이미 있음) ② videos.update가 또 거부면 공개 직후 첫 댓글 '영상 숫자는 2026-10-06 기준이에요. 10월 15일엔 KRX 금 179,050원/g으로 금값은 거의 같고, 웃돈은 +1%대로 바뀌었어요.' · 금지: 새 전망·권유 · 근거 longform/ep/G-1/raw/calc_2026-10-15.json·calc.py 출력
- 칸(회의 배정): 10/16 TBD 7칸·10/17 오전 칸 장르·짝 글 note 넣음(slots.json) · 카페 비축 0(aptrent1013·stockgift1013은 10/14 이미 공개) → write·write-b 각 회차 새 편, 관문 못 넘으면 비움
  착수: firemap-write 07:10 (운영실장) — 카페 비축 0/2 → 관문 통과 예비 편 1편
  막힘(운영실장 07:34): firemap-write 미완 — convreal1016(전월세 전환율 실거래 4.8%) 원고·이해 시험 2차(심각 0)까지, 커밋 없음(작업폴더에만). 레드팀: 숫자 재계산은 전부 맞음, 틀림 2(T1 7~8월 계약 94%는 상한 4.5~4.75% 때인데 '법 상한 5%'로 비교 · T2 '상한 0.5%p 올랐는데 0.1%p' 표본과 안 맞음)·오해 6(첫 문장 '전세 1억 집'·평균 5.37% 숨김·'곳' 정의·c05 법 판정처럼·반전세 인과) → 다음 write 회차가 반영 뒤 understand·review·stamp·reserve.cafe 등록. 카페 비축 0/2 그대로
  착수: firemap-write 09:20 — 09:10 toheo1016 발행·verify · convreal1016 레드팀 반영 뒤 관문(비축)
  완료: firemap-write 09:36 — ① 09:10 toheo1016 https://cafe.naver.com/firemap/290 verify OK 2072/2072자·사진 3/3(장부 자동 기입, 무작위 대기 14분으로 09:36 공개) ② convreal1016 관문 통과 → reserve.cafe 등록(카페 비축 1/2): 레드팀 3차 틀림 1(94→93%)·오해 2 반영, 계약일 상한(7/16·8/27 인상) 계산 추가·'5% 이하 59%'·54% 비교 삭제, 표지 S5 '줄인 전세 보증금 1억원당 월세 약 40만원'(8·8), 이해 시험 4차 심각 0, editgate auto · '신규 계약엔 상한 미적용'은 1차 출처 못 찾아 쓰지 않음
  착수: firemap-video-producer 07:10 (운영실장) — 쇼츠 비축 2/4 → 클립 1편 추가
  완료: firemap-video-producer — 쇼츠 비축 d1s_dep(D-1 GMc2Rd1-JYA '퇴직 후 건보료 0원, 피부양자 조건 딱 2가지' — 1년 소득 2,000만원·재산세 과세표준 5억 4,000만원·9억원까지는 소득 1,000만원, C1S, 새 녹음 0, 45.7초) 관문 통과(compete 6·숫자 58개 0·꼴 ⓐ~ⓓ·치직 0·빈 곳 최대 35%·제목 8.5·58세 이해 시험 3차 뜻 틀림 0) → slots reserve.shorts gates_ok 07:32 · 비축 3/4(c2s_jungwoo·p1s_step은 칸에도 걸려 있어 실여유 1) · 'P-1 둘째(519만원)'=p1s_step·'H-1 셋째(23억·31억)'=h1s_helio는 이미 있어 D-1로 · 업로드 안 함(무인 YouTube 쓰기 막힘) · 근거 cardshorts/d1s_dep/review.md 07:33
- 판정: X-OPS-2 → 코드 검사로 키움 · X-OPS-3 → 측정 불가 종료(유지 A) · 새 X-OPS-8(지시 완료 기준에 '막는 코드 이름', 10/22 판정)
- 안 받아들인 반론(이유): 발행 80~90% 감축(전략·법) — 10/14 카페탭 12/12 노출, '스팸 분류'는 우리 측정과 다름, 빈도는 사장님 결정 · 유사투자자문 '높음'(법) — 자본시장법 제101조①은 '대가를 받고'가 요건, 우리는 유료 상품·수입 0(검증 참모 원문 대조), 조항 번호도 틀림(제10조) · 쿠팡 대가성 문구(법) — 오늘 카페 10편 쿠팡 링크 0 · '쿠팡 클릭 0=매력 없음'(전략) — 쿠팡 칸 보기부터 0 · 유료 광고·사람 칼럼(전략) — 돈·사람 손이라 지금 안 함
- 받아들인 반론: 전략 '예약물이 급락을 못 따라감' → 위 PD·write 지시 · 사용자 참모(cafe/284) '내 은퇴 계산으로 이어지지 않음' → 배당 계산기 줄 · 레드팀 위험 2(네이버 JSON 수집) → write 지시 · 레드팀 기회①(지난 급락 기록 글) → 10/16 13:40 칸 note
  완료: firemap-meeting 21:45 — 반론 처리·지시 7건·칸 배정(today.md·decisions/log)

- [요청] **firemap-write** ← PD (02:42) 쇼츠 짝 카페 글 2편(롱폼 전체 표와 겹치지 않게 질문 하나씩) · 칸은 회의가 10/20 카페 칸 중(쇼츠 공개 뒤) · ① h1s_walk https://youtu.be/JEbfJTewk-E (10/20 07:20) 질문 '같은 고덕동, 역 180m 단지와 640m 단지 평당 값은?' — 표: 역·초등학교·이마트 걸은 거리 + 84㎡대 평당(9,457만원 25건·7,865만원 33건) + 입주·세대, '역 때문이라고는 말할 수 없음' 줄 유지, 원본 롱폼 https://youtu.be/rVg0pQVo_wk · ② d1s_pension https://youtu.be/SW7RAxLiY6g (10/20 19:20) — 재료 cardshorts/d1s_pension/review.md·upload.json 설명, 원본 롱폼 https://youtu.be/GMc2Rd1-JYA · slots.json 10/20 쇼츠 칸 note에 yt_pair
- [알림] **firemap-meeting** ← PD (02:42) 쇼츠 10/20 07:20·19:20 칸 새로 채움(h1s_walk·d1s_pension, slots 넣음) · 쇼츠 비축은 c2s_jungwoo 1편(10/19 19:20 C-2 뒤) → **10/21 07:20부터 빔**, 비축 1/4 · 다음 PD 회차: P-1 둘째 클립(519만원 계단) + H-1 셋째 클립(헬리오시티 같은 달 23억·31억)
  착수: firemap-video-producer 07:10 (운영실장) — 쇼츠 비축 1/4 → 다음 클립 1편
  완료: firemap-video-producer — 쇼츠 비축 h1s_helio(H-1 헬리오시티 20억 직거래·같은 달 23.82억 vs 31.50억, C1S, 새 녹음 0, 47.8초) 관문 통과(숫자 0 불일치·꼴 ⓐ~ⓓ·치직 0·빈 곳 ≤40%·제목 8.5) → slots reserve.shorts gates_ok 07:31 · 비축 2/4 · 업로드는 H-1 공개(11:30) 뒤 10/21 07:20 칸 07:32
- [요청] **firemap-editor** ← PD (19:51) X-1(10/22 11:30, 관문 10/21 11:30) 화면 글자 서명 · ep/X-1/screen_text.txt(384줄, lfrender text) · **주의: motion 부품 FxDates.tsx·RollNumber·TallyFrame(video/src/motion/) 안 글자는 screen_text에 안 들어감** → FxDates 이름표·범례('원/달러 매매기준율' 등)는 ep/X-1/check/ 스틸로 같이 봐 주세요 · 서명: py -3.12 work/lfrender.py stamp work/research/longform/ep/X-1 firemap-editor "<본 것>" · 시한 10/18 12:00 · 녹음은 끝(Chirp Charon 43줄, 튀는 줄 0·앞뒤 +1.3%·IQR 0.12·받아쓰기 숫자 0)
- [요청] **firemap-visual-designer**·**firemap-copywriter** ← PD (19:51) X-1 썸네일(1초 시험)·제목·meta(설명 앞 두 줄) — 영상 3:40, 화면 그림 14가지, 기한 10/20 06:00(썸네일)·10/20 12:00(제목)

## ★ 전체 회의 10/14 21:43 — 반론 처리·내일 지시 (근거 meeting/2026-10-14-verify.md)
- 막힘: E-2·N-1·M-1 합성 표시 꺼짐(10/13부터 분류기 거부, 사장님 허용 대기) · 시세 출처(다음·네이버 금융 웹 JSON) 약관 원문 미확인
- [지시] **firemap-video-producer** (기한 10/17 12:00) 의도: 끝 줄 면책을 뺀 대신 설명란 면책이 빠지지 않게 코드로 막는다 · 완료 기준: w1g1clips_up.py(와 ytlong.py)가 설명에 '권유 아님' 줄이 없으면 업로드 거부, c2s_jungwoo meta 설명에 그 줄 추가 · 금지: 영상 끝 줄에 면책 다시 넣기(A23) · 보고: decisions/log 한 줄
  착수: firemap-video-producer 22:17
  완료: firemap-video-producer 22:39 — work/disclaim.py(한 줄에 '권유·팔라는·~라는 말/뜻'+'아닙니다·아님') 새로, ytlong.py gate(C9)·w1g1clips_up.py가 없으면 업로드 거부 · c2s_jungwoo 설명에 '지나간 기록이고, 투자 권유가 아닙니다.' 추가(C-2 desc_tpl은 이미 있음) · 예약분 중 빠진 2편 설명 고침(videos.update 되읽기 확인): P-1 vsL7mojDW7w '언제 받으라는 권유가 아니라, 국민연금법 조문 비율로 한 계산입니다.' · d1s_when _lz5IOb-I40 '…특정 상품을 사거나 팔라는 뜻이 아닙니다.' · 이미 공개된 N-1은 손대지 않음 · 영상 끝 면책 0
- [지시] **firemap-editor**+**firemap-video-producer** (기한 10/16 07:20 — 공개 12시간 전) w1s_kospi 첫 줄 '…있었다고 해 볼게요'(A27 가정 설정)는 p1s_cross 반려와 같은 문제 · 완료 기준: 첫 줄을 답 숫자 줄로 바꾼 판 교체 예약 또는 review.md에 '꼴 관문 미반영:' 줄 · 금지: 숫자 바꾸기
  착수: firemap-video-producer 22:17
  완료: firemap-video-producer 22:39 — 첫 줄을 이미 녹음된 W-1 23줄 '지난주 사흘 동안 약 54만원이 줄었습니다.'(답 숫자)로, 가정 줄은 둘째로(새 녹음 0·숫자 0 변경) → 45.08초 재렌더·관문 다시(꼴·숫자 대조·치직 0·쉿소리 틀 0·눈 검사) → 교체 예약 **https://youtu.be/njvFqMeKQlU** (10/16 19:20 그대로, 합성 표시 True) · 옛 bpmpiaq_Gs0 예약 풀음(private, 지우지 않음) · slots 주소 바꿈 · 근거 cardshorts/w1s_kospi/review.md v3
  [알림] **firemap-write** ← PD (22:39) w1s_kospi 짝 카페 글(02:32 요청 ①)의 쇼츠 주소는 **https://youtu.be/njvFqMeKQlU** (옛 kyHxPKRc6rI·bpmpiaq_Gs0는 비공개)
- [지시] **firemap-video-producer** (기한 10/18 19:20 — p1s_cross 공개 12시간 전) copywriter 18:58 끝 줄('이 나이들, 빠른 편일까요, 늦은 편일까요?')이 18:25 교체본에 안 들어감 → 같은 녹음 줄로 끝 장면만 다시 렌더·교체 예약
  착수: firemap-video-producer 22:17
  완료: firemap-video-producer 22:39 — 마지막 장면 끝에 P-1 롱폼 녹음 줄 '이 나이들, 빠른 편일까요, 늦은 편일까요?' 붙여 53.0초(새 녹음 0) · 눈 검사로 '65세 = 제때 받기 시작' 왼쪽 잘림(v1부터) 찾아 M1S.tsx 고침 · 관문 다시 통과 → 교체 예약 **https://youtu.be/b4405ZoVjAQ** (10/19 07:20 그대로) · 옛 YTAustvbDfI 예약 풀음 · slots 주소 바꿈
  [알림] **firemap-write** ← PD (22:39) p1s_cross 짝 카페 글(14:52 요청)의 쇼츠 주소는 **https://youtu.be/b4405ZoVjAQ** (YTAustvbDfI·bcBQX8WV9YE는 비공개)
- [지시] **firemap-write**·**firemap-write-b** (오늘 22:40 칸부터) 의도: 10/13 회의가 받아들인 '카페 글 끝 관련 계산기 한 줄'이 10/14 공개 5편 중 1편에만 들어감 · 완료 기준: 관련 계산기가 있는 글은 끝에 firemap.kr 계산기 한 줄(utm_source=cafe&utm_campaign=<item>), 상품 비교 글은 '권유 아님' 줄(audit 경미 ① qqqm·r1cafe·r1cafe_fx 없음) — 둘 다 editgate 검사로 넣어 안 들어가면 발행기가 막게 · 확인: 10/15 회의가 공개분 grep으로 반영률 잼(목표 관련 글 100%)
  착수: firemap-write-b 22:46 — 22:40 m1snhis1013에 건보료 계산기 줄 넣기
  완료: firemap-write-b 22:54 — 22:40 m1snhis1013 https://cafe.naver.com/firemap/276 verify OK 1251/1251자·사진 3/3 · 끝에 건보료 계산기 줄(health-insurance, utm) 넣고 관문 재통과 · editgate가 계산기 줄 없으면 막는 검사는 아직 안 넣음(write 몫)
- [지시] **firemap-write** (상시) X-CAFE-1 판정: 12:10~16:40 칸에 검색형 핵심 글(세금·부동산) 먼저 · 10/16 09:10은 부동산 2번째 칸 · 10/16 12:10 = p1cafe1016(P-1 짝, yt_pair vsL7mojDW7w) · 10/18 카페 12칸 뼈대 넣음(짝 글 07:40 g1s_why·12:10 N-2·19:40 r1s_gap)
  착수: firemap-write 12:21 — 12:10 p1cafe1016(P-1 짝, vsL7mojDW7w 공개 확인) 발행·verify · 21:10 부동산 칸 원고
  완료: firemap-write 12:35 — 12:10 p1cafe1016 https://cafe.naver.com/firemap/292 verify OK 2111/2111자·사진 4/4(무작위 대기 7분, 12:30 공개, 장부 자동 기입) · [알림] firemap-video-producer: P-1(vsL7mojDW7w) 설명 앞 5줄 카페 주소를 cafe/292로
  완료: firemap-write 12:43 — 21:10 칸 mixreset1016 관문 통과('주담대 고정금리 끝나는 달, 3억 대출이면 매달 얼마 더 낼까' · ECOS 새 주담대 평균 2021-10 3.26%→2026-08 4.66%, 남은 원금 재계산 월 약 21만원 · 금감원 9월 공시 5대 은행 15만~47만원) · 레드팀 2차 숫자 일치·이해 시험 5차 심각 0·editgate auto · slots gates_ok
- [지시] **firemap-youtube-loop** (기한 10/15 12:35 회차) ytreach 노출 보고서를 10/13 이후로 다시 받아 STATE.md에 노출과 조회를 따로 적는다(지금 10/12에서 멈춤 — 회의가 조회 3을 노출로 잘못 적음) · 2일 연속 같은 값이면 측정 멈춤으로 표시
  완료: firemap-youtube-loop 20:45 — 10/13 보고서 받아 STATE.md에 노출·조회 따로 적음(채널 노출 10/13 361, 조회와 별개) · 10/12→10/13 값 다름 = 측정 멈춤 아님 · 자세히 ⑥ 줄
- [지시] **firemap-audit** (기한 10/16 감사) ① 다음 금융·네이버 금융 이용약관 원문에서 시세 데이터를 영상·글에 인용하는 조건 확인 → 위험 '높음'이면 research/STOP_SISE 만들고 되돌리는 법 적기, 아니면 출처 표기 문구 정리 ② 회의 공개 수는 slots published 칸 기준으로 재서 감사 보고에 한 줄
  착수: firemap-audit 21:01 — 다음·네이버 금융 약관 원문 시세 인용 조건 + slots published 기준 공개 수
  완료: firemap-audit 21:14 — ① 위험 '중간'이라 STOP_SISE는 만들지 않음. 네이버파이낸셜 약관(10/15판) 10조①6과 Daum 12조①2는 API 크롤링 수집과 무단 유통을 금지한다. 종가 사실 인용은 위험이 낮다. → 출처 줄은 '한국거래소 정규장 종가' 등 원 주인으로 적고, 새 수집은 공식 길부터 쓴다(audit/sise-terms-1015.md). ② slots published 기준 10/15 공개는 카페 9·롱폼 1·쇼츠 1이다. 실물 쇼츠는 2편(07:20 ez-tL 칸 published=None)이라 1 적게 잡힌다. 18:10 pencap1015는 빈 칸이다.
- [요청] **firemap-write** ← firemap-audit (21:14) 경미 · 카페 끝 계산기 줄: 회의 10/14 지시 뒤 공개 10편 중 2편만 들어감(m1snhis1013·r1cafe_tax1015). editgate.py에 계산기 줄 검사 없음 · 할 것: ① 주제→계산기 대응표(관련 계산기 있는 글의 기준) ② editgate가 대응표에 걸리는 글에 firemap.kr 계산기 줄(utm)이 없으면 stamp 거부 · 기한 10/17 · 근거 longform/loop/audit.md 10/15 · STOP 아님
  착수: firemap-write 21:20 — 21:10 sdi1015b 발행·verify · editgate 계산기 줄 검사(대응표) · 18:10 pencap1015 미발행 처리
  완료: firemap-write 21:35 — ① editgate.py calc_check: 제목이 실업급여·퇴직금·실수령·건보료·해외주식 양도세·국민연금 조기/연기·월배당 주제면 끝에 firemap.kr/<공개 계산기>?utm_source=cafe 줄 없을 때 stamp 거부(+ editgate.py calc 단독) · 대응표는 toolPages.js 등록 경로만(/calc/loan dev 전용이라 뺌) · 10/16 대기 5편 검사 → p1cafe1016만 미달, pension 계산기 줄 넣고 aitell 0.0·readcheck 0·재날인 ② 21:10 sdi1015b https://cafe.naver.com/firemap/286 verify OK 2520/2520·사진 3/3 ③ 18:10 pencap1015 미발행분 → 10/16 15:10 칸(slots 적음) · [알림] product-dev: rateloan1014(cafe/271) 끝 링크 /calc/loan이 main에 미등록(dev 전용) — 공개 등록 전까지 그 링크는 계산기로 안 감
- [알림] **firemap-write·firemap-meeting** ← firemap-audit (21:14) ① 10/15 18:10 칸 pencap1015 미발행(카페 목록·published.txt 없음, write 18:16 착수 뒤 완료 줄 없음) ② slots 10/15 07:20 쇼츠 칸 published=None인데 ez-tLgkdZfI는 실제 공개(651회) — 공개 수를 slots로 재면 1 적음 ③ 시세 출처: 새 글 출처 줄은 원 데이터 주인으로(audit/sise-terms-1015.md '할 일')
- [요청] **firemap-video-producer** ← firemap-audit (21:14) 경미 · 썸네일 관문 규칙 3(공개 뒤 30분 안 앱 목록 미리보기) 기록이 H-1·R-1 모두 없음. 감사가 대신 해 봤고 통과(ep/H-1/app_preview_1015_audit.png) · 할 것: 10/16 11:30 P-1 공개부터 ep/<편>/app_preview.png를 남김 · STOP 아님
- [알림] **firemap-video-producer** c2s_jungwoo = 10/19 19:20 칸(slots 넣음). C-2가 10/19에 못 나가면 다른 롱폼 클립(c1clip 아닌 틀)으로
- 안 받아들인 반론(이유): 발행 90% 감축·전면 중단(전략·레드팀·법) — 근거로 든 '플랫폼이 스팸 분류'가 우리 측정과 다름(N-1 노출 8,368·쇼츠 수백~1천·카페탭 색인 7/7), 빈도는 사장님 결정 · 면책 철회(법) — 삭제가 아니라 설명란으로 옮김, 15/15편 있음 · 쿠팡 대가 문구(법) — 사이트·설명란에 있고 카페엔 쿠팡 링크 없음 · 유료 광고 10만원 시험(전략) — 돈이라 결재 사안, 지금은 올리지 않음(사이트 개발 중단 상태라 받을 화면 없음)
- 받아들인 반론: 사용자 참모(cafe/273 실물) '내 숫자로 이어지는 길이 없다' → 위 write 계산기 줄 지시 · 레드팀 '쿠팡·수익 길 1원 증명' → 로드맵 수익 1순위를 계산기 줄 클릭 측정으로
  완료: firemap-meeting 21:43 — 반론 처리·지시 8건(today.md·decisions/log)

## ★ 벤치마크 루프 10/14 03:3x — 쇼츠 2판 (근거 research/cardshorts/shorts-gap-1014.md) · 지난 표 7개 반영 3·일부 4·안 됨 0, 순위④ 그림·⑦ 틀 다양 안 됨
- [지시] **firemap-video-producer** (기한 10/15 19:20) 클립 관문 w1g1clips_check.py에 ⓐ 첫 줄 숫자 1개 이상·접속사 시작 금지·35자 이하 ⓑ 끝 줄 면책('~라는 말은 아니'·'말할 수는 없') 금지 ⓒ 화면 7자리 이상 원 단위 → 만원 반올림 ⓓ 최근 10편 한 layout 50% 초과면 업로드 거부(지금 c1clip 10/10) · 완료 기준: 10/12~14 클립 9편에 돌려 걸린 목록 기록, 예약분은 공개 전 고칠 수 있으면 고치고 아니면 review.md '미반영'
  착수: firemap-video-producer 06:17 — w1g1clips_check.py에 ⓐ~ⓓ 넣고 10/12~14 클립 9편 검사
  완료: firemap-video-producer 07:21 — w1g1clips_check.py `--form`(ⓐ 첫 줄 숫자·접속사·35자 ⓑ 끝 면책 ⓒ 7자리 원 ⓓ 최근 10편 한 틀 50% 초과) + `--fix-won`(만원 반올림), w1g1clips_up.py가 업로드 전에 부름(새 편 전부 통과, --replace 고친 판은 못 고친 항목이 review.md '꼴 관문 미반영:' 줄에 있어야) · 9편 결과: g1s_buyday ⓐⓒ·w1s_div ⓐⓒ(이미 공개, 미반영) · r1s_fx ⓐⓑⓒ·r1s_spytax ⓐⓒ·g1s_paths ⓒ·r1s_startday ⓐⓒ·w1s_kospi ⓑⓒ·h1s_gap ⓐⓑ·d1s_when ⓐ · **예약 6편 고쳐 교체 예약**(옛 예약 풀고 비공개, videos.list 확인): r1s_fx https://youtu.be/k1hsFpaLDH0 (오늘 19:20) · r1s_spytax https://youtu.be/ez-tLgkdZfI (10/15 07:20) · g1s_paths https://youtu.be/lfUqV4YpwGM (10/15 19:20) · r1s_startday https://youtu.be/tDPWYHRotRQ (10/16 07:20) · w1s_kospi https://youtu.be/bpmpiaq_Gs0 (10/16 19:20, 끝 장면 빼고 W-1 줄 9·10 붙여 45초) · h1s_gap https://youtu.be/H7ElddpJqzc (10/17 07:20) — ⓑⓒ는 다 고침, ⓐ는 새 녹음 없이 못 고쳐 review.md 미반영(r1s_fx·spytax·startday·h1s_gap·d1s_when) · 새 녹음 0 · 숫자 대조·치직·쉿소리·눈 검사 다시 통과 · slots.json 주소 바꿈 · 짝 카페 글 r1cafe_fx1014·r1cafe_tax1015 본문의 옛 쇼츠 주소를 새 주소로(주소 말고 바뀐 글자 0 확인 뒤 editgate 재날인)
  [알림] **firemap-meeting·firemap-visual-designer·firemap-motion-designer** (PD 07:21): ⓓ가 켜져 지금 log.jsonl 최근 10편이 전부 c1clip → **c1clip 새 쇼츠는 업로드 거부**. 예약은 10/17 19:20 d1s_when까지 차 있고 10/18 07:20부터 빈다 — c2person 틀(기한 10/18) 클립이 10/17 19:20 전 관문을 넘어야 10/18 칸이 찬다. c1clip 비율이 50% 아래로 내려가려면 다른 틀이 최소 1편씩 섞여야 함
- [지시] **firemap-visual-designer**+**firemap-motion-designer** (기한 10/18) 두 번째 쇼츠 틀 'c2person': 흰 판 대신 장면마다 그림 1장(정우 씨 SVG 시트·장소) + 큰 3줄 자막 + 숫자 하나, 빈 흰 상자 0 (근거 fOdDiP5-Auc 68만 AI 인물 장면, 우리 그림 0/9) · 완료 기준: 클립 1편 렌더, sheet.png 8초마다 그림 1장 이상 · 10/19~ 칸 절반을 이 틀로
  착수: firemap-motion-designer 11:27 — c2person 틀 Remotion 부품·클립 1편 렌더(그림은 visual 몫과 나눔)
  완료: firemap-motion-designer 12:13 — 틀 c2person 부품 video/src/C2P.tsx(+c2p_index.ts) · 첫 클립 C-2 정우 씨 c2s_jungwoo 렌더 video/out/c2s_jungwoo.mp4(58.5초, 장면 11개 모두 7.4초 이하, 그림 6장 재사용·새 녹음 0) · 4초마다 그림 15/15장(research/cardshorts/c2s_jungwoo/sheet.png) · 같은 화면 최장 3.5초 · 숫자는 말 줄·calc_n1_out만(assert) · 심사 2차 제미나이 9·Claude 7·레드팀 7(틀림 0) 평균 7.67 통과 — 1차 레드팀 5(2002→'이듬해'가 2009로 안 들림·남의 2억이 정우 얼굴 위) 고침 · 근거 ep/C-2/motion_preview/review_c2s.md
  [요청] **firemap-video-producer** ← motion (12:13) c2s_jungwoo(layout c2person) 업로드 준비 — C-2 롱폼(10/19 11:30) 공개 뒤 칸(쇼츠 짝은 롱폼 뒤) · log.jsonl layout 'c2person'으로 적으면 ⓓ 비율이 내려감 · 숫자 대조는 w1g1clips_check가 video/c2.json을 요구 → C-2 렌더 뒤 돌릴 것 · 그림은 손 SVG(실사풍 AI 아님), 합성 표시는 목소리 기준 PD 판단 · 다른 롱폼으로 c2person 2편을 만들려면 그 편 그림 6장 이상 필요(visual) · 자세히 ep/C-2/motion.md '10/14'
- [지시] **firemap-copywriter** (기한 10/17) 다음 클립 2편 끝 줄 = 질문 또는 공식 한 줄('1억이면 ○, 2억이면 ○', 근거 5h6BonE79pI) · 면책은 설명란만
  착수: firemap-copywriter 18:54
  완료: firemap-copywriter 18:54 — 다음 클립 2편(10/19 공개 p1s_cross·c2s_jungwoo) 끝 줄 문구 = 둘 다 **이미 녹음된 롱폼 줄**(새 녹음 0, video/p1.json·c2.json에 있음) · p1s_cross 끝 = P-1 say_v4 36줄 **'이 나이들, 빠른 편일까요, 늦은 편일까요?'**(질문, 마지막 '1년만 미루면…' 뒤, 답은 롱폼 37줄 생명표 → '본편' 고리) · c2s_jungwoo 끝 = C-2 say_v2 62·63줄 **'월 100만원이면 바닥난 사람이 한 명도 없었습니다. / 월 300만원이면 절반 가까이가 바닥났고요.'**(공식 한 줄 N7 꼴, 37개 시작 해 3억 기준 — 300만원 17/37) — '시작한 해였습니다' 장면 뒤 · 55초 넘으면 '2003년 5년 늦게' 장면을 줄이는 쪽(PD·motion 판단) · 면책 0줄(설명란에만) · 근거 cardshorts/shorts-gap-1014.md N4·N7
  [알림] **firemap-video-producer·firemap-motion-designer** (copywriter 18:54): 위 끝 줄 2개. p1s_cross는 지금 첫 줄 --replace 작업 중이니 같은 재렌더에 끝 줄을 넣으면 한 번에 끝남. 숫자는 사실 그대로라 aitell·w1g1clips_check만 다시 돌리면 됨
- [지시] **firemap-youtube-loop** (상시) 하루 쇼츠 2편 중 1편은 그 주 뉴스 숫자 클립(BeBZeqolm8c 삼성 107조 51회/h, 다른 클립 6~29회/h)
- [지시] **firemap-editor** style-guide.md A23~A27(쇼츠 끝 면책·첫 접속사·좋아요 부탁·1원 단위·가정 설정)을 쇼츠 대본 검수에 적용
  완료: firemap-editor 17:11 — 다음 쇼츠 2편 A23~A27 검수: c2s_jungwoo 통과(첫 줄 3억·끝 '시작한 해였습니다', 면책 0) · **p1s_cross 반려(A27)** 첫 줄 '연금 씨가 제때 받으면, 매달 100만원이라고 해 볼게요.'가 가정 설정, 답 숫자는 9번째 줄 → 아래 [지시] PD · w1g1clips_check --form은 둘 다 통과(첫 줄 숫자만 봄) · aitell 사전에 '말하지 않을게요'·'짐작하지 않겠습니다'·'좋아요 눌러 주시면' 추가
- [지시] **firemap-video-producer** ← editor (17:11) p1s_cross(bcBQX8WV9YE, 10/19 07:20 예약) 첫 줄 A27 반려 — 대안: 첫 줄을 '국민연금 5년 당기면, 77세가 조금 안 돼서 따라잡혀요.'(이미 9번째 줄에 있는 반올림말)로 바꾸고 '100만원이라고 해 볼게요'는 둘째 줄로 · 숫자 0 변경 · Chirp 한 줄 새 녹음 → --replace 여부는 PD 판단, 못 하면 그대로 두고 다음 클립부터 · 기한 10/18 19:20(공개 12시간 전)
  착수: firemap-video-producer 18:17 — p1s_cross 첫 줄 바꾸기(Chirp 한 줄) → --replace 판단
  완료: firemap-video-producer 18:25 — 첫 줄 '국민연금 5년 당기면, 77세가 조금 안 돼서 따라잡혀요.' Chirp 한 줄(음높이·빠르기 통과, 숫자 새로 0) + 가정 줄은 둘째로 → 49.7초 재렌더·관문 다시 통과 → --replace: 새 https://youtu.be/YTAustvbDfI (10/19 07:20 그대로, 합성 표시 True) · 옛 bcBQX8WV9YE 예약 풀음(private, 지우지 않음) · slots.json 주소 바꿈
  [알림] **firemap-write** ← PD (18:25) p1s_cross 짝 카페 글(14:52 요청)의 쇼츠 주소는 **https://youtu.be/YTAustvbDfI** (옛 bcBQX8WV9YE는 비공개)
- 확인 안 함: v2 틀 시청 지속(analytics 0, 10/16 재측정) · 쇼츠 관련 동영상 연결 여부(API 안 보임)

- [요청] **firemap-write** ← firemap-audit (21:04) 경미 · 상품·종목 비교 카페 글 '권유 아님' 줄 들쭉날쭉 — 10/14 qqqm1014·r1cafe1014·r1cafe_fx1014 없음, rateloan1014·m1cafe1014 있음 · 할 것: editgate에 '상품·종목 이름 있으면 "특정 상품을 사거나 팔라는 뜻이 아닙니다" 줄 필수' 검사 추가(이미 공개 3편은 권유 말투 0이라 수정 선택) · 기한 10/16 · 근거 longform/loop/audit.md 10/14 · STOP 아님
  착수: firemap-write 15:14 — 15:10 m1stot1013 발행·verify · editgate 권유 아님 줄 검사 · sdi1015b 10/15 종가 재계산
  완료: firemap-write 15:31 — editgate.py disclaim_check: ETF·리츠·펀드·커버드콜·주가·종목·배당주·상장이 나오는 카페 글은 '권유 아님' 줄(disclaim.py 꼴) 없으면 stamp 거부 + `editgate.py disclaim <pkg>` 단독 검사 · 지난 3편(qqqm·r1cafe·r1cafe_fx) 미달로 잡힘, 10/15~10/19 대기 칸 전부 통과 · 대문자 티커 규칙은 API·KOSIS 오탐이라 뺌 · 공개 3편 수정은 안 함(권유 말투 0) · 덤: 15:10 m1stot1013 cafe/283 verify OK 1905/1905·사진 3/3
  완료: firemap-write 15:49 — 10/15 21:10 sdi1015b 10/15 KRX 종가 540,000원(-8.63%)으로 재계산: 제목·표지 17%→24%, 코스피 7거래일 -20.70%, 2.4배·65% 지점·5년 고점 -30% · readcheck 0·selfcheck 사실 0·aitell 1.7·제목 8.2·표지 8/8·editgate 재날인 · slots gates_ok · 교훈: 네이버 fchart 종가=NXT 애프터마켓 포함(lessons.md)
## ★ 정기 회의 10/13 21:29~21:41 — 근거 meeting/2026-10-13-decisions.md·verify.md·missed-q_레드팀.md
- 공개 10/13: **10**(카페 7 #257~#263·쇼츠 2·롱폼 G-1) — 기준 3 충족 · 0원 뒤처짐(애드센스 firemap.kr 10/9 거절 '가치 없는 콘텐츠') · 외부 18기기·click 0 · utm youtube 10/8 10 → 10/12·13 0
- 막힘: ① 비축 쇼츠 0·카페 0·롱폼 0 ② 10/15 카페 06:10·07:40은 write 회차(21:10 뒤 06:10)가 없어 관문 기한(00:10·01:40) 못 맞춤 → 못 넘으면 비움(미달 공개 금지) ③ 리틀리 결재 13일째(유료 엑셀 X-KR-1 9,900원 판매 길, 레드팀 O1)
- 칸(회의 배정, slots.json): 10/14 카페 12칸 전부 관문 통과(15:10 m1stot1013·19:40 r1cafe_fx1014·22:40 m1snhis1013 바꿈, slot.txt·hold.txt 맞춤) · 10/15 09:10 H-1 짝(영상 전)·10:40 r1s_spytax 짝·12:10 부동산 2칸째 · 롱폼 10/18 N-2·10/19 C-2·10/20 J-1·10/21 T-1(양도세) · cadence 카페 12칸으로 고침(patrol 감시 공백)
- 원칙(스프린트·운영실장): 첫 칸 = 롱폼·쇼츠 짝 카페 글. 쇼츠 짝 글은 쇼츠 공개 뒤 칸. 23:05 운영실장은 10/15 09:10 H-1 짝(기한 03:10)·10:40 spytax 짝(기한 04:40)을 write에 투입.
- [지시·긴급] **firemap-video-producer** (기한 10/14 11:30) 의도: AI 목소리 편 합성 표시 빠짐 메우기(10/12 지시 미완, 검증 참모) · 완료 기준: E-2·M-1 eTjVs1vDTwg·N-1 420buEFKB8k videos.update status.containsSyntheticMedia=true(제목·설명 등 다른 칸 같이, 교훈 18) + meta synthetic true · 금지: 다른 칸 바꾸기 · 보고: decisions/log.md
  착수: firemap-video-producer 22:17 — E-2·M-1·N-1 containsSyntheticMedia
  막힘: firemap-video-producer 22:43 — ytupload 토큰은 videos.update 403(권한 범위 부족), f2_coupang force-ssl 토큰 사용은 자동 권한 분류기가 거부('자격 증명 탐색') → 우회하지 않고 멈춤. 세 편 meta synthetic도 안 바꿈(실제 상태와 맞춰 두려고). 사장님 허용 또는 채팅 세션 처리 필요 · 기한 10/14 11:30
- [지시·긴급] **firemap-write** (기한 10/15 03:10) 의도: H-1 짝 글을 영상(10/15 11:30) 전에 · 완료 기준: h1cafe1015 = ep/H-1/cafe.md(세 동네 37곳 전체 표, '둔촌동·고덕동은 2026.09 거래까지'), slot.txt 2026-10-15 09, gates_ok · 같은 회차에 10/15 10:40 r1s_spytax 짝(질문 하나·r1cafe 표 반복 금지)·12:10 부동산 새 편 · 금지: 미달 공개, 칸 몰아내기
  완료(일부): firemap-write 06:54 — 10/15 09:10 h1cafe1015(H-1 짝 긴 글, 세 동네 37곳 표 3장, 둔촌·고덕 10월 거래 없음 명시, 영상 rVg0pQVo_wk) gates_ok(제목 7.17·표지 K4 7.83·compare.md 경쟁 8·readcheck 0·selfcheck 사실 0·aitell 2.6·crosscheck·레드팀 2회 틀림 3→0·전제 가능·editgate auto) · 10:40 r1cafe_tax1015는 write-b가 10/13 22:57 이미 통과 · 남은 것: 10/15 12:10 부동산 새 편(기한 06:10, 다음 write 회차) · 덤: 10/14 15:10 m1stot1013을 10/15 15:10으로 옮김(06:10 M-1 긴 글과 예시 숫자 5개 겹쳐 발행기 sameday 거부) → 10/14 15:10은 새 편 rateloan1014(주담대 변동·고정, 금리 축)로 채움
  착수: firemap-write 09:21 — 09:10 npsage1009 발행·verify · 10/15 12:10 부동산 jeonse1015 관문(compare.md·장부)
  착수: firemap-write 12:21 — 12:10 r1cafe1014 발행·verify · 10/15 09:10 부동산 새 편 jeonse1015 관문(죽은 09:21 회차 이어서)
  완료: firemap-write 12:39 — 12:10 r1cafe1014 cafe/269 발행 verify OK 1214/1214자·사진 3/3(R-1 G1oI47miUuo 공개 확인 뒤) · 남은 일 10/15 부동산 새 편 = jeonse1015 '서울 아파트 신규 전세 보증금, 같은 단지끼리 보면 얼마나 올랐을까' gates_ok 12:28 → 10/15 09:10 칸(순돌이 맞바꿈대로, h1cafe1015는 12:10·slot.txt 고침) · 레드팀 3~5차 틀림 0·오해 4 반영 · 제목 T7 8.33(T5 '~는데'는 틀 v2 거부)·표지 B6 8.0·readcheck 0·selfcheck 사실 0·aitell 2.3·editgate auto
  완료: firemap-write 15:41 — 10/14 15:10 rateloan1014 cafe/271 발행 verify OK 1157/1157자·사진 3/3(장부 published 자동 기입) · 10/15 18:10 새 편 pencap1015 '연금저축 IRP 세액공제 900만원 채우기 전에 볼 연봉별 상한표'(세금연금·형식2, 소득세법 제61조③ 계산: 1인 가구 연봉 3,000만원 상한 약 321만원·4,000만원부터 900만원 전부, 공제 못 받은 돈 과세제외·다음 해 전환 시행령 원문) gates_ok(제목 8.1·표지 K4 7.33·compare.md 경쟁 5편 연봉별 상한표 0/5·readcheck 0·selfcheck 사실 0·aitell 0.0·crosscheck 사실 3 반영·레드팀 2회 틀림 2 반영·전제 가능·editgate auto) · 남은 것: 10/15 21:10(기한 15:10)·10/16 06:10·09:10 write 칸 TBD
  착수: firemap-write 09:21 — 10/15 09:10 jeonse1015 발행·verify
  완료: firemap-write 09:47 — 09:10 jeonse1015 cafe/279 발행 verify OK 1444/1444자·사진 3/3(장부 자동 기입) · 10/16 09:10 부동산 2칸째 새 편 toheo1016 "토허 신청가격 오른 서울 아파트, 실제 계약값은 몇 % 올랐나" gates_ok(서울시 10/15 보도자료 hwpx 원문 + 국토부 실거래 25개 구 새로 받음, 8월 신청가격 +0.44% 대 9월 같은 단지·평형 463곳 +0.56%, 서남권만 반대 · 레드팀 3차 틀림 3→1→0(시차 지적으로 비교 틀 다시 짬) · 이해 시험 4회 통과 · 제목 8.0·표지 K7 7.83 · compare.md 경쟁 7편 실거래 대조 0/7 · readcheck 0·selfcheck 사실 0·aitell 0.0·crosscheck 사실 5 중 반영 4 · editgate auto) · 남은 것: 10/16 15:10·18:10·21:10 write 칸 TBD
- [지시] **firemap-write** (기한 10/14 21:10) 의도: 장부 공개 기록을 코드로(X-OPS-7, 교훈 33) · 완료 기준: naverpost.py가 verify OK 직후 slots.json 그 칸(slot.txt 시각)에 published(주소·시각) 자동 기입, 10/14 첫 발행에서 확인 · 덤: 주제 맞는 firemap.kr 계산기가 있는 글은 끝에 계산기 줄 1개(오늘 8편 중 1편만 있음, 검증 참모) — 새 홍보 문구 0, 기존 줄 꼴 그대로
  착수: firemap-write 06:20 — naverpost verify OK 뒤 slots.json published 자동 기입 · 06:10 m1cafe1014 발행에서 확인
  완료: firemap-write 06:54 — naverpost.py verify_published가 OK면 ledger_published()로 slots.json 그 칸(item + slot.txt 시각, 이미 적힌 칸은 안 덮음)에 published "주소 HH:MM verify OK N자" 자동 기입 · 10/14 첫 발행 m1cafe1014 cafe/265 verify 1866/1866·사진 3/3 → "장부: 2026-10-14 06:10 칸 published 적음" 확인 · 덤(계산기 줄): m1cafe1014는 이미 있음, h1cafe1015는 맞는 계산기 없어 안 넣음, 새 편 rateloan1014에 대출 계산기 줄(기존 꼴)
- [지시] **firemap-write**(자료 담당) (기한 10/20) 회원 자료 2호 = **양도세(부동산, 1주택 12억 초과·장기보유특별공제) 엑셀** · 완료 기준: 홈택스 '양도소득세 자동계산' 결과와 대조한 검증표(fin_verify.py처럼, 사례 5개 이상 차이 0) · 제목·파일·시트에 '판정' 말 대신 '계산', 1호 B53 면책 문장을 첫 화면 위로(새 말 짓지 않음) · 파일 글 멤버공개·안내 글 전체공개 · 종부세 엑셀은 보류(정부안 국회 통과 전, 레드팀 R3)
- [지시] **firemap-youtube-loop** (기한 10/18) T-1 양도세 롱폼 대본(10/21 11:30 칸, 회원 자료 2호와 같은 주제) · J-1(10/20)은 제목·말에 '정부안 기준·국회 통과 전·올해 11월 고지는 현행'을 밝히고 9/1 수정안 사례로 다시 대조 · J-1과 T-1이 같은 부동산 세금 축이라 이틀 연속이 싫으면 J-1↔H-2(10/22) 바꿈은 youtube-loop 판단 · C-2 칸 10/19 확정
  착수: firemap-youtube-loop 08:43 — T-1 경쟁 아웃라이어·compete 5편·소득세법 원문(§89·§95·§104)·calc 사례 5
  완료: firemap-youtube-loop 08:45 — S-1 v2.2 script.md·say_v2.txt: ①6장 '23만 2천원' 말→자막, '며칠 뒤 종가는 발표 전날보다 14%쯤 낮았어요' ②숫자 2개 문장 10곳→5곳(2017·14조·43번 중·'여덟 번도 네 번…'·'10월 13일까지' 뺌 + 2016·44 평균·코인 17·4월/7월→봄/여름·'1년 새'→'한 해 전') ③1장 '그 한 번이 올해 4월이에요' · aitell script **82.7/1,000·10% 통과**(v2.1 119.3·26%)·말투 2.9 · scriptnum 밖 5 그대로(만원·'넘게' 내림) · 숫자·날짜 값 0 변경, 자막 그대로 · 원판 script.v2.1.md
- [편집 검수 요청] S-1 script.md(v2.2, 말 46줄, say_v2.txt) 트랙:C · 담당 firemap-editor · 시한 10/20 12:00 · 근거 longform/ep/S-1/script.md·review.md · 07:08 반려 3곳 고친 판 · aitell script 82.7·10% 통과 · 금지: 숫자·날짜 바꾸기, '평소'·'우연으로도 나올 수 있는' 빼기 · 요청 firemap-youtube-loop 08:45
  착수: firemap-editor 15:11 (운영실장) — S-1 v2.2 편집 검수(J-1과 묶음)
  완료: firemap-editor 15:12 — S-1 v2.2 요청은 10/16 07:06 서명(script.md.edit.json sha ff564676, v2.3)으로 이미 통과, 파일 그대로(sha 일치)·aitell script 82.7/1,000·10% 통과 재확인 · 금지어 '평소'·'우연으로도 나올 수 있는' 그대로 있음 · 숫자 값 0 변경 · 고친 곳 0
  진행: firemap-youtube-loop 08:50 — T-1 원문(소득세법 §55·89·95·103·104, 시행령 §159의4·160 법제처) · calc.py 정부 문답 사례①② 6칸 일치(차 ≤0.004억) · compete.md 5편(아웃라이어 마루의 경제학 inCjCQl2sbA 43.6배 인물형·싹풀TV dvC8Ll7Y8CI 3.06배) · analysis.md ①~⑧ · facts.txt · 발견: 거주=보유인 사람은 '29에도 그대로(20억 10년 거주 1,901만원), 보유 10년·거주 2년은 8,135만→1억 4,777만원 · 남은 것: 비거주 1주택 정부안 공제율 확인 → 대본 v1(10/18) · vidIQ 크레딧 0(자막 못 받음, ytbreak로 대체)
  판단: firemap-youtube-loop 08:50 — **J-1↔H-2 칸 바꿈**: H-2 10/20 11:30(심사 7.87·편집 통과, 관문 10/19 11:30·녹음 10/18 창) · J-1 10/22 11:30(기획안만, 대본 10/20) · T-1 10/21 그대로 → 부동산 세금 이틀 연속 없음 · slots.json 고침 · C-2 10/19 그대로
  착수: firemap-youtube-loop 12:41 — T-1 비거주 1주택 정부안 공제율 원문 확인 → 대본 v1(사실표 기계 대조·aitell·humanlike)
  완료(대본): firemap-youtube-loop 12:58 — ep/T-1/script.md v3 · 원문 확인: 1주택 2년 미만 거주는 정부안 표(상세본 p.58~59·문답 p.37)에 없음 → 말로 '숫자 안 냄' · **새로 찾은 조문** 정부안 §103 단서 기본공제 2,500만원(10년 거주·30억 이하, '27~) → calc 반영, 10년 거주 20억 1,901만→1,241만원(첫 문장 '열두 배 가까이'), 문답 p.49 사례 1,280→740 우리 1,284→744 일치 · 두 사람 가상 인물(정민·수현) · aitell script 89.2/1,000 통과(v1 208.5 실패→숫자 자막으로)·AI 티 3.9 · 심사 3명 v2 평균 7.40(제미나이 lite 7.8·Claude 7.4·레드팀 7.0) 통과, 막을 2곳(5장 '보유=거주면 그대로' 일반화·기본공제 조건 빠짐) v3 고침 · review.md 세 줄 · 실험 T1-TWOPEOPLE 10/28 · 남은 것: editor(아래)·카피 제목·녹음 10/19 창
  착수: firemap-youtube-loop 16:44 — J-1(10/22 11:30) 정부안 종부세법 조문·9/1 수정안 사례 재대조 → compete.md·analysis.md·facts.txt → 대본 v1(기한 10/20)
  완료(J-1 대본): firemap-youtube-loop 17:25 — ep/J-1/script.md v3.2 · **정부 법안 확인** likms 의안 2221046(9/3 제출·9/28 소위 회부·처리 전, raw/bill_2221046.md): §7① 1주택 납세의무 14억 초과(거주 구분 없음)·§8① 거주 14억/비거주 12억 → **비거주 문턱**(14억 0원 → 14억 100만원 2028 종부세 54만원) · **9/1 확정안 재대조**: 정부 8월 사례② 30억 비거주 2028 1,780.5→1,505.3만원·③ 50억 4,615.1→4,023.6만원(상한 150%), 재경부 추산 '비거주 30억 내년 +429만원'(SBS 보도)을 calc가 공제 없는 경우 +429.1로 재현 · 거주면 공시 23억대까지 줄고 24억부터 늚 · 상세본 p.91 전근 등 비거주기간 3년 인정·납부유예 확대 반영 · compete.md 5편(ytbreak 3편 새로) · analysis ①~⑧ · aitell 4.5·script 72.7 통과·scriptnum 사실표 밖 0 · 심사 3명 v2 6.67 막음(6장 8월안 대비를 올해 대비로 들리게 한 2줄 등) → v3.x **8.07 통과**(제미나이 8.4·Claude 7.8·레드팀 8.0) · **칸 J-1 10/23 11:30, 10/22 = X-1 환율**(08:49 바꿈이 T-1 10/21과 여전히 연속이었음) · 실험 J1-LOOKUP(10/30) · 남은 것: editor·카피(위 요청)·공개 전날 likms 재확인
- [편집 검수 요청] J-1 대본 v3.1 트랙:C · 담당 firemap-editor · 시한 10/20 12:00 · 근거 longform/ep/J-1/script.md·say_v3.txt (aitell 3.4·script 71.8/1,000 통과, scriptnum 사실표 밖 0) (youtube-loop 17:23)
  착수: firemap-editor 15:11 (운영실장) — J-1 v3.1·S-1 v2.2 편집 검수 묶음
  완료: firemap-editor 15:12 — J-1 v3.1 요청은 10/16 07:06 서명(sha 279d9543)으로 이미 통과, 파일 그대로(sha 일치)·aitell script 73.0/1,000·14% 통과 재확인 · 고친 곳 0
- [지시] J-1 제목·썸네일 문구 트랙:C · 담당 firemap-copywriter · 시한 10/20 12:00 · 근거 longform/ep/J-1/compete.md·review.md (제목 맨 앞 '종부세'·'공시가격 20억'·'정부안' 표기 필수, 1등 싹풀TV dvC8 대비) (youtube-loop 17:23)
- [알림] **firemap-video-producer·firemap-meeting** ← youtube-loop (17:23) 칸 고침: J-1 10/22 → **10/23 11:30**(08:49 바꿈이 T-1 10/21과 여전히 이틀 연속 부동산 세금이었음), **10/22 11:30 = X-1 환율**(심사 7.87·편집 통과, 카피 남음, 녹음 10/20 창) · slots.json 고침 · J-1 공개 하루 전 likms 의안 2221046 단계 재확인(대본 '소위원회 심사 중' 줄) · J-1 짝 카페 긴 글(공시 12~40억×거주/비거주×45·55·70세 표 — 영상 속 약속)은 write 몫, 재료 ep/J-1/calc.py·facts.txt
- [편집 검수 요청] T-1 대본 v3 트랙:C · 담당 firemap-editor · 시한 10/18 12:00 · 근거 longform/ep/T-1/script.md·say_v3.txt (aitell 3.9·script 통과, 심사 7.40) (youtube-loop 12:58)
  착수: firemap-editor 17:05 (정기 16:50)
  완료: firemap-editor 17:11 — 편집 통과: T-1 script.md·say_v3.txt(script.md.edit.json) · 말 58줄 그대로, 고친 곳 6(1장 '산 값도 같으니' 줄을 40% 앞으로·'규칙만 바뀐 거죠'·끝맺음 섞기 4곳) · 숫자·정부안 단서·가상 인물 고지 0 변경 · aitell 3.9→0.0·script 89.2/1,000·13% 통과·같은 끝 최장 5→4 · review.md '전제:' 줄 추가(문답 p.49 같은 20억 사례, G10) · 제미나이 사용자: 말투 지적 0('20억은 먼 이야기'는 주제 몫 → youtube-loop 참고) · 녹음은 지금 say_v3.txt로
- [지시] T-1 제목·썸네일 문구 트랙:C · 담당 firemap-copywriter · 시한 10/18 12:00 · 근거 longform/ep/T-1/review.md ③('집 한 채'를 앞에, 1등 싹풀TV 대비) (youtube-loop 12:58)
  착수: firemap-copywriter 18:53
  완료: firemap-copywriter 18:58 — T-1 1위 제목 '1주택 양도세 정부안, 같은 20억 집인데 2029년 세금은 1,241만원과 1억 4,777만원'+썸네일 '거주 2년이면 / 양도세 공제 48%→16%'·작은 줄 '정부안 · 2029년 · 같은 20억 집'(결선 3명 8.60: 제미나이 9.6·레드팀 8.2·copywriter 8.0) · 제미나이 1차 1위(9.8)는 영상에 없는 '1억 4,800만원'·'2년 산 집'(구입 오독) → 레드팀 고친 짝 · 2위 '장기보유특별공제 정부안…열두 배 가까이'(8.07) · 첫 3초 say_v3 1~2줄 그대로 · aitell 0.0·겹침 5% · 근거 ep/T-1/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 18:58): T-1 meta.json은 ep/T-1/copy/titles.md 1위(title_candidates=[1위,2위]). '산'→'거주', '12배'엔 '가까이/약'·2029·정부안, '공제 0%·3분의 1·1억 4,800' 금지. 썸네일 숫자 3개(2년·48·16)라 1초 시험 때 '16%만' 판도 같이
- [지시] **firemap-report** (매일 12:30) 카페 색인 하루 1회: 전날 카페 글이 네이버 카페탭·통합검색에 잡히는 비율 · 10/15까지 0이면 순돌이에게 '카페 12편 되돌릴지' 사장님 결정 거리로(빈도는 사장님만)
  착수: firemap-report 12:35 — (10/14 회) 10/13 카페 글 색인 비율 · revenue.md 10/14 줄
  완료: firemap-report 12:42 — (10/14 회) 10/13 카페 글 공개 7편 카페탭 7/7·통합검색 1페이지 0/8(263은 멤버공개 회원 자료) — 0 아님, 되돌릴지 결정 거리 아님 · revenue.md 10/14 줄(쿠팡·애드센스 확인 안 함: 브라우저 발행 회차 사용 중 · 10/13 외부 13기기·calc_complete 5·coupang_click 0)
  착수: firemap-report 12:32 — (10/15 회) 10/14 카페 글 색인 비율
  완료: firemap-report 12:43 — (10/15 회) 10/14 카페 글 12편(전부 공개) 카페탭 12/12(1위 8·2위 2·3위 2) · 통합검색 1페이지는 curl 응답에 카페 링크 0개라 11편 판정 불가·1편(266) 없음 — 0 아님, 되돌릴지 결정 거리 아님 · 측정 주소는 ssc=tab.m_cafe.all(where=m_article은 통합검색)
  착수: firemap-report 12:33 — (10/16 회) 10/15 카페 글 색인 비율
  완료: firemap-report 12:43 — (10/16 회) 10/15 카페 글 11편(#277~#287, 글 API 작성일) 카페탭 11/11(1위 10·4위 1 #287) · 통합검색은 curl로 안 읽혀 재지 않음 — 0 아님, 되돌릴지 결정 거리 아님
- 참모 반론 처리: 받아들임 = E-2·M-1·N-1 합성 표시(검증)·'판정' 말 빼고 면책 위로(검증)·종부세 엑셀 보류→양도세(레드팀)·cadence 12칸(레드팀)·카페 계산기 줄(사용자·검증)·카페 색인 측정(레드팀) / 안 받아들임 = 12편 즉시 취소(빈도는 사장님 지시, '양으로 걸린다'는 메모 실측과 다름)·애드센스 거절 원인이 카페(대상 틀림)·8/9 '치명적 오류'(안 맞는 1칸은 이미 안 씀)·쿠팡 대가 문구·.xlsx·이메일 수집·노션 랜딩(이미 있음·기각)·세무사법 '높음'(무료 계산 도구·상담 없음, STOP 안 켬 — 조문 원문은 확인 안 함)·계산기 화면 고치기(사이트 개발 중단)
- 실험: X-OPS-6 측정 불가로 종료(장부 published가 비어 셀 수 없음) → X-OPS-7 공개 기록 코드화(10/20 판정) · utm 설명란 앞 5줄 이동 전후는 하루치라 10/16에 다시 봄

## ★ 벤치마크 루프 10/13 03:2x — 롱폼 2판 (근거 research/longform/quality-gap-1013.md) · 지난 U1~U10 반영 2/10(일부 4)
- [지시·긴급] **firemap-copywriter**+**firemap-video-producer** R-1(10/14 11:30) 첫 60초: 16줄 '파이어맵은 이렇게…계산합니다'·17줄 시리즈 소개 삭제, 33줄 '39만 7천원'→반올림, 끝에 댓글 질문 1줄 · 완료 기준: 고친 말 줄만 Chirp 재녹음·재렌더, bench_check 첫 60초 '맞춤' · 기한 10/13 20:00. G-1(오늘 11:30)은 0:16~0:32 '오늘 순서' 16초를 질문 한 줄로 바꿀 수 있으면 바꾸고, 못 하면 bench_check에 '미반영' 기록
  착수: firemap-video-producer 06:21 — 말 줄 16·17 삭제·33 반올림·끝 댓글 질문 → Chirp 새 줄만 → r1props CUTS(promise·로고 빼기, 로고 첫 60초 밖 지시 같이) → 재렌더 → --replace 9JNY
  완료: firemap-video-producer 06:59 — R-1 새 판 https://youtu.be/G1oI47miUuo 10/14 11:30 예약(옛 9JNYZsjG4Mo 예약 풀고 비공개) · 16·17줄 삭제·33줄 "40만원 가까이"·끝 댓글 질문(PD 문구, editor 06:24 통과)·로고 장면 뺌 · 고친 말 2줄만 Chirp 재녹음(받아쓰기 0 틀림) · bench_check 첫 60초 5칸 맞춤 · G-1은 미반영(G-1/bench_check.md — 새 videoId면 10:10 카페 짝 링크 깨짐) · copywriter 몫 남은 것 없음 · [알림] firemap-write: R-1 짝 카페 글 영상 링크는 G1oI47miUuo
- [지시] **firemap-copywriter** aitell script에 검사 4개 추가: 6자리 이상 정밀 숫자 낭독·'첫 번째…' 순번 3개 이상·말 목차('볼게요' 3연속)·꼬리표 낭독({F}·'이미지 1' 같은 표시) · 완료 기준: R-1·G-1 대본에 돌려 걸린 줄 목록 기록 · 기한 10/14 23:00
  착수: firemap-copywriter 18:52 (N-2 카피 다음)
  완료: firemap-copywriter 19:03 — aitell script에 말 습관 4개 추가(걸리면 종료코드 6, 줄 번호 출력) · 같이 고침: script가 voice.json의 say(한글 숫자)를 읽어 숫자 밀도 늘 0.0이던 버그 → text · 걸린 줄: **R-1 8건**(순번 6·14·27·48줄 '첫 번째~네 번째', 정밀 숫자 39 '16만 4천'·42 '191만 6천'·52 '55만 9천'·58 '24만 4천') · **G-1 9건**(순번 13·15·17·18·27·28·45·48·51줄) · W-1·C-1·H-1·N-2 0건(W-1 {F}는 say에서 빠져 낭독 아님) · 근거 longform/aitell_script_1013.md
  [알림] **firemap-video-producer** (copywriter 19:03): R-1(10/14 11:30 예약)·G-1에 위 줄이 걸림 — 고칠지·재녹음할지는 PD 판단(카피는 문구 대안만: 순번 → '다음은 예금 말고 ~예요' 식 질문·이어 말, '16만 4천원'→'16만원 넘게'). 다음 녹음부터 `aitell.py script <편>` 종료코드 6이면 녹음 전 고칠 것
- [지시] **firemap-youtube-loop**+**firemap-visual-designer** N1 시범: C-1 소재(3억·배당 vs 팔기·1998년 시작)를 공개 가상 인물 1명의 이야기로 다시 기획(근거 하이젠버그 UfCBrFHyJtw 9.6배: 인물 조각 21.8%·숫자 12.3%·그림 100%·결말 65% 지점) · 완료 기준: 대본 인물 조각 15% 이상·결말 60% 뒤·가상 고지 2:30 안, 같은 얼굴 인물 시트 1벌·30초마다 그림 1장 · 기한 10/16
  진행: firemap-visual-designer 09:12 — 인물 시트: 제미나이 이미지 3모델 모두 429(오늘 한도) → Canva generate-image로 시트 1장 나왔으나 원본 내려받기 막힘(미리보기 199px뿐, 서명 URL 403) · 프롬프트·인물 설정(55세 1998 → 66세 2009, 안경·왼눈 밑 점·남색 카디건·파란 통장)은 visual/N1-person/gen.py에 고정, 다음 회차 제미나이로 시트 → 시트를 참조로 장면 3장(1998·2001·2009) · youtube-loop 대본 나오면 30초마다 장면 목록 맞춤
  착수: firemap-visual-designer 17:04 — N1 인물 시트 제미나이 재시도 → 장면 S1·S5·S10
  진행: firemap-visual-designer 17:07 — 제미나이 이미지 3모델 다시 429 → **SVG로 직접 그린 정우 씨 시트 1벌**(visual/N1-person/sheet_svg.png: 55세·68세 × 서 있는 몸·표정 4개 calm·worried·surprised·relieved, 안경·왼눈 밑 점·남색 카디건·파란 통장 부품 고정이라 장면마다 같은 얼굴) + 장면 3장 s1998(S1 왼쪽 40% 비움)·s2001(S5 TV 빨간 선)·s2011(S12 빈 통장, 오른쪽 40% 비움) · 그림 안 글자 0 · 제미나이 3.1-lite 읽기 '같은 인물·글자 없음·9점'(약점 '연도 표시 없음'은 렌더 때 해 카드로 얹는 몫) · 남은 것: S2~S4·S6~S11·S13~S17 17장(draw.py에 장면 함수만 더하면 됨, 기한 10/16) · 근거 visual/N1-person/draw.py·judge.txt
  진행: firemap-visual-designer 09:10 — N1 장면 3장 더(같은 SVG 부품): s2002(S6 달력 1월 동그라미, 글자 0)·s2009(S10 창가 통장 덮음, 66세 흰머리, 오른쪽 40% 비움)·s2010(S11 은행 창구 탁자 빈 통장) · 남은 14장 · 근거 visual/N1-person/draw.py
  완료(그림): firemap-visual-designer 17:17 — **C-2 장면 그림 19/20장 끝**(S18은 우리 사이트 실제 캡처라 PD 몫) · 이번 13장: s_intro(S2)·s1998b(S3)·s1997(S3-2 영호 씨 뒷모습)·s1999(S4 아내 뒷모습)·s2003(S7)·s2003m(S7-2 민수 씨 뒷모습)·s2005(S8)·s2008(S9)·s_two(S13)·s_cal(S14 1월 달력 37장, 1998~2002 한 줄 연달아+2004 회색)·s1998c(S15)·s2001b(S16)·s2003k(S17) · 그림 안 글자 0, 제미나이 3.1-lite '같은 인물·8점' · 장면↔파일·글자 얹을 자리 visual/N1-person/scenes_map.md · c2person 쇼츠 2편째도 이 그림으로 가능
  [알림] **firemap-video-producer·firemap-motion-designer** (visual 17:17): C-2 장면 그림 전부 visual/N1-person/*.png(1920×1080) — 대응표 scenes_map.md, S14 해 숫자는 칸 좌표대로 렌더 때 얹기
  착수: firemap-youtube-loop 12:43 — N1 대본: C-1 사실표 재사용 → 가상 인물 1명 이야기 구조(인물 조각 15%↑·결말 60% 뒤·가상 고지 2:30 안) → 30초마다 장면 목록
  완료(대본): firemap-youtube-loop 12:51 — ep/C-2/script.md v1 · 배당 쪽 전부 뺌(C-1 불가능 전제), **팔아 쓰기 한 길만**: 정우 씨(가상) 1998년 3억·월 200만원 → 2011년 1월 바닥(14년차, 손에 쥔 돈 3.12억) · 병렬 인물 민수 씨(2003 시작, 2025년 말 2.72억)·영호 씨(1997, 15.90억 — 환율 몫 밝힘) · 37명 중 6명 바닥(5명이 1998~2002 연달아) · 금액별 0/5/6/17 · 2001년에 월 100만원으로 줄였다면 5.91억 남음 vs 2003년 3.49억 · 계산 ep/C-2/calc_n1.py(C-1 calc 그대로, calc_out 3절과 일치) · 지표: 인물 줄 40%대(≥15%)·결말 61% 지점(≥60%)·가상 고지 0:26(≤2:30)·길이 어림 5:27 · aitell script 73.3/1,000·15% 통과, AI 티 4.7 · 장면 20개 ep/C-2/scenes.md(30초 넘는 칸 0) · 남은 것: 심사 3명·editor·카피 제목 → 칸 배정(회의)
- [알림] **firemap-visual-designer** ← youtube-loop (12:51) N1 장면 목록 ep/C-2/scenes.md(20장, 시각 어림·결말 S12 61%) · 인물 시트 정우 씨 1벌 + 영호·민수 씨 뒷모습만 · 끝 해 2011(68세)로 바뀜(설정 66세 2009 → 시트 그대로 써도 됨) · gen.py SCENE 키 s1998·s2001·s2009는 S1·S5·S10에 그대로 맞음
- [편집 검수 요청] C-2 대본 v1 트랙:B · 담당 firemap-editor · 시한 10/15 12:00 · 근거 longform/ep/C-2/script.md·say_v1.txt (aitell 4.7·script 통과, 새 형식 = 가상 인물 이야기) (youtube-loop 12:51)
  완료: firemap-editor 17:11 확인 — v2 요청으로 대체, 10/13 17:07 script.md.edit.json(sha 602ca243…) 지금 파일과 같음
- [지시] **firemap-youtube-loop** N2: 세법 개정안(종부세·양도세) 의안 원문 확인 → '공시가격 구간별 1주택 종부세 전·후' 편 기획안 · 기한 10/15 · U10 결론(클립 fF_5 648회 → M-1 롱폼 17→20회) 기록 + 클립 방식 변경안, W-1 3일 노출 10/15 기록(U1)
  착수: firemap-youtube-loop 04:43 — 정부안 원문(재경부 상세본·문답·9/1 확정 보도자료) → calc.py → 기획안
  완료(기획안·U10): firemap-youtube-loop 04:51 — ep/J-1/plan.md · 원문 3건 받아 읽음(raw/mofe_0803_6·8, mofe_0901: 9/1 수정 = 비거주 1주택 공제 12억 유지·상한 150% 유지·9/3 국회 제출) · calc.py가 정부 적용사례 9칸 중 8칸 일치(사례③ 2027만 원문 세율표로 2,251.7 vs 정부 표 1,942.1 → 그 칸 안 씀) · 발견: 55세 10년 실거주는 공시 22억까지 2028 보유세가 오히려 줄고(20억 −22.5만원) 25억부터 늚(30억 +135.9만원), 같은 20억도 안 살면 +140.9만원 · 수요 kwvol 종부세 9,210·장특공제 8,580·계산기 5,530, 유튜브 '종부세 개편' 75일 상위 30편 중앙 16.3만 → 만든다, 칸은 10/20 주 11:30 1개(회의 배정) · 확인 필요: 정부 제출 법안 의안번호·조문(열린국회 무키 API는 최근 5건만) · **U10 결론**: M-1(eTjVs1vDTwg) 10/8~ 유입 = 구독자 16·검색 2·채널 1·관련 동영상 0·쇼츠 0(analytics 2~3일 늦음) → 클립 fF_5(648회)가 롱폼으로 데려온 사람 0 확인. 변경안: ① 클립은 노출 붙은 롱폼(N-1·A-1·R-1)에서만 자름 ② 쇼츠 '관련 동영상' 연결은 API로 못 넣어 스튜디오 화면 작업(채팅 세션) ③ 끝 문장은 '본편에서 ○○의 답' 한 가지 질문으로 · W-1 3일 노출은 10/15에 기록
- [지시] **firemap-video-producer** 다음 렌더부터 로고 카드 첫 60초 밖(W-1 0:16~0:20에 남음), W-1 음높이 앞뒤 차 측정 1줄 · 기한 10/15
  완료: firemap-video-producer 06:40 — lfrender.py gates에 logo_check 추가(로고 장면이 첫 60초 안에서 시작하면 렌더 거부, 지금 w1 16.1초·g1 30.3초 잡힘) · R-1 새 판은 로고 장면 뺌 · W-1 음높이 앞뒤 절반 차 −1.4%·IQR/중앙 0.13(lfvoice check, 녹음 날 10/12 하루, 통과)

## ★ 정기 회의 10/12 21:28~21:41 (19:16 따라잡기 뒤 결정만) — 근거 meeting/2026-10-12b-decisions.md·b-verify.md
- 공개 10/12: **4**(쇼츠 m1s_nhis70·롱폼 W-1 0yWQ·카페 #254·#255) — 기준 3 충족. 22:10 didim1012 남음 · 0원 뒤처짐 · 외부 15기기·click 0
- 막힘: ① 10/13 20:10 m1stot1013은 발행기가 '같은 대상 이미 씀'(#245 schdacct1007과 SCHD가 겹침, naverpost subject_keys)으로 막는다 ② 비축 쇼츠 0/1·카페 1/2 ③ 저장소 public(우리 비밀값은 노출 안 됨, 의장 확인 — 결재 유지)
- [지시·긴급] **firemap-write** (기한 10/13 14:10 = 20:10 칸 관문 기한) 의도: 10/13 20:10 칸이 발행기에서 막히지 않게 · 완료 기준: m1stot1013 대신 m1s_total1y 쇼츠 질문 하나에 답하는 글이고 subject_keys가 기존 발행 글과 안 겹치는 편(티커 없이 '1년 총수익' 질문으로 다시 쓰거나 비축분과 바꾸기) → slots note에 yt_pair 유지·gates_ok 시각 · 금지: SCHD·JEPQ 제목 재사용, 칸 비우기 · 확인: 운영실장 07:05 · 보고: decisions/log.md · 덤: 카페 실제 작성 시각이 칸보다 30분 넘게 늦은 날이 이틀(18:48·20:42) — 늦은 이유를 한 줄로
  착수: firemap-write 22:31 — 22:10 didim1012 발행(대기 중) · m1stot1013 subject_keys 안 겹치게 다시 쓰기 · 10/13 18:10 새 편
  완료: firemap-write 22:42 — m1stot1013 제목 티커 뺌 "배당 ETF 셋 중 분배금 최고 커버드콜이 1년 총수익 꼴찌인 이유"(subject_keys 빈 집합·최근 카페 겹침 0, 본문·표지·yt_pair 그대로) · 제미나이 9·레드팀 7(틀림 0) · readcheck 0·틀 v2 0 · editgate auto 재날인 · slots 10/13 20:10 gates_ok 22:42 · 덤: 18:47 늦음=PC 재부팅(18:33) 뒤 첫 회차, 20:42 늦음=20:21 회차+발행기 무작위 대기(0~17분)
- [지시] **firemap-video-producer** (기한 10/13 10:30 = G-1 공개 1시간 전) 의도: 수익에 가장 가까운 자리와 AI 표시를 맞춘다 · 완료 기준: ① G-1 xBTZtRp5lMs의 containsSyntheticMedia를 True로 맞추고 meta synthetic도 True(R-1·W-1과 같은 기준, 10/12 회의 결정) ② youtube-loop 20:51 요청대로 N-1 카페 짝 글 주소와 A-1 계산기 줄을 설명란 앞 5줄로 올린다(새 문구 0, 기존 줄 옮기기만) ③ ytlong.py 업로드 직전 검사를 넣는다: 같은 편이 slots published나 upload.json 예약에 이미 있으면 멈춘다(교훈 31·체크리스트 41) · 금지: 설명란에 새 홍보 문구 추가 · 보고: decisions/log.md
  착수: firemap-video-producer 22:17
  완료: firemap-video-producer 22:21 — ① G-1 xBTZtRp5lMs containsSyntheticMedia=True(update 응답 확인, private+publishAt 10/13 02:30Z 그대로 — videos.list는 이 칸을 안 돌려줌)·meta synthetic True ② N-1 카페 #208 줄 → 3번째 줄, A-1 계산기·카페 #187 줄 → 3·4번째 줄(쿠팡 고지 2줄 아래) · 새 문구 0(줄 집합 같음 assert, 제목 그대로) ③ ytlong.py dup_check: uploads.jsonl 같은 편 살아 있는 줄·slots.json 같은 편/같은 칸 published 있으면 up 멈춤, 새 판은 --replace <옛ID>(옛 줄 replaced 자동) · `ytlong.py dup <ep>` 단독 검사(G-1·R-1 막힘, H-1 통과 확인)
- 참모 반론 처리: 받아들임 = D11 칸 교체·G-1 AI 표시 맞춤·설명란 접힘 위(검증 사실 확인) · 안 받아들임 = 법1 면책(이미 있음)·법2 쿠팡 대가 문구(A-1에만 링크, 문구 있음)·법3 AI 표기(있음)·법4 스톡 구매 기록(Pexels 무료)·법6 삭제가 유리(근거 없음)·전략 발행 중단·포맷 하나(사장님 '롱폼 하루 한 편' 지시와 충돌)·사용자 '통합 계산기'(10/6 사이트 개발 중단)
- 원칙 바꿈: 사용자 참모에는 다음 회차부터 회의록 대신 그날 공개한 실제 결과물 1편을 넣는다(회의록은 헤더를 달아도 '서비스 평가'로 읽힘) · second_opinion.py는 결정 문서에 '읽는 법' 헤더가 없으면 멈춘다

## ★ 회의 10/12 18:59~ (10/11 회의는 PC 꺼짐으로 못 열림, 이틀치) — 근거 meeting/2026-10-12-decisions.md·verify.md·missed-q_레드팀.md
- 막힘: ① 회차 0: 10/11 17:33 충전기 빠짐 → 18:21 와이파이 끊긴 뒤 다시 못 붙음(PC는 켜져 있었음) → 10/12 01:22 배터리 절전 → 13:15 비정상 종료 → 18:33 재부팅(검증 참모, 윈도 이벤트 로그). 카페 이틀 8칸·쇼츠 07:20·롱폼 11:30(W-1) 빠짐, 이달 두 번째 · 결재: 충전기 상시 + 와이파이 자동 재연결(시스템 설정이라 사장님 손) ② 저장소 아직 public(레드팀 10/12 api.github.com private:false, 결재 10/8부터) — 순돌이 ③ 쇼츠 비축 0, C-1 클립 3칸(10/13·14·15 07:20) 사용 금지로 TBD ④ 카페 비축 1/2(npsage1009 10/14~) ⑤ H-1(10/15 11:30) compare.md 없음(patrol)
- 공개: 10/11 7(카페 5·쇼츠 1·롱폼 C-1 → 비공개) / 10/12 19:00까지 1(카페 #254) — 기준 3 미달, 원인 PC 꺼짐. 헛돈 회차·X-OPS 지표는 PC 꺼짐으로 표본 없음(확인 안 함)
- 원칙(스프린트·운영실장): 첫 칸 = 수익에 가장 가까운 일 = **롱폼·쇼츠 짝 카페 글**(설명란 앞 5줄 → 카페 → 계산기 쿠팡 칸). 카페 칸 배정은 짝 글 먼저. 빠진 칸 몰아내기 금지.
- [지시·긴급] **firemap-video-producer** (기한 오늘 23:00·10/13 09:30) 의도: 롱폼 정규 칸을 다시 매일로 · 완료 기준: ① W-1 새 판 오늘 밤 공개 → 링크를 slots.json 10/13 08:10 note·이 줄 밑에(write 짝 글용) ② G-1 EZvDDPlXo90 10/13 11:30 재예약 → slots gates_ok 시각 ③ c1s_receipt QlL0VK4PB_8: 순돌이 해제 목록에 없고 upload.json엔 10/14 07:20 예약이 남음(검증 참모) — videos.list로 publishAt 실측, 남아 있으면 풀기(권한 막히면 순돌이) ④ 10/13 07:20·10/14 07:20 쇼츠 = G-1·W-1 클립(같은 날 19:20 m1s와 다른 롱폼), numread 받아쓰기 대조 통과분만 예약 ⑤ W-1이 오늘 나가면 10/14 11:30 = P-1(관문 기한 10/13 11:30), 못 넘으면 R-1 · 기준 예시: G-1 10/11 17:18 관문 전부 통과 기록 · 금지: C-1 클립 사용, 숫자 읽기 대조 없이 예약, 미달 공개, 빠진 칸 몰아 공개 · 확인 시점: 운영실장 23:05 · 보고: decisions/log.md
  진행: firemap-video-producer 19:22 — ① 완료: W-1 https://youtu.be/0yWQeW38UJE 19:47 공개 예약, slots 10/13 08:10 note에 yt_pair 링크 · ②③(G-1 재예약·쇼츠)은 G-1 회차(순돌이 배차 18:45) 몫
- [지시·긴급] **firemap-video-producer** (기한 G-1 재예약 전, 오늘 23:00) 의도: AI 목소리 편은 전부 '변경·합성 콘텐츠' 켬(A-1 meta synthetic_why·RULES 4장) · 완료 기준: G-1·H-1·R-1 meta.json synthetic=true(업로드 전), 이미 올린 M-1 eTjVs1vDTwg·N-1 420buEFKB8k·E-2는 videos.update status.containsSyntheticMedia=true(제목·설명 등 다른 칸 같이 넘기기, 교훈 18) · 금지: 카페 'AI(Claude) 작성' 끝문장 되살리기(사장님 10/11 지시 — 유튜브 표시와 별개) · 보고: decisions/log.md, 권한 403이면 막힘 줄
  착수: firemap-video-producer 02:19
- [지시·긴급] **firemap-write** (기한 10/13 02:10·04:10) 의도: 내일 아침 짝 글 두 칸을 영상보다 먼저 · 완료 기준: 오늘 20:10 med1011·22:10 didim1012 발행 verify + 10/13 08:10 W-1 짝(ep/W-1/cafe.md, W-1 공개 시)·10:10 G-1 짝(ep/G-1/cafe.md, '영수증' 2곳 평범한 말로) gates_ok · 10/13 18:10 새 편(기한 12:10)·20:10 m1s_total1y 짝·22:10 m1s_nhis70 짝·10/14 08:10 M-1 짝 · 카페 비축 2/2 회복 · 기준 예시: inhded1011(관문 전부·compare.md) · 금지: 짝 글에 영상 없는 숫자 새로 만들기, 같은 내용 두 번(롱폼 글=전체 표, 쇼츠 글=질문 하나), 국민연금 제목 10/14 08:30 전 · 확인 시점: 운영실장 23:05·07:05 · 보고: 칸마다 gates_ok 시각 · slot.txt는 회의가 med·didim·issnote·kidcred·yuryu 칸 시각으로 맞춰 둠(19:05)
  착수: firemap-write 20:21 — 20:10 med1011 발행·verify · 22:10 didim1012 · 내일 08:10 W-1 짝·10:10 G-1 짝 관문
  완료(일부): firemap-write 20:45 — 20:10 med1011 cafe/255 발행 20:42 verify OK 1487/1487자·사진 3/3 · 10/13 08:10 w1cafe1013(W-1 짝, 영상 0yWQeW38UJE 링크, 영수증 0곳) gates_ok 20:44(제목 7.75·표지 K1 7.67·compare.md 6편·readcheck 0·selfcheck 사실 0·aitell 0.0·crosscheck·레드팀 2회·전제 가능·editgate auto) · 10/13 10:10 g1cafe1013(G-1 짝, 새 판 xBTZtRp5lMs 링크, 영수증 0곳) gates_ok 20:32(제목 7.33·표지 8.0·compare.md 7편·전제 가능) · slots.json 두 칸 item·gates_ok 적음 · 10/13 20:10·22:10 쇼츠 짝 글 보조 작성 중 · 남은 것: 22:10 didim1012 발행(다음 회차), 10/13 18:10 새 편·10/14 08:10 M-1 짝·비축 2/2
  완료(일부): firemap-write 21:05 — 10/13 20:10 m1stot1013(m1s_total1y 짝) gates_ok 21:05(제목 7.67·표지 7.67·레드팀 3회·전제 가능) · 22:10 m1snhis1013(m1s_nhis70 짝) gates_ok 21:05(제목 7.73·표지 7.33·레드팀 2회·전제 가능) · slots.json 두 칸 적음 · 남은 것: 22:10 didim1012 발행(다음 회차), 10/13 18:10 새 편(기한 12:10)·10/14 08:10 M-1 짝·비축 2/2
  완료(일부): firemap-write 22:42 — 22:10 didim1012 cafe/256 발행 22:41 verify OK 1313/1313자·사진 3/3 · 10/13 18:10 새 편 주제 = 리츠 ETF 분배금(배당현금흐름, 검색 리츠ETF 3,510·월배당ETF 4,720, 이슈 국채금리 급등에도 개인 리츠 ETF 순매수, 최근 카페 100편 중 리츠 0) — 원고·관문은 10/13 08:10 회차(기한 12:10) · 남은 것: 10/14 08:10 M-1 짝·비축 2/2
  착수: firemap-write 23:10 (운영실장) — 10/13 12:10 issnote1012·14:10 kidcred1012·16:10 yuryu1011 gates_ok(전제 줄 포함) · 18:10 리츠 ETF 새 편 관문 · 10/14 08:10 M-1 짝
  완료(일부): firemap-write 23:11 — 10/13 12:10 issnote1012·14:10 kidcred1012·16:10 yuryu1011 세 칸 review.md '전제: 가능 — 근거' 줄 확인 + editgate stamp 세 편 모두 '찍음'(전제 관문 통과) + slots.json gates_ok 23:11 · 남은 것: 10/13 18:10 리츠 ETF 새 편(기한 12:10)·10/14 08:10 M-1 짝(기한 02:10)·카페 비축 1/2(npsage 10/14~)
  착수: firemap-write 08:20 — 08:10 w1cafe1013 발행·verify · 18:10 리츠 ETF 새 편 관문(기한 12:10) · 10/14 08:10 M-1 짝 · R-1 짝 링크 확인
  완료: firemap-write 08:33 — 08:10 w1cafe1013 cafe/257 발행 verify OK 1439/1439자·사진 3/3 · 10/14 08:10 m1cafe1014(M-1 짝 긴 글, 필요 원금 전체 표·가장 적은 달 기준, 영상 eTjVs1vDTwg) gates_ok 08:33(제목 8.13·표지 K4 8.0·compare.md 경쟁 5편 건보료 0/5·readcheck 0·selfcheck 사실 0·aitell 2.4·레드팀 2회 틀림 1 반영·전제 가능·editgate auto) · 10/14 10:10 renew1011 전제 줄·제목 쉼표 뺌(틀 v2)·slot.txt·재날인 gates_ok · 18:10 reitetf1013은 07:24 이미 통과 · 남은 것: 10/14 14:10 r1cafe1014·16:10 cheongyak·18:10 qqqm·20:10 r1cafe_fx·22:10 dcpension(기한 각 6시간 전), 비축 카페 2/2
  착수: firemap-write 10:22 — 10:10 g1cafe1013 발행·verify · 남은 칸 관문 점검
  완료: firemap-write 10:52 — 10:10 g1cafe1013 cafe/258 발행 10:51 verify OK 1912/1912자·사진 4/4(aitell 같은 예시 오탐 고침) · 10/14 14:10 r1cafe1014(R-1 짝 긴 글, 영상 G1oI47miUuo) gates_ok(제목 7.33·표지 K4 7.67·compare.md 경쟁 6편·readcheck 0·selfcheck 사실 0·aitell 2.7·레드팀 2회 틀림 2 반영·전제 가능·editgate auto) · 10/14 12:10 npsage1009 gates_ok · issnote1012 특판 재확인 · 남은 것: 10/14 16:10 cheongyak·18:10 qqqm·20:10 r1cafe_fx·22:10 dcpension, 비축 2/2
  착수: firemap-write 12:20 — 12:10 issnote1012 발행·verify · 10/14 16:10 cheongyak1012 관문
  완료: firemap-write 12:46 — 12:10 issnote1012 cafe/259 발행 12:46 verify OK 1955/1955자·사진 3/3 · 10/14 16:10 cheongyak1012(청약통장 해지 추징, 세율별 감면 대 추징·퇴직 6개월 예외) gates_ok 12:37(제목 8.0·표지 Q5 8.0·compare.md 경쟁 8·readcheck 0·selfcheck 사실 0·aitell 0.0·레드팀 2회 틀림 1 반영·전제 가능·editgate auto) · 남은 것: 10/14 18:10 qqqm(기한 12:10)·20:10 r1cafe_fx·22:10 dcpension, 비축 카페 2/2
  착수: firemap-write 14:21 — 14:10 kidcred1012 발행·verify · 남은 칸 관문 점검
  완료: firemap-write 14:42 — 14:10 kidcred1012 cafe/260 발행 14:41 verify OK 1840/1840자·사진 3/3 · 10/14 20:10 r1cafe_fx1014(쇼츠 r1s_fx 짝, "미국 ETF 환차손, 달러로 번 1년 수익은 원화로 몇 % 줄었을까", 영상 2i957iWL8ko·본편 G1oI47miUuo) gates_ok 14:38(제목 8.0·표지 K2 8.0·compare.md 경쟁 4·readcheck 0·selfcheck 사실 0·aitell 0.0·레드팀 2회 틀림 1 반영·전제 가능·editgate auto·titlegate·sameday 통과) · 남은 것: 10/14 18:10 qqqm1014(기한 지남, 카페 #46과 같은 각도 — 막히면 비축분으로)·22:10 dcpension1014(기한 16:10)
  착수: firemap-write 16:21 — 16:10 yuryu1011 발행·verify · 10/14 18:10 qqqm1014·22:10 dcpension1014 관문
  착수: firemap-write 18:21 — 18:10 aptrent1013 발행·verify · 10/15 21:10·10/16 write 칸 새 편 관문
  완료: firemap-write 18:54 — 18:10 aptrent1013 cafe/273 발행 18:40 verify OK 1430/1430자·사진 3/3(장부 자동) · 10/15 21:10 sdi1015b '삼성SDI 주가 올해 고점보다 17% 아래, 배당은 쉬기로 한 지금 자리'(종목·형식4, 제목 7.33·표지 M1 7.67·레드팀 3회 틀림 0·readcheck 0·selfcheck 사실 0·aitell 1.1·compare 경쟁 5·editgate) gates_ok 18:53 — **10/15 장 마감 뒤 write 회차(18:10 전)가 10/15 종가로 calc.py 재계산·17% 바뀌면 제목·표지 재심·재날인** · 10/16 06:10 costchk1016 '재개발 재건축 공사비 15% 올라도 검증 의무가 없을 수 있는 계약 시점'(부동산·형식2, 도시정비법 제29조의2·국토부 10/14 138곳 발표·ECOS 생산자물가, 제목 7.33·표지 K8 7.67·레드팀 4회 틀림 0·aitell 0.0·editgate) gates_ok 18:54 · 남은 것: 10/16 09:10·12:10(P-1 짝)·15:10·18:10·21:10 write 칸 · 10/15 07:40 write-b가 삼성SDI 고르지 않게(같은 날 같은 종목)
  완료: firemap-write 16:38 — 16:10 yuryu1011 cafe/261 발행 16:37 verify OK 1470/1470자·사진 3/3 · 10/14 22:10 dcpension1014(퇴직연금 DB형 대 DC형, 손익분기=월급 인상률·임금피크 예시) gates_ok 16:34(제목 7.9·표지 K4 7.67·compare.md 경쟁 6편·readcheck 0·selfcheck 사실 0·aitell 2.5·레드팀 2회 틀림 1·오해 6 반영·전제 가능·editgate auto) · 18:10 qqqm1014는 15:24 이미 통과 · 10/14 카페 8칸 전부 gates_ok · 남은 것: 카페 비축 2/2(지금 0 — 10/14 칸에 다 배정)
  착수: firemap-write 18:22 — 18:10 reitetf1013 발행·verify · 카페 비축 0/2 채우기
  완료: firemap-write 18:57 — 18:10 reitetf1013 cafe/262 발행 18:29 verify OK 1138/1138자·사진 3/3 · 카페 비축 0/2→2/2: aptrent1013(서울 아파트 월세 같은 단지·면적 +5.6%, 제목 7.83·표지 7.58·editgate auto, slot 가안 10/16 16) · stockgift1013(상장주식 증여 전후 2개월 평균, 제목 7.92·표지 7.67·editgate auto, slot 가안 10/16 10 — '10월 말' 반환 기한 때문에 10/16까지만) · [알림] firemap-meeting: 두 편 slots 칸 배정 필요(pending '장부에 칸 없음') · [알림] firemap-copywriter: stockgift1013 제목 끝 '~나온 계산' 압축 모양 재검토(바꾸면 재심사·editgate 재날인)
- [지시] **firemap-write** (기한 10/14 12:00, 레드팀 R2) 의도: 카페에도 전제 관문 · 완료 기준: editgate.py stamp가 카페 pkg review/compare에 '전제:'(가능/불가능 + facts 근거) 줄 없으면 '안 찍음' + 대기 편(issnote1012·kidcred1012·yuryu1011·npsage1009)에 '전제:' 줄 · 시험: 임시 사본에서 줄 빼면 거부 · 금지: 사이트 코드 · 보고: today.md 완료 줄+커밋
  완료: firemap-write 20:45 — editgate.py stamp가 카페 pkg의 review.md/compare.md(pkg 또는 위 폴더)에 '전제: 가능 — <근거>' 줄이 없거나 '불가능'·근거 없음이면 '안 찍음 · 전제 관문' · 시험: inhded1011 임시 사본에서 줄 뺌→거부, 불가능→거부, 가능+근거→찍음 · issnote1012·kidcred1012·yuryu1011·npsage1009 review.md에 전제 줄(전부 가능, facts 번호) — 기존 날인 해시 그대로 일치
- [지시] **firemap-report** (기한 10/13 12:30 회차, 레드팀 R1) 의도: 사이트 유입 1/3 감소(10/7 33기기 → 10/11 12, utm youtube 7 → 0) 원인 · 완료 기준: sitedaily로 10/5~10/12 날짜별 외부 기기·utm source 표를 growth/revenue.md에, 줄어든 source 한 줄 원인(설명란 링크 위치 변경 10/11 등 날짜 대조) + 쿠팡·애드센스 화면 실측(10/12 확인 안 함) · 금지: 추정 숫자 · 보고: launch-checklist 39 경보 줄
  착수: firemap-report 12:34 — 10/5~10/12 사이트 외부 기기·utm 표, 감소 원인, 쿠팡·애드센스 화면
  완료: firemap-report 12:46 — revenue.md 10/5~10/12 표(외부 24·27·33·32·18·18·12·17기기) · 줄어든 source = utm youtube yts2-n1(N-1 설명) 7→0, N-1 노출 4,876(10/7)→179(10/9) 노출 창 닫힘 · utm 없음 27→14도 같은 날 꺾였으나 referrer 미기록이라 원인 확인 안 함 · 쿠팡 클릭1/구매0(리포트 10/13) · **애드센스 firemap.kr 주의 필요·가치가 별로 없는 콘텐츠(10/9 01:10)** — 크롬 u/0은 스꾸 계정, 파이어맵은 u/2
- [지시] **firemap-youtube-loop** (기한 10/13 08:35 회차) 의도: 노출이 붙은 롱폼에서 사이트로(레드팀 O2) + 국민연금 주간(O1) · 완료 기준: ① N-1(노출 8,338)·A-1(5,771) 설명란 앞 5줄에 계산기(/calc/salary 등 쿠팡 칸 있는 쪽)·카페 링크가 있는지 실측, 없으면 PD에 videos.update 요청 줄 ② P-1 대본·전제 줄 최종 → PD 10/14 칸 넘김(짝 카페는 npsage1009 10/14 12:10) ③ H-1 compare.md ④ H-2(대치·잠실·반포, 10/22 11:30) 대본 10/19까지 · 금지: 투자 권유·전망
  착수: firemap-youtube-loop 20:43 — ① N-1·A-1 설명란 앞 5줄 실측 → ③ H-1 compare.md → ② P-1 전제·대본 최종 → ④ H-2
  진행: firemap-youtube-loop 20:47 — ① 실측(videos.list): N-1 앞 5줄에 /calc/salary(쿠팡 칸 있음) 2번째 줄 ✔·카페 링크 없음(맨 끝 대문 주소뿐) / A-1 앞 5줄 = 쿠팡 2줄·빈 줄·요약 2줄, 계산기는 6번째 줄(firemap.kr 첫 화면)·카페는 맨 끝 대문 → PD 요청 아래 ② P-1 전제 줄 '확인 필요' 닫음: 공단 원문 「노령종류별 지급현황(202407~202506).csv」 2025-06 완전노령연금(20년+) 1,170,946명 평균 약 111만원(facts [P0]) · 10/14 11:30은 R-1이 이미 예약(PD 20:25)이라 **P-1 = 10/16 11:30 칸**(slots 적음, 녹음 10/14 16:01, 관문 10/15 11:30), 짝 카페 npsage1009 10/14 12:10 그대로 ③ H-1 compare.md 씀(1등 VLj3irGy-ic 대비 나은 점 2·지난 N-1 대비 1·따라잡을 점 1) · ④ H-2는 다음 회차(10/19 기한)
- [요청] **firemap-video-producer** ← youtube-loop (20:47) 트랙:C · 시한 10/13 12:00 · N-1(420buEFKB8k)·A-1(SCOI0DP-l-s) 설명란 앞 5줄에 사이트·카페 링크 · videos.update(snippet 전체 칸 같이, 교훈 18·A-1 쿠팡 첫 2줄·paidProductPlacement 그대로): **N-1** 3번째 줄로 '연봉·순자산 칸별 전체 표(카페): https://cafe.naver.com/firemap/208' 끼움(맨 끝 대문 줄은 그대로) · **A-1** 3번째 빈 줄 자리에 지금 6번째 줄 '내 은퇴 나이 계산(영상 끝 장면 계산기): https://firemap.kr/?utm_source=youtube&utm_medium=desc&utm_campaign=a-1'을 올리고 4번째 줄 'ETF별 전체 표(카페): https://cafe.naver.com/firemap/187'(끝의 대문 주소 줄을 이 글 주소로 옮김), 그 아래 빈 줄 하나 뒤 요약 2줄 · 새 문구 0(기존 줄 옮기기·글 주소만) · A-1 계산기는 주제(배당·은퇴)와 맞는 첫 화면 유지 — 쿠팡 칸 계산기(/calc/salary)는 N-1에만 맞음 · 확인: videos.list 앞 5줄 되읽기 · 근거 ep/N-1·A-1 meta.json, 카페 #208(n1cafe1004)·#187(a1cafe1001)
  완료: firemap-youtube-loop 20:54 — ①(PD 요청 위)·②(P-1 전제 공단 원문·10/16 11:30 칸, 10/14는 R-1 예약)·③(H-1 compare.md) 끝 · ④ H-2 착수: 검증 통과(은마 62,010·경쟁 bSrhZncUGD4 8.77배)·analysis.md ①~④-0, 대치·잠실 실거래·지도 수집(raw/tour_*), 반포는 Overpass 504 두 번 → 다음 회차 · 1차 각도 '오래된 재건축이 새 아파트보다 비싼 동네(잠실 5단지 평당 1억 7,449만원 > 리센츠 1억 3,283만원)와 아닌 동네(대치 은마 1억 5,231만원 < 래미안대치팰리스 1억 6,630만원)' · 대본 기한 10/19 그대로
- [판단] **firemap-youtube-loop** 20:47 P-1 bench_check ③④(PD 19:17 'youtube-loop 판단') → script.md v2.3: 인물 첫 등장 0:45 그대로(콜드오픈 재사용 줄·고지 2:30 안 맞음), 말 속 인물 2→6줄(7.7%), 끝 '정리할게요' 4줄 삭제 → 건보료 연결+이전 편 D-1+댓글 질문 · 근거 ep/P-1/bench_check.md 맨 아래
- [편집 검수 요청] P-1 v2.3 바뀐 말 8줄 트랙:C · 담당 firemap-editor · 시한 10/14 14:00(녹음 16:01 전) · 근거 ep/P-1/say_v4.txt vs say_v3.txt
  완료: firemap-editor 17:11 확인 — 10/14 07:07 script.md.edit.json(sha e6516dc6…)이 지금 파일과 같음, 이미 통과(줄만 안 적혀 있었음)
- [요청] **firemap-video-producer** ← youtube-loop (20:47) 트랙:C · 시한 10/15 11:30(관문) · P-1 말 8줄만 Chirp 재녹음(10/14 16:01 창, editor 통과 뒤): 바뀐 5(1·2·3·4·5장 '연금 씨') + 끝 새 3 · 끝 장면에 D-1(GMc2Rd1-JYA) 카드·최종 화면도 D-1 · 자막 '피부양자 소득 요건 연 2,000만원 이하(연금 포함) · 건보공단' · 근거 ep/P-1/script.md v2.3
  진행: firemap-video-producer 07:21 — editor 07:07 v2.3 재서명 확인 → 새 8줄 Chirp 녹음(16:01 창 안 기다림, Chirp) · 4:0 '빠름' 1줄 다시 받기 → lfvoice check 통과(튀는 줄 0·앞뒤 −1.2%·IQR 0.16·둘째 날 줄 8/78) · readback 78문장 숫자 걸림 0(받아쓰기 글자 잡음 6줄, 숫자 맞음) · stepprops·p1props 새 목소리로 다시 만듦 · **남은 것: 마무리 장면** — p1props 'sum'이 옛 '정리' 카드(77세·519만원·계단 at)라 v2.3 끝 3줄(건보료 자막·D-1 카드·댓글 질문)에 안 맞음 → D-1 카드 부품·자막 → lfrender text → editor 재서명 → render → 관문, 다음 PD 회차 첫 일(관문 기한 10/15 11:30)
- [지시] **firemap-audit** (기한 10/13 20:50) 의도: 공개 전 전제 표본 · 완료 기준: 10/13 공개 카페 8편·G-1·W-1 중 3편 '전제' 대조(가능/불가능) + 저장소 공개 상태 API 한 줄(checklist 40) · 보고: audit.md
  착수: firemap-audit 21:00 — 10/13 공개 예정 카페·G-1·W-1 중 3편 전제 대조 + 저장소 공개 상태 API
  완료: firemap-audit 21:04 — 전제 표본 3/3 가능·숫자 틀림 0(w1cafe1013 야후 종가 직접·g1cafe1013 링크 xBT 10/13 11:30 예약 직접·issnote1012 세후 재계산) · 저장소: 웹·raw 200 = 여전히 공개(REST API는 비인증 한도 403, 값 못 받음) · 근거 longform/loop/audit.md 10/12 21:04
- [요청] **firemap-write** ← firemap-audit (21:04) 경미 · didim1012(오늘 22:10)·review/compare에 '전제:' 줄 없음(20:45 전제 관문 전 날인) — 감사가 직접 대조해 가능(금리 4칸·월 상환액·이자 차 재계산 일치)이라 발행은 그대로, review.md에 '전제: 가능 — <근거>' 한 줄 추가 · 기한 10/13 12:00 · STOP 아님
  완료: firemap-write 22:42 — didim1012/review.md에 "전제: 가능 — 금리 4칸·한도 2억 안·월 상환액·총이자 차 calc_out 일치" 줄 추가(발행 전)
- [지시] **firemap-dispatcher** (23:05·07:05 회차) 의도: 관문 기한 칸 먼저 · 완료 기준: write 10/13 08:10·10:10 짝 글이 기한(02:10·04:10)에 gates_ok 없으면 write 투입, PD W-1 공개 안 됐으면 PD 투입 줄을 dispatch/log.md에
  착수: firemap-dispatcher 23:10 — 08:10 w1cafe1013·10:10 g1cafe1013 gates_ok 있음·W-1 0yWQeW38UJE 예약됨 → write·PD 해당 투입 불필요. write(12:10·14:10·16:10 gates_ok·18:10 새 편)·PD(쇼츠 비축 0/1) 투입
  완료: firemap-dispatcher 23:21 — write 89913f0(12:10·14:10·16:10 gates_ok 23:11, 18:10 새 편·10/14 08:10 M-1 짝은 다음 회차 08:19 몫)·PD ce121a0(쇼츠 비축 r1s_spytax 1/1, gates_ok 23:20, 10/15 07:20용·미업로드)
- 받아들인 반론(참모 3+레드팀): 전제 관문 카페까지(레드팀·전략·법) · 유입 추세 경보(레드팀) · 저장소 공개 결재 안건 유지(레드팀) · **AI 음성 표시(법 일부)** — 회의 19:09 grep: Chirp·TTS 목소리인데 meta synthetic=false인 편 G-1·H-1·R-1·M-1·N-1·E-2(true는 A-1·C-1·D-1·E-1·W-1), RULES 4장 '애매하면 켠다'와 어긋남 → PD [지시·긴급] · 국민연금 주간 P-1 10/14(레드팀) · 몰아내기 금지 유지(법) / 안 받음: VPS 이전(Claude 예약 작업·브라우저 로그인·렌더가 이 PC에 묶임, 결재만 남김) · 발행 1/4로 줄이기(빈도는 사장님 10/11 지시) · 이메일 수집·유료 상담(사이트 개발 중단·유사투자자문 소지)

- [알림·긴급] **firemap-write·firemap-youtube-loop** ← firemap-audit (18:57) c1cafe1011(C-1 짝 카페, pending 5편 마지막) 발행 보류 — pkg/hold.txt 만듦. C-1을 내린 불가능 전제(S&P500 3억 배당 월 200만원, c02 첫해 분배금 3,122만원)·'영수증' 비유·비공개 영상 참조를 그대로 담음. gates_ok(10/11 16:34)가 전제 검사 지시(17:1x)보다 먼저라 안 걸림. 대기 다른 4편(med·didim·issnote·kidcred)은 그대로 · 풀기: C-1 재기획이 전제 검사 통과한 뒤 hold.txt 삭제 · STOP_cafe 아님 · 근거 longform/loop/audit.md 10/12
- [지시·긴급] **firemap-write** (회의 21:41, 기한 10/11 06:10 = 12:10 칸 관문) 의도: 비축 0인 채 10/11 카페 6칸(12:10·14:10·16:10·18:10·20:10·22:10)과 10/12 08:10이 TBD — 칸 비우기는 실패 · 완료 기준: 각 칸 발행 6시간 전 gates_ok + 비축 카페 실사용 1/2 이상 · 기준 예시: inhded1011·netpay1011(제목 7 이상·표지 7 이상·compare.md·editgate auto) · 금지: 청년 전용 상품(youthsave1010 예외 없음), 국민연금 제목 10/14 08:30 전, 계산기 B칸 하루 2칸 초과·연속 · 확인 시점: 운영실장 23:05·03:05 회차 · 보고: 칸마다 gates_ok 시각
  착수: firemap-write 22:22 — 22:10 odivfx1010 발행·verify · 10/11 12:10 칸부터 편 확정·관문
  완료(일부): firemap-write 22:52 — 22:10 odivfx1010 cafe/248 발행 22:39 verify OK 2002/2002자·사진 3/3 · 12:10 mortded1011 gates_ok 22:50(주담대 이자 소득공제, 제목 8.23·표지 8.0·레드팀 2차 틀림 0·editgate auto) · 14:10 cardded1011 gates_ok 22:48(신용카드 소득공제, 제목 8.0·표지 7.67) · 16:10·18:10 보조 투입 중 · 남은 TBD 20:10·22:10·10/12 08:10
  완료(일부): firemap-write 23:08 — 16:10 saving1011b(적금 이자 세후, 배당현금흐름) gates_ok 23:07 · 18:10 dsrlim1011c(스트레스 DSR 수도권·지방 한도, 부동산) gates_ok 23:07 · 10/11 카페 6칸 중 4칸 관문 통과(12·14·16·18시) · 남은 TBD 20:10(기한 14:10)·22:10(기한 16:10)·10/12 08:10(기한 02:10) — 다음 write 회차 08:10·10:10에서
  착수: firemap-write 23:09 (운영실장) — 남은 TBD 20:10·22:10·10/12 08:10 중 한 칸 관문 + 비축 카페
  완료(일부): firemap-write 23:26 — 10/11 20:10 칸 med1011(부모님 병원비 의료비 세액공제, 세금연금·형식2) gates_ok 23:26(제목 8.0·표지 7.33·compare.md 경쟁 5편·editgate auto) · improve 22:41 알림 확인: cardded1011은 22:48에 compare.md(경쟁 5편)·cover_review 평균 7.67·소제목 5로 이미 채워져 유효(pending check 지적 없음) · 10/11 카페 6칸 중 5칸 관문 통과 · 남은 TBD 22:10(기한 16:10)·10/12 08:10(기한 02:10) · 비축 카페 새 편은 못 만듦(칸 우선)
  착수: firemap-write 08:20 — 08:10 inhded1011 발행·verify · 남은 TBD 22:10(기한 16:10)·10/12 08:10(기한 02:10) 관문
  완료: firemap-write 08:41 — 08:10 inhded1011 cafe/249 발행 08:40 verify OK 1729/1729자·사진 4/4 · 22:10 renew1011(계약갱신청구권 실거주 거절 뒤 새 세입자 배상금, 부동산·형식2) gates_ok 08:34(제목 7.67·표지 K6 7.33·compare.md 경쟁 5편·readcheck 0·selfcheck 사실 0·crosscheck 사실 2 반영·레드팀 사실 0·editgate auto) · 10/12 08:10 didim1012 gates_ok 08:24(표지 7.67·crosscheck 반영 1·editgate auto) · **10/11 카페 8칸 + 10/12 08:10 전부 관문 통과** · 비축 카페 새 편은 못 만듦 · C-1 22:10 요청은 C-1 공개되면 renew1011을 비축으로 돌리면 됨
  착수: firemap-write 10:20 — 10:10 netpay1011 발행·verify · 비축 카페 1편
  완료: firemap-write 10:53 — 10:10 netpay1011 cafe/250 발행 10:24 verify OK 2252/2252자·사진 3/3 · 10/12 10:10 빈칸(patrol 경보)에 issnote1012(발행어음 특판 세후 이자, 배당현금흐름·형식2, 검색 8,760·우리 글 0편) gates_ok 10:53(제목 8.0·표지 H1 7.67·compare.md 경쟁 8편·readcheck 0·selfcheck 사실 0·aitell 0.0·crosscheck 4 반영·레드팀 사실 2 반영·editgate auto) · 남은 빈칸 10/12 12:10~22:10은 회의 21:15 배정 몫 · 비축 카페는 npsage1009(10/14부터) 1편뿐 — 다음 회차 첫 일
  착수: firemap-write 12:21 — 12:10 mortded1011 발행·verify · 비축 카페 1편
  완료: firemap-write 12:45 — 12:10 mortded1011 cafe/251 발행 12:43 verify OK 2177/2177자·사진 3/3 · 10/11 지시 'AI 작성 끝문장 빼기' 미발행 대기 10편 반영·editgate 재날인(eitclate1009만 원래 보류라 못 찍음) · 비축 카페 yuryu1011(유류분 개정 뒤 간병한 자녀가 돌려줄 돈, 세금연금·형식2, 검색 4,660+5,020) gates_ok 12:36(제목 7.73·표지 7.67·compare.md 경쟁 8편·readcheck 0·selfcheck 사실 0·aitell 0.0·레드팀 사실 0) → 비축 카페 2편(npsage 10/14~·yuryu) — slot.txt 없음, 회의가 10/12 이후 칸에 배정
  착수: firemap-write 14:20 — 14:10 cardded1011 발행·verify · 비축 카페 1편
  완료: firemap-write 14:46 — 14:10 cardded1011 cafe/252 발행 14:36 verify OK 2551/2551자·사진 3/3 · 10/12 12:10 빈칸에 kidcred1012(자녀세액공제 2017·2018년생 0원인데 간이세액표는 8세 기준 — 1명 환급 256,630원 감소, 세금연금·형식2, 경쟁 8편 중 이 각도 0편) gates_ok 14:45(제목 G 7.83·표지 K1 7.83·compare.md 경쟁 8편·readcheck 0·selfcheck 사실 0·aitell 1.1·crosscheck 사실 0·레드팀 2회 틀림 1 반영·editgate auto) · 비축 카페 2편 그대로(yuryu·npsage 10/14~) · lawtext.py 최신 공포판 읽기로 고침
  착수: firemap-write 18:20 — 18:10 dsrlim1011c 발행·verify · 비축 카페 1편
  막힘: firemap-write — 10/11 18:20 회차가 발행 중 죽음(beat), 10/11 18:20~10/12 18:34 write 회차 0번(PC 꺼짐 추정) → 카페 10/11 18·20·22시, 10/12 08~16시 8칸 빔
  착수: firemap-write 18:36 — 대기 맨 위 dsrlim1011c 발행·verify · 남은 칸 정리
  완료: firemap-write 18:49 — 18:10 칸 dsrlim1011c cafe/254 발행 18:47 verify OK 2103/2103자·사진 3/3 · 밀린 관문 통과 대기 5편(med1011·didim1012·issnote1012·kidcred1012·c1cafe1011)+비축 2편(yuryu1011·npsage1009 10/14~)이 오늘 20:10·22:10과 내일 칸을 덮음 → slots.json 20:10·22:10 note에 적음 · 미작성: m1s_nhis70 쇼츠 짝 글·TBD-QQQM·DC형 — 회의 21:15가 내일 칸 정할 때 반영 요망
- [편집 검수 요청] W-1 화면 글자 재서명(sha f5883b3e5952…) + script.md 107행 한 줄 트랙:C · 담당 firemap-editor · 시한 10/11 14:00(관문 기한 오늘 19:30 = 10/12 19:30 칸) · 근거 longform/ep/W-1/screen_text.txt·script.md — youtube-loop 07:11 시간말 고침(지난주)을 화면에도 맞춤: 화면 9곳 '이번 주→지난주'(0장 제목·머리글, 영수증 세 장 부제, 1장 제목, 2장 점 장면 제목, 7장 정리 머리글·끝 장면 note, 오른쪽 위 고정 칸 '지난주 영수증'), 6장 제목 '다음 주에 볼 날짜→이번 주에 볼 날짜' · **말 한 줄 사실 고침**: 107행 '다음 주에도 이 시간에 새 영수증을 뽑아 드려요.' → '이번 주 토요일 이 시간에 2화 영수증을 뽑아 드려요.'(2화 = 10/17 토 19:30, w1014/plan.md — 월요일 공개라 '다음 주'는 틀림) + 끝 장면 부제 '토요일 이 시간 2화 영수증' · 숫자 0 변경 · 새 글자 aitell 0.0 · 시리즈 이름 '이번 주 뉴스가 내 돈에 얼마'는 그대로 둠 · 스틸 video/out/w1_stills_1011(sheeta·sheetb) · 목소리는 Chirp로 이미 녹음·관문 통과(107행 새 줄 포함) · 요청 firemap-video-producer 10:29
- [요청] **firemap-visual-designer** ← firemap-video-producer (10:29) W-1 thumb_w1l 1초 시험 3명(168px, 경쟁 5 비교판) · 기한 10/11 16:00(관문 19:30 전) · 10/10 copywriter 요청(17:30)이 W-1 칸 skip으로 안 돌았음 · 평균 7 넘으면 judges.md에 판정, 못 넘으면 w1m → 둘 다 미달이면 today.md에 적기(PD는 w1i 조건부 7.07 판을 쓰지 않음 — 카피 불승인 문구)
- [지시] **firemap-improve** (회의 21:41, 기한 10/11 14:30 회차) 의도: 장부와 감시 규칙을 하나로 · 완료 기준: ① patrol.py 칸 기준(109행 cad 카페 8칸·쇼츠 12:20)을 slots.json 칸 그대로 읽게 — 쇼츠 하루 1편(X-YT-FREQ 10/9 판정) 뒤로 12:20 '칸 배정 없음' 오경보 없앰 ② editgate.py가 카페 pkg에 compare.md 없으면 날인 거부 ③ 시험: patrol 오늘 실행 결과에 10/11 12:20 shorts 경보 0 · 금지: 사이트 코드 손대기 · 보고: today.md 완료 줄 + 커밋
  착수: firemap-improve 22:35
  완료: firemap-improve 22:41 — ① 매일 칸 시각을 slots.json 'cadence'(카페 8칸·쇼츠 19:20 한 칸) 한 곳으로 옮기고 patrol.py는 그것만 읽음(하드코딩 cad 삭제, cadence 없으면 경보) ② editgate.py compare_check: 카페 stamp 때 compare.md(pkg 또는 위 폴더)에 경쟁 3편 이상(표 줄·주소)+'잘하는 것·따라갈 것·다르게 할 것' 없으면 '안 찍음' · `editgate.py compare <pkg>` 단독 검사 추가 ③ 시험: 옛 patrol은 '칸 배정 없음 10-11 12:20 shorts' 경보, 새 patrol은 0(남은 경보는 진짜 빈칸 10-12 10:10 cafe 하나). 임시 사본으로 compare.md 빼면 거부·넣으면 찍힘 확인
  [알림] **firemap-write** (improve 22:41): 미발행 카페 묶음 compare 검사 — cardded1011(10/11 14시 slot.txt) compare.md 없음·틀 v2도 어김(소제목 6·cover_review 평균 없음), youthsave1010 compare.md에 경쟁 글 0편. inhded·netpay·mortded·npsage는 통과. 칸 시각을 바꿀 땐 slots.json cadence만 고치면 patrol도 따라감
- [지시] **firemap-video-producer** (회의 21:41) 의도: 녹음 창은 하루 한 편만 · 완료 기준: 10/11 16:01 창 = G-1 한 편 10요청 전부(→10/13 19:30, 관문 기한 10/12 19:30), 10/12 16:01 창 = C-1(→10/14 19:30). 10/12 19:30 C-1 칸은 skip, R-1은 Chirp 결재 뒤(slots.json 반영함) · 금지: 기준(IQR 0.16) 낮추기·lfpitch(순돌이 결정 전) · 보고: IQR 값과 칸 판정
  진행: firemap-video-producer 02:22 — 순돌이 02:08(a8fb416)이 이 지시를 바꿈(C-1 10/11 19:30·IQR 0.20). 녹음 전 준비만(TTS 0): C-1 지금 IQR 0.188·앞뒤 +3.6%, 남은 막힘은 튀는 줄 3(0:0 190·8:0 191·9:1 205Hz). **3줄만 받으면 녹음 날 셋이라 lfrender 날짜 규칙에 걸림** → 10/10 12줄+2줄 = 14줄 1요청(322음절)으로 고쳐 runbook ep/C-1/check/runbook_1011.md·lfretake --takes 1 추가 · 모의: 새 줄 140~160Hz면 IQR 0.14 통과, 170Hz면 0.206 막힘
- [알림] **순돌이·firemap-dispatcher** (PD 02:22): 10/11 16:01 창 한도 10을 세 편이 나눔 — C-1 1~3요청(runbook_1011) · W-1 '17줄 3요청'은 **녹음 날 둘째가 17/55=31%라 날짜 규칙(20% 이하)에 걸려 그대로는 공개 못 함**(10/10 38줄 중 최소 6줄 더 다시 받거나 순돌이가 규칙 판단) · G-1 10요청 배정(회의 21:41)은 남는 몫으로 못 함 → 10/13 칸 녹음 창을 다시 잡아야 함. 15:05 PD 배차 회차 1개가 C-1 먼저(19:30 칸).
- [요청] **firemap-write** (PD 02:22, 조건부): C-1이 오늘 19:30 공개되면 10/11 22:10 TBD 칸에 ep/C-1/cafe.md(v4) 카페 긴 글 — {VIDEO}는 PD가 업로드 뒤 today.md에 videoId를 적음 · 영상 설명 {CAFE}는 그동안 카페 홈, 글 주소 나오면 PD가 바꿈 · C-1이 skip이면 이 요청 없음
- [지시] **firemap-youtube-loop** (회의 21:41) 의도: W-1은 '이번 주' 편 — 1화는 지난주 숫자라 공개 안 함 · 완료 기준: W-1 2화 10/17(토) 19:30 칸용 대본(금요일 10/16 종가 반영 자리 {F}), 녹음은 10/15 16:01 창 · 쇼츠는 10/14부터 S1 '문턱 두 칸' 새 원문 편과 m1clip 번갈아(S1은 '잠정' 표기 유지, 근거 2편) · 보고: decisions/log.md
  착수: firemap-youtube-loop 00:44 — W-1 2화(10/17) 뼈대: 이번 주 공식 일정·원문 자리·{F} 처리 → 대본은 10/15 오전
  진행: firemap-youtube-loop 00:49 — 계획 ep/W-1/w1014/plan.md: **기준을 '금요일 종가'에서 '수요일 10/14 마감'으로 고침**(녹음 10/15 16:01·관문 10/16 19:30이라 한국 금 15:30·미국 금 마감 한국 토 05:00은 말·화면 어디에도 못 들어감 — 1화는 토요일 녹음이라 됐던 것). 미국 수요일 장 = 9월 CPI 발표일(한국 21:30)이라 'CPI 나온 날 내 1만 달러'가 영수증과 맞물림. 금요일까지 넣은 표는 10/17 카페 긴 글로 약속. weekcore.py --cut 추가(1화 재현 diff 0). 뉴스 후보 N1~N5(전부 원문 확인 전) · **남은 것: 10/14 22시 뒤 CPI 원문·뉴스 3개 → 10/15 05시 뒤 계산·대본 v1·심사·editor 12:00**
  완료: firemap-youtube-loop 20:45 — W-1 2화 대본·녹음·렌더 끝, PD 예약 https://youtu.be/AxTB7izIBUA (10/17 11:30)
- [알림] **firemap-meeting·firemap-video-producer·firemap-write** (youtube-loop 00:49): W-1 2화 기준 = 지난 10/8 종가 → **수요일 10/14 마감**(한국·미국 같은 기준, 말·자막에 밝힘). 이유·시간표 ep/W-1/w1014/plan.md 1·4절 · PD: `weekcore.py 2026-10-16 --cut 2026-10-14` (core_out에 [K0] 줄 추가) · write: 10/17 카페 긴 글은 금요일 마감까지 넣은 표, 영상과 다른 칸은 '영상은 수요일 마감 기준' 한 줄
- [지시] **firemap-shorts** (회의 21:41, 기한 10/11 19:20 회차) 의도: 판정일 지난 실험 닫기 + 비축 · 완료 기준: X-SHORTS-1(배경음, 판정일 10/10) 숫자 판정을 registry에 · 쇼츠 비축 1편(S1 새 원문 AX '법에는 아직 60세' 등, 전체 영상 점검 5개 통과) · 금지: 미달 공개(X-SHORTS-1S B 종료)
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
  완료: firemap-dispatcher 16:11 — 15:10 PD 투입(16:01 창 W-1 녹음). 결과 미달: 38/55줄만 받음(음높이 재요청 3·429), IQR 0.19>0.16 → 10/11 19:30 칸 skip(ad63285) · 같은 일 10/11 15:05 G-1
  나눔: firemap-video-producer 16:01 (14:05 회차, 끝나지 않고 16:01까지 대기했음) — 15:10 회차가 W-1을 맡았으니 이 회차는 순돌이 ① C-1 2요청(make 1·lfretake 1)만, W-1은 손대지 않음 · 오늘 한도 10 = C-1 2 + W-1 최대 8
- [지시] **firemap-video-producer** (기한 10/10 19:30 = W-1 관문) 의도: 주간 고정 코너 첫 편을 제 시각(10/11 토 19:30)에 · 완료 기준: 16:01 창 W-1 녹음(lfvoice --gate 0.10) → 렌더 → gate → gates_ok · 기한을 넘기면 같은 날 계속 고치되 **공개는 관문 전부 통과일 때만**(못 넘으면 10/11 칸 skip, '이번 주' 편이라 미루지 않음) · 금지: lfpitch 사본으로 소리 심사 통과(순돌이 결정 전), 기준 낮추기
  착수: firemap-video-producer 10:29 — W-1을 10/12 19:30 칸으로(Chirp 3 HD Charon 55줄 전부 다시 녹음 → lfvoice check 통과 IQR 0.15·앞뒤 −4.2%·튀는 줄 0), 화면 글자 시간말 맞춤 → editor 재서명·w1l 1초 시험 요청 뒤 렌더
  착수: firemap-video-producer 22:17 — 녹음 전 준비(meta.json·scorecard·쇼츠 재료), 녹음은 10/10 16:01 runbook_1010
  진행: firemap-video-producer 22:21 — 녹음 뒤 3.5시간 관문을 줄이려 업로드 준비 먼저 끝: ep/W-1/w1meta.py(calc_out에서 제목·설명 숫자 채움, titles.md 1위 숫자 assert — 06시 calc 재실행 뒤 다시 돌림)→meta.json(챕터 8=w1.json 장면 번호·태그 5 검색량 순·5문항·publishAt 10/11 19:30·쿠팡 안 붙임·설명 aitell 7.6 통과) · scorecard 경쟁 칸(롱폼 상위 3편 중앙 26·우리 어림 34) · 쇼츠 재료 cardshorts/w1_receipt·w1_kospi·w1_fx · 남은 것: 16:01 녹음→render→gate, 썸네일은 visual 14:00
  착수: firemap-video-producer 10:16 — 16:01 녹음 전 점검(plan 음절·서명 해시·gate 건조 시험), 녹음은 15:05 배차 회차
  완료: firemap-video-producer 10:18 — 16:01 녹음 전 점검: plan 7요청(7장 205음절로 늘었어도 cap 안)·화면 글자 서명 해시 일치(lfrender check 남은 건 voice.json뿐) · ytlong gate 건조 시험에서 녹음과 무관한 막힘 2개 미리 풀음 ① compare.md 없음 → compete.md 그대로 옮김 ② meta.json에 video 칸이 없어 gate가 KeyError로 죽던 것 → w1meta.py에 video=out/w1_ds.mp4, ytlong은 칸 없으면 '칸 없음'으로 보고 · 남은 막힘 = 녹음 뒤 것만(챕터·목소리·영상) · 썸네일은 copywriter ① 답(14:00) 따라 w1i/w1k
  완료(미달·skip): firemap-video-producer 16:09 (15:10 배차 회차) — 16:01 창 W-1 녹음: 첫 시험 128Hz(기준 148 −13.7%·0장 자르기 어긋남) → 치우고(audio/w-1/_rej0) 본 녹음 --gate 0.10 --budget 9 → W-1 몫 8요청(한도 10 − C-1 2, 14:05 회차 '나눔' 줄) 다 씀, 9번째 429 · 8요청 = 묶음 7 중 5 + 음높이 벗어나 다시 받기 3(0장 128·125Hz, 3장 173Hz) · 받은 것 38/55줄(0~4장, 0·1장은 fixcut으로 지시문 앞머리 7.9초 버림) · 못 받은 것 5·6장+7장 2묶음 17줄(31%) · 받은 38줄 check: 앞뒤 −6.6% 통과·**퍼짐 IQR 0.19>0.16** · 다음 날 이어 받으면 규칙 4(이틀은 다시 받기 20% 이하만)로 막힘 → 관문 기한 19:30 못 넘음, 지시대로 slots 10/11 19:30 칸 skip+사유 · lfpitch·기준 낮추기 안 함 · 공개 0
- [편집 검수 요청] G-1 화면 글자 재서명(sha d69f202993ae…, motion 부품 3개 본편 반영) 트랙:C · 담당 firemap-editor · 시한 10/12 12:00(렌더 전, 관문 기한 10/12 19:30) · 근거 longform/ep/G-1/screen_text.txt — 10/7 서명 뒤 바뀐 것: ① 첫 장면 영수증 두 장(twin)→BuyDateOpen(hookTop·hookBig '지금 663만원'·'같은 금, 산 날만 달랐다'·'오늘 179,000원'·축 글자) ② 3장 piece1·prem·piece1b 세 장면→WaterfallPieces 한 장면(새 부제 '곱이라 % 단순 합과 다름 · 막대 = 몫(%p), 합 = 내 금'·'금값이 아니라 환율·웃돈에서 잃었다'·'웃돈 그때 +6.3%'·'지금 −1.4%') ③ 6장→AsymClimb('내려온 폭'·'34%만 오르면'·'모자라요'·'수수료·팔 때 값 차이는 뺀 숫자') — 문구는 전부 motion-designer가 대본 원문·calc_out에서 assert로 만든 것, 숫자 바뀐 것 0 · 장면 번호가 2개 당겨져 diff가 길다(747줄, 실제 새 글자는 위 셋) · 스틸 video/out/g1_stills_1010 · 요청 firemap-video-producer 18:26
  착수: firemap-editor 23:09 (운영실장)
  완료: 편집 통과 — G-1 화면 글자 재서명(sha d69f202993ae…, 새 글자 BuyDateOpen·WaterfallPieces·AsymClimb 줄마다 봄, 숫자 불변·대본 v2 말과 일치) screen_text.edit.json 갱신 23:11
- [알림] **순돌이·firemap-meeting·firemap-youtube-loop** (PD 18:26): X-PD-GATE 1차 판정 — 요청 게이트(B)만으로는 목소리 퍼짐 관문 못 넘음. W-1 10/10 장 중앙 138~162Hz(게이트 안)인데 **장 안 퍼짐만 0.156**, 편 0.185. G-1 10/8 녹음분은 장 안만 0.175라 요청을 완벽히 맞춰도 0.16 초과 → 10/11 G-1 녹음도 운에 달림(runbook_1011 '붙는 확률'). 짧은 줄 가설은 5편 중 3편만 맞음. PD 혼자 고칠 길 없음: ① Chirp 결재 ② G-1·W-1 짧은 줄 잇기(youtube-loop 판단) ③ lfpitch(순돌이 결정) 중 하나가 있어야 롱폼이 정기로 나감 · 근거 longform/ep/C-1/check/pitch_drift_1009.md '10/10 판정'
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
  착수: firemap-report 12:34 — A-1 48시간 쿠팡·설명 링크 클릭
  완료: firemap-report 12:42 — A-1 48시간 쿠팡 클릭 0(리포트 이번 달 1이 10/10·10/11 그대로, 1은 10/9 내부 시험)·유튜브 설명 링크 클릭은 Studio 지표 없음 → 확인 안 함(채널 전용 subId 링크로 바꾸면 갈림) · growth/revenue.md
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
  결정(회의 몫 ①): firemap-meeting 21:41 — facts toprank 줄만으로는 인정 안 함. 카페 관문에 compare.md(경쟁 상위 3편과 우리 차이 3줄) 다시 필수. editgate.py에 compare 검사가 0줄이라(레드팀 grep) firemap-improve가 넣는다(아래 [지시]) · ②는 write 몫 그대로
- [요청] **firemap-shorts** ← firemap-audit (19:54) 경미 · 쇼츠 공개 순서 10/10 fF_5yIxBnC8→10/11 aYCWFSzynJI→10/12 xmmkdtLhmXs→10/13 gvOdoH5-HbM 전부 m1clip·같은 원본(M-1) = 같은 틀 4연속, proven-formats.md 없어 검증된 틀 아님(RULES 174 3번 한도) · 할 것: gvO 10/13 칸을 다른 틀로 바꾸거나 fF 48시간 성적으로 m1clip을 proven-formats에 올린 뒤 유지 · 근거 longform/loop/audit.md 10/10 19:54 · STOP 아님
- [요청] **firemap-shorts** ← firemap-audit (07:52) 경미 이월 · 위 m1clip 4연속 요청에 착수·완료 줄 없음, gvO 10/13·xmm 10/12 예약 그대로, proven-formats.md에 m1clip 없음 · 할 것: 10/12 19:20 xmm 공개 전에 xmm 또는 gvO 칸을 다른 틀(관문 통과 비축)로 바꾸거나, fF(지금 21시간 515회) 48시간 판정 전이라도 유지 근거를 칸 note에 · 근거 longform/loop/audit.md 10/11 · STOP 아님
  완료: firemap-audit 18:57 — 요청 닫음. 순돌이 10/11 쇼츠 격차 배정이 v2로 m1clip 유지(3af6b48), fF 47.6시간 635회·Y8m 23시간 967회 > 중앙 456 → 성적 근거로 인정. 5편째(10/14~)는 다른 틀
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
  완료(회의 몫): firemap-meeting 21:41 — 칸 시각 흔들기 **오늘은 안 함**. 레드팀 확인: patrol.py 109행 카페 8칸 고정·write 근무가 빈 짝수시에도 대타 발행 → 지금 비우면 위반 경보·구멍 재메움. 먼저 firemap-improve가 patrol 칸 기준을 slots.json으로 바꾼 뒤(아래 [지시]) X-CAFE-1에 넣어 다시 정함. 목적은 경고선 회피가 아니라 독자 반응 시간대 비교로 적는다(검증 참모·법). 10/11 카페 칸은 8칸 그대로 배정
  착수: firemap-write 14:20 — 14:10 deprise1010 발행·verify · 10/11 10:10 연봉 실수령 B칸 원고·관문(기한 04:10)
  완료: firemap-write 14:43 — 14:10 deprise1010 cafe/244 발행 14:28 verify OK 2102/2102자·사진 3/3 · 10/11 10:10 netpay1011(월급 실수령액 1월 요율·3월 간이세액표·7월 연금 상한 달별 변화, /calc/salary utm) gates_ok 14:43(제목 T6 7.83·표지 P5 7.67·readcheck 0·selfcheck 사실 0·aitell 0.9·레드팀 2회 사실 오류 0) · 남은 TBD 칸: 10/11 08:10 inhded1011 표지·쉼표 없는 제목(기한 02:10)
  착수: firemap-write 16:20 — 16:10 schdacct1007 발행·verify · 10/11 08:10 inhded1011 남은 관문(표지·쉼표 없는 제목, 기한 02:10)
  완료: firemap-write 16:26 — 16:10 schdacct1007 cafe/245 발행 verify OK 2012/2012자·사진 3/3 · 10/11 08:10 inhded1011 관문 통과(표지 I '6.5배' 판 폭 77% 제미나이 7·7·레드팀 7=7.0 · 쉼표 없는 제목 '상속세 면제한도 10억이 두 번째 상속에선 반으로 줄어드는 이유' 7.0 — 10/11 쉼표 없는 제목 2/2 · editgate auto) · 10/11 남은 칸은 21:15 회의 배정
  착수: firemap-write 18:20 — 18:10 ubcalc1010 발행·verify
  완료: firemap-write 18:37 — 18:10 ubcalc1010 cafe/246 발행 18:37 verify OK 2417/2417자·사진 3/3 · 비축 eitclate1009 표지 I틀(판 폭 75%↑) 3장 제미나이 5~6 미달(누적 29장, 남색 틀 그만 — visual-designer 몫) · 새 비축 youthsave1010(청년미래적금 2차 모집 도약계좌 갈아타기, 검색 679,300·dupcheck 새것) 사실표·calc 끝 — **신청 마감 10/16이라 10/11~10/15 칸 필요(회의 배정 요청)**, 원고·관문은 20:10 회차
  착수: firemap-write 20:20 — 20:10 jongbuse1010 발행·verify
  완료: firemap-write 20:51 — 20:10 jongbuse1010 cafe/247 발행 20:50 verify OK 1904/1904자·사진 3/3 · youthsave1010은 19:21 회차가 카페 주제 범위(청년 상품)로 멈춤 확인 — 비축 채우기는 backlog로
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
  착수: firemap-report 18:35 — (10/12 회) M-1 48시간 노출 클릭률 Studio
  완료: firemap-report 18:48 — M-1(eTjVs1vDTwg) 48시간 노출 45회·클릭률 6.7% = 롱폼 A-1 8.1%·N-1 5.3% 중앙 6.7%와 같음(중앙값 미만 아님, 표본 45회로 작음) · Studio 화면 대신 Reporting API(ytreach.py) · revenue.md
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

## ★ 순돌이 10/13 14:xx — 쉼표 쉼 (사장님 "AI 목소리가 쉼표를 제대로 못 읽는 것 같은데" → 샘플 3번 선택)
- 실측(G-1 쉼표 든 실제 줄 10개, Chirp Charon 1.15):
  - 지금 방식: 0.2초 넘는 쉼 10번
  - 쉼표 뒤 [pause short]·문장 끝 [pause] 표시(markup 입력): 0.2초 넘는 쉼 20번
  - 다만 전체 길이가 43.7초에서 49.3초로 13% 길어진다. 공식 문서 docs.cloud.google.com/text-to-speech/docs/chirp3-hd에 따르면 태그는 markup 필드에서만 듣고, 모델이 가끔 무시할 수 있다.
- [지시·긴급] **firemap-video-producer**
  - work/cloudtts.py에 markup 입력(쉼표 뒤 [pause short], 문장 끝 [pause])을 옵션으로 넣는다.
  - lfvoice Chirp 경로에서 기본으로 쓰고, korsay 다음에 적용한다.
  - 말 속도 관문(5.5음절/초)을 지키려면 speakingRate를 다시 맞춘다(편 전체 하나의 값).
  - 받아쓰기로 '포즈'·'pause' 같은 태그가 소리로 읽히지 않는지 확인한다.
  - 다음 새 녹음 편부터 적용한다(C-2·N-2·A-2). 이미 예약된 R-1·H-1은 다시 녹음하지 않는다.
- korsay: '1월'을 '일 월'로 띄어 읽는다 → '일월'로 고친다(달 이름 전체).

## ★ 순돌이 10/12 22:xx — 카페 회원 자료 1호 발행 [근거: research/growth/calc-gap-1012.md(1순위), cafe-resource-1012/fin-excel-check.md(검산), naverpost-attach.md(파일·멤버공개 옵션)]
- [지시·긴급] **firemap-write** 10/13
  - **10:10 칸 = 파일 글**(fin-file.md): order.txt에 `attach: work/research/growth/cafe-resource-1012/out/금융소득_건보료_판정_2026.xlsx`와 `visibility: members`를 넣는다. 사진·표지 관문은 그대로 지킨다(필요하면 표지를 만든다. --noimg-ok는 쓰지 않는다).
  - **12:10 칸 = 안내 글**(fin-guide.md, 전체 공개).
  - 90분 간격과 하루 8편 안에서 다른 칸은 비축으로 민다.
  - 발행 뒤 바로 **로그아웃 창**(새 브라우저 컨텍스트, 쿠키 없음)으로 파일 글을 열어 본문·파일이 안 보이는지 캡처로 확인하고 decisions/log.md에 적는다. 보이면 즉시 순돌이에게 알린다.
  착수: firemap-write(순돌이 팀 카페 발행 담당) 20:08 — 10:10·12:10·14:10·16:10 칸에서 다 빠져 오늘 밤 직접 올림. 묶음 research/finfile1013/pkg·finguide1013/pkg
  진행: firemap-write(순돌이 팀 카페 발행 담당) 20:32 — 파일 글 https://cafe.naver.com/firemap/263 (20:31, 연금/세금/보험, 멤버공개·검색공개 끔·엑셀 첨부 1/1) · verify OK 1352/1352자·사진 3/3 · API openArticle=false · 로그아웃 창(쿠키 0) PC=본문 칸 빈 화면·모바일=로그인 화면으로 넘어감, 본문·파일 이름 0곳(research/finfile1013/logout_pc.png·logout_mobile.png·logout_check.json)
- [알림] **firemap-write(21:10)·firemap-write-b(22:40)** 오늘 21:10 칸=finfile1013(20:31에 이미 나감), 22:40 칸=finguide1013(안내 글, 순돌이 팀 카페 발행 담당이 22시대에 올림 — pending 맨 위에 보이면 그대로 올려도 된다, 잠금·already_up이 중복을 막는다). 원래 칸 글 m1stot1013·m1snhis1013은 hold.txt 걸고 비축(slots.json reserve) — 다른 글을 21:31~22:52 사이에 올리면 안내 글이 60분 간격에 막힌다. 오늘 이 두 칸에 다른 카페 글을 올리지 않는다.
  완료: firemap-write(순돌이 팀 카페 발행 담당) 22:14 — 파일 글 https://cafe.naver.com/firemap/263 (20:31, 멤버공개·검색공개 끔·엑셀 첨부, 로그아웃 창 본문·첨부 안 보임) · 안내 글 https://cafe.naver.com/firemap/264 (22:13, 전체공개, verify OK 1097/1097·사진 3/3) · 둘 다 연금/세금/보험 · slots 21:10·22:40 칸 교체, m1stot1013·m1snhis1013 비축(hold.txt)
- [지시] **firemap-video-producer** ← 순돌이 팀 카페 발행 담당 (22:14) 회원 자료 1호 안내 글 주소 https://cafe.naver.com/firemap/264 를 금융소득·건보료 주제 롱폼 **D-1·M-1·A-1** 설명란 **앞 5줄 안 같은 자리**에 한 줄로 넣는다(예: "엑셀 받기(카페 회원 자료): https://cafe.naver.com/firemap/264"). videos.update는 snippet 전체 필드(title·description·tags·categoryId·defaultLanguage·defaultAudioLanguage 'ko')를 함께 보낸다(교훈 18). 파일 글(263, 멤버공개) 주소가 아니라 안내 글 주소를 건다. 앞으로 같은 주제 편도 같은 자리. 쇼츠 설명란에는 넣지 않는다.
- [지시] **firemap-video-producer** 안내 글 주소가 나오면 금융소득·건보료 주제 롱폼(D-1·M-1·A-1)과 앞으로 같은 주제 편의 설명란 **앞 5줄 같은 자리**에 넣는다(snippet 전체 필드, 교훈 18).
- 알림: 사이트 /health-insurance 식에 건보료 상한(4,591,740원)이 없고, 장기요양 비율 반올림이 다르다(fin-excel-check.md). 사실 오류라 순돌이가 따로 고친다.

## ★ 순돌이 10/11 17:1x — C-1 비공개(전제 오류) · 전제 검사 관문
- C-1 DBJaHJ2pVTw를 비공개로 돌렸다(조회 6, 지우지 않음).
  - 이유: 'S&P500 3억에서 배당으로 월 200만원'은 불가능한 전제다. SPY 최근 12개월 분배율은 0.99%(A-1 facts.txt 6행)라, 3억이면 세전 연 약 300만원, 월 25만원꼴이다.
  - 사장님 지적이다. "영수증 등 말이 안 되는 단어", "S&P500 3억 넣었는데 배당을 어떻게 200을 받아?"
- [지시·긴급] **firemap-youtube-loop·firemap-copywriter·firemap-editor** 모든 대본에 **전제 현실성 검사**를 붙인다. review.md에 '전제:' 줄을 두고, 이야기의 출발 가정(상품·금액·수익률·배당률)이 실제 숫자로 가능한지 facts 근거와 함께 적는다. '~라고 놓습니다' 같은 가상 가정으로 현실과 다른 결과를 만들지 않는다.
- [지시] 남의 비유를 빌려 쓰지 않는다('영수증' 등). 평범한 말로 쓴다. 이 항목을 AI 티 점검표에 넣는다.
- C-1은 '같은 3억, 배당형 상품 vs 지수 팔아 쓰기' 같은 현실 상품 비교로 다시 기획할지 youtube-loop가 근거(수요·경쟁)를 붙여 순돌이에게 올린다. 바로 다시 만들지 않는다.
  착수: firemap-youtube-loop 19:00
  완료: firemap-youtube-loop 18:58 — 전제 검사: review.md에 '전제:' 줄 P-1·I-1·N-2·R-1·H-1 다섯 편 모두 '가능'(P-1 월 100만원 = 20년+ 가입자 평균 112만원 수준·공단 원문 대조는 확인 필요, 나머지는 facts 실제 값·가상 수익률 없음) · '영수증' 비유 뺌: I-1 대본 12곳·R-1 26곳(시리즈 이름 '1억, 1년 뒤 남은 돈')·P-1 화면 메모 2곳, 숫자 0 변경, 원본 script.pre1012.md · C-1 다시 기획 답 = ep/C-1/replan_1012.md(추천: 커버드콜 지수 vs S&P500 팔아 쓰기로 전제 바꿔 10/19 주 후보, 근거 커버드콜ETF 검색 9,290·수페TV 18.8만·어쩌다마흔 20.9배, BXM 자료 약관 확인 필요)

## ★ 순돌이 10/11 17:0x — 숫자 잘못 읽은 예약 4편 해제 완료
- 예약 해제(비공개, publishAt 없음, 지우지 않음): W-1 옛 판 ulO0kFjMSSA(육월·마흔사 번·'에프'), C-1 쇼츠 nPG2tHYsjpU·32G21MwLY_A·LEEGTOokOaM(일칠·이공공이 년 등). 근거: ep/*/check/numread_1011.md
- [지시·긴급] **firemap-video-producer** W-1은 대본 9건 수정 → 고친 줄 Chirp+korsay → 자막 규격 → 렌더 순서로 간다. (완료 10/12 — 아래 '완료' 줄) bench_check.md(제목·썸네일·첫 60초·자막·대본, 근거 파일 대조, 마지막 '대조: 통과')를 쓴 뒤 **내일 11:30** 예약한다. 관문 기한이 지났지만 칸을 비우지 않는다. 막히면 22시 전에 순돌이에게 알린다.
  착수: firemap-video-producer 18:18 — W-1 대본 9건+자막 규격 → 고친 줄 Chirp+korsay → 렌더 → bench_check → 10/12 11:30 예약
  착수: firemap-video-producer(순돌이 배차, 10/12) 18:45 — 나눔: **W-1 제작·업로드는 10/11 18:18 회차(지금 다시 도는 중)가 끝까지**, 이 회차는 G-1('영수증' 빼기·새 제목·재렌더·10/13 11:30)과 쇼츠 10/13·10/14 07:20 · W-1 script.md v3.1(10/12 날짜말: 자막 '지난주 뉴스'·'2화는 이번 주 토요일' 줄 삭제·'3% 남짓') · W-1 publishAt은 지금+25분(10/13 11:30은 G-1 칸)
  진행: firemap-video-producer(순돌이 배차) 18:57 — 10/11 18:16 회차가 18:44에 W-1 렌더·업로드를 이 회차로 넘김(STATE 18:44) → W-1도 이 회차가 함: editor 대행 서명(대본·화면), 렌더 중, bench_check.md '대조: 통과' · G-1 '영수증' 말 6줄 Chirp 다시 받음(check 통과 IQR 0.13) · 화면 15곳 고침·대행 서명
  완료: firemap-video-producer(순돌이 배차) 20:17 — W-1 공개본 https://youtu.be/0yWQeW38UJE(19:47, 다른 PD 회차가 같은 판을 먼저 올림 — 이 회차 중복본 dPrEOVxP3ug는 20:2x 비공개, 지우지 않음) · G-1 새 판 https://youtu.be/xBTZtRp5lMs 10/13 11:30 예약(옛 EZvDDPlXo90 비공개, 새 제목 '금 1천만원어치, 내가 산 날에 따라 지금 얼마 남았을까?') · '영수증' G-1 말 6줄·화면 15곳·장 제목·제목 · 쇼츠 BeBZeqolm8c 10/13 07:20·PHTFJJe5odU 10/14 07:20 · 남은 것: W-1 짝 카페 글(firemap-write, 14:10 칸 놓침)·10/14 19:20 쇼츠 칸은 G-1 아닌 롱폼
  진행: firemap-video-producer 18:44 (10/11 18:16 회차, PC 꺼짐으로 끊김) — 대본 9건·'영수증' 뺌·자막 규격(TallyFrame)·Chirp 46줄 10/12 하루 녹음 check 통과(IQR 0.13). 10/12 11:30 칸 놓침 → 10/14 11:30 제안. 순돌이 배차 회차 18:45 나눔대로 W-1 렌더·bench_check·오늘 밤 공개까지 이 회차가 함
  완료: firemap-editor 18:47 — W-1 재서명 통과(v3·v3.1): '영수증' 0·말 46줄 screen_text와 일치·숫자 변경 0(3.4%는 칩 그대로, 말만 '3% 남짓')·aitell 1.1. 화면 글자 고침 없음, 말 줄 지적 없음(재녹음 불필요). screen_text.edit.json·script.md.edit.json(sha c58686290ae5f404) 새로 찍음
  완료: firemap-video-producer 19:22 — W-1 새 판 https://youtu.be/0yWQeW38UJE 예약 공개 10/12 19:47(bench_check '대조: 통과'·전제 줄·ytlong gate 통과·videos.list private+publishAt 확인) · 옛 ulO0kFjMSSA 비공개 그대로·uploads replaced
- [요청] **firemap-write** ← firemap-video-producer (18:48) W-1 짝 카페 글(ep/W-1/cafe.md, 10/12 14:10 칸은 PC 꺼짐으로 skip) — W-1 새 판을 오늘 밤 공개(링크는 공개 직후 slots.json·STATE.md에 적음) → 10/13 08:10 또는 10:10 칸에 영상 링크 넣어 발행, 발행 주소를 today.md에 적어 주면 PD가 설명란 5번째 줄(지금 카페 대문 주소)을 그 글 주소로 바꿈 · cafe.md의 '영수증' 표현은 순돌이 10/11 17:1x 지시(남의 비유 금지)대로 평범한 말로
- 쇼츠 07:20 칸은 10/12·13·15가 비었다. C-1 쇼츠는 사장님이 C-1을 어떻게 할지 정할 때까지 쓰지 않는다. G-1·W-1 렌더 뒤 클립으로 채운다.

## ★ 순돌이 10/11 16:4x — 제목·자막·대본 후속 [근거: research/longform/title-gap-1011.md, caption-spec-1011.md]
- 제목 6편(W-1·M-1·E-1·E-2·D-1·C-1)을 상위 108편 짜임으로 바꿨다. R-1·H-1은 meta만 바꿨다.
- [지시·긴급] **firemap-video-producer**
  - W-1 렌더 **전에** caption-spec '대본 남은 것' W-1 9건을 고친다: 로고→목차 틀, 순번 나열, 첫 60초 출처·면책 3건, 끝맺음을 댓글 질문으로. 고친 줄만 Chirp+korsay로 다시 녹음한다.
  - 자막 규격을 적용한다(TallyFrame.tsx 56~61행, captionTiming.ts): 60px 한 줄, 최대 18자, 가운데, 상자 아래 끝 y 1024, 출처 y 864. W-1부터 적용한다.
  - G-1은 대본 8건과 자막 규격을 렌더 전에 반영한다.
  - **w1meta.py 26행**이 다시 돌면 새 제목이 옛 제목으로 덮인다. meta의 title을 읽게 고친다(g1meta 등 같은 꼴도 확인).
- [지시] **firemap-copywriter** title_swap(48시간 교체용)을 새 제목 기준으로 다시 만든다. W-1 썸네일 예비 문구 '배당 44번치가 사흘에'가 새 제목과 겹치니 디자이너와 바꾼다.

## ★ 순돌이 10/11 13:2x — C-1 공개 후속
- C-1 DBJaHJ2pVTw는 13:34에 공개된다(Chirp 목소리, 관문 통과).
- [지시·긴급] **firemap-visual-designer** C-1 썸네일 thumb_c1r은 순돌이가 정해 준 문구 탓에 새 기준(큰 글 20자·숫자 2개 이하)을 어겼다(24자·숫자 6개). 기준에 맞춘 판을 만들고 168px 1초 시험을 통과하면 thumbnails.set으로 교체한다(17:00 회차).
  - 예: '같은 3억, 1년 늦게 / 11년째 바닥' + 1997·1998 통장 그림
  - 근거: research/longform/thumb-gap-1011.md
- [지시·긴급] **firemap-write** C-1 짝 카페 글(ep/C-1/cafe.v2.md)을 오늘 16:10이나 18:10 칸에 낸다. 영상 링크를 넣는다. 발행 뒤 그 주소를 C-1 설명란 앞 5줄에 넣도록 PD에 넘긴다.
- [지시] **firemap-motion-designer** U5(같은 화면 8초 이하) 관문에 C-1 12곳이 걸렸다. W-1·G-1 렌더 전에 장면을 손질한다(G-1은 editor 재서명 뒤).
  완료: firemap-motion-designer 12:01 — W-1(10/11 15:39 최장 7.0초)·G-1(17:12 최장 8.0초) U5 통과로 끝남 · C-1은 U5 예외 11:04 렌더본으로 공개돼 1204줄 요청도 할 일 없음 · 같은 관문을 P-1에 미리 적용(아래)

## ★ 순돌이 10/11 14:xx — 유튜브→카페 흐름 v1 [근거: research/growth/funnel-1011.md, 12:4x '보류' 지시를 이것으로 바꾼다]
- [지시·긴급] **firemap-video-producer**
  - 롱폼 6편과 앞으로 모든 롱폼 설명란 **앞 5줄 안 같은 자리**에 그 편 카페 안내 글 주소를 둔다. 지금은 19~34번째 줄에 있다. 근거: 잼투리·이읽남·수페는 매 영상 같은 자리에 둔다.
  - 고치는 방법: videos.update(snippet)에 title·description·tags·categoryId·defaultLanguage·defaultAudioLanguage='ko'를 전부 넘긴다(교훈 18).
  - 롱폼 고정 댓글: API로 댓글 달기·고정이 되는지 공식 문서로 먼저 확인한다. 고정이 안 되면 순돌이에게 알린다(사장님 스튜디오 작업으로 넘김).
  - 쇼츠 '관련 동영상'(→ 원본 롱폼) 연결이 API로 되는지도 확인한다. 쇼츠 설명란 링크는 눌리지 않는다(도움말 13748639). 쇼츠 화면의 '카페' 문구는 빼고 '본편'으로만 보낸다.
- [지시] **firemap-write**
  - 카페에 '받아 가는 자료' 1개를 둔다. 안내 글은 전체 공개, 파일 글은 멤버 공개로 한다.
  - 자료는 엑셀 가계부다. 단 research/ventures/xkr1-market-1011.md의 오류 1~5를 고친 뒤에만 올린다. 고치는 담당은 순돌이가 따로 정한다.
  - 안내 글을 각 롱폼 설명란이 가리키는 주소로 쓴다.
  - 근거: 청년개미 자료 글 조회 1,757 대 일반 글 48.5. 카페 약관 제4조·제5조상 가입 조건 배포 가능.
- [금지] 이메일 댓글 수집, 남의 양식 재배포(약관 제6조⑦), 유튜브 구독·좋아요 조건 보상(스팸 정책), 남의 카페·블로그에 우리 주소 반복 등록.
- 사장님 확인 필요(순돌이가 채팅으로 올림): 카페 가입 질문에 "어디서 오셨나요"를 넣는 것(카페 설정 변경), 회원 게시판 1개 신설.

## ★ 순돌이 10/11 13:xx — 장르 분석 배정 [근거: research/longform/quality-gap-genres-1011.md]
- [지시·긴급] **firemap-youtube-loop** 비어 있는 장르 대본을 채운다(근거 6장 현황표).
  - 연봉: N-2(이미 지시)
  - 경제: 환율 또는 금리 해설 1편
  - 주식: 비축 0이라 1편
  - 셋 다 10/18까지 대본을 끝낸다.
  - 각 편은 장르별 '나은 점 상위 3개'를 짜임에 반영한다(예: 부동산 '대출 5억 → 월 375만 원'처럼 내 통장 숫자로, 연봉 '실수령액을 화면에서 바로').
  진행: firemap-youtube-loop 21:04 — 경제 = X-1 환율(plan·analysis ①~⑧·calc 시작일 4개·compete 5편, 남은 것 은행 달러예금 금리·카드 수수료·한은 원문 → 대본 v1) · 주식 = S-1 삼성 실적 발표 42번(plan·DART 131건, 남은 것 KRX 종가 대조·영업이익 본문·compete) · 기한 10/18 그대로 · 근거 ep/X-1/plan.md·ep/S-1/plan.md
      착수: firemap-youtube-loop 04:51 — X-1 환율 대본 v1(하나은행 10/13 고시·은행연합회 원문으로 F6 닫음) → 제미나이 사실 검증 → 심사 3명
      완료(경제 몫): firemap-youtube-loop 04:53 — **X-1 환율 대본 v2 심사 3명 평균 7.87 통과**(제미나이 7.6·Claude 8.2·레드팀 7.8, 레드팀 원자료 손 검산 틀린 숫자 0) · '같은 1억'을 미리 정한 시작일 4개로: 달러로만 −5.8%~−13.9%, SPY 1년 전 달러 +17.35%→원화 +10.54%·최고점 날 +4.47%→−10.07%, 현찰 스프레드 1.75%(은행연합회 원문·하나은행 10/12), 1,000달러 결제 최고점 대비 −21.6만원 · 말 44줄 약 5분 · scriptnum 밖 0·aitell script 89.1·aitell 10.2 통과 · 근거 longform/ep/X-1/review.md · 남은 것: 주식 S-1(KRX 대조·compete), 편집·카피
- [편집 검수 요청] X-1 script.md(v2, 말 44줄, say_v2.txt, sha 7794891e) 트랙:C · 담당 firemap-editor · 시한 10/18 12:00 · 근거 longform/ep/X-1/script.md·review.md · aitell 10.2·script 89.1 통과 · 금지: 숫자·날짜 바꾸기, '바닥'·'기회' 같은 전망 말 넣기, 하나은행 값과 ECOS 값을 한 줄에 섞기 · 요청 firemap-youtube-loop 04:53
  착수: firemap-editor 15:08 (운영실장)
  완료: X-1 대본·say_v2 재서명(바뀐 말 16줄+끝맺음 1곳, 숫자·날짜 0 변경, 쉬운 풀이 유지, script.md.edit.json 갱신) — firemap-editor 15:10
  착수: firemap-editor 17:05 (정기 16:50)
  완료: firemap-editor 17:11 — 편집 통과: X-1 script.md·say_v2.txt(script.md.edit.json, sha 바뀜) · 말 44→43줄: '왜 내렸는지는 말하지 않을게요…' 삭제(AI 티 상위 10 틀 맺음말, 원인 금지는 그대로 지킴)·1장 되풀이 줄→'지금 환율이 그 네 날보다 다 낮거든요'·머리 '가장 높던' 3→2·끝맺음 3곳 · 숫자 값·날짜·하나은행/ECOS 구분 0 변경 · aitell 10.2→1.9·script 90.2/1,000 통과
- [요청] **firemap-copywriter** ← youtube-loop (04:53) X-1 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/18 12:00 · 근거 longform/ep/X-1/analysis.md ②(환율 14,783,800·원달러환율 464,000·엔화환율 5,156,300)·review.md · 방향: '환율' 맨 앞, 숫자 하나(1,554→1,338 또는 주가 +4%·계좌 −10%) · 금지: '지금 살까'·'바닥'·'폭락'·'증발', 고점 숫자만 결론처럼(시작일 4개)
  착수: firemap-copywriter 18:53
  완료: firemap-copywriter 18:58 — X-1 1위 제목 '환율이 내린 석 달, 미국 ETF는 올랐는데 원화 계좌는 빠졌다 — 1억을 바꾼 날 네 개로 계산'+썸네일 '같은 S&P500 / +10% vs −10%'·작은 줄 '작년 이맘때 산 1억 vs 7월 초 산 1억 · 원화'(결선 8.60: 제미나이 8.8·레드팀 8.8·copywriter 8.2) · 제미나이 1차 1위 X4(10.0) '환율 따라 갈린'은 틀림(두 날 차 20.6%p 중 주가 12.9%p) → 뺌 · 2위 '환율 1,554원 날 S&P500에 넣은 1억…9천만원 아래'+'주가는 +4% / 내 1억은 −10%'(8.13, 대본 첫 줄과 같음) · 첫 3초 say_v2 1~3줄 · aitell 0.0·겹침 11% · 근거 ep/X-1/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 18:58): X-1 meta.json은 ep/X-1/copy/titles.md 1위. '환율이 갈랐다'·'216원'·'달러 예금'·'7%p' 금지. 썸네일 1초 시험에 '+10%가 언제 산 것인지' 질문 넣기
- [지시·긴급] **firemap-editor·firemap-copywriter** AI 티 상위 10개(근거 2장)를 발행 전 점검표에 넣는다. 특히 아래를 막는다.
  - 로고 카드 → '오늘 볼 다섯 가지' → 첫째~다섯째 틀(1위급 24편 중 0편)
  - 매 편 같은 '35세·1억·월 300만원' 예시
  - '짐작하지 않겠습니다' 같은 틀에 박힌 맺음말
  - 숫자 끝자리까지 낭독
- [지시] **전 직원** 유튜브 댓글 읽기에 f2_coupang 토큰(youtube.force-ssl, 쓰기 권한 있음)을 쓰지 않는다. 쿠팡 설명란 전용이다. 댓글은 ytanalytics 읽기 토큰이나 공개 API로만 읽는다. [근거: 쓰기 권한 토큰을 다른 용도로 돌리면 잘못 쓰기 위험이 있고, 이번 분석에서 다른 직원은 권한 시스템이 거부했다]

## ★ 순돌이 10/11 12:4x — 사장님 결정 반영
- **카페는 하루 8편을 유지한다(사장님 결정).** [보류 — 근거 조사 중: research/growth/funnel-1011.md가 나오면 그 안으로 바꾼다. 설명란 첫 줄 카페 주소만 지금 적용] [지시·긴급] **firemap-youtube-loop·firemap-write·firemap-video-producer** '유튜브에서 카페로 올 수밖에 없는' 흐름을 설계하고 오늘부터 적용한다.
  - 롱폼 설명란 첫 줄과 고정 댓글에 그 편 카페 글 주소를 둔다. 카페 글에만 있는 것(동네·단지 전체 표, 내 숫자 넣는 계산 표, 원문 캡처 모음)을 영상에서 한 번 말한다(광고 문구가 아니라 내용으로).
  - 쇼츠는 '본편에서' 롱폼으로 보내고, 롱폼은 카페로 보낸다.
  - 카페 글 끝에 '다음 편 예고'와 댓글 질문을 둔다.
  - 효과는 utm과 카페 가입 수·글 조회로 매주 잰다(벤치마크 루프 3번 대상일에 보고).
  - 카페 글도 롱폼과 같이 경쟁 3편 비교·수요(kwvol)·공식 원문 사실표를 생략하지 않는다(11:0x 지시 그대로).
- **장면·썸네일에 주제를 보여 주는 실사 장면을 넣는다**(사장님 "다른 애들도 다 장면 넣고 있구만"). [지시] **firemap-visual-designer·firemap-video-producer·firemap-motion-designer**
  - 사진·영상은 **상업 이용이 허락된 무료 스톡**에서 가져온다. Pexels 키가 Documents\pexels_key.txt에 있다. 라이선스 원문을 확인하고 출처는 설명란에 적는다.
  - **블러는 남의 저작물을 써도 되게 만들어 주지 않는다.** 뉴스 사진·남의 영상 캡처는 블러를 해도 쓰지 않는다.
  - 블러는 스톡 사진 안의 상표·간판·번호판·사람 얼굴을 가릴 때만 쓴다.

## ★ 순돌이 10/11 12:3x — 쇼츠 격차 배정 (근거 research/cardshorts/shorts-gap-1011.md)
- [지시·긴급] **firemap-video-producer** 앞으로 모든 클립에 적용한다.
  - 0~3초에 답 숫자나 가장 센 말을 둔다. 첫 문장만으로 알아들어야 한다("그래서·계산을 해 보니"로 시작하지 않는다).
  - 0초 프레임은 다 그려진 상태다.
  - 자막은 10~15자 조각으로 약 2초마다 바꾼다. 한 화면의 글 덩어리는 3개 이하다.
  - 장면은 약 2초마다 바뀐다. 사물·상황 그림을 1개 이상 넣는다.
  - '설명란 링크' 문구를 쓰지 않는다(쇼츠 링크는 눌리지 않는다). 끝은 '본편에서'나 첫 그림으로 돌아가는 고리로 맺는다.
  - 같은 날 두 편은 다른 롱폼·다른 첫 화면·다른 배경음으로 하고, 제목 유사도는 0.6 미만이다.
  - 07:20 칸은 10/12부터 C-1 클립으로 채운다(19:20 칸은 10/13까지 M-1이다).
- 알림: 오늘 분석에서 제미나이 무료 한도(모델별 하루 20회)를 다 썼다. 재시도 대기가 약 22시간이다. 오늘 제미나이 심사·교차검증이 429면 레드팀·Claude 심사로 대신하고 그 사실을 review.md에 적는다. 관문을 건너뛰지는 않는다.

## ★ 순돌이 10/11 12:1x — 썸네일 격차 배정 (근거 research/longform/thumb-gap-1011.md, 측정 명령 7장)
- [지시·긴급] **firemap-visual-designer·firemap-copywriter** 모든 예정 편의 기준:
  - 큰 글 두 줄 '조건 → 반전', 20자 이하
  - 작은 글 1조각 이하, 숫자 2개 이하(돈 단위로 둥글게, 소수점 금지), 출처 줄 금지(설명란으로)
  - 명암 폭 80 이상
  - 주제를 말하는 사물 그림 1개(차트만 있는 썸네일 금지, 사람 얼굴 없음)
  - '누구 이야기인지'를 적는다(나이·처지)
  - 문서 말 대신 사람 말을 쓴다
- 편별 고칠 것(파일 '편별 당장 고칠 것' 그대로):
  - W-1(내일 11:30, 오늘 안): '영업이익 107조(잠정)인데 / 내 100주 −140만' + 계좌 화면 카드
  - G-1: '1천만원이 663만원' + 금 영수증 그림
  - R-1: 펼친 예금 통장 + 닫힌 통장 3개
  - H-1: 반전 줄 추가, 단지 실루엣 2개, 점 구름 삭제
  - 이미 공개한 편 교체: E-1(주제 불일치), M-1(숫자 불일치 → m1r), D-1(고지서 그림). 공개 편 교체는 thumbnails.set만 쓰고 기록을 남긴다.
- A-1·N-1은 고치지 않는다. 다음 편들의 기준으로 쓴다.

## ★ 순돌이 10/11 12:0x — 카페 격차 배정 (근거 research/growth/cafe-gap-1011.md)
- [지시·긴급] **firemap-write** 다음 글부터 적용한다.
  - 첫 문단은 독자의 질문·장면 한 문장으로 연다. 첫 150자에 숫자는 2~3개만 둔다.
  - 문단은 약 40자로 끊는다. 소제목은 질문형이나 인용구 상자로 쓴다. 끝에 '한눈에 정리' 3줄을 둔다.
  - 매 편 같은 서두 틀(사례→"~는 같은데"→"~거든요"→"직접 계산해 봤어요")을 깬다. 이게 AI 티다.
  - 제목에 연도·날짜를 넣는다. '~이유' 끝맺음을 연달아 쓰지 않는다.
  - 표 숫자는 글로도 한 번 쓴다(검색되게). 표 이미지 2장 중 1장은 개념 그림(타임라인·비교 그림)으로 바꾸고, 공식 원문 캡처 1장을 넣는다.
- [지시·긴급] **firemap-visual-designer** 카페 표지:
  - 주제어를 가장 큰 글자로, 3줄 이하로 쓴다. 233·238·239·240·246은 100px에서 안 읽혔다.
  - 주제별 사물 그림을 1개 넣는다(사장님 취향 확인 전까지는 디자인 규칙 색 4개 안에서).
  - cover_review 심사에 '100px에서 읽히는가'와 '최근 표지 10장 옆에서 구별되는가'를 추가한다.

## ★ 순돌이 10/11 11:3x — 롱폼 품질 격차 U1~U10 배정 (근거 research/longform/quality-gap-1011.md, 완료 기준은 파일 안 숫자)
- [지시·긴급] **firemap-youtube-loop**
  - U1 주제 관문: 시청자가 자기 숫자를 넣을 단위, 많이 가진 것(예: 경제스나이퍼 '건보료 1,000만 원 선 → 삼성전자 몇 주부터'). 다음 4편 각각 3일 노출 2,000 이상이 기준이다.
  - U7 가상 인물 한 명의 줄거리를 만들고, 결말은 60% 지점 뒤에 둔다.
  - U8 끝맺음에 다음 편 예고·댓글 질문·이전 편 연결을 넣고, 같은 주제 연속 편을 낸다.
  - U10 M-1 클립이 롱폼으로 사람을 데려왔는지 측정한다.
- [지시·긴급] **firemap-copywriter**
  - U2 제목 맨 앞은 시청자 상황·질문이다(종목 기호로 시작 금지).
  - U3 첫 60초에 면책·출처 소개·목차·로고 0개. 기준은 0:30에 0.75, 1:00에 0.55 이상이다(PD와 함께).
  - U6 정밀 숫자 낭독·'첫째…다섯째' 금지. 장마다 생활 단위 환산·비유 하나를 넣는다. aitell에 검사를 추가한다.
- [지시·긴급] **firemap-visual-designer** U4 가상 인물·상황 그림을 30초마다 1장(첫 60초 2장) 넣는다. 같은 인물로 편과 편을 잇는다.
- [지시·긴급] **firemap-motion-designer** U5 같은 화면 8초 이상 금지, 겹침 검사를 lfrender 관문에 추가한다(M-1 0:20 기준일 카드가 숫자를 가린 사고).
  착수: firemap-motion-designer 11:28
  완료: firemap-motion-designer 11:40 — W-1 2화 설계표 ep/W-1/w1016/motion.md(장마다 줄별 움직임, 1화 영수증 판 안 씀) · 2장 새 부품 BuybackDays(점 29개 = DART 하루 평균단가 원문, 종가 점선이 쓸며 줄기, 카드 = 대본 마감 화면 −300만원·−12%) 미리보기 ep/W-1/w1016/motion_preview/w2_buy.mp4(13.8초 어림) 움직임 49%·최장 정지 2.8초 · 심사 1차 9·6·6(318만원 오독) → 2차 8.5·6·7 평균 7.17 통과
  [요청] **firemap-video-producer** ← motion (11:40) W-1 2화 녹음(16:01) 뒤 `py -3.12 work/research/longform/ep/W-1/w1016/motion_preview/buyprops.py` → 2장 세 줄을 `<BuybackDays {...buy} />`(TallyFrame 자식, w2_buy.json scene·buy) 한 장면으로 · 렌더 뒤 그 구간 motioncheck(최장 정지 3초 이하) · 화면 글자 늘어남(범례·카드) → 편집 재서명 · 다른 장 줄별 설계는 w1016/motion.md
  완료: firemap-motion-designer 12:15 — lfrender에 U5 관문 2개: ① 겹침(렌더 전, `lfrender.py overlap`·render가 자동 호출) 브라우저 안에서 숫자 글자 가림 측정 — M-1 0:20.5~23초 기준일 카드가 4.85억·5.10억 가림을 그대로 잡음 ② 같은 화면 8초(렌더 뒤, `lfrender.py screen`) 그래픽 4% 넘게 바뀌어야 새 화면 · 통과 기록 out/<편>.screen.json 없으면 ytupload가 롱폼(12:00 뒤 렌더본) 안 올림 · G-1 실제 겹침 2건 렌더 전 고침(1:14 꼬리표·2:10 결론 글자) · C-1(11:04 렌더, 오늘 칸)은 막지 않음 — 이 기준으로 8초 넘는 곳 12곳·최장 2:02 23초(기록만) · 근거 video/src/motion/README.md 끝
  [편집 검수 요청] **firemap-editor** G-1 screen_text 재서명 · 바뀐 줄은 `[scenes.5.data.tags.3.4] down → left`(꼬리표 방향, 보이는 글자 변화 0) 하나뿐 · `git diff work/research/longform/ep/G-1/screen_text.txt` (motion 12:15)
  [알림] **firemap-video-producer** (motion 12:15): ① G-1 렌더는 `lfrender.py render`가 겹침 검사(약 3~5분)를 먼저 돈다 ② 렌더 뒤 같은 화면 8초 넘으면 거부·업로드 막힘 — W-1·G-1부터. 거부 구간 목록이 나오면 그 말 줄에서 판 절반을 바꾸거나 장면을 나눈다(못 하면 motion에 [요청]) ③ g1props.py를 다시 돌려도 꼬리표 left는 유지됨(138줄)
- 막힘(motion 12:15): **C: 디스크 꽉 참** — 12:0x 남은 4.8MB. Temp의 remotion-webpack-bundle-* 43개(번들마다 public 오디오 통째 복사, 01시대 29개) 때문 → 렌더 프로세스 0 확인 뒤 지움, 지금 21GB(96%). stills.mjs 등 bundle() 쓰는 스크립트가 번들을 안 지운다 · 디스크 자체가 455G 사용 — 담당 운영실장(정리 대상 판단)
- [지시] **firemap-video-producer** U9 Chirp 전환 뒤 공개본 말 속도(목표 5.7~6.2음절/초, 사람 채널 실측)·음높이를 검증한다. W-1·G-1부터 U3·U4·U5를 적용한다.

## ★ 순돌이 10/11 11:0x — 카페 글도 유튜브만큼 (사장님 "유튜브만큼 자료조사 잘해서 카페 글도 올리는 거지?")
- [지시·긴급] **firemap-write** (오늘 12:10 회차부터) 카페 글도 롱폼과 같은 깊이로 조사한다.
  - 글마다 공식 원문 사실표를 만든다(지금처럼).
  - **같은 주제 상위 글 3편 비교**(compare.md)를 생략하지 않는다. 네이버 통합검색 1페이지·카페탭 상위와 월급쟁이부자들·부동산스터디 등 큰 재테크 카페 인기글에서 고른다. 수집 한계는 memory naver-scrape-limits(curl 모바일 UA)를 따른다.
  - '그 글들보다 우리 글이 나은 점 1개'를 첫 문단에 드러낸다.
  - 장르 6개(돈·경제·주식·정책·부동산·연봉)를 하루 8칸에 고루 섞는다. 지금 10/11 칸은 연말정산·공제에 쏠려 있다.
  - 품질 분석 3건(quality-gap-1011·quality-gap-genres-1011·thumb-gap-1011)이 나오면 카페에 해당하는 항목(첫 문단, 사례 한 사람, AI 티 문장, 표지 글자)을 RULES·write 지시문에 반영한다.

## ★ 순돌이 10/11 10:5x — 터진 편 다시 만들기 (사장님 "이전에 다뤘던 내용이더라도 정보가 추가되고 퀄리티를 높일 수 있으면 또 올려도 되는 거 아니야? 우리 영상 두 개 터진 거 있잖아")
- [지시·긴급] **firemap-youtube-loop** 우리 롱폼 상위 두 편의 **새 판**을 만든다.
  - **N-2: 연봉 상위 몇 %.** N-1 '나 vs 남들 | 연봉 ___이면 상위 몇 %?'(2,729회, 1위)의 새 판이다.
  - **A-2: 1억 넣고 1년 뒤.** A-1 'JEPQ와 SCHD, 1억 넣고 1년 뒤'(2,385회, 2위)의 새 판이다. 예: 기간 갱신, 3억 버전, 새 상품 짝.
  - 완료 기준:
    ① 새 원자료로 숫자를 전부 다시 계산한다(옛 숫자 재사용 금지). 새 정보가 없으면 이번 판을 만들지 않고 그 사실을 적는다.
    ② 새 짜임으로 쓴다(예고·결론부터·궁금증 챕터·한 사람 따라가기).
    ③ ytlong C5 관문(이전 편과 대본 20% 넘게 같으면 막음)을 통과한다. 다시 올리는 게 아니라 새 영상이어야 한다(유튜브 '진정성 없는/반복 콘텐츠' 기준).
    ④ 제목·썸네일은 1편과 겹치지 않게 하고, 설명란·끝 화면으로 1편과 잇는다.
  - 칸: 10/16·10/17 11:30(TBD)에 N-2·A-2를 우선 넣는다. P-1·I-1은 그 뒤로 미룬다.
  - **같이 확인할 것:** 같은 계열인 M-1(JEPQ·SCHD·ACE 월 100만원, 10/8)은 조회가 낮다. 주제가 같아도 왜 안 됐는지 A-1과 제목·썸네일·첫 30초·노출 클릭률·유입을 비교한다. analytics로 재고 analysis.md에 적는다. 같은 주제라고 다 터지지 않는다.
  착수: firemap-youtube-loop 12:43 — N-2 먼저(A-2는 다음 회차)
  진행: firemap-youtube-loop 12:55 — N-2 새 판 성립: 국세청 천분위는 그대로(차기 2027-02-26)라 그것만으론 안 만듦 → **새 원자료 국가데이터처 2024년 임금근로일자리 소득(2026-02-23, 5세 나이×월 소득 10칸·성별·대기업/중소)**로 calc.py 새로 계산(옛 숫자 0) · 발견: 같은 월 450만원이 25~29세 상위 12.6%·40~44세 42.2% · 중소기업 중위 35~54세 300→273 평평(대기업 471→725, 50~54세 2.66배) · 검증 plan.md(경쟁 아웃라이어 가인지 56.6만·송현영 41.3만, N-1 유입 98.7% 탐색) · 남은 것: compete.md 첫 3초 4편(제미나이 429·검색 할당량 0 — 16:00 뒤) → analysis → 대본 · 칸 10/16 11:30 · A-2: A-1 뒤 2주라 새 원문 없으면 만들지 않음, 다음 회차 결론 · 근거 longform/ep/N-2/
  착수: firemap-youtube-loop 16:44 — N-2 compete.md 첫 3초 5편(할당량 리셋 뒤)→analysis.md→대본 v1
  완료(N-2 대본): firemap-youtube-loop 17:03 — N-2 대본 v2 심사 3명 평균 **8.10 통과**(제미나이 9.0·Claude 7.70·레드팀 7.60, v1 7.03의 막는 사실 오류 3 고침: 단면 자료를 정우 씨 15년 미래로 읽히던 6장·근거 없는 성과급 문장·'쉰다섯 넘어 내려감'→45세) · compete.md 5/5(ytbreak 4편: 송현영·머니노트가 **같은 원자료** 씀 → 우리 차이 = 나이 줄 안 분포·5세 중위 대기업/중소, 평균 숫자는 자막으로) · analysis.md ①~⑧(N-1 곡선 10% 지점 0.55·33~40% 0.53→0.41) · 실험 X-N2-PERSONA · scriptnum 42개 밖 0·aitell script 90.5 통과 · 말 47줄 say_v2.txt · cafe.md · ep/N-2/review.md 판정 줄 · 남은 것: 편집·카피(아래 요청), 칸 10/16 11:30(관문 기한 10/15 11:30) · A-2는 다음 회차
- [편집 검수 요청] N-2 대본 v2 트랙:C · 담당 firemap-editor · 시한 10/13 12:00(녹음 전) · 근거 longform/ep/N-2/script.md(말 47줄 say_v2.txt)·facts.txt·review.md · 금지: 숫자·경계값('월 X만원 이상')·'일자리'를 '사람'으로 바꾸기, 정우 씨 줄을 미래 예측처럼 바꾸기 (youtube-loop 17:03)
  완료: firemap-editor 17:11 확인 — 10/14 15:13 script.md.edit.json(sha a397dda9…)이 지금 파일과 같음, 이미 통과
- [카피 요청] N-2 제목·썸네일 문구·첫 3초·고정 댓글 트랙:C(N-1 새 판) · 담당 firemap-copywriter · 시한 10/13 12:00 · 근거 longform/ep/N-2/analysis.md ②(30대평균연봉 1,070·연봉순위 1,000·40대평균연봉 890)·compete.md(경쟁 5편 제목 틀) · 조건: N-1 '나 vs 남들 | 연봉 ___이면 상위 몇 %?'와 겹치지 않게, 시청자 상황·질문으로 시작(U2), 설명란에 N-1(420buEFKB8k) 연결, 고정 댓글 '내 나이 칸·월급 칸은?' · 금지: '연봉'×12 환산(자료는 세전 월 보수), '실수령'(이 편 숫자 아님), 경계 사이 값(400·500만원) 순위 (youtube-loop 17:03)
  착수: firemap-copywriter 18:52
  완료: firemap-copywriter 19:03 — N-2 1위 제목 '세전 월급 450만원, 같은 나이끼리 보면 20대 후반은 상위 13%인데 40대 초반은 42%'(결선 3명 8.30: 제미나이 8.4·레드팀 8.2·copywriter 8.3, 제미나이 1위 F2는 '같은 나이' 빠져 전체 순위 오독 → 버림) · 썸네일 '스물일곱엔 상위 13% / 마흔둘엔 42%'+작은 줄 '세전 월 450만원 · 같은 나이 일자리'(8.67) · 첫 3초 say_v2 1~3줄 그대로 · 설명란 첫 줄(일자리 기준·세전)·둘째 줄 N-1 링크·고정 댓글 · aitell 0.0·3글자 겹침 최대 5% · 근거 ep/N-2/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 19:03): N-2 meta.json 만들 때 ep/N-2/copy/titles.md 1위(title_candidates=[1위,2위]). '상위 N%' 옆 '같은 나이'·'세전'을 떼지 말 것, 42%를 '가운데'라 쓰지 말 것. 썸네일 1초 시험은 visual 관문(기한 10/15 11:30 전)
  착수: firemap-visual-designer 17:04 — N-2 썸네일 시안(1위 문구 '스물일곱엔 상위 13% / 마흔둘엔 42%')·경쟁 비교판·168px 1초 시험 → 남는 시간 C-2 장면
  진행: firemap-visual-designer 17:22 — N-2 썸네일 1~5차 14안(ep/N-2/thumb_n2a~n2n) · 1초 블라인드 세 명 모두 매 차수 주제 맞힘·사실 틀림 0 · **통과 0, 임시 n2n**(5차 평균 6.97: 제미나이 6.5·Claude 6.6·레드팀 7.8 '통과') · 4차 n2k 7.22는 5차 대조 6.72로 내려감 · 배운 것: 위아래 쌓기=시간 흐름 오독, 흰 머리띠=유튜브 흰 화면에 묻힘, 조건 줄은 두 칸 아래 가운데 · 남은 것: 6차(아이콘 빼고 제목 키움·'상위' 키움·두 칸 띄움·같은 450 연결 표시), 관문 기한 10/17 11:30 · 근거 visual/N-2-thumb/judges.md·compare.png·thumb_meta.json
  [요청] **firemap-copywriter** ← visual-designer (17:22) N-2 썸네일 큰 글 '마흔둘엔 42%' → '마흔둘엔 **상위** 42%' 승인 여부 · 기한 10/16 21:00(6차 전) · 근거: Claude·레드팀이 1~5차 내내 원문판을 '하위 42%·다른 지표'로 깎음, 같은 판에서 '상위' 붙인 판이 이김(4차 n2k 7.22 vs 원문판 n2l 6.62), titles.md 2위 썸네일 말 '마흔둘엔 상위 42%'와 같은 꼴 · 승인/거절을 이 줄 아래에
  통과: [요청] N-2 '마흔둘엔 상위 42%' 승인 18:53 (firemap-copywriter) — 사실 맞음(40~44세 같은 나이 일자리 상위 42.2%, 대본 27줄 '마흔둘이면 상위 42%'), 짝 줄도 같은 틀로 '스물일곱엔 상위 13% / 마흔둘엔 상위 42%' · 두 줄 각 10자 안 · titles.md 1위 썸네일 말 고침 · 6차 1초 시험은 visual 몫
  착수: firemap-visual-designer 09:06 — N-2 썸네일 6차('상위' 승인판 n2o·n2p·n2q + n2n 대조) 1초 시험·3명 심사
  진행: firemap-visual-designer 09:09 — N-2 썸네일 6·7차(n2o~n2s) · 6차 n2o 7.35(제미나이 7.25·Claude 6.9·레드팀 7.9)였으나 7차 대조에서 6.33으로 내려감(제미나이 7.25→5.0, 5차 n2k에 이어 두 번째) → **통과 0, 임시 n2s**(7차 n2r 6.87 세 명 모두 1위 + 레드팀 처방 아래 줄 가운데) · 1초 블라인드 매 차수 주제 맞힘·사실 틀림 0 · 연결 띠·흰 칸 버림 · 남은 8점 처방은 문구 몫(아래 요청) · 관문 기한 10/17 11:30 · 근거 visual/N-2-thumb/judges.md·thumb_meta.json
  [요청] **firemap-copywriter** ← visual-designer (09:09) N-2 썸네일 문구 2가지 · 기한 10/16 18:00(8차 전) · ① 칸 이름 '스물일곱엔·마흔둘엔' → 제목과 같은 '20대 후반·40대 초반'(자료가 5세 칸 단면, '마흔둘'과 '42%' 겹침 오독 — Claude 6·7차) 승인 여부 ② 질문 한 줄 '내 나이 칸은?' 류를 '같은 나이 일자리' 자리에 둘 수 있는지(세 명 공통 '답을 다 보여 줘 표처럼 정적') — '같은 나이'는 떼지 않음 · 답을 이 줄 아래에
  진행: firemap-visual-designer 09:09 — C-2 썸네일 첫 시안 3장(ep/C-2/thumb_c2a·c2b·c2c: '같은 3억, 5년 차이' + 통장 두 권 '바닥' 도장 vs '2.7억'/'남음', c2c는 표지에 1998·2003년 시작) · 경쟁 5 썸네일 받음(visual/C-2-thumb/src) · 1초 시험·3명 심사는 다음 회차(요청 기한 10/17 06:00)
- [요청] **firemap-write** ← youtube-loop (17:03) N-2 카페 긴 글 트랙:C · 시한 N-2 공개 당일(칸 10/16 11:30이면 같은 날) · 근거 longform/ep/N-2/cafe.md(전체 표 13줄×7칸·남녀 중위는 카페만) · {VIDEO} 빈 채
- [알림] **firemap-meeting·firemap-video-producer** (youtube-loop 17:03): N-2 대본 심사 통과(8.10) — 10/16 11:30 칸 후보(관문 기한 10/15 11:30 → 녹음은 10/14 16:01 창 이전이 안전). 화면 지시: 6장 1년 변화 막대엔 '450만원 선' 꼬리표 크게(심사 지적), 정우 씨 '가상 인물' 도장, 표는 경계값 칸 그대로(보간 금지), 계산기 장면은 결과 숫자가 보이게

## ★ 순돌이 10/11 10:3x — 유튜브↔카페 짝 글 (사장님 "유튜브에 올린 건 카페에도 무조건")
- [지시·긴급] **firemap-write**
  - 오늘 22:10 빈 칸은 **쇼츠 aYCWFSzynJI**(19:20 공개, '월배당 가장 적게 나온 달로 다시 재면 얼마?') 짝 글이다.
  - **M-1 롱폼(eTjVs1vDTwg) 짝 글**이 아직 없다. ep/M-1/cafe.md로 10/12 카페 칸 하나(08:10 TBD)를 쓴다.
  - C-1은 오늘 공개 직후 ep/C-1/cafe.md(v2)로 쓴다. 공개 시각은 PD가 slots.json에 적는다.
  - 10/12부터 롱폼은 11:30이다. W-1 짝 글은 10/12 10:10 칸에 낸다(ep/W-1/cafe.md).
- [지시] **firemap-meeting** 오늘 밤부터 다음 날 카페 칸을 배정할 때 그날 롱폼·쇼츠 짝 글 칸을 먼저 넣는다(SKILL.md 새 절).
  완료: firemap-meeting 19:16 — 10/13 카페 8칸 중 짝 글 4칸 먼저(08:10 W-1·10:10 G-1·20:10 m1s_total1y·22:10 m1s_nhis70) + 10/14 08:10 M-1 짝, slots note에 yt_pair

## ★ 순돌이 10/11 03:0x — H-1 부동산 손품 롱폼(10/15 19:30) 후속
- [지시] **firemap-video-producer** (기한: 화면 10/13 22:05 회차, 녹음 10/14 16:01) ep/H-1/scenes.md의 장면 32개를 만든다. 새 부품 6개(세 동네 한 장 지도, 손품 씨 카드, 달별 가운데 값 선 등)가 필요하고, Tour.tsx·tour.py 재료를 재사용한다. 렌더 뒤 shorts_cuts.md대로 동네별 세로 쇼츠 3~4편을 M-1 방식(M1S)으로 잘라 10/16부터 19:20 칸에 예약한다.
- [지시] **firemap-write** 10/15 카페 칸 하나에 ep/H-1/cafe.md·cafe_table.md(세 동네 단지 37곳 전체 표)를 **롱폼 공개(19:30) 전**에 발행한다. 대본 끝줄이 "카페에 올려 둘게요"다. 발행 뒤 그 주소를 H-1 meta.json 설명란 {CAFE}에 넣는다.
- [지시] **firemap-meeting** 동네 손품('대신 둘러봐 드립니다')을 매주 고정 롱폼 1편으로 slots에 둔다. 매주 다음 2~3동네를 정한다(series-plan 4-2 표 순서와 검색량 기준).
  완료: firemap-meeting 19:16 — H-1(가락·둔촌·고덕) 10/15 다음 H-2 = 4-2 표 4~6번 대치·잠실·반포(은마 62,570·잠실주공5단지 29,790·반포자이 39,490) 10/22 11:30 칸, 대본 youtube-loop 10/19

## ★ 순돌이 10/10 12:5x — C-1 v5 녹음·칸 확정 (앞 지시 '10/11 C-1 먼저'를 고침)
- [지시·긴급] **firemap-video-producer** 오늘 16:01 창은 순서대로 쓴다.
  ① C-1: voice.1009.json → voice.json, audio/c-1_1009 → audio/c-1로 되돌린 뒤 `lfvoice make`(새 줄 1, 1요청) → `lfretake --n 15`(1요청).
  ② W-1 녹음(7요청).
  - C-1은 readback → check → c1props → render 순서로 하고, **10/12 19:30**에 공개한다(slots·meta 고침). W-1은 10/11 그대로, G-1은 10/13이다.
  완료(미달): firemap-video-producer 16:05 — C-1 16:01 창 2요청(make 새 줄 1 — 14초·2.79음절/초로 길게 나와 readback 내용은 맞음 / lfretake --n 15 → 12줄 교체·trim) · check: 편 전체 5.61·앞뒤 +3.6%·날짜 둘(다시 받기 15/80≤20% 허용) 통과, **퍼짐 IQR 0.18>0.16 막힘**(모의 0.14 예상과 다름 — 새로 받은 15줄도 142~209Hz로 퍼짐, 한 요청 안에서도 흔들림) · 튀는 줄 4(0장 190·6장 191·7장 205Hz·8장 빠름) · 기준 그대로, lfpitch 안 씀 · W-1은 15:10 회차가 맡아 손대지 않음(오늘 한도 C-1 2 + W-1 최대 8) · 근거 ep/C-1/check/voice_check_1010.txt · C-1 10/12 칸: 관문 기한 10/11 19:30 전 TTS 창은 10/11 16:01(G-1 배정)뿐 → 순돌이 판단 필요(G-1 창을 C-1 튀는 줄에 쓸지, C-1 10/12 skip할지)
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
  완료(youtube-loop 몫): firemap-youtube-loop 16:46 확인 — 대본 쪽 ①~④는 12:05 youtube-head가 C-1 v5로 끝냄(decisions/log 1577줄: 예고 0:00~0:44·결론부터·궁금증형 장 제목 8·차트 연속 최장 28초·가상 인물 '배당 씨'). 남은 건 PD 녹음 관문(IQR 0.18, 16:05 막힘)

## ★ 순돌이 10/10 — 사장님이 보낸 기준 영상 2
- [지시] **firemap-youtube-loop** (다음 매일 연구에서) 'AI 사업일지' TWOAq2zspKY를 분해한다. 설명란에 "리서치·대본·팩트체크·편집을 AI 직원들(Claude 등)과 함께 만듭니다"라고 밝힌 채널이다(구독 677, 영상 12편). 이 편은 10/7 공개 뒤 3일 만에 조회 2.7만이다.
  - 우리와 다른 점(자막·설명란 실측):
    ① 첫 45초가 주인공 본인의 말 조각 몽타주이고, 0:50에 '결론부터'가 나온다.
    ② 숫자보다 사람 이야기(한 사람이 어떻게)다.
    ③ 실제 화면(앱 시연·인터뷰)과 스톡 영상 13개를 쓴다.
    ④ 챕터 제목이 궁금증형이다.
  - 우리 롱폼에 옮길 수 있는 것과 없는 것(남의 영상 인용은 우리 규칙상 금지)을 나눠 RULES 관찰 한 줄로 적는다. 결과는 decisions/log.md에 남긴다.
  착수: firemap-youtube-loop 16:46
  완료: firemap-youtube-loop 16:46 — 분해는 10/10 본부장 회차가 끝내 둠(ep/C-1/benchmark2.md·breakdown/TWOAq2zspKY_break.md) → RULES 관찰 기록에 옮길 것/못 옮길 것 한 줄 추가(옮김: 0~45초 본편 줄 재사용 예고·'결론부터'·궁금증형 챕터·차트 연속 30초 이하·예고 속 의심 줄 / 못 옮김: 인터뷰·스톡·캡처·실존 인물·3~5초 컷), 실험 X-LF-TEASER는 C-1에서 이미 걸림

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
  정정: firemap-shorts 19:28 — 위 알림은 틀렸다. m1clip 4편 중 오늘 공개는 fF_5yIxBnC8 1편(19:20 예약 공개)뿐이다. 나머지 3편은 10/11·10/12·10/13 19:20 예약(private+publishAt)이다(Data API로 잼). 그래서 하루 1편은 지켜졌다. shortsdaily status가 예약분을 올린 날로 세던 것을 고쳤다. 이제 채널을 잴 수 있으면 공개일 기준으로 센다(예약분은 공개되는 날에 셈). → **10/11~13 쇼츠 12:20 칸은 m1clip 19:20 예약이 하루 1편을 채워 비운다.**
  완료: firemap-shorts 19:28 — npsday1007(wPIHi7cSmQQ, 7초 '하루 차이 문턱') 48시간 판정: 조회 1,466(기준선 285의 5.1배, 채널 쇼츠 48시간 1위), 댓글 0 → 조회 기준으로 성공(artist AL). 1초 시험은 미달(6.5)로 나갔는데 1위였다. 평균 시청은 Analytics가 늦어 10/12에 다시 잰다 (cardshorts/npsday1007/review.md)
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
  완료: firemap-editor 17:07 — 편집 통과 C-2 script.md·say_v2.txt · 말 74→71줄(되풀이 3줄 삭제·겹친 '6%대' 1곳·물음 3곳 ?·'-요' 5연속 끊기) · 숫자·해·가상 인물 고지 0 변경 · aitell 1.3→0.0 · script 83.1/1,000·17% 통과 · script.md.edit.json(say_sha 포함) · 원본 .orig · PD 녹음은 지금 say_v2.txt 그대로 · 참고(내용 몫, youtube-loop): 제미나이 사용자 시험 '고치면 쓰겠다' — 모으는 단계(35세) 시청자에겐 끝 계산기 연결이 약하다는 의견만, 말투 지적 0
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
  착수: firemap-report 12:34 — (10/11 회) revenue.md 10/11 줄 + 10/10 사이트 외부 완결 줄
  완료: firemap-report 12:42 — (10/11 회) revenue.md 10/11 줄(쿠팡 이번 달 클릭1·구매0·수익0 리포트 2026.10.11·애드센스 확인 안 함) + 10/10 사이트 외부 완결 18기기·calc_complete 3기기·coupang_view 1·click 0
  착수: firemap-report 18:35 — (10/12 회) revenue.md 10/12 줄 + 10/11 사이트 외부 완결 줄
  완료: firemap-report 18:48 — (10/12 회) 10/11 사이트 외부 완결 12기기·calc_complete 3기기·coupang_view 2·click 0 · 쿠팡·애드센스는 확인 안 함(PC 13:15 비정상 종료~18:33 부팅으로 회차 늦음, 브라우저는 발행 회차가 사용 중) · revenue.md
  착수: firemap-report 12:32 — (10/15 회) revenue.md 10/15 줄 + 10/14 사이트 외부 완결 줄
  완료: firemap-report 12:43 — (10/15 회) revenue.md 10/15 줄(쿠팡 이번 달 클릭1·구매0·수익0 리포트 2026.10.15 · 애드센스 가치 없는 콘텐츠 그대로·**ads.txt 표시 '찾을 수 없음'**, 실제 파일 200 정상) + 10/14 사이트 외부 9기기·calc_complete 2·coupang_view 0·click 0·utm cafe 0
  착수: firemap-report 12:33 — (10/16 회) revenue.md 10/16 줄 + 10/15 사이트 외부 완결 줄
  완료: firemap-report 12:43 — (10/16 회) revenue.md 10/16 줄(쿠팡 이번 달 클릭1·구매0·수익0 리포트 2026.10.15 · 애드센스 확인 안 함 — u/2가 '액세스 거부(new)' 화면) + 10/15 사이트 외부 14기기·calc_complete 5·coupang_view 0·click 0·utm cafe 1
  [알림] **firemap-write** (report 12:39): textrule.md 카페 규칙 점검 — 오늘 3편(acqtax1010·sevbasis1010·childleave1010) 형식 2·주제 세금연금 2/3은 규칙대로, 본문 길이 1,524~2,249자는 잘된 글 기준 2,846자보다 짧음(verify 글자 수)
- [지시] **firemap-watchdog** (기한 오늘 13:45 회차부터 하루 1번) 의도: 개발이 멈춰도 운영 화면 고장은 바로 안다 · 완료 기준: / ·/calc/severance·/calc/unemployment-benefit·/calc/salary curl 200 + 제목 일치 한 줄(decisions/log.md), 실패면 today.md 막힘 칸 · 금지: 사이트 코드 고치기(막힘만 적고 순돌이 몫)
  완료: firemap-watchdog 13:22 — (10/8 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 13:52
  완료: firemap-watchdog 13:53 — 사이트 4쪽 curl 200·제목 일치(/ 파이어 가능 나이 계산기 · /calc/severance 퇴직금 계산기 · /calc/unemployment-benefit 실업급여 계산기 · /calc/salary 연봉계산기 2026). 막힘 없음
  착수: firemap-watchdog 18:39
  완료: firemap-watchdog 18:51 — (10/12 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  완료: firemap-watchdog 09:53 — (10/7 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:53 — (10/9 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:52 — (10/10 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:53 — (10/11 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:53 — (10/13 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 10:25
  완료: firemap-watchdog 10:26 — (10/14 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:53 — (10/15 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
  착수: firemap-watchdog 09:52
  완료: firemap-watchdog 09:53 — (10/16 회) 사이트 4쪽 curl 200·제목 일치(/ · /calc/severance · /calc/unemployment-benefit · /calc/salary). 막힘 없음
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
  완료: firemap-write 07:25 — 10/13 18:10 카페 칸 편 확정·관문 통과 reitetf1013(TIGER 리츠부동산인프라·KODEX 한국부동산리츠인프라 1억 1년 세전/세후, 배당현금흐름·형식2, 검색 9,810 새것): readcheck 0·selfcheck 사실 0·aitell 2.9·crosscheck 사실 2 반영·레드팀 2회(숫자 직접 재조회 일치, 틀림 1 반영)·제목 7.67·표지 K4 8.0·compare.md 8편·editgate auto → slots.json gates_ok 07:24 · 10/14 카페 10:10~22:10 일곱 칸 배정(renew1011·npsage1009·R-1 짝·cheongyak1012·qqqm1014·r1s_fx 짝·DC형, 관문 아직) · 카페 비축 1/2 그대로(npsage는 12:10 칸으로 쓰이게 돼 reserve 항목이 겹침, 새 비축 편은 다음 회차) · 경로 work/research/reitetf1013
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
  착수: firemap-copywriter 18:49 (① 본전·회복 허용 판단)
  완료: firemap-copywriter 18:57 — '본전'·'원금' 계속 금지(KRX 매매 수수료가 빠져 실제 본전은 +50.7%보다 큼, 168px에 '수수료 별도'를 읽힐 자리 없음) · '회복'은 '산 값 회복'처럼 목적어 붙일 때만 허용 · r1 틀 문구만 바꿔 재시험(rejudge_ff 고정 조건): u1 '고점에 샀다면?/산 값 회복까지/+51%' 6·6.5 · **u2 '금 -34%/산 값 회복까지/+51%' 6.5·6.5**(보정 7.5·7) — r1 6.13보다 +0.37, '+51%=수익률' 오독은 사라졌지만 **7 미달**. 남은 지적은 그림 정적·질문형 아님 → 문구는 병목 아님(07:52 결론 그대로) · 근거 cardshorts/g1_climb/ff3/README.md
  [알림] **firemap-shorts·firemap-visual-designer** (copywriter 18:57): 쇼츠 첫 프레임에 '산 값 회복까지'는 써도 됨('본전'·'원금'·'회복' 단독은 여전히 금지). g1_climb 다음 판을 만들면 문구는 u2(cardshorts/g1_climb/ff3/u2.png), 남은 1점은 그림·움직임 몫
- 막힘(firemap-video-producer 16:09): W-1 10/11 칸 skip — 무료 TTS 한 창 W-1 몫 8요청 중 3요청이 음높이 벗어남(0장 두 번 125~128Hz, 3장 173Hz)으로 날아가 5·6·7장 17줄 못 받음 · 받은 38줄도 IQR 0.19(R-1·G-1·C-1에 이어 네 번째) → 무료 Gemini TTS로는 IQR 0.16 통과가 운이라는 10/9 판단 그대로. 판단 필요(순돌이): ① Chirp 3 HD 결재(approvals.md 맨 위) ② W-1을 다음 주 2화로 넘길지·이번 38줄 버릴지 · 담당 순돌이
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
  착수: firemap-visual-designer 17:04
  완료: firemap-visual-designer 17:05 — 할 일 없음으로 닫음: firemap-write가 16:23에 재시안 I('6.5배' 430px 판 폭 77%·아랫줄 130px) 세 명 평균 7.0으로 통과시킴(cover_review.md, pkg/img/00.png=I), slots.json 08:10 칸 gates_ok 16:26 · 더 고치지 않음(넣었다 뺐다 금지)
- [카피 요청] P-1 국민연금 수령나이 롱폼 제목·썸네일 문구·첫 3초 트랙:C · 담당 firemap-copywriter · 시한 10/12 12:00(주간 선정 전) · 근거 longform/ep/P-1/analysis.md ②(검색어 '국민연금 수령나이' 45,780 맨 앞)·compete.md 경쟁 제목 틀(명령형 경고·'덜컥 받으면 큰일' — 피할 틀)·script.md 0장(하루 차이 생일 두 장) · 금지: '받으세요'·'이득'·'손해'·68세 단정 (youtube-loop 12:49)
  착수: firemap-copywriter 18:49
  완료: firemap-copywriter 18:57 — P-1 1위 제목 '국민연금 수령나이, 1년만 당기면 따라잡히는 나이가 오히려 늦다'(대본 첫 3초 둘째 줄과 글자 같음) + 썸네일 '5년 당김 76.7세 / 1년 당김 80.7세'(작은 줄 '제때 받은 쪽이 따라잡는 나이 · 1969년생·월 100만원 가정') · 12안 1차 제미나이·레드팀 둘 다 P5 1위 → 결선 평균 8.33(제미나이 8.8·레드팀 8.2·작성자 8.0) · 2위 '…연봉 약 7,600만원을 넘으면 월 15만원부터 깎여요' 8.17 · 사실 대조 전부 맞음, aitell 0.0 · 근거 longform/ep/P-1/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 18:57): P-1 meta.json 만들 때 title_candidates=[1위, 2위](copy/titles.md). 썸네일 작은 줄 '1969년생·월 100만원 가정' 지우지 말 것(1965~68년생은 75.7·82.9) · '15만원씩'·'월급 519만원'·'6/17 개정' 금지
- [편집 검수 요청] P-1 대본 v1 트랙:C · 담당 firemap-editor · 시한 10/12 18:00 · 근거 longform/ep/P-1/script.md(말 76줄, say_v1.txt) · scriptnum 35개 중 사실표 밖 0·aitell script 62.9/7% 통과·제미나이 지적 3 반영(review_v1_gemini.md) · 금지: 숫자·조문 표현('조문대로 계산하면') 바꾸기 (youtube-loop 12:49)
  완료: firemap-editor 17:08 — v2.1 요청(아래)으로 대체, v2.2로 편집 통과
- 확인(youtube-loop 12:49): 자발 — PD 대기열 C-1·G-1 뒤 빈칸이라 P-1 대본 v1을 주간 선정(10/12) 전에 미리 씀. 선정 안 되면 비축 롱폼. 남은 것: 심사 3명(review.md)·카피·편집
  완료: firemap-youtube-loop 16:52 — P-1 대본 v2.1 심사 3명 평균 **7.20 통과**(제미나이 7.2·Claude 7.30·레드팀 7.10, 막는 사실 오류 0) · 새 짜임 적용(0~45초 본편 줄 재사용 예고 5줄→'결론부터'→궁금증형 장 제목 7→가상 인물 '69년생 연금 씨' 장면 3) · 숫자 변경 0(scriptnum 39 밖 0·aitell 69.5/7%) · review.md 판정 줄 · 남은 것: 카피(792줄)·편집(아래 v2.1 요청)
- [편집 검수 요청] P-1 대본 v2.1(793줄 v1 요청 대체 — 0장·1장·결론부터·장 제목 바뀜) 트랙:C · 담당 firemap-editor · 시한 10/12 18:00 · 근거 longform/ep/P-1/script.md(말 78줄 say_v2.txt)·review.md 남긴 지적(④ '~입니다' 단조) · 금지: 숫자·날짜 바꾸기, 예고 줄은 본편 줄과 글자 같게 유지(PD가 녹음 조각 재사용) (youtube-loop 16:52)
  착수: firemap-editor 17:04 (정기 16:50)
  완료: firemap-editor 17:07 — 편집 통과: P-1 대본 v2.2(script.md, 원본 script.md.orig·script.v2_1.md) · 말투 16곳만: 끝맺음 섞기(say 기준 -요 75→60%·습니다 17→24%·같은 끝 최장 연속 8→5)·물음표 2·6장 긴 문장 하나 둘로(말 78→79줄) · 숫자 diff 0·조문 표현 그대로·예고 5줄 본편과 글자 같음(각 2회 확인) · aitell script 69.1/1,000·7% 통과·AI 티 0.0 · say_v3.txt 새로 뽑음(녹음은 이걸로) · script.md.edit.json · 참고(막지 않음, youtube-loop 몫): 제미나이 사용자 반론(say_v3_사용자.md)은 말투 아닌 표적 지적 — 30대 파이어 시청자에겐 '69년생' 기준이 멀다, 조기은퇴 공백과 연결 원함
- [알림] **firemap-write** (improve 14:37): rules.json 새 규칙 — 카페 배당·ETF 제목은 %보다 원 금액(224편 실측, 배당·ETF 안 % 제목 19편 하루당 0.41 vs 48편 0.74). 오늘 22:10 odivfx1010 제목 '…석 달 새 11.35% 감소'가 해당 — facts C5에 '100주 세후 34,958→30,989원(3,969원 감소)' 금액이 있음. 제목을 바꾸면 제목 관문(judge_title) 다시 거칠 것, 시간이 없으면 그대로 내도 됨(판단은 write)
- 예술가 제안: **DA 문턱 쇼츠 '국민연금 밖' 대조 1편** — 건보 피부양자 소득 2,000만원 경계 두 칸('1,999만원 / 2,001만원' → 피부양자 유지 / 지역가입자), 숫자는 시행규칙 별표 원문 사실표 먼저(내 원문 확인 안 함)·보험료는 계산 줄 있을 때만·'폭탄' 금지 → 담당 firemap-shorts, 다음 빈 쇼츠 칸(비축 0이면 비축 1번), 시험 기한 10/17 · 목적: AL(npsday1007 46h 1,457회, 1초 5·5)이 '문턱 모양' 덕인지 '국민연금 검색어' 덕인지 가르기 · 성공: 48h ≥675(중앙 450×1.5) 또는 댓글 '부모님' ≥3 · 버림: 48h <450이면 문턱은 국민연금 안에서만 · 경쟁 상위 8편 전부 8~28분 설명, 경계 두 칸 쇼츠 0 · 근거 art/2026-10-10-1445.md DA (artist 14:48)
- 판정(artist 14:48): **AL 하루 차이 문턱 성공**(성공선 48h ≥430 → 46h 1,457회, 최근 12편 1위) → [알림] **firemap-youtube-loop**: longform/loop/proven-formats.md에 쇼츠 '문턱 두 칸' 틀 등록 검토(기준선 1.5배 넘음 — 편마다 새 원문 1개) · 참고: 1초 점수 5·5 편이 1위 = X-SHORTS-1S 판정 자료 · AY 계기판 247회(시청 시간 비교 확인 안 함)
  완료: firemap-youtube-loop 20:45 — proven-formats.md 새로 만들고 쇼츠 S1 '문턱 두 칸' 잠정 등록(npsday1007 1,475·d1_kunbo 695, 기준선 300의 4.9·2.3배) · 수요 덕인지 틀 덕인지는 DA(kwvol 30) 결과로 가름, 450 미만이면 '수요 있는 주제에서만'으로 좁힘
- [배차] firemap-shorts 비축 쇼츠 0/1 — artist 14:48 제안 DA 문턱 '1,999만원/2,001만원' 피부양자 대조 1편(AL 문턱 틀 46h 1,457회 성공) 사실표 원문부터·관문 통과 시 reserve.shorts (운영실장 15:10)
  착수: firemap-shorts 15:10 (운영실장)
  완료(미달): firemap-shorts 15:30 — DA 문턱 피부양자(da_thresh): 법제처 원문(시행규칙 별표 1의2 소득요건 '연간 2천만원 이하'·시행령 제41조·법 제6조③) facts.txt·compete 5(경쟁 전부 '탈락 N가지' 목록, 경계 두 칸 0/5, 조회/구독 x75.9)·check 문제 없음·32초 아닌 6초 vs 카드 렌더·전체 영상 점검 통과(빈 곳 65%→38%, cardshort.py vs_point_size 추가). 1초 시험(첫 프레임 168px) v1 5·5·v2 5·5 = 5.0 미달 → gates_ok·reserve.shorts 안 넣음, **비축 쇼츠 0/1 그대로**. 안 돌린 것: aitell·편집·레드팀(미달이라 건너뜀). 키워드 수요 낮음(kwvol 피부양자소득 30) (cardshorts/da_thresh/review.md)
- 막힘(운영실장 16:11): ① W-1 16:01 창 38/55줄·IQR 0.19 미달 → 10/11 19:30 롱폼 칸 skip(PD ad63285) · 순돌이 판단: Chirp 3 HD 결재, W-1 다음 주 2화로 넘기고 38줄 버릴지 → firemap-video-producer ② 비축 쇼츠 0/1 — da_thresh(피부양자 2천만원 경계) 사실표·렌더 끝, 1초 시험 5·5 미달(4ea0281) · 쇼츠 1초 천장 문제(copywriter 07:52) 그대로 → firemap-shorts·순돌이
- [알림] **firemap-write** ← firemap-editor (17:08) 오늘 22:10 odivfx1010 c01 '…3,969원이 줄었어요'→'…빠진 거죠'(같은 맺음 3번) — 숫자·출처·면책 0 변경, frame 통과, editgate 재stamp, 발행 그대로 진행
- [알림] **firemap-youtube-loop** ← firemap-editor (17:08) P-1 대본 v2.2 편집 통과 — 녹음은 say_v3.txt(79줄, 6장 한 문장이 둘로) · 제미나이 사용자 반론(say_v3_사용자.md): 말투·신뢰는 좋음, 30대 파이어 시청자에겐 '69년생' 기준이 멀다는 표적 지적 — 판단은 youtube-loop
  완료: firemap-youtube-loop 20:45 — 69년생 기준 유지(시청자 45~64세 57.7%·25~34세 16.5%, ytanalytics) · 30대 각도는 별도 편 후보 '조기은퇴 납부 공백·임의가입·추납'으로 10/12 주간 선정에 · 근거 ep/P-1/review.md 끝
- 확인(firemap-editor 17:08): 정기 16:50 근무 — 열린 [편집 검수 요청] 1건(P-1 v2.1) 통과, v1 요청(794줄)은 v2.1로 대체돼 닫음 · auto 표본 1(고침 1) · sweep은 다음 근무
- [배차] firemap-write 비축 카페 실사용 0/2(npsage1009는 10/14부터) — youthsave1010 사실표 이어서 원고~관문 통과 시 slots.json reserve.cafe (운영실장 19:09)
  착수: firemap-write 19:09 (운영실장)
  완료(막힘): firemap-write 19:21 — youthsave1010 원고·표·제목·표지 시안·레드팀 반영 끝, **관문 못 넘음**: aitell 편집 관문이 '카페 주제 밖(청년 전용 상품)'으로 막음(brand/guide.md ①-카페 주제 범위, 청년 전용 상품=카페 금지→새 사이트 쪽). 우회 안 함, reserve.cafe 안 넣음, 비축 카페 실사용 0/2 그대로 · 결정 필요(brand-director/순돌이): ① 이 편만 예외 허용(신청 마감 10/16, 검색 679,300) 또는 ② 새 사이트 X-CN-1로 보냄 · 남은 관문은 youthsave1010/review.md · 경로 work/research/youthsave1010
  결정: firemap-meeting 21:41 — youthsave1010 **예외 없음**(brand/guide.md ① 카페 주제 범위, 기준 하나). 원고는 보관만. 카페 비축은 세금연금·형식2 편으로 채운다
- [배차] firemap-visual-designer 비축 롱폼 0/1 준비 — P-1 썸네일 시안(copywriter 18:57 1위 문구 '5년 당김 76.7세 / 1년 당김 80.7세'·작은 줄 '1969년생·월 100만원 가정' 유지), 주간 선정(10/12) 전 미리 (운영실장 19:09)
  착수: firemap-visual-designer 19:09 (운영실장)
  완료: firemap-visual-designer 19:23 — P-1 썸네일 **p1f 조건부 확정**(2차 세 명 평균 7.17: 제미나이 3.1-lite 7.5·8.5·Claude 7.0·레드팀 6.5, 목표 8 미달) · 진한 크림 판 + 65~85세 눈금 위 막대 둘(5년 당김 76.7세 짧은 남색·1년 당김 80.7세 긴 빨강 = 반전을 길이로) · 문구 copywriter 1위 그대로·작은 줄 '1969년생·월 100만원 가정' 유지·금지어 0 · 1초 블라인드 2차수 모두 주제 맞힘 · 사실 대조 맞음·가려짐 0 · 대조 p1b 6.58·p1e 6.73 · 열린 위험(레드팀): 막대가 65세에서 시작해 '받는 기간'으로 오독 가능 → 다음 회차 p1g(끝점 표시) 같은 판 재심 · 파일 ep/P-1/thumb_p1f.png · 근거 visual/P-1-thumb/judges.md
  [알림] **firemap-youtube-loop·firemap-video-producer** (visual-designer 19:23): P-1 meta.json 만들 때 thumb=thumb_p1f.png(조건부 7.17), thumb_alt=thumb_p1e.png(6.73). 공개 48h 뒤 CTR 중앙값 미만이면 교체 1회
- 막힘(운영실장 19:24): 비축 카페 실사용 0/2 그대로 — youthsave1010(청년 저축 상품, 신청 마감 10/16) 원고·사실 관문 끝났으나 editgate가 '카페 주제 밖(청년 전용 상품)'(brand/guide.md ①)으로 막음(3dcf119) · 순돌이 판단: 이 편 카페 예외 허용 여부, 아니면 비축은 다른 주제로 · 비축 쇼츠 0/1 그대로(1초 천장 문제) · P-1 썸네일 p1f 평균 7.17 조건부 확정(6a489c1, 레드팀 '65세 시작 막대' 오독 위험 → p1g 재심 backlog)
- [자발] copywriter M-1 공개 48시간 클릭률 판정 (열린 지시 0)
  착수: firemap-copywriter 01:49
  완료: firemap-copywriter 01:52 — M-1(eTjVs1vDTwg) 공개 조회 16 · 노출 보고서 10/8만(노출 20·5.0%, 클릭 1) → **판정 불가, 제목·썸네일 교체 안 함**(교체는 한 번뿐) · 누적 노출 100회 넘는 보고서 들어오면(10/12~13) 재판정, 비교선 N-1 5.38%·A-1 8.14% · 낮은 건 클릭률보다 노출(N-1 첫날 1,164 vs M-1 20) · 근거 copy/learn.md 끝
  [알림] **firemap-youtube-loop** (copywriter 01:52): M-1 title_swap은 아직 쓰지 말 것 — 노출 20회로는 클릭률 판정 안 됨. 문제는 노출 쪽(주제·첫 노출 창)이라 카피 교체로는 못 고침
- [배차] 10/11 22:10 카페 칸 TBD(관문 기한 16:10) 편 정하고 관문까지 · 담당 firemap-write
  착수: firemap-write 03:10 (운영실장)
  완료(미달): firemap-write 03:14 — 22:10 칸 편 확정 renew1011(계약갱신청구권 갱신 증액 5%·실거주 거절 뒤 제3자 임대 손해배상, 부동산·형식2, 수요 12,060·dupcheck 새것) · 법령 원문(주임법 6조의3·7조·7조의2·시행령 9조)·기준금리 3.0%→전환율 5% 확인·calc.py·facts.txt·slot.txt(10/11 22시) · 원고·교차검증·제목·표지·editgate·gates_ok 아직(기한 16:10) — 08:10 write가 이어서. 10/12 08:10 칸은 못 함(후보 디딤돌 대출 60,800 새것)
- [배차] 비축 쇼츠 0/1 — proven-formats S1 '문턱 두 칸' 틀로 예비 1편 · 담당 firemap-shorts
  착수: firemap-shorts 03:10 (운영실장)
  완료(미달): firemap-shorts 03:23 — 비축 쇼츠 문턱 두 칸 = bp_thresh(기초연금 선정기준액 단독 월 247만원 이하 vs 초과, 복지부 보도자료 10/11 원문 확인·facts.txt·compete 5·수요 기초연금기준 7,770/월). check 문제 없음·렌더. 1초 시험(첫 프레임 168px, 고정 조건) v1 5·5, v2 6·6 = 7 미달 → gates_ok·reserve.shorts 안 넣음, **비축 쇼츠 0/1 그대로**. 안 돌린 것: aitell·편집·레드팀(미달). 다음 안: 두 상자 숫자를 다르게(단독 247만원 vs 부부 395만 2,000원) 또는 질문형 제목 (cardshorts/bp_thresh/review.md)
- 막힘(운영실장 03:24): ① 10/11 22:10 카페 renew1011(계약갱신청구권) 사실표·계산만, 원고~gates_ok 남음(기한 16:10, baf1731) → write 08:10 정기 1순위 · 10/12 08:10 칸 미배정(후보 디딤돌, 기한 02:10) ② 비축 쇼츠 0/1 — bp_thresh(기초연금 선정기준 247만원) 1초 v1 5·5·v2 6·6 미달(2417945), 다음 안 review.md · 쇼츠 1초 천장 문제 그대로 → 순돌이 판단 · 비축 카페 실사용 0/2
- [자발] 롱폼 하루 한 편 대본 비축 — 10/16·17 칸 TBD(R-1·P-1·I-1), 대본 준비본 P-1뿐 → I-1(ISA) 원문·경쟁 (youtube-loop)
  착수: firemap-youtube-loop 04:47
  완료: firemap-youtube-loop 04:52 — I-1 사실표 facts.txt(조특법 §91의18 2026-09-18 시행본·소득세법 §129·지방세법 §103의13·재경부 8/3 상세본·**9/1 정부안 보도자료 korea.kr 원본**: 일반 ISA 5년 제한·이월 불가 철회, 생산적금융 ISA도 무기한·이월, 국회 통과 전) · compete.md 9/1 이후 상위 5편(김짠부 47.3만·래빗해빛 2.19배 등) — **'개편 철회'는 9월에 다 다룸 → 빈칸은 '같은 돈 계좌만 바꾼 실제 5년 세후 영수증'**(5편 중 래빗해빛 한 줄 계산뿐) · ② kwvol: ISA계좌 70,700·생산적금융ISA 8,210 · 남은 것: ETF 과표기준가 자료 확인 → calc.py → 대본 v1 (10/18 이후 칸 후보)
- [알림] **firemap-video-producer**(15:05·16:01 회차) · **운영실장** ← PD (06:21) W-1 10/12 칸 메모대로 '못 받은 17줄만' 받으면 녹음 날 10/10 38줄+10/11 17줄 = 둘째 날 30.9% → lfrender 날짜 규칙(둘째 20% 이하)으로 **렌더 거부**. 고친 순서: 0·1장 11줄만 10/10으로 두고 2~7장 44줄을 16:01 창 5요청(C-1 최대 3 다음)으로 새로 받음 → 10/10 몫 20.0% · ep/W-1/check/runbook_1011.md·park_1011.py(--dry 확인: 남김 11·옮김 27) · 기준 그대로·TTS 0회 사용
- [요청] **firemap-youtube-loop**(대본)·**firemap-editor**(재서명) ← PD (06:21, 기한 10/11 15:00 — 16:01 녹음 전) W-1이 10/12(월) 19:30 공개로 바뀌었는데 말 줄에 '이번 주' 12곳(0장 2·1장 1·2장 3·3장 2·7장 4)·장 제목 '6. 다음 주에 볼 날짜' — 월요일 시청자에게 '이번 주'는 10/12~16 주라 사실과 어긋남. '지난주'·'이번 주에 볼 날짜' 등으로 고칠지 판단·고치면 editor 재서명. 숫자 0 변경. 0·1장 줄이 바뀌면 PD가 그 줄도 새로 받음(요청 +1~2). 기한 안 답 없으면 편집 통과본 그대로 녹음
  착수: firemap-youtube-loop 07:09 (운영실장)
  완료: firemap-youtube-loop 07:11 — 고침 판정(editor 제안본 그대로 채택): W-1 script.md에 시간말 16줄만 반영(이번 주→지난주 11행·다음 주→이번 주 3곳·'같은 주'·'10월 둘째 주' 각 1), 숫자·날짜·면책 뜻 0 변경, script.1011_proposal.md.edit.json(sha da6522a0)→script.md.edit.json 복사·sha 일치, say_v2.txt 같은 말 줄 동기, aitell 67.7/1,000·12% 통과, lfvoice plan 장 구성 그대로. 시리즈 이름 '이번 주 뉴스가 내 돈에 얼마'와 107행 '다음 주에도 이 시간에'는 그대로(코너 이름·다음 회차 예고). 근거 ep/W-1/check/thisweek_1011.md
- [알림] **firemap-video-producer** (youtube-loop 07:11, 16:01 녹음 전) W-1 대본 시간말 바뀐 줄(script.md 행/say_v2 행): 11/1·17/4·25/6·44/17·55/23·56/24·66/28·68/29·99/44·111/50·112/51·114/53·115/54 + 장 제목 23(1장 '지난주는 사흘짜리였어요')·97(6장 '이번 주에 볼 날짜')·화면 메모 98. 녹음 영향: 0장 2줄(11·17)·1장 1줄(25)·1장 제목·그 밖 지난주/이번 주 줄 → 이미 받은 소리 중 해당 줄만 새로 받기(옛 소리 보관), 나머지 그대로. 화면 글자는 PD 몫(check/thisweek_1011.md '화면 글자'): scenes.0.title·9 data.head·scenes.4.title·scenes.12.title·scenes.21.title '이번 주에 볼 날짜'·scenes.24.data.head·data.note·W1.tsx 고정 칸 '지난주 영수증' — 그대로 둘 것: 시리즈 이름·'다음 주 이 시간 새 영수증'. 카페 cafe.md의 '이번 주'도 10/12 월요일 공개 기준으로 firemap-write가 맞출 것. editor 재서명 필요 없음(제안본 서명 그대로 복사).
  착수: firemap-editor 07:04 (정기 06:50)
  진행: firemap-editor 07:05 — 편집 쪽 준비 끝: 제안본 ep/W-1/script.1011_proposal.md(시간말 16줄, 숫자 0 변경)·미리 서명 .edit.json·대조표 check/thisweek_1011.md(화면 글자 9곳 포함) · youtube-loop가 제안본을 script.md로 쓰면 서명 복사만 하면 됨, 고쳐 쓰면 editor 재서명 · script.md는 아직 안 바뀜(담당 youtube-loop)
  완료: firemap-editor 07:08 — 편집 몫 끝: 제안본 script.1011_proposal.md 미리 서명(sha da6522a0, 시간말 16줄·숫자 0) · youtube-loop가 그대로 쓰면 script.1011_proposal.md.edit.json을 script.md.edit.json으로 복사, 다르게 고치면 [편집 검수 요청] 다시 · 화면 글자 9곳은 PD 몫(check/thisweek_1011.md)
- [알림] **firemap-write** ← firemap-editor (07:08) 오늘 08:10 inhded1011 c02 한 곳·14:10 cardded1011 '-죠' 맺음 13→8(c01·c02·c05) 말투만 손봄 — 숫자·출처·면책 0 변경, frame 통과, editgate 재stamp, 발행 그대로 진행. aitell에 '~죠' 쏠림 검사 생김(12% 넘으면 점수)
- [알림] **firemap-youtube-loop·firemap-video-producer** ← firemap-editor (07:08) W-1 '이번 주' 고침안 = ep/W-1/script.1011_proposal.md(편집 미리 서명) · 대조표 ep/W-1/check/thisweek_1011.md(말 16줄 + 화면 글자 9곳) — 쓰기로 하면 0장 2줄·1장 1줄+장 제목이 바뀌어 녹음 +3~4줄
- 확인(firemap-editor 07:08): 정기 06:50 근무 — 열린 요청 1건(W-1 이번 주) 편집 몫 끝 · auto 표본 2(고침 2) · sweep은 다음 근무
- [배차] 10/12 08:10 카페 칸 미배정(관문 기한 02:10 지남) 편 정하고 관문까지 — 후보 디딤돌 · 담당 firemap-write
  착수: firemap-write 07:09 (운영실장)
  완료(일부): firemap-write 07:19 — 10/12 08:10 칸 편 확정 didim1012(디딤돌 대출 소득 칸별 월 상환액·검색 60,800·dupcheck 새것) 원고·readcheck 0·selfcheck 사실 0·aitell 0.0·frame 통과·compare.md·제목 평균 7.5·레드팀 사실 오류 1 반영 / 남은 관문: 표지 제미나이·제3 심사(레드팀 7 하나)·crosscheck·editgate — gates_ok 못 씀(기한 02:10 지남), 08:10 정기 근무 몫 · renew1011은 안 건드림
- 막힘(운영실장 07:20): 10/12 08:10 카페 didim1012(디딤돌 대출) 원고·제목 평균 7.5까지, 표지 평균 줄·crosscheck·editgate·gates_ok 남음(기한 02:10 지남, 03d500d) → write 08:10 정기가 renew1011(기한 16:10)과 함께 · W-1 '이번 주' 고침 script.md 반영·서명 복사(c24785c) — PD 16:01 녹음 때 바뀐 줄만 다시 받기·화면 글자 9곳 PD 몫 · 비축 쇼츠 0/1·카페 실사용 0/2 그대로
- [자발] copywriter H-1(10/15 19:30 롱폼) 제목·썸네일 문구 결선 — meta.json 'copywriter 결선 전'(본부장 가안 3개) (열린 지시 0, G-1 calc 대조는 10/12)
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:55 — 1위 제목 '올림픽파크포레온·헬리오시티 84㎡ 1년 실거래 전부 깔아 보니, 평당 1억 1천만원 거의 같았다' + 썸네일 '6년 가까이 늦게 지었는데'(작은 줄 '84㎡대 1년 실거래 · 평당 중앙') · 12안 1차(제미나이 H5 10·레드팀 H4 8.0) → 결선 평균 8.63(제미나이 9.0·레드팀 8.4·작성자 8.5) · 2위 F1 8.20(썸네일 '23.8억 한 건, 나머지는 30억+') · 본부장 가안 사실 오류 고침: '6년 차이'(5년 11개월)·H2 '23억+직거래 2건'(23.82억은 중개거래) · aitell 0.0 · 겹침 최고 0.33 · 근거 longform/ep/H-1/copy/titles.md·review.md
  [알림] **firemap-video-producer·firemap-visual-designer** (copywriter 07:55): H-1 meta.json title·title_swap·thumb_text(_small)·thumb_text_swap(_small) 넣음 — 썸네일 큰 글씨에 '−0.6%'·'−37%'·'직거래'·'6년 차이' 쓰지 말 것(하락·사정 오독), 23.8억은 내림 금지 · 2위 썸네일 작은 줄 '헬리오시티 84㎡'는 크게(작으면 포레온 거래로 읽힘)
  착수: firemap-visual-designer 09:04 (정기) — H-1 썸네일 시안·1초 시험(1위 문구 '6년 가까이 늦게 지었는데')
  완료(미달): firemap-visual-designer 09:19 — H-1 썸네일 1~4차 8안(h1a~h1h, 실제 84㎡대 거래 점 85·45건 판) **7 넘은 안 없음** · 임시 thumb_h1d.png(2차 평균 6.58: 제미나이 3.1-lite 6.5·6·Claude 6·레드팀 7.5, 겹침 2) meta.json thumb·thumb_status 적음 · 제미나이 블라인드 1초 4차수 모두 주제 맞힘, Claude는 168px 단지 이름 작음으로 5~6 고정 · 결론 '둘 다 평당 1억 1천만' 크게(h1h)는 경쟁 '억 금액 줄'과 겹침 3으로 레드팀 반려 · 같은 판 멈춤, 다음 회차 새 형식(이름 100px급 좌우 두 칸·큰 입주 연도·점 띠 축소) · 근거 visual/H-1-thumb/judges.md·compare.png
  [알림] **firemap-video-producer** (visual-designer 09:19): H-1 썸네일은 아직 임시 thumb_h1d.png(6.58, 통과 아님) — 업로드 판 확정은 관문 기한 10/14 19:30 전 visual-designer가 다시 알림
  착수: firemap-visual-designer 17:03 (정기) — H-1 썸네일 새 형식 5차(이름 좌우 두 칸·큰 입주 연도·점 띠 축소), h1d 대조
  완료: firemap-visual-designer 17:14 — H-1 썸네일 **h1k 조건부 확정**(새 형식 5~7차 6안, 7차 세 명 평균 7.00: 제미나이 3.1-lite 7.5·7.5·Claude 7·레드팀 6.5, 겹침 2, 목표 8 미달) · 판: 좌우 두 칸(헬리오시티 2018 입주 / 올림픽파크포레온 2024 입주, 연도 144px) + 아래 전폭 띠 '둘 다 평당 1억 1천만' · 1초 블라인드 7차수 모두 주제 맞힘 · 사실 대조 맞음(85·45건·11,087·10,988)·가려짐 0 · 대조 h1j 6.97→5.83·h1n(실제 두 값) 6.5·h1m('평당 ?') 6.33 · 7차부터 심사에 바뀐 질문형 제목 반영(질문=제목·답=썸네일, title_1011.note와 같음) · meta.json thumb=thumb_h1k.png·thumb_alt=thumb_h1d.png · 근거 visual/H-1-thumb/judges.md 5~7차
  [요청] **firemap-copywriter** ← visual-designer (17:14) H-1 썸네일 h1k 문구 2가지 · 기한 10/13 18:00(관문 10/14 11:30 전) · ① 띠 '둘 다 평당 1억 1천만'을 '…1억 1천만 안팎'으로 할지(포레온 10,988은 반올림 1억 1천, 레드팀 6차) ② 작은 줄 '84㎡대 1년 실거래 · 평당 중앙'에 '전용'을 넣을지(facts.txt 39행 평당=전용 기준, 공급 평당 시청자 반박 위험 — 레드팀 6·7차) · 바꾸면 meta thumb_text_small만 고치고 visual이 make_thumbs.py h1k 다시 렌더 · 근거 visual/H-1-thumb/judges.md 5~7차
  착수: firemap-copywriter 19:07
  완료: firemap-copywriter 19:09 — ① 띠 '둘 다 평당 1억 1천만' → **'둘 다 평당 약 1억 1천만'**('안팎'은 3자 더라 84px 전폭 띠 15자≈1,260px로 넘침, '약'은 2자) ② 작은 줄 **'84㎡대 1년 실거래 · 전용 평당 중앙'**(meta thumb_text_small 고침, cd9fe3e, facts '평당=전용면적 기준') · aitell 0.0 · 근거 ep/H-1/copy/titles.md 끝
  [알림] **firemap-visual-designer** (copywriter 19:09): H-1 make_thumbs.py h1k 띠 글자를 '둘 다 평당 약 1억 1천만'으로 바꾸고 다시 렌더(작은 줄은 meta에서 읽음) — 168px에서 띠가 넘치지 않는지만 확인
  [알림] **firemap-video-producer** (visual-designer 17:14): H-1 썸네일 = ep/H-1/thumb_h1k.png(조건부 7.00), thumb_alt=thumb_h1d.png(6.58). 업로드 때 h1k · 공개 48h 뒤 CTR 중앙값 미만이면 교체 1회
- [자발] I-1(ISA) calc → 분석 관문 ④-0~⑧ → 대본 v1 (롱폼 하루 한 편, 10/16·17 칸 대본 비축) · youtube-loop
  착수: firemap-youtube-loop 08:43
  완료: firemap-youtube-loop 08:51 — 과표기준가 원자료 확보(제로인 funetf 360750 일별 종가·기준가·과표 2021~2026, 종가 야후 6개 날짜 일치)·운용사 과세식 원문·소득세법 §14③6 → calc.py: 1억(10월 2천만원×5)·5년 일반 세금 1,053만·세후 1억5,916만 vs ISA 일반형 659만·1억6,330만(**+414만**)·서민형 +434만 · **숨은 차이: 일반계좌는 판 해 배당소득 6,561만원 → 2천만원 문턱 넘어 종합과세**(경쟁 5편 중 0편) · analysis ①~⑧ 끝·실험 I1-HIDDEN · 대본 v1 말 71줄 aitell 통과(46.9·7%)·scriptnum 밖 0·제미나이 3.7-flash 막을 문제 2 반영 · 남은 것: 심사 3명 → 편집 → 카피 · 확인 필요 2(ISA 안 해외 ETF 차익 Min식 원문·분배금 과표증분 기간)
- [요청] **firemap-copywriter** ← youtube-loop (08:51) I-1 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/14 12:00 · 근거 longform/ep/I-1/analysis.md ②(맨 앞 'ISA 계좌' 70,700)·calc_out.txt [I_*]·[X2] · 결론 두 단(겉 +414만원 → 판 해 6,561만원·2천만원 문턱) · 금지: '갈아타세요'·'무조건'·종목 기호 제목 맨 앞(M-1 노출 20 가설)·서민형 숫자를 일반 결론처럼
  착수: firemap-copywriter 19:10
  완료: firemap-copywriter 19:16 — 1위 제목 **'ISA 계좌 vs 일반계좌, 같은 1억·같은 ETF 5년인데 다른 건 계좌 하나'**(대본 둘째 줄과 같은 말) + 썸네일 **'+414만원'**(작은 줄 'ISA가 더 손에 쥔 돈 · 안 잡힌 차이 하나 더') · 12안 1차(레드팀 I5 8.6·제미나이 I11 9.4/레드팀 7.4) → 결선 평균 **8.60**(제미나이 9.2·레드팀 8.6·작성자 8.0) · 2위 'ISA 계좌 없이 미국 지수 ETF 1억 5년, 파는 해 금융소득 6,561만원'+막대 8.50 · 숫자 calc_out 대조 맞음, aitell 0.0, 겹침 최고 0.13 · 근거 longform/ep/I-1/copy/titles.md·review.md
  [알림] **firemap-youtube-loop·firemap-video-producer·firemap-visual-designer** (copywriter 19:16): I-1 meta.json 만들 때 title_candidates=[1위, 2위](copy/titles.md) · 설명 첫 줄에 '2021~2025년 10월 2천만원씩 샀다고 가정·2026-10-08 종가' 꼭 · '세후 414만원'·'세금 폭탄'·'함정'·'5년 보유' 금지(414만은 종합과세 추가분 없는 값, 6,561만은 과세분)
  완료: firemap-youtube-loop 08:57 — I-1 대본 심사 3명 평균 **7.73 통과**(제미나이 8.4·Claude 7.2·레드팀 7.6, 막는 사실 오류 0, 레드팀 손 검산·calc 점검 통과) · v2 반영(문턱 '금지'처럼 들림·20만원 설명·3년 가입 제한 반전·끝 행동 한 문장, 숫자 0 변경, aitell 45.6/6%) · review.md 판정 줄 · 공개 조건 3(의안 확인·카페 글 먼저·공개 전날 calc)
- [편집 검수 요청] I-1 script.md(v2, 말 72줄) 트랙:C · 담당 firemap-editor · 시한 10/14 12:00 · 근거 longform/ep/I-1/script.md·say_v2.txt·review.md · aitell script 45.6/1,000·6% 통과 · 숫자 scriptnum 밖 0 · 요청 firemap-youtube-loop 08:57
  착수: firemap-editor 15:10 (운영실장)
  완료: firemap-editor 15:22 — 편집 통과 I-1 script.md(v2) · aitell 44.9/1,000·6% · 하는 일 없는 말 3줄 삭제+끝맺음 3곳, 숫자·사실 0 변경 · script.md.edit.json 찍음 · 화면 글자(screen_text)는 PD가 뽑은 뒤 따로 서명
- [알림] **firemap-video-producer(W-1·G-1 회차)** ← PD C-1 회차 (10:23) lfvoice.py에 Chirp 엔진 붙음: tts.json {"model":"chirp3-hd","voice":"ko-KR-Chirp3-HD-Charon","speakingRate":1.1} → make(줄마다) → 튀는 줄 `lfvoice.py retake <ep> 장:줄 --takes 5`. C-1 실측: speakingRate 1.0이면 편 전체 약 5.3(관문 5.5 미달)·1.05면 5.56·1.1이면 5.73 · 1.1에서 줄 속도 >8.2 '빠름' 4~8줄 나오나 retake --takes로 통과 · IQR 0.13·앞뒤 +1.1%. ytlong gate 시각 창 19~21시 → 11~21시(정규 11:30)로 고침.
- [편집 검수 요청] G-1 화면 글자 재서명 트랙:C · 담당 firemap-editor · 시한 10/12 09:00(관문 기한 10/12 11:30 전 렌더) · 근거 longform/ep/G-1/screen_text.txt — 서명(10/10 23:11) 뒤 바뀐 것은 motion 12:15 커밋(786689b, U5 겹침 고침)의 g1props 꼬리표 방향 한 줄 'scenes.5.data.tags.3.4 down→left'뿐(글자 아닌 배치 값) · 목소리는 Chirp 1.15로 10/11 전부 다시 녹음(관문 통과: 5.54음절/초·IQR 0.15·앞뒤 +2.1%) · 요청 firemap-video-producer 12:20
  착수: firemap-editor 14:21 (PD가 Agent로 투입)
  완료: firemap-editor 14:23 — 재서명 b74fbbdf…(b5e789a 서명본 대비 786689b diff 1줄 꼬리표 방향 down→left뿐, 글자·숫자 0 변경), lfrender check 관문 통과
- [요청] **firemap-motion-designer** ← PD (12:41, 기한: 16:10 C-1 듣기 결과가 NOISE면 바로) C-1 12:17 렌더본이 U5 같은 화면 8초에 12곳 걸림(최장 2:09~ 16초, 5:15~ 13.5, 5:57~ 12.5, 5:30~ 12, 1:14~ 12, 4:11~ 11.5, 3:55~ 10, 3:35~ 10, 0:05~ 9.5, 2:43~ 9, 1:29~ 9, 1:05~ 9 — 근거 scratchpad 아님: 다시 재려면 lfrender.py screen ep/C-1 <mp4>) · 지금 공개 계획은 U5 예외인 11:04 렌더본 + 16:00 뒤 제미나이 듣기(48.2초)라 C-1은 안 고쳐도 됨. 듣기가 NOISE면 새 렌더가 필요하고 그때 U5를 넘어야 함 → C1.tsx 장면 나누기/판 바꾸기 손 필요 · G-1·W-1도 렌더 전 같은 관문
- 막힘(firemap-report 12:47): M-1 48시간 노출 클릭률 확인 안 함 — 이번 회차 Studio 화면을 열지 않음(쿠팡·사이트 측정 우선). 다음 12:30 회차 첫 일 · 담당 firemap-report
- [편집 검수 요청] W-1 화면 글자 재서명 트랙:C · 담당 firemap-editor · 시한 지금(10/12 11:30 칸 관문 기한 10/11 11:30 이미 지남) · 근거 longform/ep/W-1/screen_text.txt — 서명(10/10 07:06) 뒤 바뀐 것은 79e0185의 시간말뿐(이번 주→지난주 화면 글자 9곳·6장 '이번 주에 볼 날짜'·25장 '토요일 이 시간 2화'·'10월 둘째 주'), 숫자 0 변경, 대본 script.md는 youtube-loop 07:11 서명 복사분과 같은 말 · 요청 firemap-video-producer 14:18 (10:29 요청 줄이 today.md에 없어 다시 씀)
  착수: firemap-editor 14:18 (PD가 Agent로 투입)
  완료: firemap-editor 14:20 — 재서명 f5883b3e…(83f63fa 서명본 대비 diff 24줄 시간말뿐·숫자 0 변경·말 55줄 script.md 일치·날짜 요일 맞음·aitell 3.3), lfrender check 관문 통과 · 남은 것: 2화를 10/17 11:30 롱폼 칸에 넣어야 '토요일 이 시간' 약속이 맞음(slots 10/17 item TBD, w1014/plan.md 제목은 아직 19:30)
- [요청] **firemap-meeting**·**firemap-youtube-loop** ← PD (14:20) W-1 1화(10/12 11:30) 말·화면에 '이번 주 토요일 이 시간에 2화'가 들어감 → 10/17(토) 11:30 롱폼 칸에 W-1 2화(w1014) 배정 필요(지금 slots ep TBD, R-1·P-1·I-1 후보 메모뿐) · w1014/plan.md 제목·관련 요청 줄의 19:30도 11:30으로 · 2화 대본은 10/16 11:30 전(관문 24h) 끝나야 함 · 근거 editor 14:20 재서명 메모
  착수: firemap-youtube-loop 18:51
  완료: firemap-youtube-loop 18:52 — slots.json 10/17 11:30 롱폼 칸 = W-1-2(w1014) 배정·owner PD · w1014/plan.md 19:30→11:30, 관문 기한 10/16 11:30(녹음 10/15 16:01 뒤 19.5시간) · 1화가 PD 제안대로 10/14 11:30으로 가도 '이번 주 토요일'=10/17이라 약속 맞음, 기간도 10/2→10/8 · 10/8→10/14로 안 겹침 · 1화가 10/17 뒤로 밀리면 2화도 다음 토요일로
- [요청] **firemap-meeting**·**firemap-write** ← PD (14:22) W-1 롱폼(10/12 11:30 예약 예정) 짝 카페 글 = ep/W-1/cafe.md(세 영수증 전체 표) — 10/12 카페 칸 하나(영상 11:30 공개 뒤 12:10 또는 14:10)에 yt_pair: W-1 · 영상 주소는 PD가 업로드 직후 slots note에 적음 · 설명란 앞 5줄 카페 줄은 지금 cafe.naver.com/firemap, 글 주소 나오면 PD가 videos.update로 바꿈 · 주의: cafe.md 표 머리 "이번 주(10/2 → 10/8)"는 10/12 발행이면 "지난주"(영상과 같게)
  완료(write 몫): firemap-write 15:18 — 10/12 14:10 카페 칸에 W-1 배정·note yt_pair: W-1(12:10은 kidcred1012 관문 통과분) · cafe.md 표 머리·25행 '이번 주'→'지난주' · 영상 주소는 PD가 14:10 칸 note에
- [알림] **firemap-video-producer** ← visual-designer (14:27) W-1 썸네일 8차 1초 시험 미달 — thumb_w1l.png 그대로 · 세 명 평균 w1l 6.93 · 처방판 w1n 6.32 · 도전안 w1o 6.18(통과선 7) · 셋 다 주제 맞힘 · '공시까지 사흘' 빼면 공시 원인 오독 2/3 → 남김 · 카드 '평가손익'은 사실 틀림(평가액 감소폭) · 다음 판 w1l 그림+작은 글 삭제+−140만 1.5배 · 근거 work/research/visual/W-1-thumb/judges.md 8차
- [알림] **firemap-video-producer** ← visual-designer (14:31) W-1 썸네일 9차 1초 시험 통과 — thumb_w1p.png로 교체(세 명 평균 7.37: 제미나이 7.5·Claude 7.3·레드팀 7.3, 셋 다 주제 맞힘), thumb_alt=thumb_w1l.png(6.92) · '공시까지 사흘' 안 씀(반쯤 틀린 말, 기간은 '10/2~10/8' 태그) · 남은 위험 '인데' 공시 원인 오독 2/3 → 48h CTR 확인 · 업로드 때 thumb_w1p.png 쓰기 · 근거 work/research/visual/W-1-thumb/judges.md 9차

- [배차] 10/12 카페 14:10·16:10·18:10·20:10·22:10 칸 미배정(patrol) — 편·담당 slots.json에 적기(W-1 짝 카페 ep/W-1/cafe.md는 12:10 또는 14:10 칸 yt_pair) · 담당 firemap-write
  착수: firemap-write 15:10 (운영실장)
  완료: firemap-write 15:18 — slots.json 10/12 카페 다섯 칸 배정(담당 firemap-write): 14:10 W-1 짝(yt_pair: W-1, ep/W-1/cafe.md '이번 주'→'지난주' 2곳·{F} SPY 10/9 최종 종가 확인해 숫자 그대로) · 16:10 cheongyak1012 청약통장(18,740 새것, 사실표 착수 — 조특법 87조 원문) · 18:10 QQQM(33,120 새것) · 20:10 쇼츠 m1s_nhis70 짝(yt_pair, 배당 건보료) · 22:10 퇴직연금 DC형(21,610 새것) / 양도소득세는 cafe/223(10/6)과 겹쳐 뺌 · patrol 미배정 경보 사라짐 · 관문은 아직(각 칸 기한 = 발행 6시간 전)
  막힘: firemap-write 15:21 — git push origin dev가 이 세션 권한(auto mode 분류기 'Production Deploy')에 막힘. 커밋 22d94ca는 로컬 dev에만 있음(ahead 3, 다른 직원 커밋 2개 포함) → 16:10 정기 근무·다른 회차 push가 함께 올림. 우회 안 함- [요청] **firemap-meeting**·**firemap-write** ← PD (15:28) C-1 세로 클립 4편 예약(07:20) — 쇼츠 1편 = 카페 글 1편(그 쇼츠 질문 하나 + 쇼츠 링크 + 원본 롱폼 DBJaHJ2pVTw + 그 질문의 표), 같은 날 20:10 또는 22:10 칸 · 10/12 c1s_half nPG2tHYsjpU '평균이면 평생, 실제로 돌리면?' · 10/13 c1s_300 32G21MwLY_A '3억에서 월 300만원 꺼내면 몇 년?' · 10/14 c1s_receipt QlL0VK4PB_8 첫해 7,223,493원 vs 0원 · 10/15 c1s_fx LEEGTOokOaM 1997 달러 +33.4%→원화 +123.6% · 근거 cardshorts/c1s_*/review.md · C-1 롱폼 짝 카페 글(ep/C-1/cafe.md)이 이미 나갔으면 같은 표 반복 금지(질문 하나만)
- [알림] **firemap-video-producer** ← motion (15:39) W-1 U5 통과 — out/w1.mp4 재렌더(15:39) 같은 화면 최장 7.0초·8초 넘는 곳 0·겹침 0(252프레임), screen.json ok · 고친 장면 2 three·9 rcpt·16 stamp·19 bridge·20 trio·23 road·24 sum·25 end(줄마다 말하는 항목을 검은 띠·카드로) · 화면 글자 새로 안 씀 → 재서명 불필요(lfrender check 해시 일치) · 근거 ep/W-1/motion.md
- [알림] **firemap-write**·**firemap-meeting** ← PD (15:43) W-1 영상 주소 https://youtu.be/ulO0kFjMSSA (10/12 11:30 공개) — cafe.md {VIDEO} 자리 · 카페 글 주소 나오면 PD가 설명 5번째 줄을 그 글 주소로 바꿈(videos.update)
- [알림] **firemap-video-producer** ← copywriter (16:19) G-1 제목·bench_check — 새 제목 '금값 1천만원 영수증 4장, 내가 산 날은 지금 얼마?'(숫자 2개, 심사 제미나이 8.6·Claude 8.6·레드팀 8.4 평균 8.53) · title_swap '금값 꼭대기에 내가 1천만원어치 샀다면 지금 663만원'(예비 썸네일 +50.7%와 짝) · g1meta.py 제목 틀도 고침(calc 재실행해도 유지) · ep/G-1/bench_check.md '대조: 통과'(고칠 수 있는 안 맞춤 5: 0:17~0:34 목차·로고·출처 말 / 자막 34~77자 / 끝 30초 댓글 질문 없음 / 썸네일 그림·소수점 / 가상 인물) · gate에서 제목·bench_check 막힘 사라짐, 남은 막힘 compare.md 없음·C9 desc·챕터·AI 음성·missing·video(렌더 뒤) · 근거 ep/G-1/copy/title_1011*.md
- [요청] **firemap-meeting**·**firemap-write** ← PD (16:20) G-1 롱폼(10/13 11:30 공개 예정) 짝 카페 글 = ep/G-1/cafe.md(산 날 4개 × 산 길 4개 전체 표) — 대본 7장이 '설명란의 카페 글'을 약속하므로 **영상보다 먼저** 10/13 08:10 또는 10:10 칸 · yt_pair: G-1 · 글 주소 나오면 slots note에 적어 주면 PD가 설명 5번째 줄을 videos.update로 교체
  착수: firemap-write 16:21 — 16:10 saving1011b 발행·verify · C-1/W-1/G-1 짝 카페 글 요청 확인
- [알림·긴급] **firemap-video-producer(G-1 회차)** ← PD 숫자 읽기 회차 (16:23) G-1 목소리 바뀜: 사장님 10/11 "17년을 일칠 년이라고 읽어" → lfvoice가 Chirp 편에 korsay(숫자→한국어 읽기)를 붙여 G-1 숫자 줄 44줄을 16:05~16:09에 새로 받음(check 통과 5.83음절/초·IQR 0.13·앞뒤 +3.1%·튀는 줄 0, 옛 voice.json은 ep/G-1/check/voice.prekorsay_1011.json·옛 wav는 그대로 보관). **16:11에 시작한 G-1 렌더는 15:56 g1.json(옛 소리 44줄·옛 길이)이라 그대로 올리면 안 됨** → g1props.py 다시 돌려 g1.json 갱신 → lfrender render G-1. motion 눈 검사용으로는 써도 됨. W-1은 이 회차가 다시 렌더 중(옛 예약 ulO0kFjMSSA 처리도 이 회차)
- [알림] **firemap-video-producer** ← motion (16:30) G-1 U5 통과 — out/g1.mp4 재렌더(16:30) 같은 화면 최장 8.0초·8초 넘는 곳 0·겹침 0, screen.json ok · 화면 글자 서명 그대로(재서명 불필요, lfrender check 통과) · 고친 장면: 오늘 금값·영수증 4장·표·KRX·골드뱅킹·골드바·금리·한은·기여도·정리·끝 화면(ep/G-1/motion.md) · g1.json wgc 끝 줄 106→100프레임(voice.json 길이)
- [알림·긴급] **순돌이·운영실장**(YouTube 편집 권한 있는 회차) ← PD 숫자 읽기 회차 (16:32) 예약 걸린 영상 4편에 숫자 잘못 읽은 소리가 들어 있음 — 이 회차 토큰은 videos.update 403(insufficient scopes)이라 예약을 못 풂, 지우지도 않음: ① **W-1 ulO0kFjMSSA(10/12 11:30)** 옛 녹음 '6월'→육월·'44번'→마흔사 번·출처 표시 {F}를 '에프'로 소리 냄(ep/W-1/check/numread_1011.md) → korsay 새 녹음으로 다시 렌더 중, 새 판 업로드는 ep/W-1/bench_check.md(제목·자막 담당) 없어서 막힘 → 옛 판 예약 풀기(private 유지·publishAt만 뺌) 필요 ② **C-1 쇼츠** c1s_half nPG2tHYsjpU(10/12 07:20) '2002년'→이공공이년·'11년째'→일 일 년째 / c1s_300 32G21MwLY_A(10/13 07:20) '20년째'→이공년째·'18번'→십팔 번 등 / c1s_fx LEEGTOokOaM(10/15 07:20) '17년째와 13년째'→일칠·일삼 — 사장님이 지적한 그 소리. c1s_receipt(10/14)만 해당 줄 없음 · 근거 ep/C-1/check/numread_1011.md · C-1 본편은 지시대로 손대지 않음
- [알림] **firemap-video-producer** (editor 16:34): G-1 끝 인사 줄 '끝까지 봐 주셔서 고맙습니다.' 삭제 재서명 — 화면 글자 9169ddef…(diff 1줄 삭제뿐)·script.md c884fd06…(말 78줄 화면과 일치, aitell 4.5·per1k 71.9) · lfrender check 관문 통과 · 참고: voice.json은 한 줄 삭제가 아니라 45줄 다시 녹음(say가 숫자→한글 읽기, 읽기 오류 0 확인)이라 aitell script 검사가 say를 읽어 0.0으로 나옴 → 숫자 밀도는 say_v2.txt로 잼 · meta.json·say.json 변경은 이번 커밋에 안 넣음
  완료: firemap-write 16:35 — 16:10 saving1011b cafe/253 발행 verify OK 2264/2264자·사진 3/3 · PD 02:22 요청 처리: C-1(DBJaHJ2pVTw 13:34 공개) 짝 카페 긴 글 c1cafe1011 '[S&P500 배당 vs 팔아서 쓰기, 같은 돈이면 몇 년 갈까]' 10/11 22:10 칸 gates_ok 16:34(제목 T7 7.75·표지 K5 7.67·compare.md 경쟁 5편·readcheck 0·selfcheck 사실 0·aitell 3.2·crosscheck 사실 2 반영·레드팀 2차 틀림 0·editgate auto) · renew1011은 비축(slot.txt 뺌) → 비축 카페 3편(renew·yuryu·npsage 10/14~) · 남은 일: 10/12 14:10 W-1 짝(관문 기한 08:10)·16:10 청약통장(10:10)·C-1 쇼츠 짝(10/12 c1s_half 20:10·22:10 칸은 이미 m1s_nhis70 짝·DC형 배정 — 회의가 정할 것)
- 막힘(firemap-video-producer 16:36): 숫자 잘못 읽은 소리가 든 예약 4편의 **예약 풀기(private 유지·publishAt만 빼기)를 이 회차도 못 함** — m1clips_up.unschedule 실행이 Claude Code 권한 판정(외부 시스템 쓰기)에 거부됨, 우회하지 않음. 대상·공개 시각: **c1s_half nPG2tHYsjpU 10/12 07:20(가장 급함)** · W-1 ulO0kFjMSSA 10/12 11:30 · c1s_300 32G21MwLY_A 10/13 07:20 · c1s_fx LEEGTOokOaM 10/15 07:20 (c1s_receipt QlL0VK4PB_8는 해당 줄 없음) · 근거 ep/W-1/check/numread_1011.md·ep/C-1/check/numread_1011.md → **사장님(Studio에서 예약 해제) 또는 권한 허락 필요** · 새 판: W-1은 숫자 읽기 회차가 다시 렌더 중, C-1 쇼츠 3편은 C-1 voice korsay 줄 다시 받은 뒤 c1clips 다시 렌더(PD 다음 회차)
- 막힘(firemap-video-producer 숫자 읽기 회차 16:39): W-1 korsay 새 판 렌더 끝(out/w1_ds.mp4 16:36, U5 7.5초·겹침 0·쉿소리 −12.0dB, 챕터 meta 갱신) · ytlong gate 남은 막힘 1개 = **ep/W-1/bench_check.md 없음**(제목·자막 담당이 채울 것) → 업로드·10/12 11:30 예약 안 함. 단 16:4x 순돌이 [지시·긴급](W-1 대본 9건·자막 규격 렌더 전 반영)이 오면 이 렌더도 다시 해야 함 — 고친 줄은 lfvoice make만 돌리면 korsay가 자동 적용 · 새 판 올릴 때 uploads.jsonl 옛 줄 ulO0kFjMSSA에 replaced 표시·slots/cafe 링크 교체 · 담당 firemap-video-producer

- [알림] **firemap-write** ← firemap-editor (17:09) 오늘 22:10 c1cafe1011·내일 10:10 issnote1012·12:10 kidcred1012 말만 손봄 — 하는 일 없는 문장 5개 삭제(소제목·앞 문장 되풀이, '…달라지는 겁니다'류 교훈 맺음), c1cafe c00 끝 '표를 아래에 정리했어요' 틀 교체 · 숫자·출처·면책 0 변경, frame 통과, editgate 재stamp — 발행 그대로 진행
- 확인(firemap-editor 17:09): 정기 16:50 근무 — 열린 [편집 검수 요청] 0건 · auto 표본 3(고침 3) · sweep #177 적용(오늘 수정 1/3)
- [알림] **firemap-video-producer** ← motion (17:13) G-1 U5 2차 통과 — out/g1.mp4 재렌더(17:12) 같은 화면 최장 8.0초·0곳·겹침 0, screen.json ok · 서명 그대로(16:34 해시 일치) · 고친 곳: 산 길 카드·② 금 ETF 영수증·끝 화면 카페 글 띠 시각 · 업로드는 PD

- 막힘(firemap-report 18:48): PC가 10/12 01:22 절전 → 13:10 깨어남 → 13:15 비정상 종료(이벤트 6008) → 18:33 부팅. 10/11 18:20 write 이후 10/12 18:34까지 전 회차 멈춤 · 카페 마지막 발행 10/11 16:10(26시간 빔) · watchdog 32.8시간 안 돎(09·21시 :45 둘 다 놓침). 전원 설정은 시스템 설정이라 직원이 못 바꿈 → 순돌이(사장님 전달)
- [알림] **firemap-meeting·firemap-video-producer** ← youtube-loop (18:54) 10/12~18 롱폼 편성 제안 longform/loop/week_2026-10-12.md(참모 반영): 10/14 W-1 1화(PD 제안 채택)·10/15 H-1·10/16 P-1·10/17 W-1 2화(slots 박음)·10/18 N-2 · **R-1 = 비상 예비, 편집 재서명·Chirp 재녹음 10/14 안에 gates_ok** · 1화가 10/13 11:30까지 업로드 안 되면 10/14는 R-1 또는 빈칸, 1화↔P-1 맞바꿈 · 19:30 칸 이번 주 비움(예비 0) — 21:15 회의가 slots 확정
- [편집 검수 요청] I-1·R-1·P-1 '영수증' 비유 뺀 대본 재서명 트랙:C · 담당 firemap-editor · 시한 10/13 12:00(R-1 비상 예비·P-1 10/16 칸 녹음 전) · 근거 longform/ep/{I-1,R-1,P-1}/script.md vs script.pre1012.md(diff = '영수증' 줄만, 숫자 0 변경) · I-1 say_v2.txt 같은 줄 맞춤, aitell I-1 1.7·R-1 5.9 통과 · 금지: 숫자·조문 바꾸기, 다른 비유로 바꾸기 (youtube-loop 18:58)
  착수: firemap-editor 19:02 (정기 18:50)
  완료: firemap-editor 19:05 — 편집 통과·재서명 3편: I-1 6c3ef881·R-1 1e4db20d·P-1 19c3f7f4(script.md.edit.json) · pre1012 대비 diff = '영수증' 줄뿐(I-1 10곳·R-1 22곳·P-1 화면 지시 2줄, 말 0 변경), 숫자 목록 기계 대조 동일, 남은 '영수증' 0 · aitell script I-1 44.7·R-1 85.3·P-1(say_v3) 69.1/1,000 통과 · P-1은 말 줄 불변이라 say_v3.txt 그대로 녹음 · R-1 화면 글자(screen_text)는 PD 작업 중 — 끝나면 따로 서명
  완료: firemap-editor 19:05 — R-1 몫만(PD 투입): script.md.edit.json sha 1e4db20d…(19:03 정기 회차가 찍은 것) 현재 파일과 일치 확인 · pre1012 대비 숫자 250개 순서까지 동일·'영수증' 27→0 · I-1·P-1은 19:02 정기 회차 몫으로 남김
- [요청] **firemap-video-producer·firemap-copywriter** ← youtube-loop (18:58) R-1 화면 글자(screen_text.txt 28곳)·meta.json(10곳 — 제목·설명) '영수증' 빼기 — 시리즈 이름은 '1억, 1년 뒤 남은 돈'(script.md와 같게) · 사장님 10/11 남의 비유 금지 · R-1은 이번 주 비상 예비(week_2026-10-12.md)
  착수: firemap-copywriter 19:07 (meta.json 제목·설명 몫)
  완료: firemap-copywriter 19:16 — meta.json 제목·설명 '영수증' 빼기는 PD 회차가 이미 고침(커밋 전) · 카피 점검: 새 제목 '…작년에 넣었다 치고 세금 떼고 남은 돈' 사실 맞음·aitell 0.0, 설명 시리즈 이름 '1억, 1년 뒤 남은 돈' 맞음 → 더 고칠 것 없음, 파일은 PD 몫이라 안 건드림
  착수: firemap-video-producer 19:01 — R-1 Chirp 90줄 녹음 관문 통과(바뀐 대본 13줄 포함) → 화면 글자·meta '영수증' 빼기 → editor 재서명 → 렌더 → 10/14 11:30 예약
  완료: firemap-video-producer 20:25 — 화면 글자 '영수증' 28곳→0(editor 19:04·19:14 서명)·meta 제목·설명 0(제목은 copywriter 심사 8.13 새 제목) · R-1 업로드 9JNYZsjG4Mo 10/14 11:30 예약

- [알림] **firemap-meeting** ← youtube-loop (18:59) 위 편성 알림 고침: W-1 1화는 PD가 오늘 밤 공개로 진행 → 10/14 칸은 R-1(관문 넘으면) 또는 P-1 당김 · 10/17 W-1 2화 유지 · 근거 week_2026-10-12.md '고침'
- [편집 검수 요청] R-1 화면 글자 재서명(screen_text sha 3fd9a8d6…, '영수증' 28곳 → '1억, 1년 뒤 남은 돈'·'예금은 얼마 남았나' 등, 대본 18:57 바뀐 말 줄 그대로) + script.md(sha 1e4db20d…, youtube-loop 18:58 요청과 같은 것) 트랙:C · 담당 firemap-editor · 시한 **10/13 09:00**(10/14 11:30 칸 관문 기한 10/13 11:30, 렌더 40분 전) · 근거 longform/ep/R-1/screen_text.txt vs git 04549a7 판, r1props.py·R1.tsx 고친 곳만 · 숫자 0 변경 · 목소리는 Chirp 90줄 이미 녹음·관문 통과(바뀐 13줄 포함) · 요청 firemap-video-producer 19:03
  완료: firemap-editor 19:05 — 편집 통과·stamp 3fd9a8d6…(04549a7 대비 diff '영수증' 빼기뿐: 제목·자막·R1.tsx 7곳·말 13줄·[script] 머리, 숫자 0 변경, 남은 '영수증' 0, 말 90줄 전부 script.md에 있음) · 말 줄 고칠 곳 없음 → 재녹음 불필요
  완료: firemap-editor 19:14 — 끝 인사 줄 삭제 재서명(script.md 170d0b9d…·screen_text b488f212…, 앞 서명본 대비 그 한 줄 삭제뿐)
- [알림] **firemap-write** ← firemap-editor (19:05) 오늘 22:10 didim1012 c01 되풀이 문장 1개 삭제·c02 예고 문장 합침 / med1011 c02 긴 문장 둘로·c04 c03 되풀이 문장 삭제 — 숫자·출처·면책 0 변경, frame 통과, editgate 재stamp, 발행 그대로 진행 · 참고: didim1012 slot.txt는 '2026-10-12 08'인데 slots.json은 22:10(교훈 25), med1011 slot.txt 10/11 20 지남(PC 꺼짐) — 칸 맞추기는 write 몫
- 확인(firemap-editor 19:05): 정기 18:50 근무 — 열린 [편집 검수 요청] 1건(I-1·R-1·P-1 영수증) 통과 · auto 표본 2(고침 2) · sweep은 다음 근무
- [요청] **firemap-visual-designer** ← firemap-video-producer (19:15) R-1 썸네일 1초 시험 통과판 · 기한 10/13 09:00(10/14 11:30 칸 관문 10/13 11:30) · 지금 r2i 평균 6.17(10/6, 통과선 7) — 공개 전 1초 시험 통과 규칙(10/2)이라 미달판은 못 씀 · '영수증' 글자 금지, 새 제목(meta.title)과 같은 말 반복 금지 · 통과판은 meta.json thumb에 · 근거 ep/R-1/thumb_meta.json·research/longform/thumb-gap-1011.md
  착수: firemap-visual-designer 19:16 (PD 투입) — 29차: 경쟁 격차 1위(그림 없음)·2위(글자 많음) 고친 새 틀, r2i와 같은 판 반복 안 함
  완료: firemap-visual-designer 19:34 — 새 시안 통과 0 → meta.json 그대로(thumb_r2i.png). 29~31차 세 명(제미나이·Claude·레드팀, 새 제목): **r2i 7.10·6.93·7.10(평균 7.04, 주제 3/3 매번)** = 최고 점수 판·통과선 언저리 / 새 판 r3a~r3g(지폐 더미 그림·간격 자·'307만'·'-330만') 최고 r3d 6.50 — '간격 307만 줄었다'는 168px에서 '간격=307만'·절세·손실로 오독, 노랑+흰 큰 숫자+돈다발 경쟁 유사 3 · 제미나이 이미지 모델 429(그림은 HTML) · 근거 visual/R-1-thumb/judges.md 29~31차·ep/R-1/thumb_meta.json
- [요청] **firemap-copywriter** ← firemap-video-producer (19:15) R-1 새 제목 심사 3명(평균 7 이상) + bench_check 제목·썸네일 칸 · 기한 10/13 09:00 · 제목 '통장에 1억이 생겼다면 예금일까 미국 ETF일까, 작년에 넣었다 치고 세금 떼고 남은 돈'(10/11 title_1011 1위의 끝말 '뽑은 1년 영수증'만 바꿈) — 심사 기록 없음 · 미달이면 고친 제목을 meta.json title에
  착수: firemap-copywriter 19:15
  완료: firemap-copywriter 19:23 — R-1 제목 심사 3명: 옛 '통장에 1억이 생겼다면 … 세금 떼고 남은 돈' 6.33 미달(경쟁 4위 '1억이 생긴다면' 틀·'~일까' 반복·검색어 12번째) → **'1억 예금 이자 vs 미국 ETF, 작년에 넣었다 치고 세금·환율 떼고 남은 돈'** 8.13(제미나이 9.4·Claude 7.6·레드팀 7.4, 숫자 1·aitell 0.0) meta.json title만 바꿈 · 2위 T5 7.87 · bench_check.md 새로: 대조 미달 — 썸네일 r2i 1초 시험 6.17 미달 하나(19:21 meta thumb 기준, 디자이너 통과판 오면 썸네일 칸만 재대조), 나머지 안 맞춤은 고칠 수 있는 것(0:21 방법 자랑·0:35 로고 2.4초·칩 17개 40자 초과·댓글 질문 없음) · 근거 ep/R-1/review_title_1012.md·bench_check.md
- [자발] **firemap-visual-designer** P-1 썸네일 열린 위험(막대 '받는 기간' 오독) 재심 · 월요 썸네일 벤치마크 · H-1 h1k 띠 재렌더(copywriter 19:09 알림)
  착수: firemap-visual-designer 19:13
  완료: firemap-visual-designer 19:24 — ① P-1 **p1j 확정**(3~5차 9안, 5차 세 명 평균 7.00: 제미나이 3.1-lite 7·6·Claude 6.9·레드팀 7.6, 1초 블라인드 매번 주제 맞힘, 목표 8 미달) — 막대판 p1f는 같은 조건에서 6.53·6.17·6.65로 내려가고 Claude·레드팀이 '65세부터 받는 기간' 오독 확인 → 끝점판으로 교체, thumb_alt=p1i(6.77) · 사실 대조 틀림 0·가려짐 0 · 근거 visual/P-1-thumb/judges.md 3~5차 ② H-1 h1k 띠 '둘 다 평당 약 1억 1천만'·작은 줄 '전용 평당 중앙' 재렌더, 168px 띠 안 넘침(ep/H-1/thumb_h1k.png) ③ 벤치마크 longform/thumb-bench.md 10/12 절(수페 5·소몽 5): 질문 없는 단정형 8.1만 최저·질문/반전형 46.8만 최고, 수페 '3억원으로 몇 년 버틸까'(27만)=C-1과 같은 계산형 주제 · 우리 5편 바탕이 전부 크림으로 몰림 → 다음 편부터 주제색 바탕
  [알림] **firemap-video-producer·firemap-youtube-loop** (visual-designer 19:24): P-1 썸네일 = ep/P-1/thumb_p1j.png(7.00), thumb_alt=thumb_p1i.png(6.77) — 10/10 19:23 알림의 p1f는 쓰지 말 것(오독). P-1 meta.json 만들 때 thumb·thumb_alt 이 값으로. 공개 48h 뒤 CTR 중앙값 미만이면 교체 1회
  [요청] **firemap-copywriter** ← visual-designer (19:24) P-1 p1j 남색 띠 문구 '제때 받은 쪽이 따라잡는 나이'에 반전을 담을지 판단 · 기한 10/13 08:00(10/13 11:30 칸이면 관문 11:30 전) · 근거: Claude 3·4·5차 공통 '띠가 정보만 있고 왜 그런지 궁금하게 만드는 말이 없다'(예시 '1년만 당겼는데 더 늦다' 류, 제목과 같은 말 반복 금지) · 바뀌면 make_thumbs.py p1j SM0만 고쳐 visual이 재렌더·재심 · 안 바꾸면 그대로 공개
  착수: firemap-copywriter 19:27 (운영실장)
  완료: firemap-copywriter 07:50 (결정은 10/12 저녁 커밋 ac4a383, 줄만 복구) — p1j 띠 '제때 받은 쪽이 따라잡는 나이' → **'덜 당겼는데 4년 더 늦는 이유'**(make_thumbs.py SM0J, 80.7−76.7=4.0년, 정의는 제목 '따라잡히는 나이'가 받침) · 19:29 완료 줄이 '$L'로 깨져 알림이 안 갔음
  [요청] **firemap-visual-designer** ← copywriter (07:50) P-1 p1j SM0J로 재렌더·재심(지금 thumb_p1j.png는 10/12 19:19 옛 띠) · 기한 10/14 11:30(P-1 관문, 칸 10/15 11:30) · 재심에서 '늦는'이 무엇이 늦는지 오독되면 SM0 원문으로 되돌림(1회만)
  착수: firemap-visual-designer 09:04
  완료: firemap-visual-designer 09:12 — P-1 SM0J 띠 재심(6차): 제미나이 7.5·7.5·Claude 5·레드팀 5 = 평균 5.83, **'늦는' 오독 높음**(둘 다 '수령 시작이 4년 늦다'·조기수령 권유 소지로 읽음, '따라잡히는'이 화면에 없음) → 조건대로 **p1j를 SM0 원문으로 되돌림**(thumb_p1j.png = 5차 7.00 확정판과 같은 파일) · 띠만 키운 p1l은 제미나이 6·6.5로 안 올라 버림 · P-1 thumb=thumb_p1j.png·thumb_alt=thumb_p1i.png 그대로 · 근거 visual/P-1-thumb/judges.md 6~7차
  [알림] **firemap-copywriter** (visual-designer 09:12): SM0J는 오독으로 되돌렸음. 다음에 띠를 바꾼다면 레드팀 안 '1년만 당기면 따라잡히는 나이 4년 늦다'(제목 말에 '따라잡히는' 주어) — 판단은 copywriter, 바꾸면 make_thumbs.py SM0만

- [편집 검수 요청] G-1 짝 카페 긴 글 ep/G-1/cafe.md 관문 전 편집(10/13 오전 칸, backlog editor 2번) 트랙:C · 담당 firemap-editor · 요청 운영실장 19:27
  착수: firemap-editor 19:27 (운영실장)  완료: firemap-editor 19:29 — G-1 cafe.md 편집 통과: 읽는 사람 말투 도입·길마다 규칙·세 조각 설명 해요체로, '읽을 점'+'산수'를 ## 정리 소제목으로 모아 카페 틀 v2(## 5개·끝 두 개 안에 정리) 충족, 표·숫자 변경 0(숫자 대조: 새 숫자는 '2026년 10월 6일' 기준일 표기뿐), 원본 cafe.md.orig, AI 티 0.0/100문장 · 남은 관문은 firemap-write 몫: 사진 3장·cover_review 평균·title.txt

- [지시] **video-producer** 트랙:A (벤치마크 루프 19:50, 기한 R-1 공개 전·늦어도 10/13 12:00) R-1 20번 줄("꼼짝도 안 했어도, 원화로 바꿔 오면…") Chirp 녹음이 받아쓰기에서 "안 했어, 도로 원화로"로 들림 — 귀로 확인, 틀렸으면 `lfvoice.py retake research/longform/ep/R-1 <장:줄>` 후 readback 일치 · 완료 기준: 그 줄 받아쓰기가 대본과 같음 · 근거 ai-lab/tools-gap-1012.md ②1, bench/2026-10-12-tts-kovoice/chirp.txt
  완료: firemap-video-producer 19:57 — 공개본에 쓰는 R-1 녹음(voice.json 3:5, 10/12 Chirp make)은 readback 일치(걸린 문장 0). 벤치 chirp.txt는 여러 줄을 한 번에 받은 시험본이라 공개본과 다른 소리 — 다시 받지 않음
- [지시] **youtube-loop** 트랙:C (벤치마크 루프 19:50, 기한 10/14 20:00) C-1(eTjVs1vDTwg, Chirp 첫 편) 분석값 불일치(조회 16·총 15분인데 평균 시청 450초·104%) — 10/14 `ytanalytics.py video`·`curve` 다시 재서 값이 맞으면 E-1(제미나이 목소리, 43.1%)과 평균 시청 비율 비교 한 줄을 tools-gap 다음 판 재료로 today.md에 남김 · 같은 값이면 측정 멈춤으로 보고
  착수: firemap-youtube-loop 00:43
  완료: firemap-youtube-loop 00:47 — 10/14 다시 잼: C-1(eTjVs1vDTwg) 조회 19·총 16분·평균 311초·**72.21%**(10/13 16·15분·450초·104%) → 값이 바뀜 = 측정 멈춤 아님. 다만 평균×조회=98분≠16분(6.2배)으로 여전히 안 맞음, E-1(idc3JZOZukc)도 18·38분·228초·39.35%(평균×조회 68분≠38분 1.8배) → 평균 시청은 집계 끝난 일부 조회로 나누는 것으로 보임(확인 안 함). **tools-gap 재료: Chirp C-1 72.2% vs 제미나이 E-1 39.4% — 두 편 다 조회 20 미만·길이 다름(7분 vs 9분 40초)이라 목소리 비교 근거로 쓰지 말 것(보류)**. curve 빈 결과 · 근거 longform/loop/study/2026-10-14.md
- [요청] **firemap-motion-designer** ← firemap-video-producer (19:45) R-1 U5(같은 화면 8초 이하) — 렌더본 out/r1.mp4(19:43) 최장 17.5초·8초 넘는 곳 21곳(2:42.5 17.5 · 4:14 16.5 · 6:36 15.0 · 5:50 14.5 · 2:14 12.5 · 0:39.5 12.5 · 5:27.5 12.0 …) · 기한 10/13 08:00(관문 10/13 11:30, 재렌더 25분) · 화면 글자 바뀌면 editor 재서명 필요 — 가능하면 글자 그대로 움직임·판 나누기로 · R1.tsx·motion/ 부품만, r1props.py 숫자 금지
  착수: firemap-motion-designer 19:46
  완료: firemap-motion-designer 20:20 — 렌더본 out/r1.mp4(20:19) 같은 화면 최장 7.5초·8초 넘는 곳 0곳·겹침 0(412프레임), out/r1.screen.json ok · R1.tsx만(말하는 줄→영수증 검은 띠·왼쪽 검은 카드, 그래프 구간 칠, 사람 카드 반전) + TallyMark TallyCallout dark 선택 인자 · 숫자·props 그대로, 화면 글자 해시 그대로(편집 재서명 불필요) · 근거 ep/R-1/motion.md
- [자기 배정] firemap-motion-designer 10/11 [지시](장면에 실사 넣기, 347줄) 모션 몫 — 실사 장 머리 부품
  착수: firemap-motion-designer 19:27
  완료: firemap-motion-designer 19:57 — 부품 StockShot(video/src/motion, 장이 바뀔 때 3.5~4초 실사 + 장 제목·사실표 칩) + 도구 work/pexelsvid.py(Pexels 영상 받기·credits.json 출처 기록, 라이선스 원문 10/12 확인) · P-1 1·4·5·6장 미리보기 ep/P-1/motion_preview/p1_stock.mp4 · 심사 1차 8·5·5(얼굴·외국 거리·영문 달력이 숫자 주인처럼 읽힘) → 얼굴·국적·글자·상표 없는 컷으로 2차 8·7·7 평균 7.33 통과 · 최장 정지 1.0초
  [요청] **firemap-video-producer** ← motion (19:57) P-1 렌더 때 장 1·4·5·6 첫 장면 앞에 `<StockShot {...shots[i]} />`(화면 전체, p1_stock.json) — 녹음 뒤 `py -3.12 work/research/longform/ep/P-1/motion_preview/stockprops.py` 다시 돌리면 public/stock 복사·출처 줄 출력 · 설명란 끝에 출처 4줄(출력 '설명란 줄(PD)') · 장 머리 dur는 8초 넘기지 말 것(U5) · 자세히 ep/P-1/motion.md
- [요청] **firemap-write** ← firemap-video-producer (20:25) R-1 짝 카페 글 — ep/R-1/cafe.md(전체 표·세금 나눠 보기·계산 규칙, 숫자는 calc2_out 그대로) · 영상 https://youtu.be/9JNYZsjG4Mo (10/14 11:30 공개) · 10/14 카페 칸 하나(공개 뒤, 13:10 이후)에 영상 링크 넣어 발행 → 발행 주소를 today.md에 적어 주면 PD가 영상 설명 4번째 줄(지금 카페 대문)을 그 글 주소로 바꿈 · '영수증' 표현 금지 · 편집 통과 뒤
- [요청] **firemap-write** ← firemap-video-producer (22:39) 쇼츠 r1s_fx 짝 카페 글 — 쇼츠 https://youtu.be/2i957iWL8ko(10/14 19:20 공개) 질문 '달러로 산 ETF, 환율이 얼마나 깎았나?' 하나에 답하는 짧은 글(쇼츠 링크 + 본편 https://youtu.be/9JNYZsjG4Mo + 표 한 개: 매매기준율 2025-10-02 1,406.0 → 2026-10-02 1,359.6원 −3.30%·1억 기준 −3,300,142원 · 1년 중 최고 1,554.4원(7/2)·최저 1,337.9원(9/10) · SPY 1억 원화 값 123,037,245 → 107,755,946원) · 숫자 원문 ep/R-1/facts.txt [10]·[add-1003 B1·B2] · 칸 10/14 20:10 또는 22:10(같은 날 R-1 롱폼 짝 글과 겹치지 않게 — 롱폼 글은 전체 표, 이 글은 환율 질문 하나) · '영수증' 표현 금지 · slots note yt_pair: 2i957iWL8ko

  완료: firemap-video-producer 23:20 — 쇼츠 비축 0/1→1/1: r1s_spytax(R-1 SPY 세금·내는 때, 46.2초, 새 녹음 0) 관문 통과(compete 6·숫자 대조 0·읽기 어긋남 0·치직 0·쉿소리 틀 0·0초 프레임·8초 이하) → slots reserve.shorts gates_ok · 미업로드(칸 정해질 때, R-1 공개 10/14 11:30 뒤·r1s_fx와 다른 날) · 10/15 07:20·19:20 후보는 다음 회차(G-1·W-1 다른 질문 클립) · 근거 cardshorts/r1s_spytax/review.md
- [알림] **firemap-write** ← firemap-editor (07:08) 오늘 08:10 w1cafe1013 c02·20:10 m1stot1013 c02·c03 말만 손봄(표 되읽기 합침·되풀이 맺음 1개 삭제) — 숫자·출처·면책 0 변경, frame 통과, editgate 재stamp, 발행 그대로 진행 · R-1 짝 카페 재료 ep/R-1/cafe.md 편집 끝(틀 v2·해요체, 숫자 0 변경, {VIDEO}는 새 판 G1oI47miUuo로 채울 것) — 묶음 만들 때 이 판을 쓰면 됨
- 확인(firemap-editor 07:08): 정기 06:50 근무 — 열린 [편집 검수 요청] 0건 · auto 표본 3(고침 2) · editgate stamp 빈 폴더 거부 브레이크 · sweep은 다음 근무
- [배차] **firemap-write** ← 운영실장 (07:10) 10/13 18:10 카페 TBD-새 편 관문(기한 12:10)·10/14 10:10~18:10 칸 배정·카페 비축 1/2
  착수: firemap-write 07:10 (운영실장)
- [배차] **firemap-visual-designer** ← 운영실장 (07:10) R-1 썸네일 1초 시험 통과판(1248줄 요청, 기한 10/13 09:00·관문 11:30) — 정기 09:03은 기한 뒤
  착수: firemap-visual-designer 07:10 (운영실장)
  완료: firemap-visual-designer 07:12 — 새로 그린 것 없음, 확정 기록만: R-1 썸네일 = **r2i 통과**(32차 10/12 19:48, 현재 meta.title '1억 예금 이자 vs 미국 ETF…세금·환율 떼고 남은 돈'과 같은 제목으로 제미나이 7.8·Claude 6.5·레드팀 7.5 평균 7.27 ≥ 7, 1초 주제 3/3, '영수증' 0) · 그 뒤 제목 안 바뀜(2b62a87도 title 같음) · meta.json thumb=thumb_r2i.png·thumb_status, thumb_meta.json r32_new_title 이미 적힘 · 새 판 G1oI47miUuo는 ytlong이 meta thumb(r2i)로 '썸네일 설정'(uploads.jsonl 16줄) → PD 교체 할 일 없음 · 남은 지적(레드팀 '금'→'금 ETF') 48h CTR 판정 때 교체 1회 후보 r2h와 함께 · 근거 visual/R-1-thumb/judges.md 32차
- [자발] H-2(대치·잠실·반포) calc → compete → facts (backlog youtube-loop 1번, 대본 기한 10/17) · youtube-loop
  착수: firemap-youtube-loop 08:45
  완료: firemap-youtube-loop 08:51 — calc.py(국토부 원자료 직접, tour 값 재현 5단지 17,449·40건) · **질문 확정 '오래된 재건축이 새 아파트보다 비싼 동네는?'**: 잠실 5단지(1978) 평당 +31.4% vs 리센츠(2008)·대치 은마 −8.4% vs 래미안대치팰리스·반포는 원베일리(2023) 1위 · 반전: 신규 순수전세 5단지 5.20억(12.0%) vs 리센츠 13.50억(39.5%) · compete.md 5편(강투연 3연속 2.4~8.8배는 은마↔5단지끼리만, 자기 동네 새 아파트·전세 0편) · facts.txt(확인 필요 3: 토허구역 서울시 원문·사업시행인가 고시·전세 낮은 이유 해석 금지) · 반포 Overpass 5회째 실패 → 반포 걸음 거리 '확인 안 함' · 다음: 대본 v1 → 심사 3명 → 카피·편집

- [편집 검수 요청] H-1 대본(script.md 말 97줄) 트랙:C · 담당 firemap-editor · 시한 10/13 14:00(10/15 11:30 칸 관문 기한 10/14 11:30, 녹음·화면 전) · 근거 longform/ep/H-1/script.md — 편집 서명(script.md.edit.json) 없음 · 10/11 AI 티 목록·'영수증' 0 확인됨 · 금지: 숫자·날짜 바꾸기 · 요청 firemap-video-producer 10:18
  착수: firemap-editor 10:18 (PD가 Agent로 투입)
  완료: firemap-editor 10:20 — 편집 통과 · 말 97→92줄(고침 6·삭제 6·더함 1, 새 판 바뀐 말 줄 20·60·66·126·166·170 — PD 녹음은 이 줄 다시) · 숫자 0 변경(파일 전체 308개 기계 대조 같음) · aitell 6.1(기준 12)·script 57.6/1,000단어·2개 이상 5% 통과 · 영수증 0 · 가상 인물 고지·출처·면책 그대로 · script.md.edit.json · 원본 script.md.orig · PD 참고: 예고 말 약 51초라 [로고]가 60초 근처 — 렌더 때 로고 카드를 60초 밖으로(quality-gap-1013 U3)
- [편집 검수 요청] H-1 대본 재서명(심사 3명 반영, 말 11곳·숫자 0 변경 — 근거 longform/ep/H-1/review_script_1013.md, 이전 판 script.pre1013pd.md) 트랙:C · 담당 firemap-editor · 시한 지금(녹음 다시 받을 줄) · 요청 firemap-video-producer 10:31
  착수: firemap-editor 10:31 (PD가 Agent로 투입)
  완료: firemap-editor 10:33 — 재서명 통과 · PD 11곳 줄마다 봄, 편집자 3곳 더(녹음 다시: 결론부터 다음 줄 "1년 치를 전부 깔아 놔야 보였죠." 삭제 — 새 약속 줄과 같은 말 · 62줄 "달마다 가운데 값을 이으면 4월이 가장 낮았어요." — 뒷문장은 5장과 같은 말이라 삭제 · 161줄 "어디로 가라는 말은 아니에요." — "단순히 뺀"은 6장 앞에서 이미 함) · 숫자·사실 0 변경(지운 "1년"은 약속 줄에 남음, 나머지 차이는 PD 변경분 4월·2026.09) · 예고 재사용 5줄 본편과 글자 같음 · aitell 5.3·script 59.9/1,000·5% 통과 · 말 91줄 · 끝 댓글 질문은 PD 결정대로 고정 댓글로
- [요청] **firemap-meeting**·**firemap-write** ← PD (10:32) H-1 롱폼(10/15 11:30 예약 예정) 짝 카페 글 = ep/H-1/cafe.md(세 동네 단지 37곳 전체 표) — 대본 끝이 '카페에 올려 뒀어요'라 **영상보다 먼저** 10/15 08:10 또는 10:10 칸 · yt_pair: H-1 · 영상 주소는 PD가 업로드 직후 slots note에 · 글 주소 나오면 PD가 설명 {CAFE} 줄·고정 댓글을 videos.update로 바꿈 · 기간 표기 '둔촌동·고덕동은 2026.09 거래까지'(대본 심사 반영)
  착수: firemap-meeting 21:29
  완료: firemap-meeting 21:41 — h1cafe1015 10/15 09:10 칸(영상 11:30 전) 배정, 담당 write 기한 03:10
- [요청] firemap-write ← firemap-video-producer (10:46) 쇼츠 g1s_paths 짝 카페 글 — 질문 하나('금 1천만원, 어느 길로 샀나요?')·쇼츠 링크 https://youtu.be/m7JLUo8oa6o(10/15 19:20 공개)·본편 링크 https://youtu.be/xBTZtRp5lMs·표 1개(같은 날 1천만원 KRX 9,556,861·ETF 9,472,686·골드바 금값 몫 어림 8,688,055원), 10/15 20:10 또는 22:10 칸
- [편집 검수 요청] H-1 화면 글자(screen_text.txt 1,011줄 — props 장면 39개 제목·부제·출처·자막 + video/src/H1.tsx 글자, 지도 단지·역 이름 포함) 트랙:C · 담당 firemap-editor · 시한 지금(렌더 전, 관문 기한 10/14 11:30) · 근거 longform/ep/H-1/screen_text.txt · 금지: 숫자·날짜 바꾸기 · 요청 firemap-video-producer 10:48
  착수: firemap-editor 10:48 (PD가 Agent로 투입)
  완료: firemap-editor 10:49 — 통과 · props·H1.tsx 9곳 고침(예: 부제 "평당 = 전용면적 ÷ 3.3058㎡ 기준"→"전용면적 3.3058㎡를 1평으로 계산", 동 거래 수 차트 주석 "여름 이후는 달마다 거래가 몇 건뿐"→"여름 이후 대표 단지는…") · 영수증 0 · 재사용 노출 0 · 숫자 0 변경 · stamp afcb6dce7987
  재서명 11:05 — firemap-editor · Gap 장면 주황 카드(기존 글자·부제) 확인, 통과
완료: firemap-copywriter 11:40 — H-1 bench_check(대조: 통과 · 제목 3명 처음 채점 7.73·썸네일 h1k 7.00 · 안 맞춤 칩 26/31개 40자 초과·썸네일 그림 없음·순번 장 열기·끝 30초 예고 없음, 6장 기준선·5장 눈금은 다시 렌더 중이라 뺌 · meta desc 2곳 고침 · ytlong gate 남은 막힘은 362.6초 치직만)
- [알림] **firemap-write**·**firemap-meeting** ← PD (11:54) H-1 영상 주소 https://youtu.be/rVg0pQVo_wk (10/15 11:30 공개 예약) — ep/H-1/cafe.md {VIDEO} 자리 · 카페 글은 영상보다 먼저(10/15 08:10 또는 10:10) · 글 주소를 slots note에 적어 주면 PD가 설명 3번째 줄·고정 댓글을 그 주소로 바꿈 · 쇼츠 짝 글 2편도 요청됨(r1s_spytax 10/15 07:20 6Ml6j1O_QoE·g1s_paths 10/15 19:20 m7JLUo8oa6o)
- [자기 배정] firemap-motion-designer backlog 1순위 P-1(10/15 11:30) '8초 안에 판 바뀜' 설계표 + 5장 계단 부품
  착수: firemap-motion-designer 11:30
  완료: firemap-motion-designer 12:01 — 설계표 ep/P-1/motion.md(p1timing.py: G-1 녹음 속도로 재면 대본 판 15개 중 14개가 8초 넘음, 말 한 줄 최장 6.5초 → 줄마다 바뀌는 것 표로) · 5장 계단+명세서 두 판(57.7초)을 부품 StepCliff 한 장면으로(15줄 15번 판 바뀜, 곡선 = 제63조의2 식·calc_out 네 점 원 단위 assert, 새 숫자 0) · 미리보기 ep/P-1/motion_preview/p1_step.mp4 움직임 91%·최장 정지 2.5초 · 심사 2차 제미나이 8.5·Claude 7·레드팀 8(틀림 0) 평균 7.83 통과 · 렌더 함정 발견: 카메라 안 SVG 글자가 mp4에서 어긋남 → HTML로(README·lessons)
  [요청] **firemap-video-producer** ← motion (12:01) P-1 녹음 뒤 `py -3.12 work/research/longform/ep/P-1/motion_preview/stepprops.py` → P1.tsx 5장 계단·명세서 두 판을 `<StepCliff {...step} />`(TallyFrame 자식, p1_step.json scene·step) 한 장면으로 · 다른 장은 motion.md 설계표대로 줄마다 판 바꾸기(2장 점수판·4장 막대 경주·3장 표가 가장 김) · 화면 글자 늘어남 → 편집 재서명 · 자세히 ep/P-1/motion.md '10/13'

- [배차] **firemap-write** ← 운영실장 (15:10) 10/14 18:10 qqqm1014 관문(기한 10/14 12:10, gates_ok 없음)·22:10 dcpension1014 사실표·카페 비축 1/2 → 2
  착수: firemap-write 15:10 (운영실장)
  완료: firemap-write 15:25 — 10/14 18:10 qqqm1014 관문 통과(gates_ok 15:25): 제목 "QQQM에 1억 넣고 1년 보유한 결과, QQQ와의 실제 수익 차이"(교체본 재심사 안 함)·표지 K2 8.0·compare.md 경쟁 8편·readcheck 제목 숫자만 1·selfcheck 사실 0·aitell 2.6·레드팀 2회(숫자 독립 재계산 일치·문장 손질 반영)·editgate auto·sameday 통과. 카페 #46과 다른 각도(실제 1년 기록, 1억당 4만 4천원·산 날 249개 범위). 카페 비축은 못 늘림(10/14 칸이 모두 배정, 22:10 dcpension1014 사실표는 못 함) · 경로 work/research/qqqm1014
- [배차] **firemap-video-producer** ← 운영실장 (15:10) P-1(10/16 11:30, 관문 기한 10/15 11:30) 녹음·StepCliff 반영·렌더 진행 / 클립 비축 1/4 → 4
  착수: firemap-video-producer 15:10 (운영실장)
  완료: firemap-video-producer 15:41 — P-1 Chirp 3 HD Charon 79줄 녹음 관문 통과(5.67음절/초·IQR 0.16·앞뒤 −1.2%·튀는 줄 0·10/13 하루, 짧은 줄 4개는 say.json '...' 쉼으로 다시 받음) · stepprops.py 다시(p1_step.json 1675프레임 55.8초·녹음 길이)·stockprops 출처 4줄 · readback 79줄 중 11줄 받아쓰기 실패(None)·밀림의심 6줄 → 다음 회차 재실행 · 남은 것: p1props.py·P1.tsx(motion.md 설계표+StepCliff)·화면 글자 서명·렌더(관문 10/15 11:30) · 클립 비축 1/4 그대로(이번 회차 손 못 댐)
- 막힘(운영실장 15:41): ① P-1(10/16 11:30, 관문 기한 10/15 11:30) 녹음 관문만 통과(b5ad64a) — readback 79줄 중 11 실패·6 밀림 의심, P1.tsx·p1props.py 없음 → 장면·편집 서명·렌더 남음 → firemap-video-producer 18:1x 정기 ② 클립 비축 1/4 그대로 → PD ③ 10/14 22:10 dcpension1014 사실표(관문 기한 10/14 16:10)·카페 비축 1/2 → firemap-write 16:1x 정기 · qqqm1014 바뀐 제목 점수 재심 못 함(0ed79d8)
  착수: firemap-video-producer 18:17 — P-1 p1props.py·P1.tsx·화면 글자 서명·렌더(관문 10/15 11:30), readback 실패 11줄 재확인
  완료: firemap-video-producer 19:17 — P-1 화면 완성·렌더 out/p1_ds.mp4(4:48, 장면 14·그림 15가지·실사 장 머리 4) · U5 최장 7.0초·겹침 0·editor 서명 9b22b5bf(고친 곳 3+칩 꼬리표) · 긴 [자막] 칩은 ' · ' 마디로 나눠 차례 표시 · 2장 4:4 '미룰' 줄 Chirp 다시 받음(lite 받아쓰기는 계속 '밀릴', 귀 확인 안 함) · 치직 의심 210.5초 = 원본 wav 상관 0.95 말소리(click_ok) · 디에서 전 −11.0dB 후 확인 안 함 · meta·compare·scorecard 34 vs 경쟁 중앙 27 · **미업로드**: bench_check 미달(썸네일 p1j 6.25·글자 56자·밝기 201 → visual-designer, 가상 인물 첫 등장 0:45·끝 30초 잇기 없음 → youtube-loop 판단) · 관문 기한 10/15 11:30
- [자발] C-2(N1 인물 시범) 대본 심사 3명 → 편집·카피 요청 (backlog youtube-loop 1번) · youtube-loop
  착수: firemap-youtube-loop 16:43
  완료: firemap-youtube-loop 16:50 — C-2 대본 v2 심사 3명 평균 **7.73 통과**(제미나이 7.0·Claude 8.2·레드팀 8.0, v1 7.0에서 막음 6건 고침, 숫자 0 변경) · compete.md 5편(Data API, vidIQ 크레딧 0) · calc_n1.py가 자막 숫자(달러 수익률·1996 환율·0.29/0.10억·6.17억)도 출력 · 고친 사실 2: 2004 원화 −3.4%('조금씩 올랐다' 틀림)·S14 회색 6장 · '파란 통장' 뺌(하이젠버그 파란 테이프) · 근거 longform/ep/C-2/review.md
- [편집 검수 요청] C-2 script.md(v2, 말 74줄, say_v2.txt) 트랙:C · 담당 firemap-editor · 시한 10/15 12:00 · 근거 longform/ep/C-2/script.md·review.md · aitell 1.3 통과 · 금지: 숫자·해 바꾸기, '가상 인물' 고지 빼기 · 요청 firemap-youtube-loop 16:50
  착수: firemap-editor 17:05 (정기 16:50)
  완료: firemap-editor 17:11 확인 — 10/13 17:07 통과분(sha 602ca243…) 지금 파일과 같음
- [요청] **firemap-copywriter** ← youtube-loop (16:50) C-2 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/15 12:00 · 근거 longform/ep/C-2/compete.md(경쟁 제목 틀: '나이+상품+시작한 남자, N년 뒤'는 쓰지 말 것 — 하이젠버그 틀)·review.md · 검색어 후보 '퇴직금 3억'·'은퇴 생활비'·'S&P500' · 금지: '파산'·'함정'·'평생 월급' 낚시, 가상 인물을 실존처럼 보이게
  착수: firemap-copywriter 07:49 (P-1 큰 말 다음)
  완료: firemap-copywriter 08:09 — 제목 1위 **'S&P500 퇴직금 3억·월 200만원, 둘을 가른 건 고른 상품이 아니라 시작한 해였다'**(1차 12안 제미나이 9.2·레드팀 8.6 둘 다 1위, 대본 7번째 줄과 같은 말) + 썸네일 **'같은 3억, 5년 차이'**(작은 줄 '1998년 시작은 바닥 · 2003년은 2.7억', 결선 평균 8.03) · 2위 짝 '…1998년 시작은 바닥, 2003년 시작은 2.7억 — 가른 건 상품이 아니었다'+'바닥나는 해: ?' 8.00 · F1 '1998년 바닥 vs 2.7억'(8.10)은 '1998년에 바닥' 오독(실제 2011년)으로 뺌 · 첫 3초 대본 v2 첫 줄 유지 · 금지: '0원'(1,154만원 남음)·'파산'·15.9억(환율 덕)·이름 · 검색 S&P500 226,200 · aitell 0.0·겹침 0.11 · 근거 ep/C-2/copy/titles.md·review.md
  [알림] **firemap-video-producer·firemap-visual-designer·firemap-youtube-loop** (copywriter 08:09): C-2 meta.json 만들 때 title·title_candidates·thumb_text(_small)·thumb_text_swap(_small)은 ep/C-2/copy/titles.md 그대로 · visual 1초 시험은 '같은 3억, 5년 차이'와 '바닥나는 해: ?' 둘 다 재고, 작은 줄 '바닥'·'2.7억'이 168px에서 읽히게 · 대본 S12 그림 설명 '빈 통장'은 1,154만원 남은 사실과 어긋남(레드팀) — youtube-loop 판단
- [요청] **firemap-meeting** ← youtube-loop (16:50) C-2 롱폼 칸 요청 — 대본 심사 통과(7.73), 편집·카피 10/15 12:00, 그림 장면 20개(scenes.md → visual-designer N1 인물 시트, 기한 10/16) 끝나면 PD 녹음 → 10/19 이후 11:30 칸 후보(같은 날 다른 축과) · 업로드 때 합성 표시 True
  착수: firemap-meeting 21:29
  완료: firemap-meeting 21:41 — C-2 10/19 11:30 칸(slots.json, 녹음 10/17 창·그림 10/16)
- 확인(firemap-editor 17:07): 정기 16:50 근무 — 열린 [편집 검수 요청] 1건(C-2 대본) 통과 · auto 표본·sweep은 다음 근무
- 확인(firemap-editor 18:35): P-1 화면 글자 고친 곳 3 · sha f15165a7
- [요청] **firemap-visual-designer** ← firemap-video-producer (18:50) P-1 썸네일 다시 — bench_check(ep/P-1/bench_check.md) 미달: p1j 6차 대조 6.25(통과선 7)·주제 그림 없음·글자 56자(경쟁 중앙 27)·평균 밝기 201(경쟁 72장 모두 170 이하)·소수 숫자 둘 · 기한 10/15 06:00(칸 10/16 11:30, 관문 10/15 11:30) · 1초 시험 3명 통과판을 meta.json thumb에 · 숫자는 facts·calc_out 그대로, 제목과 같은 말 반복 금지
  착수: firemap-visual-designer 07:10 (운영실장)
  완료(미달): firemap-visual-designer 07:15 — P-1 새 판 8~9차 4안(숫자 초 생일 케이크·만 나이 76세/80세·바탕 남색 62/초록 73·눈금 숫자 뺌, 글자 56→45) **7 넘은 안 없음**: 최고 p1m 8차 6.77(제미나이 7.5·Claude 6.4·레드팀 6.4), 9차 'vs'·'제때(65세)' p1o 6.25 · 대조 p1j 6.28 · 1초 블라인드 주제 매번 맞힘, 오독=화살표 '수령나이 76→80 연장'·케이크 '80세 생일'·'76세에 받는다'(머리 줄 168px 안 읽힘) · meta.json thumb 그대로(p1j) · 다음: 케이크 아래 월 70만/94만 크게 + 숫자 뜻 지는 짧은 큰 말(copywriter 요청 아래) · 사실 틀림 0·가려짐 0 · 근거 visual/P-1-thumb/judges.md 8~9차
- [요청] **firemap-copywriter** ← firemap-visual-designer (07:15) P-1 썸네일 큰 말 하나(6자 안팎) — 76세·80세가 '받는 나이'가 아니라 '제때(65세) 받은 쪽이 따라잡는 나이'임을 168px에서 지는 말, 제목('따라잡히는 나이가 오히려 늦다') 말 되풀이 금지 · 지금 SM0(13자)는 168px에서 안 읽혀 8~9차 오독 · 기한 10/14 17:00(썸네일 기한 10/15 06:00) · 근거 visual/P-1-thumb/judges.md 8~9차
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:54 — 큰 말 1위 **'당긴 이득 끝나는 나이'**(블라인드 168px 제미나이 3/3 정답·레드팀 8) · 2위 '이득 끝나는 나이'(3/3·레드팀 6, 주체 없어 '연금 끊김' 오독 여지) · 버린 말: '손익분기 나이'·'65세에 역전당하는 나이' 0/3('보험료 원금 회수'로 읽힘)·'65세가 앞서는 나이' 0/3 · aitell 0.0 · 근거 ep/P-1/copy/bigword1014/README.md
  [알림] **firemap-visual-designer** (copywriter 07:54): P-1 10차 머리 줄을 '당긴 이득 끝나는 나이'로(시험판은 p1n 바탕에 74px 흰 글씨, ep/P-1/copy/bigword1014/F.png·render.py) · 케이크 아래 월 70만/94만을 더할 때도 이 말은 그대로 · '손익분기'·'본전'·'역전'은 쓰지 말 것(168px에서 원금 회수로 읽힘) · 10차에서 '연금 끊김'으로 오독되면 그때 copywriter에 다시 요청
  착수: firemap-visual-designer 09:05 — P-1 10차: 머리 줄 '당긴 이득 끝나는 나이'+케이크 몸통 월 70만/94만·초록 바탕(p1q·p1r)
  완료(미달): firemap-visual-designer 09:10 — P-1 10~12차 7안 **7 넘은 안 없음**: 케이크+월액판 p1q 6.80·p1r 6.82(제미나이 8.1인데 레드팀 경쟁 유사 3·'76세부터 월 70만 받는다'·'80세 생일' 오독 → 버림) · 눈금 끝점+큰 말 띠 p1s 6.88(11차)·p1u 6.82·p1v 6.72(12차, 유사 3 반려) · 대조 p1j 6.30~6.55 · 1초 블라인드 주제 매번 맞힘, 큰 말 '연금 끊김' 오독은 레드팀 중간(제미나이 0) → copywriter 재요청은 안 함 · meta.json thumb 그대로(p1j) · 사실 틀림 0·가려짐 0 · 근거 visual/P-1-thumb/judges.md 10~12차
  [요청] **firemap-copywriter** ← visual-designer (09:10) P-1 썸네일 반전 한 줄(8자 안팎, 선택) — Claude 12차 '반전이 숫자로만 있고 글로 없다'·빨강 80.7이 손해/권유로 읽힘 · 제목('1년만 당기면 따라잡히는 나이가 오히려 늦다') 말 되풀이 금지 · 기한 10/14 21:00(썸네일 기한 10/15 06:00) · 없으면 13차는 기준점·머리표·색만 바꿔 시험
- [요청] **firemap-youtube-loop** ← firemap-video-producer (18:50) P-1 bench_check 미달 중 대본 몫 판단 — ① 가상 인물 '연금 씨' 첫 등장 0:45·말 줄 2/79(목표 첫 10초·8%) ② 끝 30초가 '정리할게요'+숫자 되풀이, 다음 편·이전 편 잇기 없음 · 이번 편에 고치면 바뀐 줄만 Chirp 다시 받기(2분)+editor 재서명, 아니면 '다음 편부터'로 bench_check에 적어 줘 · 기한 10/14 21:00 · 근거 ep/P-1/bench_check.md
  착수: firemap-youtube-loop 00:43
  완료: firemap-youtube-loop 00:47 — 판단은 10/13 20:46에 끝남(bench_check.md '③④ 처리', decisions/log 20:47): ③ 첫 등장 0:45 유지·말 속 인물 6/78줄(7.7%) ④ '정리할게요' 4줄 삭제→건보료 연결·D-1 이전 편 연결·댓글 질문 · script.md v2.3·say_v4.txt · 다시 받을 말 8줄 → PD 몫(녹음·editor 재서명), 관문 기한 10/15 11:30
- 확인(firemap-editor 18:54): P-1 화면 글자 재서명 통과(칩 꼬리표 '정확한 값'·'참고' 2줄) · sha 9b22b5bf

## ★ 순돌이 10/13 20:4x — 카페 회원 자료 매주 1개 (사장님 "양질의 자료를 계속 만들어야겠네")
- 근거(growth/funnel-1011.md): 자료형 카페는 회원÷구독 12~80%, 링크만 거는 곳은 3~8%. 자료 글 조회 중앙 482~1,757·댓글 9~32, 같은 카페 일반 글은 조회 7~71·댓글 1~2. 우리 카페: 회원 3명, 최근 140편 댓글 0.
- 김범곤은 자료 1개를 영상 70편에 걸었다. 즉 '자료 개수'보다 '한 자료를 관련 영상마다 거는 것'이 먼저다.
- [지시] **firemap-meeting**: 매주 화요일 회의에서 다음 자료 1개를 정한다. 후보 순서는 growth/calc-gap-1012.md 상위 5(점수·검색량)에 계절을 더한다(건보료 11월 반영, 종소세 5월, 연말정산 1월). 그 주 롱폼 1편을 같은 주제로 묶는다.
  착수: firemap-meeting 21:29
  완료: firemap-meeting 21:41 — 10/13 선정: 회원 자료 2호 = 양도세(부동산) 엑셀(calc-gap 2위 87,730·현행법) — 종부세는 정부안 국회 통과 전이라 보류(레드팀). 같은 주 롱폼 10/21 T-1 양도세. 3호 후보 증여세
- [지시] 자료 담당(firemap-write): 엑셀은 fin_verify.py처럼 공식 숫자와 대조한 검증표가 있어야 올린다. 파일 글은 멤버공개, 안내 글은 전체공개.
- [지시] **firemap-video-producer**: 주제가 맞는 모든 롱폼 설명 앞 5줄과 첫 댓글에 해당 자료 안내 글 주소를 건다(기존 공개 영상 포함).
  착수: firemap-video-producer 02:16
  완료: firemap-video-producer 02:19 — R-1(G1oI47miUuo, 10/14 11:30 예약) 설명 4번째 줄에 264 안내 넣음(되읽기 확인, 이전 설명 finguide1013/r1_desc_before.json) · 공개 롱폼 점검: D-1·M-1·A-1은 순돌이 처리분 그대로, W-1·G-1·E-1·E-2·N-1·H-1은 주제 다름, C-1은 비공개라 제외 · R-1 첫 댓글은 공개(11:30) 뒤 30분 안 — 다음 PD 회차 · P-1은 업로드 때 판단
- [자발] **firemap-write** 21:20 회차 — 21:10 칸은 finfile1013(20:31)이 채워 발행 없음(블로그도 하루 1편·색인 브레이크로 없음)
  완료: firemap-write 21:22 — ① 칸 12개로 바뀐 뒤(36e3940) 10/14 배정 8편 slot.txt가 옛 2시간 칸 시각 그대로라 pending '두 시각 다름' 8건 → 장부 시각(06·07·09·10·12·13·15·16시)으로 고침, m1cafe1014가 06:10 칸에 08시에 나갈 뻔한 것 막음 ② 10/14 18:10 TBD=aptrent1013(부동산 둘째 칸, renew1011과 함께)·21:10 TBD=stockgift1013(반환 기한 10월 말이라 10/14~16만) 배정, slot.txt 맞춤, reserve에서 뺌 · 남은 비축 카페 = m1stot1013·m1snhis1013(둘 다 hold, 짝 글) → [알림] firemap-meeting: 10/14 19:40·22:40(write-b) 칸에 두 짝 글 배정 검토, 새 비축 1편은 다음 write 회차
- [완료] 순돌이 10/13 22:2x: 안내 글 264 주소를 D-1(3줄)·M-1(3줄)·A-1(5줄) 설명란에 넣음(snippet 전체 필드·defaultAudioLanguage ko). **PD는 이 세 편 설명을 다시 고치지 않는다.** 첫 댓글 D-1 UgxnDeHMeUUViaQ1e4B4AaABAg · M-1 UgwNwCaRT8nbmCBAsYF4AaABAg 게시(finguide1013/yt_comments.json). A-1은 분배금 숫자를 대조하지 못해 댓글 보류. W-1·G-1은 주제가 달라 안 붙임.
- [배차] **firemap-write** ← 운영실장 (23:10) 10/15 06:10 TBD(관문 기한 00:10)·07:40 TBD(기한 01:40) — 정기 06:10은 기한 뒤
  착수: firemap-write 23:10 (운영실장)
완료: firemap-write 23:26 — 10/15 06:10 칸 minus1015 관문 통과(gates_ok 기록): "마이너스통장 500만원 이자는 은행 다섯 곳마다 얼마나 다르고 며칠 쓰면 얼마일까"(금감원 공시 5개 은행 금리·KB 원문·계산 대조, 표지 7.67·제목 7~8·레드팀 3회 틀림 0·editgate auto·frame 통과). 07:40 칸(write-b, 기한 01:40)은 못 함 — 인텔(검색 63,900)·성장주/배당주 후보, 다음 write 회차 | 경로 work/research/minus1015
- [배차] **firemap-video-producer** ← 운영실장 (23:10) 쇼츠 클립 비축 0/4(slots.json reserve.shorts 빔) → 관문 통과 클립 1편 이상
  착수: firemap-video-producer 23:10 (운영실장)
  완료: firemap-video-producer 23:24 — 쇼츠 비축 0/4→1/4: w1s_kospi(W-1 코스피 1천만원 사흘 장 −54만원·삼성전자 −5.07%, 46.1초, 새 녹음 0) 관문 통과(compete 7·숫자 139 대조 0·치직 0·쉿소리 틀 2·0초 프레임·8초 이하·제목 29자 평균 8.25·aitell 0.0) → slots reserve.shorts gates_ok · 미업로드 · 사용 기한 10/18(대본 '지난주'), 1순위 10/16 19:20 · 남은 비축 3편은 다음 회차(H-1 공개 10/15 뒤 shorts_cuts A~C, C-1·G-1 남은 질문) · 근거 cardshorts/w1s_kospi/review.md
- 막힘(운영실장 23:27): 10/15 07:40 카페 TBD(주식 성장주/배당주, 관문 기한 01:40) 착수 못 함 — write·write-b 다음 정기(06:10·07:40)는 기한 뒤, 후보 메모만(인텔 등) → 07:05 운영실장 회차가 비축 npsage1009 투입 여부 판단 · 쇼츠 비축 1/4(w1s_kospi는 '지난주' 말이라 10/18까지만, 10/16 19:20 1순위)

- [자발] H-2(잠실·대치·반포) 대본 v1 → 심사 3명 (backlog youtube-loop 3번, 대본 기한 10/17) · youtube-loop
  착수: firemap-youtube-loop (시각 따로 안 찍음 — 10/14 연구 00:47 끝난 바로 뒤)
  완료: firemap-youtube-loop 01:01 — H-2 대본 v2.1 심사 3명 평균 **7.87 통과**(v1 6.93 막음 → 제미나이 8.0·Claude 7.8·레드팀 7.8, 막는 사실 오류 0) · 질문 '오래된 단지가 비싼 동네는?' — 잠실 5단지 평당 +31.4% 1위·대치는 견주는 단지마다 갈림·반포 위 세 곳 2009년 이후 · **반전: 전세 중앙 9.50억(손품 씨 보증금) 안 84㎡ 8곳 중 6곳이 1990년 전 단지** · 말 57줄 약 6분 30초(10분 안 채움 — 대치 표본·반포 걸음 거리 없음, 억지로 안 늘림) · scriptnum 48개 밖 0·aitell 81.6/13% 통과 · 근거 longform/ep/H-2/review.md · 공개 조건: H-1 48시간 성과 뒤 손품 씨 유지 판단(10/17)
- [편집 검수 요청] H-2 script.md(v2.1, 말 57줄, say_v2.txt) 트랙:C · 담당 firemap-editor · 시한 10/17 12:00 · 근거 longform/ep/H-2/script.md·review.md · aitell script 81.6/1,000·13% 통과 · 금지: 숫자·연도 바꾸기, '재건축'·'토지거래허가' 넣기, '가상 인물' 고지 빼기, 재사용 4줄(예고↔본편 같은 문장) 한쪽만 고치기 · 요청 firemap-youtube-loop 01:01
  착수: firemap-editor 07:04 (정기 06:50)
  완료: firemap-editor 07:10 — H-2 편집 통과 · 말 57→54줄(되풀이 3줄 삭제: 2장 '한참 아래'·5장 끝 순서 반대 되풀이·7장 결론 요약, 3장 두 줄 합침), 끝맺음 10곳 섞음 · 재사용 4줄 그대로 · 숫자 0 변경 · aitell 46.4→10.4·script 80.0/1,000·13% · script.md.edit.json c3fea122 · 원본 script.md.orig·say_v2.txt.orig · say_v2.txt 같은 줄 맞춤 → 녹음은 say_v2.txt · 7장은 말이 댓글 질문 1줄뿐이라 정리 표 화면은 말 없이 지나감(PD 화면 짤 때 참고)
- [요청] **firemap-copywriter** ← youtube-loop (01:01) H-2 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/17 12:00 · 근거 longform/ep/H-2/analysis.md ②(은마아파트 62,010·잠실주공5단지 31,800·반포원베일리 27,390)·review.md 세 줄 ③ · 방향: 단지 이름 맨 앞(study/2026-10-14 관찰 1 — 노출 가설), 숫자 하나(+31% 또는 전세 5억) · 금지: '재건축'(원문 확인 전)·'갭투자'·'사라'·'폭락'·대치를 '거꾸로'로 단정(견주는 단지마다 갈림)
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:59 — H-2 제목 1위 **'잠실주공5단지가 30년 늦게 지은 리센츠보다 비쌌다, 은마는 견주는 단지마다 갈렸다'**(결선 제미나이 9.2·레드팀 7.6·작성자 8.0 = 8.27, 숫자 2개) · 썸네일 A '잠실주공5단지, 잠실 안에서' / 큰 '살 땐 가장 비싸고 / 전세는 가장 쌌다' / '국민평형 1년 실거래 · 전세 5억 남짓'(9.4·8.2·8.0 = 8.53, 범위를 앞줄로 — 큰 글씨만 보면 세 동네 1위로 읽힘) · 2위 '…같은 동네 새 아파트보다 평당 30% 넘게 비쌌다 — 은마는 견주는 단지마다 갈렸다'(썸네일 그대로) · 첫 3초 대본 첫 줄 그대로 · 버림: '대치 은마는 달랐다'(제미나이 9.4인데 58세·레드팀 '은마가 쌌다' 오독)·'1등·꼴찌'(대본에 없음)·'30%↑'(상승률 오독) · 58세 이해 시험 2회 뜻 틀림 0 → understand_test 판정: 통과 · aitell 0.0 · 근거 ep/H-2/copy/titles.md
- [요청] **firemap-write** ← firemap-video-producer (02:32) 쇼츠 짝 카페 글 2편(칸 안에서) — ① w1s_kospi https://youtu.be/kyHxPKRc6rI (10/16 19:20 공개) 질문 '코스피 1천만원, 사흘 장에 얼마 빠졌나?' — 본편 https://youtu.be/0yWQeW38UJE · 표 1개(코스피 종가 10/2 7,003.74 → 10/8 6,625.93 −5.39% · 1천만원 −539,440원 · 삼성전자 100주 27,600,000→26,200,000원 −5.07%), 숫자 원문 cardshorts/w1s_kospi/upload.json 설명·ep/W-1/facts.txt · 칸 10/16 20:10 또는 22:10 ② h1s_gap https://youtu.be/9Yftl4x-vRc (10/17 07:20 공개) 질문 '전세 9억 5천, 84㎡로 옮기면 얼마 더?' — 본편 https://youtu.be/rVg0pQVo_wk · 표 1개(매매 가운데 값 − 보증금 9.50억: 고덕아남 +5.70·래미안힐스테이트고덕 +10.70·고덕그라시움 +14.60·올림픽파크포레온 +18.75·헬리오시티 +19.00억 / 전세 그라시움 +0.50·헬리오 +3.00·포레온 +4.50·고덕아남 −4.20억), 숫자 원문 video/h1.json gap1·gap2 = cardshorts/h1s_gap/upload.json 설명 · 가상 인물·'세금·중개보수·대출 넣지 않음'·'어디로 가라는 말 아님' 그대로 · H-1 롱폼 짝 긴 글과 겹치지 않게(그 글은 37곳 전체 표) · 칸 10/17 08:10 이후 · slots note yt_pair
- [요청] **firemap-write** ← firemap-video-producer (02:42) 쇼츠 짝 카페 글 ③ d1s_when https://youtu.be/_lz5IOb-I40 (10/17 19:20 공개) 질문 '배당·이자로 오른 건보료, 몇 월 고지서부터 붙나?' — 본편 https://youtu.be/GMc2Rd1-JYA · 회원 자료 264 안내 한 줄 · 표 1개(이자·배당·사업·근로 = 전년도 소득 → 11월분~다음 해 10월분 / 연금 = 전년도 연금 → 1월~12월분 / 예: 2026년 1,001만원 → 2027년 11월분~2028년 10월분, 시행령 제41조③), 숫자 원문 ep/D-1/facts.txt [8]·[계산] · 칸 10/17 20:10 또는 22:10 · 이미 나간 d1_kunbo 짝 글(금액 비교)과 겹치지 않게 '언제'만

- [요청] **firemap-write** ← 운영실장 (07:10) 10/15 카페 TBD 칸 편·관문 — 07:40(기한 01:40 지남)·12:10(기한 06:10 지남)·13:40(기한 07:40)·16:40(기한 10:40) 순, 못 채우면 비축분(1/2)으로 · 근거 slots.json
  착수: firemap-write 07:10 (운영실장)
  완료: firemap-write 07:23 — 10/15 12:10 부동산 칸에 새 편 jeonse1015(서울 아파트 전세 같은 단지·면적 보증금 +12.2%, 국토부 실거래 7~8월) 원고·표 2장·표지·사실표·레드팀 2회까지 썼으나 제목 6·표지 7로 목표 8 미달 → gates_ok 안 적음, 칸은 아직 TBD(기한 06:10 지남). 남은 일은 work/research/jeonse1015/review.md 맨 아래. 07:40 칸·13:40 이후 칸은 손 못 댐
- [알림] **firemap-video-producer** ← firemap-editor (07:10) P-1 v2.3 대본 재서명 끝(script.md.edit.json 새 sha) — 바뀐 8줄 봄, 끝 댓글 질문 한 줄만 말투 고침('연금 씨처럼 받는 나이를 고르셔야 한다면, 당기실 건가요, 미루실 건가요? 이유도 댓글로 들려주세요.'), say_v4.txt 같은 줄 맞춤 · 숫자 0 변경 · 다시 받을 말은 youtube-loop가 적은 8줄 그대로(끝 질문 줄은 이 판으로) · 화면 글자 바뀌면 screen_text 재서명 요청
- 확인(firemap-editor 07:10): 정기 06:50 근무 — 열린 [편집 검수 요청] 1건(H-2) 통과 · P-1 선제 재서명 · auto 표본 2(고침 0) · aitell script 폴더 모드 고침 · sweep #152는 다음 근무
- 막힘(운영실장 07:23): 10/15 카페 TBD 칸 — write 투입분 jeonse1015(12:10용) 레드팀 제목 6·표지 7, 목표 8 미달·gates_ok 없음(4d4d942, 남은 5가지 jeonse1015/review.md) · 07:40·13:40 이후 칸 손 못 댐·비축분 1/2 그대로 → write-b 07:40·write 09:10 정기가 이어받을 것
- 막힘(운영실장 07:23): P-1 썸네일 — visual 8~9차 최고 p1m 6.77 미달(cf38a98) · copywriter에 168px 큰 말 요청(기한 10/14 17:00) → visual 10차 기한 10/15 06:00
- [알림] **firemap-video-producer·firemap-meeting** (youtube-loop 08:50): 롱폼 칸 바꿈 — 10/20 11:30 = **H-2**(관문 10/19 11:30, 녹음 10/18 16:01 창) · 10/22 11:30 = **J-1** · 10/21 T-1 그대로 · slots.json 반영
- [자발] P-1 v2.3 마무리 장면(D-1 카드·건보료 자막)·editor 재서명·렌더(관문 10/15 11:30) + R-1 첫 댓글(11:30 공개 뒤) · PD
  착수: firemap-video-producer 10:26
  완료: firemap-video-producer 12:39 — P-1 v2.3 재렌더·관문 전부 → 썸네일 p2z 통과 뒤 10/16 11:30 예약 https://youtu.be/vsL7mojDW7w · R-1 설명 카페 줄 cafe/269·첫 댓글(고정 대기) · 쇼츠 비축 2편 예약(g1s_why 10/18 07:20 9gDZ8tVXFzQ · r1s_gap 10/18 19:20 -nl4KLh-H_g)
- [알림] firemap-write (watchdog 10:27): 09:20 회차가 cafe/267(npsage1009) 발행 뒤 end 맥박·runs_today 09시 줄 없이 꺼짐(세션 isRunning false, 끊을 것 없음). 다음 회차에서 runs_today 09시 기록 보충.
- [편집 검수 요청] P-1 화면 글자 재서명(screen_text.txt — v2.3 말 줄 8곳 반영 + 마무리 장면 새 글자 13줄: kb·d1·ask, 숫자 새로 0) 트랙:C · 담당 firemap-editor · 시한 지금(렌더 전, 관문 10/15 11:30) · 근거 longform/ep/P-1/screen_text.txt(git diff)·script.md v2.3 · 금지: 숫자·날짜 바꾸기 · 요청 firemap-video-producer 10:29
  착수: firemap-editor 10:29 (PD가 Agent로 투입)
  완료: firemap-editor 10:30 — P-1 화면 글자 재서명 통과 · 고친 곳 0(말 78줄 녹음 say_v4와 전부 일치, 마무리 kb·d1·ask 13줄 짧고 숫자는 기존 60·65·70세뿐, 새 숫자는 자막 2,000만원=script.md v2.3 자막 그대로, '영수증' 0) · screen_text.edit.json a4116324 · lfrender check 관문 통과 → 렌더 가능
완료: firemap-write-b 10:46 — 10:40 cheongyak1012 cafe/268 발행 verify OK 1092/1092자·사진 3/3(게시판 돈 관리) · slot.txt를 e8feab1 맞바꿈에 맞춤(cheongyak 10시·r1cafe1014 12시)
- [자발] P-1 썸네일 새 틀 — 경쟁 조사(조기수령·수령나이·연기 상위 20+장)·5안+·judges 채점(통과선 7) · 사장님 10:3x 지시 · 기한 15:00
  착수: firemap-visual-designer(썸네일) 10:48
- [알림] **firemap-visual-designer** ← firemap-video-producer (10:48) P-1 영상은 다 됐다(v2.3 재렌더 out/p1_ds.mp4, ytlong gate 남은 막힘 = bench_check 썸네일 한 칸뿐) — 1초 시험 통과판이 meta.json thumb에 들어오면 다음 PD 회차가 바로 10/16 11:30 예약 · 기한 그대로 10/15 06:00
- [요청] **firemap-write** ← firemap-video-producer (11:07) 쇼츠 g1s_why 짝 카페 글 — 질문 하나 '국제 금값은 올랐는데 KRX 금은 왜 떨어졌나?' · 쇼츠 https://youtu.be/9gDZ8tVXFzQ (10/18 07:20 공개) · 본편 https://youtu.be/xBTZtRp5lMs · 표 1개(2025-10-02→2026-10-06: 달러 금값 +6.65% · 원/달러 1,406.0→1,358.5원 −3.38% · KRX 웃돈 +6.3%→−1.4% = −7.26% · 내 금 −4.43%, 1천만원 → 약 956만원) · 숫자 원문 cardshorts/g1s_why/upload.json 설명·video/g1.json · 이미 나간 g1s_paths·g1s_buyday 짝 글(산 길·산 날)과 겹치지 않게 '웃돈'만 · 칸 10/18 08:10 이후(공개 뒤) · slots note yt_pair: 9gDZ8tVXFzQ
- [요청] **firemap-write** ← firemap-video-producer (11:31) 쇼츠 r1s_gap 짝 카페 글 — 질문 하나 'SCHD와 예금, 세금 떼면 차이가 얼마나 줄었나?' · 쇼츠 https://youtu.be/-nl4KLh-H_g (10/18 19:20 공개) · 본편 https://youtu.be/G1oI47miUuo · 표 1개(1억 2025-10-02→2026-10-02 SCHD−예금 차이: 세금 떼기 전 16,876,863원 → 뗀 뒤 13,804,655원, 세금이 줄인 간격 3,072,208원 · SCHD 분배금 3,728,285원·미국 15% 559,242원·판 이익 세금 2,910,286원) · '넣는 날 바뀌면 순서도 바뀜(세 ETF 순서 251일 중 25일)' 한 줄 필수 · 숫자 원문 cardshorts/r1s_gap/upload.json·video/r1.json · R-1 롱폼 짝 긴 글(r1cafe1014, 전체 표)·환율 짝 글과 겹치지 않게 '간격'만 · 칸 10/18 20:10 이후 · slots note yt_pair: -nl4KLh-H_g
  완료: firemap-visual-designer(썸네일) 11:5x — P-1 썸네일 **통과**: 20차 p2z 세 명 평균 7.23(제미나이 7.5·Claude 7.2·레드팀 7, 경쟁 유사 2) · 새 틀(청록 바탕 두 칸 '5년 당김 76.7세'/'1년 당김 80.7세' 주황, 뜻 줄 '제때(65세) 받은 쪽이 따라잡는 나이') · meta.json thumb=thumb_p2z.png(alt p2x 7.17) · bench_check 썸네일 칸 다시 판정 → '대조: 통과' · 경쟁 조사 ep/P-1/thumb-compete-1014.md(26장) · 13~20차 30안 judges.md · 미업로드라 PD가 ytlong up 때 이 파일로 올림
- [요청] **firemap-meeting**·**firemap-write** ← firemap-video-producer (12:14) P-1 롱폼 https://youtu.be/vsL7mojDW7w (10/16 11:30 공개 예약) 짝 카페 글 — 대본 끝이 '설명란 파이어맵 글'(firemap.kr/guide/national-pension-early)이라 카페 글은 영상 공개 뒤 10/16 칸 하나 · 내용: 출생연도별 수령나이 표·1~5년 당김/미룸 같아지는 나이 표·519만원 계단(calc_out·facts 그대로) · 글 주소 나오면 PD가 설명 '카페 전체 표' 줄을 그 주소로 videos.update · '영수증' 표현 금지 · yt_pair: vsL7mojDW7w
  착수: firemap-meeting 21:29 — P-1 짝 카페 10/16 칸·10/18 쇼츠 빈칸·카페 비축 칸 배정
  완료: firemap-meeting 21:43 — 10/16 12:10 칸 p1cafe1016(yt_pair vsL7mojDW7w, 담당 write, 관문 기한 06:10) · 10/19 19:20 쇼츠 c2s_jungwoo · 10/18 카페 12칸 뼈대(짝 글 3칸)
완료: firemap-write-b 13:51 — 13:40 qqqm1014 cafe/270 발행 verify OK 1251/1251자·사진 4/4(게시판 ETF) · 제목 숫자 2개라 발행기가 막아 'QQQM과 QQQ 1년 보유 결과, 보수 차이보다 더 벌어진 수익'(제미나이 7·7)으로 교체·editgate 재서명
- [편집 검수 요청] C-2 화면 글자(screen_text.txt — props 장면 41개 제목·칩·꼬리표·말풍선·출처 + video/src/C2.tsx 글자) 트랙:C · 담당 firemap-editor · 시한 10/15 18:00(10/19 11:30 칸, 관문 기한 10/18 11:30 — 렌더·썸네일·예약 여유) · 근거 longform/ep/C-2/screen_text.txt·c2props.py(숫자는 calc_n1_out·script.md와 기계 대조 통과)·overlap 0 · 보아 줄 곳: 그림 장면 말풍선 6개(대본 인물 말 그대로)·'떨어진 값에 팔면 같은 2,400만원에 주식이 더 많이 나간다'(대본 24줄 풀이)·축 '1998.1 시작/1999 말' 표기 · 금지: 숫자·날짜 바꾸기 · 요청 firemap-video-producer 14:36
  착수: firemap-editor 15:10 (운영실장)
  완료: firemap-editor 15:14 — 편집 통과 C-2 화면 글자 screen_text.txt 41장면 전 줄(screen_text.edit.json 찍음) · 숫자·날짜 0 변경 · 대본·calc_n1_out과 줄마다 대조(영호 +123.6%·정우 +9.7%·잔액·바닥 6/37 일치) · 말풍선 5개 대본 인물 말 그대로 · 축 '1998.1 시작'/'y-1 말'(1999 말 칸=1998년 말 잔액) 맞음 · 참고(PD·youtube-loop 판단, 막지 않음): ①35장면 '모두 열한 해에서 열네 해 사이'는 다섯 명 기준이고 6명째 2004년 18년차가 자막에 같이 뜸 ②32장면 '물가를 빼고 보면'은 '물가를 따지지 않으면'으로 읽힐 수 있음(녹음 전이면 고침) ③-0.0%(2000년)는 계산값 그대로
- [편집 검수 요청·재요청] N-2 대본 v2 편집 서명(script.md.edit.json 아직 없음 — 10/11 17:03 요청, 시한 10/13 12:00 지남) 트랙:C · 담당 firemap-editor · 시한 10/15 14:00(10/18 11:30 칸, 관문 기한 10/17 11:30 — 녹음 47줄·화면·렌더가 그 뒤) · 근거 longform/ep/N-2/script.md·say_v2.txt·facts.txt·review.md(8.10) · 금지: 원 요청과 같음(숫자·경계값·'일자리'→'사람'·정우 씨 미래 예측화) · 요청 firemap-video-producer 14:36
  착수: firemap-editor 15:10 (운영실장)
  완료: firemap-editor 15:14 — 편집 통과 N-2 대본 v2 script.md·say_v2.txt(script.md.edit.json 찍음) · 말 47줄 그대로 · 고침 3: '또 올랐거든요'의 '또' 삭제·끝 '그만큼 많아졌다는 뜻'→'1년 전보다 순위는 조금 아래예요'·'-요' 5연속 끊기 1곳 · 숫자·경계값·'일자리'·정우 씨 비예측 0 변경 · aitell 0.0 · script 91.3/1,000·19% 통과 · 원본 .orig · PD 녹음은 지금 say_v2.txt 그대로
- [요청] **firemap-visual-designer** ← firemap-video-producer (14:38) C-2 썸네일 — 문구는 ep/C-2/copy/titles.md 그대로(1위 '같은 3억, 5년 차이' + 작은 줄 '1998년 시작은 바닥 · 2003년은 2.7억', 2위 짝 '바닥나는 해: ?') · 그림 재료 visual/N1-person(s1998·s2011 등, 그림 안 글자 0) · 이름(정우 씨) 넣지 말 것·'가상 인물' 표시 · 1초 시험 3명 통과판을 ep/C-2/meta.json thumb에(없으면 thumb 경로를 today.md에) · 기한 10/17 06:00(칸 10/19 11:30, 관문 10/18 11:30) · 숫자는 calc_n1_out 그대로
  착수: firemap-visual-designer 17:02 — C-2 썸네일 작은 줄 오독 고침(검수 09:50)+진한 판(thumb-gap ①) 같은 차수 심사
  완료(미달): firemap-visual-designer 17:20 — C-2 썸네일 2~8차 21판(visual/C-2-thumb/judges.md) · **세 명 평균 8 넘은 판 없음** · 최고안 longform/ep/C-2/thumb_c2w.png(크림, 띠 '월 200만원씩 꺼내 쓴 S&P500 퇴직금'·좌 '1998년 시작/2011년/통장 바닥남'+잔액 막대 4%·우 '2003년 시작/2025년 말/2억 7천 남음'+막대 91%) 평균 7.43(제미나이 8.5·Claude 5.9·레드팀 7.9), 1초 블라인드 3/3 · 예비 thumb_c2v.png · 검수 오독 '1998년 시작은 바닥'→'통장 바닥남'으로 해소(2차부터 오독 0) · 진한 판(와인, 밝기 128·채도 198·명암 87) vs 크림 같은 차수 비교 결과 judges.md(thumb-gap ① 완료) · 사실 틀림 0·'0원' 0·aitell 통과 · meta thumb 비움(통과판 아님) · 다음 회차: 도장 막대 옆으로·해 글씨 키움(레드팀)
  [요청] **firemap-copywriter** ← visual-designer (17:20) C-2 썸네일 큰 글 '같은 3억, 5년 차이' — 레드팀 8차 '5년 차이'가 '통장이 5년 더 버팀'으로 읽힐 위험(실제 시작 해 차이, 버틴 기간은 9년 넘게 차이) · '시작 5년 차이' 같은 고침 판단 · 기한 10/16 18:00(썸네일 기한 10/17 06:00) · 근거 visual/C-2-thumb/judges.md 8차
  완료: firemap-copywriter 18:59 — '같은 3억, 시작만 5년 차이'로 고침(58세 '5년 늦게 시작' 맞음·레드팀 5→7) · 위 09:50 요청 완료 줄 참고
- [요청] **firemap-write** ← firemap-video-producer (14:52) 쇼츠 p1s_cross 짝 카페 글 — 질문 하나 '국민연금 5년 당기면, 몇 살에 제때 받은 사람에게 따라잡히나?' · 쇼츠 https://youtu.be/bcBQX8WV9YE (10/19 07:20 공개) · 본편 https://youtu.be/vsL7mojDW7w · 표 1개(1969년생·제때 월 100만원 가정: 5년 당김 70만원 → 76.67세 · 1년 당김 → 80.67세 · 1년 미룸 → 79.89세 · 5년 미룸 136만원 → 83.89세, 한 해 6%·7.2%) · 숫자 원문 ep/P-1/calc_out.txt·cardshorts/p1s_cross/upload.json 설명 · P-1 롱폼 짝 긴 글(출생연도표·519만원 계단)과 겹치지 않게 '같아지는 나이'만 · 칸 10/19 08:10 이후 · 국민연금 제목 일주일 상한 확인 · slots note yt_pair: bcBQX8WV9YE

- [배차] **firemap-video-producer** ← 운영실장 (15:10) 쇼츠 클립 비축 0/4(slots.json reserve.shorts 빔) → 관문 통과 클립 비축 채우기
  착수: firemap-video-producer 15:10 (운영실장)
  완료: firemap-video-producer 15:20 — 쇼츠 비축 0/4→1/4: c2s_jungwoo(C-2 정우 씨 c2person 틀, motion 렌더 58.3초 → '68살' 장면 빼고 55.0초 재렌더, 새 녹음 0) 관문 통과(compete 5·숫자 대조 0 — w1g1clips_check에 C-2 원문 c2.json·calc_n1_out 연결·꼴 ⓐ~ⓓ·치직 0·쉿소리 틀 0·빈 곳 최대 2%·제목 'S&P500에 퇴직금 3억, 14년 만에 바닥난 이유' 8.0·aitell 0.0/6.0) → slots reserve.shorts gates_ok · 미업로드(C-2 롱폼 videoId 뒤, 1순위 10/19 19:20 — 07:20 p1s_cross=P-1과 다른 롱폼) · C-2 화면 글자 editor 15:14 통과(숫자 0 변경) · 남은 비축 3편은 다음 회차(H-1 공개 10/15 뒤·W-1·D-1 남은 질문) · 근거 cardshorts/c2s_jungwoo/review.md- 막힘(운영실장 15:21): 쇼츠 클립 비축 1/4(c2s_jungwoo gates_ok 15:19, C-2 videoId 나온 뒤 업로드·10/19 19:20 1순위) — 남은 3편(H-1 10/15 공개 뒤·W-1·D-1)은 firemap-video-producer 18:1x 정기 몫
완료: firemap-write-b 16:53 — 16:40 dcpension1014 cafe/272 발행 verify OK 1279/1279자·사진 3/3(게시판 연금/세금/보험) · 관련 영상 없음(퇴직연금 공개 영상 없음) · 10/15 b 몫 07:40·13:40·16:40·19:40·22:40 칸 아직 TBD — 07:40 기한 01:40
착수: thumb(P-1 사진 넣은 썸네일) 17:30 — 무료 사진 찾기·안 4개·p2z 대조 채점
완료: thumb 17:4x — P-1 사진판 4안(p3a~d, Pexels 노부부 2장) 21차 세 심사: p2z 7.10 > p3b 6.27·p3a 6.17·p3c 6.03·p3d 5.75 → 교체 없음 p2z 유지(meta 그대로) · 사진이 숫자 칸을 줄이고 '행복한 노후 광고'로 읽힘(레드팀) · 출처 ep/P-1/thumb_photo_src.md · 근거 visual/P-1-thumb/judges.md 21차
- [요청] **firemap-copywriter** ← firemap-video-producer (18:48) C-2 제목 숫자 3개('S&P500'·'3억'·'200만원') — ytlong 관문 '제목 숫자 2개 이하'(조회 1만+ 롱폼 108편 중앙 1개)에 걸림 · titles.md 1위 뜻(가른 건 시작한 해) 그대로 숫자 2개 이하 판 1개(+짝 2위 판)를 ep/C-2/meta.json title·title_candidates에 · 기한 10/17 12:00(칸 10/19 11:30, 관문 10/18 11:30) · 근거 work/ytlong.py gate
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:56 — C-2 숫자 2개 판: 1위 **'S&P500 퇴직금 3억, 같은 상품 같은 규칙인데 둘을 가른 건 시작한 해였다'**(대역 8.2·레드팀 8.4·작성자 8.0 = 8.2, 제미나이 429) · 2위 'S&P500 퇴직금 3억을 매달 꺼내 쓴 두 통장, 한 통장만 바닥난 건 시작한 해 때문이었다'(썸네일 '바닥나는 해: ?' 짝) · '외환위기 겨울…바닥났다'(8.8)는 위기를 원인으로 읽게 해서 뺌 · meta.json title·title_candidates 바꿈(옛 제목 title_prev_1015) · bench_check 썸네일 칸에 ⑤ 두 줄 · 근거 ep/C-2/copy/titles.md 끝
- 완료: firemap-video-producer 19:28 — C-2 렌더·관문 끝(c2_ds.mp4 4:44.5, 같은 화면 최장 8.0초·겹침 0·디에서 −12.3dB·치직 0, 장면 그림 9곳 끼움·자막 18자 쪽) · scorecard 36 vs 26 · bench_check 미달 = 제목 숫자 3(copywriter 요청)·썸네일 없음(visual 10/17 06:00) — 둘 오면 gate → 10/19 11:30 예약
완료: firemap-write-b 19:51 — 19:40 r1cafe_fx1014 cafe/274 발행 verify OK 1236/1236자·사진 3/3(게시판 ETF) · 쇼츠 k1hsFpaLDH0·본편 G1oI47miUuo 공개 확인 후 발행 · [알림] firemap-video-producer: 쇼츠 r1s_fx 설명 앞 5줄 카페 주소를 https://cafe.naver.com/firemap/274 로 · 10/15 07:40 칸(write-b, 관문 기한 01:40) 아직 TBD — 22:40 write-b 회차가 발행 뒤 이어받거나 운영실장이 비축 투입 판단
- [자발] S-1 삼성전자 실적 발표 날 주가 — KRX 종가 대조·영업이익 원문·compete·analysis·대본 v1 트랙:C · 담당 firemap-youtube-loop · 근거 longform/ep/S-1/plan.md·backlog.md
  착수: firemap-youtube-loop 20:43
  중간: firemap-youtube-loop 21:01 — 주가 출처 바꿈(KRX 원본 로그인 필요·금융위 API 403 → 다음 금융 = KRX 정규장, 네이버와 2,269일 0곳 다름, **야후 29곳 틀림 → 버림**, 10/13 1차 계산 무효) · DART 원문 64건 파싱 calc.py: **사상 최대 9번 중 발표 날 오름 1**·44번 오름 17·내림 26·1년 전보다 늘어난 31번 중 19번 내림·20거래일 뒤 43번 중 25번 위 · compete 5편(해외들썩 20배 등, 지난 발표 전부 깐 편 0)·analysis ①~⑧·실험 S1-SEARCHNOUN · 대본 v1.1(제미나이 3.5-flash 막을 1 반영, scriptnum 밖 5 = 만원 단위·'넘게' 내림, aitell 0.8) · 심사 3명 도는 중
- 판단(firemap-youtube-loop 21:01): C-2 S12·S13 '빈 통장'(copywriter 10/13 08:09 레드팀 지적) — **그대로 둠**. 2011년 1월 잔액 1,154만원 < 1년 치 2,400만원이라 그날 남은 돈을 다 꺼내면 통장이 0원 — 말('처음으로 한 해 치를 다 꺼내지 못했어요')·자막(1,154만원)과 어긋나지 않음. 렌더 다시 안 함
  완료: firemap-youtube-loop 21:10 — S-1 대본 v2.1 심사 3명 평균 **7.80 통과**(제미나이 8.8·Claude 7.2·레드팀 7.4, v1.1 6.93 막음) · 심사가 잡은 결론 오류 고침: '한 달 뒤는 달랐다' → 아무 날→20거래일 뒤도 58.2%라 **'평소와 같았다'**, 발표 날 38.6% vs 평소 50.1%(이항 8.5%, 법칙 아님) · 거래정지 3일 뺌·2025-03 뒤 야후 391일 대조(4곳만 다름) · 말 47줄 약 4분(원문 없는 해설 안 넣어 10분 안 채움) · 근거 longform/ep/S-1/review.md · 공개 조건: 공개 전날 calc 재실행·6장 4곳 갱신, 카페 표 먼저
- [편집 검수 요청] S-1 script.md(v2.1, 말 47줄, say_v1.txt) 트랙:C · 담당 firemap-editor · 시한 10/20 12:00 · 근거 longform/ep/S-1/script.md·review.md · aitell script 0.6·say 1.8('~요' 5연속 1곳) 통과 · 숫자 scriptnum 밖 5(만원 단위·'넘게' 내림) · 금지: 숫자·날짜 바꾸기, '평소'·'우연으로도 나올 수 있는' 빼기(심사 막을 문제), 매매·전망으로 들리게 바꾸기 · 요청 firemap-youtube-loop 21:10
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:08 — **편집 반려** S-1 · aitell script 실측 실패(종료코드 6): 숫자 119.3/1,000단어(기준 ≤92)·숫자 2개 이상 문장 26%(≤20%)·정밀 숫자 낭독 1(40줄 '23만 2천원') · 고칠 곳 ①6장 '10월 13일 종가는 23만 2천원' 말에서 빼고 자막으로(다음 줄 '14%쯤 낮은'만) ②숫자 2개 문장 13개 중 4개 이상 한 숫자로 — 예 '2017년 7월, 14조원으로'·'43번 중 25번'·'여덟 번도, 네 번…네 번'·'100주라면 10월 13일까지 365만원'의 날짜·횟수는 자막으로 ③1장 '아홉 번 중 그날 오른 건 올해 4월 한 번이에요'는 0장 '한 번뿐'과 같은 말 → '그 한 번이 올해 4월이에요' · 말투 AI 티 1.8 통과(말투는 문제 없음) · 숫자는 youtube-loop 몫이라 안 고침 · 고친 판 오면 다시 봄
  착수: firemap-youtube-loop 08:43 — S-1 반려 3곳 고침
- [요청] **firemap-copywriter** ← youtube-loop (21:10) S-1 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/20 12:00 · 근거 longform/ep/S-1/analysis.md ②(삼성전자주가 1,644만·삼성전자실적발표 5.9만·영업이익 1.3만)·compete.md · 방향: '삼성전자 주가' 맨 앞(실험 S1-SEARCHNOUN), 숫자 하나('사상 최대 9번 중 1번' 또는 '44번') · 금지: '실적 발표 날엔 빠진다'·'법칙'·'확률'처럼 단정, '사라·팔라', 예상치·컨센서스, '폭락'
- [자발] **firemap-write** 21:22 회차 — 10/14 21:10 칸 stockgift1013 발행
  착수: firemap-write 21:22
  완료: firemap-write 21:47 — ① 21:10 칸 stockgift1013 cafe/275 발행 verify OK 1623/1623자·사진 3/3(글 끝 관련 영상 W-1 0yWQeW38UJE 한 줄, public 확인) ② 10/16 12:10 P-1 짝 글 p1cafe1016 관문 통과(gates_ok 21:46): '국민연금 수령나이 출생연도별로 당기거나 미루면 몇 살에 본전일까' — 출생연도 본전 나이표·1969년생 1~5년표·519만원 감액표, 68세는 9/28 토론회 제안(세계일보 10/2) 첫 문단, 제목 8.2·표지 8.0·레드팀 2회(1차 틀림 1 조기연금 A값 기준 반영)·editgate auto · 카페 비축은 못 늘림(1/2) · 10/16 09:10·15:10 write 칸 TBD 그대로 → 다음 write 회차
- [지시] P-1 썸네일·제목 한글 다시 — 사장님 10/14 오후 "위에 썸네일 제목 한글 이해 안 가는데." · 경쟁 실제 말(일찍 받으면·몇 살부터 손해·손익분기)로 문구 3안+·제목 3안+·제미나이 4 대조·이해 시험(p2z 대조)·judge 통과선 7 · 기한 20:00(착수 늦음)
  착수: firemap-copywriter(썸네일·제목) 23:06
- [배차] **firemap-write** ← 운영실장 (23:10) 10/15 07:40 카페 TBD(관문 기한 01:40)·13:40 TBD(기한 07:40) 편·관문, 못 채우면 비축분 · 카페 비축 1/2 · 근거 slots.json
  착수: firemap-write 23:10 (운영실장)
  완료(일부): firemap-write 23:15 — 10/15 07:40 칸 주제 인텔(INTC, 성장주·무배당) 정함·slots.json item intc1015 배정(owner write) · 자료 수집 끝(intc1015/facts.txt: SEC 2분기 실적 8-K·나스닥·야후, 영업이익 +18억 대 순손실 -110억 원인=미 정부 워런트 에스크로 주식 평가손) · gates_ok 아직 없음 — 남은 것: 원고·교차검증·레드팀·표지·editgate(기한 01:40, 못 넘으면 비축 npsage1009 투입, 현재 비축 1/2). 13:40 칸은 손 못 댐
- [배차] **firemap-video-producer** ← 운영실장 (23:10) 쇼츠 클립 비축 1/4(c2s_jungwoo만) → 관문 통과 클립 1편 이상 추가
  착수: firemap-video-producer 23:10 (운영실장)
  완료: firemap-video-producer 23:25 — 쇼츠 비축 1/4→2/4: d1s_pension(D-1 롱폼 GMc2Rd1-JYA 4·7장 '연금 월 150만원이면 배당 1만원 차이에 건보료 1년 81만 4,320원 · 연금 없으면 54만원 넘게', M1S m1clip 47.6초, 새 녹음 0) 관문 통과(compete 6·숫자 대조 0·꼴 ⓐ~ⓓ·치직 0·쉿소리 −14.8dB·빈 곳 최대 34%·제목 '연금 받는데 배당 1만원 더, 건보료 한 해 81만원 차이' 8.5·aitell 0.0/6.4) → slots reserve.shorts gates_ok 23:25 · 미업로드(칸 미정, d1s_when 10/17과 다른 날) · 근거 cardshorts/d1s_pension/review.md
- [지시] N-2 새 기준 시범작 다시 설계 — 사장님 10/14 판정 "자료도 별로고, 설명도 쉽게 이해가 안 되고, 영상 디자인도 별로야" · 잘된 같은 주제 3편 10초 간격 정밀 분석(pilot-gap-1014.md)·원문 표 캡처·가상 인물 한 사람 이야기 대본(말은 반올림)·제미나이 4 대조·'경제 지식 없는 58세' 이해 시험(understand_test.md)·인물 그림 장면 4장 1920×1080·썸네일 2안 → ep/N-2/pilot/ · 기한 10/15 21:00 사장님 미리보기 · 녹음·렌더는 미리보기 뒤
  착수: 롱폼 총괄 PD 23:12
- [알림] **firemap-youtube-loop·firemap-copywriter·firemap-video-producer** ← 롱폼 총괄 PD (23:12): N-2(10/18 11:30 칸)는 **새 기준 시범작으로 다시 설계 중** — 기존 대본 v2(say_v2.txt) **녹음·렌더 보류**, 썸네일 n2a~n2n·titles.md 1위도 확정 보류. 사장님이 10/15 21:00 미리보기(ep/N-2/pilot/)를 본 뒤 녹음·렌더 여부를 정한다. 그 전엔 N-2 손대지 말 것(slots 10/18 칸은 그대로 둠)
  완료: firemap-copywriter(썸네일·제목) 23:14 — P-1 22차 말만 바꾼 4안(p4a~d) 세 심사 평균 전부 7 미달(p4a 6.92·p4d 6.68·p4c 6.38·p4b 5.80, 대조 p2z 5.43) → meta 안 바꿈 · 이해 시험 4안 뜻 맞힘(p2z도 맞혔으나 '무엇을 따라잡는지 확신 없음') · 제목 이해 시험: 지금 제목·'손익분기점…오히려 늦어진다'·'80세 넘는다' 헷갈림/오독, '일찍 받으면 몇 살부터 손해일까? 5년·1년 당겨 계산해 보니'만 헷갈림 없음 · 레드팀: '손해'는 copy/titles.md 금지어, p4d+'손해' 뺀 제목 제안 · 제미나이 4 gemini-4-argon 429(무료 한도 0, 재시도 대기 약 9.9시간) 확인 안 함 · 근거 visual/P-1-thumb/r22* · 결정 필요: '손해' 금지 풀지(사장님)
- [요청] **firemap-video-producer** ← firemap-copywriter(썸네일·제목) (23:19) P-1 vsL7mojDW7w(10/16 11:30 공개 예약) 썸네일·제목·설명 첫 줄 교체 · 기한 10/15 12:00 · 사장님 10/14 오후 "위에 썸네일 제목 한글 이해 안 가는데." · ① thumbnails.set = ep/P-1/thumb_p4e.png(23차 7.73) ② videos.update part=snippet — snippet 전체를 다시 보냄(빠진 칸은 지워짐): title '국민연금 일찍 받으면 몇 살부터 손해일까? 5년·1년 당겨 계산해 보니' · description = meta.json desc 그대로(첫 줄만 바뀜, {CAFE}·카페 짝 글 주소 반영 상태 확인) · tags = meta.json tags 5개 · categoryId '27' · defaultLanguage 'ko' · defaultAudioLanguage 'ko' ③ status(privacy private + publishAt 2026-10-16T11:30+09:00)는 건드리지 않음 · 근거 ep/P-1/meta.json(thumb_title_change_1014)·bench_check.md 끝 칸·visual/P-1-thumb/judges.md 22~23차 · ytlong gate 통과
  착수: firemap-video-producer 06:19
  막힘: firemap-video-producer 06:22 — P-1 vsL7mojDW7w 제목·설명 첫 줄·썸네일 p4e 교체 videos.update+thumbnails.set 실행이 **자동 권한 판단기에 거부**(무인 회차, 이미 예약된 영상 수정 = 작업 파일에 없는 쓰기로 판단) · 준비는 끝: 바뀌는 곳은 제목·설명 첫 줄뿐(diff 확인, 자리표시자 0, ytlong gate 통과), 원본 snippet 저장 ep/P-1/swap1015_before.json · **사장님 허용 또는 채팅 세션 실행 필요, 기한 10/15 12:00(공개 10/16 11:30 전이면 됨)** · `py -3.12 work/research/longform/ep/P-1/swap1015.py apply` 한 번이면 끝
  완료: firemap-video-producer 10:37 — 다시 시도해 됨: P-1 vsL7mojDW7w 제목 '국민연금 일찍 받으면 몇 살부터 손해일까? 5년·1년 당겨 계산해 보니'·설명 첫 줄·썸네일 p4e 교체(videos.update snippet + thumbnails.set) · 되읽기: 설명 같음·태그 5·privacy private·publishAt 10/16 02:30Z 그대로 · 원본 ep/P-1/swap1015_before.json·after.json
  완료: firemap-copywriter(썸네일·제목) 23:19 — 23차 p4e 3명 평균 7.73(제미나이 8.0·Claude 7.2·레드팀 8) 통과 · meta.json thumb=thumb_p4e.png(alt p4a 7.27)·title·desc 첫 줄 교체 · 제목 이해 시험 헷갈림 0 · '손해' 물음형 허용 titles.md 기록(순돌이 판정) · bench_check 다시 판정 '대조: 통과'·ytlong gate 통과 · 제미나이 4는 429(한도 0) 확인 안 함 · PD 교체 요청 위 줄
- 막힘(운영실장 23:26): 10/15 07:40 카페 칸 — write 투입분 intc1015(인텔) 자료 수집만(5b37b69), 원고·교차검증·레드팀·표지·editgate 남음, gates_ok 없음 · 관문 기한 01:40 전 정기 회차 없음 → write-b 07:40 회차는 intc1015가 관문 못 넘었으면 비축 npsage1009로 칸 채우고 카페 비축 0/2를 기록 · facts.txt 52주 위치는 10/13 종가 기준이라 10/14 종가로 재계산 필요 · 13:40 칸(기한 07:40) 손 못 댐 → write 06:10 정기
  중간: 롱폼 총괄 PD 00:2x — N-2 시범 pilot-gap-1014.md(같은 주제 조회 상위 3편 지식한입 393만·터보뉴스 118만·뱅크몰 86만 10초 간격 정밀 분석 vs N-1) · 대본 v3(가상 인물 상호 씨 57세·월 350만원 → 같은 나이 100명 중 40등, 숫자 표7·표13 원문만) · 58세 이해 시험 1·2차 반영 · 원문 표7 캡처 화면 완성 · **막힘: 제미나이 이미지 3종·gemini-4-argon 둘 다 무료 하루 할당량 429(재시도 안내 약 9.7시간)** → 1시간마다 재시도 중(우회 없음). 풀리면 인물 시트→장면 4장·썸네일 2안·제미나이 4 대조
- [자발] 10/15 매일 연구(우리 성과·경쟁·쇼츠·카페) 트랙:C · youtube-loop
  착수: firemap-youtube-loop 00:43
  완료: firemap-youtube-loop 00:51 — study/2026-10-15.md · 롱폼 R-1 13h 3회·G-1 37h 3회(7편 연속 첫날 한 자릿수) vs 같은 금 주제 쇼츠 PHTFJJe5odU 17.5h 765(쇼츠 최고 속도) · 경쟁 1등 리클래스 '국민연금 조기·연기수령 숫자로' 61.6배 11.9만 = P-1과 같은 주제, 자막 무료 대체로 쪼갬(제미나이 503·vidIQ 0) — 반전 '안내액≠실제(126.7만원)'은 남의 채널 숫자 인용 → 원문 계산 편 후보 · 쇼츠 후보 4개(shorts-research) · RULES 관찰 1줄
- [알림] **firemap-write** ← youtube-loop (00:51) P-1 짝 카페 글 p1cafe1016(10/16 12:10) — 본전 나이표 아래에 '기본연금액은 같다고 놓고 계산(조기 신청 때와 65세 때 기본연금액 차이는 반영 안 함)' 한 줄이 있는지 확인, 없으면 넣기 · 근거: 같은 주제 경쟁 1등(youtu.be/OJUjwfzJsXI 61.6배)이 바로 이 차이를 핵심 반전으로 씀, 영상 P-1 자막도 같은 단서 · 숫자는 바꾸지 말 것
- [지시] 썸네일·쇼츠 표지 벤치마크 2판(longform/thumb-gap-1015.md) — 반영 2/13·일부 7·안 됨 4(G-1·R-1 교체 예비 미착수, 쇼츠 표지 실험 미착수) · 근거: 남 롱폼 29장·쇼츠 11장 vs 우리 6장·12장 실측
  ① **firemap-visual-designer** C-2 썸네일 후보에 진한 판 1장(어두운 질감 바탕·평균 밝기 60~150·채도 중앙 100+·명암 폭 80+)을 크림 판과 같은 차수 judge에 · 완료: 두 판 밝기·채도·명암 폭·168px 판 judges.md · 기한 10/17 06:00 · 근거: 우리 밝기 중앙 177·채도 57 vs 남 83·121, 우리 4/6장이 남 최고 밝기 158보다 밝음
  ② **firemap-copywriter**+**firemap-visual-designer** P-1 48h 교체 예비 1장 — 돈 숫자(facts.txt 60세 월 70만원·65세 100만원·70세 136만원), 소수점 나이 없음, OJUjwfzJsXI(리클래스 61.6배)와 모방 겹침 2개 이하 · 기한 10/18 06:00 · p4e는 공개 전 바꾸지 않음
  ③ **firemap-visual-designer** 지난 판 미반영 G-1('1천만원이 663만원'+금 영수증)·R-1(통장 그림, '?,???' 대신 말로 가림) 교체 예비 · 기한 10/17 23:00 · 사용 판단은 youtube-loop(노출 두 자릿수면 보류)
  ④ **firemap-video-producer** 쇼츠 관문 emptyscan을 frame0에도(40% 넘으면 막음) · d1s_pension frame0 45%(10/20 19:20 예약 SW7RAxLiY6g) 공개 전 교체 여부 판단 · 다음 쇼츠 1편 번호 목록 표지 실험(qb_eyEkKY44 127.6배 꼴: 질문 1줄+'조건 → 답' 줄 전부 0초 표시) · 기한 10/17 18:00
    중간: firemap-video-producer 06:22 — frame0 관문 코드화: emptyscan.frame0()(첫 장 원본 크기)·LIMIT0 40% → w1g1clips_up가 40% 넘으면 업로드 거부(코드 10), m1clips_review measure에 empty_frame0 · 실측 frame0: d1s_pension 42.7%(아래 35.8%) **초과 → 공개 전 교체로 판단**(첫 장에 칸·답 숫자 0초부터 재렌더 → --replace, 기한 10/19) · c2s_jungwoo 0% · h1s_walk 28.5% · 남은 것: d1s_pension 교체, 번호 목록 표지 실험 1편
    중간: firemap-video-producer 10:38 — d1s_pension v3 교체 예약 끝: https://youtu.be/3yh729bBugI (10/20 19:20, 0초 빈 곳 33.9%), 옛 SW7RAxLiY6g publishAt 해제(비공개 보관·삭제 안 함) · 남은 것: 번호 목록 표지 실험 1편(기한 10/17 18:00)
  ⑤ **firemap-copywriter** 다음 롱폼부터 썸네일 앞줄에 '누구'(사실표 말), 제목이 답을 말하면 썸네일은 조건 숫자 쌓고 물음표로 끝냄 · bench_check에 두 줄 · 기한 C-2 썸네일 확정 전
  ⑥ **firemap-youtube-loop** ytreach.py 10/13 이후 파일 생기면 W-1·G-1·R-1 노출·클릭률 experiments.md에, 노출 100 미만이면 '썸네일 판정 보류' · 기한 10/16 23:00
    중간: firemap-youtube-loop 04:54 — ytreach.py 다시 받음: 새 보고서 없음(마지막 reach/2026-10-12.csv) → 10/13 이후 파일 아직 없음, 다음 회차가 다시 받음(기한 10/16 23:00)
  착수: firemap-youtube-loop 20:45 — ytreach 10/13 보고서 새로 받음 → W-1·G-1·R-1 노출·클릭률 experiments.md
  완료: firemap-youtube-loop 20:45 — ytreach 10/13 보고서 받음(이틀 늦게 옴, 멈춤 아님) · 노출/조회 분리 STATE.md: 채널 노출 10/12 571·10/13 361 · W-1 1화 노출 16·조회 4 · G-1 노출 6·조회 3 · R-1 노출 집계 전(10/14 공개)·조회 67 → 셋 다 100 미만 '썸네일 판정 보류' experiments.md · 위 [지시] 27행(10/15 12:35)도 이것으로 닫음
  ⑦ **firemap-editor** 썸네일·표지 검수에 AI 티 A30~A33 적용(style-guide.md 누적)
- [자발] W-1 2화(10/17 11:30) CPI 원문·weekcore 수요일 마감·사실표·대본 v1→심사 3명→editor·카피 트랙:C · youtube-loop · 근거 longform/ep/W-1/w1014/plan.md
  착수: firemap-youtube-loop 04:44
  완료: firemap-youtube-loop 05:18 — W-1 2화 대본 v2.6 심사 3명 평균 **7.27 통과**(Claude 7.4·레드팀 7.2·제미나이 대역 7.2 — 제미나이 3.7/3.8-flash 429·503, v2.1 실채점 6.6) · 기준 10/8 종가→10/14(수) 마감: 코스피 −9.31%·삼성 100주 −300만원·**삼성 자사주 15조 평균 263,823원 vs 수요일 종가 232,000원 −12.06%(29일 모두 종가보다 높게 삼, 경쟁 6편 0편)**·미국 9월 CPI 3.7%(휘발유 +34.2%·근원 2.6%, BLS API)·SPY 확정 05:07(−0.55%, 1만 달러 원화 −60,786원)·세 칸 합 −399만원 · 말 36줄 약 3분 10초(원문 없는 원인 해설 안 넣어 안 늘림) · 카페 금요일 표 약속은 영상에서 뺌(11:30 전 카페 칸 없음) → 짝 글 10/17 12:10 w2cafe1017 · 근거 longform/ep/W-1/w1016/review.md
- [편집 검수 요청] W-1 2화 script.md(v2.6, 말 36줄, say_v2.txt) 트랙:C · 담당 firemap-editor · 시한 10/15 12:00 · 근거 longform/ep/W-1/w1016/script.md·review.md · aitell script 90.0/1,000·17% 통과 · 금지: 숫자·날짜 바꾸기, '수요일 마감'·'월요일부터 수요일까지' 기준 말 빼기, '싸다는 뜻은 아니에요'·'매수·매도 신호 아님' 빼기, 원인(외국인·금리) 넣기, '영수증' · 요청 firemap-youtube-loop 05:18
  착수: firemap-editor 07:05 (정기 06:50)
  완료: firemap-editor 07:08 — 편집 통과 W-1 2화 · 말 36줄 그대로 · 끝맺음 8곳 섞음('~요' 10연속·비율 76% → aitell 25.0→3.3) · 5장 끝 '열 배 넘게 벌어진'(여는 장면과 같은 말)→'이만큼 갈린' · 숫자 0 변경(script 488·say 28개 기계 대조 같음) · 금지 줄 그대로 · script 91.2/1,000·17% 통과 · script.md.edit.json 4aefaaf3 · 원본 .orig · **녹음은 지금 say_v2.txt**(바뀐 말 줄 3·16·18·19·23·27·30·31·33)
- [요청] **firemap-copywriter** ← youtube-loop (05:18) W-1 2화 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/15 13:00 · 근거 longform/ep/W-1/w1016/analysis.md ②(삼성전자주가 1,648.7만·코스피 728.6만·삼성전자자사주 5,510)·compete.md · 방향: '삼성전자 주가' 맨 앞(실험 X-W1-SEARCHFRONT), 숫자 하나(−300만원 또는 '15조 평균값보다 12%') · 금지: '바닥'·'싸다'·'기회'·'폭락'·'이유'(원인 단정), '이번 주'(토요일 공개라 '월~수'), '영수증', 1화 제목 틀('~주주라면 …빠졌다') 반복
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:56 — W-1 2화 제목 1위 **'삼성전자 주가 수요일 종가, 회사가 15조원에 산 자사주 평균값보다 12% 낮았다'**(결선 제미나이 9.2·레드팀 8.2·작성자 8.0 = 8.47, 대본 3번째 줄과 같은 말, 숫자 2개) · 2위 '삼성전자 주가 사흘 −11%, 회사가 15조원에 산 자사주 평균값 아래로' 8.10 · 썸네일 '삼성전자 100주 · 월~수' / 큰 '300만원 줄었다'(−기호는 168px에서 사라짐) · 첫 3초 대본 첫 줄 그대로 · 레드팀이 뺀 말: '지금'(계산은 수요일 종가)·'같은 사흘 미국'(SPY는 나흘)·'비쌌다/낮게 산 날 0일'(싸다를 돌려 말함) · aitell 0.0 · 근거 ep/W-1/w1016/copy/titles.md·review.md
- [요청] **firemap-video-producer** ← youtube-loop (05:18) W-1 2화(10/17 11:30 칸) 녹음 10/15 16:01 창 · 대본 v2.6 say_v2.txt(editor 서명 뒤) · 화면 그림 장면은 script.md (화면:) 줄 · 계산 w1016/calc_out.txt(weekcore 2026-10-16 --cut 2026-10-14 = 확정, 다시 받으면 SPY 769.67 확인) · 합성 표시 판단(실사 생성 장면 없으면 False) · 끝 화면 카드 1화 0yWQeW38UJE · 관문 기한 10/16 11:30
  착수: firemap-video-producer 14:18
  완료: firemap-video-producer 10/15 15:52 — W-1 2화 https://youtu.be/AxTB7izIBUA 10/17 11:30 예약(STATE 10/15 15:52) · 완료 줄 빠져 있던 것 14:18에 채움
- [요청] **firemap-write** ← youtube-loop (05:18) W-1 2화 짝 카페 글 w2cafe1017 (slots 10/17 12:10) 트랙:C · 금요일 10/16 마감까지 넣은 표(한국 10/16 15:30 뒤 weekcore·daum 다시, 미국 10/17 05:00 뒤) · 영상과 다른 칸에 '영상은 수요일 마감 기준' 한 줄 · 자사주 29일 표·CPI 부문 표 재사용 · 금지: 대본 그대로 붙이기·'싸다/바닥'·원인 단정 · 근거 longform/ep/W-1/w1016/
- [자발] **firemap-write** 06:20 회차 — 06:10 칸 minus1015 발행·13:40 칸(기한 07:40)·p1cafe1016 단서 한 줄
  착수: firemap-write 06:20
  완료: firemap-write 06:44 — ① 06:10 minus1015 cafe/277 verify OK 1191/1191·사진 3/3 ② 07:40 칸 intc1015 관문 통과(gates_ok 06:33): '인텔 주가 올라서 생긴 손실? 영업이익 흑자에도 순손실인 이유'(제목 8·표지 K4 8.0·레드팀 2회 틀림 0·editgate auto) → write-b 07:40 발행 ③ 13:40 칸 cpi1015(미국 9월 CPI, 경제 이야기) 관문 통과(06:37, 제목 7.33·표지 7.67) ④ p1cafe1016 c01에 기본연금액 단서 한 줄(youtube-loop 00:51 알림)·재날인 · 카페 비축 0/2(npsage1009는 10/14 발행됨) — 16:40·19:40·22:40 write-b 칸 TBD 남음 · [알림] youtube-loop: w2cafe1017(10/17)이 CPI 표를 쓰면 cpi1015(10/15 13:40)와 겹치지 않게 부문 표만
- [알림] **firemap-video-producer** ← firemap-editor (07:08) W-1 2화 say_v2.txt 편집 통과(edit.json 4aefaaf3) — 16:01 녹음은 이 판으로, 바뀐 말 줄 3·16·18·19·23·27·30·31·33
- [알림] **firemap-write** ← firemap-editor (07:08) p1cafe1016(10/16 12:10) 표본 검수 — c02 '가장 빨리 따라잡아요'(다음 문단과 같은 말) 지움, 숫자 0 변경, frame 통과, editgate 재stamp 9931902c · 발행 그대로
- [알림] **firemap-copywriter·firemap-visual-designer** ← firemap-editor (07:08) 썸네일 AI 티 A30·A31·A33 기계 검사 `py -3.12 work/aitell.py thumb "<큰 글>" …`(걸리면 5) · P-1 thumb_p4e '76.7세부터·80.7세부터' A31 걸림 — thumb-gap ②대로 공개 전엔 안 바꾸고 48h 교체 예비(소수점 없음)에 반영
- 확인(firemap-editor 07:08): 정기 06:50 근무 — 열린 [편집 검수 요청] 2건(W-1 2화 통과·S-1 반려) · auto 표본 2/3(cpi1015 고칠 곳 0·p1cafe1016 고침 1) · ⑦ A30~A33 aitell thumb 모드 · sweep은 다음 근무

- [알림] **firemap-video-producer·firemap-visual-designer** (copywriter 07:56): ① W-1 2화 meta.json title·title_candidates·thumb_text(_swap)는 ep/W-1/w1016/copy/titles.md 그대로 · 설명 첫 줄에 '바닥·매수 신호라는 뜻 아님'(대본 4번째 줄 뜻)을 넣어 제목 오독을 막을 것 · 썸네일 '300만원 줄었다'는 1화 '내 100주' 꼴과 같아 1초 시험 때 1화 썸네일과 나란히 ② C-2 meta 제목 숫자 2개로 바꿈 → bench_check 제목 칸·ytlong gate 다시
- [지시] 이해 시험(쉽게 쓰기) — 사장님 10/15 09:1x "유튜브도 카페도 쉽게 설명해 주고 쉽게 이해되게 써야 할 거 아니야" · ① H-1(11:30 공개) 제목·썸네일·설명 앞 5줄 ② 안 나간 카페 묶음(10/15~16) 제목·대표 이미지·본문 → research/<글>/understand.md ③ 미업로드 롱폼(W-1-2·C-2·H-2·T-1·J-1) 장별·제목·썸네일 → ep/<편>/understand_test.md · 심사관 = 새 Claude '경제 지식 없는 58세' · 담당 firemap-검수
  착수: firemap-검수 09:22
  완료: firemap-검수 09:50 — ① H-1: 제목·썸네일 뜻 맞음, 설명 앞 줄 둘째 줄 이해 못 함 → 쉬운 안 재시험 맞음, PD [요청](공개 예약 안 건드림) ② 카페 10묶음: 9편 쉬운 말로 고쳐 재시험 통과(r1cafe·h1cafe·cpi·m1stot·pencap·g1cafe·sdi·costchk·p1cafe, 제목 3개·표지 2장 포함, editgate auto 재stamp, 숫자 값 변경 0) · jeonse1015는 발행 중이라 기록만(뜻 맞음, 헷갈림 13곳 write에 넘김) ③ 롱폼 5편: W-1 2화 통과(헷갈린 줄 8) · C-2 보류(썸네일 작은 줄·4장 거꾸로 읽힘, 9) · T-1 보류(제목 2위·썸네일 1위 갈림, 대본 8) · H-2 보류(대본 9, 제목·썸네일 후보 없음) · J-1 보류(대본 14, 후보 없음) · 커밋 8dbcec8·c13bccb·3779686 외(푸시 안 함)
- [요청] **firemap-video-producer** ← firemap-검수 (09:26) H-1(rVg0pQVo_wk, 11:30 공개) 설명 앞 줄 쉬운 말로 교체 · 이해 시험: 제목·썸네일 뜻 맞음, **설명 둘째 줄은 58세 심사관이 '무슨 얘기인지 모르겠다'**(1억 1,017만원이 집값인지 평 값인지·중개거래·등기·직거래·호가 등 19개 헷갈림) → 쉬운 안 새 심사관 재시험 뜻 맞음 · 바꿀 앞 줄(숫자는 facts F4·F5 그대로, 문장은 '~쯤'): ① '84㎡ 아파트 한 채 값은 헬리오시티 28억 5천만원쯤, 올림픽파크포레온 28억 2천만원쯤으로 거의 같았습니다. 올림픽파크포레온이 6년 가까이 더 새 아파트인데도 값은 비슷했습니다(국토교통부에 신고된 1년 치 거래 전부로 계산).' ② '헬리오시티는 2026년 2월에 23억 8천만원에 팔린 집이 있었지만, 같은 달 다른 3채는 30억~31억 5천만원에 팔렸습니다. 한 건만 보고 값을 판단하면 안 되는 이유입니다(투자 권유 아님).' ③ 카페 줄 '송파구 가락동·강동구 둔촌동·고덕동 아파트 37곳 값과 역·학교까지 걸어서 몇 m인지 전체 표(카페): {CAFE}' · 평당 1억 1,017/1,087만원·직거래 2건·등기 설명은 출처 칸으로 내림(지우지 않음) · 공개 예약 시각은 그대로(안 건드림) · videos.update는 snippet만 · 근거 longform/ep/H-1/understand_test.md
  착수: firemap-video-producer 10:17
  완료: firemap-video-producer 10:21 — rVg0pQVo_wk 설명 앞 두 줄·카페 줄 요청 문구 그대로 교체(aitell 0.0·'권유 아님' 줄 있음), 옛 숫자(평당 1억 1,087/1,017·25%·23.82억 중개·직거래 2건)는 '계산 가정' 아래 '앞 줄 숫자 자세히:' 한 줄로 내림 · 되읽기 같음 · 제목·태그·publishAt 10/15 11:30 그대로 · 카페 줄은 아직 대문 주소 — h1cafe1015(12:10) 올라가면 글 주소로 바꿔야 함 · 원본 ep/H-1/check/desc_before_1015.json·desc_1015.py
  [알림] **firemap-meeting·firemap-write** ← PD (11:06) 쇼츠 비축 3/4: p1s_step(P-1 '공제 뒤 519만원 넘는 순간 15만원' 계단, 관문 통과 11:05) → 1순위 **10/21 19:20**(07:20 h1s_helio=H-1과 다른 롱폼), P-1 공개(10/16 11:30) 뒤 예약 · 짝 카페 글은 쇼츠 공개 뒤 20:10/22:10 칸, 질문 하나('공제 뒤 519만원 넘으면 연금이 얼마 깎이나' — 0원/15만/27만/46만/50만원, 근거 cardshorts/p1s_step/upload.json·review.md), p1cafe1016 전체 표와 겹치지 않게
  [알림] **firemap-write** ← PD (10:21) h1cafe1015(12:10) 발행 뒤 주소를 slots.json note에 'yt_pair: rVg0pQVo_wk'와 함께 적어 주세요 — 다음 PD 회차가 H-1 설명 카페 줄을 그 주소로 바꿈

## ★ 순돌이 10/15 09:3x — 회원 자료가 가입으로 안 이어짐 (사장님 "카페 가입하면 무료 자료 받게 한 것 잘 하고 있어?")
- 실측: 카페 회원 3명(10/13 자료 발행 전과 같음). 안내 글 264 조회 4(2일). 안내를 건 영상 D-1 106·M-1 19회 — 보는 사람이 적은 영상에만 걸려 있다.
- [지시] **firemap-write**: 264 제목을 쉬운 말로 바꾼다(예: '퇴직 후 건보료 얼마 나올까? 계산 엑셀 무료(카페 회원)'). understand.md 이해 시험 통과 뒤 카페 글 수정. 기한 10/15 18:00.
- [지시] **firemap-meeting / 자료 담당**: 회원 자료 1개를 N-2(10/18, 소득 상위% — 우리 최고 조회 N-1 2,742회의 다시 만들기)에 붙인다. '내 연봉·순자산 상위 몇 % 계산 엑셀'. 공식 통계(국세청 통계연보·통계청 가계금융복지조사) 원문 숫자로만, 검증표 필수. 파일 글 멤버공개 + 쉬운 제목 안내 글. 기한 10/17 21:00. 양도세 엑셀(T-1)은 그다음.
- [지시] **firemap-video-producer**: N-2 설명 앞 5줄·고정 댓글·끝 화면에 이 자료 안내. N-1(420buEFKB8k)에도 같은 안내를 설명 앞 5줄과 고정 댓글로(자료 글이 올라간 뒤).
- [지시] **firemap-meeting**: 매주 월요일 cafemembers.py로 회원 수를 재서 today.md에 남긴다(자료·영상별 증감).
- [요청] **firemap-write** ← firemap-검수 (09:47) 카페 이해 시험 결과 · ① jeonse1015(09:10 칸, 09:21부터 발행 중이라 안 건드림): 뜻은 맞게 읽혔으나 본문 헷갈림 13곳 — 특히 **본문 '용산구 5.6%'가 그림2 표에 없음**, '5.3% vs 12.2% 뭘 믿나', '가운데 값의 가운데 값' → 발행 뒤 고칠지(naverpost rewrite) 판단 · 근거 research/jeonse1015/understand.md ② 9묶음 본문을 쉬운 말로 고치고 editgate auto 재stamp함(r1cafe·h1cafe·cpi·m1stot·pencap·g1cafe·sdi·costchk·p1cafe) — 숫자 값 변경 0 · **제목 3개 바꿈**: pencap '…900만원 다 넣기 전에…'(900만원을 돌려받는 돈으로 오독), sdi '…최고가보다 17% 아래, 배당까지 쉬는 지금 실적'(투자 판단 글로 오독), p1cafe '…당기거나 미루면 받은 돈이 같아지는 나이'(본전=낸 보험료 회수로 오독) · **표지 2장 바꿈**: r1cafe T4(275만원이 세금인지 몰라), p1cafe P6(본전 오독) — 같은 틀·숫자, cover_review.md 끝에 기록 ③ facts에 근거 줄 더할지 판단: costchk(생산자물가 뜻·손실보상=도시정비법 제73조), p1cafe(A값·부양가족연금·일부 연기 제62조①) ④ sdi1015b '발행 전 10/15 종가 재계산·재날인'은 그대로 남아 있음(이번엔 말만 바꿈) · 근거 research/<글>/understand.md
- [요청] **firemap-editor** ← firemap-검수 (09:50) 롱폼 대본 이해 시험(58세 심사관, 장별) 쉬운 말 제안 — 숫자 그대로, 말만 · ① **W-1 2화(16:01 녹음 전)**: 8장 모두 뜻 맞음, 헷갈린 줄 8개(평가액·29일·세 칸·기간 전체·연준·공시를 곱한다 등) 제안 → 녹음 전 반영 여부 판단 · 근거 ep/W-1/w1016/understand_test.md ② **C-2**: 4장 '금융위기 직전, 통장은 1억 밑으로'가 **민수 씨 통장으로 읽힘** → '정우 씨 통장은'(꼭) + 헷갈린 줄 9개 · ep/C-2/understand_test.md ③ **T-1**: 3장 '세금은 해마다 3천만원 넘게 늘어납니다'(매년 낸다로 읽힘) → '한 해 늦게 팔 때마다 수현 씨 세금은…', 6장 '깎이는 돈이 4억이 안 돼서'(1장 5억과 섞임) → '공제로 빼 주는 돈이' + 6개 · ep/T-1/understand_test.md ④ **H-2**: 4장 '네 건뿐'·'열한 건 모두'·'18억 차이' 어느 단지인지 갈림(꼭) + 8개 · ep/H-2/understand_test.md ⑤ **J-1**: 6장 '9월 확정안'이 '이미 정해짐'으로 읽힘 → '9월 국무회의에서 정한 정부안(국회 통과 전)'(꼭) + 13개 · ep/J-1/understand_test.md · 반영 뒤 그 줄만 다시 시험(검수)
  착수: firemap-editor 17:05 (정기 16:50)
  완료: firemap-editor 17:10 — ① W-1 2화 14:54 판단 그대로(반영 0) ② C-2 말 9줄 반영(4장 '정우 씨 통장은' 꼭 포함, 8장은 calc 1998~2002 다섯 명이라 '정우 씨와 그 뒤 네 해 사이'), 녹음 다시 say_v2 2·10·20·28·37·40·52·58·66줄 ③ T-1은 youtube-loop 16:44 반영분 재서명 ④ H-2 꼭 고칠 4장: '래미안원베일리에선 같은 달에 18억'·'그달 열한 건'(검수 제안 '한 해 거래 열한 건'은 사실과 달라 안 씀, 11건=2026.05) + 8곳, 재사용 줄 예고·본편 같이, 말 54→56줄 ⑤ J-1 '9월 확정안'→'9월 국무회의에서 정한 정부안'(장 제목·화면·자막 포함) + 14곳, 첫 서명 · 숫자 값 0 변경(전 편 숫자 목록 기계 대조, 새 글자는 반올림·자막에 있던 값뿐) · aitell C-2 0.0·H-2 10.4→6.1·J-1 4.3, script 밀도 전부 통과 · 각 script.md.edit.json, 원본 .orig1015 · 재시험(그 줄만)은 검수 몫
- [요청] **firemap-copywriter·firemap-visual-designer** ← firemap-검수 (09:50) 롱폼 제목·썸네일 이해 시험 · ① **C-2 썸네일 작은 줄 '1998년 시작은 바닥'** → 58세 심사관이 '1998년에 주가 바닥(제일 쌀 때) 들어가 잘됐다'로 **거꾸로 읽음**(사실: 1998년 시작 통장이 2011년에 바닥남) → '1998년 시작 통장은 바닥남 · 2003년은 2.7억 남음' 같은 말로 · 제목 1위 '같은 규칙'(넣는? 꺼내는?) 제안 '매달 같은 돈을 꺼낸' ② **T-1 제목 2위** '…열두 배 가까이 차이' → 세금인지 공제인지 모름 → '…양도세 열두 배 가까이 차이' · **썸네일 1위** '거주 2년이면 / 양도세 공제 48%→16%' → 손해 방향이 안 보임('2년 살면 혜택?') → '2년만 살았으면' 또는 세금 쪽 숫자 한 줄 · 썸네일 2위·제목 1위는 뜻 맞음 ③ W-1 2화 제목 1·2위·썸네일 글자 뜻 맞음(설명 첫 줄 '싸다는 뜻 아님'은 그대로 필요) ④ H-2·J-1은 제목·썸네일 후보가 없어 시험 못 함 — 나오면 검수에 알림 · 근거 각 ep/<편>/understand_test.md
  착수: firemap-copywriter 18:55
  완료: firemap-copywriter 18:59 — 이해 시험 반영(58세 새 심사관 1명 항목별·레드팀 채점, 뜻 틀림 0) · **C-2** 제목 1위 'S&P500 퇴직금 3억, 매달 같은 돈을 꺼낸 두 통장을 가른 건 시작한 해였다'(레드팀 6→7, 숫자 2개) · 썸네일 큰 글 **'같은 3억, 시작만 5년 차이'**('5년 더 버팀' 오독 막음, 5→7 · visual 17:20 요청 답) · meta.json 바꿈(옛 title_prev_1015b) · **T-1** 제목 2위 '…양도세 열두 배 가까이 차이'(6→7) · 썸네일 1위 **'2년만 살았으면 / 양도세 공제 48%→16%로 줄어'**(58세 방향 맞음, 레드팀 6 — 1초 시험에서 '양도세가 줄어' 오독 나오면 2위 '거주 10년 vs 2년 / 양도세 약 12배'를 1위로) · '양도세 1.8배'는 비교 대상 몰라 뺌 · T-1 understand_test 판정: 통과 · aitell 0.0 · 근거 ep/C-2·T-1/copy/titles.md 끝
완료: firemap-write-b 10:52 — 10:40 r1cafe_tax1015 https://cafe.naver.com/firemap/280 verify OK 1927/1927자·사진 3/3(게시판 연금/세금/보험) · 끝에 양도세 계산기 줄(firemap.kr/tax, utm r1cafe_tax1015) 넣고 관문 재통과 · [알림] firemap-video-producer: 쇼츠 r1s_spytax(ez-tLgkdZfI) 설명 앞 5줄 카페 주소를 https://cafe.naver.com/firemap/280 로
- [자기 배정] firemap-motion-designer W-1 2화(10/17) 모션 설계표 + 2장 자사주 29일 막대 부품
  착수: firemap-motion-designer 11:28
  완료: firemap-motion-designer 10/15 11:40 (이 줄은 위 670줄 [지시·긴급] 밑에 적힘 — 10/16 11:49 표시만)
- [자발] **firemap-write** 12:21 회차 — 12:10 칸 h1cafe1015(H-1 짝) 발행·264 제목 지시
  착수: firemap-write 12:21
완료: firemap-write 12:35 — ① 12:10 h1cafe1015 https://cafe.naver.com/firemap/281 verify OK 2221/2221자·사진 4/4(게시판 부동산) · H-1 rVg0pQVo_wk public 확인 뒤 발행, 짝 글 규칙대로 c00 끝에 영상 링크 한 줄 더하고 editgate 재stamp · slots 12:10 note에 yt_pair: rVg0pQVo_wk·281 적음 → [알림] firemap-video-producer: H-1 설명 카페 줄을 https://cafe.naver.com/firemap/281 로 ② [지시] 264 제목 바꿈(기한 18:00): '이자·배당 1년 2천만원 넘으면 세금·건보료 얼마? 계산 엑셀, 카페 가입하면 무료' — 58세 이해 시험 2회(옛 제목 '종합과세' 모름·무료 안 보임 → 새 제목 뜻 맞음) finguide1013/understand.md 판정 통과 · rewrite 뒤 verify OK 1097자·사진 3/3, 본문 변경 0 ③ 검수 요청 ① jeonse1015 '용산구 5.6%'는 facts 12번에 있는 숫자(그림2에 없을 뿐) — 틀린 숫자 아니라 279 rewrite 안 함 · 카페 비축 실제 0/2(npsage1009는 10/14 발행됐는데 reserve 목록에 남아 있음) — 오늘 16:40·22:40 write-b TBD
- [자발] X-1 환율(10/22 칸) 이해 시험 — 사장님 10/15 '쉽게' 지시, X-1만 understand_test 없음 트랙:C · 담당 firemap-youtube-loop · 근거 longform/ep/X-1/understand_test.md
  착수: firemap-youtube-loop 12:44
  완료: firemap-youtube-loop 12:52 — 58세 심사관 새 Claude 6명(제목·썸네일·대본 장별, 고친 뒤 2·3차): **뜻 틀림 0**, 헷갈린 곳 고침 — 말 16줄(숫자 값 0 변경·반올림만): '7%포인트'→'1억으로 치면 700만원 가까이'·매매기준율 풀이·엔화 비교를 '96만원쯤→85만원쯤'·달러도 '155만원쯤→134만원쯤'·4장 끝 '실제 남는 돈은 조금 더 적다'·S&P500/나스닥100 한 줄 풀이 · aitell script(say) 90.7·19% 통과·aitell 3.4 · 판정: 통과 · 옛 서명본 script.v2.signed_1014.md · ytreach 다시 받음: 10/13 이후 파일 여전히 없음(⑥ 기한 10/16 23:00)
- [편집 검수 요청] X-1 script.md·say_v2.txt 재서명(이해 시험 반영, 바뀐 말 16줄만 — diff script.v2.signed_1014.md) 트랙:C · 담당 firemap-editor · 시한 10/19 12:00(10/22 11:30 칸, 관문 10/21 11:30, 녹음 전) · 근거 longform/ep/X-1/understand_test.md · 금지: 숫자·날짜 바꾸기, 쉬운 풀이('기준 환율'·'1억으로 치면'·'96만원쯤→85만원쯤') 되돌리기 · 요청 firemap-youtube-loop 12:52
  착수: firemap-editor 17:05 (정기 16:50)
  완료: firemap-editor 17:10 확인 — 15:10 재서명분(sha cedadc8f…·say fa2d8f34…) 지금 파일과 같음, 다시 볼 것 없음
  더함: firemap-youtube-loop 12:50 — 화면 자막 2줄도 같이(diff script.md.orig1016): 2장 '2026년 최저는 10.13 1,335.8원' 뺌 · 5장 엔화 '최저는 다음 날 10.13 842.3원' · 말 바뀐 것 없음
- [요청] **firemap-copywriter·firemap-visual-designer** ← youtube-loop (12:52) X-1 이해 시험 결과(막지 않음) · 제목 1위 '1억을 바꾼 날'은 무엇을 무엇으로 바꾼지 모름 → '1억을 달러로 바꾼 날' 제안, 58세 심사관은 2위('9천만원 아래')가 더 와닿는다 · 썸네일 B(swap) '네 날 중 하나' 뜻 모름 → '달러 가장 비쌀 때 산 경우'로 · 썸네일 A '· 원화' → '· 원화로 따지면' · 시한 10/20 12:00 · 근거 longform/ep/X-1/understand_test.md
  착수: firemap-copywriter 18:55
  완료: firemap-copywriter 18:59 — X-1 제목 1위 '…1억을 **달러로** 바꾼 날 네 개로 계산'(레드팀 6→7) · 1·2위 순서 유지(2위는 숫자 4개라 ytlong 막힘) · 썸네일 A 작은 줄 '· 원화로 따지면' · B 작은 줄 **'2024년 이후 달러가 가장 비싸던 7월 2일에 산 경우'**(레드팀: 기간 없는 '가장'은 과장 → facts F1 '2024년 이후 최고') · 58세 뜻 맞음 · 근거 ep/X-1/copy/titles.md 끝·understand_test.md
  [알림] **firemap-visual-designer** (copywriter 18:59): C-2 9차 큰 글 '같은 3억, 시작만 5년 차이'(작은 줄 c2w 카드 그대로) · T-1 썸네일 1위 '2년만 살았으면 / 양도세 공제 48%→16%로 줄어'·작은 줄 '정부안 · 2029년 · 20억 집 팔 때' — 1초 시험에 '세금이 늘어나나 줄어드나' 질문 넣고 '줄어'를 세금으로 읽으면 2위를 1위로 · X-1 B 작은 줄 '2024년 이후 달러가 가장 비싸던 7월 2일에 산 경우', A 끝 '· 원화로 따지면'
  착수: firemap-visual-designer 09:04 — C-2 썸네일 9차: 큰 글 '같은 3억, 시작만 5년 차이'·해 글씨 키움·도장 막대 옆(레드팀 8차)
  완료(미달): firemap-visual-designer 09:17 — C-2 썸네일 10~13차 9판(큰 글 '같은 3억, 시작만 5년 차이' 반영) **세 명 평균 8 넘은 판 없음** · 후보 longform/ep/C-2/thumb_c3b.png(7.47→7.10→6.93, 13차 레드팀 '사물 0' 반려)·thumb_c3e.png(펼친 통장 모양, 7.03) · 10차 c2y 7.70은 다음 차수 6.70 · 1초 블라인드 매 차수 3/3, '5년 더 버팀' 오독 0 · 진한 판 c3a·노란 크림 c3c·카드 없앤 c3d 반려 · 막힌 곳 = Claude 독자 6.2~6.8('정보판·작은 줄 많음') → 14차는 글자 줄 6→4·굵은 제본선 · meta thumb 비움(thumb_status 갱신) · 사실 틀림 0·aitell 통과·가려짐 0 · 근거 visual/C-2-thumb/judges.md 10~13차 · 기한 10/17 06:00 그대로
  착수: firemap-visual-designer 17:05 — C-2 썸네일 14차: 글자 줄 6→4·구멍 빼고 제본선·실물 통장 사진 바탕 시안(제미나이 이미지)
  완료(미달): firemap-visual-designer 17:15 — C-2 썸네일 14~16차 8판 **세 명 평균 8 넘은 판 없음** · 최고 longform/ep/C-2/thumb_c3j.png 16차 7.63(제미나이 8.5·Claude 7·레드팀 7.4: 위 띠를 남색 띠 흰 글 72px로·큰 글 한 줄·구멍 뺌·잔고 막대 유지) · 예비 thumb_c3l.png 7.43 · 1초 블라인드 매 차수 3/3 · 쌓인 쪽 두께·제본선은 168px에서 안 보임, 나무 책상 진한 판 c3h·c3k는 레드팀 경쟁 유사 3 반려 · 제미나이 이미지 3종 429라 실물 통장 사진 못 시험 · 사실 틀림 0·가려짐 0·아래 5% 비움 · meta thumb 비움(thumb_status 갱신) · 근거 visual/C-2-thumb/judges.md 14~16차
  [요청] **firemap-copywriter** ← visual-designer (17:15) C-2 썸네일 남은 막힘 2개는 문구 몫 — ① 도장 '통장 바닥남'이 168px에서 0원으로 읽힘(레드팀 14~16차 매번, 실제 1,154만원 남음): 레드팀 제안 '1년 치 못 꺼냄' 또는 '1,154만원 남음'(큰 글로, 오른쪽 '2억 7천 남음'과 짝) 중 판단 ② 정체성 1종(실제 결과 숫자)뿐 — 둘째 종류(예: 계산기 표시 짧은 꼬리표) 넣을지 · 글자 줄은 늘리지 말 것 · 기한 10/16 23:00(썸네일 기한 10/17 06:00) · 근거 visual/C-2-thumb/judges.md 16차·판정
  착수: firemap-copywriter 18:45
  완료: firemap-copywriter 19:02 — C-2 왼쪽 칸 **'1998년 시작 통장 → 1년 쓸 돈 모자람'**(오른쪽 '2003년 시작 → 2억 7천 남음' 그대로) · 레드팀 '통장 바닥남' 5·'1,154만원 남음' 5(2011년 값과 2025년 말 값 시점 오독)·'1년 치 못 꺼냄' 6.5·'14년째 돈 모자람' 6·**'1년 쓸 돈 모자람' 8** · 58세 두 명: '못 꺼냄'=은행이 막았나, '모자람'=0원·출금 막힘 오독 없음(다만 '별일 아님'으로 읽음 → 잔고 빈 막대로 받칠 것) · 정체성 둘째 종류는 썸네일에 안 넣음(편 전체로 원문·계산기 2종, 넣는다면 결과 칸 테두리만 계산기 창 모양) · meta.json thumb_text_small 바꿈(옛 _prev_1016) · 근거 ep/C-2/copy/titles.md 끝
- [수리] 카페 글 유튜브 주소 조각(tps·://y·ou) — 사장님 13:4x 질문, 원인 재현·입력 고치기·verify 검사 추가·나간 글(208·257·265·269·276·281 등) 조각만 지우기 트랙:카페 · 담당 카페 발행 도구 · 근거 work/naverpost.py
  착수: 카페 발행 도구 13:51
- [편집 검수 요청] W-1 2화 화면 글자(screen_text.txt 409줄, sha는 lfrender text) + 이해 시험 제안 8줄(16:01 녹음 전 판단 요청 09:50 — 녹음은 v2.6 서명본으로 먼저 함, 반영하면 그 줄만 Chirp 다시) 트랙:C · 담당 firemap-editor · 시한 10/16 06:00(관문 10/16 11:30, 렌더 3시간 전) · 근거 longform/ep/W-1/w1016/screen_text.txt·understand_test.md · 화면: video/src/W1016.tsx(1화 W1 틀) + w1016props.py · 요청 firemap-video-producer 14:49
  완료: firemap-editor 14:54 — 화면 글자 서명(screen_text.edit.json sha 88e71f75…) · 고친 것: 출처 중복('한국은행 ECOS 원달러 매매기준율' 두 번) 3장면(ratio·trio·rates)·끝 장면 '출처 전망·투자 권유 아님'(면책이 출처 칸에, 한 화면 3번) 제거 — w1016props.py만, 숫자 0 변경 · 이해 시험 제안 8줄 반영 0(심사관 8장 모두 뜻 맞음·숫자 칸과 화면 날짜가 같이 나옴·7장은 면책 줄) → 다시 녹음 없음, script.md 서명 4aefaaf3 그대로
- [요청] **firemap-visual-designer** ← PD (14:50) W-1 2화 썸네일 + 1초 시험(168px, 심사 3명, 경쟁 상위 5 비교판, 1화 thumb_w1l과 나란히) 트랙:C · 시한 10/16 08:00(관문 10/16 11:30) · 문구 copy/titles.md 그대로(앞줄 '삼성전자 100주 · 월~수' / 큰 '300만원 줄었다', 예비 swap) · 오른쪽 아래 길이 자리 비움 · 결과 ep/W-1/w1016/thumb_w2*.png + judges.md 판정 → meta.json thumb는 PD가 적음
  완료: firemap-visual-designer 15:37 — 쓸 것 ep/W-1/w1016/thumb_w2c.png('삼성전자 100주 / −300만원 / 월~수 사흘', swap 문구) · 1초 시험 3/3 맞힘 · 평균 7.87(제미나이 3-flash 8.5·Claude 7.7·레드팀 7.4) → 통과선 8 미달 0.13 · 예비 thumb_w2a.png(카피 1위 원문, 7.33) · 비교판 thumb_w2_compare.png · 기록 judges.md · meta thumb는 PD가
  완료: firemap-visual-designer 15:50 — 2·3차(PD 요청) 끝: 최고안 ep/W-1/w1016/thumb_w2f.png('삼성전자 100주 / 지난주 −140만원 / 월~수 −300만원') 평균 7.47(제미나이 3-flash 7.5·Claude 7.6·레드팀 7.3) → 판정 미달(8 못 넘음) · 문구가 titles.md에 없어 **copywriter 승인 필요**, 안 나면 thumb_w2a.png(카피 원문, 3차수 7.23~7.33) · w2e(코스피 −93만)는 원금 다른 비교 3배 착시로 레드팀 반려 · judges.md 갱신
  완료: 카페 발행 도구 14:57 — 원인: 주소 줄 Enter 뒤 링크 카드가 1~4초 늦게 붙는 사이 다음 글을 계속 쳐서 주소 문단이 맨 끝으로 밀리고, 이어 쓰기 클릭(문단 왼쪽 20px=두세 글자 뒤)이 그 안에 새 글을 끼워 주소가 2~4자씩 잘려 흩어짐(카드 응답 4초 지연으로 281과 같은 조각 재현). 화면 글자 수는 같아 verify OK로 나갔음 · 고침(161262f): 주소 줄 뒤 카드 다 붙을 때까지 대기+끝 문단 다시 잡기, 클릭 뒤 End, verify_body가 편집기 저장 문서로 주소 검사(잘린 링크·빠진 주소·붙은 줄·조각 → 등록 안 함), 블로그도 같은 함수 · 같은 지연 재현에서 조각 0·원고와 문단 100% 일치(281·280 묶음) · 나간 글 9편 수정(208·233·257·265·269·276·281 조각, 265·274·280 주소 줄이 다음 줄과 붙음) → API 재확인 전부 주소 문제 0·원고 일치·공개 설정 그대로 · 재점검 work/cafe_urlfix.py scan, 원본 백업 research/_cafe_edit/<번호>/urlfix_*
- [요청] **firemap-write** ← PD (15:01) 쇼츠 짝 카페 글 1편 · h1s_helio https://youtu.be/XB9fAhJrxFA (10/21 07:20 예약) 질문 '헬리오시티 84㎡ 20억 직거래, 같은 달 가운데 값은?' — 표: 5월 26층 20.00억 직거래 vs 같은 달 17건 가운데 28.10억 · 2월 23.82억 vs 31.50억 · 달별 가운데 값(재료 cardshorts/h1s_helio/review.md·upload.json 설명) · 원본 롱폼 https://youtu.be/rVg0pQVo_wk · H-1 짝 긴 글 281과 겹치지 않게 · 칸은 회의가 10/21 쇼츠 공개 뒤
- [알림] **firemap-write** ← PD (15:01) H-1 rVg0pQVo_wk 설명 카페 줄 → https://cafe.naver.com/firemap/281 바꿈(되읽기 확인) · 첫 댓글 달림(37곳 20·10·7, 281 주소) · r1s_spytax ez-tLgkdZfI 설명엔 카페 줄이 원래 없어 새 줄은 안 넣음(공개된 쇼츠에 새 문구 추가 안 함)

- [배차] **firemap-write** 10/16 07:40 카페 TBD 칸(관문 기한 10/16 01:40) 편 정해 관문 통과 + 카페 비축 0/2(npsage1009는 10/14 발행됨) 채우기 · 22:40 칸은 write 15:1x 정기 몫 · 운영실장 15:08
  착수: firemap-write 15:08 (운영실장)
  완료(부분): firemap-write 15:28 — 07:40 칸에 r1s_startday 짝 글 r1cafe_start1016 배정, 원고·표지·그림·교차검증·레드팀 4회·58세 이해 시험 4회까지. 제목·표지 6~7점·본문 이해 시험 심각 5건 남아 gates_ok 못 적음(근거 research/r1cafe_start1016/review.md, 다음 회차 첫 일). reserve.cafe의 발행 끝난 npsage1009 정리(카페 비축 0/2 그대로). 22:40 칸 안 건드림 · 커밋 9b12c53
- 막힘(운영실장 15:29): 10/16 07:40 카페 칸 r1cafe_start1016(r1s_startday 짝) 관문 미달 — 제목 레드팀 6·표지 7·58세 이해 시험 뜻 틀릴 곳 5건(9b12c53, 남은 것 r1cafe_start1016/review.md), 관문 기한 10/16 01:40 → write 18:1x·21:1x 정기 1순위 · 카페 비축 실제 0/2(npsage1009 목록 정리됨) · 22:40·10/16 10:40 이후 TBD 칸 그대로
  완료: firemap-video-producer 15:52 — W-1 2화 https://youtu.be/AxTB7izIBUA 10/17 11:30 예약(slots gates_ok) · Chirp 36줄(쉼 태그 첫 적용)·editor 화면 서명·렌더 관문 전부·점수표 35·썸네일 w2a · [알림] firemap-write: w2cafe1017 영상 주소 = AxTB7izIBUA · [알림] firemap-copywriter: 썸네일 w2f('지난주 −140만원 / 월~수 −300만원', visual 3차 7.47) 48h 교체 후보 승인 여부
  답: firemap-copywriter 07:59 — w2f **승인 안 함**: 작은 줄 '지난주 −140만원'은 2화 낭독에 없는 숫자(2화는 '지난주 5% 남짓'·'두 주 142만원')라 영상에 없는 숫자, '−' 기호는 168px에서 사라짐(교본 10/15). 48h 교체는 이미 심사 받은 **thumb_w2c.png**(7.87·1초 3/3)로 — 노출 100회 넘고 CTR이 중앙값 아래일 때만
- [지시] **firemap-write** ← 사장님 (10/15) cafe/281(강남·송파 손품 37곳) 칸 많은 표가 휴대폰에서 이해 안 됨 → '표 대신 한눈에 보기' 꼴로 고쳐 쓰기(pkg_v2·이해 시험·281 수정·slots note)
  착수: firemap-write 16:30

- [자발] **firemap-write-b** 16:43 회차 — 16:40 칸 TBD(비축 0) 새 글 편성·관문·발행
  착수: firemap-write-b 16:43
- [자발] T-1 양도세(10/21 칸) 대본 이해 시험 보류분 고치기·재시험 트랙:C · 담당 firemap-youtube-loop · 근거 longform/ep/T-1/understand_test.md
  착수: firemap-youtube-loop 16:37
  완료: firemap-youtube-loop 16:44 — script.md v3.1·say_v3.txt 말 26줄 쉬운 말로(숫자 값 0 변경) · 58세 새 심사관 2·3차 **뜻 틀림 0/9장** · 1차 제안 그대로 넣으면 aitell 숫자 밀도 121(기준 92)로 실패 → 숫자 대신 말로 풂('같은 비율만큼만'·'두 공제를 다 채워'·'아무리 커도 10억까지'), 최종 90.4·16% 통과, aitell 1.4 · 판정 보류는 제목 2위·썸네일 1위(copywriter·visual, 09:50 [요청]) 몫만 남음 · ⑥ ytreach 16:3x 다시 받음: 새 보고서 여전히 없음(마지막 10/12)
- [편집 검수 요청] T-1 script.md·say_v3.txt 재서명(이해 시험 반영, 바뀐 말 26줄만 — diff script.v3.signed_1014.md) 트랙:C · 담당 firemap-editor · 시한 10/18 12:00(10/21 11:30 칸, 관문 10/20 11:30, 녹음 전) · 근거 longform/ep/T-1/understand_test.md · aitell script 90.4·16%(숫자 밀도 기준선 가까움 — 숫자 넣는 고침 금지) · 금지: 숫자·연도 바꾸기, '정부안'·'국회 통과 전'·'가상 인물' 빼기, '8억에 샀으니'·'같은 비율만큼만'·'10년을 넘지 않는다면' 되돌리기 · 요청 firemap-youtube-loop 16:44
  착수: firemap-editor 17:05 (정기 16:50)
  완료: firemap-editor 17:10 — 재서명 통과(script.md.edit.json e48ee894) · 바뀐 26줄 줄마다 봄, 편집자 2곳: 5장 '언제 팔아도'→'네 해 중 언제 팔아도'(표가 2026~2029뿐) · 1장 '12억이고요'→'12억입니다'(~요 5연속 끊기) · 숫자 목록 기계 대조 동일 · 금지 줄 그대로 · aitell 1.4→0.0 · script 89.2/1,000·13% · 녹음은 say_v3.txt(바뀐 줄 11·40 더해짐) · 참고: 8장 '4%씩'은 %p 뜻, 자막 32%p가 받침
- 완료: 순돌이 10/15 16:5x — cafe/281 '한눈에 보기' 판으로 수정(naverpost rewrite), 확인: 제목·전체공개·게시판·사진 7/7·주소 문제 0·문단 69/69 일치. 이해 시험 4회차 understand_v2.md.

- [알림] **firemap-youtube-loop·firemap-video-producer** ← firemap-editor (17:10) 이해 시험 반영 서명 4편 — C-2 녹음 다시 say_v2 9줄(2·10·20·28·37·40·52·58·66) · H-2 say_v2 56줄(바뀐 줄 3·4·10·11·12·17·20·23·26·34·35·37·38·45·49·55, 재사용 예고 줄 같이) · J-1 say_v3 첫 서명(아직 녹음 전) · T-1 say_v3 · 검수에 그 줄만 재시험 부탁 · J-1 남은 판단(youtube-loop): 0장 '내년 고지서부터'(2027)와 '2028년' 숫자를 한 말로 이을지
  착수: firemap-youtube-loop 00:43 — J-1 0장 2027·2028 이을지 판단
  완료: firemap-youtube-loop 00:47 — J-1 0장 '내년 고지서부터'(2027) 뒤 한 줄로 이음: '앞에서 2028년을 든 건, 오래 가진 집에 주던 세금 할인이 내년엔 일부만 바뀌고 2028년에 다 바뀌어서예요.'(안 §9⑧ 자막과 맞음, 숫자 값 0 변경) · 58세 새 심사관 2회(1차 '할인 규칙' 어려움 → 고침, 2차 뜻 맞음) 판정 통과 · aitell 4.2 · 원본 .orig1016 · 근거 longform/ep/J-1/understand_test.md
- [편집 검수 요청] J-1 script.md·say_v3.txt 재서명(0장 1줄 추가만, diff script.md.orig1016) 트랙:C · 담당 firemap-editor · 시한 10/19 12:00(10/22 11:30 칸, 녹음 전) · 근거 longform/ep/J-1/understand_test.md · 금지: 연도 바꾸기, '일부만'·'다 바뀌어서' 빼기 · 요청 firemap-youtube-loop 00:47
  착수: firemap-editor 07:04 (정기 06:50)
  완료: firemap-editor 07:09 — 재서명 통과(script.md.edit.json, sha 279d9543) · 0장 추가 1줄 그대로(앞 '내년 고지서부터'와 '2028년' 사이 빈칸 메움, '일부만'·'다 바뀌어서' 그대로) · 편집자 고침 0 · 숫자 값 0 변경 · aitell 4.2 · script 73.0/1,000·14% 통과 · 녹음은 say_v3.txt(8줄 추가)
- [자발] 10/16 매일 연구 트랙:C · 담당 firemap-youtube-loop
  완료: firemap-youtube-loop 00:47 — study/2026-10-16.md · **H-1 롱폼 13.2h 57회 — 첫날 한 자릿수 7연속 깨짐**(단지 이름 제목) · 쇼츠 금 lfUqV4YpwGM 5.4h 1,021(최고 속도) · 구독 58 · ytreach 새 보고서 없음(10/13까지) · 경쟁 '큰 돈=매달 얼마' 틀(퇴직금 1억=연금 50만원 13.9배)·건보료 3주째·월배당 ETF 10.5배 · RULES 관찰 1줄
- 확인(firemap-editor 17:10): 정기 16:50 근무 — 열린 [편집 검수 요청] 2건(X-1 확인·T-1 통과) + 검수 09:50 [요청](C-2·H-2·J-1 반영) · auto 표본·sweep은 다음 근무  완료: firemap-write-b 17:11 — 16:40 칸 bankdiv1015 https://cafe.naver.com/firemap/284 verify OK 1616/1616자·사진 3/3(게시판 배당주) · 코스피 -7.57% 날 은행 지주 5곳 1천만원 배당(작년 배당 기준) · 레드팀이 우리금융지주 감액배당 비과세 잡아 세후 예시 하나금융으로 · 22:40 write-b 칸 TBD 남음
- [자발] **firemap-write** 18:16 회차 — 18:10 칸 pencap1015 발행·10/16 07:40 r1cafe_start1016 관문(기한 01:40)
  착수: firemap-write 18:16
- [편집 검수 요청] C-2 화면 글자 재서명(lfrender text 18:21) 트랙:C · 담당 firemap-editor · 시한 10/17 11:30(관문 10/18 11:30) · 근거 longform/ep/C-2/screen_text.txt — 바뀐 곳 9줄뿐이고 전부 editor 17:08 서명한 script.md 말 줄(2·10·20·28·37·40·52·58·66)과 같은 글자(자막). 숫자 0 변경 · 9줄 Chirp 다시 녹음 check 통과(튀는 줄 0·앞뒤 +1.3%·IQR 0.16·받아쓰기 숫자 0) · c2props 숫자 대조 통과 294.3초
  완료: firemap-editor 18:22 — 화면 글자 재서명 통과(stamp 01cbede5) · 바뀐 자막 9줄 script.md 말 줄과 글자 동일 · 숫자 값 0 변경(새 글자 '500곳'·'1월'은 S&P500 이름·data.year 2001년 1월과 맞음) · aitell 6.6 전후 같음 · lfrender check 편집 통과·관문 통과
  추가 요청(PD, 58세 재시험 18:3x) 완료: firemap-editor 18:24 — script.md·say_v2.txt 2줄 고치고 script 재서명(script.md.edit.json cfd40ac5, 원본 .orig1015b) · 3장 끝 '꺼내 쓴 돈은…'→'다섯 해 동안 꺼내 쓴 돈은…'(calc_n1_out 1998~2002 5회×2,400만=1.2억, 3.00→1.60억) · 4장 '그 뒤 네 해는…'→'정우 씨에겐 그 뒤 네 해 동안…'(민수 씨로 읽힘 막기) · 숫자 값 0 변경 · aitell 0.9 · script 82.9/1,000·19% 통과 · 녹음 다시 say_v2 28·34줄 · 화면 글자 stamp(18:22)는 그대로, PD가 다시 녹음·c2props·lfrender text 뒤 재요청
  완료: firemap-editor 18:25 — C-2 화면 글자 재서명 통과(2줄 다시 녹음 뒤) · 바뀐 자막 2줄(scenes.14.lines.1·scenes.18.lines.0) 18:23 서명 script.md와 글자 같음 · data 줄 변경 0·숫자 값 0 변경 · 자막 전 줄이 script.md에 있음 · aitell 6.6 · lfrender check 편집 통과·관문 통과
  추가 요청(PD, 58세 2차 재시험) 완료: firemap-editor 18:26 — 4장 1줄 고치고 script 재서명(원본 .orig1015c) · '그걸로는 해마다 꺼내는 2,400만원을 메울 수 없었죠.'→'그 정도로는 정우 씨가 해마다 꺼내는 2,400만원을 메울 수 없었어요.'(민수 씨로 읽힘 막기, 앞줄 '6%대였죠'와 -죠 연속 끊기) · 숫자 값 0 변경 · aitell 0.9 · script 82.1/1,000·19% 통과 · 녹음 다시 say_v2 35줄 · 화면 글자 stamp(18:25)는 그대로, PD 다시 녹음·text 뒤 재요청
  완료: firemap-editor 18:27 — C-2 화면 글자 재서명 통과(35줄 다시 녹음 뒤) · 바뀐 자막 1줄(scenes.18.lines.1) 18:26 서명 script.md와 글자 같음 · data 줄 변경 0·숫자 값 0 변경 · 자막 전 줄이 script.md에 있음 · aitell 6.6 · lfrender check 편집 통과·관문 통과
- [자발] **firemap-write-b** 19:42 회차 — 19:40 칸 g1cafe_paths1015(g1s_paths 짝) 발행
  착수: firemap-write-b 19:42
  완료: firemap-write-b 19:47 — 19:40 g1cafe_paths1015 https://cafe.naver.com/firemap/285 verify OK 1425/1425자·사진 3/3(게시판 돈 관리) · 쇼츠 lfUqV4YpwGM·본편 xBTZtRp5lMs public 확인 뒤 발행 · 발행기 경고: 오늘 제목 끝말 '얼마' 5칸째(다음 칸부터 다른 끝말) · [알림] firemap-video-producer: 쇼츠 g1s_paths(lfUqV4YpwGM) 설명 앞 5줄 카페 주소를 https://cafe.naver.com/firemap/285 로 · 22:40 write-b 칸 TBD 남음
- [알림] **firemap-video-producer** ← firemap-write-b (19:47) 쇼츠 g1s_paths lfUqV4YpwGM 설명 앞 5줄 카페 주소 → https://cafe.naver.com/firemap/285
- [편집 검수 요청] S-1 script.md v2.3(이해 시험 반영, 말 18줄) 트랙:C · 담당 firemap-editor · 시한 10/20 12:00 · 근거 longform/ep/S-1/understand_test.md·say_v2.txt (옛 서명본 script.v2.2.signed_1015.md) · 숫자 값 0 변경 · aitell script 78.8·14% 통과 · 끝 질문(숫자 먼저 vs 주가 먼저)이 갑작스럽다는 심사관 지적은 editor 판단 (youtube-loop 20:48)
  착수: firemap-editor 07:04 (정기 06:50)
  완료: firemap-editor 07:09 — 편집 통과(script.md.edit.json, sha ff564676) · 바뀐 18줄 calc 대조(절반 넘는 19번=31 중 19·그대로 1·2017.7.7 첫 기록·43번 중 25번 맞음) · 편집자 3곳: 1장 '아홉 번 가운데' 두 줄 연속 → 둘째 줄 '그날 주가가 오른 한 번은' · 3장 '드물긴 해도 아주 드문 일은 아니라는'→'흔하진 않아도, 우연으로 충분히 나올 수 있다는' · **끝 질문은 정리 바로 뒤로 올림**('발표된 숫자'→'이익 숫자'), 맨 끝은 카페 표 안내 하나 · 숫자 값 0 변경 · aitell 1.7 · script 82.7/1,000·10% 통과 · 녹음은 say_v2.txt(바뀐 줄 9·23, 45·46 순서) · 원본 .orig1016 · 바뀐 3곳 이해 재시험은 youtube-loop 판단
- [자발] **firemap-write-b** 22:43 회차 — 22:40 칸 TBD(비축 0) 장르 보험·정책 새 편 편성·관문·발행
  착수: firemap-write-b 22:42
  완료: firemap-write-b 23:20 — 22:40 silson1015 https://cafe.naver.com/firemap/287 verify OK 1703/1703자·사진 3/3(게시판 연금/세금/보험) · 5세대 실손·초기 실손 11월 할인(금융위 원문) · 레드팀 틀림 0·58세 이해 2회 통과·제목 7.0·표지 7.67 · 관련 영상 없음
- [지시] **firemap-write** (기한 10/16 04:40 — 10:40 칸 관문 6시간 전) 10/16 10:40 카페 TBD 칸 편·관문 통과(gates_ok) · 카페 비축 0/2
  착수: firemap-write 23:10 (운영실장)
$MSG
- [지시] **firemap-video-producer** (상시) 쇼츠 비축 2/4 → 관문 통과 클립 1편 추가(c1clip 아닌 틀, 다른 롱폼)
  착수: firemap-video-producer 23:10 (운영실장)
  완료: firemap-video-producer 23:35 — 쇼츠 클립 1편 추가: h1s_forest(H-1 롱폼 rVg0pQVo_wk 둔촌동 '집값 같은데 전세 14억', c2person 틀 — m1clip은 ⓓ 5/9라 업로드 거부·c1clip 지시 제외, Pexels 참고 영상 프레임·배지 '화면 속 아파트는 포레온 아님', 새 녹음 0, 51.7초) 관문 통과(compete 7·숫자 대조 47개 0·꼴 ⓐ~ⓓ·치직 0·쉿소리 틀 0·빈 곳 최대 1%·제목 8.5·aitell 0.0/7.7·58세 이해 시험 뜻 맞음, 배지 헷갈림 고쳐 재렌더) → gates_ok 23:34 · **10/22 19:20 예약 https://youtu.be/RmjfiIlKNeU**(slots 새 줄) · 비축(reserve)은 그대로 2/4(c2s_jungwoo·p1s_step) — 칸에 바로 걸어서 · 10/22 07:20은 H-1 아닌 롱폼으로 · vidIQ 크레딧 0(경쟁 조사는 innertube+Data API) · 근거 cardshorts/h1s_forest/review.md
- 막힘: 운영실장 23:37 — 카페 비축 0/2 그대로(write 23:10 투입은 10:40 칸만 통과), 쇼츠 비축 2/4(새 클립은 칸에 바로 예약)
- 착수: 롱폼 총괄 PD 01:35 — N-2 새 기준 시범작 사장님 미리보기 마무리(기한 10/16 18:00): 대본 확정(한 질문 '내 월급은 100명 중 몇 번째', 낮은→높은 월급 한 방향, 한 달 실수령, 가상 인물 최소)·58세 이해 시험 틀림 0까지·대표 장면 4장·썸네일 2안(judge 7+)·N-1 나란히 비교 1장 → ep/N-2/pilot/preview/ · 녹음·렌더는 사장님 본 뒤
  완료(일부): 롱폼 총괄 PD 02:1x — N-2 미리보기 ep/N-2/pilot/preview/(장면 4장 Pexels 사진+큰 숫자 29~30%·썸네일 A 7.5~8.5·G 8.5·N-1 비교 1장·대본 요약) · 대본 v7.8(상호 씨 뺌, 한 질문 '100명 중 몇 등', 세전 150→1,000만원 한 방향, 말로는 세전·등수만, 통장은 화면+'1할 더하면 세전') · aitell 숫자 88.5 통과 · 58세 이해 시험 1~8차(16명) 틀림 매번 고침, **9차(최종판) 결과 받기 전 마감 → understand_test.md 판정: 보류** · 제미나이 이미지 3종 429(재시도 약 7.3h)라 Pexels 사용 · 녹음·렌더는 사장님 확인 뒤

## ★ 벤치마크 루프 10/16 03시 — 카페 글 2판 배정 (근거 research/growth/cafe-gap-1016.md, 지난 개선 반영 2/16·일부 6)
- [지시] **firemap-write** (기한 10/17 첫 회차부터) 완료 기준: ① 첫 문장은 독자 질문·고민 문장(면책·낱말 풀이·영상 안내 금지, A34~A36) ② 첫 150자 숫자 3개 이하(지금 중앙 8) ③ 예시 금액·날짜·상품이 직전 3일 공개분과 겹치지 않음(274·280 'SPY 1억 10/2' 재발 금지, A37) ④ 끝 '한눈에 정리'(지금 4/20) · 확인: 다음 판에서 같은 metrics로 첫 150자 숫자·인용구·정리 칸 수
- [지시] **firemap-write** (기한 10/18) cafeedit.py 편집기 경로로 시험 글 1편에 텍스트 표 1개·인용구 소제목 1개가 들어가는지 확인(1011 #13 지시 뒤 기록 없음, 남 pardus/1958733 se-table 3·nds07/5789267 se-quotation 10) · 공개 글에 넣지 말고 비공개·임시저장으로 · 결과를 decisions/log에 됨/안 됨 한 줄
- [지시] **firemap-visual-designer** (기한 10/18) 표지 3건 재배정: ① 주제 사물 그림 1개(지금 0/20) ② 주제어 줄을 가장 큰 글자로(지금 큰 글자는 숫자) ③ cover_review.md에 '100px 읽힘'·'최근 10장 옆 구별' 두 줄(10/13~15 pkg 26개 중 0) · 본문 표 그림은 800px에서 읽히는 열 수로(286 표 3장 판독 불가)
- [지시] **firemap-copywriter** (기한 10/18) 카페 제목에 날짜·연도('10월 15일'·'2026') 넣는 비율 20/20 중 0 → 다음 10편 중 3편 이상
  착수: firemap-copywriter 07:49
  완료: firemap-copywriter 07:59 — 근거 다시 잼: 남 '2026' 제목 9/38(1011)·우리 0/20, 그러나 '2026 국민연금' 검색 40·'2026연말정산' 480 vs '국민연금수령나이' 49,980(kwvol 10/16) → 연도는 맨 앞 말고 검색어 뒤, 시점 있는 글(시행일·기준일·종가 날)에만 · work/titlegate.py가 연도·날짜 없는 후보에 '참고(막지 않음)' 줄을 띄움 · 확인: 다음 판 벤치마크에서 10편 중 3편
- [지시] **firemap-editor** (상시) style-guide A34~A37 카페 원고 점검에 추가, aitell 사전에 넣을 수 있는 것(A36 첫 문장 '~라는 글이 아니에요')은 사전으로
  착수: firemap-editor 07:04 (정기 06:50)
  완료(상시 첫 회): firemap-editor 07:09 — aitell.py에 opening_check(A34 첫 400자 괄호 풀이 ≥2 · A36 첫 문장 면책·영상 안내·주소) · **10/17 슬롯부터 frame이 막고**, 그 전은 gate 경고만 · 10/12~16 묶음 40개에 돌려 5개 걸림(r1cafe_tax1015 4개·r1cafe_start1016·qqqm1014·sdi1015b A34+A36), 오탐 거름(출처·입주·년생·날짜 괄호) · A35·A37은 눈으로(style-guide) · 오늘 07:40 r1cafe_start1016 c00 괄호 덧말 문장으로·c01 되풀이 1문장 지움, 재stamp ede50819
- [요청] **firemap-report** ← 벤치마크 (10/16 03시) 모바일 카페 탭(m.search where=m_article)에서 주제어 5개·우리 제목 원문 2개로 firemap 링크 0이 나왔다(제목 원문 검색은 남 카페 링크도 0 → 받는 방식 문제일 수 있음). 10/15 '카페탭 12/12'와 같은 방식으로 10/15 공개분 다시 재서 노출 변화인지 측정 문제인지 한 줄
- 결정 필요(순돌이 → 사장님): 회원 3명·댓글 0/37 그대로 — 남 고조회 글 7편 중 4편이 회원의 1인칭 고민·질문(댓글 합 36). 글 형식으로는 못 푸는 일(1011 #16)

- [알림] **firemap-write** ← firemap-editor (07:09) ① 07:40 r1cafe_start1016 표본 검수: c00 '(미국 돈인 달러로…)' 괄호 → 다음 문장, c01 '이 계산을 251번 했어요' 지움 · 숫자 0 변경 · frame 통과 · editgate 재stamp ede50819 · 발행 그대로 ② 18:10 retax1016 소제목 1 '같은 2억원인데 왜 세 배…'(제목·첫 문단과 같은 말) → '세금이 갈리는 곳은 빼 주는 금액과 세율' · 재stamp 5804e53e ③ **10/17 슬롯부터 aitell frame이 A34(첫 400자 괄호 풀이 2개 이상)·A36(첫 문장 면책·영상 안내·주소)을 막음** — 쇼츠 짝 글의 '오늘 아침 짧은 영상에서…'+주소는 끝으로
- [알림] **firemap-youtube-loop·firemap-video-producer** ← firemap-editor (07:09) J-1 say_v3 재서명(0장 1줄 추가) · S-1 say_v2 서명(바뀐 줄 9·23, 끝 질문을 정리 뒤로 옮겨 45·46 순서 바뀜)
- 확인(firemap-editor 07:09): 정기 06:50 근무 — 열린 [편집 검수 요청] 2건(J-1·S-1 통과) + [지시] A34~A37 · auto 표본 2/6(r1cafe_start1016·retax1016 고침) · sweep은 다음 근무- [자발] **firemap-write-b** 07:42 회차 — 07:40 칸 r1cafe_start1016(r1s_startday tDPWYHRotRQ 짝) 발행
  착수: firemap-write-b 07:42
  완료: firemap-write-b 07:51 — 07:40 r1cafe_start1016 https://cafe.naver.com/firemap/289 verify OK 1820/1820자·사진 3/3(게시판 ETF) · readcheck 6건 고친 뒤 재서명 · [알림] firemap-video-producer: 쇼츠 r1s_startday(tDPWYHRotRQ) 설명 앞 5줄 카페 주소를 https://cafe.naver.com/firemap/289 로 · 13:40 write-b 칸 TBD(관문 기한 07:40 지남)
- [알림] **firemap-video-producer** ← firemap-write-b (07:51) 쇼츠 r1s_startday tDPWYHRotRQ 설명 앞 5줄 카페 주소 → https://cafe.naver.com/firemap/289

- [알림] **firemap-video-producer·firemap-visual-designer·firemap-youtube-loop** (copywriter 07:59): H-2 meta.json 만들 때 title·title_candidates·thumb_text는 ep/H-2/copy/titles.md 1위 짝 그대로 · 설명 첫 줄 제안도 거기 · visual: 썸네일 A 1초 시험에 '가장 비싸고 가장 싼 건 어디 안에서?'를 넣고 '서울·세 동네'로 읽히면 앞줄 '잠실 안에서'를 키울 것 · '1등·꼴찌'·'30%↑'·'재건축' 쓰지 말 것 · H-2 understand_test 판정: 통과
- [자발] P-2(35세 조기은퇴 뒤 국민연금) 대본 v1·심사·이해 시험 트랙:C · 담당 firemap-youtube-loop · 근거 longform/ep/P-2/analysis.md
  착수: firemap-youtube-loop 08:43
  완료: firemap-youtube-loop 09:04 — P-2 대본 v3.2 심사 통과(2차 평균 7.27: Claude 7.4·레드팀 7.8·제미나이 6.6 → 막을 문제 고친 뒤 레드팀 3차 8.0~8.2) · **전제 고침**: 혼자 사는 무소득 퇴사자는 국민연금법 제9조상 당연 지역가입자라 임의가입 대상 아님 → 준호 씨 = 배우자가 회사 다니는 무소득자 · 공단 안내 원문으로 임의가입 중위수 '26.4 101.3만원 확인(Q6 닫음) · 세 길 39·62·96만원쯤, 더 낸 1,400·3,800만원쯤, 본전 70.2·70.6세, **물가보다 연 2% 더 불렸다면 74세 무렵**(calc 새로, 경쟁 1등이 우리보다 나은 점 따라잡음) · 58세 이해 3차 뜻 틀림 0(대본 통과, 제목·썸네일은 카피 뒤) · 말 60줄 약 5분 반(원문 없는 세금·건보료 안 넣어 10분 안 채움) · 근거 longform/ep/P-2/review.md
- [편집 검수 요청] P-2 script.md v3.2(말 60줄, say_v3.txt) 트랙:C · 담당 firemap-editor · 시한 10/20 12:00 · 근거 longform/ep/P-2/review.md·understand_test.md · aitell script 78.9·19%(숫자 2개 문장 기준선 가까움 — 숫자 넣는 고침 금지)·aitell 1.9 통과 · 금지: 숫자·나이 바꾸기, '배우자가 회사에서 국민연금을 내고 있으면'·'배우자가 없다면…지역가입자' 범위 넓히기(제9조1호 — 레드팀 두 번 막음), '오늘 돈'·'받기 시작한 뒤에도'·'물가보다 해마다 2% 더' 빼기, '그 전에 세상을 떠나면…본전에 못 미칩니다'(균형 문장) 빼기, '임의가입 하세요'류 · 요청 firemap-youtube-loop 09:04
  착수: firemap-editor 17:04 (정기 16:50)
  완료: firemap-editor 17:10 — 편집 통과(script.md.edit.json sha 4ff84367) · 말 60줄 줄마다 봄 · 편집자 1곳: 0장 '혼자 이어 내면'→'계속 이어 내면'('혼자'가 혼자 사는 사람으로 읽혀 임의가입 대상 아닌 사람을 부름 — 요청 금지 범위) · 금지 줄 전부 그대로 · 숫자 값 0 변경 · aitell 3.9 · script 78.9/1,000·19% 통과 · 녹음 say_v3.txt 3줄 · 원본 .orig1016
- [요청] **firemap-copywriter** ← youtube-loop (09:04) P-2 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/19 12:00 · 근거 longform/ep/P-2/analysis.md ②(국민연금임의가입 7,510·파이어족 12,530·임의가입금액 1,580)·compete.md(1등 '낸 돈·더 받는 돈 숫자 둘 + 이득일까?') · 방향: '국민연금 임의가입' 맨 앞, 숫자 하나(39만원→96만원 또는 '본전 70세') · 금지: '이득'·'무조건'·'모르면 손해'·'공단이 안 알려줌', 1등 제목 틀 그대로, '혼자 사는 퇴사자'처럼 임의가입 대상이 아닌 사람을 부르는 말(법상 배우자가 가입자인 무소득자만 대상)
  착수: firemap-copywriter 18:45
  완료: firemap-copywriter 19:02 — P-2 title 1위 **'국민연금 임의가입, 퇴사 뒤 더 낸 3,800만원은 몇 살에 다 돌아올까'**(제미나이 7.6·레드팀 8·copywriter 8 = 7.87, 영상 첫머리 약속과 같은 말·숫자 1개·P-1 겹침 0.07) · 2위 '…그냥 둘까 이어 낼까? 39만원과 96만원 사이'(7.63) · 썸네일 '35세에 퇴사한 나 · 배우자는 직장인' / **'받는 연금 월 39만원 vs 96만원'** / '그냥 둘 때 · 60세 전까지 보험료 낼 때'(58세 1차 '→'가 내는 돈·권유로 읽혀 고침, 2차 뜻 맞음) · 첫 3초 대본 첫 줄 그대로 · 뺀 말: '한 달 10만원씩'(2033년 13만원)·'본전 일흔 살' 단정(이자 0% 가정)·'끝까지' · understand_test 제목·썸네일 판정: 통과 · aitell 0.0 · 근거 ep/P-2/copy/titles.md·review_in_카피_카피.md
- [요청] **firemap-meeting** ← youtube-loop (09:04) P-2 롱폼 칸 요청 — 대본 심사 통과(7.27), 편집·카피 10/20, 녹음 1창(말 60줄) · 같은 연금 축 P-1(10/16)과 이틀 붙지 않게 10/24 이후 11:30 칸 · 합성 표시: 실사 생성 장면 넣으면 True · 짝 카페 글 자료(세 길 전체 표·1~3% 본전 표·calc_out)는 칸 정해지면 write에
- [편집 검수 요청] T-1 화면 글자(screen_text.txt 377줄, lfrender text — sha는 lfrender check가 잼) 트랙:C · 담당 firemap-editor · 시한 10/18 12:00(칸 10/21 11:30, 관문 10/20 11:30 — 렌더·점수표·업로드가 그 뒤) · 근거 longform/ep/T-1/screen_text.txt · 화면 video/src/T1.tsx + ep/T-1/t1props.py(숫자는 calc_out·자막에서 need로 기계 대조) · aitell 2.9 통과 · 판단 부탁: '산 해'는 '사다'로 읽혀 화면에선 '살았던 해'로 씀, 사례 ①② → '사례 1·2' · 녹음 63줄 끝(Charon 1.1·쉼 태그, 튀는 줄 0·앞뒤 −3.5%·받아쓰기 걸린 줄 다시 받아 0) · 요청 firemap-video-producer 10:36
  착수: firemap-editor 17:04 (정기 16:50)
  완료: firemap-editor 17:10 — 화면 글자 편집 통과(lfrender stamp 785b008c, text 다시 뽑아 바뀐 것 0) · 고침 0 · '살았던 해'·'사례①②' PD 판단 그대로 좋음 · 8장 '4%씩'은 %p 뜻, 자막 32%p가 받침 · aitell 2.9 · lfrender check 관문 통과
- [요청] **firemap-visual-designer** ← firemap-video-producer (10:36) T-1 썸네일 — 문구는 ep/T-1/copy/titles.md 1위 짝('2년만 살았으면 / 양도세 공제 48%→16%로 줄어' · 작은 줄 '정부안 · 2029년 · 20억 집 팔 때', copywriter 18:59) · 1초 시험 3명 통과판을 ep/T-1/meta.json thumb에(없으면 경로를 today.md에) · 1초 시험에서 '양도세가 줄어'로 읽히면 2위 '거주 10년 vs 2년 / 양도세 약 12배' · 화면 재료: video/out/t1_stills_1115(두 집 그림·계단 칸) · 기한 10/19 06:00(관문 10/20 11:30)
- [요청] **firemap-copywriter** ← firemap-video-producer (10:40) T-1 제목 숫자 6개('1주택'·'20억'·'2029년'·'1,241만원'·'1억 4,777만원') — ytlong 관문 '제목 숫자 2개 이하'에 걸림(C-2와 같은 일) · titles.md 2위('…살았던 햇수 하나로 양도세 열두 배 가까이 차이', 숫자 1개)를 1위로 올릴지, 1위 뜻 그대로 숫자 2개 이하 판을 새로 낼지 판단해 ep/T-1/meta.json title·title_candidates에 · 기한 10/19 12:00(칸 10/21 11:30, 관문 10/20 11:30) · 근거 work/ytlong.py gate
  착수: firemap-copywriter 18:45
  완료: firemap-copywriter 19:02 — T-1 title 1위 **'장기보유특별공제 정부안, 2029년엔 같은 20억 집이 살았던 햇수 하나로 양도세 열두 배 가까이 차이'**(숫자 6→2) · 레드팀 8.5(연도 없으면 올해도 12배로 읽힘, 올해는 4.3배) · 58세 뜻 맞음(오래 산 사람 vs 짧게 산 사람·확정 아님) · 검색 장기보유특별공제 8,370 > 1주택양도세 3,220(kwvol) · 2위 '양도세 정부안, 같은 20억 집 한 채인데 2029년 세금은 열두 배 가까이 차이' · meta.json title·title_candidates(옛 title_prev_1016) · understand_test 판정: 통과 · 남은 막힘: meta.json에 desc 칸이 없어 ytlong gate가 KeyError로 멈춤(PD 몫) · 근거 ep/T-1/copy/titles.md 끝
- [자발] **firemap-write-b** 10:42 회차 — 10:40 칸 deposit1016 발행
  착수: firemap-write-b 10:42
  완료: firemap-write-b 10:55 — 10:40 deposit1016 https://cafe.naver.com/firemap/291 verify OK 939/939자·사진 3/3(게시판 돈 관리) · 관련 영상 없음(예금 금리 공개 영상 없음) · 남은 b 칸: 13:40·16:40·19:40·22:40 TBD

## ★ 순돌이 10/16 11:4x — 손품 롱폼 주 2편(사장님 "손품 영상 주 2편으로 올려")
- 근거: H-1 공개 1일 80회 vs 같은 주 G-1 3일 3회·W-1 4일 4회·R-1 2일 117회.
- [지시] **firemap-youtube-loop**: 손품은 매주 화·금 11:30 고정. 10/20 H-2(대치·잠실·반포), 10/23 H-3(series-plan 4-2 다음 동네). J-1은 10/24로. H-3 대본 10/20 21:00, 관문 10/22 11:30. 이후 화·금 칸을 매주 회의에서 먼저 채운다.
  착수: firemap-youtube-loop 12:44 — H-3 분석 관문(동네 고르기·수요·거래량)부터
  중간: firemap-youtube-loop 12:50 — H-3 분석 관문 통과(analysis.md·compete.md·calc_out.txt): 압구정·신천·목동(4-2 순서 7~9) · 검색 압구정현대아파트 33,510·목동 20,340·잠실파크리오 20,110 · 3개월 거래 39·48·98(신정 201) · **질문 '같은 30억이면 몇 ㎡?'** — 30억 안팎 신천 175건(전용 중앙 85㎡)·목동 67건(96㎡)·압구정 0건(가장 싼 거래 35.7억) · 목동신시가지 1~7(목동)↔8~14(신정동) 같은 60~70㎡ 평당 +20.4% · 같은 단지 작은 집 평당 더 비쌈(파크리오 35↔145㎡ +61%) · 경쟁 5편은 거래 한 건·재건축 전망뿐 · 실험 X-H3-SAMEMONEY · 다음: facts→대본 v1→심사→58세 이해 시험(기한 10/20 21:00)
  착수: firemap-youtube-loop 16:45 — H-3 사실표·대본 v1·심사·58세 이해 시험
  완료: firemap-youtube-loop 16:55 — H-3 대본 v2.2 심사 통과(v2 평균 7.93: 제미나이 8.2·Claude 8.0·레드팀 7.6, v1.1은 7.0이고 사실 오류 1이라 막음) · **calc §7 새로: 같은 단지 작은 집 평당이 더 높은 곳, 골라 본 5곳이 아니라 전부 — 신천·목동·신정 26곳 중 24곳**(압구정은 기준 넘는 단지 1곳뿐이고 거꾸로 → 자막만) · 압구정 가장 싼 거래 = 한양1차 63.87㎡ 35.70억 **직거래**(분석 관문의 '50㎡대'는 틀림 → 고침) · 레드팀 v2: 공급 '34평' + 전용 '3평' 섞으면 37평으로 들림 → '34평' 뺌, 말은 ㎡ 하나로 · 58세 이해 4차 뜻 틀림 0·퀴즈 8/8 · 말 44줄 약 4분(숫자 밀도 71.2·aitell 0.0, 억지로 안 늘림) · 손품 씨 안 넣음(30억과 무관) · 판정 보류는 제목·썸네일 몫 · 근거 longform/ep/H-3/review.md·understand_test.md
- [편집 검수 요청] H-3 script.md v2.2(말 44줄, say_v2.txt) 트랙:C · 담당 firemap-editor · 시한 10/19 12:00(칸 10/23 11:30, 관문 10/22 11:30, 녹음 전) · 근거 longform/ep/H-3/review.md·understand_test.md·facts.txt · aitell script 71.2·6%·aitell 0.0 통과 · 금지: 숫자 값 바꾸기, '34평'·평 단위 다시 넣기(전용·공급 섞임), '목동신시가지 앞 번호 단지들'을 '목동'으로 줄이기(1~7단지만 셈), '열에 아홉 가까이'를 '네 동네'로 넓히기(압구정 제외), '왜 이만큼 차이가 나는지는 실거래 자료에 나오지 않습니다' 빼기, 재건축·토지거래허가 · 요청 firemap-youtube-loop 16:55
  착수: firemap-editor 17:04 (정기 16:50)
  완료: firemap-editor 17:10 — 편집 통과(script.md.edit.json sha 294c0651) · 말 44줄 줄마다 봄 · 편집자 1곳: 6장 '정리하면, 30억으로 신천동에선…'·'압구정동엔 그 값의 거래가 없었고요' 2줄 지움(0장 결론과 같은 말 — 본문↔마무리 되풀이 금지, 정리 표는 화면에 남음) · 금지 줄 그대로 · 숫자 값 0 변경 · aitell 0.0 · script 72.0/1,000·7% · 녹음 say_v2.txt 42줄(옛 41·42 지움) · 원본 .orig1016
- [요청] **firemap-copywriter** ← youtube-loop (16:55) H-3 제목·썸네일 문구·첫 3초 트랙:C · 시한 10/20 12:00 · 근거 longform/ep/H-3/analysis.md ②(압구정현대아파트 33,510·목동 20,340·잠실파크리오 20,110)·compete.md(경쟁 틀 '1단지부터 14단지까지 총정리'·'대장주') · 방향: 숫자 하나 '30억', 질문 '같은 30억이면 몇 ㎡'·압구정 0건 · 금지: '34평'(전용·공급 섞임), '대장주'·'오를'·'기회'·'폭등', 재건축·분담금, '목동'을 1~14단지 전체처럼(30억 숫자는 1~7단지만), 경쟁 '총정리' 틀 그대로 · 58세 시험 걸림 말: '국민평형'·'중간 크기'
- [요청] **firemap-write** ← youtube-loop (16:55) H-3 짝 카페 글(10/23 영상 전 같은 날 카페 칸, 회의 배정) — 대본 끝 '목동신시가지 열네 단지와 압구정·신천 단지별 표는 파이어맵 카페에' 약속 · 재료 ep/H-3/calc_out.txt §1(1~14단지)·§2(압구정 22곳)·§3(신천)·§5(같은 돈 몇 ㎡)·§7(작은 집 평당 26곳) · 금지: 대본 붙이기·재건축·'34평' · 발행 주소를 slots.json note에 'yt_pair: H-3'로(PD가 자막·고정 댓글에 씀)
- [지시] **firemap-meeting**: 배당 롱폼 주 1편 고정 검토 — 30일 유튜브 조회 상위 15편 중앙값: 배당주 21.5만·월배당 ETF 13.6만·SCHD 10.8만(성장주 0.9만). 우리 A-1(JEPQ·SCHD) 2,393회가 두 번째로 많음. 10/26 주부터 배당 1칸.
- [지시] **firemap-video-producer**: 손품 롱폼마다 동네별 쇼츠(PD가 잘라 예약) + 카페 짝 글(표 대신 한눈에 보기).
  착수: firemap-video-producer 14:18 — H-2(10/20 11:30) 녹음·화면·렌더부터, 동네별 쇼츠(대치·잠실·반포)·카페 짝 글은 렌더 뒤

- [지시] **쇼츠 담당** ← 순돌이 (11:3x) 사장님 "숏츠는 영상이 왜 이렇게 잘려" — 유튜브 앱 UI·화면 꽉 채움에 글자가 가려짐. 원인·안전 영역 기준(safe-zone-1016.md)·렌더 뒤 관문·예약분 재렌더·공개분 목록 · 시한 오늘 18:00
  착수: 쇼츠 담당 11:41
- [자기 배정] firemap-motion-designer X-1 환율(10/22 칸) 모션 설계표 + 1·2장 핵심 장면 부품 — backlog 1순위(W-1 2화 렌더 확인)는 10/15 15:25 screen.json 통과·예약 끝이라 할 일 없음
  착수: firemap-motion-designer 11:27
  완료: firemap-motion-designer 11:49 — 설계표 ep/X-1/motion.md(장마다 움직임, 0·3·4장은 다음 회차) · 새 부품 video/src/motion/FxDates.tsx(1장 ECOS 일별 선 245점+날짜 점 4개·'결과가 제일 나쁜 날을 고른 셈' 빨간 폭 / 2장 같은 1억 막대 4개가 말 순서로 10.12 원화까지 내려앉음, 왼쪽 빨간 세로=내린 환율·오른쪽 빨간 틈=줄어든 원화) · 미리보기 ep/X-1/motion_preview/x1_fx.mp4(39.2초 어림, 움직임 33%·최장 정지 5.5초) · 숫자 calc_out·원문 assert · 심사 제미나이 9·Claude 6·레드팀 7(틀림 0) 평균 7.33 통과
  [요청] **firemap-video-producer** ← motion (11:49) X-1 녹음 뒤 `py -3.12 work/research/longform/ep/X-1/motion_preview/fxprops.py` → X1.tsx 1장 `<FxDates {...fx} phase="line" />`·2장 `phase="bars"`(TallyFrame 자식, s1·s2 frames 그대로) · 렌더 뒤 그 구간 motioncheck·overlap · 화면 글자 늘어남 → 편집 재서명 · 절차 ep/X-1/motion.md
  [알림] **firemap-youtube-loop·firemap-editor** (motion 11:49): X-1 2장 끝 [자막] '2026년 최저는 10.13 1,335.8원'이 그래프 끝(10.12) 다음 날 값이라 심사 2명이 '화면에 없는 날'로 지적 — 사실 틀림은 아님, 자막 유지 여부만 판단
  완료: firemap-youtube-loop 12:50 — 판단: 2장 자막에서 '2026년 최저는 10.13 1,335.8원' 뺌(말에 안 나오고 영상 기준일 10.12와 어긋남) · 5장 엔화 자막은 말 '거의 가장 싼 값'의 근거라 남기되 '최저는 다음 날 10.13 842.3원'으로 날짜를 밝힘 · 숫자 값 0 변경 · aitell 1.3 · 원본 script.md.orig1016 · editor 재서명은 위 X-1 [편집 검수 요청](10/19 12:00)에 이 2줄 더함
  완료: firemap-editor 17:10 — X-1 script.md 재서명(sha aa8d8413) · 자막 2줄만 바뀜(2장 2026년 최저 뺌·5장 엔화 최저 날짜 밝힘), 말 줄 0 변경·say_v2 그대로 · 숫자 값 0 변경 · aitell 1.3
  완료: 쇼츠 담당 12:44 — 원인: 쇼츠 틀(C1S·M1S·C2P)이 글자를 화면 끝·유튜브 UI 자리(위 띠 y 30~307, 아래 답 칸 y 1533~1693, 오른쪽 값 x 1028, 왼쪽 +10% x 23)에 둠. 기준 = Google Ads 세로 동영상 안전 영역(위 288·아래 672·왼쪽 48·오른쪽 192px, 글자는 x 48~888·y 288~1248). 관문 work/safezone.py(1초 간격 글자 상자) — ytupload·w1g1/c1/m1clips_up 통과 없이는 못 올림(종료 11). 새 틀 video/src/parts/safeframe.tsx. 예약 쇼츠 12편 전부 재렌더·교체(같은 publishAt, 옛 12편 비공개·삭제 안 함, slots.json ID 갱신). 공개 쇼츠 26편 전부 걸림(조회 합 16,330) — 목록만, 전환 안 함. 근거 research/cardshorts/safe-zone-1016.md·.png · cardshort.py(옛 카드 틀)는 안 고침 → 그 틀로는 못 올림
  착수: 쇼츠 디자인 담당 12:47 — safeframe 작은 상자 판(위15%·아래35% 검은 빈칸·오른쪽 빔) 고침: 바탕 1080×1920 꽉, 글자만 안전 영역, 답 숫자 크게 · 19:20 w1s_kospi 17:30까지 교체 · 나머지 11편 공개 6시간 전까지
  중간: 쇼츠 디자인 담당 13:38 — 19:20 w1s_kospi 새 틀 v2 판으로 교체 https://youtu.be/DRtKbSuCUiQ (같은 publishAt, 옛 pt1_YLQ8KBs 예약 풀고 비공개·삭제 안 함, slots·yt_pair 갱신) · 58세 이해 시험 4명 한 문장 4/4 · 나머지 11편 렌더 중
- [자발] **firemap-write-b** 13:42 회차 — 13:40 칸 TBD → 비축분 convreal1016 발행
  착수: firemap-write-b 13:42
  완료: firemap-write-b 13:55 — 13:40 convreal1016 https://cafe.naver.com/firemap/293 verify OK 1395/1395자·사진 3/3 · 부동산(전월세 전환율 실거래) · 급락 경제 편은 비축·원고 없어 못 씀 · 비축 카페 0편 → 다음 회차 첫 일 비축 2편 · 남은 b 칸: 16:40·19:40·22:40 TBD
- 완료: firemap-editor 14:40 — H-2 화면 글자 편집 통과·stamp(sha 0d512555) · 고친 곳 3(h2props.py: 18장 부제 보증금 근거 '지난 편 고덕동'→'래미안힐스테이트고덕'(H-1 calc §8 단지 값) · 14장 '(견줌)'→'(비교용)' · 7장 '84㎡대 하나'→'84㎡대만') · 숫자 0 변경(diff 3줄뿐) · 금지어 0 · aitell 3.2 통과 · 원본 h2props.py.pre1016ed
- 완료: firemap-editor 14:58 — H-2 화면 글자 재서명(PD w_ruler step 분할 2줄: 래미안대치팰리스 한티역까지 530m · 대치르엘은 1km 넘게/2021년 단지 · 대치역까지 1,010m — calc_out §5 일치) · 숫자 0 변경 · 다른 곳 손대지 않음
  완료: 쇼츠 디자인 담당 14:59 — 원인: 12시 safeframe v1이 판 전체를 0.66배로 줄여 위 0~288·아래 1248~1920 검은 빈칸·오른쪽 빔. v2(video/src/parts/safeframe.tsx·C1S·M1S·C2P): 바탕 1080×1920 전체(아래는 같은 판 흐리게), 글자만 x 48~888·y 288~1248, 질문 최대 76px·답 숫자 최대 128px·판은 실제 그려진 범위만 잘라 840 너비 채움·대결 칸 나란히·C2P 사진 화면 끝까지 · 예약 12편 전부 재렌더·교체(같은 publishAt, 옛 12편 예약 풀고 비공개·삭제 0, 합성 표시 True update 응답, videos.list 재확인) · 19:20 w1s_kospi = DRtKbSuCUiQ · 안전 영역 관문 12/12 걸림 0·0초 빈 곳 0~21%·58세 이해 시험 편마다 1~4명 한 문장 전부 맞음(g1s_why는 큰 숫자 오독 2회 → 내 금 −4.43%로 묶어 3차 통과) · slots.json·yt_pair 새 ID · 비교 research/cardshorts/safe-zone-1016b.png · 근거 safe-zone-1016.md v2 절 · 남은 약점: 판 안 작은 글씨·막대 하나 장면 휑함(판 부품 일)
- [요청] **firemap-copywriter** ← firemap-video-producer (15:15) H-2 bench_check.md(잘된 영상 대조: 제목·썸네일·첫 60초·자막·대본 표 + 맨 끝 '대조: 통과') · 렌더본 work/video/out/h2_ds.mp4(4:38, h2.json 24장면) · 스틸 video/out/h2_lines/ · 썸네일은 visual 진행 중(ep/H-2/meta.json thumb) · 기한 10/19 06:00(칸 10/20 11:30, 관문 10/19 11:30) · H-1 bench_check 형식 그대로
  착수: firemap-copywriter 18:45
  완료: firemap-copywriter 19:09 — H-2 bench_check.md(제목·썸네일·첫 60초·자막·대본 44행, 맞춤 30·안 맞춤 13·반반 1) **대조: 통과** · 막을 문제 없음 · 고칠 것: ① thumb_h2t.png가 옛 문구 그대로(새 앞줄·작은 줄 반영판 visual) ② 정확한 값 칩 20개 중 13개 40자 넘음(3:27 124자, motion) ③ 0:48 지도 단지 조각이 범례를 덮고 '주공5단지' 잘림(motion) ④ 0:38 카드 '오래된 단지가 37.2% 쌌음' — 고덕아남(1996)은 이 편 기준 '1990년 전'이 아님, PD·youtube-loop 확인 ⑤ 끝 30초에 H-1 연결 없음 · 다음 ytlong gate 남은 막힘: review.md 판정 줄 '미달' 낱말(PD)
- [요청] **firemap-write** ← firemap-video-producer (15:15) H-2 짝 카페 글 — 재료 ep/H-2/cafe.md(순돌이 10/16 '표 대신 한눈에 보기': 동네마다 우리 렌더 스틸 한 장 + 세 줄, 28단지는 접은 표 하나) · 영상 공개(10/20 11:30) 전 같은 날 08:10·10:10 칸(대본 '카페에 올려 둘게요') · 발행 주소를 slots.json note에 'yt_pair: H-2'로 · 회의(21:15)가 10/20 카페 칸 배정
  완료(일부): firemap-video-producer 15:15 — 손품 [지시](10/16 11:4x) 중 H-2 몫: 동네별 쇼츠 재료 3편 cardshorts/h2_specs/spec.md(잠실·대치·반포, 공개 뒤 자르기) · 카페 짝 글 재료 ep/H-2/cafe.md·write 요청
- 완료: firemap-video-producer 15:15 — H-2 렌더·관문 끝(h2_ds.mp4 4:38 · Chirp Charon 56줄 · 그림 14가지 · 같은 화면 최장 8.0초·겹침 0·쉿소리 −12.1dB·치직 0 · editor 화면 서명 14:58 · 점수표 35 vs 경쟁 중앙 25 · 설명 앞 두 줄 58세 3차 통과) · 남은 것: 썸네일(visual 투입 중)·bench_check(copywriter) → ytlong gate → 10/20 11:30 예약
- 완료: firemap-visual-designer 15:26 — H-2 썸네일 thumb_h2t.png 임시(1초 시험 미달) · 11차 최종 평균 6.83(세 명: 제미나이 8·7 · Claude 6 · 레드팀 7 겹침 2, 최고 h2s 6.92) · 주제 맞힘 3/3 · 58세 '잠실에서 사려면 제일 비싸고(43억), 전세는 제일 싸다(5억)' 뜻 맞음 · meta thumb/thumb_status · 비교판 ep/H-2/thumb_compare.png · [요청] copywriter: '1년'(잠실 11개월치)·'잠실 안에서'(잠실동만)·작은 줄 '전세 5억 남짓' 되풀이 판단 — 기록 visual/H-2-thumb/judges.md
  답: firemap-copywriter 19:03 — H-2 판단 3건: ① '1년' 그대로(대본 10줄 '최근 1년 치'·조회 창 12개월, 11개월 거래는 설명 출처 줄에 있음 — 레드팀 문제 아님) 단 '1년 실거래'→'최근 1년 거래' ② 앞줄 **'잠실주공5단지, 잠실동 안에서'**(자료는 법정동 잠실동만, 신천동 미확인) ③ '전세 5억 남짓' **뺌** → 작은 줄 **'국민평형 84㎡대 · 최근 1년 거래'**, 빈 자리는 막대 키우기에 · 레드팀 6.5→8 · 58세 뜻 맞음 · meta.json thumb_text_top·thumb_text_small 바꿈(옛 _prev_1016) · 큰 두 줄은 그대로
- 막힘: firemap-video-producer 15:27 — H-2 썸네일 1초 시험 11차 최고 6.92·최종 h2t 6.83(통과선 7 미달, 주제는 매번 3/3 맞힘·58세 뜻 맞음) → **예약 안 걺**. 다음 PD 회차 또는 visual이 Claude 심사관 지적('보고서 슬라이드 같다·값 더 크게')과 레드팀 '경쟁 겹침'이 함께 풀리는 판 1개 + copywriter 판단 3건(잠실 11개월치 '1년'·'잠실 안에서' 범위·작은 줄 '5억' 되풀이) 뒤 재심사 · 기한 10/19 06:00(관문 10/19 11:30) · 근거 visual/H-2-thumb/judges.md

- [자발] **firemap-write** 15:20 회차 — 15:10 칸 pencap1015 발행 + 10/17 06:10 경제 TBD 칸 새 편
  착수: firemap-write 15:20
  완료: firemap-write 15:42 — 15:10 pencap1015 https://cafe.naver.com/firemap/294 verify OK 1739/1739자·사진 3/3 · 10/17 06:10 kospidrop1017 '코스피 폭락한 날 산 100만원은 일 년 뒤 얼마가 됐을까?' 관문 통과(ECOS 원자료 24번 전부·레드팀 2차 틀림 0·58세 이해 3차 심각 0·제목 7.83·표지 7.67·editgate auto) · 남은 write 칸 10/17: 09:10 부동산·12:10 돈 관리·15:10·18:10·21:10 TBD · H-2 짝 글 요청은 backlog 1순위(10/20 칸 회의 배정 뒤)

- [알림] **firemap-youtube-loop·firemap-video-producer** ← firemap-editor (17:10) P-2 say_v3 3줄('혼자'→'계속') · H-3 say_v2 41·42줄 지움(끝 정리 되풀이, 화면 정리 표는 그대로) · T-1 화면 글자 stamp 785b008c(렌더 가능) · X-1 script 재서명(자막만, 녹음 그대로)
- [알림] **firemap-write** ← firemap-editor (17:10) ① 10/17 06:10 kospidrop1017 표본 검수: c01 되풀이 1줄('대부분은…메우지 못한 거죠')·상투 넘김 1줄('이야기가 달라져요') 지움, '-어요' 3연속 끊기 · 숫자 0 변경 · frame 통과 · editgate 재stamp 42838743 ② soxl1016(16:40 발행 중) c04 '떨어진 폭이 세 배 가까이 컸던 거죠'(앞 줄 13%·35% 되풀이) — 공개 뒤 editor가 cafeedit로 지움, write 할 일 없음
- 확인(firemap-editor 17:10): 정기 16:50 근무 — 열린 [편집 검수 요청] 3건(P-2·H-3·T-1 화면) + X-1 자막 재서명 · auto 표본 2/5(kospidrop1017 고침·soxl1016 공개 뒤 고침) · 10/17 카페 묶음 frame 1/1 통과 · sweep은 soxl1016 공개 뒤 1건- [자발] **firemap-write-b** 16:42 회차 — 16:40 칸 TBD·비축 0 → 새 편 soxl1016
  착수: firemap-write-b 16:42
  완료: firemap-write-b 17:21 — 16:40 soxl1016 https://cafe.naver.com/firemap/295 verify OK 1980/1980자·사진 3/3(게시판 ETF) · 관문 17:07(제목 7.75·표지 7.67·레드팀 틀림 0·이해 4차) · 비축 카페 0편 → 19:40(쇼츠 짝)·22:40 TBD

- [지시] **영상 디자인 총괄** ← 순돌이 (18:1x) 사장님 "두 번째 세 번째처럼 모든 쇼츠 롱폼에 영상 넣으면 되겠다. 문구나 꾸민 건 잘되는 채널 참고한 거 맞아? 자막 위치·크기·색·도형" — 경쟁 쇼츠10·롱폼5 실측→기준 한 장(research/visual/design-spec-1016.md)·견본 4장·모든 장면 실사 배경·틀 반영·렌더 뒤 검사·예약분 재렌더 · 시한 실측·기준 10/17 09:00, 틀 10/17 18:00
  착수: 영상 디자인 총괄 18:16
- [자발] **firemap-write** 18:21 회차 — 18:10 칸 retax1016 발행·10/17 09:10 부동산 TBD 칸 새 편
  착수: firemap-write 18:21
  완료: firemap-write 18:59 — ① 18:10 retax1016 https://cafe.naver.com/firemap/296 verify OK 1813/1813자·사진 3/3(게시판 연금/세금/보험) ② 10/17 09:10 부동산 칸 sangdo1017 관문 통과(gates_ok 18:58) '상도동 아파트 시세는 같은 단지끼리 보면 작년보다 얼마나 올랐을까?' — 국토부 실거래 동작구 원자료·tour.py, 같은 단지 11곳 작년·올해 여름 비교+14곳 순위+동작구 8개 동 · 레드팀 2회 사실 0 · 58세 이해 2차 통과 · 제목 7.07(레드팀 6 — 숫자 없는 질문형)·표지 7.67 · editgate auto ③ tour.py overpass 미러 재시도 고침 · 남은 write 칸 10/17: 12:10 돈 관리·15:10·18:10·21:10 TBD · 카페 비축 0/2 그대로
- [알림] **firemap-visual-designer·firemap-video-producer** (copywriter 19:03): ① C-2 썸네일 왼쪽 칸 '1년 쓸 돈 모자람'(meta thumb_text_small) — 1초 시험에 '왼쪽 통장은 0원? 은행이 막았나?' 질문, '별일 아님'으로 읽히면 빈 잔고 막대를 키움 ② H-2 앞줄 '잠실동 안에서'·작은 줄 '국민평형 84㎡대 · 최근 1년 거래'(5억 줄 뺌) — 재심사 ③ P-2 썸네일 문구 ep/P-2/copy/titles.md 1위 짝, 1초 시험에 '39·96만원은 받는 돈? 내는 돈?' 질문 ④ T-1 제목 숫자 2개로 바꿈, meta.json에 desc 칸이 없어 ytlong gate가 KeyError(PD) ⑤ H-2 review.md 마지막 판정 줄 '통과 — …목표 8 미달'의 '미달' 낱말 때문에 ytlong gate가 막음, understand_test도 '뜻 틀림 0'의 '틀림' 때문에 막혔던 것(copywriter가 새 '판정: 통과' 줄 더함) — review.md 판정 줄은 '판정: 통과(평균 7.87, 목표 8)'처럼 금지 낱말 없이(PD)
  중간: 영상 디자인 총괄 19:39 — 1·2 끝: research/visual/design-spec-1016.md(경쟁 쇼츠 10·롱폼 5 vs 우리 쇼츠 12·롱폼) · 차이 핵심: ① 배경 실사 경쟁 쇼츠 9/10·롱폼 5/5 vs 우리 2/12·0/2 ② 자막 글자 높이 경쟁 3.28% vs 우리 2.29% ③ 자막 상자 없음+검은 테두리 경쟁 8/9 vs 우리 10/12 검은 상자 ④ 장면 길이 경쟁 5.0초 vs 우리 컷 0(판 8~27초) ⑤ 위 제목 글자 4.6% vs 3.5%(자막 위치 61.6% vs 61.1%는 이미 같음) · 견본 4장 research/visual/design-spec-1016/{short_board,short_photo,long_board,long_bignum}.png · 틀 코드 반영 중(safeframe DS·OutlineCaption·BgLayer, C1S·M1S·C2P, TallyFrame bg) · 배경 고르기·N-2 제작은 Agent 병렬
- [자발] **firemap-write-b** 19:44 회차 — 19:40 칸 TBD(w1s_kospi 쇼츠 DRtKbSuCUiQ 짝)·비축 0 → 새 편
  착수: firemap-write-b 19:44
- [지시] **firemap-video-producer** ← 영상 디자인 총괄 (19:5x) 디자인 기준 v3(research/visual/design-spec-1016.md) 롱폼 적용 — 모든 장면 뒤 주제 실사 사진·영상. `TallyFrame`에 `bg={src, start, kind, x}`(work/video/public 기준)를 장면마다 넘긴다 · 같은 배경 8초 넘으면 클립·구간 바꿈 · 렌더 뒤 `py -3.12 work/bgcheck.py <mp4>` 통과(ytupload가 통과 없으면 막음, 종료 12) · 자막은 TallyFrame 기본(한 줄·60px·검은 상자) 그대로 · 순서: N-2(10/18, 오늘 밤 N-2 PD Agent가 제작 중) → C-2(10/19 11:30, 관문 공개 6시간 전 10/19 05:30) → H-2(10/20 11:30, h2_ds.mp4 15:15 렌더본은 배경 없음 → 다시 렌더, 10/20 05:30까지) · 설명란 끝에 배경 출처 줄(stock/credits.json desc_line)
- [지시] **firemap-visual-designer** ← 영상 디자인 총괄 (19:5x) C-2·H-2 장면별 배경 실사 고르기 — Pexels만(`py -3.12 work/pexelsvid.py "영어 검색어" 4 research/longform/ep/<편>`, 사진은 work/pexels.py) · 프레임을 눈으로 봐서 실존 인물 얼굴·상표·로고·간판 글자·워터마크 0 · 고른 것 work/video/public/bg/<편>/(영상은 -an h264) · 장면 키→파일·시작 초 목록을 ep/<편>/bg_plan.json(라이선스 주소·작가·페이지)으로 PD에게 · 기한 C-2 10/18 18:00, H-2 10/19 18:00
  착수: firemap-visual-designer 23:11 (운영실장)
  완료: firemap-visual-designer 23:41 — C-2 장면별 배경 실사 41장면 고름(Pexels 영상 32개·프레임 눈으로 보고 얼굴·신문 제호·지폐 인물·상표 있는 것 탈락) · work/video/public/bg/c2/(-an h264) · research/longform/ep/C-2/bg_plan.json(장면 0~40→파일·시작 초·작가·페이지·라이선스, 테마 풀 포함) · 4458918은 0~7초만 · H-2는 다음 회차
- [지시] **firemap-motion-designer** ← 영상 디자인 총괄 (19:5x) 움직임 부품은 흰 보드(카드) 안에서 그대로 쓴다 · 보드 없는 장면(board=false)은 실사 배경 위 흰 카드(모서리 24·그림자)에 숫자 하나 — 견본 research/visual/design-spec-1016/long_bignum.png · 쇼츠 판은 FitBoard card(흰 카드 95%)로 바뀜, 판 안 흰 바탕 가정 그대로 유효 · 새 부품은 배경 위에 글자를 직접 두지 말고 카드 안에
- [지시] **쇼츠 담당·firemap-video-producer(클립)** ← 영상 디자인 총괄 (19:5x) 새 클립부터 v3 틀: ① 배경 고르기 → research/cardshorts/<편>/bg_plan.json ② `py -3.12 work/research/cardshorts/bgprops.py <편>`(말 줄 경계·최장 6초) ③ 렌더(자막은 자동으로 한 줄 72px 테두리 — parts/safeframe `OutlineCaption`, 숫자 노랑) ④ `bgcheck.py`·`safezone.py` 통과 — w1g1/c1/m1clips_up이 둘 다 요구
  완료: firemap-write-b 20:19 — 19:40 w1scafe1016 https://cafe.naver.com/firemap/297 verify OK 1115/1115자·사진 3/3(게시판 경제 이야기) · 쇼츠 DRtKbSuCUiQ 짝(10/2→10/16 코스피 1천만원 809만원) · 관문 20:04(제목 7.67·표지 7.67·레드팀 틀림 0·58세 이해 2차) · 비축 카페 0편 → 22:40 TBD
- [알림] **firemap-video-producer** ← firemap-write-b (20:19) 쇼츠 w1s_kospi DRtKbSuCUiQ 설명 앞 5줄 카페 주소 → https://cafe.naver.com/firemap/297
- [자발] H-2 0:38 카드 '오래된 단지가 37.2% 쌌음' 정의 어긋남(copywriter 19:09 ④ 'PD·youtube-loop 확인') 트랙:C · 담당 firemap-youtube-loop · 근거 longform/ep/H-2/bench_check.md
  착수: firemap-youtube-loop 20:43
  완료: firemap-youtube-loop 20:46 — 판단: 이 편 정의('1990년 전')로 고덕아남(1996.03)은 오래된 단지가 아님 → 카드 문구 '지난 편 고덕동: 1996년 단지가 2019년 단지보다 37.2% 쌌음'(H-1 calc_out §: 그라시움 2019.09 9,457 vs 아남 1996.03 5,937 → −37.2%, 값 0 변경) · h2props.py에 두 단지 연도 assert 더함 · h2.json·screen_text.txt 다시 뽑음(diff 1줄) · 원본 h2props.py.pre1016yl · editor 화면 서명은 깨짐 → 아래 요청
- [편집 검수 요청] H-2 화면 글자 재서명(scenes.5 beats.1.1 한 줄만, git diff screen_text.txt) 트랙:C · 담당 firemap-editor · 시한 10/19 06:00(칸 10/20 11:30, PD 배경 v3 재렌더 전) · 금지: '오래된 단지'로 되돌리기(이 편 정의 1990년 전) · 요청 firemap-youtube-loop 20:46
- [알림] **firemap-video-producer** ← youtube-loop (20:46) H-2 h2.json 0:38 카드 문구 바뀜 — 배경 v3 재렌더 때 그대로 반영됨(h2props.py 다시 돌리면 같음), editor 재서명 뒤 렌더
- [자발] H-4(10/27 화 손품) 분석 관문 — 동네 고르기(4-2 순서 10 공덕·후보 철산·방배·한남)·수요·거래량 트랙:C · 담당 firemap-youtube-loop · 근거 longform/series-plan.md 4-2
  착수: firemap-youtube-loop 20:46
  완료: firemap-youtube-loop 20:57 — H-4 분석 관문 **통과**(analysis.md·compete.md·calc_out.txt·pick_out.txt): 동네 **광명 철산·하안·광명동**(공덕 1,560은 수요 최하라 미룸·방배는 디에이치방배 입주 전 매매 0·한남은 3개월 21건에 100억대 튐) · 검색 철산자이더헤리티지 84,200·광명역 70,600 · 3개월 매매 167·151·155 · 경쟁 '광명, 서울보다 비싸다' 틀 댑쏭 6.29배·오감스 4.0배(자막 5편 읽음 — 전부 단지 한두 곳 최고값·호가로 비교) · **질문 '84㎡ 거래 전부로 서울 25개 구와 줄 세우면 광명은 몇 번째?'** — 2026.07~09 같은 창 광명 9.70억 = 26곳 중 18번째(낮은 서울 구 8개), 2019년 뒤 지은 광명 단지만 14.71억(영등포 14.30억 위) · 철산동 주공13(1986) 13.85억 > 래미안자이(2009) 13.40억 · 철산자이더헤리티지 신규 전세 가운데 8.70억 ≤ 같은 동 84㎡ 매매 가운데 값 16곳 중 6곳 · 실험 X-H4-VSSEOUL · 칸 10/27 11:30 후보(회의 확정) · 다음: facts→대본 v1→심사→58세 시험(기한 10/23 21:00)
- [요청] **firemap-meeting** ← youtube-loop (20:57) H-4(광명 철산·하안·광명동) 손품 칸 10/27(화) 11:30 — 분석 관문 통과, 대본 10/23 21:00·관문 10/26 11:30 · 근거 longform/ep/H-4/analysis.md
- [자발] **firemap-write** 21:20 회차 — 21:10 칸 mixreset1016 발행 + 10/17 12:10 돈 관리 TBD 칸 새 편
  착수: firemap-write 21:23
  완료: firemap-write 22:08 — ① 21:10 mixreset1016 https://cafe.naver.com/firemap/298 verify OK 1401/1401자·사진 3/3(게시판 부동산) ② 10/17 12:10 돈 관리 칸 jeonseloan1017 관문 통과 '전세대출 금리, 2억 새로 빌리면 은행마다 한 달 이자 몇만원 차이 날까?' — 금감원 9월 공시 은행별 전월 취급 평균금리(경쟁 5편 언급 0)·ECOS · 레드팀 3회 계산 원 단위 일치 · 58세 이해 4차 심각 0 · 제목 7.33·표지 7.67 · editgate auto ③ apis.finlife가 버리던 평균금리·중도상환수수료·한도 칸 살림 · 남은 write 칸 10/17: 15:10·18:10·21:10 TBD · 카페 비축 0/2 그대로
  중간: 영상 디자인 총괄 21:39 — 틀 반영 끝(커밋 a30f916·e4238ca: safeframe DS·OutlineCaption·BgLayer, C1S·M1S·C2P, TallyFrame bg, 관문 work/bgcheck.py — ytupload·ytlong·w1g1/c1/m1clips_up이 요구) · 예약 쇼츠 v3 교체 4/10: d1s_when→XFEU7Etfusc · r1s_gap→_eJV4g7ZvUA · h1s_walk→thlIsON6S_k · p1s_cross→vDccXdJOfo8(같은 publishAt, 옛 판 예약 해제·비공개, 삭제 0, slots ID 갱신) · 렌더 중 6편(배경 관문에 걸린 클립 시세판·시계·어두운 복도·노을 빼고 다시) · N-2 kXnAKjC-84Q 10/18 13:40(주 7편 관문으로 11:30→13:40)
- [요청] **firemap-visual-designer** ← firemap-video-producer (22:35) T-1·X-1 장면별 배경 실사 고르기(디자인 기준 v3, 총괄 19:5x 지시는 N-2·C-2·H-2만 적혀 있음) — ytlong gate bgcheck: T-1 out/t1_ds.mp4 배경 실사 8%(최장 108초 없음, ep/T-1/check/gate_1016_2235.txt) → 재렌더 필요 · 방법은 C-2·H-2 지시와 같음(Pexels만, 얼굴·상표·간판 글자·워터마크 0, work/video/public/bg/<편>/, ep/<편>/bg_plan.json) · 장면 키: video/t1.json 14장면(duel·price·ladder·taxcard·rates·climb·basic·ratio·five·verify·cap·excluded·calendar·ask), 주제: 아파트 매매·세금 고지서 없는 서류·달력·두 집 · 기한 T-1 10/19 22:00(칸 10/21 11:30, 관문 10/20 11:30), X-1 10/20 22:00(칸 10/22 11:30)
- 메모: firemap-video-producer 22:35 — T-1 gate에서 PD 몫 3개 채움(compare.md 3줄·§5.2 5문항 답·missing 0) · 남은 T-1 막힘: thumb(visual 10/19 06:00)·bench_check(썸네일 뒤)·배경 v3 재렌더(위 요청)
- [지시] **썸네일 담당** ← 순돌이 (22:35) 사장님 휴대폰 '동영상' 탭 — R-1 G1oI47miUuo 썸네일 금·S&P500·SCHD '+???만' 물음표 가림이 깨진 화면처럼 보임(aitell A30 위반) · facts·calc_out·meta 숫자로 새 2안 → 58세 이해 시험·judge_1014 방식 7 이상 → thumbnails.set 교체 · 오늘 밤
  착수: 썸네일 담당 22:39
  완료: 썸네일 담당 22:47 — R-1 G1oI47miUuo 썸네일 **교체됨**(thumbnails.set 성공, 되받은 maxres = r4a) · 새 판 ep/R-1/thumb_r4a.png '작년에 1억 넣었다면? / 예금에 넣었으면 1억 218만 vs 미국 배당 ETF(SCHD) 1억 1,599만'(세금·환율 떼고, facts [영수증]) · 물음표 0·소수점 0·큰 숫자 2개 · aitell thumb 통과 · 58세 이해(새 Claude) "예금은 218만 늘었는데 미국 배당 ETF는 1,599만 늘었다" 뜻 맞음(SCHD·ETF는 모르는 말) · 점수 judge_1016(judge_1014 방식) 제미나이 8·Claude 7, 대조 r2i 6·5 (gemini-3.1-flash-lite 503 → 3.5-flash-lite) · 2안 r4b 막대 3줄 7·6 · 전 판 ep/R-1/thumb_before_1016.png · 심사 고칠 점: 라벨 168px 작음·질문형 머리 경쟁과 겹침
- [지시] **firemap-write** ← 운영실장 (23:11) 10/17 07:40·10:40 카페 칸(slots.json, write-b 배정) gates_ok 없음 — 관문 기한 01:40·04:40, 카페 비축 0/2 · write-b는 22:40 회차 running이라 write가 07:40 칸부터 관문 통과(원고·제목·표지·58세 이해 시험) → gates_ok에 시각 · 발행은 정기 회차 몫
  착수: firemap-write 23:11 (운영실장)
  완료: firemap-write 23:42 — 10/17 07:40 카페 칸(쇼츠 h1s_gap f3BaZbJLMMk 짝 글) h1gapcafe1017 관문 통과(gates_ok 23:41) '고덕동 전세 사는 사람이 헬리오시티 집을 사려면 얼마가 더 필요할까?' — 국토부 실거래 10월분 10/16 재수신으로 영상 값 갱신(래미안힐스 20.2→20.35·그라시움 24.1→24.3억), 제목 7.4·표지 7.75·레드팀 틀림 0·58세 이해 2차·editgate auto · 커밋 301948c · 10:40 w2cafe1017(W-1 2화 짝)은 시간 모자라 못 함 — write-b 04:40 기한 · 07:40 발행은 영상 07:20 공개 뒤 정기 회차 몫
- [자발] **firemap-write-b** 22:42 회차 — 22:40 칸 TBD(장르 시리즈·연금)·비축 0 → 새 편 bpcut1016(기초연금 국민연금 연계감액)
  착수: firemap-write-b 22:42
  완료: firemap-write-b 23:31 — 22:40 bpcut1016 https://cafe.naver.com/firemap/299 verify OK 1776/1776자·사진 3/3(게시판 연금/세금/보험) · 기초연금 국민연금 연계감액(누리집 2026 산정표·법 5~8조·시행령 10조) · 관문 23:19(제목 7.33·표지 7.5·레드팀 2회 틀림 0·58세 이해 7차) · 비축 카페 0편 · 경고: 오늘 제목 끝말 '얼마' 3칸 — 다음 칸은 다른 끝말
