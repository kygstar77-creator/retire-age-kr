import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import IdentityLine from './IdentityLine.jsx';
import { identityIds, accountHandle } from '../../utils/identity.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank, submitScore, fetchAggregates, fetchNeighbors } from '../../utils/firemapScoresApi.js';
import { fetchSaveBoard } from '../../utils/firemapSaveApi.js';
import { displayName } from '../../firemap-v2/funName.js';
import { wonStr, fmtAdvance, readJSON, todayStr } from '../../firemap-v2/dailyData.js';
import { computeProgress, hasCalculated } from '../../utils/savingsEngine.js';
import BalanceGame from './BalanceGame.jsx';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));
const readNick = () => { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } };
const myCid = () => { try { return localStorage.getItem('fm_cid'); } catch { return null; } };

const BOARDS = [
  { key: 'fire', label: '빠른 은퇴' },
  { key: 'advance', label: '퇴사 앞당김' },
  { key: 'deposit', label: '이번 달 저축' },
  { key: 'save', label: '절약' }
];
const SUBS = {
  fire: '은퇴 가능 나이가 빠른 순 · 나이가 같으면 저축 많이 한 사람이 위',
  advance: '적립·절약으로 은퇴를 가장 많이 앞당긴 순',
  deposit: '이번 달 실제 적립이 많은 순 · 매월 새로 시작',
  save: '아껴서 모은 돈 랭킹'
};

export default function Leaderboard({ simulation, onBack, onMove }) {
  const base = statsRank(simulation);
  const score = simulation.survivalScore;
  const earliest = simulation.earliestRetirementAge;
  const ids = identityIds();
  const acctHandle = accountHandle();
  const myAdvance = hasCalculated() ? Math.max(0, computeProgress(simulation).advanceDays) : 0;
  const [board, setBoard] = useState('fire');
  const [saveMetric, setSaveMetric] = useState('total');
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
        fetchUserRank(earliest, bandArg, myAdvance),
        fetchAggregates(),
        fetchNeighbors(earliest, bandArg)
      ]);
      setTop(t); setMe(r); setAgg(a); setNeighbors(nb);
    } else {
      setTop(null); setNeighbors(null);
      const metric = board === 'save' ? saveMetric : board;
      const rows = await fetchSaveBoard(metric, 10);
      setTop(rows);
    }
  };

  useEffect(() => { load(); /* eslint-disable-next-line */ }, [score, scope, board, saveMetric]);

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
    if (board === 'advance') return (fmtAdvance((Number(row.value) || 0) * 86400) || '0초') + ' 앞당김';
    if (board === 'save' && saveMetric === 'streak') return `${row.value || 0}일`;
    return wonStr(row.value || 0);
  };

  // 저축 계열 보드: 내 기록(로컬 기준) — top 10 밖이어도 내 숫자가 보이게
  const myBoardValue = () => {
    const sv = readJSON('fm_save') || {};
    if (board === 'save') {
      if (saveMetric === 'today') return sv.lastDate === todayStr() ? (sv.today || 0) : 0;
      if (saveMetric === 'streak') return sv.streak || 0;
      return sv.total || 0;
    }
    if (board === 'deposit') return computeProgress(simulation).monthDeposit || 0;
    if (board === 'advance') return hasCalculated() ? Math.max(0, computeProgress(simulation).advanceDays) : 0;
    return 0;
  };
  const fmtMyVal = (v) => {
    if (board === 'advance') return (fmtAdvance(v * 86400) || '0초') + ' 앞당김';
    if (board === 'save' && saveMetric === 'streak') return `${v}일`;
    return wonStr(v);
  };
  const inTop = !!(top && top.some((r) => r.client_id && ids.includes(r.client_id)));

  // 균형 잡힌 주변 윈도우: 위 2 + 아래 2를 기본으로, 한쪽이 모자라면 반대쪽으로 채워 총 4명 유지
  const rawAbove = neighbors ? neighbors.above : [];
  const rawBelow = neighbors ? neighbors.below : [];
  const sameCount = neighbors ? (neighbors.same || 0) : 0;
  const aAvail = rawAbove.length;
  const bAvail = rawBelow.length;
  let aWant = Math.min(2, aAvail);
  let bWant = Math.min(2, bAvail);
  let slack = 4 - aWant - bWant;
  if (slack > 0) { const addB = Math.min(slack, bAvail - bWant); bWant += addB; slack -= addB; aWant += Math.min(slack, aAvail - aWant); }
  const aboveN = aWant > 0 ? rawAbove.slice(-aWant) : [];
  const belowN = rawBelow.slice(0, bWant);
  const nearAbove = aboveN.length ? aboveN[aboveN.length - 1] : null;

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="랭킹" onBack={onBack} />

      <div className="fm-board-tabs">
        {BOARDS.map((b) => (
          <button type="button" key={b.key} className={board === b.key ? 'on' : ''} onClick={() => setBoard(b.key)}>{b.label}</button>
        ))}
      </div>
      {board === 'save' && (
        <div className="fm-scope-toggle">
          <button type="button" className={saveMetric === 'total' ? 'on' : ''} onClick={() => setSaveMetric('total')}>누적</button>
          <button type="button" className={saveMetric === 'today' ? 'on' : ''} onClick={() => setSaveMetric('today')}>오늘</button>
          <button type="button" className={saveMetric === 'streak' ? 'on' : ''} onClick={() => setSaveMetric('streak')}>연속</button>
        </div>
      )}

      {board === 'fire' && (
        <>
          <section className="fm-rank-hero">
            <p className="fm-rank-label">내 순위 · {scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} · 가장 빨리 은퇴 순</p>
            <div className="fm-rank-top">
              <span className="fm-rank-pct">{me ? `${me.position.toLocaleString()}위` : '집계 중…'}</span>
            </div>
            {me && <p className="fm-rank-line">{scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} {me.total.toLocaleString()}명 중 상위 {me.percentile}% · {earliest ? `${earliest}세 은퇴 가능` : '아직 은퇴 어려움'}</p>}
            {me && (me.position > 1
              ? <p className="fm-rank-climb">1등까지 <b>{(me.position - 1).toLocaleString()}명</b> · 은퇴 나이가 빠를수록 위로, <b>은퇴 나이가 같으면 저축 많이 한 사람이 위</b>예요</p>
              : <p className="fm-rank-climb">지금 전체 1등! 매일 저축해서 자리를 지켜요 🔥</p>)}
          </section>

          <div className="fm-scope-toggle">
            <button type="button" className={scope === 'all' ? 'on' : ''} onClick={() => setScope('all')}>전체</button>
            <button type="button" className={scope === 'band' ? 'on' : ''} onClick={() => setScope('band')}>{base.ageBandLabel} 또래</button>
          </div>

          {me && (aboveN.length > 0 || belowN.length > 0) && (
            <section className="fm-card">
              <h2 className="fm-section-title">내 주변 순위</h2>
              {nearAbove && earliest
                ? <p className="fm-section-sub">바로 위 <b>{displayName(nearAbove)}</b>는 {nearAbove.earliest_age}세 · 은퇴를 <b>{Math.max(1, earliest - nearAbove.earliest_age)}년</b>만 앞당기면 제쳐요!</p>
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
                {agg.avgEarliest != null && <div><small>또래 평균 은퇴</small><b>{agg.avgEarliest}세</b></div>}
                {agg.avgEarliest != null && earliest && <div><small>또래 대비 나</small><b>{agg.avgEarliest - earliest === 0 ? '평균과 같음' : `${Math.abs(agg.avgEarliest - earliest)}년 ${agg.avgEarliest - earliest > 0 ? '빠름' : '느림'}`}</b></div>}
                {hasCalculated() && <div><small>또래 중 자산</small><b>상위 {base.percentile}%</b></div>}
              </div>
            </section>
          )}

          <section className="fm-card fm-nick">
            <IdentityLine onMove={onMove} />
            <button type="button" className="fm-nick-reg" onClick={saveNick} disabled={saving}>{saving ? '등록 중' : saved ? '등록됨 ✓' : '내 등수 랭킹에 올리기'}</button>
            <small>익명이면 '알뜰한 너구리'처럼 자동 별명으로, 계정을 만들면 내 이름으로 올라가요.</small>
          </section>
        </>
      )}

      <section className="fm-card">
        <h2 className="fm-section-title">{BOARDS.find((b) => b.key === board).label} 상위</h2>
        <p className="fm-section-sub">{SUBS[board]}</p>
        {board !== 'fire' && (
          myBoardValue() > 0
            ? <p className="fm-save-myrank">내 기록 <b>{fmtMyVal(myBoardValue())}</b> · {inTop ? '위 목록에 있어요 🎉' : '아직 10위권 밖이에요'}</p>
            : <p className="fm-save-myrank">이 보드엔 아직 내 기록이 없어요 · ‘저축’ 탭에서 기록하면 올라가요</p>
        )}
        <ol className="fm-lb-list">
          {top === null && <li className="fm-lb-empty">불러오는 중…</li>}
          {top && top.length === 0 && <li className="fm-lb-empty">아직 데이터가 적어요. 첫 랭커가 되어보세요!</li>}
          {top && top.map((row, i) => {
            const mine = row.client_id && ids.includes(row.client_id);
            return (
              <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}${mine ? ' me' : ''}`}>
                <span className="fm-lb-rank">{medal(i)}</span>
                <span className="fm-lb-who">{mine && acctHandle ? acctHandle : displayName(row)}{mine ? ' (나)' : ''}{row.age_band ? ` · ${row.age_band}대` : ''}</span>
                <span className="fm-lb-score">{rowValue(row)}</span>
              </li>
            );
          })}
        </ol>
      </section>

      {board === 'fire' && <BalanceGame />}

      <button type="button" className="fm-city-cta" onClick={() => onMove(board === 'fire' ? 'experiment' : 'save')}>{board === 'fire' ? '조건 바꿔 순위 올리기' : '저축 기록하러 가기'}</button>
    </main>
  );
}
