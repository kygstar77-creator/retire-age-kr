// E-1 "메모리 3사 — 이익은 몇 배, 주가는 얼마나 흔들렸나" — 재료: work/video/e1.json(ep/E-1/e1props.py가 script.md·voice.json·원자료로 만든다)
// 장면 종류 13가지(선+낙폭 음영·목록·같은 출발점 선·낙폭 막대+달력 띠·작은 막대 3폭·이익률 선·쌍 막대·카운터+표·원문 카드+범위 띠·일정 카드·
// 입력 카드·나이 막대·정리 표). 숫자는 전부 e1.json에서 온다(코드 안에는 눈금·배치 값만). 단계 시점은 data.at(문장 번호, 못 찾으면 −1=안 나옴).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {line as d3line, curveMonotoneX} from 'd3-shape';
import {T, F, CL, FONT_CSS, VScene, at, appear, HandCircle, CountUp, Caption, Page, LogoSting, ProgressRail} from './parts/fm';

export type E1Props = {fps: number; scenes: VScene[]; missing: number; holes: number};
export const e1Frames = (p: E1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: VScene};
const NEVER = 1e9;
const A = (s: VScene, k: number) => (s.data.at?.[k] ?? -1) < 0 ? NEVER : at(s, s.data.at[k]);
const CO: Record<string, string> = {'마이크론': T.ink, 'SK하이닉스': T.accent, '삼성전자': T.fall};
const RAIL = ['1년 주가·낙폭', '여덟 분기 매출', '이익률', '주가 vs 이익', '회사가 적은 위험'];
const md = (d: string) => `${+d.slice(4, 6)}/${+d.slice(6, 8)}`;
const Card: React.FC<{x: number; y: number; w: number; h: number; o?: number; bg?: string; children?: React.ReactNode}> = ({x, y, w, h, o = 1, bg = T.surface, children}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: bg, borderRadius: 20, opacity: o}}>{children}</div>
);
const P: React.FC<S & {children: React.ReactNode}> = ({s, children}) => (
  <Page s={{...s, rail: 0}}>{s.rail ? <ProgressRail n={5} cur={s.rail} labels={RAIL} /> : null}{children}</Page>
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
        <path d={path} stroke={T.daccent} strokeWidth={6} fill="none" strokeLinejoin="round" />
        <text x={X1} y={Y0 + 44} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.dink3}>{md(p.last[0])}</text>
        <g opacity={dn}><text x={(x(ip) + x(it)) / 2} y={Y1 - 34} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill="#9dbcf2">{`${md(p.peak)} → ${md(p.trough)}`}</text></g>
      </svg>
      <div style={{position: 'absolute', left: 1230, top: 230, opacity: up}}>
        <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink3}}>{s.data.name} 1년</div>
        <div style={{...F, fontWeight: 700, fontSize: 128, color: T.rise, lineHeight: 1.1}}>+<CountUp to={p.ret} p={up} digits={1} />%</div>
      </div>
      <div style={{position: 'absolute', left: 1230, top: 500, opacity: dn}}>
        <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink3}}>그 안의 최대 낙폭</div>
        <div style={{...F, fontWeight: 700, fontSize: 128, color: '#6f9cf0', lineHeight: 1.1}}><CountUp to={p.dd} p={dn} digits={1} />%</div>
      </div>
      <div style={{...F, fontWeight: 700, fontSize: 36, color: T.dink, position: 'absolute', left: 1230, top: 740, opacity: Math.max(q4, qs), background: T.dsurface, borderRadius: 16, padding: '14px 26px'}}>
        {qs > q4 ? '이익은 주가만큼 늘었을까?' : '+ 마이크론 회계 4분기 실적'}</div>
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
            <div style={{width: 84, height: 84, borderRadius: 20, background: T.accent, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
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
            <path d={d} stroke={CO[c.name]} strokeWidth={c.name === 'SK하이닉스' ? 6 : 4.5} fill="none" strokeLinejoin="round" />
            <text x={x(m - 1) + 14} y={y(end) + 10} fontFamily="PD" fontWeight={700} fontSize={32} fill={CO[c.name]}>{`${c.name} ${end}`}</text></g>;
        })}
        <text x={X0} y={Y0 + 42} fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{md(cos[0].d[0])}</text>
        <text x={X1} y={Y0 + 42} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{md(cos[0].d[n - 1])}</text>
      </svg>
      <div style={{opacity: ddo}}>
        {[4, 5, 6].map((k, i) => { const c = cos[[0, 2, 1][i]]; const o = appear(f, A(s, k) === NEVER ? sw + 20 + i * 30 : A(s, k), 20); const W = 900 * Math.abs(c.dd) / 60;
          return <div key={c.name} style={{position: 'absolute', left: 200, top: 250 + i * 150, opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink, width: 260, position: 'absolute', top: 18}}>{c.name}</div>
            <div style={{position: 'absolute', left: 270, top: 6, width: W * o, height: 76, borderRadius: 12, background: c.name === 'SK하이닉스' ? T.fall : '#9dbcf2'}} />
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

// ───── 3. 여덟 분기 매출 — 작은 막대 3폭 ─────
const Revenue: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cos = s.data.cos; const W = 500, gap = 60, x0 = 200;
  return (
    <P s={s}>
      {cos.map((c: any, k: number) => {
        const st = A(s, k === 0 ? 0 : k + 1); const o = appear(f, st === NEVER ? 20 + k * 30 : st, 30); const mx = Math.max(...c.rev);
        const bw = W / 8 - 12; const H = 380, base = 800;
        return (
          <div key={c.name} style={{position: 'absolute', left: x0 + k * (W + gap), top: 0, width: W, height: 1080, opacity: Math.max(appear(f, 6 + k * 8), 0)}}>
            <div style={{...F, fontWeight: 700, fontSize: 38, color: CO[c.name], position: 'absolute', top: 240}}>{c.name}</div>
            <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', top: 290}}>{c.unit}</div>
            <svg width={W} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
              {c.rev.map((v: number, i: number) => { const h = (v / mx) * H * o; const last = i === 7, yago = i === 3;
                return <g key={i}>
                  <rect x={i * (W / 8)} y={base - h} width={bw} height={h} rx={6} fill={last ? CO[c.name] : T.line} stroke={yago ? T.ink : 'none'} strokeWidth={yago ? 4 : 0} />
                  <text x={i * (W / 8) + bw / 2} y={base + 30} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={18} fill={T.ink3}>{c.q[i]}</text>
                  {last || yago ? <text opacity={o} x={i * (W / 8) + bw / 2} y={base - h - 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={last ? 30 : 24} fill={last ? CO[c.name] : T.ink}>{v.toLocaleString()}</text> : null}
                </g>; })}
            </svg>
            <div style={{...F, fontWeight: 700, fontSize: 32, color: '#fff', background: T.accent, borderRadius: 30, padding: '4px 20px', position: 'absolute', top: 325, opacity: appear(f, (st === NEVER ? 20 : st) + 40)}}>
              1년 전의 {c.revx.toFixed(2)}배</div>
          </div>
        );
      })}
      <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, position: 'absolute', left: 1320 + 110, top: 284, background: T.soft, borderRadius: 12, padding: '4px 14px', opacity: appear(f, A(s, 4))}}>
        회사 전체(스마트폰·가전 포함)</div>
    </P>
  );
};

// ───── 4. 이익률 선 3개(8분기) ─────
const Margin: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cos = s.data.cos; const X0 = 240, X1 = 1420, Y0 = 820, Y1 = 250;
  const x = scaleLinear().domain([0, 7]).range([X0, X1]); const y = scaleLinear().domain([0, 100]).range([Y0, Y1]);
  const order = [0, 2, 3];
  const coin = appear(f, A(s, 1), 20); const back = appear(f, A(s, 4), 24);
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {[0, 20, 40, 60, 80, 100].map((g) => <g key={g}><line x1={X0} x2={X1} y1={y(g)} y2={y(g)} stroke={T.line} strokeWidth={2} />
          <text x={X0 - 16} y={y(g) + 9} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{g}%</text></g>)}
        {cos.map((c: any, k: number) => { const st = A(s, order[k]); const p = appear(f, st === NEVER ? 20 + k * 30 : st, 36); const m = Math.max(2, Math.round(8 * p));
          const d = d3line<number>().x((_, i) => x(i)).y((v) => y(v)).curve(curveMonotoneX)(c.margin.slice(0, m)) || '';
          return <g key={c.name} opacity={Math.min(1, p * 3)}>
            <path d={d} stroke={CO[c.name]} strokeWidth={c.name === '마이크론' ? 7 : 4.5} fill="none" />
            {[3, 7].filter((i) => i < m).map((i) => <circle key={i} cx={x(i)} cy={y(c.margin[i])} r={9} fill={CO[c.name]} />)}
            {m === 8 ? <text x={X1 + 20} y={y(c.margin[7]) + 12 + (c.name === 'SK하이닉스' ? 18 : c.name === '마이크론' ? -14 : 0)} fontFamily="PD" fontWeight={700} fontSize={34} fill={CO[c.name]}>{`${c.name} ${c.margin[7]}%`}</text> : null}
          </g>; })}
        {cos[0].q.map((q: string, i: number) => <text key={i} x={x(i)} y={Y0 + 36} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={20} fill={T.ink3}>{q}</text>)}
        <g opacity={back}><HandCircle cx={x(0) + 20} cy={y(cos[0].margin[0])} rx={60} ry={40} p={back} />
          <text x={X0 + 20} y={Y1 + 60} fontFamily="PD" fontWeight={700} fontSize={32} fill={T.accent}>{`마이크론 ${cos[0].margin[0]}% (${cos[0].q[0]})`}</text></g>
      </svg>
      <Card x={1480} y={560} w={380} h={200} o={coin} bg={T.soft}>
        <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink, padding: '34px 30px', lineHeight: 1.4}}>100원 팔면<br /><span style={{color: T.accent, fontSize: 56}}>약 80원</span> 남음</div>
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
            <rect x={cx} y={base - h1} width={140} height={h1} rx={8} fill={CO[name]} opacity={Math.min(1, o1 * 3)} />
            <text x={cx + 70} y={base - h1 - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={44} fill={CO[name]} opacity={o1}>{opx.toFixed(2)}배</text>
            <rect x={cx + 160} y={base - h2} width={140} height={h2} rx={8} fill={T.line} stroke={T.ink2} strokeWidth={3} opacity={Math.min(1, o2 * 3)} />
            <text x={cx + 230} y={base - h2 - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.ink2} opacity={o2}>{px.toFixed(2)}배</text>
            <text x={cx + 150} y={base + 50} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={36} fill={T.ink}>{name}</text>
            <text x={cx + 70} y={base + 86} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>영업이익</text>
            <text x={cx + 230} y={base + 86} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3} opacity={o2}>주가 1년</text>
          </g>; })}
        <g opacity={gapN}><HandCircle cx={1360 + 150} cy={base - 230} rx={250} ry={290} p={gapN} /></g>
      </svg>
      <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, position: 'absolute', left: 1180, top: 150, background: T.soft, borderRadius: 14, padding: '10px 20px', opacity: appear(f, A(s, 5))}}>
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
        <div style={{...F, fontWeight: 700, fontSize: 110, color: T.fall, padding: '0 40px', lineHeight: 1.1}}><CountUp to={d.n} p={c1} />건</div>
        <div style={{...F, fontWeight: 500, fontSize: 30, color: T.ink2, padding: '0 40px'}}>{d.sh.toLocaleString()}주 · 약 ${d.usd}M</div>
      </Card>
      <Card x={960} y={250} w={460} h={260} o={c2}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, padding: '26px 40px 0'}}>공개시장 매수</div>
        <div style={{...F, fontWeight: 700, fontSize: 110, color: T.ink, padding: '0 40px', lineHeight: 1.1}}>{d.buys}건</div>
      </Card>
      <div style={{position: 'absolute', left: 200, top: 560, width: 1220, opacity: tb}}>
        {d.rows.map(([n, t, sh, usd]: [string, string, number, number], i: number) => (
          <div key={n} style={{display: 'flex', alignItems: 'center', height: 70, borderBottom: `2px solid ${T.line}`, background: i === 0 ? T.soft : 'transparent', padding: '0 20px', borderRadius: i === 0 ? 10 : 0}}>
            <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, width: 360}}>{n}</span>
            <span style={{...F, fontWeight: 500, fontSize: 24, color: T.ink2, width: 420}}>{t}</span>
            <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, width: 200, textAlign: 'right'}}>{sh.toLocaleString()}주</span>
            <span style={{...F, fontWeight: 700, fontSize: 30, color: i === 0 ? T.accent : T.ink, width: 200, textAlign: 'right'}}>${usd}M</span>
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
        <div style={{position: 'absolute', left: 60, top: 30, fontFamily: 'Georgia, serif', fontSize: 120, color: T.accent, lineHeight: 1}}>“</div>
        <div style={{position: 'absolute', left: 130, right: 70, top: 70, fontFamily: 'Georgia, serif', fontSize: 40, color: T.ink2, lineHeight: 1.4, fontStyle: 'italic'}}>{q[0]}</div>
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
          <div style={{position: 'absolute', left: 36, top: 40, width: 80, height: 80, borderRadius: 16, background: ok ? T.accent : T.line}} />
          <div style={{...F, fontWeight: 700, fontSize: 42, color: T.ink, position: 'absolute', left: 150, top: 30}}>{n}</div>
          <div style={{...F, fontWeight: 500, fontSize: 32, color: ok ? T.accent : T.ink3, position: 'absolute', left: 150, top: 88}}>{d}</div>
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
            <rect x={x0 + i * cw} y={base - h} width={cw - 40} height={h} rx={8} fill={i === 0 ? T.ink3 : key ? T.accent : '#ffb48a'} />
            <text x={x0 + i * cw + (cw - 40) / 2} y={base - h - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={44} fill={key ? T.accent : T.ink}>{age}세</text>
            <text x={x0 + i * cw + (cw - 40) / 2} y={base + 38} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink2}>{n}</text>
            <text x={x0 + i * cw + (cw - 40) / 2} y={base + 72} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{dd ? `1억→${asset.toLocaleString()}만` : '1억'}</text>
          </g>; })}
      </svg>
      <div style={{...F, fontWeight: 700, fontSize: 32, color: '#fff', background: T.accent, borderRadius: 30, padding: '8px 26px', position: 'absolute', left: 900, top: 240, opacity: appear(f, A(s, 4))}}>
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
            color: i === 0 ? CO[r[0]] : hi[i] > 0.5 ? (i === 2 ? T.fall : i === 1 ? T.rise : T.accent) : T.ink}}>{c}</div>)}</div>)}
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
    case 'summary': return <Summary s={s} />; default: return <Bullets s={s} />;
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
