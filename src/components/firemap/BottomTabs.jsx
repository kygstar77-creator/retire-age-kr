import { Icon } from '../../ui/index.js';
import { TABS, screens } from '../../firemap-v2/screens.js';

const ICONS = { result: 'flag', experiment: 'sliders', ranking: 'trophy', menu: 'menu' };

// 하단 탭 4 — 결과·바꿔보기·랭킹·전체. DS 클래스만 사용.
export default function BottomTabs({ current, onMove }) {
  const activeTab = screens[current]?.tab;
  return (
    <nav className="ds-tabbar" aria-label="메뉴">
      {TABS.map((t) => (
        <button type="button" key={t.id} className="ds-tabbar__tab" aria-current={activeTab === t.id ? 'page' : undefined} onClick={() => onMove(t.target)}>
          <Icon name={ICONS[t.id]} size={22} />
          <span>{t.label}</span>
        </button>
      ))}
    </nav>
  );
}
