export default function Header({ tag, onBack }) {
  const goHome = () => { window.location.hash = '#home'; };
  return (
    <header className="fm-topbar">
      <button type="button" className="fm-logo" onClick={goHome} aria-label="처음으로">
        <svg className="fm-logo-mark" viewBox="0 0 24 24" width="21" height="21" aria-hidden="true">
          <path fillRule="evenodd" clipRule="evenodd" d="M12.963 2.286a.75.75 0 0 0-1.071-.136 9.742 9.742 0 0 0-3.539 6.176 7.547 7.547 0 0 1-1.705-1.715.75.75 0 0 0-1.152-.082A9 9 0 1 0 15.68 4.534a7.46 7.46 0 0 1-2.717-2.248ZM15.75 14.25a3.75 3.75 0 1 1-7.313-1.172c.628.465 1.35.81 2.133 1.013A5.99 5.99 0 0 1 12.6 8.539a3.75 3.75 0 0 1 3.15 5.711Z" fill="#ff5a00"/>
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
