// fetch-realestate — 국토부(MOLIT) 아파트 매매 실거래가 수집기 (추가전용).
// MOLIT_API_KEY 시크릿이 있을 때만 동작. 없으면 전체 건너뜀(graceful). 실패해도 기존 값 보존.
// 공공데이터포털 '아파트 매매 실거래가 상세' 서비스. 대표 지역 몇 곳만 집계(월평균 거래금).

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const MOLIT_KEY = Deno.env.get("MOLIT_API_KEY") || "";

// 대표 지역(시군구 5자리 LAWD_CD) — 앞으로 확장 가능
const REGIONS: [string, string][] = [
  ["11680", "서울 강남구"], ["11350", "서울 노원구"], ["11440", "서울 마포구"],
  ["26350", "부산 해운대구"], ["27260", "대구 수성구"], ["41135", "성남 분당구"], ["36110", "세종"]
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

async function regionAvg(lawd: string, ymd: string): Promise<number | null> {
  const url = `https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev?serviceKey=${encodeURIComponent(MOLIT_KEY)}&LAWD_CD=${lawd}&DEAL_YMD=${ymd}&numOfRows=1000&pageNo=1`;
  const res = await fetch(url);
  if (!res.ok) return null;
  const xml = await res.text();
  const amounts: number[] = [];
  const re = /<(?:dealAmount|거래금액)>\s*([0-9,]+)\s*<\/(?:dealAmount|거래금액)>/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(xml)) !== null) { const v = Number(m[1].replace(/,/g, "")); if (isFinite(v) && v > 0) amounts.push(v); }
  if (!amounts.length) return null;
  return Math.round(amounts.reduce((a, b) => a + b, 0) / amounts.length); // 만원 단위
}

Deno.serve(async (_req: Request) => {
  const now = new Date().toISOString();
  if (!MOLIT_KEY) {
    return new Response(JSON.stringify({ ok: true, at: now, updated: [], skipped: { all: "no MOLIT_API_KEY (dormant)" } }), { headers: { "content-type": "application/json" } });
  }
  const ymd = lastMonthYM();
  const updated: string[] = [];
  const skipped: Record<string, string> = {};
  for (const [lawd, name] of REGIONS) {
    try {
      const avg = await regionAvg(lawd, ymd);
      if (avg != null) { await upsert({ region: name, deal_type: "sale", metric: "avg_price", value: avg, unit: "만원", period: ymd, source: "molit", updated_at: now }); updated.push(`${name}:${avg}`); }
      else skipped[name] = "no deals";
    } catch (e) { skipped[name] = String((e as Error)?.message || e); }
  }
  return new Response(JSON.stringify({ ok: true, at: now, ymd, updated, skipped }), { headers: { "content-type": "application/json" } });
});
