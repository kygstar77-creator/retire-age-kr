// 식 조각 계산서(EqStack) — 10/18 견본 방식(Sample1017 Eq)을 여러 편에 쓰는 부품으로(2026-10-18 motion). TallyFrame 자식.
// 영수증처럼 한 줄씩 쌓는다: 첫 줄(바뀌는 값) → 빼거나 더하는 조각이 말 따라 한 줄씩 → 밑줄이 그어지고 '= 답 ?'
// 라운드(rounds)마다 첫 줄 값이 바뀌고 답은 다시 '?' → 말이 답에 닿을 때(revealQ) 열리며 손 동그라미 한 번. 지난 답은 오른쪽 회색 칩으로 쌓임.
// 주황은 지금 답 하나에만. 숫자 글자는 props만(편별 props 스크립트가 calc_out·대본 assert). 글자는 전부 HTML(카메라 안 SVG 글자 어긋남 교훈 10/13).
// 편마다 seed로 계산서 x·칩 쪽(왼/오)·밑줄 모양이 바뀐다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig, Img, staticFile} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';
import {BOARD} from './TallyFrame';

export type EqTerm = {op: string; label: string; v: string; at: number};
export type EqRound = {at: number; name: string; price: string; ans: string};
export type EqStackProps = {
  seed: string; layout?: 'ledger'; baseLabel: string; blank: string; terms: EqTerm[]; ansLabel: string;
  rounds: EqRound[]; revealQ: number[]; note?: string; who?: string; beats: number[]; paper?: boolean;
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
// 글자 폭 어림(PD 굵게): 한글 1, 숫자 0.6, 쉼표·마침표 0.3, 빈칸 0.3 (em)
const em = (s: string) => [...s].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /[0-9]/.test(c) ? 0.6 : /[,.\s]/.test(c) ? 0.3 : 0.62), 0);

export const EqStack: React.FC<EqStackProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (i: number) => B[i] ?? 1e9; const len = (i: number) => (B[i + 1] ?? at(i) + 180) - at(i);
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 15}});
  const chipLeft = r('side') < 0.5;
  const X0 = chipLeft ? 760 + Math.round(r('x') * 40) : 220 + Math.round(r('x') * 40);   // 계산서 왼끝
  const W = chipLeft ? 940 : 1000; const XR = X0 + W;                                                       // 값 오른끝
  const CX = chipLeft ? 150 : 1300;                                                        // 칩 열 왼끝
  // 지금 라운드
  let ri = -1; p.rounds.forEach((d, i) => { if (f >= at(d.at)) ri = i; });
  const cur = ri >= 0 ? p.rounds[ri] : null;
  const rv = cur ? at(cur.at) + len(cur.at) * (p.revealQ[ri] ?? 0.6) : 1e9;
  const open = f >= rv; const ao = g(f, rv, 12);
  const circ = interpolate(f, [rv + 10, rv + 34], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
  const swap = cur ? g(f, at(cur.at), 12) : 0;   // 첫 줄 값이 바뀌는 순간
  const prev = ri > 0 ? p.rounds[ri - 1] : null;
  const ruleAt = Math.max(...p.terms.map((t) => at(t.at))) + 16;
  const ruleP = g(f, ruleAt, 18);
  const rowY = (i: number) => 330 + i * 84;                  // 0 첫 줄 · 1.. 조각 (보드 위 [정확한 값] 띠 아래부터)
  const yRule = rowY(p.terms.length) + 86; const yAns = yRule + 56;   // 답은 이름표 다음 줄에 오른쪽 맞춤(긴 답도 겹치지 않게)
  const lab: React.CSSProperties = {...F, fontWeight: 700, fontSize: 40, color: T.ink2, whiteSpace: 'nowrap'};
  const val: React.CSSProperties = {...F, fontWeight: 800, fontSize: 76, color: T.ink, letterSpacing: -2, whiteSpace: 'nowrap', lineHeight: 1};
  const ansZ = Math.min(116, Math.floor((W - 40) / Math.max(...p.rounds.map((d) => em(d.ans))))); const aw = em(cur?.ans ?? '?') * ansZ;
  return (
    <>
      {p.paper !== false && <div style={{position: 'absolute', left: BOARD.x, top: BOARD.y, width: BOARD.w, height: BOARD.h, borderRadius: 24, overflow: 'hidden', mixBlendMode: 'multiply', opacity: 0.85, pointerEvents: 'none'}}>
        <Img src={staticFile('paper.png')} style={{width: 1920, height: 1080, marginLeft: -BOARD.x, marginTop: -BOARD.y}} /></div>}
      {p.who && <div style={{position: 'absolute', left: X0 + W - 400, width: 400, textAlign: 'right', top: 806, ...F, fontWeight: 700, fontSize: 26, color: T.ink3, opacity: g(f, at(0))}}>{p.who}</div>}
      {/* 첫 줄: 한 채 값(라운드마다 바뀜) */}
      <div style={{position: 'absolute', left: X0, top: rowY(0) - 6, ...lab, opacity: g(f, at(0))}}>{cur ? cur.name : p.baseLabel}</div>
      <div style={{position: 'absolute', left: X0, width: W, top: rowY(0) - 18, height: 90, overflow: 'hidden', textAlign: 'right'}}>
        {prev && swap < 1 && <div style={{...val, position: 'absolute', right: 0, top: 6 - swap * 90, opacity: 1 - swap}}>{prev.price}</div>}
        <div style={{...val, position: 'absolute', right: 0, top: 6 + (cur ? (1 - swap) * 90 : 0), color: cur ? T.ink : T.ink3, opacity: cur ? swap : g(f, at(0))}}>{cur ? cur.price : `${p.blank} ?`}</div>
      </div>
      {/* 조각 줄: 말 따라 한 줄씩 떨어져 앉음 */}
      {p.terms.map((t, i) => { const o = sp(at(t.at) + 4); const y = rowY(i + 1);
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: X0, top: y - 6 - (1 - o) * 40, opacity: Math.min(1, o), display: 'flex', alignItems: 'center', gap: 18}}>
            <span style={{...F, fontWeight: 800, fontSize: 64, color: T.ink3, width: 44, textAlign: 'center', lineHeight: 1}}>{t.op}</span><span style={lab}>{t.label}</span></div>
          <div style={{position: 'absolute', left: X0, width: W, top: y - 12 - (1 - o) * 40, textAlign: 'right', opacity: Math.min(1, o), ...val}}>{t.v}</div>
        </React.Fragment>; })}
      {/* 밑줄(영수증 점선 → 실선) */}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {ruleP > 0.01 && <line x1={X0} x2={X0 + W * ruleP} y1={yRule} y2={yRule} stroke={T.ink} strokeWidth={r('rule') < 0.5 ? 5 : 4} strokeDasharray={r('rule') < 0.5 ? undefined : '14 8'} strokeLinecap="round" />}
      </svg>
      {/* 답 줄 */}
      <div style={{position: 'absolute', left: X0, top: yRule + 18, opacity: ruleP, display: 'flex', alignItems: 'center', gap: 18}}>
        <span style={{...F, fontWeight: 800, fontSize: 52, color: T.ink3, width: 44, textAlign: 'center', lineHeight: 1}}>=</span><span style={{...lab, fontSize: 36, color: T.ink}}>{p.ansLabel}</span></div>
      <div style={{position: 'absolute', left: X0, width: W, top: yAns + 20, textAlign: 'right', opacity: ruleP}}>
        {!open ? <span style={{...F, fontWeight: 800, fontSize: ansZ, color: T.ink3, lineHeight: 1.05}}>?</span>
          : <span style={{display: 'inline-block', ...F, fontWeight: 800, fontSize: ansZ, color: T.accent, letterSpacing: -4, lineHeight: 1.05, opacity: ao, transform: `scale(${0.9 + 0.1 * ao})`, transformOrigin: '100% 50%', whiteSpace: 'nowrap'}}>{cur!.ans}</span>}
      </div>
      {open && <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
        <HandCircle cx={XR - aw / 2} cy={yAns + 20 + ansZ * 0.54} rx={aw / 2 + 40} ry={ansZ * 0.62} p={circ} /></svg>}
      {/* 지난 답 칩(회색) — 다음 라운드가 열리면 지금 답이 칩으로 옮겨 감 */}
      {p.rounds.map((d, i) => { if (i >= ri) return null; const o = sp(at(p.rounds[i + 1].at)); const y = 330 + i * 140;
        return <div key={i} style={{position: 'absolute', left: CX, top: y + (1 - Math.min(1, o)) * 60, width: 470, opacity: Math.min(1, o), background: T.bg, border: `2px solid ${T.line}`, borderRadius: 16, padding: '16px 24px'}}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink3, whiteSpace: 'nowrap'}}>{d.name} {d.price}</div>
          <div style={{...F, fontWeight: 800, fontSize: 50, color: T.ink2, letterSpacing: -1, whiteSpace: 'nowrap', marginTop: 4}}>{d.ans} 더</div>
        </div>; })}
      {p.note && <div style={{position: 'absolute', left: X0, top: 806, ...F, fontWeight: 700, fontSize: 30, color: T.ink2, opacity: ruleP}}>{p.note}</div>}
    </>
  );
};
