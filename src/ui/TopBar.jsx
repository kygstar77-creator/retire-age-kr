// DS-16 TopBar — 화면 상단 1층. 로고(또는 ← 뒤로) · 제목 · 우측 액션. 3층(Header+LiveBanner+IdentityLine)을 대체.
import { IconButton } from './Button.jsx';

const Logo = () => (
  <svg className="ds-topbar__mark" viewBox="118 84 276 276" width="22" height="22" aria-hidden="true">
    <path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00" />
    <path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74" />
  </svg>
);

// title: 화면 제목(없으면 로고+파이어맵) · onBack: ← · actions: 우측 노드 배열 · sticky(기본 true)
export function TopBar({ title, onBack, onHome, actions, sticky = true, className = '' }) {
  return (
    <header className={`ds-topbar ${sticky ? 'ds-topbar--sticky' : ''} ${className}`}>
      <div className="ds-topbar__side">
        {onBack
          ? <IconButton label="이전" plain onClick={onBack}>‹</IconButton>
          : <button type="button" className="ds-topbar__logo" onClick={onHome} aria-label="파이어맵 홈"><Logo /><span>파이어맵</span></button>}
        {title && onBack && <h1 className="ds-topbar__title">{title}</h1>}
      </div>
      {title && !onBack && <h1 className="ds-topbar__title ds-topbar__title--center">{title}</h1>}
      <div className="ds-topbar__side ds-topbar__side--end">{actions}</div>
    </header>
  );
}
