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

export default function CafePoster({ onBack }) {
  const [canPost, setCanPost] = useState(false);
  const [hasNaver, setHasNaver] = useState(false);
  const [busyId, setBusyId] = useState(null);
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
    const r = await postToCafe({ subject: p.title, content: p.body });
    setBusyId(null);
    if (r.ok) {
      const next = { ...done, [p.id]: new Date().toISOString().slice(0, 10) };
      setDone(next); writeDone(next);
      track('cafe_post_ops', { id: p.id });
      toast.good('카페에 올렸어요');
      if (r.url) { try { window.open(r.url, '_blank', 'noopener'); } catch { /* ignore */ } }
      return;
    }
    console.error('cafe post failed:', r.reason);
    track('cafe_post_fail', { reason: String(r.reason || '').slice(0, 300), id: p.id });
    if (r.reason === 'login') {
      try { sessionStorage.removeItem('fm_naver_token'); } catch { /* ignore */ }
      await login();
      return;
    }
    toast.bad('못 올렸어요 · 잠시 뒤 다시');
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
        </Card>
      ))}
    </main>
  );
}
