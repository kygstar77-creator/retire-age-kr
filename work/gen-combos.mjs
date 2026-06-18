// 조합형 프로그래매틱 SEO — "현재자산 × 월저축 × 목표자산"별 파이어 도달 플랜 페이지를 대량 생성.
// 각 페이지는 실제 계산된 고유 수치(도달 기간/나이 무관 연수)를 담아 thin content 회피.
// 빌드 시 firemap_market(실데이터)을 가져와 '오늘의 참고 시세'를 주입(실패해도 빌드 지속).
import { mkdirSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const ROOT = process.env.GUIDE_OUT || 'outputs/deploy';
const OUT = join(ROOT, 'guide', 'plan');
const BASE = 'https://firemap.kr';
const SUPA = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SKEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');

// 축: 월저축(만원) × 현재자산(만원) × 목표자산(억)
const MONTHLY = [30, 50, 70, 100, 150, 200, 300];
const ASSET = [0, 5000, 10000, 30000];
const TARGET_EOK = [3, 5, 7, 10, 15];
const RET = 6; // 연 수익률 가정(보수적, 명목) — 본문에 명시

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const won = (manwon) => { const m = Math.round(manwon); return m >= 10000 ? `${(m / 10000).toFixed(m % 10000 === 0 ? 0 : 1)}억` : `${m.toLocaleString()}만원`; };
const eokWon = (eok) => eok * 100000000;

// 적립식 복리로 목표 도달까지 개월수 — A*(1+i)^n + m*((1+i)^n-1)/i = T
function monthsToTarget(assetWon, monthlyWon, targetWon, annualPct) {
  const i = annualPct / 100 / 12;
  if (assetWon >= targetWon) return 0;
  if (monthlyWon <= 0 && assetWon <= 0) return Infinity;
  const k = monthlyWon / i; // m/i
  const g = (targetWon + k) / (assetWon + k);
  if (g <= 1) return 0;
  const n = Math.log(g) / Math.log(1 + i);
  return n;
}
function fmtDur(months) {
  if (!isFinite(months)) return '도달 불가(저축·수익률 상향 필요)';
  if (months <= 0) return '이미 목표 달성';
  const y = Math.floor(months / 12); const mo = Math.round(months - y * 12);
  if (y <= 0) return `${Math.max(1, mo)}개월`;
  return mo > 0 ? `${y}년 ${mo}개월` : `${y}년`;
}

const CSS = "body{margin:0;background:#fffdf9;color:#18212c;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7}main{max-width:760px;margin:0 auto;padding:28px 20px 80px}h1{font-size:27px;letter-spacing:-.04em;line-height:1.3}h2{margin-top:30px;font-size:20px}a{color:#ea580c;font-weight:700;text-decoration:none}.lead{color:#5b6470}.box{border:1px solid #ffe1d0;border-radius:16px;background:#fff7f2;padding:16px 18px;margin:16px 0}.stat{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}.stat div{flex:1;min-width:130px;background:#fff;border:1px solid #eee;border-radius:14px;padding:12px 14px}.stat small{color:#9aa3bf;font-weight:700;font-size:12px}.stat b{display:block;font-size:19px;margin-top:3px}.cta{display:block;text-align:center;background:linear-gradient(180deg,#ff6a35,#ee4a1f);color:#fff;border-radius:14px;padding:14px;font-weight:800;margin:22px 0}.mkt{font-size:12.5px;color:#0f6e56;background:#f1faf6;border:1px solid #d6efe4;border-radius:10px;padding:9px 12px;margin:14px 0}.tags a{display:inline-block;background:#fff;border:1px solid #eee;border-radius:999px;padding:6px 12px;margin:4px 6px 0 0;font-size:13px;color:#555}table{width:100%;border-collapse:collapse;margin:12px 0;font-size:15px}th,td{border:1px solid #eee;padding:9px 10px;text-align:left}th{background:#f7f8fa}.note{color:#9aa3bf;font-size:12px;line-height:1.6}";

function page({ title, desc, keywords, canonical, body, faq }) {
  const ld = [
    { '@context': 'https://schema.org', '@type': 'Article', headline: title, description: desc, inLanguage: 'ko-KR', isPartOf: { '@type': 'WebSite', name: '파이어맵', url: BASE }, publisher: { '@type': 'Organization', name: '파이어맵' }, mainEntityOfPage: canonical },
    { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })) }
  ];
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><meta name="keywords" content="${esc(keywords)}"><link rel="canonical" href="${canonical}"><meta name="robots" content="index, follow"><meta property="og:type" content="article"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${canonical}"><meta property="og:image" content="${BASE}/og-image.png"><meta name="theme-color" content="#ff5a00"><script type="application/ld+json">${JSON.stringify(ld)}</script><style>${CSS}</style></head><body><main>${body}<p class="note">※ 파이어맵은 입력값을 기계적으로 계산하는 참고용 시뮬레이션이며 투자·세무 자문이 아니에요. 도달 기간은 연 ${RET}% 수익 가정의 근사치로, 실제는 물가·세금·건강보험료·국민연금에 따라 달라져요 — <a href="${BASE}/">계산기로 내 수치 보기</a>.</p></main></body></html>`;
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
  const asOf = (spx && spx.updated_at) || (fx && fx.updated_at) || '';
  const d = asOf ? String(asOf).slice(0, 10) : '';
  return `<p class="mkt">📈 오늘의 참고 시세 — ${parts.join(' · ')}${d ? ` (기준일 ${d})` : ''}. 시장 수익률은 장기 평균으로 보수적으로 가정하세요.</p>`;
}

function comboPage(monthly, asset, targetEok, market) {
  const mWon = monthly * 10000;
  const aWon = asset * 10000;
  const tWon = eokWon(targetEok);
  const months = monthsToTarget(aWon, mWon, tWon, RET);
  const dur = fmtDur(months);
  const slug = `m${monthly}-a${asset}-t${targetEok}`;
  const canonical = `${BASE}/guide/plan/${slug}.html`;
  const aLabel = asset === 0 ? '자산 0원에서' : `현재 ${won(asset)}으로`;
  const title = `${aLabel} 월 ${won(monthly)} 모으면 ${targetEok}억까지 얼마나? | 파이어맵`;
  const desc = `현재 자산 ${won(asset)}, 매달 ${won(monthly)} 저축, 목표 ${targetEok}억일 때 파이어(목표자산) 도달까지 약 ${dur}(연 ${RET}% 가정). 실제 내 수치는 계산기로 1분.`;
  const keywords = `월 ${monthly}만원 저축, ${targetEok}억 모으기, 파이어 도달 기간, 목표자산 ${targetEok}억, 저축 계획, 파이어 계산기`;
  const sib = MONTHLY.filter((x) => x !== monthly).map((x) => `<a href="${BASE}/guide/plan/m${x}-a${asset}-t${targetEok}.html">월 ${won(x)}</a>`).join('');
  const sibT = TARGET_EOK.filter((x) => x !== targetEok).map((x) => `<a href="${BASE}/guide/plan/m${monthly}-a${asset}-t${x}.html">${x}억 목표</a>`).join('');
  const remain = Math.max(0, tWon - aWon);
  const body = `<p><a href="${BASE}/guide/plan/">← 파이어 플랜 계산 모음</a></p>
  <h1>${aLabel} 월 ${won(monthly)} 모으면 ${targetEok}억까지 얼마나 걸릴까?</h1>
  <p class="lead">현재 금융자산 ${won(asset)}, 매달 ${won(monthly)}씩 저축·투자해서 목표 ${targetEok}억(파이어 목표자산)에 도달하는 시간을 연 ${RET}% 수익 가정으로 계산했어요.</p>
  ${marketLine(market)}
  <div class="stat"><div><small>목표까지 더 필요</small><b>${won(Math.round(remain / 10000))}</b></div><div><small>도달 예상 기간</small><b>${dur}</b></div><div><small>가정 수익률</small><b>연 ${RET}%</b></div></div>
  <div class="box"><b>어떻게 계산했나</b><br>적립식 복리로, 현재자산이 불어나는 동시에 매달 저축이 더해져요. 월 ${won(monthly)}·연 ${RET}%면 목표 ${targetEok}억까지 <b>${dur}</b> 걸려요. 저축을 늘리거나 목표를 낮추면 크게 단축돼요.</div>
  <h2>저축액을 바꾸면? (목표 ${targetEok}억 · 현재 ${won(asset)})</h2>
  <table><tr><th>월 저축</th><th>도달 기간</th></tr>${MONTHLY.map((x) => `<tr><td>월 ${won(x)}${x === monthly ? ' (이 글)' : ''}</td><td>${fmtDur(monthsToTarget(aWon, x * 10000, tWon, RET))}</td></tr>`).join('')}</table>
  <a class="cta" href="${BASE}/">국민연금·물가·세금까지 반영해 내 파이어 나이 계산 →</a>
  <h2>이 플랜은 파이어 여정의 ‘실행·가속’ 단계예요</h2>
  <p>목표와 저축액이 정해졌다면 이제 <b>매달 기록하며 굴리는 단계</b>예요. 파이어맵에서 저축·절약을 기록하면 파이어가 며칠씩 당겨지는 걸 눈으로 볼 수 있어요.</p>
  <h2>다른 조합도 보기</h2>
  <p class="lead">같은 목표, 다른 월 저축:</p><div class="tags">${sib}</div>
  <p class="lead" style="margin-top:10px">현재 자산은 같고, 다른 목표:</p><div class="tags">${sibT}</div>
  <a class="cta" href="${BASE}/">🔥 내 파이어 가능 나이 1분 계산 →</a>`;
  const faq = [
    { q: `월 ${won(monthly)} 저축하면 ${targetEok}억까지 얼마나 걸리나요?`, a: `현재 자산 ${won(asset)}에서 연 ${RET}% 수익을 가정하면 약 ${dur} 걸립니다. 수익률·물가·세금에 따라 달라지니 계산기로 본인 수치를 확인하세요.` },
    { q: '수익률은 몇 %로 봐야 하나요?', a: `장기 분산투자 기준 연 ${RET}% 안팎을 보수적으로 가정하는 경우가 많습니다. 높은 수익률 전제는 도달이 늦어질 위험을 키웁니다.` }
  ];
  return { slug, html: page({ title, desc, keywords, canonical, body, faq }) };
}

async function main() {
  if (!existsSync(ROOT)) { console.log(`[gen-combos] ROOT ${ROOT} 없음 — 건너뜀`); return; }
  mkdirSync(OUT, { recursive: true });
  const market = await fetchMarket();
  let n = 0;
  for (const m of MONTHLY) for (const a of ASSET) for (const t of TARGET_EOK) {
    const { slug, html } = comboPage(m, a, t, market);
    writeFileSync(join(OUT, `${slug}.html`), html);
    n++;
  }
  const hubBody = `<p><a href="${BASE}/">← 파이어맵</a></p><h1>파이어 플랜 계산 모음</h1><p class="lead">현재 자산·월 저축·목표 금액 조합별로 파이어(목표자산) 도달 기간을 계산했어요. ${n}개 시나리오.</p>` +
    TARGET_EOK.map((t) => `<h2>목표 ${t}억</h2><div class="tags">${MONTHLY.map((m) => `<a href="${BASE}/guide/plan/m${m}-a0-t${t}.html">월 ${won(m)}</a>`).join('')}</div>`).join('') +
    `<a class="cta" href="${BASE}/">내 파이어 나이 계산하기 →</a>`;
  writeFileSync(join(OUT, 'index.html'), page({ title: '파이어 플랜 계산 모음 — 월 저축·목표별 도달 기간 | 파이어맵', desc: `현재 자산·월 저축·목표 금액 조합별 파이어 도달 기간 ${n}개 시나리오.`, keywords: '파이어 계산, 저축 계획, 목표자산, 파이어 도달 기간', canonical: `${BASE}/guide/plan/`, body: hubBody, faq: [{ q: '이 계산은 정확한가요?', a: '연 6% 수익 가정의 근사치입니다. 물가·세금·국민연금·건강보험료가 반영되는 정확한 값은 계산기에서 확인하세요.' }] }));
  n++;
  console.log(`[gen-combos] ${n} pages → ${OUT}${market ? ' (market injected)' : ' (no market data)'}`);
}
main();
