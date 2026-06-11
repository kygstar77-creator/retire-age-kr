import { useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, runwayText, deltaText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { FIRE_CITIES as CITIES } from '../../firemap-v2/cities.js';


export default function CityExplorer({ inputs, simulation, onChange, onMove, onBack }) {
  const [open, setOpen] = useState(null);
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
      <div className="fm-ce-grid">
        {CITIES.map((c, i) => {
          const sc = buildScenario(inputs, { monthlyLivingCost: c.krw });
          const isOpen = open === i;
          return (
            <article className="fm-ce-card" key={c.city}>
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
