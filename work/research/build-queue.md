# 도구 만들기 대기열 — 자가발전 루틴 C(17:30)가 위에서부터 하나씩 만든다. 만들면 "완료 날짜·파일"을 적는다.

1. **완료 2026-09-23 17:47** `work/listings.py` — 해외 매물+생활비 읽기. `py -3.12 work/listings.py <도시> [건수]` → work/research/listings/<도시>_<날짜>.json(확인일·URL 포함).
   실행 확인(2026-09-23): 매물 6도시 — 치앙마이·방콕·푸켓·파타야(fazwaz.com, `div.result-search__item`), 리스본·포르투(idealista.pt, `article.item`). 필드: 단지·제목·동네·월세·㎡당·면적·방·욕실·유형·준공·시설·게시일·설명·URL.
   생활비는 Numbeo `?displayCurrency=KRW`로 **원화 직접**(원룸/방3 월세 도심·도심밖, 식사·교통·공과금·통신·인터넷·헬스 10항목 + 서울 대비 % 요약) — 22개 도시 전부 됨.
   막힘(실측): fazwaz.com/…/indonesia/bali 404 · fazwaz.id Cloudflare 403 · idealista.com(스페인) 403 → 발리·바르셀로나·발렌시아·마드리드는 생활비만. 파타야 경로는 `chonburi`가 아니라 `chon-buri`. DDproperty·PropertyGuru는 이전 회차에 차단 확인(대체 미시험).
2. **완료 2026-09-23 16:50** `work/rtmolit.py` — 국토부 실거래(서울 25구 2026-07~09 매매·전월세 150회 호출 100초): **공공데이터 키 확보됨(Documents\datago_key.txt, 2026-09-23)**. 엔드포인트 apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev(매매 상세)·RTMSDataSvcAptRent(전월세)·RTMSDataSvcAptTrade, 파라미터 serviceKey·LAWD_CD(시군구 5자리)·DEAL_YMD(YYYYMM)·numOfRows·pageNo. 마포구 202608 매매 112건·전월세 774건 확인. 서울 25개 구 + 수도권 주요 시군구 최근 3개월을 Supabase 또는 work/research/rt/<구>_<월>.json에 저장하는 수집기. 단지·계약별 매매·전세·월세·오피스텔.
3. **1차 완료 2026-09-23 16:55(전세가율·월세수익률)** `work/undervalue.py` — B10 지표 6개 계산(남은 것: 고점 대비·평당가 편차·오피스텔·공시가격)(전세가율·고점대비·평당가 편차·월세 수익률·오피스텔 수익률·공시가격 대비). 공시가격은 realtyprice.kr(읽기 확인).
4. `work/ytlearn.py --channels` 부동산 상위 채널 매일: 투미TV UC9meL6XNNckzlleWelmO9tQ · 부동산쿨TV UClWhdsAcFX-t5OsBC7yWuSA · 하이클래스 UCMsuAb9v3Q1AB89bB5EFK7A · KB부동산TV UCHmXGmj6JA-4iQ1UFMC7LYw · 리치고TV UC3nsb3SxlRrJQ9egkKNnlfg · 저평가 아파트 발굴단 UCaXYdIFec07keCSvEQ87-Bg · 아파트써처 UCEoF-IS2vWlL1MGIMBry5Lw · 시크릿브라더 UCGzEAhEIZuQA7EibT-W-lCg · 김경민의 노트 UCU09s-DZfqlZsbIm49WbOZw · 오피스텔TV UCjtt1zQiVYuVgtSPyLj9wwA · 월세냄비 UCJ6pu5zitBOSNALEnGOSbCw. 이들의 자막·장면으로 "사람들이 궁금해하는 저평가 판단 기준"을 뽑아 B10 지표에 반영.
5. `work/ytlearn.py` RSS 404/500 채널 처리(채널 ID 추출 오류 수정).
6. `work/planner.py` 신호 추가: 부동산원 주간 통계, 히트맵 상위 등락 종목, 카페 벤치마크 제목.
7. `work/sonpum.py` — **자동 손품 영상**(사장님 아이디어 2026-09-23): Playwright가 네이버 부동산(new.land.naver.com)을 실제로 돌아다니며 녹화(record_video_dir 확인됨) — 동네 지도 → 단지 → 매매/전세/월세 호가 → 평형·준공·세대수 → 역 거리·학교·주변 → 각 장면마다 edge-tts(무료 한국어 신경망 음성, 확인됨)로 해설 → 영상+음성 합치기(imageio-ffmpeg, pip 무료) → mp4. 첫 프로토타입: 마포구 공덕동 아파트 5분. 경사는 국토지리정보원 표고 또는 open-elevation으로 계산. 유튜브 업로드는 사장님 OAuth 1회 필요. 네이버 부동산은 API 429가 나므로 사람 속도(장면당 3~5초)로만.
8. `work/heatmap_re.py` — **부동산 히트맵**: 서울 25개 구·수도권 시군구를 면적=거래량, 색=전세가율 또는 주간 변동률로 그리기(heatmap.py 재사용). 매일 "부동산 한 장"에 들어간다.
10. **Canva 썸네일**: 손품 영상·브리핑 영상 썸네일과 블로그 대표 이미지를 Canva 커넥터(generate-design → export-design PNG)로 만들고, 실패하면 blogimg.py(PIL)로 폴백. 첫 시도: 공덕동 손품 영상 썸네일 1장(제목 한 줄·숫자 두 개 원칙).
