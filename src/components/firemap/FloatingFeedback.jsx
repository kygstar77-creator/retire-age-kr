import { useEffect, useMemo, useState } from 'react';
import { loadFeedback, sendFeedback } from '../../utils/firemapFeedbackApi.js';

function relativeTime(value) {
  const diff = Math.max(1, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (diff < 60) return `${diff}분 전`;
  const hours = Math.round(diff / 60);
  if (hours < 24) return `${hours}시간 전`;
  return `${Math.round(hours / 24)}일 전`;
}

export default function FloatingFeedback() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [items, setItems] = useState([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const visibleItems = useMemo(() => items.slice(0, 20), [items]);

  useEffect(() => {
    let alive = true;
    loadFeedback().then((rows) => { if (alive) setItems(rows); });
    return () => { alive = false; };
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    const text = message.trim().slice(0, 240);
    if (!text || sending) return;
    setSending(true);
    setError('');
    try {
      const created = await sendFeedback(text);
      if (created) setItems((current) => [created, ...current]);
      setMessage('');
    } catch {
      setError('저장에 실패했어요. 잠시 후 다시 시도해주세요.');
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      <button type="button" className="fm-feedback-fab" aria-label="의견 남기기" onClick={() => setOpen(true)} title="의견 남기기"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.6-.8L3 21l1.9-5.7A8.4 8.4 0 0 1 3.5 11.5 8.5 8.5 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/></svg></button>
      {open && (
        <div className="fm-feedback-layer" role="presentation">
          <button type="button" className="fm-feedback-dim" aria-label="의견창 닫기" onClick={() => setOpen(false)} />
          <section className="fm-feedback-sheet" role="dialog" aria-modal="true" aria-label="파이어맵 익명 의견창">
            <div className="fm-feedback-head">
              <div>
                <p className="fm-kicker">파이어맵 의견</p>
                <h2>불편한 점을 남겨주세요</h2>
              </div>
              <button type="button" aria-label="닫기" onClick={() => setOpen(false)}>×</button>
            </div>
            <p className="fm-feedback-safe">익명 의견만 저장돼요. 개인정보나 구체적인 금융정보는 남기지 마세요.</p>
            <div className="fm-feedback-list" aria-label="익명 의견 목록">
              {visibleItems.length === 0 ? (
                <div className="fm-feedback-empty">아직 등록된 의견이 없어요.</div>
              ) : visibleItems.map((item) => (
                <article key={item.id}>
                  <div><strong>{item.nickname || '익명'}</strong><small>{relativeTime(item.created_at)}</small></div>
                  <p>{item.message}</p>
                </article>
              ))}
            </div>
            {error && <p className="fm-feedback-error">{error}</p>}
            <form className="fm-feedback-form" onSubmit={submit}>
              <textarea value={message} onChange={(event) => setMessage(event.target.value)} maxLength={240} aria-label="의견 입력" />
              <button type="submit" disabled={sending}>{sending ? '등록 중' : '등록'}</button>
            </form>
          </section>
        </div>
      )}
    </>
  );
}
