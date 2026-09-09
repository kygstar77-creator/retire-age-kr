// 결과 — 숫자 1(파이어 나이) + 필요 자산 + 레버 3 + 인증 카드. 세그먼트: 몇 살에? | N억이면?(역산).
// 18블록·12~20버튼·팝업 2 → 6블록·버튼 ≤ 10·팝업 0. 근거: 최종본 §3-2, 4차 '얼마' 1위, ChooseFI 레버 3, TDS Result.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, StatHero, Card, SectionHead, Button, LeverList, Fold, Tabs, RangeField, Stat, toast } from '../../ui/index.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, buildGrowthSeries, scenarioEndAge, survivalPhrase, runwayText } from '../../firemap-v2/scenarios.js';
import { simulateRetirement, inputsIsReal, monteCarloSuccess, findEarliestRetirementAge } from '../../utils/retirementSimulator.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { statsTopPercentile } from '../../firemap-v2/stats.js';
import { submitScoreFromSim, fetchUserRank, fetchAggregates, assetBandOf, ASSET_BAND_LABELS } from '../../utils/firemapScoresApi.js';
import { saveRankSnapshot } from '../../firemap-v2/rankHistory.js';
import { FIRE_CITIES } from '../../firemap-v2/cities.js';
import { track } from '../../firemap-v2/dailyData.js';
import { estimateLocalPremium } from '../../firemap-v2/healthInsurance.js';
import { syncWidgetSnapshot } from '../../utils/widgetState.js';
import ConsentSheet from './Consent.jsx';
import ShareSheet from './ShareSheet.jsx';

const eok = (n) => formatWon(Math.round(n || 0));

function solveMin(test, hi, round) {
  if (test(0)) return 0;
  if (!test(hi)) return null;
  let lo = 0, h = hi;
  for (let i = 0; i < 18; i += 1) { const m = (lo + h) / 2; if (test(m)) h = m; else lo = m; }
  return Math.ceil(h / round) * round;
}

// 레버 3 — 목표 미달이면 '목표 달성', 달성 중이면 '1년 더 당기기'
function useLevers(simulation, onChange) {
  return useMemo(() => {
    const ni = simulation.inputs;
    const until = ni.simulationUntilAge;
    const earliest = simulation.earliestRetirementAge;
    const baseOk = !simulateRetirement(ni).depletionAge;
    const goal = baseOk && earliest ? Math.max(ni.currentAge, earliest - 1) : null;
    const ok = baseOk
      ? (patch) => { const e = findEarliestRetirementAge({ ...ni, ...patch }); return e != null && e <= goal; }
      : (patch) => !simulateRetirement({ ...ni, ...patch }).depletionAge;
    const lc = ni.monthlyLivingCost || 0;
    const defs = [
      { key: 'save', tag: '저축', solve: solveMin((d) => ok({ monthlyInvestment: ni.monthlyInvestment + d }), 20000000, 100000), label: (d) => `월 ${formatWon(d)} 더 저축`, patch: (d) => ({ monthlyInvestment: ni.monthlyInvestment + d }) },
      { key: 'cost', tag: '생활비', solve: solveMin((d) => ok({ monthlyLivingCost: Math.max(800000, lc - d) }), Math.max(0, lc - 800000), 100000), label: (d) => `파이어 후 생활비 월 ${formatWon(d)} 줄이기`, patch: (d) => ({ monthlyLivingCost: Math.max(800000, lc - d) }) },
      { key: 'side', tag: '부업', solve: solveMin((d) => ok({ partTimeIncomeAfterRetirement: ni.partTimeIncomeAfterRetirement + d }), 6000000, 100000), label: (d) => `파이어 후 월 ${formatWon(d)} 벌기`, patch: (d) => ({ partTimeIncomeAfterRetirement: ni.partTimeIncomeAfterRetirement + d }) }
    ];
    const items = defs.map((it) => ({
      key: it.key, tag: it.tag,
      off: it.solve === null || it.solve === 0,
      label: it.solve === null ? '이 방법만으론 어려워요' : it.solve === 0 ? '이미 충분해요' : it.label(it.solve),
      gain: it.solve ? (baseOk ? `−1년 → ${goal}세` : `${ni.targetRetirementAge}세 달성`) : null,
      onApply: it.solve ? () => { Object.entries(it.patch(it.solve)).forEach(([k, v]) => onChange(k, v)); try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch { /* ignore */ } toast.good('적용했어요. 위 숫자가 바뀌었어요'); } : null
    }));
    return { items, baseOk, goal, until };
  }, [simulation, onChange]);
}

function YearlyAssetChart({ simulation }) {
  const rows = simulation.targetResult.rows || [];
  const [sel, setSel] = useState(null);
  if (rows.length < 2) return null;
  const g = buildGrowthSeries(simulation);
  const pts = rows.map((r, i) => ({ age: r.age, status: r.status, principal: Math.max(0, g.principal[i] ?? 0), gains: Math.max(0, g.gains[i] ?? 0), v: Math.max(0, g.total[i] ?? r.financialAsset) }));
  const n = pts.length; const maxV = Math.max(...pts.map((p) => p.v), 1);
  const a0 = pts[0].age, a1 = pts[n - 1].age; const W = 320, H = 120, P = 8;
  const X = (a) => P + ((a - a0) / Math.max(1, a1 - a0)) * (W - 2 * P);
  const Y = (v) => H - P - (v / maxV) * (H - 2 * P);
  const principalTop = pts.map((p, i) => `${i ? 'L' : 'M'}${X(p.age).toFixed(1)} ${Y(p.principal).toFixed(1)}`).join(' ');
  const principalArea = `${principalTop} L${X(a1).toFixed(1)} ${(H - P).toFixed(1)} L${X(a0).toFixed(1)} ${(H - P).toFixed(1)} Z`;
  const totalTop = pts.map((p, i) => `${i ? 'L' : 'M'}${X(p.age).toFixed(1)} ${Y(p.v).toFixed(1)}`).join(' ');
  const principalBack = pts.slice().reverse().map((p) => `L${X(p.age).toFixed(1)} ${Y(p.principal).toFixed(1)}`).join(' ');
  const gainsArea = `${totalTop} ${principalBack} Z`;
  const ret = simulation.inputs.targetRetirementAge; const retX = X(Math.min(a1, Math.max(a0, ret)));
  const retIdx = Math.max(0, pts.findIndex((p) => p.age >= ret));
  const cur = sel != null ? pts[Math.min(sel, n - 1)] : (pts[retIdx] || pts[n - 1]);
  const pick = (e) => { const box = e.currentTarget.getBoundingClientRect(); const cx = e.touches && e.touches[0] ? e.touches[0].clientX : e.clientX; setSel(Math.max(0, Math.min(n - 1, Math.round(((cx - box.left) / box.width) * (n - 1))))); };
  return (
    <div className="fm-yac">
      <div className="fm-yac-read"><b>{cur.age}세</b><span className={cur.status === '파이어 후' ? 'after' : 'before'}>{cur.status}</span><strong>{formatWon(cur.v)}</strong></div>
      <p className="fm-yac-split"><i className="fm-dot fm-dot-principal" />넣은 돈 {formatWon(cur.principal)} · <i className="fm-dot fm-dot-gains" />불어난 돈 {formatWon(cur.gains)}</p>
      <div className="fm-yac-canvas" style={{ touchAction: 'none' }} onPointerDown={pick} onPointerMove={(e) => { if (e.buttons) pick(e); }} onTouchStart={pick} onTouchMove={pick}>
        <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" role="img" aria-label="나이별 자산 그래프">
          <path d={principalArea} className="fm-yac-area-principal" /><path d={gainsArea} className="fm-yac-area-gains" /><path d={totalTop} className="fm-yac-line" fill="none" />
          <line x1={retX} y1={P} x2={retX} y2={H - P} className="fm-yac-ret" /><line x1={X(cur.age)} y1={P} x2={X(cur.age)} y2={H - P} className="fm-yac-cross" /><circle cx={X(cur.age)} cy={Y(cur.v)} r="3.5" className="fm-yac-dot" />
        </svg>
      </div>
      <div className="fm-yac-x"><span>{a0}세</span><span>파이어 {ret}세</span><span>{a1}세</span></div>
    </div>
  );
}

function ReverseMode({ simulation, onOpenShare }) {
  const inp = simulation.inputs;
  const [asset, setAsset] = useState(() => Math.max(100000000, Math.round((inp.financialAsset || 0) / 100000000) * 100000000 || 300000000));
  const [debounced, setDebounced] = useState(asset);
  useEffect(() => { const t = setTimeout(() => setDebounced(asset), 150); return () => clearTimeout(t); }, [asset]);
  const age = useMemo(() => findEarliestRetirementAge({ ...inp, financialAsset: debounced }), [inp, debounced]);
  const need = Math.round(simulation.requiredFireAssetByFourPercent || 0);
  const gap = Math.max(0, need - debounced);
  const bands = useMemo(() => [300000000, 500000000, 1000000000, need].filter((v, i, a) => v > 0 && a.indexOf(v) === i).sort((a, b) => a - b).map((v) => ({ v, age: findEarliestRetirementAge({ ...inp, financialAsset: v }), pct: statsTopPercentile(v, inp.currentAge) })), [inp, need]);
  return (
    <>
      <StatHero tone="dark" label={`${eok(debounced)}이면`} value={age ? `${age}세` : '아직'} unit={age ? '' : ''} sub={age ? `${age}세에 파이어 가능 · 필요 자산까지 ${gap > 0 ? `${eok(gap)} 부족` : '충분'}` : '이 자산만으론 70세까지도 어려워요 · 생활비를 낮춰보세요'}>
        <div className="ds-mt-2-5">
          <RangeField label="자산이" value={asset} min={100000000} max={3000000000} step={50000000} money format={eok} onChange={setAsset} />
        </div>
      </StatHero>
      <Card>
        <SectionHead size="sm" kicker="구간별" title="자산이 이만큼이면 몇 살에?" desc="같은 저축·생활비 조건 · 또래 상위 %는 통계청 순자산 분포 기준" />
        <div className="ds-list">
          {bands.map((b) => (
            <div key={b.v} className="ds-row-item ds-row-item--M ds-row-item--static">
              <span className="ds-row-item__body"><span className="ds-row-item__title num">{eok(b.v)}{b.v === need ? ' · 필요 자산' : ''}</span><span className="ds-row-item__desc">또래 상위 {b.pct}%</span></span>
              <span className="ds-row-item__trail num">{b.age ? `${b.age}세` : '—'}</span>
            </div>
          ))}
        </div>
        <Button variant="tint" size="md" full className="ds-mt-3" onClick={onOpenShare}>🪪 이 결과로 인증 카드</Button>
      </Card>
    </>
  );
}

export default function Result({ inputs, simulation, rankingSimulation, onMove, onChange }) {
  const rs = rankingSimulation || simulation;
  const base = statsRank(rs);
  const inp = simulation.inputs;
  const earliest = simulation.earliestRetirementAge;
  const rankEarliest = rs.earliestRetirementAge;
  const target = inp.targetRetirementAge;
  const need = Math.round(simulation.requiredFireAssetByFourPercent || 0);
  const ph = survivalPhrase(simulation);
  const [mode, setMode] = useState('age');
  const [live, setLive] = useState(null);
  const [agg, setAgg] = useState(null);
  const [bandRank, setBandRank] = useState(null);
  const [shareOpen, setShareOpen] = useState(false);
  const levers = useLevers(simulation, onChange);
  const success = useMemo(() => { try { return monteCarloSuccess(inp, { paths: 300 }); } catch { return null; } }, [inp]);
  const myBand = assetBandOf(simulation.netWorth);
  const inputsHash = `${earliest}|${rankEarliest}|${target}|${inp.financialAsset}|${inp.monthlyInvestment}|${inp.monthlyLivingCost}`;

  useEffect(() => {
    let alive = true;
    if (!inputsIsReal(inp)) return undefined;
    saveRankSnapshot({ percentile: base.percentile, grade: base.grade, score: rs.survivalScore, earliest });
    syncWidgetSnapshot(simulation);
    track('calc_complete', { earliest: earliest || 0 });
    (async () => {
      try {
        const key = `fm_score_sent_${inputsHash}`;
        if (!sessionStorage.getItem(key)) {
          let nick = ''; try { nick = localStorage.getItem('fm_nickname') || ''; } catch { /* ignore */ }
          await submitScoreFromSim({ rankingSimulation, simulation, nickname: nick });
          sessionStorage.setItem(key, '1');
        }
      } catch { /* ignore */ }
      const [r, a, b] = await Promise.all([fetchUserRank(rankEarliest), fetchAggregates(base.ageBand), fetchUserRank(rankEarliest, undefined, undefined, myBand)]);
      if (alive) { setLive(r); setAgg(a); setBandRank(b); }
    })();
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inputsHash]);

  const peerAvg = agg && agg.avgEarliest ? agg.avgEarliest : null;
  const diff = (peerAvg != null && rankEarliest != null) ? (peerAvg - rankEarliest) : null;
  const delta = diff == null ? null : diff > 0 ? { text: `또래 평균보다 ${diff}년 빨라요`, dir: 'up' } : diff < 0 ? { text: `또래 평균보다 ${Math.abs(diff)}년 늦어요`, dir: 'down' } : { text: '또래 평균과 비슷해요' };

  // 물가 낮은 곳(접힘)
  const cities = useMemo(() => {
    const baseEnd = scenarioEndAge(simulation);
    return FIRE_CITIES.filter((c) => c.krw < inp.monthlyLivingCost).map((c) => { const sc = buildScenario(inp, { monthlyLivingCost: c.krw }); return { ...c, gain: scenarioEndAge(sc) - baseEnd, runway: runwayText(sc) }; }).filter((c) => c.gain > 0).sort((a, b) => b.gain - a.gain).slice(0, 3);
  }, [inp, simulation]);
  const fireAsset = simulation.retirementFinancialAsset || simulation.netWorth || inp.financialAsset || 0;
  const hiEst = (() => { try { return estimateLocalPremium({ chargeableIncomeManwon: Math.round((fireAsset * 0.04) / 10000), propertyTaxBaseEok: 0 }); } catch { return null; } })();

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="결과" onBack={() => onMove('home')} actions={<Button variant="ghost" size="sm" onClick={() => { try { sessionStorage.setItem('fm_recalc', '1'); } catch { /* ignore */ } onMove('question'); }}>새로 계산</Button>} />
      <ConsentSheet />
      <Tabs items={[{ key: 'age', label: '몇 살에?' }, { key: 'asset', label: 'N억이면?' }]} value={mode} onChange={setMode} label="결과 모드" />

      {mode === 'asset' ? <ReverseMode simulation={simulation} onOpenShare={() => setShareOpen(true)} /> : (
        <>
          <StatHero
            tone="dark"
            label={`내 파이어 나이 · ${base.ageBandLabel} 또래 기준`}
            value={earliest ? `${earliest}` : '아직'} unit={earliest ? '세' : ''}
            delta={delta}
            sub={<>필요 자산 <b className="num">{eok(need)}</b> · 지금 <b className="num">{eok(inp.financialAsset)}</b>{success != null ? <> · 성공확률 <b className="num">{success}%</b></> : null}</>}
            tiles={[
              { label: '파이어 때 자산', value: simulation.retirementFinancialAsset ? eok(simulation.retirementFinancialAsset) : '—' },
              { label: '버티는 나이', value: ph.runway },
              { label: `같은 구간 · ${ASSET_BAND_LABELS[myBand]}`, value: bandRank ? `상위 ${bandRank.percentile}%` : (live ? `${live.position.toLocaleString()}등` : '집계 중'), onClick: () => onMove('ranking') }
            ]}
          >
            {live && <p className="ds-caption ds-mt-3 ds-mt-3">함께 계산한 {live.total.toLocaleString()}명 중 {live.position.toLocaleString()}등 · 등수는 세전 공정 비교</p>}
          </StatHero>

          <Card>
            <SectionHead size="sm" kicker={levers.baseOk ? '더 당기기' : '목표 달성 플랜'} title={levers.baseOk ? `${levers.goal}세로 1년 당기려면` : `${target}세 파이어를 성공시키려면`} desc={levers.baseOk ? '셋 중 하나만 해도 돼요. 적용하면 위 숫자가 바로 바뀌어요.' : `${levers.until}세까지 자산이 버티게 하는 최소치예요. 하나만 골라도 돼요.`} />
            <LeverList items={levers.items} />
          </Card>

          <div className="ds-bottomcta ds-mt-0">
            <Button variant="secondary" size="lg" onClick={() => onMove('experiment')}>🎛️ 바꿔보기</Button>
            <Button variant="primary" size="lg" onClick={() => { track('cert_open', {}); setShareOpen(true); }}>🪪 인증 카드</Button>
          </div>

          <Fold icon="📈" title="자산 흐름" hint="넣은 돈 vs 불어난 돈 · 나이별" onOpen={() => track('fold_open', { k: 'flow' })}>
            <YearlyAssetChart simulation={simulation} />
          </Fold>
          <Fold icon="🩺" title="파이어 후 건보료·세금" hint={hiEst ? `지역가입 전환 시 월 약 ${hiEst.monthly.toLocaleString()}원 (추정)` : '지역가입자 전환 · 배당세'}>
            <p className="ds-p">직장을 그만두면 건보료를 혼자 내고 소득·재산 기준 <b>지역가입자</b>로 바뀌어요. 4% 인출 기준 연 금융소득 {Math.round((fireAsset * 0.04) / 10000).toLocaleString()}만원으로 잡은 대략값이에요.</p>
            <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => onMove('dependent')}>건보료 정밀 계산</Button><Button variant="secondary" size="md" onClick={() => onMove('foreignTax')}>양도·배당세</Button></div>
          </Fold>
          {cities.length > 0 && (
            <Fold icon="🌏" title="물가 낮은 곳에 살면" hint={`${cities[0].flag} ${cities[0].city} +${cities[0].gain}년`}>
              <div className="ds-list">
                {cities.map((c) => (
                  <div key={c.city} className="ds-row-item ds-row-item--S ds-row-item--static">
                    <span className="ds-row-item__lead">{c.flag}</span>
                    <span className="ds-row-item__body"><span className="ds-row-item__title">{c.city}</span><span className="ds-row-item__desc">월 {formatWon(c.krw)} · {c.runway}까지</span></span>
                    <span className="ds-row-item__trail num ds-good">+{c.gain}년</span>
                  </div>
                ))}
              </div>
              <Button variant="ghost" size="sm" className="ds-mt-2" onClick={() => onMove('cities')}>전 세계 파이어 도시 탐색 →</Button>
            </Fold>
          )}
          <Fold icon="🧭" title="내 파이어 유형" hint="12문항 · 살 도시 Top3">
            <Button variant="secondary" size="md" full onClick={() => onMove('firetype')}>유형 테스트 하기</Button>
          </Fold>

          <p className="ds-caption ds-textcenter">통계청 2024 가계금융복지조사 · 연 수익률 {inp.annualReturnRate}% · 물가 {inp.inflationRate}% · 국민연금 {inp.expectedPensionAge}세~ 월 {formatWon(inp.expectedMonthlyPension)} · 참고용 계산이에요 · 투자 자문이 아니에요</p>
        </>
      )}

      <ShareSheet open={shareOpen} onClose={() => setShareOpen(false)} simulation={simulation} onMove={onMove} />
    </main>
  );
}
