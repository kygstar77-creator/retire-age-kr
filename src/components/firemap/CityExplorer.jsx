import { useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, runwayText, deltaText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { FIRE_CITIES as CITIES } from '../../firemap-v2/cities.js';


const CONTINENTS = [
  '15,30 40,22 85,20 120,30 125,42 100,65 80,72 60,60 50,40',
  '100,82 120,85 145,95 140,115 125,130 110,145 108,120',
  '170,54 180,47 195,52 210,45 220,30 205,20 185,30 170,40',
  '163,76 190,55 213,58 230,78 220,100 200,125 192,110 170,85',
  '220,50 240,35 270,22 320,22 330,45 300,70 275,82 250,65 225,60',
  '293,102 310,102 333,118 325,129 300,125 293,112'
];
function WorldMap({ cities, active, onPick }) {
  return (
    <div className="fm-wm">
      <svg viewBox="0 0 360 180" preserveAspectRatio="xMidYMid meet" role="img" aria-label="전세계 파이어 도시 지도">
        <rect x="0" y="0" width="360" height="180" rx="10" fill="#eef4fb" />
        {CONTINENTS.map((pts, i) => <polygon key={i} points={pts} fill="#d7e3f0" />)}
        {cities.map((c, i) => {
          if (c.lat == null || c.lon == null) return null;
          const x = c.lon + 180, y = 90 - c.lat;
          return (
            <g key={c.city} className={`fm-wm-pin${active === i ? ' on' : ''}`} onClick={() => onPick(i)} style={{ cursor: 'pointer' }}>
              <circle cx={x} cy={y} r={active === i ? 6 : 4} />
              {active === i && <text x={x} y={y - 8} textAnchor="middle" className="fm-wm-lbl">{c.city}</text>}
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
