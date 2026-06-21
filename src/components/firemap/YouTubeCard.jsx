import { useEffect, useState } from 'react';
import { track } from '../../firemap-v2/dailyData.js';

const CHANNEL = 'https://www.youtube.com/@firemapkr';

const S = {
  card: { background: '#18224d', borderRadius: 16, padding: '16px 16px 14px', color: '#fff' },
  head: { display: 'flex', alignItems: 'center', gap: 10 },
  play: { width: 34, height: 34, borderRadius: 9, background: '#ff0033', color: '#fff', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 15, flex: '0 0 auto' },
  ttl: { fontSize: 16, fontWeight: 800, margin: 0 },
  sub: { fontSize: 12.5, color: '#9aa4d4', margin: '2px 0 0' },
  vids: { display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginTop: 12 },
  vid: { textDecoration: 'none', color: '#fff' },
  thumb: { width: '100%', aspectRatio: '16 / 9', objectFit: 'cover', borderRadius: 8, display: 'block', background: '#0f1838' },
  vtitle: { fontSize: 11, lineHeight: 1.3, margin: '5px 0 0', color: '#cdd3ee', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' },
  cta: { display: 'block', textAlign: 'center', marginTop: 12, background: '#ff5a00', color: '#fff', fontWeight: 800, fontSize: 14, padding: '11px', borderRadius: 12, textDecoration: 'none' }
};

export default function YouTubeCard() {
  const [vids, setVids] = useState([]);
  useEffect(() => {
    let alive = true;
    fetch('/yt')
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { if (alive && d && Array.isArray(d.videos)) setVids(d.videos.slice(0, 3)); })
      .catch(() => {});
    return () => { alive = false; };
  }, []);
  const hit = (where) => { try { track('youtube_click', { where }); } catch { /* ignore */ } };
  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.play} aria-hidden="true">▶</span>
        <div>
          <p style={S.ttl}>파이어맵 유튜브</p>
          <p style={S.sub}>영상으로 보는 파이어 — 계산 다음, 더 깊이 배우기</p>
        </div>
      </div>
      {vids.length > 0 && (
        <div style={S.vids}>
          {vids.map((v) => (
            <a key={v.id} href={v.url} target="_blank" rel="noopener noreferrer" style={S.vid} onClick={() => hit('video')}>
              <img src={v.thumb} alt={v.title} loading="lazy" style={S.thumb} />
              <p style={S.vtitle}>{v.title}</p>
            </a>
          ))}
        </div>
      )}
      <a href={CHANNEL} target="_blank" rel="noopener noreferrer" style={S.cta} onClick={() => hit('channel')}>▶ 채널 보러가기 · 구독하기 →</a>
    </section>
  );
}
