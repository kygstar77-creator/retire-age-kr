import { useState, useEffect } from 'react';
import Header from './Header.jsx';
import { OverseasStayModule } from './City.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, runwayText, deltaText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { FIRE_CITIES as CITIES, KR_REGIONS } from '../../firemap-v2/cities.js';


const LAND = [
  'M18 30 L60 18 L95 16 L120 24 L126 40 L112 50 L100 56 L99 66 L86 64 L75 72 L68 64 L57 52 L55 42 L40 32 Z',
  'M100 84 L118 86 L145 96 L142 112 L128 130 L113 148 L110 130 L108 105 Z',
  'M165 76 L178 60 L200 58 L215 60 L222 78 L218 95 L210 120 L200 124 L190 112 L188 95 L170 84 Z',
  'M172 50 L168 44 L180 40 L190 34 L205 26 L215 36 L205 46 L195 50 L182 52 Z',
  'M215 36 L235 26 L270 20 L305 24 L320 40 L312 52 L300 60 L290 70 L278 78 L262 74 L258 88 L250 74 L240 70 L230 66 L222 58 L215 50 Z',
  'M295 100 L315 100 L333 110 L328 128 L305 126 L295 112 Z',
  'M138 16 L150 18 L148 30 L135 28 Z',
  'M313 52 L318 54 L316 60 L312 58 Z',
  'M173 41 L177 41 L176 46 L172 45 Z',
  'M226 108 L230 110 L229 117 L225 115 Z',
  'M283 96 L300 95 L302 99 L285 100 Z'
];
function ringContains(lon, lat, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
    if (((yi > lat) !== (yj > lat)) && (lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi)) inside = !inside;
  }
  return inside;
}
const featPolys = (f) => (f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates);
function bboxOf(f) {
  let a = 180, b = 90, c = -180, d = -90;
  featPolys(f).forEach((poly) => poly[0].forEach(([x, y]) => { if (x < a) a = x; if (y < b) b = y; if (x > c) c = x; if (y > d) d = y; }));
  return [a, b, c, d];
}

function WorldMap({ cities, active, onPick }) {
  const [dots, setDots] = useState(null);
  const W = 360, H = 180;
  const proj = (lon, lat) => [((lon + 180) / 360) * W, ((90 - lat) / 180) * H];
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [topo, topojson] = await Promise.all([
          fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then((r) => r.json()),
          import('https://esm.sh/topojson-client@3')
        ]);
        const feats = topojson.feature(topo, topo.objects.countries).features.map((f) => ({ f, bbox: bboxOf(f) }));
        const ds = [];
        for (let lat = 78; lat >= -56; lat -= 2.4) {
          for (let lon = -180; lon < 180; lon += 2.4) {
            for (const { f, bbox } of feats) {
              if (lon >= bbox[0] && lon <= bbox[2] && lat >= bbox[1] && lat <= bbox[3]) {
                let hit = false;
                for (const poly of featPolys(f)) { if (ringContains(lon, lat, poly[0])) { hit = true; break; } }
                if (hit) { const [x, y] = proj(lon, lat); ds.push(x.toFixed(1) + ',' + y.toFixed(1)); break; }
              }
            }
          }
        }
        if (alive) setDots(ds);
      } catch { /* 폴백: 윤곽 */ }
    })();
    return () => { alive = false; };
  }, []);
  return (
    <div className="fm-wm">
      <svg viewBox="0 0 360 180" preserveAspectRatio="xMidYMid meet" role="img" aria-label="전세계 파이어 도시 지도">
        <rect x="0" y="0" width="360" height="180" rx="12" fill="#0f1830" />
        {dots
          ? dots.map((xy, i) => { const [x, y] = xy.split(','); return <circle key={i} cx={x} cy={y} r="0.85" fill="#3b4a6b" />; })
          : LAND.map((d, i) => <path key={i} d={d} fill="#26324f" stroke="#3b4a6b" strokeWidth="0.3" />)}
        {cities.map((c, i) => {
          if (c.lat == null || c.lon == null) return null;
          const [x, y] = proj(c.lon, c.lat);
          return (
            <g key={c.city} className={`fm-wm-pin${active === i ? ' on' : ''}`} onClick={() => onPick(i)} style={{ cursor: 'pointer' }}>
              {active === i && <circle cx={x} cy={y} r="6" className="fm-wm-halo" />}
              <circle cx={x} cy={y} r={active === i ? 3.2 : 2.4} />
              {active === i && <text x={x} y={y - 6} textAnchor="middle" className="fm-wm-lbl">{c.city}</text>}
            </g>
          );
        })}
      </svg>
      <p className="fm-wm-hint">지도의 점을 눌러 도시를 골라보세요</p>
    </div>
  );
}

export default function CityExplorer({ inputs, simulation, onChange, onMove, onBack, onPreviewCity }) {
  const [tab, setTab] = useState('domestic');
  const [open, setOpen] = useState(null);
  const [active, setActive] = useState(null);
  const pick = (i) => { setActive(i); const el = document.getElementById(`ce-${i}`); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' }); };
  // 적용 = 미리보기 샌드박스로만(기존 저장 무손상).
  const apply = (krw) => { if (onPreviewCity) { onPreviewCity(krw); return; } if (onMove) onMove('result'); };

  const curCost = Number(inputs.monthlyLivingCost) || 0;
  const curAge = simulation.earliestRetirementAge;
  const overseas = CITIES.filter((c) => c.country !== '한국');

  const regions = KR_REGIONS
    .map((r) => ({ ...r, age: buildScenario(inputs, { monthlyLivingCost: r.krw }).earliestRetirementAge }))
    .sort((a, b) => {
      const aa = a.age == null ? 999 : a.age;
      const bb = b.age == null ? 999 : b.age;
      return aa !== bb ? aa - bb : a.krw - b.krw;
    });

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="지역 탐색" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">어디서 살까</p>
        <h2>지역 바꾸면 파이어가 당겨져요</h2>
        <p>생활비 낮은 곳으로 옮기면 같은 자산으로 더 일찍·더 오래 파이어할 수 있어요. 지역을 골라 바로 계산해 보세요.</p>
      </section>

      <div className="fm-scope-toggle fm-region-tabs">
        <button type="button" className={tab === 'domestic' ? 'on' : ''} onClick={() => setTab('domestic')}>🇰🇷 국내</button>
        <button type="button" className={tab === 'overseas' ? 'on' : ''} onClick={() => setTab('overseas')}>🌏 해외</button>
      </div>

      {tab === 'domestic' ? (
        <>
          {curAge != null && <p className="fm-region-base">지금 생활비 <b>월 {formatWon(curCost)}</b> 기준 <b>{curAge}세 파이어</b> · 지역 바꾸면 ↓</p>}
          <section className="fm-card fm-region-list">
            {regions.map((r) => {
              const delta = (curAge != null && r.age != null) ? curAge - r.age : null;
              return (
                <button type="button" className="fm-region-row" key={r.city} onClick={() => apply(r.krw)}>
                  <span className="fm-region-main"><b>{r.city}</b><em>월 {formatWon(r.krw)}{r.note ? ` · ${r.note}` : ''}</em></span>
                  <span className="fm-region-res">
                    <b>{r.age != null ? `${r.age}세` : '자산 부족'}</b>
                    {delta != null && <em className={delta > 0 ? 'early' : delta < 0 ? 'late' : 'same'}>{delta > 0 ? `${delta}년 일찍` : delta < 0 ? `${-delta}년 늦음` : '비슷'}</em>}
                  </span>
                </button>
              );
            })}
          </section>
          <p className="fm-ce-note">1인 월 생활비(주거 포함) 추정치 · 통계청 1인가구(월평균 약 169만)+지역 물가 참고. 실제는 주거·의료 조건에 따라 달라져요. {sourceLine('cityCost')}</p>
        </>
      ) : (
        <>
          <WorldMap cities={overseas} active={active} onPick={pick} />
          <div className="fm-ce-grid">
            {overseas.map((c, i) => {
              const sc = buildScenario(inputs, { monthlyLivingCost: c.krw });
              const isOpen = open === i;
              return (
                <article className={`fm-ce-card${active === i ? ' active' : ''}`} id={`ce-${i}`} key={c.city}>
                  <button type="button" className="fm-ce-head" style={{ background: `linear-gradient(135deg, ${c.c1}, ${c.c2})` }} onClick={() => setOpen(isOpen ? null : i)}>
                    <span className="fm-ce-flag">{c.flag}</span>
                    <span className="fm-ce-name"><b>{c.city}</b><em>{c.country}</em></span>
                    <span className="fm-ce-cost">월 {formatWon(c.krw)}</span>
                  </button>
                  <div className="fm-ce-body">
                    <p className="fm-ce-vibe">{c.vibe}</p>
                    <div className="fm-ce-tags">
                      {c.food.map((f) => <span key={f} className="fm-ce-tag food">🍽 {f}</span>)}
                      {c.play.map((pl) => <span key={pl} className="fm-ce-tag play">📍 {pl}</span>)}
                    </div>
                    <p className="fm-ce-run">이 생활비면 <b>{runwayText(sc)}</b>까지 버텨요 · {deltaText(simulation, sc)}</p>
                    {isOpen && <p className="fm-ce-visa">{c.visa}</p>}
                    <button type="button" className="fm-ce-cta" onClick={() => apply(c.krw)}>이 도시로 미리보기</button>
                  </div>
                </article>
              );
            })}
          </div>
          {onChange && <OverseasStayModule inputs={inputs} simulation={simulation} onChange={onChange} />}
          <p className="fm-ce-note">도시별 금액은 1인 월 생활비 대략 추정치예요. 실제 주거·의료·환율·비자 조건에 따라 달라질 수 있어요. {sourceLine('cityCost')}</p>
        </>
      )}

      <section className="fm-card" style={{ marginTop: 14 }}>
        <p className="fm-kicker">더 깊이 보기</p>
        <a href="/guide/region-plan/" style={CE.guideRow}>
          <span style={CE.guideIco}>🏘️</span>
          <span style={CE.guideTx}><b style={CE.guideTitle}>지역·가구별 필요자산 사례</b><em style={CE.guideDesc}>지역×가구×유형별 필요자산 자료</em></span>
          <span style={CE.guideGo}>›</span>
        </a>
        <a href="/guide/regions/" style={{ ...CE.guideRow, borderBottom: 0 }}>
          <span style={CE.guideIco}>🏙️</span>
          <span style={CE.guideTx}><b style={CE.guideTitle}>도시별 생활비·집값</b><em style={CE.guideDesc}>생활비·실거래가·물가 자료</em></span>
          <span style={CE.guideGo}>›</span>
        </a>
      </section>
    </main>
  );
}

const CE = {
  guideRow: { display: 'flex', alignItems: 'center', gap: 12, width: '100%', textDecoration: 'none', borderBottom: '1px solid #f3f1ee', padding: '12px 2px' },
  guideIco: { fontSize: 19, flex: '0 0 auto', width: 24, textAlign: 'center' },
  guideTx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, gap: 2 },
  guideTitle: { fontSize: 14, fontWeight: 700, color: '#15151b', lineHeight: 1.3 },
  guideDesc: { fontSize: 11.5, fontWeight: 500, color: '#8a8f99', fontStyle: 'normal', lineHeight: 1.4 },
  guideGo: { fontSize: 18, color: '#c2c7d0', fontWeight: 700, flex: '0 0 auto' }
};
