export default function Header({ tag, onBack }) {
  return (
    <header className="fm-topbar">
      <div className="fm-logo"><span aria-hidden="true">FIRE</span>파이어맵</div>
      <div className="fm-actions">
        <span>{tag}</span>
        {onBack && <button type="button" onClick={onBack}>이전</button>}
      </div>
    </header>
  );
}
