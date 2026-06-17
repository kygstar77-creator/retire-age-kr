import { useEffect, useMemo, useState } from 'react';
import { journeyStage } from '../../utils/journeyStage.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { buildSimulation } from '../../utils/retirementSimulator.js';
import { dailyNeedOf } from '../../firemap-v2/dailyData.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';

const SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');

const ASSET_MS = [
  { v: 100000000, label: '1억' },
  { v: 300000000, label: '3억' },
  { v: 500000000, label: '5억' },
  { v: 1000000000, label: '10억' }
];

export default function JourneyMap({ simulation, onMove }) {
  const [peerAvg, setPeerAvg] = useState(null);
  const [celebrate, setCelebrate] = useState(null);
  const [marketRet, setMarketRet] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchAggregates().then((a) => { if (alive && a && a.avgEarliest) setPeerAvg(a.avgEarliest); }).catch(() => {});
    fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_market_latest`, { method: 'POST', headers: { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json' }, body: '{}' })
      .then((r) => (r.ok ? r.json() : [])).then((rows) => { const m = (rows || []).find((x) => x.symbol === '^spx'); if (alive && m && typeof m.ret_7d === 'number') setMarketRet(m.ret_7d); }).catch(() => {});
    return () => { alive = false; };
  }, []);

  const j = useMemo(() => {
    let adv = 0;
    try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
    let histLen = 0;
    try { histLen = getAssetHistory().length; } catch { /* ignore */ }
    return journeyStage(simulation, { advanceDays: adv, peerAvg, assetHistoryLen: histLen });
  }, [simulation, peerAvg]);

  useEffect(() => {
    if (!j.earliest) return;
    try {
      const done = j.milestones.filter((m) => m.done).map((m) => m.label);
      let seen = []; try { seen = JSON.parse(localStorage.getItem('fm_journey_seen') || '[]'); } catch { /* ignore */ }
      const fresh = done.filter((l) => !seen.includes(l));
      if (seen.length > 0 && fresh.length > 0) setCelebrate(fresh[fresh.length - 1]);
      localStorage.setItem('fm_journey_seen', JSON.stringify(done));
    } catch { /* ignore */ }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [j.stage]);

  // 살아있는 파이어 — 이번 주 시장(S&P500) 수익률을 내 자산에 적용 → 일일필요액으로 환산해 파이어 '며칠' 움직였는지.
  const marketLiving = useMemo(() => {
    if (marketRet == null) return null;
    const asset = j.asset;
    if (!(asset > 0)) return { pct: marketRet, days: 0 };
    let days = 0;
    try {
      const need = dailyNeedOf(simulation); // 원/일, 목표 달성이면 null
      if (need && need > 0) days = Math.round((asset * (marketRet / 100)) / need);
    } catch { /* ignore */ }
    return { pct: marketRet, days };
  }, [marketRet, simulation, j.asset]);

  const living = useMemo(() => {
    try {
      const hist = getAssetHistory();
      if (hist.length >= 2 && simulation && simulation.inputs && simulation.earliestRetirementAge) {
        const prevAsset = hist[hist.length - 2].v;
        const prevSim = buildSimulation({ ...simulation.inputs, financialAsset: prevAsset });
        const e0 = prevSim.earliestRetirementAge;
        const e1 = simulation.earliestRetirementAge;
        if (e0 && e1 && e0 !== e1) return { years: e0 - e1 };
      }
    } catch { /* ignore */ }
    return null;
  }, [simulation]);

  if (!j.earliest) return null;

  const acc = account();
  const loggedIn = !!(acc && acc.handle);

  const nextMs = ASSET_MS.find((m) => j.asset < m.v);
  const prevMsV = nextMs ? (ASSET_MS.filter((m) => m.v < nextMs.v).map((m) => m.v).pop() || 0) : 0;
  const msProg = nextMs ? Math.max(4, Math.min(100, Math.round(((j.asset - prevMsV) / (nextMs.v - prevMsV)) * 100))) : 100;

  const go = (to) => { try { track('journey_next_step', { stage: j.stage, to }); } catch { /* ignore */ } onMove(to); };
  const mlColor = marketLiving ? (marketLiving.days > 0 ? '#0f6e56' : marketLiving.days < 0 ? '#854f0b' : '#6b6f76') : '#0f6e56';

  return (
    <section className="fm-card" style={S.card}>
      {celebrate && (
        <div style={S.celebrate}>🎉 <b>{celebrate}</b> 달성! 한 단계 가까워졌어요</div>
      )}

      <div style={S.head}>
        <span style={S.kicker}>내 파이어 여정</span>
        <span style={S.stageNo}>{j.stage}<span style={S.stageNoTot}>/6단계</span></span>
      </div>

      <div style={S.rail}>
        <div style={S.railLine} />
        <div style={{ ...S.railFill, width: `${((j.stage - 1) / 5) * 100}%` }} />
        <div style={S.nodes}>
          {j.stages.map((st) => {
            const done = st.n < j.stage;
            const cur = st.n === j.stage;
            return (
              <div key={st.key} style={S.node}>
                <div style={{ ...S.dot, ...(done ? S.dotDone : cur ? S.dotCur : S.dotFut) }}>{done ? '✓' : st.emoji}</div>
                <div style={{ ...S.nodeLabel, ...(cur ? S.nodeLabelCur : done ? S.nodeLabelDone : null) }}>{st.name}</div>
              </div>
            );
          })}
        </div>
      </div>

      <p style={S.here}><b style={{ color: '#ff5a00' }}>{j.current.emoji} {j.current.name}</b> 단계예요 · {j.current.tag}</p>

      <button type="button" style={S.cta} onClick={() => go(j.nextStep.to)}>
        <span style={S.ctaTextWrap}>
          <span style={S.ctaCap}>다음 한 걸음</span>
          <span style={S.ctaMain}>{j.nextStep.label}</span>
        </span>
        <span style={S.ctaArrow}>→</span>
      </button>

      {nextMs && (
        <div style={S.goal}>
          <div style={S.goalTop}>
            <span style={S.goalLabel}>다음 목표 · <b style={{ color: '#1e2859' }}>{nextMs.label} 돌파</b></span>
            <span style={S.goalGap}>{formatWon(Math.max(0, nextMs.v - j.asset))} 남음</span>
          </div>
          <div style={S.goalTrack}><div style={{ ...S.goalFill, width: `${msProg}%` }} /></div>
        </div>
      )}

      {marketLiving
        ? <p style={{ ...S.momentum, color: mlColor }}>📈 이번 주 시장 {marketLiving.pct > 0 ? '+' : ''}{marketLiving.pct}%{Math.abs(marketLiving.days) >= 1 ? <> — 파이어 <b>{Math.abs(marketLiving.days)}일</b> {marketLiving.days > 0 ? '빨라졌어요' : '늘춰졌어요'}</> : ' 반영 중'} <span style={S.mlNote}>· S&P500 기준</span></p>
        : living
          ? <p style={S.momentum}>📈 지난 기록보다 파이어 <b>{Math.abs(living.years) >= 1 ? `${Math.abs(living.years)}년` : '약간'}</b> {living.years > 0 ? '빨라졌어요' : '늘춰졌어요'}</p>
          : (j.momentum ? <p style={S.momentum}>🔥 이번 달 파이어 <b>{fmtAdv(j.momentum.advanceDays)}</b> 당겼어요</p> : null)}

      {!loggedIn && (
        <button type="button" style={S.profile} onClick={() => { try { track('journey_profile_cta', {}); } catch { /* ignore */ } onMove('account'); }}>
          🔒 이 여정을 저장하려면 — <b style={{ color: '#ff5a00' }}>내 파이어 프로필 만들기 ›</b>
        </button>
      )}

      <button type="button" style={S.indexLink} onClick={() => { try { track('journey_index', {}); } catch { /* ignore */ } onMove('index'); }}>
        📊 대한민국 파이어 지수에서 내 위치 보기 ›
      </button>
    </section>
  );
}

function fmtAdv(days) {
  const d = Math.round(days);
  if (d >= 365) { const y = Math.floor(d / 365); const r = Math.round((d - y * 365) / 30); return r > 0 ? `${y}년 ${r}개월` : `${y}년`; }
  if (d >= 30) { const m = Math.floor(d / 30); const r = d - m * 30; return r > 0 ? `${m}개월 ${r}일` : `${m}개월`; }
  return `${Math.max(1, d)}일`;
}

const S = {
  card: { borderColor: 'rgba(255,90,0,0.3)', boxShadow: '0 1px 2px rgba(20,18,15,.04), 0 18px 36px -20px rgba(255,90,0,.28)' },
  celebrate: { background: 'linear-gradient(90deg,#FFF0E8,#FFF8F4)', border: '1px solid rgba(255,90,0,0.25)', borderRadius: 12, padding: '9px 12px', fontSize: 12.5, color: '#9a3a12', fontWeight: 700, marginBottom: 13 },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  stageNo: { fontSize: 18, fontWeight: 800, color: '#ff5a00', fontVariantNumeric: 'tabular-nums' },
  stageNoTot: { fontSize: 11, fontWeight: 700, color: '#9aa3bf', marginLeft: 1 },
  rail: { position: 'relative', margin: '4px 4px 12px' },
  railLine: { position: 'absolute', top: 15, left: 15, right: 15, height: 3, background: '#eef0f3', borderRadius: 9 },
  railFill: { position: 'absolute', top: 15, left: 15, height: 3, background: 'linear-gradient(90deg,#FFB48F,#ff5a00)', borderRadius: 9, maxWidth: 'calc(100% - 30px)' },
  nodes: { position: 'relative', display: 'flex', justifyContent: 'space-between' },
  node: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 5, width: 46 },
  dot: { width: 30, height: 30, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, border: '2px solid #fff' },
  dotDone: { background: '#ff5a00', color: '#fff', boxShadow: '0 2px 6px rgba(255,90,0,0.35)' },
  dotCur: { background: '#fff', boxShadow: '0 0 0 2px #ff5a00, 0 4px 10px rgba(255,90,0,0.4)', transform: 'scale(1.14)' },
  dotFut: { background: '#f1f0ee', color: '#b7b2a8' },
  nodeLabel: { fontSize: 10, fontWeight: 700, color: '#b0aaa1' },
  nodeLabelCur: { color: '#ff5a00' },
  nodeLabelDone: { color: '#6b6f76' },
  here: { fontSize: 12.5, color: '#6b6f76', margin: '0 0 12px', lineHeight: 1.5 },
  cta: { width: '100%', border: 0, cursor: 'pointer', textAlign: 'left', background: 'linear-gradient(180deg,#ff6a35,#ee4a1f)', color: '#fff', borderRadius: 14, padding: '13px 15px', display: 'flex', alignItems: 'center', boxShadow: '0 12px 24px -10px rgba(232,67,28,0.55)' },
  ctaTextWrap: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 },
  ctaCap: { fontSize: 10.5, fontWeight: 700, opacity: 0.85, letterSpacing: '0.02em' },
  ctaMain: { fontSize: 15, fontWeight: 800, marginTop: 2 },
  ctaArrow: { fontSize: 18, fontWeight: 800, marginLeft: 10, flex: '0 0 auto' },
  goal: { marginTop: 13 },
  goalTop: { display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 6 },
  goalLabel: { fontSize: 12, color: '#6b6f76', fontWeight: 600 },
  goalGap: { fontSize: 12, color: '#ff5a00', fontWeight: 800, fontVariantNumeric: 'tabular-nums' },
  goalTrack: { height: 7, borderRadius: 9, background: '#f0ede9', overflow: 'hidden' },
  goalFill: { height: '100%', borderRadius: 9, background: 'linear-gradient(90deg,#FFB48F,#ff5a00)' },
  momentum: { fontSize: 12.5, color: '#0f6e56', fontWeight: 700, margin: '12px 0 0', textAlign: 'center', lineHeight: 1.5 },
  mlNote: { color: '#9aa3bf', fontWeight: 600, fontSize: 11 },
  profile: { width: '100%', marginTop: 12, background: 'rgba(255,90,0,0.06)', border: '1px solid rgba(255,90,0,0.22)', borderRadius: 12, padding: '11px 13px', fontSize: 12.5, color: '#6b6f76', fontWeight: 600, cursor: 'pointer', textAlign: 'center' },
  indexLink: { width: '100%', marginTop: 10, background: 'none', border: 0, color: '#1e2859', fontWeight: 700, fontSize: 12.5, cursor: 'pointer', textAlign: 'center', padding: '4px 0' }
};
