// DS-23 PotCard — 파이어 통(Monzo Pot 문법): 이름·이모지·현재/목표·진행률·이번 달.
import { ProgressBar } from './Stat.jsx';
const cx = (...a) => a.filter(Boolean).join(' ');

// pot{name, emoji} · current · target · monthLabel · monthValue · onEdit · fmt(fn) · hideAmount
export function PotCard({ pot, current = 0, target = 0, monthLabel, monthValue, onEdit, fmt = (v) => String(v), hideAmount = false, className = '' }) {
  const pct = target > 0 ? Math.max(0, Math.min(100, (current / target) * 100)) : 0;
  const mask = (v) => (hideAmount ? '•••' : fmt(v));
  return (
    <section className={cx('ds-card', 'ds-card--hero', 'ds-pot', className)}>
      <button type="button" className="ds-pot__head" onClick={onEdit} aria-label="파이어 통 이름·목표 바꾸기">
        <span className="ds-pot__emoji" aria-hidden="true">{(pot && pot.emoji) || '🔥'}</span>
        <span className="ds-pot__name">{(pot && pot.name) || '내 파이어 통'}</span>
        <span className="ds-pot__edit" aria-hidden="true">✎</span>
      </button>
      <div className="ds-pot__nums">
        <span className="ds-pot__cur num">{mask(current)}</span>
        <span className="ds-pot__tgt num">/ {mask(target)}</span>
      </div>
      <ProgressBar value={pct} max={100} thin />
      <div className="ds-pot__foot">
        <span className="num">{Math.round(pct)}%</span>
        {monthLabel && <span className="num">{monthLabel} {hideAmount ? '•••' : monthValue}</span>}
      </div>
    </section>
  );
}
