
## toprank.py — 상위 글 내용 분석기 (2026-09-20)
`python work/toprank.py "검색어" [내초안.txt] [상위N=8]`
네이버 블로그 탭 상위 글 본문을 읽어 (1) 글마다 길이·사진 수·소제목 후보 (2) 상위 글 과반이 쓰는데 내 초안에 없는 말 (3) 상위 글에 2번 이상 나오는데 내 초안에 없는 숫자를 뽑는다. HTTP만 쓰므로 스크린샷 비용 없음. 결과는 work/toprank_last.json.
한국어 형태소 분석은 kiwipiepy(pip install kiwipiepy). 없으면 import 에러가 난다.
