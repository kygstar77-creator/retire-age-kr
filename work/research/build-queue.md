# 도구 만들기 대기열 — 자가발전 루틴 C(17:30)가 위에서부터 하나씩 만든다. 만들면 "완료 날짜·파일"을 적는다.

1. `work/listings.py` — 해외 매물 읽기: FazWaz(치앙마이·방콕·다낭 등)·Idealista(리스본·포르투·발렌시아)·Numbeo. 입력 도시 → 매물 8건(동네·단지·월세·면적·방·시설·층·가구·설명·URL·게시일) JSON. 2026-09-23 프로필 없는 Playwright로 읽기 확인. DDproperty·PropertyGuru는 차단(대체: Hipflat·iProperty 시험).
2. `work/rtmolit.py` — 국토부 실거래: **공공데이터 키 확보됨(Documents\datago_key.txt, 2026-09-23)**. 엔드포인트 apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev(매매 상세)·RTMSDataSvcAptRent(전월세)·RTMSDataSvcAptTrade, 파라미터 serviceKey·LAWD_CD(시군구 5자리)·DEAL_YMD(YYYYMM)·numOfRows·pageNo. 마포구 202608 매매 112건·전월세 774건 확인. 서울 25개 구 + 수도권 주요 시군구 최근 3개월을 Supabase 또는 work/research/rt/<구>_<월>.json에 저장하는 수집기. 단지·계약별 매매·전세·월세·오피스텔.
3. `work/undervalue.py` — B10 지표 6개 계산(전세가율·고점대비·평당가 편차·월세 수익률·오피스텔 수익률·공시가격 대비). 공시가격은 realtyprice.kr(읽기 확인).
4. `work/ytlearn.py --channels` 부동산 상위 채널 매일: 투미TV UC9meL6XNNckzlleWelmO9tQ · 부동산쿨TV UClWhdsAcFX-t5OsBC7yWuSA · 하이클래스 UCMsuAb9v3Q1AB89bB5EFK7A · KB부동산TV UCHmXGmj6JA-4iQ1UFMC7LYw · 리치고TV UC3nsb3SxlRrJQ9egkKNnlfg · 저평가 아파트 발굴단 UCaXYdIFec07keCSvEQ87-Bg · 아파트써처 UCEoF-IS2vWlL1MGIMBry5Lw · 시크릿브라더 UCGzEAhEIZuQA7EibT-W-lCg · 김경민의 노트 UCU09s-DZfqlZsbIm49WbOZw · 오피스텔TV UCjtt1zQiVYuVgtSPyLj9wwA · 월세냄비 UCJ6pu5zitBOSNALEnGOSbCw. 이들의 자막·장면으로 "사람들이 궁금해하는 저평가 판단 기준"을 뽑아 B10 지표에 반영.
5. `work/ytlearn.py` RSS 404/500 채널 처리(채널 ID 추출 오류 수정).
6. `work/planner.py` 신호 추가: 부동산원 주간 통계, 히트맵 상위 등락 종목, 카페 벤치마크 제목.
7. `work/sonpum.py` — **자동 손품 영상**(사장님 아이디어 2026-09-23): Playwright가 네이버 부동산(new.land.naver.com)을 실제로 돌아다니며 녹화(record_video_dir 확인됨) — 동네 지도 → 단지 → 매매/전세/월세 호가 → 평형·준공·세대수 → 역 거리·학교·주변 → 각 장면마다 edge-tts(무료 한국어 신경망 음성, 확인됨)로 해설 → 영상+음성 합치기(imageio-ffmpeg, pip 무료) → mp4. 첫 프로토타입: 마포구 공덕동 아파트 5분. 경사는 국토지리정보원 표고 또는 open-elevation으로 계산. 유튜브 업로드는 사장님 OAuth 1회 필요. 네이버 부동산은 API 429가 나므로 사람 속도(장면당 3~5초)로만.
8. `work/heatmap_re.py` — **부동산 히트맵**: 서울 25개 구·수도권 시군구를 면적=거래량, 색=전세가율 또는 주간 변동률로 그리기(heatmap.py 재사용). 매일 "부동산 한 장"에 들어간다.
