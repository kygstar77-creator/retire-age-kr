// DS-17 Notice / EmptyState · DS-18 Skeleton / Spinner
import { IconButton, Button } from './Button.jsx';
const cx = (...a) => a.filter(Boolean).join(' ');

// tone: neutral | accent | good | warn | bad
export function Notice({ tone = 'neutral', icon, title, onClose, className = '', children }) {
  return (
    <div className={cx('ds-notice', tone !== 'neutral' && `ds-notice--${tone}`, className)} role={tone === 'bad' ? 'alert' : undefined}>
      {icon && <span className="ds-notice__icon" aria-hidden="true">{icon}</span>}
      <div className="ds-notice__body">
        {title && <span className="ds-notice__title">{title}</span>}
        {children}
      </div>
      {onClose && <IconButton label="닫기" size="sm" plain className="ds-notice__close" onClick={onClose}>✕</IconButton>}
    </div>
  );
}

export function EmptyState({ icon = '🌱', title, desc, action, className = '' }) {
  return (
    <div className={cx('ds-empty', className)}>
      <div className="ds-empty__icon" aria-hidden="true">{icon}</div>
      {title && <p className="ds-empty__title">{title}</p>}
      {desc && <p className="ds-empty__desc">{desc}</p>}
      {action && <Button variant="secondary" size="sm" onClick={action.onClick}>{action.label}</Button>}
    </div>
  );
}

export function Skeleton({ lines = 3, card = false, className = '' }) {
  if (card) return <span className={cx('ds-skel', 'ds-skel--card', className)} aria-hidden="true" />;
  return (
    <div className={className} aria-hidden="true">
      <span className="ds-skel ds-skel--title" />
      {Array.from({ length: Math.max(0, lines - 1) }).map((_, i) => <span key={i} className="ds-skel" style={{ width: `${88 - i * 14}%` }} />)}
    </div>
  );
}

export function Spinner({ label = '불러오는 중' }) { return <span className="ds-spinner" role="status" aria-label={label} />; }
