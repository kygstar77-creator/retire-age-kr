import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { account } from '../../utils/identity.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import DailyFire from './DailyFire.jsx';
import FeedbackButton from './FeedbackButton.jsx';
import { track } from '../../firemap-v2/dailyData.js';
import FirePlan from './FirePlan.jsx';
import InstallButton from './InstallButton.jsx';
import IdentityLine from './IdentityLine.jsx';

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

  // 계산 이력이 있으면 재방문 시 홈을 '파이어 플랜 대시보드'로. (로그인 여부 무관 — 기록은 로컬에 있고,
  // 로그인은 대시보드 안 fm-acct-bar에서 '기록 지키기'로 유도해 발견→로그인 동선을 만든다.)
  // 단, 친구 공유로 들어온 도전(challenge) 방문은 랜딩+도전 카드를 그대로 보여준다.
  if (latest && !challenge) return <FirePlan simulation={simulation} onMove={onMove} onChange={onChange} asHome />;

  return (
    <main className="fm-screen fm-home-v3 fm-has-tabbar">
      <Header tag="1분 계산" />
      <IdentityLine onMove={onMove} />
      {latest && (
        <button type="button" className="fm-recent-rank" onClick={() => { window.location.hash = '#result'; }}>
          <span className="fm-recent-label">최근 계산 결과</span>
          <span className="fm-recent-main">{latest.earliest ? `${latest.earliest}세에 파이어 가능` : '내 파이어 결과 보기'}</span>
          <span className="fm-recent-sub">로그인하면 이 결과·기록이 저장돼요 · 다시 보기 ›</span>
        </button>
      )}
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
        <span>물가·국민연금까지 반영하는 <b>가장 현실적인 파이어 계산</b>이에요. 파이어 후 건보료·세금은 도구로 따로 점검해요. 자산·생활비만 넣으면 1분.</span>
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
      <section className="fm-card" style={{ borderColor: 'rgba(255,90,0,0.3)' }}>
        <p className="fm-kicker">🔥 숫자 하나로 끝이 아니에요</p>
        <h2 style={{ margin: '2px 0 10px' }}>계산 다음, 파이어 여정이 시작돼요</h2>
        <p style={{ fontSize: '13px', color: 'var(--fm-muted, #6b6f76)', lineHeight: 1.6, margin: 0 }}>
          파이어맵은 물가·국민연금·건보료·세금까지 반영한 현실적인 계산으로 끝나지 않아요. 지금 내가 어느 단계인지, 다음 한 걸음은 무엇인지 — <b>목표까지 가는 길 전체를 지도로</b> 안내하고, 내 기록을 한 곳에 모아 계속 관리해요.
        </p>
      </section>
      <nav className="fm-policy-links" aria-label="정책 및 문의">
        <a href="/privacy.html">개인정보처리방침</a>
        <a href="/disclaimer.html">면책 안내</a>
        <a href="/contact.html">문의</a>
        <FeedbackButton />
      </nav>
    </main>
  );
}
