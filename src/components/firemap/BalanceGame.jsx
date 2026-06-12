import { useEffect, useState } from 'react';
import { votePoll, fetchPollResults } from '../../utils/firemapScoresApi.js';
import { BASE_URL } from '../../firemap-v2/data.js';

const GAMES = [
  { key: 'bg_money_vs_quit', a: '10억 받고 80세까지 일하기', b: '지금 당장 퇴사하기' },
  { key: 'bg_lean_vs_fat', a: '적게 쓰고 40대에 퇴사', b: '많이 벌고 60대에 퇴사' },
  { key: 'bg_now_vs_later', a: '월 200으로 지금 자유', b: '월 500으로 10년 뒤 자유' },
  { key: 'bg_city_vs_country', a: '도시에서 바쁘게 파이어', b: '시골·해외서 느긋하게' },
  { key: 'bg_solo_vs_together', a: '혼자 빨리 파이어', b: '같이 천천히 파이어' },
  { key: 'bg_save_vs_earn', a: '아끼는 게 체질', b: '버는 게 체질' },
  { key: 'bg_stock_vs_estate', a: '주식으로 파이어', b: '부동산으로 파이어' }
];
const readMine = (k) => { try { return localStorage.getItem('fm_bg_' + k) || ''; } catch { return ''; } };

export default function BalanceGame() {
  const [idx, setIdx] = useState(0);
  const g = GAMES[idx];
  const [res, setRes] = useState(null);
  const [mine, setMine] = useState(() => readMine(GAMES[0].key));

  const load = async (key) => setRes(await fetchPollResults(key, ['a', 'b']));
  useEffect(() => { setMine(readMine(g.key)); setRes(null); load(g.key); /* eslint-disable-next-line */ }, [idx]);

  const vote = async (c) => {
    setMine(c);
    try { localStorage.setItem('fm_bg_' + g.key, c); } catch { /* ignore */ }
    await votePoll(g.key, c);
    await load(g.key);
  };
  const total = res ? res.total : 0;
  const pctOf = (c) => (total > 0 && res ? Math.round(((res.counts[c] || 0) / total) * 100) : 0);
  const reveal = !!mine;
  const next = () => setIdx((idx + 1) % GAMES.length);

  const share = async () => {
    const myText = mine === 'a' ? g.a : g.b;
    const pct = pctOf(mine);
    const text = `밸런스 게임 🔥 "${g.a}" vs "${g.b}"\n나는 「${myText}」! 파이어족 ${pct}%가 같은 선택. 너라면?`;
    if (navigator.share) {
      try { await navigator.share({ title: '파이어맵 — 밸런스 게임', text, url: BASE_URL }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(`${text} ${BASE_URL}`); window.alert('공유 문구를 복사했어요!'); } catch { /* ignore */ }
  };

  return (
    <section className="fm-card fm-bg">
      <div className="fm-bg-head">
        <h2 className="fm-section-title">밸런스 게임 🔥</h2>
        <button type="button" className="fm-bg-next" onClick={next}>다른 질문 ›</button>
      </div>
      <p className="fm-section-sub">둘 중 하나만! 탭하면 사람들의 선택이 보여요 · 익명</p>
      <div className="fm-bg-opts">
        {['a', 'b'].map((c) => {
          const label = c === 'a' ? g.a : g.b;
          const voted = mine === c;
          return (
            <button key={c} type="button" className={`fm-bg-opt${voted ? ' voted' : ''}`} onClick={() => vote(c)}>
              <span className="fm-bg-fill" style={{ height: reveal ? `${pctOf(c)}%` : '0%' }} />
              <span className="fm-bg-label">{label}</span>
              {reveal && <span className="fm-bg-pct">{pctOf(c)}%</span>}
              {voted && <span className="fm-bg-mine">내 선택</span>}
            </button>
          );
        })}
        <span className="fm-bg-vs">VS</span>
      </div>
      {reveal && total > 0 && <p className="fm-poll-total">{total.toLocaleString()}명 참여</p>}
      {reveal && <button type="button" className="fm-poll-share" onClick={share}>내 선택 공유하기</button>}
    </section>
  );
}
