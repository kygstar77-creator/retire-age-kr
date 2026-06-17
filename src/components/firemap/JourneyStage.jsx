import { useEffect, useMemo, useState } from 'react';
import Header from './Header.jsx';
import { journeyStage } from '../../utils/journeyStage.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { track } from '../../firemap-v2/dailyData.js';

const INTRO = {
  1: '내 파이어 나이를 알게 된 단계예요. 결과와 또래 위치를 확인하고 내 기록을 지켜요.',
  2: '목표와 전략을 정하는 단계예요. 어떻게 도달할지 길을 그려요.',
  3: '추적을 시작하는 단계예요. 기록이 쌓이면 파이어가 움직여요.',
  4: '진짜 전진하는 단계예요. 가장 큰 레버로 파이어를 당겨요.',
  5: '거의 다 온 단계예요. 건보·세금·인출을 점검해 검증해요.',
  6: '파이어 단계예요. 지속 가능한 인출과 커뮤니티로 함께해요.'
};

function tasksFor(n, s) {
  const M = (label, done, to) => ({ label, done: !!done, to });
  if (n === 1) return [M('파이어 나이 계산 완료', s.calculated && s.earliest, null), M('결과·또래 등수 자세히 보기', false, 'result'), M('내 프로필 만들기(기록 저장)', false, 'account')];
  if (n === 2) return [M('목표 파이어 나이 정하기', s.targetAge > 0, 'experiment'), M('월 저축 계획 세우기', s.monthlyInvestment > 0, 'experiment'), M('바꿔보기로 목표 달성 경로 찾기', false, 'experiment'), M('지역·세금·연금 조건 점검', false, 'tools')];
  if (n === 3) return [M('이번 달 자산 기록하기', s.histLen >= 1, 'home'), M('오늘 절약·적립 기록하기', s.saveTotal > 0 || s.dailyN > 0, 'save'), M('파이어 시계 알림 켜기', s.notif, 'home')];
  if (n === 4) return [M('1억 돌파', s.asset >= 100000000, null), M('또래 평균 추월', s.peerAvg && s.earliest && s.earliest < s.peerAvg, 'index'), M('지역·부업·세금으로 더 당기기', false, 'tools'), M('3억 돌파', s.asset >= 300000000, null)];
  if (n === 5) return [M('파이어 후 건보료 점검', false, 'dependent'), M('양도·배당세 점검', false, 'foreignTax'), M('현금흐름·인출 계획', false, 'dividend')];
  return [M('인출 전략 점검', false, 'dividend'), M('파이어족 커뮤니티 합류', false, 'community')];
}

export default function JourneyStage({ simulation, onMove, onBack }) {
  const [peerAvg, setPeerAvg] = useState(null);
  useEffect(() => { let a = true; fetchAggregates().then((x) => { if (a && x && x.avgEarliest) setPeerAvg(x.avgEarliest); }).catch(() => {}); return () => { a = false; }; }, []);
  const j = useMemo(() => {
    let adv = 0; try { adv = Math.max(0, computeProgress(simulation).advanceDays || 0); } catch { /* ignore */ }
    let h = 0; try { h = getAssetHistory().length; } catch { /* ignore */ }
    return journeyStage(simulation, { advanceDays: adv, peerAvg, assetHistoryLen: h });
  }, [simulation, peerAvg]);
  const [open, setOpen] = useState(j.stage);
  const s = j.signals || {};
  const doneCount = (n) => { const ts = tasksFor(n, s); return ts.filter((t) => t.done).length + '/' + ts.length; };

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="내 파이어 여정" onBack={onBack} />
      <section className="fm-card" style={H.intro}>
        <span style={H.k}>{j.current.emoji} {j.stage}/6단계 · {j.current.name}</span>
        <p style={H.t}>{INTRO[j.stage]}</p>
      </section>
      {j.stages.map((st) => {
        const done = st.n < j.stage, cur = st.n === j.stage, locked = st.n > j.stage;
        const isOpen = open === st.n;
        const tasks = tasksFor(st.n, s);
        return (
          <section className="fm-card" key={st.key} style={{ ...H.card, ...(cur ? H.cardCur : null) }}>
            <button type="button" style={H.row} onClick={() => setOpen(isOpen ? 0 : st.n)}>
              <span style={{ ...H.badge, ...(done ? H.bDone : cur ? H.bCur : H.bLock) }}>{done ? '✓' : locked ? '🔒' : st.emoji}</span>
              <span style={H.rowtx}><b style={{ color: locked ? '#9aa3bf' : '#15151b' }}>{st.n}. {st.name}</b><em>{st.tag} · 할 일 {doneCount(st.n)}</em></span>
              <span style={H.chev}>{isOpen ? '▴' : '▾'}</span>
            </button>
            {isOpen && (
              <div style={H.body}>
                <p style={H.bodyIntro}>{INTRO[st.n]}</p>
                <ul style={H.ul}>
                  {tasks.map((tk, i) => (
                    <li key={i} style={H.li}>
                      <span style={{ ...H.cb, ...(tk.done ? H.cbDone : null) }}>{tk.done ? '✓' : ''}</span>
                      <span style={{ ...H.litx, ...(tk.done ? H.litxDone : null) }}>{tk.label}</span>
                      {!tk.done && tk.to && <button type="button" style={H.do} onClick={() => { try { track('journey_task', { stage: st.n, to: tk.to }); } catch { /* ignore */ } onMove(tk.to); }}>하기 →</button>}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        );
      })}
      <p style={H.foot}>각 단계의 할 일을 끝내면 다음 단계로 나아가요. 파이어까지 함께합니다.</p>
    </main>
  );
}

const H = {
  intro: { borderColor: 'rgba(255,90,0,0.3)', background: 'radial-gradient(120% 90% at 100% 0%, rgba(255,90,0,0.06), transparent 50%), #fff' },
  k: { display: 'inline-block', fontSize: 12, fontWeight: 800, color: '#e8431c', background: '#fff0ea', padding: '5px 11px', borderRadius: 999 },
  t: { fontSize: 13.5, color: '#15151b', fontWeight: 600, lineHeight: 1.55, margin: '12px 0 0' },
  card: { padding: 0, overflow: 'hidden' },
  cardCur: { borderColor: 'rgba(255,90,0,0.4)', boxShadow: '0 1px 2px rgba(20,18,15,.04), 0 16px 32px -20px rgba(255,90,0,.3)' },
  row: { width: '100%', border: 0, background: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 12, padding: '16px 16px' },
  badge: { width: 34, height: 34, borderRadius: 11, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 15, flex: '0 0 auto' },
  bDone: { background: '#ff5a00', color: '#fff' },
  bCur: { background: '#fff0ea', boxShadow: '0 0 0 2px #ff5a00 inset' },
  bLock: { background: '#f1f0ee', color: '#b7b2a8' },
  rowtx: { flex: 1, textAlign: 'left', display: 'flex', flexDirection: 'column', gap: 2 },
  chev: { color: '#9aa3bf', fontSize: 13, flex: '0 0 auto' },
  body: { padding: '0 16px 16px' },
  bodyIntro: { fontSize: 12.5, color: '#6b6f76', lineHeight: 1.55, margin: '0 0 12px' },
  ul: { listStyle: 'none', margin: 0, padding: 0 },
  li: { display: 'flex', alignItems: 'center', gap: 10, padding: '10px 0', borderTop: '1px solid #f2f0ec' },
  cb: { width: 20, height: 20, borderRadius: 6, border: '2px solid #d7dae0', flex: '0 0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 12, fontWeight: 800 },
  cbDone: { background: '#ff5a00', borderColor: '#ff5a00' },
  litx: { flex: 1, fontSize: 13.5, color: '#15151b', fontWeight: 600 },
  litxDone: { color: '#9aa3bf', textDecoration: 'line-through' },
  do: { flex: '0 0 auto', fontSize: 12, fontWeight: 800, color: '#fff', background: 'linear-gradient(180deg,#ff6a35,#ee4a1f)', border: 0, borderRadius: 9, padding: '7px 12px', cursor: 'pointer' },
  foot: { fontSize: 11.5, color: '#9aa3bf', lineHeight: 1.6, textAlign: 'center', padding: '6px 18px 0' }
};
