-- 파이어맵 하루 외부 유입 집계 (firemap-growth, 2026-10-05). Supabase c7cd8a90 execute_sql에 붙여 쓴다.
-- 날짜만 바꾼다: :day = '2026-10-05'
-- 거름 1: 10/1 이후 bot·internal·로컬/pages.dev/github.io 기록이 한 번이라도 있는 기기는 통째로 뺀다.
-- 거름 2(10/5 추가, 링크 미리보기 몰림): utm이 붙은 첫 진입인데 ±60초 안에 같은 utm_source 새 기기가 3대 이상이고,
--   그 기기가 화면 1개(session_start·screen_view) 말고 아무 행동이 없으면 뺀다.
--   근거: 10/5 12:46 youtube 19대 = youtube-loop 12:49 커밋(쇼츠 6편 설명에 utm) 직후, 04:40 3대 = 04:42 VIDEOID 치환.
--   10초 창은 04:40(14초 간격)을 놓쳐서 60초로 넓혔다. 계산·클릭을 한 기기는 몰림 안이어도 사람으로 남긴다.
with allss as (
  select client_id, ts, props->>'utm_source' src from firemap_events
  where event='session_start' and (ts at time zone 'Asia/Seoul')::date = date '2026-10-05'),
ex as (select distinct client_id from firemap_events where ts >= '2026-10-01 00:00+09'
  and (props ? 'bot' or props ? 'internal' or props->>'host' ~* '(localhost|127\.0\.0\.1|pages\.dev|github\.io)')),
burst as (select distinct a.client_id from allss a where a.src is not null
  and (select count(distinct b.client_id) from allss b where b.src=a.src
       and b.ts between a.ts - interval '60 seconds' and a.ts + interval '60 seconds') >= 3
  and not exists (select 1 from firemap_events e where e.client_id=a.client_id
       and e.event not in ('session_start','screen_view'))),
keep as (select distinct client_id from allss
  where client_id not in (select client_id from ex) and client_id not in (select client_id from burst))
select event, count(*) n, count(distinct client_id) dev
from firemap_events where (ts at time zone 'Asia/Seoul')::date = date '2026-10-05' and client_id in (select client_id from keep)
group by event
union all select '_몰림_뺀_기기(봇 제외)', count(*), 0 from burst where client_id not in (select client_id from ex)
union all
select 'src:'||coalesce(props->>'utm_source','기록없음'), count(*), count(distinct client_id)
from firemap_events where event='session_start' and (ts at time zone 'Asia/Seoul')::date = date '2026-10-05'
  and client_id in (select client_id from keep) group by 1
order by 1;
