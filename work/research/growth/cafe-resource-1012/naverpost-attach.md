# naverpost.py 카페 옵션 — 파일 첨부·멤버공개 (발행 도구 담당, 2026-10-12)

상태: **코드 추가·화면 시험 끝. 실제 등록은 안 했다.** 순돌이가 검토한 뒤 실제 발행에 쓴다.

## 1. 쓰는 법 (pkg/order.txt에 줄 추가)
```
카페 발행
제목: title.txt
게시판: 자유게시판
c00.txt
img/00.png
attach: ventures/x-kr-1/out/가계부_은퇴나이_2026.xlsx
visibility: members
```
- `attach: <경로>` 한 줄에 파일 하나, 여러 줄 가능. `attach: ["a.xlsx", "b.xlsx"]`도 받는다. 경로 규칙은 사진과 같다(절대경로 → `pkg/..` 기준 → `pkg` 기준).
- `visibility: members`(또는 `"members"`·`멤버공개`). `public`·`전체공개`는 지금과 같다.
- 파일은 본문을 다 넣은 뒤 **본문 끝**에 붙는다(order.txt의 줄 위치와 상관없다).
- 두 줄이 없으면 아무것도 바뀌지 않는다. 지금 있는 order.txt 372개 중 이 줄이 있는 것은 0개다.

## 2. 바뀐 코드 (work/naverpost.py만)
| 자리 | 내용 |
|---|---|
| `pkg_options(pkg)` 새 함수 | order.txt에서 attach·visibility만 읽는다. 파일 없음·50MB 초과·모르는 공개 값이면 ValueError |
| `read_pkg` | 옵션 줄은 본문·사진 순서에서 빼고 `meta['attach']`·`meta['visibility']`에 넣는다 |
| `main()` (blog/cafe) | 쉬기 전에 옵션을 검사한다. 옵션 오류 또는 **블로그 묶음에 옵션이 있으면 exit 4**(올리지 않음) |
| `post_cafe` | `verify_body` 뒤에 `attach_file`을 파일마다 부르고 파일 칸 수를 센다(모자라면 등록 안 함). `visibility == 'members'`면 `set_cafe_members`(실패하면 등록 안 함), 아니면 지금처럼 `set_cafe_public` |
| `attach_file` 새 함수 | 파일 버튼 → '내 컴퓨터' → 파일 고르기 → 업로드 응답(200)과 본문 파일 칸·파일 이름을 확인한다. 하나라도 없으면 멈춘다 |
| `set_cafe_members` 새 함수 | '공개 설정'을 펼쳐 `label[for=member]`를 누른다. `input#member` 체크·`input#all` 해제를 확인한다. '검색·네이버 서비스공개' 상태는 로그에만 남긴다 |
| `post_blog` | 옵션 있는 묶음이면 RuntimeError(이중 안전) |
| `rewrite_cafe` | 옵션 있는 묶음이면 거부(본문을 비우면 파일 칸이 지워지고 전체공개로 다시 등록되기 때문) |

건드리지 않은 것: DAY_CAP(카페 8편)·간격(gap_min)·rate_guard·jitter·day_guard·STOP 스위치·사진 수 관문·표지 관문·읽기 검사·aitell·editgate·same_subject·submit_cafe.

## 3. 찾은 선택자 (2026-10-12 20:0x~20:43 발행 프로필 headless로 글쓰기 화면을 열어 확인)
- 파일 버튼: `button[data-name="file"]`(도구 막대 '파일'). 누르면 파일 고르기 창이 바로 뜨지 않는다. 대신 **'파일 불러오기' 창**이 뜬다("파일당 50MB까지 첨부 가능합니다", 내 컴퓨터 / 네이버 MYBOX).
- 내 컴퓨터: `button.se-popup-file-source-button-local, button:has-text("내 컴퓨터")`. 이것을 눌러야 파일 고르기 창(filechooser, 한 개씩)이 열린다. 첫 조각은 DOM 덤프에서 클래스 앞 60자(`se-popup-file-source-button se-popup-file-source-button-loca…`)만 봤다. 클래스 전체 이름은 확인하지 않았다. 그래서 글자로 찾는 조각을 같이 둔다.
- 업로드 요청: `POST https://upapi.cafe.naver.com/v1.0/cafes/editor/files` → 200.
- 첨부 결과: `.se-component.se-file` 아래 `.se-file-name`에 파일 이름이 그대로 나온다. 화면에는 초록 체크가 보인다(`.se-file-status-icon`의 클래스에는 완료 표시가 따로 없었다).
- 공개 설정: `button.btn_open_set`('공개 설정', 눌러야 펼쳐짐). 라디오는 `input#all[name=public][value=true]`(전체공개)와 `input#member[name=public][value=false]`(멤버공개)다. 라벨은 `label[for=member]`.
- **새 글의 기본값은 멤버공개다**(probe1 DOM: member checked=True). 지금 코드가 매번 전체공개를 눌러 바꿔 왔다.
- '검색 · 네이버 서비스공개': `input#permit`, **기본 켜짐**. 화면 안내 문구: "검색 ∙ 네이버 서비스 공개 허용 시 멤버가 아닌 사람도 글을 볼 수 있는 경우가 있습니다."

## 4. 시험 결과 — 등록·임시등록 안 누름, 제목·본문 안 넣음
최종 시험은 새 함수(`attach_file`·`set_cafe_members`)를 그대로 불러 돌렸다(probe_final.py).
```
임시등록 before: 임시등록 1
파일 첨부: 가계부_은퇴나이_2026.xlsx · 업로드 응답 [200] · 본문 파일 칸 ['가계부_은퇴나이_2026.xlsx']
멤버공개: 선택됨 (검색·네이버 서비스공개 켜짐)
등록 버튼 개수(누르지 않음): 1
임시등록 after 20s: 임시등록 1
임시등록 on reopen: 임시등록 1
```
- 등록 직전 캡처: 본문에 `가계부_은퇴나이_2026.xlsx` 칸과 초록 체크가 보이고, 공개 설정에 ●멤버공개 ○전체공개가 보인다.
- 임시등록 수는 시험 전·후·다시 열었을 때 모두 1이다(원래 있던 1개). POST 요청은 graphql 조회(homeHealthStatus·cafeApiHealthStatus·editorMeta)와 파일 업로드 1건뿐이었다. 저장 요청은 없었다.
- 회귀 확인:
  - py_compile 통과.
  - 기존 pkg 370개(title.txt 있는 것)로 옛 `read_pkg`와 새 `read_pkg` 결과를 대조했다. 370개 모두 같았다.
  - 옵션 파싱 단위 확인을 통과했다(절대·상대·JSON 목록·멤버공개 별칭·없는 파일 거부·모르는 값 거부).
  - 시험 도중 20:21~20:42에 무인 회차가 이 수정본으로 `cafe med1011`을 올렸다(옵션 없음). 결과는 firemap/255이고 verify ok(1487/1487자, 사진 3/3)였다.
- work/tests: 79 통과, 3 실패. 실패 3건은 test_lfrender·test_r1_visual_v6(롱폼 R-1 영상)이다. naverpost를 import하지 않는다. 같은 시각에 R-1 자료가 바뀌는 중이었다(커밋 5a0fbe9 'pd: R-1').

스크린샷(scratchpad, `C:\Users\강영준\AppData\Local\Temp\claude\C--Users-----Documents-Codex\0a2acdc7-66d4-4f89-8e2d-a7e9e75c81f6\scratchpad\attach\`):
- `p1_02_popups_closed.png` — 첫 화면(공개 설정 접힘, 기본 멤버공개, 임시등록 1)
- `p2_04_open_set.png` — 파일 버튼을 누른 뒤 뜬 '파일 불러오기' 창
- `f01_open.png` — 최종 시험 시작
- `f02_attached.png` — 파일 첨부 직후
- **`f03_before_submit.png` — 등록 직전(파일 첨부됨·멤버공개 선택됨)**
- `f04_reopen_before_popups.png` — 닫고 다시 연 화면(임시등록 1 그대로)
- 시험 스크립트: `probe1.py`(DOM 읽기), `probe3.py`, `probe_final.py`, `unit.py`, `regress.py`

## 5. 남은 위험 (실제 발행 전에 순돌이가 정할 것)
1. **'검색·네이버 서비스공개'가 켜진 채 나간다.** 멤버공개여도 비회원이 검색으로 볼 수 있는 경우가 있다고 화면이 직접 말한다. 끄는 칸은 `input#permit`(label[for=permit])으로 확인했다. 이번 지시 범위(첨부·멤버공개)가 아니어서 코드는 건드리지 않았다. 끌지는 순돌이가 정한다.
2. **등록 뒤 단계는 시험하지 않았다.** `submit_cafe`는 전체공개 확인 창("계속할까요")을 8초 기다린다. 멤버공개 글에서 이 창이 안 뜨면 '확인 창 처리 실패' 줄과 `cafe_confirm_fail.png`가 남고 다음 단계로 넘어간다. 등록에는 지장이 없을 것으로 보지만 실제로 본 적은 없다. 멤버공개 글 등록 뒤 확인 창이 뜨는지도 모른다.
3. **기존 관문이 그대로라 파일 글에도 사진 3장(정사각 표지 첫 장·cover_review.md 평균 7점 이상)·읽기 검사·aitell을 요구한다.** 그림 없는 파일 글이면 `--noimg-ok --cover-ok`가 필요하다. 하루 8편·90분 간격에도 같이 센다.
4. **발행 뒤 검증이 공개 범위를 보지 않는다.** `verify`는 글자·사진 수만 센다. 첫 발행 뒤에는 로그아웃 창으로 주소를 열어 본문과 파일이 가려지는지 사람이 한 번 본다(publish-check.md 3장 7번).
5. **이 옵션을 모르는 다른 길.** `cafeapi.py`(중지 상태)는 `read_pkg`를 쓰지만 attach·visibility를 무시한다. 그래서 이 묶음을 그 길로 보내면 **전체공개·파일 없이** 나간다. `cafeedit.py`(edit/editimg/edittitle)와 `public` 명령은 늘 전체공개로 다시 등록한다. 멤버공개 글에 쓰면 전체공개로 바뀐다. `rewrite`만 막아 두었다.
6. 시험 때 파일 1개가 네이버 업로드 서버(upapi)로 올라갔다. 글에는 붙지 않았다. 그 파일이 서버에 얼마나 남는지는 모른다(확인 안 함).

## 6. 추가 변경 (2026-10-12 순돌이 결정 반영)
1. **`visibility: members`면 '검색·네이버 서비스공개'를 끈다.** `set_cafe_members`가 멤버공개를 고른 다음, `input#permit`이 켜져 있으면 `label[for=permit]`을 눌러 끈다(최대 2번). 멤버공개 선택(`#member` 켜짐·`#all` 꺼짐)과 `#permit` 꺼짐이 모두 확인돼야 True를 돌려준다. 아니면 post_cafe가 '멤버공개·검색공개 끄기 실패 — 등록하지 않음'으로 멈춘다. members가 아니면 이 칸을 건드리지 않는다(전체공개 경로는 그대로).
2. **`submit_cafe(page, title=None, members=False)`.** members=True일 때는 전체공개 확인 창("계속할까요")을 8초 기다리지 않는다. 그 순간 창이 떠 있으면 보이는 '확인'을 누르고, 없으면 바로 넘어간다. '확인 창 처리 실패' 줄이나 `cafe_confirm_fail.png`는 남지 않는다. members=False(기본값)는 예전 블록 그대로다. 다른 호출(cafeedit·titletest·cafe_make_public·rewrite_cafe)은 인자를 안 주므로 바뀌지 않는다.

확인 (등록·임시등록 안 누름, probe_permit.py):
```
파일 첨부: 가계부_은퇴나이_2026.xlsx · 업로드 응답 [200] · 본문 파일 칸 ['가계부_은퇴나이_2026.xlsx']
멤버공개: 선택됨 · 검색·네이버 서비스공개 꺼짐
set_cafe_members -> True {'member': True, 'all': False, 'permit': False}
임시등록 before 1 · after 20s 1 · reopen 1
```
- 등록 직전 캡처: scratchpad `attach\g03_before_submit.png`. 파일 칸과 초록 체크가 보이고, ●멤버공개, '검색 · 네이버 서비스공개' 체크 해제 상태다. 같은 폴더에 g01·g02·g04가 있다.
- py_compile 통과. 옛·새 read_pkg 대조는 372/372 같음, 옵션 단위 확인 통과.
- work/tests: 79 통과, 3 실패. 실패한 3건은 앞(4장)과 같은 롱폼 R-1 시험이다. naverpost를 import하지 않으며, 이번 변경 전에도 같은 3건이 실패했다.
- 멤버공개 글에서 등록 뒤 확인 창이 정말 안 뜨는지는 여전히 실제 등록으로 본 적이 없다. 뜬다면 위 1번 동작처럼 그 자리에서 누른다. 다만 창이 늦게(등록 직후 1.5초 넘어) 뜨면 못 누를 수 있다. 그때는 30초 이동 실패 뒤 목록 확인(already_up)으로 넘어간다.
