import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank, submitScore, fetchAggregates } from '../../utils/firemapScoresApi.js';
import Poll from './Poll.jsx';

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
  const [agg, setAgg] = useState(null);
  const [scope, setScope] = useState('all');
  const bandArg = scope === 'band' ? base.ageBand : undefined;

  const load = async () => {
    const [t, r, a] = await Promise.all([fetchTopScores(10, bandArg), fetchUserRank(earliest, bandArg), fetchAggregates()]);
    setTop(t);
    setMe(r);
    setAgg(a);
  };

  useEffect(() => { load(); }, [score, scope]);

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
        <p className="fm-rank-label">내 순위 · {scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} · 가장 빨리 은퇴 순</p>
        <div className="fm-rank-top">
          <span className="fm-rank-pct">{me ? `${me.position.toLocaleString()}위` : '집계 중…'}</span>
          <span className="fm-rank-badge">{base.grade}등급</span>
        </div>
        {me && <p className="fm-rank-line">{scope === 'band' ? `${base.ageBandLabel} 또래` : '전체'} {me.total.toLocaleString()}명 중 · {earliest ? `${earliest}세 은퇴 가능` : '아직 은퇴 어려움'} · {score}점</p>}
        {me && (me.position > 1
          ? <p className="fm-rank-climb">1등까지 <b>{(me.position - 1).toLocaleString()}명</b> · 더 일찍 은퇴 가능하면 순위가 올라가요</p>
          : <p className="fm-rank-climb">지금 전체 1등이에요! 가장 빨리 은퇴 가능한 사람</p>)}
      </section>

      <div className="fm-scope-toggle">
        <button type="button" className={scope === 'all' ? 'on' : ''} onClick={() => setScope('all')}>전체</button>
        <button type="button" className={scope === 'band' ? 'on' : ''} onClick={() => setScope('band')}>{base.ageBandLabel} 또래</button>
      </div>

      {agg && agg.total > 0 && (
        <section className="fm-card fm-stats">
          <h2 className="fm-section-title">파이어맵 현황</h2>
          <p className="fm-section-sub">지금까지 함께 계산한 모두의 익명 집계예요</p>
          <div className="fm-stats-grid">
            <div><small>함께 계산</small><b>{agg.total.toLocaleString()}명</b></div>
            {agg.avgEarliest != null && <div><small>평균 은퇴 가능</small><b>{agg.avgEarliest}세</b></div>}
            {agg.avgScore != null && <div><small>평균 자산수명</small><b>{agg.avgScore}점</b></div>}
            {agg.topBand != null && <div><small>가장 많은 연령대</small><b>{agg.topBand}대</b></div>}
          </div>
        </section>
      )}

      <Poll />

      <section className="fm-card fm-nick">
        <label htmlFor="fm-nick-input">내 닉네임 (랭킹에 표시)</label>
        <div className="fm-nick-row">
          <input id="fm-nick-input" maxLength={16} value={nick} placeholder="예: 파이어왕" onChange={(e) => setNick(e.target.value)} />
          <button type="button" onClick={saveNick} disabled={saving || !nick.trim()}>{saving ? '등록 중' : saved ? '등록됨' : '랭킹 등록'}</button>
        </div>
        <small>익명도 괜찮아요. 닉네임을 넣으면 아래 랭킹에 내 이름으로 올라가요.</small>
      </section>

      <section className="fm-card">
        <h2 className="fm-section-title">전체 상위 랭킹</h2>
        <p className="fm-section-sub">{scope === 'band' ? `${base.ageBandLabel} 또래 중 ` : ''}가장 빨리 은퇴 가능한 순 · 계산하는 사람이 늘수록 갱신돼요</p>
        <ol className="fm-lb-list">
          {top === null && <li className="fm-lb-empty">불러오는 중…</li>}
          {top && top.length === 0 && <li className="fm-lb-empty">아직 데이터가 적어요. 첫 랭커가 되어보세요!</li>}
          {top && top.map((row, i) => (
            <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}`}>
              <span className="fm-lb-rank">{medal(i)}</span>
              <span className="fm-lb-who">{row.nickname ? row.nickname : '익명'}{row.age_band ? ` · ${row.age_band}대` : ''}</span>
              <span className="fm-lb-score">{row.earliest_age ? `${row.earliest_age}세 은퇴` : `${row.fire_score}점`}</span>
            </li>
          ))}
        </ol>
      </section>

      <button type="button" className="fm-city-cta" onClick={() => onMove('experiment')}>조건 바꿔 순위 올리기</button>
    </main>
  );
}
