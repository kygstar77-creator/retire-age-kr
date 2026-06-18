// fetch-market — 파이어맵 시장 데이터 수집기 (Phase 1)
// 무료/공개 소스(Yahoo Finance chart API, open.er-api.com)에서 지수·환율을 받아 firemap_market에 추가전용 upsert.
// 안전 원칙: 심볼별 개별 upsert(부분 실패가 기존 행을 덮지 않음), 값 검증 실패 시 건너뜀(기존 값 유지). 입력 미신뢰(고정 소스만). 쓰기는 service_role.

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

// db symbol(앱이 읽는 키)  <-  yahoo 심볼
const SYMBOLS = [
  { symbol: "^spx", ysym: "^GSPC", name: "S&P 500", asset_class: "index", currency: "USD" },
  { symbol: "^ndq", ysym: "^IXIC", name: "Nasdaq Composite", asset_class: "index", currency: "USD" },
  { symbol: "^kospi", ysym: "^KS11", name: "KOSPI", asset_class: "index", currency: "KRW" },
  { symbol: "usdkrw", ysym: "KRW=X", name: "USD/KRW", asset_class: "fx", currency: "KRW" },
];

const round2 = (v: number) => Math.round(v * 100) / 100;
const pct = (a: number, b: number) => (b > 0 && isFinite(a) && isFinite(b) ? round2((a / b - 1) * 100) : null);

async function fetchSeries(ysym: string): Promise<{ closes: number[]; ts: number[] }> {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(ysym)}?range=1y&interval=1d`;
  const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (firemap-fetch-market)" } });
  if (!res.ok) throw new Error(`yahoo ${ysym} ${res.status}`);
  const j = await res.json();
  const r = j?.chart?.result?.[0];
  const rawC: (number | null)[] = r?.indicators?.quote?.[0]?.close ?? [];
  const rawT: number[] = r?.timestamp ?? [];
  const closes: number[] = []; const ts: number[] = [];
  for (let i = 0; i < rawC.length; i++) {
    const c = rawC[i];
    if (typeof c === "number" && isFinite(c) && c > 0) { closes.push(c); ts.push(rawT[i]); }
  }
  if (closes.length < 1) throw new Error(`yahoo ${ysym} no closes`);
  return { closes, ts };
}

async function fxUsdKrwFallback(): Promise<number | null> {
  try {
    const r = await fetch("https://open.er-api.com/v6/latest/USD");
    const j = await r.json();
    const v = j?.rates?.KRW;
    return typeof v === "number" && v > 0 ? round2(v) : null;
  } catch { return null; }
}

async function upsertOne(row: Record<string, unknown>) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/firemap_market?on_conflict=symbol`, {
    method: "POST",
    headers: {
      apikey: SERVICE_KEY,
      authorization: `Bearer ${SERVICE_KEY}`,
      "content-type": "application/json",
      prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify(row),
  });
  if (!res.ok) throw new Error(`upsert ${row.symbol} ${res.status} ${await res.text()}`);
}

Deno.serve(async (_req: Request) => {
  const now = new Date().toISOString();
  const year = new Date().getUTCFullYear();
  const updated: string[] = [];
  const skipped: Record<string, string> = {};

  for (const meta of SYMBOLS) {
    try {
      let level: number | null = null;
      let ret_1d: number | null = null, ret_7d: number | null = null, ret_30d: number | null = null, ret_ytd: number | null = null;
      let source = "yahoo";
      try {
        const { closes, ts } = await fetchSeries(meta.ysym);
        const n = closes.length;
        const last = closes[n - 1];
        const back = (k: number) => (n - 1 - k >= 0 ? closes[n - 1 - k] : NaN);
        level = round2(last);
        ret_1d = pct(last, back(1));
        ret_7d = pct(last, back(5));
        ret_30d = pct(last, back(21));
        let ytdBase = NaN;
        for (let i = 0; i < ts.length; i++) { if (new Date(ts[i] * 1000).getUTCFullYear() === year) { ytdBase = closes[i]; break; } }
        ret_ytd = pct(last, ytdBase);
      } catch (e) {
        if (meta.asset_class === "fx") {
          const fx = await fxUsdKrwFallback();
          if (fx != null) { level = fx; source = "open.er-api.com"; }
          else throw e;
        } else { throw e; }
      }
      if (level == null || !(level > 0)) { skipped[meta.symbol] = "no level"; continue; }

      const row: Record<string, unknown> = {
        symbol: meta.symbol, name: meta.name, asset_class: meta.asset_class, currency: meta.currency,
        level, source, updated_at: now,
      };
      if (ret_1d != null) row.ret_1d = ret_1d;
      if (ret_7d != null) row.ret_7d = ret_7d;
      if (ret_30d != null) row.ret_30d = ret_30d;
      if (ret_ytd != null) row.ret_ytd = ret_ytd;

      await upsertOne(row);
      updated.push(meta.symbol);
    } catch (e) {
      skipped[meta.symbol] = String((e as Error)?.message || e);
    }
  }

  return new Response(JSON.stringify({ ok: true, at: now, updated, skipped }), {
    headers: { "content-type": "application/json" },
  });
});
