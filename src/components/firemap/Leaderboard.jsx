import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank, submitScore } from '../../utils/firemapScoresApi.js';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));
const readNick = () => { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } };

export default function Leaderboard({ simulation, onBack, onMove }) {
  const base = statsRank(simulation);
  const score = simulation.survivalScore;
  const earliest = simulation.earliestRetirementAge;
  const [top, setTop] = useState(null);
  const [me, setMe] = useState(null);
  const [nick, setNick] = useState(readNick);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const load = async () => {
    const [t, r] = await Promise.all([fetchTopScores(10), fetchUserRank(earliest)]);
    setTop(t); setMe(r);
  };

  useEffect(() => { let alive = true; (async () => { await load(); })(); return () => { alive = false; }; }, [score]);

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

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="랭킹" onBack={onBack} />
      <section className="fm-rank-hero">
        <p className="fm-rank-label">내 순위 · 가장 빨리 은퇴 가능한 순</p>
        <div className="fm-rank-top">
          <span className="fm-rank-pct">{me ? `${me.position.toLocaleString()}위` : '집계 중…'}</span>
          <span className="fm-rank-badge">{base.grade}등급</span>
        </div>
        {me && <p className="fm-rank-line">전체 {me.total.toLocaleString()}명 중 · {earliest ? `${earliest}세 은퇴 가능` : '아직 은퇴 어려움'} · {score}점</p>}
        {me && me.position > 1
          ? <p className="fm-rank-climb">1등까지 <b>{(me.position - 1).toLocaleString()}명</b> · 더 일찍 은퇴 가능하면 순위가 올라가요</p>
          : me && <p className="fm-rank-climb">지금 전체 1등이에요! 가장 빨리 은퇴 가능한 사람</p>}
      </section>

      <section className="fm-card fm-nick">
        <label htmlFor="fm-nick-input">내 닉네임 (랭킹에