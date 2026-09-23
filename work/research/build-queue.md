# 도구 만들기 대기열 — 자가발전 루틴 C(17:30)가 위에서부터 하나씩 만든다. 만들면 "완료 날짜·파일"을 적는다.

1. `work/listings.py` — 해외 매물 읽기: FazWaz(치앙마이·방콕·다낭 등)·Idealista(리스본·포르투·발렌시아)·Numbeo. 입력 도시 → 매물 8건(동네·단지·월세·면적·방·시설·층·가구·설명·URL·게시일) JSON. 2026-09-23 프로필 없는 Playwright로 읽기 확인. DDproperty·PropertyGuru는 차단(대체: Hipflat·iProperty 시험).
2. `work/rtmolit.py` — 국토부 실거래 내려받기: rt.molit.go.kr/pt/xls/xls.do 조건별 다운로드(폼 POST 분석) 또는 공공데이터포털 키(Documents\datago_key.txt)가 생기면 API. 단지·계약별 매매·전세·월세·오피스텔.
3. `work/undervalue.py` — B10 지표 6개 계산(전세가율·고점대비·평당가 편차·월세 수익률·오피스텔 수익률·공시가격 대비). 공시가격은 realtyprice.kr(읽기 확인).
4. `work/ytlearn.py --channels` 부동산 상위 채널 매일: 투미TV UC9meL6XNNckzlleWelmO9tQ · 부동산쿨TV UClWhdsAcFX-t5OsBC7yWuSA · 하이클래스 UCMsuAb9v3Q1AB89bB5EFK7A · KB부동산TV UCHmXGmj6JA-4iQ1UFMC7LYw · 리치고TV UC3nsb3SxlRrJQ9egkKNnlfg · 저평가 아파트 발굴단 UCaXYdIFec07keCSvEQ87-Bg · 아파트써처 UCEoF-IS2vWlL1MGIMBry5Lw · 시크릿브라더 UCGzEAhEIZuQA7EibT-W-lCg · 김경민의 노트 UCU09s-DZfqlZsbIm49WbOZw · 오피스텔TV UCjtt1zQiVYuVgtSPyLj9wwA · 월세냄비 UCJ6pu5zitBOSNALEnGOSbCw. 이들의 자막·장면으로 "사람들이 궁금해하는 저평가 판단 기준"을 뽑아 B10 지표에 반영.
5. `work/ytlearn.py` RSS 404/500 채널 처리(채널 ID 추출 오류 수정).
6. `work/planner.py` 신호 추가: 부동산원 주간 통계, 히트맵 상위 등락 종목, 카페 벤치마크 제목.
