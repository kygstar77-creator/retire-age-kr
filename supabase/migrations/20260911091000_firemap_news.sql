-- 소식 테이블: 카페봇(자동, kind='auto')과 사람이 쓴 소식(kind='human')을 한 곳에.
-- 읽기: anon/authenticated SELECT. 쓰기: service_role만(Worker·운영자). anon INSERT 정책 없음 = 막힘.
-- 프로젝트 cvhskxdwqubmshdgkzhj (파이어맵 전용).

create table if not exists public.firemap_news (
  id          bigserial primary key,
  title       text not null,
  body        text,
  url         text,
  source      text,
  category    text default 'news',
  kind        text not null default 'human',
  created_at  timestamptz default now()
);

create index if not exists firemap_news_created_idx on public.firemap_news (created_at desc);
create index if not exists firemap_news_category_idx on public.firemap_news (category, created_at desc);

alter table public.firemap_news enable row level security;

drop policy if exists firemap_news_anon_read on public.firemap_news;
create policy firemap_news_anon_read
  on public.firemap_news for select
  to anon, authenticated
  using (true);

-- INSERT/UPDATE/DELETE 정책은 만들지 않는다 → RLS를 우회하는 service_role만 쓸 수 있다.
revoke all on public.firemap_news from anon, authenticated;
grant select on public.firemap_news to anon, authenticated;
grant all on public.firemap_news to service_role;
grant usage, select on sequence public.firemap_news_id_seq to service_role;

notify pgrst, 'reload schema';
