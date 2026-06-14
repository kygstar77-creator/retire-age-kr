import { useEffect, useState } from 'react';
import { fetchCommunityPeek } from '../../utils/firemapFeedbackApi.js';
import { funHandle } from '../../firemap-v2/funName.js';

const SEED_PROMPTS = [
  '파이어하면 제일 하고 싶은 거 하나만 적어주세요',
  '한 달 생활비, 다들 얼마로 잡으세요?',
  '파이어 준비하면서 제일 어려운 점은?',
  '지금 제일 후회되는 소비 하나?'
];

export default function CommunityPeek({ onMove }) {
  const [posts, setPosts] = useState(null);
  useEffect(() => {
    let alive = true;
    fetchCommunityPeek(3).then((r) => { if (alive) setPosts(r || []); }).catch(() => { if (alive) setPosts([]); });
    return () => { alive = false; };
  }, []);

  const hasPosts = posts && posts.length > 0;
  const seed = SEED_PROMPTS[new Date().getDate() % SEED_PROMPTS.length];

  return (
    <section className="fm-card fm-lounge">
      <p className="fm-kicker">파이어족 라운지</p>
      <h2 className="fm-section-title">다른 사람들은 어떻게 준비할까?</h2>
      {posts === null && <p className="fm-lounge-loading">불러오는 중…</p>}
      {posts !== null && hasPosts && (
        <ul className="fm-lounge-list">
          {posts.map((p) => (
            <li key={p.id} className="fm-lounge-item">
              <span className="fm-lounge-nick">{p.nickname || funHandle(p.id)}</span>
              <span className="fm-lounge-msg">{p.message}</span>
            </li>
          ))}
        </ul>
      )}
      {posts !== null && !hasPosts && (
        <p className="fm-lounge-empty">아직 조용해요 🤫 첫 한마디를 남겨보세요<br /><b>“{seed}”</b></p>
      )}
      <button type="button" className="fm-lounge-cta" onClick={() => onMove('community')}>
        {hasPosts ? '나도 한마디 남기기  →' : '첫 글 남기러 가기  →'}
      </button>
    </section>
  );
}
