-- 추가전용: 미국 ETF 배당락 테이블(실제 actual + 예상 expected). 기존 테이블/RPC 변경 없음.
-- 쓰기는 fetch-dividends Edge Function(service_role)만, 읽기는 anon/authenticated select.
create table if not exists public.firemap_dividends (
  symbol text not null,
  ex_date date not null,
  amount numeric,
  kind text not null default 'actual',
  updated_at timestamptz default now(),
  primary key (symbol, ex_date, kind)
);
alter table public.firemap_dividends enable row level security;
drop policy if exists "firemap_dividends_select" on public.firemap_dividends;
create policy "firemap_dividends_select" on public.firemap_dividends
  for select to anon, authenticated using (true);
grant select on public.firemap_dividends to anon, authenticated;

NOTIFY pgrst, 'reload schema';

-- Weekly dividend refresh via pg_cron -> pg_net -> fetch-dividends Edge Function.
-- Monday 09:00 KST = Monday 00:00 UTC. pg_cron & pg_net already installed. Additive (schedules a job; no data mutation of app tables).
-- Note: Authorization Bearer uses the project anon key (redacted here; set the real key when re-applying).
select cron.schedule(
  'firemap-dividends-weekly',
  '0 0 * * 1',
  $$ select net.http_post(
       url := 'https://cvhskxdwqubmshdgkzhj.supabase.co/functions/v1/fetch-dividends',
       headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer <ANON_KEY>'),
       body := '{}'::jsonb
     ) $$
);
