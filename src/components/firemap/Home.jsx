import Header from './Header.jsx';
import { getLatestRank, getRankChange } from '../../firemap-v2/rankHistory.js';
import DailyFire from './DailyFire.jsx';

export default function Home({ onStart }) {
  return (
    <main className="fm-screen fm-home-v3">
      <Header tag="1분 계산" />
      {(() => {
        const latest = getLatestRank();
        if (!latest) return null;
        const change = getRankChange();
        const goResult = () => { window.location.hash = '#result'; };
        return (
          <button type="button" className="fm-recent-rank" onClick={goResult}>
            <span className="fm-recent-label">내 최근 등수</span>
            <span className="fm-recent-main">또래 상위 {latest.percentile}% · {latest.grade}등급</span>
            <span className="fm-recent-sub">
              {change && change.deltaPercentile !== 0
                ? `지난번보다 ${Math.abs(change.deltaPercentile)}%p ${change.deltaPercentile > 0 ? '상승 ▲' : '하락 ▼'} · 다시 확인하기 ›`
                : '다시 확인하기 ›'}
            </span>
          </button>
        );
      })()}
      <section className="fm-home-hero-card">
        <p>퇴사나이 계산기</p>
        <h1>내 돈은 몇 살까지<br />버틸 수 있을까?</h1>
        <span>자산, 생활비, 수익률, 국민연금으로 나의 FIRE 시점을 계산해보세요.</span>
        <button type="button" onClick={onStart}>1분 만에 계산하기</button>
      </section>
      <DailyFire />
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
