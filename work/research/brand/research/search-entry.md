# 유입 검색어: 상품·제도 이름 vs 계산 꼴 (2026-10-05 02:4x, brand-researcher)

결론: **상위 30 검색어 비율은 확인 안 함.** 검색어가 우리 쪽에 한 글자도 안 들어온다.

## 막힌 이유 (실측)
- 서치어드바이저(네이버): 읽는 공식 API·스크립트 없음. work/ 아래 연결 코드 없음(grep). 웹 화면 로그인이 필요해 무인 불가.
- GA4: 읽는 스크립트 없음(revenue_model.py 주석도 "사람이 화면에서 읽는다"). 키·토큰 없음.
- 사이트 이벤트 firemap_events(Supabase c7cd8a90): session_start props에 host·path·ref·utm만 있고 검색어 칸 없음. 구글·네이버는 검색어를 ref에 안 넘긴다.

## 대신 잰 것 (firemap_events session_start, 최근 30일, bot·internal 제외)
- 총 5,289 세션 중 (direct) 5,263 = 99.5%.
- 검색 계열 ref: m.search.naver.com 4, naver.com 1 (+ 카페·블로그 등 네이버 4) , 구글 0. 검색 유입으로 볼 수 있는 건 10건 안팎(0.2%).
- 그 외 ref: youtube 8, viva.republica.toss 5, dcinside 3, facebook 1.
- 검색 계열 랜딩 path: / 8, /calc/unemployment-benefit 1. 표본 9로는 이름 vs 계산 꼴 비율을 말할 수 없다.

## 해석
- persona 2회차의 "이름 있는 계산이 유입을 만든다"는 이번에도 **검증 안 됨**(반증도 아님).
- 다만 (direct) 99.5%는 ref 수집이 새는 것일 수 있다. 확인 안 함: 앱 내 브라우저·ref 정책 차단 여부.

## 풀려면 (사람 필요)
- 서치어드바이저 '검색 키워드' 화면과 GA4 획득 화면을 사람이 CSV로 내려 work/data/ 에 두면 즉시 30개 분류 가능.
- 또는 서치콘솔 API 서비스계정(OAuth 허용) — 승인 필요, today.md 막힘에 적음.
