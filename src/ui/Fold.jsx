// DS-20 Fold — 접힘 섹션. fm-section-toggle·fm-advanced-toggle·fm-calc-toggle 4벌 대체. 열 때만 children 렌더(lazy).
import { useState } from 'react';
const cx = (...a) => a.filter(Boolean).join(' ');

export function Fold({ title, hint, icon, defaultOpen = false, onOpen, className = '', children }) {
  const [open, setOpen] = useState(defaultOpen);
  const toggle = () => { const n = !open; setOpen(n); if (n && onOpen) onOpen(); };
  return (
    <section className={cx('ds-fold', open && 'ds-fold--open', className)}>
      <button type="button" className="ds-fold__head" onClick={toggle} aria-expanded={open}>
        {icon && <span className="ds-fold__icon" aria-hidden="true">{icon}</span>}
        <span className="ds-fold__text">
          <span className="ds-fold__title">{title}</span>
          {hint && <span className="ds-fold__hint">{hint}</span>}
        </span>
        <span className="ds-fold__chev" aria-hidden="true">{open ? '▴' : '▾'}</span>
      </button>
      {open && <div className="ds-fold__body">{children}</div>}
    </section>
  );
}
