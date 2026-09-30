# 파이어맵 상황판 — 새로 고치는 법

상황판: https://claude.ai/artifact/T19NbGV17UaZaX8wWmuyyB (사장님 휴대폰용, 비공개)

두 가지가 따로 움직인다.
- **실시간 책상 상태**: 직원이 회차 시작·끝에 상황판 데이터베이스(`status` 컬렉션)에 직접 적는다. 규칙은 STATUS.md. 다시 게시할 필요 없다.
- **나머지 전부**(결재·숫자·직원 칩·일감·결정·실험): 아래 3단계로 다시 만들어 같은 주소에 다시 게시한다.

## 1. MCP 자료 모으기 → `work/dashboard/mcp_input.json`
Python은 MCP를 못 부르므로 세션이 모아 파일에 넣는다. 형식은 지금 파일 그대로.
1. ToolSearch `select:mcp__scheduled-tasks__list_scheduled_tasks,mcp__scheduled-tasks__list_task_runs,mcp__ccd_session_mgmt__get_usage`
2. `list_scheduled_tasks` → `taskId`가 `firemap-`로 시작하는 것만 `tasks`에 넣는다(taskId·title·description·schedule·enabled·nextRunAt·lastRunAt). **seukku 작업은 넣지 않는다.** 꺼진 1회성 작업은 넣어도 빌더가 버린다.
3. 켜진 firemap 작업마다 `list_task_runs`(limit 3) → `runs["<taskId>"]`에 status·started_at·last_activity_at(있으면 error·summary). session_id는 안 넣어도 된다.
4. `get_usage` → `usage.weekly_all`(Weekly · all models의 percentUsed·resetsAt), `usage.five_hour`.
5. `captured_at`을 지금 UTC로, `manual.revenue_krw`는 실측 수익(모르면 키를 지운다 → 화면에 '확인 안 함').

## 2. 빌드
```
py -3.12 work/dashboard/build.py
```
`data.json`과 `board.html`(자료를 박아 넣은 페이지)을 쓴다. 저장소 파일(agents.md·meeting/today.md·approvals.md·decisions/log.md·experiments-registry.md·roadmap.md·growth/daily.md·runs_today.json·쇼츠 log·롱폼 uploads·git log 24시간)은 스크립트가 직접 읽는다.
화면 틀을 고칠 땐 `board.template.html`을 고치고 다시 빌드한다. `board.html`을 손으로 고치지 않는다.

## 3. 같은 주소에 다시 게시
Artifact 도구: `file_path` = `work/dashboard/board.html`, `url` = 위 주소. `capabilities`는 빼서 기존 선언(db)을 그대로 둔다. `icon`도 뺀다.
다른 대화에서 처음 게시할 때는 먼저 `action: "read"`로 그 주소를 읽어야 게시가 받아들여진다.

## 판정 규칙(build.py)
- 칩: 마지막 회차 실패 → 실패 · 근무 중 → 일함 · 회차 없음 → 대기 · 마지막 기록에 "발행 없음/대본 없음/만들 편 없음" → 헛돎 · 기록 있음 → 일함 · 24시간 기록 없음 → 확인 안 함.
- 커밋 접두어 → 직원 매핑은 build.py `PREFIX`. 새 직원을 뽑으면 `DEPTS`·`NAME`·`PREFIX`에 한 줄씩 더한다(안 더해도 '미분류'로 나온다).
- 키·토큰·계정 식별자·메일은 `REDACT`로 가린다.
