// 방명록 전체 — 홈 💬(Wall.jsx)에서 넘어오는 전체 글·답글 화면(screens 'wall'). 개편 최종본 §3 방명록.
// 탭 4(전체·인증·질문·자유) · 글마다 카드 · 공감·답글 · 내 글 수정/삭제(RPC) · 글쓰기는 Sheet.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, Tabs, Card, Button, Badge, Sheet, Dialog, Chips, Chip, Skeleton, EmptyState, toast } from '../../ui/index.js';
import { loadCommunityThread, sendCommunity, likeCommunity, editCommunity, deleteCommunity } from '../../utils/firemapFeedbackApi.js';
import { displayNameOf } from '../../firemap-v2/funName.js';
import { JOURNEY_STAGES, journeyStage } from '../../utils/journeyStage.js';
import { identityIds, account } from '../../utils/identity.js';
import '../../ui/screens/wall.css';

const TABS = [
  { key: 'all', label: '전체' },
  { key: 'goal', label: '인증' },
  { key: 'question', label: '질문' },
  { key: 'free', label: '자유' }
];
// 쓰기 분류(저장값) — 옛 글의 'qa'도 질문으로 읽어요.
const WRITE_CATS = [
  { key: 'goal', label: '🔥 인증' },
  { key: 'qa', label: '❓ 질문' },
  { key: 'free', label: '💬 자유' }
];
const tabOf = (row) => {
  const c = row.category || 'free';
  if (c === 'goal') return 'goal';
  if (c === 'qa' || c === 'question') return 'question';
  return 'free';
};
const TAB_LABEL = { goal: '인증', question: '질문', free: '자유' };
// 공식 계정 글 중 방명록 성격(인증·자유·질문·가계부)만 보여요. 뉴스성 글은 소식 화면 담당.
const OFFICIAL_WALL_CATS = new Set(['free', 'goal', 'qa', 'question', 'budget']);

function titleFromStats(s) {
  if (!s) return null;
  if (s.posts >= 5 || s.likes >= 10) return '⭐ 방명록 스타';
  if (s.replies >= 5) return '😇 답글 천사';
  if (s.likes >= 5) return '💖 공감 부자';
  if (s.posts >= 2) return '☕ 단골';
  return null;
}

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
const MAX = 240;

export default function Community({ onBack, onMove, simulation }) {
  const myStage = (() => { try { return journeyStage(simulation || null).stage; } catch { return null; } })();
  const stageMeta = (n) => JOURNEY_STAGES.find((x) => x.n === Number(n)) || null;
  const [rows, setRows] = useState(null);
  const [tab, setTab] = useState('all');
  const [openId, setOpenId] = useState(null);
  const [replyText, setReplyText] = useState('');
  const [mine, setMine] = useState(loadMine());
  const [composer, setComposer] = useState(null); // {mode:'new'|'edit', id?, cat, text}
  const [sending, setSending] = useState(false);
  const [delTarget, setDelTarget] = useState(null);

  useEffect(() => {
    let alive = true;
    loadCommunityThread().then((r) => { if (alive) setRows(Array.isArray(r) ? r : []); }).catch(() => { if (alive) setRows([]); });
    return () => { alive = false; };
  }, []);

  const loggedIn = !!(account() && account().handle);
  const myIds = identityIds();
  const isMine = (row) => mine.includes(row.id) || (!!row.client_id && myIds.includes(row.client_id));
  const remember = (id) => { addMine(id); setMine(loadMine()); };

  const stats = useMemo(() => {
    const s = {};
    (rows || []).forEach((r) => {
      const cid = r.client_id; if (!cid) return;
      const x = s[cid] || { posts: 0, replies: 0, likes: 0 };
      if (r.parent_id) x.replies += 1; else x.posts += 1;
      x.likes += Number(r.likes) || 0;
      s[cid] = x;
    });
    return s;
  }, [rows]);
  const titleOf = (cid) => titleFromStats(cid && stats[cid]);

  const all = rows || [];
  const filtered = all
    .filter((r) => !r.parent_id && (r.client_id !== 'firemap-official' || OFFICIAL_WALL_CATS.has(r.category || 'free')) && (tab === 'all' || tabOf(r) === tab))
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  const weekAgo = Date.now() - 7 * 86400000;
  const best = filtered.filter((r) => (r.likes || 0) > 0 && new Date(r.created_at).getTime() > weekAgo).sort((a, b) => (b.likes || 0) - (a.likes || 0))[0] || null;
  const repliesOf = (id) => all.filter((r) => r.parent_id === id).sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  const needLogin = () => { toast('로그인하면 내 이름으로 남길 수 있어요'); onMove && onMove('account'); };
  const openNew = () => { if (!loggedIn) { needLogin(); return; } setComposer({ mode: 'new', cat: tab === 'question' ? 'qa' : (tab === 'goal' ? 'goal' : 'free'), text: '' }); };
  const openEdit = (row) => setComposer({ mode: 'edit', id: row.id, cat: row.category || 'free', text: row.message || '', isReply: !!row.parent_id });
  const closeComposer = () => setComposer(null);

  const submitComposer = async () => {
    if (!composer || sending) return;
    const text = composer.text.trim().slice(0, MAX);
    if (!text) return;
    setSending(true);
    if (composer.mode === 'new') {
      const created = await sendCommunity(text, null, composer.cat, myStage || null);
      setSending(false);
      if (!created) { toast.bad('올리지 못했어요 · 잠시 뒤 다시 해보세요'); return; }
      setRows((r) => [...(r || []), { ...created, parent_id: null, likes: 0, category: composer.cat, stage: myStage || null }]);
      remember(created.id);
      setTab(tabOf({ category: composer.cat }));
      toast.good('방명록에 남겼어요');
    } else {
      const ok = await editCommunity(composer.id, text);
      setSending(false);
      if (!ok) { toast.bad('고치지 못했어요 · 내 글만 고칠 수 있어요'); return; }
      setRows((r) => (r || []).map((x) => (x.id === composer.id ? { ...x, message: text } : x)));
      toast.good('고쳤어요');
    }
    closeComposer();
  };

  const submitReply = async (parentId) => {
    const text = replyText.trim().slice(0, MAX);
    if (!loggedIn) { needLogin(); return; }
    if (!text || sending) return;
    setSending(true);
    const created = await sendCommunity(text, parentId);
    setSending(false);
    if (!created) { toast.bad('답글을 올리지 못했어요'); return; }
    setRows((r) => [...(r || []), { ...created, parent_id: parentId, likes: 0 }]);
    remember(created.id);
    setReplyText('');
  };

  const like = async (row) => {
    if (isLiked(row.id)) { toast('이미 공감했어요'); return; }
    const ok = await likeCommunity(row.id, row.likes || 0);
    if (!ok) return;
    try { localStorage.setItem(likedKey(row.id), '1'); } catch { /* ignore */ }
    setRows((r) => (r || []).map((x) => (x.id === row.id ? { ...x, likes: (x.likes || 0) + 1 } : x)));
  };

  const confirmDelete = async () => {
    const row = delTarget; if (!row) return;
    const ok = await deleteCommunity(row.id);
    setDelTarget(null);
    if (!ok) { toast.bad('지우지 못했어요 · 내 글만 지울 수 있어요'); return; }
    setRows((r) => (r || []).filter((x) => x.id !== row.id && x.parent_id !== row.id));
    if (openId === row.id) setOpenId(null);
    toast('지웠어요');
  };

  const Author = ({ row, size }) => {
    const t = titleOf(row.client_id);
    const st = row.stage != null ? stageMeta(row.stage) : null;
    return (
      <span className={`sc-wall-author${size === 'sm' ? ' sc-wall-author--sm' : ''}`}>
        <b>{displayNameOf(row)}</b>
        {isMine(row) && <Badge tone="accent">나</Badge>}
        {st && <Badge tone="neutral">{st.emoji} {row.stage}단계</Badge>}
        {t && <Badge tone="neutral">{t}</Badge>}
        <span className="sc-wall-time">{relativeTime(row.created_at)}</span>
      </span>
    );
  };

  const PostCard = (p, isBest) => {
    const reps = repliesOf(p.id);
    const open = openId === p.id;
    const liked = isLiked(p.id);
    const mineRow = isMine(p);
    return (
      <Card key={p.id} variant={isBest ? 'hero' : 'base'} className="sc-wall-post">
        <div className="sc-wall-post__head">
          <span className="sc-wall-post__tags">
            {isBest && <Badge tone="accent">🏆 이번 주 베스트</Badge>}
            <Badge tone="neutral">{TAB_LABEL[tabOf(p)]}</Badge>
            {(p.likes || 0) >= 3 && <Badge tone="warn">인기</Badge>}
          </span>
        </div>
        <p className="sc-wall-msg">{p.message}</p>
        <Author row={p} />
        <div className="sc-wall-actions">
          <Button variant={liked ? 'tint' : 'secondary'} size="sm" onClick={() => like(p)} aria-pressed={liked} aria-label="공감">♥ <span className="num">{p.likes || 0}</span></Button>
          <Button variant={open ? 'tint' : 'secondary'} size="sm" onClick={() => { setOpenId(open ? null : p.id); setReplyText(''); }} aria-expanded={open}>💬 <span className="num">{reps.length}</span></Button>
          {mineRow && <span className="sc-wall-own"><Button variant="ghost" size="sm" onClick={() => openEdit(p)}>수정</Button><Button variant="ghost" size="sm" className="sc-wall-del" onClick={() => setDelTarget(p)}>삭제</Button></span>}
        </div>
        {open && (
          <div className="sc-wall-replies">
            {reps.length === 0 && <p className="ds-caption sc-wall-replies__empty">아직 답글이 없어요 · 첫 답글을 남겨보세요</p>}
            {reps.map((r) => (
              <div className="sc-wall-reply" key={r.id}>
                <p className="sc-wall-reply__msg">{r.message}</p>
                <div className="sc-wall-reply__foot">
                  <Author row={r} size="sm" />
                  {isMine(r) && <span className="sc-wall-own"><Button variant="ghost" size="sm" onClick={() => openEdit(r)}>수정</Button><Button variant="ghost" size="sm" className="sc-wall-del" onClick={() => setDelTarget(r)}>삭제</Button></span>}
                </div>
              </div>
            ))}
            {loggedIn ? (
              <div className="sc-wall-reply-input">
                <input className="ds-input" maxLength={MAX} value={replyText} onChange={(e) => setReplyText(e.target.value)} placeholder="답글 남기기" aria-label="답글 입력" onKeyDown={(e) => { if (e.key === 'Enter' && !e.nativeEvent.isComposing) { e.preventDefault(); submitReply(p.id); } }} />
                <Button variant="primary" size="md" onClick={() => submitReply(p.id)} disabled={!replyText.trim()} loading={sending}>등록</Button>
              </div>
            ) : (
              <Button variant="secondary" size="sm" full onClick={needLogin}>🔒 로그인하고 답글 남기기</Button>
            )}
          </div>
        )}
      </Card>
    );
  };

  const posts = filtered.filter((r) => !best || r.id !== best.id);
  const [shown, setShown] = useState(15);
  const emptyText = tab === 'goal' ? '아직 인증이 없어요 · 내 결과로 첫 인증을 남겨보세요' : tab === 'question' ? '아직 질문이 없어요 · 궁금한 걸 남겨보세요' : '아직 조용해요 · 첫 한마디를 남겨보세요';

  return (
    <main className="fm-screen fm-scroll ds-screen-gap">
      <TopBar title="방명록" onBack={onBack} />
      <Tabs items={TABS} value={tab} onChange={(k) => { setTab(k); setOpenId(null); }} label="방명록 분류" />
      <p className="ds-caption sc-wall-cap">파이어족끼리 한마디 · 욕설·비방·개인정보는 지워질 수 있어요</p>

      <div className="ds-bottomcta sc-wall-cta">
        <Button variant="tint" size="md" onClick={() => onMove && onMove('result')}>🪪 인증 카드 만들기</Button>
        <Button variant="primary" size="md" onClick={openNew}>한마디 남기기</Button>
      </div>

      {rows === null && <Card><Skeleton lines={3} /></Card>}
      {rows !== null && !best && posts.length === 0 && <EmptyState icon="💬" title={emptyText.split(' · ')[0]} desc={emptyText.split(' · ')[1]} action={{ label: tab === 'goal' ? '인증 카드 만들기' : '한마디 남기기', onClick: tab === 'goal' ? () => onMove && onMove('result') : openNew }} />}
      {best && PostCard(best, true)}
      {posts.slice(0, shown).map((p) => PostCard(p, false))}
      {posts.length > shown && <Button variant="secondary" size="md" full onClick={() => setShown((n) => n + 15)}>더 보기 · {posts.length - shown}개</Button>}

      <Sheet open={!!composer} title={composer && composer.mode === 'edit' ? '내 글 고치기' : '한마디 남기기'} onClose={closeComposer}>
        {composer && composer.mode === 'new' && (
          <Chips className="sc-wall-composer__cats">
            {WRITE_CATS.map((c) => <Chip key={c.key} on={composer.cat === c.key} onClick={() => setComposer((s) => ({ ...s, cat: c.key }))}>{c.label}</Chip>)}
          </Chips>
        )}
        <textarea
          className="ds-textarea ds-mt-3"
          maxLength={MAX}
          autoFocus
          value={composer ? composer.text : ''}
          onChange={(e) => setComposer((s) => (s ? { ...s, text: e.target.value } : s))}
          placeholder={composer && composer.cat === 'goal' ? '예: 56세 파이어 인증해요. 생활비를 줄이니 5년 당겨졌어요' : '예: 다들 생활비 어떻게 아끼세요?'}
          aria-label="글 내용"
        />
        <p className="ds-caption sc-wall-composer__count"><span className="num">{composer ? composer.text.length : 0}</span>/{MAX}{composer && composer.mode === 'new' && myStage && stageMeta(myStage) ? ` · ${stageMeta(myStage).emoji} ${myStage}단계 표시로 올라가요` : ''}</p>
        <div className="ds-bottomcta">
          <Button variant="secondary" size="md" onClick={closeComposer}>취소</Button>
          <Button variant="primary" size="md" onClick={submitComposer} disabled={!composer || !composer.text.trim()} loading={sending}>{composer && composer.mode === 'edit' ? '저장' : '올리기'}</Button>
        </div>
      </Sheet>

      <Dialog
        open={!!delTarget}
        title="이 글을 지울까요?"
        desc={delTarget && !delTarget.parent_id ? '답글도 같이 지워져요 · 되돌릴 수 없어요' : '되돌릴 수 없어요'}
        primary={{ label: '지우기', variant: 'danger', onClick: confirmDelete }}
        secondary={{ label: '취소' }}
        onClose={() => setDelTarget(null)}
      />
    </main>
  );
}
