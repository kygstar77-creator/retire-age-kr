import { useEffect, useState } from 'react';
import { votePoll, fetchPollResults } from '../../utils/firemapScoresApi.js';
import { BASE_URL } from '../../firemap-v2/data.js';

const GAMES = [
  { key: 'bg_money_vs_quit', q: '당신의 선택은?', a: '10억 받고\n80세까지 일', b: '0원이어도\n지금 퇴사' },
  { key: 'bg_lean_vs_fat', q: '어떤 파이어?', a: '적게 쓰고\n빨리 은퇴', b: '많이 벌고\n늦게 은퇴' },
  { key: 'bg_now_vs_later', q: '돈 vs 시간', a: '월 200\n지금 자유', b: '월 500\n10년 뒤 자유' },
  { key: 'bg_city_vs_country', q: '어디서 살래?', a: '도시에서\n바쁘게', b: '시골·해외서\n느긋하게' },
  { key: 'bg_solo_vs_together', q: '누구랑?', a: '혼자\n빨리 파이어', b: '같이\n천천히 파이어' },
  { key: 'bg_save_vs_earn', q: '내 체질은?', a: '아끼는 게\n체질', b: '버는 게\n체질' },
  { key: 'bg_stock_vs_estate', q: '뭐로 모을래?', a: '주식으로\n파이어', b: '부동산으로\n파이어' }
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
        <h2 className="fm-section-title">밸런스 게임 🔥 · {g.q}</h2>
        <button type="button" className="fm-bg-next" onClick={next}>다른 질문 ›</button>
      </div>
      <p className="fm-section-sub">당신이라면? 탭하면 사람들의 선택이 보여요 · 익명</p>
      <div className="fm-bg-opts">
        {['a', 'b'].map((c) => {
          const label = c === 'a' ? g.a : g.b;
          const voted = mine === c;
          return (
            <button key={c} type="button" className={`fm-bg-opt${voted ? ' voted' : ''}`} onClick={() => vote(c)}>
              <span className="fm-bg-fill" style={{ height: reveal ? `${pctOf(c)}%` : '0%' }} />
              <span className="fm-bg-label">{label.split('\n').map((ln, k) => <span key={k} className="fm-bg-line">{ln}</span>)}</span>
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
