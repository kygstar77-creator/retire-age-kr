import { TABS, screens } from '../../firemap-v2/screens.js';

const ICONS = {
  home: 'M3 11.5 12 4l9 7.5M5 10v9h5v-5h4v5h5v-9',
  tools: 'M4 5h6v6H4zM14 5h6v6h-6zM4 15h6v6H4zM14 15h6v6h-6z',
  guide: 'M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 0-3 3zM5 4v16'
};

export default function BottomTabs({ current, onMove }) {
  const activeTab = screens[current]?.tab;
  return (
    <nav className="fm-tabbar" aria-label="메뉴">
      {TABS.map((t) => {
        const icon = <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={ICONS[t.id]} /></svg>;
        if (t.href) return <a key={t.id} href={t.href} className="fm-tab">{icon}<span>{t.label}</span></a>;
        const active = activeTab === t.id;
        return <button type="button" key={t.id} className={`fm-tab${active ? ' is-active' : ''}`} onClick={() => onMove(t.target)}>{icon}<span>{t.label}</span></button>;
      })}
    </nav>
  );
}
