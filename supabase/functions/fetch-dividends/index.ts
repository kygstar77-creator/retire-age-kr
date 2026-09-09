// fetch-dividends — 파이어맵 미국 ETF 배당락 수집기.
// Yahoo Finance chart API(events=div)에서 과거 2년 배당락·배당금을 받아 firemap_dividends에 upsert(kind='actual').
// 최근 배당락 간격 패턴을 반복해 다음 4회를 kind='expected'로 저장(앱은 항상 "예상"으로 표기).
// 안전 원칙: 심볼별 try/catch(부분 실패가 다른 심볼을 막지 않음), 빈 결과로는 절대 덮어쓰지 않음, 쓰기는 service_role.

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const TABLE = "firemap_dividends";

const SYMBOLS = ["SCHD", "JEPI", "JEPQ", "VYM", "O", "VTI", "QQQ"];
const EXPECTED_COUNT = 4;
const DAY_MS = 86400000;

type DivRow = { symbol: string; ex_date: string; amount: number | null; kind: "actual" | "expected"; updated_at: string };

const isoDate = (ms: number) => new Date(ms).toISOString().slice(0, 10);
const round4 = (v: number) => Math.round(v * 10000) / 10000;

async function fetchDividends(sym: string): Promise<{ date: number; amount: number }[]> {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(sym)}?range=2y&interval=1d&events=div`;
  const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (firemap-fetch-dividends)" } });
  if (!res.ok) throw new Error(`yahoo ${sym} ${res.status}`);
  const j = await res.json();
  const evs = j?.chart?.result?.[0]?.events?.dividends ?? {};
  const seen = new Map<string, { date: number; amount: number }>();
  for (const v of Object.values(evs as Record<string, { date?: number; amount?: number }>)) {
    const d = Number(v?.date), a = Number(v?.amount);
    if (!isFinite(d) || d <= 0 || !isFinite(a) || a <= 0) continue;
    const ms = d * 1000;
    seen.set(isoDate(ms), { date: ms, amount: round4(a) }); // 같은 날 중복은 마지막 값
  }
  return [...seen.values()].sort((x, y) => x.date - y.date);
}

// 최근 배당락 간격(일)의 중앙값을 반복 — 분기(≈91일)·월(≈30일) 패턴을 그대로 이어감
function deriveExpected(sym: string, actual: { date: number; amount: number }[], now: string): DivRow[] {
  if (actual.length < 2) return [];
  const gaps: number[] = [];
  for (let i = Math.max(1, actual.length - 5); i < actual.length; i++) {
    const g = Math.round((actual[i].date - actual[i - 1].date) / DAY_MS);
    if (g >= 7 && g <= 400) gaps.push(g);
  }
  if (gaps.length === 0) return [];
  gaps.sort((a, b) => a - b);
  const interval = gaps[Math.floor(gaps.length / 2)];
  const last = actual[actual.length - 1];
  const today = Date.now();
  const rows: DivRow[] = [];
  for (let k = 1; rows.length < EXPECTED_COUNT && k <= EXPECTED_COUNT + 12; k++) {
    const ms = last.date + k * interval * DAY_MS;
    if (ms <= today) continue;
    rows.push({ symbol: sym, ex_date: isoDate(ms), amount: last.amount, kind: "expected", updated_at: now });
  }
  return rows;
}

async function upsertRows(rows: DivRow[]) {
  if (rows.length === 0) return;
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?on_conflict=symbol,ex_date,kind`, {
    method: "POST",
    headers: {
      apikey: SERVICE_KEY,
      authorization: `Bearer ${SERVICE_KEY}`,
      "content-type": "application/json",
      prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify(rows),
  });
  if (!res.ok) throw new Error(`upsert ${rows[0].symbol} ${res.status} ${await res.text()}`);
}

// 새 예상치가 있을 때만 이전 예상 행을 지움(빈 결과로 덮어쓰지 않음)
async function deleteExpected(sym: string) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?symbol=eq.${encodeURIComponent(sym)}&kind=eq.expected`, {
    method: "DELETE",
    headers: { apikey: SERVICE_KEY, authorization: `Bearer ${SERVICE_KEY}`, prefer: "return=minimal" },
  });
  if (!res.ok) throw new Error(`delete expected ${sym} ${res.status} ${await res.text()}`);
}

Deno.serve(async (_req: Request) => {
  const now = new Date().toISOString();
  const updated: Record<string, { actual: number; expected: number }> = {};
  const skipped: Record<string, string> = {};

  for (const sym of SYMBOLS) {
    try {
      const actual = await fetchDividends(sym);
      if (actual.length === 0) { skipped[sym] = "no dividends"; continue; }
      const actualRows: DivRow[] = actual.map((d) => ({ symbol: sym, ex_date: isoDate(d.date), amount: d.amount, kind: "actual", updated_at: now }));
      await upsertRows(actualRows);
      const expected = deriveExpected(sym, actual, now);
      if (expected.length > 0) {
        await deleteExpected(sym);
        await upsertRows(expected);
      }
      updated[sym] = { actual: actualRows.length, expected: expected.length };
    } catch (e) {
      skipped[sym] = String((e as Error)?.message || e);
    }
  }

  return new Response(JSON.stringify({ ok: true, at: now, updated, skipped }), {
    headers: { "content-type": "application/json" },
  });
});
