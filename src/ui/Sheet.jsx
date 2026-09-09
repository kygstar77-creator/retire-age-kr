// DS-12 Sheet(바텀시트) · DS-13 Dialog
import { useEffect } from 'react';
import { IconButton, Button } from './Button.jsx';

function useEsc(onClose) {
  useEffect(() => {
    const h = (e) => { if (e.key === 'Escape' && onClose) onClose(); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [onClose]);
}

export function Sheet({ open, title, onClose, children, className = '' }) {
  useEsc(open ? onClose : null);
  if (!open) return null;
  return (
    <div className="ds-dim" onClick={(e) => { if (e.target === e.currentTarget && onClose) onClose(); }}>
      <div className={`ds-sheet ${className}`} role="dialog" aria-modal="true" aria-label={typeof title === 'string' ? title : undefined}>
        <div className="ds-sheet__grab" aria-hidden="true" />
        {(title || onClose) && (
          <div className="ds-sheet__head">
            <h2 className="ds-sheet__title">{title}</h2>
            {onClose && <IconButton label="닫기" size="sm" plain onClick={onClose}>✕</IconButton>}
          </div>
        )}
        <div className="ds-sheet__body">{children}</div>
      </div>
    </div>
  );
}

// confirm형: primary/secondary 라벨과 핸들러. alert형은 secondary 생략.
export function Dialog({ open, title, desc, primary, secondary, onClose, children }) {
  useEsc(open ? onClose : null);
  if (!open) return null;
  return (
    <div className="ds-dim ds-dim--center" onClick={(e) => { if (e.target === e.currentTarget && onClose) onClose(); }}>
      <div className="ds-dialog" role="alertdialog" aria-modal="true" aria-label={title}>
        {title && <h2 className="ds-dialog__title">{title}</h2>}
        {desc && <p className="ds-dialog__desc">{desc}</p>}
        {children}
        <div className="ds-bottomcta ds-mt-2">
          {secondary && <Button variant="secondary" size="md" onClick={secondary.onClick || onClose}>{secondary.label}</Button>}
          {primary && <Button variant={primary.variant || 'primary'} size="md" onClick={primary.onClick}>{primary.label}</Button>}
        </div>
      </div>
    </div>
  );
}
