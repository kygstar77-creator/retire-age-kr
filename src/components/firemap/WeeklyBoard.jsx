import { useEffect, useState } from 'react';
import { identityIds, accountHandle } from '../../utils/identity.js';
import { funHandle } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { fetchWeeklySaveBoard } from '../../utils/firemapSaveApi.js';

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
  const [rows, setRows] = useState(null);
  const ids = identityIds();
  const acctHandle = accountHandle();
  useEffect(() => {
    let alive = true;
    const run = () => fetchWeeklySaveBoard(10).then((r) => { if (alive) setRows(r); });
    run();
    window.addEventListener('fm-savings-changed', run);
    return () => { alive = false; window.removeEventListener('fm-savings-changed', run); };
  }, []);
  return (
    <section className='fm-card'>
      <p className='fm-kicker'>이번 주 절약왕 🏆</p>
      <p className='fm-section-sub'>이번 주(월~일) 가장 많이 아낀 사람 · {resetText()}</p>
      <ol className='fm-lb-list'>
        {rows === null && <li className='fm-lb-empty'>불러오는 중…</li>}
        {rows && rows.length === 0 && <li className='fm-lb-empty'>이번 주 첫 주자가 되어보세요!</li>}
        {rows && rows.map((r, i) => {
          const mine = r.client_id && ids.includes(r.client_id);
          return (
            <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}${mine ? ' me' : ''}`}>
              <span className='fm-lb-rank'>{medal(i)}</span>
              <span className='fm-lb-who'>{mine && acctHandle ? acctHandle : (r.nickname || funHandle(r.client_id))}{mine ? ' (나)' : ''}{r.age_band ? ` · ${r.age_band}대` : ''}</span>
              <span className='fm-lb-score'>{wonStr(r.value)}</span>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
