// 배당으로 파이어 — 숫자 하나(월 배당이 생활비가 되는 나이) + 입력 3 + 월별 배당 막대 + 배당 캘린더(예상) + 내 계산에 반영.
// 배당락 예상일은 dividendWatch.js 고정표. 실제 확정은 fetch-dividends(Yahoo)로만.
import { useMemo, useState } from 'react';
import { TopBar, Card, SectionHead, RangeField, StatHero, Chips, Chip, Fold, Button, Notice, toast } from '../../ui/index.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { todayStr } from '../../utils/dates.js';
import { expectedExDates, lastDayOf, YIELD_PRESETS } from '../../firemap-v2/dividendWatch.js';
import '../../ui/screens/dividend.css';

const AFTER_TAX = 0.846; // 배당소득세 15.4% 원천징수
const MAX_YEARS = 40;
const eok = (n) => formatWon(Math.round(n || 0));
const pctFmt = (v) => `${(Number(v) || 0).toFixed(1)}%`;
const WD = ['일', '월', '화', '수', '목', '금', '토'];

// 매월 적립 + 배당 전액 재투자 — 세후 월 배당이 생활비에 닿는 첫 해
function yearsToCover({ asset, yieldPct, contrib, target }) {
  if (!(target > 0) || !(yieldPct > 0)) return null;
  const monthlyAfter = (a) => (a * (yieldPct / 100) * AFTER_TAX) / 12;
  if (monthlyAfter(asset) >= target) return 0;
  const r = yieldPct / 100 / 12;
  let a = asset;
  for (let y = 1; y <= MAX_YEARS; y += 1) {
    for (let k = 0; k < 12; k += 1) a = a * (1 + r) + contrib;
    if (monthlyAfter(a) >= target) return y;
  }
  return null;
}

function MonthBars({ annualAfterTax, mode, nowMonth }) {
  const W = 320, H = 118, P = 4, TOP = 20, BOT = 16;
  const bw = (W - 2 * P) / 12;
  const vals = Array.from({ length: 12 }, (_, i) => (mode === 'quarter' ? ((i + 1) % 3 === 0 ? annualAfterTax / 4 : 0) : annualAfterTax / 12));
  const max = Math.max(...vals, 1);
  const inner = H - TOP - BOT;
  return (
    <div className="sc-div-bars">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="월별 배당 막대">
        {vals.map((v, i) => {
          const m = i + 1;
          const h = v > 0 ? Math.max(3, (v / max) * inner) : 3;
          const x = P + i * bw + bw * 0.18;
          const y = TOP + inner - h;
          const now = m === nowMonth;
          const showVal = v > 0 && (mode === 'quarter' || now);
          return (
            <g key={m}>
              <rect className={`sc-div-bar${v > 0 ? '' : ' sc-div-bar--zero'}${now && v > 0 ? ' sc-div-bar--now' : ''}`} x={x.toFixed(1)} y={y.toFixed(1)} width={(bw * 0.64).toFixed(1)} height={h.toFixed(1)} rx="3" />
              {showVal && <text className="sc-div-bar__val" x={(x + bw * 0.32).toFixed(1)} y={(y - 4).toFixed(1)}>{eok(v)}</text>}
              <text className={`sc-div-bar__month${now ? ' sc-div-bar__month--now' : ''}`} x={(x + bw * 0.32).toFixed(1)} y={H - 3}>{m}월</text>
            </g>
          );
        })}
      </svg>
      <div className="sc-div-bars__foot">
        <span className="ds-caption">{mode === 'quarter' ? '3·6·9·12월에 몰려 들어와요' : '매달 비슷하게 들어와요'}</span>
        <span className="ds-caption num">연 {eok(annualAfterTax)} 세후</span>
      </div>
    </div>
  );
}

function MiniCalendar() {
  const today = todayStr();
  const [yy, mm, dd] = today.split('-').map(Number);
  const [sel, setSel] = useState(null);
  const marks = useMemo(() => expectedExDates(yy, mm), [yy, mm]);
  const byDay = useMemo(() => marks.reduce((acc, it) => { (acc[it.day] = acc[it.day] || []).push(it); return acc; }, {}), [marks]);
  const first = new Date(yy, mm - 1, 1).getDay();
  const last = lastDayOf(yy, mm);
  const cells = [...Array.from({ length: first }, () => null), ...Array.from({ length: last }, (_, i) => i + 1)];
  const list = sel ? marks.filter((it) => it.day === sel) : marks.filter((it) => it.day >= dd);
  return (
    <div className="sc-div-cal">
      <div className="sc-div-cal__head">
        <span className="sc-div-cal__title num">{yy}년 {mm}월</span>
        <span className="sc-div-cal__tag">전부 예상일이에요</span>
      </div>
      <div className="sc-div-cal__grid" role="grid" aria-label={`${mm}월 배당 캘린더`}>
        {WD.map((w, i) => <span key={w} className={`sc-div-cal__wd${i === 0 ? ' sc-div-cal__wd--sun' : ''}`}>{w}</span>)}
        {cells.map((d, i) => d == null
          ? <span key={`b${i}`} className="sc-div-cal__day sc-div-cal__day--blank" aria-hidden="true" />
          : (
            <button
              type="button" key={d}
              className={`sc-div-cal__day${d === dd ? ' sc-div-cal__day--today' : ''}${byDay[d] ? ' sc-div-cal__day--mark' : ''}${sel === d ? ' sc-div-cal__day--sel' : ''}`}
              onClick={() => setSel(sel === d ? null : d)}
              aria-label={`${d}일${byDay[d] ? ` 배당락 예상 ${byDay[d].length}개` : ''}`}
            >
              {d}
              <span className="sc-div-cal__dots" aria-hidden="true">{(byDay[d] || []).slice(0, 3).map((it) => <i key={it.symbol} />)}</span>
            </button>
          ))}
      </div>
      {list.length > 0 ? (
        <div className="ds-list sc-div-cal__list">
          {list.map((it) => (
            <div key={`${it.symbol}-${it.day}`} className="ds-row-item ds-row-item--S ds-row-item--static">
              <span className="ds-row-item__lead num">{it.day}일</span>
              <span className="ds-row-item__body"><span className="ds-row-item__title">{it.name}</span><span className="ds-row-item__desc">{it.market === 'US' ? '미국' : '국내'} · {it.freq === 'monthly' ? '월배당' : '분기배당'}</span></span>
              <span className="ds-row-item__trail sc-div-cal__tag">예상</span>
            </div>
          ))}
        </div>
      ) : (
        <p className="ds-caption sc-div-cal__empty">{sel ? `${sel}일엔 예상 배당락이 없어요` : '이번 달 남은 예상 배당락이 없어요'}</p>
      )}
    </div>
  );
}

export default function DividendLifeCalc({ inputs, onChange, onMove, onBack }) {
  void onMove;
  const [asset, setAsset] = useState(() => Math.max(0, Number(inputs?.financialAsset) || 300000000));
  const [yieldPct, setYieldPct] = useState(4.0);
  const [contrib, setContrib] = useState(() => Math.max(0, Number(inputs?.monthlyInvestment) || 500000));
  const [barMode, setBarMode] = useState('quarter');
  const [divGrowth, setDivGrowth] = useState(0);

  const currentAge = Number(inputs?.currentAge) || 35;
  const target = Number(inputs?.monthlyLivingCost) || 0;
  const annual = asset * (yieldPct / 100);
  const annualAfter = annual * AFTER_TAX;
  const monthlyAfter = annualAfter / 12;
  const needed = yieldPct > 0 && target > 0 ? (target * 12) / ((yieldPct / 100) * AFTER_TAX) : 0;
  const coverage = target > 0 ? Math.round((monthlyAfter / target) * 100) : null;
  const years = useMemo(() => yearsToCover({ asset, yieldPct, contrib, target }), [asset, yieldPct, contrib, target]);
  const fireAge = years == null ? null : currentAge + years;
  const over2000 = annual > 20000000;
  const over1000 = annual > 10000000;
  const nowMonth = Number(todayStr().split('-')[1]);

  const appliedMonthly = Math.round(monthlyAfter);
  const isApplied = appliedMonthly > 0 && Math.round(Number(inputs?.dividendIncomeMonthly) || 0) === appliedMonthly;
  const apply = () => {
    if (!onChange) return;
    onChange('dividendIncomeMonthly', appliedMonthly);
    onChange('dividendIncomeGrowth', divGrowth);
    // 배당세(재투자)와는 같은 배당을 두 번 세지 않도록 한쪽만 켜요
    const it = Number(inputs?.investType) || 0;
    if (it === 2) onChange('investType', 0);
    else if (it === 3) onChange('investType', 1);
    toast.good('반영했어요. 결과 숫자가 바뀌어요');
  };
  const unapply = () => { if (onChange) onChange('dividendIncomeMonthly', 0); toast('반영을 해제했어요'); };

  const heroValue = target <= 0 ? '—' : years == null ? '아직' : years === 0 ? '지금' : String(fireAge);
  const heroUnit = target > 0 && years != null && years > 0 ? '세' : '';
  const heroSub = target <= 0
    ? '파이어 후 생활비를 먼저 정하면 나이가 나와요'
    : yieldPct <= 0
      ? '배당률을 넣으면 나이가 나와요'
      : years == null
        ? `${MAX_YEARS}년 안엔 안 닿아요 · 월 적립을 늘려보세요`
      : years === 0 ? '벌써 생활비를 넘겼어요 · 세후 · 건보료 별도' : '세후 · 건보료 별도';

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <TopBar title="배당으로 파이어" onBack={onBack} />

      <Card>
        <SectionHead size="sm" kicker="내 조건" title="배당 자산과 배당률" desc="세후 15.4% 기준 · 배당은 전부 다시 투자한다고 봐요" />
        <RangeField label="배당 자산" value={asset} min={0} max={3000000000} step={10000000} money format={eok} chips={[10000000, 100000000, 1000000000]} onChange={setAsset} />
        <RangeField label="배당률" value={yieldPct} min={0} max={12} step={0.1} format={pctFmt} onChange={(v) => setYieldPct(Math.round(v * 10) / 10)} hint="SCHD는 오르는 데 같이 가고, JEPI는 배당은 높지만 상승은 제한돼요" />
        <Chips className="ds-mt-2">
          {YIELD_PRESETS.map((p) => <Chip key={p.label} on={Math.abs(yieldPct - p.value) < 0.05} onClick={() => setYieldPct(p.value)}>{p.label} {p.value.toFixed(1)}%</Chip>)}
        </Chips>
        <RangeField label="월 적립" value={contrib} min={0} max={5000000} step={100000} money format={eok} chips={[100000, 500000, 1000000]} onChange={setContrib} />
      </Card>

      <StatHero
        tone="dark"
        label={target > 0 ? `월 배당 ${eok(target)}이 되는 나이` : '월 배당이 생활비가 되는 나이'}
        value={heroValue} unit={heroUnit}
        sub={heroSub}
        tiles={[
          { label: '지금 월 배당 · 세후', value: eok(monthlyAfter) },
          { label: '필요 자산', value: needed > 0 ? eok(needed) : '—' },
          { label: '생활비 충당', value: coverage != null ? `${Math.min(999, coverage)}%` : '—' }
        ]}
      />

      {over2000 && <Notice tone="warn" icon="⚠️">연 배당 <b className="num">{eok(annual)}</b> · 2,000만원을 넘으면 종합과세 대상이에요</Notice>}
      {!over2000 && over1000 && <Notice tone="warn" icon="🩺">연 배당 <b className="num">{eok(annual)}</b> · 1,000만원을 넘으면 건보료에 잡혀요</Notice>}

      <Card>
        <SectionHead size="sm" kicker="월별" title="월별 배당" desc="지금 자산 기준 세후 배당이 달마다 얼마씩 들어오는지" action={
          <Chips>
            <Chip on={barMode === 'quarter'} onClick={() => setBarMode('quarter')}>분기</Chip>
            <Chip on={barMode === 'month'} onClick={() => setBarMode('month')}>월배당</Chip>
          </Chips>
        } />
        <MonthBars annualAfterTax={annualAfter} mode={barMode} nowMonth={nowMonth} />
      </Card>

      <Card>
        <SectionHead size="sm" kicker="배당락" title="배당 캘린더" desc="배당락은 이 날 전에 사야 배당을 받는 날이에요 · 날짜를 누르면 종목이 보여요" />
        <MiniCalendar />
      </Card>

      <Fold icon="🧮" title="내 파이어 계산에 반영" hint={isApplied ? `반영 중 · 월 ${eok(appliedMonthly)}` : `세후 월 ${eok(monthlyAfter)}을 배당 소득으로`}>
        <p className="ds-body-sm sc-div-note">세후 월 배당이 파이어 후 배당 소득으로 매년 들어가요. 배당세 재투자 조건과는 한쪽만 켜져요.</p>
        <RangeField label="배당 매년 성장률" value={divGrowth} min={0} max={10} step={1} format={(v) => `${Math.round(v)}%`} onChange={(v) => setDivGrowth(Math.round(v))} />
        {isApplied
          ? <Button variant="secondary" size="md" full onClick={unapply}>✓ 반영 중 · 월 {eok(appliedMonthly)} · 해제</Button>
          : <Button variant="primary" size="md" full disabled={appliedMonthly <= 0} onClick={apply}>월 {eok(monthlyAfter)} 반영</Button>}
      </Fold>

      <p className="ds-caption ds-textcenter">참고용 계산이에요 · 투자 자문이 아니에요</p>
    </main>
  );
}
