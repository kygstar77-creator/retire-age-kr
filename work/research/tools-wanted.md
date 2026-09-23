# 사장님 손이 필요한 것 (무료만)

| 무엇 | 왜 | 절차 | 상태 |
|---|---|---|---|
| Gemini API 키 | 교차검증(사실 대조·말투) | aistudio.google.com → API 키 만들기 → 키를 채팅에 붙이면 Documents\gemini_key.txt에 저장 | **완료 2026-09-23 16:14** — gemini_key.txt, 무료 등급. Pro는 한도 없음(429) → Flash 3.5~3.8로 자동 전환 |
| DART 오픈API 키 | 국내 종목·국내상장 ETF 공시·실적 | opendart.fss.or.kr | **완료 2026-09-23 16:20** — dart_key.txt(공시목록·배당정보·회사코드 확인) |
| FRED API 키 | 미국 금리·물가 시계열 | fred.stlouisfed.org My Account → API Keys(무료) | 대기 |
| Alpha Vantage 키 | PER·배당률·실적(야후가 막음) | alphavantage.co 무료 키 | 대기 |
| MCP 커넥터(Alpha Vantage·FMP) | 위와 같음, PC 앱에서만 연결 가능 | PC에서 이 대화의 커넥터 카드 | 대기 |
| 공공데이터포털 키(국토부 실거래가 API) | 부동산 시리즈(B4·B8·B10) 아파트 실거래 원자료 | data.go.kr | **완료 2026-09-23 16:16** — datago_key.txt, 아파트 매매·매매상세·전월세 승인(마포구 8월 매매 112건·전월세 774건 확인). 오피스텔 매매·전월세는 아직 미신청 |
| (막힘 기록 2026-09-23 15시) Nasdaq dividends API | O·SCHD·VOO·SPY·QLD 모두 'N/A'만 돌려줌(JEPQ만 정상). assetclass를 stocks/etf 둘 다 시도해도 같음 | 사장님 손 필요 없음 — Yahoo chart `?events=div`로 대체 확인(7종목 전부 정상). 17시 도구 회차에서 stockwants/crosscheck가 Nasdaq 배당을 쓰면 Yahoo로 바꿀 것 | 대체됨 |
| 은행연합회 달러예금 금리 공시 | 카페 '달러예금 vs 미국 단기채 ETF' 비교에 국내 예금 금리가 필요 | 무료 공개 페이지 — 읽는 스크립트가 없음(확인 안 함). 17시 회차에서 nvread/Playwright로 읽어볼 것 | 대기 |
- EDGAR 전문검색(efts.sec.gov) 기간 조회 붙이기 — getcurrent 피드가 20건만 줘서 내부자 매수(Form 4 코드 P)가 회당 1건밖에 안 잡힌다. 키는 필요 없고 스크립트 작업만 남았다(2026-09-23 16시 회차, work/insider.py).
| 한국은행 ECOS 키 | 기준금리·환율·물가 시계열 | ecos.bok.or.kr | **완료 2026-09-23 16:37** — ecos_key.txt(기준금리 2.5→2.75→3.0, 원달러 일별 확인) |
| 카카오 REST 키 | 주변 시설 거리 | developers.kakao.com | 키 저장(kakao_key.txt)했으나 **카카오맵 활성화 안 함**(계정당 1개 앱만 무료 쿼터 — 아껴 둠). 거리는 OpenStreetMap(무료·키 없음)으로 대체 확인 |
| 네이버 검색·데이터랩 API | 뉴스 검색·검색 추세 | — | **불필요** — 2026-07-31부터 개발자센터 신규 신청 종료(NAVER API HUB로 이관, 추후 유료). 구글 뉴스 RSS(무료·키 없음)로 대체 확인 |
| VWorld 키 | 지오코더·배경지도·2D 데이터(행정구역 등) | vworld.kr | **완료 2026-09-23 16:40** — vworld_key.txt(개발키, 2027-03-23 만료, 지오코더·타일·시군구 조회 확인) |
| YouTube 업로드 OAuth | 손품·브리핑 영상 자동 업로드, 채널 통계 | console.cloud.google.com | **완료 2026-09-23 17:05** — youtube_client.json + youtube_token.json(오프라인 토큰, 자동 갱신). ytupload.py upload/stats |
| FMP 키 | 미국 종목 프로필(시가총액·최근 배당·52주 범위·업종·CEO)·실적 캘린더 | financialmodelingprep.com | **완료 2026-09-23 17:16** — fmp_key.txt. 무료 등급은 profile·earnings-calendar만 됨; quote·배당 이력·ETF 구성은 402(유료) → 그건 Nasdaq API·운용사 페이지로 |
| Alpha Vantage 키 | PER·배당률·배당 이력·분기 실적(EPS 서프라이즈) | alphavantage.co | **완료 2026-09-23 17:18** — alphavantage_key.txt(하루 25회 무료) |
| 공공데이터 오피스텔 전월세 | 오피스텔 월세 수익률 | data.go.kr | **완료 2026-09-23 17:16**(마포구 8월 453건). 오피스텔 매매는 활용신청 대기 |
