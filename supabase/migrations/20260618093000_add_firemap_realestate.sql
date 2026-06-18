-- 추가전용: 부동산 실거래가 테이블 + 최신 조회 RPC. 기존 테이블/RPC 변경 없음.
create table if not exists public.firemap_realestate (
  id bigint generated always as identity primary key,
  region text not null,
  deal_type text not null default 'sale',
  metric text not null default 'avg_price',
  value numeric,
  unit text default '만원',
  period text,
  source text,
  updated_at timestamptz default now(),
  unique (region, deal_type, metric, period)
);
alter table public.firemap_realestate enable row level security;
create or replace function public.fm_realestate_latest()
returns json language sql stable security definer set search_path to 'public'
as $$
  select coalesce(json_agg(t order by t.region, t.deal_type), '[]'::json)
  from (
    select distinct on (region, deal_type, metric) region, deal_type, metric, value, unit, period, source, updated_at
    from public.firemap_realestate
    order by region, deal_type, metric, period desc
  ) t;
$$;
grant execute on function public.fm_realestate_latest() to anon, authenticated;
