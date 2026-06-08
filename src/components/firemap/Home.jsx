import Header from './Header.jsx';

export default function Home({ onStart }) {
  return (
    <main className="fm-screen fm-home-v3">
      <Header tag="1분 계산" />
      <section className="fm-home-hero-card">
        <div className="fm-home-brand"><span aria-hidden="true">🔥</span><b>파이어맵</b></div>
        <p>퇴사나이 계산기</p>
        <h1>내 돈은 몇 살까지<br />버틸 수 있을까?</h1>
        <span>자산, 생활비, 수익률, 국민연금으로 나의 FIRE 시점을 계산해보세요.</span>
        <button type="button" onClick={onStart}>1분 만에 계산하기</button>
      </section>
      <section className="fm-home-mini-card">
        <strong>입력값은 기기 안에서 계산돼요</strong>
        <p>공유 전에는 민감한 금액이 링크에 포함되는지 확인해주세요.</p>
      </section>
      <nav className="fm-policy-links" aria-label="정책 및 문의">
        <a href="/privacy.html">개인정보처리방침</a>
        <a href="/disclaimer.html">면책 안내</a>
        <a href="/contact.html">문의</a>
      </nav>
    </main>
  );
}
