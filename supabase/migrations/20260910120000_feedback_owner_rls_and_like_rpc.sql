-- 0주차 보안: firemap_feedback를 anon 키로 아무나 수정·삭제하던 구멍을 막는다.
--  · 좋아요 = fm_like (원자 증가)  · 수정 = fm_edit(작성자 검증)  · 삭제 = fm_delete(작성자 검증, 답글 포함)
--  · 그 뒤 anon의 직접 UPDATE/DELETE 권한을 회수한다.
-- ⚠ 적용 시점: dev 코드(RPC 호출)가 main에 병합된 뒤. 지금 main은 직접 PATCH/DELETE를 쓰므로 먼저 적용하면
--   운영의 글 수정·삭제·좋아요가 실패한다. 파일만 레포에 두고, 병합과 같은 날 `supabase db push`.

create or replace function public.fm_like(p_id bigint)
returns integer
language sql
security definer
set search_path = public
as $$
  update public.firemap_feedback
     set likes = coalesce(likes, 0) + 1
   where id = p_id and status = 'visible'
  returning likes;
$$;
grant execute on function public.fm_like(bigint) to anon, authenticated;

create or replace function public.fm_edit(p_id bigint, p_cid text, p_message text)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare n integer;
begin
  if p_cid is null or length(trim(p_message)) = 0 then return false; end if;
  update public.firemap_feedback
     set message = left(trim(p_message), 240)
   where id = p_id and client_id = p_cid and status = 'visible';
  get diagnostics n = row_count;
  return n > 0;
end;
$$;
grant execute on function public.fm_edit(bigint, text, text) to anon, authenticated;

create or replace function public.fm_delete(p_id bigint, p_cid text)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare n integer;
begin
  if p_cid is null then return false; end if;
  delete from public.firemap_feedback
   where (id = p_id or parent_id = p_id)
     and exists (select 1 from public.firemap_feedback f where f.id = p_id and f.client_id = p_cid);
  get diagnostics n = row_count;
  return n > 0;
end;
$$;
grant execute on function public.fm_delete(bigint, text) to anon, authenticated;

-- 직접 UPDATE/DELETE 회수 (INSERT/SELECT는 유지)
revoke update, delete on public.firemap_feedback from anon;
revoke update, delete on public.firemap_feedback from authenticated;
alter table public.firemap_feedback enable row level security;
drop policy if exists "feedback anon update" on public.firemap_feedback;
drop policy if exists "feedback anon delete" on public.firemap_feedback;

-- firemap_scores: advanced_days PATCH도 RPC로 (client_id 검증)
create or replace function public.fm_score_advance(p_cids text[], p_adv numeric)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare n integer;
begin
  update public.firemap_scores set advanced_days = p_adv where client_id = any(p_cids);
  get diagnostics n = row_count;
  return n;
end;
$$;
grant execute on function public.fm_score_advance(text[], numeric) to anon, authenticated;

-- 집계 RPC: 2,000행 다운로드 대신 서버 집계
create or replace function public.fm_aggregates(p_band integer default null)
returns table(total bigint, avg_earliest numeric, avg_score numeric)
language sql
stable
security definer
set search_path = public
as $$
  select count(*)::bigint as total,
         round(avg(earliest_age) filter (where earliest_age is not null and earliest_age > 0), 0) as avg_earliest,
         round(avg(fire_score), 0) as avg_score
    from public.firemap_scores
   where (p_band is null or age_band = p_band);
$$;
grant execute on function public.fm_aggregates(integer) to anon, authenticated;
