import { useEffect, useState } from 'react';
import { votePoll, fetchPollResults } from '../../utils/firemapScoresApi.js';

const POLL = {
  key: 'fire_type_2026',
  q: '당신의 파이어 유형은?',
  choices: ['린 파이어', '팻 파이어', '코스트 파이어', '바리스타 파이어']
};
const readMine = () => { try { return localStorage.getItem('fm_poll_' + POLL.key) || ''; } catch { return ''; } };

export default function Poll() {
  const [res, setRes] = useState(null);
  const [mine, setMine] = useState(readMine);
  const load = async () => setRes(await fetchPollResults(POLL.key, POLL.choices));
  useEffect(() => { load(); }, []);
  const vote = async (c) => {
    setMine(c);
    try { localStorage.setItem('fm_poll_' + POLL.key, c); } catch { /* ignore */ }
    await votePoll(POLL.key, c);
    await load();
  };
  const total = res ? res.total : 0;
  const reveal = !!mine;
  return (
    <section className="fm-card fm-poll">
      <h2 className="fm-section-title">{POLL.q}</h2>
      <p className="fm-section-sub">한 번 탭하면 실시간 결과가 보여요 · 익명</p>
      <div className="fm-poll-list">
        {POLL.choices.map((c) => {
          const n = res ? (res.counts[c] || 0) : 0;
          const pct = total > 0 ? Math.round((n / total) * 100) : 0;
          const voted = mine === c;
          return (
            <button key={c} type="button" className={`fm-poll-opt${voted ? ' voted' : ''}`} onClick={() => vote(c)}>
              <span className="fm-poll-bar" style={{ width: reveal ? `${pct}%` : '0%' }} />
              <span className="fm-poll-label">{c}{voted ? ' ✓' : ''}</span>
              {reveal && <span className="fm-poll-pct">{pct}%</span>}
            </button>
          );
        })}
      </div>
      {reveal && total > 0 && <p className="fm-poll-total">{total.toLocaleString()}명 참여 중</p>}
    </section>
  );
}
