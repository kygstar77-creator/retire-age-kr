import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import DailyFire from './DailyFire.jsx';

export default function Home({ onStart, onMove }) {
  const [agg, setAgg] = useState(null);
  const [age, setAge] = useState(35);
  useEffect(() => {
    let alive = true;
    fetchAggregates().then((a) => { if (alive) setAgg(a); });
    return () => { alive = false; };
  }, []);

  const latest = getLatestRank();
  const proof = agg && agg.total > 0
    ? `${agg.total.toLocaleString()}명이 이미 계산했어요${agg.avgEarliest ? ` · 또래 평균 퇴사 ${agg.avgEarliest}세` : ''}`
    : '';
  const setClamp = (v) => setAge(Math.max(19, Math.min(80, v)));

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
        <div className="fm-home-age">
          <label htmlFor="fm-home-age-in">지금 몇 살인가요?</label>
          <div className="fm-home-age-ctrl">
            <button type="button" aria-label="나이 감소" onClick={() => setClamp(age - 1)}>−</button>
            <input id="fm-home-age-in" inputMode="numeric" value={age} onChange={(e) => setClamp(Number(String(e.target.value).replace(/[^0-9]/g, '')) || 0)} />
            <span className="fm-home-age-unit">세</span>
            <button type="button" aria-label="나이 증가" onClick={() => setClamp(age + 1)}>+</button>
          </div>
        </div>
        <button type="button" className="fm-home-cta" onClick={() => onStart(age)}>이 나이로 1분 계산 시작 →</button>
        {proof && <p className="fm-home-proof">{proof}</p>}
      </section>
      <DailyFire onMove={onMove} />
      <section className="fm-home-mini-card">
        <strong>입력값은 기기 안에서 계산돼요</strong>
        <p>공유 전에는 민감한 금액이 링크에 포함되는지 확인해주세요.</p>
      </section>
      <nav className="fm-policy-links" aria-label="정책 및 문의">
        <a href="/privacy.html">개인정보처리방침</a>
        <a href="/disclaimer.html">면책 안내</a>
        <a href="/guide/">은퇴 백과</a>
        <a href="/contact.html">문의</a>
      </nav>
    </main>
  );
}
