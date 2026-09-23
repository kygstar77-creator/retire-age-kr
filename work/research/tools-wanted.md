# 사장님 손이 필요한 것 (무료만)

| 무엇 | 왜 | 절차 | 상태 |
|---|---|---|---|
| Gemini API 키 | 교차검증(사실 대조·말투) | aistudio.google.com → API 키 만들기 → 키를 채팅에 붙이면 Documents\gemini_key.txt에 저장 | 사장님이 "이미 줬다"고 함 — 이 프로젝트 파일에는 없음. 다시 붙여 주세요 |
| DART 오픈API 키 | 국내 종목·국내상장 ETF 공시·실적 | opendart.fss.or.kr 가입 → 인증키 신청(무료) | 대기 |
| FRED API 키 | 미국 금리·물가 시계열 | fred.stlouisfed.org My Account → API Keys(무료) | 대기 |
| Alpha Vantage 키 | PER·배당률·실적(야후가 막음) | alphavantage.co 무료 키 | 대기 |
| MCP 커넥터(Alpha Vantage·FMP) | 위와 같음, PC 앱에서만 연결 가능 | PC에서 이 대화의 커넥터 카드 | 대기 |
| 공공데이터포털 키(국토부 실거래가 API) | 부동산 시리즈(B4·B8) 아파트 실거래 원자료 | data.go.kr 가입 → 활용신청(무료, 자동승인) | 대기 |
| (막힘 기록 2026-09-23 15시) Nasdaq dividends API | O·SCHD·VOO·SPY·QLD 모두 'N/A'만 돌려줌(JEPQ만 정상). assetclass를 stocks/etf 둘 다 시도해도 같음 | 사장님 손 필요 없음 — Yahoo chart `?events=div`로 대체 확인(7종목 전부 정상). 17시 도구 회차에서 stockwants/crosscheck가 Nasdaq 배당을 쓰면 Yahoo로 바꿀 것 | 대체됨 |
| 은행연합회 달러예금 금리 공시 | 카페 '달러예금 vs 미국 단기채 ETF' 비교에 국내 예금 금리가 필요 | 무료 공개 페이지 — 읽는 스크립트가 없음(확인 안 함). 17시 회차에서 nvread/Playwright로 읽어볼 것 | 대기 |
