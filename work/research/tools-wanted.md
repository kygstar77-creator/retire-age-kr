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
- (2026-09-23 20:26 감시 회차) **Gemini 무료 등급이 하루 할당량을 다 썼다(HTTP 429 quota exceeded).** 503(일시 과부하)이 아니라 오늘치를 소진한 것이다. 이번 회차에 만든 묶음 6개 중 xyldcc 하나만 말투 검증을 받았고 나머지 다섯(nobl25·tenbil·jeonseratio·levetf·offiyield)은 check_*.txt가 없다. 발행 회차가 올리기 전에 다시 돌려야 한다. 하루 24편 × 2매체를 한 무료 키로 검증하는 구조가 한계다 — OpenAI 키를 받거나 유료 전환이 필요하다(사장님 판단).
- (2026-09-23 19시) **Gemini 무료 등급이 503으로 막힌다** — 묶음 1개 검증에 10분 넘게 걸려 밀린 54개를 못 따라잡는다. 키 하나로는 하루 24편 검증이 안 된다. 무료 대안을 E 회차에 찾거나, 유료 전환은 사장님 판단.

- [2026-09-23 19시] 금융감독원 금융상품통합비교공시 API 인증키가 "미등록 인증키(err_cd 010)"로 거부됨. 파일은 Documents\finlife_key.txt에 있다. 이 API가 살아야 은행별 정기예금·주담대 금리를 1차 출처로 쓸 수 있다(지금은 매체 보도로만 적고 있다). 사람이 봐야 함 — finlife.fss.or.kr에서 키 재발급·승인 확인 필요.

## 사람이 봐야 함 — 2026-09-23 20:15 · **dev 푸시가 막혔다(비밀키가 커밋에 들어감)**

**증상**: `git push origin dev`가 GitHub 푸시 보호(GH013)에 막힌다. dev·main 둘 다 안 올라간다.
지금 로컬에만 쌓인 커밋 4개(4af3a68·3cc8448·717f120·dd2ea29)가 통째로 못 나간다.

**원인**: 커밋 `3cc8448`이 `work/research/_boss_msgs.txt`(423줄)와
`work/research/_boss_recent.txt`(51줄)를 같이 커밋했는데, 그 줄에
**사장님이 2026-09-23 07:10 대화창에 붙여 넣은 GCP API 키(`AQ.`로 시작)** 가 그대로 들어 있다.
지시문을 받아 적는 기록 파일이 대화 내용을 글자 그대로 저장한 탓이다.

**중요**: `.gitignore` 7줄에 `work/research/_boss_*.txt`가 **이미 있다.** 그런데도 들어간 것은
그 회차가 경로를 직접 적어 `git add` 했기 때문이다(명시 경로는 .gitignore를 무시한다).

**다행인 점**: 푸시가 막혔으므로 **키는 GitHub에 올라가지 않았다.** 이 컴퓨터 안에만 있다.

**내가 못 한 것과 이유**: 고치려면 로컬 커밋 히스토리를 다시 써야 하는데(`git filter-branch`로
그 두 파일만 빼기), 히스토리 재작성은 되돌리기 어려운 작업이라 권한에서 막혔다.
게다가 작업 중에 다른 세션이 커밋(dd2ea29)을 올리고 있어서, 지금 히스토리를 갈아엎으면
그쪽 작업을 덮어쓸 수 있다. 그래서 **일부러 강행하지 않았다.**

**사람이 해 줄 것 — 순서대로**
1. **키부터 바꾼다.** 그 GCP/Gemini 키를 콘솔에서 폐기하고 새로 발급한다.
   대화창에 붙여 넣은 순간 기록 파일·로그 여러 곳에 복사됐다고 보는 게 안전하다.
   새 키는 대화창에 붙여 넣지 말고 키 파일에 직접 넣는다.
2. 히스토리에서 그 두 파일을 뺀다(아래 한 줄). 다른 세션 작업이 끝난 걸 확인하고 한다.
   `FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --index-filter "git rm --cached --ignore-unmatch work/research/_boss_msgs.txt work/research/_boss_recent.txt" -- origin/dev..HEAD`
3. 그 다음 `git push origin dev`.

**하지 말 것**: GitHub가 알려 주는 "unblock-secret" 링크로 통과시키기.
그건 키를 그대로 공개 저장소에 올리는 것이다.

**재발 방지(다음 회차가 할 일)**: 기록 파일에 키 형태 문자열(`AQ.`·`AIza`·`sk-`)이 들어오면
저장할 때 가려서 쓰도록 고친다. 그리고 회차 루틴은 `git add`에 `_boss_*` 경로를 절대 적지 않는다.

## Gemini 무료 할당량이 하루 24편 속도를 못 따라간다 (2026-09-23 20시 회차)
`crosscheck.py`가 HTTP 429(You exceeded your current quota)로 사실 대조·말투 검증을 둘 다 못 했다.
전부 무료 원칙이라 사실 대조까지 Gemini 하나가 맡고 있는데, 하루 48편(블로그 24·카페 24)에 묶음당 2회를 부르면 무료 한도를 넘는다.
**사람이 해 줄 것**: OpenAI 키를 `Documents\openai_key.txt`에 넣어 주면 사실 대조를 그쪽으로 돌려 Gemini 호출이 절반으로 준다.
(그 전까지는 할당량이 도는 시각에만 검증이 되고, 안 되는 회차는 runs note에 "교차검증 미실행(429)"으로 남는다.)
| 대기 | 브이월드 **데이터 API(GetFeature)** 권한 — 지금 키는 주소·검색만 되고 데이터 API는 INCORRECT_KEY (2026-09-23 확인) | 손품 영상에 사장님이 말한 "경사"를 넣으려면 수치표고(DEM)가 필요하다. vworld.kr에서 같은 키에 데이터 API 활용신청을 추가하면 된다 |
| 대기 | 네이버 클립·인스타 릴스·틱톡 **업로드** | 숏폼 mp4는 자동으로 만들어지지만 유튜브만 API 업로드가 된다. 나머지 셋은 공개 업로드 API가 없거나 사업자 심사가 필요해 지금은 사람이 올려야 한다. 파일은 work/research/shorts/ 에 쌓인다 |
