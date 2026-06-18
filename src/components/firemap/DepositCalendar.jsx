import { useEffect, useState } from 'react';
import { pushState, pullKey } from '../../utils/firemapStateApi.js';
import { notifySavingsChanged, reportBoard } from '../../utils/savingsEngine.js';
import { track } from '../../firemap-v2/dailyData.js';

const readObj = (key) => { try { return JSON.parse(localStorage.getItem(key) || 'null') || {}; } catch { return {}; } };
const readDays = (key, field) => { const o = readObj(key); return (o && o[field]) || {}; };
const ymd = (y, m, d) => `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;

const EDIT_STYLE = `
.fm-cal button.fm-cal-cell{ appearance:none; border:0; background:none; font:inherit; cursor:pointer; padding:0; width:100%; }
.fm-cal-cell.future{ color:#cdd3db; cursor:default; }
.fm-cal-cell.sel{ outline:2px solid #ff5a00; outline-offset:-2px; }
.fm-cal-edit{ margin-top:10px; align-items:center; }
.fm-cal-edit-date{ font-size:12.5px; font-weight:800; color:#c2410c; flex:0 0 auto; }
.fm-cal-hint{ font-size:11px; color:#9aa3bf; margin:8px 0 0; line-height:1.5; }
`;

// 저축 달력 — 이번 달 기록을 한눈에. editable=true면 과거(오늘 포함) 날짜를 눌러
// 소급(백필) 입력/수정할 수 있어요. 데이터는 날짜별 키(days[YYYY-MM-DD])라 추가전용으로 안전하게 들어가요.
// editable 없이 쓰면 기존처럼 표시 전용(하위호환).
export default function DepositCalendar({ storageKey = 'fm_daily', field = 'days', label = '저축', editable = false, simulation = null }) {
  const [days, setDays] = useState(() => readDays(storageKey, field));
  const [pick, setPick] = useState(null); // 선택된 날짜 'YYYY-MM-DD' | null
  const [amt, setAmt] = useState('');
  useEffect(() => {
    const h = () => setDays(readDays(storageKey, field));
    window.addEventListener('fm-savings-changed', h);
    // 마운트 시 클라우드에서 한 번 받아와 로컬에 채우고 화면 갱신 (로그인 기기 동기화 대비)
    let alive = true;
    pullKey(storageKey).then((v) => {
      if (!alive || !v || !v[field]) return;
      try { localStorage.setItem(storageKey, JSON.stringify(v)); } catch { /* ignore */ }
      setDays(v[field] || {});
    }).catch(() => {});
    return () => { alive = false; window.removeEventListener('fm-savings-changed', h); };
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

  const openCell = (d) => {
    if (!editable || d > today) return; // 미래 날짜는 입력 불가
    const key = ymd(y, m, d);
    setPick(key);
    setAmt(days[key] != null ? String(days[key]) : '');
  };
  const savePick = () => {
    if (!pick) return;
    const v = Math.max(0, Math.round(Number(String(amt).replace(/[^0-9]/g, '')) || 0));
    const obj = readObj(storageKey);
    const nextDays = { ...(obj[field] || {}) };
    if (v > 0) nextDays[pick] = v; else delete nextDays[pick];
    const next = { ...obj, [field]: nextDays };
    try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch { /* ignore */ }
    setDays(nextDays);
    pushState(storageKey, next);
    notifySavingsChanged();
    if (simulation) { try { reportBoard(simulation); } catch { /* ignore */ } }
    try { track('deposit_backfill', { date: pick, amt: v }); } catch { /* ignore */ }
    setPick(null); setAmt('');
  };

  return (
    <section className="fm-card fm-cal">
      {editable && <style>{EDIT_STYLE}</style>}
      <p className="fm-kicker">{m + 1}월 {label} 달력 · {logged}일 기록{editable ? ' · 날짜를 눌러 입력' : ''}</p>
      <div className="fm-cal-grid">
        {['일', '월', '화', '수', '목', '금', '토'].map((w) => <span key={w} className="fm-cal-w">{w}</span>)}
        {cells.map((d, i) => {
          if (d == null) return <span key={`e${i}`} className="fm-cal-cell empty" />;
          const key = ymd(y, m, d);
          const has = days[key] > 0;
          const future = d > today;
          const cls = `fm-cal-cell${has ? ' on' : ''}${d === today ? ' today' : ''}${editable && future ? ' future' : ''}${editable && pick === key ? ' sel' : ''}`;
          if (editable && !future) {
            return <button type="button" key={d} className={cls} onClick={() => openCell(d)} aria-label={`${m + 1}월 ${d}일 ${label} 입력`}>{d}</button>;
          }
          return <span key={d} className={cls}>{d}</span>;
        })}
      </div>
      {editable && pick && (
        <div className="fm-save-inline fm-cal-edit">
          <span className="fm-cal-edit-date">{pick.slice(5).replace('-', '/')} {label}</span>
          <input inputMode="numeric" className="fm-save-inline-in" value={amt} onChange={(e) => setAmt(e.target.value.replace(/[^0-9]/g, ''))} placeholder="금액 (원)" autoFocus />
          <button type="button" className="fm-save-inline-go" onClick={savePick}>저장</button>
          <button type="button" className="fm-save-inline-cancel" onClick={() => { setPick(null); setAmt(''); }}>취소</button>
        </div>
      )}
      {editable && <p className="fm-cal-hint">빠뜨린 날도 눌러서 채울 수 있어요 · 미래 날짜는 입력할 수 없어요.</p>}
    </section>
  );
}
