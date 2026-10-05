# 신사업 새 사이트 키트 (firemap-venture-builder, 2026-10-01 07:25~07:34)

지시서가 오면 이 키트로 **몇 시간 안에** 첫 판을 낸다. 전부 운영에서 실측으로 확인했다.

## 1. 배포 길
| 길 | 주소 | 상태 | 확인 |
|---|---|---|---|
| ① 파이어맵 저장소 안 경로 | `public/<경로>/index.html` → `https://firemap.kr/<경로>/` | **됨** | 07:3x `public/kit/demo/` 올려 push 후 약 2분 40초 만에 운영 200. 절차: dev에서 `npm run build`(테스트·lint 포함) 통과 → 내 파일만 `git commit -- <경로>` → `git push -q origin dev:main` → Cloudflare가 main을 빌드 |
| ② 독립 무료 주소 — GitHub Pages | `https://kygstar77-creator.github.io/<저장소>/` | **가능(선례 있음)** | GitHub MCP 로그인 = kygstar77-creator(get_me). 같은 계정의 duo-memo가 `kygstar77-creator.github.io/duo-memo/`로 200. 새 저장소는 MCP `create_repository`로 만들 수 있으나 **Pages 켜기 도구가 MCP에 없다** — `kygstar77-creator.github.io` 이름의 사용자 사이트 저장소는 만들면 자동 공개되는 것으로 알려져 있음(확인 안 함). 필요해지면 그때 만들고 실측 |
| ② 독립 무료 주소 — Cloudflare *.pages.dev | — | **막힘** | 이 PC에 wrangler CLI 없음·로그인 흔적 없음. 계정 로그인은 하지 않는다 → 필요하면 결재함에 "사장님 1회 로그인" 요청 |
| 새 도메인 | — | 결재 필요 | approvals.md에 비용·이유 올린 뒤 |

주의(①): `/x.html`은 빌드 후 `/x`로 바뀐다(fix-seo-links). noindex 페이지는 사이트맵에서 자동 제외(gen-seo). `functions/_middleware.js`는 `/`와 toolPages 경로만 건드리므로 새 폴더 경로는 그대로 나간다. GA·애드센스 스크립트는 **자동으로 붙지 않는다**(데모에서 확인) — 붙일지는 사이트마다 정한다(애드센스 재심사 중).

## 2. 파일
- `public/kit/fmkit.js` — 운영 주소 `https://firemap.kr/kit/fmkit.js`. 의존성 0.
  - `FMKit.init({site, lang})` → `session_start`(utm_*·ref 호스트·화면 폭)
  - `FMKit.log(event, props)` → 모든 이벤트에 `site·lang·path`, `?fm_internal=1` 기기는 `internal:1`, firemap.kr 밖이면 `host`
  - `FMKit.share({title, big, sub, brand, url, text, accent})` → 1080×1080 결과 카드 PNG → 파일 공유 → 링크 공유 → 링크 복사 → 이미지 저장 순. 공유 링크에 `utm_source=share&utm_medium=<site>` 자동. `share_open`/`share_done{method}` 기록
- `template-ko.html` / `template-en.html` — 빈 템플릿. `{{…}}` 채우고 `compute()`만 구현. 본문이 JS 없이 첫 HTML에 있다(체크리스트 16), 숫자1+행동1·다크카드1·색4(디자인 정체성), 320px 넘침 없음, 다크 모드, 면책 문구, hreflang 자리. 영어 바닥 `{{BUCKET_LABEL}}` = FMKit.log로 보내는 구간 이름(예: salary band). fmkit이 구간을 보내므로 'numbers stay in your browser'만 쓰면 거짓(editor-en 10/1).
- `public/kit/demo/` — noindex 점검 페이지(`https://firemap.kr/kit/demo/?fm_internal=1`). 배포·측정 회귀 확인용. 제품 아님.

## 3. 측정 보기 (Supabase c7cd8a90, 표 firemap_events, 시각 열은 `ts`)
```sql
select event, count(*) from firemap_events
where props->>'site'='<SITE_ID>' and coalesce(props->>'internal','0')<>'1' and props->>'host' is null
group by 1;
```
운영 실측 07:32(UTC 22:32): kit-demo `session_start{w,utm_source}`·`calc_submit{bucket}` 두 줄 들어옴, internal:1 정상.

## 4. 금지 (지시서와 무관하게 항상)
- 입력 원값(금액·이름·생일)을 이벤트에 넣지 않는다 — 구간(bucket)만.
- 금융상품 권유 문구 금지, 제휴 링크는 대가성 문구를 링크 바로 위에.
- 템플릿을 찍어 같은 틀 페이지를 대량으로 만들지 않는다(애드센스·구글 scaled content).

## 5. 발견 (IndexNow — 사람 손 0, 2026-10-05 13:34 실측)
- 키: 사용자 사이트 루트 `https://kygstar77-creator.github.io/7fac259e36e5f4929ac442e7d451b11f.txt` → 200, 본문 = 파일 이름과 같은 32자 16진수 → **IndexNow 키 맞음**(키 파일 형식). 키는 공개 파일이라 비밀 아님.
- 제출 대상 = 두 사이트 sitemap.xml에 있는 URL 전부 5개(uk-take-home-pay 4: `/`·`/60-percent-tax-trap/`·`/privacy/`·`/about/`, exam-dates-kr 1: `/hanneunggeom/`). `/exam-dates-kr/`·`/exam-dates-kr/privacy/`·사용자 사이트 `/`는 noindex라 뺐다.
- POST JSON(host·key·keyLocation·urlList) 응답 코드 13:34:38~57:
  | 받는 곳 | 코드 |
  |---|---|
  | api.indexnow.org | 200 |
  | www.bing.com/indexnow | 200 |
  | yandex.com/indexnow | 202 (`success:true`, 키 확인 중) |
  | searchadvisor.naver.com/indexnow | 200 (공식 표 '200 Success') |
- **네이버 IndexNow 지원 = 공식 확인**: 네이버 서치어드바이저 가이드 `searchadvisor.naver.com/guide/indexnow-request`(GET `?url=&key=`·POST `/indexnow` JSON, 응답표 200/202/400/403/422/429)와 indexnow.org 참여 엔진 목록(searchengines.json에 naver, `searchadvisor.naver.com/indexnow/meta.json`). 서치어드바이저 사이트 등록이 먼저 필요한지는 **확인 안 함**(가이드 본문에서 찾지 못함).
- 구글은 IndexNow 참여 엔진 목록에 없다 → 구글 색인은 서치콘솔 속성(growth [요청], approvals 13행)·들어오는 링크가 길. 이 제출로 구글 site: 0쪽은 안 바뀐다.
- 다음 회차: 페이지가 바뀔 때마다(deploy.py·daily Actions) 같은 POST를 다시 보낸다 → `kit/indexnow.py`로 묶기(backlog). 효과 측정 = 3일 뒤 bing `site:` 수.
- 기준선 13:35: bing `site:kygstar77-creator.github.io` curl 결과에서 주소 0개(봇 차단 결과인지는 확인 안 함 — 3일 뒤 같은 방법으로 비교).
