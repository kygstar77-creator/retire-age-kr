# 공개 저장소 노출 범위 — retire-age-kr (firemap-audit, 2026-10-08 20:02 실측)

기준: origin/main(41,385파일) · api.github.com 응답 private:false·visibility public·has_pages true(19:5x 재확인). 저장소 설정은 건드리지 않음.

## ① 비밀키·토큰 의심 — 우리 비밀키 노출 0건
| 무엇 | 결과 |
|---|---|
| functions/naver-token.js | 시크릿 없음. env.NAVER_CLIENT_ID·NAVER_CLIENT_SECRET(Cloudflare 설정)만 읽는다 |
| supabase/functions/kakao-auth/index.ts | 시크릿 없음. Deno.env(KAKAO_CLIENT_SECRET·SERVICE_ROLE_KEY)만 읽는다 |
| src/utils/kakaoAuth.js | 카카오 JS 키 1개 — 원래 브라우저에 공개되는 키(도메인 제한). 문제 아님 |
| src/utils/supabaseClient.js | sb_publishable 키 — 공개용 키. service_role·sb_secret 0 |
| _boss_*.txt | origin 모든 브랜치에 0. 3cc8448(_boss_msgs·_boss_recent)은 **로컬 브랜치 dev-secret-backup에만** 있음 — 그 브랜치를 push하면 안 됨 |
| 패턴 검색(origin/main 전체) | Google OAuth(ya29·GOCSPX·refresh_token) 0 · GitHub PAT 0 · Anthropic/OpenAI 키 0 · 개인키(BEGIN PRIVATE KEY) 0 · 네이버 쿠키 값 0(NID_AUT는 이름만, 4파일) |
| 걸린 것(남의 공개 값) | AIza 1건 = nongji1005/iq.html 안 남의 사이트 Firebase 웹 설정 · Bearer JWT 5건 = 퍼 온 페이지 안 livere 댓글 위젯 공개 토큰. 우리 키 아님 |

## ② 내부 문서 — 공개된 범위
- work/ 40,548파일, 그중 work/research/ 39,653파일·472폴더(대부분 yt 24,450·rt 1,394·visual 1,249·longform 921·cardshorts 804 = 수집 자료·작업물)
- **운영 내부 문서(공개 중):** meeting/ 58 · decisions/ 7 · admin/ 4(직원 고용 지시문 포함) · playbooks/ 41 · cloud/ 66 · brand/ 49 · editor/ 81 · work/research 바로 아래 md 54개 — approvals.md(결재함)·lessons.md·backlog.md·owner-lens.md·conductor-manual.md·revenue-strategy.md·strategy-2026-10.md·ops-cost.md·redteam-prompt.md·plan_2026-09-24~30 등
- 개인정보: 사장님 실명은 윈도 경로(C:/Users/…) 안에만 511파일, 경로 밖 0 · 계정 메일 kygstar77@gmail.com 8파일(요청 UA·결재 문구) · 휴대폰 번호 3개는 남의 공개 페이지를 퍼 온 것(toejikavg1006/moel_calc·cardshorts/e1_hynix_dd/compete_raw.json·yt/lessons_2026-09-23.md)

## ③ firemap.kr 배포처
- **firemap.kr = Cloudflare**(응답 server: cloudflare·CF-RAY, POST /naver-token이 Pages Function으로 응답 400 bad_json, wrangler.jsonc assets ./outputs/deploy).
- GitHub Pages는 **미리보기 사본**만: .github/workflows/pages.yml(main push → kygstar77-creator.github.io/retire-age-kr/, 같은 제목 200 OK).
- 비공개로 돌리면: 무료 요금제 GitHub Pages 미리보기는 멈출 수 있음(firemap.kr 본 사이트와 무관). Cloudflare가 이 저장소를 Git 연동으로 빌드하는지, 손 업로드(wrangler)인지는 **확인 안 함** — Git 연동이면 Cloudflare GitHub 앱 권한이 비공개 저장소까지 있는지 봐야 함.
