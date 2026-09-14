// DS-32 Ticker — 지표·소식 한 줄이 몇 초마다 다음 항목으로 넘어간다(토스증권 상단 지수 표기 방식).
// items: [{ key, label, value, unit, delta, sub, text }] · 한 항목이면 그대로 고정 · 탭이 숨겨지면 멈춘다.
// 움직임 줄이기(prefers-reduced-motion)면 넘어가긴 하되 미끄러지지 않고 바로 바뀐다.
import { useEffect, useState } from 'react';

const STEP_MS = 4000;

export function Ticker({ items = [], onClick, className = '', ariaLabel }) {
  const [i, setI] = useState(0);
  const n = items.length;
  useEffect(() => { setI(0); }, [n]);
  useEffect(() => {
    if (n < 2) return undefined;
    const t = setInterval(() => { if (!document.hidden) setI((k) => (k + 1) % n); }, STEP_MS);
    return () => clearInterval(t);
  }, [n]);
  if (!n) return null;
  const it = items[i % n];
  const dir = it.delta == null ? null : (String(it.delta).startsWith('+') ? 'up' : (String(it.delta).startsWith('-') ? 'down' : 'flat'));
  const body = (
    <span key={it.key ?? i} className="ds-ticker__item">
      {it.text != null ? <span className="ds-ticker__text">{it.text}</span> : (
        <>
          <span className="ds-ticker__label">{it.label}{it.sub ? <span className="ds-ticker__sub">{it.sub}</span> : null}</span>
          <span className="ds-ticker__value num">{it.value}{it.unit ? <span className="ds-ticker__unit">{it.unit}</span> : null}</span>
          {it.delta != null && <span className={`ds-ticker__delta num ds-ticker__delta--${dir}`}>{it.delta}</span>}
        </>
      )}
    </span>
  );
  const cls = `ds-ticker ${className}`;
  return onClick
    ? <button type="button" className={`${cls} ds-ticker--btn`} onClick={onClick} aria-label={ariaLabel} aria-live="off">{body}</button>
    : <div className={cls} aria-label={ariaLabel} aria-live="off">{body}</div>;
}
