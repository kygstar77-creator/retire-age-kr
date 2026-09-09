// DS-1 Button · DS-2 IconButton · DS-3 BottomCTA
const cx = (...a) => a.filter(Boolean).join(' ');

export function Button({ variant = 'primary', size = 'md', full = false, loading = false, as, href, className = '', children, ...rest }) {
  const cls = cx('ds-btn', `ds-btn--${variant}`, `ds-btn--${size}`, full && 'ds-btn--full', loading && 'ds-btn--loading', className);
  if (as === 'a' || href) {
    return <a className={cls} href={href} aria-disabled={rest.disabled ? 'true' : undefined} {...rest}>{children}</a>;
  }
  return <button type="button" className={cls} disabled={rest.disabled || loading} {...rest}>{children}</button>;
}

export function IconButton({ label, size = 'md', plain = false, className = '', children, ...rest }) {
  return (
    <button type="button" className={cx('ds-iconbtn', size === 'sm' && 'ds-iconbtn--sm', plain && 'ds-iconbtn--plain', className)} aria-label={label} title={label} {...rest}>
      {children}
    </button>
  );
}

// primary 하나 또는 secondary+primary 둘. fixed면 하단 고정(세이프에어리어 포함).
export function BottomCTA({ primary, secondary, fixed = false, className = '' }) {
  return (
    <div className={cx('ds-bottomcta', fixed && 'ds-bottomcta--fixed', className)}>
      {secondary && <Button variant="secondary" size="lg" onClick={secondary.onClick} disabled={secondary.disabled}>{secondary.label}</Button>}
      {primary && <Button variant="primary" size="lg" onClick={primary.onClick} disabled={primary.disabled} loading={primary.loading}>{primary.label}</Button>}
    </div>
  );
}
