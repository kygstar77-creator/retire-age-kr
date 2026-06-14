import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { loadCommunityThread, sendCommunity, likeCommunity, editCommunity, deleteCommunity } from '../../utils/firemapFeedbackApi.js';
import { funHandle } from '../../firemap-v2/funName.js';
import { identityIds } from '../../utils/identity.js';
import AccountCard from './AccountCard.jsx';

function relativeTime(value) {
  const diff = Math.max(1, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (diff < 60) return `${diff}분 전`;
  const hours = Math.round(diff / 60);
  if (hours < 24) return `${hours}시간 전`;
  return `${Math.round(hours / 24)}일 전`;
}
const likedKey = (id) => `fm_liked_${id}`;
const isLiked = (id) => { try { return !!localStorage.getItem(likedKey(id)); } catch { return false; } };

const MINE_KEY = 'fm_my_posts';
const loadMine = () => { try { return JSON.parse(localStorage.getItem(MINE_KEY) || '[]'); } catch { return []; } };
const addMine = (id) => { try { const m = loadMine(); if (!m.includes(id)) localStorage.setItem(MINE_KEY, JSON.stringify([...m, id])); } catch { /* ignore */ } };

function myNickname() {
  try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; }
}

// 입력창 포커스 유지를 위해 컴포넌트를 모듈 스코프에 정의(부모 리렌더 시 remount 방지)
function OwnerControls({ mine, row, onEdit, onDelete }) {
  if (!mine) return null;
  return (
    <span className="fm-post-own">
      <button type="button" className="fm-post-edit" onClick={() => onEdit(row)}>수정</button>
      <button type="button" className="fm-post-del" onClick={() => onDelete(row)}>삭제</button>
    </span>
  );
}

function EditBox({ id, value, onChange, onCancel, onSave }) {
  return (
    <div className="fm-post-edit-box">
      <textarea maxLength={240} value={value} onChange={(e) => onChange(e.target.value)} autoFocus />
      <div className="fm-post-edit-row">
        <button type="button" className="fm-post-edit-cancel" onClick={onCancel}>취소</button>
        <button type="button" className="fm-post-edit-save" onClick={() => onSave(id)} disabled={!value.trim()}>저장</button>
      </div>
    </div>
  );
}

export default function Community({ onBack }) {
  const [rows, setRows] = useState([]);
  const [post, setPost] = useState('');
  const [sending, setSending] = useState(false);
  const [openId, setOpenId] = useState(null);
  const [replyText, setReplyText] = useState('');
  const [mine, setMine] = useState(loadMine());
  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState('');

  useEffect(() => {
    let alive = true;
    loadCommunityThread().then((r) => { if (alive) setRows(r); });
    return () => { alive = false; };
  }, []);

  const nick = myNickname();
  const myIds = identityIds();
  // '내 글' 판별: 이 기기에서 올린 글 ID(localStorage) 또는 기기 고유 client_id 일치. 닉네임은 중복될 수 있어 쓰지 않음.
  const isMine = (row) => mine.includes(row.id) || (!!row.client_id && myIds.includes(row.client_id));
  const remember = (id) => { addMine(id); setMine(loadMine()); };

  const posts = rows.filter((r) => !r.parent_id).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  const repliesOf = (id) => rows.filter((r) => r.parent_id === id).sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  const submitPost = async (event) => {
    event.preventDefault();
    const text = post.trim().slice(0, 240);
    if (!text || sending) return;
    setSending(true);
    const created = await sendCommunity(text, null);
    setSending(false);
    if (created) { setRows((r) => [...r, { ...created, parent_id: null, likes: 0 }]); remember(created.id); setPost(''); }
  };

  const submitReply = async (parentId) => {
    const text = replyText.trim().slice(0, 240);
    if (!text) return;
    const created = await sendCommunity(text, parentId);
    if (created) { setRows((r) => [...r, { ...created, parent_id: parentId, likes: 0 }]); remember(created.id); setReplyText(''); }
  };

  const like = async (row) => {
    if (isLiked(row.id)) return;
    const ok = await likeCommunity(row.id, row.likes || 0);
    if (ok) {
      try { localStorage.setItem(likedKey(row.id), '1'); } catch { /* ignore */ }
      setRows((r) => r.map((x) => (x.id === row.id ? { ...x, likes: (x.likes || 0) + 1 } : x)));
    }
  };

  const startEdit = (row) => { setEditId(row.id); setEditText(row.message); };
  const cancelEdit = () => { setEditId(null); setEditText(''); };
  const saveEdit = async (id) => {
    const text = editText.trim().slice(0, 240);
    if (!text) return;
    const ok = await editCommunity(id, text);
    if (ok) {
      setRows((r) => r.map((x) => (x.id === id ? { ...x, message: text } : x)));
      cancelEdit();
    }
  };
  const removeRow = async (row) => {
    if (!window.confirm('이 글을 삭제할까요? 되돌릴 수 없어요.')) return;
    const ok = await deleteCommunity(row.id);
    if (ok) {
      setRows((r) => r.filter((x) => x.id !== row.id && x.parent_id !== row.id));
      if (editId === row.id) cancelEdit();
    }
  };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="커뮤니티" onBack={onBack} />
      <AccountCard />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">파이어족 라운지</p>
        <h2>다 같이 파이어 이야기</h2>
        <p>닉네임으로 글 쓰고, 답글로 서로 대화해요. 내가 쓴 글은 수정·삭제할 수 있어요. 버그·불편 신고는 홈 맨 아래 ‘의견 보내기’로.</p>
      </section>

      <form className="fm-card fm-community-form" onSubmit={submitPost}>
        <label htmlFor="fm-community-input">새 글 쓰기</label>
        <textarea id="fm-community-input" maxLength={240} value={post} onChange={(e) => setPost(e.target.value)} placeholder="예: 생활비를 줄이니 파이어가 5년 당겨졌어요. 다들 어떻게 아끼세요?" />
        <div className="fm-community-form-row">
          <small>{post.length}/240 · {nick ? `${nick} 으로 게시` : '닉네임 자동 생성'}</small>
          <button type="submit" disabled={sending || !post.trim()}>{sending ? '올리는 중' : '글 올리기'}</button>
        </div>
      </form>

      <section className="fm-community-feed">
        {posts.length === 0 && <p className="fm-community-empty">아직 글이 없어요. 첫 글을 남기면 다른 파이어족들이 답글로 응원해줘요 🔥</p>}
        {posts.map((p) => {
          const reps = repliesOf(p.id);
          const open = openId === p.id;
          return (
            <article className="fm-card fm-post" key={p.id}>
              {editId === p.id ? <EditBox id={p.id} value={editText} onChange={setEditText} onCancel={cancelEdit} onSave={saveEdit} /> : <p className="fm-post-msg">{p.message}</p>}
              <div className="fm-post-meta">
                <span className="fm-post-author">{p.nickname || funHandle(p.id)} · {relativeTime(p.created_at)}</span>
                <div className="fm-post-actions">
                  <OwnerControls mine={isMine(p)} row={p} onEdit={startEdit} onDelete={removeRow} />
                  <button type="button" className={`fm-post-like${isLiked(p.id) ? ' on' : ''}`} onClick={() => like(p)} aria-label="공감">♥ {p.likes || 0}</button>
                  <button type="button" className="fm-post-reply" onClick={() => { setOpenId(open ? null : p.id); setReplyText(''); }}>💬 {reps.length}</button>
                </div>
              </div>
              {open && (
                <div className="fm-replies">
                  {reps.map((r) => (
                    <div className="fm-reply" key={r.id}>
                      {editId === r.id ? <EditBox id={r.id} value={editText} onChange={setEditText} onCancel={cancelEdit} onSave={saveEdit} /> : <p>{r.message}</p>}
                      <div className="fm-reply-meta">
                        <small>{r.nickname || funHandle(r.id)} · {relativeTime(r.created_at)}</small>
                        <OwnerControls mine={isMine(r)} row={r} onEdit={startEdit} onDelete={removeRow} />
                      </div>
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
