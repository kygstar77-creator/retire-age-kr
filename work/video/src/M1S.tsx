// M-1 롱폼을 자른 세로 쇼츠(1080×1920) — 재료: work/video/m1s_<편>.json (research/cardshorts/m1clips.py가 voice.json·m1.json에서 만든다)
// 목소리는 롱폼 문장 wav 그대로. 숫자 글자는 전부 props에서 온다(코드 안 숫자는 배치 값뿐).
// 화면: 위 질문(고정) · 가운데 흰 판(장면 그림) · 큰 말 자막 · 정확한 값 칩 · 출처 · 진행 막대. 아래 끝 230px은 유튜브 제목 덮개 자리.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame, HandCircle} from './parts/fm';
import {TallyBars, TallyBar} from './motion/TallyBars';

type SLine = {n: number; text: string; cap?: string | null; audio: string; frames: number};
type SScene = {kind: string; label: string; source?: string | null; data: any; lines: SLine[]; frames: number};
export type M1SProps = {fps: number; name: string; question: string[]; hot: string; track?: [string, number, string][] | null; base: string; long: string; scenes: SScene[]};
export const m1sFrames = (p: M1SProps) => p.scenes.reduce((a, s) => a + s.frames, 0);

const BW = 1000, BH = 860;
const COL: Record<string, string> = {accent: T.accent, ink: T.ink, rise: T.rise, ink2: T.ink2, fall: T.fall};
const starts = (lines: SLine[]) => { const o: number[] = []; let a = 0; for (const l of lines) { o.push(a); a += l.frames; } return o; };
// 줄 번호(소수면 그 줄 안 비율) → 장면 안 프레임
const atL = (s: SScene, x: number | null | undefined) => {
  if (x == null) return 1e9; const i = Math.min(Math.floor(x), s.lines.length - 1); const st = starts(s.lines);
  return st[i] + (x - i) * s.lines[i].frames;
};
const ease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
const pop = (f: number, a: number) => ({opacity: ease(f, a, 8), transform: `translateY(${(1 - ease(f, a, 12)) * 24}px)`});

const Box: React.FC<{x: number; y: number; w: number; h?: number; bg?: string; children: React.ReactNode; style?: React.CSSProperties}> = ({x, y, w, h, bg = T.bg, children, style}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, background: bg, borderRadius: 22, padding: '20px 28px', boxSizing: 'border-box', ...style}}>{children}</div>
);
const Txt: React.FC<{s: number; c?: string; w?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({s, c = T.ink, w = 700, children, style}) => (
  <div style={{...F, fontWeight: w, fontSize: s, color: c, lineHeight: 1.18, letterSpacing: s > 60 ? -2 : -0.5, wordBreak: 'keep-all', ...style}}>{children}</div>
);
const nameSize = (n: string, big: number) => (n.length > 8 ? Math.round(big * 0.68) : big);

// ───────── 장면들 (판 안 좌표 1000×860) ─────────
const Ask: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <>
      <Box x={40} y={30} w={920} bg={T.soft}>
        <Txt s={130} c={T.accent}>{d.goal}</Txt>
        <Txt s={36} c={T.ink2} style={{marginTop: 8}}>{d.goalSub}</Txt>
      </Box>
      <svg width={120} height={140} style={{position: 'absolute', left: 440, top: 290, opacity: 1}}>
        <path d={`M60 0 L60 ${40 + 60 * ease(f, 0, 12)}`} stroke={T.ink} strokeWidth={12} strokeLinecap="round" />
        <path d="M22 80 L60 122 L98 80" fill="none" stroke={T.ink} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" opacity={ease(f, 4, 6)} />
      </svg>
      <div style={{position: 'absolute', left: 0, width: BW, top: 440, textAlign: 'center', ...pop(f, 0)}}><Txt s={100}>{d.ask}</Txt></div>
      {d.names.map((n: string, i: number) => (
        <Box key={i} x={40 + i * 313} y={600} w={294} h={220} bg={T.bg} style={{...pop(f, 2 + i * 5), textAlign: 'center'}}>
          <Txt s={n.length > 6 ? 26 : 40} c={T.ink2} style={{height: 70, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{n}</Txt>
          <Txt s={92} c={T.ink3} style={{transform: `scale(${1 + 0.06 * Math.sin((f - i * 9) / 6)})`}}>?억원</Txt>
        </Box>
      ))}
    </>
  );
};

const Flow: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const L1 = s.lines[0].frames;
  return (
    <>
      <Box x={40} y={30} w={920} bg={T.soft} style={pop(f, 0)}>
        <Txt s={96} c={T.ink}>{d.top[0]}</Txt><Txt s={32} c={T.ink2} style={{marginTop: 6}}>{d.top[1]}</Txt>
      </Box>
      <div style={{position: 'absolute', left: 60, top: 268, display: 'flex', alignItems: 'center', gap: 22, ...pop(f, L1 * 0.04)}}>
        <svg width={60} height={90}><path d="M30 86 L30 8 M8 32 L30 8 L52 32" stroke={T.rise} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
        <Txt s={52} c={T.rise}>{d.mid}</Txt>
      </div>
      <Box x={40} y={390} w={920} bg={T.ink} style={pop(f, L1 * 0.1)}>
        <Txt s={38} c={T.dink}>{d.bottom[0]}</Txt>
        <Txt s={124} c={T.daccent} style={{marginTop: 4}}>{d.bottom[1]}</Txt>
        <Txt s={32} c={T.dink3} style={{marginTop: 6, opacity: ease(f, L1 * 0.3)}}>{d.bottom[2]}</Txt>
      </Box>
      <Box x={40} y={720} w={920} bg={T.bg} style={pop(f, L1 * 0.4)}><Txt s={40} c={T.ink}>{d.rule}</Txt></Box>
    </>
  );
};

const Track: React.FC<{track: [string, number, string][]; upto: number; at: number; y: number}> = ({track, upto, at, y}) => {
  const f = useCurrentFrame(); const max = Math.max(...track.map((t) => t[1])) * 1.05;
  return (
    <div style={{position: 'absolute', left: 40, top: y, width: 920}}>
      <Txt s={30} c={T.ink3}>월 100만원에 필요한 돈</Txt>
      {track.map((t, i) => {
        const p = i < upto ? 1 : i === upto ? ease(f, at, 20) : 0;
        return (
          <div key={i} style={{display: 'flex', alignItems: 'center', marginTop: 14, height: 66}}>
            <Txt s={28} c={i > upto ? T.ink3 : T.ink2} style={{width: 290}}>{t[0]}</Txt>
            {i > upto ? <Txt s={34} c={T.ink3}>?억원</Txt> : null}
            <div style={{height: 60, width: 430 * (t[1] / max) * p, background: i === upto ? T.accent : T.ink3, borderRadius: 8}} />
            <Txt s={34} c={i === upto ? T.accent : T.ink2} style={{marginLeft: 14, opacity: p, whiteSpace: 'nowrap'}}>{t[2]}</Txt>
          </div>
        );
      })}
    </div>
  );
};

const Card: React.FC<{s: SScene; track?: [string, number, string][] | null}> = ({s, track}) => {
  const f = useCurrentFrame(); const d = s.data;
  const ra = atL(s, d.rateAt), na = atL(s, d.needAt);
  const needC = d.hot ? T.accent : T.ink;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 26, ...pop(f, 0)}}>
        <Txt s={nameSize(d.name, 92)}>{d.name}</Txt>
        <Txt s={30} c={T.ink2} style={{marginTop: 8}}>{d.desc}</Txt>
        <div style={{display: 'inline-block', marginTop: 12, ...F, fontWeight: 700, fontSize: 28, color: '#fff', background: T.ink2, borderRadius: 10, padding: '4px 14px'}}>분배 {d.freq}</div>
      </div>
      <div style={{position: 'absolute', left: 40, top: 250, opacity: f >= ra ? 1 : 0.45}}>
        <Txt s={32} c={T.ink2}>지난 1년 분배율</Txt>
        <Txt s={108} style={{whiteSpace: 'nowrap', marginTop: 10, transform: `scale(${0.85 + 0.15 * ease(f, ra)})`, transformOrigin: 'left center'}}>{f >= ra ? d.rate : '?%'}</Txt>
        <Txt s={26} c={T.ink3} style={{opacity: ease(f, ra + 8)}}>{d.rateCalc}</Txt>
      </div>
      <div style={{position: 'absolute', left: 480, top: 250, opacity: f >= na ? 1 : 0.45}}>
        <Txt s={32} c={T.ink2}>필요한 돈</Txt>
        <Txt s={104} c={needC} style={{whiteSpace: 'nowrap', marginTop: 10, transform: `scale(${0.8 + 0.2 * ease(f, na)})`, transformOrigin: 'left center'}}>{f >= na ? d.need : '?억원'}</Txt>
      </div>
      {f >= na ? <svg width={BW} height={BH} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}><HandCircle cx={715} cy={375} rx={250} ry={90} p={ease(f, na + 6, 18)} color={needC} /></svg> : null}
      {d.note ? <div style={{position: 'absolute', right: 40, top: 150, width: 520, textAlign: 'right', ...pop(f, atL(s, 0.6))}}><Txt s={26} c={T.ink2}>{d.note}</Txt></div> : null}
      {d.count ? (
        <div style={{position: 'absolute', left: 40, top: 478, width: 920, display: 'flex', alignItems: 'center', gap: 16, ...pop(f, 4)}}>
          <Txt s={26} c={T.ink3} style={{width: 150, whiteSpace: 'nowrap'}}>1년 분배 횟수</Txt>
          <div style={{display: 'flex', gap: 12}}>
            {Array.from({length: 12}).map((_, i) => <div key={i} style={{width: 50, height: 50, borderRadius: 25, background: i < d.count ? T.accent : T.line, opacity: i < d.count ? ease(f, 6 + i * 2, 8) : 1}} />)}
          </div>
        </div>
      ) : null}
      {track ? <Track track={track} upto={d.track} at={na} y={570} /> : null}
    </>
  );
};

const Bars: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[], i: number) => ({label: b[0], value: b[1], valueText: b[2], start: -22 + i * 4, color: COL[b[3]] ?? T.ink2}));
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 30, ...pop(f, 0)}}>
        <Txt s={58} c={T.ink}>{d.note[0]}</Txt><Txt s={58} c={T.accent}>{d.note[1]}</Txt>
      </div>
      <TallyBars bars={bars} x={80} y={250} w={840} h={420} max={d.max} labelSize={30} valueSize={60} tags />
      {d.stamp ? <div style={{position: 'absolute', left: 40, top: 800, opacity: ease(f, 30)}}><Txt s={24} c={T.ink3}>{d.stamp}</Txt></div> : null}
    </>
  );
};

const Jump: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const base = 790, H = 560, sc = (v: number) => (v / d.max) * H;
  const bar = (x: number, v: [number, string, string], col: string, big: boolean) => (
    <>
      <div style={{position: 'absolute', left: x, top: base - sc(v[0]), width: 280, height: sc(v[0]), background: col, borderRadius: '16px 16px 0 0'}} />
      <div style={{position: 'absolute', left: x - 60, width: 400, top: base - sc(v[0]) - (big ? 124 : 96), textAlign: 'center'}}>
        <Txt s={big ? 100 : 76} c={col} style={{whiteSpace: 'nowrap'}}>{v[1]}</Txt>
      </div>
      <div style={{position: 'absolute', left: x - 40, width: 380, top: base + 12, textAlign: 'center'}}><Txt s={30} c={T.ink2}>{v[2]}</Txt></div>
    </>
  );
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={46}>{d.name}</Txt><Txt s={30} c={T.ink2} style={{marginTop: 6}}>{d.what}</Txt></div>
      <div style={{position: 'absolute', left: 60, right: 60, top: base, borderTop: `4px solid ${T.ink}`}} />
      {bar(120, d.a, T.ink3, false)}
      {bar(620, d.b, T.accent, true)}
      <svg width={180} height={120} style={{position: 'absolute', left: 420, top: 440}}><path d="M10 60 L150 60 M110 22 L152 60 L110 98" stroke={T.ink} strokeWidth={12} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
      <div style={{position: 'absolute', left: 40, top: 150, ...F, fontWeight: 700, fontSize: 40, color: '#fff', background: T.rise, borderRadius: 12, padding: '6px 18px',
        transform: `scale(${1 + 0.08 * ease(f, 10, 8) - 0.08 * ease(f, 18, 10)})`}}>{d.mult}</div>
    </>
  );
};

const Morph: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const L1 = s.lines[0].frames;
  const avg = d.vals.reduce((a: number, v: number) => a + v, 0) / d.vals.length;
  const m = ease(f, L1 * 0.32, L1 * 0.3);
  const n = d.vals.length, x0 = 50, w = 900, g = 14, bw = (w - g * (n - 1)) / n, base = 700, H = 420;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={30} c={T.ink2}>{d.name}</Txt></div>
      <div style={{position: 'absolute', left: 40, top: 80}}>
        <Txt s={88} c={m > 0.5 ? T.ink3 : T.ink} style={{textDecoration: m > 0.5 ? 'line-through' : 'none'}}>{d.ask}</Txt>
        <Txt s={50} c={T.accent} style={{marginTop: 10, opacity: ease(f, L1 * 0.62)}}>{d.ans}</Txt>
      </div>
      {d.vals.map((v: number, i: number) => {
        const h = ((avg + (v - avg) * m) / d.hi) * H * ease(f, i * 2, 12);
        const hot = m > 0.95 && (i === d.min || i === d.max);
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: x0 + i * (bw + g), top: base - h, width: bw, height: h, background: hot ? (i === d.min ? T.accent : T.ink) : T.ink3, borderRadius: '8px 8px 0 0'}} />
            {hot ? <div style={{position: 'absolute', left: x0 + i * (bw + g) + bw / 2, top: base - h - 52, transform: 'translateX(-50%)', ...F, fontWeight: 700, fontSize: 30, color: '#fff',
              background: i === d.min ? T.accent : T.ink, borderRadius: 8, padding: '2px 10px', whiteSpace: 'nowrap'}}>{d.texts[i]}</div> : null}
            <div style={{position: 'absolute', left: x0 + i * (bw + g) - 6, width: bw + 12, top: base + 10, textAlign: 'center', ...F, fontWeight: 500, fontSize: 19, color: T.ink3}}>{d.labels[i]}</div>
          </React.Fragment>
        );
      })}
      <div style={{position: 'absolute', left: 50, right: 50, top: base, borderTop: `3px solid ${T.ink}`}} />
    </>
  );
};

const Months: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const mi = atL(s, d.minAt), ma = atL(s, d.maxAt);
  const n = d.vals.length, x0 = 50, w = 900, g = 14, bw = (w - g * (n - 1)) / n, base = 520, H = 330;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 22}}><Txt s={nameSize(d.name, 64)}>{d.name}</Txt><Txt s={28} c={T.ink3} style={{marginTop: 4}}>{d.unit} · 지난 12회</Txt></div>
      {d.ratio ? <div style={{position: 'absolute', right: 40, top: 40, ...pop(f, atL(s, d.ratio[1])), ...F, fontWeight: 700, fontSize: 34, color: '#fff', background: T.ink, borderRadius: 12, padding: '8px 18px'}}>{d.ratio[0]}</div> : null}
      {d.vals.map((v: number, i: number) => {
        const h = (v / d.hi) * H * ease(f, 2 + i * 2, 14);
        const isMin = i === d.min && f >= mi, isMax = i === d.max && f >= ma;
        const col = isMin ? T.accent : isMax ? T.ink : T.ink3;
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: x0 + i * (bw + g), top: base - h, width: bw, height: h, background: col, borderRadius: '8px 8px 0 0'}} />
            <div style={{position: 'absolute', left: x0 + i * (bw + g) - 8, width: bw + 16, top: base + 10, textAlign: 'center', ...F, fontWeight: 500, fontSize: 19, color: isMin ? T.accent : T.ink3}}>{d.labels[i]}</div>
          </React.Fragment>
        );
      })}
      <div style={{position: 'absolute', left: 50, right: 50, top: base, borderTop: `3px solid ${T.ink}`}} />
      {[d.max, d.min].map((i: number) => {
        const isMin = i === d.min, on = isMin ? f >= mi : f >= ma; if (!on) return null;
        const h = (d.vals[i] / d.hi) * H; const cx = x0 + i * (bw + g) + bw / 2;
        const shift = isMin && Math.abs(d.min - d.max) === 1 ? (d.max > d.min ? -88 : -12) : -50;
        return <div key={i} style={{position: 'absolute', left: Math.min(Math.max(cx, 120), 880), top: base - h - 58, transform: `translateX(${shift}%) scale(${0.7 + 0.3 * ease(f, isMin ? mi : ma, 8)})`,
          ...F, fontWeight: 700, fontSize: 32, color: '#fff', background: isMin ? T.accent : T.ink, borderRadius: 8, padding: '3px 12px', whiteSpace: 'nowrap', boxShadow: '0 0 0 3px #fff'}}>{(isMin ? '최소 ' : '최대 ') + d.texts[i]}</div>;
      })}
      {d.note ? <div style={{position: 'absolute', left: 40, top: 590, ...pop(f, atL(s, d.note[1]))}}><Txt s={40} c={T.rise}>{d.note[0]}</Txt></div> : null}
      <Box x={40} y={660} w={920} h={180} bg={T.bg} style={{opacity: 0.35 + 0.65 * ease(f, atL(s, d.jump[3]))}}>
        <Txt s={30} c={T.ink2}>월 100만원에 필요한 돈</Txt>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 18, marginTop: 6}}>
          <Txt s={64} c={T.ink3}>{d.jump[0]}</Txt><Txt s={64} c={T.ink3}>→</Txt>
          <Txt s={88} c={T.accent} style={{opacity: ease(f, atL(s, d.jump[3]) + 10)}}>{f >= atL(s, d.jump[3]) ? d.jump[1] : '?'}</Txt>
          <Txt s={30} c={T.rise} style={{whiteSpace: 'nowrap', opacity: ease(f, atL(s, d.jump[3]) + 18)}}>{d.jump[2]}</Txt>
        </div>
      </Box>
    </>
  );
};

const Pair: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines);
  const G = d.groups.length, x0 = 60, w = 880, gw = w / G, base = 600, H = 400;
  const dim = (gi: number, bi: number) => {
    if (!d.dimPlan) return 1; let o = 1;
    st.forEach((a, i) => { const [g, b] = d.dimPlan[Math.min(i, d.dimPlan.length - 1)]; const hit = (g < 0 || g === gi) && (b < 0 || b === bi);
      const t = interpolate(f, [a, a + 12], [0, 1], CL); o = o + ((hit ? 1 : 0.25) - o) * t; });
    return o;
  };
  let call: [string, number] | null = null; for (const c of d.call ?? []) if (f >= atL(s, c[1])) call = c;
  const ghost = !call && d.pre && d.call?.length ? d.call[0] : null;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 26, display: 'flex', gap: 30}}>
        {d.legend.map((l: [string, string], i: number) => <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10}}><div style={{width: 30, height: 30, borderRadius: 6, background: COL[l[1]]}} /><Txt s={32} c={T.ink2}>{l[0]}</Txt></div>)}
      </div>
      {d.groups.map((g: [string, [number, string, string][]], gi: number) => {
        const nb = g[1].length, bw = Math.min(180, (gw - 60) / nb);
        return (
          <React.Fragment key={gi}>
            {g[1].map((b, bi) => {
              const h = (b[0] / d.max) * H * ease(f, (d.pre ? -18 : 2) + gi * 6 + bi * 4, 16); const x = x0 + gi * gw + (gw - nb * bw - (nb - 1) * 14) / 2 + bi * (bw + 14);
              return (
                <div key={bi} style={{opacity: dim(gi, bi)}}>
                  <div style={{position: 'absolute', left: x, top: base - h, width: bw, height: h, background: COL[b[2]], borderRadius: '10px 10px 0 0'}} />
                  <div style={{position: 'absolute', left: x - 7, width: bw + 14, top: base - h - 50, textAlign: 'center', ...F, fontWeight: 700, fontSize: Math.min(44, Math.floor((bw + 14) / (b[1].length * 0.58))), color: COL[b[2]], whiteSpace: 'nowrap'}}>{b[1]}</div>
                </div>
              );
            })}
            <div style={{position: 'absolute', left: x0 + gi * gw, width: gw, top: base + 12, textAlign: 'center'}}><Txt s={g[0].length > 6 ? 24 : 34} c={T.ink}>{g[0]}</Txt></div>
          </React.Fragment>
        );
      })}
      <div style={{position: 'absolute', left: 50, right: 50, top: base, borderTop: `3px solid ${T.ink}`}} />
      {call ? <Box key={call[0]} x={40} y={690} w={920} bg={T.ink} style={pop(f, atL(s, call[1]))}><Txt s={40} c={T.dink}>{call[0]}</Txt></Box> : null}
      {ghost ? <Box x={40} y={690} w={920} bg={T.ink} style={{opacity: 0.18}}><Txt s={40} c={T.dink}>{ghost[0]}</Txt></Box> : null}
      {d.stamp ? <div style={{position: 'absolute', left: 40, top: 820}}><Txt s={22} c={T.ink3}>{d.stamp}</Txt></div> : null}
    </>
  );
};

const First: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const L1 = s.lines[0].frames;
  const b = L1 * 0.62;
  const chips = ['연 세전 분배', '세금', '건강보험료', '손에 남는 돈'];
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 30}}>
        <Txt s={46} c={T.ink2}>제일 먼저 부딪히는 건</Txt>
        <Txt s={130} c={f >= b ? T.ink3 : T.ink} style={{textDecoration: f >= b ? 'line-through' : 'none', marginTop: 6}}>{d.a}?</Txt>
      </div>
      <div style={{position: 'absolute', left: 40, top: 250, ...pop(f, b)}}>
        <Txt s={150} c={T.rise}>{d.b}</Txt>
      </div>
      <div style={{position: 'absolute', left: 40, top: 280 + 200 * ease(f, b - 4, 12), display: 'flex', flexWrap: 'wrap', gap: 16, width: 920}}>
        {chips.map((c, i) => {
          const hot = i === 2 && f >= b;
          return <div key={i} style={{...F, fontWeight: 700, fontSize: 46, width: 452, height: 116, boxSizing: 'border-box', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: 14, color: hot ? '#fff' : T.ink, background: hot ? T.rise : T.bg,
            border: `3px solid ${hot ? T.rise : T.line}`}}>{(i ? '→ ' : '') + c}</div>;
        })}
      </div>
      <div style={{position: 'absolute', left: 40, top: 760}}><Txt s={32} c={T.ink2}>{d.sub}</Txt></div>
    </>
  );
};

const Gauge: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const X = 50, W = 900, Y = 120, HH = 110, sc = (v: number) => (Math.min(v, d.max) / d.max) * W;
  let val = 0, col = T.ink;
  for (const [v, at, c] of d.fill) { const a = atL(s, at); const t = ease(f, a, 18); if (f >= a) col = COL[c]; val = val + (v - val) * t; }
  const lx = X + sc(d.line[0]);
  let cur = -1; d.rows.forEach((r: any[], i: number) => { if (f >= atL(s, r[0])) cur = i; });
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 26, opacity: d.under ? 1 - ease(f, atL(s, d.under[1]), 10) * (1 - ease(f, atL(s, d.under[2]), 10)) : 1}}><Txt s={34} c={T.ink2}>{d.head}</Txt></div>
      <div style={{position: 'absolute', left: X, top: Y, width: W, height: HH, background: T.line, borderRadius: 16}} />
      <div style={{position: 'absolute', left: X, top: Y, width: sc(val), height: HH, background: col, borderRadius: 16}} />
      <div style={{position: 'absolute', left: lx - 4, top: Y - 24, width: 8, height: HH + 48, background: T.accent, borderRadius: 4}} />
      <div style={{position: 'absolute', left: lx - 150, width: 300, top: Y + HH + 30, textAlign: 'center'}}><Txt s={38} c={T.accent}>{d.line[1]}</Txt></div>
      {d.under ? (() => { const u = atL(s, d.under[1]); const o = ease(f, u, 10) * (1 - ease(f, atL(s, d.under[2]), 10));
        return <div style={{position: 'absolute', left: X, top: Y - 14, width: lx - X, height: HH + 28, border: `6px solid ${T.ink}`, borderRadius: 20, opacity: o}}>
          <div style={{position: 'absolute', left: 16, top: -58, ...F, fontWeight: 700, fontSize: 34, color: '#fff', background: T.ink, borderRadius: 10, padding: '4px 14px', whiteSpace: 'nowrap'}}>{d.under[0]}</div>
        </div>; })() : null}
      {d.rows.map((r: any[], i: number) => {
        const big = i === 2;
        const top = [330, 450, 570, 740][i];
        return (
          <div key={i} style={{position: 'absolute', left: 40, top, width: 920, display: 'flex', alignItems: 'baseline', gap: 18, opacity: i > cur ? 0.2 : (i === cur ? 1 : 0.55) * (0.2 + 0.8 * ease(f, atL(s, r[0]), 10))}}>
            <Txt s={big ? 84 : 50} c={COL[r[3]]} style={{whiteSpace: 'nowrap'}}>{r[1]}</Txt>
            <Txt s={big ? 28 : 34} c={T.ink2}>{r[2]}</Txt>
          </div>
        );
      })}
    </>
  );
};

const Premium: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const b = atL(s, d.at);
  const W = 900, wa = (d.a[2] / d.b[2]) * W;
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 26}}><Txt s={34} c={T.ink2}>지역가입자 · {d.who}</Txt></div>
      <div style={{position: 'absolute', left: 40, top: 100}}>
        <Txt s={34} c={T.ink2}>{d.a[1]}</Txt><Txt s={124} c={T.ink}>{d.a[0]}</Txt>
      </div>
      <div style={{position: 'absolute', left: 50, top: 300, width: wa * ease(f, 4, 16), height: 84, background: T.ink, borderRadius: 12}} />
      <div style={{position: 'absolute', left: 40, top: 410, opacity: 0.2 + 0.8 * ease(f, b, 10)}}>
        <Txt s={34} c={T.ink2}>{d.b[1]}</Txt><Txt s={136} c={T.rise}>{d.b[0]}</Txt>
      </div>
      <div style={{position: 'absolute', left: 50, top: 650, width: W * ease(f, b + 6, 22), height: 84, background: T.rise, borderRadius: 12}} />
      <div style={{position: 'absolute', left: 40, top: 740, ...pop(f, b + 40)}}><Txt s={30} c={T.ink2}>{d.note}</Txt></div>
    </>
  );
};

const Timeline: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const fa = atL(s, d.fillAt), ha = atL(s, d.hitAt);
  const cw = 64, g = 6, X = 150;
  const row = (y: number, label: string, cell: (i: number) => [string, string]) => (
    <div style={{position: 'absolute', left: 30, top: y}}>
      <Txt s={40} style={{position: 'absolute', left: 0, top: 24}}>{label}</Txt>
      {Array.from({length: 12}).map((_, i) => { const [bg, fg] = cell(i); return (
        <div key={i} style={{position: 'absolute', left: X - 30 + i * (cw + g), top: 0, width: cw, height: 96, borderRadius: 10, background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center',
          ...F, fontWeight: 700, fontSize: 26, color: fg}}>{i + 1}</div>); })}
    </div>
  );
  const segOn = [fa, ha - 10, ha];
  return (
    <>
      {row(40, d.y0, (i) => (f >= fa + i * 2 ? [T.soft, T.accent] : [T.bg, T.ink3]))}
      {row(160, d.y1, (i) => (i >= d.hit && f >= ha ? [T.rise, '#fff'] : f >= ha - 10 ? [T.line, T.ink3] : [T.bg, T.ink3]))}
      {d.segs.map((sg: [string, string], i: number) => (
        <div key={i} style={{position: 'absolute', left: 40, top: 320 + i * 125, display: 'flex', alignItems: 'baseline', gap: 20, opacity: 0.22 + 0.78 * ease(f, segOn[i], 10)}}>
          <Txt s={52} c={i === 2 ? T.rise : T.ink} style={{whiteSpace: 'nowrap'}}>{sg[0]}</Txt><Txt s={34} c={T.ink2}>{sg[1]}</Txt>
        </div>
      ))}
      {d.note ? <Box x={40} y={712} w={920} bg={T.ink} style={{opacity: 0.18 + 0.82 * ease(f, atL(s, d.note[1]), 10)}}><Txt s={46} c={T.dink}>{d.note[0]}</Txt></Box> : null}
    </>
  );
};

const Ask1: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const ca = atL(s, d.chipAt);
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 24}}><Txt s={40} c={T.ink2}>{d.when}</Txt></div>
      {d.names.map((n: string, i: number) => (
        <Box key={i} x={40 + i * 313} y={100} w={294} h={250} bg={T.soft} style={{...pop(f, 4 + i * 8), textAlign: 'center'}}>
          <Txt s={100} c={T.accent}>{d.put}</Txt>
          <Txt s={n.length > 6 ? 26 : 38} c={T.ink2} style={{marginTop: 18}}>{n}</Txt>
        </Box>
      ))}
      <div style={{position: 'absolute', left: 0, width: BW, top: 400, textAlign: 'center', ...pop(f, 30)}}>
        <Txt s={44} c={T.ink2}>{d.now}</Txt>
        <Txt s={110} style={{transform: `scale(${1 + 0.04 * Math.sin(f / 7)})`}}>{d.ask}</Txt>
      </div>
      <div style={{position: 'absolute', left: 40, top: 680, display: 'flex', gap: 16}}>
        {d.chips.map((c: string, i: number) => <div key={i} style={{...F, fontWeight: 700, fontSize: 40, color: '#fff', background: i ? T.ink2 : T.ink, borderRadius: 14, padding: '14px 26px', opacity: 0.2 + 0.8 * ease(f, ca + i * 10, 10)}}>{c}</div>)}
      </div>
    </>
  );
};

const Total: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const bars: TallyBar[] = d.bars.map((b: any[]) => ({label: b[0], value: b[1], valueText: b[2], start: atL(s, b[5]) + 2, color: COL[b[3]] ?? T.ink2, sub: b[4]}));
  return (
    <>
      <div style={{position: 'absolute', left: 40, top: 26}}><Txt s={52} c={T.ink}>1억 → 1년 뒤</Txt><Txt s={30} c={T.ink2} style={{marginTop: 4}}>원화 · 세전 · 분배금 + 가격 변화</Txt></div>
      {bars.map((b, i) => { const n = bars.length, g = Math.min(80, 840 / n * 0.35), bw = (840 - g * (n - 1)) / n; const o = 1 - ease(f, b.start, 8);
        return o <= 0 ? null : <div key={i} style={{position: 'absolute', left: 80 + i * (bw + g), top: 200 + 440 * 0.45, width: bw, height: 440 * 0.55, background: T.line, borderRadius: '10px 10px 0 0', opacity: o,
          display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 700, fontSize: 90, color: T.ink3}}>?</div>; })}
      <TallyBars bars={bars} x={80} y={200} w={840} h={440} max={d.max} labelSize={30} valueSize={64} tags circle={{i: 0, start: 30}} />
    </>
  );
};

const Body: React.FC<{s: SScene; p: M1SProps}> = ({s, p}) => {
  switch (s.kind) {
    case 'ask': return <Ask s={s} />;
    case 'flow': return <Flow s={s} />;
    case 'card': return <Card s={s} track={p.track} />;
    case 'bars': return <Bars s={s} />;
    case 'jump': return <Jump s={s} />;
    case 'morph': return <Morph s={s} />;
    case 'months': return <Months s={s} />;
    case 'pair': return <Pair s={s} />;
    case 'first': return <First s={s} />;
    case 'gauge': return <Gauge s={s} />;
    case 'premium': return <Premium s={s} />;
    case 'timeline': return <Timeline s={s} />;
    case 'ask1': return <Ask1 s={s} />;
    case 'total': return <Total s={s} />;
    default: return null;
  }
};

// 말 자막: 줄 안 문장을 글자 수 비율로 나눠 보여 준다(한 화면 글자가 5초 넘게 그대로 있지 않게)
const sentences = (t: string) => t.split(/(?<=[.?!])\s+/).filter(Boolean);
const Caption: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  let k = -1; st.forEach((a, i) => { if (f >= a) k = i; });
  if (k < 0) k = 0;
  const l = s.lines[k]; const ss = sentences(l.text); const tot = ss.reduce((a, x) => a + x.length, 0);
  const speak = l.frames - 8; let acc = 0, j = 0, from = st[k];
  for (let i = 0; i < ss.length; i++) { const a = st[k] + (acc / tot) * speak; if (f >= a) { j = i; from = a; } acc += ss[i].length; }
  const o = interpolate(f, [from, from + 4], [0, 1], CL);
  return (
    <div style={{height: 246, boxSizing: 'border-box', background: T.ink, padding: '18px 32px', borderRadius: 22, display: 'flex', alignItems: 'center'}}>
      <div style={{...F, fontWeight: 700, fontSize: ss[j].length > 40 ? 50 : 58, lineHeight: 1.3, color: '#fff', wordBreak: 'keep-all', opacity: 0.4 + 0.6 * o, transform: `translateY(${(1 - o) * 8}px)`}}>{ss[j]}</div>
    </div>
  );
};

const CapChip: React.FC<{s: SScene}> = ({s}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  let cap: string | null = null, at = 0;
  s.lines.forEach((l, i) => { if (f >= st[i] && l.cap) { cap = l.cap; at = st[i]; } });
  const label = cap ?? s.label; const isCap = !!cap;
  return (
    <div style={{minHeight: 132, boxSizing: 'border-box', display: 'flex', gap: 16, alignItems: 'center', background: isCap ? T.soft : '#eceff3', borderRadius: 16, padding: '14px 22px',
      opacity: isCap ? interpolate(f, [at, at + 8], [0.3, 1], CL) : 1}}>
      <span style={{...F, fontWeight: 700, fontSize: 26, color: isCap ? T.accent : T.ink2, whiteSpace: 'nowrap'}}>{isCap ? (/\d/.test(label) ? '정확한 값' : '참고') : '지금'}</span>
      <span style={{...F, fontWeight: 700, fontSize: label.length > 80 ? 26 : 32, color: T.ink, lineHeight: 1.3, wordBreak: 'keep-all'}}>{label}</span>
    </div>
  );
};

const Frame: React.FC<{s: SScene; p: M1SProps; from: number; total: number}> = ({s, p, from, total}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  const drift = interpolate(f, [0, s.frames], [1, 1.03], CL);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 40, top: 322, width: BW, height: BH, background: '#fff', border: `2px solid ${T.line}`, borderRadius: 32, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: BW, height: BH, transform: `scale(${drift})`, transformOrigin: '50% 40%'}}><Body s={s} p={p} /></div>
      </div>
      <div style={{position: 'absolute', left: 40, top: 1200, width: 920, display: 'flex', flexDirection: 'column', gap: 16}}>
        <Caption s={s} />
        <CapChip s={s} />
      </div>
      <div style={{position: 'absolute', left: 40, top: 1612, width: 920}}>
        {s.source ? <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink2, lineHeight: 1.35, wordBreak: 'keep-all'}}>출처 {s.source}</div> : null}
      </div>
      <div style={{position: 'absolute', left: 40, top: 1700, width: 920, height: 12, background: T.line, borderRadius: 6}}>
        <div style={{width: `${((from + f) / total) * 100}%`, height: 12, background: T.accent, borderRadius: 6}} />
      </div>
      <div style={{position: 'absolute', left: 40, top: 1726, ...F, fontWeight: 700, fontSize: 28, color: T.ink2}}>{p.long}</div>
      {s.lines.map((l, i) => <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
    </AbsoluteFill>
  );
};

export const M1S: React.FC<M1SProps> = (p) => {
  const total = m1sFrames(p); let from = 0;
  const q = p.question;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: 40, top: 62, display: 'flex', alignItems: 'center', gap: 12}}>
        <Flame size={30} /><span style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2}}>파이어맵</span>
        <span style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3, marginLeft: 12}}>{p.base}</span>
      </div>
      <div style={{position: 'absolute', left: 40, top: 118, width: 1000}}>
        {q.map((line, i) => {
          const k = line.indexOf(p.hot);
          return <div key={i} style={{...F, fontWeight: 700, fontSize: 76, lineHeight: 1.2, color: T.ink, letterSpacing: -2, whiteSpace: 'nowrap'}}>
            {k < 0 ? line : <>{line.slice(0, k)}<span style={{color: T.accent}}>{p.hot}</span>{line.slice(k + p.hot.length)}</>}</div>;
        })}
      </div>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><Frame s={s} p={p} from={from} total={total} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
