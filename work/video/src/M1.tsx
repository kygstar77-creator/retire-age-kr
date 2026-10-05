// M-1 "월배당, 매달 100만원 받으려면 얼마 있어야 하나(거꾸로 계산)" 화면 — 재료: work/video/m1.json(ep/M-1/m1props.py가 script.v2.md·voice.json·calc_out·facts로 만든다)
// R-1과 같은 흰 보드 틀(TallyFrame) + 문장마다 표시가 하나씩 더해짐. 장면 종류 15가지, 누적(쌓은) 막대 없음 — 분배·가격은 나란히(GroupBars).
// 숫자 글자는 전부 m1.json에서 온다. 코드 안 숫자는 배치 값뿐.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {T, F, CL, LogoSting} from './parts/fm';
import {RuleCards, Gauge, Timeline, FlowBoxes, ProductCard, Calendar12, GroupBars, Grid, COLR} from './parts/reverse';
import {TallyFrame, TallyLine, tallyStarts} from './motion/TallyFrame';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyTag, TallyCallout} from './motion/TallyMark';
import {ReverseAsk} from './motion/ReverseAsk';

type MLine = TallyLine & {audio?: string | null};
export type MScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: MLine[]; frames: number};
export type M1Props = {fps: number; scenes: MScene[]; missing: number; script?: string; rate?: number};
export const m1Frames = (p: M1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const activeRow = (rows: TallyRow[], f: number) => { let k = -1; rows.forEach((r, i) => { if (f >= r.start) k = i; }); return k; };

const Note: React.FC<{text: string; at: number; x?: number; y?: number; color?: string; size?: number}> = ({text, at, x = 150, y = 760, color = T.ink2, size = 34}) => {
  const f = useCurrentFrame();
  return <div style={{...F, position: 'absolute', left: x, top: y + (1 - fade(f, at)) * 10, fontWeight: 700, fontSize: size, color, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{text}</div>;
};

const Big: React.FC<{text: string; sub: string; at: number; x?: number; y?: number; size?: number; color?: string}> = ({text, sub, at, x = 150, y = 420, size = 120, color = T.accent}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - at, fps, config: {damping: 12}});
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: f >= at ? 1 : 0}}>
      <div style={{...F, fontWeight: 700, fontSize: size, color, lineHeight: 1.05, whiteSpace: 'nowrap', letterSpacing: -2, transform: `scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center'}}>{text}</div>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginTop: 12, whiteSpace: 'nowrap'}}>{sub}</div>
    </div>
  );
};

const Road: React.FC<{s: MScene}> = ({s}) => {
  const f = useCurrentFrame();
  const rows: TallyRow[] = s.data.rows.map(([t, at]: [string, number]) => ({label: t, start: at, tone: 'in'}));
  return <TallyReceipt x={360} y={300} w={1200} head={s.title} rows={rows} size={44} active={activeRow(rows, f)} />;
};

const Rules: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  let act = -1; for (const [i, at] of d.active) if (f >= at) act = i;
  return (
    <>
      <RuleCards cards={d.cards} active={act} y={320} />
      {d.warn ? <TallyTag x={150 + 258 + (d.warn[2] ?? 0) * 552} y={590} text={d.warn[0]} start={d.warn[1]} side="down" size={26} /> : null}
      {d.fx ? (
        <div style={{position: 'absolute', left: 150, top: 690, opacity: fade(f, d.fx[3]), display: 'flex', alignItems: 'baseline', gap: 20}}>
          <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2}}>{d.fx[0]}</span>
          <span style={{...F, fontWeight: 700, fontSize: 52, color: T.ink3}}>{d.fx[1]}</span>
          <span style={{...F, fontWeight: 700, fontSize: 52, color: T.ink3}}>→</span>
          <span style={{...F, fontWeight: 700, fontSize: 52, color: T.fall}}>{d.fx[2]}</span>
        </div>
      ) : null}
      {d.stamp ? (
        <div style={{position: 'absolute', left: 150, top: 700, ...F, fontWeight: 700, fontSize: 36, color: T.accent, border: `4px solid ${T.accent}`, borderRadius: 12, padding: '6px 20px',
          opacity: fade(f, d.stamp[1], 6), transform: `rotate(-3deg) scale(${interpolate(f, [d.stamp[1], d.stamp[1] + 8], [1.5, 1], CL)})`, transformOrigin: 'left center'}}>{d.stamp[0]}</div>
      ) : null}
    </>
  );
};

const Receipt: React.FC<{s: MScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const rows: TallyRow[] = d.rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));
  return (
    <>
      <TallyReceipt x={940} y={300} w={840} head={d.head} rows={rows} size={rows.length > 3 ? 34 : 38} active={activeRow(rows, f)} />
      {d.side ? <Big text={d.side[0]} at={d.side[1]} sub={d.side[2]} y={400} /> : null}
      {d.count ? (
        <div style={{position: 'absolute', left: 150, top: 340, opacity: fade(f, d.count[4])}}>
          <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2}}>{d.count[3]}</div>
          <div style={{display: 'flex', alignItems: 'baseline', gap: 18, marginTop: 10}}>
            <span style={{...F, fontWeight: 700, fontSize: 50, color: T.ink3, whiteSpace: 'nowrap'}}>{d.count[0]}</span>
            <span style={{...F, fontWeight: 700, fontSize: 50, color: T.ink3}}>→</span>
          </div>
          <div style={{...F, fontWeight: 700, fontSize: 96, color: T.rise, letterSpacing: -2, whiteSpace: 'nowrap', opacity: fade(f, d.count[4] + 20)}}>{d.count[1]}</div>
          <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3}}>{d.count[2]} → 총 보험료(건강 + 장기요양)</div>
        </div>
      ) : null}
      {d.callout ? <TallyCallout x={150} y={700} text={d.callout[0]} start={d.callout[1]} size={28} w={740} /> : null}
    </>
  );
};

const GaugeView: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Gauge max={d.max} lines={d.lines} fill={d.fill} target={d.target} y={570} />
      {d.all ? <TallyCallout x={150} y={330} text={d.all[0]} start={d.all[1]} size={32} /> : null}
      {d.side.map((x: [string, string, number], i: number) => <React.Fragment key={i}><Note text={x[0]} at={x[2]} x={1040} y={330} color={T.accent} size={40} /><Note text={x[1]} at={x[2] + 6} x={1040} y={386} size={24} color={T.ink3} /></React.Fragment>)}
    </>
  );
};

const TimelineView: React.FC<{s: MScene}> = ({s}) => (
  <>
    <Timeline segs={s.data.segs} y={430} />
    {s.data.note ? <TallyCallout x={150} y={700} text={s.data.note[0]} start={s.data.note[1]} size={30} /> : null}
  </>
);

const FlowView: React.FC<{s: MScene}> = ({s}) => (
  <>
    <FlowBoxes boxes={s.data.boxes} y={360} />
    {s.data.note ? <Note text={s.data.note[0]} at={s.data.note[1]} x={727} y={620} size={26} color={T.ink3} /> : null}
  </>
);

const Card: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <ProductCard name={d.name} desc={d.desc} freq={d.freq} rate={d.rate} rateCalc={d.rateCalc} need={d.need} at={d.at} rateAt={d.rateAt} needAt={d.needAt} hot={d.hot} />
      {d.note ? <TallyCallout x={940} y={760} text={d.note[0]} start={d.note[1]} size={24} w={820} /> : null}
    </>
  );
};

const CalendarView: React.FC<{s: MScene}> = ({s}) => (
  <>
    <Calendar12 months={s.data.months} at={s.data.at} y={318} />
    {s.data.note ? <TallyTag x={960} y={736} text={s.data.note[0]} start={s.data.note[1]} side="down" hot size={28} /> : null}
  </>
);

const Bars: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COLR[b[4]] ?? T.ink2, sub: b[5] ?? undefined}));
  return (
    <>
      <TallyBars bars={bars} x={820} y={400} w={940} h={330} max={d.max} labelSize={28} valueSize={36} tags />
      {d.note ? <Note text={d.note[0]} at={d.note[1]} x={150} y={400} size={34} /> : null}
      {d.note2 ? <Note text={d.note2[0]} at={d.note2[1]} x={150} y={470} size={40} color={T.accent} /> : null}
    </>
  );
};

const Months: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const bars: TallyBar[] = d.vals.map((v: number, i: number) => ({label: d.labels[i], value: v, start: d.at + i * 3,
    valueText: i === d.min && f >= d.minAt ? d.texts[i] : i === d.max && f >= d.maxAt ? d.texts[i] : '',
    color: i === d.min && f >= d.minAt ? T.accent : i === d.max && f >= d.maxAt ? T.ink : T.ink3}));
  return (
    <>
      <TallyBars bars={bars} x={150} y={410} w={1060} h={300} max={d.hi} min={d.lo} labelSize={22} valueSize={30} gap={14} tags />
      <TallyCallout x={1280} y={350} text={d.ratio[0]} start={d.ratio[1]} size={28} w={480} />
      <div style={{position: 'absolute', left: 1280, top: 480, opacity: fade(f, d.jump[3])}}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2}}>월 100만원에 필요한 돈</div>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 14, marginTop: 8}}>
          <span style={{...F, fontWeight: 700, fontSize: 44, color: T.ink3, whiteSpace: 'nowrap'}}>{d.jump[0]}</span>
          <span style={{...F, fontWeight: 700, fontSize: 44, color: T.ink3}}>→</span>
        </div>
        <div style={{...F, fontWeight: 700, fontSize: 90, color: T.accent, letterSpacing: -2, whiteSpace: 'nowrap', opacity: fade(f, d.jump[3] + 14)}}>{d.jump[1]}</div>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.accent, opacity: fade(f, d.jump[3] + 20)}}>{d.jump[2]}</div>
      </div>
    </>
  );
};

const Pair: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <GroupBars groups={d.groups} max={d.max} at={d.at} legend={d.legend} x={150} y={430} w={1160} h={300} />
      {d.chip ? <TallyTag x={150 + d.chip[0] * ((1160 - 180) / 3 + 90) + (1160 - 180) / 6} y={512} text={d.chip[1]} start={d.chip[2]} side="up" size={22} /> : null}
      {d.save ? <TallyCallout x={1380} y={360} text={d.save[0]} start={d.save[1]} size={28} w={380} /> : null}
      {d.save2 ? <TallyCallout x={1380} y={600} text={d.save2[0]} start={d.save2[1]} size={26} w={380} /> : null}
    </>
  );
};

const Table: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Grid cols={d.cols} rows={d.rows} stamp={d.stamp} hot={d.hot} y={d.top ? 370 : 330} />
      {d.top ? <Note text={d.top[0]} at={d.top[1]} x={150} y={320} size={30} color={T.accent} /> : null}
    </>
  );
};

const End: React.FC<{s: MScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const sp = spring({frame: f - d.at, fps, config: {damping: 12}});
  return (
    <>
      <div style={{position: 'absolute', left: 150, top: 400, opacity: sp}}>
        <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink2}}>{d.ctaSub}</div>
        <div style={{...F, fontWeight: 700, fontSize: 130, color: T.accent, letterSpacing: -3, transform: `scale(${0.8 + 0.2 * sp})`, transformOrigin: 'left center'}}>{d.cta}</div>
      </div>
      <div style={{position: 'absolute', left: 1000, top: 300, width: 780, height: 440, borderRadius: 20, border: `3px dashed ${T.line}`, opacity: fade(f, 0, 14)}} />
    </>
  );
};

const Body: React.FC<{s: MScene}> = ({s}) => {
  switch (s.kind) {
    case 'open': return <ReverseAsk {...s.data.rev} />;
    case 'road': return <Road s={s} />;
    case 'rules': return <Rules s={s} />;
    case 'receipt': return <Receipt s={s} />;
    case 'gauge': return <GaugeView s={s} />;
    case 'timeline': return <TimelineView s={s} />;
    case 'flow': return <FlowView s={s} />;
    case 'card': return <Card s={s} />;
    case 'calendar': return <CalendarView s={s} />;
    case 'bars': return <Bars s={s} />;
    case 'months': return <Months s={s} />;
    case 'pair': return <Pair s={s} />;
    case 'table': return <Table s={s} />;
    case 'end': return <End s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: MScene}> = ({s}) => {
  if (s.kind === 'logo') return <AbsoluteFill><LogoSting sub={s.data.sub} /></AbsoluteFill>;
  const st = tallyStarts(s.lines);
  return (
    <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines}>
      <Body s={s} />
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </TallyFrame>
  );
};

export const M1: React.FC<M1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
