// P-1 "국민연금 수령나이: 당기기·제때·미루기, 그리고 60대에 일하면" 화면 — 재료 work/video/p1.json(ep/P-1/p1props.py가 script.md·voice.json·calc_out·facts로 만든다)
// 틀은 TallyFrame(제목·형광 부제·흰 보드·정확한 값 칩·말 자막·출처). 색·글꼴은 parts/fm 토큰 그대로.
// 그림 종류: 예고 카드 · 결론 점수판 · 생일 카드 · 출생연도 계단 · 가상 인물 카드 · 세 칸 점수판+속도 막대 · 누적 두(세) 선 · 1~5년 표 · 기대여명 막대 · 누적 막대 경주 ·
//   StepCliff(5장 계단) · 환급 카드·도장 · '법 개정 아님' 도장 · 정리 타일 · 실사 장 머리(StockShot, 1·4·5·6장 첫 줄).
// U5(같은 화면 8초 이하): 말 줄이 바뀔 때마다 판의 큰 칸(검은 카드·칸 반전·막대 다시 자람)이 바뀐다. 숫자 글자는 그림 위에 두지 않는다(겹침 0).
// 숫자 글자는 전부 p1.json에서 온다. 코드 안 숫자는 배치·눈금뿐.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, HandCircle} from './parts/fm';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';
import {StepCliff, StepCliffProps} from './motion/StepCliff';
import {StockShot, StockShotProps} from './motion/StockShot';

type PLine = TallyLine & {audio?: string | null};
export type PScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: PLine[]; frames: number; stock?: StockShotProps};
export type P1Props = {fps: number; scenes: PScene[]; missing: number};
export const p1Frames = (p: P1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);
const ease = (f: number, a: number, d: number) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const Y0 = 345;

// 줄 박자: k = 지금 말하는 줄, at(i) = i번째 줄 시작(장면 안). 대본에서 못 찾은 박자(-1)는 1e9(안 나옴).
const useBeat = (s: PScene) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines); const n = s.lines.length;
  const k = Math.max(0, tallyIdx(s.lines, f));
  const at = (i: number) => (i == null || i < 0) ? 1e9 : st[Math.min(n - 1, i)] ?? 0;
  return {f, k, at, n, end: s.frames};
};
const beatOf = (ats: number[], at: (i: number) => number, f: number) => { let b = -1; ats.forEach((i, j) => { if (f >= at(i)) b = j; }); return b; };

const Box: React.FC<{x: number; y: number; w: number; h: number; o?: number; bg?: string; border?: string; r?: number; children?: React.ReactNode; dy?: number; center?: boolean; pad?: string}> =
  ({x, y, w, h, o = 1, bg = '#fff', border, r = 18, children, dy = 0, center = true, pad = '14px 24px'}) => o <= 0 ? null : (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 10 + dy, width: w, height: h, opacity: o, background: bg, border: border ?? 'none', borderRadius: r,
    boxSizing: 'border-box', padding: pad, display: 'flex', flexDirection: 'column', justifyContent: center ? 'center' : 'flex-start', overflow: 'hidden'}}>{children}</div>
);
const Txt: React.FC<{s: number; c?: string; w?: number; children: React.ReactNode; al?: 'left' | 'center' | 'right'; wrap?: boolean}> = ({s, c = T.ink, w = 700, children, al = 'left', wrap}) => (
  <div style={{...F, fontWeight: w, fontSize: s, color: c, lineHeight: 1.2, textAlign: al, whiteSpace: wrap ? 'normal' : 'nowrap', wordBreak: 'keep-all'}}>{children}</div>
);

// ───────── 0. 예고: 검은 바탕, 줄마다 카드 한 장 ─────────
const Mini: React.FC<{kind: string}> = ({kind}) => {
  const a = T.daccent, w = '#fff';
  if (kind === 'step') return <svg width={360} height={300}><path d="M20 250 H190 V120 H250 V90 H340" fill="none" stroke={a} strokeWidth={12} strokeLinejoin="round" /><line x1={20} y1={262} x2={340} y2={262} stroke={T.dink3} strokeWidth={4} /></svg>;
  if (kind === 'cross') return <svg width={360} height={300}><path d="M20 230 L340 120" stroke={T.dfall} strokeWidth={10} fill="none" /><path d="M110 270 L340 40" stroke={a} strokeWidth={10} fill="none" /><circle cx={222} cy={160} r={16} fill={w} /></svg>;
  if (kind === 'bars') return <svg width={360} height={300}><rect x={20} y={70} width={250} height={70} rx={10} fill={T.dfall} /><rect x={20} y={170} width={320} height={70} rx={10} fill={a} /></svg>;
  if (kind === 'refund') return <svg width={360} height={300}><rect x={40} y={60} width={280} height={190} rx={18} fill="none" stroke={w} strokeWidth={8} /><path d="M40 70 L180 170 L320 70" fill="none" stroke={a} strokeWidth={8} /></svg>;
  if (kind === 'stamp') return <svg width={360} height={300}><g transform="rotate(-12 180 150)"><rect x={40} y={80} width={280} height={140} rx={16} fill="none" stroke={T.rise} strokeWidth={10} /><line x1={60} y1={150} x2={300} y2={150} stroke={T.rise} strokeWidth={8} /></g></svg>;
  return <svg width={360} height={300}>{[0, 1, 2].map((i) => <rect key={i} x={20 + i * 115} y={90} width={95} height={130} rx={12} fill={i === 1 ? a : 'none'} stroke={w} strokeWidth={6} />)}</svg>;
};
const Teaser: React.FC<{s: PScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const c = s.data.cards[Math.min(k, s.data.cards.length - 1)]; const o = fade(f, at(k), 7);
  return (
    <>
      <AbsoluteFill style={{background: T.dbg}} />
      <div style={{position: 'absolute', right: 120, top: 60}}><Txt s={30} c={T.dink3}>{s.title}</Txt></div>
      <div style={{position: 'absolute', left: 300, top: 250, width: 1320, height: 500, opacity: o, transform: `scale(${0.96 + 0.04 * o})`, background: T.dsurface, borderRadius: 28,
        display: 'flex', alignItems: 'center', gap: 50, padding: '0 60px', boxSizing: 'border-box'}}>
        <Mini kind={c[0]} />
        <div>
          <Txt s={c[1].length > 14 ? 58 : 76} c="#fff">{c[1]}</Txt>
          <div style={{height: 18}} />
          <Txt s={44} c={T.daccent}>{c[2]}</Txt>
          {c[3] ? <><div style={{height: 22}} /><Txt s={28} c={T.dink3} w={500}>{c[3]}</Txt></> : null}
        </div>
      </div>
    </>
  );
};

// ───────── 결론부터 ─────────
const Cells: React.FC<{cells: string[][]; x: number; y: number; w: number; h: number; gap: number; on: (i: number) => boolean; o: number; big?: number}> = ({cells, x, y, w, h, gap, on, o, big = 64}) => (
  <>{cells.map((c, i) => (
    <Box key={i} x={x + i * (w + gap)} y={y} w={w} h={h} o={o} bg={on(i) ? T.ink : '#fff'} border={on(i) ? 'none' : `3px solid ${T.line}`}>
      <Txt s={34} c={on(i) ? T.daccent : T.ink3} al="center">{c[0]}</Txt>
      <Txt s={big} c={on(i) ? '#fff' : T.ink} al="center">{c[1]}</Txt>
      {c[2] ? <Txt s={28} c={on(i) ? T.dink3 : T.ink2} al="center">{c[2]}</Txt> : null}
    </Box>
  ))}</>
);
const Concl: React.FC<{s: PScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const word = 1 - ease(f, at(1), 12);
  return (
    <>
      <Cells cells={k >= 1 ? d.cells.map((c: string[]) => [c[0], c[1], d.q]) : d.cells} x={190} y={Y0 + 20} w={460} h={k >= 2 ? 250 : 400} gap={70} on={() => k >= 1} o={k >= 1 ? 1 : 0.35} />
      {word > 0 ? <Box x={460} y={Y0 + 90} w={1000} h={260} bg={T.accent} o={word}><Txt s={130} c="#fff" al="center">{s.title}</Txt></Box> : null}
      <Box x={190} y={Y0 + 300} w={1540} h={160} bg={T.soft} o={fade(f, at(2), 10)}>
        <div style={{display: 'flex', alignItems: 'center', gap: 40}}>
          <svg width={200} height={110}><path d="M10 100 H100 V40 H190" fill="none" stroke={T.accent} strokeWidth={12} strokeLinejoin="round" /></svg>
          <div><Txt s={52}>{d.stair}</Txt><Txt s={28} c={T.ink2}>{d.chip}</Txt></div>
        </div>
      </Box>
    </>
  );
};

// ───────── 1장 ─────────
const Birth: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const t1 = at(1);
  return (
    <>
      {d.cards.map((c: string[], i: number) => (
        <React.Fragment key={i}>
          <Box x={220 + i * 840} y={Y0 + 10} w={640} h={240} o={fade(f, t1, 10)} border={`3px solid ${T.line}`}>
            <Txt s={30} c={T.ink3} al="center">생일</Txt><Txt s={86} al="center">{c[0]}</Txt>
          </Box>
          <Box x={220 + i * 840} y={Y0 + 280} w={640} h={190} bg={i ? T.accent : T.ink} o={fade(f, t1 + 30 + i * 14, 10)}>
            <Txt s={30} c={i ? '#fff' : T.dink3} al="center">{c[1]}</Txt><Txt s={84} c="#fff" al="center">{c[2]}</Txt>
          </Box>
        </React.Fragment>
      ))}
      <Box x={880} y={Y0 + 85} w={160} h={90} bg={T.soft} o={fade(f, t1 + 14, 10)}><Txt s={40} al="center">{d.band}</Txt></Box>
    </>
  );
};
const Stairs: React.FC<{s: PScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data; const n = d.rows.length;
  const blink = k >= 1 ? Math.floor((f - at(1)) / 12) % n : -1;
  return (
    <>{d.rows.map((r: string[], i: number) => {
      const h = 130 + i * 55; const x = 200 + i * 310; const g = ease(f, at(0) + i * 8, 16); const on = i === blink || (k === 0 && i === n - 1);
      return (
        <React.Fragment key={i}>
          <div style={{position: 'absolute', left: x, top: 790 - h * g, width: 270, height: h * g, background: on ? T.accent : i === n - 1 ? T.ink : T.ink2, borderRadius: '14px 14px 0 0'}} />
          <div style={{position: 'absolute', left: x, top: 790 - h - 70, width: 270, opacity: g}}><Txt s={50} al="center">{r[1]}</Txt></div>
          <div style={{position: 'absolute', left: x, top: 800, width: 270}}><Txt s={30} c={T.ink2} al="center">{r[0]}</Txt></div>
        </React.Fragment>
      );
    })}
    {k >= 1 ? <Box x={200} y={Y0 + 5} w={420} h={80} bg={T.soft} o={fade(f, at(1), 8)}><Txt s={36} al="center">{d.mine}</Txt></Box> : null}
    </>
  );
};
const Person: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data;
  return (
    <>
      <Box x={180} y={Y0 + 10} w={520} h={470} o={fade(f, 0, 10)} border={`3px solid ${T.line}`} center={false} pad="24px">
        <svg width={472} height={300} viewBox="0 0 472 300"><circle cx={236} cy={90} r={62} fill={T.ink2} /><path d="M116 300 C116 200 176 170 236 170 C296 170 356 200 356 300 Z" fill={T.ink2} /></svg>
        <div style={{display: 'flex', gap: 14, alignItems: 'center', justifyContent: 'center', marginTop: 16}}>
          <Txt s={44}>{d.name}</Txt>
          <div style={{background: T.accent, borderRadius: 8, padding: '2px 12px'}}><Txt s={26} c="#fff">{d.tag}</Txt></div>
        </div>
      </Box>
      <Box x={760} y={Y0 + 10} w={960} h={220} o={fade(f, 12, 10)} bg={T.ink}>
        <Txt s={34} c={T.dink3}>{d.bill[0]}</Txt>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 16}}><Txt s={90} c="#fff">{d.bill[1]}</Txt><Txt s={40} c={T.daccent}>{d.bill[2]}</Txt></div>
      </Box>
      <Box x={760} y={Y0 + 260} w={960} h={210} bg={T.accent} o={f >= at(2) ? 0 : fade(f, at(1), 10)}><Txt s={60} c="#fff">{d.first}</Txt></Box>
      {f >= at(2) ? <Box x={760} y={Y0 + 260} w={960} h={210} bg={T.fall} o={fade(f, at(2), 10)}><Txt s={44} c="#fff" wrap>{d.same}</Txt></Box> : null}
    </>
  );
};

// ───────── 2장 점수판 ─────────
const Board: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const act = b <= 0 ? 1 : b <= 2 ? 0 : b <= 4 ? 2 : -1;
  const shrink = ease(f, at(d.at[5]), 14); const h = 330 - 150 * shrink;
  const show = (i: number) => i === 1 ? b >= 0 : i === 0 ? b >= 1 : b >= 3;
  return (
    <>
      {d.cells.map((c: string[], i: number) => {
        const on = i === act; const o = show(i) ? 1 : 0.3;
        return (
          <Box key={i} x={170 + i * 540} y={Y0 + 30} w={500} h={h} bg={on ? T.ink : '#fff'} border={on ? 'none' : `3px solid ${T.line}`} o={o}>
            <Txt s={32} c={on ? T.daccent : T.ink3} al="center">{c[0]} · {c[1]}</Txt>
            <Txt s={86 - 20 * shrink} c={on ? '#fff' : T.ink} al="center">{show(i) ? c[2] : '?'}</Txt>
          </Box>
        );
      })}
      {[0, 2].map((i) => {
        const bt = i === 0 ? 2 : 4; const o = (b >= bt ? 1 : 0) * (1 - shrink);
        return o > 0 ? <Box key={i} x={170 + i * 540} y={Y0 + 380} w={500} h={110} bg={i ? T.accent : T.fall} o={o * fade(f, at(d.at[bt]), 8)}><Txt s={50} c="#fff" al="center">{d.cells[i][3]}</Txt></Box> : null;
      })}
      {b === 5 ? (
        <Box x={170} y={Y0 + 230} w={1580} h={260} o={fade(f, at(d.at[5]) + 8, 10)} border={`3px solid ${T.line}`}>
          {d.speed.map((r: any[], i: number) => (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, margin: '12px 0'}}>
              <div style={{width: 220}}><Txt s={32} c={T.ink2}>{r[0]}</Txt></div>
              <div style={{width: 1000 * (r[1] / 7.2) * ease(f, at(d.at[5]) + 12 + i * 10, 18), height: 70, background: i ? T.accent : T.fall, borderRadius: 10}} />
              <Txt s={40}>{r[2]}</Txt>
            </div>
          ))}
        </Box>
      ) : null}
      {b === 6 ? <Box x={170} y={Y0 + 230} w={1580} h={260} bg={T.accent} o={fade(f, at(d.at[6]), 8)}><Txt s={110} c="#fff" al="center">{d.warn}</Txt><Txt s={36} c="#fff" al="center">{d.rule[0]}</Txt></Box> : null}
      {b === 7 ? (
        <Box x={170} y={Y0 + 230} w={1580} h={260} bg={T.ink} o={fade(f, at(d.at[7]), 8)}>
          <Txt s={32} c={T.daccent}>{d.rule[0]} · {d.rule[2]}</Txt><div style={{height: 14}} /><Txt s={50} c="#fff">'{d.rule[1]}'</Txt>
        </Box>
      ) : null}
      {b >= 8 ? <Box x={170} y={Y0 + 230} w={1580} h={260} bg={T.soft} o={fade(f, at(d.at[8]), 8)}><Txt s={64} al="center">{d.dep}</Txt></Box> : null}
    </>
  );
};

// ───────── 3장 누적 선 ─────────
const CX0 = 250, CX1 = 1330, CY0 = 790, CY1 = 410;
const Cross: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const cv: number[][] = d.curve; const ymax = 33000;
  const X = (a: number) => CX0 + (a - 60) / 30 * (CX1 - CX0); const Y = (v: number) => CY0 - v / ymax * (CY0 - CY1);
  const path = (j: number, t: number) => { const last = 60 + 30 * t; let p = ''; cv.forEach((r) => { if (r[0] <= last) p += (p ? 'L' : 'M') + X(r[0]) + ',' + Y(r[j]); }); return p; };
  const t0 = ease(f, at(d.at[0]), 90); const t2 = ease(f, at(d.at[4]), 60);
  const yE = Y(cv[0][1] + (d.xe - 60) * 12 * 70);
  const shade = cv.filter((r) => r[0] <= d.xe).map((r) => `${X(r[0])},${Y(r[1])}`).join(' ') + ' ' + cv.filter((r) => r[0] <= d.xe).reverse().map((r) => `${X(r[0])},${Y(r[2])}`).join(' ');
  const cols = [T.fall, T.ink, T.accent];
  return (
    <>
      <div style={{position: 'absolute', left: CX0, top: Y0, display: 'flex', gap: 30}}>
        {d.names.map((n: string, i: number) => (i < 2 || b >= 4) ? <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10}}><div style={{width: 34, height: 10, background: cols[i], borderRadius: 4}} /><Txt s={26} c={T.ink2}>{n}</Txt></div> : null)}
      </div>
      <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}>
        {[60, 65, 70, 75, 80, 85, 90].map((a) => <g key={a}><line x1={X(a)} y1={CY0} x2={X(a)} y2={CY0 + 10} stroke={T.ink3} strokeWidth={2} /><text x={X(a)} y={CY0 + 40} textAnchor="middle" fontSize={24} fill={T.ink3} style={{...F, fontWeight: 700}}>{a}세</text></g>)}
        <line x1={CX0} y1={CY0} x2={CX1} y2={CY0} stroke={T.ink3} strokeWidth={3} />
        {b >= 1 && b < 4 ? <polygon points={shade} fill={T.fall} opacity={0.18 * fade(f, at(d.at[1]), 12)} /> : null}
        <path d={path(1, t0)} stroke={cols[0]} strokeWidth={8} fill="none" strokeLinecap="round" />
        <path d={path(2, t0)} stroke={cols[1]} strokeWidth={8} fill="none" strokeLinecap="round" />
        {b >= 4 ? <path d={path(3, t2)} stroke={cols[2]} strokeWidth={8} fill="none" strokeLinecap="round" /> : null}
        {b >= 2 ? <circle cx={X(d.xe)} cy={yE} r={18 * fade(f, at(d.at[2]), 8)} fill="#fff" stroke={T.ink} strokeWidth={6} /> : null}
        {b >= 3 ? <line x1={X(d.xe)} y1={yE + 20} x2={X(d.xe)} y2={CY0} stroke={T.ink} strokeWidth={3} strokeDasharray="8 8" /> : null}
        {b >= 4 && t2 > 0.78 ? <circle cx={X(d.xd)} cy={Y((d.xd - 65) * 12 * 100)} r={18} fill="#fff" stroke={T.accent} strokeWidth={6} /> : null}
      </svg>
      <Box x={1400} y={Y0 + 20} w={380} h={200} bg={T.ink} o={fade(f, at(d.at[3]), 10)}><Txt s={30} c={T.dink3}>당김 = 제때</Txt><Txt s={72} c="#fff">{d.flags[0]}</Txt></Box>
      <Box x={1400} y={Y0 + 250} w={380} h={200} bg={T.accent} o={fade(f, at(d.at[4]) + 50, 10)}><Txt s={30} c="#fff">제때 = 미룸</Txt><Txt s={72} c="#fff">{d.flags[1]}</Txt></Box>
      {b >= 1 && b < 3 ? <Box x={1400} y={Y0 + 20} w={380} h={200} bg={b === 1 ? T.fall : T.soft} o={1}><Txt s={44} c={b === 1 ? '#fff' : T.ink}>{b === 1 ? '당김이 앞섬' : '제때가 따라잡음'}</Txt></Box> : null}
    </>
  );
};

// ───────── 3장 1~5년 표 ─────────
const Years: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const W = [150, 210, 230, 210, 230]; const X0 = 150; const RH = 66;
  const xs = W.map((_, i) => X0 + W.slice(0, i).reduce((a, v) => a + v, 0));
  const hi = (r: number, c: number) => (b === 1 && r === 0 && c <= 2) || (b === 2 && r === 0 && (c === 0 || c >= 3)) || (b === 3 && (c === 2 || c === 4));
  const card: [string, string, string, string] = ([['?', s.title, '', '#fff'], ['1년 당김', d.rows[0][2], '따라잡히는 나이', T.ink], ['1년 미룸', d.rows[0][4], '앞서는 나이', T.fall],
    ['오래 당길수록', '↓ 빨라짐', '오래 미룰수록 ↑ 늦어짐', T.accent], [d.b64[0], d.b64[1], d.b64[2], T.ink]] as [string, string, string, string][])[Math.max(0, b)];
  return (
    <>
      {d.cols.map((c: string, i: number) => <div key={i} style={{position: 'absolute', left: xs[i], top: Y0 + 5, width: W[i]}}><Txt s={24} c={T.ink3} al="center">{c}</Txt></div>)}
      {d.rows.map((r: string[], ri: number) => (
        <React.Fragment key={ri}>
          {r.map((v, ci) => {
            const on = hi(ri, ci);
            return <div key={ci} style={{position: 'absolute', left: xs[ci] + 3, top: Y0 + 50 + ri * RH, width: W[ci] - 6, height: RH - 8, borderRadius: 10, opacity: fade(f, ri * 6, 10),
              background: on ? (b === 2 ? T.fall : b === 3 ? T.accent : T.ink) : ri % 2 ? '#fff' : T.bg, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <Txt s={32} c={on ? '#fff' : T.ink}>{v}</Txt></div>;
          })}
        </React.Fragment>
      ))}
      <Box x={1230} y={Y0 + 50} w={550} h={320} bg={card[3]} border={b <= 0 ? `3px solid ${T.line}` : undefined} o={1}>
        <Txt s={32} c={b <= 0 ? T.ink3 : '#fff'} wrap>{card[0]}</Txt><div style={{height: 10}} />
        <Txt s={b <= 0 ? 60 : 64} c={b <= 0 ? T.ink : '#fff'} wrap>{card[1]}</Txt><div style={{height: 10}} />
        {card[2] ? <Txt s={b >= 3 ? 36 : 30} c={b <= 0 ? T.ink2 : '#fff'} wrap>{card[2]}</Txt> : null}
      </Box>
    </>
  );
};

// ───────── 4장 기대여명 막대 ─────────
const LX0 = 300, LX1 = 1500;
const Life: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const X = (a: number) => LX0 + (a - 60) / 35 * (LX1 - LX0);
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}>
          {[60, 65, 70, 75, 80, 85, 90, 95].map((a) => <text key={a} x={X(a)} y={720} textAnchor="middle" fontSize={24} fill={T.ink3} style={{...F, fontWeight: 700}}>{a}세</text>)}
          <line x1={LX0} y1={690} x2={LX1} y2={690} stroke={T.ink3} strokeWidth={3} />
          {d.ticks.map((t: any[], i: number) => b >= 3 + i ? <g key={i} opacity={fade(f, at(d.at[3 + i]), 10)}><line x1={X(t[0])} y1={420} x2={X(t[0])} y2={690} stroke={i ? T.accent : T.ink} strokeWidth={4} strokeDasharray="10 8" /></g> : null)}
        </svg>
        {d.bars.map((r: any[], i: number) => {
          const g = ease(f, at(d.at[1 + i]), 20); if (g <= 0) return null;
          return (
            <React.Fragment key={i}>
              <div style={{position: 'absolute', left: 220, top: 455 + i * 120, width: 60}}><Txt s={40} c={T.ink2}>{r[0]}</Txt></div>
              <div style={{position: 'absolute', left: X(65), top: 450 + i * 120, width: (X(r[1]) - X(65)) * g, height: 80, background: i ? T.accent : T.fall, borderRadius: 10}} />
              <div style={{position: 'absolute', left: X(r[1]) + 16, top: 452 + i * 120, opacity: g}}><Txt s={40}>{r[2]}</Txt><Txt s={24} c={T.ink2}>{r[3]}</Txt></div>
            </React.Fragment>
          );
        })}
        {d.ticks.map((t: any[], i: number) => b >= 3 + i ? <div key={i} style={{position: 'absolute', left: X(t[0]) - 90, top: 372, width: 180, opacity: fade(f, at(d.at[3 + i]), 10)}}><Txt s={30} c={i ? T.accent : T.ink} al="center">{t[1]}</Txt></div> : null)}
      </div>
      {b >= 5 ? <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}><HandCircle cx={X(d.ticks[1][0]) + 4} cy={490} rx={32} ry={62} p={ease(f, at(d.at[5]), 16)} /></svg> : null}
      {b >= 3 ? <Box x={300} y={750} w={620} h={90} bg={b >= 5 ? T.accent : T.ink} o={fade(f, at(d.at[3]), 10)}><Txt s={34} c="#fff">{d.ticks[0][1]} · {d.ticks[0][2]}</Txt></Box> : null}
      {b >= 4 ? <Box x={960} y={750} w={760} h={90} bg={b >= 5 ? T.ink : T.accent} o={fade(f, at(d.at[4]), 10)}><Txt s={34} c="#fff">{d.ticks[1][1]} ↔ {d.bars[0][2]} · {d.gap}</Txt></Box> : null}
    </>
  );
};

// ───────── 4장 누적 막대 경주 ─────────
const Race: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const W = b >= 3; const rows = W ? d.w : d.m; const max = 310000000; const g = ease(f, at(d.at[W ? 3 : 0]), 30);
  return (
    <>
      <Box x={170} y={Y0} w={520} h={64} bg={W ? T.accent : T.fall} o={1} key={W ? 'w' : 'm'}><Txt s={32} c="#fff">{W ? d.wAge : d.mAge}</Txt></Box>
      {b < 6 && rows.map((r: any[], i: number) => (
        <div key={i}>
          <div style={{position: 'absolute', left: 170, top: Y0 + 100 + i * 100, width: 110}}><Txt s={36} c={T.ink2}>{r[0]}</Txt></div>
          <div style={{position: 'absolute', left: 290, top: Y0 + 90 + i * 100, width: 950 * r[1] / max * g, height: 70, background: i === 2 ? T.accent : i === 1 ? T.ink : T.fall, borderRadius: 10}} />
          <div style={{position: 'absolute', left: 290 + 950 * r[1] / max * g + 16, top: Y0 + 100 + i * 100, opacity: g}}><Txt s={36}>{r[2]}</Txt></div>
        </div>
      ))}
      {b >= 1 && b < 3 ? <Box x={170} y={Y0 + 400} w={700} h={100} bg={T.ink} o={fade(f, at(d.at[1]), 8)}><Txt s={40} c="#fff">{d.chips[0]}</Txt></Box> : null}
      {b === 2 ? <Box x={900} y={Y0 + 400} w={700} h={100} bg={T.accent} o={fade(f, at(d.at[2]), 8)}><Txt s={40} c="#fff">{d.chips[1]}</Txt></Box> : null}
      {b === 4 ? <Box x={170} y={Y0 + 400} w={760} h={100} bg={T.accent} o={fade(f, at(d.at[4]), 8)}><Txt s={40} c="#fff">{d.chips[2]}</Txt></Box> : null}
      {b === 5 ? <Box x={170} y={Y0 + 400} w={1560} h={100} bg={T.ink} o={fade(f, at(d.at[5]), 8)}><Txt s={40} c="#fff">{d.arrow[0]}  ·  {d.arrow[1]}</Txt></Box> : null}
      {b === 6 ? <Box x={360} y={Y0 + 110} w={1200} h={240} bg={T.ink} o={fade(f, at(d.at[6]), 8)}><Txt s={84} c="#fff" al="center">{d.ans}</Txt></Box> : null}
      {b >= 7 ? d.two.map((t: string, i: number) => <Box key={i} x={250 + i * 740} y={Y0 + 110} w={680} h={240} bg={i ? T.accent : T.ink} o={fade(f, at(d.at[7]) + i * 18, 8)}><Txt s={64} c="#fff" al="center">{t}</Txt></Box>) : null}
    </>
  );
};

// ───────── 6장 환급 ─────────
const Refund: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const A = (i: number) => at(d.at[i]);
  return (
    <>
      <Box x={170} y={Y0} w={1580} h={70} bg={T.soft} o={fade(f, 0, 8)}><Txt s={30}>{d.law}</Txt></Box>
      <Box x={170} y={Y0 + 95} w={1000} h={200} o={fade(f, A(1), 10)} border={`3px solid ${T.ink}`}><Txt s={34} c={T.ink2}>{d.who[0]}</Txt><div style={{height: 10}} /><Txt s={46}>{d.who[1]}</Txt></Box>
      {f >= A(2) ? <div style={{position: 'absolute', left: 1240, top: Y0 + 110, width: 480, height: 170, border: `8px solid ${T.rise}`, borderRadius: 18, transform: `rotate(-6deg) scale(${1.3 - 0.3 * ease(f, A(2), 8)})`, opacity: fade(f, A(2), 6),
        display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#fff'}}><Txt s={44} c={T.rise}>{d.stamp}</Txt></div> : null}
      <Box x={170} y={Y0 + 320} w={640} h={180} bg={T.ink} o={fade(f, A(3), 10)}><Txt s={84} c="#fff">{d.big[0]}</Txt><Txt s={32} c={T.daccent}>{d.big[1]}</Txt></Box>
      <Box x={840} y={Y0 + 320} w={420} h={180} bg={T.accent} o={fade(f, A(4), 10)}><Txt s={32} c="#fff">{d.avg[0]}</Txt><Txt s={64} c="#fff">{d.avg[1]}</Txt></Box>
      <Box x={1290} y={Y0 + 320} w={460} h={180} bg={T.fall} o={fade(f, A(5), 10)}><Txt s={26} c="#fff">{d.ex[0]}</Txt><Txt s={34} c="#fff">{d.ex[1]}</Txt><Txt s={26} c="#fff" wrap>{d.ex[2]}</Txt></Box>
    </>
  );
};

// ───────── 7장 68세 ─────────
const Stamp: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const A = (i: number) => at(d.at[i]);
  return (
    <>
      <Box x={180} y={Y0 + 10} w={680} h={300} bg={f >= A(1) ? T.bg : T.ink} o={fade(f, 0, 10)}><Txt s={200} c={f >= A(1) ? T.ink : '#fff'} al="center">{d.big}</Txt></Box>
      <Box x={180} y={Y0 + 330} w={680} h={110} bg={T.ink} o={fade(f, A(1), 8)}><Txt s={46} c="#fff" al="center">{d.tag}</Txt></Box>
      {f >= A(2) ? <div style={{position: 'absolute', left: 980, top: Y0 + 60, width: 680, height: 220, border: `12px solid ${T.rise}`, borderRadius: 24, transform: `rotate(-8deg) scale(${1.4 - 0.4 * ease(f, A(2), 8)})`, opacity: fade(f, A(2), 6),
        display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#fff'}}><Txt s={96} c={T.rise}>{d.stamp}</Txt></div> : null}
      <Box x={960} y={Y0 + 330} w={760} h={110} bg={T.accent} o={fade(f, A(3), 8)}><Txt s={46} c="#fff" al="center">{d.now[0]} · {d.now[1]}</Txt></Box>
    </>
  );
};

// ───────── 마무리 ─────────
const Sum: React.FC<{s: PScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const A = (i: number) => at(d.at[i]); const b = beatOf(d.at, at, f);
  const tiles = [...d.cells, d.line, d.stair];
  return (
    <>
      {b === 0 ? <>
        {tiles.map((t: string[], i: number) => (
          <Box key={i} x={160 + i * 410} y={Y0 + 10} w={380} h={260} o={fade(f, i * 6, 10)} bg={i === 2 ? T.accent : i === 3 ? T.fall : T.ink}>
            <Txt s={30} c="#fff" al="center">{t[0]}</Txt><Txt s={60} c="#fff" al="center">{t[1]}</Txt><Txt s={28} c="#fff" al="center">{t[2]}</Txt>
          </Box>
        ))}
        <Box x={160} y={Y0 + 300} w={1640} h={170} bg="#fff" border={`4px solid ${T.ink}`} o={fade(f, 24, 10)}>
          <Txt s={36} c={T.ink2}>{d.kb[0]}</Txt><Txt s={64}>{d.kb[1]}</Txt>
        </Box>
      </> : null}
      {b === 1 ? <>
        <div style={{position: 'absolute', left: 160, top: Y0 + 10, width: 800, height: 450, borderRadius: 18, overflow: 'hidden', opacity: fade(f, A(1), 10),
          transform: `scale(${0.96 + 0.04 * fade(f, A(1), 12)})`, boxShadow: '0 8px 30px rgba(0,0,0,.18)'}}>
          <img src={staticFile(d.d1.img)} style={{width: 800, height: 450, objectFit: 'cover'}} />
        </div>
        <Box x={1010} y={Y0 + 10} w={790} h={200} bg={T.ink} o={fade(f, A(1) + 10, 10)}><Txt s={32} c={T.daccent}>{d.d1.tag}</Txt><Txt s={64} c="#fff">{d.d1.title}</Txt></Box>
        <Box x={1010} y={Y0 + 240} w={790} h={220} bg="#fff" border={`4px solid ${T.accent}`} o={fade(f, A(1) + 24, 10)}><Txt s={50} wrap>{d.d1.q}</Txt></Box>
      </> : null}
      {b === 2 ? <Box x={160} y={Y0 + 60} w={1640} h={300} bg={T.ink} o={fade(f, A(2), 10)}><Txt s={34} c={T.daccent}>{d.link[0]} · {d.link[2]}</Txt><div style={{height: 16}} /><Txt s={72} c="#fff">{d.link[1]}</Txt></Box> : null}
      {b >= 3 ? <>
        <Box x={160} y={Y0 + 10} w={1640} h={160} bg={T.ink} o={fade(f, A(3), 10)}><Txt s={64} c="#fff" al="center">{d.ask.q}</Txt></Box>
        {d.ask.cells.map((c: string[], i: number) => (
          <Box key={i} x={160 + i * 560} y={Y0 + 200} w={520} h={200} o={fade(f, A(3) + 12 + i * 8, 10)} bg="#fff" border={`4px solid ${T.ink}`}>
            <Txt s={40} c={T.ink2} al="center">{c[0]}</Txt><Txt s={80} c={T.ink} al="center">{c[1]}</Txt>
          </Box>
        ))}
        <div style={{position: 'absolute', left: 160, top: Y0 + 425, width: 1640, opacity: fade(f, A(3) + 40, 10)}}><Txt s={40} c={T.ink2} al="center">{d.ask.tail}</Txt></div>
      </> : null}
    </>
  );
};

const Body: React.FC<{s: PScene}> = ({s}) => {
  switch (s.kind) {
    case 'teaser': return <Teaser s={s} />;
    case 'concl': return <Concl s={s} />;
    case 'birth': return <Birth s={s} />;
    case 'stairs': return <Stairs s={s} />;
    case 'person': return <Person s={s} />;
    case 'board': return <Board s={s} />;
    case 'cross': return <Cross s={s} />;
    case 'years': return <Years s={s} />;
    case 'life': return <Life s={s} />;
    case 'race': return <Race s={s} />;
    case 'step': return <StepCliff {...(s.data.step as StepCliffProps)} />;
    case 'refund': return <Refund s={s} />;
    case 'stamp': return <Stamp s={s} />;
    case 'sum': return <Sum s={s} />;
    default: return null;
  }
};

// 실사 장 머리 위 말 자막(그 장 첫 줄) — TallyFrame 자막과 같은 검은 띠
const StockCap: React.FC<{text: string}> = ({text}) => {
  const u = [...text].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.3 : 0.56), 0);
  return (
    <div style={{position: 'absolute', left: 260, width: 1400, bottom: 56, display: 'flex', justifyContent: 'center'}}>
      <div style={{...F, fontWeight: 700, fontSize: Math.min(56, Math.floor(1330 / Math.max(1, u))), lineHeight: 1.25, color: '#fff', background: T.ink, padding: '10px 32px', borderRadius: 12, whiteSpace: 'nowrap'}}>{text}</div>
    </div>
  );
};

// 정확한 값 칩 — 대본 [자막]이 40자를 넘으면 ' · ' 마디로 나눠 40자 안 쪽으로 묶고 그 줄 길이 안에서 차례로 보인다(bench_check 10/13: 칩 16개가 40자 넘음, 최장 109자)
const CHIP_MAX = 40;
const chipPages = (cap: string) => {
  const parts = cap.split(' · '); const out: string[] = []; let cur = '';
  for (const p of parts) { const nx = cur ? cur + ' · ' + p : p; if (cur && nx.length > CHIP_MAX) { out.push(cur); cur = p; } else cur = nx; }
  if (cur) out.push(cur); return out;
};
const Chip: React.FC<{lines: PLine[]}> = ({lines}) => {
  const f = useCurrentFrame(); const st = tallyStarts(lines); const k = tallyIdx(lines, f);
  let i = -1; for (let j = 0; j <= k; j++) if (lines[j]?.cap) i = j;
  if (i < 0) return null;
  const cap = lines[i].cap as string; const pages = chipPages(cap);
  let nxt = lines.length; for (let j = i + 1; j < lines.length; j++) if (lines[j].cap) { nxt = j; break; }
  const win = (nxt < lines.length ? st[nxt] : st[lines.length - 1] + lines[lines.length - 1].frames) - st[i];   // 다음 칩이 나올 때까지 이 칩 차례
  const per = Math.max(60, Math.floor(win / pages.length));
  const pi = Math.min(pages.length - 1, Math.floor((f - st[i]) / per));
  const a = st[i] + pi * per; const co = interpolate(f, [a, a + 8], [0, 1], CL);
  return (
    <div style={{position: 'absolute', left: 130, top: 252, maxWidth: 1660, opacity: co, transform: `translateY(${(1 - co) * -8}px)`,
      background: T.ink, borderRadius: 10, padding: '7px 16px', display: 'flex', gap: 12, alignItems: 'baseline'}}>
      <span style={{...F, fontWeight: 700, fontSize: 20, color: T.daccent, whiteSpace: 'nowrap'}}>{/\d/.test(cap) ? '정확한 값' : '참고'}{pages.length > 1 ? ` ${pi + 1}/${pages.length}` : ''}</span>
      <span style={{...F, fontWeight: 700, fontSize: 26, color: '#fff', lineHeight: 1.3, whiteSpace: 'nowrap'}}>{pages[pi]}</span>
    </div>
  );
};

// 실사 장 머리가 덮는 동안은 판 그림을 그리지 않는다(가려진 숫자 = 겹침 관문)
const Hold: React.FC<{until: number; children: React.ReactNode}> = ({until, children}) => useCurrentFrame() < until ? null : <>{children}</>;

const SceneView: React.FC<{s: PScene; last: boolean}> = ({s, last}) => {
  const st = tallyStarts(s.lines);
  return (
    <AbsoluteFill>
      <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines.map((l) => ({...l, cap: null}))} board={s.kind !== 'teaser'} capX={last ? 760 : 960}>
        <Hold until={s.stock ? s.stock.dur - 12 : 0}><Body s={s} /></Hold>
        <Chip lines={s.lines} />
      </TallyFrame>
      {s.stock ? <Sequence from={0} durationInFrames={s.stock.dur}><StockShot {...s.stock} /><StockCap text={s.lines[0].text} /></Sequence> : null}
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </AbsoluteFill>
  );
};

export const P1: React.FC<P1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} last={i === p.scenes.length - 1} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
