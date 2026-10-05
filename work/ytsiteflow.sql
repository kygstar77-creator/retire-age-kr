-- 유튜브 영상 → 파이어맵 사이트 유입, 영상별(utm_campaign=영상ID) (firemap-youtube-loop, 2026-10-05).
-- Supabase c7cd8a90 execute_sql에 붙여 쓴다. 날짜만 바꾼다(아래 두 곳 '2026-10-05').
-- 거름은 work/sitedaily.sql과 같다(growth 10/5 요청): 거름 1 봇·내부·로컬 기기 통째로 뺌,
-- 거름 2 utm 첫 진입 ±60초 안 같은 utm_source 새 기기 3대 이상 + 화면 1개 말고 행동 없음 = 링크 미리보기 몰림 → 뺌.
-- 설명란을 고친 직후 1~3분 몰림이 사람으로 세어지지 않게 한다. 계산·클릭을 한 기기는 몰림 안이어도 남긴다.
-- 같은 목적의 work/sql/yt_inflow.sql(firemap-loop, 14일치·몰림 창 다름)과 다르다: 이것은 growth 거름 정의(sitedaily.sql)와 숫자를 맞추는 하루치 표.
with allss as (
  select client_id, ts, props->>'utm_source' src, props->>'utm_campaign' camp from firemap_events
  where event='session_start' and (ts at time zone 'Asia/Seoul')::date = date '2026-10-05'),
ex as (select distinct client_id from firemap_events where ts >= '2026-10-01 00:00+09'
  and (props ? 'bot' or props ? 'internal' or props->>'host' ~* '(localhost|127\.0\.0\.1|pages\.dev|github\.io)')),
burst as (select distinct a.client_id from allss a where a.src is not null
  and (select count(distinct b.client_id) from allss b where b.src=a.src
       and b.ts between a.ts - interval '60 seconds' and a.ts + interval '60 seconds') >= 3
  and not exists (select 1 from firemap_events e where e.client_id=a.client_id
       and e.event not in ('session_start','screen_view')))
select coalesce(camp,'(캠페인 없음)') campaign,
  count(distinct client_id) filter (where client_id not in (select client_id from ex) and client_id not in (select client_id from burst)) people,
  count(distinct client_id) filter (where client_id in (select client_id from burst) and client_id not in (select client_id from ex)) burst_removed,
  count(distinct client_id) filter (where client_id in (select client_id from ex)) internal_removed
from allss where src ilike 'youtube%'
group by 1 order by 2 desc, 3 desc;
