// fetch-realestate v5 — 국토부(MOLIT) 아파트 실거래가 수집기 (추가전용).
// MOLIT_API_KEY 있을 때만 동작. 없으면 건너뜀(graceful). 실패해도 기존 값 보존.
// 경로: /1613000/{op}/get{op}. 매매: 상세 → 기본 폴백. 전세: getRTMSDataSvcAptRent(월세 0).
// region 키 = 사이트 지역 페이지 이름. 주 1회 cron(firemap-realestate-weekly, 수 22:40 UTC)으로 갱신.

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const MOLIT_KEY = Deno.env.get("MOLIT_API_KEY") || "";

const REGIONS: [string, string[]][] = [
  ["서울", ["11680", "11710", "11350", "11440"]],
  ["부산", ["26350", "26230", "26260"]],
  ["대구", ["27260", "27290", "27110"]],
  ["인천", ["28185", "28237", "28200"]],
  ["광주", ["29200", "29170", "29155"]],
  ["대전", ["30200", "30170", "30110"]],
  ["울산", ["31140", "31110"]],
  ["세종", ["36110"]],
  ["수원", ["41117", "41113", "41115"]],
  ["성남", ["41135", "41131", "41133"]],
  ["고양", ["41285", "41281"]],
  ["용인", ["41465", "41463"]],
  ["청주", ["43113", "43111"]],
  ["천안", ["44133", "44131"]],
  ["전주", ["45111", "45113"]],
  ["창원", ["48123", "48121"]],
  ["포항", ["47111", "47113"]],
  ["제주시", ["50110"]],
  ["강릉", ["51150"]],
  ["춘천", ["51110"]],
  ["여수", ["46130"]],
  ["경주", ["47130"]],
  ["목포", ["46110"]],
  ["군산", ["45130"]],
  ["김해", ["48250"]],
  ["진주", ["48170"]],
  ["양산", ["48330"]],
  ["구미", ["47190"]],
  ["원주", ["51130"]],
  ["아산", ["44200"]]
];

function lastMonthYM(): string {
  const d = new Date();
  d.setUTCDate(1); d.setUTCMonth(d.getUTCMonth() - 1);
  return `${d.getUTCFullYear()}${String(d.getUTCMonth() + 1).padStart(2, "0")}`;
}

async function upsert(row: Record<string, unknown>) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/firemap_realestate?on_conflict=region,deal_type,metric,period`, {
    method: "POST",
    headers: { apikey: SERVICE_KEY, authorization: `Bearer ${SERVICE_KEY}`, "content-type": "application/json", prefer: "resolution=merge-duplicates,return=minimal" },
    body: JSON.stringify(row),
  });
  if (!res.ok) throw new Error(`upsert ${res.status} ${await res.text()}`);
}

async function avgForOp(op: string, kind: "sale" | "jeonse", lawds: string[], ymd: string): Promise<number | null> {
  const amounts: number[] = [];
  for (const lawd of lawds) {
    try {
      const url = `https://apis.data.go.kr/1613000/${op}/get${op}?serviceKey=${encodeURIComponent(MOLIT_KEY)}&LAWD_CD=${lawd}&DEAL_YMD=${ymd}&numOfRows=1000&pageNo=1`;
      const res = await fetch(url);
      if (!res.ok) continue;
      const xml = await res.text();
      if (kind === "sale") {
        const re = /<(?:dealAmount|거래금액)>\s*([0-9,]+)\s*<\/(?:dealAmount|거래금액)>/g;
        let m: RegExpExecArray | null;
        while ((m = re.exec(xml)) !== null) { const v = Number(m[1].replace(/,/g, "")); if (isFinite(v) && v > 0) amounts.push(v); }
      } else {
        const items = xml.split(/<item>/).slice(1);
        for (const it of items) {
          const dm = it.match(/<(?:deposit|보증금액|보증금)>\s*([0-9,]+)/);
          const mm = it.match(/<(?:monthlyRent|월세금액|월세)>\s*([0-9,]*)/);
          const dep = dm ? Number(dm[1].replace(/,/g, "")) : 0;
          const mon = mm ? Number((mm[1] || "0").replace(/,/g, "")) : 0;
          if (isFinite(dep) && dep > 0 && mon === 0) amounts.push(dep);
        }
      }
    } catch { /* skip */ }
  }
  if (!amounts.length) return null;
  return Math.round(amounts.reduce((a, b) => a + b, 0) / amounts.length);
}

async function saleAvg(lawds: string[], ymd: string): Promise<number | null> {
  for (const op of ["RTMSDataSvcAptTradeDev", "RTMSDataSvcAptTrade"]) {
    const v = await avgForOp(op, "sale", lawds, ymd);
    if (v != null) return v;
  }
  return null;
}

Deno.serve(async (_req: Request) => {
  const now = new Date().toISOString();
  if (!MOLIT_KEY) {
    return new Response(JSON.stringify({ ok: true, at: now, updated: [], skipped: { all: "no MOLIT_API_KEY (dormant)" } }), { headers: { "content-type": "application/json" } });
  }
  const ymd = lastMonthYM();
  const updated: string[] = [];
  const skipped: Record<string, string> = {};
  for (const [name, lawds] of REGIONS) {
    try {
      const sale = await saleAvg(lawds, ymd);
      if (sale != null) { await upsert({ region: name, deal_type: "sale", metric: "avg_price", value: sale, unit: "만원", period: ymd, source: "molit", updated_at: now }); updated.push(`${name}/sale:${sale}`); }
      const jeonse = await avgForOp("RTMSDataSvcAptRent", "jeonse", lawds, ymd);
      if (jeonse != null) { await upsert({ region: name, deal_type: "jeonse", metric: "avg_deposit", value: jeonse, unit: "만원", period: ymd, source: "molit", updated_at: now }); updated.push(`${name}/jeonse:${jeonse}`); }
      if (sale == null) skipped[`${name}/sale`] = "no data";
      if (jeonse == null) skipped[`${name}/jeonse`] = "no data";
    } catch (e) { skipped[name] = String((e as Error)?.message || e); }
  }
  return new Response(JSON.stringify({ ok: true, at: now, ymd, updated: updated.slice(0, 80), skipped }), { headers: { "content-type": "application/json" } });
});
