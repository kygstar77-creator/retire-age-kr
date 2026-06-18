-- Phase 2: 거시 지표(금리·물가) 추가전용 테이블 + 읽기 RPC. 적용 완료(project cvhskxdwqubmshdgkzhj).
create table if not exists public.firemap_rates (
  key text primary key, label text, value numeric not null, unit text default '%',
  as_of text, source text, updated_at timestamptz default now()
);
create table if not exists public.firemap_cpi (
  period text primary key, region text default 'KR', index numeric, yoy numeric,
  source text, updated_at timestamptz default now()
);
alter table public.firemap_rates enable row level security;
alter table public.firemap_cpi  enable row level security;
-- anon select policy: rates_anon_read / cpi_anon_read
-- RPC: fm_macro_latest() returns {rates, cpi} (cpi는 seed보다 실수집 소스 우선)
-- pg_cron: 'firemap-macro-weekly' (0 23 * * 1) -> fetch-macro Edge Function (anon bearer)
