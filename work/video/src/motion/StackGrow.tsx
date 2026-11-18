// 쌓이는 잔액 막대(StackGrow) — JT-1 4장 '대출 잔액에 쌓이는 것' 정지 판(jt1_stack.png)을 움직이는 부품으로(2026-11-17 motion). TallyFrame 자식.
// 모양만 그린다(금액 축 없음): 막대 n개가 왼쪽부터 하나씩 서고, 막대마다 세 층(받은 돈 → 보증료 → 이자)이 아래부터 쌓인다.
//  - 받은 돈 층은 곧게(달마다 같은 돈), 이자 층은 갈수록 두꺼워진다(잔액에 붙는 이자) — 모양 비율은 seed로 조금씩 다름, 판 아래 '그림은 모양만' 줄은 TallyFrame source가 맡음.
//  - focus: 말이 부르는 층만 진하게, 나머지 0.3 · 오른쪽 이름표도 그 층만 크게.
//  - balance: 마지막 막대 오른쪽 세로 괄호 + '대출 잔액' · first: 첫 막대 보증료 칸 손 동그라미 + 주황 값(편 props가 사실표 값만 넣음) · wobble: 이자 층 높이가 출렁(금리 변동)
//  - foot: 판 아래 주황 한 줄. 주황은 first 값·foot 가운데 그 화면 답 하나만 쓰는 게 원칙(편 props에서 둘 다 켜지 않기).
// 정직성: 숫자 글자는 props(first.text)만 — 막대 높이는 금액이 아님. 반복 방지: seed로 막대 수 그대로 두고 x 여백·면 결 기울기·층 비율·손떨림이 바뀜.
// 들어오는 법: 막대는 '아래에서 차오름'(층 순서대로), 이름표는 층이 처음 찰 때 옆에서 찍힘 — 다른 판(찍기·써지듯)과 겹치지 않게.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

type Layer = 'pay' | 'fee' | 'int';
type Mark = {text: string; at: number};
export type StackGrowProps = {
  seed: string;
  bars: number;                                        // 4~8
  names: {pay: string; fee: string; int: string};
  build: [number, number] | null;                      // 막대가 서는 박자 구간(소수 박자), null = 처음부터 다 서 있음
  focus: {layer: Layer | null; at: number; bars?: 'first' | 'rest'}[];   // 박자마다 진하게 할 층(null = 모두) · bars: 그 층 중 첫 막대만/나머지만(11/18 '가입 때 한 번' vs '매년')
  balance: Mark | null;
  first: Mark | null;
  wobble: {at: number} | null;
  foot: Mark | null;
  note?: Mark | null;                                  // 11/18 먹 한 줄(대본 자막에 있는 식만, 예 '코픽스 + 0.85%') — 주황 아님
  wobAmp?: number;                                     // 출렁 크기(기본 0.09)
  origin?: string;                                     // 다가가는 중심(기본 '42% 70%' · 이자 층이 주인공이면 오른쪽 위)
  pushTo?: number;                                     // 다가가기 끝 배율(기본 1.06)
  beats: number[];
};

const out = Easing.out(Easing.cubic), io = Easing.inOut(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const TAN = '#b8895a';   // 이자 층(정지 판 jt1_stack과 같은 계열)
const COL: Record<Layer, string> = {pay: T.ink, fee: T.ink2, int: TAN};

export const StackGrow: React.FC<StackGrowProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { if (x < 0) return -100; const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const n = Math.max(2, Math.min(8, p.bars));
  const X0 = 230 + Math.round(r('x') * 60), X1 = 1380, YB = 860, HMAX = 560;
  const slot = (X1 - X0) / n, bw = slot * (0.66 + r('w') * 0.08);
  // 층 모양(금액 아님): 받은 돈은 곧게, 보증료는 얇게(첫 막대에 가입 때 한 번 몫), 이자는 갈수록 두껍게
  const kInt = 0.9 + r('k') * 0.5;
  const raw = Array.from({length: n}, (_, i) => {
    const pay = (i + 1);
    const fee = 0.16 + 0.07 * i;
    const int = kInt * (0.05 * (i + 1) * (i + 1) + 0.05 * i);
    return {pay, fee, int};
  });
  const top = Math.max(...raw.map((v) => v.pay + v.fee + v.int));
  const S = HMAX / top;
  // 막대가 서는 시각
  const bStart = p.build ? at(p.build[0]) : -100, bEnd = p.build ? at(p.build[1]) : -100;
  const barT = (i: number) => p.build ? bStart + (bEnd - bStart) * (i / Math.max(1, n - 1)) * 0.85 : -100;
  const fill = (i: number, k: number) => g(f, barT(i) + k * 9, 16, io);   // k = 0 받은 돈, 1 보증료, 2 이자
  // 지금 진한 층
  const fo0 = p.focus.filter((fo) => f >= at(fo.at)); const lastAt = fo0.length ? at(fo0[fo0.length - 1].at) : -100;
  const curF = fo0.length ? fo0[fo0.length - 1] : null, prevF = fo0.length > 1 ? fo0[fo0.length - 2] : null;
  const cur: Layer | null = curF ? curF.layer : null;
  const ease = g(f, lastAt, 12);
  const lit = (fo: typeof curF, L: Layer, i: number) => fo === null || fo.layer === null || (fo.layer === L && (!fo.bars || (fo.bars === 'first' ? i === 0 : i > 0)));
  const opOf = (L: Layer, i = -1) => { const ok = (fo: typeof curF) => i < 0 ? (fo === null || fo.layer === null || fo.layer === L) : lit(fo, L, i);
    const now = ok(curF) ? 1 : 0.3; const was = ok(prevF) ? 1 : 0.3; return was + (now - was) * ease; };
  // 금리 변동: 이자 층 높이가 천천히 출렁(±9%) — 모양만
  const wob = p.wobble && f >= at(p.wobble.at) ? Math.sin((f - at(p.wobble.at)) / 11) * (p.wobAmp ?? 0.09) * g(f, at(p.wobble.at), 20) : 0;
  const tilt = 36 + Math.round(r('t') * 22);
  const endF = (B[B.length - 1] ?? 0) + 150;
  // 11/18 U5: 1.03은 느려서 같은 화면 9.0초·8.5초(층 강조만 바뀌는 줄) — EqRow처럼 1.06 + 왼쪽으로 조금 흐름
  const push = interpolate(f, [0, endF], [1, p.pushTo ?? 1.06], CL), drift = interpolate(f, [0, endF], [0, -28], CL);
  const jit = (i: number, k: string) => (r(`j${i}${k}`) - 0.5) * 5;   // 손떨림 꼭짓점
  const quad = (x: number, y0: number, y1: number, w: number, i: number, k: string) =>
    `${x + jit(i, k + 'a')},${y0 + jit(i, k + 'b')} ${x + w + jit(i, k + 'c')},${y0 + jit(i, k + 'd')} ${x + w + jit(i, k + 'e')},${y1} ${x + jit(i, k + 'f')},${y1}`;
  const geo = raw.map((v, i) => {
    const x = X0 + slot * i + (slot - bw) / 2;
    const hp = v.pay * S * fill(i, 0), hf = v.fee * S * fill(i, 1), hi = v.int * S * (1 + wob * (0.4 + 0.6 * i / (n - 1))) * fill(i, 2);
    return {x, yPay: YB - hp, yFee: YB - hp - hf, yInt: YB - hp - hf - hi};
  });
  const last = geo[n - 1];
  const balO = p.balance ? g(f, at(p.balance.at), 14) : 0, firO = p.first ? g(f, at(p.first.at), 14) : 0, footO = p.foot ? g(f, at(p.foot.at), 16) : 0;
  const nameAt: Record<Layer, number> = {pay: p.build ? barT(0) + 6 : 4, fee: p.build ? barT(0) + 15 : 8, int: p.build ? barT(0) + 24 : 12};
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const LX = Math.max(X1 + 150, last.x + bw + 170);
  const ly: Record<Layer, number> = {int: 330, fee: 470, pay: 610};
  const g0 = geo[0];
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translateX(${drift}px) scale(${push})`, transformOrigin: p.origin ?? '42% 70%'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <defs>
          {(['pay', 'fee', 'int'] as Layer[]).map((L, k) => (
            <pattern key={L} id={`sg${L}${p.seed}`} width={16 - k * 2} height={16 - k * 2} patternUnits="userSpaceOnUse" patternTransform={`rotate(${tilt + k * 7})`}>
              <line x1={0} y1={0} x2={0} y2={16} stroke={COL[L]} strokeWidth={3} strokeOpacity={0.55} />
            </pattern>))}
        </defs>
        <line x1={X0 - 30} x2={X1 + 30} y1={YB + 2} y2={YB + 2 + jit(0, 'base')} stroke={T.ink} strokeWidth={4} strokeLinecap="round" />
        {geo.map((q, i) => (fill(i, 0) <= 0 ? null : <g key={i}>
          <polygon points={quad(q.x, q.yPay, YB, bw, i, 'p')} fill={`url(#sgpay${p.seed})`} stroke={COL.pay} strokeWidth={5} strokeLinejoin="round" opacity={opOf('pay', i)} />
          {fill(i, 1) > 0 ? <polygon points={quad(q.x, q.yFee, q.yPay, bw, i, 'f')} fill={`url(#sgfee${p.seed})`} stroke={COL.fee} strokeWidth={5} strokeLinejoin="round" opacity={opOf('fee', i)} /> : null}
          {fill(i, 2) > 0 ? <polygon points={quad(q.x, q.yInt, q.yFee, bw, i, 'i')} fill={`url(#sgint${p.seed})`} stroke={COL.int} strokeWidth={5} strokeLinejoin="round" opacity={opOf('int', i)} /> : null}
        </g>))}
        {/* 대출 잔액: 마지막 막대 오른쪽 세로 괄호 */}
        <path d={`M${last.x + bw + 18} ${YB} h20 V${last.yInt} h-20`} fill="none" stroke={T.ink} strokeWidth={5} strokeLinejoin="round" opacity={balO} />
        {/* 첫 막대 보증료 칸(가입 때 한 번) */}
        <HandCircle cx={g0.x + bw / 2} cy={(g0.yFee + g0.yPay) / 2} rx={bw * 0.72} ry={Math.max(34, (g0.yPay - g0.yFee) * 1.4)} p={firO} />
        <line x1={g0.x + bw / 2 + 20} y1={g0.yFee - 46} x2={g0.x + bw / 2 + 90} y2={g0.yFee - 150} stroke={T.accent} strokeWidth={4} opacity={firO} />
      </svg>
      {(['int', 'fee', 'pay'] as Layer[]).map((L) => {
        const on = cur === L;
        return <div key={L} style={lab({left: LX, top: ly[L] + (on ? -8 : 0), fontWeight: 800, fontSize: on ? 78 : 64, color: COL[L],
          opacity: g(f, nameAt[L], 10) * (0.35 + 0.65 * opOf(L)), transform: `translateX(${(1 - g(f, nameAt[L], 10)) * 40}px)`})}>{p.names[L]}</div>;
      })}
      {p.balance ? <div style={lab({left: last.x + bw + 50, top: (YB + last.yInt) / 2 - 150, width: 60, fontWeight: 800, fontSize: 46, color: T.ink, opacity: balO, writingMode: 'vertical-rl', letterSpacing: 6})}>{p.balance.text}</div> : null}
      {p.first ? <div style={lab({left: g0.x + bw / 2 + 70, top: g0.yFee - 250, fontWeight: 900, fontSize: 96, color: T.accent, opacity: firO, transform: `scale(${0.85 + 0.15 * firO})`, transformOrigin: '0% 100%'})}>{p.first.text}</div> : null}
      {p.wobble ? <div style={lab({left: LX, top: ly.int - 92, fontWeight: 800, fontSize: 58, color: TAN, opacity: g(f, at(p.wobble.at), 12)})}>↕ 변동</div> : null}
      {p.note ? (() => { const o = g(f, at(p.note.at), 22, io); return <div style={lab({left: X0, top: 350, fontWeight: 800, fontSize: 62, color: T.ink, opacity: Math.min(1, o * 2) * (1 - 0.75 * firO), clipPath: `inset(0 ${(1 - o) * 100}% 0 0)`})}>{p.note.text}</div>; })() : null}
      {/* 11/18: 판 아래(YB+40)는 자막 띠와 겹쳤음 → 왼쪽 위 빈 자리(앞 막대가 낮은 곳), 써지듯 왼쪽부터 */}
      {p.foot ? <div style={lab({left: X0, top: 270, fontWeight: 800, fontSize: 54, color: T.accent, opacity: footO, clipPath: `inset(0 ${(1 - footO) * 100}% 0 0)`})}>{p.foot.text}</div> : null}
    </div>
  );
};
