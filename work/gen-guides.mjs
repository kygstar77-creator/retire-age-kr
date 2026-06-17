import { mkdirSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// 빌드타임 백과 생성기 — 지역/체류지별 파이어 가이드를 대량 생성. gen-seo 직전에 실행되어 sitemap 자동 포함.
const ROOT = process.env.GUIDE_OUT || 'outputs/deploy';
const OUT = join(ROOT, 'guide', 'regions');
const BASE = 'https://firemap.kr';

// 1인 월 생활비(주거 포함) 추정 — tier 기준(원). 통계청 1인가구 평균 + 지역 물가 참고.
const TIER_COST = { 1: 2050000, 2: 1600000, 3: 1350000, 4: 1200000, 5: 1000000 };
const TIER_LABEL = { 1: '전국 최고 비용', 2: '대도시·수도권', 3: '지방 중소도시', 4: '지방 소도시', 5: '군 단위·읍면' };

// [이름, 시도, tier]
const REGIONS = [
  ['서울','서울',1],['인천','인천',2],['수원','경기',2],['성남','경기',2],['고양','경기',2],['용인','경기',2],['부천','경기',2],['안산','경기',3],['안양','경기',2],['남양주','경기',3],['화성','경기',2],['평택','경기',3],['의정부','경기',3],['시흥','경기',3],['파주','경기',3],['김포','경기',3],['광명','경기',2],['군포','경기',3],['하남','경기',2],['오산','경기',3],['이천','경기',3],['안성','경기',4],['구리','경기',2],['포천','경기',4],['여주','경기',4],['양평','경기',4],['가평','경기',5],
  ['부산','부산',2],['대구','대구',2],['광주','광주',2],['대전','대전',2],['울산','울산',2],['세종','세종',2],
  ['춘천','강원',3],['원주','강원',3],['강릉','강원',3],['동해','강원',4],['속초','강원',3],['삼척','강원',4],['홍천','강원',5],['평창','강원',5],['정선','강원',5],['영월','강원',5],
  ['청주','충북',3],['충주','충북',4],['제천','충북',4],['음성','충북',4],['진천','충북',4],['단양','충북',5],['괴산','충북',5],
  ['천안','충남',3],['아산','충남',3],['서산','충남',4],['당진','충남',4],['논산','충남',4],['공주','충남',4],['보령','충남',4],['홍성','충남',4],['예산','충남',5],
  ['전주','전북',3],['익산','전북',4],['군산','전북',4],['정읍','전북',5],['남원','전북',5],['김제','전북',5],['고창','전북',5],['완주','전북',4],
  ['여수','전남',3],['순천','전남',3],['목포','전남',4],['광양','전남',4],['나주','전남',4],['무안','전남',5],['해남','전남',5],['완도','전남',5],['보성','전남',5],
  ['포항','경북',3],['구미','경북',3],['경주','경북',4],['안동','경북',4],['김천','경북',4],['영주','경북',4],['상주','경북',5],['문경','경북',5],['칠곡','경북',5],['울릉','경북',5],
  ['창원','경남',3],['김해','경남',3],['진주','경남',3],['양산','경남',3],['거제','경남',4],['통영','경남',4],['사천','경남',4],['밀양','경남',5],['남해','경남',5],['하동','경남',5],['거창','경남',5],
  ['제주시','제주',3],['서귀포','제주',3]
];

const OVERSEAS = [
  ['치앙마이','태국','🇹🇭',2200000,'카페·코워킹과 사원, 산이 공존하는 디지털 노마드의 성지','관광·교육·O-A 비자 옵션, 민간 의료보험 권장, 건기 11~2월 쿾적'],
  ['다낭','베트남','🇻🇳',2300000,'긴 해변과 따뜻한 날씨, 낮은 물가로 시작하기 좋은 해외살이','관광·거주 옵션, 사보험 필요, 우기 9~12월 유의'],
  ['우봇(발리)','인도네시아','🇮🇩',2300000,'논뱭과 요가, 자연 속 힐링형 라이프','관광·B211 등 장기 옵션, 사보험 필요, 우기 11~3월'],
  ['쿠알라룼푸르','말레이시아','🇲🇾',2900000,'대도시 인프라와 영어 생활권, 든든한 의료','MM2H 등 장기 옵션, 의료 양호, 연중 고온다습'],
  ['트빌리시','조지아','🇬🇪',2000000,'초저비용과 관대한 체류 조건, 와인·온천의 숨은 성지','다수 국적 1년 무비자 체류(확인 필요), 물가 매우 저렴'],
  ['리스본','포르투갈','🇵🇹',3800000,'온화한 유럽, 해산물과 골목의 낭만형','유럽 장기 비자 옵션(요건 까다로움), 물가 서유럽 중 낮은 편'],
  ['후쿠오카','일본','🇯🇵',3300000,'한국과 가깝고 음식·치안 최고, 도시와 자연이 가까움','관광·장기 비자 옵션, 의료·치안 우수, 가까운 거리'],
  ['방콕','태국','🇹🇭',2700000,'없는 게 없는 대도시와 저렴한 외식, 의료 관광 허브','관광·장기 비자 옵션, 사보험 권장, 연중 무더위'],
  ['호치민','베트남','🇻🇳',2200000,'활기차 거리와 초저비용, 빠르게 크는 노마드 도시','관광·거주 옵션, 사보험 필요, 우기 5~10월'],
  ['페낭','말레이시아','🇲🇾',2400000,'음식의 천국과 영어 생활권, 저렴한 의료의 섬','MM2H 등 장기 옵션, 의료 양호, 고온다습'],
  ['세부','필리핀','🇵🇭',2100000,'에메랄드 바다와 다이빙, 영어 통하는 저비용 휴양','관광 연장·SRRV 옵션, 사보험 필요, 우기 유의'],
  ['타이베이','대만','🇹🇼',3000000,'한국과 가깝고 치안·교통·야시장이 강한 도시형','관광·장기 옵션, 의료·치안 우수, 습한 기후'],
  ['포르투','포르투갈','🇵🇹',3200000,'리스본보다 저렴한 유럽, 와인과 강변의 낭만','유럽 장기 비자 옵션(요건 까다로움), 온화한 기후'],
  ['메데인','콜롬비아','🇨🇴',2000000,'“영원한 봄의 도시”, 초저비용과 노마드 커뮤니티','관광·노마드 비자 옵션, 사보험 필요, 치안 지역 확인']
];

const won = (n) => { const m = Math.round(n/10000); return m>=10000?`${(m/10000).toFixed(1)}억`:`${m.toLocaleString()}만원`; };
const slugify = (s) => s.replace(/[()]/g,'').replace(/[^가-힣a-zA-Z0-9]/g,'-');
const esc = (s) => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

const CSS = "body{margin:0;background:#fffdf9;color:#18212c;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7}main{max-width:760px;margin:0 auto;padding:28px 20px 80px}h1{font-size:28px;letter-spacing:-.04em;line-height:1.3}h2{margin-top:28px;font-size:19px}a{color:#ea580c;font-weight:700;text-decoration:none}.box{border:1px solid #eee;border-radius:18px;background:#fff;padding:16px 18px;margin:16px 0}.stat{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0}.stat div{flex:1;min-width:120px;background:#fff;border:1px solid #eee;border-radius:14px;padding:12px 14px}.stat small{color:#9aa3bf;font-weight:700;font-size:12px}.stat b{display:block;font-size:20px;margin-top:3px}.cta{display:block;text-align:center;background:linear-gradient(180deg,#ff6a35,#ee4a1f);color:#fff;border-radius:14px;padding:14px;font-weight:800;margin:22px 0}.tags a{display:inline-block;background:#fff;border:1px solid #eee;border-radius:999px;padding:6px 12px;margin:4px 6px 0 0;font-size:13px;color:#555}.note{color:#9aa3bf;font-size:12px;line-height:1.6}";

function page({ title, desc, body, canonical }) {
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${canonical}"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:type" content="article"><meta name="theme-color" content="#ff5a00"><script type="application/ld+json">${JSON.stringify({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"inLanguage":"ko-KR","isPartOf":{"@type":"WebSite","name":"파이어맵","url":BASE},"publisher":{"@type":"Organization","name":"파이어맵"}})}</script><style>${CSS}</style></head><body><main>${body}<p class="note">※ 파이어맵은 정보 제공 서비스이며 투자자문이 아니에요. 생활비·필요자산은 일반 통계·물가 기반 추정치이며, 실제 파이어 시점은 자산·국민연금·세금·건강보험료에 따라 달라져요 — <a href="${BASE}/">계산기로 내 수치 보기</a>.</p></main></body></html>`;
}

function regionPage(name, sido, tier) {
  const monthly = TIER_COST[tier];
  const annual = monthly*12;
  const ref25 = annual*25;
  const peers = REGIONS.filter(r=>r[1]===sido && r[0]!==name).slice(0,6);
  const title = `${name} 파이어 생활비·필요자산 (${sido}) | 파이어맵`;
  const desc = `${name}에서 파이어(조기은퇴)하려면? 1인 월 생활비 ${won(monthly)} 기준 연 생활비와 단순 참고 필요자산, 장단점, 주거 팁.`;
  const body = `<p><a href="${BASE}/guide/regions/">← 지역별 파이어 백과</a></p>
  <h1>${name}에서 파이어하려면?</h1>
  <p>${name}(${sido})은 ${TIER_LABEL[tier]} 지역으로, 1인 가구 기준 주거를 포함한 월 생활비는 약 <b>${won(monthly)}</b>으로 추정돼요. 파이어는 결국 “생활비를 자산이 감당하느냐”의 문제라, 사는 곳의 생활비가 파이어 시점을 크게 좌우해요.</p>
  <div class="stat"><div><small>1인 월 생활비(추정)</small><b>${won(monthly)}</b></div><div><small>연 생활비</small><b>${won(annual)}</b></div><div><small>단순 참고 필요자산</small><b>${won(ref25)}</b></div></div>
  <p class="note">※ ‘단순 참고 필요자산’은 연 생활비×25의 일반적 참고치예요. 실제로는 국민연금·임대·배당·세금·건강보험료가 더해져 더 적게도, 더 많이도 필요해요. 정확한 값은 계산기에서 확인하세요.</p>
  <h2>${name} 파이어의 장점</h2>
  <p>${tier>=3?`수도권 대비 주거비가 낮아 같은 자산으로도 파이어 시점이 빨라질 수 있어요. 생활비를 ${won(2050000-monthly)} 아끼면 그만큼 필요자산이 줄어들어요.`:`인프라·의료·교통이 잘 갖춰져 파이어 후에도 생활 편의가 높아요. 다만 주거비가 높아 필요자산이 커지는 편이에요.`}</p>
  <h2>주거 팁</h2>
  <p>${tier>=4?'월세·전세 모두 수도권보다 크게 저렴해 고정비를 줄이기 좋아요. 다만 일자리·병원 접근성을 미리 확인하세요.':tier===3?'역세권을 조금 벗어나면 주거비를 더 낮출 수 있어요. 자차 여부에 따라 체감 비용이 달라져요.':'주거비 비중이 커서, 평수를 줄이거나 외곽으로 이동하면 필요자산이 눈에 띄게 줄어요.'}</p>
  ${peers.length?`<h2>${sido}의 다른 지역</h2><div class="tags">${peers.map(p=>`<a href="${BASE}/guide/regions/${slugify(p[0])}.html">${p[0]} 생활비</a>`).join('')}</div>`:''}
  <a class="cta" href="${BASE}/">${name} 생활비로 내 파이어 나이 계산하기 →</a>`;
  return page({ title, desc, body, canonical: `${BASE}/guide/regions/${slugify(name)}.html` });
}

function overseasPage(name, country, flag, monthly, vibe, visa) {
  const annual = monthly*12, ref25 = annual*25;
  const title = `${name} 파이어 한 달 살기·생활비 (${country}) | 파이어맵`;
  const desc = `${flag} ${name}(${country}) 파이어/한 달 살기 생활비 약 ${won(monthly)}. ${vibe}`;
  const body = `<p><a href="${BASE}/guide/regions/">← 지역별 파이어 백과</a></p>
  <h1>${flag} ${name}에서 파이어 한 달 살기</h1>
  <p>${vibe}. 1인 기준 월 생활비는 약 <b>${won(monthly)}</b> 수준으로 추정돼요(환율·생활 방식에 따라 변동).</p>
  <div class="stat"><div><small>월 생활비(추정)</small><b>${won(monthly)}</b></div><div><small>연 생활비</small><b>${won(annual)}</b></div><div><small>단순 참고 필요자산</small><b>${won(ref25)}</b></div></div>
  <h2>비자·체류</h2><p>${visa}.</p>
  <h2>파이어 관점</h2><p>물가가 낮은 해외에서 일정 기간 체류하면 같은 자산으로 자산 수명이 늘어, 파이어 시점을 앞당기거나 인출 부담을 줄일 수 있어요. 단, 건강보험·세금·환율 변동을 함께 고려해야 해요.</p>
  <a class="cta" href="${BASE}/">해외 체류를 반영해 내 파이어 계산하기 →</a>`;
  return page({ title, desc, body, canonical: `${BASE}/guide/regions/${slugify(name)}.html` });
}

if (!existsSync(ROOT)) { console.log(`[gen-guides] ROOT ${ROOT} 없음 — 건너뜀`); process.exit(0); }
mkdirSync(OUT, { recursive: true });

let n = 0;
for (const [name, sido, tier] of REGIONS) { writeFileSync(join(OUT, `${slugify(name)}.html`), regionPage(name, sido, tier)); n++; }
for (const [name, country, flag, cost, vibe, visa] of OVERSEAS) { writeFileSync(join(OUT, `${slugify(name)}.html`), overseasPage(name, country, flag, cost, vibe, visa)); n++; }

const bySido = {};
for (const [name, sido] of REGIONS) { (bySido[sido] ||= []).push(name); }
const hub = `<p><a href="${BASE}/">← 파이어맵</a></p><h1>지역별 파이어 백과</h1><p>사는 곳에 따라 파이어 시점이 달라져요. 국내 ${REGIONS.length}개 지역과 해외 ${OVERSEAS.length}개 체류지의 생활비·필요자산을 정리했어요.</p>` +
  Object.entries(bySido).map(([s,arr])=>`<h2>${s}</h2><div class="tags">${arr.map(nm=>`<a href="${BASE}/guide/regions/${slugify(nm)}.html">${nm}</a>`).join('')}</div>`).join('') +
  `<h2>해외 체류지</h2><div class="tags">${OVERSEAS.map(o=>`<a href="${BASE}/guide/regions/${slugify(o[0])}.html">${o[2]} ${o[0]}</a>`).join('')}</div><a class="cta" href="${BASE}/">내 파이어 나이 계산하기 →</a>`;
writeFileSync(join(OUT, 'index.html'), page({ title: '지역별 파이어 백과 — 도시별 생활비·필요자산 | 파이어맵', desc: `국내 ${REGIONS.length}개 지역·해외 ${OVERSEAS.length}개 체류지의 파이어 생활비와 필요자산 가이드.`, body: hub, canonical: `${BASE}/guide/regions/` }));
n++;
console.log(`[gen-guides] ${n} pages → ${OUT}`);
