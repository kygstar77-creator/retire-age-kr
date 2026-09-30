# 상황판 실시간 상태 적기 (모든 직원 공통 규칙)

사장님 상황판: https://claude.ai/artifact/T19NbGV17UaZaX8wWmuyyB

상황판 '지금 사무실'의 책상은 직원이 직접 적은 상태를 30초 안에 보여 준다.
회차를 시작할 때 한 번, 끝낼 때 한 번 적는다. 적는 곳은 상황판 데이터베이스의 `status` 컬렉션이고, 문서 이름은 내 예약 작업 ID다(예: `firemap-write`). 순돌이는 `soondol`.

## 필드
| 필드 | 값 |
|---|---|
| `state` | `일하는 중` · `쉬는 중` · `막힘` · `실패` 중 하나(글자 그대로) |
| `task` | 지금 하는 일 한 줄(80자 안). 끝나면 빈 문자열 |
| `started_at` | 회차 시작 시각, ISO 8601 KST. 예 `2026-10-01T08:10:00+09:00` |
| `finished_at` | 회차 끝 시각, 같은 형식. 일하는 중이면 빈 문자열 |
| `last_output` | 이번 회차 결과 한 줄(80자 안). 예 "카페 186 발행·verify OK" |

## 회차 시작 (2번 호출)
ArtifactData 도구는 ToolSearch `select:ArtifactData`로 불러 쓴다.

1. 지금 버전을 읽는다.
```json
{"action": "get", "url": "https://claude.ai/artifact/T19NbGV17UaZaX8wWmuyyB", "collection": "status", "doc_id": "<내 작업 ID>"}
```
2. 결과의 `version`을 `if_version`에 넣어 합친다(update는 적은 필드만 바꾼다).
```json
{"action": "update", "url": "https://claude.ai/artifact/T19NbGV17UaZaX8wWmuyyB", "collection": "status", "doc_id": "<내 작업 ID>", "if_version": <읽은 version>,
 "data": {"state": "일하는 중", "task": "<지금 하는 일 한 줄>", "started_at": "<지금 ISO KST>", "finished_at": ""}}
```
결과에 새 `version`이 나온다. 끝날 때 쓰려고 기억해 둔다.

## 회차 끝 (1번 호출)
```json
{"action": "update", "url": "https://claude.ai/artifact/T19NbGV17UaZaX8wWmuyyB", "collection": "status", "doc_id": "<내 작업 ID>", "if_version": <시작 때 받은 새 version>,
 "data": {"state": "쉬는 중", "task": "", "finished_at": "<지금 ISO KST>", "last_output": "<결과 한 줄>"}}
```
- 결과 없이 끝났으면 `last_output`에 사실 그대로("상한 도달로 발행 없음").
- 막혔으면 `state`를 `막힘`, `task`에 무엇에 막혔는지, `last_output`에 풀 사람·방법.
- 실패했으면 `state`를 `실패`, `last_output`에 오류 한 줄.

## 막힐 때
- 버전이 바뀌었다는 오류: `get`으로 다시 읽고 같은 update를 새 `version`으로 한 번 더.
- 문서가 없다는 오류(새로 뽑힌 직원): `if_version` 없이 `set`으로 다섯 필드를 모두 적는다.
- 상황판 쓰기가 안 돼도 본 업무는 멈추지 않는다. 회차 기록(decisions·로그)에 "상황판 기록 실패: 이유"를 한 줄 남긴다.

## 금지
- 키·토큰·비밀번호·계정 메일·결제 정보를 적지 않는다. 상황판은 사장님 휴대폰에 그대로 보인다.
- 스꾸(seukku) 작업·내용을 적지 않는다.
- 남의 문서(다른 작업 ID)를 고치지 않는다. 순돌이만 예외.
- 짐작으로 적지 않는다. 모르면 "확인 안 함".
