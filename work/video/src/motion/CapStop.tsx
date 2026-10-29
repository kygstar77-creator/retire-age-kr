// 천장에 닿아 멈추는 막대(CapStop) — N-3 '3. 어디서 빠지나' 국민연금 상한(2026-10-29 motion). TallyFrame 자식.
// 연봉 칸마다 한 달 보험료 막대가 왼쪽부터 차례로 자란다. 말이 '끝'에 닿으면 천장 점선이 그어지고,
// 높은 칸 막대는 자라다 천장에 부딪혀 눌렸다 멈춘다(스프링). 주황은 천장 값 하나 + 손 동그라미.
// 정직성: 막대 높이는 props 값(calc_out 원 단위) 그대로 — 천장이 없었다면 얼마였을지(유령 막대)는 그리지 않는다(사실표에 없는 숫자).
// 상한·세율·한도처럼 '어디서부터 안 는다'는 말에 다시 쓴다. 편마다 seed로 막대 폭·천장 쪽 글자 자리·자라는 순서 간격이 바뀐다.
// 글자는 전부 HTML(10/13 교훈). 판 전체 1.00→1.04 다가가기(U5 10/19).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type CapStopProps = {
  seed: string;
  bars: {label: string; v: number; at: number}[];   // v = 원, at = 말 줄 번호 + 비율
  cap: number;                                       // 원
  capLabel: string; capAt: number;                   // 천장 점선 + 이름(먹)
  stopText: string; stopAt: number;                  // 답(주황)
  axis: string;                                      // 막대 아래 이름(무엇의 칸인지)
  beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

export const CapStop: React.FC<CapStopProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const n = p.bars.length;
  const X0 = 220, X1 = 1700, BASE = 800, TOP = 450;   // 천장 y = TOP
  const slot = (X1 - X0) / n; const bw = slot * (0.52 + r('w') * 0.14);
  const Y = (v: number) => BASE - v / p.cap * (BASE - TOP);
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.04], CL);
  const cA = at(p.capAt), sA = at(p.stopAt);
  const capO = g(f, cA, 22, Easing.inOut(Easing.cubic));
  const hit = (v: number) => v >= p.cap;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '50% 70%'}}>
      {/* 바닥 */}
      <div style={{position: 'absolute', left: X0 - 30, top: BASE, width: (X1 - X0 + 60) * g(f, 0, 20), height: 5, background: T.ink, borderRadius: 3}} />
      {p.bars.map((b, i) => {
        const a = at(b.at);
        const x = X0 + slot * i + (slot - bw) / 2;
        let h: number;
        if (hit(b.v)) {
          // 천장까지 빨리 자라 부딪힌 뒤 살짝 눌렸다 펴짐 — 천장이 아직 안 그어졌어도 그 자리에서 멈춘다
          const grow = g(f, a, 12, Easing.in(Easing.quad));
          const bump = f > a + 12 ? 1 - 0.035 * Math.exp(-(f - a - 12) / 5) * Math.cos((f - a - 12) / 2.4) : 1;
          h = (BASE - Y(b.v)) * grow * Math.min(1, bump);
        } else {
          h = (BASE - Y(b.v)) * spring({frame: f - a, fps, config: {damping: 15}});
        }
        const lo = g(f, a, 10);
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: x, top: BASE - h, width: bw, height: h, background: hit(b.v) ? T.ink : T.ink2, borderRadius: '6px 6px 0 0'}} />
          <div style={{position: 'absolute', left: x + bw / 2 - 110, top: BASE + 18, width: 220, textAlign: 'center', opacity: lo, ...F, fontWeight: 700, fontSize: 32, color: T.ink, whiteSpace: 'nowrap'}}>{b.label}</div>
        </React.Fragment>;
      })}
      {/* 무엇의 막대인지 — 왼쪽 위(아래는 출처 줄 자리, 10/29 눈 검사 겹침) */}
      <div style={{position: 'absolute', left: X0 - 30, top: TOP - 128, opacity: g(f, 10, 12), ...F, fontWeight: 700, fontSize: 32, color: T.ink2, whiteSpace: 'nowrap'}}>{p.axis}</div>
      {/* 천장 — 이름은 낮은 막대 쪽(왼쪽): 오른쪽은 답·손 동그라미 자리 */}
      <div style={{position: 'absolute', left: X0 - 30, top: TOP - 3, width: (X1 - X0 + 60) * capO, height: 0, borderTop: `6px dashed ${T.ink}`}} />
      <div style={{position: 'absolute', left: X0 - 30, top: TOP - 66 + (1 - g(f, cA + 8, 12)) * 10, opacity: g(f, cA + 8, 12), ...F, fontWeight: 800, fontSize: 44, color: T.ink, whiteSpace: 'nowrap'}}>{p.capLabel}</div>
      {/* 답 — 천장에 닿은 막대들 위(천장 이름보다 한 층 위) */}
      {(() => {
        const idx = p.bars.map((b, i) => hit(b.v) ? i : -1).filter((i) => i >= 0);
        if (!idx.length) return null;
        const xa = X0 + slot * idx[0], xb = X0 + slot * (idx[idx.length - 1] + 1);
        const so = g(f, sA, 12);
        const cx = (xa + xb) / 2;
        return <>
          <div style={{position: 'absolute', left: cx - 300, top: TOP - 176 + (1 - so) * 14, width: 600, textAlign: 'center', opacity: so, ...F, fontWeight: 800, fontSize: 84, color: T.accent, letterSpacing: -2, whiteSpace: 'nowrap'}}>{p.stopText}</div>
          <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible', pointerEvents: 'none'}}>
            <HandCircle cx={cx} cy={TOP} rx={(xb - xa) / 2 + 20} ry={44} p={g(f, sA + 14, 22, Easing.inOut(Easing.quad))} />
          </svg>
        </>;
      })()}
    </div>
  );
};
