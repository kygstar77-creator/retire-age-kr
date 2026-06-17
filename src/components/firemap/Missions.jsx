import { useMemo, useState } from 'react';
import { journeyStage } from '../../utils/journeyStage.js';
import { journeyModel } from '../../utils/journeyModel.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { account } from '../../utils/identity.js';
import { missionsFor, setManual } from '../../utils/missions.js';
import { track } from '../../firemap-v2/dailyData.js';

// 이번 단계 미션 — 자동 판정 + 수동 체크. 의지를 유지하는 진짜 할 일.
export default function Missions({ simulation, onMove }) {
  const [tick, setTick] = useState(0);
  const data = useMemo(() => {
    let adv = 0; try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
    let histLen = 0; try { histLen = getAssetHistory().length; } catch { /* ignore */ }
    let j; try { j = journeyStage(simulation, { advanceDays: adv, assetHistoryLen: histLen }); } catch { return null; }
    const s = j.signals || {};
    let rateOK = false;
    try { const m = journeyModel(simulation, { stage: j.stage }); rateOK = m.targets.curSavingsRate >= m.targets.needSavingsRate; } catch { /* ignore */ }
    const acc = account();
    const asset = s.asset || (simulation && simulation.inputs && simulation.inputs.financialAsset) || 0;
    const ctx = { calculated: s.calculated, histLen, saveTotal: s.saveTotal || 0, loggedIn: !!(acc && acc.handle), rateOK, asset, notif: s.notif };
    return { stage: j.stage, current: j.current, ...missionsFor(j.stage, ctx) };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [simulation, tick]);

  if (!data || !data.total) return null;

  const handle = (it) => {
    if (it.kind === 'auto') { if (!it.done && it.to) onMove(it.to); return; }
    setManual(it.id, !it.done);
    try { track('mission_toggle', { id: it.id, on: !it.done }); } catch { /* ignore */ }
    setTick((t) => t + 1);
  };

  const pct = Math.round((data.doneCount / data.total) * 100);

  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.kicker}>🎖️ 이번 단계 미션</span>
        <span style={S.count}>{data.doneCount}<span style={S.countTot}>/{data.total}</span></span>
      </div>
      {data.current ? <p style={S.stageline}><b style={{ color: '#ff5a00' }}>{data.current.emoji} {data.current.name}</b> 단계의 할 일</p> : null}
      <div style={S.track}><div style={{ ...S.fill, width: `${Math.max(3, pct)}%` }} /></div>

      <div style={S.list}>
        {data.items.map((it) => (
          <button type="button" key={it.id} style={S.row} onClick={() => handle(it)}>
            <span style={{ ...S.check, ...(it.done ? S.checkOn : S.checkOff) }}>{it.done ? '✓' : ''}</span>
            <span style={S.tx}>
              <b style={{ ...S.label, ...(it.done ? S.labelDone : null) }}>{it.label}</b>
              <em style={S.hint}>{it.hint}{it.kind === 'auto' && !it.done && it.to ? ' · 하러 가기 ›' : ''}</em>
            </span>
            {it.kind === 'auto' && it.done ? <span style={S.autoTag}>자동</span> : null}
          </button>
        ))}
      </div>

      {data.allDone
        ? <p style={S.allDone}>🎉 이번 단계 미션 완료! 다음 단계가 열렸어요</p>
        : <button type="button" style={S.more} onClick={() => onMove('journey')}>단계별 할 일 전체 보기 ›</button>}
    </section>
  );
}

const S = {
  card: { borderColor: 'rgba(30,40,89,0.14)' },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  count: { fontSize: 18, fontWeight: 800, color: '#ff5a00', fontVariantNumeric: 'tabular-nums' },
  countTot: { fontSize: 12, fontWeight: 700, color: '#9aa3bf', marginLeft: 1 },
  stageline: { fontSize: 12.5, color: '#6b6f76', margin: '0 0 10px', fontWeight: 600 },
  track: { height: 7, borderRadius: 9, background: '#f0ede9', overflow: 'hidden', marginBottom: 14 },
  fill: { height: '100%', borderRadius: 9, background: 'linear-gradient(90deg,#FFB48F,#ff5a00)' },
  list: { display: 'flex', flexDirection: 'column', gap: 9 },
  row: { display: 'flex', alignItems: 'center', gap: 11, width: '100%', textAlign: 'left', cursor: 'pointer', background: '#fff', border: '1px solid #ececec', borderRadius: 12, padding: '11px 12px' },
  check: { flex: '0 0 auto', width: 22, height: 22, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, fontWeight: 800 },
  checkOn: { background: '#ff5a00', color: '#fff', border: '2px solid #ff5a00' },
  checkOff: { background: '#fff', color: 'transparent', border: '2px solid #d7dae0' },
  tx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, gap: 2 },
  label: { fontSize: 13.5, fontWeight: 700, color: '#15151b', lineHeight: 1.3 },
  labelDone: { color: '#9aa3bf', textDecoration: 'line-through' },
  hint: { fontSize: 11.5, fontWeight: 500, color: '#8a8f99', fontStyle: 'normal' },
  autoTag: { fontSize: 10, fontWeight: 800, color: '#0f6e56', background: '#e6f5ef', borderRadius: 6, padding: '2px 6px', flex: '0 0 auto' },
  allDone: { fontSize: 12.5, fontWeight: 800, color: '#0f6e56', textAlign: 'center', margin: '14px 0 0' },
  more: { width: '100%', marginTop: 12, background: 'none', border: 0, color: '#1e2859', fontWeight: 700, fontSize: 12.5, cursor: 'pointer', textAlign: 'center', padding: '4px 0' }
};
