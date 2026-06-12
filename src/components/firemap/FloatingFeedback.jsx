import { useState } from 'react';
import { sendCommunity } from '../../utils/firemapFeedbackApi.js';

// 플로팅 FAB = 커뮤니티 '한마디 쓰기'(공개 참여 유도). 비공개 의견은 홈 푸터 '의견 보내기'로.
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
      const created = await sendCommunity(text);
      if (created) { setSent(true); setMessage(''); }
      else setError('전송에 실패했어요. 잠시 후 다시 시도해주세요.');
    } catch {
      setError('전송에 실패했어요. 잠시 후 다시 시도해주세요.');
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      <button type="button" className="fm-feedback-fab fm-fab-write" aria-label="커뮤니티에 한마디 쓰기" onClick={() => setOpen(true)} title="한마디 쓰기"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z" /></svg></button>
      {open && (
        <div className="fm-feedback-layer" role="presentation">
          <button type="button" className="fm-feedback-dim" aria-label="닫기" onClick={close} />
          <section className="fm-feedback-sheet" role="dialog" aria-modal="true" aria-label="커뮤니티 한마디">
            <div className="fm-feedback-head">
              <div>
                <p className="fm-kicker">커뮤니티</p>
                <h2>{sent ? '올라갔어요! 🎉' : '파이어 한마디 남기기'}</h2>
              </div>
              <button type="button" aria-label="닫기" onClick={close}>×</button>
            </div>
            {sent ? (
              <div className="fm-feedback-thanks">
                <p className="fm-feedback-safe">커뮤니티에 올라갔어요. 다른 사람들에게도 힘이 돼요!</p>
                <button type="button" className="fm-feedback-done" onClick={() => { window.location.hash = '#community'; close(); }}>커뮤니티 보러가기</button>
              </div>
            ) : (
              <>
                <p className="fm-feedback-safe">공개로 올라가요. 개인정보·구체적 금융정보는 남기지 마세요. (버그·불편 신고는 홈 하단 ‘의견 보내기’로)</p>
                {error && <p className="fm-feedback-error">{error}</p>}
                <form className="fm-feedback-form" onSubmit={submit}>
                  <textarea value={message} onChange={(e) => setMessage(e.target.value)} maxLength={240} placeholder="예: 생활비 줄이니 은퇴가 5년 당겨졌어요!" aria-label="한마디 입력" />
                  <button type="submit" disabled={sending || !message.trim()}>{sending ? '올리는 중' : '올리기'}</button>
                </form>
              </>
            )}
          </section>
        </div>
      )}
    </>
  );
}
