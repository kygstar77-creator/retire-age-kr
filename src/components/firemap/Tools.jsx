import Header from './Header.jsx';
import { TOOLS } from '../../firemap-v2/screens.js';

const ICONS = { experiment: '🎛️', dependent: '🩺', foreignTax: '🧾', dividend: '💵', pension: '🏦', cities: '📍', community: '💬' };
const GROUPS = [
  { label: '내 파이어 시뮬', ids: ['cities', 'experiment'] },
  { label: '은퇴 후 현금·세금·건보', ids: ['dividend', 'dependent', 'foreignTax', 'pension'] }
];
const byId = Object.fromEntries(TOOLS.map((t) => [t.id, t]));

export default function Tools({ onMove }) {
  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="도구" />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">정밀 도구</p>
        <h2>필요한 것만 골라서</h2>
        <p>핵심 계산 외 현금흐름·세금·건보료·지역 같은 정밀 도구를 여기서 확인해요.</p>
      </section>
      {GROUPS.map((g) => (
        <div key={g.label} className="fm-tool-group">
          <p className="fm-tool-group-label">{g.label}</p>
          <div className="fm-tool-grid">
            {g.ids.map((id) => {
              const t = byId[id];
              if (!t) return null;
              return (
                <button type="button" key={id} className="fm-tool-tile" onClick={() => onMove(id)}>
                  <span className="fm-tool-ico">{ICONS[id]}</span>
                  <strong>{t.title}</strong>
                  <em>{t.desc}</em>
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </main>
  );
}
