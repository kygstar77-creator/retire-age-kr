# 도구 장부 — 총무·인사팀(firemap-admin)
마지막 실측: **2026-09-30 23:39** (1회차). 값은 전부 이 회차에 직접 호출해서 잰 것. 키·토큰 값은 적지 않는다.

| 도구 | 상태 | 계정(전용/공유) | 남은 한도·만료 | 누가 쓰나 | 확인 방법 · 비고 |
|---|---|---|---|---|---|
| Figma MCP (커넥터 9961c0a8) | **연결됨 · 편집 됨** | kygstar77@gmail.com, 팀 "JUN의 팀" 스타터, 좌석 View(role admin) — 파이어맵 전용 여부 확인 안 함 | 스타터 요율 제한(공식 문서) | 전담 디자이너·디자인 개선 | whoami 통과 → create_new_file(드래프트) 성공 → use_figma로 사각형 1개 추가 성공. **View 좌석이어도 내 드래프트 파일은 편집 가능**. 팀 프로젝트 파일 편집은 시험 안 함. 시험 파일: figma.com/design/P6lkgYdYoEUl1tInvFnEkA (지워도 됨) |
| figma / mobbin (사용자 설정 MCP, http) | needs_auth | — | — | 없음 | 위 커넥터와 **중복**. 커넥터 쪽이 연결돼 있어 쓸 일 없음. 결재함 "Mobbin·Figma 연결 로그인" 항목은 로그인 문제가 아님 |
| Mobbin MCP (커넥터 17cbfd68) | **막힘(유료 필요)** | 계정 확인 안 함 | — | 전담 디자이너 | search_screens → "requires a paid plan". MCP는 모든 유료 요금제에 포함, 팀 요금제 연간 결제 시 1인 월 16달러(mobbin.com 검색 결과, 가격 페이지는 403이라 원문 확인 안 함) |
| 캔바 MCP (커넥터 48ffb38b) | 연결됨 · **파이어맵 사용 보류** | 이메일 확인 수단 없음. 소유 디자인 2개(2021-09 화장품·디저트 광고) — 스꾸 흔적은 없음, 파이어맵 것도 아님 | — | (보류) | search-designs(owned). 누구 계정인지 확정 못 함 → 지시대로 확정 전엔 안 씀 |
| vidIQ MCP | 연결됨 · **크레딧 거의 소진** | kygstar77@gmail.com | **2/150**, 갱신 2026-10-23 | 카피라이터·유튜브 총괄 | balance·user_channels. **우리 채널 미연결(channels 빈 목록)** — 연결 위젯은 사람이 눌러야 함 |
| 제미나이 텍스트 | **정상** | 키 파일 1개(gemini_key.txt, 2026-09-23 수정) — 스꾸 공유 여부 확인 안 함 | 429 없음 | 참모 3명·second_opinion·전 직원 | gemini-3-flash-preview 200, gemini-3.8-flash 200. **gemini-2.5-flash는 404(모델 없음)** — second_opinion·ytbreak·judge_thumb 예비 목록 끝에 남아 있음(맨 끝이라 실제 피해 없음) |
| 제미나이 TTS | **정상** | 위와 같음 | 429 없음 | 영상 PD | gemini-3.8-flash-tts 200. **gemini-2.5-flash-preview-tts는 400** — A-1/voice.py·sonpum2/tour_voice.py 예비 목록에 있음 |
| 제미나이 이미지 | **막힘(무료 없음)** | 위와 같음 | — | 비주얼·일러스트·모션 | gemini-2.5-flash-image 429 RESOURCE_EXHAUSTED. 공식 가격표상 **이미지 모델은 무료 등급 자체가 없다** → 기다려도 안 풀린다. 유료 1K 한 장: 2.5 Flash Image 0.039달러, 3.1 Flash Lite Image 0.0336달러, 3.1 Flash Image 0.067달러, 3 Pro Image 0.134달러 (ai.google.dev/gemini-api/docs/pricing) |
| 유튜브 업로드 토큰 (youtube_token.json) | **정상** | 파이어맵 채널(구독 39) | refresh token 있음, 갱신 성공(액세스 만료 00:35 → 자동 갱신) | 영상 PD·쇼츠 | ytupload.creds() + channels.list(mine) |
| 유튜브 분석 토큰 (youtube_analytics_token.json) | **정상** | 파이어맵 채널 | refresh token 있음, 갱신 성공 | 유튜브 총괄·카피라이터 | ytanalytics.creds() |
| 네이버 로그인 (naver_profile) | 쿠키 살아 있음 | 파이어맵 ID | NID_AUT·NID_SES 만료 **2026-10-26 23:34** (27일 남음) | 글쓰기·감시 | storage_state.json 쿠키 만료만 봄(가벼운 확인). **글쓰기 권한(logged_in deep)은 발행 잠금과 겹쳐 이번엔 안 봄** — 쿠키가 살아도 글쓰기만 401인 사례 있음(naver-write-ip-block). 블로그는 STOP_blog로 정지 중 |
| 쿠팡 파트너스 | 확인 안 함 | kygstar77@naver.com, ID AF9074391 | — | 작가·유튜브 | 크롬 로그인 유지 여부는 이번 회차에 못 봄(Chrome 확장 미사용). 다음 회차 |
| ChatGPT 웹 | 확인 안 함(로그인 여부) | **스꾸와 한도 공유**(결재함 기록) | 오늘 3건 기록(실사용 2, 0건 1) | 순돌이·디자이너 | gpt-usage.jsonl 기준. 이미지 생성 금지 유지 |
| Supabase 파이어맵 (c7cd8a90) | **정상** | 파이어맵 전용 | — | 제품·성장·보고 | firemap_events 24시간: screen_view 450, session_start 380, calc_complete 42 — 최신 23:22 |
| Cloudflare Pages retire-age-kr | **정상** | 파이어맵 | — | 제품 | retire-age-kr.pages.dev → firemap.kr 200, dev.retire-age-kr.pages.dev 200. origin/main 22:43, origin/dev 23:34 |
| Blender | **미설치** | — | — | 모션·일러스트 | 설치 흔적 없음(Program Files 폴더 없음, winget 목록에 없음). 설치는 파일 다운로드라 **사장님 채팅 허락 필요** — 결재함 |
| 스케줄 앱 예약 작업 | 정상 | — | — | 전원 | 최근 7회 실패 0건(전 직원). 상세는 staff.md |
| Metricool·Gmail·GitHub·Claude Docs 커넥터 | 연결됨 | 확인 안 함 | — | 확인 안 함 | 연결 상태만 봄(session_connectors_status) |

## 만료 달력
- 2026-10-23 vidIQ 크레딧 갱신(150)
- 2026-10-26 네이버 로그인 쿠키 만료 → 10-19에 '만료 임박'으로 올린다
