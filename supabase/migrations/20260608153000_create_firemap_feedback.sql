create table if not exists public.firemap_feedback (
  id uuid primary key default gen_random_uuid(),
  message text not null check (char_length(message) between 1 and 240),
  nickname text not null default '익명',
  page_path text,
  client_type text not null default 'unknown',
  status text not null default 'visible',
  created_at timestamptz not null default now()
);

alter table public.firemap_feedback enable row level security;

drop policy if exists firemap_feedback_read_visible on public.firemap_feedback;
create policy firemap_feedback_read_visible
  on public.firemap_feedback
  for select
  to anon, authenticated
  using (status = 'visible');

drop policy if exists firemap_feedback_insert_anon on public.firemap_feedback;
create policy firemap_feedback_insert_anon
  on public.firemap_feedback
  for insert
  to anon, authenticated
  with check (
    status = 'visible'
    and nickname = '익명'
    and char_length(message) between 1 and 240
  );

create index if not exists firemap_feedback_created_idx on public.firemap_feedback (created_at desc);
create index if not exists firemap_feedback_status_created_idx on public.firemap_feedback (status, created_at desc);
