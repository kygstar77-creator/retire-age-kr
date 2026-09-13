// 결과 — 파이어 나이 하나를 크게 띄우고, 나머지 숫자에는 어느 나이 기준인지 이름표를 붙인다.
// 나이는 둘뿐이다: 내가 적은 '목표 나이'와, 계산이 찾아낸 '파이어 가능 나이'.
// 필요 자산도 파이어 나이와 같은 시뮬레이션으로 구한다(retirementSimulator의 findRequiredAssetNow).
// 'N억이면?' 탭은 없앴다 — 바꿔보기에서 '현재 자산'을 움직이면 같은 답이 나온다.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, StatHero, Card, SectionHead, Button, StatTiles } from '../../ui/index.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, buildGrowthSeries, scenarioEndAge, survivalPhrase, runwayText, targetGapText } from '../../firemap-v2/scenarios.js';
import { inputsIsReal } from '../../utils/retirementSimulator.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { submitScoreFromSim, fetchUserRank, fetchAggregates, assetBandOf, ASSET_BAND_LABELS } from '../../utils/firemapScoresApi.js';
import { saveRankSnapshot } from '../../firemap-v2/rankHistory.js';
import { FIRE_CITIES } from '../../firemap-v2/cities.js';
import { track } from '../../firemap-v2/dailyData.js';
import { assessDependentEligibility, estimateLocalPremium } from '../../firemap-v2/healthInsurance.js';
import { fireIncomeParts } from './DependentCheck.jsx';
import { syncWidgetSnapshot } from '../../utils/widgetState.js';
import ConsentSheet from './Consent.jsx';
import ShareSheet from './ShareSheet.jsx';
import FireWidgetCard from './FireWidgetCard.jsx';
import CommunityCta from './CommunityCta.jsx';

const eok = (n) => formatWon(Math.round(n || 0));

function YearlyAssetChart({ simulation }) {
  const rows = simulation.displayResult.rows || [];
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
  const ret = simulation.displayResult.retirementAge; const retX = X(Math.min(a1, Math.max(a0, ret)));
  const retIdx = Math.max(0, pts.findIndex((p) => p.age >= ret));
  const cur = sel != null ? pts[Math.min(sel, n - 1)] : (pts[retIdx] || pts[n - 1]);
  const pick = (e) => { const box = e.currentTarget.getBoundingClientRect(); const cx = e.touches && e.touches[0] ? e.touches[0].clientX : e.clientX; setSel(Math.max(0, Math.min(n - 1, Math.round(((cx - box.left) / box.width) * (n - 1))))); };
  return (
    <div className="fm-yac">
      <div className="fm-yac-read"><b>{cur.age}세</b><span className={cur.status === '파이어 후' ? 'after' : 'before'}>{cur.status}</span><strong>{formatWon(cur.v)}</strong></div>
      <p className="fm-yac-split"><i className="fm-dot fm-dot-principal" />납입 원금 {formatWon(cur.principal)} · <i className="fm-dot fm-dot-gains" />투자 수익 {formatWon(cur.gains)}</p>
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

function AssetJourney({ simulation }) {
  const rows = simulation.displayResult.rows || [];
  if (rows.length < 2) return null;
  const cur = rows[0];
  const start = cur.financialAsset;
  const y1 = rows[1] ? rows[1].financialAsset - start : 0;
  const y5 = rows[5] ? rows[5].financialAsset - start : null;
  const save1 = rows[1] ? Math.max(0, rows[1].investmentAdded) : 0;
  const ret1 = Math.max(0, y1 - save1);

  const items = [{ age: cur.age, label: '지금 시작', sub: formatWon(cur.financialAsset), hi: false }];
  [100000000, 300000000, 500000000, 1000000000, 2000000000].forEach((t) => {
    if (t > cur.financialAsset) {
      const hit = rows.find((r) => r.financialAsset >= t);
      if (hit && hit.age > cur.age) items.push({ age: hit.age, label: `자산 ${formatWon(t)} 돌파`, sub: null, hi: false });
    }
  });
  if (simulation.earliestRetirementAge) items.push({ age: simulation.earliestRetirementAge, label: '파이어 가능 나이', sub: null, hi: true });
  items.push({ age: simulation.inputs.targetRetirementAge, label: '목표 파이어', sub: null, hi: true });
  const seen = new Set();
  const list = items
    .filter((m) => { const k = `${m.age}|${m.label}`; if (seen.has(k)) return false; seen.add(k); return true; })
    .sort((a, b) => a.age - b.age);

  return (
    <Card>
      <SectionHead size="sm" kicker="내 자산 흐름" title="나이별로 얼마가 되는지" />
      <YearlyAssetChart simulation={simulation} />
      <p className="ds-caption ds-textcenter">그래프를 누르면 그 나이의 자산이 보여요</p>
      <StatTiles className="ds-mt-3" items={[
        { label: '1년 뒤', value: `+${formatWon(Math.max(0, y1))}` },
        ...(y5 != null ? [{ label: '5년 뒤', value: `+${formatWon(Math.max(0, y5))}` }] : []),
        { label: `${simulation.displayResult.retirementAge}세 때`, value: formatWon(simulation.displayResult.fireAsset || 0) }
      ]} />
      {y1 > 0 && <p className="ds-caption ds-mt-2">1년 새 <b className="num">+{formatWon(Math.max(0, y1))}</b> = 내 저축 <b className="num">{formatWon(save1)}</b> + 투자수익 <b className="num">{formatWon(ret1)}</b></p>}
      <ol className="ds-road">
        {list.map((m) => (
          <li key={`${m.age}|${m.label}`} className={`ds-road__step${m.hi ? ' ds-road__step--hi' : ''}`}>
            <span className="ds-road__age num">{m.age}세</span>
            <span className="ds-road__body"><b>{m.label}</b>{m.sub && <em className="num">{m.sub}</em>}</span>
          </li>
        ))}
      </ol>
      <p className="ds-caption">연 수익률 {simulation.inputs.annualReturnRate}% · 물가 {simulation.inputs.inflationRate}% · 그때 통장에 찍힐 금액이라 물가는 빼지 않았어요</p>
    </Card>
  );
}

export default function Result({ inputs, simulation, rankingSimulation, onMove, onChange }) {
  const rs = rankingSimulation || simulation;
  const base = statsRank(rs);
  const inp = simulation.inputs;
  const earliest = simulation.earliestRetirementAge;
  const rankEarliest = rs.earliestRetirementAge;
  const target = inp.targetRetirementAge;
  const ph = survivalPhrase(simulation);
  const [live, setLive] = useState(null);
  const [agg, setAgg] = useState(null);
  const [bandRank, setBandRank] = useState(null);
  const [shareOpen, setShareOpen] = useState(() => {
    // 랭킹에서 '인증 카드'로 넘어온 경우 결과를 열면서 시트도 같이 연다.
    try { if (sessionStorage.getItem('fm_open_cert')) { sessionStorage.removeItem('fm_open_cert'); return true; } } catch { /* ignore */ }
    return false;
  });
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
      } catch (err) { console.error('[result] 점수 전송 실패', err); }
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
    // '앞당겨져요'는 파이어 나이가 몇 년 빨라지는지다. 예전엔 자산 수명 차이를 써서 2배 넘게 부풀려졌다.
    const baseAge = simulation.earliestRetirementAge;
    if (!baseAge) return [];
    return FIRE_CITIES.filter((c) => c.krw < inp.monthlyLivingCost).map((c) => { const sc = buildScenario(inp, { monthlyLivingCost: c.krw }); const age = sc.earliestRetirementAge; return { ...c, gain: age ? baseAge - age : 0, runway: runwayText(sc) }; }).filter((c) => c.gain > 0).sort((a, b) => b.gain - a.gain).slice(0, 3);
  }, [inp, simulation]);
  // 건보료 추정 — 건보료 화면과 같은 경로로 계산한다(금융소득 1,000만 게이트 포함).
  // 예전엔 파이어 시점 '미래 명목' 자산의 4%를 전액 금융소득으로 넣어 4배 넘게 부풀려졌다.
  const atE = simulation.atEarliest || null;
  const fireAssetToday = simulation.displayResult.fireAssetToday || inp.financialAsset || 0;  // 문구가 '오늘 화폐로'라 오늘 돈을 쓴다
  const hiEst = (() => {
    try {
      const finMan = Math.round((fireAssetToday * 0.04) / 10000);
      const parts = fireIncomeParts(inp, simulation);
      const halfMan = Math.round((parts.work + parts.pension) / 10000);
      const r = assessDependentEligibility({ otherIncomeManwon: Math.round(parts.rental / 10000) + halfMan, financialIncomeManwon: finMan, propertyTaxBaseEok: 0 });
      // 건보료 화면과 같은 규칙: 금융소득 1,000만 게이트 · 임대 100% · 근로·연금 50%
      return { ...estimateLocalPremium({ chargeableIncomeManwon: Math.round(parts.rental / 10000) + (finMan > 1000 ? finMan : 0), halfRatedIncomeManwon: halfMan, propertyTaxBaseEok: 0 }), finMan };
    } catch { return null; }
  })();

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="결과" onHome={() => { try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch { /* ignore */ } }} actions={<Button variant="ghost" size="sm" onClick={() => { try { sessionStorage.setItem('fm_recalc', '1'); } catch { /* ignore */ } onMove('question'); }}>새로 계산</Button>} />
      <ConsentSheet />
      <>
          <StatHero
            tone="dark"
            label={`내 파이어 나이 · ${base.ageBandLabel} 또래 기준`}
            value={earliest ? `${earliest}` : '아직'} unit={earliest ? '세' : ''}
            delta={delta}
            sub={<>현재 자산 <b className="num">{eok(inp.financialAsset)}</b></>}
            tiles={[
              { label: `목표 ${target}세`, value: targetGapText(simulation) },
              { label: `${atE ? atE.age : target}세 때 자산`, value: eok(simulation.displayResult.fireAsset) },
              { label: `같은 구간 · ${ASSET_BAND_LABELS[myBand]}`, value: bandRank ? `상위 ${bandRank.percentile}%` : (live ? `${live.position.toLocaleString()}등` : '집계 중'), onClick: () => onMove('ranking') }
            ]}
          >
            <p className="ds-caption ds-mt-3">{[
              // 위 나이는 세금을 넣은 값인데 또래 비교·등수는 모두 세금을 뺀 값으로 맞춘다.
              // 두 값이 다를 때만 그 사실을 적어 준다.
              earliest !== rankEarliest ? '또래 비교와 등수는 세금 빼고 맞춰요' : null,
              live ? `함께 계산한 ${live.total.toLocaleString()}명 중 ${live.position.toLocaleString()}등` : null
            ].filter(Boolean).join(' · ')}</p>
          </StatHero>

          <FireWidgetCard simulation={simulation} onMove={onMove} />


          <div className="ds-bottomcta ds-mt-0">
            <Button variant="primary" size="lg" onClick={() => { track('cert_open', {}); setShareOpen(true); }}>🪪 인증 카드</Button>
          </div>

          <AssetJourney simulation={simulation} />
          <Card>
            <SectionHead size="sm" kicker="파이어 후" title="건보료와 세금" desc={hiEst ? `지역가입자로 전환되면 월 약 ${hiEst.monthly.toLocaleString()}원 (추정)` : '지역가입자 전환 · 배당세'} />
            <p className="ds-p">직장을 그만두면 건보료를 혼자 내고 소득·재산 기준 <b>지역가입자</b>로 바뀌어요. 오늘 화폐로 연 금융소득 {hiEst ? hiEst.finMan.toLocaleString() : '—'}만원을 가정한 대략값이고, 재산은 넣지 않았어요.</p>
            <div className="ds-bottomcta"><Button variant="secondary" size="md" onClick={() => onMove('dependent')}>건보료 정밀 계산</Button><Button variant="secondary" size="md" onClick={() => onMove('foreignTax')}>양도·배당세</Button></div>
          </Card>
          {cities.length > 0 && (
            <Card>
              <SectionHead size="sm" kicker="어디서 살까" title="물가 낮은 곳에 살면" desc={`${cities[0].flag} ${cities[0].city}로 가면 ${cities[0].gain}년 앞당겨져요`} />
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
            </Card>
          )}
          <CommunityCta where="result" />

          <p className="ds-caption ds-textcenter">통계청 2024 가계금융복지조사 · 연 수익률 {inp.annualReturnRate}% · 물가 {inp.inflationRate}% · 국민연금 {inp.expectedPensionAge}세~ 월 {formatWon(inp.expectedMonthlyPension)} · 참고용 계산이에요 · 투자 권유가 아니에요</p>
      </>

      <ShareSheet open={shareOpen} onClose={() => setShareOpen(false)} simulation={simulation} onMove={onMove} />
    </main>
  );
}
