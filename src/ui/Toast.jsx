// DS-13 Toast — window.alert 대체. toast('문구') 어디서나 호출, <Toaster/>는 앱 루트에 1개.
import { useEffect, useState } from 'react';

const listeners = new Set();
let seq = 0;

// tone: 'neutral' | 'good' | 'bad' · action: {label, onClick}
export function toast(message, opts = {}) {
  const item = { id: ++seq, message, tone: opts.tone || 'neutral', action: opts.action || null, ms: opts.ms || 2600 };
  listeners.forEach((fn) => fn(item));
  return item.id;
}
toast.good = (m, o) => toast(m, { ...o, tone: 'good' });
toast.bad = (m, o) => toast(m, { ...o, tone: 'bad' });

export function Toaster() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    const on = (item) => {
      setItems((c) => [...c.slice(-2), item]);
      window.setTimeout(() => setItems((c) => c.filter((x) => x.id !== item.id)), item.ms);
    };
    listeners.add(on);
    return () => listeners.delete(on);
  }, []);
  if (!items.length) return null;
  return (
    <div className="ds-toaster" aria-live="polite">
      {items.map((it) => (
        <div key={it.id} className={`ds-toast${it.tone !== 'neutral' ? ` ds-toast--${it.tone}` : ''}`} role="status">
          <span>{it.message}</span>
          {it.action && <button type="button" className="ds-toast__action" onClick={() => { it.action.onClick(); setItems((c) => c.filter((x) => x.id !== it.id)); }}>{it.action.label}</button>}
        </div>
      ))}
    </div>
  );
}
