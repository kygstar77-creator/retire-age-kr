# FIREMAP (파이어맵) — 인수인계 문서 (HANDOFF)

> 이 문서 하나 + GitHub 저장소만 있으면 새 담당자(또는 다른 Claude 계정)가 FIREMAP을 그대로 이어받을 수 있도록 작성했습니다.
> 최종 갱신: 2026-06-15

---

## 0. 한 줄 요약

**FIREMAP(파이어맵, firemap.kr)** 은 한국 사용자가 "내 자산·생활비로 몇 살에 파이어(조기은퇴) 가능한지"를 1분에 계산하고, 물가·국민연금·건강보험료·세금까지 현실적으로 반영하는 React + Vite 웹앱입니다. 또래 순위·절약/적립 기록·해외체류·배당 현금흐름 등 부가 기능을 갖춘 PWA이며, Supabase(익명 점수/피드백)와 GitHub Actions→GitHub Pages(+Cloudflare) 배포를 씁니다.

---

## 1. 저장소 · 라이브 · 배포

| 항목 | 값 |
|---|---|
| GitHub 저장소 | `https://github.com/kygstar77-creator/retire-age-kr` |
| 운영 URL | `https://firemap.kr` (커스텀 도메인) |
| 운영 브랜치 | `main` (push 시 자동 배포) |
| 동기화 브랜치 | `firemap-v3` (main과 동일하게 유지 중) |
| 프리뷰 | `https://firemap-v3.retire-age-kr.pages.dev/` (Cloudflare Pages 프리뷰) |
| 배포 방식 | `.github/workflows/pages.yml` — main에 push → `npm install` → `npm run build` → `outputs/deploy`를 GitHub Pages로 배포 |
| 부가 배포설정 | `wrangler.json` / `wrangler.jsonc` — Cloudflare가 `./outputs/deploy`를 서빙(SPA) |
| Node | 22 (CI 기준) |

**배포 검증법:** push 후 1~2분 뒤 `https://firemap.kr/assets/index-XXXX.js` 가 로컬 빌드 산출물(`outputs/deploy/assets/index-*.js`)과 같은 해시로 200을 반환하면 반영 완료. (Vite 콘텐츠 해시라 같은 해시면 같은 코드)

---

## 2. 기술 스택 · 실행/빌드

- **프론트엔드:** React + Vite (vite v8 / rolldown), 순수 JSX, 단일 SPA. 상태는 React useState (외부 상태관리 없음).
- **백엔드(서버리스):** Supabase REST (익명 점수 랭킹 `firemap_scores`, 피드백 `firemap_feedback`, 사용자 상태 동기화). 마이그레이션은 `supabase/migrations/`.
- **분석/광고:** Google Analytics(`G-SYD7WCD35C`), Google AdSense(`ca-pub-3225798545626010`).
- **QA:** Playwright 모바일 테스트(`npm run qa:mobile`), 시뮬레이터 회귀 테스트(`work/test-simulator.mjs`, build 전 prebuild로 자동 실행).

```bash
npm install
npm run dev      # 로컬 개발 (http://localhost:5173)
npm run build    # 정적 산출물 → outputs/deploy (prebuild로 시뮬레이터 테스트 먼저 통과해야 함)
```

`npm run build` 파이프라인: `test-simulator.mjs`(회귀) → `build-deploy.mjs`(vite build) → `fix-ads-txt` → `fix-ga` → `fix-branding-og` → `fix-share-panel` → `gen-seo`(sitemap/robots).

---

## 3. 아키텍처 · 파일 지도

### 루트
- `src/components/FireMapMVP.jsx` — **앱의 심장.** 화면 라우팅(hash 기반), `inputs` 상태 보유, 두 개의 시뮬레이션 생성:
  - `simulation = buildSimulation(inputs)` → **개인 결과(세금 반영)**
  - `rankingSimulation = buildSimulation({...inputs, investType:0})` → **랭킹/점수(세전 공정)**
  - `onChange(key,value)` (함수형 업데이트), `applyPatch(patch)` (도구 반영용).

### 화면/컴포넌트 (`src/components/firemap/`)
- `Home.jsx` — 비로그인 홈(계산 시작 + 최근결과 칩 + 로그인 바 `IdentityLine`). 로그인+결과 있으면 `FirePlan`(대시보드) 렌더.
- `FirePlan.jsx` — 홈 대시보드(자산추이·다음할일·한국제도 반영 요약: 국민연금/물가/건보료/세금 + 끄기 링크).
- `Question.jsx` — 입력 질문 플로우.
- `Result.jsx` — 결과 히어로(파이어 나이·등수·세전 안내), 자산차트, 해자카드(건보료/세금), 공유.
- `Experiment.jsx` — **바꿔보기**(슬라이더 미리보기 샌드박스, draft에서 굴리고 "저장" 눌러야 실제 반영). `PensionControls`, 세금/수익률 섹션 포함.
- `DependentCheck.jsx` — **건보료** 도구(피부양자 판정+지역가입 추정, 반영/해제 토글).
- `TaxPensionModules.jsx` — `ForeignStockTaxCard`(해외 양도세), `DividendCard`(배당세), `PensionEarlyClaimCard`(국민연금 조기수령). 전부 반영/해제 토글.
- `DividendLifeCalc.jsx` — **파이어 후 현금흐름**(배당 인출소득 계산→`dividendIncomeMonthly`로 반영, 성장률 슬라이더).
- `Savings.jsx` — 적립/절약 기록(저축 랭킹 포함).
- `City.jsx` / `CityExplorer.jsx` — 해외체류·지역 비교.
- `Leaderboard.jsx` — 전체/또래 랭킹(세전 기준).
- `Share.jsx`, `Community.jsx`, `Tools.jsx`, `AccountCard.jsx`, `IdentityLine.jsx`, `PensionControls.jsx`, `DailyFire.jsx` 등.

### 엔진/유틸
- `src/utils/retirementSimulator.js` — **핵심 시뮬레이터.** `defaultInputs`, `normalizeInputs`(국민연금 조기수령 실효값 계산 포함), `buildSimulation`.
- `src/firemap-v2/` — `healthInsurance.js`(건보료 추정), `pension.js`(`earlyClaim` 조기수령 감액), `rank.js`/`stats.js`(순자산 백분위), `formatters.js`, `data.js`, `screens.js`(화면/탭 정의), `scenarios.js`, `dailyData.js`(이벤트 트래킹), `rankHistory.js`.
- `src/utils/firemap*Api.js` — Supabase 연동(scores/save/state/account/feedback). `identity.js`(익명 client id/계정), `assetHistory.js`, `shareState.js`(공유 URL 인코딩), `taxCalculator.js`, `savingsEngine.js`.

---

## 4. 시뮬레이션 모델 (가장 중요 — 계산 로직)

`defaultInputs` 주요 필드: `currentAge, targetRetirementAge, financialAsset, monthlyLivingCost, annualReturnRate, inflationRate, expectedPensionAge, expectedMonthlyPension, partTimeIncomeAfterRetirement, simulationUntilAge, healthInsuranceEnabled, monthlyHealthInsurance, overseas*, investType, dividendYield, dividendIncomeMonthly, dividendIncomeGrowth, pensionClaimAge`.

연도별 루프(은퇴 후): `인출액 = max(0, 생활비(+건보료) − 부업소득 − 국민연금 − 배당인출소득)` 후 세금 차감·수익률 적용.

### 세금/소득 반영 규칙 (서로 중복 없이 정리됨)
- **건강보험료** (`healthInsuranceEnabled`+`monthlyHealthInsurance`): 매년 비용으로 가산. 독립적. 도구(DependentCheck)에서 반영/해제.
- **투자유형 세금** (`investType`): `0` 국내(면제) · `1` 해외 양도세 22%(매도 차익분, 250만 공제) · `2` 배당세 15.4%(자산×배당률, 재투자 가정) · `3` 둘 다(독립 가산). 양도세는 **매년 인출액 기준 동적 계산**.
- **배당 인출소득** (`dividendIncomeMonthly`, 세후 / `dividendIncomeGrowth` 성장률): 부업소득과 **별도 칸**으로 인출을 줄임. **배당세(investType 2/3)와 상호배타**(같은 배당 이중계산 방지 — UI에서 한쪽 켜면 다른쪽 자동 해제).
- **국민연금 조기수령** (`pensionClaimAge`): 정상 연금(`expectedPensionAge`/`expectedMonthlyPension`)은 **baseline로 보존**. `normalizeInputs`에서 `pensionClaimAge`가 정상보다 이르면 `earlyClaim`(연 6%, 최대 30% 감액)으로 실효 연금만 감액. 늦으면 그 나이부터(증액 미반영). **도구(PensionEarlyClaimCard)와 바꿔보기(PensionControls)가 같은 `pensionClaimAge`를 공유**.

### 랭킹 공정성 (중요)
- **순자산 백분위**(또래 상위 %)는 `netWorth` 기반 → 세금과 무관.
- **"가장 빨리 파이어" 리더보드**(Supabase 제출)는 `rankingSimulation`(=`investType:0`, 세전) 기준으로 제출/조회 → 양도·배당세 선택과 무관하게 공정. 개인 결과 히어로는 세금 반영값, 세금 적용 시 "등수는 세전 N세 기준" 안내 표시.

---

## 5. 반영 도구 UX 규칙 (일관성)

결과에 반영되는 도구 5종(**건보료 · 양도세 · 배당세 · 배당인출소득 · 국민연금 조기수령**)은 모두 동일 패턴:
- 버튼: 미반영 시 "…계산에 반영하기", 반영 시 **"✓ 반영됨 · 해제(또는 되돌리기)"** 토글.
- **결과로 자동 이동하지 않고 도구에 잔류** (여러 개 차례로 켠 뒤 결과를 한 번에 확인).
- 홈 대시보드(FirePlan)의 건보료·세금 줄에서도 "…반영 · 끄기 ›"로 도구에 진입해 해제 가능.
- **바꿔보기(Experiment)** 는 "미리보기 샌드박스" — 슬라이더로 즉시 미리보기, "이 조건을 내 결과로 저장"을 눌러야 실제 반영. `investType`·`dividendYield`는 PREVIEW_ONLY(저장 안 됨), 나머지(연금·부업·배당인출 등)는 저장됨.

---

## 6. 로그인 · 데이터 모델

- **전략(직방·삼쩜삼식):** 계산·결과는 비로그인 무료, **저장된 개인 대시보드/커뮤니티 글쓰기**는 로그인. 홈 상단 `IdentityLine`("닉네임 만들고 기록 지키기 · 로그인 →")로 진입.
- 익명 식별자(`identity.js`)로 점수 제출. 로그인 시 입력값·자산추이를 Supabase로 동기화(개인정보처리방침상 원본 민감 금액 일부 제외 정책). 로그아웃 시 기기 개인데이터 삭제(서버 백업 후 복원 가능).
- 컴플라이언스: 면책에 "금융투자업·투자자문업·유사수신업 아님, 자금 예치·운용·상품 판매 안 함" 명시. (법률 검토는 별도 권장 — 변호사 검토 1회 권함)

---

## 7. 제품 · 의사결정 기록 (왜 이렇게 했는가)

- **결과=세금 반영 / 랭킹=세전 공정.** 개인이 보는 파이어 나이엔 본인 세금·건보료 반영, 남과 겨루는 등수는 모두 세전이라야 공정.
- **투자유형 단일 모델(택1, 단 해외+배당 동시는 `investType=3`).** 포트폴리오 비율 세분화는 의도적으로 안 함(단순성).
- **배당세(재투자) ↔ 배당인출소득 상호배타.** 같은 배당을 재투자 드래그와 인출소득으로 동시에 세면 모순이라 차단.
- **부업소득 / 배당인출소득 별도 필드.** 예전엔 같은 칸이라 덮어쓰기 발생 → 분리해 합산.
- **국민연금 정상/조기 분리(baseline 보존).** 예전엔 도구가 정상값을 덮어써 재적용 시 감액 누적 버그 → `pensionClaimAge`로 분리해 해결, 바꿔보기와 동기화.
- **반영 버튼 전부 도구 잔류·토글로 통일.** (현금흐름만 결과로 튀던 동작 제거.)
- **공유/OG 프레임을 "등수 자랑"→"현실 계산"으로** (앱 내부 완료). ※ 정적 index.html OG 메타는 아직 일부 랭킹 프레임 잔존(아래 한계 참고).
- **홈 "다음 할 일"에서 자산기록 항목 제거** (바로 위 카드와 중복이라).

---

## 8. 자격증명 · 계정 이전 가이드 (신규 담당자/계정)

> 코드는 GitHub에 있으므로 "이전"의 핵심은 **저장소 권한 + 외부 서비스 소유권 + 새 토큰 발급**입니다.

### (1) GitHub
- 저장소 `kygstar77-creator/retire-age-kr`. 이전 방법 둘 중 하나:
  - **권한만 부여:** Settings → Collaborators에 새 계정 추가(가장 간단).
  - **소유권 이전:** Settings → Danger Zone → Transfer ownership.
- 새 담당자(또는 새 Claude)는 **fine-grained PAT**(권한: 해당 repo Contents read/write) 발급 후 push에 사용.
- ⚠️ **현재 채팅에 노출된 기존 토큰은 즉시 폐기(revoke)하세요.** (Settings → Developer settings → Personal access tokens)

### (2) Supabase (랭킹/피드백/동기화)
- 클라이언트에 기본 URL/anon key가 하드코딩(공개 anon 키): `firemapScoresApi.js` 등. 환경변수 `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`로 override 가능.
- 프로젝트(현재 ref: `cvhskxdwqubmshdgkzhj`) 소유권/멤버를 새 계정에 이전하거나 새 Supabase 프로젝트 생성 후 `supabase/migrations/`(scores·feedback 테이블) 적용하고 URL/anon key 교체. RLS 정책 확인 필요.

### (3) GitHub Pages / Cloudflare / 도메인
- 배포는 GitHub Actions(Pages)로 자동. Pages 설정은 저장소와 함께 이동.
- `wrangler.json(c)`는 Cloudflare Pages용. Cloudflare 계정 사용 중이면 프로젝트/도메인 연결을 새 계정에 위임.
- **도메인 `firemap.kr`** 은 도메인 등록처(레지스트라) 계정에서 소유권/DNS 이전 필요.

### (4) 분석/광고
- GA: `G-SYD7WCD35C` (`work/fix-ga.mjs`). 새 GA 속성으로 바꾸려면 이 값 교체.
- AdSense: `ca-pub-3225798545626010` (`work/build-deploy.mjs`, ads.txt). 새 퍼블리셔 ID로 교체 + 승인 필요.
- OG 이미지 버전: `work/fix-branding-og.mjs`의 `ogVersion`.

### (5) 새 Claude 계정 시작 체크리스트
1. 저장소 클론 → `npm install` → `npm run build` 통과 확인.
2. 위 자격증명(특히 GitHub PAT) 새로 준비.
3. 이 문서(특히 §4 시뮬레이션 모델, §5 도구 UX 규칙, §7 의사결정) 숙지.
4. 변경 → `npm run build`(회귀 테스트 통과) → `main`에 push → 라이브 해시 확인(§1).

---

## 9. 남은 작업 · 알려진 한계

**남은 작업(보류/외부 계정 필요):**
- 소셜 로그인(카카오·구글 OAuth) — OAuth 앱 등록 필요(보류).
- AdSense 승인, 프리미엄 PDF·토스페이먼츠 결제 — 계정/키 필요.
- 환율 주간 자동갱신 cron(`work/refresh-data.mjs`) — workflow 권한 토큰 필요.
- 정적 index.html OG 메타가 일부 "또래 중 내 FIRE 등수는?"(랭킹) 프레임으로 남아 있음(`fix-branding-og.mjs`) — 현실계산 프레임으로 교체 권장.
- 동적 OG(공유 URL별 이미지)는 엣지 렌더 필요(현재 정적 + 등급카드 이미지로 대체).

**모델 한계(근사 시뮬레이터임):**
- 세금은 근사 — 누진구간·금융소득종합과세·지방세·계좌별 절세(ISA/연금계좌) 단순화.
- 배당률·수익률·물가·배당성장은 사용자 가정값(미래 보장 X).
- 투자유형 단순화(국내/해외/배당), 포트폴리오 비율 세분화 없음.
- 연기연금 증액 미반영, 부동산·대출은 순자산엔 반영되나 인출 모델엔 제한적.
- 법률/세무는 전문가 검토 권장.

---

## 10. 빠른 참조 (명령어)

```bash
git clone https://github.com/kygstar77-creator/retire-age-kr.git
cd retire-age-kr && npm install
npm run dev                 # 개발
npm run build               # 빌드(+회귀 테스트)
# 변경 후:
git add -A && git commit -m "..."
git push origin main        # → 자동 배포(GitHub Actions)
```

— 끝 —
