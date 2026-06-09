create table if not exists public.firemap_scores (
  id uuid primary key default gen_random_uuid(),
  fire_score smallint not null check (fire_score between 0 and 100),
  age_band smallint check (age_band between 10 and 100),
  survival_age smallint check (survival_age between 0 and 130),
  client_type text not null default 'unknown',
  created_at timestamptz not null default now()
);

alter table public.firemap_scores enable row level security;

drop policy if exists firemap_scores_read on public.firemap_scores;
create policy firemap_scores_read
  on public.firemap_scores for select to anon, authenticated using (true);

drop policy if exists firemap_scores_insert_anon on public.firemap_scores;
create policy firemap_scores_insert_anon
  on public.firemap_scores for insert to anon, authenticated
  with check (
    fire_score between 0 and 100
    and (age_band is null or age_band between 10 and 100)
    and (survival_age is null or survival_age between 0 and 130)
  );

create index if not exists firemap_scores_score_idx on public.firemap_scores (fire_score desc);
create index if not exists firemap_scores_band_score_idx on public.firemap_scores (age_band, fire_score desc);
create index if not exists firemap_scores_created_idx on public.firemap_scores (created_at desc);
