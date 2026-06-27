import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { loadOfficialNews } from '../../utils/firemapFeedbackApi.js';
import FireClockPush from './FireClockPush.jsx';

// 공식 경제뉴스(파이어맵 공식 글)만 모아 보는 '소식·뉴스' 화면. 커뮤니티(유저 글)와 분리.
const CATS = [
  { key: 'news', label: '경제', emoji: '📈' },
  { key: 'realestate', label: '부동산', emoji: '🏠' },
  { key: 'invest', label: '투자', emoji: '🌎' },
  { key: 'sidejob', label: '부업', emoji: '💼' },
  { key: 'pension', label: '연금·세금', emoji: '🏦' },
  { key: 'life', label: '파이어 후', emoji: '🏝️' },
  { key: 'save', label: '저축', emoji: '💰' }
];
const catMeta = (k) => CATS.find((c) => c.key === k) || { label: '소식', emoji: '📰' };

function relativeTime(value) {
  const diff = Math.max(1, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (diff < 60) return `${diff}분 전`;
  const h = Math.round(diff / 60);
  if (h < 24) return `${h}시간 전`;
  return `${Math.round(h / 24)}일 전`;
}

const STYLE = `
.fm-news-cats{display:flex;gap:8px;overflow-x:auto;padding:4px 0 12px;-webkit-overflow-scrolling:touch}
.fm-news-cats button{flex:0 0 auto;border:1px solid #e5e7eb;background:#fff;border-radius:99px;padding:7px 12px;font-size:13px;font-weight:700;color:#4b5563;cursor:pointer;white-space:nowrap}
.fm-news-cats button.on{background:#ff5a00;border-color:#ff5a00;color:#fff}
.fm-news-card{border:1px solid #eee;border-radius:16px;background:#fff;padding:14px 16px;margin:0 0 10px}
.fm-news-top{display:flex;align-items:center;gap:8px;margin:0 0 8px}
.fm-news-badge{font-size:11px;font-weight:800;color:#c2410c;background:#fff4e8;border-radius:6px;padding:2px 7px}
.fm-news-time{font-size:11.5px;color:#9aa3bf;font-weight:600}
.fm-news-title{font-size:15.5px;font-weight:800;color:#15151b;line-height:1.4;margin:0 0 6px}
.fm-news-body{font-size:13px;color:#4b5563;line-height:1.6;white-space:pre-line;margin:0}
.fm-news-empty{text-align:center;color:#9aa3bf;font-size:13.5px;padding:30px 0}
`;

export default function News({ onBack, simulation }) {
  const [rows, setRows] = useState(null);
  const [cat, setCat] = useState('all');

  useEffect(() => {
    let alive = true;
    loadOfficialNews(80).then((r) => { if (alive) setRows(Array.isArray(r) ? r : []); });
    return () => { alive = false; };
  }, []);

  // 뉴스 카테고리만 노출(자유·질문 등 커뮤니티 글은 커뮤니티 탭으로) — 공식 자유토픽이 뉴스탭에 새던 문제 수정
  const NEWS_CATS = new Set(['news', 'realestate', 'invest', 'sidejob', 'pension', 'life', 'save']);
  const list = (rows || []).filter((r) => {
    const c = r.category || 'news';
    if (!NEWS_CATS.has(c)) return false;
    return cat === 'all' || c === cat;
  });

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <style>{STYLE}</style>
      <Header tag="소식·뉴스" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">📰 오늘의 경제 소식</p>
        <h2>파이어에 필요한 뉴스만</h2>
        <p>경제·부동산·투자·부업·연금·저축까지, 파이어 관점으로 매일 정리해 드려요. 출처 표기 · 정보 제공이며 투자 조언이 아니에요.</p>
      </section>

      <FireClockPush simulation={simulation} />

      <div className="fm-news-cats">
        <button type="button" className={cat === 'all' ? 'on' : ''} onClick={() => setCat('all')}>전체</button>
        {CATS.map((c) => (
          <button type="button" key={c.key} className={cat === c.key ? 'on' : ''} onClick={() => setCat(c.key)}>{c.emoji} {c.label}</button>
        ))}
      </div>

      <section>
        {rows === null && <p className="fm-news-empty">불러오는 중…</p>}
        {rows !== null && list.length === 0 && <p className="fm-news-empty">아직 이 분야 소식이 없어요. 곧 채워질 거예요 🙂</p>}
        {list.map((r) => {
          const lines = String(r.message || '').split('\n');
          const title = lines[0] || '';
          const body = lines.slice(1).join('\n').trim();
          const m = catMeta(r.category || 'news');
          return (
            <article className="fm-news-card" key={r.id}>
              <div className="fm-news-top">
                <span className="fm-news-badge">{m.emoji} {m.label}</span>
                <span className="fm-news-time">{relativeTime(r.created_at)}</span>
              </div>
              <p className="fm-news-title">{title}</p>
              {body && <p className="fm-news-body">{body}</p>}
            </article>
          );
        })}
      </section>
    </main>
  );
}
