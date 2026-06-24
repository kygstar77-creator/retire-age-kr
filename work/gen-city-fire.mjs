import { mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';
import { TEST_CITIES } from '../src/firemap-v2/cityTypeTest.js';

// 빌드타임 도시별 '파이어로 살기' SEO 페이지 생성기 — gen-seo 직전 실행되어 sitemap 자동 포함.
// 각 도시: 월 생활비·4%룰 필요자산·장단점·FAQ + JSON-LD(Place/FAQPage/BreadcrumbList) + 유형테스트/계산기 CTA.
const ROOT = process.env.CITY_OUT || 'outputs/deploy';
const BASE = 'https://firemap.kr';
const SWR = 0.04; // 4% 룰

const SLUG = {
  '제주(서귀포)': 'jeju', '부산': 'busan', '강릉': 'gangneung', '양평': 'yangpyeong', '속초': 'sokcho',
  '전주': 'jeonju', '경주': 'gyeongju', '통영': 'tongyeong', '서울': 'seoul', '인천': 'incheon', '대전': 'daejeon', '여수': 'yeosu',
  '치앙마이': 'chiangmai', '다낭': 'danang', '우붓(발리)': 'ubud-bali', '쿠알라룸푸르': 'kuala-lumpur',
  '트빌리시': 'tbilisi', '리스본': 'lisbon', '후쿠오카': 'fukuoka', '방콕': 'bangkok', '호치민': 'hochiminh', '페낭': 'penang'
};
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const eok = (won) => { const m = Math.round(won / 10000); return m >= 10000 ? `${(m / 10000).toFixed(1)}억원` : `${m.toLocaleString()}만원`; };
const CSS = "body{margin:0;background:#fffdf9;color:#18212c;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7}main{max-width:760px;margin:0 auto;padding:28px 20px 80px}h1{font-size:27px;letter-spacing:-.04em;line-height:1.3}h2{margin-top:26px;font-size:19px}a{color:#ea580c;font-weight:700;text-decoration:none}.stat{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}.stat div{flex:1;min-width:130px;background:#fff;border:1px solid #eee;border-radius:14px;padding:13px 15px}.stat small{color:#9aa3bf;font-weight:700;font-size:12px}.stat b{display:block;font-size:21px;margin-top:3px}.cta{display:block;text-align:center;background:linear-gradient(180deg,#ff6a35,#ee4a1f);color:#fff;border-radius:14px;padding:14px;font-weight:800;margin:20px 0}.faq{border:1px solid #eee;border-radius:14px;background:#fff;padding:4px 16px;margin:8px 0}.tags a{display:inline-block;background:#fff;border:1px solid #eee;border-radius:999px;padding:6px 12px;margin:4px 6px 0 0;font-size:13px;color:#555}.note{color:#9aa3bf;font-size:12px;line-height:1.6;margin-top:24px}";

function faqLd(faqs) {
  return { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: faqs.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })) };
}
function crumbLd(city) {
  return { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
    { '@type': 'ListItem', position: 1, name: '파이어맵', item: BASE },
    { '@type': 'ListItem', position: 2, name: '도시별 파이어', item: `${BASE}/fire-city/` },
    { '@type': 'ListItem', position: 3, name: city }
  ] };
}
function placeLd(c) {
  return { '@context': 'https://schema.org', '@type': 'Place', name: c.city, address: { '@type': 'PostalAddress', addressCountry: c.country }, geo: { '@type': 'GeoCoordinates', latitude: c.lat, longitude: c.lon } };
}

function cityPage(c, siblings) {
  const slug = SLUG[c.city] || encodeURIComponent(c.city);
  const annual = c.krw * 12;
  const required = annual / SWR; // 4%룰 필요자산
  const title = `${c.city} 파이어·은퇴 살기 비용 (2026) — 월 생활비·필요 자산 | 파이어맵`;
  const desc = `${c.city}(${c.country})에서 파이어/조기은퇴로 살 때 월 생활비 약 ${eok(c.krw)}, 4%룰 기준 필요 자산 약 ${eok(required)} 추정. 의료·기후·비자까지 한눈에. 2026 기준 추정.`;
  const faqs = [
    { q: `${c.city}에서 한 달 생활비는 얼마인가요?`, a: `1인 기준 월 약 ${eok(c.krw)}로 추정해요(주거 포함, 통계·물가 기반 추정치). 실제는 주거 형태·환율에 따라 달라져요.` },
    { q: `${c.city}에서 파이어하려면 자산이 얼마나 필요한가요?`, a: `4%룰(연 생활비÷0.04) 기준 약 ${eok(required)}가 필요해요. 국민연금·부업·임대수입이 있으면 더 적어도 돼요 — 계산기로 내 조건을 넣어보세요.` },
    { q: `${c.city}는 어떤 파이어족에게 어울리나요?`, a: `${c.blurb} 9문항 '파이어 유형 테스트'로 나에게 맞는지 확인할 수 있어요.` }
  ];
  const ld = [placeLd(c), faqLd(faqs), crumbLd(c.city)];
  const sibLinks = siblings.map((s) => `<a href="${BASE}/fire-city/${SLUG[s.city] || encodeURIComponent(s.city)}/">${esc(s.city)}</a>`).join(' ');
  const body = `<h1>${esc(c.city)}에서 파이어하면? 월 생활비·필요 자산</h1>
<p>${esc(c.country)} · ${esc(c.blurb)}</p>
<div class="stat"><div><small>예상 월 생활비(1인)</small><b>약 ${eok(c.krw)}</b></div><div><small>연 생활비</small><b>약 ${eok(annual)}</b></div><div><small>4%룰 필요 자산</small><b>약 ${eok(required)}</b></div></div>
<a class="cta" href="${BASE}/#firetype">🌍 9문항으로 내 파이어 유형 + 맞는 도시 Top3 보기</a>
<h2>내 조건으로 정확히 계산하기</h2>
<p>위 필요 자산은 생활비만으로 잡은 추정이에요. 국민연금·건강보험료·세금·부업까지 반영한 <b>내 파이어 가능 나이</b>는 계산기로 확인하세요.</p>
<a class="cta" href="${BASE}/">🔥 내 파이어 나이 계산하기 (1분)</a>
<h2>${esc(c.city)} 파이어 FAQ</h2>
${faqs.map((f) => `<div class="faq"><h3 style="font-size:15px">${esc(f.q)}</h3><p style="color:#475569">${esc(f.a)}</p></div>`).join('')}
<h2>다른 도시와 비교</h2>
<div class="tags">${sibLinks} <a href="${BASE}/fire-city/">전체 도시 보기 →</a></div>`;
  const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${BASE}/fire-city/${slug}/"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:type" content="article"><meta name="theme-color" content="#ff5a00"><script type="application/ld+json">${JSON.stringify(ld)}</script><style>${CSS}</style></head><body><main>${body}<p class="note">※ 파이어맵은 정보 제공 서비스이며 투자자문이 아니에요. 생활비·필요자산은 통계·물가 기반 2026 추정치이며 실제와 다를 수 있어요.</p></main></body></html>`;
  return { slug, html, title, required };
}

const dir = join(ROOT, 'fire-city');
mkdirSync(dir, { recursive: true });
let n = 0;
const cards = [];
for (const c of TEST_CITIES) {
  const siblings = TEST_CITIES.filter((x) => x.dom === c.dom && x.city !== c.city).slice(0, 3);
  const { slug, html } = cityPage(c, siblings);
  mkdirSync(join(dir, slug), { recursive: true });
  writeFileSync(join(dir, slug, 'index.html'), html);
  cards.push(`<a class="card" href="${BASE}/fire-city/${slug}/"><b>${esc(c.flag)} ${esc(c.city)}</b><span>${esc(c.country)} · 월 ${eok(c.krw)}</span></a>`);
  n += 1;
}
// 허브
const hubBody = `<h1>도시별 파이어 살기 — 국내·해외 ${n}곳</h1>
<p>각 도시의 월 생활비와 4%룰 필요 자산을 한눈에. 나에게 맞는 도시는 <a href="${BASE}/#firetype">파이어 유형 테스트</a>로 찾아보세요.</p>
<div class="hubgrid">${cards.join('')}</div>`;
const hubCss = CSS + ".hubgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}.card{display:flex;flex-direction:column;border:1px solid #eee;border-radius:14px;background:#fff;padding:13px 15px;color:#18212c}.card b{font-size:15px}.card span{font-size:12px;color:#9aa3bf;margin-top:3px}";
const hub = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>도시별 파이어 살기 비용 — 국내·해외 ${n}곳 | 파이어맵</title><meta name="description" content="국내·해외 ${n}개 도시의 파이어 월 생활비와 4%룰 필요 자산을 비교. 나에게 맞는 도시는 파이어 유형 테스트로. 2026 기준 추정."><link rel="canonical" href="${BASE}/fire-city/"><meta property="og:title" content="도시별 파이어 살기 비용 — 국내·해외 ${n}곳"><meta name="theme-color" content="#ff5a00"><style>${hubCss}</style></head><body><main>${hubBody}<p class="note">※ 정보 제공 서비스이며 투자자문이 아니에요. 2026 추정치.</p></main></body></html>`;
writeFileSync(join(dir, 'index.html'), hub);
console.log(`[gen-city-fire] ${n} city pages + hub`);
