// G-1 "금값 1천만원 영수증 4장" 화면 — 재료: work/video/g1.json(ep/G-1/g1props.py가 script.md·voice.json·calc_out.txt·raw로 만든다)
// 틀은 R-1(1억의 1년 영수증)과 같은 TallyFrame(흰 보드·형광 부제·[자막] 칩·출처) + 영수증 종이. 새 그림은 parts/gold.tsx(세 조각 좌우 막대·줄어든 만큼 막대·몫 나누기·살 때/팔 때 띠).
// 숫자 글자는 전부 g1.json에서 온다(calc_out 문구 그대로). 코드 안 숫자는 배치 좌표뿐. 본문 계산기 장면 없음(RULES X-CALC-VID), 전망 없음.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, spring, useVideoConfig, Easing} from 'remotion';
import {T, F, CL, LogoSting} from './parts/fm';
import {Stamp} from './parts/receipt';
import {Tokens, Tok} from './parts/explain';
import {RuleCards, Grid} from './parts/reverse';
import {DivRows, LossRows, SplitBar, SpreadBand} from './parts/gold';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';
import {TallyCountUp} from './motion/TallyCountUp';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyZoom} from './motion/TallyZoom';
import {TallyTag, TallyCallout} from './motion/TallyMark';
import {TallyLineChart, lineXY} from './motion/TallyLineChart';
import {BuyDateOpen} from './motion/BuyDateOpen';
import {WaterfallPieces} from './motion/WaterfallPieces';
import {AsymClimb} from './motion/AsymClimb';

type GLine = TallyLine & {audio?: string | null};
export type GScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: GLine[]; frames: number};
export type G1Props = {fps: number; scenes: GScene[]; missing: number; script?: string; rate?: number; asof?: string};
export const g1Frames = (p: G1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {ink: T.ink2, ink3: T.ink3, accent: T.accent, rise: T.rise, fall: T.fall};
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const activeRow = (rows: TallyRow[], f: number) => { let k = -1; rows.forEach((r, i) => { if (f >= r.start) k = i; }); return k; };
const toRows = (rows: any[]): TallyRow[] => rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));

const Note: React.FC<{text: string; at: number; x?: number; y?: number; color?: string; size?: number}> = ({text, at, x = 150, y = 760, color = T.ink2, size = 34}) => {
  const f = useCurrentFrame();
  return <div style={{...F, position: 'absolute', left: x, top: y + (1 - fade(f, at)) * 10, fontWeight: 700, fontSize: size, color, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{text}</div>;
};

// U5(10/11 motion): 줄이 바뀌면 그 줄이 말하는 항목을 판에서 꺼낸다 — 검은 띠·검은 카드·값 띠. 글자는 props·다른 장면에 이미 있는 것만 다시 놓는다.
const pickAt = (tl: [number, number][] | undefined, f: number, dflt: number) => { let k = dflt; (tl ?? []).forEach(([at, v]) => { if (f >= at) k = v; }); return k; };
const DarkBar: React.FC<{text: string; at: number; x: number; y: number; w: number; size?: number; color?: string; bg?: string; wrap?: boolean}> = ({text, at, x, y, w, size = 44, color = T.dink, bg = T.ink, wrap}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (f < at) return null;
  const sp = spring({frame: f - at, fps, config: {damping: 14}});
  return <div style={{position: 'absolute', left: x, top: y + (1 - sp) * 20, width: w, opacity: sp, background: bg, borderRadius: 16, padding: '22px 34px', boxSizing: 'border-box',
    ...F, fontWeight: 700, fontSize: size, color, whiteSpace: wrap ? 'normal' : 'nowrap', wordBreak: 'keep-all', lineHeight: 1.25}}>{text}</div>;
};
// 영수증 한 줄을 검은 띠로(TallyReceipt와 같은 자리·같은 글자)
const DarkRow: React.FC<{r: TallyRow; x: number; y: number; w: number; size: number; i: number}> = ({r, x, y, w, size, i}) => {
  const rowH = size * 1.75; const tone = r.tone ?? 'in';
  const col = tone === 'tax' ? '#ff8a8d' : tone === 'net' || tone === 'hi' ? T.daccent : T.dink;
  return (
    <div style={{position: 'absolute', left: x + 30, width: w - 60, top: y + 96 + i * rowH, height: rowH, background: T.ink, borderRadius: 8, display: 'flex', alignItems: 'center', padding: '0 18px', boxSizing: 'border-box'}}>
      <span style={{...F, fontWeight: 700, fontSize: tone === 'net' ? size * 0.92 : size * 0.8, color: T.dink, whiteSpace: 'nowrap'}}>{r.label}</span>
      <span style={{...F, fontWeight: 700, fontSize: tone === 'net' ? size * 1.15 : size, color: col, marginLeft: 'auto', whiteSpace: 'nowrap'}}>{r.value ?? ''}</span>
    </div>
  );
};

const Side: React.FC<{side?: [string, number, string]; y?: number; hideSub?: boolean}> = ({side, y = 440, hideSub}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  if (!side) return null;
  const s = spring({frame: f - side[1], fps, config: {damping: 12}});
  return (
    <div style={{position: 'absolute', left: 150, top: y, opacity: f >= side[1] ? 1 : 0}}>
      <div style={{...F, fontWeight: 700, fontSize: side[0].length > 8 ? 84 : 120, color: T.accent, lineHeight: 1.05, whiteSpace: 'nowrap', letterSpacing: -2, transform: `scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center'}}>{side[0]}</div>
      {hideSub ? null : <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginTop: 14, whiteSpace: 'nowrap'}}>{side[2]}</div>}
    </div>
  );
};

// 여는 장면: 영수증 두 장(고점 / 1년 전) — 첫 프레임부터 종이가 내려온다
const Twin: React.FC<{s: GScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <>
      {d.cards.map((c: any, i: number) => {
        const rows = toRows(c.rows); const x = i === 0 ? 150 : 990; const st = i === 0 ? 0 : c.rows[0][3];
        return (
          <React.Fragment key={i}>
            {f >= st ? <TallyReceipt x={x} y={310} w={780} head={c.head} rows={rows} size={32} start={st} active={activeRow(rows, f)} /> : null}
            {f >= c.bigAt ? <div style={{position: 'absolute', left: x + 40, top: 700, display: 'flex', alignItems: 'baseline', gap: 22}}>
              <TallyZoom text={c.big} start={c.bigAt} x={0} y={0} size={96} color={i === 0 ? T.fall : T.ink} />
              <div style={{...F, position: 'absolute', left: 430, top: 30, fontWeight: 700, fontSize: 40, color: T.fall, opacity: fade(f, c.bigAt + 10), whiteSpace: 'nowrap'}}>{c.pct}</div>
            </div> : null}
          </React.Fragment>
        );
      })}
    </>
  );
};

const Cards: React.FC<{s: GScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  let act = -1; d.cards.forEach((c: any, i: number) => { if (f >= c[3]) act = i; });
  return <RuleCards cards={d.cards} active={act} x={150} y={400} w={1620} />;
};

const Road: React.FC<{s: GScene}> = ({s}) => {
  const f = useCurrentFrame();
  const rows: TallyRow[] = s.data.rows.map(([t, at]: [string, number]) => ({label: t, start: at, tone: 'in'}));
  return <TallyReceipt x={360} y={290} w={1200} head="금값 1천만원 영수증 · 오늘 순서" rows={rows} size={42} active={activeRow(rows, f)} />;
};

const Line: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data;
  const X = 260, Y = 320, W = d.callouts ? 940 : 1260, H = 430;
  const series = d.series.map(([name, col, pts]: [string, string, number[]]) => ({name, color: COL[col], pts, width: col === 'accent' ? 6 : 5}));
  const n = d.series[0][2].length; const xy = lineXY(X, Y, W, H, d.min, d.max, n); const f = useCurrentFrame();
  const SH = [T.fall, T.rise];   // U5: shade = [시작 점, 위 값, 아래 값, 나타남, 사라짐, 색] — 산 값~오늘 값 띠
  return (
    <>
      {(d.cols ?? []).map(([i, a, b]: number[], k: number) => { if (f < a || f >= b) return null; const [cx] = xy(i, d.min);
        return <div key={'c' + k} style={{position: 'absolute', left: cx - 20, top: Y, width: 40, height: H, background: T.ink, opacity: 0.16 * fade(f, a + k * 4, 8), borderRadius: 8}} />; })}
      {(d.shade ?? []).map(([i, v1, v2, a, b, tone]: number[], k: number) => { if (f < a || f >= b) return null; const [x1, y1] = xy(i, v1); const [x2, y2] = xy(n - 1, v2); const c = SH[tone] ?? T.fall;
        return <React.Fragment key={'s' + k}>
          <div style={{position: 'absolute', left: x1, top: Math.min(y1, y2), width: (x2 - x1) * fade(f, a, 14), height: Math.abs(y2 - y1), background: c, opacity: 0.3}} />
          <div style={{position: 'absolute', left: x1 - 3, top: Math.min(y1, y2), width: 6, height: Math.abs(y2 - y1), background: c, opacity: fade(f, a, 6)}} />
        </React.Fragment>; })}
      <TallyLineChart series={series} x={X} y={Y} w={W} h={H} min={d.min} max={d.max} start={d.draw} dur={d.dur ?? 60}
        base={d.base ? {v: d.base[0], text: d.base[1]} : undefined} ticks={d.ticks.map(([v, t]: [number, string]) => ({v, text: t}))}
        xlabels={d.xlabels.map(([i, t]: [number, string]) => ({i, text: t}))} />
      {d.tags.map((t: any, i: number) => { const [tx, ty] = xy(t[0], t[1]); return <TallyTag key={i} x={tx} y={ty} text={t[2]} start={t[3]} side={t[4]} hot={t[5]} size={24} />; })}
      {(d.callouts ?? []).map((c: any, i: number) => <TallyCallout key={i} x={c[2]} y={c[3]} text={c[0]} start={c[1]} size={30} w={500} />)}
      {(d.pull ?? []).map(([ti, py]: number[], i: number) => <DarkBar key={'p' + i} text={d.tags[ti][2]} at={d.tags[ti][3]} x={1350} y={py} w={450} size={36} bg={d.tags[ti][5] ? T.accent : T.ink} color="#fff" />)}
    </>
  );
};

const Loss: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <LossRows x={170} y={340} w={820} rowH={d.rows.length > 3 ? 112 : 130} max={d.max} rows={d.rows} />
      {d.gap ? <TallyCallout x={1180} y={720} text={d.gap[0]} start={d.gap[1]} size={30} /> : null}
    </>
  );
};

const Diverge: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <DivRows x0={900} y={400} rowH={150} half={380} max={d.max} rows={d.rows} labelW={340} />
      {d.q && f >= d.q[1] ? <TallyZoom text={d.q[0]} start={d.q[1]} x={1000} y={720} size={d.q[0].length > 4 ? 52 : 110} color={T.accent} /> : null}
    </>
  );
};

const Formula: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  let si = 0;
  const toks: Tok[] = d.toks.map(([t, at, tone]: [string, number, string]) => {
    const o = fade(f, at, 12);
    if (tone === 'op') return {t, o, op: true};
    const sub = tone === 'ink' ? d.subs[si++] : undefined;
    return {t, o, tone: tone === 'num' ? 'soft' : 'ink', sub, subO: o};
  });
  return <Tokens x={170} y={450} toks={toks} size={58} gap={22} />;
};

const Pieces: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <DivRows x0={900} y={330} rowH={108} half={380} max={d.max} rows={d.rows} total />
      {d.prem ? <TallyCallout x={1000} y={775} text={d.prem[0]} start={d.prem[1]} size={28} w={520} /> : null}
      {d.note ? <Note text={d.note[0]} at={d.note[1]} x={170} y={790} color={T.accent} size={36} /> : null}
    </>
  );
};

const GridS: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const fr = pickAt(d.focus, f, -1); const row = fr >= 0 ? d.rows[fr] : null;
  const GY = 292;   // 정확한 값 칩(y 252~297)이 첫 열 머리 '달러 금값'을 가리지 않게
  const lw = 380, cw = (1620 - lw) / d.cols.length, rh = d.rows.length > 2 ? 120 : 150, top = GY + 76 + 10 + fr * rh;
  return (
    <>
      <Grid cols={d.cols} rows={row && f >= row[2] ? d.rows.map((r: any, i: number) => i === fr ? ['', r[1].map(() => ''), r[2]] : r) : d.rows} hot={d.hot} x={150} y={GY} w={1620} />
      {row && f >= row[2] ? <div style={{position: 'absolute', left: 150, top: top - 4, width: 1620, height: rh - 10, background: T.ink, borderRadius: 14}}>
        <div style={{...F, position: 'absolute', left: 24, top: 0, height: rh - 10, display: 'flex', alignItems: 'center', fontWeight: 700, fontSize: 40, color: T.dink, whiteSpace: 'nowrap'}}>{row[0]}</div>
        {row[1].map((c: string, i: number) => { const h = d.hot.find(([hr, hc]: number[]) => hr === fr && hc === i); const on = h ? f >= h[2] : false;
          return <div key={i} style={{position: 'absolute', left: lw + i * cw + 12, width: cw - 24, top: 4, height: rh - 18, borderRadius: 14, background: on ? T.accent : 'transparent',
            display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 700, fontSize: 54, color: on ? '#fff' : T.dink, whiteSpace: 'nowrap'}}>{c}</div>; })}
      </div> : null}
    </>
  );
};

const Law: React.FC<{s: GScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const rows = toRows(d.rows); const size = rows.length > 4 ? 31 : 34;
  const act = activeRow(rows, f); const fr0 = d.focus ? pickAt(d.focus, f, -1) : -1; const fr = fr0 === -2 ? act : fr0;   // -2 = 방금 찍힌 줄
  return (
    <>
      <TallyReceipt x={900} y={280} w={880} head={d.head} rows={fr >= 0 && f >= rows[fr].start + 10 ? rows.map((r, i) => i === fr ? {...r, label: '', value: ''} : r) : rows} size={size} active={act} />
      {fr >= 0 && f >= rows[fr].start + 10 ? <DarkRow r={rows[fr]} x={900} y={280} w={880} size={size} i={fr} /> : null}
      <Side side={d.side} hideSub={d.side2At != null} />
      {d.side2At != null && d.side ? <DarkBar text={d.side[2]} at={d.side2At} x={150} y={600} w={700} size={36} wrap /> : null}
    </>
  );
};

const Spread: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <SpreadBand x={200} y={560} w={900} step={150} mid={d.mid} buy={d.buy} sell={d.sell} gap={d.gap}
        labels={{mid: '기준가격', buy: '살 때 +1.00%', sell: '팔 때 −1.00%', gap: '사고팔기만 해도 2% 가까이'}} />
      <TallyTag x={1360} y={360} text="차익엔 배당소득세 15.4%" start={d.tax} side="right" size={26} />
      <DarkBar text="원 단위 결과는 고시 확인 전" at={d.stamp} x={1390} y={540} w={410} size={46} wrap />
    </>
  );
};

const Split: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <SplitBar x={200} y={400} w={1400} h={130} ratio={d.ratio} at={d.at} splitAt={d.vatAt} whole="낸 돈 1천만원"
        a={['금값 몫', d.gold]} b={['부가세 10%', d.vat]} />
      {f >= d.need[1] ? <>
        <div style={{position: 'absolute', left: 200, top: 670, width: 1400 * (1 - d.ratio), height: 80, background: T.ink2, borderRadius: '12px 0 0 12px', opacity: fade(f, d.need[1], 8)}} />
        <div style={{position: 'absolute', left: 200 + 1400 * (1 - d.ratio), top: 670, height: 80, background: T.accent, borderRadius: '0 12px 12px 0',
          width: (1400 * d.ratio + 18) * interpolate(f, [d.need[1] + 8, d.need[1] + 38], [0, 1], {...CL, easing: Easing.out(Easing.cubic)})}} />
      </> : null}
      <TallyCallout x={200} y={770} text={d.need[0]} start={d.need[1]} size={32} />
      <Note text={d.fee[0]} at={d.fee[1]} x={900} y={785} color={T.ink3} size={28} />
    </>
  );
};

const Bars: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2, sub: b[5] ?? undefined}));
  return <TallyBars bars={bars} x={600} y={360} w={720} h={360} max={d.max} labelSize={32} valueSize={44} />;
};

const Quote: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <div style={{position: 'absolute', left: 150, top: 290 + (1 - fade(f, d.at)) * 24, width: 1620, height: 220, background: T.surface, borderRadius: 20, opacity: fade(f, d.at), borderTop: `8px solid ${T.ink}`}}>
        <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink3, padding: '26px 40px 0'}}>{d.src}</div>
        <div style={{...F, fontWeight: 700, fontSize: 52, color: T.ink, padding: '28px 40px 0', whiteSpace: 'nowrap'}}>{d.body}</div>
      </div>
      <DarkBar text={d.q2} at={d.q2At} x={150} y={540} w={1620} size={40} />
      {f >= d.bigAt ? <Stamp x={170} y={680} o={fade(f, d.bigAt, 8)} text={d.big} color={T.rise} size={44} rot={-4} /> : null}
    </>
  );
};

const Count: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <TallyCountUp from={d.from} to={d.to} text={d.text} start={d.start} dur={40} prefix="US$" suffix="bn" size={150} color={T.accent} x={150} y={360} label={d.label} note={d.pre} />
      <TallyTag x={1150} y={460} text={d.tag[0]} start={d.tag[1]} side="right" hot size={32} />
      <TallyCallout x={1150} y={620} text={d.call[0]} start={d.call[1]} size={30} />
    </>
  );
};

const Stamps: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const g = 36, w = (1620 - g * 3) / 4;
  return (
    <>
      {d.cards.map(([h, sub, at]: [string, string, number], i: number) => {
        const sp = spring({frame: f - at, fps, config: {damping: 14}});
        return (
          <div key={i} style={{position: 'absolute', left: 150 + i * (w + g), top: 340 + (1 - sp) * 30, width: w, height: 260, background: T.surface, borderRadius: 20, opacity: f >= at ? sp : 0,
            boxShadow: '0 10px 30px rgba(0,0,0,0.07)'}}>
            <div style={{...F, position: 'absolute', left: 30, top: 34, fontWeight: 700, fontSize: 52, color: T.ink}}>{h}</div>
            <div style={{...F, position: 'absolute', left: 30, top: 120, fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{sub}</div>
            {f >= d.stamp[1] ? <Stamp x={26} y={180} o={fade(f, d.stamp[1] + i * 4, 8)} text={d.stamp[0]} color={T.rise} size={24} rot={-6} /> : null}
          </div>
        );
      })}
      <DarkBar text={d.no[0]} at={d.no[1]} x={150} y={650} w={760} size={46} />
    </>
  );
};

const Asym: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = [{label: '내려온 폭', value: d.down[0], valueText: d.down[1], start: d.down[2], color: T.fall}, {label: '산 값까지 올라야 할 폭', value: d.up[0], valueText: d.up[1], start: d.up[2], color: T.rise}];
  return (
    <>
      <TallyCountUp from={d.from} to={d.to} text={d.to.toLocaleString('en-US') + '원'} start={d.start} dur={45} suffix="원" size={96} color={T.ink} x={150} y={360} label="1g 값이 돌아가야 할 곳" note={`지금 ${d.from.toLocaleString('en-US')}원`} />
      <TallyBars bars={bars} x={1000} y={330} w={720} h={380} max={60} labelSize={28} valueSize={48} />
      <TallyCallout x={150} y={620} text={d.note[0]} start={d.note[1]} size={32} />
      <Note text={d.fee[0]} at={d.fee[1]} x={150} y={760} color={T.ink3} size={28} />
    </>
  );
};

const End: React.FC<{s: GScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const {fps} = useVideoConfig(); const st = tallyStarts(s.lines);
  // U5: 끝 화면 20초(말 11초 + 엔드 스크린) — 줄마다 왼쪽 판이 바뀐다: 숫자 → '지나간 값' 띠 → 전체 표 카드 → 카페 글 띠. 오른쪽 점선 상자는 엔드 스크린 자리라 비워 둔다.
  const tEnd = st[st.length - 1] + s.lines[s.lines.length - 1].frames;
  const cardAt = st[2] ?? tEnd; const ctaAt = tEnd + 48;
  const out = interpolate(f, [cardAt - 6, cardAt], [1, 0], CL); const cs = spring({frame: f - cardAt, fps, config: {damping: 14}});
  return (
    <>
      {f < cardAt ? <div style={{opacity: out}}><TallyZoom text={d.text} start={d.start} x={150} y={420} size={110} label={d.label} note={d.note} /></div> : null}
      {f >= cardAt ? <div style={{position: 'absolute', left: 150, top: 380 + (1 - cs) * 30, width: 820, opacity: cs, background: T.ink, borderRadius: 20, padding: '30px 40px', boxSizing: 'border-box'}}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.dink3, whiteSpace: 'nowrap'}}>{d.label}</div>
        <div style={{...F, fontWeight: 700, fontSize: 84, color: T.daccent, marginTop: 12, whiteSpace: 'nowrap', letterSpacing: -2}}>{d.text}</div>
      </div> : null}
      {s.source && f < ctaAt ? <DarkBar text={s.source} at={st[1] ?? 0} x={150} y={670} w={820} size={38} /> : null}
      <DarkBar text={d.note} at={ctaAt} x={150} y={670} w={820} size={44} bg={T.accent} color="#fff" />
      <div style={{position: 'absolute', left: 1000, top: 300, width: 780, height: 440, borderRadius: 20, border: `3px dashed ${T.line}`, opacity: fade(f, 0, 14)}} />
    </>
  );
};

const Body: React.FC<{s: GScene}> = ({s}) => {
  switch (s.kind) {
    case 'open': return <BuyDateOpen {...s.data.open} />;   // motion-designer 첫 장면(10/10 PD 넣음)
    case 'waterfall': return <WaterfallPieces {...s.data.wf} />;   // 3장 세 조각(piece1·prem·piece1b 자리)
    case 'twin': return <Twin s={s} />;
    case 'cards': return <Cards s={s} />;
    case 'road': return <Road s={s} />;
    case 'line': return <Line s={s} />;
    case 'loss': return <Loss s={s} />;
    case 'diverge': return <Diverge s={s} />;
    case 'formula': return <Formula s={s} />;
    case 'pieces': return <Pieces s={s} />;
    case 'grid': return <GridS s={s} />;
    case 'law': return <Law s={s} />;
    case 'spread': return <Spread s={s} />;
    case 'split': return <Split s={s} />;
    case 'bars': return <Bars s={s} />;
    case 'quote': return <Quote s={s} />;
    case 'count': return <Count s={s} />;
    case 'stamps': return <Stamps s={s} />;
    case 'asym': return s.data.asym ? <AsymClimb {...s.data.asym} /> : <Asym s={s} />;   // 6장 AsymClimb, 없으면 옛 판
    case 'end': return <End s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: GScene}> = ({s}) => {
  if (s.kind === 'logo') return <AbsoluteFill><LogoSting sub={s.data.sub} /></AbsoluteFill>;
  const st = tallyStarts(s.lines);
  return (
    <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines}>
      <Body s={s} />
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </TallyFrame>
  );
};

export const G1: React.FC<G1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
export const _g1unused = {tallyIdx};
