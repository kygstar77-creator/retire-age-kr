// DS-10 Chip / Badge · DS-14 Tabs(segmented)
const cx = (...a) => a.filter(Boolean).join(' ');

export function Chips({ className = '', children }) { return <div className={cx('ds-chips', className)}>{children}</div>; }

export function Chip({ on = false, onClick, className = '', children, ...rest }) {
  if (!onClick) return <span className={cx('ds-chip', 'ds-chip--static', on && 'ds-chip--on', className)} {...rest}>{children}</span>;
  return <button type="button" className={cx('ds-chip', on && 'ds-chip--on', className)} aria-pressed={on} onClick={onClick} {...rest}>{children}</button>;
}

// tone: neutral | accent | good | warn | bad | dark
export function Badge({ tone = 'neutral', className = '', children }) {
  return <span className={cx('ds-badge', `ds-badge--${tone}`, className)}>{children}</span>;
}

// items: [{key,label}] · value · onChange(key) · variant: segmented | pill
export function Tabs({ items = [], value, onChange, variant = 'segmented', label, className = '' }) {
  return (
    <div className={cx('ds-tabs', variant === 'pill' && 'ds-tabs--pill', className)} role="tablist" aria-label={label}>
      {items.map((it) => (
        <button type="button" key={it.key} role="tab" className="ds-tabs__item" aria-selected={value === it.key} onClick={() => onChange && onChange(it.key)}>{it.label}</button>
      ))}
    </div>
  );
}
