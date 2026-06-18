// fetch-realestate v2 — 국토부(MOLIT) 아파트 실거래가 수집기 (추가전용).
// MOLIT_API_KEY 시크릿이 있을 때만 동작. 없으면 전체 건너뜀(graceful). 실패해도 기존 값 보존.
// 매매(아파트 매매 실거래가 상세) + 전세(아파트 전월세 실거래가, 월세=0 보증금). 시(市)별 대표 자치구 평균.
// region 키는 사이트 지역 페이지 이름과 동일하게 저장(예: '서울','부산','성남','세종') → 페이지에서 이름으로 조인.

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const MOLIT_KEY = Deno.env.get("MOLIT_API_KEY") || "";

// [페이지 지역명, [대표 시군구 LAWD 5자리 ...]] — 평균으로 집계. 코드 추가/수정 시 그대로 확장.
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
  ["춘천", ["51110"]]
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

// kind: 'sale' = 거래금액 평균 / 'jeonse' = 월세 0인 전세 보증금 평균. 단위 만원.
async function avgFor(kind: "sale" | "jeonse", lawds: string[], ymd: string): Promise<number | null> {
  const op = kind === "sale" ? "RTMSDataSvcAptTradeDev" : "RTMSDataSvcAptRent";
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
    } catch { /* skip this lawd */ }
  }
  if (!amounts.length) return null;
  return Math.round(amounts.reduce((a, b) => a + b, 0) / amounts.length);
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
      const sale = await avgFor("sale", lawds, ymd);
      if (sale != null) { await upsert({ region: name, deal_type: "sale", metric: "avg_price", value: sale, unit: "만원", period: ymd, source: "molit", updated_at: now }); updated.push(`${name}/sale:${sale}`); }
      const jeonse = await avgFor("jeonse", lawds, ymd);
      if (jeonse != null) { await upsert({ region: name, deal_type: "jeonse", metric: "avg_deposit", value: jeonse, unit: "만원", period: ymd, source: "molit", updated_at: now }); updated.push(`${name}/jeonse:${jeonse}`); }
      if (sale == null && jeonse == null) skipped[name] = "no deals";
    } catch (e) { skipped[name] = String((e as Error)?.message || e); }
  }
  return new Response(JSON.stringify({ ok: true, at: now, ymd, updated, skipped }), { headers: { "content-type": "application/json" } });
});
