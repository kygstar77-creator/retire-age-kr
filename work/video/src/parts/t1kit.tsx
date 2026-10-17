// T-1 양도세 편 판 부품(10/17 PD, T1.tsx v4.1에서 처음) — 글자·숫자는 전부 props(t1.json, ep/T-1/t1props.py가 calc·대본과 기계 대조)에서 온다.
// TallyFrame(10/17 롱폼 화면 기준: 큰 제목·art·출처·정확한 값 칸) 안에 그리는 판 9종:
//   Table(연도 칸 표 · 줄마다 한 칸 켜짐) · Cells(해마다 칸 10개 두 줄 — 공제율 계단) · Price(판 값 막대 · 기준 12억 회색 / 번 돈 12억 파랑, 색을 달리)
//   Cal(석 달 달력 · 잔금일 → 그달 말일 → 두 달 뒤 말일) · Zones(지도 두 칸 · 조정/조정 아님 → 기한) · Memo(메모 세 줄)
//   Stairs(세율 계단 8칸 · 한 사람 몫 vs 반씩 나눈 몫) · Band(관리처분 인가 → 공사 기간 → 입주 띠 · 절반에 색) · Five(갈래 다섯 줄 · 지금 줄만 켜짐)
// 다른 세금·제도 편에서 그대로 쓴다(장면 data 모양은 t1props.py 참고). 칸 안 숫자(날짜 칸 번호 등)는 그리지 않는다 — 숫자는 props 글자만.
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import * as Lucide from 'lucide-react';
import {T, F, CL} from './fm';
import {TallyFrame, TallyLine, TallyArt} from '../motion/TallyFrame';

export type KLine = {text: string; audio: string; frames: number; cap?: string | null};
export type KScene = {kind: string; lines: KLine[]; frames: number; data: any};
const COL: Record<string, string> = {accent: T.accent, fall: T.fall, rise: T.rise, ink: T.ink};
export const kcol = (c?: string) => COL[c || 'ink'] || T.ink;
const out = Easing.out(Easing.cubic);
export const kease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
export const kstarts = (ls: KLine[]) => { const o: number[] = []; let a = 0; for (const l of ls) { o.push(a); a += l.frames; } return o; };
export const klineAt = (ls: KLine[], f: number) => { const st = kstarts(ls); let k = 0; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };
export const katLine = (ls: KLine[], i?: number | null) => { const st = kstarts(ls); if (i == null) return 4; return i >= st.length ? st[st.length - 1] + ls[st.length - 1].frames / 2 : st[i] + 4; };
export const ktl = (ls: KLine[]): TallyLine[] => ls.map(l => ({text: l.text.replace(/^"|"$/g, ''), frames: l.frames, cap: l.cap ?? null}));
export const kart = (icon?: string, color?: string): TallyArt | null => icon ? {kind: 'icon', icon, license: 'lucide ISC', color} : null;
const Icon: React.FC<{name: string; size: number; color: string}> = ({name, size, color}) => {
  const I = (Lucide as unknown as Record<string, React.FC<{size?: number; color?: string; strokeWidth?: number}>>)[name];
  return I ? <I size={size} color={color} strokeWidth={2.4} /> : null;
};
const Frame: React.FC<{s: KScene; children: React.ReactNode}> = ({s, children}) => (
  <TallyFrame title={s.data.title} art={kart(s.data.icon)} source={s.data.source} chapter={s.data.chapter} lines={ktl(s.lines)}>{children}</TallyFrame>
);

// ───────── Table: 연도 칸 표 ─────────
export const KTable: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const cols: string[] = d.cols; const rows: string[][] = d.rows;
  const k = klineAt(s.lines, f); const lit: number = (d.lit as number[])[k] ?? -1;
  const X0 = 200, LW = 420, CW = 400, Y0 = 340, HH = 110, RH = 170;
  return (
    <Frame s={s}>
      {lit >= 0 ? <div style={{position: 'absolute', left: X0 + LW + lit * CW, top: Y0 - 6, width: CW - 16, height: HH + RH * rows.length + 6, background: T.soft, borderRadius: 22}} /> : null}
      {cols.map((c, j) => <div key={j} style={{position: 'absolute', left: X0 + LW + j * CW, width: CW - 16, top: Y0, height: HH, display: 'flex', alignItems: 'center', justifyContent: 'center',
        ...F, fontWeight: 700, fontSize: 50, color: j === lit ? T.accent : T.ink2, whiteSpace: 'nowrap'}}>{c}</div>)}
      {rows.map((r, i) => { const o = kease(f, 4 + i * 8, 12); return (
        <div key={i} style={{position: 'absolute', left: X0, top: Y0 + HH + i * RH, width: LW + CW * cols.length - 16, height: RH - 14, opacity: o, borderTop: `2px solid ${T.line}`}}>
          <div style={{position: 'absolute', left: 10, top: 0, height: RH - 14, display: 'flex', alignItems: 'center', ...F, fontWeight: 700, fontSize: 52, color: T.ink, whiteSpace: 'nowrap'}}>{r[0]}</div>
          {r.slice(1).map((v, j) => { const on = j <= Math.max(lit, 0) || lit < 0; return <div key={j} style={{position: 'absolute', left: LW + j * CW, width: CW - 16, top: 0, height: RH - 14,
            display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 800, fontSize: j === lit ? 104 : 84, letterSpacing: -2,
            color: j === lit ? (i === 0 ? T.accent : T.ink) : T.ink2, opacity: on ? 1 : 0.35, whiteSpace: 'nowrap'}}>{v}</div>; })}
        </div>); })}
    </Frame>
  );
};

// ───────── Cells: 해마다 칸 10개 두 줄 ─────────
export const KCells: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows: [string, string, number, string, number?][] = d.rows;
  return (
    <Frame s={s}>
      {rows.map(([label, sub, n, c, a], i) => { const st = katLine(s.lines, a); const y = 360 + i * 210;
        return <div key={i} style={{position: 'absolute', left: 170, top: y, width: 1600, height: 180}}>
          <div style={{position: 'absolute', left: 0, top: 18, width: 420}}>
            <div style={{...F, fontWeight: 800, fontSize: 56, color: T.ink, whiteSpace: 'nowrap'}}>{label}</div>
            <div style={{...F, fontWeight: 700, fontSize: 40, color: kcol(c), marginTop: 6, whiteSpace: 'nowrap'}}>{sub}</div>
          </div>
          {Array.from({length: n}).map((_, j) => { const p = kease(f, st + j * 5, 8);
            return <div key={j} style={{position: 'absolute', left: 440 + j * 112, top: 20, width: 100, height: 130, borderRadius: 14, border: `3px solid ${p > 0.5 ? kcol(c) : T.line}`,
              background: kcol(c), opacity: 0.12 + 0.88 * p, transform: `scaleY(${0.7 + 0.3 * p})`}} />; })}
        </div>; })}
      {d.total ? <div style={{position: 'absolute', left: 0, width: 1920, top: 790, textAlign: 'center', opacity: kease(f, katLine(s.lines, s.lines.length - 1), 12), ...F, fontWeight: 700, fontSize: 40, color: T.ink2}}>{d.total}</div> : null}
    </Frame>
  );
};

// ───────── Price: 판 값 막대(기준 12억 회색 · 넘는 몫 주황) + 산 값/번 돈 막대(번 돈 파랑) ─────────
export const KPrice: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const X = 220, W = 1480; const cut = X + W * 0.6; const two = d.step >= 2;
  const a1 = kease(f, 4, 18); const a2 = kease(f, two ? 4 : katLine(s.lines, 1), 16); const a3 = kease(f, katLine(s.lines, 0) + 10, 16); const a4 = kease(f, katLine(s.lines, 1), 16);
  const y1 = two ? 405 : 440; const y2 = 640;
  return (
    <Frame s={s}>
      <div style={{position: 'absolute', left: X, top: y1 - 70, ...F, fontWeight: 700, fontSize: 46, color: T.ink, opacity: a1}}>{d.sell}</div>
      <div style={{position: 'absolute', left: X, top: y1, width: (cut - X) * a1, height: 110, background: '#c9ced6', borderRadius: '18px 0 0 18px'}} />
      <div style={{position: 'absolute', left: cut, top: y1, width: (X + W - cut) * a2, height: 110, background: T.accent, borderRadius: '0 18px 18px 0'}} />
      <div style={{position: 'absolute', left: cut - 2, top: y1 - 24, height: 158, borderLeft: `5px dashed ${T.ink}`, opacity: a1}} />
      <div style={{position: 'absolute', left: cut - 380, width: 360, top: y1 + 24, textAlign: 'right', ...F, fontWeight: 800, fontSize: 56, color: T.ink, opacity: a1}}>{d.line}</div>
      <div style={{position: 'absolute', left: cut + 20, width: X + W - cut - 30, top: y1 + 124, ...F, fontWeight: 700, fontSize: 44, color: T.accent, opacity: a2, whiteSpace: 'nowrap'}}>{d.over}</div>
      {two ? <>
        <div style={{position: 'absolute', left: X, top: y2, width: W * 0.4 * a3, height: 110, background: '#eceef2', border: `2px solid ${T.line}`, borderRadius: '18px 0 0 18px'}} />
        <div style={{position: 'absolute', left: X + 20, top: y2 + 28, ...F, fontWeight: 700, fontSize: 46, color: T.ink2, opacity: a3}}>{d.buy}</div>
        <div style={{position: 'absolute', left: X + W * 0.4, top: y2, width: W * 0.6 * a3, height: 110, background: T.fall, borderRadius: '0 18px 18px 0'}} />
        <div style={{position: 'absolute', left: X + W * 0.4 + 24, top: y2 + 22, ...F, fontWeight: 800, fontSize: 56, color: '#fff', opacity: a3, whiteSpace: 'nowrap'}}>{d.gain}</div>
        <div style={{position: 'absolute', left: X + W - W * 0.6 * 0.4, top: y2 - 10, width: W * 0.6 * 0.4, height: 130, border: `6px solid ${T.ink}`, borderRadius: 18, opacity: a4,
          background: 'repeating-linear-gradient(45deg, rgba(255,255,255,0.35) 0 12px, rgba(255,255,255,0) 12px 24px)'}} />
        <div style={{position: 'absolute', left: X + W - 560, width: 560, top: y2 + 128, textAlign: 'right', ...F, fontWeight: 800, fontSize: 50, color: T.ink, opacity: a4, whiteSpace: 'nowrap'}}>{d.taxed}</div>
      </> : null}
    </Frame>
  );
};

// ───────── Cal: 석 달 달력(칸 번호 없이) ─────────
export const KCal: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const at: number[] = d.at; const months: string[] = d.months;
  const aE = kease(f, katLine(s.lines, at[0]) + 8, 14), aC = kease(f, katLine(s.lines, at[1]), 14), aP = kease(f, katLine(s.lines, at[2]), 14), aX = kease(f, katLine(s.lines, at[3]), 14);
  const MX = [210, 720, 1230], MW = 470, CY = 420, CS = 62, G = 4;
  const cell = (m: number, r: number, c: number) => ({left: MX[m] + 12 + c * (CS + G), top: CY + r * (CS + G)});
  const last = (m: number) => cell(m, 4, m === 1 ? 3 : 4);
  return (
    <Frame s={s}>
      {months.map((mn, m) => <div key={m}>
        <div style={{position: 'absolute', left: MX[m], width: MW, top: 330, textAlign: 'center', ...F, fontWeight: 800, fontSize: 62, color: m === 2 && aX > 0.5 ? T.rise : T.ink}}>{mn}</div>
        {Array.from({length: 35}).map((_, i) => { const r = Math.floor(i / 7), c = i % 7; const p = cell(m, r, c);
          return <div key={i} style={{position: 'absolute', ...p, width: CS, height: CS, borderRadius: 10, background: '#f1f3f6', border: `1px solid ${T.line}`}} />; })}
      </div>)}
      <div style={{position: 'absolute', ...cell(0, 2, 2), width: CS, height: CS, borderRadius: CS / 2, background: T.ink, opacity: aP, transform: `scale(${0.6 + 0.4 * aP})`}} />
      <div style={{position: 'absolute', left: cell(0, 2, 2).left - 40, top: cell(0, 2, 2).top - 54, ...F, fontWeight: 700, fontSize: 36, color: T.ink, opacity: aP, whiteSpace: 'nowrap', background: '#fff', padding: '0 8px'}}>{d.pay}</div>
      <div style={{position: 'absolute', ...last(0), width: CS, height: CS, borderRadius: 10, background: T.accent, opacity: aE}} />
      <div style={{position: 'absolute', ...last(2), width: CS, height: CS, borderRadius: 10, background: T.rise, opacity: aE}} />
      <div style={{position: 'absolute', left: last(0).left - 120, top: last(0).top + CS + 14, ...F, fontWeight: 700, fontSize: 36, color: T.accent, opacity: aE, whiteSpace: 'nowrap'}}>{d.end1}</div>
      <div style={{position: 'absolute', left: last(2).left - 120, top: last(2).top + CS + 14, ...F, fontWeight: 700, fontSize: 36, color: T.rise, opacity: aE, whiteSpace: 'nowrap'}}>{d.end2}</div>
      <div style={{position: 'absolute', left: last(0).left + CS + 10, top: last(0).top + CS / 2 - 3, width: (last(2).left - last(0).left - CS - 20) * aE, height: 6, background: T.ink, borderRadius: 3}} />
      {d.chip ? <div style={{position: 'absolute', left: 740, width: 440, top: 806, textAlign: 'center', opacity: aC, transform: `scale(${0.85 + 0.15 * aC})`}}>
        <span style={{...F, fontWeight: 800, fontSize: 40, color: '#fff', background: T.ink, borderRadius: 12, padding: '2px 24px', whiteSpace: 'nowrap'}}>{d.chip}</span></div> : null}
      {d.ex ? <div style={{position: 'absolute', left: MX[2], width: MW, top: 326, height: 432, border: `5px solid ${T.rise}`, borderRadius: 22, opacity: aX}} /> : null}
      {d.ex ? <div style={{position: 'absolute', left: MX[2] + 110, top: 806, ...F, fontWeight: 800, fontSize: 38, color: '#fff', background: T.rise, borderRadius: 14, padding: '2px 22px', opacity: aX, whiteSpace: 'nowrap'}}>{d.ex}</div> : null}
    </Frame>
  );
};

// ───────── Zones: 지도 두 칸 → 기한 ─────────
export const KZones: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const both = d.mode === 'both';
  const tile = (x: number, name: string, on: boolean, a: number) => {
    const o = kease(f, a, 14);
    return <div style={{position: 'absolute', left: x, top: 350, width: 440, height: 380, borderRadius: 26, opacity: o, overflow: 'hidden',
      background: on ? '#fff1e8' : '#f1f3f6', border: `4px solid ${on ? T.accent : T.line}`}}>
      {[1, 2, 3].map(k => <div key={k} style={{position: 'absolute', left: 0, right: 0, top: k * 95, borderTop: `2px solid ${on ? '#ffd2b8' : '#e1e4e9'}`}} />)}
      {[1, 2].map(k => <div key={k} style={{position: 'absolute', top: 0, bottom: 0, left: k * 147, borderLeft: `2px solid ${on ? '#ffd2b8' : '#e1e4e9'}`}} />)}
      <div style={{position: 'absolute', left: 0, right: 0, top: 70, display: 'flex', justifyContent: 'center'}}><Icon name="House" size={110} color={on ? T.accent : T.ink3} /></div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 200, textAlign: 'center', ...F, fontWeight: 800, fontSize: 60, color: T.ink}}>{name}</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 290, textAlign: 'center'}}>
        <span style={{...F, fontWeight: 800, fontSize: 44, color: '#fff', background: on ? T.accent : T.ink3, borderRadius: 12, padding: '2px 22px', whiteSpace: 'nowrap'}}>{on ? d.on : d.off}</span></div>
    </div>;
  };
  const r = kease(f, 20, 14);
  return (
    <Frame s={s}>
      {tile(220, d.old, true, 4)}
      <div style={{position: 'absolute', left: 676, top: 500, ...F, fontWeight: 800, fontSize: 80, color: T.ink3}}>+</div>
      {tile(760, d.new, both, 10)}
      <div style={{position: 'absolute', left: 1230, top: 500, opacity: r}}><Icon name="ArrowRight" size={90} color={T.ink} /></div>
      <div style={{position: 'absolute', left: 1350, top: 400, width: 360, height: 280, borderRadius: 30, background: both ? T.rise : T.fall, opacity: r,
        display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${0.85 + 0.15 * r})`}}>
        <span style={{...F, fontWeight: 800, fontSize: 170, color: '#fff', letterSpacing: -4}}>{d.res}</span></div>
    </Frame>
  );
};

// ───────── Memo: 메모 세 줄 ─────────
export const KMemo: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const items: string[] = d.items; const at: number[] = d.at;
  return (
    <Frame s={s}>
      <div style={{position: 'absolute', left: 430, top: 320, width: 1060, height: 500, background: '#fffbea', borderRadius: 18, boxShadow: '0 10px 30px rgba(0,0,0,0.10)', border: '2px solid #f1e6b8', transform: 'rotate(-1deg)'}}>
        {items.map((t, i) => { const a = katLine(s.lines, at[i]) + (i === 2 ? 40 : i * 12); const o = kease(f, a, 12); const hot = i === items.length - 1;
          return <div key={i} style={{position: 'absolute', left: 60, right: 60, top: 50 + i * 150, height: 120, borderBottom: '2px solid #ece0ac', display: 'flex', alignItems: 'center', gap: 28, opacity: o}}>
            <div style={{width: 64, height: 64, borderRadius: 12, border: `4px solid ${hot ? T.rise : T.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none'}}>
              {o > 0.6 ? <Icon name="Check" size={46} color={hot ? T.rise : T.ink} /> : null}</div>
            <span style={{...F, fontWeight: 800, fontSize: 66, color: hot ? T.rise : T.ink, whiteSpace: 'nowrap'}}>{t}</span>
          </div>; })}
      </div>
    </Frame>
  );
};

// ───────── Stairs: 세율 계단 8칸 ─────────
export const KStairs: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const at: number[] = d.at; const N = 8, X = 300, SW = 165, BOT = 800;
  const h = (i: number) => 70 + i * 58; const one = 5, half = 4;
  const a1 = kease(f, katLine(s.lines, at[0]) + 20, 14), a2 = kease(f, katLine(s.lines, at[1]), 14);
  return (
    <Frame s={s}>
      {Array.from({length: N}).map((_, i) => { const o = kease(f, 4 + i * 4, 10); const c = i === one && a1 > 0.5 ? T.rise : i === half && a2 > 0.5 ? T.fall : '#d9dde3';
        return <div key={i} style={{position: 'absolute', left: X + i * SW, top: BOT - h(i) * o, width: SW - 10, height: h(i) * o, background: c, borderRadius: '12px 12px 0 0'}} />; })}
      <div style={{position: 'absolute', left: X, width: SW - 10, top: BOT + 6, textAlign: 'center', ...F, fontWeight: 800, fontSize: 48, color: T.ink2}}>{d.low}</div>
      <div style={{position: 'absolute', left: X + 7 * SW, width: SW - 10, top: BOT - h(7) - 64, textAlign: 'center', ...F, fontWeight: 800, fontSize: 48, color: T.ink2}}>{d.high}</div>
      <div style={{position: 'absolute', left: X + one * SW - 40, top: BOT - h(one) - 150, opacity: a1, display: 'flex', flexDirection: 'column', alignItems: 'center', width: SW + 70}}>
        <span style={{...F, fontWeight: 800, fontSize: 44, color: '#fff', background: T.rise, borderRadius: 12, padding: '2px 16px', whiteSpace: 'nowrap'}}>{d.one}</span>
        <Icon name="User" size={74} color={T.rise} /></div>
      <div style={{position: 'absolute', left: X + half * SW - 170, top: BOT - h(half) - 150, opacity: a2, display: 'flex', flexDirection: 'column', alignItems: 'center', width: SW + 130}}>
        <span style={{...F, fontWeight: 800, fontSize: 44, color: '#fff', background: T.fall, borderRadius: 12, padding: '2px 16px', whiteSpace: 'nowrap'}}>{d.half}</span>
        <div style={{display: 'flex'}}><Icon name="User" size={64} color={T.fall} /><Icon name="User" size={64} color={T.fall} /></div></div>
    </Frame>
  );
};

// ───────── Band: 관리처분 인가 → 공사 기간 → 입주 ─────────
export const KBand: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const steps: string[] = d.steps; const at: number[] = d.at;
  const X = 200, Y = 430, Wd = [300, 920, 300]; const xs = [X, X + Wd[0] + 10, X + Wd[0] + Wd[1] + 20];
  const a = kease(f, katLine(s.lines, at[0]), 16), b = kease(f, katLine(s.lines, at[1]) + 10, 20);
  return (
    <Frame s={s}>
      {steps.map((t, i) => <div key={i} style={{position: 'absolute', left: xs[i], top: Y, width: Wd[i], height: 140, borderRadius: 18, opacity: kease(f, 4 + i * 10, 12),
        background: i === 1 ? '#eceef2' : T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden'}}>
        {i === 1 ? <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: Wd[1] * 0.5 * b, background: T.accent}} /> : null}
        <span style={{position: 'relative', ...F, fontWeight: 800, fontSize: i === 1 ? 60 : 40, color: i === 1 ? T.ink : '#fff', textAlign: 'center', wordBreak: 'keep-all', lineHeight: 1.15}}>{t}</span>
      </div>)}
      <div style={{position: 'absolute', left: xs[1], width: Wd[1] * 0.5, top: Y + 160, borderTop: `5px solid ${T.accent}`, opacity: b}} />
      <div style={{position: 'absolute', left: xs[1], top: Y + 180, ...F, fontWeight: 800, fontSize: 52, color: T.accent, opacity: b, whiteSpace: 'nowrap'}}>{d.half}</div>
      {d.when ? <div style={{position: 'absolute', left: X, top: 345, opacity: a}}>
        <span style={{...F, fontWeight: 800, fontSize: 44, color: '#fff', background: T.rise, borderRadius: 12, padding: '2px 20px', whiteSpace: 'nowrap'}}>{d.when}</span></div> : null}
    </Frame>
  );
};

// ───────── Five: 갈래 다섯 줄(지금 줄만 켜짐, 지나간 줄은 체크) ─────────
export const KFive: React.FC<{s: KScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const items: [string, string][] = d.items; const k = klineAt(s.lines, f);
  const lit: number = (d.lit as number[])[k] ?? -1; const done: number[] = d.done || [];
  return (
    <Frame s={s}>
      <div style={{position: 'absolute', left: 180, top: 336, width: 1560}}>
        {items.map(([a, b], i) => { const on = i === lit; const dn = done.includes(i) || i < lit; const o = kease(f, 4 + i * 6, 10);
          return <div key={i} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 92, marginBottom: 8, padding: '0 30px', borderRadius: 16, opacity: o * (on || dn ? 1 : 0.55),
            background: on ? T.soft : '#fff', border: `2px solid ${on ? T.accent : T.line}`}}>
            <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
              <div style={{width: 52, height: 52, borderRadius: 26, background: on ? T.accent : dn ? T.ink : T.line, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                {dn && !on ? <Icon name="Check" size={34} color="#fff" /> : null}</div>
              <span style={{...F, fontWeight: 700, fontSize: 46, color: T.ink, whiteSpace: 'nowrap'}}>{a}</span></div>
            <span style={{...F, fontWeight: 800, fontSize: 48, color: on ? T.accent : T.ink2, whiteSpace: 'nowrap'}}>{b}</span>
          </div>; })}
      </div>
    </Frame>
  );
};
