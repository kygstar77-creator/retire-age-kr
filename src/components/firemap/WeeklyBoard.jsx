import { useEffect, useState } from 'react';
import { identityIds, accountHandle } from '../../utils/identity.js';
import { funHandle } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { fetchWeeklySaveBoard, fetchWeeklyHall } from '../../utils/firemapSaveApi.js';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));

function resetText() {
  const now = new Date();
  const day = now.getDay();
  let d = (1 - day + 7) % 7;
  if (d === 0) d = 7;
  const next = new Date(now.getFullYear(), now.getMonth(), now.getDate() + d, 0, 0, 0, 0);
  const ms = next - now;
  const hours = Math.floor(ms / 3600000);
  const days = Math.floor(hours / 24);
  const rh = hours - days * 24;
  return days > 0 ? `${days}일 ${rh}시간 후 리셋` : `${rh}시간 후 리셋`;
}

export default function WeeklyBoard() {
  const [tab, setTab] = useState('this');
  const [rows, setRows] = useState(null);
  const [hall, setHall] = useState(null);
  const ids = identityIds();
  const acctHandle = accountHandle();

  useEffect(() => {
    let alive = true;
    const off = tab === 'last' ? 1 : 0;
    setRows(null);
    fetchWeeklySaveBoard(10, off).then((r) => { if (alive) setRows(r); });
    const onChange = () => { if (tab === 'this') fetchWeeklySaveBoard(10, 0).then((r) => { if (alive) setRows(r); }); };
    window.addEventListener('fm-savings-changed', onChange);
    return () => { alive = false; window.removeEventListener('fm-savings-changed', onChange); };
  }, [tab]);

  useEffect(() => {
    let alive = true;
    fetchWeeklyHall(8).then((h) => { if (alive) setHall(h); });
    return () => { alive = false; };
  }, []);

  const nameOf = (r) => (r.nickname && r.nickname.trim()) || funHandle(r.client_id || '');
  const mine = (r) => r.client_id && ids.includes(r.client_id);

  return (
    <>
      <section className='fm-card'>
        <p className='fm-kicker'>절약왕 시즌 🏆</p>
        <div className='fm-scope-toggle'>
          <button type='button' className={tab === 'this' ? 'on' : ''} onClick={() => setTab('this')}>이번 주</button>
          <button type='button' className={tab === 'last' ? 'on' : ''} onClick={() => setTab('last')}>지난 주</button>
        </div>
        <p className='fm-section-sub'>{tab === 'this' ? `이번 주(월~일) 가장 많이 아낀 사람 · ${resetText()}` : '지난주 최종 순위'}</p>
        <ol className='fm-lb-list'>
          {rows === null && <li className='fm-lb-empty'>불러오는 중…</li>}
          {rows && rows.length === 0 && <li className='fm-lb-empty'>{tab === 'this' ? '이번 주 첫 주자가 되어보세요!' : '지난주 기록이 없어요'}</li>}
          {rows && rows.map((r, i) => (
            <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}${mine(r) ? ' me' : ''}`}>
              <span className='fm-lb-rank'>{medal(i)}</span>
              <span className='fm-lb-who'>{mine(r) && acctHandle ? acctHandle : nameOf(r)}{mine(r) ? ' (나)' : ''}{r.age_band ? ` · ${r.age_band}대` : ''}</span>
              <span className='fm-lb-score'>{wonStr(r.value)}</span>
            </li>
          ))}
        </ol>
      </section>

      {hall && hall.length > 0 && (
        <section className='fm-card'>
          <p className='fm-kicker'>명예의 전당 👑</p>
          <p className='fm-section-sub'>지난 주차별 절약왕</p>
          <ol className='fm-lb-list'>
            {hall.map((h, i) => (
              <li key={i} className={`fm-lb-row${mine(h) ? ' me' : ''}`}>
                <span className='fm-lb-rank'>👑</span>
                <span className='fm-lb-who'>{h.weekLabel} · {mine(h) && acctHandle ? acctHandle : nameOf(h)}{mine(h) ? ' (나)' : ''}</span>
                <span className='fm-lb-score'>{wonStr(h.value)}</span>
              </li>
            ))}
          </ol>
        </section>
      )}
    </>
  );
}
