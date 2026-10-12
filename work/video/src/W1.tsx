// W-1 1화 "이번 주 뉴스가 내 돈에 얼마" 화면 — 재료: work/video/w1.json(ep/W-1/w1props.py가 script.md·voice.json·calc_out.txt·w1009/raw로 만든다)
// 틀은 C-1·G-1과 같은 TallyFrame(흰 보드·형광 부제·[자막] 칩·출처). 새 그림은 parts/weekly.tsx(다섯 칸 띠·다리 막대·점 세기·다음 주 달력·작은 선·지난주 내 돈 칸).
// 숫자 글자는 전부 w1.json에서 온다(calc_out·원문 그대로). 코드 안 숫자는 배치 좌표뿐. 전망·추천 없음. 색: 줄어듦 파랑(fall)·늘어남 빨강(rise)·우리 강조 주황(accent).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {T, F, CL, LogoSting} from './parts/fm';
import {Stamp} from './parts/receipt';
import {Grid, Timeline} from './parts/reverse';
import {DivRows} from './parts/gold';
import {WeekStrip, BridgeBars, DotCount, NextCal, MiniLine, WeekTotal} from './parts/weekly';
import {TallyFrame, TallyLine, tallyStarts} from './motion/TallyFrame';
import {TallyCountUp} from './motion/TallyCountUp';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyZoom} from './motion/TallyZoom';
import {TallyCallout} from './motion/TallyMark';

type WLine = TallyLine & {audio?: string | null};
export type WScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: WLine[]; frames: number};
export type W1Props = {fps: number; scenes: WScene[]; missing: number; script?: string; rate?: number; us_last?: string};
export const w1Frames = (p: W1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {ink: T.ink2, ink3: T.ink3, accent: T.accent, rise: T.rise, fall: T.fall};
const HEAD = '지난주 내 돈';
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const activeRow = (rows: TallyRow[], f: number) => { let k = -1; rows.forEach((r, i) => { if (f >= r.start) k = i; }); return k; };
const toRows = (rows: any[]): TallyRow[] => rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at ?? 0}));
const lift = '0 10px 30px rgba(0,0,0,0.07)';
// U5(같은 화면 8초 이하): 줄이 바뀌면 그 줄이 말하는 항목을 검은 띠·검은 카드로 꺼낸다. 글자는 props에 있는 것만 다시 놓는다.
const sayAt = (s: WScene, li: number, needle?: string) => { const st = tallyStarts(s.lines); const l = s.lines[li]; if (!l) return 1e9;
  const k = needle ? l.text.indexOf(needle) : -1; return st[li] + (k > 0 ? Math.round(l.frames * k / l.text.length) : 0); };
const DarkBar: React.FC<{text: string; at: number; x: number; y: number; w: number; size?: number; color?: string}> = ({text, at, x, y, w, size = 46, color = T.dink}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (f < at) return null;
  const sp = spring({frame: f - at, fps, config: {damping: 14}});
  return <div style={{position: 'absolute', left: x, top: y + (1 - sp) * 20, width: w, opacity: sp, background: T.ink, borderRadius: 16, padding: '26px 40px', boxSizing: 'border-box',
    ...F, fontWeight: 700, fontSize: size, color, whiteSpace: 'nowrap', lineHeight: 1.2}}>{text}</div>;
};

const Note: React.FC<{text: string; at: number; x?: number; y?: number; color?: string; size?: number}> = ({text, at, x = 150, y = 760, color = T.ink2, size = 34}) => {
  const f = useCurrentFrame();
  return <div style={{...F, position: 'absolute', left: x, top: y + (1 - fade(f, at)) * 10, fontWeight: 700, fontSize: size, color, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{text}</div>;
};

const Big: React.FC<{b?: [string, number, string]; x?: number; y?: number; color?: string; size?: number}> = ({b, x = 1000, y = 400, color = T.accent, size}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!b) return null;
  const s = spring({frame: f - b[1], fps, config: {damping: 12}});
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: f >= b[1] ? 1 : 0}}>
      <div style={{...F, fontWeight: 700, fontSize: size ?? (b[0].length > 8 ? 110 : 150), color, lineHeight: 1, whiteSpace: 'nowrap', letterSpacing: -3, transform: `scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center'}}>{b[0]}</div>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginTop: 18, whiteSpace: 'nowrap'}}>{b[2]}</div>
    </div>
  );
};

const Open: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows = toRows(d.rows);
  const dim = d.big && f >= d.big[1] ? 0.55 : 1;
  return (
    <>
      <div style={{opacity: dim}}><TallyReceipt x={170} y={310} w={760} head={d.head} rows={rows} size={36} active={activeRow(rows, f)} /></div>
      <Big b={d.big} x={1020} y={400} />
    </>
  );
};

const Bars: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2, sub: b[5] ?? undefined}));
  return <TallyBars bars={bars} x={bars.length > 2 ? 300 : 560} y={330} w={bars.length > 2 ? 1060 : 800} h={400} min={d.min} max={d.max} labelSize={32} valueSize={44} />;
};

const Three: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const g = 40, w = (1620 - g * 2) / 3;
  const cards: [string, string, number][] = s.data.cards;
  const on = cards.map(([, sub]) => sayAt(s, 0, sub)); let cur = -1; on.forEach((a, i) => { if (f >= a) cur = i; });
  return (
    <>
      {cards.map(([h, sub, at], i) => {
        const sp = spring({frame: f - at, fps, config: {damping: 14}}); const dk = i === cur;
        return (
          <div key={i} style={{position: 'absolute', left: 150 + i * (w + g), top: 330 + (1 - sp) * 40, width: w, height: 400, background: dk ? T.ink : T.surface, borderRadius: '18px 18px 0 0', boxShadow: lift, opacity: f >= at ? sp : 0}}>
            <div style={{...F, position: 'absolute', left: 34, top: 34, fontWeight: 700, fontSize: 30, color: dk ? T.daccent : T.accent}}>{['한 종목', '시장 전체', '해외'][i]}</div>
            <div style={{...F, position: 'absolute', left: 34, top: 84, fontWeight: 700, fontSize: 44, color: dk ? T.dink : T.ink, whiteSpace: 'nowrap'}}>{h}</div>
            <div style={{position: 'absolute', left: 34, right: 34, top: 160, borderTop: `3px dashed ${dk ? T.dink3 : T.line}`}} />
            {dk ? null : [0, 1, 2].map((k) => <div key={k} style={{position: 'absolute', left: 34, right: 34, top: 190 + k * 54, height: 30, borderRadius: 8, background: `repeating-linear-gradient(135deg, ${T.bg} 0 10px, ${T.surface} 10px 20px)`}} />)}
            <div style={{...F, position: 'absolute', left: 34, right: 30, ...(dk ? {top: 196} : {bottom: 30}), fontWeight: 700, fontSize: dk ? 40 : 28, color: dk ? T.dink : T.ink2, lineHeight: 1.3, wordBreak: 'keep-all'}}>{sub}</div>
          </div>
        );
      })}
    </>
  );
};

const Week: React.FC<{s: WScene}> = ({s}) => <WeekStrip days={s.data.days} lo={s.data.lo} hi={s.data.hi} barAt={s.data.barAt} x={150} y={320} w={1620} h={500} />;

const Count: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  return <TallyCountUp from={0} to={Math.abs(d.to)} text={d.text} start={d.start} dur={40} digits={d.text.includes('.') ? (d.text.split('.')[1].replace('%', '').length) : 0}
    prefix={d.to < 0 ? '−' : '+'} suffix="%" size={190} color={d.to < 0 ? T.fall : T.rise} x={200} y={380} label={d.label} note={d.note} />;
};

const MLine: React.FC<{s: WScene}> = ({s}) => {
  const L = s.data.lines; const two = L.length > 1; const h = two ? 170 : 380;
  return (
    <>
      {L.map(([name, pts, vt, col, at, pct]: [string, [string, number][], [string, string], string, number, string], i: number) => (
        <React.Fragment key={i}>
          <MiniLine name={name} note={pct} pts={pts} vt={vt} color={COL[col] ?? T.ink2} at={at} x={170} y={two ? 340 + i * 260 : 360} w={1580} h={h} />
        </React.Fragment>
      ))}
    </>
  );
};

const GridS: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Grid cols={d.cols} rows={d.rows} hot={d.hot} x={150} y={310} w={1620} />
      {d.note ? <TallyCallout x={150} y={700} text={d.note[0]} start={d.note[1]} size={30} /> : null}
    </>
  );
};

const Quote: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <>
      <div style={{position: 'absolute', left: 200, top: 360, width: 1520, padding: '44px 56px', background: T.bg, borderLeft: `10px solid ${T.ink2}`, borderRadius: 12, opacity: fade(f, 0, 12)}}>
        <div style={{...F, fontWeight: 700, fontSize: 24, color: T.ink3, marginBottom: 16}}>공시 원문 · 4. 기타</div>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, lineHeight: 1.5, wordBreak: 'keep-all'}}>{`“${d.quote}”`}</div>
      </div>
      <Stamp x={1480} y={620} o={fade(f, d.stamp[1], 8)} text={d.stamp[0]} color={T.rise} size={44} rot={-10} />
    </>
  );
};

const Rcpt: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows = toRows(d.rows);
  return (
    <>
      <TallyReceipt x={200} y={310} w={1000} head={d.head} rows={rows} size={38} active={activeRow(rows, f)} focus />
      {d.stamp ? <DarkBar text={d.stamp[0]} at={d.stamp[1]} x={200} y={690} w={1000} size={42} color={T.daccent} /> : null}
      <WeekTotal head={HEAD} cells={d.total} />
    </>
  );
};

const Div: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows = toRows(d.rows);
  return (
    <>
      <TallyReceipt x={160} y={300} w={720} head={d.head} rows={rows} size={32} active={activeRow(rows, f)} />
      <Timeline segs={d.segs} x={930} y={440} w={620} />
      <WeekTotal head={HEAD} cells={d.total} />
    </>
  );
};

const Pairs: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return (
    <>
      {s.data.groups.map(([name, bars, tag, tagAt]: [string, [string, number, string, number][], string, number], i: number) => {
        const x = 200 + i * 820; const mx = Math.max(...bars.map((b) => b[1])) * 1.15;
        const tb: TallyBar[] = bars.map((b, k) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: k === 1 ? (i === 0 ? T.accent : T.ink2) : T.ink3}));
        const sp = spring({frame: f - tagAt, fps, config: {damping: 12}});
        return (
          <React.Fragment key={i}>
            <div style={{...F, position: 'absolute', left: x, top: 300, fontWeight: 700, fontSize: 40, color: T.ink, whiteSpace: 'nowrap'}}>{name}</div>
            <TallyBars bars={tb} x={x} y={380} w={620} h={330} max={mx} labelSize={26} valueSize={38} />
            <div style={{...F, position: 'absolute', left: x + 380, top: 300, fontWeight: 700, fontSize: 44, color: i === 0 ? T.accent : T.ink2, opacity: f >= tagAt ? 1 : 0, transform: `scale(${0.7 + 0.3 * sp})`, transformOrigin: 'left center', whiteSpace: 'nowrap'}}>{tag}</div>
          </React.Fragment>
        );
      })}
    </>
  );
};

const Dots: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  return <DotCount n={d.n} at={d.at} big={d.big} label={d.label} x={180} y={350} w={820} per={11} />;
};

const Cards2: React.FC<{cards: [string, string, number][]; stamp?: [string, number]; dashed?: number}> = ({cards, stamp, dashed = 1}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const g = 48, w = (1560 - g) / 2;
  return (
    <>
      {cards.map(([h, sub, at], i) => {
        const sp = spring({frame: f - at, fps, config: {damping: 14}}); const ghost = i === dashed;
        return (
          <div key={i} style={{position: 'absolute', left: 180 + i * (w + g), top: 340 + (1 - sp) * 30, width: w, height: 280, borderRadius: 20, opacity: f >= at ? sp : 0,
            background: ghost ? T.bg : T.surface, border: ghost ? `4px dashed ${T.ink3}` : undefined, boxShadow: ghost ? undefined : lift}}>
            <div style={{...F, position: 'absolute', left: 36, top: 40, fontWeight: 700, fontSize: 46, color: ghost ? T.ink2 : T.ink, whiteSpace: 'nowrap'}}>{h}</div>
            <div style={{...F, position: 'absolute', left: 36, top: 130, fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{sub}</div>
          </div>
        );
      })}
      {stamp ? <Stamp x={180 + w + g + 60} y={560} o={fade(f, stamp[1], 8)} text={stamp[0]} color={T.rise} size={40} rot={-8} /> : null}
    </>
  );
};

const Pending: React.FC<{s: WScene}> = ({s}) => <Cards2 cards={s.data.cards} stamp={s.data.stamp} />;

const KBars: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2}));
  return (
    <>
      <TallyBars bars={bars} x={180} y={360} w={680} h={380} min={d.min} max={d.max} labelSize={28} valueSize={30} />
      <Big b={d.big} x={920} y={430} color={T.fall} size={110} />
      <WeekTotal head={HEAD} cells={d.total} />
    </>
  );
};

const Diverge: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <DivRows x0={1000} y={400} rowH={150} half={420} max={d.max} rows={d.rows} labelW={260} />
      <TallyCallout x={150} y={720} text={d.q[0]} start={d.q[1]} size={34} />
    </>
  );
};

const StampS: React.FC<{s: WScene}> = ({s}) => (
  <>
    <Cards2 cards={s.data.cards} stamp={s.data.stamp} dashed={-1} />
    <DarkBar text={s.data.no[0]} at={s.data.no[1]} x={180} y={672} w={1560} size={46} />
  </>
);

const Bridge: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <BridgeBars steps={d.steps} lo={d.lo} hi={d.hi} x={200} y={350} w={1140} h={380} dimAt={s.lines.length > 2 ? tallyStarts(s.lines)[2] : undefined} />
      <WeekTotal head={HEAD} cells={d.total} />
    </>
  );
};

const Trio: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const g = 36, w = (1620 - g * 2) / 3;
  let cur = -1; d.cards.forEach((c: any, i: number) => { if (f >= c.at) cur = i; }); if (f >= d.q[1]) cur = -1;
  return (
    <>
      {d.cards.map((c: any, i: number) => {
        const rows: TallyRow[] = c.rows.map(([l, v, t]: [string, string, any]) => ({label: l, value: v, tone: t, start: 0}));
        const on = f >= c.at; const dk = i === cur;
        return (
          <React.Fragment key={i}>
            <div style={{opacity: on ? 1 : 0.85}}><TallyReceipt x={150 + i * (w + g)} y={350} w={w} head={c.head} rows={rows} size={30} start={i * 8} active={on ? rows.length - 1 : -1} focus={dk} /></div>
            <div style={{...F, position: 'absolute', left: 150 + i * (w + g), top: 622, width: w, boxSizing: 'border-box', padding: '14px 30px', borderRadius: 16, background: dk ? T.ink : 'transparent', fontWeight: 700, fontSize: 50, lineHeight: 1.2,
              color: !on ? T.ink3 : c.pct.includes('−') ? (dk ? T.dfall : T.fall) : T.rise, opacity: fade(f, i * 8 + 20), whiteSpace: 'nowrap'}}>{c.pct}</div>
          </React.Fragment>
        );
      })}
      <TallyCallout x={150} y={740} text={d.q[0]} start={d.q[1]} size={34} />
    </>
  );
};

const Cal: React.FC<{s: WScene}> = ({s}) => <NextCal cells={s.data.cells} later={s.data.later} x={150} y={340} w={1620} />;

const Road: React.FC<{s: WScene; next?: string}> = ({s, next}) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines);
  const rows: TallyRow[] = s.data.rows.map(([t, at]: [string, number]) => ({label: t, start: at, tone: 'in'}));
  const a1 = st[0] + Math.round(s.lines[0].frames * 0.5);
  const act = s.lines.length > 2 && f >= st[2] ? -1 : f >= st[1] ? 3 : f >= a1 ? 2 : 1;
  return (
    <>
      <TallyReceipt x={360} y={300} w={1200} head={s.data.head} rows={rows} size={36} active={act} focus />
      {next && s.lines.length > 2 ? <DarkBar text={next} at={st[2]} x={360} y={712} w={1200} size={44} color={T.daccent} /> : null}
    </>
  );
};

const Sum: React.FC<{s: WScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows = toRows(d.rows);
  return (
    <>
      <TallyReceipt x={760} y={300} w={1020} head={d.head} rows={rows} size={30} active={activeRow(rows, f)} focus />
      <Big b={d.side} x={170} y={420} size={110} />
    </>
  );
};

const End: React.FC<{s: WScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const {fps} = useVideoConfig(); const st = tallyStarts(s.lines);
  const parts: string[] = String(d.note).split(' · '); const subs: string[] = String(s.sub ?? '').split(' · ');
  const bAt = sayAt(s, 0, s.lines[0]?.text.split('. ')[1]?.slice(0, 4));
  const tEnd = st[st.length - 1] + s.lines[s.lines.length - 1].frames;
  const g = 48, w = (1560 - g) / 2; const out = interpolate(f, [d.start - 8, d.start], [1, 0], CL);
  const ls = spring({frame: f - d.start, fps, config: {damping: 14}});
  return (
    <>
      {f < d.start ? parts.slice(0, 2).map((t, i) => {
        const at = i === 0 ? 6 : bAt; const dk = i === 0 ? f < st[1] : f >= st[1];
        const sp = spring({frame: f - at, fps, config: {damping: 14}});
        return <div key={i} style={{position: 'absolute', left: 180 + i * (w + g), top: 360 + (1 - sp) * 30, width: w, height: 260, borderRadius: 20, opacity: (f >= at ? sp : 0) * out, boxSizing: 'border-box', padding: '0 44px',
          display: 'flex', alignItems: 'center', background: dk ? T.ink : T.bg, border: dk ? undefined : `4px dashed ${T.ink3}`, ...F, fontWeight: 700, fontSize: 50, color: dk ? T.dink : T.ink2, lineHeight: 1.3, wordBreak: 'keep-all'}}>{t}</div>;
      }) : null}
      {f >= d.start ? (
        <div style={{position: 'absolute', left: 150, top: 360 + (1 - ls) * 30, width: 1620, opacity: ls, background: T.ink, borderRadius: 20, padding: '34px 44px', boxSizing: 'border-box'}}>
          <div style={{...F, fontWeight: 700, fontSize: 34, color: T.dink3, whiteSpace: 'nowrap'}}>{d.label}</div>
          <div style={{...F, fontWeight: 700, fontSize: 56, color: T.daccent, marginTop: 14, whiteSpace: 'nowrap', letterSpacing: -1}}>{d.text}</div>
        </div>
      ) : null}
      {subs.length > 1 ? <DarkBar text={subs[subs.length - 1]} at={tEnd} x={150} y={640} w={1620} size={44} color={T.daccent} /> : null}
    </>
  );
};

const Body: React.FC<{s: WScene; next?: string}> = ({s, next}) => {
  switch (s.kind) {
    case 'open': return <Open s={s} />;
    case 'bars': return <Bars s={s} />;
    case 'three': return <Three s={s} />;
    case 'week': return <Week s={s} />;
    case 'count': return <Count s={s} />;
    case 'mline': return <MLine s={s} />;
    case 'grid': return <GridS s={s} />;
    case 'quote': return <Quote s={s} />;
    case 'rcpt': return <Rcpt s={s} />;
    case 'div': return <Div s={s} />;
    case 'pairs': return <Pairs s={s} />;
    case 'dots': return <Dots s={s} />;
    case 'pending': return <Pending s={s} />;
    case 'kbars': return <KBars s={s} />;
    case 'diverge': return <Diverge s={s} />;
    case 'stamp': return <StampS s={s} />;
    case 'bridge': return <Bridge s={s} />;
    case 'trio': return <Trio s={s} />;
    case 'cal': return <Cal s={s} />;
    case 'road': return <Road s={s} next={next} />;
    case 'sum': return <Sum s={s} />;
    case 'end': return <End s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: WScene; next?: string}> = ({s, next}) => {
  if (s.kind === 'logo') return <AbsoluteFill><LogoSting sub={s.data.sub} /></AbsoluteFill>;
  const st = tallyStarts(s.lines);
  return (
    <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines} capX={s.kind === 'end' ? 760 : 960}>
      <Body s={s} next={next} />
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </TallyFrame>
  );
};

export const W1: React.FC<W1Props> = (p) => {
  let from = 0;
  const endSub = p.scenes.find((x) => x.kind === 'end')?.sub; const next = endSub ? endSub.split(' · ').slice(-1)[0] : undefined;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} next={next} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
