import Header from './Header.jsx';

export default function Home({ onStart }) {
  return (
    <main className="fm-screen">
      <Header tag="2분 계산" />
      <section className="fm-hero">
        <p>퇴사나이 계산기</p>
        <h1>내 돈은 몇 살까지 버틸까?</h1>
        <span>퇴사나이와 파이어를 앞당기는 방법을 2분 만에 계산해보세요.</span>
        <button type="button" onClick={onStart}>시작하기</button>
      </section>
      <section className="fm-card fm-two">
        <strong>입력값은 브라우저에만 저장</strong>
        <strong>참고용 계산</strong>
      </section>
    </main>
  );
}
