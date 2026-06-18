import { useEffect, useMemo, useState } from 'react';
import Header from './Header.jsx';
import { journeyStage } from '../../utils/journeyStage.js';
import { computeProgress } from '../../utils/savingsEngine.js';
import { getAssetHistory } from '../../utils/assetHistory.js';
import { fetchAggregates } from '../../utils/firemapScoresApi.js';
import { track } from '../../firemap-v2/dailyData.js';

const GUIDE = {
  1: '내 파이어 나이를 알았다면, 이제 ‘파이어’가 한 종류가 아니라는 걸 알 차례예요. 완전 은퇴(린·팻)부터 코스트·바리스타·반퇴까지 — 내게 맞는 유형을 정하면 목표가 또렷해져요. 결과와 또래 위치를 먼저 확인하고, 기록이 사라지지 않게 프로필을 만들어두세요.',
  2: '목표를 정하는 단계예요. 목표 자산은 얼마인지, 코스트파이어(더 안 모아도 굴러가는 시점)는 언제인지, ISA·연금계좌로 세금을 줄이며 모으는 법까지 — 도달 경로를 그려요. ‘바꿔보기’로 저축·생활비·근무 레버를 돌려 내 목표 나이를 맞춰보세요.',
  3: '가장 긴 구간이에요. 핵심은 ‘저축률’. 고정비부터 구조적으로 줄이고, 매달 자산을 기록해 진도를 눈으로 보세요. 작은 저축도 파이어를 며칠씩 당깁니다 — 기록이 쌓이면 숫자가 살아 움직여요.',
  4: '모으는 속도를 끜어올리는 단계예요. 지방·동남아 이주로 생활비를 낮추거나, 부업·배당으로 현금흐름을 더하면 파이어가 몇 년씩 당겨져요. 세금(양도·배당)도 최적화 포인트예요.',
  5: '돈은 거의 모였어요. 이제 ‘진짜 되는지’ 검증할 때. 퇴사하면 건강보험이 지역가입자로 바뀌고, 연금 받기 전까지 소득 공백(크레바스)이 생기고, 자산을 어떤 순서로 인출하느냐로 세금이 달라져요. 이걸 점검해야 안전한 파이어예요.',
  6: '축하해요. 이제 ‘돈이 안 떨어지게’ 지키는 단계. 인출 순서 전략으로 세금을 아끼고, 같은 길을 걷는 파이어족과 이야기 나누며 길게 함껴해요.'
};

const READS = {
  1: [['파이어 종류 — 린·팻·코스트·바리스타', 'fire-types'], ['나이별 파이어 전략', 'fire-by-age'], ['4% 룰이란?', 'four-percent-rule'], ['물가와 은퇴 자금', 'inflation-retirement']],
  2: [['목표 자산 시나리오', 'asset-target-scenarios'], ['코스트파이어 계산', 'coast-fire-calculation'], ['ISA·연금계좌 절세', 'isa-pension-accounts'], ['반퇴(세미리타이어)', 'semi-retirement']],
  3: [['생활비 구조적으로 줄이기', 'cut-living-cost'], ['알뜰한 식비 절약법', 'frugal-food-tips'], ['배당으로 월 현금흐름', 'dividend-monthly-income']],
  4: [['지방·주택 다운사이징', 'real-estate-downsizing'], ['동남아 은퇴', 'southeast-asia-retirement'], ['파이어 후 부업', 'post-retirement-side-jobs'], ['디지털노마드 소득', 'digital-nomad-income']],
  5: [['파이어 후 건보료·피부양자', 'health-insurance-dependent'], ['소득 크레바스(연금 공백)', 'income-crevasse'], ['국민연금 조기수령', 'national-pension-early'], ['인출 순서 전략', 'withdrawal-order-strategy'], ['해외주식 양도세', 'foreign-stock-tax'], ['퇴직금·IRP 세금', 'severance-irp-tax']],
  6: [['인출 순서 전략', 'withdrawal-order-strategy'], ['배당과 건강보험료', 'dividend-health-insurance'], ['배당 소득세 기준', 'dividend-tax-thresholds']]
};

function tasksFor(n, s) {
  const M = (label, done, to) => ({ label, done: !!done, to });
  if (n === 1) return [M('파이어 나이 계산 완료', s.calculated && s.earliest, null), M('결과·또래 등수 자세히 보기', false, 'result'), M('내 프로필 만들기(기록 저장)', false, 'account')];
  if (n === 2) return [M('목표 파이어 나이 정하기', s.targetAge > 0, 'experiment'), M('월 저축 계획 세우기', s.monthlyInvestment > 0, 'experiment'), M('바꿔보기로 목표 달성 경로 찾기', false, 'experiment'), M('지역·세금·연금 조건 점검', false, 'tools')];
  if (n === 3) return [M('이번 달 자산 기록하기', s.histLen >= 1, 'home'), M('오늘 저축 기록하기', s.saveTotal > 0 || s.dailyN > 0, 'save'), M('파이어 시계 알림 켜기', s.notif, 'home')];
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
  const overall = (() => { let d = 0, t = 0; for (let n = 1; n <= 6; n++) { const ts = tasksFor(n, s); d += ts.filter((x) => x.done).length; t += ts.length; } return { d, t, pct: t ? Math.round((d / t) * 100) : 0 }; })();
  const readGuide = (slug) => { try { track('journey_read', { slug }); } catch { /* ignore */ } try { window.open('/guide/' + slug + '.html', '_blank', 'noopener'); } catch { window.location.href = '/guide/' + slug + '.html'; } };

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="내 파이어 여정" onBack={onBack} />
      <section className="fm-card" style={H.intro}>
        <span style={H.k}>{j.current.emoji} {j.stage}/6단계 · {j.current.name}</span>
        <p style={H.t}>{GUIDE[j.stage]}</p>
        <div style={H.introBarTop}><span>여정 진행률</span><b>{overall.pct}% · 할 일 {overall.d}/{overall.t}</b></div>
        <div style={H.introBar}><div style={{ ...H.introFill, width: `${Math.max(2, overall.pct)}%` }} /></div>
      </section>
      {j.stages.map((st) => {
        const done = st.n < j.stage, cur = st.n === j.stage, locked = st.n > j.stage;
        const isOpen = open === st.n;
        const tasks = tasksFor(st.n, s);
        const td = tasks.filter((t) => t.done).length;
        const tt = tasks.length;
        const tpct = tt ? Math.round((td / tt) * 100) : 0;
        const allDone = tt > 0 && td === tt;
        const reads = READS[st.n] || [];
        return (
          <section className="fm-card" key={st.key} style={{ ...H.card, ...(cur ? H.cardCur : null) }}>
            <button type="button" style={H.row} onClick={() => setOpen(isOpen ? 0 : st.n)}>
              <span style={{ ...H.badge, ...(done ? H.bDone : cur ? H.bCur : H.bLock) }}>{done ? '✓' : locked ? '🔒' : st.emoji}</span>
              <span style={H.rowtx}>
                <b style={{ color: locked ? '#9aa3bf' : '#15151b' }}>{st.n}. {st.name}</b>
                <span style={H.rowsub}>{st.tag} · 할 일 {td}/{tt}{allDone ? ' · 완료 🎉' : ''}</span>
                {!locked && <span style={H.miniBar}><span style={{ ...H.miniFill, width: `${Math.max(3, tpct)}%`, background: allDone ? '#10b981' : (cur ? '#ff5a00' : '#c2c7d0') }} /></span>}
              </span>
              <span style={H.chev}>{isOpen ? '▴' : '▾'}</span>
            </button>
            {isOpen && (
              <div style={H.body}>
                <p style={H.bodyIntro}>{GUIDE[st.n]}</p>

                <p style={H.subh}>✓ 지금 할 일 ({td}/{tt})</p>
                <ul style={H.ul}>
                  {tasks.map((tk, i) => (
                    <li key={i} style={H.li}>
                      <span style={{ ...H.cb, ...(tk.done ? H.cbDone : null) }}>{tk.done ? '✓' : ''}</span>
                      <span style={{ ...H.litx, ...(tk.done ? H.litxDone : null) }}>{tk.label}</span>
                      {!tk.done && tk.to && <button type="button" style={H.do} onClick={() => { try { track('journey_task', { stage: st.n, to: tk.to }); } catch { /* ignore */ } onMove(tk.to); }}>하기 →</button>}
                    </li>
                  ))}
                </ul>

                {reads.length > 0 && (
                  <>
                    <p style={H.subh}>📖 이 단계에서 꼭 읽어볼 글</p>
                    <div style={H.reads}>
                      {reads.map(([title, slug]) => (
                        <button type="button" key={slug + title} style={H.read} onClick={() => readGuide(slug)}>
                          <span style={H.readT}>{title}</span><span style={H.readArrow}>›</span>
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>
            )}
          </section>
        );
      })}
      <p style={H.foot}>각 단계의 할 일과 읽을 거리를 끝내면 다음 단계로 나아가요. 파이어가 몇 년 남았든, 여기서 함께합니다.</p>
    </main>
  );
}

const H = {
  intro: { borderColor: 'rgba(255,90,0,0.3)', background: 'radial-gradient(120% 90% at 100% 0%, rgba(255,90,0,0.06), transparent 50%), #fff' },
  k: { display: 'inline-block', fontSize: 12, fontWeight: 800, color: '#e8431c', background: '#fff0ea', padding: '5px 11px', borderRadius: 999 },
  t: { fontSize: 13.5, color: '#15151b', fontWeight: 500, lineHeight: 1.65, margin: '12px 0 0' },
  introBarTop: { display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', fontSize: 11.5, fontWeight: 700, color: '#6b6f76', margin: '14px 0 6px' },
  introBar: { height: 8, borderRadius: 9, background: '#f0ede9', overflow: 'hidden' },
  introFill: { height: '100%', borderRadius: 9, background: 'linear-gradient(90deg,#FFB48F,#ff5a00)' },
  miniBar: { display: 'block', height: 5, borderRadius: 6, background: '#f0ede9', overflow: 'hidden', marginTop: 6 },
  miniFill: { display: 'block', height: '100%', borderRadius: 6 },
  card: { padding: 0, overflow: 'hidden' },
  cardCur: { borderColor: 'rgba(255,90,0,0.4)', boxShadow: '0 1px 2px rgba(20,18,15,.04), 0 16px 32px -20px rgba(255,90,0,.3)' },
  row: { width: '100%', border: 0, background: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 12, padding: '16px 16px' },
  badge: { width: 34, height: 34, borderRadius: 11, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 15, flex: '0 0 auto' },
  bDone: { background: '#ff5a00', color: '#fff' },
  bCur: { background: '#fff0ea', boxShadow: '0 0 0 2px #ff5a00 inset' },
  bLock: { background: '#f1f0ee', color: '#b7b2a8' },
  rowtx: { flex: 1, textAlign: 'left', display: 'flex', flexDirection: 'column', gap: 3 },
  rowsub: { fontSize: 11.5, color: '#9aa3bf', fontWeight: 600, fontStyle: 'normal' },
  chev: { color: '#9aa3bf', fontSize: 13, flex: '0 0 auto' },
  body: { padding: '0 16px 16px' },
  bodyIntro: { fontSize: 13, color: '#565c68', lineHeight: 1.65, margin: '0 0 14px' },
  subh: { fontSize: 12, fontWeight: 800, color: '#1e2859', margin: '0 0 8px' },
  ul: { listStyle: 'none', margin: '0 0 16px', padding: 0 },
  li: { display: 'flex', alignItems: 'center', gap: 10, padding: '9px 0', borderTop: '1px solid #f2f0ec' },
  cb: { width: 20, height: 20, borderRadius: 6, border: '2px solid #d7dae0', flex: '0 0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 12, fontWeight: 800 },
  cbDone: { background: '#ff5a00', borderColor: '#ff5a00' },
  litx: { flex: 1, fontSize: 13.5, color: '#15151b', fontWeight: 600 },
  litxDone: { color: '#9aa3bf', textDecoration: 'line-through' },
  do: { flex: '0 0 auto', fontSize: 12, fontWeight: 800, color: '#fff', background: 'linear-gradient(180deg,#ff6a35,#ee4a1f)', border: 0, borderRadius: 9, padding: '7px 12px', cursor: 'pointer' },
  reads: { display: 'flex', flexDirection: 'column', gap: 8 },
  read: { width: '100%', textAlign: 'left', display: 'flex', alignItems: 'center', gap: 8, background: '#f8f6f2', border: '1px solid #efece7', borderRadius: 11, padding: '11px 13px', cursor: 'pointer' },
  readT: { flex: 1, fontSize: 13, color: '#15151b', fontWeight: 700 },
  readArrow: { color: '#ff5a00', fontWeight: 800, fontSize: 15 },
  foot: { fontSize: 11.5, color: '#9aa3bf', lineHeight: 1.6, textAlign: 'center', padding: '6px 18px 0' }
};
