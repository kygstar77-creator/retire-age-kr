
## toprank.py — 상위 글 내용 분석기 (2026-09-20)
`python work/toprank.py "검색어" [내초안.txt] [상위N=8]`
네이버 블로그 탭 상위 글 본문을 읽어 (1) 글마다 길이·사진 수·소제목 후보 (2) 상위 글 과반이 쓰는데 내 초안에 없는 말 (3) 상위 글에 2번 이상 나오는데 내 초안에 없는 숫자를 뽑는다. HTTP만 쓰므로 스크린샷 비용 없음. 결과는 work/toprank_last.json.
한국어 형태소 분석은 kiwipiepy(pip install kiwipiepy). 없으면 import 에러가 난다.

## pick.py + calendar.json — 이번에 쓸 글 고르기 (2026-09-21)
`python work/pick.py [며칠치=45]`
조회수는 검색수가 아니라 **마감일**이 만든다. 그래서 일정표(calendar.json)를 1순위로 두고 점수를 낸다.
점수 = 검색수 × 시의성 × (1−경쟁) × 중복감점. 시의성은 일정의 lead일 안에 들어왔거나 진행 중이면 만점.
블로그·카페를 따로 보고 "쓸 곳"을 표시한다(카페는 cafePosts.js, 블로그는 RSS로 판정).
calendar.json의 `src`가 `미확인`인 날짜는 글쓰기 전에 원문으로 확인할 것. 검색수 100 미만은 검색광고 API가 값을 가린 것이라 순위를 믿지 말 것(기준금리·국민연금 계열이 그렇다).
새 일정이 생기면 calendar.json에 추가한다.
