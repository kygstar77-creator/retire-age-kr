// 결과 ↔ 바꿔보기 세그먼트 (홈 안에서 한 번에 토글)
export default function ResultSimTabs({ current }) {
  const go = (h) => { try { window.location.hash = h; } catch { /* ignore */ } };
  return (
    <div className="fm-rs-tabs" role="tablist" aria-label="결과/바꿔보기">
      <button type="button" role="tab" aria-selected={current === 'result'} className={current === 'result' ? 'on' : ''} onClick={() => go('#result')}>📊 내 결과</button>
      <button type="button" role="tab" aria-selected={current === 'sim'} className={current === 'sim' ? 'on' : ''} onClick={() => go('#experiment')}>🎛️ 바꿔보기</button>
      <button type="button" className="fm-rs-new" onClick={() => go('#home')}>새로 계산</button>
    </div>
  );
}
