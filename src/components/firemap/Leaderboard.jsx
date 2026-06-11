import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank } from '../../utils/firemapScoresApi.js';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));

export default function Leaderboard({ simulation, onBack, onMove }) {
  const base = statsRank(simulation);
  const score = simulation.survivalScore;
  const [top, setTop] = useState(null);
  const [me, setMe] = useState(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      const [t, r] = await Promise.all([fetchTopScores(10), fetchUserRank(score)]);
      if (alive) { setTop(t); setMe(r); }
    })();
    return () => { alive = false; };
  }, [score]);

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="랭킹" onBack={onBack} />
      <section className="fm-rank-hero">
        <p className="fm-rank-label">내 순위 · {base.ageBandLabel} 포함 전체</p>
        <div className="fm-rank-top">
          <span className="fm-rank-pct">{me ? `${me.position.toLocaleString()}위` : '집계 중…'}</span>
          <span className="fm-rank-badge">{base.grade}등급</span>
        </div>
        {me && <p className="fm-rank-line">전체 {me.total.toLocaleString()}명 중 · 상위 {base.percentile}% · {score}점</p>}
        {me && me.position > 1
          ? <p className="fm-rank-climb">1등까지 <b>{(me.position - 1).toLocaleString()}명</b> · 조건을 바꾸면 등수가 올라가요</p>
          : me && <p className="fm-rank-climb">지금 전체 1등이에요! 이 자리를 지켜보세요</p>}
      </section>

      <section className="fm-card">
        <h2 className="fm-section-title">전체 상위 랭킹</h2>
        <p className="fm-section-sub">익명 · 자산수명 점수 순 · 계산하는 사람이 늘수록 갱신돼요</p>
        <ol className="fm-lb-list">
          {top === null && <li className="fm-lb-empty">불러오는 중…</li>}
          {top && top.length === 0 && <li className="fm-lb-empty">아직 데이터가 적어요. 첫 랭커가 되어보세요!</li>}
          {top && top.map((row, i) => (
            <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}`}>
              <span className="fm-lb-rank">{medal(i)}</span>
              <span className="fm-lb-who">익명{row.age_band ? ` · ${row.age_band}대` : ''}</span>
              <span className="fm-lb-score">{row.fire_score}점</span>
            </li>
          ))}
        </ol>
      </section>

      <button type="button" className="fm-city-cta" onClick={() => onMove('experiment')}>조건 바꿔 순위 올리기</button>
    </main>
  );
}
