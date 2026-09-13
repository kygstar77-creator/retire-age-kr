import { TABS, screens } from '../../firemap-v2/screens.js';

const ICONS = {
  // 결과 = 도달한 깃발 · 바꿔보기 = 조절 손잡이 · 랭킹 = 트로피 · 전체 = 목록
  result: 'M6 21V4M6 4h11l-2.2 3.6L17 11H6',
  experiment: 'M4 7h9m3 0h4M4 17h4m3 0h9M13 4.5v5M8 14.5v5',
  ranking: 'M8 21h8M12 17v4M6 4h12v5a6 6 0 0 1-12 0zM6 6H3.5v1A3.5 3.5 0 0 0 7 11M18 6h2.5v1A3.5 3.5 0 0 1 17 11',
  menu: 'M4 6h16M4 12h16M4 18h16'
};

// 하단 탭 4 — 결과·바꿔보기·랭킹·전체. DS 클래스만 사용.
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
