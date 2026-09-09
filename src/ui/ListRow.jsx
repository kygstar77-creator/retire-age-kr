// DS-6 ListRow / ListGroup — 토스 TDS ListRow(S/M/L) 문법
const cx = (...a) => a.filter(Boolean).join(' ');

export function ListGroup({ label, className = '', children }) {
  return (
    <div className={cx('ds-listgroup', className)}>
      {label && <p className="ds-list__label">{label}</p>}
      <div className="ds-list">{children}</div>
    </div>
  );
}

// lead: 이모지/아이콘 노드 · trail: 값/노드 · chevron: › 표시 · href면 <a>, onClick이면 <button>, 둘 다 없으면 static div
export function ListRow({ lead, title, desc, trail, chevron = true, size = 'M', accent = false, href, external = false, onClick, className = '', ...rest }) {
  const cls = cx('ds-row-item', `ds-row-item--${size}`, accent && 'ds-row-item--accent', !href && !onClick && 'ds-row-item--static', className);
  const body = (
    <>
      {lead != null && <span className="ds-row-item__lead" aria-hidden="true">{lead}</span>}
      <span className="ds-row-item__body">
        <span className="ds-row-item__title">{title}</span>
        {desc && <span className="ds-row-item__desc">{desc}</span>}
      </span>
      {(trail != null || chevron) && (
        <span className="ds-row-item__trail">
          {trail}
          {chevron && (href || onClick) && <span className="ds-row-item__chev" aria-hidden="true">›</span>}
        </span>
      )}
    </>
  );
  if (href) return <a className={cls} href={href} {...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {})} {...rest}>{body}</a>;
  if (onClick) return <button type="button" className={cls} onClick={onClick} {...rest}>{body}</button>;
  return <div className={cls} {...rest}>{body}</div>;
}
