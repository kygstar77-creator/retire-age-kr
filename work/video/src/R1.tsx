// R-1 "1억의 1년 영수증"(X-SERIES-1 ①) v6 화면 — 재료: work/video/r1.json(ep/R-1/r1props.py가 script.v6.md·voice.json·calc2_out·원자료로 만든다)
// 장면마다 움직임은 하나만(2026-10-03 사장님 "대본도 화면도 안 나아진다"): 숫자 굴러가기 · 막대 자라기 · 영수증 한 줄씩 인쇄 · 강조 숫자 키우기.
// 부품은 src/motion/Tally*.tsx. 글자는 안전 구역 안에만(오른쪽 아래 25%×20%, 맨 아래 5% 비움 — TallyFrame.SAFE).
// 숫자 글자는 전부 r1.json에서 온다(facts.txt 문구 그대로). 코드 안 숫자는 배치·눈금 값뿐. 겹치는(누적) 구간 그래프 없음.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {T, F, CL, LogoSting} from './parts/fm';
import {TallyFrame, TallyLine, tallyStarts} from './motion/TallyFrame';
import {TallyCountUp} from './motion/TallyCountUp';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyZoom} from './motion/TallyZoom';

type RLine = TallyLine & {audio?: string | null};
export type RScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: RLine[]; frames: number};
export type R1Props = {fps: number; scenes: RScene[]; missing: number; script?: string; rate?: number};
export const r1Frames = (p: R1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {ink: T.ink2, accent: T.accent, rise: T.rise, fall: T.fall};
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);

// 화면 오른쪽 그림 자리: x 980~1800, y 340~840 (오른쪽 아래 글자 금지 구역 위에서 끝남)
const Note: React.FC<{text: string; at: number; x?: number; y?: number; color?: string; size?: number}> = ({text, at, x = 120, y = 760, color = T.ink2, size = 34}) => {
  const f = useCurrentFrame();
  return <div style={{...F, position: 'absolute', left: x, top: y, fontWeight: 700, fontSize: size, color, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{text}</div>;
};

const Open: React.FC<{s: RScene}> = ({s}) => {
  const f = useCurrentFrame();
  const bars: TallyBar[] = s.data.bars.map(([name, at]: [string, number]) => ({label: name, value: 1, valueText: '1억', start: at, color: T.ink2}));
  return (
    <>
      <TallyBars bars={bars} x={980} y={400} w={820} h={340} max={1.25} labelSize={34} valueSize={40} />
      <div style={{...F, position: 'absolute', left: 120, top: 420, fontWeight: 700, fontSize: 96, color: T.accent, opacity: fade(f, s.data.q), lineHeight: 1.1}}>1년 뒤<br />얼마?</div>
    </>
  );
};

const Road: React.FC<{s: RScene}> = ({s}) => {
  const rows: TallyRow[] = s.data.rows.map(([t, at]: [string, number]) => ({label: t, start: at, tone: 'in'}));
  return <TallyReceipt x={120} y={250} w={1100} head="1억의 1년 영수증 · 오늘 순서" rows={rows} size={44} />;
};

const Receipt: React.FC<{s: RScene}> = ({s}) => {
  const f = useCurrentFrame();
  const rows: TallyRow[] = s.data.rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));
  const size = rows.length > 5 ? 32 : 36;
  const side = s.data.side as [string, number, string] | undefined;
  return (
    <>
      <TallyReceipt x={980} y={340} w={820} head={s.data.head} rows={rows} size={size} />
      {side ? (
        <div style={{position: 'absolute', left: 120, top: 520, opacity: fade(f, side[1])}}>
          <div style={{...F, fontWeight: 700, fontSize: side[0].length > 10 ? 44 : 110, color: T.accent, lineHeight: 1.05, whiteSpace: 'nowrap'}}>{side[0]}</div>
          <div style={{...F, fontWeight: 500, fontSize: 30, color: T.ink3, marginTop: 12, whiteSpace: 'nowrap'}}>{side[2]}</div>
        </div>
      ) : null}
    </>
  );
};

const Fx: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <div style={{position: 'absolute', left: 120, top: 380, opacity: fade(f, d.aAt)}}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>작년 그날 (2025.10.2)</div>
        <div style={{...F, fontWeight: 700, fontSize: 96, color: T.ink3, lineHeight: 1.05}}>{d.a}</div>
      </div>
      <TallyCountUp from={d.av} to={d.bv} text={d.b} start={d.start} dur={40} digits={1} suffix="원" size={150} color={T.fall} x={980} y={360} label="올해 같은 날 (2026.10.2)" note={d.pct} />
      <Note text={`1억이면 환율만으로 ${d.loss}`} at={d.lossAt} x={980} y={620} color={T.rise} size={40} />
    </>
  );
};

const Bars: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2, sub: b[5], lo: b[6], loText: b[7]}));
  const n = bars.length;
  const note = d.note as [string, number] | undefined;
  if (d.dir === 'h') {
    return (
      <>
        <TallyBars dir="h" bars={bars} x={120} y={410} w={1480} h={n * 110 + (n - 1) * 40} max={d.max} min={d.min ?? 0} labelSize={34} valueSize={36} gap={40}
          marker={d.marker ? {value: d.marker[0], text: d.marker[1], start: d.marker[2]} : undefined} />
      </>
    );
  }
  const w = n <= 2 ? 620 : n <= 4 ? 980 : 1240;
  const x = n <= 2 ? 980 : n <= 4 ? 820 : 520;
  return (
    <>
      <TallyBars bars={bars} x={x} y={400} w={w} h={330} max={d.max} labelSize={n > 4 ? 26 : 32} valueSize={n > 4 ? 30 : 38} />
      {note ? <Note text={note[0]} at={note[1]} x={120} y={n > 4 ? 400 : 560} size={n > 4 ? 30 : 36} color={T.ink2} /> : null}
    </>
  );
};

const Count: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Note text={d.pre} at={d.preAt} x={120} y={380} color={T.ink3} size={40} />
      <TallyCountUp from={d.from} to={d.to} text={d.text} start={d.start} dur={45} suffix="원" size={150} color={T.accent} x={120} y={450} label={d.label} />
      <Note text={d.cut} at={d.cutAt} x={120} y={700} color={T.rise} size={44} />
    </>
  );
};

const Zoom: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      {d.card ? (
        <>
          <div style={{position: 'absolute', left: 980, top: 360, width: 820, height: 400, background: '#fff', borderRadius: 20, boxShadow: '0 14px 40px rgba(0,0,0,0.09)'}}>
            <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2, padding: '30px 40px 0'}}>{d.card}</div>
            <div style={{...F, fontWeight: 500, fontSize: 28, color: T.ink3, padding: '26px 40px 0'}}>자산</div>
            <div style={{position: 'absolute', left: 40, right: 40, top: 170, height: 170, border: `4px solid ${T.accent}`, borderRadius: 16}} />
          </div>
          <TallyZoom text={d.text} start={d.start} x={1030} y={545} size={130} />
          <div style={{position: 'absolute', left: 120, top: 420, opacity: fade(f, d.start + 10)}}>
            <div style={{...F, fontWeight: 700, fontSize: 54, color: T.ink, lineHeight: 1.25, wordBreak: 'keep-all', width: 780}}>{d.label}</div>
            <div style={{...F, fontWeight: 500, fontSize: 32, color: T.ink3, marginTop: 18}}>{d.note}</div>
          </div>
        </>
      ) : <TallyZoom text={d.text} start={d.start} x={120} y={400} size={180} label={d.label} note={d.note} />}
      {d.after ? (
        <div style={{position: 'absolute', left: 980, top: 420, opacity: fade(f, d.after[3])}}>
          <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>{d.after[0]}</div>
          <div style={{...F, fontWeight: 700, fontSize: 72, color: T.ink, whiteSpace: 'nowrap'}}>{d.after[1]}</div>
          <div style={{...F, fontWeight: 700, fontSize: 44, color: T.accent}}>{d.after[2]}</div>
        </div>
      ) : null}
    </>
  );
};

const Body: React.FC<{s: RScene}> = ({s}) => {
  switch (s.kind) {
    case 'open': return <Open s={s} />;
    case 'road': return <Road s={s} />;
    case 'receipt': return <Receipt s={s} />;
    case 'fx': return <Fx s={s} />;
    case 'bars': return <Bars s={s} />;
    case 'count': return <Count s={s} />;
    case 'zoom': return <Zoom s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: RScene}> = ({s}) => {
  if (s.kind === 'logo') return <AbsoluteFill><LogoSting sub={s.data.sub} /></AbsoluteFill>;
  const st = tallyStarts(s.lines);
  return (
    <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines}>
      <Body s={s} />
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </TallyFrame>
  );
};

export const R1: React.FC<R1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
