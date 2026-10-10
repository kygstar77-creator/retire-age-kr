// C-1 "3억으로 매달 200만원 — 배당으로 받기 vs 팔아서 쓰기" 화면 — 재료: work/video/c1.json(ep/C-1/c1props.py가 script.md·voice.json·calc_out.txt·raw로 만든다)
// 틀은 G-1·R-1과 같은 TallyFrame(흰 보드·형광 부제·[자막] 칩·출처). 새 그림은 parts/withdraw.tsx(점수판·통장 통·두 칸 대결·두 사람·문턱 자·해마다 막대·시작 해 칸).
// 숫자 글자는 전부 c1.json에서 온다(calc_out 문구 그대로). 코드 안 숫자는 배치 좌표뿐. 상품 추천·전망 없음. 색: 배당 씨 주황(accent)·매도 씨 파랑(fall).
// v5(10/10): 사람 장면 persona = 기존 부품 Person(두 사람 아이콘) + Stamp('가상 인물' 도장) + TallyReceipt(한 달 영수증·통장) — 차트만 30초 넘게 잇지 않게.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {T, F, CL, LogoSting} from './parts/fm';
import {Stamp} from './parts/receipt';
import {RuleCards, Grid} from './parts/reverse';
import {DivRows} from './parts/gold';
import {ScoreBoard, Tank, VsTiles, Duo, Ruler, YearBars, StartTiles, Person} from './parts/withdraw';
import {TallyFrame, TallyLine, tallyStarts} from './motion/TallyFrame';
import {TallyCountUp} from './motion/TallyCountUp';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyZoom} from './motion/TallyZoom';
import {TallyTag, TallyCallout} from './motion/TallyMark';
import {TallyLineChart, lineXY} from './motion/TallyLineChart';

type CLine = TallyLine & {audio?: string | null};
export type CScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: CLine[]; frames: number};
export type C1Props = {fps: number; scenes: CScene[]; missing: number; script?: string; rate?: number};
export const c1Frames = (p: C1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {ink: T.ink2, ink3: T.ink3, accent: T.accent, rise: T.rise, fall: T.fall};
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const activeRow = (rows: TallyRow[], f: number) => { let k = -1; rows.forEach((r, i) => { if (f >= r.start) k = i; }); return k; };
const toRows = (rows: any[]): TallyRow[] => rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));

const Note: React.FC<{text: string; at: number; x?: number; y?: number; color?: string; size?: number}> = ({text, at, x = 150, y = 760, color = T.ink2, size = 34}) => {
  const f = useCurrentFrame();
  return <div style={{...F, position: 'absolute', left: x, top: y + (1 - fade(f, at)) * 10, fontWeight: 700, fontSize: size, color, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{text}</div>;
};

const Side: React.FC<{side?: [string, number, string]; x?: number; y?: number}> = ({side, x = 150, y = 440}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!side) return null;
  const s = spring({frame: f - side[1], fps, config: {damping: 12}});
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: f >= side[1] ? 1 : 0}}>
      <div style={{...F, fontWeight: 700, fontSize: side[0].length > 8 ? 76 : 104, color: T.accent, lineHeight: 1.05, whiteSpace: 'nowrap', letterSpacing: -2, transform: `scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center'}}>{side[0]}</div>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginTop: 14, whiteSpace: 'nowrap'}}>{side[2]}</div>
    </div>
  );
};

const Drain: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Tank x={220} y={330} w={420} h={380} label={d.tank} out={d.out} inText={d.in} />
      <ScoreBoard cells={d.score} />
    </>
  );
};

const Vs: React.FC<{s: CScene}> = ({s}) => <><VsTiles tiles={s.data.tiles} x={150} y={330} w={1220} /><ScoreBoard cells={s.data.score} /></>;

const GridS: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const rows = d.rows.length;
  return (
    <>
      <Grid cols={d.cols} rows={d.rows} hot={d.hot} x={150} y={300} w={1620} />
      {d.note ? <TallyCallout x={150} y={rows > 2 ? 760 : 700} text={d.note[0]} start={d.note[1]} size={30} /> : null}
    </>
  );
};

const Road: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame();
  const rows: TallyRow[] = s.data.rows.map(([t, at]: [string, number]) => ({label: t, start: at, tone: 'in'}));
  return <TallyReceipt x={460} y={300} w={1000} head="배당 씨 vs 매도 씨 · 오늘 순서" rows={rows} size={34} active={activeRow(rows, f)} />;
};

const Cards: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  let act = -1; d.cards.forEach((c: any, i: number) => { if (f >= c[3]) act = i; });
  return <RuleCards cards={d.cards} active={act} x={150} y={400} w={1620} />;
};

const Stamps: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const g = 36, w = (1620 - g * 3) / 4;
  return (
    <>
      {d.cards.map(([h, sub, at]: [string, string, number], i: number) => {
        const sp = spring({frame: f - at, fps, config: {damping: 14}});
        return (
          <div key={i} style={{position: 'absolute', left: 150 + i * (w + g), top: 340 + (1 - sp) * 30, width: w, height: 260, background: T.surface, borderRadius: 20, opacity: f >= at ? sp : 0, boxShadow: '0 10px 30px rgba(0,0,0,0.07)'}}>
            <div style={{...F, position: 'absolute', left: 30, top: 34, fontWeight: 700, fontSize: h.length > 6 ? 38 : 50, color: T.ink, whiteSpace: 'nowrap'}}>{h}</div>
            <div style={{...F, position: 'absolute', left: 30, top: 120, fontWeight: 700, fontSize: 28, color: T.ink2, whiteSpace: 'nowrap'}}>{sub}</div>
            {f >= d.stamp[1] ? <Stamp x={26} y={180} o={fade(f, d.stamp[1] + i * 4, 8)} text={d.stamp[0]} color={T.rise} size={26} rot={-6} /> : null}
          </div>
        );
      })}
      <Note text={d.no[0]} at={d.no[1]} x={150} y={680} color={T.accent} size={40} />
    </>
  );
};

const Law: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const rows = toRows(d.rows); const size = rows.length > 5 ? 28 : 34;
  return (
    <>
      <TallyReceipt x={900} y={300} w={880} head={d.head} rows={rows} size={size} active={activeRow(rows, f)} />
      <Side side={d.side} />
    </>
  );
};

const Thresh: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Ruler x={200} y={520} w={1440} max={d.max} marks={d.marks} fill={d.fill} />
      <Note text={d.note[0]} at={d.note[1]} x={200} y={780} color={T.ink3} size={28} />
    </>
  );
};

const TwinR: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame();
  return (
    <>
      {s.data.cards.map((c: any, i: number) => {
        const rows = toRows(c.rows); const x = i === 0 ? 150 : 990; const st = c.rows[0][3];
        return f >= st ? <div key={i} style={{opacity: c.dim ? 0.5 : 1}}><TallyReceipt x={x} y={300} w={780} head={c.head} rows={rows} size={30} start={st} active={c.dim ? -1 : activeRow(rows, f)} /></div> : null;
      })}
    </>
  );
};

const Bars: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2, sub: b[5] ?? undefined}));
  return <TallyBars bars={bars} x={bars.length > 2 ? 420 : 560} y={330} w={bars.length > 2 ? 1080 : 800} h={380} max={d.max} labelSize={32} valueSize={44} />;
};

const Count: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <TallyCountUp from={0} to={d.to} text={d.text} start={d.start} dur={40} digits={2} suffix="%" size={170} color={T.accent} x={180} y={380} label={d.label} note={d.note} />
      <ScoreBoard cells={d.score} />
    </>
  );
};

const Zoom: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <TallyZoom text={d.text} start={d.start} x={180} y={380} size={150} color={T.accent} label={d.label} />
      <TallyCallout x={180} y={680} text={d.note} start={d.noteAt} size={32} />
    </>
  );
};

const Years: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return <YearBars x={200} y={320} w={1520} h={440} years={d.years} vals={d.vals} min={d.min} max={d.max} start={d.start} tags={d.tags} />;
};

const Diverge: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <DivRows x0={1000} y={400} rowH={150} half={420} max={d.max} rows={d.rows} labelW={260} />
      <TallyCallout x={150} y={720} text={d.q[0]} start={d.q[1]} size={34} />
    </>
  );
};

const Tiles: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data;
  return <StartTiles x={150} y={340} w={1640} rows={d.rows} count={d.count} box={d.box} />;
};

const Line: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const X = 260, Y = 330, W = d.score ? 1060 : 1400, H = 400;
  const series = d.series.map(([name, col, pts]: [string, string, number[]]) => ({name, color: COL[col], pts, width: 6}));
  const n = d.series[0][2].length; const xy = lineXY(X, Y, W, H, d.min, d.max, n);
  return (
    <>
      <TallyLineChart series={series} x={X} y={Y} w={W} h={H} min={d.min} max={d.max} start={d.draw} dur={d.dur ?? 60}
        ticks={d.ticks.map(([v, t]: [number, string]) => ({v, text: t}))} xlabels={d.xlabels.map(([i, t]: [number, string]) => ({i, text: t}))} />
      {d.tags.map((t: any, i: number) => { const [tx, ty] = xy(t[0], t[1]); return <TallyTag key={i} x={tx} y={ty} text={t[2]} start={t[3]} side={t[4]} hot={t[5]} size={24} />; })}
      {d.legend ? d.series.map(([name, col]: [string, string], i: number) => (
        <div key={i} style={{...F, position: 'absolute', left: X + i * 200, top: Y - 20, fontWeight: 700, fontSize: 28, color: COL[col], opacity: fade(f, 0), whiteSpace: 'nowrap'}}>━ {name}</div>
      )) : null}
      {d.score ? <ScoreBoard cells={d.score} y={330} /> : null}
    </>
  );
};

const Persona: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const rows = toRows(d.rows);
  return (
    <>
      <Person x={150} y={330} name={d.person[0]} desc={d.person[1]} at={0} color={COL[d.person[2]] ?? T.accent} />
      <Stamp x={230} y={690} o={fade(f, 8, 8)} text={d.tag} color={T.ink3} size={26} rot={-6} />
      <TallyReceipt x={720} y={300} w={1060} head={d.head} rows={rows} size={rows.length > 4 ? 30 : 34} active={activeRow(rows, f)} stamp={d.stamp ? {text: d.stamp[0], start: d.stamp[1]} : undefined} />
    </>
  );
};

const DuoS: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <>
      <Duo mid={d.mid} a={d.a} b={d.b} />
      {d.tag ? [210, 1350].map((x, i) => <Stamp key={i} x={x} y={690} o={fade(f, d.tag[1] + i * 4, 8)} text={d.tag[0]} color={T.ink3} size={24} rot={-6} />) : null}
    </>
  );
};

const End: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <TallyZoom text={d.text} start={d.start} x={180} y={400} size={84} label={d.label} />
      <Note text={d.note} at={d.start + 30} x={180} y={600} color={T.ink3} size={30} />
      <div style={{position: 'absolute', left: 150, top: 330, width: 1620, height: 440, borderRadius: 20, border: `3px dashed ${T.line}`, opacity: fade(f, 0, 14)}} />
    </>
  );
};

const Body: React.FC<{s: CScene}> = ({s}) => {
  switch (s.kind) {
    case 'drain': return <Drain s={s} />;
    case 'vs': return <Vs s={s} />;
    case 'grid': return <GridS s={s} />;
    case 'duo': return <DuoS s={s} />;
    case 'persona': return <Persona s={s} />;
    case 'road': return <Road s={s} />;
    case 'cards': return <Cards s={s} />;
    case 'stamps': return <Stamps s={s} />;
    case 'law': return <Law s={s} />;
    case 'thresh': return <Thresh s={s} />;
    case 'twinr': return <TwinR s={s} />;
    case 'bars': return <Bars s={s} />;
    case 'count': return <Count s={s} />;
    case 'zoom': return <Zoom s={s} />;
    case 'years': return <Years s={s} />;
    case 'diverge': return <Diverge s={s} />;
    case 'tiles': return <Tiles s={s} />;
    case 'line': return <Line s={s} />;
    case 'end': return <End s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: CScene}> = ({s}) => {
  if (s.kind === 'logo') return <AbsoluteFill><LogoSting sub={s.data.sub} /></AbsoluteFill>;
  const st = tallyStarts(s.lines);
  return (
    <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines}>
      <Body s={s} />
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </TallyFrame>
  );
};

export const C1: React.FC<C1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
