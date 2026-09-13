// 어디서 살까 — 결론 하나(여기 살면 N세) · 국내|해외 탭 · 지역 목록/도시 카드 · 해외 체류. 적용은 미리보기 샌드박스로만.
import { useMemo, useState } from 'react';
import { TopBar, StatHero, Tabs, Card, SectionHead, ListGroup, ListRow, Badge, Button, Chips, Chip, Icon } from '../../ui/index.js';
import { OverseasStayModule } from './OverseasStayModule.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, runwayText, deltaText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { FIRE_CITIES as CITIES, KR_REGIONS } from '../../firemap-v2/cities.js';
import { WORLD_LAND } from '../../firemap-v2/worldLand.js';
import '../../ui/screens/cities.css';

const eok = (n) => formatWon(Math.round(n || 0));


function WorldMap({ cities, active, onPick }) {
  const W = 360, H = 180;
  const proj = (lon, lat) => [((lon + 180) / 360) * W, ((90 - lat) / 180) * H];
  // 도시가 있는 범위만 보여준다: 경도 -105~150 · 위도 -40~62
  const [vx0, vy0] = proj(-105, 62); const [vx1, vy1] = proj(150, -40);
  return (
    <div className="sc-ce-map">
      <svg viewBox={`${vx0} ${vy0} ${vx1 - vx0} ${vy1 - vy0}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="전 세계 파이어 도시 지도">
        {WORLD_LAND.map((d, i) => <path key={i} d={d} className="sc-ce-land" />)}
        {cities.map((c, i) => {
          if (c.lat == null || c.lon == null) return null;
          const [x, y] = proj(c.lon, c.lat);
          return (
            <g key={c.city} className={`sc-ce-pin${active === i ? ' is-on' : ''}`} onClick={() => onPick(i)} role="button" aria-label={c.city}>
              {active === i && <circle cx={x} cy={y} r="7" className="sc-ce-halo" />}
              <circle cx={x} cy={y} r={active === i ? 3.4 : 2.6} />
              {active === i && <text x={x} y={y - 7} textAnchor="middle" className="sc-ce-lbl">{c.city}</text>}
            </g>
          );
        })}
      </svg>
      <p className="ds-caption ds-textcenter ds-mt-2">지도의 점을 누르면 도시로 이동해요</p>
    </div>
  );
}

function deltaBadge(curAge, age) {
  if (curAge == null || age == null) return null;
  const d = curAge - age;
  if (d > 0) return <Badge tone="good">{d}년 일찍</Badge>;
  if (d < 0) return <Badge tone="bad">{-d}년 늦게</Badge>;
  return <Badge tone="neutral">비슷</Badge>;
}

export default function CityExplorer({ inputs, simulation, onChange, onMove, onBack, onPreviewCity, onPreviewPatch }) {
  const [tab, setTab] = useState('domestic');
  const [active, setActive] = useState(null);
  const [sel, setSel] = useState(null); // { name, krw }
  void onChange;
  // 적용 = 미리보기 샌드박스로만(기존 저장 무손상).
  const apply = (krw) => { if (onPreviewCity) { onPreviewCity(krw); return; } if (onMove) onMove('result'); };

  const curCost = Number(inputs.monthlyLivingCost) || 0;
  const curAge = simulation.earliestRetirementAge;
  const overseas = useMemo(() => CITIES.filter((c) => c.country !== '한국'), []);
  const regions = useMemo(() => KR_REGIONS
    .map((r) => ({ ...r, age: buildScenario(inputs, { monthlyLivingCost: r.krw }).earliestRetirementAge }))
    .sort((a, b) => {
      const aa = a.age == null ? 999 : a.age;
      const bb = b.age == null ? 999 : b.age;
      return aa !== bb ? aa - bb : a.krw - b.krw;
    }), [inputs]);

  const pick = (i) => {
    const c = overseas[i];
    setActive(i); setSel({ name: c.city, krw: c.krw });
    const el = document.getElementById(`ce-${i}`); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };
  const selSim = useMemo(() => (sel ? buildScenario(inputs, { monthlyLivingCost: sel.krw }) : null), [inputs, sel]);
  const selAge = selSim ? selSim.earliestRetirementAge : curAge;
  const heroSub = sel
    ? (selAge != null ? <>월 <b className="num">{eok(sel.krw)}</b>으로 살면 · {runwayText(selSim)}까지 버텨요 · {deltaText(simulation, selSim)}</> : '이 생활비로도 아직 안 나와요 · 더 낮은 곳을 골라봐요')
    : (curAge != null ? '지역을 고르면 여기 숫자가 바뀌어요' : '아직 파이어 나이가 안 나와요 · 생활비 낮은 곳을 골라봐요');

  return (
    <main className="fm-screen fm-scroll ds-screen-gap">
      <TopBar title="어디서 살까" onBack={onBack} />

      <StatHero
        tone="light" size="md"
        label={sel ? `${sel.name}에 살면` : `지금 생활비 월 ${eok(curCost)}이면`}
        value={selAge != null ? `${selAge}` : '아직'} unit={selAge != null ? '세' : ''}
        delta={sel && curAge != null && selAge != null && curAge !== selAge ? { text: curAge > selAge ? `지금보다 ${curAge - selAge}년 일찍` : `지금보다 ${selAge - curAge}년 늦게`, dir: curAge > selAge ? 'up' : 'down' } : null}
        sub={heroSub}
      >
        {sel && <Button variant="primary" size="md" full className="ds-mt-3" onClick={() => apply(sel.krw)}>이 조건으로 미리보기</Button>}
      </StatHero>

      <Tabs items={[{ key: 'domestic', label: '국내' }, { key: 'overseas', label: '해외' }]} value={tab} onChange={setTab} label="지역 범위" />

      {tab === 'domestic' ? (
        <>
          <ListGroup label="1인 월 생활비 기준 · 빠른 순">
            {regions.map((r) => (
              <ListRow
                key={r.city} size="M"
                title={r.city} desc={`월 ${eok(r.krw)}${r.note ? ` · ${r.note}` : ''}`}
                trail={<><b className="num">{r.age != null ? `${r.age}세` : '아직'}</b>{deltaBadge(curAge, r.age)}</>}
                className={sel && sel.name === r.city ? 'sc-ce-row sc-ce-row--on' : 'sc-ce-row'}
                onClick={() => setSel({ name: r.city, krw: r.krw })}
              />
            ))}
          </ListGroup>
          <p className="ds-caption">주거 포함 1인 월 생활비 추정이에요 · 통계청 1인가구 월평균 169만과 지역 물가 참고 · {sourceLine('cityCost')}</p>
        </>
      ) : (
        <>
          <WorldMap cities={overseas} active={active} onPick={pick} />
          {overseas.map((c, i) => {
            const sc = buildScenario(inputs, { monthlyLivingCost: c.krw });
            const on = active === i;
            return (
              <Card key={c.city} id={`ce-${i}`} className={on ? 'sc-ce-card--on' : ''}>
                <ListRow
                  size="M" lead={c.flag} title={c.city} desc={`${c.country} · 월 ${eok(c.krw)}`}
                  trail={<><b className="num">{sc.earliestRetirementAge != null ? `${sc.earliestRetirementAge}세` : '아직'}</b>{deltaBadge(curAge, sc.earliestRetirementAge)}</>}
                  onClick={() => { setActive(i); setSel({ name: c.city, krw: c.krw }); }}
                  className="sc-ce-row sc-ce-cityrow"
                />
                <p className="ds-p ds-mt-2">{c.vibe}</p>
                <Chips className="ds-mt-2">
                  {c.food.map((f) => <Chip key={f}>{f}</Chip>)}
                  {c.play.map((pl) => <Chip key={pl}>{pl}</Chip>)}
                </Chips>
                <p className="ds-caption ds-mt-2">이 생활비면 <b className="num">{runwayText(sc)}</b>까지 버텨요 · {deltaText(simulation, sc)}</p>
                <p className="ds-caption">{c.visa}</p>
                <Button variant="tint" size="md" full className="ds-mt-2" onClick={() => apply(c.krw)}>이 도시로 미리보기</Button>
              </Card>
            );
          })}
          <OverseasStayModule inputs={inputs} simulation={simulation} onPreviewPatch={onPreviewPatch} />
          <p className="ds-caption">도시별 금액은 1인 월 생활비 대략 추정이에요 · 주거·의료·환율·비자에 따라 달라져요 · {sourceLine('cityCost')}</p>
        </>
      )}

      <Card padding="md">
        <SectionHead size="sm" kicker="더 깊이 보기" title="지역 자료" />
        <ListRow lead={<Icon name="home" />} title="지역·가구별 필요 자산 사례" desc="지역·가구·유형별 필요 자산" href="/guide/region-plan/" size="S" />
        <ListRow lead={<Icon name="buildings" />} title="도시별 생활비·집값" desc="생활비·실거래가·물가" href="/guide/regions/" size="S" />
      </Card>
    </main>
  );
}
