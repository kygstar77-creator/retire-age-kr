import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { loadCommunityThread, sendCommunity, likeCommunity } from '../../utils/firemapFeedbackApi.js';
import { funHandle } from '../../firemap-v2/funName.js';

function relativeTime(value) {
  const diff = Math.max(1, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (diff < 60) return `${diff}분 전`;
  const hours = Math.round(diff / 60);
  if (hours < 24) return `${hours}시간 전`;
  return `${Math.round(hours / 24)}일 전`;
}
const likedKey = (id) => `fm_liked_${id}`;
const isLiked = (id) => { try { return !!localStorage.getItem(likedKey(id)); } catch { return false; } };

export default function Community({ onBack }) {
  const [rows, setRows] = useState([]);
  const [post, setPost] = useState('');
  const [sending, setSending] = useState(false);
  const [openId, setOpenId] = useState(null);
  const [replyText, setReplyText] = useState('');

  useEffect(() => {
    let alive = true;
    loadCommunityThread().then((r) => { if (alive) setRows(r); });
    return () => { alive = false; };
  }, []);

  const posts = rows.filter((r) => !r.parent_id).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  const repliesOf = (id) => rows.filter((r) => r.parent_id === id).sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  const submitPost = async (event) => {
    event.preventDefault();
    const text = post.trim().slice(0, 240);
    if (!text || sending) return;
    setSending(true);
    const created = await sendCommunity(text, null);
    setSending(false);
    if (created) { setRows((r) => [...r, { ...created, parent_id: null, likes: 0 }]); setPost(''); }
  };

  const submitReply = async (parentId) => {
    const text = replyText.trim().slice(0, 240);
    if (!text) return;
    const created = await sendCommunity(text, parentId);
    if (created) { setRows((r) => [...r, { ...created, parent_id: parentId, likes: 0 }]); setReplyText(''); }
  };

  const like = async (row) => {
    if (isLiked(row.id)) return;
    const ok = await likeCommunity(row.id, row.likes || 0);
    if (ok) {
      try { localStorage.setItem(likedKey(row.id), '1'); } catch { /* ignore */ }
      setRows((r) => r.map((x) => (x.id === row.id ? { ...x, likes: (x.likes || 0) + 1 } : x)));
    }
  };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="커뮤니티" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">파이어족 라운지</p>
        <h2>다 같이 파이어 이야기</h2>
        <p>익명으로 글 쓰고, 답글로 서로 대화해요. 버그·불편 신고는 홈 화면 맨 아래 ‘의견 보내기’로.</p>
      </section>

      <form className="fm-card fm-community-form" onSubmit={submitPost}>
        <label htmlFor="fm-community-input">새 글 쓰기</label>
        <textarea id="fm-community-input" maxLength={240} value={post} onChange={(e) => setPost(e.target.value)} placeholder="예: 생활비를 줄이니 은퇴가 5년 당겨졌어요. 다들 어떻게 아끼세요?" />
        <div className="fm-community-form-row">
          <small>{post.length}/240 · 익명</small>
          <button type="submit" disabled={sending || !post.trim()}>{sending ? '올리는 중' : '글 올리기'}</button>
        </div>
      </form>

      <section className="fm-community-feed">
        {posts.length === 0 && <p className="fm-community-empty">첫 글을 남겨보세요.</p>}
        {posts.map((p) => {
          const reps = repliesOf(p.id);
          const open = openId === p.id;
          return (
            <article className="fm-card fm-post" key={p.id}>
              <p className="fm-post-msg">{p.message}</p>
              <div className="fm-post-meta">
                <span className="fm-post-author">{p.nickname || funHandle(p.id)} · {relativeTime(p.created_at)}</span>
                <div className="fm-post-actions">
                  <button type="button" className={`fm-post-like${isLiked(p.id) ? ' on' : ''}`} onClick={() => like(p)} aria-label="공감">♥ {p.likes || 0}</button>
                  <button type="button" className="fm-post-reply" onClick={() => { setOpenId(open ? null : p.id); setReplyText(''); }}>💬 {reps.length}</button>
                </div>
              </div>
              {open && (
                <div className="fm-replies">
                  {reps.map((r) => (
                    <div className="fm-reply" key={r.id}>
                      <p>{r.message}</p>
                      <small>{r.nickname || funHandle(r.id)} · {relativeTime(r.created_at)}</small>
                    </div>
                  ))}
                  <div className="fm-reply-input">
                    <input maxLength={240} value={replyText} onChange={(e) => setReplyText(e.target.value)} placeholder="답글 달기…" onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); submitReply(p.id); } }} />
                    <button type="button" onClick={() => submitReply(p.id)} disabled={!replyText.trim()}>등록</button>
                  </div>
                </div>
              )}
            </article>
          );
        })}
      </section>
    </main>
  );
}
