// T-1 "집 한 채 양도세, 2027·2028·2029에 팔면(정부안)" 화면 — 재료 work/video/t1.json(ep/T-1/t1props.py가 script.md·voice.json·calc_out·facts로 만든다)
// 틀은 TallyFrame(P1과 같음: 제목·형광 부제·흰 보드·정확한 값 칩·말 자막·출처). 색·글꼴은 parts/fm 토큰 그대로.
// 그림 종류(14): 두 집 대결 · 판 값 띠 · 공제 계단 칸 · 세금 카드 · 연도 공제율 표 · 세금 계단 막대 · 기본공제 카드+조건 · 배수 막대 ·
//   다섯 사람 표 · 정부 대조표 · 공제 한도 막대 · 계산 밖 카드+도장 · 햇수 달력 · 끝 질문.
// U5(같은 화면 8초 이하): 말 줄이 바뀔 때마다 판의 큰 칸이 바뀐다. 숫자 글자는 도형 위에 겹치지 않게 옆·위에 둔다(겹침 0).
// 숫자 글자는 전부 t1.json에서 온다. 코드 안 숫자는 배치·눈금뿐.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, HandCircle} from './parts/fm';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';

type TLine = TallyLine & {audio?: string | null};
export type TScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: TLine[]; frames: number};
export type T1Props = {fps: number; scenes: TScene[]; missing: number};
export const t1Frames = (p: T1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);
const ease = (f: number, a: number, d: number) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const Y0 = 345;

const useBeat = (s: TScene) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines); const n = s.lines.length;
  const at = (i: number) => (i == null || i < 0) ? 1e9 : st[Math.min(n - 1, i)] ?? 0;
  return {f, at, n};
};
const beatOf = (ats: number[], at: (i: number) => number, f: number) => { let b = -1; ats.forEach((i, j) => { if (f >= at(i)) b = j; }); return b; };

const Box: React.FC<{x: number; y: number; w: number; h: number; o?: number; bg?: string; border?: string; r?: number; children?: React.ReactNode; center?: boolean; pad?: string; row?: boolean}> =
  ({x, y, w, h, o = 1, bg = '#fff', border, r = 18, children, center = true, pad = '14px 24px', row}) => o <= 0 ? null : (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 10, width: w, height: h, opacity: o, background: bg, border: border ?? 'none', borderRadius: r,
    boxSizing: 'border-box', padding: pad, display: 'flex', flexDirection: row ? 'row' : 'column', alignItems: row ? 'center' : undefined, gap: row ? 24 : undefined,
    justifyContent: center ? 'center' : 'flex-start', overflow: 'hidden'}}>{children}</div>
);
const Txt: React.FC<{s: number; c?: string; w?: number; children: React.ReactNode; al?: 'left' | 'center' | 'right'; wrap?: boolean}> = ({s, c = T.ink, w = 700, children, al = 'left', wrap}) => (
  <div style={{...F, fontWeight: w, fontSize: s, color: c, lineHeight: 1.2, textAlign: al, whiteSpace: wrap ? 'normal' : 'nowrap', wordBreak: 'keep-all'}}>{children}</div>
);
const At: React.FC<{x: number; y: number; w?: number; o?: number; children: React.ReactNode}> = ({x, y, w, o = 1, children}) => o <= 0 ? null :
  <div style={{position: 'absolute', left: x, top: y, width: w, opacity: o}}>{children}</div>;

const House: React.FC<{w: number; c: string}> = ({w, c}) => (
  <svg width={w} height={w * 0.8} viewBox="0 0 100 80"><path d="M10 38 L50 6 L90 38" fill="none" stroke={c} strokeWidth={7} strokeLinejoin="round" strokeLinecap="round" />
    <rect x={20} y={36} width={60} height={40} rx={4} fill={c} /><rect x={43} y={52} width={14} height={24} rx={2} fill="#fff" /></svg>
);

// ───────── 0. 두 집 대결 ─────────
const Duel: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  if (b >= 6) return <Box x={560} y={Y0 + 40} w={800} h={400} bg={T.accent} o={fade(f, at(d.at[6]), 8)}><Txt s={200} c="#fff" al="center">{d.q}</Txt></Box>;
  if (b >= 4) {
    const max = 15000; const H = 330; const base = 800;
    const hi = b === 4 ? 0 : 3;
    return (
      <>
        {d.years.map((r: number[], i: number) => {
          const x = 220 + i * 330; const g = ease(f, at(d.at[4]) + i * 6, 16);
          const on = i === hi;
          return (
            <React.Fragment key={i}>
              <div style={{position: 'absolute', left: x, top: base - H * r[1] / max * g, width: 110, height: H * r[1] / max * g, background: T.accent, opacity: on ? 1 : 0.45, borderRadius: '10px 10px 0 0'}} />
              <div style={{position: 'absolute', left: x + 120, top: base - Math.max(8, H * r[2] / max * g), width: 110, height: Math.max(8, H * r[2] / max * g), background: T.ink, opacity: on ? 1 : 0.45, borderRadius: '10px 10px 0 0'}} />
              <At x={x} y={base + 8} w={230}><Txt s={32} c={on ? T.ink : T.ink3} al="center">{r[0]}년</Txt></At>
            </React.Fragment>
          );
        })}
        <At x={220} y={Y0 + 5}><div style={{display: 'flex', gap: 30}}>{[[T.accent, d.who[1][0]], [T.ink, d.who[0][0]]].map(([c, n], i) => <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10}}><div style={{width: 34, height: 18, background: c, borderRadius: 4}} /><Txt s={28} c={T.ink2}>{n}</Txt></div>)}</div></At>
        <Box x={1480} y={Y0 + 70} w={300} h={210} bg={b === 4 ? T.ink : T.accent} o={1}><Txt s={30} c="#fff">{b === 4 ? '2026년 차이' : '2029년 차이'}</Txt><Txt s={b === 4 ? 56 : 44} c="#fff">{d.gap[b === 4 ? 0 : 1]}</Txt></Box>
      </>
    );
  }
  return (
    <>
      {d.who.map((w: string[], i: number) => (
        <React.Fragment key={i}>
          <Box x={180 + i * 900} y={Y0 + 10} w={660} h={280} o={fade(f, i * 8, 10)} border={`3px solid ${T.line}`} row>
            <House w={190} c={i ? T.accent : T.ink} />
            <div><Txt s={52}>{w[0]}</Txt><div style={{height: 12}} />
              <div style={{background: b >= 1 ? (i ? T.accent : T.ink) : T.soft, borderRadius: 10, padding: '6px 16px', display: 'inline-block'}}><Txt s={40} c={b >= 1 ? '#fff' : T.ink}>{w[1]}</Txt></div></div>
          </Box>
          {b < 2 ? <Box x={180 + i * 900} y={Y0 + 320} w={660} h={160} bg={i ? T.accent : T.ink} o={fade(f, 40 + i * 12, 10)}><Txt s={28} c="#fff">2029년에 판다면</Txt><Txt s={64} c="#fff">{w[2]}</Txt></Box> : null}
        </React.Fragment>
      ))}
      <Box x={860} y={Y0 + 100} w={200} h={100} bg={T.soft}><Txt s={48} al="center">{d.price}</Txt></Box>
      {b >= 2 ? <Box x={180} y={Y0 + 320} w={1560} h={160} bg={T.ink} o={fade(f, at(d.at[2]), 8)} row>
        {d.gov.map((g: string, i: number) => <Txt key={i} s={i === 2 ? 46 : 40} c={i === 2 ? T.daccent : '#fff'}>{g}{i < 2 ? '  ·' : ''}</Txt>)}</Box> : null}
      {b >= 3 ? <div style={{position: 'absolute', left: 760, top: Y0 + 230, width: 400, height: 70, border: `6px solid ${T.rise}`, borderRadius: 14, background: '#fff', transform: `rotate(-4deg) scale(${1.2 - 0.2 * ease(f, at(d.at[3]), 8)})`,
        opacity: fade(f, at(d.at[3]), 6), display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Txt s={32} c={T.rise}>{d.fake}</Txt></div> : null}
    </>
  );
};

// ───────── 1장 판 값 띠 ─────────
const PX0 = 200, PU = 70;   // 1억 = 70px
const Price: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const g0 = ease(f, 0, 24); const R1 = Y0 + 70, R2 = Y0 + 230, R3 = Y0 + 380;
  return (
    <>
      <At x={PX0} y={R1 - 50}><Txt s={32} c={b >= 2 ? T.ink : T.ink3}>{d.sell}</Txt></At>
      <div style={{position: 'absolute', left: PX0, top: R1, width: 12 * PU * g0, height: 70, background: T.line, borderRadius: '10px 0 0 10px'}} />
      <div style={{position: 'absolute', left: PX0 + 12 * PU, top: R1, width: 8 * PU * ease(f, 12, 20), height: 70, background: b >= 1 ? T.accent : T.ink3, borderRadius: '0 10px 10px 0'}} />
      <div style={{position: 'absolute', left: PX0 + 12 * PU - 2, top: R1 - 14, width: 4, height: 98, background: T.ink}} />
      <At x={PX0} y={R1 + 80} w={12 * PU}><Txt s={30} c={T.ink2} al="center">{d.free}</Txt></At>
      {b >= 1 ? <At x={PX0 + 12 * PU} y={R1 + 80} w={8 * PU} o={fade(f, at(d.at[1]), 8)}><Txt s={30} c={T.accent} al="center">{d.over}</Txt></At> : null}
      {b >= 2 ? <Box x={1660} y={R1 - 20} w={150} h={110} bg={T.ink} o={fade(f, at(d.at[2]), 8)}><Txt s={30} c="#fff" al="center">{d.pct}</Txt><Txt s={22} c={T.dink3} al="center">판 값 중</Txt></Box> : null}
      {b >= 3 ? <>
        <div style={{position: 'absolute', left: PX0, top: R2, width: 8 * PU * ease(f, at(d.at[3]), 14), height: 60, background: T.ink3, borderRadius: '10px 0 0 10px'}} />
        <div style={{position: 'absolute', left: PX0 + 8 * PU, top: R2, width: 12 * PU * ease(f, at(d.at[3]) + 10, 18), height: 60, background: T.fall, borderRadius: '0 10px 10px 0'}} />
        <At x={PX0} y={R2 + 68} w={8 * PU}><Txt s={30} c={T.ink2} al="center">{d.buy}</Txt></At>
        <At x={PX0 + 8 * PU} y={R2 + 68} w={12 * PU}><Txt s={30} c={T.fall} al="center">{d.gain}</Txt></At>
      </> : null}
      {b >= 5 ? <>
        <div style={{position: 'absolute', left: PX0 + 8 * PU, top: R3, width: 12 * PU, height: 60, background: T.line, borderRadius: 10}} />
        <div style={{position: 'absolute', left: PX0 + 8 * PU, top: R3, width: 4.8 * PU * ease(f, at(d.at[5]), 16), height: 60, background: T.accent, borderRadius: '10px 0 0 10px'}} />
        <At x={PX0} y={R3 + 10} w={8 * PU - 20}><Txt s={30} c={T.ink2} al="right">{d.gain}의 {d.pct}</Txt></At>
      </> : null}
      {b >= 6 ? <Box x={1620} y={R3 - 50} w={190} h={150} bg={T.accent} o={fade(f, at(d.at[6]), 8)}><Txt s={24} c="#fff" wrap>세금이 붙는 돈</Txt><Txt s={52} c="#fff">{d.taxed}</Txt></Box> : null}
    </>
  );
};

// ───────── 2장 공제 계단 칸 ─────────
const LX0 = 560, LW = 84, LG = 10;
const Ladder: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const who = b >= 5 ? d.S : d.J; const nm = b >= 5 ? '수현 씨' : '정민 씨';
  const fill = (r: number) => {
    if (b < 1) return 0;
    if (b >= 5) return Math.round(who[r] * ease(f, at(d.at[5]) + r * 14, 24));
    if (b === 1) return r === 0 ? Math.round(10 * ease(f, at(d.at[1]), 30)) : 0;
    if (b === 2) return r === 0 ? 10 : Math.round(10 * ease(f, at(d.at[2]), 30));
    return 10;
  };
  return (
    <>
      {b >= 3 ? <Box x={160} y={Y0} w={360} h={80} bg={b >= 5 ? T.accent : T.ink} o={1}><Txt s={40} c="#fff" al="center">{nm}</Txt></Box> : null}
      {d.rows.map((r: string[], ri: number) => {
        const y = Y0 + 120 + ri * 170; const n = fill(ri);
        return (
          <React.Fragment key={ri}>
            <At x={160} y={y + 12} w={380}><Txt s={36}>{r[0]}</Txt><Txt s={26} c={T.ink2}>{r[1]}</Txt></At>
            {Array.from({length: 10}).map((_, i) => (
              <div key={i} style={{position: 'absolute', left: LX0 + i * (LW + LG), top: y, width: LW, height: 110, borderRadius: 12,
                background: i < n ? (ri ? T.accent : T.ink) : '#fff', border: i < n ? 'none' : `3px solid ${T.line}`, boxSizing: 'border-box'}} />
            ))}
          </React.Fragment>
        );
      })}
      {b === 4 || b >= 6 ? <Box x={1530} y={Y0 + 120} w={250} h={280} bg={b >= 6 ? T.accent : T.ink} o={fade(f, at(d.at[b >= 6 ? 6 : 4]), 8)}>
        <Txt s={28} c="#fff" al="center">공제율</Txt><Txt s={84} c="#fff" al="center">{who[2]}</Txt></Box> : null}
      <At x={LX0} y={Y0 + 470} w={940}><Txt s={26} c={T.ink3}>한 칸 = 1년 · 최대 10년</Txt></At>
    </>
  );
};

// ───────── 2장 세금 카드 ─────────
const TaxCard: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const card = (p: string[], i: number, o: number) => (
    <Box key={i} x={180 + i * 820} y={Y0 + 10} w={740} h={b >= 2 ? 250 : 400} bg={i ? T.accent : T.ink} o={o}>
      <Txt s={40} c="#fff">{p[0]} · 공제율 {p[1]}</Txt><div style={{height: 14}} /><Txt s={b >= 2 ? 70 : 96} c="#fff">{p[2]}</Txt>
    </Box>
  );
  return (
    <>
      {card(d.J, 0, fade(f, 0, 10))}
      {card(d.S, 1, b >= 1 ? fade(f, at(d.at[1]), 10) : 0.15)}
      {b >= 2 ? <Box x={180} y={Y0 + 290} w={1560} h={190} bg={T.soft} o={fade(f, at(d.at[2]), 8)} row>
        <div style={{width: 400, position: 'relative'}}><Txt s={44}>갖고 있던 해</Txt>
          <div style={{position: 'absolute', left: -10, right: 0, top: 26, height: 8, background: T.rise, transform: `scaleX(${ease(f, at(d.at[2]) + 8, 12)})`, transformOrigin: 'left'}} /></div>
        <Txt s={50}>{d.cut}</Txt></Box> : null}
    </>
  );
};

// ───────── 3장 연도 공제율 표 ─────────
const RCX = 560, RCW = 380, RCG = 20;
const Rates: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const col = b <= 0 ? 0 : b <= 2 ? 1 : 2;
  const hiCell = (ri: number, ci: number) => b < 4 && ci === col && (b === 1 ? ri === 0 : b === 2 ? ri === 1 : true);
  const rows: string[][] = [...d.rows, ...(b >= 4 ? [d.J] : []), ...(b >= 5 ? [d.S] : [])];
  return (
    <>
      {d.cols.map((c: string, i: number) => <At key={i} x={RCX + i * (RCW + RCG)} y={Y0} w={RCW}><Txt s={32} c={i === col && b < 4 ? T.accent : T.ink3} al="center">{c}</Txt></At>)}
      {rows.map((r: string[], ri: number) => {
        const y = Y0 + 55 + ri * 105 + (ri >= 2 ? 20 : 0); const person = ri >= 2;
        return (
          <React.Fragment key={ri}>
            <At x={160} y={y + 22} w={380} o={fade(f, person ? at(d.at[ri + 2]) : 0, 10)}><Txt s={36} c={person ? (ri === 3 ? T.accent : T.ink) : T.ink2}>{r[0]}</Txt></At>
            {r.slice(1).map((v, ci) => {
              const on = hiCell(ri, ci); const strike = v === '없음';
              const bg = on ? T.ink : person ? (ri === 3 ? T.accent : T.ink) : ri % 2 ? '#fff' : T.bg;
              return <div key={ci} style={{position: 'absolute', left: RCX + ci * (RCW + RCG), top: y, width: RCW, height: 90, borderRadius: 12, background: bg,
                border: !on && !person && ri % 2 ? `3px solid ${T.line}` : 'none', boxSizing: 'border-box', opacity: fade(f, person ? at(d.at[ri + 2]) + ci * 10 : ci * 5, 10),
                display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Txt s={46} c={on || person ? '#fff' : strike ? T.rise : T.ink}>{v}</Txt></div>;
            })}
          </React.Fragment>
        );
      })}
    </>
  );
};

// ───────── 3장 수현 씨 세금 계단 ─────────
const Climb: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const max = 15000, H = 360, base = 820;
  return (
    <>
      {d.bars.map((r: any[], i: number) => {
        const x = 220 + i * 360; const g = ease(f, i * 20, 18); const h = H * r[1] / max * g;
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: x, top: base - h, width: 240, height: h, background: i === 2 ? T.accent : T.ink2, borderRadius: '12px 12px 0 0'}} />
            <At x={x - 40} y={base - h - 56} w={320} o={g}><Txt s={36} al="center">{r[2]}</Txt></At>
            <At x={x} y={base + 6} w={240}><Txt s={30} c={T.ink2} al="center">{r[0]}년</Txt></At>
          </React.Fragment>
        );
      })}
      {d.steps.map((t: string, i: number) => <Box key={i} x={420 + i * 360} y={Y0 + 10 + (1 - i) * 60} w={300} h={64} bg={T.soft} o={fade(f, 30 + i * 20, 8)}><Txt s={30} al="center">{t}</Txt></Box>)}
      {b >= 1 ? <Box x={1340} y={Y0 + 40} w={440} h={330} bg={T.ink} o={fade(f, at(d.at[1]), 8)}>
        {d.same.split(' · ').map((t: string, i: number) => <Txt key={i} s={i === 2 ? 46 : 38} c={i === 2 ? T.daccent : '#fff'}>{t}</Txt>)}</Box> : null}
    </>
  );
};

// ───────── 4장 기본공제 ─────────
const Basic: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  return (
    <>
      {b <= 0 ? <Box x={360} y={Y0 + 60} w={1200} h={340} bg={T.ink} o={fade(f, 0, 10)}><Txt s={44} c={T.dink3} al="center">정부안대로라면</Txt><Txt s={100} c="#fff" al="center">정민 씨 세금 ↓</Txt></Box> : null}
      {b >= 1 ? <Box x={160} y={Y0} w={820} h={300} bg="#fff" border={`4px solid ${T.ink}`} o={fade(f, at(d.at[1]), 10)}>
        <Txt s={34} c={T.ink2}>기본공제</Txt><div style={{height: 10}} />
        <div style={{display: 'flex', alignItems: 'baseline', gap: 20}}><Txt s={56} c={T.ink3}>{d.from}</Txt><Txt s={50} c={T.ink3}>→</Txt><Txt s={76} c={T.accent}>{d.to}</Txt></div>
        {b >= 2 ? <div style={{marginTop: 12, background: T.accent, borderRadius: 10, padding: '4px 16px', alignSelf: 'flex-start', opacity: fade(f, at(d.at[2]), 8)}}><Txt s={36} c="#fff">{d.x}</Txt></div> : null}
      </Box> : null}
      {b >= 2 ? d.conds.map((c: string, i: number) => (
        <Box key={i} x={1030} y={Y0 + i * 100} w={740} h={84} bg={T.soft} o={fade(f, at(d.at[2]) + 10 + i * 10, 8)} row pad="10px 24px">
          <svg width={44} height={44}><path d="M6 24 L18 36 L38 8" fill="none" stroke={T.accent} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" /></svg><Txt s={36}>{c}</Txt>
        </Box>)) : null}
      {b >= 3 ? <Box x={160} y={Y0 + 330} w={1610} h={150} bg={T.ink} o={fade(f, at(d.at[3]), 8)} row>
        <Txt s={36} c={T.dink3}>정민 씨</Txt><Txt s={56} c={T.dink3}>{d.J[0]}</Txt><Txt s={56} c="#fff">→</Txt><Txt s={72} c={T.daccent}>{d.J[1]}</Txt></Box> : null}
    </>
  );
};

// ───────── 4장 배수 막대 ─────────
const Ratio: React.FC<{s: TScene}> = ({s}) => {
  const {f} = useBeat(s); const d = s.data; const max = 15000;
  return (
    <>
      {d.bars.map((r: any[], i: number) => {
        const g = ease(f, i * 10, 20); const w = Math.max(14, 1050 * r[1] / max * g);
        return (
          <React.Fragment key={i}>
            <At x={160} y={Y0 + 30 + i * 150}><Txt s={40} c={T.ink2}>{r[0]}</Txt></At>
            <div style={{position: 'absolute', left: 360, top: Y0 + 15 + i * 150, width: w, height: 90, background: i ? T.ink : T.accent, borderRadius: 12}} />
            <At x={360 + w + 20} y={Y0 + 33 + i * 150} o={g}><Txt s={44}>{r[2]}</Txt></At>
          </React.Fragment>
        );
      })}
      <Box x={1450} y={Y0 + 260} w={330} h={200} bg={T.accent} o={fade(f, 40, 8)}><Txt s={30} c="#fff" al="center">차이</Txt><Txt s={84} c="#fff" al="center">{d.times}</Txt></Box>
      {d.why.map((t: string, i: number) => <Box key={i} x={160 + i * 640} y={Y0 + 330} w={600} h={110} bg={T.soft} o={fade(f, 75 + i * 10, 8)}><Txt s={38} al="center">{t}</Txt></Box>)}
    </>
  );
};

// ───────── 5장 다섯 사람 표 ─────────
const FW = [150, 500, 250, 250, 250, 250]; const FX0 = 130; const FRH = 76;
const fxs = FW.map((_, i) => FX0 + FW.slice(0, i).reduce((a, v) => a + v, 0));
const Five: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const hiRow = b === 1 ? 0 : b === 2 || b === 3 ? 3 : b === 4 || b === 5 ? 4 : -1;
  const tag = b === 1 ? d.tags[1] : b === 2 || b === 3 ? d.tags[2] : b === 5 ? d.tags[3] : b >= 6 ? d.tags[4] : '';
  return (
    <>
      {['', '판 값 · 갖고 있던 · 살았던', ...d.cols].map((c: string, i: number) => <At key={i} x={fxs[i]} y={Y0} w={FW[i]}><Txt s={26} c={T.ink3} al="center">{c}</Txt></At>)}
      {d.rows.map((r: any[], ri: number) => {
        const cells = [r[0], r[1], ...r[2]]; const on = ri === hiRow;
        return cells.map((v: string, ci: number) => {
          const hot = on && (ci >= 2) && (b !== 5 || ci === 5); const dsc = b >= 6 && ci === 1;
          return <div key={ri + '-' + ci} style={{position: 'absolute', left: fxs[ci] + 3, top: Y0 + 40 + ri * FRH, width: FW[ci] - 6, height: FRH - 8, borderRadius: 10, opacity: fade(f, ri * 5, 10),
            background: hot ? (b >= 4 ? T.accent : T.ink) : on || dsc ? T.soft : ri % 2 ? '#fff' : T.bg, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <Txt s={ci === 1 ? 28 : 32} c={hot ? '#fff' : T.ink}>{v}</Txt></div>;
        });
      })}
      {tag ? <Box x={FX0} y={Y0 + 440} w={900} h={56} bg={b >= 6 ? T.ink : T.accent} o={1} pad="6px 20px"><Txt s={32} c="#fff">{tag}</Txt></Box> : null}
    </>
  );
};

// ───────── 6장 정부 대조표 ─────────
const Verify: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  return (
    <>
      {b <= 0 ? <Box x={360} y={Y0 + 60} w={1200} h={340} bg={T.ink} o={fade(f, 0, 10)} row>
        <Txt s={80} c="#fff">정부 숫자</Txt><Txt s={80} c={T.daccent}>=?</Txt><Txt s={80} c="#fff">파이어맵</Txt></Box> : null}
      {b >= 1 ? d.cases.map((c: any[], ci: number) => {
        const show = b >= (ci ? 4 : 2); const o = show ? fade(f, at(d.at[ci ? 4 : 2]), 10) : 0.25; const ok = b >= (ci ? 5 : 3);
        const X = 160 + ci * 820;
        return (
          <React.Fragment key={ci}>
            <Box x={X} y={Y0} w={780} h={90} bg={ci ? T.accent : T.ink} o={b >= 1 ? 1 : 0}><Txt s={32} c="#fff">{c[0]} · {c[1]}</Txt></Box>
            {d.heads.map((h: string, i: number) => <At key={i} x={X + i * 260} y={Y0 + 104} w={250}><Txt s={24} c={T.ink3} al="center">{h}</Txt></At>)}
            {c[2].map((r: string[], ri: number) => {
              const jump = ci === 1 && ri === 2 && b >= 5;
              return [r[0] + '년', r[2], r[1]].map((v, i) => (
                <div key={ri + '-' + i} style={{position: 'absolute', left: X + i * 260 + 4, top: Y0 + 140 + ri * 82, width: 252, height: 72, borderRadius: 10, opacity: o,
                  background: jump && i ? T.accent : i === 2 && ok ? T.soft : ri % 2 ? '#fff' : T.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8}}>
                  <Txt s={34} c={jump && i ? '#fff' : T.ink}>{v}</Txt>{i === 2 && ok ? <Txt s={30} c={jump ? '#fff' : T.accent}>✓</Txt> : null}</div>
              ));
            })}
          </React.Fragment>
        );
      }) : null}
      {b >= 5 ? <Box x={980} y={Y0 + 400} w={780} h={80} bg={T.ink} o={fade(f, at(d.at[5]) + 10, 8)}><Txt s={34} c="#fff" al="center">{d.jump}</Txt></Box> : null}
    </>
  );
};

// ───────── 6장 공제 한도 ─────────
const CPX = 520, CPU = 48;   // 1억 = 48px (10/16 PD: 55px면 '한도 20억' 글자가 판 오른쪽 테두리에 걸림)
const Cap: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const rows: any[][] = [...d.caps, d.mine];
  return (
    <>
      {rows.map((r: any[], i: number) => {
        const g = ease(f, i * 14, 18); const y = Y0 + 20 + i * 140; const w = r[1] * CPU * g;
        return (
          <React.Fragment key={i}>
            <At x={160} y={y + 18} w={340}><Txt s={36} c={i === 2 ? T.ink : T.ink2}>{r[0]}</Txt></At>
            <div style={{position: 'absolute', left: CPX, top: y, width: w, height: 84, background: i === 2 ? T.accent : i ? T.ink : T.ink3, borderRadius: 12}} />
            <At x={CPX + w + 20} y={y + 16} o={g}><Txt s={44}>{i === 2 ? r[2] : '한도 ' + r[2]}</Txt></At>
          </React.Fragment>
        );
      })}
      <div style={{position: 'absolute', left: CPX + 10 * CPU - 2, top: Y0 + 150, width: 4, height: 300, background: T.ink, opacity: fade(f, 40, 10)}} />
      {b >= 1 ? <Box x={1120} y={Y0 + 300} w={640} h={140} bg={T.soft} o={fade(f, at(d.at[1]), 8)}><Txt s={50} al="center">{d.safe}</Txt></Box> : null}
    </>
  );
};

// ───────── 7장 계산 밖 ─────────
const Excluded: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const when = [1, 3, 4]; const third = [2, 3, 5];
  const midT = at(d.at[3]) + 135;   // 65세 줄(9초 남짓)은 가운데에서 셋째 줄을 띄운다
  return (
    <>
      {b <= 0 ? <Box x={460} y={Y0 + 60} w={1000} h={320} bg={T.ink} o={fade(f, 0, 10)}><Txt s={84} c="#fff" al="center">계산에서 뺀 것</Txt></Box> : null}
      {b >= 1 ? d.cards.map((c: string[], i: number) => {
        if (b < when[i]) return null; const on = (i === 0 && b <= 2) || (i === 1 && b === 3) || (i === 2 && (b === 4 || b === 5));
        const show3 = i === 1 ? f >= midT || b >= 4 : b >= third[i];
        return (
          <Box key={i} x={160 + i * 545} y={Y0} w={515} h={290} bg={on ? T.ink : '#fff'} border={on ? 'none' : `3px solid ${T.line}`} o={fade(f, at(d.at[when[i]]), 10)} center={false} pad="26px 28px">
            <Txt s={36} c={on ? '#fff' : T.ink} wrap>{c[0]}</Txt><div style={{height: 16}} />
            <Txt s={30} c={on ? T.dink3 : T.ink2} wrap>{c[1]}</Txt><div style={{height: 16}} />
            {show3 ? <div style={{background: on ? T.accent : T.soft, borderRadius: 10, padding: '6px 14px', opacity: fade(f, i === 1 ? Math.min(midT, at(d.at[4])) : at(d.at[third[i]]), 8)}}><Txt s={30} c={on ? '#fff' : T.ink} wrap>{c[2]}</Txt></div> : null}
          </Box>
        );
      }) : null}
      {b >= 6 ? <div style={{position: 'absolute', left: 560, top: Y0 + 360, width: 800, height: 110, border: `8px solid ${T.rise}`, borderRadius: 18, background: '#fff', transform: `rotate(-3deg) scale(${1.25 - 0.25 * ease(f, at(d.at[6]), 8)})`,
        opacity: fade(f, at(d.at[6]), 6), display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Txt s={50} c={T.rise}>{d.stamp}</Txt></div> : null}
    </>
  );
};

// ───────── 8장 햇수 달력 ─────────
const KX0 = 520, KW = 100, KG = 12;
const Calendar: React.FC<{s: TScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const gapOn = b >= 1;
  return (
    <>
      {d.rows.map((r: any[], ri: number) => {
        const y = Y0 + 20 + ri * 160;
        return (
          <React.Fragment key={ri}>
            <At x={160} y={y + 30} w={340}><Txt s={38}>{r[0]}</Txt></At>
            {Array.from({length: 10}).map((_, i) => {
              const on = i < Math.round(r[1] * ease(f, ri * 20, 30)); const gap = gapOn && ri === 1 && i >= r[1];
              return <div key={i} style={{position: 'absolute', left: KX0 + i * (KW + KG), top: y, width: KW, height: 120, borderRadius: 12, boxSizing: 'border-box',
                background: on ? (ri ? T.accent : T.ink) : gap ? T.soft : '#fff', border: on ? 'none' : gap ? `3px dashed ${T.rise}` : `3px solid ${T.line}`}} />;
            })}
          </React.Fragment>
        );
      })}
      {gapOn ? <Box x={KX0 + 2 * (KW + KG)} y={Y0 + 330} w={8 * (KW + KG) - KG} h={70} bg={T.rise} o={fade(f, at(d.at[1]), 8)}><Txt s={36} c="#fff" al="center">{d.per}</Txt></Box> : null}
      {b >= 2 ? <Box x={160} y={Y0 + 330} w={KX0 + 2 * (KW + KG) - 190} h={140} bg={T.ink} o={fade(f, at(d.at[2]), 8)}>
        <Txt s={30} c={T.dink3}>{d.S[0]} · {d.S[1]}</Txt><Txt s={48} c="#fff">{d.S[2]}</Txt></Box> : null}
      {b >= 2 ? <At x={KX0 + 2 * (KW + KG)} y={Y0 + 420} w={8 * (KW + KG)} o={fade(f, at(d.at[2]) + 10, 8)}><Txt s={36} c={T.ink2} al="center">{d.S[3]}</Txt></At> : null}
    </>
  );
};

// ───────── 끝 질문(끝 화면 20초: 6초마다 판이 바뀐다) ─────────
const Ask: React.FC<{s: TScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const ph = f < 180 ? 0 : f < 360 ? 1 : 2;
  return (
    <>
      <Box x={160} y={Y0} w={1180} h={140} bg={T.ink} o={fade(f, 0, 10)}><Txt s={62} c="#fff">{d.q}</Txt></Box>
      {ph !== 1 ? d.cells.map((c: string[], i: number) => (
        <Box key={i} x={160 + i * 600} y={Y0 + 170} w={560} h={200} border={`4px solid ${i ? T.accent : T.ink}`} o={fade(f, ph ? 360 : 12 + i * 8, 10)}>
          <Txt s={40} c={T.ink2} al="center">{c[0]}</Txt><Txt s={80} al="center">{c[1]}</Txt></Box>)) : null}
      {ph === 1 ? d.sum.map((c: string[], i: number) => (
        <Box key={i} x={160 + i * 600} y={Y0 + 170} w={560} h={200} bg={i ? T.accent : T.ink} o={fade(f, 180 + i * 8, 10)}>
          <Txt s={36} c="#fff" al="center">{c[0]} · {c[1]}</Txt><Txt s={60} c="#fff" al="center">{c[2]}</Txt></Box>)) : null}
      <At x={160} y={Y0 + 400} w={1180} o={fade(f, 30, 10)}><Txt s={40} c={ph === 2 ? T.accent : T.ink2}>{ph === 1 ? '2029년에 판다면 · ' + d.note : d.tail}</Txt></At>
      {ph === 2 ? <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}><HandCircle cx={330} cy={Y0 + 425} rx={210} ry={50} p={ease(f, 370, 16)} /></svg> : null}
    </>
  );
};

const Body: React.FC<{s: TScene}> = ({s}) => {
  switch (s.kind) {
    case 'duel': return <Duel s={s} />;
    case 'price': return <Price s={s} />;
    case 'ladder': return <Ladder s={s} />;
    case 'taxcard': return <TaxCard s={s} />;
    case 'rates': return <Rates s={s} />;
    case 'climb': return <Climb s={s} />;
    case 'basic': return <Basic s={s} />;
    case 'ratio': return <Ratio s={s} />;
    case 'five': return <Five s={s} />;
    case 'verify': return <Verify s={s} />;
    case 'cap': return <Cap s={s} />;
    case 'excluded': return <Excluded s={s} />;
    case 'calendar': return <Calendar s={s} />;
    case 'ask': return <Ask s={s} />;
    default: return null;
  }
};

// 정확한 값 칩 — P1과 같음(40자 넘으면 ' · ' 마디로 나눠 차례로)
const CHIP_MAX = 40;
const chipPages = (cap: string) => {
  const parts = cap.split(' · '); const out: string[] = []; let cur = '';
  for (const p of parts) { const nx = cur ? cur + ' · ' + p : p; if (cur && nx.length > CHIP_MAX && cur.length >= 12) { out.push(cur); cur = p; } else cur = nx; }
  if (cur) out.push(cur); return out;
};
const Chip: React.FC<{lines: TLine[]}> = ({lines}) => {
  const f = useCurrentFrame(); const st = tallyStarts(lines); const k = tallyIdx(lines, f);
  let i = -1; for (let j = 0; j <= k; j++) if (lines[j]?.cap) i = j;
  if (i < 0) return null;
  const cap = lines[i].cap as string; const pages = chipPages(cap);
  let nxt = lines.length; for (let j = i + 1; j < lines.length; j++) if (lines[j].cap) { nxt = j; break; }
  const win = (nxt < lines.length ? st[nxt] : st[lines.length - 1] + lines[lines.length - 1].frames) - st[i];
  const per = Math.max(60, Math.floor(win / pages.length));
  const pi = Math.min(pages.length - 1, Math.floor((f - st[i]) / per));
  const a = st[i] + pi * per; const co = interpolate(f, [a, a + 8], [0, 1], CL);
  return (
    <div style={{position: 'absolute', left: 130, top: 252, maxWidth: 1660, opacity: co, transform: `translateY(${(1 - co) * -8}px)`,
      background: T.ink, borderRadius: 10, padding: '7px 16px', display: 'flex', gap: 12, alignItems: 'baseline'}}>
      <span style={{...F, fontWeight: 700, fontSize: 20, color: T.daccent, whiteSpace: 'nowrap'}}>{/\d/.test(cap) ? '정확한 값' : '참고'}{pages.length > 1 ? ` ${pi + 1}/${pages.length}` : ''}</span>
      <span style={{...F, fontWeight: 700, fontSize: 26, color: '#fff', lineHeight: 1.3, whiteSpace: 'nowrap'}}>{pages[pi]}</span>
    </div>
  );
};

// 실사 끼우기(10/16 PD, U5 같은 화면 8초 — C2 CutAway와 같은 방식): data.cutaways = [[줄, 그림, 시작 비율, 끝 비율]] · 새 글자 0(자막은 그 줄 말, 출처는 장면 출처)
const CutAway: React.FC<{src: string; text: string; source: string; n: number}> = ({src, text, source, n}) => {
  const f = useCurrentFrame(); const z = interpolate(f, [0, n], [1.3, 1.36], CL); /* 오른쪽 맞춤 확대: 왼쪽 가장자리 간판(상호) 글자를 화면 밖으로 */ const o = interpolate(f, [0, 6], [0, 1], CL);
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden', opacity: o}}>
      <Img src={staticFile(src)} style={{position: 'absolute', left: 1920 - 1920 * z, top: (1080 - 1080 * z) / 2, width: 1920 * z, height: 1080 * z, filter: 'saturate(0.85) brightness(0.9)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 330, background: 'linear-gradient(rgba(16,17,20,0), rgba(16,17,20,0.85))'}} />
      <div style={{...F, fontWeight: 500, fontSize: source.length > 120 ? 17 : 20, color: 'rgba(255,255,255,0.75)', position: 'absolute', left: 64, right: 110, bottom: 18, whiteSpace: 'nowrap', overflow: 'hidden'}}>{source}</div>
      <div style={{position: 'absolute', bottom: 58, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <div style={{...F, fontWeight: 700, fontSize: 40, lineHeight: 1.35, color: '#fff', background: 'rgba(16,17,20,0.86)', padding: '14px 34px', borderRadius: 16, maxWidth: 1500, textAlign: 'center', wordBreak: 'keep-all'}}>{text}</div>
      </div>
    </AbsoluteFill>
  );
};

// 그림이 덮는 동안 밑의 판은 그리지 않는다(겹침 검사가 가려진 판 글자를 잡음 — C2 UnderCut과 같음, 판 움직임은 프레임 계산이라 뒤에 그대로 이어짐)
const UnderCut: React.FC<{s: TScene; st: number[]; children: React.ReactNode}> = ({s, st, children}) => {
  const f = useCurrentFrame();
  const hide = (s.data.cutaways || []).some((c: any[]) => { const lf = s.lines[c[0]].frames; const a = st[c[0]] + Math.round(lf * (c[2] ?? 0)); const b = st[c[0]] + Math.round(lf * (c[3] ?? 1)); return f >= a && f < b; });
  return hide ? null : <>{children}</>;
};

const SceneView: React.FC<{s: TScene; last: boolean}> = ({s, last}) => {
  const st = tallyStarts(s.lines);
  return (
    <AbsoluteFill>
      <UnderCut s={s} st={st}>
        <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines.map((l) => ({...l, cap: null}))} board capX={last ? 760 : 960}>
          <Body s={s} />
          <Chip lines={s.lines} />
        </TallyFrame>
      </UnderCut>
      {(s.data.cutaways || []).map((c: [number, string, number?, number?], j: number) => { const lf = s.lines[c[0]].frames; const a = st[c[0]] + Math.round(lf * (c[2] ?? 0)); const n = Math.round(lf * ((c[3] ?? 1) - (c[2] ?? 0)));
        return <Sequence key={'c' + j} from={a} durationInFrames={n}><CutAway src={c[1]} text={s.lines[c[0]].text} source={s.source || ''} n={n} /></Sequence>; })}
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </AbsoluteFill>
  );
};

export const T1: React.FC<T1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} last={i === p.scenes.length - 1} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
