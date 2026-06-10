export default function Header({ tag, onBack }) {
  const goHome = () => { window.location.hash = '#home'; };
  return (
    <header className="fm-topbar">
      <button type="button" className="fm-logo" onClick={goHome} aria-label="처음으로">
        <svg className="fm-logo-mark" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
          <path d="M13.2 2.3c1.1 4.2-2 5.4-2 8.3 0 1.5 1 2.1 1 2.1s-2 .3-2.1 2.6c-1.9-1.5-3.6-3.6-3.6-3.6s-1.2 1.9-1.2 4.1a6.8 6.8 0 0 0 13.5.2c0-5.2-4-7.4-5.6-13.7z" fill="#ff5a00"/>
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
