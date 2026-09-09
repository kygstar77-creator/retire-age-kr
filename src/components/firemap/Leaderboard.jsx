// 랭킹 — 같은 구간(자산 밴드) · 또래 · 저축 리그. 4차 조사 결론: 금액 훈수 갈등 → 같은 구간 비교만. 384행 → ~170행.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, Tabs, StatHero, Card, SectionHead, ListGroup, ListRow, Button, Skeleton, EmptyState } from '../../ui/index.js';
import { identityIds, accountHandle } from '../../utils/identity.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { fetchTopScores, fetchUserRank, fetchAggregates, fetchNeighbors, assetBandOf, ASSET_BAND_LABELS, fetchPeerBoard } from '../../utils/firemapScoresApi.js';
import { fetchSaveBoard } from '../../utils/firemapSaveApi.js';
import { displayName } from '../../firemap-v2/funName.js';
import { wonStr, fmtAdvance, track } from '../../firemap-v2/dailyData.js';
import { computeProgress, hasCalculated } from '../../utils/savingsEngine.js';
import { simulateRetirement, findEarliestRetirementAge } from '../../utils/retirementSimulator.js';
import { formatWon } from '../../firemap-v2/formatters.js';

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));
const BOARDS = [{ key: 'band', label: '같은 구간' }, { key: 'peer', label: '또래' }, { key: 'save', label: '저축 리그' }];

// 바로 위 사람의 파이어 나이에 닿으려면 월 저축 얼마 더?
function monthlyToReach(inp, targetAge) {
  if (!targetAge || !inp) return null;
  const ok = (d) => { const e = findEarliestRetirementAge({ ...inp, monthlyInvestment: (inp.monthlyInvestment || 0) + d }); return e != null && e <= targetAge; };
  if (ok(0)) return 0;
  if (!ok(20000000)) return null;
  let lo = 0, hi = 20000000;
  for (let i = 0; i < 16; i += 1) { const m = (lo + hi) / 2; if (ok(m)) hi = m; else lo = m; }
  return Math.ceil(hi / 10000) * 10000;
}

export default function Leaderboard({ simulation, rankingSimulation, onMove }) {
  const rs = rankingSimulation || simulation;
  const base = statsRank(rs);
  const earliest = rs.earliestRetirementAge;
  const ids = identityIds();
  const acctHandle = accountHandle();
  const calculated = hasCalculated();
  const myAdvance = calculated ? Math.max(0, computeProgress(simulation).advanceDays) : 0;
  const myBand = calculated ? assetBandOf(simulation.netWorth) : null;
  const [board, setBoard] = useState('band');
  const [data, setData] = useState({ loading: true });

  useEffect(() => {
    let alive = true;
    setData({ loading: true });
    (async () => {
      try {
        if (board === 'band') {
          const [top, me, nb, agg] = await Promise.all([fetchTopScores(10, undefined, myBand), fetchUserRank(earliest, undefined, myAdvance, myBand), fetchNeighbors(earliest, undefined, undefined, myBand), fetchAggregates()]);
          if (alive) setData({ top: top || [], me, nb, agg });
        } else if (board === 'peer') {
          const pr = await fetchPeerBoard({ currentAge: rs.inputs.currentAge, ageBand: base.ageBand, earliestAge: earliest, advancedDays: myAdvance, limit: 10 });
          const nb = pr ? await fetchNeighbors(earliest, pr.scope === 'band' ? base.ageBand : undefined, pr.scope === 'age' ? rs.inputs.currentAge : undefined) : null;
          if (alive) setData({ top: pr ? pr.top : [], me: pr ? { position: pr.position, total: pr.total, percentile: pr.percentile } : null, nb, peer: pr });
        } else {
          const rows = await fetchSaveBoard('deposit', 10);
          if (alive) setData({ top: rows || [], save: true });
        }
      } catch { if (alive) setData({ top: [] }); }
    })();
    track('ranking_view', { board });
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [board, earliest, myBand]);

  const nearAbove = data.nb && data.nb.above && data.nb.above.length ? data.nb.above[data.nb.above.length - 1] : null;
  const needMonthly = useMemo(() => (board !== 'save' && nearAbove && nearAbove.earliest_age && earliest && nearAbove.earliest_age < earliest) ? monthlyToReach(rs.inputs, nearAbove.earliest_age) : null, [board, nearAbove, earliest, rs.inputs]);

  const scopeLabel = board === 'band' ? `자산 ${ASSET_BAND_LABELS[myBand] || '전체'} 구간` : board === 'peer' ? (data.peer ? data.peer.ageLabel : `${base.ageBandLabel} 또래`) : '이번 달 저축';
  const rowValue = (r) => (data.save ? wonStr(r.value || 0) : (r.earliest_age ? `${r.earliest_age}세` : '—'));

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="랭킹" onHome={() => onMove('home')} />
      <Tabs items={BOARDS} value={board} onChange={setBoard} label="랭킹 종류" />

      {!calculated && <EmptyState icon="🧮" title="계산하면 내 등수가 나와요" desc="1분이면 같은 구간에서 몇 등인지 보여줘요" action={{ label: '계산하기', onClick: () => onMove('question') }} />}

      {calculated && board !== 'save' && (
        <StatHero
          tone="dark"
          label={`${scopeLabel} 중 내 위치`}
          value={data.me && data.me.percentile != null ? `상위 ${data.me.percentile}` : (data.loading ? '…' : '—')} unit={data.me && data.me.percentile != null ? '%' : ''}
          sub={data.me ? `${data.me.total.toLocaleString()}명 중 ${data.me.position.toLocaleString()}등 · ${earliest ? `${earliest}세 파이어 가능` : '아직 파이어 어려움'} · 세전 공정 비교` : '집계 중…'}
          tiles={[
            { label: '구간 평균', value: data.agg && data.agg.avgEarliest ? `${data.agg.avgEarliest}세` : '—' },
            { label: '1등', value: data.top && data.top[0] && data.top[0].earliest_age ? `${data.top[0].earliest_age}세` : '—' },
            { label: '내 등수', value: data.me ? `${data.me.position.toLocaleString()}등` : '—' }
          ]}
        >
          {needMonthly != null && nearAbove && <p className="ds-caption ds-mt-3">바로 위 {displayName(nearAbove)}({nearAbove.earliest_age}세)까지 {needMonthly === 0 ? '거의 다 왔어요' : `월 +${formatWon(needMonthly)} 저축이면 제쳐요`}</p>}
        </StatHero>
      )}
      {calculated && board === 'save' && (
        <StatHero tone="dark" label="내 파이어 앞당김" value={myAdvance > 0 ? (fmtAdvance(myAdvance * 86400) || '0초') : '0초'} sub={myAdvance > 0 ? '저축을 기록할수록 더 당겨져요 🔥' : '저축 탭에서 기록하면 파이어가 당겨지고 순위가 올라요'} size="title" />
      )}

      <ListGroup label={`${scopeLabel} 상위 10`}>
        {data.loading && <div className="ds-p-3-5"><Skeleton lines={4} /></div>}
        {!data.loading && data.top && data.top.length === 0 && <div className="ds-p-3-5"><p className="ds-caption ds-m-0">아직 기록이 적어요. 첫 랭커가 되어봐요.</p></div>}
        {!data.loading && data.top && data.top.map((r, i) => {
          const mine = r.client_id && ids.includes(r.client_id);
          return <ListRow key={i} className={`ds-rank-row${mine ? ' ds-rank-row--me' : ''}`} lead={medal(i)} title={`${mine && acctHandle ? acctHandle : displayName(r)}${mine ? ' (나)' : ''}`} desc={r.age_band ? `${r.age_band}대` : undefined} trail={<span className="num">{rowValue(r)}</span>} chevron={false} size="S" />;
        })}
        {!data.loading && data.me && data.me.position > 10 && (
          <ListRow className="ds-rank-row ds-rank-row--me" lead={String(data.me.position)} title={`${acctHandle || '나'} (나)`} trail={<span className="num">{earliest ? `${earliest}세` : '—'}</span>} chevron={false} size="S" />
        )}
      </ListGroup>

      <p className="ds-caption ds-textcenter">✋ 모든 순위는 직접 입력한 기록 기반 · 자산은 구간만 저장돼요</p>
      <div className="ds-bottomcta ds-mt-0">
        <Button variant="secondary" size="md" onClick={() => onMove(board === 'save' ? 'save' : 'experiment')}>{board === 'save' ? '저축 기록하기' : '조건 바꿔 올리기'}</Button>
        <Button variant="tint" size="md" onClick={() => onMove('result')}>🪪 인증 카드</Button>
      </div>
    </main>
  );
}
