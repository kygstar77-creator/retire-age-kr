// C-2 "1998년 3억, 매달 200만원 팔아 쓰기 — 정우 씨 통장은 언제 바닥났나" 화면 — 재료 work/video/c2.json(ep/C-2/c2props.py가 script.md·voice.json·calc_n1_out.txt로 만든다)
// 틀: 그림 장면(정우 씨 SVG 시트, 16:9 전체·켄 번스·해 칩·숫자 카드·말풍선) ↔ 흰 보드(통장 선·해마다 막대·환율·달력 벽·꺼낸 돈별 막대·줄였다면 표)를 말 줄마다 번갈아.
// 장면 안에서 말 줄(k)마다 한 칸씩 바뀐다(U5 같은 화면 8초 이하). 오른쪽 위 '바닥나는 해: ?' 칸은 4번째 줄부터 결말 줄까지 고정, 그 뒤 '2011년'.
// 숫자 글자는 전부 c2.json에서 온다(c2props.py가 calc·대본과 기계 대조). 코드 안 숫자는 배치 좌표와 축 눈금뿐. 색: 정우 씨 주황(accent)·민수 씨 파랑(fall)·오르면 빨강·내리면 파랑.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame, HandCircle} from './parts/fm';

type CLine = {text: string; audio: string; frames: number};
type CScene = {kind: string; lines: CLine[]; frames: number; data: any};
export type C2Props = {fps: number; scenes: CScene[]; boxOn: number; boxFlip: number; boxQ: string; boxA: string; boxLabel: string; badge: string; missing: number};
export const c2Frames = (p: C2Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {accent: T.accent, fall: T.fall, rise: T.rise, ink: T.ink2};
const starts = (ls: CLine[]) => { const o: number[] = []; let a = 0; for (const l of ls) { o.push(a); a += l.frames; } return o; };
const curLine = (s: CScene, f: number) => { const st = starts(s.lines); let k = 0; st.forEach((a, i) => { if (f >= a) k = i; }); return {k, st}; };
const ease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
const sgn = (s: string) => s.replace(/^-/, '−');
const W = 1920, H = 1080;

// ───────── 공통: 자막 · 흰 보드 틀 ─────────
const Caption: React.FC<{s: CScene; dark?: boolean}> = ({s, dark}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const o = interpolate(f, [st[k], st[k] + 5], [0.2, 1], CL);
  return (
    <div style={{position: 'absolute', bottom: 58, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{...F, fontWeight: 700, fontSize: 40, lineHeight: 1.35, color: '#fff', background: dark ? 'rgba(16,17,20,0.86)' : T.ink,
        padding: '14px 34px', borderRadius: 16, maxWidth: 1500, textAlign: 'center', wordBreak: 'keep-all'}}>{s.lines[k].text.replace(/^"|"$/g, '')}</div>
    </div>
  );
};

const Board: React.FC<{s: CScene; children: React.ReactNode}> = ({s, children}) => {
  const f = useCurrentFrame(); const o = ease(f, 0, 10); const src: string = s.data.source;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <div style={{position: 'absolute', left: 110, top: 64, opacity: o, transform: `translateY(${(1 - o) * 12}px)`}}>
        <div style={{...F, fontWeight: 700, fontSize: 56, color: T.ink, whiteSpace: 'nowrap'}}>{s.data.title}</div>
      </div>
      {children}
      {src ? <div style={{...F, fontWeight: 500, fontSize: src.length > 120 ? 17 : 20, color: T.ink3, position: 'absolute', left: 110, right: 110, bottom: 18, whiteSpace: 'nowrap', overflow: 'hidden'}}>출처 {src}</div> : null}
      <Caption s={s} />
    </AbsoluteFill>
  );
};

// ───────── 그림 장면 ─────────
const PicScene: React.FC<{s: CScene; badge: string}> = ({s, badge}) => {
  const f = useCurrentFrame(); const d = s.data; const {k, st} = curLine(s, f);
  const t = interpolate(f, [0, s.frames], [0, 1], {...CL, easing: Easing.inOut(Easing.sin)});
  const punch = interpolate(f, [0, 8], [1.04, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const z = (d.zoom[0] + (d.zoom[1] - d.zoom[0]) * t) * punch;
  const iw = W * z, ih = H * z;
  let x = W / 2 - d.cx * z + d.pan * t; x = Math.min(0, Math.max(W - iw, x));
  let y = d.fy * H * (1 - z); y = Math.min(0, Math.max(H - ih, y));
  const card = (() => { for (let i = k; i >= 0; i--) if (d.cards[i]) return {c: d.cards[i], at: st[i]}; return null; })();
  const quote = d.quote ? d.quote[k] : null;
  const yo = ease(f, 3, 10);
  const sp = card ? spring({frame: f - card.at - 3, fps: 30, config: {damping: 13, mass: 0.7}}) : 0;
  const qo = quote ? ease(f, st[k] + 2, 10) : 0;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={staticFile(d.pic)} style={{position: 'absolute', left: x, top: y, width: iw, height: ih, filter: d.gray ? 'grayscale(1) brightness(0.6)' : undefined}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 330, background: 'linear-gradient(rgba(16,17,20,0), rgba(16,17,20,0.85))'}} />
      {d.year ? <div style={{position: 'absolute', left: 64, top: 52, padding: '10px 26px', background: T.accent, borderRadius: 14, opacity: yo, transform: `translateX(${(1 - yo) * -30}px)`}}>
        <span style={{...F, fontWeight: 700, fontSize: 48, color: '#fff', whiteSpace: 'nowrap'}}>{d.year}</span></div> : null}
      <div style={{position: 'absolute', left: 64, top: d.year ? 140 : 56, padding: '6px 16px', borderRadius: 10, background: 'rgba(255,255,255,0.9)'}}>
        <span style={{...F, fontWeight: 700, fontSize: 24, color: T.ink, whiteSpace: 'nowrap'}}>{badge}</span></div>
      {card ? (
        <div style={{position: 'absolute', left: 64, top: 640, padding: '18px 34px 20px', background: '#fff', borderRadius: 26, boxShadow: '0 14px 40px rgba(0,0,0,0.35)',
          transform: `translateY(${(1 - sp) * 40}px) scale(${0.9 + 0.1 * sp})`, transformOrigin: 'left bottom', opacity: Math.min(1, sp * 1.4)}}>
          <div style={{...F, fontWeight: 700, fontSize: card.c[0].length > 7 ? 84 : 108, lineHeight: 1, color: T.accent, letterSpacing: -3, whiteSpace: 'nowrap'}}>{card.c[0]}</div>
          {card.c[1] ? <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2, marginTop: 10, whiteSpace: 'nowrap'}}>{card.c[1]}</div> : null}
        </div>) : null}
      {quote ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 250, display: 'flex', justifyContent: 'center', opacity: qo, transform: `translateY(${(1 - qo) * 16}px)`}}>
          <div style={{...F, fontWeight: 700, fontSize: 64, color: T.ink, background: '#fff', padding: '22px 44px', borderRadius: 40, boxShadow: '0 12px 36px rgba(0,0,0,0.3)', whiteSpace: 'nowrap'}}>“{quote}”</div>
        </div>) : null}
      <div style={{...F, fontWeight: 500, fontSize: 20, color: 'rgba(255,255,255,0.75)', position: 'absolute', left: 64, bottom: 18, whiteSpace: 'nowrap'}}>{d.source}</div>
      <Caption s={s} dark />
    </AbsoluteFill>
  );
};

// ───────── 통장 선 그래프 ─────────
const PX0 = 230, PX1 = 1640, PY0 = 250, PY1 = 820;
const ChartScene: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const {k, st} = curLine(s, f);
  const ser: {name: string; color: string; pts: [number, number][]; upto: number[]}[] = d.series;
  const ends = ser.flatMap((x) => x.upto);
  const x0 = Math.min(...ser.map((x) => x.pts[0][0])), x1 = Math.max(...ends);
  const X = (v: number) => PX0 + ((v - x0) / Math.max(1, x1 - x0)) * (PX1 - PX0);
  const Y = (v: number) => PY1 - (v / d.ymax) * (PY1 - PY0);
  const reach = (u: number[]) => { const prev = k > 0 ? u[k - 1] : (u[0] > x0 ? x0 : u[0]); return prev + (u[k] - prev) * ease(f, st[k], 26); };
  const ticks = [1, 2, 3].filter((v) => v <= d.ymax);
  const yrs: number[] = []; for (let y = x0; y <= x1; y++) yrs.push(y);
  const every = yrs.length > 16 ? 4 : yrs.length > 8 ? 2 : 1;
  const valAt = (color: string, xv: number) => { const sx = ser.find((q) => q.color === (color === 'rise' ? 'accent' : color)) || ser[0]; const p = sx.pts.find((q) => q[0] === xv); return p ? p[1] : 0; };
  const band = d.band || (d.band2 ? d.band2[k] : null);
  return (
    <Board s={s}>
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        {band && band[0] != null ? <g opacity={ease(f, d.band ? 0 : st[k], 12)}>
          <rect x={X(band[0])} y={PY0 - 10} width={X(band[1]) - X(band[0])} height={PY1 - PY0 + 10} fill={T.soft} opacity={0.7} rx={8} />
          <text x={(X(band[0]) + X(band[1])) / 2} y={PY0 - 22} textAnchor="middle" style={{...F, fontWeight: 700, fontSize: 28, fill: T.accent}}>{band[2]}</text></g> : null}
        {ticks.map((v) => <g key={v}><line x1={PX0} x2={PX1} y1={Y(v)} y2={Y(v)} stroke={T.line} strokeWidth={2} />
          <text x={PX0 - 18} y={Y(v) + 9} textAnchor="end" style={{...F, fontWeight: 500, fontSize: 26, fill: T.ink3}}>{v}억</text></g>)}
        <line x1={PX0} x2={PX1} y1={PY1} y2={PY1} stroke={T.ink3} strokeWidth={2} />
        {d.line1 ? <g><line x1={PX0} x2={PX1} y1={Y(1)} y2={Y(1)} stroke={T.rise} strokeWidth={3} strokeDasharray="12 10" /></g> : null}
        {d.floor ? <g opacity={ease(f, 10)}><line x1={PX0} x2={PX1} y1={Y(0.24)} y2={Y(0.24)} stroke={T.rise} strokeWidth={3} strokeDasharray="12 10" />
          <text x={PX0 + 12} y={Y(0.24) - 14} textAnchor="start" style={{...F, fontWeight: 700, fontSize: 26, fill: T.rise}}>1년 치 꺼낼 돈</text></g> : null}
        {yrs.filter((y, i) => (i % every === 0 && x1 - y >= every / 2) || y === x1).map((y) => <text key={y} x={X(y)} y={PY1 + 40} textAnchor="middle" style={{...F, fontWeight: 500, fontSize: 24, fill: T.ink3}}>{y === x0 ? `${y}.1 시작` : `${y - 1} 말`}</text>)}
        {ser.map((sx, i) => {
          const r = reach(sx.upto); const vis = sx.pts.filter((p) => p[0] <= r + 1e-6);
          if (!vis.length) return null;
          let pts = vis.map((p) => `${X(p[0])},${Y(p[1])}`);
          const nx = sx.pts.find((p) => p[0] > r);
          const last = vis[vis.length - 1];
          if (nx && r > last[0]) { const u = (r - last[0]) / (nx[0] - last[0]); pts = [...pts, `${X(r)},${Y(last[1] + (nx[1] - last[1]) * u)}`]; }
          return <g key={i}>
            <polyline points={pts.join(' ')} fill="none" stroke={COL[sx.color]} strokeWidth={7} strokeLinejoin="round" strokeLinecap="round" />
            {vis.map((p, j) => <circle key={j} cx={X(p[0])} cy={Y(p[1])} r={8} fill="#fff" stroke={COL[sx.color]} strokeWidth={4} />)}
          </g>;
        })}
        {(() => { const placed: number[][] = []; return d.beats.slice(0, k + 1).flatMap((bs: [number, string, string][], j: number) => bs.map((b, i) => {
          const o = ease(f, st[j] + 8 + i * 12, 10); const v = valAt(b[2], b[0]); const cx = X(b[0]); const cy = Y(v);
          const w = b[1].length * 26 + 34; const left = Math.min(PX1 + 150 - w, Math.max(PX0, cx - w / 2)); let top = cy - 74;
          const hit = (tp: number) => placed.some((q) => left < q[0] + q[2] + 8 && q[0] < left + w + 8 && tp < q[1] + 58 && q[1] < tp + 58);
          for (let g = 0; g < 8 && hit(top); g++) top -= 60;
          if (top < PY0 - 30 || (left + w > PX1 - 120 && top < 230)) { top = cy + 24; for (let g = 0; g < 8 && hit(top); g++) top += 60; }
          placed.push([left, top, w]);
          return <g key={`${j}-${i}`} opacity={o}><line x1={cx} x2={cx} y1={top > cy ? top : top + 50} y2={top > cy ? cy + 10 : cy - 10} stroke={COL[b[2]]} strokeWidth={2} />
            <rect x={left} y={top} width={w} height={50} rx={12} fill={COL[b[2]]} />
            <text x={left + w / 2} y={top + 36} textAnchor="middle" style={{...F, fontWeight: 700, fontSize: 30, fill: '#fff'}}>{sgn(b[1])}</text></g>;
        })); })()}
      </svg>
      <div style={{position: 'absolute', left: 110, top: 146, display: 'flex', gap: 28}}>
        {ser.map((sx, i) => <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10}}>
          <div style={{width: 34, height: 8, borderRadius: 4, background: COL[sx.color]}} /><span style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2}}>{sx.name}</span></div>)}
        <span style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3, alignSelf: 'center'}}>연말 잔액(원화)</span>
      </div>
      {d.minus && k >= 1 ? <div style={{position: 'absolute', left: 300, top: 650, display: 'flex', gap: 24, opacity: ease(f, st[1] + 4)}}>
        {d.minus.map((m: string, i: number) => <div key={i} style={{...F, fontWeight: 700, fontSize: 36, color: i ? T.rise : T.ink2, background: '#fff', padding: '14px 26px', borderRadius: 16, border: `3px solid ${i ? T.rise : T.line}`, whiteSpace: 'nowrap', opacity: ease(f, st[1] + 4 + i * 18)}}>{m}</div>)}
      </div> : null}
    </Board>
  );
};

// ───────── 해마다 막대 ─────────
const BarsScene: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const {k, st} = curLine(s, f);
  const n = d.years.length; const bw = Math.min(170, 1300 / n - 40); const gap = (1400 - n * bw) / Math.max(1, n - 1);
  const mx = Math.max(...d.vals.map((v: number) => Math.abs(v)));
  const zero = 560, scale = 250 / mx;
  const shown = d.show[k];
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 260, top: zero, width: 1400, height: 3, background: T.ink3}} />
      {d.years.map((y: number, i: number) => {
        const p = ease(f, i * 8, 18) * (i < shown ? 1 : 0); const v = d.vals[i]; const h = Math.abs(v) * scale * p; const up = v > 0;
        const x = 260 + i * (bw + gap); const c = up ? T.rise : T.fall;
        return <React.Fragment key={y}>
          <div style={{position: 'absolute', left: x, top: up ? zero - h : zero + 3, width: bw, height: Math.max(h, 4), background: c, borderRadius: 8}} />
          <div style={{...F, position: 'absolute', left: x - 30, width: bw + 60, textAlign: 'center', top: up ? zero - h - 56 : zero + h + 12, fontWeight: 700, fontSize: 40, color: c, opacity: p}}>{sgn(d.fmt[i])}</div>
          <div style={{...F, position: 'absolute', left: x - 30, width: bw + 60, textAlign: 'center', top: up ? zero + 14 : zero - 46, fontWeight: 500, fontSize: 28, color: T.ink3, opacity: p}}>{y}</div>
        </React.Fragment>;
      })}
      {d.sell[k] ? <div style={{...F, position: 'absolute', left: 260, top: 850, fontWeight: 700, fontSize: 34, color: T.ink, padding: '10px 22px', background: T.soft, borderRadius: 12, opacity: ease(f, st[k] + 6), whiteSpace: 'nowrap'}}>{d.sell[k]}</div> : null}
    </Board>
  );
};

// ───────── 칩·카드형 보드들 ─────────
const Chip: React.FC<{big: string; small?: string; o: number; color?: string; w?: number}> = ({big, small, o, color = T.accent, w}) => (
  <div style={{background: '#fff', borderRadius: 22, padding: '22px 30px', boxShadow: '0 6px 24px rgba(0,0,0,0.06)', border: `2px solid ${T.line}`, opacity: o, transform: `translateY(${(1 - o) * 18}px)`, width: w}}>
    <div style={{...F, fontWeight: 700, fontSize: 60, color, whiteSpace: 'nowrap', letterSpacing: -1}}>{sgn(big)}</div>
    {small ? <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginTop: 8, whiteSpace: 'nowrap'}}>{small}</div> : null}
  </div>
);

const Preview: React.FC<{s: CScene}> = ({s}) => { const f = useCurrentFrame(); return (
  <Board s={s}><div style={{position: 'absolute', left: 260, top: 330, display: 'flex', gap: 60}}>
    {s.data.items.map((it: string[], i: number) => <Chip key={i} big={it[0]} small={it[1]} o={ease(f, 10 + i * 40)} w={620} />)}</div></Board>); };

const Who: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  const st0 = spring({frame: f - 10, fps: 30, config: {damping: 10}});
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 110, top: 200, width: 760, height: 560, borderRadius: 26, overflow: 'hidden'}}>
        <Img src={staticFile(d.pic)} style={{position: 'absolute', left: 380 - 1025 * (1 + 0.04 * k), top: -70 * (1 + 0.04 * k), width: 1920 * 0.95 * (1 + 0.04 * k)}} />
        <div style={{position: 'absolute', right: 26, top: 26, transform: `rotate(-8deg) scale(${1.4 - 0.4 * st0})`, opacity: Math.min(1, st0 * 1.5), border: `6px solid ${T.rise}`, borderRadius: 14, padding: '6px 20px'}}>
          <span style={{...F, fontWeight: 700, fontSize: 48, color: T.rise}}>가상 인물</span></div>
      </div>
      <div style={{position: 'absolute', left: 940, top: 200, display: 'flex', flexDirection: 'column', gap: 18}}>
        {d.chips.map((c: string[], i: number) => i <= k ? <Chip key={i} big={c[0]} small={c[1]} o={ease(f, st[i] + 4)} color={i === 3 ? T.ink : T.accent} w={860} /> : null)}
      </div>
    </Board>
  );
};

const Fx: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  // 줄별: 0 사람만 · 1 환율 두 칸 · 2 영호 수익 · 3 1998 환율 · 4 정우 수익
  const rates = d.rates as string[][]; const nR = k >= 3 ? 3 : k >= 1 ? 2 : 0;
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 150, top: 190, ...F, fontWeight: 700, fontSize: 30, color: T.ink3}}>원/달러 연말 환율</div>
      <div style={{position: 'absolute', left: 150, top: 240, display: 'flex', alignItems: 'center', gap: 26}}>
        {rates.slice(0, nR).map((r, i) => <React.Fragment key={i}>
          {i ? <span style={{...F, fontWeight: 700, fontSize: 50, color: T.ink3, opacity: ease(f, (i === 2 ? st[3] : st[1]) + i * 6)}}>→</span> : null}
          <Chip big={r[1]} small={r[0]} o={ease(f, (i === 2 ? st[3] : st[1]) + i * 10)} color={i === 1 ? T.rise : T.ink} w={380} /></React.Fragment>)}
      </div>
      <div style={{position: 'absolute', left: 150, top: 520, display: 'flex', gap: 50}}>
        {d.people.map((pp: string[], i: number) => {
          const showRet = i === 0 ? k >= 2 : k >= 4; const at = i === 0 ? st[2] : st[4];
          return <div key={i} style={{width: 760, background: '#fff', borderRadius: 24, padding: '24px 32px', border: `3px solid ${i ? T.accent : T.line}`, opacity: ease(f, 6 + i * 16)}}>
            <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink}}>{pp[0]} <span style={{fontSize: 30, color: T.ink3}}>{pp[1]}</span></div>
            {showRet ? <div style={{display: 'flex', gap: 40, marginTop: 18, opacity: ease(f, at + 6)}}>
              <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2}}>{pp[2]}</div>
              <div style={{...F, fontWeight: 700, fontSize: 64, color: T.rise, marginTop: -12}}>{pp[3]}</div></div> : <div style={{height: 70}} />}
          </div>;
        })}
      </div>
    </Board>
  );
};

const Tax: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 150, top: 210, display: 'flex', gap: 30, alignItems: 'center'}}>
        {d.taxes.map((t: string[], i: number) => <Chip key={i} big={t[1]} small={t[0]} o={ease(f, 8 + i * 14)} color={T.ink} w={400} />)}
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.accent, opacity: ease(f, 40), whiteSpace: 'nowrap'}}>{d.basic}</div>
      </div>
      {k >= 1 ? <div style={{position: 'absolute', left: 150, top: 480, opacity: ease(f, st[1] + 2)}}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2, marginBottom: 18}}>지역 건강보험료에 들어가는 소득</div>
        <div style={{display: 'flex', gap: 16}}>
          {d.kunbo.map((c: [string, number], i: number) => <div key={i} style={{...F, fontWeight: 700, fontSize: 36, padding: '16px 26px', borderRadius: 14, whiteSpace: 'nowrap',
            background: c[1] ? '#fff' : T.soft, color: c[1] ? T.ink : T.accent, border: `3px solid ${c[1] ? T.line : T.accent}`, opacity: ease(f, st[1] + 6 + i * 6)}}>{c[1] ? '✓ ' : '✗ '}{c[0]}</div>)}
        </div></div> : null}
    </Board>
  );
};

const Fx08: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 150, top: 240, display: 'flex', gap: 60}}>
        <Chip big={d.usd} small="지수(달러 기준)" o={ease(f, 8)} color={T.fall} w={640} />
        {k >= 1 ? <Chip big={d.krw} small="정우 씨 통장(원화 기준)" o={ease(f, st[1] + 4)} color={T.fall} w={640} /> : null}
      </div>
      {k >= 1 ? <div style={{position: 'absolute', left: 150, top: 560, display: 'flex', gap: 26, alignItems: 'center'}}>
        <span style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, opacity: ease(f, st[1] + 30)}}>원/달러 연말 환율</span>
        {d.rates.map((r: string[], i: number) => <React.Fragment key={i}>{i ? <span style={{...F, fontWeight: 700, fontSize: 48, color: T.ink3, opacity: ease(f, st[1] + 40)}}>→</span> : null}
          <Chip big={r[1]} small={r[0]} o={ease(f, st[1] + 30 + i * 14)} color={i ? T.rise : T.ink} w={360} /></React.Fragment>)}
      </div> : null}
    </Board>
  );
};

const Jar: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 150, top: 290, display: 'flex', alignItems: 'center', gap: 28}}>
        {d.steps.map((st: string[], i: number) => <React.Fragment key={i}>{i ? <span style={{...F, fontWeight: 700, fontSize: 56, color: T.ink3, opacity: ease(f, 10 + i * 26)}}>→</span> : null}
          <Chip big={st[1]} small={st[0]} o={ease(f, 10 + i * 26)} color={i === 1 ? T.rise : T.ink} w={430} /></React.Fragment>)}
      </div>
      <div style={{position: 'absolute', left: 150, top: 560, ...F, fontWeight: 700, fontSize: 44, color: T.rise, padding: '18px 30px', border: `4px dashed ${T.rise}`, borderRadius: 18, opacity: ease(f, 90), whiteSpace: 'nowrap'}}>{d.need}</div>
    </Board>
  );
};

const Sum: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  const per = Math.max(4, Math.floor((s.lines[0].frames - 30) / d.n));
  const shown = Math.min(d.n, Math.floor(f / per) + 1);
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 150, top: 220, display: 'flex', gap: 12}}>
        {Array.from({length: d.n}).map((_, i) => <div key={i} style={{width: 96, height: 150, borderRadius: 12, background: i < shown ? T.accent : T.line, opacity: i < shown ? 1 : 0.5,
          display: 'flex', alignItems: 'flex-end', justifyContent: 'center', paddingBottom: 10}}>
          <span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff'}}>{i + 1}</span></div>)}
      </div>
      <div style={{position: 'absolute', left: 150, top: 410, ...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>한 칸 = {d.each}</div>
      <div style={{position: 'absolute', left: 150, top: 480, display: 'flex', gap: 40, alignItems: 'flex-end'}}>
        <Chip big={d.total} small={`다 꺼낸 해 ${d.n}번`} o={ease(f, per * d.n)} w={560} />
        {k >= 1 ? <Chip big={d.put.replace('넣은 돈 ', '')} small="넣은 돈" o={ease(f, st[1] + 4)} color={T.ink} w={460} /> : null}
      </div>
    </Board>
  );
};

const Yh: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 150, top: 250, display: 'flex', gap: 60}}>
        {d.big.map((b: string[], i: number) => <Chip key={i} big={b[1]} small={b[0]} o={ease(f, 8 + i * 50)} color={T.rise} w={620} />)}
      </div>
      <div style={{position: 'absolute', left: 150, top: 560, ...F, fontWeight: 700, fontSize: 40, color: T.ink2, opacity: ease(f, 110)}}>{d.note}</div>
    </Board>
  );
};

const Wall: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  const cols = 19, tw = 86, th = 132, gx = 6, gy = 74, x0 = 90, y0 = 220;
  const fails = Object.keys(d.fail);
  return (
    <Board s={s}>
      {d.years.map((y: number, i: number) => {
        const r = Math.floor(i / cols), c = i % cols; const x = x0 + c * (tw + gx), yy = y0 + r * (th + gy);
        const fail = fails.includes(String(y)); const dark = fail && k >= 1; const five = k >= 2 && fail && y <= 2002;
        const o = ease(f, i * 2.5, 8); const dim = k >= 4 && !fail ? 1 : 0;
        return <React.Fragment key={y}>
          <div style={{position: 'absolute', left: x, top: yy, width: tw, height: th, borderRadius: 10, opacity: o, transform: `translateY(${(1 - o) * 14}px)`,
            background: dark ? '#4b4f58' : dim ? '#e3f4e8' : '#fff', border: `${five ? 5 : 2}px solid ${five ? T.accent : T.line}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
            <span style={{...F, fontWeight: 500, fontSize: 20, color: dark ? '#cfd2d8' : T.ink3}}>1월</span>
            <span style={{...F, fontWeight: 700, fontSize: 27, color: dark ? '#fff' : T.ink}}>{y}</span>
          </div>
          {fail && k >= 3 ? <div style={{position: 'absolute', left: x - 10, width: tw + 20, top: yy + th + 8, textAlign: 'center', ...F, fontWeight: 700, fontSize: 26, color: T.accent, opacity: ease(f, st[3] + fails.indexOf(String(y)) * 6), whiteSpace: 'nowrap'}}>{d.fail[String(y)]}</div> : null}
        </React.Fragment>;
      })}
      {k >= 1 ? <div style={{position: 'absolute', left: 130, top: 640, display: 'flex', gap: 30}}>
        <Chip big={d.count[0]} small="2025년 말까지" o={ease(f, st[1] + 6)} color={T.ink} w={360} />
        {k >= 4 ? <Chip big={d.count[1]} small="2025년 말까지" o={ease(f, st[4] + 6)} color={'#1f9d55'} w={360} /> : null}
      </div> : null}
    </Board>
  );
};

const Amount: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data; const vis: number[] = d.order[k];
  return (
    <Board s={s}>
      {d.rows.map((r: [string, number], i: number) => {
        const on = vis.includes(i); const first = d.order.findIndex((o: number[]) => o.includes(i)); const o = on ? ease(f, (first === k ? st[k] : 0) + 6 + (first === k ? vis.indexOf(i) * 10 : 0), 18) : 0;
        const y = 220 + i * 140; const w = 1100 * (r[1] / 37) * o;
        return <React.Fragment key={i}>
          <div style={{...F, position: 'absolute', left: 130, top: y + 18, width: 260, fontWeight: 700, fontSize: 38, color: T.ink, opacity: on ? 1 : 0.35}}>{r[0]}</div>
          <div style={{position: 'absolute', left: 400, top: y, width: 1100, height: 90, background: T.line, borderRadius: 12, opacity: on ? 1 : 0.35}} />
          <div style={{position: 'absolute', left: 400, top: y, width: Math.max(w, on ? 6 : 0), height: 90, background: i === 2 ? T.accent : T.ink2, borderRadius: 12}} />
          {on ? <div style={{...F, position: 'absolute', left: 400 + Math.max(w, 6) + 24, top: y + 16, fontWeight: 700, fontSize: 44, color: i === 2 ? T.accent : T.ink, opacity: o, whiteSpace: 'nowrap'}}>{r[1]}명 / 37</div> : null}
        </React.Fragment>;
      })}
    </Board>
  );
};

const Race: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const X = (y: number) => 330 + (y - 1998) * 50;
  return (
    <Board s={s}>
      {d.rows.map((r: [string, number, string], i: number) => {
        const p = ease(f, 10 + i * 60, 40); const y = 300 + i * 200; const end = 1998 + (r[1] - 1998) * p;
        return <React.Fragment key={i}>
          <div style={{...F, position: 'absolute', left: 110, top: y + 14, fontWeight: 700, fontSize: 38, color: i ? T.accent : T.ink2}}>{r[0]}</div>
          <div style={{position: 'absolute', left: X(1998), top: y, width: X(end) - X(1998), height: 80, background: i ? T.accent : T.ink2, borderRadius: 12}} />
          <div style={{...F, position: 'absolute', left: X(end) + 20, top: y + 14, fontWeight: 700, fontSize: 40, color: i ? T.accent : T.ink, opacity: interpolate(p, [0.9, 1], [0, 1], CL), whiteSpace: 'nowrap'}}>{r[2]}</div>
        </React.Fragment>;
      })}
      <div style={{...F, position: 'absolute', left: X(1998) - 40, top: 700, fontWeight: 500, fontSize: 28, color: T.ink3}}>1998.1 시작</div>
    </Board>
  );
};

const Cut: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const {k, st} = curLine(s, f); const d = s.data;
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 130, top: 190, ...F, fontWeight: 700, fontSize: 34, color: T.ink3, opacity: ease(f, 4)}}>{d.base}</div>
      {d.rows.map((r: string[], i: number) => {
        if (i > k) return null; const ok = r[2] === 'ok'; const o = ease(f, st[i] + 4); const hl = k >= 3;
        const c = ok ? '#1f9d55' : T.rise;
        return <div key={i} style={{position: 'absolute', left: 130, top: 270 + i * 165, width: 1640, height: 135, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 40px',
          background: '#fff', borderRadius: 22, border: `${hl ? 5 : 2}px solid ${hl ? c : T.line}`, opacity: o, transform: `translateX(${(1 - o) * -30}px)`, boxSizing: 'border-box'}}>
          <span style={{...F, fontWeight: 700, fontSize: 44, color: T.ink}}>{r[0]}</span>
          <span style={{...F, fontWeight: 700, fontSize: 52, color: c}}>{r[1]}</span></div>;
      })}
    </Board>
  );
};

const Cta: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const sp = spring({frame: f - 6, fps: 30, config: {damping: 14}});
  return (
    <Board s={s}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 230, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 24, transform: `scale(${0.85 + 0.15 * sp})`, opacity: sp}}>
          <Flame size={90} /><span style={{...F, fontWeight: 700, fontSize: 120, color: T.ink}}>{d.url}</span></div>
        <div style={{display: 'flex', gap: 30}}>
          {d.fields.map((x: string, i: number) => <div key={i} style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, background: '#fff', border: `3px solid ${T.line}`, borderRadius: 18, padding: '22px 60px', opacity: ease(f, 40 + i * 20)}}>{x}</div>)}
        </div>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.accent, opacity: ease(f, 90)}}>설명란 첫 줄</div>
      </div>
    </Board>
  );
};

const KIND: Record<string, React.FC<{s: CScene}>> = {chart: ChartScene, bars: BarsScene, preview: Preview, who: Who, fx: Fx, tax: Tax, fx08: Fx08, jar: Jar, sum: Sum, yh: Yh, wall: Wall, amount: Amount, race: Race, cut: Cut, cta: Cta};

// ───────── 고정 칸: 바닥나는 해 ─────────
const FloorBox: React.FC<{p: C2Props}> = ({p}) => {
  const f = useCurrentFrame(); if (f < p.boxOn) return null;
  const o = ease(f, p.boxOn, 12); const flip = f >= p.boxFlip; const sp = flip ? spring({frame: f - p.boxFlip, fps: 30, config: {damping: 10}}) : 0;
  return (
    <div style={{position: 'absolute', right: 56, top: 130, padding: '12px 26px', borderRadius: 16, background: flip ? T.accent : 'rgba(24,25,29,0.9)', opacity: o, display: 'flex', alignItems: 'baseline', gap: 14,
      transform: `scale(${flip ? 0.85 + 0.15 * sp : 1})`, transformOrigin: 'right top'}}>
      <span style={{...F, fontWeight: 700, fontSize: 28, color: '#fff', whiteSpace: 'nowrap'}}>{p.boxLabel}</span>
      <span style={{...F, fontWeight: 700, fontSize: 48, color: flip ? '#fff' : '#FFD000', whiteSpace: 'nowrap'}}>{flip ? p.boxA : p.boxQ}</span>
    </div>
  );
};

export const C2: React.FC<C2Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => {
        const C = s.kind === 'pic' ? null : KIND[s.kind]; const st = starts(s.lines);
        const el = <Sequence key={i} from={from} durationInFrames={s.frames}>
          {s.kind === 'pic' ? <PicScene s={s} badge={p.badge} /> : C ? <C s={s} /> : null}
          {s.lines.map((l, j) => <Sequence key={j} from={st[j]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
        </Sequence>;
        from += s.frames; return el;
      })}
      <div style={{position: 'absolute', right: 56, top: 56, display: 'flex', alignItems: 'center', gap: 10, padding: '8px 16px', borderRadius: 12, background: 'rgba(255,255,255,0.85)'}}>
        <Flame size={24} /><span style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2}}>파이어맵</span></div>
      <FloorBox p={p} />
    </AbsoluteFill>
  );
};
export const _unused = {HandCircle};
