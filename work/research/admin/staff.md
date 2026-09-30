# 직원 명부 — 총무·인사팀(firemap-admin)
마지막 대조: **2026-09-30 23:39** (list_scheduled_tasks + list_task_runs 최근 7회). 스꾸 예약 작업은 조직 밖이라 적지 않는다.
헛돎 판정: 회차가 1분 안에 끝나면 '헛돎 의심'(감시처럼 원래 짧은 자리는 제외). 내용은 열어 보지 않았다 → '의심'까지만.
성숙도는 conductor-manual.md 표를 옮긴 것. 표에 없는 자리는 '신규'.

| 직원(예약 작업) | 근무(실제 cron, KST) | 최근 7회 | 헛돎 | 사고 사례 | 성숙도 |
|---|---|---|---|---|---|
| firemap-write 카페·블로그 작가 | 01:10부터 3시간마다 | 성공 7 / 실패 0 | 없음 | 블로그 9/23 이후 무색인 → STOP_blog | 중간 |
| firemap-watchdog 발행 감시 | 02:45부터 3시간마다 | 성공 7 / 실패 0 | 해당 없음(1분 점검) | 발행 멈춤을 못 잡던 이력(firemap-publish-watchdog) | 높음 |
| firemap-report 보고 비서 | 12:30 | 성공 7 / 실패 0 | 없음 | — | 높음 |
| firemap-improve 생산·개선 | 14:30·22:30 | 성공 7 / 실패 0 | 없음 | — | 표에 없음 |
| firemap-loop 디자인 개선 | 09:45·15:45·21:45 | 성공 7 / 실패 0 | 없음(4분 회차 3번 — 짧음) | — | 표에 없음 |
| firemap-shorts 쇼츠 PD | 19:20 | 성공 5 / 실패 0 (전체 5회) | 없음 | 9/30 하루 2회 돎(10:26·11:59 UTC) — 일정 변경 날 | 중간 |
| firemap-youtube-loop 유튜브·카페 총괄 | 4시간마다 :35 | 성공 6 / 실패 0 (전체 6회) | 없음 | — | 표에 없음 |
| firemap-video-producer 영상 PD | 02:05부터 4시간마다 | 성공 5 / 실패 0 (전체 5회) | **의심 2회**(9/30 18:17 30초, 22:17 42초) — 만들 편이 없을 때 도는 듯 | A-1 썸네일 재작업 | 낮음(썸네일) |
| firemap-audit 감사관 | 07:40·19:40 | 성공 2 / 0 | 없음 | — | 표에 없음 |
| firemap-product-dev 제품 개발 | 11:10·17:10 | 성공 2 / 0 | 없음 | 푸시가 권한 검사에 막힘(9/30, 사장님 승인으로 처리) | 중간 |
| firemap-growth 성장·유입 | 10:40·16:40 | 성공 2 / 0 | 없음 | GA4·서치콘솔 못 읽음(결재 대기) | 중간 |
| firemap-meeting 전체 회의 | 21:15 | 성공 1 / 0 | 없음 | — | 표에 없음 |
| firemap-venture 신사업 | 13:10·20:10 | 성공 1 / 0 | 없음 | — | 낮음 |
| firemap-designer 전담 디자이너 | 10:20·18:20 | 성공 1 / 0 | 없음 | — | 낮음 |
| firemap-copywriter 카피라이터 | 07:20·15:20 | 성공 1 / 0 | 없음 | — | 낮음 |
| firemap-artist 예술가 | 11:40 | 성공 1 / 0 | 없음 | — | 낮음 |
| firemap-bizdev 사업개발 | 월 10:15 | 성공 1 / 0 | 없음 | — | 표에 없음 |
| firemap-editor 문장 편집자 | 06:50·12:50·17:50 | **아직 0회**(첫 근무 10-01 07:03) | — | — | 낮음 |
| firemap-visual-designer 비주얼 | 09:10·14:10 (설명은 20:40도 적혀 있으나 cron엔 없음) | 아직 0회 | — | — | 신규 |
| firemap-motion-designer 모션 | 11:20·23:20 | 아직 0회 | — | — | 신규 |
| firemap-illustrator 일러스트 | 13:40 | 아직 0회 | — | 캐릭터 폐기(9/30)로 역할 변경 — 설명엔 아직 "흰 고양이" | 신규 |
| firemap-brand-director 브랜드 디렉터 | 10:00 | 아직 0회 | — | — | 신규 |
| firemap-brand-researcher 브랜드 리서처 | 08:30 | 아직 0회 | — | — | 신규 |
| firemap-admin 총무·인사(나) | 07:00·19:00 | 이번이 1회차 | — | — | 신규 |
| firemap-designer-orgchart (1회 근무) | 09-30 23:45 1회 | 대기 | — | — | — |

## 명부와 실제가 다른 것
- **firemap-ai-lab**: SKILL.md 폴더만 있고(23:36 생성) 예약 작업 목록엔 **없다** → 근무 안 함. 결정 로그상 "운영실장 등록은 안전장치에 막힘"과 같은 사정으로 보임(확인 안 함).
- 폴더만 남은 옛 작업: firemap-report-0921, firemap-test-0921 (목록에 없음, 무해).
- firemap-titletest-followup: 1회용, 꺼짐.

## 지시문 공통 규칙 점검 (O=있음, X=없음 — 문자열 검사)
기준: 스꾸 금지 · lessons.md · 실험 장부(experiments-registry) · 헛돌지 않기 · 경쟁 비교 · 푸시 명령 `git -C ... push -q origin dev`

| 직원 | 스꾸 | 교훈 | 실험 | 헛돎 | 경쟁 | 푸시 |
|---|---|---|---|---|---|---|
| write | X | O | O | O | O | X |
| watchdog | X | O | X | X | O | X |
| report | X | O | X | X | O | X |
| improve | X | O | X | O | O | O |
| loop | X | O | X | O | O | O |
| shorts | O | O | O | O | O | X |
| video-producer | O | O | O | O | O | X |
| audit | O | O | X | X | O | X |
| bizdev | O | O | X | O | O | X |
| meeting | O | O | O | O | O | X |
| artist | O | O | X | O | O | O |
| designer | O | O | X | O | O | O |
| editor | O | O | X | O | O | O |
| venture | O | O | X | O | O | O |
| illustrator | O | O | X | X | O | O |
| motion-designer | O | O | X | X | O | O |
| visual-designer | O | O | O | X | O | O |
| brand-director | O | O | O | X | O | O |
| brand-researcher | O | X | X | X | O | O |
| copywriter · growth · product-dev · youtube-loop | O | O | O | O | O | O |

푸시 X인 곳 중 일부는 옛 형태 `git push origin ...`(merge 후 push)를 쓴다. 지시문 수정은 순돌이·회의 몫 → today.md '추가 필요'에 올림.

## 2026-10-01 07:5x 대조 (2회차, 바뀐 것만)
- 최근 회차 실패 0건: write 7/7, video-producer 7/7, youtube-loop 7/7, audit 2/2, dispatcher 3/3(+1 실행 중).
- 영상 PD 헛돎 의심 해소: 최근 2회 12분·68분(21:16 UTC 회차) — 일감이 생김.
- 운영실장(dispatcher) 19:46 UTC 회차가 **2시간 47분** 이어짐 → 매시 :05 회차와 겹침. 그래서 운영실장 2(:35)가 생긴 것으로 보임. 운영실장 2는 아직 실행 0회(첫 회차 08:35 예정) → 다음 회차 온보딩 점검.
- 새 자리(09-30 23:39 이후 등록): firemap-dispatcher-2, firemap-finishline-check(3시간마다 :50, 아직 0회), firemap-venture-builder(5회/일), firemap-venture-research-global·kr(각 2회/일). 첫 회차 결과는 venture-builder만 확인(today.md 07:34 완료 기록 있음).
- 근무 시각 불일치: venture-researcher-global 설명 08:20 vs cron 20 8,14 일치. artist 설명 "11:40·19:10"인데 cron은 11:40만. brand-director 설명 10:00·제목 10:10 vs cron 0 10.
