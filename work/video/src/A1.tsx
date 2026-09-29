// A-1 "JEPQ와 SCHD, 1억 넣고 1년 뒤 실제로 남은 돈은?" — 재료: work/video/a1.json(ep/A-1/a1props.py가 voice.json + 사실표로 만든다)
// 장면 종류 17가지(질문 카드·카운트업·목록·흐름도·원문 카드·도넛·숫자 쌍·쌓은 막대·선 그래프·음수 막대·원화 표·보유 목록·세금 카드·
// 비율 막대·기준선 막대·월별 기둥·계산기 입력). 틀은 장마다 바뀌고, 틀 안에서는 문장이 바뀔 때마다 하나씩 더한다(RULES 관찰 2026-09-30).
// 남의 차트·사진 없음. 숫자는 전부 a1.json에서 온다(코드 안에 숫자를 새로 쓰지 않는다 — 눈금·배치 값만).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {line as d3line, curveMonotoneX, arc as d3arc} from 'd3-shape';
import {T, F, CL, FONT_CSS, VScene, at, appear, fmtPct, eok, HandCircle, CountUp, Caption, Page, LogoSting, Flame} from './parts/fm';

export type A1Props = {fps: number; scenes: VScene[]; missing: number};
export const a1Frames = (p: A1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: VScene};
const KIND_COLOR: Record<string, string> = {cc: T.accent, idx: T.ink2, div: T.fall};
const KIND_NAME: Record<string, string> = {cc: '커버드콜', idx: '지수 그대로', div: '배당주'};

const Card: React.FC<{x: number; y: number; w: number; h: number; o?: number; dy?: number; children?: React.ReactNode; bg?: string}> = ({x, y, w, h, o = 1, dy = 0, children, bg = T.surface}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * (dy || 24), width: w, height: h, background: bg, borderRadius: 20, opacity: o}}>{children}</div>
);
const Legend: React.FC<{items: [string, string][]; x: number; y: number; o?: number}> = ({items, x, y, o = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', gap: 28, opacity: o}}>
    {items.map(([c, t]) => <div key={t} style={{display: 'flex', alignItems: 'center', gap: 10}}>
      <div style={{width: 22, height: 22, borderRadius: 6, background: c}} /><span style={{...F, fontWeight: 500, fontSize: 26, color: T.ink2}}>{t}</span></div>)}
  </div>
);

// ───── 0. 여는 장면: 검색창 같은 질문 카드 → 두 계좌 잔고 카운트업 ─────
const Open: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const q = interpolate(f, [0, 10, at(s, 0) + 30, at(s, 0) + 44], [0, 1, 1, 0], CL);
  const num = appear(f, at(s, 0) + 30, 40); const dist = appear(f, at(s, 1)); const ring = appear(f, at(s, 2), 22); const note = appear(f, at(s, 3)); const qs = appear(f, at(s, 4));
  const vals: number[] = d.big.map((b: any[]) => b[2]);
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      <div style={{position: 'absolute', left: 360, right: 360, top: 420, height: 130, borderRadius: 65, background: T.dsurface, opacity: q,
        display: 'flex', alignItems: 'center', gap: 26, padding: '0 50px', transform: `scale(${0.96 + q * 0.04})`}}>
        <svg width={48} height={48} viewBox="0 0 24 24"><circle cx={10} cy={10} r={7} stroke={T.dink3} strokeWidth={2.5} fill="none" /><line x1={15} y1={15} x2={21} y2={21} stroke={T.dink3} strokeWidth={2.5} strokeLinecap="round" /></svg>
        <span style={{...F, fontWeight: 700, fontSize: 58, color: T.dink}}>{d.q}</span>
      </div>
      {d.big.map(([name]: string[], i: number) => (
        <div key={name} style={{position: 'absolute', left: 170 + i * 820, top: 170, width: 800, opacity: num, transform: `translateY(${(1 - num) * 30}px)`}}>
          <div style={{...F, fontWeight: 700, fontSize: 58, color: T.dink3}}>{name}</div>
          <div style={{fontWeight: 700, fontSize: 104, color: i === 1 ? T.daccent : T.dink, lineHeight: 1.2, whiteSpace: 'nowrap'}}>
            <span style={{...F}}>{num < 1 ? eok(Math.round(vals[i] * num)) : d.big[i][1]}</span>
          </div>
          <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink, marginTop: 26, opacity: dist, display: 'inline-block', padding: '10px 26px',
            borderRadius: 14, background: T.dsurface}}>{d.dist[i][1]}</div>
        </div>
      ))}
      <svg width={1920} height={1080} style={{position: 'absolute'}}><HandCircle cx={1330} cy={312} rx={380} ry={70} p={ring} color={T.daccent} /></svg>
      <div style={{...F, fontWeight: 500, fontSize: 32, color: T.dink3, position: 'absolute', left: 170, top: 660, opacity: note}}>{d.note}</div>
      <div style={{position: 'absolute', left: 170, top: 740, display: 'flex', gap: 20, opacity: qs}}>
        {['원금이 깎이나?', '떨어진 해에는?', '세금·건보료 떼면?'].map((t, i) => (
          <div key={t} style={{...F, fontWeight: 700, fontSize: 36, color: T.dink, border: `3px solid ${T.dink3}`, borderRadius: 40, padding: '10px 28px',
            opacity: appear(f, at(s, 4) + i * 10)}}>{t}</div>))}
      </div>
      <div style={{...F, fontWeight: 500, fontSize: 22, color: T.dink3, position: 'absolute', left: 120, bottom: 20}}>출처 {s.source}</div>
      <Caption s={s} dark />
    </AbsoluteFill>
  );
};

// ───── 1. 오늘 확인할 다섯 가지 ─────
const Agenda: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const items: string[] = s.data.items;
  const when = [at(s, 1), at(s, 1) + 40, at(s, 1) + 80, at(s, 2), at(s, 2) + 40];
  return (
    <Page s={s}>
      {items.map((t, i) => {
        const o = appear(f, when[i]);
        return (
          <div key={t} style={{position: 'absolute', left: 200, top: 250 + i * 112, display: 'flex', alignItems: 'center', gap: 34, opacity: o, transform: `translateX(${(1 - o) * -30}px)`}}>
            <div style={{width: 84, height: 84, borderRadius: 20, background: T.accent, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <span style={{...F, fontWeight: 700, fontSize: 48, color: '#fff'}}>{i + 1}</span></div>
            <span style={{...F, fontWeight: 700, fontSize: 60, color: T.ink}}>{t}</span>
          </div>
        );
      })}
      <div style={{...F, fontWeight: 700, fontSize: 44, color: T.accent, position: 'absolute', left: 1180, top: 480, padding: '24px 36px', background: T.soft, borderRadius: 20,
        opacity: appear(f, at(s, 3))}}>{s.data.extra}</div>
    </Page>
  );
};

// ───── 2. 구조: 흐름도 → 원문 카드 → 도넛 → 원문 카드 ─────
const Donut: React.FC<{x: number; y: number; name: string; parts: [string, number][]; p: number}> = ({x, y, name, parts, p}) => {
  const R = 170, r = 110; let a0 = 0; const cols = [T.ink2, T.accent];
  const rest = 100 - parts.reduce((a, b) => a + b[1], 0);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 760, opacity: p}}>
      <svg width={380} height={380} style={{position: 'absolute', left: 0, top: 0}}>
        <g transform="translate(190,190)">
          {parts.map(([n, v], i) => {
            const a1 = a0 + (v / 100) * Math.PI * 2 * p; const d = d3arc()({innerRadius: r, outerRadius: R, startAngle: a0, endAngle: a1}) || ''; a0 = a1;
            return <path key={n} d={d} fill={cols[i]} />;
          })}
          <path d={d3arc()({innerRadius: r, outerRadius: R, startAngle: a0, endAngle: a0 + (rest / 100) * Math.PI * 2 * p}) || ''} fill={T.line} />
          <text textAnchor="middle" y={16} fontFamily="PD" fontWeight={700} fontSize={48} fill={T.ink}>{name}</text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 400, top: 110}}>
        {parts.map(([n, v], i) => (
          <div key={n} style={{display: 'flex', alignItems: 'baseline', gap: 16, marginBottom: 14}}>
            <div style={{width: 20, height: 20, borderRadius: 5, background: cols[i]}} />
            <span style={{...F, fontWeight: 500, fontSize: 30, color: T.ink2}}>{n}</span>
            <span style={{...F, fontWeight: 700, fontSize: 44, color: i === 1 ? T.accent : T.ink}}>{v.toFixed(2)}%</span>
          </div>))}
        <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3}}>나머지 현금 등 {rest.toFixed(2)}%</div>
      </div>
    </div>
  );
};
const Quote: React.FC<{en: string; ko: string; o: number; y?: number}> = ({en, ko, o, y = 290}) => (
  <Card x={200} y={y} w={1520} h={430} o={o}>
    <div style={{position: 'absolute', left: 60, top: 30, fontFamily: 'Georgia, serif', fontSize: 120, color: T.accent, lineHeight: 1}}>“</div>
    <div style={{position: 'absolute', left: 130, right: 70, top: 70, fontFamily: 'Georgia, serif', fontSize: 44, color: T.ink2, lineHeight: 1.4, fontStyle: 'italic'}}>{en}</div>
    <div style={{...F, position: 'absolute', left: 130, right: 70, bottom: 56, fontWeight: 700, fontSize: 48, color: T.ink, lineHeight: 1.35, wordBreak: 'keep-all'}}>{ko}</div>
  </Card>
);
const Structure: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const [a, b, c, e] = d.steps.map((i: number) => at(s, i));
  const vis = (from: number, to: number | null) => interpolate(f, to === null ? [from, from + 12] : [from, from + 12, to, to + 10], to === null ? [0, 1] : [0, 1, 1, 0], CL);
  const o1 = vis(a, b), o2 = vis(b, c), o3 = vis(c, e), o4 = vis(e, null);
  const q3 = appear(f, at(s, 8));
  const W = 330, gap = 90, x0 = (1920 - (W * 4 + gap * 3)) / 2;
  return (
    <Page s={s}>
      <div style={{opacity: o1}}>
        {d.flow.map((t: string, i: number) => {
          const st = a + i * 45 + (i >= 2 ? Math.max(0, at(s, 2) - a - 90) : 0); const o = appear(f, st);
          return (
            <React.Fragment key={t}>
              <Card x={x0 + i * (W + gap)} y={420} w={W} h={180} o={o} bg={i === 3 ? T.accent : T.surface}>
                <div style={{...F, fontWeight: 700, fontSize: 44, color: i === 3 ? '#fff' : T.ink, textAlign: 'center', marginTop: 62}}>{t}</div>
              </Card>
              {i < 3 ? <svg width={gap} height={60} style={{position: 'absolute', left: x0 + i * (W + gap) + W, top: 480, opacity: appear(f, st + 20)}}>
                <path d={`M10 30 L${gap - 22} 30 M${gap - 36} 14 L${gap - 16} 30 L${gap - 36} 46`} stroke={T.ink3} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg> : null}
            </React.Fragment>
          );
        })}
        <div style={{...F, fontWeight: 500, fontSize: 30, color: T.ink3, position: 'absolute', left: x0, top: 650, opacity: appear(f, a + 40)}}>배당 ETF: 배당 주는 주식 → 들어온 배당을 나눠 줌</div>
      </div>
      <div style={{opacity: o2}}><Quote en={d.quote1} ko={d.quote1ko} o={1} /></div>
      <div style={{opacity: o3}}>
        {d.donut.map((dn: any, i: number) => <Donut key={dn.name} x={170 + i * 860} y={300} name={dn.name} parts={dn.parts} p={appear(f, c + (i ? Math.max(40, at(s, 5) - c) : 0), 30)} />)}
      </div>
      <div style={{opacity: o4}}>
        <Quote en={d.quote2} ko={d.quote2ko} o={1} y={250} />
        <div style={{position: 'absolute', left: 200, top: 700, width: 1520, opacity: q3, display: 'flex', gap: 24, alignItems: 'center',
          background: T.soft, borderRadius: 16, padding: '20px 30px', boxSizing: 'border-box'}}>
          <span style={{fontFamily: 'Georgia, serif', fontStyle: 'italic', fontSize: 30, color: T.ink2}}>{d.quote3}</span>
          <span style={{...F, fontWeight: 700, fontSize: 30, color: T.accent, whiteSpace: 'nowrap'}}>{d.quote3ko}</span>
        </div>
      </div>
    </Page>
  );
};

// ───── 3. 숫자 쌍: KODEX 200 vs 커버드콜 ─────
const Pairs: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <Page s={s}>
      {d.names.map((n: string, j: number) => (
        <div key={n} style={{...F, fontWeight: 700, fontSize: 34, color: j ? T.accent : T.ink2, position: 'absolute', left: 560 + j * 620, top: 250, width: 560, textAlign: 'center',
          opacity: appear(f, at(s, 1))}}>{n}</div>))}
      {d.rows.map((r: any[], i: number) => {
        const o = appear(f, at(s, d.steps[i]), 20); const chip = appear(f, at(s, d.steps[i] + (i ? 1 : 2)));
        return (
          <Card key={r[0]} x={140} y={310 + i * 280} w={1640} h={250} o={o}>
            <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, position: 'absolute', left: 50, top: 100}}>{r[0]}</div>
            {[r[1], r[2]].map((v: number, j: number) => (
              <div key={j} style={{position: 'absolute', left: 420 + j * 620, top: 50, width: 560, textAlign: 'center'}}>
                <CountUp to={v} p={o} digits={2} suffix="%" prefix={v > 0 ? '+' : ''} style={{fontWeight: 700, fontSize: 110, color: v > 0 ? T.rise : T.fall}} />
              </div>))}
            <div style={{...F, fontWeight: 700, fontSize: 34, color: '#fff', background: T.accent, borderRadius: 30, padding: '6px 22px', position: 'absolute', right: 40, bottom: 14,
              opacity: chip}}>{r[3]}</div>
          </Card>
        );
      })}
    </Page>
  );
};

// ───── 4. 1년: 분배금 + 주가 쌓은 막대 ─────
const Stack: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const items: [string, number, number, string][] = d.items;
  const X0 = 520, X1 = 1640; const x = scaleLinear().domain([0, 26]).range([X0, X1]); const rowH = 70, y0 = 262;
  const kd = appear(f, at(s, d.kodexAt));
  return (
    <Page s={s}>
      <Legend items={[[T.accent, '분배금'], [T.ink3, '주가 변화']]} x={1240} y={190} o={appear(f, at(s, 1))} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {[0, 5, 10, 15, 20, 25].map((t) => <g key={t}><line x1={x(t)} x2={x(t)} y1={y0 - 10} y2={y0 + rowH * 7} stroke={T.line} strokeWidth={2} />
          <text x={x(t)} y={y0 + rowH * 7 + 30} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{t}%</text></g>)}
        {items.map(([n, dv, pv, k], i) => {
          const o = appear(f, at(s, d.show[i]) + (i === 4 ? 30 : 0), 20); const y = y0 + i * rowH + 8; const h = rowH - 22;
          const dw = (x(dv) - X0) * o; const pEnd = x(dv + pv) ; const pw = (pEnd - x(dv)) * o;
          const tot = d.total[n];
          return (
            <g key={n} opacity={Math.min(1, o * 2)}>
              <text x={X0 - 24} y={y + h / 2 + 12} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={36} fill={T.ink}>{n}</text>
              <text x={X0 - 24} y={y + h / 2 + 36} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={18} fill={KIND_COLOR[k]}>{KIND_NAME[k]}</text>
              <rect x={X0} y={y} width={Math.max(0, dw)} height={h} rx={6} fill={T.accent} />
              {pv >= 0 ? <rect x={X0 + dw} y={y} width={Math.max(0, pw)} height={h} rx={6} fill={T.ink3} />
                : <rect x={X0 + dw + pw} y={y} width={Math.max(0, -pw)} height={h} fill={T.fall} opacity={0.85} />}
              <text x={Math.max(X0 + dw, X0 + dw + pw) + 16} y={y + h / 2 + 12} fontFamily="PD" fontWeight={700} fontSize={34} fill={n === 'SCHD' ? T.accent : T.ink}>{(tot * o).toFixed(2)}%</text>
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: 200, top: 800, width: 1520, height: 76, borderRadius: 16, background: T.surface, opacity: kd,
        display: 'flex', alignItems: 'center', gap: 40, padding: '0 34px', boxSizing: 'border-box'}}>
        <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink}}>{d.kodex[0]} 최근 1년</span>
        <span style={{...F, fontWeight: 700, fontSize: 38, color: T.accent}}>{d.kodex[1].toFixed(2)}%</span>
        <span style={{...F, fontWeight: 500, fontSize: 30, color: T.ink2}}>비교지수 {d.kodex[2].toFixed(2)}%</span>
        <span style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3}}>운용사 공시값(계산 방식 다름)</span>
      </div>
    </Page>
  );
};

// ───── 5. 원금: 두 선 그래프(주가만 → 재투자) ─────
const Lines: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const ats: number[] = d.at.map((i: number) => at(s, i));
  let k = 0; ats.forEach((a, i) => { if (f >= a) k = i; });
  const P = d.panels[k]; const t0 = ats[k];
  const X0 = 250, X1 = 1600, Y0 = 290, Y1 = 830;
  const hi = Math.max(...P.B, ...P.A), lo = Math.min(0, ...P.A, ...P.B);
  const x = scaleLinear().domain([0, P.A.length - 1]).range([X0, X1]); const y = scaleLinear().domain([lo, hi * 1.08]).range([Y1, Y0]).nice(5);
  const mk = (arr: number[]) => d3line<number>().x((_, i) => x(i)).y((v) => y(v)).curve(curveMonotoneX)(arr) || '';
  const draw = appear(f, t0 + 4, 50); const lab = appear(f, t0 + 50);
  const yr = (dt: string) => `${dt.slice(0, 4)}.${dt.slice(5, 7)}`;
  const n = P.A.length - 1;
  return (
    <Page s={s} sub={P.sub}>
      <Card x={120} y={250} w={1680} h={640} o={1} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {y.ticks(5).map((t: number) => <g key={t}><line x1={X0} x2={X1} y1={y(t)} y2={y(t)} stroke={t === 0 ? T.ink3 : T.line} strokeWidth={t === 0 ? 3 : 2} />
          <text x={X0 - 18} y={y(t) + 9} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{t}%</text></g>)}
        <text x={X0} y={Y1 + 42} fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{yr(P.d0)}</text>
        <text x={X1} y={Y1 + 42} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{yr(P.d1)}</text>
        <path d={mk(P.B)} fill="none" stroke={T.ink3} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        <path d={mk(P.A)} fill="none" stroke={T.accent} strokeWidth={6} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        <circle cx={x(n)} cy={y(P.A[n])} r={10 * lab} fill={T.accent} stroke={T.surface} strokeWidth={4} />
        <circle cx={x(n)} cy={y(P.B[n])} r={10 * lab} fill={T.ink2} stroke={T.surface} strokeWidth={4} />
      </svg>
      {[[P.b, P.endB, T.ink2, P.B[n]], [P.a, P.endA, T.accent, P.A[n]]].map(([nm, v, c, yv]: any) => (
        <div key={nm} style={{position: 'absolute', left: X1 + 22, top: Math.min(Math.max(y(yv) - 40, 270), 810), opacity: lab}}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: c}}>{nm}</div>
          <div style={{...F, fontWeight: 700, fontSize: 40, color: c}}>{fmtPct(v)}</div>
        </div>))}
    </Page>
  );
};

// ───── 6. 2022년: 음수 막대 ─────
const Neg: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const items: [string, number, string][] = d.items;
  const Z = 1560, x = scaleLinear().domain([-35, 0]).range([520, Z]);
  const show = [1, 1, 2, 3]; const jp = appear(f, at(s, 2) + 20);
  return (
    <Page s={s}>
      <Legend items={[[T.ink2, '지수 그대로'], [T.accent, '커버드콜'], [T.fall, '배당주']]} x={1060} y={190} o={appear(f, at(s, 1))} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {[-30, -20, -10, 0].map((t) => <g key={t}><line x1={x(t)} x2={x(t)} y1={270} y2={750} stroke={t === 0 ? T.ink3 : T.line} strokeWidth={t === 0 ? 3 : 2} />
          <text x={x(t)} y={782} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{t}%</text></g>)}
        {items.map(([n, v, k], i) => {
          const o = appear(f, at(s, show[i]) + (i === 1 ? 30 : 0), 22); const y = 290 + i * 115; const w = (Z - x(v)) * o;
          return (
            <g key={n} opacity={Math.min(1, o * 2)}>
              <text x={Z + 24} y={y + 50} fontFamily="PD" fontWeight={700} fontSize={40} fill={T.ink}>{n}</text>
              <rect x={Z - w} y={y} width={w} height={76} rx={8} fill={KIND_COLOR[k]} />
              <text x={Z - w - 18} y={y + 52} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.fall}>{fmtPct(v * o)}</text>
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: 200, top: 800, opacity: jp, display: 'flex', gap: 22, alignItems: 'center'}}>
        <span style={{...F, fontWeight: 700, fontSize: 32, color: T.ink}}>JEPI 2022년</span>
        <span style={{...F, fontWeight: 700, fontSize: 32, color: T.fall}}>주가 {fmtPct(d.jepi[0])}</span>
        <span style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3}}>+</span>
        <span style={{...F, fontWeight: 700, fontSize: 32, color: T.accent}}>분배금 {fmtPct(d.jepi[1])}</span>
      </div>
    </Page>
  );
};

// ───── 7. 1억 → 1년 뒤 원화 표 ─────
const Won: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows: [string, number, number, number][] = s.data.rows; const show = [1, 2, 2, 3];
  const cols = ['ETF', '세후 분배금', '1년 뒤 평가금액', '합계'], cx = [200, 560, 960, 1400];
  const ring = appear(f, at(s, 4), 22);
  return (
    <Page s={s}>
      <Card x={140} y={250} w={1640} h={600} />
      {cols.map((c, i) => <div key={c} style={{...F, fontWeight: 500, fontSize: 28, color: T.ink3, position: 'absolute', left: cx[i], top: 290}}>{c}</div>)}
      <div style={{position: 'absolute', left: 180, width: 1560, top: 344, height: 2, background: T.line}} />
      {rows.map(([n, dv, pv, tv], i) => {
        const o = appear(f, at(s, show[i]) + (i === 2 ? 40 : 0)); const y = 372 + i * 118;
        return (
          <div key={n} style={{opacity: o, position: 'absolute', top: y, left: 0, width: 1920, transform: `translateY(${(1 - o) * 16}px)`}}>
            <div style={{...F, fontWeight: 700, fontSize: 48, color: T.ink, position: 'absolute', left: cx[0]}}>{n}</div>
            <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink2, position: 'absolute', left: cx[1]}}>{eok(dv)}</div>
            <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink2, position: 'absolute', left: cx[2]}}>{eok(pv)}</div>
            <div style={{...F, fontWeight: 700, fontSize: 52, color: i === 0 ? T.accent : T.ink, position: 'absolute', left: cx[3]}}>{eok(tv)}</div>
          </div>
        );
      })}
      <svg width={1920} height={1080} style={{position: 'absolute'}}><HandCircle cx={660} cy={522} rx={150} ry={50} p={ring} /></svg>
    </Page>
  );
};

// ───── 8. 보유 상위 10 ─────
const Holdings: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const x = scaleLinear().domain([0, 8]).range([0, 300]);
  return (
    <Page s={s}>
      {d.cols.map((c: any, j: number) => {
        const o = appear(f, at(s, d.at[j]), 20);
        return (
          <Card key={c.name} x={140 + j * 555} y={240} w={530} h={640} o={o}>
            <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink, position: 'absolute', left: 34, top: 22}}>{c.name}</div>
            <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', left: 34, top: 84}}>{c.note}</div>
            <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', right: 34, top: 20}}>상위 10 합</div>
            <div style={{...F, fontWeight: 700, fontSize: 54, color: T.accent, position: 'absolute', right: 34, top: 46}}>{c.top10.toFixed(2)}%</div>
            {c.rows.map(([tk, v]: [string, number], i: number) => {
              const r = appear(f, at(s, d.at[j]) + 10 + i * 4, 12);
              return (
                <div key={tk} style={{position: 'absolute', left: 34, top: 136 + i * 48, display: 'flex', alignItems: 'center'}}>
                  <span style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, width: 100}}>{tk}</span>
                  <div style={{width: x(v) * r, height: 26, background: i === 0 && c.name === 'JEPQ' ? T.accent : T.ink3, borderRadius: 5}} />
                  <span style={{...F, fontWeight: 700, fontSize: 26, color: T.ink, marginLeft: 12, opacity: r}}>{v.toFixed(2)}</span>
                </div>
              );
            })}
          </Card>
        );
      })}
    </Page>
  );
};

// ───── 9. 세금: 두 카드 + 분배금 쪼개기 막대 ─────
const Tax: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const A = d.at.map((i: number) => at(s, i));
  return (
    <Page s={s}>
      {d.cards.map((c: string[], i: number) => {
        const o = appear(f, A[i ? 1 : 0], 18);
        return (
          <Card key={c[0]} x={140 + i * 830} y={240} w={810} h={270} o={o}>
            <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink2, position: 'absolute', left: 40, top: 30}}>{c[0]}</div>
            <div style={{...F, fontWeight: 700, fontSize: 96, color: T.accent, position: 'absolute', left: 36, top: 76}}>{c[1]}</div>
            <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink, position: 'absolute', left: i ? 360 : 300, top: 110, width: i ? 420 : 480, wordBreak: 'keep-all'}}>{c[2]}</div>
            <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', left: 40, bottom: 26}}>{c[3]}</div>
          </Card>
        );
      })}
      {d.split.map((sp: any, i: number) => {
        const o = appear(f, A[i ? 3 : 2], 26); const W = 1220; const tw = (sp.taxed / sp.total) * W * o; const y = 560 + i * 150;
        const share = ((sp.taxed / sp.total) * 100).toFixed(1);
        return (
          <div key={sp.name} style={{position: 'absolute', left: 140, top: y, width: 1640, opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink}}>{sp.name} · 1년 분배금 {sp.total.toLocaleString()}원</div>
            <div style={{position: 'relative', marginTop: 12, width: W, height: 60, background: T.line, borderRadius: 10, overflow: 'hidden'}}>
              <div style={{position: 'absolute', left: 0, top: 0, height: 60, width: tw, background: T.accent}} />
            </div>
            <div style={{...F, fontWeight: 700, fontSize: 32, color: T.accent, position: 'absolute', left: W + 30, top: 50}}>과세표준 {sp.taxed.toLocaleString()}원 · {share}%</div>
          </div>
        );
      })}
    </Page>
  );
};

// ───── 9-2. 국내 커버드콜 11종 과세 몫 ─────
const TAXC: Record<string, string> = {'국내주식': T.accent, '채권': T.ink3, '혼합자산': T.ink2, '해외주식': T.fall};
const TaxBars: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const items: [string, number, string, string][] = s.data.items;
  const X0 = 900, W = 760; const when = (i: number) => (i < 2 ? at(s, 2) : i < 3 ? at(s, 2) + 30 : i < 6 ? at(s, 3) + (i - 3) * 12 : at(s, 4) + (i - 6) * 10);
  return (
    <Page s={s}>
      <Legend items={Object.entries(TAXC).map(([k, c]) => [c, k] as [string, string])} x={1060} y={190} o={appear(f, at(s, 1))} />
      {items.map(([n, v, k, note], i) => {
        const o = appear(f, when(i), 18); const y = 250 + i * 54;
        return (
          <div key={n} style={{position: 'absolute', top: y, left: 0, width: 1920, opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: 25, color: T.ink, position: 'absolute', right: 1920 - X0 + 20, top: 8, whiteSpace: 'nowrap'}}>{n.replace('KODEX ', '')}</div>
            <div style={{position: 'absolute', left: X0, top: 6, width: W, height: 36, background: T.line, borderRadius: 6}} />
            <div style={{position: 'absolute', left: X0, top: 6, width: Math.max(4, (v / 100) * W * o), height: 36, background: TAXC[k], borderRadius: 6}} />
            <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink, position: 'absolute', left: X0 + W + 18, top: 8}}>{v.toFixed(1)}%{note ? <span style={{fontWeight: 500, fontSize: 20, color: T.ink3}}> · {note}</span> : null}</div>
          </div>
        );
      })}
      <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', left: X0, top: 850}}>이름 앞 KODEX 생략</div>
    </Page>
  );
};

// ───── 10. 2천만원 선 ─────
const Line2k: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const A = d.at.map((i: number) => at(s, i));
  return (
    <Page s={s}>
      {d.bars.map(([n, big, total, note]: [string, string, number, string], i: number) => {
        const o = appear(f, A[i ? 1 : 0], 24); const W = 1100; const share = i ? 2000 / total : 1; const y = 250 + i * 170;
        return (
          <div key={n} style={{position: 'absolute', left: 140, top: y, opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2}}>{n} <span style={{fontWeight: 500, fontSize: 24, color: T.ink3}}>· {note}</span></div>
            <div style={{position: 'relative', marginTop: 10, width: W * o, height: 56, background: T.line, borderRadius: 10}}>
              <div style={{position: 'absolute', left: 0, top: 0, height: 56, width: W * share * o, background: T.accent, borderRadius: 10}} />
            </div>
            <div style={{...F, fontWeight: 700, fontSize: 44, color: T.accent, position: 'absolute', left: W + 40, top: 38, whiteSpace: 'nowrap'}}>{big}</div>
            <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, marginTop: 8}}>주황 = 2천만원을 셈하는 몫</div>
          </div>
        );
      })}
      {d.law.map((t: string, i: number) => (
        <div key={t} style={{position: 'absolute', left: 140, top: 620 + i * 76, display: 'flex', gap: 18, alignItems: 'center', opacity: appear(f, A[2] + i * 40)}}>
          <div style={{width: 14, height: 14, borderRadius: 7, background: i === 2 ? T.accent : T.ink2}} />
          <span style={{...F, fontWeight: 700, fontSize: 36, color: i === 2 ? T.accent : T.ink}}>{t}</span>
        </div>))}
    </Page>
  );
};

// ───── 11. 월별 분배금 기둥 ─────
const Monthly: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <Page s={s}>
      {(['JEPQ', 'JEPI'] as const).map((nm, j) => {
        const arr: [string, number][] = d[nm]; const o = appear(f, at(s, d.at[j]), 30); const vals = arr.map((a) => a[1]);
        const mx = Math.max(...vals), mn = Math.min(...vals); const x0 = 170 + j * 840, W = 740, H = 440, base = 790;
        const y = scaleLinear().domain([0, 0.75]).range([0, H]); const bw = W / 12 - 14;
        return (
          <div key={nm} style={{opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, position: 'absolute', left: x0, top: 250}}>{nm}
              <span style={{fontWeight: 700, fontSize: 32, color: T.accent, marginLeft: 20}}>최고 ÷ 최저 {(mx / mn).toFixed(2)}배</span></div>
            <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
              <line x1={x0} x2={x0 + W} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} />
              {arr.map(([dt, v], i) => {
                const h = y(v) * appear(f, at(s, d.at[j]) + i * 3, 16); const c = v === mx ? T.accent : v === mn ? T.fall : T.ink3;
                return (
                  <g key={dt}>
                    <rect x={x0 + i * (W / 12)} y={base - h} width={bw} height={h} rx={4} fill={c} />
                    {v === mx || v === mn ? <text x={x0 + i * (W / 12) + bw / 2} y={base - h - 12} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={24} fill={c}>{v.toFixed(3)}</text> : null}
                    {i % 3 === 0 ? <text x={x0 + i * (W / 12) + bw / 2} y={base + 30} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={20} fill={T.ink3}>{dt.slice(2, 7).replace('-', '.')}</text> : null}
                  </g>
                );
              })}
            </svg>
          </div>
        );
      })}
    </Page>
  );
};

// ───── 12. 세후 월 100만원 원금 ─────
const Need: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const items: [string, number][] = d.items; const when = [2, 2, 4, 3, 3, 4];
  const X0 = 700, x = scaleLinear().domain([0, 45000]).range([0, 860]);
  return (
    <Page s={s}>
      <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2, position: 'absolute', left: 1180, top: 184, padding: '8px 20px', border: `2px solid ${T.ink3}`, borderRadius: 30,
        opacity: appear(f, at(s, 1))}}>ISA·연금계좌는 방식이 다름</div>
      {items.map(([n, v], i) => {
        const o = appear(f, at(s, when[i]) + (i % 2) * 24, 22); const y = 262 + i * 98;
        return (
          <div key={n} style={{position: 'absolute', top: y, left: 0, width: 1920, opacity: Math.min(1, o * 2)}}>
            <div style={{...F, fontWeight: 700, fontSize: n.length > 10 ? 28 : 40, color: T.ink, position: 'absolute', right: 1920 - X0 + 24, top: n.length > 10 ? 18 : 10, whiteSpace: 'nowrap'}}>{n}</div>
            <div style={{position: 'absolute', left: X0, top: 6, width: x(v) * o, height: 60, background: n.startsWith('KODEX') ? T.fall : n === 'SCHD' ? T.ink2 : T.accent, borderRadius: 8}} />
            <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, position: 'absolute', left: X0 + x(v) * o + 20, top: 10, whiteSpace: 'nowrap'}}>{d.labels[n]}</div>
          </div>
        );
      })}
    </Page>
  );
};

// ───── 13. 한 장 정리 ─────
const Summary: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cells: string[][] = s.data.cells; const when = [1, 1, 2, 3];
  return (
    <Page s={s}>
      {cells.map(([h, big, small], i) => {
        const o = appear(f, at(s, when[i]) + (i === 1 ? 50 : 0), 18);
        return (
          <Card key={h} x={140 + (i % 2) * 830} y={250 + Math.floor(i / 2) * 310} w={810} h={290} o={o}>
            <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, position: 'absolute', left: 40, top: 32}}>{h}</div>
            <div style={{...F, fontWeight: 700, fontSize: 54, color: T.ink, position: 'absolute', left: 40, top: 96, wordBreak: 'keep-all', right: 40}}>{big}</div>
            <div style={{...F, fontWeight: 700, fontSize: 32, color: T.accent, position: 'absolute', left: 40, bottom: 36}}>{small}</div>
          </Card>
        );
      })}
    </Page>
  );
};

// ───── 14. 계산기 입력 → 은퇴 나이 기둥 ─────
const Age: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const A = d.at.map((i: number) => at(s, i));
  const base = 820, y = scaleLinear().domain([40, 65]).range([0, 520]); const x0 = 860, cw = 150;
  return (
    <Page s={s}>
      <Card x={140} y={250} w={620} h={600} o={appear(f, at(s, 0) + 20)}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, position: 'absolute', left: 36, top: 28}}><Flame size={24} />
          <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink}}>은퇴 계산기</span></div>
        {d.inputs.map(([k, v]: string[], i: number) => (
          <div key={k} style={{position: 'absolute', left: 36, right: 36, top: 100 + i * 78, height: 62, borderRadius: 12, background: T.bg, display: 'flex',
            alignItems: 'center', justifyContent: 'space-between', padding: '0 22px', opacity: appear(f, at(s, 1) + i * 12)}}>
            <span style={{...F, fontWeight: 500, fontSize: 26, color: T.ink2}}>{k}</span><span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink}}>{v}</span>
          </div>))}
      </Card>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={x0 - 20} x2={x0 + cw * 6} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} />
        {d.ages.map(([r, a]: number[], i: number) => {
          const key = r === 4 || r === 6; const o = appear(f, key ? A[0] + (r === 6 ? 30 : 0) : A[2] + i * 8, 20); const h = y(a) * o;
          return (
            <g key={r} opacity={Math.min(1, o * 2)}>
              <rect x={x0 + i * cw} y={base - h} width={cw - 30} height={h} rx={8} fill={key ? T.accent : T.ink3} />
              <text x={x0 + i * cw + (cw - 30) / 2} y={base - h - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={key ? T.accent : T.ink}>{a}세</text>
              <text x={x0 + i * cw + (cw - 30) / 2} y={base + 38} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2}>연 {r}%</text>
            </g>
          );
        })}
      </svg>
      <div style={{...F, fontWeight: 700, fontSize: 36, color: '#fff', background: T.accent, borderRadius: 30, padding: '8px 26px', position: 'absolute', left: 1180, top: 220,
        opacity: appear(f, A[1])}}>2%포인트 차이 = 6년</div>
    </Page>
  );
};

// ───── 15. 마무리: 원문 인용 + 카페·계산기 ─────
const Close: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o = appear(f, 0, 16);
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      <div style={{position: 'absolute', left: 200, right: 200, top: 160, opacity: o}}>
        <div style={{fontFamily: 'Georgia, serif', fontSize: 120, color: T.daccent, lineHeight: 1}}>“</div>
        <div style={{fontFamily: 'Georgia, serif', fontStyle: 'italic', fontSize: 44, color: T.dink3, lineHeight: 1.4}}>{d.quote}</div>
        <div style={{...F, fontWeight: 700, fontSize: 54, color: T.dink, marginTop: 30, lineHeight: 1.35}}>{d.ko}</div>
        <div style={{...F, fontWeight: 500, fontSize: 26, color: T.dink3, marginTop: 18}}>{d.src}</div>
      </div>
      <div style={{position: 'absolute', left: 200, top: 700, display: 'flex', gap: 24}}>
        {d.cta.map((t: string, i: number) => <div key={t} style={{...F, fontWeight: 700, fontSize: 38, color: T.dink, background: T.dsurface, borderRadius: 18, padding: '18px 32px',
          border: `3px solid ${i ? T.daccent : T.dsurface}`, opacity: appear(f, at(s, 1 + i))}}>{t}</div>)}
      </div>
      <Caption s={s} dark />
    </AbsoluteFill>
  );
};

const View: React.FC<S> = ({s}) => {
  switch (s.kind) {
    case 'open': return <Open s={s} />; case 'logo': return <LogoSting sub={s.data.sub} />; case 'agenda': return <Agenda s={s} />;
    case 'structure': return <Structure s={s} />; case 'pairs': return <Pairs s={s} />; case 'stack': return <Stack s={s} />; case 'lines': return <Lines s={s} />;
    case 'neg': return <Neg s={s} />; case 'won': return <Won s={s} />; case 'holdings': return <Holdings s={s} />; case 'tax': return <Tax s={s} />;
    case 'taxbars': return <TaxBars s={s} />; case 'line2k': return <Line2k s={s} />; case 'monthly': return <Monthly s={s} />; case 'need': return <Need s={s} />;
    case 'summary': return <Summary s={s} />; case 'age': return <Age s={s} />; default: return <Close s={s} />;
  }
};

export const A1: React.FC<A1Props> = ({scenes}) => {
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
