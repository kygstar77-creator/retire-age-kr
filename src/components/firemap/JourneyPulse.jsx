import { useMemo, useState } from 'react';
import { journeyStage } from '../../utils/journeyStage.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { pickForToday } from '../../firemap-v2/journeyPlaybook.js';
import { track } from '../../firemap-v2/dailyData.js';
import WeeklyBoard from './WeeklyBoard.jsx';

// 여정 펄스 — 단계×주기 콘텐츠 허브. 오늘의 한 걸음(단계 반영)·이번 주 미션/추천글·
// 월간 점검·연간 회고를 한 카드에. 추천글은 실제 대량 콘텐츠(/guide)로 연결.
const seenKey = (k) => { try { return localStorage.getItem(k) === '1'; } catch { return false; } };
const markSeen = (k) => { try { localStorage.setItem(k, '1'); } catch { /* ignore */ } };
const monthKey = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`; };
const yearKey = () => new Date().getFullYear();

export default function JourneyPulse({ simulation, onMove }) {
  const j = useMemo(() => {
    let adv = 0; try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
    let h = 0; try { h = getAssetHistory().length; } catch { /* ignore */ }
    return journeyStage(simulation, { advanceDays: adv, assetHistoryLen: h });
  }, [simulation]);
  const stage = j.stage;
  const pb = useMemo(() => pickForToday(stage), [stage]);
  const mKey = `fm_pulse_m_${stage}_${monthKey()}`;
  const yKey = `fm_pulse_y_${stage}_${yearKey()}`;
  const [showM, setShowM] = useState(() => !seenKey(mKey));
  const [showY, setShowY] = useState(() => !seenKey(yKey));

  if (!j.earliest) return null; // 계산 전엔 JourneyMap이 각성 단계를 안내하므로 숨김

  const openHref = (href) => { try { window.open(href, '_blank', 'noopener'); } catch { window.location.href = href; } };
  const goAction = (a) => { if (!a) return; try { track('pulse_daily', { stage, to: a.to || a.href }); } catch { /* ignore */ } if (a.href) openHref(a.href); else onMove(a.to); };
  const openRead = (r) => { try { track('pulse_read', { stage, href: r.href }); } catch { /* ignore */ } if (String(r.href).startsWith('/guide')) openHref(r.href); else onMove(r.href); };
  const dismissM = () => { markSeen(mKey); setShowM(false); };
  const dismissY = () => { markSeen(yKey); setShowY(false); };

  const act = pb.action;
  const wk = pb.weekly;

  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.kicker}>🧭 {j.current.emoji} {j.current.name} 단계 플랜</span>
        <button type="button" style={S.allBtn} onClick={() => { try { track('pulse_open_journey', {}); } catch { /* ignore */ } onMove('journey'); }}>단계 전체 ›</button>
      </div>

      {act && (
        <button type="button" style={S.daily} onClick={() => goAction(act)}>
          <span style={S.dTx}><span style={S.dCap}>오늘의 한 걸음</span><span style={S.dMain}>{act.ico} {act.label}</span></span>
          <span style={S.dArrow}>→</span>
        </button>
      )}
      {pb.tip && <p style={S.tip}>💡 {pb.tip}</p>}

      {wk && (
        <div style={S.block}>
          <p style={S.blockCap}>📌 이번 주 미션</p>
          <button type="button" style={S.mission} onClick={() => goAction(wk.mission)}>
            <span>{wk.mission.ico} {wk.mission.label}</span><span style={S.mArrow}>→</span>
          </button>
          {wk.reads && wk.reads.length > 0 && (
            <>
              <p style={S.readsCap}>이번 주 추천 읽을거리</p>
              <div style={S.reads}>
                {wk.reads.map((r) => (
                  <button type="button" key={r.href + r.title} style={S.read} onClick={() => openRead(r)}>
                    <span style={S.readT}>📖 {r.title}</span><span style={S.readArrow}>›</span>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      <div style={S.block}>
        <p style={S.blockCap}>🏅 이번 주 절약왕</p>
        <WeeklyBoard />
      </div>

      {showM && pb.monthly && (
        <div style={S.review}>
          <div style={S.reviewTop}><span style={S.reviewTitle}>🗓️ {pb.monthly.title}</span><button type="button" style={S.reviewX} onClick={dismissM} aria-label="이번 달 점검 닫기">✕</button></div>
          <ul style={S.ul}>{pb.monthly.items.map((it, i) => <li key={i} style={S.li}>{it}</li>)}</ul>
          {pb.monthly.to && <button type="button" style={S.reviewGo} onClick={() => { try { track('pulse_monthly', { stage, to: pb.monthly.to }); } catch { /* ignore */ } onMove(pb.monthly.to); }}>지금 점검하러 가기 →</button>}
        </div>
      )}

      {showY && pb.yearly && (
        <div style={{ ...S.review, ...S.reviewYear }}>
          <div style={S.reviewTop}><span style={S.reviewTitle}>📅 {pb.yearly.title}</span><button type="button" style={S.reviewX} onClick={dismissY} aria-label="연간 회고 닫기">✕</button></div>
          <ul style={S.ul}>{pb.yearly.items.map((it, i) => <li key={i} style={S.li}>{it}</li>)}</ul>
          {pb.yearly.to && <button type="button" style={S.reviewGo} onClick={() => { try { track('pulse_yearly', { stage, to: pb.yearly.to }); } catch { /* ignore */ } onMove(pb.yearly.to); }}>돌아보러 가기 →</button>}
        </div>
      )}
    </section>
  );
}

const S = {
  card: { borderColor: 'rgba(30,40,89,0.18)', boxShadow: '0 1px 2px rgba(20,18,15,.04), 0 16px 32px -22px rgba(30,40,89,.25)' },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 },
  kicker: { fontSize: 13, fontWeight: 800, color: '#1e2859', letterSpacing: '-0.01em' },
  allBtn: { border: 0, background: 'none', color: '#1e2859', fontSize: 12, fontWeight: 700, cursor: 'pointer' },
  daily: { width: '100%', border: 0, cursor: 'pointer', textAlign: 'left', background: 'linear-gradient(180deg,#ff6a35,#ee4a1f)', color: '#fff', borderRadius: 14, padding: '13px 15px', display: 'flex', alignItems: 'center', boxShadow: '0 12px 24px -10px rgba(232,67,28,0.5)' },
  dTx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 },
  dCap: { fontSize: 10.5, fontWeight: 700, opacity: 0.85, letterSpacing: '0.02em' },
  dMain: { fontSize: 14.5, fontWeight: 800, marginTop: 2 },
  dArrow: { fontSize: 18, fontWeight: 800, marginLeft: 10, flex: '0 0 auto' },
  tip: { fontSize: 12.5, color: '#565c68', lineHeight: 1.6, margin: '10px 2px 0', fontWeight: 500 },
  block: { marginTop: 14 },
  blockCap: { fontSize: 12, fontWeight: 800, color: '#1e2859', margin: '0 0 8px 2px' },
  mission: { width: '100%', border: '1px solid #ffd9c7', background: '#fff7f2', borderRadius: 12, padding: '11px 13px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: 13.5, fontWeight: 700, color: '#9a3a12' },
  mArrow: { fontWeight: 800, marginLeft: 8 },
  readsCap: { fontSize: 11, fontWeight: 700, color: '#9aa3bf', margin: '10px 2px 6px' },
  reads: { display: 'flex', flexDirection: 'column', gap: 7 },
  read: { width: '100%', textAlign: 'left', display: 'flex', alignItems: 'center', gap: 8, background: '#f8f6f2', border: '1px solid #efece7', borderRadius: 11, padding: '10px 12px', cursor: 'pointer' },
  readT: { flex: 1, fontSize: 12.5, color: '#15151b', fontWeight: 700 },
  readArrow: { color: '#ff5a00', fontWeight: 800, fontSize: 15 },
  review: { marginTop: 14, background: '#f6f7fb', border: '1px solid #e7ebf3', borderRadius: 13, padding: '12px 13px' },
  reviewYear: { background: '#fffdf3', borderColor: '#ffe6a6' },
  reviewTop: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 },
  reviewTitle: { fontSize: 12.5, fontWeight: 800, color: '#1e2859' },
  reviewX: { border: 0, background: 'none', color: '#9aa3bf', fontSize: 13, fontWeight: 800, cursor: 'pointer', lineHeight: 1 },
  ul: { listStyle: 'disc', margin: '0 0 10px', padding: '0 0 0 18px', display: 'flex', flexDirection: 'column', gap: 6 },
  li: { fontSize: 12.5, color: '#3a3f4a', fontWeight: 500, lineHeight: 1.5 },
  reviewGo: { width: '100%', border: 0, background: '#1e2859', color: '#fff', borderRadius: 10, padding: '9px', fontSize: 12.5, fontWeight: 700, cursor: 'pointer' }
};
