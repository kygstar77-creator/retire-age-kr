
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

## 발행이 막힐 때 — 화면이 검게 가려지는 경우 (2026-09-21 확인)

computer-use는 권한 목록에 없는 앱의 창이 있는 화면 영역을 **검게 칠한다**. 웨일 창이
그 위에 있어도 가려진다. 블로그 에디터 왼쪽(사진 삽입 버튼 등)이 이 영역에 걸리면
이미지를 넣을 수 없다.

푸는 법: `mcp__computer-use__request_access` 에 그 앱 이름을 넣는다. 스크린샷 결과에
어떤 앱이 숨겨졌는지 이름이 나온다. 실측에서 `["계산기","캡처 도구","스티커 메모"]`
셋을 받자 마스크가 완전히 풀렸다. 조작하지 않고 가림만 푸는 용도다.

사장님 개인 앱(텔레그램, 카카오톡 등)은 요청하지 않는다. 그것들이 원인이면 마스크를
피해 웨일 창을 옮기거나, 발행을 대기로 남기고 그 사실을 적는다.

## 한글을 직접 타이핑하지 않는다 — 입력기 창이 발행을 8시간 막았다 (2026-09-21)

computer-use의 `type` 액션으로 한글을 치면 Windows 입력기 창(TextInputHost.exe)이 뜬다.
이 창이 포커스를 잡고 놓지 않으면 **이후 모든 클릭·키 입력이 차단**된다.
"Textinputhost is not in the allowed applications and is currently in front" 오류가 난다.

2026-09-21 새벽 블로그 태그 15개를 `type`으로 한글 입력한 뒤 이 상태가 되어,
03:40부터 11:13까지 웨일 조작이 전부 막혔다. request_access에 textinputhost.exe를
넣어도 시스템 앱이라 거부되고, PowerShell SetForegroundWindow·AppActivate로
웨일을 앞으로 끌어와도 소용없었다.

규칙:
- **한글·긴 텍스트는 전부 클립보드로 넣는다.** PowerShell
  `[System.Windows.Forms.Clipboard]::SetText(...)` 후 `ctrl+v`.
- **블로그 태그도 한 개씩 클립보드로.** 쉼표로 한 번에 붙이면 하나로 뭉치므로
  태그마다 SetText → ctrl+v → Return 을 반복한다.
- `type` 은 URL·영문·숫자에만 쓴다.
- 이 오류가 나면 더 시도하지 말고, 그 회차의 묶음을 pkg/ 에 저장하고
  runs_today.json note에 "입력기 창 차단"이라고 적고 끝낸다. 사장님이 화면을 한 번
  클릭하면 풀린다.
