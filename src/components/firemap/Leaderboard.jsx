import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank, submitScore, fetchAggregates, fetchNeighbors } from '../../utils/firemapScoresApi.js';
import { fetchSaveBoard } from '../../utils/firemapSaveApi.js';
import { displayName } from '../../firemap-v2/funName.js';
import { wonStr } from '../../firemap-v2/dailyData.js';
import BalanceGame from './BalanceGame.jsx';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));
const readNick = () => { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } };
const myCid = () => { try { return localStorage.getItem('fm_cid'); } catch { return null; } };

const BOARDS = [
  { key: 'fire', label: '빠른 은퇴' },
  { key: 'today', label: '오늘의 절약왕' },
  { key: 'total', label: '누적 절약' },
  { key: 'streak', label: '연속일' }
];
const SUBS = {
  fire: '가장 빨리 은퇴 가능한 순 · 계산하는 사람이 늘수록 갱신',
  today: '오늘 가장 많이 아낀 순 · 매일 0시 새로 시작',
  total: '지금까지 누적 절약이 많은 순',
  streak: '절약을 연속으로 기록한 날이 많은 순'
};

export default function Leaderboard({ simulation, onBack, onMove }) {
  const base = statsRank(simulation);
  const score = simulation.survivalScore;
  const earliest = simulation.earliestRetirementAge;
  const cid = myCid();
  const [board, setBoard] = useState('fire');
  const [top, setTop] = useState(null);
  const [me, setMe] = useState(null);
  const [neighbors, setNeighbors] = useState(null);
  const [agg, setAgg] = useState(null);
  const [scope, setScope] = useState('all');
  const [nick, setNick] = useState(readNick);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const bandArg = scope === 'band' ? base.ageBand : undefined;

  const load = async () => {
    if (board === 'fire') {
      const [t, r, a, nb] = await Promise.all([
        fetchTopScores(10, bandArg),
        fetchUserRank(earliest, bandArg),
        fetchAggregates(),
        fetchNeighbors(earliest, bandArg)
      ]);
      setTop(t); setMe(r); setAgg(a); setNeighbors(nb);
    } else {
      setTop(null); setNeighbors(null);
      const rows = await fetchSaveBoard(board, 10);
      setTop(rows);
    }
  };

  useEffect(() => { load(); /* eslint-disable-next-line */ }, [score, scope, board]);

  const saveNick = async () => {
    const v = nick.trim().slice(0, 16);
    setSaving(true);
    try { localStorage.setItem('fm_nickname', v); } catch { /* ignore */ }
    await submitScore({
      fireScore: score,
      ageBand: base.ageBand,
      survivalAge: (simulation.targetResult && simulation.targetResult.depletionAge) || simulation.inputs.simulationUntilAge,
      nickname: v,
      earliestAge: earliest
    });
    await load();
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const rowValue = (row) => {
    if (board === 'fire') return row.earliest_age ? `${row.earliest_age}세 은퇴` : '—';
    if (board === 'streak') return `${row.value || 0}일`;
    return wonStr(row.value || 0);
  };

  const nearAbove = neighbors && neighbors.above.length ? neighbors.above[neighbors.above.length - 1] : null;
  const aboveN = neighbors ? neighbors.above : [];
  const belowN = neighbors ? neighbors.below : [];

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="랭킹" onBack={onBack} />

      <div className="fm-board-tabs">
        {BOARDS.map((b) => (
          <button type="button" key={b.key} className={board === b.key ? 'on' : ''} onClick={() => setBoard(b.key)}>{b.label}</button>
        ))}
      </div>

      {board === 'fire' && (
        <>
          <section className="fm-rank-hero">
            <p className="fm-rank-label">내 순위 · {scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} · 가장 빨리 은퇴 순</p>
            <div className="fm-rank-top">
              <span className="fm-rank-pct">{me ? `${me.position.toLocaleString()}위` : '집계 중…'}</span>
            </div>
            {me && <p className="fm-rank-line">{scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} {me.total.toLocaleString()}명 중 · {earliest ? `${earliest}세 은퇴 가능` : '아직 은퇴 어려움'}</p>}
            {me && (me.position > 1
              ? <p className="fm-rank-climb">1등까지 <b>{(me.position - 1).toLocaleString()}명</b> · 더 일찍 은퇴 가능하면 순위가 올라가요</p>
              : <p className="fm-rank-climb">지금 전체 1등이에요! 가장 빨리 은퇴 가능한 사람</p>)}
          </section>

          <div className="fm-scope-toggle">
            <button type="button" className={scope === 'all' ? 'on' : ''} onClick={() => setScope('all')}>전체</button>
            <button type="button" className={scope === 'band' ? 'on' : ''} onClick={() => setScope('band')}>{base.ageBandLabel} 또래</button>
          </div>

          {me && (aboveN.length > 0 || belowN.length > 0) && (
            <section className="fm-card">
              <h2 className="fm-section-title">내 주변 순위</h2>
              {nearAbove && earliest
                ? <p className="fm-section-sub">바로 위 <b>{displayName(nearAbove)}</b>는 {nearAbove.earliest_age}세 · <b>{Math.max(1, earliest - nearAbove.earliest_age)}년</b>만 당기면 제쳐요!</p>
                : <p className="fm-section-sub">바로 위·아래 라이벌이에요. 조건을 바꿔 따라잡아 보세요.</p>}
              <ol className="fm-lb-list">
                {aboveN.map((r, i) => (
                  <li key={`a${i}`} className="fm-lb-row">
                    <span className="fm-lb-rank">{(me.position - (aboveN.length - i)).toLocaleString()}</span>
                    <span className="fm-lb-who">{displayName(r)}</span>
                    <span className="fm-lb-score">{r.earliest_age ? `${r.earliest_age}세 은퇴` : '—'}</span>
                  </li>
                ))}
                <li className="fm-lb-row me">
                  <span className="fm-lb-rank">{me.position.toLocaleString()}</span>
                  <span className="fm-lb-who">{nick.trim() ? nick.trim() : '나'} (나)</span>
                  <span className="fm-lb-score">{earliest ? `${earliest}세 은퇴` : '—'}</span>
                </li>
                {belowN.map((r, i) => (
                  <li key={`b${i}`} className="fm-lb-row">
                    <span className="fm-lb-rank">{(me.position + i + 1).toLocaleString()}</span>
                    <span className="fm-lb-who">{displayName(r)}</span>
                    <span className="fm-lb-score">{r.earliest_age ? `${r.earliest_age}세 은퇴` : '—'}</span>
                  </li>
                ))}
              </ol>
            </section>
          )}

          {agg && agg.total > 0 && (
            <section className="fm-card fm-stats">
              <h2 className="fm-section-title">파이어맵 현황</h2>
              <p className="fm-section-sub">지금까지 함께 계산한 모두의 익명 집계예요</p>
              <div className="fm-stats-grid">
                <div><small>함께 계산</small><b>{agg.total.toLocaleString()}명</b></div>
                {agg.avgEarliest != null && <div><small>평균 은퇴 가능</small><b>{agg.avgEarliest}세</b></div>}
                {agg.topBand != null && <div><small>가장 많은 연령대</small><b>{agg.topBand}대</b></div>}
              </div>
            </section>
          )}

          <section className="fm-card fm-nick">
            <label htmlFor="fm-nick-input">내 닉네임 (랭킹에 표시)</label>
            <div className="fm-nick-row">
              <input id="fm-nick-input" maxLength={16} value={nick} placeholder="예: 파이어왕" onChange={(e) => setNick(e.target.value)} />
              <button type="button" onClick={saveNick} disabled={saving || !nick.trim()}>{saving ? '등록 중' : saved ? '등록됨' : '랭킹 등록'}</button>
            </div>
            <small>닉네임을 안 넣어도 '알뜰한 너구리'처럼 자동 별명으로 올라가요. 넣으면 내 이름으로 바뀌어요.</small>
          </section>
        </>
      )}

      <section className="fm-card">
        <h2 className="fm-section-title">{BOARDS.find((b) => b.key === board).label} 상위</h2>
        <p className="fm-section-sub">{SUBS[board]}</p>
        <ol className="fm-lb-list">
          {top === null && <li className="fm-lb-empty">불러오는 중…</li>}
          {top && top.length === 0 && <li className="fm-lb-empty">아직 데이터가 적어요. 첫 랭커가 되어보세요!</li>}
          {top && top.map((row, i) => {
            const mine = row.client_id && cid && row.client_id === cid;
            return (
              <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}${mine ? ' me' : ''}`}>
                <span className="fm-lb-rank">{medal(i)}</span>
                <span className="fm-lb-who">{displayName(row)}{mine ? ' (나)' : ''}{row.age_band ? ` · ${row.age_band}대` : ''}</span>
                <span className="fm-lb-score">{rowValue(row)}</span>
              </li>
            );
          })}
        </ol>
      </section>

      {board === 'fire' && <BalanceGame />}

      <button type="button" className="fm-city-cta" onClick={() => onMove(board === 'fire' ? 'experiment' : 'save')}>{board === 'fire' ? '조건 바꿔 순위 올리기' : '절약 더 하러 가기'}</button>
    </main>
  );
}
