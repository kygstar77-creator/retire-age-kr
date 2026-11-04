// 오린 종이 블록 쌓기(PayBlocks) — N-3 '3. 어디서 빠지나' 보험료는 같은 비율·소득세만 가파르게(2026-11-01 motion, shot_plan r18). TallyFrame 자식.
// 연봉 칸마다 세전 월급에서 빠지는 몫을 블록으로 쌓는다. 보험료 블록 넷(연금·건강·장기요양·고용)이 먼저 칸마다 떨어져 쌓이고,
// 그 위에 소득세(+지방소득세) 블록이 떨어진다. 둘째 줄 앞쪽에서 보험료 윗선에 점선(거의 평평) → 뒤쪽에서 소득세 블록만 주황으로 바뀌며 윗선이 가파른 손 선으로.
// 정직성: 블록 높이 = 공제 ÷ 세전 월급(calc_out 원 단위 그대로, props 스크립트가 나눔). 높이가 '금액'으로 읽히지 않게 블록마다 % 글자(11/1 심사·레드팀: % 없이는 '보험료 = 같은 돈'으로 오독).
// 연금 상한(1억 위) 칸은 '같은 비율'이 깨지므로 props에서 상한 아래 칸만 넣는다(assert). 편마다 seed로 블록 기울기·떨어지는 순서·칸 폭이 바뀐다.
// 글자는 전부 HTML(10/13 교훈). 판 전체 1.00→1.04 다가가기(U5 10/19).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type PayBlocksProps = {
  seed: string;
  cols: {label: string; ins: number[]; tax: number; insPct: string; taxPct: string}[];   // ins = 보험료 넷 몫(0~1), tax = 소득세+지방 몫 · *Pct = 화면 글자('8.9%')
  insLabel: string; taxLabel: string; axis: string;
  insAt: number; taxAt: number; flatAt: number; steepAt: number;   // 말 줄 번호 + 비율
  circleAt?: number;   // 끝 칸 손 동그라미(없으면 가파른 선 뒤) — N-3 11/4: 첫 줄이 '8천 칸부터'라 말에 맞춰 당김
  beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const INS_C = ['#5d636e', '#7b818c', '#999ea8', '#b6bac2'];   // 회색 넷 — 블록끼리 구분만, 주황 아님

export const PayBlocks: React.FC<PayBlocksProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const n = p.cols.length;
  const X0 = 470, X1 = 1650, BASE = 790, K = 2300;   // 몫 1 = 2300px(20% → 460px) · BASE 790: 아래 출처 줄(≈860)과 칸 이름이 안 겹치게(11/1 눈 검사)
  const slot = (X1 - X0) / n; const bw = slot * (0.5 + r('w') * 0.12);
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.04], CL);
  const iA = at(p.insAt), tA = at(p.taxAt), flA = at(p.flatAt), stA = at(p.steepAt);
  const order = p.cols.map((_, i) => i).sort((a, b) => (r('o' + a) - r('o' + b)) * 0.6 + (a - b) * 0.4);   // 대체로 왼쪽부터, 편마다 조금 섞임
  const drop = (start: number) => spring({frame: f - start, fps, config: {damping: 13, stiffness: 140}});
  const cx = (i: number) => X0 + slot * i + slot / 2;
  const insTop = (c: PayBlocksProps['cols'][0]) => BASE - c.ins.reduce((a, b) => a + b, 0) * K;
  const allTop = (c: PayBlocksProps['cols'][0]) => insTop(c) - c.tax * K;
  const steep = g(f, stA, 16);
  const flatP = g(f, flA, 24, Easing.inOut(Easing.cubic)), steepP = g(f, stA + 6, 26, Easing.inOut(Easing.cubic));
  const last = n - 1;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '50% 72%'}}>
      <div style={{position: 'absolute', left: X0 - 40, top: BASE, width: (X1 - X0 + 80) * g(f, 0, 20), height: 5, background: T.ink, borderRadius: 3}} />
      <div style={{position: 'absolute', left: X0 - 40, top: 300, opacity: g(f, 8, 12), ...F, fontWeight: 700, fontSize: 32, color: T.ink2, whiteSpace: 'nowrap'}}>{p.axis}</div>
      {p.cols.map((c, i) => {
        const k = order.indexOf(i);
        let y = BASE;
        const x = cx(i) - bw / 2;
        const blocks = c.ins.map((v, j) => {
          const h = v * K; y -= h;
          const s = drop(iA + k * 7 + j * 4);
          const rot = (r(`r${i}${j}`) - 0.5) * 2.4 * (1 - s * 0.6);
          return <div key={j} style={{position: 'absolute', left: x + (r(`x${i}${j}`) - 0.5) * 6, top: y - (1 - s) * 90, width: bw, height: Math.max(3, h - 3), opacity: Math.min(1, s * 1.6),
            background: INS_C[j % 4], borderRadius: 3, transform: `rotate(${rot}deg)`, boxShadow: '0 2px 0 rgba(0,0,0,0.10)'}} />;
        });
        const th = c.tax * K; const ty = y - th;
        const ts = drop(tA + k * 8);
        const trot = (r(`t${i}`) - 0.5) * 3 * (1 - ts * 0.6);
        const taxC = steep > 0 ? `rgb(${Math.round(24 + (255 - 24) * steep)},${Math.round(25 + (90 - 25) * steep)},${Math.round(29 + (0 - 29) * steep)})` : T.ink;
        return <React.Fragment key={i}>
          {blocks}
          <div style={{position: 'absolute', left: x + (r(`tx${i}`) - 0.5) * 8, top: ty - (1 - ts) * 120, width: bw, height: Math.max(4, th - 3), opacity: Math.min(1, ts * 1.6),
            background: taxC, borderRadius: 3, transform: `rotate(${trot}deg)`, boxShadow: '0 2px 0 rgba(0,0,0,0.12)'}} />
          <div style={{position: 'absolute', left: x, top: BASE - c.ins[0] * K / 2 - 22, width: bw, textAlign: 'center', opacity: g(f, iA + k * 7 + 16, 10), ...F, fontWeight: 800, fontSize: 36, color: '#ffffff', whiteSpace: 'nowrap'}}>{c.insPct}</div>
          <div style={{position: 'absolute', left: cx(i) - 120, top: ty - 84, width: 240, textAlign: 'center', opacity: g(f, tA + k * 8 + 10, 10), ...F, fontWeight: 800, fontSize: 40, color: steep > 0.5 ? T.accent : T.ink, whiteSpace: 'nowrap'}}>{c.taxPct}</div>
          <div style={{position: 'absolute', left: cx(i) - 130, top: BASE + 18, width: 260, textAlign: 'center', opacity: g(f, iA + k * 7, 10), ...F, fontWeight: 700, fontSize: 34, color: T.ink, whiteSpace: 'nowrap'}}>{c.label}</div>
        </React.Fragment>;
      })}
      {/* 왼쪽 이름 둘 — 첫 칸 블록 높이에 맞춤 */}
      <div style={{position: 'absolute', left: X0 - 360, top: (BASE + insTop(p.cols[0])) / 2 - 24, width: 300, textAlign: 'right', opacity: g(f, iA + 10, 12), ...F, fontWeight: 800, fontSize: 42, color: T.ink2, whiteSpace: 'nowrap'}}>{p.insLabel}</div>
      <div style={{position: 'absolute', left: X0 - 360, top: insTop(p.cols[0]) - 80, width: 300, textAlign: 'right', opacity: g(f, tA + 4, 12), ...F, fontWeight: 800, fontSize: 42, color: steep > 0.5 ? T.accent : T.ink, whiteSpace: 'nowrap'}}>{p.taxLabel}</div>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible', pointerEvents: 'none'}}>
        {/* 보험료 윗선 — 거의 평평한 점선 */}
        {(() => { const pts = p.cols.map((c, i) => [cx(i), insTop(c) - 2]);
          const xa = pts[0][0] - bw / 2 - 20, xb = pts[last][0] + bw / 2 + 20;
          const d = `M${xa} ${pts[0][1]} ` + pts.map((q) => `L${q[0]} ${q[1]}`).join(' ') + ` L${xb} ${pts[last][1]}`;
          return <>
            <defs><clipPath id={p.seed + '-flat'}><rect x={xa - 10} y={0} width={(xb - xa + 20) * flatP} height={1080} /></clipPath></defs>
            <path d={d} fill="none" stroke={T.ink} strokeWidth={5} strokeDasharray="14 12" clipPath={`url(#${p.seed}-flat)`} />
          </>; })()}
        {/* 소득세 윗선 — 가파른 손 선(주황) */}
        {(() => { const pts = p.cols.map((c, i) => [cx(i) + (r('h' + i) - 0.5) * 10, allTop(c) - 4]); let len = 0; for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
          const d = 'M' + pts.map((q) => `${q[0]} ${q[1]}`).join(' L');
          return <path d={d} fill="none" stroke={T.accent} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - steepP)} opacity={steepP > 0.01 ? 1 : 0} />; })()}
        <HandCircle cx={cx(last)} cy={allTop(p.cols[last]) + p.cols[last].tax * K / 2} rx={bw / 2 + 34} ry={p.cols[last].tax * K / 2 + 16} p={g(f, p.circleAt != null ? at(p.circleAt) : stA + 30, 22, Easing.inOut(Easing.quad))} />
      </svg>
    </div>
  );
};
