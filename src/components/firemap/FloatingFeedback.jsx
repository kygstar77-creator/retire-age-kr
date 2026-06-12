import { useState } from 'react';
import { sendFeedback } from '../../utils/firemapFeedbackApi.js';

export default function FloatingFeedback() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');

  const close = () => { setOpen(false); setSent(false); setError(''); setMessage(''); };

  const submit = async (event) => {
    event.preventDefault();
    const text = message.trim().slice(0, 240);
    if (!text || sending) return;
    setSending(true);
    setError('');
    try {
      await sendFeedback(text, 'feedback');
      setMessage('');
      setSent(true);
    } catch {
      setError('전송에 실패했어요. 잠시 후 다시 시도해주세요.');
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      <button type="button" className="fm-feedback-fab" aria-label="의견 남기기" onClick={() => setOpen(true)} title="의견 남기기"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.6-.8L3 21l1.9-5.7A8.4 8.4 0 0 1 3.5 11.5 8.5 8.5 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/></svg></button>
      {open && (
        <div className="fm-feedback-layer" role="presentation">
          <button type="button" className="fm-feedback-dim" aria-label="의견창 닫기" onClick={close} />
          <section className="fm-feedback-sheet" role="dialog" aria-modal="true" aria-label="파이어맵 익명 의견창">
            <div className="fm-feedback-head">
              <div>
                <p className="fm-kicker">파이어맵에 의견 보내기</p>
                <h2>{sent ? '고마워요! 🙏' : '불편한 점·아이디어를 알려주세요'}</h2>
              </div>
              <button type="button" aria-label="닫기" onClick={close}>×</button>
            </div>
            {sent ? (
              <div className="fm-feedback-thanks">
                <p className="fm-feedback-safe">보내주셔서 감사해요. 빠르게 살펴볼게요. 더 좋은 파이어맵을 만들게요!</p>
                <button type="button" className="fm-feedback-done" onClick={close}>닫기</button>
              </div>
            ) : (
              <>
                <p className="fm-feedback-safe">개발자에게만 전달되는 <b>비공개</b> 의견이에요. 개인정보·구체적 금융정보는 남기지 마세요. (다른 사람과 나눌 한마디는 ‘커뮤니티’ 탭에서)</p>
                {error && <p className="fm-feedback-error">{error}</p>}
                <form className="fm-feedback-form" onSubmit={submit}>
                  <textarea value={message} onChange={(event) => setMessage(event.target.value)} maxLength={240} placeholder="예: OO 화면에서 OO가 불편해요 / OO 기능이 있으면 좋겠어요" aria-label="의견 입력" />
                  <button type="submit" disabled={sending || !message.trim()}>{sending ? '보내는 중' : '보내기'}</button>
                </form>
              </>
            )}
          </section>
        </div>
      )}
    </>
  );
}
