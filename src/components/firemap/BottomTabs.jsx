import { TABS, screens } from '../../firemap-v2/screens.js';

const ICONS = {
  home: 'M3 11.5 12 4l9 7.5M5 10v9h5v-5h4v5h5v-9',
  tools: 'M4 5h6v6H4zM14 5h6v6h-6zM4 15h6v6H4zM14 15h6v6h-6z',
  menu: 'M4 6h16M4 12h16M4 18h16',
  save: 'M5 9h14l-1 9a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2zM9 9V6a3 3 0 0 1 6 0v3M12 13v3',
  ranking: 'M8 21h8M12 17v4M6 4h12v5a6 6 0 0 1-12 0zM6 6H3.5v1A3.5 3.5 0 0 0 7 11M18 6h2.5v1A3.5 3.5 0 0 1 17 11',
  community: 'M17 20v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M10 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M21 20v-1a4 4 0 0 0-3-3.86M16 4.14a4 4 0 0 1 0 7.72',
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
