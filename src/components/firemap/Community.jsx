import { useEffect, useRef, useState } from 'react';
import Header from './Header.jsx';
import { loadCommunityThread, sendCommunity, likeCommunity, editCommunity, deleteCommunity, bumpView, loadViewCounts } from '../../utils/firemapFeedbackApi.js';
import { funHandle } from '../../firemap-v2/funName.js';
import { JOURNEY_STAGES, journeyStage } from '../../utils/journeyStage.js';
import { identityIds, account } from '../../utils/identity.js';

const CATEGORIES = [
  { key: 'free', label: '자유수다', emoji: '💬' },
  { key: 'news', label: '경제뉴스', emoji: '📰' },
  { key: 'save', label: '저축꿀팁', emoji: '✂️' },
  { key: 'invest', label: '투자·자산배분', emoji: '📈' },
  { key: 'realestate', label: '부동산', emoji: '🏠' },
  { key: 'sidejob', label: '부업·N잡', emoji: '💼' },
  { key: 'pension', label: '연금·세금·건보', emoji: '🧾' },
  { key: 'life', label: '파이어 후 삶', emoji: '🌴' },
  { key: 'goal', label: '목표·인증', emoji: '🎯' },
  { key: 'qa', label: '질문·고민상담', emoji: '❓' },
  { key: 'budget', label: '가계부·지출공유', emoji: '📊' }
];
const catLabel = (k) => { const c = CATEGORIES.find((x) => x.key === k); return c ? `${c.emoji} ${c.label}` : '💬 자유수다'; };
const catOf = (row) => row.category || 'free';

// 기여 칭호 — 이미 불러온 스레드 데이터로 계산(진화·랭킹과 무관한 명예 표시)
function titleFromStats(s) {
  if (!s) return null;
  if (s.posts >= 5 || s.likes >= 10) return '⭐ 라운지 스타';
  if (s.replies >= 5) return '😇 답글 천사';
  if (s.likes >= 5) return '💖 공감 부자';
  if (s.posts >= 2) return '☕ 단골';
  return null;
}

const STYLE = `
.fm-cat-bar{display:flex;gap:8px;overflow-x:auto;padding:4px 0 10px;-webkit-overflow-scrolling:touch}
.fm-cat-bar button{flex:0 0 auto;border:1px solid #e5e7eb;background:#fff;border-radius:99px;padding:7px 12px;font-size:13px;font-weight:700;color:#4b5563;cursor:pointer;white-space:nowrap}
.fm-cat-bar button.on{background:#ff5a00;border-color:#ff5a00;color:#fff}
.fm-cat-select{margin-bottom:8px}
.fm-cat-select select{width:100%;padding:9px;border:1px solid #e5e7eb;border-radius:10px;font-size:14px;background:#fff}
.fm-cat-badge{display:inline-block;font-size:11px;font-weight:800;color:#c2410c;background:#fff4e8;border-radius:6px;padding:1px 6px;margin-right:6px}
.fm-sortbar{display:flex;gap:8px;margin-bottom:10px}
.fm-sortbar button{border:1px solid #e5e7eb;background:#fff;border-radius:99px;padding:6px 14px;font-size:13px;font-weight:700;color:#4b5563;cursor:pointer}
.fm-sortbar button.on{background:#18212c;border-color:#18212c;color:#fff}
.fm-best{border:1px solid #ffd23f !important;background:#fffdf3 !important}
.fm-best-tag{font-size:12px;font-weight:800;color:#b45309;margin:0 0 6px}
.fm-title-chip{display:inline-block;font-size:10.5px;font-weight:800;color:#1d4ed8;background:#eaf1ff;border-radius:6px;padding:1px 6px;margin-left:6px}
.fm-hot-chip{display:inline-block;font-size:10.5px;font-weight:800;color:#b91c1c;background:#fdecec;border-radius:6px;padding:1px 6px;margin-right:6px}
.fm-mytitle{font-size:12px;color:#6b7280;margin:0 0 8px}
.fm-mytitle b{color:#1d4ed8}
.fm-stage-bar{display:flex;gap:8px;overflow-x:auto;padding:2px 0 10px;-webkit-overflow-scrolling:touch}
.fm-stage-bar button{flex:0 0 auto;border:1px solid #e5e7eb;background:#fff;border-radius:99px;padding:7px 12px;font-size:13px;font-weight:700;color:#4b5563;cursor:pointer;white-space:nowrap}
.fm-stage-bar button.on{background:#1e2859;border-color:#1e2859;color:#fff}
.fm-stage-bar .fm-stage-mine{border-color:#ff8a4c;color:#c2410c}
.fm-stage-bar .fm-stage-mine.on{background:#ff5a00;border-color:#ff5a00;color:#fff}
.fm-stage-desc{font-size:12.5px;color:#565c68;background:#f6f7fb;border:1px solid #e7ebf3;border-radius:10px;padding:9px 12px;margin:0 0 10px;line-height:1.55}
.fm-stage-desc b{color:#1e2859}
.fm-stage-badge{display:inline-block;font-size:11px;font-weight:800;color:#1e2859;background:#eef1f9;border-radius:6px;padding:1px 6px;margin-right:6px}
`;

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

export default function Community({ onBack, onMove, simulation }) {
  const myJourney = (() => { try { return journeyStage(simulation || null); } catch { return null; } })();
  const myStage = myJourney ? myJourney.stage : null;
  const stageMeta = (n) => JOURNEY_STAGES.find((x) => x.n === Number(n)) || null;
  const stageOf = (row) => (row && row.stage != null ? Number(row.stage) : null);
  const [rows, setRows] = useState([]);
  const [post, setPost] = useState('');
  const [sending, setSending] = useState(false);
  const [openId, setOpenId] = useState(null);
  const [replyText, setReplyText] = useState('');
  const [mine, setMine] = useState(loadMine());
  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState('');
  const [cat, setCat] = useState('all');
  const [postCat, setPostCat] = useState('free');
  const [sort, setSort] = useState('new');
  const [stageFilter, setStageFilter] = useState('all');
  const [views, setViews] = useState({});

  useEffect(() => {
    let alive = true;
    loadCommunityThread().then((r) => { if (alive) setRows(r); });
    loadViewCounts('community').then((m) => { if (alive) setViews(m); });
    return () => { alive = false; };
  }, []);

  const nick = myNickname();
  const loggedIn = !!(account() && account().handle);
  const myIds = identityIds();
  const isMine = (row) => mine.includes(row.id) || (!!row.client_id && myIds.includes(row.client_id));
  const remember = (id) => { addMine(id); setMine(loadMine()); };
  // 글이 화면에 실제로 보이면(절반 이상 노출) 조회수 +1 — 세션당 글마다 1회.
  // 커뮤니티 글은 목록에서 본문이 바로 읽히므로 '노출 = 조회'로 집계한다.
  const seenRef = useRef(new Set());
  useEffect(() => {
    if (typeof IntersectionObserver === 'undefined') return undefined;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const id = en.target.getAttribute('data-post-id');
        if (!id || seenRef.current.has(id)) return;
        seenRef.current.add(id);
        io.unobserve(en.target);
        setViews((v) => ({ ...v, [id]: (v[id] || 0) + 1 }));
        bumpView('community', id);
      });
    }, { threshold: 0.5 });
    const t = setTimeout(() => {
      document.querySelectorAll('[data-post-id]').forEach((el) => {
        if (!seenRef.current.has(el.getAttribute('data-post-id'))) io.observe(el);
      });
    }, 0);
    return () => { clearTimeout(t); io.disconnect(); };
  }, [rows, cat, stageFilter, sort]);

  // 기여 통계(client_id별): 글 수·답글 수·받은 공감 → 칭호
  const stats = {};
  rows.forEach((r) => {
    const cid = r.client_id;
    if (!cid) return;
    const s = stats[cid] || { posts: 0, replies: 0, likes: 0 };
    if (r.parent_id) s.replies += 1; else s.posts += 1;
    s.likes += Number(r.likes) || 0;
    stats[cid] = s;
  });
  const titleOf = (cid) => titleFromStats(cid && stats[cid]);
  const myTitle = (() => { for (const id of myIds) { const t = titleOf(id); if (t) return t; } return null; })();

  const filtered = rows.filter((r) => !r.parent_id && (cat === 'all' || catOf(r) === cat) && (stageFilter === 'all' || stageOf(r) === Number(stageFilter)));
  const weekAgo = Date.now() - 7 * 86400000;
  const best = filtered.filter((r) => (r.likes || 0) > 0 && new Date(r.created_at).getTime() > weekAgo).sort((a, b) => (b.likes || 0) - (a.likes || 0))[0] || null;
  const posts = filtered.filter((r) => !best || r.id !== best.id).sort((a, b) => (sort === 'hot' ? ((b.likes || 0) - (a.likes || 0)) || (new Date(b.created_at) - new Date(a.created_at)) : (new Date(b.created_at) - new Date(a.created_at))));
  const repliesOf = (id) => rows.filter((r) => r.parent_id === id).sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  const submitPost = async (event) => {
    event.preventDefault();
    const text = post.trim().slice(0, 240);
    if (!loggedIn) { onMove && onMove('account'); return; }
    if (!text || sending) return;
    setSending(true);
    const created = await sendCommunity(text, null, postCat, myStage || null);
    setSending(false);
    if (created) { setRows((r) => [...r, { ...created, parent_id: null, likes: 0, category: postCat, stage: myStage || null }]); remember(created.id); setPost(''); setCat(postCat); setSort('new'); }
  };

  const submitReply = async (parentId) => {
    const text = replyText.trim().slice(0, 240);
    if (!loggedIn) { onMove && onMove('account'); return; }
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

  const PostCard = (p, isBest) => {
    const reps = repliesOf(p.id);
    const open = openId === p.id;
    const ptitle = titleOf(p.client_id);
    return (
      <article className={`fm-card fm-post${isBest ? ' fm-best' : ''}`} key={p.id} data-post-id={p.id}>
        {isBest && <p className="fm-best-tag">🏆 이번 주 베스트</p>}
        {editId === p.id ? <EditBox id={p.id} value={editText} onChange={setEditText} onCancel={cancelEdit} onSave={saveEdit} /> : <p className="fm-post-msg">{p.message}</p>}
        <div className="fm-post-meta">
          <span className="fm-post-author">{(p.likes || 0) >= 3 && <span className="fm-hot-chip">🔥 인기</span>}<span className="fm-cat-badge">{catLabel(catOf(p))}</span>{stageOf(p) && stageMeta(stageOf(p)) && <span className="fm-stage-badge">{stageMeta(stageOf(p)).emoji} {stageOf(p)}단계</span>}{p.nickname || funHandle(p.id)}{ptitle && <span className="fm-title-chip">{ptitle}</span>} · {relativeTime(p.created_at)}</span>
          <div className="fm-post-actions">
            <OwnerControls mine={isMine(p)} row={p} onEdit={startEdit} onDelete={removeRow} />
            <span className="fm-post-views" aria-label="조회수" style={{ display: 'inline-flex', alignItems: 'center', gap: '3px', fontSize: '12px', fontWeight: 800, color: '#9ca3af', padding: '5px 4px', whiteSpace: 'nowrap' }}>👁 {views[p.id] || 0}</span>
            <button type="button" className={`fm-post-like${isLiked(p.id) ? ' on' : ''}`} onClick={() => like(p)} aria-label="공감">♥ {p.likes || 0}</button>
            <button type="button" className="fm-post-reply" onClick={() => { setOpenId(open ? null : p.id); setReplyText(''); }}>💬 {reps.length}</button>
          </div>
        </div>
        {open && (
          <div className="fm-replies">
            {reps.map((r) => {
              const rtitle = titleOf(r.client_id);
              return (
                <div className="fm-reply" key={r.id}>
                  {editId === r.id ? <EditBox id={r.id} value={editText} onChange={setEditText} onCancel={cancelEdit} onSave={saveEdit} /> : <p>{r.message}</p>}
                  <div className="fm-reply-meta">
                    <small>{r.nickname || funHandle(r.id)}{rtitle && <span className="fm-title-chip">{rtitle}</span>} · {relativeTime(r.created_at)}</small>
                    <OwnerControls mine={isMine(r)} row={r} onEdit={startEdit} onDelete={removeRow} />
                  </div>
                </div>
              );
            })}
            {loggedIn ? (
              <div className="fm-reply-input">
                <input maxLength={240} value={replyText} onChange={(e) => setReplyText(e.target.value)} placeholder="답글 달기…" onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); submitReply(p.id); } }} />
                <button type="button" onClick={() => submitReply(p.id)} disabled={!replyText.trim()}>등록</button>
              </div>
            ) : (
              <button type="button" className="fm-reply-login" onClick={() => onMove && onMove('account')}>🔒 로그인하고 답글 달기 →</button>
            )}
          </div>
        )}
      </article>
    );
  };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <style>{STYLE}</style>
      <Header tag="커뮤니티" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">파이어족 라운지</p>
        <h2>다 같이 파이어 이야기</h2>
        <p>관심 가는 카테고리를 골라 글을 쓰고, 답글로 서로 대화해요. 글·답글·공감이 쌓이면 닉네임 옆에 칭호가 붙어요. 내가 쓴 글은 수정·삭제할 수 있어요.</p>
      </section>

      <div className="fm-stage-bar">
        <button type="button" className={stageFilter === 'all' ? 'on' : ''} onClick={() => setStageFilter('all')}>전체 단계</button>
        {myStage && stageMeta(myStage) && (
          <button type="button" className={'fm-stage-mine' + (String(stageFilter) === String(myStage) ? ' on' : '')} onClick={() => setStageFilter(String(myStage))}>⭐ 내 단계 · {stageMeta(myStage).emoji}{stageMeta(myStage).name}</button>
        )}
        {JOURNEY_STAGES.map((st) => (
          <button type="button" key={st.key} className={String(stageFilter) === String(st.n) ? 'on' : ''} onClick={() => setStageFilter(String(st.n))}>{st.emoji} {st.n}.{st.name}</button>
        ))}
      </div>

      {stageFilter !== 'all' && stageMeta(stageFilter) && (
        <p className="fm-stage-desc">{stageMeta(stageFilter).emoji} <b>{stageMeta(stageFilter).n}단계 · {stageMeta(stageFilter).name}</b> — ‘{stageMeta(stageFilter).tag}’ 단계를 지나는 파이어족의 글 모음이에요. 같은 구간에 있는 분들과 이야기 나눠보세요.</p>
      )}

      <div className="fm-cat-bar">
        <button type="button" className={cat === 'all' ? 'on' : ''} onClick={() => setCat('all')}>전체</button>
        {CATEGORIES.map((c) => (
          <button type="button" key={c.key} className={cat === c.key ? 'on' : ''} onClick={() => setCat(c.key)}>{c.emoji} {c.label}</button>
        ))}
      </div>

      <div className="fm-sortbar">
        <button type="button" className={sort === 'new' ? 'on' : ''} onClick={() => setSort('new')}>최신순</button>
        <button type="button" className={sort === 'hot' ? 'on' : ''} onClick={() => setSort('hot')}>인기순</button>
      </div>

      {loggedIn ? (
      <form className="fm-card fm-community-form" onSubmit={submitPost}>
        <label htmlFor="fm-community-input">새 글 쓰기</label>
        <p className="fm-mytitle">내 칭호: {myTitle ? <b>{myTitle}</b> : '아직 없음 (글·답글·공감으로 모아요)'}</p>
        {myStage && stageMeta(myStage) && <p className="fm-mytitle">내 단계: <b>{stageMeta(myStage).emoji} {myStage}단계 · {stageMeta(myStage).name}</b> · 글에 자동으로 표시돼 같은 단계 그룹에 모여요</p>}
        <div className="fm-cat-select">
          <select value={postCat} onChange={(e) => setPostCat(e.target.value)} aria-label="카테고리 선택">
            {CATEGORIES.map((c) => <option key={c.key} value={c.key}>{c.emoji} {c.label}</option>)}
          </select>
        </div>
        <textarea id="fm-community-input" maxLength={240} value={post} onChange={(e) => setPost(e.target.value)} placeholder="예: 생활비를 줄이니 파이어가 5년 당겨졌어요. 다들 어떻게 아끼세요?" />
        <div className="fm-community-form-row">
          <small>{post.length}/240 · {nick ? `${nick} 으로 게시` : '닉네임 자동 생성'}</small>
          <button type="submit" disabled={sending || !post.trim()}>{sending ? '올리는 중' : '글 올리기'}</button>
        </div>
      </form>
      ) : (
        <button type="button" className="fm-community-login" onClick={() => onMove && onMove('account')}>
          🔒 로그인하고 글 남기기
          <span>읽기는 로그인 없이 자유롭게 · 글쓰기는 내 닉네임으로 남겨요</span>
        </button>
      )}

      <section className="fm-community-feed">
        {best && PostCard(best, true)}
        {posts.length === 0 && !best && <p className="fm-community-empty">{(cat === 'all' && stageFilter === 'all') ? '아직 글이 없어요. 첫 글을 남기면 다른 파이어족들이 답글로 응원해줘요 🔥' : '이 그룹의 첫 글을 남겨보세요 🔥'}</p>}
        {posts.map((p) => PostCard(p, false))}
      </section>
    </main>
  );
}
