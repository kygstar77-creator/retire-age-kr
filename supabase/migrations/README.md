# 마이그레이션 규칙

## 2026-10-30부터: public 새 테이블은 GRANT를 같은 마이그레이션에

- **배경:** 2026-10-21 Supabase가 보낸 안내 메일 "Final notice: new tables in "public" need grants from October 30"
  - 10/30부터 public 스키마에 새로 만드는 테이블은 Data API(supabase-js·PostgREST·GraphQL) 권한이 자동으로 붙지 않는다.
  - GRANT가 없으면 API가 "permission denied"를 낸다.
  - 이미 있는 테이블은 영향 없다.
- **할 일:** `create table public.x` 하는 마이그레이션에 아래를 함께 넣는다.
  - 필요한 grant
  - RLS 켜기와 정책
- **예시:**

```sql
grant select on public.x to anon, authenticated;            -- 읽기만 공개
grant insert, update, delete on public.x to authenticated;  -- 쓰기가 필요할 때만
grant all on public.x to service_role;
alter table public.x enable row level security;
```

- **범위:** 파이어맵 프로젝트(cvhskxdwqubmshdgkzhj)만 다룬다. 스꾸 프로젝트는 손대지 않는다.
