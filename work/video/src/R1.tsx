// R-1 "1억의 1년 영수증"(X-SERIES-1 ①) 최종 화면 — 재료: work/video/r1.json(ep/R-1/r1props.py가 script.v6.md·voice.json·calc2_out·원자료로 만든다)
// 기준(2026-10-03 사장님 "잘 만든 다음에 반응을 봐라"): 오늘 조회 상위 한국 재테크 롱폼과 나란히 놓아도 밀리지 않는 화면.
//  - 흰 보드 + 형광 부제 + 판 안에서 문장마다 표시가 하나씩 더해짐(동그라미·값 꼬리표·말풍선·현재 줄 강조) — 참고: 소수몽키·수페TV 프레임(work/research/yt/full)
//  - 장면 20~40초마다 틀이 바뀜, 겹치는(누적) 구간 그래프 없음, 글자는 안전 구역 안(TallyFrame.SAFE), 본문 계산기 장면 없음(RULES X-CALC-VID)
// 숫자 글자는 전부 r1.json에서 온다(facts.txt 문구 그대로). 코드 안 숫자는 배치·눈금 값뿐.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {T, F, CL, LogoSting} from './parts/fm';
import {Stamp} from './parts/receipt';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';
import {TallyCountUp} from './motion/TallyCountUp';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyZoom} from './motion/TallyZoom';
import {TallyTag, TallyCallout, TallyCircle} from './motion/TallyMark';
import {TallyLineChart, lineXY} from './motion/TallyLineChart';

type RLine = TallyLine & {audio?: string | null};
export type RScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: RLine[]; frames: number};
export type R1Props = {fps: number; scenes: RScene[]; missing: number; script?: string; rate?: number};
export const r1Frames = (p: R1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {ink: T.ink2, ink3: T.ink3, accent: T.accent, rise: T.rise, fall: T.fall};
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const activeRow = (rows: TallyRow[], f: number) => { let k = -1; rows.forEach((r, i) => { if (f >= r.start) k = i; }); return k; };

const Note: React.FC<{text: string; at: number; x?: number; y?: number; color?: string; size?: number}> = ({text, at, x = 140, y = 760, color = T.ink2, size = 34}) => {
  const f = useCurrentFrame();
  return <div style={{...F, position: 'absolute', left: x, top: y + (1 - fade(f, at)) * 10, fontWeight: 700, fontSize: size, color, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{text}</div>;
};

// 왼쪽 큰 숫자(보드 왼쪽 절반) — 주황 큰 값 + 회색 설명
const Side: React.FC<{side?: [string, number, string]}> = ({side}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!side) return null;
  const s = spring({frame: f - side[1], fps, config: {damping: 12}});
  return (
    <div style={{position: 'absolute', left: 150, top: 470, opacity: f >= side[1] ? 1 : 0}}>
      <div style={{...F, fontWeight: 700, fontSize: side[0].length > 9 ? 76 : 120, color: T.accent, lineHeight: 1.05, whiteSpace: 'nowrap', letterSpacing: -2, transform: `scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center'}}>{side[0]}</div>
      <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2, marginTop: 14, whiteSpace: 'nowrap'}}>{side[2]}</div>
    </div>
  );
};

const Open: React.FC<{s: RScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const bars: TallyBar[] = d.bars.map(([name, at]: [string, number]) => ({label: name, value: 1, valueText: '1억', start: at, color: T.ink2}));
  return (
    <>
      <TallyBars bars={bars} x={980} y={400} w={780} h={330} max={1.3} labelSize={34} valueSize={40} tags />
      {d.bars.map((_: any, i: number) => (f >= d.q + 8 + i * 6 ? <div key={i} style={{...F, position: 'absolute', left: 980 + i * (780 + 0) / 4 + 50, top: 470, fontSize: 110, fontWeight: 700, color: '#fff', opacity: fade(f, d.q + 8 + i * 6, 6) * (f >= d.gap ? 0 : 1)}}>?</div> : null))}
      <div style={{...F, position: 'absolute', left: 150, top: 380, fontWeight: 700, fontSize: 100, color: T.ink, opacity: fade(f, 0), lineHeight: 1.08}}>1년 뒤<br /><span style={{color: T.accent}}>얼마?</span></div>
      <TallyCallout x={150} y={660} text={d.gapText} start={d.gap} size={32} />
    </>
  );
};

const Promise: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const rows: TallyRow[] = d.rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));
  return (
    <>
      <TallyReceipt x={980} y={300} w={800} head="파이어맵 영수증 규칙" rows={rows} size={34} active={activeRow(rows, f)} stamp={{text: '1편', start: d.stamp}} />
      <div style={{position: 'absolute', left: 150, top: 380}}>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, opacity: fade(f, 0)}}>시리즈</div>
        <div style={{...F, fontWeight: 700, fontSize: 84, color: T.ink, lineHeight: 1.1, opacity: fade(f, 4)}}>1억의<br />1년 영수증</div>
      </div>
      {f >= d.stamp ? <Stamp x={150} y={640} o={fade(f, d.stamp, 8)} text="1편 · 2025.10 → 2026.10" color={T.accent} size={34} /> : null}
      <TallyCallout x={150} y={740} text="순위까지 뒤집혔을까?" start={d.q} size={30} />
    </>
  );
};

const Road: React.FC<{s: RScene}> = ({s}) => {
  const f = useCurrentFrame();
  const rows: TallyRow[] = s.data.rows.map(([t, at]: [string, number]) => ({label: t, start: at, tone: 'in'}));
  return <TallyReceipt x={360} y={300} w={1200} head="1억의 1년 영수증 · 오늘 순서" rows={rows} size={44} active={activeRow(rows, f)} />;
};

const Receipt: React.FC<{s: RScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const rows: TallyRow[] = d.rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));
  const size = rows.length > 5 ? 31 : rows.length > 4 ? 33 : 36;
  return (
    <>
      <TallyReceipt x={980} y={300} w={800} head={d.head} rows={rows} size={size} active={activeRow(rows, f)} />
      <Side side={d.side} />
      {d.callout ? <TallyCallout x={150} y={720} text={d.callout[0]} start={d.callout[1]} size={30} w={760} /> : null}
    </>
  );
};

const Fx: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <div style={{position: 'absolute', left: 150, top: 360, opacity: fade(f, d.aAt)}}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>작년 그날 (2025.10.2)</div>
        <div style={{...F, fontWeight: 700, fontSize: 110, color: T.ink3, lineHeight: 1.05, letterSpacing: -2}}>{d.a}</div>
      </div>
      <div style={{position: 'absolute', left: 860, top: 430, ...F, fontSize: 80, fontWeight: 700, color: T.ink3, opacity: fade(f, d.start)}}>→</div>
      <TallyCountUp from={d.av} to={d.bv} text={d.b} start={d.start} dur={40} digits={1} suffix="원" size={140} color={T.fall} x={1000} y={340} label="올해 같은 날 (2026.10.2)" note={d.pct} />
      <TallyCallout x={150} y={640} text={`1억이면 환율만으로 ${d.loss}`} start={d.lossAt} size={34} />
      <TallyTag x={1320} y={660} text="ETF 값이 그대로여도 줄어듦" start={d.meanAt} side="right" />
    </>
  );
};

const Swing: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const X = 300, Y = 330, W = 1250, H = 450;
  const series = d.series.map(([name, col, pts]: [string, string, number[]]) => ({name, color: COL[col], pts, width: col === 'accent' ? 6 : 4, dash: col === 'ink3' ? '10 8' : undefined}));
  const xy = lineXY(X, Y, W, H, d.min, d.max, d.n);
  return (
    <>
      <TallyLineChart series={series} x={X} y={Y} w={W} h={H} min={d.min} max={d.max} start={d.draw} dur={75}
        base={{v: 10000, text: '넣은 돈 1억'}} ticks={[{v: 9000, text: '9,000'}, {v: 11000, text: '1.1억'}, {v: 13000, text: '1.3억'}, {v: 15000, text: '1.5억'}]}
        xlabels={d.xlabels.map(([i, t]: [number, string]) => ({i, text: t}))} />
      {d.tags.map((t: any, i: number) => { const [tx, ty] = xy(t[1], t[2]); return <TallyTag key={i} x={tx} y={ty} text={t[3]} start={t[4]} side={t[5]} hot={t[6]} size={22} />; })}
      <TallyCallout x={1560} y={330} text={d.fx[0]} start={d.fxAt} size={24} w={230} />
      <TallyCallout x={1560} y={420} text={d.fx[1]} start={d.fxAt + 40} size={24} w={230} />
    </>
  );
};

const HLine: React.FC<{x: number; w: number; y: number; text: string; at: number}> = ({x, w, y, text, at}) => {
  const f = useCurrentFrame(); const o = fade(f, at);
  return (
    <>
      <div style={{position: 'absolute', left: x - 20, width: (w + 40) * o, top: y, borderTop: `4px dashed ${T.rise}`}} />
      <div style={{...F, position: 'absolute', left: 150, top: y - 22, fontWeight: 700, fontSize: 30, color: T.rise, opacity: o, whiteSpace: 'nowrap'}}>{text}</div>
    </>
  );
};

const BarsBody: React.FC<{d: any; x0?: number}> = ({d, x0}) => {
  const f = useCurrentFrame();
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2, sub: b[5] ?? undefined, lo: b[6], loText: b[7]}));
  const n = bars.length;
  if (d.dir === 'h') {
    return <TallyBars dir="h" bars={bars} x={x0 ?? 140} y={400} w={x0 ? 1780 - x0 : 1460} h={n * 110 + (n - 1) * 44} max={d.max} min={d.min ?? 0} labelSize={34} valueSize={34} gap={44}
      marker={d.marker ? {value: d.marker[0], text: d.marker[1], start: d.marker[2]} : undefined} />;
  }
  const w = x0 ? 1760 - x0 : n <= 2 ? 640 : n <= 4 ? 940 : 1180;
  const x = x0 ?? (n <= 2 ? 1060 : n <= 4 ? 820 : 580);
  const min = d.min ?? 0; const H = 330, Y = 410;
  return (
    <>
      <TallyBars bars={bars} x={x} y={Y} w={w} h={H} max={d.max} min={min} labelSize={n > 4 ? 24 : 30} valueSize={n > 4 ? 30 : 36} tags={d.tags}
        circle={d.circle ? {i: d.circle[0], start: d.circle[1]} : undefined} />
      {d.hline ? <HLine x={x} w={w} y={Y + H * (1 - (d.hline[0] - min) / (d.max - min))} text={d.hline[1]} at={d.hline[2]} /> : null}
      {d.note ? <Note text={d.note[0]} at={d.note[1]} x={150} y={400} size={n > 4 ? 30 : 34} /> : null}
      {d.note2 ? <Note text={d.note2[0]} at={d.note2[1]} x={150} y={460} size={30} color={T.accent} /> : null}
      {f < 0 ? null : null}
    </>
  );
};

const Bars: React.FC<{s: RScene}> = ({s}) => <BarsBody d={s.data} />;

// 사람 카드(사진 없음 — 나이 글자 원 + 상황) + 오른쪽 그래프
const Person: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const sp = spring({frame: f, fps, config: {damping: 14}});
  return (
    <>
      <div style={{position: 'absolute', left: 140, top: 300, width: 420, height: 400, background: T.bg, borderRadius: 22, transform: `translateX(${(1 - sp) * -40}px)`, opacity: sp}}>
        <div style={{position: 'absolute', left: 130, top: 40, width: 160, height: 160, borderRadius: 80, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <span style={{...F, fontWeight: 700, fontSize: 52, color: '#fff'}}>{d.who}</span>
        </div>
        <div style={{...F, position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center', fontWeight: 700, fontSize: 36, color: T.ink}}>{d.what}</div>
        <div style={{position: 'absolute', left: 60, right: 60, top: 300, height: 8, borderRadius: 4, background: T.accent}} />
      </div>
      <BarsBody d={d} x0={d.dir === 'h' ? 620 : 760} />
      {d.callout ? <TallyCallout x={d.dir === 'h' ? 1150 : 1250} y={d.dir === 'h' ? 680 : 300} text={d.callout[0]} start={d.callout[1]} size={30} /> : null}
    </>
  );
};

const Count: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <Note text={d.pre} at={d.preAt} x={150} y={340} color={T.ink3} size={40} />
      <TallyCountUp from={d.from} to={d.to} text={d.text} start={d.start} dur={45} suffix="원" size={150} color={T.accent} x={150} y={420} label={d.label} />
      <TallyTag x={1300} y={700} text={d.cut} start={d.cutAt} side="left" hot size={30} />
      {d.callout ? <TallyCallout x={1180} y={340} text={d.callout[0]} start={d.callout[1]} size={30} w={560} /> : null}
    </>
  );
};

const Zoom: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <div style={{position: 'absolute', left: 140, top: 330, width: 760, height: 420, background: T.soft, borderRadius: 22, opacity: fade(f, 0)}} />
      <TallyZoom text={d.text} start={d.start} x={190} y={420} size={150} label={d.label} note={d.note} />
      {d.after ? (
        <div style={{position: 'absolute', left: 1000, top: 400, opacity: fade(f, d.after[3])}}>
          <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>{d.after[0]}</div>
          <div style={{...F, fontWeight: 700, fontSize: 80, color: T.ink, whiteSpace: 'nowrap', letterSpacing: -1}}>{d.after[1]}</div>
          <div style={{...F, fontWeight: 700, fontSize: 50, color: T.accent}}>{d.after[2]}</div>
        </div>
      ) : null}
    </>
  );
};

const Act: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const rows: TallyRow[] = d.rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));
  return (
    <>
      <TallyReceipt x={700} y={310} w={1080} head={d.head} rows={rows} size={38} active={activeRow(rows, f)} />
      <div style={{position: 'absolute', left: 150, top: 380, opacity: fade(f, 0)}}>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2}}>오늘 할 일</div>
        <div style={{...F, fontWeight: 700, fontSize: 130, color: T.accent, lineHeight: 1}}>하나</div>
      </div>
    </>
  );
};

const End: React.FC<{s: RScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <TallyZoom text={d.text} start={d.start} x={150} y={420} size={150} label={d.label} note={d.note} />
      <div style={{position: 'absolute', left: 1000, top: 300, width: 780, height: 440, borderRadius: 20, border: `3px dashed ${T.line}`, opacity: fade(f, 0, 14)}} />
    </>
  );
};

const Body: React.FC<{s: RScene}> = ({s}) => {
  switch (s.kind) {
    case 'open': return <Open s={s} />;
    case 'promise': return <Promise s={s} />;
    case 'road': return <Road s={s} />;
    case 'receipt': return <Receipt s={s} />;
    case 'fx': return <Fx s={s} />;
    case 'swing': return <Swing s={s} />;
    case 'bars': return <Bars s={s} />;
    case 'person': return <Person s={s} />;
    case 'count': return <Count s={s} />;
    case 'zoom': return <Zoom s={s} />;
    case 'act': return <Act s={s} />;
    case 'end': return <End s={s} />;
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

// 썸네일 1280×720 — 위 절반 그림(영수증 네 장 막대), 아래 두 줄 큰 글자(주황 숫자 줄 + 흰 줄). 사람 사진 없음.
export const R1Thumb: React.FC<{net: [string, string, string][]}> = ({net}) => (
  <AbsoluteFill style={{background: '#101114'}}>
    <style>{`@font-face{font-family:'PD';font-weight:700;src:url('${staticFile('fonts/pd700.ttf')}')}`}</style>
    {net.map(([name, val, pct], i) => {
      const h = [220, 165, 80, 66][i];
      return (
        <div key={i} style={{position: 'absolute', left: 70 + i * 290, top: 320 - h, width: 250}}>
          <div style={{...F, fontWeight: 700, fontSize: 30, color: i === 0 ? T.daccent : '#c9ccd2', textAlign: 'center', marginBottom: 8}}>{pct}</div>
          <div style={{height: h, background: i === 0 ? T.accent : '#3a3d45', borderRadius: '14px 14px 0 0'}} />
          <div style={{...F, fontWeight: 700, fontSize: 32, color: '#fff', textAlign: 'center', marginTop: 8}}>{name}</div>
        </div>
      );
    })}
    <div style={{position: 'absolute', left: 60, right: 60, top: 408, height: 4, background: '#2a2c33'}} />
    <div style={{...F, position: 'absolute', left: 50, top: 428, fontWeight: 700, fontSize: 100, color: T.daccent, letterSpacing: -3, whiteSpace: 'nowrap'}}>세금이 줄인 차이 307만원</div>
    <div style={{...F, position: 'absolute', left: 50, top: 556, fontWeight: 700, fontSize: 96, color: '#fff', letterSpacing: -3, whiteSpace: 'nowrap'}}>1억 넣고 1년, 실제 영수증</div>
    <div style={{...F, position: 'absolute', left: 1010, top: 40, fontWeight: 700, fontSize: 28, color: '#101114', background: T.daccent, borderRadius: 10, padding: '6px 16px'}}>1억의 1년 영수증 #1</div>
  </AbsoluteFill>
);
