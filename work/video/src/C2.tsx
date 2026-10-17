// C-2 v3.3 "퇴직금 3억, 매달 200만원 팔아 쓰면 평생 가나" 화면 — 재료 work/video/c2.json(ep/C-2/c2props.py가 script.md·voice.json·calc 두 개로 만듦)
// 10/17 롱폼 화면 기준(visual-gap-1017 7절, 관문 work/bgcheck.py): 판(TallyFrame, 큰 제목·아이콘·큰 숫자 하나) ↔ 꽉 찬 실사(TallyBroll) ↔ 정우 씨 그림(visual/N1-person)을 번갈아.
// 판은 글자 줄 8개 이하(제목·큰 값·작은 줄·출처·자막), 같은 판 20초 이하는 c2props가 잰다. 말 줄이 7초를 넘으면 줄 가운데에서 강조 칸이 한 번 바뀐다(lfrender '같은 화면 8초').
// 숫자 글자는 전부 c2.json에서 온다(c2props.py가 calc·대본과 기계 대조). 옛 v2 화면은 ep/C-2/C2.v2.tsx.bak.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from './parts/fm';
import {TallyFrame, TallyCaption, TallyLine, TallyArt, SAFE} from './motion/TallyFrame';
import {TallyBroll} from './motion/TallyBroll';
import {TallyBars} from './motion/TallyBars';

type CLine = {text: string; audio: string; frames: number; cap?: string | null};
type CScene = {kind: string; lines: CLine[]; frames: number; data: any};
export type C2Props = {fps: number; scenes: CScene[]; boxOn: number; boxFlip: number; boxQ: string; boxA: string; boxLabel: string; badge: string};
export const c2Frames = (p: C2Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {accent: T.accent, fall: T.fall, rise: T.rise, ink: T.ink};
const col = (c?: string) => COL[c || 'ink'] || T.ink;
const out = Easing.out(Easing.cubic);
const ease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
const starts = (ls: CLine[]) => { const o: number[] = []; let a = 0; for (const l of ls) { o.push(a); a += l.frames; } return o; };
const lineAt = (ls: CLine[], f: number) => { const st = starts(ls); let k = 0; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };
// 줄 안 박자: 7초 넘는 줄은 가운데에서 한 번 더 바뀐다 → 장면 안 박자 번호(0,1,2…)
const beatAt = (ls: CLine[], f: number) => { const st = starts(ls); let b = 0; ls.forEach((l, i) => { if (f >= st[i] && i > 0) b++; if (l.frames > 210 && f >= st[i] + l.frames / 2) b++; }); return b; };
const tl = (ls: CLine[]): TallyLine[] => ls.map(l => ({text: l.text.replace(/^"|"$/g, ''), frames: l.frames, cap: l.cap ?? null}));
const bigSize = (t: string, room: number, max: number) => { const u = [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.3 : 0.6), 0); return Math.max(84, Math.min(max, Math.floor(room / Math.max(1, u)))); };
const art = (icon?: string, color?: string): TallyArt | null => icon ? {kind: 'icon', icon, license: 'lucide ISC', color} : null;

// 강조 칸: 박자가 홀수면 큰 값 뒤에 연주황 띠가 깔린다(화면 그래픽 영역 4% 넘게 바뀜)
const Pulse: React.FC<{s: CScene; x: number; y: number; w: number; h: number}> = ({s, x, y, w, h}) => {
  const f = useCurrentFrame(); const b = beatAt(s.lines, f);
  return b % 2 === 1 ? <div style={{position: 'absolute', left: x, top: y, width: w, height: h, background: T.soft, borderRadius: 28}} /> : null;
};

// ───────── 판 ─────────
const Big: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 4, 16); const z = bigSize(d.v, 1600, 210);
  return (
    <TallyFrame title={d.title} art={art(d.icon, d.c ? col(d.c) : undefined)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <Pulse s={s} x={160} y={300} w={1600} h={z * 1.25} />
      <div style={{position: 'absolute', left: 100, width: 1720, top: 300 + (210 - z) * 0.5, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `scale(${0.94 + 0.06 * o})`}}>
        <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.18, color: col(d.c), letterSpacing: -4, whiteSpace: 'nowrap'}}>{d.v}</div>
        {d.s ? <div style={{...F, fontWeight: 700, fontSize: 46, color: T.ink2, marginTop: 22, whiteSpace: 'nowrap'}}>{d.s}</div> : null}
      </div>
    </TallyFrame>
  );
};

const Pair: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines);
  const at2 = d.at2 != null ? st[Math.min(d.at2, st.length - 1)] : (s.lines.length > 1 ? st[1] : Math.round(s.lines[0].frames * 0.45));
  const one = (v: string, sub: string, c: string, a: number, x: number) => { const o = ease(f, a, 14); const z = bigSize(v, 760, 170);
    return <div style={{position: 'absolute', left: x, width: 800, top: 330, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 20}px)`}}>
      <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.15, color: col(c), letterSpacing: -4, whiteSpace: 'nowrap'}}>{v}</div>
      <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink2, marginTop: 18, whiteSpace: 'nowrap'}}>{sub}</div></div>; };
  const lit = f >= at2 + 12;
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      {lit ? <div style={{position: 'absolute', left: 1000, top: 290, width: 760, height: 330, background: T.soft, borderRadius: 28}} /> : null}
      {one(d.v1, d.s1, d.c1, 4, 160)}
      <div style={{position: 'absolute', left: 940, top: 360, width: 40, height: 220, borderLeft: `3px solid ${T.line}`}} />
      {one(d.v2, d.s2, d.c2, at2, 960)}
    </TallyFrame>
  );
};

const Rows: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines); const rows: [string, string?, string?, number?][] = d.rows;
  const n = rows.length; const fs = n >= 4 ? 52 : 60; const rh = n >= 4 ? 112 : 136;
  const show = (i: number) => { const at = rows[i][3]; if (at == null) return 4 + i * 8; return at >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[at]; };
  const k = (() => { let j = 0; rows.forEach((_, i) => { if (f >= show(i)) j = i; }); return j; })();
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 200, width: 1520, top: 300 + (4 - Math.min(4, n)) * 30}}>
        {rows.map((r, i) => { const o = ease(f, show(i), 12); const hot = d.hot !== false && i === k && n > 1;
          return <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: rh, padding: '0 36px', marginBottom: 10, borderRadius: 18,
            background: hot ? T.soft : '#fff', border: `2px solid ${hot ? T.soft : T.line}`, opacity: o, transform: `translateX(${(1 - o) * -30}px)`}}>
            <span style={{...F, fontWeight: 700, fontSize: fs, color: T.ink, whiteSpace: 'nowrap'}}>{r[0]}</span>
            {r[1] ? <span style={{...F, fontWeight: 800, fontSize: fs + 6, color: col(r[2]), whiteSpace: 'nowrap', marginLeft: 40}}>{r[1]}</span> : null}
          </div>; })}
      </div>
    </TallyFrame>
  );
};

const Bars: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const st = starts(s.lines);
  const at = (a?: number) => a == null ? 6 : a >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[a] + 4;
  const bars = (d.bars as [string, number, string, string, number?][]).map(([label, value, valueText, c, a]) => ({label, value: Math.abs(value), valueText, color: col(c), start: at(a)}));
  const v = d.dir === 'v';
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <Pulse s={s} x={v ? 180 : 140} y={v ? 270 : 280} w={v ? 1560 : 1640} h={v ? 560 : 540} />
      <TallyBars bars={bars} x={v ? 300 : 420} y={v ? 330 : 310} w={v ? 1320 : 1180} h={v ? 420 : 480} max={d.max} min={0} dir={v ? 'v' : 'h'} labelSize={v ? 44 : 46} valueSize={v ? 60 : 62} />
    </TallyFrame>
  );
};

const Grid: React.FC<{s: CScene}> = ({s}) => {   // 바닥난 6명: 3×2 칸
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines); const cells: [string, string, number][] = d.cells;
  const k = lineAt(s.lines, f);
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 200, top: 300, width: 1520, display: 'flex', flexWrap: 'wrap', gap: 28}}>
        {cells.map(([a, b, ln], i) => { const o = ease(f, (st[ln] ?? 0) + 4 + (i % 5) * 6, 12); const lit = (d.lit as number[][])[k]?.includes(i);
          return <div key={i} style={{width: 488, height: 220, borderRadius: 22, background: lit ? T.soft : '#fff', border: `2px solid ${lit ? T.accent : T.line}`, opacity: o,
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{...F, fontWeight: 800, fontSize: 92, color: T.ink, lineHeight: 1.1}}>{a}</div>
            <div style={{...F, fontWeight: 700, fontSize: 42, color: T.accent, marginTop: 6}}>{b}</div></div>; })}
      </div>
    </TallyFrame>
  );
};

const Ask: React.FC<{s: CScene}> = ({s}) => {   // 질문 카드
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 2, 14); const z = bigSize(d.q, 1560, 112);
  return (
    <AbsoluteFill style={{background: T.ink}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff'}}>파이어맵</span></div>
      <div style={{position: 'absolute', left: 180, width: 1560, top: 250, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 24}px)`}}>
        <div style={{...F, fontWeight: 700, fontSize: 52, color: '#fff', background: T.accent, borderRadius: 14, padding: '6px 26px'}}>{d.n}</div>
        <div style={{...F, fontWeight: 800, fontSize: z, color: '#fff', marginTop: 40, lineHeight: 1.2, letterSpacing: -2, textAlign: 'center', wordBreak: 'keep-all', maxWidth: 1560}}>{d.q}</div>
        {d.from ? <div style={{...F, fontWeight: 600, fontSize: 32, color: T.dink3, marginTop: 40, textAlign: 'center', maxWidth: 1400, wordBreak: 'keep-all'}}>{d.from}</div> : null}
      </div>
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

const List5: React.FC<{s: CScene}> = ({s}) => {   // 질문 다섯 줄
  const f = useCurrentFrame(); const d = s.data;
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 260, top: 268, width: 1400}}>
        {(d.items as string[]).map((t, i) => { const o = ease(f, 6 + i * 14, 12);
          return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, height: 104, opacity: o, transform: `translateX(${(1 - o) * -24}px)`}}>
            <div style={{...F, fontWeight: 800, fontSize: 50, color: '#fff', background: T.accent, width: 74, height: 74, borderRadius: 37, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
            <div style={{...F, fontWeight: 700, fontSize: 54, color: T.ink, whiteSpace: 'nowrap'}}>{t}</div></div>; })}
      </div>
    </TallyFrame>
  );
};

// ───────── 그림 장면(정우 씨·영호 씨·민수 씨) ─────────
const Pic: React.FC<{s: CScene; badge: string}> = ({s, badge}) => {
  const f = useCurrentFrame(); const d = s.data; const z = interpolate(f, [0, s.frames], d.zoom || [1.0, 1.1], CL);
  const st = starts(s.lines); const ca = d.chipAt != null ? st[Math.min(d.chipAt, st.length - 1)] : 10; const co = ease(f, ca, 14);
  const q = d.quote ? ease(f, 6, 12) : 0;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <style>{FONT_CSS}</style>
      <AbsoluteFill style={{transform: `scale(${z}) translateX(${interpolate(f, [0, s.frames], [0, d.pan || 0], CL)}px)`, transformOrigin: `${d.cx ?? 50}% ${d.cy ?? 40}%`, filter: d.gray ? 'grayscale(0.85)' : undefined}}>
        <Img src={staticFile(d.pic)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(10,11,14,0.55) 0%, rgba(10,11,14,0) 30%)'}} />
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', textShadow: '0 1px 8px rgba(0,0,0,0.6)'}}>파이어맵</span>
        <div style={{...F, fontWeight: 700, fontSize: 22, color: T.ink, background: 'rgba(255,255,255,0.9)', borderRadius: 8, padding: '1px 10px', marginLeft: 8}}>{badge}</div></div>
      {d.year ? <div style={{position: 'absolute', left: SAFE.left, top: 70, ...F, fontWeight: 800, fontSize: 104, lineHeight: 1.1, color: '#fff', background: 'rgba(16,17,20,0.82)', borderRadius: 20, padding: '4px 30px'}}>{d.year}</div> : null}
      {d.chip ? <div style={{position: 'absolute', ...(d.chipPos === 'left' ? {left: SAFE.left, top: d.year ? 230 : 90} : {right: 100, top: 250}), opacity: co, transform: `translateY(${(1 - co) * 20}px)`, background: 'rgba(255,255,255,0.95)', borderRadius: 24, padding: '20px 40px', maxWidth: 1000}}>
        <div style={{...F, fontWeight: 800, fontSize: bigSize(d.chip[0], 900, 120), color: col(d.chipC || 'accent'), lineHeight: 1.1, whiteSpace: 'nowrap'}}>{d.chip[0]}</div>
        {d.chip[1] ? <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, marginTop: 8, whiteSpace: 'nowrap'}}>{d.chip[1]}</div> : null}</div> : null}
      {d.quote ? <div style={{position: 'absolute', left: SAFE.left, top: 600, opacity: q, transform: `scale(${0.9 + 0.1 * q})`, transformOrigin: 'left center',
        ...F, fontWeight: 800, fontSize: bigSize(d.quote, 1150, 104), color: T.ink, background: '#fff', borderRadius: 30, padding: '22px 44px', whiteSpace: 'nowrap', boxShadow: '0 12px 40px rgba(0,0,0,0.35)'}}>“{d.quote}”</div> : null}
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

const KIND: Record<string, React.FC<{s: CScene}>> = {big: Big, pair: Pair, rows: Rows, bars: Bars, grid: Grid, ask: Ask, list5: List5};

// ───────── 고정 칸: 바닥나는 해 ─────────
const FloorBox: React.FC<{p: C2Props}> = ({p}) => {
  const f = useCurrentFrame(); if (f < p.boxOn) return null;
  const o = ease(f, p.boxOn, 12); const flip = f >= p.boxFlip;
  return (
    <div style={{position: 'absolute', right: 56, top: 14, padding: '4px 18px', borderRadius: 12, background: flip ? T.accent : 'rgba(24,25,29,0.88)', opacity: o, display: 'flex', alignItems: 'baseline', gap: 12}}>
      <span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', whiteSpace: 'nowrap'}}>{p.boxLabel}</span>
      <span style={{...F, fontWeight: 700, fontSize: 32, color: flip ? '#fff' : '#FFD000', whiteSpace: 'nowrap'}}>{flip ? p.boxA : p.boxQ}</span>
    </div>
  );
};

export const C2: React.FC<C2Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => {
        const st = starts(s.lines); const K = KIND[s.kind];
        const el = <Sequence key={i} from={from} durationInFrames={s.frames}>
          {s.kind === 'pic' ? <Pic s={s} badge={p.badge} /> : s.kind === 'broll' ? <TallyBroll src={s.data.src} license={s.data.license} from={s.data.from} say={s.data.say} side={s.data.side} x={s.data.x} chapter={s.data.chapter} lines={tl(s.lines)} /> : K ? <K s={s} /> : null}
          {s.lines.map((l, j) => <Sequence key={j} from={st[j]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
        </Sequence>;
        from += s.frames; return el;
      })}
      <FloorBox p={p} />
    </AbsoluteFill>
  );
};
