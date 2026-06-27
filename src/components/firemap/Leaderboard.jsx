import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { identityIds, accountHandle } from '../../utils/identity.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank, submitScoreFromSim, fetchAggregates, fetchNeighbors, fetchAssetPercentile, assetBandOf, fetchPeerBoard, fetchStageBoard } from '../../utils/firemapScoresApi.js';
import { fetchSaveBoard, fetchCohortAdvanceBoard } from '../../utils/firemapSaveApi.js';
import { displayName } from '../../firemap-v2/funName.js';
import { wonStr, fmtAdvance, readJSON, todayStr } from '../../firemap-v2/dailyData.js';
import { computeProgress, hasCalculated, reportBoard } from '../../utils/savingsEngine.js';
import CommunityPeek from './CommunityPeek.jsx';
import { journeyStage, JOURNEY_STAGES } from '../../utils/journeyStage.js';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));
const readNick = () => { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } };
const myCid = () => { try { return localStorage.getItem('fm_cid'); } catch { return null; } };

const BOARDS = [
  { key: 'fire', label: '전체 순위' },
  { key: 'peer', label: '내 또래 순위' },
  { key: 'advance', label: '저축 순위' }
];
const SUBS = {
  stage: '나와 같은 FIRE 여정 단계에 있는 사람들끼리 순위 — 같은 출발선에서 누가 더 빨리 가나',
  peer: '같은 나이 또래 중 내 파이어 등수 — 같은 나이가 모이면 정확 나이 기준으로 좁혀져요',
  fire: '전체에서 파이어 가능 나이가 빠른 순 · 같으면 저축 많이 한 사람이 위',
  cohort: '같은 나이·목표 또래끼리 — 저축으로 파이어를 더 당긴 순 (절대 저축액이 아니라 공평)',
  advance: '저축으로 파이어를 가장 많이 앞당긴 순',
  deposit: '이번 달 실제 저축이 많은 순 · 매월 새로 시작',
  save: '아껴서 모은 돈 랭킹'
};
const COHORT_SCOPE_WORD = { exact: '나랑 같은 나이·목표 또래', cohort: '같은 나이대·목표 또래', age: '같은 나이대 또래', all: '전체' };

export default function Leaderboard({ simulation, rankingSimulation, onBack, onMove }) {
  const rs = rankingSimulation || simulation;
  const base = statsRank(rs);
  const myJourney = (() => { try { return journeyStage(simulation); } catch { return null; } })();
  const myStage = myJourney ? myJourney.stage : null;
  const stageMeta = JOURNEY_STAGES.find((x) => x.n === myStage) || null;
  const score = rs.survivalScore;
  const earliest = rs.earliestRetirementAge;
  const ids = identityIds();
  const acctHandle = accountHandle();
  const myAdvance = hasCalculated() ? Math.max(0, computeProgress(simulation).advanceDays) : 0;
  const myBand = hasCalculated() ? assetBandOf(simulation.netWorth) : null;
  const [board, setBoard] = useState('fire');
  const [peer, setPeer] = useState(null);
  const [stageB, setStageB] = useState(null);
  const [saveMetric, setSaveMetric] = useState('total');
  const [top, setTop] = useState(null);
  const [me, setMe] = useState(null);
  const [neighbors, setNeighbors] = useState(null);
  const [assetPct, setAssetPct] = useState(null);
  const [agg, setAgg] = useState(null);
  const [scope, setScope] = useState('all');
  const [cohortScope, setCohortScope] = useState(null);
  const [nick, setNick] = useState(readNick);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const bandArg = scope === 'band' ? base.ageBand : undefined;
  const scopeWord = scope === 'band' ? `${base.ageBandLabel} 또래` : '전체';

  const load = async () => {
    if (board === 'stage') {
      setNeighbors(null); setMe(null);
      const [sb, a] = await Promise.all([
        fetchStageBoard({ stage: myStage, earliestAge: earliest, advancedDays: myAdvance, limit: 10 }),
        fetchAggregates(base.ageBand)
      ]);
      setStageB(sb);
      setTop(sb ? sb.top : []);
      setAgg(a);
    } else if (board === 'fire') {
      const [t, r, a, nb, ap] = await Promise.all([
        fetchTopScores(10, bandArg),
        fetchUserRank(earliest, bandArg, myAdvance),
        fetchAggregates(bandArg),
        fetchNeighbors(earliest, bandArg),
        fetchAssetPercentile(bandArg, myBand)
      ]);
      setTop(t); setMe(r); setAgg(a); setNeighbors(nb); setAssetPct(ap);
    } else if (board === 'peer') {
      setMe(null);
      const [pr, a, ap] = await Promise.all([
        fetchPeerBoard({ currentAge: rs.inputs && rs.inputs.currentAge, ageBand: base.ageBand, earliestAge: earliest, advancedDays: myAdvance, limit: 10 }),
        fetchAggregates(base.ageBand),
        fetchAssetPercentile(base.ageBand, myBand)
      ]);
      setPeer(pr);
      setTop(pr ? pr.top : []);
      setAgg(a);
      setAssetPct(ap);
      // 또래 보드도 전체 순위처럼 '내 주변 순위' 표시 — 보드 범위(정확 나이/연령대)에 맞춰 조회
      const exactAge = pr && pr.scope === 'age' ? (rs.inputs && rs.inputs.currentAge) : undefined;
      const bandForNb = pr && pr.scope === 'band' ? base.ageBand : undefined;
      const nb = await fetchNeighbors(earliest, bandForNb, exactAge);
      setNeighbors(nb);
    } else if (board === 'cohort') {
      setTop(null); setNeighbors(null);
      const tgt = Number(rs.inputs && rs.inputs.targetRetirementAge) || null;
      const lo = tgt != null ? Math.floor(tgt / 5) * 5 : null;
      const hi = lo != null ? lo + 4 : null;
      const rows = await fetchCohortAdvanceBoard(base.ageBand, lo, hi, 10, rs.inputs && rs.inputs.currentAge);
      setTop(rows);
      setCohortScope(rows && rows.length ? rows[0].scope : null);
    } else {
      setTop(null); setNeighbors(null);
      const metric = board === 'save' ? saveMetric : board;
      const rows = await fetchSaveBoard(metric, 10);
      setTop(rows);
    }
  };

  useEffect(() => {
    let alive = true;
    (async () => {
      if (hasCalculated()) { try { await reportBoard(simulation); } catch { /* ignore */ } }
      if (alive) load();
    })();
    return () => { alive = false; };
    // eslint-disable-next-line
  }, [score, scope, board, saveMetric]);

  const saveNick = async () => {
    const v = nick.trim().slice(0, 16);
    setSaving(true);
    try { localStorage.setItem('fm_nickname', v); } catch { /* ignore */ }
    await submitScoreFromSim({ rankingSimulation, simulation, nickname: v });
    await load();
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const rowValue = (row) => {
    if (board === 'fire' || board === 'peer' || board === 'stage') return row.earliest_age ? `${row.earliest_age}세 파이어` : '—';
    if (board === 'advance' || board === 'cohort') return (fmtAdvance((Number(row.value) || 0) * 86400) || '0초') + ' 앞당김';
    if (board === 'save' && saveMetric === 'streak') return `${row.value || 0}일`;
    return wonStr(row.value || 0);
  };

  // 저축 계열 보드: 내 기록(로컬 기준) — top 10 밖이어도 내 숫자가 보이게
  const myBoardValue = () => {
    const sv = readJSON('fm_save') || {};
    if (board === 'cohort') return hasCalculated() ? Math.max(0, computeProgress(simulation).advanceDays) : 0;
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
    if (board === 'advance' || board === 'cohort') return (fmtAdvance(v * 86400) || '0초') + ' 앞당김';
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

  // 코호트(목표 라이벌) 정보 — 나이·목표나이 표시
  const myAge = Number(rs.inputs && rs.inputs.currentAge) || null;
  const myTarget = Number(rs.inputs && rs.inputs.targetRetirementAge) || null;
  const tLo = myTarget != null ? Math.floor(myTarget / 5) * 5 : null;
  const tHi = tLo != null ? tLo + 4 : null;
  const cohortTitle = cohortScope === 'exact'
    ? `${myAge}세 · 목표 ${tLo}~${tHi}세 라이벌`
    : cohortScope === 'cohort'
      ? `${base.ageBandLabel} · 목표 ${tLo}~${tHi}세 라이벌`
      : cohortScope === 'age' ? `${base.ageBandLabel} 또래` : '전체 파이어족';
  const cohortHint = cohortScope === 'exact' ? ''
    : cohortScope === 'cohort' ? ' · 같은 나이가 더 모이면 정확 나이로 좁혀져요'
    : ' · 기록이 더 쌓이면 같은 나이·목표끼리 좁혀져요';

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="랭킹" onBack={onBack} />

      <div className="fm-board-tabs">
        {BOARDS.map((b) => (
          <button type="button" key={b.key} className={board === b.key ? 'on' : ''} onClick={() => setBoard(b.key)}>{b.label}</button>
        ))}
      </div>
      <p style={{ textAlign: 'center', fontSize: '12px', color: '#9a3412', background: '#fff7ed', border: '1px solid #fed7aa', borderRadius: '10px', padding: '7px 12px', margin: '0 0 10px' }}>✋ 모든 순위는 사용자가 직접 입력한 기록 기반이에요 — 서로 양심껏 기록해요</p>
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
            <p className="fm-rank-label">내 순위 · {scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} · 가장 빨리 파이어 순</p>
            <div className="fm-rank-top">
              <span className="fm-rank-pct">{me ? `${me.position.toLocaleString()}위` : '집계 중…'}</span>
            </div>
            {me && <p className="fm-rank-line">{scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} {me.total.toLocaleString()}명 중 상위 {me.percentile}% · {earliest ? `${earliest}세 파이어 가능` : '아직 파이어 어려움'}</p>}
            {me && (me.position > 1
              ? <p className="fm-rank-climb">1등까지 <b>{(me.position - 1).toLocaleString()}명</b> · 파이어 나이가 빠를수록 위로, <b>파이어 나이가 같으면 저축 많이 한 사람이 위</b>예요</p>
              : <p className="fm-rank-climb">지금 전체 1등! 매일 저축해서 자리를 지켜요 🔥</p>)}
          </section>

          {me && (aboveN.length > 0 || belowN.length > 0) && (
            <section className="fm-card">
              <h2 className="fm-section-title">내 주변 순위</h2>
              {nearAbove && earliest
                ? <p className="fm-section-sub">바로 위 <b>{displayName(nearAbove)}</b>는 {nearAbove.earliest_age}세 · 파이어를 <b>{Math.max(1, earliest - nearAbove.earliest_age)}년</b>만 앞당기면 제쳐요!</p>
                : <p className="fm-section-sub">바로 위·아래 라이벌이에요. 조건을 바꿔 따라잡아 보세요.</p>}
              <ol className="fm-lb-list">
                {aboveN.map((r, i) => (
                  <li key={`a${i}`} className="fm-lb-row">
                    <span className="fm-lb-rank">{(me.position - (aboveN.length - i)).toLocaleString()}</span>
                    <span className="fm-lb-who">{displayName(r)}</span>
                    <span className="fm-lb-score">{r.earliest_age ? `${r.earliest_age}세 파이어` : '—'}</span>
                  </li>
                ))}
                <li className="fm-lb-row me">
                  <span className="fm-lb-rank">{me.position.toLocaleString()}</span>
                  <span className="fm-lb-who">{nick.trim() ? nick.trim() : '나'} (나)</span>
                  <span className="fm-lb-score">{earliest ? `${earliest}세 파이어` : '—'}</span>
                </li>
                {belowN.map((r, i) => (
                  <li key={`b${i}`} className="fm-lb-row">
                    <span className="fm-lb-rank">{(me.position + i + 1).toLocaleString()}</span>
                    <span className="fm-lb-who">{displayName(r)}</span>
                    <span className="fm-lb-score">{r.earliest_age ? `${r.earliest_age}세 파이어` : '—'}</span>
                  </li>
                ))}
              </ol>
            </section>
          )}

          {agg && agg.total > 0 && (
            <section className="fm-card fm-stats">
              <h2 className="fm-section-title">통계 현황</h2>
              <p className="fm-section-sub">지금까지 함께 계산한 모두의 익명 집계예요</p>
              <div className="fm-stats-grid">
                <div><small>함께 계산</small><b>{agg.total.toLocaleString()}명</b></div>
                {agg.avgEarliest != null && <div><small>전체 평균 파이어</small><b>{agg.avgEarliest}세</b></div>}
                {agg.avgEarliest != null && earliest && <div><small>전체 대비 나</small><b>{agg.avgEarliest - earliest === 0 ? '평균과 같음' : `${Math.abs(agg.avgEarliest - earliest)}년 ${agg.avgEarliest - earliest > 0 ? '빠름' : '느림'}`}</b></div>}
                {assetPct && <div><small>전체 중 자산</small><b>상위 {assetPct.percentile}%</b></div>}
              </div>
            </section>
          )}

          <section className="fm-card fm-nick">
            <button type="button" className="fm-nick-reg" onClick={saveNick} disabled={saving}>{saving ? '등록 중' : saved ? '등록됨 ✓' : '내 닉네임으로 랭킹에 올리기'}</button>
            <small>카카오로 로그인하거나 닉네임을 정하면 내 이름으로 올라가요. 익명이면 '알뜰한 너구리'처럼 자동 별명이 붙어요.</small>
          </section>
        </>
      )}

      {board === 'peer' && (
        <>
          <section className="fm-rank-hero">
            <p className="fm-rank-label">{peer ? `${peer.ageLabel} 중 내 순위` : '집계 중…'}</p>
            <div className="fm-rank-top">
              <span className="fm-rank-pct">{peer && peer.percentile != null ? `상위 ${peer.percentile}%` : (peer && peer.position != null ? `${peer.position.toLocaleString()}위` : '집계 중…')}</span>
            </div>
            {peer && peer.position != null
              ? <p className="fm-rank-line">{peer.ageLabel} {peer.total.toLocaleString()}명 중 <b>{peer.position.toLocaleString()}위</b> · {earliest ? `${earliest}세 파이어 가능` : '아직 파이어 어려움'}</p>
              : <p className="fm-rank-line">{earliest ? `${earliest}세 파이어 가능` : '계산하면 내 또래 순위가 나와요'}</p>}
            {peer && peer.scope === 'band'
              ? <p className="fm-rank-climb">아직 같은 나이 표본이 적어 <b>{peer.ageLabel}</b> 기준이에요 · 같은 나이가 모이면 자동으로 좁혀져요</p>
              : peer && peer.scope === 'age' && peer.position > 1
                ? <p className="fm-rank-climb">1위까지 <b>{(peer.position - 1).toLocaleString()}명</b> · 조건 바꾸면 등수가 올라가요</p>
                : peer && peer.scope === 'age' && peer.position === 1
                  ? <p className="fm-rank-climb">{peer.ageLabel} 중 전체 1위예요! 🔥</p>
                  : null}
          </section>

          {peer && peer.position != null && (aboveN.length > 0 || belowN.length > 0) && (
            <section className="fm-card">
              <h2 className="fm-section-title">내 주변 순위</h2>
              {nearAbove && earliest
                ? <p className="fm-section-sub">바로 위 <b>{displayName(nearAbove)}</b>는 {nearAbove.earliest_age}세 · 파이어를 <b>{Math.max(1, earliest - nearAbove.earliest_age)}년</b>만 앞당기면 제쳐요!</p>
                : <p className="fm-section-sub">{peer.ageLabel} 안에서 바로 위·아래 라이벌이에요.</p>}
              <ol className="fm-lb-list">
                {aboveN.map((r, i) => (
                  <li key={`pa${i}`} className="fm-lb-row">
                    <span className="fm-lb-rank">{(peer.position - (aboveN.length - i)).toLocaleString()}</span>
                    <span className="fm-lb-who">{displayName(r)}</span>
                    <span className="fm-lb-score">{r.earliest_age ? `${r.earliest_age}세 파이어` : '—'}</span>
                  </li>
                ))}
                <li className="fm-lb-row me">
                  <span className="fm-lb-rank">{peer.position.toLocaleString()}</span>
                  <span className="fm-lb-who">{nick.trim() ? nick.trim() : '나'} (나)</span>
                  <span className="fm-lb-score">{earliest ? `${earliest}세 파이어` : '—'}</span>
                </li>
                {belowN.map((r, i) => (
                  <li key={`pb${i}`} className="fm-lb-row">
                    <span className="fm-lb-rank">{(peer.position + i + 1).toLocaleString()}</span>
                    <span className="fm-lb-who">{displayName(r)}</span>
                    <span className="fm-lb-score">{r.earliest_age ? `${r.earliest_age}세 파이어` : '—'}</span>
                  </li>
                ))}
              </ol>
            </section>
          )}

          {agg && agg.total > 0 && (
            <section className="fm-card fm-stats">
              <h2 className="fm-section-title">또래 비교</h2>
              <p className="fm-section-sub">{base.ageBandLabel} 또래끼리 비교한 익명 집계예요</p>
              <div className="fm-stats-grid">
                <div><small>{base.ageBandLabel} 또래</small><b>{agg.total.toLocaleString()}명</b></div>
                {agg.avgEarliest != null && <div><small>{base.ageBandLabel} 평균 파이어</small><b>{agg.avgEarliest}세</b></div>}
                {agg.avgEarliest != null && earliest && <div><small>또래 대비 나</small><b>{agg.avgEarliest - earliest === 0 ? '평균과 같음' : `${Math.abs(agg.avgEarliest - earliest)}년 ${agg.avgEarliest - earliest > 0 ? '빠름' : '느림'}`}</b></div>}
                {assetPct && <div><small>{base.ageBandLabel} 중 자산</small><b>상위 {assetPct.percentile}%</b></div>}
              </div>
            </section>
          )}

          <section className="fm-card fm-nick">
            <button type="button" className="fm-nick-reg" onClick={saveNick} disabled={saving}>{saving ? '등록 중' : saved ? '등록됨 ✓' : '내 닉네임으로 랭킹에 올리기'}</button>
            <small>카카오로 로그인하거나 닉네임을 정하면 내 이름으로 올라가요. 익명이면 '알뜰한 너구리'처럼 자동 별명이 붙어요.</small>
          </section>
        </>
      )}

      {board === 'advance' && (
        <section className="fm-rank-hero">
          <p className="fm-rank-label">전체 중 내 파이어 앞당김</p>
          <div className="fm-rank-top">
            <span className="fm-rank-pct">{myAdvance > 0 ? (fmtAdvance(myAdvance * 86400) || '0초') : '0초'}</span>
            <span className="fm-rank-badge">내 파이어 당김</span>
          </div>
          <p className="fm-rank-line">
            {myAge != null ? `나 ${myAge}세` : '나'}{myTarget != null ? ` · 목표 ${myTarget}세 파이어` : ''}
          </p>
          {myAdvance > 0
            ? <p className="fm-rank-climb">저축을 기록할수록 파이어가 더 당겨지고 순위가 올라가요 🔥</p>
            : <p className="fm-rank-climb">아직 당긴 기록이 없어요. ‘저축’ 탭에서 저축을 기록하면 파이어가 당겨지고 순위가 올라가요.</p>}
        </section>
      )}

      <section className="fm-card">
        <h2 className="fm-section-title">{BOARDS.find((b) => b.key === board).label} 상위</h2>
        <p className="fm-section-sub">{SUBS[board]}</p>
        {board === 'advance' && (
          myBoardValue() > 0
            ? <p className="fm-save-myrank">내 기록 <b>{fmtMyVal(myBoardValue())}</b> · {inTop ? '상위 10위 안에 있어요 🎉' : '아직 10위권 밖 — 더 기록하면 올라요'}</p>
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

      {(board === 'fire' || board === 'peer') && <CommunityPeek onMove={onMove} />}

      <button type="button" className="fm-city-cta" onClick={() => onMove(board === 'advance' ? 'save' : 'experiment')}>{board === 'advance' ? '저축 기록하러 가기' : '조건 바꿔 순위 올리기'}</button>
    </main>
  );
}
