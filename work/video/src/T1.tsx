// T-1 v4.1 "1주택 양도세 12억 초과·장기보유특별공제 정부안" 화면 — 재료 work/video/t1.json(ep/T-1/t1props.py가 script.md·voice.json·calc 두 개로 만듦)
// 10/17 롱폼 화면 기준(visual-gap-1017 7절, 관문 work/bgcheck.py): C2.tsx 틀을 따라 판(TallyFrame, 큰 제목·아이콘·큰 숫자 하나) ↔ 꽉 찬 실사(TallyBroll) ↔ 질문 카드를 번갈아.
// 판은 글자 줄 8개 이하(제목·큰 값·작은 줄·출처·자막), 같은 판 20초 이하는 t1props가 잰다. 말 줄이 7초를 넘으면 줄 가운데에서 강조 칸이 한 번 바뀐다(lfrender '같은 화면 8초').
// 숫자 글자는 전부 t1.json에서 온다(t1props.py가 calc·대본과 기계 대조). T-1 전용 판 9종은 parts/t1kit.tsx. 옛 v3 화면은 ep/T-1/T1.v3.tsx.bak.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from './parts/fm';
import {TallyFrame, TallyCaption, TallyLine, TallyArt, SAFE} from './motion/TallyFrame';
import {TallyBroll} from './motion/TallyBroll';
import {TallyBars} from './motion/TallyBars';
import {KTable, KCells, KPrice, KCal, KZones, KMemo, KStairs, KBand, KFive} from './parts/t1kit';

type CLine = {text: string; audio: string; frames: number; cap?: string | null};
type CScene = {kind: string; lines: CLine[]; frames: number; data: any};
export type T1Props = {fps: number; scenes: CScene[]; badge: string};
export const t1Frames = (p: T1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {accent: T.accent, fall: T.fall, rise: T.rise, ink: T.ink};
const col = (c?: string) => COL[c || 'ink'] || T.ink;
const out = Easing.out(Easing.cubic);
const ease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
const starts = (ls: CLine[]) => { const o: number[] = []; let a = 0; for (const l of ls) { o.push(a); a += l.frames; } return o; };
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
      <Pulse s={s} x={160} y={340} w={1600} h={z * 1.25} />
      <div style={{position: 'absolute', left: 100, width: 1720, top: 340 + (210 - z) * 0.5, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `scale(${0.94 + 0.06 * o})`}}>
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
    return <div style={{position: 'absolute', left: x, width: 800, top: 360, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 20}px)`}}>
      <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.15, color: col(c), letterSpacing: -4, whiteSpace: 'nowrap'}}>{v}</div>
      <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink2, marginTop: 18, whiteSpace: 'nowrap'}}>{sub}</div></div>; };
  // 오른쪽 값이 첫 줄부터 나오는 판(at2=0)은 줄(박자)마다 강조 칸이 켜졌다 꺼진다 — 줄마다 화면이 바뀌게
  const lit = f >= at2 + 12 && (d.at2 === 0 ? beatAt(s.lines, f) % 2 === 0 : true);
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      {lit ? <div style={{position: 'absolute', left: 1000, top: 320, width: 760, height: 330, background: T.soft, borderRadius: 28}} /> : null}
      {one(d.v1, d.s1, d.c1, 4, 160)}
      <div style={{position: 'absolute', left: 940, top: 370, width: 40, height: 220, borderLeft: `3px solid ${T.line}`}} />
      {one(d.v2, d.s2, d.c2, at2, 960)}
    </TallyFrame>
  );
};

const Rows: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines); const rows: [string, string?, string?, number?][] = d.rows;
  const n = rows.length; const fs = n >= 4 ? 52 : 60; const rh = n >= 4 ? 108 : 136;
  const show = (i: number) => { const at = rows[i][3]; if (at == null) return 4 + i * 8; return at >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[at]; };
  const k = (() => { let j = 0; rows.forEach((_, i) => { if (f >= show(i)) j = i; }); return j; })();
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 200, width: 1520, top: 350 + (4 - Math.min(4, n)) * 30}}>
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
      <Pulse s={s} x={v ? 180 : 140} y={v ? 280 : 290} w={v ? 1560 : 1640} h={v ? 550 : 530} />
      <TallyBars bars={bars} x={v ? 300 : 460} y={v ? 360 : 355} w={v ? 1320 : 920} h={v ? 390 : 440} max={d.max} min={0} dir={v ? 'v' : 'h'} labelSize={44} valueSize={v ? 58 : 60} />
    </TallyFrame>
  );
};

const Ask: React.FC<{s: CScene}> = ({s}) => {   // 질문 카드 — 실제 질문(지식iN·유튜브 댓글)을 우리 글씨로, 출처 줄
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 2, 14); const z = bigSize(d.q, 1560 * 2, 104);
  return (
    <AbsoluteFill style={{background: T.ink}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff'}}>파이어맵</span></div>
      <div style={{position: 'absolute', left: 180, width: 1560, top: 230, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 24}px)`}}>
        <div style={{...F, fontWeight: 700, fontSize: 52, color: '#fff', background: T.accent, borderRadius: 14, padding: '6px 26px'}}>{d.n}</div>
        <div style={{...F, fontWeight: 800, fontSize: z, color: '#fff', marginTop: 40, lineHeight: 1.2, letterSpacing: -2, textAlign: 'center', wordBreak: 'keep-all', maxWidth: 1560}}>“{d.q}”</div>
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
      <div style={{position: 'absolute', left: 300, top: 290, width: 1400}}>
        {(d.items as string[]).map((t, i) => { const o = ease(f, 6 + i * 14, 12);
          return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, height: 106, opacity: o, transform: `translateX(${(1 - o) * -24}px)`}}>
            <div style={{...F, fontWeight: 800, fontSize: 50, color: '#fff', background: i === 2 ? T.rise : T.accent, width: 74, height: 74, borderRadius: 37, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
            <div style={{...F, fontWeight: 700, fontSize: 56, color: T.ink, whiteSpace: 'nowrap'}}>{t}</div></div>; })}
      </div>
    </TallyFrame>
  );
};

const KIND: Record<string, React.FC<{s: CScene}>> = {big: Big, pair: Pair, rows: Rows, bars: Bars, ask: Ask, list5: List5,
  table: KTable, cells: KCells, price: KPrice, cal: KCal, zones: KZones, memo: KMemo, stairs: KStairs, band: KBand, five: KFive};

// 글꼴(PD)을 다 받은 뒤 그린다 — 10/17 C-2 미리보기에서 숫자가 대체 글꼴로 찍힌 프레임이 섞였다(@font-face만으로는 렌더가 기다리지 않음)
const useFont = () => {
  const [h] = React.useState(() => delayRender('PD 글꼴'));
  React.useEffect(() => {
    Promise.all([['700', 'fonts/pd700.ttf'], ['500', 'fonts/pd500.ttf']].map(([w, u]) => new FontFace('PD', `url(${staticFile(u)})`, {weight: w}).load()))
      .then((fs) => { fs.forEach((x) => document.fonts.add(x)); continueRender(h); }).catch((e) => { console.error(e); continueRender(h); });
  }, [h]);
};

// 가상 인물 표시: 정민 씨·수현 씨가 나오는 판 오른쪽 위 작은 칩 — 10/17 스틸 실측 판 글자 줄 중앙 8.0(기준 8 끝)이라 판에서는 끔(0장 '가상 인물' 말·끝 질문 카드·설명란에 있음). 다시 켤 땐 <Badge> 한 줄
const Badge: React.FC<{s: CScene; badge: string}> = ({s, badge}) => {
  const txt = JSON.stringify(s.data) + s.lines.map(l => l.cap || '').join('');
  if (!/정민 씨|수현 씨/.test(txt) || s.kind === 'broll' || s.kind === 'ask') return null;
  return <div style={{position: 'absolute', right: 56, top: 14, padding: '2px 14px', borderRadius: 10, background: 'rgba(24,25,29,0.88)', ...F, fontWeight: 700, fontSize: 22, color: '#fff', whiteSpace: 'nowrap'}}>{badge}</div>;
};

export const T1: React.FC<T1Props> = (p) => {
  useFont();
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => {
        const st = starts(s.lines); const K = KIND[s.kind];
        const el = <Sequence key={i} from={from} durationInFrames={s.frames}>
          {s.kind === 'broll' ? <TallyBroll src={s.data.src} license={s.data.license} from={s.data.from} say={s.data.say} side={s.data.side} x={s.data.x} chapter={s.data.chapter} lines={tl(s.lines)} /> : K ? <K s={s} /> : null}
          {s.lines.map((l, j) => <Sequence key={j} from={st[j]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
        </Sequence>;
        from += s.frames; return el;
      })}
    </AbsoluteFill>
  );
};
