# 파이어맵 카페봇 (Cloudflare Worker)

지표·랭킹·인증 모음 글을 자동으로 만들어 `firemap_news`(kind=`auto`)에 넣고, 네이버 카페 토큰이 있으면 카페 '소식' 게시판에도 올려요. 앱의 소식 화면은 이 글에 `자동` 배지를 붙여 보여줘요.

파이어맵 전용이에요. 스꾸 등 다른 프로젝트의 Cloudflare 계정·KV·Supabase와 절대 섞지 않아요.

## 일정 (cron은 UTC)

| cron | KST | 글 |
| --- | --- | --- |
| `0 22 * * *` | 매일 07:00 | 아침 지표(코스피·S&P500·환율·기준금리·물가) |
| `0 9 * * 5` | 금요일 18:00 | 이번 주 랭킹(계산 인원·평균 파이어 나이·또래별) |
| `0 0 1 * *` | 매월 1일 09:00 | 지난달 인증 모음(개수·공감·단계 분포, 본문 인용 없음) |

하루 최대 2개만 올려요. KV(`CAFEBOT_KV`)에 날짜별 개수와 마지막 게시 기록을 남겨서 넘기면 건너뛰어요.
데이터가 비어 있으면(지표 없음, 계산 0명, 인증 0개) 글을 만들지 않아요.

## 비밀값 (전부 `wrangler secret put`, 파일에 적지 않기)

| 이름 | 설명 |
| --- | --- |
| `SUPABASE_URL` | 파이어맵 Supabase 프로젝트 URL (`cvhskxdwqubmshdgkzhj`) |
| `SUPABASE_SERVICE_KEY` | service_role 키. `firemap_news`는 service_role만 INSERT 가능(마이그레이션 `20260911091000_firemap_news.sql`) |
| `NAVER_CAFE_TOKEN` | 네이버 로그인 OAuth 액세스 토큰(카페 글쓰기 권한 포함) — 아래 주의 |
| `NAVER_CLUB_ID` | 파이어맵 카페 clubid (숫자) |
| `NAVER_MENU_ID_NEWS` | '소식' 게시판 menuid (숫자) |

`NAVER_*` 세 개가 하나라도 없으면 카페 게시는 건너뛰고 `firemap_news`에만 저장해요. 카페 API가 429(한도)·401(토큰 만료)을 돌려주면 로그만 남기고 그 회차는 넘어가요.

### 네이버 토큰은 반드시 공식 카페 계정(사장님)의 것

- 카페 글쓰기 API는 토큰 주인의 이름으로 글이 올라가요. 봇 전용 계정을 만들어 쓰면 카페 운영 정책 위반 소지가 있고, 공식 계정이 아닌 이름으로 '공지성' 글이 올라가 신뢰를 잃어요.
- 토큰은 파이어맵 카페 매니저(사장님) 네이버 계정으로 네이버 로그인 OAuth를 거쳐 발급받고, 만료되면 같은 계정으로 다시 발급해요. 절대 다른 사람 계정이나 봇 계정 토큰을 넣지 않아요.
- 토큰이 401을 내면 Worker 로그에 "사장님 계정으로 토큰 재발급 필요"가 찍혀요.

## 배포

```bash
cd workers/cafe-bot
npm i
npx wrangler kv namespace create CAFEBOT_KV      # 나온 id를 wrangler.toml의 REPLACE_WITH_KV_NAMESPACE_ID에
npx wrangler secret put SUPABASE_URL
npx wrangler secret put SUPABASE_SERVICE_KEY
npx wrangler secret put NAVER_CAFE_TOKEN
npx wrangler secret put NAVER_CLUB_ID
npx wrangler secret put NAVER_MENU_ID_NEWS
npx wrangler deploy
```

로컬에서 cron을 흉내 내려면:

```bash
npx wrangler dev --test-scheduled
curl "http://localhost:8787/__scheduled?cron=0+22+*+*+*"
```

배포된 Worker의 URL을 GET 하면 오늘 게시 개수와 마지막 게시 기록(JSON)만 돌려줘요. 게시는 cron으로만 일어나요.

## 글 형식

- 제목은 `[자동] `으로 시작해요(앱이 이 접두어와 `kind='auto'`로 자동 글을 구분해요).
- 본문은 해요체, 숫자 중심, 마지막 줄에 앱 링크. 지표 글엔 "지표는 참고만 해요"가 항상 붙어요.
- 인증 모음은 개수·공감·단계 분포만 집계해요. 사용자가 쓴 본문은 인용하지 않아요.
