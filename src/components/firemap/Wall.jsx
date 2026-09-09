import { useEffect, useRef, useState } from 'react';
import { loadWall, sendCommunity } from '../../utils/firemapFeedbackApi.js';
import { fetchLivePresence } from '../../utils/live.js';
import { identityIds } from '../../utils/identity.js';
import { funHandle } from '../../firemap-v2/funName.js';
import { track } from '../../firemap-v2/dailyData.js';

// 방명록 — 홈 전용 플로팅 💬 버튼 → 실시간 한마디 패널(스꾸 방명록 패턴 이식).
// 열려 있는 동안만 주기 폴링으로 새 글을 맨 위에 붙이고, 읽던 스크롤 위치는 유지한다.
// 공식 글(firemap-official)은 여기 안 나옴 — '소식·뉴스' 탭 담당. 전체 글·답글은 #community.
const POLL_MS = 10000;
const PRESENCE_MS = 30000;
const PAGE = 50;
const EMOJI = ['🔥', '🌱', '🐿️', '🦊', '🦦', '🐧', '🐢', '🦉', '🐹', '🐼', '🍀', '⭐', '🌙', '🍑', '🥕', '🧭', '🎯', '💰', '🏝️', '🚀'];

function hashOf(s) { let h = 0; const t = String(s || ''); for (let i = 0; i < t.length; i += 1) h = (h * 31 + t.charCodeAt(i)) >>> 0; return h; }
const avatarOf = (row) => EMOJI[hashOf(row.client_id || row.id) % EMOJI.length];
const nameOf = (row) => row.nickname || funHandle(row.client_id || row.id);
function timeAgo(iso) {
  const d = new Date(iso); const diff = (Date.now() - d.getTime()) / 1000;
  if (diff < 60) return '방금';
  if (diff < 3600) return `${Math.floor(diff / 60)}분 전`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`;
  if (diff < 2592000) return `${Math.floor(diff / 86400)}일 전`;
  return `${d.getMonth() + 1}월 ${d.getDate()}일`;
}

export default function Wall({ visible }) {
  const [open, setOpen] = useState(false);
  const [rows, setRows] = useState(null);      // 최신이 맨 위(desc)
  const [online, setOnline] = useState(0);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const listRef = useRef(null);
  const rowsRef = useRef([]);
  const mine = new Set(identityIds());

  // 이미 있는 글은 제외하고 새 글만 맨 위에. 맨 위를 보고 있을 때만 새 글로 올리고, 아니면 읽던 위치 유지.
  const mergeFresh = (incoming) => {
    const have = new Set(rowsRef.current.map((r) => String(r.id)));
    const fresh = (incoming || []).filter((r) => !have.has(String(r.id)));
    if (!fresh.length) return;
    const el = listRef.current;
    const atTop = !el || el.scrollTop < 40;
    const prevH = el ? el.scrollHeight : 0; const prevTop = el ? el.scrollTop : 0;
    fresh.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    const next = [...fresh, ...rowsRef.current];
    rowsRef.current = next;
    setRows(next);
    requestAnimationFrame(() => { const l = listRef.current; if (!l) return; l.scrollTop = atTop ? 0 : prevTop + (l.scrollHeight - prevH); });
  };
  const pollOnce = () => { loadWall(30).then(mergeFresh).catch(() => {}); };
  const loadFirst = () => { loadWall(PAGE).then((r) => { rowsRef.current = r || []; setRows(r || []); }).catch(() => { rowsRef.current = []; setRows([]); }); };
  const refreshOnline = () => { fetchLivePresence().then((p) => { if (p) setOnline(p.online || 0); }); };

  useEffect(() => {
    if (!open) return undefined;
    if (rows === null) loadFirst(); else pollOnce();   // 열 때 최신도 즉시 반영
    refreshOnline();
    track('wall_open');
    const iv = setInterval(() => { if (!document.hidden) pollOnce(); }, POLL_MS);
    const pv = setInterval(() => { if (!document.hidden) refreshOnline(); }, PRESENCE_MS);
    const onKey = (e) => { if (e.key === 'Escape') setOpen(false); };
    window.addEventListener('keydown', onKey);
    return () => { clearInterval(iv); clearInterval(pv); window.removeEventListener('keydown', onKey); };
  }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  // 홈을 벗어나면 열린 패널 자동 닫기(버튼 없이 열린 채 방치 방지)
  useEffect(() => { if (!visible && open) setOpen(false); }, [visible, open]);

  const submit = async (e) => {
    if (e) e.preventDefault();
    const clean = text.trim().slice(0, 240);
    if (!clean || sending) return;
    setSending(true); setError('');
    try {
      const created = await sendCommunity(clean, null, 'free');
      if (created) { setText(''); mergeFresh([created]); track('wall_post'); }
      else setError('전송에 실패했어요. 잠시 후 다시 시도해주세요.');
    } catch { setError('전송에 실패했어요. 잠시 후 다시 시도해주세요.'); }
    finally { setSending(false); }
  };
  const onKeyDown = (e) => { if (e.key === 'Enter' && !e.nativeEvent.isComposing && e.keyCode !== 229) { e.preventDefault(); submit(); } };

  if (!visible) return null;
  return (
    <>
      <button type="button" className={`fm-wall-fab${open ? ' is-open' : ''}`} aria-label={open ? '방명록 닫기' : '방명록'} aria-expanded={open} onClick={() => setOpen((o) => !o)}>{open ? '✕' : '💬'}</button>
      {open && (
        <section className="fm-wall" role="dialog" aria-label="방명록">
          <header className="fm-wall-head">
            <div>
              <h3>💬 방명록</h3>
              <p>파이어족끼리 자유롭게 한마디 🍀<br />욕설·비방·개인정보는 삭제될 수 있어요.</p>
            </div>
            <span className="fm-wall-live" aria-live="polite"><i aria-hidden="true" />{online > 0 ? `${online}명 접속 중` : '접속 확인 중'}</span>
          </header>
          <div className="fm-wall-list" ref={listRef}>
            {rows === null && <p className="fm-wall-empty">불러오는 중…</p>}
            {rows !== null && rows.length === 0 && <p className="fm-wall-empty">아직 조용해요 🤫<br />첫 한마디를 남겨보세요</p>}
            {rows !== null && rows.map((r) => {
              const isMine = r.client_id && mine.has(r.client_id);
              return (
                <article key={r.id} className={`fm-wall-item${isMine ? ' mine' : ''}`}>
                  <span className="fm-wall-ava" aria-hidden="true">{avatarOf(r)}</span>
                  <div>
                    <b>{nameOf(r)}</b><small>{isMine ? '나 · ' : ''}{timeAgo(r.created_at)}</small>
                    <p>{r.message}</p>
                  </div>
                </article>
              );
            })}
          </div>
          {error && <p className="fm-wall-error">{error}</p>}
          <form className="fm-wall-input" onSubmit={submit}>
            <input value={text} maxLength={240} placeholder="한마디 남기기" autoComplete="off" aria-label="한마디 입력" onChange={(e) => setText(e.target.value)} onKeyDown={onKeyDown} />
            <button type="submit" disabled={sending || !text.trim()}>{sending ? '올리는 중' : '등록'}</button>
          </form>
        </section>
      )}
    </>
  );
}
