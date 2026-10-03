// E-2 "테슬라 — 매출 10분기 최대, 영업이익률 1.4%" — 재료: work/video/e2.json(ep/E-2/e2props.py가 script.md·voice.json·원자료로 만든다)
// 장면 종류 19가지: 저울+숫자 카드 · 목록 6칸 · 막대+선 10분기 · 같은 분기 가로 막대 · 순이익 두 칸+도넛 · 띠 비율 · 기울기 줄 · 계단 · 동전 탑→원문→비교 막대 ·
// 폭포 · 10분기 막대+메모 · 채움 막대 · 들어온/나간 돈 탑 · 타임라인+한도 띠 · 면적 원 · 5년 선+낙폭 음영 · 나이 막대 2묶음 · 두 칸 정리 · 문장 카드
// 숫자는 전부 e2.json에서 온다(코드 안에는 눈금·배치 값만). 단계 시점은 data.at(문장 번호, 못 찾으면 −1=안 나옴).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {line as d3line, area as d3area, curveMonotoneX} from 'd3-shape';
import {T, F, CL, FONT_CSS, VScene, at, appear, HandCircle, CountUp, Page, LogoSting, ProgressRail} from './parts/fm';
import {BarSeries, Donut, Seesaw, QuoteCard, Stairs} from './parts/charts';
import {ComboBarLine, Waterfall, SlopeRows, AreaCircles, FillBar} from './parts/ledger';

export type E2Props = {fps: number; rail: string[]; scenes: VScene[]; missing: number; holes: number};
export const e2Frames = (p: E2Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: VScene};
const NEVER = 1e9;
const A = (s: VScene, k: number) => (s.data.at?.[k] ?? -1) < 0 ? NEVER : at(s, s.data.at[k]);
const RailCtx = React.createContext<string[]>([]);
const n0 = (v: number) => v.toLocaleString();
const usd = (m: number) => { const e = Math.floor(m / 100), r = m % 100; return e ? (r ? `${e}억 ${r}00만` : `${e}억`) : `${r}00만`; };   // 백만 달러 → '억 ○00만'
const Card: React.FC<{x: number; y: number; w: number; h?: number; o?: number; bg?: string; style?: React.CSSProperties; children?: React.ReactNode}> = ({x, y, w, h, o = 1, bg = T.surface, style, children}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: bg, borderRadius: 20, opacity: o, ...style}}>{children}</div>
);
const Chip: React.FC<{x: number; y: number; o: number; text: string; dark?: boolean; size?: number; right?: boolean}> = ({x, y, o, text, dark = true, size = 32, right}) => (
  <div style={{...F, position: 'absolute', [right ? 'right' : 'left']: x, top: y, opacity: o, fontWeight: 700, fontSize: size, color: dark ? '#fff' : T.ink, background: dark ? T.ink : T.soft,
    borderRadius: 40, padding: '10px 28px', whiteSpace: 'nowrap'}}>{text}</div>
);
const P: React.FC<S & {children: React.ReactNode}> = ({s, children}) => {
  const rail = React.useContext(RailCtx);
  return <Page s={{...s, rail: 0}}>{s.rail ? <ProgressRail n={rail.length} cur={s.rail} labels={rail} on={T.ink} /> : null}{children}</Page>;
};

// ───── 0. 여는 장면: 저울(이자수익 > 영업이익) → 숫자 카드 두 장 → 질문 두 개 ─────
const Open: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const tilt = appear(f, 20, 40); const c1 = appear(f, A(s, 1)), c2 = appear(f, A(s, 2)); const ret = appear(f, A(s, 3)), qs = appear(f, A(s, 4));
  const so = interpolate(f, [A(s, 1), A(s, 1) + 12], [1, 0], CL);
  return (
    <P s={{...s, title: '테슬라 2026년 2분기 — 본업보다 이자'}}>
      <div style={{opacity: so}}>
        <Seesaw cx={960} cy={420} L={['이자수익', `${usd(d.int)} 달러`]} R={['영업이익(본업)', `${usd(d.op)} 달러`]} ratio={0.45} p={tilt} />
      </div>
      <Card x={200} y={290} w={700} h={300} o={c1 * (1 - qs)}>
        <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink3, padding: '34px 44px 0'}}>매출 · 10분기 중 최대</div>
        <div style={{...F, fontWeight: 700, fontSize: 132, color: T.ink, padding: '0 44px', lineHeight: 1.2}}><CountUp to={d.rev} p={c1} />억$</div>
      </Card>
      <Card x={1000} y={290} w={720} h={300} o={c2 * (1 - qs)} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 36, color: T.dink3, padding: '34px 44px 0'}}>영업이익률 · 10분기 중 최저</div>
        <div style={{...F, fontWeight: 700, fontSize: 132, color: T.daccent, padding: '0 44px', lineHeight: 1.2}}><CountUp to={d.margin} p={c2} digits={1} />%</div>
      </Card>
      <Chip x={200} y={640} o={ret * (1 - qs)} text="끝에서: 이 흔들림이 내 은퇴 나이를 몇 년 바꾸나" dark={false} />
      {['매출은 늘었는데 본업 이익은 왜 줄었나?', '9월 29일 300억 달러 신용 한도 공시는 무슨 뜻?'].map((t, i) => (
        <Card key={t} x={260} y={300 + i * 180} w={1400} h={140} o={appear(f, A(s, 4) + i * 30)}>
          <div style={{...F, fontWeight: 700, fontSize: 54, color: T.ink, padding: '36px 50px'}}><span style={{color: T.accent}}>Q{i + 1}. </span>{t}</div>
        </Card>))}
    </P>
  );
};

// ───── 1. 오늘 볼 여섯 가지(2열) ─────
const Agenda: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const items: string[] = s.data.items; const per = Math.max(20, Math.floor((s.frames - 60) / items.length));
  return (
    <P s={s}>
      {items.map((t, i) => { const o = appear(f, 20 + i * per);
        return <div key={t} style={{position: 'absolute', left: 220 + (i % 2) * 800, top: 290 + Math.floor(i / 2) * 170, display: 'flex', alignItems: 'center', gap: 34, opacity: o, transform: `translateX(${(1 - o) * -30}px)`}}>
          <div style={{width: 96, height: 96, borderRadius: 22, background: i === items.length - 1 ? T.accent : T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <span style={{...F, fontWeight: 700, fontSize: 52, color: '#fff'}}>{i + 1}</span></div>
          <span style={{...F, fontWeight: 700, fontSize: 60, color: T.ink}}>{t}</span>
        </div>; })}
    </P>
  );
};

// ───── 2a. 10분기 매출 막대 + 영업이익률 선 ─────
const Ledger: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <ComboBarLine x={240} y={820} w={1440} h={480} vals={d.rev} labels={d.q} line={d.margin} lineMax={14} p={appear(f, 6, 40)} tagBars={[0, 9]} tagP={appear(f, A(s, 1))}
        lp={appear(f, A(s, 2), 40)} fmt={(v) => `${v}억`} />
    </P>
  );
};

// ───── 2b. 같은 분기 가로 막대 2쌍 ─────
const Yoy: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows = s.data.rows; const call = appear(f, A(s, 1));
  return (
    <P s={s}>
      {rows.map(([n, a, b, pct]: [string, number, number, string], i: number) => { const mx = Math.max(a, b);   // 줄마다 자기 눈금(매출과 영업이익은 단위 크기가 30배 달라 같은 눈금이면 영업이익이 안 보인다)
        const o = appear(f, 10 + i * 40, 30); const top = 260 + i * 290; const sc = 950 / mx;
        return <div key={n} style={{position: 'absolute', left: 200, top}}>
          <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink}}>{n}</div>
          {[[a, '2025년 2분기', T.line], [b, '2026년 2분기', i === 0 ? T.ink : T.fall]].map(([v, lab, c], j) => (
            <div key={j} style={{position: 'absolute', left: 260, top: j * 84 - 10, display: 'flex', alignItems: 'center', gap: 18}}>
              <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3, width: 150}}>{lab as string}</div>
              <div style={{width: (v as number) * sc * o, height: 62, borderRadius: 10, background: c as string}} />
              <div style={{...F, fontWeight: 700, fontSize: 40, color: j ? (i === 0 ? T.ink : T.fall) : T.ink2, opacity: o}}>{n0(v as number)}</div>
            </div>))}
          <div style={{...F, position: 'absolute', left: 0, top: 64, fontWeight: 700, fontSize: 60, color: pct.startsWith('−') ? T.fall : T.rise, opacity: o}}>{pct}</div>
        </div>; })}
      <Chip x={200} y={860} o={call} text="매출 ¼ 늘고, 본업 이익은 절반 넘게 줄고" size={34} />
    </P>
  );
};

// ───── 2c. 순이익 두 칸 → 세전이익 중 영업 몫 도넛 ─────
const Pretax: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const dn = appear(f, A(s, 1), 30);
  return (
    <P s={s}>
      {[['2025년 2분기 순이익', d.net[0]], ['2026년 2분기 순이익', d.net[1]]].map(([t, v], i) => (
        <Card key={i} x={200 + i * 420} y={280} w={380} h={220} o={appear(f, 10 + i * 20)}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink3, padding: '30px 34px 0'}}>{t as string}</div>
          <div style={{...F, fontWeight: 700, fontSize: 84, color: T.ink, padding: '6px 34px'}}>{n0(v as number)}</div>
        </Card>))}
      <div style={{...F, position: 'absolute', left: 580, top: 350, fontWeight: 700, fontSize: 60, color: T.ink3, opacity: appear(f, 30)}}>→</div>
      <Chip x={200} y={540} o={appear(f, 50)} text="거의 그대로" dark={false} />
      <Donut cx={1440} cy={500} r={170} v={d.share} p={dn} label={`세전이익 ${n0(d.pre)} 중 영업이익 몫`} />
      <div style={{position: 'absolute', left: 200, top: 650, opacity: dn}}>
        {[['영업이익', d.op, T.ink], ['이자수익', d.int, T.accent], ['기타수익', d.oth, T.ink2]].map(([k, v, c], i) => (
          <div key={i} style={{display: 'flex', gap: 24, alignItems: 'baseline', height: 66}}>
            <span style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2, width: 170}}>{k as string}</span>
            <span style={{...F, fontWeight: 700, fontSize: 46, color: c as string}}>{n0(v as number)}</span></div>))}
      </div>
    </P>
  );
};

// ───── 3a. 부문 띠(205/31/46) + 부문 카드 ─────
const Mix: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows = s.data.rows; const tot = rows.reduce((a: number, r: any[]) => a + r[1], 0); const W = 1560, X = 200;
  let acc = 0;
  return (
    <P s={s}>
      {rows.map(([n, v, g, note]: [string, number, string, string], i: number) => { const x = X + (acc / tot) * W; acc += v; const w = (v / tot) * W; const o = appear(f, A(s, i + 1) === NEVER ? 20 + i * 30 : A(s, i + 1), 20);
        const cardX = [200, 760, 1260][i];
        return <React.Fragment key={n}>
          <div style={{position: 'absolute', left: x, top: 280, width: Math.max(4, (w - 6) * Math.max(appear(f, 6, 30), 0)), height: 130, borderRadius: 14, background: o > 0.5 ? [T.ink, T.accent, T.ink2][i] : T.line}} />
          {w > 400 ? <div style={{...F, position: 'absolute', left: x + 30, top: 318, fontWeight: 700, fontSize: 46, color: '#fff', opacity: o}}>{`${n} ${v}억$`}</div> : null}
          <Card x={cardX} y={480} w={i === 0 ? 520 : 460} h={300} o={o}>
            <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, padding: '28px 34px 0'}}>{n}</div>
            <div style={{...F, fontWeight: 700, fontSize: 80, color: T.ink, padding: '0 34px'}}>{v}<span style={{fontSize: 40}}>억$</span></div>
            <div style={{...F, fontWeight: 700, fontSize: 40, color: T.rise, padding: '0 34px'}}>{g}</div>
            <div style={{...F, fontWeight: 500, fontSize: 26, color: T.ink2, padding: '10px 34px'}}>{note}</div>
          </Card>
        </React.Fragment>; })}
    </P>
  );
};

// ───── 3b. 매출총이익률 기울기 줄 ─────
const Slope: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <SlopeRows x={200} y={300} w={1500} h={500} rows={d.rows} max={34} hi={d.hi} heads={['2025년 2분기', '2026년 2분기']}
        p={d.rows.map((_: any, i: number) => appear(f, A(s, i + 1) === NEVER ? 20 + i * 40 : A(s, i + 1), 30))} />
    </P>
  );
};

// ───── 3c. 매출총이익 계단 ─────
const StairsV: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <Stairs x={500} y={800} w={900} h={430} rows={d.rows} p={d.rows.map((_: any, i: number) => appear(f, 6 + i * 20, 24))} tag={`매출총이익 ${d.tag}`} tagP={appear(f, A(s, 1))} fmt={n0} />
    </P>
  );
};

// ───── 4. 규제 크레딧: 동전 탑 → 원문 카드 → '줄어든 돈 vs 영업이익 전체' ─────
const Credit: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const q = A(s, 3), cmp = A(s, 4);
  const coinO = interpolate(f, [q, q + 12], [1, 0], CL); const qo = interpolate(f, [q, q + 12, cmp, cmp + 10], [0, 1, 1, 0], CL); const co = appear(f, cmp + 6);
  const stack = (cx: number, v: number, p: number, lab: string, dark: boolean) => { const n = Math.round((v / 20) * p);
    return <g>{Array.from({length: n}).map((_, i) => <ellipse key={i} cx={cx} cy={800 - i * 24} rx={120} ry={30} fill={dark ? T.ink : T.line} stroke={dark ? T.ink2 : T.ink3} strokeWidth={3} />)}
      <text x={cx} y={800 - n * 24 - 46} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={48} fill={T.ink} opacity={p}>{v}</text>
      <text x={cx} y={880} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2}>{lab}</text></g>; };
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute', opacity: coinO}}>
        {stack(560, d.a, appear(f, 10, 40), '2025년 2분기', false)}
        {stack(1060, d.b, appear(f, A(s, 2) === NEVER ? 60 : A(s, 2) - 20, 30), '2026년 2분기', true)}
      </svg>
      <div style={{...F, position: 'absolute', left: 1300, top: 420, fontWeight: 700, fontSize: 120, color: T.fall, opacity: appear(f, A(s, 2)) * coinO}}>{d.pct}</div>
      <div style={{position: 'absolute', left: 0, top: 0, opacity: qo}}>
        <Card x={200} y={280} w={1520} h={440}>
          <div style={{...F, position: 'absolute', left: 50, top: 30, fontWeight: 700, fontSize: 26, color: T.ink3}}>테슬라 10-Q (2026-07-23)</div>
          <div style={{position: 'absolute', left: 50, top: 60, fontFamily: 'PD', fontWeight: 700, fontSize: 120, color: T.line, lineHeight: 1}}>“</div>
          <div style={{position: 'absolute', left: 130, right: 70, top: 90, fontFamily: 'PD', fontWeight: 500, fontSize: 36, color: T.ink2, lineHeight: 1.4}}>{d.quote[0]}</div>
          <div style={{...F, position: 'absolute', left: 130, right: 70, bottom: 60, fontWeight: 700, fontSize: 52, color: T.ink, lineHeight: 1.35, wordBreak: 'keep-all'}}>{d.quote[1]}</div>
        </Card>
      </div>
      <svg width={1920} height={1080} style={{position: 'absolute', opacity: co}}>
        {[['줄어든 규제 크레딧', d.cut, T.fall], ['이번 분기 영업이익 전체', d.op, T.ink]].map(([n, v, c], i) => { const w = ((v as number) / d.op) * 1100 * co;
          return <g key={i}><text x={200} y={360 + i * 220} fontFamily="PD" fontWeight={700} fontSize={36} fill={T.ink2}>{n as string}</text>
            <rect x={200} y={390 + i * 220} width={w} height={100} rx={12} fill={c as string} />
            <text x={220 + w} y={460 + i * 220} fontFamily="PD" fontWeight={700} fontSize={56} fill={c as string}>{v as number}</text></g>; })}
      </svg>
    </P>
  );
};

// ───── 5a. 폭포: 매출총이익 → 연구개발비 → 판매관리비 → 영업이익 ─────
const WaterfallV: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o = [appear(f, 10, 24), appear(f, A(s, 1), 24), appear(f, A(s, 2), 24), appear(f, A(s, 2) === NEVER ? 80 : A(s, 2) + 40, 24)];
  return (
    <P s={s}>
      <Waterfall x={300} y={790} w={1200} h={480} steps={d.steps} p={o} tags={d.yoy} tagP={appear(f, A(s, 4))} />
      <Chip x={110} y={250} right o={appear(f, A(s, 3))} text={`영업비용 ${n0(d.opex[0])} → ${n0(d.opex[1])}`} size={34} />
      {[1, 2].map((k) => <Chip key={k} x={300 + (k - 1) * 460} y={232} o={o[k]} text={`${d.steps[k][0]} ${n0(d.steps[k][1]).replace("-", "−")} · ${d.yoy[k]}`} size={30} />)}
    </P>
  );
};

// ───── 5b. 연구개발비 10분기 + 사이버캡·옵티머스 메모 ─────
const Rd10: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const tag = appear(f, 50); const nt = appear(f, A(s, 1));
  return (
    <P s={s}>
      <BarSeries x={240} y={800} w={1100} h={440} vals={d.v} labels={d.q} p={appear(f, 6, 40)} color={T.ink} hi={[9]} ring={[0]} fmt={n0} />
      <Chip x={240} y={260} o={tag} text={`첫 분기의 ${d.x}배`} size={40} />
      {d.notes.map(([k, v]: string[], i: number) => <Card key={k} x={1420} y={330 + i * 200} w={440} h={170} o={appear(f, (nt > 0 ? A(s, 1) : NEVER) + i * 20)}>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, padding: '30px 34px 0'}}>{k}</div>
        <div style={{...F, fontWeight: 500, fontSize: 30, color: T.ink2, padding: '8px 34px'}}>{v}</div></Card>)}
    </P>
  );
};

// ───── 6a. 설비투자: 올해 계획 테두리 안 상반기 채움 + 남은 칸 + 1년 전 상반기 ─────
const Capex: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <FillBar x={200} y={400} w={1500} h={150} plan={d.plan} done={d.h1} p={appear(f, A(s, 1) === NEVER ? 10 : A(s, 1) - 10, 30)} planP={appear(f, A(s, 2))} restP={appear(f, A(s, 3), 24)}
        ghost={d.prev} ghostP={appear(f, A(s, 1) + 30)} labels={{done: `상반기 ${n0(d.h1)}`, plan: `올해 계획 ${n0(d.plan)} 넘게`, rest: `하반기 최소 ${n0(d.left)}`, ghost: `1년 전 상반기 ${n0(d.prev)} → ${d.x}배`}} />
    </P>
  );
};

// ───── 6b. 상반기 들어온 현금 vs 나간 돈 탑 + 원문 ─────
const Cash: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const H = 480, base = 800, mx = (d.capex + d.spacex) * 1.08; const sy = (v: number) => (v / mx) * H;
  const o1 = appear(f, 10, 24), o2 = appear(f, A(s, 1) === NEVER ? 40 : A(s, 1), 24); const qo = appear(f, A(s, 2));
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={200} x2={1000} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} />
        <rect x={260} y={base - sy(d.capex) * o1} width={220} height={sy(d.capex) * o1} rx={8} fill={T.ink} />
        <rect x={260} y={base - sy(d.capex) - sy(d.spacex) * o1} width={220} height={sy(d.spacex) * o1} rx={8} fill={T.ink2} />
        <text x={370} y={base - sy(d.capex) / 2} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill="#fff" opacity={o1}>{`설비투자 ${n0(d.capex)}`}</text>
        <text x={370} y={base - sy(d.capex) - sy(d.spacex) / 2 + 10} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill="#fff" opacity={o1}>{`스페이스X ${n0(d.spacex)}`}</text>
        <text x={370} y={base + 44} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink}>나간 돈</text>
        <rect x={620} y={base - sy(d.in) * o2} width={220} height={sy(d.in) * o2} rx={8} fill={T.accent} />
        <text x={730} y={base - sy(d.in) * o2 - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={36} fill={T.accent} opacity={o2}>{n0(d.in)}</text>
        <text x={730} y={base + 44} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink}>영업으로 들어온 현금</text>
        <g opacity={o2}><line x1={860} x2={900} y1={base - sy(d.capex + d.spacex)} y2={base - sy(d.capex + d.spacex)} stroke={T.fall} strokeWidth={4} />
          <line x1={880} x2={880} y1={base - sy(d.capex + d.spacex)} y2={base - sy(d.in)} stroke={T.fall} strokeWidth={4} />
          <text x={910} y={base - sy(d.in) - 30} fontFamily="PD" fontWeight={700} fontSize={40} fill={T.fall}>{`−${n0(d.gap)}`}</text></g>
      </svg>
      <div style={{position: 'absolute', left: 0, top: 0}}><QuoteCard x={1060} y={300} w={780} h={440} o={qo} src="테슬라 10-Q (2026-07-23)" body={d.quote[0]} big="" /></div>
      <div style={{...F, position: 'absolute', left: 1150, top: 610, width: 640, fontWeight: 700, fontSize: 40, color: T.ink, opacity: qo, wordBreak: 'keep-all', lineHeight: 1.35}}>{d.quote[1]}</div>
    </P>
  );
};

// ───── 7a. 타임라인 + 새 한도 띠(3년 200·5년 80·364일 20) ─────
const Facility: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const tl = appear(f, 6, 30); const rows = d.rows; const W = 1500, X = 200; let acc = 0;
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={X} x2={X + (W) * tl} y1={300} y2={300} stroke={T.ink3} strokeWidth={4} />
        {d.tl.map(([dt, t]: string[], i: number) => <g key={i} opacity={appear(f, 10 + i * 30)}>
          <circle cx={X + 200 + i * 900} cy={300} r={18} fill={i ? T.accent : T.ink2} />
          <text x={X + 200 + i * 900} y={262} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={34} fill={T.ink}>{dt}</text>
          <text x={X + 200 + i * 900} y={352} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={28} fill={T.ink2}>{t}</text></g>)}
      </svg>
      {rows.map(([n, v]: [string, number], i: number) => { const x = X + (acc / d.total) * W; acc += v; const w = (v / d.total) * W; const o = appear(f, (A(s, 1) === NEVER ? 60 : A(s, 1)) + i * 20, 20);
        return <React.Fragment key={n}>
          <div style={{position: 'absolute', left: x, top: 470, width: Math.max(0, (w - 8) * o), height: 160, borderRadius: 14, background: [T.ink, T.ink2, T.ink3][i]}} />
          <div style={{...F, position: 'absolute', left: x + (i === 2 ? 12 : 24), top: 490, fontWeight: 700, fontSize: i === 2 ? 24 : 40, color: '#fff', opacity: o, whiteSpace: 'nowrap'}}>{n}</div>
          <div style={{...F, position: 'absolute', left: x + (i === 2 ? 12 : 24), top: 540, fontWeight: 700, fontSize: i === 2 ? 40 : 64, color: '#fff', opacity: o}}>{v}</div>
        </React.Fragment>; })}
      <div style={{...F, position: 'absolute', left: X, top: 660, fontWeight: 700, fontSize: 48, color: T.ink, opacity: appear(f, A(s, 1) + 70)}}>{`합계 ${d.total}억 달러`}</div>
      <Chip x={X + 640} y={664} o={appear(f, A(s, 2))} text="필요할 때 꺼내 쓰는 통장 · 공시일 빌린 돈 0" />
    </P>
  );
};

// ───── 7b. 면적 원 50 vs 300 + 현금 카드 ─────
const Circles: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <AreaCircles cx={760} cy={520} a={d.old} b={d.new} R={230} p={appear(f, 20, 30)} la="옛 한도(2023년, 해지)" lb="새 한도 합계" />
      <Chip x={180} y={280} o={appear(f, A(s, 1))} text={`넓이로 ${d.new / d.old}배`} size={40} />
      <Card x={1360} y={300} w={480} h={230} o={appear(f, A(s, 2))}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink3, padding: '28px 34px 0'}}>6월 말 현금+단기투자</div>
        <div style={{...F, fontWeight: 700, fontSize: 64, color: T.ink, padding: '4px 34px'}}>{n0(d.cash)}</div>
        <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3, padding: '0 34px'}}>백만 달러</div></Card>
      <Card x={1360} y={570} w={480} h={150} o={appear(f, A(s, 3))} bg={T.soft}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink, padding: '30px 34px 0'}}>어디에 쓸지: 공시 없음</div>
        <div style={{...F, fontWeight: 500, fontSize: 26, color: T.ink2, padding: '6px 34px'}}>짐작하지 않습니다</div></Card>
    </P>
  );
};

// ───── 8. 5년 주가 선 + 최대 낙폭 음영 + 표시점 ─────
const Price5: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const p = s.data; const X0 = 200, X1 = 1480, Y0 = 800, Y1 = 260; const v: number[] = p.v; const n = v.length;
  const x = scaleLinear().domain([0, n - 1]).range([X0, X1]); const y = scaleLinear().domain([0, Math.max(...v) * 1.1]).range([Y0, Y1]);
  const m = Math.max(2, Math.round(n * appear(f, 6, 60))); const d = d3line<number>().x((_, i) => x(i)).y((q) => y(q)).curve(curveMonotoneX)(v.slice(0, m)) || '';
  const ar = d3area<number>().x((_, i) => x(i)).y0(Y0).y1((q) => y(q)).curve(curveMonotoneX)(v.slice(0, m)) || '';
  const k1 = appear(f, A(s, 1)), k2 = appear(f, A(s, 2)), k3 = appear(f, A(s, 3)), k4 = appear(f, A(s, 4));
  const md = (s2: string) => `${s2.slice(0, 4)}.${+s2.slice(4, 6)}`;
  const dot = (i: number, val: number, lab: string, o: number, c: string, dy = -24, anc: 'start' | 'middle' | 'end' = 'middle') => <g opacity={o}><circle cx={x(i)} cy={y(val)} r={12} fill={c} />
    <text x={x(i) + (anc === 'start' ? -10 : anc === 'end' ? 10 : 0)} y={y(val) + dy} textAnchor={anc} stroke={T.bg} strokeWidth={10} paintOrder="stroke" fontFamily="PD" fontWeight={700} fontSize={30} fill={c}>{lab}</text></g>;
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {[0, 100, 200, 300, 400, 500].map((g) => <g key={g}><line x1={X0} x2={X1} y1={y(g)} y2={y(g)} stroke={T.line} strokeWidth={2} />
          <text x={X0 - 16} y={y(g) + 9} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{`$${g}`}</text></g>)}
        <rect x={x(p.i.mf)} y={Y1} width={(x(p.i.mt) - x(p.i.mf)) * k4} height={Y0 - Y1} fill={T.fall} opacity={0.16} />
        <path d={ar} fill={T.line} opacity={0.6} />
        <path d={d} stroke={T.ink} strokeWidth={5} fill="none" strokeLinejoin="round" />
        {[0, Math.round((n - 1) / 5), Math.round((n - 1) * 2 / 5), Math.round((n - 1) * 3 / 5), Math.round((n - 1) * 4 / 5), n - 1].map((i) =>
          <text key={i} x={x(i)} y={Y0 + 36} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{md(p.d[i])}</text>)}
        {dot(n - 1, p.last[1], `$${p.last[1]}`, k1, T.accent, 56, 'end')}
        {dot(p.i.y1, p.y1[1], `1년 전 $${p.y1[1]}`, k1, T.ink2, -36, 'end')}
        {dot(0, p.y5[1], `5년 전 $${p.y5[1].toFixed(2)}`, k2, T.ink2, 56, 'start')}
        {dot(p.i.peak, p.peak[1], `최고 $${p.peak[1]}`, k3, T.rise, -30)}
      </svg>
      {[[k1, '9월 30일 종가', `$${p.last[1]}`, T.daccent, ''], [k2, '5년 전(분할 반영)', `$${p.y5[1].toFixed(2)}`, T.dink, ''],
        [k3, '최고 종가 대비 지금', `${p.from_peak}%`, T.dfall, ''], [k4, '5년 중 최대 낙폭', `${p.mdd.pct}%`, T.dfall, `${md(p.mdd.from)} → ${md(p.mdd.to)}`]].map(([o, lab, val, c, sub]: any, i: number) =>
        <Card key={i} x={1530} y={250 + i * 150} w={340} h={140} o={o} bg={T.ink}>
          <div style={{...F, fontWeight: 700, fontSize: 22, color: T.dink3, padding: '18px 26px 0'}}>{lab}</div>
          <div style={{...F, fontWeight: 700, fontSize: 52, color: c, padding: '0 26px', lineHeight: 1.15}}>{val}</div>{sub ? <div style={{...F, fontWeight: 500, fontSize: 20, color: T.dink3, padding: '0 26px'}}>{sub}</div> : null}</Card>)}
    </P>
  );
};

// ───── 9. 은퇴 나이 — 가정 카드 → 35세 막대 3 → 50세 막대 3 ─────
const Age2: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const base = 750; const y = scaleLinear().domain([0, 70]).range([0, 330]);
  const asm = appear(f, A(s, 1)) * (1 - appear(f, A(s, 2)));
  const g = (k: number) => ({first: appear(f, A(s, 2 + k * 2)), rest: appear(f, A(s, 3 + k * 2))});
  return (
    <P s={s}>
      <Card x={300} y={300} w={1320} h={300} o={asm}>
        {[['수익률', '연 5%'], ['물가', '연 3%'], ['국민연금', '65세부터 월 100만원']].map(([k, v], i) => <div key={k} style={{display: 'flex', justifyContent: 'space-between', padding: '0 60px', height: 90, alignItems: 'center', borderBottom: i < 2 ? `2px solid ${T.line}` : 'none', marginTop: i ? 0 : 15}}>
          <span style={{...F, fontWeight: 500, fontSize: 38, color: T.ink2}}>{k}</span><span style={{...F, fontWeight: 700, fontSize: 44, color: T.ink}}>{v}</span></div>)}
      </Card>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {d.groups.map((gr: any, k: number) => { const o = g(k); const x0 = 220 + k * 820; const all = Math.max(o.first, o.rest);
          return <g key={k} opacity={all}>
            <text x={x0} y={350} fontFamily="PD" fontWeight={700} fontSize={36} fill={T.ink}>{gr.who}</text>
            <line x1={x0 - 10} x2={x0 + 680} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} />
            {gr.ages.map((a: number, i: number) => { const oo = i === 0 ? o.first : o.rest; const h = y(a) * oo; const late = a - gr.ages[0];
              return <g key={i} opacity={Math.min(1, oo * 2)}>
                <rect x={x0 + i * 230} y={base - h} width={180} height={h} rx={8} fill={i === 0 ? T.accent : i === 2 ? T.ink : T.line} />
                <text x={x0 + i * 230 + 90} y={base - h - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={48} fill={i === 0 ? T.accent : T.ink}>{a}세</text>
                <text x={x0 + i * 230 + 90} y={base + 40} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2}>{d.labels[i]}</text>
                {late > 0 ? <text x={x0 + i * 230 + 90} y={base - h + 50} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={32} fill={i === 2 ? '#fff' : T.ink}>{`+${late}년`}</text> : null}
              </g>; })}
          </g>; })}
      </svg>
      <Chip x={110} y={232} right o={appear(f, A(s, 6))} text="모은 돈이 크고 남은 시간이 짧을수록 더 크게 움직인다" size={30} />
    </P>
  );
};

// ───── 10. 두 칸 정리(장부에 있음 / 없음) → 다음 분기 세 칸 ─────
const Check2: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const nx = appear(f, A(s, 4)); const disc = appear(f, A(s, 5)); const cta = appear(f, A(s, 6));
  const yo = (i: number) => appear(f, i < 2 ? A(s, 1) + i * 20 : A(s, 2) + (i - 2) * 16);
  return (
    <P s={s}>
      <div style={{opacity: 1 - nx}}>
        <div style={{...F, position: 'absolute', left: 200, top: 240, fontWeight: 700, fontSize: 36, color: T.ink}}>장부에 있음</div>
        {d.yes.map((t: string, i: number) => <div key={t} style={{...F, position: 'absolute', left: 200, top: 330 + i * 100, fontWeight: 700, fontSize: 42, color: T.ink, opacity: yo(i), display: 'flex', gap: 18, alignItems: 'center'}}>
          <span style={{width: 40, height: 40, borderRadius: 10, background: T.ink, color: '#fff', fontSize: 28, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>✓</span>{t}</div>)}
        <div style={{...F, position: 'absolute', left: 1180, top: 240, fontWeight: 700, fontSize: 36, color: T.ink3, opacity: appear(f, A(s, 3))}}>장부에 없음 · 숫자 없음</div>
        {d.no.map((t: string, i: number) => <div key={t} style={{...F, position: 'absolute', left: 1180, top: 330 + i * 100, fontWeight: 700, fontSize: 42, color: T.ink2, opacity: appear(f, A(s, 3) + i * 20), display: 'flex', gap: 18, alignItems: 'center'}}>
          <span style={{width: 40, height: 40, borderRadius: 10, border: `3px dashed ${T.ink3}`, boxSizing: 'border-box'}} />{t}</div>)}
      </div>
      <div style={{...F, position: 'absolute', left: 200, top: 260, fontWeight: 700, fontSize: 44, color: T.ink, opacity: nx}}>다음 분기 보고서에서 볼 세 칸</div>
      {d.next.map((t: string, i: number) => <Card key={t} x={200 + i * 540} y={380} w={480} h={300} o={appear(f, A(s, 4) + i * 16)}>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink3, padding: '44px 40px 0'}}>{`칸 ${i + 1}`}</div>
        <div style={{...F, fontWeight: 700, fontSize: 72, color: T.ink, padding: '10px 40px'}}>{t}</div></Card>)}
      <Chip x={200} y={760} o={disc * (1 - cta)} text="투자 권유 아님 · 공개 자료 정리 · 출처는 설명란" dark={false} size={30} />
      <Chip x={200} y={760} o={cta} text="설명란 계산기: 내 나이·모은 돈 넣고 −27.6%·−73.6% 적용해 보기" size={32} />
    </P>
  );
};

const Bullets: React.FC<S> = ({s}) => {
  const f = useCurrentFrame();
  return (
    <P s={s}>
      {s.lines.slice(0, 6).map((l, i) => <div key={i} style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, position: 'absolute', left: 200, right: 200, top: 250 + i * 95,
        opacity: appear(f, at(s, i)), wordBreak: 'keep-all'}}>{l.text.length > 46 ? l.text.slice(0, 46) + '…' : l.text}</div>)}
    </P>
  );
};

const View: React.FC<S> = ({s}) => {
  switch (s.kind) {
    case 'open': return <Open s={s} />; case 'logo': return <LogoSting sub={s.data.sub} />; case 'agenda': return <Agenda s={s} />;
    case 'ledger': return <Ledger s={s} />; case 'yoy': return <Yoy s={s} />; case 'pretax': return <Pretax s={s} />;
    case 'mix': return <Mix s={s} />; case 'slope': return <Slope s={s} />; case 'stairs': return <StairsV s={s} />; case 'credit': return <Credit s={s} />;
    case 'waterfall': return <WaterfallV s={s} />; case 'rd10': return <Rd10 s={s} />; case 'capex': return <Capex s={s} />; case 'cash': return <Cash s={s} />;
    case 'facility': return <Facility s={s} />; case 'circles': return <Circles s={s} />; case 'price5': return <Price5 s={s} />; case 'age2': return <Age2 s={s} />;
    case 'check2': return <Check2 s={s} />;
    default: return <Bullets s={s} />;
  }
};

export const E2: React.FC<E2Props> = ({scenes, rail}) => {
  let acc = 0;
  return (
    <RailCtx.Provider value={rail}>
      <AbsoluteFill style={{background: T.bg}}>
        <style>{FONT_CSS}</style>
        {scenes.map((s, i) => {
          const from = acc; acc += s.frames; let a = 6;
          return (
            <Sequence key={i} from={from} durationInFrames={s.frames}>
              <View s={s} />
              {s.lines.map((l, j) => { const st = a; a += l.frames;
                return l.audio ? <Sequence key={j} from={st} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null; })}
            </Sequence>
          );
        })}
      </AbsoluteFill>
    </RailCtx.Provider>
  );
};
