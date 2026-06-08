export default function Header({ tag, onBack }) {
  return (
    <header className="fm-topbar">
      <div className="fm-logo">파이어맵</div>
      <div className="fm-actions">
        <span>{tag}</span>
        {onBack && <button type="button" onClick={onBack}>결과로</button>}
      </div>
    </header>
  );
}
