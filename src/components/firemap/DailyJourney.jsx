import { useState } from 'react';
import { todayTip, todayAction, getCheckin, checkInToday } from '../../firemap-v2/journeyDaily.js';
import { todayStr, track } from '../../firemap-v2/dailyData.js';
import { journeyStage } from '../../utils/journeyStage.js';

// 오늘의 파이어 — 매일 새 지식 + 오늘의 한 걸음 + 연속 출석. 매일 열 이유.
export default function DailyJourney({ onMove, simulation }) {
  const stage = (() => { try { return simulation ? journeyStage(simulation).stage : null; } catch { return null; } })();
  const [ck, setCk] = useState(getCheckin);
  const done = ck.last === todayStr();
  const tip = todayTip(stage);
  const act = todayAction(stage);
  const doToday = () => {
    const nc = checkInToday();
    setCk(nc);
    try { track('daily_step', { to: act.to, streak: nc.count }); } catch { /* ignore */ }
    onMove(act.to);
  };
  return (
    <section className="fm-card" style={S.card}>
      <div style={S.head}>
        <span style={S.title}>☀️ 오늘의 파이어</span>
        <span style={S.streak}>🔥 {ck.count || 0}일 연속</span>
      </div>
      <div style={S.tipBox}>
        <span style={S.tipK}>오늘의 파이어 지식</span>
        <p style={S.tip}>{tip}</p>
      </div>
      <button type="button" style={S.act} onClick={doToday}>
        <span style={S.actTx}>
          <span style={S.actCap}>{done ? '오늘 한 걸음 완료 ✓ · 하나 더?' : '오늘의 한 걸음'}</span>
          <span style={S.actMain}>{act.ico} {act.label}</span>
        </span>
        <span style={S.actArrow}>→</span>
      </button>
    </section>
  );
}

const S = {
  card: { borderColor: 'rgba(255,90,0,0.3)', boxShadow: '0 1px 2px rgba(20,18,15,.04), 0 18px 36px -20px rgba(255,90,0,.28)' },
  head: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 },
  title: { fontSize: 14, fontWeight: 800, color: '#15151b', letterSpacing: '-0.01em' },
  streak: { fontSize: 12.5, fontWeight: 800, color: '#e8431c', background: '#fff0ea', borderRadius: 999, padding: '5px 11px' },
  tipBox: { background: '#f8f6f2', border: '1px solid #efece7', borderRadius: 13, padding: '13px 14px', marginBottom: 12 },
  tipK: { fontSize: 11, fontWeight: 800, color: '#9aa3bf', letterSpacing: '0.02em' },
  tip: { fontSize: 13.5, color: '#15151b', fontWeight: 600, lineHeight: 1.6, margin: '6px 0 0' },
  act: { width: '100%', border: 0, cursor: 'pointer', textAlign: 'left', background: 'linear-gradient(180deg,#ff6a35,#ee4a1f)', color: '#fff', borderRadius: 14, padding: '13px 15px', display: 'flex', alignItems: 'center', boxShadow: '0 12px 24px -10px rgba(232,67,28,0.55)' },
  actTx: { display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 },
  actCap: { fontSize: 10.5, fontWeight: 700, opacity: 0.85, letterSpacing: '0.02em' },
  actMain: { fontSize: 14.5, fontWeight: 800, marginTop: 2 },
  actArrow: { fontSize: 18, fontWeight: 800, marginLeft: 10, flex: '0 0 auto' }
};
