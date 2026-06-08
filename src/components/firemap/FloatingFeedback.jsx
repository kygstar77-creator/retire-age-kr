import { useEffect, useMemo, useState } from 'react';

const STORAGE_KEY = 'firemap:v3:feedback';
const seedFeedback = [
  { id: 'seed-1', name: '익명', message: '결과에서 바로 조건을 고칠 수 있으면 좋아요.' },
  { id: 'seed-2', name: '익명', message: '생활비를 낮췄을 때 몇 살 늘어나는지 한눈에 보이면 좋겠어요.' }
];

function loadFeedback() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    return Array.isArray(saved) ? saved : [];
  } catch {
    return [];
  }
}

export default function FloatingFeedback() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [items, setItems] = useState(loadFeedback);
  const visibleItems = useMemo(() => [...items, ...seedFeedback].slice(0, 20), [items]);

  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); } catch { /* ignore */ }
  }, [items]);

  const submit = (event) => {
    event.preventDefault();
    const text = message.trim().slice(0, 240);
    if (!text) return;
    setItems((current) => [{ id: `local-${Date.now()}`, name: '익명', message: text }, ...current]);
    setMessage('');
  };

  return (
    <>
      <button type="button" className="fm-feedback-fab" aria-label="의견 남기기" onClick={() => setOpen(true)}>의견</button>
      {open && (
        <div className="fm-feedback-layer" role="presentation">
          <button type="button" className="fm-feedback-dim" aria-label="의견창 닫기" onClick={() => setOpen(false)} />
          <section className="fm-feedback-sheet" role="dialog" aria-modal="true" aria-label="익명 의견창">
            <div className="fm-feedback-head">
              <div>
                <p className="fm-kicker">V3 의견창</p>
                <h2>써보고 불편한 점을 남겨주세요</h2>
              </div>
              <button type="button" aria-label="닫기" onClick={() => setOpen(false)}>닫기</button>
            </div>
            <p className="fm-feedback-safe">로그인 없이 이 브라우저에만 임시 저장돼요. 구체적인 금융정보나 연락처는 남기지 마세요.</p>
            <div className="fm-feedback-list" aria-label="익명 의견 목록">
              {visibleItems.map((item) => (
                <article key={item.id}>
                  <strong>{item.name}</strong>
                  <p>{item.message}</p>
                </article>
              ))}
            </div>
            <form className="fm-feedback-form" onSubmit={submit}>
              <textarea value={message} onChange={(event) => setMessage(event.target.value)} maxLength={240} placeholder="예: 결과 카드가 너무 길어요 / 국민연금 조건을 바꾸고 싶어요" />
              <button type="submit">익명으로 남기기</button>
            </form>
          </section>
        </div>
      )}
    </>
  );
}
