// fetch-macro — 거시 지표 수집기 (Phase 2)
// 무키 공개 소스(World Bank)에서 한국 CPI 물가상승률·예금금리를 수집해 firemap_cpi/firemap_rates에 추가전용 upsert.
// ECOS_API_KEY 시크릿이 설정되면 한국은행 기준금리도 수집(없으면 스킵→기존 값 유지).
// 안전: 실패 시 건너뜀(기존 값 보존), 입력 미신뢰. 쓰기는 service_role.

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ECOS_KEY = Deno.env.get("ECOS_API_KEY") || "";

const round2 = (v: number) => Math.round(v * 100) / 100;

async function wbLatest(indicator: string): Promise<{ date: string; value: number } | null> {
  try {
    const url = `https://api.worldbank.org/v2/country/KR/indicator/${indicator}?format=json&mrv=8`;
    const res = await fetch(url, { headers: { "User-Agent": "firemap-fetch-macro/1.0" } });
    if (!res.ok) return null;
    const j = await res.json();
    const rows = Array.isArray(j) && Array.isArray(j[1]) ? j[1] : [];
    for (const r of rows) {
      if (r && typeof r.value === "number" && isFinite(r.value)) return { date: String(r.date), value: r.value };
    }
    return null;
  } catch { return null; }
}

async function upsert(table: string, conflict: string, row: Record<string, unknown>) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${table}?on_conflict=${conflict}`, {
    method: "POST",
    headers: {
      apikey: SERVICE_KEY, authorization: `Bearer ${SERVICE_KEY}`,
      "content-type": "application/json", prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify(row),
  });
  if (!res.ok) throw new Error(`upsert ${table} ${res.status} ${await res.text()}`);
}

Deno.serve(async (_req: Request) => {
  const now = new Date().toISOString();
  const updated: string[] = [];
  const skipped: Record<string, string> = {};

  // 1) CPI 물가상승률 (World Bank FP.CPI.TOTL.ZG, %)
  try {
    const cpi = await wbLatest("FP.CPI.TOTL.ZG");
    if (cpi) { await upsert("firemap_cpi", "period", { period: cpi.date, region: "KR", yoy: round2(cpi.value), source: "worldbank", updated_at: now }); updated.push(`cpi:${cpi.date}`); }
    else skipped["cpi"] = "no value";
  } catch (e) { skipped["cpi"] = String((e as Error)?.message || e); }

  // 2) 예금금리 (World Bank FR.INR.DPST, %)
  try {
    const dep = await wbLatest("FR.INR.DPST");
    if (dep) { await upsert("firemap_rates", "key", { key: "deposit_12m", label: "예금금리(World Bank)", value: round2(dep.value), unit: "%", as_of: dep.date, source: "worldbank", updated_at: now }); updated.push(`deposit:${dep.date}`); }
    else skipped["deposit"] = "no value";
  } catch (e) { skipped["deposit"] = String((e as Error)?.message || e); }

  // 3) 기준금리 — ECOS 키 있을 때만(없으면 기존 seed 유지)
  if (ECOS_KEY) {
    try {
      const url = `https://ecos.bok.or.kr/api/StatisticSearch/${ECOS_KEY}/json/kr/1/1/722Y001/M/202401/209912/0101000`;
      const res = await fetch(url);
      const j = await res.json();
      const row = j?.StatisticSearch?.row?.[0];
      const v = row ? Number(row.DATA_VALUE) : NaN;
      if (isFinite(v)) { await upsert("firemap_rates", "key", { key: "base_rate", label: "한국은행 기준금리(ECOS)", value: v, unit: "%", as_of: String(row.TIME), source: "ecos", updated_at: now }); updated.push("base_rate"); }
      else skipped["base_rate"] = "ecos no value";
    } catch (e) { skipped["base_rate"] = String((e as Error)?.message || e); }
  } else { skipped["base_rate"] = "no ECOS key"; }

  return new Response(JSON.stringify({ ok: true, at: now, updated, skipped }), { headers: { "content-type": "application/json" } });
});
