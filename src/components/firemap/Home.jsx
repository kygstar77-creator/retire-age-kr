import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import DailyFire from './DailyFire.jsx';
import FeedbackButton from './FeedbackButton.jsx';
import { track } from '../../firemap-v2/dailyData.js';
import FirePlan from './FirePlan.jsx';
import InstallButton from './InstallButton.jsx';

function readChallenge() {
  try {
    const q = new URLSearchParams(window.location.search || '');
    if (q.get('from') !== 'share') return null;
    const ea = parseInt(q.get('ea') || '', 10);
    const pos = parseInt(q.get('pos') || '', 10);
    const tot = parseInt(q.get('tot') || '', 10);
    const pct = (pos > 0 && tot > 0) ? Math.max(1, Math.round((pos / tot) * 100)) : null;
    if (!ea && !pct) return null;
    return { ea: ea || null, pos: pos || null, tot: tot || null, pct };
  } catch { return null; }
}

export default function Home({ onStart, onMove, simulation, onChange }) {
  const [agg, setAgg] = useState(null);
  const [age, setAge] = useState(35);
  const [challenge] = useState(readChallenge);
  useEffect(() => {
    if (challenge) {
      try { track('share_inbound', { ea: challenge.ea || 0, pct: challenge.pct || 0 }); } catch { /* ignore */ }
    }
  }, [challenge]);
  useEffect(() => {
    let alive = true;
    fetchAggregates().then((a) => { if (alive) setAgg(a); });
    return () => { alive = false; };
  }, []);

  const latest = getLatestRank();
  const proof = agg && agg.total > 0
    ? `${agg.total.toLocaleString()}명이 이미 계산했어요${agg.avgEarliest ? ` · 전체 평균 파이어 ${agg.avgEarliest}세` : ''}`
    : '';
  const setClamp = (v) => setAge(Math.max(19, Math.min(80, v)));

  if (latest) return <FirePlan simulation={simulation} onMove={onMove} onChange={onChange} asHome />;

  return (
    <main className="fm-screen fm-home-v3 fm-has-tabbar">
      <Header tag="1분 계산" />
      {challenge && (
        <section className="fm-challenge" aria-label="친구가 보낸 파이어 도전">
          <span className="fm-challenge-kicker">🔥 친구가 보낸 파이어 도전</span>
          <p className="fm-challenge-main">
            {challenge.ea ? <>친구는 <b>{challenge.ea}세</b>에 파이어 가능</> : '친구가 파이어 등수를 보냈어요'}
          </p>
          {challenge.pct != null && (
            <p className="fm-challenge-rank">
              {challenge.pos && challenge.tot
                ? <>함께 계산한 {challenge.tot.toLocaleString()}명 중 <b>{challenge.pos.toLocaleString()}등</b> · 또래 상위 <b>{challenge.pct}%</b></>
                : <>또래 상위 <b>{challenge.pct}%</b></>}
            </p>
          )}
          <p className="fm-challenge-cta-line">당신은 몇 살에 가능할까요? 아래에서 1분이면 확인돼요 ↓</p>
        </section>
      )}
      <section className="fm-home-hero-card">
        <p>파이어맵</p>
        <h1>나는 몇 살에<br />파이어할 수 있을까?</h1>
        <span>물가·국민연금·건강보험료·세금까지 반영한 <b>가장 현실적인 계산</b>이에요. 자산·생활비만 넣으면 1분이면 나와요.</span>
        <div className="fm-home-age">
          <label htmlFor="fm-home-age-in">지금 몇 살인가요?</label>
          <div className="fm-home-age-ctrl">
            <button type="button" className="fm-age-btn" aria-label="나이 감소" onClick={() => setClamp(age - 1)}>−</button>
            <div className="fm-age-display">
              <input id="fm-home-age-in" className="fm-age-input" inputMode="numeric" value={age} onChange={(e) => setClamp(Number(String(e.target.value).replace(/[^0-9]/g, '')) || 0)} />
              <span className="fm-age-unit">세</span>
            </div>
            <button type="button" className="fm-age-btn" aria-label="나이 증가" onClick={() => setClamp(age + 1)}>+</button>
          </div>
        </div>
        <button type="button" className="fm-home-cta" onClick={() => { track('start_calc', { age, from: challenge ? 'share' : 'home' }); onStart(age); }}>{challenge ? '나도 계산하고 친구랑 비교하기 →' : '내 파이어 나이 계산하기 →'}</button>
        {proof && <p className="fm-home-proof">{proof}</p>}
      </section>
      <section className="fm-why" aria-label="파이어맵이 다른 이유">
        <p className="fm-why-cap">🔍 다른 계산기는 안 보여줘요</p>
        <div className="fm-why-grid">
          <span>✅ 물가 상승 반영</span>
          <span>✅ 국민연금 반영</span>
          <span>✅ 은퇴 후 건강보험료</span>
          <span>✅ 세금까지 반영</span>
        </div>
      </section>
      <InstallButton />
      <DailyFire onMove={onMove} />
      <section className="fm-home-mini-card">
        <strong>입력값은 기기 안에서 계산돼요</strong>
        <p>공유 전에는 민감한 금액이 링크에 포함되는지 확인해주세요.</p>
      </section>
      <nav className="fm-policy-links" aria-label="정책 및 문의">
        <a href="/privacy.html">개인정보처리방침</a>
        <a href="/disclaimer.html">면책 안내</a>
        <a href="/guide/">파이어 백과</a>
        <a href="/contact.html">문의</a>
        <FeedbackButton />
      </nav>
    </main>
  );
}
