import { TABS, screens } from '../../firemap-v2/screens.js';

export default function BottomTabs({ current, onMove }) {
  const activeTab = screens[current]?.tab;
  return (
    <nav className="fm-tabbar" aria-label="메뉴">
      {TABS.map((t) => {
        if (t.href) return <a key={t.id} href={t.href} className="fm-tab">{t.label}</a>;
        const active = activeTab === t.id;
        return (
          <button type="button" key={t.id} className={`fm-tab${active ? ' is-active' : ''}`} onClick={() => onMove(t.target)}>{t.label}</button>
        );
      })}
    </nav>
  );
}
