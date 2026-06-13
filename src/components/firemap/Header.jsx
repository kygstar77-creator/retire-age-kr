export default function Header({ tag, onBack }) {
  const goHome = () => { window.location.hash = '#home'; };
  return (
    <header className="fm-topbar">
      <button type="button" className="fm-logo" onClick={goHome} aria-label="처음으로">
        <svg className="fm-logo-mark" viewBox="118 84 276 276" width="21" height="21" aria-hidden="true">
          <path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/>
          <path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/>
        </svg>
        파이어맵
      </button>
      <div className="fm-actions">
        {tag && <span className="fm-tag">{tag}</span>}
        {onBack && <button type="button" className="fm-back-btn" onClick={onBack}>‹ 이전</button>}
      </div>
    </header>
  );
}
