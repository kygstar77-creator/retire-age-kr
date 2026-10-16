// C-1 롱폼(DBJaHJ2pVTw)을 자른 세로 쇼츠(1080×1920) — 재료: work/video/c1s_<편>.json (research/cardshorts/c1clips.py가 c1.json에서 만든다)
// 틀은 M1S v2와 같다(위 검은 띠 질문 2줄 · 가운데 흰 판 · 10~15자 자막 조각 · 아래 답 칸 고정 · 링크 안내 줄 없음).
// 목소리는 C-1 voice.json wav 그대로(Chirp 3 HD Charon). 숫자 글자는 전부 props(c1.json = 편집 통과한 롱폼 화면 글자)에서 온다. 코드 안 숫자는 배치 값뿐.
// 판 안 그림은 C-1 부품(parts/withdraw·reverse·gold·motion/Tally*)을 세로 판(1000×860) 좌표로 다시 놓은 것. 시각(프레임)은 c1clips.py가 장면 안 프레임으로 넘긴다.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing, spring} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from './parts/fm';
import {Stamp} from './parts/receipt';
import {DivRows} from './parts/gold';
import {Tank, Person, Ruler, YearBars} from './parts/withdraw';
import {TallyBars, TallyBar} from './motion/TallyBars';
import {TallyReceipt, TallyRow} from './motion/TallyReceipt';
import {TallyTag, TallyCallout} from './motion/TallyMark';
import {TallyLineChart, lineXY} from './motion/TallyLineChart';
import {TopBand, AnswerCard, BottomShade, boardBox, capTop, capSize, CAP_H, SZ, Answer} from './parts/safeframe';

type SLine = {n: number; text: string; cap?: string | null; audio: string; frames: number};
type SScene = {kind: string; label: string; source?: string | null; data: any; lines: SLine[]; frames: number};
export type C1SProps = {fps: number; name: string; question: string[]; hot: string; base: string; scenes: SScene[]; answer?: {label: string; items: string[]; arrow?: boolean; note?: string} | null};
export const c1sFrames = (p: C1SProps) => p.scenes.reduce((a, s) => a + s.frames, 0);

const BW = 1000, BH = 860;
const COL: Record<string, string> = {accent: T.accent, ink: T.ink2, rise: T.rise, fall: T.fall, ink3: T.ink3};
const starts = (lines: SLine[]) => { const o: number[] = []; let a = 0; for (const l of lines) { o.push(a); a += l.frames; } return o; };
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);
const toRows = (rows: any[]): TallyRow[] => rows.map(([label, value, tone, at]: [string, string, any, number]) => ({label, value, tone, start: at}));
const activeRow = (rows: TallyRow[], f: number) => { let k = -1; rows.forEach((r, i) => { if (f >= r.start) k = i; }); return k; };
const Txt: React.FC<{s: number; c?: string; children: React.ReactNode; style?: React.CSSProperties}> = ({s, c = T.ink, children, style}) => (
  <div style={{...F, fontWeight: 700, fontSize: s, color: c, lineHeight: 1.18, letterSpacing: s > 60 ? -2 : -0.5, wordBreak: 'keep-all', whiteSpace: 'nowrap', ...style}}>{children}</div>
);
const Big: React.FC<{side?: [string, number, string] | null; x?: number; y?: number}> = ({side, x = 40, y = 560}) => {
  const f = useCurrentFrame(); if (!side || f < side[1]) return null;
  const s = spring({frame: f - side[1], fps: 30, config: {damping: 12}});
  return <div style={{position: 'absolute', left: x, top: y}}>
    <Txt s={side[0].length > 8 ? 76 : 100} c={T.accent} style={{transform: `scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center'}}>{side[0]}</Txt>
    <Txt s={34} c={T.ink2} style={{marginTop: 10}}>{side[2]}</Txt>
  </div>;
};

// ───────── 장면들 (판 안 좌표 1000×860) ─────────
// 시작 해 칸: 사람마다 18칸(9칸 × 2줄). 20년 안에 바닥난 칸(‘+’ 없고 ≤20)만 그 사람 색으로 켜진다. rows = [이름, 색, [[해, 연차]], 켜지는 프레임, 개수 글자, 개수 프레임]
const TileGrid: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const cw = 94, ch = 86, g = 9;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 22}}><Txt s={34} c={T.ink2}>{d.head}</Txt></div>
      {d.rows.map(([name, col, cells, at, cnt, cntAt]: any, r: number) => {
        const y0 = 92 + r * 370; const c = COL[col] ?? T.ink;
        return (
          <div key={r} style={{position: 'absolute', left: 40, top: y0, width: 920}}>
            <Txt s={50} c={c}>{name}</Txt>
            <div style={{position: 'absolute', right: 0, top: -14, opacity: fade(f, cntAt), transform: `scale(${0.8 + 0.2 * fade(f, cntAt, 8)})`, transformOrigin: 'right center'}}><Txt s={92} c={c}>{cnt}</Txt></div>
            {cells.map(([yv, v]: [number, string], i: number) => {
              const dead = !v.endsWith('+') && Number(v) <= 20; const on = dead && f >= at + i * 2;
              return (
                <div key={i} style={{position: 'absolute', left: (i % 9) * (cw + g) + 2, top: 84 + Math.floor(i / 9) * (ch + g), width: cw, height: ch, borderRadius: 12, background: on ? c : T.bg,
                  display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
                  <span style={{...F, fontWeight: 500, fontSize: 20, color: on ? 'rgba(255,255,255,0.8)' : T.ink3}}>{String(yv).slice(2)}</span>
                  <span style={{...F, fontWeight: 700, fontSize: 34, color: on ? '#fff' : T.ink3, lineHeight: 1}}>{v}</span>
                </div>
              );
            })}
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 40, top: 800}}><Txt s={26} c={T.ink3}>{d.foot}</Txt></div>
    </>
  );
};

const TankS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div>
      <Tank x={40} y={140} w={400} h={400} label={d.tank} out={d.out} inText={d.in} />
      <div style={{position: 'absolute', left: 40, top: 690, display: 'flex', alignItems: 'baseline', gap: 24, opacity: fade(f, d.scoreAt)}}>
        <Txt s={44} c={T.ink2}>{d.score[0]}</Txt><Txt s={110} c={T.accent}>{d.score[1]}</Txt>
      </div>
    </>
  );
};

const YearsS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div>
      <YearBars x={40} y={140} w={920} h={600} years={d.years} vals={d.vals} min={d.min} max={d.max} start={d.start} tags={d.tags} />
    </>
  );
};

const PersonaS: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows = toRows(d.rows);
  return (
    <>
      <div style={{position: 'absolute', left: -10, top: 10, transform: 'scale(0.8)', transformOrigin: '50% 0'}}><Person x={0} y={0} name={d.person[0]} desc={d.person[1]} at={0} color={COL[d.person[2]] ?? T.accent} /></div>
      <Stamp x={420} y={150} o={fade(f, 6, 8)} text={d.tag} color={T.ink3} size={30} rot={-6} />
      <TallyReceipt x={40} y={290} w={920} head={d.head} rows={rows} size={rows.length > 4 ? 34 : 40} active={activeRow(rows, f)} stamp={d.stamp ? {text: d.stamp[0], start: d.stamp[1]} : undefined} />
    </>
  );
};

const LineS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame();
  const X = 110, Y = 160, W = 720, H = 540;
  const series = d.series.map(([, col, pts]: [string, string, number[]]) => ({name: '', color: COL[col], pts, width: 7}));   // 끝 이름표는 끄고 위 범례로(두 선이 같은 점에서 끝나면 이름이 겹침)
  const n = d.series[0][2].length; const xy = lineXY(X, Y, W, H, d.min, d.max, n);
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div>
      {d.series.map(([name, col]: [string, string], i: number) => <div key={i} style={{position: 'absolute', left: 40 + i * 230, top: 84, opacity: fade(f, 0)}}><Txt s={32} c={COL[col]}>━ {name}</Txt></div>)}
      <TallyLineChart series={series} x={X} y={Y} w={W} h={H} min={d.min} max={d.max} start={d.draw} dur={d.dur ?? 50}
        ticks={d.ticks.map(([v, t]: [number, string]) => ({v, text: t}))} xlabels={d.xlabels.map(([i, t]: [number, string]) => ({i, text: t}))} />
      {d.tags.map((t: any, i: number) => { const [tx, ty] = xy(t[0], t[1]); return <TallyTag key={i} x={tx} y={ty} text={t[2]} start={t[3]} side={t[4]} hot={t[5]} size={30} />; })}
    </>
  );
};

// 세로 판용 표(parts/reverse Grid와 같은 뜻 — rows = [줄 이름, 칸 글자들, 나타날 프레임], hot = [줄, 칸, 프레임] 주황 테두리). 이름 칸을 좁히고 글자 길이에 맞춰 크기를 줄인다(칸 넘침 방지).
const GridV: React.FC<{cols: string[]; rows: [string, string[], number][]; hot?: [number, number, number][]; x: number; y: number; w: number}> = ({cols, rows, hot = [], x, y, w}) => {
  const f = useCurrentFrame();
  const lw = rows.some((r) => r[0].length > 7) ? 270 : 230; const cw = (w - lw) / cols.length; const rh = rows.length > 2 ? 130 : 160; const hh = 70;
  const cs = (c: string) => (c.length <= 5 ? 56 : c.length <= 7 ? 44 : 36);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w}}>
      {cols.map((c, i) => <div key={i} style={{position: 'absolute', left: lw + i * cw, width: cw, top: 0, height: hh, lineHeight: `${hh}px`, textAlign: 'center', ...F, fontWeight: 700, fontSize: 32, color: T.ink2, whiteSpace: 'nowrap'}}>{c}</div>)}
      <div style={{position: 'absolute', left: 0, right: 0, top: hh, borderTop: `3px solid ${T.ink}`}} />
      {rows.map(([name, cells, at], r) => {
        const o = fade(f, at, 12); const top = hh + 12 + r * rh;
        return (
          <div key={r} style={{position: 'absolute', left: 0, right: 0, top, height: rh - 14, opacity: o, transform: `translateY(${(1 - o) * 14}px)`}}>
            <div style={{position: 'absolute', left: 6, width: lw - 12, top: 0, height: rh - 14, display: 'flex', alignItems: 'center', ...F, fontWeight: 700, fontSize: name.length > 7 ? 30 : 36, color: T.ink, lineHeight: 1.15, wordBreak: 'keep-all'}}>{name}</div>
            {cells.map((c, i) => {
              const h = hot.find(([hr, hc]) => hr === r && hc === i); const on = h ? f >= h[2] : false;
              return <div key={i} style={{position: 'absolute', left: lw + i * cw + 8, width: cw - 16, top: 0, height: rh - 14, borderRadius: 14, background: on ? T.soft : T.bg,
                boxShadow: on ? `inset 0 0 0 4px ${T.accent}` : undefined, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                <span style={{...F, fontWeight: 700, fontSize: cs(c), color: on ? T.accent : T.ink, whiteSpace: 'nowrap', letterSpacing: -1}}>{c}</span></div>;
            })}
          </div>
        );
      })}
    </div>
  );
};

const GridS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      {d.head ? <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div> : null}
      <GridV cols={d.cols} rows={d.rows} hot={d.hot} x={40} y={100} w={920} />
      {d.note ? <TallyCallout x={40} y={100 + 82 + d.rows.length * (d.rows.length > 2 ? 130 : 160) + 30} text={d.note[0]} start={d.note[1]} w={920} size={38} /> : null}
    </>
  );
};

const ReceiptS: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows = toRows(d.rows);
  return (
    <>
      <TallyReceipt x={40} y={30} w={920} head={d.head} rows={rows} size={d.size ?? (rows.length > 5 ? 32 : 42)} active={activeRow(rows, f)} />
      <Big side={d.side} x={40} y={rows.length > 5 ? 620 : 520} />
    </>
  );
};

const TwinS: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame();
  return (
    <>
      {s.data.cards.map((c: any, i: number) => {
        const rows = toRows(c.rows); const st = c.rows[0][3];
        return f >= st ? <div key={i} style={{opacity: c.dim ? 0.5 : 1}}><TallyReceipt x={40} y={i === 0 ? 20 : 330} w={920} head={c.head} rows={rows} size={i === 0 ? 30 : 36} start={st} active={c.dim ? -1 : activeRow(rows, f)} /></div> : null;
      })}
    </>
  );
};

const ThreshS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div>
      <Ruler x={60} y={420} w={880} max={d.max} marks={d.marks} fill={d.fill} />
      {d.note ? <TallyCallout x={40} y={660} text={d.note[0]} start={d.note[1]} w={920} size={34} /> : null}
    </>
  );
};

const BarsS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: b[3], color: COL[b[4]] ?? T.ink2, sub: b[5] ?? undefined}));
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div>
      <TallyBars bars={bars} x={60} y={170} w={880} h={540} max={d.max} labelSize={30} valueSize={64} tags />
    </>
  );
};

const DuoS: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <>
      <div style={{position: 'absolute', left: 300, top: 30, width: 400, height: 130, borderRadius: 22, background: T.ink, opacity: fade(f, 0), display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <Txt s={60} c="#fff">{d.mid}</Txt>
      </div>
      <div style={{position: 'absolute', left: 0, top: 200, transform: 'scale(1.25)', transformOrigin: '0 0'}}>
        <Person x={-20} y={0} name={d.a[0]} desc={d.a[1]} at={d.a[2]} color={T.accent} />
        <Person x={380} y={0} name={d.b[0]} desc={d.b[1]} at={d.b[2]} color={T.fall} />
      </div>
      {d.tag ? [130, 630].map((x, i) => <Stamp key={i} x={x} y={740} o={fade(f, d.tag[1] + i * 4, 8)} text={d.tag[0]} color={T.ink3} size={24} rot={-6} />) : null}
    </>
  );
};

// 두 칸 대결(세로로 쌓음): tiles = [머리, 큰 값, 아래 글, 시작, 색]
const VsS: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame();
  return (
    <>
      {s.data.tiles.map(([head, big, sub, at, col]: any, i: number) => {
        const c = COL[col] ?? T.ink; const y = 40 + i * 400;
        if (f < at) return <div key={i} style={{position: 'absolute', left: 40, top: y, width: 920, height: 360, borderRadius: 22, border: `3px dashed ${T.line}`}} />;
        const sp = spring({frame: f - at, fps: 30, config: {damping: 13}});
        return (
          <div key={i} style={{position: 'absolute', left: 40, top: y + (1 - sp) * 30, width: 920, height: 360, background: T.bg, borderRadius: 22, opacity: sp, boxShadow: `inset 0 12px 0 ${c}`}}>
            <div style={{position: 'absolute', left: 44, top: 46}}><Txt s={48} c={T.ink2}>{head}</Txt></div>
            <div style={{position: 'absolute', left: 44, top: 120}}><Txt s={120} c={c}>{big}</Txt></div>
            <div style={{position: 'absolute', left: 44, top: 280}}><Txt s={36} c={T.ink3}>{sub}</Txt></div>
          </div>
        );
      })}
    </>
  );
};

const DivS: React.FC<{s: SScene}> = ({s}) => {
  const d = s.data;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.head}</Txt></div>
      <DivRows x0={d.x0 ?? 500} y={220} rowH={170} half={d.half ?? 250} max={d.max} rows={d.rows} labelW={180} />
      {d.q ? <TallyCallout x={40} y={620} text={d.q[0]} start={d.q[1]} w={920} size={40} /> : null}{/* 10/16 n1s_top10: q 없으면 생략(줄 4개면 y 620에서 겹침) */}
    </>
  );
};

const Body: React.FC<{s: SScene}> = ({s}) => {
  switch (s.kind) {
    case 'tilegrid': return <TileGrid s={s} />;
    case 'tank': return <TankS s={s} />;
    case 'years': return <YearsS s={s} />;
    case 'persona': return <PersonaS s={s} />;
    case 'line': return <LineS s={s} />;
    case 'grid': return <GridS s={s} />;
    case 'receipt': return <ReceiptS s={s} />;
    case 'twin': return <TwinS s={s} />;
    case 'thresh': return <ThreshS s={s} />;
    case 'bars': return <BarsS s={s} />;
    case 'duo': return <DuoS s={s} />;
    case 'vs': return <VsS s={s} />;
    case 'diverge': return <DivS s={s} />;
    default: return null;
  }
};

// ───────── 틀(M1S v2와 같은 규칙) ─────────
const chunks = (t: string) => {
  const out: string[] = [];
  for (const sen of t.split(/(?<=[.?!])\s+/).filter(Boolean)) {
    const w = sen.split(/\s+/).filter(Boolean); const n = w.length; const L = sen.length; const k = Math.max(1, Math.round(L / 13)); const tg = L / k;
    const len = (i: number, j: number) => w.slice(i, j).join(' ').length;
    const best: number[] = Array(n + 1).fill(Infinity); const prev: number[] = Array(n + 1).fill(0); best[0] = 0;
    for (let j = 1; j <= n; j++) for (let i = 0; i < j; i++) {
      const l = len(i, j); if (l > 16 && j - i > 1) continue;
      const c = best[i] + (l - tg) * (l - tg) + (l < 5 ? 60 : 0) + (j < n && /\d[억만천원]*$/.test(w[j - 1]) && /^\d/.test(w[j]) ? 400 : 0) + (j < n && w[j - 1].length === 1 ? 200 : 0); if (c < best[j]) { best[j] = c; prev[j] = i; }
    }
    const cut: string[] = []; for (let j = n; j > 0; j = prev[j]) cut.unshift(w.slice(prev[j], j).join(' '));
    out.push(...cut);
  }
  return out.map((c) => c.replace(/[.,]$/, ''));
};
const NUMRX = /(\d[\d,.]*\s?(?:천만원|만원|억|원|%|배|번|년째|년|월)?)/;
const Hi: React.FC<{t: string}> = ({t}) => <>{t.split(NUMRX).map((x, i) => (i % 2 ? <span key={i} style={{color: '#FFD000'}}>{x}</span> : <React.Fragment key={i}>{x}</React.Fragment>))}</>;
const Caption: React.FC<{s: SScene; first: boolean}> = ({s, first}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  let k = 0; st.forEach((a, i) => { if (f >= a) k = i; });
  const l = s.lines[k]; const cs = chunks(l.text); const tot = cs.reduce((a, x) => a + x.replace(/\s/g, '').length, 0);
  const speak = l.frames - 8; let acc = 0, j = 0, from = st[k];
  for (let i = 0; i < cs.length; i++) { const a = st[k] + (acc / tot) * speak; if (f >= a) { j = i; from = a; } acc += cs[i].replace(/\s/g, '').length; }
  const o = first && k === 0 && j === 0 ? 1 : interpolate(f, [from, from + 3], [0, 1], CL);
  return (
    <div style={{height: CAP_H, boxSizing: 'border-box', background: T.ink, padding: '6px 20px', borderRadius: 20, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{...F, fontWeight: 700, fontSize: capSize(cs[j]), lineHeight: 1.2, color: '#fff', textAlign: 'center', whiteSpace: 'nowrap', letterSpacing: -1, opacity: 0.5 + 0.5 * o, transform: `scale(${0.97 + 0.03 * o})`}}><Hi t={cs[j]} /></div>
    </div>
  );
};
// 10/16 안전 영역 틀(parts/safeframe): 판은 위 띠 끝 ~ 자막 위, 안전 영역 가운데에 줄여 둔다. 글자는 전부 x 48~888 · y 288~1248.
const Frame: React.FC<{s: SScene; from: number; total: number; first: boolean; p: C1SProps}> = ({s, from, total, first, p}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  // 장면 안 컷: 약 2.5초(75프레임)마다 판을 4.5% 당겼다 놓는다(내용은 그대로, 자막 조각 바뀜과 함께 화면이 2~3초마다 달라지게 — today.md 12:3x '장면 약 2초마다')
  const k = Math.floor(f / 75); const pin = (k % 2) * interpolate(f - k * 75, [0, 6], [0, 1], CL) + (1 - (k % 2)) * (k ? interpolate(f - k * 75, [0, 6], [1, 0], CL) : 0);
  const drift = interpolate(f, [0, s.frames], [1, 1.025], CL) + 0.045 * pin;
  const body = s.data.full ? <Sequence from={-90} layout="none"><Body s={s} /></Sequence> : <Body s={s} />;
  const b = boardBox(p.question, p.answer as Answer, BW, BH);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 0, top: b.top, width: 1080, height: b.bottom - b.top, background: '#fff'}} />
      <div style={{position: 'absolute', left: b.left, top: b.y, width: b.w, height: b.h, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: BW, height: BH, transform: `scale(${b.s})`, transformOrigin: '0 0'}}><div style={{position: 'absolute', left: 0, top: 0, width: BW, height: BH, transform: `scale(${drift})`, transformOrigin: '50% 42%'}}>{body}</div></div>
      </div>
      <div style={{position: 'absolute', left: SZ.x0 + 6, top: capTop(p.answer as Answer), width: SZ.x1 - SZ.x0 - 12}}><Caption s={s} first={first} /></div>
      <BottomShade progress={(from + f) / total} />
      {s.lines.map((l, i) => <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
    </AbsoluteFill>
  );
};

export const C1S: React.FC<C1SProps> = (p) => {
  const total = c1sFrames(p); let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      <TopBand question={p.question} hot={p.hot} base={p.base} />
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><Frame s={s} from={from} total={total} first={i === 0} p={p} /></Sequence>; from += s.frames; return el; })}
      <AnswerCard answer={p.answer as Answer} />
    </AbsoluteFill>
  );
};
