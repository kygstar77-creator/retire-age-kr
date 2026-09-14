// 랜딩 — 계산 전 사용자. 팝업 0·로그인 유도 0. 1분 계산 · 가입 없음. 예시 결과는 남의 숫자라 뺐다(2026-09-14).
import { useEffect, useState } from 'react';
import { TopBar, Card, SectionHead, Button, Notice, IconButton, Icon } from '../../ui/index.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { track } from '../../firemap-v2/dailyData.js';
import CommunityCta from './CommunityCta.jsx';

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

  const clampAge = (v) => Math.max(19, Math.min(80, v));
  const setClamp = (v) => { const c = clampAge(v); setAge(c); setAgeStr(String(c)); };
  const onAgeInput = (e) => { const d = String(e.target.value).replace(/[^0-9]/g, '').slice(0, 3); setAgeStr(d); if (d !== '') { const n = Number(d); if (n >= 19 && n <= 80) setAge(n); } };
  const commitAge = () => { const n = Number(ageStr); const c = (ageStr === '' || Number.isNaN(n)) ? age : clampAge(n); setAge(c); setAgeStr(String(c)); return c; };
  const proof = agg && agg.total > 0 ? `${agg.total.toLocaleString()}명이 계산했어요${agg.avgEarliest ? ` · 평균 파이어 ${agg.avgEarliest}세` : ''}` : '';

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar onHome={() => onMove('home')} />

      {challenge && (
        <Notice tone="accent" icon={<Icon name="fire" />} title={challenge.ea ? `친구는 ${challenge.ea}세에 파이어 가능` : '친구가 파이어 등수를 보냈어요'}>
          {challenge.pct != null ? `또래 상위 ${challenge.pct}% · ` : ''}당신은 몇 살에 가능할까요? 1분이면 나와요.
        </Notice>
      )}

      <Card variant="hero" padding="lg">
        <SectionHead kicker="1분 계산 · 가입 없음" title={<>나는 몇 살에<br />파이어할 수 있을까?</>} desc="자산·저축·생활비만 넣으면 물가·국민연금까지 반영한 현실적인 파이어 나이가 나와요." />
        <div className="ds-row sc-home-agebox">
          <span className="ds-body-sm ds-bold">현재 나이</span>
          <div className="ds-row">
            <IconButton label="나이 감소" size="sm" onClick={() => setClamp(age - 1)}>−</IconButton>
            <input aria-label="나이" className="ds-input num sc-home-agein" inputMode="numeric" value={ageStr} onChange={onAgeInput} onBlur={commitAge} />
            <span className="ds-body-sm">세</span>
            <IconButton label="나이 증가" size="sm" onClick={() => setClamp(age + 1)}>+</IconButton>
          </div>
        </div>
        <Button variant="primary" size="lg" full className="ds-mt-3" onClick={() => { const a = commitAge(); track('start_calc', { age: a, from: challenge ? 'share' : 'home' }); onStart(a); }}>
          {challenge ? '나도 계산하고 친구랑 비교하기 →' : '내 파이어 나이 계산하기 →'}
        </Button>
        {proof && <p className="ds-caption ds-textcenter ds-mt-2 ds-mb-0">{proof}</p>}
      </Card>

      <CommunityCta where="landing" />

      <p className="ds-caption ds-textcenter"><a className="ds-link ds-link--muted" href="/privacy">개인정보처리방침</a> · <a className="ds-link ds-link--muted" href="/disclaimer">면책</a> · <a className="ds-link ds-link--muted" href="/contact">문의</a></p>
    </main>
  );
}
