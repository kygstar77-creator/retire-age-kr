# 운영 반영 통과 기록 (work/shipgate.py가 읽는다)
- 한 줄 = 한 커밋 한 관문: `- <sha7> 편집 통과 <task-id HH:MM>` · `- <sha7> 디자인 통과 <task-id HH:MM>` · 해당 없으면 `- <sha7> 편집 해당없음 <이유>`
- 검수자가 today.md에 통과를 쓸 때 여기에도 한 줄, 또는 커밋한 사람이 통과 줄을 보고 옮긴다. 날짜 순으로 아래에 더한다.
- 2026-10-05 firemap-improve: 이 장부에 줄이 없으면 dev:main 푸시가 막힌다(.git/hooks/pre-push 종료 1). --no-verify 금지.

## 2026-10-05 (사후 기록 — 이미 운영에 있음)
- c7d1ba4 디자인 통과 firemap-designer 13:42 (연봉 v5 구현본)
- c7d1ba4 편집 통과 firemap-editor-web 15:48 (사후, 운영 반영 뒤 — 게이트 어김 1건으로 남김)
- 1eb9cc4 편집 통과 firemap-editor-web 21:08 (today.md 완료 줄 옮김, firemap-improve 22:49 — 디자인은 판정 고친 뒤 해당 아님: 같은 클래스 안 글자만)
