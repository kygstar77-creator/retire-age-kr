// fetch-macro v5 — 거시 지표 수집기 (추가전용).
// World Bank(무키): CPI 물가상승률 + 예금금리 폴백. ECOS(키): 기준금리 · 월별 CPI · 월별 정기예금 금리.
// 안전: 실패/무키 시 해당 항목만 건너뜀(기존 값 보존). 쓰기는 service_role.

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

function ym(d: Date) { return `${d.getUTCFullYear()}${String(d.getUTCMonth() + 1).padStart(2, "0")}`; }

// ECOS 시계열 조회: 최근 N개월 윈도에서 [{time,value}] 오름차순 반환
async function ecosSeries(stat: string, item: string, monthsBack: number): Promise<{ time: string; value: number }[]> {
  const d = new Date();
  const end = ym(d);
  const start = ym(new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - monthsBack, 1)));
  const url = `https://ecos.bok.or.kr/api/StatisticSearch/${ECOS_KEY}/json/kr/1/700/${stat}/M/${start}/${end}/${item}`;
  const res = await fetch(url);
  const j = await res.json();
  const rows = j?.StatisticSearch?.row || [];
  const out: { time: string; value: number }[] = [];
  for (const r of rows) { const v = Number(r.DATA_VALUE); if (isFinite(v)) out.push({ time: String(r.TIME), value: v }); }
  if (!out.length && j?.RESULT?.MESSAGE) throw new Error(`ecos ${stat}: ${j.RESULT.MESSAGE}`);
  return out;
}

// ECOS 통계항목 탐색: 항목코드를 박아두지 않고 항목명으로 찾는다.
// (코드를 하드코딩하면 오타·개편 시 조용히 빈 값이 되므로)
type EcosItem = { ITEM_CODE?: string; ITEM_NAME?: string };
async function ecosItemFind(stat: string, re: RegExp): Promise<{ code: string; name: string } | null> {
  const url = `https://ecos.bok.or.kr/api/StatisticItemList/${ECOS_KEY}/json/kr/1/500/${stat}`;
  const res = await fetch(url);
  const j = await res.json();
  const rows: EcosItem[] = j?.StatisticItemList?.row || [];
  if (!rows.length && j?.RESULT?.MESSAGE) throw new Error(`ecos items ${stat}: ${j.RESULT.MESSAGE}`);
  const hits = rows.filter((r) => r.ITEM_CODE && re.test(String(r.ITEM_NAME || "")));
  if (!hits.length) return null;
  // 이름이 가장 짧은 것 = 세분류가 아닌 대표 항목 (예: '정기예금' < '정기예금(6개월미만)')
  hits.sort((a, b) => String(a.ITEM_NAME).length - String(b.ITEM_NAME).length);
  return { code: String(hits[0].ITEM_CODE), name: String(hits[0].ITEM_NAME) };
}

Deno.serve(async (_req: Request) => {
  const now = new Date().toISOString();
  const updated: string[] = [];
  const skipped: Record<string, string> = {};

  // 1) CPI 물가상승률 (World Bank FP.CPI.TOTL.ZG, 연간 %) — 항상 보존되는 베이스
  try {
    const cpi = await wbLatest("FP.CPI.TOTL.ZG");
    if (cpi) { await upsert("firemap_cpi", "period", { period: cpi.date, region: "KR", yoy: round2(cpi.value), source: "worldbank", updated_at: now }); updated.push(`cpi_wb:${cpi.date}`); }
    else skipped["cpi_wb"] = "no value";
  } catch (e) { skipped["cpi_wb"] = String((e as Error)?.message || e); }

  // 2) 예금금리 — ECOS 월별(121Y002 예금은행 수신금리 / 정기예금) 우선.
  //    World Bank FR.INR.DPST는 '연평균'이라 최신 표기와 최대 1년 이상 어긋난다
  //    (예: 2026년 9월에 2025년 연평균이 최신값으로 노출 → 기준금리보다 낮아 역전처럼 보임).
  //    그래서 ECOS가 실패할 때만 폴백으로 쓰고, 그 경우 source='worldbank'라 UI가 알아서 숨긴다.
  let depositFromEcos = false;
  if (ECOS_KEY) {
    try {
      const item = await ecosItemFind("121Y002", /정기예금/);
      if (!item) skipped["deposit_ecos"] = "121Y002에 정기예금 항목 없음";
      else {
        const s = await ecosSeries("121Y002", item.code, 24);
        const latest = s.length ? s[s.length - 1] : null;
        if (latest) {
          await upsert("firemap_rates", "key", { key: "deposit_12m", label: `${item.name} 금리(ECOS)`, value: round2(latest.value), unit: "%", as_of: latest.time, source: "ecos", updated_at: now });
          updated.push(`deposit_ecos:${latest.time}(${item.name})`);
          depositFromEcos = true;
        } else skipped["deposit_ecos"] = "ecos no value";
      }
    } catch (e) { skipped["deposit_ecos"] = String((e as Error)?.message || e); }
  }
  if (!depositFromEcos) {
    try {
      const dep = await wbLatest("FR.INR.DPST");
      if (dep) { await upsert("firemap_rates", "key", { key: "deposit_12m", label: "예금금리(World Bank)", value: round2(dep.value), unit: "%", as_of: dep.date, source: "worldbank", updated_at: now }); updated.push(`deposit_wb:${dep.date}`); }
      else skipped["deposit_wb"] = "no value";
    } catch (e) { skipped["deposit_wb"] = String((e as Error)?.message || e); }
  }

  // 3) 기준금리 — ECOS 키 있을 때만(722Y001/0101000, 최신값). 없으면 기존 seed 유지
  if (ECOS_KEY) {
    try {
      const s = await ecosSeries("722Y001", "0101000", 24);
      const latest = s.length ? s[s.length - 1] : null;
      if (latest) { await upsert("firemap_rates", "key", { key: "base_rate", label: "한국은행 기준금리(ECOS)", value: round2(latest.value), unit: "%", as_of: latest.time, source: "ecos", updated_at: now }); updated.push(`base_rate:${latest.time}`); }
      else skipped["base_rate"] = "ecos no value";
    } catch (e) { skipped["base_rate"] = String((e as Error)?.message || e); }

    // 4) 월별 CPI (ECOS 901Y009 총지수 '0', 신규) — 13개월 윈도로 전년동월비 계산
    try {
      const s = await ecosSeries("901Y009", "0", 15);
      if (s.length >= 13) {
        const latest = s[s.length - 1];
        const yearAgo = s[s.length - 13];
        const yoy = round2((latest.value / yearAgo.value - 1) * 100);
        await upsert("firemap_cpi", "period", { period: latest.time, region: "KR", index: round2(latest.value), yoy, source: "ecos", updated_at: now });
        updated.push(`cpi_ecos:${latest.time}`);
      } else skipped["cpi_ecos"] = `insufficient rows (${s.length})`;
    } catch (e) { skipped["cpi_ecos"] = String((e as Error)?.message || e); }
  } else { skipped["ecos"] = "no ECOS key (seed/WB 유지)"; }

  return new Response(JSON.stringify({ ok: true, at: now, updated, skipped }), { headers: { "content-type": "application/json" } });
});
