// 거꾸로 계단(RaiseStairs) — N-3 '5. 거꾸로: 통장 300만원이 되려면' 통장 100만원씩 올릴 때 필요한 연봉(2026-11-01 motion, shot_plan r28). TallyFrame 자식.
// 가로 = 통장 목표(같은 폭 = 같은 100만원), 세로 = 필요한 연봉. 첫 칸(300만원)은 앞 장면에서 말한 값이라 처음부터 서 있고,
// 말 따라 한 칸씩 솟아오른다(연봉 글자는 '?'로 서 있다가 말이 닿을 때 열림). '칸 사이' 줄부터 칸마다 앞 칸보다 더 솟은 부분(챌면)을 진하게 칠하고
// 그 안에 연봉 차를 흰 글자로 — 맨 위 차 하나만 주황 + 손 동그라미. 끝 줄에선 통장 목표 글자 밑에 같은 폭 손 밑줄이 차례로(흰 '+100만원'을 칸 안에 두면 칸 아랫부분이 100만원처럼 읽힘 — 11/1 레드팀).
// 정직성: 칸 높이 = 연봉(만원)을 0원부터 비례로(11/1 심사: 바닥을 첫 칸 값으로 자르면 9,100이 4,100의 6배로 읽힘 — 실제 2.2배). 솟은 차도 그대로 비례.
// 숫자 글자는 props만(편별 props 스크립트가 calc_out·대본 assert). 편마다 seed로 계단 방향(왼→오/오→왼)·칸 폭·솟는 탄성이 바뀐다.
// 글자는 전부 HTML(10/13 교훈). 판 전체 1.00→1.04 다가가기(U5 10/19).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';
import {HandUnderline} from '../parts/human';

export type RaiseStairsProps = {
  seed: string;
  steps: {goal: string; pay: string; v: number; at: number; openAt: number}[];   // v = 연봉(만원), at = 솟는 줄, openAt = 연봉 열리는 줄
  gaps: {text: string; at: number}[];                                             // steps[i] → steps[i+1] 차, 마지막 = 답(주황)
  gapAt: number;                                                                  // 챌면 칠하기 시작
  unitAt: number;                                                                 // 끝 줄 — 통장 목표 글자 밑 손 밑줄(같은 폭 = 같은 100만원)
  axis: string;
  beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

export const RaiseStairs: React.FC<RaiseStairsProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const n = p.steps.length;
  const flip = r('dir') < 0.35;   // 편마다 가끔 오른쪽에서 왼쪽으로 오른다
  const W = 300 + Math.round(r('w') * 40), X0 = (1920 - W * n) / 2, BASE = 780;   // BASE 780: 출처 줄과 안 겹치게(11/1 눈 검사)
  const K = 470 / p.steps[n - 1].v;   // 0원 → 맨 위 칸 470px(맨 위 연봉 글자가 제목에 안 닿는 높이)
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.04], CL);
  const xOf = (i: number) => X0 + W * (flip ? n - 1 - i : i);
  const topOf = (i: number) => BASE - p.steps[i].v * K;
  const damp = 11 + r('d') * 5;
  const grow = (i: number) => i === 0 ? 1 : spring({frame: f - at(p.steps[i].at), fps, config: {damping: damp, stiffness: 120}});
  const gA = at(p.gapAt);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: flip ? '30% 70%' : '70% 70%'}}>
      <div style={{position: 'absolute', left: X0 - 40, top: 290, opacity: g(f, 8, 12), ...F, fontWeight: 700, fontSize: 32, color: T.ink2, whiteSpace: 'nowrap'}}>{p.axis}</div>
      <div style={{position: 'absolute', left: X0 - 40, top: BASE, width: (W * n + 80) * g(f, 0, 20), height: 5, background: T.ink, borderRadius: 3}} />
      {p.steps.map((s, i) => {
        const gr = grow(i);
        const fullH = BASE - topOf(i);
        const prevH = i === 0 ? fullH : BASE - topOf(i - 1);
        const h = i === 0 ? fullH : prevH * Math.min(1, gr * 3) + (fullH - prevH) * gr;   // 앞 칸 높이까지 먼저, 그다음 차만큼 솟음
        const show = i === 0 ? 1 : g(f, at(s.at), 6);
        const x = xOf(i);
        const isAns = i === n - 1;
        const gp = i > 0 ? g(f, gA + (i - 1) * 10, 14) : 0;
        const riseH = fullH - prevH;
        const op = g(f, at(s.openAt), 10);
        const gapAns = i === n - 1;
        const gText = i > 0 ? p.gaps[i - 1] : null;
        const gO = gText ? g(f, at(gText.at), 12) : 0;
        return <React.Fragment key={i}>
          {/* 칸 몸통 */}
          <div style={{position: 'absolute', left: x + 2, top: BASE - h, width: W - 4, height: h, opacity: show, background: T.ink2, borderRadius: '4px 4px 0 0'}} />
          {/* 앞 칸보다 더 솟은 부분 */}
          {i > 0 && <div style={{position: 'absolute', left: x + 2, top: BASE - h, width: W - 4, height: Math.max(0, riseH * gr), opacity: gp,
            background: gapAns && gO > 0.5 ? T.accent : T.ink, borderRadius: '4px 4px 0 0'}} />}
          {gText && <div style={{position: 'absolute', left: x, top: BASE - h + riseH * gr / 2 - 34, width: W, textAlign: 'center', opacity: gO * show, ...F, fontWeight: 800, fontSize: 52, color: '#ffffff', letterSpacing: -1, whiteSpace: 'nowrap'}}>{gText.text}</div>}
          {/* 연봉 — '?' → 열림 */}
          <div style={{position: 'absolute', left: x - 20, top: BASE - h - 92, width: W + 40, textAlign: 'center', opacity: show, ...F, fontWeight: 800, fontSize: isAns ? 66 : 58, color: T.ink, letterSpacing: -1.5, whiteSpace: 'nowrap'}}>
            <span style={{opacity: 1 - op, position: 'absolute', left: 0, right: 0}}>?</span>
            <span style={{opacity: op, display: 'inline-block', transform: `scale(${0.85 + 0.15 * op})`}}>{s.pay}</span>
          </div>
          {/* 통장 목표 */}
          <div style={{position: 'absolute', left: x, top: BASE + 16, width: W, textAlign: 'center', opacity: show, ...F, fontWeight: 700, fontSize: 36, color: T.ink, whiteSpace: 'nowrap'}}>{s.goal}</div>
        </React.Fragment>;
      })}
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible', pointerEvents: 'none'}}>
        {p.steps.map((_, i) => i > 0 ? <HandUnderline key={i} x={xOf(i) + 40} y={BASE + 56} w={W - 80} p={g(f, at(p.unitAt) + (i - 1) * 9, 14)} color={T.ink2} seed={i} stroke={5} /> : null)}
        {(() => { const i = n - 1; const top = topOf(i), mid = BASE - (BASE - topOf(i - 1));
          return <HandCircle cx={xOf(i) + W / 2} cy={(top + mid) / 2} rx={W / 2 - 6} ry={(mid - top) / 2 + 12} p={g(f, at(p.gaps[n - 2].at) + 16, 22, Easing.inOut(Easing.quad))} />; })()}
      </svg>
    </div>
  );
};
