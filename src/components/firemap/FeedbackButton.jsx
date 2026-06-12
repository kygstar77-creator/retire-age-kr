import { useState } from 'react';
import { sendFeedback } from '../../utils/firemapFeedbackApi.js';

export default function FeedbackButton() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);
  const close = () => { setOpen(false); setSent(false); setMessage(''); };

  const submit = async (event) => {
    event.preventDefault();
    const text = message.trim().slice(0, 240);
    if (!text || sending) return;
    setSending(true);
    try { await sendFeedback(text, 'feedback'); setSent(true); setMessage(''); } catch { /* ignore */ } finally { setSending(false); }
  };

  return (
    <>
      <button type="button" className="fm-policy-fbtn" onClick={() => setOpen(true)}>의견 보내기</button>
      {open && (
        <div className="fm-feedback-layer" role="presentation">
          <button type="button" className="fm-feedback-dim" aria-label="닫기" onClick={close} />
          <section className="fm-feedback-sheet" role="dialog" aria-modal="true" aria-label="비공개 의견">
            <div className="fm-feedback-head">
              <div>
                <p className="fm-kicker">비공개 의견</p>
                <h2>{sent ? '고마워요! 🙏' : '불편한 점·아이디어를 알려주세요'}</h2>
              </div>
              <button type="button" aria-label="닫기" onClick={close}>×</button>
            </div>
            {sent ? (
              <div className="fm-feedback-thanks">
                <p className="fm-feedback-safe">보내주셔서 감사해요. 빠르게 살펴볼게요!</p>
                <button type="button" className="fm-feedback-done" onClick={close}>닫기</button>
              </div>
            ) : (
              <>
                <p className="fm-feedback-safe">개발자에게만 전달되는 <b>비공개</b> 의견이에요. 커뮤니티에는 안 올라가요.</p>
                <form className="fm-feedback-form" onSubmit={submit}>
                  <textarea value={message} onChange={(e) => setMessage(e.target.value)} maxLength={240} placeholder="예: OO 화면에서 OO가 불편해요 / OO 기능이 있으면 좋겠어요" aria-label="의견 입력" />
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
