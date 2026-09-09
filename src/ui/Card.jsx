// DS-4 Card · DS-5 SectionHead
const cx = (...a) => a.filter(Boolean).join(' ');

// variant: base | hero(주황 테두리) | soft | flat | tint | dark
export function Card({ variant = 'base', padding = 'md', onClick, as, className = '', children, ...rest }) {
  const cls = cx('ds-card', variant !== 'base' && `ds-card--${variant}`, padding === 'lg' && 'ds-card--lg', onClick && 'ds-card--clickable', className);
  const Tag = as || (onClick ? 'button' : 'section');
  const extra = Tag === 'button' ? { type: 'button', onClick } : (onClick ? { onClick } : {});
  return <Tag className={cls} {...extra} {...rest}>{children}</Tag>;
}

// kicker(작은 주황 라벨) · title · desc · action(우측)
export function SectionHead({ kicker, title, desc, action, size, as = 'h2', className = '' }) {
  const T = as;
  return (
    <div className={cx('ds-sh', size === 'sm' && 'ds-sh--sm', className)}>
      <div style={{ minWidth: 0, flex: 1 }}>
        {kicker && <span className="ds-sh__kicker">{kicker}</span>}
        {title && <T className="ds-sh__title">{title}</T>}
        {desc && <p className="ds-sh__desc">{desc}</p>}
      </div>
      {action && <div className="ds-sh__action">{action}</div>}
    </div>
  );
}
