import Header from './Header.jsx';
import { TOOLS } from '../../firemap-v2/screens.js';

export default function Tools({ onMove }) {
  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="도구" />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">정밀 도구</p>
        <h2>필요한 것만 골라서</h2>
        <p>핵심 계산 외 세금·건보료·도시·커뮤니티는 여기서 따로 확인해요.</p>
      </section>
      <div className="fm-tool-list">
        {TOOLS.map((t) => (
          <button type="button" key={t.id} className="fm-tool-card" onClick={() => onMove(t.id)}>
            <em>{t.tag}</em>
            <strong>{t.title}</strong>
            <span>{t.desc}</span>
          </button>
        ))}
      </div>
    </main>
  );
}
