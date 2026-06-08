import Header from './Header.jsx';

export default function Home({ onStart }) {
  return (
    <main className="fm-screen">
      <Header tag="2분 계산" />
      <section className="fm-hero">
        <p>퇴사나이 계산기</p>
        <h1>내 돈은 몇 살까지 버틸까?</h1>
        <span>퇴사나이와 FIRE를 앞당기는 방법을 2분 만에 계산해보세요.</span>
        <button type="button" onClick={onStart}>시작하기</button>
      </section>
      <section className="fm-card fm-two">
        <strong>입력값은 브라우저에만 저장</strong>
        <strong>투자·세무·법률 자문 아님</strong>
      </section>
      <section className="fm-card fm-text-card">
        <b>민감한 금액은 공유 전 확인해주세요</b>
        <p>내 조건 링크를 공유하면 일부 입력값이 링크에 포함될 수 있어요.</p>
      </section>
    </main>
  );
}
