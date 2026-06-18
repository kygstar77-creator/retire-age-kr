import { firePlan } from '../../utils/firePlan.js';
import { formatWon } from '../../firemap-v2/formatters.js';

const won = (n) => formatWon(Math.round(n || 0));
const eok = (n) => { const v = (n || 0) / 1e8; return v >= 10 ? `${Math.round(v)}억` : `${v.toFixed(1)}억`; };
const readJSON = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

export default function CompletionCard({ simulation, onMove }) {
  const p = firePlan(simulation);
  if (!p.G || !p.targetAge) return null;
  const earliest = simulation && simulation.earliestRetirementAge;
  const annualPct = Math.round(p.annual * 100);

  const fd = readJSON('fm_daily');
  const ym = new Date().toISOString().slice(0, 7);
  const monthSaved = fd && fd.days ? Object.entries(fd.days).filter(([k]) => k.startsWith(ym)).reduce((a, [, v]) => a + (Number(v) || 0), 0) : 0;
  const monthGoal = p.pmt;
  const monthPct = monthGoal > 0 ? Math.max(0, Math.min(100, Math.round((monthSaved / monthGoal) * 100))) : 0;

  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.kicker}>🎯 완주 플랜 · 목표까지의 길</span>
        <span style={S.years}>{p.yearsLeft}년 남음</span>
      </div>

      <div style={S.progRow}>
        <span style={S.bigPct}>{p.progress}<span style={S.bigPctU}>%</span></span>
        <div style={S.progMeta}>
          <div style={S.progTrack}><div style={{ ...S.progFill, width: `${Math.max(2, p.progress)}%` }} /></div>
          <p style={S.progTx}>목표 <b>{eok(p.G)}</b> 중 <b style={{ color: '#ff5a00' }}>{eok(p.A)}</b> · <b>{eok(p.remaining)}</b> 남음</p>
        </div>
      </div>

      <div style={S.ageRow}>
        <div style={S.ageCell}><small style={S.ageSmall}>목표 파이어</small><b style={S.ageBig}>{p.targetAge}세</b></div>
        <div style={S.ageDiv} />
        <div style={S.ageCell}><small style={S.ageSmall}>지금 속도면</small><b style={{ ...S.ageBig, color: '#ff5a00' }}>{earliest ? `${earliest}세` : '—'}</b></div>
      </div>

      {p.alreadyOnTrack ? (
        <div style={S.planBox}>
          <p style={S.planMain}>🎉 지금 자산만 굴려도 목표 도달 — <b>코스트파이어</b> 상태예요</p>
          <p style={S.planSub}>더 안 모아도 연 {annualPct}% 가정 시 목표 나이에 닿아요.</p>
        </div>
      ) : (
        <div style={S.planBox}>
          <p style={S.planLead}>목표 {p.targetAge}세에 닿으려면 (연 {annualPct}% 가정)</p>
          <div style={S.planNums}>
            <div style={S.pnCell}><small style={S.pnSmall}>매달</small><b style={S.pnBig}>{won(p.pmt)}</b></div>
            <div style={S.pnCell}><small style={S.pnSmall}>하루</small><b style={S.pnBig}>{won(p.daily)}</b></div>
          </div>
          {p.shortfall > 0
            ? <p style={S.planSub}>지금 계획(월 {won(p.planMonthly)})보다 <b style={{ color: '#e8431c' }}>매달 {won(p.shortfall)}</b> 더 모으면 달성해요.</p>
            : <p style={{ ...S.planSub, color: '#0f6e56' }}>지금 계획(월 {won(p.planMonthly)})이면 충분해요 👏 더 빨리도 가능!</p>}
        </div>
      )}

      {!p.alreadyOnTrack && monthGoal > 0 && (
        <div style={S.month}>
          <div style={S.monthTop}>
            <span style={S.monthLabel}>이번 달 모은 돈</span>
            <span style={S.monthVal}><b>{won(monthSaved)}</b> / 목표 {won(monthGoal)}</span>
          </div>
          <div style={S.monthTrack}><div style={{ ...S.monthFill, width: `${Math.max(2, monthPct)}%` }} /></div>
        </div>
      )}

      <div style={S.cta}>
        <button type="button" style={S.ctaSave} onClick={() => onMove('save')}>오늘 저축하기</button>
        <button type="button" style={S.ctaView} onClick={() => onMove('result')}>📊 결과·또래 등수 보기</button>
      </div>
    </section>
  );
}

const S = {
  card: { borderColor: 'rgba(255,90,0,0.3)', boxShadow: '0 1px 2px rgba(20,18,15,.04), 0 18px 36px -20px rgba(255,90,0,.28)' },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  years: { fontSize: 12.5, fontWeight: 800, color: '#ff5a00' },
  progRow: { display: 'flex', alignItems: 'center', gap: 14, marginBottom: 13 },
  bigPct: { fontSize: 40, fontWeight: 800, color: '#ff5a00', letterSpacing: '-0.04em', lineHeight: 1, fontVariantNumeric: 'tabular-nums', flex: '0 0 auto' },
  bigPctU: { fontSize: 20, fontWeight: 800 },
  progMeta: { flex: 1, minWidth: 0 },
  progTrack: { height: 8, borderRadius: 9, background: '#f0ede9', overflow: 'hidden', marginBottom: 7 },
  progFill: { height: '100%', borderRadius: 9, background: 'linear-gradient(90deg,#FFB48F,#ff5a00)' },
  progTx: { fontSize: 12.5, color: '#565c68', fontWeight: 600, margin: 0 },
  ageRow: { display: 'flex', alignItems: 'center', background: '#f8f6f2', borderRadius: 12, padding: '11px 0', marginBottom: 13 },
  ageCell: { flex: 1, textAlign: 'center', display: 'flex', flexDirection: 'column', gap: 3 },
  ageSmall: { fontSize: 11, color: '#9aa3bf', fontWeight: 700 },
  ageBig: { fontSize: 18, color: '#15151b', fontWeight: 800, fontVariantNumeric: 'tabular-nums' },
  ageDiv: { width: 1, alignSelf: 'stretch', background: '#e7e3dd', margin: '2px 0' },
  planBox: { background: 'linear-gradient(180deg,#fff6f2,#fff)', border: '1px solid rgba(255,90,0,0.2)', borderRadius: 14, padding: '14px', marginBottom: 12 },
  planLead: { fontSize: 12, color: '#6b6f76', fontWeight: 700, margin: '0 0 9px' },
  planNums: { display: 'flex', gap: 10, marginBottom: 9 },
  pnCell: { flex: 1, background: '#fff', border: '1px solid #f0e7e1', borderRadius: 11, padding: '9px 12px', display: 'flex', flexDirection: 'column', gap: 3 },
  pnSmall: { fontSize: 11, color: '#9aa3bf', fontWeight: 700 },
  pnBig: { fontSize: 19, color: '#15151b', fontWeight: 800, letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums' },
  planMain: { fontSize: 14, fontWeight: 800, color: '#15151b', margin: '0 0 4px' },
  planSub: { fontSize: 12.5, color: '#565c68', fontWeight: 600, lineHeight: 1.55, margin: 0 },
  month: { marginBottom: 13 },
  monthTop: { display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 },
  monthLabel: { fontSize: 12, color: '#6b6f76', fontWeight: 700 },
  monthVal: { fontSize: 12.5, color: '#15151b', fontWeight: 700 },
  monthTrack: { height: 7, borderRadius: 9, background: '#f0ede9', overflow: 'hidden' },
  monthFill: { height: '100%', borderRadius: 9, background: 'linear-gradient(90deg,#7fd3b0,#10b981)' },
  cta: { display: 'flex', gap: 9 },
  ctaSave: { flex: 1, border: 0, cursor: 'pointer', background: 'linear-gradient(180deg,#ff6a35,#ee4a1f)', color: '#fff', borderRadius: 12, padding: '12px', fontSize: 14, fontWeight: 800, boxShadow: '0 10px 22px -10px rgba(232,67,28,0.5)' },
  ctaView: { flex: 1, border: 0, cursor: 'pointer', background: 'linear-gradient(180deg,#3a4cff,#2230cc)', color: '#fff', borderRadius: 12, padding: '12px', fontSize: 14, fontWeight: 800, boxShadow: '0 10px 22px -10px rgba(34,48,204,0.5)' }
};
