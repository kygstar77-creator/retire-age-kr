# 외부 데이터 연동 — 소스·키·폴백 (firemap)

데이터는 **추가전용**(기존 행/컬럼/RPC 무변경, 새 컬럼 nullable). 키가 없으면 graceful 폴백(해당 항목만 건너뛰고 기존 값 보존).

## 지금 자동으로 수집되는 것 (키 불필요 또는 키 설정 완료)

| 지표 | 소스 | 키 | 저장 위치 | 수집기 | 주기 |
|---|---|---|---|---|---|
| 주가지수(S&P500 등)·환율 | Yahoo Finance / er-api | 불필요 | `firemap_market` | `fetch-market` | 일(cron) |
| 물가상승률(연) | World Bank | 불필요 | `firemap_cpi` | `fetch-macro` | 주(cron) |
| 예금금리 | World Bank | 불필요 | `firemap_rates(deposit_12m)` | `fetch-macro` | 주 |
| **기준금리** | **한국은행 ECOS** | `ECOS_API_KEY` (설정됨) | `firemap_rates(base_rate)` | `fetch-macro` | 주 |
| **물가지수·물가상승률(월)** | **한국은행 ECOS 901Y009** | `ECOS_API_KEY` (설정됨) | `firemap_cpi(source=ecos, 월별)` | `fetch-macro` | 주 |

노출: 지역·가구 플랜 페이지(`/guide/region-plan/*`) "거시 지표(참고)" 줄, 홈 여정 허브 월간 점검 카드, 상단 마퀴(시장).

## 키가 있어야 켜지는 것 (현재 dormant, 준비 완료)

### 1) 국토부 아파트 실거래가 — `MOLIT_API_KEY`  ← 사이트에 표시 자리 연결됨
- 받는 곳: 공공데이터포털(data.go.kr)에서 아래 **두 API**를 활용신청 → 일반 인증키(Encoding) 1개 발급(같은 키로 둘 다 사용).
  - **국토교통부_아파트 매매 실거래가 상세 자료** (`getRTMSDataSvcAptTradeDev`)
  - **국토교통부_아파트 전월세 실거래가 자료** (`getRTMSDataSvcAptRent`) — 전세(월세 0) 평균에 사용
- 넣는 곳: Supabase → Project Settings → Edge Functions → Secrets에 `MOLIT_API_KEY` 추가. **키는 사용자가 직접 넣어야 합니다(보안상 대신 입력 불가).**
- 동작: 수집기 `fetch-realestate`가 대표 20개 도시(서울·부산·대구·인천·광주·대전·울산·세종·수원·성남·고양·용인·청주·천안·전주·창원·포항·제주시·강릉·춘천)의 **대표 자치구 평균 매매가·전세 보증금**을 전월 기준으로 `firemap_realestate`에 적재. 키 없으면 `{skipped:{all:"no MOLIT_API_KEY"}}`로 무동작.
- 키 적용 후: `fetch-realestate`를 1회 호출(또는 cron 등록)하면 적재. RPC `fm_realestate_latest()`로 조회.
- **표시되는 곳(자동 연결됨)**: `firemap_realestate`에 데이터가 들어오면, 빌드 시 아래 페이지에 자동 노출돼요(데이터 없으면 줄 자체가 숨겨짐 — 폴백).
  - `/guide/regions/<도시>` 지역 페이지: "🏠 OO 아파트 실거래 평균 — 매매 X억 · 전세 Y억 (YYYY.MM · 국토부 실거래가)" 박스
  - `/guide/region-plan/<지역>-<가구>-<유형>` 페이지: 거시 지표 줄 아래 같은 한 줄
  - (도시명이 위 20개 목록에 매핑된 지역만 표시. 매핑 없는 지역은 미표시 — LAWD 코드 추가로 확장 가능.)

### 2) 통계청 KOSIS (가구 소득·지출 등 세부) — `KOSIS_API_KEY` (선택)
- 받는 곳: KOSIS 공유서비스(kosis.kr) → OpenAPI 활용신청 → 인증키.
- 넣는 곳: Supabase Edge Functions Secrets에 `KOSIS_API_KEY`.
- 비고: CPI·금리는 이미 ECOS로 충분. KOSIS는 가구 소득분위·소비지출 등 **추가 디테일**이 필요할 때 확장용. (수집기는 키 확보 후 ECOS 패턴으로 추가 예정.)

## 키 적용 후 흐름(공통)
1. Supabase Secrets에 키 추가 → 2. 해당 edge function 1회 호출(pg_net 또는 대시보드) → 3. 테이블 적재 확인 → 4. 다음 빌드/배포 시 정적 페이지에 반영, 앱은 RPC로 즉시 반영.

## 안전 원칙
- 모든 수집은 실패 시 해당 항목만 건너뛰고 기존 값 보존(graceful).
- 쓰기는 service_role(edge function 내부)만. 앱은 SECURITY DEFINER RPC로 읽기만.
- 키는 코드/리포에 절대 저장하지 않음 — Supabase Secrets에만.
