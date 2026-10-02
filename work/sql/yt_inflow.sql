-- 유튜브·쇼츠 설명란 utm 링크 → firemap.kr 실유입 (firemap-loop 2026-10-02)
-- Supabase MCP(c7cd8a90) execute_sql로 그대로 돌린다. 테이블 firemap_events(id, client_id, event, props jsonb, ts).
-- 왜 burst를 빼나: 업로드 직후 같은 campaign에 서로 다른 client 2~3개가 1~3초 안에 들어온다(ref 없음, bot 표시 안 됨).
--   10/1 sevpay 19:26:29 2건, 10/2 e-1 06:56:46~48 3건, scV67 00:02:59~03:00 2건 — 사람이 같은 초에 여럿 누를 수 없다.
--   14일치 youtube/shorts 세션 18건 중 14건이 burst였다(78%). 이걸 빼지 않으면 '링크가 눌린다'로 잘못 판정한다.
with s as (
  select ts, client_id, props->>'utm_source' src, props->>'utm_campaign' camp
  from firemap_events
  where event = 'session_start'
    and props->>'utm_source' in ('youtube', 'shorts')
    and coalesce(props->>'bot', '0') not in ('1', 'true')
    and coalesce(props->>'internal', '0') not in ('1', 'true')
    and ts > now() - interval '14 days'),
b as (
  select s.*, exists(select 1 from s s2 where s2.camp = s.camp and s2.client_id <> s.client_id
                     and abs(extract(epoch from s2.ts - s.ts)) <= 3) burst
  from s)
select src, camp,
       count(distinct client_id) filter (where not burst) real_clients,
       count(*) filter (where not burst) real_sessions,
       count(*) filter (where burst) burst_sessions
from b group by 1, 2 order by real_clients desc;
