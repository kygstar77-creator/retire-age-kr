// 랜딩 — 계산 전 사용자. 팝업 0·로그인 유도 0. 1분 계산 · 가입 없음 · 결과 미리보기(ChooseFI 3체크 · Networthify).
import { useEffect, useState } from 'react';
import { TopBar, Card, SectionHead, Button, Stat, Notice, IconButton } from '../../ui/index.js';
import { getLatestRank } from '../../firemap-v2/rankHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL } from '../../firemap-v2/links.js';
import Today from './Today.jsx';

function readChallenge() {
  try {
    const q = new URLSearchParams(window.location.search || '');
    if (q.get('from') !== 'share') return null;
    const ea = parseInt(q.get('ea') || '', 10); const pos = parseInt(q.get('pos') || '', 10); const tot = parseInt(q.get('tot') || '', 10);
    const pct = (pos > 0 && tot > 0) ? Math.max(1, Math.round((pos / tot) * 100)) : null;
    if (!ea && !pct) return null;
    return { ea: ea || null, pos: pos || null, tot: tot || null, pct };
  } catch { return null; }
}

export default function Home({ onStart, onMove, simulation }) {
  const [agg, setAgg] = useState(null);
  const [age, setAge] = useState(35);
  const [ageStr, setAgeStr] = useState('35');
  const [challenge] = useState(readChallenge);
  useEffect(() => { if (challenge) { try { track('share_inbound', { ea: challenge.ea || 0, pct: challenge.pct || 0 }); } catch { /* ignore */ } } }, [challenge]);
  useEffect(() => { let alive = true; fetchAggregates().then((a) => { if (alive) setAgg(a); }); return () => { alive = false; }; }, []);

  const latest = getLatestRank();
  if (latest && !challenge) return <Today simulation={simulation} onMove={onMove} />;

  const clampAge = (v) => Math.max(19, Math.min(80, v));
  const setClamp = (v) => { const c = clampAge(v); setAge(c); setAgeStr(String(c)); };
  const onAgeInput = (e) => { const d = String(e.target.value).replace(/[^0-9]/g, '').slice(0, 3); setAgeStr(d); if (d !== '') { const n = Number(d); if (n >= 19 && n <= 80) setAge(n); } };
  const commitAge = () => { const n = Number(ageStr); const c = (ageStr === '' || Number.isNaN(n)) ? age : clampAge(n); setAge(c); setAgeStr(String(c)); return c; };
  const proof = agg && agg.total > 0 ? `${agg.total.toLocaleString()}명이 계산했어요${agg.avgEarliest ? ` · 평균 파이어 ${agg.avgEarliest}세` : ''}` : '';

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar onHome={() => onMove('home')} actions={<a className="ds-topbar__handle" href={CAFE_URL} target="_blank" rel="noopener noreferrer"><span>🟢 카페</span></a>} />

      {challenge && (
        <Notice tone="accent" icon="🔥" title={challenge.ea ? `친구는 ${challenge.ea}세에 파이어 가능` : '친구가 파이어 등수를 보냈어요'}>
          {challenge.pct != null ? `또래 상위 ${challenge.pct}% · ` : ''}당신은 몇 살에 가능할까요? 1분이면 나와요.
        </Notice>
      )}

      <Card variant="hero" padding="lg">
        <SectionHead kicker="1분 계산 · 가입 없음" title={<>나는 몇 살에<br />파이어할 수 있을까?</>} desc="자산·저축·생활비만 넣으면 물가·국민연금까지 반영한 현실적인 파이어 나이가 나와요." />
        <div className="ds-row" style={{ justifyContent: 'space-between', background: 'var(--ds-surface-2)', borderRadius: 14, padding: '10px 12px', marginTop: 4 }}>
          <span className="ds-body-sm" style={{ fontWeight: 700 }}>지금 나이</span>
          <div className="ds-row">
            <IconButton label="나이 감소" size="sm" onClick={() => setClamp(age - 1)}>−</IconButton>
            <input aria-label="나이" className="ds-input num" style={{ width: 64, textAlign: 'center', fontSize: 18, fontWeight: 800, padding: '6px 4px' }} inputMode="numeric" value={ageStr} onChange={onAgeInput} onBlur={commitAge} />
            <span className="ds-body-sm">세</span>
            <IconButton label="나이 증가" size="sm" onClick={() => setClamp(age + 1)}>+</IconButton>
          </div>
        </div>
        <Button variant="primary" size="lg" full className="ds-mt-3" onClick={() => { const a = commitAge(); track('start_calc', { age: a, from: challenge ? 'share' : 'home' }); onStart(a); }}>
          {challenge ? '나도 계산하고 친구랑 비교하기 →' : '내 파이어 나이 계산하기 →'}
        </Button>
        {proof && <p className="ds-caption ds-textcenter ds-mt-2" style={{ marginBottom: 0 }}>{proof}</p>}
      </Card>

      <Card variant="soft">
        <SectionHead size="sm" kicker="계산하면 이런 게 나와요" title="숫자 하나로 시작해요" />
        <div className="ds-three" style={{ background: 'var(--ds-surface)', borderRadius: 14, padding: 6 }}>
          <Stat label="파이어 나이" value={<>51<span className="ds-stat__unit">세</span></>} size="md" />
          <Stat label="필요 자산" value={<>13.1<span className="ds-stat__unit">억</span></>} size="md" />
          <Stat label="같은 구간" value={<>18<span className="ds-stat__unit">%</span></>} size="md" />
        </div>
        <p className="ds-caption ds-mt-2" style={{ marginBottom: 0 }}>예시예요. 결과에서 저축·생활비·부업 중 하나만 바꿔도 몇 년이 당겨지는지 보여줘요.</p>
      </Card>

      <Card padding="md">
        <SectionHead size="sm" title="🟢 파이어맵 카페" desc="인증 · 봐주세요 · 파이어 후 하루 — 파이어족 커뮤니티 본진" action={<Button as="a" href={CAFE_URL} target="_blank" rel="noopener noreferrer" variant="tint" size="sm">가기</Button>} />
      </Card>

      <p className="ds-caption ds-textcenter"><a className="ds-link" href="/privacy.html" style={{ color: 'var(--ds-ink-3)' }}>개인정보처리방침</a> · <a className="ds-link" href="/disclaimer.html" style={{ color: 'var(--ds-ink-3)' }}>면책</a> · <a className="ds-link" href="/contact.html" style={{ color: 'var(--ds-ink-3)' }}>문의</a></p>
    </main>
  );
}
