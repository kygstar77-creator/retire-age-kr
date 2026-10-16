// X-1 "같은 1억, 바꾼 날마다"(환율 편) 화면 — 재료 work/video/x1.json(ep/X-1/x1props.py가 script.md·voice.json·calc_out·facts·raw 원문으로 만든다)
// 틀은 TallyFrame(T1과 같음: 제목·형광 부제·흰 보드·정확한 값 칩·말 자막·출처). 색·글꼴은 parts/fm 토큰 + 초록 하나(motion.md '달러로 번 몫').
// 그림 종류(14): 두 선+틈 칠하기 · 날짜 네 장 물음 카드 · 환율 선+날짜 점(FxDates line) · 같은 1억 막대(FxDates bars) · 번 몫/깎은 몫 폭포 막대 ·
//   주가×환율 식 카드 · 은행 창구+고시판 · 사고팔 때 벌어지는 띠(parts/spread) · 계산 밖 카드 · 시소 · 결제 카드+굴림 숫자 · 엔화 선+계수기 · 지난 편 타일 · 끝 표.
// U5(같은 화면 8초 이하): 말 줄마다(긴 줄은 줄 안 비율로) 판의 큰 칸이 바뀐다. 숫자 글자는 도형 위에 겹치지 않게 옆·위·아래에 둔다.
// 실사: public/stock 안 기존 컷(P-1 달력·노인·작업장·서류)은 은행·공항·엔화와 맞지 않고 다른 편 컷 재사용 금지라 쓰지 않음 → 그림으로.
// 숫자 글자는 전부 x1.json에서 온다. 코드 안 숫자는 배치·눈금뿐.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, HandCircle} from './parts/fm';
import {SpreadBand} from './parts/spread';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';
import {FxDates, FxDatesProps} from './motion/FxDates';
import {RollNumber} from './motion/RollNumber';

type TLine = TallyLine & {audio?: string | null};
export type XScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: TLine[]; frames: number};
export type X1Props = {fps: number; scenes: XScene[]; missing: number};
export const x1Frames = (p: X1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const GREEN = T.ink;   // 10/16 PD: 토큰 밖 초록(#1f9d55) 대신 잉크 — 색 4개 원칙, '번 몫'=잉크·'깎은 몫'=rise
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);
const ease = (f: number, a: number, d: number) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const Y0 = 345;

const useBeat = (s: XScene) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines); const n = s.lines.length;
  const at = (i: number) => (i == null || i < 0) ? 1e9 : st[Math.min(n - 1, i)] ?? 0;
  const total = s.lines.reduce((a, l) => a + l.frames, 0);
  return {f, at, n, total};
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
const Pill: React.FC<{x: number; y: number; o?: number; bg?: string; c?: string; s?: number; children: React.ReactNode}> = ({x, y, o = 1, bg = T.ink, c = '#fff', s = 30, children}) => o <= 0 ? null :
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 8, opacity: o, background: bg, borderRadius: 12, padding: '8px 20px'}}><Txt s={s} c={c}>{children}</Txt></div>;

// ───────── 0. 두 선 + 틈 칠하기 ─────────
const TwoLine: React.FC<{s: XScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const n = d.up.length; const X0 = 300, X1 = 1290, YT = 410, YB = 790;
  const X = (i: number) => X0 + i / (n - 1) * (X1 - X0); const Y = (v: number) => YB - (v - d.min) / (d.max - d.min) * (YB - YT);
  const p1 = ease(f, 6, Math.min(150, at(1) - 10)); const p2 = ease(f, at(1) + 4, 120);
  const path = (v: number[], p: number) => { const m = Math.max(1, Math.round(p * (n - 1))); return v.slice(0, m + 1).map((y, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)},${Y(y).toFixed(1)}`).join(' '); };
  const gap = b >= 3 ? ease(f, at(d.at[3]), 30) : 0;
  const m = Math.max(1, Math.round(gap * (n - 1)));
  const poly = gap > 0 ? [...d.up.slice(0, m + 1).map((v: number, i: number) => `${X(i)},${Y(v)}`), ...d.dn.slice(0, m + 1).map((v: number, i: number) => `${X(i)},${Y(v)}`).reverse()].join(' ') : '';
  const eu = Y(d.up[n - 1]), ed = Y(d.dn[n - 1]);
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {d.yt.map(([v]: [number, string], i: number) => <line key={i} x1={X0} x2={X1} y1={Y(v)} y2={Y(v)} stroke={v === 0 ? T.ink3 : T.line} strokeWidth={v === 0 ? 3 : 2} strokeDasharray={v === 0 ? '10 8' : undefined} />)}
        {gap > 0 && <polygon points={poly} fill={T.rise} opacity={0.28} />}
        <path d={path(d.up, p1)} fill="none" stroke={GREEN} strokeWidth={6} strokeLinejoin="round" />
        {f >= at(1) && <path d={path(d.dn, p2)} fill="none" stroke={T.rise} strokeWidth={6} strokeLinejoin="round" />}
        {p1 >= 1 && <circle cx={X(n - 1)} cy={eu} r={11} fill={GREEN} stroke="#fff" strokeWidth={4} />}
        {p2 >= 1 && <circle cx={X(n - 1)} cy={ed} r={11} fill={T.rise} stroke="#fff" strokeWidth={4} />}
      </svg>
      {d.yt.map(([v, t]: [number, string], i: number) => <At key={i} x={X0 - 130} y={Y(v) - 16} w={110}><Txt s={25} w={500} c={T.ink3} al="right">{t}</Txt></At>)}
      {d.xl.map(([i, t]: [number, string], k: number) => <At key={k} x={X(i) - 50} y={YB + 14} w={100} o={fade(f, 6 + (Math.min(150, at(1) - 10)) * i / (n - 1), 8)}><Txt s={24} w={500} c={T.ink3} al="center">{t}</Txt></At>)}
      {/* 끝 이름표 */}
      <At x={X1 + 30} y={eu - 62} o={fade(f, Math.min(150, at(1) - 10), 10)}><Txt s={28} c={GREEN}>{d.nameUp}</Txt><Txt s={44} c={GREEN}>{d.tagUp}</Txt></At>
      {f >= at(1) ? <At x={X1 + 30} y={ed - 20} o={fade(f, at(1) + 120, 10)}><Txt s={28} c={T.ink}>{d.nameDn}</Txt><Txt s={44} c={T.rise}>{d.tagDn}</Txt></At> : null}
      {/* 물음 */}
      {b === 2 ? <div style={{position: 'absolute', left: X(Math.round(n * 0.62)) - 170, top: (Y(d.up[Math.round(n * 0.62)]) + Y(d.dn[Math.round(n * 0.62)])) / 2 - 46, opacity: fade(f, at(d.at[2]), 8),
        transform: `scale(${0.9 + 0.1 * ease(f, at(d.at[2]), 10)})`, background: T.accent, borderRadius: 16, padding: '12px 28px'}}><Txt s={52} c="#fff">{d.q}</Txt></div> : null}
      {/* 새 나간 건 환율 */}
      {b >= 3 ? <Box x={X1 + 24} y={(eu + ed) / 2 - 64} w={480} h={140} bg={T.ink} o={fade(f, at(d.at[3]) + 20, 10)} pad="10px 22px" center>
        <Txt s={28} c={T.daccent}>{d.leak} · {d.rateName}</Txt>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 12, marginTop: 6}}><Txt s={40} c={T.dink3}>{d.from}</Txt><Txt s={36} c="#fff">→</Txt><Txt s={46} c="#fff">{d.to}</Txt></div>
      </Box> : null}
    </>
  );
};

// ───────── 0. 날짜 네 장 물음 카드 ─────────
const DateCards: React.FC<{s: XScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const h = b >= 1 ? 250 : 330;
  return (
    <>
      {d.cards.map((c: string[], i: number) => {
        const o = fade(f, 4 + i * 12, 10); const x = 160 + i * 410;
        return (
          <Box key={i} x={x} y={Y0} w={380} h={h} o={o} border={`3px solid ${T.line}`} center pad="16px 20px">
            <Txt s={38} al="center">{c[0]}</Txt><Txt s={26} w={500} c={T.ink3} al="center">{c[1]}</Txt>
            <div style={{height: b >= 1 ? 12 : 30}} />
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 14}}><Txt s={44} c={T.ink2}>{d.base}</Txt><Txt s={40} c={T.ink3}>→</Txt>
              <Txt s={b >= 1 ? 52 : 70} c={T.accent}>?</Txt></div>
          </Box>
        );
      })}
      {b < 1 ? <At x={160} y={Y0 + 360} w={1600} o={fade(f, 60, 10)}><Txt s={36} c={T.ink2} al="center">{d.q} — {d.qNote}</Txt></At> : null}
      {b >= 1 ? <Box x={160} y={Y0 + 290} w={1600} h={180} bg={T.ink} o={fade(f, at(d.at[1]), 10)} row pad="16px 40px">
        <svg width={120} height={90} viewBox="0 0 120 90"><path d="M8 52 L112 22 L104 12 L60 26 L34 6 L22 10 L40 32 L18 38 L10 30 L4 32 L10 48 Z" fill={T.daccent} /><rect x={8} y={74} width={104} height={6} rx={3} fill={T.dink3} /></svg>
        <div><Txt s={30} c={T.dink3}>{d.otherHead}</Txt><Txt s={58} c="#fff">{d.other}</Txt></div>
        <div style={{marginLeft: 'auto'}}><Txt s={32} c={T.daccent}>{d.otherSub}</Txt></div>
      </Box> : null}
    </>
  );
};

// ───────── 3. 번 몫 / 깎은 몫 폭포 막대 ─────────
const Waterfall: React.FC<{s: XScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const top = 440, bot = 760; const k = (bot - top) / (d.max - d.min); const Y = (v: number) => top + (d.max - v) * k; const zy = Y(0);
  const cw = 150, cg = 44; const gx = (g: number) => 250 + g * 800;
  const colX = (g: number, c: number) => gx(g) + c * (cw + cg);
  const nameY = Math.max(zy, Y(d.min)) + (d.min < 0 ? 34 : 14);
  return (
    <>
      {d.groups.map((g: any, gi: number) => {
        if (b < d.show[gi]) return null;
        const o = fade(f, at(d.at[d.show[gi]]), 10);
        const [gb, rb] = d.grow[gi]; const pg = b >= gb ? ease(f, at(d.at[gb]) + 6, 20) : 0;
        const pr = b >= rb ? ease(f, at(d.at[rb]) + (gb === rb ? 34 : 6), 20) : 0; const pk = b >= rb ? ease(f, at(d.at[rb]) + (gb === rb ? 58 : 30), 20) : 0;
        const yr = Y(g.r * pg); const yk = Y(g.r + (g.k - g.r) * pr); const yres = Y(g.k * pk);
        return (
          <React.Fragment key={gi}>
            <At x={gx(gi)} y={Y0 - 8} o={o}><div style={{display: 'flex', alignItems: 'baseline', gap: 16}}><Txt s={36}>{g.head}</Txt>
              {d.first && gi === 0 ? <div style={{background: T.accent, borderRadius: 10, padding: '4px 14px'}}><Txt s={26} c="#fff">{d.first}</Txt></div> : null}
              {d.calls.map((c: any[], ci: number) => s.key === 'wf2' && ci === 1 && c[1] === gi && b >= c[0] ? <div key={ci} style={{background: T.rise, borderRadius: 10, padding: '4px 14px', opacity: fade(f, at(d.at[c[0]]) + 10, 8)}}><Txt s={26} c="#fff">{c[2]}</Txt></div> : null)}
            </div></At>
            <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: o}}>
              <line x1={gx(gi) - 20} x2={colX(gi, 2) + cw + 20} y1={zy} y2={zy} stroke={T.ink} strokeWidth={3} strokeDasharray="10 8" />
              {pg > 0 && <rect x={colX(gi, 0)} y={Math.min(yr, zy)} width={cw} height={Math.abs(zy - yr)} rx={6} fill={GREEN} />}
              {pr > 0 && <line x1={colX(gi, 0) + cw} x2={colX(gi, 1)} y1={Y(g.r)} y2={Y(g.r)} stroke={T.ink3} strokeWidth={2} strokeDasharray="5 5" />}
              {pr > 0 && <rect x={colX(gi, 1)} y={Y(g.r)} width={cw} height={Math.max(0, yk - Y(g.r))} rx={6} fill={T.rise} />}
              {pk > 0 && <line x1={colX(gi, 1) + cw} x2={colX(gi, 2)} y1={Y(g.k)} y2={Y(g.k)} stroke={T.ink3} strokeWidth={2} strokeDasharray="5 5" />}
              {pk > 0 && <rect x={colX(gi, 2)} y={Math.min(yres, zy)} width={cw} height={Math.abs(zy - yres)} rx={6} fill={g.k < 0 ? T.ink : T.ink2} />}
            </svg>
            {pg > 0 ? <At x={colX(gi, 0) - 40} y={Y(g.r) - 44} w={cw + 80} o={fade(f, at(d.at[gb]) + 22, 8)}><Txt s={28} c={GREEN} al="center">{g.rText}</Txt></At> : null}
            {pr > 0.9 && g.gap ? <At x={colX(gi, 1) - 40} y={Y(g.k) + 8} w={cw + 80} o={fade(f, at(d.at[rb]) + (gb === rb ? 50 : 22), 8)}><Txt s={28} c={T.rise} al="center">−{g.gap}</Txt></At> : null}
            {pk > 0.9 ? <At x={colX(gi, 2) - 50} y={g.k >= 0 ? Y(g.k) - 44 : Y(g.k) + 8} w={cw + 100} o={fade(f, at(d.at[rb]) + (gb === rb ? 74 : 46), 8)}><Txt s={28} c={T.ink} al="center">{g.kText}</Txt></At> : null}
            {d.cols.map((c: string, ci: number) => <At key={ci} x={colX(gi, ci) - 24} y={nameY} w={cw + 48} o={o}><Txt s={23} w={700} c={ci === 0 ? GREEN : ci === 1 ? T.rise : T.ink2} al="center">{c}</Txt></At>)}
            <At x={gx(gi) - 120} y={zy - 18} w={92} o={o}><Txt s={28} c={T.ink} al="right">{d.base}</Txt></At>
          </React.Fragment>
        );
      })}
      {/* 말 속 금액(다른 묶음 빈 칸 위) */}
      {d.calls.map((c: any[], ci: number) => {
        if (s.key === 'wf2' && ci === 1) return null;
        const on = b === c[0]; if (!on) return null;
        const other = c[1] === 0 ? 1 : 0;
        const y = s.key === 'wf2' ? 600 : 392;
        return <div key={ci} style={{position: 'absolute', left: gx(other) - 20, width: 620, top: y + (1 - fade(f, at(d.at[c[0]]) + 12, 10)) * 12, opacity: fade(f, at(d.at[c[0]]) + 12, 10),
          textAlign: 'center'}}><span style={{...F, fontSize: 46, fontWeight: 700, color: '#fff', background: T.rise, borderRadius: 14, padding: '10px 26px', whiteSpace: 'nowrap'}}>{c[2]} {c[1] === 0 ? '←' : '→'}</span></div>;
      })}
    </>
  );
};

// ───────── 3. 주가 × 환율 ─────────
const Two: React.FC<{s: XScene}> = ({s}) => {
  const {f, total} = useBeat(s); const d = s.data;
  const t = (q: number) => Math.round(total * q);
  const card = (x: number, c: string[], bg: string, o: number) => <Box x={x} y={Y0 + 50} w={420} h={260} bg={bg} o={o}><Txt s={70} c="#fff" al="center">{c[0]}</Txt><Txt s={30} c="#ffffffcc" al="center">{c[1]}</Txt></Box>;
  return (
    <>
      {card(200, d.a, GREEN, fade(f, 4, 10))}
      <At x={640} y={Y0 + 130} w={110} o={fade(f, t(0.2), 8)}><Txt s={90} c={T.ink3} al="center">×</Txt></At>
      {card(760, d.b, T.rise, fade(f, t(0.2), 10))}
      <At x={1200} y={Y0 + 130} w={110} o={fade(f, t(0.42), 8)}><Txt s={90} c={T.ink3} al="center">=</Txt></At>
      <Box x={1320} y={Y0 + 50} w={440} h={260} bg={T.ink} o={fade(f, t(0.42), 10)}><Txt s={60} c="#fff" al="center">{d.eq}</Txt></Box>
      <At x={200} y={Y0 + 360} w={1560} o={fade(f, t(0.62), 10)}><Txt s={48} c={T.ink} al="center">{d.tail}</Txt></At>
      {f >= t(0.62) ? <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}><HandCircle cx={980} cy={Y0 + 390} rx={560} ry={62} p={ease(f, t(0.66), 16)} /></svg> : null}
    </>
  );
};

// ───────── 4. 은행 창구 + 고시판 ─────────
const Bank: React.FC<{s: XScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const row = (y: number, t: string, o: number, hot: boolean) => (
    <div style={{position: 'absolute', left: 860, top: y + (1 - o) * 10, width: 860, height: 96, opacity: o, background: hot ? T.dsurface : '#24262c', borderRadius: 14, display: 'flex', alignItems: 'center', padding: '0 30px', boxSizing: 'border-box'}}>
      <Txt s={44} c={hot ? T.daccent : '#fff'}>{t}</Txt>
    </div>
  );
  return (
    <>
      {/* 창구 그림(상표 없음) */}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}} opacity={fade(f, 0, 12)}>
        <rect x={170} y={370} width={560} height={300} rx={18} fill={T.bg} stroke={T.line} strokeWidth={4} />
        <rect x={230} y={410} width={200} height={170} rx={10} fill="#dfe7f3" /><rect x={470} y={410} width={200} height={170} rx={10} fill="#dfe7f3" />
        <circle cx={330} cy={480} r={30} fill={T.ink3} /><rect x={290} y={515} width={80} height={65} rx={30} fill={T.ink3} />
        <rect x={150} y={600} width={600} height={46} rx={8} fill={T.ink2} /><rect x={150} y={646} width={600} height={150} rx={8} fill={T.ink} />
        <rect x={520} y={555} width={120} height={64} rx={6} fill="#e6e9ee" stroke={GREEN} strokeWidth={4} /><circle cx={580} cy={587} r={16} fill="none" stroke={GREEN} strokeWidth={4} />
      </svg>
      <At x={170} y={810} w={560}><Txt s={26} w={500} c={T.ink3} al="center">{d.counter}</Txt></At>
      {/* 고시판 */}
      <div style={{position: 'absolute', left: 820, top: Y0, width: 940, height: 470, background: T.dbg, borderRadius: 22, opacity: fade(f, 4, 10)}} />
      {b >= 1 ? row(Y0 + 40, d.buy, fade(f, at(d.at[1]), 10), b === 1) : null}
      {row(Y0 + 190, d.mid, fade(f, 10, 10), b === 0)}
      {b >= 1 ? <At x={1400} y={Y0 + 150} o={fade(f, at(d.at[1]) + 14, 8)}><Txt s={30} c={T.daccent}>↑ {d.pricier}</Txt></At> : null}
      {b >= 2 ? <>
        <div style={{position: 'absolute', left: 1640, top: Y0 + 70, width: 24, height: 168, borderRight: `6px solid ${T.daccent}`, borderTop: `6px solid ${T.daccent}`, borderBottom: `6px solid ${T.daccent}`, borderRadius: '0 10px 10px 0', opacity: fade(f, at(d.at[2]), 8)}} />
        <Box x={860} y={Y0 + 320} w={860} h={120} bg={T.accent} o={fade(f, at(d.at[2]) + 10, 10)} row pad="10px 30px"><Txt s={44} c="#fff">{d.fee}</Txt><Txt s={36} c="#fff">= {d.pref}</Txt></Box>
      </> : null}
    </>
  );
};

// ───────── 4. 계산 밖 카드 ─────────
const Note: React.FC<{s: XScene}> = ({s}) => {
  const {f, total} = useBeat(s); const d = s.data; const m = Math.round(total * d.mid);
  const two = f >= m;
  return (
    <>
      <Box x={160} y={Y0} w={two ? 760 : 1600} h={two ? 300 : 340} bg={two ? '#fff' : T.ink} border={two ? `3px solid ${T.line}` : undefined} o={fade(f, 0, 10)} pad="24px 40px">
        <Txt s={two ? 34 : 50} c={two ? T.ink2 : T.dink3} wrap>{d.c1[0]}</Txt><div style={{height: 14}} /><Txt s={two ? 40 : 60} c={two ? T.ink : '#fff'} wrap>{d.c1[1]}</Txt>
      </Box>
      {two ? <Box x={960} y={Y0} w={800} h={300} bg={T.ink} o={fade(f, m, 10)} pad="24px 40px">
        <Txt s={34} c={T.dink3}>{d.c2[0]}</Txt><div style={{height: 14}} /><Txt s={52} c="#fff">{d.c2[1]}</Txt>
      </Box> : null}
      {two ? <Box x={160} y={Y0 + 340} w={1600} h={130} bg={T.soft} o={fade(f, m + 40, 10)} row pad="10px 40px">
        <Txt s={60} c={T.rise}>↓</Txt><Txt s={50} c={T.ink}>{d.c3}</Txt></Box> : null}
    </>
  );
};

// ───────── 5. 시소 ─────────
const Seesaw: React.FC<{s: XScene}> = ({s}) => {
  const {f, total} = useBeat(s); const d = s.data; const m = Math.round(total * d.mid);
  const rOn = d.both ? fade(f, 4, 10) : fade(f, m, 10);
  const tilt = (d.both ? ease(f, 10, 30) : ease(f, m + 6, 30)) * 9;
  const cx = 960, cy = 640, arm = 560; const rad = tilt * Math.PI / 180;
  const ly = cy + arm * Math.sin(rad), ry = cy - arm * Math.sin(rad);
  const tagOn = d.both ? fade(f, m, 10) : 0;
  const by = (x: number) => cy + (cx - x) * Math.tan(rad);   // 막대 위 y(왼쪽이 내려감)
  const card = (x: number, _y: number, t: string[], c: string, o: number, arrow: string) => o <= 0 ? null : (
    <div style={{position: 'absolute', left: x - 270, top: Math.min(by(x - 270), by(x + 270)) - 194 + (1 - o) * 10, width: 540, height: 170, opacity: o, background: '#fff', border: `4px solid ${c}`, borderRadius: 20, boxSizing: 'border-box', padding: '18px 26px'}}>
      <Txt s={36} c={T.ink}>{t[0]}</Txt><div style={{height: 10}} /><Txt s={40} c={c}>{arrow} {t[1]}</Txt>
    </div>
  );
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <polygon points={`${cx},${cy} ${cx - 70},${cy + 170} ${cx + 70},${cy + 170}`} fill={T.ink2} />
        <line x1={cx - arm * Math.cos(rad)} y1={ly} x2={cx + arm * Math.cos(rad)} y2={ry} stroke={T.ink} strokeWidth={14} strokeLinecap="round" />
      </svg>
      {card(cx - arm * Math.cos(rad) + 90, ly, d.L, T.rise, fade(f, 0, 10), '↓')}
      {card(cx + arm * Math.cos(rad) - 90, ry, d.R, T.fall, rOn, '↑')}
      {tagOn > 0 ? <>
        <Pill x={cx - arm + 20} y={ly + 30} o={tagOn} bg={T.rise} s={36}>{d.tagL}</Pill>
        <Pill x={cx + arm - 140} y={ry + 30} o={fade(f, m + 10, 10)} bg={T.fall} s={36}>{d.tagR}</Pill>
      </> : null}
    </>
  );
};

// ───────── 5. 결제 카드 + 굴림 숫자 ─────────
const Cards: React.FC<{s: XScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  if (b < 1) return (
    <>
      <div style={{position: 'absolute', left: 560, top: Y0 + 30 + (1 - fade(f, 0, 12)) * 14, width: 800, height: 330, opacity: fade(f, 0, 12), background: '#ffffff', border: `6px solid ${GREEN}`, borderRadius: 24,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', boxSizing: 'border-box'}}>
        <Txt s={110} c={GREEN} al="center">{d.bill}</Txt><Txt s={36} c={T.ink2} al="center">{d.billSub}</Txt>
      </div>
    </>
  );
  const card = (i: number, c: string[]) => {
    const x = 160 + i * 880; const o = fade(f, at(d.at[1]) + i * 30, 10);
    return (
      <div key={i} style={{position: 'absolute', left: x, top: Y0 + (1 - o) * 12, width: 720, height: 270, opacity: o, background: i ? T.ink : '#2a2c33', borderRadius: 26, padding: '26px 36px', boxSizing: 'border-box'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 18}}><div style={{width: 70, height: 50, borderRadius: 8, background: '#d9b25c'}} /><Txt s={40} c="#fff">{c[0]}</Txt><Txt s={28} c={T.dink3}>· {c[1]}</Txt></div>
        <div style={{marginTop: 34}}><RollNumber text={c[2]} size={86} color={i ? T.daccent : '#fff'} font="PD" seed={'X-1-card' + i} start={at(d.at[1]) + i * 30 + 6} /></div>
      </div>
    );
  };
  return (
    <>
      {d.c.map((c: string[], i: number) => card(i, c))}
      <At x={880} y={Y0 + 90} w={160} o={fade(f, at(d.at[1]) + 30, 8)}><Txt s={70} c={T.ink3} al="center">→</Txt></At>
      <Pill x={780} y={Y0 + 300} o={fade(f, at(d.at[1]) + 60, 10)} bg={T.fall} s={40}>{d.diff}</Pill>
      {b >= 2 ? <Box x={160} y={Y0 + 400} w={1600} h={100} bg={T.soft} o={fade(f, at(d.at[2]), 10)} row pad="8px 36px">
        <Txt s={38} c={T.ink}>{d.c3[0]}</Txt><Txt s={30} c={T.ink2}>{d.c3[1]}</Txt><Txt s={44} c={T.fall}>{d.c3[2]}</Txt></Box> : null}
    </>
  );
};

// ───────── 5. 엔화 선 + 계수기 ─────────
const Yen: React.FC<{s: XScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data; const b = beatOf(d.at, at, f);
  const n = d.vals.length; const sh = b >= 1 ? ease(f, at(d.at[1]), 20) : 0;
  const X0 = 280, X1 = 1460 - sh * 480, YT = 420, YB = 760;
  const X = (i: number) => X0 + i / (n - 1) * (X1 - X0); const Y = (v: number) => YB - (v - d.min) / (d.max - d.min) * (YB - YT);
  const p = ease(f, 4, 70); const m = Math.max(1, Math.round(p * (n - 1)));
  const path = d.vals.slice(0, m + 1).map((v: number, i: number) => `${i ? 'L' : 'M'}${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' ');
  const ex = X(n - 1), ey = Y(d.vals[n - 1]); const jx = X(d.hi7), jy = Y(d.vals[d.hi7]);
  const k = d.k; const ko = fade(f, at(d.at[1]) + 14, 10);
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {d.yt.map(([v]: [number, string], i: number) => <line key={i} x1={X0} x2={X1 + 10} y1={Y(v)} y2={Y(v)} stroke={T.line} strokeWidth={2} />)}
        <path d={path} fill="none" stroke={T.ink2} strokeWidth={4} strokeLinejoin="round" />
        {p >= 1 && <circle cx={ex} cy={ey} r={12} fill={T.fall} stroke="#fff" strokeWidth={4} />}
        {b >= 1 && <circle cx={jx} cy={jy} r={12} fill={T.ink} stroke="#fff" strokeWidth={4} opacity={ko} />}
      </svg>
      <At x={X0} y={YT - 66}><Txt s={30} c={T.ink2}>{d.name}</Txt></At>
      {d.yt.map(([v, t]: [number, string], i: number) => <At key={i} x={X0 - 140} y={Y(v) - 16} w={120}><Txt s={24} w={500} c={T.ink3} al="right">{t}</Txt></At>)}
      {d.xl.map(([i, t]: [number, string], j: number) => (j === d.xl.length - 1 || X(d.xl[d.xl.length - 1][0]) - X(i) > 90) ? <At key={j} x={X(i) - 50} y={YB + 14} w={100}><Txt s={24} w={500} c={T.ink3} al={j === d.xl.length - 1 ? 'center' : 'left'}>{t}</Txt></At> : null)}
      {p >= 1 ? <At x={ex - 320} y={ey + 10} w={300} o={fade(f, 74, 8)}><Txt s={28} c={T.fall} al="right">{d.endText}</Txt></At> : null}
      {p >= 1 && b < 1 ? <Pill x={ex - 560} y={430} o={fade(f, 84, 10)} bg={T.fall} s={34}>{d.lowTag} ↘</Pill> : null}
      {b >= 1 ? <At x={jx - 60} y={jy - 52} w={120} o={ko}><Txt s={28} c={T.ink} al="center">{d.jul}</Txt></At> : null}
      {b >= 1 ? <div style={{position: 'absolute', left: 1120, top: Y0 + (1 - ko) * 12, width: 650, height: 480, opacity: ko, background: T.ink, borderRadius: 24, padding: '28px 40px', boxSizing: 'border-box'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 16}}><div style={{width: 64, height: 40, borderRadius: 6, background: '#c9b28a', ...F, fontSize: 28, fontWeight: 700, color: T.ink, textAlign: 'center', lineHeight: '40px'}}>¥</div><Txt s={38} c="#fff">{k[0]}</Txt></div>
        <div style={{marginTop: 34, display: 'flex', alignItems: 'baseline', gap: 24}}><Txt s={32} c={T.dink3}>{k[1]}</Txt><RollNumber text={k[2]} size={64} color={T.dink3} font="PD" seed="X-1-yen0" start={at(d.at[1]) + 20} /></div>
        <div style={{marginTop: 18, display: 'flex', alignItems: 'baseline', gap: 24, opacity: fade(f, at(d.at[1]) + 70, 10)}}><Txt s={32} c="#fff">{k[3]}</Txt><RollNumber text={k[4]} size={80} color="#fff" font="PD" seed="X-1-yen1" start={at(d.at[1]) + 72} /></div>
        <div style={{marginTop: 22, display: 'inline-block', background: T.dfall, borderRadius: 12, padding: '6px 18px', opacity: fade(f, at(d.at[1]) + 110, 10)}}><Txt s={36} c="#fff">{k[5]}</Txt></div>
      </div> : null}
    </>
  );
};

// ───────── 6. 지난 편 타일 ─────────
const Prev: React.FC<{s: XScene}> = ({s}) => {
  const {f, total} = useBeat(s); const d = s.data; const q1 = Math.round(total * d.q1), m = Math.round(total * d.mid);
  return (
    <>
      <At x={160} y={Y0 - 4} o={fade(f, 0, 10)}><Txt s={30} c={T.ink3}>{d.head}</Txt></At>
      {d.tiles.map((t: any[], i: number) => {
        const o = fade(f, 6 + i * 8, 10); const etf = t[1] === 1 && f >= q1;
        return <Box key={i} x={160 + i * 405} y={Y0 + 50} w={380} h={180} bg={etf ? T.ink : '#fff'} border={etf ? undefined : `3px solid ${T.line}`} o={o}>
          <Txt s={50} c={etf ? '#fff' : T.ink} al="center">{t[0]}</Txt>{etf ? <Txt s={26} c={T.daccent} al="center">{d.etf}</Txt> : null}</Box>;
      })}
      {f >= q1 ? <>
        <div style={{position: 'absolute', left: 565 + 20, top: Y0 + 250, width: 3 * 405 - 45, height: 30, borderLeft: `6px solid ${T.rise}`, borderRight: `6px solid ${T.rise}`, borderBottom: `6px solid ${T.rise}`, borderRadius: '0 0 12px 12px', opacity: fade(f, q1, 8)}} />
        <At x={565} y={Y0 + 296} w={3 * 405 - 25} o={fade(f, q1 + 10, 8)}><Txt s={40} c={T.rise} al="center">{d.cut}</Txt></At>
      </> : null}
      {f >= m ? <Box x={160} y={Y0 + 370} w={1600} h={120} bg={T.accent} o={fade(f, m, 10)} row pad="10px 40px"><Txt s={36} c="#fff">{d.now}</Txt><Txt s={56} c="#fff">{d.nowBig}</Txt></Box> : null}
    </>
  );
};

// ───────── 6. 끝 표(20초: 6~7초마다 판이 바뀐다) ─────────
const TW = [300, 260, 300, 330, 330]; const TX0 = 220; const TRH = 78;
const txs = TW.map((_, i) => TX0 + TW.slice(0, i).reduce((a, v) => a + v, 0));
const Table: React.FC<{s: XScene}> = ({s}) => {
  const {f} = useBeat(s); const d = s.data; const sp = s.lines[0].frames;
  const ph = f < sp ? 0 : f < sp + 205 ? 1 : 2;
  const dim = ph === 1 ? 0.25 : 1;
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, opacity: dim}}>
        {d.cols.map((c: string, i: number) => <At key={i} x={txs[i]} y={Y0 - 4} w={TW[i]}><Txt s={28} c={T.ink3} al="center">{c}</Txt></At>)}
        {d.rows.map((r: string[], ri: number) => {
          const cells = [r[0] + ' ' + r[1], r[2], r[3], r[4], r[5]];
          return cells.map((v: string, ci: number) => {
            const neg = v.startsWith('−') && ci >= 2;
            return <div key={ri + '-' + ci} style={{position: 'absolute', left: txs[ci] + 4, top: Y0 + 40 + ri * TRH, width: TW[ci] - 8, height: TRH - 10, borderRadius: 10, opacity: fade(f, 6 + ri * 6 + ci * 3, 10),
              background: ri % 2 ? '#fff' : T.bg, border: ri % 2 ? `2px solid ${T.line}` : 'none', boxSizing: 'border-box', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <Txt s={ci === 0 ? 27 : 34} c={ci === 0 ? T.ink : neg ? T.rise : ci >= 2 ? T.fall : T.ink2}>{v}</Txt></div>;
          });
        })}
        <At x={TX0} y={Y0 + 40 + 4 * TRH + 6} w={1520}><Txt s={28} c={T.ink2} al="right">{d.endRate}</Txt></At>
      </div>
      {ph === 0 ? <Box x={TX0} y={Y0 + 410} w={1520} h={80} bg={T.ink} o={fade(f, 30, 10)} row pad="8px 30px"><Txt s={40} c="#fff">{d.q}</Txt><Txt s={34} c={T.daccent}>{d.ask[0]}</Txt></Box> : null}
      {ph === 1 ? <Box x={360} y={Y0 + 40} w={1200} h={400} bg={T.ink} o={fade(f, sp, 10)}>
        <Txt s={64} c="#fff" al="center">{d.q}</Txt><div style={{height: 26}} /><Txt s={42} c={T.daccent} al="center">{d.ask[0]}</Txt><div style={{height: 10}} /><Txt s={36} c={T.dink3} al="center">{d.ask[1]}</Txt></Box> : null}
      {ph === 2 ? <>
        <Box x={TX0} y={Y0 + 410} w={760} h={80} bg={T.accent} o={fade(f, sp + 205, 10)} row pad="8px 30px"><Txt s={40} c="#fff">{d.cafe[0]}</Txt><Txt s={36} c="#fff">→ {d.cafe[1]}</Txt></Box>
        <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}><HandCircle cx={TX0 + 380} cy={Y0 + 450} rx={420} ry={62} p={ease(f, sp + 220, 16)} /></svg>
      </> : null}
    </>
  );
};

const Body: React.FC<{s: XScene}> = ({s}) => {
  switch (s.kind) {
    case 'twoline': return <TwoLine s={s} />;
    case 'promise': return <DateCards s={s} />;
    case 'fxline': case 'fxbars': return <FxDates {...(s.data as FxDatesProps)} />;
    case 'wf': return <Waterfall s={s} />;
    case 'two': return <Two s={s} />;
    case 'bank': return <Bank s={s} />;
    case 'band': { const st = tallyStarts(s.lines); return <SpreadBand {...s.data} beats={s.data.at.map((i: number) => st[i])} />; }
    case 'note': return <Note s={s} />;
    case 'seesaw': return <Seesaw s={s} />;
    case 'cards': return <Cards s={s} />;
    case 'yen': return <Yen s={s} />;
    case 'prev': return <Prev s={s} />;
    case 'table': return <Table s={s} />;
    default: return null;
  }
};

// 정확한 값 칩 — T1과 같음(40자 넘으면 ' · ' 마디로 나눠 차례로). 마디 하나가 길면(원문 인용) 두 줄로 감싼다.
const CHIP_MAX = 40;
const chipPages = (cap: string) => {
  // ' / '로 나뉜 항목을 먼저 지키고, 항목 하나가 길면 그 안을 ' · '로 나눈다. [앞 구분자, 글] 쌍.
  const parts: [string, string][] = cap.includes(' / ')
    ? cap.split(' / ').flatMap((q) => q.length > 56 ? q.split(' · ').map((x, i) => [i ? ' · ' : ' / ', x] as [string, string]) : [[' / ', q] as [string, string]])
    : cap.split(' · ').map((x) => [' · ', x] as [string, string]);
  const out: string[] = []; let cur = '';
  for (const [sep, p] of parts) { const nx = cur ? cur + sep + p : p; if (cur && nx.length > CHIP_MAX && cur.length >= 12) { out.push(cur); cur = p; } else cur = nx; }
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
  const long = pages[pi].length > 56;
  return (
    <div style={{position: 'absolute', left: 130, top: 252, maxWidth: 1660, opacity: co, transform: `translateY(${(1 - co) * -8}px)`,
      background: T.ink, borderRadius: 10, padding: '7px 16px', display: 'flex', gap: 12, alignItems: 'baseline'}}>
      <span style={{...F, fontWeight: 700, fontSize: 20, color: T.daccent, whiteSpace: 'nowrap'}}>{/\d/.test(cap) ? '정확한 값' : '원문'}{pages.length > 1 ? ` ${pi + 1}/${pages.length}` : ''}</span>
      <span style={{...F, fontWeight: 700, fontSize: long ? 23 : 26, color: '#fff', lineHeight: 1.3, whiteSpace: long ? 'normal' : 'nowrap', wordBreak: 'keep-all'}}>{pages[pi]}</span>
    </div>
  );
};

const SceneView: React.FC<{s: XScene; last: boolean}> = ({s, last}) => {
  const st = tallyStarts(s.lines);
  return (
    <AbsoluteFill>
      <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines.map((l) => ({...l, cap: null}))} board capX={last ? 760 : 960}>
        <Body s={s} />
        <Chip lines={s.lines} />
      </TallyFrame>
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </AbsoluteFill>
  );
};

export const X1: React.FC<X1Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} last={i === p.scenes.length - 1} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
