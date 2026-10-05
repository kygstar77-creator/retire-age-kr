// M-1(월배당 거꾸로 계산)에서 처음 만든 부품 — 흰 보드(TallyFrame) 안에서 쓴다. 글자는 props로 받는다(부품 안 고정 낱말은 '분배'·'지난 1년 분배율'·'필요한 돈'뿐 — lfrender text가 같이 뽑는다).
// RuleCards 규칙 카드 줄 · Gauge 가로 문턱 게이지 · Timeline 구간 띠 · FlowBoxes 거꾸로 화살표 상자 · ProductCard 상품 카드
// Calendar12 12칸 달력(동전) · GroupBars 묶음 막대(나란히, 쌓지 않음 — RULES 누적 막대 금지) · Grid 표(칸마다 도장)
import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig, spring, Easing} from 'remotion';
import {T, F, CL} from './fm';

const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);
const lift = '0 2px 4px rgba(24,25,29,0.06), 0 14px 34px rgba(24,25,29,0.09)';
export const COLR: Record<string, string> = {ink: T.ink2, ink3: T.ink3, dim: T.ink3, accent: T.accent, rise: T.rise, fall: T.fall};

export const RuleCards: React.FC<{cards: [string, string, string, number][]; active: number; x?: number; y?: number; w?: number}> = ({cards, active, x = 150, y = 330, w = 1620}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const g = 36; const cw = (w - g * (cards.length - 1)) / cards.length;
  return (
    <>
      {cards.map(([n, head, sub, at], i) => {
        const s = spring({frame: f - at, fps, config: {damping: 14}});
        const on = i === active;
        if (f < at) return (
          <div key={i} style={{position: 'absolute', left: x + i * (cw + g), top: y, width: cw, height: 250, borderRadius: 20, border: `3px dashed ${T.line}`, opacity: fade(f, 0, 14)}}>
            <div style={{...F, position: 'absolute', left: 30, top: 24, fontWeight: 700, fontSize: 56, color: T.line}}>{n}</div>
          </div>
        );
        return (
          <div key={i} style={{position: 'absolute', left: x + i * (cw + g), top: y + (1 - s) * 30, width: cw, height: 250, opacity: f >= at ? s : 0, background: T.surface, borderRadius: 20,
            boxShadow: on ? `inset 0 0 0 4px ${T.accent}, ${lift}` : lift}}>
            <div style={{...F, position: 'absolute', left: 30, top: 24, fontWeight: 700, fontSize: 56, color: on ? T.accent : T.ink3}}>{n}</div>
            <div style={{...F, position: 'absolute', left: 30, top: 104, right: 24, fontWeight: 700, fontSize: 40, color: T.ink, whiteSpace: 'nowrap'}}>{head}</div>
            <div style={{...F, position: 'absolute', left: 30, top: 166, right: 24, fontWeight: 500, fontSize: 24, color: T.ink2, lineHeight: 1.35, wordBreak: 'keep-all'}}>{sub}</div>
          </div>
        );
      })}
    </>
  );
};

// 가로 게이지: 0 ~ max(만원). lines = 문턱 [값, 글자, 나타날 프레임], fill = [값, 시작 프레임, 색] 차례로 그 값까지 차오름(나중 것이 앞 것을 덮음)
export const Gauge: React.FC<{max: number; lines: [number, string, number][]; fill: [number, number, string][]; target?: [number, string, number] | null; x?: number; y?: number; w?: number; unit?: string}> =
  ({max, lines, fill, target, x = 200, y = 560, w = 1500, unit = '만원'}) => {
  const f = useCurrentFrame();
  const H = 70; const sx = (v: number) => (v / max) * w;
  let cur = 0; let col = T.ink2;
  for (const [v, at, c] of fill) { if (f >= at) { const p = interpolate(f, [at, at + 24], [0, 1], {...CL, easing: Easing.out(Easing.cubic)}); cur = cur + (v - cur) * p; col = COLR[c] ?? T.ink2; } }
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: H}}>
      <div style={{position: 'absolute', inset: 0, background: T.line, borderRadius: 14}} />
      <div style={{position: 'absolute', left: 0, top: 0, height: H, width: sx(cur), background: col, borderRadius: 14}} />
      <div style={{...F, position: 'absolute', left: 0, top: H + 14, fontWeight: 700, fontSize: 26, color: T.ink3}}>0</div>
      {lines.map(([v, t, at], i) => (
        <div key={i} style={{position: 'absolute', left: sx(v) - 3, top: -60, width: 6, height: H + 60 + 18, background: T.ink, borderRadius: 3, opacity: fade(f, at)}}>
          <div style={{...F, position: 'absolute', left: 0, top: H + 82, transform: 'translateX(-50%)', fontWeight: 700, fontSize: 30, color: T.ink, whiteSpace: 'nowrap'}}>{t}</div>
        </div>
      ))}
      {target ? (
        <div style={{position: 'absolute', left: sx(target[0]), top: -92, opacity: fade(f, target[2]), transform: 'translateX(-50%)'}}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: '#fff', background: T.accent, borderRadius: 10, padding: '4px 14px', whiteSpace: 'nowrap'}}>{target[1]}</div>
          <div style={{width: 0, height: 0, margin: '0 auto', borderLeft: '12px solid transparent', borderRight: '12px solid transparent', borderTop: `14px solid ${T.accent}`}} />
        </div>
      ) : null}
      <div style={{...F, position: 'absolute', right: 0, top: H + 14, fontWeight: 500, fontSize: 22, color: T.ink3}}>{unit}</div>
    </div>
  );
};

export const Timeline: React.FC<{segs: [string, string, string, number][]; x?: number; y?: number; w?: number}> = ({segs, x = 160, y = 470, w = 1600}) => {
  const f = useCurrentFrame();
  const ws = [0.42, 0.36, 0.22]; let left = 0;
  return (
    <>
      {segs.map(([head, sub, c, at], i) => {
        const sw = w * (ws[i] ?? 1 / segs.length); const l = left; left += sw;
        const p = interpolate(f, [at, at + 18], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
        const col = COLR[c] ?? T.ink2;
        return (
          <div key={i} style={{position: 'absolute', left: x + l, top: y, width: sw - 12, opacity: f >= at ? 1 : 0}}>
            <div style={{height: 90, width: `${p * 100}%`, background: c === 'dim' ? `repeating-linear-gradient(135deg, ${T.line} 0 12px, ${T.surface} 12px 24px)` : col, borderRadius: 14}} />
            <div style={{...F, fontWeight: 700, fontSize: 38, color: c === 'accent' ? T.accent : T.ink, marginTop: 20, whiteSpace: 'nowrap', opacity: p}}>{head}</div>
            <div style={{...F, fontWeight: 500, fontSize: 28, color: T.ink2, marginTop: 6, whiteSpace: 'nowrap', opacity: p}}>{sub}</div>
          </div>
        );
      })}
    </>
  );
};

// 거꾸로 화살표 상자: boxes는 왼쪽→오른쪽 순서, 나타나는 건 at 순서(보통 오른쪽 먼저). 화살표는 오른쪽에서 왼쪽을 가리킨다.
export const FlowBoxes: React.FC<{boxes: [string, string, number][]; x?: number; y?: number; w?: number}> = ({boxes, x = 150, y = 380, w = 1620}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const g = 110; const bw = (w - g * (boxes.length - 1)) / boxes.length;
  return (
    <>
      {boxes.map(([head, sub, at], i) => {
        const s = spring({frame: f - at, fps, config: {damping: 14}});
        const last = i === boxes.length - 1; const first = i === 0;
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: x + i * (bw + g), top: y + (1 - s) * 24, width: bw, height: 220, opacity: f >= at ? s : 0, background: last ? T.ink : T.surface, borderRadius: 20,
              boxShadow: first ? `inset 0 0 0 4px ${T.accent}, ${lift}` : lift}}>
              <div style={{...F, position: 'absolute', left: 30, top: 34, fontWeight: 700, fontSize: 32, color: last ? T.daccent : T.ink2}}>{head}</div>
              <div style={{...F, position: 'absolute', left: 30, top: 96, right: 20, fontWeight: 700, fontSize: sub.length > 14 ? 34 : 46, color: last ? '#fff' : first ? T.accent : T.ink, lineHeight: 1.2, wordBreak: 'keep-all'}}>{sub}</div>
            </div>
            {!first ? <div style={{...F, position: 'absolute', left: x + i * (bw + g) - g + 14, top: y + 70, fontSize: 70, fontWeight: 700, color: T.accent, opacity: f >= at ? s : 0}}>←</div> : null}
          </React.Fragment>
        );
      })}
    </>
  );
};

export const ProductCard: React.FC<{name: string; desc: string; freq: string; rate: string; rateCalc: string; need: string; at: number; rateAt: number; needAt: number; hot?: boolean}> =
  ({name, desc, freq, rate, rateCalc, need, at, rateAt, needAt, hot}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - at, fps, config: {damping: 14}});
  const r = spring({frame: f - rateAt, fps, config: {damping: 12}});
  const n = spring({frame: f - needAt, fps, config: {damping: 11}});
  return (
    <>
      <div style={{position: 'absolute', left: 150, top: 330 + (1 - s) * 30, width: 700, height: 470, background: T.surface, borderRadius: 24, boxShadow: lift, opacity: s}}>
        <div style={{height: 14, background: hot ? T.accent : T.ink, borderRadius: '24px 24px 0 0'}} />
        <div style={{...F, position: 'absolute', left: 40, top: 54, right: 30, fontWeight: 700, fontSize: name.length > 8 ? 52 : 80, color: T.ink, lineHeight: 1.1, wordBreak: 'keep-all'}}>{name}</div>
        <div style={{...F, position: 'absolute', left: 40, top: 250, right: 30, fontWeight: 500, fontSize: 28, color: T.ink2, lineHeight: 1.4, wordBreak: 'keep-all'}}>{desc}</div>
        <div style={{...F, position: 'absolute', left: 40, bottom: 40, fontWeight: 700, fontSize: 26, color: T.ink, background: T.bg, borderRadius: 10, padding: '6px 16px'}}>분배 {freq}</div>
      </div>
      <div style={{position: 'absolute', left: 940, top: 340, opacity: f >= rateAt ? 1 : 0}}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2}}>지난 1년 분배율</div>
        <div style={{...F, fontWeight: 700, fontSize: 120, color: T.ink, lineHeight: 1.05, letterSpacing: -2, transform: `scale(${0.75 + 0.25 * r})`, transformOrigin: 'left center'}}>{rate}</div>
        <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3}}>{rateCalc}</div>
      </div>
      <div style={{position: 'absolute', left: 940, top: 620, opacity: f >= needAt ? 1 : 0, display: 'flex', alignItems: 'baseline', gap: 22}}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2, whiteSpace: 'nowrap'}}>필요한 돈</div>
        <div style={{...F, fontWeight: 700, fontSize: 100, color: hot ? T.accent : T.ink, letterSpacing: -2, whiteSpace: 'nowrap', transform: `scale(${0.7 + 0.3 * n})`, transformOrigin: 'left center'}}>{need}</div>
      </div>
    </>
  );
};

export const Calendar12: React.FC<{months: [string, string][]; at: number; x?: number; y?: number; w?: number}> = ({months, at, x = 150, y = 330, w = 1620}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const cols = 6; const g = 18; const cw = (w - g * (cols - 1)) / cols; const ch = 196;
  return (
    <>
      {months.map(([m, v], i) => {
        const cx = x + (i % cols) * (cw + g); const cy = y + Math.floor(i / cols) * (ch + g);
        const ca = at + 6 + i * 4; const s = spring({frame: f - ca, fps, config: {damping: 10}});
        return (
          <div key={i} style={{position: 'absolute', left: cx, top: cy, width: cw, height: ch, background: v ? T.soft : T.surface, borderRadius: 16, boxShadow: lift, opacity: fade(f, i * 2)}}>
            <div style={{...F, position: 'absolute', left: 20, top: 14, fontWeight: 700, fontSize: 28, color: T.ink2}}>{m}</div>
            {v ? (
              <div style={{position: 'absolute', left: '50%', top: 66, transform: `translateX(-50%) scale(${f >= ca ? s : 0})`, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <div style={{width: 64, height: 64, borderRadius: 32, background: T.accent, boxShadow: 'inset 0 -6px 0 rgba(0,0,0,0.15)'}} />
                <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, marginTop: 6, whiteSpace: 'nowrap'}}>{v}</div>
              </div>
            ) : <div style={{position: 'absolute', left: '50%', top: 92, width: 34, height: 4, background: T.line, transform: 'translateX(-50%)', borderRadius: 2}} />}
          </div>
        );
      })}
    </>
  );
};

// 묶음 막대(같은 0 기준선, 묶음 안 막대를 나란히) — 쌓지 않는다
export const GroupBars: React.FC<{groups: [string, [number, string, string][]][]; max: number; at: number; legend: [string, string][]; x?: number; y?: number; w?: number; h?: number}> =
  ({groups, max, at, legend, x = 560, y = 420, w = 1180, h = 330}) => {
  const f = useCurrentFrame();
  const gg = 90; const gw = (w - gg * (groups.length - 1)) / groups.length; const bw = Math.min(150, (gw - 20) / 2);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: h, borderTop: `3px solid ${T.ink}`}} />
      {groups.map(([name, bars], gi) => {
        const gx = gi * (gw + gg); const tot = bars.length * bw + (bars.length - 1) * 16; const ox = gx + (gw - tot) / 2;
        return (
          <React.Fragment key={gi}>
            {bars.map(([v, t, c], bi) => {
              const st = at + gi * 14 + bi * 18;
              const p = interpolate(f, [st, st + 22], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
              const bh = (v / max) * h * p; const col = COLR[c] ?? T.ink2;
              return (
                <React.Fragment key={bi}>
                  <div style={{position: 'absolute', left: ox + bi * (bw + 16), width: bw, top: h - bh, height: bh, background: col, borderRadius: '10px 10px 0 0'}} />
                  <div style={{...F, position: 'absolute', left: ox + bi * (bw + 16) - 30, width: bw + 60, top: h - bh - 46, textAlign: 'center', fontWeight: 700, fontSize: 32, color: col, opacity: fade(f, st + 16), whiteSpace: 'nowrap'}}>{t}</div>
                </React.Fragment>
              );
            })}
            <div style={{...F, position: 'absolute', left: gx, width: gw, top: h + 14, textAlign: 'center', fontWeight: 700, fontSize: name.length > 8 ? 26 : 32, color: T.ink, opacity: fade(f, at), wordBreak: 'keep-all'}}>{name}</div>
          </React.Fragment>
        );
      })}
      <div style={{position: 'absolute', right: 0, top: -64, display: 'flex', gap: 26, opacity: fade(f, at)}}>
        {legend.map(([t, c], i) => (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10}}>
            <div style={{width: 24, height: 24, borderRadius: 6, background: COLR[c] ?? T.ink2}} />
            <span style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, whiteSpace: 'nowrap'}}>{t}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// 표: cols 머리, rows = [줄 이름, 칸 글자들, 나타날 프레임], stamp가 있으면 칸마다 작은 도장, hot = [줄, 칸, 프레임] 주황 테두리
export const Grid: React.FC<{cols: string[]; rows: [string, string[], number][]; stamp?: string | null; hot?: [number, number, number][]; x?: number; y?: number; w?: number}> =
  ({cols, rows, stamp, hot = [], x = 150, y = 330, w = 1620}) => {
  const f = useCurrentFrame();
  const lw = 380; const cw = (w - lw) / cols.length; const rh = rows.length > 2 ? 120 : 150; const hh = 76;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w}}>
      {cols.map((c, i) => <div key={i} style={{...F, position: 'absolute', left: lw + i * cw, width: cw, top: 0, height: hh, textAlign: 'center', fontWeight: 700, fontSize: c.length > 8 ? 26 : 32, color: T.ink2, opacity: fade(f, 0), lineHeight: `${hh}px`, whiteSpace: 'nowrap'}}>{c}</div>)}
      <div style={{position: 'absolute', left: 0, right: 0, top: hh, borderTop: `3px solid ${T.ink}`, opacity: fade(f, 0)}} />
      {rows.map(([name, cells, at], r) => {
        const o = fade(f, at, 12); const top = hh + 10 + r * rh;
        return (
          <div key={r} style={{position: 'absolute', left: 0, right: 0, top, height: rh - 10, opacity: o, transform: `translateY(${(1 - o) * 14}px)`}}>
            <div style={{...F, position: 'absolute', left: 10, top: 0, height: rh - 10, display: 'flex', alignItems: 'center', fontWeight: 700, fontSize: 36, color: T.ink, whiteSpace: 'nowrap'}}>{name}</div>
            {cells.map((c, i) => {
              const h = hot.find(([hr, hc]) => hr === r && hc === i); const on = h ? f >= h[2] : false;
              return (
                <div key={i} style={{position: 'absolute', left: lw + i * cw + 12, width: cw - 24, top: 0, height: rh - 18, background: on ? T.soft : T.bg, borderRadius: 14,
                  boxShadow: on ? `inset 0 0 0 4px ${T.accent}` : undefined, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14}}>
                  <span style={{...F, fontWeight: 700, fontSize: /\d/.test(c) ? 50 : 32, color: on ? T.accent : /\d/.test(c) ? T.ink : T.ink3, whiteSpace: 'nowrap'}}>{c}</span>
                  {stamp ? <span style={{...F, fontWeight: 700, fontSize: 22, color: T.rise, border: `3px solid ${T.rise}`, borderRadius: 8, padding: '0 8px', transform: 'rotate(-8deg)', whiteSpace: 'nowrap'}}>{stamp}</span> : null}
                </div>
              );
            })}
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 0, right: 0, top: hh + 10 + rows.length * rh, borderTop: `2px solid ${T.line}`, opacity: fade(f, rows[rows.length - 1]?.[2] ?? 0)}} />
    </div>
  );
};
