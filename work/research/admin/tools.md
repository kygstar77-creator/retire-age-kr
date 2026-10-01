# 도구 장부 — 총무·인사팀(firemap-admin)
마지막 실측: **2026-10-01 17:2x**(운영실장 투입 회차 — 쿠팡·data.go.kr·Claude 한도 줄만) / **07:49** (2회차, 바뀐 줄만 고침 — 나머지는 1회차 23:39 값). 값은 전부 이 회차에 직접 호출해서 잰 것. 키·토큰 값은 적지 않는다.

| 도구 | 상태 | 계정(전용/공유) | 남은 한도·만료 | 누가 쓰나 | 확인 방법 · 비고 |
|---|---|---|---|---|---|
| Figma MCP (커넥터 9961c0a8) | **연결됨 · 편집 됨** | kygstar77@gmail.com, 팀 "JUN의 팀" 스타터, 좌석 View(role admin) | 스타터 요율 제한 | 전담 디자이너·디자인 개선 | 10-01 07:4x whoami 재확인 같음. 편집 시험은 1회차 통과 |
| figma / mobbin (사용자 설정 MCP, http) | needs_auth | — | — | 없음 | 위 커넥터와 **중복**. 커넥터 쪽이 연결돼 있어 쓸 일 없음. 결재함 "Mobbin·Figma 연결 로그인" 항목은 로그인 문제가 아님 |
| Mobbin MCP (커넥터 17cbfd68) | **막힘(유료 필요)** | 계정 확인 안 함 | — | 전담 디자이너 | search_screens → "requires a paid plan". MCP는 모든 유료 요금제에 포함, 팀 요금제 연간 결제 시 1인 월 16달러(mobbin.com 검색 결과, 가격 페이지는 403이라 원문 확인 안 함) |
| WWIT(wwit.design) — Mobbin 무료 대안 | **정상 · 무료·가입 없음** | 계정 없음 | — | 전담 디자이너·제품 개발 | 2026-10-01 AI 연구소가 curl로 시험함(목록·화면 원본 webp 200). 한국 금융 앱 14개. 참고만 하고 산출물에 넣지 않음. 보조: 유아이볼(무료는 최신 3개, Pro 월 14,000원). ai-lab/bench/2026-10-01-mobbin-alternatives.md |
| 캔바 MCP (커넥터 48ffb38b) | 연결됨 · **파이어맵 사용 보류** | 이메일 확인 수단 없음. 소유 디자인 2개(2021-09 화장품·디저트 광고) — 스꾸 흔적은 없음, 파이어맵 것도 아님 | — | (보류) | search-designs(owned). 누구 계정인지 확정 못 함 → 지시대로 확정 전엔 안 씀 |
| vidIQ MCP | 연결됨 · **크레딧 거의 소진** | kygstar77@gmail.com | **2/150**, 갱신 2026-10-23 | 카피라이터·유튜브 총괄 | 10-01 07:4x 재확인 같음. 우리 채널 미연결. 유료 플랜은 휴대폰 결재 **반려**(07:02) → 무료 2크레딧은 아껴 쓴다 |
| 제미나이 텍스트 | **정상(19:0x 재측정)** | 키 파일 1개(KEY= 형식) — 스꾸 공유 여부 확인 안 함 | 10-01 19:0x 3.5-flash·flash-latest·3-flash-preview·3.5-flash-lite·flash-lite-latest 전부 200(07:45엔 flash 전부 429 → 일일 한도 리셋 뒤 회복) | 참모 3명·second_opinion·전 직원 | 일일 무료 한도라 낮 사용량 많으면 다시 429 — 그때 lite 예비 그대로 |
| 제미나이 TTS | **정상(19:0x)** | 위와 같음 | 10-01 19:0x gemini-3.8-flash-tts 200(07:45엔 429) | 영상 PD | 영상 목소리 작업 가능 — 일일 한도 공유라 텍스트 대량 호출과 겹치면 다시 막힘 |
| 제미나이 이미지 | **막힘(무료 없음)** | 위와 같음 | — | 비주얼·일러스트·모션 | 10-01 19:0x 2.5-flash-image 여전히 429. 결재함 휴대폰 결정 **보류**(07:03) |
| 유튜브 업로드 토큰 (youtube_token.json) | **정상** | 파이어맵 채널(구독 39) | refresh token 있음, 갱신 성공(액세스 만료 00:35 → 자동 갱신) | 영상 PD·쇼츠 | ytupload.creds() + channels.list(mine) |
| 유튜브 분석 토큰 (youtube_analytics_token.json) | **정상** | 파이어맵 채널 | refresh token 있음, 갱신 성공 | 유튜브 총괄·카피라이터 | ytanalytics.creds() |
| 네이버 로그인 (naver_profile) | 쿠키 살아 있음 | 파이어맵 ID | NID_AUT·NID_SES 만료 **2026-10-26 23:34** (27일 남음) | 글쓰기·감시 | storage_state.json 쿠키 만료만 봄(가벼운 확인). **글쓰기 권한(logged_in deep)은 발행 잠금과 겹쳐 이번엔 안 봄** — 쿠키가 살아도 글쓰기만 401인 사례 있음(naver-write-ip-block). 블로그는 STOP_blog로 정지 중 |
| 쿠팡 파트너스 | **본인인증 완료(10/1 17:04 사장님)** | kygstar77@naver.com, ID AF9074391 | — | 유튜브 루프·제품 개발 | 링크 발급은 youtube-loop 17:40 지시. 쿠팡 인플루언서(influencers.coupang.com) 첫 화면 PC 크롬 열림 17:2x, 신청은 결재함 14행 |
| data.go.kr(공공데이터포털) | **크롬 로그인 풀림** | 계정 있음(키 1개), 로그인 방식 확인 안 함 | — | 기획자·신사업 | 10/1 17:2x 마이페이지 → 로그인 화면, 아이디 로그인에 보안문자 → 무인 불가. TourAPI·고캠핑 활용신청은 결재함 줄(사장님 손) |
| Claude 주간 한도 | **62%** (10/1 17:20) | 스꾸와 공유 | 리셋 10/4 21:00 KST · 하루 약 30%p → 90% ≈ 10/2 15:40 | 전 직원 | get_usage. 추가 사용량 꺼짐. admin/usage.md |
| ChatGPT 웹 | 확인 안 함(로그인 여부) | **스꾸와 한도 공유**(결재함 기록) | 오늘 3건 기록(실사용 2, 0건 1) | 순돌이·디자이너 | gpt-usage.jsonl 기준. 이미지 생성 금지 유지 |
| Supabase 파이어맵 (c7cd8a90) | **정상** | 파이어맵 전용 | — | 제품·성장·보고 | firemap_events 24시간: screen_view 450, session_start 380, calc_complete 42 — 최신 23:22 |
| Cloudflare Pages retire-age-kr | **정상** | 파이어맵 | — | 제품 | retire-age-kr.pages.dev → firemap.kr 200, dev.retire-age-kr.pages.dev 200. origin/main 22:43, origin/dev 23:34 |
| Blender | **설치됨 · 시험 통과** | — | — | 모션·일러스트 | 10-01 16:49 확인: winget BlenderFoundation.Blender 5.2.1 LTS 설치 성공(관리자 승인 통과). 경로 `C:\Program Files\Blender Foundation\Blender 5.2lender.exe`. `blender -b --factory-startup -P 스크립트`로 320×180 렌더 1장 저장 성공(17초) |
| 스케줄 앱 예약 작업 | 정상 | — | — | 전원 | 최근 7회 실패 0건(전 직원). 상세는 staff.md |
| Metricool·Gmail·GitHub·Claude Docs 커넥터 | 연결됨 | 확인 안 함 | — | 확인 안 함 | 연결 상태만 봄(session_connectors_status) |

## 만료 달력
- 2026-10-23 vidIQ 크레딧 갱신(150)
- 2026-10-26 네이버 로그인 쿠키 만료 → 10-19에 '만료 임박'으로 올린다
| 네이버 오픈API(개발자센터) | **앱 있음 · 키 파일 없음** | 앱 '파이어맵'(파이어맵 네이버 ID) | 10-01 19:1x 앱 목록 확인, 데이터랩 API 상태 정상. 비밀값 꺼내기는 무인 권한 검사에 막힘 → 결재함 | (예정) 데이터랩 검색어트렌드 연령·성별 | 사장님이 naver_openapi.txt 저장하면 다음 회차에 호출 시험 |
