// 조합형 프로그래매틱 SEO (2) — "지역 × 가구형태 × 파이어유형"별 필요자산·저축 플랜 페이지.
// 실제 계산된 고유 수치를 담아 thin content 회피. 빌드 시 firemap_market 실데이터 주입.
import { mkdirSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const ROOT = process.env.GUIDE_OUT || 'outputs/deploy';
const OUT = join(ROOT, 'guide', 'region-plan');
const BASE = 'https://firemap.kr';
const SUPA = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SKEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');

// 1인 월 생활비(주거 포함) tier 추정(원)
const TIER_COST = { 1: 2050000, 2: 1600000, 3: 1350000, 4: 1200000, 5: 1000000 };
// 대표 지역(이름, tier)
const REGIONS = [
  ['서울', 1], ['부산', 2], ['대구', 2], ['인천', 2], ['광주', 2], ['대전', 2], ['울산', 2], ['세종', 2],
  ['수원', 2], ['성남', 2], ['고양', 2], ['용인', 2], ['청주', 3], ['천안', 3], ['전주', 3], ['포항', 3],
  ['창원', 3], ['제주시', 3], ['춘천', 3], ['강릉', 3], ['여수', 3], ['경주', 4], ['목포', 4], ['군산', 4]
];
const HOUSEHOLD = [
  { key: '1인', label: '1인 가구', mult: 1.0 },
  { key: '부부', label: '부부(2인)', mult: 1.6 },
  { key: '4인', label: '4인 가족', mult: 2.2 }
];
const FIRETYPE = [
  { key: '린', label: '린파이어', costMult: 1.0, note: '생활비를 최소화해 더 적은 자산으로 일찍' },
  { key: '팻', label: '팻파이어', costMult: 1.4, note: '넉넉한 생활비를 유지하며 여유롭게' }
];
const RET = 6;
const SAVE_OPTS = [50, 100, 150, 200, 300]; // 월 저축(만원)

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const won = (won0) => { const m = Math.round(won0 / 10000); return m >= 10000 ? `${(m / 10000).toFixed(1)}억` : `${m.toLocaleString()}만원`; };
const slug = (s) => s.replace(/[^가-힣a-zA-Z0-9]/g, '');

function monthsToTarget(assetWon, monthlyWon, targetWon, annualPct) {
  const i = annualPct / 100 / 12;
  if (assetWon >= targetWon) return 0;
  if (monthlyWon <= 0) return Infinity;
  const k = monthlyWon / i;
  const g = (targetWon + k) / (assetWon + k);
  if (g <= 1) return 0;
  return Math.log(g) / Math.log(1 + i);
}
function fmtDur(months) {
  if (!isFinite(months)) return '저축 늘려야 도달';
  if (months <= 0) return '이미 달성';
  const tm = Math.round(months); const y = Math.floor(tm / 12); const mo = tm - y * 12;
  if (y <= 0) return `${Math.max(1, mo)}개월`;
  return mo > 0 ? `${y}년 ${mo}개월` : `${y}년`;
}

const CSS = "body{margin:0;background:#fffdf9;color:#18212c;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7}main{max-width:760px;margin:0 auto;padding:28px 20px 80px}h1{font-size:26px;letter-spacing:-.04em;line-height:1.3}h2{margin-top:30px;font-size:20px}a{color:#ea580c;font-weight:700;text-decoration:none}.lead{color:#5b6470}.box{border:1px solid #ffe1d0;border-radius:16px;background:#fff7f2;padding:16px 18px;margin:16px 0}.stat{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}.stat div{flex:1;min-width:130px;background:#fff;border:1px solid #eee;border-radius:14px;padding:12px 14px}.stat small{color:#9aa3bf;font-weight:700;font-size:12px}.stat b{display:block;font-size:19px;margin-top:3px}.cta{display:block;text-align:center;background:linear-gradient(180deg,#ff6a35,#ee4a1f);color:#fff;border-radius:14px;padding:14px;font-weight:800;margin:22px 0}.mkt{font-size:12.5px;color:#0f6e56;background:#f1faf6;border:1px solid #d6efe4;border-radius:10px;padding:9px 12px;margin:14px 0}.tags a{display:inline-block;background:#fff;border:1px solid #eee;border-radius:999px;padding:6px 12px;margin:4px 6px 0 0;font-size:13px;color:#555}table{width:100%;border-collapse:collapse;margin:12px 0;font-size:15px}th,td{border:1px solid #eee;padding:9px 10px;text-align:left}th{background:#f7f8fa}.note{color:#9aa3bf;font-size:12px;line-height:1.6}";

function page({ title, desc, keywords, canonical, body, faq }) {
  const ld = [
    { '@context': 'https://schema.org', '@type': 'Article', headline: title, description: desc, inLanguage: 'ko-KR', isPartOf: { '@type': 'WebSite', name: '파이어맵', url: BASE }, publisher: { '@type': 'Organization', name: '파이어맵' }, mainEntityOfPage: canonical },
    { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })) }
  ];
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><meta name="keywords" content="${esc(keywords)}"><link rel="canonical" href="${canonical}"><meta name="robots" content="index, follow"><meta property="og:type" content="article"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${canonical}"><meta property="og:image" content="${BASE}/og-image.png"><meta name="theme-color" content="#ff5a00"><script type="application/ld+json">${JSON.stringify(ld)}</script><style>${CSS}</style></head><body><main>${body}<p class="note">※ 파이어맵은 참고용 시뮬레이션이며 투자·세무 자문이 아니에요. 필요자산은 4% 룰(연 생활비×25) 기반 추정이며, 도달 기간은 연 ${RET}% 수익 가정의 근사치예요 — <a href="${BASE}/">계산기로 내 수치 보기</a>.</p></main></body></html>`;
}

async function fetchMarket() {
  try {
    const res = await fetch(`${SUPA}/rest/v1/rpc/fm_market_latest`, { method: 'POST', headers: { apikey: SKEY, authorization: `Bearer ${SKEY}`, 'content-type': 'application/json' }, body: '{}' });
    if (!res.ok) return null;
    const rows = await res.json();
    return Array.isArray(rows) ? rows : null;
  } catch { return null; }
}
function marketLine(market) {
  if (!market) return '';
  const spx = market.find((m) => m.symbol === '^spx');
  const fx = market.find((m) => m.symbol === 'usdkrw');
  const parts = [];
  if (spx && spx.ret_7d != null) parts.push(`S&P500 주간 ${spx.ret_7d > 0 ? '+' : ''}${spx.ret_7d}%`);
  if (fx && fx.level != null) parts.push(`환율 1USD≈${Math.round(fx.level).toLocaleString()}원`);
  if (!parts.length) return '';
  const d = String((spx && spx.updated_at) || (fx && fx.updated_at) || '').slice(0, 10);
  return `<p class="mkt">📈 오늘의 참고 시세 — ${parts.join(' · ')}${d ? ` (기준일 ${d})` : ''}.</p>`;
}

function comboPage(region, tier, hh, ft, market) {
  const monthly1 = TIER_COST[tier];
  const monthly = Math.round(monthly1 * hh.mult * ft.costMult);
  const annual = monthly * 12;
  const need = annual * 25;
  const s = slug(region);
  const canonical = `${BASE}/guide/region-plan/${s}-${hh.key}-${ft.key}.html`;
  const title = `${region} ${hh.label} ${ft.label} 필요자산·저축 플랜 | 파이어맵`;
  const desc = `${region}에서 ${hh.label} 기준 ${ft.label}(${ft.note})하려면 월 생활비 약 ${won(monthly)}, 필요자산 약 ${won(need)}. 월 저축별 도달 기간까지 계산.`;
  const keywords = `${region} 파이어, ${region} ${hh.label} 생활비, ${ft.label} 필요자산, ${region} 은퇴 자금, 파이어 계산기`;
  const sibHH = HOUSEHOLD.filter((x) => x.key !== hh.key).map((x) => `<a href="${BASE}/guide/region-plan/${s}-${x.key}-${ft.key}.html">${x.label}</a>`).join('');
  const sibFT = FIRETYPE.filter((x) => x.key !== ft.key).map((x) => `<a href="${BASE}/guide/region-plan/${s}-${hh.key}-${x.key}.html">${x.label}</a>`).join('');
  const body = `<p><a href="${BASE}/guide/region-plan/">← 지역·가구별 파이어 플랜</a></p>
  <h1>${region}에서 ${hh.label}로 ${ft.label}하려면?</h1>
  <p class="lead">${region}의 ${hh.label} 월 생활비를 약 <b>${won(monthly)}</b>으로 보면(${ft.label} 기준), 4% 룰로 필요한 자산은 약 <b>${won(need)}</b>이에요. ${ft.note} 방식이에요.</p>
  ${marketLine(market)}
  <div class="stat"><div><small>월 생활비(추정)</small><b>${won(monthly)}</b></div><div><small>연 생활비</small><b>${won(annual)}</b></div><div><small>필요자산(4% 룰)</small><b>${won(need)}</b></div></div>
  <h2>현재 자산 0에서 월 저축별 도달 기간 (연 ${RET}% 가정)</h2>
  <table><tr><th>월 저축</th><th>${won(need)} 도달</th></tr>${SAVE_OPTS.map((m) => `<tr><td>월 ${m}만원</td><td>${fmtDur(monthsToTarget(0, m * 10000, need, RET))}</td></tr>`).join('')}</table>
  <a class="cta" href="${BASE}/">국민연금·물가·건보까지 반영해 내 파이어 나이 계산 →</a>
  <h2>같은 ${region}, 다른 조건</h2>
  <p class="lead">가구형태 바꾸기:</p><div class="tags">${sibHH}</div>
  <p class="lead" style="margin-top:10px">파이어 유형 바꾸기:</p><div class="tags">${sibFT}</div>
  <p style="margin-top:14px"><a href="${BASE}/guide/regions/${s}.html">${region} 지역 생활비 자세히 →</a></p>
  <a class="cta" href="${BASE}/">🔥 내 파이어 가능 나이 1분 계산 →</a>`;
  const faq = [
    { q: `${region}에서 ${hh.label} ${ft.label}하려면 얼마가 필요한가요?`, a: `월 생활비 약 ${won(monthly)} 기준 4% 룰로 약 ${won(need)}이 필요합니다. 국민연금·물가·세금에 따라 달라지니 계산기로 확인하세요.` },
    { q: '린파이어와 팻파이어 차이는?', a: '린파이어는 생활비를 최소화해 더 적은 자산으로 일찍 은퇴, 팻파이어는 넉넉한 생활비를 유지하며 은퇴하는 방식입니다.' }
  ];
  return { slug: `${s}-${hh.key}-${ft.key}`, html: page({ title, desc, keywords, canonical, body, faq }) };
}

async function main() {
  if (!existsSync(ROOT)) { console.log(`[gen-region-plans] ROOT ${ROOT} 없음 — 건너뜀`); return; }
  mkdirSync(OUT, { recursive: true });
  const market = await fetchMarket();
  let n = 0;
  for (const [region, tier] of REGIONS) for (const hh of HOUSEHOLD) for (const ft of FIRETYPE) {
    const { slug: sl, html } = comboPage(region, tier, hh, ft, market);
    writeFileSync(join(OUT, `${sl}.html`), html);
    n++;
  }
  const hubBody = `<p><a href="${BASE}/">← 파이어맵</a></p><h1>지역·가구별 파이어 플랜</h1><p class="lead">지역 × 가구형태(1인·부부·4인) × 파이어유형(린·팻)별 필요자산과 저축 플랜. ${n}개 조합.</p>` +
    REGIONS.map(([r]) => `<h2>${r}</h2><div class="tags">${HOUSEHOLD.map((h) => FIRETYPE.map((f) => `<a href="${BASE}/guide/region-plan/${slug(r)}-${h.key}-${f.key}.html">${h.label}·${f.label}</a>`).join('')).join('')}</div>`).join('') +
    `<a class="cta" href="${BASE}/">내 파이어 나이 계산하기 →</a>`;
  writeFileSync(join(OUT, 'index.html'), page({ title: '지역·가구별 파이어 플랜 — 필요자산·저축 계획 | 파이어맵', desc: `지역×가구형태×파이어유형 ${n}개 조합의 필요자산·저축 플랜.`, keywords: '지역 파이어, 가구별 필요자산, 린파이어, 팻파이어, 파이어 계산', canonical: `${BASE}/guide/region-plan/`, body: hubBody, faq: [{ q: '이 수치는 정확한가요?', a: '4% 룰·연 6% 가정의 근사치입니다. 정확한 값은 계산기에서 확인하세요.' }] }));
  n++;
  console.log(`[gen-region-plans] ${n} pages → ${OUT}${market ? ' (market injected)' : ''}`);
}
main();
