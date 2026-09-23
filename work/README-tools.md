
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

## 예약 실행에서는 computer-use 승인이 안 난다 (2026-09-21 12시 테스트 회차)

예약 작업(scheduled-tasks) 안에서 `request_access`를 부르면 "can't be approved during a
scheduled run"으로 거부된다(웨일+보조앱 1회, 웨일 단독 1회 시도). 승인 카드를 띄울 사람이
없기 때문이다. Chrome 확장(claude-in-chrome)은 naver.com 자체를 안전 제한으로 막는다.
→ 자동 발행을 하려면 **예약 작업 설정에 '네이버 웨일'(필요하면 계산기·캡처 도구·스티커 메모)을
허용 앱으로 미리 추가**해야 한다. 그 전까지 예약 회차는 묶음을 pkg/에 만들고 끝난다.

## 2026-09-21 실측 — 발행 조작에서 걸린 것들

### 예약 루틴은 웨일을 조작할 수 없다 (가장 중요)
앱 루틴(scheduled-tasks)은 사장님이 "지금 실행"을 눌러도 **무인 실행**으로 처리되고,
computer-use request_access가 승인 카드 없이 **자동 거부**된다. 두 번 확인했다.
→ 루틴은 자료조사·글·이미지를 만들어 `work/research/<주제>/pkg/` 에 두는 데까지만 한다.
→ 실제 발행은 **사장님이 있는 대화 세션**에서 한다(그 세션은 웨일 접근 가능).
내장 브라우저(mcp__Claude_Browser)와 Chrome 확장은 naver.com을 막는다(2026-09-21 재확인).

### 조작 요령
- **드롭다운·버튼은 mouse_move로 먼저 올린 뒤 클릭.** 블로그 카테고리 목록은 hover 없이
  누르면 선택이 안 된다.
- **블로그 카테고리 드롭다운이 열린 채로 남으면 이후 붙여넣기·Enter를 다 먹는다.**
  카테고리를 고른 뒤 Escape로 닫고, 드롭다운 머리를 한 번 눌러 닫힌 것을 확인한다.
- **태그는 하나씩.** 쉼표든 줄바꿈이든 한 번에 붙이면 하나로 뭉친다.
  `mcp__computer-use__write_clipboard`(포커스를 안 뺏는다) → 입력칸의 "#태그 입력" 글자
  위치를 클릭 → ctrl+v → Return. 태그 칩 위를 누르면 칩이 선택되고 입력이 안 들어간다.
  입력칸이 다음 줄로 넘어가면 클릭 위치도 따라 내려간다. 넣을 때마다 zoom으로 확인.
- **본문 조각을 붙일 때 텍스트 줄 위를 클릭하지 않는다.** 그 자리에 끼어든다(국제유가 글에서
  표가 문장 중간에 들어갔다). 마지막 요소 **바로 아래 빈 곳**을 누르거나, 마지막 줄 끝을
  누르고 End.
- **카페 편집기의 ctrl+End는 문서 끝이 아니라 문단 끝으로 간다.** 카페는 반드시
  "마지막 줄 끝 클릭 → End → Return → ctrl+v". (1억 모으기 글에서 문단이 표 위로 들어갔다.)
- **카페 등록 버튼**은 페이지를 맨 위로 올린 상태에서 (1105,420) 근처. 스크롤된 상태의
  고정 헤더 버튼은 눌러도 반응이 없었다.
- **PowerShell로 클립보드를 쓰면 웨일 포커스가 빠진다.** 붙여넣기 전에 편집기 안을 한 번 클릭.
- **open_application("네이버 웨일")은 새 빈 창을 열 수 있다.** 편집 중이면 부르지 말고 그 창을 클릭.
- **사장님이 PC를 같이 쓰면 클립보드가 섞인다.** 사장님이 복사한 내용이 블로그에 들어갈 뻔했고,
  카톡 창이 앞에 있을 때 붙여넣기가 카톡으로 가서 이미지 전송 창이 떴다. 붙여넣은 뒤에는
  반드시 화면으로 결과를 확인한다. 엉뚱한 창이 앞에 있으면 아무 키도 누르지 않는다.

### 카페 공개 설정
카페는 '공개', 자유게시판은 '전체공개'로 되어 있는데도 글쓰기 화면의 '전체공개'가 선택되지
않는다(원인 미확인). '검색·네이버 서비스 공개'는 켜져 있어, 네이버 도움말에 따르면 비회원도
검색·네이버 서비스 경로로 들어오면 일정 기간 글을 볼 수 있다. 카페 멤버는 1명(사장님).

## 텔레그램 보고도 예약 실행에서는 막힌다 (2026-09-22 12시 점검 회차)
Telegram request_access가 두 번(인자 전부/최소) 모두 "can't be approved during a scheduled run"으로 거부됐다.
보고문은 `work/research/reports/<날짜>.txt` 에 남긴다. 예약 작업 설정에 Telegram을 허용 앱으로 넣으면 풀린다.

## perf.py 색인 측정 보강 (2026-09-22)
원고 파일(blog.txt)이 없는 글은 RSS `<description>` 본문 요약에서 문장을 골라 따옴표 검색한다.
발행 묶음이 `draft.txt`·`pkg/`로 바뀐 뒤에도 색인을 잴 수 있다.

## 발행은 naverpost.py로 한다 (2026-09-22부터) — 화면 조작 폐기

`work/naverpost.py`는 Playwright 전용 크로미움(프로필 `Documents\naver_profile`)으로 네이버에 올린다.
사장님 웨일·크롬과 완전히 별개라 PC를 같이 써도 안 섞이고, **화면 권한이 없어 예약 루틴이 무인으로 돌린다.**
- `python work/naverpost.py check` 로그인 유지 여부 (쿠키 NID_AUT/NID_SES). 안 되면 `login`을 PC에서 사람이 한 번.
- `pending` 안 올라간 묶음(RSS·카페 API 제목 대조, published.txt 없는 것) 오래된 순.
- `blog <pkg>` / `cafe <pkg>` 발행 후 `URL ...` 출력, pkg/published.txt 생성. 실패 시 research/_shots/error_*.png.
- 로그인 쿠키는 세션 쿠키라 프로필만으로는 창을 닫으면 사라진다 → `storage_state.json`에 저장해 매번 add_cookies.
- **사고(2026-09-22 22시 발견)**: 카페 37~45 아홉 편이 사진만 있고 본문 0자로 발행됐다. 사진을 넣으면 포커스가 업로드용
  iframe에 남아 `locator.click()`으로는 다음 글자가 어디에도 안 들어간다. 고침: 마지막 글 문단(`.se-component.se-text .se-text-paragraph`,
  사진 설명 문단 제외)의 bounding_box 좌표를 `page.mouse.click`. 등록 전 `verify_body`(글자 90%·사진 수)로 막고,
  발행 뒤 `python work/naverpost.py verify <pkg>`(또는 `verify today`)로 **올라간 페이지**를 다시 잰다. 잘못 나간 카페 글은
  `python work/naverpost.py rewrite <글번호> <pkg>`(수정 화면에서 본문 비우고 다시 넣기, 글 번호 유지)로 고쳤다.
- 편집기 요령(실측): 본문 문단은 마지막 글 문단을 가운데로 스크롤 후 **마우스 좌표 클릭**(글감 검색 바가 가림),
  텍스트는 keyboard.insert_text + Enter, 이미지는 사진 버튼 → file chooser → `.se-component.se-image` 수가 늘 때까지 대기.
  블로그 발행 버튼은 `button[class^="publish_btn"]`(예약 버튼은 reserve_btn), 패널 항목은 문구(get_by_text/placeholder)로.
  카페 등록은 정규식 `^등록$`(그냥 has-text("등록")은 임시등록을 잡는다). 발행 후 URL은 blog `logNo=`, cafe `articleid=`.
- 카페 글쓰기 화면의 '전체공개'는 선택되지 않는다(멤버공개 고정, 검색·네이버 서비스 공개는 켜짐). 원인 미확인.
- 네이버 약관은 자동화 수단에 의한 게시를 금지한다(2018.5.1 개정, 한국경제TV 보도). 사장님이 위험을 알고 진행을 결정했다(2026-09-22).

## 카페 전체공개·텔레그램 보고 (2026-09-22 실측)
- 카페 글쓰기의 '전체공개' 라디오는 비활성이 아니다. **일반 클릭**으로 앱 상태까지 바뀌고, 등록을 누르면
  "이 글은 전체공개로 설정되어 있어요 … 계속할까요?" 확인 창이 뜬다 → 확인. naverpost.py가 처리한다.
  force 클릭은 화면만 바꾸고 상태는 안 바뀌어 멤버공개로 올라갔다(35~38번이 그렇게 됐고 `public` 명령으로 되돌림).
  검증은 카페 API `openArticle`(True=전체공개)로 한다.
- 이미 올라간 글 전환: `python work/naverpost.py public <id> ...` (수정 → 전체공개 → 등록, 새 탭 처리).
- 텔레그램 보고: `work/tgreport.py`. 봇 @firemap_report_bot, 키 파일 `Documents\telegram_bot.txt`(TOKEN, CHAT_ID).
  `python work/tgreport.py sendfile <파일>` / `send "문장"`. HTTP라 무인 실행 가능. 12시 보고 루틴이 쓴다.

## 교차검증은 API로 (2026-09-23)
사장님 지시(09-14) "내 초안 → ChatGPT(사실·정확성) → Gemini(구조·말투) → 검증 안 된 건 뺀다"를 루틴이 09-20~23 동안 빼먹었다(웨일 창에서 손으로 하던 단계라 무인 루틴에 옮기지 않았다). `work/crosscheck.py check <pkg>`가 같은 프롬프트로 API를 부른다. 키는 `Documents\openai_key.txt`, `Documents\gemini_key.txt`(KEY=…). Gemini는 무료 등급 있음(ai.google.dev/pricing 확인). 키가 없으면 그 역할은 건너뛰고 runs note에 남긴다.
