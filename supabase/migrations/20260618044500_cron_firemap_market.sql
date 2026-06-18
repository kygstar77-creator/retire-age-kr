-- Daily market refresh via pg_cron -> pg_net -> fetch-market Edge Function.
-- pg_cron & pg_net already installed. Additive (schedules a job; no data mutation of app tables).
-- Note: Authorization Bearer uses the project anon key (redacted here; set the real key when re-applying).
select cron.schedule(
  'firemap-market-daily',
  '0 22 * * *',
  $$ select net.http_post(
       url := 'https://cvhskxdwqubmshdgkzhj.supabase.co/functions/v1/fetch-market',
       headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer <ANON_KEY>'),
       body := '{}'::jsonb
     ) $$
);
