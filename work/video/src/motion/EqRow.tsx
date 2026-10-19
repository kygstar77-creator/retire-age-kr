// 가로식 계산(EqRow) — EqStack(세로 영수증)의 변주(2026-10-19 motion, T-1용). TallyFrame 자식.
// 한 줄 식이 말 따라 조각마다 붙는다: 값 → 연산 → 값 → '= ?' → 말이 답에 닿을 때 주황으로 열리고 손 동그라미 한 번.
// 줄(row)이 바뀌면 지난 식은 작은 회색 줄로 위(또는 아래)에 쌓인다. 주황은 지금 답 하나에만.
// 조각 시각 at = 말 줄 번호 + 줄 안 비율(1.4 = 둘째 줄 40% 자리). 숫자 글자는 props만(편별 props 스크립트가 calc·대본 assert).
// 글자는 전부 HTML(카메라 안 SVG 글자 어긋남 교훈 10/13). 판 전체 1.00→1.03 다가가기(U5 같은 화면 8초 교훈 10/19).
// 편마다 seed로 정렬(왼/가운데)·지난 줄 쪽(위/아래)·답 밑줄 모양이 바뀐다(반복 템플릿 신호 피하기).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig, Img, staticFile} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';
import {BOARD} from './TallyFrame';

export type EqPart = {t: string; sub?: string; op?: boolean; at: number};
export type EqLine = {label: string; parts: EqPart[]; ans: string; reveal: number; ansSub?: string};
export type EqRowProps = {seed: string; rows: EqLine[]; note?: string; who?: string; beats: number[]; paper?: boolean; tail?: {at: number; text: string}};   // tail = 끝 검은 카드 한 장(식 뒤 단서·한계)

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
// 글자 폭 어림(PD 굵게): 한글 1, 숫자 0.6, 쉼표·마침표 0.3, 빈칸 0.3 (em)
const em = (s: string) => [...s].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /[0-9]/.test(c) ? 0.6 : /[,.\s]/.test(c) ? 0.3 : 0.62), 0);
// 값 조각 바탕(계산기 키) — 판(종이 결 ~238)보다 24단계 넘게 어두워야 U5가 '바뀜'으로 셈(10/19 year 첫 8초)
const KEY = '#c9d0da';   // #d9dee6은 160×90 회색에서 판과 17단계 차이뿐이라 안 셈(10/19 실측)
const GAP = 0.7;    // 조각 사이 (em) — 0.45는 렌더에서 '48%−'처럼 붙음(10/19 눈 검사)

export const EqRow: React.FC<EqRowProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 14}});
  const center = r('align') < 0.5; const histTop = r('hist') < 0.6; const solid = r('rule') < 0.5;
  const L = 170, W = 1580;
  // 지금 줄
  let ri = 0; p.rows.forEach((row, i) => { if (i > 0 && f >= at(row.parts[0].at)) ri = i; });
  const cur = p.rows[ri];
  const toks = [...cur.parts.map((q) => ({...q, w: em(q.t) * (q.op ? 1 : 1.1)})),   // 값 1.1배: '만원'·'%p' 실제 폭이 어림보다 넓어 키 칸이 '='를 덮음(10/19 T-1 렌더 겹침)
    {t: '=', op: true, at: cur.parts[cur.parts.length - 1].at + 0.12, w: em('=')}];
  const ansW = Math.max(em(cur.ans) * 1.15, 1.6);   // 짧은 답('16%')은 어림보다 넓어 칸 끝에 붙음(10/19 심사)
  const totalEm = toks.reduce((a, q) => a + q.w + GAP, 0) + ansW + 0.3;   // 0.3 = '='와 손 동그라미 사이
  const PAD = 48; const nV = cur.parts.filter((q) => !q.op).length;   // 값 조각 = 계산기 키 칸(옆 여백 24씩)
  const Z = Math.min(104, Math.floor((W * 0.84 - (PAD + 28) * nV) / totalEm));   // 폭 어림이 실제보다 좁아 0.84 여유(10/19 ratio 답 동그라미가 판 끝에 닿음)
  let x = center ? L + (W - totalEm * Z) / 2 : L;
  const hist = p.rows.slice(0, ri);
  const yCur = p.rows.length === 1 ? 460 : histTop ? 300 + Math.max(1, p.rows.length - 1) * 70 + 110 : 400;
  const yHist = (i: number) => histTop ? 318 + i * 70 : yCur + Z + 150 + i * 64;
  const rv = at(cur.reveal); const open = f >= rv; const ao = g(f, rv, 12);
  const circ = interpolate(f, [rv + 10, rv + 34], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
  const rowIn = ri > 0 ? g(f, at(cur.parts[0].at), 16) : 1;
  const endF = (B[B.length - 1] ?? 0) + 150; const push = interpolate(f, [0, endF], [1, 1.05], CL);   // 장면 길이에 맞춰 1.00→1.05(10/19 U5: 600f에 1.03은 느려서 8.5초 걸림)
  const val: React.CSSProperties = {...F, fontWeight: 800, fontSize: Z, color: T.ink, letterSpacing: -2, whiteSpace: 'nowrap', lineHeight: 1};
  const subS: React.CSSProperties = {...F, fontWeight: 700, fontSize: Math.max(28, Math.round(Z * 0.34)), color: T.ink2, whiteSpace: 'nowrap', marginTop: 14};
  // 값 칸 뒤 +28: 폭 어림보다 실제 글자가 넓어 칸이 '='를 가림(10/19 눈 검사)
  const items = toks.map((q, i) => { const x0 = x; x += (q.w + GAP) * Z + (q.op ? 0 : PAD + 28); const o = q.op ? g(f, at(q.at), 10) : sp(at(q.at));
    return <div key={`${ri}-${i}`} style={{position: 'absolute', left: x0, top: yCur + (q.op ? 0 : (1 - Math.min(1, o)) * 36), opacity: Math.min(1, o)}}>
      <div style={{...val, color: q.op ? T.ink3 : T.ink, transform: q.op ? `scale(${0.7 + 0.3 * o})` : undefined,
        ...(q.op ? {} : {background: KEY, borderRadius: 20, padding: `${Math.round(Z * 0.16)}px 24px`, margin: `-${Math.round(Z * 0.16)}px 0 0 -24px`})}}>{q.t}</div>
      {q.sub && <div style={subS}>{q.sub}</div>}
    </div>; });
  const ax = x + 0.45 * Z; const aw = ansW * Z; const ansShow = g(f, at(toks[toks.length - 1].at) + 4, 12);
  return (
    <>
      {p.paper !== false && <div style={{position: 'absolute', left: BOARD.x, top: BOARD.y, width: BOARD.w, height: BOARD.h, borderRadius: 24, overflow: 'hidden', mixBlendMode: 'multiply', opacity: 0.85, pointerEvents: 'none'}}>
        <Img src={staticFile('paper.png')} style={{width: 1920, height: 1080, marginLeft: -BOARD.x, marginTop: -BOARD.y}} /></div>}
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: `${BOARD.x + BOARD.w / 2}px ${BOARD.y + BOARD.h / 2}px`}}>
        {/* 지난 줄(회색 한 줄) */}
        {hist.map((h, i) => { const o = sp(at(p.rows[i + 1].parts[0].at));
          return <div key={i} style={{position: 'absolute', left: center ? L : L, width: W, textAlign: center ? 'center' : 'left', top: yHist(i) + (1 - Math.min(1, o)) * (histTop ? 40 : -40), opacity: Math.min(1, o), ...F, fontWeight: 700, fontSize: 40, color: T.ink3, whiteSpace: 'nowrap'}}>
            <span style={{fontSize: 30, marginRight: 22}}>{h.label}</span>{h.parts.map((q) => q.t).join(' ')} = <span style={{fontWeight: 800, color: T.ink2}}>{h.ans}</span></div>; })}
        {/* 지금 줄 이름표 */}
        <div style={{position: 'absolute', left: center ? L : L, width: W, textAlign: center ? 'center' : 'left', top: yCur - 66, opacity: rowIn * g(f, at(cur.parts[0].at) - 6), ...F, fontWeight: 700, fontSize: 36, color: T.ink2, whiteSpace: 'nowrap'}}>{cur.label}</div>
        <div style={{opacity: rowIn}}>
          {/* 답 바탕은 글자 밑에 — 위에 그리면 겹침 관문이 답 숫자를 '가려짐'으로 셈(10/19 T-1 렌더 25건) */}
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
            {open && <rect x={ax - 36} y={yCur - Z * 0.22} width={aw + 72} height={Z * 1.44} rx={22} fill={T.soft} opacity={ao} />}
          </svg>
          {items}
          {/* 답 칸: '?' → 주황 답 */}
          <div style={{position: 'absolute', left: ax, top: yCur, width: aw, opacity: ansShow}}>
            {!open ? <div style={{...val, color: T.ink3, textAlign: 'center'}}>?</div>
              : <div style={{...val, color: T.accent, letterSpacing: -3, opacity: ao, transform: `scale(${0.9 + 0.1 * ao})`, transformOrigin: '0% 50%'}}>{cur.ans}</div>}
            {open && cur.ansSub && <div style={{...subS, opacity: ao, color: T.ink2}}>{cur.ansSub}</div>}
          </div>
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
            {!open && ansShow > 0.01 && <line x1={ax} x2={ax + aw * ansShow} y1={yCur + Z + 8} y2={yCur + Z + 8} stroke={T.ink3} strokeWidth={4} strokeDasharray={solid ? undefined : '12 8'} strokeLinecap="round" />}
            {open && <HandCircle color={p.tail && f >= at(p.tail.at) ? T.ink3 : undefined} cx={ax + aw / 2} cy={yCur + Z * 0.5} rx={aw / 2 + 36} ry={Z * 0.72} p={circ} />}
          </svg>
        </div>
        {p.tail && (() => { const o = sp(at(p.tail.at)); return <div style={{position: 'absolute', left: L, width: W, top: 640 + (1 - Math.min(1, o)) * 40, opacity: Math.min(1, o), textAlign: center ? 'center' : 'left'}}>
          <span style={{display: 'inline-block', background: T.ink, color: '#fff', borderRadius: 18, padding: '18px 34px', ...F, fontWeight: 800, fontSize: 46, whiteSpace: 'nowrap'}}>{p.tail.text}</span></div>; })()}
        {p.note && <div style={{position: 'absolute', left: L, width: W, textAlign: center ? 'center' : 'left', top: 760, ...F, fontWeight: 700, fontSize: 30, color: T.ink2, opacity: g(f, at(0) + 20)}}>{p.note}</div>}
        {p.who && <div style={{position: 'absolute', left: L + W - 500, width: 500, textAlign: 'right', top: 806, ...F, fontWeight: 700, fontSize: 26, color: T.ink3, opacity: g(f, at(0))}}>{p.who}</div>}
      </div>
    </>
  );
};
