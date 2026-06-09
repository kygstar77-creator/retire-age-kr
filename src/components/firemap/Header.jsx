export default function Header({ tag, onBack }) {
  return (
    <header className="fm-topbar">
      <div className="fm-logo"><span aria-hidden="true">FIRE</span>파이어맵</div>
      <div className="fm-actions">
        {tag && <span>{tag}</span>}
        {onBack && <button type="button" className="fm-back-btn" onClick={onBack}><span className="fm-back-arrow" aria-hidden="true">←</span>이전</button>}
      </div>
    </header>
  );
}
