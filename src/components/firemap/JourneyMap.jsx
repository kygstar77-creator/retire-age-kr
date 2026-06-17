import { useEffect, useMemo, useState } from 'react';
import { journeyStage } from '../../utils/journeyStage.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { account } from '../../utils/identity.js';
import { track } from '../../firemap-v2/dailyData.js';

// 파이어 여정 지도 — "너 여기 + 다음 한 걸음 + 모멘텀". 흔어진 기능을 하나의 길로.
export default function JourneyMap({ simulation, onMove }) {
  const [peerAvg, setPeerAvg] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchAggregates().then((a) => { if (alive && a && a.avgEarliest) setPeerAvg(a.avgEarliest); }).catch(() => {});
    return () => { alive = false; };
  }, []);

  const j = useMemo(() => {
    let adv = 0;
    try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
    let histLen = 0;
    try { histLen = getAssetHistory().length; } catch { /* ignore */ }
    return journeyStage(simulation, { advanceDays: adv, peerAvg, assetHistoryLen: histLen });
  }, [simulation, peerAvg]);

  if (!j.earliest) return null; // 계산 전이면 지도 숨김

  const acc = account();
  const loggedIn = !!(acc && acc.handle);

  const go = (to) => {
    try { track('journey_next_step', { stage: j.stage, to }); } catch { /* ignore */ }
    onMove(to);
  };

  return (
    <section className="fm-card" style={S.card}>
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
                <div style={{ ...S.dot, ...(done ? S.dotDone : cur ? S.dotCur : S.dotFut) }}>
                  {done ? '✓' : st.emoji}
                </div>
                <div style={{ ...S.nodeLabel, ...(cur ? S.nodeLabelCur : done ? S.nodeLabelDone : null) }}>{st.name}</div>
              </div>
            );
          })}
        </div>
      </div>

      <p style={S.here}><b style={{ color: '#ff5a00' }}>{j.current.emoji} {j.current.name}</b> 단계예요 · {j.current.tag}</p>

      <button type="button" style={S.cta} onClick={() => go(j.nextStep.to)}>
        <span style={S.ctaCap}>다음 한 걸음</span>
        <span style={S.ctaMain}>{j.nextStep.label}</span>
        <span style={S.ctaArrow}>→</span>
      </button>

      {j.momentum && (
        <p style={S.momentum}>🔥 이번 달 파이어 <b>{fmtAdv(j.momentum.advanceDays)}</b> 당겨어요</p>
      )}

      {!loggedIn && (
        <button type="button" style={S.profile} onClick={() => { try { track('journey_profile_cta', {}); } catch { /* ignore */ } onMove('account'); }}>
          🔒 이 여정을 저장하려면 — <b>내 파이어 프로필 만들기 ›</b>
        </button>
      )}
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
  card: { borderColor: 'rgba(255,90,0,0.28)' },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  stageNo: { fontSize: 18, fontWeight: 800, color: '#ff5a00', fontVariantNumeric: 'tabular-nums' },
  stageNoTot: { fontSize: 11, fontWeight: 700, color: '#9aa3bf', marginLeft: 1 },
  rail: { position: 'relative', margin: '4px 4px 12px' },
  railLine: { position: 'absolute', top: 15, left: 15, right: 15, height: 3, background: '#eef0f3', borderRadius: 9 },
  railFill: { position: 'absolute', top: 15, left: 15, height: 3, background: '#ff5a00', borderRadius: 9, maxWidth: 'calc(100% - 30px)' },
  nodes: { position: 'relative', display: 'flex', justifyContent: 'space-between' },
  node: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 5, width: 46 },
  dot: { width: 30, height: 30, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, border: '2px solid #fff' },
  dotDone: { background: '#ff5a00', color: '#fff', boxShadow: '0 2px 6px rgba(255,90,0,0.35)' },
  dotCur: { background: '#fff', boxShadow: '0 0 0 2px #ff5a00, 0 4px 10px rgba(255,90,0,0.35)', transform: 'scale(1.12)' },
  dotFut: { background: '#f1f0ee', color: '#b7b2a8' },
  nodeLabel: { fontSize: 10, fontWeight: 700, color: '#b0aaa1' },
  nodeLabelCur: { color: '#ff5a00' },
  nodeLabelDone: { color: '#6b6f76' },
  here: { fontSize: 12.5, color: '#6b6f76', margin: '0 0 12px', lineHeight: 1.5 },
  cta: { width: '100%', border: 0, cursor: 'pointer', textAlign: 'left', background: '#ff5a00', color: '#fff', borderRadius: 14, padding: '13px 15px', display: 'flex', flexDirection: 'column', position: 'relative', boxShadow: '0 10px 22px -10px rgba(255,90,0,0.5)' },
  ctaCap: { fontSize: 10.5, fontWeight: 700, opacity: 0.85, letterSpacing: '0.02em' },
  ctaMain: { fontSize: 15, fontWeight: 800, marginTop: 2, paddingRight: 18 },
  ctaArrow: { position: 'absolute', right: 15, top: '50%', transform: 'translateY(-50%)', fontSize: 18, fontWeight: 800 },
  momentum: { fontSize: 12.5, color: '#0f6e56', fontWeight: 700, margin: '10px 0 0', textAlign: 'center' },
  profile: { width: '100%', marginTop: 10, background: 'rgba(255,90,0,0.06)', border: '1px solid rgba(255,90,0,0.2)', borderRadius: 12, padding: '11px 13px', fontSize: 12.5, color: '#6b6f76', fontWeight: 600, cursor: 'pointer', textAlign: 'center' }
};
