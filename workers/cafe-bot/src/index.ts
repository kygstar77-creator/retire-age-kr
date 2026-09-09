// 파이어맵 카페봇 — cron으로 지표·랭킹·인증 모음 글을 만들어 firemap_news(kind='auto')에 넣고,
// 네이버 카페 토큰이 있으면 카페 '소식' 게시판에도 올려요. 하루 2개 초과 금지(KV 가드).
// 비밀값은 env로만. 코드에 URL·키를 적지 않는다.

export interface Env {
  SUPABASE_URL: string;
  SUPABASE_SERVICE_KEY: string;
  NAVER_CAFE_TOKEN?: string;
  NAVER_CLUB_ID?: string;
  NAVER_MENU_ID_NEWS?: string;
  CAFEBOT_KV: KVNamespace;
  APP_URL?: string;
  CAFE_URL?: string;
}

type Job = 'market' | 'ranking' | 'certs';
const JOB_OF_CRON: Record<string, Job> = {
  '0 22 * * *': 'market',
  '0 9 * * 5': 'ranking',
  '0 0 1 * *': 'certs',
};
const MAX_POSTS_PER_DAY = 2;

// ---------- 날짜(KST) ----------
const kstNow = () => new Date(Date.now() + 9 * 3600 * 1000);
const kstDateKey = () => kstNow().toISOString().slice(0, 10); // YYYY-MM-DD
const kstLabel = () => { const d = kstNow(); return `${d.getUTCMonth() + 1}월 ${d.getUTCDate()}일`; };
const isoDaysAgo = (n: number) => new Date(Date.now() - n * 86400000).toISOString();

// ---------- 포맷 ----------
const num0 = (v: unknown) => Math.round(Number(v)).toLocaleString('ko-KR');
const pct1 = (v: unknown) => (v == null || Number.isNaN(Number(v)) ? null : `${Number(v) > 0 ? '+' : ''}${Number(v).toFixed(1)}%`);
const stripTrailingZero = (s: string) => s.replace(/\.?0+$/, '');

// ---------- Supabase REST ----------
function sbHeaders(env: Env, extra: Record<string, string> = {}) {
  return { apikey: env.SUPABASE_SERVICE_KEY, authorization: `Bearer ${env.SUPABASE_SERVICE_KEY}`, 'content-type': 'application/json', ...extra };
}
async function sbRpc<T = unknown>(env: Env, fn: string, args: Record<string, unknown> = {}): Promise<T | null> {
  try {
    const res = await fetch(`${env.SUPABASE_URL}/rest/v1/rpc/${fn}`, { method: 'POST', headers: sbHeaders(env), body: JSON.stringify(args) });
    if (!res.ok) { console.log(`rpc ${fn} ${res.status}`); return null; }
    const txt = await res.text();
    return txt ? (JSON.parse(txt) as T) : null;
  } catch (e) { console.log(`rpc ${fn} error`, String(e)); return null; }
}
async function sbGet<T = unknown>(env: Env, pathAndQuery: string): Promise<T | null> {
  try {
    const res = await fetch(`${env.SUPABASE_URL}/rest/v1/${pathAndQuery}`, { headers: sbHeaders(env) });
    if (!res.ok) { console.log(`get ${pathAndQuery.split('?')[0]} ${res.status}`); return null; }
    return (await res.json()) as T;
  } catch (e) { console.log('get error', String(e)); return null; }
}
async function sbCount(env: Env, pathAndQuery: string): Promise<number | null> {
  try {
    const res = await fetch(`${env.SUPABASE_URL}/rest/v1/${pathAndQuery}`, { method: 'HEAD', headers: sbHeaders(env, { prefer: 'count=exact' }) });
    if (!res.ok) return null;
    const cr = res.headers.get('content-range') || '';
    const total = cr.split('/')[1];
    return total && total !== '*' ? Number(total) : null;
  } catch { return null; }
}

// ---------- 글 조립(해요체) ----------
interface Post { title: string; body: string; category: string; }
interface MarketRow { symbol: string; level: number | null; ret_1d: number | null; ret_7d: number | null; ret_30d?: number | null; updated_at?: string; }
interface Macro { rates?: { key: string; value: number; as_of?: string }[]; cpi?: { period?: string; yoy?: number | null } | null; }

async function buildMarketPost(env: Env): Promise<Post | null> {
  const [market, macro] = await Promise.all([sbRpc<MarketRow[]>(env, 'fm_market_latest'), sbRpc<Macro>(env, 'fm_macro_latest')]);
  const rows = Array.isArray(market) ? market : [];
  const find = (s: string) => rows.find((r) => r.symbol === s);
  const lines: string[] = [];
  const line = (label: string, r: MarketRow | undefined, unit = '') => {
    if (!r || r.level == null) return;
    const d = pct1(r.ret_1d) ?? pct1(r.ret_7d);
    const when = r.ret_1d != null ? '어제보다' : '이번 주';
    lines.push(`${label} ${num0(r.level)}${unit}${d ? ` · ${when} ${d}` : ''}`);
  };
  line('코스피', find('^kospi'));
  line('S&P500', find('^spx'));
  line('환율 1달러', find('usdkrw'), '원');
  const base = macro?.rates?.find((x) => x.key === 'base_rate');
  if (base && base.value != null) lines.push(`기준금리 ${stripTrailingZero(Number(base.value).toFixed(2))}%`);
  const cpi = macro?.cpi;
  if (cpi && cpi.yoy != null) lines.push(`물가 1년 전보다 ${Number(cpi.yoy).toFixed(1)}%`);
  if (lines.length === 0) return null;
  const body = [
    `${kstLabel()} 아침 지표예요.`,
    '',
    ...lines.map((l) => `· ${l}`),
    '',
    '지표는 참고만 해요. 내 파이어 나이엔 영향 없어요.',
    `내 파이어 나이 계산하기 → ${env.APP_URL || 'https://firemap.kr'}`,
  ].join('\n');
  return { title: `[자동] ${kstLabel()} 아침 지표 · 코스피 ${find('^kospi')?.level != null ? num0(find('^kospi')!.level) : '—'}`, body, category: 'news' };
}

interface ScoreRow { earliest_age: number | null; age_band: number | null; }
async function buildRankingPost(env: Env): Promise<Post | null> {
  const since = isoDaysAgo(7);
  const rows = await sbGet<ScoreRow[]>(env, `firemap_scores?select=earliest_age,age_band&created_at=gte.${encodeURIComponent(since)}&earliest_age=not.is.null&order=earliest_age.asc&limit=2000`);
  const total = await sbCount(env, 'firemap_scores?select=id');
  const list = Array.isArray(rows) ? rows.filter((r) => r.earliest_age != null) : [];
  if (list.length === 0 && !total) return null;
  const ages = list.map((r) => Number(r.earliest_age)).filter((n) => n > 0);
  const avg = ages.length ? Math.round(ages.reduce((a, b) => a + b, 0) / ages.length) : null;
  const best = ages.length ? Math.min(...ages) : null;
  const median = ages.length ? ages.slice().sort((a, b) => a - b)[Math.floor(ages.length / 2)] : null;
  const bands: Record<string, number[]> = {};
  for (const r of list) { if (r.age_band == null) continue; (bands[String(r.age_band)] ||= []).push(Number(r.earliest_age)); }
  const bandLines = Object.keys(bands).sort().map((b) => { const a = bands[b]; return `· ${b}대 ${a.length}명 · 평균 ${Math.round(a.reduce((x, y) => x + y, 0) / a.length)}세`; });
  const body = [
    `이번 주 파이어맵 랭킹이에요.`,
    '',
    `· 이번 주 계산한 사람 ${ages.length.toLocaleString('ko-KR')}명${total ? ` · 지금까지 ${total.toLocaleString('ko-KR')}명` : ''}`,
    avg != null ? `· 이번 주 평균 파이어 나이 ${avg}세 · 중간값 ${median}세` : '',
    best != null ? `· 이번 주 가장 빠른 파이어 나이 ${best}세` : '',
    ...(bandLines.length ? ['', '또래별로 보면요', ...bandLines] : []),
    '',
    '순위는 직접 입력한 기록 기반이에요. 자산은 구간만 저장돼요.',
    `내 등수 보기 → ${env.APP_URL || 'https://firemap.kr'}/#ranking`,
  ].filter((l) => l !== '').join('\n');
  return { title: `[자동] 이번 주 랭킹 · ${ages.length}명 계산${avg != null ? ` · 평균 ${avg}세` : ''}`, body, category: 'ranking' };
}

interface CertRow { id: number; likes: number | null; stage: number | null; created_at: string; }
async function buildCertsPost(env: Env): Promise<Post | null> {
  const since = isoDaysAgo(31);
  const rows = await sbGet<CertRow[]>(env, `firemap_feedback?select=id,likes,stage,created_at&kind=eq.community&status=eq.visible&category=eq.goal&parent_id=is.null&created_at=gte.${encodeURIComponent(since)}&order=created_at.desc&limit=1000`);
  const list = Array.isArray(rows) ? rows : [];
  if (list.length === 0) return null;
  const likes = list.reduce((a, r) => a + (Number(r.likes) || 0), 0);
  const stages: Record<string, number> = {};
  for (const r of list) { if (r.stage != null) stages[String(r.stage)] = (stages[String(r.stage)] || 0) + 1; }
  const STAGE_NAME: Record<string, string> = { '1': '각성', '2': '설계', '3': '실행', '4': '가속', '5': '임박', '6': '파이어' };
  const stageLines = Object.keys(stages).sort().map((s) => `· ${s}단계 ${STAGE_NAME[s] || ''} ${stages[s]}명`);
  const d = kstNow();
  const prevMonth = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, 1));
  const monthLabel = `${prevMonth.getUTCMonth() + 1}월`;
  const body = [
    `${monthLabel} 한 달 동안 방명록에 올라온 파이어 인증을 모았어요.`,
    '',
    `· 인증 ${list.length.toLocaleString('ko-KR')}개 · 받은 공감 ${likes.toLocaleString('ko-KR')}개`,
    ...(stageLines.length ? ['', '여정 단계로 보면요', ...stageLines] : []),
    '',
    '인증 글 하나하나는 파이어맵 방명록에서 볼 수 있어요.',
    `방명록 보기 → ${env.APP_URL || 'https://firemap.kr'}/#wall`,
    `내 인증 카드 만들기 → ${env.APP_URL || 'https://firemap.kr'}/#result`,
  ].join('\n');
  return { title: `[자동] ${monthLabel} 인증 모음 · ${list.length}명이 파이어 나이를 인증했어요`, body, category: 'goal' };
}

// ---------- 저장·게시 ----------
async function insertNews(env: Env, post: Post, url: string | null): Promise<boolean> {
  try {
    const res = await fetch(`${env.SUPABASE_URL}/rest/v1/firemap_news`, {
      method: 'POST',
      headers: sbHeaders(env, { prefer: 'return=minimal' }),
      body: JSON.stringify({ title: post.title, body: post.body, url, source: '파이어맵 카페봇', category: post.category, kind: 'auto' }),
    });
    if (!res.ok) console.log('firemap_news insert', res.status, await res.text());
    return res.ok;
  } catch (e) { console.log('firemap_news insert error', String(e)); return false; }
}

// 네이버 카페 글쓰기 API — 토큰은 공식 카페 계정(사장님)의 것. 봇 계정 금지(README 참고).
async function postToCafe(env: Env, post: Post): Promise<string | null> {
  if (!env.NAVER_CAFE_TOKEN || !env.NAVER_CLUB_ID || !env.NAVER_MENU_ID_NEWS) { console.log('cafe: token/club/menu 없음 → 건너뜀'); return null; }
  const url = `https://openapi.naver.com/v1/cafe/${encodeURIComponent(env.NAVER_CLUB_ID)}/menu/${encodeURIComponent(env.NAVER_MENU_ID_NEWS)}/articles`;
  const content = post.body.replace(/\n/g, '<br>');
  const form = `subject=${encodeURIComponent(post.title)}&content=${encodeURIComponent(content)}`;
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { authorization: `Bearer ${env.NAVER_CAFE_TOKEN}`, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8' },
      body: form,
    });
    if (res.status === 429) { console.log('cafe: 429 요청 한도 · 이번 회차 건너뜀'); return null; }
    if (res.status === 401) { console.log('cafe: 401 토큰 만료 또는 권한 없음 · 사장님 계정으로 토큰 재발급 필요'); return null; }
    if (!res.ok) { console.log('cafe: 실패', res.status, (await res.text()).slice(0, 300)); return null; }
    const j = (await res.json().catch(() => null)) as { message?: { result?: { articleUrl?: string } } } | null;
    const articleUrl = j?.message?.result?.articleUrl || null;
    console.log('cafe: 게시 완료', articleUrl || '');
    return articleUrl;
  } catch (e) { console.log('cafe: error', String(e)); return null; }
}

// 하루 2개 가드 — KV에 날짜별 개수 + 마지막 게시일
async function canPostToday(env: Env): Promise<boolean> {
  const key = `count:${kstDateKey()}`;
  const n = Number((await env.CAFEBOT_KV.get(key)) || 0);
  return n < MAX_POSTS_PER_DAY;
}
async function markPosted(env: Env, job: Job) {
  const day = kstDateKey();
  const key = `count:${day}`;
  const n = Number((await env.CAFEBOT_KV.get(key)) || 0) + 1;
  await env.CAFEBOT_KV.put(key, String(n), { expirationTtl: 3 * 86400 });
  await env.CAFEBOT_KV.put('last_post', JSON.stringify({ date: day, job, at: new Date().toISOString() }));
}

async function runJob(env: Env, job: Job): Promise<string> {
  if (!env.SUPABASE_URL || !env.SUPABASE_SERVICE_KEY) return 'skip: SUPABASE_URL/SUPABASE_SERVICE_KEY 없음';
  if (!(await canPostToday(env))) return `skip: 오늘 이미 ${MAX_POSTS_PER_DAY}개 게시`;
  const post = job === 'market' ? await buildMarketPost(env) : job === 'ranking' ? await buildRankingPost(env) : await buildCertsPost(env);
  if (!post) return `skip: ${job} 데이터 없음 → 빈 글은 안 올려요`;
  const cafeUrl = await postToCafe(env, post);
  const saved = await insertNews(env, post, cafeUrl);
  if (saved || cafeUrl) await markPosted(env, job);
  return `${job}: news=${saved ? 'ok' : 'fail'} cafe=${cafeUrl ? 'ok' : 'skip'}`;
}

export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    const job = JOB_OF_CRON[event.cron];
    if (!job) { console.log('unknown cron', event.cron); return; }
    ctx.waitUntil(runJob(env, job).then((r) => console.log(r)));
  },
  // 상태 확인용. 게시는 cron으로만(수동 실행은 `wrangler dev --test-scheduled` 후 /__scheduled?cron=...).
  async fetch(_req: Request, env: Env) {
    const last = await env.CAFEBOT_KV.get('last_post');
    const today = await env.CAFEBOT_KV.get(`count:${kstDateKey()}`);
    return new Response(JSON.stringify({ ok: true, today: kstDateKey(), postedToday: Number(today || 0), last: last ? JSON.parse(last) : null }), { headers: { 'content-type': 'application/json' } });
  },
};
