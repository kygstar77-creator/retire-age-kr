import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import DailyFire from './DailyFire.jsx';

export default function Home({ onStart, onMove }) {
  const [agg, setAgg] = useState(null);
  useEffect(() => {
    let alive = true;
    fetchAggregates().then((a) => { if (alive) setAgg(a); });
    return () => { alive = false; };
  }, []);
  const latest = getLatestRank();

  return (
    <main className="fm-screen fm-home-v3 fm-has-tabbar">
      <Header tag="1분 계산" />
      {latest && (
        <button type="button" className="fm-recent-rank" onClick={() => { window.location.hash = '#result'; }}>
          <span className="fm-recent-label">내 최근 계산</span>
          <span className="fm-recent-main">{latest.earliest ? `${latest.earliest}세에 퇴사 가능` : '내 퇴사 가능 나이'}</span>
          <span className="fm-recent-sub">지난 계산 다시 보기 ›</span>
        </button>
      )}
      <section className="fm-home-hero-card">
        <p>퇴사나이 계산기</p>
        <h1>나는 몇 살에<br />퇴사할 수 있을까?</h1>
        <span>자산·생활비만 입력하면 1분 만에 내 퇴사 가능 나이와 또래 중 내 등수까지 나와요.</span>
        <button type="button" onClick={onStart}>1분 만에 내 퇴사 나이 계산하기</button>
        {agg && agg.total > 0 && (
          <p className="fm-home-proof">
            <b>{agg.total.toLocaleString()}명</b>이 이미 계산했어요{agg.avgEarliest ? <> · 또래 평균 퇴사 <b>{agg.avgEarliest}세</b></> : null}
          </p>
        )}
      </section>
      <DailyFire onMove={onMove} />
      <section className="fm-home-mini-card"