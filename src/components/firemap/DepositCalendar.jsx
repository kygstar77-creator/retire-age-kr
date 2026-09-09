// 저축 달력 — 이번 달 기록 한눈에. 지난 날짜를 눌러 채울 수 있다(추가 전용, 서버 병합 저장).
import { useEffect, useState } from 'react';
import { Button, Chips, Chip, toast } from '../../ui/index.js';
import { pushState, pullKey, pushDailyMerged } from '../../utils/firemapStateApi.js';
import { notifySavingsChanged, reportBoard } from '../../utils/savingsEngine.js';
import { track, dailyNeedOf, fmtAdvance } from '../../firemap-v2/dailyData.js';
import { formatWon } from '../../firemap-v2/formatters.js';

const readObj = (key) => { try { return JSON.parse(localStorage.getItem(key) || 'null') || {}; } catch { return {}; } };
const readDays = (key, field) => { const o = readObj(key); return (o && o[field]) || {}; };
const ymd = (y, m, d) => `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;

export default function DepositCalendar({ storageKey = 'fm_daily', field = 'days', label = '저축', editable = false, simulation = null }) {
  const [days, setDays] = useState(() => readDays(storageKey, field));
  const [pick, setPick] = useState(null);
  const [amt, setAmt] = useState('');
  useEffect(() => {
    const h = () => setDays(readDays(storageKey, field));
    window.addEventListener('fm-savings-changed', h);
    let alive = true;
    pullKey(storageKey).then((v) => {
      if (!alive || !v || !v[field] || !Object.keys(v[field]).length) return;
      const merged = { ...v[field], ...readDays(storageKey, field) };
      try { const o = readObj(storageKey); localStorage.setItem(storageKey, JSON.stringify({ ...o, [field]: merged })); } catch { /* ignore */ }
      setDays(merged);
    }).catch(() => {});
    return () => { alive = false; window.removeEventListener('fm-savings-changed', h); };
  }, [storageKey, field]);

  const now = new Date(); const y = now.getFullYear(); const m = now.getMonth();
  const first = new Date(y, m, 1).getDay(); const dim = new Date(y, m + 1, 0).getDate(); const today = now.getDate();
  const prefix = `${y}-${String(m + 1).padStart(2, '0')}`;
  const logged = Object.keys(days).filter((k) => k.startsWith(prefix) && days[k] > 0).length;
  const monthTotal = Object.entries(days).filter(([k]) => k.startsWith(prefix)).reduce((a, [, v]) => a + (Number(v) || 0), 0);
  const cells = []; for (let i = 0; i < first; i += 1) cells.push(null); for (let d = 1; d <= dim; d += 1) cells.push(d);

  const openCell = (d) => { if (!editable || d > today) return; const key = ymd(y, m, d); setPick(key); setAmt(days[key] != null ? String(days[key]) : ''); };
  const savePick = () => {
    if (!pick) return;
    const v = Math.max(0, Math.round(Number(String(amt).replace(/[^0-9]/g, '')) || 0));
    const obj = readObj(storageKey);
    const nextDays = { ...(obj[field] || {}) };
    if (v > 0) nextDays[pick] = v; else delete nextDays[pick];
    const next = { ...obj, [field]: nextDays };
    try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch { /* ignore */ }
    setDays(nextDays);
    if (storageKey === 'fm_daily') {
      pushDailyMerged(next).then((merged) => {
        try { const o2 = readObj(storageKey); localStorage.setItem(storageKey, JSON.stringify({ ...o2, [field]: merged.days || {} })); } catch { /* ignore */ }
        setDays(merged.days || {}); notifySavingsChanged();
        if (simulation) { try { reportBoard(simulation); } catch { /* ignore */ } }
      });
    } else { pushState(storageKey, next); notifySavingsChanged(); if (simulation) { try { reportBoard(simulation); } catch { /* ignore */ } } }
    try { track('deposit_backfill', { date: pick, amt: v }); } catch { /* ignore */ }
    if (v > 0 && simulation) {
      try { const need = dailyNeedOf(simulation); const adv = need ? fmtAdvance((v / need) * 86400) : ''; toast.good(adv ? `${formatWon(v)} 기록 · 파이어 ${adv} 당겨졌어요` : `${formatWon(v)} 기록했어요`); } catch { /* ignore */ }
    }
    setPick(null); setAmt('');
  };

  return (
    <div className="ds-cal">
      <p className="ds-caption ds-cal__head">{m + 1}월 · {logged}일 기록 · <b className="num">{formatWon(monthTotal)}</b>{editable ? ' · 날짜를 눌러 채워요' : ''}</p>
      <div className="ds-cal__grid">
        {['일', '월', '화', '수', '목', '금', '토'].map((w) => <span key={w} className="ds-cal__w">{w}</span>)}
        {cells.map((d, i) => {
          if (d == null) return <span key={`e${i}`} className="ds-cal__cell ds-cal__cell--empty" />;
          const key = ymd(y, m, d); const has = days[key] > 0; const future = d > today;
          const cls = `ds-cal__cell${has ? ' ds-cal__cell--on' : ''}${d === today ? ' ds-cal__cell--today' : ''}${future ? ' ds-cal__cell--future' : ''}${pick === key ? ' ds-cal__cell--sel' : ''}`;
          if (editable && !future) return <button type="button" key={d} className={cls} onClick={() => openCell(d)} aria-label={`${m + 1}월 ${d}일 ${label} 입력`}>{d}</button>;
          return <span key={d} className={cls}>{d}</span>;
        })}
      </div>
      {editable && pick && (
        <div className="ds-mt-3">
          <p className="ds-caption ds-cal__head">{pick.slice(5).replace('-', '/')} {label}</p>
          <input className="ds-input num" inputMode="numeric" value={amt} onChange={(e) => setAmt(e.target.value.replace(/[^0-9]/g, ''))} placeholder="금액" autoFocus />
          <Chips className="ds-mt-2">{[10000, 30000, 50000, 100000].map((n) => <Chip key={n} onClick={() => setAmt(String(n))}>{formatWon(n)}</Chip>)}</Chips>
          <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => { setPick(null); setAmt(''); }}>취소</Button><Button variant="primary" size="md" onClick={savePick}>저장</Button></div>
        </div>
      )}
    </div>
  );
}
