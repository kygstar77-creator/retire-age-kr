import { useEffect, useState } from 'react';

const readDays = (key, field) => { try { const v = JSON.parse(localStorage.getItem(key) || 'null'); return (v && v[field]) || {}; } catch { return {}; } };
const ymd = (y, m, d) => `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;

export default function DepositCalendar({ storageKey = 'fm_daily', field = 'days', label = '저축' }) {
  const [days, setDays] = useState(() => readDays(storageKey, field));
  useEffect(() => {
    const h = () => setDays(readDays(storageKey, field));
    window.addEventListener('fm-savings-changed', h);
    return () => window.removeEventListener('fm-savings-changed', h);
  }, [storageKey, field]);
  const now = new Date();
  const y = now.getFullYear();
  const m = now.getMonth();
  const first = new Date(y, m, 1).getDay();
  const dim = new Date(y, m + 1, 0).getDate();
  const today = now.getDate();
  const prefix = `${y}-${String(m + 1).padStart(2, '0')}`;
  const logged = Object.keys(days).filter((k) => k.startsWith(prefix) && days[k] > 0).length;
  const cells = [];
  for (let i = 0; i < first; i += 1) cells.push(null);
  for (let d = 1; d <= dim; d += 1) cells.push(d);
  return (
    <section className="fm-card fm-cal">
      <p className="fm-kicker">{m + 1}월 {label} 달력 · {logged}일 기록</p>
      <div className="fm-cal-grid">
        {['일', '월', '화', '수', '목', '금', '토'].map((w) => <span key={w} className="fm-cal-w">{w}</span>)}
        {cells.map((d, i) => {
          if (d == null) return <span key={`e${i}`} className="fm-cal-cell empty" />;
          const has = days[ymd(y, m, d)] > 0;
          return <span key={d} className={`fm-cal-cell${has ? ' on' : ''}${d === today ? ' today' : ''}`}>{d}</span>;
        })}
      </div>
    </section>
  );
}
