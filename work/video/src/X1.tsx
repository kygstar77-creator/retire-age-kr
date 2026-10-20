// X-1 v3 "환율 1,554원 → 1,339원, 사람들이 물은 다섯 질문" 화면 — 재료 work/video/x1.json(ep/X-1/x1props.py가 script.md·voice.json·calc_out·raw로 만듦)
// 10/17 롱폼 화면 기준(visual-gap-1017 7절, 관문 work/bgcheck.py) · C2.tsx 틀: 판(TallyFrame, 큰 제목·아이콘·큰 숫자) ↔ 꽉 찬 실사(TallyBroll) ↔ 질문 카드(어두운 판)를 번갈아.
// 판은 글자 줄 8개 이하, 같은 판 20초 이하는 x1props가 잰다(판이 이어지면 사이에 실사·질문 카드).
// motion 부품: FxDates(질문 1 날짜 넷 선·막대) · EvenLadder(본전 환율) · HedgeFlip(환노출 vs (H)) · DaysBelow(지금보다 쌌던 날) — 한 부품 장면이 20초를 넘으면
//   x1props가 줄 단위로 나눠 사이에 실사를 끼운다(kind 'mo': 부품은 전체 줄 시간표 그대로 돌고, 나눈 조각은 그 시간표의 off 프레임부터 보여 준다 → beats = tallyStarts(전체 줄)).
// 새 부품(parts/fx.tsx): TwoLines(여는 두 선) · DcaCal12(12칸 달력) · CardSlips(카드 결제·취소 전표 두 장, 우리가 그림) · EqSteps(곱셈 식).
// 숫자 글자는 전부 x1.json에서 온다(x1props.py가 calc_out·대본과 기계 대조). 옛 v2 화면은 ep/X-1/X1.v2.tsx.bak.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from './parts/fm';
import {TallyFrame, TallyCaption, TallyLine, TallyArt, SAFE, tallyStarts} from './motion/TallyFrame';
import {TallyBroll} from './motion/TallyBroll';
import {TallyBars} from './motion/TallyBars';
import {TallyLineChart, lineXY} from './motion/TallyLineChart';
import {TallyTag} from './motion/TallyMark';
import {FxDates} from './motion/FxDates';
import {HedgeFlip} from './motion/HedgeFlip';
import {EvenLadder} from './motion/EvenLadder';
import {DaysBelow} from './motion/DaysBelow';
import {TwoLines, DcaCal12, CardSlips, EqSteps} from './parts/fx';

type CLine = {text: string; audio: string; frames: number; cap?: string | null};
type CScene = {kind: string; lines: CLine[]; frames: number; data: any};
type MoScene = {title: string; source: string; chapter?: string | null; lines: CLine[]; frames: number; data: any};
export type X1Props = {fps: number; scenes: CScene[]; fx: any; motion: Record<string, MoScene>};
export const x1Frames = (p: X1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

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
// 10/20 PD: 그래프 판은 아래 날짜·이름 글자가 830 줄까지 내려와 [정확한 값] 띠와 겹쳤다(lfrender overlap 93건) — 띠를 제목 아래로
const CAPUP = ['fxline', 'fxbars', 'line', 'mo']; const CAPTOP = 232;
const Frame: React.FC<{s: CScene; children?: React.ReactNode}> = ({s, children}) => {
  const d = s.data; return <TallyFrame title={d.title} art={art(d.icon, d.c ? col(d.c) : undefined)} source={d.source} chapter={d.chapter} lines={tl(s.lines)} capTop={CAPUP.includes(s.kind) ? CAPTOP : undefined}>{children}</TallyFrame>;
};

// 강조 칸: 박자가 홀수면 큰 값 뒤에 연주황 띠가 깔린다(화면 그래픽 영역 4% 넘게 바뀜)
const Pulse: React.FC<{s: CScene; x: number; y: number; w: number; h: number}> = ({s, x, y, w, h}) => {
  const f = useCurrentFrame(); const b = beatAt(s.lines, f);
  return b % 2 === 1 ? <div style={{position: 'absolute', left: x, top: y, width: w, height: h, background: T.soft, borderRadius: 28}} /> : null;
};

// ───────── 판(C2 틀) ─────────
const Big: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 4, 16); const z = bigSize(d.v, 1600, 200);
  return (
    <Frame s={s}>
      <Pulse s={s} x={160} y={340} w={1600} h={z * 1.25} />
      <div style={{position: 'absolute', left: 100, width: 1720, top: 340 + (200 - z) * 0.5, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `scale(${0.94 + 0.06 * o})`}}>
        <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.18, color: col(d.c), letterSpacing: -4, whiteSpace: 'nowrap'}}>{d.v}</div>
        {d.s ? <div style={{...F, fontWeight: 700, fontSize: 46, color: T.ink2, marginTop: 22, whiteSpace: 'nowrap'}}>{d.s}</div> : null}
      </div>
    </Frame>
  );
};

const Pair: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines);
  const at2 = d.at2 != null ? st[Math.min(d.at2, st.length - 1)] : (s.lines.length > 1 ? st[1] : Math.round(s.lines[0].frames * 0.45));
  const one = (v: string, sub: string, c: string, a: number, x: number) => { const o = ease(f, a, 14); const z = bigSize(v, 760, 160);
    return <div style={{position: 'absolute', left: x, width: 800, top: 360, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 20}px)`}}>
      <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.15, color: col(c), letterSpacing: -4, whiteSpace: 'nowrap'}}>{v}</div>
      <div style={{...F, fontWeight: 700, fontSize: 42, color: T.ink2, marginTop: 18, whiteSpace: 'nowrap'}}>{sub}</div></div>; };
  const lit = f >= at2 + 12;
  return (
    <Frame s={s}>
      {lit ? <div style={{position: 'absolute', left: 1000, top: 320, width: 760, height: 330, background: T.soft, borderRadius: 28}} /> : null}
      {one(d.v1, d.s1, d.c1, 4, 160)}
      <div style={{position: 'absolute', left: 940, top: 370, width: 40, height: 220, borderLeft: `3px solid ${T.line}`}} />
      {one(d.v2, d.s2, d.c2, at2, 960)}
    </Frame>
  );
};

const Rows: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines); const rows: [string, string?, string?, number?][] = d.rows;
  const n = rows.length; const fs = n >= 4 ? 50 : 58; const rh = n >= 4 ? 106 : 130;
  const show = (i: number) => { const at = rows[i][3]; if (at == null) return 4 + i * 8; return at >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[at]; };
  const k = (() => { let j = 0; rows.forEach((_, i) => { if (f >= show(i)) j = i; }); return j; })();
  return (
    <Frame s={s}>
      <div style={{position: 'absolute', left: 200, width: 1520, top: 350 + (4 - Math.min(4, n)) * 30}}>
        {rows.map((r, i) => { const o = ease(f, show(i), 12); const hot = d.hot !== false && i === k && n > 1;
          return <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: rh, padding: '0 36px', marginBottom: 10, borderRadius: 18,
            background: hot ? T.soft : '#fff', border: `2px solid ${hot ? T.soft : T.line}`, opacity: o, transform: `translateX(${(1 - o) * -30}px)`}}>
            <span style={{...F, fontWeight: 700, fontSize: fs, color: T.ink, whiteSpace: 'nowrap'}}>{r[0]}</span>
            {r[1] ? <span style={{...F, fontWeight: 800, fontSize: fs + 6, color: col(r[2]), whiteSpace: 'nowrap', marginLeft: 40}}>{r[1]}</span> : null}
          </div>; })}
      </div>
    </Frame>
  );
};

const Bars: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const st = starts(s.lines);
  const at = (a?: number) => a == null ? 6 : a >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[a] + 4;
  const bars = (d.bars as [string, number, string, string, number?][]).map(([label, value, valueText, c, a]) => ({label, value: Math.abs(value), valueText, color: col(c), start: at(a)}));
  const v = d.dir === 'v';
  return (
    <Frame s={s}>
      <Pulse s={s} x={v ? 180 : 140} y={300} w={v ? 1560 : 1640} h={v ? 530 : 520} />
      <TallyBars bars={bars} x={v ? 300 : 520} y={v ? 370 : 360} w={v ? 1320 : 1100} h={v ? 380 : 430} max={d.max} min={0} dir={v ? 'v' : 'h'} labelSize={v ? 40 : 44} valueSize={v ? 56 : 58} />
    </Frame>
  );
};

const Ask: React.FC<{s: CScene}> = ({s}) => {   // 질문 카드(어두운 판 — 화면 전체 컷)
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 2, 14); const z = bigSize(d.q, 1560, 112);
  return (
    <AbsoluteFill style={{background: T.ink}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff'}}>파이어맵</span></div>
      <div style={{position: 'absolute', left: 180, width: 1560, top: 230, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 24}px)`}}>
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
    <Frame s={s}>
      <div style={{position: 'absolute', left: 230, top: 290, width: 1460}}>
        {(d.items as string[]).map((t, i) => { const o = ease(f, 6 + i * 12, 12);
          return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, height: 104, opacity: o, transform: `translateX(${(1 - o) * -24}px)`}}>
            <div style={{...F, fontWeight: 800, fontSize: 48, color: '#fff', background: T.accent, width: 72, height: 72, borderRadius: 36, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none'}}>{i + 1}</div>
            <div style={{...F, fontWeight: 700, fontSize: 52, color: T.ink, whiteSpace: 'nowrap'}}>{t}</div></div>; })}
      </div>
    </Frame>
  );
};

// ───────── 새 판(parts/fx) ─────────
const Two: React.FC<{s: CScene}> = ({s}) => <Frame s={s}><TwoLines {...s.data.two} beats={tallyStarts(tl(s.lines))} /></Frame>;
const Dca: React.FC<{s: CScene}> = ({s}) => <Frame s={s}><DcaCal12 {...s.data.cal} beats={tallyStarts(tl(s.lines))} /></Frame>;
const Slips: React.FC<{s: CScene}> = ({s}) => <Frame s={s}><CardSlips {...s.data.slips} beats={tallyStarts(tl(s.lines))} /></Frame>;
const Eq: React.FC<{s: CScene}> = ({s}) => <Frame s={s}><EqSteps {...s.data.eq} beats={tallyStarts(tl(s.lines))} /></Frame>;

// ───────── motion 부품 장면 ─────────
const FxScene: React.FC<{s: CScene; fx: any}> = ({s, fx}) => (
  <Frame s={s}><FxDates {...fx} phase={s.kind === 'fxline' ? 'line' : 'bars'} /></Frame>
);
// 부품 하나를 줄 단위 조각으로 — 조각 장면 안에서 off 프레임만큼 앞당겨 같은 시간표를 보여 준다(전체 줄 = 자막·[자막] 띠·박자)
const Mo: React.FC<{s: CScene; m: MoScene}> = ({s, m}) => {
  const full = tl(m.lines); const b0 = tallyStarts(full); const sk: number[] = m.data.skipBeats || []; const beats = b0.filter((_: number, i: number) => !sk.includes(i)); const c = s.data.comp;   // 10/20 PD: 한 줄을 두 줄로 나눈 자리(skipBeats)는 부품 박자에서 빼 옛 박자 번호 그대로
  const child = c === 'hedge' ? <HedgeFlip {...m.data} beats={beats} /> : c === 'even' ? <EvenLadder {...m.data} beats={beats} /> : <DaysBelow {...m.data} beats={beats} />;
  return (
    <Sequence from={-s.data.off} durationInFrames={s.data.off + s.frames} layout="none">
      <TallyFrame title={m.title} art={art(s.data.icon)} source={m.source} chapter={s.data.chapter} lines={full} capTop={CAPTOP}>{child}</TallyFrame>
    </Sequence>
  );
};


// 10/19 벤치마크 지시(quality-gap-1019): 시간에 따라 변하는 돈은 장마다 선 그래프 한 장 — 원자료(ECOS·KRX) 선 + 점선 기준 + 말 순서대로 켜지는 꼬리표
const LineS: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const f = useCurrentFrame(); const st = starts(s.lines);
  const at = (a: number) => a >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[a] + 6;
  const X = 300, Y = 330, W = 1300, H = 400;
  const series = d.series.map(([name, c, pts]: [string, string, number[]]) => ({name, color: col(c), pts, width: 6}));
  const n = d.series[0][2].length; const xy = lineXY(X, Y, W, H, d.min, d.max, n);
  return (
    <Frame s={s}>
      <TallyLineChart series={series} x={X} y={Y} w={W} h={H} min={d.min} max={d.max} start={4} dur={d.dur ?? 70}
        base={d.base ? {v: d.base[0], text: d.base[1], x: d.base[2]} : undefined}
        ticks={d.ticks.map(([v, t]: [number, string]) => ({v, text: t}))} xlabels={d.xlabels.map(([i, t]: [number, string]) => ({i, text: t}))} />
      {d.tags.map((t: any, i: number) => { const [tx, ty] = xy(t[0], t[1]); return <TallyTag key={i} x={tx} y={ty} text={t[2]} start={at(t[3]) + (t[6] || 0)} side={t[4]} hot={t[5]} size={30} />; })}
      {d.big ? <div style={{...F, position: 'absolute', left: 330, top: 300, fontWeight: 800, fontSize: 104, color: col(d.big[1]), opacity: ease(f, at(d.big[2] ?? 0), 14), whiteSpace: 'nowrap', letterSpacing: -3}}>{d.big[0]}</div> : null}
    </Frame>
  );
};

const KIND: Record<string, React.FC<{s: CScene}>> = {line: LineS, big: Big, pair: Pair, rows: Rows, bars: Bars, ask: Ask, list5: List5, two: Two, dca: Dca, slips: Slips, eq: Eq};

// 글꼴(PD)을 다 받은 뒤 그린다 — 10/17 미리보기에서 숫자가 대체 글꼴로 찍힌 프레임이 섞였다(@font-face만으로는 렌더가 기다리지 않음)
const useFont = () => {
  const [h] = React.useState(() => delayRender('PD 글꼴'));
  React.useEffect(() => {
    Promise.all([['700', 'fonts/pd700.ttf'], ['500', 'fonts/pd500.ttf']].map(([w, u]) => new FontFace('PD', `url(${staticFile(u)})`, {weight: w}).load()))
      .then((fs) => { fs.forEach((x) => document.fonts.add(x)); continueRender(h); }).catch((e) => { console.error(e); continueRender(h); });
  }, [h]);
};

export const X1: React.FC<X1Props> = (p) => {
  useFont();
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => {
        const st = starts(s.lines); const K = KIND[s.kind];
        const el = <Sequence key={i} from={from} durationInFrames={s.frames}>
          {s.kind === 'broll' ? <TallyBroll src={s.data.src} license={s.data.license} from={s.data.from} say={s.data.say} side={s.data.side} x={s.data.x} chapter={s.data.chapter} lines={tl(s.lines)} />
            : s.kind === 'mo' ? <Mo s={s} m={p.motion[s.data.comp]} />
            : s.kind === 'fxline' || s.kind === 'fxbars' ? <FxScene s={s} fx={p.fx} />
            : K ? <K s={s} /> : null}
          {s.lines.map((l, j) => <Sequence key={j} from={st[j]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
        </Sequence>;
        from += s.frames; return el;
      })}
    </AbsoluteFill>
  );
};
