export default function Header({ tag, onBack }) {
  const goHome = () => { window.location.hash = '#home'; };
  return (
    <header className="fm-topbar">
      <button type="button" className="fm-logo" onClick={goHome} aria-label="처음으로">
        <span className="fm-logo-mark" aria-hidden="true">F</span>파이어맵
      </button>
      <div className="fm-actions">
        {tag && <span className="fm-tag">{tag}</span>}
        {onBack && <button type="button" className="fm-back-btn" onClick={onBack}>‹ 이전</button>}
      </div>
    </header>
  );
}
