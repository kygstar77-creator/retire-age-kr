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
- **해결 2026-09-23 17:50(17시 회차)** EDGAR 20건 제한 — 전문검색 대신 **일별 인덱스**(`Archives/edgar/daily-index/<연>/QTR<분기>/form.<YYYYMMDD>.idx`)로 바꿨다. 그날 접수분 전체를 준다(2026-09-22 Form 4 847건 확인). insider.py 실행 확인: 109건 조회 → 매수(P) 17건(예전 1건). `py -3.12 work/insider.py 20 --days 2 --max 400 --min-amt 100000`. 키 필요 없음. 같은 접수번호가 발행사·신고자 CIK 경로로 두 번 나와 접수번호로 중복을 지운다. 당일 인덱스는 장 마감 뒤에 올라온다(오늘 것은 404).
| 한국은행 ECOS 키 | 기준금리·환율·물가 시계열 | ecos.bok.or.kr | **완료 2026-09-23 16:37** — ecos_key.txt(기준금리 2.5→2.75→3.0, 원달러 일별 확인) |
| 카카오 REST 키 | 주변 시설 거리 | developers.kakao.com | 키 저장(kakao_key.txt)했으나 **카카오맵 활성화 안 함**(계정당 1개 앱만 무료 쿼터 — 아껴 둠). 거리는 OpenStreetMap(무료·키 없음)으로 대체 확인 |
| 네이버 검색·데이터랩 API | 뉴스 검색·검색 추세 | — | **불필요** — 2026-07-31부터 개발자센터 신규 신청 종료(NAVER API HUB로 이관, 추후 유료). 구글 뉴스 RSS(무료·키 없음)로 대체 확인 |
| VWorld 키 | 지오코더·배경지도·2D 데이터(행정구역 등) | vworld.kr | **완료 2026-09-23 16:40** — vworld_key.txt(개발키, 2027-03-23 만료, 지오코더·타일·시군구 조회 확인) |
| YouTube 업로드 OAuth | 손품·브리핑 영상 자동 업로드, 채널 통계 | console.cloud.google.com | **완료 2026-09-23 17:05** — youtube_client.json + youtube_token.json(오프라인 토큰, 자동 갱신). ytupload.py upload/stats |
| FMP 키 | 미국 종목 프로필(시가총액·최근 배당·52주 범위·업종·CEO)·실적 캘린더 | financialmodelingprep.com | **완료 2026-09-23 17:16** — fmp_key.txt. 무료 등급은 profile·earnings-calendar만 됨; quote·배당 이력·ETF 구성은 402(유료) → 그건 Nasdaq API·운용사 페이지로 |
| Alpha Vantage 키 | PER·배당률·배당 이력·분기 실적(EPS 서프라이즈) | alphavantage.co | **완료 2026-09-23 17:18** — alphavantage_key.txt(하루 25회 무료) |
| 공공데이터 오피스텔 전월세 | 오피스텔 월세 수익률 | data.go.kr | **완료 2026-09-23 17:16**(마포구 8월 453건). 오피스텔 매매도 완료 2026-09-23 17:19 |
| Canva 커넥터 | 썸네일·숏폼·카드 이미지 자동 생성(generate-design·export-design) | 클로드 앱 커넥터 | **완료 2026-09-23 17:24** — 세션에서 API 응답 확인(브랜드 키트 0개). 루틴(새 세션)에서 바로 사용 가능 |
| 금융상품 한눈에 키 | 예금·적금 실제 금리(은행권 39상품) | finlife.fss.or.kr | **완료 2026-09-23 17:27** — finlife_key.txt |
| FRED 키 | 연방기금금리·CPI·10년물·실업률 시계열 | fred.stlouisfed.org | **완료 2026-09-23 17:30** — fred_key.txt |
| (막힘 기록 2026-09-23 17시) 발리·스페인 매물 | 해외 도시 글의 '지금 나와 있는 월세' | 사장님 손 필요 없음 — fazwaz.com/…/indonesia/bali 404, fazwaz.id Cloudflare 403, idealista.com(스페인) 403. 같은 스크립트로 태국(fazwaz.com)·포르투갈(idealista.pt)은 정상. 다음 도구 회차에서 대체 사이트(Rumah123·Fotocasa) 시험할 것 | 대기 |

- (2026-09-23 19시) **OpenAI 키가 없다** — C:\Users\강영준\Documents\openai_key.txt 없음. 그래서 사실 대조를 Gemini 한 곳이 혼자 하고 있다(자기 계열 모델이 자기 글을 보는 셈이라 교차검증이 아니다). 무료 아님(종량). 절차: platform.openai.com → API keys → 발급 → 위 경로에 KEY=sk-... 한 줄.
- (2026-09-23 19시) **Gemini 무료 등급이 503으로 막힌다** — 묶음 1개 검증에 10분 넘게 걸려 밀린 54개를 못 따라잡는다. 키 하나로는 하루 24편 검증이 안 된다. 무료 대안을 E 회차에 찾거나, 유료 전환은 사장님 판단.
