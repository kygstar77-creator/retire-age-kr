import { useState, useEffect } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, runwayText, deltaText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { FIRE_CITIES as CITIES } from '../../firemap-v2/cities.js';


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
function WorldMap({ cities, active, onPick }) {
  const [land, setLand] = useState(null);
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
        const geo = topojson.feature(topo, topo.objects.countries);
        const paths = geo.features.map((f) => {
          const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
          let d = '';
          polys.forEach((poly) => poly.forEach((ring) => {
            ring.forEach((pt, i) => { const [x, y] = proj(pt[0], pt[1]); d += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); });
            d += 'Z';
          }));
          return d;
        });
        if (alive) setLand(paths);
      } catch { /* CDN 실패 시 폴백 유지 */ }
    })();
    return () => { alive = false; };
  }, []);
  const drawn = land || LAND;
  return (
    <div className="fm-wm">
      <svg viewBox="0 0 360 180" preserveAspectRatio="xMidYMid meet" role="img" aria-label="전세계 파이어 도시 지도">
        <rect x="0" y="0" width="360" height="180" rx="10" fill="#dbeafe" />
        {drawn.map((d, i) => <path key={i} d={d} fill="#eef6ee" stroke="#cbd5e1" strokeWidth="0.3" />)}
        {cities.map((c, i) => {
          if (c.lat == null || c.lon == null) return null;
          const [x, y] = proj(c.lon, c.lat);
          return (
            <g key={c.city} className={`fm-wm-pin${active === i ? ' on' : ''}`} onClick={() => onPick(i)} style={{ cursor: 'pointer' }}>
              <circle cx={x} cy={y} r={active === i ? 5 : 3} />
              {active === i && <text x={x} y={y - 6} textAnchor="middle" className="fm-wm-lbl">{c.city}</text>}
            </g>
          );
        })}
      </svg>
      <p className="fm-wm-hint">지도의 점을 눌러 도시를 골라보세요</p>
    </div>
  );
}

export default function CityExplorer({ inputs, simulation, onChange, onMove, onBack }) {
  const [open, setOpen] = useState(null);
  const [active, setActive] = useState(null);
  const pick = (i) => { setActive(i); const el = document.getElementById(`ce-${i}`); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' }); };
  const apply = (krw) => {
    if (onChange) onChange('monthlyLivingCost', krw);
    if (onMove) onMove('result');
  };
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="해외 도시" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">파이어하면 어디서 살까</p>
        <h2>전 세계 파이어 도시 탐색</h2>
        <p>도시를 골라 "이 생활비로 살면 내 자산이 몇 살까지 버티는지" 바로 계산해 보세요. 파이어 후의 하루를 미리 그려보는 거예요.</p>
      </section>
      <WorldMap cities={CITIES} active={active} onPick={pick} />
      <div className="fm-ce-grid">
        {CITIES.map((c, i) => {
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
                  {c.play.map((p) => <span key={p} className="fm-ce-tag play">📍 {p}</span>)}
                </div>
                <p className="fm-ce-run">이 생활비면 <b>{runwayText(sc)}</b>까지 버텨요 · {deltaText(simulation, sc)}</p>
                {isOpen && <p className="fm-ce-visa">{c.visa}</p>}
                <button type="button" className="fm-ce-cta" onClick={() => apply(c.krw)}>이 도시로 내 결과 보기</button>
              </div>
            </article>
          );
        })}
      </div>
      <p className="fm-ce-note">도시별 금액은 1인 월 생활비 대략 추정치예요. 실제 주거·의료·환율·비자 조건에 따라 달라질 수 있어요. {sourceLine('cityCost')}</p>
    </main>
  );
}
