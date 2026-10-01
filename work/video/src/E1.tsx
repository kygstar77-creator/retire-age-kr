// E-1 "메모리 3사 — 이익은 몇 배, 주가는 얼마나 흔들렸나" — 재료: work/video/e1.json(ep/E-1/e1props.py가 script.md·voice.json·원자료로 만든다)
// 장면 종류 20가지(10/1 v1 추가: 마이크론 8분기 큰 막대·전망 범위 띠·사업부 전후 막대·삼성 DS 반기 vs 연간+도넛·SK 계단·원문 카드 2장·저울·전망 점선 막대 / 선+낙폭 음영·목록·같은 출발점 선·낙폭 막대+달력 띠·작은 막대 3폭·이익률 선·쌍 막대·카운터+표·원문 카드+범위 띠·일정 카드·
// 입력 카드·나이 막대·정리 표). 숫자는 전부 e1.json에서 온다(코드 안에는 눈금·배치 값만). 단계 시점은 data.at(문장 번호, 못 찾으면 −1=안 나옴).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {line as d3line, curveMonotoneX} from 'd3-shape';
import {T, F, CL, FONT_CSS, VScene, at, appear, HandCircle, CountUp, Caption, Page, LogoSting, ProgressRail} from './parts/fm';
import {BarSeries, RangeDot, PairBars, Donut, Seesaw, QuoteCard, Stairs} from './parts/charts';

export type E1Props = {fps: number; scenes: VScene[]; missing: number; holes: number};
export const e1Frames = (p: E1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: VScene};
const NEVER = 1e9;
const A = (s: VScene, k: number) => (s.data.at?.[k] ?? -1) < 0 ? NEVER : at(s, s.data.at[k]);
// 회사는 색이 아니라 이름표·선 모양으로 가른다(guide ③: 주황=파이어맵 숫자, 빨강/파랑=등락만) — 2026-10-01 motion 감사
const CO: Record<string, string> = {'마이크론': T.ink, 'SK하이닉스': T.ink2, '삼성전자': T.ink3};
const DASH: Record<string, string | undefined> = {'SK하이닉스': '14 9', '삼성전자': '3 9'};
const RAIL = ['1년 주가·낙폭', '여덟 분기 매출', '이익률', '주가 vs 이익', '회사가 적은 위험'];
const md = (d: string) => `${+d.slice(4, 6)}/${+d.slice(6, 8)}`;
const Card: React.FC<{x: number; y: number; w: number; h: number; o?: number; bg?: string; children?: React.ReactNode}> = ({x, y, w, h, o = 1, bg = T.surface, children}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: bg, borderRadius: 20, opacity: o}}>{children}</div>
);
const P: React.FC<S & {children: React.ReactNode}> = ({s, children}) => (
  <Page s={{...s, rail: 0}}>{s.rail ? <ProgressRail n={5} cur={s.rail} labels={RAIL} on={T.ink} /> : null}{children}</Page>
);

// ───── 0. 여는 장면: SK하이닉스 1년 선 + 고점→저점 음영 + 두 숫자 ─────
const Open: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const p = s.data.p;
  const X0 = 150, X1 = 1160, Y0 = 790, Y1 = 250;
  const x = scaleLinear().domain([0, p.v.length - 1]).range([X0, X1]); const y = scaleLinear().domain([0, Math.max(...p.v) * 1.05]).range([Y0, Y1]);
  const draw = appear(f, 4, 70); const n = Math.max(2, Math.round(p.v.length * draw));
  const path = d3line<number>().x((_, i) => x(i)).y((v) => y(v)).curve(curveMonotoneX)(p.v.slice(0, n)) || '';
  const ip = p.d.findIndex((d: string) => d >= p.peak), it = p.d.findIndex((d: string) => d >= p.trough);
  const up = appear(f, 50), dn = appear(f, A(s, 1)), q4 = appear(f, A(s, 3)), qs = appear(f, A(s, 4));
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={X0} x2={X1} y1={y(100)} y2={y(100)} stroke={T.dink3} strokeWidth={2} strokeDasharray="8 8" />
        <text x={X0} y={y(100) + 36} fontFamily="PD" fontWeight={500} fontSize={24} fill={T.dink3}>{`${md(p.first[0])} 출발 = 100`}</text>
        <rect x={x(ip)} y={Y1 - 20} width={(x(it) - x(ip)) * dn} height={Y0 - Y1 + 20} fill={T.fall} opacity={0.28} />
        <path d={path} stroke={T.dink} strokeWidth={6} fill="none" strokeLinejoin="round" />
        <text x={X1} y={Y0 + 44} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.dink3}>{md(p.last[0])}</text>
        <g opacity={dn}><text x={(x(ip) + x(it)) / 2} y={Y1 - 34} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.dfall}>{`${md(p.peak)} → ${md(p.trough)}`}</text></g>
      </svg>
      <div style={{position: 'absolute', left: 1230, top: 230, opacity: up}}>
        <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink3}}>{s.data.name} 1년</div>
        <div style={{...F, fontWeight: 700, fontSize: 128, color: T.rise, lineHeight: 1.1}}>+<CountUp to={p.ret} p={up} digits={1} />%</div>
      </div>
      <div style={{position: 'absolute', left: 1230, top: 500, opacity: dn}}>
        <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink3}}>그 안의 최대 낙폭</div>
        <div style={{...F, fontWeight: 700, fontSize: 128, color: T.dfall, lineHeight: 1.1}}><CountUp to={p.dd} p={dn} digits={1} />%</div>
      </div>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.dink, position: 'absolute', left: 1230, top: 740, opacity: Math.max(q4, qs), background: T.dsurface, borderRadius: 16, padding: '14px 24px', whiteSpace: 'nowrap'}}>
        {qs > q4 ? '이익은 주가만큼 늘었을까?' : (s.data.q4 || '+ 마이크론 회계 4분기 실적')}</div>
      <div style={{...F, fontWeight: 500, fontSize: 22, color: T.dink3, position: 'absolute', left: 120, bottom: 20}}>출처 {s.source}</div>
      <Caption s={s} dark />
    </AbsoluteFill>
  );
};

// ───── 1. 오늘 볼 다섯 가지 ─────
const Agenda: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const items: string[] = s.data.items; const b = A(s, 1);
  return (
    <P s={s}>
      {items.map((t, i) => { const o = appear(f, (b === NEVER ? 30 : b) + i * 22);
        return (
          <div key={t} style={{position: 'absolute', left: 200, top: 240 + i * 112, display: 'flex', alignItems: 'center', gap: 34, opacity: o, transform: `translateX(${(1 - o) * -30}px)`}}>
            <div style={{width: 84, height: 84, borderRadius: 20, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <span style={{...F, fontWeight: 700, fontSize: 48, color: '#fff'}}>{i + 1}</span></div>
            <span style={{...F, fontWeight: 700, fontSize: 58, color: T.ink}}>{t}</span>
          </div>); })}
      <div style={{...F, fontWeight: 700, fontSize: 42, color: T.accent, position: 'absolute', left: 1160, top: 470, padding: '24px 36px', background: T.soft, borderRadius: 20,
        opacity: appear(f, A(s, 2))}}>{s.data.extra}</div>
    </P>
  );
};

// ───── 2. 같은 출발점 100 선 3개 → 낙폭 막대 + 달력 띠 ─────
const Price: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cos = s.data.cos; const sw = A(s, 3);
  const lo = interpolate(f, [sw, sw + 12], [1, 0], CL), ddo = appear(f, sw + 6);
  const X0 = 230, X1 = 1400, Y0 = 810, Y1 = 250; const n = cos[0].v.length;
  const x = scaleLinear().domain([0, n - 1]).range([X0, X1]); const y = scaleLinear().domain([0, 700]).range([Y0, Y1]);
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute', opacity: lo}}>
        {[100, 300, 500, 700].map((g) => <g key={g}><line x1={X0} x2={X1} y1={y(g)} y2={y(g)} stroke={T.line} strokeWidth={2} />
          <text x={X0 - 16} y={y(g) + 9} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{g}</text></g>)}
        {cos.map((c: any, i: number) => {
          const st = A(s, i) === NEVER ? 20 + i * 40 : A(s, i); const p = appear(f, st, 40); const m = Math.max(2, Math.round(c.v.length * p));
          const d = d3line<number>().x((_, j) => x(j)).y((v) => y(v)).curve(curveMonotoneX)(c.v.slice(0, m)) || '';
          const end = c.v[m - 1];
          return <g key={c.name} opacity={Math.min(1, p * 3)}>
            <path d={d} stroke={CO[c.name]} strokeWidth={5} strokeDasharray={DASH[c.name]} fill="none" strokeLinejoin="round" />
            <text x={x(m - 1) + 14} y={y(end) + 10} fontFamily="PD" fontWeight={700} fontSize={32} fill={c.name === '마이크론' ? T.ink : T.ink2}>{`${c.name} ${end}`}</text></g>;
        })}
        <text x={X0} y={Y0 + 42} fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{md(cos[0].d[0])}</text>
        <text x={X1} y={Y0 + 42} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{md(cos[0].d[n - 1])}</text>
      </svg>
      <div style={{opacity: ddo}}>
        {[4, 5, 6].map((k, i) => { const c = cos[[0, 2, 1][i]]; const o = appear(f, A(s, k) === NEVER ? sw + 20 + i * 30 : A(s, k), 20); const W = 900 * Math.abs(c.dd) / 60;
          return <div key={c.name} style={{position: 'absolute', left: 200, top: 250 + i * 150, opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink, width: 260, position: 'absolute', top: 18}}>{c.name}</div>
            <div style={{position: 'absolute', left: 270, top: 6, width: W * o, height: 76, borderRadius: 12, background: T.fall, opacity: c.name === 'SK하이닉스' ? 1 : 0.45}} />
            <div style={{...F, fontWeight: 700, fontSize: 48, color: T.fall, position: 'absolute', left: 290 + W, top: 14, whiteSpace: 'nowrap'}}>{c.dd}%</div>
          </div>; })}
        <DateBand s={s} cos={cos} start={A(s, 7)} />
      </div>
    </P>
  );
};
// 6~8월 달력 띠: 세 회사의 고점→저점 구간이 같은 여름에 겹친다
const DateBand: React.FC<{s: VScene; cos: any[]; start: number}> = ({cos, start}) => {
  const f = useCurrentFrame(); const o = appear(f, start === NEVER ? NEVER : start, 18);
  const X0 = 470, X1 = 1500; const day = (d: string) => (+d.slice(4, 6) - 6) * 30.5 + +d.slice(6, 8); const x = scaleLinear().domain([1, 92]).range([X0, X1]);
  return (
    <div style={{position: 'absolute', left: 0, top: 740, width: 1920, opacity: o}}>
      {['6월', '7월', '8월'].map((m, i) => <div key={m} style={{...F, fontWeight: 700, fontSize: 26, color: T.ink3, position: 'absolute', left: x(1 + i * 30.5), top: 0}}>{m}</div>)}
      {cos.map((c, i) => <div key={c.name} style={{position: 'absolute', left: x(day(c.peak)), top: 40 + i * 30, width: x(day(c.trough)) - x(day(c.peak)), height: 22, borderRadius: 6, background: CO[c.name]}} />)}
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, position: 'absolute', left: 200, top: 50}}>고점 → 저점</div>
    </div>
  );
};

// ───── 3a. 마이크론 여덟 분기 매출 — 큰 막대 하나(1년 전 테두리) + 14주 꼬리표 ─────
const Mu8: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const p = appear(f, 8, 40); const b = appear(f, A(s, 2)); const w = appear(f, A(s, 3));
  return (
    <P s={s}>
      <BarSeries x={240} y={800} w={1180} h={470} vals={d.rev} labels={d.q} p={p} color={T.ink} hi={[7]} ring={[3]} />
      <div style={{...F, position: 'absolute', left: 1480, top: 300, opacity: b}}>
        <div style={{fontWeight: 700, fontSize: 34, color: T.ink3}}>1년 전 같은 분기의</div>
        <div style={{fontWeight: 700, fontSize: 120, color: T.ink, lineHeight: 1.1}}><CountUp to={d.revx} p={b} digits={2} />배</div></div>
      <div style={{...F, position: 'absolute', left: 1480, top: 560, opacity: w, background: T.surface, borderRadius: 16, padding: '20px 26px', width: 400}}>
        <div style={{fontWeight: 700, fontSize: 34, color: T.ink}}>{`이번 분기 ${d.weeks[0]}주`}</div>
        <div style={{fontWeight: 500, fontSize: 28, color: T.ink2, marginTop: 6}}>{`1년 전 분기 ${d.weeks[1]}주 — 한 주 더`}</div>
        <div style={{fontWeight: 500, fontSize: 22, color: T.ink3, marginTop: 6}}>분기 끝 날짜로 계산</div></div>
    </P>
  );
};

// ───── 3b. 회사 전망(6월) 범위 띠 위에 실제 매출 점 ─────
const Guide: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <RangeDot x0={260} x1={1660} y={580} dom={[460, 560]} lo={d.lo} hi={d.hi} act={d.act} pBand={appear(f, 10, 20)} pDot={appear(f, 50, 30)} unit="억$"
        bandLabel="회사 전망(2026년 6월)" actLabel={`실제 ${d.act.toFixed(1)}억$`} />
    </P>
  );
};

// ───── 3c. 마이크론 사업부 4개 — 1년 전 vs 이번 분기 ─────
const Seg: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows = s.data.rows;
  return (
    <P s={s}>
      <PairBars x={200} y={280} w={960} rows={rows} p={rows.map((_: any, i: number) => appear(f, 8 + i * 14, 24))} hi={0} tags={['1년 전 같은 분기', '이번 분기']} />
    </P>
  );
};

// ───── 3e. 삼성전자 DS 부문 — 2025년 12개월 vs 2026년 상반기 6개월 + 97.4% 도넛 ─────
const DsDx: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const pa = appear(f, A(s, 2) === NEVER ? 10 : A(s, 2), 24), pb = appear(f, A(s, 1) === NEVER ? 10 : A(s, 1), 24);
  const po = appear(f, A(s, 3), 24), dn = appear(f, A(s, 4), 30);
  const jo = (v: number) => `${Math.floor(v / 10000)}조 ${(v % 10000).toLocaleString()}억`;
  const grp = (x: number, title: string, a: number, b: number, qa: number, qb: number, mult: string) => {
    const mx = Math.max(a, b) * 1.1; const H = 400, base = 800;
    return <g>
      <text x={x + 170} y={290} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={38} fill={T.ink}>{title}</text>
      <rect x={x} y={base - (a / mx) * H * qa} width={150} height={(a / mx) * H * qa} rx={8} fill={T.line} stroke={T.ink3} strokeWidth={2} />
      <rect x={x + 190} y={base - (b / mx) * H * qb} width={150} height={(b / mx) * H * qb} rx={8} fill={T.ink} />
      <text x={x + 75} y={base - (a / mx) * H * qa - 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink} opacity={qa}>{jo(a)}</text>
      <text x={x + 265} y={base - (b / mx) * H * qb - 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink} opacity={qb}>{jo(b)}</text>
      <text x={x + 75} y={base + 36} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink2}>2025년 12개월</text>
      <text x={x + 265} y={base + 36} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink}>2026년 상반기 6개월</text>
      <g opacity={Math.min(qa, qb)}><rect x={x + 90} y={310} width={160} height={56} rx={28} fill={T.ink} />
        <text x={x + 170} y={349} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={32} fill="#fff">{mult}</text></g>
    </g>;
  };
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={180} x2={1320} y1={800} y2={800} stroke={T.ink3} strokeWidth={2} />
        {grp(200, 'DS 매출', d.rev[0], d.rev[1], pa, pb, `${(d.rev[1] / d.rev[0]).toFixed(2)}배`)}
        {grp(800, 'DS 영업이익', d.op[0], d.op[1], po, po, `${(d.op[1] / d.op[0]).toFixed(2)}배`)}
      </svg>
      <Donut cx={1600} cy={500} r={150} v={d.share} p={dn} label="회사 영업이익 중 DS 몫" />
    </P>
  );
};

// ───── 3f. SK하이닉스 해마다 매출 계단 ─────
const StairsV: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <Stairs x={300} y={820} w={1300} h={440} rows={d.rows} p={d.rows.map((_: any, i: number) => appear(f, 6 + i * 16, 24))} tag={`반년 만에 작년의 ${d.x}배`} tagP={appear(f, 70)}
        fmt={(v) => `${Math.floor(v / 10000)}조 ${(v % 10000).toLocaleString()}억`} />
    </P>
  );
};

// ───── 3-1a. 원문 카드 2장(삼성 +220%, SK하이닉스 D램·낸드) ─────
const Quotes2: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const c = s.data.cards;
  return (
    <P s={s}>
      {c.map(([src, body, big]: string[], i: number) => <QuoteCard key={i} x={200 + i * 800} y={260} w={740} h={470} o={appear(f, A(s, i + 1) === NEVER ? 10 + i * 40 : A(s, i + 1), 18)} src={src} body={body} big={big} />)}
    </P>
  );
};

// ───── 3-1b. 저울 — 파는 쪽 DS vs 사는 쪽 DX ─────
const Scale: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const tilt = appear(f, A(s, 2), 36); const mid = appear(f, A(s, 1), 20); const note = appear(f, A(s, 4), 20);
  const jo = (v: number) => `${Math.floor(v / 10000)}조 ${(v % 10000).toLocaleString()}억원`;
  return (
    <P s={s}>
      <Seesaw cx={960} cy={470} L={['DS(메모리 파는 쪽)', jo(d.op[1])]} R={['DX(메모리 사는 쪽)', jo(d.dx_op[1])]} ratio={1} p={tilt}
        mid={['메모리 판매가격 +220%', '모바일 메모리 매입가 +211%']} midP={mid} />
      <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2, position: 'absolute', right: 140, top: 236, background: T.surface, borderRadius: 14, padding: '12px 22px', opacity: tilt}}>
        {`DX 몫 ${d.dx_share}% · 작년 한 해 DX ${jo(d.dx_op[0])}`}</div>
      <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink3, position: 'absolute', right: 150, top: 580, opacity: note}}>DX 이익 감소가 메모리 값 때문인지는 보고서로 나눌 수 없음</div>
    </P>
  );
};

// ───── 8a. 마이크론 분기 매출 + 다음 분기 회사 전망(점선·오차 막대) ─────
const Outlook: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s}>
      <BarSeries x={240} y={800} w={1400} h={460} vals={d.rev} labels={d.q} p={appear(f, 4, 30)} color={T.ink} hi={[7]} est={[d.next, d.pm]} estP={appear(f, 40, 30)} estLabel="다음 분기 전망" />
      <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2, position: 'absolute', left: 240, top: 250, background: T.line, borderRadius: 14, padding: '10px 22px', opacity: appear(f, A(s, 1))}}>
        다음 실적 발표 날짜: 보도자료에 없음</div>
    </P>
  );
};

// ───── 3d. 세 회사 여덟 분기 매출 — 작은 막대 3폭 ─────
const Revenue: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cos = s.data.cos; const W = 500, gap = 60, x0 = 200;
  return (
    <P s={s}>
      {cos.map((c: any, k: number) => {
        const st = A(s, k === 0 ? 0 : k + 1); const o = appear(f, st === NEVER ? 20 + k * 30 : st, 30); const mx = Math.max(...c.rev);
        const bw = W / 8 - 12; const H = 380, base = 800;
        return (
          <div key={c.name} style={{position: 'absolute', left: x0 + k * (W + gap), top: 0, width: W, height: 1080, opacity: Math.max(appear(f, 6 + k * 8), 0)}}>
            <div style={{...F, fontWeight: 700, fontSize: 38, color: T.ink, position: 'absolute', top: 240}}>{c.name}</div>
            <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', top: 290}}>{c.unit}</div>
            <svg width={W} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
              {c.rev.map((v: number, i: number) => { const h = (v / mx) * H * o; const last = i === 7, yago = i === 3;
                return <g key={i}>
                  <rect x={i * (W / 8)} y={base - h} width={bw} height={h} rx={6} fill={last ? T.ink : T.line} stroke={yago ? T.ink : 'none'} strokeWidth={yago ? 4 : 0} />
                  <text x={i * (W / 8) + bw / 2} y={base + 30} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={18} fill={T.ink3}>{c.q[i]}</text>
                  {last || yago ? <text opacity={o} x={i * (W / 8) + bw / 2} y={base - h - 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={last ? 30 : 24} fill={T.ink}>{v.toLocaleString()}</text> : null}
                </g>; })}
            </svg>
            <div style={{...F, fontWeight: 700, fontSize: 32, color: '#fff', background: T.ink, borderRadius: 30, padding: '4px 20px', position: 'absolute', top: 325, opacity: appear(f, (st === NEVER ? 20 : st) + 40)}}>
              1년 전의 {c.revx.toFixed(2)}배</div>
          </div>
        );
      })}
      <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, position: 'absolute', left: 1320 + 110, top: 284, background: T.line, borderRadius: 12, padding: '4px 14px', opacity: appear(f, A(s, 4))}}>
        회사 전체(스마트폰·가전 포함)</div>
    </P>
  );
};

// ───── 4. 이익률 선 3개(8분기) ─────
const Margin: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cos = s.data.cos; const X0 = 240, X1 = 1330, Y0 = 820, Y1 = 250;
  const x = scaleLinear().domain([0, 8]).range([X0, X1]); const y = scaleLinear().domain([0, 100]).range([Y0, Y1]);
  const order = [0, 2, 3]; const ser = (c: any) => (c.margin9 || c.margin) as number[];
  const coin = appear(f, A(s, 1), 20); const back = appear(f, A(s, 4), 24);
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {[0, 20, 40, 60, 80, 100].map((g) => <g key={g}><line x1={X0} x2={X1} y1={y(g)} y2={y(g)} stroke={T.line} strokeWidth={2} />
          <text x={X0 - 16} y={y(g) + 9} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{g}%</text></g>)}
        {cos.map((c: any, k: number) => { const st = A(s, order[k]); const p = appear(f, st === NEVER ? 20 + k * 30 : st, 36); const M = ser(c); const N = M.length; const m = Math.max(2, Math.round(N * p));
          const d = d3line<number>().x((_, i) => x(i)).y((v) => y(v)).curve(curveMonotoneX)(M.slice(0, m)) || '';
          return <g key={c.name} opacity={Math.min(1, p * 3)}>
            <path d={d} stroke={CO[c.name]} strokeWidth={c.name === '마이크론' ? 7 : 5} strokeDasharray={DASH[c.name]} fill="none" />
            {[N - 5, N - 1].filter((i) => i < m).map((i) => <g key={i}><circle cx={x(i)} cy={y(M[i])} r={9} fill={CO[c.name]} />
              {i === N - 5 ? <text x={x(i)} y={y(M[i]) + (c.name === '마이크론' ? -22 : 44)} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={c.name === '마이크론' ? T.ink : T.ink2}>{M[i]}%</text> : null}</g>)}
            {m === N ? <text x={x(N - 1) + 22} y={y(M[N - 1]) + 12 + (c.name === 'SK하이닉스' ? 20 : c.name === '마이크론' ? -16 : 0)} fontFamily="PD" fontWeight={700} fontSize={32} fill={c.name === '마이크론' ? T.ink : T.ink2}>{`${c.name} ${M[N - 1]}%`}</text> : null}
          </g>; })}
        {(cos[0].q9 || cos[0].q).map((q: string, i: number) => <text key={i} x={x(i)} y={Y0 + 34} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={20} fill={T.ink}>{q}</text>)}
        {cos[1].q.map((q: string, i: number) => <text key={'k' + i} x={x(i)} y={Y0 + 60} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={18} fill={T.ink3}>{q}</text>)}
        <g opacity={back}><HandCircle cx={x(0)} cy={y(ser(cos[0])[0])} rx={60} ry={40} p={back} />
          <text x={X0 + 20} y={Y1 + 60} fontFamily="PD" fontWeight={700} fontSize={32} fill={T.ink}>{`마이크론 ${ser(cos[0])[0]}% (${(cos[0].q9 || cos[0].q)[0]}) → ${ser(cos[0]).slice(-1)[0]}%`}</text></g>
      </svg>
      <Card x={1540} y={600} w={340} h={200} o={coin}>
        <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink, padding: '34px 30px', lineHeight: 1.4}}>100원 팔면<br /><span style={{fontSize: 56}}>약 80원</span> 남음</div>
      </Card>
    </P>
  );
};

// ───── 5. 영업이익 몇 배 vs 주가 몇 배 — 쌍 막대 ─────
const Twin: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows = s.data.rows; const base = 700, H = 420, mx = Math.max(...rows.map((r: number[]) => r[1] as number)) * 1.08;
  const pb = A(s, 3); const gapN = appear(f, A(s, 4));
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={220} x2={1700} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} />
        {rows.map(([name, opx, px]: [string, number, number], i: number) => {
          const cx = 360 + i * 500; const o1 = appear(f, A(s, i) === NEVER ? 20 + i * 30 : A(s, i), 24); const o2 = appear(f, pb === NEVER ? 200 : pb + i * 10, 24);
          const h1 = (opx / mx) * H * o1, h2 = (px / mx) * H * o2;
          return <g key={name}>
            <rect x={cx} y={base - h1} width={140} height={h1} rx={8} fill={T.ink} opacity={Math.min(1, o1 * 3)} />
            <text x={cx + 70} y={base - h1 - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={44} fill={T.ink} opacity={o1}>{opx.toFixed(2)}배</text>
            <rect x={cx + 160} y={base - h2} width={140} height={h2} rx={8} fill={T.line} stroke={T.ink2} strokeWidth={3} opacity={Math.min(1, o2 * 3)} />
            <text x={cx + 230} y={base - h2 - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.ink2} opacity={o2}>{px.toFixed(2)}배</text>
            <text x={cx + 150} y={base + 50} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={36} fill={T.ink}>{name}</text>
            <text x={cx + 70} y={base + 86} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>영업이익</text>
            <text x={cx + 230} y={base + 86} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3} opacity={o2}>주가 1년</text>
          </g>; })}
        <g opacity={gapN}><HandCircle cx={1360 + 150} cy={base - 230} rx={250} ry={290} p={gapN} /></g>
      </svg>
      <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, position: 'absolute', left: 1180, top: 150, background: T.line, borderRadius: 14, padding: '10px 20px', opacity: appear(f, A(s, 5))}}>
        이익은 분기, 주가는 1년 — 같은 구간 아님</div>
    </P>
  );
};

// ───── 6. Form 4 — 카운터 두 개 → 상위 4줄 표 ─────
const Form4: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = appear(f, A(s, 1), 36), c2 = appear(f, A(s, 2)), tb = appear(f, A(s, 3)), plan = appear(f, A(s, 4));
  return (
    <P s={s}>
      <Card x={200} y={250} w={700} h={260} o={c1}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, padding: '26px 40px 0'}}>공개시장 매도</div>
        <div style={{...F, fontWeight: 700, fontSize: 110, color: T.ink, padding: '0 40px', lineHeight: 1.1}}><CountUp to={d.n} p={c1} />건</div>
        <div style={{...F, fontWeight: 500, fontSize: 30, color: T.ink2, padding: '0 40px'}}>{d.sh.toLocaleString()}주 · 약 ${d.usd}M</div>
      </Card>
      <Card x={960} y={250} w={460} h={260} o={c2}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, padding: '26px 40px 0'}}>공개시장 매수</div>
        <div style={{...F, fontWeight: 700, fontSize: 110, color: T.ink, padding: '0 40px', lineHeight: 1.1}}>{d.buys}건</div>
      </Card>
      <div style={{position: 'absolute', left: 200, top: 560, width: 1220, opacity: tb}}>
        {d.rows.map(([n, t, sh, usd]: [string, string, number, number], i: number) => (
          <div key={n} style={{display: 'flex', alignItems: 'center', height: 70, borderBottom: `2px solid ${T.line}`, background: i === 0 ? T.line : 'transparent', padding: '0 20px', borderRadius: i === 0 ? 10 : 0}}>
            <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, width: 360}}>{n}</span>
            <span style={{...F, fontWeight: 500, fontSize: 24, color: T.ink2, width: 420}}>{t}</span>
            <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, width: 200, textAlign: 'right'}}>{sh.toLocaleString()}주</span>
            <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, width: 200, textAlign: 'right'}}>${usd}M</span>
          </div>))}
      </div>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, position: 'absolute', left: 1480, top: 600, width: 380, lineHeight: 1.4, background: T.surface, borderRadius: 16, padding: '22px 26px', opacity: plan}}>
        CEO 매도 서류: 10b5-1<br /><span style={{fontWeight: 500, fontSize: 26}}>미리 정해 둔 매매 계획</span><br /><span style={{fontWeight: 500, fontSize: 26, color: T.ink3}}>매도 이유는 서류에 없음</span></div>
    </P>
  );
};

// ───── 7. 회사가 적은 위험 — 원문 카드 3장 → 가격 변동 범위 띠 ─────
const Risk: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const qs = s.data.quotes; const band = A(s, 4);
  const cur = [1, 2, 3].reduce((a, k) => (f >= A(s, k) ? k - 1 : a), 0);
  const qo = interpolate(f, [A(s, 0), A(s, 0) + 12, band, band + 10], [0, 1, 1, 0], CL); const bo = appear(f, band + 6);
  const q = qs[cur]; const x = scaleLinear().domain([-50, 50]).range([300, 1620]);
  return (
    <P s={s}>
      <Card x={200} y={260} w={1520} h={440} o={qo}>
        <div style={{position: 'absolute', left: 60, top: 30, fontFamily: 'PD', fontWeight: 700, fontSize: 120, color: T.line, lineHeight: 1}}>“</div>
        <div style={{position: 'absolute', left: 130, right: 70, top: 70, fontFamily: 'PD', fontWeight: 500, fontSize: 38, color: T.ink2, lineHeight: 1.4}}>{q[0]}</div>
        <div style={{...F, position: 'absolute', left: 130, right: 70, bottom: 50, fontWeight: 700, fontSize: 48, color: T.ink, lineHeight: 1.35, wordBreak: 'keep-all'}}>{q[1]}</div>
        <div style={{...F, position: 'absolute', right: 40, top: 26, fontWeight: 700, fontSize: 26, color: T.ink3}}>{cur + 1} / {qs.length}</div>
      </Card>
      <svg width={1920} height={1080} style={{position: 'absolute', opacity: bo}}>
        <text x={960} y={330} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.ink}>D램 평균 판매 가격, 1년 변화율(지난 5년 범위)</text>
        <line x1={x(-50)} x2={x(50)} y1={480} y2={480} stroke={T.line} strokeWidth={4} />
        <line x1={x(0)} x2={x(0)} y1={420} y2={540} stroke={T.ink3} strokeWidth={3} />
        <text x={x(0)} y={585} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={26} fill={T.ink3}>0%</text>
        <rect x={x(-47) + (x(0) - x(-47)) * (1 - bo)} y={450} width={(x(0) - x(-47)) * bo} height={60} rx={8} fill={T.fall} />
        <rect x={x(0)} y={450} width={(x(42) - x(0)) * bo} height={60} rx={8} fill={T.rise} />
        <text x={x(-47)} y={420} fontFamily="PD" fontWeight={700} fontSize={40} fill={T.fall}>−40% 후반</text>
        <text x={x(42)} y={420} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.rise}>+40% 초반</text>
        <text x={960} y={680} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.ink} opacity={appear(f, A(s, 5))}>최근 분기 영업이익률 80%도 이 가격 위에서 나온 숫자</text>
      </svg>
    </P>
  );
};

// ───── 8. 일정 카드 ─────
const Calendar: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const it = s.data.items;
  return (
    <P s={s}>
      {it.map(([n, d, ok]: [string, string, boolean], i: number) => { const o = appear(f, (i === 0 ? 6 : A(s, 1)) + (i > 1 ? 16 : 0));
        return <Card key={n} x={200} y={260 + i * 190} w={1300} h={160} o={o}>
          <div style={{position: 'absolute', left: 36, top: 40, width: 80, height: 80, borderRadius: 16, background: ok ? T.ink : T.line}} />
          <div style={{...F, fontWeight: 700, fontSize: 42, color: T.ink, position: 'absolute', left: 150, top: 30}}>{n}</div>
          <div style={{...F, fontWeight: 500, fontSize: 32, color: ok ? T.ink : T.ink3, position: 'absolute', left: 150, top: 88}}>{d}</div>
        </Card>; })}
    </P>
  );
};

// ───── 9. 은퇴 나이 — 입력 카드 → 54세 → 나이 막대 4개 ─────
const Age: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const inp = appear(f, A(s, 0)), res = appear(f, A(s, 1)), bars = A(s, 2);
  const bo = appear(f, bars); const base = 740, cw = 250, x0 = 900; const y = scaleLinear().domain([0, 60]).range([0, 420]);
  return (
    <P s={s}>
      <Card x={200} y={250} w={600} h={520} o={inp}>
        {d.inputs.map(([k, v]: string[], i: number) => <div key={k} style={{display: 'flex', justifyContent: 'space-between', padding: '0 40px', height: 84, alignItems: 'center', borderBottom: i < 4 ? `2px solid ${T.line}` : 'none', marginTop: i ? 0 : 30}}>
          <span style={{...F, fontWeight: 500, fontSize: 32, color: T.ink2}}>{k}</span><span style={{...F, fontWeight: 700, fontSize: 38, color: T.ink}}>{v}</span></div>)}
      </Card>
      <div style={{...F, fontWeight: 700, fontSize: 140, color: T.accent, position: 'absolute', left: 1000, top: 380, opacity: res * (1 - bo)}}>{d.bars[0][3]}세 은퇴</div>
      <svg width={1920} height={1080} style={{position: 'absolute', opacity: bo}}>
        <line x1={x0 - 20} x2={x0 + cw * 4} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} />
        {d.bars.map(([n, dd, asset, age]: [string, number, number, number], i: number) => {
          const o = appear(f, i === 0 || i === 3 ? bars : A(s, 3) + (i - 1) * 8, 20); const h = y(age) * o; const key = i === 0 || i === 3;
          return <g key={n} opacity={Math.min(1, o * 2)}>
            <rect x={x0 + i * cw} y={base - h} width={cw - 40} height={h} rx={8} fill={i === 0 ? T.accent : key ? T.ink : T.line} />
            <text x={x0 + i * cw + (cw - 40) / 2} y={base - h - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={44} fill={i === 0 ? T.accent : T.ink}>{age}세</text>
            <text x={x0 + i * cw + (cw - 40) / 2} y={base + 38} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink2}>{n}</text>
            <text x={x0 + i * cw + (cw - 40) / 2} y={base + 72} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{dd ? `1억→${asset.toLocaleString()}만` : '1억'}</text>
          </g>; })}
      </svg>
      <div style={{...F, fontWeight: 700, fontSize: 32, color: '#fff', background: T.ink, borderRadius: 30, padding: '8px 26px', position: 'absolute', left: 900, top: 240, opacity: appear(f, A(s, 4))}}>
        지금 가진 돈보다 매달 넣는 300만원이 더 크다</div>
    </P>
  );
};

// ───── 10. 한 장 정리 표 ─────
const Summary: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const cw = [300, 240, 240, 200, 340, 220]; const x0 = 180;
  const hi = [0, appear(f, A(s, 1)), appear(f, A(s, 1)), 0, 0, appear(f, 6)];
  return (
    <P s={s}>
      <div style={{position: 'absolute', left: x0, top: 260}}>
        <div style={{display: 'flex', height: 70, alignItems: 'center', borderBottom: `3px solid ${T.ink}`}}>
          {d.head.map((h: string, i: number) => <div key={i} style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2, width: cw[i], textAlign: i ? 'right' : 'left'}}>{h}</div>)}</div>
        {d.rows.map((r: string[], j: number) => <div key={r[0]} style={{display: 'flex', height: 110, alignItems: 'center', borderBottom: `2px solid ${T.line}`, opacity: appear(f, 6 + j * 10)}}>
          {r.map((c, i) => <div key={i} style={{...F, fontWeight: 700, fontSize: i ? 40 : 38, width: cw[i], textAlign: i ? 'right' : 'left',
            color: i === 0 ? T.ink : hi[i] > 0.5 ? (i === 2 ? T.fall : i === 1 ? T.rise : T.ink) : T.ink}}>{c}</div>)}</div>)}
      </div>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, position: 'absolute', left: x0, top: 690, opacity: appear(f, A(s, 3))}}>
        앞으로 오를지는 말하지 않습니다 · 지난 숫자는 앞으로를 보장하지 않습니다 · 8분기 전체 표는 카페에</div>
    </P>
  );
};

// ───── 목록에 없는 장(루프가 더한 장): 문장 카드 ─────
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
    case 'price': return <Price s={s} />; case 'revenue': return <Revenue s={s} />; case 'margin': return <Margin s={s} />; case 'twin': return <Twin s={s} />;
    case 'form4': return <Form4 s={s} />; case 'risk': return <Risk s={s} />; case 'calendar': return <Calendar s={s} />; case 'age': return <Age s={s} />;
    case 'summary': return <Summary s={s} />;
    case 'mu8': return <Mu8 s={s} />; case 'guide': return <Guide s={s} />; case 'seg': return <Seg s={s} />; case 'dsdx': return <DsDx s={s} />;
    case 'stairs': return <StairsV s={s} />; case 'quotes2': return <Quotes2 s={s} />; case 'scale': return <Scale s={s} />; case 'outlook': return <Outlook s={s} />;
    default: return <Bullets s={s} />;
  }
};

export const E1: React.FC<E1Props> = ({scenes}) => {
  let acc = 0;
  return (
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
  );
};
