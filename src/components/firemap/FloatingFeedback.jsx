import { useEffect, useMemo, useState } from 'react';
import { feedbackReady, loadFeedback, sendFeedback } from '../../utils/firemapFeedbackApi.js';

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
    const created = await sendFeedback(text);
    if (created) setItems((current) => [created, ...current]);
    setMessage('');
    setSending(false);
  };

  return (
    <>
      <button type="button" className="fm-feedback-fab" aria-label="의견 남기기" onClick={() => setOpen(true)}>의견 남기기</button>
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
            <p className="fm-feedback-safe">익명 의견만 저장돼요. 개인정보, 자산, 계좌, 연락처는 입력하지 마세요. {feedbackReady ? 'Supabase에 연결됐어요.' : '연결 전에는 예시 의견으로 표시돼요.'}</p>
            <div className="fm-feedback-list" aria-label="익명 의견 목록">
              {visibleItems.map((item) => (
                <article key={item.id}>
                  <div><strong>{item.nickname || '익명'}</strong><small>{relativeTime(item.created_at)}</small></div>
                  <p>{item.message}</p>
                </article>
              ))}
            </div>
            <form className="fm-feedback-form" onSubmit={submit}>
              <textarea value={message} onChange={(event) => setMessage(event.target.value)} maxLength={240} placeholder="예: 결과 카드가 너무 길어요 / 국민연금 조건을 바꾸고 싶어요" />
              <button type="submit" disabled={sending}>{sending ? '등록 중' : '등록'}</button>
            </form>
          </section>
        </div>
      )}
    </>
  );
}
