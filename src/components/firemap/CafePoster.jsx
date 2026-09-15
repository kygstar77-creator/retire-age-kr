// 카페에 올리기(#ops) — 운영자 전용. 준비된 글을 한 편씩 눌러서 카페에 올린다.
// 메뉴에 없고 사이트맵에도 없다. 주소 뒤에 ?ops=1 을 한 번 붙여 들어오면 그 기기에서만 열린다.
// 저절로 올라가는 글은 없다. 누른 사람 본인 계정으로 올라가고(봇 계정 없음), 올린 글은 기기에 기억해 중복 게시를 막는다.
import { useEffect, useState } from 'react';
import { TopBar, Card, SectionHead, Button, Notice, toast } from '../../ui/index.js';
import { CAFE_POSTS } from '../../firemap-v2/cafePosts.js';
import { cafePostEnabled, naverLoginStart, naverToken, postToCafe } from '../../utils/naverAuth.js';
import { track } from '../../firemap-v2/dailyData.js';

const DONE_KEY = 'fm_cafe_posted';
const readDone = () => { try { return JSON.parse(localStorage.getItem(DONE_KEY) || '{}'); } catch { return {}; } };
const writeDone = (v) => { try { localStorage.setItem(DONE_KEY, JSON.stringify(v)); } catch { /* ignore */ } };


// 네이버 카페 API는 첨부 그림을 전부 글 맨 앞에 붙인다(공식 문서에 위치 지정 방법이 없고,
// content에 <img>를 박으면 403 code 999로 막힌다 — 두 조합 다 실측). 그래서 본문 중간에
// 넣으려면 올린 뒤 카페 편집기에서 사람이 끌어 옮겨야 한다. 어디로 옮길지는 여기서 알려준다.
function placementGuide(p) {
  if (!p || !Array.isArray(p.images) || !p.images.length) return [];
  const paras = String(p.body || '').split(String.fromCharCode(10, 10));
  const out = [];
  paras.forEach((para, i) => {
    const m = para.trim().match(/^\[\[img(\d+)\]\]$/);
    if (!m) return;
    const n = Number(m[1]);
    const next = (paras[i + 1] || '').trim().slice(0, 24);
    if (p.images[n - 1]) out.push({ n, file: p.images[n - 1].split('/').pop(), next });
  });
  return out;
}

export default function CafePoster({ onBack }) {
  const [canPost, setCanPost] = useState(false);
  const [hasNaver, setHasNaver] = useState(false);
  const [busyId, setBusyId] = useState(null);
  const [lastError, setLastError] = useState('');
  const [done, setDone] = useState(readDone);

  useEffect(() => {
    let alive = true;
    setHasNaver(!!naverToken());
    cafePostEnabled().then((v) => { if (alive) setCanPost(v); });
    return () => { alive = false; };
  }, []);

  const login = async () => {
    const started = await naverLoginStart('#ops');
    if (!started) toast.bad('네이버 로그인을 아직 쓸 수 없어요');
  };

  const post = async (p) => {
    if (!naverToken()) { await login(); return; }
    setBusyId(p.id);
    // 대표 이미지: 우리 서버가 그리는 카드(/og?mode=post). 검색 결과에 썸네일이 붙는다.
    const img = p.card ? (() => { const u = new URL('/og', window.location.origin); u.searchParams.set('mode', 'post'); u.searchParams.set('t', p.card.t); p.card.l.forEach((v, i) => u.searchParams.set(`l${i + 1}`, v)); return u.toString(); })() : null;
    // 글에 딸린 그림(public/cafe/...)이 있으면 그걸 붙인다. 숫자 카드는 그림이 없는 글에만.
    const pics = Array.isArray(p.images) && p.images.length
      ? p.images.map((rel) => new URL(rel, window.location.origin).toString())
      : null;
    const r = await postToCafe({ subject: p.title, content: p.body, imageUrl: pics ? null : img, imageUrls: pics });
    setBusyId(null);
    if (r.ok) {
      const next = { ...done, [p.id]: new Date().toISOString().slice(0, 10) };
      setDone(next); writeDone(next);
      track('cafe_post_ops', { id: p.id, via: String(r.via || '') });
      try { sessionStorage.removeItem('fm_naver_retried'); } catch { /* ignore */ }
      setLastError('');
      toast.good(r.via && r.via !== 'inline+all' ? `올렸어요 · ${r.via}로 통과` : '카페에 올렸어요');
      if (r.url) { try { window.open(r.url, '_blank', 'noopener'); } catch { /* ignore */ } }
      return;
    }
    console.error('cafe post failed:', r.reason);
    track('cafe_post_fail', { reason: String(r.reason || '').slice(0, 60), detail: String(r.detail || '').slice(0, 240), id: p.id });
    if (r.reason === 'login') {
      // 로그인을 새로 해도 또 막히면 토큰 문제가 아니다. 두 번째부터는 다시 보내지 않고 그대로 알려준다.
      const again = sessionStorage.getItem('fm_naver_retried') === '1';
      try { sessionStorage.removeItem('fm_naver_token'); } catch { /* ignore */ }
      if (again) { toast.bad('네이버가 글쓰기를 막고 있어요 · 토큰 문제는 아니에요'); return; }
      try { sessionStorage.setItem('fm_naver_retried', '1'); } catch { /* ignore */ }
      await login();
      return;
    }
    try { sessionStorage.removeItem('fm_naver_retried'); } catch { /* ignore */ }
    // 네이버는 사유를 code 999로만 줄 때가 많다. 그래도 화면에 그대로 띄워야 뭘 고칠지 안다.
    setLastError(`${r.reason || '알 수 없음'}${r.detail ? ` · ${r.detail}` : ''}`);
    toast.bad('못 올렸어요 · 아래 사유 확인');
  };

  return (
    <main className="fm-screen fm-scroll ds-screen-gap">
      <TopBar title="카페에 올리기" onBack={onBack} />

      {!canPost && <Notice tone="warn" title="네이버 로그인이 아직 꺼져 있어요" desc="Cloudflare 환경변수를 넣고 다시 배포하면 켜져요" />}
      {canPost && !hasNaver && (
        <Card>
          <SectionHead size="sm" kicker="한 번만" title="네이버 로그인" />
          <Button variant="primary" size="lg" full onClick={login}>네이버 로그인</Button>
        </Card>
      )}

      {lastError && (
        <Notice tone="warn" title="네이버가 돌려보낸 말" desc={lastError} />
      )}

      {CAFE_POSTS.map((p) => (
        <Card key={p.id}>
          <SectionHead size="sm" kicker={done[p.id] ? `올림 · ${done[p.id]}` : p.source} title={p.title} />
          <p className="ds-p sc-ops-body">{p.body}</p>
          <Button
            variant={done[p.id] ? 'secondary' : 'primary'}
            size="md"
            full
            loading={busyId === p.id}
            onClick={() => post(p)}
          >
            {done[p.id] ? '한 번 더 올리기' : '카페에 올리기'}
          </Button>
          {placementGuide(p).length > 0 && (
            <ul className="ds-list sc-ops-guide">
              {placementGuide(p).map((g) => (
                <li key={g.n} className="ds-caption">
                  {g.n}번 {g.file} → {g.next ? `${g.next}… 문단 앞` : '글 끝'}
                </li>
              ))}
            </ul>
          )}
        </Card>
      ))}
    </main>
  );
}
