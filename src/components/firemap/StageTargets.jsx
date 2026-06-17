import { useMemo } from 'react';
import { journeyModel } from '../../utils/journeyModel.js';
import { journeyStage } from '../../utils/journeyStage.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { track } from '../../firemap-v2/dailyData.js';

const won = (n) => formatWon(Math.round(n || 0));

// 내 단계 타깃 + 상황별 정보 — "투자 추천"이 아니라 단계에 맞는 재무 타깃과 필요한 정보를 제공.
export default function StageTargets({ simulation, onMove }) {
  const m = useMemo(() => {
    let stage = 1;
    try {
      let adv = 0;
      try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
      let histLen = 0;
      try { histLen = getAssetHistory().length; } catch { /* ignore */ }
      stage = journeyStage(simulation, { advanceDays: adv, assetHistoryLen: histLen }).stage || 1;
    } catch { /* ignore */ }
    return journeyModel(simulation, { stage });
  }, [simulation]);

  if (!m.plan.G || !m.plan.targetAge) return null;
  const t = m.targets;
  const a = t.allocation;
  const rateOK = t.curSavingsRate >= t.needSavingsRate;
  const go = (to) => { try { track('stage_info', { stage: m.stage, to }); } catch { /* ignore */ } onMove(to); };

  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.kicker}>🧭 내 단계 타깃 · 지금 맞춰야 할 것</span>
      </div>

      <div style={S.block}>
        <div style={S.blockTop}>
          <span style={S.blockLabel}>저축률 (가용소득 대비)</span>
          <span style={S.blockVal}>지금 <b style={{ color: rateOK ? '#0f6e56' : '#e8431c' }}>{t.curSavingsRate}%</b> · 목표 <b>{t.needSavingsRate}%</b></span>
        </div>
        <div style={S.rateTrack}>
          <div style={{ ...S.rateFill, width: `${Math.max(2, Math.min(100, t.curSavingsRate))}%`, background: rateOK ? 'linear-gradient(90deg,#7fd3b0,#10b981)' : 'linear-gradient(90deg,#FFB48F,#ff5a00)' }} />
          <div style={{ ...S.rateMark, left: `${Math.max(0, Math.min(100, t.needSavingsRate))}%` }} title="목표" />
        </div>
        <p style={S.blockMsg}>
          {rateOK
            ? <>목표 저축률을 이미 넘었어요 👏 이 속도면 충분해요.</>
            : <>목표까지 매달 <b style={{ color: '#e8431c' }}>{won(t.needMonthly)}</b> 필요 {t.sideIncomeGoal > 0 ? <>· 부업·추가소득으로 <b>{won(t.sideIncomeGoal)}</b> 메우는 것도 방법</> : null}</>}
        </p>
      </div>

      <div style={S.block}>
        <div style={S.blockTop}>
          <span style={S.blockLabel}>참고 자산배분 (나이·단계 기준)</span>
        </div>
        <div style={S.allocBar}>
          <div style={{ ...S.allocSeg, width: `${a.growth}%`, background: '#ff5a00' }} />
          <div style={{ ...S.allocSeg, width: `${a.income}%`, background: '#10b981' }} />
          <div style={{ ...S.allocSeg, width: `${a.safe}%`, background: '#1e2859' }} />
        </div>
        <div style={S.allocLegend}>
          <span><i style={{ ...S.dot, background: '#ff5a00' }} />성장(주식·ETF) {a.growth}%</span>
          <span><i style={{ ...S.dot, background: '#10b981' }} />인컴(배당·임대) {a.income}%</span>
          <span><i style={{ ...S.dot, background: '#1e2859' }} />안전(채권·예금) {a.safe}%</span>
        </div>
      </div>

      <div style={S.miniRow}>
        <div style={S.miniCell}><small style={S.miniSmall}>주거비 상한(월)</small><b style={S.miniBig}>{won(t.housingMax)}</b></div>
        <div style={S.miniDiv} />
        <div style={S.miniCell}><small style={S.miniSmall}>비상금 목표</small><b style={S.miniBig}>{won(t.emergencyFund)}</b></div>
      </div>

      <p style={S.infoTitle}>지금 알아두면 좋은 것</p>
      <div style={S.infoList}>
        {m.situation.map((s) => (
          <button type="button" key={s.title} style={S.infoRow} onClick={() => go(s.to)}>
            <span style={S.infoIco}>{s.ico}</span>
            <span style={S.infoTx}>
              <b style={S.infoTitleTx}>{s.title}</b>
              <em style={S.infoDesc}>{s.desc}</em>
            </span>
            <span style={S.infoGo}>›</span>
          </button>
        ))}
      </div>

      <p style={S.note}>※ 정보 제공 목적이며 투자자문이 아니에요. 배분은 나이·단계 기준 참고치예요.</p>
    </section>
  );
}

const S = {
  card: { borderColor: 'rgba(30,40,89,0.14)' },
  head: { marginBottom: 14 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  block: { marginBottom: 16 },
  blockTop: { display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 8, gap: 8 },
  blockLabel: { fontSize: 12, fontWeight: 700, color: '#6b6f76' },
  blockVal: { fontSize: 12.5, fontWeight: 600, color: '#15151b', whiteSpace: 'nowrap' },
  rateTrack: { position: 'relative', height: 8, borderRadius: 9, background: '#f0ede9', overflow: 'visible', marginBottom: 8 },
  rateFill: { height: '100%', borderRadius: 9 },
  rateMark: { position: 'absolute', top: -3, width: 3, height: 14, background: '#1e2859', borderRadius: 2, transform: 'translateX(-50%)' },
  blockMsg: { fontSize: 12.5, color: '#565c68', fontWeight: 600, lineHeight: 1.55, margin: 0 },
  allocBar: { display: 'flex', height: 14, borderRadius: 8, overflow: 'hidden', marginBottom: 9 },
  allocSeg: { height: '100%' },
  allocLegend: { display: 'flex', flexWrap: 'wrap', gap: '4px 14px', fontSize: 11.5, color: '#6b6f76', fontWeight: 700 },
  dot: { display: 'inline-block', width: 9, height: 9, borderRadius: '50%', marginRight: 5, verticalAlign: 'middle' },
  miniRow: { display: 'flex', alignItems: 'center', background: '#f8f6f2', borderRadius: 12, padding: '11px 0', marginBottom: 16 },
  miniCell: { flex: 1, textAlign: 'center', display: 'flex', flexDirection: 'column', gap: 3 },
  miniSmall: { fontSize: 11, color: '#9aa3bf', fontWeight: 700 },
  miniBig: { fontSize: 16, color: '#15151b', fontWeight: 800, fontVariantNumeric: 'tabular-nums' },
  miniDiv: { width: 1, alignSelf: 'stretch', background: '#e7e3dd', margin: '2px 0' },
  infoTitle: { fontSize: 12, fontWeight: 800, color: '#1e2859', margin: '0 0 10px' },
  infoList: { display: 'flex', flexDirection: 'column', gap: 8 },
  infoRow: { display: 'flex', alignItems: 'center', gap: 11, width: '100%', textAlign: 'left', cursor: 'pointer', background: '#fff', border: '1px solid #ececec', borderRadius: 12, padding: '11px 12px' },
  infoIco: { fontSize: 18, flex: '0 0 auto' },
  infoTx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, gap: 2 },
  infoTitleTx: { fontSize: 13, fontWeight: 800, color: '#15151b', lineHeight: 1.3 },
  infoDesc: { fontSize: 11.5, fontWeight: 500, color: '#8a8f99', fontStyle: 'normal', lineHeight: 1.4 },
  infoGo: { fontSize: 17, color: '#c2c7d0', fontWeight: 700, flex: '0 0 auto' },
  note: { fontSize: 10.5, color: '#9aa3bf', lineHeight: 1.5, margin: '14px 0 0' }
};
