// fetch-market — 파이어맵 시장 데이터 수집기 (Phase 1)
// 무료/공개 소스(Yahoo Finance chart API, open.er-api.com)에서 지수·환율을 받아 firemap_market에 추가전용 upsert.
// 안전 원칙: 심볼별 개별 upsert(부분 실패가 기존 행을 덮지 않음), 값 검증 실패 시 건너뜀(기존 값 유지). 입력 미신뢰(고정 소스만). 쓰기는 service_role.
// 폴백(조사로 확인): S&P500은 FRED csv(SP500), KOSPI는 네이버 모바일 증권 JSON. 둘 다 실패하면 그 심볼만 건너뛰고 빈 값은 절대 쓰지 않음.

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

type Series = { closes: number[]; ts: number[] };
type Quote = { level: number; ret_1d: number | null };

async function fetchSeries(ysym: string): Promise<Series> {
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

// 폴백 1: FRED csv — S&P500 종가 일별 시계열. 값이 '.'이면 휴장(건너뜀). 최근 1년만 사용.
async function fredSp500Series(): Promise<Series> {
  const res = await fetch("https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500", { headers: { "User-Agent": "Mozilla/5.0 (firemap-fetch-market)" } });
  if (!res.ok) throw new Error(`fred SP500 ${res.status}`);
  const text = await res.text();
  const lines = text.trim().split(/\r?\n/);
  const closes: number[] = []; const ts: number[] = [];
  const cutoff = Date.now() / 1000 - 370 * 86400;
  for (let i = 1; i < lines.length; i++) {
    const [d, v] = lines[i].split(",");
    if (!d || v == null || v.trim() === ".") continue;
    const n = Number(v);
    const t = Date.parse(`${d.trim()}T00:00:00Z`) / 1000;
    if (!isFinite(n) || n <= 0 || !isFinite(t) || t < cutoff) continue;
    closes.push(n); ts.push(t);
  }
  if (closes.length < 1) throw new Error("fred SP500 no closes");
  return { closes, ts };
}

// 폴백 2: 네이버 모바일 증권 — KOSPI 현재가·전일 대비 등락률만(시계열 없음 → 1d만 기록).
async function naverKospiQuote(): Promise<Quote> {
  const res = await fetch("https://m.stock.naver.com/api/index/KOSPI/basic", { headers: { "User-Agent": "Mozilla/5.0 (firemap-fetch-market)", accept: "application/json" } });
  if (!res.ok) throw new Error(`naver KOSPI ${res.status}`);
  const j = await res.json();
  const level = Number(String(j?.closePrice ?? "").replace(/,/g, ""));
  if (!isFinite(level) || level <= 0) throw new Error("naver KOSPI no closePrice");
  const ratio = Number(String(j?.fluctuationsRatio ?? "").replace(/,/g, ""));
  return { level: round2(level), ret_1d: isFinite(ratio) ? round2(ratio) : null };
}

async function fxUsdKrwFallback(): Promise<number | null> {
  try {
    const r = await fetch("https://open.er-api.com/v6/latest/USD");
    const j = await r.json();
    const v = j?.rates?.KRW;
    return typeof v === "number" && v > 0 ? round2(v) : null;
  } catch { return null; }
}

function statsFromSeries({ closes, ts }: Series, year: number) {
  const n = closes.length;
  const last = closes[n - 1];
  const back = (k: number) => (n - 1 - k >= 0 ? closes[n - 1 - k] : NaN);
  let ytdBase = NaN;
  for (let i = 0; i < ts.length; i++) { if (new Date(ts[i] * 1000).getUTCFullYear() === year) { ytdBase = closes[i]; break; } }
  return {
    level: round2(last),
    ret_1d: pct(last, back(1)),
    ret_7d: pct(last, back(5)),
    ret_30d: pct(last, back(21)),
    ret_ytd: pct(last, ytdBase),
  };
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
        const s = statsFromSeries(await fetchSeries(meta.ysym), year);
        level = s.level; ret_1d = s.ret_1d; ret_7d = s.ret_7d; ret_30d = s.ret_30d; ret_ytd = s.ret_ytd;
      } catch (e) {
        // 심볼별 폴백 — 폴백도 실패하면 원래 에러를 던져 이 심볼만 건너뜀(기존 행 유지)
        if (meta.ysym === "^GSPC") {
          try {
            const s = statsFromSeries(await fredSp500Series(), year);
            level = s.level; ret_1d = s.ret_1d; ret_7d = s.ret_7d; ret_30d = s.ret_30d; ret_ytd = s.ret_ytd;
            source = "fred";
          } catch (e2) { throw new Error(`${String((e as Error)?.message || e)} / ${String((e2 as Error)?.message || e2)}`); }
        } else if (meta.ysym === "^KS11") {
          try {
            const q = await naverKospiQuote();
            level = q.level; ret_1d = q.ret_1d;
            source = "naver";
          } catch (e2) { throw new Error(`${String((e as Error)?.message || e)} / ${String((e2 as Error)?.message || e2)}`); }
        } else if (meta.asset_class === "fx") {
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
