import { TABS, screens } from '../../firemap-v2/screens.js';

const ICONS = {
  home: 'M3 11.5 12 4l9 7.5M5 10v9h5v-5h4v5h5v-9',
  save: 'M5 9h14l-1 9a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2zM9 9V6a3 3 0 0 1 6 0v3M12 13v3',
  ranking: 'M8 21h8M12 17v4M6 4h12v5a6 6 0 0 1-12 0zM6 6H3.5v1A3.5 3.5 0 0 0 7 11M18 6h2.5v1A3.5 3.5 0 0 1 17 11',
  menu: 'M4 6h16M4 12h16M4 18h16'
};

// 하단 탭 4 — 오늘·저축·랭킹·전체 (6차 결정: 케이뱅크·M3 문법). DS 클래스만 사용.
export default function BottomTabs({ current, onMove }) {
  const activeTab = screens[current]?.tab;
  return (
    <nav className="ds-tabbar" aria-label="메뉴">
      {TABS.map((t) => (
        <button type="button" key={t.id} className="ds-tabbar__tab" aria-current={activeTab === t.id ? 'page' : undefined} onClick={() => onMove(t.target)}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={ICONS[t.id]} /></svg>
          <span>{t.label}</span>
        </button>
      ))}
    </nav>
  );
}
