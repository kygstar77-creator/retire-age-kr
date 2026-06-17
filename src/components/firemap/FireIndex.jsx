import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { track } from '../../firemap-v2/dailyData.js';

// 대한민국 파이어 지수 — 우리 익명 집계로만 만들 수 있는 '표준' 콘텐츠 + 내 위치 비교.
const SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');

const bandLabel = (b) => `${b}대`;

export default function FireIndex({ simulation, onBack }) {
  const [rows, setRows] = useState(null);
  const [err, setErr] = useState(false);

  useEffect(() => {
    let alive = true;
    try { track('fire_index_view', {}); } catch { /* ignore */ }
    (async () => {
      try {
        const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_fire_index`, {
          method: 'POST',
          headers: { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json' },
          body: '{}'
        });
        const data = res.ok ? await res.json() : [];
        if (alive) setRows(Array.isArray(data) ? data : []);
      } catch { if (alive) setErr(true); }
    })();
    return () => { alive = false; };
  }, []);

  const inp = (simulation && simulation.inputs) || {};
  const myAge = Number(inp.currentAge) || 0;
  const myBand = myAge ? Math.min(60, Math.max(20, Math.floor(myAge / 10) * 10)) : null;
  const myTarget = Number(inp.targetRetirementAge) || null;
  const myEarliest = simulation && simulation.earliestRetirementAge;
  const myGap = (myEarliest && myTarget) ? Math.round((myEarliest - myTarget) * 10) / 10 : null;

  const totalN = rows ? rows.reduce((a, r) => a + Number(r.n || 0), 0) : 0;
  const natAvgEarliest = rows && totalN > 0
    ? Math.round((rows.reduce((a, r) => a + Number(r.avg_earliest || 0) * Number(r.n || 0), 0) / totalN) * 10) / 10
    : null;
  const myRow = rows && myBand ? rows.find((r) => Number(r.band) === myBand) : null;

  const pos = (age) => Math.max(0, Math.min(100, ((age - 40) / 20) * 100));

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="대한민국 파이어 지수" onBack={onBack} />

      <section className="fm-card" style={S.hero}>
        <span style={S.kicker}>🔥 대한민국 파이어 지수</span>
        <h1 style={S.h1}>한국인은 몇 살에<br />파이어를 꿈꾸고, 가능할까?</h1>
        {natAvgEarliest != null
          ? <p style={S.heroSub}>함께 계산한 <b>{totalN.toLocaleString()}명</b>의 익명 집계 · 전국 평균 파이어 가능 나이 <b style={{ color: '#ff5a00' }}>{natAvgEarliest}세</b></p>
          : <p style={S.heroSub}>{err ? '집계를 불러오지 못했어요. 잠시 후 다시 시도해 주세요.' : '집계 불러오는 중…'}</p>}
      </section>

      {rows && rows.length > 0 && (
        <section className="fm-card">
          <p style={S.sectTitle}>연령대별 파이어 현황</p>
          {rows.map((r) => {
            const t = Number(r.avg_target), e = Number(r.avg_earliest), gap = Number(r.gap);
            const mine = myBand && Number(r.band) === myBand;
            return (
              <div key={r.band} style={{ ...S.bandRow, ...(mine ? S.bandMine : null) }}>
                <div style={S.bandHead}>
                  <span style={S.bandName}>{bandLabel(r.band)}{mine ? ' · 나' : ''}</span>
                  <span style={S.bandN}>{Number(r.n).toLocaleString()}명</span>
                </div>
                <div style={S.barWrap}>
                  <div style={S.barTrack} />
                  <div style={{ ...S.barSeg, left: `${pos(Math.min(t, e))}%`, width: `${Math.max(2, Math.abs(pos(e) - pos(t)))}%` }} />
                  <div style={{ ...S.pin, left: `${pos(t)}%`, background: '#1e2859' }} />
                  <div style={{ ...S.pin, left: `${pos(e)}%`, background: '#ff5a00' }} />
                </div>
                <div style={S.bandStats}>
                  <span>목표 <b style={{ color: '#1e2859' }}>{t}세</b></span>
                  <span>가능 <b style={{ color: '#ff5a00' }}>{e}세</b></span>
                  <span>격차 <b>{gap > 0 ? `+${gap}` : gap}년</b></span>
                </div>
              </div>
            );
          })}
          <div style={S.legend}><span><i style={{ ...S.dot, background: '#1e2859' }} />목표 나이</span><span><i style={{ ...S.dot, background: '#ff5a00' }} />현실 가능 나이</span></div>
        </section>
      )}

      {myRow && myGap != null && (
        <section className="fm-card" style={S.mine}>
          <p style={S.sectTitle}>📍 {bandLabel(myBand)} 또래 중 내 위치</p>
          <p style={S.mineLead}>당신: 목표 <b>{myTarget}세</b> · 가능 <b style={{ color: '#ff5a00' }}>{myEarliest}세</b> · 격차 <b>{myGap > 0 ? `+${myGap}` : myGap}년</b></p>
          {(() => {
            const cohortGap = Number(myRow.gap);
            const diff = Math.round((myGap - cohortGap) * 10) / 10;
            if (Math.abs(diff) < 0.3) return <p style={S.mineMsg}>또래 평균과 <b>거의 비슷한</b> 격차예요.</p>;
            return diff < 0
              ? <p style={{ ...S.mineMsg, color: '#0f6e56' }}>또래 평균보다 <b>{Math.abs(diff)}년 앞선</b> 계획이에요 👏</p>
              : <p style={{ ...S.mineMsg, color: '#854f0b' }}>또래 평균보다 <b>{diff}년 더 벌어진</b> 격차예요. 다음 한 걸음으로 좁혀봐요.</p>;
          })()}
          <p style={S.mineCmp}>{bandLabel(myBand)} 평균 — 목표 {myRow.avg_target}세 · 가능 {myRow.avg_earliest}세 · 격차 {Number(myRow.gap) > 0 ? `+${myRow.gap}` : myRow.gap}년</p>
        </section>
      )}

      <p style={S.foot}>※ 파이어맵에서 직접 계산한 사용자들의 익명 집계예요(개인 식별정보 없음). 표본 20명 이상 연령대만 표시하며, 집계는 계속 갱신돼요.</p>
    </main>
  );
}

const S = {
  hero: { borderColor: 'rgba(255,90,0,0.3)' },
  kicker: { display: 'inline-block', fontSize: 11.5, fontWeight: 800, color: '#e8431c', background: '#fff0ea', padding: '5px 11px', borderRadius: 999 },
  h1: { fontSize: 22, fontWeight: 800, color: '#15151b', lineHeight: 1.3, letterSpacing: '-0.02em', margin: '13px 0 8px' },
  heroSub: { fontSize: 13, color: '#6b6f76', lineHeight: 1.6, margin: 0 },
  sectTitle: { fontSize: 13, fontWeight: 800, color: '#1e2859', margin: '0 0 14px' },
  bandRow: { padding: '12px 12px', borderRadius: 14, marginBottom: 10, border: '1px solid #ececec', background: '#fff' },
  bandMine: { borderColor: 'rgba(255,90,0,0.4)', background: 'rgba(255,90,0,0.04)' },
  bandHead: { display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 9 },
  bandName: { fontSize: 14, fontWeight: 800, color: '#15151b' },
  bandN: { fontSize: 11.5, fontWeight: 700, color: '#9aa3bf' },
  barWrap: { position: 'relative', height: 16, margin: '4px 0 9px' },
  barTrack: { position: 'absolute', top: 7, left: 0, right: 0, height: 3, background: '#eef0f3', borderRadius: 9 },
  barSeg: { position: 'absolute', top: 7, height: 3, background: 'linear-gradient(90deg,#1e2859,#ff5a00)', borderRadius: 9 },
  pin: { position: 'absolute', top: 2, width: 13, height: 13, borderRadius: '50%', border: '2px solid #fff', transform: 'translateX(-50%)', boxShadow: '0 2px 4px rgba(0,0,0,.18)' },
  bandStats: { display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#6b6f76', fontWeight: 600 },
  legend: { display: 'flex', gap: 16, justifyContent: 'center', marginTop: 6, fontSize: 11, color: '#9aa3bf', fontWeight: 700 },
  dot: { display: 'inline-block', width: 9, height: 9, borderRadius: '50%', marginRight: 5, verticalAlign: 'middle' },
  mine: { borderColor: 'rgba(255,90,0,0.3)', background: 'radial-gradient(120% 90% at 100% 0%, rgba(255,90,0,0.05), transparent 50%), #fff' },
  mineLead: { fontSize: 13.5, color: '#15151b', fontWeight: 600, margin: '0 0 8px' },
  mineMsg: { fontSize: 13, fontWeight: 800, color: '#6b6f76', margin: '0 0 8px' },
  mineCmp: { fontSize: 11.5, color: '#9aa3bf', fontWeight: 600, margin: 0 },
  foot: { fontSize: 11, color: '#9aa3bf', lineHeight: 1.6, padding: '4px 18px 0' }
};
