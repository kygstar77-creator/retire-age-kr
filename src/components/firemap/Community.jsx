import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { loadFeedback, sendFeedback } from '../../utils/firemapFeedbackApi.js';

function relativeTime(value) {
  const diff = Math.max(1, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (diff < 60) return `${diff}분 전`;
  const hours = Math.round(diff / 60);
  if (hours < 24) return `${hours}시간 전`;
  return `${Math.round(hours / 24)}일 전`;
}

export default function Community({ onBack }) {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');

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
    <main className="fm-screen fm-scroll">
      <Header tag="커뮤니티" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">결과 이후</p>
        <h2>다른 사람들의 한마디</h2>
        <p>익명으로 남기는 공간이에요. 입력한 금융 금액은 저장하지 않고, 남긴 글만 보여요.</p>
      </section>
      <form className="fm-card fm-community-form" onSubmit={submit}>
        <label htmlFor="fm-community-input">한마디 남기기</label>
        <textarea id="fm-community-input" maxLength={240} value={message} onChange={(event) => setMessage(event.target.value)} placeholder="예: 생활비를 줄이니 은퇴가 5년 당겨지네요." />
        <div className="fm-community-form-row">
          <small>{message.length}/240 · 익명</small>
          <button type="submit" disabled={sending || !message.trim()}>{sending ? '등록 중' : '등록'}</button>
        </div>
        {error && <small className="fm-community-error">{error}</small>}
      </form>
      <section className="fm-card fm-community-list">
        {items.length === 0 && <p className="fm-community-empty">첫 한마디를 남겨보세요.</p>}
        {items.map((item) => (
          <article className="fm-community-item" key={item.id}>
            <p>{item.message}</p>
            <small>{item.nickname || '익명'} · {relativeTime(item.created_at)}</small>
          </article>
        ))}
      </section>
    </main>
  );
}
