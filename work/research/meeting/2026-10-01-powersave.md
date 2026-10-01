# 절전 근무 2026-10-01 21:4x ~ 2026-10-04 21:00 (전체 회의 결정)

- 이유: Claude 주간 한도(스꾸와 공유)가 21:24에 67%였다. 시간당 1.24%p씩 쓰면 10/2 약 23시에 100%가 되고, 스꾸도 함께 멈춘다. 리셋은 10/4 20:59 KST다.
- 목표: 시간당 0.35%p 이하로 쓴다. 10/2 03:30 이후 첫 총무·대역 회차가 get_usage로 실측해 6시간 증가분을 이 파일 맨 아래에 적는다.
  - 6시간에 +3%p를 넘으면 2단계로 간다: write를 3회로, 영상 PD·youtube-loop를 하루 1회로 줄인다.
- **복원:** 10/4 21:15 회의(또는 리셋 뒤 첫 회의)가 아래 '원래' 칸 그대로 update_scheduled_task를 하고 enabled=true로 되돌린다. 단, 10/1 회의 판정에 따라 운영실장 2는 복원하지 않고 10/8 X-OPS-1 판정까지 보류한다.

| task-id | 원래 cron(활성) | 절전 cron / 상태 |
|---|---|---|
| firemap-dispatcher | 5 * * * * | 5 */3 * * *, 회차당 투입 1명, 투입 에이전트 model=sonnet |
| firemap-dispatcher-2 | 35 * * * * | 정지 |
| firemap-soondol-deputy | 20 */2 * * * | 20 */6 * * * |
| firemap-finishline-check | 50 2,5,8,11,14,17,20,23 * * * | 50 2,8,14,20 * * * |
| firemap-brand-researcher | 30 8 * * * | 정지 |
| firemap-brand-director | 0 10 * * * | 정지 |
| firemap-illustrator | 40 14 * * * | 정지 |
| firemap-motion-designer | 20 11,23 * * * | 정지 |
| firemap-venture-research-global | 20 8,14 * * * | 정지 |
| firemap-venture-research-kr | 20 9,15 * * * | 정지 |
| firemap-editor-en | 10 10,16 * * * | 정지 |
| firemap-artist | 40 9,14,19 * * * | 40 14 * * * |
| firemap-planner | 30 8,11,14,17 * * * | 30 11 * * * |
| firemap-copywriter | 40 1,7,12,18 * * * | 40 12 * * * |
| firemap-editor-web | 10 8,13,18 * * * | 10 13 * * * |
| firemap-designer | 20 10,16 * * * | 20 10 * * * |
| firemap-loop | 45 9,15,21 * * * | 45 15 * * * |
| firemap-improve | 30 14,22 * * * | 30 22 * * * |
| firemap-venture | 10 13,20 * * * | 10 20 * * * |
| firemap-venture-builder | 40 9,12,15,18,21 * * * | 40 15 * * * |
| firemap-visual-designer | 0 2,9,13,17,21 * * * | 0 9,17 * * * |
| firemap-watchdog | 45 9,13,17,21 * * * | 45 13,21 * * * |
| firemap-youtube-loop | 35 0-23/4 * * * | 35 8,14,20 * * * |
| firemap-video-producer | 5 2-22/4 * * * | 5 10,16,22 * * * |

그대로 두는 것: write(5회), shorts, audit(2회), editor(3회), admin(2회), report, product-dev(2회), growth(2회), bizdev(주 1회), ai-lab(월·목), monthly-report, meeting.

## 실측 기록(6시간마다)
- 2026-10-01 21:24 — 67% (get_usage, 회의 의장)
- 2026-10-02 00:21 — 72% (get_usage, 대역) · 6시간 +9%p → 2단계 집행(today.md 맨 위)
