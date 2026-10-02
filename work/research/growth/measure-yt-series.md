# 측정 시안 — yt-series (② 나 vs 남들 · ① N억 1년 뒤 · ③ B10) (firemap-growth, 2026-10-02 10:5x)
[시안 요청] plans/yt-series.md 59줄(growth: utm=yt-series·48시간 지표) 답. 실측 기준은 growth/channels.md 1장(로컬·internal·몰림 봇 제외).

## 1. utm — 기존 규칙(utm.md) 안에서, 시리즈는 campaign 앞머리로 묶는다
plans 5장의 'utm=yt-series'는 새 source를 만들면 집계가 쪼개지므로 **campaign 접두어**로 바꾼다. 영상·글 id 규칙(처음 쓴 값 유지)은 그대로.

| 시리즈 | campaign 접두어 | 롱폼 설명란 | 쇼츠 설명란 | 카페 같은 주제 글 본문 |
|---|---|---|---|---|
| ② 나 vs 남들 | `yts2-` | `?utm_source=youtube&utm_medium=desc&utm_campaign=yts2-<편폴더>` | `?utm_source=shorts&utm_medium=desc&utm_campaign=yts2-<편폴더>` | `?utm_source=cafe&utm_medium=post&utm_campaign=yts2-<글폴더>` |
| ① 1억의 1년 영수증 | `yts1-` | 같은 꼴 | 같은 꼴 | 같은 꼴 |
| ③ B10 | `b10`(이미 등록, 바꾸지 않음) | — | `?utm_source=shorts&utm_medium=desc&utm_campaign=b10` | `?utm_source=cafe&utm_medium=post&utm_campaign=b10` |
- 링크 목적지: ② → `/calc/salary`(연봉 '당신 숫자' 칸), ① → `/`(예금·투자 비교 계산기 없음 — 확인 안 함, 생기면 그 경로). 한 편·한 글에 firemap.kr 링크 **1개**.
- 편폴더 = 작업 폴더 이름(예 `s2salary1005`). 업로드 뒤에도 영상 id로 바꾸지 않는다.
- 점검·미리보기는 `&fm_internal=1`을 덧붙여 연다(집계에서 빠짐).

## 2. 48시간 지표 — 누가·어디서·언제
| 지표 | 원천 | 담당 수집 | 시점 |
|---|---|---|---|
| 롱폼 조회 48h | YouTube Data API(youtube-loop 순찰 값) | youtube-loop → growth가 daily.md에 옮김 | 공개 +48h |
| 쇼츠 컷 조회 48h (기준 285) | 같음 | shorts·youtube-loop | 공개 +48h |
| 카페 글 2일 조회 (기준 10) | 카페 공개 목록 API ArticleListV2dot1(cafe-views-1002.md 방식) | growth | 공개 +48h |
| 사이트 유입 | firemap_events session_start, campaign `like 'yts2-%'` 등 | growth | +48h · +7일 |
| 사이트 행동 | 같은 기기의 calc_complete·calc_submit | growth | +48h · +7일 |
- 사이트 유입은 판정 기준이 아니라 **보조 숫자**(plans 5장: 판정 지표는 유입이지만 영상 조회 기준이 먼저). 표본이 10기기 미만이면 비율은 적지 않고 숫자만 적는다.

## 3. 집계 SQL(growth, 편마다 +48h)
```sql
with e as (select client_id, event, props, ts from firemap_events where ts > now() - interval '9 days'),
bad as (select distinct client_id from e where props->>'host' ~ '(127\.0\.0\.1|localhost|pages\.dev)' or props->>'internal' in ('1','true')),
s as (select client_id, props->>'utm_source' src, props->>'utm_campaign' camp, min(ts) f from e
      where event='session_start' and props->>'utm_campaign' ~ '^(yts1-|yts2-|b10)' and client_id not in (select client_id from bad) group by 1,2,3)
select camp, src, count(distinct s.client_id) dev,
  count(distinct s.client_id) filter (where exists (select 1 from e x where x.client_id=s.client_id and x.event in ('calc_complete','calc_submit') and x.ts>=s.f)) calc_dev
from s group by 1,2 order by 1,2;
```
- 같은 utm이 같은 초에 2기기 이상 = 점검 추정(channels.md 4번), 60초 안 2기기+각자 화면 1개 = 몰림 봇(5번) — 둘 다 뺀 값과 원값을 함께 적는다.

## 4. 공개 전 점검(각 편 담당이 공개 직전 1회)
1. 설명란 링크를 `&fm_internal=1` 붙여 한 번 연다 → growth가 SQL로 internal=1 session_start에 campaign이 찍혔는지 확인.
2. 링크가 유튜브에서 눌리는지(쇼츠 설명 링크는 눌리지 않을 수 있다 — 확인 안 함, behavior 10/3 설계 8번 결과 따름).

## 5. 기록 자리
- 편마다 daily.md에 한 줄: `<날짜> yt-series <편> · 조회48h · 쇼츠48h · 카페2일 · 사이트 기기/계산 기기`.
- 10/23 시리즈 판정 표는 growth가 10/23 10:40 회차에 plans/yt-series.md 6장 아래에 채운다.
